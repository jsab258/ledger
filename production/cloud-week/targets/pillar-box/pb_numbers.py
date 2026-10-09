"""Quay Street pillar box: the numbers, each with its kind and source.

Every number the target uses is registered here once (id, value, unit, kind, source), and
make_target.py reads the values back from this registry, so target.json cannot disagree with it.

Kinds (the brief's, no more):
  Read       printed in the repository (the scene file, the earlier research, a sibling target) -- or the
             conversion of a printed figure
  Scaled     measured off a drawing: NONE here (no drawing reached)
  Photo      measured on a photograph: NONE here (no photograph of a pillar box was reached; see TARGET.md 2)
  Derived    computed from other numbers in this registry
  Judgement  the writer's choice; where it rests on the writer's general knowledge of the type and not on
             any source read in this session, `basis` says "Memory" (lowest weight: a guess to be corrected
             by the first dated photograph)

All lengths millimetres unless the unit says otherwise. z up from the footway surface at the box's axis.
"""

REG = {}


def reg(i, value, unit, kind, src, basis=None):
    assert i not in REG, i
    assert kind in ("Read", "Derived", "Judgement"), kind
    REG[i] = {"value": value, "unit": unit, "kind": kind, "source": src}
    if basis:
        REG[i]["basis"] = basis
    return value


SCENE = "production/specs/vignette-scene.json furniture E4_pillar_box (read 9 October 2026; also SCENE-SLOTS.md)"
RES = "production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 1 (read on the PC; photographs of survivors after 2000; no drawing)"
KERBS = "production/cloud-week/targets/kerbs-and-covers/target.json"
WEAR = "production/cloud-week/targets/wear/target.json"

# ---- Read: the scene's stand-in (a trade-standard guess, not a photograph) -----------------------------------
reg("scene_body_diameter", 597, "mm", "Read", SCENE + ": body_diameter_m 0.597")
reg("scene_body_height", 1372, "mm", "Read", SCENE + ": body_height_m 1.372 (the stand-in puts the 0.100 cap and 0.140 dome ON TOP of it: 1612 in all)")
reg("scene_cap_diameter", 660, "mm", "Read", SCENE + ": cap_diameter_m 0.660")
reg("scene_cap_height", 100, "mm", "Read", SCENE + ": cap_height_m 0.100")
reg("scene_dome_height", 140, "mm", "Read", SCENE + ": dome_height_m 0.140")
reg("scene_aperture_width", 320, "mm", "Read", SCENE + ": aperture_width_m 0.320")
reg("scene_aperture_height", 45, "mm", "Read", SCENE + ": aperture_height_m 0.045")
reg("scene_aperture_centre_z", 1150, "mm", "Read", SCENE + ": aperture_at_m 1.150 (StreetVignette.cs PillarBox: the box's centre at gy + 1.15)")
reg("scene_x", 27.0, "m", "Read", SCENE + ": x_m 27.0, side east")
reg("scene_setback", 0.60, "m", "Read", SCENE + ": setback_from_kerb_m 0.60; StreetVignette.cs Furniture(): z = FootwayFrontZ + setback, i.e. the box's AXIS stands 0.60 m behind the back of the kerb")
reg("scene_footway_width", 2000, "mm", "Read", "vignette-scene.json street.footway.width_m 2.0")
reg("scene_footway_crossfall", 0.025, "ratio", "Read", "vignette-scene.json street.footway.crossfall 0.025, falling toward the road")
reg("scene_lamp_column_x_east", 28.0, "m", "Derived", "vignette-scene.json lighting.column: first_offset 8.0, spacing 4.0 x 5.0 m alternating sides every 10 m: east at x = 8 and 28 (StreetVignette.cs Columns); setback 0.6, the same line as the box")
reg("scene_lantern_linear_srgb", [1.0, 0.7055, 0.0], "linear", "Read", "vignette-scene.json lighting.lantern.linear_srgb (589 nm, clipped and normalised)")

# ---- Read: the earlier research (listings and an untraced figure; all uncertain) -----------------------------
reg("research_width_untraced_typeA", 19.25, "in", "Read", RES + ": 'an untraced source gives a Type A as 5 ft 4 in tall and 1 ft 7 1/4 in (49 cm) wide' (UNVERIFIED)")
reg("research_width_c1955_listing", 19, "in", "Read", RES + ": 'body width 19 in (48 cm) on a c.1955 box' (a salvage dealer's listing)")
reg("research_width_narrow_listing", 15, "in", "Read", RES + ": '15 in (38 cm) on a Carron PB42' (the narrower Type B size)")
reg("research_total_casting", 73, "in", "Read", RES + ": 'the whole casting is 73 in (185 cm), of which 15-20 in is buried'")
reg("research_buried_min", 15, "in", "Read", RES + ": 15-20 in buried")
reg("research_buried_max", 20, "in", "Read", RES + ": 15-20 in buried")
reg("research_visible_range_cm", [135, 147], "cm", "Read", RES + ": 'about 135-147 cm above the pavement'")
reg("research_working_height", 1500, "mm", "Read", RES + ": 'working figures: about 150 cm above ground and 49 cm across' (the 150 lies above the research's own 135-147 range)")
reg("research_working_width", 490, "mm", "Read", RES + ": 49 cm across")
reg("research_base_height", 200, "mm", "Read", RES + ": 'Base: black, about 20 cm tall'")
reg("research_aperture", "a horizontal slot with a small hood just under the cap; a flush door with plate frame and keyhole; domed cap with an overhanging moulded rim a few centimetres proud of the body", "text", "Read", RES + " Modelling")

# ---- Read: sibling targets (the footway it stands on, the wear it takes) -------------------------------------
reg("kerb_top_above_channel", 115, "mm", "Read", KERBS + " frame/section: granite kerb top z = +115 above the channel setts")
reg("flag_level_above_channel", 110, "mm", "Read", KERBS + " frame: footway flags +110 at the kerb back (5 below the kerb top)")
reg("kerb_granite_top_width", 170, "mm", "Read", KERBS + " section 4.1: top width 170 (the scene's 125 is the concrete kerb)")
reg("wear_pillar_red_srgb", [150, 30, 32], "sRGB", "Read", WEAR + " surfaces.pillar_box_red [150,30,32] ('the furniture family's own colour wins')")
reg("wear_pillar_tone_mark", [124, 104, 92], "sRGB", "Read", WEAR + " iron_wear tone row for pillar_box_red: grey primer and rust showing through, 124/104/92, multiplier 1.0 (replacing)")
reg("wear_iron_black", [35, 35, 36], "sRGB", "Read", WEAR + " surfaces.iron_black [35,35,36]")
reg("wear_iron_share", [0.04, 0.08], "share", "Read", WEAR + " iron_wear density (the downpipe's: 4 to 8 % of the area lost to paint)")
reg("wear_patch_eqd", [20, 45, 110], "mm", "Read", WEAR + " iron_wear patch_eqd_mm p10/p50/p90")
reg("wear_lowest_share", 0.4, "share", "Read", WEAR + " iron_wear placement foot_lowest_0.3m 0.4")
reg("wear_edge_mm", 4, "mm", "Read", WEAR + " iron_wear edge_for_envelope_mm 4")
reg("wear_pipe_strip", 214, "mm", "Read", WEAR + " iron_wear: the pillar box takes the mask as a 0.214 m strip tiled round its girth, mirrored on alternate repeats")
reg("wear_splash_levels", [[240, 1.0], [330, 0.85], [450, 0.5], [610, 0.15], [750, 0.0]], "mm,level", "Read", WEAR + " wall_foot_splash levels (height, strength)")
reg("wear_rust_bleed_trickle", {"width_mm": [5, 10, 20], "length_m": [0.15, 0.35, 0.8], "drops_eqd_mm": [30, 90]}, "mm", "Read", WEAR + " rust_bleed geometry (p10/p50/p90; Photo M14 of a brick wall, not of iron)")
reg("wear_poster_paper_mark", [196, 186, 168], "sRGB", "Read", WEAR + " poster_remnant tone 'paper and paste'")
reg("wear_bird_mark", [226, 224, 214], "sRGB", "Read", WEAR + " bird_dropping tone on iron/stone")

# ---- The body: what the earlier research's figures give ------------------------------------------------------
BODY_D = reg("body_diameter", 489, "mm", "Derived",
             "19 1/4 in x 25.4 = 489 (the research's untraced Type A figure, 49 cm; the two listings 19 in = 483 and a Type A circumference of about 60 in (a search lead, 486) agree within 1 %)")
R_BODY = BODY_D / 2.0
H_TOTAL = reg("total_height", 1372, "mm", "Judgement",
              "the scene's 1.372 m READ AS THE WHOLE BOX ABOVE THE FOOTWAY (cap and dome inside it, not on top). It sits inside the research's 135-147 cm (73 in casting less 15-20 in buried); the scene's stand-in is 1612 mm and the research's 'working' 150 cm lies above its own range", basis="Memory/Read")
BURIED = reg("buried_depth", 482, "mm", "Derived", "73 in total casting (1854.2 mm) - 1372 mm visible = 482.2, i.e. 19 in (inside the research's 15-20 in)")
# foot (plinth)
R_FOOT = reg("foot_radius", 288, "mm", "Judgement", "the foot is wider than the body by 43.5 mm all round (diameter 576, 3.5 % under the scene's 597 body figure, which is therefore read as the foot: the widest thing at the pavement)", basis="Memory")
FOOT_BAND = reg("foot_band_height", 48, "mm", "Judgement", "plain vertical band of the foot, then a rounded top edge and a splay", basis="Memory")
FOOT_TOP_ROUND = reg("foot_top_round", 12, "mm", "Judgement", "quarter-round on the foot's top edge")
FOOT_SPLAY_TOP_R = reg("foot_splay_top_radius", 262, "mm", "Judgement", "end of the 45 degree splay, start of the cove")
FOOT_SPLAY_Z = reg("foot_splay_top_z", 72, "mm", "Judgement", "end of the splay")
COVE_TOP_Z = reg("foot_cove_top_z", 140, "mm", "Judgement", "the cove runs out into the plain body here")
# cap
CAP_SOFFIT_Z = reg("cap_soffit_z", 1215, "mm", "Judgement", "where the body starts to flare into the cap's under-moulding", basis="Memory")
R_CAP = reg("cap_radius", 268, "mm", "Judgement", "cap rim 23.5 mm proud of the body: diameter 536 (the scene's 660 would be 1.35 times the body; the research says the rim is a few centimetres proud)", basis="Memory")
CAP_COVE_H = reg("cap_cove_height", 13, "mm", "Judgement", "under-moulding (cove) height")
CAP_RIM_TOP_Z = reg("cap_rim_top_z", 1250, "mm", "Judgement", "top of the vertical rim")
CAP_BEAD_R = reg("cap_bead_radius", 12, "mm", "Judgement", "quarter-round bead above the rim")
CAP_SHOULDER_R = reg("cap_shoulder_radius", 250, "mm", "Judgement", "dome springs at this radius after a short neck")
DOME_BASE_Z = reg("dome_base_z", 1292, "mm", "Judgement", "top of the neck, base of the dome")
DOME_SAGITTA = reg("dome_sagitta", 80, "mm", "Judgement", "a shallow bowl: rise / diameter = 0.16 (the scene's 140 is 0.25: too steep)", basis="Memory")
# aperture
AP_W = reg("aperture_width", 320, "mm", "Read", "the scene's 0.320 kept (a letter slot about 12.6 in wide; no photograph to overturn it)")
AP_H = reg("aperture_height", 45, "mm", "Read", "the scene's 0.045 kept")
AP_Z = reg("aperture_centre_z", 1150, "mm", "Read", "the scene's 1.150 kept: 1127.5 to 1172.5, 42.5 below the cap's under-moulding")
AP_CORNER_R = reg("aperture_corner_radius", 5, "mm", "Judgement", "the slot's corner radius")
WALL = reg("wall_thickness", 12, "mm", "Judgement", "cast iron wall, for the section drawing and the slot's depth; the build may close the interior", basis="Memory")
HOOD_PROJ = reg("hood_projection", 30, "mm", "Judgement", "hood stands 30 proud of the body (r 274.5), about level with the cap rim (268)", basis="Memory")
HOOD_Z0 = reg("hood_z_bottom", 1172.5, "mm", "Derived", "= the slot's top edge: the hood's underside is flat on it")
HOOD_FRONT_TOP_Z = reg("hood_front_top_z", 1195, "mm", "Judgement", "top of the hood's vertical front")
HOOD_TOP_Z = reg("hood_top_z", 1205, "mm", "Judgement", "the hood's sloped top meets the body here, 10 below the cap's under-moulding")
HOOD_HALF_ANGLE = reg("hood_half_angle", 48, "deg", "Judgement", "the hood is a curved lip wrapped round the front, a little wider than the slot (slot half angle 40.9)")
SILL_PROJ = reg("sill_projection", 11.5, "mm", "Judgement", "the sill lip below the slot")
SILL_HALF_ANGLE = reg("sill_half_angle", 44, "deg", "Judgement", "")
SILL_Z0 = reg("sill_z_bottom", 1112, "mm", "Judgement", "lower edge of the sill's chamfer")
FLAP = reg("flap", {"width": 300, "height": 30, "thickness": 2, "tilt_deg": 15, "hinged": "top edge, inside the slot", "colour_srgb": [40, 40, 42]}, "mm", "Judgement", "the letter flap seen through the slot", basis="Memory")
# door
DOOR_HW = reg("door_half_width", 150, "mm", "Judgement", "door 300 wide in elevation (angular half-width 37 degrees)", basis="Memory")
DOOR_Z0 = reg("door_z_bottom", 280, "mm", "Judgement", "door's bottom edge: 80 above the black band's top (200)")
DOOR_Z1 = reg("door_z_top", 1040, "mm", "Judgement", "door's top edge: 72.5 under the slot's sill chamfer")
DOOR_PROUD = reg("door_proud", 4, "mm", "Judgement", "door face stands 4 proud of the body")
DOOR_GROOVE = reg("door_groove", {"width": 3, "depth": 3}, "mm", "Judgement", "the joint line round the door")
DOOR_CORNER = reg("door_corner_radius", 10, "mm", "Judgement", "")
HINGE = reg("hinge", {"count": 2, "x": -150, "z": [420, 900], "knuckle_diameter": 26, "length": 96, "pin_head_diameter": 18, "pin_head_height": 6, "side": "left as seen from the front"}, "mm", "Judgement", "two barrel hinges on the door's left edge", basis="Memory")
LOCK = reg("lock", {"x": 112, "z": 690, "escutcheon_diameter": 36, "proud": 3, "keyhole_w": 4, "keyhole_h": 12, "shutter_w": 22, "shutter_h": 10, "shutter_t": 2, "side": "right (opposite the hinges)"}, "mm", "Judgement", "keyhole escutcheon with a brass swivel shutter, no maker's mark", basis="Memory")
# panels
LETTER_PANEL = reg("lettering_panel", {"x0": -150, "x1": 150, "z0": 1062, "z1": 1102, "proud": 3, "corner_radius": 4, "surface": "body", "blank": True}, "mm", "Judgement",
                   "BLANK raised pad where a real box carries its operator lettering; the position is a guess (the order of lettering, cypher and plates on the real type is the first thing to read from a dated photograph)", basis="Memory")
CYPHER_PANEL = reg("cypher_panel", {"cx": 0, "cz": 960, "diameter": 110, "proud": 3, "surface": "door", "blank": True}, "mm", "Judgement",
                   "BLANK raised roundel where the royal cypher would be: canon owes the postal cypher", basis="Memory")
COLLECT_FRAME = reg("collection_plate_frame", {"cx": 0, "cz": 790, "outer_w": 210, "outer_h": 125, "bezel": 12, "bezel_proud_at_axis": 6, "plate_recess": 3, "form": "flat-faced boss: its face plane is tangent to the door at the axis plus 6, its sides run back to the cylinder"}, "mm", "Judgement",
                    "frame for the collection-times plate", basis="Memory")
ENAMEL_FRAME = reg("enamel_plate_frame", {"cx": 0, "cz": 590, "outer_w": 160, "outer_h": 100, "bezel": 10, "bezel_proud_at_axis": 6, "plate_recess": 3, "form": "flat-faced boss as the collection frame"}, "mm", "Judgement",
                   "frame for the small enamel instruction plate (left BLANK)", basis="Memory")
# paint
BLACK_TOP = reg("black_band_top", 200, "mm", "Read", "the research: 'Base: black, about 20 cm tall' (a search lead: a reclamation firm shows about 6 in = 152 of black when it sets a box)")
RED = reg("red_srgb", [150, 30, 32], "sRGB", "Read", "kept from the wear target's pillar_box_red; see TARGET.md 6 for why (value, saturation and the accent budget)")
BLACK = reg("black_srgb", [35, 35, 36], "sRGB", "Read", "the wear target's iron_black")
# footway
FOOTWAY_Z_AT_AXIS = reg("footway_at_axis_above_channel", 125, "mm", "Derived", "110 (flags at the kerb back) + 600 mm x 0.025 fall = 15 -> 125 above the channel top (the scene's footway falls toward the road)")
PLINTH_FILLET = reg("base_fillet", {"width": [15, 35], "height": 10, "colour_srgb": [56, 53, 50]}, "mm", "Judgement", "dark bitumen and mortar fillet where the cut paving meets the foot")
FOOT_TILT = reg("footway_fall_across_foot", 14.4, "mm", "Derived", "576 mm x 0.025: the footway differs by 14 mm across the foot; the box stands vertical, the fillet takes it up")
# wear numbers of this target
reg("wear_share_box", [0.03, 0.06], "share", "Judgement", "paint loss to primer and rust, of the body and foot area (door furniture and aperture excluded). The wear target's 0.04-0.08 is the downpipe's; a box in service is touched up, so the box takes the lower end (0.04 typical)")
reg("repeat_count", 8, "count", "Derived", "circumference 2 pi x 244.5 = 1536 mm; 1536 / 214 = 7.2 repeats: 7 is odd (a mirrored strip needs an even count to close at the seam), 8 repeats of 192 mm (the strip 10 % narrower) is the nearest")
