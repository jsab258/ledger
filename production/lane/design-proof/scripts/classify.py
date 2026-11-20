import json,re,collections,sys
d=json.load(open('/home/claude/ledger/production/lane/parts-tree/PARTS-TREE.json'))
P={p['id']:p for p in d['parts']}
L=[p for p in d['parts'] if p['leaf']]
OUTSIDE_PREFIX=('5.1','5.2','5.3','5.4','5.6.1','5.6.2','5.7','5.8.2','5.9','5.10','8.1','8.5','8.7','4.4','4.5.2','4.6','4.1.5','3.2.6','10.1','10.3','10.4','10.5','10.8','10.10','10.2')
def outside(p):
    if p['track']!='unreal': return False
    return any(p['id']==x or p['id'].startswith(x+'.') for x in OUTSIDE_PREFIX)
PC_RN={'RN-01','RN-05','RN-07','RN-08','RN-14','RN-03'}
weak=re.compile(r'to be measured|not yet|no standard|none yet|^none|TBD|owed|unknown|research item',re.I)
ref=re.compile(r'REFERENCE-MECH|PLAYERS|FEEL|DRIVING|ACTIVITY|measured|reference game|KCD2|GTA|RDR2|footage|M\d\.\d+',re.I)
rul=re.compile(r'ruling|RULINGS|canon|\bD\d+\b|\d+ (Sep|Oct|Nov)',re.I)
rows=[]
for p in L:
    g=p['id'].split('.')[0]
    if g=='9': continue
    r={'id':p['id'],'name':p['name'],'group':P[g]['name'],'felt':p['felt'],'defined_in':p['designed_in'],
       'standard':p['standard'],'test':p['test'],'standard_source':p['standard_source'],'research':p['research_items']}
    s=p['standard']+' '+p['standard_source']
    if outside(p): st='OUTSIDE'; basis='Unreal-only work (looks, engine, performance): outside this proof'
    elif p['research_items']:
        if set(p['research_items'])&PC_RN: st='PENDING'; basis='PC measuring 23 to 28 Nov ('+', '.join(p['research_items'])+')'
        else: st='UNMEASURED'; basis='research item '+', '.join(p['research_items'])+' has no dated study'
    elif weak.search(p['standard']) or not p['designed_in'] or re.search(r'not designed|undesigned',p['designed_in'],re.I):
        st='UNMEASURED'; basis='standard or design marked not yet set'
    elif ref.search(s): st='MEASURED'; basis='reference'
    elif rul.search(s): st='MEASURED'; basis='his ruling or canon (pass/fail)'
    else:
        st='RULE' ; basis='design rule only'
    r['status']=st; r['basis']=basis; rows.append(r)
c=collections.Counter(r['status'] for r in rows); print(c)
print(collections.Counter((r['status'],r['felt']) for r in rows))
json.dump(rows,open(sys.argv[1],'w'),indent=1,ensure_ascii=False)
