"""Checks for the panel on recordings (lane task 4t, piece 6). No model, no browser: a made-up session of plain frames."""
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "panel"))
import panel  # noqa: E402


def fake_session(tmp, n=90, step_min=0.5):
    shots, hidden = tmp / "sess", tmp / "hid"
    (shots / "shots").mkdir(parents=True)
    hidden.mkdir()
    with open(hidden / "actions.jsonl", "w") as f:
        f.write(json.dumps({"n": 0, "seed": 7}) + "\n")
        for i in range(1, n + 1):
            p = shots / "shots" / ("%04d.png" % i)
            Image.new("RGB", (96, 54), (i % 255, 40, 80)).save(p)
            words = {"obj": "Find the place"}
            if i == 30:
                words["dialog"] = "A LONG SPEECH " + " ".join("word%d" % k for k in range(40))
            f.write(json.dumps({"n": i, "minute": round(i * step_min, 2), "action": "hold KeyW 3", "words": words,
                                "shot": "/somewhere/else/%04d.png" % i, "hidden": {"state": {"secret": 1}}}) + "\n")
    return shots, hidden


def test_strip_whole_session_capped_and_blind(tmp_path):
    shots, hidden = fake_session(tmp_path)
    ans = tmp_path / "ans.json"
    ans.write_text(json.dumps({"best_moment": {"minute": 10, "what": "PLAYER WORDS"}, "worst_moment": {"minute": 40},
                               "faults": [{"minute": 20}], "quit": True, "quit_minute": 44, "review": "PLAYER WORDS"}))
    out = tmp_path / "pk" / "p1"
    panel.main(["strip", "--shots", str(shots), "--hidden", str(hidden), "--out", str(out), "--answer", str(ans)])
    sheets = sorted(os.listdir(out / "sheets"))
    strips = [s for s in sheets if s.startswith("strip")]
    clips = [s for s in sheets if s.startswith("clip")]
    assert 1 <= len(strips) <= 4 and 1 <= len(clips) <= panel.MAX_CLIPS
    text = "".join(open(os.path.join(dp, f), errors="ignore").read() for dp, _, fs in os.walk(out) for f in fs if f.endswith(".md"))
    assert "PLAYER WORDS" not in text and "secret" not in text   # the judge never sees the player's words or hidden state
    side = json.load(open(tmp_path / "pk" / "p1.moments.json"))
    assert {c["why"] for c in side["clips"]} >= {"best_moment", "worst_moment", "fault", "quit"}
    assert not (out / "p1.moments.json").exists()


def test_strip_spacing_covers_session():
    rows = [{"n": i, "minute": i * 0.25, "shot": __file__} for i in range(1, 400)]   # about 100 minutes
    picked = panel.pick_strip(rows, "")
    assert len(picked) <= panel.MAX_STRIP_FRAMES
    assert picked[0]["minute"] == 0.25 and picked[-1]["minute"] >= rows[-1]["minute"] - 3


def write(d, name, obj):
    d.mkdir(exist_ok=True)
    (d / (name + ".json")).write_text(json.dumps(obj))


def test_pair_winner_must_hold_in_both_orders_and_labels_hidden(tmp_path):
    a, b = tmp_path / "before", tmp_path / "after"
    for d, lab in ((a, "loop 1 BEFORE, the rusher"), (b, "loop 2 AFTER, the rusher")):
        d.mkdir()
        (d / "PACKET.md").write_text("# Recording packet: %s\n\nx\n" % lab)
        (d / "LOG.md").write_text("# log\n\n%s. Minute played\n" % lab)
    keys = tmp_path / "keys"
    keys.mkdir()
    out = tmp_path / "pairout"
    panel.main(["pair", "--a", str(a), "--b", str(b), "--out", str(out), "--key", str(keys / "p1.key.json"), "--seed", "3"])
    alltext = "".join(open(os.path.join(dp, f)).read() for dp, _, fs in os.walk(out) for f in fs if f.endswith(".md"))
    assert "BEFORE" not in alltext and "AFTER" not in alltext and "loop" not in alltext
    assert "p1/order1" in (out / "order1" / "PAIR.md").read_text()
    key = json.load(open(keys / "p1.key.json"))
    o1, o2 = key["orders"]["order1"], key["orders"]["order2"]
    assert {o1, o2} == {"A", "B"}
    other = {"A": "B", "B": "A"}
    ans = tmp_path / "ans"
    # judge 1 picks the after version in both orders (and on tension); judge 2 always says "A" (position bias): a tie
    write(ans, "j1a", {"judge": "1", "pair": "p1/order1", "better": o1, "axes": {"tension": o1, "hands_busy": "A"}})
    write(ans, "j1b", {"judge": "1", "pair": "p1/order2", "better": o2, "axes": {"tension": o2, "hands_busy": "A"}})
    write(ans, "j2a", {"judge": "2", "pair": "p1/order1", "better": "A"})
    write(ans, "j2b", {"judge": "2", "pair": "p1/order2", "better": "A"})
    write(ans, "j3a", {"judge": "3", "pair": "p1/order1", "better": other[o1]})
    v_path = tmp_path / "verdict.md"
    panel.main(["score", "--answers", str(ans), "--pairs", str(keys), "--out", str(v_path)])
    v = v_path.read_text()
    assert "After the loop better: 1; before better: 0; tie or order-dependent: 1." in v
    assert "| tension | 1 | 0 | 1 |" in v and "| hands busy | 0 | 0 | 2 |" in v
    assert "judge 3: judged in one order only" in v


def test_refuses_to_clear_a_foreign_folder(tmp_path):
    shots, hidden = fake_session(tmp_path, n=5)
    precious = tmp_path / "precious"
    precious.mkdir()
    (precious / "his.txt").write_text("keep")
    try:
        panel.main(["strip", "--shots", str(shots), "--hidden", str(hidden), "--out", str(precious)])
    except SystemExit as e:
        assert "refusing" in str(e)
    else:
        raise AssertionError("a foreign folder was cleared")
    assert (precious / "his.txt").exists()


def test_pair_key_never_inside_packet(tmp_path):
    a = tmp_path / "a"
    a.mkdir()
    try:
        panel.main(["pair", "--a", str(a), "--b", str(a), "--out", str(tmp_path / "o"), "--key", str(tmp_path / "o" / "k.json")])
    except SystemExit as e:
        assert "--key" in str(e)
    else:
        raise AssertionError("a key inside the judge's folder was accepted")


def test_single_scores_per_session_and_merged_dead(tmp_path):
    ans = tmp_path / "ans"
    base = {"session": "s", "faults_seen": [{"minute": 3, "what": "camera in wall"}]}
    write(ans, "j1", dict(base, judge="1", would_recommend=True, scores={"tension": {"score": 4}, "hands_busy": {"score": 2}},
                          dead_stretches=[{"from": 10, "to": 14}]))
    write(ans, "j2", dict(base, judge="2", would_recommend=False, scores={"tension": {"score": 2}, "hands_busy": "not shown",
                          "town_alive": {"score": True}}, dead_stretches=[{"from": 12, "to": 16}]))
    write(ans, "j3", dict(base, judge="3", would_recommend=False, scores={"tension": {"score": 9}}, dead_stretches=[{"from": 30, "to": 31}]))
    write(ans, "j4", {"session": "other", "judge": "4", "would_recommend": True, "scores": {"tension": {"score": 5}},
                      "dead_stretches": [{"from": 30, "to": 31}]})
    out = tmp_path / "v.md"
    panel.main(["score", "--answers", str(ans), "--out", str(out)])
    v = out.read_text()
    assert "### s" in v and "### other" in v
    assert "Recommends: 1 of 3 judges." in v and "Recommends: 1 of 1 judges." in v
    assert "| tension | 3.0 | 2 to 4 | 2 |" in v          # the out-of-range 9 is not counted
    assert "| hands busy | 2.0 | 2 to 2 | 1 |" in v
    assert "| town alive | not judged |" in v              # a true/false is not a score
    assert "10 to 16 (2 judges)" in v and "30 to 31" not in v   # overlaps merged; one session's stretch never meets another's
    assert "replay by machine" in v
