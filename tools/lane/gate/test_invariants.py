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


def test_camera_clear():
    assert inv.camera_clear(None, 6, 0.6)["ok"]
    assert inv.camera_clear(0.4, 6, 0.6)["ok"]          # its own body, ignored
    assert inv.camera_clear(3.0, 6, 0.6)["ok"] is False  # a wall between
    assert inv.camera_clear(5.8, 6, 0.6)["ok"]           # within slack


def test_summarise():
    s = inv.summarise([{"rule": "a", "ok": True}, {"rule": "a", "ok": False, "x": 1}])
    assert s["a"]["checked"] == 2 and s["a"]["failed"] == 1


def test_game_words_come_from_the_source():
    # the lines the game writes for a crash and a run-down, built from kinds.js and talk_lines.js: if the game's
    # wording drifts, these break (the gate then matches the new wording, not old guesses)
    crash = inv.source_phrases("crash")
    knocked = inv.source_phrases("knocked")
    assert len(crash) >= 3 and len(knocked) >= 3
    hit = lambda pats, s: any(p.search(s) for p in pats)
    assert hit(crash, "Noted in the Ledger: the big man on the rank may have seen that you put the cab into something on Quay Street.")
    assert hit(crash, "You'll have that wing to pay for.")
    assert hit(knocked, "Noted in the Ledger: Ron Kirby knows that you knocked Ron Kirby down with the cab.")
    assert hit(knocked, "You had Ron Kirby over with that car.")
    assert not hit(crash, "Noted in the Ledger: 11 things") and not hit(knocked, "Crunch.")
    assert inv.count_line_rx().search("Noted in the Ledger: 11 things")


def test_kinds_exist_in_source():
    src = open(os.path.join(inv.SRC, "kinds.js")).read()
    drive = open(os.path.join(inv.SRC, "drive.js")).read()
    for k in ("crash", "knocked"):
        assert "\n  %s: K(" % k in src and "act('%s'" % k in drive


def _msgs(**kw):
    d = {"subs": [], "noted": "", "queued": [], "news": "", "bubbles": []}
    d.update(kw)
    return d


def test_told_from_the_event_frame():
    pats = inv.source_phrases("crash")
    line = "Noted in the Ledger: somebody passing may have seen that you put the cab into something on Copper Row."
    before = _msgs()
    frames = [(0.02, _msgs(queued=[line])), (0.4, _msgs(noted=line))]
    r = inv.told(before, frames, pats)
    assert r["ok"] and r["where"] == "noted" and r["after_s"] == 0.4 and r["queued_at_s"] == 0.02
    # queued but never shown: not told
    r = inv.told(before, [(0.02, _msgs(queued=[line])), (1.4, _msgs(queued=[line]))], pats)
    assert not r["ok"] and r["queued_at_s"] == 0.02
    # only the merged count line: not told
    r = inv.told(before, [(0.3, _msgs(noted="Noted in the Ledger: 3 things"))], pats, count_rx=inv.count_line_rx())
    assert not r["ok"] and r["count_line_at_s"] == 0.3
    # late
    r = inv.told(before, [(2.0, _msgs(noted=line))], pats)
    assert not r["ok"] and r["late_at_s"] == 2.0
    # already on screen before the event: not new
    assert not inv.told(_msgs(noted=line), [(0.3, _msgs(noted=line))], pats)["ok"]
    # unrelated words: not told
    assert not inv.told(before, [(0.3, _msgs(subs=["Crunch."]))], pats)["ok"]


def test_drawn_props_from_the_source():
    d = inv.drawn_props()
    kinds = {p["type"] for p in d}
    assert {"lamp post", "bollard", "parked car"} <= kinds
    assert sum(p["type"] == "lamp post" for p in d) >= 20 and sum(p["type"] == "parked car" for p in d) >= 5


DT = 1 / 60


def test_steering_snap_fails_on_press_release_and_reverse():
    press = [0.0] + [1.5] * 30
    release = [1.5] + [0.0] * 30
    reverse = [-1.5] + [1.5] * 30
    for s in (press, release, reverse):
        r = inv.steer_change(s, DT)
        assert not r["ok"] and r["rise_10_90_s"] == 0 and r["biggest_frame_step_share"] == 1.0


def test_steering_two_frame_ramp_fails():
    r = inv.steer_change([0.0, 0.75, 1.5] + [1.5] * 20, DT)
    assert not r["ok"]


def test_steering_eased_passes_press_release_and_reverse():
    n = 10  # a straight ramp over 10 frames (about 0.17 s)
    up = [1.5 * min(1, k / n) for k in range(0, 40)]
    down = [1.5 * max(0, 1 - k / n) for k in range(0, 40)]
    rev = [-1.5 + 3.0 * min(1, k / n) for k in range(0, 40)]
    for s in (up, down, rev):
        r = inv.steer_change(s, DT)
        assert r["ok"], r
        assert r["rise_10_90_s"] >= 0.1 and r["biggest_frame_step_share"] <= 0.2


def test_steering_long_ramp_with_one_jump_fails():
    s = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 1.2, 1.3, 1.4, 1.5, 1.5]
    r = inv.steer_change(s, DT)
    assert not r["ok"] and r["biggest_frame_step_share"] > 0.2


def test_steering_no_change_fails():
    assert not inv.steer_change([0.0] * 10, DT)["ok"]
