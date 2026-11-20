# Run 2, step (c): how and when every UNMEASURED row gets measured.
import json,collections
OUT='/home/claude/ledger/production/lane/design-proof'
d=json.load(open(OUT+'/coverage.json')); b={r['id']:r for r in d['rows']}
P={
 'GV':('GTA VI footage pass (his ruling 22:08, 20 Nov: the full pass), first in the order','PC, Mon 23 to Tue 24 Nov'),
 'FEEL':('feel measuring block already in the order (FEEL-MEASUREMENT-METHOD-2026-11-20), with GTA VI as a fourth game','PC, 23 to 26 Nov'),
 'TEAR':('teardown: an hour of each reference game coded by the twelve kinds (TEARDOWN-BRIEF, Mafia replaced by GTA IV) and the hour split','PC, 25 to 28 Nov'),
 'A':('MEASUREMENTS-NEEDED A: an extra row on the feel sheets, same method','PC, 26 to 28 Nov'),
 'SND':('MEASUREMENTS-NEEDED A7: the listening pass on the teardown\'s town pieces','PC, 27 to 28 Nov'),
 'B':('MEASUREMENTS-NEEDED B: 1990 period sources, read in full','cloud, Sat 21 to Tue 24 Nov'),
 'PUB':('MEASUREMENTS-NEEDED C: published guides and wikis for the reference games\' figures','cloud, Sat 21 to Wed 25 Nov'),
 'TEST':('design pass 2: the row\'s pointer replaced by a pass-or-fail test from the description\'s own numbers (no measuring needed; then MEASURED)','cloud, next run (Sat 21 Nov)'),
 'STORY':('the story measure: the measured story fixes its content and counts','cloud, by Sat 28 Nov 12:00'),
 'SET':('a labelled test set built and run in the cloud','cloud, by Thu 26 Nov'),
 'PANEL':('the panel of eight kinds of player on the built prototype (M1); its bar figure from the players study','after the one-shot, from about 3 Dec; the bar itself from the players study by the next run'),
}
plan={
 '1.1.4':'A','1.1.6':'A','1.2.6':'A','1.3.10':'A','1.6.2':'A','2.1.5':'A','7.13':'PUB','8.10':'TEST',
 '1.1.7':'TEAR','1.2.7':'TEAR','1.6.3':'TEAR','1.6.4':'TEAR','1.6.5':'TEAR','1.6.6':'TEAR','1.7.1':'TEAR','1.7.3':'TEAR','2.2.6':'TEAR','2.9.1':'TEAR','2.12.4':'TEAR','2.12.5':'TEAR','2.15.1':'TEAR','2.18':'TEAR','3.4.1':'TEAR','3.4.2':'TEAR','3.5.1':'TEAR','3.6.4':'TEAR','5.8.3':'TEAR','6.5':'TEAR','7.6':'TEAR','7.12':'TEAR','7.14':'TEAR',
 '1.2.3':'FEEL','1.3.6':'FEEL','1.3.8':'FEEL','2.2.4':'SND','5.5.1':'SND','5.5.2':'SND','5.5.3':'SND','5.5.4':'SND','5.5.5':'SND','5.5.6':'SND','5.5.7':'SND',
 '2.1.2':'B','2.6.4':'B','2.7.4':'B','2.7.6':'B',
 '2.4.2':'PUB','GD-04':'PUB','8.3.1':'PUB',
 '2.7.1':'TEST','2.7.2':'TEST','2.7.3':'TEST','2.8.2':'TEST','2.6.6':'TEST','2.12.2':'TEST','2.12.3':'TEST','2.11.1':'TEST','2.11.3':'TEST','2.10.4':'TEST','2.15.2':'TEST','3.5.5':'TEST','2.9.2':'TEST','2.4.3':'TEST',
 '2.8.1':'STORY','3.1.2':'STORY','3.5.2':'STORY','3.5.3':'STORY','3.5.4':'STORY',
 'RT-14':'SET','7.2':'PANEL','7.3':'PANEL',
}
un=[r for r in d['rows'] if r['status']=='UNMEASURED']
miss=[r['id'] for r in un if r['id'] not in plan]; assert not miss, miss
for r in un:
    how,when=P[plan[r['id']]]
    r['measure_how']=how; r['measure_when']=when; r['closed_by']=how+' ('+when+')'; r['plan_group']=plan[r['id']]
json.dump(d,open(OUT+'/coverage.json','w'),indent=1,ensure_ascii=False)
c=collections.Counter(plan[r['id']] for r in un); print(len(un),c)
json.dump({k:[r['id'] for r in un if plan[r['id']]==k] for k in P},open(OUT+'/scripts/plan_groups.json','w'),indent=1)
