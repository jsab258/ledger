import re,collections
maps={}
for line in open('LABELS.txt'):
    m=re.match(r'reader (\d): (.*)',line)
    if m: maps['R'+m.group(1)]=dict(p.split('=') for p in m.group(2).split(', '))
S=collections.defaultdict(lambda: collections.defaultdict(list))
for line in open('scores.txt'):
    r,a,rest=line.split(None,2); a=a.rstrip(':')
    for p in rest.split():
        k,v=p.split('='); S[a][maps[r][k]].append(int(v))
games=['RDR2','GTAV','G4','KCD2','SD','HIT','WDL','LAN','PM3']
print('aspect '+' '.join(f'{g:>5}' for g in games)+'  best(shipped)  PM3gap')
for i in range(1,16):
    a=f'A{i}'; m={g:sum(S[a][g])/3 for g in games}
    sh=sorted([g for g in games if g!='PM3'],key=lambda g:-m[g])
    top=m[sh[0]]
    best=[g for g in sh if top-m[g]<=0.34]
    print(f'{a:6} '+' '.join(f'{m[g]:5.1f}' for g in games)+f'  {"/".join(best)}  {m["PM3"]-top:+.1f}  rank {sorted(games,key=lambda g:-m[g]).index("PM3")+1}  raw {S[a]["PM3"]} best raw {S[a][sh[0]]}')
