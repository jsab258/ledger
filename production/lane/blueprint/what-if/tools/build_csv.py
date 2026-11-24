import json, csv
from questions import Q
A=json.load(open('answers-merged.json'))
R={json.loads(l)['id']:json.loads(l) for l in open('../review-work/reviewer-verdicts.jsonl')}
extra=[("Q211","Can Frank rob the bank, the one place with CCTV?","reviewer R15 (missed by the sweep)","rob","bank","day","R15"),
("Q212","Is Frank's cash taken when he is arrested, and is the solicitor free or paid?","reviewer R16 (missed)","arrest","police","custody","R16"),
("Q213","What does the player see if he draws a weapon in a shop in the first hour, before hold-ups are allowed?","reviewer R17 (missed)","hold up","shopkeeper","early","R17"),
("Q214","What happens if Frank attacks a rival's man during Garbutt's truce?","reviewer R24 (missed)","strike","rival's men","truce","R24"),
("Q215","Does a crewman Frank sacks hold a grudge, and what can he do with what he knows?","reviewer R25 (missed)","dismiss","crew","later","R25"),
("Q216","Can Frank romance Alison or Philip while doing crimes, and what if they find out?","reviewer R30 (missed)","romance","love interest","talk","R30")]
P={}
def m(ids,txt):
    for i in ids.split(): P[i]=txt
m("Q001 Q010 Q011 Q012 Q013 Q015 Q022 Q051 Q052","LONG-HEAT.md LH-01 to LH-11 (the long heat; remand, committal, bribe, handing himself in)")
m("Q002 Q025 Q026 Q027 Q028 Q029 Q037","LONG-HEAT.md LH-12 (RT2-02 fixed: perception decides what a struck officer knows)")
m("Q003 Q004 Q063 Q069 Q206 Q126 Q127","LONG-HEAT.md LH-13 (same rules for every officer; the town reads a blow on a woman or over-sixty one step heavier; Ellis's case to DI Hebden)")
m("Q005","LONG-HEAT.md LH-14a (question Q-H1: committed thrust on a spent man; recommended)")
m("Q006 Q208 Q161","LONG-HEAT.md LH-14b (a drawn weapon in talk is a rung-6 threat; temper decides)")
m("Q007","LONG-HEAT.md LH-14c (kick only on a downed man; counts as fists)")
m("Q008 Q134 Q135","LONG-HEAT.md LH-14d (disposal; prints only with an earlier arrest; search reaches)")
m("Q009","LONG-HEAT.md LH-14e (the weapon clip list)")
m("Q105 Q106 Q107 Q108","PROPOSED-PARTS.md P07 and LONG-HEAT.md LH-04, LH-09")
m("Q192 Q047","LONG-HEAT.md LH-07 (remand road with daily visits) and PROPOSED-PARTS.md P04")
m("Q088 Q092 Q096","PROPOSED-PARTS.md P01")
m("Q089 Q120 Q123 Q124 Q178 Q195 Q193 Q194","PROPOSED-PARTS.md P02")
m("Q046 Q045 Q212","PROPOSED-PARTS.md P03")
m("Q093","PROPOSED-PARTS.md P04")
m("Q101 Q118","PROPOSED-PARTS.md P05")
m("Q076 Q077 Q080","PROPOSED-PARTS.md P06")
m("Q019 Q020 Q033","PROPOSED-PARTS.md P08")
m("Q143 Q144 Q198","PROPOSED-PARTS.md P09")
m("Q055","PROPOSED-PARTS.md P10")
m("Q190 Q191","PROPOSED-PARTS.md P11")
m("Q097 Q211 Q213","PROPOSED-PARTS.md P12")
m("Q214","PROPOSED-PARTS.md P13")
m("Q091 Q215","PROPOSED-PARTS.md P14")
m("Q184","PROPOSED-PARTS.md P15")
m("Q216","PROPOSED-PARTS.md P16 (story lane)")
m("Q109 Q078 Q018","Question Q-H3 for him (holding a person overnight); recommended answer in SUMMARY.md")
m("Q075 Q103 Q146","Question Q-H4 for him (fire as a verb); recommended answer in SUMMARY.md")
m("Q205 Q095","Question Q-H5 for him (leaving Meridian); recommended answer in SUMMARY.md")
W={'crash':5,'dead end':4,'absurd':4,'immersion':3,'minor':1,'none':0}
rows=[]
for q in Q:
    d=A[q[0]]; rows.append([q[0],q[1],q[2],q[3],q[4],q[5],d.get('answer',''),d.get('parts',''),d['verdict'],d.get('why',''),d.get('likely',''),d.get('harm','')])
for e in extra:
    d=R[e[6]]; rows.append([e[0],e[1],e[2],e[3],e[4],e[5],'',d.get('parts',''),d['verdict'],d.get('why',''),d.get('likely',''),d.get('harm','')])
for r in rows:
    v=r[8]; s=0 if v=='WELL' else float(r[10] or 1)*W.get(r[11],1)*(1.25 if v=='UNANSWERED' else 1)
    r.append(round(s,2))
order=sorted(rows,key=lambda r:-r[12])
rank={r[0]:(i+1 if r[12]>0 else '') for i,r in enumerate(order)}
with open('../QUESTIONS.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['id','question','where the question came from','verb','person','situation','the blueprint\'s answer','parts','verdict','why','likely in first hours (1-5)','harm if hit','score (likely x harm)','rank','proposed answer'])
    for r in rows: w.writerow(r+[rank[r[0]],P.get(r[0],'')])
from collections import Counter
print(Counter(r[8] for r in rows), len(rows), sum(1 for r in rows if r[0] in P and r[8]!='WELL'))
for r in order[:12]: print(rank[r[0]],r[0],r[12],r[1][:80],'|',P.get(r[0],'-')[:40])
