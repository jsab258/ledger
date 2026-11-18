import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import item_tags as it  # noqa: E402

T = dt.datetime(2026, 11, 18, 8, 0)


def lines(p, rows):
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return str(p)


def test_code_in():
    assert it.code_in("n16-1 Kiln") == "n16-1"
    assert it.code_in("tool loop: Kiln round 6 (n09-6 clothing)") == "n09-6"
    assert it.code_in("[n16-10] backup") == "n16-10"
    assert it.code_in("n02-3-3-stutter") == "n02-3"
    assert it.code_in("kn16-1") is None
    assert it.code_in("n16-123") is None
    assert it.code_in("tool loop: kiln round 4") is None
    assert it.code_in(None) is None


def test_current_item_roundtrip(tmp_path):
    p = str(tmp_path / "cur.json")
    assert it.read_current(p) is None
    it.set_current("n16-1", "Kiln", path=p, at=T)
    assert it.read_current(p) == "n16-1"
    try:
        it.set_current("kiln", path=p)
        assert False
    except SystemExit:
        pass


def test_session_hook_writes_item(tmp_path):
    cur, log = str(tmp_path / "c.json"), str(tmp_path / "t.jsonl")
    it.set_current("n16-3", path=cur, at=T)
    row = it.hook_session({"session_id": "s1", "source": "startup"}, timelog=log, current=cur, at=T)
    assert row["item"] == "n16-3" and row["event"] == "start" and row["task"].startswith("n16-3")
    assert json.loads(open(log).read())["item"] == "n16-3"
    assert it.hook_session({"agent_id": "a1"}, timelog=log, current=cur) is None


def test_session_hook_without_current_is_untagged(tmp_path):
    log = str(tmp_path / "t.jsonl")
    row = it.hook_session({"source": "compact"}, timelog=log, current=str(tmp_path / "none.json"), at=T)
    assert row["item"] == "untagged" and row["auto"] == "session-compact"


def test_helper_hook_prefixes_current_item(tmp_path):
    cur, hp = str(tmp_path / "c.json"), str(tmp_path / "h.jsonl")
    it.set_current("n16-1", path=cur, at=T)
    out, row = it.hook_helper({"tool_name": "Agent", "tool_input": {"description": "drape review", "prompt": "check it", "subagent_type": "general-purpose"}},
                              helpers=hp, current=cur, at=T)
    upd = out["hookSpecificOutput"]["updatedInput"]
    assert upd["description"] == "[n16-1] drape review" and upd["prompt"] == "check it" and upd["subagent_type"] == "general-purpose"
    assert row["item"] == "n16-1"


def test_helper_hook_keeps_own_code(tmp_path):
    cur, hp = str(tmp_path / "c.json"), str(tmp_path / "h.jsonl")
    it.set_current("n16-1", path=cur, at=T)
    out, row = it.hook_helper({"tool_name": "Agent", "tool_input": {"description": "n16-6 bench leg 2"}}, helpers=hp, current=cur, at=T)
    assert out is None and row["item"] == "n16-6"
    out, row = it.hook_helper({"tool_name": "Agent", "tool_input": {"description": "bench", "prompt": "for n16-6, run"}}, helpers=hp, current=cur, at=T)
    assert out["hookSpecificOutput"]["updatedInput"]["description"] == "[n16-6] bench" and row["item"] == "n16-6"


def test_helper_hook_ignores_other_tools(tmp_path):
    assert it.hook_helper({"tool_name": "Bash", "tool_input": {}}, helpers=str(tmp_path / "h"), current=str(tmp_path / "c")) == (None, None)


def test_helper_hook_no_current_no_rewrite(tmp_path):
    out, row = it.hook_helper({"tool_name": "Task", "tool_input": {"description": "x"}}, helpers=str(tmp_path / "h"), current=str(tmp_path / "c"), at=T)
    assert out is None and row["item"] == "untagged"


def _log(tmp_path):
    return lines(tmp_path / "t.jsonl", [
        {"event": "start", "at": "2026-11-18T08:00:00", "task": "tool loop: kiln round 11", "item": "n16-1"},
        {"event": "stop", "at": "2026-11-18T09:00:00"},
        {"event": "start", "at": "2026-11-18T09:10:00", "task": "n16-6 bench leg 2"},
        {"event": "start", "at": "2026-11-18T09:40:00", "task": "records and the row"},
        {"event": "stop", "at": "2026-11-18T10:00:00"},
    ])


def test_windows_carry_items(tmp_path):
    wins, last = it.windows(_log(tmp_path))
    assert [w[2] for w in wins] == ["n16-1", "n16-6", "untagged"]
    assert last == dt.datetime(2026, 11, 18, 10, 0)


def test_attribution_order(tmp_path):
    wins, last = it.windows(_log(tmp_path))
    at = lambda h, m: dt.datetime(2026, 11, 18, h, m)  # noqa: E731
    assert it.attribute(at(8, 30), wins, last) == "n16-1"
    assert it.attribute(at(8, 30), wins, last, helper_desc="[n16-6] bench") == "n16-6"   # helper's own code first
    assert it.attribute(at(9, 5), wins, last, current="n16-1") == "untagged"            # a gap inside the log stays untagged
    assert it.attribute(at(9, 20), wins, last) == "n16-6"
    assert it.attribute(at(9, 50), wins, last) == "untagged"
    assert it.attribute(at(11, 0), wins, last, current="n16-1") == "n16-1 (current item, inferred)"
    assert it.attribute(at(11, 0), wins, last) == "untagged"


def test_open_window_runs_on(tmp_path):
    p = lines(tmp_path / "t.jsonl", [{"event": "start", "at": "2026-11-18T08:00:00", "task": "n16-1 Kiln"}])
    wins, last = it.windows(p)
    assert it.attribute(dt.datetime(2026, 11, 18, 11, 59), wins, last, current="n16-3") == "n16-1"
    # after OPEN_LIMIT_H hours the open window ends; later steps fall to the current item, inferred
    assert it.attribute(dt.datetime(2026, 11, 18, 12, 30), wins, last, current="n16-3") == "n16-3 (current item, inferred)"


def test_kiln_share_counts_by_code_not_name(tmp_path):
    wins, last = it.windows(_log(tmp_path))
    at = lambda h, m: dt.datetime(2026, 11, 18, h, m)  # noqa: E731
    steps = [(at(8, 10), 3.0, None),                       # session in the Kiln window
             (at(9, 20), 1.0, "[n16-1] seam review"),      # Kiln helper during the bench window: Kiln
             (at(9, 20), 2.0, None),                       # bench
             (at(9, 50), 1.0, "drape check, kiln"),        # names kiln but no code: untagged, not Kiln
             (at(11, 0), 3.0, None)]                       # after the log's end: current item, inferred
    by = it.split(steps, wins, last, current="n16-1")
    assert by == {"n16-1": 4.0, "n16-6": 2.0, "untagged": 1.0, "n16-1 (current item, inferred)": 3.0}
    k, total, u = it.kiln_share(by, {"n16-1", "n09-6"})
    assert (k, total, u) == (7.0, 10.0, 1.0)
    line = it.kiln_line(k, total, u, dt.datetime(2026, 11, 16))
    assert "70.0%" in line and "untagged US$1.00 (10.0%)" in line
    assert it.kiln_line(k, total, u, dt.datetime(2026, 11, 16), cap=60).startswith("KILN OVER 60%")
    assert it.kiln_line(0, 0, 0, dt.datetime(2026, 11, 16)).endswith("(0.0%)")


def test_kiln_items_file():
    ks = it.kiln_items()
    assert "n16-1" in ks and "n09-6" in ks


def test_hourly_line():
    line = it.hourly_line({"n16-1": 3.0, "n16-6": 1.25, "untagged": 0.001}, "07:15")
    assert line == "By item since 07:15 (US$4.25): n16-1 US$3.00; n16-6 US$1.25"
    assert it.hourly_line({}, "07:15").endswith("nothing spent")


def test_since_time_across_midnight():
    assert it.since_time("23:30", dt.datetime(2026, 11, 18, 0, 10)) == dt.datetime(2026, 11, 17, 23, 30)


def test_cli_hooks_never_block(tmp_path, monkeypatch, capsys):
    import io as _io
    monkeypatch.setattr(sys, "stdin", _io.StringIO("not json"))
    assert it.main(["hook-helper"]) == 0
    assert capsys.readouterr().out == ""


def test_real_time_log_parses():
    wins, last = it.windows()
    assert wins and last is not None
    tagged = sum(1 for w in wins if w[2] != "untagged")
    assert 0 < tagged <= len(wins)


def test_compact_or_resume_keeps_the_open_task(tmp_path):
    cur, log = str(tmp_path / "c.json"), str(tmp_path / "t.jsonl")
    it.set_current("n16-1", path=cur, at=T)
    lines(tmp_path / "t.jsonl", [{"event": "start", "at": "2026-11-18T09:00:00", "task": "n16-6 bench", "phase": "2", "kind": "production"}])
    assert it.hook_session({"source": "compact"}, timelog=log, current=cur, at=dt.datetime(2026, 11, 18, 9, 30)) is None
    assert it.hook_session({"source": "resume"}, timelog=log, current=cur, at=dt.datetime(2026, 11, 18, 9, 31)) is None
    wins, _ = it.windows(log)
    assert it.item_at(wins, dt.datetime(2026, 11, 18, 9, 45)) == "n16-6"
    assert it.hook_session({"source": "startup"}, timelog=log, current=cur, at=dt.datetime(2026, 11, 18, 10, 0))["item"] == "n16-1"


def test_helper_hook_returns_the_whole_input(tmp_path):
    cur, hp = str(tmp_path / "c.json"), str(tmp_path / "h.jsonl")
    it.set_current("n16-1", path=cur, at=T)
    inp = {"description": "x", "prompt": "p", "subagent_type": "Explore", "model": "sonnet", "run_in_background": True}
    out, _ = it.hook_helper({"tool_name": "Agent", "tool_input": inp}, helpers=hp, current=cur, at=T)
    upd = out["hookSpecificOutput"]["updatedInput"]
    assert upd == dict(inp, description="[n16-1] x")


def test_odd_payloads_and_files_do_not_crash(tmp_path, monkeypatch, capsys):
    import io as _io
    monkeypatch.setattr(it, "HELPERS", str(tmp_path / "h.jsonl"))
    monkeypatch.setattr(it, "CURRENT", str(tmp_path / "none.json"))
    for text in ("[1, 2]", "null", '{"tool_name": "Agent", "tool_input": {"description": null, "prompt": 5}}'):
        monkeypatch.setattr(sys, "stdin", _io.StringIO(text))
        assert it.main(["hook-helper"]) == 0
    p = tmp_path / "c.json"
    for text in ("[1]", '{"item": 5}'):
        p.write_text(text, encoding="utf-8")
        assert it.read_current(str(p)) is None
    assert it.code_in(5) is None


def test_attribution_matches_token_audit(tmp_path):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import token_audit as ta
    p = lines(tmp_path / "t.jsonl", [                                  # unsorted and overlapping, as the real log
        {"event": "stop", "at": "2026-11-18T07:00:00"},                # a stop with no start
        {"event": "start", "at": "2026-11-18T09:00:00", "task": "n16-6 a"},
        {"event": "stop", "at": "2026-11-18T09:59:00"},
        {"event": "start", "at": "2026-11-18T09:20:00+01:00", "task": "n16-1 b"},
        {"event": "stop", "at": "2026-11-18T10:02:00"}])
    wins, _ = it.windows(p)
    tw = ta.task_windows(p)
    t = dt.datetime(2026, 11, 18, 6, 50)
    while t < dt.datetime(2026, 11, 18, 10, 10):
        assert (it.item_at(wins, t) is None) == (ta.item_at(tw, t) == "not in the time log"), t
        t += dt.timedelta(minutes=1)
    assert it.item_at(wins, dt.datetime(2026, 11, 18, 9, 59)) is None   # the 09:59 stop closed n16-1 in both


def test_kiln_share_cli_fails_over_the_cap(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(it, "steps_from_logs", lambda a, b=None: [(dt.datetime(2026, 11, 18, 8, 10), 1.0, "[n16-1] x"),
                                                                     (dt.datetime(2026, 11, 18, 8, 20), 1.0, None)])
    assert it.main(["kiln-share", "2026-11-18"]) == 1
    assert capsys.readouterr().out.startswith("KILN OVER 15%")


def test_two_codes_take_the_first():
    assert it.code_in("n16-6 after n16-1") == "n16-6"
