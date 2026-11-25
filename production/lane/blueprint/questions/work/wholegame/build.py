import csv,re
qs=[]
for f in ['q-A.md','q-B.md','q-C.md']:
    for l in open(f):
        l=l.strip()
        if not l: continue
        m=re.match(r'- \[(.+?)\] (.*)',l); qs.append((m.group(1),m.group(2)))
assert len(qs)==347,len(qs)
rows={}
for f in ['ans/A.txt','ans/B.txt','ans/C.txt']:
    for l in open(f):
        l=l.rstrip('\n')
        if not l: continue
        p=l.split('|')
        if len(p)!=11 and p[1] in 'WO': p=[p[0],p[1],p[2],p[3],'','','','','',p[-2],'']
        assert len(p)==11,(l[:40],len(p))
        rows[int(p[0])]=p[1:10]
assert sorted(rows)==list(range(1,348)),set(range(1,348))-set(rows)
W=[38,49,57,68,86,88,93,98,105,117,119,141,155,157,160,171,182,183,188,191,193,195,198,200,202,206,208,214,219,221,222,225,227,240,245,247,250,251,256,261,263,271,273,274,275,278,279,280,281,282,284,287,289,290,293,294,298,309,311,312,316,321,323,328,333,335,337,341,342,343,346]
FIX={
224:("G28","Name the quiet beats in the director's cards: an evening in the office after each heavy beat, with something to do there (the board, Sheila's count, a visitor).","content","medium: earned quiet","none"),
236:("G28","Measure driving repetition in the style bots: no route driven more than five times an evening without a fare wrinkle or a happening on it.","content","medium: driving that stays fresh","none"),
317:("G27","Pressure shows on the roads: more panda cars by Ellis's stage, fewer of Frank's cabs out at night in War, a rival's van parked on his rank.","content","medium: traffic as a gauge","none"),
238:("G28","Keep the Landing's wounded old man as the first serious harm on every path; a death of a known person stays the player's or the dial's, never forced.","content","low: confirm as designed","none"),
283:("G05","Ellis's wants (her case, her standing at the station) are held facts Frank can learn and use under the hooks rule, giving a police arc that only that player sees.","build","medium: an officer with wants","none"),
136:("G25","Write the clean firm's routes through weeks 5 to 7 (the search finds nothing, the attempts are warned off, the yard is a trade); it already reaches the Kingdom at rung 2 if the books hold.","build","high: a clean path through a crime story","none"),
164:("G31","A person or job that closes says so through a person a game day ahead or at the time; the Ledger keeps a closed line.","content","medium: nothing lost silently","none"),
100:("G02","Overheard plans follow the first pass's rule G02: talk Frank overhears comes from what the speakers hold and can change his next move; nothing new for the whole game.","build","high: eavesdropping that matters","none"),
146:("G20","As the first pass's rule G20: accounts and contracts read the firm's name and drop or grow on what the town holds of it.","build","medium: business that reads talk","none"),
147:("G28","Measure seven weeks of a firm-only bot for repeated fare wrinkles and rota chores; add a new kind of fare or account each week of Act II.","content","medium: a firm that stays fresh","none"),
159:("G31","The close's voices are chosen from people holding his deeds first hand, so a late clean-up is told by people who remember the early rackets; say this in the close rule.","content","medium: history in the close","none"),
167:("G28","Say it plainly: one run takes one route per job; side jobs stay open after the ending, and trying other routes is a second run.","content","low: honest scope","none"),
177:("G13","As the first pass's rule G13 (objects carry owners and facts); the whole-game answer is its count of small answers, to be listed in the can-you census.","build","high: wide answers","clips"),
189:("G30","List the calendar-fixed days in the design (the display Saturday, Remembrance Sunday, the gate chained on 1 December, rent each Friday); everything else moves on states and the per-save draw.","content","medium: readable fixed points","none"),
194:("G30","Run GD-04's two-bot test with opposite week-one readings and count named differences by week four.","content","medium: measured replay","none"),
196:("G30","Draw small week-one variation per save (who is in the caff, which fare people call, the weather) inside the staged beats.","content","medium: a fresh opening","none"),
207:("G22","A prevented attempt in week 5 still counts as that rival's go; he tries another man or another way, said by Garbutt.","content","medium: foresight rewarded","none"),
212:("G30","Measure: two panel players play the same week and list their stories; aim at most shared beats, most different details.","content","low: measurement","none"),
216:("G28","Time the first hour's beats in the first loop and hold MEM-10 (a deed said to his face within 30 real minutes).","content","low: measurement","none"),
233:("G28","Measure side-story and happening density per week against heavy beats; thickest where the spine is thinnest (weeks 2, 3 and 6).","content","low: measurement","none"),
237:("G28","Measure climaxes per evening in style bots; the director's spacing should give one every 40 to 60 minutes.","content","low: measurement","none"),
252:("G01","Tips and rumours under the source-of-talk rule; police and gangs weigh them against what they hold, and a trick repeated is traced, so it is a strategy with a cost, not an exploit.","build","high: three-way play","none"),
267:("G13","As the first pass's G13 and G18; the can-you census is the check that each sensible try has an answer.","build","high: wide answers","none"),
269:("G25","Every main beat carries a talk, a stealth and a force route; the yard and week 7's fight get their quiet routes first.","build","high: a non-violent crime story","none"),
320:("G30","Count street differences between two week-six bot runs (shops, posts, marks, greetings, crowd); aim at twenty.","content","low: measurement","none"),
330:("G28","Measure tension per style (ER-TENS-01) for a careful and a reckless bot; each must pass every week.","content","low: measurement","none"),
334:("G25","Week 7's one fight gets talk and stealth routes by the three-route rule; the mornings already test several kinds of play.","build","medium: a varied finale","none"),
340:("G25","Write the quiet routes to every beat; the pacifist's difficulty is people's dials and the town's memory, never a locked door.","build","high: fair non-violence","none"),
344:("G22","A failed job may come back once in a harder form or go to a rival, said by its giver; the town keeps the first failure.","content","medium: failure with a memory","none"),
345:("G26","Readings move within a game week with new people and never with those who hold a deed first hand; say both in the reputation rule.","build","medium: readable recovery","none"),
}
V={'W':'answered well','P':'partly','M':'missing','C':'contradictory','O':'answered well'}
P={'wg':'whole game: pacing and styles'}
code={'the ghost':'GH','the pacifist talker':'PT','the brute':'BR','the stealth player':'ST','the schemer':'SC','the honest businessman':'HB','the completionist':'CO','the second-playthrough player':'SP','the pacing critic':'PC','the systems critic':'SY','the story critic':'SR','the long-term reactivity critic':'LT','the challenge critic':'CH'}
cnt={};out=[]
for i,(lens,q) in enumerate(qs,1):
    v,parts,ans,prop,rule,cls,cy,anim,pas=rows[i]
    if i in W: v='W'
    if i in FIX: rule,prop,cls,cy,anim=FIX[i]
    if v in 'WO': prop=rule=cls=cy=anim=''
    if v in 'PMC' and not prop: raise SystemExit(f'no proposal {i}')
    c=code[lens]; cnt[c]=cnt.get(c,0)+1
    out.append([f'WG-{c}{cnt[c]:02d}',q,'whole-game lens: '+lens,'whole game',V[v],parts,ans,prop,rule,cls,cy,anim,pas])
SAT=[
 ['WG-SAT01','What does a run look like where Frank never builds a crew at all and does every job himself, and which story beats or endings does that close off for good?','saturation check (fresh reviewer)','whole game','partly','STORY-FRAME 5; 2.12.2; 3.1.4; RT2-09','Week 5\'s aim is to keep three men stood at their posts and rungs 3 and 4 need men at posts, so a crewless Frank stays at rung 2 and loses week 5\'s aim; no ending needs crew.','By the three-route rule the spine\'s crew aims get a solo route (posts held by paid outsiders or by an arrangement), and the Ledger says before week 5 that its aim needs men.','G25','build','high: a lone-wolf crime run','none','story'],
 ['WG-SAT02','Which rival gang strategies (fight both, play them off, ally with one, ignore them) produce genuinely different Decembers, and which converge on the same final situation dressed differently?','saturation check (fresh reviewer)','whole game','partly','GD-04; RT-04; STORY-FRAME 5, 8','Act II ends at a sit-down with one head and Danny is on the quay on every path; the Widow as ally hands the Landing to Danny; how far Decembers differ by rival strategy is not measured.','Run four rival-strategy bots; each December must differ in at least five named things (who holds the dock gate, who sat at Grace\'s, who calls him what, which posts stand, who is in the close).','G30','content','medium: strategy that shows','none','whole game: pacing and styles'],
 ['WG-SAT03','If Frank makes an enemy in week one and avoids him entirely, does that grudge grow, fade or get passed on to others by week six, and is there a way the player can feel it coming?','saturation check (fresh reviewer)','whole game','partly','2.14; 2.4.1; 2.3.1','The grudge dial sets how long a wrong is held and talk passes it on, but a grudge never acts or grows by itself.','A held grudge acts by the person\'s dials over time: he tells his ties, takes it to a rival or the police when a chance comes, and the sign shows first (he is seen with Danny\'s men).','G07','build','high: enemies who simmer','none','people'],
]
out+=SAT
for r in out:
    for x in r: assert '\n' not in x and '—' not in x, r
with open('../../QUESTIONS-WHOLEGAME.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow('id,question,source or lens,area,verdict,parts,answer,proposal,rule id,class,can-you value,animation,pass'.split(',')); w.writerows(out)
from collections import Counter
print(Counter(r[4] for r in out)); print(Counter(r[8] for r in out if r[8])); print(Counter(r[9] for r in out if r[9])); print(Counter(r[12] for r in out))
