"""The photograph frames of the railings family: where each elevation plane stands in its panorama.  Read by measure.py, make_previews.py, make_target.py.
A frame: the panorama, the camera height at the object's ground (m), two ground points given as the pixel (col, row) of the foot of the object (the
bottom of the plinth, wall or flange; for a post the point is pushed back to its axis), the plane offset behind that line (mm), the window and the scale."""
FRAMES = {
    'R3B': dict(id='R3B', pano='bethnal_green_entrance', what='the park railing on its brick plinth, with a hinge post and pier (the main photograph)',
                h_cam=0.97, feet_px=[[2330, 2282], [3070, 2225]], off_mm=110.0, window=dict(s0=0, s1=3870, z0=-50, z1=2450),
                preview=dict(s0=700, s1=3870, z0=-50, z1=2450, mm=3), mask=[[200, 700, 1100, 1500]]),
    'R3A': dict(id='R3A', pano='bethnal_green_entrance', what='the area railing on a two-stage dwarf wall in front of a housing block (oblique, 32 degrees to the line of sight)',
                h_cam=0.97, feet_px=[[7540, 2243], [7990, 2155]], off_mm=110.0, window=dict(s0=0, s1=3200, z0=-50, z1=2300),
                preview=dict(s0=0, s1=3200, z0=-50, z1=2300, mm=3), mask=[]),
    'R3D': dict(id='R3D', pano='urban_street_01', what='the low green railing on a dark brick garden wall (a front garden of a council estate)',
                h_cam=1.12, feet_px=[[3964, 2255], [4498, 2299]], off_mm=110.0, window=dict(s0=0, s1=2860, z0=-60, z1=1300),
                preview=dict(s0=0, s1=2860, z0=-60, z1=1300, mm=3), mask=[]),
    'LHB': dict(id='LHB', pano='limehouse', what='one bay of the marina quay edge: two bolted cast-iron chain posts and two swags of chain',
                h_cam=1.12, feet_px=[[2741, 2882], [3376, 2400]], flange_r_mm=143.0, off_mm=0.0, window=dict(s0=-600, s1=3440, z0=-100, z1=1400),
                preview=dict(s0=-600, s1=3440, z0=-100, z1=1400, mm=4), mask=[[140, 540, 470, 780]]),
}
# stated camera height at each object's ground (m) and its error; the self-check recomputes the mean of the anchors at that ground
CAMERAS = {
    'bethnal_green_entrance': dict(h_cam=0.97, err=0.06, anchors=['bge_planter_wall', 'bge_gate_pier', 'bge_dwarf_wall'],
                                   why='three brick walls and piers on the same block paving as the railings: 0.963, 0.927 and 1.020 m (mean 0.970); the bollards target states 1.02 +-0.07 for this panorama (inside)'),
    'urban_street_01': dict(h_cam=1.12, err=0.06, anchors=['us01_garden_wall', 'us01_gate_pier'],
                            why='the garden wall and the gate pier on the footway: 1.156 and 1.084 m (mean 1.120); the bollards target adds the 0.07 step to its bed (1.23 and 1.15 there)'),
    'limehouse': dict(h_cam=1.12, err=0.07, anchors=['lh_building_wall_a', 'lh_building_wall_b'], quoted=[dict(id='lh_paver_100', h=1.15, src='bollards TARGET.md section 3: a clay paver 200 x 100 reads 146 x 280 at 1.6 m, quoted'),
                                                                                                   dict(id='lh_paver_200', h=1.17, src='the same, quoted (the reviewer 1.15 to 1.18)')],
                      why='two column bands of the dock building beside the quay walk (1.095, 1.052 m) and the two quoted paver readings (1.15, 1.17): mean 1.117'),
}
