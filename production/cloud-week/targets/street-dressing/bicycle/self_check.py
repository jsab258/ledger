"""bicycle: the self-check. python self_check.py [--live] [--previews] [--no-controls]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF

V = "BI1"


def part(T, V_, pid):
    return [p for p in T["variants"][V_]["parts"] if p["id"] == pid][0]


def tube_angle(p):
    dx = p["p1"][0] - p["p0"][0]
    dz = p["p1"][2] - p["p0"][2]
    return math.degrees(math.atan2(abs(dz), abs(dx)))


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    ps2 = K._ps_cache(T["variants"]["BI2"]["parts"])
    st = part(T, V, "seat_tube")
    ht = part(T, V, "head_tube")
    rows.near("frame", "frame/seat tube angle from its own end points is 72 degrees", tube_angle(st), 72.0, 1.0, unit="deg")
    rows.near("frame", "frame/head tube angle from its own end points is 68 degrees", tube_angle(ht), 68.0, 1.0, unit="deg")
    rows.add("frame", "frame/the top tube is level", abs(part(T, V, "top_tube")["p0"][2] - part(T, V, "top_tube")["p1"][2]) < 12.0, "")
    # wheels
    tr = [ps.part_bbox(n) for n in ps.names if n.startswith("rw_tyre")]
    tf = [ps.part_bbox(n) for n in ps.names if n.startswith("fw_tyre")]
    rz = (max(h[2] for l, h in tr), min(l[2] for l, h in tr))
    fz = (max(h[2] for l, h in tf), min(l[2] for l, h in tf))
    rows.near("wheel", "wheel/both tyres stand on the ground and are the same height", abs(rz[0] - fz[0]) + abs(rz[1] - fz[1]) + abs(rz[1]) + abs(fz[1]), 0.0, 1.0)
    rows.add("wheel", "wheel/sixteen tyre segments and eight spokes on each wheel", all(len([n for n in ps.names if n.startswith(w + "_tyre")]) == 16 and len([n for n in ps.names if n.startswith(w + "_spoke")]) == 8 for w in ("rw", "fw")), "")
    # bottom bracket 30 below the axles
    rows.near("frame", "frame/the bottom bracket is 30 mm below the axle line", ps.part_bbox("rw_hub")[0][2] / 1.0 + 0 - 0 + (ps.part_bbox("rw_hub")[1][2] - ps.part_bbox("rw_hub")[0][2]) / 2 - (ps.part_bbox("bb_spindle")[0][2] + ps.part_bbox("bb_spindle")[1][2]) / 2, 30.0, 1.0)
    # ranges for a gent's roadster
    sad = ps.part_bbox("saddle")[1][2]
    rows.add("range", "range/saddle top between 900 and 1100", 900 <= sad <= 1100, "%.0f" % sad)
    wb = (ps.part_bbox("fw_hub")[0][0] + ps.part_bbox("fw_hub")[1][0]) / 2 - (ps.part_bbox("rw_hub")[0][0] + ps.part_bbox("rw_hub")[1][0]) / 2
    rows.add("range", "range/wheelbase between 1050 and 1160", 1050 <= wb <= 1160, "%.0f" % wb)
    gr = ps.part_bbox("grip_r")[1][2]
    rows.add("range", "range/grips between the saddle less 100 and the saddle plus 100", sad - 100 <= gr <= sad + 100, "%.0f against %.0f" % (gr, sad))
    # the lean and the wall
    lean = [p for p in T["variants"]["BI2"]["parts"] if p["id"] == "rw_hub"][0]["xf"]["rot"][2]
    rows.near("lean", "lean/12 degrees", lean, 12.0, 0.01, unit="deg")
    rows.add("lean", "lean/every part of the bicycle carries the same transform", len({json.dumps(p.get("xf")) for p in T["variants"]["BI2"]["parts"] if p["id"] != "wall"}) == 1, "")
    wl, wh = ps2.part_bbox("wall")
    bl, bh = ps2.bbox(only=[n for n in ps2.names if n != "wall"])
    rows.near("lean", "lean/the bicycle's furthest part just reaches the wall", bh[1], wl[1], 1.5)
    ground = ps2.bbox(only=[n for n in ps2.names if "tyre" in n])[0][1]
    clear = T["placement"]["footway_mm"] - (wl[1] - ground)
    rows.at_least("placement", "placement/the footway keeps a metre clear beside the leaning bicycle", clear, T["placement"]["min_clear_mm"])
    rows.near("placement", "placement/the stated length is the bicycle's", ps.bbox()[1][0] - ps.bbox()[0][0], T["placement"]["length_mm"], 1.0)
    rows.add("detail", "detail/no badge, no lettering part", not any(("badge" in n or "plate" in n or "text" in n or "label" in n) for v in T["variants"].values() for n in K._ps_cache(v["parts"]).names), "")
    rows.add("detail", "detail/an adult's frame: seat tube at least 500 and wheels at least 600", math.hypot(st["p1"][0] - st["p0"][0], st["p1"][2] - st["p0"][2]) >= 500 and (rz[0] - rz[1]) >= 600, "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/the two cranks are 180 degrees apart", ps.part_bbox("crank_r")[1][0] > ps.part_bbox("bb_spindle")[1][0] and ps.part_bbox("crank_l")[0][0] < ps.part_bbox("bb_spindle")[0][0], "")


def extra_controls(T):
    return [
        ("frame: the seat tube made 80 degrees", lambda t: part(t, V, "seat_tube").__setitem__("p1", [part(t, V, "seat_tube")["p0"][0] - 100.0, 0.0, part(t, V, "seat_tube")["p0"][2] + 567.0]), "frame/seat tube angle"),
        ("frame: the head tube made 75 degrees", lambda t: part(t, V, "head_tube").__setitem__("p0", [part(t, V, "head_tube")["p1"][0] + 39.0, 0.0, part(t, V, "head_tube")["p1"][2] - 145.0]), "frame/head tube angle"),
        ("frame: the top tube sloping 100 mm", lambda t: part(t, V, "top_tube").__setitem__("p1", [part(t, V, "top_tube")["p1"][0], 0.0, part(t, V, "top_tube")["p1"][2] + 100.0]), "frame/the top tube is level"),
        ("range: the saddle 150 mm too high", lambda t: K.shift_part(t, V, "saddle", [0, 0, 150]), "range/saddle top"),
        ("range: a wheelbase of 1300 (the front wheel's hub moved)", lambda t: K.shift_part(t, V, "fw_hub", [200, 0, 0]), "range/wheelbase"),
        ("wheel: one front tyre segment removed", lambda t: K.drop_part(t, V, "fw_tyre3"), "wheel/sixteen tyre segments"),
        ("lean: 25 degrees on one part only", lambda t: part(t, "BI2", "bell").__setitem__("xf", {"rot": [0, 0, 25], "t": [0, 0, 0], "pivot": [0, 0, 0]}), "lean/every part of the bicycle carries the same transform"),
        ("lean: the wall 50 mm further off", lambda t: K.shift_part(t, "BI2", "wall", [0, 50, 0]), "lean/the bicycle's furthest part just reaches the wall"),
        ("placement: a 1.2 m wide footway taken", lambda t: t["placement"].__setitem__("footway_mm", 1200.0), "placement/the footway keeps a metre clear"),
        ("detail: a badge part on the head tube", lambda t: t["variants"][V]["parts"].append({"id": "head_badge", "type": "box", "c": [900, -20, 760], "s": [60, 3, 40], "material": "steel"}), "detail/no badge"),
        ("detail: a ballast block through the top tube", lambda t: t["variants"][V]["parts"].append({"id": "ballast", "type": "box", "c": [560, 0, 840], "s": [100, 100, 100], "material": "steel"}), "geometry/BI1/no part sinks into another"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="bell", leaf_move=[0, 0, 60], bridge="seat_post", join=("crank_r", "bb_spindle"), join_move=[0, 0, 60], blocker={}, number_id="N2")
    sys.exit(1 if SF.selfcheck_main(HERE, "bicycle", extra, extra_controls, spec) else 0)
