#!/usr/bin/env python
"""Author tool: writes target.json (the shopfront target) from the part, shop and text modules and the
photograph's measurements (photo_measurements.json, from measure_leadenhall.py).

    /home/user/.bpyenv/bin/python make_target.py

target_drawing.py and self_check.py read target.json ALONE. Millimetres throughout; the game's viewer
frame (u from the viewer's left); d out from the wall; z up from the footway.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tgt_parts as T  # noqa: E402
import tgt_shops as S  # noqa: E402
import tgt_text as X  # noqa: E402
from tgt_profiles import r1  # noqa: E402

F_PX = 2400.0
CROP_PREVIEW = {"plinth": "P1-leadenhall-pilaster-plinth.jpg", "capital": "P1-leadenhall-pilaster-capital.jpg",
                "fascia": "P1-leadenhall-pier-fascia-cornice.jpg", "sill": "P1-leadenhall-sill-stallriser-stile.jpg",
                "transom": "P1-leadenhall-transom-mullion.jpg", "cornice": "P1-leadenhall-cornice-run.jpg",
                "door": "P1-leadenhall-shop-door-glass-foot.jpg", "pier": "P1-leadenhall-pier-elevation.jpg"}


def photo_block():
    pm = json.load(open(os.path.join(HERE, "photo_measurements.json")))
    M = pm["features"]

    def y(k):
        return M[k]["y"]

    def x(k):
        return M[k]["x"]
    sg = M["_sign"]
    sw, sh = sg["x1"] - sg["x0"], sg["y1"] - sg["y0"]
    s_door = 0.5 * (148.0 / sw + 210.0 / sh)
    ratio = y("pil_foot") / y("door_foot")                 # door plane is this much farther than the pilaster's front
    s_p = s_door / ratio                                   # mm per px at the pilaster's front plane
    ratio_win = y("pil_foot") / y("bottom_rail_foot")      # the window's own plane (its foot row)
    s_win = s_p * ratio_win                                # mm per px at the window frame's plane
    Zp = s_p * F_PX
    cam_h = y("pil_foot") * s_p                            # eye height above the footway
    cx = 0.5 * (x("shaft_left") + x("shaft_right"))
    shaft_w_px = x("shaft_right") - x("shaft_left")
    ret_px = x("shaft_return_outer") - x("shaft_right")
    x_mid = abs(0.5 * (x("shaft_right") + x("shaft_return_outer")))
    proud_low = ret_px * Zp / x_mid                        # the painted return: a lower bound on the relief beside the next surface
    ret2_px = x("shaft_return_frame") - x("shaft_right")
    x_mid2 = abs(0.5 * (x("shaft_right") + x("shaft_return_frame")))
    proud_frame = ret2_px * Zp / x_mid2                    # to the teal window frame
    foot = y("pil_foot")
    z = lambda k: (foot - y(k)) * s_p                      # height above the footway at the pilaster's front plane
    zw = lambda k: (y("bottom_rail_foot") - y(k)) * s_win  # height above the footway at the window's plane
    front_h = (foot - y("cornice_top")) * s_p
    crown_app = (y("cornice_base") - y("cornice_top")) * s_p
    d = {
        "id": "P1", "source": "Leadenhall Market HDRI, Andreas Mischok, CC0, taken 2019-05-19 (polyhaven.com/a/leadenhall_market)",
        "view": pm["view"], "crops": pm["crops"], "previews": CROP_PREVIEW,
        "scale": {"fit_dimension": "an A5 notice (148 x 210 mm) taped to the shop door's glass",
                  "notice_px": [round(sw, 2), round(sh, 2)], "mm_per_px_door_plane": round(s_door, 4),
                  "door_plane_over_pilaster_plane": round(ratio, 4), "mm_per_px_pilaster_plane": round(s_p, 4),
                  "window_plane_over_pilaster_plane": round(ratio_win, 4), "mm_per_px_window_plane": round(s_win, 4),
                  "camera_height_mm_above_footway": round(cam_h, 0),
                  "plane_depths_behind_pier_face_mm": {"window_frame": round((ratio_win - 1.0) * Zp, 0), "shop_door": round((ratio - 1.0) * Zp, 0)},
                  "error_pct": 8, "kind": "Photo",
                  "method": "the notice measured by edge snapping on the unmasked view (78.35 x 108.90 px, ratio 0.719 against A5's 0.705); a plane's depth from the ratio of the plinth's foot row (604.1) to that plane's own foot row (the door's 547.0, the window frame's 559.3), all at the same footway level: mm per px on a plane = camera height / its foot row; error: notice 1 px (1.3 per cent), plane ratio 3 per cent, the notice assumed to be A5 (England's statutory no-smoking sign, whose 2007 minimum size was A5: from memory, legislation.gov.uk unreached), say 8 per cent in all. Ratios do not carry it",
                  "note": "an elevation of a plane parallel to the wall is at one scale, and each plane has its own: the pier's front 1.7282, the window frame's 1.8666, the door's 1.9085 mm a pixel. Parts above eye level and proud of their plane are drawn taller by D.p/(D - p) (D the height above the eye, p the projection over the camera's distance): the crown and the capital are NOT measurable this way, only bounded"},
        "features": M,
        "derived_mm": {
            "shaft_width": round(shaft_w_px * s_p, 1),
            "shaft_return_px": round(ret_px, 2), "shaft_proud": round(proud_low, 1),
            "shaft_proud_note": "the painted return between the shaft's face and the next surface beside it: a LOWER bound on the relief; to the teal window frame it is %.0f (the frame's own foot row puts it %.0f behind the pier's face)" % (proud_frame, (ratio_win - 1.0) * Zp),
            "shaft_proud_to_window_frame": round(proud_frame, 0),
            "plinth_block1_top_z": round(z("plinth_block1_top"), 0), "plinth_block2_top_z": round(z("plinth_block2_top"), 0),
            "plinth_block3_top_z": round(z("plinth_block3_top"), 0), "plinth_top_z": round(z("plinth_cap_top"), 0),
            "plinth_cavetto_foot_z": round(z("plinth_block3_top"), 0),
            "shaft_top_z": round(z("shaft_top"), 0), "neck_ledge_z": round(z("neck_ledge"), 0), "abacus_top_z": round(z("abacus_top"), 0),
            "capital_height": round((y("shaft_top") - y("abacus_top")) * s_p, 0),
            "capital_height_note": "an UPPER bound: the flare's and the abacus's undersides lie inside the 174 px, adding roughly 30 to 60 mm",
            "board_between_crown_and_capital_top": round((y("fascia_field_bottom") - y("fascia_field_top")) * s_p, 0),
            "board_between_note": "the board between the crown's lowest fillet and the capital's top (not between the gilt keylines: the keyline sits about 65 px lower)",
            "front_height_to_cornice_top": round(front_h, 0),
            "front_height_note": "includes the crown, drawn taller by D.p/(D - p): good to about 5 per cent",
            "sill_top_z_window_plane": round(zw("sill_top"), 0),
            "window_stile_face": round((x("stile_right") - x("stile_left")) * s_win, 0),
            "mullion_face": round((x("mullion_right") - x("mullion_left")) * s_win, 0),
            "transom_bar_face": round((y("transom_bottom") - y("transom_top")) * s_win, 0),
            "stallriser_panel_height": round((y("grille_bottom") - y("grille_top")) * s_win, 0),
            "door_leaf_height_door_plane": round((y("door_foot") - y("door_leaf_top")) * s_door, 0),
            "door_glass_foot_door_plane": round((y("door_foot") - y("door_glass_bottom")) * s_door, 0),
            "door_glazed_from_fraction": round((y("door_foot") - y("door_glass_bottom")) / (y("door_foot") - y("door_leaf_top")), 3),
            "door_glazed_to_fraction": round((y("door_foot") - y("door_glass_top")) / (y("door_foot") - y("door_leaf_top")), 3),
            "door_foot_strip_height": round((y("door_foot") - y("door_foot_strip_top")) * s_door, 0),
            "crown_apparent_height_pilaster_plane": round(crown_app, 0),
            "crown_true_range": [170, 300],
            "crown_note": "NOT measurable by this method: the apparent 433 (446 on the wall plane the first try used) includes D.p/(D - p) for the projecting members (130 to 270); the true crown is between 170 and 300",
        },
        "ratios": {
            "plinth_top_over_sill_top": round(z("plinth_cap_top") / zw("sill_top"), 3),
            "plinth_top_over_front_height": round(z("plinth_cap_top") / front_h, 3),
            "sill_top_over_front_height": round(zw("sill_top") / front_h, 3),
            "capital_height_over_shaft_width": round((y("shaft_top") - y("abacus_top")) / shaft_w_px, 3),
            "shaft_proud_over_shaft_width": round(proud_low / (shaft_w_px * s_p), 3),
            "mullion_over_light": round((x("mullion_right") - x("mullion_left")) / (x("mullion_left") - x("stile_right")), 3),
            "crown_apparent_over_board": round((y("cornice_base") - y("cornice_top")) / (y("fascia_field_bottom") - y("fascia_field_top")), 3),
            "crown_true_over_board_range": [0.35, 0.6],
        },
    }
    # ---- the instance drawn on the photograph: apparent elevation bands built from the measured rows and columns
    cap_x0 = x("plinth_block1_left")
    sym = lambda xl: 2 * cx - xl
    crop = pm["crops"]

    def rect(name, x0, y0, x1, y1, tested):
        return {"name": name, "pts": [[round(x0, 2), round(y0, 2)], [round(x1, 2), round(y0, 2)], [round(x1, 2), round(y1, 2)], [round(x0, 2), round(y1, 2)]],
                "tested": tested}
    inst = []
    cp = crop["plinth"]
    inst.append({"crop": "plinth", "polys": [
        rect("plinth_block1", x("plinth_block1_left"), y("plinth_block1_top"), sym(x("plinth_block1_left")), y("pil_foot"),
             [("row", "plinth_block1_top"), ("col", "plinth_block1_left"), ("row", "pil_foot")]),
        rect("plinth_block2", x("plinth_block2_left"), y("plinth_block2_top"), sym(x("plinth_block2_left")), y("plinth_block1_top"),
             [("row", "plinth_block2_top"), ("col", "plinth_block2_left")]),
        rect("plinth_block3", x("plinth_block3_left"), y("plinth_block3_top"), sym(x("plinth_block3_left")), y("plinth_block2_top"),
             [("row", "plinth_block3_top"), ("col", "plinth_block3_left")]),
        rect("plinth_cavetto_and_band", x("plinth_cap_left"), y("plinth_cap_top"), sym(x("plinth_cap_left")), y("plinth_block3_top"),
             [("row", "plinth_cap_top")]),
    ]})
    inst.append({"crop": "capital", "polys": [
        rect("shaft", x("shaft_left"), crop["capital"][1] + crop["capital"][3], x("shaft_right"), y("shaft_top"),
             [("col", "shaft_left"), ("col", "shaft_right"), ("row", "shaft_top")]),
        rect("shaft_return", x("shaft_right"), crop["capital"][1] + crop["capital"][3] - 90, x("shaft_return_outer"), crop["capital"][1] + crop["capital"][3] - 20,
             [("col", "shaft_return_outer")]),
        rect("neck_ledge", x("neck_ledge_left"), y("neck_ledge") - 6.0, sym(x("neck_ledge_left")), y("neck_ledge"),
             [("row", "neck_ledge")]),
        rect("abacus", x("neck_ledge_left") - 62.0, y("abacus_top"), sym(x("neck_ledge_left")) + 62.0, y("abacus_bottom"),
             [("row", "abacus_top"), ("row", "abacus_bottom")]),
    ]})
    cf = crop["fascia"]
    inst.append({"crop": "fascia", "polys": [
        rect("board_between_crown_and_capital_top", cf[0] + cf[2] - 130, y("fascia_field_top"), cf[0] + cf[2] - 20, y("fascia_field_bottom"),
             [("row", "fascia_field_top"), ("row", "fascia_field_bottom")]),
        rect("crown_top_band", cf[0] + 100, y("crown_top"), cf[0] + 400, y("crown_top") + 4.0, [("row", "crown_top")]),
    ]})
    cs = crop["sill"]
    inst.append({"crop": "sill", "polys": [
        rect("stile", x("stile_left"), cs[1], x("stile_right"), cs[1] + cs[3] - 60,
             [("col", "stile_left"), ("col", "stile_right")]),
        rect("sill_group", x("stile_right"), y("sill_top"), x("stile_right") + 560, y("sill_nose"),
             [("row", "sill_top"), ("row", "sill_nose")]),
        rect("stallriser_panel", x("stile_right") + 30, y("grille_top"), x("stile_right") + 530, y("grille_bottom"),
             [("row", "grille_top"), ("row", "grille_bottom")]),
        rect("bottom_rail", x("stile_right"), y("grille_bottom"), x("stile_right") + 560, y("bottom_rail_foot"),
             [("row", "bottom_rail_foot")]),
    ]})
    cc = crop["cornice"]
    inst.append({"crop": "cornice", "polys": [
        rect("crown_cove", cc[0] + 30, y("cornice_cove_top"), cc[0] + 170, y("cornice_base"), [("row", "cornice_base"), ("row", "cornice_cove_top")]),
        rect("crown_soffit", cc[0] + 30, y("cornice_soffit_top"), cc[0] + 170, y("cornice_cove_top"), [("row", "cornice_soffit_top")]),
        rect("crown_lit", cc[0] + 30, y("cornice_lit_top"), cc[0] + 170, y("cornice_soffit_top"), [("row", "cornice_lit_top")]),
        rect("crown_red", cc[0] + 30, y("cornice_frieze_foot"), cc[0] + 170, y("cornice_lit_top"), [("row", "cornice_frieze_foot")]),
        rect("crown_face", cc[0] + 30, y("cornice_top"), cc[0] + 170, y("cornice_frieze_foot"), [("row", "cornice_top")]),
    ]})
    ct = crop["transom"]
    inst.append({"crop": "transom", "polys": [
        rect("transom_bar", ct[0] + 20, y("transom_top"), ct[0] + 640, y("transom_bottom"),
             [("row", "transom_top"), ("row", "transom_bottom")]),
        rect("mullion", x("mullion_left"), ct[1], x("mullion_right"), ct[1] + ct[3],
             [("col", "mullion_left"), ("col", "mullion_right")]),
    ]})
    cd = crop["door"]
    inst.append({"crop": "door", "polys": [
        rect("door_glazing_foot_bead", cd[0] + 10, y("door_glass_bottom") - 6.0, cd[0] + cd[2] - 10, y("door_glass_bottom"),
             [("row", "door_glass_bottom")]),
        rect("door_foot_strip", cd[0] + 10, y("door_foot_strip_top"), cd[0] + cd[2] - 10, y("door_foot"),
             [("row", "door_foot_strip_top"), ("row", "door_foot")]),
    ]})
    d["instance_polys_px"] = inst
    d["tolerances_px"] = {"default": 4.0, "weak_strength_below": 6.0, "weak": 8.0,
                          "note": "an edge is tested by re-snapping to the strongest gradient within the tolerance of the drawn edge on the saved preview"}
    d["not_remeasurable_on_previews"] = [k for k, v in M.items() if k != "_sign" and v.get("remeasurable") is False] + ["_sign"]
    # ---- Rita's elevation laid on the re-projected pier, at the shaft's width (one scale): the anchors
    d["rita_overlay"] = {
        "crop": "pier", "mm_per_px_pilaster_plane": round(s_p, 4), "mm_per_px_window_plane": round(s_win, 4),
        "foot_row": round(y("pil_foot"), 2), "window_foot_row": round(y("bottom_rail_foot"), 2), "shaft_centre_col": round(cx, 2),
        "tile_rows": 1000, "tile_width": crop["pier"][2], "tile_gap": 4,
        "note": "the target's Rita pilaster (the left one, u 0 to 350, shaft centre u 175) drawn in cyan at the pilaster plane's scale, so its shaft is as wide as P1's; the window-zone members (sill, transom, head) in yellow at the window plane's scale from the window's own foot row",
    }
    d["rita_vs_p1"] = [
        {"item": "plinth top", "target": 600, "p1": round(z("plinth_cap_top"), 0), "unit": "mm", "reading": "P1's 1.33 times its sill; Rita's line (the plinth level with the stallriser) is kept: D1"},
        {"item": "shaft width", "target": 290, "p1": round(shaft_w_px * s_p, 0), "unit": "mm", "reading": "the fit: 290.1 at the scale fitted on the notice, so the overlay is at one scale"},
        {"item": "shaft face in front of the next surface", "target": "40 to 45 (the frames' 95 and 100 behind 140)", "p1": "117 (the painted return) to %.0f (the teal frame)" % proud_frame, "unit": "mm", "reading": "the target lies inside P1's two bounds; P1's window frame stands %.0f and its door %.0f behind the pier's face, which Rita's frames (fixed at 95 and 100 by the kit) cannot copy" % ((ratio_win - 1.0) * Zp, (ratio - 1.0) * Zp)},
        {"item": "capital height", "target": 310, "p1": "at most %.0f" % ((y("shaft_top") - y("abacus_top")) * s_p), "unit": "mm", "reading": "upper bound: D4"},
        {"item": "capital top above the footway", "target": 2850, "p1": round(z("abacus_top"), 0), "unit": "mm", "reading": "P1's front is %.0f high to the crown's top against the street's 3550: a market hall's storey, not a parade's" % front_h},
        {"item": "sill top", "target": 600, "p1": round(zw("sill_top"), 0), "unit": "mm", "reading": "P1's sill is 0.172 of its front's height against 0.169: D9; the absolute 844 follows from the taller front"},
        {"item": "door glass foot above the footway", "target": 600, "p1": round((y("door_foot") - y("door_glass_bottom")) * s_door, 0), "unit": "mm", "reading": "level with the sill in both (P1: 798 against its sill 844, 46 apart; 0.304 of the leaf against the target's 0.294): D2"},
        {"item": "door leaf height", "target": 2040, "p1": round((y("door_foot") - y("door_leaf_top")) * s_door, 0), "unit": "mm", "reading": "P1's double doors are a market hall's"},
        {"item": "window stile face", "target": 50, "p1": round((x("stile_right") - x("stile_left")) * s_win, 0), "unit": "mm", "reading": "not followed (a heavy arcade frame)"},
        {"item": "mullion face", "target": 70, "p1": round((x("mullion_right") - x("mullion_left")) * s_win, 0), "unit": "mm", "reading": "partly followed: D5"},
        {"item": "front height to the cornice top", "target": 3550, "p1": round(front_h, 0), "unit": "mm", "reading": "the fascia target fixes the street's"},
        {"item": "crown (cornice) height", "target": 150, "p1": "170 to 300 (the apparent 433 is inflated by parts above eye level and proud of the plane)", "unit": "mm", "reading": "not measurable by this method: D7"},
    ]
    return d


def checks(shops):
    C = []

    def add(id_, part, name, measure, expected, tol, unit="mm", method="mesh bounding box or section"):
        C.append({"id": id_, "part": part, "name": name, "measure": measure, "expected": expected, "tolerance": tol, "unit": unit, "method": method})
    # pilaster
    add("PIL-01", "pilaster", "slot width", "bounding width of the plinth in u", 350.0, 1.0)
    add("PIL-02", "pilaster", "plinth top", "z of the plinth cap's flat top (Rita's line: level with the sill and the stallriser)", 600.0, 2.0)
    add("PIL-03", "pilaster", "plinth proud", "max d of the plinth's front", 180.0, 1.0)
    add("PIL-04", "pilaster", "shaft width (panel, flute, render)", "bounding width of the shaft in u", 290.0, 1.5)
    add("PIL-05", "pilaster", "shaft proud", "d of the shaft's front face (clad variant: the casing's face)", 140.0, 1.0)
    add("PIL-06", "pilaster", "neck", "z of the shaft's top / the astragal's foot", 2540.0, 2.0)
    add("PIL-07", "pilaster", "capital top", "z of the abacus's flat top", 2850.0, 1.0)
    add("PIL-08", "pilaster", "capital top size", "u extent and d extent of the capital's top face (the flat reaches d 172 and the ovolo rounds the last 3)", [350.0, 175.0], 3.5)
    add("PIL-09", "pilaster", "capital height", "capital top minus neck", 310.0, 1.0)
    add("PIL-10", "pilaster", "panelled shaft", "stile 45, sunk field 12, bead 10; rails 600 to 740 (the base ogee on its foot) and 2430 to 2540", [45.0, 12.0, 10.0], 1.0)
    add("PIL-11", "pilaster", "fluted shaft", "5 flutes, each 43.6 wide and 12 deep between 12 fillets", [5, 43.6, 12.0], 0.8, "count, mm")
    add("PIL-12", "pilaster", "party-wall pair gap", "distance between neighbouring plinth caps, capitals and plinths at the party line (u 0 / 6000)", 0.0, 3.0)
    add("PIL-13", "pilaster", "downpipe chase", "a notch 76 wide from d 50 in both neighbours' plinths (z 0 to 600) and capitals at each party line; the pipe's front (d 128) stands 12 behind the shafts' faces", [76.0, 50.0], 1.0)
    add("PIL-14", "pilaster", "profile fit", "capital_side, the plinth cap, plinth_stepped_side and the base ogee: two-way Hausdorff distance to the target profile", 0.0, 1.5)
    add("PIL-15", "pilaster", "relief beside the frames", "shaft face minus the front face of every frame beside it (window jamb 95, 75 or 40; shop-door frame 100; F1 frame 100) is at least 40; per shop in shops[].relief_beside_frames", 40.0, 0.0, "mm, at least")
    add("PIL-16", "pilaster", "plinth head (render variant)", "hollow moulding (cavetto) from d 172 at z 484 back to d 148 at z 579 (a quarter ellipse 24 by 95), then a band 21 high at d 148 to z 600, 8 in front of the shaft; blocks to 360 / 450 / 484", [172.0, 484.0, 148.0, 579.0, 600.0], 1.0)
    add("PIL-17", "pilaster", "base ogee (panel and flute)", "an ogee 25 proud of the shaft's face and 60 high on the plinth's top (z 600 to 660), returned on both sides of the shaft", [25.0, 60.0, 600.0], 1.0)
    # console
    add("CON-01", "console", "envelope", "bounding box width x depth x height", [240.0, 180.0, 550.0], 1.0)
    add("CON-02", "console", "centred on the pilaster", "u of the console's centre", [175.0, 5825.0], 1.0)
    add("CON-03", "console", "foot on the capital", "every point of the toe (240 x 60 at z 2850) lies within the capital's top (u 0..350, d 0..175) and at most 1 above it", 0.0, 1.0)
    add("CON-04", "console", "top at the cornice's soffit", "console top z", 3400.0, 1.0)
    add("CON-05", "console", "silhouette", "two-way Hausdorff between the built side section and side_silhouette", 0.0, 2.0)
    add("CON-06", "console", "leaf", "leaf relief max 12 proud, within u +-60 and z_local 120 to 440", [12.0, 60.0, 120.0, 440.0], 1.5)
    add("CON-07", "console", "volutes", "upper volute: eye (d 126, z 470), outer radius 54, the front reaches d 180 at z 470 and the top (126, 524); lower volute: eye (46, 62), outer radius 30, reaching d 76 at z 62; the waist narrowest d 62 at z 130; cap block 180 deep at z 528 to 550", [126.0, 470.0, 54.0, 46.0, 62.0, 30.0, 62.0, 130.0], 1.5)
    add("CON-08", "console", "side grooves", "grooves 8 inside the outline at the front, 5 wide, 4 deep, winding into an eye boss 16 across and 3 proud at each eye (upper 1.25 turns, lower one turn the other way)", [8.0, 5.0, 4.0, 16.0, 3.0], 0.5)
    # fascia and cornice
    add("FAS-01", "fascia_board", "board size", "u range, z range, face d", [[295.0, 5705.0], [2850.0, 3400.0], 120.0], 1.0)
    add("FAS-02", "fascia_board", "foot on the abacus", "overlap of the board's foot with each abacus top in u", 55.0, 1.0)
    add("FAS-03", "fascia_board", "bed mould", "z 2850 to 2890, front d 132 (43 behind the capital's top front, 175)", [2890.0, 132.0], 1.0)
    add("COR-01", "cornice", "size", "length x depth x height, z bottom", [5892.0, 215.0, 150.0, 3400.0], 1.0)
    add("COR-02", "cornice", "oversail", "cornice depth minus board face; minus console depth", [95.0, 35.0], 1.0)
    add("COR-03", "cornice", "soffit on the board", "gap between the soffit (3400) and the board's top and the consoles' tops", 0.0, 1.0)
    add("COR-04", "cornice", "profile", "two-way Hausdorff to the section", 0.0, 1.5)
    add("COR-05", "cornice", "stops short of the party line", "u range of the nose line", [54.0, 5946.0], 1.0)
    add("COR-06", "cornice", "closed mitred return at each end", "each end is a mitred return of the full 19-point section, 215 deep back to the wall (a right triangle in plan, area 23112.5 mm2): the section turned 90 degrees (return_left_uz, return_right_uz) has two-way Hausdorff <= 1.5 to the section; the nose line keeps 54..5946 and the back 269..5731", 0.0, 1.5)
    # sill, stallriser, window
    add("SIL-01", "sill", "sill", "z range and nose d", [[525.0, 600.0], 150.0], 1.0)
    add("SIL-02", "sill", "profile", "two-way Hausdorff to the section", 0.0, 1.5)
    add("STA-01", "stallriser", "height and face", "top z (under the sill) and face d", [525.0, 125.0], 1.0)
    add("STA-02", "stallriser", "panel count (panel variant)", "one raised and fielded panel per light of the window above", "n_lights", 0.0, "count")
    add("STA-03", "stallriser", "tile courses", "tile_square: skirting 100 + two courses at 155.4 pitch + one half course at 79.2 + cap 35 = 525", 525.0, 2.0)
    add("WIN-01", "window_frame", "frame on the sill", "bottom seat's foot z (a 25 seat: the lights stand on the sill)", 600.0, 1.0)
    add("WIN-02", "window_frame", "transom and head", "transom z range; head z range", [[2400.0, 2480.0], [2790.0, 2850.0]], 1.0)
    add("WIN-03", "window_frame", "mullion section", "T1 face 70, front d 92 (62 in front of the glass at d 30)", [70.0, 92.0, 62.0], 1.0)
    add("WIN-04", "window_frame", "mullion positions", "centres from the frame's left edge, per shop (shops[].glazing_layout)", "per shop", 3.0)
    add("WIN-05", "window_frame", "glass plane", "d of the glass", 30.0, 1.0)
    add("WIN-06", "window_frame", "frame length", "per shop (shops[].window_length)", "per shop", 1.0)
    # doors
    add("DOR-01", "shop_door", "leaf", "width x height", [900.0, 2040.0], 1.0)
    add("DOR-02", "shop_door", "glazed from", "bottom of the glass opening above the footway: level with the sill's top (600)", 600.0, 3.0)
    add("DOR-03", "shop_door", "slot", "overall width of frame", 1006.0, 1.0)
    add("DOR-04", "shop_door", "foot strip", "brass strip 30 high across the leaf's foot (the lowest 30 of the kick plate on T1)", 30.0, 1.0)
    add("DOR-05", "shop_door", "furniture heights", "lever handles at z 1000; letter plate 250 x 40 centred at z 545 in the lock rail (490 to 600), not in the glass", [1000.0, 545.0], 5.0)
    add("DOR-06", "shop_door", "door glass level with the sill", "per shop with a T1 or M2 door (shops[].door_glass_rule_applies): shop door glass foot minus window sill top = 0", 0.0, 5.0)
    add("DOR-07", "shop_door", "hinge and lever side per shop", "per shop (shops[].shop_door_hinge_viewer, shop_door_lever_viewer, side_door_hinge_viewer, side_door_knob_viewer, letter_plate_viewer): the shop door hinged on the window side with its lever on the opposite edge; the side door hinged on the shop-door side with its knob on the pier side; the letter plate centred on each leaf's width; the lever and plate side of each leaf are the table's", "per shop", 0.0, "side")
    add("SID-01", "side_door_slot", "slot width", "overall width of the side-door slot", 944.0, 1.0)
    add("SID-02", "side_door_slot", "F1 head meets the transom", "the F1 head trimmed at z 2400; gap to the transom's underside", 0.0, 3.0)
    add("SID-03", "side_door_slot", "F1 frame face", "d of the F1 frame's outside face (40 behind the shafts' faces)", 100.0, 1.0)
    add("SID-04", "side_door_slot", "threshold nose", "d of the trimmed threshold's front", 130.0, 1.0)
    # the opening
    add("ZON-01", "assembly", "zones fill the opening", "side-door slot + shop-door slot + window = 5300 (no side door: 5300 - 1006 = 4294)", 5300.0, 1.0)
    add("ZON-02", "assembly", "window length", "default 3350; no side door 4294", [3350.0, 4294.0], 1.0)
    # alterations
    add("ALT-01", "roller_shutter", "hood", "height x depth, z range", [300.0, 210.0, 2550.0, 2850.0], 2.0)
    add("ALT-02", "roller_shutter", "guide rail", "face x depth, d range (on steel spacer brackets through the frames into the pilaster core)", [50.0, 40.0, 150.0, 190.0], 1.0)
    add("ALT-03", "aluminium_refit", "section", "stile, mullion and transom face x depth", [50.0, 75.0], 1.0)
    add("ALT-04", "empty_unit", "the absent console", "no console at u 55..295 on the empty unit; a stump 240 x 60 x 90", [240.0, 60.0, 90.0], 2.0)
    add("ALT-05", "box_sign", "stands on the board", "front d of the laundry box 270; newsagent 260; tea panel 150", [270.0, 260.0, 150.0], 2.0)
    add("ALT-06", "recessed_lobby", "depth", "the door frame's front face d: grocer -500 (recess 600 from the frame line d 100), laundry -200 (recess 300)", [-500.0, -200.0], 3.0)
    add("ALT-07", "roller_shutter", "curtain plane", "curtain plane at d 170: at least the sill's nose (150) + 15 and within the hood's depth (210); the lowered variant (the curtain from the hood to the footway in front of window and door) intersects no frame, sill, stallriser or threshold", [170.0, 15.0, 210.0], 1.0)
    add("ALT-08", "newsagent", "board colour", "the newsagent's fascia board paint is the fascia target's old_board cream (222, 209, 175)", [222.0, 209.0, 175.0], 2.0, "sRGB units")
    # per shop assembly checks
    for s in shops:
        w = s["zones_u"]["window"]
        add("ASM-%s-door" % s["id"], "assembly", "%s: door end and zones" % s["id"], "shop door slot u range; window u range; side door slot",
            [s["zones_u"]["shop_door"], w, s["zones_u"]["side_door"]], 1.0, "mm")
        add("ASM-%s-x" % s["id"], "assembly", "%s: window and side-door centres in street x" % s["id"], "street x of the window centre and the side door's centre (the fascia target's window_centre and fanlight x)",
            [s["centres_street_x_m"]["window"], s["centres_street_x_m"]["side_door"]], 0.005, "m")
    add("MAT-01", "all", "materials", "at most three plain PBR materials per piece: paint, metal or glass-like, tile or stone; no textures", 3, 0, "count")
    add("MAT-02", "all", "paint is a per-shop parameter", "each piece's paint colour is read from shops[].paints (sRGB), not baked", "per shop", 2.0, "sRGB units")
    add("NO-01", "all", "no lettering, no maker's mark, no drink or gambling, no children", "the glbs carry no text geometry and no texture", 0, 0, "count")
    add("CLR-01", "assembly", "no solid overlaps except those enclosed", "interpenetration pairs: console toe into its dowel holes; fascia ends into console rebates; frame tenons into jambs", "enclosed only", 0.0, "count")
    return C


def build():
    photo = photo_block()
    pil, con, fas, cor, sil, sta, win, shd, sid, lob = (T.pilaster(), T.console(), T.fascia_board(), T.cornice(), T.sill(), T.stallriser(),
                                                        T.window_frame(), T.shop_door(), T.side_door_slot(), T.lobby())
    fronts = S.fronts()
    # glazing layouts per shop from the pattern
    for f in fronts:
        g = f["glazing"]
        w = f["window_length"]
        jw = 50.0 if g["window_frame"] in ("T1", "T2", "M1") else 28.0
        if g["window_frame"] == "M2":
            jw = 28.0
        mw = float(g["mullion_face"])
        f["glazing_layout"] = S.window_layout(w, g["n_mullions"], mw, jw, g["toplights"], 28.0 if g["window_frame"] != "M1" else 50.0, g.get("toplight_aligned", False))
        f["glazing_layout"]["jamb_face"] = jw
        f["glazing_layout"]["mullion_face"] = mw
        f["glazing_layout"]["frame_front_d"] = {"T1": 95.0, "T2": 95.0, "M1": 75.0, "M2": 40.0}[g["window_frame"]]
        f["glazing_layout"]["mullion_front_d"] = {"T1": 92.0, "T2": 92.0, "M1": 75.0, "M2": 40.0}[g["window_frame"]]
        f["paint_srgb"] = {k: (S.PAINTS[v]["srgb"] if v in S.PAINTS else None) for k, v in f["paints"].items() if v}
        f["paint_names"] = {k: (S.PAINTS[v]["plain"] if v in S.PAINTS else None) for k, v in f["paints"].items() if v}
        # the relief of each pier's shaft in front of the frame beside it (the shaft's face less that frame's front face)
        win_front = f["glazing_layout"]["frame_front_d"]
        door_front = T.FRAME_FRONT["door"]
        beside_win = T.SHAFT_PROUD - win_front
        beside_door = T.SHAFT_PROUD - (T.FRAME_FRONT["F1"] if f["side_door"] else door_front)
        left_is_door = f["door_end_viewer"] == "L"
        f["relief_beside_frames"] = {"left_pier": round(beside_door if left_is_door else beside_win, 1), "right_pier": round(beside_win if left_is_door else beside_door, 1),
                                     "shaft_face_d": T.SHAFT_PROUD, "window_frame_front_d": win_front, "door_frame_front_d": door_front, "min": round(min(beside_door, beside_win), 1)}
    dm = photo["derived_mm"]
    rt = photo["ratios"]
    sill_over = T.SILL_TOP
    derived = [
        {"id": "R1", "name": "plinth top over sill top", "photo": rt["plinth_top_over_sill_top"], "target": round(T.PLINTH_TOP / T.SILL_TOP, 3), "tolerance_pct": 12, "followed": False,
         "reading": "P1's plinth stands 1.33 times its sill (800 at the street's scale); Rita's front, the approved model, has the plinth's top level with the stallriser (1.0): Rita's line is kept and the photograph's is offered as variants.plinth_tall (D1)"},
        {"id": "R2", "name": "plinth top over the front's height", "photo": rt["plinth_top_over_front_height"], "target": round(T.PLINTH_TOP / T.CORNICE_TOP, 3), "tolerance_pct": 8, "followed": False,
         "reading": "0.228 against 0.169: Rita's line kept (D1)"},
        {"id": "R3", "name": "sill top over the front's height", "photo": rt["sill_top_over_front_height"], "target": round(T.SILL_TOP / T.CORNICE_TOP, 3), "tolerance_pct": 10,
         "reading": "the window's own plane puts P1's sill top at %.0f mm: 0.172 against 0.169; no disagreement with the scene's 600" % dm["sill_top_z_window_plane"]},
        {"id": "R4", "name": "capital height over shaft width", "photo": rt["capital_height_over_shaft_width"], "target": round(T.CAP_H / T.SHAFT_W, 3), "tolerance_pct": 8, "followed": False, "kind": "upper bound",
         "reading": "P1's 1.04 is an UPPER bound (the flare's and abacus's undersides add 30 to 60 mm to the 174 px); 310 / 290 = 1.069 is Judgement (the capital must carry the console's toe and the board's foot)"},
        {"id": "R5", "name": "shaft proud over shaft width", "photo": rt["shaft_proud_over_shaft_width"], "photo_high": round(dm["shaft_proud_to_window_frame"] / T.SHAFT_W, 3), "target": round(T.SHAFT_PROUD / T.SHAFT_W, 3), "tolerance_pct": 0, "range": True,
         "reading": "P1's painted return (117) is the LOWER bound and the teal window frame (about %.0f in front of it) the upper: the shaft's relief beside the next surface; 140 sits inside both" % dm["shaft_proud_to_window_frame"]},
        {"id": "R6", "name": "shop door glazed from, over the leaf", "photo": dm["door_glazed_from_fraction"], "target": round(600.0 / 2040.0, 3), "tolerance_pct": 8,
         "reading": "P1 0.304 of its leaf (620 on a 2040 leaf); 600 / 2040 = 0.294; the scene's 1000 / 2040 = 0.49 is far outside"},
        {"id": "R7", "name": "shaft width, absolute", "photo": dm["shaft_width"], "target": T.SHAFT_W, "tolerance_pct": 8,
         "reading": "scale error 8 per cent"},
        {"id": "R8", "name": "crown height over the board", "photo": rt["crown_apparent_over_board"], "target": round(150.0 / 550.0, 3), "tolerance_pct": 0, "followed": False, "kind": "not measurable",
         "reading": "not measurable by this method: the apparent 0.86 includes D.p/(D - p) for projecting members above eye level; the true crown is 170 to 300 (0.35 to 0.6 of the board). The street's 0.27 stands (the fascia target fixes the cornice top); the corona's 0.35 of the height is Judgement (D7)"},
        {"id": "R9", "name": "door glass foot minus window sill top (mm)", "photo": round(dm["door_glass_foot_door_plane"] - dm["sill_top_z_window_plane"], 0), "target": 0.0, "tolerance_abs": 60.0,
         "reading": "P1: the door's glass (798 on the door's plane) starts 46 below its window's sill (844): level to within the scale error; the target puts them level (600)"},
    ]
    for r in derived:
        if r.get("range"):
            r["within"] = r["photo"] <= r["target"] <= r["photo_high"]
        elif "tolerance_abs" in r:
            r["within"] = abs(r["photo"] - r["target"]) <= r["tolerance_abs"]
        else:
            r["within"] = abs(r["photo"] - r["target"]) / r["target"] * 100.0 <= r["tolerance_pct"]
        r.setdefault("followed", True)
    T_json = {
        "schema": "cloud-week-42 target v1 (shopfronts)",
        "family": "the shopfront as a kit of parts",
        "summary_line": "The shopfront kit's target (second try): pilasters (plinth 600 at Rita's line, shaft 140 proud, necking, capital 350 x 175 on a hollow flare), two-volute scrolled consoles, fascia board and cornice with mitred returns, sill and stallriser, window frames, the shop door glazed from 600 level with the sill and its plate in the lock rail, the F1 side door's slot and ten fronts assembled by a table with a hinge side each, with the 1990 alterations by kind; measured today on one reached photograph (Leadenhall Market, at its own planes' scales), which corrects the shaft's relief, the plinth's hollow head, the door's glazing and the sill.",
        "status": "SECOND TRY, 9 October 2026 (cloud week 42), by the target writer, answering the fresh reviewer's eleven faults (TARGET-REVIEW.md, FAIL). Not reviewed again. Nothing is committed. self_check is written by self_check.py.",
        "units": "millimetres; angles in degrees; colours sRGB 0-255 (aged to 1990); roughness 0-1; metal 0-1",
        "axes": {
            "u": "across the bay from the VIEWER'S left party-wall line (0) to the right one (6000), as a player standing in the street and facing the front sees it IN THE GAME (the fascia target's frame: on the east parade low street x is on the viewer's RIGHT, on the west block on the viewer's LEFT)",
            "d": "out from the wall face (positive toward the street; the kit's y = -d)",
            "z": "up from the footway at the frontage (the street adds its own 0.1 m offset)",
            "sections": "d-z a side section; u-d a plan section; a-p a small moulding (a along its face, p proud); u-z an elevation. Closed outlines are counter-clockwise with the first axis right and the second up",
            "mapping": "street x = bay high end - u/1000 on the east parade; bay low end + u/1000 on the west block. The recipe's doors_on word is 'left' for a viewer's RIGHT door end and 'right' for a viewer's LEFT door end (shops[].recipe_doors_on)",
            "pivot": "each part's origin is where the part's own `origin` field says (default: the bay datum at the middle of the part's width, d 0 at the wall, z 0 at the footway), as the kit; glb forward -Z as production/specs/asset-interface.md says (the kit's note stands: each kit piece wants the opposite yaw to the consoles' when placed)"},
        "bay": {"width": T.BAY, "pilaster_slot": T.SLOT, "opening_zone": T.ZONE, "side_door_slot": T.SIDE_SLOT, "shop_door_slot": T.SHOP_SLOT,
                "window_default": T.WINDOW_LEN, "window_no_side_door": T.ZONE - T.SHOP_SLOT,
                "z": {"sill_top": 600.0, "sill_underside": 525.0, "transom": [2400.0, 2480.0], "head": [2790.0, 2850.0], "fascia": [2850.0, 3400.0], "cornice": [3400.0, 3550.0]},
                "d": {"shaft_front": T.SHAFT_PROUD, "plinth_front": T.PLINTH_PROUD, "capital_top_front": T.CAP_TOP_PROUD, "fascia_face": 120.0, "cornice_nose": 215.0,
                      "console_front": 180.0, "sill_nose": 150.0, "stallriser_face": 125.0, "frame_fronts": [95.0, 100.0], "mullion_front": 92.0, "glass": 30.0,
                      "shutter_curtain": 170.0, "shutter_rails": [150.0, 190.0], "shutter_hood": 210.0},
                "source": "Read: SCENE-SLOTS.md, the shopfront kit README, the fascia target (board 295 to 5705, 120 proud, cornice top 3.55), fascia-01 (cornice 5892 x 215 x 150, console 240 x 180 x 550); Derived: the zones (350 + 944 + 1006 + 3350 + 350 = 6000)"},
        "photo": photo,
        "derived_rules": derived,
        "parts": {"pilaster": pil, "console": con, "fascia_board": fas, "cornice": cor, "sill": sil, "stallriser": sta, "window_frame": win,
                  "shop_door": shd, "side_door_slot": sid, "lobby": lob},
        "meets": X.JOINTS,
        "fixings": X.FIXINGS,
        "wear": X.WEAR,
        "alterations": S.ALTERATIONS,
        "paints": S.PAINTS,
        "shops": fronts,
        "game_today": X.GAME_TODAY,
        "variants": {
            "plinth_tall": "P1's plinth at the street's scale, 800 high (variants.plinth_tall of the pilaster): NOT used; Rita's 600 wins",
            "cornice_tall": {"use": "optional: a cornice 300 high (z 3400 to 3700), 280 deep, for a reviewer who reads P1's crown as binding; the crown is not measurable by the method, so there is no photographic basis; it would collide with the fascia target's hanging-sign brackets at 3.60 and the first-floor sills; NOT the default",
                             "dims": {"height": 300.0, "depth": 280.0}},
            "shutter_down": "the newsagent's curtain lowered: a slatted plane at d 170 over window and door, z 0 to 2550, between the guide rails (d 150 to 190), clear of every frame, the sill (nose 150) and the threshold (130)",
            "paint_fresh": "each paint's fresh value is the fascia target's where it has one (palette.srgb_fresh); the rest are the aged value lifted 8 per cent",
        },
        "evidence_basis": X.EVIDENCE,
        "kit_vs_target": X.KIT_VS_TARGET,
        "disagreements_photographs_win": X.DISAGREEMENTS,
        "review_faults_answered": X.REVIEW_FAULTS,
        "sources": X.SOURCES,
        "unreached": X.UNREACHED,
        "would_read_when_network_opens": X.WOULD_READ,
        "could_not_settle": X.COULD_NOT_SETTLE,
        "checks": checks(fronts),
        "self_check": None,
    }
    return T_json


def main():
    t = build()
    path = os.path.join(HERE, "target.json")
    json.dump(t, open(path, "w"), indent=1)
    print("wrote", path, os.path.getsize(path), "bytes;", len(t["checks"]), "checks;", len(t["shops"]), "shops")
    for r in t["derived_rules"]:
        print(" ", r["id"], r["name"], "photo", r["photo"], "target", r["target"], "within" if r["within"] else "OUT", "" if r["followed"] else "(not followed)")
    print(json.dumps(t["photo"]["derived_mm"], indent=1))
    print(json.dumps(t["photo"]["scale"], indent=1)[:900])


if __name__ == "__main__":
    main()
