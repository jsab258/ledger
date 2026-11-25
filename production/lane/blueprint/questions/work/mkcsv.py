import json,csv,re,collections
rows=json.load(open('rows2.json'))
def c(s):
    s=str(s).replace('—',', ').replace('–','-').replace('\n',' ').replace('\r',' ')
    return re.sub(r'\*+','',s).strip()
cols=['id','question','source or lens','area','verdict','parts','answer','proposal','rule id','class','can-you value','animation','pass']
ok=('partly','missing','contradictory')
with open('/home/claude/lane/production/lane/blueprint/questions/QUESTIONS.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols)
    for r in rows:
        fl=r['verdict'] in ok
        w.writerow([c(x) for x in [r['id'],r['question'],r['source'],r['area'],r['verdict'],r['parts'],r['answer'],r['proposal'] if fl else '',r['rule'] if fl else '',r['cls'] if fl else '',r['canyou'] if fl else '',r['anim'] if fl else '',r['pas'] if fl else '']])
print(len(rows),collections.Counter(r['verdict'] for r in rows))
