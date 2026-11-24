# Candidates B: hidden details from the town blueprint (BLUEPRINT-02, temper, ai-brain)

Read: BLUEPRINT-02-town.md in full, temper/TEMPER-MODEL.md and SUMMARY.md, ai-brain/SUMMARY.md and BRAIN-SWITCH.md. Nothing changed.

Clock note used for "first ten hours": 120 real seconds is a game hour, 48 real minutes a game day, 5.6 real hours a game week (2.1.1). Ten real hours is about 12 game days, so about 1.8 game weeks from Monday 15 October 1990: Act I, two Fridays (19 and 26 Oct), two Thursdays and two Saturdays, the outfit's asks on nights 1, 3, 5, 7, and the start of Act II. Bonfire Night and Remembrance Sunday (week 4) fall outside it.

Status words: designed = rules and exact numbers or data given; partly = words only, or numbers or data missing, or marked pending, unmeasured or gap; missing = wish named, no design. A part marked "pending" or "unmeasured" in the blueprint but carrying full numbers is called designed here, with the blueprint's own word quoted.

## A. Routines and the living town

### 1
- Detail: Run the same save dry, in drizzle and in rain and Quay Street is three different streets, the same way every time.
- Parts: 2.1.4; data/light-weather.json
- Status as written: designed. "The same seed dry, in drizzle and in rain gives three different streets"; rain halves each crowd band, cuts sight and sound, makes the road slippery. Part status "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 2
- Detail: A lit window means somebody is home: everyone sleeps at night and their windows go dark.
- Parts: 2.1.1; data/routines.json, data/places.json
- Status as written: designed. "People sleep at night and their windows go dark; a lit window means somebody is home"; routines for 41 people and 24 areas in hook-cast.json.
- First ten hours: yes
- Build or content: n/a (designed)

### 3
- Detail: The town carries on without Frank: the week plays out deed for deed whether he watches or not, and jobs wait while he is away and settle by the clock when he returns.
- Parts: 2.1.3
- Status as written: designed for the core rule ("a week plays out the same, deed for deed, whether Frank watches or not"); partly for mending: "mending a routine after interference is not named".
- First ten hours: yes
- Build or content: build for the mend (a rule that routines close up again after Frank upsets them); the rest is done.

### 4
- Detail: Thursday is market day in Copper Row and the Hook's shops go quiet; on Saturday the match doubles the street at three and five.
- Parts: 2.1.2, 2.1.6, FIT-G9; data/crowd.json, data/timetables.json
- Status as written: designed. Numbers given: Thursday takes a third off shops' daytime bands, Saturday doubles the street at 15:00 and 17:00 for half an hour (up to 30). Marked "unmeasured" and "pending" ("the design's until the 1990 hours are found").
- First ten hours: yes
- Build or content: n/a (designed)

### 5
- Detail: The shops really shut by eight, as the 1950 Shops Act said: the newsagent closes at six, the chip shop at half eleven, and at 23:00 at least three places are still open with people in them.
- Parts: FIT-G10; data/timetables.json
- Status as written: designed. Full hours list for newsagent, caff, chip shop, launderette, pawn (back room by knock to 22:00), boxing club, chapel hall, dock tea stall, ferry window; part status "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 6
- Detail: There is no pub: after work the regulars meet at the caff and the launderette, and every shop, caff and tea stall serves no drink.
- Parts: 2.1.1 (A day, not a post), FIT-G10
- Status as written: partly. "Partly: hourly routines exist; short are chained jobs and a shared evening place. Feature only; no timing."
- First ten hours: yes
- Build or content: build (a routine structure of job chains that end at a shared evening place); the opening hours already exist.

### 7
- Detail: When it rains people shelter in doorways and the bus shelter and open umbrellas.
- Parts: 2.1.4 (Weather changes people)
- Status as written: partly. "rain already empties the street and halves each crowd band; where people stand and umbrellas are not yet named."
- First ten hours: yes
- Build or content: build (a rule that sends people to cover, not only thins them); umbrellas themselves are content.

### 8
- Detail: Nobody ever pops into existence or vanishes in front of Frank: crowds spawn out of sight.
- Parts: 2.1.5 (Checklist A13.25, A25.16)
- Status as written: missing. "missing: nobody may appear or vanish in plain view ... with a distance test. Gap for the design proof."
- First ten hours: yes
- Build or content: build (a spawn and despawn visibility rule in the crowd system).

### 9
- Detail: The crowd walks round Frank, looks before stepping into the road, uses the crossings, and nobody steps out within 23 m of a moving car.
- Parts: 2.1.5; data/tune.json
- Status as written: partly. "Named only; not designed beyond"; the 23 m figure is given, but "avoidance distances and step-aside timing are still to be timed from reference footage". Part status "unmeasured".
- First ten hours: yes
- Build or content: build (pedestrian steering and road-crossing behaviour the code must have), then tuning values from footage.

## B. Perception: what a person can see and hear

### 10
- Detail: A watcher sees a shape at 35 m, a mark (your coat, a limp) at 18 m and a face only at 8 m, and the light changes all of it: a still man in a doorway is almost invisible.
- Parts: 2.2.3
- Status as written: designed. Distances and light values (1, 0.7, 0.25, 0.12) given; part status "pending" ("LEDGER's own first values", "waits on a dated study").
- First ten hours: yes
- Build or content: n/a (designed)

### 11
- Detail: A stranger who saw Frank's face clearly from 5 m can describe him but can never name him.
- Parts: 2.2.2, RT2-03
- Status as written: designed. "Recognition is gated by knowing him, never by distance and light alone"; status "ruled".
- First ten hours: yes
- Build or content: n/a (designed)

### 12
- Detail: A person knows Frank for good in only four ways: he spoke to them, they rode as his fare, someone they know named him in his sight, or they saw his face at the office on two different days.
- Parts: 2.2.2, RT2-03
- Status as written: designed. Four triggers with 8 m and light 0.7 given; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 13
- Detail: A man who saw Frank's face once but does not know him can say "that's the man" on seeing it again and point him out to the police, yet cannot name him until told.
- Parts: 2.2.2, RT2-03, 2.6.3
- Status as written: designed. Rule given in three parts; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 14
- Detail: A footstep at 3 am carries about 3.6 m and at noon nothing; a car is heard 44 m by day, a shot 177 m, and rain cuts all of it.
- Parts: 2.2.4; data/tune.json; SND-07
- Status as written: designed. Figures given, including a searched drawer at 2 m and a forced cupboard 10 m at night; part status "unmeasured" ("no reference figure yet").
- First ten hours: yes
- Build or content: n/a (designed)

### 15
- Detail: After a seen deed the whole street goes quieter for a game hour: witnesses talk lower and the sound mix drops at least 6 dB.
- Parts: 2.5.3, 2.2.4 (SND-13)
- Status as written: designed. "witnesses talk quieter for a game hour"; SND-13 "fall at least 6 dB in that street for about a game hour (own design)".
- First ten hours: yes
- Build or content: n/a (designed)

### 16
- Detail: Wear the same coat as last night's job and the shopkeeper knows it again; change coat and the face stops matching, but a deed from the car always names the car.
- Parts: 2.2.5, GV-02
- Status as written: designed. "the coat buys doubt about the face and none about the car"; "decided" and "ruled".
- First ten hours: yes
- Build or content: n/a (designed)

### 17
- Detail: Frank can walk out of a witness's memory by changing one thing: swap the coat, repaint the car, put on a cap and scarf at night, visit the barber for a week, or walk apart from Ron, but anyone who already told the street still names it.
- Parts: GV-02, 2.2.5
- Status as written: designed. Each slot's remedy given, "gossip already carried is never undone"; a cap or scarf is itself a mark by day; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 18
- Detail: Walk into a private shop-back or yard and the owner warns, warns again, then acts within half a minute; the customs shed and the Harbour Board's back office skip the first warning.
- Parts: 2.2.6; data/places.json
- Status as written: designed. "warns, warns again, then calls someone or acts, within half a minute at worst"; "forbidden places ... skip the first warning"; part status "unmeasured".
- First ten hours: yes
- Build or content: n/a (designed)

### 19
- Detail: A forced door shows for a day, broken glass stays broken until the owner mends it, blood stays until rain or a bucket, and a beaten Frank carries bruises three days and a limp for one.
- Parts: 2.19, 2.2.6
- Status as written: designed. Durations given; "Marks keep across save and load, and nothing is ever wiped"; "ruled".
- First ten hours: yes
- Build or content: n/a (designed)

## C. Memory

### 20
- Detail: A crowd extra who sees anything of Frank's deed becomes a real person with a fixed face, coat, home and routine, and can be found again at his usual places.
- Parts: 2.3.1, RT2-10
- Status as written: designed. "A kept extra remembers for good ... After seven game days with no open matter he lives at the soft edge"; "decided". Face and coat generation for extras is not detailed.
- First ten hours: yes
- Build or content: n/a (designed); content volume (faces and coats for kept extras) is a cost, not a new system.

### 21
- Detail: A shopkeeper who saw "a man in a dark coat" says exactly that, "could have been anyone", even when Frank was the only man in the street.
- Parts: 2.3.2
- Status as written: designed. "A witness is only as sure as what they caught"; "ruled".
- First ten hours: yes
- Build or content: n/a (designed)

### 22
- Detail: Frank's own Ledger grades what people know in plain words: said to his face is sure, "saw them looking" is "thinks so", two heads together is "guesses".
- Parts: 2.3.2, GV-02, RT-07
- Status as written: designed. Three grades given; "ruled".
- First ten hours: yes
- Build or content: n/a (designed)

### 23
- Detail: A regular who suddenly stops turning up is noticed, asked after and talked about.
- Parts: 2.16 (The gap the bar leaves)
- Status as written: partly. "Already covered for a killed or missing man; partly for an ordinary absence such as illness."
- First ten hours: likely
- Build or content: build (a rule that any missed routine becomes a trace someone finds); the lines for it are content.

## D. Gossip, the paper and how Frank is shown to know

### 24
- Detail: Tell one person and it spreads, but each retelling is weaker: about 0.8 a hop, gone after about seven, and told only between people who know each other and meet within 6 m.
- Parts: 2.4.1; data/tune.json
- Status as written: designed. Numbers given; "decided" but "no outside measurement". A deed seen by one principal reaches about five of nine on the first day.
- First ten hours: yes
- Build or content: n/a (designed)

### 25
- Detail: How a deed was done travels with the story: a man who held back is retold as restraint, a cruel one as cruelty.
- Parts: 2.4.1
- Status as written: partly. One sentence: "How a deed was done (restraint or cruelty) travels with the telling"; no data, no rule on what changes in the telling.
- First ten hours: yes
- Build or content: build (the story record must carry a manner field that the retelling and the posture ladder read).

### 26
- Detail: Talk cools by kind: a scuffle in a day or two, a break-in about three, a robbery about a week, but a body never cools.
- Parts: 2.4.2; data/tune.json
- Status as written: designed. Days by kind given; part status "pending" ("a reference-game lead"); "needs new golden rows".
- First ten hours: yes
- Build or content: n/a (designed)

### 27
- Detail: People react to Frank before a word is said: a woman at the bus stop looks a beat too long, the grocer serves him without a word, a docker crosses the road, a man says "you want to watch yourself, son".
- Parts: 2.4.3; data/lines/
- Status as written: designed. Six-step ladder (notice, watch, comment, avoid, refuse, confront); "a told version never above a seen one"; "decided". Lines are in data.
- First ten hours: yes
- Build or content: n/a (designed)

### 28
- Detail: Every deed anyone saw comes back to Frank in week one: someone he has met says it to his face within a game day, and it can happen within his first 30 minutes (Darren, at minute 13).
- Parts: 2.4.4; MEM-01, MEM-10
- Status as written: partly. Part status "pending"; "the rule is written for week one only; later weeks and the line bank are missing."
- First ten hours: yes
- Build or content: content (the line bank per deed kind and speaker kind) plus a small rule extension to later weeks.

### 29
- Detail: The local paper comes out twice a week, but it only prints what reporter Alison Sedman actually knows, so a story about Frank is only as sure as what she was told.
- Parts: 2.4.5; data/letters-and-print.json
- Status as written: designed. "A story prints only what she knows"; letters go into the Ledger; "ruled". The paper's name is owed.
- First ten hours: yes
- Build or content: n/a (designed)

### 30
- Detail: The newsagent's window has notices, and the cab office has a board, so the world writes things down.
- Parts: 2.4.5 (The world writes things down), 1.7.3
- Status as written: partly. "the paper is covered here and the board in 1.7.3; newsagent window notices are not."
- First ten hours: yes
- Build or content: content (notices), small system to tie them to events.

## E. Witnesses and what they do next

### 31
- Detail: A witness sets off on foot to a friend, a phone box or the station, and Frank can watch her go: no mobiles in 1990, so the walk is the timer, at least 30 real seconds.
- Parts: 2.5.1
- Status as written: designed. "at least 30 real seconds (50% longer with the assist)"; "'Oi!' stops a walker for about 2 s"; "ruled".
- First ten hours: yes
- Build or content: n/a (designed)

### 32
- Detail: A neighbour crosses the road to tell the grocer, and who heard depends on who talked.
- Parts: 2.5.1 (Word passed person to person)
- Status as written: partly. "Already covered for a witness walking to tell; partly for second-hand tellers shown crossing the street."
- First ten hours: yes
- Build or content: build (the walk-to-tell behaviour applied to gossip passing, not only to reports).

### 33
- Detail: A threat can stop a witness signing for the police, but never stops her telling her sister.
- Parts: 2.5.2; data/tune.json
- Status as written: designed. "A threat can stop a report to the police, never the street's talk"; "ruled". Core must change (TEMPER section 8.3, today Contain stops both).
- First ten hours: yes
- Build or content: n/a (designed)

### 34
- Detail: Pay a witness and she remembers being paid, and an honest one cannot be bought at all.
- Parts: 2.5.2, 2.14; temper tempers.json
- Status as written: designed. "Paid, she remembers being paid"; in the test week "none could be bought even with two weeks' money".
- First ten hours: yes
- Build or content: n/a (designed)

### 35
- Detail: Mickey's own people never go to the police about one of their own, and neither do Rita, Wayne, Hal, the scrap dealer, the customs officer or the outfit's man, because of their trade.
- Parts: 2.5.2, 2.14; temper law dial
- Status as written: designed. Named list; law 0.15 or under replaces the old flag.
- First ten hours: yes
- Build or content: n/a (designed)

### 36
- Detail: After a seen deed people look, one gathers and drifts back, and a person with the nerve may step in unarmed at a hold-up or a beating.
- Parts: 2.5.3; temper nerve (stepping in rule: nerve 0.75 less 0.05 per bystander, at most 4)
- Status as written: designed. "ruled"; formula and the research behind it given in TEMPER-MODEL.
- First ten hours: likely
- Build or content: n/a (designed)

### 37
- Detail: Bystanders who see a weapon run away from the danger and towards doors, not past it.
- Parts: 2.5.3 (Checklist A13.18)
- Status as written: missing. "missing: bystanders who saw a weapon must run away from the danger and toward doors ... with a test. Gap for the design proof."
- First ten hours: likely
- Build or content: build (a flee-to-cover rule: pick a door away from the threat).

### 38
- Detail: Three seen deeds on one street in two days and it goes on edge: doors locked earlier, shops shut early, witnesses setting off sooner, and a second constable walking the beat half a cycle behind.
- Parts: 2.5.4, FIT-G5; data/tune.json, data/police.json
- Status as written: designed. Numbers given (gaps halve to 2 minutes at Mickey's door, 4 at the yards' lane); part status "pending" ("a reference-game lead").
- First ten hours: likely
- Build or content: n/a (designed)

### 39
- Detail: Repeat deeds on a street make witnesses quieter, fewer people go out, and talk moves to the counter.
- Parts: 2.5.4 (Repeated deeds grow the response)
- Status as written: partly. "the street on edge has witnesses telling sooner, the opposite of quieter witnesses; fewer people out and talk of it at the counter are for the design proof to weigh."
- First ten hours: likely
- Build or content: build (a decision first: the part contradicts itself; then a street-mood effect on crowd density and where talk happens).

### 40
- Detail: An unseen deed is still found: the cleaner at six, the owner on his return or the first dock worker finds the glass, and nothing is found by a dice roll.
- Parts: 2.5.5; data/routines.json
- Status as written: designed. "found by the first person whose routine passes it ... holds only the aftermath"; part status "pending".
- First ten hours: yes
- Build or content: n/a (designed)

### 41
- Detail: Sink a body from the quay edge in 3 s and it is never found, but the missing man becomes the town's question: his landlady asks, his mates at the dock gate ask, DS Ellis asks.
- Parts: 2.5.5, 2.16
- Status as written: designed. "A body hidden or sunk ... is never found"; named askers; "pending" and "ruled".
- First ten hours: likely
- Build or content: n/a (designed)

## F. Police and law

### 42
- Detail: The night constable walks the same beat every night at 1.1 m/s, tries Mickey's door every lap, and a player who watches can learn it to the minute: about 7 minutes round.
- Parts: 2.6.1, FIT-G5; data/police.json
- Status as written: designed. Beat lengths, speeds, 15 s landing look, gaps (Mickey's door in sight at least every 4 real minutes) given; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 43
- Detail: If a constable stops Frank and searches him, he finds exactly what is under the coat and in his hand, and keeps it, cash included.
- Parts: 2.6.2, RT-17
- Status as written: designed. "he finds exactly what is under the coat and in the hand, and what he finds he keeps"; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 44
- Detail: Offer a note to one of the two bought constables and he looks away once (£50) or loses a statement once (£200); offer it to an honest one and it is a crime he saw.
- Parts: 2.6.2, 2.6.8; data/people/
- Status as written: designed. Prices and limits given; "ruled". Colleague who sees the bribe keeps it.
- First ten hours: likely
- Build or content: n/a (designed)

### 45
- Detail: Talk alone never gets Frank arrested: it takes a signed statement from someone who knew it was him, or an officer who saw it.
- Parts: 2.6.3
- Status as written: designed. "decided"; arrest rule and station memory given.
- First ten hours: yes
- Build or content: n/a (designed)

### 46
- Detail: An arrest costs hours, not a game over: about 6 for a window, 8 for a wounding, 12 for a robbery, 22 for a killing, in under 2 real minutes of play, and the street sees him go.
- Parts: 2.6.4; CLOUD-FIGURES B2
- Status as written: designed. Hours by deed and PACE limits given; part status "sourced". Ron's remand is a gap (C-336).
- First ten hours: likely
- Build or content: n/a (designed)

### 47
- Detail: DS Ellis climbs four stages and each shows a sign: nothing, her name in the street's talk, an officer at his door, and a car on the street with his description said aloud at least a game hour before any arrest.
- Parts: 2.6.5, RT-13; data/police.json
- Status as written: designed. Triggers, falls and signs given; "decided".
- First ten hours: likely
- Build or content: n/a (designed)

### 48
- Detail: The morning after a deed a constable knocks along the street asking at windows, the spot is walked more often for two nights, and a body brings tape, a torch at night and Ellis.
- Parts: 2.6.10; data/police.json
- Status as written: designed. Part status "pending" ("a reference-game lead"); no circle on screen.
- First ten hours: yes
- Build or content: n/a (designed)

## G. Money, shops and the fence

### 49
- Detail: Frank starts with £23.50, rent is £18 every Friday, and a week of his own taxi fares (£2.50 to £3.50, at least seven) just about pays it.
- Parts: 2.7.1, 2.7.4, FIT-F24
- Status as written: partly. "seven fares at £2.50 is £17.50, under the £18 rent ... gap for the design proof"; "how the driver's half passes through the book is not written: gap".
- First ten hours: yes
- Build or content: build (how the driver's half flows through the fare book; whether fares or rent move); content if only the numbers shift.

### 50
- Detail: Skip the rent and nothing happens at once: the agent says it Monday, two Fridays missed brings a notice to quit the flat, three and Frank sleeps in the office, which can never be lost.
- Parts: 2.7.4, RT-16
- Status as written: designed. Ladder given; "No game over, no dead end"; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 51
- Detail: Night money in the tin cannot be explained, and money spent where it can be seen is a lie someone may one day hold up.
- Parts: 2.7.2, RT-17
- Status as written: designed. "the tin can be lost only by being stolen ... or found in the office search, and that is said in words"; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 52
- Detail: At the count Sheila refuses to launder more than the book will stand: "That's more than the book will stand, love. You sure?"
- Parts: 2.7.3; economy design (M4)
- Status as written: designed in rule, with a number in conflict: part says £10 plus 80% of all fares; economy design counts drivers' fares at 40% and Frank's at 80%, plus £60 a front (C-332). Part status "pending" ("the 80% is PENDING").
- First ten hours: likely
- Build or content: n/a (designed); the number still moves.

### 53
- Detail: Sheila walks out if asked three counts running to put the books off, and comes back if Frank calls at her house.
- Parts: RT2-06
- Status as written: designed. "Sheila leaves if asked ... three counts running; ... she comes back if Frank calls at her house after a game week in which he asked nobody"; "decided".
- First ten hours: likely
- Build or content: n/a (designed)

### 54
- Detail: Shops remember a robber, a man who walked out of a haggle, and a man who robbed the shop next door, and a haggle is three offers at most with no numbers shown but the prices spoken.
- Parts: 2.7.5
- Status as written: designed. "decided"; the three-offer rule given.
- First ten hours: yes
- Build or content: n/a (designed)

### 55
- Detail: The grocer and the newsagent remember Frank's last visit and any trouble, ask after it, and ring the police quicker.
- Parts: 2.7.5 (Shopkeepers remember)
- Status as written: partly. "short is a clerk asking after the last visit, and trust or a quicker call to the police following."
- First ten hours: yes
- Build or content: build (a per-shop trust state that changes call speed); lines are content.

### 56
- Detail: Rita's back room pays about a third of retail for hot goods, less for each further piece in the week, and different buyers take different things: radios at the second-hand shop, car parts at the scrap yard, jewellery from the man at the back of the caff.
- Parts: 2.7.6; CLOUD-FIGURES B3
- Status as written: designed. "about 0.2 for jewellery up to 0.4 for a video recorder"; part status "sourced". Rita opens from rung 2.
- First ten hours: likely
- Build or content: n/a (designed)

### 57
- Detail: Sell Rita a radio for £12 and buy it back for £15 on day six, but not on day eight.
- Parts: 2.7.6 (EC-10)
- Status as written: designed for the number test ("a radio sold for £12 is £15 on day 6, gone on day 8"); partly for the rule: "what is bought back, and from whom, is not written: gap".
- First ten hours: likely
- Build or content: build (a held-goods record with a 7-day timer on the buyer).

### 58
- Detail: The game tells Frank his money in words: "£31 in your pocket. The tin has about £40 in it. Rent, £18, Friday. Darren still owes £12."
- Parts: 2.7.7, 2.8.2
- Status as written: designed. Example line given; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

## H. Debts, the outfit, rivals, crew, position

### 59
- Detail: Mickey's debt book holds five debtors who each need a different answer: Darren pays in what he hears, Wayne in goods from the pawn's back room, Lee stands and it comes to blows, Julie cannot pay, and Dennis Iveson has the money and a yard hand.
- Parts: 2.8.1; data/people/
- Status as written: designed in content. Amounts and the answer per debtor given (£156 in all); part status "unmeasured".
- First ten hours: yes
- Build or content: n/a (designed)

### 60
- Detail: A debtor pays only what is in his purse and the rest stays on the book: "Darren still owes £12", and debtors pay on Friday or not at all.
- Parts: 2.8.2
- Status as written: designed. "A payment never exceeds the debtor's purse"; "decided".
- First ten hours: yes
- Build or content: n/a (designed)

### 61
- Detail: On nights one, three, five and seven Ron arrives after dark in a dark coat with an envelope for the ferry landing, a man says "Mickey's?", and a constable who searches Frank keeps the envelope.
- Parts: 2.9.1; economy 5.6; story S34
- Status as written: partly. "unmeasured"; "the data sweep ... needs the scenes file (data file 18), still to be made from the story on paper; exact values pending it."
- First ten hours: yes
- Build or content: content (scene data); the rules (one ask a night, search keeps envelope) are written.

### 62
- Detail: Each rival climbs the same five rungs (noticed, a visit, pressure, a threat, a sit-down), never skips one, and each is said to Frank's face or shown on his street within a game day.
- Parts: 2.10.1, RT2-07
- Status as written: designed in rule. Part status "decided"; NUMBERS-RUN found the pace too fast or too slow ("an aggressive player's Act II ends on day 12") and proposed fix A or B, not adopted; first-notice days (Widow 8, Cammack 10, Agar 13) are "assumed".
- First ten hours: likely
- Build or content: build (a pacing rule: one rung per rival per five game days, or a paid-hold limit) if the fix is taken.

### 63
- Detail: The first thing the Widow hears of Frank may come from his own day driver, Kevin, over a radio nobody can help overhearing.
- Parts: 2.10.2; data/people/
- Status as written: designed. "Each rival knows only what its own people saw or heard"; named eyes (Lee, Kevin, Susan Coverdale, Rita).
- First ten hours: likely
- Build or content: n/a (designed)

### 64
- Detail: You can recruit a regular two ways: meet a need (slow, holds) or spend a hook (quick, brittle), and a hook recruit breaks first under the same pressure.
- Parts: 2.11.1, RT-07; data/people/
- Status as written: designed in rule. "decided"; but "the loyalty ceiling, nerve and break numbers are still gaps" (2.11.2) and the pressure figure is open (TEMPER section 9).
- First ten hours: likely
- Build or content: build (a pressure figure that decides when each man breaks).

### 65
- Detail: People call Frank by the name he has earned: "the new owner", then Nowak, then Frank, then Frankie, and Sheila withholds his name until she trusts him.
- Parts: 2.12.1; story S1, S40
- Status as written: partly. Ladder "ruled"; but for Sheila "what the state is and what shows it is not yet written (gap)".
- First ten hours: yes
- Build or content: build (a trust state for Sheila, the one name gate that is not knowing).

### 66
- Detail: Walk the same street at rung 1 and rung 3 and at least three things differ: a nod, a door held, a path cleared, "morning, Mr Nowak", or a street that goes quiet.
- Parts: 2.12.4; data/lines/
- Status as written: partly. Part status "unmeasured"; counts set (60 own lines for each of 12 people, 30 for the rest, residents about 5 each after the first loops), but "made after the first loops".
- First ten hours: yes
- Build or content: content (the lines); the rule exists.

### 67
- Detail: The office changes as Frank rises: more phones, a night desk, the board crowded, the flat above stops being Mickey's, and his cars pass him in the street.
- Parts: 2.12.5; data/rooms.json
- Status as written: partly. Part status "unmeasured"; no rung-by-rung list of changes in numbers.
- First ten hours: yes
- Build or content: content (dressing per rung); no new system.

### 68
- Detail: A hook is a fact Frank is sure of, spent once; the person then knows Frank knows and remembers, and a "guesses" line is no hook, only a bluff that works if believed.
- Parts: RT-07, 2.3.2; economy EC-09
- Status as written: designed. "decided"; a hook for money takes £50 to £300 of a purse.
- First ten hours: yes
- Build or content: n/a (designed)

### 69
- Detail: The town's escalation is a fact in its memory, not a meter: nobody carries a gun until one is seen, a shot heard and it never moves on a deed nobody saw or heard.
- Parts: 2.13, RT-12
- Status as written: designed. Four states and fall rule given; "ruled".
- First ten hours: likely
- Build or content: n/a (designed)

### 70
- Detail: The firm runs without Frank: Pauline works the chalkboard if he never touches it, Kevin drives days and Terry nights, and car two is Mickey's own and can never be sold or wrecked for more than a day.
- Parts: 2.15.1, RT2-06; data/people/
- Status as written: designed. Part status "unmeasured"; drivers leave if their half is under £60 two weeks running.
- First ten hours: yes
- Build or content: n/a (designed)

### 71
- Detail: Hit someone with the cab and people ring another firm for a while, then the fares come back as the talk fades.
- Parts: 2.15.3
- Status as written: partly. "ruled"; "fares move to the other firm after a drive-off and come back" is the test, but the amount and speed are not given beyond the 3-day cooling of a hit-and-run (2.4.2).
- First ten hours: likely
- Build or content: build (a fare-share rule tied to cooling, and the second firm's cars).

## I. Death, help and the long marks

### 72
- Detail: Frank cannot die: beaten, he comes round on the pavement, in Grace Rinaldi's kitchen or in hospital, in control within 60 real seconds.
- Parts: 2.16
- Status as written: designed. "in control within 60 real seconds"; "ruled".
- First ten hours: likely
- Build or content: n/a (designed)

### 73
- Detail: Fists never kill on open ground; a man who falls onto a kerb's edge within 3 s of a heavy blow can die, about 1 in 50 to 1 in 20 such knockdowns, and finishing a downed man is a separate choice asked twice.
- Parts: 2.16
- Status as written: designed. Odds, timing and two-step choice given; "ruled".
- First ten hours: likely
- Build or content: n/a (designed)

### 74
- Detail: If Frank stops after hitting someone with the cab, he makes the call from the phone box (10p), the ambulance arrives in about ten game minutes, and his face is now beside the cab.
- Parts: 2.18
- Status as written: designed. "about ten game minutes"; "A car never kills"; part status "unmeasured".
- First ten hours: yes
- Build or content: n/a (designed). A crowd kept back and the constable's notebook are partly covered (content).

## J. Temper: the same deed seen by different people

### 75
- Detail: The same wounding seen by Ada, Darren and Grace goes three ways: Ada reports and cannot be frightened or paid, Darren keeps quiet, folds to a word and takes the money, Grace reports and refuses everything.
- Parts: 2.14; temper/TEMPER-MODEL.md section 7; tempers.json; data/people/
- Status as written: designed. Five dials per person, formulas, and a side-by-side result from a test week over 118 people; "decided". The Core still has to be changed (section 8, "not done here").
- First ten hours: yes
- Build or content: n/a (designed); build is the builder's wiring of the five dials into the Core.

### 76
- Detail: One word frightens 42% of the town, not 86%, and honest witnesses can rarely be bought: 8 of the 48 who would report a wounding would take a week's money.
- Parts: 2.14, 2.5.2; temper section 7
- Status as written: designed. Bands and measured results given; 15 of 63 witnesses reported (24%) against about 29% in British figures.
- First ten hours: yes
- Build or content: n/a (designed)

### 77
- Detail: A frightened person sounds frightened: the nervous voice bank goes to people with nerve 0.35 or under, the steady voice to 0.65 or over.
- Parts: 2.14; temper nerve on-screen note; StreetVoice
- Status as written: designed. "the Core picks the nervous bank at nerve over 0.65 today, which the new meaning makes backwards, so it flips".
- First ten hours: yes
- Build or content: n/a (designed); a one-line code flip.

### 78
- Detail: A person with a long memory for wrongs greets Frank with the old wrong: "You'll want paying for the window, will you", and the cold shoulder lasts.
- Parts: 2.14; temper grudge dial (loss multiplied by 0.6 + 0.8 x grudge); MEM-04, TALK-05
- Status as written: designed. Formulas given; line data is in data/lines/.
- First ten hours: yes
- Build or content: n/a (designed); line writing is content.

## K. Talking to people: what the brain switch changes

### 79
- Detail: People only name facts they really hold: a character cannot reply with a fact the simulation never gave them, and Rita only gives the radios' place under a bargain.
- Parts: BRAIN-SWITCH 8.13.1; claim check; ai-brain/SUMMARY.md
- Status as written: partly. "Status: proposed; the comparison awaits his answer"; claim-check rule written, guarded hybrid "was not run"; first-word time "about 2.8 s", over the 2 s bar.
- First ten hours: yes
- Build or content: build (a decision layer with an allowed set, a classifier and a claim check on the reply).

### 80
- Detail: Nobody in the Hook can be talked into the impossible, however clever the line: 0 of 30 impossible asks were granted, and repeating the same line or reloading did not work.
- Parts: BRAIN-SWITCH 8.13.1, 8.13.4; ai-brain/SUMMARY.md
- Status as written: partly. "0 of 30 impossible asks granted, held by the classifier's tags"; asking again until yes is "owed from the brain job".
- First ten hours: yes
- Build or content: build (guard classes and replay protection are system rules).

