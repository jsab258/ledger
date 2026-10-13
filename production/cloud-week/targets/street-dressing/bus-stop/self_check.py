"""bus-stop: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF
import sd_place as PL

V = "BS1"


def times(spec):
    if not spec:
        return []
    t = (spec["first"] // 100) * 60 + spec["first"] % 100
    end = (spec["last"] // 100) * 60 + spec["last"] % 100
    out = []
    while t <= end:
        out.append(t)
        t += spec["every"]
    return out


def atlas_names():
    a = json.load(open(os.path.join(L.REPO, "production", "art", "atlas-01", "data", "atlas.json")))
    names = set()
    for r in a["routes"]:
        names.add(re.sub(r"\s*\(.*?\)", "", r["name"]).strip().lower())
    for l in a["landmarks"]:
        names.add(l["name"].strip().lower())
    for p in a["working_town"]["places"]:
        names.add(p["name"].strip().lower())
    return names


def card_lines(T):
    n = 3  # operator, stop, rule line
    for s in T["text"]["services"]:
        n += 1 + len(s["stops"]) + 3
    return n


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    names = atlas_names()
    tx = T["text"]
    for s in tx["services"]:
        for key in ("mf", "sat", "sun"):
            sp = s[key]
            if not sp:
                continue
            ts = times(sp)
            ok = ts[-1] == (sp["last"] // 100) * 60 + sp["last"] % 100 and len(ts) >= 2 and ts[0] >= 6 * 60 and ts[-1] <= 23 * 60
            rows.add("timetable", "timetable/service %s %s: first plus whole intervals reaches the last" % (s["no"], key), ok, "%d departures from %d to %d min, every %d" % (len(ts), ts[0], ts[-1], sp["every"]))
        offs = [m for n, m in s["stops"]]
        rows.add("timetable", "timetable/service %s: minutes from the stop rise" % s["no"], offs[0] == 0 and all(b > a for a, b in zip(offs, offs[1:])), str(offs))
        bad = [n for n, m in s["stops"][1:] if n.strip().lower() not in names]
        rows.add("timetable", "timetable/service %s: every stop is a road or place on the town's map" % s["no"], not bad, "not on the map: %s" % bad)
    rows.add("timetable", "timetable/the first stop is this stop", all(s["stops"][0][0].lower() == tx["stop_name"].lower().replace(" (top)", " (top)") for s in tx["services"]), tx["stop_name"])
    rows.add("timetable", "timetable/services numbered differently", len({s["no"] for s in tx["services"]}) == len(tx["services"]), "")
    # the card's capacity and place
    c = tx["card"]
    need = card_lines(T) * c["line_pitch_mm"] + c["head_mm"] * 2 + len(tx["services"]) * c["service_no_mm"]
    rows.at_most("card", "card/its lines fit the card's height", need, c["h"] - 2 * c["margin"])
    cl, ch = ps.part_bbox("case_card")
    gl, gh = ps.part_bbox("case_glass")
    rows.add("card", "card/the card lies inside the window", cl[0] >= gl[0] and ch[0] <= gh[0] and cl[2] >= gl[2] and ch[2] <= gh[2], "card %s to %s window %s to %s" % (cl, ch, gl, gh))
    rows.near("card", "card/the card's size is the text's", ch[0] - cl[0], c["w"], 0.6)
    rows.near("card", "card/the card's height is the text's", ch[2] - cl[2], c["h"], 0.6)
    # placement
    pl = T["placement"]
    hc = json.load(open(os.path.join(L.REPO, "production", "specs", "hook-cast.json")))["places"]["bus_stop"]
    rows.near("placement", "placement/x is the cast's bus stop", pl["x_m"], hc["x_m"], 0.001, unit="m")
    rows.add("placement", "placement/the waiting spot lies behind the pole on the pavement", pl["frontage_z_m"] < pl["z_wait_m"] < pl["z_m"] and abs(pl["z_wait_m"] - hc["z_m"]) < 0.001, "")
    clear = pl["footway_mm"] - pl["set_back_mm"] - ps.part_bbox("pole_foot")[1][0]
    rows.at_least("placement", "placement/footway clear behind the pole", clear, pl["min_clear_behind_mm"])
    rows.near("placement", "placement/z is the kerb's back edge less the set-back", abs(pl["z_m"] - pl["kerb_back_z_m"]) * 1000.0, pl["set_back_mm"], 0.5)
    lb = json.load(open(os.path.join(HERE, "..", "..", pl["bin_slot"]["file"], "target.json")))
    b3 = [b for b in lb["placements"]["bins"] if b["id"] == pl["bin_slot"]["slot"]][0]
    d = ((pl["x_m"] - b3["axis_x_m"]) ** 2 + (pl["z_m"] - b3["axis_z_m"]) ** 2) ** 0.5
    rows.at_most("placement", "placement/the bin is within 3 m of the pole", d, pl["bin_slot"]["max_m"], unit="m")
    # the case and the pole
    pb = ps.part_bbox("pole_foot")
    cb = ps.part_bbox("case_bar_top")
    rows.add("detail", "detail/the case is clamped to the white length of the pole", ps.part_bbox("pole_white")[0][2] < cb[0][2] and ps.part_bbox("pole_white")[1][2] > ps.part_bbox("case_bar_top")[1][2], "")
    fb = ps.part_bbox("flag_plate")
    rows.add("detail", "detail/the flag is on the black upper length", fb[0][2] >= ps.part_bbox("pole_upper")[0][2] - 1 and fb[1][2] <= ps.part_bbox("pole_upper")[1][2] + 1, "")
    rows.add("detail", "detail/the flag and the case face the same way (-y)", fb[0][1] < pb[0][1] and cb[0][1] < pb[0][1], "")
    rows.add("detail", "detail/the flag text is two lines BUS and STOP", T["text"]["flag_text"] == ["BUS", "STOP"], str(T["text"]["flag_text"]))
    rows.add("detail", "detail/BS2 has no case", not any(n.startswith("case_") for n in K._ps_cache(T["variants"]["BS2"]["parts"]).names), "")
    rows.add("detail", "detail/the card has no logo", "no operator logo" in T["text"]["no_logo"], "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    # the earlier script's flag and case really are different from this target
    scr = os.path.join(L.REPO, "tools", "meshgen", "blender", "clutter", "bus_stop.py")
    txt = open(scr).read()
    m = re.search(r"FW, FH, FT = ([0-9.]+), ([0-9.]+), ([0-9.]+)", txt)
    old_w, old_h = float(m.group(1)) * 1000, float(m.group(2)) * 1000
    rows.add("reuse", "reuse/the old script's flag (450 x 375) is not the target's plate", abs(old_w - (fb[1][0] - fb[0][0])) > 100, "old %.0f x %.0f, target %.0f x %.0f" % (old_w, old_h, fb[1][0] - fb[0][0], fb[1][2] - fb[0][2]))
    mp = re.search(r"radius=0\.038, depth=([0-9.]+)", txt)
    rows.add("reuse", "reuse/the old pole's 3.0 m is kept and its 76 mm is replaced by P1's 89 mm", mp is not None and abs(float(mp.group(1)) * 1000 - 3000) < 1 and abs(pb[1][0] - pb[0][0] - 89) < 1, "pole %.1f across" % (pb[1][0] - pb[0][0]))
    # the pole against the flag: P1 fixes the RATIO (13.4 px of 45.7), not the size
    pmf = json.load(open(os.path.join(HERE, "photo_measurements.json")))["P1"]["features"]
    pw = [(pmf["pole_r"]["px"] - pmf["pole_l"]["px"]), (pmf["pole_r2"]["px"] - pmf["pole_l2"]["px"])]
    fw = pmf["flag_right"]["px"] - pmf["flag_left"]["px"]
    ratio_photo = sum(pw) / 2.0 / fw
    ratio_target = (pb[1][0] - pb[0][0]) / (fb[1][0] - fb[0][0])
    rows.near("photo", "photo/the pole's width over the flag's width is P1's (13.4 px of 45.7: 0.29 +-0.03)", ratio_target, ratio_photo, 0.03, unit="")
    # the paint bands: the white begins at 2310 and the black ring runs 890 to 1008, directly under the case
    ring = ps.part_bbox("pole_ring")
    rows.near("detail", "detail/the black ring ends at the case's foot (its top is the case bar's lower edge)", ring[1][2], ps.part_bbox("case_bar_bottom")[0][2], 2.0)
    rows.near("detail", "detail/the white length runs 554 to 2310", ps.part_bbox("pole_white")[1][2], 2310.0, 1.0)
    rows.near("detail", "detail/the lower white begins where the foot ends (554)", ps.part_bbox("pole_white")[0][2], ps.part_bbox("pole_foot")[1][2], 1.0)
    # the case's middle bar and the card under it
    mb, mh = ps.part_bbox("case_mid_bar"), ps.part_bbox("case_mid_head_l")
    rows.add("detail", "detail/the case's middle bar is 220 x 15 x 4 at 1590 to 1605, with two 8 mm round heads at x -105 and 105 behind the clear sheet", abs((mb[1][0] - mb[0][0]) - 220.0) < 0.5 and abs((mb[1][2] - mb[0][2]) - 15.0) < 0.5 and abs((mb[1][1] - mb[0][1]) - 4.0) < 0.5 and abs(mb[0][2] - 1590.0) < 0.5
             and abs(ps.part_bbox("case_mid_head_r")[0][0] - 101.0) < 0.5 and abs(mh[1][0] + 101.0) < 0.5 and abs((mh[1][0] - mh[0][0]) - 8.0) < 0.5 and mb[0][1] >= ps.part_bbox("case_glass")[1][1] - 0.5, "bar %s to %s" % (mb[0], mb[1]))
    rows.add("detail", "detail/the card's top edge is just under the middle bar (1502, P1 row 299)", abs(ps.part_bbox("case_card")[1][2] - 1502.0) < 1.0 and ps.part_bbox("case_card")[1][2] < mb[0][2] - 50.0, "card top %.0f, bar bottom %.0f" % (ps.part_bbox("case_card")[1][2], mb[0][2]))
    # the flag's back face: the same border on both faces
    fr = {n: ps.part_bbox(n) for n in ps.names if n.startswith("flag_border_")}
    bk = {n: ps.part_bbox(n) for n in ps.names if n.startswith("flag_back_border_")}
    rows.add("detail", "detail/the flag is double-sided: a back border for each front border, the same size, on the plate's other face", len(fr) == 4 and len(bk) == 4 and all(abs((fr["flag_border_" + k][1][0] - fr["flag_border_" + k][0][0]) - (bk["flag_back_border_" + k][1][0] - bk["flag_back_border_" + k][0][0])) < 0.01 and abs(fr["flag_border_" + k][0][2] - bk["flag_back_border_" + k][0][2]) < 0.01 and bk["flag_back_border_" + k][0][1] > ps.part_bbox("flag_plate")[1][1] - 0.5 and fr["flag_border_" + k][1][1] < ps.part_bbox("flag_plate")[0][1] + 0.5 for k in ("top", "bottom", "left", "right")), "")
    rows.add("detail", "detail/the front assembly meets the pole's front face (the plate's clamps and the case's back sheet reach the pole)", ps.part_bbox("case_back")[1][1] >= -pb[1][0] - 0.5 and ps.part_bbox("flag_clamp_top")[1][1] >= -pb[1][0] - 0.5, "case back at y %.1f, the pole's front at %.1f" % (ps.part_bbox("case_back")[1][1], -pb[1][0]))
    # the slot: the pose; the wording against the scene's blocks
    pose = pl["poses"][0]
    rows.add("placement", "placement/the pose is the stated slot (x, z) and the flag faces -x", abs(pose["x_m"] - pl["x_m"]) < 1e-6 and abs(pose["z_m"] - pl["z_m"]) < 1e-6 and PL.direction_name(PL.front_direction(pose)) == "-x", "")
    blocks = {b["id"]: b for b in json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))["blocks"]}
    wn = blocks["west_north"]
    wn_end = wn["start_x_m"] + wn["bays"] * wn["bay_width_m"]
    rows.add("placement", "placement/the slot's wording matches the scene: the west row ends at x 42, the stop is 4.0 m past it, Rita's is not on this side", abs(wn_end - 42.0) < 1e-6 and abs(pl["x_m"] - wn_end - 4.0) < 1e-6 and "(x 39)" not in " ".join(pl["reasons"]) and "Rita's, the newsagent's" not in " ".join(pl["reasons"]) and "4.0 m past it" in " ".join(pl["reasons"]), "west_north ends at x %.1f" % wn_end)
    rows.add("detail", "detail/the operator's name is a placeholder on its own texture layer, blank in pictures for his page", T["text"]["operator_layer"]["blank_in_pictures_for_his_page"] and T["text"]["operator"].lower() in [p["name"].lower() for p in T["placeholders"]], "")


def extra_controls(T):
    def svc(t, i, key, field, val):
        t["text"]["services"][i][key][field] = val
    C = [
        ("timetable: the last time not on the interval", lambda t: svc(t, 0, "mf", "last", 1755), "timetable/service 4 mf"),
        ("timetable: the stops' minutes not rising", lambda t: t["text"]["services"][1]["stops"].__setitem__(2, ["Retort Works", 3]), "timetable/service 9: minutes from the stop rise"),
        ("timetable: a stop that is not on the town's map", lambda t: t["text"]["services"][2]["stops"].__setitem__(3, ["Leeds Station", 18]), "timetable/service 12: every stop is a road or place"),
        ("timetable: too many services for the card", lambda t: t["text"]["services"].extend([dict(t["text"]["services"][0], no=str(20 + i)) for i in range(6)]), "card/its lines fit"),
        ("card: the card made wider than the window", lambda t: [p.__setitem__("s", [260.0, p["s"][1], p["s"][2]]) for p in t["variants"][V]["parts"] if p["id"] == "case_card"], "card/the card lies inside the window"),
        ("pole: the first version's 76 mm tube (the ratio to the flag drops to 0.25)", lambda t: [p.__setitem__("r0", 38.0) for p in t["variants"][V]["parts"] if p["id"] in ("pole_foot", "pole_white", "pole_upper")], "photo/the pole's width over the flag's width"),
        ("pole: the first version's white length starting at 2118", lambda t: [p["p1"].__setitem__(2, 2118.0) for p in t["variants"][V]["parts"] if p["id"] == "pole_white"], "detail/the white length runs 554 to 2310"),
        ("pole: the black ring dropped to the foot's top (554 to 700)", lambda t: [(p["p0"].__setitem__(2, 554.0), p["p1"].__setitem__(2, 700.0)) for p in t["variants"][V]["parts"] if p["id"] == "pole_ring"], "detail/the black ring ends at the case's foot"),
        ("case: the middle bar removed", lambda t: [K.drop_part(t, V, n) for n in ("case_mid_bar", "case_mid_head_l", "case_mid_head_r")], "detail/the case's middle bar is 220 x 15 x 4"),
        ("case: the card top moved up to 1518 (as the first version had it)", lambda t: K.shift_part(t, V, "case_card", [0, 0, 16.0]), "detail/the card's top edge is just under the middle bar"),
        ("flag: a back border removed (single-sided again)", lambda t: K.drop_part(t, V, "flag_back_border_left"), "detail/the flag is double-sided"),
        ("flag: the front assembly left where the 76 mm pole had it (6.5 mm too far back)", lambda t: [K.shift_part(t, V, n, [0, 6.5, 0]) for n in ("case_back", "flag_clamp_top")], "detail/the front assembly meets the pole's front face"),
        PL.ctl("placement: the flag turned to face the street's far side (yaw 0)", "stop", "place/stop/front faces", yaw_deg=0.0),
        PL.ctl("placement: the pole set in the carriageway (z -2.0)", "stop", "place/stop/feet lie in zone", z_m=-2.0),
        ("placement: the wording put back to 'beyond the west block's end (x 39)'", lambda t: t["placement"]["reasons"].append("the stop is beyond the west block's end (x 39)"), "placement/the slot's wording matches the scene"),
        ("placement: the stop moved to x 30", lambda t: t["placement"].__setitem__("x_m", 30.0), "placement/x is the cast's bus stop"),
        ("placement: the pole 1.2 m behind the kerb", lambda t: (t["placement"].__setitem__("set_back_mm", 1500.0), t["placement"].__setitem__("z_m", -4.625)), "placement/footway clear behind the pole"),
        ("placement: the bin 8 m away", lambda t: t["placement"]["bin_slot"].__setitem__("max_m", 1.0), "placement/the bin is within 3 m"),
        ("detail: the flag text changed", lambda t: t["text"].__setitem__("flag_text", ["BUS", "STOP", "HERE"]), "detail/the flag text"),
        ("detail: a case part added to BS2", lambda t: t["variants"]["BS2"]["parts"].append({"id": "case_bar_x", "type": "box", "c": [0, -60, 1500], "s": [100, 40, 100], "material": "case_green"}), "detail/BS2 has no case"),
        ("photograph: the case 120 mm too high", lambda t: (K.shift_part(t, V, "case_bar_top", [0, 0, 120]), K.shift_part(t, V, "case_bar_left", [0, 0, 120]), K.shift_part(t, V, "case_bar_right", [0, 0, 120])), "photo/P1/case_top"),
        ("photograph: the flag 90 mm too narrow", lambda t: [p.__setitem__("s", [210.0, p["s"][1], p["s"][2]]) for p in t["variants"][V]["parts"] if p["id"] == "flag_plate"], "photo/P1/flag_left"),
        ("numbers: the pole 300 mm too short", lambda t: [(p.__setitem__("p0", [0, 0, p["p0"][2] * 0.9]), p.__setitem__("p1", [0, 0, p["p1"][2] * 0.9])) for p in t["variants"][V]["parts"] if p["id"].startswith("pole_") and p["id"] != "pole_collar"], "numbers/N1"),
    ]
    return C


if __name__ == "__main__":
    spec = dict(V=V, leaf="case_lock", leaf_move=[0, -40, 0], bridge="pole_upper", join=("case_card", "case_glass"), join_move=[0, 30, 0], overlap=("case_bar_top", [0, 40, 0]), photo_squeeze=0.7,
                blocker={"flag plate": "flag_plate"}, number_id="N5")
    sys.exit(1 if SF.selfcheck_main(HERE, "bus-stop", extra, extra_controls, spec) else 0)
