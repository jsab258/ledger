#!/usr/bin/env python3
"""Validate every blueprint data file against schemas.json, then the cross-file checks.
No library needed. Usage: python3 validate_data.py [-v]. Exit 1 on any failure. Written 24 Nov 2026.
Files still to come (people/, ties.json, routines.json, lines/, jobs/, fares.json, happenings.json,
side-stories/, scenes/) are tested by their schema the moment they exist."""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..'))
SC = json.load(open(os.path.join(D, 'schemas.json')))
FAIL, OK = [], []

def ok(c, m):
    (OK if c else FAIL).append(m)

TYPES = {'null': lambda v: v is None, 'boolean': lambda v: isinstance(v, bool), 'integer': lambda v: isinstance(v, int) and not isinstance(v, bool),
         'number': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool), 'string': lambda v: isinstance(v, str),
         'array': lambda v: isinstance(v, list), 'object': lambda v: isinstance(v, dict)}

def validate(v, s, path, errs):
    if len(errs) > 20:
        return
    t = s.get('type')
    if t:
        ts = t if isinstance(t, list) else [t]
        if not any(TYPES[x](v) for x in ts):
            errs.append('%s: %s is not %s' % (path, type(v).__name__, '/'.join(ts)))
            return
    if 'enum' in s and v not in s['enum']:
        errs.append('%s: %r not in %s' % (path, v, s['enum']))
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if 'minimum' in s and v < s['minimum']:
            errs.append('%s: %s below %s' % (path, v, s['minimum']))
        if 'maximum' in s and v > s['maximum']:
            errs.append('%s: %s above %s' % (path, v, s['maximum']))
    if isinstance(v, str) and 'pattern' in s and not re.search(s['pattern'], v):
        errs.append('%s: %r does not match %s' % (path, v, s['pattern']))
    if isinstance(v, dict):
        for k in s.get('required', []):
            if k not in v:
                errs.append('%s: missing %s' % (path, k))
        props = s.get('properties', {})
        for k, x in v.items():
            if k in props:
                validate(x, props[k], path + '.' + k, errs)
            elif isinstance(s.get('additionalProperties'), dict):
                validate(x, s['additionalProperties'], path + '.' + k, errs)
    if isinstance(v, list) and 'items' in s:
        for i, x in enumerate(v):
            validate(x, s['items'], '%s[%d]' % (path, i), errs)

data = {}
for name, s in SC['files'].items():
    p = os.path.join(D, name)
    if not os.path.exists(p):
        ok(False, '%s exists' % name)
        continue
    d = json.load(open(p))
    data[name] = d
    errs = []
    validate(d, s, name, errs)
    ok(not errs, '%s matches its format%s' % (name, (': ' + '; '.join(errs[:6])) if errs else ''))
    ok((d.get('clock') or {}).get('realSecondsPerGameHour') == 120, '%s is on the 120 s hour' % name)
for pat, s in SC['files_to_come'].items():
    files = glob.glob(os.path.join(D, pat.replace('<id>', '*').replace('<file>', '*')))
    for p in files:
        errs = []
        validate(json.load(open(p)), s, os.path.relpath(p, D), errs)
        ok(not errs, '%s matches %s%s' % (os.path.relpath(p, D), pat, (': ' + '; '.join(errs[:6])) if errs else ''))
    if not files:
        OK.append('%s: not made yet (waits on the story)' % pat)

# ---- cross-file checks
M = data.get('map.json', {})
doors = {d['id'] for d in M.get('doors', [])}
plots = {p['id'] for p in M.get('plots', [])}
roads = {r['id'] for r in M.get('roads', [])}
nodes = {n['id'] for n in M.get('graph', {}).get('nodes', [])}
mplaces = {p['place'] for p in M.get('plots', []) if p.get('place')}

def walk(o, fn, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            fn(k, v, path + '.' + k)
            walk(v, fn, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, fn, '%s[%d]' % (path, i))

for f in ('rooms.json', 'places.json', 'police.json', 'vehicles.json', 'crowd.json', 'timetables.json'):
    bad = []
    def fn(k, v, path):
        if k in ('door', 'doors') and v is not None:
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, str) and x.startswith('d_') and x not in doors:
                    bad.append((path, x))
        if k in ('plot',) and isinstance(v, str) and v not in plots:
            bad.append((path, v))
        if k in ('road', 'road_id') and isinstance(v, str) and v not in roads:
            bad.append((path, v))
        if k in ('node', 'nodes', 'route', 'waypoints') and v is not None:
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, str) and (x.startswith('j_') or x.startswith('n_')) and x not in nodes:
                    bad.append((path, x))
    if f in data:
        walk(data[f], fn)
        ok(not bad, '%s: every door, plot, road and graph node it names is in map.json%s' % (f, (' (%s)' % bad[:5]) if bad else ''))

P = data.get('places.json', {})
pids = {p['id'] for p in P.get('places', [])}
ok(mplaces <= pids, 'every map place has a places.json record (missing %s)' % sorted(mplaces - pids)[:8])

R = data.get('rooms.json', {})
ui = data.get('ui-text.json', {})
prompt_ids = set()
walk(ui, lambda k, v, p: prompt_ids.add(v) if k == 'id' and isinstance(v, str) and v.startswith('prompt.') else None)
needed = set(x if isinstance(x, str) else x.get('id') for x in R.get('new_prompts_needed', []))
missing = set()
def rp(k, v, p):
    if k in ('prompt', 'prompt_id') and isinstance(v, str) and v.startswith('prompt.') and v not in prompt_ids and v not in needed:
        missing.add(v)
walk(R, rp)
ok(not missing, 'every room prompt is in ui-text.json or listed as needed (%s)' % sorted(missing)[:8])
S = data.get('sounds.json', {})
rev = set()
walk(S, lambda k, v, p: rev.update(v.keys()) if k in ('reverb', 'reverb_kinds', 'room_reverb') and isinstance(v, dict) else None)
walk(S, lambda k, v, p: [rev.add(x.get('id') or x.get('kind')) for x in v if isinstance(x, dict)] if k in ('reverb', 'reverb_kinds', 'room_reverb') and isinstance(v, list) else None)
badrev = set()
walk(R, lambda k, v, p: badrev.add(v) if k in ('reverb', 'reverb_kind') and isinstance(v, str) and v not in rev and v != 'none' else None)
ok(not badrev, 'every room reverb kind is in sounds.json (%s)' % sorted(badrev))
T = data.get('tune.json', {})
tkeys = {n['key'] for n in T.get('numbers', [])}
refs = {}
for f, d in data.items():
    s = json.dumps(d)
    for m in re.findall(r'tune:([a-z0-9_.*]+)', s):
        if '*' not in m:
            refs.setdefault(m, f)
unk = {k: f for k, f in refs.items() if k not in tkeys}
ok(not unk, 'every tune: reference names a tune.json key (%d unknown, e.g. %s)' % (len(unk), list(unk.items())[:4]))
svg = open(os.path.join(D, 'paper-map.svg')).read() if os.path.exists(os.path.join(D, 'paper-map.svg')) else ''
marks = set(re.findall(r'data-place="([a-z0-9_]+)"', svg))
ok(mplaces <= marks, 'the paper map has a mark for every map place (missing %s)' % sorted(mplaces - marks)[:6])
ok('visibility="hidden"' in svg and svg.count('visibility="visible"') <= 3, 'the paper map hides unknown places (only Mickey\'s and the edges shown at the start)')
top = open(os.path.join(D, 'map-topdown.svg')).read() if os.path.exists(os.path.join(D, 'map-topdown.svg')) else ''
ok('render_map.py' in top, 'map-topdown.svg was drawn from map.json by render_map.py')
# content: the forbidden-word patterns over player-facing text fields
CW = data.get('content-words.json', {})
pats = []
for c in CW.get('categories', []):
    if isinstance(c, dict) and c.get('id') in ('alcohol', 'gambling', 'children'):
        for p in c.get('patterns', []):
            pats.append((c['id'], p if isinstance(p, str) else p.get('pattern', '')))
hits = []
TEXT_KEYS = ('text', 'tom', 'truth', 'headline', 'body', 'label', 'said', 'line', 'lines', 'title')
for f in ('ui-text.json', 'ledger-texts.json', 'letters-and-print.json', 'places.json', 'sounds.json'):
    def ct(k, v, path, f=f):
        if k in TEXT_KEYS and isinstance(v, str):
            low = v.lower()
            for cat, p in pats:
                if p and re.search(p, low):
                    hits.append((f, path, cat, p))
    if f in data:
        walk(data[f], ct)
ok(not hits, 'no drink, gambling or children word in player-facing text (%d hits, e.g. %s)' % (len(hits), hits[:3]) if pats else 'content patterns loaded')

print('data files: %d checks passed, %d failed' % (len(OK), len(FAIL)))
for m in FAIL:
    print('FAIL', m)
if '-v' in sys.argv:
    for m in OK:
        print('ok  ', m)
sys.exit(1 if FAIL else 0)
