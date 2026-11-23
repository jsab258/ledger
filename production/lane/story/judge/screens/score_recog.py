import json,sys,re
s={x['id']:x for x in json.load(open('scenes_v3.json'))}
def norm(g):
  g=g.lower()
  for k,v in [('red dead','RDR2'),('kingdom come','KCD2'),('witcher','W3'),('sleeping dogs','SD'),('true crime','SD?'),('noire','LAN'),('legion','WDL'),('watch dogs','WD?'),('grand theft auto iv','GTAIV'),('gta iv','GTAIV'),('gta 4','GTAIV'),('grand theft auto v','GTAV'),('gta v','GTAV'),('gta 5','GTAV')]:
    if k in g: return v
  return g[:20]
def mnorm(m): return re.sub(r'[^a-z ]','',m.lower())
res={}
for f in sys.argv[1:]:
  for x in json.load(open(f)):
    t=norm(s[x['id']]['game']); g=norm(x['game'])
    game_ok = t==g or (t=='WDL' and g=='WD?')
    sm=mnorm(s[x['id']]['mission'].split('(')[0]).strip(); gm=mnorm(x.get('mission') or '')
    mis_ok = game_ok and len(sm)>3 and sm in gm
    rec = game_ok and (x['confidence']>=50 or mis_ok)
    r=res.setdefault(x['id'],[])
    r.append((f.split('_')[-1][:5],g,x['confidence'],game_ok,mis_ok,rec))
drop=[i for i,r in res.items() if any(z[5] for z in r)]
low=[i for i,r in res.items() if i not in drop and any(z[3] for z in r)]
for i in sorted(res): print(i,s[i]['label'][:3],norm(s[i]['game']),res[i])
print('recognised (drop):',len(drop),sorted(drop)); print('right game, low conf, kept:',len(low),sorted(low))
from collections import Counter
print('kept by label',Counter(s[i]['label'] for i in s if i not in drop))
json.dump({'drop':drop,'low':low},open('recog_result.json','w'))
