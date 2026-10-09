#!/usr/bin/env python
"""Writes target.json of the railings family from the hand-read numbers below, anchors.json, photo_measurements.json and frames.py.
    /home/user/.bpyenv/bin/python make_target.py
Everything is millimetres unless a key says _m (metres, the street's frame).  Each number carries its kind: Read (printed in the repository),
Photo (measured on a photograph, method and error given), Derived, Judgement (a trade or period guess, said so)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from frames import FRAMES, OBJECTS, SCALE, FIRST_H, H_CAM

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
anchors = json.load(open(os.path.join(HERE, 'anchors.json')))
PM = json.load(open(os.path.join(HERE, 'photo_measurements.json')))
HR = PM['hand_reads']
R3B = PM['R3B']
import struct, random
import numpy as _np

T = {}
T['family'] = 'railings'
T['title'] = "Quay Street's kerbside guard rail, its quay railing and chain, and the boundary railings the street does not have"
T['version'] = 'second version, after the fresh review of 9 October 2026 (TARGET-REVIEW.md): A1 in the reviewer\'s rectangular-hollow-section form; the jetty railing amended; camera heights per object'
T['written'] = '2026-10-09'
T['units'] = 'millimetres unless a key ends in _m (metres, the street recipe\'s frame); the .glb is metres, z up, scale 1'

# ------------------------------------------------------------------------------------------------------------------ scene numbers (Read)
T['scene_numbers'] = [
    dict(id='guard_rail_line', file='production/cloud-week/targets/SCENE-SLOTS.md', find='1.0 high; posts 0.05; rails 0.04; five infill bars of 0.025 a panel', what='the scene\'s stand-in: 1.0 high, posts 0.05, rails 0.04, five infill bars of 0.025 a panel', value=dict(height_m=1.0, post_m=0.05, rail_m=0.04, bars=5, bar_m=0.025)),
    dict(id='guard_rail_place', file='production/cloud-week/targets/SCENE-SLOTS.md', find='east side, x 10.0 to 12.0 (one 2.0 m panel, beside the gully), 0.25 m back from the kerb', what='one 2.0 m panel, east side, x 10.0 to 12.0, 0.25 m back from the kerb', value=dict(x0_m=10.0, x1_m=12.0, setback_from_kerb_m=0.25)),
    dict(id='scene_panels', file='production/specs/vignette-scene.json', find='"panels": 1,', what='E8 has one panel', value=1),
    dict(id='scene_setback', file='production/specs/vignette-scene.json', find='"setback_from_kerb_m": 0.25', what='E8 set-back 0.25 m', value=0.25),
    dict(id='scene_infill', file='production/specs/vignette-scene.json', find='"infill_per_panel": 5', what='E8 five infill bars', value=5),
    dict(id='scene_post_d', file='production/specs/vignette-scene.json', find='"post_diameter_m": 0.050', what='E8 post 0.050', value=0.05),
    dict(id='scene_rail_d', file='production/specs/vignette-scene.json', find='"rail_diameter_m": 0.040', what='E8 rail 0.040', value=0.04),
    dict(id='scene_infill_d', file='production/specs/vignette-scene.json', find='"infill_diameter_m": 0.025', what='E8 infill 0.025', value=0.025),
    dict(id='feet_post0', file='production/specs/vignette-feet.json', find='"x_m":10,"z_m":3.375,"foot_y_m":0.05625', what='post 0 stands at x 10, z 3.375, its foot at y 0.05625 (the footway there)', value=dict(x_m=10.0, z_m=3.375, foot_y_m=0.05625)),
    dict(id='feet_post1', file='production/specs/vignette-feet.json', find='"name":"rail_post1","bom":"E8_guard_railing","edge":"east_footway","region":"x12_18","x_m":12,"z_m":3.375', what='post 1 stands at x 12, z 3.375', value=dict(x_m=12.0, z_m=3.375)),
    dict(id='pieces_lower_rail', file='production/specs/vignette-pieces.json', find='"name":"rail_bar0_45","shape":"cyl","surface":"metal","asset":null,"x_m":11,"y_m":0.50625,"z_m":3.375', what='the stand-in\'s lower rail is 0.45 above its foot (y 0.50625 over 0.05625)', value=dict(above_foot_m=0.45)),
    dict(id='stallriser', file='production/cloud-week/targets/SCENE-SLOTS.md', find='stallriser 0.60 high, 0.15 proud', what='stallriser 0.15 proud of the frontage line', value=dict(proud_m=0.15)),
    dict(id='pilaster', file='production/cloud-week/targets/SCENE-SLOTS.md', find='pilasters 0.35 wide, 0.10 proud', what='pilasters 0.10 proud', value=dict(proud_m=0.10)),
    dict(id='frontage_z', file='production/specs/terrace-fronts.md', find='`frontage_z_m` 5.125', what='the frontage line is z 5.125 (the kerb face z 3.0 + the kerb 0.125 + the footway 2.0)', value=5.125),
    dict(id='kerb_target_top', file='production/cloud-week/targets/kerbs-and-covers/TARGET.md', find='115 mm upstand, about 170 mm top', what='the kerbs target: granite kerb 115 upstand, 170 top', value=dict(upstand=115, top=170)),
    dict(id='kerb_target_flags', file='production/cloud-week/targets/kerbs-and-covers/TARGET.md', find='footway flags +110', what='the kerbs target: footway flags +110 over the channel', value=110),
    dict(id='bollard_chain_bar', file='production/cloud-week/targets/bollards/TARGET.md', find='plain short link, a 13 mm bar', what='the bollards target\'s plain chain: short link, 13 mm bar', value=13),
    dict(id='bollard_post_spacing', file='production/cloud-week/targets/bollards/TARGET.md', find='post spacing 3.0 m', what='the bollards target\'s chain posts 3.0 m apart', value=3000),
    dict(id='bollard_lugs', file='production/cloud-week/targets/bollards/TARGET.md', find='a cast **D-lug** on each side of the shaft at z **420 and 840**', what='K5 chain eyes at z 420 and 840', value=[420, 840]),
    dict(id='bollard_sag', file='production/cloud-week/targets/bollards/target.json', find='"sag_mm": 150', what='K5 chain sag 150 (Judgement there)', value=150),
    dict(id='kit_jetty_x', file='tools/art-recipes/south-quay/south_quay_geom.py', find='"jetty_x": (220.0 - 350.0, 240.0 - 350.0)', what='the jetty strip x -130 to -110', value=[-130.0, -110.0]),
    dict(id='kit_jetty_end', file='tools/art-recipes/south-quay/south_quay_geom.py', find='"jetty_end_y": 385.0 - 400.0', what='the jetty\'s end at y -15', value=-15.0),
    dict(id='kit_cope', file='tools/art-recipes/south-quay/south_quay_geom.py', find='COPING_W_M = 0.60', what='the cope 0.60 across', value=0.60),
    dict(id='kit_parapet', file='tools/art-recipes/south-quay/south_quay_geom.py', find='kit.box(par, x_a, x_a + 0.80, -100.0 - COPING_W_M, at["jetty_end_y"] - 8.0,', what='the jetty\'s stone parapet on the seaward side: x -129.4 to -128.6, ending at y -23.0', value=dict(x=[-129.4, -128.6], y_end=-23.0)),
    dict(id='kit_light', file='tools/art-recipes/south-quay/south_quay_geom.py', find='c = ((jx0 + jx1) / 2.0, at["jetty_end_y"] - 4.5)', what='the harbour light stands at x -120, y -19.5', value=dict(x=-120.0, y=-19.5, plinth_half=1.4)),
    dict(id='kit_no_railing', file='production/art/south-quay/README.md', find='Ladder | 0.45 m wide, rungs 0.30 m apart', what='the kit has a ladder and bollards and a stone parapet on the jetty; it has no railing on any quay edge', value='none'),
    dict(id='asset_plan_rows', file='production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md', find='2 m guard-rail panel (posts, rails, infill); two-rail tube railing with chain', what='the asset plan\'s linear kit rows', value='2 m panel; two-rail tube railing with chain'),
    dict(id='asset_plan_counts', file='production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md', find='Guard railing; quay railing with chain; fences', what='guard railing 1 kit, 1 to 3 panels; quay railing with chain 1 kit, along the quay', value='1 kit; 1 kit'),
    dict(id='hull_chain_edge', file='production/research/atlas-01/CONTINUATION.md', find='chain-edged quay', what='R08, River Hull, 1989 (a photograph read by an earlier session, not reachable here): a chain-edged quay', value='chain-edged'),
    dict(id='e8_not_tree_guard', file='production/specs/vignette-bill-of-materials.md', find='**E8 is not the railing we hold.**', what='the held trunk_protection_railing is a tree-pit guard, not E8', value='not E8'),
    dict(id='yard_gap', file='production/specs/vignette-scene.json', find='The 3.0 m between west_south\'s end at x=21.0 and this block\'s start at x=24.0 is the YARD ENTRANCE', what='the yard entrance is a 3.0 m gap in the data, x 21.0 to 24.0, west side', value=[21.0, 24.0]),
    dict(id='awning_piece', file='production/specs/vignette-pieces.json', find='"name":"prop_awning_02_0","shape":"mesh","surface":"wood","asset":"awning_02","x_m":12,"y_m":2.28835,"z_m":4.25745,"sx_m":3,"sy_m":1.3233,"sz_m":1.7351', what='the fish market\'s awning (E18): x 10.5 to 13.5, z 3.39 to 5.125, y 1.627 to 2.95, awning_02.glb', value=dict(x_m=12.0, y_m=2.28835, z_m=4.25745, sx_m=3.0, sy_m=1.3233, sz_m=1.7351)),
    dict(id='kit_rings_jetty', file='tools/art-recipes/south-quay/south_quay_geom.py', find='for y in (-62.0, -32.0):', what='the kit hangs mooring rings on the jetty\'s basin face at y -62 and -32 (x = the jetty\'s -110 less the cope nose 0.05)', value=[[-110.05, -62.0], [-110.05, -32.0]]),
    dict(id='kit_cope_nose', file='tools/art-recipes/south-quay/south_quay_geom.py', find='COPING_NOSE_M = 0.05', what='the cope stands 50 mm proud of the wall face', value=0.05),
]

# ------------------------------------------------------------------------------------------------------------------ street frame numbers
T['street_frame'] = dict(
    note='the street recipe\'s frame, metres: x along the street (0 at its south end, + north), z across (the crown 0, + east); the kerb face at z +-3.0; the kerb\'s top 0.125 wide in the scene (170 in the kerbs target); the footway 2.0 wide to the frontage line z 5.125',
    kerb_face_z_m=3.0, kerb_back_scene_z_m=3.125, kerb_back_kerbs_target_z_m=3.170, frontage_z_m=5.125, stallriser_face_z_m=5.125 - 0.15, pilaster_face_z_m=5.125 - 0.10,
    channel_above_crown_m=-0.075, flags_above_channel_mm_kerbs_target=110, footway_crossfall='1 in 40, rising away from the kerb',
    foot_y_scene_m=0.05625, foot_y_kerbs_target_m=round(-0.075 + 0.115, 5),
    quay_frame='the south-quay kit\'s frame: x along Quay Street (0 at its south end, + north, so the quay is at x -70), y across (east +), z up; the apron and the copes at +0.05 over the crown')

# ------------------------------------------------------------------------------------------------------------------ the awning and the rings (Read from the repository)
import awning_lib as AL
AW, AWP = AL.AW, AL.AWP
_aw_off, _aw_slope = AL.y_off, AL.slope
footway_y = AL.footway_y
awning_underside_above_footway = AL.underside_above_footway
clear_at_height = AL.clear_at_height


WALK = dict(
    x_range_m=[9.5, 12.5], heights_m=[0.0, 2.0], rear_face_z_m=3.400, stallriser_face_z_m=4.975,
    ground_clear_m=round(4.975 - 3.400, 3),
    awning=dict(prop='awning_02 over the fish market (E18)', piece='prop_awning_02_0 in vignette-pieces.json', x_m=[10.5, 13.5], z_m=[3.39, 5.125], front_edge_z_m=3.39, valance_bottom_above_footway_m=round(_aw_off + AW['valance_bottom_mesh_y'] - footway_y(3.39), 3),
                body_underside_above_footway_at_front_m=round(awning_underside_above_footway(3.395), 3), body_slope=round(_aw_slope, 4), mesh=AW,
                note='read from the glb: the body falls from the fascia\'s underside at the wall to its front edge, with a scalloped valance hanging 0.32 m below that edge; the review\'s estimate (the front edge 1.57 m over the footway, clear about 1.0 m at 2.0 m head height) assumed a straight line from the valance\'s bottom'),
    clear_at_heights_m={str(h): clear_at_height(h) for h in (0.0, 1.0, 1.57, 1.8, 1.9, 2.0)},
    clear_at_head_2_0_review_estimate_m=round(4.975 - (3.39 + (2.0 - 1.57) / (2.95 - 0.057 - 1.57) * 1.7351), 3),
    rule='the free width between the rail\'s rear face and the nearest fixed projection (the stallriser face 4.975 at every height, the awning\'s underside above 1.9 m) for a body from 0 to 2.0 m high, in x 9.5 to 12.5, at least 0.68')
WALK['min_clear_m'] = min(WALK['clear_at_heights_m'].values())
RINGS_KIT = [[-110.05, -62.0], [-110.05, -32.0]]       # south_quay_geom._quay_furniture: for y in (-62.0, -32.0): _ring(kit, rings, (jx1 - COPING_NOSE_M, y), ...) with jx1 = -110.0

# ------------------------------------------------------------------------------------------------------------------ calibration, per object
cal = dict(method='horizon method of the bollards and kerbs targets (calibrate.py): camera height above a brick wall\'s foot = 75 mm x tan(angle of the foot) / (course pitch in tan units); the pitch by a fold of the column-band profile',
           horizon_anchors=anchors, objects={}, first_version=dict(R3B=FIRST_H['R3B'], R3A=FIRST_H['R3A'], R3D=FIRST_H['R3D'], LHB=FIRST_H['LHB'], what='the first version pooled one height for a whole panorama (0.97 Bethnal Green; 1.12 Urban Street 01 and Limehouse); the fresh review showed that two of the three pooled heights mix different grounds'))
for k, O in OBJECTS.items():
    D_ = dict(pano=O['pano'], h_cam=O['h_cam'], err=O['err'], ground=O['ground'], anchors=O['anchors'], excluded=O['excluded'], corroboration=O['corroboration'], why=O['why'],
              scale_from_first_version=O['scale'], first_version_h=FIRST_H[k])
    if 'quoted' in O: D_['quoted'] = O['quoted']
    cal['objects'][k] = D_
cal['review_remeasure_16k'] = dict(source='TARGET-REVIEW.md narrow point 1: the reviewer measured at 16k on the same three panoramas (CC0, Andreas Mischok)', R3B_gate_pier=0.942, R3B_rectified_pier=0.941, R3A_wall=1.017, R3D_wall=1.148, R3D_wall_bands=[1.13, 1.16], LHB_wall=1.09, LHB_pavers=[1.12, 1.15])
cal['camera_note'] = ('None of the panoramas was taken at 1.6 m: R3B 0.945, R3A 1.02, R3D 1.15, LHB 1.13, each at its own ground. Every length below is +-6 % in absolute size (R3A +-8 %); counts, ratios and pitches are exact to the pixel.')
T['calibration'] = cal

T['photo_frames'] = {k: dict(F) for k, F in FRAMES.items()}
T['photo_measurements'] = dict(R3B_auto=R3B, hand_reads=HR, hand_reads_as_read_at_first_version=PM['hand_reads_as_read_at_first_version'], scale_from_first_version=PM['scale'])
T['street_fixtures'] = dict(walking_strip=WALK, kit_rings_jetty_m=RINGS_KIT)


def _circle(r, n=32, cx=0.0, cy=0.0):
    return [[round(cx + r * math.cos(2 * math.pi * k / n), 3), round(cy + r * math.sin(2 * math.pi * k / n), 3)] for k in range(n)]


def _stadium(length, width, n=8):
    r = width / 2.0
    L = length - width
    pts = []
    for k in range(n + 1):
        a = -math.pi / 2 + math.pi * k / n
        pts.append([round(L / 2 + r * math.cos(a), 3), round(r * math.sin(a), 3)])
    for k in range(n + 1):
        a = math.pi / 2 + math.pi * k / n
        pts.append([round(-L / 2 + r * math.cos(a), 3), round(r * math.sin(a), 3)])
    return pts


def _tube(od, wall):
    return dict(outer=_circle(od / 2.0), inner=_circle(od / 2.0 - wall), od=od, wall=wall)


def _rrect(w, h, r, n=6):
    """a rounded rectangle of width w (u) and height h (v), corner radius r, centred, counter-clockwise from the lower right"""
    pts = []
    for (cx, cy, a0) in ((w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90.0 * k / n)
            pts.append([round(cx + r * math.cos(a), 3), round(cy + r * math.sin(a), 3)])
    return pts


def _rhs(w, h, t, ro, ri):
    return dict(outer=_rrect(w, h, ro), inner=_rrect(w - 2 * t, h - 2 * t, ri), width=w, height=h, wall=t, outer_radius=ro, inner_radius=ri)


def _hex(af):
    R = af / (2 * math.cos(math.pi / 6))
    return [[round(R * math.cos(math.pi / 6 + k * math.pi / 3), 3), round(R * math.sin(math.pi / 6 + k * math.pi / 3), 3)] for k in range(6)]


def _catenary(x0, x1, z_eye, sag, step=100.0):
    span = x1 - x0
    lo, hi = 1.0, 1e8
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid * (math.cosh(span / (2 * mid)) - 1) > sag:
            lo = mid
        else:
            hi = mid
    a = (lo + hi) / 2
    xm = (x0 + x1) / 2
    n = max(2, int(round(span / step)))
    return [[round(x0 + span * k / n, 2), round(z_eye - sag + a * (math.cosh((x0 + span * k / n - xm) / a) - 1), 2)] for k in range(n + 1)]


# ------------------------------------------------------------------------------------------------------------------ the kinds
kinds = {}

# ============================================================== A1: the kerbside pedestrian guard rail panel (E8), in the fresh review's form
C2C = 2000.0
POST_W, POST_D, POST_T, POST_H = 50.0, 30.0, 3.0, 1030.0
TOP_TOP, TOP_W, TOP_Hh, TOP_T = 1000.0, 50.0, 30.0, 3.0          # RHS laid flat: 50 across (y), 30 high (z)
TOP_AXIS = TOP_TOP - TOP_Hh / 2.0                                # 985
TOP_UNDER = TOP_TOP - TOP_Hh                                     # 970
BOT_W, BOT_Hh, BOT_T, BOT_AXIS = 40.0, 20.0, 2.5, 200.0
FACE_IN = C2C / 2.0 - POST_W / 2.0                               # 975
FACE_OUT = C2C / 2.0 + POST_W / 2.0                              # 1025
N_BARS, BAR_D = 17, 12.0
_xf_old = 975.85                                                 # the first version's bar list is kept unchanged (the review: "unchanged x list")
_gap_old = (2 * _xf_old - N_BARS * BAR_D) / (N_BARS + 1)
BAR_PITCH = _gap_old + BAR_D
BAR_X = [round(-_xf_old + _gap_old + BAR_D / 2.0 + i * BAR_PITCH, 2) for i in range(N_BARS)]
BAR_Z = [BOT_AXIS + BOT_Hh / 2.0, TOP_UNDER]                     # 210 to 970
GAP_BARS = round(BAR_PITCH - BAR_D, 2)
GAP_POST = round(FACE_IN - (abs(BAR_X[0]) + BAR_D / 2.0), 2)
PLATE_T, BOLT_AF_HEAD, BOLT_HEAD_H, BOLT_AF_NUT, BOLT_NUT_H, BOLT_THREAD = 6.0, 17.0, 7.0, 17.0, 8.0, 3.0
BOLT_ZS = [TOP_AXIS, BOT_AXIS]
bolts = []
for sx in (-1, 1):
    for z in BOLT_ZS:
        bolts.append(dict(post_x=sx * C2C / 2, z=z, y=0.0, head_x=[sx * (FACE_IN - PLATE_T - BOLT_HEAD_H), sx * (FACE_IN - PLATE_T)], plate_x=[sx * (FACE_IN - PLATE_T), sx * FACE_IN],
                          nut_x=[sx * FACE_OUT, sx * (FACE_OUT + BOLT_NUT_H)], thread_end_x=sx * (FACE_OUT + BOLT_NUT_H + BOLT_THREAD)))
X_MAX = FACE_OUT + BOLT_NUT_H + BOLT_THREAD                      # 1036
rnd = random.Random(1990)
patch_pts = []
for k in range(24):
    a = 2 * math.pi * k / 24
    r0 = 125.0 / max(abs(math.cos(a)), abs(math.sin(a)))            # a 250 x 250 square's edge at this angle
    patch_pts.append([round(r0 * math.cos(a) + rnd.uniform(-20, 20) * (1 if abs(math.cos(a)) > abs(math.sin(a)) else 0), 1), round(r0 * math.sin(a) + rnd.uniform(-20, 20) * (0 if abs(math.cos(a)) > abs(math.sin(a)) else 1), 1)])
for p_ in patch_pts:                                              # the footway side (local y < 0, away from the carriageway) is one straight cut flag edge
    if p_[1] < -100:
        p_[1] = -125.0
A1 = dict(
    id='A1', name='guard_rail_panel', title='Kerbside pedestrian guard rail, one 2.0 m panel of rectangular hollow-section rails bolted to two posts (the scene\'s E8)',
    basis='Judgement, the fresh review\'s form (both sides are judgement: no photograph of a guard rail was reachable; see section 3 of TARGET.md): rectangular hollow-section posts and rails, round-bar infill, bolted panel ends, galvanised. The scene\'s round primitives (post 0.05, rail 0.04) were the first version\'s only basis for round tube and its own search-summary lead said "posts 50 x 30 mm"; the review\'s form is also what that lead describes. The infill, the 2.0 m panel, the 1.0 m height, x 10.0 to 12.0 and the axis z 3.375 are unchanged',
    frame='local: x along the panel (0 at its middle), y across (0 on the rail line, + toward the carriageway), z up from the flag top at the posts; pivot at the middle of the panel on the ground',
    panel=dict(centre_to_centre=C2C, height=TOP_TOP, overall_height=POST_H,
               post=dict(section='RHS 50 x 30 x 3.0, the 50 face along the run (x), the 30 across (y); outer corner radius 4.5, inner 1.5', width=POST_W, depth=POST_D, wall=POST_T, height=POST_H, x=[-C2C / 2, C2C / 2], face_in_x=FACE_IN, face_out_x=FACE_OUT, proud_of_top_rail=POST_H - TOP_TOP),
               cap=dict(what='a welded 3 mm flat cap plate flush with the four sides, edges broken R1', thickness=3.0, z=[POST_H - 3.0, POST_H], edge_radius=1.0, outline_radius=4.5),
               top_rail=dict(section='RHS 50 x 30 x 3.0 laid flat: 50 across (y), 30 high (z)', width=TOP_W, height=TOP_Hh, wall=TOP_T, axis_z=TOP_AXIS, top_z=TOP_TOP, underside_z=TOP_UNDER, x=[-FACE_IN, FACE_IN]),
               bottom_rail=dict(section='RHS 40 x 20 x 2.5 laid flat: 40 across (y), 20 high (z)', width=BOT_W, height=BOT_Hh, wall=BOT_T, axis_z=BOT_AXIS, z=[BOT_AXIS - BOT_Hh / 2, BOT_AXIS + BOT_Hh / 2], x=[-FACE_IN, FACE_IN]),
               infill=dict(count=N_BARS, diameter=BAR_D, section='round solid mild-steel bar, vertical, welded to both rails with a 2 mm fillet at each end', x=BAR_X, z=BAR_Z, pitch=round(BAR_PITCH, 2), clear_gap_between_bars=GAP_BARS, clear_gap_bar_to_post_face=GAP_POST,
                           gap_rule='every clear gap at most 100 (a 100 mm sphere may not pass: the present-day safety rule and the search-summary lead of 12 mm bars at 110 to 112 centres, Judgement); the photographed bar railings have gaps of 61 to 100'),
               end_plates=dict(thickness=PLATE_T, outline='the rail\'s own outline (50 x 30 and 40 x 20), welded to the rail end and bearing on the post\'s inner face at x +-975'),
               bolts=dict(count=4, per='panel', size='M10', head=dict(across_flats=BOLT_AF_HEAD, height=BOLT_HEAD_H, where='on the panel side, against the end plate, inside the rail\'s end: hidden'),
                          nut=dict(across_flats=BOLT_AF_NUT, height=BOLT_NUT_H, where='on the post\'s OUTER face (x +-1025), visible from the pavement end of the panel'), thread_beyond_nut=BOLT_THREAD, z=BOLT_ZS, y=0.0, list=bolts,
                          finish='the bright steel is painted over (black variants) and rust-streaked below the nut; on the galvanised default the nut is bare zinc with a rust streak'),
               weld=dict(bead=2.0, what='2 mm fillet at each bar end and each end plate; the cap plate is welded all round (a 1 mm bead, ground flush on the sides); not ground off elsewhere')),
    ground=dict(kind='the posts are concreted into the footway; the flag is cut for each and the cut made good with a dark tarmac reinstatement patch', patch=dict(size=[250.0, 250.0], ragged_edge=20.0, flush_with_flags=3.0, srgb=[45, 43, 41], roughness=0.85,
                what='about 250 x 250 round the post, ragged edges +-20, flush with the flags to +-3; the footway-side edge is one straight cut flag edge; a 5 to 15 mm dark grit joint where the patch meets the flags', outline_xy=patch_pts, joint=[5.0, 15.0]), below_ground_not_modelled=400.0),
    bbox=dict(x=[-X_MAX, X_MAX], y=[-TOP_W / 2, TOP_W / 2], z=[0.0, POST_H], note='x +-1036 includes the nuts and 3 mm of thread; y +-25 is the top rail laid flat'),
    ends='the panel ends at its posts: an end post is the same post with the same cap; no return, no end rail, no stay (the one panel stops at x 12.0 beside the gully)',
    joins='a second panel (none on this street) would bolt to the same post\'s other face with the same bolt; the bars are not offset',
    edges='post and rail corners rounded (outer R4.5 on the 3.0 wall, R3.75 on the 2.5 wall); the post cap\'s edges broken R1; bar ends hidden in 2 mm welds',
    fixings='an M10 bolt at each of the four rail ends: head on the panel side hidden inside the rail end, nut on the post\'s outer face with 3 mm of thread beyond it',
    seams='the RHS\'s longitudinal weld seam shows as a 0.4 mm ridge on the narrow face turned to the footway (Judgement)',
    marks='none: no maker\'s plate, no council number, no crest, no stencilled letters',
    paint=dict(default='galvanised, weathered dull grey, streaked; no paint', srgb=[118, 120, 122], roughness_words='dull, slightly sheened, 0.55', roughness=0.55, metal=1,
               basis='Judgement, agreed with the review: BS 3049-pattern panels were galvanised steel and painting was the owner\'s option, so weathered zinc is at least as likely as black for a provincial highway authority in 1990; no photograph either way (the photographed black ironwork is cast and wrought iron, not galvanised steel). Black over galvanising stays as 45 % of the conditions. No bands, no reflective sleeves, no stripes.',
               details=['dark run-marks below the bolts (60, 56, 52) 40 to 150 long', 'white zinc bloom (200, 200, 196) in patches to 150 high at the feet', 'rust streak (110, 60, 32) from each nut', 'the road face grimed brown-grey by tyre spray to about 500']),
    black_condition=dict(srgb=[24, 24, 26], roughness=0.42, metal=0, note='black gloss over galvanising: the black measured on the cast ironwork in two panoramas ((22, 21, 21) and (23, 24, 28)) and the bollards target\'s'),
    wear=['the road face grimed brown-grey by tyre spray to about 500 mm, the footway face cleaner',
          'top rail polished bright along its upper (flat) face where hands rest, in patches 150 to 300 long (150, 150, 152)',
          'galvanised default: bright zinc scuffs on the lower rail\'s road face (kicked) and at the post caps, white zinc bloom at the feet, dark run-marks under the bolts; black variants: paint chipped to grey zinc at the same places',
          'rust bloom (110, 60, 32) at the nuts, the weld ends and the post feet, 0 to 1',
          'one or two bars bent out 5 to 15 mm at 300 to 600 high (a bumped panel), 0 to 2 per panel',
          'a lean of the posts of 0 to 1 degree toward the carriageway',
          'a sticker or poster remnant on the top rail 0 to 2 (pale paper scraps, no lettering)',
          'cigarette ends and a sweet wrapper lodged between the kerb and the post (the litter set\'s, not this kit\'s)'],
    alternative_recorded=dict(what='the first version\'s round-tube form, set aside: posts round tube 48.3 x 3.2 with flat plug caps flush with the rail top (1000), rails round tube 42.4 (axis 978.8) and 33.7 (axis 200), saddle-cut and welded, no visible fixings, black',
                              why_set_aside='its only basis was the scene stand-in\'s cylinders (post 0.05, rail 0.04); its own lead said "posts 50 x 30 mm"; the fresh review judged a 1976-pattern panel to be RHS and bolted. Both are judgement. It is not to be built; it stays here so that the confirmation from the PC (two dated photographs) can pick either'))
kinds['A1'] = A1
A1['profiles'] = dict(
    note='sections and profiles as point lists, millimetres: RHS as outer and inner rounded rectangles in (u across, v up) coordinates centred on the section, the post in plan (x along the run, y across); hex outlines; the cap plate; the reinstatement patch (A1.ground.patch.outline_xy)',
    post_section=_rhs(POST_W, POST_D, POST_T, 4.5, 1.5), top_rail_section=_rhs(TOP_W, TOP_Hh, TOP_T, 4.5, 1.5), bottom_rail_section=_rhs(BOT_W, BOT_Hh, BOT_T, 3.75, 1.25), bar_section=dict(outer=_circle(BAR_D / 2.0), od=BAR_D),
    cap_plate=dict(outline=_rrect(POST_W, POST_D, 4.5), thickness=3.0, edge_radius=1.0),
    bolt_head_hex=_hex(BOLT_AF_HEAD), bolt_nut_hex=_hex(BOLT_AF_NUT), bolt_head_height=BOLT_HEAD_H, bolt_nut_height=BOLT_NUT_H, bolt_shank_diameter=10.0, thread_beyond_nut=BOLT_THREAD,
    end_plate_outlines=dict(top=_rrect(TOP_W, TOP_Hh, 4.5), bottom=_rrect(BOT_W, BOT_Hh, 3.75), thickness=PLATE_T),
    weld_fillet=[[0.0, 0.0], [2.0, 0.0], [0.0, 2.0]])

# ============================================================== Q2: the quay tube railing (two-rail, and rail with chain)
Q_bay, Q_short = 3000.0, 1400.0
q_post_od, q_post_wall, q_post_h = 76.1, 5.0, 1100.0
q_top_od, q_top_wall, q_low_od = 60.3, 3.6, 42.4
q_top_axis, q_low_axis = 1000.0, 500.0
q_xface = Q_bay / 2 - q_post_od / 2
eye_hole_d, eye_from_post = 24.0, 45.0
q_eye_x = Q_bay / 2 - q_post_od / 2 - eye_from_post
chain_sag = 200.0
span_eye = 2 * q_eye_x
arc = span_eye + 8.0 * chain_sag ** 2 / (3.0 * span_eye)
span_short = Q_short - q_post_od - 2 * eye_from_post
sag_short = round(chain_sag * span_short / span_eye, 1)
arc_short = span_short + 8.0 * sag_short ** 2 / (3.0 * span_short)
Q2 = dict(
    id='Q2', name='quay_tube_railing', title='Quay tube railing: two tube rails on round steel posts (Q2a), or one tube rail and a swag of chain (Q2b), on the jetty only',
    basis='Judgement: no photograph of a tube railing on a quay was reachable. The chain is the bollards target\'s plain chain (Read there) and its sag is Photo on the marina chain (LHB, 215 to 240). The asset plan names the kit ("two-rail tube railing with chain"); the Hull photograph R08 of 1989 (read by an earlier session) shows a chain-edged quay. Second version: the top rail is 60.3 x 3.6 for the 3.0 m bays (the review\'s first choice; 2.0 m bays with a 48.3 rail was its second)',
    frame='local: x along the run (0 at the middle of a bay), y across (0 on the rail line, + toward the water), z up from the apron at the post foot; pivot at the middle of the bay on the ground',
    bay=dict(centre_to_centre=Q_bay, short_end_bay=Q_short, allowed=[3000.0, 1400.0], note='bays of 3.0 m (the bollards target\'s post spacing); the return\'s end bay is 1.4 m'),
    post=dict(od=q_post_od, wall=q_post_wall, height=q_post_h, section='round steel tube, 76.1 mm (3 inch nominal bore)', cap=dict(kind='pressed domed cap, welded', od=80.0, rise=14.0, z=[q_post_h - 14.0, q_post_h]),
              base_plate=dict(size=[200.0, 200.0], thickness=12.0, holes=dict(diameter=18.0, pitch=150.0, count=4), fixing='four M16 studs in the cope with hex nuts, 24 across flats and 13 high, studs 10 proud of the nuts',
                              grout='25 mm cement grout bedding, a 20 mm fillet round the plate, stained dark'), weld='a 5 mm fillet all round the post foot on the plate'),
    top_rail=dict(od=q_top_od, wall=q_top_wall, axis_z=q_top_axis, top_z=q_top_axis + q_top_od / 2, x=[-q_xface, q_xface], section='round steel tube 60.3 x 3.6 (2 inch nominal bore), saddle-welded to the posts; the review\'s amendment for a 3.0 m span (48.3 would be spindly)'),
    low_rail=dict(od=q_low_od, wall=2.6, axis_z=q_low_axis, x=[-q_xface, q_xface], section='round steel tube 42.4 (Q2a only)'),
    chain=dict(replaces='the low rail (Q2b only)', eyes=dict(z=q_low_axis, x=[-q_eye_x, q_eye_x], ear=dict(width=40.0, height=70.0, thickness=8.0, hole_diameter=eye_hole_d, hole_centre_from_post_surface=eye_from_post, what='a flat-bar ear welded to the post on the rail line, facing the bay; ONLY on the sides that face a Q2b bay: none on a Q2a bay, one at a Q2a/Q2b corner post, two at a post between two chain bays, one at a run\'s end post')),
               link=dict(bar=13.0, kind='plain short link', inner_length=39.0, inner_width=18.0, outer_length=65.0, outer_width=44.0, pitch=39.0, note='the bollards target\'s plain chain, unchanged (agrees)'),
               sag=chain_sag, sag_basis='Photo LHB: the marina chain\'s two swags sag 215 (upper) and 240 (lower), mean 227 +-35, over a 2840 span (8 %); the bollards target\'s 150 is Judgement and is low; 200 (7 %) here',
               span_between_eyes=round(span_eye, 2), arc_length=round(arc, 1), links=int(round(arc / 39.0)), short_bay=dict(span_between_eyes=round(span_short, 2), sag=sag_short, arc_length=round(arc_short, 1), links=int(round(arc_short / 39.0)), note='the 1.4 m end bay of the return: the same 7 % sag'),
               curve='a catenary hanging from the two eye holes: z(x) = z_eye - sag + a (cosh(x/a) - 1) with a = span^2 / (8 sag)'),
    bbox=dict(x=[-(Q_bay / 2 + q_post_od / 2), Q_bay / 2 + q_post_od / 2], y=[-100.0, 100.0], z=[0, q_post_h]),
    ends='a run ends at a post of the same kind; at a corner two runs share one post, rails mitred to it; the return\'s last bay is 1.4 m',
    edges='saddle cuts and fillet welds; the cap\'s rim R3; the base plate\'s edges R2',
    marks='none',
    paint=dict(default='black, satin over galvanising', srgb=[24, 24, 26], roughness_words='satin, chalky on the sea side', roughness=0.55, metal=0, note='the same black and roughness as the K5 chain post and the K6 mooring bollards beside it (bollards target); the nuts and studs bright steel (150, 150, 152), dull rust at the threads'),
    wear=['salt bloom (pale, dry) on the sea face of posts and rails to 1.0 m; rust at the base plate, the nuts and the weld rings, 0 to 1',
          'paint rubbed bright on the upper face of the top rail at the walking places (150, 150, 152)',
          'the chain black, rubbed bright where the links touch (the bollards target); links slightly rusty at their crossings',
          'a rope scuff on one post at 400 to 600 high, 0 to 1 per run',
          'the apron around the plates stained dark by oil and rain'])
kinds['Q2'] = Q2
Q2['profiles'] = dict(
    note='sections and profiles as point lists, millimetres',
    post_section=_tube(q_post_od, q_post_wall), top_rail_section=_tube(q_top_od, q_top_wall), low_rail_section=_tube(q_low_od, 2.6),
    cap_rz=[[0.0, q_post_h], [20.0, q_post_h - 3.0], [34.0, q_post_h - 8.0], [40.0, q_post_h - 12.0], [40.0, q_post_h - 14.0], [38.05, q_post_h - 14.0]],
    base_plate_outline=[[-100.0, -100.0], [100.0, -100.0], [100.0, 100.0], [-100.0, 100.0]], base_plate_holes=[[-75.0, -75.0], [75.0, -75.0], [75.0, 75.0], [-75.0, 75.0]], hole_diameter=18.0,
    nut_hex_outline=_hex(24.0), nut_across_flats=24.0, nut_height=13.0, stud_diameter=16.0, stud_above_nut=10.0,
    ear_outline=dict(outline=[[0.0, -35.0], [(eye_from_post + 20.0), -35.0], [(eye_from_post + 20.0), 35.0], [0.0, 35.0]], hole_centre=[eye_from_post, 0.0], hole_diameter=eye_hole_d, thickness=8.0),
    link_inplane=dict(outline=_stadium(65.0, 44.0), hole=_stadium(39.0, 18.0)), link_edge_on=[[-32.5, -6.5], [32.5, -6.5], [32.5, 6.5], [-32.5, 6.5]],
    catenary_xz=_catenary(-q_eye_x, q_eye_x, q_low_axis, chain_sag), catenary_short_xz=_catenary(-span_short / 2, span_short / 2, q_low_axis, sag_short, 50.0),
    catenary_note='z of the chain\'s centre line along x, eyes at z 500, lowest point z 300 (the 3.0 m bay) and 413 (the 1.4 m end bay)')

# ============================================================== reserve kinds, photographed, NOT placed on the street
_hd = HR['R3B']['bar_head']['v']
_knop_r = max(r for r, z in _hd)
_knop_z = [z for r, z in _hd if r == _knop_r][0]
_ring2 = [(r, z) for r, z in _hd if z > _knop_z + 20 and r > 12 and r < 30][:3]
R3B_k = dict(
    id='R3B', name='park_railing_tall', title='Tall cast-iron park railing on a brick plinth with a hinge post (RESERVE, not on Quay Street)', placed=False, frame_id='R3B',
    basis='Photo, Bethnal Green Entrance (2019), the main photograph: 1 mm a pixel elevation at 0.945 +-0.02 m (the camera height at the gate pier\'s ground); lengths +-6 %',
    plinth=dict(coping_top_z=HR['R3B']['coping_top_z'], stone_coping='a stone slab about 50 thick with a weathered top, overhanging the brick by about 25', brick='red-brown brick, four courses at 75 below the coping, moss and lichen on the north face',
                pier=dict(width=HR['R3B']['pier_width'], top='a stone pier cap with a low pyramidal weathering at the coping level')),
    rails=dict(bottom_axis_z=HR['R3B']['bottom_rail_axis_z'], mid_axis_z=HR['R3B']['mid_rail_axis_z'], top_axis_z=HR['R3B']['top_rail_axis_z'], section='flat bar about 20 high by 10 thick, bars passed through or riveted to them (not resolved)'),
    bars=dict(pitch=R3B['bar_pitch_mm'], count_measured=len(R3B['bar_centres_s_mm']), first_s=R3B['bar_fit_first_s_mm'], diameter=round(17.0 * SCALE['R3B'], 1), diameter_err=3.0, section='round', tall_every=2,
              short_tip_z=HR['R3B']['short_bar_tip_z'], tall_tip_z=HR['R3B']['tall_bar_tip_z'], head_rz=HR['R3B']['bar_head']['v'], foot='a small ball end (about 20 across) a few mm below the bottom rail',
              knop=dict(width=round(2 * _knop_r, 1), z=_knop_z, text='a turned knop about %d across at z %d, a ring about 44 across just above it, a spire to the tip' % (round(2 * _knop_r), round(_knop_z))),
              leaf_note='the gate leaf right of the hinge post is swung open toward the camera: the plane magnifies it (its bars read at %.1f) so it is not measured' % R3B['leaf_bar_pitch_mm'],
              note='all bars at %.1f (three inches is 76.2: the pitch at the corrected camera height is within 0.5 %% of it); every second bar rises to a spire; the others stop at the middle rail with a small spear (z %d)' % (R3B['bar_pitch_mm'], round(HR['R3B']['short_bar_tip_z']['v']))),
    post=dict(axis_s=HR['R3B']['post_axis_s'], shaft_width=HR['R3B']['post_shaft_width'], collar_width=HR['R3B']['post_collar_width'], urn_width=HR['R3B']['urn_width'], top_z=HR['R3B']['post_top_z'], kind='cast iron, round, with a fluted collar at the top rail, a vase and a spire; a boss and a strap hinge at the bottom rail level (a gate stile)'),
    height_to_tip=HR['R3B']['tall_bar_tip_z']['v'], spacing_of_posts='not seen: one hinge post in 3.9 m of railing',
    paint=dict(srgb=[24, 24, 26], note='black, semi-gloss, chalky on the plinth side; measured medians of the dark pixels (36, 43, 30) are polluted by foliage; the R3A and LHB blacks are (22, 21, 21) and (23, 24, 28)'),
    wear=['paint flaking at the post collars; bright rust spots at the bar feet', 'moss and lichen on the plinth and a green-black stain under the coping', 'a notice board and a locked-site sign wired to the bars (not drawn)'])
R3A_k = dict(
    id='R3A', name='area_railing_on_dwarf_wall', title='Area railing on a two-stage dwarf wall in front of a housing block (RESERVE, not on Quay Street)', placed=False, frame_id='R3A',
    basis='Photo, Bethnal Green Entrance (2019): oblique view, 10 mm a pixel along the wall, lengths +-8 %; camera height 1.02 +-0.03 m at its own wall; heritage replica or 1980s work: unknown',
    wall=dict(top_z=HR['R3A']['wall_top_z'], string_z=HR['R3A']['wall_string_z'], courses='lower stage 4 courses of blue-black engineering brick under a blue bullnose string, red wall five stretcher courses, a blue bullnose coping course; one brick thick (215, Judgement)'),
    rails=dict(bottom_axis_z=HR['R3A']['bottom_rail_axis_z'], mid_axis_z=HR['R3A']['mid_rail_axis_z'], top_axis_z=HR['R3A']['top_rail_axis_z']),
    bars=dict(pitch_all=HR['R3A']['bar_pitch_all'], tall_first_s=HR['R3A']['tall_first_s'], left_run_max_s=HR['R3A']['left_run_max_s'], tall_tip_z=HR['R3A']['tall_tip_z'], thick_width=HR['R3A']['bar_thick_width'],
              pattern='THE NUMBERS ARE THE LEFT RUN\'S (preview s < %d): thick tall bars with spear heads every %d and thin short bars with lily plaques between them to the middle rail; right of the cast post the photograph shows a second pattern (fleur-de-lis heads about half a pitch out of step) that is NOT measured and not drawn' % (round(HR['R3A']['left_run_max_s']['v']), round(2 * HR['R3A']['bar_pitch_all']['v']))),
    post=dict(top_z=HR['R3A']['post_top_z'], shaft_width=HR['R3A']['post_shaft_width'], kind='cast post with a vase and ball, scroll knees to the top rail'),
    paint=dict(srgb=[22, 21, 21], note='black'))
_r3d_c = _np.array(HR['R3D']['bar_centres_s']['v'], float)
_r3d_fit = _np.polyfit(_np.arange(10), _r3d_c, 1)
R3D_k = dict(
    id='R3D', name='low_garden_railing_and_gate', title='Low green railing, wall and gate of a council-estate front garden (RESERVE, not on Quay Street)', placed=False, frame_id='R3D',
    basis='Photo, Urban Street 01 (2019): 1 mm a pixel elevation at 1.15 +-0.02 m (the camera height at the garden wall\'s own foot); lengths +-6 %; a 1960s to 80s estate form',
    wall=dict(top_z=HR['R3D']['wall_top_z'], courses='eight courses of dark brick at 75 plus a header coping; no piers in the window'),
    rails=dict(bottom_axis_z=HR['R3D']['bottom_rail_axis_z'], top_axis_z=HR['R3D']['top_rail_axis_z'], section='flat bar'),
    bars=dict(pitch=dict(v=round(float(_r3d_fit[0]), 2), err=3, how='line fit of the ten hand-read bar centres (hand_reads.R3D.bar_centres_s)'), first_s=round(float(_r3d_fit[1]), 2), width=HR['R3D']['bar_width'], tip_z=HR['R3D']['bar_tip_z'], section='round, plain small spear points'),
    gate=dict(width=HR['R3D']['gate_width'], top_z=HR['R3D']['gate_top_z'], pattern='a leaf of plain bars with two C-scrolls at mid height and a scroll at the foot, hung from a brick pier'),
    paint=dict(srgb=HR['R3D']['paint_srgb']['v'], name='dark green', roughness=0.5, note='the only coloured ironwork reached; a council-estate green'))
kinds['R3B'] = R3B_k
kinds['R3A'] = R3A_k
kinds['R3D'] = R3D_k
R3B_k['profiles'] = dict(bar_head_rz=HR['R3B']['bar_head']['v'], bar_head_error=HR['R3B']['bar_head']['err'],
                         hinge_post_rz=[[HR['R3B']['post_shaft_width']['v'] / 2, 2000 * SCALE['R3B']], [HR['R3B']['post_collar_width']['v'] / 2, 2000 * SCALE['R3B'] + 10], [HR['R3B']['post_collar_width']['v'] / 2, 2035 * SCALE['R3B']], [42.5, 2060 * SCALE['R3B']], [42.5, 2110 * SCALE['R3B']],
                                        [HR['R3B']['urn_width']['v'] / 2, 2150 * SCALE['R3B']], [HR['R3B']['urn_width']['v'] / 2, 2200 * SCALE['R3B']], [30, 2250 * SCALE['R3B']], [12, 2300 * SCALE['R3B']], [5, 2350 * SCALE['R3B']], [0, HR['R3B']['post_top_z']['v']]],
                         note='(r, z) from the ground; read by eye on the 1 mm elevation, +-15 (blur 6 mm), already scaled to the corrected camera height')
T['kinds'] = kinds

# ------------------------------------------------------------------------------------------------------------------ placements
street_axis_z = 3.375
quay_basin = [[-110.4, -21.4], [-110.4, -18.4], [-110.4, -15.4]]
quay_tip = [[round(-110.4 - 3.0 * k, 2), -15.4] for k in range(1, 7)]
quay_return = [[-128.4, -18.4], [-128.4, -21.4], [-128.4, -22.8]]
_all_posts = quay_basin + quay_tip + quay_return
_bays = [dict(a=quay_basin[0], b=quay_basin[1], model='Q2a', length=3.0), dict(a=quay_basin[1], b=quay_basin[2], model='Q2a', length=3.0)]
_prev = quay_basin[2]
for p_ in quay_tip:
    _bays.append(dict(a=_prev, b=p_, model='Q2b', length=3.0))
    _prev = p_
for p_ in quay_return:
    _bays.append(dict(a=_prev, b=p_, model='Q2b', length=round(math.hypot(p_[0] - _prev[0], p_[1] - _prev[1]), 3)))
    _prev = p_
# ears: only on the sides that face a Q2b bay
_ears = []
for p_ in _all_posts:
    faces = []
    for bay in _bays:
        if bay['model'] != 'Q2b': continue
        for me, other in ((bay['a'], bay['b']), (bay['b'], bay['a'])):
            if me == p_:
                d_ = [round(other[0] - me[0], 3), round(other[1] - me[1], 3)]
                n_ = math.hypot(*d_)
                faces.append([round(d_[0] / n_, 3), round(d_[1] / n_, 3)])
    _ears.append(dict(post=p_, faces=faces))
_total_len = round(sum(b['length'] for b in _bays), 2)
T['placements'] = dict(
    rule='frames: A1 in the street recipe\'s frame (x along, z across, metres); Q2 in the south-quay kit\'s frame (x along Quay Street, y across, metres)',
    street=[dict(id='E8', kind='A1', side='east', count=1, panels=1, x_m=[10.0, 12.0], z_axis_m=street_axis_z, from_kerb_face_m=round(street_axis_z - 3.0, 4), behind_scene_kerb_back_m=round(street_axis_z - 3.125, 4),
                 behind_kerbs_target_back_m=round(street_axis_z - 3.170, 4), axis_basis='Read: vignette-feet.json (rail_post0/1 at z 3.375); the scene\'s "0.25 m back from the kerb" is taken from the kerb\'s back edge (3.125); the kerbs target widens the kerb to 170, leaving 0.205',
                 rear_face_z_m=round(street_axis_z + TOP_W / 2000.0, 4), road_face_z_m=round(street_axis_z - TOP_W / 2000.0, 4),
                 foot_note='the post feet stand on the flag top; the scene\'s foot level is y 0.05625 and the kerbs target\'s flag level is y 0.040: the builder reads the ground under the posts',
                 facing='the road side is the -z face (toward the carriageway); the bolts\' nuts face the panel\'s ends (x 9.964 and 12.036)', beside='the gully at x 12.0 in the channel (the grate 0.44 x 0.29 in the kerbs target) and the fish market\'s frontage and awning behind')],
    quay=[dict(id='Q2_basin_edge', kind='Q2a', frame='south-quay kit', line_x_m=-110.4, behind_nose_m=0.4, posts_xy_m=quay_basin, bays=2, bay_m=3.0, why='the last two bays of the jetty\'s basin edge before the light, cut back from the first version\'s seven so that the berth (the kit\'s mooring rings at y -62 and -32, K6 bollards, K7 cleats, the boat) stays open'),
          dict(id='Q2_tip', kind='Q2b', frame='south-quay kit', line_y_m=-15.4, behind_nose_m=0.4, posts_xy_m=quay_tip, bays=6, bay_m=3.0, shares_post_with='Q2_basin_edge at (-110.4, -15.4)', why='the jetty\'s end in front of the harbour light: the same posts with the chain in place of the low rail'),
          dict(id='Q2_seaward_return', kind='Q2b', frame='south-quay kit', line_x_m=-128.4, posts_xy_m=quay_return, bays=3, bay_m=[3.0, 3.0, 1.4], shares_post_with='Q2_tip at (-128.4, -15.4)',
               why='closes the open corner between the tip and the seaward parapet\'s end (x -130 to -128.4, y -23 to -15.4): the first version left it open "for boats", but boats do not lie on the exposed seaward side and that corner is where a visitor to the light would walk off; its end post stands 0.2 m from the parapet\'s inner face (x -128.6) and its end (y -23.0), the plate 0.1 m clear'),
          dict(id='quay_unrailed', kind=None, why='the north quay, the east quay and the jetty\'s berth stay unrailed except the bollards target\'s K5 chain posts about the ladder (x -69.5, y -40.5 to -31.5): working berths with boats alongside; a railing would stop the lines. The cope nose stays bare.')],
    kit_rings_jetty_m=RINGS_KIT, bays_detail=_bays, ears=_ears,
    counts=dict(street_posts=2, quay_posts=len(_all_posts), quay_bays=len(_bays), quay_length_m=_total_len, chain_bays=sum(1 for b in _bays if b['model'] == 'Q2b'), ears=sum(len(e['faces']) for e in _ears)),
    absent=dict(area_railings='none on Quay Street: every frontage stands on the building line (frontage_z 5.125, a doorstep only); the south-quay kit\'s walled yards have brick piers and boarded gates, no railings; no chapel or church stands on the street (the chapel is at x 100 in hook-cast.json, beyond the bend)',
                yard_gate='none: the yard mouth (x 21.0 to 24.0, west) is a 3.0 m gap with a dropped kerb, its two corners guarded by the bollards target\'s K1 posts, and the scene stands a held crowd-control barrier across it (E11, prop_crowd_control_barrier_0 at x 22.5, z -4.85); the town session decides whether it is ever gated',
                backdrop='the north approach\'s garden walls are knee-high stone boxes in the backdrop (terrace-front.py), not game objects'))

# ------------------------------------------------------------------------------------------------------------------ materials
T['materials'] = [
    dict(id='galvanised_weathered', srgb=[118, 120, 122], roughness=0.55, roughness_words='dull, slightly sheened', metal=1, use='A1 default (55 %): streaked weathered zinc'),
    dict(id='iron_black_semi', srgb=[24, 24, 26], roughness=0.42, roughness_words='semi-gloss, dulled', metal=0, use='A1 black conditions (45 %); R3B, R3A'),
    dict(id='iron_black_satin', srgb=[24, 24, 26], roughness=0.55, roughness_words='satin, chalky', metal=0, use='Q2, and the K5 and K6 beside it'),
    dict(id='iron_green', srgb=[38, 56, 36], roughness=0.50, roughness_words='satin', metal=0, use='R3D'),
    dict(id='zinc_bloom', srgb=[200, 200, 196], roughness=0.8, roughness_words='dry, chalky', metal=0, use='white zinc bloom at the feet of the galvanised A1'),
    dict(id='run_marks', srgb=[60, 56, 52], roughness=0.7, roughness_words='dull', metal=0, use='dark streaks below the bolts and nuts'),
    dict(id='bright_steel_rub', srgb=[150, 150, 152], roughness=0.35, roughness_words='polished by hands', metal=1, use='top rails\' upper face, nuts, studs, chain contacts'),
    dict(id='rust', srgb=[110, 60, 32], roughness=0.85, roughness_words='dry, matt', metal=0, use='blooms at feet, welds, nuts'),
    dict(id='tarmac_patch', srgb=[45, 43, 41], roughness=0.85, roughness_words='dull, gritty', metal=0, use='the reinstatement patch round each A1 post'),
]

# ------------------------------------------------------------------------------------------------------------------ variants
T['variants'] = dict(
    models=dict(A1=1, Q2=2, R3B=1, R3A=1, R3D=1),
    note='one panel on the street, so one A1; the asset plan\'s "1 kit" holds. Q2 has two models (a, b).',
    A1_conditions=[dict(id='A1_galvanised_weathered', share=0.55, srgb=[118, 120, 122], roughness=0.55, metal=1, note='DEFAULT: unpainted galvanising weathered dull grey, streaked, dark run-marks below the bolts, white zinc bloom at the feet'),
                   dict(id='A1_black_scuffed', share=0.30, srgb=[24, 24, 26], note='black over galvanising, scuffed, the nuts painted over and rust-streaked'),
                   dict(id='A1_black_chipped', share=0.15, srgb=[24, 24, 26], note='black with the chips down to grey zinc at the road side, the caps and the bolts')],
    seeds=dict(lean_deg=[0.0, 1.0], bent_bars=[0, 2], bend_mm=[5, 15], bend_z_mm=[300, 600], rust_foot=[0.0, 1.0], dirt_height_mm=[300, 600], rub_bright_patches=[0, 3], sticker_remnants=[0, 2], chips=[0, 10], patch_ragged_mm=[-20, 20]),
    Q2_conditions=['Q2a: two rails, salt bloom and rust at the plates', 'Q2b: rail and chain, links rusted at the crossings'])

# ------------------------------------------------------------------------------------------------------------------ photographs win / disagreements
T['photographs_win'] = [
    dict(element='post and rail sections of the guard rail', book='the scene\'s cylinders (post 0.05, rail 0.04) and the first version\'s round tubes (48.3, 42.4, 33.7); the search-summary lead "posts 50 x 30 mm"', photograph='none (no guard rail was photographed)',
         chosen='RHS, as the lead says: posts 50 x 30 x 3.0 to 1030, top rail 50 x 30 laid flat with its top at 1000, bottom rail 40 x 20 at 200, bolted panel ends (the fresh review\'s form). Judgement until a photograph is reached; both sides were judgement'),
    dict(element='infill of the guard rail', book='the scene\'s stand-in: five 25 mm bars in 2.0 m (clear gaps of 308); the asset plan "posts, rails, infill"',
         photograph='every photographed bar railing has its bars at 76.6 (R3B), 97 (R3D) or 120 (R3A, at 1.02 m) centres, so clear gaps of 60 to 105; none has a gap over 105. No guard rail was photographed',
         chosen='seventeen 12 mm bars at 109.1 centres (clear gap 97.1 between bars, 96.2 to a post face): Judgement from the analogues and the search-summary lead; the five-bar stand-in is replaced'),
    dict(element='lower rail height', book='the stand-in has its lower rail at 0.45 (half height)', photograph='R3D\'s bottom rail is 60 above its wall; R3B\'s 433 above the ground with a 336 plinth below it; the bars of both run to the bottom rail', chosen='lower rail axis at 200 (190 to 210): Judgement (no photograph)'),
    dict(element='the post top', book='none', photograph='none (R3B has cast finials, R3D plain spear points: neither applies to a steel guard rail)', chosen='the post stands 30 above the top rail with a welded flat cap plate (the fresh review; the first version had a plug cap flush with the rail)'),
    dict(element='fixings', book='the first version: "none visible" (a welded panel)', photograph='none', chosen='an M10 bolt at each rail end, nut on the post\'s outer face (the fresh review: a struck panel can be unbolted)'),
    dict(element='paint finish', book='"metal" in the scene; the first version: black over galvanising', photograph='all photographed ironwork is cast or wrought iron, black (22 to 24) except R3D\'s green (38, 56, 36): none is galvanised steel', chosen='weathered galvanised grey as the default (55 %), black 45 %: Judgement, agreed with the review'),
    dict(element='ground detail', book='the first version: a neat 20 mm bitumen ring', photograph='none', chosen='a ragged dark tarmac reinstatement patch about 250 x 250 round each post, one straight flag edge, a grit joint (the review)'),
    dict(element='camera height', book='1.6 m (the street writer\'s default); the first version\'s pooled 0.97 and 1.12', photograph='R3B 0.945, R3A 1.02, R3D 1.15, LHB 1.13, each at its own ground', chosen='the anchors in section 4; every length read at the first version\'s height was multiplied by 0.974, 1.052, 1.027 and 1.009'),
    dict(element='R3B bar heads', book='the first version: a vase swelling to 60 across at 2128, tip 2300', photograph='the 16k re-measurement: a turned knop 87 to 100 across (median 95) at 2090 to 2110, tips at 2255 to 2285 (at 0.97)', chosen='the review\'s profile, scaled to 0.945: a knop about 90 across, a tip at 2211 +-15'),
    dict(element='chain sag', book='the bollards target 150 (Judgement)', photograph='Photo LHB: 227 +-35 over 2840 (two swags: 215 and 240)', chosen='200 for Q2b; the bollards writer should raise K5\'s to 200'),
    dict(element='K5 post height', book='the bollards target 1135 at 1.17 m', photograph='LHB 1086 at 1.12 m, now 1096 at 1.13 m (3.4 % lower than 1135, the camera heights\' ratio 1.13 / 1.17 = 0.966)', chosen='no change: agrees inside the errors'),
    dict(element='the quay tube railing\'s bay', book='the bollards target\'s 3.0 m post-and-chain spacing', photograph='none', chosen='3.0 m kept with a 60.3 x 3.6 top rail (the review: 3 m bays of a 48.3 rail are spindly)'),
]

# ------------------------------------------------------------------------------------------------------------------ checks
def chk(name, what, expected, tol, unit, kind, basis='Judgement', **kw):
    d = dict(name=name, what=what, expected=expected, tol=tol, unit=unit, kind=kind, basis=basis)
    d.update(kw)
    return d


_near_k6 = min(math.hypot(p[0] - q[0], p[1] - q[1]) for p in _all_posts for q in [(-110.75, -45.0), (-110.75, -80.0), (-110.25, -52.0), (-110.25, -58.0), (-110.25, -64.0)])
_near_ring = min(math.hypot(p[0] - q[0], p[1] - q[1]) for p in _all_posts for q in RINGS_KIT)
_light = [(-121.4, -20.9), (-118.6, -18.1)]
_near_light = min(max(_light[0][0] - p[0], 0, p[0] - _light[1][0]) ** 2 + max(_light[0][1] - p[1], 0, p[1] - _light[1][1]) ** 2 for p in _all_posts) ** 0.5
C = [
    chk('A1_panel_length', 'distance between the two post axes', 2000, 5, 'mm', 'A1', 'Read: the scene (2.0 m) and vignette-feet (x 10 and 12)'),
    chk('A1_height_to_top_rail', 'top of the top rail above the flag top at the post', 1000, 10, 'mm', 'A1', 'Read: the scene (1.0 high)'),
    chk('A1_post_section', 'post section, along the run x across (RHS)', [50, 30], 2, 'mm', 'A1', 'Judgement: the fresh review; the search-summary lead "posts 50 x 30"'),
    chk('A1_post_wall', 'post wall', 3.0, 0.5, 'mm', 'A1'),
    chk('A1_post_top', 'post top above the flag top (30 over the top rail)', 1030, 10, 'mm', 'A1', 'Judgement: the fresh review'),
    chk('A1_top_rail_section', 'top rail section, across x high, laid flat; its top at 1000 +-10', [50, 30], 2, 'mm', 'A1', 'Judgement: the fresh review', top_z=[1000, 10]),
    chk('A1_bottom_rail_section', 'bottom rail section, across x high, laid flat', [40, 20], 2, 'mm', 'A1', 'Judgement: the fresh review'),
    chk('A1_bottom_rail_axis', 'bottom rail axis above the flag', 200, 15, 'mm', 'A1'),
    chk('A1_bar_count', 'infill bars between the posts', 17, 0, 'count', 'A1'),
    chk('A1_bar_diameter', 'infill bar diameter', 12, 1.5, 'mm', 'A1'),
    chk('A1_bar_gap_max', 'largest clear gap between bars, and bar to post face', 100, 0, 'mm (maximum)', 'A1', max=True),
    chk('A1_bar_gap', 'clear gap between bars (and bar to post face: 96.24)', 97.09, 1.5, 'mm', 'A1'),
    chk('A1_bars_touch_rails', 'each bar\'s ends lie on the bottom rail\'s top (z 210) and the top rail\'s underside (z 970)', [210, 970], 1.0, 'mm', 'A1'),
    chk('A1_bolts', 'M10 bolts at the rail ends: 4 per panel, each head on the panel side and its nut (17 across flats, 8 high, 3 mm thread beyond) on the post\'s OUTER face at x +-1025', 4, 0, 'count', 'A1', 'Judgement: the fresh review', nut_face_x=1025, nut_height=8, thread=3),
    chk('A1_bolt_heights', 'bolt axes at the rail axes', [985, 200], 5, 'mm', 'A1'),
    chk('A1_street_position', 'post axes at x 10.0 and 12.0, z 3.375', [10.0, 12.0, 3.375], 0.05, 'm', 'A1', 'Read: vignette-feet.json'),
    chk('A1_behind_kerb_back', 'axis behind the kerbs target\'s 170 kerb back edge (z 3.170)', 0.205, 0.05, 'm', 'A1', 'Derived'),
    chk('A1_walking_clear', 'the free width between the panel\'s rear face (z 3.400) and the nearest fixed projection, for a body from 0 to 2.0 m high in x 9.5 to 12.5: the stallriser face (z 4.975) at every height and the fish market\'s awning above 1.9 m (its sloping underside, read from awning_02.glb): the least of them', WALK['min_clear_m'], 0.0, 'm (at least 0.68)', 'A1', 'Derived (the awning mesh read; the review\'s straight-line estimate about 1.0)', minimum=0.68, ground_clear=WALK['ground_clear_m'], review_estimate=WALK['clear_at_head_2_0_review_estimate_m']),
    chk('A1_no_deep_obstacle', 'no object deeper than 0.895 m stands behind the panel (x 9.5 to 12.5) between the rail and the frontage, so that 0.68 m remains: the fish market\'s 0.92 m crates may not stand there', 0.895, 0.0, 'm (maximum depth)', 'A1', 'Derived: 1.575 - 0.68', max=True),
    chk('A1_no_lettering', 'no lettering, number, crest, maker\'s mark or plate on any mesh or texture', 'none', 0, '-', 'A1', 'Read: canon, brief'),
    chk('A1_paint_albedo', 'base colour within 12 of the chosen condition: galvanised (118, 120, 122) by default, or black (24, 24, 26)', [118, 120, 122], 12, 'sRGB', 'A1'),
    chk('A1_bbox', 'overall size of the built panel including nuts and thread', [2072, 50, 1030], 8.0, 'mm', 'A1', 'Judgement: the fresh review'),
    chk('A1_outline_residual', 'largest distance between a built elevation outline and the target\'s at the same x', 0, 6, 'mm', 'A1'),
    chk('A1_foot_patch', 'dark tarmac reinstatement patch round each post, ragged, flush with the flags to +-3', [250, 250], 60, 'mm', 'A1', 'Judgement: the fresh review'),
    chk('A1_lean', 'seed lean of a post', [0, 1], 0, 'deg (range)', 'A1'),
    chk('Q2_bay', 'post axis to post axis (3.0 m; the return\'s end bay 1.4 m)', 3000, 30, 'mm', 'Q2', 'Read: the bollards target (3.0 m)'),
    chk('Q2_short_bay', 'the return\'s end bay, post axis to post axis', 1400, 30, 'mm', 'Q2'),
    chk('Q2_post_od', 'post outside diameter', 76.1, 4.0, 'mm', 'Q2'),
    chk('Q2_post_height', 'post top above the apron', 1100, 20, 'mm', 'Q2'),
    chk('Q2_top_rail_axis', 'top rail axis above the apron', 1000, 15, 'mm', 'Q2'),
    chk('Q2_top_rail_od', 'top rail outside diameter', 60.3, 3.0, 'mm', 'Q2', 'Judgement: the fresh review (3.0 m bays)'),
    chk('Q2_low_rail_axis', 'low rail (Q2a) or chain eye (Q2b) above the apron', 500, 15, 'mm', 'Q2'),
    chk('Q2_base_plate', 'base plate 200 x 200 x 12 with four nuts on a 150 square', [200, 200, 12], 3, 'mm', 'Q2'),
    chk('Q2_chain_bar', 'chain bar diameter, agreeing with the bollards target', 13, 1, 'mm', 'Q2', 'Read: bollards target'),
    chk('Q2_chain_sag', 'mid-span sag of the Q2b chain below its eyes (3.0 m bays; 87 on the 1.4 m end bay)', 200, 50, 'mm', 'Q2b', 'Photo (LHB 227 +-35)'),
    chk('Q2_chain_no_spikes', 'no spikes on any link', 'none', 0, '-', 'Q2b', 'Read: bollards target (plain chain)'),
    chk('Q2_ears', 'ears only on the sides that face a Q2b bay: two per Q2b bay, 18 in all, none on a Q2a bay, one on the Q2a/Q2b corner post (-110.4, -15.4), one on the return\'s end post', sum(len(e['faces']) for e in _ears), 0, 'count', 'Q2b', 'Derived'),
    chk('Q2_basin_posts', 'three posts on x -110.4: y -21.4, -18.4 and the corner -15.4 (two bays of 3.0)', [-110.4, -21.4, -15.4], 0.05, 'm', 'Q2', 'Derived: the fresh review'),
    chk('Q2_tip_posts', 'six more posts on y -15.4, x -113.4 to -128.4 every 3.0 (the corner (-128.4, -15.4) is the last)', [-113.4, -128.4, -15.4], 0.05, 'm', 'Q2', 'Derived'),
    chk('Q2_return_posts', 'three posts on x -128.4: y -18.4, -21.4 and the end post -22.8 (bays 3.0, 3.0, 1.4)', [-128.4, -18.4, -22.8], 0.05, 'm', 'Q2', 'Derived: the fresh review'),
    chk('Q2_totals', '12 posts, 11 bays, 31.4 m of railing', [12, 11, 31.4], 0.05, 'count, count, m', 'Q2', 'Derived: the fresh review'),
    chk('Q2_behind_nose', 'rail line behind the cope nose (x -110 on the basin edge, y -15 at the tip)', 0.4, 0.05, 'm', 'Q2', 'Derived'),
    chk('Q2_clear_of_mooring', 'no post within 8 m of a K6 bollard (-110.75, -45 and -80) or a K7 cleat (-110.25, -52 to -64): the nearest post, y -21.4, is %.1f from the K6 at -45' % _near_k6, round(_near_k6, 1), 0.0, 'm (at least 8.0)', 'Q2', 'Derived', minimum=8.0),
    chk('Q2_clear_of_rings', 'no post or rail within 4.0 m of the south-quay kit\'s mooring rings on the jetty\'s basin face, (-110.05, -62) and (-110.05, -32) (the review: (-110, ...)); nearest post (-110.4, -21.4)', round(_near_ring, 1), 0.0, 'm (at least 4.0)', 'Q2', 'Derived: the kit\'s _quay_furniture', minimum=4.0),
    chk('Q2_corner_closed', 'the return\'s end post (-128.4, -22.8) stands within 0.25 of the parapet\'s inner face line (x -128.6) and of its end (y -23.0); its plate clears the parapet by 0.1', [0.2, 0.2], 0.05, 'm', 'Q2', 'Derived: the fresh review'),
    chk('Q2_clear_of_light', 'tip rail at least 2.5 m from the harbour light\'s plinth face (y -18.1)', round(_near_light, 1), 0.0, 'm (at least 2.5)', 'Q2', 'Derived', minimum=2.5),
    chk('Q2_walking_clear', 'a person on the jetty keeps at least 0.68 m between the rail and any fixed object (the jetty is 20 m across)', 19.6, 0.0, 'm (at least 0.68)', 'Q2', 'Derived', minimum=0.68),
    chk('Q2_paint_albedo', 'base colour within 10 of the sRGB', [24, 24, 26], 10, 'sRGB', 'Q2'),
    chk('Q2_no_lettering', 'no lettering, crest or maker\'s mark', 'none', 0, '-', 'Q2'),
]
T['checks'] = C

# ------------------------------------------------------------------------------------------------------------------ could not settle / to read / handover
T['could_not_settle'] = [
    'No photograph of a British pedestrian guard rail of any date was reachable: the whole of A1 other than the scene\'s 2.0 m, 1.0 m, x and z is Judgement, and BOTH sides of its form are judgement (the first version\'s round tube, the fresh review\'s RHS with bolted ends; the review\'s form is also what the search-summary lead "posts 50 x 30 mm" describes). Eight other panoramas (urban_street_03 and 04, cambridge, birbeck, canary_wharf, adams_place_bridge, roof_garden, greenwich_park) show none. TO CONFIRM FROM THE PC before the build is gated: two dated (1985 to 1995) Geograph or Commons photographs of a British kerbside guard rail, for the sections, the post top and the clamp.',
    'Whether Quay Street\'s rail in 1990 was galvanised grey (the default now), black, white-and-black banded or green: no photograph either way; the photographed ironwork is black cast and wrought iron, not galvanised steel.',
    'The lower rail\'s height and the infill\'s kind (round bar, flat bar, or open with two rails only). The 1983 and 1988 accident studies (search summaries) say the conventional rail of the 1980s hid the road from short pedestrians and that a see-through type did better, which supports dense infill for the rail of 1990; no number.',
    'The bolt: the head is hidden inside the rail end (the end plate has the rail\'s own outline), so the bolt could not be fitted in a real panel without an access hole or a larger plate; the nut and thread on the post\'s outer face are what is seen. Kept as the review wrote it.',
    'Q2: whether a harbour authority of the Hook would rail the jetty tip; the kit has no railing and the asset plan names one. The Hull 1989 photograph (an earlier session\'s note) supports chain at a working quay edge, not a tube railing. The commonest 1990 dock-edge form may have been galvanised ball-type stanchions with rails through forged balls at 1.8 to 2.0 m (the review): not in this target.',
    'The camera heights rest on 75 mm brick courses (73 to 79 mm if Victorian): R3B 0.945 +-0.02, R3A 1.02 +-0.03, R3D 1.15 +-0.02, LHB 1.13 +-0.03, each at its own ground, +-6 % in size (R3A +-8 %). The building wall\'s own foot at Limehouse reads 1.052 to 1.095 (the review 1.09), 6 % under the paving the posts stand on; it is corroboration only.',
    'R3A is oblique (32 degrees): widths there are blur-doubled; only its heights, rails and pitches on the left run are used; the run right of its cast post is another pattern and is not measured.',
    'R3B, the height of the knop: the review\'s head list (scaled by 0.974) puts the turned knop (about 90 across) at z 2044 and the ring above it (about 44) at about 2094; the 1 mm head close in the previews reads the knop\'s widest row (about 95 across) at z 2062 and the ring (about 45 across) at about 2115, 18 to 20 mm higher, while the widths, the shaft and the tip (2205 read, 2211 stated) agree. The list is kept as the review wrote it (R3B is a reserve kind and is not placed); a build of R3B would read the knop height from the head close.',
    'The bars of the R3B photograph lean about 0.7 degrees to the left going up (probably the capture\'s own roll: their centres at z 1800 sit 12 to 18 mm left of the same bars at z 770); the target\'s bars are vertical, so its overlay is up to 20 mm off at the heads. Not corrected: the numbers are heights, pitches and widths, inside their stated errors.',
    'R3A, read directly on the new 3 mm elevation (h 1.02): the course pitch of its red courses is 75 (autocorrelation, weak on an oblique brick face), which supports the height; but the strongest brightness steps of its wall edges lie 31 (coping) and 41 (lower string) above the first version\'s reads times 1.052, and its bottom rail 25 above; the bullnose edges are soft on an oblique view and the stated error is 8 %, so the scaled numbers stay.',
    'The paint on the photographed ironwork has been renewed since 1990 and the panoramas are 2019: none of R3A, R3B, R3D or the K5 post is known to be older than 1990; a Victorian pattern is plausible for R3B.',
    'Whether the park railing\'s bar section is round or square (the blur hides it): round is assumed.',
    'The awning\'s underside: read from awning_02.glb (a body falling from the fascia\'s underside to its front edge, a valance 0.32 below). The review estimated the clear width at a 2.0 m head height as about 1.0 m from a straight line from the valance\'s bottom; the mesh gives about 1.4. Both pass 0.68.',
    'The one photographed multi-rail tube railing (greenwich_park_02, a path edge) was not measured for want of an anchor: Q2\'s two-rail form (top 1000, low 500) is not checked against it; a five-rail form would be an alternative for the jetty.']
T['to_read_when_the_network_opens'] = [
    'FIRST, FROM THE PC (Jafar\'s PC reaches Geograph and Commons): two dated (1985 to 1995) photographs of a British kerbside pedestrian guard rail, to confirm the sections (RHS or round tube), the post top, the clamp or bolt, the finish (galvanised or painted) and the infill, before the build is gated',
    'BS 3049:1976 "Specification for pedestrian guard rails (metal)" (withdrawn 15 November 1995; BSI Knowledge or a standards retailer): post and rail sizes, infill, finish, classes; and BS 7818:1995, which replaced it',
    'Department for Transport Local Transport Note 2/09 "Pedestrian guardrailing" (assets.publishing.service.gov.uk), its history section and its set-back from the kerb (the scene\'s 0.25 m behind the kerb leaves the rail\'s road face 0.35 m from the kerb face; a 1980s rule of about 0.45 m is remembered by the writer and the reviewer and has not been read: the scene is left as it is); Kent County Council\'s pedestrian guardrail policy (democracy.kent.gov.uk), which dates guardrail from the 1930s',
    'Wikimedia Commons categories for pedestrian guard railings, railings in Britain and bollards and chains at quays, 1975 to 2000 photographs; Geograph squares of fishing towns (Whitby, Brixham, Grimsby, Hull, North Shields) 1980s to 1990s: the author, licence and date on each file page',
    'Peter Marshall\'s River Hull photograph of 1989 (Flickr 51040207776, the atlas\'s R08): the chain-edged quay, its posts and its chain, if the licence allows measuring',
    'Historic England: list entries for quay walls and railings (Truro, list entry 1201539, "quay walls and railings"; Bideford, 1282939, cast-iron fence posts with tubular bars and chains), the Historic England Archive\'s 1980s photographs of dock edges and street furniture',
    'The Health and Safety Executive\'s Docks Regulations 1988 and "Safety in Docks" approved code of practice (what edge protection a 1990 quay needed); Torbay and North Devon harbour edge-protection audits (summaries say working fish quay berths were left unfenced)',
    'Tyne and Wear HER and North Shields Fish Quay conservation area notes; 1980s street-furniture catalogues for guard-rail panels and dock-edge stanchions: sizes and finishes only, no makers\' marks',
    'The street recipe\'s own reference photographs of the Hook sheet, if it shows a railing']
T['handover'] = dict(
    to_builder='A1 replaces the scene\'s five-bar stand-in at the same x and z; the posts keep the scene\'s x 10.0 and 12.0, z 3.375; it is now an RHS panel with bolted ends and a galvanised default. Q2 is new to the south-quay kit: it needs a recipe step (twelve posts, eleven bays, nine chains, the return) or a placement from this target; the kit has no railing today.',
    to_bollards_writer='the chain: sag 200, not 150 (Photo LHB, two swags 215 and 240, mean 227 +-35); lug heights 806 and 409 here (at 1.13 m) against 840 and 420 there (inside the errors); K5 height 1096 at 1.13 m against 1135 at 1.17 m (the camera heights\' ratio)',
    to_kerbs_writer='the kerb stands 0.205 m in front of the guard rail\'s axis (granite top 170, back edge z 3.170); the flag level at the post is y 0.040 against the scene\'s 0.05625',
    to_town_session='the fish market\'s crates (0.92 m deep) must not stand in x 9.5 to 12.5 behind the rail: that leaves 0.655 m of footway, under a walking person\'s 0.68. The awning over the fish market (awning_02) reaches the rail line at 1.57 m and leaves 1.39 m clear at a 2.0 m head height. Whether the yard mouth gets gates is the town\'s call; this target has no yard gate',
    for_NOW_md='Railings target v2 (cloud week 42, after the fresh review): guard rail A1 = 2.0 m panel of RHS (posts 50 x 30 to 1030, top rail 50 x 30 flat with its top at 1000, bottom 40 x 20 at 200, seventeen 12 mm bars, M10 bolts, nuts on the posts\' outer faces), galvanised by default; quay tube railing Q2 on the jetty only (12 posts, 11 bays, 31.4 m: two bays of two rails at the tip of the basin edge, the tip and the seaward return with chain); no area railings or yard gates on the street; no guard-rail photograph reached: two dated photographs to be read from the PC before the build is gated.')

# ------------------------------------------------------------------------------------------------------------------ sources
T['sources'] = [
    dict(id='S1', url='https://polyhaven.com/a/bethnal_green_entrance', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0 (https://polyhaven.com/license, read 2026-10-09)', taken='2019-08-18 07:01 UTC (51.526915, -0.054044), api.polyhaven.com/info read 2026-10-09',
         shows='a park entrance in Bethnal Green: a tall cast-iron park railing on a brick plinth with a hinge post and brick piers (R3B); a housing block\'s railing on a two-stage dwarf wall (R3A); a hoop-top railing and gate leaf; bollards; block paving', used='YES: R3B main photograph, R3A; calibration anchors',
         period='the Victorian pattern is long-lived but the paint, the hoop-top gate and the signs are 2000s; whether any of it stood in 1990 is unknown (R3A may be a replica); the picture is for bar proportions, rails, finials and the black paint, not as a 1990 record'),
    dict(id='S2', url='https://polyhaven.com/a/urban_street_01', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-08-18 07:09 UTC (51.528295, -0.053879)',
         shows='an estate street: a low dark-green railing and gate on a dark brick garden wall (R3D); park railings with spear heads on a granite plinth; bollards', used='YES: R3D; calibration anchors',
         period='an estate of the 1960s to 80s with renewed paint; the railing form is plausible for 1990 (a council green), the exact paint date is unknown'),
    dict(id='S3', url='https://polyhaven.com/a/limehouse', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-05-19 15:45 UTC (51.510606, -0.036324)',
         shows='a marina basin: bolted cast-iron chain posts with two swags of spiked chain, a timber-piled quay edge across the water, pontoons', used='YES: LHB (the chain\'s lug heights and sag; the K5 post cross-check)',
         period='a 1980s to 90s marina redevelopment; the chain is ornamental (spiked); only its sag and the post\'s lug heights are used'),
    dict(id='S4', url='the repository', read='2026-10-09', author='the project', licence='n/a', taken='2026-09-02 to 2026-10-09',
         shows='SCENE-SLOTS.md, vignette-scene.json, vignette-feet.json, vignette-pieces.json, terrace-fronts.md, the kerbs and bollards targets, the south-quay kit (south_quay_geom.py incl. _quay_furniture, README, METHOD), the held prop awning_02.glb, the asset plan, the street-clutter research, atlas CONTINUATION.md (R08), TARGET-REVIEW.md', used='YES: Read numbers', period='n/a'),
    dict(id='S5', url='WebSearch result summaries, 2026-10-09 (three queries: BS 3049 and guard rail infill; the history of British pedestrian guardrail; harbour quay edge railings and chain)', read='2026-10-09', author='third-party pages reached only as summaries', licence='n/a', taken='n/a',
         shows='leads: BS 3049:1976 was withdrawn on 15 November 1995 and replaced by BS 7818; present-day guard rails use 12 mm bars at 110 to 112 centres, 50 x 30 mm posts and a 1100 height; a 1983 London study and a 1988 article on guardrail visibility; Kent dates guardrail from the 1930s; Torbay\'s audit leaves working fish-quay berths unfenced; Bideford\'s quay has cast-iron posts with tubular bars and chains from 1899 to 1905', used='LEADS ONLY: no number taken as a measurement; the "50 x 30" lead now stands behind the RHS post; the 100 gap rule is marked Judgement', period='n/a')]
T['unreached'] = ['Wikimedia Commons', 'Geograph', 'Flickr (including the Hull photograph R08)', 'archive.org', 'HathiTrust', 'Historic England and the Historic England Archive', 'British Listed Buildings', 'BSI Knowledge', 'gov.uk (LTN 2/09)', 'legislation.gov.uk', 'openverse.org', 'Wikipedia', 'Project Gutenberg', 'Sketchfab', 'europeana.eu', 'api.wellcomecollection.org', 'loc.gov', 'web.archive.org (all refused with 403 or not resolvable, tried 2026-10-09); only polyhaven.com and ambientcg.com answered']
T['looked_at_and_left_out'] = ['greenwich_park_02 (one run of black multi-rail railing along a path edge: square posts, five slender round rails and a flat top rail on a brick edging; SEEN AND NOT MEASURED: no wall or other anchor in its view gives its camera height; it is the nearest photographed thing to a tube railing, and it says a park railing of rails without bars was common in 2019)',
                              'urban_street_02 (a steel palisade along a railway arch and a security door: a 2000s fence, not a railing of the period)', 'urban_street_03 and 04, cambridge, birbeck_street_underpass, leadenhall_market, greenwich_park x3, roof_garden (no railing that bears on this family; urban_street_04 has plastered balustrades of Kensington, not an ironwork form)',
                              'canary_wharf and adams_place_bridge (stainless dock-edge balustrades of the 2000s: modern-only forms, not used)', 'docklands_01 and 02 (Dublin, not Britain)', 'Poly Haven models: modular_chainlink_fence and large_iron_gate exist (CC0) but are not period guard rails or the street\'s; nothing in the catalogue is a guard rail, a tube railing or a quay chain']

json.dump(T, open(os.path.join(HERE, 'target.json'), 'w'), indent=1)
print('wrote target.json', os.path.getsize(os.path.join(HERE, 'target.json')), 'bytes')
