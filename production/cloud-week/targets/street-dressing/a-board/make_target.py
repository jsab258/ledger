"""a-board: writes target.json and TARGET.md (cloud week 42, unit 13, family 9: the A-board outside the fish market)."""
import copy
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY, PR, WIRE

FAMILY = "a-board"
PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))
P1, P2 = PM["P1"], PM["P2"]
F1, A1 = P1["features"], P1["arch_features"]

ALPHA = 12.0                                  # each leaf stands this far off the vertical (Judgement)
CA, SA = math.cos(math.radians(ALPHA)), math.sin(math.radians(ALPHA))

# AB1: the painted plywood board of the fish market (P1's type)
W1, LL1, TH1 = 600.0, 990.0, 12.0             # leaf width, leaf length along the slope, ply thickness
ARCH_H = 58.0                                 # height of the foot arch (P1: 34 px of 0.612 px per mm, along the slope)
FOOT_BASE = 118.0                             # width of each foot at the ground (P1: arch base 223.2 px of a 367.4 px leaf)
ARCH_TOP_HALF = 138.0                         # half width of the arch's flat top (read by eye, not measured)
STILE_W, STILE_D, STILE_X = 34.0, 18.0, 245.0 # back battens (Judgement, hidden from the front)
EYE_Z1 = 605.0                                # the chain's eye, measured along the leaf from the foot (P1: ring at 592 mm above the paving)
CHAIN_DEPTH1 = 242.0                          # how far the chain hangs below its eyes (P1: 148 px read by eye)

# AB2: the framed notice board of P2's type
W2, LL2, TH2 = 508.0, 762.0, 18.0
FRAME2 = 28.0
EYE_Z2 = 480.0
CHAIN_DEPTH2 = 170.0

HOURS_LINES = ["MON TO SAT 7.30 TO 2", "WED SHUT 1"]


def xf_of(side, LL):
    roll = -ALPHA if side == "F" else ALPHA
    return {"rot": [0.0, 0.0, roll], "pivot": [0.0, 0.0, float(LL)], "t": [0.0, 0.0, round(-LL * (1.0 - CA), 4)]}


def world(p, xf):
    R = L.rot(*xf["rot"])
    o = np.array(xf["pivot"], float)
    t = np.array(xf["t"], float)
    return (np.array(p, float) - o) @ R.T + o + t


def catenary(tip_a, tip_b, depth, n=16):
    """Points of a hanging chain between two tips at the same height, dropping `depth` below them (a catenary)."""
    ya, yb = tip_a[1], tip_b[1]
    hw = (yb - ya) / 2.0
    yc = (ya + yb) / 2.0
    lo, hi = 1.0, 20000.0
    for _ in range(200):
        a = (lo + hi) / 2.0
        d = a * (math.cosh(hw / a) - 1.0)
        if d > depth:
            lo = a
        else:
            hi = a
    a = (lo + hi) / 2.0
    pts = []
    for u in np.linspace(-1.0, 1.0, n + 1):
        pts.append([tip_a[0], yc + hw * u, tip_a[2] - depth + a * (math.cosh(hw * u / a) - 1.0)])
    return pts


def put(parts, side, LL):
    xf = xf_of(side, LL)
    for p in parts:
        p["xf"] = copy.deepcopy(xf)
    return parts


def Y(side, a, b):
    return (a, b) if side == "F" else (-b, -a)


def foot_poly(sign):
    pts = [(-W1 / 2.0, 0.0), (-(W1 / 2.0 - FOOT_BASE), 0.0), (-176.0, 14.0), (-165.0, 29.0), (-152.0, 42.0), (-143.0, 52.0), (-ARCH_TOP_HALF, ARCH_H), (-W1 / 2.0, ARCH_H)]
    if sign > 0:
        return [(-x, z) for x, z in reversed(pts)]
    return pts


def leaf1(pre, side):
    y0, y1 = Y(side, -TH1, 0.0)
    ys0, ys1 = Y(side, 0.0, STILE_D)
    yp0, yp1 = Y(side, 0.0, 3.0)
    ye = (-TH1 / 2.0) if side == "F" else (TH1 / 2.0)
    P = []
    P.append(B(pre + "main", -W1 / 2, W1 / 2, y0, y1, ARCH_H, LL1, "ply_paint", edge="arrises eased 2 mm; cut edges bare ply, one long strip of bare edge on the right",
               note="12 mm plywood leaf, 600 wide, from the arch's top to the ridge; the painted face is the front"))
    P.append(PR(pre + "foot_l", "xz", foot_poly(-1), y0, y1, "ply_paint", note="left foot, 118 wide at the ground, the arch's flared side up to the flat top"))
    P.append(PR(pre + "foot_r", "xz", foot_poly(+1), y0, y1, "ply_paint", note="right foot, the left one mirrored"))
    P.append(B(pre + "stile_l", -STILE_X - STILE_W / 2, -STILE_X + STILE_W / 2, ys0, ys1, 120.0, LL1 - 150.0, "timber", note="back batten 34 x 18, stops the ply bowing (Judgement, hidden)"))
    P.append(B(pre + "stile_r", STILE_X - STILE_W / 2, STILE_X + STILE_W / 2, ys0, ys1, 120.0, LL1 - 150.0, "timber"))
    P.append(B(pre + "rail", -(STILE_X - STILE_W / 2), STILE_X - STILE_W / 2, ys0, ys1, 380.0, 414.0, "timber", note="cross batten between the two"))
    P.append(B(pre + "hplate_l", -230.0, -180.0, yp0, yp1, LL1 - 60.0, LL1 - 8.0, "zinc", note="hinge leaf, 50 x 52 x 3, two screws (Judgement)"))
    P.append(B(pre + "hplate_r", 180.0, 230.0, yp0, yp1, LL1 - 60.0, LL1 - 8.0, "zinc"))
    P.append(CY(pre + "eye", (W1 / 2 - 4.0, ye, EYE_Z1), (W1 / 2 + 12.0, ye, EYE_Z1), 5.0, "zinc", note="screw eye in the right edge, 12 mm proud, holds the chain"))
    return put(P, side, LL1)


def build_ab1():
    P = leaf1("f_", "F") + leaf1("r_", "R")
    pz = round(LL1 * CA, 4)
    P.append(CY("hinge_pin_l", (-232.0, 0.0, pz), (-178.0, 0.0, pz), 4.0, "zinc", note="hinge knuckle on the ridge line, 8 mm"))
    P.append(CY("hinge_pin_r", (178.0, 0.0, pz), (232.0, 0.0, pz), 4.0, "zinc"))
    xf_f, xf_r = xf_of("F", LL1), xf_of("R", LL1)
    ta = world((W1 / 2 + 12.0, -TH1 / 2.0, EYE_Z1), xf_f)
    tb = world((W1 / 2 + 12.0, TH1 / 2.0, EYE_Z1), xf_r)
    P.append(WIRE("chain", catenary(ta, tb, CHAIN_DEPTH1), 2.5, "steel", note="a slack chain between the two screw eyes, 5 mm links, hanging free"))
    return P, ta, tb


def leaf2(pre, side):
    y0, y1 = Y(side, -TH2, 0.0)
    py0, py1 = Y(side, -12.0, -8.0)
    yp0, yp1 = Y(side, 0.0, 3.0)
    ye = (-TH2 / 2.0) if side == "F" else (TH2 / 2.0)
    P = []
    P.append(B(pre + "frame_l", -W2 / 2, -W2 / 2 + FRAME2, y0, y1, 0.0, LL2, "timber_frame", edge="arrises eased 2 mm", note="softwood frame strip 28 x 18, painted white, worn to the grain on the arrises"))
    P.append(B(pre + "frame_r", W2 / 2 - FRAME2, W2 / 2, y0, y1, 0.0, LL2, "timber_frame"))
    P.append(B(pre + "frame_t", -W2 / 2 + FRAME2, W2 / 2 - FRAME2, y0, y1, LL2 - FRAME2, LL2, "timber_frame"))
    P.append(B(pre + "frame_b", -W2 / 2 + FRAME2, W2 / 2 - FRAME2, y0, y1, 0.0, FRAME2, "timber_frame"))
    P.append(B(pre + "panel", -W2 / 2 + FRAME2, W2 / 2 - FRAME2, py0, py1, FRAME2, LL2 - FRAME2, "card_white", note="4 mm white board set 6 mm back from the frame's face, holds the notice"))
    P.append(B(pre + "hplate_l", -200.0, -150.0, yp0, yp1, LL2 - 60.0, LL2 - 8.0, "zinc"))
    P.append(B(pre + "hplate_r", 150.0, 200.0, yp0, yp1, LL2 - 60.0, LL2 - 8.0, "zinc"))
    P.append(CY(pre + "eye", (W2 / 2 - 4.0, ye, EYE_Z2), (W2 / 2 + 12.0, ye, EYE_Z2), 5.0, "zinc", note="screw eye in the right edge for the chain"))
    return put(P, side, LL2)


def build_ab2():
    P = leaf2("f_", "F") + leaf2("r_", "R")
    pz = round(LL2 * CA, 4)
    P.append(CY("hinge_pin_l", (-202.0, 0.0, pz), (-148.0, 0.0, pz), 4.0, "zinc"))
    P.append(CY("hinge_pin_r", (148.0, 0.0, pz), (202.0, 0.0, pz), 4.0, "zinc"))
    xf_f, xf_r = xf_of("F", LL2), xf_of("R", LL2)
    ta = world((W2 / 2 + 12.0, -TH2 / 2.0, EYE_Z2), xf_f)
    tb = world((W2 / 2 + 12.0, TH2 / 2.0, EYE_Z2), xf_r)
    P.append(WIRE("chain", catenary(ta, tb, CHAIN_DEPTH2), 2.5, "steel", note="a slack chain between the two screw eyes"))
    return P


def face(id, o_local, side, LL, nu, nv, depth, blockers, apertures=None):
    xf = xf_of(side, LL)
    R = L.rot(*xf["rot"])
    o = world(o_local, xf)
    v = R @ np.array([0.0, 0.0, 1.0])
    n = R @ np.array([0.0, -1.0 if side == "F" else 1.0, 0.0])
    d = {"id": id, "o": [round(float(x), 3) for x in o], "u": [1, 0, 0], "v": [round(float(x), 5) for x in v], "n": [round(float(x), 5) for x in n],
         "nu": nu, "nv": nv, "depth": depth, "blockers": blockers}
    if apertures:
        d["apertures"] = apertures
    return d


def build():
    P1parts, ta, tb = build_ab1()
    P2parts = build_ab2()
    d1 = 2.0 * (LL1 * SA + TH1 * CA)
    h1 = LL1 * CA + 4.0
    d2 = 2.0 * (LL2 * SA + TH2 * CA)
    h2 = LL2 * CA + 4.0
    joins1 = [["f_foot_l", "f_main"], ["f_foot_r", "f_main"], ["f_stile_l", "f_main"], ["f_stile_r", "f_main"], ["f_rail", "f_stile_l"], ["f_rail", "f_stile_r"], ["f_hplate_l", "f_main"], ["f_hplate_r", "f_main"],
              ["f_eye", "f_main"], ["r_foot_l", "r_main"], ["r_foot_r", "r_main"], ["r_stile_l", "r_main"], ["r_stile_r", "r_main"], ["r_rail", "r_stile_l"], ["r_rail", "r_stile_r"],
              ["r_hplate_l", "r_main"], ["r_hplate_r", "r_main"], ["r_eye", "r_main"], ["f_main", "r_main"], ["hinge_pin_l", "f_main"], ["hinge_pin_l", "r_main"], ["hinge_pin_r", "f_main"],
              ["hinge_pin_r", "r_main"], ["chain", "f_eye"], ["chain", "r_eye"]]
    embeds1 = [["f_eye", "f_main", 5.0], ["r_eye", "r_main", 5.0], ["hinge_pin_l", "f_main", 5.0], ["hinge_pin_l", "r_main", 5.0], ["hinge_pin_r", "f_main", 5.0], ["hinge_pin_r", "r_main", 5.0],
               ["f_main", "r_main", 5.0], ["chain", "f_eye", 5.0], ["chain", "r_eye", 5.0]]
    joins2 = [["f_frame_l", "f_frame_t"], ["f_frame_r", "f_frame_t"], ["f_frame_b", "f_frame_l"], ["f_frame_b", "f_frame_r"], ["f_panel", "f_frame_l"], ["f_panel", "f_frame_t"],
              ["f_hplate_l", "f_frame_t"], ["f_hplate_r", "f_frame_t"], ["f_eye", "f_frame_r"], ["r_frame_l", "r_frame_t"], ["r_frame_r", "r_frame_t"], ["r_frame_b", "r_frame_l"], ["r_frame_b", "r_frame_r"],
              ["r_panel", "r_frame_l"], ["r_panel", "r_frame_t"], ["r_hplate_l", "r_frame_t"], ["r_hplate_r", "r_frame_t"], ["r_eye", "r_frame_r"], ["f_frame_t", "r_frame_t"], ["hinge_pin_l", "f_frame_t"],
              ["hinge_pin_l", "r_frame_t"], ["hinge_pin_r", "f_frame_t"], ["hinge_pin_r", "r_frame_t"], ["chain", "f_eye"], ["chain", "r_eye"]]
    embeds2 = [["f_eye", "f_frame_r", 5.0], ["r_eye", "r_frame_r", 5.0], ["hinge_pin_l", "f_frame_t", 5.0], ["hinge_pin_l", "r_frame_t", 5.0], ["hinge_pin_r", "f_frame_t", 5.0], ["hinge_pin_r", "r_frame_t", 5.0],
               ["f_frame_t", "r_frame_t", 5.0], ["chain", "f_eye", 5.0], ["chain", "r_eye", 5.0]]
    T = {
        "family": FAMILY,
        "title": "Quay Street's A-board outside the fish market",
        "units": "millimetres; angles in degrees; z up; the front leaf's painted face looks -y and the back leaf's looks +y; the pivot is the centre of the two feet's line on the paving",
        "status": "written 13 October 2026, not yet reviewed",
        "sample": "AB1",
        "materials": {
            "ply_paint": {"name": "painted plywood, off-white, weathered", "srgb": [212, 213, 206], "rough": 0.6, "rough_words": "satin to matt, chalking", "metal": False,
                          "note": "emulsion over ply (P1: grey-white, a blue cast in shade); the lower 150 mm streaked grey with splash, the top edge and the right arris rust-brown where the ply's glue line weeps (P1)"},
            "timber": {"name": "softwood batten, bare", "srgb": [176, 140, 96], "rough": 0.8, "rough_words": "rough", "metal": False, "note": "back of the board, grey-brown, never painted"},
            "timber_frame": {"name": "softwood frame, white gloss, worn", "srgb": [226, 224, 214], "rough": 0.45, "rough_words": "gloss, chipped", "metal": False, "note": "knocked to bare wood on the arrises and the lower rail"},
            "card_white": {"name": "board panel, white", "srgb": [236, 235, 228], "rough": 0.7, "rough_words": "matt", "metal": False, "note": "holds a notice card; the notice is a decal, never part of this mesh"},
            "zinc": {"name": "zinc-plated steel, dull", "srgb": [140, 142, 140], "rough": 0.5, "rough_words": "satin", "metal": True, "note": "hinge leaves and knuckles, screw eyes: grey, a little rust at the screws"},
            "steel": {"name": "chain, bright steel gone dull", "srgb": [118, 118, 114], "rough": 0.45, "rough_words": "semi-gloss", "metal": True, "note": "5 mm links, a few with rust"},
        },
        "variants": {
            "AB1": {"name": "AB1: painted plywood board with a foot arch, fish list on both faces (the sample; the fish market's)", "parts": P1parts,
                    "overall": {"w": W1, "d": round(d1, 1), "h": round(h1, 1)}, "overall_tol": 1.5, "overall_exclude": ["f_eye", "r_eye", "chain"],
                    "joins": joins1, "embeds": embeds1,
                    "faces": [
                        face("front leaf outer face", (-W1 / 2, -TH1, ARCH_H), "F", LL1, W1, LL1 - ARCH_H, TH1 + 2.0, ["f_main"]),
                        face("back leaf outer face", (-W1 / 2, TH1, ARCH_H), "R", LL1, W1, LL1 - ARCH_H, TH1 + 2.0, ["r_main"]),
                        face("front leaf feet", (-W1 / 2, -TH1, 0.0), "F", LL1, W1, ARCH_H, TH1 + 2.0, ["f_foot_l", "f_foot_r"], apertures=[[FOOT_BASE - 16.0, 0.0, W1 - FOOT_BASE + 16.0, ARCH_H]]),
                        face("back leaf feet", (-W1 / 2, TH1, 0.0), "R", LL1, W1, ARCH_H, TH1 + 2.0, ["r_foot_l", "r_foot_r"], apertures=[[FOOT_BASE - 16.0, 0.0, W1 - FOOT_BASE + 16.0, ARCH_H]]),
                    ]},
            "AB2": {"name": "AB2: framed notice board of the 1978 type (smaller; for the newsagent or the tea room, not placed today)", "parts": P2parts,
                    "overall": {"w": W2, "d": round(d2, 1), "h": round(h2, 1)}, "overall_tol": 1.5, "overall_exclude": ["f_eye", "r_eye", "chain"],
                    "joins": joins2, "embeds": embeds2,
                    "faces": [
                        face("front leaf outer face", (-W2 / 2, -TH2, 0.0), "F", LL2, W2, LL2, TH2 + 2.0, ["f_panel", "f_frame_l", "f_frame_r", "f_frame_t", "f_frame_b"]),
                        face("back leaf outer face", (-W2 / 2, TH2, 0.0), "R", LL2, W2, LL2, TH2 + 2.0, ["r_panel", "r_frame_l", "r_frame_r", "r_frame_t", "r_frame_b"]),
                    ]},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "z300", "axis": "z", "at": 300.0}, {"id": "z800", "axis": "z", "at": 800.0}]},
    }
    # numbers
    sL = (F1["right_top"]["px"] + F1["right_bot"]["px"] - F1["left_top"]["px"] - F1["left_bot"]["px"]) / 2.0   # leaf width in px (367.4)
    s_px = sL / W1
    hproj = (F1["foot_left_y"]["px"] - F1["top_y"]["px"]) / s_px
    T["numbers"] = [
        {"id": "N1", "what": "leaf width", "value": W1, "kind": "Judgement", "source": "a 600 mm (2 ft) board; assumed, and it sets P1's scale (%.4f px per mm from the leaf's width of %.1f px); error 15" % (s_px, sL), "tol": 15.0, "measure": {"kind": "local", "part": "f_main", "axis": "x", "what": "extent"}},
        {"id": "N2", "what": "leaf length along the slope", "value": LL1, "kind": "Photo", "source": "P1: leaf height %.1f px (top edge to the foot's lower edge) = %.0f mm projected; over the lean's cosine (%.3f) with a 2.5 mm thickness term gives about 986; 990 kept (error 25)" % (F1["foot_left_y"]["px"] - F1["top_y"]["px"], hproj, CA), "tol": 25.0, "measure": {"kind": "local", "part": "f_main", "axis": "z", "what": "hi"}},
        {"id": "N3", "what": "ply thickness", "value": TH1, "kind": "Judgement", "source": "12 mm plywood (P1's bare edge strip is about 6 px = 10 mm at the lean; the standard sheet is 12); error 3", "tol": 3.0, "measure": {"kind": "local", "part": "f_main", "axis": "y", "what": "extent"}},
        {"id": "N4", "what": "foot arch height", "value": ARCH_H, "kind": "Photo", "source": "P1: from the feet (mean of two, %.1f px) up to the arch top (%.1f px) is %.1f px = %.0f mm projected; error 6" % ((F1["foot_left_y"]["px"] + F1["foot_right_y"]["px"]) / 2.0, F1["arch_top_y"]["px"], (F1["foot_left_y"]["px"] + F1["foot_right_y"]["px"]) / 2.0 - F1["arch_top_y"]["px"], ((F1["foot_left_y"]["px"] + F1["foot_right_y"]["px"]) / 2.0 - F1["arch_top_y"]["px"]) / s_px), "tol": 6.0, "measure": {"kind": "local", "part": "f_main", "axis": "z", "what": "lo"}},
        {"id": "N5", "what": "each foot's width at the ground", "value": FOOT_BASE, "kind": "Photo", "source": "P1: the left foot %.1f px and the right foot %.1f px at 0.612 px per mm = %.0f and %.0f mm; error 8" % (A1["arch_base_left_x"]["px"] - (F1["left_bot"]["px"]), F1["right_bot"]["px"] - A1["arch_base_right_x"]["px"], (A1["arch_base_left_x"]["px"] - F1["left_bot"]["px"]) / s_px, (F1["right_bot"]["px"] - A1["arch_base_right_x"]["px"]) / s_px), "tol": 8.0, "measure": {"kind": "local", "part": "f_foot_l", "axis": "x", "what": "extent", "where": {"axis": "z", "lo": -1.0, "hi": 1.0}}},
        {"id": "N6", "what": "half width of the arch's flat top", "value": ARCH_TOP_HALF, "kind": "Judgement", "source": "read by eye on a 3 times crop of P1 (the flat top ends about 85 px from the centre); not measured by the algorithm; error 15", "tol": 15.0, "measure": {"kind": "local", "part": "f_foot_r", "axis": "x", "what": "lo"}},
        {"id": "N7", "what": "lean of each leaf off the vertical (degrees)", "unit": "deg", "value": ALPHA, "kind": "Judgement", "source": "12 degrees, the usual set of a pavement board; P1 is a front view and cannot show the lean; error 3", "tol": 3.0, "measure": {"kind": "xf", "part": "f_main", "index": 2}},
        {"id": "N8", "what": "height to the ridge (top of the hinge knuckles)", "value": round(h1, 1), "kind": "Photo", "source": "P1: %.1f px from the top edge to the lower foot edge = %.0f mm projected (the front leaf's own top is 2.5 mm over the ridge line); the hinge knuckles 4 mm over; error 30" % (F1["foot_left_y"]["px"] - F1["top_y"]["px"], hproj), "tol": 30.0, "measure": {"kind": "bbox", "axis": "z", "exclude": ["f_eye", "r_eye", "chain"]}},
        {"id": "N9", "what": "depth of the standing board (foot to foot)", "value": round(d1, 1), "kind": "Judgement", "source": "from the lean and the length: 2 x (990 x sin 12 + 12 x cos 12) = 435; the scene's placeholder was 357 deep; error 40", "tol": 40.0, "measure": {"kind": "bbox", "axis": "y", "exclude": ["f_eye", "r_eye", "chain"]}},
        {"id": "N10", "what": "chain: from its lowest point up to the top of its eye", "value": CHAIN_DEPTH1 + 7.5, "kind": "Photo", "source": "P1: the ring at y 272 and the chain's lower end at y 420, read by eye on a 4 times crop (+-8 px): 148 px = %.0f mm below the eye; the eye's radius 5 and the chain's 2.5 added; error 40" % (148.0 / s_px), "tol": 40.0, "measure": {"kind": "span", "axis": "z", "a": "chain", "b": "f_eye"}},
        {"id": "N11", "what": "screw eye's height above the paving", "value": None, "kind": "Photo", "source": "", "tol": 30.0, "measure": {"kind": "centre", "axis": "z", "part": "f_eye"}},
        {"id": "N12", "what": "distance between the two hinges", "value": 410.0, "kind": "Judgement", "source": "two butt hinges 205 mm either side of the middle (hidden on the inner faces; typical); error 30", "tol": 30.0, "measure": {"kind": "centre_dx", "axis": "x", "a": "hinge_pin_l", "b": "hinge_pin_r"}},
        {"id": "N20", "variant": "AB2", "what": "AB2 leaf width", "value": W2, "kind": "Judgement", "source": "20 inches; P2's board is 60.6 px wide beside a bus tyre of about 128 px (taken as 1.0 m): about 0.47 m (+-15 percent), so the 508 mm board is the nearest standard; error 60", "tol": 60.0, "measure": {"kind": "local_span", "axis": "x", "a": "f_frame_l", "b": "f_frame_r"}},
        {"id": "N21", "variant": "AB2", "what": "AB2 leaf length", "value": LL2, "kind": "Judgement", "source": "30 inches; P2's board is 91.3 px high (projected) = about 0.71 m of tyre-scaled height, 0.73 m along the slope; error 70", "tol": 70.0, "measure": {"kind": "local", "part": "f_frame_l", "axis": "z", "what": "extent"}},
        {"id": "N22", "variant": "AB2", "what": "AB2 frame strip width", "value": FRAME2, "kind": "Judgement", "source": "28 mm softwood strip; P2's frame is about 3 px wide, below the pixel's reach; error 6", "tol": 6.0, "measure": {"kind": "local", "part": "f_frame_l", "axis": "x", "what": "extent"}},
        {"id": "N23", "variant": "AB2", "what": "AB2 frame depth", "value": TH2, "kind": "Judgement", "source": "18 mm; error 4", "tol": 4.0, "measure": {"kind": "local", "part": "f_frame_l", "axis": "y", "what": "extent"}},
    ]
    # N11 value: the P1 ring height above the foot line, projected, over the cosine
    ring_z = (F1["foot_left_y"]["px"] - 272.0) / s_px
    for n in T["numbers"]:
        if n["id"] == "N11":
            n["value"] = round(ring_z, 0)
            n["source"] = "P1: the ring at y 272 (read by eye) is %.0f px above the left foot's lower edge = %.0f mm; error 30" % (F1["foot_left_y"]["px"] - 272.0, ring_z)
    # photographs
    refs = {"left_top": ("x", "f_main", "lo"), "left_bot": ("x", "f_foot_l", "lo"), "right_top": ("x", "f_main", "hi"), "right_bot": ("x", "f_foot_r", "hi"),
            "top_y": ("y", "f_main", "hi"), "foot_left_y": ("y", "f_foot_l", "lo"), "foot_right_y": ("y", "f_foot_r", "lo"), "arch_top_y": ("y", "f_main", "lo")}
    pm = dict(P1)
    pm["features"] = {k: v for k, v in F1.items() if k in refs}
    ph1 = SF.photo_entry(pm, "P1", "S1", "AB1", refs, ["f_main", "f_foot_l", "f_foot_r"], anchors=("top_y", "foot_left_y"),
                         boundary=("left_top", "left_bot", "right_top", "right_bot", "top_y", "foot_left_y", "foot_right_y"),
                         fit_top="top_y", fit_bottom="foot_left_y",
                         centre_from=lambda FF: (FF["left_top"]["px"] + FF["left_bot"]["px"] + FF["right_top"]["px"] + FF["right_bot"]["px"]) / 4.0, min_tol=5.0, file="P1rot.jpg",
                         method="the photograph was first turned 2.6 degrees about (265, 335) because the board's vertical edges ran 2 to 3 degrees off the picture's vertical (the left edge moved 22 px and the right edge 14 px over 420 rows); each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band; the scale is fitted on the one height from the leaf's top edge to the left foot's lower edge (592.3 px) and the width, the right foot, the arch and the centre are predicted from it; the leaf's width of 600 mm is the unit that sets the absolute size (Judgement), so the check is of proportions; the tolerance is the measured spread times 3 plus 2 px, at least 5 px (8 mm); the right foot sits 4.2 px higher than the left in the picture (the ground slopes), inside the tolerance")
    ph1["rotated"] = P1["rotated"]
    T["photos"] = [ph1]
    # P2: the framed notice board, ratio only (no scale fit: the board is tilted and sheared in the picture)
    F2 = P2["features"]
    feats = []
    refs2 = {"left_x": ("x", "f_frame_l", "lo"), "right_x": ("x", "f_frame_r", "hi"), "top_y": ("y", "f_frame_t", "hi"), "bottom_y": ("y", "f_frame_b", "lo")}
    for fid, f in F2.items():
        ax, part, side = refs2[fid]
        band, win = f["band"], f["win"]
        box = [band[0], win[0], band[1], win[1]] if ax == "y" else [win[0], band[0], win[1], band[1]]
        feats.append({"id": fid, "axis": ax, "px": f["px"], "box": box, "tol_px": round(max(4.0, 3.0 * f["spread"] + 2.0), 1), "contrast": f["contrast"],
                      "measure": {"axis": f["axis"], "band": band, "win": win, "pol": f.get("pol", "any")}, "ref": {"part": part, "side": side}, "anchor": False, "boundary": True})
    wpx = F2["right_x"]["px"] - F2["left_x"]["px"]
    hpx = F2["bottom_y"]["px"] - F2["top_y"]["px"]
    T["photos"].append({"id": "P2", "source": "S2", "file": "P2.jpg", "view": "front", "variant": "AB2", "object_box": P2["object_box"], "features": feats,
                        "ratio": {"width_px": round(wpx, 2), "height_px": round(hpx, 2), "width_over_height": round(wpx / hpx, 4), "tol": 0.05,
                                  "note": "taken at rows 500 to 520 and columns 505 to 535; the board is sheared about 6 degrees in the picture (its left edge moves 7 px and its right edge 9 px over 65 rows) and tilted back, so only the ratio is used"},
                        "method": "each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band; no scale is fitted (the board's plane is neither square on nor level); only the projected width over the projected height is used, against the same ratio of the AB2 front leaf's drawing"})
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/3671864", "read": "2026-10-13", "author": "Walter Baxter", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2013-09-14", "kind": "photograph",
         "shows": "a painted plywood A-board on a village pavement, front leaf square on: a plain rectangle with two feet and a flared arch cut in its lower edge, painted lettering in black, pink and blue, a bare-ply edge strip on its right side, the back leaf's edge beside it, and a loose steel chain hanging from a screw eye in the right edge",
         "used": True, "not_used_for": "any lettering or name (it names a tea room and carries a hard-hat picture; none is copied), the colours of the lettering, any absolute size (no scale object; the leaf's width is assumed), the lean (a front view)",
         "period": "2013 photograph of a home-made board of a type that was common long before 1990 (ply, hinges, chain, foot arch); it is the construction that is used, never its date"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/6913397", "read": "2026-10-13", "author": "Alan Murray-Rust", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "1978-08-04", "kind": "photograph",
         "shows": "a framed white notice board leaning against the front of an open-top tour bus on a bus station apron: a thin timber frame holding a white panel with a printed card, standing on the ground at a lean; people and a bus operator's marks are in the picture",
         "used": True, "not_used_for": "the people (not drawn, not in any preview), the operator's name and plates (real marks, masked), the card's wording, the board's absolute size (the bus tyre as a scale is judged to 15 percent)",
         "period": "1978: the only 1975 to 1995 photograph of a pavement board that was found; 12 years before the game but the same trade type"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/2783627", "read": "2026-10-13", "author": "HelenK", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2012-01-27", "kind": "photograph",
         "shows": "a green-bordered black chalkboard on an A-frame with an arched top outside a cafe, on a wet pavement beside a road",
         "used": False, "not_used_for": "everything: looked at and set aside; a painted chalk menu board with an arched top is a 2010s fashion that no 1975 to 1995 photograph found here supports, and it is not a fishmonger's board", "period": "2012"},
        {"id": "S4", "url": "https://www.geograph.org.uk/photo/2808162", "read": "2026-10-13", "author": "John Baker", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "1984-04-13", "kind": "photograph",
         "shows": "a narrow shopping street in York in 1984 with hanging signs and a plain board fixed to a wall; no pavement board is in the picture",
         "used": False, "not_used_for": "everything: looked at for 1980s street signage; it shows no A-board", "period": "1984"},
        {"id": "S5", "url": "https://api.geograph.org.uk/syndicator.php (terms sandwich board, pavement board, a-board, shop, shops, cafe, pavement, street, market, fish, chip, takeaway, butcher, bakery, newsagent, board, sign, blackboard, menu; each with takenyear 1975 to 1996)",
         "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "no 1980 to 1995 photograph whose caption or text names an A-board, sandwich board or pavement board; the year-filtered search for sandwich board gave two hits (a 1978 bus station, which is S2, and a 1985 dock view in Hull, read by caption only); the unfiltered searches gave 200 distinct photographs, 197 of them taken in 2006 or later, the other three being S2, that Hull dock view and a 1986 York street named Pavement",
         "used": False, "not_used_for": "measuring (the hits were read for what they show, S2 aside)", "period": "n/a"},
        {"id": "S6", "url": "https://api.polyhaven.com/assets?t=models and /info/standing_chalkboard_01 (this folder's polyhaven_checked_raw.json)", "read": "2026-10-13", "author": "ParzivalCG (Poly Haven)", "licence": "CC0 1.0", "taken": "published 2021-12-24",
         "kind": "model list", "shows": "of 521 models only two are signs: standing_chalkboard_01 (an A-frame chalkboard 920 x 759 x 1509 mm, a cafe menu board; base colour checked at 100 percent: dark grey with chalk smudges and bare wood, no lettering) and WetFloorSign_01 (a yellow hazard sign 300 x 359 x 630 mm)",
         "used": False, "not_used_for": "this board: the chalkboard is 1.5 m tall and a cafe's, not a fishmonger's 0.97 m painted board; it stays held for the tea room (the asset plan's line)", "period": "n/a"},
        {"id": "S7", "url": "production/specs/vignette-scene.json (held_props pavement_sign at east x 15.2, the railing note, the awning at x 12.0, the decals block) and production/specs/vignette-bill-of-materials.json (E12, G6) (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the placeholder board 0.68 x 0.90 x 0.36 m at x 15.2, 1.1 m from the kerb face, its faces turned along the pavement; the awning over the fish market at x 12.0; the 29 September finding that a gap under 0.68 m is too narrow to walk; the board's text is to come from the gig-bill decals (G6)",
         "used": True, "not_used_for": "the board's size and place (both are replaced) and its text (the fish list replaces the gig bill)", "period": "n/a"},
        {"id": "S8", "url": "production/research/shop-window-interiors/FISHMONGER-2026-10-03.md (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "3 October 2026", "kind": "own",
         "shows": "the ONS cod fillet price of 1990 (574p/kg, about 2.60 a pound), prices per pound, hand-lettered tickets and whitewash lettering, the fish a 1990 shop sold",
         "used": True, "not_used_for": "any price except cod (no 1990 figure was found for the other fish: they are marked invented in text.lines)", "period": "1990 figures"},
        {"id": "S9", "url": "production/specs/hook-cast.json (places fish_front, fish_counter; area fish_market hours) and RULINGS.md (3 Oct trades) (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the fish market's hours (Monday to Saturday, opening 7.30, closing 14.00, Wednesday 13.00), its pavement spot at x 12.0, z 4.2 and a doorway about x 9.4; bay 1 is the fishmonger",
         "used": True, "not_used_for": "the board's design", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-village-board-front-leaf.jpg", "source": "S1", "credit": "Walter Baxter, Geograph 3671864, CC BY-SA 2.0, 2013-09-14, turned 2.6 degrees and cropped to the board; all lettering and the picture blurred beyond reading (script)",
         "masked": ["the lettering and the hard-hat picture on the board's face (blurred by script)", "the tea room's name in the lettering (blurred)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p1-village-board-target-on-photo.jpg", "source": "S1", "credit": "overlay of this target's front drawing (red; the battens, rail and hinge leaves behind the ply and the back leaf are drawn as well) on the same crop, the scale fitted on the height from the leaf's top edge to the left foot, measured edges in green",
         "masked": ["as p1"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p2-1978-notice-board.jpg", "source": "S2", "credit": "Alan Murray-Rust, Geograph 6913397, CC BY-SA 2.0, 1978-08-04, cropped to the board; the board's print, the bus's body and the tyre and the ground left of it blurred (script); no person is in the crop",
         "masked": ["the card's print and the operator's mark on it (blurred by script)", "the bus's lettering, the tyre and the ground left of the board (blurred)", "people (outside the crop)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    lines = [
        {"id": "head", "text": "FRESH FISH", "price": None, "h": 70.0, "z_top": 930.0, "align": "centre", "basis": "heading"},
        {"id": "cod", "text": "COD FILLET", "price": "2.60 LB", "h": 36.0, "z_top": 800.0, "align": "split", "basis": "sourced: ONS 1990, 574p/kg, about 2.60 a pound (S8)"},
        {"id": "haddock", "text": "HADDOCK", "price": "2.35 LB", "h": 36.0, "z_top": 735.0, "align": "split", "basis": "invented: a little under cod; no 1990 figure was found"},
        {"id": "plaice", "text": "PLAICE", "price": "2.10 LB", "h": 36.0, "z_top": 670.0, "align": "split", "basis": "invented; no 1990 figure was found"},
        {"id": "kippers", "text": "KIPPERS", "price": "1.45 LB", "h": 36.0, "z_top": 605.0, "align": "split", "basis": "invented; no 1990 figure was found"},
        {"id": "crab", "text": "DRESSED CRAB", "price": "95P EACH", "h": 36.0, "z_top": 540.0, "align": "split", "basis": "invented; no 1990 figure was found"},
        {"id": "hours1", "text": HOURS_LINES[0], "price": None, "h": 34.0, "z_top": 400.0, "align": "centre", "basis": "the market's hours, hook-cast.json (S9)"},
        {"id": "hours2", "text": HOURS_LINES[1], "price": None, "h": 34.0, "z_top": 340.0, "align": "centre", "basis": "the market's Wednesday close, hook-cast.json (S9)"},
    ]
    T["text"] = {
        "variant": "AB1", "carrier": "the fish market (bay 1), RULINGS 3 Oct", "shop_name": None,
        "no_name": "no shop name on the board and no logo; the fish market is the fish market (hook-cast names: the fish market, the fishmonger's, the market)",
        "style": "hand-painted signwriter's capitals in black emulsion on the off-white leaf, a plain upright narrow face; letters of uneven height by 2 to 3 percent, not a font on the final mesh (the decal is painted by hand, then ground into the wear)",
        "cap_width_factor": 0.62, "margin_mm": 40.0, "gap_mm": 60.0, "currency": "pounds and pence as 2.60 and pence as 95P, the price is per pound (LB) unless EACH",
        "faces": "both outer faces carry the same list (the board's two faces look up and down the pavement), the back leaf's lines identical",
        "lines": lines,
        "ab2_note": "AB2 carries a notice card of 400 x 640 whose wording is a decal chosen by the street (never this target); no shop name",
    }
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the board is not out at night: the fish market shuts at 14.00 (13.00 on Wednesdays) and the board goes indoors; in a dusk shot it stands in the dark between lamp pools (the nearest lamp column is x 8 east, 6 m away) and its off-white face takes the lantern colour only as a faint wash on the face turned towards the lamp"}
    pl = {
        "slot": "east pavement outside the fish market (bay 1, x 9 to 15): centre x 14.45 m, centre z 4.600 m (1.60 m from the kerb face), the board's two faces looking up and down the pavement (the scene's yaw 90), its back leaf's feet 0.063 m clear of the stallriser line; it replaces the scene's line at x 15.2, 1.1 m from the kerb face",
        "x_m": 14.45, "z_m": 4.600, "yaw_deg": 90, "kerb_face_z_m": 3.0, "kerb_back_z_m": 3.125, "stallriser_line_z_m": 4.975, "frontage_z_m": 5.125,
        "across_half_mm": 312.0, "along_half_mm": 217.6, "min_clear_mm": 1000.0, "walking_person_mm": 680.0,
        "pilaster_x_m": 15.0, "pilaster_half_mm": 175.0, "pilaster_gap_min_mm": 100.0,
        "awning_x_m": [10.5, 13.5], "awning_gap_min_mm": 500.0, "fish_front": {"x_m": 12.0, "z_m": 4.2, "min_m": 1.0}, "fish_door_x_m": 9.4, "door_gap_min_m": 2.0,
        "old": {"x_m": 15.2, "z_from_kerb_face_m": 1.1, "across_mm": 681.1, "source": "vignette-scene.json held_props pavement_sign"},
        "reasons": [
            "the scene's line stood at x 15.2 with its 0.68 m width across the pavement and its centre 1.1 m from the kerb face: it left 0.64 m on the kerb side and 0.54 m on the shop side of a 1.85 m footway, both under the 0.68 m of a walking person (the 29 September walk found the footway walled by a smaller obstruction), and its depth put it on the line of the party pilaster between the fish market and Rita's",
            "against the stallriser the board leaves 1.16 m clear on the kerb side, over the 1.0 m this target requires; the board is a shopkeeper's, put where the pavement is widest beside the shop",
            "x 14.45 is in front of the fish market's own window (bay 1 is x 9 to 15, RULINGS 3 Oct) and clear of Rita's (the pilaster face is 0.157 m beyond the board's end); the awning (x 10.5 to 13.5) is 0.73 m away and the pavement spot where the cast stands (x 12.0, z 4.2) is 2.5 m away, so nobody who waits at the fish market stands behind the board",
            "the fish market's doorway is at about x 9.4 and the board stands 5 m from it, so no door is blocked; the railing by the gully (x 10 to 12) is 2.2 m away",
            "the faces look along the pavement, as the scene had them: a board read by people walking up or down the street; the leaf's long side lies across the pavement",
            "the board is out only in the market's hours (Monday to Saturday from 7.30, shut at 14.00, Wednesday 13.00); a night frame has no board",
        ],
    }
    T["placement"] = pl
    T["wear"] = [
        "the leaf's paint is chalking off-white with a grey splash band to 150 mm above the paving, the lower arris and the feet's edges worn to bare ply; the top edge and the right arris carry rust-brown weeping from the glue line (P1)",
        "lettering is hand-painted and slightly uneven; one letter is overpainted in a second colour (P1 shows a word corrected in blue): a decal detail, not a mesh one",
        "the feet's arch is dirty to its flared edges; the ply swells at the foot's corners (a 2 mm lift) and the lower 40 mm of the bare edge is dark",
        "the screw eyes are grey with a rust ring; the chain is dull, two links rusted, hanging in a deep loop between the leaves (P1)",
        "the back of each leaf is bare grey-brown batten and ply, never painted",
        "NOT shown: a shop name, an advertisement, a person, a drink, a bet, a real brand on any face",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "the board's size", "book": "the scene's placeholder: 0.68 x 0.90 x 0.36 m", "photo": "S1: a leaf about 600 wide and 1.65 times as long, two feet, a chain between the leaves; S2: a smaller framed board about 0.5 m wide", "chose": "AB1 600 x 990 (the sample) and AB2 508 x 762; the placeholder is not used"},
        {"id": "W2", "what": "the foot", "book": "none (a plain board in the plan)", "photo": "S1: the foot is cut with a flared arch, 58 mm high, the base 364 mm wide", "chose": "the arch as photographed (two feet, the arch's flat top 276 mm wide)"},
        {"id": "W3", "what": "what the board carries", "book": "the scene file: the carrier gets a fly-posted gig bill (BOM line G6)", "photo": "S1 and S8: a shop's own board carries its own trade in hand-painted capitals, and a fishmonger lists fish and prices per pound; gig bills are for blank walls", "chose": "a painted fish list with the market's hours on both faces; G6 stays for the walls and the glazed case"},
        {"id": "W4", "what": "the chain", "book": "none", "photo": "S1: one loose chain hangs in a deep loop from a screw eye in each leaf's right edge, seen as one vertical line from the front", "chose": "one catenary chain between two eyes at 592 mm, hanging 242 mm below them"},
        {"id": "W5", "what": "the board's place", "book": "the scene's line at x 15.2, 1.1 m from the kerb face", "photo": "no photograph can say (the scene gives 0.54 and 0.64 m of walking room on either side; the 29 September finding says 0.68 m)", "chose": "x 14.45 against the stallriser, 1.16 m clear on the kerb side"},
    ]
    T["variants_note"] = [
        "AB1 (the sample): the fish market's painted board, one outside the fish market, out in its hours (7.30 to 14.00, Wednesday 13.00).",
        "AB2: the smaller framed notice board of S2's type (508 x 762, thin frame, white panel, a notice card); for the newsagent or the tea room if the town wants one; not placed today. The newsagent's wire-fronted headline board of the asset plan is a different object (its paper's name is owed by canon) and is not written here.",
        "conditions (materials): C0 sound; C1 worn (the sample's wear); C2 a leaf with a corner chipped to bare ply and the chain missing (a seed, not a mesh).",
        "lettering: T1 the fish list as written; T2 the same list with one price overpainted (a decal mask over T1, never other words).",
    ]
    T["owed"] = []
    T["not_settled"] = [
        "absolute sizes: S1 has no scale object, the leaf's width (600 mm) is assumed and sets 0.612 px per mm; every size from S1 is Judgement or Photo within the stated error; AB2's size rests on S2's tyre as a scale, good to about 15 percent",
        "the lean (12 degrees): neither photograph is a side view; a real board stands between 10 and 15 degrees",
        "the 1975 to 1995 date of S1's type: the only dated photograph (S2, 1978) shows a framed board, not a painted ply board with a foot arch; a home-made painted board is certainly older than 1990, but no 1990 photograph of one was found",
        "the hinges and the back battens: both are hidden from the front and no photograph shows them (Judgement)",
        "the other fish's 1990 prices (only the cod's is sourced); and the wording a real fishmonger would have painted",
        "whether Quay Street's fishmonger put the board out every day (the hours say when it could be out; the town has no rule)",
    ]
    T["content_rule_note"] = "no shop name, advertisement, person, drink or betting wording on any face (a statement of the content rule)."
    T["builder_notes"] = [
        "leaf: a 12 mm ply panel 600 wide from the arch's top to the ridge plus two feet cut with the flared arch, all one mesh of one material; the arch's flared sides are the polygon in the foot parts; the painted face is the decal (text.lines) laid on the outer face, 3 px per mm",
        "pose: both leaves hang from the ridge line (the pivot in each part's xf) and lean 12 degrees, the front leaf's face looking -y; the lowest edge of each leaf is its inner foot edge on the paving; build in the leaf's own frame and use the xf as given",
        "the chain: 16 straight 5 mm segments along the catenary in the wire part (a chain of links is a texture on a tube); it hangs free of both leaves and of the ground (its lowest point is 350 mm up)",
        "hinges: two butt hinges on the inner faces, knuckles on the ridge line; the leaves' top inner edges meet there",
        "orientation: the local -y faces up the pavement for the front leaf; the street's yaw 90 turns the board so the two faces look along the pavement",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f %s" % (n["value"], n.get("unit", "mm")), "tol": "+-%.0f" % n["tol"]})
    C += [
        {"name": "C1: no part floats", "measure": "the contact graph of the meshes (touching within 2 mm)", "expect": "all parts reach the ground through the feet", "tol": "0 floating"},
        {"name": "C2: both leaves' outer faces and feet are closed", "measure": "rays at each leaf's face at 0, 30 and 45 degrees; the arch is the only opening", "expect": "0 get through", "tol": "exact"},
        {"name": "C3: the chain is slack, hangs free and ends on both eyes", "measure": "the chain's polyline: ends on the eye tips, length over span at least 1.15, lowest point over 150 mm above the paving", "expect": "all three", "tol": "exact"},
        {"name": "C4: the text fits the leaf and says what the market says", "measure": "line widths at 0.62 of the letter height against the leaf's width less 80 mm; hours against hook-cast.json; cod price against the research note", "expect": "fits and agrees", "tol": "exact"},
        {"name": "C5: the board stands where the placement says and leaves 1.0 m", "measure": "the footprint against the kerb, stallriser, pilaster, awning, doorway and the cast's spot", "expect": "x 14.45, z 4.600, 1.16 m clear", "tol": "+-50 mm"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The A-board is the fish market's painted plywood pavement board: two leaves 600 x 990 x 12 hinged at the top and standing 12 degrees off the vertical (972 high, 435 deep), each with two feet cut with a flared arch 58 high, back battens, a screw eye in the right edge and one loose steel chain hanging 242 below the eyes; "
           "a fish list painted on both faces (cod at 2.60 a pound is the only sourced price) with the market's own hours; it stands on the east pavement outside the fish market at x 14.45 against the stallriser, 1.16 m clear on the kerb side, and is out only from 7.30 to 14.00 (Wednesday 13.00); "
           "a second, smaller framed notice board (508 x 762) after a 1978 photograph is written for a second shop; it replaces the scene's 0.68 x 0.90 x 0.36 placeholder and moves it off a line that left under 0.68 m of walking room on both sides; "
           "no photograph of 1975 to 1995 shows a painted ply board, so its construction rests on a 2013 photograph and its proportions are checked on a 1978 one.")


def story(T):
    N = {n["id"]: n for n in T["numbers"]}
    S = {
        "no": "9", "title": "Quay Street's A-board outside the fish market: the exact target", "summary": SUMMARY,
        "previews_list": "p1 (S1, the board's face blurred), its target-on-photo overlay, and p2 (S2, the 1978 notice board)",
        "rulings": {"ruling_2oct": "not a car, skip or pallet and not the phone box; the A-board is a shop's pavement furniture, so none of the 2 October lines is touched",
                    "sources_order": "no free model fits: Poly Haven has one chalkboard (1.5 m, a cafe's, held for the tea room) and a hazard sign (S6), so the board is our own, scripted from S1 and S2",
                    "content": "no shop name, drink, bet, person or advertisement on any face; the list is fish and its prices per pound; the data scan finds none",
                    "noai": "S1 to S4 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source; nothing is placed or traced",
                    "look": "off-white ply, black capitals, grey splash and rust weeping: grime is the strategy; the board is a worn thing in a damp street", "night": "the board is indoors at night (the market shuts at 14.00)"},
        "rulings_extra": [["RULINGS 3 Oct (trades)", "bay 1 fishmonger, bay 3 empty unit, bay 4 launderette, bay 5 grocer; west_north newsagent and tobacconist, ironmonger, tea room; east_chandler a chandler", "the board is the fishmonger's and stands in bay 1; AB2 is a spare for the newsagent or the tea room"],
                          ["RULINGS 3 Oct (poll-tax posters)", "an invented local campaign, never real parties or people", "no poster on any face; the notice card of AB2 is left to the street's decals"]],
        "searched": "What was searched: Geograph's feed for sandwich board, pavement board, a-board, blackboard, menu and a score of street words for each year 1975 to 1996, then unfiltered. Two period photographs were found and read in full: S2 (1978, the one used) and S4 (1984, no board). Every other hit with a board in it was 2005 or later. Wikimedia Commons and archive.org were not asked (the container's access is limited and Commons rate-limits). Sketchfab was not reached; Poly Haven's list was read in full (S6).",
        "reuse": [
            ["vignette-scene.json held_props pavement_sign (0.68 x 0.90 x 0.36, x 15.2, 1.1 m from the kerb face, yaw 90)", "a placeholder board outside the fish market", "REPLACED as a mesh (the leaf is 600 wide and 990 long); MENDED as a slot: the side, the faces along the pavement and 'outside the fish market' are kept, the line is moved to x 14.45 against the stallriser", "its size disagrees with S1 and S2 (W1) and its place leaves under 0.68 m on both sides (W5)"],
            ["vignette-scene.json decals, BOM line G6 (fly-posted gig bills and notices)", "the board's text was to be a gig bill", "NOT USED for this board; kept for the walls and the glazed case", "a shop's board carries the shop's own trade (W3)"],
            ["production/research/asset-plan 3-FURNITURE-PROPS-FOOD.md: Chalk A-board = Poly Haven standing_chalkboard_01 (held), the cafe's menu board", "a CC0 chalkboard 920 x 759 x 1509", "KEPT for the tea room (not this target)", "it is 1.5 m tall, an easel, and no 1975 to 1995 photograph supports a chalkboard of its kind (S3, S6)"],
            ["production/assets/street/clutter/ (bollard, dustbin, grit bin, kx100, litter bin, pillar box, telegraph pole)", "scripted street clutter", "none to reuse", "no A-board is among them"],
            ["CATALOGUE.md, production/research (street-clutter-1990, asset-plan), every git branch (git log --all)", "the newsagent's wire-fronted A-board is a reserve line; nothing was built", "none to reuse", "only research lines; no mesh or script for an A-board exists on any branch"],
            ["Poly Haven models, WetFloorSign_01", "a yellow plastic hazard sign 300 x 359 x 630", "NOT USED", "a different object (S6)"],
        ],
        "axes": "Axes: x across the leaf (right is +x seen from the front leaf's face), y from the front leaf's painted face (-y) to the back leaf's (+y), z up from the paving, the pivot at the middle of the feet's line. Each leaf is built in its own frame and hung from the ridge line by its xf (a roll of -12 and +12 degrees about the pivot (0, 0, 990) and a lift that sets its inner foot edge on the paving). Parts are boxes, prisms (the feet), cylinders and one wire (the chain); the self-check measures every number back off the parts, in the part's own frame where the part is rotated.",
        "assembly": [
            "**The leaf**: a 12 mm ply panel 600 wide from 58 mm above the foot line to the ridge, and below it two feet, each 118 wide at the ground, whose inner edge flares from 182 mm out from the middle at the ground to 138 mm at the arch's flat top (58 high): the foot arch is 364 wide at the base and 276 at the top. Arrises eased 2 mm.",
            "**The back of each leaf**: two softwood battens 34 x 18 at 245 mm either side of the middle from 120 to 840 mm up, a cross batten 34 x 18 at 380 to 414 between them; two hinge leaves 50 x 52 x 3 near the top on the inner face. The inside is bare wood.",
            "**The ridge**: the two leaves meet along the line (0, 0, 968) and are held by two 8 mm knuckles, 54 long, 205 mm either side of the middle.",
            "**The chain**: a screw eye (r 5, 16 long, 12 mm proud) in each leaf's right edge 605 up the leaf (592 mm above the paving) and 5 mm links hanging free between them in a catenary 242 mm deep.",
            "**AB2**: a frame of 28 x 18 softwood strips, 508 x 762, a 4 mm white panel set 6 mm back, the same hinges, eyes and a chain (170 deep).",
            "**Pose and size**: each leaf stands 12 degrees off the vertical, 435 deep foot to foot, 972 high to the knuckles; AB2 is 352 deep and 749 high.",
        ],
        "lettering": [
            "No shop name and no logo. Hand-painted capitals in black on both outer faces of AB1: heading FRESH FISH 70 mm; five lines of 36 mm, the fish at the left margin and the price at the right (cod fillet 2.60 LB, haddock 2.35 LB, plaice 2.10 LB, kippers 1.45 LB, dressed crab 95P EACH); then the market's hours: %s and %s (30 mm gap below the list)." % (HOURS_LINES[0], HOURS_LINES[1]),
            "Prices: only the cod's is sourced (ONS 1990, 574p/kg, about 2.60 a pound, S8); the others are invented within a few percent and marked so in text.lines. The hours are the fish market's own from the town's cast file (S9).",
            "Letters are 0.62 of their height wide (a narrow signwriter's capital) with a 40 mm margin and at least a 60 mm gap between a fish's name and its price: every line is checked to fit the 600 mm leaf above the arch.",
        ],
        "own_rows": "the lean from the parts' transform, the two leaves as mirrors, the foot arch against P1's arch ratio, the chain's ends, slack and clearance, the text's fit and its hours and cod price against the town's files and the research note, AB2's ratio against P2's measured edges, the slot against the kerb, stallriser, pilaster, awning, doorway and the cast's spot, and the scene's old line against the 0.68 m walking width",
    }
    return S


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
