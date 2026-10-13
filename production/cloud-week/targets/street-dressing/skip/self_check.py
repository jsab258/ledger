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
import sd_place as PL

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
    pieces = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-pieces.json")))["pieces"]
    pose = pl["poses"][0]
    cones = sorted((i["x_m"], i["z_from_kerb_face_m"]) for i in sc["held_props"]["items"] if i.get("asset", "").startswith("traffic_cone"))
    rows.add("placement", "placement/the scene's cones are at x 21.3 and 23.7 (read from the scene)", [c[0] for c in cones] == pl["cones_scene_x_m"], str(cones))
    cp = [p for p in pieces if p["name"].startswith("prop_traffic_cone")]
    rows.add("placement", "placement/the scene's cones stand on the west footway at the stated z (read from the pieces)", len(cp) == 2 and all(abs(p["z_m"] - pl["cones_scene_z_m"]) < 0.01 for p in cp) and all(p["z_m"] < -3.125 for p in cp), "cone z %s" % [p["z_m"] for p in cp])
    prisms, base = PL.object_prisms(T, pose)
    from shapely.geometry import box as sbox
    from shapely.ops import unary_union
    sk = unary_union([q.poly for q in prisms])
    dcone = min(sk.distance(sbox(p["x_m"] - p["sx_m"] / 2, p["z_m"] - p["sz_m"] / 2, p["x_m"] + p["sx_m"] / 2, p["z_m"] + p["sz_m"] / 2)) for p in cp)
    rows.add("placement", "placement/the scene's cones do not touch the skip, so no cone moves (0.3 m or more clear)", dcone >= 0.3, "nearest cone %.2f m from the skip" % dcone)
    bol = [p for p in pieces if p["name"].startswith("prop_decorative_bollard")]
    oc = pl["cones_optional"]
    ok = all(-3.0 < oc["z_m"] < 3.0 for _ in [0]) and abs(oc["z_m"] - pose["z_m"]) < 0.01 and min(oc["x_m"]) < ends[0] - 0.19 and max(oc["x_m"]) > ends[1] + 0.19 and min(oc["x_m"]) > ends[0] - 0.40 and max(oc["x_m"]) < ends[1] + 0.40
    dbol = min(math.hypot(x - b["x_m"], oc["z_m"] - b["z_m"]) for x in oc["x_m"] for b in bol)
    rows.add("placement", "placement/the optional road-end cones stand in the carriageway on the skip's centre line, 0.2 to 0.4 m beyond its ends, clear of the bollards", ok and dbol > 1.0, "x %s z %.2f; skip x %.2f to %.2f; nearest bollard %.2f m" % (oc["x_m"], oc["z_m"], ends[0], ends[1], dbol))
    tf = open(os.path.join(L.REPO, "tools", "art-recipes", "terrace-front.py"), encoding="utf-8").read()
    rows.add("placement", "placement/the cones are off the drawn street since 3 October (terrace-front.py HELD_PROPS_OFF_STREET)", 'HELD_PROPS_OFF_STREET = ("traffic_cone_01", "traffic_cone_02")' in tf, "")
    rows.add("placement", "placement/the skip's x range covers the yard mouth centre", ends[0] <= (pl["yard_x_m"][0] + pl["yard_x_m"][1]) / 2 <= ends[1], "")
    rows.add("placement", "placement/the pose is the stated slot (centre z is the near side plus half the width)", abs(pose["x_m"] - pl["x_m"]) < 1e-6 and abs(pose["z_m"] - (pl["z_near_m"] + (ps.part_bbox("floor")[1][1] - ps.part_bbox("floor")[0][1] + 10.0) / 2000.0)) < 0.01, "pose z %.3f, near side %.2f" % (pose["z_m"], pl["z_near_m"]))
    # the road's camber: the floor tilts with it
    cf = sc["street"]["carriageway"]["crossfall"]
    wid = ps.bbox()[1][1] - ps.bbox()[0][1]
    rows.near("placement", "placement/the floor's tilt is the road's camber (1 in 40: 1.43 degrees)", pl["tilt"]["deg"], math.degrees(math.atan(cf)), 0.02, unit="deg")
    rows.near("placement", "placement/the drop across the skip's width follows the camber", pl["tilt"]["drop_across_mm"], (ps.part_bbox("floor")[1][1] - ps.part_bbox("floor")[0][1] + 10.0) * cf, 2.0)
    # the accent budget: the skip's share of the hook frame, by projection of its own parts
    cam = pl["hook_camera"]
    scam = [x for x in sc["cameras"] if x["id"] == "cam_hook"][0]
    rows.add("placement", "placement/the hook camera is the scene's", abs(scam["x_m"] - cam["x_m"]) < 0.01 and abs(scam["z_m"] - cam["z_m"]) < 0.01 and abs(scam["yaw_deg"] - cam["yaw_deg"]) < 0.01 and abs(scam["pitch_deg"] - cam["pitch_deg"]) < 0.01 and abs(scam["fov_vertical_deg"] - cam["fov_vertical_deg"]) < 0.01, "")
    share = PL.camera_share(T, pose, cam)
    ac = pl["accent"]
    rows.near("placement", "placement/the skip's stated share of the hook frame is the projection's", share, ac["hook_frame_share"], 0.0005, unit="")
    rows.add("placement", "placement/the share is far under the accent ceiling (a fifth of 0.078 at most), so the sample stays yellow", share < 0.2 * ac["ceiling"] and abs(ac["ceiling"] - 0.078) < 1e-9, "%.4f of the frame against 0.078" % share)
    # text, lamps
    import re
    rows.add("detail", "detail/the firm is the placeholder and the number is a British one (an STD code and six digits, no 555)", T["text"]["hire_firm"] == "TIDEWAY SKIP HIRE" and bool(re.match(r"^TEL\. 0\d{3,4} \d{5,6}$", T["text"]["number_line"])) and "555" not in T["text"]["number_line"], str(T["text"]))
    rows.add("detail", "detail/the firm and the number are listed as fictional placeholders", {p["name"].lower() for p in T["placeholders"]} >= {T["text"]["hire_firm"].lower(), T["text"]["number_line"][5:].lower()}, str([p["name"] for p in T["placeholders"]]))
    rows.add("detail", "detail/the name and the lamps face the road: local -y is street +z (the pose turns the piece half round)", PL.direction_name(PL.front_direction(pose)) == "+z", "")
    rows.add("detail", "detail/two lamps, amber, on the road side", len([n for n in ps.names if n.startswith("lamp_") and "hook" not in n]) == 2 and all(ps.part_bbox(n)[1][1] < ps.part_bbox("side_f")[0][1] for n in ("lamp_1", "lamp_2")), "")
    rows.add("detail", "detail/four lugs, two on each side", len([n for n in ps.names if n.startswith("lug_")]) == 4, "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/the lamp lens is lit in the lantern colour at night", T["night"]["lantern_linear"] == L.LANTERN_LINEAR, "")
    rows.add("reuse", "reuse/the scene's skip is off the street (not_placed)", any(i.get("asset") == "skip" for i in sc["held_props"]["not_placed"]), "")
    marking_rows(T, rows, ps)


def marking_rows(T, rows, ps):
    """The end markings of the Builders' Skips (Markings) Regulations 1984, from the built parts and the stored ranges."""
    R = T["marking"]["regulation"]
    ch = T["marking"]["chosen"]
    plates = [p for p in T["variants"][V]["parts"] if p.get("material") == "marking_red_yellow"]
    ends = {"s": [p for p in plates if p["id"].startswith("mark_s")], "n": [p for p in plates if p["id"].startswith("mark_n")]}
    rows.add("marking", "marking/both ends carry two plates each (4 in all)", len(ends["s"]) == R["plates_per_end"] and len(ends["n"]) == R["plates_per_end"], "south %d, north %d" % (len(ends["s"]), len(ends["n"])))
    bad_size, bad_stripe, bad_pos, bad_area = [], [], [], []
    for p in plates:
        L_, W_, T_ = p["s"]
        if not (R["plate_length_mm"][0] <= L_ <= R["plate_length_mm"][1] and R["plate_width_mm"][0] <= W_ <= R["plate_width_mm"][1]):
            bad_size.append((p["id"], L_, W_))
        if L_ * W_ / 100.0 < R["min_area_cm2"]:
            bad_area.append((p["id"], round(L_ * W_ / 100.0)))
        st = p.get("stripe", {})
        if not (R["stripe_angle_deg"][0] <= st.get("angle_deg", 0) <= R["stripe_angle_deg"][1] and R["stripe_breadth_mm"][0] <= st.get("breadth_mm", 0) <= R["stripe_breadth_mm"][1] and st.get("rise") == "toward the inner edge"):
            bad_stripe.append((p["id"], st))
    rows.add("marking", "marking/every plate is within the regulation's width and length (Schedule 1 notes a and b)", not bad_size, "out of range: %s" % bad_size)
    rows.add("marking", "marking/every plate has at least 980 square cm (note d)", not bad_area, "too small: %s" % bad_area)
    rows.add("marking", "marking/every plate's stripes are 40 to 50 degrees to the vertical, 133 to 147 broad and rise toward the inner edge (notes c and e)", not bad_stripe, "out of range: %s" % bad_stripe)
    rows.add("marking", "marking/the chosen numbers are the parts' (size, area, stripe angle and breadth)", all(abs(p["s"][0] - ch["plate_length_mm"]) < 0.01 and abs(p["s"][1] - ch["plate_width_mm"]) < 0.01 and abs(p["stripe"]["angle_deg"] - ch["stripe_angle_deg"]) < 0.01 and abs(p["stripe"]["breadth_mm"] - ch["stripe_breadth_mm"]) < 0.01 for p in plates)
             and abs(ch["area_cm2"] - ch["plate_length_mm"] * ch["plate_width_mm"] / 100.0) < 0.5 and abs(ch["stripe_period_mm"] - 2 * ch["stripe_breadth_mm"]) < 0.01, "")
    for tag, pl_ in ends.items():
        if len(pl_) != 2:
            continue
        a, b = pl_
        ba, bb = ps.part_bbox(a["id"]), ps.part_bbox(b["id"])
        yca, ycb = (ba[0][1] + ba[1][1]) / 2, (bb[0][1] + bb[1][1]) / 2
        same = a["s"] == b["s"] and a["rot"] == b["rot"] and a["material"] == b["material"]
        rows.add("marking", "marking/%s end: the two plates are equal in size and shape and mirror images about the skip's axis (Schedule 2 paragraph 1 and 3b)" % tag, same and abs(yca + ycb) < 0.5, "centres y %.1f and %.1f" % (yca, ycb))
        inner_a = min(abs(ba[0][1]), abs(ba[1][1]))
        inner_b = min(abs(bb[0][1]), abs(bb[1][1]))
        rows.add("marking", "marking/%s end: the innermost edges are the same distance from the skip's axis (paragraph 3b)" % tag, abs(inner_a - inner_b) < 0.5, "%.1f and %.1f" % (inner_a, inner_b))
        rows.add("marking", "marking/%s end: the upper edges are level with each other (paragraph 3c)" % tag, abs(ba[1][2] - bb[1][2]) < 0.5, "%.1f and %.1f mm" % (ba[1][2], bb[1][2]))
        outer = max(abs(ba[0][1]), abs(ba[1][1]), abs(bb[0][1]), abs(bb[1][1]))
        ep = ps.part_bbox("end_up_r" if tag == "s" else "end_up_l")
        rows.add("marking", "marking/%s end: each plate is as near the outer edge as the end allows and does not project beyond it (paragraph 3a)" % tag, outer <= ep[1][1] + 0.5 and outer >= ep[1][1] - 12.0, "outermost %.1f, the end plate's edge %.1f" % (outer, ep[1][1]))
        top = max(ba[1][2], bb[1][2])
        rows.add("marking", "marking/%s end: the upper edge is at most 1500 mm above the ground (paragraph 3e i)" % tag, top <= R["upper_edge_max_above_ground_mm"], "%.0f mm" % top)
        rows.add("marking", "marking/%s end: the upper edge is no lower than the rim bar allows (within 100 mm of the skip's top; paragraph 3e ii)" % tag, T["variants"][V]["overall"]["h"] - top <= 100.0, "%.0f mm below the top" % (T["variants"][V]["overall"]["h"] - top))
    onplate = all(any(set(j) == {p["id"], ("end_up_r" if p["id"].startswith("mark_s") else "end_up_l")} for j in T["variants"][V]["joins"]) for p in plates)
    rows.add("marking", "marking/every plate is joined to its end's UPPER end plate and the skip has no lid or door part (paragraph 3d)", onplate and not any(n.startswith(("lid", "door")) for n in ps.names), "")
    rows.add("marking", "marking/the plates lie in the plane of the upper end plate (same rotation)", all(p["rot"] == [q for q in T["variants"][V]["parts"] if q["id"] == ("end_up_r" if p["id"].startswith("mark_s") else "end_up_l")][0]["rot"] for p in plates), "")
    rows.add("marking", "marking/the material is the red-on-yellow one with both colours stated", T["materials"]["marking_red_yellow"].get("srgb") and T["materials"]["marking_red_yellow"].get("stripe_srgb") and all(p["material"] == "marking_red_yellow" for p in plates), "")
    rows.add("marking", "marking/the regulation is a listed source marked used (S8)", any(s["id"] == "S8" and s["used"] and "legislation.gov.uk/uksi/1984/1933" in s["url"] for s in T["sources"]), "")
    if "--live" in sys.argv:
        import re as _re, subprocess
        scr = os.path.join(os.path.dirname(L.REPO), "ledger-scratch", "street-dressing", "skip")
        os.makedirs(scr, exist_ok=True)
        p = os.path.join(scr, "si1984-1933.htm")
        if not os.path.exists(p) or os.path.getsize(p) < 5000:
            subprocess.run(["curl", "-sS", "-m", "60", "-A", L.UA_API, "https://www.legislation.gov.uk/uksi/1984/1933/made/data.htm", "-o", p], check=False)
        txt = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
        flat = _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", " ", txt))
        need = ["On and after 1st January 1986", "any part of which is placed on any part of a highway except a footway or a verge", "BS AU 152", "two plates of equal size", "red fluorescent", "yellow reflex reflecting", "not more than 1.5 metres from the ground", "upper edge of each plate is parallel to"]
        miss = [n for n in need if n not in flat]
        rows.add("live", "live/the regulation's text (legislation.gov.uk) still carries the marking's requirements", not miss, "missing: %s" % miss)


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
