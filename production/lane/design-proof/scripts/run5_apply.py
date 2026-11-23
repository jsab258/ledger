# Run 5 (23 Nov 2026): design pass 4 into coverage.json. Safe to rerun.
import json, os
from collections import Counter
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(here, 'coverage.json'); d = json.load(open(p)); R = d['rows']; byid = {r['id']: r for r in R}
DEF = 'DEFINITIONS-2026-11-21.md, design pass 4 (run 5)'
def setrow(i, st, basis, rb=None, **kw):
    r = byid[i]; r['status'] = st; r['basis'] = basis; r['run5'] = 'pass 4'
    r.pop('real_basis', None)
    if st == 'MEASURED': r['real_basis'] = rb
    r.update(kw)
for i in ['CLK-01','CLK-02','CLK-03','CLK-04','CLK-05','CLK-06','CLK-07','FIT-F13']:
    setrow(i, 'MEASURED', 'his ruling of 21 Nov: clock B, 60 s a game hour, Act II about 5 weeks (' + DEF + ')', 'his ruling or canon',
           standard='see ' + DEF + ', the clock', closed_by='his ruling of 21 Nov (run 5)')
setrow('7.13', 'MEASURED', 'his ruling of 21 Nov: 60 s a game hour, 24 real minutes a day', 'his ruling or canon',
       standard='60 real s a game hour, 24 real minutes a day, evening 6 real minutes (references 48 to 144 minutes a day, CLOUD-FIGURES C2); no file still says 45 s', closed_by='his ruling of 21 Nov (run 5)')
setrow('1.2.3', 'MEASURED', 'GTA VI five parked-car entries, uncut, dated, SOLID (one player)', 'reference game',
       standard='a car Tom may open: door to seated 1.5 to 2.5 s, moving within 1 s after; out under 2 s; forced entry of a locked car about 6 s; a blocked door never traps (ER-DRIVE-07)',
       standard_source='STATUS.md and gtavi-driving-builder-2026-11-21 (SOLID); description section 23', closed_by='design pass 4 (run 5)')
setrow('GD-02', 'PENDING', 'band DECIDED (12 to 20 in the busiest view) until five-sample counts of GTA VI, KCD2 (installed) and the 1990 archive; ' + DEF,
       standard='busiest view (Quay Street parade front) at its busiest hour 12 to 20 distinct people (above GTA VI counted street views about 10, a lead; ceiling inside the 1990 archive event night); things per street minute within the teardown band; no shared street line twice in one real hour')
setrow('FIT-G9', 'PENDING', 'bands rescaled to GD-02 (' + DEF + '); five-sample counts and 2.1.2 hourly figure pending')
setrow('FIT-F04', 'PENDING', 'chase lengths: the 19 chases of the chase sheet are leads (floors at 7 to 67 s steps); five-sample lengths in PC block 1 and the feel block, 23 to 27 Nov')
new = [
 ('DP5-C01', 'A chase has no timer (car and foot)', 'DECIDED', 'raised by GTA VI: chases end lost, caught, wrecked or at the edge, never by a clock; replaces "within 90 real seconds"; his to overturn'),
 ('DP5-C02', 'Chase length on the Hook\'s loops', 'PENDING', 'band 60 to 120 s median, 90th percentile under 240 s (car), foot 30 to 90 s; five-sample chase lengths, PC block 1 and feel block, 23 to 27 Nov'),
 ('DP5-C03', 'The search after a chase is lost', 'PENDING', 'band 30 to 120 s; sighting inside resumes the same chase; five-sample search lengths (GTA VI being seen), PC block 1, 23 to 24 Nov'),
]
for i, n, st, note in new:
    r = byid.get(i) or {'id': i}
    r.update({'name': n, 'group': 'What the player does with his hands', 'felt': True, 'defined_in': DEF + ', the chase',
              'standard': 'see ' + DEF + ', the chase', 'test': 'B: seeded chase set, lengths logged',
              'standard_source': 'car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13',
              'research': [], 'status': st, 'basis': note, 'closed_by': 'design pass 4 (run 5)' if st != 'PENDING' else note,
              'source': 'run 5, chase sheet', 'run5': 'pass 4', 'parent': '1.5.3, 2.6.10'})
    r.pop('real_basis', None)
    if i not in byid: R.append(r); byid[i] = r
r = byid['RT-04']; r['basis'] = (r.get('basis', '') + '; fail-safe now from four game days before the end of Act II week 5 (clock B, run 5)').strip('; ')
c = Counter(x['status'] for x in R)
rb = Counter(x.get('real_basis') for x in R if x['status'] == 'MEASURED')
d['counts'] = {'rows': len(R), **{s: c.get(s, 0) for s in d['statuses']},
  'MEASURED_by_real_basis': dict(rb), 'MEASURED_on_reference_or_real_world_figures': rb['reference game'] + rb['real-world figure or published standard'],
  'as_of': '2026-11-23, run 5'}
if 'run 5' not in d.get('made', ''): d['made'] = d.get('made', '') + '; updated by run 5, 23 Nov 2026'
json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
print(d['counts'])
