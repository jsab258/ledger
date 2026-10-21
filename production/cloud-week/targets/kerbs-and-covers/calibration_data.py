"""Camera heights of the Poly Haven panoramas, measured for each one on its own, at the ground each measurement of this target sits on.
(9 October 2026, after the bollards' writer and reviewer showed that none of these panoramas was taken at 1.6 m.)

Method 1, BRICK COURSES BY THE HORIZON METHOD (the bollards' writer's method, production/cloud-week/targets/bollards/calibrate.py; used here
with their anchors for urban_street_01, 02, bethnal_green_entrance and birbeck_street_underpass, re-run, and with five new walls for urban_street_03):
in a levelled equirectangular panorama the horizon is the middle row (H/2 = 2048 of 4096). On a vertical wall the courses are evenly spaced in tan(angle
below the horizon), so  camera height above the wall's foot = gauge x tan(angle of the foot) / (course pitch in tan units).  The pitch is fitted by a
Fourier fold of the column band's profile in tan units (calibrate.py); the joints are counted by eye on a crop for the starting guess; the foot row is read by eye.
Gauge 75 mm (4 courses = 300 mm; Victorian 73 to 79 mm gives +-4 %).

Method 2, CAR WHEELS: a tyre of known outer diameter D (a car's standard fit), top row and bottom row on the panorama:
    h = D tan(a_b) / (tan(a_b) - tan(a_t))   with a = (row - 2048) x pi / 4096.
It needs no wall and no foot ground: the contact patch is on the road. D is known to about +-4 %; the readings of the top of a tyre under its arch are +-3 rows.
Where both methods can be run on one panorama (urban_street_03) they agree within 2 %.

Every number below is raw: self_check.py recomputes each height from these rows and fails if the mean is farther from the stated height than the stated
error, and fails if any panorama is given a height that is not supported (the 1.6 m the first draft assumed is no longer used for any panorama).
"""

ASSUMED_FIRST_DRAFT_M = 1.6   # the height the first draft assumed for every panorama; not used any more

# brick anchors: pitch_tan is the fitted course pitch (calibrate.py re-fits it); foot_row read by eye; ground_step_m = how far the wall's foot ground
# stands ABOVE the ground the measurement sits on (the road or channel for kerbs and covers).
BRICKS = [
    # ---- urban_street_01 (the bollards' anchors, re-run; the footway at the wall stands one kerb upstand above the road)
    dict(pano='urban_street_01', id='us01_garden_wall', cols=[4250, 4275], rows=[2170, 2280], foot_row=2287, pitch_tan=0.01203, px_pitch_by_eye=15.3, gauge_mm=75.0,
         ground_step_m=0.11, step_kind='Judgement: the footway stands one kerb upstand (about 0.11) above the road; the bollards\' bed (0.07 below the footway) is not used here',
         what='garden wall on the footway behind the bollard US01_b', source='bollards/anchors.json, re-run'),
    dict(pano='urban_street_01', id='us01_gate_pier', cols=[3760, 3830], rows=[2170, 2222], foot_row=2225, pitch_tan=0.01049, px_pitch_by_eye=11.9, gauge_mm=75.0,
         ground_step_m=0.11, step_kind='Judgement (as above)', what='brick gate pier on the same footway', source='bollards/anchors.json, re-run'),
    # ---- urban_street_02
    dict(pano='urban_street_02', id='us02_building_wall', cols=[740, 840], rows=[2045, 2192], foot_row=2194, pitch_tan=0.00963, px_pitch_by_eye=11.75, gauge_mm=75.0,
         ground_step_m=0.11, step_kind='Judgement: footway to road, one kerb upstand (the bollards\' writer added 0.125)', what='the building wall behind US02_a, on its footway', source='bollards/anchors.json, re-run'),
    dict(pano='urban_street_02', id='us02_gate_pier', cols=[7970, 8000], rows=[2028, 2215], foot_row=2226, pitch_tan=0.01121, px_pitch_by_eye=14.77, gauge_mm=75.0,
         ground_step_m=0.11, step_kind='Judgement (as above)', what='gate pier at the panorama seam, on the same footway', source='bollards/anchors.json, re-run'),
    # ---- bethnal_green_entrance (the cover lies on the same block paving as the wall's foot: no step)
    dict(pano='bethnal_green_entrance', id='bge_planter_wall', cols=[5840, 5940], rows=[2100, 2258], foot_row=2262, pitch_tan=0.0129, px_pitch_by_eye=15.3, gauge_mm=75.0,
         ground_step_m=0.0, step_kind='Read: same block paving (the bollards\' writer)', what='planter wall on the same block paving as the cover', source='bollards/anchors.json, re-run'),
    # ---- birbeck_street_underpass (the footway; the road, where the kerb foot and the grate lie, is one concrete kerb upstand below it)
    dict(pano='birbeck_street_underpass', id='bb_viaduct_wall', cols=[3700, 3760], rows=[1845, 2015], foot_row=2318, pitch_tan=0.01502, px_pitch_by_eye=19.7, gauge_mm=75.0,
         ground_step_m=0.10, step_kind='Photo: the bollards\' writer measured the footway 0.105 above the road; this target\'s PM03 reads the concrete kerb at about 0.09 to 0.10',
         what='yellow-stock wall above the paint, on the footway', source='bollards/anchors.json, re-run'),
    # ---- urban_street_03 (new here): five brick surfaces along the footway; the footway at a wall stands the kerb upstand less the 5 mm flag step, plus the footway's
    # crossfall rise over about 2 m (1 in 40: 0.05), about 0.15 above the channel
    dict(pano='urban_street_03', id='us03_garage_pier', cols=[1500, 1590], rows=[2000, 2290], foot_row=2310, pitch_tan=0.01221, px_pitch_by_eye=15.7, gauge_mm=75.0,
         ground_step_m=0.15, step_kind='Judgement: 0.11 (kerb upstand less the flag step) + 0.05 (crossfall over about 2 m)', what='brick pier beside the garage doors, on the footway', source='this target'),
    dict(pano='urban_street_03', id='us03_wall_mid', cols=[1100, 1180], rows=[2000, 2262], foot_row=2264, pitch_tan=0.00993, px_pitch_by_eye=13.0, gauge_mm=75.0,
         ground_step_m=0.15, step_kind='Judgement (as above)', what='boundary wall with red bands, middle', source='this target'),
    dict(pano='urban_street_03', id='us03_wall_right_face', cols=[1240, 1320], rows=[2000, 2280], foot_row=2290, pitch_tan=0.01061, px_pitch_by_eye=13.7, gauge_mm=75.0,
         ground_step_m=0.15, step_kind='Judgement (as above)', what='the same wall, yellow-stock face', source='this target'),
    dict(pano='urban_street_03', id='us03_wall_left', cols=[960, 1040], rows=[2000, 2230], foot_row=2228, pitch_tan=0.00884, px_pitch_by_eye=12.0, gauge_mm=75.0,
         ground_step_m=0.15, step_kind='Judgement (as above)', what='the same wall, left end', source='this target'),
    dict(pano='urban_street_03', id='us03_low_wall', cols=[5180, 5320], rows=[2175, 2270], foot_row=2290, pitch_tan=0.01021, px_pitch_by_eye=14.5, gauge_mm=75.0,
         ground_step_m=0.15, step_kind='Judgement (as above)', what='low front-garden wall, 20 m round the corner of the view', source='this target'),
]

# wheel anchors: top and bottom rows of the outer tyre, tyre outer diameter D (m) and its error
WHEELS = [
    dict(pano='urban_street_03', id='us03_citroen_rear', top_row=2190, bottom_row=2302, D_m=0.65, D_err_m=0.025, what='a 2013-18 Citroen people-carrier, rear near wheel (205/55R16 to 215/55R17: 0.63 to 0.67)'),
    dict(pano='urban_street_04', id='us04_bmw_front', top_row=2143, bottom_row=2214, D_m=0.65, D_err_m=0.025, what='a grey BMW 3-series estate, front near wheel (225/50R17 or 225/40R18: 0.64 to 0.66)'),
    dict(pano='urban_street_04', id='us04_aygo_rear', top_row=2178, bottom_row=2249, D_m=0.555, D_err_m=0.012, what='a silver Toyota Aygo (first generation), rear near wheel (155/65R14 to 165/60R14: 0.55 to 0.56)'),
    dict(pano='urban_street_04', id='us04_convertible_front', top_row=2100, bottom_row=2145, D_m=0.65, D_err_m=0.03, what='a grey BMW convertible, front far wheel (low resolution: tyre top +-3 rows)'),
]
WHEELS_NOT_USED = [
    'urban_street_04 Aygo front wheel: the top of the tyre is hidden in the arch (its rim alone gives 1.25 m with a 14-inch rim, its tyre-ratio 1.85): not used',
    'urban_street_04 Volkswagen SUV far wheel: too dark and too small: not used',
]

# the stated height for each panorama, at the ground its measurements sit on, with the error that self_check.py holds the anchors to.
# `ground`: where the measurements lie (road/channel level unless said); `anchors`: ids used.
HEIGHTS = {
    'urban_street_03': dict(h_m=1.44, err_m=0.07, ground='the channel setts at the kerb foot (the road)', bricks=['us03_garage_pier', 'us03_wall_mid', 'us03_wall_right_face', 'us03_wall_left', 'us03_low_wall'], wheels=['us03_citroen_rear'],
                            note='bricks mean 1.28 above the wall foot + 0.15 = 1.43; the wheel 1.46; adopted 1.44 (the first draft: 1.6, which is 11 % high). The 75 mm yellow line does not decide it: read on the 1.6 m picture it is 64 mm (area over length), 72 mm (one cut) or 76 to 82 (the review, edges by eye), i.e. 1.46 to 1.87 for a 75 mm line, and painted lines are ragged: inconclusive, consistent with 1.44 only if the line is about 68 mm'),
    'urban_street_01': dict(h_m=1.23, err_m=0.08, ground='the road beside the kerb (the footway stands one kerb upstand above it)', bricks=['us01_garden_wall', 'us01_gate_pier'], wheels=[],
                            note='garden wall 1.27 and gate pier 1.09 (both +0.11 to the road); the bollards\' writer adopted 1.195 at the bed (= 1.235 at the road) and their reviewer measured 1.23 and 1.19 (about 1.27 at the road); adopted 1.23 (the first draft: 1.6, 30 % high)'),
    'urban_street_02': dict(h_m=1.01, err_m=0.06, ground='the carriageway (the footway stands one kerb upstand above it)', bricks=['us02_building_wall', 'us02_gate_pier'], wheels=[],
                            note='building wall 0.875 and gate pier 0.919 above their footway, + 0.11 = 0.99 and 1.03; the bollards\' writer 0.92 and their reviewer 0.91 to 0.93 (about 1.03 to 1.05 at the road); adopted 1.01 (the first draft: 1.6, 58 % high)'),
    'bethnal_green_entrance': dict(h_m=1.00, err_m=0.06, ground='the block paving the cover lies in', bricks=['bge_planter_wall'], wheels=[],
                                   note='planter wall 0.96; the bollards\' reviewer 1.03 to 1.04; their adopted 1.02; adopted 1.00 (the first draft: 1.6, 60 % high)'),
    'birbeck_street_underpass': dict(h_m=1.165, err_m=0.07, ground='the carriageway at the kerb foot (the footway stands one concrete kerb upstand above it)', bricks=['bb_viaduct_wall'], wheels=[],
                                     note='viaduct wall 1.05 above the footway; the bollards\' reviewer mean 1.085; + 0.10 to the road = 1.15 to 1.185; adopted 1.165 (the first draft: 1.6, 37 % high)'),
    'urban_street_04': dict(h_m=1.50, err_m=0.10, ground='the carriageway', bricks=[], wheels=['us04_bmw_front', 'us04_aygo_rear', 'us04_convertible_front'],
                            note='no brick wall stands on the ground here (stucco, stone), so wheels only: BMW 1.51, Aygo 1.56, convertible 1.40, mean 1.49; the method was checked on urban_street_03 (wheel 1.46 against bricks 1.43); adopted 1.50 (the first draft: 1.6, 7 % high: inside the error)'),
}
