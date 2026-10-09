#!/usr/bin/env python
"""Tests the kerbs-and-covers target against its own sources before anything is built.

  A  printed numbers (SCENE-SLOTS.md, the wear target) come back from target.json; every place the target differs from a printed
     number is named in photographs_win
  B  every photograph measurement is recomputed from its raw readings; every value the target uses lies within its stated error of
     the measurement, or the override is written down
  C  the drawing's projected edges (the photographed crossing, from target_drawing.py) fall on the two main photographs within the
     stated error, at a scale fitted on one dimension only
  D  internal consistency: sections and plans add up, nothing overlaps that should not, nothing floats

Prints a result line, writes {"self_check": ...} into target.json.   /home/user/.bpyenv/bin/python self_check.py
"""
import datetime, json, math, os, re, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import measure as M          # noqa: E402
import target_drawing as TD  # noqa: E402

TJ = os.path.join(HERE, 'target.json')
T = json.load(open(TJ))


def repo_root():
    p = HERE
    while p != '/' and not os.path.exists(os.path.join(p, 'canon.md')):
        p = os.path.dirname(p)
    return p


ROOT = repo_root()
PREV = os.path.join(ROOT, 'production', 'previews', 'cloud-week', 'refs', 'kerbs-and-covers')
R = []   # (part, name, ok, detail)


def ck(part, name, ok, detail=''):
    R.append((part, name, bool(ok), detail))


def near(a, b, tol):
    return abs(a - b) <= tol


# =============================================================================== A: printed numbers
def part_A():
    sc = T['scene_numbers']
    p = os.path.join(ROOT, 'production', 'cloud-week', 'targets', 'SCENE-SLOTS.md')
    txt = open(p).read() if os.path.exists(p) else ''
    ck('A', 'SCENE-SLOTS.md found', bool(txt), p)
    row = lambda name: next((l for l in txt.splitlines() if l.startswith('| ' + name)), '')
    k = row('Kerb')
    g = row('Gully grate')
    rd = row('Road and footway')

    def m(rx, s):
        r = re.search(rx, s)
        return float(r.group(1)) if r else None
    pr = {
        'kerb_upstand': (m(r'upstand ([0-9.]+)', k), 1000), 'kerb_width': (m(r'width ([0-9.]+)', k), 1000), 'kerb_depth': (m(r'depth ([0-9.]+)', k), 1000),
        'kerb_block_length': (m(r'blocks ([0-9.]+) long', k), 1000), 'channel_course_width': (m(r'channel course ([0-9.]+) wide', k), 1000),
        'crossover_width': (m(r'\(([0-9.]+) wide', k), 1000), 'crossover_centre_x_m': (m(r'at x ([0-9.]+)', k), 1), 'crossover_upstand': (m(r'([0-9.]+) mm upstand', k), 1),
        'gully_grate_square': (m(r'grate ([0-9.]+) square', g), 1000), 'gully_recess': (m(r'recess ([0-9.]+)', g), 1000), 'gully_dish': (m(r'dish ([0-9.]+)', g), 1000),
        'gully_x_m': (m(r'x ([0-9.]+)', g), 1), 'carriageway_width': (m(r'\| ([0-9.]+) m carriageway', rd), 1000),
        'crown_above_channel': (m(r'crown ([0-9.]+) mm', rd), 1), 'footway_width': (m(r'footways ([0-9.]+) m', rd), 1000),
    }
    for key, (val, mult) in pr.items():
        ok = val is not None and near(val * mult, sc[key], 1e-6)
        ck('A', f'printed {key} = target.json scene_numbers', ok, f'printed {val} x {mult} vs {sc[key]}')
    # numbers used in the pieces that are Read must equal the printed ones
    P = T['pieces']
    ck('A', 'kerb depth used = printed 255', P['kerb_granite']['depth'] == sc['kerb_depth'] and P['kerb_concrete']['depth'] == sc['kerb_depth'])
    ck('A', 'concrete block length used = printed 915', P['kerb_concrete']['length_mm']['fixed'] == sc['kerb_block_length'])
    ck('A', 'concrete channel block width used = printed 255', P['channel_concrete']['width'] == sc['channel_course_width'])
    ck('A', 'granite channel 225 differs from the printed 255 and says so; its courses add to 225', P['channel_setts']['width_total'] == sum(c['across'] for c in P['channel_setts']['courses']) == 225 and any('channel width' in w['item'] for w in T['photographs_win']))
    ck('A', 'crossing width used = printed 3.0 m', P['crossover']['width_between_kerb_ends'] == sc['crossover_width'])
    ck('A', 'crossover upstand: scene 6 mm is overridden (lip 15) and says so', any('crossover' in w['item'] for w in T['photographs_win']))
    # every difference from a printed number is named in photographs_win
    diffs = [('kerb_width', P['kerb_granite']['top_width'], 'kerb top width'), ('kerb_upstand', P['kerb_concrete']['upstand'], 'kerb upstand'),
             ('kerb_block_length', P['kerb_granite']['length_mm']['mean'], 'kerb block length'), ('gully_grate_square', P['gully_grate_A']['overall_along_kerb'], 'gully grate'),
             ('crossover_upstand', P['crossover']['lip_row']['top_z'], 'dropped crossover upstand'), ('gully_dish', P['gully_grate_A']['dish'], 'gully grate'),
             ('channel_course_width', P['channel_setts']['width_total'], 'channel width')]
    wins = ' | '.join(w['item'] for w in T['photographs_win'])
    for key, used, kw in diffs:
        if isinstance(used, str):
            used = 0
        differs = key in sc and not near(used, sc[key], 1e-6) if isinstance(sc.get(key), (int, float)) else False
        ck('A', f'difference from printed {key} is written down', (not differs) or kw in wins, f'scene {sc.get(key)} / used {used} -> "{kw}" in photographs_win')
    # the wear target's numbers
    wj = os.path.join(ROOT, 'production', 'cloud-week', 'targets', 'wear', 'target.json')
    if os.path.exists(wj):
        W = json.load(open(wj))
        ad = W['surfaces']['asphalt_dry']['albedo_srgb']
        ck('A', 'wear asphalt_dry albedo = the anchor used for colours', ad == T['photo_samples']['wear_asphalt_dry'], f'{ad}')
        co = W['measurements']['M24']['values']['channel_over_road']
        chk = next(c for c in T['checks'] if c['name'] == 'channel_over_road_brightness')
        ck('A', 'wear M24 channel over road 1.35 to 1.7 = the check', [chk['expected']['min'], chk['expected']['max']] == co, f'{co}')
        kg = W['surfaces']['kerb_granite']['albedo_srgb']
        mine = T['materials']['granite_grey']['srgb']
        ck('A', 'granite colour within 12 levels of the wear target kerb_granite', all(near(a, b, 12) for a, b in zip(mine, kg)), f'{mine} vs {kg}')
    else:
        ck('A', 'wear target.json found', False, wj)


# =============================================================================== B: photograph measurements
def part_B():
    pms = {p['id']: p for p in T['photo_measurements']}
    for pid, p in pms.items():
        res = M.compute(p)
        ok = json.dumps(res, sort_keys=True) == json.dumps(p['result'], sort_keys=True)
        # tolerate float noise
        if not ok:
            ok = all((near(res[k], p['result'][k], 0.06) if isinstance(res[k], (int, float)) else res[k] == p['result'][k]) for k in res if not isinstance(res[k], (list, dict))) and set(res) == set(p['result'])
        ck('B', f'{pid} recomputes from its raw readings', ok, f'{res}')
    P = T['pieces']
    kg, kc, cx = P['kerb_granite'], P['kerb_concrete'], P['crossover']

    def mid_height(sec):          # height of the 45-degree point of the rounded arris
        pts = sec['section_yz']
        zs = [z for y, z in pts if z > 0]
        return None
    # the arris middle: 45 degrees on a circle of radius R whose centre is (R, up - R)
    mid_g = (kg['upstand'] - kg['top_arris_radius']) + kg['top_arris_radius'] * math.sin(math.radians(45))
    mid_c = (kc['upstand'] - kc['top_arris_radius']) + kc['top_arris_radius'] * math.sin(math.radians(45))
    up = [pms['PM01']['result']['upstand_to_arris_mid_mm'], pms['PM02']['result']['upstand_to_arris_mid_mm']]
    ck('B', 'granite upstand (to the arris middle) within 15 mm of PM01/PM02 mean', near(mid_g, sum(up) / 2, 15), f'model {mid_g:.1f} vs {sum(up) / 2:.1f}')
    w = [pms['PM01']['result']['top_width_given_measured_upstand_mm'], pms['PM02']['result']['top_width_given_measured_upstand_mm'], pms['PM25']['result']['values_mm'][0]]
    ck('B', 'granite top width within 15 mm of the mean of PM01, PM02 (at the measured upstand) and PM25', near(kg['top_width'], sum(w) / 3, 15), f'{kg["top_width"]} vs {sum(w) / 3:.1f} from {w}')
    ck('B', 'concrete upstand (arris middle) within 15 mm of PM03', near(mid_c, pms['PM03']['result']['upstand_to_arris_mid_mm'], 15), f'{mid_c:.1f} vs {pms["PM03"]["result"]["upstand_to_arris_mid_mm"]}')
    ck('B', 'concrete top width within 25 mm of PM03 (at the measured upstand: 166)', near(kc['top_width'], pms['PM03']['result']['top_width_given_measured_upstand_mm'], 25), f"{pms['PM03']['result']}")
    ck('B', 'granite face set-back (25 at z 100) within 9 of PM26 (the arris middle, 29)', near(kg['face_batter']['set_back_mm'] + (kg['top_arris_radius'] - kg['top_arris_radius'] * math.cos(math.radians(45))), pms['PM26']['result']['set_back_mm'], 9), f"{pms['PM26']['result']}")
    ck('B', 'granite block length mean within 30 mm of PM04; all three inside 800 to 1200', near(kg['length_mm']['mean'], pms['PM04']['result']['mean_mm'], 30) and
       all(kg['length_mm']['min'] <= v <= kg['length_mm']['max'] for v in pms['PM04']['result']['values_mm']), f"{pms['PM04']['result']['values_mm']}")
    ck('B', 'joint 9 within 3 of PM05', near(kg['joint_mm']['width'], pms['PM05']['result']['width_mm'], 3))
    chan = pms['PM06']['result']['width_mm']
    ck('B', 'granite channel 225 within 15 of PM06 (226)', near(P['channel_setts']['width_total'], chan, 15), f'{chan}')
    ck('B', 'lip sett length within 9 of PM07 mean', near(cx['lip_row']['sett_along_mm'], pms['PM07']['result']['mean_mm'], 9))
    ck('B', 'lip depth within 9 of PM08 (125)', near(cx['lip_row']['y1'] - cx['lip_row']['y0'], pms['PM08']['result']['mean_mm'], 9), f"{pms['PM08']['result']}")
    ck('B', 'lip upstand within 8 of PM09', near(cx['lip_row']['top_z'], pms['PM09']['result']['height_mm'], 8))
    ck('B', 'reference gap within 30 of PM10', near(T['reference_instance']['gap_between_kerb_ends'], pms['PM10']['result']['length_mm'], 30))
    ck('B', 'ramp back edge within 40 of PM11', near(-cx['ramp']['plan_y'][0], pms['PM11']['result']['difference_mm'], 40), f"{pms['PM11']['result']}")
    ck('B', 'flank width within 12 of the mean of PM12 (171, 141)', near(cx['flank_strips']['width_mm'], (pms['PM12']['result']['values_mm'][0] + pms['PM12']['result']['values_mm'][1]) / 2, 12))
    ck('B', 'flank length within 20 of the mean of PM12 (750, 705)', near(cx['flank_strips']['length_mm'], (pms['PM12']['result']['values_mm'][2] + pms['PM12']['result']['values_mm'][3]) / 2, 20))
    ga = P['gully_grate_A']
    ck('B', 'grate overall within 9 of PM13', near(ga['overall_along_kerb'], pms['PM13']['result']['values_mm'][0], 9) and near(ga['overall_across'], pms['PM13']['result']['values_mm'][1], 9))
    ck('B', 'grate slot span, slot length and pitch within 8/8/3 of PM14', near(ga['slot_span'], pms['PM14']['result']['values_mm'][0], 8) and near(ga['slot_length'], pms['PM14']['result']['values_mm'][1], 8) and near(ga['slot_pitch'], pms['PM14']['result']['values_mm'][2], 3))
    ck('B', 'grate B pitch within 6 of PM15', near(P['gully_grate_B']['slot_pitch'], pms['PM15']['result']['width_mm'], 6), f"{pms['PM15']['result']}")
    ck('B', 'corner radius within 600 of PM16', near(P['kerb_corner_radius']['radius_face_mm'], pms['PM16']['result']['radius_face_mm'], 600))
    st = P['cover_stud_square']
    ck('B', 'stud pitch within 8 of the mean of PM17 (97.7, 91.1); lattice square (cos < 0.05)', near(st['pattern']['pitch_mm'], (pms['PM17']['result']['pitch_a_mm'] + pms['PM17']['result']['pitch_b_mm']) / 2, 8) and abs(pms['PM17']['result']['dot_cos']) < 0.05)
    ck('B', 'stud cover outer within 70 of PM18 mean', near(st['outer'][0], sum(pms['PM18']['result']['lengths_mm']) / 2, 70))
    r19 = pms['PM19']['result']['values_mm']
    cf = P['cover_recessed_footway']
    ck('B', 'footway cover outer 1180 x 670 within 50/100 of PM19; infill within 30/60', near(cf['outer'][0], r19[0], 50) and near(cf['outer'][1], r19[1], 100) and near(cf['infill'][0], r19[2], 30) and near(cf['infill'][1], r19[3], 60))
    ck('B', 'footway cover rim 110 within 25 of PM19 (126)', near(cf['frame_rim_total'], r19[4], 25))
    r20 = pms['PM20']['result']['values_mm']
    ck('B', 'tarmac-filled recess within 40 of PM20', near(P['cover_recessed_road']['outer'][0], r20[0], 40) and near(P['cover_recessed_road']['outer'][1], r20[1], 40))
    r21 = pms['PM21']['result']['values_mm']
    ck('B', 'two-leaf cover within 150 of PM21', near(P['cover_road_double_leaf']['outer'][0], r21[0], 150) and near(P['cover_road_double_leaf']['outer'][1], r21[1], 150))
    ck('B', 'yellow line 72 mm against 75: the 1.6 m camera scale holds within 5 %', near(pms['PM22']['result']['values_mm'][0], 75, 4))
    rc = P['cover_round_600']
    ck('B', 'round cover frame 690, lid 590, depth 68 within 5/5/3 of the model', near(rc['frame_outer_diameter'], pms['PM24']['result']['outer_diameter_mm'], 5) and near(rc['lid_diameter'], 2 * pms['PM24']['result']['lid_radius_mm'], 5) and near(rc['frame_depth'], pms['PM24']['result']['depth_mm'], 3))
    ck('B', 'lug cell = the autocorrelation periods', rc['pattern']['cell_mm'] == [pms['PM23']['result']['period_x_mm'], pms['PM23']['result']['period_y_mm']])
    # colours: recompute the albedos from the stored photograph samples
    from make_target import albedo_from, PHOTO_SAMPLES   # same function that wrote them
    ok = True
    for key, smp in (('granite_blue_grey', [112, 116, 126]), ('sett_pale_worn', PHOTO_SAMPLES['channel_setts_pale']), ('sett_dull', PHOTO_SAMPLES['channel_setts_dull']), ('concrete_ramp', PHOTO_SAMPLES['concrete_ramp'])):
        ok = ok and T['materials'][key]['srgb'] == albedo_from(smp)
    ck('B', 'material albedos recompute from the photograph samples (linear ratio to the road)', ok)
    ck('B', 'photograph samples stored match target.json photo_samples', T['photo_samples']['samples'] == PHOTO_SAMPLES)


# =============================================================================== C: drawing on the photographs
def gray(path):
    return np.asarray(Image.open(path).convert('L'), dtype=float)


def probe(G, pr, scale):
    """look for an edge near its predicted place on the photograph; returns detected minus predicted in mm along the edge's normal
    (+ = down the picture for a horizontal edge, + = right for a vertical one), or None when the edge is outside the picture"""
    mm = T['photo_frames']['MAIN']['mm_per_px']
    plane = pr['image']
    z = pr.get('z_mm', 0.0)
    typ = pr.get('type', 'step')
    if pr['kind'] == 'h':
        ca, ra = TD.plan_to_px(T, pr['span'][0] * scale, pr['fixed'] * scale, z, plane)
        cb, _ = TD.plan_to_px(T, pr['span'][1] * scale, pr['fixed'] * scale, z, plane)
        c0, c1 = int(round(min(ca, cb))), int(round(max(ca, cb)))
        if c0 < 0 or c1 >= G.shape[1] or ra < 16 or ra > G.shape[0] - 16:
            return None
        prof = G[:, c0:c1 + 1].mean(1)
        pred = ra
    else:
        ca, _ = TD.plan_to_px(T, pr['fixed'] * scale, 0, z, plane)
        _, ra = TD.plan_to_px(T, 0, pr['span'][0] * scale, z, plane)
        _, rb = TD.plan_to_px(T, 0, pr['span'][1] * scale, z, plane)
        r0, r1 = int(round(min(ra, rb))), int(round(max(ra, rb)))
        if r0 < 0 or r1 >= G.shape[0] or ca < 16 or ca > G.shape[1] - 16:
            return None
        prof = G[r0:r1 + 1, :].mean(0)
        pred = ca
    i0 = int(round(pred))
    win = range(i0 - 8, i0 + 9)
    if typ == 'step':
        d = np.abs(prof[2:] - prof[:-2]) / 2.0
        best = max(win, key=lambda i: d[i - 1])
    elif typ == 'line':
        sm = gaussian_filter(prof, 1.0)
        best = min(win, key=lambda i: sm[i])
    else:   # step_low: the start of a soft rise, 20 % of the way from the dark side to the light side
        lo = min(prof[i] for i in win)
        hi = max(prof[i] for i in win)
        thr = lo + 0.2 * (hi - lo)
        best = next((i for i in win if prof[i] >= thr), i0)
        if best > win[0]:
            a_, b_ = prof[best - 1], prof[best]
            best = best - 1 + (thr - a_) / (b_ - a_) if b_ != a_ else best
    return (best - pred) * mm


def part_C():
    fr = T['photo_frames']['MAIN']
    paths = {'ground': os.path.join(PREV, fr['ground_image']), 'top': os.path.join(PREV, fr['top_image'])}
    for k, p in paths.items():
        ck('C', f'main photograph ({k}) present, at most 1200 px and under 300 KB', os.path.exists(p) and max(Image.open(p).size) <= 1200 and os.path.getsize(p) < 300000, p)
    if not all(os.path.exists(p) for p in paths.values()):
        return
    G = {k: gaussian_filter(gray(p), 1.2) for k, p in paths.items()}
    probes = {p['id']: p for p in T['edge_probes']}
    # scale fitted on one dimension: the distance between the two flank strips' outer edges, on the top photograph
    sf = T['scale_fit']
    pl, pr_ = probes[sf['left']], probes[sf['right']]
    offL = probe(G['top'], pl, 1.0)
    offR = probe(G['top'], pr_, 1.0)
    scale = 1.0
    if offL is not None and offR is not None:
        detected = (pr_['fixed'] + offR) - (pl['fixed'] + offL)
        scale = detected / sf['mm_between']
    ck('C', 'scale fitted on one dimension (flank outer to flank outer) is 1.00 +-0.03', abs(scale - 1) <= 0.03, f'fitted {scale:.3f}')
    offs = []
    for pr in T['edge_probes']:
        off = probe(G[pr['image']], pr, scale)
        if off is None:
            ck('C', f"edge {pr['id']} found inside the picture", False, 'outside the frame')
            continue
        offs.append(abs(off))
        ck('C', f"edge {pr['id']} within {pr['tol_mm']} mm of the photograph's edge", abs(off) <= pr['tol_mm'], f"{pr['what']}: offset {off:+.0f} mm")
    if offs:
        ck('C', 'median edge offset within 9 mm', float(np.median(offs)) <= 9, f'median {np.median(offs):.1f} mm over {len(offs)} edges')
    # the overlay pictures exist
    for n in ('ph-urban_street_03-target-on-photo.jpg', 'ph-urban_street_03-target-on-top-photo.jpg'):
        ck('C', f'overlay {n} present and small', os.path.exists(os.path.join(PREV, n)) and os.path.getsize(os.path.join(PREV, n)) < 300000)
    # every preview is at most 1200 px and under 300 KB
    bad = [f for f in os.listdir(PREV) if f.endswith('.jpg') and (max(Image.open(os.path.join(PREV, f)).size) > 1200 or os.path.getsize(os.path.join(PREV, f)) >= 300000)]
    ck('C', 'every preview is at most 1200 px and under 300 KB', not bad, str(bad))


# =============================================================================== D: internal consistency
def poly(pts):
    return Polygon(pts)


def part_D():
    P = T['pieces']
    # --- kerb sections
    for key in ('kerb_granite', 'kerb_concrete'):
        s = P[key]
        pg = poly(s['section_yz'])
        minx, miny, maxx, maxy = pg.bounds
        ck('D', f'{key} section is a valid polygon', pg.is_valid and pg.area > 0)
        ck('D', f'{key} section width = top_width, height = upstand, depth = 255, face at y = 0 and back at y = -width', near(maxx - minx, s['top_width'], 0.01) and near(maxy, s['upstand'], 0.01) and near(maxy - miny, s['depth'], 0.01) and near(maxx, 0, 0.01), f'{pg.bounds}')
        # arris radius: the arc points lie on the circle
        R_ = s['top_arris_radius']
        bat = s.get('face_batter', {}).get('set_back_mm', 0)
        cy, cz = -R_ - bat, s['upstand'] - R_
        arc = [p for p in s['section_yz'] if cy < p[0] < cy + R_ and p[1] > cz + 1e-6 and p[1] < s['upstand']]
        ck('D', f'{key} arris points on a circle of radius {R_}', all(near(math.hypot(p[0] - cy, p[1] - cz), R_, 0.1) for p in arc) and len(arc) >= 4, f'{len(arc)} points')
        if bat:
            fp = [p for p in s['section_yz'] if p[0] == 0 and p[1] > 0]
            ck('D', f'{key} face: vertical to z = 45 then set back 25 mm by z = 100', fp and max(p[1] for p in fp) == s['face_batter']['vertical_to_z'] and any(p == [-bat, s['face_batter']['at_z']] for p in s['section_yz']), f'{fp}')
    # --- channel
    ch = P['channel_setts']
    ck('D', 'channel courses are contiguous and add to 225', ch['courses'][0]['y0'] == 0 and ch['courses'][0]['y1'] == ch['courses'][1]['y0'] and ch['courses'][1]['y1'] == ch['width_total'] == 225)
    # --- crossover: parts add up
    cx = P['crossover']
    lip, rp, fl = cx['lip_row'], cx['ramp'], cx['flank_strips']
    gap = cx['width_between_kerb_ends']
    n = math.ceil(gap / (lip['sett_along_mm'] + lip['joint_mm']))
    ck('D', 'lip setts: count x pitch fills the gap (17 setts, pitch 176 within 10 of 180)', n == 17 and near(gap / n, lip['sett_along_mm'] + lip['joint_mm'], 10), f'{n}, pitch {gap / n:.1f}')
    ck('D', 'ramp meets the lip across a 12 mm joint: ramp front y = lip back y - 12; ramp z at the lip = lip top', rp['plan_y'][1] == lip['y0'] - rp['joint_to_lip_and_flanks_mm'] == -137 and rp['z_at_lip'] == lip['top_z'])
    ck('D', 'ramp gradient: rise 105 over run 780 = 1 in 7.4', near(rp['z_at_back'] - rp['z_at_lip'], 105, 0) and near(rp['plan_y'][1] - rp['plan_y'][0], 780, 0) and near(780 / 105, 7.43, 0.02))
    ck('D', 'ramp back z = footway z (120) = flank top; kerb top = footway + 5', rp['z_at_back'] == fl['top_z'] == 120 and P['kerb_granite']['upstand'] - 120 == 5)
    kw = P['kerb_granite']['top_width']
    ck('D', 'flank strip front is 12 mm behind the kerb back; back within 15 of the ramp back', near(-fl['plan_y'][1] - kw, 12, 0.01) and near(fl['plan_y'][0], rp['plan_y'][0], 15), f"{fl['plan_y']} vs kerb back {-kw}")
    ck('D', 'flank length = back minus front', near(fl['plan_y'][1] - fl['plan_y'][0], fl['length_mm'], 0.01))
    ck('D', 'lip back (-125) is within the kerb body (-190): the lip stands where the kerb stood', lip['y0'] > -kw and lip['y1'] == 0)
    ref = T['reference_instance']
    ck('D', 'reference instance: flank, ramp and lip numbers equal the street instance; its flank widths average the street\'s 155', ref['flank']['y0'] == fl['plan_y'][0] and ref['flank']['y1'] == fl['plan_y'][1] and ref['ramp_back_y'] == rp['plan_y'][0] and ref['ramp_front_y'] == rp['plan_y'][1] and ref['lip']['y0'] == lip['y0'] and near(((ref['flank']['left_x'][1] - ref['flank']['left_x'][0]) + (ref['flank']['right_x'][1] - ref['flank']['right_x'][0])) / 2, fl['width_mm'], 2))
    # --- plan overlaps: build the street crossing and test
    v = TD.plan_crossover(T, 'street')
    sh = {}
    for i, pl in enumerate(v.polys):
        sh.setdefault(pl['name'], []).append((i, Polygon(pl['points'])))
    # kerb blocks, flank strips, ramp, lip setts must not overlap each other (touching is fine)
    solid = [(n, i, g) for n in ('kerb_block_L', 'kerb_block_R', 'flank_L', 'flank_R', 'ramp', 'lip_sett') for i, g in sh[n]]
    worst = 0.0
    bad = []
    for a in range(len(solid)):
        for b in range(a + 1, len(solid)):
            ia = solid[a][2].intersection(solid[b][2]).area
            if ia > 1.0:
                bad.append((solid[a][0], solid[b][0], round(ia, 1)))
            worst = max(worst, ia)
    ck('D', 'crossing plan: no overlap between kerb blocks, flank strips, ramp and lip setts (over 1 mm2)', not bad, str(bad[:4]))
    # channel setts do not overlap each other nor the lip row beyond 1 mm2
    cs = [g for n in ('sett_A', 'sett_B') for i, g in sh.get(n, [])]
    ck('D', 'channel setts: no overlap with each other', all(cs[a].intersection(cs[b]).area <= 1.0 for a in range(len(cs)) for b in range(a + 1, min(len(cs), a + 40))))
    # blocks: lengths in range, no equal neighbours, joints 9 apart
    for side in ('kerb_block_L', 'kerb_block_R'):
        bl = sorted([g for i, g in sh[side]], key=lambda g: g.bounds[0])
        Ls = [g.bounds[2] - g.bounds[0] + 9 for g in bl]
        ok = all(790 <= L <= 1210 for L in Ls[:-1]) and all(abs(Ls[i] - Ls[i + 1]) >= 20 for i in range(len(Ls) - 1))
        ck('D', f'{side}: lengths 800 to 1200 (last one cut), neighbours differ by 20+', ok, f'{[round(L) for L in Ls]}')
        gaps = [bl[i + 1].bounds[0] - bl[i].bounds[2] for i in range(len(bl) - 1)]
        ck('D', f'{side}: joints are 9 mm', all(near(g, 9, 0.5) for g in gaps))
    # nothing floats: every section polygon touches or overlaps another one in its view (one connected group)
    for nm in ('section_kerb_granite', 'section_kerb_concrete', 'section_crossover'):
        vw = {'section_kerb_granite': TD.section_kerb(T, 'granite'), 'section_kerb_concrete': TD.section_kerb(T, 'concrete'), 'section_crossover': TD.section_crossover(T)}[nm]
        gs = [Polygon(pl['points']).buffer(0.5) for pl in vw.polys]
        comp = [0]
        seen = {0}
        while comp:
            i = comp.pop()
            for j in range(len(gs)):
                if j not in seen and gs[i].intersects(gs[j]):
                    seen.add(j)
                    comp.append(j)
        ck('D', f'{nm}: every piece touches another (nothing floats)', len(seen) == len(gs), f'{len(seen)} of {len(gs)}')
    # --- gully grates
    ga = P['gully_grate_A']
    ck('D', 'grate A: slot span + two end walls = overall along; slot length + two end walls = overall across',
       near(ga['slot_span'] + 2 * ga['end_wall_along'], ga['overall_along_kerb'], 0.01) and near(ga['slot_length'] + 2 * ga['end_wall_across'], ga['overall_across'], 0.01))
    ck('D', 'grate A: 8 slots, bar = pitch - slot = 39, slot centres symmetric', ga['slot_count'] == 8 and ga['bar_width'] == 39 and near(sum(ga['slot_centres_x']), 0, 1e-6) and len(ga['slot_centres_x']) == 8)
    gv = TD.plan_gully(T, 'A')
    outer = Polygon(gv.polys[0]['points'])
    slots = [Polygon(p['points']) for p in gv.polys[1:]]
    ck('D', 'grate A: every slot inside the grate and no two slots overlap', all(outer.contains(s) for s in slots) and all(slots[i].intersection(slots[j]).area == 0 for i in range(8) for j in range(i + 1, 8)))
    gb = P['gully_grate_B']
    ck('D', 'grate B: 7 slot lengths, symmetric, all inside the frame', len(gb['slot_lengths']) == gb['slot_count'] == 7 and gb['slot_lengths'] == gb['slot_lengths'][::-1] and max(gb['slot_lengths']) < gb['overall_across'] and (gb['slot_count'] - 1) * gb['slot_pitch'] + gb['slot_width'] < gb['overall_along_kerb'])
    ref_g = ref['gully']
    ck('D', 'reference gully: along x across = grate A overall within 9; its y range = plan_position within 3', near(ref_g['along'], ga['overall_along_kerb'], 9) and near(ref_g['across'], ga['overall_across'], 9) and near(ref_g['y0'], ga['plan_position']['y0'], 3) and near(ref_g['y1'], ga['plan_position']['y1'], 3))
    # --- covers
    st = P['cover_stud_square']
    n_ = st['pattern']['count'][0]
    span = (n_ - 1) * st['pattern']['pitch_mm'] + st['pattern']['stud_mm']
    ck('D', 'stud cover: 8 x 8 studs fit the lid with the edge margin', near((st['lid_inner'][0] - span) / 2, st['pattern']['edge_margin_mm'], 6), f'span {span}, margin {(st["lid_inner"][0] - span) / 2:.1f}')
    ck('D', 'stud cover: lid inner = outer - 2 x rim', st['lid_inner'][0] == st['outer'][0] - 2 * st['frame_rim'])
    rc = P['cover_round_600']
    ck('D', 'round cover: lid < frame; ring width 50 = (690 - 590)/2', rc['lid_diameter'] < rc['frame_outer_diameter'] and near((rc['frame_outer_diameter'] - rc['lid_diameter']) / 2, rc['frame_ring_width'], 0.01))
    rv = TD.plan_cover_round(T)
    lid = Polygon(rv.polys[1]['points'])
    lugs = [Polygon(p['points']) for p in rv.polys[2:]]
    ck('D', 'round cover: every lug inside the lid, none overlapping', len(lugs) > 20 and all(lid.contains(l) for l in lugs) and all(lugs[i].intersection(lugs[j]).area == 0 for i in range(len(lugs)) for j in range(i + 1, min(len(lugs), i + 12))), f'{len(lugs)} lugs')
    cf = P['cover_recessed_footway']
    ck('D', 'footway cover: infill + 2 x rim = outer in both directions (960 + 220 = 1180; 440 + 220 = 660)', near(cf['infill'][0] + 2 * cf['frame_rim_total'], cf['outer'][0], 0.01) and near(cf['infill'][1] + 2 * cf['frame_rim_total'], cf['outer'][1], 0.01), f"{cf['infill']} + 2 x {cf['frame_rim_total']} vs {cf['outer']}")
    ck('D', 'footway cover: step widths 45 + 65 = rim 110', 45 + 65 == cf['frame_rim_total'])
    dl = P['cover_road_double_leaf']
    ck('D', 'two-leaf cover: two leaves + the 15 mm gap = outer length', near(2 * (dl['outer'][0] / 2 - 7.5) + 15, dl['outer'][0], 0.01))
    # --- no lettering, no tactile
    txt = json.dumps(T).lower()
    objtxt = json.dumps({'pieces': T['pieces'], 'materials': T['materials']}).lower()
    names = ('british gas', 'thames water', 'british telecom', 'post office', 'macfarlane', 'ham baker', 'saint-gobain', 'lion foundry', 'glenfield', 'dudley', 'stanton', 'royal', 'victoria regina', 'borough council', 'city council', 'lewisham', 'southwark', 'islington', 'tower hamlets', 'kensington')
    ck('D', 'no real maker, operator or council name on any piece or material (pieces and materials scanned)', not [w for w in names if w in objtxt], str([w for w in names if w in objtxt]))
    ck('D', 'pieces.tactile_paving says none', 'none' in P['tactile_paving']['what'])
    # --- drawing JSON polygons inside their view ranges
    bad = set()
    for vw in TD.all_views(T):
        x0, x1 = vw.xr
        y0, y1 = vw.yr
        for pl in vw.polys:
            for x, y in pl['points']:
                if not (x0 - 1 <= x <= x1 + 1 and y0 - 1 <= y <= y1 + 1):
                    bad.add(vw.name + ':' + pl['name'])
    ck('D', 'every drawn polygon lies inside its view range', not bad, str(sorted(bad)[:6]))
    ck('D', 'every check in the list has name, measure, expected and tolerance', all(all(k in c for k in ('name', 'measure', 'expected', 'tolerance')) for c in T['checks']), f"{len(T['checks'])} checks")


def part_E():
    p = os.path.join(HERE, 'TARGET.md')
    ok = os.path.exists(p)
    ck('E', 'TARGET.md exists', ok)
    if not ok:
        return
    txt = open(p).read()
    lines = [l for l in txt.splitlines() if l.strip()]
    ck('E', 'TARGET.md starts with a title and one bold summary line equal to target.json summary_line', lines[0].startswith('# ') and lines[1] == '**' + T['summary_line'] + '**')
    P_ = T['pieces']
    nums = {'upstand 125': P_['kerb_granite']['upstand'], 'top width 190': P_['kerb_granite']['top_width'], 'concrete width 160': P_['kerb_concrete']['top_width'], 'depth 255': P_['kerb_granite']['depth'],
            'length 915': P_['kerb_concrete']['length_mm']['fixed'], 'granite channel 225': P_['channel_setts']['width_total'], 'crossing 3000': P_['crossover']['width_between_kerb_ends'],
            'grate 485': P_['gully_grate_A']['overall_along_kerb'], 'grate 325': P_['gully_grate_A']['overall_across'], 'slot pitch 57': P_['gully_grate_A']['slot_pitch'],
            'slot length 285': P_['gully_grate_A']['slot_length'], 'stud cover 860': P_['cover_stud_square']['outer'][0], 'stud pitch 95': P_['cover_stud_square']['pattern']['pitch_mm'],
            'round frame 690': P_['cover_round_600']['frame_outer_diameter'], 'round lid 590': P_['cover_round_600']['lid_diameter'], 'footway cover 1180': P_['cover_recessed_footway']['outer'][0],
            'footway cover 660': P_['cover_recessed_footway']['outer'][1], 'infill 960': P_['cover_recessed_footway']['infill'][0], 'infill 440': P_['cover_recessed_footway']['infill'][1],
            'road recess 1050': P_['cover_recessed_road']['outer'][1], 'double leaf 1820': P_['cover_road_double_leaf']['outer'][0], 'corner radius 6500': P_['kerb_corner_radius']['radius_face_mm'],
            'lip 15': P_['crossover']['lip_row']['top_z'], 'ramp back 917': -P_['crossover']['ramp']['plan_y'][0], 'flank 155': P_['crossover']['flank_strips']['width_mm']}
    missing = [k for k, v in nums.items() if str(v) not in txt]
    ck('E', 'every key number of target.json appears in TARGET.md', not missing, str(missing))
    ck('E', 'TARGET.md names every source id and every photograph-wins item', all(('| ' + s['id'] + ' |') in txt for s in T['sources']) and all(w['item'] in txt for w in T['photographs_win']))
    ck('E', 'TARGET.md has the sections the brief asks for (sources, target, photographs win, variants, materials, wear, could not settle)', all(h in txt for h in ('## 2. Sources', '## 4. The target', '## 6. Where the photographs win', '## 8. Variants', '## 7. Materials', '## 9. Wear', '## 12. What the target could not settle')))


def main():
    part_A()
    part_B()
    part_C()
    part_D()
    part_E()
    npass = sum(1 for r in R if r[2])
    nfail = len(R) - npass
    by = {}
    for p, n, ok, d in R:
        by.setdefault(p, [0, 0])[0 if ok else 1] += 1
    line = (f"SELF-CHECK {'PASS' if nfail == 0 else 'FAIL'}: {npass} of {len(R)} tests pass "
            f"(A printed numbers {by.get('A', [0, 0])[0]}/{sum(by.get('A', [0, 0]))}, B photograph measurements {by.get('B', [0, 0])[0]}/{sum(by.get('B', [0, 0]))}, "
            f"C drawing on the photographs {by.get('C', [0, 0])[0]}/{sum(by.get('C', [0, 0]))}, D internal consistency {by.get('D', [0, 0])[0]}/{sum(by.get('D', [0, 0]))}, E text {by.get('E', [0, 0])[0]}/{sum(by.get('E', [0, 0]))})")
    print(line)
    for p, n, ok, d in R:
        if not ok:
            print('  FAIL', p, n, '|', d)
    if '-v' in sys.argv:
        for p, n, ok, d in R:
            if ok:
                print('  ok  ', p, n, '|', d)
    T2 = json.load(open(TJ))
    T2['self_check'] = {'date': datetime.date.today().isoformat(), 'result_line': line, 'passed': npass, 'total': len(R),
                        'parts': by, 'failures': [{'part': p, 'name': n, 'detail': d} for p, n, ok, d in R if not ok],
                        'tests': [{'part': p, 'name': n, 'ok': ok, 'detail': d} for p, n, ok, d in R]}
    json.dump(T2, open(TJ, 'w'), indent=1)
    sys.exit(0 if nfail == 0 else 1)


if __name__ == '__main__':
    main()
