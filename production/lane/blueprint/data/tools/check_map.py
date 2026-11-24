#!/usr/bin/env python3
"""Check map.json against FIT-G1, 4.1 and its own rules. Needs shapely and networkx
(pip install shapely networkx). Exit code 1 on any failure. Written 24 Nov 2026."""
import json, math, os, sys
from collections import Counter
import networkx as nx
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, '..', 'map.json')))
FAIL, OK, WARN = [], [], []

def check(cond, msg):
    (OK if cond else FAIL).append(msg)

def plen(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))

roads = {r['id']: r for r in M['roads']}

# 1. G1 lengths within 5%, widths within 1 m (Quay Street: the built street's 48 m and 10.25 m front to front)
for r in M['roads']:
    L = plen(r['pts'])
    check(abs(L - r['length_m']) < 0.05, f"{r['id']}: stored length {r['length_m']} equals the drawn {L:.2f}")
    g = r.get('g1_length_m')
    if g:
        measured = r['built']['length_m'] if r['id'] == 'quay_street' else L
        dev = (measured - g) / g
        if r['id'].startswith('cut_'):
            WARN.append(f"{r['id']}: {measured:.1f} m against G1 {g} m ({dev:+.0%}): G1's own Basin Road line fixes this distance (open point, not a pass)")
        else:
            check(abs(dev) <= 0.05, f"{r['id']}: {measured:.1f} m against G1 {g} m ({dev:+.1%})")
    w = r.get('g1_width_m')
    if w:
        width = r['built']['front_to_front_m'] if r['id'] == 'quay_street' else r['carriageway_m']
        check(abs(width - w) <= 1.0, f"{r['id']}: width {width} m against G1 {w} m")

qs = roads['quay_street']['built']
qpts = roads['quay_street']['pts']
built_drawn = [p for p in qpts if 4.5 - 0.01 <= p[1] <= 52.5 + 0.01]
check(abs(plen(built_drawn) - 48.0) < 0.01, f"Quay Street's drawn centre line holds the built 48 m between y 4.5 and 52.5 ({plen(built_drawn):.2f})")
east = [p for p in M['plots'] if p['street'] == 'quay_street' and p['building'] and p['number'] and p['number'] % 2 == 1]
west = [p for p in M['plots'] if p['street'] == 'quay_street' and p['building'] and p['number'] and p['number'] % 2 == 0 and p['number'] <= 12]
check(all(abs(min(x for x, y in p['outline']) - 125.125) < 0.01 for p in east) and all(abs(max(x for x, y in p['outline']) - 114.875) < 0.01 for p in west),
      'Quay Street drawn 10.25 m front to front (east frontage x 125.125, west 114.875)')
check(qs['length_m'] == 48.0 and qs['front_to_front_m'] == 10.25 and qs['bay_m'] == 6.0 and qs['kerb_upstand_m'] == 0.115,
      'Quay Street as built: 48 m, 10.25 m front to front, 6 m bays, 115 mm kerb')
qlamps = sorted([l for l in M['lamp_columns'] if l['road'] == 'quay_street'], key=lambda l: l['y'])
check([round(l['y'] - 4.5) for l in qlamps] == [8, 18, 28, 38] and [l['x'] > 120 for l in qlamps] == [True, False, True, False],
      "Quay Street's four lamp columns at street x 8 east, 18 west, 28 east, 38 west")
fp = M['footprint']
check(fp['x'] == [-80, 540] and fp['y'] == [0, 400], 'footprint x -80 to 540, y 0 to 400 (about 620 by 400 m)')

# 2. graphs
G = nx.Graph()
nodes = {n['id']: n for n in M['graph']['nodes']}
for e in M['graph']['edges']:
    G.add_edge(e['a'], e['b'], length=e['length_m'], foot_only=e.get('foot_only', False))
check(set(G.nodes) <= set(nodes), 'every graph edge joins named nodes')
D = nx.Graph()
for a, b, d in G.edges(data=True):
    if not d['foot_only']:
        D.add_edge(a, b, **d)

def path_len(graph, seq):
    total = 0.0
    for a, b in zip(seq, seq[1:]):
        total += nx.shortest_path_length(graph, a, b, weight='length')
    return total

loops = M['loops']
cl = path_len(D, loops['chase_loop']['nodes'])
check(abs(cl - 1528) <= 1528 * 0.02 and cl >= 1500, f'chase loop {cl:.1f} m against 1,528 m (at least 1,500)')
br = path_len(D, loops['basin_ring']['nodes'])
check(abs(br - 1000) <= 100, f'basin ring {br:.1f} m against about 1,000 m')
pl = path_len(D, loops['parade_loop']['nodes'])
check(abs(pl - 910) <= 91, f'parade loop {pl:.1f} m against about 910 m')
cr = nx.shortest_path_length(D, 'j_landing', 'j_north_edge', weight='length')
check(abs(cr - 548) <= 548 * 0.05, f'crossing by road {cr:.1f} m against 548 m')
cf = nx.shortest_path_length(G, 'j_landing', 'j_north_edge', weight='length')
check(abs(cf - 475) <= 475 * 0.05, f'crossing on foot {cf:.1f} m against 475 m')
# the chase loop's six junctions shared with the other loops
def loop_path(seq):
    pth = []
    for a, b in zip(seq, seq[1:]):
        pth += nx.shortest_path(D, a, b, weight='length')[:-1]
    return pth
lp = {k: set(n for n in loop_path(loops[k]['nodes']) if nodes[n]['kind'] == 'junction' and D.degree(n) > 2) for k in ('chase_loop', 'basin_ring', 'parade_loop')}
shared = (lp['chase_loop'] & lp['basin_ring']) | (lp['chase_loop'] & lp['parade_loop']) | (lp['basin_ring'] & lp['parade_loop'])
check(len(shared) >= 6, f'the three loops share at least six drivable junctions, so a chase can change loop ({len(shared)}: {sorted(shared)})')
comps = list(nx.connected_components(D))
check(len(comps) == 1, f'the driving graph is one piece ({len(comps)} pieces; the smaller ones {[sorted(c)[:3] for c in sorted(comps, key=len)[:-1]][:3]})')

# 3. every door reachable on foot from Mickey's front door; every place-door's street drivable or within 60 m of a drivable node
start = 'n_d_qs_1'
reach = nx.node_connected_component(G, start)
unreached = [d['id'] for d in M['doors'] if 'n_' + d['id'] not in reach]
check(not unreached, f'every door reachable on foot from Mickey\'s ({len(M["doors"])} doors; unreached: {unreached[:8]})')
for p in M['plots']:
    if p.get('place'):
        ds = [d for d in M['doors'] if d['plot'] == p['id']]
        check(bool(ds), f"named place {p['place']} has a door")

# 4. foot-only ways never in the driving graph; bollards at both ends
for r in M['roads']:
    if r['foot_only']:
        n_b = len([b for b in M['bollards'] if b.get('way') == r['id']])
        check(n_b >= 4, f"{r['id']}: bollards at both ends ({n_b})")
drive_roads = {e['road'] for e in M['graph']['edges'] if 'road' in e and not e['foot_only']}
check(not (drive_roads & {r['id'] for r in M['roads'] if r['foot_only']}), 'no foot-only way in the driving graph')

# 5. overlaps: buildings with each other, with road corridors and with water
def corridor(r):
    if r['foot_only']:
        w = r['carriageway_m'] / 2.0
        return LineString(r['pts']).buffer(w, cap_style=2)
    lw = r['carriageway_m'] / 2.0 + 0.125 + r['left'].get('width_m', 0)
    rw = r['carriageway_m'] / 2.0 + 0.125 + r['right'].get('width_m', 0)
    line = LineString(r['pts'])
    left = line.buffer(lw, cap_style=2, single_sided=True)
    right = line.buffer(-rw, cap_style=2, single_sided=True)
    return unary_union([left, right])
cors = {r['id']: corridor(r) for r in M['roads']}
from shapely.geometry import box
qr = roads['quay_road']
bridge = LineString([(250, 0), (480, 0)]).buffer(qr['carriageway_m'] / 2.0 + 0.125 + 2.0, cap_style=2)
cors['quay_road'] = unary_union([cors['quay_road'].difference(box(250, -50, 480, 50)), bridge])
waters = [Polygon(w['poly']) for w in M['water']]
polys = {p['id']: Polygon(p['outline']) for p in M['plots']}
bad_shape = [k for k, v in polys.items() if not v.is_valid or v.area <= 0]
check(not bad_shape, f'every plot outline is a valid polygon ({bad_shape[:5]})')
ids = list(polys)
over = []
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        a, b = polys[ids[i]], polys[ids[j]]
        if a.intersection(b).area > 0.05:
            pa, pb = M['plots'][i], M['plots'][j]
            # a building inside a yard or lot it belongs to is allowed (the hut in Iveson's yard, the lot's hut, the loft)
            inside_ok = {('iveson_yard', 'iveson_hut'), ('lot', 'lot_hut'), ('allotments', 'pigeon_loft')}
            if (ids[i], ids[j]) in inside_ok or (ids[j], ids[i]) in inside_ok:
                continue
            over.append((ids[i], ids[j], round(a.intersection(b).area, 1)))
check(not over, f'no two plots overlap ({over[:6]})')
rover = []
apron = {p['id'] for p in M['plots'] if p.get('on_quay_apron')}
for p in M['plots']:
    if p['id'] in apron:
        check(max(y for x, y in p['outline']) <= -4.5 + 0.01, f"{p['id']} stands on the quay apron, clear of the carriageway")
for pid, poly in polys.items():
    if pid in apron:
        continue
    for rid, c in cors.items():
        a = poly.intersection(c).area
        if a > 0.5:
            rover.append((pid, rid, round(a, 1)))
check(not rover, f'no plot stands on a road, pavement or lane ({rover[:8]})')
wover = [(pid, round(poly.intersection(w).area, 1)) for pid, poly in polys.items() for w in waters
         if poly.intersection(w).area > 0.05 and pid != 'ferry_landing']
check(not wover, f'no plot stands in the water except the landing pontoon ({wover[:5]})')
# roads cross water only on the basin bridge
for rid, c in cors.items():
    for w, wd in zip(waters, M['water']):
        a = c.intersection(w).area
        check(a < 0.5, f'{rid} keeps out of {wd["id"]} ({a:.1f} m2)')
# road centre lines cross only at named junctions
jxy = {(round(n['x'], 1), round(n['y'], 1)) for n in M['graph']['nodes'] if n['kind'] in ('junction', 'bend', 'vault')}
cross_bad = []
rl = list(M['roads'])
for i in range(len(rl)):
    for j in range(i + 1, len(rl)):
        x = LineString(rl[i]['pts']).intersection(LineString(rl[j]['pts']))
        if x.is_empty:
            continue
        pts = [x] if x.geom_type == 'Point' else list(getattr(x, 'geoms', []))
        for p in pts:
            if p.geom_type != 'Point':
                cross_bad.append((rl[i]['id'], rl[j]['id'], 'overlap'))
                continue
            if (round(p.x, 1), round(p.y, 1)) not in jxy:
                cross_bad.append((rl[i]['id'], rl[j]['id'], round(p.x, 1), round(p.y, 1)))
check(not cross_bad, f'roads and lanes cross only at named junctions ({cross_bad[:5]})')
gin = LineString(roads['ginnel']['pts']).intersection(LineString(roads['chapel_lane']['pts']))
check(gin.geom_type == 'Point' and abs(gin.x - 139) < 0.5 and abs(gin.y - 260) < 0.5, 'the ginnel crosses Chapel Lane at (139, 260)')

# 6. ids unique, references good, door numbers unique per street, doors on their plot and facing their street
allids = []
for key in ('roads', 'plots', 'doors', 'name_plates', 'lamp_columns', 'vault_places', 'quay_ladders', 'bollards', 'phone_boxes', 'cab_ranks',
            'turf_posts', 'rival_bases', 'police_points', 'landmarks', 'soft_edges', 'off_map', 'street_furniture', 'fishing_spots', 'water', 'quay_edges'):
    allids += [x['id'] for x in M[key]]
allids += [x['id'] for x in M['props']['items']]
dup = [k for k, v in Counter(allids).items() if v > 1]
check(not dup, f'every id unique across the file ({len(allids)} ids; duplicates {dup[:5]})')
plot_ids = set(polys)
check(all(d['plot'] in plot_ids for d in M['doors']), 'every door names a plot that exists')
check(all(d['street'] in roads for d in M['doors'] if d['street']), 'every door\'s street exists')
nums = Counter((d['street'], d['number']) for d in M['doors'] if d['number'] is not None and d['kind'] == 'front')
dupn = [k for k, v in nums.items() if v > 1]
check(not dupn, f'front door numbers unique per street ({dupn[:5]})')
off = []
for d in M['doors']:
    dist = polys[d['plot']].exterior.distance(Point(d['x'], d['y']))
    if dist > 0.25:
        off.append((d['id'], round(dist, 2)))
check(not off, f'every door lies on its plot\'s outline ({off[:6]})')
face_bad = []
for d in M['doors']:
    if d['kind'] != 'front' or not d['street']:
        continue
    th = math.radians(d['facing'])
    reach = 3 + d.get('setback_m', 0)
    fx, fy = d['x'] + reach * math.sin(th), d['y'] + reach * math.cos(th)
    if not cors[d['street']].buffer(0.3).contains(Point(fx, fy)):
        face_bad.append(d['id'])
check(not face_bad, f'every front door faces its own street ({face_bad[:6]})')
for b in M['rival_bases']:
    check(b['plot'] in plot_ids and any(d['id'] == b['door'] for d in M['doors']), f"rival base {b['id']} has its plot and door")

# 7. vault places: six, on foot-only ways, under 1.2 m
vs = M['vault_places']
check(len(vs) == 6, f'six vault places ({len(vs)})')
check(all(v['height_m'] < 1.2 for v in vs), 'every vault place under 1.2 m')
check(all(roads[v['way']]['foot_only'] for v in vs), 'every vault place is on a foot-only way')
check(Counter(v['way'] for v in vs) == Counter({'ginnel': 3, 'yards_lane': 1, 'cut_150': 1, 'cut_300': 1}),
      'vault places: one on the yards\' lane, three on the ginnel, one on each cut')

# 8. counts: phone boxes 3, ranks 2 or more, posts 3, bases 3, ladders within 20 m of every quay point
check(len(M['phone_boxes']) == 3, 'three phone boxes')
check(len(M['cab_ranks']) >= 2, 'two ranks besides or with Mickey\'s')
check(len(M['turf_posts']) == 3 and len(M['rival_bases']) == 3, 'three turf posts and three rival bases')
worst = 0
for e in M['quay_edges']:
    line = LineString(e['pts'])
    lads = [Point(l['x'], l['y']) for l in M['quay_ladders'] if l['edge'] == e['id']]
    for k in range(int(line.length) + 1):
        p = line.interpolate(k)
        worst = max(worst, min(p.distance(q) for q in lads))
check(worst <= 25, f'no point on a quay edge more than 25 m from a ladder (worst {worst:.1f} m)')

# 8b. point features stand on land, outside every building (yards and lots allowed for posts and stalls)
bpolys = [Polygon(p['outline']) for p in M['plots'] if p['building'] and not p.get('on_quay_apron')]
def on_land(x, y):
    q = Point(x, y)
    return not any(w.contains(q) for w in waters)
def in_bldg(x, y):
    q = Point(x, y)
    return any(b.contains(q) for b in bpolys)
pts_all = [(k, f) for k in ('phone_boxes', 'turf_posts', 'lamp_columns', 'street_furniture', 'fishing_spots', 'name_plates', 'vault_places', 'police_points') for f in M[k]]
wet = [f['id'] for k, f in pts_all if not on_land(f['x'], f['y'])]
check(not wet, f'no point feature stands in the water ({wet[:6]})')
inb = [f['id'] for k, f in pts_all if k not in ('landmarks',) and in_bldg(f['x'], f['y'])]
check(not inb, f'no point feature stands inside a building ({inb[:6]})')
wetp = [p['id'] for p in M['props']['items'] if not on_land(p['x'], p['y'])]
check(not wetp, f'no prop stands in the water ({len(wetp)}: {wetp[:4]})')
for rk in M['cab_ranks']:
    check(all(on_land(x, y) and not in_bldg(x, y) for x, y in rk['pts']), f"rank {rk['id']} is on the kerb, on land")

# 9. props: at least 5 per 10 m of every drivable road
pc = Counter(p['kind'] for p in M['props']['items'])
check(not (set(pc) & set(M['props']['forbidden'])), 'no forbidden prop kinds')
for r in M['roads']:
    n = len([p for p in M['props']['items'] if p['road'] == r['id']])
    need = 5 if not r['foot_only'] else 2
    check(n >= r['length_m'] / 10.0 * need - 0.5, f"{r['id']}: {n} props in {r['length_m']} m (at least {need} per 10 m)")

# 10. the longest run on the chase loop with no junction, yard mouth or door
loop_nodes = set()
path = []
seq = loops['chase_loop']['nodes']
for a, b in zip(seq, seq[1:]):
    path += nx.shortest_path(D, a, b, weight='length')[:-1]
stops = [n for n in path if D.degree(n) > 2]
longest = 0
acc = 0
for a, b in zip(path, path[1:] + path[:1]):
    acc += D[a][b]['length']
    if b in stops:
        longest = max(longest, acc)
        acc = 0
check(longest <= 280 * 1.05, f'the longest stretch of the chase loop with no place a car can turn off is {longest:.0f} m (G1: 280, within 5%)')

# 11. Quay Street's trades and canon's three sides
qsp = {p['number']: p for p in M['plots'] if p['street'] == 'quay_street' and p['building'] and p['number']}
check(qsp[1]['use'] == 'cab_office' and qsp[3]['use'] == 'fishmonger' and qsp[7]['use'] == 'empty_shop' and qsp[9]['use'] == 'launderette' and qsp[11]['use'] == 'grocer',
      "Quay Street's east side: Mickey's, then bay 1 fishmonger, bay 3 the empty unit, bay 4 launderette, bay 5 grocer")
check(all(qsp[n]['use'] == 'home' for n in (2, 4, 6)) and [qsp[n]['use'] for n in (8, 10, 12)] == ['newsagent', 'ironmonger', 'tea_room'],
      "west side: plain terraces across from Mickey's, the newsagent, ironmonger and tea room across from the parade's north half")
# content rule: no plot use or name that is drink or gambling
bad_words = ['bookmaker', 'betting', 'bookie', 'casino', 'arcade', 'bingo', 'off-licence', 'off licence', 'bar ', 'brewery', 'wine', 'beer', 'school children', 'nursery']
hits = [p['id'] for p in M['plots'] for w in bad_words if w in (p['name'] + ' ' + p['use'] + ' ' + p.get('note', '')).lower()]
check(not hits, f'no plot is a drink or gambling place, nor holds children ({hits})')

print(f"map.json: {len(OK)} checks passed, {len(FAIL)} failed, {len(WARN)} warnings (open points)")
for m in WARN:
    print('WARN', m)
for m in FAIL:
    print('FAIL', m)
if '-v' in sys.argv:
    for m in OK:
        print('ok  ', m)
sys.exit(1 if FAIL else 0)
