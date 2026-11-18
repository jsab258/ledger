"""Tests for tools/lane/melee_drills.py (18 Nov 2026). Run:
python -m pytest tools/lane/test_melee_drills.py -q
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import melee_drills as md  # noqa: E402


def verdicts(result, targets=None):
    return {r[0]: r[4] for r in md.compare_targets(result, targets)}


def test_every_drill_has_a_scorer_and_a_simulation():
    assert set(md.DRILLS) == set(md.SCORERS)
    for name in md.DRILLS:
        assert md.simulate(name), name


def test_reference_fighter_meets_every_band():
    result = md.score_runs(md.simulate_all())
    v = verdicts(result)
    bad = {k: x for k, x in v.items() if x != "PASS"}
    assert bad == {}


def test_every_target_has_a_source():
    for k, (lo, hi, src) in md.TARGETS.items():
        assert src, k
        assert lo is not None or hi is not None, k
        if lo is not None and hi is not None:
            assert lo <= hi, k


def test_jab_numbers_exact():
    r = md.score_drill("M1_jab", md.simulate("M1_jab"))
    assert r["jab_input_to_motion_s"] == pytest.approx(0.05)
    assert r["jab_startup_s"] == pytest.approx(0.32)
    assert r["jab_active_s"] == pytest.approx(0.06)
    assert r["jab_hitstop_s"] == pytest.approx(0.035)
    # recovery excludes the hit-stop freeze
    assert r["jab_recovery_s"] == pytest.approx(0.30)
    assert r["light_stagger_s"] == pytest.approx(0.60)
    assert r["impact_sync_s"] == pytest.approx(0.01)


def test_slow_input_fails_latency():
    p = {"lag": 0.15}
    r = md.score_drill("M1_jab", md.simulate("M1_jab", p))
    assert verdicts(r)["jab_input_to_motion_s"] == "FAIL"


def test_heavy_miss_gives_miss_recovery():
    r = md.score_drill("M1_heavy", md.simulate("M1_heavy", land=False))
    assert "heavy_startup_s" not in r
    assert r["heavy_miss_recovery_s"] == pytest.approx(0.80)


def test_hook_too_slow_fails():
    p = {"hook": (0.95, 0.10, 0.42, 0.06)}
    r = md.score_drill("M1_hook", md.simulate("M1_hook", p))
    assert verdicts(r)["hook_startup_s"] == "FAIL"


def test_combo_lands_three():
    r = md.score_drill("M2_combo", md.simulate("M2_combo"))
    assert r["combo_hits_landed"] == 3


def test_block_and_dodge():
    b = md.score_drill("M3_block", md.simulate("M3_block"))
    assert b["blocked"] == 1 and b["telegraph_lead_s"] == pytest.approx(0.60)
    assert b["guard_raise_s"] == pytest.approx(0.10)
    d = md.score_drill("M4_dodge", md.simulate("M4_dodge"))
    assert d["evaded"] == 1 and d["dodge_invuln_s"] == pytest.approx(0.28)


def test_short_telegraph_fails():
    r = md.score_drill("M3_block", md.simulate("M3_block", {"telegraph_lead": 0.30}))
    assert verdicts(r)["telegraph_lead_s"] == "FAIL"


def test_dodge_hit_counts_as_not_evaded():
    log = md.simulate("M4_dodge")
    log.append({"t": 1.6, "ev": "hit_contact", "actor": "a1", "target": "player"})
    r = md.score_drill("M4_dodge", log)
    assert r["evaded"] == 0


def test_knockdown_and_ko():
    k = md.score_drill("M5_knockdown", md.simulate("M5_knockdown", ko=False))
    assert k["blows_to_knockdown"] == 4
    assert k["down_time_s"] == pytest.approx(2.2)
    assert k["getup_s"] == pytest.approx(1.4)
    o = md.score_drill("M5_knockdown", md.simulate("M5_knockdown", ko=True))
    assert o["ko_time_s"] == pytest.approx(12.0)
    assert o["fist_rule_violations"] == 0


def test_fist_death_through_kerb_fall_is_allowed():
    log = md.simulate("M5k_kerb", death=True, hazard=True)
    assert md.fist_rule_violations(log) == 0


def test_fist_death_without_fall_breaks_ruling():
    log = md.simulate("M5k_kerb", death=True, hazard=False)
    assert md.fist_rule_violations(log) == 1
    r = md.score_drill("M5k_kerb", log)
    assert verdicts(r)["fist_rule_violations"] == "FAIL"


def test_fall_long_after_blow_does_not_excuse():
    log = [e for e in md.simulate("M5k_kerb", death=True, hazard=True)
           if e["ev"] not in ("fall_hazard", "death")]
    last = max(e["t"] for e in log)
    log.append({"t": last + 10, "ev": "fall_hazard", "actor": "opp", "surface": "step"})
    log.append({"t": last + 10.2, "ev": "death", "actor": "opp", "cause": "fall"})
    assert md.fist_rule_violations(log) == 1


def test_player_can_never_die():
    log = [{"t": 1.0, "ev": "death", "actor": "player", "cause": "weapon"},
           {"t": 0.5, "ev": "hit_contact", "actor": "a1", "target": "player", "weapon": "pipe"}]
    assert md.fist_rule_violations(log) == 1


def test_weapon_death_is_not_a_fist_rule_break():
    log = [{"t": 0.5, "ev": "hit_start", "actor": "player", "weapon": "pipe"},
           {"t": 1.0, "ev": "hit_contact", "actor": "player", "target": "opp", "weapon": "pipe"},
           {"t": 1.5, "ev": "death", "actor": "opp", "cause": "weapon"}]
    assert md.fist_rule_violations(log) == 0


def test_attackers():
    r = md.score_drill("M6_two_attackers", md.simulate("M6_two_attackers"))
    assert r["max_simultaneous_attackers"] == 2
    assert r["min_attack_start_gap_s"] == pytest.approx(0.6)
    assert r["max_attacker_idle_s"] == pytest.approx(1.6)


def test_three_at_once_fails():
    log = md.simulate("M6_two_attackers")
    log.append({"t": 1.1, "ev": "attack_start", "actor": "a3"})
    log.append({"t": 1.9, "ev": "attack_end", "actor": "a3"})
    r = md.score_drill("M6_two_attackers", log)
    v = verdicts(r)
    assert r["max_simultaneous_attackers"] == 3
    assert v["max_simultaneous_attackers"] == "FAIL"
    assert v["min_attack_start_gap_s"] == "FAIL"


def test_breakage_counts():
    assert md.score_drill("M7_breakage", md.simulate("M7_breakage", weapon="chair"))["chair_hits_to_break"] == 2
    assert md.score_drill("M7_breakage", md.simulate("M7_breakage", weapon="pipe"))["pipe_hits_to_break"] == 25


def test_pipe_breaking_fails():
    log = md.simulate("M7_breakage", {"breaks": {"chair": 2, "brick": 3, "pipe": 3}}, weapon="pipe")
    r = md.score_drill("M7_breakage", log)
    assert verdicts(r)["pipe_hits_to_break"] == "FAIL"


def test_camera_numbers_and_occlusion():
    log = md.simulate("M8_camera_narrow")
    r = md.score_drill("M8_camera_narrow", log)
    assert r["cam_dist_m"] == pytest.approx(4.2)
    assert r["close_in_hold_s"] == pytest.approx(0.8)
    assert r["occluded_frames"] == 0
    for e in log:
        if e["ev"] == "camera" and 2.0 <= e["t"] < 2.5:
            e["occluded"] = True
            e["both_visible"] = False
    r2 = md.score_drill("M8_camera_narrow", log)
    assert r2["occluded_frames"] > 0
    assert verdicts(r2)["occluded_frames"] == "FAIL"


def test_stamina():
    r = md.score_drill("M9_stamina", md.simulate("M9_stamina"))
    assert r["jabs_to_empty"] == 8
    assert r["heavies_to_empty"] == 4
    assert r["regen_full_s"] == pytest.approx(6.0)


def test_mashing_without_cost_fails():
    p = {"stamina_cost": {"jab": 0.05, "heavy": 0.30}}
    r = md.score_drill("M9_stamina", md.simulate("M9_stamina", p))
    assert verdicts(r)["jabs_to_empty"] == "FAIL"


def test_targets_and_warp():
    r = md.score_drill("M10_targets", md.simulate("M10_targets"))
    assert r["target_pick_correct_pct"] == 100.0
    assert r["warp_end_dist_m"] == pytest.approx(1.0)
    bad = md.score_drill("M10_targets", md.simulate("M10_targets", wrong_pick="left"))
    assert verdicts(bad)["target_pick_correct_pct"] == "FAIL"


def test_log_round_trip(tmp_path):
    log = md.simulate("M1_jab")
    p = tmp_path / "jab.jsonl"
    md.write_log(p, log)
    back = md.read_log(p)
    assert md.score_drill("M1_jab", back) == md.score_drill("M1_jab", log)


def test_unknown_event_rejected(tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text('{"t": 0.1, "ev": "teleport"}\n')
    with pytest.raises(ValueError):
        md.read_log(p)


def test_missing_band_and_no_band():
    v = verdicts({"jab_startup_s": 0.3, "something_new": 1.0},
                 {"jab_startup_s": md.TARGETS["jab_startup_s"], "hook_startup_s": md.TARGETS["hook_startup_s"]})
    assert v == {"jab_startup_s": "PASS", "something_new": "NO BAND", "hook_startup_s": "MISSING"}


def test_band_edges_included():
    v = verdicts({"jab_startup_s": 0.25}, {"jab_startup_s": md.TARGETS["jab_startup_s"]})
    assert v["jab_startup_s"] == "PASS"


def test_unreal_against_browser():
    browser = md.score_runs(md.simulate_all())
    same = md.score_runs(md.simulate_all())
    assert all(r[3] == "PASS" for r in md.compare_results(same, browser))
    slower = md.score_runs(md.simulate_all({"jab": (0.40, 0.06, 0.30, 0.035)}))
    rows = {r[0]: r[3] for r in md.compare_results(slower, browser)}
    assert rows["jab_startup_s"] == "FAIL"
    # within one frame at 30 fps passes
    near = md.score_runs(md.simulate_all({"jab": (0.34, 0.06, 0.30, 0.035)}))
    rows = {r[0]: r[3] for r in md.compare_results(near, browser)}
    assert rows["jab_startup_s"] == "PASS"
    missing = dict(browser)
    missing.pop("hook_startup_s")
    rows = {r[0]: r[3] for r in md.compare_results(missing, browser)}
    assert rows["hook_startup_s"] == "FAIL"


def test_no_drink_items_in_drills():
    text = " ".join(str(d) for d in md.DRILLS.values()).lower()
    for word in ("bottle", "glass", "pint", "bar stool"):
        assert word not in text
