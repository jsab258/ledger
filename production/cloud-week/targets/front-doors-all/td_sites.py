"""Derives the street's household doors from tools/art-recipes/terrace-front.py (the one home of what the street draws) and the
windows target (which houses were modernised). Used by make_target.py (writes them into target.json) and self_check.py --live
(re-derives and compares). Run with /home/user/.bpyenv/bin/python (terrace-front.py needs nothing from bpy at import)."""
import importlib.util
import re
import sys

from td_common import ROOT, TERRACE_FRONT, WINDOWS_T, load_json

sys.dont_write_bytecode = True


def load_tf():
    spec = importlib.util.spec_from_file_location("tf_td", TERRACE_FRONT)
    tf = importlib.util.module_from_spec(spec)
    sys.modules["tf_td"] = tf
    spec.loader.exec_module(tf)
    return tf


SIDE_LEAF = re.compile(r"^(east_parade|west_south|west_north|east_chandler)_side_door_leaf_bay(\d+)$")
KIT_SIDE = re.compile(r"^east_parade_kit_side_door_\d+_[a-z_]+_bay(\d+)$")


def derive():
    """Returns (houses, tf). Each house: block, bay, id, side, door centre x (m, street), leaf x0/x1, casing, doors_on, step, kit flag."""
    tf = load_tf()
    parts, err = tf.plan_street(ROOT)
    if err:
        raise RuntimeError(err)
    by_id = {q["id"]: q for q in parts}
    houses = []
    for q in parts:
        m = SIDE_LEAF.match(q["id"])
        if not m:
            continue
        blk, bay = m.group(1), int(m.group(2))
        cl = by_id.get("%s_side_door_casing_left_bay%d" % (blk, bay))
        cr = by_id.get("%s_side_door_casing_right_bay%d" % (blk, bay))
        head = by_id.get("%s_side_door_casing_head_bay%d" % (blk, bay))
        step = by_id.get("%s_doorstep_bay%d" % (blk, bay))
        lp = by_id.get("%s_letterplate_bay%d" % (blk, bay))
        x0 = min(q["x0"], cl["x0"], cr["x0"])
        x1 = max(q["x1"], cl["x1"], cr["x1"])
        houses.append({
            "block": blk, "bay": bay, "house": "%s_bay%d" % (blk, bay), "side": "east" if blk.startswith("east") else "west",
            "x_centre_m": round((x0 + x1) / 2.0, 3), "opening_w_mm": round((x1 - x0) * 1000.0, 1),
            "leaf_w_mm": round((q["x1"] - q["x0"]) * 1000.0, 1), "leaf_h_mm": round((q["z1"] - q["z0"]) * 1000.0, 1),
            "head_top_above_ground_mm": round((head["z1"] - head["z0"] + 0.0) * 0 + (head["z1"] - q["z0"]) * 1000.0, 1),
            "ground_z_m": round(q["z0"], 3),
            "stand_in_paint": q.get("paint_name"),
            "step": ({"w_mm": round((step["x1"] - step["x0"]) * 1000.0, 1), "depth_mm": round((step["y1"] - step["y0"]) * 1000.0, 1),
                      "h_mm": round((step["z1"] - step["z0"]) * 1000.0, 1)} if step else None),
            "letterplate_stand_in_mm": ([round((lp["x1"] - lp["x0"]) * 1000.0, 1), round((lp["z1"] - lp["z0"]) * 1000.0, 1),
                                         round((lp["z0"] - q["z0"]) * 1000.0, 1)] if lp else None),
            "kit_side_door": False,
        })
    # east_parade bay 2 is the shopfront kit's: its side door is the kit's (a fanlight over it), no leaf part of this name
    kit_bays = sorted({int(KIT_SIDE.match(k).group(1)) for k in by_id if KIT_SIDE.match(k)})
    for bay in kit_bays:
        fan = by_id.get("east_parade_kit_glass_side_door_fanlight_bay%d" % bay)
        houses.append({
            "block": "east_parade", "bay": bay, "house": "east_parade_bay%d" % bay, "side": "east",
            "x_centre_m": round((fan["x0"] + fan["x1"]) / 2.0, 3), "opening_w_mm": round((fan["x1"] - fan["x0"]) * 1000.0, 1),
            "leaf_w_mm": None, "leaf_h_mm": None, "head_top_above_ground_mm": None, "ground_z_m": 0.1, "stand_in_paint": None,
            "step": None, "letterplate_stand_in_mm": None, "kit_side_door": True,
        })
    houses.sort(key=lambda h: (h["side"], h["x_centre_m"]))
    return houses, tf


def modernised_houses():
    """Houses whose windows the windows target made replacement (white_upvc), by house id."""
    t = load_json(WINDOWS_T)
    out = {}
    for s in t["sites"]:
        out.setdefault(s["house"], set()).add(s["paint"])
    return {h: sorted(p) for h, p in out.items()}


if __name__ == "__main__":
    hs, _ = derive()
    mod = modernised_houses()
    for h in hs:
        print(h["house"], h["side"], h["x_centre_m"], h["opening_w_mm"], h["leaf_w_mm"], h["step"], mod.get(h["house"]))
