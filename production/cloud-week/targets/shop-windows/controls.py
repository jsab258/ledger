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
