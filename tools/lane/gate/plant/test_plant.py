"""Checks for the testers' tester (no browser, no build)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import panel_vs_him as pv  # noqa: E402
import plant  # noqa: E402

SRC = os.path.join(plant.LANE_TOOLS, "prototype", "project", "src")


def test_every_fault_applies_once_to_the_current_source(tmp_path):
    for f in plant.load_faults():
        d = tmp_path / f["id"]
        d.mkdir()
        (d / f["file"]).write_text(open(os.path.join(SRC, f["file"]), encoding="utf-8").read(), encoding="utf-8")
        assert plant.apply_fault(str(d), f) is None, f["id"]
        assert f["new"] in (d / f["file"]).read_text(encoding="utf-8")
        assert f["testers"] and all(t in plant.TESTERS for t in f["testers"]), f["id"]
        assert f.get("watch"), f["id"]


def test_a_fault_whose_text_moved_is_not_planted(tmp_path):
    (tmp_path / "a.js").write_text("x\nx\n")
    assert "2 times" in plant.apply_fault(str(tmp_path), {"file": "a.js", "old": "x", "new": "y"})
    assert "no file" in plant.apply_fault(str(tmp_path), {"file": "b.js", "old": "x", "new": "y"})


def r(rule, ok, steps="s"):
    return {"rule": rule, "ok": ok, "steps": steps}


def test_caught_only_on_new_failures_where_the_fault_aims():
    clean = {"results": [r("a", True), r("b", False, "old fault")]}
    same = {"results": [r("a", True), r("b", False, "old fault")]}
    worse = {"results": [r("a", False), r("b", False, "old fault")]}
    assert plant.caught("machine", [clean, clean], same, ["a"])[0] is False
    assert plant.caught("machine", [clean, clean], worse, ["a"])[0] is True
    assert plant.caught("machine", [clean, clean], worse, ["b"])[0] is False  # a failure elsewhere is not a catch
    assert plant.caught("machine", [clean, clean], {"broke": "x"}, ["a"])[0] is None


def test_unreached_means_not_tested_only_for_watched_checks():
    clean = {"results": [r("save", False, "not reached: no saved week"), r("other", None)]}
    assert plant.caught("machine", [clean, clean], clean, ["save"])[0] is None
    clean2 = {"results": [r("save", True), r("other", None)]}
    assert plant.caught("machine", [clean2, clean2], clean2, ["save"])[0] is False  # a real miss stays a miss
    noted = {"results": [{"rule": "steer", "ok": False, "steps": "setup", "note": "not reached: a box opened"}]}
    assert plant.caught("clumsy", [clean2, clean2], noted, ["steer"])[0] is None


def test_noise_between_clean_runs_never_counts():
    c1 = {"results": [r("camera clear", False, "at A")]}
    c2 = {"results": [r("camera clear", True)]}
    planted = {"results": [r("camera clear", False, "at A")]}
    assert plant.caught("clumsy", [c1, c2], planted, ["camera clear"])[0] is False


def num(i, v):
    return {"id": i, "verdict": v}


def test_feel_compares_numbers_outside_bands():
    clean = {"numbers": [num("C2_jab_contact_s", "inside"), num("cam", "outside")], "faults": []}
    planted = {"numbers": [num("C2_jab_contact_s", "outside"), num("cam", "outside")], "faults": []}
    ok, ev = plant.caught("feel", [clean, clean], planted, ["C2_jab_contact_s"])
    assert ok and "C2_jab_contact_s: outside" in ev
    assert plant.caught("feel", [clean, clean], clean, ["C2_jab_contact_s"])[0] is False
    assert plant.caught("feel", [planted, planted], planted, ["C2_jab_contact_s"])[0] is None  # already outside


def test_panel_flags_after_two_disagreements_in_three():
    e = [{"his_verdict": "no", "panel_verdict": "yes"}, {"his_verdict": "yes", "panel_verdict": "yes"},
         {"his_verdict": "no", "panel_verdict": "yes"}]
    rows, flags, k, n = pv.judge(e)
    assert flags and n == 3 and k is None
    assert not pv.judge(e[1:2])[1]


def test_panel_named_share_and_kappa():
    assert pv.named_share(["the cab camera is too far"], ["Cab camera too far behind"]) == 1.0
    assert pv.named_share(["the cab camera"], ["fists feel slow"]) == 0.0
    assert pv.named_share(["cab camera"], ["cab door sticks"]) == 0.0
    assert pv.named_share(["camera too close in the cab"], ["the fists are too slow in a fight"]) == 0.0
    assert pv.kappa([("yes", "yes"), ("no", "no")]) == 1.0
    assert pv.report([], [], None, 0).count("No entries yet") == 1


def test_faults_file_is_valid_json():
    d = json.load(open(os.path.join(plant.HERE, "faults.json"), encoding="utf-8"))
    ids = [f["id"] for f in d["faults"]]
    assert len(ids) == len(set(ids)) >= 5
