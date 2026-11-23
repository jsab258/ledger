"""Tests for the hidden-check harness (no browser, no game)."""
import os
import hidden as H

CAN = "LEDGER-HIDDEN-CANARY-0123456789abcdef"
BODY = "// check W07: the constable walks to the last place he saw him\n" + "x" * 300 + "\n// " + CAN + "\n"


def mk(tmp, rel, text):
    p = os.path.join(tmp, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)
    return p


def test_manifest_catches_changed_added_missing(tmp_path):
    d = str(tmp_path / "checks")
    mk(d, "W07.mjs", BODY)
    mk(d, "W08.mjs", BODY + "y")
    m = H.manifest(d)
    assert H.verify(d, m) == []
    mk(d, "W07.mjs", BODY + "changed")
    mk(d, "W09.mjs", "new")
    os.remove(os.path.join(d, "W08.mjs"))
    p = H.verify(d, m)
    assert "changed: W07.mjs" in p and "added: W09.mjs" in p and "missing: W08.mjs" in p


def test_leak_finds_canary_and_copied_file(tmp_path):
    d = str(tmp_path / "checks")
    mk(d, "W07.mjs", BODY)
    t = str(tmp_path / "builder")
    mk(t, "src/game/x.js", "const k = '%s';\n" % CAN)
    mk(t, "test/copied.mjs", BODY)
    mk(t, "src/clean.js", "nothing here\n")
    out = H.leak(d, [t])
    assert any("canary" in l and "src/game/x.js" in l for l in out)
    assert any("copied" in l and "test/copied.mjs" in l for l in out)
    assert not any("clean.js" in l for l in out)


def test_no_leak_in_a_clean_tree(tmp_path):
    d = str(tmp_path / "checks")
    mk(d, "W07.mjs", BODY)
    t = str(tmp_path / "builder")
    mk(t, "src/a.js", "the constable walks\n")
    assert H.leak(d, [t]) == []


def test_redact_keeps_what_the_player_met_and_drops_code():
    r = [{"check": "W07", "story": "S05", "week": 1, "run": 1, "verdict": "fail", "variant": "off-path",
          "met": "no fresh call where he was last seen " + CAN, "code": "await P.walkTo(1, 2)"}]
    out = H.redact(r)
    assert out[0]["verdict"] == "fail" and "fresh call" in out[0]["met"]
    assert "code" not in out[0] and "check" not in out[0] and "variant" not in out[0]
    assert CAN not in out[0]["met"]


def rec(c, run, variant, v, week=1):
    return {"check": c, "story": "S0x", "week": week, "run": run, "variant": variant, "verdict": v}


def test_verdict_needs_both_runs_and_the_off_path_variant():
    rs = []
    for c in ("A", "B", "C", "D"):
        for run in (1, 2):
            for var in ("scripted", "off-path"):
                rs.append(rec(c, run, var, "pass"))
    v = H.verdict(rs)
    assert v["go"] and v["working"] == 4
    # C passes only on the scripted path; D is flaky; B never left the scripted path
    rs = [r for r in rs if not (r["check"] == "C" and r["variant"] == "off-path")] + [rec("C", 1, "off-path", "fail")]
    rs = [r for r in rs if not (r["check"] == "D" and r["run"] == 2 and r["variant"] == "scripted")] + [rec("D", 2, "scripted", "fail")]
    rs = [r for r in rs if not (r["check"] == "B" and r["variant"] == "off-path")]
    v = H.verdict(rs)
    assert v["working"] == 1 and v["of"] == 4 and not v["go"] and v["flaky"] == 1
    assert "C (passes only on the scripted path)" in v["not_working"]


def test_verdict_unreached_and_later_weeks():
    rs = [rec("A", 1, "off-path", "not reached"), rec("A", 2, "off-path", "not reached"),
          rec("Z", 1, "off-path", "pass", week=3)]
    v = H.verdict(rs)
    assert v["of"] == 1 and v["working"] == 0 and not v["go"]
    assert not H.verdict([])["go"]
