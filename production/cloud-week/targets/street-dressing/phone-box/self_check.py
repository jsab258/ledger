"""phone-box: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]
Offline: every row is derived from target.json's parts and text. --live re-reads the Geograph pages and re-measures the
photograph's edges from its pixels. --previews checks the preview files."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_place as PL

V = "KX1"


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    lo, hi = ps.bbox(only=[n for n in ps.names if n != "f_pull"])
    depth = hi[1] - lo[1]
    pl = T["placement"]
    pose = pl["poses"][0]
    # the slot from the pose and the built parts (not from the target's own sentence)
    prisms, base = PL.object_prisms(T, pose)
    body = [q for q in prisms if q.part != "f_pull"]
    from shapely.ops import unary_union
    b = unary_union([q.poly for q in body]).bounds        # x0, z0, x1, z1 of the box without the pull
    full = unary_union([q.poly for q in prisms]).bounds
    rows.near("placement", "placement/the box's faces fall where the target states (z)", b[1], pl["kiosk_face_z_m"][0], 0.002, unit="m")
    rows.near("placement", "placement/the box's far face falls where the target states (z)", b[3], pl["kiosk_face_z_m"][1], 0.002, unit="m")
    rows.near("placement", "placement/the box is 890 deep on the street's z", (b[3] - b[1]) * 1000.0, depth, 1.5)
    rows.near("placement", "placement/clear strip behind the door is derived from the parts and the stallriser line", (pl["stallriser_line_z_m"] - b[3]) * 1000.0, pl["clear_strip_mm"], 1.0)
    rows.near("placement", "placement/105 mm remain between the kerb's back edge and the box's road face", (b[1] - pl["kerb_back_z_m"]) * 1000.0, pl["to_kerb_back_edge_mm"], 1.0)
    rows.near("placement", "placement/the strip at the pull is stated", (pl["stallriser_line_z_m"] - full[3]) * 1000.0, pl["clear_strip_at_pull_mm"], 1.0)
    rows.at_least("placement", "placement/the strip is at least a walking person", (pl["stallriser_line_z_m"] - full[3]) * 1000.0, pl["min_clear_mm"])
    # C9: the place
    rows.add("placement", "placement/C9 the kiosk stands at x 16.5 +-0.05, centre z 3.675 +-0.05, door to +z",
             abs(pose["x_m"] - 16.5) <= 0.05 and abs(pose["z_m"] - 3.675) <= 0.05 and PL.direction_name(PL.front_direction(pose)) == "+z" and
             abs(0.5 * (b[0] + b[2]) - 16.5) <= 0.05 and abs(0.5 * (b[1] + b[3]) - 3.675) <= 0.05,
             "pose x %.3f z %.3f, yaw %.0f, front to %s; the built box's centre x %.3f z %.3f" % (pose["x_m"], pose["z_m"], pose["yaw_deg"], PL.direction_name(PL.front_direction(pose)), 0.5 * (b[0] + b[2]), 0.5 * (b[1] + b[3])))
    rows.add("placement", "placement/the target's checks list C9", any(c["name"].startswith("C9") for c in T["checks"]), "")
    rows.add("placement", "placement/no move is put to Jafar (no owed line asks for one)", not any(("move" in o["line"].lower() or "23.5" in o["line"]) for o in T["owed"]) and all(o["id"] != "O2" for o in T["owed"]), "owed: %s" % [o["id"] for o in T["owed"]])
    # the town's own place for the kiosk lies beyond the door, outside the box, inside the strip
    hc = os.path.join(L.REPO, pl["town_place"]["file"])
    if os.path.exists(hc):
        pk = json.load(open(hc))["places"][pl["town_place"]["place"]]
        inside = full[0] <= pk["x_m"] <= full[2] and full[1] <= pk["z_m"] <= full[3]
        rows.add("placement", "placement/the town's kiosk place (hook-cast places.kiosk) is outside the box", not inside and abs(pk["x_m"] - pl["town_place"]["x_m"]) < 0.01 and abs(pk["z_m"] - pl["town_place"]["z_m"]) < 0.01,
                 "place (%.2f, %.2f); the box with its pull spans x %.3f to %.3f, z %.3f to %.3f" % (pk["x_m"], pk["z_m"], full[0], full[2], full[1], full[3]))
        rows.add("placement", "placement/the place lies beyond the door and inside the strip, 0.10 m or more clear of the pull", pk["z_m"] - full[3] >= 0.10 and pk["z_m"] < pl["stallriser_line_z_m"] - 0.3 and abs(pk["x_m"] - 0.5 * (b[0] + b[2])) <= 0.5,
                 "%.0f mm beyond the pull, %.0f mm from the stallriser line" % ((pk["z_m"] - full[3]) * 1000, (pl["stallriser_line_z_m"] - pk["z_m"]) * 1000))
    else:
        rows.add("placement", "placement/hook-cast.json is present", False, hc)
    # the pull stands 28 proud of the band, the band 10 proud of the frame, three hinges
    pull_lo, _ = ps.part_bbox("f_pull")
    band_lo, _ = ps.part_bbox("f_band")
    stile_lo, _ = ps.part_bbox("f_stile_l")
    rows.near("detail", "detail/the pull stands 28 mm out of the band", band_lo[1] - pull_lo[1], 28.0, 3.0)
    rows.near("detail", "detail/the band stands 10 mm out of the frame", stile_lo[1] - band_lo[1], 10.0, 2.0)
    rows.near("detail", "detail/three hinges on the right post", ps.names.__len__() and len([n for n in ps.names if n.startswith("f_hinge")]), 3, 0.1, unit="")
    # the glass lies inside its frame, in the stated places
    gl, gh = ps.part_bbox("f_glass_up")
    zl = T["text"]["logo_zone"]
    rows.add("detail", "detail/the logo zone lies on the upper front pane and holds no part",
             zl[0] >= gl[0] and zl[1] <= gh[0] and zl[2] >= gl[2] and zl[3] <= gh[2] and not any(
                 p["id"].startswith("f_") and p["id"] not in ("f_glass_up",) and ps.part_bbox(p["id"])[0][2] < zl[3] and ps.part_bbox(p["id"])[1][2] > zl[2] and ps.part_bbox(p["id"])[0][0] < zl[1] and ps.part_bbox(p["id"])[1][0] > zl[0]
                 for p in T["variants"][V]["parts"] if p["id"] not in ("f_stile_l", "f_stile_r", "f_hinge1", "f_hinge2", "f_hinge3")), "")
    rows.add("detail", "detail/the header word is the plain word and nothing else", T["text"]["header_word"] == "Telephone", T["text"]["header_word"])
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/only glass is transparent", all((p.get("material") == "glass") == bool(p.get("transparent")) for v in T["variants"].values() for p in v["parts"]), "")
    # the doorless variant has the same lid, posts, back and payphone as the door variant, and no leaf
    ps2 = K._ps_cache(T["variants"]["KX2"]["parts"])
    same = all(n in ps2.names for n in ("lid_top", "p_fl", "back_panel", "pp_body", "f_header"))
    leafless = not any(n.startswith(("f_glass", "f_stile", "f_band", "f_hinge", "f_pull", "f_rail")) for n in ps2.names)
    rows.add("detail", "detail/KX2 keeps the shell and drops the leaf", same and leafless, "")
    # the earlier script's numbers really are the ones the target says it replaces
    scr = os.path.join(L.REPO, "tools", "meshgen", "blender", "clutter", "kx100_kiosk.py")
    if os.path.exists(scr):
        txt = open(scr).read()
        H0 = float(re.search(r"^H = ([0-9.]+)", txt, re.M).group(1)) * 1000
        band = re.search(r'panel\("band", ([0-9.]+), ([0-9.]+)', txt)
        zc, hh = float(band.group(1)), float(band.group(2))
        old_b0, old_b1 = (zc - hh / 2) * 1000, (zc + hh / 2) * 1000
        n_b0 = ps.part_bbox("f_band")[0][2]
        rows.add("reuse", "reuse/the old script's band (1.00 to 1.12 m) is not the target's", abs((old_b0 + old_b1) / 2 - (n_b0 + ps.part_bbox("f_band")[1][2]) / 2) > 20, "old %.0f to %.0f, target %.0f to %.0f" % (old_b0, old_b1, n_b0, ps.part_bbox("f_band")[1][2]))
        rows.add("reuse", "reuse/the old script's height (2.18 m) differs from the printed 2192", abs(H0 - hi[2]) > 5, "old %.0f, target %.0f" % (H0, hi[2]))
    else:
        rows.add("reuse", "reuse/the old script is present", False, scr)
    sc_path = os.path.join(L.REPO, "production", "specs", "vignette-scene.json")
    if os.path.exists(sc_path):
        sc = json.load(open(sc_path))
        e3 = [f for f in sc["furniture"] if f.get("bom") == "E3_telephone_kiosk"][0]
        rows.add("reuse", "reuse/the scene's kiosk is the older proportions (plan 0.914, height 2.515)", abs(e3["plan_m"] * 1000 - 914) < 1 and abs(e3["height_m"] * 1000 - 2515) < 1, str((e3["plan_m"], e3["height_m"])))
        # the scene's set-back is to the kiosk's CENTRE: its own plinth faces leave more than a walking person behind
        pz = [p for p in json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-pieces.json")))["pieces"] if p["name"] == "kiosk_plinth"][0]
        face = pz["z_m"] + pz["sz_m"] / 2.0
        rows.add("placement", "placement/the scene's 0.55 m set-back is to the centre: its plinth leaves 0.68 m or more behind it", (pl["stallriser_line_z_m"] - face) >= 0.68 and abs(pz["z_m"] - (pl["kerb_back_z_m"] + e3["setback_from_kerb_m"])) < 0.005,
                 "plinth centre z %.3f = kerb back %.3f + set-back %.2f; far face %.3f; %.0f mm behind it" % (pz["z_m"], pl["kerb_back_z_m"], e3["setback_from_kerb_m"], face, (pl["stallriser_line_z_m"] - face) * 1000))
        rows.add("placement", "placement/the pose's x is the scene's x (the slot is kept)", abs(e3["x_m"] - pose["x_m"]) < 0.01 and abs(pz["z_m"] - pose["z_m"]) < 0.01, "scene x %.2f z %.3f, pose x %.2f z %.3f" % (e3["x_m"], pz["z_m"], pose["x_m"], pose["z_m"]))


def extra_controls(T):
    def ch(t, key, val):
        t["placement"][key] = val

    old_slot = dict(x_m=23.5, z_m=4.53, yaw_deg=0.0)   # the first version's slot: x 23.5, the door to the road

    def second_o1(t):
        t["owed"].append({"id": "O1b", "line": "Move the phone box from before Rita's window to before the empty unit, 7 m up the street (east x 23.5)?", "recommended": "Yes, move it"})
    C = [
        PL.ctl("placement: the first version's slot (x 23.5) lies under the empty unit's awning and against its wall", "kiosk", "place/kiosk/clear of every street piece", **old_slot),
        PL.ctl("placement: the first version's slot (x 23.5) stands across the empty unit's shop door", "kiosk", "place/kiosk/clear of every shop and house door zone", **old_slot),
        PL.ctl("placement: the first version's slot (x 23.5) leaves under 0.68 m under the awning's valance", "kiosk", "place/kiosk/walking strip", **old_slot),
        PL.ctl("placement: the first version's slot (x 23.5) leaves under 0.68 m at head height", "kiosk", "place/kiosk/head-height strip", **old_slot),
        PL.ctl("placement: the door turned to the road again (yaw 0)", "kiosk", "place/kiosk/front faces", yaw_deg=0.0),
        PL.ctl("placement: the box set in the carriageway (z 2.0)", "kiosk", "place/kiosk/feet lie in zone", z_m=2.0),
        PL.ctl("placement: the box moved 0.5 m along the street (C9 asks x 16.5 +-0.05)", "kiosk", "placement/C9", x_m=17.0),
        PL.ctl_copies_across("placement: a fence of copies across the footway leaves no walking strip", "kiosk", "place/kiosk/walking strip"),
        ("placement: the clear strip stated as the first version's 960", lambda t: t["placement"].__setitem__("clear_strip_mm", 960.0), "placement/clear strip behind the door is derived"),
        ("placement: the old wrong 0.56 m reason put back as the strip", lambda t: t["placement"].__setitem__("clear_strip_at_pull_mm", 560.0), "placement/the strip at the pull is stated"),
        ("placement: the town's kiosk place moved into the box (z 4.1)", lambda t: t["placement"]["town_place"].__setitem__("z_m", 4.1), "placement/the town's kiosk place"),
        ("owed: the move put to Jafar again", second_o1, "placement/no move is put to Jafar"),
        ("detail: the pull only 10 mm out", lambda t: K.shift_part(t, V, "f_pull", [0, 18, 0]), "detail/the pull stands 28 mm"),
        ("detail: a hinge removed", lambda t: K.drop_part(t, V, "f_hinge3"), "detail/three hinges"),
        ("detail: the header word changed", lambda t: t["text"].__setitem__("header_word", "Telephone Kiosk"), "detail/the header word"),
        ("detail: a logo part put in the logo zone", lambda t: t["variants"][V]["parts"].append({"id": "f_logo", "type": "box", "c": [0, -430, 1400], "s": [200, 4, 200], "material": "handle_yellow"}), "detail/the logo zone"),
        ("detail: a material missing", lambda t: t["variants"][V]["parts"][0].__setitem__("material", "chrome"), "detail/every part's material"),
        ("detail: the doorless variant given a glass pane", lambda t: t["variants"]["KX2"]["parts"].append({"id": "f_glass_x", "type": "box", "c": [0, -430, 1400], "s": [600, 4, 600], "material": "glass", "transparent": True}), "detail/KX2 keeps the shell"),
        ("photograph: the handle band moved 40 mm up", lambda t: K.shift_part(t, V, "f_band", [0, 0, 40]), "photo/P1/band_top"),
        ("photograph: the header 60 mm too low", lambda t: K.shift_part(t, V, "f_header", [0, 0, -60]), "photo/P1/header_bottom"),
        ("photograph: the glazing 60 mm too narrow", lambda t: (K.shift_part(t, V, "f_stile_l", [60, 0, 0]), K.shift_part(t, V, "f_stile_r", [-60, 0, 0])), "photo/P1/glass_l"),
        ("photograph: the posts 30 mm too thick", lambda t: [p.__setitem__("s", [70.0, p["s"][1], p["s"][2]]) for p in t["variants"][V]["parts"] if p["id"] in ("p_fl",)], "photo/P1/frame_l_outer"),
        ("numbers: the lid skirt 40 mm deeper", lambda t: [p.__setitem__("s", [p["s"][0], p["s"][1], p["s"][2] + 40]) for p in t["variants"][V]["parts"] if p["id"] == "lid_skirt_front"], "numbers/N4"),
    ]
    return C


if __name__ == "__main__":
    spec = dict(V=V, leaf="pp_keypad", bridge="back_panel", join=("f_pull", "f_band"), join_move=[0, 0, 200], overlap=("f_hinge2", [-30, 0, 0]),
                blocker={"back": "back_panel", "roof": "lid_top", "header front": "f_header", "handle band": "f_band", "left side header": "sl_header"}, number_id="N6")
    sys.exit(1 if K.main("phone-box", HERE, extra=extra, extra_controls=extra_controls, ctl_spec=spec) else 0)
