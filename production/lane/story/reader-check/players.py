# Players' story ranking from STORY-PATTERNS-STEAM-2026-11-20.md (hand-read counts).
# net = (praise mentions - complaint mentions) / story-speaking reviews.
# Main: every coded sub-theme except the general-praise row (coded in 3 games only).
P,C='p','c'
g={
'KCD2':(43,30,[(10,P),(5,C),(5,P),(4,C),(3,P),(3,C),(2,C),(2,P),(2,C),(1,C),(1,P),(1,P)]),
'GTAV':(18,0,[(15,P),(4,P),(4,P),(4,P),(1,P),(1,C)]),
'RDR2':(26,0,[(19,P),(8,P),(8,P),(5,P),(3,C),(3,P),(2,C),(2,C),(2,C),(1,P),(1,P)]),
'SleepingDogs':(21,0,[(12,P),(6,C),(2,P),(2,C),(2,P),(2,P),(1,C),(1,P),(1,C),(1,P),(1,C),(1,C),(1,C)]),
'GTAIV':(25,0,[(18,P),(6,P),(5,C),(3,P),(1,C),(1,P),(1,P),(1,C),(1,C)]),
'LANoire':(20,0,[(5,C),(5,C),(4,P),(3,C),(3,C),(2,P),(2,P),(2,P),(1,C),(1,C),(1,P),(1,C),(1,C),(1,C)]),
'Hitman':(32,14,[(4,C),(3,C),(2,P),(2,C),(2,P),(2,P),(1,P),(1,P),(1,P)]),
'WDLegion':(40,14,[(16,C),(2,C),(2,P),(1,C),(1,P),(1,P),(1,P),(1,P),(1,C),(1,C)]),
}
rows=[]
for k,(n,gen,l) in g.items():
    p=sum(a for a,s in l if s==P); c=sum(a for a,s in l if s==C)
    rows.append((k,n,p,c,(p-c)/n,(p+gen-c)/n))
for r in sorted(rows,key=lambda r:-r[4]): print("%-13s n=%2d praise=%2d compl=%2d net=%+.2f  with-general=%+.2f"%r)
