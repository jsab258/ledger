"""Door furniture variants of the front-doors-all target: size, place, material, colour, source. Positions are per kind (the leaf frame: u across
from the leaf's left edge seen from outside, v up from its bottom). No real maker's name or mark anywhere: the 'Yale-type' lock is a rim night latch.
make_target.py writes these into target.json under furniture."""
import sys

from td_kinds import d2_f5_fractions, d4_t3_fractions, d5_fractions, d3_fractions

sys.dont_write_bytecode = True

BRASS = {"material": "brass", "srgb": [181, 150, 85], "metal": 1.0, "roughness": 0.4, "worn_roughness": 0.25}
CHROME = {"material": "nickel or chrome-look", "srgb": [170, 170, 168], "metal": 1.0, "roughness": 0.35}
ALU = {"material": "anodised aluminium, pale", "srgb": [190, 190, 185], "metal": 1.0, "roughness": 0.45}
STEEL_DARK = {"material": "dark steel", "srgb": [40, 40, 42], "metal": 1.0, "roughness": 0.6}
IRON_BLACK = {"material": "cast iron, black", "srgb": [30, 30, 32], "metal": 1.0, "roughness": 0.65}
PLASTIC_WHITE = {"material": "white moulded plastic", "srgb": [226, 224, 214], "metal": 0.0, "roughness": 0.4}
PAINT_WHITE = {"material": "white gloss paint", "srgb": [226, 224, 214], "metal": 0.0, "roughness": 0.35}


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
    slit_plate_v = round((f5["plate"]["v"][0] + f5["plate"]["v"][1]) / 2.0 * 1960.6, 1)
    t3_plate_v = round((f4["plate"]["v"][0] + f4["plate"]["v"][1]) / 2.0 * 1927.6, 1)
    f6_plate_v = round((f6["plate"]["v"][0] + f6["plate"]["v"][1]) / 2.0 * 1981.0, 1)
    f6_handle_v = round((f6["handle"]["v"][0] + f6["handle"]["v"][1]) / 2.0 * 1981.0, 1)
    f5_handle_v = round((f5["handle"]["v"][0] + f5["handle"]["v"][1]) / 2.0 * 1960.6, 1)
    f5_handle_u = round(20.4 + (f5["handle"]["u"][0] + f5["handle"]["u"][1]) / 2.0 * 797.2, 1)
    f5_plate_u = round(20.4 + (f5["plate"]["u"][0] + f5["plate"]["u"][1]) / 2.0 * 797.2, 1)
    t3_handle_v = round((f4["handle"]["v"][0] + f4["handle"]["v"][1]) / 2.0 * 1927.6, 1)
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
                "place": {"F6": {"u": round(0.5 * (f6["plate"]["u"][0] + f6["plate"]["u"][1]) * 762.0, 1), "v": f6_plate_v}},
                "src": "Photo D5: 107 x 30 px at 2.35 mm a pixel = 250 x 70, centre at 0.506 of the leaf's width and 912 above its foot (+-15)"},
        "LP5": {"name": "pale low plate in the bottom rail", "outer": [250.0, 50.0], "frame_w": 5.0, "proud": 2.0, **ALU,
                "place": {"T2": {"u": "leaf centre", "v": 100.0}, "F4": {"u": "leaf centre", "v": 100.0}},
                "src": "Photo D1 right door (rows 659 to 662.5 of a 150 px leaf: centre 83 above the foot, 46 high) and D4 black door (a 10 x 3 px plate at the foot, 90): centre 100 chosen to sit mid-rail (+-20)"},
        "LP6": {"name": "white plastic oblong in a moulded door", "outer": [270.0, 50.0], "frame_w": 5.0, "proud": 3.0, **PLASTIC_WHITE,
                "place": {"T3": {"u": "leaf centre", "v": t3_plate_v}}, "src": "Photo D4 right door: 12 x 3.1 px at 21.7 mm a pixel = 260 x 67, centre 0.448 of the visible height (+-25)"},
        "LP7": {"name": "small pale plate under a slit light", "outer": [265.0, 50.0], "frame_w": 5.0, "proud": 2.0, **ALU,
                "place": {"F5": {"u": f5_plate_u, "v": slit_plate_v}}, "src": "Photo D2 middle door: 11 x 2 px at 23.8 mm a pixel = 262 x 48 (+-24), centre about 830"},
    }
    F["handle"] = {
        "HD0": {"name": "none", "note": "T1, T2's lock side has HD3, F7 HD4"},
        "HD1": {"name": "turned centre knob on a dished rose", "dia": kn["diameter_mm"], "proud": kn["projection_mm"], "rose": kn["rose_diameter_mm"], "profile_rz": kn["profile_rz_mm"],
                "cap": "brass 4 mm", "material": "black-painted wood, brass cap", "srgb": [35, 36, 40],
                "place": {"F1": {"u": "leaf centre", "v": kn["centre_above_leaf_bottom_mm"]}, "F2": {"u": "leaf centre", "v": round(opt["furniture_heights_fraction_of_visible_height"]["knob"] * H31, 1)}},
                "src": "3.1 as built (P2 8x crop)"},
        "HD2a": {"name": "lever handle on a round rose, chrome-look, right stile", "lever": [105.0, 18.0], "lever_proud": 55.0, "rose_dia": 50.0, "rose_proud": 6.0, **CHROME,
                 "place": {"F6": {"u": round(0.5 * (f6["handle"]["u"][0] + f6["handle"]["u"][1]) * 762.0, 1), "v": f6_handle_v}},
                 "src": "Photo D5: lever 45 px = 106 at 2.35 mm a pixel, centre 902 above the foot (+-15), on the right stile"},
        "HD2b": {"name": "lever handle on a round rose, chrome-look, left stile", "lever": [100.0, 18.0], "lever_proud": 55.0, "rose_dia": 50.0, "rose_proud": 6.0, **CHROME,
                 "place": {"F5": {"u": f5_handle_u, "v": f5_handle_v}, "F4": {"u": 95.0, "v": 1228.0}},
                 "src": "Photo D2: a small pale handle at the left stile of the middle door, 0.557 of the visible height (about 1092, +-24); the left door's at about 1228 (+-30)"},
        "HD2c": {"name": "short lever at the lock edge of a moulded door", "lever": [80.0, 16.0], "lever_proud": 45.0, "rose_dia": 40.0, "rose_proud": 5.0, **CHROME,
                 "place": {"T3": {"u": 757.0, "v": t3_handle_v}}, "src": "Photo D4 right door: a dark 2 x 4 px mark at the right edge, 0.43 of the visible height (+-35); lever size Judgement"},
        "HD3": {"name": "vertical bar pull on the lock stile", "size": [25.0, 270.0], "proud": 35.0, **STEEL_DARK,
                "place": {"T2": {"u": 67.0, "v": round(1927.6 * 0.5 * ((633.75 - 524.25) / 190.0 + (633.75 - 498.25) / 190.0), 1)}, "F3": {"u": 67.0, "v": 1255.0}},
                "src": "Photo D3: a dark vertical handle on the left stile, rows 498.25 to 524.25 of a 190 px visible leaf = 264 long, v 1111 to 1375 (+-30); D1 left door shows a vertical metal strip on its left stile"},
        "HD4": {"name": "thumb latch on a ledged door", "plate": [38.0, 190.0], "plate_t": 3.0, "bar": [20.0, 150.0], "thumb_piece": "a 25 x 35 pressed thumb piece", **STEEL_DARK,
                "place": {"F7": {"u": 838.0 - 100.0, "v": 1000.0}}, "src": "Judgement: the usual iron thumb latch for a ledged door; Hasluck draws only the hinges"},
    }
    F["latch"] = {
        "LK0": {"name": "none"},
        "LK1": {"name": "rim night latch, plain collar (the escutcheon), 3.1 T1", "collar": lk["outer_diameter_mm"], "plug": lk["plug_diameter_mm"], "collar_proud": 5.0, "keyway": "vertical 3 x 9", **CHROME,
                "place": {"T1": {"u": "46.6 from the stop face, right", "v": lk["centre_above_leaf_bottom_mm"]}}, "src": "3.1 as built (P1: collar 43.5, 8.4 px; the 3.1 name for it was cylinder lock)"},
        "LK2": {"name": "rim night latch, knurled collar (the escutcheon), 3.1 F1", "collar": fir["cylinder_lock"]["outer_diameter_mm"], "plug": fir["cylinder_lock"]["plug_diameter_mm"], "collar_proud": 5.0, "scallops": 8,
                "keyway": "vertical 3 x 9", **CHROME, "place": {"F1": {"u": "46.3 from the stop face, right", "v": fir["cylinder_lock"]["centre_above_leaf_bottom_mm"]},
                                                              "F2": {"u": "46.3 from the stop face, right", "v": round(opt["furniture_heights_fraction_of_visible_height"]["cylinder"] * H31, 1)}},
                "src": "3.1 as built (P2: collar 37, scalloped)"},
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
                          "F2": {"v": 1943.0, "u": "leaf centre"}}, "src": "3.1 (P1 stacked on the muntin, P2 in a row on the top rail: 56 high)"},
        "NM2": {"name": "black metal screwed numerals (reserve)", "digit": [51.0, 56.0], "stroke": 6.0, "relief": 3.0, **IRON_BLACK, "place": {}, "src": "Judgement"},
        "NM3": {"name": "numerals painted white on the leaf's top rail", "digit_h": 60.0, "stroke": 8.0, **PAINT_WHITE, "place": {"F3": {"v": 1925.0, "u": "leaf centre"}},
                "src": "Photo D6: a white numeral painted on a blue door (size Judgement, 60 +-15)"},
        "NM4": {"name": "numerals painted white on the transom glass", "digit_h": 90.0, "stroke": 10.0, **PAINT_WHITE, "place": {"T2": {"on": "the transom glass, centred"}},
                "src": "Judgement: a fanlight number is standard on such houses; no period photograph read shows one at a readable size"},
        "NM5": {"name": "oval plaque with a relief ornament, no digits (reserve)", "size": [230.0, 154.0], "material": "dark moulded plastic with a pale rim", "place": {},
                "src": "Photo D2 white door: an oval 9.5 x 6.4 px at 24 mm a pixel (a house number's place); not placed"},
    }
    F["scraper"] = {
        "BS0": {"name": "none"},
        "BS1": {"name": "cast-iron boot scraper beside the step", "size": [330.0, 130.0, 200.0], "blade": [300.0, 25.0], "standards": "two end standards 200 high with scroll tops",
                **IRON_BLACK, "place": {"T1": {"x_from_jamb": "left, 150 clear of the step's end", "z": 0.0}},
                "src": "Photo D10 (2014, said why: iron fittings of this kind were never renewed); sizes are Judgement, the photograph has no scale in its plane (+-25 per cent)"},
    }
    return F


GLASS = {
    "plain_3mm": {"name": "plain clear float", "thickness": 3.0, "ior": 1.5, "roughness": 0.05, "transmission": 1.0, "src": "3.1"},
    "reeded_4mm": {"name": "reeded (ribbed) glass", "thickness": 4.0, "flute_pitch": 6.0, "flute_depth": 1.2, "section": "circular segments, vertical", "roughness": 0.08, "transmission": 0.9,
                   "src": "Photo D5: a ribbed transom and sidelight, vertical flutes; pitch and depth Judgement"},
    "leaded_diamond": {"name": "leaded light, diamond lattice", "came_w": 6.0, "came_proud": 3.0, "diamond": [95.0, 70.0], "glass_t": 3.0, "came_material": "dull lead-grey (90, 92, 95), roughness 0.5",
                       "src": "Photo D3: a leaded diamond fanlight over the leaf; the pitch is scaled to the T frame's 267 high light (Judgement)"},
    "frosted": {"name": "acid-etched frosted (reserve, not placed)", "thickness": 4.0, "roughness": 0.35, "transmission": 0.6, "src": "Judgement; no photograph read shows it"},
    "wired": {"name": "wired polished (reserve, not placed)", "thickness": 6.0, "mesh": 12.5, "wire_dia": 0.6, "src": "Judgement; a stair door of a council block; none read"},
    "lens_14": {"name": "door viewer lens, 14 across (D5's spyhole place only)", "dia": 14.0, "src": "Photo D5, place only"},
}
