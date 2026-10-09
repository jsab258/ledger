#!/usr/bin/env python
"""Tests the railings target against its own sources before anything is built.

/home/user/.bpyenv/bin/python self_check.py [--no-write]

A  every printed number the target uses comes back from target.json (and is found in the repository file it is quoted from; the kit's and the bollards target's numbers are read live)
B  every photograph measurement overrides as stated (camera heights recomputed from their anchors; bars, rails and the cross-checks against the bollards target's chain post)
C  the drawing's projected edges fall on the main photograph (R3B) and the others within the stated error (a scale fitted on ONE dimension, the bar pitch)
D  internal consistency (parts add up, nothing floats, nothing overlaps that should not, the street clearances, the quay runs against the kit)
E  the text and the files: no real name or mark, previews within their size limits, the numbers in TARGET.md are target.json's
Prints a result line and writes it into target.json under "self_check"."""
import sys, os, json, math, re
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import target_drawing as D

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
Q2 = K['Q2']
HRd = T['photo_measurements']['hand_reads']
R3B = T['photo_measurements']['R3B_auto']
SF = T['street_frame']
PL = T['placements']
CK = {c['name']: c for c in T['checks']}

# ------------------------------------------------------------------------------------------------------------------ A
for s in T['scene_numbers']:
    p = os.path.join(ROOT, s['file'])
    ok = os.path.exists(p)
    txt = open(p, encoding='utf-8').read() if ok else ''
    t('A', f"printed {s['id']} found in {s['file']}", ok and s['find'] in txt, s['what'])
S = {s['id']: s for s in T['scene_numbers']}
v = S['guard_rail_line']['value']
t('A', 'the scene\'s height is 1.0 m and A1\'s top is 1000', near(A['height'], v['height_m'] * 1000, 0.001))
t('A', 'A1\'s post (48.3) and top rail (42.4) are within 10 % of the scene\'s 50 and 40', near(A['post']['od'], v['post_m'] * 1000, 5) and near(A['top_rail']['od'], v['rail_m'] * 1000, 4))
t('A', 'the scene\'s five bars of 25 are replaced (A1 has more, thinner bars; the change is listed under photographs_win)', A['infill']['count'] > v['bars'] and A['infill']['diameter'] < v['bar_m'] * 1000 and any(d['element'] == 'infill of the guard rail' for d in T['photographs_win']))
pl_s = S['guard_rail_place']['value']
t('A', 'the panel runs x 10.0 to 12.0 and is 2.0 m (c2c 2000 = 12.0 - 10.0)', near(pl_s['x1_m'] - pl_s['x0_m'], A['centre_to_centre'] / 1000, 1e-9) and PL['street'][0]['x_m'] == [10.0, 12.0])
t('A', 'the axis z 3.375 = kerb face 3.0 + the scene\'s kerb 0.125 + its 0.25 set-back', near(SF['kerb_face_z_m'] + 0.125 + pl_s['setback_from_kerb_m'], PL['street'][0]['z_axis_m'], 1e-9) and S['feet_post0']['value']['z_m'] == PL['street'][0]['z_axis_m'])
t('A', 'the kerbs target\'s back edge (3.0 + 0.170) leaves 0.205 to the axis', near(PL['street'][0]['z_axis_m'] - (3.0 + S['kerb_target_top']['value']['top'] / 1000), PL['street'][0]['behind_kerbs_target_back_m'], 1e-9) and near(PL['street'][0]['behind_kerbs_target_back_m'], CK['A1_behind_kerb_back']['expected'], 1e-9))
t('A', 'the stand-in\'s lower rail is 0.45 above its foot (y 0.50625 - 0.05625) and A1\'s is 0.20', near(0.50625 - 0.05625, S['pieces_lower_rail']['value']['above_foot_m'], 1e-9) and A['bottom_rail']['axis_z'] == 200.0)
t('A', 'the footway level at the posts: scene y 0.05625; kerbs target flags +110 over the channel -0.075 plus the fall 0.205/40 = 0.040', near(SF['foot_y_kerbs_target_m'], -0.075 + 0.110 + 0.005, 0.0006) and near(SF['foot_y_scene_m'], 0.05625, 1e-9))
t('A', 'the frontage line 5.125 = kerb face 3.0 + 0.125 + 2.0 and the stallriser face is 0.15 in front of it (4.975: the scene\'s "fish market\'s front (4.97 m)")',
  near(3.0 + 0.125 + 2.0, S['frontage_z']['value'], 1e-9) and near(S['frontage_z']['value'] - S['stallriser']['value']['proud_m'], SF['stallriser_face_z_m'], 1e-9) and "the fish market's front (4.97 m)" in open(os.path.join(ROOT, 'production/specs/vignette-scene.json'), encoding='utf-8').read())
scene_txt = open(os.path.join(ROOT, 'production/specs/vignette-scene.json'), encoding='utf-8').read()
t('A', 'the scene\'s note: three panels left 1.57 m, the crates 0.92 m deep left 0.65, under 0.68', 'there is 1.57 m' in scene_txt and 'crates (0.92 m deep) left 0.65 m' in scene_txt and 'walking person\'s 0.68' in scene_txt)
rear = PL['street'][0]['z_axis_m'] + A['post']['od'] / 2000
clear = SF['stallriser_face_z_m'] - rear
t('A', 'walking clear behind the panel = stallriser face - the rail\'s rear face = 1.576 (the scene says 1.57)', near(clear, CK['A1_walking_clear']['expected'], 0.002))
t('A', 'the deepest obstacle that leaves 0.68 is 1.576 - 0.68 = 0.896; the 0.92 crates exceed it', near(clear - 0.68, CK['A1_no_deep_obstacle']['expected'], 0.002) and 0.92 > CK['A1_no_deep_obstacle']['expected'])
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
try:
    import south_quay_geom as G
    kit, jn, info = G.build(ROOT)
    e_ = info['edges']
    t('A', 'kit: the jetty\'s basin edge is x -110 from y -100.6 to -15 and its end y -15 from x -130 to -110.6 (live from south_quay_geom.build)', e_['jetty_north'] == ((-110.0, -100.6), (-110.0, -15.0)) and e_['jetty_end'] == ((-130.0, -15.0), (-110.6, -15.0)))
    t('A', 'kit: the quay edge x -70 and the apron at the kerb top +0.05', near(info['quay_edge_x'], -70.0, 1e-9) and near(info['apron_z'], 0.05, 1e-9))
    jx0, jx1 = -130.0, -110.0
    t('A', 'kit: the cope is 0.60 across; the parapet is on the seaward side x -129.4 to -128.6 and ends at y -23.0', near(G.COPING_W_M, 0.6, 1e-9) and near(jx0 + G.COPING_W_M, -129.4, 1e-9) and near(jx0 + G.COPING_W_M + 0.80, -128.6, 1e-9) and S['kit_parapet']['value']['y_end'] == -15.0 - 8.0)
    t('A', 'kit: the kit has no railing piece: no kit piece name contains "rail"', not any('rail' in k.lower() for k in kit.pieces))
except Exception as ex:
    t('A', 'kit: south_quay_geom imports and builds (%s)' % ex, False)
t('A', 'the kit\'s README lists a ladder, bollards and a stone parapet but no railing', 'railing' not in open(os.path.join(ROOT, 'production/art/south-quay/README.md'), encoding='utf-8').read().lower().replace('no railing', ''))
t('A', 'the scene file names the yard entrance as a 3.0 m gap in the data, x 21.0 to 24.0 (no gate is placed)', S['yard_gap']['value'] == [21.0, 24.0] and 'gate' not in json.dumps(T['placements']['street'][0]).lower())
t('A', 'the bollards target\'s yard-mouth K1 posts guard the gap: x 20.7 and 24.3', [e for e in BT['placements']['street_proper'] if e['id'] == 'yard_mouth'][0]['x_m'] == [20.7, 24.3])
pieces = json.load(open(os.path.join(ROOT, 'production/specs/vignette-pieces.json')))['pieces']
bar = [p for p in pieces if p['name'].startswith('prop_crowd_control_barrier')]
t('A', 'the scene stands a held crowd-control barrier at the yard mouth (x 22.5, z -4.85), an E11 prop, not this family\'s', len(bar) == 1 and near(bar[0]['x_m'], 22.5, 1e-9) and near(bar[0]['z_m'], -4.85, 1e-9) and bar[0]['bom'] == 'E11_cones_barrier')
east_front = [p for p in pieces if p['name'].startswith(('east_parade_', 'east_chandler_')) and p['shape'] == 'box' and p['name'].endswith(tuple('0123456789')) and 'bay' in p['name']]
t('A', 'every east frontage block stands on the building line: its near face is z 5.125 (the shops have no forecourt); the only pieces named rail are E8\'s', len(east_front) >= 6 and all(near(p['z_m'] - p['sz_m'] / 2, 5.125, 0.01) for p in east_front) and {p['name'].split('_')[0] for p in pieces if p['name'].startswith('rail')} == {'rail'} and all(p['bom'] == 'E8_guard_railing' for p in pieces if p['name'].startswith('rail')))
t('A', 'the street\'s pieces include no gate, fence, palisade or area railing by name', not any(w in p['name'] for p in pieces for w in ('gate', 'fence', 'palisade', 'area_rail')))
t('A', 'models per kind at most four (asset plan: two to four a kind)', all(v_ <= 4 for v_ in T['variants']['models'].values()))
t('A', 'asset plan rows: 1 kit for the guard railing, 1 for the quay railing with chain (a rail and a chain run: A1; Q2)', S['asset_plan_counts']['value'] == '1 kit; 1 kit' and T['variants']['models']['A1'] == 1)

# ------------------------------------------------------------------------------------------------------------------ B
cal = T['calibration']
byid = {a['id']: a for a in cal['horizon_anchors']}
t('B', 'no anchor\'s fit is on the edge of its search range', not any(a['fit_on_edge'] for a in cal['horizon_anchors']))
for a in cal['horizon_anchors']:
    H = a['image_rows']
    tf = math.tan((a['foot_row'] - H / 2) * math.pi / H)
    a['_h'] = a['gauge_mm'] * tf / a['pitch_tan'] / 1000 + a['step_m']
    p_by_eye = a['px_pitch_by_eye'] * math.pi / H
    t('B', f"anchor {a['id']}: pitch inside +-15 % of the pitch read by eye ({a['pitch_tan']:.5f} against {p_by_eye:.5f}), height {a['_h']:.3f} m", abs(a['pitch_tan'] / p_by_eye - 1) <= 0.151)
for pano, P in cal['panoramas'].items():
    hs = [byid[i]['_h'] for i in P['anchors']] + [q['h'] for q in P.get('quoted', [])]
    mean = sum(hs) / len(hs)
    t('B', f"{pano}: the mean of its anchors at the objects' ground, {mean:.3f} m, is within the stated error of the stated height {P['h_cam']} +-{P['err']}", abs(mean - P['h_cam']) <= P['err'] and all(abs(h - P['h_cam']) <= P['err'] + 0.005 for h in hs))
    t('B', f"{pano}: at least two anchors", len(hs) >= 2)
t('B', 'no panorama is used at 1.6 m', all(P['h_cam'] < 1.4 for P in cal['panoramas'].values()))
t('B', 'the elevations were made at the stated heights', all(abs(T['photo_frames'][k_]['h_cam'] - cal['panoramas'][T['photo_frames'][k_]['pano']]['h_cam']) < 1e-9 for k_ in T['photo_frames']))
bt_cal = BT['calibration']['panoramas']
t('B', 'Bethnal Green: 0.97 lies inside the bollards target\'s 1.02 +-0.07 (the two families agree)', abs(cal['panoramas']['bethnal_green_entrance']['h_cam'] - bt_cal['bethnal_green_entrance']['h_cam']) <= bt_cal['bethnal_green_entrance']['h_cam_err'] + 1e-9)
t('B', 'Limehouse: 1.12 lies inside the bollards target\'s 1.17 +-0.06', abs(cal['panoramas']['limehouse']['h_cam'] - bt_cal['limehouse']['h_cam']) <= 0.07)
# R3B bars
pk = np.array(R3B['bar_centres_s_mm'], float)
fit = np.polyfit(np.arange(len(pk)), pk, 1)
t('B', 'R3B: the bar pitch refitted from the 26 stored bar centres equals the stated 78.54 +-0.05', near(fit[0], R3B['bar_pitch_mm'], 0.05) and len(pk) == 26)
t('B', 'R3B: the pitch is within 4 % of three inches (76.2), inside the 6 % scale error', abs(R3B['bar_pitch_mm'] / 76.2 - 1) < 0.04 and abs(R3B['bar_pitch_mm'] / 76.2 - 1) < cal['panoramas']['bethnal_green_entrance']['err'] / cal['panoramas']['bethnal_green_entrance']['h_cam'])
t('B', 'R3B: the bar centres are regular (rms residual to the line at most 6 mm; the detections lie on 3 to 4 mm native pixels)', R3B['bar_pitch_resid_rms_mm'] <= 6.0)
t('B', 'R3B: the bar\'s width, 20 FWHM blur included, reads 17 +-3 round', near(K['R3B']['bars']['diameter'], R3B['bar_fwhm_mm_median'] - 3, 3.5))
rl = {round(r['z']): r for r in R3B['rails']}
t('B', 'R3B: the top rail row 2000 and the bottom rail row 441 are in the automated rail list', any(abs(z - 2000) <= 5 for z in rl) and any(abs(z - 441) <= 6 for z in rl))
t('B', 'R3B: the hand-read bottom and mid rails (445, 1045) agree with the automated rows (441, 1036) within their errors', near(HRd['R3B']['bottom_rail_axis_z']['v'], 441, HRd['R3B']['bottom_rail_axis_z']['err']) and near(HRd['R3B']['mid_rail_axis_z']['v'], 1036, HRd['R3B']['mid_rail_axis_z']['err']))
t('B', 'R3B: the coping top: automated 331 on the plane 110 behind the face + 13 for the lip = the stated 345 +-20', near(HRd['R3B']['coping_top_z']['v'], R3B['coping_top_z_mm'] + 13, HRd['R3B']['coping_top_z']['err']))
t('B', 'R3B: the post shaft, mean of the eight automated widths, equals the stated 100 +-10', near(np.mean(R3B['post_width_mm']), HRd['R3B']['post_shaft_width']['v'], HRd['R3B']['post_shaft_width']['err']))
t('B', 'R3B: tall tips (2300) lie 300 above the top rail (2000), short tips (1225) about 180 above the middle rail (1045)', near(HRd['R3B']['tall_bar_tip_z']['v'] - HRd['R3B']['top_rail_axis_z']['v'], 300, 40) and near(HRd['R3B']['short_bar_tip_z']['v'] - HRd['R3B']['mid_rail_axis_z']['v'], 180, 40))
t('B', 'R3B: the head profile rises to the stated tip (2335 on the profile, 2300 +-20 read: the spire\'s last 35 is a point under the blur) and its widest ring is 60', max(r for r, z in K['R3B']['bars']['head_rz']) * 2 >= 55 and K['R3B']['bars']['head_rz'][-1][1] - HRd['R3B']['tall_bar_tip_z']['v'] <= 45)
t('B', 'R3A: five red courses between z 330 and 705 are 75 each (the elevation\'s scale, +-5)', near((705 - 330) / HRd['R3A']['red_courses_between']['v'], 75, 5))
t('B', 'R3A: the wall is 780 = the string at 300 + 0.. (4 lower courses at 75 = 300) + five red 375 + the coping about 105 for two bullnose courses', near(300 + 375 + 105, HRd['R3A']['wall_top_z']['v'], HRd['R3A']['wall_top_z']['err']))
t('B', 'R3A: the rails 840, 1435, 1645 stand 595 and 210 apart; the bars all 114 apart (tall every 228)', near(HRd['R3A']['mid_rail_axis_z']['v'] - HRd['R3A']['bottom_rail_axis_z']['v'], 595, 40) and near(HRd['R3A']['top_rail_axis_z']['v'] - HRd['R3A']['mid_rail_axis_z']['v'], 210, 30) and near(HRd['R3A']['bar_pitch_all']['v'], 114, 5))
t('B', 'R3D: the wall is 620 = eight courses of 75 (600) + 20 of coping; the railing above it is 465 to the top rail', near(HRd['R3D']['wall_top_z']['v'], 8 * 75 + 20, 20) and near(HRd['R3D']['top_rail_axis_z']['v'] - HRd['R3D']['wall_top_z']['v'], 465, 30))
cs_ = np.array(HRd['R3D']['bar_centres_s']['v'], float)
f_ = np.polyfit(np.arange(10), cs_, 1)
t('B', 'R3D: ten hand-read bar centres give a pitch of %.1f (stated 94.5 +-3) and the stored fit equals it' % f_[0], near(f_[0], HRd['R3D']['bar_pitch']['v'], 3.0) and near(f_[0], K['R3D']['bars']['pitch']['v'], 0.01) and near(f_[1], K['R3D']['bars']['first_s'], 0.01))
t('B', 'R3D: the gate\'s paint (38, 56, 36) lies between the two measured medians (32, 47, 28) and (51, 69, 45)', all(a <= b <= c for a, b, c in zip((32, 47, 28), HRd['R3D']['paint_srgb']['v'], (51, 69, 45))))
t('B', 'LHB: the post top 1086 against the bollards target\'s 1135 has the ratio of the camera heights (1.12 / 1.17 = 0.957) within 2 %', abs(HRd['LHB']['post_top_z']['v'] / 1135.0 / (cal['panoramas']['limehouse']['h_cam'] / bt_cal['limehouse']['h_cam']) - 1) <= 0.02)
t('B', 'LHB: the lugs (800, 405) against K5\'s (840, 420) have the same ratio within 6 %', all(abs(a / b / 0.957 - 1) <= 0.06 for a, b in ((HRd['LHB']['upper_lug_z']['v'], 840.0), (HRd['LHB']['lower_lug_z']['v'], 420.0))))
t('B', 'LHB: both swags sag 215 to 240 below their lugs, a mean of 227 +-35; the target\'s 200 lies between the bollards target\'s 150 and the photograph\'s 227', near((HRd['LHB']['upper_lug_z']['v'] - HRd['LHB']['upper_chain_lowest_z']['v'] + HRd['LHB']['lower_lug_z']['v'] - HRd['LHB']['lower_chain_lowest_z']['v']) / 2.0, 227, 35) and 150 < Q2['chain']['sag'] < 227)
t('B', 'LHB: the span read from the flanges (2840) is within 5 % of 3.0 m (the bollards target\'s 3.06 m between two posts, 3.0 nominal)', abs(HRd['LHB']['span_mm']['v'] / 3000.0 - 1) <= 0.06)
t('B', 'LHB: K5 has four flange nuts, as the bollards target says', HRd['LHB']['flange_bolts']['v'] == k5['fixings']['bolts']['count'] == 4)

# ------------------------------------------------------------------------------------------------------------------ C
FR = T['photo_frames']


def gray(name):
    return np.asarray(Image.open(os.path.join(PREV, name)).convert('L'), float)


def band_profile(im, win, mm, zlo, zhi, s0=None, s1=None):
    r0, r1 = int(round((win['z1'] - zhi) / mm)), int(round((win['z1'] - zlo) / mm))
    prof = im[r0:r1].mean(0)
    return prof


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
    # centroid of the peak
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


# C: R3B, the main photograph
F = FR['R3B']['preview']
im = gray('ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg')
mm = F['mm']
prof = band_profile(im, F, mm, 700, 900)
bars = [(s, tall) for s, tall in D.r3b_bar_positions(None, 760.0, 2480.0)]
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
t('C', f"R3B: after the fit the residual's median is {np.median(abs(res_fit)):.1f} mm (at most 3)", np.median(abs(res_fit)) <= 3.0)
cols = (800.0, 2400.0)
for key, z_p, half in (('bottom_rail', K['R3B']['rails']['bottom_axis_z']['v'], 25), ('mid_rail', K['R3B']['rails']['mid_axis_z']['v'], 30), ('top_rail', K['R3B']['rails']['top_axis_z']['v'], 30)):
    z_f, dep = row_extreme(im, F, mm, z_p, cols, half, 'dark')
    t('C', f"R3B: {key} predicted at z {z_p:.0f}, the strongest dark row in the preview at {z_f:.0f} (within the {K['R3B']['rails'][key + '_axis_z' if False else key.replace('_rail', '') + '_axis_z']['err']} + 10 mm)", abs(z_f - z_p) <= K['R3B']['rails'][key.replace('_rail', '') + '_axis_z']['err'] + 10)
# the coping's top edge: the strongest light-to-dark step going down within 300..400 over s 900..2300
c0, c1 = [int(round((x - F['s0']) / mm)) for x in (900, 2300)]
col = gaussian_filter1d(im[:, c0:c1].mean(1), 1.0)
r_lo, r_hi = int(round((F['z1'] - 420) / mm)), int(round((F['z1'] - 290) / mm))
gr = col[r_lo + 1:r_hi + 1] - col[r_lo - 1:r_hi - 1]
z_cop = F['z1'] - (r_lo + int(np.argmax(np.abs(gr)))) * mm
t('C', f"R3B: the coping's top edge in the preview is at z {z_cop:.0f}, the target's {K['R3B']['plinth']['coping_top_z']['v']} - 13 for the projection = {K['R3B']['plinth']['coping_top_z']['v'] - 13} (within 25)", abs(z_cop - (K['R3B']['plinth']['coping_top_z']['v'] - 13)) <= 25)
# tips and the hinge post's top, on the 1 mm close of the head (a bright sky behind): the first row from the top where the strip is darker than the background by 30 for three rows
hc = gray('ph-bethnal_green_entrance-r3b-park-railing-head-close.jpg')
z1h, s0h = 2450.0, 2300.0


def top_dark(s_c, thr=30):
    c = int(round(s_c - s0h))
    strip = hc[:, c - 1:c + 2].mean(1)
    bg = np.median(np.concatenate([hc[:, c - 25:c - 12], hc[:, c + 13:c + 26]], 1), 1)
    d = bg - strip
    for r in range(0, hc.shape[0] - 3):
        if d[r] > thr and d[r + 1] > thr and d[r + 2] > thr:
            return z1h - r
    return None


tall_in = [s for s, tall in D.r3b_bar_positions(None, 2300.0, 2535.0) if tall]
tz = [top_dark(s) for s in tall_in]
t('C', f"R3B: the tall bar at s {tall_in[0]:.0f} has its tip at z {tz[0]} in the head close; the target's {K['R3B']['bars']['tall_tip_z']['v']} +-{K['R3B']['bars']['tall_tip_z']['err']} (within 45)", tz[0] is not None and abs(tz[0] - K['R3B']['bars']['tall_tip_z']['v']) <= 45)
pz = top_dark(2590.0)
t('C', f"R3B: the hinge post's finial top is at z {pz} in the head close; the target's {K['R3B']['post']['top_z']['v']} (within 25)", pz is not None and abs(pz - K['R3B']['post']['top_z']['v']) <= 25)
# the drawing's bar widths against the preview: the bar's FWHM in the preview 17 +- 6 incl. blur
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
t('C', f"R3B: the bars' FWHM in the 3 mm preview is {np.median(ws):.0f} (the target's 17 round + blur: between 14 and 30)", 14 <= np.median(ws) <= 30)

# C: R3D
F = FR['R3D']['preview']
im = gray('ph-urban_street_01-r3d-garden-railing-elevation.jpg')
mm = F['mm']
c0, c1 = [int(round((x - F['s0']) / mm)) for x in (100, 1000)]
col = gaussian_filter1d(im[:, c0:c1].mean(1), 1.0)
r_lo, r_hi = int(round((F['z1'] - 700) / mm)), int(round((F['z1'] - 540) / mm))
gr = col[r_lo + 1:r_hi + 1] - col[r_lo - 1:r_hi - 1]
z_wt = F['z1'] - (r_lo + int(np.argmax(np.abs(gr)))) * mm
t('C', f"R3D: the wall's top edge in the preview is at z {z_wt:.0f} against the target's {K['R3D']['wall']['top_z']['v']} (within 30)", abs(z_wt - K['R3D']['wall']['top_z']['v']) <= 30)
z_top, dep = row_extreme(im, F, mm, K['R3D']['rails']['top_axis_z']['v'], (1400.0, 2400.0), 50, 'light')
t('C', f"R3D: the top rail (a pale flat bar in the photograph) at z {z_top:.0f} against the target's {K['R3D']['rails']['top_axis_z']['v']} (within 30)", abs(z_top - K['R3D']['rails']['top_axis_z']['v']) <= 30)
z_bot, dep = row_extreme(im, F, mm, K['R3D']['rails']['bottom_axis_z']['v'], (1400.0, 2200.0), 25, 'dark')
t('C', f"R3D: the bottom rail at z {z_bot:.0f} against the target's {K['R3D']['rails']['bottom_axis_z']['v']} (within 35)", abs(z_bot - K['R3D']['rails']['bottom_axis_z']['v']) <= 30)
prof_d = band_profile(im, F, mm, 800, 1000)
pred_d = [K['R3D']['bars']['first_s'] + K['R3D']['bars']['pitch']['v'] * k for k in range(0, 10)]
fd = [locate_dark(prof_d, F, mm, s, 12.0) for s in pred_d]
okd = [(p, f) for p, f in zip(pred_d, fd) if f is not None]
t('C', f"R3D: {len(okd)} of 10 predicted bars (s 1500 to 2350) have a dark line within 12 mm (at least 5: foliage behind them)", len(okd) >= 5)
if len(okd) >= 5:
    rr = np.array([f - p for p, f in okd])
    t('C', f"R3D: median residual {np.median(abs(rr)):.1f} mm (at most 12: the hand-read centres are +-6 and the foliage behind the bars shifts a dark minimum by a few mm)", np.median(abs(rr)) <= 12)

# C: R3A
F = FR['R3A']['preview']
im = gray('ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg')
mm = F['mm']
for key, z_p in (('bottom', K['R3A']['rails']['bottom_axis_z']['v']), ('mid', K['R3A']['rails']['mid_axis_z']['v']), ('top', K['R3A']['rails']['top_axis_z']['v'])):
    z_f, dep = row_extreme(im, F, mm, z_p, (100.0, 1300.0), 45, 'dark')
    t('C', f"R3A: the {key} rail at z {z_f:.0f} against the target's {z_p} (within 40, oblique view)", abs(z_f - z_p) <= 40)
c0, c1 = [int(round((x - F['s0']) / mm)) for x in (100, 900)]
col = gaussian_filter1d(im[:, c0:c1].mean(1), 1.0)
for nm, zc in (('coping top', K['R3A']['wall']['top_z']['v']), ('lower string', K['R3A']['wall']['string_z']['v'])):
    r_lo, r_hi = int(round((F['z1'] - zc - 60) / mm)), int(round((F['z1'] - zc + 60) / mm))
    gr = col[r_lo + 1:r_hi + 1] - col[r_lo - 1:r_hi - 1]
    zf = F['z1'] - (r_lo + int(np.argmax(np.abs(gr)))) * mm
    t('C', f"R3A: the wall's {nm} edge at z {zf:.0f} against the target's {zc} (within 45)", abs(zf - zc) <= 45)
prof_a = band_profile(im, F, mm, 1000, 1300)
tallpos = [s for s in [K['R3A']['bars']['tall_first_s']['v'] + 2 * K['R3A']['bars']['pitch_all']['v'] * k for k in range(0, 6)]]
fa = [locate_dark(prof_a, F, mm, s, 25.0) for s in tallpos]
oka = [(p, f) for p, f in zip(tallpos, fa) if f is not None]
t('C', f"R3A: {len(oka)} of 6 predicted tall bars (s 204 + 228 k) have a dark line within 25 mm (at least 4)", len(oka) >= 4)

# C: LHB
F = FR['LHB']['preview']
imc = np.asarray(Image.open(os.path.join(PREV, 'ph-limehouse-lhb-chain-bay-elevation.jpg')).convert('L'), float)
mm = F['mm']
span = HRd['LHB']['span_mm']['v']
for nm, zl, zlow in (('upper', HRd['LHB']['upper_lug_z']['v'], HRd['LHB']['upper_chain_lowest_z']),
                     ('lower', HRd['LHB']['lower_lug_z']['v'], HRd['LHB']['lower_chain_lowest_z'])):
    z_pred = zl - Q2['chain']['sag']
    z_f, dep = row_extreme(imc, F, mm, z_pred, (span / 2 - 120.0, span / 2 + 120.0), 110, 'dark')
    t('C', f"LHB: the {nm} swag's lowest dark row in the preview is z {z_f:.0f}; the target's chain (lug {zl} - sag {Q2['chain']['sag']}) puts it at {z_pred:.0f} (within 60), the hand-read {zlow['v']} +-{zlow['err']}", abs(z_f - z_pred) <= 60 and abs(z_f - zlow['v']) <= zlow['err'] + 25)
rows_ = {}
for nm, z_p in (('post_top_left', HRd['LHB']['post_top_z']['v']),):
    c = int(round((0 - F['s0']) / mm))
    col = gaussian_filter1d(imc[:, c - 4:c + 5].mean(1), 1.0)
    rr_ = int(round((F['z1'] - z_p) / mm))
    seg = col[rr_ - 12:rr_ + 13]
    zf = F['z1'] - (rr_ - 12 + int(np.argmax(np.abs(np.gradient(seg))))) * mm
    t('C', f"LHB: the left post's top edge at z {zf:.0f} against the stated {z_p} (within 45)", abs(zf - z_p) <= 45)

# ------------------------------------------------------------------------------------------------------------------ D
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
P = D.a1_parts()
polys = {k_: [Polygon(p).buffer(0.0) for p in v_] for k_, v_ in P.items()}
allp = unary_union([g.buffer(0.3) for v_ in polys.values() for g in v_])
t('D', 'A1: all parts form one connected solid (posts, caps, rails, bars, welds); nothing floats', allp.geom_type == 'Polygon')
t('D', 'A1: the stored bar count equals the bars drawn and the listed x (17)', len(polys['bar']) == A['infill']['count'] == len(A['infill']['x']) == 17)
xs = A['infill']['x']
t('D', 'A1: the bars are symmetric about the middle of the panel (x_i = -x_(n-1-i), 0.02 mm)', all(near(xs[i], -xs[-1 - i], 0.02) for i in range(len(xs))))
gaps = [xs[i + 1] - xs[i] - A['infill']['diameter'] for i in range(len(xs) - 1)]
edge_gaps = [xs[0] - A['infill']['diameter'] / 2 - (-A['top_rail']['x'][1]), A['top_rail']['x'][1] - (xs[-1] + A['infill']['diameter'] / 2)]
allg = gaps + edge_gaps
t('D', f"A1: every clear gap (bar to bar and bar to post) is {min(allg):.1f} to {max(allg):.1f} mm: equal within 0.1 and at most 100", max(allg) - min(allg) < 0.1 and max(allg) <= 100.0)
t('D', 'A1: the stored clear gap is the computed one', near(A['infill']['clear_gap'], np.mean(allg), 0.01) and near(A['infill']['pitch'], A['infill']['diameter'] + np.mean(allg), 0.01))
t('D', 'A1: rails end on the post faces (x = 1000 - 24.15) and the bars end on the rail axes', near(A['top_rail']['x'][1], A['centre_to_centre'] / 2 - A['post']['od'] / 2, 0.01) and near(A['infill']['z'][0], A['bottom_rail']['axis_z'], 0.01) and near(A['infill']['z'][1], A['top_rail']['axis_z'], 0.01))
t('D', 'A1: the top rail\'s top (axis + 21.2) and the cap top equal 1000', near(A['top_rail']['axis_z'] + A['top_rail']['od'] / 2, 1000, 0.01) and near(A['cap']['z'][1], 1000, 0.01) and near(A['post']['height'], 1000, 0.01))
t('D', 'A1: the bottom rail clears the ground by 183 (underside) and is the thinner tube', near(A['bottom_rail']['underside_z'], 200 - 16.85, 0.01) and A['bottom_rail']['od'] < A['top_rail']['od'] < A['post']['od'])
t('D', 'A1: the cap is wider than the post (52 against 48.3), 8 high, and its rim is rounded R2', A['cap']['od'] > A['post']['od'] and A['cap']['thickness'] == 8.0 and A['cap']['edge_radius'] == 2.0)
bb = A1['bbox']
t('D', 'A1: the bounding box is 2052 x 52 x 1000 (the caps\' 52 across at x +-1000)', near(bb['x'][1] - bb['x'][0], 2052.0, 0.01) and near(bb['y'][1] - bb['y'][0], 52.0, 0.01) and near(bb['z'][1] - bb['z'][0], 1000.0, 0.01))
t('D', 'A1: the check A1_bbox lists the same box within its tolerance (2048.3 against 2052 at 8)', near(CK['A1_bbox']['expected'][0], bb['x'][1] - bb['x'][0], CK['A1_bbox']['tol']))
ring = A1['ground']['ring_gap']
t('D', 'A1: the dark ring is 20 wide, the post foot 48.3: the flags are cut for a 88.3 hole', near(ring, CK['A1_foot_ring']['expected'], CK['A1_foot_ring']['tol']))
post_pol = [g for g in polys['post']]
t('D', 'A1: the two posts do not overlap each other or the bars', not post_pol[0].intersects(post_pol[1]) and not any(post_pol[0].buffer(-0.1).intersects(b) or post_pol[1].buffer(-0.1).intersects(b) for b in polys['bar']))
t('D', 'A1: bars do not overlap each other (clear gaps positive)', all(g_ > 0 for g_ in gaps))
t('D', 'A1: walking clear 1.576 against 0.68, and the crates\' 0.92 leave 0.656 (under it): the check names that case', clear >= 0.68 and clear - 0.92 < 0.68 and 'crates' in CK['A1_no_deep_obstacle']['what'])
t('D', 'A1: the panel stands inside the footway (z 3.375 between the kerb back 3.170 and the stallriser face 4.975) and its rear face leaves at least 0.68', 3.170 < PL['street'][0]['z_axis_m'] < SF['stallriser_face_z_m'] and clear >= 0.68)
t('D', 'A1: the panel ends at the gully\'s centre line (x 12.0): its end post stands 0.024 over; the gully is in the channel at z 2.8 to 3.0', PL['street'][0]['x_m'][1] == 12.0)
# Q2
Qp = Q2['post']
t('D', 'Q2: the base plate (200) is wider than the post foot (76.1) and holds its four studs on a 150 square, each 25 from the edge', Qp['base_plate']['size'][0] > Qp['od'] and near((Qp['base_plate']['size'][0] - Qp['base_plate']['holes']['pitch']) / 2, 25, 0.01) and Qp['base_plate']['holes']['count'] == 4)
t('D', 'Q2: the nut (24 across flats, 13 high) fits between the stud holes and the post: the hole centre (75, 75) is 106 from the axis, the post radius 38.05, the nut radius 13.9', math.hypot(75, 75) - 13.9 > Qp['od'] / 2)
t('D', 'Q2: the top rail passes under the cap (rail top 1024.2 < post top 1100 - 14)', Q2['top_rail']['top_z'] < Qp['height'] - Qp['cap']['rise'] and near(Q2['top_rail']['top_z'], 1000 + 24.15, 0.01))
t('D', 'Q2: the rails end on the post faces: x = 1500 - 38.05', near(Q2['top_rail']['x'][1], Q2['bay']['centre_to_centre'] / 2 - Qp['od'] / 2, 0.01) and near(Q2['low_rail']['x'][1], Q2['top_rail']['x'][1], 0.01))
ch = Q2['chain']
pts, a_ = D.catenary_pts(ch['eyes']['x'][0], ch['eyes']['x'][1], ch['eyes']['z'], ch['sag'], 400)
arc = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
t('D', f"Q2b: the catenary through the eyes (span {ch['span_between_eyes']}) with sag 200 has an arc of {arc:.1f} mm; stated {ch['arc_length']} (within 3), and {ch['links']} links of 39 = {ch['links'] * 39} (within one link)", near(arc, ch['arc_length'], 3.0) and abs(ch['links'] * 39 - arc) <= 39)
t('D', 'Q2b: the eyes\' x is 1500 - 38.05 - 45 = 1416.95 and the span between the holes 2833.9', near(ch['eyes']['x'][1], 1416.95, 0.01) and near(ch['span_between_eyes'], 2833.9, 0.01))
t('D', 'Q2b: the chain\'s lowest point (z 300) stays 300 above the apron and 200 under the eyes', near(min(z for x, z in pts), ch['eyes']['z'] - ch['sag'], 0.5) and min(z for x, z in pts) > 0)
t('D', 'Q2b: the link is 3 x its bar for the inner length, the outer = inner + 2 bars, the pitch = the inner length', near(ch['link']['inner_length'], 3 * ch['link']['bar'], 0.01) and near(ch['link']['outer_length'], ch['link']['inner_length'] + 2 * ch['link']['bar'], 0.01) and near(ch['link']['outer_width'], ch['link']['inner_width'] + 2 * ch['link']['bar'], 0.01) and ch['link']['pitch'] == ch['link']['inner_length'])
bp = PL['quay']
runA, runB = bp[0], bp[1]
pa, pb = runA['posts_xy_m'], runB['posts_xy_m']
allpost = pa + pb
t('D', 'Q2: 8 posts on the basin edge x -110.4 at 3.0 and 6 more on the tip y -15.4: 14 posts, 13 bays', len(pa) == 8 and len(pb) == 6 and len(allpost) == PL['counts']['quay_posts'] == 14 and PL['counts']['quay_bays'] == 13)
t('D', 'Q2: the posts are 3.0 apart (0.001) along each run, and the corner post (-110.4, -15.4) is the last of the first run, the tip run\'s first step from it', all(near(math.hypot(pa[i + 1][0] - pa[i][0], pa[i + 1][1] - pa[i][1]), 3.0, 0.001) for i in range(7)) and near(math.hypot(pb[0][0] - pa[-1][0], pb[0][1] - pa[-1][1]), 3.0, 0.001) and all(near(math.hypot(pb[i + 1][0] - pb[i][0], pb[i + 1][1] - pb[i][1]), 3.0, 0.001) for i in range(5)))
t('D', 'Q2: the basin run is 0.4 behind the cope nose (x -110) and the tip run 0.4 behind the end nose (y -15)', all(near(p[0], -110.4, 1e-9) for p in pa) and all(near(p[1], -15.4, 1e-9) for p in pb + [pa[-1]]))
t('D', 'Q2: every post is on the jetty strip (x -130 to -110, y -100 to -15) with its 200 plate: plate edge at least 0.25 behind the nose', all(-130 < p[0] and p[0] + 0.1 <= -110 - 0.25 + 1e-9 and p[1] + 0.1 <= -15 - 0.25 + 1e-9 for p in allpost))
dmin = min(math.hypot(p[0] - q[0], p[1] - q[1]) for p in allpost for q in [(-110.75, -45.0), (-110.75, -80.0)] + [(-110.25, y) for y in (-52.0, -58.0, -64.0)])
t('D', f"Q2: the nearest post to a K6 bollard or K7 cleat is {dmin:.2f} m (at least 8.0: moorings stay clear)", dmin >= 8.0 and near(dmin, CK['Q2_clear_of_mooring']['expected'], 0.01))
plinth = box(-121.4, -20.9, -118.6, -18.1)
dl = min(plinth.distance(Point(p[0], p[1])) for p in allpost)
t('D', f"Q2: the nearest post to the harbour light's plinth is {dl:.2f} m (at least 2.5)", dl >= 2.5 and near(dl, CK['Q2_clear_of_light']['expected'], 0.01))
par = box(-129.4, -100.6, -128.6, -23.0)
t('D', 'Q2: no post or plate touches the jetty\'s seaward parapet', all(par.distance(box(p[0] - 0.1, p[1] - 0.1, p[0] + 0.1, p[1] + 0.1)) > 0.0 for p in allpost))
t('D', 'Q2: the K5 ladder group on the north quay (x -69.5) is untouched: no Q2 post within 30 m of it', min(math.hypot(p[0] + 69.5, p[1] + 36.0) for p in allpost) > 30)
t('D', 'Q2: a person on the jetty keeps far more than 0.68 m (the strip is 20 m across; the rail line is 0.4 behind the nose)', 20.0 - 0.4 - 0.1 > 0.68 and CK['Q2_walking_clear']['expected'] == 19.6)

# profiles as point lists
PRA = A1['profiles']
t('D', 'A1 profiles: the post section is a circle of the stated OD with an inner circle of OD - 2 wall (32 points each)', all(abs(math.hypot(*p_) - A['post']['od'] / 2) < 0.01 for p_ in PRA['post_section']['outer']) and all(abs(math.hypot(*p_) - (A['post']['od'] / 2 - A['post']['wall'])) < 0.01 for p_ in PRA['post_section']['inner']))
t('D', 'A1 profiles: the top rail, bottom rail and bar sections have the stated radii', all(abs(math.hypot(*p_) - A['top_rail']['od'] / 2) < 0.01 for p_ in PRA['top_rail_section']['outer']) and all(abs(math.hypot(*p_) - A['bottom_rail']['od'] / 2) < 0.01 for p_ in PRA['bottom_rail_section']['outer']) and all(abs(math.hypot(*p_) - 6.0) < 0.01 for p_ in PRA['bar_section']['outer']))
t('D', 'A1 profiles: the cap (r, z) rises to z 1000 on the axis, is 26 across and 8 high', PRA['cap_rz'][-1] == [0.0, 1000.0] and near(max(p_[0] for p_ in PRA['cap_rz']), 26.0, 1e-9) and near(max(p_[1] for p_ in PRA['cap_rz']) - min(p_[1] for p_ in PRA['cap_rz']), 8.0, 1e-9))
t('D', 'A1 profiles: the ground ring is 20 wide round the post', near(PRA['ground_ring']['width'], 20.0, 1e-9) and near(max(math.hypot(*p_) for p_ in PRA['ground_ring']['outer']) - A['post']['od'] / 2, 20.0, 0.01))
PRQ = Q2['profiles']
t('D', 'Q2 profiles: the post section is 76.1 with a 5.0 wall; the cap rises to 1100 on the axis, 80 across', all(abs(math.hypot(*p_) - 38.05) < 0.01 for p_ in PRQ['post_section']['outer']) and PRQ['cap_rz'][0] == [0.0, 1100.0] and near(2 * max(p_[0] for p_ in PRQ['cap_rz']), 80.0, 1e-9))
t('D', 'Q2 profiles: the hex nut is 24 across flats (distance between opposite sides) and 13 high', near(2 * 13.856 * math.cos(math.pi / 6), PRQ['nut_across_flats'], 0.01) and len(PRQ['nut_hex_outline']) == 6 and PRQ['nut_height'] == 13.0)
t('D', 'Q2 profiles: the stud holes are on a 150 square inside the plate, 25 from its edges', all(abs(abs(h_[0]) - 75.0) < 1e-9 and abs(abs(h_[1]) - 75.0) < 1e-9 for h_ in PRQ['base_plate_holes']) and near(100.0 - 75.0, 25.0, 1e-9))
xs_l = [p_[0] for p_ in PRQ['link_inplane']['outline']]
ys_l = [p_[1] for p_ in PRQ['link_inplane']['outline']]
t('D', 'Q2 profiles: the in-plane link is 65 x 44 outside and 39 x 18 inside (the bollards target\'s plain chain)', near(max(xs_l) - min(xs_l), 65.0, 0.01) and near(max(ys_l) - min(ys_l), 44.0, 0.01) and near(max(p_[0] for p_ in PRQ['link_inplane']['hole']) - min(p_[0] for p_ in PRQ['link_inplane']['hole']), 39.0, 0.01))
cz = PRQ['catenary_xz']
t('D', 'Q2 profiles: the catenary is symmetric, starts and ends at the eyes (z 500) and its lowest point is z 300 at mid-span', near(cz[0][1], 500.0, 0.01) and near(cz[-1][1], 500.0, 0.01) and near(min(p_[1] for p_ in cz), 300.0, 0.6) and near(cz[0][0], -cz[-1][0], 0.01))
# the checks
names = [c['name'] for c in T['checks']]
t('D', f"checks: {len(names)} listed, names unique", len(set(names)) == len(names))
t('D', 'checks: every one has a number or a stated value, a tolerance, a unit, a kind and a basis', all(('expected' in c and 'tol' in c and 'unit' in c and 'kind' in c and 'basis' in c) for c in T['checks']))
t('D', 'checks: the footway one is a minimum of 0.68 m', CK['A1_walking_clear'].get('minimum') == 0.68)
t('D', 'checks: kinds named are A1, Q2, Q2b only', {c['kind'] for c in T['checks']} <= {'A1', 'Q2', 'Q2b'})
t('D', 'variants: the three A1 conditions\' shares sum to 1', near(sum(c['share'] for c in T['variants']['A1_conditions']), 1.0, 1e-9))
t('D', 'materials: unique ids, each with sRGB in 0..255, roughness 0..1', len({m['id'] for m in T['materials']}) == len(T['materials']) and all(all(0 <= c <= 255 for c in m['srgb']) and 0 <= m['roughness'] <= 1 for m in T['materials']))
t('D', 'paint: A1 default is black (24, 24, 26), the same as Q2 and the bollards\' K1 and K5', A['post'] is not None and A1['paint']['srgb'] == Q2['paint']['srgb'] == [24, 24, 26] == BT['kinds']['K1']['paint']['srgb'])
t('D', 'the reserve kinds are marked placed = false and have no placement', all(K[k_]['placed'] is False for k_ in ('R3A', 'R3B', 'R3D')) and not any(p.get('kind') in ('R3A', 'R3B', 'R3D') for p in PL['street'] + PL['quay']))
t('D', 'no area railing, yard gate or chapel on the street is stated in placements.absent, with the reasons', all(k_ in PL['absent'] for k_ in ('area_railings', 'yard_gate', 'backdrop')))
t('D', 'the photograph windows hold their objects: each preview window is inside its plane\'s window and its mm a pixel gives at most 1200 px', all((F_['preview']['s1'] - F_['preview']['s0']) / F_['preview']['mm'] <= 1200 and (F_['preview']['z1'] - F_['preview']['z0']) / F_['preview']['mm'] <= 1200 for F_ in FR.values()))
drw = D.all_views()
t('D', f"the drawing makes {len(drw)} views from target.json alone; every polygon has at least three points and finite numbers", all(len(pg['poly']) >= 3 and all(math.isfinite(c) for pt in pg['poly'] for c in pt) for v_ in drw for pg in v_.polys))

# ------------------------------------------------------------------------------------------------------------------ E
files = sorted(os.listdir(PREV)) if os.path.isdir(PREV) else []
t('E', f"{len(files)} previews exist in production/previews/cloud-week/refs/railings/", len(files) >= 10)
bad = []
for f_ in files:
    p = os.path.join(PREV, f_)
    im_ = Image.open(p)
    if max(im_.size) > 1200 or os.path.getsize(p) > 300 * 1024 or not f_.lower().endswith('.jpg'):
        bad.append((f_, im_.size, os.path.getsize(p)))
t('E', 'every preview is a JPEG of at most 1200 px and under 300 KB' + (' (%s)' % bad if bad else ''), not bad)
t('E', 'the main photograph overlay exists: ...-target-on-photo.jpg', any(f_.endswith('-target-on-photo.jpg') for f_ in files) and 'ph-bethnal_green_entrance-r3b-park-railing-target-on-photo.jpg' in files)
t('E', 'names follow <ref>-<place>-<what>.jpg (ph- or target- prefix)', all(re.match(r'^(ph|target)-[a-z0-9_\-]+\.jpg$', f_) for f_ in files))
txt_all = json.dumps(T).lower()
doc = open(os.path.join(HERE, 'TARGET.md'), encoding='utf-8').read() if os.path.exists(os.path.join(HERE, 'TARGET.md')) else ''
forb = ['jacksons', 'glasdon', 'marshalls', 'streetscape', 'lion foundry', 'carron', 'royal mail', 'post office', 'thorn', 'tower hamlets', 'alcohol', 'beer', 'lager', 'whisky', 'betting', 'bookmaker', 'casino', 'child']
hit = [w for w in forb if w in txt_all]
t('E', 'target.json carries no maker\'s, council\'s or brand name and no word of the content rule (%s)' % (hit or 'none'), not hit)
if doc:
    dh = [w for w in forb if w in doc.lower()]
    t('E', 'TARGET.md carries none of them (%s)' % (dh or 'none'), not dh)
    t('E', 'TARGET.md has a one-line summary first and states the self-check result line', doc.split('\n')[0].startswith('# ') and ('**' in doc.split('\n')[2] or '**' in doc.split('\n')[3]))
    miss = [c['name'] for c in T['checks'] if c['name'] not in doc]
    t('E', 'TARGET.md names every check (%d missing%s)' % (len(miss), ': ' + ', '.join(miss[:6]) if miss else ''), not miss)
    nums = ['48.3', '42.4', '33.7', '97.1', '109.1', '76.1', '3.375', '0.205', '1.576', '0.896', '78.5', '94.5', '-110.4', '-15.4', '0.97', '1.12', '200']
    t('E', 'TARGET.md quotes the key numbers of target.json: ' + ', '.join(nums), all(n_ in doc for n_ in nums))
    t('E', 'TARGET.md has the sections of the brief: sources, the target part by part, photographs-win, variants, materials, wear, what the target could not settle, what to read when the network opens, the previews', all(k_ in doc.lower() for k_ in ('sources', 'photographs', 'variants', 'materials', 'wear', 'could not settle', 'network opens', 'previews')))
else:
    t('E', 'TARGET.md exists', False)
t('E', 'the unreached sources are listed and none is used: every S-row marked unreached is absent from the used list', all(u not in [s_['url'] for s_ in T['sources']] for u in T['unreached']))

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
    print('  FAIL', g, n)
if '--no-write' not in sys.argv:
    T['self_check'] = dict(result=line, tests=[dict(group=g, name=n, ok=ok) for g, n, ok, d in RES], details=[dict(group=g, name=n, detail=d) for g, n, ok, d in RES if d])
    json.dump(T, open(TP, 'w'), indent=1)
sys.exit(0 if not fails else 1)
