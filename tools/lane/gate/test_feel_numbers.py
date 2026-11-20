"""Tests for feel_numbers.py's measures, on made-up frames (no browser)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feel_numbers as fn  # noqa: E402

DT = fn.DT


def test_speeds_and_start_stop():
    # still 10 frames, then speed ramps 0 to 2 m/s over 6 frames, holds, then stops over 3 frames
    v = [0] * 10 + [2 * (i + 1) / 6 for i in range(6)] + [2] * 40 + [2 * (2 - i) / 3 for i in range(3)] + [0] * 10
    xs, x = [0.0], 0.0
    for s in v[1:]:
        x += s * DT
        xs.append(x)
    sp = fn.speeds(xs, [0.0] * len(xs))
    assert abs(fn.steady(sp[10:56]) - 2) < 1e-9
    assert abs(fn.time_to_reach(sp, 10, 2.0) - 6 * DT) < 1e-9  # 90% of 2 first reached at the 6th frame (1.67 < 1.8)
    assert abs(fn.time_to_fall(sp, 56, 0.05) - 3 * DT) < 1e-9
    assert fn.time_to_reach(sp, 10, 5.0) is None


def test_turn_time_instant_and_eased():
    # running +z at 4 m/s for 20 frames, then at once -z: the turn takes one frame
    zs = [0.0]
    for i in range(1, 40):
        zs.append(zs[-1] + (4 if i < 20 else -4) * DT)
    xs = [0.0] * 40
    assert abs(fn.turn_time(xs, zs, 20, 4.0, 0.0) - DT) < 1e-9
    # eased: speed falls to 0 over 10 frames and back up the other way over 10
    zs = [0.0]
    for i in range(1, 60):
        if i < 20:
            v = 4
        elif i < 30:
            v = 4 - 0.4 * (i - 19)
        elif i < 40:
            v = -0.4 * (i - 29)
        else:
            v = -4
        zs.append(zs[-1] + v * DT)
    t = fn.turn_time([0.0] * 60, zs, 20, 4.0, 0.0)
    assert 18 * DT <= t <= 21 * DT


def test_lag_and_fov():
    assert fn.lag_seconds(6.0, 5.0, 10.0) == 0.1
    assert fn.lag_seconds(5.0, 5.0, 0.1) is None
    assert abs(fn.hfov(56, 16 / 9) - 86.78) < 0.05
    assert abs(fn.hfov(90, 1.0) - 90) < 1e-9


def frames(st, stop, hurt, foe):
    return [{"st": a, "stop": b, "foeHurt": c, "foeSt": d} for a, b, c, d in zip(st, stop, hurt, foe)]


def test_strike_from_frames_and_record():
    # press before frame 5; wind-up starts at frame 5 (1 frame), contact at frame 23 (18 frames after start),
    # 3 frames of hit-stop, busy to frame 40, the man staggers 36 frames from contact
    n = 80
    st = ["idle"] * 5 + ["windup"] * 18 + ["recover"] * 17 + ["idle"] * (n - 40)
    stop = [0] * 23 + [0.05, 0.03, 0.01] + [0] * (n - 26)
    hurt = [0] * 23 + [0.2] * (n - 23)
    foe = ["still"] * 23 + ["stagger"] * 36 + ["still"] * (n - 59)
    m = fn.strike_from_frames(frames(st, stop, hurt, foe), 5)
    assert abs(m["press_to_start_s"] - DT) < 1e-9
    assert abs(m["start_to_contact_s"] - 18 * DT) < 1e-9
    assert abs(m["hitstop_s"] - 3 * DT) < 1e-9
    assert abs(m["recover_s"] - 14 * DT) < 1e-9
    assert abs(m["react_s"] - 36 * DT) < 1e-9
    rec = [{"t": 5 * DT, "ev": "hit_start", "actor": "player"}, {"t": 23 * DT, "ev": "hit_contact", "actor": "player"},
           {"t": 23 * DT, "ev": "hitstop_start"}, {"t": 26 * DT, "ev": "hitstop_end"},
           {"t": 40 * DT, "ev": "recovery_end", "actor": "player"},
           {"t": 23 * DT, "ev": "stagger_start", "actor": "a1"}, {"t": 59 * DT, "ev": "stagger_end", "actor": "a1"}]
    r = fn.strike_from_record(rec)
    assert fn.compare_record(m, r, "jab") == []
    rec[1]["t"] = 26 * DT  # the record says contact 3 frames later than the frames show
    assert any("start_to_contact" in x for x in fn.compare_record(m, fn.strike_from_record(rec), "jab"))


def test_no_contact_is_not_measured():
    n = 60
    m = fn.strike_from_frames(frames(["idle"] * 5 + ["windup"] * 30 + ["idle"] * 25, [0] * n, [0] * n, ["still"] * n), 5)
    assert m["start_to_contact_s"] is None and fn.judge("C2_jab_contact_s", m["start_to_contact_s"])["verdict"] == "not measured"


def test_judge():
    assert fn.judge("C2_jab_contact_s", 0.30)["verdict"] == "inside"
    assert fn.judge("C2_jab_contact_s", 0.25 - DT / 3)["verdict"] == "inside"  # within half a frame of the edge
    assert fn.judge("C2_jab_contact_s", 0.45)["verdict"] == "outside"
    assert fn.judge("W4_walk_mps", 1.8)["verdict"] == "no reference yet"
    assert fn.judge("C10_foe_in_frame", 0.94)["verdict"] == "outside"  # shares get no frame tolerance
