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
import sd_place as PL

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
    # the lean and the wall: the roll tips the top toward -y, so the wall must stand on the -y side and the LEFT grip end touches it
    lean = [p for p in T["variants"]["BI2"]["parts"] if p["id"] == "rw_hub"][0]["xf"]["rot"][2]
    rows.near("lean", "lean/12 degrees", lean, 12.0, 0.01, unit="deg")
    rows.add("lean", "lean/every part of the bicycle carries the same transform", len({json.dumps(p.get("xf")) for p in T["variants"]["BI2"]["parts"] if p["id"] != "wall"}) == 1, "")
    wl, wh = ps2.part_bbox("wall")
    bl, bh = ps2.bbox(only=[n for n in ps2.names if n != "wall"])
    sad = ps2.part_bbox("saddle")
    top_y = (sad[0][1] + sad[1][1]) / 2.0
    rows.add("lean", "lean/the wall stands on the side the top tips toward (the saddle's y and the wall are on the same side of the tyres' line)", top_y < 0.0 and wh[1] < 0.0, "saddle y %.0f, the wall's face at y %.0f" % (top_y, wh[1]))
    rows.near("lean", "lean/the bicycle's furthest part on that side just reaches the wall", bl[1], wh[1], 1.5)
    gl_ = ps2.part_bbox("grip_l")
    rows.add("lean", "lean/that furthest part is the left grip's end", abs(gl_[0][1] - bl[1]) < 1.5, "left grip y %.1f, furthest %.1f" % (gl_[0][1], bl[1]))
    ground = ps2.bbox(only=[n for n in ps2.names if "tyre" in n])[1][1]
    clear = T["placement"]["footway_mm"] - (ground - wh[1])
    rows.at_least("placement", "placement/the footway keeps a metre clear beside the leaning bicycle", clear, T["placement"]["min_clear_mm"])
    rows.near("placement", "placement/the stated length is the bicycle's", ps.bbox()[1][0] - ps.bbox()[0][0], T["placement"]["length_mm"], 1.0)
    slot_checks(T, rows, ps2)
    drive_rows(T, rows, ps)
    parts_rows(T, rows, ps)
    rows.add("detail", "detail/no badge, no lettering part", not any(("badge" in n or "plate" in n or "text" in n or "label" in n) for v in T["variants"].values() for n in K._ps_cache(v["parts"]).names), "")
    rows.add("detail", "detail/an adult's frame: seat tube at least 500 and wheels at least 600", math.hypot(st["p1"][0] - st["p0"][0], st["p1"][2] - st["p0"][2]) >= 500 and (rz[0] - rz[1]) >= 600, "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/the two cranks are 180 degrees apart", ps.part_bbox("crank_r")[1][0] > ps.part_bbox("bb_spindle")[1][0] and ps.part_bbox("crank_l")[0][0] < ps.part_bbox("bb_spindle")[0][0], "")


def _cyl_len(p):
    return math.dist(p["p0"], p["p1"])


def _cyl_mid(p):
    return [(p["p0"][i] + p["p1"][i]) / 2.0 for i in range(3)]


def slot_checks(T, rows, ps2):
    """The slot against the street's own drawn openings: the contact on brick, the tyres clear of the door and its step, the pose against the wall."""
    pl = T["placement"]
    pose = pl["poses"][0]
    on = pl["openings_named"]
    sc = PL.scene()
    doors = {d["id"]: d for d in sc["doors"]}
    wins = {w["id"]: w for w in PL.drawn_openings()}
    d = doors["house/" + on["door"]["id"]]
    w = wins[on["window"]["id"]]
    rows.add("slot", "slot/the openings the slot names are the front-doors and house-windows targets' (door, doorstep, window, sill)",
             abs(d["x0"] - on["door"]["x"][0]) < 0.01 and abs(d["x1"] - on["door"]["x"][1]) < 0.01 and abs((d["step"]["w_mm"] / 2000.0 + 0.5 * (d["x0"] + d["x1"])) - on["door"]["step_to_x"]) < 0.01
             and abs(w["x0"] - on["window"]["x"][0]) < 0.01 and abs(w["x1"] - on["window"]["x"][1]) < 0.01 and abs(w["sill_x0"] - on["window"]["sill_x"][0]) < 0.01 and abs(w["y0"] - on["window"]["sill_above_crown_m"]) < 0.001,
             "door %.3f to %.3f, step to %.3f; window %.3f to %.3f, sill from %.3f" % (d["x0"], d["x1"], 0.5 * (d["x0"] + d["x1"]) + d["step"]["w_mm"] / 2000.0, w["x0"], w["x1"], w["sill_x0"]))
    prisms, base = PL.object_prisms(T, pose)
    byn = {q.part: q for q in prisms}
    g = byn["grip_l"].poly.bounds                      # the grip end that touches the wall
    openings = []
    for dd in sc["doors"]:
        if dd["side"] == -1 and dd["kind"] == "house_door":
            st = dd.get("step")
            half = (st["w_mm"] / 2000.0) if st else 0.0
            openings.append((dd["id"], min(dd["x0"], 0.5 * (dd["x0"] + dd["x1"]) - half), max(dd["x1"], 0.5 * (dd["x0"] + dd["x1"]) + half)))
    for ww in PL.drawn_openings():
        openings.append((ww["id"], ww["sill_x0"], ww["sill_x1"]))
    hit = [(n, round(a, 3), round(b, 3)) for n, a, b in openings if g[2] > a - 0.10 and g[0] < b + 0.10]
    rows.add("slot", "slot/the left grip's contact lies on brick: 0.10 m or more clear of every drawn door, doorstep, window and sill", not hit, "contact x %.3f to %.3f; within 0.1 m of: %s" % (g[0], g[2], hit))
    tyres = [q for q in prisms if "tyre" in q.part]
    from shapely.ops import unary_union
    tu = unary_union([q.poly for q in tyres])
    steps = [o for o in sc["obs"] if o.kind == "step" and "west_south" in o.name]
    dstep = min(tu.distance(o.poly) for o in steps)
    ddoor = min(max(0.0, max(dd["x0"] - tu.bounds[2], tu.bounds[0] - dd["x1"])) for dd in sc["doors"] if dd["side"] == -1 and dd["kind"] == "house_door" and "west_south" in dd["id"])
    rows.add("slot", "slot/both tyres stand clear of the door's opening and its doorstep by 0.10 m or more", dstep >= 0.10 and ddoor >= 0.10, "tyres to the doorstep %.2f m; to the door's opening along x %.2f m" % (dstep, ddoor))
    wall_local = ps2.part_bbox("wall")[1][1] / 1000.0
    rows.near("slot", "slot/the wall (z -5.125) is where the pose puts the stand-in wall's face (the pose's z less the wall's distance)", pose["z_m"] + wall_local, pl["wall_z_m"], 0.003, unit="m")
    rows.add("slot", "slot/the bicycle faces +x (up the street) in the pose", PL.to_street(pose, 1000.0, 0.0)[0] > pose["x_m"] + 0.9, "")
    rows.near("slot", "slot/the pose is the stated centre x (the parts' span centre)", (min(q.poly.bounds[0] for q in prisms if q.part != "wall") + max(q.poly.bounds[2] for q in prisms if q.part != "wall")) / 2.0, pl["x_m"], 0.01, unit="m")


def drive_rows(T, rows, ps):
    D = T["drive"]
    R1 = D["pitch_mm"] / (2.0 * math.sin(math.pi / D["ring_teeth"]))
    R2 = D["pitch_mm"] / (2.0 * math.sin(math.pi / D["sprocket_teeth"]))
    ring, spr, hubp = part(T, V, "chainring"), part(T, V, "sprocket"), part(T, V, "rw_hub")
    c1 = (ring["p0"][0], ring["p0"][2])
    c2 = (spr["p0"][0], spr["p0"][2])
    rows.near("drive", "drive/the sprocket is 73 across (18 teeth: its pitch circle is %.1f)" % (2 * R2), 2 * spr["r0"], 73.0, 0.5)
    rows.near("drive", "drive/an 18 tooth sprocket at 12.7 pitch has a pitch circle of about 73", 2 * R2, 73.0, 0.5)
    rows.add("drive", "drive/the chainring (180 across) is a 44 tooth ring at 12.7 pitch: its outer radius is just over the pitch radius", R1 <= ring["r0"] <= R1 + 4.0, "pitch radius %.1f, ring %.1f" % (R1, ring["r0"]))
    rows.near("drive", "drive/the sprocket stands on the hub's axle (x and z)", math.dist(c2, (_cyl_mid(hubp)[0], _cyl_mid(hubp)[2])), 0.0, 0.5)
    chain = [p for p in T["variants"][V]["parts"] if p["id"].startswith("chain_") and p["type"] == "box"]
    names = [p["id"] for p in chain]
    rows.add("drive", "drive/the chain is 28 strips: two runs and 14 + 12 wrap strips", len(chain) == 28 and sum(1 for n in names if n in ("chain_top", "chain_bot")) == 2 and sum(1 for n in names if n.startswith("chain_c")) == 14 and sum(1 for n in names if n.startswith("chain_s")) == 12, "%d strips" % len(chain))
    rows.add("drive", "drive/every chain strip is 8 wide and 6 thick in the plane y = 55", all(abs(p["s"][1] - D["chain_width_mm"]) < 0.01 and abs(p["s"][2] - D["chain_thickness_mm"]) < 0.01 and abs(p["c"][1] - D["chain_y_mm"]) < 0.01 for p in chain), "")
    rows.near("drive", "drive/the chainring lies in the chain's plane", (ring["p0"][1] + ring["p1"][1]) / 2.0, D["chain_y_mm"], 0.5)
    d = math.dist(c1, c2)
    run = math.sqrt(d * d - (R1 - R2) ** 2)
    for nm in ("chain_top", "chain_bot"):
        rows.near("drive", "drive/%s is the tangent run between the pitch circles (%.1f long)" % (nm, run), part(T, V, nm)["s"][0], run, 1.0)
    # the run's place: the outer tangent of the two pitch circles (the tangent points are c + R n, n . (c2 - c1) = R1 - R2)
    ux, uz = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
    a_ = (R1 - R2) / d
    b_ = math.sqrt(max(0.0, 1.0 - a_ * a_))
    for nm, want_up in (("chain_top", True), ("chain_bot", False)):
        cands = [(a_ * ux - e * b_ * uz, a_ * uz + e * b_ * ux) for e in (1.0, -1.0)]
        nx, nz = [c for c in cands if (c[1] > 0) == want_up][0]
        mid = ((c1[0] + R1 * nx + c2[0] + R2 * nx) / 2.0, (c1[1] + R1 * nz + c2[1] + R2 * nz) / 2.0)
        pc = part(T, V, nm)["c"]
        rows.near("drive", "drive/%s lies on the outer tangent of the two pitch circles (centre at x %.1f, z %.1f)" % (nm, mid[0], mid[1]), math.dist((pc[0], pc[2]), mid), 0.0, 1.5)
    # the whole chain's pitch length is a whole, even number of links within half a link
    tot = sum(p["s"][0] for p in chain)
    n_ = round(tot / D["pitch_mm"])
    rows.add("drive", "drive/the chain's length is %d links of 12.7 (an even number, within half a link)" % D["links"], n_ % 2 == 0 and n_ == D["links"] and abs(tot - n_ * D["pitch_mm"]) <= D["pitch_mm"] / 2.0 + 0.5, "%.1f mm = %.2f links" % (tot, tot / D["pitch_mm"]))
    # the wrap strips lie on the pitch circles
    badw = []
    for p in chain:
        if p["id"].startswith("chain_c"):
            r = math.dist((p["c"][0], p["c"][2]), c1)
            if not (R1 - 2.0 <= r <= R1 + 0.2):
                badw.append((p["id"], round(r, 1)))
        elif p["id"].startswith("chain_s"):
            r = math.dist((p["c"][0], p["c"][2]), c2)
            if not (R2 - 2.0 <= r <= R2 + 0.2):
                badw.append((p["id"], round(r, 1)))
    rows.add("drive", "drive/every wrap strip lies on its pitch circle (88.9 on the ring, 36.6 on the sprocket)", not badw, "off: %s" % badw[:4])
    st = part(T, V, "chain_stay_r")
    rows.add("drive", "drive/the chain, ring and sprocket run outboard of the chain stays (their inner side is clear of the stay's outer face)", min(p["c"][1] - p["s"][1] / 2.0 for p in chain) >= abs(st["p0"][1]) + st["r0"] + 2.0 and ring["p0"][1] >= abs(st["p0"][1]) + st["r0"], "chain from y %.1f; stay's outer face %.1f" % (min(p["c"][1] - p["s"][1] / 2.0 for p in chain), abs(st["p0"][1]) + st["r0"]))
    # the chainguard
    g = part(T, V, "chainguard")
    rows.near("guard", "guard/the chainguard is 60 deep and 1 thick", g["s"][1] * 1000 + g["s"][2], D["guard"]["depth_mm"] * 1000 + D["guard"]["thickness_mm"], 0.5)
    lo, hi = ps.part_bbox("chainguard")
    rows.near("guard", "guard/it reaches the sprocket's centre (x 0)", lo[0], c2[0], 3.0)
    rows.near("guard", "guard/its front end is 40 mm behind the chainring's front", hi[0] - (c1[0] + ring["r0"]), -D["guard"]["front_behind_ring_front_mm"], 3.0)
    top = part(T, V, "chain_top")
    ang = math.radians(-top["rot"][1])
    nrm = (-math.sin(ang), math.cos(ang))
    off = (g["c"][0] - top["c"][0]) * nrm[0] + (g["c"][2] - top["c"][2]) * nrm[1]
    rows.near("guard", "guard/it stands 13 mm over the chain's pitch line", off, D["guard"]["over_chain_mm"], 1.0)
    rows.add("guard", "guard/it is fixed to the right chain stay and the seat tube", any(set(j) == {"chainguard", "chainguard_clip"} for j in T["variants"][V]["joins"]) and any(set(j) == {"chainguard_clip", "chain_stay_r"} for j in T["variants"][V]["joins"]) and any(set(j) == {"chainguard_strap", "seat_tube"} for j in T["variants"][V]["joins"]), "")


def parts_rows(T, rows, ps):
    D = T["drive"]
    # rims
    for w, cx in (("rw", 0.0), ("fw", part(T, V, "fw_hub")["p0"][0])):
        rims = [p for p in T["variants"][V]["parts"] if p["id"].startswith(w + "_rim")]
        rows.add("rim", "rim/%s has its own ring of 16 rim segments, 25 wide and 10 deep" % w, len(rims) == 16 and all(abs(p["s"][1] - D["rims"]["width_mm"]) < 0.01 and abs(p["s"][2] - D["rims"]["depth_mm"]) < 0.01 for p in rims), "%d segments" % len(rims))
        rows.add("rim", "rim/%s: the rim's outer face is the tyre's inner face (radius 292)" % w, all(abs(math.hypot(p["c"][0] - cx, p["c"][2] - 330.0) + D["rims"]["depth_mm"] / 2.0 - D["rims"]["outer_face_radius_mm"]) < 1.0 for p in rims), "")
    # brakes
    hubs = {"fw": part(T, V, "fw_hub"), "rw": part(T, V, "rw_hub")}
    for sd in ("l", "r"):
        lv = part(T, V, "brake_lever_%s" % sd)
        rows.near("brake", "brake/lever %s is 120 long and 12 across" % sd, _cyl_len(lv) + lv["r0"] * 2 / 1000.0, D["brakes"]["lever_mm"] + 12.0 / 1000.0, 0.5)
        gr = part(T, V, "grip_%s" % sd)
        rows.add("brake", "brake/lever %s is clamped under its grip's inner end" % sd, abs(gr["p0"][1]) <= abs(lv["p0"][1]) <= abs(gr["p1"][1]) and 0.0 <= (gr["p0"][2] - lv["p0"][2]) <= 20.0, "lever at y %.0f z %.0f; grip axis z %.0f" % (lv["p0"][1], lv["p0"][2], gr["p0"][2]))
    for nm, lv_nm in (("brake_rod_f", "brake_lever_l"), ("brake_rod_r", "brake_lever_r")):
        rd = part(T, V, nm)
        lv = part(T, V, lv_nm)
        rows.near("brake", "brake/%s is 8 across" % nm, rd["r0"] * 2, D["brakes"]["rod_mm"], 0.1)
        rows.near("brake", "brake/%s starts at its lever's tip" % nm, math.dist(rd["p0"], lv["p1"]), 0.0, 1.0)
    for w, cx in (("rw", 0.0), ("fw", hubs["fw"]["p0"][0])):
        bar = part(T, V, "%s_stirrup_bar" % w)
        mid = _cyl_mid(bar)
        rad = math.hypot(mid[0] - cx, mid[2] - 330.0)
        rows.near("brake", "brake/%s stirrup crossbar lies under the rim at radius 270 (the rim's inner face is 282)" % w, rad, D["brakes"]["stirrup_radius_mm"], 1.0)
        rows.near("brake", "brake/%s stirrup crossbar is 56 wide and 6 across" % w, _cyl_len(bar) + bar["r0"] * 2 / 1000.0, 56.0 + 6.0 / 1000.0, 0.5)
        pads = [p for p in T["variants"][V]["parts"] if p["id"].startswith(w + "_pad_")]
        rows.add("brake", "brake/%s has two pads whose outer face is at the rim's inner face (281 against 282)" % w, len(pads) == 2 and all(abs(math.hypot(p["c"][0] - cx, p["c"][2] - 330.0) + p["s"][2] / 2.0 - D["brakes"]["rim_inner_radius_mm"]) <= 2.5 for p in pads), "%d pads" % len(pads))
        br = part(T, V, "%s_brake_bridge" % w)
        rows.at_least("brake", "brake/%s bridge stands above the tyre and its mudguard (radius 345 or more)" % w, math.hypot(br["c"][0] - cx, br["c"][2] - 330.0), 345.0)
    # mudguard stays and the reflector
    for w, cx in (("rw", 0.0), ("fw", hubs["fw"]["p0"][0])):
        sts = [p for p in T["variants"][V]["parts"] if p["id"].startswith(w + "_guard_stay_")]
        rows.add("guard", "guard/%s mudguard has two 5 mm stays running to the drop-out at the axle's height" % w, len(sts) == 2 and all(abs(p["r0"] * 2 - 5.0) < 0.01 and abs(p["p1"][2] - 330.0) < 1.0 and abs(abs(p["p1"][1]) - 57.0) < 1.0 and p["p0"][2] > 400.0 for p in sts) and sts[0]["p1"][1] * sts[1]["p1"][1] < 0, "%d stays" % len(sts))
    rf = part(T, V, "rw_reflector")
    rows.add("guard", "guard/the rear reflector is red, 60 across, faces back and sits on the rear mudguard's tail", rf["material"] == "reflector_red" and abs(2 * rf["r0"] - 60.0) < 0.1 and rf["p1"][0] < rf["p0"][0] and abs(rf["p1"][1]) < 0.01 and ps.part_bbox("rw_guard5")[0][0] - 12.0 <= rf["p0"][0] <= ps.part_bbox("rw_guard5")[1][0] + 12.0 and rf["p0"][2] > 400.0, "")
    # carrier
    dk = ps.part_bbox("carrier_deck")
    rows.add("carrier", "carrier/the platform is 340 x 130 at 780 and stands 80 mm or more over the rear mudguard", abs((dk[1][0] - dk[0][0]) - D["carrier"]["length_mm"]) < 1.0 and abs((dk[1][1] - dk[0][1]) - D["carrier"]["width_mm"]) < 1.0 and abs(dk[1][2] - D["carrier"]["top_mm"]) < 1.0 and dk[0][2] - ps.bbox(only=[n for n in ps.names if n.startswith("rw_guard")])[1][2] >= 80.0, "deck top %.0f; guard top %.0f" % (dk[1][2], ps.bbox(only=[n for n in ps.names if n.startswith("rw_guard")])[1][2]))
    rails = [p for p in T["variants"][V]["parts"] if p["id"] in ("carrier_rail_l", "carrier_rail_r", "carrier_cross_rear")]
    stays = [p for p in T["variants"][V]["parts"] if p["id"] in ("carrier_stay_l", "carrier_stay_r")]
    rows.add("carrier", "carrier/two side rails, a rear cross rail and two stays, all 10 mm tube", len(rails) == 3 and len(stays) == 2 and all(abs(p["r0"] * 2 - D["carrier"]["tube_mm"]) < 0.01 for p in rails + stays), "%d rails, %d stays" % (len(rails), len(stays)))
    rows.add("carrier", "carrier/each stay runs from the rail's rear end to the drop-out (axle height within 25 mm, |y| 57)", all(abs(p["p1"][2] - 340.0) < 25.0 and abs(abs(p["p1"][1]) - 57.0) < 1.0 and abs(p["p0"][2] - (D["carrier"]["top_mm"] - 9.0)) < 1.0 for p in stays), "")
    rows.add("carrier", "carrier/the platform is clear of the saddle (100 mm or more below it) and meets the seat stay at its front end", dk[1][2] + 100.0 <= ps.part_bbox("saddle")[0][2] and any(set(j) == {"carrier_deck", "seat_stay_l"} for j in T["variants"][V]["joins"]), "")


def extra_controls(T):
    return [
        ("frame: the seat tube made 80 degrees", lambda t: part(t, V, "seat_tube").__setitem__("p1", [part(t, V, "seat_tube")["p0"][0] - 100.0, 0.0, part(t, V, "seat_tube")["p0"][2] + 567.0]), "frame/seat tube angle"),
        ("frame: the head tube made 75 degrees", lambda t: part(t, V, "head_tube").__setitem__("p0", [part(t, V, "head_tube")["p1"][0] + 39.0, 0.0, part(t, V, "head_tube")["p1"][2] - 145.0]), "frame/head tube angle"),
        ("frame: the top tube sloping 100 mm", lambda t: part(t, V, "top_tube").__setitem__("p1", [part(t, V, "top_tube")["p1"][0], 0.0, part(t, V, "top_tube")["p1"][2] + 100.0]), "frame/the top tube is level"),
        ("range: the saddle 150 mm too high", lambda t: K.shift_part(t, V, "saddle", [0, 0, 150]), "range/saddle top"),
        ("range: a wheelbase of 1300 (the front wheel's hub moved)", lambda t: K.shift_part(t, V, "fw_hub", [200, 0, 0]), "range/wheelbase"),
        ("wheel: one front tyre segment removed", lambda t: K.drop_part(t, V, "fw_tyre3"), "wheel/sixteen tyre segments"),
        ("lean: 25 degrees on one part only", lambda t: part(t, "BI2", "bell").__setitem__("xf", {"rot": [0, 0, 25], "t": [0, 0, 0], "pivot": [0, 0, 0]}), "lean/every part of the bicycle carries the same transform"),
        ("lean: the wall 50 mm further off", lambda t: K.shift_part(t, "BI2", "wall", [0, -50, 0]), "lean/the bicycle's furthest part on that side just reaches the wall"),
        ("lean: the wall put on the far side (+y), where the first version had it, against the right grip", lambda t: K.shift_part(t, "BI2", "wall", [0, 800.0, 0]), "lean/the wall stands on the side the top tips toward"),
        ("lean: the bicycle rolled the other way (-12) with the wall where it was", lambda t: [p.__setitem__("xf", {"rot": [0, 0, -12.0], "t": [0, 0, 0], "pivot": [0, 0, 0]}) for p in t["variants"]["BI2"]["parts"] if p["id"] != "wall"], "lean/the wall stands on the side the top tips toward"),
        PL.ctl("slot: the first version's centre (pivot x 15.0: the grip lands on the cottage window at x 15.7)", "bicycle", "slot/the left grip's contact lies on brick", x_m=15.0),
        PL.ctl("slot: the bicycle at the cottage door (x 12.9): the tyres stand in the door's approach", "bicycle", "place/bicycle/clear of every shop and house door zone", x_m=12.9),
        PL.ctl("slot: the tyres across the doorstep (x 13.4)", "bicycle", "slot/both tyres stand clear", x_m=13.4),
        PL.ctl("slot: the bicycle standing in the carriageway (z -2.0)", "bicycle", "place/bicycle/feet lie in zone", z_m=-2.0),
        PL.ctl("slot: the bicycle 0.5 m out from the wall (the grip no longer touches)", "bicycle", "slot/the wall (z -5.125)", z_m=-4.0257),
        PL.ctl("slot: the bicycle turned to face -x", "bicycle", "slot/the bicycle faces +x", yaw_deg=180.0),
        ("slot: the stated door opening moved 0.3 m", lambda t: t["placement"]["openings_named"]["door"].__setitem__("x", [13.381, 14.219]), "slot/the openings the slot names"),
        ("slot: a window recorded at x 15.0 in the stated openings", lambda t: t["placement"]["openings_named"]["window"].__setitem__("sill_x", [14.5, 15.5]), "slot/the openings the slot names"),
        ("drive: the chain strips 12 wide", lambda t: [p["s"].__setitem__(1, 12.0) for p in t["variants"][V]["parts"] if p["id"].startswith("chain_") and p["type"] == "box"], "drive/every chain strip is 8 wide"),
        ("drive: the sprocket 100 across", lambda t: part(t, V, "sprocket").__setitem__("r0", 50.0), "drive/the sprocket is 73 across"),
        ("drive: one wrap strip missing", lambda t: K.drop_part(t, V, "chain_c07"), "drive/the chain is 28 strips"),
        ("drive: the top run moved 30 mm", lambda t: K.shift_part(t, V, "chain_top", [0, 0, 30.0]), "drive/chain_top lies on the outer tangent"),
        ("drive: the ring's tooth count stated as 50 (the chain would be 40 mm longer)", lambda t: t["drive"].__setitem__("ring_teeth", 50), "drive/the chainring (180 across) is a 44 tooth ring"),
        ("drive: the chain inboard of the stay (y moved 25 mm)", lambda t: [p.__setitem__("c", [p["c"][0], p["c"][1] - 25.0, p["c"][2]]) for p in t["variants"][V]["parts"] if p["id"].startswith("chain_") and p["type"] == "box"], "drive/the chain, ring and sprocket run outboard"),
        ("drive: a wrap strip pushed 8 mm off its circle", lambda t: K.shift_part(t, V, "chain_s04", [-8.0, 0, 0]), "drive/every wrap strip lies on its pitch circle"),
        ("guard: the chainguard 30 deep", lambda t: part(t, V, "chainguard").__setitem__("s", [part(t, V, "chainguard")["s"][0], 30.0, 1.0]), "guard/the chainguard is 60 deep"),
        ("guard: the chainguard 30 mm over the chain", lambda t: K.shift_part(t, V, "chainguard", [0, 0, 17.0]), "guard/it stands 13 mm over the chain"),
        ("guard: no fixings for the chainguard", lambda t: t["variants"][V]["joins"].remove(["chainguard_strap", "seat_tube"]), "guard/it is fixed to the right chain stay"),
        ("rim: one rim segment missing from the front wheel", lambda t: K.drop_part(t, V, "fw_rim3"), "rim/fw has its own ring of 16"),
        ("rim: the rear rim 40 wide", lambda t: [p["s"].__setitem__(1, 40.0) for p in t["variants"][V]["parts"] if p["id"].startswith("rw_rim")], "rim/rw has its own ring of 16"),
        ("rim: the front rim ring 12 mm too far out", lambda t: [K.shift_part(t, V, "fw_rim%d" % k, [12.0 * math.cos(2 * math.pi * (k - 1) / 16), 0, 12.0 * math.sin(2 * math.pi * (k - 1) / 16)]) for k in range(1, 17)], "rim/fw: the rim's outer face is the tyre's inner face"),
        ("brake: the left lever 80 long", lambda t: part(t, V, "brake_lever_l").__setitem__("p1", [part(t, V, "brake_lever_l")["p0"][0] + 70.0, part(t, V, "brake_lever_l")["p0"][1], part(t, V, "brake_lever_l")["p0"][2] - 40.0]), "brake/lever l is 120 long"),
        ("brake: the front rod 5 across", lambda t: part(t, V, "brake_rod_f").__setitem__("r0", 2.5), "brake/brake_rod_f is 8 across"),
        ("brake: the front stirrup inside the rim (crossbar 20 mm too high)", lambda t: K.shift_part(t, V, "fw_stirrup_bar", [0, 0, 20.0]), "brake/fw stirrup crossbar lies under the rim"),
        ("brake: a pad removed", lambda t: K.drop_part(t, V, "rw_pad_r"), "brake/rw has two pads"),
        ("brake: the rear bridge dropped into the tyre (40 mm)", lambda t: K.shift_part(t, V, "rw_brake_bridge", [-60.0, 0, -80.0]), "brake/rw bridge stands above the tyre"),
        ("stay: one mudguard stay removed from the rear guard", lambda t: K.drop_part(t, V, "rw_guard_stay_r"), "guard/rw mudguard has two 5 mm stays"),
        ("stay: the front guard's stays 8 across", lambda t: [part(t, V, n).__setitem__("r0", 4.0) for n in ("fw_guard_stay_l", "fw_guard_stay_r")], "guard/fw mudguard has two 5 mm stays"),
        ("reflector: 40 across", lambda t: part(t, V, "rw_reflector").__setitem__("r0", 20.0), "guard/the rear reflector is red"),
        ("carrier: the platform 120 mm lower", lambda t: K.shift_part(t, V, "carrier_deck", [0, 0, -120.0]), "numbers/N13"),
        ("carrier: the platform only 200 long", lambda t: part(t, V, "carrier_deck").__setitem__("s", [200.0, 130.0, 4.0]), "numbers/N11"),
        ("carrier: the platform 60 mm over the guard only (rails and stays 14 across)", lambda t: [part(t, V, n).__setitem__("r0", 7.0) for n in ("carrier_rail_l", "carrier_rail_r", "carrier_cross_rear", "carrier_stay_l", "carrier_stay_r")], "carrier/two side rails, a rear cross rail and two stays"),
        ("carrier: one stay removed", lambda t: K.drop_part(t, V, "carrier_stay_l"), "carrier/two side rails"),
        ("placement: a 1.2 m wide footway taken", lambda t: t["placement"].__setitem__("footway_mm", 1200.0), "placement/the footway keeps a metre clear"),
        ("detail: a badge part on the head tube", lambda t: t["variants"][V]["parts"].append({"id": "head_badge", "type": "box", "c": [900, -20, 760], "s": [60, 3, 40], "material": "steel"}), "detail/no badge"),
        ("detail: a ballast block through the top tube", lambda t: t["variants"][V]["parts"].append({"id": "ballast", "type": "box", "c": [560, 0, 840], "s": [100, 100, 100], "material": "steel"}), "geometry/BI1/no part sinks into another"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="bell", leaf_move=[0, 0, 60], bridge="seat_post", join=("crank_r", "bb_spindle"), join_move=[0, 0, 60], blocker={}, number_id="N2")
    sys.exit(1 if SF.selfcheck_main(HERE, "bicycle", extra, extra_controls, spec) else 0)
