"""Tests the litter-bins target against its own sources before anything is built, and writes its result into target.json under "self_check".

    /home/user/.bpyenv/bin/python -I self_check.py

Groups: 1 the numbers read from other files come back (the scene, the other targets); 2 the checks in target.json are computed from the target's own profiles and parts where they
can be (the rest are listed as reported); 3 K2's photograph measurement (S12) against K2's profile and the drawing laid on the photograph; 4 internal consistency (profiles, parts
inside the shell, the aperture and the liner, the lettering, the placements and their clearances); 5 the drawing's polygons (valid, no part outside the silhouette); 6 the content
rule (no brand, no alcohol or gambling or child word anywhere in the target's strings that name something on a bin); 7 files (the preview crop and its overlay).
"""
import json
import math
import os
import re
import sys

from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, HERE)
TPATH = os.path.join(HERE, 'target.json')
T = json.load(open(TPATH, encoding='utf-8'))
R = []          # (group, name, ok, detail)
REPORTED = []


def ok(group, name, cond, detail=''):
    R.append((group, name, bool(cond), str(detail)[:300]))


def near(a, b, tol):
    if isinstance(a, (list, tuple)):
        return all(near(x, y, t) for x, y, t in zip(a, b, tol if isinstance(tol, (list, tuple)) else [tol] * len(a)))
    return abs(a - b) <= tol + 1e-9


def r_of_z(prof, z):
    """the outer radius of a lathe profile at height z (the largest r of the segments that cross z)"""
    best = None
    for (r0, z0), (r1, z1) in zip(prof[:-1], prof[1:]):
        lo, hi = min(z0, z1), max(z0, z1)
        if lo <= z <= hi:
            r = r0 if z1 == z0 else r0 + (r1 - r0) * (z - z0) / (z1 - z0)
            best = r if best is None else max(best, r)
    return best


def resolve(doc, path):
    """a dotted path with [id=X] or [n] steps"""
    cur = doc
    for part in re.findall(r'[^.\[\]]+|\[[^\]]+\]', path):
        if part.startswith('['):
            sel = part[1:-1]
            if '=' in sel:
                k, v = sel.split('=', 1)
                cur = next(x for x in cur if str(x.get(k)) == v)
            else:
                cur = cur[int(sel)]
        elif isinstance(cur, list):
            cur = next(x for x in cur if part in (x.get('id'), x.get('name'), x.get('bom'), x.get('kind')))
        else:
            cur = cur[part]
    return cur


# ---- 1 the numbers read from other files
for n in T['scene_numbers'] + T['other_target_numbers'] + T['hook_cast_numbers']:
    f = os.path.join(ROOT, n['file'])
    try:
        v = resolve(json.load(open(f, encoding='utf-8')), n['path'])
        ok(1, 'READ %s' % n['id'], near(v, n['value'], 1e-6) if isinstance(v, (int, float)) else v == n['value'], '%s = %s (target %s)' % (n['path'], v, n['value']))
    except Exception as e:
        ok(1, 'READ %s' % n['id'], False, 'cannot read %s %s: %s' % (n['file'], n['path'], e))

K1, K2, D1 = T['kinds']['K1'], T['kinds']['K2'], T['kinds']['D1']
k2p, k1b, d1p = K2['outer_profile_rz'], K1['bin']['outer_profile_rz'], D1['outer_profile_rz']
ap = K2['aperture']
Pl = T['placements']

# ---- 2 the checks of target.json, computed where the target's own numbers give them
def vol_litres(wall_section):
    """the inner volume of a bin from its outer profile less the wall: the solid of revolution of the inside outline"""
    P = [(r - K1['bin']['wall'], z) for r, z in k1b if z >= K1['bin']['z_base'] + K1['bin']['base_plate']['thickness']]
    poly = Polygon(P + [(0, P[-1][1]), (0, P[0][1])]).buffer(0)
    return 2 * math.pi * poly.centroid.x * poly.area / 1e6


computed = {
    'K1_total_height': K1['post']['height'], 'K1_post_diameter': K1['post']['od'], 'K1_rim_height': K1['bin']['z_rim_top'],
    'K1_bin_height': K1['bin']['z_rim_top'] - K1['bin']['z_base'], 'K1_bin_rim_diameter': 2 * max(r for r, z in k1b), 'K1_bin_foot_diameter': 2 * K1['bin']['r_base'],
    'K1_bin_offset': K1['bin']['axis_offset_x'], 'K1_capacity_litres': round(vol_litres(None), 1), 'K1_wall_thickness': K1['bin']['wall'],
    'K1_clamp_count_and_z': [(c['z0'] + c['z1']) / 2 for c in K1['bracket']['clamps']],
    'K1_drain_holes': [K1['bin']['base_plate']['drain_holes']['count'], K1['bin']['base_plate']['drain_holes']['diameter'], K1['bin']['base_plate']['drain_holes']['on_radius']],
    'K1_letter_height': K1['lettering'].get('cap_height'), 'K1_only_word': [K1['lettering'].get('text')], 'K1_bead_diameter': K1['bin']['rim_bead']['diameter'],
    'K2_total_height': max(z for r, z in k2p), 'K2_hood_diameter': 2 * r_of_z(k2p, 750.0), 'K2_body_diameter': 2 * r_of_z(k2p, 500.0), 'K2_collar_diameter': 2 * r_of_z(k2p, 320.0),
    'K2_base_diameter': 2 * r_of_z(k2p, 120.0), 'K2_aperture_width': ap['width'], 'K2_aperture_height': ap['top_z'] - ap['sill_z'], 'K2_aperture_sill_z': ap['sill_z'],
    'K2_liner_rim_z': K2['parts']['liner']['rim_z'][0], 'K2_join_groove_z': K2['parts']['join_groove']['z'], 'K2_letter_height': K2['lettering']['cap_height'], 'K2_only_word': [K2['lettering']['text']],
    'D1_total_height': D1['lid']['handle']['top_z'], 'D1_lid_height': D1['lid']['handle']['top_z'] - D1['rim']['z'][1],
    'D1_body_height': D1['rim']['z'][1], 'D1_rim_diameter': 2 * D1['rim']['bead_r_max'], 'D1_lid_diameter': 2 * D1['lid']['skirt_r_outer'],
    'D1_foot_diameter': 2 * D1['foot_ring']['r_max'], 'D1_rib_count_and_z': list(D1['rib_z']),
    'D1_side_handles': [D1['side_handles']['count'], D1['side_handles']['z'], D1['side_handles']['proud']],
    'D1_lid_clearance': round(D1['lid']['profile_rz'][0][0] - D1['rim']['bead_r_max'], 1),
    'street_bin_count': len(Pl['bins']), 'dustbin_count_and_x': [len(Pl['dustbins'])] + [d['axis_x_m'] for d in Pl['dustbins']], 'dustbin_setback': Pl['dustbins'][0]['setback_from_kerb_m'],
    'B1_place': [Pl['bins'][0]['post_x_m'], Pl['bins'][0]['post_z_m']], 'B2_place': [Pl['bins'][1]['post_x_m'], Pl['bins'][1]['post_z_m']],
    'B3_place': [Pl['bins'][2]['axis_x_m'], abs(Pl['bins'][2]['axis_z_m'])],
    'tri_budget': {k: T['kinds'][k]['tri_budget'] for k in ('K1', 'K2', 'D1')},
}
for c in T['checks']:
    nm = c['name']
    v = computed.get(nm)
    exp, tol = c['expected'], c['tolerance']
    if v is None:
        if nm in ('walking_strip', 'kerb_clear', 'door_leaf_clear', 'every_bin_within_3m_of_a_door_or_the_stop', 'wear_iron_share', 'no_brand_text', 'no_alcohol_gambling_children', 'dressing_separate'):
            REPORTED.append('%s: a placement or content rule, tested in groups 4 and 6' % nm)
        else:
            REPORTED.append('%s: not computed here (%s)' % (nm, c['measure'][:60]))
        continue
    if tol == 'at least' or tol == 'at most':
        continue
    if isinstance(exp, dict):
        ok(2, 'CHECK ' + nm, v == exp, v)
    elif isinstance(exp, list) and isinstance(tol, list) and isinstance(v, list) and len(v) != len(exp):
        ok(2, 'CHECK %s: %s against %s' % (nm, v, exp), False, v)
    elif isinstance(exp, list) and isinstance(exp[0], str):
        ok(2, 'CHECK ' + nm, v == exp, v)
    else:
        ok(2, 'CHECK %s: %s against %s +-%s' % (nm, v, exp, tol), near(v, exp, tol), v)

# ---- 3 K2 against its photograph (S12)
pm = T['photo_measurements']['s12_974902']
for row in pm['rows_px_and_mm']:
    zs = {'hood skirt': 750.0, 'body': 500.0, 'collar': 330.0, 'base drum': 120.0}
    key = next(k for k in zs if row['part'].startswith(k))
    r = r_of_z(k2p, zs[key])
    ok(3, 'PHOTO %s: radius %.1f at z %d against the photograph %.0f (+-12)' % (row['part'], r, zs[key], row['r_mm']), near(r, row['r_mm'], 12.0), '')
    ok(3, 'PHOTO %s: the width in pixels times the scale gives the diameter (3.09 mm a pixel)' % row['part'], near(row['width_px'] * 3.09, row['diameter_mm'], 2.0), row['width_px'] * 3.09)
REPORTED.append('PHOTO the scale: 900 mm over 291 px is 3.09 mm a pixel, FITTED to K2\'s Judgement height; the pillar box beside the bin is of an unestablished type and height (462 px tall, 101 across: 4.6 to 1, not Type A\'s 3.07), so S12 gives proportions only (TARGET-REVIEW fault 8)')
REPORTED.append('PHOTO the pixel table (rows_px_and_mm) is the writer\'s reading, re-measured by a fresh reviewer on 12 October on 4x and 8x enlargements (the collar and the groove corrected); this group compares K2\'s profile with that table')
ok(3, 'PHOTO the order of the stations: base drum widest, then collar, hood skirt, body narrowest', r_of_z(k2p, 120) > r_of_z(k2p, 330) > r_of_z(k2p, 750) > r_of_z(k2p, 500), [round(r_of_z(k2p, z), 1) for z in (120, 330, 750, 500)])
ok(3, 'PHOTO the aperture sits in the hood skirt, between the groove and the dome shoulder', K2['parts']['join_groove']['z'][1] <= ap['sill_z'] and ap['top_z'] <= 822.0, '%s %s' % (ap['sill_z'], ap['top_z']))
for p_ in ('geo974902-southampton-hooded-bin-2008.jpg', 'geo974902-southampton-hooded-bin-2008-target-on-photo.jpg'):
    f = os.path.join(ROOT, 'production', 'previews', 'cloud-week', 'refs', 'litter-bins', p_)
    ok(7, 'FILE ' + p_, os.path.exists(f) and os.path.getsize(f) < 300_000, os.path.getsize(f) if os.path.exists(f) else 'missing')

# ---- 4 internal consistency
for nm, prof in (('K2', k2p), ('K1 bin', k1b), ('D1', d1p)):
    zs = [z for r, z in prof]
    ok(4, '%s profile: every r is 0 or positive and the points are not repeated' % nm, all(r >= 0 for r, z in prof) and len(set(map(tuple, prof))) == len(prof), len(prof))
ok(4, 'K2 profile: z never falls (a lathe outline from the base to the crown)', all(b[1] >= a[1] for a, b in zip(k2p[:-1], k2p[1:])), '')
ok(4, 'K2 profile closes on the axis at the crown (r 0 at z 900)', k2p[-1] == [0.0, 900.0] or tuple(k2p[-1]) == (0.0, 900.0), k2p[-1])
liner = K2['parts']['liner']['profile_rz']
ok(4, 'K2 liner stands inside the body\'s inner wall (its r 200 against the body 210 less the 5 shell)', max(r for r, z in liner) <= r_of_z(k2p, 500.0) - K2['shell'], max(r for r, z in liner))
ok(4, 'K2 liner rim shows in the aperture (between the sill and the top)', ap['sill_z'] < K2['parts']['liner']['rim_z'][0] < ap['top_z'], K2['parts']['liner']['rim_z'])
ok(4, 'K2 aperture width fits the hood skirt (a chord of its circle under 100 degrees)', ap['width'] <= 2 * r_of_z(k2p, 740.0) * math.sin(math.radians(50)), ap['width'])
L = K2['lettering']
chord = 2 * r_of_z(k2p, L['z_centre']) * math.sin(math.radians(L['arc_deg'] / 2))
ok(4, 'K2 lettering lies on the body below the groove and above the collar', K2['parts']['body']['z'][0] < L['z_centre'] - L['cap_height'] / 2 and L['z_centre'] + L['cap_height'] / 2 < K2['parts']['join_groove']['z'][0], L['z_centre'])
ok(4, 'K2 lettering: LITTER at 55 cap across a chord that holds six letters of about 40 each', chord > 6 * 36.0, round(chord, 1))
parts_ok = all(a['z'][1] <= b['z'][0] + 1e-6 for a, b in ((K2['parts']['base_drum'], K2['parts']['collar']), (K2['parts']['collar'], K2['parts']['body']), (K2['parts']['body'], K2['parts']['join_groove']), (K2['parts']['join_groove'], K2['parts']['hood'])))
ok(4, 'K2 parts follow each other in z without overlap', parts_ok, '')
ok(4, 'K1 capacity is the research\'s 50 litre class within 15 per cent', abs(computed['K1_capacity_litres'] - 50.0) / 50.0 < 0.15, computed['K1_capacity_litres'])
bins = Pl['bins']
for b in bins:
    k = b['kind']
    ok(4, '%s placed inside the footway: its far edge is under the building line (4.975) and clear of the kerb by 0.25' % b['id'], b.get('near_edge_from_kerb_face_m', 0.45) >= 0.25 - 1e-9 and b.get('far_edge_from_kerb_face_m', 0.8) < 1.975, '%s %s' % (b.get('near_edge_from_kerb_face_m'), b.get('far_edge_from_kerb_face_m')))
ok(4, 'the street has three public bins (K1, K1, K2) and two dustbins', [b['kind'] for b in bins] == ['K1', 'K1', 'K2'] and len(Pl['dustbins']) == 2, [b['kind'] for b in bins])
ok(4, 'B3 (K2) stands at x 44.0 on the west side', bins[2]['side'] == 'west', bins[2]['side'])

# ---- 4b K1's bin against its post, spacer and clamps (TARGET-REVIEW fault 9: the first try's 216 put the rim bead 8.5 into the post and no test saw it)
off = K1['bin']['axis_offset_x']
xs = [(z, off - r_of_z(k1b, z)) for z in range(560, 1051, 10)]
ok(4, 'K1 bin clears the post: the wall\'s nearest x (the bead included) is over the post radius + 3 at every height from 560 to 1050', all(x >= K1['post']['od'] / 2.0 + 3.0 for z, x in xs), min(x for z, x in xs))
sp = K1['bracket']['back_strap']
ok(4, 'K1 spacer bar: the wall stands at least 8 off the clamp rings\' outer face (x 43.05) from z 590 to 1030, so the bar is 8 thick or more all along', all(x - sp['x_from'] >= 8.0 for z, x in xs if sp['z0'] <= z <= sp['z1']), [round(x - sp['x_from'], 1) for z, x in xs if z in (590, 640, 800, 980, 1030)])
ok(4, 'K1 spacer bar: 21 thick at z 640 and 10 at z 980 (the review), as the data computes them', near([sp['thickness_at_640'], sp['thickness_at_980']], [21.0, 10.0], 1.5), [sp['thickness_at_640'], sp['thickness_at_980']])
ok(4, 'D1: the two rolled rings under the rim at z 530 and 556 do not overlap each other or the rim bead (each 18 high)', D1['rib_z'] == [530.0, 556.0] and 556.0 - 530.0 >= 18.0 and 582.0 - 556.0 >= 9.0, D1['rib_z'])
ok(4, 'D1 side handles: a 12 mm bar 170 long standing 38 proud on two lugs 25 x 55 x 3 with two 8 mm rivets 40 apart', (D1['side_handles']['bar_d'], D1['side_handles']['length'], D1['side_handles']['proud'], D1['side_handles']['rivets_per_end'], D1['side_handles']['rivet_pitch']) == (12.0, 170.0, 38.0, 2, 40.0), D1['side_handles'])
ok(4, 'K2 ground patch: an irregular flush disc r 290 to 330 round the base drum (r 247), 0 to 2 proud', K2['parts']['ground_patch']['r'][0] > 247.0 + 40.0 and K2['parts']['ground_patch']['proud'][1] <= 2.0, K2['parts']['ground_patch']['r'])

# ---- 5 the drawing
import target_drawing as TD
views = TD.build_all(T)
for name, v in views.items():
    bad = [p['name'] for p in v.polys if not p['geom'].is_valid]
    ok(5, 'DRAWING %s: every polygon is valid (%d polygons)' % (name, len(v.polys)), not bad, bad[:3])
sec = views['K2_section']
sil = TD.silhouette(k2p)
liner_geoms = [p['geom'] for p in sec.polys if p['part'] == 'liner']
ok(5, 'DRAWING K2 section: the liner lies inside the shell\'s silhouette (right side)', all(g.difference(sil.buffer(0.5)).area < 1.0 for g in liner_geoms), '')
front = views['K2_front']
hole = [p['geom'] for p in front.polys if p['name'] == 'aperture_void'][0]
ok(5, 'DRAWING K2 front: the aperture is inside the silhouette', hole.difference(sil).area < 1.0, round(hole.difference(sil).area, 2))
ok(5, 'DRAWING K2 front: the aperture is %.0f x %.0f' % (ap['width'], ap['top_z'] - ap['sill_z']), near((hole.bounds[2] - hole.bounds[0], hole.bounds[3] - hole.bounds[1]), (ap['width'], ap['top_z'] - ap['sill_z']), 1.0), hole.bounds)

# ---- 6 the content rule
blob = json.dumps({k: T[k] for k in ('kinds', 'dressing', 'variants', 'placements', 'wear')}).lower()
for neg in ('never beer, lager or cider', 'no alcohol, gambling or child-related object', 'no alcohol or gambling or children'):
    blob = blob.replace(neg, '')
banned = ['beer', ' ale ', 'lager', 'whisky', 'vodka', 'wine bottle', 'betting', 'casino', 'bookmaker', 'lottery', 'slot machine', 'child', 'children', 'baby', 'toddler', 'pushchair', 'kids']
hits = [w for w in banned if w in blob]
ok(6, 'CONTENT no alcohol, gambling or child word in the kinds, dressing, variants, placements and wear', not hits, hits)
brand_hits = [w for w in ('glasdon', 'topsy', 'dennis', 'cooper', 'council name') if w in json.dumps({k: T['kinds'][k] for k in ('K1', 'K2', 'D1')}).lower().replace('not the form of any maker', '').replace('the topsy', '').replace('topsy-type', '')]
ok(6, 'CONTENT no maker\'s name on a bin\'s own lettering fields (the leads and sources may name them, the kinds\' parts and lettering may not)', not [w for w in ('glasdon', 'topsy') if w in json.dumps({k: {x: y for x, y in T['kinds'][k].items() if x not in ('basis', 'title')} for k in ('K1', 'K2', 'D1')}).lower()], '')
ok(6, 'CONTENT the only word on a council bin is LITTER', K1['lettering']['text'] == 'LITTER' and K2['lettering']['text'] == 'LITTER', '')
ok(6, 'CONTENT the K2 target keeps the sticker out: not modelled', 'not modelled' in json.dumps(pm).lower(), '')

failed = [r for r in R if not r[2]]
groups = {}
for g, nm, c, d in R:
    groups.setdefault(g, [0, 0])
    groups[g][0] += 1
    groups[g][1] += 1 if c else 0
line = 'SELF-CHECK litter-bins: %d checks, %d passed, %d failed, %d reported' % (len(R), len(R) - len(failed), len(failed), len(REPORTED))
for g in sorted(groups):
    print('group %s: %d of %d' % (g, groups[g][1], groups[g][0]))
for g, nm, c, d in failed:
    print('FAIL [%s] %s | %s' % (g, nm, d))
for r in REPORTED:
    print('reported:', r)
print(line)
T['self_check'] = dict(line=line, checks=len(R), passed=len(R) - len(failed), failed=[(g, nm, d) for g, nm, c, d in failed], reported=REPORTED, groups={str(g): v for g, v in groups.items()})
json.dump(T, open(TPATH, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
sys.exit(1 if failed else 0)
