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
# the lower column of variant A (painted steel; the alternative since try 2) and the shared bracket geometry
# ------------------------------------------------------------------------------------------------------------------------------------
SLEEVE_R = V("sleeve_od") / 2.0          # 62
SHAFT_R_LOW = V("shaft_od_at_cone") / 2.0  # 34
SHAFT_R_TOP = V("shaft_od_at_top") / 2.0   # 30 at z 4560 (the taper line's own end, hidden in the socket)
SOCKET_R = V("socket_od") / 2.0            # 32
Z_SLEEVE = V("sleeve_height")              # 978
Z_CONE = V("cone_top")                     # 1038
Z_RING = Z_CONE + V("weld_ring_height")    # 1044
Z_TOP = V("socket_top_z")                  # 4620
Z_SOCKET = V("socket_bottom_z")            # 4370
Z_LINE_END = 4560
TOP_CH = V("socket_top_chamfer")           # 3
HIDDEN = 150
R_AT_SOCKET = round(SHAFT_R_LOW + (SHAFT_R_TOP - SHAFT_R_LOW) * (Z_SOCKET - Z_RING) / (Z_LINE_END - Z_RING), 3)   # the same straight taper line, to the socket's foot

outer_rz = [[0, -HIDDEN], [SLEEVE_R, -HIDDEN], [SLEEVE_R, Z_SLEEVE], [SHAFT_R_LOW, Z_CONE], [SHAFT_R_LOW + 1.5, Z_CONE], [SHAFT_R_LOW + 1.5, Z_RING],
            [SHAFT_R_LOW, Z_RING], [R_AT_SOCKET, Z_SOCKET], [SOCKET_R, Z_SOCKET], [SOCKET_R, Z_TOP - TOP_CH], [SOCKET_R - TOP_CH, Z_TOP], [0, Z_TOP]]


def shaft_radius_at(z):
    """the outer radius of the lower column at height z (mm), from the profile above (linear between its points)"""
    pts = [(p[1], p[0]) for p in outer_rz[1:-1]]
    for (z0, r0), (z1, r1) in zip(pts, pts[1:]):
        if z0 <= z <= z1 and z1 > z0:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return None


# ------------------------------------------------------------------------------------------------------------------------------------
# the bracket (both variants): a vertical stem, ONE 90 degree bend of centreline radius 130, a straight LEVEL arm to the lantern's rear boss
# (plane y-z, y toward the carriageway); review faults 1 and 3
# ------------------------------------------------------------------------------------------------------------------------------------
R_BEND = V("bend_radius")                      # 130
RAKE = V("rake_deg")                           # 0
TURN = V("bend_turn_deg")                      # 90
STEM_TOP = V("stem_top_z")                     # 4800.8
BEND_END_Y = R_BEND * (1 - math.cos(math.radians(TURN)))      # 130
BEND_END_Z = STEM_TOP + R_BEND * math.sin(math.radians(TURN))  # 4930.8
ARM_END_Y = V("bracket_reach_to_spigot")        # 430
ARM_END_Z = BEND_END_Z                          # level: the same z
ARM_LEN = math.hypot(ARM_END_Y - BEND_END_Y, ARM_END_Z - BEND_END_Z)   # 300


def make_centreline(z_from):
    cl = [[0.0, float(z)] for z in range(int(z_from), int(STEM_TOP), 40)] + [[0.0, STEM_TOP]]
    for i in range(1, 13):
        a = math.radians(TURN) * i / 12.0
        cl.append([round(R_BEND * (1 - math.cos(a)), 3), round(STEM_TOP + R_BEND * math.sin(a), 3)])
    n = max(4, math.ceil(ARM_LEN / 35.0))
    for i in range(1, n + 1):
        cl.append([round(BEND_END_Y + (ARM_END_Y - BEND_END_Y) * i / n, 3), round(BEND_END_Z + (ARM_END_Z - BEND_END_Z) * i / n, 3)])
    return cl


centreline = make_centreline(Z_TOP - 60)          # A: from inside the socket (z 4560)
centreline_C = make_centreline(V("c_top_z") - 60)  # C: from 60 inside the concrete's top (z 4560)

# ------------------------------------------------------------------------------------------------------------------------------------
# the lantern L1 (frame: the column's, y toward the carriageway; the lantern's long axis lies along y)
# ------------------------------------------------------------------------------------------------------------------------------------
RIM_Z = V("canopy_rim_z")                    # 4925
LIP = V("canopy_lip_height")                 # 12
DOME_BASE_Z = RIM_Z + LIP                    # 4937
DY = V("lantern_dy")                         # 205: review fault 3 moved every y station out by 205
YC = V("lantern_centre_outreach")            # 755
Y_REAR, Y_FRONT = V("lantern_rear_end_y"), V("lantern_front_end_y")   # 430, 980


# second review, narrow point 1: every y station of try 2 becomes 430 + (y - 430) x 13/11 (the lantern 650 long, the boss still at y 430 to 485)
canopy_plan_half = [[430, 0], [435.9, 30], [453.6, 58], [483.2, 86], [518.6, 108], [565.9, 128], [636.8, 144], [695.9, 150], [778.6, 150], [873.2, 146], [955.9, 134], [1020.9, 108], [1062.3, 62], [1080, 0]]
canopy_top_z = [[430, 4937], [471.4, 4962], [542.3, 4990], [636.8, 5000], [755, 4998], [873.2, 4985], [967.7, 4963], [1032.7, 4945], [1080, 4937]]
bowl_base_half = [[518.6, 0], [522.2, 22], [542.3, 52], [577.7, 70], [636.8, 80], [755, 82], [873.2, 80], [932.3, 70], [967.7, 52], [987.8, 22], [991.4, 0]]
bowl_section_at_centre = [[82, 4800], [90, 4806], [100, 4815], [118, 4842], [130, 4872], [138, 4900], [142, 4925]]   # (half width, z) at the lantern's centre y
# second review, narrow point 2: the bowl's rear end now stands clear of the boss (the boss hangs 24 below the rim, z 4925, out to y 485), so the rim starts at y 488; the front curve is written out
bowl_long_rear_curve = [[488, 4925], [492, 4890], [500, 4850], [510, 4818], [518.6, 4800]]
bowl_long_front_curve = [[991.4, 4800], [1009.1, 4818], [1036.3, 4850], [1062.3, 4890], [1070.5, 4925]]


def interp(table, y):
    for (y0, v0), (y1, v1) in zip(table, table[1:]):
        if y0 <= y <= y1:
            return v0 + (v1 - v0) * (y - y0) / (y1 - y0) if y1 > y0 else v0
    return None


lantern = {
    "envelope": {"length_y": [Y_REAR, Y_FRONT], "width_x": [-150, 150], "height_z": [4800, 5000], "centre": [0, YC, 4900],
                 "note": "650 x 300 x 200 (the scene's 550 x 300 x 200 box lengthened by the second review, narrow point 1), turned so that its long side lies ALONG THE ARM (y), not along the street: the photographs win (US01, seen from below, the arm enters the lantern's rear end and the lantern lies along the arm). Since try 2 it stands 430 out at its rear (the research's 406 to 457 reach to the spigot) and 755 out at its centre, its front end 1080: the scene's 0.5 was a trade-standard guess"},
    "canopy": {"material": "painted aluminium", "shell_thickness": 2.5, "rim_z": RIM_Z, "lip_height": LIP, "dome_base_z": DOME_BASE_Z,
               "plan_half_width": canopy_plan_half, "top_z_along_y": canopy_top_z,
               "section": "at each y the dome is a half ellipse: z = dome_base_z + (top_z(y) - dome_base_z) x sqrt(1 - (x / w(y))^2), w(y) from plan_half_width and top_z(y) from top_z_along_y (both linear between their stations); the lip is the vertical band from rim_z to dome_base_z; the underside is offset 2.5 inward",
               "gear": "the control gear lives inside the canopy (no separate external box): the canopy's highest part, 4998 to 5000, is the gear tray over y 640 to 755",
               "underside": "white reflector (reflector_srgb) with a 45 x 60 lamp-holder pad at the rear (y 555 to 600); a flat cast soffit in the canopy's material closes the underside at z 4925 from y 430 to 488, and the boss's lower 24 mm hang below it (second review, narrow point 2)"},
    "bowl": {"material": "clear acrylic, yellowed", "shell_thickness": 3.0, "rim_z": RIM_Z, "rim_inset": V("bowl_rim_inset"), "base_z": 4800,
             "rim_plan": "canopy plan_half_width reduced by rim_inset at every station, between y 488 and 1070.5",
             "base_plan_half_width": bowl_base_half, "section_at_centre_half_width_z": bowl_section_at_centre, "long_section_rear_curve_yz": bowl_long_rear_curve, "long_section_front_curve_yz": bowl_long_front_curve,
             "sides": "rise from the flat refractor base (473 x 164, corner radius 55) outward to the rim in the section's curve at every y; the rim has a 6 x 6 bead",
             "refractor": "fine prismatic grooves on the base's underside, 2 mm pitch across the lantern (x)",
             "loft": "ring(z): the closed outline whose half width at y is hw(y, z) = bw(y) + (rw(y) - bw(y)) x s(z), for y from y_rear(z) to y_front(z); bw(y) is base_plan_half_width (0 outside y 518.6 to 991.4), rw(y) is the canopy's plan half width minus rim_inset, s(z) = (section_at_centre half width at z - 82) / (142 - 82), y_rear(z) is read off long_section_rear_curve_yz at z and y_front(z) off long_section_front_curve_yz at z (second review, narrow point 2: the front curve is written out, no longer a mirror): at z 4800 the ring is the flat base (y 518.6 to 991.4), at z 4925 it is the rim (y 488 to 1070.5)"},
    "lamp": {"what": "a 35 W low-pressure sodium lamp: one glass jacket, 54 across and 310 long, lying along y, with the arc tube inside it", "od": V("lamp_od"), "length": V("lamp_length"),
             "centre": [0, V("lamp_centre_y"), V("lamp_centre_z")], "holder": {"y": [555, 600], "x": [-30, 30], "z": [4852, 4892]},
             "arc_tube": {"what": "review point 3: a glowing U-shaped tube inside the jacket: two legs of 16 OD, centres at x +-11, z 4872, from y 605 (rear ends at the holder) forward, joined at the front by a half-torus of centreline radius 11; the whole tube spans y 605 to 895 (legs straight to y 876, the half-torus's outer surface reaching 895)",
                          "leg_od": 16, "leg_x": [-11, 11], "z": 4872, "y": [605, 895], "legs_straight_to_y": 876, "bend_centreline_radius": 11, "bend_at_front": True},
             "emissive": {"arc_tube": "full strength (the reference 1.0): " + str(round(V("emissive_jacket_cd_m2") / V("emissive_jacket_over_tube"), -2)) + " cd/m2 in the units below",
                          "jacket": "0.3 of the tube: about " + str(V("emissive_jacket_cd_m2")) + " cd/m2 (4,550 lm over its 0.0526 m2 surface)",
                          "bowl": "about " + str(V("emissive_bowl_cd_m2")) + " cd/m2 (80 % of the flux through about 0.21 m2 of bowl, Lambertian)",
                          "colour": "all three the one orange (255, 137, 0): a sodium lamp's own light is one orange; the yellow core of the photograph is the camera's clipping and is left to the grade",
                          "or": "both follow VignetteShot.cpp's kLampEmissiveUnitless = 1.0 times the lantern colour in linear (1, 0.25, 0) until the night audit puts the glow in units"}},
    "hinge": {"where": "rear of the bowl rim", "knuckles": 2, "x": [-60, 60], "y": 497, "size": [22, 22, 14], "z": RIM_Z},
    "catches": {"where": "the bowl's two long sides at the rim", "y": 932.3, "size_y_z_proud": [30, 14, 7], "x_abs": 136.0, "z": RIM_Z, "count": 2},
    "boss": {"od": V("boss_od"), "length": V("boss_length"), "axis_from": [0, ARM_END_Y, round(ARM_END_Z, 3)], "axis_deg_above_horizontal": RAKE,
             "top_above_rear_crown_mm": round(ARM_END_Z + V("boss_od") / 2 - DOME_BASE_Z, 1),
             "grub_screws": {"count": 2, "azimuths_deg_about_axis": [90, 270], "head_od": 10, "proud": 3, "note": "M8 socket set screws, round-headed"},
             "note": "horizontal, along +y from (0, 430, 4930.8) forward 55, coaxial with the lantern's long axis on its centreline; its top (4960.8) stands 24 above the canopy's rear crown (4937) and its front end (y 485) lies inside the dome (the dome is 4967 there), so nothing pokes through the dome; its lower 24 mm hang below the rim, under the flat soffit that closes the canopy's underside from y 430 to 488 (the bowl starts at y 488: it does not cut the boss)"},
    "tilt_deg": 0,
}
# the boss lies inside the canopy's rear end: check numbers used by the self-check
boss_axis_z = ARM_END_Z

# ------------------------------------------------------------------------------------------------------------------------------------
# variant A's door, plate and socket; variant C's shaft, cap, door and plate
# ------------------------------------------------------------------------------------------------------------------------------------
door = {"on": "the sleeve", "facing": "-y (away from the carriageway, toward the building line)", "centre_azimuth_deg_from_plus_y": 180, "z": [400, 900], "arc_width": 100,
        "arc_deg": round(math.degrees(100 / SLEEVE_R), 1), "proud": 1.5, "corner_radius": 15,
        "joint_groove": {"width": 2.5, "depth": 2.0, "colour": "dark: black paint in the groove", "corner_radius": 15},
        "screws": {"count": 2, "z": [425, 875], "head_od": 12, "proud": 2.0, "kind": "round-headed hex-socket captive screw"},
        "hinge": "concealed (no hinge shows)", "lock": "none visible: the door is held by its two screws", "lettering": "none: no maker's name, no plate on the door",
        "corner_note": "review point 2: US01's flush door has rounded top corners: all four corners of the door and of its joint groove are rounded to radius 15 (Photo, US01, about 2 px at 7 mm)",
        "kind_of_source": "Judgement; the earlier research puts 'a door plate about 50 cm up'; US01's sleeve shows a rectangular door outline with its top edge at about 86 % of the sleeve's height (qualitative); a search lead (a modern catalogue, never a number) gives a 500 x 100 door opening 400 above the ground on a 5 m stepped steel column, which the sleeve's 978 height accommodates (door 400 to 900)"}
plate = {"on": "the shaft, the carriageway face (+y)", "z_centre": V("bge_plate_z"), "size": [90, 45], "arc_deg": round(math.degrees(90 / 33.0), 1), "thickness": 1.2, "proud": 1.4,
         "fixing": "two domed rivets, 5 across, at 8 from each end, on the centreline",
         "text": {"template": "LC n", "n": [1, 2, 3, 4], "font": "plain upright sans (any OFL grotesque), black on white, letters 24 high",
                  "note": "generic: 'LC' for lamp column and the column's number in the street (placement table); no authority's name, no crest, no maker"}}
socket = {"od": V("socket_od"), "z": [Z_SOCKET, Z_TOP], "length": Z_TOP - Z_SOCKET, "proud_of_shaft_at_foot_mm": round(SOCKET_R - R_AT_SOCKET, 1), "top_chamfer": TOP_CH,
          "foot_seam": "a 1 mm seam groove round its foot at z 4370 (review point 1: a seam at its foot)",
          "set_screws": {"count": 2, "on": "-y", "azimuth_deg_from_plus_y": 180, "z": list(V("socket_screw_z")), "head_od": 10, "proud": 3.0, "kind": "M8 socket set screw, round head; one above the other on the -y face"},
          "note": "review point 1: US01's shaft top is the bracket's socket sleeve (about 450 mm on that 11 m column), no step a 7 mm pixel can see, a flat top with a small chamfer into the stem, a seam at its foot and two set screws one above the other on one side"}

C_FOOT, C_TOP, C_CH, C_TOPCH = V("c_foot_side"), V("c_top_side"), V("c_arris_chamfer"), V("c_top_face_chamfer")
C_ZTOP = V("c_top_z")                          # 4985.8: the shaft's top face, one face with the arm's top (second review, R1)
C_ZREF = V("c_taper_ref_z")                    # 4620: where the shaft is 125 across
C_TOP_AT_ARM = V("c_top_side_at_arm_top")      # 117.5: the same straight taper carried up to the arm's top
ARM_SQ, ARM_CH, ARM_END = V("c_arm_square"), V("c_arm_chamfer"), V("c_arm_end_y")
SPIGOT_OD, SPIGOT_Y, SPIGOT_EXPOSED = V("c_spigot_od"), V("c_spigot_y"), V("c_spigot_exposed_y")


def c_side(z):
    return C_FOOT + (C_TOP - C_FOOT) * z / C_ZREF


c_door = {"recess": dict(V("c_door_recess")), "plate": {"width": 132, "height": 342, "thickness": 3, "proud": 3, "z": [444, 786], "screws": {"count": 2, "head_od": 10, "z": [444 + 25, 786 - 25], "from_ends": 25, "kind": "round-headed hex-socket screw, blank"},
                                                          "corner_radius": 10, "lettering": "none (no maker's name, no cast mark)"},
          "face": "-y", "centre_azimuth_deg_from_plus_y": 180, "corner_note": "the recess is square-cornered with 6 mm radii, the steel plate's corners are rounded to 10 (Judgement)"}
variant_C = {
    "id": "C", "name": "precast concrete column with a cast concrete arm, the lantern (the main build since try 2; the arm since the second review)", "build": True, "count_in_street": 4,
    "why": "review fault 2: the earlier research (street-clutter-1990, section 3) names precast concrete columns with sodium lanterns as the commonest of the period and the 2019 steel photographs are not period evidence; the DECISIONS entry of 9 October 12:29 makes it the main build, a session decision Jafar can overturn; its numbers are Judgement or the research's except where the period and 'unchanged object' photographs of try 2 say otherwise (TARGET.md section 0.5)",
    "frame": "as A: axis at the footway, z up, +y to the carriageway; the section is square to the street (faces at +-x and +-y)",
    "shaft": {"section": "square, arrises chamfered", "points_z_side_chamfer": [[-HIDDEN, C_FOOT, C_CH], [0, C_FOOT, C_CH], [C_ZREF, C_TOP, C_CH], [C_ZTOP, C_TOP_AT_ARM, C_CH]],
              "side_at_z0": C_FOOT, "side_at_z4620": C_TOP, "side_at_top": C_TOP_AT_ARM, "top_z": C_ZTOP, "chamfer": C_CH, "hidden_root": HIDDEN,
              "taper": "linear in z between the listed points: the side narrows 20.6 mm a metre (95 over 4620), both pairs of faces alike, the same straight line carried on to 117.5 at the arm's top (z 4985.8); the 15 chamfers are the same size at every height",
              "top_face": "flat, with a %d mm chamfer all round its edge; it is one face with the arm's top (second review, R1)" % C_TOPCH, "top_face_chamfer_mm": C_TOPCH,
              "root": "the shaft is planted: the lowest %d mm are hidden below the footway; no base plate, no collar: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar (as A's sleeve; Photo, BGE: block paving cut round a steel sleeve; no photograph of a concrete column's root was measured)" % HIDDEN,
              "kind": "Judgement: the research's '20 to 25 cm at the foot' (Read) and 'square or tapered in section' (uncertain); the photographs of try 2 agree with a plain tapering square shaft, see TARGET.md"},
    "bracket": {"kind": "a precast concrete arm cast as one with the shaft (second review, R1: every photograph of a concrete column with an angular arm shows an arm as thick as the column's top, joined to it in a sharp mitre, made of the column's own concrete; there is no cap, no stem and no bend radius)",
                "section": {"square": ARM_SQ, "chamfer": ARM_CH}, "axis_z": round(ARM_END_Z, 3), "top_z": C_ZTOP, "underside_z": V("c_arm_underside_z"),
                "from": "the shaft's -y face (y -58.7) along +y to a flat end face at y %d (edge chamfer %d)" % (ARM_END, V("c_arm_end_chamfer")),
                "centreline_yz": [[0, round(ARM_END_Z, 3)], [ARM_END, round(ARM_END_Z, 3)]], "joint": "mitre", "bend_turn_deg": TURN, "rake_deg": RAKE,
                "mitre": {"outer_corner_radius": V("c_mitre_outer_radius"), "outer_corner": "where the top face meets the shaft's -y face", "inner_fillet_radius": V("c_mitre_inner_fillet"), "inner_corner": "where the arm's underside meets the shaft's +y face, at (59.9, 4875.8)"},
                "material": "concrete_C, unpainted", "arm_end_y": ARM_END,
                "note": "the arm's top (4985.8) is one face with the shaft's top; the arm's end face at y 400 is flat; the spigot below leaves it and carries the lantern's boss"},
    "spigot": {"od": SPIGOT_OD, "y": list(SPIGOT_Y), "exposed_y": list(SPIGOT_EXPOSED), "axis_z": round(ARM_END_Z, 3), "paint": "black (31, 31, 34)", "material": "c_spigot",
               "kind": "a steel tube OD 42 on the arm's axis from y 340 (60 cast into the arm) to y 485 (inside the lantern's boss); 30 of it shows between the arm's end (400) and the boss (430); the boss, the lantern and the light are unchanged"},
    "door": c_door,
    "number_plate": {"on": "the +y face", "z_centre": V("bge_plate_z"), "size": [90, 45], "thickness": 1.2, "proud": 1.4, "flat": True, "fixing": "two domed rivets 5 across at 8 from each end", "text": "LC n as A's"},
    "plate_number": "as A: 90 x 45 white plate at z 2160 on +y, flat on the concrete face",
    "paint": "none: bare concrete (c_albedo_srgb) with algae and lime marks, shaft and arm alike; only the spigot is painted black",
    "materials": {"concrete": {"srgb": V("c_albedo_srgb"), "roughness": V("c_roughness"), "metal": 0.0, "paint": "none"}},
    "wear": [
        {"id": "algae", "where": "green algae on the -y face (the shaded face) from the footway to z 700, patchy, strongest below z 300; a lighter film on the other three faces to z 350", "colour": [86, 104, 70], "strength": 0.5, "kind": "Judgement (review F2); the photographs of try 2 show dark staining low down on the shaded side"},
        {"id": "lime_streaks", "where": "from the top face and the arm: 6 to 10 vertical lime streaks 30 to 400 long, 4 to 20 wide, pale (190, 188, 180) on every face, strongest under the arm", "colour": [190, 188, 180], "kind": "Judgement (review F2)"},
        {"id": "rust_bleed", "where": "under the door plate's two screws on -y: two streaks 60 to 200 long, 4 to 8 wide, rust brown", "colour": V("rust_srgb"), "kind": "Judgement (review F2)"},
        {"id": "chipped_arris", "where": "LC 2 only (x 18, west): one chipped arris on the +y face's right-hand edge, 60 long x 25 wide x 8 deep at z 400 to 460, the aggregate showing", "kind": "Judgement (review F2; a vehicle's knock; replaces A's dent)"},
        {"id": "splash_band", "where": "z 0 to 250 all round, darker grey-brown (112, 106, 98), top edge soft over 60", "colour": [112, 106, 98], "kind": "Judgement; the wear target lists lamp-column bases among its foot-splash features"},
    ],
}
variant_C["wear"] += [
    {"id": "arm_algae", "where": "a green algae film (86, 104, 70) on the arm's top face, patchy, strength 0.35", "colour": [86, 104, 70], "strength": 0.35, "kind": "Judgement (second review, R1)"},
    {"id": "arm_lime", "where": "2 to 4 lime streaks from the arm's underside and end face, 30 to 150 long, 4 to 12 wide, pale (190, 188, 180)", "colour": [190, 188, 180], "kind": "Judgement (second review, R1)"},
    {"id": "spigot_rust", "where": "one rust streak 20 to 60 long under the spigot at the arm's end", "colour": V("rust_srgb"), "kind": "Judgement (second review, R1)"},
    {"id": "canopy_streaks", "where": "8 to 12 vertical grime streaks from the canopy lip down the bowl, black (40, 38, 36) at 0.35", "kind": "Judgement"},
    {"id": "bowl_yellowing", "where": "the whole bowl, tint to bowl_unlit_srgb; 12 to 25 dark specks 1 to 3 mm inside it (dead insects)", "kind": "Judgement"},
    {"id": "bird_marks", "where": "the canopy's top, 2 to 3 patches of 20 to 60 mm, white-grey (205, 205, 190); the arm's top too", "kind": "Judgement; the wear target lists lamp tops as perches"},
]
variant_P = {
    "id": "P", "name": "post-top pod on the same lower column (the form BGE shows)", "build": False,
    "why": "BGE's column is exactly this: a black steel stepped tube with a small flat dish of a lantern on its top; the scene's lamps are bracket lamps, so P is not placed",
    "shaft_top_z": 4300, "pod": {"diameter": 420, "centre_z": 4375, "kind": "Photo diameter (417 +-30); the height 150 is Judgement (the thickness cannot be read from below)",
                                 "profile_rz": [[0, 4300], [30, 4300], [120, 4312], [180, 4340], [210, 4378], [200, 4418], [150, 4445], [60, 4455], [0, 4455]]},
    "pod_colours": {"shell": "dark grey-blue (60, 62, 78) as the sky tints it in BGE", "underside": "pale grey (190, 188, 184)"},
}
_w_arm_z = 4350
variant_W1 = {
    "id": "W1", "name": "wall bracket for the same lantern (optional, not placed)", "build": False,
    "why": "the street's old quarter may have a lantern on a wall; no photograph of a council wall bracket was reached (the two wall lanterns reached are a bespoke college lantern at Cambridge and a 2019 estate bulkhead, neither a street fitting); all Judgement",
    "plate": {"width": 150, "height": 220, "thickness": 8, "bolts": {"count": 4, "pitch": [100, 160], "head": "domed nut 24 across"}, "z_centre": 4300},
    "arm": {"od": 42, "from": [0, _w_arm_z], "rake_deg": 0, "to_y": ARM_END_Y, "strut": {"od": 25, "from": [0, 4130], "to_arm_at_y": 140},
            "note": "review point 8: level and coaxial with the lantern (rake 0), so no kink where it enters the boss; the reach to the spigot is the column's 430"},
    "lantern": "L1 unchanged, its rear boss at y 430 from the wall face; the arm runs level at z %d, so the lantern's top stands at z %d (the whole lantern %d lower than on the column)" % (_w_arm_z, round(5000 - (ARM_END_Z - _w_arm_z)), round(ARM_END_Z - _w_arm_z)),
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
                    "plate_text": f"LC {i + 1}", "wear_seed": 11 + 7 * i, "dent": (i == 1), "chipped_arris": (i == 1)})

# ------------------------------------------------------------------------------------------------------------------------------------
# the checks (what unit 3.8's automatic check must pass)
# ------------------------------------------------------------------------------------------------------------------------------------
def chk(name, applies, measure, expected, tol, kind):
    return {"name": name, "applies_to": applies, "measure": measure, "expected": expected, "tolerance": tol, "kind": kind}


checks = [
    chk("pivot_and_datum", "whole piece", "the pivot (origin) lies on the shaft's axis at the footway surface (z = 0) and the lowest vertex lies between z = -160 and z = -140", {"origin_xy_mm": [0, 0], "lowest_z_range": [-160, -140]}, 3, "Read (brief: pivot at the base's centre on the ground); the hidden skirt is 150"),
    chk("lantern_top_z", "A, C", "max z of the lantern's mesh above the footway, mm", 5000, 10, "Read (scene: mounting height 5.0 m to the lantern's top)"),
    chk("lantern_bounding_box", "A, C", "extent of the lantern mesh (canopy, bowl, catches, hinge; not the boss) along y, x, z, mm", {"y": 650, "x": 300, "z": 200}, 8, "Read (scene 0.55 x 0.30 x 0.20) lengthened to 650 by the second review, narrow point 1, and turned so the long side lies along y"),
    chk("lantern_centre", "A, C", "the lantern's bounding-box centre (x, y, z), mm", [0, YC, 4900], 12, "Read (the research's reach to the spigot 430 + half the length 325 = 755; top 5000, 200 tall): review fault 3 and second review point 1"),
    chk("lantern_axis", "A, C", "angle between the lantern's long axis and the arm's direction in plan (+y), degrees", 0.0, 3.0, "Photo (US01: the lantern lies along its arm)"),
    chk("lantern_tilt", "A, C", "angle between the bowl's base plane and the horizontal, degrees", 0.0, 1.5, "Judgement (level, as the scene)"),
    chk("lantern_canopy_rim_z", "A, C", "z of the canopy's lower edge, mm", V("canopy_rim_z"), 6, "Judgement"),
    chk("lantern_dome_height", "A, C", "the maximum over y of the canopy's top z minus the z of its lip's top, mm", 63, 6, "Judgement; review point 6 (the maximum is 63 at y 637; at the centre y 755 it is 61)"),
    chk("lantern_plan_silhouette", "A, C", "largest nearest distance (both ways) between the lantern's plan outline at z = 4925 and the polygon in target.json geometry.lantern.canopy.plan_half_width, mm", 0.0, 6.0, "Derived from the plan stations"),
    chk("lantern_section_silhouette", "A, C", "the same, for the cross-section at y = 755 and the long section at x = 0, against target_drawing.py's polygons", 0.0, 6.0, "Derived"),
    chk("bowl_base", "A, C", "the bowl's flat base: z 4800, length (y) and width (x), mm", {"z": 4800, "length": 473, "width": 164}, 8, "Judgement"),
    chk("lamp_in_bowl", "A, C", "the lamp's axis: parallel to y, centre (x, y, z), diameter and length, mm", {"centre": [0, YC, 4872], "od": 54, "length": 310}, 6, "Judgement (a 35 W SOX lamp)"),
    chk("lamp_arc_tube", "A, C", "the arc tube inside the jacket: two legs of 16 OD at x +-11, z 4872, y 605 to 895, joined at the front by a half-torus; wholly inside the jacket", {"leg_od": 16, "x": [-11, 11], "z": 4872, "y": [605, 895], "joined_at_front": True}, 3, "Judgement; the earlier research's 'a glowing U-shaped tube' and US01's lit lamp's bright stripes (review point 3)"),
    chk("lamp_inside_bowl_and_canopy", "A, C", "the lamp's whole volume lies inside the bowl's and canopy's inner shell: no vertex of the lamp outside the lantern's envelope", True, 0, "Derived"),
    chk("glow_surface", "A, C", "the emissive surfaces are the arc tube (full strength), the jacket (0.3 of it) and the bowl, nothing else emits: no emissive vertex outside them", {"emissive_parts": ["arc_tube", "lamp_jacket", "bowl"]}, 0, "Judgement; Photo (US01 lit: the bowl glows orange round a brighter core)"),
    chk("glow_strength", "A, C", "emissive strengths in cd/m2: jacket, bowl (the tube is the jacket over 0.3); or the engine's kLampEmissiveUnitless rule, stated", {"jacket_cd_m2": V("emissive_jacket_cd_m2"), "bowl_cd_m2": V("emissive_bowl_cd_m2"), "tube_over_jacket": round(1 / V("emissive_jacket_over_tube"), 2)}, 600, "Derived (4,550 lm over the jacket's 0.0526 m2; 80 % of it through 0.24 m2 of bowl): review point 4 and second review point 1"),
    chk("glow_colour_bowl", "A, C", "the bowl's emissive colour, sRGB 8-bit", V("glow_bowl_srgb"), 12, "Derived (the night note's lamp (1, 0.25, 0) gamma-encoded); Photo US01 251/152/14"),
    chk("glow_colour_lamp", "A, C", "the lamp jacket's and arc tube's emissive colour, sRGB 8-bit: the same orange as the bowl (the yellow core is the camera's clipping)", V("glow_lamp_srgb"), 12, "Derived (a sodium lamp's own light is one orange): review point 5"),
    chk("arm_stem_od", "A", "outer diameter of the bracket's steel stem, mm", V("stem_od"), 4, "Photo ratio (US01 0.47 to 0.67 of the shaft's top) + Judgement"),
    chk("c_arm_section", "C", "the concrete arm's section (square, width and height), the arris chamfer, the axis height and the end face's y, mm", {"width": ARM_SQ, "height": ARM_SQ, "chamfer": ARM_CH, "axis_z": round(ARM_END_Z, 1), "end_y": ARM_END}, 5, "Photo (GG3, 1485521: an arm about 0.85 to 1.2 of the shaft top, 9 of 10 px) + Judgement (110, 10): second review, R1"),
    chk("arm_rake", "A, C", "angle of the straight arm above horizontal, degrees (for C on the arm's and the spigot's common axis)", RAKE, 5.0, "Photo (US01, corrected for the arm's 35 to 42 degree turn toward the camera: true rake 0 to 7) + lead (vertical and horizontal sections) + the period photographs of 1989 (near-level arms)"),
    chk("arm_bend_turn", "A", "the one bend from the vertical stem to the level arm, degrees", TURN, 5.0, "Judgement (review fault 1)"),
    chk("arm_bend_radius", "A", "centreline radius of the bend, mm", R_BEND, 75, "Judgement (3 tube diameters, review fault 1); the tolerance spans the photographs: a mitred elbow of 55 (Birchington) to 3 diameters (Orrell)"),
    chk("arm_reaches_boss", "A, C", "the straight arm's end point (y, z), mm", [ARM_END_Y, round(ARM_END_Z, 1)], 12, "Read (the research's 406 to 457 reach to the spigot; review fault 3) + Judgement (the height); for C the spigot's and boss's common axis"),
    chk("arm_lantern_coaxial", "A, C", "the angle between the arm's last 50 mm, the boss axis and the lantern's long axis (all in the y-z plane), degrees: the largest of the three differences", 0.0, 2.0, "Photo (US01: the lantern lies on the arm's line, to within a few degrees; the 1989 stations; review fault 1)"),
    chk("boss_top_and_dome", "A, C", "the boss's top above the canopy's rear crown (z 4937) and the dome's height over the boss's front end (y 485): the top stands 24 above, and the dome is not pierced", {"top_above_crown": 23.8, "dome_over_front_end_z": 4967.4}, 6, "Judgement; review fault 1 (nothing pokes through the dome)"),
    chk("arm_continuity", "A", "no gap and no kink: the arm's centreline sampled every 10 mm is continuous (largest step under 12 mm; largest turn between consecutive samples under 8 degrees)", True, 0, "Derived"),
    chk("boss_clear_of_bowl", "A, C", "the nearest distance between the boss and the bowl (second review, narrow point 2: the bowl starts at y 488, the boss ends at y 485), mm", {"at_least": 3}, 0, "Derived (second review, narrow point 2)"),
    chk("arm_direction", "A, C", "the arm's plan direction against the carriageway's normal, degrees", 0.0, 3.0, "Read (scene: the lantern out toward the road)"),
    chk("sleeve_od", "A, P", "outer diameter of the sleeve at z = 300 and z = 800, mm", V("sleeve_od"), 9, "Photo (BGE 123.6 +-9; the scene's 114 is inside)"),
    chk("sleeve_height", "A, P", "z where the sleeve's straight side ends, mm", V("sleeve_height"), 15, "Photo (BGE 978 +-10)"),
    chk("cone", "A, P", "outer diameter at z = 1010 (about half way up the cone), mm", round(2 * shaft_radius_at(1010), 1), 8, "Derived from the profile"),
    chk("shaft_od_low", "A, P", "outer diameter of the shaft at z = 1200, mm", round(2 * shaft_radius_at(1200), 1), 6, "Photo (BGE 66 to 69)"),
    chk("shaft_od_mid", "A, P", "outer diameter of the shaft at z = 2500, mm", round(2 * shaft_radius_at(2500), 1), 6, "Derived (linear between the two photographed heights)"),
    chk("shaft_od_high", "A, P", "outer diameter of the shaft at z = 3900, mm", round(2 * shaft_radius_at(3900), 1), 6, "Photo (BGE 61)"),
    chk("shaft_taper_monotone", "A, P", "outer diameter never increases between z = 1044 and z = 4370 (steps of 100 mm)", True, 0, "Derived"),
    chk("collar", "A", "the bracket's socket sleeve: outer diameter and z range, mm", {"od": V("socket_od"), "z": [Z_SOCKET, Z_TOP]}, 4, "Photo qualitative (US01: no step, a flat chamfered top, a foot seam, two set screws) + Judgement: review point 1"),
    chk("socket_set_screws", "A", "two M8 set screws on -y (azimuth 180 from +y) at z 4580 and 4420, heads 10 across, proud 3, mm", {"count": 2, "z": list(V("socket_screw_z")), "azimuth": 180, "head_od": 10, "proud": 3}, 1.5, "Photo qualitative (US01: two set screws one above the other on one side): review point 1"),
    chk("lower_profile_silhouette", "A, P", "largest nearest distance (both ways) between the built lower column's outline in the y-z plane and geometry.A.lower.outer_rz mirrored, mm", 0.0, 4.0, "Derived; the profile is Photo (BGE)"),
    chk("door", "A", "door arc width, height, bottom z, proud, mm", {"arc_width": 100, "height": 500, "z_bottom": 400, "proud": 1.5}, 10, "Judgement (a lead: a modern 5 m stepped column has a 500 x 100 door 400 above the ground; US01: the door outline's top at about 86 % of the sleeve; the research: a door plate about 50 cm up)"),
    chk("door_corner_radius", "A", "the radius of all four corners of the door and of its joint groove, mm", 15, 3, "Photo (US01: the flush door's rounded top corners, about 2 px at 7 mm): review point 2"),
    chk("door_face", "A", "azimuth of the door's centre against +y, degrees", 180, 12, "Judgement"),
    chk("door_groove", "A", "joint groove width and depth round the door, mm", {"width": 2.5, "depth": 2.0}, 1.0, "Judgement"),
    chk("number_plate", "A, C", "plate size (arc x height), centre z, face (+y), mm", {"size": [90, 45], "z": 2160, "face": "+y"}, 8, "Photo (BGE: a reference plate at z 2115 to 2200)"),
    chk("plate_text_only_lc_n", "A, C", "the only characters on any surface of the piece are 'LC' and one digit 1 to 4, on the plate", True, 0, "Judgement: no maker, no council, no crown"),
    chk("no_maker_marks", "all", "no text, logo or relief lettering on any mesh or texture except the plate's; in particular none of the makers' names in the earlier research, none on the door, the lantern, the base or the concrete", True, 0, "Rulings 8 October and brief"),
    chk("boss", "A, C", "the lantern's rear boss: outer diameter, length, axis rake, mm and degrees", {"od": 60, "length": 55, "rake_deg": RAKE}, 5, "Judgement; level since try 2"),
    chk("c_shaft_side_z300", "C", "the concrete shaft's side across the faces at z = 300, mm", round(c_side(300), 1), 6, "Judgement (linear 220 to 125 over 4620; review F2: 213.8)"),
    chk("c_shaft_side_z2300", "C", "the concrete shaft's side at z = 2300, mm", round(c_side(2300), 1), 6, "Judgement (review F2: 172.7)"),
    chk("c_shaft_side_z4300", "C", "the concrete shaft's side at z = 4300, mm", round(c_side(4300), 1), 6, "Judgement (review F2: 131.6)"),
    chk("c_chamfer", "C", "the arris chamfer (leg length on each face), mm, at z = 300, 2300 and 4300", C_CH, 3, "Judgement (review F2: 15 throughout)"),
    chk("c_top_face_chamfer", "C", "the top face's edge chamfer, mm", C_TOPCH, 2, "Judgement (review F2: 5)"),
    chk("c_section_square_to_street", "C", "the section's faces against the street's axes (x along the street, y to the carriageway), degrees", 0.0, 2.0, "Judgement (review F2)"),
    chk("c_door_recess", "C", "the door recess on -y: width, height, depth, z range, mm", {"width": 120, "height": 330, "depth": 14, "z": [450, 780]}, 5, "Judgement (review F2; the research: a door plate about 50 cm up)"),
    chk("c_door_plate", "C", "the steel door plate over the recess: width, height, thickness, proud, mm", {"width": 132, "height": 342, "thickness": 3, "proud": 3}, 5, "Judgement (review F2)"),
    chk("c_door_screws", "C", "two screws 10 across on the plate's centre line, 25 from its ends (z 469 and 761), blank heads", {"count": 2, "head_od": 10, "z": [469, 761]}, 5, "Judgement (review F2)"),
    chk("c_mitre", "C", "the arm's joint with the shaft: a sharp mitre, the outer corner (the top face meeting the shaft's -y face) rounded to radius 20, the inner corner (the underside meeting the +y face, at (59.9, 4875.8)) a fillet of radius 10; the top face's z, mm", {"outer_corner_radius": V("c_mitre_outer_radius"), "inner_fillet_radius": V("c_mitre_inner_fillet"), "top_face_z": C_ZTOP}, 5, "Photo (GG3: the inner corner square, the outer rounded by about 2 px) + Judgement (20, 10): second review, R1"),
    chk("c_spigot", "C", "the steel spigot on the arm's axis: OD, its y range (60 cast into the arm) and the 30 that shows between the arm's end and the boss, mm", {"od": SPIGOT_OD, "y": list(SPIGOT_Y), "exposed_y": list(SPIGOT_EXPOSED)}, 3, "Judgement (second review, R1)"),
    chk("c_albedo", "C", "mean albedo of the concrete shaft and arm, sRGB 8-bit", V("c_albedo_srgb"), 12, "Judgement (weathered precast concrete)"),
    chk("c_roughness", "C", "roughness of the concrete, shaft and arm (0 to 1)", V("c_roughness"), 0.1, "Judgement (rough matt)"),
    chk("c_no_paint", "C", "the shaft and arm carry no paint, no band and no lettering; only the spigot is black", True, 0, "Judgement (review F2)"),
    chk("c_wear_features", "C", "the concrete's wear: algae to z 700 on -y, lime streaks from the top, rust bleed under the door plate's screws, a chipped arris 60 x 25 x 8 at z 400 to 460 on +y on LC 2 only", {"algae_z_max": 700, "chipped_arris": [60, 25, 8], "chipped_z": [400, 460], "only_on": "LC 2"}, 0, "Judgement (review F2)"),
    chk("paint_black", "A, P", "mean albedo of the sleeve's undamaged paint, sRGB 8-bit", V("paint_black_srgb"), 12, "Photo (BGE 31/31/33)"),
    chk("paint_gloss", "A, P", "roughness of the undamaged paint on the sleeve (0 to 1); the upper shaft is 0.15 higher", {"sleeve": 0.42, "upper_shaft_plus": 0.15}, 0.10, "Judgement (the recipe's 0.42; BGE shows gloss worn to semi-gloss)"),
    chk("splash_band", "A, P", "the splash band's height above the footway where the albedo returns to the paint, mm", 250, 60, "Photo (BGE: z 0 to 250 is 49/46/42)"),
    chk("canopy_colour", "A, C", "mean albedo of the canopy's undamaged paint, sRGB 8-bit", V("canopy_srgb"), 18, "Judgement"),
    chk("placement_xs", "street", "the four columns' x, m", V("scene_column_x"), 0.05, "Read (pieces file and code)"),
    chk("placement_sides", "street", "the four columns' sides, east first", ["east", "west", "east", "west"], 0, "Read"),
    chk("placement_setback", "street", "the axis's distance behind the kerb's BACK face, mm", 600, 40, "Read (scene 0.6)"),
    chk("placement_vertical", "street", "the axis's lean from vertical, degrees (the footway falls 1 in 40 toward the road; the column stands plumb)", 0.0, 0.3, "Derived"),
    chk("light_position", "A, C", "the point light's position (x, y, z), mm, and the count per column", {"pos": [0, YC, 4850], "count_per_column": 1}, 12, "Read (scene: 0.05 m below the centre) with the lantern's centre at y 755: review fault 3 and second review point 1"),
    chk("light_pool", "A, C", "the pool spot: lumens, inner and outer cone, degrees, aimed straight down, shadows on", {"lm": 350, "inner": 15, "outer": 55}, 0, "Read (night note step 4)"),
    chk("light_skirt", "A, C", "the skirt spot: lumens, inner and outer cone, degrees, straight down, no shadows", {"lm": 800, "inner": 45, "outer": 80}, 0, "Read (night note step 4)"),
    chk("light_glow", "A, C", "the all-round glow: lumens, no shadows", {"lm": 40}, 0, "Read (night note, DECISIONS 7 October)"),
    chk("light_colour", "A, C", "the lights' colour, linear sRGB (the night note's lamp, one number to be tried at (1, 0.40, 0.03))", V("night_current_lamp_linear"), 0.03, "Read (night note); NOT the scene's (1, 0.7055, 0)"),
    chk("triangles", "A, C", "triangle count of one column with its lantern at LOD0", [3000, 12000], 0, "Judgement (mid-poly, a bevel on every edge: the asset plan; four columns are about 4 % of a frame)"),
    chk("bevels", "A, C", "every hard edge has a bevel; radii in `bevels`", True, 0, "Judgement (the asset plan's method)"),
]

bevels = [{"edge": "sleeve top lip (z 978)", "radius": 1.5}, {"edge": "socket top chamfer and foot edge", "radius": 1.5}, {"edge": "concrete shaft arrises (chamfer)", "radius": 15.0}, {"edge": "concrete top face edge (chamfer)", "radius": 5.0}, {"edge": "concrete arm arrises (chamfer)", "radius": 10.0}, {"edge": "arm end face edge (chamfer)", "radius": 5.0}, {"edge": "door perimeter (outer)", "radius": 1.0},
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
    "title": "Quay Street's lamp posts: the target (cloud week 42, try 2 and the second review's fixes, 11 and 12 October 2026)",
    "written": "2026-10-09",
    "rewritten": "2026-10-11 (try 2: the review of 9 October applied); 2026-10-12 (the second review of 11 October applied: the concrete arm, the 650 lantern; not re-reviewed)",
    "units": {"length": "millimetres in this file unless a key says metres (_m)", "glb": "metres, z up, scale 1",
              "frame": "origin on the column's vertical axis at the footway surface; +y toward the carriageway (the lantern side); x along the street; z up; for the west side's columns the whole piece is turned 180 degrees about z so that +y still points at the road",
              "pivot": "the axis at z = 0 (the footway surface); the sleeve runs 150 mm below it, hidden"},
    "summary_line": "",  # filled below
    "no_period_photograph_of_a_concrete_column_with_sodium_lantern": True,
    "period_photographs_of_steel_columns": True,
    "decision_type": {
        "main": "C: a precast concrete column (a square shaft 220 at the foot tapering to 125 at 4620 and 117.5 at its top, arrises chamfered 15, planted) with a precast concrete arm of the shaft's own width (110 square) leaving its top in a mitre and running LEVEL to 400, a 42 steel spigot from the arm's end into the rear boss (at 430) of a boat-shaped aluminium canopy (650 x 300 x 200, its top at 5000, its centre 755 out) over a deep yellowed clear bowl with a 54 x 310 sodium lamp and a U-shaped arc tube inside it, the lamp's long axis along the arm; 4 columns at x 8, 18, 28, 38, alternate sides",
        "alternatives": ["A: painted-steel stepped column (124 sleeve, cone, 68-to-60 shaft, a 250 socket) with a steel bent-arm bracket (a 48 stem, one 90 degree bend of radius 130, a level arm to 430) and the same lantern (written in full; built only if ruled in)", "P: post-top dish on the same lower column (what BGE shows; not placed)", "W1: a wall bracket for the same lantern (optional; not placed)"],
        "why_C_is_main": "review fault 2 (9 October): the earlier research (street-clutter-1990, section 3) says precast concrete into the 1980s; the steel form rested on 2019 London photographs that may be replacements; DECISIONS.md 9 October 12:29 records the swap as a session decision Jafar can overturn",
        "who_decides": "the builder builds C; Jafar may rule A in (one line on his page: 'The street's lamp columns: concrete (recommended) or black steel')"},
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
        {"id": "PW2", "what": "the bracket", "scene": "a swan neck of three short cylinders on a quarter circle, rising over the lantern and dropping into it (the code's comment: 'a straight bracket reads as a modern column')", "photograph": "US01: a vertical stem, one bend, a straight arm (level, read in 3D) entering the lantern's rear end; the 1989 stations the same; R07 reads 'plain bent-arm lighting' (production/reference/photographs.md)", "chose": "the bent arm", "kind": "Photo + Read"},
        {"id": "PW3", "what": "the lantern's long axis", "scene": "0.55 along the street", "photograph": "US01 seen from below: the arm enters the lantern's rear end and the lantern lies along it", "chose": "along the arm (y); the box's size is kept", "kind": "Photo"},
        {"id": "PW4", "what": "the lantern's form", "scene": "a box", "photograph": "US01 lit lantern: a boat-shaped canopy over a bowl that glows orange round a brighter core; the research: 'a boat-shaped canopy 60 to 70 cm long over a deep clear trough-shaped bowl'", "chose": "canopy over bowl, the lamp visible inside", "kind": "Photo + Read"},
        {"id": "PW5", "what": "the lantern's colour", "scene": "linear (1.0, 0.7055, 0.0), gamma (255, 219, 0): a yellow", "photograph": "US01 lit: median 251/152/14 (orange); the night note's lamp (1, 0.25, 0); derived 589 nm: (1, 0.2195, 0) linear = 255/129/0", "chose": "(255, 137, 0) for the bowl (the night note's lamp gamma-encoded); the scene's xy is 585 nm, not 589, and its normalisation skipped the division in green", "kind": "Photo + Derived"},
        {"id": "PW6", "what": "the column's concrete or steel", "scene": "steel (surface 'metal')", "photograph": "the 2019 photographs show steel (not period evidence for the type); the earlier research says concrete; the period photographs of 1989 show steel stepped columns at two railway stations; the 'unchanged object' photographs of 2008 to 2010 show concrete columns with their original sodium lanterns (TARGET.md section 0.5)", "chose": "precast concrete main (C), steel as the variant (A): review fault 2; DECISIONS.md 9 October 12:29", "kind": "Judgement"},
        {"id": "PW8", "what": "the bracket's rake", "scene": "a swan neck rising over the lantern; try 1 of this target read 40 degrees from US01's apparent slope", "photograph": "US01's 41.7 degrees is perspective: its arm points 35 to 42 degrees toward the camera (the street's vanishing point) and the camera looks up 45 degrees, so the true rake is 0 to 7 and the lantern lies on the arm's line; the 1989 photographs of two steel columns (Orrell, Appley Bridge) show arms rising 10 degrees or less in the picture with the lantern in line; GG3's arm rises 16 to 19 degrees in the picture (1485521's about 18); the arm's plan direction cannot be read off one 640 px picture, so its true rake is 0 to about 18; the level arm of US01 read in 3D and the 1989 photographs is kept (rake 0 +-5)", "chose": "rake 0 (+-5): one 90 degree bend and a level arm, the lantern level and coaxial", "kind": "Photo (3D reading) + lead"},
        {"id": "PW9", "what": "the bracket's reach", "scene": "outreach_m 0.5 to the lantern's CENTRE (the stand-in's trade guess), which put the lantern's rear 225 from the axis", "photograph": "the earlier research (Read): the arm reaches 1 ft 4 in to 1 ft 6 in (406 to 457) to the spigot; US01's reach to the boss is 0.12 to 0.14 of the column's height (0.6 to 0.7 m at 5 m); Birchington (2008): the lantern's rear stands about 4.3 column-top widths from the axis, 430 to 540 for a top of 100 to 125; the two 1989 steel columns on railway premises show 2.8 and 5 tube widths (170 to 300 mm for a 60 tube): shorter, with an unknown scale, so not followed", "chose": "430 to the spigot (the lantern's rear), 755 to its centre, 1080 to its front end (the lantern 650 long since the second review)", "kind": "Read + Photo"},
        {"id": "PW10", "what": "the arm's form on a concrete column", "scene": "a swan neck; the first review's thin black steel tube on a cap", "photograph": "GG3 (Birchington, 2008) and 1485521 (2008): an arm 0.85 to 1.2 of the column top's width, joined in a sharp mitre, made of the column's own concrete, no cap; 5418611, 7029133 and 6558618: the shaft's own width and colour carry on into a curved arm; 6538305 and 6558618: 'matching concrete outreach brackets'; Chigwell Road (GG4, 2009) and Coundon (GG5, 2010): thin steel goosenecks (GG5's on a pale socket cap)", "chose": "the mitred concrete arm (R1, below and PW13); the curved concrete arm and the thin steel gooseneck are not written out", "kind": "Photo (several photographs, 640 px)"},
        {"id": "PW11", "what": "the bend's radius (variant A only since the second review)", "scene": "the review: 130, three tube diameters", "photograph": "Birchington: a mitred elbow, centreline radius about 55 (+-30, one diameter), which is now C's mitre; Orrell (1989): about 3 tube diameters; Appley Bridge (1989): about 2", "chose": "130 as the review gives it for A's steel bracket, inside the span of the two steel photographs; the check's tolerance is +-75", "kind": "Photo + Judgement"},
        {"id": "PW12", "what": "the lantern's length", "scene": "0.55 along the arm (a stand-in's box; the research estimates 600 to 700)", "photograph": "the earlier research (Read): 600 to 700; GG3's lantern is about 62 px long, about 6 times its arm (680 at the amended 110), foreshortening only makes it longer; GG1 and GG2's lanterns are 12 to 14 tube widths, against the 550's 9", "chose": "650 (second review, narrow point 1): every y station of the lantern becomes 430 + (y - 430) x 13/11, the boss stays at y 430 to 485, the lamp and its arc tube keep their sizes", "kind": "Photo (qualitative) + Read"},
        {"id": "PW13", "what": "the arm on a concrete column", "scene": "the book or stand-in: the first review's 48 steel stem, cast cap and 90 degree bend", "photograph": "GG3 and 1485521 (a mitred arm 0.85 to 1.2 of the top); 5418611, 7029133 and 6558618 (curved arms of the shaft's width); 6538305 ('matching concrete outreach brackets', about 1970, low-pressure sodium); thin steel brackets on a concrete column only in GG4 and GG5, both curved goosenecks or hooks; the target's bracket appears on no concrete column (it is the steel stations' GG1 and GG2)", "chose": "the mitred concrete arm: 110 square, level at z 4930.8 out to y 400, outer corner R20, inner fillet R10, a 42 black steel spigot into the lantern's boss", "kind": "Photo"},
        {"id": "PW7", "what": "the count and places", "scene": "SCENE-SLOTS.md 'every 20 m, alternate sides, first at 8 m'", "photograph": "the code and pieces file: x 8, 18, 28, 38, east, west, east, west", "chose": "the code's four", "kind": "Read"},
    ],
    "variants": {"C": variant_C, "A": {"id": "A", "name": "steel bent-arm column (the alternative since try 2)", "build": False, "count_in_street": 0, "built_only_if": "Jafar rules the steel column in",
                                         "note_point_9": "review point 9: if A is built, use a shaft top of 64 to 68 at z 4560 (a straight taper from 68, nearly parallel) so that the stem and socket do not look heavier than the shaft; the socket is then made 4 to 6 larger than the shaft top; not applied to A's numbers because C is the main build"}, "P": variant_P, "W1": variant_W1},
    "geometry": {
        "lantern": lantern,
        "C": {
            "shaft": variant_C["shaft"], "door": c_door, "number_plate": variant_C["number_plate"],
            "bracket": variant_C["bracket"], "spigot": variant_C["spigot"], "lantern": {"same_as": "geometry.lantern"},
            "notes": "the main build since try 2; see variants.C for its materials and wear",
        },
        "A": {
            "lower": {"outer_rz": outer_rz, "hidden_skirt": HIDDEN,
                      "root": {"meets_ground": "the sleeve runs straight into the footway: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar; no base plate, no collar, no bolts show; the skirt continues 150 mm below the footway (hidden); the footway falls 1 in 40 toward the road, which is 3 mm across the sleeve, and the column stands plumb",
                               "kind": "Photo (BGE: the block paving is cut round the sleeve with a dark joint, no plate) + Judgement (the figures)"},
                      "note": "(radius, z) in mm of the outer surface, revolved about the axis; the sleeve to z 978, a cone to 1038 (25 degrees off the vertical), a 1.5 proud ring 1038 to 1044, the shaft's straight taper from r 34 (the same line carried on to r 30 at z 4560, hidden in the socket), the socket r 32 from 4370 to 4620 with a 3 chamfer on its top edge",
                      "weld_seam": "a longitudinal weld line 1.5 wide and 0.5 proud on the shaft, on the -y face (BGE shows a faint vertical line near the shaft's edge: qualitative)",
                      "sleeve_joint": "a 1 mm groove round the sleeve at z 978 where the cone cap is welded on"},
            "door": door, "plate": plate, "socket": socket,
            "bracket": {"tube_od_stem": V("stem_od"), "centreline_yz": centreline, "stem_from_z": Z_TOP - 60, "stem_to_z": STEM_TOP, "bend_radius": R_BEND, "bend_turn_deg": TURN,
                        "rake_deg": RAKE, "arm_start": [round(BEND_END_Y, 3), round(BEND_END_Z, 3)], "arm_end": [ARM_END_Y, round(ARM_END_Z, 3)], "arm_length": round(ARM_LEN, 2),
                        "note": "the stem rises vertically from inside the socket (z 4560) to z 4800.8, one 90 degree bend of centreline radius 130 to a straight LEVEL arm 300 long ending at (430, 4930.8), inside the lantern's rear boss"},
            "lantern": {"same_as": "geometry.lantern"},
        },
    },
    "light": {
        "lamp": {"what": "35 W low-pressure sodium (SOX), 589 nm", "lumens": V("lamp_lumens_35w_sox"), "kind": "Read (the night note, a maker's datasheet by search summary)"},
        "position_mm": [0, V("lamp_centre_y"), V("light_z")], "placement_rule": "Read: one point light 0.05 m below the centre of the emissive piece (the lantern's centre z 4900, y 755)",
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
                   "photo_lit_lantern_median_srgb": V("us01_lit_median_srgb"), "glow_bowl_srgb": V("glow_bowl_srgb"), "glow_lamp_srgb": V("glow_lamp_srgb"), "jacket_note": "review point 5: the jacket is the same orange at full strength; the photograph's yellow core is the camera's clipping and is left to the grade",
                   "note": "an RGB renderer cannot reproduce the colour loss (evening note section 3); the lamp's own light is one orange"},
        "warm_up": "a freshly lit SOX lamp glows dim red-pink for a few minutes before turning yellow-orange (evening note section 1); an optional start-up ramp, not required",
        "glow_surface": {"emissive_parts": ["arc tube (the U, full strength)", "lamp jacket (cylinder 54 x 310 at (0, 755, 4872), 0.3 of the tube)", "the bowl (translucent)"], "not_emissive": ["canopy", "arm", "column", "boss", "catches", "hinge"],
                     "lit_srgb": {"lamp": V("glow_lamp_srgb"), "bowl": V("glow_bowl_srgb")}, "units_cd_m2": {"jacket": V("emissive_jacket_cd_m2"), "bowl": V("emissive_bowl_cd_m2"), "tube": round(V("emissive_jacket_cd_m2") / V("emissive_jacket_over_tube"), -2)}, "unitless_fallback": "kLampEmissiveUnitless = 1.0 times the lantern colour in linear (1, 0.25, 0)", "unlit": "both read pale and clear by day (materials.lamp_glass, materials.bowl)"},
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
        "lamp_glass": {"srgb_unlit": [200, 196, 180], "emissive_srgb_lit": V("glow_lamp_srgb"), "emissive_cd_m2": V("emissive_jacket_cd_m2"), "relative_to_tube": V("emissive_jacket_over_tube"), "name": "the lamp's glass jacket, pale when cold, glowing when lit", "roughness": 0.10, "roughness_words": "glossy", "metal": 0.0},
        "arc_tube": {"srgb_unlit": [170, 166, 158], "emissive_srgb_lit": V("glow_lamp_srgb"), "emissive_cd_m2": round(V("emissive_jacket_cd_m2") / V("emissive_jacket_over_tube"), -2), "name": "the U-shaped arc tube inside the jacket: grey when cold, the full-strength orange when lit", "roughness": 0.2, "metal": 0.0, "kind": "Judgement (review point 3)"},
        "bowl_emissive_lit": {"srgb": V("glow_bowl_srgb"), "emissive_cd_m2": V("emissive_bowl_cd_m2"), "relative_to_jacket": round(V("emissive_bowl_cd_m2") / V("emissive_jacket_cd_m2"), 2), "name": "the bowl lit: sodium orange", "roughness": 0.15, "roughness_words": "glossy", "metal": 0.0},
        "plate": {"srgb_white": V("plate_white_srgb"), "srgb_letters": V("plate_black_srgb"), "name": "aged white enamel number plate", "roughness": 0.30, "roughness_words": "semi-gloss enamel", "metal": 0.0},
        "concrete_C": {"srgb": V("c_albedo_srgb"), "name": "weathered grey precast concrete (variant C, the main build)", "roughness": V("c_roughness"), "roughness_words": "rough matt", "metal": 0.0, "kind": "Judgement; the photographs of 2008 to 2010 show pale grey-brown concrete, darker low down on the shaded side"},
        "c_door_plate": {"srgb": [60, 62, 60], "name": "painted steel door plate, dark grey-green, blank", "roughness": 0.6, "roughness_words": "satin, worn", "metal": 0.0, "kind": "Judgement"},
        "c_spigot": {"srgb": V("paint_black_srgb"), "name": "the steel spigot from the concrete arm into the lantern's boss: lamp-post black like A's paint", "roughness": 0.42, "metal": 0.0, "kind": "Judgement (second review, R1)"},
    },
    "wear": {
        "state": "a tired column of twenty or thirty years in a port town's wet air: the concrete (main build C) streaked and greened low on its shaded side, limed under its arm, rust at the door plate's screws and under the spigot; variant A's black paint gone to semi-gloss, chipped where knocked, a splash band, rust at fixings",
        "features": variant_C["wear"],
        "agrees_with": "the wear target (production/cloud-week/targets/wear/TARGET.md: 'lamp-column bases' in the foot-splash feature list; 'street lamp tops' as perches)",
        "features_A": [
            {"id": "splash_band", "where": "the sleeve, z 0 to 250, all round (1.0 on the carriageway face, 0.6 elsewhere), top edge soft over 60", "colour": V("splash_srgb"), "kind": "Photo (BGE)"},
            {"id": "chips", "where": "the sleeve, carriageway face, z 150 to 900: 12 to 20 chips of 2 to 10 mm showing primer, 20 % with a rust speck; plus 5 to 8 chips of 4 to 15 mm on the sleeve's top lip and the cone", "colour": V("primer_srgb"), "kind": "Photo (US01: pale patches at the shoulder) + Judgement"},
            {"id": "scratches", "where": "the sleeve's carriageway face, z 380 to 430: 6 to 10 hairlines of 30 to 120 mm in light grey, no letters", "colour": [120, 118, 115], "kind": "Photo (BGE)"},
            {"id": "rust_streaks", "where": "under each socket set screw (two, 80 to 200 long, 3 to 6 wide, strength 0.6); from the door's two lower corners (two, 40 to 120); under the boss's two grub screws (two, 40 to 100)", "colour": V("rust_srgb"), "kind": "Judgement"},
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
T["period_photographs"] = json.load(open(os.path.join(HERE, "period_photos.json")))
T["summary_line"] = (
    "Quay Street's four lamp posts (x 8, 18, 28, 38, alternate sides) are precast concrete columns, the main build since the review of 9 October: a square shaft 220 at the foot tapering to 125 at 4.62 m with 15 mm chamfered arrises, "
    "a door recess 120 x 330 with a blank steel plate at z 450 to 780, a 90 x 45 reference plate 'LC n', and a precast concrete arm of the shaft's own width (110 square) leaving its top in a mitre and running LEVEL to 400, a 42 steel spigot carrying the lantern's rear boss at 430 "
    "into a boat-shaped aluminium canopy (650 x 300 x 200, its top at 5000, centred 755 out, the lantern in line with the arm) over a yellowed clear bowl with a 54 x 310 sodium lamp and a U-shaped arc tube inside it; "
    "the painted-steel stepped column of the 2019 photographs (a 124 sleeve 978 high, a 60 mm cone, a 68-to-60 shaft, a 250 socket sleeve for the same bracket) is kept in full as the alternative; "
    "the lit lantern is orange (255, 137, 0), the scene's (255, 219, 0) being the colour of 585 nm, not 589; no photograph of a concrete column with a sodium lantern taken before 2000 was found "
    "(two of 1989 (GG1, GG2) show steel columns with near-level arms and the lantern in line; the concrete ones are of 2008 to 2010 and have old lanterns by their photographers' word: GG4's 'looks to still retain its original low pressure sodium lamp'; GG3's lantern 'old', its decade not stated; GG5's lantern not dated), so every concrete length is Judgement within the photographs' span.")
T["leads"] = [
    {"text": "the SOX 35 W lamp is listed as 311 mm long and 52 mm across by a maker's datasheet and 310 x 54 by a catalogue table; 4,550 lm, 1,700 to 1,800 K", "via": "WebSearch summary, a lamp maker's datasheet and a trade catalogue table", "effect": "the lamp's 54 x 310 sits inside both; not changed"},
    {"text": "a modern 5 m stepped root-mounted steel column is listed with a 76 mm shaft, a 140 mm base, a 500 x 100 door 400 above the ground, a 150 x 75 cable slot, an 800 mm planting depth and a bitumen-coated root; its standard (the 1978 BS 5649 series, current to 2006) was not reached", "via": "WebSearch summary, three makers' catalogues (modern)", "effect": "A's door is 100 x 500 at 400; the photographed sleeve 124 and shaft 68 to 60 are smaller than that catalogue's 140 and 76 (BGE's is a post-top column) and are kept"},
    {"text": "enthusiasts' pages describe 1960s to 1970s 5 m precast concrete columns carrying 35 W SOX lanterns on 'angular top-entry brackets', a maker's mark cast into the inspection door, and two 5 m tubular steel columns with 'angular' brackets with a vertical and a horizontal section, the lantern steeply tilted; install dates not stated", "via": "WebSearch summary of streetlightonline.co.uk pages (unreached)", "effect": "both types existed with the same lantern; the 'vertical and horizontal section' bracket is the review's amendment; a real door might carry a maker's mark: ours is blank by rule"},
    {"text": "no source for a bracket's upsweep angle was found (the results were Australian and modern)", "via": "WebSearch summary", "effect": "the rake rests on US01 read in 3D and on the photographs of 1989, 2008 and 2009"},
]
T["unreached"] = [
    {"what": "Wikipedia, Flickr, HathiTrust, the National Archives, Historic England, legislation.gov.uk, the street-lighting enthusiasts' sites the earlier research cites, the lantern and column makers' catalogues", "result": "000 or 403 at the proxy on 9 October 2026 (curl, 20 s); not retried on 11 October", "used": "nothing"},
    {"what": "Wikimedia Commons (api.php search and category listings, 11 October 2026)", "result": "reached, but the shared address was rate-limited (HTTP 429) and the searches that did return gave no 1975 to 2000 photograph of a British lamp column; nothing was taken from it", "used": "nothing"},
    {"what": "archive.org advancedsearch.php (11 October 2026)", "result": "reached (HTTP 200); one search for 'street lighting column' returned books and reports, no period street photograph; nothing taken", "used": "nothing"},
]
T["to_read_when_the_network_opens"] = [
    "dated photographs, 1975 to 1995, of provincial British streets with a PRECAST CONCRETE lighting column and a low-pressure sodium lantern close enough to read the bracket, the shaft's taper, the base or door and the root (try 2 found none: Geograph's pre-2000 photographs that mention lighting are few and mostly stations and trams); from the PC: the Middlesbrough, Tyne and Wear and North Tyneside albums on Flickr and the lighting enthusiasts' pages, by date taken",
    "the 1989 code for minor roads (BS 5489-3, current from 31 August 1989 to August 1992) for the column heights and spacing the street would have used",
    "the standard tube sizes of tubular steel columns (BS 1308 / BS 5649 families) and the maker-neutral root-section proportions of a 5 m stepped column",
    "a SOX 35 W lamp's datasheet: jacket diameter and length, lumens, warm-up curve",
    "a larger copy of one concrete-column photograph (Geograph gives 640 px; the originals are with the photographers) to read the top width, the elbow's radius and the lantern's length to better than +-20 %",
]
T["could_not_settle"] = [
    "whether 1990's minor street in a northern port town had precast concrete or painted tubular steel columns: still no 1975 to 1995 photograph of a concrete column with a sodium lantern was found; concrete is the main build on the review's judgement and the earlier research (DECISIONS.md 9 October 12:29), two photographs of 1989 (GG1, GG2) show steel columns with a steel bracket and the same lantern form, and the concrete photographs are of 2008 to 2021 (old lanterns by their photographers' word, not proved)",
    "the arm's form: GG3 and 1485521 show a mitred concrete arm (built); 5418611, 7029133 and 6558618 show curved concrete arms and GG4 and GG5 thin steel goosenecks (not written out: PW10, PW13)",
    "the bend's radius (variant A only): 130 (three diameters) lies inside the two steel photographs' 2 to 3 diameters; the check's tolerance is +-75",
    "the lantern's length: 650 (second review, narrow point 1) rests on one oblique 640 px picture's ratio to the arm (about 6) and on the research's 600 to 700; the error of that picture is as big as 50 mm; the first thing to settle from the PC is a larger copy of GG3 or 1485521",
    "every BGE and US01 length is +-7 % in absolute size (camera height 1.02 +-0.07 m, 1.16 +-0.07 m); if the BGE sleeve is the standard 114.3 mm tube, all BGE lengths are 7 % smaller",
    "the door's real size and place on both columns (only a faint outline on US01; the concrete door is Judgement)",
    "the 35 W SOX lamp's physical size: 54 x 310 is a catalogue table's figure by search lead (a maker's datasheet lead says 52 x 311); no datasheet was reached",
    "the real light: the night note's numbers are its own intent, not measured in the game; whether the orange (255, 137, 0) reads right in the game's camera is for a fresh reviewer to judge against photographs from the PC; the emissive units are derived, not measured",
    "no photograph of a council wall bracket lantern was reached: W1 is entirely Judgement",
]
T["handover"] = {
    "for_scene_file": "furniture E1 and E2: replace the base 0.2 x 0.3, the 0.114 shaft, the three-cylinder swan neck and the box lantern by the kit piece C at the same four places (x 8 E, 18 W, 28 E, 38 W; axis 0.6 m behind the kerb's back); the lantern's top stays at 5.0 and its long side lies along the arm; outreach_m 0.5 becomes 0.755 (the lantern's centre; its rear end is 0.43 out and its front 1.08; its centre stands 15 mm behind the kerb face and its front end 310 over the channel); the night note's pool and skirt numbers are unchanged and the pool moves 0.2 m toward the road",
    "for_the_night_scene": "the point light and the two spots at (0, 755, 4850) in the piece's frame; colour (1, 0.25, 0) linear, not the scene file's (1, 0.7055, 0); the arc tube, jacket and bowl are the emissive parts (about 91,700, 27,500 and 4,800 cd/m2, or the kLampEmissiveUnitless rule); the scene file's lantern colour needs correcting (a ruling, so asked first)",
    "for_Jafar_s_page": "if the builder wants it confirmed: 'The street's lamp columns: concrete (recommended) or black steel' (DECISIONS.md 9 October 12:29 records concrete as a session decision he can overturn)",
    "for_the_wear_target": "the lamp-column base foot-splash is the splash_band here (z 0 to 250); for the concrete column the wear target's iron_wear tone row applies to the spigot only",
    "for_the_posters_target": "its SF4 puts bills on the shafts at x 8, 28, 48: the street has columns at 8, 18, 28, 38; the shaft is 125 to 220 across (concrete, square) at the bill's height, not 114; a bill on a column stands on a flat face of 172 at z 2300 (so 'the middle 0.17 m of an A3 shows face-on' becomes the whole width of an A3's 0.297 over the corner chamfers: the face is flat 142 wide between the 15 chamfers at z 2300)",
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
