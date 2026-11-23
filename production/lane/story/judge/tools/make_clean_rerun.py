import json,random
s={x['id']:x for x in json.load(open('scenes_final.json'))}
rng=random.Random(77)
pairs=[p for t in 'ab' for p in json.load(open(f'pairs_{t}.json'))['pairs'] if p['clean']]
brief=open('/home/claude/lane/production/lane/story/judge/BRIEF-v1.md').read().split('---',1)[1].strip()
jud=[];meta=[]
for k,p in enumerate(pairs):
  pid=f'c{k:02d}'; a,f=p['admired'],p['forgettable']
  first=rng.choice([a,f]); second=f if first==a else a
  jud.append((pid+'x',first,second)); jud.append((pid+'y',second,first))
  meta.append({'pair':pid,'admired':a,'forgettable':f,'clean':True})
X=[j for j in jud if j[0].endswith('x')]; Y=[j for j in jud if j[0].endswith('y')]
rng.shuffle(X); rng.shuffle(Y)
for g,grp in enumerate([X[:20],X[20:],Y[:20],Y[20:]]):
  txt=brief+'\n\n'
  for pid,one,two in grp: txt+=f'===== PAIR {pid}\n\n--- SCENE 1\n{s[one]["text"]}\n\n--- SCENE 2\n{s[two]["text"]}\n\n'
  open(f'judge_c_{g}.md','w').write(txt)
json.dump({'pairs':meta,'judgements':[{'id':j[0],'first':j[1],'second':j[2]} for j in jud]},open('pairs_c.json','w'),indent=1)
print(len(meta))
