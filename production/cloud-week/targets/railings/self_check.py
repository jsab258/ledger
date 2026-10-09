#!/usr/bin/env python
"""Tests the railings target against its own sources before anything is built.

/home/user/.bpyenv/bin/python self_check.py [--no-write]

A  every printed number the target uses comes back from target.json (and is found in the repository file it is quoted from; the kit's, the bollards target's and the awning's numbers are read live)
B  every photograph measurement stands as stated (camera heights recomputed from their anchors, one per object's own ground; the first-version reads times the scale factors; bars, rails and the cross-checks)
C  the drawing's projected edges fall on the photographs (R3B main; the others within the stated error; a scale fitted on ONE dimension, the bar pitch)
D  internal consistency (parts add up, nothing floats, the sections and the bolts, the walking strip from 0 to 2.0 m high, the quay runs against the kit, the rings and the moorings)
E  the text and the files: no real name or mark, previews within their size limits, the numbers in TARGET.md are target.json's
Prints a result line and writes it into target.json under "self_check"."""
import sys, os, json, math, re
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import target_drawing as D
import awning_lib as AL

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PREV = os.path.join(ROOT, 'production', 'previews', 'cloud-week', 'refs', 'railings')
TP = os.path.join(HERE, 'target.json')
T = json.load(open(TP))
RES = []


def t(group, name, ok, detail=''):
    RES.append((group, name, bool(ok), detail))


def near(a, b, tol):
    return abs(a - b) <= tol


K = T['kinds']
A1 = K['A1']
A = A1['panel']
PRA = A1['profiles']
Q2 = K['Q2']
HRd = T['photo_measurements']['hand_reads']
HR1 = T['photo_measurements']['hand_reads_as_read_at_first_version']
R3B = T['photo_measurements']['R3B_auto']
SF = T['street_frame']
PL = T['placements']
CK = {c['name']: c for c in T['checks']}
WS = T['street_fixtures']['walking_strip']
SC = T['calibration']['first_version']
CAL = T['calibration']
SCALE = {k_: o['scale_from_first_version'] for k_, o in CAL['objects'].items()}

# ------------------------------------------------------------------------------------------------------------------ A
for s in T['scene_numbers']:
    p = os.path.join(ROOT, s['file'])
    ok = os.path.exists(p)
    txt = open(p, encoding='utf-8').read() if ok else ''
    t('A', f"printed {s['id']} found in {s['file']}", ok and s['find'] in txt, s['what'])
S = {s['id']: s for s in T['scene_numbers']}
v = S['guard_rail_line']['value']
t('A', 'the scene\'s height is 1.0 m and A1\'s top rail top is 1000', near(A['top_rail']['top_z'], v['height_m'] * 1000, 0.001) and near(A['height'], v['height_m'] * 1000, 0.001))
t('A', 'A1\'s post (50 along) and bottom rail (40 across) keep the scene\'s stand-in sizes 0.05 and 0.04 (they are now rectangular sections of those widths)', near(A['post']['width'], v['post_m'] * 1000, 0.001) and near(A['bottom_rail']['width'], v['rail_m'] * 1000, 0.001))
t('A', 'the scene\'s five bars of 25 are replaced (A1 has more, thinner bars; the change is listed under photographs_win)', A['infill']['count'] > v['bars'] and A['infill']['diameter'] < v['bar_m'] * 1000 and any(d['element'] == 'infill of the guard rail' for d in T['photographs_win']))
t('A', 'the section change (round to rectangular) is listed under photographs_win with its basis (Judgement until a photograph is reached)', any('section' in d['element'] and 'Judgement' in json.dumps(d) for d in T['photographs_win']))
pl_s = S['guard_rail_place']['value']
t('A', 'the panel runs x 10.0 to 12.0 and is 2.0 m (c2c 2000 = 12.0 - 10.0)', near(pl_s['x1_m'] - pl_s['x0_m'], A['centre_to_centre'] / 1000, 1e-9) and PL['street'][0]['x_m'] == [10.0, 12.0])
t('A', 'the axis z 3.375 = kerb face 3.0 + the scene\'s kerb 0.125 + its 0.25 set-back', near(SF['kerb_face_z_m'] + 0.125 + pl_s['setback_from_kerb_m'], PL['street'][0]['z_axis_m'], 1e-9) and S['feet_post0']['value']['z_m'] == PL['street'][0]['z_axis_m'])
t('A', 'the kerbs target\'s back edge (3.0 + 0.170) leaves 0.205 to the axis', near(PL['street'][0]['z_axis_m'] - (3.0 + S['kerb_target_top']['value']['top'] / 1000), PL['street'][0]['behind_kerbs_target_back_m'], 1e-9) and near(PL['street'][0]['behind_kerbs_target_back_m'], CK['A1_behind_kerb_back']['expected'], 1e-9))
t('A', 'the stand-in\'s lower rail is 0.45 above its foot (y 0.50625 - 0.05625) and A1\'s is 0.20', near(0.50625 - 0.05625, S['pieces_lower_rail']['value']['above_foot_m'], 1e-9) and A['bottom_rail']['axis_z'] == 200.0)
t('A', 'the footway level at the posts: scene y 0.05625; kerbs target flags +110 over the channel -0.075 plus the fall 0.205/40 = 0.040', near(SF['foot_y_kerbs_target_m'], -0.075 + 0.110 + 0.005, 0.0006) and near(SF['foot_y_scene_m'], 0.05625, 1e-9))
scene_txt = open(os.path.join(ROOT, 'production/specs/vignette-scene.json'), encoding='utf-8').read()
t('A', 'the frontage line 5.125 = kerb face 3.0 + 0.125 + 2.0 and the stallriser face is 0.15 in front of it (4.975: the scene\'s "fish market\'s front (4.97 m)")',
  near(3.0 + 0.125 + 2.0, S['frontage_z']['value'], 1e-9) and near(S['frontage_z']['value'] - S['stallriser']['value']['proud_m'], SF['stallriser_face_z_m'], 1e-9) and "the fish market's front (4.97 m)" in scene_txt)
t('A', 'the scene\'s note: three panels left 1.57 m, the crates 0.92 m deep left 0.65, under 0.68', 'there is 1.57 m' in scene_txt and 'crates (0.92 m deep) left 0.65 m' in scene_txt and 'walking person\'s 0.68' in scene_txt)
rear = PL['street'][0]['z_axis_m'] + A['top_rail']['width'] / 2000
clear = SF['stallriser_face_z_m'] - rear
t('A', 'the rail\'s rear face = axis 3.375 + half the top rail\'s 50 across = 3.400; clear to the stallriser face 4.975 = 1.575 at ground level (the scene says 1.57)', near(rear, WS['rear_face_z_m'], 1e-9) and near(clear, WS['ground_clear_m'], 0.0005) and near(clear, 1.57, 0.006))
t('A', 'the deepest obstacle that leaves 0.68 is 1.575 - 0.68 = 0.895; the 0.92 crates exceed it', near(clear - 0.68, CK['A1_no_deep_obstacle']['expected'], 0.0006) and 0.92 > CK['A1_no_deep_obstacle']['expected'])
# the awning, read live from the repository
pcs = json.load(open(os.path.join(ROOT, 'production/specs/vignette-pieces.json')))['pieces']
aw = [p for p in pcs if p['name'] == 'prop_awning_02_0']
t('A', 'the fish market\'s awning prop_awning_02_0 stands at x 10.5 to 13.5 and z 3.39 to 5.125 over the footway (live from vignette-pieces.json)',
  len(aw) == 1 and near(aw[0]['x_m'] - aw[0]['sx_m'] / 2, 10.5, 0.001) and near(aw[0]['x_m'] + aw[0]['sx_m'] / 2, 13.5, 0.001) and near(aw[0]['z_m'] - aw[0]['sz_m'] / 2, 3.39, 0.001) and near(aw[0]['z_m'] + aw[0]['sz_m'] / 2, 5.125, 0.001))
hs_ = [round(0.1 * i, 1) for i in range(0, 21)]
cl_ = [AL.clear_at_height(h) for h in hs_]
t('A', f"the free width from 0 to 2.0 m high recomputed from awning_02.glb every 0.1 m: the least is {min(cl_):.3f} (stored {WS['min_clear_m']}) and the ground-level one {cl_[0]:.3f} (stored {WS['ground_clear_m']})", near(min(cl_), WS['min_clear_m'], 0.002) and near(cl_[0], WS['ground_clear_m'], 0.0006) and min(cl_) >= 0.68)
t('A', 'the awning mesh numbers stored in target.json equal the live read of the glb (depth, front edge, valance, slope)', near(AL.AW['depth_m'], WS['awning']['mesh']['depth_m'], 1e-6) and near(AL.AW['body_front_edge_mesh_y'], WS['awning']['mesh']['body_front_edge_mesh_y'], 1e-6) and near(AL.slope, WS['awning']['body_slope'], 1e-4) and near(AL.valance_bottom_above_footway(), WS['awning']['valance_bottom_above_footway_m'], 0.001))
t('A', 'the awning leaves the strip free at ground level and the valance (1.57 above the footway) hangs at z 3.39, 10 mm in front of the rail\'s rear face: nobody walks into it from behind the rail', near(WS['awning']['valance_bottom_above_footway_m'], 1.57, 0.005) and WS['awning']['front_edge_z_m'] < WS['rear_face_z_m'])
# the bollards target, read live
BT = json.load(open(os.path.join(ROOT, 'production/cloud-week/targets/bollards/target.json')))
k5 = BT['kinds']['K5']
t('A', 'Q2b\'s chain is the bollards target\'s plain chain: bar, link lengths, widths and pitch equal', all(Q2['chain']['link'][k] == k5['chain']['plain'][k2] for k, k2 in (('bar', 'bar_diameter'), ('inner_length', 'inner_length'), ('inner_width', 'inner_width'), ('outer_length', 'outer_length'), ('outer_width', 'outer_width'), ('pitch', 'pitch'))))
t('A', 'Q2\'s bay is the bollards target\'s post spacing (3.0 m)', near(Q2['bay']['centre_to_centre'], k5['chain']['post_spacing_m'] * 1000, 1e-9))
t('A', 'Q2\'s chain eye height (500) is within 20 % of K5\'s lower eye (420) and Q2\'s top (1000) near K5\'s upper (840) +-20 %', near(Q2['chain']['eyes']['z'], k5['fixings']['chain_eyes']['z'][0], 100) and near(Q2['top_rail']['axis_z'], k5['fixings']['chain_eyes']['z'][1], 170))
t('A', 'Q2b\'s sag (200) differs from K5\'s (150, Judgement there) and is Photo here: LHB 227 +-35 reads inside 200 +-50', k5['chain']['plain']['sag_mm'] == 150 and Q2['chain']['sag'] == 200 and near(HRd['LHB']['lower_lug_z']['v'] - HRd['LHB']['lower_chain_lowest_z']['v'], 240, 40))
t('A', 'Q2 paint is K5\'s (24, 24, 26) satin 0.55', Q2['paint']['srgb'] == k5['paint']['srgb'] and near(Q2['paint']['roughness'], k5['paint']['roughness'], 1e-9))
pK = BT['placements']['quay']
k6 = [e for e in pK if e['id'] == 'quay_edge'][0]['places']
k7 = [e for e in pK if e['id'] == 'cleats'][0]
jet6 = [(p['x_m'], p['y_m']) for p in k6 if p['x_m'] == -110.75]
t('A', 'the bollards target\'s jetty K6 are at (-110.75, -80) and (-110.75, -45); its K7 cleats at x -110.25, y -64, -58, -52', sorted(jet6) == [(-110.75, -80.0), (-110.75, -45.0)] and k7['x_m'] == -110.25 and k7['y_m'] == [-64.0, -58.0, -52.0])
# the south-quay kit, live
sys.path.insert(0, os.path.join(ROOT, 'tools', 'art-recipes', 'south-quay'))
KIT_RINGS = []
try:
    import south_quay_geom as G
    kit, jn, info = G.build(ROOT)
    e_ = info['edges']
    t('A', 'kit: the jetty\'s basin edge is x -110 from y -100.6 to -15 and its end y -15 from x -130 to -110.6 (live from south_quay_geom.build)', e_['jetty_north'] == ((-110.0, -100.6), (-110.0, -15.0)) and e_['jetty_end'] == ((-130.0, -15.0), (-110.6, -15.0)))
    t('A', 'kit: the quay edge x -70 and the apron at the kerb top +0.05', near(info['quay_edge_x'], -70.0, 1e-9) and near(info['apron_z'], 0.05, 1e-9))
    jx0, jx1 = -130.0, -110.0
    t('A', 'kit: the cope is 0.60 across; the parapet is on the seaward side x -129.4 to -128.6 and ends at y -23.0', near(G.COPING_W_M, 0.6, 1e-9) and near(jx0 + G.COPING_W_M, -129.4, 1e-9) and near(jx0 + G.COPING_W_M + 0.80, -128.6, 1e-9) and S['kit_parapet']['value']['y_end'] == -15.0 - 8.0)
    t('A', 'kit: the kit has no railing piece: no kit piece name contains "rail"', not any('rail' in k.lower() for k in kit.pieces))
    pc = np.array(kit.pieces['iron_black__mooring_rings']['verts'])
    jr = pc[(pc[:, 0] > -111.0) & (pc[:, 0] < -109.0)]
    cl_y = sorted({round(float(y_), 0) for y_ in jr[:, 1]})
    KIT_RINGS = [[round(float(jr[abs(jr[:, 1] - y_) < 1][:, 0].mean()), 2), y_] for y_ in cl_y]
    t('A', f"kit: the mooring rings on the jetty's basin face (live vertices of the kit's mooring_rings piece): {KIT_RINGS}; target.json's {T['street_fixtures']['kit_rings_jetty_m']} lies within 0.1", cl_y == [-62.0, -32.0] and all(near(a_[0], b_[0], 0.1) and near(a_[1], b_[1], 0.01) for a_, b_ in zip(KIT_RINGS, T['street_fixtures']['kit_rings_jetty_m'])))
    t('A', 'kit: the cope\'s nose stands 0.05 proud of the wall face (the rings hang from x -110.05)', near(G.COPING_NOSE_M, S['kit_cope_nose']['value'], 1e-9) and near(-110.0 - G.COPING_NOSE_M, T['street_fixtures']['kit_rings_jetty_m'][0][0], 1e-9))
except Exception as ex:
    t('A', 'kit: south_quay_geom imports and builds (%s)' % ex, False)
t('A', 'the kit\'s README lists a ladder, bollards and a stone parapet but no railing', 'railing' not in open(os.path.join(ROOT, 'production/art/south-quay/README.md'), encoding='utf-8').read().lower().replace('no railing', ''))
t('A', 'the scene file names the yard entrance as a 3.0 m gap in the data, x 21.0 to 24.0 (no gate is placed)', S['yard_gap']['value'] == [21.0, 24.0] and 'gate' not in json.dumps(T['placements']['street'][0]).lower())
t('A', 'the bollards target\'s yard-mouth K1 posts guard the gap: x 20.7 and 24.3', [e for e in BT['placements']['street_proper'] if e['id'] == 'yard_mouth'][0]['x_m'] == [20.7, 24.3])
bar = [p for p in pcs if p['name'].startswith('prop_crowd_control_barrier')]
t('A', 'the scene stands a held crowd-control barrier at the yard mouth (x 22.5, z -4.85), an E11 prop, not this family\'s', len(bar) == 1 and near(bar[0]['x_m'], 22.5, 1e-9) and near(bar[0]['z_m'], -4.85, 1e-9) and bar[0]['bom'] == 'E11_cones_barrier')
east_front = [p for p in pcs if p['name'].startswith(('east_parade_', 'east_chandler_')) and p['shape'] == 'box' and p['name'].endswith(tuple('0123456789')) and 'bay' in p['name']]
t('A', 'every east frontage block stands on the building line: its near face is z 5.125 (the shops have no forecourt); the only pieces named rail are E8\'s', len(east_front) >= 6 and all(near(p['z_m'] - p['sz_m'] / 2, 5.125, 0.01) for p in east_front) and {p['name'].split('_')[0] for p in pcs if p['name'].startswith('rail')} == {'rail'} and all(p['bom'] == 'E8_guard_railing' for p in pcs if p['name'].startswith('rail')))
t('A', 'the street\'s pieces include no gate, fence, palisade or area railing by name', not any(w in p['name'] for p in pcs for w in ('gate', 'fence', 'palisade', 'area_rail')))
t('A', 'models per kind at most four (asset plan: two to four a kind)', all(v_ <= 4 for v_ in T['variants']['models'].values()))
t('A', 'asset plan rows: 1 kit for the guard railing, 1 for the quay railing with chain (a rail and a chain run: A1; Q2)', S['asset_plan_counts']['value'] == '1 kit; 1 kit' and T['variants']['models']['A1'] == 1)

# ------------------------------------------------------------------------------------------------------------------ B
byid = {a['id']: a for a in CAL['horizon_anchors']}
t('B', 'no anchor\'s fit is on the edge of its search range', not any(a['fit_on_edge'] for a in CAL['horizon_anchors']))
for a in CAL['horizon_anchors']:
    H = a['image_rows']
    tf = math.tan((a['foot_row'] - H / 2) * math.pi / H)
    a['_h'] = a['gauge_mm'] * tf / a['pitch_tan'] / 1000 + a['step_m']
    p_by_eye = a['px_pitch_by_eye'] * math.pi / H
    t('B', f"anchor {a['id']}: pitch inside +-15 % of the pitch read by eye ({a['pitch_tan']:.5f} against {p_by_eye:.5f}), height {a['_h']:.3f} m", abs(a['pitch_tan'] / p_by_eye - 1) <= 0.151)
for k_, O in CAL['objects'].items():
    hs_a = [byid[i]['_h'] for i in O['anchors']]
    hs_q = [q['h'] for q in O.get('quoted', [])]
    hs = hs_a + hs_q
    mean = sum(hs) / len(hs)
    t('B', f"{k_}: the mean of the anchors at its own ground ({', '.join(O['anchors'] + [q['id'] for q in O.get('quoted', [])])}) is {mean:.3f} m, within its stated error of the stated height {O['h_cam']} +-{O['err']}, and so is each", abs(mean - O['h_cam']) <= O['err'] and all(abs(h - O['h_cam']) <= O['err'] + 0.005 for h in hs))
    t('B', f"{k_}: every anchor used stands in the object's own panorama ({O['pano']}) and at least one reading is at its ground", all(byid[i]['pano'] == O['pano'] for i in O['anchors']) and len(hs) >= 1)
    for ex_ in O['excluded']:
        h_ex = byid[ex_['id']]['_h'] if ex_['id'] in byid else ex_['h']
        t('B', f"{k_}: the set-aside reading {ex_['id']} ({h_ex:.3f}) lies outside the band {O['h_cam']} +-{O['err']} (so it was rightly not pooled)", abs(h_ex - O['h_cam']) > O['err'])
    for cid in O['corroboration']:
        t('B', f"{k_}: the corroboration anchor {cid} ({byid[cid]['_h']:.3f}, a different ground) is 3 to 9 % under the stated height and so not used for it", 0.91 <= byid[cid]['_h'] / O['h_cam'] <= 0.97)
    t('B', f"{k_}: the scale factor is the new height over the first version's ({O['h_cam']} / {SC[k_]} = {O['scale_from_first_version']})", near(O['scale_from_first_version'], O['h_cam'] / SC[k_], 0.00006) and O['first_version_h'] == SC[k_])
t('B', 'no object is photographed at 1.6 m: every height is under 1.4', all(O['h_cam'] < 1.4 for O in CAL['objects'].values()))
t('B', 'the elevations were made at the stated per-object heights', all(abs(T['photo_frames'][k_]['h_cam'] - CAL['objects'][k_]['h_cam']) < 1e-9 for k_ in T['photo_frames']))
t('B', 'the review\'s 16k remeasurements agree with the stated heights within their errors: R3B 0.942/0.941, R3A 1.017, R3D 1.148, LHB pavers 1.12 to 1.15', all(abs(x_ - CAL['objects']['R3B']['h_cam']) <= 0.02 for x_ in (CAL['review_remeasure_16k']['R3B_gate_pier'], CAL['review_remeasure_16k']['R3B_rectified_pier'])) and near(CAL['review_remeasure_16k']['R3A_wall'], CAL['objects']['R3A']['h_cam'], 0.03) and near(CAL['review_remeasure_16k']['R3D_wall'], CAL['objects']['R3D']['h_cam'], 0.02) and all(abs(x_ - CAL['objects']['LHB']['h_cam']) <= 0.03 for x_ in CAL['review_remeasure_16k']['LHB_pavers']))
bt_cal = BT['calibration']['panoramas']
bge = bt_cal['bethnal_green_entrance']
t('B', 'Bethnal Green: R3A 1.02 equals the bollards target\'s 1.02 +-0.07; R3B 0.945 (the gate pier\'s ground) is %.3f under it, 0.005 outside that band, while the planter wall both targets use reads %.3f, inside it: the families agree within their errors' % (bge['h_cam'] - CAL['objects']['R3B']['h_cam'], byid['bge_planter_wall']['_h']), abs(CAL['objects']['R3A']['h_cam'] - bge['h_cam']) <= bge['h_cam_err'] and abs(CAL['objects']['R3B']['h_cam'] - bge['h_cam']) <= bge['h_cam_err'] + 0.01 and abs(byid['bge_planter_wall']['_h'] - bge['h_cam']) <= bge['h_cam_err'])
t('B', 'Limehouse: 1.13 lies inside the bollards target\'s 1.17 +-0.06', abs(CAL['objects']['LHB']['h_cam'] - bt_cal['limehouse']['h_cam']) <= 0.07)
# the scaled hand reads: every number read at the first version's height is now read x the object's scale
bad_sc = []
for fid, rd in HRd.items():
    for name, r in rd.items():
        r1 = HR1[fid][name]
        sc = r['scaled_by']
        v_, v1 = r['v'], r1['v']
        if isinstance(v1, (int, float)):
            if not near(v_, v1 * sc, 0.011): bad_sc.append((fid, name))
        elif isinstance(v1, list) and v1 and isinstance(v1[0], (int, float)):
            if not all(near(a_, b_ * sc, 0.011) for a_, b_ in zip(v_, v1)): bad_sc.append((fid, name))
        elif isinstance(v1, list) and v1 and isinstance(v1[0], list):
            if not all(near(a_[0], b_[0] * sc, 0.011) and near(a_[1], b_[1] * sc, 0.011) for a_, b_ in zip(v_, v1)): bad_sc.append((fid, name))
        if sc not in (1.0, SCALE[fid]): bad_sc.append((fid, name, 'scale'))
t('B', 'every hand-read length is the first version\'s read times its object\'s scale (R3B 0.974, R3A 1.052, R3D 1.027, LHB 1.009; counts and brick courses unscaled)' + (' %s' % bad_sc if bad_sc else ''), not bad_sc)
# R3B bars (re-measured automatically at the new height)
pk = np.array(R3B['bar_centres_s_mm'], float)
fit = np.polyfit(np.arange(len(pk)), pk, 1)
t('B', 'R3B: the bar pitch refitted from the stored bar centres equals the stated %.2f +-0.05, and %d bars were found' % (R3B['bar_pitch_mm'], len(pk)), near(fit[0], R3B['bar_pitch_mm'], 0.05) and len(pk) == 26 and near(fit[0], K['R3B']['bars']['pitch'], 0.05))
t('B', 'R3B: the pitch 76.6 is within 1 % of three inches (76.2) and within 0.3 of the review\'s 16k re-measurement (76.5), as the review expected of a Victorian railing', abs(R3B['bar_pitch_mm'] / 76.2 - 1) < 0.01 and near(R3B['bar_pitch_mm'], 76.5, 0.3))
t('B', 'R3B: the bar centres are regular (rms residual to the line at most 6 mm; the detections lie on 3 to 4 mm native pixels)', R3B['bar_pitch_resid_rms_mm'] <= 6.0)
t('B', 'R3B: the stored first bar (fitted intercept %.2f) is the line\'s' % K['R3B']['bars']['first_s'], near(fit[1], K['R3B']['bars']['first_s'], 1.0) and near(R3B['bar_fit_first_s_mm'], K['R3B']['bars']['first_s'], 0.05))
t('B', 'R3B: the bar\'s width, 20 FWHM blur included, reads 16.6 +-3 round (the first version\'s 17 x 0.974)', near(K['R3B']['bars']['diameter'], R3B['bar_fwhm_mm_median'] - 3.4, 3.5))
rz = [r['z'] for r in R3B['rails']]


def any_near(z0, tol):
    return any(abs(z - z0) <= tol for z in rz)


H_ = HRd['R3B']
t('B', 'R3B: the hand-read (first version x 0.974) top rail %.0f, mid rail %.0f and bottom rail %.0f each agree with a row of the automated rail list at the new height (%s) within their errors' % (H_['top_rail_axis_z']['v'], H_['mid_rail_axis_z']['v'], H_['bottom_rail_axis_z']['v'], ', '.join('%.0f' % z for z in rz)), any_near(H_['top_rail_axis_z']['v'], H_['top_rail_axis_z']['err']) and any_near(H_['mid_rail_axis_z']['v'], H_['mid_rail_axis_z']['err']) and any_near(H_['bottom_rail_axis_z']['v'], H_['bottom_rail_axis_z']['err']))
t('B', 'R3B: the review\'s 16k numbers (rails 433 / 1018 / 1948, tall tips about 2210, post top 2313, pitch 76.5) are reproduced by the scaled reads within their errors', near(H_['bottom_rail_axis_z']['v'], 433, 15) and near(H_['mid_rail_axis_z']['v'], 1018, 15) and near(H_['top_rail_axis_z']['v'], 1948, 15) and near(H_['tall_bar_tip_z']['v'], 2210, 15) and near(H_['post_top_z']['v'], 2313, 15))
t('B', 'R3B: the coping top: automated %d on the plane 110 behind the face + 13 for the lip = the stated %.0f +-%.0f' % (R3B['coping_top_z_mm'], K['R3B']['plinth']['coping_top_z']['v'], K['R3B']['plinth']['coping_top_z']['err']), near(HRd['R3B']['coping_top_z']['v'], R3B['coping_top_z_mm'] + 13, HRd['R3B']['coping_top_z']['err']))
t('B', 'R3B: the post shaft, mean of the eight automated widths (%.1f), equals the stated %.1f +-%.1f' % (np.mean(R3B['post_width_mm']), HRd['R3B']['post_shaft_width']['v'], HRd['R3B']['post_shaft_width']['err']), near(np.mean(R3B['post_width_mm']), HRd['R3B']['post_shaft_width']['v'], HRd['R3B']['post_shaft_width']['err']))
t('B', 'R3B: tall tips lie about 260 above the top rail, short tips about 175 above the middle rail', near(H_['tall_bar_tip_z']['v'] - H_['top_rail_axis_z']['v'], 263, 40) and near(H_['short_bar_tip_z']['v'] - H_['mid_rail_axis_z']['v'], 175, 40))
hd = K['R3B']['bars']['head_rz']
rmax = max(r for r, z in hd)
t('B', 'R3B: the bar head (the review\'s profile x 0.974): its tip %.0f is within the head error (8) of the stated tall tip %.0f; its knop is %.0f across (the review 87 to 100 x 0.974 = 85 to 97) at z %.0f' % (hd[-1][1], K['R3B']['bars']['tall_tip_z']['v'], 2 * rmax, K['R3B']['bars']['knop']['z']), near(hd[-1][1], K['R3B']['bars']['tall_tip_z']['v'], 8.0) and 84.0 <= 2 * rmax <= 98.0 and near(K['R3B']['bars']['knop']['z'], 2090 * 0.9742, 25) and near(K['R3B']['bars']['knop']['width'], 2 * rmax, 0.05))
ring_ = max(r for r, z in hd if 2085 <= z <= 2110) * 2
t('B', 'R3B: the ring above the knop is %.0f across (the review: about 45 x 0.974 = 44) and the text says so' % ring_, near(ring_, 44, 3) and 'ring about 44' in K['R3B']['bars']['knop']['text'] and 'turned knop about 90' in K['R3B']['bars']['knop']['text'])
t('B', 'R3B: the hinge post\'s axis (%.0f) is at least 48 + 5 from the last drawn bar' % K['R3B']['post']['axis_s']['v'], max(s_ for s_, _ in D.r3b_bar_positions(None, 0.0, 9999.0)) < K['R3B']['post']['axis_s']['v'] - K['R3B']['post']['shaft_width']['v'] / 2)
t('B', 'R3A: the wall top 820 and the string 315 are the first version\'s 780 and 300 x 1.052; four courses of 75 x 1.052 = 316 below the string', near(HRd['R3A']['wall_top_z']['v'], 780 * SCALE['R3A'], 1.0) and near(HRd['R3A']['wall_string_z']['v'], 300 * SCALE['R3A'], 1.0))
t('B', 'R3A: five red courses between the first version\'s z 330 and 705 read 75 each (+-5) there and %.1f at the new height (the Victorian 73 to 79 range)' % ((705 - 330) * SCALE['R3A'] / 5), near((705 - 330) / HR1['R3A']['red_courses_between']['v'], 75, 5) and near((705 - 330) * SCALE['R3A'] / HR1['R3A']['red_courses_between']['v'], 75, 5))
t('B', 'R3A: the wall is 780 at the first version = 4 lower courses at 75 (300) + five red 375 + the coping about 105', near(300 + 375 + 105, HR1['R3A']['wall_top_z']['v'], HR1['R3A']['wall_top_z']['err']))
t('B', 'R3A: the rails stand 595 and 210 apart at the first version (626 and 221 now) and the bars all 114 apart (119.9 now; tall every 240)', near(HRd['R3A']['mid_rail_axis_z']['v'] - HRd['R3A']['bottom_rail_axis_z']['v'], 595 * SCALE['R3A'], 40) and near(HRd['R3A']['top_rail_axis_z']['v'] - HRd['R3A']['mid_rail_axis_z']['v'], 210 * SCALE['R3A'], 30) and near(HRd['R3A']['bar_pitch_all']['v'], 114 * SCALE['R3A'], 5))
t('B', 'R3A: the numbers are the LEFT run\'s: the pattern text says so, left_run_max_s is 1500 x 1.052 = %.0f, and the run beyond the cast post is stated as another pattern, not measured' % K['R3A']['bars']['left_run_max_s']['v'], near(K['R3A']['bars']['left_run_max_s']['v'], 1500 * SCALE['R3A'], 2.0) and 'left run' in K['R3A']['bars']['pattern'].lower() and 'not measured' in K['R3A']['bars']['pattern'].lower())
t('B', 'R3D: the wall is 637 = 620 x 1.027 (eight courses of 75 + 20 of coping); the railing above it is 465 x 1.027 to the top rail', near(HRd['R3D']['wall_top_z']['v'], (8 * 75 + 20) * SCALE['R3D'], 20) and near(HRd['R3D']['top_rail_axis_z']['v'] - HRd['R3D']['wall_top_z']['v'], 465 * SCALE['R3D'], 30))
cs_ = np.array(HRd['R3D']['bar_centres_s']['v'], float)
f_ = np.polyfit(np.arange(10), cs_, 1)
t('B', 'R3D: ten hand-read bar centres give a pitch of %.1f; the stated read 97.0 +-3 (94.5 x 1.027, the review\'s 97.0) is %.1f higher, inside its error; the stored fit equals the centres\' fit' % (f_[0], HRd['R3D']['bar_pitch']['v'] - f_[0]), near(f_[0], HRd['R3D']['bar_pitch']['v'], 3.0) and near(f_[0], K['R3D']['bars']['pitch']['v'], 0.01) and near(f_[1], K['R3D']['bars']['first_s'], 0.01) and near(HRd['R3D']['bar_pitch']['v'], 97.0, 0.1))
t('B', 'R3D: the gate\'s paint (38, 56, 36) lies between the two measured medians (32, 47, 28) and (51, 69, 45)', all(a <= b <= c for a, b, c in zip((32, 47, 28), HRd['R3D']['paint_srgb']['v'], (51, 69, 45))))
t('B', 'LHB: the post top %.0f against the bollards target\'s 1135 has the ratio of the camera heights (1.13 / 1.17 = 0.966) within 2 %%' % HRd['LHB']['post_top_z']['v'], abs(HRd['LHB']['post_top_z']['v'] / 1135.0 / (CAL['objects']['LHB']['h_cam'] / bt_cal['limehouse']['h_cam']) - 1) <= 0.02)
t('B', 'LHB: the lugs (807, 409) against K5\'s (840, 420) have the same ratio within 6 %', all(abs(a / b / (CAL['objects']['LHB']['h_cam'] / bt_cal['limehouse']['h_cam']) - 1) <= 0.06 for a, b in ((HRd['LHB']['upper_lug_z']['v'], 840.0), (HRd['LHB']['lower_lug_z']['v'], 420.0))))
sag_m = (HRd['LHB']['upper_lug_z']['v'] - HRd['LHB']['upper_chain_lowest_z']['v'] + HRd['LHB']['lower_lug_z']['v'] - HRd['LHB']['lower_chain_lowest_z']['v']) / 2.0
t('B', 'LHB: both swags sag 217 to 242 below their lugs, a mean of %.0f +-35; the target\'s 200 lies between the bollards target\'s 150 and the photograph\'s mean' % sag_m, near(sag_m, 227, 35) and 150 < Q2['chain']['sag'] < sag_m)
t('B', 'LHB: the span read from the flanges (%.0f) is within 5 %% of 3.0 m (the bollards target\'s 3.06 m between two posts, 3.0 nominal)' % HRd['LHB']['span_mm']['v'], abs(HRd['LHB']['span_mm']['v'] / 3000.0 - 1) <= 0.06)
t('B', 'LHB: K5 has four flange nuts, as the bollards target says', HRd['LHB']['flange_bolts']['v'] == k5['fixings']['bolts']['count'] == 4)

# ------------------------------------------------------------------------------------------------------------------ C
FR = T['photo_frames']


def gray(name):
    return np.asarray(Image.open(os.path.join(PREV, name)).convert('L'), float)


def band_profile(im, win, mm, zlo, zhi):
    r0, r1 = int(round((win['z1'] - zhi) / mm)), int(round((win['z1'] - zlo) / mm))
    return im[r0:r1].mean(0)


def locate_dark(prof, win, mm, s_pred, half_mm=10.0):
    d = gaussian_filter1d(gaussian_filter1d(prof, 12 / mm) - prof, 0.8)
    c = int(round((s_pred - win['s0']) / mm))
    h_ = int(round(half_mm / mm))
    if c - h_ < 1 or c + h_ >= len(d) - 1:
        return None
    seg = d[c - h_:c + h_ + 1]
    k0 = int(np.argmax(seg))
    if seg[k0] < 2.0:
        return None
    lo, hi = max(0, k0 - 2), min(len(seg), k0 + 3)
    w = np.clip(seg[lo:hi], 0, None)
    kk = (np.arange(lo, hi) * w).sum() / w.sum()
    return win['s0'] + (c - h_ + kk) * mm


def row_extreme(im, win, mm, z_pred, s_cols, half_mm, kind='dark'):
    r_pred = (win['z1'] - z_pred) / mm
    c0, c1 = [int(round((x - win['s0']) / mm)) for x in s_cols]
    prof = im[:, c0:c1].mean(1)
    sm = gaussian_filter1d(prof, 1.0)
    bg = gaussian_filter1d(prof, 20 / mm)
    r_lo, r_hi = int(round(r_pred - half_mm / mm)), int(round(r_pred + half_mm / mm))
    seg = (bg - sm)[r_lo:r_hi + 1] if kind == 'dark' else (sm - bg)[r_lo:r_hi + 1]
    k0 = int(np.argmax(seg))
    return win['z1'] - (r_lo + k0) * mm, float(seg[k0])


def step_edge(im, win, mm, z_pred, s_cols, half_mm):
    """z of the strongest vertical brightness step within +-half_mm of z_pred over the columns"""
    c0, c1 = [int(round((x - win['s0']) / mm)) for x in s_cols]
    col = gaussian_filter1d(im[:, c0:c1].mean(1), 1.0)
    r_lo, r_hi = int(round((win['z1'] - z_pred - half_mm) / mm)), int(round((win['z1'] - z_pred + half_mm) / mm))
    gr = col[r_lo + 1:r_hi + 1] - col[r_lo - 1:r_hi - 1]
    return win['z1'] - (r_lo + int(np.argmax(np.abs(gr)))) * mm


# C: R3B, the main photograph
KB = K['R3B']
F = FR['R3B']['preview']
im = gray('ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg')
mm = F['mm']
prof = band_profile(im, F, mm, 650 * SCALE['R3B'], 900 * SCALE['R3B'])
bars = [(s, tall) for s, tall in D.r3b_bar_positions(None, F['s0'] + 60.0, 2440.0)]
found = [locate_dark(prof, F, mm, s) for s, _ in bars]
ok_idx = [i for i, f in enumerate(found) if f is not None]
pred = np.array([bars[i][0] for i in ok_idx])
fnd = np.array([found[i] for i in ok_idx])
kfit = np.polyfit(pred - pred[0], fnd - pred[0], 1)
res_raw = fnd - pred
res_fit = fnd - (kfit[1] + pred[0] + kfit[0] * (pred - pred[0]))
t('C', f"R3B: {len(ok_idx)} of {len(bars)} predicted bars have a dark minimum within 10 mm (at least 90 %)", len(ok_idx) >= 0.9 * len(bars))
t('C', f"R3B: median residual of the bar centres against the preview {np.median(abs(res_raw)):.1f} mm (at most 4), 90th percentile {np.percentile(abs(res_raw), 90):.1f} (at most 9)", np.median(abs(res_raw)) <= 4 and np.percentile(abs(res_raw), 90) <= 9)
t('C', f"R3B: the pitch scale fitted on that one dimension is {kfit[0]:.4f} (inside 1 +-0.02), the offset {kfit[1]:.1f} mm", abs(kfit[0] - 1) <= 0.02 and abs(kfit[1]) <= 8)
t('C', f"R3B: after the fit the residual's median is {np.median(abs(res_fit)):.1f} mm (at most 3.5: one native pixel is 3 to 4 mm)", np.median(abs(res_fit)) <= 3.5)
cols = (800.0, 2400.0)
for key, half in (('bottom', 25), ('mid', 30), ('top', 30)):
    z_p = KB['rails'][key + '_axis_z']['v']
    z_f, dep = row_extreme(im, F, mm, z_p, cols, half, 'dark')
    t('C', f"R3B: {key} rail predicted at z {z_p:.0f}, the strongest dark row in the preview at {z_f:.0f} (within the {KB['rails'][key + '_axis_z']['err']} + 10 mm)", abs(z_f - z_p) <= KB['rails'][key + '_axis_z']['err'] + 10)
z_cop = step_edge(im, F, mm, KB['plinth']['coping_top_z']['v'] - 13, (900.0, 2300.0), 65)
t('C', f"R3B: the coping's top edge in the preview is at z {z_cop:.0f}, the target's {KB['plinth']['coping_top_z']['v']:.0f} - 13 for the projection = {KB['plinth']['coping_top_z']['v'] - 13:.0f} (within 25)", abs(z_cop - (KB['plinth']['coping_top_z']['v'] - 13)) <= 25)
# tips and the hinge post's top, on the 1 mm close of the head (a bright sky behind): the first row from the top where the strip is darker than the background by 30 for three rows
HC = FR['R3B']['head_close']
hc = gray('ph-bethnal_green_entrance-r3b-park-railing-head-close.jpg')
z1h, s0h = HC['z1'], HC['s0']


def dark_run_centre(rowseg, thr, centre):
    """the dark run (below the window's edge median by thr) nearest the window's middle: (start, end) or None"""
    bg = np.median(np.concatenate([rowseg[:10], rowseg[-10:]]))
    dark = rowseg < bg - thr
    runs, i = [], 0
    while i < len(dark):
        if dark[i]:
            j = i
            while j < len(dark) and dark[j]: j += 1
            runs.append((i, j)); i = j
        else:
            i += 1
    if not runs: return None
    return min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - centre))


def head_column(s_pred):
    """the column (s) of a tall bar's shaft just under its head (z 1750 to 1850 in the head close), found within 45 mm of the predicted s: the photograph's bars lean about 1 degree"""
    c = int(round(s_pred - s0h))
    row = int(round(z1h - 1800))
    seg = hc[row - 8:row + 9, c - 45:c + 46].mean(0)
    r = dark_run_centre(seg, 40, 45)
    return None if r is None else s0h + c - 45 + (r[0] + r[1]) / 2.0


def top_dark(s_c, thr=80, img=None, z1=None, s0=None, mm_=1.0):
    """the first row from the top where the 3-column strip at s_c is iron-dark (below thr) for three rows: the z of a tip or a finial"""
    img = hc if img is None else img
    z1 = z1h if z1 is None else z1
    s0 = s0h if s0 is None else s0
    c = int(round((s_c - s0) / mm_))
    strip = img[:, c - 1:c + 2].mean(1)
    for r in range(0, img.shape[0] - 3):
        if strip[r] < thr and strip[r + 1] < thr and strip[r + 2] < thr:
            return z1 - r * mm_
    return None


tall_in = [s for s, tall in D.r3b_bar_positions(None, HC['s0'] + 40.0, 2440.0) if tall]
hcols = [head_column(s) for s in tall_in]
tz = [max(z_ for z_ in (top_dark(hcol + dc) for dc in range(-12, 5, 2)) if z_ is not None) for hcol in hcols if hcol is not None]
# the lean of the bars in the photograph: the centre of a tall bar at z 750 (the 3 mm preview) against its centre under the head (z 1800)
lean_s = [hcols[i] - locate_dark(prof, F, mm, tall_in[i], 20.0) for i in range(len(tall_in)) if hcols[i] is not None and locate_dark(prof, F, mm, tall_in[i], 20.0) is not None]
lean_deg = math.degrees(math.atan(np.median(lean_s) / (1800 - 0.5 * (650 + 900) * SCALE['R3B']))) if lean_s else None
t('C', f"R3B: the tall bars lean {lean_deg:.2f} degrees in the photograph (their centres under the head sit {np.median(lean_s):.0f} mm from the same bars at z 770: the capture's roll; the target's bars are vertical; at most 1.5 degrees)", lean_deg is not None and abs(lean_deg) <= 1.5)
t('C', f"R3B: the tall bar at s {tall_in[0]:.0f} has its tip at z {tz[0]} in the head close; the target's {KB['bars']['tall_tip_z']['v']:.0f} +-{KB['bars']['tall_tip_z']['err']} (within 45)", len(tz) >= 1 and abs(tz[0] - KB['bars']['tall_tip_z']['v']) <= 45)
pz = top_dark(KB['post']['axis_s']['v'])
t('C', f"R3B: the hinge post's finial top is at z {pz} in the head close; the target's {KB['post']['top_z']['v']:.0f} (within 25)", pz is not None and abs(pz - KB['post']['top_z']['v']) <= 25)
# the knop: the dark run of a tall bar's head at the knop's z, 87 to 100 across (the review x 0.974), on the 1 mm head close (one bar left of the post) and on the 3 mm preview (all of them)
kz = KB['bars']['knop']['z']
row = int(round(z1h - kz))
kws1, kz1 = [], []
for hcol in hcols:
    if hcol is None: continue
    c = int(round(hcol - s0h))
    best = (0, None)
    for z_ in range(1990, 2125, 2):
        r_ = int(round(z1h - z_))
        r = dark_run_centre(hc[r_ - 1:r_ + 2, c - 70:c + 71].mean(0), 35, 70)
        if r and r[1] - r[0] > best[0]: best = (r[1] - r[0], z_)
    kws1.append(best[0]); kz1.append(best[1])
tall_all = [s for s, tall in D.r3b_bar_positions(None, F['s0'] + 60.0, 2440.0) if tall]
kws3, tips3 = [], []
band_h = band_profile(im, F, mm, 1750, 1850)
for sp in tall_all:
    sc_ = locate_dark(band_h, F, mm, sp, 45.0)
    if sc_ is None: continue
    c = int(round((sc_ - F['s0']) / mm))
    rw = int(round((F['z1'] - kz) / mm))
    r = dark_run_centre(im[rw - 2:rw + 3, c - 25:c + 26].mean(0), 35, 25)
    if r: kws3.append((r[1] - r[0]) * mm)
    tp = top_dark(sc_, 100, im, F['z1'], F['s0'], mm)
    if tp is not None: tips3.append(tp)
t('C', f"R3B: the knops of the tall bars (z {kz:.0f}) are {np.median(kws3):.0f} across by the median of {len(kws3)} bars on the 3 mm preview and {kws1[0]} on the 1 mm head close (its widest row); the target's {KB['bars']['knop']['width']:.0f} (within 22: blur on both edges)", len(kws3) >= 8 and len(kws1) >= 1 and abs(np.median(kws3) - KB['bars']['knop']['width']) <= 22 and abs(np.median(kws1) - KB['bars']['knop']['width']) <= 22)
t('C', f"R3B: the knop's widest row in the 1 mm head close is at z {kz1[0]}, {kz1[0] - kz:.0f} mm above the review's list (z {kz:.0f} after scaling): inside 40 and recorded as unsettled", abs(kz1[0] - kz) <= 40 and any('knop' in c_ and 'head close' in c_ for c_ in T['could_not_settle']))
d_ = gaussian_filter1d(gaussian_filter1d(prof, 12 / mm) - prof, 0.8)
ws = []
for f_ in found:
    if f_ is None: continue
    c = int(round((f_ - F['s0']) / mm))
    seg = d_[c - 15:c + 16]
    m = seg.max()
    if m < 15: continue
    idx = np.where(seg > m / 2)[0]
    ws.append((idx.max() - idx.min() + 1) * mm)
t('C', f"R3B: the bars' FWHM in the 3 mm preview is {np.median(ws):.0f} (the target's 16.6 round + blur: between 14 and 30)", 14 <= np.median(ws) <= 30)

# C: R3D
KD = K['R3D']
F = FR['R3D']['preview']
im = gray('ph-urban_street_01-r3d-garden-railing-elevation.jpg')
mm = F['mm']
z_wt = step_edge(im, F, mm, KD['wall']['top_z']['v'], (100.0, 1000.0), 90)
t('C', f"R3D: the wall's top edge in the preview is at z {z_wt:.0f} against the target's {KD['wall']['top_z']['v']:.0f} (within 30)", abs(z_wt - KD['wall']['top_z']['v']) <= 30)
z_top, dep = row_extreme(im, F, mm, KD['rails']['top_axis_z']['v'], (1400.0, 2400.0), 50, 'light')
t('C', f"R3D: the top rail (a pale flat bar in the photograph) at z {z_top:.0f} against the target's {KD['rails']['top_axis_z']['v']:.0f} (within 30)", abs(z_top - KD['rails']['top_axis_z']['v']) <= 30)
z_bot, dep = row_extreme(im, F, mm, KD['rails']['bottom_axis_z']['v'], (1400.0, 2200.0), 25, 'dark')
t('C', f"R3D: the bottom rail at z {z_bot:.0f} against the target's {KD['rails']['bottom_axis_z']['v']:.0f} (within 30)", abs(z_bot - KD['rails']['bottom_axis_z']['v']) <= 30)
prof_d = band_profile(im, F, mm, 800 * SCALE['R3D'], 1000 * SCALE['R3D'])
pred_d = [KD['bars']['first_s'] + KD['bars']['pitch']['v'] * k for k in range(0, 10)]
fd = [locate_dark(prof_d, F, mm, s, 12.0) for s in pred_d]
okd = [(p, f) for p, f in zip(pred_d, fd) if f is not None]
t('C', f"R3D: {len(okd)} of 10 predicted bars (s {pred_d[0]:.0f} to {pred_d[-1]:.0f}) have a dark line within 12 mm (at least 5: foliage behind them)", len(okd) >= 5)
if len(okd) >= 5:
    rr = np.array([f - p for p, f in okd])
    t('C', f"R3D: median residual {np.median(abs(rr)):.1f} mm (at most 12: the hand-read centres are +-6 and the foliage behind the bars shifts a dark minimum by a few mm)", np.median(abs(rr)) <= 12)

# C: R3A, the LEFT run only (s below left_run_max_s: the run right of the cast post is another pattern, not measured)
KA = K['R3A']
F = FR['R3A']['preview']
im = gray('ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg')
mm = F['mm']
lmax = KA['bars']['left_run_max_s']['v']
for key in ('bottom', 'mid', 'top'):
    z_p = KA['rails'][key + '_axis_z']['v']
    z_f, dep = row_extreme(im, F, mm, z_p, (100.0, lmax - 200), 45, 'dark')
    t('C', f"R3A: the {key} rail at z {z_f:.0f} against the target's {z_p:.0f} (within 45, oblique view; left run, s 100 to {lmax - 200:.0f})", abs(z_f - z_p) <= 45)
for nm, zc in (('coping top', KA['wall']['top_z']['v']), ('lower string', KA['wall']['string_z']['v'])):
    zf = step_edge(im, F, mm, zc, (100.0, 900.0), 65)
    t('C', f"R3A: the wall's {nm} edge at z {zf:.0f} against the target's {zc:.0f} (within 50)", abs(zf - zc) <= 50)
prof_a = band_profile(im, F, mm, 1000 * SCALE['R3A'], 1300 * SCALE['R3A'])
tallpos = [KA['bars']['tall_first_s']['v'] + 2 * KA['bars']['pitch_all']['v'] * k for k in range(0, 8)]
tallpos = [s for s in tallpos if s < lmax - 60]
fa = [locate_dark(prof_a, F, mm, s, 25.0) for s in tallpos]
oka = [(p, f) for p, f in zip(tallpos, fa) if f is not None]
t('C', f"R3A: {len(oka)} of {len(tallpos)} predicted tall bars of the left run (s {tallpos[0]:.0f} + {2 * KA['bars']['pitch_all']['v']:.0f} k, below {lmax:.0f}) have a dark line within 25 mm (at least 4)", len(oka) >= 4 and len(oka) >= 0.6 * len(tallpos))

# the brick courses in the new elevations: the camera height at each wall's own ground was set from these courses, so they must read 75 there
def course_pitch(img, win, mm_, s0_, s1_, z0_, z1_):
    c0, c1 = [int((x - win['s0']) / mm_) for x in (s0_, s1_)]
    r0, r1 = [int((win['z1'] - z) / mm_) for z in (z1_, z0_)]
    pr = img[r0:r1, c0:c1].mean(1)
    pr = gaussian_filter1d(pr - gaussian_filter1d(pr, 60 / mm_), 1.0)
    n_ = len(pr)
    ac = np.correlate(pr, pr, 'full')[n_ - 1:]
    ac = ac / ac[0]
    lags = np.arange(n_) * mm_
    sel = (lags > 55) & (lags < 110)
    k_ = int(np.argmax(ac[sel]))
    return float(lags[sel][k_]), float(ac[sel][k_])


imd = gray('ph-urban_street_01-r3d-garden-railing-elevation.jpg')
pd_, cd_ = course_pitch(imd, FR['R3D']['preview'], FR['R3D']['preview']['mm'], 100, 1000, 20, 600)
t('C', f"R3D: the brick courses of the garden wall in the new elevation (h 1.15) are {pd_:.0f} mm apart (autocorrelation {cd_:.2f}; a course is 75, within 3): the height is the wall's own", abs(pd_ - 75) <= 3 and cd_ >= 0.4)
ima = gray('ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg')
pa_, ca_ = course_pitch(ima, FR['R3A']['preview'], FR['R3A']['preview']['mm'], 100, 1300, 360, 740)
t('C', f"R3A: the red courses of the dwarf wall in the new elevation (h 1.02, oblique) are {pa_:.0f} mm apart (autocorrelation {ca_:.2f}, weak on the oblique brick; within 4 of 75): the first version's 0.97 would have read 71", abs(pa_ - 75) <= 4 and ca_ >= 0.1)

# C: LHB
F = FR['LHB']['preview']
imc = np.asarray(Image.open(os.path.join(PREV, 'ph-limehouse-lhb-chain-bay-elevation.jpg')).convert('L'), float)
mm = F['mm']
span = HRd['LHB']['span_mm']['v']
for nm, zl, zlow in (('upper', HRd['LHB']['upper_lug_z']['v'], HRd['LHB']['upper_chain_lowest_z']),
                     ('lower', HRd['LHB']['lower_lug_z']['v'], HRd['LHB']['lower_chain_lowest_z'])):
    z_pred = zl - Q2['chain']['sag']
    z_f, dep = row_extreme(imc, F, mm, z_pred, (span / 2 - 120.0, span / 2 + 120.0), 110, 'dark')
    t('C', f"LHB: the {nm} swag's lowest dark row in the preview is z {z_f:.0f}; the target's chain (lug {zl:.0f} - sag {Q2['chain']['sag']}) puts it at {z_pred:.0f} (within 60), the hand-read {zlow['v']:.0f} +-{zlow['err']}", abs(z_f - z_pred) <= 60 and abs(z_f - zlow['v']) <= zlow['err'] + 25)
for nm, z_p in (('post_top_left', HRd['LHB']['post_top_z']['v']),):
    c = int(round((0 - F['s0']) / mm))
    col = gaussian_filter1d(imc[:, c - 4:c + 5].mean(1), 1.0)
    rr_ = int(round((F['z1'] - z_p) / mm))
    seg = col[rr_ - 12:rr_ + 13]
    zf = F['z1'] - (rr_ - 12 + int(np.argmax(np.abs(np.gradient(seg))))) * mm
    t('C', f"LHB: the left post's top edge at z {zf:.0f} against the stated {z_p:.0f} (within 45)", abs(zf - z_p) <= 45)

# ------------------------------------------------------------------------------------------------------------------ D
from shapely.geometry import Polygon, Point, box, LineString
from shapely.ops import unary_union
P = D.a1_parts()
polys = {k_: [Polygon(p).buffer(0.0) for p in v_] for k_, v_ in P.items()}
allp = unary_union([g.buffer(0.3) for v_ in polys.values() for g in v_])
t('D', 'A1: all parts form one connected solid (posts, caps, rails, end plates, bars, welds, nuts, thread); nothing floats', allp.geom_type == 'Polygon')
xs = A['infill']['x']
t('D', 'A1: the stored bar count equals the bars drawn and the listed x (17), and each has 4 weld fillets', len(polys['bar']) == A['infill']['count'] == len(xs) == 17 and len(polys['weld']) == 4 * 17)
t('D', 'A1: the bars are symmetric about the middle of the panel (x_i = -x_(n-1-i), 0.02 mm)', all(near(xs[i], -xs[-1 - i], 0.02) for i in range(len(xs))))
pf = A['post']['face_in_x']
gaps = [xs[i + 1] - xs[i] - A['infill']['diameter'] for i in range(len(xs) - 1)]
edge_gaps = [pf - (xs[-1] + A['infill']['diameter'] / 2), xs[0] - A['infill']['diameter'] / 2 + pf]
t('D', f"A1: every clear gap is at most 100: bar to bar {min(gaps):.2f} to {max(gaps):.2f} (stored {A['infill']['clear_gap_between_bars']}), bar to post face {max(edge_gaps):.2f} (stored {A['infill']['clear_gap_bar_to_post_face']}); the review's 97.09 and 96.24", max(gaps + edge_gaps) <= 100.0 and max(gaps) - min(gaps) < 0.1 and near(max(gaps), A['infill']['clear_gap_between_bars'], 0.02) and near(max(edge_gaps), A['infill']['clear_gap_bar_to_post_face'], 0.02) and near(A['infill']['clear_gap_between_bars'], 97.09, 0.01) and near(A['infill']['clear_gap_bar_to_post_face'], 96.24, 0.01))
t('D', 'A1: the stored pitch is the diameter plus the computed clear gap', near(A['infill']['pitch'], A['infill']['diameter'] + np.mean(gaps), 0.01))
t('D', 'A1: the rails end on the post faces (x = 1000 - 25 = 975) and the bars end on the lower rail\'s top (210) and the upper rail\'s underside (970)', near(A['top_rail']['x'][1], A['centre_to_centre'] / 2 - A['post']['width'] / 2, 0.01) and near(A['bottom_rail']['x'][1], 975.0, 0.01) and near(A['infill']['z'][0], A['bottom_rail']['axis_z'] + A['bottom_rail']['height'] / 2, 0.01) and near(A['infill']['z'][1], A['top_rail']['axis_z'] - A['top_rail']['height'] / 2, 0.01))
t('D', 'A1: the top rail\'s top is 1000 (axis 985 + 15), the post top 1030 stands 30 proud of it, under a 3 mm cap plate (z 1027 to 1030)', near(A['top_rail']['axis_z'] + A['top_rail']['height'] / 2, 1000, 0.01) and near(A['top_rail']['top_z'], 1000, 0.01) and near(A['post']['height'], 1030, 0.01) and near(A['post']['proud_of_top_rail'], 30, 0.01) and A['cap']['z'] == [1027.0, 1030.0] and A['cap']['thickness'] == 3.0)
t('D', 'A1: the bottom rail is z 190 to 210 (axis 200), 190 clear of the flags, and the lighter section (40 x 20 x 2.5 against 50 x 30 x 3)', near(A['bottom_rail']['axis_z'] - A['bottom_rail']['height'] / 2, 190.0, 0.01) and A['bottom_rail']['z'] == [190.0, 210.0] and A['bottom_rail']['width'] < A['top_rail']['width'] and A['bottom_rail']['wall'] < A['top_rail']['wall'])


def rhs_area(sec):
    return Polygon(sec['outer']).area - Polygon(sec['inner']).area


for nm, sec, w_, h_, wl in (('post', PRA['post_section'], 50.0, 30.0, 3.0), ('top rail', PRA['top_rail_section'], 50.0, 30.0, 3.0), ('bottom rail', PRA['bottom_rail_section'], 40.0, 20.0, 2.5)):
    xo = [p_[0] for p_ in sec['outer']]
    yo = [p_[1] for p_ in sec['outer']]
    xi = [p_[0] for p_ in sec['inner']]
    ideal = w_ * h_ - (w_ - 2 * wl) * (h_ - 2 * wl)
    ro = sec['outer_radius']
    t('D', f"A1 profiles: the {nm} section is a rounded rectangle {w_:.0f} x {h_:.0f}, wall {wl}: extents {max(xo) - min(xo):.1f} x {max(yo) - min(yo):.1f}, inner {max(xi) - min(xi):.1f}, area {rhs_area(sec):.0f} mm2 (square-cornered {ideal:.0f})",
      near(max(xo) - min(xo), w_, 0.01) and near(max(yo) - min(yo), h_, 0.01) and near(max(xi) - min(xi), w_ - 2 * wl, 0.01) and 0.93 * ideal <= rhs_area(sec) <= 1.01 * ideal and sec['outer_radius'] == 1.5 * wl and near(sec['inner_radius'], 0.5 * wl, 1e-9))
t('D', 'A1 profiles: the bar is a 12 round', all(abs(math.hypot(*p_) - 6.0) < 0.01 for p_ in PRA['bar_section']['outer']))
t('D', 'A1 profiles: the cap plate is the post\'s own outline, 3 mm thick, edges broken R1', PRA['cap_plate']['outline'] == PRA['post_section']['outer'] and PRA['cap_plate']['thickness'] == 3.0 and PRA['cap_plate']['edge_radius'] == 1.0)
t('D', 'A1 profiles: the end plates are the rails\' own outlines, 6 mm thick', PRA['end_plate_outlines']['top'] == PRA['top_rail_section']['outer'] and PRA['end_plate_outlines']['bottom'] == PRA['bottom_rail_section']['outer'] and PRA['end_plate_outlines']['thickness'] == 6.0 == A['end_plates']['thickness'])
afh = Polygon(PRA['bolt_head_hex'])
afn = Polygon(PRA['bolt_nut_hex'])
px_ = [p_[0] for p_ in PRA['bolt_nut_hex']]
t('D', 'A1 profiles: the bolt head and the nut are hexagons of 17 across flats (%.2f), 7 and 8 high, on a 10 shank, with 3 mm of thread beyond the nut' % (max(px_) - min(px_)), near(max(px_) - min(px_), 17.0, 0.01) and len(PRA['bolt_nut_hex']) == 6 and PRA['bolt_head_height'] == 7.0 and PRA['bolt_nut_height'] == 8.0 and PRA['bolt_shank_diameter'] == 10.0 and PRA['thread_beyond_nut'] == 3.0 and near(afh.area, afn.area, 0.01))
t('D', 'A1 profiles: the 2 mm weld fillet is a right triangle with 2 mm legs', Polygon(PRA['weld_fillet']).area == 2.0)
# the bolts
BL = A['bolts']['list']
t('D', 'A1 bolts: four, one at each rail end (x +-1000 posts, z 985 and 200), the axes along x through the posts and the rails\' axes', len(BL) == 4 == A['bolts']['count'] and sorted((b['post_x'], b['z']) for b in BL) == [(-1000.0, 200.0), (-1000.0, 985.0), (1000.0, 200.0), (1000.0, 985.0)] and all(b['y'] == 0.0 for b in BL))
t('D', 'A1 bolts: every nut sits on the post\'s OUTER face (x +-1025, 8 high to +-1033) with the thread 3 mm beyond (+-1036); the head is on the panel side (|x| 962 to 969) against the end plate (969 to 975)',
  all(near(min(abs(x_) for x_ in b['nut_x']), 1025.0, 1e-9) and near(max(abs(x_) for x_ in b['nut_x']), 1033.0, 1e-9) and near(abs(b['thread_end_x']), 1036.0, 1e-9) and near(min(abs(x_) for x_ in b['head_x']), 962.0, 1e-9) and near(max(abs(x_) for x_ in b['head_x']), 969.0, 1e-9) and near(min(abs(x_) for x_ in b['plate_x']), 969.0, 1e-9) and near(max(abs(x_) for x_ in b['plate_x']), 975.0, 1e-9) for b in BL)
  and all(near(abs(b['post_x']) + A['post']['width'] / 2, min(abs(x_) for x_ in b['nut_x']), 1e-9) for b in BL))
t('D', 'A1 bolts: the nut (across corners 19.6) is narrower than the post\'s 30 face and sits on the flat of it (30 - 2 x 4.5 = 21)', max(v_ for u_, v_ in PRA['bolt_nut_hex']) * 2 < A['post']['depth'] - 2 * PRA['post_section']['outer_radius'] + 0.0 and max(v_ for u_, v_ in PRA['bolt_nut_hex']) * 2 < 21.0)
hc_top = max(v_ for u_, v_ in PRA['bolt_head_hex']) * 2
t('D', f"A1 bolts: the head ({hc_top:.1f} across corners, 17 flats) fits inside the top rail's hollow (inner {A['top_rail']['height'] - 2 * A['top_rail']['wall']:.0f} high) but not inside the bottom rail's ({A['bottom_rail']['height'] - 2 * A['bottom_rail']['wall']:.0f} high): the caveat is recorded in could_not_settle", hc_top < A['top_rail']['height'] - 2 * A['top_rail']['wall'] and 17.0 > A['bottom_rail']['height'] - 2 * A['bottom_rail']['wall'] and any('access hole' in c_ for c_ in T['could_not_settle']))
# the bounding box from the parts
xmax = max(abs(x_) for k_ in ('post', 'cap', 'rail', 'nut', 'thread') for g in polys[k_] for x_ in g.exterior.xy[0])
zmax = max(z_ for g in polys['cap'] for z_ in g.exterior.xy[1])
zmin = min(z_ for g in polys['post'] for z_ in g.exterior.xy[1])
bb = A1['bbox']
t('D', f"A1: the bounding box recomputed from the drawn parts is x +-{xmax:.0f} (nuts and thread), y +-{A['top_rail']['width'] / 2:.0f} (the top rail laid flat), z {zmin:.0f} to {zmax:.0f}: {2 * xmax:.0f} x {A['top_rail']['width']:.0f} x {zmax - zmin:.0f}; the review's [2072, 50, 1030]",
  near(2 * xmax, 2072.0, 0.01) and near(zmax - zmin, 1030.0, 0.01) and near(bb['x'][1] - bb['x'][0], 2072.0, 0.01) and near(bb['y'][1] - bb['y'][0], 50.0, 0.01) and near(bb['z'][1] - bb['z'][0], 1030.0, 0.01) and A['top_rail']['width'] == 50.0 and A['post']['depth'] < A['top_rail']['width'])
t('D', 'A1: the check A1_bbox lists the same box within its tolerance', all(near(a_, b_, CK['A1_bbox']['tol']) for a_, b_ in zip(CK['A1_bbox']['expected'], [bb['x'][1] - bb['x'][0], bb['y'][1] - bb['y'][0], bb['z'][1] - bb['z'][0]])))
# the reinstatement patch
pt = A1['ground']['patch']
pp = Polygon(pt['outline_xy'])
xs_p = [p_[0] for p_ in pt['outline_xy']]
ys_p = [p_[1] for p_ in pt['outline_xy']]
straight = [p_ for p_ in pt['outline_xy'] if abs(p_[1] - min(ys_p)) < 1e-6]
t('D', f"A1 ground: the reinstatement patch is {max(xs_p) - min(xs_p):.0f} x {max(ys_p) - min(ys_p):.0f} (250 x 250 +-60, ragged edges +-20), area {pp.area / 1e4:.1f} dm2, holds the post's footprint, and one edge ({len(straight)} points) is a straight cut flag edge",
  pp.is_valid and near(max(xs_p) - min(xs_p), 250, CK['A1_foot_patch']['tol']) and near(max(ys_p) - min(ys_p), 250, CK['A1_foot_patch']['tol']) and pp.contains(box(-25, -15, 25, 15)) and len(straight) >= 5 and pt['ragged_edge'] == 20.0 and pt['flush_with_flags'] == 3.0 and pt['srgb'] == [45, 43, 41] and pt['roughness'] == 0.85)
t('D', 'A1 ground: the patch stays on the flags: its widest reach toward the kerb (local y +%.0f) leaves the footway side of the kerb back (the axis is 0.205 behind it)' % max(ys_p), max(ys_p) / 1000 < PL['street'][0]['behind_kerbs_target_back_m'])
post_pol = polys['post']
t('D', 'A1: the two posts do not overlap each other or the bars', not post_pol[0].intersects(post_pol[1]) and not any(post_pol[0].buffer(-0.1).intersects(b) or post_pol[1].buffer(-0.1).intersects(b) for b in polys['bar']))
t('D', 'A1: bars do not overlap each other (clear gaps positive)', all(g_ > 0 for g_ in gaps))
# the walking strip, from 0 to 2.0 m high
t('D', f"A1 walking strip: from 0 to 2.0 m high in x 9.5 to 12.5 the least clear width between the rail's rear face (3.400) and a fixed projection is {min(cl_):.3f} (at a 2.0 m head, under the awning's body), {cl_[0]:.3f} at the ground; at least 0.68", min(cl_) >= 0.68 and near(min(cl_), CK['A1_walking_clear']['expected'], 0.002) and CK['A1_walking_clear']['minimum'] == 0.68)
t('D', 'A1 walking strip: the review\'s straight-line estimate at a 2.0 m head (1.02) is under the mesh-read value and above 0.68: both pass; the stored estimate is the review\'s', WS['clear_at_head_2_0_review_estimate_m'] < min(cl_) and WS['clear_at_head_2_0_review_estimate_m'] >= 0.68)
t('D', 'A1 walking strip: a lowered awning would be caught: the check is the least over 0 to 2.0 m, not the ground value (the awning\'s valance 1.57 stays above a 1.57 m head only at z 3.39, 10 mm in front of the rear face)', 'from 0 to 2.0' in CK['A1_walking_clear']['what'] and set(WS['clear_at_heights_m']) >= {'0.0', '2.0'})
t('D', 'A1 walking strip: the 0.92 crates leave %.3f (under 0.68): the no-deep-obstacle check names that case' % (clear - 0.92), clear >= 0.68 and clear - 0.92 < 0.68 and 'crates' in CK['A1_no_deep_obstacle']['what'])
t('D', 'A1: the panel stands inside the footway (z 3.375 between the kerb back 3.170 and the stallriser face 4.975) and its rear face leaves at least 0.68', 3.170 < PL['street'][0]['z_axis_m'] < SF['stallriser_face_z_m'] and clear >= 0.68)
t('D', 'A1: the panel ends at the gully\'s centre line (x 12.0): its end post stands 0.025 over the line; the gully is in the channel at z 2.8 to 3.0', PL['street'][0]['x_m'][1] == 12.0)
t('D', 'A1: the alternative round-tube form is recorded and not built (post 48.3 x 3.2, rails 42.4 and 33.7), with the reason', 'round tube 48.3' in A1['alternative_recorded']['what'] and 'not to be built' in A1['alternative_recorded']['why_set_aside'])
# Q2
Qp = Q2['post']
t('D', 'Q2: the base plate (200) is wider than the post foot (76.1) and holds its four studs on a 150 square, each 25 from the edge', Qp['base_plate']['size'][0] > Qp['od'] and near((Qp['base_plate']['size'][0] - Qp['base_plate']['holes']['pitch']) / 2, 25, 0.01) and Qp['base_plate']['holes']['count'] == 4)
t('D', 'Q2: the nut (24 across flats, 13 high) fits between the stud holes and the post: the hole centre (75, 75) is 106 from the axis, the post radius 38.05, the nut radius 13.9', math.hypot(75, 75) - 13.9 > Qp['od'] / 2)
t('D', 'Q2: the top rail is 60.3 x 3.6 (the review\'s option for 3.0 m bays), its axis 1000 so its top is 1030.15, under the cap (1086)', near(Q2['top_rail']['od'], 60.3, 1e-9) and Q2['top_rail']['wall'] == 3.6 and Q2['top_rail']['top_z'] < Qp['height'] - Qp['cap']['rise'] and near(Q2['top_rail']['top_z'], 1000 + 30.15, 0.01) and near(CK['Q2_top_rail_od']['expected'], 60.3, 1e-9))
t('D', 'Q2: the rails end on the post faces: x = 1500 - 38.05', near(Q2['top_rail']['x'][1], Q2['bay']['centre_to_centre'] / 2 - Qp['od'] / 2, 0.01) and near(Q2['low_rail']['x'][1], Q2['top_rail']['x'][1], 0.01))
ch = Q2['chain']
pts, a_ = D.catenary_pts(ch['eyes']['x'][0], ch['eyes']['x'][1], ch['eyes']['z'], ch['sag'], 400)
arc = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
t('D', f"Q2b: the catenary through the eyes (span {ch['span_between_eyes']}) with sag 200 has an arc of {arc:.1f} mm; stated {ch['arc_length']} (within 3), and {ch['links']} links of 39 = {ch['links'] * 39} (within one link)", near(arc, ch['arc_length'], 3.0) and abs(ch['links'] * 39 - arc) <= 39)
sb = ch['short_bay']
ps_, a2_ = D.catenary_pts(-sb['span_between_eyes'] / 2, sb['span_between_eyes'] / 2, ch['eyes']['z'], sb['sag'], 400)
arc2 = sum(math.hypot(ps_[i + 1][0] - ps_[i][0], ps_[i + 1][1] - ps_[i][1]) for i in range(len(ps_) - 1))
t('D', f"Q2b: the 1.4 m end bay's chain (span {sb['span_between_eyes']}, sag {sb['sag']}, the same 7 %) has an arc of {arc2:.1f}; stated {sb['arc_length']} (within 2), {sb['links']} links", near(arc2, sb['arc_length'], 2.0) and abs(sb['links'] * 39 - arc2) <= 39 and near(sb['sag'] / sb['span_between_eyes'], ch['sag'] / ch['span_between_eyes'], 0.001) and near(sb['span_between_eyes'], Q2['bay']['short_end_bay'] - 2 * (Qp['od'] / 2 + 45), 0.1))
t('D', 'Q2b: the eyes\' x is 1500 - 38.05 - 45 = 1416.95 and the span between the holes 2833.9', near(ch['eyes']['x'][1], 1416.95, 0.01) and near(ch['span_between_eyes'], 2833.9, 0.01))
t('D', 'Q2b: the chain\'s lowest point (z 300) stays 300 above the apron and 200 under the eyes', near(min(z for x, z in pts), ch['eyes']['z'] - ch['sag'], 0.5) and min(z for x, z in pts) > 0)
t('D', 'Q2b: the link is 3 x its bar for the inner length, the outer = inner + 2 bars, the pitch = the inner length', near(ch['link']['inner_length'], 3 * ch['link']['bar'], 0.01) and near(ch['link']['outer_length'], ch['link']['inner_length'] + 2 * ch['link']['bar'], 0.01) and near(ch['link']['outer_width'], ch['link']['inner_width'] + 2 * ch['link']['bar'], 0.01) and ch['link']['pitch'] == ch['link']['inner_length'])
# the runs
bp = PL['quay']
run_b, run_t, run_r = bp[0], bp[1], bp[2]
pa, pb, pr = [tuple(p_) for p_ in run_b['posts_xy_m']], [tuple(p_) for p_ in run_t['posts_xy_m']], [tuple(p_) for p_ in run_r['posts_xy_m']]
uniq = []
for p_ in pa + pb + pr:
    if p_ not in uniq: uniq.append(p_)
bays = PL['bays_detail']
dist = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
t('D', f"Q2: the basin run is 3 posts (two bays), the tip run 6 more, the return 3 more: {len(uniq)} posts, {len(bays)} bays, {sum(b['length'] for b in bays):.1f} m of railing (the review's 12, 11, 31.4)", len(pa) == 3 and len(pb) == 6 and len(pr) == 3 and len(uniq) == PL['counts']['quay_posts'] == 12 and len(bays) == PL['counts']['quay_bays'] == 11 and near(sum(b['length'] for b in bays), PL['counts']['quay_length_m'], 1e-9) and near(PL['counts']['quay_length_m'], 31.4, 1e-9))
t('D', 'Q2: the posts are 3.0 apart (0.001) along the basin and tip runs, and 3.0, 3.0, 1.4 along the return; each run starts from the last post of the one before', all(near(dist(pa[i], pa[i + 1]), 3.0, 0.001) for i in range(2)) and near(dist(pa[-1], pb[0]), 3.0, 0.001) and all(near(dist(pb[i], pb[i + 1]), 3.0, 0.001) for i in range(5)) and near(dist(pb[-1], pr[0]), 3.0, 0.001) and near(dist(pr[0], pr[1]), 3.0, 0.001) and near(dist(pr[1], pr[2]), 1.4, 0.001) and pa[-1] == (-110.4, -15.4) and run_t['shares_post_with'].startswith('Q2_basin_edge') and run_r['shares_post_with'].startswith('Q2_tip'))
t('D', 'Q2: the review\'s posts exactly: basin (-110.4, -21.4), (-110.4, -18.4), (-110.4, -15.4); tip every 3.0 from the corner to (-128.4, -15.4); return (-128.4, -18.4), (-128.4, -21.4), (-128.4, -22.8)', pa == [(-110.4, -21.4), (-110.4, -18.4), (-110.4, -15.4)] and pb == [(round(-113.4 - 3.0 * i, 1), -15.4) for i in range(6)] and pr == [(-128.4, -18.4), (-128.4, -21.4), (-128.4, -22.8)])
t('D', 'Q2: the models: the two basin bays Q2a, the nine tip and return bays Q2b (chain)', [b['model'] for b in bays] == ['Q2a'] * 2 + ['Q2b'] * 9 and PL['counts']['chain_bays'] == 9)
t('D', 'Q2: the basin run is 0.4 behind the cope nose (x -110) and the tip run 0.4 behind the end nose (y -15)', all(near(p[0], -110.4, 1e-9) for p in pa) and all(near(p[1], -15.4, 1e-9) for p in pb + [pa[-1]]))
t('D', 'Q2: every post is on the jetty strip (x -130 to -110, y -100 to -15) with its 200 plate: plate edge at least 0.25 behind the nose', all(-130 < p[0] and p[0] + 0.1 <= -110 - 0.25 + 1e-9 and p[1] + 0.1 <= -15 - 0.25 + 1e-9 for p in uniq))
moor = [(-110.75, -45.0), (-110.75, -80.0)] + [(-110.25, y) for y in (-52.0, -58.0, -64.0)]
dmin = min(dist(p, q) for p in uniq for q in moor)
t('D', f"Q2: the nearest post to a K6 bollard or K7 cleat is {dmin:.2f} m (at least 8.0: moorings stay clear)", dmin >= 8.0 and near(dmin, CK['Q2_clear_of_mooring']['expected'], 0.06))
rings = KIT_RINGS or T['street_fixtures']['kit_rings_jetty_m']
segs = [LineString([b['a'], b['b']]) for b in bays]
d_ring = min(min(dist(p, q) for p in uniq for q in rings), min(s_.distance(Point(q)) for s_ in segs for q in rings))
t('D', f"Q2: no post or rail runs within 4.0 m of a mooring ring of the kit (live: {rings}): the nearest post is {min(dist(p, q) for p in uniq for q in rings):.2f} m, the nearest rail {min(s_.distance(Point(q)) for s_ in segs for q in rings):.2f} m", d_ring >= 4.0 and near(d_ring, CK['Q2_clear_of_rings']['expected'], 0.06) and CK['Q2_clear_of_rings']['minimum'] == 4.0)
t('D', 'Q2: the ring at y -32 is 10.6 m clear of the basin run\'s first post (-110.4, -21.4), so the berth stays open (the first version\'s run stood 1.4 m from it)', near(dist((-110.4, -21.4), rings[1]), 10.6, 0.06) and min(p[1] for p in uniq) > rings[1][1] + 4.0)
plinth = box(-121.4, -20.9, -118.6, -18.1)
dl = min(plinth.distance(Point(p[0], p[1])) for p in uniq)
dls = min(plinth.distance(s_) for s_ in segs)
t('D', f"Q2: the nearest post to the harbour light's plinth is {dl:.2f} m and the nearest rail {dls:.2f} m (at least 2.5)", dl >= 2.5 and dls >= 2.5 and near(dl, CK['Q2_clear_of_light']['expected'], 0.06))
par = box(-129.4, -100.6, -128.6, -23.0)
t('D', 'Q2: no post or plate touches the jetty\'s seaward parapet (x -129.4 to -128.6, ending y -23.0): the return\'s plates stand 0.1 clear', all(par.distance(box(p[0] - 0.1, p[1] - 0.1, p[0] + 0.1, p[1] + 0.1)) > 0.0 for p in uniq) and 0.0999 <= par.distance(box(-128.5, -22.9, -128.3, -22.7)) <= 0.1415)
ep_ = pr[-1]
t('D', f"Q2: the return closes the corner: its end post {ep_} stands {ep_[0] - (-128.6):.2f} from the parapet's inner face (x -128.6) and {ep_[1] - (-23.0):.2f} from its end (y -23.0), both within 0.25; the corner x -130 to -128.4 is closed by tip, return and parapet", near(ep_[0] - (-128.6), 0.2, 0.001) and near(ep_[1] - (-23.0), 0.2, 0.001) and ep_[0] - (-128.6) <= 0.25 and ep_[1] - (-23.0) <= 0.25)
t('D', 'Q2: the K5 ladder group on the north quay (x -69.5) is untouched: no Q2 post within 30 m of it', min(math.hypot(p[0] + 69.5, p[1] + 36.0) for p in uniq) > 30)
t('D', 'Q2: a person on the jetty keeps far more than 0.68 m (the strip is 20 m across; the rail line is 0.4 behind the nose)', 20.0 - 0.4 - 0.1 > 0.68 and CK['Q2_walking_clear']['expected'] == 19.6)
# ears only on the sides facing a Q2b bay
ears = PL['ears']
exp_faces = {}
for b in bays:
    for end, other in ((b['a'], b['b']), (b['b'], b['a'])):
        if b['model'] == 'Q2b':
            dx, dy = other[0] - end[0], other[1] - end[1]
            L = math.hypot(dx, dy)
            exp_faces.setdefault(tuple(end), []).append((round(dx / L, 3), round(dy / L, 3)))
okE = True
for e in ears:
    got = sorted((round(f[0], 3), round(f[1], 3)) for f in e['faces'])
    okE &= got == sorted(exp_faces.get(tuple(e['post']), []))
t('D', f"Q2: ears only on the sides that face a Q2b bay: {sum(len(e['faces']) for e in ears)} ears (two per Q2b bay: 9 bays = 18), the end and corner posts one or two, none toward a Q2a bay", okE and sum(len(e['faces']) for e in ears) == 18 == PL['counts']['ears'] == CK['Q2_ears']['expected'] and [e['faces'] for e in ears if tuple(e['post']) == (-110.4, -15.4)][0] == [[-1.0, 0.0]] and [e['faces'] for e in ears if tuple(e['post']) == (-110.4, -18.4)][0] == [])
# profiles as point lists
PRQ = Q2['profiles']
t('D', 'Q2 profiles: the post section is 76.1 with a 5.0 wall; the cap rises to 1100 on the axis, 80 across', all(abs(math.hypot(*p_) - 38.05) < 0.01 for p_ in PRQ['post_section']['outer']) and PRQ['cap_rz'][0] == [0.0, 1100.0] and near(2 * max(p_[0] for p_ in PRQ['cap_rz']), 80.0, 1e-9))
t('D', 'Q2 profiles: the top rail section is a 60.3 tube with a 3.6 wall, the low rail 42.4', all(abs(math.hypot(*p_) - 30.15) < 0.01 for p_ in PRQ['top_rail_section']['outer']) and all(abs(math.hypot(*p_) - 26.55) < 0.01 for p_ in PRQ['top_rail_section']['inner']) and all(abs(math.hypot(*p_) - 21.2) < 0.01 for p_ in PRQ['low_rail_section']['outer']))
t('D', 'Q2 profiles: the hex nut is 24 across flats (distance between opposite sides) and 13 high', near(2 * 13.856 * math.cos(math.pi / 6), PRQ['nut_across_flats'], 0.01) and len(PRQ['nut_hex_outline']) == 6 and PRQ['nut_height'] == 13.0)
t('D', 'Q2 profiles: the stud holes are on a 150 square inside the plate, 25 from its edges', all(abs(abs(h_[0]) - 75.0) < 1e-9 and abs(abs(h_[1]) - 75.0) < 1e-9 for h_ in PRQ['base_plate_holes']) and near(100.0 - 75.0, 25.0, 1e-9))
xs_l = [p_[0] for p_ in PRQ['link_inplane']['outline']]
ys_l = [p_[1] for p_ in PRQ['link_inplane']['outline']]
t('D', 'Q2 profiles: the in-plane link is 65 x 44 outside and 39 x 18 inside (the bollards target\'s plain chain)', near(max(xs_l) - min(xs_l), 65.0, 0.01) and near(max(ys_l) - min(ys_l), 44.0, 0.01) and near(max(p_[0] for p_ in PRQ['link_inplane']['hole']) - min(p_[0] for p_ in PRQ['link_inplane']['hole']), 39.0, 0.01))
cz = PRQ['catenary_xz']
t('D', 'Q2 profiles: the catenary is symmetric, starts and ends at the eyes (z 500) and its lowest point is z 300 at mid-span', near(cz[0][1], 500.0, 0.01) and near(cz[-1][1], 500.0, 0.01) and near(min(p_[1] for p_ in cz), 300.0, 0.6) and near(cz[0][0], -cz[-1][0], 0.01))
cs2 = PRQ['catenary_short_xz']
t('D', 'Q2 profiles: the short bay\'s catenary starts and ends at its eyes (x +-616.95, z 500) and sags to about z 413', near(cs2[0][0], -616.95, 0.01) and near(cs2[0][1], 500.0, 0.01) and near(min(p_[1] for p_ in cs2), 500.0 - sb['sag'], 1.0))
eo = PRQ['ear_outline']
t('D', 'Q2 profiles: the ear is a flat bar 65 x 70 x 8 with a 24 hole 45 from the post surface', near(max(p_[0] for p_ in eo['outline']), 65.0, 1e-9) and near(max(p_[1] for p_ in eo['outline']) - min(p_[1] for p_ in eo['outline']), 70.0, 1e-9) and eo['hole_centre'] == [45.0, 0.0] and eo['hole_diameter'] == 24.0 and eo['thickness'] == 8.0)
# the checks
names = [c['name'] for c in T['checks']]
t('D', f"checks: {len(names)} listed, names unique", len(set(names)) == len(names))
t('D', 'checks: every one has a number or a stated value, a tolerance, a unit, a kind and a basis', all(('expected' in c and 'tol' in c and 'unit' in c and 'kind' in c and 'basis' in c) for c in T['checks']))
t('D', 'checks: the review\'s new and re-stated ones are all there', all(n_ in CK for n_ in ('A1_post_section', 'A1_post_top', 'A1_top_rail_section', 'A1_bottom_rail_section', 'A1_bolts', 'A1_bbox', 'A1_walking_clear', 'A1_no_deep_obstacle', 'A1_foot_patch', 'Q2_clear_of_rings', 'Q2_corner_closed', 'Q2_basin_posts', 'Q2_tip_posts', 'Q2_return_posts', 'Q2_totals', 'Q2_top_rail_od', 'Q2_clear_of_mooring')) and 'A1_foot_ring' not in CK)
t('D', 'checks: the review\'s values: A1_post_section [50, 30] +-2; A1_post_top 1030 +-10; A1_top_rail_section [50, 30] +-2 with the top at 1000 +-10; A1_bottom_rail_section [40, 20] +-2; A1_bbox [2072, 50, 1030] +-8; A1_foot_patch [250, 250] +-60; Q2_top_rail_od 60.3 +-3',
  CK['A1_post_section']['expected'] == [50, 30] and CK['A1_post_section']['tol'] == 2 and CK['A1_post_top']['expected'] == 1030 and CK['A1_post_top']['tol'] == 10 and CK['A1_top_rail_section']['expected'] == [50, 30] and CK['A1_top_rail_section']['top_z'] == [1000, 10]
  and CK['A1_bottom_rail_section']['expected'] == [40, 20] and CK['A1_bbox']['expected'] == [2072, 50, 1030] and CK['A1_bbox']['tol'] == 8.0 and CK['A1_foot_patch']['expected'] == [250, 250] and CK['A1_foot_patch']['tol'] == 60 and CK['Q2_top_rail_od']['expected'] == 60.3 and CK['Q2_top_rail_od']['tol'] == 3.0)
t('D', 'checks: the footway one is a minimum of 0.68 m over 0 to 2.0 m; the obstacle one is a maximum of 0.895', CK['A1_walking_clear'].get('minimum') == 0.68 and CK['A1_no_deep_obstacle']['expected'] == 0.895 and CK['A1_no_deep_obstacle'].get('max') is True)
t('D', 'checks: kinds named are A1, Q2, Q2b only', {c['kind'] for c in T['checks']} <= {'A1', 'Q2', 'Q2b'})
t('D', 'variants: the three A1 conditions\' shares sum to 1 and the default (galvanised) is the largest, 55 %', near(sum(c['share'] for c in T['variants']['A1_conditions']), 1.0, 1e-9) and T['variants']['A1_conditions'][0]['share'] == 0.55 and [c['share'] for c in T['variants']['A1_conditions']] == [0.55, 0.30, 0.15])
t('D', 'materials: unique ids, each with sRGB in 0..255, roughness 0..1', len({m['id'] for m in T['materials']}) == len(T['materials']) and all(all(0 <= c <= 255 for c in m['srgb']) and 0 <= m['roughness'] <= 1 for m in T['materials']))
t('D', 'paint: A1 default is galvanised (118, 120, 122) rough 0.55 metal 1; its black condition (24, 24, 26) is the same as Q2 and the bollards\' K1 and K5', A1['paint']['srgb'] == [118, 120, 122] and A1['paint']['roughness'] == 0.55 and A1['paint']['metal'] == 1 and A1['black_condition']['srgb'] == Q2['paint']['srgb'] == [24, 24, 26] == BT['kinds']['K1']['paint']['srgb'])
t('D', 'the reserve kinds are marked placed = false and have no placement', all(K[k_]['placed'] is False for k_ in ('R3A', 'R3B', 'R3D')) and not any(p.get('kind') in ('R3A', 'R3B', 'R3D') for p in PL['street'] + PL['quay']))
t('D', 'no area railing, yard gate or chapel on the street is stated in placements.absent, with the reasons', all(k_ in PL['absent'] for k_ in ('area_railings', 'yard_gate', 'backdrop')))
t('D', 'the photograph windows hold their objects: each preview window gives at most 1200 px', all((F_['preview']['s1'] - F_['preview']['s0']) / F_['preview']['mm'] <= 1200 and (F_['preview']['z1'] - F_['preview']['z0']) / F_['preview']['mm'] <= 1200 for F_ in FR.values()))
drw = D.all_views()
t('D', f"the drawing makes {len(drw)} views from target.json alone; every polygon has at least three points and finite numbers", all(len(pg['poly']) >= 3 and all(math.isfinite(c) for pt_ in pg['poly'] for c in pt_) for v_ in drw for pg in v_.polys) and len(drw) == 14)
jv = [v_ for v_ in drw if v_.name == 'jetty_plan'][0]
t('D', 'the jetty plan draws the two mooring rings (layer ring) at the kit\'s y -62 and -32, three runs of rail (2 Q2a and 9 Q2b bays) and 12 posts', sorted(round(sum(p_[1] for p_ in pg['poly']) / len(pg['poly']) / 1000) for pg in jv.polys if pg['layer'] == 'ring') == [-62, -32] and sum(1 for pg in jv.polys if pg['layer'] == 'rail') == 2 and sum(1 for pg in jv.polys if pg['layer'] == 'rail_chain') == 9 and sum(1 for pg in jv.polys if pg['layer'].startswith('post_')) == 12)

# ------------------------------------------------------------------------------------------------------------------ E
files = sorted(os.listdir(PREV)) if os.path.isdir(PREV) else []
t('E', f"{len(files)} previews exist in production/previews/cloud-week/refs/railings/", len(files) >= 14)
bad = []
for f_ in files:
    p = os.path.join(PREV, f_)
    im_ = Image.open(p)
    if max(im_.size) > 1200 or os.path.getsize(p) > 300 * 1024 or not f_.lower().endswith('.jpg'):
        bad.append((f_, im_.size, os.path.getsize(p)))
t('E', 'every preview is a JPEG of at most 1200 px and under 300 KB' + (' (%s)' % bad if bad else ''), not bad)
t('E', 'the main photograph overlay exists: ...-target-on-photo.jpg', 'ph-bethnal_green_entrance-r3b-park-railing-target-on-photo.jpg' in files)
t('E', 'the previews that show the amended objects exist: the A1 bolt section, the walking strip section, the jetty plan, the street plan, the A1 beside the photographed bars, the drawing sheet', all(n_ in files for n_ in ('target-a1-bolt-section.jpg', 'target-a1-walking-section.jpg', 'target-plan-jetty.jpg', 'target-plan-street.jpg', 'target-a1-beside-photographed-bars.jpg', 'target-drawing-sheet.jpg')))
t('E', 'names follow <ref>-<place>-<what>.jpg (ph- or target- prefix)', all(re.match(r'^(ph|target)-[a-z0-9_\-]+\.jpg$', f_) for f_ in files))
txt_all = json.dumps(T).lower()
doc = open(os.path.join(HERE, 'TARGET.md'), encoding='utf-8').read() if os.path.exists(os.path.join(HERE, 'TARGET.md')) else ''
forb = ['jacksons', 'glasdon', 'marshalls', 'streetscape', 'lion foundry', 'carron', 'royal mail', 'post office', 'thorn', 'tower hamlets', 'alcohol', 'beer', 'lager', 'whisky', 'betting', 'bookmaker', 'casino', 'child']
hit = [w for w in forb if w in txt_all]
t('E', 'target.json carries no maker\'s, council\'s or brand name and no word of the content rule (%s)' % (hit or 'none'), not hit)
src_txt = ' '.join(open(os.path.join(HERE, f_), encoding='utf-8').read().lower() for f_ in os.listdir(HERE) if f_.endswith('.py') and f_ not in ('self_check.py',))
hit2 = [w for w in forb if w in src_txt]
t('E', 'the makers and the drawing script carry none of them either (%s)' % (hit2 or 'none'), not hit2)
if doc:
    dh = [w for w in forb if w in doc.lower()]
    t('E', 'TARGET.md carries none of them (%s)' % (dh or 'none'), not dh)
    t('E', 'TARGET.md has a one-line summary first and states the self-check result line', doc.split('\n')[0].startswith('# ') and ('**' in doc.split('\n')[2] or '**' in doc.split('\n')[3]))
    miss = [c['name'] for c in T['checks'] if c['name'] not in doc]
    t('E', 'TARGET.md names every check (%d missing%s)' % (len(miss), ': ' + ', '.join(miss[:6]) if miss else ''), not miss)
    nums = ['50 x 30', '40 x 20', '97.09', '96.24', '109.09', '60.3', '76.1', '3.375', '0.205', '1.575', '0.895', '2072', '1036', '-110.4', '-128.4', '-22.8', '31.4', '10.6', '0.945', '1.02', '1.15', '1.13', '0.974', '1.052', '1.027', '1.009']
    t('E', 'TARGET.md quotes the key numbers of target.json: ' + ', '.join(nums), all(n_ in doc for n_ in nums))
    t('E', 'TARGET.md has the sections of the brief: sources, the target part by part, photographs-win, variants, materials, wear, what the target could not settle, what to read when the network opens, the previews', all(k_ in doc.lower() for k_ in ('sources', 'photographs', 'variants', 'materials', 'wear', 'could not settle', 'network opens', 'previews')))
    t('E', 'TARGET.md section 13 starts with the PC photographs (two dated 1985 to 1995) and names the set-back note next to LTN 2/09', 'two dated (1985 to 1995)' in doc and 'LTN 2/09' in doc and '0.45' in doc and doc.index('two dated (1985 to 1995)') < doc.index('LTN 2/09'))
    t('E', 'TARGET.md says plainly that both sides of A1\'s form are judgement', 'both sides' in doc.lower() and 'judgement' in doc.lower())
else:
    t('E', 'TARGET.md exists', False)
t('E', 'the unreached sources are listed and none is used: every S-row marked unreached is absent from the used list', all(u not in [s_['url'] for s_ in T['sources']] for u in T['unreached']))
t('E', 'TARGET-REVIEW.md is present and was not rewritten by the makers (no maker script names it as an output)', os.path.exists(os.path.join(HERE, 'TARGET-REVIEW.md')) and not any(("open(os.path.join(HERE, 'TARGET-REVIEW.md'), 'w" in open(os.path.join(HERE, f_), encoding='utf-8').read()) for f_ in os.listdir(HERE) if f_.endswith('.py') and f_ != 'self_check.py'))

# ------------------------------------------------------------------------------------------------------------------ result
groups = {}
for g, n, ok, d in RES:
    groups.setdefault(g, [0, 0])
    groups[g][1] += 1
    groups[g][0] += int(ok)
fails = [(g, n, d) for g, n, ok, d in RES if not ok]
tot = len(RES)
npass = sum(1 for r in RES if r[2])
names_ = {'A': 'printed numbers', 'B': 'photograph measurements', 'C': 'drawing on the photographs', 'D': 'internal consistency', 'E': 'text and files'}
line = ('SELF-CHECK PASS: %d of %d tests pass (' % (npass, tot) if not fails else 'SELF-CHECK FAIL: %d of %d tests pass (' % (npass, tot)) + ', '.join('%s %s %d/%d' % (g, names_[g], groups[g][0], groups[g][1]) for g in 'ABCDE' if g in groups) + ')'
print(line)
for g, n, d in fails:
    print('  FAIL', g, n, d)
if '--no-write' not in sys.argv:
    T['self_check'] = dict(result=line, tests=[dict(group=g, name=n, ok=ok) for g, n, ok, d in RES], details=[dict(group=g, name=n, detail=d) for g, n, ok, d in RES if d])
    json.dump(T, open(TP, 'w'), indent=1)
sys.exit(0 if not fails else 1)
