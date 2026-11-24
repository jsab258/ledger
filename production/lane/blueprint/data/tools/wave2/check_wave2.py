#!/usr/bin/env python3
"""Cross-file checks for wave 2's files (people, routines, lines, jobs, fares, happenings, side stories), called by
validate_data.py. Returns a list of (ok, message). Written 24 Nov 2026 after the fresh reviews."""
import json, os, re, glob, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..', '..'))

def run():
    out = []
    r = subprocess.run([sys.executable, os.path.join(HERE, 'build_people.py'), '--check-only'], capture_output=True, text=True)
    out.append((r.returncode == 0, 'routines.json: walking reach (CLK-03 cap, bike, car), presence, early starts, whole-stay hours and the finders (tools/wave2/build_people.py --check-only)' + ('' if r.returncode == 0 else ': ' + ' | '.join(l for l in r.stdout.splitlines() if l.startswith('FAIL'))[:600])))
    people = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(os.path.join(D, 'people', '*.json'))}
    sit = json.load(open(os.path.join(D, 'line-situations.json')))
    kinds = set(sit['speaker_kinds']) | set(sit['extra_kinds'])
    cw = json.load(open(os.path.join(D, 'content-words.json')))
    pats = [re.compile(p['pattern'], 0 if p.get('cased') else re.I) for c in cw['categories'] for p in c.get('patterns', [])]
    bad_who, bad_text, tom = [], [], []
    for f in glob.glob(os.path.join(D, 'lines', '*.json')):
        for l in json.load(open(f))['lines']:
            w = l['who']
            if not (w in people or (w.startswith('kind:') and w[5:] in kinds)):
                bad_who.append(l['id'])
            if not l['text'].startswith('TO WRITE') and any(p.search(l['text']) for p in pats):
                bad_text.append(l['id'])
            if not l['text'].startswith('TO WRITE') and re.search(r'\bTom(my)?\b', l['text'] + ' ' + l['situation']):
                tom.append(l['id'])
    out.append((not bad_who, 'lines/: every who is a people id or a kind in line-situations.json' + (': ' + ', '.join(bad_who[:8]) if bad_who else '')))
    out.append((not bad_text, 'lines/: every written text passes content-words.json' + (': ' + ', '.join(bad_text[:8]) if bad_text else '')))
    out.append((not tom, 'lines/: nobody says Tom or Tommy (decision of 24 Nov)' + (': ' + ', '.join(tom[:8]) if tom else '')))
    miss = [pid for pid, p in people.items() if isinstance(p.get('lines', {}).get('own'), str) and p['lines']['own'].startswith('lines/') and not os.path.exists(os.path.join(D, p['lines']['own']))]
    out.append((not miss, 'people/: every lines.own file exists' + (': ' + ', '.join(miss[:8]) if miss else '')))
    pl = {p['id'] for p in json.load(open(os.path.join(D, 'places.json')))['places']} | {r['id'] for r in json.load(open(os.path.join(D, 'rooms.json')))['rooms']} | {d['id'] for d in json.load(open(os.path.join(D, 'map.json')))['doors']}
    prov = set(json.load(open(os.path.join(D, 'routines.json'))).get('provisional_places', {}))
    badp = []
    for f in glob.glob(os.path.join(D, 'jobs', '*.json')):
        badp += ['%s:%s' % (os.path.basename(f), s['at']) for s in json.load(open(f))['steps'] if s['at'] not in pl | prov]
    for h in json.load(open(os.path.join(D, 'happenings.json')))['happenings']:
        if h['where'] not in pl | prov:
            badp.append(h['id'])
    for fp in json.load(open(os.path.join(D, 'fares.json')))['fare_people']:
        for r in fp['rides']:
            for x in (r['from'], r['to']):
                if x not in pl | prov:
                    badp.append(r['id'])
    out.append((not badp, 'jobs, fares, happenings: every place is a places.json, rooms.json or map.json door id' + (': ' + ', '.join(badp[:8]) if badp else '')))
    cover = [pid for pid, p in people.items() if (p['sex'] == 'f' or p['age'] >= 60 or pid == 'brendan_walsh') and p['can_die']]
    out.append((not cover, "people/: Frank's line (women, sixty and over, the priest) means can_die false" + (': ' + ', '.join(cover[:8]) if cover else '')))
    return out

if __name__ == '__main__':
    res = run()
    for ok, m in res:
        print('OK  ' if ok else 'FAIL', m)
    sys.exit(0 if all(ok for ok, _ in res) else 1)
