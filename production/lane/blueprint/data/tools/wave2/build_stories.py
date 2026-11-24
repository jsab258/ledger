#!/usr/bin/env python3
"""Build jobs/, fares.json, happenings.json and side-stories/ (blueprint data file 11) from jobs_src.py and stories_src.py,
and check every place against places.json, rooms.json and map.json doors, every person against people/, every break-in
step's three keys, the wrinkle rules (7.14) and the counts (3.3, 3.4.1, 3.7). Written 24 Nov 2026 (wave 2)."""
import json, os, sys, glob, re
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import jobs_src as JS, stories_src as SS
from build_people import C, PROVISIONAL
CLOCK = {"realSecondsPerGameHour": 120}
PL = {p['id'] for p in json.load(open(os.path.join(D, 'places.json')))['places']}
RM = {r['id'] for r in json.load(open(os.path.join(D, 'rooms.json')))['rooms']}
DR = {d['id'] for d in json.load(open(os.path.join(D, 'map.json')))['doors']}
PEOPLE = {p['id'] for p in C.P}
PEOPLE_CANDIE = {p['id']: p['die'] for p in C.P}
COVERED = {'sheila_dunn', 'pauline_kitching', 'ada_vane', 'june_suddaby', 'alison_sedman', 'carol_ellis', 'maureen_jensen', 'brendan_walsh'}
AGES = {p['id']: p['a'] for p in C.P}
fails, warns = [], []
from build_people import parse_rt, parse_days, mins, point_of
import math
ROUT = {p['id']: p for p in C.P}
def slots(pid):
    out = []
    p = ROUT.get(pid)
    if not p or p['rt'] == 'lead':
        return out
    for days, rows in parse_rt(p['rt']):
        for i, (t, pl, act) in enumerate(rows):
            end = mins(rows[i + 1][0]) if i + 1 < len(rows) else 1440
            out.append((parse_days(days), mins(t), end, pl, rows[i - 1][1] if i else None))
    return out
def near(a, b):
    if a == b:
        return True
    pa, pb = point_of(a), point_of(b)
    return bool(pa and pb and math.dist(pa, pb) <= 20)
fit_log = Counter()

WAYS = [('force', r'\b(force|fists|fight|push|hurt|humiliate|beat|blows)\b'), ('key', r'\b(key|keys|locks?|Ian)\b'),
        ('pay', r'\b(pay|paid|buy|money|price|fee|terms)\b'), ('threat', r'(front (him )?up|lean on|defy|threat)'),
        ('back_way', r"(back way|yards' lane|crane gap|side door|the window|back door|in with the contract|back fence|hut at night|cold-store road)"),
        ('talk', r'\b(talk|word|ask|bluff|haggle|introduction|appointment|counter|trade|claim|tell|radio|read|meeting|truce)\b'),
        ('route', r'\b(quay|cab|road|water|on foot|lane|gate|boat|convoy|drive|wheel|chase|by night|at night)\b'),
        ('watch', r'\b(watch|look|follow|stand|sit|wait|hold|presence|routine|tail|from the|window)\b'),
        ('choice', r'.')]
def way_of(text):
    for w, rx in WAYS:
        if re.search(rx, text, re.I):
            return w
    return 'talk'
def keys_of(keys):
    return [{"way": way_of(k), "how": k} for k in keys]
def pay_of(p):
    out = dict(p)
    to = out.get('to')
    if to not in ('pocket', 'tin', 'book'):
        out['to'] = 'tin'
        out.setdefault('pence', 0)
        if to not in (None, 'none'):
            out['paid_to'] = to
    if isinstance(out.get('band'), str):
        out['band_note'] = out.pop('band')
    return out

def place_ok(x, where):
    if x in PL or x in RM or x in DR:
        return True
    if x in PROVISIONAL:
        warns.append('%s: provisional place %s' % (where, x))
        return True
    fails.append('%s: %s is not a places.json, rooms.json or map.json door id' % (where, x))
    return False

def person_ok(x, where):
    if x is None or x in PEOPLE:
        return
    if re.match(r'^[a-z]+_[a-z_]+$', x) and not ' ' in x and x not in ('fare_people',):
        fails.append('%s: %s looks like a person id but is not in people/' % (where, x))

# ---------------- jobs
os.makedirs(os.path.join(D, 'jobs'), exist_ok=True)
for f in glob.glob(os.path.join(D, 'jobs', '*.json')):
    os.remove(f)
for j in JS.JOBS:
    person_ok(j['giver'], 'job ' + j['id'])
    for p in j['people']:
        person_ok(p, 'job ' + j['id'])
    for s in j['steps']:
        place_ok(s['at'], 'job %s step %s' % (j['id'], s['id']))
        if len(s['keys']) != 3:
            fails.append('job %s step %s: %d keys, not three' % (j['id'], s['id'], len(s['keys'])))
        if s['fail'] and s['fail'] not in {t['id'] for t in j['steps']}:
            fails.append('job %s step %s: fail %s is no step' % (j['id'], s['id'], s['fail']))
    if j['kind'] == 'send':
        for p in j['people']:
            if p in COVERED or AGES.get(p, 0) >= 60:
                fails.append('job %s: a send at a covered person %s (RT2-05)' % (j['id'], p))
    rec = {"id": j['id'], "kind": j['kind'], "name": j['name'], "giver": j['giver'], "act_min": j['act_min'], "rung_min": j['rung_min'],
           "when": j['when'] or "the giver's routine puts them where Frank is, and the job's state holds (the story director's card)",
           "window": j['window'], "offer": j['offer'] or [SS.TW],
           "steps": [dict(t, keys=keys_of(t['keys']), lines=[t['words']]) for t in j['steps']], "pay": pay_of(j['pay']), "ledger": j['ledger'], "returns": j['returns'], "people": j['people'],
           "clock": CLOCK, "src": j['src']}
    for extra in ('target', 'man', 'by_path', 'dial_rule', 'fail_rule', 'order', 'people_note'):
        if extra in j:
            rec[extra] = j[extra]
    json.dump(rec, open(os.path.join(D, 'jobs', j['id'] + '.json'), 'w'), indent=1, ensure_ascii=False)

# ---------------- fares
fp = []
prev_w = None
wr = Counter()
for pid, rides in SS.FARES:
    person_ok(pid, 'fare ' + pid)
    if pid not in PEOPLE:
        fails.append('fare person %s is not in people/' % pid)
    rr = []
    for i, (a, b, hours, days, w, lines, cond, src) in enumerate(rides):
        place_ok(a, 'fare %s ride %d from' % (pid, i + 1)); place_ok(b, 'fare %s ride %d to' % (pid, i + 1))
        wr[w] += 1
        rr.append({"id": "%s.%d" % (pid, i + 1), "n": i + 1, "from": a, "to": b, "wrinkle": None if w == 'none' else w,
                   "when": {"hours": hours, "days": days, "offered_when": cond or ("first ride" if i == 0 else "changed by what Frank has done")},
                   "lines": lines if isinstance(lines, list) else [lines], "src": src})
    if len(rr) < 2:
        fails.append('fare %s: fewer than two rides' % pid)
    for r in rr:
        h1, h2 = [mins(x) if x != '24:00' else 1440 for x in r['when']['hours'].split('-')]
        ok = any((r['when']['days'] == 'daily' or (parse_days(r['when']['days']) & ds)) and near(pl, r['to']) and (prev is None or near(prev, r['from']) or r['from'] in ('edge_north', 'edge_west') or prev in ('edge_north', 'edge_west', 'police_station', 'infirmary'))
                 and (h1 <= st <= h2 or (h2 < h1 and (st >= h1 or st <= h2)))
                 for ds, st, en, pl, prev in slots(pid))
        if not ok and r['when']['offered_when'] not in ('first ride', 'changed by what Frank has done'):
            r['scene_ride'] = 'the rider\'s routine is set aside for this ride: a scene, offered only when its condition holds'
            fit_log['scene ride (routine set aside)'] += 1
        elif not ok:
            # fit the ride to a real move in the rider's routine (3.4.1: a fare goes where the routine takes them)
            moves = [(ds, st, pl, prev) for ds, st, en, pl, prev in slots(pid) if prev and prev != pl and not (pl.startswith('edge') and prev.startswith('edge'))]
            if moves:
                used = {(x['from'], x['to']) for x in rr if x is not r}
                moves = [m for m in moves if (m[3], m[2]) not in used] or moves
                ds, st, pl, prev = max(moves, key=lambda m: (m[2] not in ('edge_north', 'edge_west'), m[1] >= 5 * 60, -abs(m[1] - h1)))
                r['fitted_from'] = {'from': r['from'], 'to': r['to'], 'hours': r['when']['hours'], 'days': r['when']['days']}
                r['from'], r['to'] = prev, pl
                r['when']['hours'] = '%02d:%02d-%02d:%02d' % (max(0, st - 30) // 60, max(0, st - 30) % 60, st // 60, st % 60)
                r['when']['days'] = ','.join(d for d in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] if d in ds)
                fit_log['fare ride fitted to the routine'] += 1
            else:
                fails.append('fare %s: no routine move to fit' % r['id'])
    name = next(p['n'] for p in C.P if p['id'] == pid) if pid in PEOPLE else pid
    fp.append({"id": pid, "person": pid, "name": name, "rides": rr, "src": "3.4.1; FIT-G7; " + rr[0]['src']})
if len(fp) < 40:
    fails.append('only %d fare people (3.4.1 asks at least 40)' % len(fp))
if sum(1 for p in fp for r in p['rides'] if r['wrinkle'] is None) != 1:
    fails.append('exactly one ride (the first teaching fare) has no wrinkle (FIT-G7)')
json.dump({"file": "fares.json", "version": "wave2-2026-11-24", "clock": CLOCK,
           "sources": ["BLUEPRINT-03 3.4.1; BLUEPRINT-07 FIT-G7, 7.14", SS.PROTO + " (14 rides with words)", "game-design/side-stories-2026-11-08.md (fares inside side stories)", "STORY-FRAME-2026-11-26", "economy: a fare is 80p plus 1.10 pounds a mile, a quarter more at night and on Sunday"],
           "rules": {"offer": "Pauline calls the fares Frank is offered; each is a named person going where their routine takes them at that hour (routines.json). A fare lasts 1 to 2 real minutes.",
                     "wrinkles": "Every fare after the first teaching fare carries one of seven wrinkles: talker, parcel, tail, runner, wait, hurry, face; never the same wrinkle twice running (7.14) and no fare person rides with the same lines twice in a playthrough (FIT-G7). The fare picker enforces 'twice running'; this file gives each ride its wrinkle.",
                     "pay": "80p flag fall plus 1.10 pounds a mile, a quarter more after 22:00 and on Sunday (economy); drivers keep half of their own fares (choice 1, economy).",
                     "second_ride": "The second ride is offered only once its offered_when holds: changed by what Frank has done."},
           "counts": {"fare_people": len(fp), "rides": sum(len(p['rides']) for p in fp), "wrinkles": dict(wr),
                      "rides_with_words": sum(1 for p in fp for r in p['rides'] if not r['lines'][0].startswith('TO WRITE'))},
           "open_points": ["Lines for most rides are TO WRITE for the story lane; the 14 prototype rides keep their words (renamed for the lead).",
                           "Rides whose from or to is off the Hook (edge_north, police_station, infirmary, copper_row_market) are driven to the soft edge and end there (2.2, soft edges)."],
           "fare_people": fp}, open(os.path.join(D, 'fares.json'), 'w'), indent=1, ensure_ascii=False)

# ---------------- happenings
hh = []
per = Counter()
for kind, where, hours, who, cond, choices, keeps in SS.H:
    if where == 'd_cs_19' and kind == 'locked_out':
        continue  # the Widow is never locked out: a joke for the story lane, not a placed scene
    per[kind] += 1
    place_ok(where, 'happening %s' % kind)
    for w in who:
        person_ok(w, 'happening %s' % kind)
    h1, h2 = [mins(x) if x != '24:00' else 1440 for x in hours.split('-')]
    who2 = []
    for w in who:
        if w in PEOPLE:
            sl = [x for x in slots(w) if near(x[3], where)]
            if not any(x[1] < h2 and x[2] > h1 for x in sl):
                if sl:
                    x = max(sl, key=lambda x: x[2] - x[1])
                    a, b = x[1], min(x[2], x[1] + 120)
                    hours = '%02d:%02d-%02d:%02d' % (a // 60, a % 60, b // 60, b % 60) if b < 1440 else '%02d:%02d-24:00' % (a // 60, a % 60)
                    h1, h2 = a, b
                    fit_log['happening hours fitted to a named person'] += 1
                else:
                    w = 'a passer (in place of %s, who is never at %s)' % (w, where)
                    fit_log['happening person replaced by a passer'] += 1
        who2.append(w)
    who = who2
    hid = '%s.%02d' % (kind, per[kind])
    hh.append({"id": hid, "kind": 'crate_spill' if kind == 'crate' else kind, "what": SS.KINDS[kind],
               "when": {"hours": hours, "state": cond, "note": "placed by the town's state and the hour, never by dice (3.7)"},
               "who": who, "where": where,
               "beats": [{"say": SS.TW + ": the opening, under two minutes in all"}, {"choose": choices}, {"say": SS.TW + ": one line per choice"}],
               "sets": ["happening.%s.done" % hid, "town_keeps:%s" % keeps], "town_keeps": keeps,
               "once": True, "cool_real_minutes": 180,
               "src": "BLUEPRINT-03 3.7; FIT-G6; DEFINITIONS G6 (no scene twice within 3 real hours; none twice in the game unless its people have changed; none twice in 30 minutes or twice in a week on one street)"})
if len(hh) < 60 or len(per) < 8:
    fails.append('happenings: %d over %d kinds (3.7 asks at least 60 over at least 8)' % (len(hh), len(per)))
moves = []
for id, rival, k, where, what, kind, repair in SS.RIVAL_MOVES:
    place_ok(where, 'rival move ' + id)
    moves.append({"id": id, "rival": rival, "kind": k, "where": where, "what": what, "touches": kind,
                  "answers": {"pay": "holds the rival on its rung two game weeks unless Frank does a deed against him", "defy": "climbs the ladder (2.10.1)", "counter": "spends a hook Frank holds"},
                  "repair": repair, "words": SS.TW, "src": "BLUEPRINT-02 2.10.3, RT-06; STORY-FRAME 2 and 5"})
json.dump({"file": "happenings.json", "version": "wave2-2026-11-24", "clock": CLOCK,
           "sources": ["BLUEPRINT-03 3.7; BLUEPRINT-07 FIT-G6, 7.14; DEFINITIONS G6", "BLUEPRINT-02 2.10.3, RT-06 (rival moves)", "routines.json (who is where at the hour)"],
           "kinds": {('crate_spill' if k == 'crate' else k): v for k, v in SS.KINDS.items()}, "counts": {"happenings": len(hh), "by_kind": {('crate_spill' if k == 'crate' else k): v for k, v in per.items()}, "rival_moves": len(moves)},
           "rules": {"placement": "A happening is eligible when its hours and state hold and its people are where routines.json puts them; the director picks among the eligible, never by dice.",
                     "repeat": "No scene twice within 3 real hours (cool_real_minutes 180); none twice in the game unless its people have changed; none twice in 30 minutes or twice in a week on one street.",
                     "return": "A helped stranger can turn up days later with a small favour (3.7).",
                     "content": "No children (a 'lad' is an adult of 18 or more), no alcohol or gambling, no slurs; every scene passes the content gate."},
           "open_points": ["Every happening's words are TO WRITE for the story lane; the structure (who, where, hours, state, choices, what the town keeps) is here.",
                           "One of the eight kinds, the crate, is always at the dock gate by the blueprint's wording; its eight scenes differ by hour and by who is watching."],
           "happenings": hh, "rival_moves": moves}, open(os.path.join(D, 'happenings.json'), 'w'), indent=1, ensure_ascii=False)

# ---------------- side stories
os.makedirs(os.path.join(D, 'side-stories'), exist_ok=True)
for f in glob.glob(os.path.join(D, 'side-stories', '*.json')):
    os.remove(f)
tones = Counter()
KEEP = {3, 4, 6, 9, 11, 23, 25, 27, 31}
for (n, id, title, giver, tone, act, found, steps, ends, tie, offered, waits) in [x for x in SS.SIDE if x[0] <= 32]:
    person_ok(giver, 'side story ' + id)
    place_ok(found[0], 'side story %s found' % id)
    tones[tone] += 1
    st = [{"id": "found", "at": found[0], "who": giver, "verb": "found on foot, no marker", "lines": [found[1]], "next": ["s1"] if steps else ["ends"]}]
    for i, (at, who, verb) in enumerate(steps):
        place_ok(at, 'side story %s step %d' % (id, i + 1)); person_ok(who, 'side story %s step %d' % (id, i + 1))
        st.append({"id": "s%d" % (i + 1), "at": at, "who": who, "verb": verb, "lines": [SS.TW],
                   "next": ["s%d" % (i + 2)] if i + 1 < len(steps) else ["ends"]})
    en = [{"id": "end_%d" % (k + 1), "choice": label, "sets": sets, "town_keeps": keys, "lines": [SS.TW]} for k, (label, sets, keys) in enumerate(ends)]
    rec = {"id": id, "n": n, "title": title, "giver": giver, "tone": tone, "act": act,
           "opens_when": offered, "waits": waits, "empire_tie": tie, "steps": st, "ends": en,
           "selection": "must keep: the frame ties it to a return (STORY-FRAME 4, 5, 7)" if n in KEEP else "one of the 32 drafts of 8 Nov: the story lane cuts to 22 to 28 (3.3), keeping 3, 4, 6, 9, 11, 23, 25, 27 and 31, and writes the step lines. The frame's three new ones (Fifteen pounds, The back room, Five mornings) are main-line jobs (jobs/debt_lee, rita_back_room_front, five_mornings), not side stories",
           "clock": CLOCK, "src": "%s story %d%s" % (SS.SS, n, '' if n <= 32 else ' (new in STORY-FRAME 4)')}
    json.dump(rec, open(os.path.join(D, 'side-stories', id + '.json'), 'w'), indent=1, ensure_ascii=False)

print('jobs', len(JS.JOBS), Counter(j['kind'] for j in JS.JOBS))
print('fare people', len(fp), 'wrinkles', dict(wr))
print('happenings', len(hh), dict(per), 'rival moves', len(moves))
print('side stories', sum(tones.values()), dict(tones))
print('fitted', dict(fit_log))
print('fails', len(fails), 'warnings', len(warns))
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
