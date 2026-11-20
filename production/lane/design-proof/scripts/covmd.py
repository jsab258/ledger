import json,collections
OUT='/home/claude/ledger/production/lane/design-proof'
d=json.load(open(OUT+'/coverage.json')); R=d['rows']
th=json.load(open(OUT+'/themes.json'))
c=collections.Counter(r['status'] for r in R)
def cut(s,n=110):
    s=(s or '').replace('|','/').replace('\n',' ')
    return s if len(s)<=n else s[:n-3]+'...'
L=[]
L.append('# Design coverage map (20 November 2026; run 2, 21 November)\n')
L.append('One row per part of LEDGER a player meets: the parts tree\'s leaves (group 9, the machinery, is not met by a player and is left out), plus rows added from the review studies, critics, the accessibility and PC standards, design-document categories and the first red team. The data is coverage.json; the review themes are themes.json; the source extractions are in sources/.\n')
L.append('Unreal-only work (looks, engine, performance on his PC) is outside this proof; those rows are marked OUTSIDE and not judged here.\n')
L.append('## Counts\n')
L.append('| Status | Rows | Meaning |\n|---|---|---|')
mean={'MEASURED':'defined, standard set from reference data, his ruling or canon, or a pass/fail guard','PENDING':'defined, its standard waits on a dated study','UNMEASURED':'defined, no reference figure behind its standard yet','UNDEFINED':'needed, not defined (or only named)','OUT':'left out by his ruling or canon','OUTSIDE':'Unreal-only work, outside this proof'}
for s in d['statuses']: L.append(f'| {s} | {c[s]} | {mean[s]} |')
L.append(f'| all | {len(R)} | |\n')
mb=collections.Counter(r['basis'] for r in R if r['status']=='MEASURED')
L.append('MEASURED rows by basis: '+'; '.join(f'{k}: {v}' for k,v in mb.items())+'. Honest note: only the "reference figure" rows rest on numbers taken from the reference games; the others are pass or fail by a ruling, canon or a guard, which a checker can score but which no reference game set.\n')
L.append('## The punished categories, and what prevents each\n')
L.append('The review studies name these as punished across games. Each has a part, a standard and a test; the status shows how firm the standard is.\n')
L.append('| Punished | Part | Standard | Status |\n|---|---|---|---|')
byid={r['id']:r for r in R}
for name,ids in [('Missions that waste time (long drives, walking, waiting)',['1.2.7','7.11','3.5.6','GD-01']),('The same loop over and over',['7.14','1.3.12','3.4.2']),('Boredom, nothing to do',['7.12','GD-02','RT-19']),('A thin story or flat characters',['3.1.2','3.3','RT-02']),('Scripted missions that fail for small deviations',['3.5.6','7.9','GD-03']),('Bugs, crashes, broken saves',['7.8','8.2.1','AX-07']),('Slow, clunky controls',['1.1.1','6.6','1.2.1']),('Clunky combat',['1.3.1','1.3.2','RT-11']),('Economy breaks late (too much money, nothing to buy)',['2.7.8','GD-07','RT-17'])]:
    for i in ids:
        r=byid[i]; L.append(f'| {name} | {i} {r["name"]} | {cut(r["standard"],90)} | {r["status"]} |'); name=''
L.append('')
L.append('## Review themes\n')
inc=[t for t in th if not t['excluded']]
tc=collections.Counter(t['status_of_parts'] for t in inc)
L.append(f'{len(inc)} themes (Steam players for KCD2, GTA V and RDR2; critics for the same three) each map to a part with a test (themes.json). The weakest status among each theme\'s parts: '+'; '.join(f'{k} {v}' for k,v in tc.most_common())+f'. {len(th)-len(inc)} more themes from the October KCD2 and Mafia study are kept but not counted (Mafia is not a reference game, his ruling of 20 Nov). Run 2 added the six walkthrough games\' Steam themes (WT rows, from STEAM-WALKTHROUGH-GAMES-2026-11-20 on wip) and the eight-game story patterns (SP rows); GTA VI\'s yardstick and mechanics are mapped line by line in GTAVI-MAP-2026-11-21.md.\n')
groups=[]
for r in R:
    g=r['group']
    if g not in groups: groups.append(g)
for g in groups:
    L.append(f'## {g}\n')
    L.append('| Id | Part | Status | Standard | Defined in | Reference or basis | Closed by |\n|---|---|---|---|---|---|---|')
    for r in R:
        if r['group']!=g: continue
        L.append(f"| {r['id']} | {cut(r['name'],60)} | {r['status']} | {cut(r['standard'])} | {cut(r['defined_in'],70)} | {cut(r['standard_source'],60)}; {cut(r['basis'],60)} | {cut(r['closed_by'],50)} |")
    L.append('')
open(OUT+'/COVERAGE.md','w').write('\n'.join(L))
print(len('\n'.join(L).split()))
