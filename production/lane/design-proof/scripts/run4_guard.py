"""Run 4, step (a): the pre-mortem guard. MEASURED stays MEASURED only when the
standard rests on a real figure: a reference game's measured number, a dated
real-world figure (or a published standard with a date), or a pass-or-fail rule
of his (his ruling, canon, his D-numbered decisions). Everything else that was
MEASURED becomes DECIDED (a design decision he may overturn). Safe to rerun."""
import json, re, os
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(here, 'coverage.json')
d = json.load(open(p))
# per-row judgements read by hand on 21 Nov (run 4); key -> real basis
manual = {
 # reference figures
 **{k: 'reference game' for k in ['1.2.11','1.3.5','1.3.12','1.6.12','1.6.13','1.6.14','2.4.1','2.4.2','2.4.4',
     '2.5.4','2.5.5','2.6.10','2.11.4','3.2.4','3.2.7','3.3','7.2','7.3','8.3.1','GD-04']},
 # dated real-world figures or published standards with a date
 **{k: 'real-world figure or published standard' for k in ['2.6.4','2.7.4','2.7.6','8.2.1','10.11','RT-14',
     'AX-01','AX-02','AX-03','AX-04','AX-05','AX-06','AX-08','AX-09','AX-11']},
}
# rows whose source names only DESIGN sections or open questions despite a "ruling" basis label
force_decided = {'1.2.10','2.14','7.16','1.2.9','AX-07','AX-10'}
his_pat = re.compile(r'ruling|RULINGS|canon|\bD\d+\b|his combat design', re.I)
for r in d['rows']:
    if r.get('run4_was') == 'MEASURED' and r['status'] in ('MEASURED', 'DECIDED'):
        r['status'] = 'MEASURED'  # rerun from the original state
    if r['status'] != 'MEASURED':
        continue
    r['run4_was'] = 'MEASURED'
    src = r.get('standard_source', '') + ' ' + r.get('basis', '')
    if r['id'] in manual:
        r['real_basis'] = manual[r['id']]
    elif r['id'] not in force_decided and his_pat.search(r.get('standard_source', '')) \
            and 'design decision' not in r.get('basis', ''):
        r['real_basis'] = 'his ruling or canon'
    else:
        r['status'] = 'DECIDED'
        r['real_basis'] = ''
        r['decided_note'] = 'design decision; his to overturn (run 4 guard)'
if 'DECIDED' not in d['statuses']:
    d['statuses'].insert(1, 'DECIDED')
d['note'] = d.get('note', '') + ' Run 4 (21 Nov): DECIDED = defined with a pass-or-fail standard that is a design decision, his to overturn; MEASURED now means the standard rests on a real figure (real_basis says which).' if 'Run 4' not in d.get('note', '') else d['note']
json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
from collections import Counter
c = Counter(r['status'] for r in d['rows'])
rb = Counter(r.get('real_basis') for r in d['rows'] if r['status'] == 'MEASURED')
print(c); print(rb)
