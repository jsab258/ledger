"""The corrected numbers of the kerbs-and-covers target (9 October 2026, camera heights corrected), and the first draft's numbers beside them.

Every length read off a Poly Haven panorama scales with that panorama's camera height (a flat plane read at an assumed 1.6 m is the true plane
times 1.6 / h), so a number measured on urban_street_03 (h 1.44 m) is multiplied by 0.90, on urban_street_01 (1.23) by 0.77, on urban_street_02 (1.01) by 0.63,
on bethnal_green_entrance (1.00) by 0.625, on birbeck_street_underpass (1.165) by 0.73, on urban_street_04 (1.50) by 0.94. Angles, counts, ratios, Read
numbers (SCENE-SLOTS.md, the Poly Haven model and texture) and Judgement numbers that do not come from a picture are NOT scaled.
`N` is what the target now says; `OLD` is the first draft; CORRECTIONS lists every number that changed, with its rule.
"""
import calibration_data as CD

H = {k: v['h_m'] for k, v in CD.HEIGHTS.items()}
R = {k: round(v * 1000.0 / 1600.0, 4) for k, v in H.items()}   # scale from the 1.6 m readings to the measured height

N = dict(
    # ---- granite kerb (urban_street_03, x 0.90)
    U=115, TOPW=170, BATTER=20, VERT_Z=45, ARRIS_R=25, END_R=10, DEPTH=255,
    LEN_MIN=750, LEN_MAX=1050, LEN_MEAN=900, JOINT=8, FLAGS_Z=110,
    # ---- concrete kerb (birbeck_street_underpass, x 0.73; the street's 915 block Read)
    CU=95, CW=125, CR=50,
    # ---- channel (x 0.90): two courses of setts
    CH_W=204, CH_A=104, CH_B=100, SETT_MIN=120, SETT_MAX=210, SETT_MEAN=160, SETT_JOINT=11, CH_CONC_W=255,
    # ---- crossover (x 0.90)
    LIP_Z=12, LIP_W=112, LIP_SETT=155, LIP_JOINT=9, RAMP_BACK=845, RAMP_JOINT=12, FLANK_W=140, TAPER_W=125,
    # ---- gully grate A (x 0.90)
    GA_L=440, GA_W=290, GA_SLOT_W=26, GA_SLOT_L=255, GA_PITCH=51, GA_Y0=90, GA_N=8,
    # ---- gully grate B (birbeck_street_underpass, x 0.73)
    GB_L=355, GB_W=325, GB_SLOT_W=20, GB_BAR=22, GB_PITCH=42, GB_LENGTHS=[91, 182, 255, 288, 255, 182, 91], GB_HOLE=18, GB_HOLE_OFF=40,
    # ---- covers
    STUD_OUT=600, STUD_RIM=12, STUD_PITCH=59, STUD=28, STUD_MARGIN=8, STUD_H=3, STUD_KEYHOLE=12, STUD_BOSS=[50, 25, 2], STUD_JOINT=3,   # bethnal_green_entrance x 0.625
    FW_OUT=[1060, 600], FW_IN=[860, 400], FW_RIM=100, FW_FLANGE=40, FW_LEDGE=60, FW_STEP=11, FW_CHAMFER=22,                         # urban_street_03 x 0.90
    RD_OUT=[645, 670], RD_HAIR=10, RD_RIM=25,                                                                                      # urban_street_02 x 0.63
    DL_OUT=[1710, 570], DL_PITCH=31, DL_STUD=17, DL_MARGIN=28, DL_SURR=140,                                                       # urban_street_04 x 0.94
    TC_LID=[335, 150], TC_FRAME=[385, 195], TC_SURR=28,
    CORNER_R=6200, CORNER_CHORD=1200,
)

OLD = dict(
    U=125, TOPW=190, BATTER=25, LEN_MIN=800, LEN_MAX=1200, LEN_MEAN=1000, JOINT=9, FLAGS_Z=120,
    CU=110, CW=160, CR=60,
    CH_W=225, CH_A=115, CH_B=110, SETT_MIN=130, SETT_MAX=230, SETT_MEAN=180, SETT_JOINT=12,
    LIP_Z=15, LIP_W=125, LIP_SETT=170, LIP_JOINT=10, RAMP_BACK=917, FLANK_W=155, TAPER_W=160,
    GA_L=485, GA_W=325, GA_SLOT_W=29, GA_SLOT_L=285, GA_PITCH=57, GA_Y0=100,
    GB_L=490, GB_W=445, GB_SLOT_W=28, GB_BAR=30, GB_PITCH=58, GB_HOLE=25, GB_HOLE_OFF=55,
    STUD_OUT=960, STUD_RIM=20, STUD_PITCH=95, STUD=45, STUD_MARGIN=10, STUD_H=4, STUD_KEYHOLE=20, STUD_BOSS=[80, 40, 3], STUD_JOINT=5,
    FW_OUT=[1180, 660], FW_IN=[960, 440], FW_RIM=110, FW_STEP=12, FW_CHAMFER=25,
    RD_OUT=[1000, 1050], RD_HAIR=15, RD_RIM=40,
    DL_OUT=[1820, 620], DL_PITCH=33, DL_STUD=18, DL_MARGIN=30, DL_SURR=150,
    TC_LID=[360, 160], TC_FRAME=[410, 210], TC_SURR=30,
    CORNER_R=6500,
)

# derived
N['RAMP_FRONT'] = N['LIP_W'] + N['RAMP_JOINT']                      # 124: the ramp's front edge, behind the lip row and a joint
N['FLANK_Y1'] = N['TOPW'] + 12                                      # 182: the flank strip's kerb end, 12 mm behind the kerb back
N['LIP_N'] = -(-3000 // (N['LIP_SETT'] + N['LIP_JOINT']))           # setts in the 3.0 m gap
N['RAMP_RISE'] = N['FLAGS_Z'] - N['LIP_Z']                          # 98
N['RAMP_RUN'] = N['RAMP_BACK'] - N['RAMP_FRONT']                    # 706
N['GA_SPAN'] = (N['GA_N'] - 1) * N['GA_PITCH'] + N['GA_SLOT_W']     # 383
N['GA_BAR'] = N['GA_PITCH'] - N['GA_SLOT_W']                        # 25
N['GA_END_ALONG'] = (N['GA_L'] - N['GA_SPAN']) / 2.0                # 28.5
N['GA_END_ACROSS'] = (N['GA_W'] - N['GA_SLOT_L']) / 2.0             # 17.5
N['GA_Y1'] = N['GA_Y0'] + N['GA_W']                                 # 380
N['GA_OPEN'] = round(N['GA_N'] * N['GA_SLOT_W'] * N['GA_SLOT_L'] / (N['GA_L'] * N['GA_W']), 3)

# the photographed crossing (urban_street_03) at the corrected height: the first-draft numbers x 0.90
REF = dict(
    gap=1930, foot_line_distance=3412, gap_centre_local_x=-605, channel_width=204, lip_y0=-112, ramp_back=-845, ramp_front=-124,
    flank_width=140, flank_y1=-182, flank_left_x=[-1263, -1109], flank_right_x=[968, 1094], kerb_top_rear_y=-170,
    gully=dict(x_centre=-676, y0=92, y1=383, along=440, across=292),
)

# (item, pano, first draft, corrected, rule)
CORRECTIONS = [
    ('granite kerb top width', 'urban_street_03', 190, N['TOPW'], 'Photo: PM01, PM02, PM25 (181, 185, 189 at 1.6 m) x 0.90 = 163, 167, 170; the review\'s 193 and 201 x 0.90 = 174, 181'),
    ('granite kerb upstand (top)', 'urban_street_03', 125, N['U'], 'Photo: the arris-middle readings 118 and 113 x 0.90 = 107 and 102 (vertical-face equivalents 104 to 116); the scene\'s 125 Read falls outside the error, so the photographs win'),
    ('granite kerb batter (set back at z = U - 25)', 'urban_street_03', 25, N['BATTER'], 'Photo: PM26 29.3 x 0.90 = 26.4 at the arris middle (the arris rounding alone is 7.3)'),
    ('granite block lengths', 'urban_street_03', '800 to 1200, mean 1000', '750 to 1050, mean 900', 'Photo: PM04 (1011, 837, 1143) x 0.90 = 910, 753, 1029; the review 830, 1050, 1130 x 0.90'),
    ('granite kerb joint', 'urban_street_03', 9, N['JOINT'], 'Photo: PM05 9.2 x 0.90 = 8.3'),
    ('footway flag level above the channel', 'urban_street_03', 120, N['FLAGS_Z'], 'Derived: kerb top less 5'),
    ('concrete kerb upstand', 'birbeck_street_underpass', 110, N['CU'], 'Photo: PM03 arris middle 96.5 x 0.73 = 70 (top about 85 to 88 for R 50 to 60); the bollards\' writer measured the footway 0.105 above the road; between them, 95'),
    ('concrete kerb top width', 'birbeck_street_underpass', 160, N['CW'], 'Photo: PM03 166 x 0.73 = 121; also the scene\'s 125 and the BS 125 section'),
    ('concrete kerb arris radius', 'birbeck_street_underpass', 60, N['CR'], 'Judgement, rescaled with the kerb'),
    ('granite sett channel width', 'urban_street_03', 225, N['CH_W'], 'Photo: PM06 226 x 0.90 = 204'),
    ('channel courses A, B', 'urban_street_03', '115, 110', '104, 100', 'Photo x 0.90'),
    ('sett length along the kerb', 'urban_street_03', '130 to 230, mean 180', '120 to 210, mean 160', 'Photo x 0.90'),
    ('sett joint', 'urban_street_03', 12, N['SETT_JOINT'], 'Photo x 0.90'),
    ('lip row across', 'urban_street_03', 125, N['LIP_W'], 'Photo: PM08 124.8 x 0.90 = 112'),
    ('lip sett length', 'urban_street_03', 170, N['LIP_SETT'], 'Photo: PM07 171 x 0.90 = 154'),
    ('lip joint', 'urban_street_03', 10, N['LIP_JOINT'], 'Photo x 0.90'),
    ('lip height above the channel', 'urban_street_03', 15, N['LIP_Z'], 'Photo: PM09 12.2 x 0.90 = 11'),
    ('lip setts in the 3.0 m gap', 'urban_street_03', 17, N['LIP_N'], 'Derived: 3000 / (155 + 9)'),
    ('ramp back edge behind the foot line', 'urban_street_03', 917, N['RAMP_BACK'], 'Photo: PM11 (924 at 1.6 m, 1.0034 for the top-plane smear) x 0.90 = 846'),
    ('ramp front edge', 'urban_street_03', 137, N['RAMP_FRONT'], 'Derived: lip row + a 12 mm joint'),
    ('ramp rise and run', 'urban_street_03', '105 over 780 (1 in 7.4)', '98 over 721 (1 in 7.4)', 'Derived'),
    ('flank strip width', 'urban_street_03', 155, N['FLANK_W'], 'Photo: PM12 (171, 141 at 1.6 m) x 0.90 = 154, 127: mean 140'),
    ('flank strip length', 'urban_street_03', 715, N['RAMP_BACK'] - N['FLANK_Y1'], 'Derived: ramp back to 12 mm behind the kerb back'),
    ('taper block width (variant)', 'urban_street_03', 160, N['TAPER_W'], 'Derived: the concrete kerb\'s 125'),
    ('gully grate A overall', 'urban_street_03', '485 x 325', '440 x 290', 'Photo: PM13 489 x 324 x 0.90 = 440 x 292'),
    ('gully grate A slot width, bar', 'urban_street_03', '29, 28', '26, 25', 'Photo: PM28 / PM30 28.6 x 0.90 = 25.7'),
    ('gully grate A slot length', 'urban_street_03', 285, N['GA_SLOT_L'], 'Photo: PM14 285 x 0.90 = 256'),
    ('gully grate A slot pitch', 'urban_street_03', 57, N['GA_PITCH'], 'Photo: PM30 56.97 x 0.90 = 51.3'),
    ('gully grate A slot span', 'urban_street_03', 428, N['GA_SPAN'], 'Derived: 7 x 51 + 26 (PM14 433 x 0.90 = 390)'),
    ('gully grate A end walls (along, across)', 'urban_street_03', '28.5, 20', '28.5, 17.5', 'Derived'),
    ('gully grate A kerb-side edge', 'urban_street_03', 100, N['GA_Y0'], 'Photo x 0.90'),
    ('gully grate A open fraction', 'urban_street_03', 0.42, N['GA_OPEN'], 'unchanged by scale'),
    ('gully grate B overall', 'birbeck_street_underpass', '490 x 445', '355 x 325', 'Photo x 0.73'),
    ('gully grate B slot, bar, pitch', 'birbeck_street_underpass', '28, 30, 58', '20, 22, 42', 'Photo (PM29, PM15) x 0.73'),
    ('gully grate B lifting hole, offset', 'birbeck_street_underpass', '25, 55', '18, 40', 'Photo x 0.73'),
    ('stud cover outer', 'bethnal_green_entrance', 960, N['STUD_OUT'], 'Photo: PM18 (980 x 920 by the review) x 0.625 = 612 x 575'),
    ('stud cover rim, lid', 'bethnal_green_entrance', '20, 920', '12, 576', 'Photo x 0.625'),
    ('stud cover stud pitch, stud', 'bethnal_green_entrance', '95, 45', '59, 28', 'Photo: PM17 94.4 x 0.625 = 59'),
    ('stud cover margin, height, joint', 'bethnal_green_entrance', '10, 4, 5', '8, 3, 3', 'Photo / Judgement x 0.625'),
    ('stud cover keyhole, boss', 'bethnal_green_entrance', '20, 80 x 40 x 3', '12, 50 x 25 x 2', 'Photo x 0.625'),
    ('footway recessed cover outer, infill', 'urban_street_03', '1180 x 660, 960 x 440', '1060 x 600, 860 x 400', 'Photo: PM19 x 0.90'),
    ('footway recessed cover rim (flange + ledge)', 'urban_street_03', '110 (45 + 65)', '100 (40 + 60)', 'Photo x 0.90'),
    ('tarmac-filled road cover', 'urban_street_02', '1000 x 1050', '645 x 670', 'Photo: PM20 (1020 x 1065) x 0.63'),
    ('two-leaf road cover', 'urban_street_04', '1820 x 620', '1710 x 570', 'Photo: PM21 (1824 x 600) x 0.94'),
    ('two-leaf cover stud pitch, stud, margin, surround', 'urban_street_04', '33, 18, 30, 150', '31, 17, 28, 140', 'Photo x 0.94'),
    ('telecom blank lid, frame, surround', 'urban_street_04', '360 x 160, 410 x 210, 30', '335 x 150, 385 x 195, 28', 'Photo x 0.94'),
    ('radius corner (face)', 'urban_street_04', 6500, N['CORNER_R'], 'Photo: PM16 (6.8 m to the line x 0.94 = 6.4 m, less 0.2 m)'),
    ('mitred corner angle', 'urban_street_01', 133, 133, 'an angle: unchanged by scale'),
]
