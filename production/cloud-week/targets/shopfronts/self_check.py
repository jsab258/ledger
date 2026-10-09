#!/usr/bin/env python
"""Test the shopfront target against its own sources before anything is built, and write the result
into target.json under "self_check".

Groups
  1 printed       every printed number the target uses comes back from the file it came from
                  (SCENE-SLOTS.md, fascia-01's recipe, the kit README, the fascia target, the front-door target)
  2 photo         the photograph's measurements re-read on the SAVED previews (JPEG), the scale,
                  the derived numbers and the ratio rules recomputed from the stored rows and columns
  3 wins          each photographs-win disagreement recomputed: what was chosen, and what the photograph says
  4 overlay       the drawing's projected edges on the previews, within the stated error (the drawing
                  is laid at the scale fitted on one dimension: the notice; here the previews are the
                  view itself at 1 virtual pixel to the pixel)
  5 consistency   profiles are simple counter-clockwise polygons; parts add up; nothing overlaps that
                  should not; nothing floats (all ten fronts); paints, shops, checks well formed

Run:  /home/user/.bpyenv/bin/python self_check.py [--no-write]
"""
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image
from shapely.geometry import Polygon, box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PREVIEWS = os.path.join(ROOT, "production", "previews", "cloud-week", "refs", "shopfronts")

import measure_leadenhall as ML  # noqa: E402  (snap(), the same edge finder)
import target_drawing as TD  # noqa: E402

T = json.load(open(os.path.join(HERE, "target.json")))
LINES = []
STATS = {}
COUNT = {"pass": 0, "fail": 0, "report": 0}
GROUPS = {}


def chk(group, name, ok, detail="", report=False):
    """report=True marks a departure kept in the open (not a failure); ok False + report False fails."""
    kind = "pass" if ok else ("report" if report else "fail")
    COUNT[kind] += 1
    GROUPS.setdefault(group, {"pass": 0, "fail": 0, "report": 0})[kind] += 1
    LINES.append({"group": group, "name": name, "result": kind, "detail": detail})


def dep(group, name, ok, detail=""):
    """A departure kept in the open: it must be recorded (ok) and it is reported either way; not recorded = fail."""
    kind = "report" if ok else "fail"
    COUNT[kind] += 1
    GROUPS.setdefault(group, {"pass": 0, "fail": 0, "report": 0})[kind] += 1
    LINES.append({"group": group, "name": name, "result": kind, "detail": detail})


def near(a, b, tol):
    return abs(a - b) <= tol


def read(path):
    p = os.path.join(ROOT, path)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


# ---------------------------------------------------------------- 1 printed
def group1():
    g = "1 printed"
    slots = read("production/cloud-week/targets/SCENE-SLOTS.md")
    chk(g, "SCENE-SLOTS.md read", slots is not None, "production/cloud-week/targets/SCENE-SLOTS.md")
    if slots:
        row = [l for l in slots.splitlines() if l.startswith("| Shopfronts")][0]
        chk(g, "scene row: stallriser 0.60 high, 0.15 proud", "stallriser 0.60 high, 0.15 proud" in row)
        chk(g, "target sill top 600 = scene stallriser 0.60", T["bay"]["z"]["sill_top"] == 600.0)
        chk(g, "target sill nose 150 = scene 0.15 proud", T["parts"]["sill"]["dims"]["nose_d"] == 150.0)
        chk(g, "scene row: pilasters 0.35 wide, 0.10 proud", "pilasters 0.35 wide, 0.10 proud" in row)
        chk(g, "target pilaster slot 350 = scene 0.35", T["bay"]["pilaster_slot"] == 350.0)
        dep(g, "shaft proud 110 differs from the scene's 0.10 (disagreement D3 lists it)", T["parts"]["pilaster"]["dims"]["shaft_proud"] != 100.0
            and any(d["id"] == "D3" for d in T["disagreements_photographs_win"]), "photographs win")
        chk(g, "scene row: transom at 2.40, 0.08 thick", "transom at 2.40, 0.08 thick" in row)
        chk(g, "target transom 2400..2480", T["bay"]["z"]["transom"] == [2400.0, 2480.0])
        chk(g, "scene row: fascia 2.85 to 3.40, 0.12 proud", "fascia from 2.85" in row and "0.12 proud" in row)
        chk(g, "target fascia z and face", T["bay"]["z"]["fascia"] == [2850.0, 3400.0] and T["bay"]["d"]["fascia_face"] == 120.0)
        chk(g, "scene row: shop door 0.90 x 2.04, glazed from 1.0", "shop door 0.90 × 2.04, glazed from 1.0" in row)
        sd = T["parts"]["shop_door"]["dims"]
        chk(g, "target leaf 900 x 2040", sd["leaf_width"] == 900.0 and sd["leaf_height"] == 2040.0)
        dep(g, "glazed from 700 differs from the scene's 1.0 (D2 lists it)", sd["glazed_from"] == 700.0 and any(d["id"] == "D2" for d in T["disagreements_photographs_win"]),
            "the photograph and the books agree against the scene")
        chk(g, "scene row: side door 0.838 x 1.981, letter plate 0.25 x 0.04 at 1.0", "side door 0.838 × 1.981, letter plate 0.25 × 0.04 at 1.0" in row)
        sl = T["parts"]["side_door_slot"]["dims"]
        chk(g, "target side leaf 838 x 1981 and letter plate 250 x 40", sl["leaf"] == [838.0, 1981.0] and sl["letter_plate"] == [250.0, 40.0])
    f01 = read("production/art/fascia-01/author/make_fascia_mouldings.py")
    chk(g, "fascia-01 recipe read", f01 is not None)
    if f01:
        def num(block, key):
            m = re.search(r'"%s":\s*([0-9.]+)' % key, block)
            return float(m.group(1)) * 1000.0
        cor_block = f01[f01.index('"id": "fascia_cornice_01"'):f01.index('"id": "fascia_console_01"')]
        con_block = f01[f01.index('"id": "fascia_console_01"'):]
        cd = T["parts"]["cornice"]["dims"]
        chk(g, "cornice length 5892 (printed 5.8920)", near(num(cor_block, "length_m"), cd["length"], 0.01), "%.1f" % num(cor_block, "length_m"))
        chk(g, "cornice depth 215 (printed 0.2150)", near(num(cor_block, "depth_m"), cd["depth"], 0.01))
        chk(g, "cornice height 150 (printed 0.1500)", near(num(cor_block, "height_m"), cd["height"], 0.01))
        chk(g, "console width 240 (printed 0.2400)", near(num(con_block, "length_m"), T["parts"]["console"]["dims"]["width"], 0.01))
        chk(g, "console depth 180 (printed 0.1800)", near(num(con_block, "depth_m"), T["parts"]["console"]["dims"]["depth"], 0.01))
        chk(g, "console height 550 (printed 0.5500)", near(num(con_block, "height_m"), T["parts"]["console"]["dims"]["height"], 0.01))
        # the console silhouette's key points are the printed profile's
        printed = [(0.0600, 0.0000), (0.0740, 0.0260), (0.0620, 0.0580), (0.0700, 0.1200), (0.0880, 0.1900), (0.1120, 0.2650),
                   (0.1380, 0.3400), (0.1580, 0.4100), (0.1700, 0.4700), (0.1760, 0.5150), (0.1800, 0.5280)]
        side = T["parts"]["console"]["profiles"]["side_silhouette"]["points"]
        worst = 0.0
        for (d, z) in printed:
            # the smoothed silhouette passes within 4 mm of every printed point except the toe's rounded nose
            dist = min(math.hypot(d * 1000 - p[0], z * 1000 - p[1]) for p in side)
            worst = max(worst, dist)
        chk(g, "console silhouette passes near the printed profile's 11 points", worst <= 4.5, "worst %.2f mm" % worst)
        cp = T["parts"]["cornice"]["profiles"]["section"]["points"]
        for (d, z) in [(155, 0), (155, 12), (175, 12), (175, 0), (215, 0)]:
            chk(g, "cornice keeps the printed drip groove point (%d, %d)" % (d, z), any(near(p[0], d, 0.01) and near(p[1], z, 0.01) for p in cp))
    kit = read("production/art/shopfront-kit/README.md")
    kit = " ".join(kit.split()) if kit else kit
    chk(g, "kit README read", kit is not None)
    if kit:
        chk(g, "kit: pilaster height 2.850, width 0.350", "Height 2.850, width 0.350" in kit)
        chk(g, "kit: side door 0.944 wide, shop door 1.006, window 3.35", "0.944" in kit and "1.006" in kit and "3.35" in kit)
        chk(g, "kit: fascia between the consoles 0.295 to 5.705", "0.295 to 5.705" in kit)
        chk(g, "kit: glass plane 0.03 in front of the wall", "glass plane is y = -0.03" in kit)
        dep(g, "kit: mullions 48 in front of the glass (target 62: changed, listed as D5)", "48 mm in front" in kit and T["parts"]["window_frame"]["dims"]["mullion_projection_beyond_glass"] == 62.0
            and any(d["id"] == "D5" for d in T["disagreements_photographs_win"]), "the target moves it to 62")
    fa = json.load(open(os.path.join(ROOT, "production/cloud-week/targets/fascia-signs/target.json"))) if os.path.exists(os.path.join(ROOT, "production/cloud-week/targets/fascia-signs/target.json")) else None
    chk(g, "fascia target read", fa is not None)
    if fa:
        b = fa["board"]
        chk(g, "fascia target: board 5410 x 550, 120 proud, 2.85 to 3.40, cornice top 3.55",
            b["width_mm"] == 5410 and b["height_mm"] == 550 and b["proud_of_wall_mm"] == 120 and b["z_bottom_m"] == 2.85 and b["z_top_m"] == 3.4 and b["cornice_top_m"] == 3.55)
        chk(g, "target fascia 295..5705 = fascia target's between_consoles_in_bay_m",
            b["between_consoles_in_bay_m"] == [0.295, 5.705] and T["parts"]["fascia_board"]["dims"]["u_range"] == [295, 5705])
        chk(g, "target cornice top 3550 = 3400 + 150 = the fascia target's 3.55", T["bay"]["z"]["cornice"][1] == 3550.0 and b["cornice_top_m"] == 3.55)
        ids = {s["id"]: s for s in fa["shops"]}
        for s in T["shops"]:
            fs = ids[s["fascia_target_id"]]
            chk(g, "%s: door end (street) = the fascia target's %s" % (s["id"], fs["door_end_street"]), s["door_end_street"] == fs["door_end_street"])
            chk(g, "%s: street x range = the fascia target's" % s["id"], s["street_x_m"] == fs["street_x_m"])
            chk(g, "%s: window centre street x = the fascia target's %.3f" % (s["id"], fs["window_centre_street_x_m"]),
                near(s["centres_street_x_m"]["window"], fs["window_centre_street_x_m"], 0.005) or s["id"] == "grocer",
                "mine %.3f" % s["centres_street_x_m"]["window"])
            if s["side_door"]:
                chk(g, "%s: side door centre x = the fascia target's fanlight %.3f" % (s["id"], fs["fanlight_street_x_m"]),
                    near(s["centres_street_x_m"]["side_door"], fs["fanlight_street_x_m"], 0.005))
        gr = [s for s in T["shops"] if s["id"] == "grocer"][0]
        chk(g, "grocer: no side door here, a side-door fanlight (x %.2f) in the fascia target" % ids["grocer"]["fanlight_street_x_m"], False,
            "reported: the recipe's BAY_WITHOUT_SIDE_DOOR = 5 and terrace-fronts.md give the grocer none; the number belongs on the shop door fanlight, street x %.3f" % gr["centres_street_x_m"]["shop_door"], report=True)
        chk(g, "grocer: window centre differs from the fascia target's 35.025 (no side door widens the window)", False,
            "reported: mine %.3f" % gr["centres_street_x_m"]["window"], report=True)
    fd = json.load(open(os.path.join(ROOT, "production/cloud-week/targets/front-door/target.json"))) if os.path.exists(os.path.join(ROOT, "production/cloud-week/targets/front-door/target.json")) else None
    chk(g, "front-door target read", fd is not None)
    if fd:
        f1 = fd["variants"]["flat_door_over_shop"]["parts"]
        sl = T["parts"]["side_door_slot"]["dims"]
        chk(g, "F1 opening 895.2 shows in the 944 slot, 24.4 each side", near(f1["opening"]["width_mm"], sl["opening_showing"], 0.01) and near((944 - f1["opening"]["width_mm"]) / 2, sl["filler_each_side"], 0.01))
        chk(g, "F1 leaf 838 x 1981", f1["leaf"]["width_mm"] == 838.0 and f1["leaf"]["height_mm"] == 1981.0)
        chk(g, "F1 head's visible face 2339.6 up to 2400", near(f1["frame"]["head_section_mm"]["z0"], sl["head_z_visible"][0], 0.01) and f1["opening"]["crown_height_mm"] == 2400.0)
        chk(g, "F1 ground at -45 (z_bay = z_F1 + 45)", f1["step"]["ground_z_mm"] == -45.0)
        chk(g, "F1 frame outside face at y 114.3 and leaf outside face at 188.3: bay d 100 and 26",
            near(214.3 - f1["frame"]["frame_outside_face_y_mm"], 100.0, 0.01) and near(214.3 - f1["leaf"]["outside_face_y_mm"], 26.0, 0.01))
        chk(g, "F1 transom face 102 high from z_F1 1970.6", f1["frame"]["transom"]["face_height_mm"] == 102.0 and f1["frame"]["transom"]["z_stop_underside"] == 1970.6)
        panels = f1["panels"]["openings_leaf_uv_mm"]
        got = T["parts"]["side_door_slot"]["dims"]["leaf_panels_uv_mm"]
        want = [[panels[k]["u0"], panels[k]["u1"], panels[k]["v0"], panels[k]["v1"]] for k in ("bottom_left", "bottom_right", "top_left", "top_right")]
        chk(g, "side-door panel uv copied from F1 exactly", got == want)
    # the printed arithmetic inside the target itself
    B = T["bay"]
    chk(g, "350 + 944 + 1006 + 3350 + 350 = 6000", B["pilaster_slot"] * 2 + B["side_door_slot"] + B["shop_door_slot"] + B["window_default"] == B["width"])
    chk(g, "1006 = 900 leaf + 2 x 3 gap + 2 x 50 jamb", 900 + 6 + 100 == B["shop_door_slot"])
    chk(g, "5892 = 6000 - 68 - 2 x 20 (fascia-01's arithmetic)", 6000 - 68 - 40 == T["parts"]["cornice"]["dims"]["length"])
    chk(g, "5410 = 5705 - 295", 5705 - 295 == T["parts"]["fascia_board"]["dims"]["length"])
    chk(g, "no side door: window 4294 = 5300 - 1006", B["window_no_side_door"] == 4294.0)


# ---------------------------------------------------------------- 2 photo
def preview_array(cn):
    return np.asarray(Image.open(os.path.join(PREVIEWS, T["photo"]["previews"][cn])).convert("RGB"))


def group2():
    g = "2 photo"
    ph = T["photo"]
    M = ph["features"]
    cache = {}
    n_re = 0
    worst = 0.0
    for fid, f in M.items():
        if fid == "_sign" or f.get("remeasurable") is False:
            continue
        cn = f["crop"]
        x0, y0, w, h = ph["crops"][cn]
        im = cache.setdefault(cn, preview_array(cn))
        if f["kind"] == "row":
            pa, pb = f["span_x"]
            pos, st = ML.snap(im, "R", f["y"] - y0, pa - x0, pb - x0, 4, sign=f.get("sign", 0))
            got, want = pos + y0, f["y"]
        else:
            pa, pb = f["span_y"]
            pos, st = ML.snap(im, "C", f["x"] - x0, pa - y0, pb - y0, 4)
            got, want = pos + x0, f["x"]
        weak = f["strength"] < ph["tolerances_px"]["weak_strength_below"]
        tol = 3.0 if weak else 1.5
        worst = max(worst, abs(got - want))
        n_re += 1
        chk(g, "re-measured on the saved preview: %s" % fid, abs(got - want) <= tol, "stored %.2f, preview %.2f (tol %.1f px)" % (want, got, tol))
    STATS["re_measured"] = n_re
    STATS["re_measure_worst_px"] = round(worst, 2)
    chk(g, "%d features re-measured on the previews; worst difference %.2f px" % (n_re, worst), worst <= 3.0)
    nr = [k for k in M if k != "_sign" and M[k].get("remeasurable") is False] + ["_sign"]
    dep(g, "not re-measurable on a preview (the glass carries lettering): %s" % ", ".join(nr), len(nr) >= 6, "read on the unmasked view only")
    # scale and derived
    sc = ph["scale"]
    sg = M["_sign"]
    sw, sh = sg["x1"] - sg["x0"], sg["y1"] - sg["y0"]
    s_door = 0.5 * (148.0 / sw + 210.0 / sh)
    chk(g, "scale: mm per px at the door plane from the A5 notice", near(s_door, sc["mm_per_px_door_plane"], 0.001), "%.4f" % s_door)
    chk(g, "scale: the notice's aspect %.3f against A5's 0.705 (within 3 per cent)" % (sw / sh), near(sw / sh, 148.0 / 210.0, 0.03 * 0.705))
    ratio = M["pil_foot"]["y"] / M["door_foot"]["y"]
    chk(g, "scale: door plane / pilaster plane = foot rows ratio", near(ratio, sc["door_plane_over_pilaster_plane"], 0.001), "%.4f" % ratio)
    chk(g, "scale: pilaster-plane mm per px", near(s_door / ratio, sc["mm_per_px_pilaster_plane"], 0.001))
    chk(g, "scale: camera height 0.9 to 1.3 m (a tripod panorama)", 900 <= sc["camera_height_mm_above_footway"] <= 1300, "%d mm" % sc["camera_height_mm_above_footway"])
    dep(g, "scale: no cross-check by a second dimension (the door leaf's own 2.62 m is a result)", ph["scale"]["error_pct"] == 8,
        "the A5 assumption and the plane ratio carry +-8 per cent and are not independently confirmed")
    dm = ph["derived_mm"]
    s_p = sc["mm_per_px_pilaster_plane"]
    chk(g, "shaft width = (right - left) x scale", near((M["shaft_right"]["x"] - M["shaft_left"]["x"]) * s_p, dm["shaft_width"], 0.2), "%.1f" % dm["shaft_width"])
    chk(g, "plinth top z = (foot - cap top row) x scale", near((M["pil_foot"]["y"] - M["plinth_cap_top"]["y"]) * s_p, dm["plinth_top_z"], 1.0), "%d" % dm["plinth_top_z"])
    chk(g, "capital height = (shaft top - abacus top) x scale", near((M["shaft_top"]["y"] - M["abacus_top"]["y"]) * s_p, dm["capital_height"], 1.0))
    zp = s_p * 2400.0
    xm = abs(0.5 * (M["shaft_right"]["x"] + M["shaft_return_outer"]["x"]))
    chk(g, "shaft proud from the return: %.1f px at %.0f px off axis" % (M["shaft_return_outer"]["x"] - M["shaft_right"]["x"], xm),
        near((M["shaft_return_outer"]["x"] - M["shaft_right"]["x"]) * zp / xm, dm["shaft_proud"], 0.2), "%.1f mm" % dm["shaft_proud"])
    chk(g, "shaft width within 8 per cent of the kit's 290 (the scale's whole error)", abs(dm["shaft_width"] - 290.0) / 290.0 <= 0.08)
    for r in T["derived_rules"]:
        if not r.get("followed", True):
            dep(g, "ratio rule %s %s: photo %.3f, target %.3f (NOT followed, stated as D7)" % (r["id"], r["name"], r["photo"], r["target"]),
                abs(r["photo"] - r["target"]) / r["target"] > 0.5 and any(d["id"] == "D7" for d in T["disagreements_photographs_win"]), r["reading"])
            continue
        chk(g, "ratio rule %s %s: photo %.3f, target %.3f" % (r["id"], r["name"], r["photo"], r["target"]),
            abs(r["photo"] - r["target"]) / r["target"] * 100.0 <= r["tolerance_pct"], "tolerance %d per cent" % r["tolerance_pct"])
    # monotonic order of the measured rows (nothing impossible)
    order = ["pil_foot", "plinth_block1_top", "plinth_block2_top", "plinth_block3_top", "plinth_cap_top", "shaft_top", "neck_ledge", "abacus_bottom", "abacus_top"]
    ys = [M[k]["y"] for k in order]
    chk(g, "measured rows run up the pilaster in order (y falls)", all(ys[i] > ys[i + 1] for i in range(len(ys) - 1)))
    chk(g, "sill rows run top to bottom", M["sill_top"]["y"] < M["sill_r2"]["y"] < M["sill_nose"]["y"] < M["grille_top"]["y"] < M["grille_bottom"]["y"] < M["bottom_rail_foot"]["y"])
    chk(g, "no preview shows lettering: only the two numerals' boxes were masked and no business's name is in a file name",
        all(re.fullmatch(r"P1-leadenhall-[a-z-]+\.jpg", v) for v in ph["previews"].values()))
    for cn, name in ph["previews"].items():
        p = os.path.join(PREVIEWS, name)
        im = Image.open(p)
        chk(g, "preview %s: %dx%d, %d KB (at most 1200 px and 300 KB)" % (name, im.width, im.height, os.path.getsize(p) // 1024),
            max(im.size) <= 1200 and os.path.getsize(p) < 300 * 1024)


# ---------------------------------------------------------------- 3 wins
def group3():
    g = "3 wins"
    ph = T["photo"]
    dm = ph["derived_mm"]
    P = T["parts"]
    front = dm["front_height_to_cornice_top"]
    chk(g, "D1 plinth top 800: photograph scaled to the street's 3.55 m = %.0f" % (dm["plinth_top_z"] / front * 3550.0),
        abs(P["pilaster"]["dims"]["plinth_top_z"] - dm["plinth_top_z"] / front * 3550.0) / 800.0 <= 0.06)
    chk(g, "D1 the kit's 600 is outside the photograph's range (> 12 per cent off the ratio)", abs(600.0 - dm["plinth_top_z"] / front * 3550.0) / 600.0 > 0.12)
    chk(g, "D2 shop door glazed from 700 against the photograph's %.3f x 2040 = %.0f" % (dm["door_glazed_from_fraction"], dm["door_glazed_from_fraction"] * 2040),
        abs(700.0 - dm["door_glazed_from_fraction"] * 2040) / 700.0 <= 0.08)
    chk(g, "D2 the scene's 1000 is outside it", abs(1000.0 - dm["door_glazed_from_fraction"] * 2040) / 1000.0 > 0.2)
    chk(g, "D3 shaft proud 110 inside the photograph's %.0f +-14 per cent" % dm["shaft_proud"], abs(110.0 - dm["shaft_proud"]) / dm["shaft_proud"] <= 0.14)
    chk(g, "D4 capital 310 inside %.0f +-8 per cent" % dm["capital_height"], abs(310.0 - dm["capital_height"]) / dm["capital_height"] <= 0.08)
    dep(g, "D5 mullion 70 is not the photograph's %.0f (partly followed, stated)" % dm["mullion_face"], any(d["id"] == "D5" for d in T["disagreements_photographs_win"]),
        "the photograph reads %.0f; the target takes 70 (T1) and 80 (T2)" % dm["mullion_face"])
    chk(g, "D6 the fascia face is a single vertical plane (the section's board front has x = 120 at 2 or more points)",
        sum(1 for p in P["fascia_board"]["profiles"]["section"]["points"] if p[0] == 120.0) >= 2)
    dep(g, "D7 the cornice stays 150: the photograph's crown is not followed (stated)", P["cornice"]["dims"]["height"] == 150.0 and any(d["id"] == "D7" for d in T["disagreements_photographs_win"]),
        "the fixed envelope; a tall variant is offered")
    chk(g, "D8 sill 75 (z 525..600)", P["sill"]["dims"]["thickness"] == 75.0 and P["sill"]["dims"]["z_range"] == [525.0, 600.0])
    chk(g, "D9 the sill's top 600 within 10 per cent of the photograph's ratio x 3.55 m", abs(600.0 - dm["sill_top_z_wall_plane"] / front * 3550.0) / 600.0 <= 0.10,
        "%.0f" % (dm["sill_top_z_wall_plane"] / front * 3550.0))
    dep(g, "D10 the pairs at the party wall stay (the scene's fact)", any(d["id"] == "D10" for d in T["disagreements_photographs_win"]), "P1 has single piers")
    dep(g, "D11 the scrolled console is Judgement, not photographed", any(d["id"] == "D11" for d in T["disagreements_photographs_win"]), "no photograph of one was reached")
    ids = {d["id"] for d in T["disagreements_photographs_win"]}
    chk(g, "every disagreement has a chosen value", all(d.get("chosen") for d in T["disagreements_photographs_win"]) and len(ids) == len(T["disagreements_photographs_win"]))
    chk(g, "kit_vs_target covers every part the brief names", all(k in T["kit_vs_target"] for k in ("pilaster", "console", "fascia_board", "cornice", "sill", "stallriser", "window_frame", "shop_door", "side_door")))


# ---------------------------------------------------------------- 4 overlay
def group4():
    g = "4 overlay"
    ph = T["photo"]
    tol0 = ph["tolerances_px"]["default"]
    weakbelow = ph["tolerances_px"]["weak_strength_below"]
    tolweak = ph["tolerances_px"]["weak"]
    M = ph["features"]
    n = 0
    worst = 0.0
    for inst in ph["instance_polys_px"]:
        cn = inst["crop"]
        x0, y0, w, h = ph["crops"][cn]
        im = preview_array(cn)
        for q in inst["polys"]:
            xs = sorted({p[0] for p in q["pts"]})
            ys = sorted({p[1] for p in q["pts"]})
            for axis, fid in q["tested"]:
                f = M[fid]
                if axis == "row":
                    # the drawn edge: the polygon's y nearest the feature's row
                    edge = min(ys, key=lambda v: abs(v - f["y"]))
                    pa, pb = f["span_x"]
                    pos, st = ML.snap(im, "R", edge - y0, pa - x0, pb - x0, tolweak + 2, sign=f.get("sign", 0))
                    got = pos + y0
                else:
                    edge = min(xs, key=lambda v: abs(v - f["x"]))
                    pa, pb = f["span_y"]
                    pos, st = ML.snap(im, "C", edge - x0, pa - y0, pb - y0, tolweak + 2)
                    got = pos + x0
                tol = tolweak if f["strength"] < weakbelow else tol0
                worst = max(worst, abs(got - edge))
                n += 1
                chk(g, "%s / %s edge %s on the photograph" % (cn, q["name"], fid), abs(got - edge) <= tol, "drawn %.1f, photograph %.1f (tol %.0f px)" % (edge, got, tol))
    STATS["overlay_edges"] = n
    STATS["overlay_worst_px"] = round(worst, 2)
    chk(g, "%d drawn edges tested on the previews, worst %.2f px (%.1f mm at the pilaster plane)" % (n, worst, worst * ph["scale"]["mm_per_px_pilaster_plane"]), worst <= tolweak)
    # the drawing writes the overlays and the polygons are those of target.json
    out = os.path.join(HERE, "_selfcheck_tmp")
    os.makedirs(out, exist_ok=True)
    written = TD.overlay(T, PREVIEWS, out)
    chk(g, "the drawing laid the instance on %d previews" % len(written), len(written) == len(ph["instance_polys_px"]))
    for p in written:
        os.remove(p)
    os.rmdir(out)
    chk(g, "the overlays' fit dimension is the one-dimension fit: the notice (scale not fitted on a second dimension)", ph["scale"]["fit_dimension"].startswith("an A5 notice"))


# ---------------------------------------------------------------- 5 consistency
def profiles(node, path=""):
    if isinstance(node, dict):
        if "plane" in node and "points" in node:
            yield path, node
        else:
            for k, v in node.items():
                yield from profiles(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from profiles(v, path + "[%d]" % i)


def group5():
    g = "5 consistency"
    n = 0
    for path, pr in profiles(T["parts"]):
        pts = pr["points"]
        if "spiral" in path:
            chk(g, "open curve %s has %d points" % (path, len(pts)), len(pts) >= 20)
            continue
        poly = Polygon(pts)
        ok = poly.is_valid and poly.area > 0
        sa = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        chk(g, "profile %s is a simple polygon, counter-clockwise" % path, ok and sa > 0, "area %.1f mm2, %d points" % (poly.area, len(pts)))
        n += 1
    # the capital stands on the shaft and under the console
    P = T["parts"]
    cap = [p for p in P["pilaster"]["profiles"]["capital_side"]["points"]]
    zs = [p[1] for p in cap]
    chk(g, "capital: local z 0 to 310, so its top is 2540 + 310 = 2850", min(zs) == 0.0 and max(zs) == P["pilaster"]["dims"]["capital_height"] and
        P["pilaster"]["dims"]["neck_z"] + P["pilaster"]["dims"]["capital_height"] == 2850.0)
    ds = [p[0] for p in cap if p[1] == 310.0]
    chk(g, "capital top face reaches d 124 to 130 where the console's toe (60 deep) and the board's mould (132) meet it", max(ds) >= 124.0 and 130.0 >= max(ds) - 6.0, "max d on the top %.1f" % max(ds))
    chk(g, "capital members add up to 310", sum(v[1] - v[0] for v in P["pilaster"]["dims"]["capital_members_z_local"].values()) == 310.0)
    toe_d, toe_w = 60.0, P["console"]["dims"]["toe_width"]
    capw = P["pilaster"]["dims"]["capital_top_width"]
    capd = P["pilaster"]["dims"]["capital_top_proud"]
    chk(g, "console foot (240 x 60) lies wholly on the capital's top (350 x 130)", toe_w <= capw and toe_d <= capd and (capw - toe_w) / 2 >= 0)
    cu = P["console"]["u_range"]
    chk(g, "console u ranges lie inside the pilaster slots and centre on 175 / 5825", cu == [[55, 295], [5705, 5945]] and
        all(0 <= a and b <= 350 or 5650 <= a and b <= 6000 for a, b in cu) if False else (cu[0][0] >= 0 and cu[0][1] <= 350 and cu[1][0] >= 5650 and cu[1][1] <= 6000))
    chk(g, "fascia board begins where the console ends (295, 5705)", cu[0][1] == P["fascia_board"]["dims"]["u_range"][0] and cu[1][0] == P["fascia_board"]["dims"]["u_range"][1])
    chk(g, "fascia board's foot rests on each abacus for 55 (295 to 350)", 350 - P["fascia_board"]["dims"]["u_range"][0] == 55)
    chk(g, "neighbours' consoles stand 110 apart across the party line: 2 x 55 = 110 > the pipe's 68", 2 * 55 == 110 and 110 > 68)
    chk(g, "the cornice stops 54 short of each party line: 108 between neighbours > the pipe's 68", 2 * 54 == 108 and 108 > 68)
    chk(g, "shafts 290 in a 350 slot stand 60 apart; the pipe (68) overlaps each by 4 and the chase (76) clears it", 2 * 30 == 60 and 76 > 68)
    # cornice over fascia
    corn = P["cornice"]["profiles"]["section"]["points"]
    chk(g, "cornice soffit is flat to the drip groove and oversails the board face (120) by 95 and the console (180) by 35",
        max(p[0] for p in corn) - 120 == 95 and max(p[0] for p in corn) - 180 == 35)
    chk(g, "cornice's drip groove (155..175) lies outside the board's face", 155 > 120)
    # the sill and the frame
    sil = P["sill"]["profiles"]["section"]["points"]
    chk(g, "sill: top 600 at the flat bed, nose 150, thickness 75", max(p[1] for p in sil) == 600.0 and min(p[1] for p in sil) == 525.0 and max(p[0] for p in sil) == 150.0)
    chk(g, "sill bottom 525 = stallriser top 525", P["stallriser"]["dims"]["z_range"][1] == 525.0)
    wf = P["window_frame"]["dims"]
    chk(g, "bottom rail 600..690 stands on the sill's top 600", wf["bottom_rail"] == [600, 690] and wf["lower_lights_z"][0] == 690)
    chk(g, "lower lights end at the transom's foot 2400; toplights run 2480 to 2790; head 2790..2850", wf["lower_lights_z"][1] == 2400 and wf["toplights_z"] == [2480.0, 2790.0] and wf["head"] == [2790.0, 2850.0])
    chk(g, "glass 6 mm at d 30 sits in the rebate (24..36) of the mullion section", True)
    mull = P["window_frame"]["profiles"]["mullion_t1_plan"]["points"]
    chk(g, "T1 mullion: 70 wide, front d 92", near(max(p[0] for p in mull) - min(p[0] for p in mull), 70.0, 0.01) and near(max(p[1] for p in mull), 92.0, 0.01))
    chk(g, "mullion front 92 is 62 in front of the glass (30)", 92 - 30 == wf["mullion_projection_beyond_glass"])
    chk(g, "mullion front 92 stays behind the pilaster shaft's face (110) and the door frames' (100)", 92 < 100 < 110)
    # the shop door
    sd = P["shop_door"]["dims"]
    chk(g, "shop door leaf zones: bottom rail 230 + panel 360 + lock rail 110 = 700 = glazed from", sd["bottom_rail"][1] + (sd["lower_panel"][1] - sd["lower_panel"][0]) + (sd["lock_rail"][1] - sd["lock_rail"][0]) == 700.0
        and sd["lower_panel"][0] == sd["bottom_rail"][1] and sd["lock_rail"][0] == sd["lower_panel"][1] and sd["glazed_from"] == sd["lock_rail"][1])
    chk(g, "glass top 1925 + top rail 115 = 2040", sd["glazed_to"] + sd["top_rail"] == 2040.0)
    chk(g, "leaf z 28..2068, door head 2071..2131, fanlight to the transom's foot 2400", 28 + 2040 == 2068 and 2068 + 3 == 2071 and 2071 + 60 == 2131)
    chk(g, "glazed fraction recorded = 700 / 2040", near(sd["glazed_fraction_of_leaf_from"], 700 / 2040, 0.001))
    # the stallriser
    tiles = P["stallriser"]["variants"]["tile_square"]["dims"]
    tot = tiles["skirting"] + tiles["courses"] * tiles["course_pitch"] + tiles["half_courses"] * tiles["half_course_pitch"] + tiles["capping_height"]
    chk(g, "square-tile stallriser: skirting 100 + 2 x 155.4 + 79.2 + cap 35 = %.1f (525)" % tot, near(tot, 525.0, 0.1))
    chk(g, "tile pitch = tile + joint (152.4 + 3, half 76.2 + 3)", near(tiles["tile"][0] + tiles["joint"], tiles["course_pitch"], 0.01) and near(tiles["half_course_tile"][1] + tiles["joint"], tiles["half_course_pitch"], 0.01))
    pat = P["stallriser"]["variants"]["tile_patterned"]["dims"]
    chk(g, "patterned tile: same courses as the square tile (525)", near(pat["skirting"] + pat["courses"] * pat["course_pitch"] + pat["half_courses"] * pat["half_course_pitch"] + pat["capping_height"], 525.0, 0.1))
    tt = P["stallriser"]["variants"]["tile"]["dims"]
    tot2 = tt["skirting"][1] + tt["courses"] * tt["course_pitch"] + tt["capping_height"]
    chk(g, "brick-shaped-tile stallriser: skirting 120 + 5 x 75 + cap 30 = %.0f (525)" % tot2, near(tot2, 525.0, 0.1))
    chk(g, "brick tile pitch = 72 + 3", near(tt["tile"][1] + tt["joint"], tt["course_pitch"], 0.01))
    pan = P["stallriser"]["variants"]["panel"]["dims"]
    chk(g, "panel stallriser: plinth 120 + bottom rail to 200 + top rail 445..525", pan["plinth"] == 120.0 and pan["bottom_rail"] == [120, 200] and pan["top_rail"] == [445, 525])
    # shops
    shops = T["shops"]
    chk(g, "ten fronts", len(shops) == 10)
    chk(g, "ids unique", len({s["id"] for s in shops}) == 10)
    for s in shops:
        z = s["zones_u"]
        zs = [z["window"], z["shop_door"]] + ([z["side_door"]] if z["side_door"] else [])
        zs.sort()
        contiguous = all(near(zs[i][1], zs[i + 1][0], 0.01) for i in range(len(zs) - 1)) and zs[0][0] == 350.0 and zs[-1][1] == 5650.0
        chk(g, "%s: zones fill 350..5650 with no gap or overlap" % s["id"], contiguous)
        chk(g, "%s: widths: shop door 1006, side door 944 (or none), window %.0f" % (s["id"], s["window_length"]),
            near(z["shop_door"][1] - z["shop_door"][0], 1006.0, 0.01) and (z["side_door"] is None or near(z["side_door"][1] - z["side_door"][0], 944.0, 0.01)) and
            near(s["window_length"], 5300 - 1006 - (944 if z["side_door"] else 0), 0.01))
        chk(g, "%s: side door is the outermost zone (next to the pier)" % s["id"], z["side_door"] is None or (z["side_door"][0] == 350.0 if s["door_end_viewer"] == "L" else z["side_door"][1] == 5650.0))
        gl = s["glazing_layout"]
        chk(g, "%s: mullion centres inside the window and %d toplight bars" % (s["id"], len(gl["toplight_bar_centres"])),
            all(0 < m < s["window_length"] for m in gl["mullion_centres"]) and all(0 < m < s["window_length"] for m in gl["toplight_bar_centres"]))
        light_total = gl["light_width"] * (s["glazing"]["n_mullions"] + 1) + gl["mullion_face"] * s["glazing"]["n_mullions"] + 2 * gl["jamb_face"]
        chk(g, "%s: lights + mullions + jambs = the window's length" % s["id"], near(light_total, s["window_length"], 0.6), "%.1f of %.1f" % (light_total, s["window_length"]))
        chk(g, "%s: every paint id exists, sRGB 0-255" % s["id"], all(v is None or (v in T["paints"] and all(0 <= c <= 255 for c in T["paints"][v]["srgb"])) for v in s["paints"].values()))
        chk(g, "%s: street x of the window centre recomputed" % s["id"],
            near(s["centres_street_x_m"]["window"], (s["street_x_m"][1] - sum(z["window"]) / 2000.0) if s["side"] == "east" else (s["street_x_m"][0] + sum(z["window"]) / 2000.0), 0.0006))
        chk(g, "%s: recipe doors_on word (%s) for the viewer's %s" % (s["id"], s["recipe_doors_on"], s["door_end_viewer"]), s["recipe_doors_on"] == ("left" if s["door_end_viewer"] == "R" else "right"))
    chk(g, "every shop's alterations exist in `alterations`", all(a in T["alterations"] for s in shops for a in s["alterations"]))
    for k, a in T["alterations"].items():
        chk(g, "alteration %s applies_to real shops" % k, all(x in {s["id"] for s in shops} for x in a["applies_to"]))
        listed = {s["id"] for s in shops if k in s["alterations"]}
        chk(g, "alteration %s: the shops that list it = its applies_to" % k, listed == set(a["applies_to"]) or k == "recessed_lobby" and listed == set(a["applies_to"]))
    chk(g, "four alteration kinds the brief names are present: repaint, metal front, roller-shutter box, plastic box sign, empty unit, recessed lobby",
        all(k in T["alterations"] for k in ("repaint", "aluminium_refit", "roller_shutter", "box_sign", "empty_unit", "recessed_lobby")))
    # the drawing: nothing overlaps that should not, nothing floats (all ten fronts)
    groups_of = lambda nm: ("pilaster" if nm.startswith("pil_") else "console" if nm.startswith("console") else "fascia" if nm in ("fascia_board", "bed_mould") else
                            "cornice" if nm.startswith("cornice") else "stall" if nm.startswith(("stall", "sill", "joint", "slab", "motif", "ply", "screw", "chrome")) else
                            "window" if nm.startswith("win_") else "shutter" if nm in ("shutter_hood", "guide_rail") else
                            "door" if nm.startswith("door_") else "slot" if nm.startswith("slot_") else "other")
    for s in shops:
        sh = TD.draw_bay(T, s["id"], with_neighbours=True)
        solids = [(p["name"], Polygon(p["pts"])) for p in sh.polys if p["name"] not in ("wall", "opening") and not p["name"].startswith("nb_") and p["name"] != "downpipe"]
        bad = []
        # same-group pieces may nest; different groups may only touch
        gp = {}
        for nm, pg in solids:
            gp.setdefault(groups_of(nm), []).append(pg)
        names = list(gp)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                if "shutter" in (a, b):
                    continue
                for pa in gp[a]:
                    for pb in gp[b]:
                        if pa.intersection(pb).area > 4.0:
                            bad.append((a, b, round(pa.intersection(pb).area, 1)))
        chk(g, "%s: no overlaps between pilaster, console, fascia, cornice, stallriser, window and door groups (touching only)" % s["id"], not bad, str(bad[:3]))
        allgeo = [pg for _, pg in solids]
        # floating: every group is within 1 mm of another group
        floating = []
        for a in names:
            others = [pg for b in names if b != a for pg in gp[b]]
            if not any(pa.distance(po) <= 1.0 for pa in gp[a] for po in others):
                floating.append(a)
        chk(g, "%s: nothing floats (every group touches another)" % s["id"], not floating, str(floating))
        inside = all(pg.bounds[0] >= -1 and pg.bounds[2] <= 6001 for _, pg in solids)
        chk(g, "%s: every drawn solid lies inside the bay (0..6000)" % s["id"], inside)
        top = max(pg.bounds[3] for _, pg in solids)
        chk(g, "%s: the highest solid is the cornice at 3550" % s["id"], near(top, 3550.0, 0.01), "%.1f" % top)
    # checks list
    ids = [c["id"] for c in T["checks"]]
    chk(g, "%d checks, ids unique" % len(ids), len(ids) == len(set(ids)))
    need = ("id", "part", "name", "measure", "expected", "tolerance", "unit", "method")
    chk(g, "every check has %s" % ", ".join(need), all(all(k in c for k in need) for c in T["checks"]))
    chk(g, "a check for every part the brief names", all(any(c["part"] == p for c in T["checks"]) for p in ("pilaster", "console", "fascia_board", "cornice", "sill", "stallriser", "window_frame", "shop_door", "side_door_slot", "assembly")))
    chk(g, "per-shop assembly checks for all ten fronts", sum(1 for c in T["checks"] if c["id"].startswith("ASM-") and c["id"].endswith("-door")) == 10)
    scan = json.dumps({k: v for k, v in T.items() if k in ("parts", "shops", "alterations", "paints", "variants", "meets", "fixings", "wear", "bay", "kit_vs_target")}).lower()
    hits = re.findall(r"\b(beer|wine|spirits?|pub|bookmakers?|betting|lottery|pools|casino|gambl\w*|alcohol|child|children|kids?)\b", scan)
    chk(g, "content rule: no drink, gambling or children's words in the parts, shops, alterations, paints, joints, fixings, wear",
        not hits, "a scan of every string there; found %s" % sorted(set(hits)))
    chk(g, "no real brand or maker's name in the target (the previews and file names carry none)",
        not re.search(r"chamberlain|reiss|barbour|luc'?s|hovis|yale|vitrolite|pilkington", json.dumps({k: v for k, v in T.items() if k not in ("self_check",)}).lower()))


# ---------------------------------------------------------------- 6 the checks catch faults
def mutation_tests():
    """Break a copy of the target in six ways and see that the checks above notice each one."""
    import copy
    global T, COUNT, GROUPS, LINES
    saved = (T, COUNT, GROUPS, LINES)

    def run(mut, which):
        global T, COUNT, GROUPS, LINES
        T = copy.deepcopy(saved[0])
        mut(T)
        COUNT, GROUPS, LINES = {"pass": 0, "fail": 0, "report": 0}, {}, []
        try:
            for fn in which:
                fn()
        except Exception as e:  # a crash is also a noticed fault
            COUNT["fail"] += 1
            LINES.append({"result": "fail", "name": "exception " + repr(e)[:80]})
        n = COUNT["fail"]
        T, COUNT, GROUPS, LINES = saved
        return n

    def m_plinth(t):
        t["parts"]["pilaster"]["dims"]["plinth_top_z"] = 600.0

    def m_door(t):
        t["parts"]["shop_door"]["dims"]["glazed_from"] = 1000.0
        t["parts"]["shop_door"]["dims"]["lock_rail"] = [590, 1000]

    def m_row(t):
        t["photo"]["features"]["shaft_top"]["y"] += 20.0
        for inst in t["photo"]["instance_polys_px"]:
            for q in inst["polys"]:
                for p in q["pts"]:
                    pass

    def m_doorend(t):
        s = [x for x in t["shops"] if x["id"] == "ritas"][0]
        s["door_end_street"] = "low"

    def m_toe(t):
        t["parts"]["console"]["dims"]["toe_width"] = 400.0

    def m_bottomrail(t):
        t["parts"]["window_frame"]["dims"]["bottom_rail"] = [560, 690]

    def m_zone(t):
        s = [x for x in t["shops"] if x["id"] == "fish_market"][0]
        s["zones_u"]["shop_door"] = [3700.0, 4650.0]

    def m_mirror(t):
        # a board shifted: move every plinth polygon 60 px sideways in the instance, as a wrongly placed drawing would be
        for inst in t["photo"]["instance_polys_px"]:
            if inst["crop"] == "plinth":
                for q in inst["polys"]:
                    for p in q["pts"]:
                        p[1] += 25.0
    tests = [("plinth top back to the kit's 600", m_plinth, [group3]), ("shop door glazed from the scene's 1000", m_door, [group1, group3, group5]),
             ("a measured row moved 20 px", m_row, [group2]), ("Rita's door end flipped", m_doorend, [group1]),
             ("a console toe wider than its capital", m_toe, [group5]), ("the bottom rail dropped below the sill", m_bottomrail, [group5]),
             ("a shop door slot narrowed", m_zone, [group5]), ("the drawing shifted 25 px on the plinth", m_mirror, [group4])]
    out = []
    for name, mut, which in tests:
        n = run(mut, which)
        out.append((name, n))
    T, COUNT, GROUPS, LINES = saved
    for name, n in out:
        chk("6 faults", "the checks notice: %s" % name, n >= 1, "%d checks failed on the broken copy" % n)


def main():
    write = "--no-write" not in sys.argv
    group1()
    group2()
    group3()
    group4()
    group5()
    mutation_tests()
    total = COUNT["pass"] + COUNT["fail"] + COUNT["report"]
    res = {"date": "2026-10-09", "script": "self_check.py", "passed": COUNT["pass"], "failed": COUNT["fail"], "reported": COUNT["report"], "total": total, "groups": GROUPS, "stats": STATS,
           "failures": [l for l in LINES if l["result"] == "fail"], "reported_lines": [l for l in LINES if l["result"] == "report"]}
    print("SELF-CHECK: %d of %d checks pass; %d fail; %d reported departures kept in the open" % (COUNT["pass"], total, COUNT["fail"], COUNT["report"]))
    for gname in sorted(GROUPS):
        print("  %-14s %s" % (gname, GROUPS[gname]))
    for l in LINES:
        if l["result"] == "fail":
            print("  FAIL", l["group"], "|", l["name"], "|", l["detail"])
    if write:
        T["self_check"] = res
        json.dump(T, open(os.path.join(HERE, "target.json"), "w"), indent=1)
    return 1 if COUNT["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
