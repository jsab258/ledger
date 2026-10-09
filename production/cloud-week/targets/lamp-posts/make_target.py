#!/usr/bin/env python
"""Writes target.json (the lamp-post target's numbers for a script) from lamp_numbers.py and photo_measurements.json.

    /home/user/.bpyenv/bin/python make_target.py        (re-writes target.json, keeping the "self_check" block of the last run)
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lamp_numbers as LN  # noqa: E402

R = LN.REG
D = LN.derive()
ALL = dict(R)
ALL.update(D)
V = lambda k: ALL[k]["value"]  # noqa: E731

PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))

# ------------------------------------------------------------------------------------------------------------------------------------
# the lower column (shared by A, P; C and W1 have their own)
# ------------------------------------------------------------------------------------------------------------------------------------
SLEEVE_R = V("sleeve_od") / 2.0          # 61
SHAFT_R_LOW = V("shaft_od_at_cone") / 2.0  # 34
SHAFT_R_TOP = V("shaft_od_at_top") / 2.0   # 30
COLLAR_R = V("collar_od") / 2.0            # 33.5
Z_SLEEVE = V("sleeve_height")              # 978
Z_CONE = V("cone_top")                     # 1038
Z_RING = Z_CONE + V("weld_ring_height")    # 1044
Z_TOP = V("collar_top_z")                  # 4620
Z_COLLAR = Z_TOP - V("collar_height")      # 4560
HIDDEN = 150

outer_rz = [[0, -HIDDEN], [SLEEVE_R, -HIDDEN], [SLEEVE_R, Z_SLEEVE], [SHAFT_R_LOW, Z_CONE], [SHAFT_R_LOW + 1.5, Z_CONE], [SHAFT_R_LOW + 1.5, Z_RING],
            [SHAFT_R_LOW, Z_RING], [SHAFT_R_TOP, Z_COLLAR], [COLLAR_R, Z_COLLAR], [COLLAR_R, Z_TOP], [0, Z_TOP]]


def shaft_radius_at(z):
    """the outer radius of the lower column at height z (mm), from the profile above (linear between its points)"""
    pts = [(p[1], p[0]) for p in outer_rz[1:-1]]
    for (z0, r0), (z1, r1) in zip(pts, pts[1:]):
        if z0 <= z <= z1 and z1 > z0:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return None


# ------------------------------------------------------------------------------------------------------------------------------------
# the bracket: a stem, one bend, a raked arm to the lantern's rear boss (plane y-z, y toward the carriageway)
# ------------------------------------------------------------------------------------------------------------------------------------
R_BEND = V("bend_radius")
RAKE = V("rake_deg")
STEM_TOP = Z_TOP + V("stem_height_above_collar")          # 4700: where the bend begins
TURN = 90.0 - RAKE                                         # 50 degrees from vertical to 40 above horizontal
BEND_END_Y = R_BEND * (1 - math.cos(math.radians(TURN)))
BEND_END_Z = STEM_TOP + R_BEND * math.sin(math.radians(TURN))
ARM_END_Y = V("lantern_rear_end_y")                          # 225: the arm reaches the lantern's rear end
ARM_END_Z = BEND_END_Z + (ARM_END_Y - BEND_END_Y) * math.tan(math.radians(RAKE))
ARM_LEN = math.hypot(ARM_END_Y - BEND_END_Y, ARM_END_Z - BEND_END_Z)
centreline = [[0.0, float(z)] for z in range(int(Z_TOP - 60), int(STEM_TOP), 40)] + [[0.0, STEM_TOP]]
for i in range(1, 13):
    a = math.radians(TURN) * i / 12.0
    centreline.append([round(R_BEND * (1 - math.cos(a)), 3), round(STEM_TOP + R_BEND * math.sin(a), 3)])
_n = max(4, math.ceil(ARM_LEN / 35.0))
for i in range(1, _n + 1):
    centreline.append([round(BEND_END_Y + (ARM_END_Y - BEND_END_Y) * i / _n, 3), round(BEND_END_Z + (ARM_END_Z - BEND_END_Z) * i / _n, 3)])

# ------------------------------------------------------------------------------------------------------------------------------------
# the lantern L1 (frame: the column's, y toward the carriageway; the lantern's long axis lies along y)
# ------------------------------------------------------------------------------------------------------------------------------------
RIM_Z = V("canopy_rim_z")                    # 4925
LIP = V("canopy_lip_height")                 # 12
DOME_BASE_Z = RIM_Z + LIP                    # 4937
canopy_plan_half = [[225, 0], [230, 30], [245, 58], [270, 86], [300, 108], [340, 128], [400, 144], [450, 150], [520, 150], [600, 146], [670, 134], [725, 108], [760, 62], [775, 0]]
canopy_top_z = [[225, 4937], [260, 4962], [320, 4990], [400, 5000], [500, 4998], [600, 4985], [680, 4963], [735, 4945], [775, 4937]]
bowl_base_half = [[300, 0], [303, 22], [320, 52], [350, 70], [400, 80], [500, 82], [600, 80], [650, 70], [680, 52], [697, 22], [700, 0]]
bowl_section_y500 = [[82, 4800], [90, 4806], [100, 4815], [118, 4842], [130, 4872], [138, 4900], [142, 4925]]
bowl_long_rear_curve = [[233, 4925], [240, 4890], [262, 4850], [285, 4818], [300, 4800]]   # the rear end of the bowl in the long section; the front end is its mirror about y = 500


def interp(table, y):
    for (y0, v0), (y1, v1) in zip(table, table[1:]):
        if y0 <= y <= y1:
            return v0 + (v1 - v0) * (y - y0) / (y1 - y0) if y1 > y0 else v0
    return None


lantern = {
    "envelope": {"length_y": [225, 775], "width_x": [-150, 150], "height_z": [4800, 5000], "centre": [0, 500, 4900],
                 "note": "550 x 300 x 200, the scene's box, turned so that its long side lies ALONG THE ARM (y), not along the street: the photographs win (US01, seen from below, the arm enters the lantern's rear end and the lantern lies along the arm)"},
    "canopy": {"material": "painted aluminium", "shell_thickness": 2.5, "rim_z": RIM_Z, "lip_height": LIP, "dome_base_z": DOME_BASE_Z,
               "plan_half_width": canopy_plan_half, "top_z_along_y": canopy_top_z,
               "section": "at each y the dome is a half ellipse: z = dome_base_z + (top_z(y) - dome_base_z) x sqrt(1 - (x / w(y))^2), w(y) from plan_half_width and top_z(y) from top_z_along_y (both linear between their stations); the lip is the vertical band from rim_z to dome_base_z; the underside is offset 2.5 inward",
               "gear": "the control gear lives inside the canopy (no separate external box): the canopy's highest part, 4998 to 5000, is the gear tray over y 400 to 500",
               "underside": "white reflector (reflector_srgb) with a 40 x 120 lamp-holder pad at the rear (y 300 to 345)"},
    "bowl": {"material": "clear acrylic, yellowed", "shell_thickness": 3.0, "rim_z": RIM_Z, "rim_inset": V("bowl_rim_inset"), "base_z": 4800,
             "rim_plan": "canopy plan_half_width reduced by rim_inset at every station, between y 233 and 767",
             "base_plan_half_width": bowl_base_half, "section_y500_half_width_z": bowl_section_y500, "long_section_rear_curve_yz": bowl_long_rear_curve,
             "sides": "rise from the flat refractor base (400 x 164, corner radius 55) outward to the rim in the section's curve at every y; the rim has a 6 x 6 bead",
             "refractor": "fine prismatic grooves on the base's underside, 2 mm pitch across the lantern (x)",
             "loft": "ring(z): the closed outline whose half width at y is hw(y, z) = bw(y) + (rw(y) - bw(y)) x s(z), for y from y_rear(z) to 1000 - y_rear(z); bw(y) is base_plan_half_width (0 outside y 300 to 700), rw(y) is the canopy's plan half width minus rim_inset, s(z) = (section_y500 half width at z - 82) / (142 - 82), y_rear(z) is read off long_section_rear_curve_yz at z (its front end is its mirror about y = 500): at z 4800 the ring is the flat base (y 300 to 700), at z 4925 it is the rim (y 233 to 767)"},
    "lamp": {"what": "a 35 W low-pressure sodium lamp: one glass jacket, 54 across and 310 long, lying along y", "od": V("lamp_od"), "length": V("lamp_length"),
             "centre": [0, V("lamp_centre_y"), V("lamp_centre_z")], "holder": {"y": [300, 345], "x": [-30, 30], "z": [4852, 4892]}},
    "hinge": {"where": "rear of the bowl rim", "knuckles": 2, "x": [-60, 60], "y": 262, "size": [22, 22, 14], "z": RIM_Z},
    "catches": {"where": "the bowl's two long sides at the rim", "y": 650, "size_y_z_proud": [30, 14, 7], "x_abs": 136.0, "z": RIM_Z, "count": 2},
    "boss": {"od": V("boss_od"), "length": V("boss_length"), "axis_from": [0, ARM_END_Y, round(ARM_END_Z, 3)], "axis_deg_above_horizontal": RAKE,
             "grub_screws": {"count": 2, "azimuths_deg_about_axis": [90, 270], "head_od": 10, "proud": 3, "note": "M8 socket set screws, round-headed"}},
    "tilt_deg": 0,
}
# the boss lies inside the canopy's rear end: check numbers used by the self-check
boss_axis_z = ARM_END_Z

# ------------------------------------------------------------------------------------------------------------------------------------
# door, plate, screws
# ------------------------------------------------------------------------------------------------------------------------------------
door = {"on": "the sleeve", "facing": "-y (away from the carriageway, toward the building line)", "centre_azimuth_deg_from_plus_y": 180, "z": [400, 900], "arc_width": 100,
        "arc_deg": round(math.degrees(100 / SLEEVE_R), 1), "proud": 1.5, "joint_groove": {"width": 2.5, "depth": 2.0, "colour": "dark: black paint in the groove"},
        "screws": {"count": 2, "z": [425, 875], "head_od": 12, "proud": 2.0, "kind": "round-headed hex-socket captive screw"},
        "hinge": "concealed (no hinge shows)", "lock": "none visible: the door is held by its two screws", "lettering": "none: no maker's name, no plate on the door",
        "kind_of_source": "Judgement; the earlier research puts 'a door plate about 50 cm up'; US01's sleeve shows a rectangular door outline with its top edge at about 86 % of the sleeve's height (qualitative); a search lead (a modern catalogue, never a number) gives a 500 x 100 door opening 400 above the ground on a 5 m stepped steel column, which the sleeve's 978 height accommodates (door 400 to 900)"}
plate = {"on": "the shaft, the carriageway face (+y)", "z_centre": V("bge_plate_z"), "size": [90, 45], "arc_deg": round(math.degrees(90 / 33.0), 1), "thickness": 1.2, "proud": 1.4,
         "fixing": "two domed rivets, 5 across, at 8 from each end, on the centreline",
         "text": {"template": "LC n", "n": [1, 2, 3, 4], "font": "plain upright sans (any OFL grotesque), black on white, letters 24 high",
                  "note": "generic: 'LC' for lamp column and the column's number in the street (placement table); no authority's name, no crest, no maker"}}
collar_screws = {"z": Z_COLLAR + 30, "azimuths_deg_from_plus_y": [45, 135], "head_od": 10, "proud": 3.0, "kind": "M8 socket set screw, flush-ish round head"}

# ------------------------------------------------------------------------------------------------------------------------------------
# variants
# ------------------------------------------------------------------------------------------------------------------------------------
C_FOOT, C_TOP, C_CHAMFER = 220, 125, 15
variant_C = {
    "id": "C", "name": "concrete shaft, steel bent-arm bracket, same lantern", "build": False,
    "why": "the earlier research (street-clutter-1990, section 3) names precast concrete columns with sodium lanterns as the commonest of the period; NO photograph of one was reached; every number is Judgement or the research's",
    "frame": "as A: axis at the footway, z up, +y to the carriageway",
    "shaft": {"section": "square, arrises chamfered", "side_at_z0": C_FOOT, "side_at_top": C_TOP, "top_z": Z_TOP, "chamfer": C_CHAMFER, "hidden_root": HIDDEN,
              "taper": "linear in plan, none in the arrises' size",
              "kind": "Judgement: the research's '20 to 25 cm at the foot' (Read) and 'square or tapered in section' (uncertain)"},
    "door": {"recess": {"width": 120, "height": 330, "depth": 14, "z": [450, 780]}, "plate": {"width": 132, "height": 342, "thickness": 3, "proud": 3, "screws": 2, "lettering": "none (no maker's name)"},
             "face": "-y"},
    "top": "flat, a 60 mm collar-less seat; the bracket tube (OD 48) enters the top face at the centre (top entry) and the same bend and rake as A follow",
    "bracket_stem_od": 48,
    "paint": "none: bare concrete (concrete_srgb) with algae and lime marks",
    "plate_number": "as A: 90 x 45 white plate at z 2160 on +y",
}
variant_P = {
    "id": "P", "name": "post-top pod on the same lower column (the form BGE shows)", "build": False,
    "why": "BGE's column is exactly this: a black steel stepped tube with a small flat dish of a lantern on its top; the scene's lamps are bracket lamps, so P is not placed",
    "shaft_top_z": 4300, "pod": {"diameter": 420, "centre_z": 4375, "kind": "Photo diameter (417 +-30); the height 150 is Judgement (the thickness cannot be read from below)",
                                 "profile_rz": [[0, 4300], [30, 4300], [120, 4312], [180, 4340], [210, 4378], [200, 4418], [150, 4445], [60, 4455], [0, 4455]]},
    "pod_colours": {"shell": "dark grey-blue (60, 62, 78) as the sky tints it in BGE", "underside": "pale grey (190, 188, 184)"},
}
variant_W1 = {
    "id": "W1", "name": "wall bracket for the same lantern (optional, not placed)", "build": False,
    "why": "the street's old quarter may have a lantern on a wall; no photograph of a council wall bracket was reached (the two wall lanterns reached are a bespoke college lantern at Cambridge and a 2019 estate bulkhead, neither a street fitting); all Judgement",
    "plate": {"width": 150, "height": 220, "thickness": 8, "bolts": {"count": 4, "pitch": [100, 160], "head": "domed nut 24 across"}, "z_centre": 4300},
    "arm": {"od": 42, "from": [0, 4350], "rake_deg": 10, "to_y": 225, "strut": {"od": 25, "from": [0, 4130], "to_arm_at_y": 140}},
    "lantern": "L1 unchanged, its rear boss at y 225 from the wall face; the arm rises 10 degrees from z 4350 to z 4390 at y 225, so the lantern's top stands at z %d (the whole lantern %d lower than on A)" % (round(5000 + (4350 + 225 * math.tan(math.radians(10))) - ARM_END_Z), round(ARM_END_Z - (4350 + 225 * math.tan(math.radians(10))))),
    "placement": "none in today's scene; if wanted, a plain gable end, never a shopfront",
    "seen_instead": "US02 (urban_street_02, 2019): a black-backed opal half-egg bulkhead 235 tall and 210 wide (measured against the wall's 75 mm brick courses, +-10 %) on a 1970s-80s brick block, its cable in surface conduit above it: an estate fitting, not a street lantern, not copied",
}

# ------------------------------------------------------------------------------------------------------------------------------------
# placement
# ------------------------------------------------------------------------------------------------------------------------------------
xs = V("scene_column_x")
zs = V("scene_column_z")
columns = []
for i, (x, z) in enumerate(zip(xs, zs)):
    side = "east" if z > 0 else "west"
    columns.append({"id": f"LC {i + 1}", "x_m": x, "side": side, "scene_z_m": z, "corrected_z_m": round(math.copysign(3.0 + 0.170 + 0.6, z), 3),
                    "arm_toward": "the carriageway (scene -z for the east side, +z for the west side)", "door_faces": "away from the carriageway",
                    "plate_text": f"LC {i + 1}", "wear_seed": 11 + 7 * i, "dent": (i == 1)})

# ------------------------------------------------------------------------------------------------------------------------------------
# the checks (what unit 3.8's automatic check must pass)
# ------------------------------------------------------------------------------------------------------------------------------------
def chk(name, applies, measure, expected, tol, kind):
    return {"name": name, "applies_to": applies, "measure": measure, "expected": expected, "tolerance": tol, "kind": kind}


checks = [
    chk("pivot_and_datum", "whole piece", "the pivot (origin) lies on the shaft's axis at the footway surface (z = 0) and the lowest vertex lies between z = -160 and z = -140", {"origin_xy_mm": [0, 0], "lowest_z_range": [-160, -140]}, 3, "Read (brief: pivot at the base's centre on the ground); the hidden skirt is 150"),
    chk("lantern_top_z", "A, C", "max z of the lantern's mesh above the footway, mm", 5000, 10, "Read (scene: mounting height 5.0 m to the lantern's top)"),
    chk("lantern_bounding_box", "A, C", "extent of the lantern mesh (canopy, bowl, catches, hinge; not the boss) along y, x, z, mm", {"y": 550, "x": 300, "z": 200}, 8, "Read (scene 0.55 x 0.30 x 0.20), turned so the long side lies along y"),
    chk("lantern_centre", "A, C", "the lantern's bounding-box centre (x, y, z), mm", [0, 500, 4900], 12, "Read (scene outreach 0.5 to the centre; top 5000, 200 tall)"),
    chk("lantern_axis", "A, C", "angle between the lantern's long axis and the arm's direction in plan (+y), degrees", 0.0, 3.0, "Photo (US01: the lantern lies along its arm)"),
    chk("lantern_tilt", "A, C", "angle between the bowl's base plane and the horizontal, degrees", 0.0, 1.5, "Judgement (level, as the scene)"),
    chk("lantern_canopy_rim_z", "A, C", "z of the canopy's lower edge, mm", V("canopy_rim_z"), 6, "Judgement"),
    chk("lantern_dome_height", "A, C", "max z of the canopy minus the z of its lip's top, at y = 500, mm", 63, 6, "Judgement"),
    chk("lantern_plan_silhouette", "A, C", "largest nearest distance (both ways) between the lantern's plan outline at z = 4925 and the polygon in target.json geometry.A.lantern.plan, mm", 0.0, 6.0, "Derived from the plan stations"),
    chk("lantern_section_silhouette", "A, C", "the same, for the cross-section at y = 500 and the long section at x = 0, against target_drawing.py's polygons", 0.0, 6.0, "Derived"),
    chk("bowl_base", "A, C", "the bowl's flat base: z 4800, length (y) and width (x), mm", {"z": 4800, "length": 400, "width": 164}, 8, "Judgement"),
    chk("lamp_in_bowl", "A, C", "the lamp's axis: parallel to y, centre (x, y, z), diameter and length, mm", {"centre": [0, 500, 4872], "od": 54, "length": 310}, 6, "Judgement (a 35 W SOX lamp)"),
    chk("lamp_inside_bowl_and_canopy", "A, C", "the lamp's whole volume lies inside the bowl's and canopy's inner shell: no vertex of the lamp outside the lantern's envelope", True, 0, "Derived"),
    chk("glow_surface", "A, C", "the emissive surface is the lamp's jacket (full strength) and the bowl (translucent, 45 % of the jacket's brightness), nothing else emits: no emissive vertex outside them", {"emissive_parts": ["lamp", "bowl"]}, 0, "Judgement; Photo (US01 lit: the bowl glows orange round a brighter core)"),
    chk("glow_colour_bowl", "A, C", "the bowl's emissive colour, sRGB 8-bit", V("glow_bowl_srgb"), 12, "Derived (the night note's lamp (1, 0.25, 0) gamma-encoded); Photo US01 251/152/14"),
    chk("glow_colour_lamp", "A, C", "the lamp jacket's emissive colour, sRGB 8-bit", V("glow_lamp_srgb"), 14, "Judgement"),
    chk("arm_stem_od", "A", "outer diameter of the bracket's stem, mm", V("stem_od"), 4, "Photo ratio (US01 0.47 to 0.67 of the shaft's top) + Judgement"),
    chk("arm_rake", "A, C", "angle of the straight arm above horizontal, degrees", RAKE, 6.0, "Photo (US01: 41.7 degrees in the picture; true 36 to 44)"),
    chk("arm_bend_radius", "A, C", "centreline radius of the bend, mm", R_BEND, 40, "Photo-scaled by reach (US01 435 / 1117 x 225 = 88) + Judgement"),
    chk("arm_reaches_boss", "A, C", "the straight arm's end point (y, z), mm", [ARM_END_Y, round(ARM_END_Z, 1)], 12, "Derived"),
    chk("arm_continuity", "A, C", "no gap and no kink: the arm's centreline sampled every 10 mm is continuous (largest step under 12 mm; largest turn between consecutive samples under 8 degrees)", True, 0, "Derived"),
    chk("arm_direction", "A, C", "the arm's plan direction against the carriageway's normal, degrees", 0.0, 3.0, "Read (scene: the lantern 0.5 out toward the road)"),
    chk("sleeve_od", "A, P", "outer diameter of the sleeve at z = 300 and z = 800, mm", V("sleeve_od"), 9, "Photo (BGE 123.6 +-9; the scene's 114 is inside)"),
    chk("sleeve_height", "A, P", "z where the sleeve's straight side ends, mm", V("sleeve_height"), 15, "Photo (BGE 978 +-10)"),
    chk("cone", "A, P", "outer diameter at z = 1010 (about half way up the cone), mm", round(2 * shaft_radius_at(1010), 1), 8, "Derived from the profile"),
    chk("shaft_od_low", "A, P", "outer diameter of the shaft at z = 1200, mm", round(2 * shaft_radius_at(1200), 1), 6, "Photo (BGE 66 to 69)"),
    chk("shaft_od_mid", "A, P", "outer diameter of the shaft at z = 2500, mm", round(2 * shaft_radius_at(2500), 1), 6, "Derived (linear between the two photographed heights)"),
    chk("shaft_od_high", "A, P", "outer diameter of the shaft at z = 3900, mm", round(2 * shaft_radius_at(3900), 1), 6, "Photo (BGE 61)"),
    chk("shaft_taper_monotone", "A, P", "outer diameter never increases between z = 1044 and z = 4560 (steps of 100 mm)", True, 0, "Derived"),
    chk("collar", "A", "collar outer diameter and z range, mm", {"od": V("collar_od"), "z": [Z_COLLAR, Z_TOP]}, 4, "Judgement"),
    chk("lower_profile_silhouette", "A, P", "largest nearest distance (both ways) between the built lower column's outline in the y-z plane and geometry.A.lower.outer_rz mirrored, mm", 0.0, 4.0, "Derived; the profile is Photo (BGE)"),
    chk("door", "A", "door arc width, height, bottom z, proud, mm", {"arc_width": 100, "height": 500, "z_bottom": 400, "proud": 1.5}, 10, "Judgement (a lead: a modern 5 m stepped column has a 500 x 100 door 400 above the ground; US01: the door outline's top at about 86 % of the sleeve; the research: a door plate about 50 cm up)"),
    chk("door_face", "A", "azimuth of the door's centre against +y, degrees", 180, 12, "Judgement"),
    chk("door_groove", "A", "joint groove width and depth round the door, mm", {"width": 2.5, "depth": 2.0}, 1.0, "Judgement"),
    chk("number_plate", "A, C", "plate size (arc x height), centre z, face (+y), mm", {"size": [90, 45], "z": 2160, "face": "+y"}, 8, "Photo (BGE: a reference plate at z 2115 to 2200)"),
    chk("plate_text_only_lc_n", "A, C", "the only characters on any surface of the piece are 'LC' and one digit 1 to 4, on the plate", True, 0, "Judgement: no maker, no council, no crown"),
    chk("no_maker_marks", "all", "no text, logo or relief lettering on any mesh or texture except the plate's; in particular none of the makers' names in the earlier research, none on the door, the lantern or the base", True, 0, "Rulings 8 October and brief"),
    chk("collar_screws", "A", "two set screws at azimuth 45 and 135 degrees from +y, heads 10 across, proud 3, mm", {"count": 2, "head_od": 10, "proud": 3}, 1.5, "Judgement"),
    chk("boss", "A, C", "the lantern's rear boss: outer diameter, length, axis rake, mm and degrees", {"od": 60, "length": 55, "rake_deg": RAKE}, 5, "Judgement"),
    chk("paint_black", "A, P", "mean albedo of the sleeve's undamaged paint, sRGB 8-bit", V("paint_black_srgb"), 12, "Photo (BGE 31/31/33)"),
    chk("paint_gloss", "A, P", "roughness of the undamaged paint on the sleeve (0 to 1); the upper shaft is 0.15 higher", {"sleeve": 0.42, "upper_shaft_plus": 0.15}, 0.10, "Judgement (the recipe's 0.42; BGE shows gloss worn to semi-gloss)"),
    chk("splash_band", "A, P", "the splash band's height above the footway where the albedo returns to the paint, mm", 250, 60, "Photo (BGE: z 0 to 250 is 49/46/42)"),
    chk("canopy_colour", "A, C", "mean albedo of the canopy's undamaged paint, sRGB 8-bit", V("canopy_srgb"), 18, "Judgement"),
    chk("placement_xs", "street", "the four columns' x, m", V("scene_column_x"), 0.05, "Read (pieces file and code)"),
    chk("placement_sides", "street", "the four columns' sides, east first", ["east", "west", "east", "west"], 0, "Read"),
    chk("placement_setback", "street", "the axis's distance behind the kerb's BACK face, mm", 600, 40, "Read (scene 0.6)"),
    chk("placement_vertical", "street", "the axis's lean from vertical, degrees (the footway falls 1 in 40 toward the road; the column stands plumb)", 0.0, 0.3, "Derived"),
    chk("light_position", "A, C", "the point light's position (x, y, z), mm, and the count per column", {"pos": [0, 500, 4850], "count_per_column": 1}, 12, "Read (scene: 0.05 m below the centre)"),
    chk("light_pool", "A, C", "the pool spot: lumens, inner and outer cone, degrees, aimed straight down, shadows on", {"lm": 350, "inner": 15, "outer": 55}, 0, "Read (night note step 4)"),
    chk("light_skirt", "A, C", "the skirt spot: lumens, inner and outer cone, degrees, straight down, no shadows", {"lm": 800, "inner": 45, "outer": 80}, 0, "Read (night note step 4)"),
    chk("light_glow", "A, C", "the all-round glow: lumens, no shadows", {"lm": 40}, 0, "Read (night note, DECISIONS 7 October)"),
    chk("light_colour", "A, C", "the lights' colour, linear sRGB (the night note's lamp, one number to be tried at (1, 0.40, 0.03))", V("night_current_lamp_linear"), 0.03, "Read (night note); NOT the scene's (1, 0.7055, 0)"),
    chk("triangles", "A", "triangle count of one column with its lantern at LOD0", [3000, 12000], 0, "Judgement (mid-poly, a bevel on every edge: the asset plan; four columns are about 4 % of a frame)"),
    chk("bevels", "A, C", "every hard edge has a bevel; radii in `bevels`", True, 0, "Judgement (the asset plan's method)"),
]

bevels = [{"edge": "sleeve top lip (z 978)", "radius": 1.5}, {"edge": "collar top and bottom edges", "radius": 1.5}, {"edge": "door perimeter (outer)", "radius": 1.0},
          {"edge": "plate perimeter", "radius": 0.8}, {"edge": "canopy lip's lower edge", "radius": 1.5}, {"edge": "bowl rim bead", "radius": 3.0},
          {"edge": "boss end", "radius": 1.5}, {"edge": "catches", "radius": 2.0}, {"edge": "sleeve bottom (z -150, hidden)", "radius": 2.0}]

# ------------------------------------------------------------------------------------------------------------------------------------
# photographs: frames of the reduced previews
# ------------------------------------------------------------------------------------------------------------------------------------
BGE_STRIP_X0, BGE_STRIP_X1, BGE_MM = -120, 180, 1.2
bge_strips = [{"z0": z0, "z1": z0 + 1200} for z0 in (0, 1200, 2400, 3600)]
photo_frames = {
    "BGE_STRIPS": {"file": "bge-bethnal-green-column-strips.jpg", "pano": "bethnal_green_entrance", "yaw_deg": 138.5, "d_m": 2.73, "camera_height_m": 1.02, "mm_per_px": BGE_MM,
                   "x0_mm": BGE_STRIP_X0, "x1_mm": BGE_STRIP_X1, "strips": bge_strips, "gap_px": 10, "size_px": [1030, 1000],
                   "layout": "four strips side by side, left to right z 0-1200, 1200-2400, 2400-3600, 3600-4800; each 250 px wide, 1000 px tall; row 0 of a strip is its z1; masked grey: the three signs (z 2185-2845 and z 3000-3720)",
                   "note": "this is the 'main photograph' of the drawing check: the lower column on it is the target's own profile"},
    "BGE_POD": {"file": "bge-bethnal-green-column-pod.jpg", "x0_mm": -300, "x1_mm": 300, "z0_mm": 4000, "z1_mm": 4900, "mm_per_px": 1.5, "size_px": [400, 600]},
    "US01_ARM": {"file": "us01-bethnal-green-bent-arm-elevation.jpg", "pano": "urban_street_01", "yaw_deg": -15.7, "d_m": 8.8, "camera_height_m": 1.16, "mm_per_px": 3.0,
                 "x0_mm": -1800, "x1_mm": 400, "z0_mm": 8800, "z1_mm": 11400, "size_px": [733, 867]},
    "US01_LIT": {"file": "us01-bethnal-green-lit-lantern-from-below.jpg", "view": "rectilinear, yaw -23.5, pitch 49, 5 degrees wide, 800 x 800"},
    "US01_SLEEVE": {"file": "us01-bethnal-green-sleeve-and-shoulder.jpg", "pano": "urban_street_01", "yaw_deg": -15.7, "d_m": 8.8, "camera_height_m": 1.16, "x0_mm": -170, "x1_mm": 170, "z0_mm": 0, "z1_mm": 1800, "mm_per_px": 2.0, "size_px": [170, 900]},
}

T = {
    "family": "lamp-posts",
    "title": "Quay Street's lamp posts: the target (cloud week 42, 9 October 2026)",
    "written": "2026-10-09",
    "units": {"length": "millimetres in this file unless a key says metres (_m)", "glb": "metres, z up, scale 1",
              "frame": "origin on the column's vertical axis at the footway surface; +y toward the carriageway (the lantern side); x along the street; z up; for the west side's columns the whole piece is turned 180 degrees about z so that +y still points at the road",
              "pivot": "the axis at z = 0 (the footway surface); the sleeve runs 150 mm below it, hidden"},
    "summary_line": "",  # filled below
    "no_period_photograph": True,
    "decision_type": {
        "main": "A: a painted-steel stepped column (124 mm black sleeve 978 high, a cone, a 68-to-60 mm tapering shaft, a collar), a plain bent-arm bracket (a vertical stem, one tight bend, a straight arm raked 15 degrees) and a boat-shaped aluminium canopy over a deep yellowed clear bowl, the lamp's long axis along the arm; 4 columns at x 8, 18, 28, 38, alternate sides",
        "alternatives": ["C: precast concrete shaft with the same bracket and lantern (the earlier research's type; no photograph; build only if ruled)", "P: post-top dish on the same lower column (what BGE shows; not placed)", "W1: a wall bracket for the same lantern (optional; not placed)"],
        "why_A_is_main": "it keeps what the scene, the recipe (accepted work) and the 2019 photographs (steel tubes, the only column photographs reached) share, corrects what the photographs show otherwise (sleeve, taper, bent arm, lantern along the arm), and leaves the concrete variant as a ruled-in alternative: the earlier research's concrete is not shown by any photograph reached",
        "who_decides": "the builder builds A; the director or Jafar may rule C in (a different shaft, door plate and paint; the same bracket, lantern, light and places)"},
    "what_the_sheets_show": {
        "approved_sheet": "production/reference/hook-sheet.png (pass 4, approved 22 September 2026; the reduced copy production/previews/hook-sheet-2026-10-05.jpg) shows NO lighting column and NO bracket lamp: read at full size on 9 October (the only vertical on its skyline is a mast on the far hill); production/reference/retired-sheet-inheritance.md row 4 and game-design/research/GOVERNS.md say the same",
        "retired_sheet": "the 'slender dark column with a small flat canopy' of the brief is the RETIRED Codex sheet's (production/art/atlas-01/concepts/hook.png on a branch that is not in this checkout); the in-house retired poster production/reference/hook-sheet-2026-09-09-retired.png shows a black post-top globe lantern 60 px tall on the quay and two box wall lanterns, each under 4 px wide: not evidence (hook-sheet-audit.md: anything under 4 px is noise)",
        "so": "no number here is read off a Hook sheet; the sheet governs mood (wet, dark, overcast), and the night frame's pools, not the column"},
    "frame_numbers": {"scene": {"column_x_m": V("scene_column_x"), "sides": ["east", "west", "east", "west"], "column_z_m": V("scene_column_z"), "setback_from_kerb_back_mm": 600,
                                "note": "the code steps x by half the spacing (10 m), alternating sides: four columns, 20 m apart on each side; SCENE-SLOTS.md's 'every 20 m, alternate sides' means 20 m on one side; the posters target's 'x 8, 28, 48' (SF4) misreads it"}},
    "photo_frames": photo_frames,
    "calibration": {
        "BGE": {"pano": "bethnal_green_entrance", "date_taken": "2019-08-18", "camera_height_m": 1.02, "error_m": 0.07, "d_axis_m": 2.73, "bearing_deg": 138.5,
                "how": "the camera height is the bollards' target's (brick-course horizon method on the planter wall of the same block paving: 0.96 by its writer, 1.03 to 1.04 by its reviewer; 1.02 +-0.07 adopted); the distance from the foot's depression angle (row 2524 of 4096, -20.9 degrees): 1.02 / tan(20.9) = 2.665 m to the sleeve's front, plus its radius 0.062 = 2.73 m; the base then appears at z = -23 mm in the elevation, as the geometry says it should",
                "independent_hint": "the sleeve at 123.6 +-9 contains the standard 114.3 mm tube; if it is that tube the camera was 0.95 m (this writer's own horizon fit: 0.96), every BGE length 7 % smaller; the stated +-7 % covers it"},
        "US01": {"pano": "urban_street_01", "date_taken": "2019-08-18", "camera_height_m": 1.16, "error_m": 0.07, "d_axis_m": 8.8, "d_error_m": 0.6, "bearing_deg": -15.7,
                 "how": "camera height above the footway: the garden wall 1.23 and the gate pier 1.15 to 1.16 (the bollards' target; both include the 0.07 m step to the bed); the distance: the gate pier's foot at -7.9 degrees gives 8.4 m, the column's lowest visible sleeve point at -7.15 degrees gives 9.2 m (its foot is hidden by a car); only RATIOS are used"}},
    "photo_measurements": PM,
    "photographs_win": [
        {"id": "PW1", "what": "the sleeve and the shaft", "scene": "a base 200 across and 300 high and ONE 114 mm shaft to the top", "photograph": "BGE: a 124 mm black sleeve 978 mm high, a 60 mm cone with a ring line, a shaft 68 mm at the cone tapering to 61 at 3.9 m; US01 the same form (sleeve 2.05 x the shaft)", "chose": "the photograph's, with the scene's 114 left inside the sleeve's +-9", "kind": "Photo"},
        {"id": "PW2", "what": "the bracket", "scene": "a swan neck of three short cylinders on a quarter circle, rising over the lantern and dropping into it (the code's comment: 'a straight bracket reads as a modern column')", "photograph": "US01: a vertical stem, one tight bend, a straight raked arm entering the lantern's rear end; R07 reads 'plain bent-arm lighting' (production/reference/photographs.md)", "chose": "the bent arm", "kind": "Photo + Read"},
        {"id": "PW3", "what": "the lantern's long axis", "scene": "0.55 along the street", "photograph": "US01 seen from below: the arm enters the lantern's rear end and the lantern lies along it", "chose": "along the arm (y); the box's size is kept", "kind": "Photo"},
        {"id": "PW4", "what": "the lantern's form", "scene": "a box", "photograph": "US01 lit lantern: a boat-shaped canopy over a bowl that glows orange round a brighter core; the research: 'a boat-shaped canopy 60 to 70 cm long over a deep clear trough-shaped bowl'", "chose": "canopy over bowl, the lamp visible inside", "kind": "Photo + Read"},
        {"id": "PW5", "what": "the lantern's colour", "scene": "linear (1.0, 0.7055, 0.0), gamma (255, 219, 0): a yellow", "photograph": "US01 lit: median 251/152/14 (orange); the night note's lamp (1, 0.25, 0); derived 589 nm: (1, 0.2195, 0) linear = 255/129/0", "chose": "(255, 137, 0) for the bowl (the night note's lamp gamma-encoded); the scene's xy is 585 nm, not 589, and its normalisation skipped the division in green", "kind": "Photo + Derived"},
        {"id": "PW6", "what": "the column's concrete or steel", "scene": "steel (surface 'metal')", "photograph": "none of the period; the 2019 photographs show steel; the earlier research says concrete", "chose": "steel main, concrete as variant C: unsettled", "kind": "Judgement"},
        {"id": "PW7", "what": "the count and places", "scene": "SCENE-SLOTS.md 'every 20 m, alternate sides, first at 8 m'", "photograph": "the code and pieces file: x 8, 18, 28, 38, east, west, east, west", "chose": "the code's four", "kind": "Read"},
    ],
    "variants": {"A": {"id": "A", "name": "steel bent-arm column (main)", "build": True, "count_in_street": 4}, "C": variant_C, "P": variant_P, "W1": variant_W1},
    "geometry": {
        "A": {
            "lower": {"outer_rz": outer_rz, "hidden_skirt": HIDDEN,
                      "root": {"meets_ground": "the sleeve runs straight into the footway: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar; no base plate, no collar, no bolts show; the skirt continues 150 mm below the footway (hidden); the footway falls 1 in 40 toward the road, which is 3 mm across the sleeve, and the column stands plumb",
                               "kind": "Photo (BGE: the block paving is cut round the sleeve with a dark joint, no plate) + Judgement (the figures)"},
                      "note": "(radius, z) in mm of the outer surface, revolved about the axis; the sleeve to z 978, a cone to 1038, a 1.5 proud ring 1038 to 1044, the shaft's straight taper from r 34 to r 30 at z 4560, the collar r 33.5 from 4560 to 4620",
                      "weld_seam": "a longitudinal weld line 1.5 wide and 0.5 proud on the shaft, on the -y face (BGE shows a faint vertical line near the shaft's edge: qualitative)",
                      "sleeve_joint": "a 1 mm groove round the sleeve at z 978 where the cone cap is welded on"},
            "door": door, "plate": plate, "collar_screws": collar_screws,
            "bracket": {"tube_od_stem": V("stem_od"), "centreline_yz": centreline, "stem_from_z": Z_TOP - 60, "stem_to_z": STEM_TOP, "bend_radius": R_BEND, "bend_turn_deg": TURN,
                        "rake_deg": RAKE, "arm_start": [round(BEND_END_Y, 3), round(BEND_END_Z, 3)], "arm_end": [ARM_END_Y, round(ARM_END_Z, 3)], "arm_length": round(ARM_LEN, 2),
                        "note": "the stem's lowest 60 mm are inside the collar; the arm's end lies inside the lantern's rear boss"},
            "lantern": lantern,
        },
    },
    "light": {
        "lamp": {"what": "35 W low-pressure sodium (SOX), 589 nm", "lumens": V("lamp_lumens_35w_sox"), "kind": "Read (the night note, a maker's datasheet by search summary)"},
        "position_mm": [0, V("lamp_centre_y"), V("light_z")], "placement_rule": "Read: one point light 0.05 m below the centre of the emissive piece (the lantern's centre z 4900)",
        "current_game": {"pool_spot": {"lm": 500, "inner_deg": 22, "outer_deg": 46, "shadows": True, "cd": D["cd_current_pool"]["value"], "lux_straight_down_at_4p78m": D["lux_current_pool"]["value"]},
                         "glow": {"lm": 40, "shadows": False}, "range_m": V("scene_lantern_range"), "colour_linear": V("night_current_lamp_linear"), "kind": "Read (the night note, DECISIONS 8 October)"},
        "proposed_by_night_note": {"pool_spot": {"lm": 350, "inner_deg": 15, "outer_deg": 55, "shadows": True, "cd": D["cd_proposed_pool"]["value"]},
                                    "skirt_spot": {"lm": 800, "inner_deg": 45, "outer_deg": 80, "shadows": False, "source_radius_mm": [50, 100], "cd": D["cd_skirt"]["value"]},
                                    "glow": {"lm": 40, "shadows": False}, "total_lm": D["proposed_total_lumens"]["value"], "share_of_lamp_lumens": D["proposed_share_of_lamp"]["value"],
                                    "peak_lux_straight_down": D["lux_proposed_peak"]["value"], "colour_try_linear": V("night_try_lamp_linear"),
                                    "kind": "Read (night note section 4 steps 4 and 5; the numbers are the note's INTENT, to be tried, not measured)"},
        "colour": {"scene_file": {"linear": V("scene_lantern_linear_srgb"), "gamma": V("scene_lantern_gamma_srgb"), "xy": V("scene_lantern_xy"), "verdict": "wrong twice: its xy is the colour of about 585 nm, and its normalisation divided red by the peak but left green and blue undivided"},
                   "derived_589nm": {"xy": D["derived_xy_d_lines"]["value"], "linear": D["derived_589_linear"]["value"], "gamma_8bit": D["derived_589_gamma_8bit"]["value"]},
                   "night_note_lamp_linear": V("night_current_lamp_linear"), "evening_note": "(0.569, 0.430), about sRGB (255, 140, 0), linear about (1, 0.25, 0)",
                   "photo_lit_lantern_median_srgb": V("us01_lit_median_srgb"), "glow_bowl_srgb": V("glow_bowl_srgb"), "glow_lamp_srgb": V("glow_lamp_srgb"),
                   "note": "an RGB renderer cannot reproduce the colour loss (evening note section 3); the lamp's own light is one orange"},
        "warm_up": "a freshly lit SOX lamp glows dim red-pink for a few minutes before turning yellow-orange (evening note section 1); an optional start-up ramp, not required",
        "glow_surface": {"emissive_parts": ["lamp jacket (cylinder 54 x 310 at (0, 500, 4872))", "the bowl (translucent, 0.45 of the jacket's brightness)"], "not_emissive": ["canopy", "arm", "column", "boss", "catches", "hinge"],
                     "lit_srgb": {"lamp": V("glow_lamp_srgb"), "bowl": V("glow_bowl_srgb")}, "unlit": "both read pale and clear by day (materials.lamp_glass, materials.bowl)"},
    "lit_vs_unlit": {"unlit": "bowl clear-yellowed (bowl_unlit_srgb) with the lamp's dark jacket and the white reflector seen through it; canopy grey", "lit": "lamp jacket and bowl emissive; the canopy and the column stay unlit paint; the road and flags below carry the orange"},
    },
    "materials": {
        "paint_black": {"srgb": V("paint_black_srgb"), "name": "lamp-post black, gloss worn to semi-gloss", "roughness_new": 0.42, "roughness_sleeve": 0.42, "roughness_upper_shaft": 0.57, "roughness_words": "semi-gloss, the gloss worn (the upper shaft chalky and duller)", "metal": 0.0, "kind": "Photo colour; roughness Judgement (the recipe's 0.42)"},
        "splash": {"srgb": V("splash_srgb"), "name": "road film over the black, z 0 to 250", "roughness": 0.80, "roughness_words": "matt, dirty", "kind": "Photo"},
        "primer": {"srgb": V("primer_srgb"), "name": "grey primer in chips", "roughness": 0.85, "roughness_words": "matt", "metal": 0.0},
        "bare_steel_rust": {"srgb": V("rust_srgb"), "name": "rust brown", "roughness": 0.90, "roughness_words": "rough, matt", "metal": 0.0},
        "canopy": {"srgb": V("canopy_srgb"), "name": "weathered painted aluminium, mid grey", "roughness": 0.55, "roughness_words": "satin, dirty", "metal": 0.0, "kind": "Judgement"},
        "bowl": {"srgb_unlit": V("bowl_unlit_srgb"), "name": "yellowed clear acrylic", "roughness": 0.15, "roughness_words": "glossy, slightly hazed", "transmission": 0.85, "ior": 1.49, "kind": "Judgement"},
        "reflector": {"srgb": V("reflector_srgb"), "name": "white-painted reflector inside the canopy", "roughness": 0.35, "roughness_words": "satin white", "metal": 0.0},
        "lamp_glass": {"srgb_unlit": [200, 196, 180], "emissive_srgb_lit": V("glow_lamp_srgb"), "name": "the lamp's glass jacket, pale when cold, glowing when lit", "roughness": 0.10, "roughness_words": "glossy", "metal": 0.0},
        "bowl_emissive_lit": {"srgb": V("glow_bowl_srgb"), "relative_to_lamp": 0.45, "name": "the bowl lit: sodium orange", "roughness": 0.15, "roughness_words": "glossy", "metal": 0.0},
        "plate": {"srgb_white": V("plate_white_srgb"), "srgb_letters": V("plate_black_srgb"), "name": "aged white enamel number plate", "roughness": 0.30, "roughness_words": "semi-gloss enamel", "metal": 0.0},
        "concrete_C": {"srgb": V("concrete_srgb"), "name": "weathered grey precast concrete (variant C)", "roughness": 0.90, "roughness_words": "rough matt", "metal": 0.0},
    },
    "wear": {
        "state": "a tired council column, twenty years since it was last painted (a port town's wet air): black gone to semi-gloss, chipped where knocked, a splash band, rust at fixings",
        "agrees_with": "the wear target (production/cloud-week/targets/wear/TARGET.md: 'lamp-column bases' in the foot-splash feature list; 'street lamp tops' as perches)",
        "features": [
            {"id": "splash_band", "where": "the sleeve, z 0 to 250, all round (1.0 on the carriageway face, 0.6 elsewhere), top edge soft over 60", "colour": V("splash_srgb"), "kind": "Photo (BGE)"},
            {"id": "chips", "where": "the sleeve, carriageway face, z 150 to 900: 12 to 20 chips of 2 to 10 mm showing primer, 20 % with a rust speck; plus 5 to 8 chips of 4 to 15 mm on the sleeve's top lip and the cone", "colour": V("primer_srgb"), "kind": "Photo (US01: pale patches at the shoulder) + Judgement"},
            {"id": "scratches", "where": "the sleeve's carriageway face, z 380 to 430: 6 to 10 hairlines of 30 to 120 mm in light grey, no letters", "colour": [120, 118, 115], "kind": "Photo (BGE)"},
            {"id": "rust_streaks", "where": "under each collar set screw (two, 80 to 200 long, 3 to 6 wide, strength 0.6); from the door's two lower corners (two, 40 to 120); under the boss's two grub screws (two, 40 to 100)", "colour": V("rust_srgb"), "kind": "Judgement"},
            {"id": "dent", "where": "LC 2 only (x 18, west): the sleeve's carriageway face at z 480 +-30, an oval 45 wide x 70 tall, 3 deep, paint cracked at its centre with a rust speck", "kind": "Judgement (a vehicle's knock)"},
            {"id": "sticker_remnants", "where": "z 1450 +-60: a torn white sticker 40 x 25 and a smear of adhesive 15 x 60 on LC 1 and LC 3; two cable-tie stubs at z 1700 on LC 3", "colour": [200, 198, 190], "kind": "Judgement; the posters target (SF4) places its own bills and stickers on these shafts"},
            {"id": "upper_shaft_dulling", "where": "z above 3000: roughness +0.15, a chalky bloom (albedo +6)", "kind": "Judgement"},
            {"id": "canopy_streaks", "where": "8 to 12 vertical grime streaks from the canopy lip down the bowl, black (40, 38, 36) at 0.35", "kind": "Judgement"},
            {"id": "bowl_yellowing", "where": "the whole bowl, tint to bowl_unlit_srgb; 12 to 25 dark specks 1 to 3 mm inside it (dead insects)", "kind": "Judgement"},
            {"id": "bird_marks", "where": "the canopy's top, 2 to 3 patches of 20 to 60 mm, white-grey (205, 205, 190)", "kind": "Judgement; the wear target lists lamp tops as perches"},
        ],
        "not_present": ["graffiti lettering", "posters (the posters target's)", "reflective bands", "yellow or white bands", "a council name", "a maker's plate"],
    },
    "placement": {"columns": columns, "rule": "the axis 600 mm behind the kerb's back face; the scene's kerb top is 125 wide so z = 3.725; the corrected granite kerb top is 170 so the same rule gives 3.77: the rule governs, within the 40 mm tolerance; the footway falls 1 in 40 to the road and the column stands plumb with its skirt hidden",
                  "arm": "the arm points at the carriageway, square to the kerb", "door": "away from the carriageway", "plate": "on the carriageway face",
                  "wear_seed": "one seed per column in the table; the dent on LC 2 only"},
    "bevels": bevels,
    "triangle_budget": {"lod0": [3000, 12000], "kind": "Judgement"},
    "checks": checks,
    "numbers": ALL,
    "number_kinds": {},
}
kinds = {}
for k, v in ALL.items():
    kinds[v["kind"]] = kinds.get(v["kind"], 0) + 1
T["number_kinds"] = {"registry": "lamp_numbers.py REG plus derive(), copied whole into `numbers`", "counts": kinds}
T["summary_line"] = (
    "Quay Street's four lamp posts (x 8, 18, 28, 38, alternate sides) are painted-steel stepped columns of the kind the 2019 photographs show: a black sleeve 124 mm across and 978 high "
    "with a 60 mm cone and a ring line, a shaft tapering from 68 to 60 mm to a collar at 4.6 m, a plain bent-arm bracket (a 42 mm stem, one 90 mm bend, a straight arm raked 40 degrees) "
    "entering the rear boss of a boat-shaped aluminium canopy (550 x 300 x 200, its top at 5000, centred 500 out) over a yellowed clear bowl with a 54 x 310 sodium lamp inside it, "
    "the lantern's long side along the arm (the scene had it along the street), a flush door 100 x 500 at z 400, a 90 x 45 reference plate 'LC n' and no maker's mark; the lit lantern is orange "
    "(255, 137, 0) with a yellower lamp, the scene's (255, 219, 0) being the colour of 585 nm, not 589; the approved Hook sheet shows no column at all, and no reachable photograph is of 1990, so every "
    "length from the photographs is +-7 % and the choice of steel over the earlier research's concrete is Judgement (concrete is written out as variant C).")
T["leads"] = [
    {"text": "the SOX 35 W lamp is listed as 311 mm long and 52 mm across by a maker's datasheet and 310 x 54 by a catalogue table; 4,550 lm, 1,700 to 1,800 K", "via": "WebSearch summary, a lamp maker's datasheet and a trade catalogue table", "effect": "the lamp's 54 x 310 sits inside both; not changed"},
    {"text": "a modern 5 m stepped root-mounted steel column is listed with a 76 mm shaft, a 140 mm base, a 500 x 100 door 400 above the ground, a 150 x 75 cable slot, an 800 mm planting depth and a bitumen-coated root; its standard (the 1978 BS 5649 series, current to 2006) was not reached", "via": "WebSearch summary, three makers' catalogues (modern)", "effect": "the door is 100 x 500 at 400 (a width of 100 and a base zone to 900 agree with the sleeve's 978 and US01's door outline); the photographed sleeve 124 and shaft 68 to 60 are smaller than that catalogue's 140 and 76 (BGE's is a post-top column) and are kept; a bracket column's top may be 76"},
    {"text": "enthusiasts' pages describe 1960s to 1970s 5 m precast concrete columns carrying 35 W SOX lanterns on 'angular top-entry brackets', a maker's mark cast into the inspection door, and two 5 m tubular steel columns with 'angular' brackets with a vertical and a horizontal section, the lantern steeply tilted; install dates not stated", "via": "WebSearch summary of streetlightonline.co.uk pages (unreached)", "effect": "both types existed with the same lantern (A and C stand); a 5 m bracket may be more horizontal than US01's 40 degree arm; a real door might carry a maker's mark: ours is blank by rule"},
    {"text": "no source for a bracket's upsweep angle was found (the results were Australian and modern)", "via": "WebSearch summary", "effect": "the rake rests on US01's photograph alone"},
]
T["unreached"] = [
    {"what": "Wikipedia, Wikimedia Commons, Geograph, Flickr, archive.org, HathiTrust, the National Archives, Historic England, legislation.gov.uk, the street-lighting enthusiasts' sites the earlier research cites (the ones with the lantern and column galleries), the lantern and column makers' catalogues", "result": "000 or 403 at the proxy on 9 October 2026 (curl, 20 s)", "used": "nothing"},
]
T["to_read_when_the_network_opens"] = [
    "dated photographs, 1975 to 2000, of provincial British streets with precast concrete and tubular steel lighting columns and sodium lanterns on brackets, with a person or a kerb in frame for scale: the column's shape, the base (sleeve or concrete foot), the door, the bracket's rake and bend, the lantern's canopy and bowl, their paint (Geograph and Wikimedia Commons, CC BY or CC BY-SA, by date taken)",
    "the 1989 code for minor roads (BS 5489-3, current from 31 August 1989 to August 1992) for the column heights and spacing the street would have used",
    "the standard tube sizes of tubular steel columns (BS 1308 / BS 5649 families) and the maker-neutral root-section proportions of a 5 m stepped column",
    "a SOX 35 W lamp's datasheet: jacket diameter and length, lumens, warm-up curve",
    "the Middlesbrough Council, Tyne and Wear Archives and North Tyneside albums on Flickr that the earlier research lists (street scenes, for the lamps in the background; licences to be read on each page)",
    "the earlier research's Geograph 1485521 (a 1950s concrete column), read at its page for the licence and date",
]
T["could_not_settle"] = [
    "whether 1990's minor street in a northern port town had precast concrete or painted tubular steel columns: no 1990 photograph was reached; steel is the main variant because the only column photographs reached (2019, London) are steel and the scene and recipe assume it; the earlier research says concrete (variant C is written out)",
    "every BGE and US01 length is +-7 % in absolute size (camera height 1.02 +-0.07 m, 1.16 +-0.07 m); if the BGE sleeve is the standard 114.3 mm tube, all BGE lengths are 7 % smaller",
    "the bracket's rake (40 degrees is the 11 m column's, from its apparent 41.7 degrees and a nearly side-on lantern; a 5 m column's own rake is not photographed and this writer recalls 5 to 15 for standard raked brackets, no source found, and a search lead says 5 m brackets had a vertical and a horizontal section) and the bend's radius (scaled by the reach)",
    "the lantern's real length (the research estimates 600 to 700; the scene's 550 is kept) and its canopy and bowl proportions: read from one photograph from below and from the earlier research's words",
    "the door's real size and place on the steel sleeve (only a faint outline on US01)",
    "the 35 W SOX lamp's physical size: 54 x 310 is a catalogue table's figure by search lead (a maker's datasheet lead says 52 x 311); no datasheet was reached",
    "the shaft's top diameter on a BRACKET column: 60 is a post-top column's (BGE); a bracket column of this height may be 76 at the top (a modern catalogue's), the collar then 83 and the stem 48",
    "the real light: the night note's numbers are its own intent, not measured in the game; whether the orange (255, 137, 0) reads right in the game's camera is for a fresh reviewer to judge against photographs from the PC",
    "no photograph of a council wall bracket lantern was reached: W1 is entirely Judgement",
]
T["handover"] = {
    "for_scene_file": "furniture E1 and E2: replace the base 0.2 x 0.3, the 0.114 shaft, the three-cylinder swan neck and the box lantern by the kit piece A at the same four places (x 8 E, 18 W, 28 E, 38 W; axis 0.6 m behind the kerb's back); the lantern's top stays at 5.0 and its centre 0.5 out; its long side now lies along the arm",
    "for_the_night_scene": "the point light and the two spots at (0, 500, 4850) in the piece's frame; colour (1, 0.25, 0) linear, not the scene file's (1, 0.7055, 0); the lantern's lamp and bowl are the emissive parts; the scene file's lantern colour needs correcting (a ruling, so asked first)",
    "for_the_wear_target": "the lamp-column base foot-splash is the splash_band here (z 0 to 250); the wear target's iron_wear tone row applies to the chips",
    "for_the_posters_target": "its SF4 puts bills on the shafts at x 8, 28, 48: the street has columns at 8, 18, 28, 38; the shaft is 61 to 68 across at the bill's height, not 114 (so 'the middle 0.17 m of an A3 shows face-on' becomes the middle 0.09 m)",
    "pivot": "the axis at the footway surface; z up; scale 1; one mesh for the column and one for the lantern (the lantern's emissive parts as separate material slots)",
}
T["self_check"] = {}
# keep the last self-check block
old = os.path.join(HERE, "target.json")
if os.path.exists(old):
    try:
        T["self_check"] = json.load(open(old)).get("self_check", {})
    except Exception:
        pass
json.dump(T, open(old, "w"), indent=1)
print("wrote target.json", len(json.dumps(T)), "bytes;", len(ALL), "numbers;", len(checks), "checks")
print("arm end", ARM_END_Y, round(ARM_END_Z, 2), "bend end", round(BEND_END_Y, 2), round(BEND_END_Z, 2), "arm length", round(ARM_LEN, 1))
