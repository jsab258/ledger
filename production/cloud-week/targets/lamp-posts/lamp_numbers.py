"""The registry of every number the lamp-post target uses: id -> (value, unit, kind, source). Try 2 (11 October 2026): the review of 9 October applied.

Kinds: Read (printed in the repository or in a file this writer opened), Photo (measured on a photograph: method and error in TARGET.md section 4),
Derived (computed from other numbers here; the formula is in `source`), Judgement (a trade or period guess, said so).
Lengths are millimetres unless the unit says otherwise. make_target.py copies the whole registry into target.json `numbers`; self_check.py
re-reads the Read ones from their files and recomputes the Derived ones."""
import math

REG = {}


def _r(id_, value, unit, kind, source):
    assert id_ not in REG, id_
    REG[id_] = {"value": value, "unit": unit, "kind": kind, "source": source}


SCENE = "production/specs/vignette-scene.json lighting.column / lighting.lantern (read 9 October 2026)"
CODE = "ledger/Assets/Scripts/Core/StreetVignette.cs Columns() lines 1196 to 1262 (read 9 October 2026)"
NIGHT = "production/cloud-week/research/1c-night-pools-lumen.md (read 9 October 2026)"
CLUT = "production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 3 (the project's earlier reading)"
BGE = "Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json"
US1 = "Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json"

# ---- the scene's stand-in (Read) ------------------------------------------------------------------------------------------------------
_r("scene_mounting_height", 5000, "mm", "Read", SCENE + ": mounting_height_m 5.0")
_r("scene_spacing_ratio", 4.0, "x mounting height", "Read", SCENE + ": spacing_per_mounting_height 4.0")
_r("scene_first_offset", 8000, "mm", "Read", SCENE + ": first_offset_m 8.0")
_r("scene_setback", 600, "mm", "Read", SCENE + ": setback_from_kerb_m 0.6 (from the kerb's back face: FootwayFrontZ = 3.0 + 0.125 = 3.125, column z 3.725)")
_r("scene_base_diameter", 200, "mm", "Read", SCENE + ": base_diameter_m 0.2")
_r("scene_base_height", 300, "mm", "Read", SCENE + ": base_height_m 0.3")
_r("scene_shaft_diameter", 114, "mm", "Read", SCENE + ": shaft_diameter_m 0.114 (the stand-in's shaft is one 114 tube from z 300 to 5000)")
_r("scene_outreach", 500, "mm", "Read", SCENE + ": outreach_m 0.5 (the lantern's CENTRE is 0.5 from the shaft axis: CODE z - sgn * reach)")
_r("scene_lantern_length", 550, "mm", "Read", SCENE + ": lantern.length_m 0.55 (the stand-in lays it ALONG the street: SX)")
_r("scene_lantern_width", 300, "mm", "Read", SCENE + ": lantern.width_m 0.3")
_r("scene_lantern_height", 200, "mm", "Read", SCENE + ": lantern.height_m 0.2 (the stand-in's lantern TOP is at the mounting height, its centre 100 below)")
_r("scene_wavelength_nm", 589, "nm", "Read", SCENE + ": lantern.wavelength_nm 589")
_r("scene_lantern_linear_srgb", [1.0, 0.7055, 0.0], "linear", "Read", SCENE + ": lantern.linear_srgb (see derived_589_linear: this triple is not 589 nm)")
_r("scene_lantern_gamma_srgb", [1.0, 0.8573, 0.0], "gamma sRGB", "Read", SCENE + ": lantern.gamma_srgb")
_r("scene_lantern_xy", [0.5467, 0.4526], "CIE 1931", "Read", SCENE + ": lantern.cie_1931_xy")
_r("scene_lantern_range", 18.0, "m", "Read", SCENE + ": lantern.range_m 18.0")
_r("scene_point_light_drop", 50, "mm", "Read", "production/specs/vignette-pieces.json lantern.placement: one point light 0.05 m below the centre of each emissive piece")
_r("scene_street_length", 48.0, "m", "Read", "production/specs/vignette-scene.json street.length_m 48.0")
_r("scene_column_x", [8.0, 18.0, 28.0, 38.0], "m", "Read", "production/specs/vignette-pieces.json column0..3_base x_m; the same list the code gives: x = 8 while x <= 48 - 8 x 0.25, step spacing x 0.5 = 10 m")
_r("scene_column_z", [3.725, -3.725, 3.725, -3.725], "m", "Read", "production/specs/vignette-pieces.json column0..3_base z_m (east is +z); sides east, west, east, west")
_r("scene_kerb_half_width", 3.0, "m", "Read", "production/specs/vignette-scene.json street.carriageway.half_width_m")
_r("scene_kerb_width", 0.125, "m", "Read", "production/specs/vignette-scene.json street.kerb.width_m (the corrected granite kerb top is 170: kerbs-and-covers target)")
_r("scene_neck_diameter_ratio", 0.8, "x shaft", "Read", CODE + ": SX = sd * 0.8")
_r("scene_neck_pieces", 3, "cylinders on a quarter circle", "Read", CODE + ": the swan neck, three short cylinders on a quarter circle")
_r("kerbs_granite_top_width", 170, "mm", "Read", "production/cloud-week/targets/kerbs-and-covers/target.json (granite kerb top width 170, upstand 115, flags +110 above the channel)")
_r("kerbs_flag_level_above_channel", 110, "mm", "Read", "production/cloud-week/targets/kerbs-and-covers/TARGET.md frame: footway flags +110")

# ---- the night note (Read) -------------------------------------------------------------------------------------------------------------
_r("lamp_lumens_35w_sox", 4550, "lm", "Read", NIGHT + " section 2: SOX 35 W gives 4,550 lm (a maker's datasheet, search summary in the note: [SS])")
_r("night_current_pool_lumens", 500, "lm", "Read", NIGHT + " section 2 and DECISIONS 8 October 11:45: lantern_pool_lumens 750 -> 500")
_r("night_current_pool_outer_deg", 46, "deg", "Read", NIGHT + " section 2: 500 lm at 46 degrees is 261 cd, 11.4 lx straight down from 4.78 m")
_r("night_current_pool_inner_deg", 22, "deg", "Read", NIGHT + " section 3 item 3: inner cone 22 degrees")
_r("night_current_glow_lumens", 40, "lm", "Read", NIGHT + " section 3 item 1: glow 40 lm, 3.2 cd, unshadowed; DECISIONS 7 October: the glow casts no shadows")
_r("night_current_height_above_ground", 4.78, "m", "Read", NIGHT + " section 2: 4.78 m (the note's own figure for the lamp's height above the ground)")
_r("night_current_peak_lux", 11.4, "lx", "Read", NIGHT + " section 2")
_r("night_current_lamp_linear", [1.0, 0.25, 0.0], "linear", "Read", NIGHT + " section 3 item 2: the lamp (1.0, 0.25, 0.0): red 4 times green")
_r("night_try_lamp_linear", [1.0, 0.40, 0.03], "linear", "Read", NIGHT + " section 4 step 5: lamp colour try (1.0, 0.40, 0.03), red to green 2.5, one number")
_r("night_skirt_lumens", 800, "lm", "Read", NIGHT + " section 4 step 4: unshadowed spot, straight down, 800 lm, inner 45, outer 80 degrees")
_r("night_skirt_inner_deg", 45, "deg", "Read", NIGHT + " section 4 step 4")
_r("night_skirt_outer_deg", 80, "deg", "Read", NIGHT + " section 4 step 4")
_r("night_proposed_pool_lumens", 350, "lm", "Read", NIGHT + " section 4 step 4: drop the pool spot 500 to 350 lm; make the cone 15 and 55")
_r("night_proposed_pool_inner_deg", 15, "deg", "Read", NIGHT + " section 4 step 4")
_r("night_proposed_pool_outer_deg", 55, "deg", "Read", NIGHT + " section 4 step 4")
_r("night_proposed_peak_lux", 12.5, "lx", "Read", NIGHT + " section 4 step 4: peak about 12.5 lx (now 11.4)")
_r("night_source_radius", [50, 100], "mm", "Read", NIGHT + " section 4 step 4: source radius 5 to 10 cm")

# ---- the earlier research on the type (Read) ------------------------------------------------------------------------------------------
_r("research_column_height_range", [4600, 6000], "mm", "Read", CLUT + ": Column 4.6 to 6 m (uncertain for any given street)")
_r("research_foot_width_range", [200, 250], "mm", "Read", CLUT + ": a tapered shaft ... 20 to 25 cm at the foot (precast concrete variant)")
_r("research_door_height_about", 500, "mm", "Read", CLUT + ": with a door plate about 50 cm up (uncertain detail)")
_r("research_bracket_reach_range", [406, 457], "mm", "Read", CLUT + ": bracket reaching out 1 ft 4 in to 1 ft 6 in (the 1958 example column); modelling note: an arm reaching out 40 to 45 cm")
_r("research_lantern_height", 197, "mm", "Read", CLUT + ": Lantern: 7 3/4 in (20 cm) tall on the early version")
_r("research_lantern_length_estimate", [600, 700], "mm", "Read", CLUT + ": length not found; estimate 60 to 70 cm (uncertain); the scene's 550 is kept")
_r("research_lamp_power", 35, "W", "Read", CLUT + ": usually 35 W SOX")

# ---- BGE column (Photo) ----------------------------------------------------------------------------------------------------------------
_r("bge_camera_height", 1.02, "m", "Read", "production/cloud-week/targets/bollards/TARGET.md section 3: bethnal_green_entrance 1.02 +-0.07 m (reviewer 1.03 to 1.04; the bollards' writer 0.96)")
_r("bge_sleeve_od_measured", 123.6, "mm", "Photo", BGE + ": left and right edges at z 100 to 800 each 100 mm, mean of 8 rows (120 to 128); +-9 (scale +-7 %, edges +-3)")
_r("bge_sleeve_top_z", 978, "mm", "Photo", BGE + ": the sleeve's straight side ends at z 978 (+-10) where the cone begins (read on the 4 x gridded crop)")
_r("bge_cone_top_z", 1040, "mm", "Photo", BGE + ": the cone meets the shaft at z 1040 (+-10), a thin ring line there")
_r("bge_shaft_od_low", 68, "mm", "Photo", BGE + ": 67 at z 1700, 69 at 1800 and 1900 (strong edges against brick), 66 read by eye at z 1100; +-6")
_r("bge_shaft_od_high", 61, "mm", "Photo", BGE + ": 61 at z 3800, 3900 and 4000 (strong edges against the sky); +-5")
_r("bge_pod_diameter_measured", 417, "mm", "Photo", BGE + ": widest run of the pod's silhouette against the sky, 417 (x -193 to +223); +-30")
_r("bge_pod_centre_height", 4410, "mm", "Photo", BGE + ": from the angles of the pod's limbs (el 53.8 and 48.5 degrees) at the axis distance 2.73 m: 4.41 m; +-300")
_r("bge_paint_black_srgb", [31, 31, 33], "sRGB", "Photo", BGE + ": median of the sleeve's face, z 500 to 900 (p10 19, p90 44; the gloss highlights reach 69 to 75)")
_r("bge_splash_srgb", [49, 46, 42], "sRGB", "Photo", BGE + ": median of the lowest 250 mm of the sleeve (warm grey-brown road film over the black; p10 34, p90 77)")
_r("bge_scratch_zone", [380, 430], "mm", "Photo", BGE + ": hairline scratches on the sleeve's face at z 380 to 430, no letters")
_r("bge_plate_z", 2160, "mm", "Photo", BGE + ": a small white plate with a short letter-and-number reference at z 2115 to 2200 on the shaft, about 125 x 85 in the picture")

# ---- US01 column (Photo, ratios only) ---------------------------------------------------------------------------------------------------
_r("us01_shaft_top_od", 89.1, "mm", "Photo", US1 + ": mean width of the shaft's top 0.9 m against the sky, z 8900 to 9700: 86 to 96; +-8 (a taller class: 11 m)")
_r("us01_stem_od", 42.0, "mm", "Photo", US1 + ": the vertical stem above the shaft's collar at z 9800 to 10000: 38 to 46; +-5")
_r("us01_arm_od", 59.9, "mm", "Photo", US1 + ": the raked arm's thickness taken vertically 80, times cos(slope 43.6 degrees seen in the picture): 60 (the slope is not the rake; the arm points partly out of the plane)")
_r("us01_arm_to_shaft_ratio", 0.67, "ratio", "Photo", US1 + ": arm 59.9 / shaft top 89.1; the stem 42.0 / 89.1 = 0.47 (the two disagree because the arm is foreshortened); kept as a range 0.47 to 0.67")
_r("us01_sleeve_to_shaft_ratio", 2.05, "ratio", "Photo", US1 + ": sleeve 232 / shaft 113 read by eye on the gridded elevation (8.8 m): a stepped column, the same form as BGE (BGE's ratio is 1.8)")
_r("us01_lit_median_srgb", [251, 152, 14], "sRGB", "Photo", US1 + ": median of the 66,611 orange pixels of the lit lantern seen from below (p10 229/105/0, p90 255/208/77); the brightest 200 pixels (252, 251, 180) are the clipped core")

# ---- the target's own numbers: shared lower column (Photo-led) ----------------------------------------------------------------------------
_r("sleeve_od", 124, "mm", "Photo", "BGE sleeve 123.6 +-9, rounded to 124 (the scene's 114 lies at its lower edge: kept as a tolerance, not as the value; 114.3 is a standard tube)")
_r("sleeve_height", 978, "mm", "Photo", "BGE sleeve top 978 +-10")
_r("cone_top", 1038, "mm", "Photo", "BGE cone top 1035 to 1040 (+-10)")
_r("shaft_od_at_cone", 68, "mm", "Photo", "BGE shaft 66 to 69 at z 1100 to 1900")
_r("shaft_od_at_top", 60, "mm", "Derived", "linear taper from 68 at z 1044 to 61 at z 3900 (BGE), carried to z 4560, where the taper line ends inside the socket: 68 - 7 x (4560 - 1044) / (3900 - 1044) = 59.4; set to 60 (60.3 is a standard 2 in tube)")
_r("socket_top_z", 4620, "mm", "Judgement", "the socket's top and the shaft's end (variant A): the 250 mm socket sleeve of the bracket stands from z 4370 to 4620 (review point 1: US01's shaft top is the bracket's socket sleeve, about 450 mm long on that 11 m column, no step a 7 mm pixel can see, a flat top with a small chamfer into the stem); the stem rises from inside it to z 4800.8")
_r("socket_bottom_z", 4370, "mm", "Judgement", "review point 1: socket z 4370 to 4620 (250 long)")
_r("socket_od", 64, "mm", "Judgement", "review point 1: socket OD 64 (2 proud of a 62 shaft: with the shaft left at its measured taper, 60.2 at z 4370, it stands 3.8 proud, which a 7 mm pixel cannot see either way)")
_r("socket_top_chamfer", 3, "mm", "Judgement", "review point 1: the socket's top edge chamfered 3")
_r("socket_screw_z", [4580, 4420], "mm", "Judgement", "review point 1: two M8 set screws one above the other on -y at z 4580 and 4420 (US01: two set screws one above the other on one side)")
_r("weld_ring_height", 6, "mm", "Photo", "BGE: a thin ring line at the cone's top, z 1036 to 1042 (read by eye on the 4 x crop)")

# ---- bracket (Photo ratios, Read reach, Judgement) ----------------------------------------------------------------------------------
_r("stem_od", 42, "mm", "Judgement", "ratio to the shaft top 0.47 to 0.67 (US01 Photo) x 60 = 28 to 40; 42.4 is a standard 1.25 in tube; the arm to the shaft's top 0.7 here because a 5 m column's top is slim (variant A; variant C's stem is 48)")
_r("stem_od_c", 48, "mm", "Judgement", "variant C's steel stem OD 48 (the review's F2 amendment; 48.3 is a standard 1.5 in tube)")
_r("us01_arm_apparent_slope_deg", 41.7, "deg", "Photo", US1 + ": the straight arm's centreline fitted over x -1150 to -350 of the elevation: slope -0.890, 41.7 degrees in the picture's plane (43.6 over x -1500 to -500); +-2. NOT the true rake: the arm points 35 to 42 degrees out of the picture's plane toward the camera (see us01_street_vp), where a level arm shows 36 to 42 degrees of rise")
_r("us01_bend_tangent_lengths", [147, 244], "mm", "Photo", US1 + ": from the corner where the stem's line meets the arm's line, the centreline leaves the stem 147 mm below it and rejoins the arm 244 mm along it; +-40 (apparent, in the picture's plane; superseded by the 3D reading)")
_r("us01_bend_radius", 435, "mm", "Photo", US1 + ": R = mean tangent length 195 / tan(24 degrees) = 435 in the picture's plane (apparent turn 48.3 degrees); about 9 arm diameters on an 11 m column; superseded: the true turn is about 90 degrees")
_r("us01_reach_to_boss", 1117, "mm", "Photo", US1 + ": from the stem's axis to the arm's end at the lantern's rear boss, in the picture's plane; +-100 (apparent; the arm points toward the camera, so its true reach is longer)")
_r("rake_deg", 0, "deg", "Photo", "review fault 1 (9 October): US01's apparent 41.7 degrees is mostly perspective (the arm points 35 to 42 degrees toward the camera, the camera looks up 45 degrees); read in 3D the true rake is 0 to 7 and the lantern lies on the arm's line; period photographs of 1989 (Orrell and Appley Bridge stations, Peter Whatley) show near-level arms with the lantern in line; a lead says 5 m brackets had a vertical and a horizontal section: 0 +-5")
_r("bend_turn_deg", 90, "deg", "Judgement", "review fault 1: one bend of 90 degrees from the vertical stem to the level arm")
_r("bend_radius", 130, "mm", "Judgement", "review fault 1: centreline radius 130 (3 tube diameters of 42 = 126, rounded)")
_r("bracket_reach_to_spigot", 430, "mm", "Read", CLUT + ": bracket reaching out 1 ft 4 in to 1 ft 6 in (406 to 457) and 'an arm reaching out 40 to 45 cm'; review fault 3: 430 from the shaft's axis to the lantern's rear spigot (the old 225 halved it)")
_r("arm_axis_z", 4930.8, "mm", "Judgement", "the arm's centreline height: inside the canopy lip band (z 4925 to 4937) so the boss is cast on the canopy's rear tip (review fault 1: the arm runs level at z 4930.8)")
_r("stem_top_z", 4800.8, "mm", "Derived", "arm_axis_z 4930.8 - bend_radius 130 = 4800.8: where the vertical stem ends and the 90 degree bend begins (review fault 1)")
_r("arm_length", 300, "mm", "Derived", "bracket_reach_to_spigot 430 - bend_radius 130 = 300: the straight level arm from (130, 4930.8) to (430, 4930.8)")
_r("lantern_dy", 205, "mm", "Derived", "430 - 225: every y station of the lantern moves 205 further out (review fault 3)")
_r("lantern_centre_outreach", 705, "mm", "Derived", "the lantern's centre: rear end 430 + half its length 275 = 705 (the scene's 0.5 was a trade-standard guess, the earlier research's 406 to 457 is the reach to the spigot, review fault 3); the scene's outreach_m becomes 0.705")
_r("lantern_rear_end_y", 430, "mm", "Read", "= bracket_reach_to_spigot: the lantern's rear end is the spigot (the boss starts here)")
_r("lantern_front_end_y", 980, "mm", "Derived", "lantern rear end 430 + length 550")
_r("boss_od", 60, "mm", "Judgement", "the lantern's rear spigot sleeve, cast into the canopy")
_r("boss_length", 55, "mm", "Judgement", "the arm's end sits inside the boss")

# ---- lantern ---------------------------------------------------------------------------------------------------------------------------
_r("lantern_length", 550, "mm", "Read", "scene 0.55: kept (the research's 600 to 700 is an estimate flagged uncertain)")
_r("lantern_width", 300, "mm", "Read", "scene 0.30")
_r("lantern_height", 200, "mm", "Read", "scene 0.20 (the research's 7 3/4 in = 197 agrees)")
_r("lantern_bottom_z", 4800, "mm", "Read", "scene: lantern top at the mounting height 5000, 200 tall")
_r("lantern_top_z", 5000, "mm", "Read", "scene: mounting height 5.0 m")
_r("canopy_rim_z", 4925, "mm", "Judgement", "canopy 75 above its rim, bowl 125 below it: the earlier research's 'boat-shaped canopy over a deep clear trough-shaped bowl'")
_r("canopy_lip_height", 12, "mm", "Judgement", "the canopy's down-turned rim")
_r("bowl_rim_inset", 8, "mm", "Judgement", "the bowl's rim sits inside the canopy's lip")
_r("lamp_od", 54, "mm", "Judgement", "a 35 W low-pressure sodium lamp: about 54 mm across and 310 mm long (a maker's datasheet recalled from memory, not read here)")
_r("lamp_length", 310, "mm", "Judgement", "as above")
_r("lamp_centre_z", 4872, "mm", "Judgement", "the lamp lies along the lantern's axis in the bowl's upper half")
_r("lamp_centre_y", 705, "mm", "Derived", "the lantern's centre (rear end 430 + 275)")
_r("light_z", 4850, "mm", "Derived", "the lantern's centre z (4900) minus the scene's rule 50 below the centre of the emissive piece; y is the lantern's centre 705")

# ---- colours ----------------------------------------------------------------------------------------------------------------------------
_r("paint_black_srgb", [31, 31, 34], "sRGB", "Photo", "BGE sleeve median 31/31/33 and US01 sleeve 32/33/38 (the sky tints the shaft): 31/31/34")
_r("splash_srgb", [49, 46, 42], "sRGB", "Photo", "BGE lowest 250 mm")
_r("primer_srgb", [112, 110, 106], "sRGB", "Judgement", "grey primer showing in chips (US01 shows pale grey patches at the shoulder and top edge, qualitative)")
_r("rust_srgb", [94, 58, 40], "sRGB", "Judgement", "rust-brown bleed")
_r("canopy_srgb", [118, 116, 112], "sRGB", "Judgement", "weathered painted aluminium, mid grey, slightly warm; US01's canopy seen from below is a dark grey-brown in shade (about 110/90/85)")
_r("bowl_unlit_srgb", [190, 182, 160], "sRGB", "Judgement", "yellowed clear acrylic, seen against the lamp and the white reflector")
_r("reflector_srgb", [226, 224, 216], "sRGB", "Judgement", "white-painted reflector inside the canopy")
_r("glow_bowl_srgb", [255, 137, 0], "sRGB", "Derived", "the night note's lamp (1.0, 0.25, 0.0) linear gamma-encoded: 1.0, 0.537, 0.0; the photograph's lit lantern median 251/152/14 is 15 higher in green")
_r("glow_lamp_srgb", [255, 137, 0], "sRGB", "Derived", "review point 5: a sodium lamp's own light is one orange, so the jacket is (255, 137, 0) at full strength like the bowl; the photograph's yellow core (252/251/180) is the camera's clipping and is left to the grade (the night note's step 2), not modelled as a colour")
_r("plate_white_srgb", [214, 212, 205], "sRGB", "Judgement", "enamel reference plate, aged white")
_r("plate_black_srgb", [30, 30, 32], "sRGB", "Judgement", "the plate's letters")
_r("concrete_srgb", [146, 143, 136], "sRGB", "Judgement", "weathered precast concrete (variant C only)")


# ---- variant C: the precast concrete column, the main build (review fault 2) ----------------------------------------------------------
_r("c_foot_side", 220, "mm", "Judgement", "the research's '20 to 25 cm at the foot' (Read) taken at 220: a square section, planted (review F2)")
_r("c_top_side", 125, "mm", "Judgement", "review F2: 125 across at the top (z 4620); a taper of 20 mm a metre across the faces")
_r("c_top_z", 4620, "mm", "Judgement", "the top face; the same as variant A's shaft end, so the arm and lantern stand at the same heights on either")
_r("c_arris_chamfer", 15, "mm", "Judgement", "review F2: arrises chamfered 15 throughout")
_r("c_top_face_chamfer", 5, "mm", "Judgement", "review F2: the top face flat with a 5 mm chamfer")
_r("c_hidden_root", 150, "mm", "Judgement", "planted: 150 hidden below the footway as variant A's skirt, the paving cut round it")
_r("c_cap_od", 90, "mm", "Judgement", "review F2: a cast-steel cap 90 OD, 30 tall, seated on the top face")
_r("c_cap_height", 30, "mm", "Judgement", "review F2")
_r("c_door_recess", {"width": 120, "height": 330, "depth": 14, "z": [450, 780]}, "mm", "Judgement", "review F2: the recess 120 x 330 x 14 at z 450 to 780 on -y (the research: 'a door plate about 50 cm up')")
_r("c_door_plate", {"width": 132, "height": 342, "thickness": 3, "proud": 3, "screws": 2, "screw_od": 10, "screw_inset": 25}, "mm", "Judgement", "review F2: the plate 132 x 342 x 3, 3 proud, two screws 10 across at 25 from its ends, blank")
_r("c_albedo_srgb", [146, 143, 136], "sRGB", "Judgement", "weathered precast concrete (variant C)")
_r("c_roughness", 0.9, "0-1", "Judgement", "rough matt concrete")

# ---- emissive strength in units (review point 4) ----------------------------------------------------------------------------------------
_r("emissive_jacket_cd_m2", 27500, "cd/m2", "Derived", "4,550 lm / (pi x 0.0526 m2 of jacket surface: pi x 0.054 x 0.310) = 27,535: about 27,500 (review point 4)")
_r("emissive_bowl_cd_m2", 5500, "cd/m2", "Derived", "80 % of the flux (3,640 lm) through about 0.21 m2 of bowl, Lambertian: 3,640 / (pi x 0.21) = 5,517: about 5,500 (review point 4)")
_r("emissive_jacket_over_tube", 0.3, "ratio", "Judgement", "review point 3: the arc tube is the full-strength emissive part and the jacket glass glows at 0.3 of it; so the tube is 27,500 / 0.3 = 91,700 cd/m2 in the same units (stated, not measured)")
_r("emissive_unitless_fallback", 1.0, "unitless", "Read", "ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp line 203: kLampEmissiveUnitless = 1.0 times the lantern colour in linear (1.0, 0.25, 0.0) until the night audit puts the glow in units: the units above are the target; the builder may use the rule instead and say so")


# ---- derived numbers: filled by make_target.py (and recomputed by self_check.py) ------------------------------------------------------
def derive():
    """Return the derived numbers as a dict id -> {value, unit, kind, source}."""
    d = {}

    def put(id_, v, u, src):
        d[id_] = {"value": v, "unit": u, "kind": "Derived", "source": src}
    # CIE 1931 colour matching functions: the multi-lobe Gaussian fit of Wyman, Sloan and Shirley (2013), recalled from memory; its 585 nm value
    # (0.5436, 0.4562) is within 0.002 of the printed table's (0.5448, 0.4544): a check that the fit is the fit
    def g(l, mu, s1, s2):
        s = s1 if l < mu else s2
        return math.exp(-0.5 * ((l - mu) / s) ** 2)

    def cmf(l):
        x = 1.056 * g(l, 599.8, 37.9, 31.0) + 0.362 * g(l, 442.0, 16.0, 26.7) - 0.065 * g(l, 501.1, 20.4, 26.2)
        y = 0.821 * g(l, 568.8, 46.9, 40.5) + 0.286 * g(l, 530.9, 16.3, 31.1)
        z = 1.217 * g(l, 437.0, 11.8, 36.0) + 0.681 * g(l, 459.0, 26.0, 13.8)
        return x, y, z

    def xy(l):
        x, y, z = cmf(l)
        s = x + y + z
        return x / s, y / s
    x585, y585 = xy(585.0)
    x589, y589 = xy(589.0)
    X = Y = Z = 0.0
    for l in (589.0, 589.6):
        a, b, c = cmf(l)
        X += a
        Y += b
        Z += c
    dxy = (X / (X + Y + Z), Y / (X + Y + Z))
    put("derived_xy_585", [round(x585, 4), round(y585, 4)], "CIE 1931", "fit of the colour matching functions at 585 nm (compare the scene's 0.5467, 0.4526)")
    put("derived_xy_589", [round(x589, 4), round(y589, 4)], "CIE 1931", "fit at 589.0 nm")
    put("derived_xy_d_lines", [round(dxy[0], 4), round(dxy[1], 4)], "CIE 1931", "equal-weight mean of the sodium D lines at 589.0 and 589.6 nm: (0.5684, 0.4315); the evening note's 0.569, 0.430 agrees")

    def rgb(x, y):
        XYZ = [x / y, 1.0, (1 - x - y) / y]
        M = [[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]
        return [sum(M[i][j] * XYZ[j] for j in range(3)) for i in range(3)]
    raw_scene = rgb(0.5467, 0.4526)
    raw_589 = rgb(dxy[0], dxy[1])
    put("derived_scene_raw_linear", [round(v, 4) for v in raw_scene], "linear sRGB, unclipped", "the scene's xy through the sRGB D65 matrix: (2.3766, 0.7055, -0.1351), as the scene's note says")
    put("derived_scene_clipped_normalised", [round(max(v, 0) / max(raw_scene), 4) for v in raw_scene], "linear",
        "clip the negative blue and divide by the peak 2.3766 -> (1, 0.2969, 0): the scene's (1, 0.7055, 0) skipped the division in green")

    def enc(c):
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    c589 = [max(v, 0) / max(raw_589) for v in raw_589]
    put("derived_589_linear", [round(v, 4) for v in c589], "linear", "589 nm (D lines) through the same matrix, clipped and divided by its peak 2.7312: (1, 0.2195, 0)")
    put("derived_589_gamma_8bit", [round(255 * enc(v)) for v in c589], "sRGB 8 bit", "the same, gamma-encoded: 255, 129, 0 (the evening note's 255, 140, 0)")
    # photometry: cd = lm / (2 pi (1 - cos outer half angle)); lux straight down = cd / h^2
    def cd(lm, outer):
        return lm / (2 * math.pi * (1 - math.cos(math.radians(outer))))
    h = REG["night_current_height_above_ground"]["value"]
    put("cd_current_pool", round(cd(500, 46), 1), "cd", "500 lm / (2 pi (1 - cos 46 deg)) = 260.7: the night note's 261")
    put("lux_current_pool", round(cd(500, 46) / h ** 2, 2), "lx", "261 cd / 4.78 m squared = 11.41: the night note's 11.4")
    put("cd_proposed_pool", round(cd(350, 55), 1), "cd", "350 lm / (2 pi (1 - cos 55 deg)) = 130.6")
    put("cd_skirt", round(cd(800, 80), 1), "cd", "800 lm / (2 pi (1 - cos 80 deg)) = 154.1")
    put("lux_proposed_peak", round((cd(350, 55) + cd(800, 80)) / h ** 2, 2), "lx", "(130.6 + 154.1) / 4.78 squared = 12.46: the night note's 'about 12.5 lx'")
    put("proposed_total_lumens", 350 + 800 + 40, "lm", "pool 350 + skirt 800 + glow 40 = 1190 lm, 26 % of the lamp's 4,550 lm (the night note cut the pool on purpose; see TARGET.md section 8)")
    put("proposed_share_of_lamp", round((350 + 800 + 40) / 4550, 3), "ratio", "1190 / 4550")
    return d
