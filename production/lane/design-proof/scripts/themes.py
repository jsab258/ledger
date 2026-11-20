import json,collections
S='/tmp/claude-0/-home-claude/41875b20-e387-5bb1-bc1f-8279467ea7a5/scratchpad'
OUT='/home/claude/ledger/production/lane/design-proof'
cov={r['id']:r for r in json.load(open(OUT+'/coverage.json'))['rows']}
tree=json.load(open('/home/claude/ledger/production/lane/parts-tree/PARTS-TREE.json'))
kids=collections.defaultdict(list)
for p in tree['parts']:
    if p['parent']: kids[p['parent']].append(p['id'])
def leaves(i):
    if i in cov: return [i]
    out=[]
    for k in kids.get(i,[]): out+=leaves(k)
    return out
GAPMAP={'original-language-audio':'OUT-10','mods':'GD-06','free-roam-bigger-map':'OUT-05','alcohol-in-play':'OUT-04','gambling-dice':'OUT-04'}
CRMAP={'CR-020':'OUT-01','CR-023':'GD-05','CR-030':'OUT-02','CR-032':'OUT-03'}
rank={'UNDEFINED':0,'UNMEASURED':1,'PENDING':2,'MEASURED':3,'OUT':4,'OUTSIDE':4}
th=[]
for f,kind in (('themes-steam.json','Steam players'),('themes-critics.json','critics')):
    for t in json.load(open(S+'/out/'+f)):
        parts=[]
        for p in t['parts']: parts+=leaves(p.replace(' (group)',''))
        if not parts:
            m=GAPMAP.get(t['theme_key']) or CRMAP.get(t['id'])
            if m: parts=[m]
        sts=[cov[p]['status'] for p in parts if p in cov]
        worst=min(sts,key=lambda s:rank[s]) if sts else 'NO PART'
        if t['theme_key']=='studio-culture-war': worst='NOT A DESIGN THEME'
        excluded = t['game']=='Mafia'
        th.append(dict(id=t['id'],source=kind,game=t['game'],theme_key=t['theme_key'],theme=t['theme'],valence=t['valence'],figure=t.get('figure') or t.get('reviews',''),parts=parts,test=t['test'],status_of_parts=worst,excluded='Mafia is not a reference game (his ruling 20 Nov)' if excluded else ''))
json.dump(th,open(OUT+'/themes.json','w'),indent=1,ensure_ascii=False)
inc=[t for t in th if not t['excluded']]
print(len(th),len(inc),collections.Counter(t['status_of_parts'] for t in inc))
print([ (t['id'],t['theme_key']) for t in inc if t['status_of_parts'] in ('NO PART',)])
