import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate  # noqa: E402

REP = {"results": [{"rule": "a", "ok": True}, {"rule": "pad", "ok": False}, {"rule": "camera clear", "ok": False}]}


def test_judge_new_failure_blocks():
    ok, new, old, b = gate.judge(REP, {"pad": "a pad only drives the Ledger"}, "all fine", [{"ok": True}])
    assert not ok and [r["rule"] for r in new] == ["camera clear"] and len(old) == 1


def test_judge_all_known_passes():
    ok, new, old, b = gate.judge(REP, {"pad": "x", "camera clear": "y"}, "nothing", [{"ok": True}])
    assert ok and not new


def test_judge_scripted_and_blockers():
    known = {"pad": "x", "camera clear": "y"}
    assert not gate.judge(REP, known, "nothing", [{"ok": False}])[0]
    ok, _, _, b = gate.judge(REP, known, "BLOCKER: stuck behind the bar\nknown blocker: pad", [{"ok": True}])
    assert not ok and b == ["BLOCKER: stuck behind the bar"]


def test_note_lists_known_and_new():
    n = gate.note(REP, {"pad": "a pad only drives the Ledger"}, [], ["drive to the quay"])
    assert "drive to the quay" in n and "pad (a pad only drives the Ledger)" in n and "camera clear (new, not yet fixed)" in n
    assert "untested" in n
