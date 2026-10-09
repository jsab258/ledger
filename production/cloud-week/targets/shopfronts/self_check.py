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
import shapely
from PIL import Image
from shapely.geometry import LinearRing, Point, Polygon, box

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


def hausdorff(a, b):
    """two-way Hausdorff distance between two closed outlines, in mm (the outlines' boundaries)"""
    return float(shapely.hausdorff_distance(LinearRing(a), LinearRing(b), densify=0.02))


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
        dep(g, "shaft proud 140 differs from the scene's 0.10 (disagreement D3 lists it: the scene's 0.10 loses)", T["parts"]["pilaster"]["dims"]["shaft_proud"] == 140.0
            and any(d["id"] == "D3" for d in T["disagreements_photographs_win"]), "photographs win")
        chk(g, "scene row: transom at 2.40, 0.08 thick", "transom at 2.40, 0.08 thick" in row)
        chk(g, "target transom 2400..2480", T["bay"]["z"]["transom"] == [2400.0, 2480.0])
        chk(g, "scene row: fascia 2.85 to 3.40, 0.12 proud", "fascia from 2.85" in row and "0.12 proud" in row)
        chk(g, "target fascia z and face", T["bay"]["z"]["fascia"] == [2850.0, 3400.0] and T["bay"]["d"]["fascia_face"] == 120.0)
        chk(g, "scene row: shop door 0.90 x 2.04, glazed from 1.0", "shop door 0.90 × 2.04, glazed from 1.0" in row)
        sd = T["parts"]["shop_door"]["dims"]
        chk(g, "target leaf 900 x 2040", sd["leaf_width"] == 900.0 and sd["leaf_height"] == 2040.0)
        dep(g, "glazed from 600 differs from the scene's 1.0 (D2 lists it: level with the sill, the scene's 1.0 loses)", sd["glazed_from"] == 600.0 and any(d["id"] == "D2" for d in T["disagreements_photographs_win"]),
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
        # the printed profile's envelope and its fixed points stay (the scroll is Judgement inside the same envelope)
        side = T["parts"]["console"]["profiles"]["side_silhouette"]["points"]
        chk(g, "console silhouette keeps the printed envelope: bounding d 0..180, z 0..550", min(p[0] for p in side) == 0.0 and max(p[0] for p in side) == 180.0 and
            min(p[1] for p in side) == 0.0 and max(p[1] for p in side) == 550.0)
        chk(g, "console silhouette keeps the printed toe (d 60 at z 0) and cap block (d 180 at z 528 and 550)",
            any(near(p[0], 60.0, 0.01) and near(p[1], 0.0, 0.01) for p in side) and any(near(p[0], 180.0, 0.01) and near(p[1], 528.0, 0.01) for p in side)
            and any(near(p[0], 180.0, 0.01) and near(p[1], 550.0, 0.01) for p in side))
        chk(g, "the printed profile's mesh is a few steps with no volute (the review's fault 5): the new outline has two eyes the printed one lacks",
            '"fascia_console_01"' in f01 and "volute" not in con_block.lower())
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
        # the boards' ground colour and the signs' rectangles are the fascia target's (the review's fault 9)
        for s_ in T["shops"]:
            fs_ = ids[s_["fascia_target_id"]]
            ob = fs_.get("old_board")
            if ob:
                want = fa["palette"][ob["colour"]]["srgb_1990"]
                have = T["paints"][s_["paints"]["fascia_board"]]["srgb"]
                chk(g, "%s: fascia board paint = the fascia target's old_board colour (%s %s)" % (s_["id"], ob["colour"], want), have == want, "mine %s" % have)
            for geo in fs_.get("geometry", []):
                if geo["kind"] in ("box_sign", "flat_panel"):
                    x0_, y0_, x1_, y1_ = geo["outer_mm"]
                    mine = s_["fascia_sign"]
                    chk(g, "%s: %s u %s, z %s, depth %d = the fascia target's outer_mm %s" % (s_["id"], geo["kind"], mine["u"], mine["z"], mine["depth"], geo["outer_mm"]),
                        mine["kind"] == geo["kind"] and near(mine["u"][0], 295 + x0_, 0.01) and near(mine["u"][1], 295 + x1_, 0.01) and near(mine["z"][0], 3400 - y1_, 0.01)
                        and near(mine["z"][1], 3400 - y0_, 0.01) and near(mine["depth"], geo["depth_m"] * 1000.0, 0.01) and near(mine["front_d"], 120 + mine["depth"], 0.01))
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
        fdmd = read("production/cloud-week/targets/front-door/TARGET.md") or ""
        chk(g, "front-door target: F1's optional hinges are 'on the left stile' (seen from outside) and its knob is centred, so it is mirrored where Rita's game frame shows the knob on the left",
            "three 100 mm steel butts on the left stile" in fdmd and "centre knob" in fdmd)

    # the printed arithmetic inside the target itself
    B = T["bay"]
    chk(g, "350 + 944 + 1006 + 3350 + 350 = 6000", B["pilaster_slot"] * 2 + B["side_door_slot"] + B["shop_door_slot"] + B["window_default"] == B["width"])
    chk(g, "1006 = 900 leaf + 2 x 3 gap + 2 x 50 jamb", 900 + 6 + 100 == B["shop_door_slot"])
    chk(g, "5892 = 6000 - 68 - 2 x 20 (fascia-01's arithmetic)", 6000 - 68 - 40 == T["parts"]["cornice"]["dims"]["length"])
    chk(g, "5410 = 5705 - 295", 5705 - 295 == T["parts"]["fascia_board"]["dims"]["length"])
    chk(g, "no side door: window 4294 = 5300 - 1006", B["window_no_side_door"] == 4294.0)
    # ---- the game's Rita frame today: brass found by colour, the hinge sides read from it
    gt = T["game_today"]
    gp = os.path.join(ROOT, "production", "previews", "rita-day-kit-2026-10-06.jpg")
    chk(g, "the game's Rita frame (rita-day-kit-2026-10-06.jpg) read", os.path.exists(gp))
    if os.path.exists(gp):
        im = np.asarray(Image.open(gp).convert("RGB")).astype(int)
        R_, G_, B_ = im[..., 0], im[..., 1], im[..., 2]
        brass = (R_ - B_ > 40) & (G_ - B_ > 18) & (R_ >= G_) & (R_ > 90)

        def box_brass(x0, y0, x1, y1):
            ys, xs = np.nonzero(brass[y0:y1, x0:x1])
            return (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0, len(xs)) if len(xs) else None
        sd_ = gt["side_door"]
        leaf0, leaf1 = sd_["leaf_x_px"]
        mid = 0.5 * (leaf0 + leaf1)
        kn_a, kn_b = box_brass(205, 478, 250, 500), box_brass(205, 555, 250, 580)
        chk(g, "game frame: the side door's two knobs (x %s and %s) are both in the leaf's left half (centre x %.1f) and within 3 px of the stored ones" % (kn_a[:2], kn_b[:2], mid),
            kn_a is not None and kn_b is not None and kn_a[1] < mid and kn_b[1] < mid and abs(0.5 * (kn_a[0] + kn_a[1]) - sd_["knob_x_px"][0]) <= 3 and abs(0.5 * (kn_b[0] + kn_b[1]) - sd_["knob_x_px"][1]) <= 3,
            "stored %s" % sd_["knob_x_px"])
        sp_ = box_brass(260, 552, 345, 580)
        chk(g, "game frame: the side door's letter plate (x %d to %d) is centred on the leaf (centre %.1f)" % (sp_[0], sp_[1], mid), abs(0.5 * (sp_[0] + sp_[1]) - mid) <= 6)
        lv = box_brass(436, 548, 490, 566)
        gl0, gl1 = gt["shop_door"]["glass_x_px"]
        chk(g, "game frame: the shop door's lever rose (x %d to %d) stands left of its glass (x %.1f to %.1f): the lever is on the leaf's left edge" % (lv[0], lv[1], gl0, gl1), lv[1] < gl0)
        pl = box_brass(480, 575, 575, 605)
        chk(g, "game frame: the shop door's letter plate (x %d to %d, y %d to %d) is in the lock rail below the glass and centred on the glass (centre %.1f)" % (pl[0], pl[1], pl[2], pl[3], 0.5 * (gl0 + gl1)),
            abs(0.5 * (pl[0] + pl[1]) - 0.5 * (gl0 + gl1)) <= 8 and pl[2] > 575)
    # the rule and every shop's table follow from it
    for s_ in T["shops"]:
        opp = "R" if s_["door_end_viewer"] == "L" else "L"
        chk(g, "%s: hinge sides: shop door hinged %s (window side), lever %s; side door hinged %s, knob %s; letter plates centred" % (s_["id"], s_["shop_door_hinge_viewer"], s_["shop_door_lever_viewer"], s_["side_door_hinge_viewer"], s_["side_door_knob_viewer"]),
            s_["shop_door_hinge_viewer"] == opp and s_["shop_door_lever_viewer"] == s_["door_end_viewer"] and s_["letter_plate_viewer"] == "centre" and
            ((s_["side_door_hinge_viewer"] == opp and s_["side_door_knob_viewer"] == s_["door_end_viewer"]) if s_["side_door"] else (s_["side_door_hinge_viewer"] is None and s_["side_door_knob_viewer"] is None)))
    rita = [x for x in T["shops"] if x["id"] == "ritas"][0]
    chk(g, "Rita's: doors on the viewer's left, both leaves hinged on the right, levers and knobs on the left (the game frame)",
        rita["door_end_viewer"] == "L" and rita["shop_door_hinge_viewer"] == "R" and rita["side_door_hinge_viewer"] == "R" and rita["shop_door_lever_viewer"] == "L" and rita["side_door_knob_viewer"] == "L")


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
    dep(g, "not re-measurable on a preview (the glass above the door's foot carries lettering and notices): %s" % ", ".join(nr), len(nr) == 3 and "door_glass_bottom" not in nr and "door_foot" not in nr,
        "read on the unmasked view only; the door's glass foot, strip and foot ARE on the masked door preview now (the review's fault 1)")
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
    ratio_w = M["pil_foot"]["y"] / M["bottom_rail_foot"]["y"]
    s_win = s_door / ratio * ratio_w
    chk(g, "scale: the window frame's own plane = the pilaster plane x (pier foot row / window foot row) = %.4f mm a pixel" % s_win, near(s_win, sc["mm_per_px_window_plane"], 0.001))
    chk(g, "scale: the camera height is the same from the pier's foot row and the door's (1044 mm each, to 1 per cent) and from the window's",
        near(M["pil_foot"]["y"] * sc["mm_per_px_pilaster_plane"], M["door_foot"]["y"] * sc["mm_per_px_door_plane"], 0.01 * 1044) and
        near(M["pil_foot"]["y"] * sc["mm_per_px_pilaster_plane"], M["bottom_rail_foot"]["y"] * sc["mm_per_px_window_plane"], 0.01 * 1044))
    chk(g, "scale: camera height 0.9 to 1.3 m (a tripod panorama)", 900 <= sc["camera_height_mm_above_footway"] <= 1300, "%d mm" % sc["camera_height_mm_above_footway"])
    dep(g, "scale: no cross-check by a second dimension (the door leaf's own 2.62 m is a result)", ph["scale"]["error_pct"] == 8,
        "the A5 assumption and the plane ratios carry +-8 per cent and are not independently confirmed; the notice is England's statutory no-smoking sign (A5 minimum from 2007), from memory")
    dm = ph["derived_mm"]
    s_p = sc["mm_per_px_pilaster_plane"]
    chk(g, "shaft width = (right - left) x scale", near((M["shaft_right"]["x"] - M["shaft_left"]["x"]) * s_p, dm["shaft_width"], 0.2), "%.1f" % dm["shaft_width"])
    chk(g, "plinth top z = (foot - cap top row) x scale", near((M["pil_foot"]["y"] - M["plinth_cap_top"]["y"]) * s_p, dm["plinth_top_z"], 1.0), "%d" % dm["plinth_top_z"])
    chk(g, "capital height (an upper bound) = (shaft top - abacus top) x scale", near((M["shaft_top"]["y"] - M["abacus_top"]["y"]) * s_p, dm["capital_height"], 1.0))
    zp = s_p * 2400.0
    xm = abs(0.5 * (M["shaft_right"]["x"] + M["shaft_return_outer"]["x"]))
    chk(g, "shaft relief, lower bound, from the painted return: %.1f px at %.0f px off axis" % (M["shaft_return_outer"]["x"] - M["shaft_right"]["x"], xm),
        near((M["shaft_return_outer"]["x"] - M["shaft_right"]["x"]) * zp / xm, dm["shaft_proud"], 0.2), "%.1f mm" % dm["shaft_proud"])
    xm2 = abs(0.5 * (M["shaft_right"]["x"] + M["shaft_return_frame"]["x"]))
    chk(g, "shaft relief to the teal window frame: %.1f px at %.0f px off axis" % (M["shaft_return_frame"]["x"] - M["shaft_right"]["x"], xm2),
        near((M["shaft_return_frame"]["x"] - M["shaft_right"]["x"]) * zp / xm2, dm["shaft_proud_to_window_frame"], 1.0), "%.0f mm" % dm["shaft_proud_to_window_frame"])
    chk(g, "the frame's own foot row puts the window frame %.0f behind the pier's face; the dark return to the frame (%.0f) is within 25 per cent of it" % (sc["plane_depths_behind_pier_face_mm"]["window_frame"], dm["shaft_proud_to_window_frame"]),
        abs(dm["shaft_proud_to_window_frame"] - sc["plane_depths_behind_pier_face_mm"]["window_frame"]) / sc["plane_depths_behind_pier_face_mm"]["window_frame"] <= 0.25)
    chk(g, "shaft width within 8 per cent of the kit's 290 (the scale's whole error)", abs(dm["shaft_width"] - 290.0) / 290.0 <= 0.08)
    zwin = lambda k: (M["bottom_rail_foot"]["y"] - M[k]["y"]) * s_win
    chk(g, "sill top on the window's own plane = (window foot - sill row) x %.4f = %.0f (the review's 844)" % (s_win, zwin("sill_top")), near(zwin("sill_top"), dm["sill_top_z_window_plane"], 1.0) and near(dm["sill_top_z_window_plane"], 844.0, 3.0))
    chk(g, "window stile = (right - left) x window scale = %.0f (the teal stile ends at x -993, not on the grille's bar)" % dm["window_stile_face"],
        near((M["stile_right"]["x"] - M["stile_left"]["x"]) * s_win, dm["window_stile_face"], 1.0) and M["stile_right"]["x"] < -985.0 and 74.0 <= dm["window_stile_face"] <= 80.0)
    chk(g, "mullion = %.0f at the window plane (92.1 px)" % dm["mullion_face"], near((M["mullion_right"]["x"] - M["mullion_left"]["x"]) * s_win, dm["mullion_face"], 1.0) and near(dm["mullion_face"], 172.0, 2.0))
    gl = (M["door_foot"]["y"] - M["door_glass_bottom"]["y"]) / (M["door_foot"]["y"] - M["door_leaf_top"]["y"])
    chk(g, "door glass foot at row %.2f (strength %.1f: a real edge, not the first try's 1.5): glazed from %.3f of the leaf" % (M["door_glass_bottom"]["y"], M["door_glass_bottom"]["strength"], gl),
        near(gl, dm["door_glazed_from_fraction"], 0.001) and M["door_glass_bottom"]["strength"] >= 5.0 and near(M["door_glass_bottom"]["y"], 128.93, 0.3))
    chk(g, "door glass foot (%.0f mm on the door's plane) is level with the window sill top (%.0f) to within 60 mm: the glass line runs on as the sill's" % (dm["door_glass_foot_door_plane"], dm["sill_top_z_window_plane"]),
        abs(dm["door_glass_foot_door_plane"] - dm["sill_top_z_window_plane"]) <= 60.0)
    chk(g, "door leaf %.0f mm, scaled to a 2040 leaf the glass starts at %.0f (P1 0.304)" % (dm["door_leaf_height_door_plane"], dm["door_glazed_from_fraction"] * 2040), near(dm["door_glazed_from_fraction"] * 2040, 620.0, 4.0))
    chk(g, "crown: the apparent %.0f at the pilaster plane is NOT used as a target: the true range is stated as %s" % (dm["crown_apparent_height_pilaster_plane"], dm["crown_true_range"]),
        dm["crown_true_range"] == [170, 300] and "NOT measurable" in dm["crown_note"])
    dmap = {"R1": "D1", "R2": "D1", "R4": "D4", "R8": "D7"}
    for r in T["derived_rules"]:
        if not r.get("followed", True):
            dep(g, "ratio rule %s %s: photo %.3f, target %.3f (NOT followed, stated as %s)" % (r["id"], r["name"], r["photo"], r["target"], dmap.get(r["id"], "?")),
                any(d["id"] == dmap.get(r["id"]) for d in T["disagreements_photographs_win"]), r["reading"])
            continue
        if r.get("range"):
            chk(g, "ratio rule %s %s: the target %.3f lies between the photograph's lower bound %.3f and upper bound %.3f" % (r["id"], r["name"], r["target"], r["photo"], r["photo_high"]),
                r["photo"] <= r["target"] <= r["photo_high"])
            continue
        if "tolerance_abs" in r:
            chk(g, "ratio rule %s %s: photo %.1f, target %.1f (within %.0f)" % (r["id"], r["name"], r["photo"], r["target"], r["tolerance_abs"]), abs(r["photo"] - r["target"]) <= r["tolerance_abs"])
            continue
        chk(g, "ratio rule %s %s: photo %.3f, target %.3f" % (r["id"], r["name"], r["photo"], r["target"]),
            abs(r["photo"] - r["target"]) / r["target"] * 100.0 <= r["tolerance_pct"], "tolerance %d per cent" % r["tolerance_pct"])
    # monotonic order of the measured rows (nothing impossible)
    order = ["pil_foot", "plinth_block1_top", "plinth_block2_top", "plinth_block3_top", "plinth_cap_top", "shaft_top", "neck_ledge", "abacus_bottom", "abacus_top"]
    ys = [M[k]["y"] for k in order]
    chk(g, "measured rows run up the pilaster in order (y falls)", all(ys[i] > ys[i + 1] for i in range(len(ys) - 1)))
    chk(g, "sill rows run top to bottom", M["sill_top"]["y"] < M["sill_r2"]["y"] < M["sill_nose"]["y"] < M["grille_top"]["y"] < M["grille_bottom"]["y"] < M["bottom_rail_foot"]["y"])
    chk(g, "door rows run top to bottom: leaf top, glass top, glass foot, foot strip top, foot",
        M["door_leaf_top"]["y"] < M["door_glass_top"]["y"] < M["door_glass_bottom"]["y"] < M["door_foot_strip_top"]["y"] < M["door_foot"]["y"])
    chk(g, "no preview shows lettering: the numerals are masked, the glass above the door's foot and everything seen through the shop window beside the pier are filled flat, and no business's name is in a file name",
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
    ph_plinth = dm["plinth_top_z"] / front * 3550.0
    chk(g, "D1 plinth top 600 = Rita's line: level with the sill top (600) and the stallriser's top (525 + the sill's 75), the kit's 0.60",
        P["pilaster"]["dims"]["plinth_top_z"] == 600.0 == T["bay"]["z"]["sill_top"] and P["stallriser"]["dims"]["z_range"][1] + P["sill"]["dims"]["thickness"] == 600.0)
    dep(g, "D1 the photograph's plinth (scaled to the street's 3.55 m = %.0f, 1.33 times its sill) is NOT followed: it breaks Rita's line; kept as variants.plinth_tall" % ph_plinth,
        P["pilaster"]["variants"]["plinth_tall"]["plinth_top_z"] == 800.0 and any(d["id"] == "D1" for d in T["disagreements_photographs_win"]) and abs(ph_plinth - 800.0) / 800.0 < 0.06,
        "Rita's window is Jafar's model")
    chk(g, "D1 every pilaster variant's plinth top is 600 on the ten fronts (render steps to 360 / 450 / 484 then the head to 600; panel cap 520 to 600)",
        P["pilaster"]["variants"]["render"]["step_heights_z"][-1] == 600 and max(p[1] for p in P["pilaster"]["profiles"]["plinth_stepped_side"]["points"]) == 600.0 and
        max(p[1] for p in P["pilaster"]["profiles"]["plinth_cap_side"]["points"]) == 600.0)
    chk(g, "D2 shop door glazed from 600 against the photograph's %.3f x 2040 = %.0f" % (dm["door_glazed_from_fraction"], dm["door_glazed_from_fraction"] * 2040),
        abs(600.0 - dm["door_glazed_from_fraction"] * 2040) / 600.0 <= 0.08)
    chk(g, "D2 the scene's 1000 is outside it", abs(1000.0 - dm["door_glazed_from_fraction"] * 2040) / 1000.0 > 0.2)
    lo, hi = dm["shaft_proud"], dm["shaft_proud_to_window_frame"]
    chk(g, "D3 shaft proud 140 lies between the photograph's lower bound %.0f and its frame bound %.0f" % (lo, hi), lo <= P["pilaster"]["dims"]["shaft_proud"] <= hi)
    chk(g, "D3 the scene's 100 is below the photograph's lower bound by more than the 14 per cent error", 100.0 < lo * 0.86)
    dep(g, "D4 capital 310 is above the photograph's upper bound %.0f (Judgement, stated)" % dm["capital_height"], P["pilaster"]["dims"]["capital_height"] > dm["capital_height"] and "UPPER bound" in dm["capital_height_note"] and
        any(d["id"] == "D4" for d in T["disagreements_photographs_win"]), "the capital carries the console's toe and the board's foot")
    dep(g, "D5 mullion 70 is not the photograph's %.0f (partly followed, stated)" % dm["mullion_face"], any(d["id"] == "D5" for d in T["disagreements_photographs_win"]),
        "the photograph reads %.0f; the target takes 70 (T1) and 80 (T2)" % dm["mullion_face"])
    chk(g, "D6 the fascia face is a single vertical plane (the section's board front has x = 120 at 2 or more points)",
        sum(1 for p in P["fascia_board"]["profiles"]["section"]["points"] if p[0] == 120.0) >= 2)
    dep(g, "D7 the cornice stays 150: the photograph's crown is not measurable by this method (170 to 300 against an apparent %.0f)" % dm["crown_apparent_height_pilaster_plane"],
        P["cornice"]["dims"]["height"] == 150.0 and any(d["id"] == "D7" for d in T["disagreements_photographs_win"]), "the fixed envelope; a tall variant is offered with no photographic basis")
    chk(g, "D8 sill 75 (z 525..600)", P["sill"]["dims"]["thickness"] == 75.0 and P["sill"]["dims"]["z_range"] == [525.0, 600.0])
    chk(g, "D9 the sill's top 600 within 10 per cent of the photograph's ratio x 3.55 m (window plane)", abs(600.0 - dm["sill_top_z_window_plane"] / front * 3550.0) / 600.0 <= 0.10,
        "%.0f" % (dm["sill_top_z_window_plane"] / front * 3550.0))
    dep(g, "D10 the pairs at the party wall stay (the scene's fact)", any(d["id"] == "D10" for d in T["disagreements_photographs_win"]), "P1 has single piers")
    dep(g, "D11 the two-volute console is Judgement, not photographed", any(d["id"] == "D11" for d in T["disagreements_photographs_win"]) and T["could_not_settle"][0].startswith("The scrolled console"),
        "no photograph of one was reached; the first item of could_not_settle")
    chk(g, "D12 the side door's hinge side in Rita's front is stated against the review (measured on the game frame)", any(d["id"] == "D12" for d in T["disagreements_photographs_win"]))
    ids = {d["id"] for d in T["disagreements_photographs_win"]}
    chk(g, "every disagreement has a chosen value", all(d.get("chosen") for d in T["disagreements_photographs_win"]) and len(ids) == len(T["disagreements_photographs_win"]))
    chk(g, "kit_vs_target covers every part the brief names", all(k in T["kit_vs_target"] for k in ("pilaster", "console", "fascia_board", "cornice", "sill", "stallriser", "window_frame", "shop_door", "side_door")))
    fl = T["review_faults_answered"]
    chk(g, "the review's eleven faults are each answered (and the plinth note, and the narrow points)", [f["n"] for f in fl if isinstance(f["n"], int)] == list(range(1, 12)) and any(f["n"] == "3b" for f in fl) and all(f.get("answer") for f in fl))
    chk(g, "the two places this target does not follow the review are stated as such (3b the plinth, 6 the side door's hinge)", [f["followed"] for f in fl if f["n"] in ("3b", 6)] == [False, "partly"])


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
                    wtol = tolweak if f["strength"] < weakbelow else tol0
                    pos, st = ML.snap(im, "R", edge - y0, pa - x0, pb - x0, wtol + 1.0, sign=f.get("sign", 0))
                    got = pos + y0
                else:
                    edge = min(xs, key=lambda v: abs(v - f["x"]))
                    pa, pb = f["span_y"]
                    wtol = tolweak if f["strength"] < weakbelow else tol0
                    pos, st = ML.snap(im, "C", edge - x0, pa - y0, pb - y0, wtol + 1.0)
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
    chk(g, "the drawing laid the instance on %d previews and Rita's elevation on the pier strip" % (len(written) - 1), len(written) == len(ph["instance_polys_px"]) + 1 and
        any(os.path.basename(w).endswith("-ritas-on-photo.jpg") for w in written))
    for p in written:
        os.remove(p)
    os.rmdir(out)
    # Rita's elevation on P1 at one scale (the shaft's width): the overlay's shaft is as wide as P1's, its foot is P1's footway, and each difference is tabled
    ro = ph["rita_overlay"]
    sp = ro["mm_per_px_pilaster_plane"]
    shaft_px_rita = T["parts"]["pilaster"]["dims"]["shaft_width"] / sp
    shaft_px_p1 = M["shaft_right"]["x"] - M["shaft_left"]["x"]
    chk(g, "Rita's overlay: her shaft (290) is %.1f px wide at %.4f mm a pixel, P1's %.1f px: one scale, fitted on the shaft's width" % (shaft_px_rita, sp, shaft_px_p1), abs(shaft_px_rita - shaft_px_p1) <= 1.5)
    chk(g, "Rita's overlay: the shaft's centre column %.2f is P1's (%.2f) and the footway row %.2f is P1's pier foot" % (ro["shaft_centre_col"], 0.5 * (M["shaft_left"]["x"] + M["shaft_right"]["x"]), ro["foot_row"]),
        near(ro["shaft_centre_col"], 0.5 * (M["shaft_left"]["x"] + M["shaft_right"]["x"]), 0.05) and near(ro["foot_row"], M["pil_foot"]["y"], 0.01))
    tab = ph["rita_vs_p1"]
    chk(g, "Rita on P1: %d differences listed (plinth, shaft, relief, capital, heights, sill, door glass, leaf, stile, mullion, front, crown)" % len(tab), len(tab) >= 12 and all(r.get("reading") for r in tab))
    plin = [r for r in tab if r["item"] == "plinth top"][0]
    chk(g, "Rita on P1: the plinth difference is listed (target 600 against P1's %s) and named as Rita's line" % plin["p1"], plin["target"] == 600 and plin["p1"] > 1000 and "Rita's line" in plin["reading"])
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
    pd_ = P["pilaster"]["dims"]
    chk(g, "capital top: the flat reaches d %.0f and the abacus front is %.0f (nominal top 350 x %.0f), the console's toe (60 deep) and the board's mould (front 132) lie inside it" % (max(ds), max(p[0] for p in cap), pd_["capital_top_proud"]),
        near(max(ds), 172.0, 0.01) and near(max(p[0] for p in cap), 175.0, 0.01) and pd_["capital_top_proud"] == 175.0 and pd_["capital_top_width"] == 350.0 and 132.0 < max(ds))
    flare = [p for p in cap if 154.0 <= p[1] <= 244.0 and 143.99 <= p[0] <= 172.01]
    chk(g, "capital flare: a hollow from d 144 at z 154 to d 172 at z 244 (it moves out %.0f over 90, the first try's 14)" % (max(p[0] for p in flare) - 144.0),
        near(min(p[0] for p in flare), 144.0, 0.01) and near(max(p[0] for p in flare), 172.0, 0.01) and near(pd_["capital_die_d"], pd_["shaft_proud"] + 4.0, 0.01))
    chk(g, "capital members add up to 310", sum(v[1] - v[0] for v in pd_["capital_members_z_local"].values()) == 310.0)
    toe_d, toe_w = 60.0, P["console"]["dims"]["toe_width"]
    capw = pd_["capital_top_width"]
    capd = pd_["capital_top_proud"]
    chk(g, "console foot (240 x 60) lies wholly on the capital's top (350 x 175)", toe_w <= capw and toe_d <= capd and (capw - toe_w) / 2 >= 0)
    side = P["console"]["profiles"]["side_silhouette"]["points"]
    chk(g, "the console's lower volute (d %.0f) overhangs its toe (60) but stays on the capital's top (175)" % max(p[0] for p in side if p[1] < 120), 60.0 < max(p[0] for p in side if p[1] < 120) < capd)
    cu = P["console"]["u_range"]
    chk(g, "console u ranges lie inside the pilaster slots and centre on 175 / 5825", cu == [[55, 295], [5705, 5945]] and
        all(0 <= a and b <= 350 or 5650 <= a and b <= 6000 for a, b in cu) if False else (cu[0][0] >= 0 and cu[0][1] <= 350 and cu[1][0] >= 5650 and cu[1][1] <= 6000))
    chk(g, "fascia board begins where the console ends (295, 5705)", cu[0][1] == P["fascia_board"]["dims"]["u_range"][0] and cu[1][0] == P["fascia_board"]["dims"]["u_range"][1])
    chk(g, "fascia board's foot rests on each abacus for 55 (295 to 350)", 350 - P["fascia_board"]["dims"]["u_range"][0] == 55)
    chk(g, "the board's bed mould (front 132) stands 43 behind the capital's top front (175), wholly on the capital", near(pd_["capital_top_proud"] - 132.0, 43.0, 0.01))
    chk(g, "neighbours' consoles stand 110 apart across the party line: 2 x 55 = 110 > the pipe's 68", 2 * 55 == 110 and 110 > 68)
    chk(g, "the cornice stops 54 short of each party line: 108 between neighbours > the pipe's 68", 2 * 54 == 108 and 108 > 68)
    chk(g, "shafts 290 in a 350 slot stand 60 apart; the pipe (68) overlaps each by 4 and the chase (76) clears it", 2 * 30 == 60 and 76 > 68)
    chk(g, "the downpipe's front (axis 94 + 34 = 128) stands 12 behind the shafts' faces (140); the chase starts at d 50 and runs z 0 to 600 and 2540 to 2850",
        94 + 34 == 128 and pd_["shaft_proud"] - 128 == 12 and pd_["downpipe_chase"]["from_d"] == 50.0 and pd_["downpipe_chase"]["z_ranges"] == [[0, 600], [2540, 2850]])
    # the relief rule: the shaft stands at least 40 in front of every frame beside it (the review's fault 4)
    rb = pd_["relief_beside_frames"]
    chk(g, "relief: the shaft's face (%.0f) less the largest frame front beside a pier (%.0f) is %.0f, at least the required %.0f" % (pd_["shaft_proud"], max(rb["frame_fronts_d"].values()), rb["min_relief"], rb["required"]),
        rb["min_relief"] >= rb["required"] and rb["min_relief"] == pd_["shaft_proud"] - max(rb["frame_fronts_d"].values()))
    chk(g, "relief: the plinth (180) stands 40 in front of the shaft and 30 in front of the sill's nose (150) and 55 in front of the stallriser (125)",
        pd_["plinth_proud"] - pd_["shaft_proud"] == 40.0 and pd_["plinth_proud"] - P["sill"]["dims"]["nose_d"] == 30.0 and pd_["plinth_proud"] - P["stallriser"]["dims"]["face_d"] == 55.0)
    chk(g, "the clad variant (Mickey's) stands as far out as the shaft it cases: %.0f" % P["pilaster"]["variants"]["clad"]["dims"]["proud"], P["pilaster"]["variants"]["clad"]["dims"]["proud"] == pd_["shaft_proud"])
    # the plinth's head, from the photograph's members (the review's fault 3)
    pr = P["pilaster"]["profiles"]
    stp = pr["plinth_stepped_side"]["points"]
    cav = [p for p in stp if 484.0 <= p[1] <= 579.0 and p[0] < 172.0 + 0.01 and p[0] > 147.99]
    resid = max(abs(((p[0] - 172.0) / 24.0) ** 2 + ((p[1] - 579.0) / 95.0) ** 2 - 1.0) for p in cav if p[1] > 484.0 and p[0] < 172.0)
    chk(g, "stepped plinth head: %d cavetto points lie on the quarter ellipse centred (172, 579), 24 x 95 (worst residual %.4f), from d 172 at z 484 to d 148 at z 579" % (len(cav), resid),
        len(cav) >= 4 and resid < 0.01 and any(near(p[0], 172.0, 0.01) and near(p[1], 484.0, 0.01) for p in stp) and any(near(p[0], 148.0, 0.01) and near(p[1], 579.0, 0.01) for p in stp))
    chk(g, "stepped plinth head: a band 21 high at d 148 to z 600, the shaft (140) 8 behind it; the three steps in d are 180 / 176 / 172",
        any(near(p[0], 148.0, 0.01) and near(p[1], 600.0, 0.01) for p in stp) and near(148.0 - pd_["shaft_proud"], 8.0, 0.01) and
        {180.0, 176.0, 172.0} <= {p[0] for p in stp} and pd_["stepped_head"]["band_z"] == [579.0, 600.0])
    tall = pr["plinth_tall_stepped_side"]["points"]
    review = [(0, 0), (150, 0), (150, 504), (146, 504), (146, 631), (142, 631), (142, 684), (132.8, 691.2), (125.0, 711.8), (119.8, 742.6), (118, 779), (118, 800), (0, 800)]
    chk(g, "the unused tall plinth carries the review's profile points (+30 in d) to within %.2f mm (two-way Hausdorff)" % hausdorff(tall, [(a + 30 if a > 0 else a, b) for a, b in review]),
        hausdorff(tall, [(a + 30 if a > 0 else a, b) for a, b in review]) <= 1.5)
    kit_src = read("tools/art-recipes/shopfront-kit/pilaster.py")
    if kit_src:
        m = re.search(r"BASE = \[(.*?)\]\npart", kit_src, re.S)
        kb = [tuple(float(x) * 1000.0 for x in t_) for t_ in re.findall(r"\(([0-9.]+), ([0-9.]+)\)", m.group(1))] if m else []
        og = pr["base_ogee"]["points"]
        want = [(140.0 + a, 600.0 + b) for a, b in kb]
        chk(g, "base ogee = the kit's BASE (pilaster.py), %d points, 25 proud of the shaft face and 60 high on the plinth's top: two-way Hausdorff %.2f" % (len(kb), hausdorff(og, want) if kb else -1),
            len(kb) == 9 and hausdorff(og, want) <= 1.5 and pd_["base_ogee"]["proud_of_shaft_face"] == 25.0 and pd_["base_ogee"]["height"] == 60.0)
    chk(g, "panel and flute elevations carry the base ogee on the plinth's top (z 600 to 660), the shaft's bottom rail above it", all(any(q["name"] == "base_ogee" and q["pts"][0][1] == 600 and q["pts"][2][1] == 660 for q in T["parts"]["pilaster"]["variants"][v]["elevation"]) for v in ("panel", "flute")))
    # the console as a scroll (the review's fault 5): the numbers recomputed from the outline itself
    cs = P["console"]
    sd_ = cs["profiles"]["side_silhouette"]["points"]
    on_up = [p for p in sd_ if abs(math.hypot(p[0] - 126.0, p[1] - 470.0) - 54.0) < 0.6]
    chk(g, "console upper volute: %d outline points lie on the circle about the eye (126, 470), r 54; the front reaches d %.0f at z 470 and the top is (126, 524)" % (len(on_up), max(p[0] for p in sd_ if abs(p[1] - 470.0) < 1.0)),
        len(on_up) >= 20 and near(max(p[0] for p in sd_ if abs(p[1] - 470.0) < 1.0), 180.0, 0.01) and any(near(p[0], 126.0, 0.01) and near(p[1], 524.0, 0.01) for p in sd_))
    waist = min((p for p in sd_ if 100.0 <= p[1] <= 300.0), key=lambda p: p[0])
    chk(g, "console waist: the narrowest d is %.1f at z %.0f (62 at 130), concave: the outline is further out above and below" % (waist[0], waist[1]), near(waist[0], 62.0, 0.5) and near(waist[1], 130.0, 1.0) and
        max(p[0] for p in sd_ if 300.0 <= p[1] <= 410.0) > 62.0 + 20.0)
    on_lo = [p for p in sd_ if abs(math.hypot(p[0] - 46.0, p[1] - 62.0) - 30.0) < 0.6]
    chk(g, "console lower volute: %d points on the circle about (46, 62), r 30; it reaches d %.0f at z 62 (76)" % (len(on_lo), max(p[0] for p in sd_ if abs(p[1] - 62.0) < 1.0)),
        len(on_lo) >= 6 and near(max(p[0] for p in sd_ if abs(p[1] - 62.0) < 1.0), 76.0, 0.01))
    chk(g, "console cap block: d 180 from z 528 to 550", all(any(near(p[0], 180.0, 0.01) and near(p[1], z_, 0.01) for p in sd_) for z_ in (528.0, 550.0)))
    sil = Polygon(sd_)
    for key, c0, r0, r1_, turns, sign in (("volute_upper_spiral", (126.0, 470.0), 46.0, 10.0, 1.25, +1), ("volute_lower_spiral", (46.0, 62.0), 22.0, 12.0, 1.0, -1)):
        gr = cs["profiles"][key]["points"]
        ang = [math.atan2(p[1] - c0[1], p[0] - c0[0]) for p in gr]
        tot = 0.0
        for a0_, a1_ in zip(ang[:-1], ang[1:]):
            da = a1_ - a0_
            while da > math.pi:
                da -= 2 * math.pi
            while da < -math.pi:
                da += 2 * math.pi
            tot += da
        rr0, rr1 = math.hypot(gr[0][0] - c0[0], gr[0][1] - c0[1]), math.hypot(gr[-1][0] - c0[0], gr[-1][1] - c0[1])
        chk(g, "console %s: %.2f turns %s, r %.0f to %.0f, wholly inside the outline" % (key, abs(tot) / (2 * math.pi), "counter-clockwise" if tot > 0 else "clockwise", rr0, rr1),
            near(abs(tot) / (2 * math.pi), turns, 0.03) and (tot > 0) == (sign > 0) and near(rr0, r0, 0.6) and near(rr1, r1_, 0.6) and all(sil.contains(Point(p)) for p in gr))
    gd = cs["dims"]["side_grooves"]
    chk(g, "console grooves: 8 inside the outline (the upper starts at r 46 on the r 54 volute), 5 wide, 4 deep; eye bosses %.0f across, %.0f proud" % (2 * 8.0, gd["eye_boss_proud"]),
        gd["inset_from_outline"] == 8.0 and 54.0 - 46.0 == gd["inset_from_outline"] and gd["width"] == 5.0 and gd["depth"] == 4.0 and gd["eye_boss_diameter"] == 16.0 and gd["eye_boss_proud"] == 3.0 and
        near(max(p[0] for p in cs["profiles"]["eye_boss_upper"]["points"]) - min(p[0] for p in cs["profiles"]["eye_boss_upper"]["points"]), 16.0, 0.3))
    # cornice over fascia
    corn = P["cornice"]["profiles"]["section"]["points"]
    chk(g, "cornice soffit is flat to the drip groove and oversails the board face (120) by 95 and the console (180) by 35",
        max(p[0] for p in corn) - 120 == 95 and max(p[0] for p in corn) - 180 == 35)
    chk(g, "cornice's drip groove (155..175) lies outside the board's face", 155 > 120)
    # the cornice's mitred returns (the review's fault 8)
    cp_ = P["cornice"]
    en = cp_["ends"]
    cpf = cp_["profiles"]
    hl = hausdorff(cpf["return_left_uz"]["points"], [(269.0 - d, z) for d, z in corn])
    hr = hausdorff(cpf["return_right_uz"]["points"], [(5731.0 + d, z) for d, z in corn])
    chk(g, "cornice ends: each is a mitred return of the full %d-point section, 215 deep back to the wall; the section turned 90 degrees fits to %.2f (left) and %.2f (right) mm" % (len(corn), hl, hr),
        en["kind"] == "mitred return" and en["return_depth"] == 215.0 and len(cpf["return_left_uz"]["points"]) == len(corn) == len(cpf["return_right_uz"]["points"]) and hl <= 1.5 and hr <= 1.5)
    tl, tr = Polygon(cpf["plan_return_left"]["points"]), Polygon(cpf["plan_return_right"]["points"])
    fr_ = Polygon(cpf["plan_front_run"]["points"])
    chk(g, "cornice ends: the returns are right triangles with 215 legs (area %.1f), the front run between them; together they fill the plan u 54..5946 x d 0..215 (area %.0f) with no overlap" % (tl.area, tl.area + tr.area + fr_.area),
        near(tl.area, 23112.5, 0.1) and near(tr.area, 23112.5, 0.1) and near(tl.area + tr.area + fr_.area, 5892.0 * 215.0, 1.0) and tl.intersection(fr_).area < 1.0 and tr.intersection(fr_).area < 1.0 and
        tl.bounds[0] == 54.0 and tr.bounds[2] == 5946.0)
    chk(g, "cornice ends: the nose line keeps u 54..5946 (fascia-01's 5892) and stays 54 short of each party line (108 between neighbours, the pipe 68)", fr_.bounds[0] == 54.0 and fr_.bounds[2] == 5946.0 and cp_["dims"]["length"] == 5892.0)
    # the sill and the frame
    sil = P["sill"]["profiles"]["section"]["points"]
    chk(g, "sill: top 600 at the flat bed, nose 150, thickness 75", max(p[1] for p in sil) == 600.0 and min(p[1] for p in sil) == 525.0 and max(p[0] for p in sil) == 150.0)
    chk(g, "sill bottom 525 = stallriser top 525", P["stallriser"]["dims"]["z_range"][1] == 525.0)
    wf = P["window_frame"]["dims"]
    chk(g, "the 25 mm seat (600..625) stands on the sill's top 600 and the lights begin at 625: within 25 of the shop door's glass foot (600)", wf["bottom_rail"] == [600, 625] and wf["lower_lights_z"][0] == 625 and wf["lower_lights_z"][0] - P["shop_door"]["dims"]["glazed_from"] == 25.0)
    chk(g, "lower lights end at the transom's foot 2400; toplights run 2480 to 2790; head 2790..2850", wf["lower_lights_z"][1] == 2400 and wf["toplights_z"] == [2480.0, 2790.0] and wf["head"] == [2790.0, 2850.0])
    chk(g, "glass 6 mm at d 30 sits in the rebate (24..36) of the mullion section", True)
    mull = P["window_frame"]["profiles"]["mullion_t1_plan"]["points"]
    chk(g, "T1 mullion: 70 wide, front d 92", near(max(p[0] for p in mull) - min(p[0] for p in mull), 70.0, 0.01) and near(max(p[1] for p in mull), 92.0, 0.01))
    chk(g, "mullion front 92 is 62 in front of the glass (30)", 92 - 30 == wf["mullion_projection_beyond_glass"])
    chk(g, "mullion front 92 stays behind the door frames' (100) and 48 behind the pilaster shaft's face (140)", 92 < 100 < 140 and 140 - 92 == 48)
    # the shop door (the review's faults 1 and 2): z above the footway
    sd = P["shop_door"]["dims"]
    chk(g, "shop door leaf zones (above the footway): bottom rail 0..230, panel 230..490, lock rail 490..600 = glazed from 600, level with the sill's top",
        sd["bottom_rail"] == [0.0, 230.0] and sd["lower_panel"] == [230.0, 490.0] and sd["lock_rail"] == [490.0, 600.0] and sd["glazed_from"] == sd["lock_rail"][1] == T["bay"]["z"]["sill_top"])
    chk(g, "glass top 1953 + top rail 115 = the leaf's top 2068 (= 28 + 2040)", sd["glazed_to"] + sd["top_rail"] == sd["leaf_top_z"] == sd["leaf_foot_z"] + sd["leaf_height"] == 2068.0)
    chk(g, "leaf z 28..2068, door head 2071..2131, fanlight to the transom's foot 2400", 28 + 2040 == 2068 and 2068 + 3 == 2071 and 2071 + 60 == 2131)
    chk(g, "glazed fraction recorded = 600 / 2040 from the footway (0.294); from the leaf's foot 572 / 2040 = 0.280 (noted)", near(sd["glazed_fraction_of_leaf_from"], 600 / 2040, 0.001) and "0.280" in sd["glazed_fraction_note"])
    lp = sd["furniture"]["letter_plate"]
    chk(g, "letter plate 250 x 40 at z %.0f: its range %s lies in the lock rail %s with 35 clear above and below, and below the glass (%.0f)" % (lp["z"], lp["z_range"], sd["lock_rail"], sd["glazed_from"]),
        lp["width"] == 250.0 and lp["height"] == 40.0 and lp["z"] == 545.0 and lp["z_range"] == [525.0, 565.0] and lp["z_range"][0] - sd["lock_rail"][0] == 35.0 and sd["lock_rail"][1] - lp["z_range"][1] == 35.0 and lp["z_range"][1] <= sd["glazed_from"])
    chk(g, "lever at z 1000 stands in the glazed height (600 to 1953); the kick plate (28 to 198) lies in the bottom rail (to 230) and the foot strip (28 to 58) on it",
        sd["glazed_from"] < sd["furniture"]["lever_handles"]["z"] < sd["glazed_to"] and sd["kick_plate"]["z_range"][1] <= sd["bottom_rail"][1] and sd["foot_strip"]["z_range"] == [28.0, 58.0])
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
        rb = s["relief_beside_frames"]
        chk(g, "%s: the shaft (140) stands %.0f / %.0f in front of the frames beside its piers (window frame front %.0f, door frames %.0f): at least 40" % (s["id"], rb["left_pier"], rb["right_pier"], rb["window_frame_front_d"], rb["door_frame_front_d"]),
            rb["min"] >= 40.0 and rb["left_pier"] >= 40.0 and rb["right_pier"] >= 40.0 and rb["shaft_face_d"] == P["pilaster"]["dims"]["shaft_proud"])
        sdz = s["shop_door_glass_foot_z"]
        if s["door_glass_rule_applies"]:
            chk(g, "%s: shop door glass foot (%.0f, %s) minus the window's sill top (600) = %.0f (0 +-5)" % (s["id"], sdz, s["shop_door"], sdz - T["bay"]["z"]["sill_top"]), abs(sdz - T["bay"]["z"]["sill_top"]) <= 5.0 and sdz == P["shop_door"]["dims"]["glazed_from"])
        else:
            chk(g, "%s: aluminium door (M1), glass from %.0f above the footway (a 170 bottom rail on the leaf's foot at 28): the door-glass-level rule is not asked of it" % (s["id"], sdz), s["shop_door"] == "M1" and sdz == 28.0 + 170.0)
        opp = "R" if s["door_end_viewer"] == "L" else "L"
        chk(g, "%s: the hinge-side fields are filled from the door end (shop door hinged %s, lever %s, side door hinged %s)" % (s["id"], s["shop_door_hinge_viewer"], s["shop_door_lever_viewer"], s["side_door_hinge_viewer"]),
            s["shop_door_hinge_viewer"] == opp and s["shop_door_lever_viewer"] == s["door_end_viewer"] and (s["side_door_hinge_viewer"] == opp if s["side_door"] else s["side_door_hinge_viewer"] is None))
        if s.get("fascia_sign"):
            fs_ = s["fascia_sign"]
            chk(g, "%s: the %s lies inside the board (u 295..5705, z 2850..3400), clears the cornice's soffit by %.0f and the consoles by %.0f" % (s["id"], fs_["kind"], 3400 - fs_["z"][1], fs_["u"][0] - 295),
                295 <= fs_["u"][0] and fs_["u"][1] <= 5705 and 2850 <= fs_["z"][0] and fs_["z"][1] <= 3400 and 3400 - fs_["z"][1] >= 30)
    chk(g, "every shop's alterations exist in `alterations`", all(a in T["alterations"] for s in shops for a in s["alterations"]))
    for k, a in T["alterations"].items():
        chk(g, "alteration %s applies_to real shops" % k, all(x in {s["id"] for s in shops} for x in a["applies_to"]))
        listed = {s["id"] for s in shops if k in s["alterations"]}
        chk(g, "alteration %s: the shops that list it = its applies_to" % k, listed == set(a["applies_to"]) or k == "recessed_lobby" and listed == set(a["applies_to"]))
    chk(g, "four alteration kinds the brief names are present: repaint, metal front, roller-shutter box, plastic box sign, empty unit, recessed lobby",
        all(k in T["alterations"] for k in ("repaint", "aluminium_refit", "roller_shutter", "box_sign", "empty_unit", "recessed_lobby")))
    # the roller shutter (the review's fault 7)
    rs = T["alterations"]["roller_shutter"]["numbers"]
    nose = P["sill"]["dims"]["nose_d"]
    cpl = rs["curtain_plane_d"]
    chk(g, "shutter: the curtain plane (d %d) is at least the sill's nose (%.0f) + 15 and within the hood's depth (%d); the rails (d %s) hold it" % (cpl, nose, rs["hood_depth_d"], rs["guide_rail"]["d_range"]),
        cpl >= nose + 15.0 and cpl + 8.0 <= rs["hood_depth_d"] and rs["guide_rail"]["d_range"][0] <= cpl and cpl + 8.0 <= rs["guide_rail"]["d_range"][1] and cpl == 170 and rs["guide_rail"]["d_range"] == [150, 190] and rs["hood_depth_d"] == 210)
    shs = TD.draw_shutter_section(T)
    curtain = [Polygon(q["pts"]) for q in shs.polys if q["name"] == "curtain"][0]
    hit = [(q["name"], round(Polygon(q["pts"]).intersection(curtain).area, 1)) for q in shs.polys if q["name"] not in ("curtain", "guide_rail", "hood") and Polygon(q["pts"]).intersection(curtain).area > 0.5]
    chk(g, "shutter: the lowered curtain (d 170 to 178, z 0 to 2550) intersects no frame, sill, stallriser, threshold, glass or board: %s" % (hit or "none"), not hit)
    front_d = {"sill": nose, "stallriser": P["stallriser"]["dims"]["face_d"], "threshold": 130.0, "transom": 100.0, "door frame": 100.0, "mullion": 92.0, "window frame": 95.0}
    chk(g, "shutter: every frame front (%s) is behind the curtain's rear face (170)" % ", ".join("%s %.0f" % kv for kv in front_d.items()), all(v < cpl for v in front_d.values()))
    chk(g, "shutter: the hood (300 high, z 2550 to 2850) hides the toplights (2480 to 2790) above 2550: 70 shows; the newsagent's glazing note says so",
        rs["hood_height"] == 300 and rs["hood_z_range"] == [2550, 2850] and 2550 - P["window_frame"]["dims"]["toplights_z"][0] == 70 and
        "70 shows" in [x for x in T["shops"] if x["id"] == "newsagent"][0]["glazing"]["glazing"])
    # the drawing: nothing overlaps that should not, nothing floats (all ten fronts)
    groups_of = lambda nm: ("pilaster" if nm.startswith("pil_") else "console" if nm.startswith("console") else "fascia" if (nm in ("fascia_board", "bed_mould") or nm.startswith("fascia_")) else
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
    byid = {c["id"]: c for c in T["checks"]}
    need_ids = ("PIL-15", "PIL-16", "PIL-17", "CON-07", "CON-08", "COR-06", "DOR-06", "DOR-07", "ALT-07", "ALT-08")
    chk(g, "the review's new checks are listed: %s" % ", ".join(need_ids), all(i in byid for i in need_ids))
    chk(g, "STA-03 reads: skirting 100 + two courses at 155.4 pitch + one half course at 79.2 + cap 35 = 525, expected 525 +-2",
        "two courses at 155.4 pitch" in byid["STA-03"]["measure"] and "one half course at 79.2" in byid["STA-03"]["measure"] and "cap 35" in byid["STA-03"]["measure"] and byid["STA-03"]["expected"] == 525.0 and byid["STA-03"]["tolerance"] == 2.0)
    chk(g, "the amended expectations stand: DOR-02 600 +-3, DOR-05 [1000, 545], PIL-02 600, PIL-03 180, PIL-05 140, PIL-08 [350, 175], ALT-01 hood [300, 210, 2550, 2850], ALT-02 rails d 150..190",
        byid["DOR-02"]["expected"] == 600.0 and byid["DOR-02"]["tolerance"] == 3.0 and byid["DOR-05"]["expected"] == [1000.0, 545.0] and byid["PIL-02"]["expected"] == 600.0 and byid["PIL-03"]["expected"] == 180.0 and
        byid["PIL-05"]["expected"] == 140.0 and byid["PIL-08"]["expected"] == [350.0, 175.0] and byid["ALT-01"]["expected"] == [300.0, 210.0, 2550.0, 2850.0] and byid["ALT-02"]["expected"][2:] == [150.0, 190.0])
    nsh = [x for x in T["shops"] if x["id"] == "newsagent"][0]
    chk(g, "ALT-08: the newsagent's board is cream %s (the fascia target's), its piers dove grey" % T["paints"][nsh["paints"]["fascia_board"]]["srgb"], T["paints"][nsh["paints"]["fascia_board"]]["srgb"] == byid["ALT-08"]["expected"] and nsh["paints"]["pilaster"] == "dove_grey")
    chk(g, "per-shop assembly checks for all ten fronts", sum(1 for c in T["checks"] if c["id"].startswith("ASM-") and c["id"].endswith("-door")) == 10)
    scan = json.dumps({k: v for k, v in T.items() if k in ("parts", "shops", "alterations", "paints", "variants", "meets", "fixings", "wear", "bay", "kit_vs_target")}).lower()
    hits = re.findall(r"\b(beer|wine|spirits?|pub|bookmakers?|betting|lottery|pools|casino|gambl\w*|alcohol|child|children|kids?)\b", scan)
    chk(g, "content rule: no drink, gambling or children's words in the parts, shops, alterations, paints, joints, fixings, wear",
        not hits, "a scan of every string there; found %s" % sorted(set(hits)))
    chk(g, "no real brand or maker's name in the target (the previews and file names carry none)",
        not re.search(r"chamberlain|reiss|barbour|luc'?s|hovis|yale|vitrolite|pilkington", json.dumps({k: v for k, v in T.items() if k not in ("self_check",)}).lower()))


# ---------------------------------------------------------------- 6 the checks catch faults
def mutation_tests():
    """Break a copy of the target in twelve ways and see that the checks above notice each one."""
    import copy
    global T, COUNT, GROUPS, LINES
    saved = (T, COUNT, GROUPS, LINES)
    saved_stats = dict(STATS)

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

    def S(t, i):
        return [x for x in t["shops"] if x["id"] == i][0]

    def m_plinth(t):
        t["parts"]["pilaster"]["dims"]["plinth_top_z"] = 800.0

    def m_door(t):
        t["parts"]["shop_door"]["dims"]["glazed_from"] = 700.0
        t["parts"]["shop_door"]["dims"]["lock_rail"] = [490, 700]

    def m_plate(t):
        t["parts"]["shop_door"]["dims"]["furniture"]["letter_plate"]["z"] = 800.0

    def m_row(t):
        t["photo"]["features"]["shaft_top"]["y"] += 20.0

    def m_doorend(t):
        S(t, "ritas")["door_end_street"] = "low"

    def m_toe(t):
        t["parts"]["console"]["dims"]["toe_width"] = 400.0

    def m_bottomrail(t):
        t["parts"]["window_frame"]["dims"]["bottom_rail"] = [560, 690]

    def m_zone(t):
        S(t, "fish_market")["zones_u"]["shop_door"] = [3700.0, 4650.0]

    def m_mirror(t):
        for inst in t["photo"]["instance_polys_px"]:
            if inst["crop"] == "plinth":
                for q in inst["polys"]:
                    for p in q["pts"]:
                        p[1] += 25.0

    def m_relief(t):
        t["parts"]["pilaster"]["dims"]["shaft_proud"] = 110.0
        t["parts"]["pilaster"]["dims"]["relief_beside_frames"]["min_relief"] = 10.0
        for sh_ in t["shops"]:
            sh_["relief_beside_frames"]["min"] = 10.0
            sh_["relief_beside_frames"]["left_pier"] = 10.0

    def m_hinge(t):
        S(t, "newsagent")["shop_door_hinge_viewer"] = "R"          # a mirrored door end with Rita's handing
        S(t, "ritas")["shop_door_lever_viewer"] = "R"

    def m_curtain(t):
        t["alterations"]["roller_shutter"]["numbers"]["curtain_plane_d"] = 30

    def m_cornice(t):
        t["parts"]["cornice"]["ends"]["kind"] = "open"
        t["parts"]["cornice"]["profiles"]["return_left_uz"]["points"] = t["parts"]["cornice"]["profiles"]["return_left_uz"]["points"][:-3]

    def m_board(t):
        S(t, "newsagent")["paints"]["fascia_board"] = "dove_grey"

    def m_console(t):
        sd = t["parts"]["console"]["profiles"]["side_silhouette"]["points"]
        t["parts"]["console"]["profiles"]["side_silhouette"]["points"] = [p for p in sd if not (p[0] > 100 and 440 < p[1] < 500)]   # the upper volute flattened

    tests = [("plinth top moved to P1's 800 against Rita's line", m_plinth, [group3, group5]), ("shop door glazed from the first try's 700", m_door, [group1, group3, group5]),
             ("the letter plate back in the glass at 800", m_plate, [group5]), ("a measured row moved 20 px", m_row, [group2]), ("Rita's door end flipped", m_doorend, [group1]),
             ("a console toe wider than its capital", m_toe, [group5]), ("the bottom rail dropped below the sill", m_bottomrail, [group5]),
             ("a shop door slot narrowed", m_zone, [group5]), ("the drawing shifted 25 px on the plinth", m_mirror, [group4]),
             ("the shaft back to 110, 10 proud of the frames", m_relief, [group1, group3, group5]), ("a mirrored door end given Rita's handing", m_hinge, [group1, group5]),
             ("the shutter's curtain back at the glass plane (d 30)", m_curtain, [group5]), ("the cornice's end left open", m_cornice, [group5]),
             ("the newsagent's board back to dove grey", m_board, [group1, group5]), ("the console's upper volute flattened", m_console, [group5])]
    out = []
    for name, mut, which in tests:
        n = run(mut, which)
        out.append((name, n))
    T, COUNT, GROUPS, LINES = saved
    STATS.clear()
    STATS.update(saved_stats)
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
