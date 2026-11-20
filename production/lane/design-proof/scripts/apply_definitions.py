# Run 2: apply DEFINITIONS-2026-11-21.md to coverage.json (row by row, from the file's own fields).
import json,re,sys
OUT='/home/claude/ledger/production/lane/design-proof'
md=open(OUT+'/DEFINITIONS-2026-11-21.md').read()
d=json.load(open(OUT+'/coverage.json')); byid={r['id']:r for r in d['rows']}
blocks=re.split(r'\n### ',md)[1:]
n=0
for b in blocks:
    rid=b.split()[0]
    if rid not in byid: print('skip',rid); continue
    def f(k):
        m=re.search(r'^'+k+r'[^.]*?\.\s*(.*)$',b,re.M); return m.group(1).strip() if m else ''
    st=re.search(r'^Status: (\w+)(?: \((.*)\))?',b,re.M)
    r=byid[rid]
    r['defined_in']='DEFINITIONS-2026-11-21 §'+rid
    if f('Standard'): r['standard']=f('Standard')
    if f('Test'): r['test']=f('Test')
    if f('Source'): r['standard_source']=f('Source')
    r['status']=st.group(1); note=st.group(2) or ''
    if r['status']=='MEASURED':
        r['basis']='design decision, pass or fail (DEFINITIONS-2026-11-21; he may overturn)' if 'design decision' in note else 'public guideline, canon, his ruling or a guard (DEFINITIONS-2026-11-21)'
        r['closed_by']='defined 21 Nov (run 2)'
    elif r['status']=='PENDING':
        r['basis']='defined; its number waits on: '+note; r['closed_by']=note
    elif r['status']=='UNMEASURED':
        r['basis']='defined; '+note; r['closed_by']=note
    elif r['status']=='OUT':
        r['basis']=note; r['closed_by']=note; r['standard']='left out'
    elif r['status']=='OUTSIDE':
        r['basis']=note; r['closed_by']='after the prototype'
    r['run2']='defined'
    n+=1
json.dump(d,open(OUT+'/coverage.json','w'),indent=1,ensure_ascii=False)
import collections;print(n,collections.Counter(r['status'] for r in d['rows']))
