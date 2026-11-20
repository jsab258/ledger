import json
def w(name,cases): json.dump({"piece":name,"cases":cases},open(f"test/cases/{name}.json","w"),indent=1)
def C(id,rule,fn,inp,out=None,outHas=None):
    d={"id":id,"rule":rule,"fn":fn,"in":inp}
    if outHas is not None: d["outHas"]=outHas
    else: d["out"]=out
    return d
base=lambda **k: dict(dict(metres=10,light=0.7,lineOfSight=True,facing=True,knowsHim=False,backTurned=False,markOnHim=True,stillInDoorway=False),**k)
c=[C("still-doorway-night","ER-HIDE-01","lightForTom",[{"light":0.7,"doorway":True,"night":True},{"stillSeconds":2,"torchOn":False}],0.12),
 C("moving-doorway-night","ER-HIDE-01","lightForTom",[{"light":0.7,"doorway":True,"night":True},{"stillSeconds":0,"torchOn":False}],0.7),
 C("torch-lights-him","A33","lightForTom",[{"light":0.1,"doorway":True,"night":True},{"stillSeconds":5,"torchOn":True}],0.7),
 C("torch-off-dark","A33","lightForTom",[{"light":0.1,"doorway":False,"night":True},{"stillSeconds":5,"torchOn":False}],0.1)]
for m,still,moving in [(4,1,3),(8,0,2),(18,0,1),(35,0,0)]:
    c.append(C(f"still-in-doorway-{m}m","ER-HIDE-01","rungCaught",[base(metres=m,light=0.12,stillInDoorway=True)],still))
    c.append(C(f"walking-past-doorway-{m}m","ER-HIDE-01","rungCaught",[base(metres=m,light=0.7)],moving))
c+=[C("daylight-shape-35m","ER-EYES-02","rungCaught",[base(metres=35,light=1,markOnHim=False)],1),
 C("daylight-mark-18m","ER-EYES-02","rungCaught",[base(metres=18,light=1)],2),
 C("daylight-face-8m","ER-EYES-02","rungCaught",[base(metres=8,light=1)],3),
 C("known-at-25m","ER-EYES-02","rungCaught",[base(metres=25,light=1,knowsHim=True)],4),
 C("stranger-never-recognises","moat","rungCaught",[base(metres=2,light=1)],3),
 C("back-turned-no-face","A1","rungCaught",[base(metres=4,light=1,backTurned=True,knowsHim=True)],2),
 C("back-turned-no-coat-a-shape","A1","rungCaught",[base(metres=4,light=1,backTurned=True,markOnHim=False)],1),
 C("behind-a-van","A1","rungCaught",[base(metres=4,light=1,lineOfSight=False)],0),
 C("not-facing","ER-EYES-02","rungCaught",[base(metres=4,light=1,facing=False)],0),
 C("glance-alone","A1","glanceSeconds",[1],0.35),
 C("glance-among-three","A1","glanceSeconds",[3],0.7),
 C("slow-walk-halves-footstep","A1","footstepReach",[3.6,True],1.8),
 C("walk-footstep","A1","footstepReach",[3.6,False],3.6)]
for m,r in ((8,2),(18,1),(35,0)):
    c.append(C(f"seated-never-more-than-walking-{m}m","ER-STOP-01","rungCaughtStopped",[base(metres=m,light=0.7),"sit"],r))
c+=[C("standing-about-at-night-draws-a-look","A10","drawsSecondLook",[True,None,25,20],True),
 C("smoking-at-night-draws-none","ER-STOP-01","drawsSecondLook",[True,"smoke",25,20],False),
 C("standing-about-by-day-draws-none","A10","drawsSecondLook",[False,None,25,20],False)]
w("hide_rules",c)
c=[C("collar-within-1m","A3","chaseStep",[{"t":3,"gap":1.2,"unseen":0},{"dt":0.5,"runnerSpeed":4.94,"pursuerSpeed":5.6,"seen":True,"behind":True}],outHas={"end":"caught"}),
 C("lost-unseen-7s","ER-POL-04","chaseStep",[{"t":20,"gap":20,"unseen":6.9},{"dt":0.2,"runnerSpeed":5,"pursuerSpeed":5,"seen":False}],outHas={"end":"lost"}),
 C("lost-70m","ER-POL-04","chaseStep",[{"t":20,"gap":69.9,"unseen":0},{"dt":0.5,"runnerSpeed":5.2,"pursuerSpeed":4,"seen":True}],outHas={"end":"lost"}),
 C("still-running","A3","chaseStep",[{"t":5,"gap":10,"unseen":0},{"dt":0.1,"runnerSpeed":5,"pursuerSpeed":5,"seen":True}],outHas={"end":None}),
 C("always-ends-by-90s","ER-PURSUE-01","chaseStep",[{"t":89.95,"gap":10,"unseen":0},{"dt":0.1,"runnerSpeed":5,"pursuerSpeed":5,"seen":True}],outHas={"end":"lost"})]
c+=[C("fifty-direct-chases-all-caught-within-90s","ER-PURSUE-02","chases",[{"n":50,"seed":1990,"startGap":8,"line":"direct"}],{"caught":50,"lost":0,"longestSeconds":19.6}),
 C("fifty-lagging-chases-all-lost-within-90s","ER-PURSUE-01","chases",[{"n":50,"seed":1990,"startGap":8,"line":"slow"}],{"caught":0,"lost":50,"longestSeconds":46.4})]
w("foot_chase",c)
c=[C("public-free","ER-GROUND-01","standing",[{"label":"public"},3],"free"),
 C("hours-open","ER-GROUND-01","standing",[{"label":"hours","openFromHour":8,"openUntilHour":18},10],"free"),
 C("hours-shut","ER-GROUND-01","standing",[{"label":"hours","openFromHour":8,"openUntilHour":18},22],"private"),
 C("hours-over-midnight","ER-GROUND-01","standing",[{"label":"hours","openFromHour":7,"openUntilHour":2},1],"free"),
 C("private","ER-GROUND-01","standing",[{"label":"private"},12],"private"),
 C("forbidden","ER-GROUND-01","standing",[{"label":"forbidden"},12],"forbidden"),
 C("warn-first","ER-GROUND-01","trespassStep",[None,{"ground":"private","watched":True,"dt":0.1}],outHas={"say":"warn","s":{"stage":1}}),
 C("unwatched-no-warning","ER-GROUND-01","trespassStep",[None,{"ground":"private","watched":False,"dt":0.1}],{"s":None,"say":None}),
 C("warn-again","ER-GROUND-01","trespassStep",[{"stage":1,"since":7.95},{"ground":"private","watched":True,"dt":0.1}],outHas={"say":"warnAgain","s":{"stage":2}}),
 C("no-act-before-warned-twice","ER-GROUND-01","trespassStep",[{"stage":1,"since":3},{"ground":"private","watched":True,"dt":0.1}],outHas={"say":None,"s":{"stage":1}}),
 C("acts-within-half-a-minute","ER-GROUND-01","trespassStep",[{"stage":2,"since":19.95},{"ground":"private","watched":True,"dt":0.1}],outHas={"say":"act","s":{"stage":3}}),
 C("forbidden-skips-first-warning","ER-GROUND-01","trespassStep",[None,{"ground":"forbidden","watched":True,"dt":0.1}],outHas={"say":"warnAgain","s":{"stage":2}}),
 C("leaving-resets","ER-GROUND-01","trespassStep",[{"stage":2,"since":12},{"ground":"free","watched":True,"dt":0.1}],{"s":None,"say":None})]
w("foot_ground",c)

# ---- the fight's pieces
c=[C("one-man-by-his-id","A29","pickTypes",[[{"id":"lee","build":0.5}],""],["brawler"]),
 C("same-man-after-another-mix","A29","pickTypes",[[{"id":"lee","build":0.5}],"boxer"],["brawler"]),
 C("no-two-fights-running-the-same-mix","ER-TYPES-01","pickTypes",[[{"id":"lee","build":0.5}],"brawler"],["boxer"]),
 C("a-big-man-by-his-build","A29","pickTypes",[[{"id":"dennis","build":0.5},{"id":"yardlad","build":0.9}],""],["boxer","big"]),
 C("two-men-mix-changes","ER-TYPES-01","pickTypes",[[{"id":"dennis","build":0.5},{"id":"yardlad","build":0.9}],"big+boxer"],["brawler","big"]),
 C("two-men-mix-kept-when-different","ER-TYPES-01","pickTypes",[[{"id":"dennis","build":0.5},{"id":"yardlad","build":0.9}],"big+brawler"],["boxer","big"]),
 C("an-authored-knife-stays","A29","pickTypes",[[{"id":"k","authored":"knife"}],"knife"],["knife"]),
 C("mix-is-order-free","ER-TYPES-01","mixOf",[["big","boxer"]],"big+boxer")]
w("fight_types",c)
c=[C("slip-takes-nothing-and-opens-the-counter","ER-DEFEND-01","blowLands",[{"heavy":True,"weapon":False,"hurts":0.24},{"doing":"slip"}],{"hurt":0,"staggered":False,"counterOpens":True}),
 C("guarded-jab-does-little-and-opens-the-counter","ER-DEFEND-01","blowLands",[{"heavy":False,"weapon":False,"hurts":0.12},{"doing":"guard","facing":True}],{"hurt":0.03,"staggered":False,"counterOpens":True}),
 C("guarded-heavy-staggers-a-little","A29","blowLands",[{"heavy":True,"weapon":False,"hurts":0.24},{"doing":"guard","facing":True}],{"hurt":0.06,"staggered":True,"counterOpens":False}),
 C("a-swung-weapon-breaks-the-guard","A29","blowLands",[{"heavy":False,"weapon":True,"hurts":0.2},{"doing":"guard","facing":True}],outHas={"staggered":True,"counterOpens":False}),
 C("guard-the-wrong-way-is-no-guard","A29","blowLands",[{"heavy":False,"weapon":False,"hurts":0.12},{"doing":"guard","facing":False}],{"hurt":0.12,"staggered":True,"counterOpens":False}),
 C("a-miss-leaves-him-open","DESIGN 7","blowLands",[{"heavy":False,"weapon":False,"hurts":0.12},{"doing":"open"}],outHas={"staggered":True,"counterOpens":False}),
 C("unanswered-blow-lands-whole","A29","blowLands",[{"heavy":True,"weapon":False,"hurts":0.24},{"doing":"idle"}],{"hurt":0.24,"staggered":True,"counterOpens":False}),
 C("jab-inside-the-window-is-a-counter","ER-DEFEND-01","jabIs",[0.3],"counter"),
 C("jab-after-the-window-is-a-jab","ER-DEFEND-01","jabIs",[0.8],"jab"),
 C("no-counter-without-a-slip-or-block","ER-DEFEND-01","jabIs",[None],"jab"),
 C("fresh-he-swings-at-full-speed","A29","windUpTimes",[1],1),
 C("half-spent-he-is-slower","A29","windUpTimes",[0.25],1.25),
 C("empty-he-is-slowest","A29","windUpTimes",[0],1.5),
 C("a-fighter-who-reads-wins-most-fair-fights","ER-DEFEND-01","duels",[{"n":200,"seed":7,"policy":"reader"}],{"won":200,"of":200}),
 C("a-masher-wins-under-three-in-ten","ER-FIGHT-07","duels",[{"n":200,"seed":7,"policy":"masher"}],{"won":48,"of":200})]
w("fight_defend",c)
