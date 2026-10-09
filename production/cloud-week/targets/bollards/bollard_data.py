"""All the hand-read numbers of the bollards family (cloud week 42, 9 October 2026), in one place.

make_target.py turns them into target.json; make_previews.py cuts the preview pictures from the Poly Haven panoramas.
Units: millimetres, profiles are (r, z): r the radius from the axis, z up from the ground at the foot (the pivot).
Readings were made on re-projected, square-on elevations of each bollard (a vertical plane through its axis, 1 mm a pixel)
and are therefore proportional to the camera height assumed for the panorama (h_read); the final numbers multiply
every r and z by h_cam / h_read.
"""

# ------------------------------------------------------------------------------------------------------------
# the photographs: Poly Haven CC0 panoramas (Andreas Mischok), 8k tone-mapped JPG, camera height CALIBRATED per panorama
# ------------------------------------------------------------------------------------------------------------
PANOS = {
    'urban_street_01': dict(date_taken='2019-08-18 07:09 UTC', coords=(51.528295, -0.053879), h_cam=1.16, h_cam_err=0.06,
                            h_why='brick course gauge 75 mm on the garden wall behind the bollard (rectified: 75 to 76 mm at 1.15 m, so 1.13 to 1.15); '
                                  'the single yellow line (98 mm at 1.6 m, so 75 mm at 1.22 m); mean 1.16'),
    'bethnal_green_entrance': dict(date_taken='2019-08-18 07:01 UTC', coords=(51.526915, -0.054044), h_cam=1.02, h_cam_err=0.08,
                                   h_why='brick course gauge 75 mm on the gate pier and its blue plinth (rectified 92 mm at 1.15 m, so 0.94; stretcher module 255 mm for 225, so 1.02); '
                                         'taken as 1.02'),
    'birbeck_street_underpass': dict(date_taken='2019-08-18 06:53 UTC', coords=(51.525806, -0.056277), h_cam=1.22, h_cam_err=0.10,
                                     h_why='the double yellow line (each line 97 mm at 1.6 m, so 75 mm at 1.24 m); no second anchor'),
    'urban_street_02': dict(date_taken='2019-08-18 06:45 UTC', coords=(51.526655, -0.056465), h_cam=1.15, h_cam_err=0.12,
                            h_why='no anchor of its own (the brick wall gave 0.84 to 0.9 but its bricks are not a 75 mm gauge); the pooled value 1.15 is used; '
                                  'it makes this K2 bollard 1188 high, the same as the Birbeck one (1186) read at its own calibrated 1.22'),
    'limehouse': dict(date_taken='2019-05-19 15:45 UTC', coords=(51.510606, -0.036324), h_cam=1.17, h_cam_err=0.06,
                      h_why='the clay brick paviors: course pitch 146 mm and stretcher 280 mm at 1.6 m against 105 and 205 (a 200 x 100 paver with a 5 mm joint): 1.15 and 1.17; taken as 1.17'),
}

# the five bollards measured
FRAMES = {
    'US01_b': dict(pano='urban_street_01', kind='K1', psi=12.670, depr=28.801, R=97.0, h_read=1.15, yaw_view=12.6,
                   what='a cast-iron domed bollard in a kerb build-out, the big collar at 0.5 H'),
    'BGE_a': dict(pano='bethnal_green_entrance', kind='K1', psi=67.342, depr=23.858, R=102.0, h_read=1.15,
                  what='the same family on block paving, paint lost from the foot'),
    'BB_b': dict(pano='birbeck_street_underpass', kind='K2', psi=-24.711, depr=18.370, R=128.0, h_read=1.15,
                 what='a plain tapered iron bollard, grey, flat top, rolled foot ring'),
    'US02_a': dict(pano='urban_street_02', kind='K2', psi=-148.800, depr=9.477, R=132.0, h_read=1.15,
                   what='the plain tapered bollard in black with a low cone cap, on flags 0.6 m behind the kerb'),
    'LH_b': dict(pano='limehouse', kind='K5', psi=-59.492, depr=36.562, R=143.0, h_read=1.17,
                 what='a bolted chain post at a marina edge'),
}

# ------------------------------------------------------------------------------------------------------------
# profiles, as READ (r, z) at the reading scale h_read; bottom (0,0) up the outline to the axis at the top
# ------------------------------------------------------------------------------------------------------------
K1_READ = [  # US01_b
    (0, 0), (94, 0), (97, 3), (97, 116), (95.5, 121), (92, 124), (78.4, 134),
    (68.3, 493),                                                                    # one straight taper from 134 to 493
    (72.5, 497), (78, 505), (81.5, 516), (82.5, 527), (81, 538), (76.5, 548), (70.5, 554), (66.6, 557),   # the bead
    (57.0, 900), (54.5, 915), (53.0, 930), (53.0, 940),                             # taper, then the neck
    (60, 943), (66.5, 947), (67.5, 953), (67, 960), (63, 965), (58.5, 968),         # the cap collar, rounded
    (58, 972), (58.5, 980), (58.5, 987),                                            # the groove and the thin ring
    (51, 988), (50, 1000), (47.5, 1012), (43, 1024), (36, 1032), (26, 1037), (14, 1040), (0, 1041),       # the flattened dome
]
K2_R_FACTOR = 1.035   # r only: after the first overlay the left edge was 8 mm out and the right 1 mm, over the whole height (a reading error of +3.5 % in r)
K2_READ_RAW = [  # BB_b, as first read
    (0, 0), (122, 0), (127, 4), (128, 12), (126, 22), (121, 32), (114, 40), (111, 46),   # rolled foot ring
    (85, 635),                                                                           # straight taper
    (88, 640), (92, 646), (93.5, 654), (93, 660), (90, 666), (86, 670), (84.5, 672),     # the collar band
    (71, 1050), (70.5, 1088),                                                            # upper shaft, a gentler taper
    (75, 1092), (76.5, 1096), (76.5, 1104), (72, 1109), (60, 1111), (30, 1112), (0, 1112.5),  # flat cap plate, slightly domed
]
K2_READ = [(round(r * K2_R_FACTOR, 2), z) for r, z in K2_READ_RAW]
K5_READ = [  # LH_b
    (0, 0), (143, 0), (143, 36), (141, 40), (125, 50), (105, 72), (95, 90), (91, 100),     # the bolted flange and its sloped top
    (91, 278),
    (95, 285), (101, 297), (105, 315), (105, 335), (103, 352), (98, 372), (92, 390), (90, 398),   # the lower bead
    (87, 600), (86, 868),
    (93, 874), (100, 888), (101, 900), (98, 915), (90, 922), (88, 926),                   # the upper bead and its fillet ring
    (80, 932), (80, 1000),                                                                # the neck
    (90, 1012), (102, 1028), (107, 1042), (106, 1055), (100, 1066), (92, 1072), (84, 1075),  # the cap collar
    (84, 1090), (62, 1095), (58, 1108), (48, 1120), (30, 1130), (14, 1134), (0, 1135),    # the step and the dome
]
# the second K2 top, read on US02_a (final scale): from the shaft top up, replacing the flat plate
K2B_TOP_FINAL = [(72, 1100), (72, 1135), (79.5, 1148), (80, 1160), (76, 1166), (50, 1178), (25, 1184), (0, 1188)]

# eyeballed readings on the gridded elevations (z, left t, right t) at h_read, kept for self_check B
READINGS = {
    'US01_b': [(10, -99, 96), (60, -100, 96), (100, -100, 96), (150, -75, 80), (200, -73, 80), (400, -65, 75), (450, -59, 78),
               (520, -71, 93), (570, -55, 78), (600, -54, 77), (670, -50, 74), (700, -49, 77), (900, -41, 73), (930, -33, 73),
               (950, -46, 88), (980, -38, 78)],
    'BB_b': [(100, -107, 113), (640, -80, 91), (654, -88, 98), (700, -82, 85), (950, -67, 77), (1050, -66, 77)],
    'LH_b': [(200, -90, 92), (330, -102, 108), (450, -87, 93), (600, -82, 93), (850, -80, 92), (900, -92, 108), (960, -70, 89),
             (1042, -98, 117)],
}

# the BGE_a second reading by thresholding (z, half width) at h_read 1.15, used only to compare with US01_b
BGE_A_HALFWIDTH = [(200, 79.5), (240, 77.5), (320, 76.5), (360, 75.0), (400, 74.0), (440, 72.5), (480, 71.5), (520, 71.0),
                   (560, 70.0), (640, 68.0), (680, 67.5), (720, 66.5), (760, 65.5), (800, 64.5), (840, 63.0)]
BGE_A_TOP_Z_READ = 1143.0    # top of the dome at h_read 1.15
BGE_A_BASE_R_READ = 102.0

# ------------------------------------------------------------------------------------------------------------
# the street, READ from the repository (each with the file and the words to find in it)
# ------------------------------------------------------------------------------------------------------------
PRINTED = [
    dict(id='street_length_m', value=48.0, file='production/specs/vignette-scene.json', find='"length_m": 48.0', what='the street is 48 m long'),
    dict(id='carriageway_half_m', value=3.0, file='production/specs/vignette-scene.json', find='"half_width_m": 3.0', what='kerb face at z = +-3.0 m'),
    dict(id='footway_width_m', value=2.0, file='production/specs/vignette-scene.json', find='"width_m": 2.0,\n      "crossfall": 0.025,\n      "surface": "sidewalk"', what='footway 2.0 m'),
    dict(id='kerb_upstand_m', value=0.125, file='production/specs/vignette-scene.json', find='"upstand_m": 0.125', what='kerb upstand 125 mm (the kerbs target keeps it for granite)'),
    dict(id='dropped_kerb_centre_x_m', value=22.5, file='production/specs/vignette-scene.json', find='"centre_x_m": 22.5', what='the west crossover centre'),
    dict(id='dropped_kerb_width_m', value=3.0, file='production/specs/vignette-scene.json', find='"crossover_width_m": 3.0', what='crossover 3.0 m wide'),
    dict(id='column_first_offset_m', value=8.0, file='production/specs/vignette-scene.json', find='"first_offset_m": 8.0', what='lamp columns at 8, 18 (west), 28, 38 (west)'),
    dict(id='kiosk_x_m', value=16.5, file='production/specs/vignette-scene.json', find='"x_m": 16.5', what='kiosk x'),
    dict(id='pillar_box_x_m', value=27.0, file='production/specs/vignette-scene.json', find='"x_m": 27.0', what='pillar box x'),
    dict(id='guard_rail_x_m', value=10.0, file='production/specs/vignette-scene.json', find='"x_m": 10.0', what='guard rail x 10 to 12'),
    dict(id='dustbin_x_m', value=21.4, file='production/specs/vignette-scene.json', find='"x_m": 21.4', what='dustbins x 21.4 and 22.0 (east)'),
    dict(id='existing_bollard_0_x_m', value=20.7, file='production/specs/vignette-pieces.json', find='"name":"prop_decorative_bollard_02_0","shape":"mesh","surface":"metal","asset":"decorative_bollard_02","x_m":20.7',
         what='the scene file already places two bollards flanking the yard mouth, 20.7 and 24.3, 0.5 m behind the west kerb'),
    dict(id='existing_bollard_1_x_m', value=24.3, file='production/specs/vignette-pieces.json', find='"name":"prop_decorative_bollard_02_1","shape":"mesh","surface":"metal","asset":"decorative_bollard_02","x_m":24.3',
         what='second yard-mouth bollard'),
    dict(id='existing_bollard_z_m', value=-3.5, file='production/specs/vignette-pieces.json', find='"x_m":20.7,"y_m":0.563525,"z_m":-3.5', what='west footway, 0.5 m behind the kerb face'),
    dict(id='existing_bollard_height_m', value=1.0083, file='production/specs/vignette-pieces.json', find='"sy_m":1.0083', what='the held stand-in mesh is 1.008 high'),
    dict(id='clutter_bollard_height_m', value=0.765, file='production/art/clutter-2026-09-29/README.md', find='cast-iron cannon-and-ball bollard', what='the street recipe builds a 0.765 m cannon-and-ball clutter bollard (glb bounds, read from production/assets/street/clutter/bollard.glb)'),
    dict(id='quay_bollard_height_m', value=0.72, file='tools/art-recipes/south-quay/south_quay_geom.py', find='(0.11, 0.71), (0.0, 0.72))', what='the south-quay kit bollard profile ends at 0.72'),
    dict(id='quay_bollard_base_r_m', value=0.25, file='tools/art-recipes/south-quay/south_quay_geom.py', find='BOLLARD_PROFILE = ((0.25, 0.00)', what='its flange radius 0.25'),
    dict(id='quay_bollard_set_back_m', value=0.75, file='production/research/south-quay/METHOD-2026-10-06.md', find='set 0.75 m back from the cope', what='ten bollards 0.75 m back from the cope nose'),
    dict(id='quay_bollard_count', value=10, file='production/research/south-quay/METHOD-2026-10-06.md', find='ten of them', what='ten bell bollards on the quay'),
    dict(id='quay_edge_x_m', value=-70.0, file='tools/art-recipes/south-quay/south_quay_geom.py', find='"north_quay_x": 280.0 - 350.0', what='the north quay edge, 70 m south of the street end'),
    dict(id='quay_bollard_x_m', value=-69.25, file='tools/art-recipes/south-quay/south_quay_geom.py', find='BOLLARDS = ((-69.25, -88.0)', what='bollards at x -69.25'),
    dict(id='asset_plan_bollard_models', value=3, file='production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md', find='| Bollards (cannon, concrete, steel) | 3 | 3 each | 6 to 10 |', what='3 models, 3 variants each, 6 to 10 on the street'),
    dict(id='asset_plan_lean_deg', value=3, file='production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md', find='lean of 1 to 3 degrees on poles and bollards', what='seed lean 1 to 3 degrees'),
    dict(id='yard_mouth_no_bands', value=0, file='production/research/street-clutter-1990/SUMMARY-2026-09-29.md', find='Wrong for 1990: reflective bands, stainless steel, gold paint.', what='no reflective bands'),
    dict(id='clutter_bollard_summary_height_cm', value=90, file='production/research/street-clutter-1990/SUMMARY-2026-09-29.md', find='Older ones were often about 90 cm (**uncertain**)', what='older cast bollards about 90 cm (uncertain)'),
]

# ------------------------------------------------------------------------------------------------------------
# more readings (h_read 1.15)
# ------------------------------------------------------------------------------------------------------------
US02_HALFWIDTH_READ = [(40, 112), (80, 111), (120, 107.5), (160, 105), (200, 104.5), (240, 103), (280, 103), (320, 101), (360, 99.5),
                       (400, 98), (440, 95.5), (480, 94), (520, 94), (560, 91.5), (600, 91), (640, 90.5), (760, 86), (800, 84),
                       (840, 83), (880, 81), (920, 79), (960, 79), (1000, 76), (1040, 75), (1080, 74), (1120, 72)]
US02_TOP_Z_READ = 1188.0
US02_FOOT_RING_R_READ = 132.0
US02_COLLAR_Z_READ = 703.0

# calibration anchors (raw numbers; self_check.py recomputes each camera height from them)
CAL = [
    dict(id='us01_brick', pano='urban_street_01', measured_mm=75.5, plane_h=1.15, true_mm=75.0, what='brick course pitch on the garden wall, rectified at 1.15 m'),
    dict(id='us01_line', pano='urban_street_01', measured_mm=98.3, plane_h=1.6, true_mm=75.0, what='single yellow line width at 1.6 m (distance transform, median ridge)'),
    dict(id='bge_brick_course', pano='bethnal_green_entrance', measured_mm=92.0, plane_h=1.15, true_mm=75.0, what='brick course pitch, gate pier and blue plinth'),
    dict(id='bge_brick_stretcher', pano='bethnal_green_entrance', measured_mm=255.0, plane_h=1.15, true_mm=225.0, what='stretcher module (215 + 10) on the same wall'),
    dict(id='bb_line', pano='birbeck_street_underpass', measured_mm=97.0, plane_h=1.6, true_mm=75.0, what='each line of the double yellow, at 1.6 m'),
    dict(id='lh_paver_course', pano='limehouse', measured_mm=146.0, plane_h=1.6, true_mm=105.0, what='clay paver 100 wide + 5 joint, course pitch'),
    dict(id='lh_paver_stretcher', pano='limehouse', measured_mm=280.0, plane_h=1.6, true_mm=205.0, what='clay paver 200 long + 5 joint'),
]

# set-backs read on the ground plans (z = 0 plane, axis at the centre): along the bearing from the axis to the kerb face foot line (or the top arris
# corrected to the foot), the angle between the kerb line and the perpendicular to the bearing, in degrees
SETBACKS = [
    dict(id='US01_b', along_mm=330, kerb_angle_deg=14, h_assumed=1.16, note='the bollard stands in the inside corner of a kerb build-out; both kerb faces are about 0.33 m from the axis'),
    dict(id='BB_b', along_mm=1090, kerb_angle_deg=16, h_assumed=1.22, note='concrete bullnosed kerb; footway about 2.5 m wide; the road-side foot line read'),
    dict(id='US02_a', along_mm=1610, kerb_angle_deg=45, h_assumed=1.15, note='the kerb top inner arris at 1.61 m along the bearing after correcting its 125 mm height; add about 0.15 for the kerb top'),
]
