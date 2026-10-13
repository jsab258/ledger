"""bus-stop: writes target.json and TARGET.md (cloud week 42, unit 13, family 2: the bus stop with its timetable)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY

FAMILY = "bus-stop"
PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))["P1"]
F = PM["features"]
S_MM = 6.56   # mm per pixel on P1 (Judgement: the flag plate is taken as 300 mm wide)
Z_TOP = 3000.0
R_POLE = 44.5                    # the pole is 89 across (3 1/2 inch tube): P1's white pole is 13 to 14 px wide, 13.5 x 6.56 = 89 (the review of 13 October)
D_FRONT = R_POLE - 38.0          # the whole front assembly (flag, case) moves this far toward the bus, so it still meets the pole's front face
WHITE_T = 2310.0                 # where the white length begins (P1 row 174.8, the review's 2310)
RING_B = 890.0                   # the black ring under the case ends here (P1 row 392.3)


def z_of(row):
    return Z_TOP - (row - F["flag_top"]["px"]) * S_MM


FLAG_B = round(z_of(F["flag_bottom"]["px"]), 0)      # 2695
CASE_T = round(z_of(F["case_top"]["px"]), 0)         # ~1883
CASE_B = round(z_of(F["case_bottom"]["px"]), 0)      # ~1008
BAND_B = round(z_of(F["band2_bottom"]["px"]), 0)     # ~554

# the timetable: fictional operator, routes and stops from the town's atlas (production/art/atlas-01/data/atlas.json)
OPERATOR = "WEIGHHOUSE MOTOR SERVICES"
STOP_NAME = "QUAY STREET (TOP)"
SERVICES = [
    {"no": "4", "via": "Weighhouse Lane, Market Hall, Civic Rise", "stops": [["Quay Street (top)", 0], ["Weighhouse Lane", 6], ["Market Hall", 11], ["Civic Rise", 19]],
     "mf": {"first": 710, "last": 1750, "every": 20}, "sat": {"first": 750, "last": 1750, "every": 30}, "sun": None},
    {"no": "9", "via": "Tannery Row, Retort Works", "stops": [["Quay Street (top)", 0], ["Tannery Row", 5], ["Retort Works", 14]],
     "mf": {"first": 710, "last": 1710, "every": 30}, "sat": {"first": 750, "last": 1350, "every": 60}, "sun": None},
    {"no": "12", "via": "Sea Road, Winter Rooms, Short Pier", "stops": [["Quay Street (top)", 0], ["Sea Road", 7], ["Winter Rooms", 15], ["Short Pier", 18]],
     "mf": {"first": 900, "last": 1700, "every": 60}, "sat": {"first": 900, "last": 1800, "every": 60}, "sun": {"first": 1100, "last": 1700, "every": 120}},
]


def hhmm(x):
    return "%02d%02d" % (x // 100, x % 100)


def times(spec):
    """departures from a first time, an interval and a last time (24 hour clock as hhmm numbers)."""
    if not spec:
        return []
    out = []
    t = (spec["first"] // 100) * 60 + spec["first"] % 100
    end = (spec["last"] // 100) * 60 + spec["last"] % 100
    while t <= end:
        out.append((t // 60) * 100 + t % 60)
        t += spec["every"]
    return out


def pole_parts(case=True):
    P = []
    P.append(CY("pole_foot", (0, 0, 0), (0, 0, BAND_B), R_POLE, "paint_black", note="89 mm steel tube (P1: the white pole is 13 to 14 px wide, 13.5 x 6.56 = 89), black lower part to 554"))
    P.append(CY("pole_white", (0, 0, BAND_B), (0, 0, WHITE_T), R_POLE, "paint_white", note="white-painted length 554 to 2310 (P1: the white begins at row 174.8, about 2310, not 2118); the case hides part of it"))
    P.append(CY("pole_ring", (0, 0, RING_B), (0, 0, CASE_B), R_POLE + 1.0, "paint_black", note="the black ring directly under the case, 890 to 1008 (P1 rows 376 to 392): a painted band, modelled as a 1 mm sleeve over the white length"))
    P.append(CY("pole_upper", (0, 0, WHITE_T), (0, 0, Z_TOP), R_POLE, "paint_black", note="black upper length 2310 to 3000 carrying the flag"))
    P.append(CY("pole_cap", (0, 0, Z_TOP), (0, 0, Z_TOP + 8.0), R_POLE + 2.0, "paint_black", note="plug cap, 8 mm, slightly proud of the tube"))
    P.append(CY("pole_collar", (0, 0, 0), (0, 0, 22.0), 95.0, "concrete", note="a small concrete collar round the foot, 22 mm proud of the paving"))
    # the flag: an enamel plate 300 x 285 on two clamps, a black border, rolled edge
    P.append(B("flag_plate", -150.0, 150.0, -48.0, -45.0, FLAG_B + 10.0, Z_TOP, "enamel_white", edge="corners r 20, edge rolled back 4 mm", note="old-style enamel plate, 3 mm steel"))
    P.append(B("flag_border_top", -138.0, 138.0, -50.0, -48.0, Z_TOP - 24.0, Z_TOP - 12.0, "enamel_black", film=False, note="black border 12 wide, 2 mm raised"))
    P.append(B("flag_border_bottom", -138.0, 138.0, -50.0, -48.0, FLAG_B + 22.0, FLAG_B + 34.0, "enamel_black"))
    P.append(B("flag_border_left", -138.0, -126.0, -50.0, -48.0, FLAG_B + 34.0, Z_TOP - 24.0, "enamel_black"))
    P.append(B("flag_border_right", 126.0, 138.0, -50.0, -48.0, FLAG_B + 34.0, Z_TOP - 24.0, "enamel_black"))
    P.append(B("flag_clamp_top", -34.0, 34.0, -48.0, -36.0, Z_TOP - 70.0, Z_TOP - 50.0, "galvanised", note="flat clamp bracket, two bolts"))
    P.append(B("flag_clamp_bottom", -34.0, 34.0, -48.0, -36.0, FLAG_B + 40.0, FLAG_B + 60.0, "galvanised"))
    if case:
        t0, t1 = CASE_B, CASE_T
        P.append(B("case_bar_top", -130.0, 130.0, -98.0, -38.0, t1 - 20.0, t1, "case_green", edge="corners r 4", note="case frame 20 wide, 60 deep, folded sheet"))
        P.append(B("case_bar_bottom", -130.0, 130.0, -98.0, -38.0, t0, t0 + 20.0, "case_green"))
        P.append(B("case_bar_left", -130.0, -110.0, -98.0, -38.0, t0 + 20.0, t1 - 20.0, "case_green"))
        P.append(B("case_bar_right", 110.0, 130.0, -98.0, -38.0, t0 + 20.0, t1 - 20.0, "case_green"))
        P.append(B("case_back", -110.0, 110.0, -44.0, -38.0, t0 + 20.0, t1 - 20.0, "case_green", note="back sheet, 6 mm with its lining"))
        P.append(B("case_glass", -112.0, 112.0, -98.0, -96.0, t0 + 18.0, t1 - 18.0, "glass", transparent=True, note="2 mm clear sheet in the front rebate (acrylic)"))
        P.append(B("case_card", -100.0, 100.0, -96.0, -95.5, t0 + 24.0, t0 + 24.0 + 470.0, "paper", film=True, note="the printed timetable card, 200 x 470, behind the sheet, its top edge at 1502 (P1 row 299, just under the middle bar)"))
        P.append(B("case_lock", 112.0, 124.0, -104.0, -98.0, t0 + 400.0, t0 + 412.0, "galvanised", note="a round lock head on the right bar, 12 mm"))
        P.append(CY("case_strap_top", (0, 0, t1 - 24.0), (0, 0, t1 - 12.0), R_POLE + 3.0, "galvanised", note="stainless clamp strap round the pole, 12 wide"))
        P.append(CY("case_strap_bottom", (0, 0, t0 + 12.0), (0, 0, t0 + 24.0), R_POLE + 3.0, "galvanised"))
        # the case's middle bar (P1 row 284.5, about 1597, 2 to 3 px = 15 mm high, a small dark fixing at each end): 220 x 15 x 4 in the rebate behind the clear sheet
        P.append(B("case_mid_bar", -110.0, 110.0, -94.0, -90.0, 1590.0, 1605.0, "case_green", note="the case's middle bar, 220 x 15 x 4, at 1590 to 1605, in the rebate behind the clear sheet (P1: a thin dark bar across the window at row 284.5)"))
        for sd, x in (("l", -105.0), ("r", 105.0)):
            P.append(CY("case_mid_head_%s" % sd, (x, -94.0, 1597.5), (x, -96.0, 1597.5), 4.0, "paint_black", note="round head 8 across, 2 proud, a fixing at the bar's end"))
    # the flag's back face (+y... the pole side): Judgement, double-sided, the same border as the front (a stop flag is read from both directions)
    P.append(B("flag_back_border_top", -138.0, 138.0, -45.0, -43.0, Z_TOP - 24.0, Z_TOP - 12.0, "enamel_black", note="back face (toward the pole): the same black border, 2 mm raised; Judgement (a flag is read from both directions)"))
    P.append(B("flag_back_border_bottom", -138.0, 138.0, -45.0, -43.0, FLAG_B + 22.0, FLAG_B + 34.0, "enamel_black"))
    P.append(B("flag_back_border_left", -138.0, -126.0, -45.0, -43.0, FLAG_B + 34.0, Z_TOP - 24.0, "enamel_black"))
    P.append(B("flag_back_border_right", 126.0, 138.0, -45.0, -43.0, FLAG_B + 34.0, Z_TOP - 24.0, "enamel_black"))
    # the front assembly stands D_FRONT further toward the bus, so that it still meets the (thicker) pole
    for p in P:
        if p["id"].startswith(("flag_", "case_")) and not p["id"].startswith("case_strap") and p["type"] == "box":
            p["c"] = [p["c"][0], round(p["c"][1] - D_FRONT, 3), p["c"][2]]
        elif p["id"].startswith("case_mid_head"):
            p["p0"] = [p["p0"][0], p["p0"][1] - D_FRONT, p["p0"][2]]
            p["p1"] = [p["p1"][0], p["p1"][1] - D_FRONT, p["p1"][2]]
    return P


def build():
    P1 = pole_parts(True)
    P2 = pole_parts(False)
    embeds = [["pole_collar", "pole_foot", 46.0], ["case_strap_top", "pole_white", 46.0], ["case_strap_bottom", "pole_white", 46.0], ["case_strap_top", "pole_upper", 46.0], ["pole_cap", "pole_upper", 5.0],
              ["pole_ring", "pole_white", 46.0], ["pole_ring", "case_strap_bottom", 46.0], ["pole_ring", "case_bar_bottom", 6.0]]
    _ex1 = ["pole_collar", "case_lock", "case_mid_head_l", "case_mid_head_r"]
    _lo1, _hi1 = L.PartSet(P1).bbox(only=[p["id"] for p in P1 if p["id"] not in _ex1])
    _lo2, _hi2 = L.PartSet(P2).bbox(only=[p["id"] for p in P2 if p["id"] != "pole_collar"])
    T = {
        "family": FAMILY,
        "title": "Quay Street's bus stop with its timetable",
        "units": "millimetres; angles in degrees; z up; the flag and the case face -y (towards the oncoming bus); the pivot is the pole's centre at the paving",
        "status": "fixes applied, not re-reviewed",
        "sample": "BS1",
        "materials": {
            "paint_black": {"name": "pole black gloss, chalked", "srgb": [28, 28, 30], "rough": 0.5, "rough_words": "semi-gloss", "metal": False, "note": "paint over steel, chipped to grey primer at the foot"},
            "paint_white": {"name": "pole white, dirty", "srgb": [214, 212, 200], "rough": 0.55, "rough_words": "semi-matt", "metal": False, "note": "street-grey, splashed to knee height"},
            "enamel_white": {"name": "enamel plate, cream-yellow, dirty", "srgb": [226, 214, 170], "rough": 0.3, "rough_words": "glossy, crazed", "metal": False, "note": "vitreous enamel on steel, yellowed with age (P1: cream with a yellow cast), chipped at the bolt holes and edges"},
            "enamel_black": {"name": "enamel dark brown-black", "srgb": [38, 28, 24], "rough": 0.3, "rough_words": "glossy", "metal": False, "note": "border and lettering"},
            "galvanised": {"name": "galvanised steel", "srgb": [140, 142, 140], "rough": 0.5, "rough_words": "satin", "metal": True, "note": "clamps, straps, lock"},
            "case_green": {"name": "case dark green", "srgb": [44, 66, 52], "rough": 0.5, "rough_words": "semi-matt", "metal": False, "note": "the 1980s council green, faded to grey-green"},
            "glass": {"name": "clear acrylic sheet, scratched", "srgb": [214, 220, 222], "rough": 0.08, "rough_words": "smooth", "metal": False, "note": "crazed at the corners, a dirt line along the lower edge"},
            "paper": {"name": "timetable card, white paper", "srgb": [236, 234, 224], "rough": 0.8, "rough_words": "matt", "metal": False, "note": "black print, a yellowed edge; no operator logo"},
            "concrete": {"name": "concrete collar", "srgb": [128, 126, 120], "rough": 0.9, "rough_words": "rough", "metal": False, "note": "cracked at the pole"},
        },
        "variants": {
            "BS1": {"name": "BS1: pole, old-style flag and timetable case (the sample)", "parts": P1, "overall": {"w": 300.0, "d": round(float(_hi1[1] - _lo1[1]), 1), "h": 3008.0}, "overall_tol": 2.0, "overall_exclude": ["pole_collar", "case_lock", "case_mid_head_l", "case_mid_head_r"],
                    "joins": [["pole_foot", "pole_white"], ["pole_white", "pole_upper"], ["pole_upper", "pole_cap"], ["flag_clamp_top", "pole_upper"], ["flag_clamp_top", "flag_plate"],
                              ["flag_clamp_bottom", "pole_upper"], ["flag_clamp_bottom", "flag_plate"], ["flag_border_top", "flag_plate"], ["case_bar_top", "pole_white"],
                              ["case_bar_bottom", "pole_white"], ["case_back", "case_bar_left"], ["case_glass", "case_bar_left"], ["case_card", "case_glass"], ["case_lock", "case_bar_right"],
                              ["case_strap_top", "case_bar_top"], ["case_strap_bottom", "case_bar_bottom"], ["pole_collar", "pole_foot"],
                              ["case_mid_bar", "case_bar_left"], ["case_mid_head_l", "case_mid_bar"], ["case_mid_head_r", "case_mid_bar"], ["flag_back_border_top", "flag_plate"], ["flag_back_border_left", "flag_plate"]],
                    "embeds": embeds + [["case_back", "case_bar_left", 6.0], ["case_back", "case_bar_right", 6.0], ["case_glass", "case_bar_left", 4.0], ["case_glass", "case_bar_right", 4.0],
                                        ["case_glass", "case_bar_top", 4.0], ["case_glass", "case_bar_bottom", 4.0], ["case_back", "case_bar_top", 6.0], ["case_back", "case_bar_bottom", 6.0]],
                    "faces": [
                        {"id": "flag plate", "o": [-150.0, -50.0 - D_FRONT, FLAG_B + 12.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": 300.0, "nv": Z_TOP - FLAG_B - 14.0, "depth": 8.0, "blockers": ["flag_plate"]},
                    ]},
            "BS2": {"name": "BS2: pole and flag without a case (a second stop elsewhere; not placed today)", "parts": P2, "overall": {"w": 300.0, "d": round(float(_hi2[1] - _lo2[1]), 1), "h": 3008.0}, "overall_tol": 2.0, "overall_exclude": ["pole_collar"],
                    "joins": [["pole_foot", "pole_white"], ["pole_upper", "pole_cap"], ["flag_clamp_top", "pole_upper"]], "embeds": embeds[:1] + embeds[3:], "faces": []},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "z1500", "axis": "z", "at": 1500.0}, {"id": "z2850", "axis": "z", "at": 2850.0}]},
        "numbers": [
            {"id": "N1", "what": "pole length above the paving to the cap's top", "value": 3008.0, "kind": "Judgement", "source": "a 3.0 m stop pole (the repository's research note and the 29 September script agree; P1's span flag top to foot gives 3.0 m only if the plate is 300 wide); error 150 mm", "tol": 150.0, "measure": {"kind": "bbox", "axis": "z", "parts": ["pole_foot", "pole_white", "pole_upper", "pole_cap"]}},
            {"id": "N2", "what": "pole diameter", "value": 2 * R_POLE, "kind": "Photo", "source": "P1: the white pole is 13 to 14 px wide on the 640 px copy (edges x 543.5 and 556.5 at rows 200 to 225; 543.5 and 557.5 at rows 395 to 410; my own edge finder gives 544.1 and 557.5), 13.5 px x 6.56 mm per px = 89 mm: a 3 1/2 inch (89 mm) tube; against the flag's 45.7 px that is 0.30 (+-0.03) while the first version built 76 / 300 = 0.25 (it had read the pole as 7 to 8 px = 50 mm and kept the 76 mm standard). The scale rests on the assumed plate width (N3)", "tol": 10.0, "measure": {"kind": "extent", "axis": "x", "part": "pole_foot"}},
            {"id": "N3", "what": "flag plate width", "value": 300.0, "kind": "Judgement", "source": "assumed 300 mm: it sets P1's scale (6.56 mm per px); P1 flag_left 526.0 to flag_right 571.7 = 45.7 px. The photograph fixes only the RATIO of the pole to the plate: with a 76 mm pole the plate would be about 255 mm, outside this number's old +-30, so the source error is +-50 (a stop plate is 250 to 350 wide); N2, N4 to N7 and N10 are scaled on it", "tol": 30.0, "measure": {"kind": "extent", "axis": "x", "part": "flag_plate"}},
            {"id": "N4", "what": "flag plate height", "value": 285.0, "kind": "Photo", "source": "P1 flag_top 70.6 to flag_bottom 117.1 (46.5 px, includes the yellow lichen and clamp below the plate) at 6.56 mm per px = 305; the plate itself 285 (+-25)", "tol": 25.0, "measure": {"kind": "extent", "axis": "z", "part": "flag_plate"}},
            {"id": "N5", "what": "case height", "value": 875.0, "kind": "Photo", "source": "P1 case_top 240.8 to case_bottom 374.2 (133.4 px) at 6.56 mm per px; error 60", "tol": 60.0, "measure": {"kind": "extent", "axis": "z", "part": "case_bar_left", "plus": 40}},
            {"id": "N6", "what": "case bottom above the paving", "value": 1008.0, "kind": "Photo", "source": "P1 case_bottom 374.2 below flag_top 70.6: 303.6 px = 1992 mm below the flag's top at 3000 (+-130)", "tol": 130.0, "measure": {"kind": "edge", "axis": "z", "part": "case_bar_bottom", "side": "lo"}},
            {"id": "N7", "what": "case top above the paving", "value": 1883.0, "kind": "Photo", "source": "P1 case_top 240.8: 170.2 px below the flag's top = 1117 mm; error 130", "tol": 130.0, "measure": {"kind": "edge", "axis": "z", "part": "case_bar_top", "side": "hi"}},
            {"id": "N8", "what": "case width", "value": 260.0, "kind": "Judgement", "source": "P1 case x 535 to 577 = 42 px = 275 mm by eye (low contrast, not measured by the algorithm); 260 kept for an A3-card case (+-35)", "tol": 35.0, "measure": {"kind": "extent", "axis": "x", "part": "case_bar_top"}},
            {"id": "N9", "what": "case depth (from the pole's front face)", "value": 60.0, "kind": "Judgement", "source": "typical stop case 60 mm; not measurable on P1 (+-20)", "tol": 20.0, "measure": {"kind": "extent", "axis": "y", "part": "case_bar_top"}},
            {"id": "N10", "what": "flag bottom above the paving", "value": 2705.0, "kind": "Photo", "source": "P1 flag_bottom 117.1 below the top: 46.5 px = 305 mm; the plate's own bottom edge at 2715 (+-30)", "tol": 30.0, "measure": {"kind": "edge", "axis": "z", "part": "flag_plate", "side": "lo"}},
        ],
        "photos": [],
        "sources": [], "previews": [], "checks": [], "owed": [],
    }
    T["numbers"][4]["measure"] = {"kind": "span", "axis": "z", "a": "case_bar_bottom", "b": "case_bar_top"}
    T["numbers"] += [
        {"id": "N11", "what": "where the white length begins (the black upper length's lower end)", "value": WHITE_T, "kind": "Photo, scaled on the assumed width", "source": "P1 white_top row 174.8 (box [540, 165, 560, 185]): 3000 - (174.8 - 70.6) x 6.56 = 2317; the review of 13 October writes 2310 (the first version had 2118 from the case's blurred upper edge); error 40", "tol": 40.0,
         "measure": {"kind": "edge", "axis": "z", "part": "pole_upper", "side": "lo"}},
        {"id": "N12", "what": "the black ring under the case: its lower end above the paving", "value": RING_B, "kind": "Photo, scaled on the assumed width", "source": "P1 ring_bottom row 392.3 (box [540, 384, 560, 400]): 3000 - (392.3 - 70.6) x 6.56 = 890; the ring runs from the case's foot (1008, row 374 to 376) down to it: a black band the first version did not have; error 40", "tol": 40.0,
         "measure": {"kind": "edge", "axis": "z", "part": "pole_ring", "side": "lo"}},
        {"id": "N13", "what": "the case's middle bar height", "value": 15.0, "kind": "Photo", "source": "P1: a thin dark bar across the window at row 284.5 (about 1597 mm), 2 to 3 px = about 15 mm high, with a small dark fixing at each end; the card's top edge just under it (row 299, about 1502); error 6", "tol": 6.0,
         "measure": {"kind": "extent", "axis": "z", "part": "case_mid_bar"}},
        {"id": "N14", "what": "the case's middle bar above the paving (its centre)", "value": 1597.5, "kind": "Photo, scaled on the assumed width", "source": "P1 row 284.5: 3000 - (284.5 - 70.6) x 6.56 = 1597; error 60", "tol": 60.0,
         "measure": {"kind": "centre", "axis": "z", "part": "case_mid_bar"}},
    ]
    # source errors: the plate's width is an ASSUMPTION (300, +-50 = 16.7 percent) that sets P1's scale, so each length measured on P1 carries that
    # relative error as what the SOURCE can tell; the builder's tolerance (tol) stays a separate field and never stands for the source's error
    rel_ = 50.0 / 300.0
    scaled_len = {"N2": 2 * R_POLE, "N4": 285.0, "N5": 875.0, "N6": 3000.0 - 1008.0, "N7": 3000.0 - 1883.0, "N10": 3000.0 - 2705.0, "N11": 3000.0 - WHITE_T, "N12": 3000.0 - RING_B, "N14": 3000.0 - 1597.5}
    for n in T["numbers"]:
        if n["id"] == "N3":
            n["source_error"] = 50.0
        elif n["id"] in scaled_len:
            n["scaled_on"] = "N3"
            n["scaled_length"] = scaled_len[n["id"]]
            n["source_error"] = math.ceil(rel_ * scaled_len[n["id"]] / 5.0) * 5.0
            if n["kind"] == "Photo":
                n["kind"] = "Photo, scaled on the assumed width"
        elif n["id"] in ("N1", "N8", "N9"):
            n["source_error"] = n["tol"]
    refs = {"flag_top": ("y", "flag_plate", "hi"), "flag_bottom": ("y", "flag_plate", "lo", {"add": -10.0}), "case_top": ("y", "case_bar_top", "hi"),
            "case_bottom": ("y", "case_bar_bottom", "lo"), "band2_bottom": ("y", "pole_foot", "hi"),
            "flag_left": ("x", "flag_plate", "lo"), "flag_right": ("x", "flag_plate", "hi"),
            "pole_l": ("x", "pole_white", "lo"), "pole_r": ("x", "pole_white", "hi"), "white_top": ("y", "pole_upper", "lo"), "ring_bottom": ("y", "pole_ring", "lo")}
    keep = {k: v for k, v in refs.items()}
    pm = dict(PM)
    pm["features"] = {k: v for k, v in F.items() if k in keep}
    T["photos"].append(SF.photo_entry(pm, "P1", "S1", "BS1", keep, ["flag_plate", "case_bar_bottom"], anchors=("flag_top", "case_bottom"), boundary=("flag_left", "flag_right", "flag_top", "band2_bottom"),
                                      fit_top="flag_top", fit_bottom="case_bottom", centre_from=lambda FF: (FF["flag_left"]["px"] + FF["flag_right"]["px"]) / 2.0, min_tol=5.0, file="P1.jpg",
                                      method="each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band; the scale is fitted on the one span from the flag plate's top edge to the case's lower edge (303.6 px); the plate's width is the unit that sets 6.56 mm per px (Judgement), so the absolute sizes are judged within the stated errors and the photograph checks the proportions; case sides were too faint to measure; the band-2 foot (the white band's lower end) has a spread of 3.6 px; the tolerance is the measured spread times 3 plus 2 px, at least 5 px (33 mm)"))
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/5668101", "read": "2026-10-13", "author": "Jaggery", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2018-01-16", "kind": "photograph",
         "shows": "an old-style bus stop in a Cotswold village: an enamel flag with BUS STOP in two lines on a black pole with white bands, a dark-green timetable case with a clear window (blank upper half, a paper card in the lower half) clamped below the flag; the foot is in shadow",
         "used": True, "not_used_for": "any absolute size (no scale object; the flag's width is assumed), the colours (a winter evening, strong shadow), the ground",
         "period": "2018 photograph of a sign of an older type that was still in use in 1990 (a Gloucestershire village stop; the type is far older than 1990)"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/1981245", "read": "2026-10-13", "author": "Rob Candlish", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2010-07-25", "kind": "photograph",
         "shows": "a stop pole with a tall case holding two printed timetables stacked and a notice; shows how a card fills a case and how text blocks stack",
         "used": True, "not_used_for": "any number; the operator's logo and the notice's wording (real marks, not copied)", "period": "2010; the paper-in-a-case idea is older"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/4340832", "read": "2026-10-13", "author": "Jaggery", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2015-02-05", "kind": "photograph",
         "shows": "a plain black pole in a terraced street with a small flag plate with a bus pictogram and a two-line text; shows how a stop sits against a kerb in a street of houses",
         "used": False, "not_used_for": "everything (looked at; the plate is of a later type)", "period": "2015"},
        {"id": "S4", "url": "production/art/atlas-01/data/atlas.json and production/specs/hook-cast.json (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the town's roads and landmarks (Weighhouse Lane, Tannery Row, Civic Rise, Sea Road, Market Hall, Retort works, Winter Rooms, Short pier) and the cast's bus stop at x 46.0, z -4.3 on the west pavement",
         "used": True, "not_used_for": "the stop's design", "period": "n/a"},
        {"id": "S5", "url": "tools/meshgen/blender/clutter/bus_stop.py, production/research/street-clutter-1990 (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "29 September 2026", "kind": "own",
         "shows": "an earlier scripted stop: a 3.0 m 76 mm pole, a 450 x 375 flag of diagram 970, a grey case at eye height",
         "used": True, "not_used_for": "its flag and case (they disagree with S1)", "period": "n/a"},
        {"id": "S6", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "no bus stop, bus shelter or timetable model; the nearest is a wet-floor sign and two chalkboards", "used": False, "not_used_for": "everything: so the stop is made by script", "period": "n/a"},
        {"id": "S7", "url": "https://api.geograph.org.uk/syndicator.php (terms bus stop, bus shelter, bus stop timetable, bus stop sign, bus stop pole, each with takenyear 1975 to 1996)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)",
         "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "about 100 photographs of 1975 to 1996 with a bus or a stop in them; the nearest to a close view of a stop is a Belfast flag of 1990 (a different country's operator flag, with a real logo) and a 1996 supermarket stop that shows a person and a real brand; none was measurable and none is used",
         "used": False, "not_used_for": "measuring", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-fulbrook-stop-flag-and-case.jpg", "source": "S1", "credit": "Jaggery, Geograph 5668101, CC BY-SA 2.0, 2018-01-16, cropped to the pole; the timetable card's small print blurred",
         "masked": ["the timetable card's print (blurred)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p1-fulbrook-stop-target-on-photo.jpg", "source": "S1", "credit": "overlay of this target's front drawing (red) on the same crop, the scale fitted on the height from the flag's top to the case's lower edge, measured edges in green",
         "masked": ["as p1"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    sv = []
    for sv_ in SERVICES:
        sv.append({"no": sv_["no"], "via": sv_["via"], "stops": sv_["stops"], "mf": sv_["mf"], "sat": sv_["sat"], "sun": sv_["sun"]})
    T["text"] = {
        "operator": OPERATOR, "stop_name": STOP_NAME,
        "card": {"w": 200.0, "h": 470.0, "margin": 10.0, "font": "Liberation Sans (SIL OFL 1.1)", "head_mm": 11.0, "service_no_mm": 16.0, "body_mm": 3.6, "line_pitch_mm": 4.6, "texture_px_per_mm": 4},
        "services": sv,
        "legend": ["Mondays to Fridays", "Saturdays", "Sundays"],
        "no_logo": "no operator logo anywhere; the name is a placeholder the town will mint (RULINGS 3 Oct: names minted within canon, placeholders meanwhile)",
        "operator_layer": {"kind": "a separate texture layer on the card", "blank_in_pictures_for_his_page": True, "note": "the placeholder name sits on its own layer of the card's texture; every picture meant for Jafar's page shows the layer blank"},
        "flag_back": "the flag's back face (toward the pole) is double-sided: the same border and BUS over STOP, Judgement (a stop flag is read from both directions); the borders exist on both faces in the parts",
        "flag_text": ["BUS", "STOP"], "flag_text_mm": 62.0, "flag_font": "a plain upright grotesque (Liberation Sans Narrow or similar, SIL OFL), black on the off-white plate, centred; two lines of 62 mm capitals",
        "road_marking": "none in this target (the road legend belongs to the wear and road targets)",
    }
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the stop has no light; the nearest lamp column is LC4 at x 38 west, 8 m away, so the flag and case stand in the dark between pools; the plate's enamel catches the lantern colour as a glint on its rolled edge"}
    T["placeholders"] = [{"name": "Weighhouse Motor Services", "marked": "fictional placeholder", "kind": "the bus company's name on the timetable card", "where": "text.operator and the card's own texture layer (blank in any picture for his page)", "until": "the town mints the operator (handover H1)"}]
    T["handovers"] = [{"id": "H1", "line": "For the town: mint the bus operator for the timetable card (its name, within canon's naming rules; the card's three services and their stops come from atlas.json already). Now the placeholder 'Weighhouse Motor Services' on the card's own texture layer, never shown on Jafar's page."}]
    T["placement"] = {
        "slot": "west pavement, pole centre at x 46.0 m (the cast's bus stop, hook-cast.json), 0.50 m behind the kerb's back edge (z -3.625), the flag and the case facing -x (south, towards the bus coming up the street); the waiting spot z -4.3 is behind it; no shelter",
        "poses": [{"id": "stop", "variant": "BS1", "x_m": 46.0, "z_m": -3.625, "yaw_deg": -90.0, "zone": "west_footway", "front_faces": "-x"}],
        "x_m": 46.0, "z_m": -3.625, "z_wait_m": -4.3, "kerb_back_z_m": -3.125, "frontage_z_m": -5.125, "footway_mm": 2000.0, "set_back_mm": 500.0, "min_clear_behind_mm": 1000.0,
        "bin_slot": {"file": "litter-bins", "slot": "B3", "max_m": 3.0},
        "reasons": [
            "the cast already puts the stop at x 46.0, z -4.3 on the west pavement (production/specs/hook-cast.json: 'the bus stop at the top of Quay Street'), and the west row's newsagent (west_north, x 36 to 42) lies below it (Rita's is on the east side, across the street); the scene file has no stop, so this is a new slot (the 29 September README said the street had none)",
            "a bus on the west lane travels north (+x) with the kerb on its left; the flag must face the bus coming from the south, so it faces -x; waiting people read the case from the road side of the pole",
            "no shelter: a shelter is 1.2 to 1.5 m deep and would leave 0.5 to 0.8 m of a 2.0 m footway, under the 1.0 m this target requires behind a pole (the tester's walk found 0.65 m too narrow on 29 September); the stop is a pole with a case",
            "the litter bin B3 of the litter-bins target (the hooded drum K2) stands at x 44.0 west, z -3.8, 2.0 m from the pole, inside the 3 m the asset plan asks for",
            "the stop is beyond the west row's end (west_north runs to x 42; the stop is 4.0 m past it), so no shopfront is hidden by the pole or the queue",
        ],
    }
    T["wear"] = [
        "the pole's paint is chipped to grey primer within 300 mm of the paving (kicks, bicycle pedals); the lowest 120 mm has a dark splash line; the white band is street-grey",
        "scraps of old sticker and tape on the pole between 1.2 and 1.6 m, never legible; a few dog marks at the foot (nothing else at the foot)",
        "the flag plate: chips at the bolt holes with rust runs 30 to 80 mm long, a bent corner, a patch of yellow-green lichen and bird lime along its lower edge and clamp (P1 shows yellow lichen under the plate), the plate off square by 2 to 3 degrees (the sample's lean; BS1 is built square and the lean is a seed)",
        "the case: green faded to grey-green on its top bar, a dirt line along the window's lower edge, two fine scratches on the sheet, one cracked corner of the sheet in the worn variant, the card yellowed at the edges with its top corner curled",
        "NOT shown: any advertisement on the case, any person, any drink, any real operator's logo",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "the flag", "book": "the 29 September script and the research note: a 450 x 375 plate of diagram 970 (a bus pictogram over a Bus Stop panel)", "photo": "S1: an old-style enamel plate, about 300 wide, two lines BUS and STOP, a black border, a rolled edge; S3 shows the later pictogram type on a street of houses", "chose": "the S1 plate as the sample; the diagram-970 plate is a later flag and not written (a variant if the street wants a second stop)"},
        {"id": "W2", "what": "the case", "book": "the script: a grey case with a perspex window at eye height", "photo": "S1: a dark-green framed case, tall (about 875 mm), with a blank upper half and the paper card in the lower half, its foot at about 1.0 m", "chose": "the S1 case: green, 260 x 875 x 60, the card low in the window"},
        {"id": "W3", "what": "the pole's paint", "book": "the script: one galvanised grey tube", "photo": "S1: black tube with a white band above the case and below it, black foot", "chose": "black foot to 554, white 554 to 2118, black above"},
        {"id": "W4", "what": "the collar", "book": "none", "photo": "S1's foot is in shadow and S2/S3 show the pole entering the paving with a small collar", "chose": "a 22 mm concrete collar r 95 (Judgement)"},
    ]
    T["variants_note"] = [
        "BS1 (the sample): pole, old-style flag, timetable case. One on the street.",
        "BS2: pole and flag only (no case), the same pole and flag: for a second stop if the town wants one (none today).",
        "conditions (materials): C0 sound; C1 worn (the sample's wear); C2 flag knocked 3 degrees off square with a bent corner and a cracked case sheet (a seed, not a mesh).",
        "timetable cards: T1 as written; T2 the same card yellowed with a curled corner and one service struck through in ink (a mask over T1, never other times).",
    ]
    T["variants"]["BS1"]["service_note"] = "see text.services"
    T["owed"] = []
    T["not_settled"] = [
        "absolute sizes: S1 has no scale object, the plate's width (300 mm) is assumed and sets 6.56 mm per px; every size from S1 is Judgement within the stated error (the flag's height, the case's height and its height above the paving, the white band's lower end)",
        "the case's width and depth (the sides were too faint to measure; 260 wide and 60 deep are typical)",
        "the 1990 flag type on the real street (S1's old enamel plate or the pictogram plate of S3): either is period; S1 is chosen because a photograph exists",
        "the real timetable's look (S2 is 2010 and carries an operator's logo, so only its stacking of text blocks is used)",
        "whether Quay Street's stop had a shelter in the cast's mind (the cast gives only the stop)",
    ]
    T["content_rule_note"] = "no advertisement, no person, no drink or betting wording on the case or card (a statement of the content rule)."
    T["builder_notes"] = [
        "pole: three tubes (black, white, black) of 76 mm and a cap; the paving collar is a short cylinder; weld the three tubes into one mesh with one material id each",
        "flag plate: 3 mm with corners r 20 and the edge rolled back 4 mm; the border and the two lines of capitals are texture on the plate, not meshes; the border strips in the parts table are the raised edge's guide (2 mm)",
        "case: four folded bars (60 deep), a 6 mm back sheet, a 2 mm clear sheet, the card 4 px per mm (800 x 1880 px) with the text from text.services set in the stated font; the card has no logo",
        "orientation: the local -y faces the bus (towards -x in the street's frame, yaw 90 degrees)",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f mm" % n["value"], "tol": "+-%.0f mm" % n["tol"]})
    C += [
        {"name": "C1: no part floats", "measure": "the contact graph of the meshes (touching within 2 mm)", "expect": "all parts reach the ground", "tol": "0 floating"},
        {"name": "C2: the flag plate is closed from the front, square on and leaning", "measure": "rays at the plate face at 0, 30 and 45 degrees", "expect": "0 get through", "tol": "exact"},
        {"name": "C3: the card lies inside the case's window", "measure": "the card's box inside the clear sheet's box", "expect": "inside", "tol": "exact"},
        {"name": "C4: the card has no logo and carries exactly the services of text.services", "measure": "the card texture's text", "expect": "services 4, 9 and 12 as written", "tol": "exact"},
        {"name": "C5: the stop stands where the placement says", "measure": "pole centre against the placement", "expect": "x 46.0, z -3.625", "tol": "+-50 mm"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The bus stop is a 76 mm pole 3.0 m high (black foot, white length, black top, a concrete collar) carrying an old-style enamel flag 300 x 285 with BUS and STOP in two lines and a black border, and below it a dark-green timetable case 260 x 875 x 60 whose window holds one 200 x 470 card: the fictional Weighhouse Motor Services, services 4, 9 and 12 to stops that are on the town's own map; it stands on the west pavement at x 46.0 (the cast's stop) 0.50 m behind the kerb, with no shelter, its flag and case facing the bus; it replaces the 29 September script's flag and case; "
           "no 1975 to 1995 photograph of a stop was measurable, so the proportions are measured on a 2018 photograph of an old-style stop and the absolute sizes are judged (the plate's width sets the scale).")


def story(T):
    N = T["numbers"]
    S = {
        "no": "2", "title": "Quay Street's bus stop with its timetable: the exact target", "summary": SUMMARY,
        "previews_list": "p1 (S1 cropped, the card's print blurred) and its target-on-photo overlay",
        "rulings": {"ruling_2oct": "not a car, skip or pallet; the kiosk is another unit; the stop is the town's own furniture", "sources_order": "no free model (S6: no bus stop in 521 Poly Haven models); so own work by script, from S1's photograph",
                    "content": "nothing the rule forbids on the case or card: the stops are streets and landmarks of the town (a seaside pier, a market hall, a works); the data scan finds none", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source; nothing is placed or traced",
                    "look": "black, off-white and green: no saturated colour except the case's faded green; grime and chips are the strategy", "night": "the stop has no light of its own"},
        "rulings_extra": [["canon (brands)", "every brand fictional; no real operator, council or maker", "the operator is Weighhouse Motor Services, a placeholder named for a minted street; no logo; the routes and stops are the town's own (atlas.json)"]],
        "searched": "What was searched: Geograph's feed for `bus stop`, `bus shelter`, `bus stop timetable`, `bus stop sign`, `bus stop pole` with each year 1975 to 1995 (about 100 candidates; no measurable close view). Wikimedia Commons was not asked. The hobby pages for the bus flag standard were not reached (the standards' text is not in the repository; the 450 x 375 figure rests on the research note alone and is not used).",
        "reuse": [
            ["tools/meshgen/blender/clutter/bus_stop.py (29 Sep) and its model on F:", "a 3.0 m 76 mm pole, a 450 x 375 diagram-970 flag, a grey case", "MENDED: the pole (76 mm, 3.0 m) is kept; the flag and the case are REPLACED", "S1 shows an older plate and a taller green case (W1, W2, W3)"],
            ["production/research/street-clutter-1990 item 5", "the flag and pole as a research item", "KEPT for the pole's size", "its flag size is unverified and not used"],
            ["production/specs/hook-cast.json: bus_stop at x 46.0, z -4.3", "the cast's stop", "KEPT as the slot", "no scene line exists, so this target adds one"],
            ["production/cloud-week/targets/litter-bins (B3, the hooded drum, at x 44.0 west)", "a hooded bin beside the stop", "KEPT, read by the self-check", "the asset plan puts a bin at the stop"],
            ["Poly Haven models, git branches (git log --all for bus stop, timetable)", "nothing relevant", "none to reuse", "S6; only the 29 September commit"],
        ],
        "axes": "Axes: x across the flag (right is +x seen from the front), y from the front (-y, towards the bus) to the back (+y), z up from the paving at the pole's centre. Every part is a box or a cylinder; the self-check measures every number back off the parts.",
        "assembly": [
            "**The pole**: a 76 mm steel tube, black from the paving to 554, white from 554 to 2118, black to the top at 3000, with a plug cap 8 mm high; a concrete collar r 95, 22 high, round the foot.",
            "**The flag**: a 300 x 285 x 3 enamel plate on two flat galvanised clamps (two bolts each), its top at 3000 and its lower edge at 2715; the border 12 wide and 2 mm raised, corners r 20, the edge rolled back 4 mm; BUS over STOP in black capitals 62 mm tall; the plate faces -y.",
            "**The case**: four folded dark-green bars 20 wide and 60 deep make a frame 260 x 875 from 1008 to 1883, a 6 mm back sheet against the pole, a 2 mm clear sheet in the front rebate and, behind it, one printed card 200 x 470 held low in the window (its lower edge 40 above the frame's bottom); a round lock head on the right bar 400 above the foot; two clamp straps round the pole at the case's top and bottom.",
            "**Edges and fixings**: tube ends square; bar corners r 4; the plate's rolled edge; clamp bolts 10 mm hex heads (Judgement); the card is held by the sheet, no fixings.",
            "**The timetable** is data (text.services): three services, each with its stops and minutes from the stop, Mondays to Fridays, Saturdays and Sundays as a first time, an interval and a last time.",
        ],
        "lettering": [
            "Operator: %s (invented; named for the town's Weighhouse Lane); the stop: %s." % (OPERATOR, STOP_NAME),
            "Card: 200 x 470 mm, margin 10; heading 11 mm capitals; service numbers 16 mm; body 3.6 mm in Liberation Sans (SIL OFL 1.1) with a 4.6 mm line pitch; times as four digits on the 24-hour clock.",
        ] + ["Service %s: %s. Quay Street (top) departures: Mondays to Fridays %s then every %d minutes until %s; Saturdays %s then every %d minutes until %s; Sundays %s." % (
            sv["no"], ", ".join("%s +%d" % (n, m) for n, m in sv["stops"]), hhmm(sv["mf"]["first"]), sv["mf"]["every"], hhmm(sv["mf"]["last"]),
            hhmm(sv["sat"]["first"]), sv["sat"]["every"], hhmm(sv["sat"]["last"]),
            ("%s then every %d minutes until %s" % (hhmm(sv["sun"]["first"]), sv["sun"]["every"], hhmm(sv["sun"]["last"]))) if sv["sun"] else "no service") for sv in SERVICES],
        "own_rows": "the timetable's arithmetic and its stops against atlas.json, the card's capacity, the card inside the window, the stop's slot against hook-cast.json and the bin's slot, the clear footway behind the pole",
    }
    S["lettering"] = S["lettering"][:-0] if False else S["lettering"]
    S["own_rows"] = "the timetable's arithmetic and its stops against atlas.json, the card's capacity, the card inside the window, the stop's slot against hook-cast.json and the bin's slot, the clear footway behind the pole"
    return S


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
