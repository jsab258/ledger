"""OUTPUT SHARE OF A DAY'S SPEND, by session or helper and model, from the session logs (advisor 98, 11 Nov).
List prices per million tokens; cache writes priced at the 1-hour rate. Measures only.
    python tools/output_share.py 2026-11-10
"""
import json,glob,os,sys,collections
root=os.path.expanduser(r"~/.claude/projects/C--Users-Jafar-ledger-local")
day=sys.argv[1]
# list prices per Mtok: input, output, cache write(1h ~2x), cache read
P={'opus':(5,25,10,0.5),'sonnet':(3,15,6,0.3),'haiku':(1,5,2,0.1),'fable':(15,75,30,1.5)}
tot=collections.Counter(); seen=set()
for f in glob.glob(root+"/**/*.jsonl",recursive=True):
    agent='agent-' in os.path.basename(f) or 'subagents' in f
    for line in open(f,encoding='utf-8',errors='ignore'):
        if day not in line[:400] and day not in line: continue
        try: d=json.loads(line)
        except: continue
        if not str(d.get('timestamp','')).startswith(day): continue
        m=d.get('message') or {}
        u=m.get('usage'); mid=m.get('id')
        if not u or mid in seen: continue
        seen.add(mid)
        model=m.get('model','')
        k=next((x for x in P if x in model),'opus'); p=P[k]
        who=('helper-' if agent else 'session-')+k
        cw=u.get('cache_creation_input_tokens',0); cr=u.get('cache_read_input_tokens',0)
        tot[who+'|out$']+=u.get('output_tokens',0)*p[1]/1e6
        tot[who+'|in$']+=(u.get('input_tokens',0)*p[0]+cw*p[2]+cr*p[3])/1e6
        tot[who+'|outtok']+=u.get('output_tokens',0)
whos=sorted({k.split('|')[0] for k in tot})
allout=sum(v for k,v in tot.items() if k.endswith('out$')); allin=sum(v for k,v in tot.items() if k.endswith('in$'))
for w in whos:
    o=tot[w+'|out$']; i=tot[w+'|in$']
    print(f"{w}: output US${o:.2f} of US${o+i:.2f} ({100*o/max(o+i,1e-9):.0f}%), {tot[w+'|outtok']} output tokens")
print(f"all: output US${allout:.2f} of US${allout+allin:.2f} ({100*allout/(allout+allin):.0f}%)")
