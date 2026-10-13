"""Door furniture variants of the front-doors-all target: size, place, material, colour, source. Positions are per kind (the leaf frame: u across
from the leaf's left edge seen from outside, v up from its bottom). No real maker's name or mark anywhere: the lock is a rim night latch.
make_target.py writes these into target.json under furniture."""
import sys

import math

from td_data import MEAS
from td_kinds import F5_V, LAP, VIS, d2_f5_fractions, d4_t3_fractions, d5_fractions, d3_fractions

sys.dont_write_bytecode = True

BRASS = {"material": "brass", "srgb": [181, 150, 85], "metal": 1.0, "roughness": 0.4, "worn_roughness": 0.25}
CHROME = {"material": "nickel or chrome-look", "srgb": [170, 170, 168], "metal": 1.0, "roughness": 0.35}
ALU = {"material": "anodised aluminium, pale", "srgb": [190, 190, 185], "metal": 1.0, "roughness": 0.45}
STEEL_DARK = {"material": "dark steel", "srgb": [40, 40, 42], "metal": 1.0, "roughness": 0.6}
IRON_BLACK = {"material": "cast iron, black", "srgb": [30, 30, 32], "metal": 1.0, "roughness": 0.65}
PLASTIC_WHITE = {"material": "white moulded plastic", "srgb": [226, 224, 214], "metal": 0.0, "roughness": 0.4}
PAINT_WHITE = {"material": "white gloss paint", "srgb": [226, 224, 214], "metal": 0.0, "roughness": 0.35}


def scraper_standard_profile():
    """One end standard of the boot scraper in elevation (x outward from the blade's end, z up, mm), a closed outline: a flat bar 25 wide rising to z 154 and then a scroll of outer
    radius 35 (centre (-10, 169), its top at z 200) curling outward through 270 degrees, the strip 12 wide, ending inside the curl at z 146 (outer) and 158 (inner). Judgement, from D10."""
    cx, cz = -10.0, 169.0
    pts = [(0.0, 0.0), (25.0, 0.0), (25.0, 154.0)]
    steps = list(range(0, 271, 30))
    for a in steps:
        r = 35.0 - 12.0 * a / 270.0
        pts.append((cx + r * math.cos(math.radians(a)), cz + r * math.sin(math.radians(a))))
    for a in reversed(steps):
        r = 35.0 - 12.0 * a / 270.0 - 12.0
        pts.append((cx + r * math.cos(math.radians(a)), cz + r * math.sin(math.radians(a))))
    pts += [(0.0, 154.0)]
    return [[round(x, 1), round(z, 1)] for x, z in pts]


# the blade's underside notch (D10 shows a central cut with a notched underside): one trapezoid cut 140 long at the underside, 116 at its top, 12 deep, in the 25 high blade; Judgement
BS1_NOTCH = {"length_at_underside": 140.0, "length_at_top": 116.0, "depth": 12.0, "centred": True, "src": "Judgement from D10"}


def furniture(A):
    """A = the 3.1 target as built (departures applied)."""
    ir = A["ironmongery"]
    lp = ir["letter_plate"]
    lk = ir["cylinder_lock"]
    fir = A["variants"]["flat_door_over_shop"]["parts"]["ironmongery"]
    kn = fir["knob"]
    kh = fir["old_keyhole"]
    opt = A["variants"]["option_six_panel"]
    H31 = 1960.6   # the visible height of frame set F: 3.1's option fractions are of the visible face
    f5 = d2_f5_fractions()
    f4 = d4_t3_fractions()
    f6 = d5_fractions()
    f3 = d3_fractions()
    VWF, VHF = VIS["F"]
    # F5: the review's v numbers (the box gives 5 to 11 mm more, inside the +-24); u from the fractions of the new box
    slit_plate_v = F5_V["plate"]
    t3_plate_v = round((f4["plate"]["v"][0] + f4["plate"]["v"][1]) / 2.0 * 1927.6, 1)
    # F6 (D5, an indoor door): u and v by D5's fractions of the VISIBLE face of the street frame F (u = 20.4 + fraction x 797.2, v = fraction x 1960.6)
    mid = lambda f, a: (f[a][0] + f[a][1]) / 2.0
    f6_plate_u = round(LAP + mid(f6["plate"], "u") * VWF, 1)
    f6_plate_v = round(mid(f6["plate"], "v") * VHF, 1)
    f6_handle_u = round(LAP + mid(f6["handle"], "u") * VWF, 1)
    f6_handle_v = round(mid(f6["handle"], "v") * VHF, 1)
    f6_lock_u = round(LAP + mid(f6["lock"], "u") * VWF, 1)
    f6_lock_v = round(mid(f6["lock"], "v") * VHF, 1)
    f5_handle_v = F5_V["handle"]
    f5_handle_u = round(LAP + (f5["handle"]["u"][0] + f5["handle"]["u"][1]) / 2.0 * VWF, 1)
    f5_plate_u = round(LAP + (f5["plate"]["u"][0] + f5["plate"]["u"][1]) / 2.0 * VWF, 1)
    t3_handle_v = 910.0       # the review's number (the box [577, 388, 578.5, 396] gives 920.6, inside the +-32)
    d3b = MEAS["D3_leaf"]["box"]
    d3_handle_rows = MEAS["D3_handle"]["box"]
    t2_handle_v = round(((d3b[3] - d3_handle_rows[1]) + (d3b[3] - d3_handle_rows[3])) / 2.0 / (d3b[3] - d3b[1]) * 1927.6, 1)
    F = {}
    F["letter_plate"] = {
        "LP0": {"name": "none", "note": "F7, the service door, has no plate"},
        "LP1": {"name": "brass plate, vertical, on the muntin", "outer": [lp["outer_w_mm"], lp["outer_h_mm"]], "aperture": [lp["aperture_w_mm"], lp["aperture_h_mm"]],
                "backplate_t": lp["backplate_thickness_mm"], "rim_proud": lp["rim_proud_mm"], "rim_edge": "chamfered 45 degrees", "flap": "sprung, hinged at the top, dished 3", **BRASS,
                "place": {"T1": {"u": "leaf centre", "v": lp["centre_above_leaf_bottom_mm"]}, "F1": {"u": "leaf centre", "v": lp["centre_above_leaf_bottom_mm"]},
                          "F3": {"u": "leaf centre", "v": lp["centre_above_leaf_bottom_mm"]}},
                "src": "3.1 as built (P1: 76 x 242, centre 1617)"},
        "LP2": {"name": "brass plate, horizontal, above the lock rail", "outer": [195.0, 70.0], "aperture": [168.0, 40.0], "rim": 12.0, "backplate_t": 3.0, "rim_proud": 6.0, "flap": "sprung, two pivot bosses",
                **BRASS, "place": {"F2": {"u": "leaf centre", "v": round(opt["furniture_heights_fraction_of_visible_height"]["letter_plate"] * H31, 1)}},
                "src": "3.1 option_six_panel (P2: 195 x 70 at 0.788 of the height)"},
        "LP3": {"name": "black iron plate, horizontal (reserve, not placed)", "outer": [230.0, 60.0], "aperture": [190.0, 30.0], "backplate_t": 4.0, "rim_proud": 5.0, **IRON_BLACK, "place": {},
                "src": "Judgement: cast-iron plates were common but none is read in a photograph here; listed so a script may place one; the check rejects it on any house today"},
        "LP4": {"name": "chrome-look oblong, flush", "outer": [250.0, 70.0], "frame_w": 6.0, "proud": 2.0, "flap": "hinged behind, the opening 238 x 58", **CHROME,
                "place": {"F6": {"u": f6_plate_u, "v": f6_plate_v}},
                "src": "Photo D5 (an indoor landing door: the place only, as fractions of its face): 107 x 30 px at 2.34 mm a pixel = 250 x 70 (the size is Judgement), centre at 0.505 of the face's width and 0.470 of its height"},
        "LP5": {"name": "pale low plate in the bottom rail", "outer": [250.0, 50.0], "frame_w": 5.0, "proud": 2.0, **ALU,
                "place": {"T2": {"u": "leaf centre", "v": 100.0}, "F4": {"u": "leaf centre", "v": 100.0}},
                "src": "Photo D1 right door (rows 659 to 662.5 of a 150 px leaf: centre 83 above the foot, 46 high) and D4 black door (a 10 x 3 px plate at the foot, 90): centre 100 chosen to sit mid-rail (+-20)"},
        "LP6": {"name": "white plastic oblong in a moulded door", "outer": [270.0, 50.0], "frame_w": 5.0, "proud": 3.0, **PLASTIC_WHITE,
                "place": {"T3": {"u": "leaf centre", "v": t3_plate_v}}, "src": "Photo D4 right door: 12 x 3.1 px at 21.7 mm a pixel = 260 x 67, centre 0.448 of the visible height (+-25)"},
        "LP7": {"name": "small pale plate under a slit light", "outer": [265.0, 50.0], "frame_w": 5.0, "proud": 2.0, **ALU,
                "place": {"F5": {"u": f5_plate_u, "v": slit_plate_v}}, "src": "Photo D2 middle door: 11 x 2 px at 24.7 mm a pixel = 272 x 49 (+-25), centre v 772 (the review's number; the leaf's own box gives 777)"},
    }
    F["handle"] = {
        "HD0": {"name": "none", "note": "T1, T2's lock side has HD3, F7 HD4"},
        "HD1": {"name": "turned centre knob on a dished rose", "dia": kn["diameter_mm"], "proud": kn["projection_mm"], "rose": kn["rose_diameter_mm"], "profile_rz": kn["profile_rz_mm"],
                "cap": "brass 4 mm", "material": "black-painted wood, brass cap", "srgb": [35, 36, 40],
                "place": {"F1": {"u": "leaf centre", "v": kn["centre_above_leaf_bottom_mm"]}, "F2": {"u": "leaf centre", "v": round(opt["furniture_heights_fraction_of_visible_height"]["knob"] * H31, 1)}},
                "src": "3.1 as built (P2 8x crop)"},
        "HD2a": {"name": "lever handle on a round rose, chrome-look, right stile", "lever": [105.0, 18.0], "lever_proud": 55.0, "rose_dia": 50.0, "rose_proud": 6.0, **CHROME,
                 "place": {"F6": {"u": f6_handle_u, "v": f6_handle_v}},
                 "src": "Photo D5 (an indoor landing door: the place only): lever 45 px = 105 at 2.34 mm a pixel, centre at 0.911 of the face's width and 0.457 of its height, on the right stile"},
        "HD2b": {"name": "lever handle on a round rose, chrome-look, left stile", "lever": [100.0, 18.0], "lever_proud": 55.0, "rose_dia": 50.0, "rose_proud": 6.0, **CHROME,
                 "place": {"F5": {"u": f5_handle_u, "v": f5_handle_v}, "F4": {"u": 95.0, "v": 1228.0}},
                 "src": "Photo D2: a small pale handle at the left stile of the middle door, v 1048 (the review's number, 0.535 of the visible height; the leaf's own box gives 1054; +-24); the left door's at about 1228 (+-30)"},
        "HD2c": {"name": "short lever at the lock edge of a moulded door", "lever": [80.0, 16.0], "lever_proud": 45.0, "rose_dia": 40.0, "rose_proud": 5.0, **CHROME,
                 "place": {"T3": {"u": 757.0, "v": t3_handle_v}}, "src": "Photo D4 right door: a dark mark at columns 577 to 578.5, rows 388 to 396, ON the door (the first box lay on the reveal), v 910 (the review's number; the box gives 921; +-32); lever size Judgement"},
        "HD3": {"name": "vertical bar pull on the lock stile", "size": [25.0, 270.0], "proud": 35.0, **STEEL_DARK,
                "place": {"T2": {"u": 57.2, "v": t2_handle_v}, "F3": {"u": 67.0, "v": 1255.0}},
                "src": "Photo D3: a dark vertical handle on the left stile, rows 498.25 to 524.25 of a 191.5 px visible leaf = 262 long (+-30), centred on the visible lock stile (u 57.2: the stile is 94.0 structural, 73.6 visible); D1 left door shows a vertical metal strip on its left stile"},
        "HD4": {"name": "thumb latch on a ledged door", "plate": [38.0, 190.0], "plate_t": 3.0, "bar": [20.0, 150.0], "thumb_piece": "a 25 x 35 pressed thumb piece", **STEEL_DARK,
                "place": {"F7": {"u": 838.0 - 100.0, "v": 1000.0}}, "src": "Judgement: the usual iron thumb latch for a ledged door; Hasluck draws only the hinges"},
    }
    F["latch"] = {
        "LK0": {"name": "none"},
        "LK1": {"name": "rim night latch, plain collar (the escutcheon), 3.1 T1", "collar": lk["outer_diameter_mm"], "plug": lk["plug_diameter_mm"], "collar_proud": 5.0, "keyway": "vertical 3 x 9", **CHROME,
                "place": {"T1": {"u": "46.6 from the stop face, right", "v": lk["centre_above_leaf_bottom_mm"]}}, "src": "3.1 as built (P1: collar 43.5, 8.4 px)"},
        "LK2": {"name": "rim night latch, knurled collar (the escutcheon), 3.1 F1", "collar": fir["cylinder_lock"]["outer_diameter_mm"], "plug": fir["cylinder_lock"]["plug_diameter_mm"], "collar_proud": 5.0, "scallops": 8,
                "keyway": "vertical 3 x 9", **CHROME, "place": {"F1": {"u": "46.3 from the stop face, right", "v": fir["cylinder_lock"]["centre_above_leaf_bottom_mm"]},
                                                              "F2": {"u": "46.3 from the stop face, right", "v": round(opt["furniture_heights_fraction_of_visible_height"]["cylinder"] * H31, 1)}},
                "src": "3.1 as built (P2: collar 37, scalloped)"},
        "LK3": {"name": "rim night latch, bare dark cylinder face under the lever, no collar", "collar": 18.0, "plug": 18.0, "collar_proud": 2.0, "keyway": "vertical 2 x 6", "material": "dark steel", "srgb": [40, 40, 42], "metal": 1.0, "roughness": 0.6,
                "place": {"F6": {"u": f6_lock_u, "v": f6_lock_v}},
                "src": "Photo D5 (an indoor landing door: the place only): a small dark mark under the lever, columns 766 to 771, rows 617 to 626, an 18 mm dark cylinder face at 0.976 of the face's width and 0.427 of its height (the review's u 743, v 845 were on the old 762 x 1981 basis)"},
    }
    F["keyhole"] = {
        "KH0": {"name": "none"},
        "KH1": {"name": "plugged mortice keyhole: a round head over a parallel slot, a dark recess 2 mm sunk, a pale metal blank filling the slot", "head_dia": 15.0, "slot_w": 8.0, "size": [23.0, 32.0], "depth": 2.0, "srgb": [60, 60, 62], "material": "dark recess, pale metal blank", "metal": 0.0, "roughness": 0.6,
                "place": {"F1": {"u": kh["centre_u_mm"], "v": kh["centre_above_leaf_bottom_mm"]}, "F2": {"u": kh["centre_u_mm"], "v": round(opt["furniture_heights_fraction_of_visible_height"]["old_keyhole"] * H31, 1)}},
                "src": "3.1 as built (P2 5x crop: (493, 447) px, 10 x 14 px = 23 x 32; head 15, slot 8); F1 at 3.1's v 1151, F2 at 0.606 of the visible height (P2)"},
    }
    F["knocker"] = {
        "KN0": {"name": "none", "note": "the default on every house"},
        "KN1": {"name": "ring knocker on a back plate (reserve, not placed)", "ring": [95.0, 12.0], "plate": [70.0, 110.0], "plate_t": 5.0, "material": "brass or iron", "place": {},
                "src": "Judgement: no period photograph read shows a knocker on these streets; the check refuses it on every house today"},
        "KN2": {"name": "plain bar knocker (reserve, not placed)", "size": [150.0, 30.0], "material": "brass", "place": {}, "src": "Judgement, as KN1"},
        "KN3": {"name": "lion's head knocker", "offered": False,
                "note": "NOT OFFERED: the photographs read (D1 to D9, P1, P2) show no lion's head on any door of these streets; the brief allows one only if they do"},
    }
    F["bell"] = {
        "BL0": {"name": "none"},
        "BL1": {"name": "plain dark oblong push, one part", "size": [22.0, 72.6], "proud": 3.0, "corner_r": 1.0, "groove": {"w": 14.0, "h": 2.0, "depth": 1.0, "below_centre": 8.0},
                "parts": 1, "material": "dark steel or dark plastic", "srgb": [60, 60, 62], "metal": 0.0, "roughness": 0.6,
                "place": {"T1": {"x": 859.4, "z_range": [1120.3, 1192.9], "on": "the right jamb's stop face (3.1 as built: x 859.4, z 1120.3 to 1192.9)"}},
                "forbidden": ["bezel", "button", "ring", "lens", "led", "camera", "speaker", "any second part", "rounded pill corners above 2 mm", "any bright or lit element"],
                "src": "Photo P1 16x crop rows 300.3 to 314.4: a dark-grey oblong 22 x 72.6, no bright element, a darker band a little below its middle; 3.1 review v2 (close) and the handover's fix: the two-part push is deleted"},
        "BL2": {"name": "old brass bell pull (reserve, not placed)", "knob": [40.0, 40.0], "rod": [12.0, 90.0], "material": "brass", "place": {},
                "src": "Judgement: no photograph read shows one; refused on every house today"},
    }
    F["number"] = {
        "NM0": {"name": "none"},
        "NM1": {"name": "screwed metal numerals in a row on the top rail", "digit": [51.0, 56.0], "stroke": 6.0, "relief": 3.0, "gap": 12.0, "face": "plain upright sans-serif, no serif, no real typeface", **BRASS,
                "place": {"T1": {"stacked": "two digits 39 x 72 on the muntin, v 1207 to 1277.6 and 1300 to 1373", "u": "leaf centre"}, "F1": {"v": 1917.0, "u": "leaf centre"},
                          "F2": {"v": 1922.0, "u": "leaf centre"}}, "src": "3.1 (P1 stacked on the muntin, P2 in a row on the top rail: 56 high); F2 at v 1922, the middle of the visible top rail, so the digits (to v 1950) stay under the visible top 1960.6 and in front of the transom"},
        "NM2": {"name": "black metal screwed numerals (reserve)", "digit": [51.0, 56.0], "stroke": 6.0, "relief": 3.0, **IRON_BLACK, "place": {}, "src": "Judgement"},
        "NM3": {"name": "numerals painted white on the leaf's top rail", "digit_h": 60.0, "stroke": 8.0, **PAINT_WHITE, "place": {"F3": {"v": 1925.0, "u": "leaf centre"}},
                "src": "Photo D6: a white numeral painted on a blue door (size Judgement, 60 +-15)"},
        "NM4": {"name": "numerals painted white on the transom glass (reserve, not placed)", "digit_h": 90.0, "stroke": 10.0, **PAINT_WHITE, "place": {},
                "src": "Judgement: a fanlight number is usual on such houses, but D3 shows its numerals on the leaf's top rail and none on the glass; refused on every house today (see NM6)"},
        "NM6": {"name": "small dark metal numerals on the leaf's top rail", "digit": [26.0, 30.0], "stroke": 3.5, "relief": 2.0, "gap": 8.0, "face": "plain upright sans-serif, no serif, no real typeface", **STEEL_DARK,
                "place": {"T2": {"v": 1898.6, "u": "leaf centre"}},
                "src": "Photo D3: small dark numerals centred on the leaf's top rail, 3 to 4 px high at 10.07 mm a pixel = 30 (+-10), box [78, 443, 84.5, 446.5] (masked in the preview); v 1898.6 is the middle of the visible top rail (the review's number)"},
        "NM5": {"name": "oval plaque with a relief ornament, no digits (reserve)", "size": [230.0, 154.0], "material": "dark moulded plastic with a pale rim", "place": {},
                "src": "Photo D2 white door: an oval 9.5 x 6.4 px at 24 mm a pixel (a house number's place); not placed"},
    }
    F["scraper"] = {
        "BS0": {"name": "none"},
        "BS1": {"name": "cast-iron boot scraper beside the step", "size": [330.0, 130.0, 200.0], "blade": [300.0, 25.0], "blade_thickness": 12.0, "blade_underside_notch": BS1_NOTCH,
                "standards": "two end standards 200 high, each a flat bar 25 x 12 rising from a splayed foot to a scroll of radius 35 curling outward at the top; the profile is the point list standard_profile_xz (x outward from the blade's end, z up, mm), mirrored for the other end",
                "standard_profile_xz": scraper_standard_profile(),
                **IRON_BLACK, "place": {"T1": {"x_from_jamb": "left, 150 clear of the step's end", "z": 0.0}},
                "src": "Photo D10 (2014, said why: iron fittings of this kind were never renewed): scrolled standards and a blade with a notched underside; every size and the profile are Judgement, the photograph has no scale in its plane (+-25 per cent)"},
    }
    return F


GLASS = {
    "plain_3mm": {"name": "plain clear float", "thickness": 3.0, "ior": 1.5, "roughness": 0.05, "transmission": 1.0, "src": "3.1"},
    "reeded_4mm": {"name": "reeded (ribbed) glass", "thickness": 4.0, "flute_pitch": 6.0, "flute_depth": 1.2, "section": "circular segments, vertical", "roughness": 0.08, "transmission": 0.9,
                   "src": "Judgement: reeded glass in F6's transom (D5's ribbed transom and sidelight are an indoor lining's, not a street door's); pitch and depth Judgement"},
    "leaded_diamond": {"name": "leaded light: a plain upper pane over a band of crossed diagonal came", "came_w": 6.0, "came_proud": 3.0, "plain_pane_h": 144.0, "band_h": 83.0, "lozenge": [145.0, 83.0],
                       "foot_came_above_foot": 40.0, "uprights": "one under each lozenge point (5)", "whole_lozenges": 5,
                       "layout": "in a light 772 x 267: the upper 144 plain; under it the band 83 high of two families of diagonal came crossing in a lattice of lozenges 145 wide and 83 high, the lozenge points (their lower vertices) on x = centre + k x 145 for k = -2 to 2 (5 whole lozenges, a tip of the next at each end, 23.5 wide), a horizontal came at the top of the band; a horizontal came 40 above the foot with an upright under each lozenge point down to the glass foot",
                       "glass_t": 3.0, "came_material": "dull lead-grey (90, 92, 95), roughness 0.5",
                       "src": "Photo D3 (fanlight rows 376 to 436 at 10.07 mm a pixel): the upper 54 per cent one plain pane (rows 376 to 408), a band of crossed diagonals at a 14.3 px (144 mm) pitch (rows 408 to 427), a foot strip with an upright under each lozenge point (rows 427 to 436); the T frame's 267 mm light is kept; came 6 wide is Judgement"},
    "frosted": {"name": "acid-etched frosted (reserve, not placed)", "thickness": 4.0, "roughness": 0.35, "transmission": 0.6, "src": "Judgement; no photograph read shows it"},
    "wired": {"name": "wired polished (reserve, not placed)", "thickness": 6.0, "mesh": 12.5, "wire_dia": 0.6, "src": "Judgement; a stair door of a council block; none read"},
    "lens_14": {"name": "door viewer lens, 14 across (D5's spyhole place only)", "dia": 14.0, "src": "Photo D5, place only"},
}
