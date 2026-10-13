"""phone-box: writes target.json and TARGET.md (cloud week 42, unit 13, family 1: the KX100 telephone box)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_doc as D
from sd_lib import B, CY

FAMILY = "phone-box"
PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))
F = PM["features"]
Q, QI, QG = 435.0, 395.0, 343.0   # post outer half width, post inner, glazing half width (the 1990 kiosk is square)
LID = 445.0
Z_TOP, Z_SKIRT, Z_HEAD, Z_BAND1, Z_BAND0, Z_RAILT, Z_RAILB = 2192.0, 2092.0, 1822.0, 1051.0, 906.0, 231.0, 163.0   # the foot gap is P1's own 163 (48 px), the rail 68 high


def kx_parts(door=True):
    P = []
    # the roof: a folded stainless lid (the Mk2 biscuit-tin lid), 3 mm sheet, a 100 mm skirt all round
    P.append(B("lid_top", -LID, LID, -LID, LID, Z_TOP - 3, Z_TOP, "stainless", edge="folded edge r 4", note="lid plate, 3 mm sheet"))
    P.append(B("lid_skirt_front", -LID, LID, -LID, -LID + 3, Z_SKIRT, Z_TOP - 2, "stainless", edge="lower edge turned in 8 mm", note="skirt 100 deep"))
    P.append(B("lid_skirt_back", -LID, LID, LID - 3, LID, Z_SKIRT, Z_TOP - 2, "stainless", edge="lower edge turned in 8 mm"))
    P.append(B("lid_skirt_left", -LID, -LID + 3, -LID + 3, LID - 3, Z_SKIRT, Z_TOP - 2, "stainless"))
    P.append(B("lid_skirt_right", LID - 3, LID, -LID + 3, LID - 3, Z_SKIRT, Z_TOP - 2, "stainless"))
    # the skirts' lower edges are turned in 8 mm (a flange 3 mm thick): the header and the back sheet meet it
    P.append(B("lid_lip_front", -LID + 3, LID - 3, -LID + 3, -LID + 11, Z_SKIRT, Z_SKIRT + 3, "stainless", note="turned-in lower edge, 8 mm"))
    P.append(B("lid_lip_back", -LID + 3, LID - 3, LID - 11, LID - 3, Z_SKIRT, Z_SKIRT + 3, "stainless"))
    P.append(B("lid_lip_left", -LID + 3, -LID + 11, -LID + 11, LID - 11, Z_SKIRT, Z_SKIRT + 3, "stainless"))
    P.append(B("lid_lip_right", LID - 11, LID - 3, -LID + 11, LID - 11, Z_SKIRT, Z_SKIRT + 3, "stainless"))
    # four corner posts: stainless box section 40 x 40, running from the ground to the lid
    for nm, sx, sy in (("p_fl", -1, -1), ("p_fr", 1, -1), ("p_bl", -1, 1), ("p_br", 1, 1)):
        x0, x1 = (-Q, -QI) if sx < 0 else (QI, Q)
        y0, y1 = (-Q, -QI) if sy < 0 else (QI, Q)
        P.append(B(nm, x0, x1, y0, y1, 0.0, Z_TOP - 3, "stainless", edge="vertical edges r 3", note="brushed box section 40 x 40"))
    # the front: header, door stiles, bottom rail, handle panel, glass, pull, hinges
    P.append(B("f_header", -QI, QI, -Q, -Q + 30, Z_HEAD, Z_SKIRT, "black_plastic", edge="corners r 6", note="black header panel, 30 deep, carries the word"))
    P.append(B("f_stile_l", -QI, -QG, -Q, -Q + 20, Z_RAILT, Z_HEAD, "black_plastic", edge="outer edge r 2", note="door stile 52 wide, 20 deep"))
    P.append(B("f_stile_r", QG, QI, -Q, -Q + 20, Z_RAILT, Z_HEAD, "black_plastic", edge="outer edge r 2"))
    P.append(B("f_rail_bottom", -QI, QI, -Q, -Q + 20, Z_RAILB, Z_RAILT, "black_plastic", edge="lower edge r 2", note="bottom rail 68 high"))
    P.append(B("f_band", -QG, QG, -Q - 10, -Q + 20, Z_BAND0, Z_BAND1, "handle_yellow", edge="corners r 8", note="moulded handle panel, 10 proud of the frame"))
    P.append(B("f_pull", -QG, -QG + 50, -Q - 38, -Q - 10, Z_BAND0 + 12, Z_BAND0 + 78, "handle_yellow", edge="r 6", note="rectangular pull with a finger recess, at the lock end"))
    P.append(B("f_glass_up", -QG - 4, QG + 4, -Q + 7, -Q + 11, Z_BAND1 - 4, Z_HEAD + 4, "glass", transparent=True, edge="arrised 1 mm", note="upper pane, 4 mm toughened"))
    P.append(B("f_glass_lo", -QG - 4, QG + 4, -Q + 7, -Q + 11, Z_RAILT - 4, Z_BAND0 + 4, "glass", transparent=True, edge="arrised 1 mm", note="lower pane, 4 mm toughened"))
    for i, z in enumerate((300.0, 1000.0, 1700.0)):
        P.append(CY("f_hinge%d" % (i + 1), (QI - 3, -Q + 10, z), (QI - 3, -Q + 10, z + 70), 7.0, "stainless", note="pivot hinge, hinge side right"))
    # the two sides (fixed glazing): the same frame, band black
    for nm, sx in (("l", -1), ("r", 1)):
        x0, x1 = (-Q, -Q + 30) if sx < 0 else (Q - 30, Q)
        xs0, xs1 = (-Q, -Q + 20) if sx < 0 else (Q - 20, Q)
        xb0, xb1 = (-Q, -Q + 20) if sx < 0 else (Q - 20, Q)
        xg0, xg1 = (-Q + 7, -Q + 11) if sx < 0 else (Q - 11, Q - 7)
        P.append(B("s%s_header" % nm, x0, x1, -QI, QI, Z_HEAD, Z_SKIRT, "black_plastic", note="black fascia round the side, same height as the header"))
        P.append(B("s%s_stile_f" % nm, xs0, xs1, -QI, -QG, Z_RAILT, Z_HEAD, "black_plastic"))
        P.append(B("s%s_stile_b" % nm, xs0, xs1, QG, QI, Z_RAILT, Z_HEAD, "black_plastic"))
        P.append(B("s%s_rail_bottom" % nm, xs0, xs1, -QI, QI, Z_RAILB, Z_RAILT, "black_plastic"))
        P.append(B("s%s_band" % nm, xb0, xb1, -QG, QG, Z_BAND0, Z_BAND1, "black_plastic", note="plain black band, flush with the posts"))
        P.append(B("s%s_glass_up" % nm, xg0, xg1, -QG - 4, QG + 4, Z_BAND1 - 4, Z_HEAD + 4, "glass", transparent=True))
        P.append(B("s%s_glass_lo" % nm, xg0, xg1, -QG - 4, QG + 4, Z_RAILT - 4, Z_BAND0 + 4, "glass", transparent=True))
    # the back: one stainless sheet from the ground to the lid, the payphone on its inner face
    P.append(B("back_panel", -Q, Q, Q - 6, Q, 0.0, Z_SKIRT, "stainless", note="single sheet back (Mk2), 6 mm with its backing"))
    P.append(B("lower_enclosure", -190.0, 260.0, 300.0, Q - 6, 120.0, 480.0, "stainless", note="coin-vault housing, brushed steel (Judgement)"))
    P.append(B("pp_body", -170.0, -30.0, 350.0, Q - 6, 1000.0, 1340.0, "phone_grey", note="payphone body, 140 x 79 x 340"))
    P.append(B("pp_keypad", -150.0, -50.0, 338.0, 350.0, 1100.0, 1200.0, "stainless"))
    P.append(B("pp_handset", -192.0, -164.0, 340.0, 390.0, 1120.0, 1300.0, "black_plastic", note="handset on its cradle at the left of the body"))
    P.append(B("notice_frame", 40.0, 210.0, Q - 20, Q - 6, 1050.0, 1350.0, "black_plastic", note="notice and charges frame"))
    if not door:
        P = [p for p in P if not p["id"].startswith("f_") or p["id"] in ("f_header",)]
    return P


def build():
    var_door = kx_parts(True)
    var_open = kx_parts(False)
    # the doorless kiosk keeps the header and gets its two front stiles back as posts-only: no leaf, no glass
    T = {
        "family": FAMILY,
        "title": "Quay Street's telephone box (the 1985 to 1991 stainless kind, no operator's mark)",
        "units": "millimetres; angles in degrees; z up, the front (the door) faces -y, the pivot is the centre of the base on the ground; the .glb is metres",
        "status": "fixes applied, not re-reviewed",
        "sample": "KX1",
        "materials": {
            "stainless": {"name": "brushed stainless steel", "srgb": [196, 198, 200], "rough": 0.38, "rough_words": "satin, brushed", "metal": True, "note": "water-stained, never mirror bright"},
            "black_plastic": {"name": "black moulded plastic, faded", "srgb": [26, 26, 27], "rough": 0.55, "rough_words": "semi-matt", "metal": False, "note": "UV-faded to a very dark grey-brown at the top edges"},
            "handle_yellow": {"name": "handle yellow, dulled", "srgb": [232, 188, 22], "rough": 0.45, "rough_words": "semi-gloss", "metal": False, "note": "the 1985 to 1991 colour; dulled, scuffed at the pull"},
            "glass": {"name": "clear toughened glass, slight grey cast", "srgb": [205, 212, 214], "rough": 0.05, "rough_words": "smooth", "metal": False, "note": "transmission 0.84 (Judgement); smoked glass belongs to the first deliveries only"},
            "phone_grey": {"name": "payphone body, cream-grey plastic", "srgb": [168, 164, 150], "rough": 0.5, "rough_words": "semi-matt", "metal": False, "note": "stained brown by smoke (tobacco is allowed)"},
        },
        "variants": {
            "KX1": {"name": "KX1: the door kiosk, 1985 to 1991 livery, clear glass (the sample)", "parts": var_door,
                    "overall": {"w": 890.0, "d": 890.0, "h": 2192.0}, "overall_tol": 1.5, "overall_exclude": ["f_pull"],
                    "joins": [["p_fl", "lid_top"], ["p_fr", "lid_top"], ["p_bl", "lid_top"], ["p_br", "lid_top"], ["lid_top", "lid_skirt_front"],
                              ["f_stile_l", "p_fl"], ["f_stile_r", "p_fr"], ["f_header", "p_fl"], ["f_header", "p_fr"], ["f_header", "lid_lip_front"],
                              ["f_rail_bottom", "f_stile_l"], ["f_band", "f_stile_l"], ["f_pull", "f_band"], ["f_glass_up", "f_header"], ["f_glass_up", "f_band"],
                              ["f_glass_lo", "f_band"], ["f_glass_lo", "f_rail_bottom"], ["f_hinge1", "p_fr"], ["f_hinge1", "f_stile_r"],
                              ["f_hinge2", "p_fr"], ["f_hinge3", "p_fr"], ["back_panel", "p_bl"], ["back_panel", "p_br"], ["back_panel", "lid_lip_back"],
                              ["sl_header", "p_fl"], ["sl_header", "p_bl"], ["sl_glass_up", "sl_header"], ["sl_glass_lo", "sl_rail_bottom"], ["sr_glass_up", "sr_band"],
                              ["pp_body", "back_panel"], ["pp_handset", "pp_body"], ["notice_frame", "back_panel"], ["lower_enclosure", "back_panel"]],
                    "embeds": [["f_hinge1", "f_stile_r", 5], ["f_hinge2", "f_stile_r", 5], ["f_hinge3", "f_stile_r", 5], ["f_hinge1", "p_fr", 5], ["f_hinge2", "p_fr", 5],
                               ["f_hinge3", "p_fr", 5], ["pp_handset", "pp_body", 5]],
                    "faces": [
                        {"id": "back", "o": [-Q, Q + 0.0, 100.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, 1, 0], "nu": 2 * Q, "nv": Z_SKIRT - 100.0, "depth": 10.0, "blockers": ["back_panel"]},
                        {"id": "roof", "o": [-LID, -LID, Z_TOP], "u": [1, 0, 0], "v": [0, 1, 0], "n": [0, 0, 1], "nu": 2 * LID, "nv": 2 * LID, "depth": 7.0, "blockers": ["lid_top"]},
                        {"id": "header front", "o": [-Q, -Q, Z_HEAD + 5.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": 2 * Q, "nv": Z_SKIRT - Z_HEAD - 10.0, "depth": 36.0, "blockers": ["f_header"]},
                        {"id": "handle band", "o": [-QG, -Q - 10.0, Z_BAND0 + 4.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": 2 * QG, "nv": Z_BAND1 - Z_BAND0 - 8.0, "depth": 33.0, "blockers": ["f_band"],
                         "apertures": [[0.0, 0.0, 52.0, 200.0]]},
                        {"id": "left side header", "o": [-Q, -QI + 2.0, Z_HEAD + 5.0], "u": [0, 1, 0], "v": [0, 0, 1], "n": [-1, 0, 0], "nu": 2 * QI - 4.0, "nv": Z_SKIRT - Z_HEAD - 10.0, "depth": 36.0, "blockers": ["sl_header"]},
                    ]},
            "KX2": {"name": "KX2: the doorless open kiosk (the 1985 'open booth' that the same makers supplied beside the door kind)", "parts": var_open,
                    "overall": {"w": 890.0, "d": 890.0, "h": 2192.0}, "overall_tol": 1.5, "noground": [],
                    "joins": [["p_fl", "lid_top"], ["f_header", "p_fl"], ["f_header", "p_fr"], ["back_panel", "p_bl"]], "embeds": [["pp_handset", "pp_body", 5]], "faces": []},
        },
        "drawing": {"views": ["front", "left", "back", "plan"],
                    "sections": [{"id": "x0", "axis": "x", "at": 0.0}, {"id": "z1000", "axis": "z", "at": 1000.0}, {"id": "z2140", "axis": "z", "at": 2140.0}]},
        "numbers": [
            {"id": "N1", "what": "overall height, ground to lid top", "value": 2192.0, "kind": "Read", "source": "britishtelephones.com KX kiosk page (read 13 Oct): Height 2192; the other site's 7 ft 1 in = 2159 is 33 mm (1.5 percent) lower and is kept as the alternative", "tol": 1.5,
             "measure": {"kind": "bbox", "axis": "z"}},
            {"id": "N2", "what": "overall width", "value": 890.0, "kind": "Read", "source": "same page: Width 890; the other site gives 2 ft 11 in = 889", "tol": 1.5, "measure": {"kind": "bbox", "axis": "x"}},
            {"id": "N3", "what": "overall depth", "value": 890.0, "kind": "Read", "source": "same page: Depth 890", "tol": 1.5, "measure": {"kind": "bbox", "axis": "y", "exclude": ["f_pull"]}},
            {"id": "N4", "what": "lid skirt depth", "value": 100.0, "kind": "Photo", "source": "P1 rows roof_top 67.1 to cap_bottom 96.3 (29.2 px) at 3.40 mm per px; error 12 mm", "tol": 12.0,
             "measure": {"kind": "extent", "axis": "z", "part": "lid_skirt_front"}},
            {"id": "N5", "what": "header height", "value": 270.0, "kind": "Photo", "source": "P1 rows cap_bottom 96.3 to header_bottom 176.0 (79.7 px) at 3.40 mm per px; error 15 mm", "tol": 15.0,
             "measure": {"kind": "extent", "axis": "z", "part": "f_header"}},
            {"id": "N6", "what": "handle band height", "value": 145.0, "kind": "Photo", "source": "P1 rows band_top 402.6 to band_bottom 445.3 (42.7 px); error 12 mm. P1's middle band is BLACK (post-1991 livery), so only its height comes from P1; the panel's form (the full-width moulded panel with a pull) comes from S2", "tol": 12.0,
             "measure": {"kind": "extent", "axis": "z", "part": "f_band"}},
            {"id": "N7", "what": "band centre above the ground", "value": 978.5, "kind": "Photo", "source": "P1 band centre row 424.0, scale from the lid top (67.1) to the bottom rail's lower edge (661.2); error 20 mm", "tol": 20.0,
             "measure": {"kind": "centre_z", "part": "f_band"}},
            {"id": "N8", "what": "gap between the bottom rail and the ground", "value": 163.0, "kind": "Photo", "source": "P1: post feet row about 709 (+-9) against rail_bottom 661.15: 48 px at 3.41 mm per px = 163 mm, error 35 mm (the first version kept 172 with no source; the review of 13 October asked for P1's 163 or a named source, and 163 is used)", "tol": 35.0,
             "measure": {"kind": "edge", "axis": "z", "part": "f_rail_bottom", "side": "lo"}},
            {"id": "N9", "what": "clear glazing width", "value": 686.0, "kind": "Photo", "source": "P1 columns glass_l 437.2 to glass_r 638.2 (201 px) at 3.40 mm per px; error 14 mm", "tol": 14.0,
             "measure": {"kind": "gap", "axis": "x", "a": "f_stile_l", "b": "f_stile_r"}},
            {"id": "N10", "what": "post face width (stainless strip seen from the front)", "value": 40.0, "kind": "Photo", "source": "P1 columns post_l_outer 410.3 to frame_l_outer 421.9 (11.6 px) = 39 mm; error 6 mm", "tol": 6.0,
             "measure": {"kind": "extent", "axis": "x", "part": "p_fl"}},
            {"id": "N11", "what": "door stile face width", "value": 52.0, "kind": "Photo", "source": "P1 columns frame_l_outer 421.9 to glass_l 437.2 (15.3 px) = 52 mm; error 8 mm", "tol": 8.0,
             "measure": {"kind": "extent", "axis": "x", "part": "f_stile_l"}},
            {"id": "N12", "what": "lid overhang each side beyond the posts", "value": 10.0, "kind": "Photo", "source": "P1: lid 17 mm wider than the posts' 870 in total (the lid is 890); error 6 mm", "tol": 6.0,
             "measure": {"kind": "gap", "axis": "x", "a": "lid_top", "b": "p_fl", "side_a": "lo", "side_b": "lo"}},
        ],
        "photos": [],
        "sources": [], "previews": [], "checks": [], "owed": [],
    }
    # numbers N7 and N12 need two more measure kinds
    T["numbers"][6]["measure"] = {"kind": "centre", "axis": "z", "part": "f_band"}
    T["numbers"][11]["measure"] = {"kind": "gap", "axis": "x", "a": "lid_top", "b": "p_fl", "side_a": "lo", "side_b": "lo"}
    # photograph P1: the features, with the fit on height only (lid top to the bottom rail's lower edge)
    feats = []
    ref = {"roof_top": ("y", "lid_top", "hi"), "cap_bottom": ("y", "lid_skirt_front", "lo"), "header_bottom": ("y", "f_header", "lo"),
           "band_top": ("y", "f_band", "hi"), "band_bottom": ("y", "f_band", "lo"), "rail_top": ("y", "f_rail_bottom", "hi"),
           "rail_bottom": ("y", "f_rail_bottom", "lo"), "post_l_outer": ("x", "p_fl", "lo"), "frame_l_outer": ("x", "p_fl", "hi"),
           "glass_l": ("x", "f_stile_l", "hi"), "glass_r": ("x", "f_stile_r", "lo"), "frame_r_outer": ("x", "p_fr", "lo"), "post_r_outer": ("x", "p_fr", "hi")}
    for fid, f in F.items():
        ax, part, side = ref[fid]
        band = f["band"]
        win = f["win"]
        box = [band[0], win[0], band[1], win[1]] if ax == "y" else [win[0], band[0], win[1], band[1]]
        err = max(4.0, 3.0 * f["spread"] + 2.0)
        feats.append({"id": fid, "axis": ax, "px": f["px"], "box": box, "tol_px": round(err, 1), "contrast": f["contrast"], "measure": {"axis": f["axis"], "band": f["band"], "win": f["win"], "pol": f["pol"]},
                      "ref": {"part": part, "side": side}, "anchor": fid in ("roof_top", "rail_bottom"), "boundary": fid in ("post_l_outer", "post_r_outer", "roof_top")})
    T["photos"].append({"id": "P1", "source": "S1", "file": "P1.jpg", "view": "front", "variant": "KX1", "object_box": PM["object_box"],
                        "fit": {"parts": ["lid_top", "f_rail_bottom"], "y_top_px": F["roof_top"]["px"], "y_bottom_px": F["rail_bottom"]["px"],
                                "x_centre_px": round((F["post_l_outer"]["px"] + F["post_r_outer"]["px"]) / 2, 2), "fitted_on": "height", "view": "front"},
                        "features": feats,
                        "method": "each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band on the kiosk's own face; the scale is fitted on the height from the lid's top edge to the bottom rail's lower edge only; the photograph leans about 1.8 degrees (the lid edge runs 4 px lower at the right) and the camera looks slightly down, so the tolerance is the measured spread plus 2 px, at least 4 px (14 mm)"})
    return T



SCRATCH_NOTE = "photographs are downloaded into /home/user/ledger-scratch/street-dressing/phone-box/ (outside git) by measure.py and by self_check.py --live"


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/5269043", "read": "2026-10-13", "author": "David Hillas", "licence": "CC BY-SA 2.0 (creativecommons.org/licenses/by-sa/2.0, read on the page)",
         "taken": "2017-01-04", "kind": "photograph",
         "shows": "a door-type KX100 in a village verge, head on, whole height, clear glass, the middle band black with a separate pink pull standing beyond the left edge at band height (post-1991), a pink 'Coins' header with a handset pictogram; roof, header, band, lower pane and the four posts all show; the grass hides the foot",
         "used": True, "not_used_for": "the livery (post-1991: the pink pull, the header's lettering and handset pictogram, the operator's printed logo and the notices, all painted out flat in the preview), the interior (painted out), the ground, the handle panel's form (P1's band is black: the form is S2's)",
         "period": "2017 photograph of a unit built 1985 to 1996; the structure is the same in 1990, the livery differs (1991 revamp), so it is used for geometry only"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/5558709", "read": "2026-10-13", "author": "David Hillas", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2017-07-19", "kind": "photograph",
         "shows": "a door-type KX100, nearer and looking down: the lid's rolled lip, the black channel frame, the stainless post with one round fixing, the moulded handle panel with its rectangular pull and finger recess, mud on the lower pane, plants at the foot",
         "used": True, "not_used_for": "measuring (the camera looks down about 25 degrees, the sides converge); the sticker on the lid, the etched figure and the notices (not period, real marks)",
         "period": "2017; unit of the same kind as 1990's apart from the 1991 livery"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/5314484", "read": "2026-10-13", "author": "David Hillas", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2017-02-17", "kind": "photograph",
         "shows": "the doorless KX100: the back panel, a payphone body with its keypad and handset, a notice frame, the stainless coin-vault housing above a low step, the two side panels seen from inside",
         "used": True, "not_used_for": "any number (oblique, the camera looks down); the notices' text and logos",
         "period": "2017; the same housing as 1990's"},
        {"id": "S4", "url": "https://www.britishtelephones.com/kxkiosk.htm", "read": "2026-10-13", "author": "the site's author (a hobbyist reference)", "licence": "read for facts only (nothing copied); facts are not licensed", "taken": "n/a (undated page)", "kind": "book",
         "shows": "KX100 dimensions Height 2192, Width 890, Depth 890 (mm), weight 266 kg; sides slightly raised above the ground against litter; the Mk2 'biscuit tin lid'; smoked glass at launch, clear later; the first handle panels yellow, 1991 pink",
         "used": True, "not_used_for": "any photograph or text copied", "period": "describes the 1985 to 1996 kiosk"},
        {"id": "S5", "url": "https://www.the-telephone-box.co.uk/kiosks/kx100/", "read": "2026-10-13", "author": "the site's author (a hobbyist reference)", "licence": "read for facts only", "taken": "n/a (undated page)", "kind": "book",
         "shows": "Height 7 ft 1 in, Width 2 ft 11 in; aluminium frame clad in stainless panels with anodised edging; black plastic modesty panel and trim; the first panels yellow, the phonecard kind green",
         "used": True, "not_used_for": "any number beyond the two dimensions (it gives 2159 x 889, which is 33 mm lower than S4; both are kept, S4 is chosen)", "period": "describes the 1985 to 1996 kiosk"},
        {"id": "S6", "url": "https://en.wikipedia.org/wiki/KX_telephone_boxes", "read": "2026-10-13 (raw wikitext through en.wikipedia.org)", "author": "Wikipedia contributors", "licence": "CC BY-SA 4.0 (the page's own)", "taken": "n/a (a text)", "kind": "book",
         "shows": "production 1985 to 1996, 3,000 a month in 1987 to 1989; the first deliveries had cylindrical levelling legs, a flat-sheet roof with upturned edges and a multi-panel back, the Mk2 followed with a single back sheet and the biscuit-tin lid; door panel and handle yellow (coin) or green (card) until the 1991 revamp; a windswept gap at the foot",
         "used": True, "not_used_for": "any picture", "period": "history of the 1985 to 1996 kiosk"},
        {"id": "S7", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "no British telephone box of any kind; the only phone is korean_public_payphone_01 (a post-mounted payphone, 401 x 301 x 740 mm)",
         "used": False, "not_used_for": "everything: no CC0 model fits, so the kiosk is made by script", "period": "n/a"},
        {"id": "S8", "url": "https://api.geograph.org.uk/syndicator.php (the feed; terms phone box, telephone box, telephone kiosk, KX100, phone kiosk, each with takenyear 1975 to 1996)", "read": "2026-10-13",
         "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "about 120 photographs of 1975 to 1996 with a telephone box in them, all of the older red boxes, one white box of a different municipal kind (1989) and one open-sided box named in a caption (1987); not one KX100 photograph before 2009 in about 400 results for the KX100 terms",
         "used": False, "not_used_for": "measuring: no period KX100 photograph was reached", "period": "n/a"},
        {"id": "S9", "url": "production/assets/street/clutter/kx100-kiosk.glb and tools/meshgen/blender/clutter/kx100_kiosk.py (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work",
         "taken": "made 29 September 2026", "kind": "own", "shows": "an earlier scripted kiosk: 0.89 square, 2.18 high, a 50 mm roof slab, header 200 high, band 1.00 to 1.12 m, panes 0.11 to 1.00 and 1.12 to 1.93, a 120 mm gap, the word Telephone in yellow",
         "used": True, "not_used_for": "its numbers (they disagree with P1 in six places, see the reuse table)", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-verge-kx100-front.jpg", "source": "S1", "credit": "David Hillas, Geograph 5269043, CC BY-SA 2.0, 2017-01-04, cropped to the kiosk; the operator's printed logo, the notices and the whole interior of the upper pane, the header's lettering and handset pictogram, and the sticker on the lower pane painted out flat",
         "masked": ["the whole upper pane inside the frame (flat fill by script: the operator's logo, the notices and the interior)", "the header's lettering and handset pictogram (flat pink)", "the sticker on the lower pane (flat fill)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p1-verge-kx100-target-on-photo.jpg", "source": "S1", "credit": "overlay of this target's front drawing (red) on the same crop (the scale fitted on the height from the lid's top edge to the bottom rail's lower edge, the measured edges in green); same photograph and masks",
         "masked": ["as p1"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p2-handle-kx100-detail.jpg", "source": "S2", "credit": "David Hillas, Geograph 5558709, CC BY-SA 2.0, 2017-07-19, cropped to the handle panel, the stainless post and the lower pane",
         "masked": ["the sticker, the etched figure and the notices are outside the crop"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    N = {n["id"]: n for n in T["numbers"]}
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the street's only light is the lantern colour; the kiosk shows it on the stainless (a warm orange wash on the brushed steel) and the glass reflects it; the kiosk's own interior lamp is OFF in the sample (an unlit kiosk is the safe 1990 night; a lit one is for his taste page later)"}
    T["placement"] = {
        "slot": "east side, where the scene has it: centre x 16.5 m, centre z 3.675 m (the scene's 0.55 m set-back is to the kiosk's CENTRE from the kerb's back edge at z 3.125), the door facing the shopfront (+z, as the scene's kiosk_door at z 4.132 does) and the back sheet to the road; the box's faces at z 3.230 and 4.120 (890 deep), 105 mm from the kerb's back edge in front and 855 mm from the stallriser line (z 4.975) behind the door",
        "scene_line": "furniture E3: east, x 16.5, setback 0.55 m (to the centre), plan 0.914, height 2.515 (K6 proportions): kiosk_plinth at z 3.675, faces at 3.218 and 4.132, door at z 4.132",
        "reasons": [
            "the slot is the scene's own and is kept: x 16.5, centre z 3.675. The first version moved the box to x 23.5 on two reasons that do not hold. (1) It read the scene's 0.55 m set-back as the distance to the kiosk's front face and so counted 2.0 - 0.55 - 0.89 = 0.56 m of footway; the 0.55 m is to the centre (vignette-pieces.json kiosk_plinth stands at z 3.675 with a 0.914 plan: faces at 3.218 and 4.132), so the strip between the kiosk and the stallriser face (4.975) is 0.843 m with the scene's box and 0.855 m with this target's 890 box, both over the 0.68 m a walker needs; there was no walking-width reason to move it. (2) It argued that a kiosk must not stand before Rita's window: that is an inference, not a ruling; the box stood there on 2 October when Jafar ruled both 'the KX100 phone box stays' and 'Rita's window is the model', so no ruling is read to forbid it",
            "the move to x 23.5 also failed the street's own pieces: the box (x 23.055 to 23.945, height 2192 on a footway 0.07 to 0.09 above the crown) lay under the empty unit's awning (awning_02 at x 24.0, x 22.5 to 25.5, its sheet 2.35 m above the crown over the box's front edge, its valance hanging to 1.63 m between z 3.39 and 3.40), left 0.45 to 0.6 m of walkable strip at head height in front of it, and stood across the empty unit's shop-door slot (x 22.294 to 23.300); the town's place for the kiosk (hook-cast.json places.kiosk, x 16.5, z 4.3, 'beside kiosk_plinth') and the meetings that use it (kiosk/ritas_step, kiosk/fish_counter) would have been 5.5 m from Rita's step. All of that is why the slot stays, and the shared placement rows (sd_place.py) now test the pose against every piece of vignette-pieces.json and the shopfronts target's door zones",
            "the town's place for the kiosk, hook-cast.json places.kiosk (x 16.5, z 4.3), lies 0.18 m beyond the door's face (4.120) and 0.15 m beyond the pull (4.148), inside the 855 mm strip: the people who meet there stand at the door, exactly as before; DECISIONS 30 September records that Marta steps onto Rita's step (x 18.0) so that her friendship with Alison at the kiosk still meets, 1.5 m away as before",
            "the door faces the shops, as the scene's own kiosk_door does (z 4.132); the back sheet, with the payphone's back, faces the road: from the hook camera (x -3, looking up the street) the player sees the stainless back and the lid, not the livery; the clear glazing of the sides shows the interior",
            "clear of the lamp column at x 28 east (11.5 m), the pillar box at x 27 (10.5 m), the fish market's board (x 14.45 after the A-board target, 1.6 m), the railing (x 10 to 12) and the awnings (x 10.5 to 13.5 and 22.5 to 25.5): the shared placement rows read each of them from the scene",
        ],
        "stallriser_line_z_m": 4.975, "kerb_back_z_m": 3.125, "kiosk_face_z_m": [3.230, 4.120], "clear_strip_mm": 855.0, "clear_strip_at_pull_mm": 827.0,
        "to_kerb_back_edge_mm": 105.0, "min_clear_mm": 680.0, "x_centre_m": 16.5, "z_centre_m": 3.675,
        "orientation": "the door faces +z in the street's frame (towards the shopfront), the back panel towards the road; the piece's own frame has the door at -y, so the pose's yaw is 180",
        "town_place": {"file": "production/specs/hook-cast.json", "place": "kiosk", "x_m": 16.5, "z_m": 4.3},
        "poses": [{"id": "kiosk", "variant": "KX1", "x_m": 16.5, "z_m": 3.675, "yaw_deg": 180.0, "zone": "east_footway", "front_faces": "+z",
                   "replaces": ["E3_"], "measure_exclude": ["f_pull"], "clear_behind_mm": 855.0, "clear_tol_mm": 6.0}],
    }
    T["wear"] = [
        "tide mark: dust and splash grime on both lower panes from the bottom rail up to about 350 mm, darkest in the lowest 100 mm, a clean line above (S2)",
        "streaks of rain-carried grime down the glass from the lid's skirt, three or four, 1 to 3 mm wide as a mask",
        "scratched patches and fine scratches on the lower pane at hand height and on the yellow handle panel (scuffed at the pull, paint dulled to 232, 188, 22)",
        "the stainless is water-stained near the foot and the lid's lower lip, never mirror bright",
        "the black frame faded to dark grey-brown on the sun side, dust in its channels, a few small round fixings visible on the posts (S2 shows one on the left post beside the handle panel)",
        "litter caught in the gap under the lower rail: two crisp-packet shapes and a few cigarette ends (tobacco is allowed), none inside the kiosk",
        "NOT shown: any card or sticker advertisement (the content rule), any person, any drink container, any real logo",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "size and proportion", "book": "the scene file (E3) draws 0.914 square and 2.515 high, a plinth 0.15, a cornice, post 0.1 and a cap 0.7 x 0.2: the proportions of the older red kiosk",
         "photo": "P1: height to width 2.51 measured over lid and posts (with the camera leaning), the printed KX100 gives 2192 / 890 = 2.46, the older kiosk 2.75; the lid, header, band and posts match the KX100", "chose": "890 x 890 x 2192; the scene's numbers are replaced"},
        {"id": "W2", "what": "roof", "book": "the 29 September script and the research note: a flat stainless slab 50 mm thick, slightly proud", "photo": "P1 and S2: a folded lid with a skirt about 100 mm deep all round and a rolled lip", "chose": "lid plate 3 mm on four 3 mm skirts 100 deep"},
        {"id": "W3", "what": "header height", "book": "the script: 200 mm (1.93 to 2.13 m)", "photo": "P1: header from the lid's lower edge to the glazing, 270 mm", "chose": "270 mm"},
        {"id": "W4", "what": "the handle band's height above the ground", "book": "the script: 1.00 to 1.12 m (a chest-high band 120 mm)", "photo": "P1: band 906 to 1051 mm, 145 mm high", "chose": "906 to 1051"},
        {"id": "W5", "what": "the foot", "book": "the script: panes begin 110 mm up and a floor plate stands inside", "photo": "P1: the bottom rail's lower edge 163 mm up (48 px), the posts alone reach the ground, no floor plate", "chose": "163 mm gap, no floor plate"},
        {"id": "W6", "what": "the lower enclosure", "book": "none", "photo": "S3 shows a stainless housing over a step; kept as a Judgement box", "chose": "lower_enclosure box, flagged Judgement"},
        {"id": "W7", "what": "the scene's set-back", "book": "the scene file: setback_from_kerb_m 0.55 and plan 0.914, read in the first version as 'the kiosk's front is 0.55 m from the kerb' (0.56 m of footway left)", "photo": "not a photograph: the scene's own kiosk_plinth stands at z 3.675 = 3.125 + 0.55 with a 0.914 plan, so 0.55 is to the CENTRE; the faces are at 3.218 and 4.132 and 0.843 m remains behind it", "chose": "the slot is kept (x 16.5, z 3.675); with the target's 890 box the strip behind is 0.855 m"},
        {"id": "W8", "what": "P1's middle band", "book": "the first version's S1 row: a post-1991 red-pink handle panel", "photo": "P1's band is black; the only colour is a separate pink pull standing beyond the left edge at band height (about x 388 to 405, y 405 to 435 on the 1024 copy); S2's door has the full-width coloured panel", "chose": "the band's height comes from P1, the panel's form from S2"},
    ]
    T["variants_note"] = [
        "KX1 (the sample): the door kiosk. It stands in the street.",
        "KX2: the doorless open kiosk (S3): the same lid, header, posts, back and payphone with no front leaf, glass, stiles or band; one more place for the town if it wants a second box (none in the scene today).",
        "conditions (materials, not shapes): C0 sound, C1 grimy (the sample's wear), C2 one lower pane cracked in a star from a point 1 m above the ground (a mask on the glass, not a mesh).",
        "glass: G0 clear (the sample), G1 smoked (transmission 0.55): the first deliveries of 1985 to 1986 and a few after; at most one in ten on the street.",
    ]
    T["text"] = {
        "header_word": "Telephone",
        "header_note": "the word is the plain English word, set in one line, upright, 100 mm tall letters in the middle of the header, in an OFL grotesque such as Liberation Sans (SIL OFL 1.1); no logo, no operator's name, no crown; colour a pale yellow-white (240, 224, 150); the mark the brand bible still owes is a placeholder: the upper pane's logo zone (centred, 300 x 300, from z 1250) stays empty",
        "logo_zone": [-150.0, 150.0, 1250.0, 1550.0],
        "forbidden": ["any real operator's name or logo", "a crown", "a cypher", "a card or advertisement", "a price"],
    }
    T["owed"] = [
        {"id": "O1", "line": "May the phone box's header carry the plain word Telephone, with no logo, until the town mints the Meridian operator's mark?",
         "recommended": "Yes, the plain word"},
    ]
    T["not_settled"] = [
        "the 1990 header's lettering colour (the research note says yellow on black; no 1985 to 1991 photograph was reached; chosen pale yellow-white, Judgement)",
        "the side fascia's height (S3 shows the header across the front; the side fascia is Judgement at the same height)",
        "the interior (payphone, enclosure and notice frame positions are Judgement within about 30 mm: S3 is oblique)",
        "whether Quay Street's box has a door (the sample has one; KX2 is the alternative)",
        "smoked or clear glass for the single box (clear chosen: from 1988 on most were clear)",
        "the exact lid lip profile (S2 shows a rolled lip; modelled as a 3 mm skirt with an 8 mm turned-in edge)",
    ]
    T["content_rule_note"] = "no cards, no stickers, no people, no drink, no betting, nobody young: the kiosk stands empty (a statement of the content rule)."
    T["builder_notes"] = [
        "build by script from the parts; every part is a box or cylinder with the edges stated in its row; weld the stainless into one shape per post; glass is a separate mesh with a glass material and 4 mm thickness",
        "replace production/assets/street/clutter/kx100-kiosk.glb with the new kiosk at the slot; the old asset stays in git",
        "UVs: stainless 1 m tiling brushed (horizontal grain on the lid and back, vertical on the posts); header and handle panel one texture each",
        "keep the foot gap open and the posts' feet 40 x 40 on the ground",
    ]
    # the builder's checks: from the numbers and the parts
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.1f mm" % n["value"], "tol": "+-%.1f mm" % n["tol"]})
    C += [
        {"name": "C1: three glazed faces and a solid back", "measure": "count the glazed faces (front, left, right) and the back sheet", "expect": "3 glazed, 1 solid", "tol": "exact"},
        {"name": "C2: three hinges on the right of the door", "measure": "count pivot hinges on the front's right post", "expect": "3", "tol": "exact"},
        {"name": "C3: the handle panel is proud of the frame", "measure": "the panel's front face minus the stile's front face", "expect": "10 mm", "tol": "+-3 mm"},
        {"name": "C4: the pull stands out of the panel", "measure": "the pull's front face minus the panel's front face", "expect": "28 mm", "tol": "+-6 mm"},
        {"name": "C5: no part floats and every join meets", "measure": "the contact graph of the meshes (touching within 2 mm)", "expect": "all parts reach the ground", "tol": "0 floating"},
        {"name": "C6: the back, lid and header are closed from the front, back and side at 0, 30 and 45 degrees", "measure": "rays at the stated faces", "expect": "0 get through", "tol": "exact"},
        {"name": "C7: the header word", "measure": "the text on the header", "expect": "Telephone", "tol": "exact"},
        {"name": "C9: the place", "measure": "the built kiosk's centre in the street's frame and the way its door faces", "expect": "x 16.5, centre z 3.675, door to +z", "tol": "+-0.05 m each, exact direction"},
        {"name": "C8: no real mark", "measure": "any text or logo on the model", "expect": "none but the header word", "tol": "exact"},
    ]
    T["checks"] = C
    return T


def doc(T):
    N = {n["id"]: n for n in T["numbers"]}
    V = T["variants"]["KX1"]
    pl = T["placement"]
    sc = T.get("self_check", {}).get("line", "SELF-CHECK phone-box: not yet run")
    out = []
    w = out.append
    w("# Quay Street's telephone box: the exact target")
    w("")
    w("**The phone box is the 1985-to-1991 stainless kind: 890 x 890 mm in plan and 2192 mm high, a folded stainless lid with a 100 mm skirt, four stainless corner posts 40 mm square, a 270 mm black header carrying only the word Telephone, glazed on three sides above and below a 145 mm band (the door's is a yellow moulded handle panel with a rectangular pull, the sides' black), a stainless back sheet with the payphone on it and a 163 mm open gap under the bottom rail; no operator's mark, no crown, no card advertisement; one box, standing where the scene has it (east x 16.5, centre z 3.675, the door to the shops, the back to the road: the first version\'s move to x 23.5 rested on a wrong number and is withdrawn); it replaces the 29 September script's kiosk, whose numbers disagree with the photograph in six places; no period KX100 photograph was reached, so the geometry is measured on a 2017 photograph of a unit of the same kind.**")
    w("")
    w("Cloud week 42, unit 13, family 1. Written 13 October 2026, not yet reviewed. `%s`" % sc)
    w("")
    w("## Files in this folder")
    w("")
    w("- `target.json`: the whole target (millimetres; z up; the door faces -y; pivot at the base's centre on the ground). Parts, numbers, photograph features, checks, owed lines.")
    w("- `make_target.py` (data and this page), `measure.py` (the pixel measurements on photograph P1), `photo_measurements.json` (their output), `target_drawing.py` (draws target.json alone), `self_check.py` (the checks and their negative controls), `make_previews.py` (the preview crops and the overlay).")
    w("- Previews in `production/previews/cloud-week/refs/street-dressing/phone-box/`: p1 (S1 cropped and masked), p1 target-on-photo, p2 (S2 detail).")
    w("- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`.")
    w("")
    w("## The rulings that bind, and how this target meets each")
    w("")
    w(D.table(["ruling", "what it says", "this target"], [
        ["RULINGS 2 Oct", "the KX100 phone box stays", "it is the KX100 kind (S4, S5, S6); one box on the street"],
        ["canon (brands)", "every brand fictional; the operator's mark and lettering are owed by the brand bible; no crown", "no logo, no operator's name; the plain word Telephone only; the logo zone stays empty (text.logo_zone)"],
        ["RULINGS 3 Oct (sources order)", "free assets first, else our own in Blender from real photographs", "no CC0 British kiosk exists (S7: 521 Poly Haven models, one non-British payphone); so own work by script (S9's route)"],
        ["content rule (canon D18)", "what the rule forbids is out of image and text", "no cards or stickers, no drink container, no one in any preview; the data scan finds none"],
        ["NoAI, licences", "nothing marked NoAI; photographs free licences, measuring only, never placed or traced", "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure; no NoAI source; nothing is placed in the game"],
        ["RULINGS 1 Oct and 3 Oct (the look)", "the Hook sheet and KCD2 frames; wet, dark, glistening street; accent budget (art-direction R-B4: red boxes carry the colour)", "stainless, black and glass are neutral; the yellow handle panel is the one saturated patch and stays small (145 x 686 mm); the red accent stays with the pillar box"],
        ["RULINGS 1 Oct (night)", "pools of lamp light, not one orange wash", "the lantern colour (1.0, 0.25, 0.0) linear only; the kiosk's own lamp is off in the sample (owed line O1 covers the lettering; a lit kiosk is a taste item for later)"],
        ["RULINGS 8 Oct", "photographs win over books, element by element", "section 'Where the photographs win' below; W1 to W8"],
        ["RULINGS 13 Oct (RECIPE)", "a notebook entry per unit", "RECIPE.md carries unit 13's entry"],
    ] + D.COMMON_RULINGS[-2:]))
    w("")
    w("## Sources")
    w("")
    w(D.sources_table(T))
    w("")
    w("What was searched: Geograph's feed for `phone box`, `telephone box`, `telephone kiosk`, `KX100`, `phone kiosk` with each year 1975 to 1996 and without a year (about 400 results for the KX100 terms alone). Wikimedia Commons was not asked (the feed answered). archive.org was not searched (no book of kiosk dimensions was expected there). Not reached: the second hobby site (redphonebox) refused the proxy (502), the C20 Society article was not opened (a lead only).")
    w("")
    w("## What already exists, and what is done with it")
    w("")
    w(D.table(["existing thing", "what it is", "verdict", "why"], [
        ["tools/meshgen/blender/clutter/kx100_kiosk.py and production/assets/street/clutter/kx100-kiosk.glb (29 Sep)", "a scripted 0.89 x 0.89 x 2.18 kiosk with a 50 mm roof slab, header 200, band 1.00 to 1.12, panes 0.11 to 1.00 and 1.12 to 1.93", "REPLACED (rebuilt from this target; its helper functions are reused)", "its numbers disagree with P1 in six places (W2 to W5 and the floor plate, section W); it also letters the header in yellow and has no payphone"],
        ["production/specs/vignette-scene.json, furniture E3", "a 0.914 square, 2.515 high kiosk with plinth and cap, east x 16.5", "REPLACED in size, parts and livery; its slot is KEPT", "K6 proportions (W1); the slot (east x 16.5, centre z 3.675, door to +z) is right: the set-back 0.55 m is to the kiosk's centre and leaves 0.843 m behind it"],
        ["production/research/street-clutter-1990, asset-plan 3 (A3 assemblies row)", "the KX100's frame, panes, band, door, handle panel, payphone, roof slab", "KEPT as the list of parts", "every named part is in the target"],
        ["Poly Haven models", "korean_public_payphone_01 and 520 others", "REJECTED", "no British kiosk; the payphone is post-mounted and Korean"],
        ["git branches (git log --all for phone box, kiosk, KX100)", "no other kiosk work", "none to reuse", "only the 29 September commit"],
    ]))
    w("")
    w("## The target")
    w("")
    w("Axes: x across the front (right is +x seen from the front), y from the door (-y) to the back (+y), z up from the ground. Every part is a box or a cylinder; its extents come from target.json and the self-check measures them back from the parts.")
    w("")
    w("### Assembly in words")
    w("")
    w("- **Four stainless posts** (40 x 40 box section, brushed, vertical edges r 3) stand on the ground at the corners and reach the lid's plate. They show 40 mm of stainless on each face.")
    w("- **The lid** is a folded stainless lid: a 3 mm plate over four 3 mm skirts 100 mm deep, its lower edge turned in 8 mm; it overhangs the posts by 10 mm each side (P1: 17 mm wider than the posts' 870).")
    w("- **The front (the door)** is a leaf hung on three stainless pivot hinges on the right post: black header 270 high and 30 deep; two black stiles 52 wide; a bottom rail 68 high; the yellow handle panel 145 high between the stiles, 10 proud, corners r 8, with a rectangular pull 50 x 66 standing 28 proud at the left (lock) end; two panes of 4 mm toughened glass, upper 1051 to 1822 and lower 231 to 906 (each 4 mm into the frame all round).")
    w("- **The two sides** are fixed frames like the front with a plain black band (flush with the posts) in place of the yellow panel and a black fascia the header's height above.")
    w("- **The back** is one stainless sheet, 6 mm with its backing, from the ground to the lid. The payphone body (140 wide), keypad, handset on the left and a notice frame hang on its inner face above a stainless coin-vault housing.")
    w("- **The foot** is open: only the posts and the back sheet reach the ground; the front and sides stop 163 mm up so litter blows through.")
    w("- **Fixings**: round pan-head fixings 4 mm across on the posts beside the handle panel (S2 shows one) and on the lid's skirt corners; no bolts on the glazing (gasketed). Joints: the lid's skirts meet at mitred corners; the header butts the posts; the frames are channels with a gasket line (a 1 mm dark line round each pane).")
    w("")
    w("### Parts, sample variant KX1 (millimetres)")
    w("")
    w(D.parts_table(T, "KX1"))
    w("")
    w("### The numbers, with their sources and kinds (the self-check measures each back off the parts)")
    w("")
    w(D.numbers_table(T))
    w("")
    w("### Photograph measurements (P1, S1)")
    w("")
    w(T["photos"][0]["method"] + ".")
    w("")
    w(D.photo_table(T))
    w("")
    w("### Materials and colours")
    w("")
    w(D.materials_table(T))
    w("")
    w("### Wear")
    w("")
    for x in T["wear"]:
        w("- " + x)
    w("")
    w("### Variants the street needs")
    w("")
    for x in T["variants_note"]:
        w("- " + x)
    w("")
    w("### Where it stands on Quay Street")
    w("")
    w("**Slot:** %s." % pl["slot"])
    w("")
    for r in pl["reasons"]:
        w("- " + r)
    w("")
    w("The scene's E3 line is not edited by this unit (it belongs to the scene's owner) and needs no change of place: the target replaces its size, parts and livery only. No move is asked of Jafar.")
    w("")
    w("### Lettering")
    w("")
    w("%s" % T["text"]["header_note"])
    w("")
    w("### Where the photographs win over the books")
    w("")
    w(D.table(["id", "what", "the book or script", "the photograph", "chosen"], [[d["id"], d["what"], d["book"], d["photo"], d["chose"]] for d in T["disagreements"]]))
    w("")
    w("### Checks for the builder (target.json `checks`)")
    w("")
    w(D.checks_table(T))
    w("")
    w("### For the builder")
    w("")
    for x in T["builder_notes"]:
        w("- " + x)
    w("")
    w("## Owed to Jafar's page (one line each, with a recommendation)")
    w("")
    w(D.owed_list(T))
    w("")
    w("## What the target could not settle")
    w("")
    for x in T["not_settled"]:
        w("- " + x)
    w("")
    w("## How the self-check is built")
    w("")
    w("`python self_check.py` (offline) rebuilds the parts' geometry and tests: the overall box against the printed numbers; every printed and photographed number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face (back, roof, header, handle band, side header) shot with rays square on and leaning 30 and 45 degrees, fine across one direction and coarse along the other; the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; this page regenerated and compared. `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each of about 20 negative controls is a deliberately wrong copy that must make the named row fail.")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    T = build()
    T = finish(T)
    tpath = os.path.join(HERE, "target.json")
    old = {}
    if os.path.exists(tpath):
        try:
            old = json.load(open(tpath)).get("self_check", {})
        except Exception:
            old = {}
    if old:
        T["self_check"] = old
    json.dump(T, open(tpath, "w"), indent=1)
    open(os.path.join(HERE, "TARGET.md"), "w", encoding="utf-8").write(doc(T))
    print("written:", len(T["variants"]["KX1"]["parts"]), "parts; TARGET.md", os.path.getsize(os.path.join(HERE, "TARGET.md")), "bytes")
