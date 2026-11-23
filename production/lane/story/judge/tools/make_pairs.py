import json,random,sys,itertools
half,brief_file,tag,seed=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
s={x['id']:x for x in json.load(open('scenes_final.json'))}
rng=random.Random(seed)
H=[x for x in s.values() if x['half']==half]
adm=[x['id'] for x in H if x['label']=='admired']; frg=[x['id'] for x in H if x['label']=='forgettable']
clean=[(a,f) for a in adm for f in frg if not s[a]['recognised'] and not s[f]['recognised']]
rest=[(a,f) for a in adm for f in frg if (a,f) not in clean]
rng.shuffle(rest)
# pick 20 from rest covering recognised scenes
chosen=[];cnt={}
for p in sorted(rest,key=lambda p:rng.random()):
  pass
rest.sort(key=lambda p:(cnt.get(p[0],0)+cnt.get(p[1],0),rng.random()))
while len(chosen)<20:
  rest.sort(key=lambda p:(cnt.get(p[0],0)+cnt.get(p[1],0),rng.random()))
  p=rest.pop(0); chosen.append(p); cnt[p[0]]=cnt.get(p[0],0)+1; cnt[p[1]]=cnt.get(p[1],0)+1
pairs=clean+chosen
brief=open(brief_file).read().split('---',1)[1].strip()
meta=[]
jud=[]
for k,(a,f) in enumerate(pairs):
  pid=f'{tag}{k:02d}'
  first=rng.choice([a,f]); second=f if first==a else a
  jud.append((pid+'x',first,second)); jud.append((pid+'y',second,first))
  meta.append({'pair':pid,'admired':a,'forgettable':f,'clean':(a,f) in clean})
X=[j for j in jud if j[0].endswith('x')]; Y=[j for j in jud if j[0].endswith('y')]
rng.shuffle(X); rng.shuffle(Y)
groups=[X[:20],X[20:],Y[:20],Y[20:]]
for g,grp in enumerate(groups):
  txt=brief+'\n\n'
  for pid,one,two in grp:
    txt+=f'===== PAIR {pid}\n\n--- SCENE 1\n{s[one]["text"]}\n\n--- SCENE 2\n{s[two]["text"]}\n\n'
  open(f'judge_{tag}_{g}.md','w').write(txt)
json.dump({'pairs':meta,'judgements':[{'id':j[0],'first':j[1],'second':j[2]} for j in jud]},open(f'pairs_{tag}.json','w'),indent=1)
print(len(pairs),sum(m['clean'] for m in meta))
