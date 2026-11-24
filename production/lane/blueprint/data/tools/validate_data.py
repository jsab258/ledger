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
    if isinstance(v, str) and 'minLength' in s and len(v.strip()) < s['minLength']:
        errs.append('%s: shorter than %d' % (path, s['minLength']))
    if isinstance(v, list):
        if 'minItems' in s and len(v) < s['minItems']:
            errs.append('%s: %d items, fewer than %d' % (path, len(v), s['minItems']))
        if 'maxItems' in s and len(v) > s['maxItems']:
            errs.append('%s: %d items, more than %d' % (path, len(v), s['maxItems']))
        for i, (x, xs) in enumerate(zip(v, s.get('tuple', []))):
            validate(x, xs, '%s[%d]' % (path, i), errs)
    if isinstance(v, dict) and 'oneKeyOf' in s and sum(1 for k in s['oneKeyOf'] if k in v) != 1:
        errs.append('%s: needs exactly one of %s' % (path, s['oneKeyOf']))
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
rev = {x.get('id') for x in (S.get('rooms') or {}).get('reverbs', []) if isinstance(x, dict)}
rkind = {x.get('room_kind') for x in (S.get('rooms') or {}).get('reverbs', []) if isinstance(x, dict)}
ok(len(rev) >= 8, 'sounds.json holds reverb for the eight room kinds (%d)' % len(rev))
badrev = sorted({str(x.get('reverb_id')) for x in R.get('rooms', []) if x.get('reverb_id') not in rev and x.get('reverb_id') not in (None, 'none')})
ok(not badrev, 'every room reverb id is in sounds.json (%s)' % badrev)
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
    if isinstance(c, dict) and c.get('id') in ('alcohol', 'gambling', 'children', 'drugs', 'sex', 'cruelty'):
        for p in c.get('patterns', []):
            pat = p if isinstance(p, str) else p.get('pattern', '')
            cased = isinstance(p, dict) and p.get('cased')
            try:
                pats.append((c['id'], re.compile(pat if cased else pat, 0 if cased else re.I)))
            except re.error:
                pass
hits = []
TEXT_KEYS = ('text', 'tom', 'truth', 'headline', 'body', 'label', 'said', 'line', 'lines', 'title', 'name', 'label_text', 'landmark', 'which_text', 'string', 'wording')
for f in ('ui-text.json', 'ledger-texts.json', 'letters-and-print.json', 'places.json', 'sounds.json', 'rooms.json', 'timetables.json', 'crowd.json', 'vehicles.json', 'police.json'):
    def ct(k, v, path, f=f):
        if k in TEXT_KEYS and isinstance(v, str):
            for cat, p in pats:
                if p.search(v):
                    hits.append((f, path, cat, p.pattern, v[:50]))
    if f in data:
        walk(data[f], ct)
ok(not hits, 'no drink, gambling or children word in player-facing text (%d hits, e.g. %s)' % (len(hits), hits[:3]) if pats else 'content patterns loaded')

# ---- hand rules: what a format cannot say
U = data.get('ui-text.json', {})
def prompt_records(o, acc):
    if isinstance(o, dict):
        if isinstance(o.get('id'), str) and o['id'].startswith('prompt.'):
            acc.append(o)
        for v in o.values():
            prompt_records(v, acc)
    elif isinstance(o, list):
        for v in o:
            prompt_records(v, acc)
    return acc
prs = prompt_records(U.get('prompts', {}), [])
ok(len(prs) >= 100 and all(isinstance(p.get('text'), str) and p['text'].strip() for p in prs if 'text' in p) and all(('text' in p) or ('which_text' in p) or ('tpl' in p) or ('template' in p) for p in prs),
   'ui-text: %d prompts, every one with words' % len(prs))
ai = U.get('ai_notice') or {}
ok(bool(ai) and len(json.dumps(ai)) > 200, 'ui-text: the AI notice is present (RULINGS 24 Sep)')
ok(isinstance(U.get('save_slots', {}).get('manual_slots'), int) and U['save_slots']['manual_slots'] >= 3 and U['save_slots'].get('autosave_slots', 0) >= 2,
   'ui-text: at least three manual saves and rotating autosaves (AX-07)')
ok(isinstance(U.get('subtitles', {}).get('floor_units'), (int, float)) and U['subtitles']['floor_units'] >= 24, 'ui-text: subtitles never below 24 units (AX-01)')
clash = []
for ctx, rows in ((r.get('context'), r) for r in (U.get('keys', {}).get('actions') or [])):
    pass
acts = U.get('keys', {}).get('actions') or []
seen = {}
for a in acts:
    for dev in ('key', 'pad'):
        k = a.get(dev)
        if not k:
            continue
        for ctx in (a.get('contexts') or [a.get('context')]):
            sig = (dev, ctx, str(k), bool(a.get('hold')))
            if sig in seen and seen[sig] != a.get('id'):
                clash.append((seen[sig], a.get('id'), sig))
            seen[sig] = a.get('id')
ok(not clash, 'ui-text: no key or button clash within a context (%s)' % clash[:3])
bad_ui = []
def ui_words(k, v, p):
    if k in ('text', 'label', 'which_text', 'title') and isinstance(v, str) and re.search(r'\b(minimap|waypoint|quest marker|objective marker|reputation|xp|level up|difficulty)\b', v, re.I):
        bad_ui.append((p, v[:40]))
walk(U, ui_words)
ok(not bad_ui, 'ui-text: no minimap, waypoint, marker, reputation, levels or difficulty in player text (RULINGS) (%s)' % bad_ui[:3])
# content: the gate's own rules, exactly
cs_path, up = None, D
for _ in range(8):
    cand = os.path.join(up, 'ledger', 'Assets', 'Scripts', 'Core', 'ContentWords.cs')
    if os.path.exists(cand):
        cs_path = cand
        break
    up = os.path.dirname(up)
ok(cs_path is not None, 'content-words: the gate source ContentWords.cs is found in the repository')
if cs_path:
    cs = open(cs_path).read()
    gate = set(r for r in re.findall(r'new Rule\("([a-z_]+)",\s*"([^"]+)",\s*(true|false),\s*@"((?:[^"]|"")*)"\)', cs) if r[0] != 'slur')   # slurs are held by reference only
    mine = set()
    for c in CW.get('categories', []):
        for p in c.get('patterns', []):
            if isinstance(p, dict) and 'ContentWords' in str(p.get('src', '')):
                mine.add((c['id'], p.get('id'), 'true' if p.get('cased') else 'false', p.get('pattern', '').replace('"', '""')))
    ok(len(gate) > 50 and gate == mine, 'content-words: the gate patterns equal ContentWords.cs exactly (%d in the gate, %d here, %d differ)' % (len(gate), len(mine), len(gate ^ mine)))
bad_re = []
for c in CW.get('categories', []):
    for p in c.get('patterns', []):
        pat = p.get('pattern', '') if isinstance(p, dict) else p
        try:
            re.compile(pat)
        except re.error as e:
            bad_re.append((c.get('id'), pat))
ok(not bad_re, 'content-words: every pattern compiles (%s)' % bad_re[:3])
cats = {c.get('id') for c in CW.get('categories', [])}
ok({'alcohol', 'gambling', 'children'} <= cats, 'content-words: the alcohol, gambling and children categories exist')
# sounds: licences, file references, no thinking cue
S = data.get('sounds.json', {})
fids = {f['id'] for f in S.get('files', [])}
lic = sorted({f.get('licence') for f in S.get('files', [])})
ok(lic == ['CC0'], 'sounds: every file CC0 (D56) (%s)' % lic)
badf = [x.get('id') for x in S.get('sound_list', []) for fid in (x.get('file_ids') or []) if fid not in fids and not str(fid).startswith('see ')]
ok(not badf, 'sounds: every sound names files that exist (%s)' % badf[:4])
ok(not re.search(r'thinking', json.dumps([x.get('id', '') + ' ' + x.get('name', '') for x in S.get('sound_list', [])]), re.I), 'sounds: no thinking cue (ruling 24 Nov)')
print('data files: %d checks passed, %d failed' % (len(OK), len(FAIL)))
for m in FAIL:
    print('FAIL', m)
if '-v' in sys.argv:
    for m in OK:
        print('ok  ', m)
sys.exit(1 if FAIL else 0)
