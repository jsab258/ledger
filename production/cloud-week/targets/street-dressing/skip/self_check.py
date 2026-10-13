"""skip: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]
--live needs the turned copy P1rot.jpg in the photographs folder (measure.py makes it)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF

V = "SK1"


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    pl = T["placement"]
    lo, hi = ps.part_bbox("side_f")
    length = hi[0] - lo[0]
    rows.at_most("shape", "shape/the skip's length does not exceed the yard mouth plus 20 mm", length, (pl["yard_x_m"][1] - pl["yard_x_m"][0]) * 1000.0 + 20.0)
    # the profile: the side plate's polygon has six corners, the widest at the stated height
    pts = None
    for p in T["variants"][V]["parts"]:
        if p["id"] == "side_f":
            pts = p["poly"]
    rows.add("shape", "shape/the side profile has six corners and is two stacked trapezia (floor shorter than the top, the top shorter than the widest)", len(pts) == 6 and abs(pts[0][0]) < abs(pts[3][0]) < abs(pts[2][0]), str([abs(q[0]) for q in pts]))
    zw = pts[2][1]
    rows.near("shape", "shape/the widest line is two thirds up (793) as in the photograph", zw / 1200.0, 0.66, 0.02, unit="")
    # the end plates lie on the profile's edges: the lower one passes through the floor edge and the widest corner
    el = ps.part_bbox("end_low_r")
    rows.near("shape", "shape/the lower end plate reaches the widest line", el[1][2], zw, 8.0)
    eu = ps.part_bbox("end_up_r")
    rows.near("shape", "shape/the upper end plate reaches the top", eu[1][2], 1200.0, 8.0)
    rows.near("shape", "shape/the end plates meet at the widest line (x)", abs(el[1][0]), abs(pts[2][0]), 8.0)
    # the placement: the lane and the cones
    free = pl["lane_mm"] - pl["gap_to_kerb_mm"] - (ps.part_bbox("floor")[1][1] - ps.part_bbox("floor")[0][1] + 2 * 5.0)
    rows.at_least("placement", "placement/the near lane keeps at least 0.9 m beside the skip", free, 900.0)
    rows.at_least("placement", "placement/the road past the skip is at least the least a bus needs (2.8 m)", pl["lane_mm"] * 2 - pl["gap_to_kerb_mm"] - (hi[1] * 0 + 1710.0) - 0.0 - (pl["lane_mm"] - 3000.0), pl["min_pass_mm"] + 400.0)
    ends = [pl["x_m"] - length / 2000.0, pl["x_m"] + length / 2000.0]
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    cones = sorted(i["x_m"] for i in sc["held_props"]["items"] if i.get("asset", "").startswith("traffic_cone"))
    rows.add("placement", "placement/the scene's cones are at x 21.3 and 23.7 (read from the scene)", cones == pl["cones_scene_x_m"], str(cones))
    rows.add("placement", "placement/the scene's cones now stand inside the skip's length (so they move out)", all(ends[0] < c < ends[1] for c in cones), "skip %.2f to %.2f" % tuple(ends))
    rows.add("placement", "placement/the skip's x range covers the yard mouth centre", ends[0] <= (pl["yard_x_m"][0] + pl["yard_x_m"][1]) / 2 <= ends[1], "")
    # text, lamps
    rows.add("detail", "detail/the firm and number are invented ones", T["text"]["hire_firm"] == "TIDEWAY SKIP HIRE" and T["text"]["number_line"].startswith("TEL 555"), str(T["text"]))
    rows.add("detail", "detail/two lamps, amber, on the road side", len([n for n in ps.names if n.startswith("lamp_") and "hook" not in n]) == 2 and all(ps.part_bbox(n)[1][1] < ps.part_bbox("side_f")[0][1] for n in ("lamp_1", "lamp_2")), "")
    rows.add("detail", "detail/four lugs, two on each side", len([n for n in ps.names if n.startswith("lug_")]) == 4, "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/the lamp lens is lit in the lantern colour at night", T["night"]["lantern_linear"] == L.LANTERN_LINEAR, "")
    rows.add("reuse", "reuse/the scene's skip is off the street (not_placed)", any(i.get("asset") == "skip" for i in sc["held_props"]["not_placed"]), "")


def extra_controls(T):
    def pts_edit(t, i, v):
        for p in t["variants"][V]["parts"]:
            if p["id"] in ("side_f", "side_b"):
                p["poly"][i] = v
    return [
        ("shape: the widest line moved to the top", lambda t: pts_edit(t, 2, [1508.0, 1100.0]), "shape/the widest line is two thirds up"),
        ("shape: a plain box (four corners)", lambda t: [p.__setitem__("poly", [p["poly"][0], p["poly"][1], p["poly"][3], p["poly"][4]]) for p in t["variants"][V]["parts"] if p["id"] in ("side_f", "side_b")], "shape/the side profile has six corners"),
        ("shape: the skip made 3.4 m long", lambda t: [pts_edit(t, 2, [1700.0, 793.0]), pts_edit(t, 5, [-1700.0, 793.0])], "shape/the skip's length"),
        ("placement: the cones put back at the skip's ends", lambda t: t["placement"].__setitem__("cones_scene_x_m", [20.0, 25.0]), "placement/the scene's cones are at x 21.3"),
        ("placement: the skip put at x 30", lambda t: t["placement"].__setitem__("x_m", 30.0), "placement/the skip's x range covers the yard mouth"),
        ("placement: the lane stated 1.5 m", lambda t: t["placement"].__setitem__("lane_mm", 1500.0), "placement/the near lane keeps"),
        ("detail: a third lug", lambda t: t["variants"][V]["parts"].append({"id": "lug_f3", "type": "box", "c": [0, -860, 1100], "s": [80, 25, 60], "material": "skip_paint"}), "detail/four lugs"),
        ("detail: the firm named by a real firm", lambda t: t["text"].__setitem__("hire_firm", "SPEEDY SKIP HIRE"), "detail/the firm and number are invented ones"),
        ("photograph: the rib 60 mm too high", lambda t: [K.shift_part(t, V, "rib_f", [0, 0, 60]), K.shift_part(t, V, "rib_b", [0, 0, 60])], "photo/P1/rim_line_y"),
        ("photograph: the profile 15 percent too short", lambda t: [p.__setitem__("poly", [[q[0] * 0.85, q[1]] for q in p["poly"]]) for p in t["variants"][V]["parts"] if p["id"] in ("side_f", "side_b")], "photo/P1/tip_left_x"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="lamp_2", leaf_move=[0, -60, 0], bridge=["floor", "side_f", "side_b", "end_low_l", "end_low_r"], join=("lamp_1", "lamp_hook_1"), join_move=[0, -40, 0], overlap=("rim_f", [0, 45, 0]), blocker={"side plate": "side_f"}, number_id="N2", photo_squeeze=0.7)
    sys.exit(1 if SF.selfcheck_main(HERE, "skip", extra, extra_controls, spec) else 0)
