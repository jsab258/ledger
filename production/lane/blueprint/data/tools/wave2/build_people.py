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
import people_fix as PF
for _p in C.P:
    if _p['id'] in RF.RT:
        _p['rt'] = RF.RT[_p['id']]
    if _p['id'] in RF.HOME:
        _p['home'] = RF.HOME[_p['id']]
    _f = PF.FIELDS.get(_p['id'], {})
    for _k in ('a', 'fb', 'k', 't', 'r', 'fight'):
        if _k in _f:
            _p[_k] = _f[_k]
    # Frank's line (RT-09, RT2-05): women, sixty and over, the priest are covered
    _covered = _p['s'] == 'f' or _p['a'] >= 60 or _p['id'] == 'brendan_walsh'
    if _p['id'] != 'frank_nowak':
        _p['die'] = not _covered
    if _covered:
        _p.pop('fight', None)
        if _p.get('fb') and _p['id'] not in ('old_firm_man',):
            _p['fb_note'] = _p.pop('fb')
    elif not _p.get('fb') and _p['id'] != 'frank_nowak':
        _p['fb'] = {'officer': 'another officer from the station', 'rival_man': "his head's next man", 'minor': 'the role passes to another of the same trade, or the thread closes'}.get(_p['k'], 'the role passes to another, or the thread closes')

MAP = json.load(open(os.path.join(D, 'map.json')))
PLACES = json.load(open(os.path.join(D, 'places.json')))
CLOCK = {"realSecondsPerGameHour": 120}
PROTO = json.load(open(os.path.join(HERE, 'protocast.json')))['cast']
PROTO = {p['id']: p for p in PROTO}
TEMPERS = json.load(open(os.path.normpath(os.path.join(D, '..', 'temper', 'tempers.json'))))['people']
_BANK = json.load(open(os.path.normpath(os.path.join(D, '..', '..', '..', 'cloud-week', 'lines', 'lines.json'))))
BANK_MEMBERS = {m: k for k, v in _BANK['speakers'].items() if not v.get('own') for m in v.get('members', [])}
BANK_MEMBERS.update({'rocco': 'driver', 'sam': 'casual_worker', 'emil': 'office_worker', 'june': 'office_worker'})
DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

# ---- chosen values (recorded in routines.json and the keeper log)
WALK_MPS = 1.4          # an ordinary adult's walk (about 1.4 m/s, the usual pedestrian figure); feel.walk_mps 1.6 is Frank's (tune.json)
WALK_MPS_OLD = 1.1      # 70 and over
REAL_S_PER_GAME_MIN = 2.0
REACH_SHARE = 0.5       # the walk to a place must take no more than half the stay there
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
CUSTOMER = re.compile(r'\b(breakfast|dinner|tea\b|a tea|his tea|her dinner|his dinner|shopping|a bit of fish|his fish|fish for|his table|pension|papers?\b|a frame|the tables|blanks|the bag|the club|his break|her pension|a pot of tea|Sunday dinner|late breakfast|the evening trade|a cup|holding court|with Danny|leaflets|Mass|the boxes|looking)', re.I)

KEEPER = re.compile(r'(opening|papers in|Sunday papers|the fryers|the urn|club night|morning Mass|Masses|evening Mass|Saturday morning)', re.I)

FOOT_CAP_M = 250        # CLK-03: a person's places lie within about 200 m of walking; 250 m tolerance (chosen)
MODE_MPS = {'by bike': 5.0, 'by car': 9.0, 'by cab': 9.0, 'on foot': None}
CARS = {'danny_cammack', 'craig_fewson', 'maureen_jensen', 'geoffrey_agar', 'keith_garbutt', 'eric_tharratt', 'harry_holt', 'bernard_gill',
        'clive_ackroyd', 'wes_akers', 'steve_brannigan', 'barry_coult', 'ray_spink', 'kenny_varley', 'simon_ombler', 'trevor_garton', 'kevin_needham', 'terry_hodgson'}
NIGHT = {'terry_hodgson', 'norman_dent', 'maggie_firth', 'pc_haigh', 'old_firm_man', 'wes_akers', 'steve_brannigan', 'sandra_newbould', 'janet_lumb',
         'eddie_birtwhistle', 'tony_marsden', 'brenda_laverack', 'dougie_saltmarsh'}
EARLIEST = {'default': 5 * 60, 'dock': 4 * 60}   # chosen: nobody leaves home before 05:00, dock and fish-dock men 04:00
HOME_KINDS = {'flat', 'home', 'boarding_house'}
def is_home(p, place):
    return place == p['home'] or place in doors and MAP_PLOT_USE.get(doors[place]['plot']) == 'home'
MAP_PLOT_USE = {pl['id']: pl.get('use') for pl in MAP['plots']}

def mode_of(p, act, dist):
    for m in ('by bike', 'by car', 'by cab', 'by bus'):
        if act.startswith(m):
            return m
    if dist is not None and dist > FOOT_CAP_M:
        return 'by car' if p['id'] in CARS else ('by cab' if p['a'] >= 65 else 'by bike')
    return 'on foot'

def stamp_modes(p):
    """Write the travel mode into each long move's act (the rule: car owners by car, 65 and over by cab, others by bike)."""
    out = []
    for days, rows in parse_rt(p['rt']):
        rr = []
        for i, (t, place, act) in enumerate(rows):
            if i and not act.startswith('by ') and rows[i - 1][1] not in PORTALS and place not in PORTALS:
                d = walk_m(rows[i - 1][1], place) if place not in PROVISIONAL and rows[i - 1][1] not in PROVISIONAL else None
                m = mode_of(p, act, d)
                if m != 'on foot' and pl_by_id.get(place, {}).get('kind') != 'off_map' and pl_by_id.get(rows[i - 1][1], {}).get('kind') != 'off_map':
                    act = m + ': ' + act
            rr.append('%s %s %s' % (t, place, act))
        out.append(days + '|' + '; '.join(rr))
    p['rt'] = '/'.join(out)

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
    foot = WALK_MPS_OLD if p['a'] >= 70 else (1.1 if 'constable' in p['r'].lower() else WALK_MPS)
    longest = 0
    def move(prev_row, row, stay, d, label):
        nonlocal longest
        prev, place, act = prev_row[1], row[1], row[2]
        if prev == place or prev in PORTALS or place in PORTALS or prev in PROVISIONAL or place in PROVISIONAL:
            return
        if act.startswith('by bus') or pl_by_id.get(place, {}).get('kind') == 'off_map' or pl_by_id.get(prev, {}).get('kind') == 'off_map':
            return
        if '(police.json)' in act and '(police.json)' in prev_row[2]:
            return   # both rows on the beat: police.json walks it
        dist = walk_m(prev, place)
        if dist is None:
            fails.append(f'{pid} {label}: no walking route {prev} -> {place}')
            return
        m = mode_of(p, act, dist)
        if m == 'on foot' and dist > FOOT_CAP_M:
            fails.append(f'{pid} {label}: {prev} -> {place} is {dist:.0f} m on foot, over the {FOOT_CAP_M} m cap (CLK-03)')
        speed = MODE_MPS.get(m) or foot
        travel = dist / speed / REAL_S_PER_GAME_MIN
        longest = max(longest, dist)
        if travel > 0.5 * stay:
            fails.append(f'{pid} {label}: {prev} -> {place} {dist:.0f} m {m} takes {travel:.0f} game min, more than half the {stay} min stay before it')
        depart = (mins(row[0]) - travel) % 1440
        if is_home(p, prev) and pid not in NIGHT and mins(row[0]) < 12 * 60:
            early = EARLIEST['dock'] if place in ('dock_gate', 'fish_dock', 'cold_stores') else EARLIEST['default']
            if depart < early:
                fails.append(f'{pid} {label}: leaves home at {int(depart)//60:02d}:{int(depart)%60:02d}, before {early//60:02d}:{early%60:02d}')
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
            end = mins(rows[i + 1][0]) if i + 1 < len(rows) else 1440
            if CUSTOMER.search(act) and not KEEPER.search(act):
                for tt in (mins(t), max(mins(t), end - 1)):
                    if place_open(place, d, tt) is False:
                        fails.append(f'{pid} {d} {t}: {place} is shut during the stay ({act})')
                        break
            if i:
                move(rows[i - 1], rows[i], mins(t) - mins(rows[i - 1][0]), d, f'{d} {t}')
    for k, d in enumerate(DAYS):
        a, b = cover.get(d), cover.get(DAYS[(k + 1) % 7])
        if a and b:
            move(a[-1], b[0], 1440 - mins(a[-1][0]), d, f'{d} to {DAYS[(k + 1) % 7]} at midnight')
    return longest

def check_finders(fails):
    rows_of = {p['id']: p for p in C.P}
    for f in FINDERS:
        p = rows_of.get(f['person'])
        if not p:
            continue
        places = {pl for _, rr in parse_rt(p['rt']) for _, pl, _ in rr}
        for x in f['passes']:
            if x not in places:
                fails.append(f"finder {f['person']}: never at {x}, which the finders list says he passes")

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
    _f = PF.FIELDS.get(p['id'], {})
    for k, v in _f.get('card', {}).items():
        card[k] = v
    for a, b in _f.get('card_replace', []):
        for k in list(card):
            if isinstance(card[k], str):
                card[k] = card[k].replace(a, b)
    if _f.get('look_h'):
        look = dict(look, h=_f['look_h'])
    card.setdefault('who', p['r'])
    card.setdefault('speak', 'TO WRITE (story lane)')
    card.setdefault('life', 'TO WRITE (story lane)')
    # the temper: home is temper/tempers.json (the temper job, 24 Nov 2026; TEMPER-MODEL.md); the old four dials are retired
    tp = TEMPERS[p['id']]
    temper = {k: tp[k] for k in ('nerve', 'greed', 'mouth', 'law', 'grudge')}
    rec = {
        "id": p['id'], "cast_id": p.get('cid'), "called": p.get('called') or p['n'], "name": p['n'], "age": p['a'], "sex": p['s'],
        "role": p['r'], "kind": p['k'], "voice": p.get('v'), "look": look,
        "temper": temper, "regard": tp['regard'], "keepsQuiet": tp['keepsQuiet'], "temper_why": tp['why'],
        "home": p['home'],
        "sched": [],
        "speaker_kind": PF.speaker_kind(p, BANK_MEMBERS),
        "lines": ({"own": "lines/own-%s.json" % p['id'], "shared": "lines/shared-street.json (who = speaker_kind)"} if PF.has_own(p)
                  else {"own": "none: shared lines only", "shared": "lines/shared-street.json (who = speaker_kind)" if PF.speaker_kind(p, BANK_MEMBERS) else "authored scenes and live talk only (a rival head: the bank's no_kind)"}),
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
        stamp_modes(p)
        longest[p['id']] = check_person(p, fails, warns)
    check_finders(fails)
    if p and not any(p['id'] == 'frank_nowak' and p['die'] is False for p in C.P):
        fails.append('Frank must have can_die false')
    print('people:', len(C.P), ' fails:', len(fails), ' warnings:', len(warns))
    for f in fails:
        print('FAIL', f)
    if check_only:
        return 1 if fails else 0
    os.makedirs(os.path.join(D, 'people'), exist_ok=True)
    import glob as _g
    for _f in _g.glob(os.path.join(D, 'people', '*.json')):
        os.remove(_f)
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
                   "walking_reach": f"CLK-03 restated for the 120 s hour (2 real seconds a game minute): on foot a move is at most {FOOT_CAP_M} m (about 200 m, the blueprint's figure, with a tolerance), at {WALK_MPS} m/s ({WALK_MPS_OLD} m/s at 70 and over, 1.1 m/s for a constable). A longer move is made by bike (5 m/s), by car (9 m/s; car owners listed in build_people.py CARS) or by cab (65 and over, or a fare); the mode is written at the start of the act. The travel comes out of the end of the stay before it and may use at most half that stay, so a person is at each place for at least half its row. Nobody leaves home before 05:00 (dock and fish-dock men 04:00) unless he works nights. Checked in code: tools/wave2/build_people.py.",
                   "from_off_the_hook": "edge_north and edge_west are the two soft edges: a person whose row is there is off the Hook. Arriving, he appears at that soft edge at the row's time (or at bus_stop_qs when the row before is a 'by bus' row) and walks or rides on; leaving, he goes to it. The police station, the Infirmary, licensing and the Copper Row market are off-map places reached through edge_north. Moves through a soft edge are not reach-checked (the bus and the town are not simulated).",
                   "hours": "A customer act (breakfast, dinner, shopping, a frame, Mass, leaflets) falls inside the place's public hours for the whole stay; a keeper or worker may be there before opening and after closing.",
                   "rota": "Police: the day beat 06:00 to 22:00 in two turns (PC Ibbotson early, PC Ackrill late, weekdays) and the night beat 22:00 to 06:00 (PC Haigh, Sunday to Thursday nights); weekend turns and Friday and Saturday nights are walked by a constable from town (police.json beat_constable_second), and the custody desk outside Sgt Bellwood's weekday days by the night sergeant in town (chosen).",
                   "firm_shifts": "Kevin 06:00 to 18:00 and Terry 18:00 to 06:00 every day, Pauline on the radio 07:00 to 19:00 every day, as timetables.json; Sheila at the counter 08:30 to 17:30 weekdays (17:45 on Friday for the reckoning), 08:30 to 13:00 Saturday and 10:00 to 13:00 Sunday for the week's read-back (STORY-FRAME 1). After her the counter is Pauline's to 19:00 and Ron's on the door to 23:00; timetables.json shift_counter (07:00 to 23:00, Sheila) should say so.",
                   "finders": "2.5.5: whoever's routine next brings them past an unseen deed finds it; the named finders are listed in finders below."},
               "chosen_values": {"walk_mps": WALK_MPS, "walk_mps_70_and_over": WALK_MPS_OLD, "foot_cap_m": FOOT_CAP_M, "bike_mps": 5.0, "car_mps": 9.0, "travel_share_of_stay_before": 0.5, "earliest_from_home": "05:00 (dock 04:00)"},
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
    {"person": "edna_coulson", "from": "06:00", "passes": ["mickeys", "tea_room", "snooker_hall"], "finds": "a forced door, glass or anything missing at Mickey's front office, the Copper Kettle or the snooker hall (the cleaner at six)"},
    {"person": "stan_pickles", "from": "07:30", "passes": ["harbour_board"], "finds": "the Harbour Board and its works yard, first in"},
    {"person": "bill_huxtable", "from": "05:05", "passes": ["fish_dock", "dock_gate"], "finds": "anything left on the east quay and the fish dock overnight (the first dock worker, from 05:05); the landing's first passer is Gordon Leckenby at 06:00"},
    {"person": "eddie_birtwhistle", "from": "04:45", "passes": ["fish_dock"], "finds": "the fish dock and the ice hut"},
    {"person": "brenda_laverack", "from": "05:00", "passes": ["fish_dock", "laveracks"], "finds": "the fish dock, then her own shop's back door"},
    {"person": "gordon_leckenby", "from": "06:00", "passes": ["ferry_landing"], "finds": "the landing and the shelter before the first boat"},
    {"person": "doreen_harland", "from": "05:45", "passes": ["launderette"], "finds": "the laundry's back door and the parade's foot"},
    {"person": "grace_rinaldi", "from": "05:30", "passes": ["caff"], "finds": "the caff's window and the quay road outside"},
    {"person": "peart", "from": "05:45", "passes": ["newsagent"], "finds": "Quay Street's shop fronts as the papers come in"},
    {"person": "norman_dent", "from": "19:30", "passes": ["dents_warehouses", "net_loft", "burned_warehouse"], "finds": "the warehouse row, all night"},
    {"person": "pc_haigh", "from": "22:00", "passes": ["mickeys"], "finds": "Mickey's door, the yards' lane and the landing on the night beat (police.json walks the beat; his row names its start)"},
    {"person": "maggie_firth", "from": "21:30", "passes": ["tea_stall"], "finds": "the quay by the tea stall, all night"},
    {"person": "neil_screeton", "from": "07:30", "passes": ["iveson_yard"], "finds": "Iveson's yard (the owner's man on his return); Dennis Iveson finds the hut at 12:00"},
    {"person": "nora_cronin", "from": "07:15", "passes": ["priests_house", "chapel"], "finds": "the priest's house and the chapel"},
    {"person": "winifred_duggleby", "from": "08:00", "passes": ["chapel"], "finds": "the chapel, its roof and its flowers"},
    {"person": "owners", "from": "the opening time", "passes": ["their own place"], "finds": "every shop's keeper finds his own shop on his return (2.5.5: the owner on his return); see each keeper's first row"},
]

if __name__ == '__main__':
    sys.exit(main())
