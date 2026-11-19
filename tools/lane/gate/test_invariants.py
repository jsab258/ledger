import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import invariants as inv  # noqa: E402


def test_moved_again_ok_and_late():
    assert inv.moved_again([(0, 0, 0), (1, 0.2, 0), (2, 0.6, 0)])["free_after_s"] == 2
    late = inv.moved_again([(0, 0, 0), (6, 1, 0)])
    assert late["ok"] is False and late["free_after_s"] == 6


def test_moved_again_never():
    r = inv.moved_again([(0, 0, 0), (3, 0.1, 0), (6, 0.2, 0)])
    assert r["ok"] is False and r["free_after_s"] is None


def test_longest_unresponsive():
    rows = [(0, True, 0, 0), (1, True, 0, 0), (2, True, 0, 0), (3, True, 1, 0), (4, False, 1, 0)]
    r = inv.longest_unresponsive(rows)
    assert r["longest_s"] == 1 and r["ok"]
    rows = [(t, True, 0, 0) for t in range(6)]
    assert inv.longest_unresponsive(rows)["ok"] is False


def test_said():
    before = {"subs": "", "prompt": "F Get in the cab"}
    assert inv.said(before, [(0.5, {"subs": "", "prompt": "F Get in the cab"})])["ok"] is False
    r = inv.said(before, [(0.2, {"subs": "", "prompt": "F Get in the cab"}), (0.9, {"subs": "Crunch.", "prompt": ""})])
    assert r["ok"] and r["where"] == "subs"
    assert inv.said(before, [(2.0, {"subs": "late"})])["ok"] is False


def test_camera_clear():
    assert inv.camera_clear(None, 6, 0.6)["ok"]
    assert inv.camera_clear(0.4, 6, 0.6)["ok"]          # its own body, ignored
    assert inv.camera_clear(3.0, 6, 0.6)["ok"] is False  # a wall between
    assert inv.camera_clear(5.8, 6, 0.6)["ok"]           # within slack


def test_summarise():
    s = inv.summarise([{"rule": "a", "ok": True}, {"rule": "a", "ok": False, "x": 1}])
    assert s["a"]["checked"] == 2 and s["a"]["failed"] == 1


def test_said_about_and_where():
    before = {"subs": "", "prompt": ""}
    frames = [(0.3, {"subs": "Never mind, love.", "prompt": "F Get out"})]
    assert inv.said(before, frames, about=inv.DAMAGE_WORDS, where=inv.MESSAGE_PLACES)["ok"] is False
    frames = [(0.3, {"subs": "The wing is dented.", "prompt": ""})]
    assert inv.said(before, frames, about=inv.DAMAGE_WORDS, where=inv.MESSAGE_PLACES)["ok"]
