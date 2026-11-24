# Candidates A: hidden details from BLUEPRINT 01 (hands), 06 (interface), 07 (shape)

Read in full on 24 Nov 2026. Status is "as written": designed = rules and exact numbers or data given; partly = words only, or numbers or data missing, or marked pending/unmeasured/gap; missing = wish named, no design. Where a part says "pending" only because a number waits on a measured reference but the number is given, I say designed and note it.

## A. On foot, being seen, hiding

### 1
- Detail: At three in the morning Frank's footsteps carry about 3.6 m; at noon they carry nothing, and walking slowly halves it.
- Parts: 1.4.3, 1.1.1; tune.json
- Status as written: designed. "a footstep at three in the morning carries about 3.6 m and at noon nothing; walking slowly halves the reach" (1.4.3 "decided").
- First ten hours: yes
- Build or content: n/a (designed)

### 2
- Detail: Stand still in a dark doorway and Frank is only a shape, and only beyond 8 m; walk through the same doorway and he is seen at the street's light.
- Parts: 1.1.5, 1.4.2, 6.1.4; tune.json
- Status as written: designed in numbers (doorway 0.12, unlit street 0.25, 8 m), but the part is "pending": "how crouch changes what is caught is not yet set".
- First ten hours: yes
- Build or content: build for the crouch rule (a new input state in the catch rule); the rest is built.

### 3
- Detail: Frank has the corners of the screen darken when he is in the dark, and that is the only "stealth meter" in the game.
- Parts: 6.1.4, 1.4.2; tune.json
- Status as written: designed. "daylight 1, lamp 0.7, unlit street 0.25, doorway 0.12; the cue is darkness at the frame's corners, no meter" (6.1.4 "decided").
- First ten hours: yes
- Build or content: n/a

### 4
- Detail: Turn your back on a watcher and he can't catch your face, but he still catches the coat.
- Parts: 1.1.5
- Status as written: partly. Rule stated in words ("his face cannot be caught, though the coat can") but part is "pending"; felt rules "to be measured".
- First ten hours: yes
- Build or content: content/tuning only (the face and coat slots already exist).

### 5
- Detail: A figure at a lit window is a watcher; a dark window never is, except Ada in her dark front room, and you learn that once.
- Parts: 1.4.1; DESIGN ER-NIGHT-02
- Status as written: designed. "A window is a watcher only when a figure shows at it (Ada in her dark front room is the one exception, learned once)". Part itself "pending" for the 8-in-10 reading test.
- First ten hours: likely
- Build or content: n/a

### 6
- Detail: Every watcher turns his head before he knows Frank, giving at least 0.8 s of warning, and a street that has noticed him goes quiet.
- Parts: 1.4.1, 1.4.3
- Status as written: designed. "The head turns at the start of the 1.2 s a watcher needs to know him, so there is at least 0.8 s of warning"; "A street that has noticed him goes quiet" (no number for the quiet).
- First ten hours: yes
- Build or content: content for the quiet (an ambience rule).

### 7
- Detail: Sit on a bench and smoke a cigarette and Frank is never caught more than when walking by; stand about at night with no reason and a neighbour tells him to move on.
- Parts: 1.1.7 (key B)
- Status as written: partly. Sitting rule is given; the neighbour's warning is "Partly... Feature only; no timing". Part "unmeasured".
- First ten hours: yes
- Build or content: content plus a small rule (warning, then complaint, then report timings).

### 8
- Detail: Wear the same coat two nights running and witnesses who saw the first night know him; buy a second coat and the ones who haven't told anyone yet lose him.
- Parts: 1.4.4, 1.6.10
- Status as written: designed. "A second coat bought after a deed breaks the mark rung for witnesses who saw the first and have not yet told anyone... what gossip has carried is never undone"; prices £15, £45, £90, barber £4.
- First ten hours: likely
- Build or content: n/a

### 9
- Detail: Pay Shaun Hewson for a respray and the roof sign comes off, so witnesses who saw the old cab can no longer name it as Mickey's.
- Parts: 1.2.9
- Status as written: designed. "takes the roof sign off and gives a new colour, after which earlier sightings no longer name that car"; new plates also clear a noted plate "only for witnesses who have not yet told anyone". Status "decided".
- First ten hours: likely
- Build or content: n/a

### 10
- Detail: Blood stays on Frank's coat until he washes it with water in private, or takes it to the launderette, which cleans it and remembers him.
- Parts: 1.6.7, 1.4.4, 1.3.11
- Status as written: designed. "blood comes off with water and privacy, or at the launderette, which washes the coat and plants a witness". Status "decided".
- First ten hours: likely
- Build or content: n/a

### 11
- Detail: Frank's bruises last three game days and a limp one, and people see the marks and mention them first.
- Parts: 1.3.11; MEM-04
- Status as written: designed. "bruises and a cut lip for three game days and a limp for one. Others see them... and say so". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 12
- Detail: A retired doctor in a terrace by the quay stitches Frank's knife wound for £20, no questions, and remembers who he was.
- Parts: 1.3.11
- Status as written: partly. Price and "remembers" given; the doctor's place, hours and name are not ("A retired doctor in a terrace by the quay").
- First ten hours: likely
- Build or content: content (a person, a door, a line) on an existing witness rule.

### 13
- Detail: On a cold night Frank's breath shows, and a soaked Frank in rain is remarked on.
- Parts: 1.3.11 (catalogue "The body shows the day"), 2.1.4
- Status as written: partly. "short are wet coat and hair in rain and breath on a cold night... Feature only; no timing".
- First ten hours: yes
- Build or content: build (a weather-to-appearance link and an NPC remark rule); art on top.

### 14
- Detail: Frank can break an arm in a fight and carry it in plaster for weeks, and it changes how he drives and fights.
- Parts: 1.3.7, 1.3.11; conflict C-338
- Status as written: missing. "a lasting arm injury and a one-armed Frank are missing"; "the need is a gap for the design proof".
- First ten hours: no (story need, later)
- Build or content: build (a lasting injury state that changes driving and fight rules).

## B. Fights

### 15
- Detail: There is no health bar: you can read how a fight is going from a man's posture, breath, dropped guard and limp.
- Parts: 1.3.7, RT-11, 6.1
- Status as written: designed. "There is no health bar: posture, breath, a dropped guard, blood and a limp show a man's state"; test "who was winning?" 4 of 5 testers. Part "ruled"; RT-11 numbers "pending".
- First ten hours: yes
- Build or content: n/a (art and animation content)

### 16
- Detail: Every punch can be seen coming 0.45 to 0.8 s before it lands, in the shoulders, feet and breath, never an icon.
- Parts: 1.3.2
- Status as written: designed. "Every incoming blow can be read 0.45 to 0.80 s before it lands"; part "pending"; "recovery times" listed as a gap.
- First ten hours: yes
- Build or content: build for recovery times (a rule); the rest content.

### 17
- Detail: Shove a man into railings and he is out of the fight for 4 s; put a man in the water and he climbs out at the nearest ladder within a minute.
- Parts: 1.3.5, FIT-P18
- Status as written: partly. The 4 s and the ladder are given; the seven places' moves "fitted by height" have no times; part "pending (a reference-game lead)".
- First ten hours: yes
- Build or content: content (paired animations per place); the fit-by-height pairing is a build item.

### 18
- Detail: Fists never kill, but a man who falls with his head by a kerb edge, already beaten, can die, and the town treats it as a killing.
- Parts: RT2-12, 1.3.7
- Status as written: designed. "head lands within 0.4 m of a kerb's edge... already spent... 1 in 50 to 1 in 20 knockdowns"; deterministic. Status "decided".
- First ten hours: likely
- Build or content: n/a

### 19
- Detail: If Frank loses, he wakes in Grace Rinaldi's kitchen or in hospital, sometimes robbed of his notes but never his coins, and in control within a minute.
- Parts: 1.3.9, RT2-13, 7.9
- Status as written: designed. "comes round on the pavement, in Grace Rinaldi's kitchen or in hospital... in control within 60 real seconds"; robbery takes "paper money (coins are left)", never "the Ledger, his coat or the office keys". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 20
- Detail: The men who rob a beaten Frank are named, have routines, and can be hunted down; a taken envelope becomes a debt that Ron mentions the next day.
- Parts: RT2-13
- Status as written: designed. "named men with routines, whom Frank can front up, send men at, or let go; a taken envelope becomes a debt... said by Ron the next day".
- First ten hours: likely
- Build or content: content (the named men) on rules that exist.

### 21
- Detail: Finish a downed man and the game asks "Finish him?" twice; with fists it is a hospital, with a weapon it is a killing.
- Parts: RT2-11
- Status as written: designed. "holds strike for 2 s, and the game asks 'Finish him?' twice"; the fist/weapon split. Story conflict C-341 over a kick input.
- First ten hours: likely
- Build or content: n/a (kick is a build change if added)

### 22
- Detail: Frank can fight in the boxing club with the death rule off, no blood and no betting, and the men who train there can join his crew.
- Parts: 7.16
- Status as written: designed. "opens 18:00 to 21:30 on Monday, Wednesday and Friday and 10:00 to 13:00 on Saturday... the fall rule off and no blood". The other three pastimes are "no place, hours or design yet (gap)".
- First ten hours: likely
- Build or content: n/a for the club.

### 23
- Detail: Frank can go fishing off the quay, play snooker (no money) and fly pigeons from an allotment loft.
- Parts: 7.16
- Status as written: missing. "The snooker hall, quay fishing and pigeon loft have no place, hours or design yet (gap)".
- First ten hours: no
- Build or content: build for fishing and the loft (new verbs and mini-systems); snooker too; places and hours are content.

### 24
- Detail: Frank can pull a gun from under his coat only on a held key, and an empty revolver clicks, because there is no ammo counter on screen.
- Parts: 1.3.10, RT-10
- Status as written: partly. Click is "in" but "each gun needs visible recoil... a rate of fire, and an empty-gun cue (click and hand action)" is a gap; part "unmeasured/pending".
- First ten hours: no (guns come late; "None in the Hook at the start")
- Build or content: build (hand action, recoil, rate of fire per gun).

### 25
- Detail: Mickey's old revolver is in his inner office desk under the real book, and Frank can only find it once, after Sheila trusts him.
- Parts: RT2-14
- Status as written: partly. "found once when the locked office opens on Sheila's trust (rung 2; see the gap on guns rare and late)"; part "pending".
- First ten hours: likely
- Build or content: content (a prop and a trigger) on existing trust states; the gap on "guns rare and late" is a rule.


## C. Cars and chases

### 26
- Detail: Hit a wall at 35 mph and the cab won't drive on; the firm fetches it and it is off the road for a day.
- Parts: 1.2.4, FIT-F05
- Status as written: partly. "under 10 mph is forgiven, then dented, then crumpled, and from about 35 mph... will not drive on"; the middle thresholds are not given; part "pending".
- First ten hours: likely
- Build or content: content/tuning (threshold values).

### 27
- Detail: Smash the front of the cab and it pulls to one side until mended, and a broken lamp darkens the road at night.
- Parts: 1.2.4 (Y1.1)
- Status as written: partly. Stated as raised by Y1.1 with no values for pull strength or lamp reach; part "pending".
- First ten hours: likely
- Build or content: build (steering bias from damage, headlamp lighting as part of damage).

### 28
- Detail: Frank's dented cab becomes a thing witnesses remember, and passers-by remark on how battered it is.
- Parts: 1.2.4, 1.2.9
- Status as written: partly. Dent is "a mark witnesses remember" (designed); the passers-by remark is "Not yet... for the design proof to place".
- First ten hours: likely
- Build or content: content (remark lines keyed to a cab-state value).

### 29
- Detail: Run down a pedestrian and the game gives Frank two seconds to choose to stop or drive off; drive off and the street says "a Mickey's cab knocked her down and never stopped".
- Parts: 1.2.5, FIT-P04
- Status as written: designed. "The choice... comes within 2 s; an ambulance takes about ten game minutes"; fall by speed given. Status "ruled". Nobody steps out inside the 23 m stopping distance.
- First ten hours: likely
- Build or content: n/a

### 30
- Detail: Honk the horn outside a door and the fare comes out within 10 s; blast it long on a quiet night and lit windows show faces.
- Parts: 1.2.11
- Status as written: designed. "a waiting fare inside 15 m comes out within 10 s"; horn heard about 60 m by day. Part "pending (a reference-game lead)".
- First ten hours: yes
- Build or content: n/a

### 31
- Detail: Frank's cab boot holds a spare coat or the envelope; a constable who stops him with cause can look in it, and what is inside survives a save.
- Parts: GV-01, 1.6.6, 1.6.9
- Status as written: designed. "A constable who stops the cab with cause may look in it, and what is in the boot survives save and load. A body goes into the boot in 4 s." Status "decided".
- First ten hours: likely
- Build or content: n/a

### 32
- Detail: A passenger who knows the town calls the way in a chase: "left after the chapel, he cannot follow you through the yard", with no marker on screen.
- Parts: GV-03, 1.2.7
- Status as written: designed. "at least one landmark line per 20 s of chase, each naming a real landmark". Story need (Ron's building-naming state that ends after the night between) is "missing".
- First ten hours: yes
- Build or content: content (lines per landmark); the story state is a small build item.

### 33
- Detail: Lose the police and the patrol searches the last streets you were seen on for up to two minutes, lamp on the turnings, then sits on that road for the night, so you must come back past it.
- Parts: 1.5.4, DP5-C03, FIT-G3
- Status as written: designed. "searches the last-seen streets for 30 to 120 real seconds, lamp on the turnings, then waits on that road for the rest of the night". Part "decided"; DP5-C03 "pending" on the band.
- First ten hours: yes
- Build or content: n/a

### 34
- Detail: Drive to the edge of the Hook during a chase and the chase ends there: Frank vanishes for 30 game minutes, which is 60 real seconds, and the constable arrives at the office at ten next morning.
- Parts: FIT-G3
- Status as written: designed. "30 game minutes out and back, which is 60 real seconds"; "a plate read within 18 m in light 0.7 or more is noted... a constable to the office next morning at ten". Status "decided".
- First ten hours: likely
- Build or content: n/a

### 35
- Detail: Chuck a stone with O, or rattle a bin, and the constable leaves his round to look, then rejoins it where he left off.
- Parts: 1.4.8
- Status as written: designed. "A rattled bin moves the beat constable off his round and he rejoins it where he left"; noise reach set by the sound rule (table in DESIGN §2, outside these chapters).
- First ten hours: yes
- Build or content: n/a

### 36
- Detail: A yard dog barks at a stranger, and a scrap of food quiets it, but Frank can never hurt a dog.
- Parts: 1.4.8
- Status as written: partly. "A yard dog barks at a stranger and a scrap of food quiets it for a while; no verb harms a dog"; no duration or reach.
- First ten hours: likely
- Build or content: content (dogs at set yards) plus a food pickup item.

### 37
- Detail: When a constable catches Frank on foot with nothing on him, he only takes his name; run with a weapon in your coat and it's an arrest, and next time that constable searches without being talked round.
- Parts: RT2-22
- Status as written: designed. "Frank's name is taken... a word, no arrest"; arrest if weapon or goods found; "the next challenge by that officer is on cause". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 38
- Detail: Frank can go over six low walls in the Hook in 0.8 s; a constable takes 1.2 s, so a yard-and-fence run really gains ground.
- Parts: 1.1.8, OUT-08, FIT-G4; map.json
- Status as written: designed in speeds; places named by count; but "Set climbing places... their places, heights and times not yet written"; part "pending".
- First ten hours: yes
- Build or content: content (marking places in map data); the extra climbing places are build.

### 39
- Detail: In a car, Frank can skip a ride when Kevin, Terry or a crewman drives; it passes exactly the drive's time on the clock, and there is no other fast travel.
- Parts: 1.2.8, 6.9
- Status as written: designed. "skip the ride, which passes exactly its drive time on the clock"; "free fast travel is out". Status "ruled".
- First ten hours: likely
- Build or content: n/a


## D. Jobs with the hands

### 40
- Detail: Frank has five debtors on Mickey's book (Darren £22, Wayne £30, Lee £15, Julie £9, Iveson £80), and every one pays in a different way: news, goods, a stand-off, nothing, a yard hand.
- Parts: 1.6.4, 7.1
- Status as written: designed. Names and sums given, each debtor's way of paying given; "a debtor pays what the purse holds"; part "unmeasured".
- First ten hours: yes
- Build or content: n/a

### 41
- Detail: Frank can break into a place three ways: borrow a key (Ian Megginson knows every lock on the street), find the back way left open, or force it, which shows on the door for a day.
- Parts: 1.6.1
- Status as written: designed. "Several keys to every lock; force is loud, shows for a day and is a crime"; a challenger "warns twice then acts within half a minute (lead)".
- First ten hours: yes
- Build or content: n/a

### 42
- Detail: Searching takes real time: a drawer 2 s, a desk 4 s, a wardrobe 5 s; in a dark room it takes twice as long without a torch, and a moving torch beam shows from the street.
- Parts: 1.6.2, 1.6.12
- Status as written: designed in numbers although the headers say "none yet"/"unmeasured"; a gap: "taking something must say what was taken... the design describes no feedback".
- First ten hours: yes
- Build or content: build for the "what was taken" feedback rule.

### 43
- Detail: Lift a key from a man's pocket with a 2 s held press: he feels it if he's attentive or the light is good or there are fewer than three people near; otherwise never. There is no dice roll.
- Parts: 1.6.13
- Status as written: designed. Fixed limits stated; "A lift on an attentive person... is always felt". Part "pending (a reference-game lead)".
- First ten hours: likely
- Build or content: n/a

### 44
- Detail: Stolen goods carry a hot mark; the owner recognises his own radio in a shop window, and till notes stay hot for a week.
- Parts: 1.6.3
- Status as written: designed. "Notes from a till are hot for a week... recognises his own goods"; fence rate 0.33 (jewellery 0.2, video recorder 0.4); haggle three offers at most; buyback "within 7 game days at the price plus a quarter". Part "unmeasured".
- First ten hours: likely
- Build or content: n/a

### 45
- Detail: Casing a shop by standing opposite or sitting in a parked car writes the shop's hours, key-holder and open back way in the Ledger as Frank saw them.
- Parts: 1.6.11, 6.2.2
- Status as written: designed. "each written in the Ledger as Frank sees it... Hours are windows, not minutes". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 46
- Detail: A phone box call costs 10p, 999 is free, and an anonymous call brings a constable to the spot that night but never makes an arrest alone.
- Parts: RT2-19
- Status as written: designed. Costs and effect stated. Status "decided".
- First ten hours: yes
- Build or content: n/a

### 47
- Detail: Frank's witness who sets off to a phone box is seen going; shout "Oi!" and she stops for about 2 s, and he can talk her round, pay her, threaten her or let her go.
- Parts: 1.4.5, 1.4.7
- Status as written: designed. "at least 30 real seconds"; "'Oi!' stops her for about 2 s"; a threat stops police report "never the street's talk"; statement signed "at nine next morning". Status "ruled".
- First ten hours: yes
- Build or content: n/a


## E. Interface and the Ledger

### 48
- Detail: There is no clock on screen: press N and Frank looks at his watch for 2 s, or read the Harbour Board's clock, or listen for the chapel bell striking the hours.
- Parts: 6.1.5; tune.json
- Status as written: designed. "N raises Frank's watch and the hour shows for 2 s... the chapel bell strikes the hours by day". Status "ruled".
- First ten hours: yes
- Build or content: n/a

### 49
- Detail: A line low on the screen says what Frank has just come to believe: "Ada saw you at the yard gate, he thinks."
- Parts: 6.1.3; ledger-texts.json
- Status as written: designed. "in words with no icon and no meter"; shown "within 3 s". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 50
- Detail: Frank's notebook shows what he thinks each person knows about him slot by slot, marked "sure", "thinks so" or "guesses" by how he learned it.
- Parts: 6.2.1; ledger-texts.json
- Status as written: designed. "said to his face is sure, saw them looking is 'thinks so', two heads together is 'guesses'". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 51
- Detail: Frank's money is said in words, never to the penny: "Thirty-one pounds in your pocket. The tin has about forty. Rent, eighteen, Friday. Darren still owes twelve."
- Parts: 6.2.4
- Status as written: designed. Sample line and numbers (start £23.50, rent £18 Friday). "the tin 'about £40', never to the penny". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 52
- Detail: At the end of Act I the Ledger gives Frank's own reading of how things stand, built only from signs he saw, never the true state.
- Parts: 6.2.5
- Status as written: designed. "built only from the signs he was given, never the true state... No ending lands while his own reading says things are quiet." Status "decided".
- First ten hours: likely
- Build or content: n/a

### 53
- Detail: The map shows only places Frank has been or been told of, and Frank himself appears only at a street sign or landmark, never as a moving dot.
- Parts: 6.3, 6.9; paper-map.svg
- Status as written: designed. "Frank shown only at a sign or landmark, never as a moving marker". Status "ruled".
- First ten hours: yes
- Build or content: n/a

### 54
- Detail: Every direction a person gives Frank is kept in the Ledger to reread, and there is no waypoint anywhere.
- Parts: 6.2.3, 6.9, OUT-09
- Status as written: partly. Ruling quoted, but "gap, run 4: the entry's exact wording and test to be written"; 6.9 itself "ruled".
- First ten hours: yes
- Build or content: build (a rule storing the direction as a Ledger entry).

### 55
- Detail: Get lost for 90 s and Frank mutters the landmark once; after three minutes the next stranger within 5 m offers to point the way.
- Parts: 6.9
- Status as written: designed. "Lost for 90 s, Frank's own line repeats the landmark once; after three minutes the next person within 5 m offers the way".
- First ten hours: yes
- Build or content: n/a

### 56
- Detail: The local paper comes out twice a week and prints only what Alison Sedman actually saw or was told, so a story about Frank is only as sure as her source.
- Parts: 6.10; letters-and-print.json
- Status as written: designed. "every printed line traces to what Alison saw or was told". Status "decided".
- First ten hours: likely
- Build or content: n/a

### 57
- Detail: Photo mode freezes the town, frees the camera within 10 m of Frank and hides all interface; leaving returns the frozen moment exactly.
- Parts: 6.8
- Status as written: designed. "save hash equal"; "no interface pixel". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 58
- Detail: Type what you want to say to anyone: "a tenner" is read as 10 pounds, and offering more than Frank carries fails in character.
- Parts: RT-14, 6.7
- Status as written: designed. "an offer's amount is read exactly... an offer above what Frank carries fails in character"; 300-line set, 98.3% agreement. Status "sourced".
- First ten hours: yes
- Build or content: n/a

### 59
- Detail: Opening the Ledger or the paper map stops Frank but not the town, so you can be robbed while reading your notes.
- Parts: RT-18, 6.3
- Status as written: designed. "Opening the Ledger, the paper map or a letter stops Frank but not the town"; assist offered. Story conflict C-343 (clock slowed on authored rides).
- First ten hours: yes
- Build or content: n/a for the base rule.

### 60
- Detail: Talk in the cab or on a walk doesn't stop the clock: the world goes on while Frank talks.
- Parts: RT2-20, 1.2.7
- Status as written: designed. "Talk staged while walking or driving... runs the clock at its rate". Status "decided".
- First ten hours: yes
- Build or content: n/a

## F. Shape of the game

### 61
- Detail: On Sunday Sheila asks if Frank will wind the firm down, take it over, or refuse to say, and if he refuses she decides from what he does.
- Parts: 7.3, RT-04
- Status as written: designed. "refuse to say leaves Sheila to read his deeds until a third car, a first recruit, or the outfit's ask taken twice in the second week". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 62
- Detail: Each person calls Frank by the name he's reached (the new owner, Nowak, Frank, Frankie), and a step never goes back.
- Parts: 7.7
- Status as written: designed. "Each person uses the name they have reached, a step never goes back and each is heard within a game day." Status "decided".
- First ten hours: likely
- Build or content: n/a

### 63
- Detail: The game has no levels; Frank's hands improve at most a quarter, and skills are taught by people who trust him and kept if lost.
- Parts: 7.7, OUT-06
- Status as written: partly. "the taught skills and the quarter cap are owed a design (gap, run 4)".
- First ten hours: no
- Build or content: build (a teaching-by-trust rule and a capped skill modifier).

### 64
- Detail: Frank can press "wait until" for any appointment he knows ("the landing at ten, Ada's pot at nine"), but the wait always stops for a man at the door.
- Parts: 7.11
- Status as written: designed. "offers 'wait until' each known appointment... always stops for what the town has for him". Status "decided".
- First ten hours: yes
- Build or content: n/a

### 65
- Detail: The same street shows more life at 6 pm than at 3 am: Thursday's market and Saturday's match fill a camera frame with 15 to 25 people.
- Parts: GD-02, FIT-F32
- Status as written: partly. Bands given but part "pending"; "The 1990 archive ceiling is still owed".
- First ten hours: yes
- Build or content: content (crowd rows); the density rule is built.

### 66
- Detail: At the evening's end Frank counts the tin against the fare book with Sheila, and the sting or reward is said to his face next morning.
- Parts: 7.2, 6.2.4
- Status as written: partly. Described in one sentence; no rule for what a mismatch does; part "pending".
- First ten hours: yes
- Build or content: build (a tin-versus-book reconciliation and a morning line trigger).

### 67
- Detail: The office chalkboard puts cars on ranks; a car on the rank is the firm's eyes there, and can give Frank an alibi.
- Parts: 1.7.3
- Status as written: partly. "A minute a day at most; Pauline runs it if he never touches it"; part "unmeasured"; the visible score (Danny's arrow, CAMMACK on a shutter) is "Not covered".
- First ten hours: likely
- Build or content: build for placements-as-witnesses; content for the score.

### 68
- Detail: Frank's whole first hour is staged to the second: control at 0:20, first fare 2:30, a choice and deed (Darren's £22) at 5:30, the landing at 11:30.
- Parts: 7.1, ER-FIRST-01 to 04
- Status as written: designed. Times and ER numbers given. Status "ruled".
- First ten hours: yes
- Build or content: n/a

