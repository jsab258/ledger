"""Run 4, steps (b) and (c): statuses of design pass 3 into coverage.json. Safe to rerun."""
import json, os
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(here, 'coverage.json'); d = json.load(open(p)); R = d['rows']; byid = {r['id']: r for r in R}
DEF = 'DEFINITIONS-2026-11-21.md, design pass 3 (run 4)'
rt2 = {  # id: (status, real_basis or note)
 'RT2-01': ('DECIDED',''), 'RT2-02': ('DECIDED',''), 'RT2-03': ('DECIDED',''),
 'RT2-04': ('PENDING','story measure, by Sat 28 Nov (Act III shape, with RT-01); the rule stands as DECIDED inside his ending rulings'),
 'RT2-05': ('DECIDED',''), 'RT2-06': ('DECIDED',''), 'RT2-07': ('DECIDED',''), 'RT2-08': ('DECIDED',''),
 'RT2-09': ('DECIDED',''), 'RT2-10': ('DECIDED',''), 'RT2-11': ('DECIDED',''), 'RT2-12': ('DECIDED',''),
 'RT2-13': ('DECIDED',''), 'RT2-14': ('PENDING','1990 prices from dated sources with G8, cloud, by Thu 26 Nov'),
 'RT2-15': ('PENDING','story measure, by Sat 28 Nov (Act III shape, with RT-01)'),
 'RT2-16': ('DECIDED',''), 'RT2-17': ('DECIDED',''), 'RT2-18': ('DECIDED',''), 'RT2-19': ('DECIDED',''),
 'RT2-20': ('DECIDED',''), 'RT2-21': ('DECIDED',''), 'RT2-22': ('DECIDED',''),
}
for i,(st,b) in rt2.items():
    r = byid[i]; r['status'] = st; r['defined_in'] = DEF + ', ' + i; r['standard'] = 'see ' + DEF + ', ' + i
    r['test'] = 'B (bot), as written under ' + i; r['standard_source'] = 'design pass 3, ' + i; r['run4'] = 'b'
    r.pop('real_basis', None)
    if st == 'MEASURED': r['real_basis'] = b; r['basis'] = 'rests on canon (see definition); inputs the design\'s'
    elif st == 'DECIDED': r['basis'] = 'design decision; his to overturn (run 4)'
    else: r['basis'] = 'PENDING: ' + b
    r['closed_by'] = 'design pass 3 (run 4, 21 Nov)' if st != 'PENDING' else b
new = [
 ('FIT-G1','The Hook\'s road plan in metres, the chase loop','DECIDED','',"crossings 560 m by road, 470 m on foot; chase loop 1,540 m; GD-01's bands PENDING the reference crossings"),
 ('FIT-G2','Car speeds and the stop band','DECIDED','','30 mph limit (RTRA 1984 s.81) and 23 m stopping distance (Highway Code); the 50 mph stop band the design\'s'),
 ('FIT-G3','A chase at the soft edge','DECIDED','',''),
 ('FIT-G4','Tom\'s, the constables\' and the runner\'s speeds','PENDING','','reference walk and run speeds from footage, PC block 2, 24 to 26 Nov'),
 ('FIT-G5','The beat constable\'s round','DECIDED','',''),
 ('FIT-G6','How many street happenings are written','DECIDED','',''),
 ('FIT-G7','How many fare people are written','DECIDED','',''),
 ('FIT-G8','Prices of what money buys','PENDING','','1990 prices from dated sources, cloud, by Thu 26 Nov; GD-07 money curve, PC 23 to 28 Nov'),
 ('FIT-G9','Crowd counts by hour and place','PENDING','','2.1.2 hourly figure (ONS tables), cloud, by Thu 26 Nov'),
 ('FIT-G10','Opening hours, day and night','DECIDED','',''),
 ('FIT-F03','What the 70 m of a lost chase means','DECIDED','',''),
 ('FIT-F13','Act II\'s week count and its fail-safe','PENDING','','his C11 (7 weeks under A, 5 under B)'),
 ('FIT-F15','What the act hours include (side stories inside 15 to 20 h)','MEASURED','his ruling or canon','his length ruling; the split is the advisor\'s D-Q3'),
 ('FIT-F20','Which fares carry a wrinkle (every one after the first)','DECIDED','','the description\'s reading of canon\'s line of 19 Nov'),
 ('FIT-F04','Chase length against the reference games (GTA IV in Mafia DE\'s place)','PENDING','','PC block 4, 26 to 28 Nov, about 2 h'),
 ('FIT-F05','How often the one-hit wreck happens in ordinary driving','PENDING','','cloud 1 h with the next prototype build'),
 ('FIT-F16','Act hours against places and people','PENDING','','GD-02 density band, PC block 3, 25 to 27 Nov'),
 ('FIT-F19','Enough shared-line situations live each hour','PENDING','','cloud 0.5 h, by Thu 26 Nov'),
 ('FIT-F24','Money over nine weeks (in against out)','PENDING','','economy bot once G8 prices are in, cloud 2 h, by Sat 28 Nov'),
 ('FIT-F32','Something within 30 s by day','PENDING','','cloud 0.5 h with the next prototype build'),
 ('FIT-P04','The struck person\'s fall','DECIDED','','inside canon: a car hurts, never kills'),
 ('FIT-P09','Music made for the game, placed in the world','MEASURED','his ruling or canon','canon: every band fictional; the allowlist'),
 ('FIT-P17','At least five kinds of fighter','DECIDED','',''),
 ('FIT-P18','Two against one stays deadly','DECIDED','',''),
 ('FIT-P34','At least 24 rooms open','DECIDED','',''),
 ('FIT-P45','Birds and animals','DECIDED','',''),
 ('FIT-P52','What an ordinary drawer holds','DECIDED','',''),
 ('FIT-L01','60 street lines for the 12 people seen most, 30 for the rest','DECIDED','','advisor D-Q4'),
]
clk = [('CLK-01','The staged first hour against the landing\'s window'),('CLK-02','The hurry wrinkle in clock terms'),
 ('CLK-03','Routines against walking'),('CLK-04','Job windows against the walk to them'),('CLK-05','The evening and the shop day'),
 ('CLK-06','Calendar and acts'),('CLK-07','Weekly rhythms (rent, cooling, rival rungs)')]
for i,n in clk: new.append((i,n,'PENDING','','his answer to C11 (A 45 s an hour or B 60 s; both written)'))
for i,n,st,rb,note in new:
    r = byid.get(i) or {'id': i}
    r.update({'name': n, 'group': 'Fit check of 21 Nov' if i.startswith('FIT') else 'The clock (his C11)', 'felt': True,
      'defined_in': DEF + ', ' + i.replace('FIT-','').replace('L01','L-01'), 'standard': 'see ' + DEF, 'test': 'B (bot) as written',
      'standard_source': 'design pass 3; FIT-CHECK-2026-11-21.md', 'research': [], 'status': st,
      'basis': (note or ('design decision; his to overturn (run 4)' if st=='DECIDED' else '')), 'closed_by': 'design pass 3 (run 4, 21 Nov)' if st!='PENDING' else note,
      'source': 'fit check' if i.startswith('FIT') else 'fit check, clock', 'run4': 'b' if i.startswith('FIT') else 'c'})
    r.pop('real_basis', None)
    if st == 'MEASURED': r['real_basis'] = rb
    if i not in byid: R.append(r); byid[i] = r
# clock rows pending his answer
r = byid['7.13']; r['status'] = 'PENDING'; r['basis'] = 'PENDING his answer to C11; both versions written (design pass 3, the clock)'; r['run4'] = 'c'
# AX-03 field of view now ruled
r = byid['AX-03']; r['basis'] = (r.get('basis','') + '; field of view a setting 75 to 100, default 86: his ruling, 21 Nov').strip('; ')
from collections import Counter
c = Counter(x['status'] for x in R)
rb = Counter(x.get('real_basis') for x in R if x['status']=='MEASURED')
d['counts'] = {'rows': len(R), **{s: c.get(s,0) for s in d['statuses']},
  'MEASURED_by_real_basis': dict(rb), 'MEASURED_on_reference_or_real_world_figures': rb['reference game'] + rb['real-world figure or published standard'],
  'as_of': '2026-11-21, run 4'}
d['made'] = d.get('made','') if 'run 4' in d.get('made','') else (d.get('made','') + '; updated by run 4, 21 Nov 2026')
json.dump(d, open(p,'w'), indent=1, ensure_ascii=False)
print(d['counts'])
