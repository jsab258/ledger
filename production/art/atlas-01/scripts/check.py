"""The adopted atlas's invariants. Arithmetic/2D checks only, never a game or Blender run.

Adopted 2026-10-06 (ADOPTED-2026-10-06.md). The branch's checks of the earlier Mickey's fit-out
(furniture clearances, stairs, sightline, door widths) went with their data. Added: the map follows
the built street (vignette-scene.json, terrace-front.py's road on), no new route crossing, and the
content rule (canon D18) over every adopted text file.

    python production/art/atlas-01/scripts/check.py [--out DIR]   # DIR: rendered SVGs to parse
"""
from pathlib import Path
import json, math, re, sys, xml.etree.ElementTree as ET
R = Path(__file__).resolve().parents[1]; REPO = R.parents[2]
A = json.loads((R/'data/atlas.json').read_text())
B = json.loads((REPO/'production/specs/vignette-bill-of-materials.json').read_text(encoding='utf-8'))
P = json.loads((REPO/'production/specs/vignette-pieces.json').read_text(encoding='utf-8'))
S = json.loads((REPO/'production/specs/vignette-scene.json').read_text(encoding='utf-8'))
TF = (REPO/'tools/art-recipes/terrace-front.py').read_text(encoding='utf-8')
ARCHIVE = Path('F:/LedgerTools/atlas-01-2026-09-22')
OUT = Path(sys.argv[sys.argv.index('--out')+1]) if '--out' in sys.argv else Path('F:/LedgerTools/atlas-01-2026-10-06')
checks = []; skipped = []
def check(name, condition):
    assert condition, name
    checks.append(name)
def intersects(a, b, r):
    x, y, w, h = r; t0 = 0; t1 = 1; dx = b[0]-a[0]; dy = b[1]-a[1]
    for p, q in [(-dx, a[0]-x), (dx, x+w-a[0]), (-dy, a[1]-y), (dy, y+h-a[1])]:
        if p == 0:
            if q < 0: return False
        else:
            t = q/p
            if p < 0: t0 = max(t0, t)
            else: t1 = min(t1, t)
            if t0 > t1: return False
    return True
def expanded(b, m): x, y, w, h = b; return [x-m, y-m, w+2*m, h+2*m]
def segments(ps): return list(zip(ps, ps[1:]))
def cross(a, b, c, d):
    """Proper crossing of segments ab and cd (touching at an end or a shared vertex is not one)."""
    def o(p, q, r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    d1, d2, d3, d4 = o(c, d, a), o(c, d, b), o(a, b, c), o(a, b, d)
    return d1*d2 < 0 and d3*d4 < 0
def inside(pt, poly):
    x, y = pt; n = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:]+poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1+(y-y1)*(x2-x1)/(y2-y1): n = not n
    return n
def const(name):
    m = re.search(r'^%s\s*=\s*(.+?)\s*(#.*)?$' % name, TF, re.M); assert m, name
    return eval(m.group(1), {})

byname = {p['name']: p for p in P['pieces']}
SA = A['street_anchor']; AP = SA['approach']
mick = byname[SA['mickeys_piece']]
check('Owner base and the source Mickey\'s shell retained', A['base_commit'] == '7722b45cb3dcee2fbcee26675fae4fef641cbba7'
      and [mick[k] for k in ['x_m', 'y_m', 'z_m', 'sx_m', 'sy_m', 'sz_m']] == [6, 3.2, 9.125, 6, 6.2, 8])
check('Street length and widths agree with the built street (48 m, 6 m road)',
      SA['length_m'] == S['street']['length_m'] == 48 and S['street']['carriageway']['half_width_m']*2 == SA['carriageway_m'] == 6)
ch = next(b for b in S['blocks'] if b['id'] == 'east_chandler')
check('The chandler\'s stands where the built street has it', SA['chandler_piece'] in byname
      and SA['chandler_x_range'] == [ch['start_x_m'], ch['start_x_m']+ch['bay_width_m']*ch['bays']])

# THE ROAD ON, read from terrace-front.py itself, not from this file's own copy.
X0, X1 = const('APPROACH_X'); XF = const('APPROACH_FLAT_TO_X'); CL = const('APPROACH_CLIMB')
BX0, BX1 = const('APPROACH_BEND_X'); BY = const('APPROACH_BEND_Y'); OX = const('APPROACH_OPEN_X')
DM = const('APPROACH_DRIFT_M'); SIDE = const('APPROACH_BEND_SIDE')
def z(x): return 0.0 if x <= XF else (min(x, BX0)-XF)*CL
def drift(x): t = min(1.0, max(0.0, (x-XF)/(BX0-XF))); return SIDE*DM*t*t
def at(x): return [round(400+drift(x), 3), round(350+x, 3)]
check('The approach record matches terrace-front.py', AP['level_x'] == [X0, XF] and AP['climb_x'] == [XF, BX0]
      and AP['bend_x'] == [BX0, BX1] and AP['open_ground_x'] == [OX[0], OX[1]] and math.isclose(CL, 1/12))
quay = next(r for r in A['routes'] if r['id'] == 'quay')['points']
need = [at(x) for x in (X0, XF, 57.0, 62.0, 67.0, BX0)]
check('Quay Street runs north to 48 m, level to 52 m, then climbs and drifts with the built road',
      all(p in quay for p in need) and quay.index(need[0]) < quay.index(need[-1]))
corner = AP['atlas_points']['bend_square']; nxt = quay[quay.index(corner)+1]
check('The bend sits at x 72 to 80 and turns the way the built bend turns (APPROACH_BEND_SIDE)',
      350+BX0 <= corner[1] <= 350+BX1 and nxt[1] == corner[1] and (nxt[0]-corner[0])*SIDE > 0 and nxt[0]-400 <= BY[1])
check('Spot heights follow approach_z on the atlas datum (height = y + 4.0)',
      all(math.isclose(sp['height'], round(4.0+z(sp['point'][1]-350), 2), abs_tol=0.01) for sp in AP['spot_heights_m'][:4])
      and math.isclose(AP['spot_heights_m'][4]['height'], round(4.0+z(BX0)+0.15, 2)))
hook = next(d for d in A['districts'] if d['id'] == 'hook')['polygon']
check('The street, its climb and its bend stay in the Hook', all(inside(p, hook) for p in need+[corner, nxt]))
check('Seven canonical districts, unique authored IDs', len(A['districts']) == 7
      and set(d['id'] for d in A['districts']) == {'hook', 'copper', 'exchange', 'parade', 'fairview', 'ironside', 'gullwing'})
check('Each district has a named information venue', all(any(l['district'] == d['id'] and l['venue'] for l in A['landmarks']) for d in A['districts']))
check('Mickey\'s is the cab office (canon D19)', next(l for l in A['landmarks'] if l['id'] == 'H1')['type'] == 'cab office')
check('Map streets clear authored massing by 5m half-corridor', not any(intersects(p, q, expanded(b[1:], 5))
      for b in A['blocks'] for r in A['routes']+[A['rail']] for p, q in segments(r['points'])))
new_q = segments(quay[quay.index(need[0])-1:])
others = [(r.get('id', 'rail'), s) for r in A['routes']+[A['rail']] if r.get('id') != 'quay' for s in segments(r['points'])]
check('Quay Street\'s new line crosses no other route or the rail', not any(cross(a, b, c, d) for a, b in new_q for _, (c, d) in others))
check('Every flow and daily route still walks the network to Mickey\'s', all(
      f['points'][-2:] == [[400, 356], [405.125, 356]] for f in [A['gameplay']['daily'][0], A['working_town']['flows'][0]]))

# CONTENT RULE (canon D18): no alcohol, gambling or children in any adopted text file.
WORDS = re.compile(r'\bpubs?\b|\bbars?\b|beer|\bales?\b|lager|\bwine|spirits|whisk|\bcask|betting|bookmaker|bingo|gambl|'
                   r'off-licen|fruit machine|arcade|\bclubs?\b|\bdrink|school|playground|child|\bkids?\b|\bpram|_PUB_', re.I)
EXEMPT = {'ADOPTED-2026-10-06.md', 'check.py', 'verification.json', 'REVIEW.md'}
texts = [p for p in R.rglob('*') if p.is_file() and p.suffix in ('.md', '.json', '.py') and p.name not in EXEMPT]
hits = [(p.name, m.group(0)) for p in texts
        for m in WORDS.finditer(p.read_text(encoding='utf-8').replace('D8-visual-bar.md', ''))]   # a decision record's file name
check('No alcohol, gambling or children in %d adopted text files' % len(texts), not hits)

audit = json.loads((R/'data/assets.json').read_text(encoding='utf-8')); ids = {x['id'] for x in B['items']}
audited = {x['id'] for x in audit['items'] if x['id_kind'] == 'existing BOM'}
check('All 77 audited BOM lines still exist in the BOM', len(audited) == 77 and audited <= ids)
check('New IDs are separate and all related BOM IDs resolve', all(x['id'] not in ids and all(y in ids for y in x['related_existing_bom_ids'])
      for x in audit['items'] if x['id_kind'] != 'existing BOM'))
if ARCHIVE.is_dir():
    check('Every picture the audit names is in the F: archive', all((ARCHIVE/x['thumbnail']).is_file() for x in audit['items'] if x['thumbnail']))
    check('Seven district concept files are in the F: archive', all((ARCHIVE/'concepts'/f'{d["id"]}.png').is_file() for d in A['districts']))
else:
    skipped.append('pictures: archive %s not reachable' % ARCHIVE)
svgs = sorted(OUT.glob('*.svg')) if OUT.is_dir() else []
for f in svgs:
    seen = [x.attrib['id'] for x in ET.parse(f).iter() if 'id' in x.attrib]
    check(f.name+' parses with unique SVG IDs', len(seen) == len(set(seen)))
if not svgs: skipped.append('SVGs: none in %s' % OUT)
for f in (R/'scripts').glob('*.py'): compile(f.read_text(encoding='utf-8'), str(f), 'exec')
check('All adopted Python sources compile', True)
report = {'kind': 'local arithmetic, source checks and SVG parsing; NOT runtime tests', 'passed': checks, 'count': len(checks),
          'skipped': skipped, 'bom_ids_not_audited': sorted(ids-audited),
          'bounds': 'Map-scale 2D checks. Routes, sightlines and timings are design intentions, not simulation results.'}
(R/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
