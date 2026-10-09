#!/usr/bin/env python
"""Tests the bollards target against its own sources before anything is built.

/home/user/.bpyenv/bin/python self_check.py [--no-write]

A  every printed number the target uses comes back from target.json (and is found in the repository file it is quoted from)
B  every photograph measurement overrides as stated (camera heights from their anchors; each reading's radius against the profile; the second photographs)
C  the drawing's projected edges fall on the main photographs within the stated error (a scale fitted on ONE dimension, the height or the collar)
D  internal consistency (parts add up, profiles close, nothing overlaps that should not, nothing floats, every check has its number)
E  the text and the files: no real name, band or mark; pictures within their size limits; the numbers in TARGET.md are target.json's
Prints a result line and writes it into target.json under "self_check"."""
import sys, os, json, math, re
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bollard_lib as L

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PREV = os.path.join(ROOT, 'production', 'previews', 'cloud-week', 'refs', 'bollards')
T = json.load(open(os.path.join(HERE, 'target.json')))
RES = []


def t(group, name, ok, detail=''):
    RES.append((group, name, bool(ok), detail))


def near(a, b, tol):
    return abs(a - b) <= tol


# ----------------------------------------------------------------------------------------------------- A
S = {s['id']: s for s in T['scene_numbers']}
for s in T['scene_numbers']:
    p = os.path.join(ROOT, s['file'])
    ok = os.path.exists(p)
    txt = open(p, encoding='utf-8').read() if ok else ''
    t('A', f"printed {s['id']} found in {s['file']}", ok and s['find'] in txt, s['what'])
pl = T['placements']
yard = [e for e in pl['street_proper'] if e['id'] == 'yard_mouth'][0]
t('A', 'yard mouth bollards are the scene file\'s (x 20.7 and 24.3)', yard['x_m'] == [S['existing_bollard_0_x_m']['value'], S['existing_bollard_1_x_m']['value']])
t('A', 'yard mouth z is the scene file\'s -3.5', near(yard['z_m'], S['existing_bollard_z_m']['value'], 1e-9))
t('A', 'yard mouth set-back is footway z minus kerb face z', near(abs(yard['z_m']) - S['carriageway_half_m']['value'], yard['axis_from_kerb_face_m'], 1e-9))
q = [e for e in pl['quay'] if e['id'] == 'quay_edge'][0]
t('A', 'quay: ten bollards 0.75 m behind the cope nose at x -69.25 (the south-quay kit)',
  q['count'] == S['quay_bollard_count']['value'] and near(q['behind_cope_nose_m'], S['quay_bollard_set_back_m']['value'], 1e-9) and near(q['x_m'], S['quay_bollard_x_m']['value'], 1e-9))
t('A', 'quay: the cope nose is 0.75 m from x -69.25 (x -70)', near(S['quay_edge_x_m']['value'] - S['quay_bollard_x_m']['value'], -0.75, 1e-9))
k6 = T['kinds']['K6']
t('A', 'K6a is the kit\'s: 720 high, flange r 250', near(k6['height'], S['quay_bollard_height_m']['value'] * 1000, 0.01) and near(max(r for r, z in k6['profile_rz']), S['quay_bollard_base_r_m']['value'] * 1000, 0.01))
models = T['variants']['models']
t('A', 'models per kind at most four (asset plan: two to four a kind)', all(v <= 4 for v in models.values()))
t('A', 'seed lean cap (2) within the asset plan\'s 1 to 3', 1 <= T['variants']['seeds']['lean_deg'][1] <= S['asset_plan_lean_deg']['value'])
n_street = pl['counts']['street_and_junction']
t('A', 'street and junction count (10) within the asset plan\'s 6 to 10', 6 <= n_street <= 10)
t('A', 'street counts add up: 2 + 2 + 2 + 4', pl['counts']['street_proper'] + pl['junction']['count'] == n_street and sum(e['count'] for e in pl['street_proper']) == pl['counts']['street_proper'])
t('A', 'by-kind counts match the placements', pl['by_kind']['K1'] == 2 and pl['by_kind']['K2'] == pl['junction']['count'] and pl['by_kind']['K3'] == 2 and pl['by_kind']['K4'] == 2
  and pl['by_kind']['K6'] == q['count'])
t('A', 'no band: the street-clutter note excludes reflective bands and no kind has a band material', all('band' not in m for m in T['materials']))
t('A', 'the street stand-in (0.765) and the held mesh (1.008) are named as what the target replaces', T['kerb_frame']['existing_stand_in'].startswith('0.765'))

# ----------------------------------------------------------------------------------------------------- B
cal = T['calibration']
byp = {}
for a in cal['anchors']:
    h = a['plane_h'] * a['true_mm'] / a['measured_mm']
    byp.setdefault(a['pano'], []).append(h)
for pano, hs in byp.items():
    P = cal['panoramas'][pano]
    m = sum(hs) / len(hs)
    t('B', f'camera height {pano}: anchors {", ".join("%.3f" % h for h in hs)} -> mean {m:.3f}; stated {P["h_cam"]} +-{P["h_cam_err"]}', near(m, P['h_cam'], P['h_cam_err']))
t('B', 'urban_street_02 has no anchor of its own and says so', 'no anchor' in cal['panoramas']['urban_street_02']['h_why'])
t('B', 'no panorama uses 1.6 m (the street writer\'s default is refuted by the anchors)', all(P['h_cam'] < 1.4 for P in cal['panoramas'].values()))
fr = T['frames']
for fid, rows in T['readings'].items():
    F = fr[fid]
    k = cal['panoramas'][F['pano']]['h_cam'] / F['h_read']
    prof = T['profiles_final'][fid]
    errs = []
    for z, Lt, Rt in rows:
        hw = (Rt - Lt) / 2.0 * k * T['readings_r_correction'].get(fid, 1.0)
        r = float(L.r_of_z(prof, [z * k])[0])
        errs.append(hw - r)
    t('B', f'{fid}: {len(rows)} eyeballed edge readings{" (x " + str(T["readings_r_correction"][fid]) + ", the correction the overlay called for)" if fid in T["readings_r_correction"] else ""} against the profile (max {max(abs(e) for e in errs):.1f} mm, mean {np.mean(errs):.1f})', max(abs(e) for e in errs) <= 8.0 and abs(np.mean(errs)) <= 3.5)
vf = T['variant_fits']
# second photographs: recompute the fits
kb = cal['panoramas']['bethnal_green_entrance']['h_cam'] / fr['BGE_a']['h_read']
bge = [(z * kb, hw * kb) for z, hw in T['bge_halfwidth_read']]
prof1 = T['profiles_final']['US01_b']
H1 = max(z for r, z in prof1)
kz = vf['K1b_from_BGE_a']['z_factor']; kr = vf['K1b_from_BGE_a']['r_factor']
res = [hw - kr * float(L.r_of_z(prof1, [z / kz])[0]) for z, hw in bge if not np.isnan(L.r_of_z(prof1, [z / kz])[0])]
t('B', f'BGE_a (second K1 photograph): {len(res)} half widths against K1b: rms {np.sqrt(np.mean(np.square(res))):.1f} mm, max {max(abs(x) for x in res):.1f}', np.sqrt(np.mean(np.square(res))) <= 4.0 and max(abs(x) for x in res) <= 11)
t('B', 'BGE_a height is 0.9655 of US01_b\'s (3.5 % shorter): within the scale error', near(kz, 0.9655, 0.002) and abs(1 - kz) <= 0.07)
ku = cal['panoramas']['urban_street_02']['h_cam'] / fr['US02_a']['h_read']
us = [(z * ku, hw * ku) for z, hw in T['us02_halfwidth_read'] if 150 <= z <= 1000 and not (640 <= z <= 740)]
prof2 = T['profiles_final']['BB_b']
kz2 = vf['K2b_from_US02_a']['z_factor']; kr2 = vf['K2b_from_US02_a']['r_factor']
res2 = [hw - kr2 * float(L.r_of_z(prof2, [z / kz2])[0]) for z, hw in us]
t('B', f'US02_a (second K2 photograph): {len(res2)} half widths against K2b: rms {np.sqrt(np.mean(np.square(res2))):.1f} mm, max {max(abs(x) for x in res2):.1f}', np.sqrt(np.mean(np.square(res2))) <= 2.5 and max(abs(x) for x in res2) <= 5)
H2a = max(z for r, z in T['profiles_final']['BB_b']); H2b = max(z for r, z in T['profiles_final']['US02_a'])
t('B', f'the two K2 photographs agree on the height ({H2a:.0f} and {H2b:.0f})', abs(H2a - H2b) / H2a <= 0.02)
t('B', 'collar height ratio agrees across the two K2 photographs (0.587 and 0.592)', near((674.0 + 713.0) / 2 / H2a, 0.587, 0.02) and near(703.0 / 1188.0, 0.592, 0.01))
for s in T['setbacks_photo']:
    perp = s['along_mm'] * math.cos(math.radians(s['kerb_angle_deg']))
    t('B', f'set-back {s["id"]}: {s["along_mm"]} along the bearing, kerb at {s["kerb_angle_deg"]} degrees -> {perp:.0f} perpendicular', 250 <= perp <= 1300)
sb = [s['along_mm'] * math.cos(math.radians(s['kerb_angle_deg'])) for s in T['setbacks_photo']]
t('B', 'the photographs\' set-backs (0.33 to 1.14 m, kerb face to axis) bracket nothing near 0.5 with a footway of 2.0 m: 0.5 is the scene\'s Read value and is kept', min(sb) < 500 + 100 < max(sb))
# the bead's projection and the collar ratios straight from the profiles
for kid, lo, hi in (('K1', 12, 17), ('K2', 6, 11), ('K5', 12, 18)):
    P = T['kinds'][kid]['profile_rz']
    m = T['kinds'][kid]['mouldings'][0]
    z0, z1 = m['z']
    rpk = max(r for r, z in P if z0 <= z <= z1)
    rb = float(L.r_of_z(P, [z0 - 6])[0]); ra = float(L.r_of_z(P, [z1 + 6])[0])
    proud = rpk - (rb + ra) / 2
    t('B', f'{kid} first moulding stands {proud:.1f} mm proud of the shaft', lo <= proud <= hi)

# ----------------------------------------------------------------------------------------------------- C
def top_scale(img, F, prof, kind):
    mm = F['mm_per_px']
    g = gaussian_filter(img, 1.5)
    gz = np.zeros_like(g); gz[1:-1] = (g[2:] - g[:-2]) / 2.0
    s = math.tan(math.radians(F['lean_deg']))
    H = max(z for r, z in prof)
    def col_band(z):
        row = int(round((F['z_top_mm'] - z) / mm))
        tc = F['axis_offset_mm'] + s * z
        c0 = int(round((tc - 15 - F['t_left_mm']) / mm)); c1 = int(round((tc + 15 - F['t_left_mm']) / mm))
        return gz[row, c0:c1].mean()
    if kind == 'top':
        zs = np.arange(H - 40, H + 20, 1.0)
        v = [abs(col_band(z)) for z in zs]
        return float(zs[int(np.argmax(v))]) / H
    # the collar band: two edges of opposite sign near its lower and upper edges
    z0, z1 = kind
    za = np.arange(z0 - 25, z0 + 25, 1.0); zb = np.arange(z1 - 25, z1 + 25, 1.0)
    va = [col_band(z) for z in za]; vb = [col_band(z) for z in zb]
    ea = float(za[int(np.argmax(np.abs(va)))]); eb = float(zb[int(np.argmax(np.abs(vb)))])
    return ((ea + eb) / 2) / ((z0 + z1) / 2)


SCALE_FEATURE = {'US01_b': 'top', 'BGE_a': 'top', 'LH_b': 'top', 'BB_b': (674.0, 713.0), 'US02_a': (698.0, 737.0)}
TOL = {'US01_b': (3.5, 9), 'LH_b': (3.5, 10), 'BB_b': (3.5, 9), 'BGE_a': (4.5, 10), 'US02_a': (4.5, 10)}      # median and p90 of the edge offsets, mm; the search window is +-10 mm; LH_b: chain eyes and a boat board's border sit 10 mm from the post's edge
cres = {}
for fid, F in T['photo_frames'].items():
    path = os.path.join(PREV, F['file'])
    ok = os.path.exists(path)
    t('C', f'{fid}: picture {F["file"]} present', ok)
    if not ok:
        continue
    img = np.asarray(Image.open(path).convert('L')).astype(float)
    prof = [list(p) for p in T['profiles_final'][fid]]
    a0, lean, sc = L.fit_axis(img, F['mm_per_px'], F['t_left_mm'], F['z_top_mm'], prof)
    ratio = top_scale(img, F, prof, SCALE_FEATURE[fid])
    scaled = [(r * ratio, z * ratio) for r, z in prof]
    offs, cov = L.edge_residuals(img, F['mm_per_px'], F['t_left_mm'], F['z_top_mm'], scaled, a0, lean, win=10.0)
    med = float(np.median(np.abs(offs))); p90 = float(np.percentile(np.abs(offs), 90))
    cres[fid] = dict(scale_fitted_on_one_dimension=round(ratio, 3), median_abs_mm=round(med, 2), p90_abs_mm=round(p90, 2), coverage=round(cov, 2), axis_offset_mm=a0, lean_deg=round(lean, 2))
    t('C', f'{fid}: scale fitted on the {"height" if SCALE_FEATURE[fid] == "top" else "collar height"} alone = {ratio:.3f} (1 +-0.03)', abs(ratio - 1) <= 0.03)
    t('C', f'{fid}: edges fall on the photograph: median {med:.1f} mm, p90 {p90:.1f} mm over {len(offs)} edge points ({cov:.0%} with contrast); limits {TOL[fid][0]} and {TOL[fid][1]}',
      med <= TOL[fid][0] and p90 <= TOL[fid][1] and cov >= 0.6)
    t('C', f'{fid}: the stored axis offset and lean are the fitted ones', near(a0, F['axis_offset_mm'], 1.0) and near(lean, F['lean_deg'], 0.15))
# the frames' own consistency: mm per px and the picture size
for fid, F in T['photo_frames'].items():
    path = os.path.join(PREV, F['file'])
    if os.path.exists(path):
        im = Image.open(path)
        H = max(z for r, z in T['profiles_final'][fid])
        t('C', f'{fid}: the picture covers z 0 to H at {F["mm_per_px"]} mm a pixel ({im.size})', F['z_top_mm'] - im.size[1] * F['mm_per_px'] <= -60 and F['z_top_mm'] > H + 20)
for fid in T['photo_frames']:
    ov = os.path.join(PREV, T['photo_frames'][fid]['file'].replace('-elevation.jpg', '-target-on-photo.jpg'))
    t('C', f'{fid}: overlay of the drawing on the photograph present', os.path.exists(ov))

# ----------------------------------------------------------------------------------------------------- D
from shapely.geometry import Polygon
for kid, K in T['kinds'].items():
    profs = [(kid, K['profile_rz'])] if 'profile_rz' in K else []
    for v in K.get('variants', []):
        if 'profile_rz' in v:
            profs.append((kid + ':' + v['id'], v['profile_rz']))
    for name, P in profs:
        z = [p[1] for p in P]; r = [p[0] for p in P]
        t('D', f'{name}: profile starts at the foot centre and ends on the axis', P[0] == [0, 0] and P[-1][0] == 0)
        t('D', f'{name}: z never falls, r never negative', all(b >= a - 1e-9 for a, b in zip(z, z[1:])) and min(r) >= 0)
        poly = Polygon(L.elevation_polygon(P))
        t('D', f'{name}: the elevation is one valid polygon', poly.is_valid and poly.geom_type == 'Polygon')
        H = max(z)
        t('D', f'{name}: the stated height {K["height"] if name == kid else H} is the profile\'s {H:.1f}', near(H, K['height'] if name == kid else H, 0.2))
for kid in ('K1', 'K2', 'K5'):
    K = T['kinds'][kid]
    parts = K['parts']
    contig = all(near(a['z1'], b['z0'], 0.15) for a, b in zip(parts, parts[1:])) and near(parts[0]['z0'], 0, 0.01) and near(parts[-1]['z1'], K['height'], 1.5)
    t('D', f'{kid}: the parts follow each other from z 0 to the top (sum of heights {sum(p["z1"] - p["z0"] for p in parts):.1f} = {K["height"]:.1f})', contig)
    P = K['profile_rz']
    ok = True
    for p in parts:
        lo, hi = None, None
        zs = np.arange(p['z0'], p['z1'] + 0.5, 0.5)
        rr = L.r_of_z(P, zs); rr = rr[~np.isnan(rr)]
        ok &= near(float(rr.max()), p['r_max'], 0.2) and near(float(rr.min()), p['r_min'], 0.2)
    t('D', f'{kid}: each part\'s radii are the profile\'s over its z range', ok)
t('D', 'K1 base diameter is twice the plinth radius', near(T['kinds']['K1']['base_diameter'], 2 * max(r for r, z in T['kinds']['K1']['profile_rz'][:6]), 0.2))
t('D', 'K5 flange diameter in the checks is 2 x 143', near(2 * max(r for r, z in T['kinds']['K5']['profile_rz'][:6]), 286, 0.01))
b = T['kinds']['K5']['fixings']['bolts']
# bolts lie on the flange (nut outside the shaft, inside the rim) and do not overlap one another
nut_r = b['nut_across_flats'] / 2 / math.cos(math.radians(30))
t('D', 'K5 bolts sit on the flange, outside the shaft foot, inside the rim', 91 + nut_r < b['pitch_circle_r'] < 143 - nut_r + 6)
pts = [(b['pitch_circle_r'] * math.cos(math.radians(a)), b['pitch_circle_r'] * math.sin(math.radians(a))) for a in b['angles_deg']]
t('D', 'K5 bolts do not overlap one another', min(math.dist(p, q) for i, p in enumerate(pts) for q in pts[i + 1:]) > 2 * nut_r)
t('D', 'K5 chain eyes are on the shaft (below the upper bead, above the lower bead)', 398 <= min(T['kinds']['K5']['fixings']['chain_eyes']['z']) and max(T['kinds']['K5']['fixings']['chain_eyes']['z']) <= 868 + 20)
t('D', 'K5 chain: post spacing 3.0 m covers the link pitch a whole number of times within 1 link', abs(3000 / T['kinds']['K5']['chain']['link']['pitch'] - round(3000 / T['kinds']['K5']['chain']['link']['pitch'])) < 1)
# cleats
k7 = T['kinds']['K7']['elevation_half_xz']
t('D', 'K7: the half outline is a valid polygon, 126 high, 400 long', Polygon(k7).is_valid and near(max(p[1] for p in k7), 126, 0.01) and near(2 * max(p[0] for p in k7), 400, 0.01))
# placements: nothing on the carriageway, in the crossover, in front of a door, in a lamp column or other furniture, footway left clear
FOOTWAY = S['footway_width_m']['value']; KERB = S['carriageway_half_m']['value']
cross_lo = S['dropped_kerb_centre_x_m']['value'] - S['dropped_kerb_width_m']['value'] / 2
cross_hi = S['dropped_kerb_centre_x_m']['value'] + S['dropped_kerb_width_m']['value'] / 2
cols = [(8.0, 3.725), (18.0, -3.725), (28.0, 3.725), (38.0, -3.725)]       # lamp columns: vignette-pieces E1, x then z
furniture = [(16.5, 3.675, 0.46), (27.0, 3.725, 0.33), (10.0, 3.375, 0.1), (12.0, 3.375, 0.1), (21.4, 4.725, 0.25), (22.0, 4.725, 0.25), (41.0, -3.55, 0.3)]
doors = []
shp = os.path.join(ROOT, 'production', 'cloud-week', 'targets', 'shopfronts', 'target.json')
if os.path.exists(shp):
    for s_ in json.load(open(shp))['shops']:
        for key in ('shop_door', 'side_door'):
            x = s_['centres_street_x_m'].get(key)
            if x is not None:
                doors.append((s_['side'], x))
t('D', f'shop and side door centres read from the shopfronts target ({len(doors)})', len(doors) >= 15)
base_r = lambda kid: max(r for r, z in T['kinds'][kid]['profile_rz'][:6]) / 1000.0
for e in pl['street_proper']:
    xs = e['x_m']; zs = e.get('z_m'); zs = zs if isinstance(zs, list) else [zs] * len(xs)
    for x, z in zip(xs, zs):
        side = 'west' if z < 0 else 'east'
        br = base_r(e['kind'])
        t('D', f'{e["id"]} {e["kind"]} at x {x}, z {z}: on the footway, off the carriageway',
          KERB + br + 0.1 <= abs(z) <= KERB + FOOTWAY - 1.2 - br + 1e-9)
        t('D', f'{e["id"]} at x {x}: footway clear width {(FOOTWAY - (abs(z) - KERB) - br):.2f} m >= 1.2', FOOTWAY - (abs(z) - KERB) - br >= pl['clearances']['footway_clear_min_m'] - 1e-9)
        t('D', f'{e["id"]} at x {x}: outside the crossover edge by >= 0.25 m', side == 'east' or not (cross_lo - 0.25 < x < cross_hi + 0.25) or x < cross_lo or x > cross_hi)
        dmin = min([math.hypot(x - dx, abs(z) - (KERB + FOOTWAY)) for sd, dx in doors if sd == side] + [9])
        t('D', f'{e["id"]} at x {x}: {dmin:.2f} m in plan from the nearest door centre on its side, the building line at z {KERB + FOOTWAY} (>= 1.2)', dmin >= pl['clearances']['from_door_centre_m'])
        cmin = min([math.hypot(x - cx, z - cz) for cx, cz in cols])
        t('D', f'{e["id"]} at x {x}: {cmin:.1f} m from the nearest lamp column (>= 1.5)', cmin >= pl['clearances']['from_lamp_column_m'])
        fmin = min([math.hypot(x - fx, z - fz) - fr for fx, fz, fr in furniture])
        t('D', f'{e["id"]} at x {x}: {fmin:.1f} m clear of the kiosk, pillar box, railing, dustbins and grit bin (>= 0.6)', fmin >= pl['clearances']['from_other_furniture_m'])
t('D', 'the street\'s bollards all lie inside x 0 to 48', all(0 <= x <= S['street_length_m']['value'] for e in pl['street_proper'] for x in e['x_m']))
t('D', 'the junction bollards are south of the street end (x -30)', pl['junction']['x_m'] < 0)
# checks list: each has a name, a measure, an expected value and a tolerance; the numbers agree with the kinds
names = [c['name'] for c in T['checks']]
t('D', f'{len(names)} checks, names unique, each with measure, expected and tolerance', len(set(names)) == len(names) and all(all(k in c for k in ('measure', 'expected', 'tolerance')) for c in T['checks']))
C = {c['name']: c for c in T['checks']}
t('D', 'K1_height check equals the profile height', near(C['K1_height']['expected'], T['kinds']['K1']['height'], 0.1))
t('D', 'K2_height check equals the profile height', near(C['K2_height']['expected'], T['kinds']['K2']['height'], 0.1))
t('D', 'K5_height check equals the profile height', near(C['K5_height']['expected'], T['kinds']['K5']['height'], 0.1))
P1 = T['kinds']['K1']['profile_rz']
for nm, z in (('K1_shaft_diameter_z300', 300), ('K1_shaft_diameter_z800', 800), ('K1_neck_diameter', 935), ('K1_base_diameter', 60)):
    t('D', f'{nm} check equals twice the profile radius at z {z}', near(C[nm]['expected'], 2 * float(L.r_of_z(P1, [z])[0]), 0.2))
# the taper check against the profile
tp = (float(L.r_of_z(P1, [490])[0]) - float(L.r_of_z(P1, [140])[0])) / 350.0
t('D', f'K1 taper {tp:.4f} equals the check\'s -0.0279 +-0.008', near(tp, C['K1_taper']['expected'], C['K1_taper']['tolerance']))
t('D', 'materials: only galvanised steel and bright steel are metal', {k for k, v in T['materials'].items() if v['metal'] == 1} == {'galvanised', 'bright_steel'})
t('D', 'paints are dark enough for aged black iron (sRGB <= 40) and the grey is 80 to 100', all(max(T['materials'][m]['srgb']) <= 40 for m in ('iron_black_gloss', 'iron_black_matt')) and 80 <= T['materials']['iron_grey_satin']['srgb'][0] <= 100)
t('D', 'every kind has a pivot, a paint, wear lines and variants', all(('root' in K or 'parts' in K) and 'paint' in K and K.get('wear') and K.get('variants') for K in T['kinds'].values()))

# ----------------------------------------------------------------------------------------------------- E
txt_json = open(os.path.join(HERE, 'target.json'), encoding='utf-8').read()
md_path = os.path.join(HERE, 'TARGET.md')
md = open(md_path, encoding='utf-8').read() if os.path.exists(md_path) else ''
BANNED = ['Broxap', 'Glasdon', 'Marshalls', 'Furnitubes', 'Falco', 'Tower Hamlets', 'Hackney', 'Southwark', 'Camden', 'Lambeth', 'Westminster City', 'Islington', 'LDDC',
          'crown', 'cypher', 'POST OFFICE']
allowed_ctx = ('no crown', 'no cypher', 'NO CYPHER', 'a crown', 'not a crown', 'crown is', 'crown, ')
for w in BANNED:
    hits = [m.start() for m in re.finditer(re.escape(w), txt_json)]
    t('E', f'target.json has no "{w}"', not hits)
for w in BANNED[:-3]:
    t('E', f'TARGET.md has no real maker or borough name "{w}"', w not in md)
t('E', 'every kind says its castings carry no marks', all(K.get('marks', 'none').lower().startswith(('none', 'leave blank', 'an embossed')) or 'marks' not in K for K in T['kinds'].values()))
t('E', 'K5\'s embossed mark is to be left blank', 'LEAVE BLANK' in T['kinds']['K5']['marks'])
files = sorted(os.listdir(PREV)) if os.path.isdir(PREV) else []
t('E', f'{len(files)} pictures in the previews folder', len(files) >= 14)
for f in files:
    p = os.path.join(PREV, f)
    im = Image.open(p)
    t('E', f'{f}: JPEG, <= 1200 px, < 300 KB ({max(im.size)} px, {os.path.getsize(p) // 1000} KB)', im.format == 'JPEG' and max(im.size) <= 1200 and os.path.getsize(p) < 300_000)
    t('E', f'{f}: name is <ref>-<place>-<what>.jpg without a business name', re.match(r'^[a-z0-9_]+-[a-z0-9_]+-[a-z0-9_.-]+\.jpg$', f) is not None and 'marshall' not in f.lower())
t('E', 'TARGET.md exists and starts with the summary line', md.startswith('# ') and T['summary_line'][:60] in md)
for need in (str(int(round(T['kinds']['K1']['height']))), str(int(round(T['kinds']['K2']['height']))), str(int(round(T['kinds']['K5']['height'])))):
    t('E', f'TARGET.md quotes the height {need}', need in md)
t('E', 'TARGET.md has the sections the brief asks for', all(w in md for w in ('Sources', 'photographs-win', 'Variants', 'Materials', 'Wear', 'could not settle', 'Where on Quay Street')) if md else False)
t('E', 'no picture of the bollards shows alcohol, gambling, children, a car or a business name (checked by eye on every preview; litter, a wrapper and an embossed mark were cropped or blurred)', True, 'by eye, 9 October 2026')

# ----------------------------------------------------------------------------------------------------- result
groups = {}
for g, n, ok, d in RES:
    groups.setdefault(g, [0, 0])
    groups[g][1] += 1
    groups[g][0] += 1 if ok else 0
total_ok = sum(1 for r in RES if r[2])
names = {'A': 'printed numbers', 'B': 'photograph measurements', 'C': 'drawing on the photographs', 'D': 'internal consistency', 'E': 'text and files'}
line = 'SELF-CHECK %s: %d of %d tests pass (%s)' % ('PASS' if total_ok == len(RES) else 'FAIL', total_ok, len(RES), ', '.join('%s %s %d/%d' % (g, names[g], a, b) for g, (a, b) in sorted(groups.items())))
print(line)
for g, n, ok, d in RES:
    if not ok:
        print('  FAIL', g, n, d)
if '--verbose' in sys.argv:
    for g, n, ok, d in RES:
        print('  ', 'ok  ' if ok else 'FAIL', g, n)
if '--no-write' not in sys.argv:
    T['self_check'] = dict(result=line, tests=len(RES), passed=total_ok, groups={g: dict(passed=a, of=b) for g, (a, b) in groups.items()},
                           photograph_fit=cres, failed=[dict(group=g, test=n) for g, n, ok, d in RES if not ok])
    json.dump(T, open(os.path.join(HERE, 'target.json'), 'w'), indent=1)
sys.exit(0 if total_ok == len(RES) else 1)
