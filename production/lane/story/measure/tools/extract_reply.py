import json,sys,re
# usage: extract.py agentid outfile header
aid,out,header=sys.argv[1],sys.argv[2],sys.argv[3]; KEY=sys.argv[4] if len(sys.argv)>4 else 'MARKS'
p=f"/root/.claude/projects/-home-claude/81c0c43c-0613-52b0-9eda-ba4692a4d148/subagents/agent-{aid}.jsonl"
best=""
for line in open(p):
    try: d=json.loads(line)
    except: continue
    m=d.get('message') or {}
    if m.get('role')!='assistant': continue
    c=m.get('content')
    if isinstance(c,str): cands=[c]
    else:
        cands=[]
        for b in c or []:
            if b.get('type')=='text': cands.append(b['text'])
            if b.get('type')=='tool_use':
                for v in (b.get('input') or {}).values():
                    if isinstance(v,str): cands.append(v)
    for t in cands:
        if KEY in t: best=t
open(out,'w').write(header+"\n\n"+best.strip()+"\n")
print(out,len(best.split()))
