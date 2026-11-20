# Run 2, step (b): GTA VI yardstick and mechanics, the six walkthrough games' Steam themes, and the
# eight-game story patterns, mapped to rows with tests; gap rows GV-01..06 added; bars raised where GTA VI is higher.
import json,collections
OUT='/home/claude/ledger/production/lane/design-proof'
d=json.load(open(OUT+'/coverage.json')); R=d['rows']; byid={r['id']:r for r in R}
th=json.load(open(OUT+'/themes.json'))
GV='production/research/lane/gtavi/'
# ---- gap rows
new=[
 ('GV-01','The boot, seen','1.6.9','The cab\'s boot holds what is not on him: the envelope, a spare coat, a box. Opening it is an act with the seven slots; a constable who stops the cab with cause may look in it; a spare coat there is preparation (raised by Y1.3, Y1.6; idea 5).','Opening the boot is perceived like any act; a stop with cause searches it; what is in it survives save and load.','B: boot opened in sight of a watcher x 20 (memory written); a stop with cause finds the boot\'s contents.'),
 ('GV-02','Shedding what a witness holds, slot by slot','1.4.4, 1.6.10, 6.2.1','Each slot a witness can hold is shed its own way, and only against witnesses who have not yet told anyone: the coat (change it at the office), the car (the second car, the roof sign off, new plates or a respray), the face (a cap and scarf at night, a barber for a week), the companion (walking apart from Ron), the weapon (got rid of). Tom\'s guess of what each person holds of him shows in words on the Ledger\'s People page, never as icons (raised by Y1.4, Y2.2; idea 1).','A changed slot no longer matches for witnesses who had not told; gossip already carried is never undone; the Ledger shows Tom\'s guess per slot in words.','B: deed, change one slot, meet the same witness: only that slot fails to match; a witness who told first still names it.'),
 ('GV-03','The passenger who knows the way','1.2.7, 6.9','Whoever rides with Tom (Ron, a crewman, a fare who knows the town) says the way by landmark in a chase and when asked on a fare: "left after the chapel, he cannot follow you through the yard". No marker; the words carry the where (raised by Y3.3; idea 4).','In a car chase with a passenger, at least one landmark line per 20 s of chase; every line names a real landmark on the way.','B: car chases with each passenger; lines logged and checked against the map.'),
 ('GV-04','Places stay open','4.1.3','Every building used in a job stays enterable afterwards, as a place in someone\'s life, unless the story closes it and says so (raised by Y4.2).','Every interior used once can be entered again after its job, or its closing is said in the world.','B: after each job, a walk back into every interior it used.'),
 ('GV-05','Bugs at release','7.8, 8.2.1','The release build has no blocking fault: never stuck, no lost save, no crash in a whole evening (raised by Y8.2: critics found almost no bugs in GTA VI; players punish bugs and ports most of all in the walkthrough games: GTA IV port 25.9%, bugs 12.7%; Forza Horizon 4 port 22.0%).','Three nights running, the AI tester\'s whole-evening and whole-week walks in the packaged build find zero blocking faults and zero crashes.','The nightly tester walk, three nights in a row before the gate is called.'),
 ('GV-06','How a deed is told: restraint and cruelty','2.4.1, 2.12.4','The telling carries how a deed was done, not only that it was: a man put down with three blows who is left alone is told differently from one who was kicked on the ground. The worst telling, once carried, is never undone (raised by Y2.4; idea 9; derived from people\'s beliefs, never a stored meter).','Two seeded fights differing only in restraint produce different told versions and different greetings within a game day.','B: paired fights; the told lines and greetings compared.'),
]
for i,n,par,defn,std,test in new:
    if i in byid: continue
    r={'id':i,'name':n,'group':'GTA VI yardstick (run 2 gaps)','felt':True,'defined_in':'DEFINITIONS-2026-11-21 §GTA VI rows; '+GV+'IDEAS-FOR-LEDGER.md','definition':defn,'standard':std,'test':test,'standard_source':GV+'YARDSTICK.md and IDEAS-FOR-LEDGER.md','research':[],'status':'MEASURED','basis':'design decision, pass or fail (DEFINITIONS-2026-11-21; he may overturn)','closed_by':'defined 21 Nov (run 2)','source':'GTA VI study','parent':par,'run2':'added'}
    R.append(r); byid[i]=r
# ---- raised bars
raise_={
 '1.2.4':'Raised by Y1.1: front damage over the crash threshold pulls the car to one side until repaired, and a broken lamp darkens the road ahead at night; a dent is a mark witnesses remember.',
 '1.2.10':'Raised by Y1.2: the two ways in differ by the car: a brick through the quarter-light (about 3 s, loud) or a tool at the door and the ignition (about 10 s, quieter); a car with a steering lock cannot be taken; times to be checked in the footage pass.',
 '1.2.9':'Raised by GTA VI\'s respray rule: new plates or a respray clear the police\'s noted plate for that car (see GV-02).',
 '6.1.1':'Raised by Y1.8 (GTA VI fails it): with two usable things in reach the wrong action never fires; a tester walk presses the key 500 times in crowded spots and counts misfires (pass: zero).',
 '6.2.1':'Raised by Y2.2: Tom\'s guess of what each person holds of him, slot by slot, in words (GV-02).',
 '2.6.10':'Raised by Y2.3: the place stays warm for days, not minutes: next morning a constable knocks along that street and asks at windows, and for two nights the spot is walked more often; no circle on screen.',
 '2.5.3':'Raised by Y2.6: a person with the nerve for it (their temper) may step in, unarmed, at a hold-up or a beating in the street; Tom\'s line holds if that person is one it covers.',
 '2.7.6':'Raised by Y2.7: buyers differ in what they take (the second-hand shop radios and video recorders, the scrap yard car parts, a man at the back of the caff jewellery) and pay less for each further piece the same week; each is also a listener. No price table on screen.',
 '3.6.3':'Raised by Y2.5: no shared street line heard twice in one real hour of play anywhere (GD-02).',
 '7.8':'Raised by Y8.2: see GV-05 (no blocking fault three nights running).',
}
for k,v in raise_.items():
    r=byid[k]
    if 'Raised by' not in r['standard']: r['standard']=r['standard'].rstrip('. ')+'. '+v
    r['run2']='raised'
# ---- GTA VI map: yardstick
Y=[('Y1.1','1.2.4','raised'),('Y1.2','1.2.10','raised'),('Y1.3','1.6.9, GV-01','met; boot added'),('Y1.4','GV-02, 1.4.4','gap added'),('Y1.5','RT-10, 1.3.9','raised (RT-10: arm shot disarms, leg shot stops a runner)'),('Y1.6','1.6.6, GV-01','met'),('Y1.7','OUT-06','out (no stats, his rulings)'),('Y1.8','6.1.1','raised'),('Y1.9','AX-01 to AX-11','raised (aim assist steps, hold becomes tap, loud noise softening, colour-blind filters)'),
 ('Y2.1','2.2.1, 2.5.1, 2.4.4','met (no deed starts anything unseen)'),('Y2.2','6.2.1, GV-02','raised'),('Y2.3','2.6.10','raised'),('Y2.4','GV-06, 2.4.1','gap added'),('Y2.5','GD-02, 3.6.3','raised'),('Y2.6','2.5.3','raised'),('Y2.7','2.7.6','raised'),('Y2.8','2.1.6, 4.8','met (the town\'s calendar, weather profiles)'),
 ('Y3.1','3.5.7','met'),('Y3.2','3.1.4, 3.1.5','met'),('Y3.3','GV-03','gap added'),
 ('Y4.1','GD-01, GD-02','raised'),('Y4.2','GV-04','gap added'),
 ('Y5.1','5.x (OUTSIDE)','outside: Unreal look gate'),('Y5.2','5.x (OUTSIDE)','outside: Unreal look gate'),('Y5.3','2.4.5','not raised: the press works only through Alison (D56); a radio bulletin would be a second press channel and needs his ruling; recorded only'),
 ('Y6.1','6.x, OUT-09','met and exceeded (no HUD at all)'),('Y6.2','1.5.3, 1.5.4','met (no police dots)'),('Y6.3','6.10, 3.5.7','met in 1990 form (office phone, phone box, the radio)'),
 ('Y7.1','7.9','met (no game over)'),('Y7.2','7.12, GD-07','met'),('Y7.3','7.1','met (a retellable moment in the first 30 minutes)'),
 ('Y8.1','8.1.1 (OUTSIDE)','outside; not a bar (LEDGER\'s 60 fps stands)'),('Y8.2','GV-05, 7.8','gap added and raised'),('Y9.1','3.6.7','recorded: not a bar LEDGER can meet by its method; the AI notice and store disclosure say what it is')]
# mechanics lines (MECHANICS.md line number: rows, verdict)
M=[(10,'1.2.1','PC measuring: handling weight'),(11,'GD-01, 4.1.3','density over size'),(12,'1.2.4','raised'),(13,'OUT (description section 3: no fuel)','out'),(14,'1.2.3','met: in or out under 2 s; nitrous out (no tuning)'),(15,'GV-03','gap added'),(16,'1.2.9','raised'),(17,'OUT (no garage of cars, boats or buses)','out'),(18,'2.4.5, 4.9','radio stations: the firm\'s radio and pirate radio in the brand bible; licensed music OUTSIDE'),(19,'1.2.2, AX-03','camera per state met; crash cameras out (no cutscenes)'),(20,'OUT (1990: no apps)','out'),
 (23,'1.2.10','only parked cars (description section 23)'),(24,'1.2.10','raised'),(25,'OUT (1990: no scanner)','out'),(26,'2.7.6, 1.2.10','plate noted stands for a tracker'),(27,'OUT (no garage of cars)','out'),
 (30,'1.1.1','PC measuring'),(31,'OUT-06','out'),(32,'OUTSIDE (Unreal look)','outside'),(33,'1.1.8','vault places met; no climbing (OUT-08)'),(34,'6.1.1','raised'),
 (37,'OUT-01','out (one lead)'),(38,'1.3.4, 1.3.2','grab and counter met; no mashed prompts (AX-05)'),(39,'RT-11','no figures to compare; KCD2 and Sleeping Dogs stay the melee references'),
 (42,'1.6.9','met (two things under the coat)'),(43,'1.4.4','met (a weapon seen is a give-away)'),(44,'RT-10','raised (aimed limb shots) without slow motion'),(45,'RT-10','men run when outmatched'),(46,'OUT (no ammunition count, no armour shops)','out'),(47,'OUT (no gunfights with cover)','out'),(48,'RT-10','cover out keeps fights from being easy'),(49,'AX-05','raised'),
 (52,'S30 hold-ups, 1.6.1','robbery verbs met in 1990 form; wiping recordings: CCTV rare (canon)'),(53,'GV-02, GV-01','gap added'),(54,'1.6.7','met (blood until washed)'),(55,'1.6.1, 1.6.2','no lockpicking game (description); keys from people met'),(56,'S30','hold-ups rare and late'),
 (59,'1.4.7','street manners met'),(60,'2.5.3','a shot heard clears a street (dial)'),(63,'OUT (1990)','out'),(64,'OUT (1990)','out'),(65,'6.10','the office phone and phone box'),(68,'OUT-01','out'),(71,'OUT-06','out'),(72,'OUT (pastimes: boxing club only; hunting and golf out of scope and content)','out'),(73,'4.11.1','yard dogs met; petting not designed (small, not a gap)'),(74,'6.8','defined (photo mode)'),
 (78,'1.4.7, 2.5.3','met'),(79,'3.6.3','raised'),(80,'2.5.3','raised (unarmed)'),(81,'GD-02','raised'),(82,'2.2.1, 2.5.1','met'),(83,'GV-02, 6.2.1','raised'),(84,'2.6.5, 2.6.6','met (dial brings faster armed calls)'),(85,'2.6.4','an arrest keeps the coat; what is found is kept'),(86,'GV-06','gap added'),(87,'2.7.6','raised'),(88,'2.1.2','shops keep 1990 hours'),(89,'4.8','met'),(90,'4.11.1','one animal kind; not a gap at this scale'),(91,'2.1.6','ferry and shift timetables'),(92,'2.4.5','not raised (D56)'),
 (100,'GD-01','density over size'),(101,'GV-04','gap added'),(102,'OUTSIDE','outside'),(103,'OUT-05','out (one port)'),(107,'OUTSIDE','outside'),(108,'OUTSIDE','outside'),(109,'OUTSIDE','outside'),(110,'OUTSIDE','outside'),
 (114,'OUT-09','met (none at all)'),(115,'GV-02','raised, in words'),(116,'6.3','the paper map of known places'),(117,'3.5.7, 6.9','met'),(118,'6.1.1','raised'),(119,'AX-05','raised'),
 (123,'3.1.2','LEDGER 15 to 20 hours (ruling)'),(124,'7.9','met'),(125,'AX-07','LEDGER saves always (stricter)'),(126,'7.10','assists only'),(127,'GD-08, 3.5.6','met'),
 (131,'8.1.1 (OUTSIDE)','not a bar'),(132,'OUTSIDE','outside'),(133,'GV-05','gap added'),(134,'none','note only'),(138,'3.6.7','recorded'),(139,'3.6.3','ambient lines: raised')]
mech=open('/home/claude/ledger/'+GV+'MECHANICS.md').read().split('\n')
L=['# GTA VI mapped to the coverage map (run 2, 21 November 2026)\n','Every standard of YARDSTICK.md and every mechanic line of MECHANICS.md, mapped to the rows of coverage.json that answer it, with what was done: met (LEDGER\'s standard already at or above it), raised (the row\'s standard lifted and the row says "Raised by Y..."), gap added (a new GV row), out (his rulings or the description leave it out), outside (Unreal-only). Systems only; no GTA VI story content.\n','## The yardstick\n','| Key | Rows | Verdict |','|---|---|---|']
for k,rows,v in Y: L.append(f'| {k} | {rows} | {v} |')
L+=['','## The mechanics, line by line\n','| MECHANICS.md line | Mechanic (first words) | Rows | Verdict |','|---|---|---|---|']
for n,rows,v in M:
    t=mech[n-1].lstrip('- ')[:70].replace('|','/')
    L.append(f'| {n} | {t} | {rows} | {v} |')
L+=['','## Gap rows added (GV-01 to GV-06)\n']
for i,n,par,defn,std,test in new: L.append(f'### {i} {n}\nDefinition. {defn}\nStandard. {std}\nTest. {test}\nParent parts: {par}. Status: MEASURED (design decision, pass or fail).\n')
L+=['## Bars raised\n']
for k,v in raise_.items(): L.append(f'- {k} {byid[k]["name"]}: {v}')
open(OUT+'/GTAVI-MAP-2026-11-21.md','w').write('\n'.join(L)+'\n')
# ---- themes: walkthrough Steam and story patterns
W='production/research/lane/STEAM-WALKTHROUGH-GAMES-2026-11-20.md (on wip)'
SP='production/research/lane/STORY-PATTERNS-STEAM-2026-11-20.md'
P={'story':(['3.1.1','3.1.2','3.1.3','3.1.4','3.2.1','RT-02'],'story measure: at or above the best reference on the checked ruler; P4 retell test'),
 'world':(['2.1.1','2.1.3','7.12','GD-02'],'GD-02 density walk; S41 five-minute rule; the town runs unwatched (B soak)'),
 'looks':(['5.4.2','5.2.6'],'Unreal look gate against KCD2 frames (outside this proof); browser: grey range and night pools'),
 'port':(['8.3.1','AX-06','AX-10','6.6','GV-05'],'PC settings and focus soak; controls on keys and pad; GV-05 nightly walk'),
 'bugs':(['GV-05','7.8','8.2.1','AX-07'],'GV-05 three clean nights; SaveChaos'),
 'missions':(['3.5.6','GD-03','1.2.7','7.11'],'GD-03 permuted steps; no fare over 2 real minutes without a decision; never forced to wait'),
 'controls':(['6.6','AX-05','1.1.1'],'input probe 100 ms; first hour on pad alone with toggles'),
 'boring':(['7.12','7.14','RT-19','GD-02'],'S41 never five minutes with nothing new; no set piece twice in thirty minutes'),
 'driving':(['1.2.1','1.2.4','1.2.2'],'driving sheet M1 to M12 inside the measured bands'),
 'fists':(['1.3.1','1.3.2','1.3.12','RT-11'],'melee sheet C1 to C15; masher wins under 3 in 10'),
 'seen':(['1.4.1','2.2.3','GV-02','1.4.4'],'eyes values inside the measured bands; slot shedding test'),
 'chases':(['1.5.1','1.5.2','1.5.3'],'every chase ends within 90 s; lost by 7 s or 70 m'),
 'characters':(['3.2.1','3.2.2','3.2.5','3.2.3'],'story measure item; P4: 4 of 5 name Tom and one other'),
 'weak-story':(['3.1.2','RT-02','RT-04'],'story measure: no punished pattern failed'),
 'writing':(['3.6.3','3.6.1','3.6.2'],'claim check; street lines checked once; fresh reader on 50 lines'),
 'hits-hard':(['7.6','3.1.1'],'one retellable moment in the first 30 minutes, two an hour after'),
 'rails':(['GD-03','3.5.6','3.1.2'],'GD-03; beats on states, never days'),
 'rushed-ending':(['3.1.3','3.1.4','RT-01'],'every ending sign shown before it decides; Act III 2 to 3 hours'),
 'humour':(['GD-05'],'a comic scene each act, a light moment each evening'),
 'ending-lands':(['3.1.4','3.1.5'],'Tom\'s reading predicts the ending; story measure endings item'),
 'turn':(['RT-02','3.1.2'],'story measure: the turn item'),
 'short':(['3.1.2','7.5'],'15 to 20 hours, Act II 11 to 14'),
 'tone-clash':(['GD-05'],'no comic scene inside death or grief'),
 'side-better':(['3.3','RT-02'],'side stories whole; main beats each a scene with a choice'),
 'thin-villain':(['RT-06','2.10.1','RT-02'],'each rival a face, a motive, a threat in its own style'),
 'missions-tell':(['3.5.7','RT-02'],'every beat carried by a system')}
rows=[]
G={'Sleeping Dogs':(['story','world','looks'],['story','controls','missions']),'GTA IV':(['story','world','looks'],['port','bugs','missions']),'L.A. Noire':(['story','world','looks'],['port','story','boring']),'Hitman: WoA':(['story','world','looks'],['missions','port','story']),'Watch Dogs: Legion':(['story','world','looks'],['story','port','missions']),'Forza Horizon 4':(['driving','looks','world'],['port','bugs','controls'])}
fig={'Sleeping Dogs':{'p':['44.8','28.2','18.0'],'n':['10.2','8.6','7.0']},'GTA IV':{'p':['35.0','19.8','12.6'],'n':['25.9','12.7','10.7']},'L.A. Noire':{'p':['39.1','21.1','15.2'],'n':['13.6','9.8','7.1']},'Hitman: WoA':{'p':['13.6','12.8','9.5'],'n':['9.0','7.2','4.8']},'Watch Dogs: Legion':{'p':['25.1','15.4','11.0'],'n':['19.6','11.5','9.1']},'Forza Horizon 4':{'p':['23.2','23.1','12.5'],'n':['22.0','4.9','3.5']}}
k=0
for g,(pr,pu) in G.items():
    for side,keys,figs in (('praised',pr,fig[g]['p']),('punished',pu,fig[g]['n'])):
        for key,f in zip(keys,figs):
            k+=1; rows.append(('WT-%03d'%k,'Steam players',g,key,key,side,f'{f}% of kept reviews (frozen coder; ranks themes, does not measure them)'))
for g,key,side,f in [('Sleeping Dogs','fists','praised','about 43% (hand 33 praise, 5 complaint)'),('Sleeping Dogs','driving','punished','about 24% (hand 12 complaint, 6 praise)'),('GTA IV','driving','praised','about 17% (hand 13 praise, 4 complaint)'),('Hitman: WoA','seen','praised','about 13% (hand 24 praise, 5 complaint)'),('Watch Dogs: Legion','driving','punished','about 7% (hand 18 of 18 complaint; handling, weight, camera)'),('Forza Horizon 4','driving','praised','about 15% (hand 14, none complaint)'),('Sleeping Dogs','chases','praised','a few % (weak)'),('L.A. Noire','chases','praised','a few % (weak)')]:
    k+=1; rows.append(('WT-%03d'%k,'Steam players (mechanic)',g,key,key,side,f))
sp=[('characters','praised','8 of 8 games; 46% of coded story reviews'),('weak-story','punished','5 of 8; 20%'),('writing','praised','7 of 8; 18%'),('hits-hard','praised','6 of 8; 9%'),('rails','punished','5 of 8; 8%'),('rushed-ending','punished','5 of 8; 6%'),('humour','praised','5 of 8; 6%'),('ending-lands','praised','5 of 8; 5%'),('turn','praised','6 of 8; 5%'),('short','punished','Sleeping Dogs, Hitman (single mentions)'),('tone-clash','punished','L.A. Noire, Watch Dogs: Legion (single)'),('side-better','punished','L.A. Noire, Watch Dogs: Legion (single)'),('thin-villain','punished','GTA IV (single)'),('missions-tell','praised','Hitman (single)')]
for i,(key,side,f) in enumerate(sp,1): rows.append(('SP-%03d'%i,'Steam story patterns','eight games',key,key,side,f))
order=['OUT','OUTSIDE','UNDEFINED','UNMEASURED','PENDING','MEASURED']
weak=lambda ps: min((byid[p]['status'] for p in ps if p in byid), key=lambda s:['UNDEFINED','UNMEASURED','PENDING','MEASURED','OUT','OUTSIDE'].index(s))
have={t['id'] for t in th}
for tid,src,g,key,_,side,f in rows:
    if tid in have: continue
    ps,test=P[key]
    th.append({'id':tid,'source':src+(' ('+W+')' if tid.startswith('WT') else ' ('+SP+')'),'game':g,'theme_key':key,'theme':key,'valence':side,'figure':f,'parts':ps,'test':test,'status_of_parts':weak(ps),'excluded':''})
json.dump(th,open(OUT+'/themes.json','w'),indent=1,ensure_ascii=False)
json.dump(d,open(OUT+'/coverage.json','w'),indent=1,ensure_ascii=False)
print(len(rows),'themes;',collections.Counter(r['status'] for r in R))
