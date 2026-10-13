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
import sd_place as PLC
import re
import struct

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
    rows.add("detail", "detail/no stamp, owner's or hire mark: no such part, no decal, an empty marks list in the texture spec", not any(("stamp" in n or "mark" in n or "label" in n or "ippc" in n) for n in ps.names) and T["texture"]["marks"] == [] and not any(re.search(r"stamp|owner|ippc|hire|brand|logo|lettering|text", str(d), re.I) for d in T["texture"]["decals"]), str(T["texture"]))
    # the materials' notes and the texture note may say there is NO mark; they may not say there is one
    pos = []
    for k, m in T["materials"].items():
        for clause in re.split(r"[;,.]", m.get("note", "") + ";" + T["texture"]["note"]):
            if re.search(r"stamp|ippc|owner|brand|hire|logo", clause, re.I) and not re.search(r"\bno\b|\bnot\b|\bnever\b|left off|without|plain", clause, re.I):
                pos.append(clause.strip())
    rows.add("detail", "detail/no material or texture note describes a stamp, owner's, hire or IPPC mark as present", not pos, str(pos[:3]))
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    # standard sizes
    rows.add("detail", "detail/the size is a European standard (1000 x 1200 x 144)", abs(p1.bbox()[1][0] - p1.bbox()[0][0] - 1000) < 1 and abs(p1.bbox()[1][1] - p1.bbox()[0][1] - 1200) < 1 and abs(p1.bbox()[1][2] - 144) < 0.5, "")
    # the scene
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    held = {i["asset"]: i for i in sc["held_props"]["not_placed"]}
    big = held["large_pallet"]
    bd = glb_dims(os.path.join(L.REPO, "ledger", "Assets", "Props", "base-mesh", "large_pallet.glb"))
    td = sorted([p1.bbox()[1][i] - p1.bbox()[0][i] for i in range(3)])
    sd = sorted(bd)
    rows.add("reuse", "reuse/the scene's large pallet (read from its model: dims_m compared with this target's box) is not this target's size", any(abs(a * 1000 - b) > 100.0 for a, b in zip(sd, td)) and "2.00 x 1.10" in big["why"], "model %s m, target %s mm" % ([round(v, 3) for v in sd], [round(v) for v in td]))
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
    pose = pl["poses"][0]
    prisms, base = PLC.object_prisms(T, pose)
    from shapely.ops import unary_union
    wl_ = unary_union([q.poly for q in prisms if q.part == "wall_gable"]).bounds
    pal = unary_union([q.poly for q in prisms if q.part != "wall_gable"]).bounds
    rows.near("placement", "placement/the gable wall's face (the pose's stand-in) is street x 21.0 and the leaning pallet's top edge reaches it", wl_[2], pl["x_wall_m"], 0.002, unit="m")
    rows.near("placement", "placement/the leaning pallet's top edge touches the wall face", pal[0], pl["x_wall_m"], 0.002, unit="m")
    rows.add("placement", "placement/the pose is the stated slot (centre z, yaw 90 so that local +y points into the wall)", abs(pose["z_m"] - pl["z_centre_m"]) < 1e-6 and PLC.to_street(pose, 0.0, 1000.0)[0] < pose["x_m"] - 0.9, "")
    fl = pl["floor"]
    rows.add("placement", "placement/the floor is stated as a Judgement, not modelled today, level 0.100, and handed over (H1)", fl["kind"] == "Judgement" and fl["modelled_today"] is False and abs(fl["level_m"] - 0.100) < 1e-9 and any(h["id"] == "H1" for h in T["handovers"]) and "gap in the data" in fl["reason"], "")
    gp = [p for p in json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-pieces.json")))["pieces"] if p["name"].startswith("ground_plot")]
    top = [p["y_m"] + p["sy_m"] / 2.0 for p in gp]
    rows.add("placement", "placement/the floor level is the ground plots' top (0.100 from vignette-pieces.json) and no ground piece covers the yard mouth today", all(abs(t - fl["level_m"]) < 0.002 for t in top) and not any(p["x_m"] - p["sx_m"] / 2 < 22.0 < p["x_m"] + p["sx_m"] / 2 and p["z_m"] - p["sz_m"] / 2 < -6.0 < p["z_m"] + p["sz_m"] / 2 for p in gp), "plot tops %s" % [round(t, 3) for t in top])


def glb_dims(path):
    """The model's size in metres as the engine sees it: the accessor's min and max through the node's scale and rotation."""
    import numpy as np
    b = open(path, "rb").read()
    length = struct.unpack("<III", b[:12])[2]
    off, js = 12, None
    while off < length:
        cl, ct = struct.unpack("<II", b[off:off + 8])
        off += 8
        if ct == 0x4E4F534A:
            js = json.loads(b[off:off + cl])
        off += cl
    nodes = js["nodes"]
    out = []

    def walk(i, M):
        n = nodes[i]
        S = np.diag(n.get("scale", [1, 1, 1]))
        x, y, z, w = n.get("rotation", [0, 0, 0, 1])
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        M2 = M @ R @ S
        if "mesh" in n:
            for pr in js["meshes"][n["mesh"]]["primitives"]:
                a = js["accessors"][pr["attributes"]["POSITION"]]
                lo, hi = a["min"], a["max"]
                for cx in (lo[0], hi[0]):
                    for cy in (lo[1], hi[1]):
                        for cz in (lo[2], hi[2]):
                            out.append(M2 @ np.array([cx, cy, cz]))
        for c in n.get("children", []):
            walk(c, M2)
    for r in js["scenes"][0]["nodes"]:
        walk(r, np.eye(3))
    arr = np.array(out)
    return list(arr.max(0) - arr.min(0))


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
        PLC.ctl("placement: the pallets moved to x 25 (into west_north's carcass)", "pallets", "place/pallets/clear of every street piece", x_m=25.0),
        PLC.ctl("placement: the pallets set behind the owed floor (z -14.5), where nothing is modelled", "pallets", "place/pallets/every foot lies on a modelled surface", z_m=-14.5),
        PLC.ctl("placement: the pallets moved to x 20.2, off the owed floor and onto no modelled ground", "pallets", "place/pallets/every foot lies on a modelled surface", x_m=20.2),
        PLC.ctl("placement: the pallets moved forward onto the crowd-control barrier (z -4.9)", "pallets", "place/pallets/clear of every street piece", z_m=-4.9, x_m=22.9),
        PLC.ctl("placement: the pallets set at the crates' x with z -4.3 (on the pavement, on the barrier and the crates)", "pallets", "place/pallets/clear of every street piece", z_m=-4.3, x_m=22.4),
        ("placement: the owed floor withdrawn from the pose (no floor, no modelled ground)", lambda t: PLC.pose_by_id(t, "pallets").pop("floor_owed"), "place/pallets/every foot lies on a modelled surface"),
        ("placement: the floor level stated at 0.0 (the crown) while the pose stands at 0.100", lambda t: PLC.pose_by_id(t, "pallets")["floor_owed"].__setitem__("level_m", 0.0), "place/pallets/the owed floor is stated with a level"),
        ("placement: the floor claimed as modelled today", lambda t: t["placement"]["floor"].__setitem__("modelled_today", True), "placement/the floor is stated as a Judgement"),
        ("placement: the stated wall x moved", lambda t: t["placement"].__setitem__("x_wall_m", 20.5), "placement/the gable wall's face"),
        ("placement: the pose turned so local +y points away from the wall (yaw 270)", lambda t: PLC.set_pose(t, "pallets", yaw_deg=270.0), "placement/the pose is the stated slot"),
        ("detail: an IPPC stamp described in a material's note", lambda t: t["materials"]["pallet_wood"].__setitem__("note", t["materials"]["pallet_wood"]["note"] + "; an IPPC stamp on each end block"), "detail/no material or texture note describes"),
        ("detail: a stamp decal in the texture spec", lambda t: t["texture"]["decals"].append({"name": "owner stamp", "where": "end block"}), "detail/no stamp, owner's or hire mark"),
        ("detail: the scene's large pallet's size taken as this target's (2.00 x 1.10 x 0.19)", lambda t: (K.scale_all(t, "PA1", 0, 2.0), K.scale_all(t, "PA1", 1, 1100.0 / 1200.0), K.scale_all(t, "PA1", 2, 190.0 / 144.0)), "reuse/the scene's large pallet"),
        ("detail: a stamp part on a board", lambda t: t["variants"][V]["parts"].append({"id": "p1_stamp", "type": "box", "c": [0, 0, 150], "s": [60, 40, 1], "material": "pallet_wood"}), "detail/no stamp, owner's or hire mark"),
    ]


if __name__ == "__main__":
    spec = dict(V="PA1", leaf="p1_top7", leaf_move=[0, 0, 60], bridge=["p1_bot1", "p1_bot2", "p1_bot3"], join=("p1_top1", "p1_str1"), join_move=[0, 0, 60], overlap=("p1_top3", [0, 0, -30]), blocker={"stringer end": "p1_str1"}, number_id="N4", photo_squeeze=0.7)
    sys.exit(1 if SF.selfcheck_main(HERE, "pallets", extra, extra_controls, spec) else 0)
