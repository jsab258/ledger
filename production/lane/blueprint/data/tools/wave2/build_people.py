#!/usr/bin/env python3
"""Build people/<id>.json, ties.json, cast.json and routines.json from cast_src.py, then check every routine
against map.json (walking reach on the map's walking graph at the 120 s hour) and places.json (ids, opening hours).
Written 24 Nov 2026 (data-build wave 2). Usage: python3 build_people.py [--check-only]. Exit 1 on a failed check."""
import json, os, sys, re, heapq, math
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import cast_src as C
import routines_fix as RF
for _p in C.P:
    if _p['id'] in RF.RT:
        _p['rt'] = RF.RT[_p['id']]
    if _p['id'] in RF.HOME:
        _p['home'] = RF.HOME[_p['id']]

MAP = json.load(open(os.path.join(D, 'map.json')))
PLACES = json.load(open(os.path.join(D, 'places.json')))
CLOCK = {"realSecondsPerGameHour": 120}
PROTO = json.load(open(os.path.join(HERE, 'protocast.json')))['cast']
PROTO = {p['id']: p for p in PROTO}
DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

# ---- chosen values (recorded in routines.json and the keeper log)
WALK_MPS = 1.4          # an ordinary adult's walk (about 1.4 m/s, the usual pedestrian figure); feel.walk_mps 1.6 is Frank's (tune.json)
WALK_MPS_OLD = 1.1      # 70 and over
REAL_S_PER_GAME_MIN = 2.0
REACH_SHARE = 0.75      # the walk to a place must take no more than half the stay there
PORTALS = {'edge_north', 'edge_west'}   # off the Hook: arrival from off is placed out of sight (rule below)
PROVISIONAL = {'tangs_takeaway': "the Tangs' takeaway on the parade: not in places.json or map.json (wave 1 gap)"}

# ---------------------------------------------------------------- geometry
doors = {d['id']: d for d in MAP['doors']}
pl_by_id = {p['id']: p for p in PLACES['places']}
nodes = {n['id']: (n['x'], n['y']) for n in MAP['graph']['nodes']}
adj = {}
for e in MAP['graph']['edges']:
    adj.setdefault(e['a'], []).append((e['b'], e['length_m']))
    adj.setdefault(e['b'], []).append((e['a'], e['length_m']))
spots = {}
for key in ('phone_boxes', 'cab_ranks', 'turf_posts', 'soft_edges', 'fishing_spots', 'street_furniture'):
    for s in MAP.get(key, []):
        if 'x' in s:
            spots[s['id']] = (s['x'], s['y'])
        elif 'pts' in s:
            spots[s['id']] = tuple(sum(c) / len(s['pts']) for c in zip(*s['pts']))
spots['market_stalls_quay'] = (90.0, 5.5)   # timetables.json market: the quay road's north pavement, x 66 to 114

def point_of(pid):
    if pid in doors:
        return (doors[pid]['x'], doors[pid]['y'])
    p = pl_by_id.get(pid)
    if p:
        if p.get('doors'):
            d = doors.get(p['doors'][0])
            if d:
                return (d['x'], d['y'])
        if 'x' in p:
            return (p['x'], p['y'])
        if pid in spots:
            return spots[pid]
    if pid in spots:
        return spots[pid]
    return None

def nearest_node(pt):
    return min(nodes, key=lambda n: (nodes[n][0] - pt[0]) ** 2 + (nodes[n][1] - pt[1]) ** 2)

_dist_cache = {}
def walk_m(a, b):
    """Walking distance in metres between two places: straight to the nearest graph node at each end, then the graph."""
    if a == b:
        return 0.0
    key = (a, b)
    if key in _dist_cache:
        return _dist_cache[key]
    pa, pb = point_of(a), point_of(b)
    if pa is None or pb is None:
        return None
    na, nb = nearest_node(pa), nearest_node(pb)
    seen = {na: 0.0}
    q = [(0.0, na)]
    while q:
        dd, n = heapq.heappop(q)
        if n == nb:
            break
        if dd > seen.get(n, 1e18):
            continue
        for m, w in adj.get(n, []):
            nd = dd + w
            if nd < seen.get(m, 1e18):
                seen[m] = nd
                heapq.heappush(q, (nd, m))
    g = seen.get(nb)
    if g is None:
        return None
    tot = g + math.dist(pa, nodes[na]) + math.dist(pb, nodes[nb])
    _dist_cache[key] = _dist_cache[(b, a)] = tot
    return tot

# ---------------------------------------------------------------- routines
def parse_days(spec):
    if spec == 'daily':
        return set(DAYS)
    out = set()
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            i, j = DAYS.index(a), DAYS.index(b)
            out |= set(DAYS[i:j + 1])
        else:
            out.add(part)
    return out

def parse_rt(rt):
    groups = []
    for g in rt.split('/'):
        days, rows = g.split('|', 1)
        rr = []
        for r in rows.split(';'):
            r = r.strip()
            if not r:
                continue
            t, place, act = r.split(' ', 2)
            rr.append((t, place, act.strip()))
        groups.append((days, rr))
    return groups

def mins(t):
    h, m = t.split(':')
    return int(h) * 60 + int(m)

def place_open(pid, day, t):
    """True if the place's public hours include game time t (minutes) on day; None if the place has no hours."""
    p = pl_by_id.get(pid)
    if not p or not p.get('hours'):
        return None
    prev = DAYS[(DAYS.index(day) - 1) % 7]
    for h in p['hours']:
        ds, a, b = parse_days(h[0]), mins(h[1]), mins(h[2])
        if b <= a:  # runs into the next morning
            if day in ds and t >= a:
                return True
            if prev in ds and t < b:
                return True
        else:
            if day in ds and a <= t < b:
                return True
    return False

# acts a non-keeper does as a customer: must be inside public hours
CUSTOMER = re.compile(r'\b(breakfast|dinner|tea\b|a tea|his tea|her dinner|his dinner|shopping|a bit of fish|his fish|fish for|his table|pension|papers?\b|a frame|the tables|blanks|the bag|his break|her pension|a pot of tea|Sunday dinner|late breakfast|the evening trade|a cup)', re.I)

KEEPER = re.compile(r'(opening|papers in|Sunday papers|the fryers|the urn)', re.I)

def check_person(p, fails, warns):
    pid = p['id']
    groups = parse_rt(p['rt'])
    cover = {}
    for days, rows in groups:
        for d in parse_days(days):
            if d in cover:
                fails.append(f'{pid}: {d} covered twice')
            cover[d] = rows
    for d in DAYS:
        if d not in cover:
            fails.append(f'{pid}: {d} not covered')
    speed = WALK_MPS_OLD if p['a'] >= 70 else WALK_MPS
    longest = 0
    for d, rows in cover.items():
        if not rows or rows[0][0] != '00:00':
            fails.append(f'{pid} {d}: first row is not 00:00')
        ts = [mins(r[0]) for r in rows]
        if ts != sorted(ts) or len(set(ts)) != len(ts):
            fails.append(f'{pid} {d}: rows out of order or two at one time')
        for i, (t, place, act) in enumerate(rows):
            if place in PROVISIONAL:
                warns.append(f'{pid} {d} {t}: provisional place {place}')
                continue
            if place not in pl_by_id and place not in doors:
                fails.append(f'{pid} {d} {t}: {place} is neither a places.json id nor a map.json door')
                continue
            # opening hours for a customer act
            if CUSTOMER.search(act) and not KEEPER.search(act) and place_open(place, d, mins(t)) is False:
                fails.append(f'{pid} {d} {t}: {place} is shut at {t} ({act})')
            if i == 0:
                continue
            prev = rows[i - 1][1]
            if act.startswith('by cab') or '(police.json)' in act or '(police.json)' in rows[i - 1][2]:
                continue
            if prev in PORTALS or place in PORTALS or prev in PROVISIONAL or prev in ('police_station', 'infirmary', 'licensing', 'copper_row_market'):
                continue
            if pl_by_id.get(place, {}).get('kind') == 'off_map':
                continue
            dist = walk_m(prev, place)
            if dist is None:
                fails.append(f'{pid} {d} {t}: no walking route {prev} -> {place}')
                continue
            stay = mins(t) - mins(rows[i - 1][0])   # the stay before the move, which the walk comes out of
            walk_game_min = dist / speed / REAL_S_PER_GAME_MIN
            longest = max(longest, dist)
            if walk_game_min > REACH_SHARE * stay:
                fails.append(f'{pid} {d} {t}: {prev} -> {place} is {dist:.0f} m, {walk_game_min:.0f} game min on foot, more than three quarters of the {stay} min stay before it')
    # the night between days: the last row of one day to the first of the next is a move too
    for k, d in enumerate(DAYS):
        a, b = cover.get(d), cover.get(DAYS[(k + 1) % 7])
        if not a or not b:
            continue
        prev, place = a[-1][1], b[0][1]
        if prev == place or prev in PORTALS or place in PORTALS or prev in PROVISIONAL or place in PROVISIONAL:
            continue
        if a[-1][2].startswith('by cab') or b[0][2].startswith('by cab') or '(police.json)' in a[-1][2]:
            continue
        if pl_by_id.get(place, {}).get('kind') == 'off_map' or pl_by_id.get(prev, {}).get('kind') == 'off_map':
            continue
        dist = walk_m(prev, place)
        stay = 24 * 60 - mins(a[-1][0])
        if dist is not None and dist / speed / REAL_S_PER_GAME_MIN > REACH_SHARE * stay:
            fails.append(f'{pid} {d} to {DAYS[(k + 1) % 7]} at midnight: {prev} -> {place} is {dist:.0f} m')
    return longest

# ---------------------------------------------------------------- people records
def person_record(p):
    pr = PROTO.get(p.get('proto') or '')
    look = p.get('look') or (pr and pr['look']) or {}
    card = dict(p.get('card') or {})
    if pr:
        pc = pr['card']
        for k in ('who', 'speak', 'life', 'fire', 'rivals', 'secret'):
            if k in pc and k not in card:
                card[k] = pc[k]
    for k in list(card):
        if isinstance(card[k], str):
            card[k] = (card[k].replace('Humberside CID', 'CID').replace('with Humberside CID', 'in CID')
                       .replace('Hull vowels', 'northern vowels').replace('Tom Nowak', 'Frank Nowak').replace(' Tom ', ' Frank ')
                       .replace(' Tom.', ' Frank.').replace(' Tom,', ' Frank,').replace('"Tom"', '"Frank"').replace('Calls Tom', 'Calls Frank'))
    card.setdefault('who', p['r'])
    card.setdefault('speak', 'TO WRITE (story lane)')
    card.setdefault('life', 'TO WRITE (story lane)')
    tr = C.TRAITS.get(p['id'])
    if tr:
        nerve, loyal, greed, saw = tr
        will = {'yes': 0.6, 'no': 0.4, 'never': 0.1}[saw]
        temper = {"nerve": nerve, "dutiful": loyal, "willingness": will, "from": "town-traits-draft-2026-09-29 (nerve, loyalty; willingness from 'a wounding they saw': yes 0.6, no 0.4, never 0.1)"}
        quiet = saw == 'never' or loyal >= 0.6
        venal = greed
    else:
        t = p.get('t') or (0.45, 0.4, 0.5)
        temper = {"nerve": t[0], "dutiful": t[1], "willingness": t[2], "from": "chosen by the data-build wave 2 job from the person's card"}
        quiet = bool(p.get('quiet', False))
        venal = round(min(1, max(0, 1 - t[1] * 0.8 - 0.1)), 2)
    rec = {
        "id": p['id'], "cast_id": p.get('cid'), "called": p.get('called') or p['n'], "name": p['n'], "age": p['a'], "sex": p['s'],
        "role": p['r'], "kind": p['k'], "voice": p.get('v'), "look": look,
        "nerve": temper['nerve'], "venal": venal,
        "talk": pr['talk'] if pr and 'talk' in pr else round(temper['willingness'], 2),
        "discretion": pr['discretion'] if pr and 'discretion' in pr else round(1 - temper['willingness'] * 0.8, 2),
        "temperament": temper, "keepsQuiet": quiet,
        "home": p['home'],
        "sched": [],
        "lines": {"own": "lines/own-%s.json" % p['id'], "note": "own lines live in lines/ (a record each); see lines/README.md"},
        "card": card, "can_die": p['die'],
        "invented": p.get('inv', False) if p.get('inv') != 'frame' else 'proposed by the story frame',
        "src": p['src'],
    }
    if p.get('fb'):
        rec['fallback_role'] = p['fb']
    if p.get('fight'):
        rec['fight_kind'] = p['fight']
    if p['id'] == 'frank_nowak':
        rec['name_ladder'] = ["the new owner", "Nowak", "Frank", "Frankie"]
        rec['never_called'] = ["Tom", "Tommy"]
        rec['lines'] = {"own": "the player's; fixed lines at authored beats only (lines/frank.json)"}
    # sched: the prototype's row shape [fromHour, where, act, days?] derived from the routine
    for days, rows in parse_rt(p['rt']) if p['rt'] != 'lead' else []:
        for (t, place, act) in rows:
            h = round(mins(t) / 60, 2)
            row = [h, place, act]
            if days != 'daily':
                row.append(days)
            rec['sched'].append(row)
    return rec

def main():
    check_only = '--check-only' in sys.argv
    fails, warns = [], []
    ids = [p['id'] for p in C.P]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        fails.append('duplicate ids: %s' % sorted(dup))
    longest = {}
    for p in C.P:
        if p['a'] < 18:
            fails.append(f"{p['id']}: under 18")
        if p['rt'] == 'lead':
            continue
        longest[p['id']] = check_person(p, fails, warns)
    if p and not any(p['id'] == 'frank_nowak' and p['die'] is False for p in C.P):
        fails.append('Frank must have can_die false')
    print('people:', len(C.P), ' fails:', len(fails), ' warnings:', len(warns))
    for f in fails:
        print('FAIL', f)
    if check_only:
        return 1 if fails else 0
    os.makedirs(os.path.join(D, 'people'), exist_ok=True)
    for p in C.P:
        json.dump(person_record(p), open(os.path.join(D, 'people', p['id'] + '.json'), 'w'), indent=1, ensure_ascii=False)
    # routines.json
    routines = []
    for p in C.P:
        if p['rt'] == 'lead':
            continue
        rows = []
        for days, rr in parse_rt(p['rt']):
            for (t, place, act) in rr:
                row = {"from": t, "place": place, "act": act}
                if days != 'daily':
                    row['days'] = days
                rows.append(row)
        routines.append({"person": p['id'], "rows": rows, "longest_walk_m": round(longest.get(p['id'], 0)), "src": p['src']})
    json.dump({"file": "routines.json", "version": "wave2-2026-11-24", "clock": CLOCK,
               "sources": ["tools/wave2/cast_src.py (one routine a person, authored on map.json and places.json ids)",
                           "production/specs/hook-cast.json routines (older place ids, remapped by hand)",
                           "BLUEPRINT-02 2.1.1, 2.5.5; BLUEPRINT-07 CLK-03; places.json hours; timetables.json shifts, ferry, beat"],
               "rules": {
                   "rows": "A row holds from its game time until the next row of the same day; every day starts at 00:00. days omitted means daily.",
                   "place": "A places.json id, or a map.json door id for a home. edge_north and edge_west mean off the Hook (home across town, the bus, the station).",
                   "walking_reach": f"Between two rows on the Hook the walk on map.json's walking graph at {WALK_MPS} m/s ({WALK_MPS_OLD} m/s at 70 and over) is taken out of the end of the stay before it (the person sets off early enough to arrive at the row's time) and uses no more than three quarters of that stay, counted in game minutes at 2 real seconds a game minute (120 s a game hour). Checked in code: tools/wave2/build_people.py.",
                   "from_off_the_hook": "Arriving from off the Hook (edge_north, edge_west, the police station, the Infirmary, licensing, the Copper Row market), the person is placed out of sight at the nearest soft edge, bus stop or door and is not reach-checked: the bus, a bike or a lift in town are not simulated (chosen).",
                   "hours": "A customer act (breakfast, dinner, shopping, a frame) falls inside the place's public hours; a keeper or worker may be there before opening and after closing.",
                   "finders": "2.5.5: whoever's routine next brings them past an unseen deed finds it; the named finders are listed in finders below."},
               "chosen_values": {"walk_mps": WALK_MPS, "walk_mps_70_and_over": WALK_MPS_OLD, "reach_share_of_stay": REACH_SHARE},
               "finders": FINDERS,
               "provisional_places": PROVISIONAL,
               "open_points": ["The Tangs' takeaway is in canon and the side stories but not on wave 1's map or places; its rows use the provisional id tangs_takeaway until the keeper adds it (likely Back Parade).",
                               "Wayne Harrison works Rita's back room here (canon: her back-room hand); places.json also gives him a pawn of his own on North Road (waynes_pawn), which no routine uses: the keeper should reconcile.",
                               "The steam laundry of canon and the Washeteria are one place (launderette) on wave 1's map; laundry workers' rows use it.",
                               "Captain Ozols's ship has no berth on the map; fishing_basin_north stands in.",
                               "Beat routes in detail are police.json's; the constables' rows name the beat's start place only."],
               "routines": routines}, open(os.path.join(D, 'routines.json'), 'w'), indent=1, ensure_ascii=False)
    print('wrote', len(C.P), 'people and', len(routines), 'routines')
    return 1 if fails else 0

FINDERS = [
    {"person": "edna_coulson", "from": "05:45", "passes": ["harbour_board", "tea_room", "agar_base"], "finds": "a forced door, glass or anything missing at the Harbour Board, the Copper Kettle or the agents' office (the cleaner at six)"},
    {"person": "bill_huxtable", "from": "05:15", "passes": ["ferry_landing", "fish_dock", "dock_gate"], "finds": "anything left on the quay overnight between the landing and the pen (the first dock worker)"},
    {"person": "eddie_birtwhistle", "from": "04:45", "passes": ["fish_dock"], "finds": "the fish dock and the ice hut"},
    {"person": "brenda_laverack", "from": "05:00", "passes": ["fish_dock", "laveracks"], "finds": "the fish dock, then her own shop's back door"},
    {"person": "gordon_leckenby", "from": "06:00", "passes": ["ferry_landing"], "finds": "the landing and the shelter before the first boat"},
    {"person": "doreen_harland", "from": "05:45", "passes": ["launderette"], "finds": "the laundry's back door and the parade's foot"},
    {"person": "grace_rinaldi", "from": "05:30", "passes": ["caff"], "finds": "the caff's window and the quay road outside"},
    {"person": "peart", "from": "05:45", "passes": ["newsagent"], "finds": "Quay Street's shop fronts as the papers come in"},
    {"person": "norman_dent", "from": "19:30", "passes": ["dents_warehouses", "net_loft", "burned_warehouse"], "finds": "the warehouse row, all night"},
    {"person": "pc_haigh", "from": "22:00", "passes": ["mickeys", "mickeys_yard", "ferry_landing"], "finds": "Mickey's door, the yards' lane and the landing on the night beat"},
    {"person": "maggie_firth", "from": "21:30", "passes": ["tea_stall"], "finds": "the quay by the tea stall, all night"},
    {"person": "neil_screeton", "from": "07:30", "passes": ["iveson_yard", "iveson_hut"], "finds": "Iveson's yard and hut (the owner's man on his return)"},
    {"person": "nora_cronin", "from": "07:15", "passes": ["priests_house", "chapel"], "finds": "the priest's house and the chapel"},
    {"person": "winifred_duggleby", "from": "08:00", "passes": ["chapel"], "finds": "the chapel, its roof and its flowers"},
    {"person": "owners", "from": "the opening time", "passes": ["their own place"], "finds": "every shop's keeper finds his own shop on his return (2.5.5: the owner on his return); see each keeper's first row"},
]

if __name__ == '__main__':
    sys.exit(main())
