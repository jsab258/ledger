import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate  # noqa: E402

REP = {"results": [{"rule": "a", "ok": True}, {"rule": "pad", "ok": False},
                   {"rule": "camera clear", "ok": False, "where": "indoors: Regent House"}]}
KNOWN_ALL = {"pad": "a pad only drives the Ledger", "camera clear | indoors: Regent House": "y"}


def test_judge_new_failure_blocks():
    ok, new, old, b = gate.judge(REP, {"pad": "a pad only drives the Ledger"}, "all fine", [{"ok": True}])
    assert not ok and [r["rule"] for r in new] == ["camera clear"] and len(old) == 1


def test_judge_all_known_passes():
    ok, new, old, b = gate.judge(REP, KNOWN_ALL, "nothing", [{"ok": True}])
    assert ok and not new


def test_known_is_keyed_by_rule_and_signature():
    # an accepted camera fault in one room does not hide a camera fault in another room
    rep = {"results": [{"rule": "camera clear", "ok": False, "where": "indoors: Mickey's"}]}
    ok, new, _, _ = gate.judge(rep, KNOWN_ALL, "nothing", [{"ok": True}])
    assert not ok and len(new) == 1
    assert not gate.judge(rep, {"camera clear": "y"}, "nothing", [{"ok": True}])[0]  # a bare rule name hides nothing


def test_judge_scripted_and_blockers():
    assert not gate.judge(REP, KNOWN_ALL, "nothing", [{"ok": False}])[0]
    ok, _, _, b = gate.judge(REP, KNOWN_ALL, "BLOCKER: stuck behind the bar\nknown blocker: pad", [{"ok": True}])
    assert not ok and b == ["BLOCKER: stuck behind the bar"]


def test_hands_on_lines_read_by_marker_only():
    text = "No blockers found.\nAn unknown blocker? none.\n- unknown blocker: the door\nMAJOR: the cab drifts\nMINOR: font"
    assert gate.hands_on_faults(text) == ["MAJOR: the cab drifts"]
    assert gate.hands_on_faults("Known blocker: pad\n* BLOCKER - stuck") == ["* BLOCKER - stuck"]
    ok, _, _, b = gate.judge(REP, KNOWN_ALL, "No blockers. Nothing major.", [{"ok": True}])
    assert ok and not b


def test_no_hands_on_never_passes():
    ok, _, _, b = gate.judge(REP, KNOWN_ALL, None, [{"ok": True}])
    assert not ok and any("no hands-on" in x for x in b)
    assert not gate.judge(REP, KNOWN_ALL, "   ", [{"ok": True}])[0]


def test_note_lists_known_and_new():
    n = gate.note(REP, {"pad": "a pad only drives the Ledger"}, [], ["drive to the quay"])
    assert "drive to the quay" in n and "pad (a pad only drives the Ledger)" in n
    assert "camera clear | indoors: Regent House (new, not yet fixed)" in n
    assert "untested" in n
