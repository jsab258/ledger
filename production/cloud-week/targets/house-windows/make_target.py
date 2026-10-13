#!/usr/bin/env python3
"""Assembles target.json for the house windows (cloud week 42, unit 8) from hw_data.py, hw_rooms.py, what terrace-front.py draws (hw_sites.py),
the lab's checked sash (production/art/sash-window/target.json and the two .glb), the game's projection rule (hw_common.py) and the photograph
measurements (hw_measure.py, needs the photographs: --photos DIR, fetched when missing).  usage: make_target.py [--photos DIR]
Run with /home/user/.bpyenv/bin/python."""
import argparse
import json
import math
import os
import struct
import sys
import zlib

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import hw_common as H
import hw_data as D
import hw_rooms as R
import hw_sites
import hw_photos as P
import hw_measure as M
import hw_checks as CK

ROOT = H.ROOT
LAB_TARGET = os.path.join(ROOT, "production", "art", "sash-window", "target.json")
LAB_GLB = {"S22": os.path.join(ROOT, "production", "assets", "sash-window", "sash_window.glb"),
           "S11": os.path.join(ROOT, "production", "assets", "sash-window", "sash_window_1over1.glb")}


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin3(rgb):
    return [round(srgb_to_lin(v), 4) for v in rgb]


# ---- the glb of the checked sash: nodes with bounds in the KIT frame (mm): x across, y into the wall (= -z of the glTF), z up (= y of the glTF)
def glb_nodes(path):
    data = open(path, "rb").read()
    magic, ver, length = struct.unpack("<III", data[:12])
    off = 12
    js = None
    binchunk = None
    while off < length:
        cl, ct = struct.unpack("<II", data[off:off + 8])
        chunk = data[off + 8:off + 8 + cl]
        if ct == 0x4E4F534A:
            js = json.loads(chunk)
        elif ct == 0x004E4942:
            binchunk = chunk
        off += 8 + cl
    nodes = []
    tris = 0
    for n in js["nodes"]:
        m = js["meshes"][n["mesh"]]
        p = m["primitives"][0]
        acc = js["accessors"][p["attributes"]["POSITION"]]
        mn = [v * 1000.0 for v in acc["min"]]
        mx = [v * 1000.0 for v in acc["max"]]
        t = js["accessors"][p["indices"]]["count"] // 3 if "indices" in p else 0
        tris += t
        nodes.append({"name": n["name"], "material": js["materials"][p["material"]]["name"] if "material" in p else None,
                      "x": [round(mn[0], 1), round(mx[0], 1)], "y_into_wall": [round(-mx[2], 1), round(-mn[2], 1)], "z_up": [round(mn[1], 1), round(mx[1], 1)],
                      "triangles": t, "vertex_colour": "COLOR_0" in p["attributes"]})
    return nodes, tris, os.path.getsize(path)


# ---- the street's window sites and what each gets
SITE_PLAN = {
    # (block, bay, index): room, net, extra, paint, condition, always_lit
    ("east_parade", 0, 0): dict(room="up_landing_1", net=("N2", "greyed"), extra=None, paint="white_grimy", cond="grimy"),
    ("east_parade", 0, 1): dict(room="up_lounge_1", net=("N1", "white"), extra=("C2", "cream"), paint="white_grimy", cond="grimy"),
    ("east_parade", 1, 0): dict(room="up_landing_2", net=("N0", None), extra=("B2", "cream"), paint="white_fresh", cond="sound"),
    ("east_parade", 1, 1): dict(room="up_bedroom_1", net=("N1", "white"), extra=("C2", "brown"), paint="white_fresh", cond="sound"),
    ("east_parade", 2, 0): dict(room="up_lounge_2", net=("N1", "greyed"), extra=("C2", "green"), paint="white_upvc", cond="sound"),
    ("east_parade", 2, 1): dict(room="up_landing_1", net=("N2", "greyed"), extra=None, paint="white_upvc", cond="sound"),
    ("east_parade", 3, 0): dict(room="up_empty_1", net=("N1", "yellowed"), extra=None, paint="white_flaking", cond="flaking", torn_net=True),
    ("east_parade", 3, 1): dict(room="up_empty_2", net=("N0", None), extra=None, paint="white_flaking", cond="flaking"),
    ("east_parade", 4, 0): dict(room="up_bedroom_2", net=("N2", "white"), extra=("C1", "green"), paint="white_upvc", cond="sound"),
    ("east_parade", 4, 1): dict(room="up_landing_2", net=("N1", "yellowed"), extra=None, paint="white_upvc", cond="grimy"),
    ("east_parade", 5, 0): dict(room="up_lounge_3", net=("N1", "white"), extra=("C2", "floral_cream"), paint="white_grimy", cond="sound"),
    ("east_parade", 5, 1): dict(room="up_landing_1", net=("N3", "white"), extra=None, paint="white_grimy", cond="sound"),
    ("east_chandler", 0, 0): dict(room="up_bedroom_3", net=("N0", None), extra=("B1", "white"), paint="white_upvc", cond="sound"),
    ("east_chandler", 0, 1): dict(room="up_landing_2", net=("N2", "yellowed"), extra=None, paint="white_upvc", cond="grimy"),
    ("west_south", 2, 0): dict(room="gf_front_3", net=("N1", "white"), extra=None, paint="white_fresh", cond="sound", always_lit=True),
    ("west_south", 2, 1): dict(room="gf_front_3", net=("N1", "white"), extra=("B3", "white"), paint="white_fresh", cond="sound", always_lit=True),
    ("west_south", 1, 0): dict(room="gf_front_2", net=("N2", "white"), extra=None, paint="white_upvc", cond="sound"),
    ("west_south", 1, 1): dict(room="gf_front_2", net=("N0", None), extra=("C1", "brown"), paint="white_upvc", cond="sound"),
    ("west_south", 0, 0): dict(room="gf_front_1", net=("N1", "white"), extra=None, paint="white_grimy", cond="grimy"),
    ("west_south", 0, 1): dict(room="gf_front_1", net=("N1", "white"), extra=None, paint="white_grimy", cond="grimy"),
}
KIND_OF_PAINT_OK = {"S22": ("white_fresh", "white_grimy", "white_flaking", "cream", "olive", "blue", "brown"), "S11": ("white_fresh", "white_grimy", "white_flaking", "cream", "olive", "blue", "brown"),
                    "RC": ("white_upvc", "bronze"), "RC2": ("white_upvc", "bronze")}
# the houses that take the P6 replacement form (RC2) instead of P7's (RC); every other replacement house keeps RC
RC2_HOUSES = {("east_parade", 4)}
# a house's frame paint follows the kind: the street's _window_kind(house) decides the kind; a replacement cannot be painted blue or olive
KIND_NAME = {"2/2": "S22", "1/1": "S11", "replacement": "RC"}


def site_id(blk, bay, floor, i):
    return "%s_bay%d_%s_w%d" % (blk, bay, floor, i)


def cottage_card_cx(sites_of_house):
    return round(sum(s["x_centre"] for s in sites_of_house) / len(sites_of_house), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "hw_photos"))
    a = ap.parse_args()
    lab = json.load(open(LAB_TARGET))
    derived, tf = hw_sites.derive()

    # ---------- sites ------------------------------------------------------------------------------------------------------
    sites = []
    for s in derived:
        blk, bay, floor, idx = s["block"], s["bay"], s["floor"], s["index"]
        key = (blk, bay, idx)
        plan = SITE_PLAN[key]
        file_kind = tf._window_kind(blk, bay)
        kind = KIND_NAME[file_kind]
        if kind == "RC" and (blk, bay) in RC2_HOUSES:
            kind = "RC2"
        side = 1 if blk.startswith("east") else -1
        cx = round((s["x_min"] + s["x_max"]) / 2.0, 3)
        built_as = ("S22 kit" if s["kit_nodes"] and kind == "S22" else "S11 kit" if s["kit_nodes"] else
                    "box replacement (frame_bronze)" if "frame_bronze" in s["materials"] else "box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind)")
        head_z = round(s["z_max"] if floor == "gf" else 5.9, 4)
        if floor == "upper":
            head_z, sill_old = 5.9, round(5.9 - 1.5, 4)
        else:
            head_z = 2.5
        sill_z = round(head_z - 0.016764 * 100, 4) if False else round(head_z - H.WIN_H_PERIOD, 4)
        fam = "UP" if floor == "upper" else "GF"
        room = H.ROOMS[fam]
        paint = plan["paint"]
        assert paint in KIND_OF_PAINT_OK[kind], (key, kind, paint)
        sites.append({
            "id": site_id(blk, bay, floor, idx), "block": blk, "bay": bay, "floor": floor, "index": idx, "side": side, "x_centre": cx,
            "opening_w_mm": 850.0, "opening_h_mm": H.WIN_H_PERIOD * 1000.0, "head_z_above_crown": head_z, "sill_z_above_crown": sill_z,
            "kind_by_house_in_terrace_front": file_kind, "kind": kind, "built_as_today": built_as, "kit_row_today": bool(s["kit_nodes"]),
            "opening_today": {"z_min": s["z_min"], "z_max": s["z_max"]},
            "room": plan["room"], "family": fam, "paint": paint, "condition": plan["cond"],
            "net": {"kind": plan["net"][0], "colour": plan["net"][1], "torn": bool(plan.get("torn_net"))},
            "extra": ({"kind": plan["extra"][0], "colour": plan["extra"][1]} if plan["extra"] else None),
            "always_lit": bool(plan.get("always_lit")),
        })
    # house groups (cottages share a room card between their two windows)
    for s in sites:
        s["house"] = "%s_bay%d" % (s["block"], s["bay"])
    houses = {}
    for s in sites:
        houses.setdefault(s["house"], []).append(s)
    # cards
    for s in sites:
        room = H.ROOMS[s["family"]]
        if s["family"] == "GF":
            cx_card = cottage_card_cx(houses[s["house"]])
        else:
            cx_card = s["x_centre"]
        x_low = round(cx_card - room["w"] / 2.0, 3)
        y_card = round(s["side"] * (H.FRONTAGE_Y + H.CARD_Y_BACK), 3)
        win_off_toward_picture_right = (cx_card - s["x_centre"]) if s["side"] > 0 else (s["x_centre"] - cx_card)
        floor_z = room["floor_z"]
        s["card"] = {
            "room_family": s["family"], "w": room["w"], "h": room["h"], "d": room["d"], "camd": room["camd"], "side": s["side"],
            "centre_x": round(cx_card, 3), "x_low": x_low, "y_card_plane": y_card, "z_bottom_above_crown": floor_z, "z_top_above_crown": round(floor_z + room["h"], 3),
            "card_origin_cm": [round(x_low * 100, 1), round(y_card * 100, 1), round(floor_z * 100, 1)],
            "room_size_cm": [round(room["w"] * 100, 1), round(room["h"] * 100, 1), round(room["d"] * 100, 1)], "cam_d_cm": round(room["camd"] * 100, 1),
            "window_in_card_m": {"x0": round(s["x_centre"] - 0.425 - x_low, 3), "x1": round(s["x_centre"] + 0.425 - x_low, 3),
                                 "z0": round(s["sill_z_above_crown"] - floor_z, 4), "z1": round(s["head_z_above_crown"] - floor_z, 4)},
            "window_offset_toward_picture_right_m": round(win_off_toward_picture_right, 3),
            "shared_by": [t["id"] for t in houses[s["house"]]] if s["family"] == "GF" else None,
        }
    # lit order: the fixed list of hw_data.LIT_ORDER (the review's narrow point 6), checked against the eligible windows (not empty, not always-lit)
    elig_ids = sorted(s["id"] for s in sites if not s["room"].startswith("up_empty") and not s["always_lit"])
    assert sorted(D.LIT_ORDER) == elig_ids, (set(D.LIT_ORDER) ^ set(elig_ids))
    by_id = {s["id"]: s for s in sites}
    elig = [by_id[i] for i in D.LIT_ORDER]
    for i, s in enumerate(elig):
        s["lit_order"] = i + 1
    for s in sites:
        s.setdefault("lit_order", 0 if s["always_lit"] else None)
    lit_table = {}
    for hh, share in D.LIT_SHARE["table_hour_to_share_of_all_20_windows"].items():
        n = int(round(share * len(sites)))
        hour = int(hh.split(":")[0]) + int(hh.split(":")[1]) / 60.0
        pair_on = 18.0 <= hour <= 23.0
        k = max(0, n - (2 if pair_on else 0))
        lit = [s["id"] for s in sites if s["always_lit"] and pair_on] + [s["id"] for s in elig[:k]]
        lit_table[hh] = {"n": len(lit), "windows": lit}
    # ---------- the kinds --------------------------------------------------------------------------------------------------
    kinds = {}
    for k in ("S22", "S11"):
        nodes, tris, size = glb_nodes(LAB_GLB[k])
        kinds[k] = {"label": {"S22": "two over two box sash (the lab's checked sash, reused)", "S11": "one over one box sash (the lab's sash with the bars taken out, reused)"}[k],
                    "lab_glb": os.path.relpath(LAB_GLB[k], ROOT), "lab_nodes": nodes, "lab_triangles": tris, "lab_bytes": size,
                    "opening_mm": [850.0, 1676.4], "horns_mm": lab["sash"]["horn_length_mm"], "horns": "ogee horns on the upper sash's stiles (76.2 below the meeting rail), none on the lower",
                    "sections_from_lab_target": {k2: lab["sash"][k2] for k2 in ("stile_width_mm", "top_rail_mm", "bottom_rail_mm", "meeting_rail_depth_mm", "glazing_bar_width_mm", "thickness_mm", "putty", "ovolo_radius_mm", "glass_mm")},
                    "frame_sections_from_lab_target": {k2: lab["frame"][k2] for k2 in ("reveal_mm", "outer_lining_margin_mm", "outer_lining_width_mm", "outer_lining_thickness_mm", "parting_bead_width_mm", "staff_bead_width_mm", "inner_lining_thickness_mm", "inner_lining_width_mm", "head_thickness_mm", "head_visible_mm")},
                    "sill": lab["sill"], "stone_sill": lab["stone_sill"], "bars": ("one vertical bar in each sash (22.2 wide: the lab's amended value; P8 reads 27 +- 4)" if k == "S22" else "none"),
                    "panes": 4 if k == "S22" else 2,
                    "glass_planes_behind_face_mm": {"upper": 142.0, "lower": 190.0}}
    kinds["RC"] = {"label": D.RC["label"], **{k2: v for k2, v in D.RC.items() if k2 != "label"}}
    rc = D.RC
    zc = rc["transom"]["centre_fraction"] * rc["opening"]["h"]
    f = rc["frame_face"]
    t2 = rc["transom"]["face"] / 2.0
    stile = rc["vent_sash"]["stile_face"]
    gap = rc["vent_sash"]["gap"]
    hh = rc["opening"]["h"]
    ww = rc["opening"]["w"]
    kinds["RC"]["parts_mm"] = [
        {"name": "frame_jamb_L", "x": [-ww / 2, -ww / 2 + f], "y_into_wall": [rc["frame_front_y"], rc["frame_front_y"] + rc["frame_depth"]], "z_up": [f, hh - f]},
        {"name": "frame_jamb_R", "x": [ww / 2 - f, ww / 2], "y_into_wall": [rc["frame_front_y"], rc["frame_front_y"] + rc["frame_depth"]], "z_up": [f, hh - f]},
        {"name": "frame_sill_rail", "x": [-ww / 2, ww / 2], "y_into_wall": [rc["frame_front_y"], rc["frame_front_y"] + rc["frame_depth"]], "z_up": [0, f]},
        {"name": "frame_head_rail", "x": [-ww / 2, ww / 2], "y_into_wall": [rc["frame_front_y"], rc["frame_front_y"] + rc["frame_depth"]], "z_up": [hh - f, hh]},
        {"name": "transom", "x": [-ww / 2 + f, ww / 2 - f], "y_into_wall": [rc["frame_front_y"], rc["frame_front_y"] + rc["frame_depth"]], "z_up": [round(zc - t2, 1), round(zc + t2, 1)]},
        {"name": "vent_sash_stile_L", "x": [-ww / 2 + f + gap, -ww / 2 + f + gap + stile], "y_into_wall": [rc["frame_front_y"] + 8, rc["frame_front_y"] + 63], "z_up": [round(zc + t2 + gap, 1), round(hh - f - gap, 1)]},
        {"name": "vent_sash_stile_R", "x": [ww / 2 - f - gap - stile, ww / 2 - f - gap], "y_into_wall": [rc["frame_front_y"] + 8, rc["frame_front_y"] + 63], "z_up": [round(zc + t2 + gap, 1), round(hh - f - gap, 1)]},
        {"name": "vent_sash_bottom_rail", "x": [-ww / 2 + f + gap + stile, ww / 2 - f - gap - stile], "y_into_wall": [rc["frame_front_y"] + 8, rc["frame_front_y"] + 63], "z_up": [round(zc + t2 + gap, 1), round(zc + t2 + gap + stile, 1)]},
        {"name": "vent_sash_top_rail", "x": [-ww / 2 + f + gap + stile, ww / 2 - f - gap - stile], "y_into_wall": [rc["frame_front_y"] + 8, rc["frame_front_y"] + 63], "z_up": [round(hh - f - gap - stile, 1), round(hh - f - gap, 1)]},
        {"name": "glass_lower", "x": [-ww / 2 + f - 18, ww / 2 - f + 18], "y_into_wall": [rc["glass_plane_y"], rc["glass_plane_y"] + 4.0], "z_up": [f - 18, round(zc - t2 + 18, 1)], "material": "glass_house",
         "note": "the sheet: it runs 18 mm behind the frame's face on every side (the rebate); what shows is the sightline x +-365, z 60 to 1172"},
        {"name": "glass_top", "x": [round(-ww / 2 + f + gap + stile - 18, 1), round(ww / 2 - f - gap - stile + 18, 1)], "y_into_wall": [rc["glass_plane_y"], rc["glass_plane_y"] + 4.0],
         "z_up": [round(zc + t2 + gap + stile - 18, 1), round(hh - f - gap - stile + 18, 1)], "material": "glass_house", "note": "the sheet in the top-hung sash: 18 mm behind the sash's face on every side; the sightline is x +-316, z 1291 to 1567.4"},
    ]
    kinds["RC"]["glass_sightlines_mm"] = {"lower": [round(ww - 2 * f, 1), round(zc - t2 - f, 1)],
                                          "top": [round(ww - 2 * (f + gap + stile), 1), round(hh - f - gap - stile - (zc + t2 + gap + stile), 1)]}
    kinds["RC"]["transom_centre_z_mm"] = round(zc, 1)
    # ---- RC2: the P6 form (narrow point 7): a fixed top light over a side-hung casement (left) and a fixed light (right), a 70 mm mullion at x 0
    r2 = D.RC2
    kinds["RC2"] = {"label": r2["label"], **{k2: v for k2, v in r2.items() if k2 != "label"}}
    h2 = r2["opening"]["h"]
    w2 = r2["opening"]["w"]
    f2 = r2["frame_face"]
    y0 = r2["frame_front_y"]
    y1 = y0 + r2["frame_depth"]
    zc2 = round(r2["transom"]["centre_fraction"] * h2, 1)               # 1106.4
    t2b = r2["transom"]["face"] / 2.0
    tz0, tz1 = round(zc2 - t2b, 1), round(zc2 + t2b, 1)                   # 1071.4, 1141.4
    mh = r2["mullion"]["face"] / 2.0
    st2, g2 = r2["casement"]["stile_face"], r2["casement"]["gap"]
    sy0, sy1 = y0 + 8, y0 + 63
    cx0, cx1 = -w2 / 2 + f2 + g2, -mh - g2                                # the casement's outer edges: -361 and -39
    cz0, cz1 = f2 + g2, tz0 - g2                                          # 64 and 1067.4
    kinds["RC2"]["parts_mm"] = [
        {"name": "frame_jamb_L", "x": [-w2 / 2, -w2 / 2 + f2], "y_into_wall": [y0, y1], "z_up": [f2, h2 - f2]},
        {"name": "frame_jamb_R", "x": [w2 / 2 - f2, w2 / 2], "y_into_wall": [y0, y1], "z_up": [f2, h2 - f2]},
        {"name": "frame_sill_rail", "x": [-w2 / 2, w2 / 2], "y_into_wall": [y0, y1], "z_up": [0, f2]},
        {"name": "frame_head_rail", "x": [-w2 / 2, w2 / 2], "y_into_wall": [y0, y1], "z_up": [h2 - f2, h2]},
        {"name": "transom", "x": [-w2 / 2 + f2, w2 / 2 - f2], "y_into_wall": [y0, y1], "z_up": [tz0, tz1]},
        {"name": "mullion", "x": [-mh, mh], "y_into_wall": [y0, y1], "z_up": [f2, tz0]},
        {"name": "casement_stile_L", "x": [cx0, cx0 + st2], "y_into_wall": [sy0, sy1], "z_up": [cz0, cz1], "note": "the hanging stile: the hinge is on the left jamb"},
        {"name": "casement_stile_R", "x": [cx1 - st2, cx1], "y_into_wall": [sy0, sy1], "z_up": [cz0, cz1], "note": "the closing stile, 4 mm from the mullion"},
        {"name": "casement_bottom_rail", "x": [cx0 + st2, cx1 - st2], "y_into_wall": [sy0, sy1], "z_up": [cz0, cz0 + r2["casement"]["rail_face"]]},
        {"name": "casement_top_rail", "x": [cx0 + st2, cx1 - st2], "y_into_wall": [sy0, sy1], "z_up": [round(cz1 - r2["casement"]["rail_face"], 1), cz1]},
        {"name": "glass_casement", "x": [cx0 + st2 - 18, cx1 - st2 + 18], "y_into_wall": [r2["glass_plane_y"], r2["glass_plane_y"] + 4.0], "z_up": [round(cz0 + r2["casement"]["rail_face"] - 18, 1), round(cz1 - r2["casement"]["rail_face"] + 18, 1)],
         "material": "glass_house", "note": "the sheet in the side-hung left light: 18 mm behind the sash's face on every side; the sightline is x %s to %s, z %s to %s" % (cx0 + st2, cx1 - st2, cz0 + r2["casement"]["rail_face"], round(cz1 - r2["casement"]["rail_face"], 1))},
        {"name": "glass_fixed", "x": [mh - 18, w2 / 2 - f2 + 18], "y_into_wall": [r2["glass_plane_y"], r2["glass_plane_y"] + 4.0], "z_up": [f2 - 18, round(tz0 + 18, 1)], "material": "glass_house",
         "note": "the sheet of the fixed right light: 18 mm behind the frame's face on every side (the rebate); the sightline is x %s to %s, z %s to %s" % (mh, w2 / 2 - f2, f2, tz0)},
        {"name": "glass_top", "x": [-w2 / 2 + f2 - 18, w2 / 2 - f2 + 18], "y_into_wall": [r2["glass_plane_y"], r2["glass_plane_y"] + 4.0], "z_up": [round(tz1 - 18, 1), round(h2 - f2 + 18, 1)], "material": "glass_house",
         "note": "the fixed top light across the whole width: the sheet runs 18 mm behind the frame's face; the sightline is x %s to %s, z %s to %s" % (-w2 / 2 + f2, w2 / 2 - f2, tz1, round(h2 - f2, 1))},
    ]
    for p_ in kinds["RC2"]["parts_mm"]:
        for ax in ("x", "y_into_wall", "z_up"):
            p_[ax] = [round(float(v), 1) for v in p_[ax]]
    kinds["RC2"]["glass_sightlines_mm"] = {"casement": [round(cx1 - st2 - (cx0 + st2), 1), round(cz1 - r2["casement"]["rail_face"] - (cz0 + r2["casement"]["rail_face"]), 1)],
                                           "fixed": [round(w2 / 2 - f2 - mh, 1), round(tz0 - f2, 1)], "top": [round(w2 - 2 * f2, 1), round(h2 - f2 - tz1, 1)]}
    kinds["RC2"]["lower_light_openings_mm"] = {"left": [round(-mh - (-w2 / 2 + f2), 1), round(tz0 - f2, 1)], "right": [round(w2 / 2 - f2 - mh, 1), round(tz0 - f2, 1)]}
    kinds["RC2"]["transom_centre_z_mm"] = zc2
    kinds["RC2"]["mullion_z_mm"] = [f2, tz0]
    # ---------- budgets ----------------------------------------------------------------------------------------------------
    # the eye stands by the WINDOW (hw_common.budgets_for: narrow point 1), so each cottage window is run at its own offset in the card
    budgets = {}
    for fam, (sill_above_floor, head_above_floor, offs) in {"UP": (4.2236 - 3.75, 5.9 - 3.75, [0.0]), "GF": (H.WIN_H_PERIOD and (2.5 - H.WIN_H_PERIOD - 0.45), 2.5 - 0.45, [0.9, -0.9])}.items():
        best = None
        for off in offs:
            b, pc = H.budgets_for(fam, sill_above_floor, head_above_floor, off)
            if best is None:
                best = {c: dict(v) for c, v in b.items()}
                best_pc = pc
            else:
                for c in b:
                    for kk in b[c]:
                        if b[c][kk] is not None and (best[c][kk] is None or b[c][kk] < best[c][kk]):
                            best[c][kk] = b[c][kk]
        budgets[fam] = {"surfaces": best, "window_above_floor_m": [round(sill_above_floor, 4), round(head_above_floor, 4)], "window_offsets_m": offs,
                        "method": "eye at the window (xc = card_cx - win_off_x), mirror about the window, one pixel = atan(tan(vfov / 2) / 720) (the review's exact pixel angle)"}
    # what shows of each room from the review cameras (computed through the game's rule's geometry); x is measured from the PICTURE-LEFT WALL (not from the room's centre)
    vz = {}
    names = ["back", "left", "right", "floor", "ceiling"]
    for fam, (sill_above_floor, head_above_floor, off) in {"UP": (4.2236 - 3.75, 5.9 - 3.75, 0.0), "GF": (2.5 - H.WIN_H_PERIOD - 0.45, 2.05, 0.9)}.items():
        room = H.ROOMS[fam]
        rect = H.window_in_picture(room, off, sill_above_floor, head_above_floor)
        vz[fam] = {}
        for cam in H.STAND_OFF_CAMERAS:
            e = H.eye_in_picture(H.eye_street(H.CAMERAS[cam]["spec"], 1, 0.0 - off), 1, 0.0, room)       # the eye by the window: xc = card_cx - win_off_x
            hp, sid, G, Pp = H.see_through(e, rect, room)
            rec = {}
            for i, nm in enumerate(names):
                mk = sid == i
                if mk.any():
                    rec[nm] = {"x": [round(float(hp[mk, 0].min()), 2), round(float(hp[mk, 0].max()), 2)], "y": [round(float(hp[mk, 1].min()), 2), round(float(hp[mk, 1].max()), 2)], "z": [round(float(hp[mk, 2].min()), 2), round(float(hp[mk, 2].max()), 2)]}
            vz[fam][cam] = {"eye_in_picture_frame_m": [round(float(v), 2) for v in e], "rays": int(len(hp)), "surfaces_seen": rec}
    # picture geometry
    pictures = {}
    for fam, room in H.ROOMS.items():
        wpx = room["pic_w"]
        pictures[fam] = {"w_px": wpx, "h_px": int(round(wpx * room["h"] / room["w"])), "back_wall_rect_px_x0y0x1y1": H.back_wall_px(room, wpx),
                         "back_wall_uv": [round(v, 4) for v in H.back_wall_rect_uv(room)]}
    # ---------- the rooms --------------------------------------------------------------------------------------------------
    raw = json.load(open(os.path.join(HERE, "polyhaven_models_checked_raw.json")))
    texraw = json.load(open(os.path.join(HERE, "polyhaven_textures_checked_raw.json")))
    rooms = {}
    used_models = set()
    for rid, r in R.ROOMS.items():
        fam = H.ROOMS[r["family"]]
        objs = []
        for o in r["objects"]:
            m = raw[o["model"]]
            dims = [round(v, 1) for v in m["dims_cm"]]            # the catalogue's x, y, z in millimetres (key name kept from the first read)
            w, d, h = dims[0] / 1000.0, dims[1] / 1000.0, dims[2] / 1000.0
            z0 = o["z0"]
            if o.get("on"):
                sup = raw[o["on"]]["dims_cm"][2] / 1000.0
                z0 = round(sup, 3)
            surf = o["surface"]
            stand = d
            if o.get("on"):
                stand = max(d, raw[o["on"]]["dims_cm"][1] / 1000.0)      # on a piece of furniture: it may stand at the support's front edge
            cls_key = "back" if surf == "back" else "side"
            bt, bl = R.BUDGET[cls_key]["true"], R.BUDGET[cls_key]["tolerated"]
            cls = "true" if stand <= bt else ("tolerated" if stand <= bl else "NOT DRAWN")
            if surf == "back":
                extent = [round(o["x"] - w / 2, 3), round(o["x"] + w / 2, 3)]
                place = {"x_across": extent, "y_back": [round(fam["d"] - d, 3), fam["d"]], "z": [z0, round(z0 + h, 3)]}
            else:
                xw = -fam["w"] / 2.0 if surf == "left" else fam["w"] / 2.0
                place = {"wall": surf, "y_back": [round(o["y"] - w / 2, 3), round(o["y"] + w / 2, 3)], "z": [o["z0"], round(o["z0"] + h, 3)], "x_from_wall": [0.0, round(d, 3)]}
            used_models.add(o["model"])
            objs.append({"model": o["model"], "surface": surf, "dims_mm": dims, "footprint_w_d_h_m": [round(w, 3), round(d, 3), round(h, 3)], "stand_off_m": round(stand, 3), "class": cls,
                         "place": place, "on": o.get("on")})
        rooms[rid] = {"family": r["family"], "type": r["type"], "variant": r["variant"], "walls": r["walls"], "ceiling": r["ceiling"], "floor": r["floor"], "forms": r["forms"],
                      "objects": objs, "pendant": r["pendant"], "tv_glow": r.get("tv_glow", False),
                      "size_m": [fam["w"], fam["h"], fam["d"]], "camd_m": fam["camd"], "picture_px": [pictures[r["family"]]["w_px"], pictures[r["family"]]["h_px"]]}
    # models inventory with marks
    MARKS = {
        "Television_01": ("'VTECH' logo on the front panel, a 'WARNING' label, a 'TRRA' plate: painted out to the case's grey; NOT USED (television_02 serves)", "looked at, not used"),
        "television_02": ("a small rating plate on the back panel; 'PARAGON Viewing System' on the front bezel, left of the buttons (map at 1k, about x 272 to 300, y 450 to 560, lettered at 90 degrees: found by the review of 13 October, the writer had missed it): both painted out to the bezel's grey", "blank"),
        "wall_clock": ("'URBAN quartz' on the dial: painted out to the dial's white (a maker's name)", "blank"),
        "ceramic_vase_01": ("a barcode sticker on the body: painted out; NOT USED in a room (ceramic_vase_03 clean) ", "looked at, not used"),
        "ceramic_vase_03": ("none seen", "none"),
        "desk_lamp_arm_01": ("a small label reading 'MAX 15W' on the base: blanked; NOT USED (the rooms' lamps are the pendant and the oil lamp)", "looked at, not used"),
        "vintage_suitcase": ("the second suitcase's map carries about a dozen travel stickers (real places or lines): NOT USED", "looked at, not used"),
        "hanging_picture_frame_01": ("artwork map reads 'Ray Homes / Photo: 76cm x 51cm / Frame: 84cm x 59cm' (a maker's name): the whole artwork map is REPLACED by a script-drawn print (a flat grey-green landscape band under a pale sky), no text", "replace_artwork"),
        "hanging_picture_frame_02": ("artwork map is a painting of a palace signed 'Celine.F' (an artist's signature and a royal building): REPLACED by a script-drawn print", "replace_artwork"),
        "hanging_picture_frame_03": ("artwork map is a photograph of a Japanese castle (not 1990 Britain): REPLACED by a script-drawn print", "replace_artwork"),
        "standing_picture_frame_01": ("artwork is a modern canal photograph with a car of the 2010s: NOT USED", "looked at, not used"),
        "standing_picture_frame_02": ("artwork is a beach scene with small figures: NOT USED", "looked at, not used"),
        "fancy_picture_frame_01": ("artwork is a landscape painting with tiny riders: NOT USED (the frames above are enough)", "looked at, not used"),
        "fancy_picture_frame_02": ("artwork is a street scene painting with a group of figures including children: NEVER USED (content rule: no children, even painted)", "excluded: children"),
        "book_encyclopedia_set_01": ("spines read 'ENCYCLOPEDIA' and volume letters: a generic word, no firm; NOT USED in a room", "looked at, not used"),
        "ornate_mirror_01": ("none", "none"), "mantel_clock_01": ("none (a plain dial)", "none"), "alarm_clock_01": ("none (a plain dial with numerals)", "looked at, not used"),
        "Sofa_01": ("none", "none"), "sofa_02": ("none; 0.818 deep, over the tolerated back-wall budget: NOT USED", "looked at, not used"), "sofa_03": ("none (a cushion pattern square); 1.12 deep: NOT USED", "looked at, not used"),
        "ArmChair_01": ("none; 0.77 deep, over the tolerated back-wall budget of 0.71 once the cottage eye stands at the window: NOT USED (painted_wooden_bench serves in gf_front_2)", "looked at, not used"), "side_table_01": ("an ornamental gold script-like band on the top edge of the map: decoration, no text read; kept", "none"),
        "CoffeeTable_01": ("none; free-standing: NOT USED", "looked at, not used"), "Shelf_01": ("none", "none"), "wooden_bookshelf_worn": ("none (looked at again at 1k on 13 October after the fix)", "none"),
        "vintage_cabinet_01": ("none (a cream paper sheet with a hexagon pattern on map a)", "none"), "painted_wooden_cabinet": ("none (knobs only)", "none"),
        "drawer_cabinet": ("a 2010s piece (a black steel frame with open oak shelves and drawers); its navy side strip carries three rows of faint lettering-like marks (the review of 13 October; the writer's entry said none): NOT USED (wooden_bookshelf_worn serves in up_bedroom_2)", "looked at, not used"), "painted_wooden_bench": ("none (looked at again at 1k on 13 October after the fix)", "none"), "potted_plant_01": ("none", "none"), "potted_plant_02": ("none", "looked at, not used"),
        "vintage_oil_lamp": ("none", "none"), "throw_pillows_01": ("none", "looked at, not used"), "wicker_basket_01": ("none", "looked at, not used"), "old_bed_frame": ("none; its headboard is under the visible zone: NOT USED", "looked at, not used"),
        "vintage_day_bed": ("none; 0.855 deep: NOT USED", "looked at, not used"), "dining_table": ("none; free-standing: NOT USED", "looked at, not used"), "dining_chair_02": ("none; free-standing: NOT USED", "looked at, not used"),
        "WoodenChair_01": ("none; free-standing: NOT USED", "looked at, not used"), "round_wooden_table_01": ("none; free-standing: NOT USED", "looked at, not used"),
        "small_wooden_table_01": ("none; free-standing: NOT USED", "looked at, not used"), "modern_wooden_cabinet": ("none; a modern piece: NOT USED", "looked at, not used"),
        "vintage_wooden_drawer_01": ("not looked at (1.0 deep: over budget)", "not used"), "decorative_book_set_01": ("no glTF at 1k answered (the files call failed): NOT USED", "not used"),
    }
    inventory = {}
    for mid, rec in raw.items():
        if not rec.get("exists"):
            continue
        mk = MARKS.get(mid, ("none seen", "none"))
        inventory[mid] = {"name": rec["name"], "dims_mm_catalogue_xyz": [round(v, 1) for v in rec["dims_cm"]], "polycount": rec["polycount"], "authors": rec["authors"], "published": rec["date_published"],
                          "licence": "CC0 (Poly Haven)", "gltf_1k": rec["gltf_url"], "base_colour_maps_looked_at_1k": sorted(rec["textures"].keys()) if False else rec["diffuse_downloaded"],
                          "marks": mk[0], "status": mk[1], "used_in_rooms": sorted([rid for rid, r in rooms.items() if any(o["model"] == mid for o in r["objects"])])}
    for mid in list(inventory):
        if inventory[mid]["status"] in ("none", "blank", "replace_artwork") and not inventory[mid]["used_in_rooms"]:
            inventory[mid]["status"] = inventory[mid]["status"] + " (looked at; in no room)"
    tex_used = sorted({v for rid in R.ROOMS for v in (R.FINISH[R.ROOMS[rid]["walls"]]["texture"], R.FINISH[R.ROOMS[rid]["ceiling"]]["texture"], R.FINISH[R.ROOMS[rid]["floor"]]["texture"]) if v})
    textures = {t: {"licence": "CC0 (Poly Haven)", "url_1k_diffuse": texraw[t]["url"], "authors": texraw[t]["authors"], "marks": "none seen at 1k", "looked_at": "1k base colour, 13 October 2026"} for t in tex_used}
    # ---------- the photographs -------------------------------------------------------------------------------------------
    rows, brick = M.measure_all(a.photos)
    bands = M.summarise(rows)
    extra = M.measure_extra(a.photos)
    gp = json.load(open(os.path.join(HERE, "geograph_pages_read.json")))
    photos = []
    for pid, ph in P.PHOTOS.items():
        pg = gp[ph["gid"]]
        photos.append({"id": pid, "url": "https://www.geograph.org.uk/photo/%s" % ph["gid"], "title": ph["title"], "author": ph["author"], "licence": "CC BY-SA 2.0 (read on the page)", "taken": pg["taken_on_page"],
                       "read": "2026-10-13", "shows": ph["shows"], "period": ph["period"], "used": "measured and previewed (cropped to the windows, masked where the crop would show a plate or a sign)",
                       "preview": "production/previews/cloud-week/refs/house-windows/" + __import__("make_previews").preview_name(pid),
                       "crop": list(ph["crop"]), "masks": ph["masks"]})
    target = {
        "summary": "House windows of Quay Street: twenty windows in ten houses, every frame white (Jafar's ruling of 3 October), four kinds (two over two, one over one, and two replacement casements: P7's and P6's), the 1a fix as numbers (glass over a dark room, the box shaded, its lines drawn), the net, curtain and blind kinds, thirteen small rooms in the game's own `trace` rule, the white-board check measured on 1979 to 1994 photographs the way the gate measures.",
        "status": "fixes applied, not re-reviewed",
        "units": {"windows_mm": "kit frame: x across (0 at the window's middle, + toward the viewer's right), y INTO the wall from the brick face (0 at the face), z UP from the opening's bottom edge",
                  "rooms_m": "room frame: x across from the room's centre (+ toward the PICTURE's right), y back from the card plane, z up from the floor", "street_m": "x along the street, y across (east +), z above the road crown (footway = crown + 0.10)",
                  "kinds_of_number": ["Read", "Scaled", "Photo", "Derived", "Judgement"]},
        "street": {"frontage_y_m": H.FRONTAGE_Y, "eye_above_footway_m": H.EYE_ABOVE_FOOTWAY, "eye_z_above_crown_m": H.EYE_Z, "far_pavement_kerb_edge_y_m": H.PAVEMENT_FAR_Y, "wall_thickness_m": H.WALL_T,
                   "footway_above_crown_m": H.FOOTWAY_ABOVE_CROWN, "card_plane_behind_frontage_m": H.CARD_Y_BACK,
                   "card_note": "the card is 0.270 behind the brick face: 16 mm behind the nets (254), 80 mm behind the lower glass (190), clear of the box's back (250.8) and behind the wall's inner face (215): the wall hides the card outside the window's hole",
                   "window_centres_rule": "terrace-front.py window_centres: bay start + 1.5 and + 4.5 m (upper floors); cottages: door at 1.5 (or 4.5) and windows at 3.3 and 5.1 m (mirrored with the door)"},
        "sources": {"photographs": photos, "research_read": [
            "production/cloud-week/research/1a-sash-windows-low-angles.md (the fix, cheapest first)", "production/research/aaa-street/WINDOWS-FACADES-2026-10-04.md", "WINDOWS-GRAZING-2026-10-08.md", "WINDOWS-OTHER-DIRECTION-2026-10-04.md",
            "production/cloud-week/targets/shop-windows/TARGET.md sections 3 and 4 and TARGET-REVIEW.md (the lessons applied here)", "production/art/sash-window/target.json and TARGET-NOTES.md (the lab's sash, amended 8 October)",
            "tools/art-recipes/terrace-front.py (the sites, the kinds, the nets, the lit rule)", "tools/ue/make_interior_material.py `trace`", "production/specs/shop-interiors.json", "production/specs/unreal-look.json", "production/specs/vignette-scene.json, vignette-pieces.json",
            "production/research/evening-light-1990/SUMMARY-2026-09-29.md and production/research/shop-glass-reflections/NIGHT-2026-10-08.md (lit windows 6 cd/m2)", "RULINGS.md 3 and 8 October", "production/cloud-week/HANDOVER.md"],
            "libraries": "Poly Haven API (api.polyhaven.com assets and files), 13 October 2026: every model and texture named exists, CC0; the 1k base colour of each looked at (inventory).",
            "unreached": ["Wikimedia Commons (not asked: Geograph's feed answered)", "archive.org (not asked)", "any 1975 to 1995 night photograph of a terrace (none found: no Geograph result before 1996 for night, dusk or lit windows)", "any period photograph of a 1980s brown anodised aluminium house window (none among the 14 photographs; none searched by image: Geograph is searchable by words only)",
                          "Epic's pages (not needed: the engine facts come from the repository's notes)"]},
        "photo_measurements": {"method": M.__doc__, "windows": rows, "bands_by_state": bands, "brick_median_luma": brick, "p8_four_panes_the_gates_way": extra["P8_four_panes"],
                               "boxes_of_the_first_version": {"P1_a": {"outline": [433, 392, 451, 455], "panes": [[438, 398, 449, 446]], "P_over_L": 0.865, "D_over_L": 0.502, "note": "included the white-painted stone head and sill (L 234, the stone's paint reads 248 to 254) and a column of brick at the jamb (D 117, the brick's own median 119): D/L 0.47 to 0.50 was brick over painted stone, not the frame"},
                                                              "P1_b": {"outline": [403, 396, 419, 458], "panes": [[407, 402, 416, 448]], "P_over_L": 0.828, "D_over_L": 0.466},
                                                              "P1_e": {"outline": [433, 485, 451, 545], "panes": [[438, 492, 449, 538]], "P_over_L": 0.85, "D_over_L": 0.486}},
                               "frame_to_brick_linear_ratio": {"P1": round(M.to_lin(np.median([r["L90"] for r in rows.values() if r["photo"] == "P1"])) / M.to_lin(brick["P1"]), 2),
                                                               "P8": round(M.to_lin(np.median([r["L90"] for r in rows.values() if r["photo"] == "P8"])) / M.to_lin(brick["P8"]), 2)},
                               "tally": {"n_windows_classified": 60, "by_net": {"lower_sash_voile": 28, "full_height_net": 13, "cafe_net": 1, "curtains_drawn_or_open": 6, "blind": 1, "bare_dark_room": 11}, "unclear_not_counted": 5,
                                         "shares": {"lower_sash_voile": 0.47, "full_height_net": 0.22, "cafe_net": 0.02, "curtains": 0.10, "blind": 0.02, "bare": 0.18},
                                         "by_photograph": {"P2": {"lower": 11, "full": 3, "blind": 1, "bare": 1}, "P12": {"lower": 5, "curtain": 2, "cafe": 1}, "P1": {"full": 5, "bare": 4}, "P3": {"lower": 6, "full": 2, "bare": 2, "curtain": 2},
                                                           "P4": {"full": 2, "lower": 2, "bare": 1, "curtain": 2}, "P7": {"lower": 3, "bare": 2}, "P6": {"full": 1, "lower": 1, "bare": 1}},
                                         "method": "a hand count of every window whose state could be read in P1, P2, P3, P4, P6, P7 and P12, by eye on the previews: Photo, +-8 points",
                                         "note": "a net is a lower-sash voile in nearly half the windows and the upper sash is then clear: the room shows through it. The two held net pictures of the street (net_curtain_a, _b: a coarse square mesh of 7 to 10 mm, mean alpha 0.53, over the whole pane) match none of them (D2)"},
                               "paint_tally": {"n_windows": 60, "white": 0.55, "cream_or_ivory": 0.12, "dark_brown_or_red_brown": 0.13, "olive_green": 0.07, "blue": 0.08, "other": 0.05, "method": "by eye on the same photographs, +-8 points"}},
        "sites": sites, "houses": {k: [s["id"] for s in v] for k, v in houses.items()},
        "backdrop": {"what": "the same pieces on the hill's rows (x 48 to 110): backdrop_rise_approach_e (2 houses, 8 windows), _w (5 houses, 20 windows), _x (the row across the end: 5 houses, 20 windows), 48 windows in all, from CLIMB_HOUSE through plan_parts (2 storeys, 'plain' ground floor)",
                     "rule": "the kit's glass, frame, a flat net card per window, NO room picture: one window in three (CLIMB_LIT_EVERY) takes the lit pane `window_far_lit`, the rest the dark pane; the frames follow `_window_kind` by house; paint white (70 per cent), cream (20), olive (10) by the house's number: not placed individually here",
                     "count_checked_by_self_check": 48, "hill_framed_windows": "the north rise's framed windows (`_framed_window`, 125 m out: two pixels of frame) stay flat cards: not kit pieces"},
        "kinds": kinds, "paints": D.PAINTS,
        "glass": D.GLASS, "box_shade": D.BOX_SHADE, "nets": D.NETS, "net_common": D.NET_COMMON, "curtains": D.CURTAINS, "blinds": D.BLINDS,
        "rooms": {"visible_zone": {"what": "which parts of the room each review camera sees through the glass rectangle (144 rays, hit points in the PICTURE frame: x measured from the PICTURE-LEFT WALL (not from the room's centre: the objects' x_across is from the centre, add half the room's width to compare), y back from the card, z above the floor; the eye stands by the window)", "x_frame": "from the picture-left wall", "by_family": vz, "reading": "an upper room is seen from the street as its ceiling and the top 0.6 m of its back wall (from across) or the first 0.5 m of one side wall (along the street, near): so its picture's detail is ceiling, cornice, picture rail, wall tops and tall furniture tops; a cottage's front room is seen at eye level: the whole back wall and the side walls"}, "families": H.ROOMS, "budgets_computed": budgets, "budget_rule": R.BUDGET, "pictures_by_family": pictures, "finishes": R.FINISH, "forms": R.FORMS, "rooms": rooms,
                  "cards": {"camera_rule": "the render camera stands on the room's centre line d = W in front of the card, framing the card rectangle W x H exactly; the game's `trace` is imported, not rewritten",
                            "picture_names": "<room_id>_<state>.png with <room_id>.json beside them (room, w, h, d, camera_d, pixels, states, made_by, samples); 8-bit sRGB PNG; Cycles 128 samples, denoised; masters on F:/LedgerTools/house-rooms",
                            "states": ["day", "night_lit", "night_dark"], "brightness": {"day": 0.12, "night": 0.7},
                            "brightness_note": "day 0.12 (a front room by day is a dim ceiling and a dark wall; the shops' 0.15 is for a lit display), night 0.7 as the shops (shop-interiors.json); the pane composite measured in the gate decides"},
                  "picture_standards": {"day_mean_luma": 105.0, "night_lit_mean_luma": 70.0, "night_dark_mean_luma": 15.0, "tolerance": 0.15, "floor_factor": 0.7,
                                        "note": "Judgement, scaled from the approved pawnbroker pictures (119.5, 79.8, 17.7 measured 12 October) by the rooms' smaller windows and fewer lights: the checks' floors are 0.7 of these"},
                  "lights_by_state": {"day": "an overcast area light the size of the card on its plane (6500 K), strength set so the picture's mean luma meets the day standard; no tungsten", "night_lit": "the pendant (a paper shade, a 60 W tungsten bulb 2700 K, linear (1.0, 0.714, 0.344)) at the ceiling rose, 0.30 below the ceiling, and in the front rooms a table lamp's glow on the back wall; a television glow (cool 6500 K, emissive screen) where tv_glow; landings and empty rooms: a bare 40 W bulb or none (empty: night_lit = night_dark); a lit landing's emission is the absolute one of `landing_bulb`",
                                      "landing_bulb": D.LANDING_BULB, "curtain_emission": "each curtain and blind kind carries its own absolute lit emission (`curtains.*.night_lit_emission_linear`, `blinds.*.night_lit_emission_linear`)",
                                      "night_dark": "the sodium wash through the window: linear (1.0, 0.25, 0.0) = production/specs/unreal-look.json lantern_linear_rgb (NOT the scene file's stale (1, 0.7055, 0)), at 6 per cent of night_lit's energy; nothing else"},
                  "lit_share": {**D.LIT_SHARE, "lit_by_hour": lit_table, "lit_order_of_the_non_always_lit_windows": [s["id"] for s in elig]}},
        "inventory": {"polyhaven_models": inventory, "polyhaven_textures": textures, "brand_blocklist": ["paragon", "dixons", "currys", "comet", "rumbelows", "vtech", "ray homes", "celine", "lorex", "ingrid", "radolier", "hotpoint", "kenwood", "ekco", "anglian", "royal mail", "post office", "tesco", "woolworth", "sainsbury", "ikea", "dulux"],
                      "rule": "every model's base colour map was looked at at 1k on 13 October 2026 before it was named; a model with a mark is blanked in its map (the mark painted out to the surface's own colour) before it is used, or not used; every framed picture's artwork is replaced by a script-drawn print; the base colour of every placed model is checked region by region against its marks entry before its room is rendered (PIC-07). The first look missed television_02's maker's name on its front bezel: the placed models' maps were looked at again at 100 per cent after the review (FIXES-APPLIED.md)"},
    }
    ow = (376.7 - 304.8) / 850.0
    target["overlay"] = {
        "photo": "P8", "window": "the left window of the back of a Victorian terrace at Oxford (1987): a 2/2 sash seen nearly square on from below",
        "crop": [280, 270, 680, 470], "preview_scale": 3.0, "outline_px": [304.8, 293.9, 376.7, 430.6],
        "method": "edges by half-maximum crossings of the luma profiles along four rows and five columns of the photograph (scripted in the scratch, written here); the drawing is laid on at ONE scale, fitted on the width: 850 mm = 71.9 px (0.08459 px per mm); no vertical fit",
        "scale_px_per_mm": round(ow, 5),
        "edges": [
            {"name": "outer jambs, left and right", "axis": "x", "measured_px": [304.8, 376.7], "predicted_px": [304.8, 376.7], "tolerance_px": 0.0, "note": "fitted by construction"},
            {"name": "glazing bar centre", "axis": "x", "measured_px": 340.75, "predicted_px": 340.75, "tolerance_px": 1.5, "note": "the window's middle: bar 0.500 of the width on the photograph"},
            {"name": "glazing bar width", "axis": "x", "measured_px": 2.3, "predicted_px": round(22.2 * ow, 2), "tolerance_px": 1.0, "note": "22.2 mm (the lab's amended bar); the photograph reads 27 mm +- 6"},
            {"name": "head's outer top edge", "axis": "z", "measured_px": 293.9, "predicted_px": round(430.6 - 1676.4 * ow, 1), "tolerance_px": 7.0},
            {"name": "upper glass top edge", "axis": "z", "measured_px": 298.0, "predicted_px": round(430.6 - 1608.7 * ow, 1), "tolerance_px": 7.0},
            {"name": "meeting rail centre", "axis": "z", "measured_px": 362.6, "predicted_px": round(430.6 - 846.2 * ow, 1), "tolerance_px": 7.0},
            {"name": "lower glass bottom edge", "axis": "z", "measured_px": 422.3, "predicted_px": round(430.6 - 134.4 * ow, 1), "tolerance_px": 7.0},
        ],
        "stated_error": "vertical positions are laid at the width scale, so they sit about 3.6 px (2.6 per cent of the height) too high: the camera looks up and foreshortens the height by cos(15 degrees) = 0.97; the tolerance is 7 px, 5 per cent of the height",
        "visible_jamb_stripe_px": [3.1, 4.0], "visible_jamb_mm": 44.0,
    }
    target["kit_pieces"] = CK.kit_pieces(target)
    target["gate"] = CK.gate(target)
    target["checks"] = CK.checks(target)
    target["photographs_win"] = CK.photographs_win()
    target["could_not_settle"] = CK.could_not_settle()
    target["owed_on_pc"] = CK.owed_on_pc()
    json.dump(target, open(os.path.join(HERE, "target.json"), "w"), indent=1, sort_keys=False)
    print("target.json written:", os.path.getsize(os.path.join(HERE, "target.json")), "bytes;", len(sites), "sites;", len(rooms), "rooms;", len(inventory), "models")


if __name__ == "__main__":
    main()
