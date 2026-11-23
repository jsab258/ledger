import json,sys,glob,re
tag=sys.argv[1]
s={x['id']:x for x in json.load(open('scenes_final.json'))}
P=json.load(open(f'pairs_{tag}.json'))
J={j['id']:j for j in P['judgements']}
res={'tag':tag,'models':{}}
verd={}
for model in ['opus','sonnet']:
  picks={}
  for f in glob.glob(f'out_{tag}_*_{model}.jsonl'):
    for line in open(f):
      line=line.strip()
      if not line: continue
      try: d=json.loads(line)
      except: continue
      j=J.get(d['pair']);
      if not j: continue
      picks[d['pair']]=j['first'] if str(d['choice']).strip()=='1' else j['second']
  n=len(picks); first=sum(picks[k]==J[k]['first'] for k in picks)
  lw=[k for k in picks if abs(s[J[k]['first']]['n_words']-s[J[k]['second']]['n_words'])>=5]
  longer=sum(s[picks[k]]['n_words']==max(s[J[k]['first']]['n_words'],s[J[k]['second']]['n_words']) for k in lw)
  out={}
  for subset in ['clean','recog','all']:
    ps=[p for p in P['pairs'] if subset=='all' or (p['clean'] if subset=='clean' else not p['clean'])]
    v={}
    for p in ps:
      a=picks.get(p['pair']+'x'); b=picks.get(p['pair']+'y')
      if a is None or b is None: v[p['pair']]='missing'; continue
      v[p['pair']]= 'A' if a==b==p['admired'] else 'F' if a==b==p['forgettable'] else 'T'
    nA=sum(x=='A' for x in v.values()); nF=sum(x=='F' for x in v.values()); nT=sum(x=='T' for x in v.values())
    dec=nA+nF
    single=[picks[p['pair']+o]==p['admired'] for p in ps for o in 'xy' if p['pair']+o in picks]
    out[subset]={'pairs':len(ps),'A':nA,'F':nF,'T':nT,'decided_share':round(dec/len(ps),3),'acc_decided':round(nA/dec,3) if dec else None,'strict':round(nA/len(ps),3),'single_acc':round(sum(single)/len(single),3)}
    if subset=='all': verd[model]=v
  out['n_judgements']=n; out['position_first']=round(first/n,3); out['length_longer']=round(longer/len(lw),3) if lw else None; out['length_pairs']=len(lw)
  res['models'][model]=out
# agreement
for subset in ['clean','all']:
  ps=[p['pair'] for p in P['pairs'] if subset=='all' or p['clean']]
  a=[verd['opus'][k] for k in ps]; b=[verd['sonnet'][k] for k in ps]
  agree=sum(x==y for x,y in zip(a,b))/len(ps)
  cats='AFT'; n=len(ps)
  pe=sum((a.count(c)/n)*(b.count(c)/n) for c in cats)
  kappa=(agree-pe)/(1-pe) if pe<1 else None
  res[f'agreement_{subset}']=round(agree,3); res[f'kappa_{subset}']=round(kappa,3) if kappa is not None else None
res['verdicts']=verd
print(json.dumps({k:v for k,v in res.items() if k!='verdicts'},indent=1))
json.dump(res,open(f'result_{tag}.json','w'),indent=1)
