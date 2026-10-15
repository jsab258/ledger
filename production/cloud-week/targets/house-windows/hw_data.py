"""Static data of the house-windows target (cloud week 42, unit 8): the kinds, the glass, the nets, the rooms, the inventory of models and
their marks, the lit share by hour. make_target.py assembles target.json from this and from what it derives (the sites from
terrace-front.py, the kit's nodes from the checked .glb files, the stand-off budgets from hw_common.py, the photograph measurements).
Units: millimetres for window parts (kit frame: x across the window, 0 at its middle; y INTO the wall from the brick face, 0 at the face;
z UP from the opening's bottom edge); metres for rooms and the street. Kinds of number: Read, Scaled, Photo, Derived, Judgement."""

# ---------------------------------------------------------------------------------------------------------------------------
# colours: sRGB triples (0-255) as seen; the builder converts to linear
PAINTS = {
    "white_fresh":   {"srgb": [234, 233, 229], "lin": [0.82, 0.812, 0.78], "rough": 0.42, "note": "the street's paint_joinery as it stands (terrace-front.py MATERIALS) and the lab sash's paint: the kit pieces' default; sound gloss white: east_parade_bay1 and west_south_bay2 take it as it is (the box shade's keep_paint rule applies to this paint only)"},
    "white_grimy":   {"srgb": [214, 212, 205], "lin": [0.68, 0.66, 0.62], "rough": 0.48, "note": "weathered 1990 gloss white, 1a's 0.72 to 0.80 less the dirt in the lower rails and the sill: the lower rail and sill at x 0.85, the rest 1.0; east_parade_bay0, east_parade_bay5 and west_south_bay0"},
    "white_flaking": {"srgb": [205, 202, 192], "lin": [0.60, 0.58, 0.53], "rough": 0.55, "note": "east_parade_bay3's paint (the unlet house): 12 per cent of the area on the lower rails, sill and stiles' feet is flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40)"},
    "cream":         {"srgb": [222, 204, 164], "lin": [0.73, 0.60, 0.37], "rough": 0.45, "note": "NOT USED ON ANY HOUSE until Jafar's page rules otherwise (his ruling of 3 October is white frames; D13). Kept as data for the photographs' mix: P3's cream-painted sashes (frame sampled 181, 163, 131 in the sun and shade of the photograph, so the paint is lighter), P2's cream render"},
    "olive":         {"srgb": [136, 140, 64], "lin": [0.246, 0.262, 0.052], "rough": 0.45, "note": "NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13). Kept as data: P12's two olive-green sashes (sampled 148, 153, 70); a painted window of a house that chose its own colour"},
    "blue":          {"srgb": [56, 92, 160], "lin": [0.040, 0.107, 0.352], "rough": 0.42, "note": "NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13). Kept as data: P2's blue sashes (sampled 61, 87, 136), the tenants' own paint on a terrace of one owner"},
    "brown":         {"srgb": [84, 58, 42], "lin": [0.089, 0.042, 0.023], "rough": 0.42, "note": "NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13). Kept as data: P1's four dark-brown sashes and P3's red-brown frames (sampled 141, 131, 115 and 162, 129, 119 in the sun): an oxide or brown gloss, the second commonest painted colour after white"},
    "bronze":        {"srgb": [74, 60, 52], "lin": [0.05, 0.038, 0.03], "rough": 0.35, "note": "NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13: the question of the chandler's bronze is on that line). The street's frame_bronze (terrace-front.py): dark anodised aluminium; NOT seen in any reached photograph (D1)"},
    "white_upvc":    {"srgb": [232, 231, 225], "lin": [0.80, 0.792, 0.762], "rough": 0.30, "note": "white replacement frame, satin: P6, P7, P11 show white in every case (4 of 4); the four replacement houses (east_parade_bay2, east_parade_bay4, west_south_bay1, east_chandler_bay0)"},
}

# ---------------------------------------------------------------------------------------------------------------------------
# nets, curtains, blinds (kit frame: mm). plane = depth behind the brick face (y). card dims: x0,x1 across; z0,z1 up from the opening bottom.
NETS = {
    "N0": {"label": "bare glass", "what": "no net: the room is seen (dark by day)", "share_photo": 0.18},
    "N1": {"label": "lower-sash voile", "what": "a gathered voile on a wire at the meeting rail, hem near the sill; the upper sash clear",
           "card": {"x": [-450, 450], "z": [60, 880]}, "height_mm": 820, "plane_mm": {"S22": 254, "S11": 254, "RC": 235, "RC2": 235},
           "lace_band": {"share_of_height": 0.30, "pattern_repeat_mm": 60, "coverage": 0.62}, "voile_coverage": 0.40, "share_photo": 0.47},
    "N2": {"label": "full-height net", "what": "a gathered net from a rod at the head to a hem near the sill",
           "card": {"x": [-450, 450], "z": [60, 1630]}, "height_mm": 1570, "plane_mm": {"S22": 254, "S11": 254, "RC": 235, "RC2": 235},
           "lace_band": {"share_of_height": 0.18, "pattern_repeat_mm": 60, "coverage": 0.62}, "voile_coverage": 0.40, "share_photo": 0.22},
    "N3": {"label": "cafe net", "what": "a half-height net on a rod across the lower sash: covers the lower third of the window only",
           "card": {"x": [-430, 430], "z": [100, 500]}, "height_mm": 400, "plane_mm": {"S22": 254, "S11": 254, "RC": 235, "RC2": 235},
           "lace_band": {"share_of_height": 0.0, "pattern_repeat_mm": 0, "coverage": 0.0}, "voile_coverage": 0.45, "share_photo": 0.02},
}
NET_COMMON = {
    "weave": "plain voile: threads under 1 mm, a pitch of 1.2 mm, so under one pixel from 1.5 m outwards: the net reads as an even translucent sheet with fold shading; only the lace band shows a pattern (repeat 60 mm) and only from under 3 m",
    "layers_and_coverage": "one layer covers 0.40 (voile) to 0.62 (lace band) of its area; gathered at 200 per cent fullness the folds overlap so the mean covered share of the sheet is 1 - (1 - 0.40)^2 = 0.64 voile, 0.86 lace band (Derived); the card's alpha is the weave and folds",
    "fullness": 2.0,
    "gather_wavelength_mm": [40, 55],
    "gather_depth_mm": 12,
    "fold_brightness_modulation": 0.22,
    "hem": "a lace border 28 mm high, scalloped, period 35 mm; the hem sags up to 12 mm between folds (the lower edge is a gentle sine of amplitude 6 mm and wavelength 90 mm)",
    "head": "a 20 mm double-thickness casing at the top (alpha 0.92) with a 2 mm dark wire line under it (alpha 0.5, luma 60)",
    "colours": {"white": [238, 238, 232], "greyed": [208, 208, 200], "yellowed": [222, 206, 158]},
    "photo_note": "P1 sampled a sunlit white net at (208, 201, 181); nets read 0.60 to 0.97 of the frame's luma in the photographs (n=9)",
    "day_look": "lit from outside by daylight: albedo x lit by the street's sky and the window's own shadow; the net is NOT emissive by day (net_day_gain 0.0, unreal-look.json)",
    "night_lit": "emissive warm tungsten: linear (1.0, 0.714, 0.344) (vignette-pieces window_practicals gamma (1, 0.86, 0.62); the street's interior_lit) x the lit-net strength 1.2 x room_glow_gain_night 0.4 = 0.48 (unreal-look.json); folds darker, the room's pendant and furniture seen through it",
    "night_dark": "unlit: net emissive 0.05 x 0.4 = 0.02 (the street's NET_EMIT_NIGHT 0.05): only the sodium lamp's colour on its fabric",
    "no_parallax": "a net 65 mm behind the glass moves under a pixel at 10 m (1a): a flat card, not geometry",
}
CURTAINS = {
    "C1": {"label": "curtains drawn", "what": "lined curtains drawn across the whole window, in front of the net", "card": {"x": [-480, 480], "z": [0, 1780]}, "plane_mm": 262,
           "opacity": 0.97, "folds": "wavelength 70 to 90 mm, brightness modulation 0.25, straight hem, a pelmet band 60 mm high at the top",
           "colours": {"cream": [214, 198, 166], "brown": [110, 82, 62], "green": [72, 98, 74]},
           "night_lit": "colour x warm light x 0.35 transmission: the curtain glows its own colour, folds dark",
           "night_lit_emission_linear": {"cream": [0.316, 0.189, 0.062], "brown": [0.417, 0.161, 0.044], "green": [0.172, 0.232, 0.063]},
           "night_lit_emission_note": "ABSOLUTE linear emission of the lit fabric (TARGET-REVIEW narrow point 5): the colour's linear albedo x the warm light (1.0, 0.714, 0.344), scaled so that the emission's luma is 0.207; seen through a square-on pane (two-face reflectance 0.082) the gate's pane median then reads 0.19 linear = sRGB 121, inside 100 to 140. Derived from the stated colours; a drawn curtain's transmission 0.35 is what the scale stands for. The lit set at 20:30 has no green drawn curtain (g > r would break r > g > b).",
           "share_photo": 0.05},
    "C2": {"label": "curtains open", "what": "a pair drawn back to the sides, two cards each 170 wide", "card_left": {"x": [-480, -310], "z": [0, 1780]}, "card_right": {"x": [310, 480], "z": [0, 1780]},
           "plane_mm": 262, "opacity": 0.97, "folds": "as C1", "colours": {"cream": [214, 198, 166], "brown": [110, 82, 62], "green": [72, 98, 74], "floral_cream": [224, 210, 180]},
           "night_lit": "as C1", "night_lit_emission_linear": {"cream": [0.316, 0.189, 0.062], "brown": [0.417, 0.161, 0.044], "green": [0.172, 0.232, 0.063], "floral_cream": [0.309, 0.191, 0.065]},
           "night_lit_emission_note": "as C1: the pair at the sides glows this; the net between them is lit as NET_COMMON night_lit says", "share_photo": 0.05},
}
BLINDS = {
    "B1": {"label": "venetian blind", "what": "a white aluminium venetian blind lowered 60 per cent of the height (z 660 to 1650), slats 25 mm, tilted closed 70 per cent", "card": {"x": [-400, 400], "z": [660, 1650]},
           "plane_mm": 240, "slat_pitch_mm": 25, "colour": [210, 210, 205], "slat_gap_alpha": 0.25, "night_lit": "slat gaps glow warm: stripes of light at the 25 mm pitch (visible under 8 m)", "night_lit_emission_linear": [0.277, 0.198, 0.09], "share_photo": 0.01},
    "B2": {"label": "roller blind", "what": "a cream roller blind half down (z 700 to 1660) with a pull cord and a 20 mm bottom batten", "card": {"x": [-390, 390], "z": [700, 1660]}, "plane_mm": 240,
           "colour": [226, 214, 176], "opacity": 0.9, "night_lit": "an even warm sheet of colour x 0.5 transmission, a dark bottom batten", "night_lit_emission_linear": [0.305, 0.193, 0.06], "share_photo": 0.01},
    "B3": {"label": "vertical louvre blind", "what": "white vertical louvres 89 mm, turned 40 per cent open (P2's ground window)", "card": {"x": [-420, 420], "z": [100, 1640]}, "plane_mm": 240,
           "slat_pitch_mm": 89, "colour": [226, 226, 220], "slat_gap_alpha": 0.35, "night_lit": "vertical stripes of warm light at the 89 mm pitch", "night_lit_emission_linear": [0.277, 0.198, 0.09], "share_photo": 0.01},
}

# ---------------------------------------------------------------------------------------------------------------------------
# the replacement casement RC (new): 850 x 1676.4 opening; mm in the kit frame
RC = {
    "label": "replacement casement (1970s to 1980s council or owner replacement): a fixed light under a top-hung light, no bars",
    "opening": {"w": 850.0, "h": 1676.4},
    "frame_face": 60.0, "frame_depth": 70.0, "frame_front_y": 72.5,
    "transom": {"centre_fraction": 0.72, "face": 70.0},
    "vent_sash": {"stile_face": 45.0, "gap": 4.0},
    "glass_plane_y": 112.5, "glass_mm": 4.0, "unit_note": "a sealed unit 4-16-4: the cloud and the game draw one pane (F0 0.08); the real unit's four faces reflect about 0.14 at normal incidence (a known shortfall, listed)",
    "gasket": {"width": 3.0, "luma_factor": 0.30},
    "weld_groove": {"width": 2.0, "luma_factor": 0.35},
    "photo_transom_fractions": {"P6": 0.66, "P11": 0.75, "P7": 0.72},
    "materials": {"default": "white_upvc", "metal_refit": "bronze (NOT USED: no house takes it until Jafar's page rules otherwise, D13)"},
}

# the replacement casement RC2 (the P6 form, added by the fixes of 13 October: narrow point 7): a fixed top light across over TWO lower lights, a side-hung
# casement beside a fixed light, the mullion at the middle. Same opening, same frame section and glass plane as RC; assigned to east_parade_bay4 (both windows).
RC2 = {
    "label": "replacement casement, the P6 form (Levenshulme, 1994): a fixed top light across over two lower lights, a side-hung casement beside a fixed light with a mullion at the middle, no bars",
    "opening": {"w": 850.0, "h": 1676.4},
    "frame_face": 60.0, "frame_depth": 70.0, "frame_front_y": 72.5,
    "transom": {"centre_fraction": 0.66, "face": 70.0, "note": "P6's 0.66 (Photo): 0.66 x 1676.4 = 1106.4 above the opening's bottom"},
    "top_light": "one fixed pane across the whole width (no sash, no gap)",
    "mullion": {"face": 70.0, "x_centre": 0.0, "z_from": 60.0, "note": "70 mm wide, centred on x = 0, from the sill rail's top (z 60) to the transom's underside (1071.4)"},
    "casement": {"side": "left light", "stile_face": 45.0, "rail_face": 45.0, "gap": 4.0, "hinge": "side-hung on the jamb side: the hinge on the left jamb (the stile at x -361 to -316 is the hanging stile), the stile by the mullion the closing stile"},
    "fixed_light": "the right light: one fixed pane in the frame",
    "glass_plane_y": 112.5, "glass_mm": 4.0, "unit_note": "as RC: a sealed unit 4-16-4 drawn as one pane (a known shortfall, listed)",
    "gasket": {"width": 3.0, "luma_factor": 0.30},
    "weld_groove": {"width": 2.0, "luma_factor": 0.35},
    "photo_transom_fractions": {"P6": 0.66},
    "materials": {"default": "white_upvc"},
    "assigned_to": ["east_parade_bay4"],
}

# ---------------------------------------------------------------------------------------------------------------------------
# glass
GLASS = {
    "pane": {
        "game": "one opaque Default Lit material on the pane (research 1a, step 1): base colour = lerp(room 0.03, lace x 0.6, the net's alpha) with the alpha WIRED; Specular 1.0 (F0 0.08, standing for both faces of a single pane); roughness 0.03; metallic 0; day emissive 0",
        "base_colour_room_linear": 0.03, "lace_albedo_factor": 0.6, "specular": 1.0, "f0": 0.08, "roughness": 0.03, "roughness_range": [0.02, 0.04], "metallic": 0.0, "day_emissive": 0.0,
        "cloud_stand_in": "Cycles Principled BSDF, NOT Glass BSDF: Base Color 0.03 (linear grey) with the net card's alpha as the mix, Specular IOR Level 1.0, Roughness 0.03, Transmission 0, Metallic 0, the room card (baked through `trace`) as Emission x (1 - Fresnel) x brightness; the opposite row and the sky dome are what it reflects (Cycles traces them; Lumen's reflections and the box-projected street cube are the game's)",
        "fresnel_two_face": {"90": 0.082, "30": 0.157, "24": 0.215, "18": 0.314, "16": 0.360, "10": 0.544, "8": 0.622},
        "fresnel_note": "Unreal's Specular 1 (F0 0.08, Schlick) gives 0.26 at 16 degrees from the wall, about three quarters of the true two-face figure (0.36): close enough",
    },
    "waviness": {
        "what": "per-pane tilt, not a wave texture: each pane mesh is rotated by a seeded angle uniform in +-0.5 degrees about the vertical axis and +-0.3 degrees about the horizontal one (never zero, the spread of a window's panes at least 0.3 degrees)",
        "photo": "P8 (Oxford rear, 1987): the four panes of the two windows measured (the boxes of section 3.2) read mean luma 86, 100, 100 and 105 (19 levels apart, 18 per cent of the brightest); inside, three are flat to 1.2 to 1.4 levels (the central 60 per cent of the box) and the fourth, the right window's upper pane, carries a brighter patch (95th percentile 176): the glass is flat to the eye and each pane catches the sky differently",
        "no_wave_normal_map": True,
    },
    "dirt": "a 6 mm band round every pane's edge is roughened (roughness 0.35, base colour x 0.8): the putty line's dirt; the lowest 25 mm of each pane carries the same (water and dust on the bottom rail)",
    "reflections_by_floor": {
        "upper": "from across the street a ray off an upper pane goes up at the eye's own elevation (18 to 22 degrees) and meets only sky (the west row's roofs are 3 m eaves; the ray is 9 m up by the west frontage): the pane carries the SKY at 8 per cent and the room at 92 per cent; P8 (blue-grey 87, 99, 135) shows it",
        "ground": "a ground pane across the street reflects the opposite row at eye height: the parade's dark fascias and the hill's trees: a darker band; the room dominates"
    },
}

BOX_SHADE = {
    "what": "1a step 2 as numbers, put in the joinery's vertex colour (COLOR_0 red channel multiplies the paint; not the AO pin)",
    "street_facing_faces": 1.0, "street_facing_note": "faces whose normal points to the street (the outer lining's street face at y 114.3, the sash rails' fronts, the sill's top) take 1.0: they are L itself, and darkening them would darken the frame the gate measures (TARGET-REVIEW narrow point 4)",
    "lining_from_brick_edge_to_glass": {"at_brick_edge": 1.0, "at_glass": 0.6, "law": "linear in depth from y = 0 to the glass plane; applies ONLY to the faces that run into the wall: the reveal-facing sides of the linings, the beads, the pulley stiles and the sash stiles"},
    "track_faces": 0.5, "track_note": "the faces of the pulley-stile track between the parting bead and the staff bead",
    "inside_corners": 0.3, "inside_corner_reach_mm": 8.0,
    "brick_returns_of_the_reveal": [0.6, 0.8], "brick_returns_note": "in the wall mesh, not the kit; stated so the wall kit takes it: 0.8 at the face falling to 0.6 at the sash, and 0.7 under the head",
    "putty_and_shadow_line_round_each_pane": {"width_mm": 6.0, "factor": 0.35, "note": "the kit's putty strips (14 on a 2/2) are 6.4 mm wide: painted 0.35"},
    "meeting_rail_underside": 0.40, "parting_bead_gap": 0.10, "parting_bead_gap_width_mm": 2.0,
    "keep_paint": {"applies_to": "white_fresh only", "albedo": [0.78, 0.80], "roughness": 0.40, "try_once": 0.35,
                   "note": "1a's keep-the-paint figure is for the sound gloss white (white_fresh: albedo about 0.80, roughness 0.42 in `paints`); every other house takes its own paint from the `paints` table (white_grimy 0.66 at roughness 0.48, white_flaking 0.58 at 0.55, white_upvc 0.79 at 0.30), which governs, not this line"},
    "line_width_rule": "at least one pixel at 10 m: 6 mm (1 px = 5.9 mm at 10 m for 1440 lines at 46 degrees, 1a); every dark line of the box is at least 6 mm wide",
}

# ---------------------------------------------------------------------------------------------------------------------------
# lit share by hour (judgement, anchored on the street's rule NET_LIT_EVERY = 3 and the two always-lit cottage windows)
LIT_SHARE = {
    "source": "Judgement. production/research/evening-light-1990 gives no share (its windows line: 'whitish fluorescent from shops, warm tungsten behind house curtains', marked its own inference); the street already lights one in three at 20:30 (terrace-front.py NET_LIT_EVERY = 3) and two cottage windows always (NET_LIT_ALWAYS). No 1975 to 1995 night photograph of a terrace was reached (no Geograph result before 1996 for night, dusk or lit windows). Kept near the street's one in three; the rest of the day follows habit (lights on at dusk, out by midnight).",
    "table_hour_to_share_of_all_20_windows": {"05:00": 0.05, "06:00": 0.10, "07:00": 0.15, "08:00": 0.05, "17:00": 0.05, "18:00": 0.15, "19:00": 0.30, "20:00": 0.35, "20:30": 0.35, "21:00": 0.35, "22:00": 0.30, "23:00": 0.20, "00:00": 0.10, "01:00": 0.05},
    "rule": "a window is lit at hour h when its place in the lit order is below round(share(h) x 20); the order is fixed (below) and never reshuffled, so a window lit at 23:00 is lit at 20:30; empty rooms are never lit; the two cottage windows of the always-lit house are lit from 18:00 to 23:00 whatever the share. THE ORDER (TARGET-REVIEW narrow point 6, Judgement): in 1990 the evening's light is in the front room or the lounge and a landing is lit briefly; after the always-lit pair: the cottage front room west_south_bay1_gf_w1, then the three lounges, then a bedroom (the chandler's), then the other cottage front rooms, then the other bedrooms, then the landings. The review's text names east_chandler_bay0_upper_w1 as the fifth, but that window is a landing (up_landing_2, as the review's own fault text says): the chandler's bedroom window, _w0, stands there",
    "by_day": "no window is lit by day; a lit room by day would be invisible in the glass's reflection",
    "lit_at_20_30": 7,
    "tolerance_at_20_30": 1,
}

# the order in which windows are lit after the always-lit pair (west_south_bay2: both windows). Fixed, never reshuffled. The counts by hour are the table above.
# The review names east_chandler_bay0_upper_w1 as the fifth: that window is a landing (up_landing_2, SITE_PLAN and the review's own fault text), so the chandler's
# other window, east_chandler_bay0_upper_w0 (its bedroom, up_bedroom_3), stands there (flagged in FIXES-APPLIED.md).
LIT_ORDER = [
    "west_south_bay1_gf_w1",          # a cottage front room, the evening room
    "east_parade_bay0_upper_w1",      # lounge 1
    "east_parade_bay2_upper_w0",      # lounge 2
    "east_parade_bay5_upper_w0",      # lounge 3
    "east_chandler_bay0_upper_w0",    # bedroom 3 (the review's text says _w1, a landing)
    "west_south_bay1_gf_w0", "west_south_bay0_gf_w1", "west_south_bay0_gf_w0",     # the other cottage front rooms
    "east_parade_bay1_upper_w1", "east_parade_bay4_upper_w0",                       # bedrooms 1 and 2
    "east_parade_bay0_upper_w0", "east_parade_bay1_upper_w0", "east_parade_bay2_upper_w1", "east_parade_bay4_upper_w1", "east_parade_bay5_upper_w1", "east_chandler_bay0_upper_w1",   # the landings
]

BRAND_BLOCKLIST = ["paragon", "dixons", "currys", "comet", "rumbelows", "vtech", "urban", "ray homes", "celine", "kentucky", "lorex", "ingrid", "radolier", "britannica", "hotpoint",
                   "hoover", "kenwood", "bush", "ferguson", "philips", "sony", "panasonic", "pye", "murphy", "ekco", "ever ready", "ikea", "habitat", "dulux", "crown paints",
                   "everest", "anglian", "marley", "rehau", "upvc ltd", "royal mail", "post office", "tesco", "boots", "woolworth", "marks", "sainsbury"]

# the bare bulb of a landing (TARGET-REVIEW narrow point 5): an absolute emission so that a lit landing reads as lit in the gate
LANDING_BULB = {
    "what": "a landing's bare 40 W bulb: PIC-02 gives its picture a mean luma of 40, which behind the glass reads dark (the card's emission is picture x 0.7 x room_glow_gain_night 0.4); the lit landing therefore takes an ABSOLUTE warm emission floor on its card",
    "disc_emission_linear": [8.0, 5.7, 2.75], "disc_note": "the glowing disc drawn in the picture (rooms.forms bare_bulb, d 0.06): HDR so that it clips to a warm white in the 8-bit picture",
    "card_emission_floor_linear": [0.28, 0.20, 0.096],
    "card_floor_note": "a lit landing's card never emits less than this (linear, the warm light (1.0, 0.714, 0.344) at luma 0.207: r > g > b, g/r 0.71, b/r 0.34); square on through the pane (two-face reflectance 0.082) the gate's pane median then reads 0.19 linear = sRGB 121, inside 100 to 140. Judgement: NIGHT-01's second form (pane median at least 4 times the dark windows' with r > g > b) is the acceptance, this is the starting value",
}
