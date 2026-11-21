"""Run 3: apply row changes by step. Safe to rerun (sets fields)."""
import json, sys, os
H = os.path.dirname(os.path.abspath(__file__)) + '/..'
d = json.load(open(H + '/coverage.json'))
rows = {r['id']: r for r in d['rows']}
CH = json.load(open(H + '/scripts/run3_changes.json'))
for step in sys.argv[1:]:
    for rid, upd in CH[step].items():
        if rid.startswith('+'):
            new = dict(upd); new['id'] = rid[1:]; new['run3'] = step
            if new['id'] not in rows: d['rows'].append(new); rows[new['id']] = new
            continue
        r = rows[rid]; r.update(upd); r['run3'] = step
from collections import Counter
c = Counter(r['status'] for r in d['rows'])
d['counts'] = {'rows': len(d['rows']), **{k: c.get(k, 0) for k in ['MEASURED','PENDING','UNMEASURED','UNDEFINED','OUT','OUTSIDE']}}
json.dump(d, open(H + '/coverage.json', 'w'), indent=1, ensure_ascii=False)
print(d['counts'])
