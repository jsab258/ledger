#!/usr/bin/env python
"""Negative controls for self_check.py: each mutation of target.json must make the self-check fail (a check that cannot fail proves nothing).

    /home/user/.bpyenv/bin/python controls.py
"""
import copy
import json
import os
import sys
import io
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import self_check as SC  # noqa: E402

BASE = json.load(open(os.path.join(HERE, "target.json")))


def run(mut):
    t = copy.deepcopy(BASE)
    mut(t)
    SC.T = t
    SC.LINES.clear()
    SC.COUNT.update({"pass": 0, "fail": 0, "report": 0})
    SC.GROUPS.clear()
    sys.argv = ["self_check.py", "--no-write"]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        SC.main()
    return SC.COUNT["fail"], [ln["name"][:70] for ln in SC.LINES if ln["result"] == "fail"][:2]


def shop(t, sid):
    return next(s for s in t["shops"] if s["id"] == sid)


CONTROLS = {
    "a free counter 2.4 m out in Rita's room": lambda t: shop(t, "ritas")["room"]["fixtures"].append({"id": "X", "surface": "back", "what": "a counter across the room", "depth_m": 1.55, "x": [-2, 1], "y": [2.4, 2.95], "z": [0, 1.05], "kind": "counter"}),
    "a unit 0.40 deep on a side wall": lambda t: shop(t, "grocer")["room"]["fixtures"].append({"id": "X", "surface": "left", "what": "a shelf unit", "depth_m": 0.40, "y": [1, 3], "z": [0.5, 1.9], "kind": "shelf_unit"}),
    "a denied model (WoodenChair_01) in the tea room's display": lambda t: shop(t, "tea_rooms")["display"]["items"].append({"model": "WoodenChair_01", "n": 1, "zone": [0.5, 0.9, 0.1, 0.5, 0, 0.9], "size_m": None, "note": ""}) or t["inventory"]["polyhaven"].update({"WoodenChair_01": {}}),
    "the T1 door's glass foot back at 600": lambda t: shop(t, "ritas")["door"].__setitem__("glass_foot_z_mm", 600.0) or shop(t, "ritas")["door"]["t1_rails_mm"]["glass"].__setitem__(0, 600),
    "a display item outside the window zone": lambda t: shop(t, "ritas")["display"]["items"].append({"model": "Camera_01", "n": 1, "zone": [3.2, 3.6, 0.1, 0.4, 0, 0.3], "size_m": None, "note": ""}),
    "the camera rule's wording changed": lambda t: t["method"]["game_rule"].__setitem__("camera_rule", "from the room's centre"),
    "a card 0.1 m off": lambda t: shop(t, "grocer")["card"].__setitem__("x0", 33.45),
    "a hook-cast hour changed": lambda t: shop(t, "fish_market")["hours"].__setitem__("mon", [9, 14]),
    "a brand in the lettering": lambda t: shop(t, "newsagent")["glass"]["lettering"].append("MARLBORO"),
    "a pub word on a fixture": lambda t: shop(t, "grocer")["room"]["fixtures"][0].__setitem__("what", "a shelf of beer and lager"),
    "a dark shop marked lit": lambda t: shop(t, "fish_market").__setitem__("lit_at_night", True),
    "the picture 2048 wide": lambda t: shop(t, "grocer")["pictures"]["json_fields"].__setitem__("pixels", [2048, 927]),
    "a good on a missing fixture": lambda t: shop(t, "chandler")["room"]["goods"].append({"model": "oil_tin", "n": 1, "on": "NOPE", "size_m": None, "note": ""}),
    # ---- the controls added after the review of 12 October (faults 1 to 3 and the narrow points) ----------------------------------------
    "a hole in the front: Rita's panel over the side door only 220 high (FRN-07)": lambda t: shop(t, "ritas")["door"]["panel_over_side_door"].__setitem__("z_mm", [2480.0, 2700.0]),
    "no head across the doors: Rita's head only 40 wide (FRN-07)": lambda t: shop(t, "ritas")["door"]["head"].__setitem__("u_mm", [350.0, 390.0]),
    "the over-door toplights gone from the grocer (FRN-07)": lambda t: shop(t, "grocer")["door"]["toplights_over_shop_door"].__setitem__("panes", [[400.0, 500.0]]),
    "a toplight bar 20 mm off its place (FRN-04)": lambda t: shop(t, "ritas")["front"]["glazing_layout"]["toplight_bars"][0].__setitem__("centre", 410.9),
    "a toplight sliver 94.5 wide beside a mullion (FRN-04)": lambda t: shop(t, "newsagent")["front"]["glazing_layout"]["toplight_panes"].__setitem__(0, [50.0, 144.5]),
    "the unaligned 2.2 toplights back on the ironmonger (FRN-04)": lambda t: shop(t, "ironmonger")["front"]["glazing"].__setitem__("toplight_aligned", False),
    "'dixons' out of the brand blocklist (INV-05)": lambda t: t["inventory"]["brand_blocklist"].remove("dixons"),
    "cassette_player's mark forgotten (INV-06)": lambda t: t["inventory"]["polyhaven"]["cassette_player"].update({"marks": None, "blank": []}),
    "a blanking step with no boxes (INV-06)": lambda t: t["inventory"]["polyhaven"]["CashRegister_01"]["blank"][0].__setitem__("boxes", []),
    "the stale sodium wash (1.0, 0.7055, 0.0) in Rita's night_dark (LIT-06)": lambda t: shop(t, "ritas")["room"]["lights"].__setitem__("night_dark_wash_linear_rgb", [1.0, 0.7055, 0.0]),
    "Rita's stock wall across her back door (SO-05)": lambda t: next(f for f in shop(t, "ritas")["room"]["fixtures"] if f["id"] == "R-back-stock").__setitem__("x", [-2.6, 2.6]),
    "Rita's stock wall 0.40 deep again (SO-01)": lambda t: next(f for f in shop(t, "ritas")["room"]["fixtures"] if f["id"] == "R-back-stock").__setitem__("depth_m", 0.40),
    "an M1 door's letter plate back in the glass at 545 (FRN-03)": lambda t: shop(t, "mickeys")["door"]["letter_plate"].__setitem__("z_mm", 545.0),
    "a ceiling fixture that fills the whole height (z 0 to 2.4)": lambda t: next(f for f in shop(t, "grocer")["room"]["fixtures"] if f["id"].endswith("ceiling-tubes")).__setitem__("z", [0.0, 2.4]),
    "P6's fascia band left unmasked (PRV-02)": lambda t: next(p for p in t["previews"]["photos"] if p["id"] == "P6")["masks"].pop(0),
    "a mask that is not grey in the committed JPEG (PRV-01)": lambda t: next(p for p in t["previews"]["photos"] if p["id"] == "P1")["masks"].__setitem__(0, {"what": "x", "shape": "rect", "box": [20, 200, 80, 260]}),
    "Rita's left wall bare again (a board only 1.8 m long)": lambda t: next(f for f in shop(t, "ritas")["room"]["fixtures"] if f["id"] == "R-left-board").__setitem__("y", [0.9, 2.7]),
    "a fourth question on Jafar's page (the lit list)": lambda t: t["needs_you"].append({"q": "At night, light the units the street file lights or only those open late?", "recommended": "keep the street file's six", "why": "x"}),
    "the nine other fronts pointing at a Markdown section again": lambda t: shop(t, "grocer")["door"].__setitem__("from", "targets/shopfronts/TARGET.md section 10"),
    "Rita's grille with no daytime state": lambda t: shop(t, "ritas").__setitem__("blinds_grilles_shutters", "a closed lattice grille outside the glass at night; none by day"),
}


def main():
    caught = 0
    for name, mut in CONTROLS.items():
        fails, which = run(mut)
        ok = fails > 0
        caught += ok
        print("%s  %-62s -> %d failing %s" % ("CAUGHT" if ok else "MISSED", name, fails, which))
    print("controls: %d of %d caught" % (caught, len(CONTROLS)))
    json.dump({"caught": caught, "of": len(CONTROLS)}, open(os.path.join(HERE, "controls_result.json"), "w"))
    return 0 if caught == len(CONTROLS) else 1


if __name__ == "__main__":
    sys.exit(main())
