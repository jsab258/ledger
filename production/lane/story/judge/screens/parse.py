import re,json,random,glob,sys
scenes=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.md')):
    t=open(f).read()
    for b in re.findall(r'=== SCENE\n(.*?)=== END',t,re.S):
        head,rw=b.split('--- REWRITE',1)
        d={}
        for line in head.strip().splitlines():
            if ':' in line:
                k,v=line.split(':',1); d[k.strip()]=v.strip()
        d['text']=rw.strip()
        d['n_words']=len(rw.split())
        scenes.append(d)
random.seed(2611)
ids=random.sample(range(10,99),len(scenes))
for s,i in zip(scenes,ids): s['id']=f'S{i}'
json.dump(scenes,open(sys.argv[2],'w'),indent=1)
from collections import Counter
print(len(scenes),Counter(s['label'] for s in scenes),Counter((s['game'],s['label']) for s in scenes))
print(sorted(s['n_words'] for s in scenes))
