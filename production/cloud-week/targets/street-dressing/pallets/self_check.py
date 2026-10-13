"""pallets: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF

V = "PA3"


def extra(T, rows):
    p1 = K._ps_cache(T["variants"]["PA1"]["parts"])
    ps = K._ps_cache(T["variants"][V]["parts"])
    pr = T["photo_ratio"]
    tops = sorted(n for n in p1.names if "_top" in n)
    lo0, hi0 = p1.part_bbox(tops[0])
    lo1, hi1 = p1.part_bbox(tops[1])
    bw = hi0[0] - lo0[0]
    pitch = lo1[0] - lo0[0]
    rows.near("photo", "photo/board width over pitch against P1's measured mean", bw / pitch, pr["mean"], pr["tol"], unit="")
    rows.add("photo", "photo/the ratio's own five boards are consistent (spread within 0.08)", max(pr["board_over_pitch"]) - min(pr["board_over_pitch"]) < 0.08, str(pr["board_over_pitch"]))
    # recompute the photograph's ratio from its recorded edges
    pm = json.load(open(os.path.join(HERE, "photo_measurements.json")))["P1"]["features"]
    fr = [(pm["board%d_right" % k]["px"] - pm["board%d_left" % k]["px"]) / (pm["board%d_left" % (k + 1)]["px"] - pm["board%d_left" % k]["px"]) for k in range(1, 5)]
    rows.near("photo", "photo/the stored mean is the edges' own", sum(fr) / 4.0, pr["mean"], 0.002, unit="")
    # counts
    rows.add("detail", "detail/seven top boards, three stringers, three bottom boards", len([n for n in p1.names if "_top" in n]) == 7 and len([n for n in p1.names if "_str" in n]) == 3 and len([n for n in p1.names if "_bot" in n]) == 3, "")
    tl = [p1.part_bbox(n) for n in tops]
    gaps = [tl[i + 1][0][0] - tl[i][1][0] for i in range(6)]
    rows.add("detail", "detail/the gaps are equal (67.5)", all(abs(g - 67.5) < 0.6 for g in gaps), str([round(g, 1) for g in gaps]))
    rows.add("detail", "detail/the stringers are flush with the board ends and in the middle", abs(p1.part_bbox("p1_str1")[0][1] - p1.part_bbox("p1_top1")[0][1]) < 0.5 and abs(p1.part_bbox("p1_str3")[1][1] - p1.part_bbox("p1_top1")[1][1]) < 0.5 and abs((p1.part_bbox("p1_str2")[0][1] + p1.part_bbox("p1_str2")[1][1]) / 2) < 0.5, "")
    # the lean: from the transform; and the lowest point on the ground
    lean = [p for p in T["variants"][V]["parts"] if p["id"].startswith("p2_top1")][0]["xf"]["rot"][2]
    rows.near("detail", "detail/the lean is 12 degrees from the vertical (78 degrees from the flat)", 90.0 - lean, 12.0, 0.01, unit="deg")
    lo, hi = ps.bbox(only=[n for n in ps.names if n.startswith("p2_")])
    rows.near("detail", "detail/the leaning pallet's lowest edge is on the ground", lo[2], 0.0, 0.5)
    wl, wh = ps.part_bbox("wall_gable")
    rows.near("detail", "detail/the wall face is where the pallet's upper edge reaches", hi[1], wl[1], 0.5)
    rows.add("detail", "detail/no mark: no text, no stamp part", not any(("stamp" in n or "mark" in n or "label" in n) for n in ps.names), "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    # standard sizes
    rows.add("detail", "detail/the size is a European standard (1000 x 1200 x 144)", abs(p1.bbox()[1][0] - p1.bbox()[0][0] - 1000) < 1 and abs(p1.bbox()[1][1] - p1.bbox()[0][1] - 1200) < 1 and abs(p1.bbox()[1][2] - 144) < 0.5, "")
    # the scene
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    held = {i["asset"]: i for i in sc["held_props"]["not_placed"]}
    big = held["large_pallet"]
    rows.add("reuse", "reuse/the scene's large pallet (2.00 x 1.10) is not this target's size", "2.00 x 1.10" in big["why"], big["why"][:60])
    crates = [i for i in sc["held_props"]["items"] if i.get("asset") == "wooden_crate_01"]
    pl = T["placement"]
    # the pallets lie in the yard mouth from the wall at x 21.0 to 21.0 + (extent of the flat pallet's local y) = the clearance to the first crate
    flat_hi = K._ps_cache(T["variants"][V]["parts"]).bbox(only=[n for n in ps.names if n.startswith("p1_")])
    far = pl["x_wall_m"] + (-(flat_hi[0][1])) / 1000.0
    crate_far = max(-(3.0 + c["z_from_kerb_face_m"]) - c["dims_m"][2] / 2 for c in crates)      # the crates' far edge from the street (most negative z)
    crate_far = min(-(3.0 + c["z_from_kerb_face_m"]) - c["dims_m"][2] / 2 for c in crates)
    pallet_near = pl["z_centre_m"] + PL_HALF() / 1000.0
    rows.at_least("placement", "placement/the pallets stand at least 0.6 m behind the scene's crates", crate_far - pallet_near, 0.6, unit="m")
    rows.add("placement", "placement/the pallets are inside the yard mouth (x 21 to 24)", pl["yard_x_m"][0] <= pl["x_wall_m"] and far <= pl["yard_x_m"][1], "far end %.2f" % far)
    rows.add("placement", "placement/behind the barrier line: the pallets stand beyond the building line (z -5.125)", pl["z_centre_m"] - PL_HALF() / 1000.0 < pl["frontage_z_m"], "")


def PL_HALF():
    return 500.0


def extra_controls(T):
    return [
        ("photo: the boards made 60 mm wide", lambda t: [K.scale_all(t, "PA1", 0, 1.0)] and [p.__setitem__("s", [60.0, p["s"][1], p["s"][2]]) for p in t["variants"]["PA1"]["parts"] if p["id"] == "p1_top1" or p["id"] == "p1_top2"], "photo/board width over pitch"),
        ("photo: the ratio stored differently from the edges", lambda t: t["photo_ratio"].__setitem__("mean", 0.40), "photo/the stored mean is the edges' own"),
        ("detail: an eighth top board", lambda t: t["variants"]["PA1"]["parts"].append({"id": "p1_top8", "type": "box", "c": [0, 0, 133], "s": [85, 1200, 22], "material": "pallet_wood"}), "detail/seven top boards"),
        ("detail: the gaps unequal", lambda t: K.shift_part(t, "PA1", "p1_top4", [20, 0, 0]), "detail/the gaps are equal"),
        ("detail: the middle stringer off centre", lambda t: K.shift_part(t, "PA1", "p1_str2", [0, 150, 0]), "detail/the stringers are flush"),
        ("detail: the lean 25 degrees", lambda t: [p["xf"]["rot"].__setitem__(2, 65) for p in t["variants"][V]["parts"] if p["id"].startswith("p2_")], "detail/the lean is 12 degrees"),
        ("detail: the pallet 1100 long", lambda t: [p.__setitem__("s", [p["s"][0], p["s"][1] + 100, p["s"][2]]) for p in t["variants"]["PA1"]["parts"] if p["id"].startswith("p1_bot")], "detail/the size is a European standard"),
        ("placement: the pallets moved out of the yard mouth", lambda t: t["placement"].__setitem__("x_wall_m", 26.0), "placement/the pallets are inside the yard mouth"),
        ("detail: a stamp part on a board", lambda t: t["variants"][V]["parts"].append({"id": "p1_stamp", "type": "box", "c": [0, 0, 150], "s": [60, 40, 1], "material": "pallet_wood"}), "detail/no mark"),
    ]


if __name__ == "__main__":
    spec = dict(V="PA1", leaf="p1_top7", leaf_move=[0, 0, 60], bridge=["p1_bot1", "p1_bot2", "p1_bot3"], join=("p1_top1", "p1_str1"), join_move=[0, 0, 60], overlap=("p1_top3", [0, 0, -30]), blocker={"stringer end": "p1_str1"}, number_id="N4", photo_squeeze=0.7)
    sys.exit(1 if SF.selfcheck_main(HERE, "pallets", extra, extra_controls, spec) else 0)
