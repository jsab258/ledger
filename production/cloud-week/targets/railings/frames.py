"""The photograph frames of the railings family: where each elevation plane stands in its panorama.  Read by measure.py, make_previews.py, make_target.py, self_check.py.
A frame: the panorama, the camera height at the OBJECT'S OWN ground (m), two ground points given as the pixel (col, row) of the foot of the object (the bottom of the plinth,
wall or flange; for a post the point is pushed back to its axis), the plane offset behind that line (mm), the window and the scale.

SECOND VERSION (after the fresh review, narrow point 1): the first version pooled one height for a whole panorama (0.97 for Bethnal Green, 1.12 for Urban Street 01 and
Limehouse).  Each object now has the height measured at its own ground.  Every length read at the first version's pooled height is multiplied by SCALE (new / first) in
measure.py; the windows below are the first version's windows multiplied by the same factor."""
FIRST_H = {'R3B': 0.97, 'R3A': 0.97, 'R3D': 1.12, 'LHB': 1.12}
H_CAM = {'R3B': 0.945, 'R3A': 1.02, 'R3D': 1.15, 'LHB': 1.13}
SCALE = {k: round(H_CAM[k] / FIRST_H[k], 4) for k in H_CAM}


def _w(k, d):
    f = SCALE[k]
    return {key: (round(v * f / 5.0) * 5 if key != 'mm' else v) for key, v in d.items()}


FRAMES = {
    'R3B': dict(id='R3B', pano='bethnal_green_entrance', what='the park railing on its brick plinth, with a hinge post and pier (the main photograph)',
                h_cam=H_CAM['R3B'], feet_px=[[2330, 2282], [3070, 2225]], off_mm=110.0, window=_w('R3B', dict(s0=0, s1=3870, z0=-50, z1=2450)),
                preview=_w('R3B', dict(s0=700, s1=3870, z0=-50, z1=2450, mm=3)), mask=[[190, 680, 1070, 1460]],
                head_close=_w('R3B', dict(s0=2300, s1=3100, z0=1700, z1=2450, mm=1)), foot_close=_w('R3B', dict(s0=2300, s1=3100, z0=-50, z1=800, mm=1))),
    'R3A': dict(id='R3A', pano='bethnal_green_entrance', what='the area railing on a two-stage dwarf wall in front of a housing block (oblique, 32 degrees to the line of sight)',
                h_cam=H_CAM['R3A'], feet_px=[[7540, 2243], [7990, 2155]], off_mm=110.0, window=_w('R3A', dict(s0=0, s1=3200, z0=-50, z1=2300)),
                preview=_w('R3A', dict(s0=0, s1=3200, z0=-50, z1=2300, mm=3)), mask=[]),
    'R3D': dict(id='R3D', pano='urban_street_01', what='the low green railing on a dark brick garden wall (a front garden of a council estate)',
                h_cam=H_CAM['R3D'], feet_px=[[3964, 2255], [4498, 2299]], off_mm=110.0, window=_w('R3D', dict(s0=0, s1=2860, z0=-60, z1=1300)),
                preview=_w('R3D', dict(s0=0, s1=2860, z0=-60, z1=1300, mm=3)), mask=[]),
    'LHB': dict(id='LHB', pano='limehouse', what='one bay of the marina quay edge: two bolted cast-iron chain posts and two swags of chain',
                h_cam=H_CAM['LHB'], feet_px=[[2741, 2882], [3376, 2400]], flange_r_mm=143.0, off_mm=0.0, window=_w('LHB', dict(s0=-600, s1=3440, z0=-100, z1=1400)),
                preview=dict(s0=-605, s1=3460, z0=-100, z1=1400, mm=4), mask=[[140, 545, 470, 785]]),
}

# the camera height at each OBJECT's own ground: the anchors that stand on that ground, the ones set aside, and the corroboration
OBJECTS = {
    'R3B': dict(pano='bethnal_green_entrance', h_cam=0.945, err=0.02, scale=SCALE['R3B'],
                ground='the block paving at the foot of the brick gate pier beside the railing (and the planter wall on the same paving)',
                anchors=['bge_gate_pier', 'bge_planter_wall'], excluded=[], corroboration=[],
                why='the gate pier (22 courses at 16k, foot row 4618 of 8192 = 2309 here: 0.942) and the planter wall on the same paving (0.963); the first version pooled 0.97 over three walls'),
    'R3A': dict(pano='bethnal_green_entrance', h_cam=1.02, err=0.03, scale=SCALE['R3A'],
                ground='the foot of its own two-stage dwarf wall (the oblique run to the right of the entrance)',
                anchors=['bge_dwarf_wall'], excluded=[], corroboration=[],
                why='the red courses of its own wall: 1.020 (the fresh review, rectified at 16k: 1.017); the pooled 0.97 was 5 % low for this wall'),
    'R3D': dict(pano='urban_street_01', h_cam=1.15, err=0.02, scale=SCALE['R3D'],
                ground='the foot of its own garden wall on the footway',
                anchors=['us01_garden_wall'], excluded=[dict(id='us01_gate_pier', h=1.084, why='the outlier (different bricks or foot), wrongly pooled in the first version')], corroboration=[],
                why='the garden wall under the railing: 1.156 (the fresh review, rectified at 16k on a 2.55 m foot line: 1.148; four column bands 1.13 to 1.16); the pooled 1.12 was 2.6 % low'),
    'LHB': dict(pano='limehouse', h_cam=1.13, err=0.03, scale=SCALE['LHB'],
                ground='the clay-paved quay walk and gravel the chain posts stand on',
                anchors=[], quoted=[dict(id='lh_paver_bollards', h=1.15, src='bollards TARGET.md section 3: a 200 x 100 clay paver reads 146 x 280 at 1.6 m (1.15)'),
                                    dict(id='lh_paver_review', h=1.135, src='the fresh review: clay paver course module 91.2 at h = 1: 1.12 (102 module) to 1.15 (105); midpoint')],
                excluded=[dict(id='lh_paver_upper', h=1.17, why='the upper end of the bollards target\'s readings, which assumes 5 mm joints (the review: holds at 1.12 to 1.15)')],
                corroboration=['lh_building_wall_a', 'lh_building_wall_b'],
                why='the paving under the posts: 1.135 to 1.15; the dock building\'s own foot (a different ground) reads 1.095 and 1.052 (the review 1.09), 6 % under, kept as corroboration only'),
}
