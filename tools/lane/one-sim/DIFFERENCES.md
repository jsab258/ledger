# Where the prototype's own town differs from the real rules, and what the swap changes for the player (step 3b)

Task 4s, run 2, 19 November 2026. Nothing in the prototype's source was changed. The swap itself is step 4, a later round through the publish gate.

Seen by a fresh reviewer the same day (production/lane/REVIEW-ONE-SIM-RUN2.md: pass with fixes). Run 3, also 19 November, applied its fixes here: the police's reach and the one deed (section 5), naming him later (section 4), the count of who can hear a story (section 3), old saves (section 9), and a new section 10 on what the town can be told. Run 3's changes have not had a fresh reviewer.

## What was compared, and how

- The prototype's side: its frozen JavaScript town as it stands in tools/lane/prototype/project/src (rules.js, cast.js, routines.js, seeing.js, gossip.js, events.js, ledger.js, police.js, state.js, clock.js). The readable source, read today. The earlier comparison (production/lane/PROTOTYPE-VS-DESIGN-2026-11-18.md, 18 rows) had to read a squeezed copy; its row numbers are given below as "V3", "V10" and so on, and its numbers were checked against the readable source wherever they are used here.
- The real side: the game's own town code as the browser copy runs it (one-sim.wasm), which gives the C# Core's answers on every row of the golden table. Numbers are from the port's own files, named each time.
- Measured where it could be: `tools/lane/one-sim/one-sim.sh differences` runs differences/measure.mjs, which loads the prototype's own rule files under Node, unchanged, beside the real town through the bridge, and asks both the same questions. Last run in run 3, 18:52 UTC (5 s on a quiet machine, 15 s on a loaded one), the same numbers as run 2's. Three measurements, M1 to M3 below, and since run 3 one check, M4: the table of section 10 against the prototype's own list.
- Read, not measured, where no call exists yet to ask the real rule from JavaScript, or where the prototype's file needs the drawing library to load (police.js). Each such line says "read".

What stays the prototype's own after the swap, so is not compared: money, debts, jobs, fares, fights and talk, and its street (the map, walking, light, lines of sight, weather, the cab, the screens).

## The short answer

After the swap the player meets a larger, quieter, more regular street. More people (41, not 28), most of them without a name yet. People stand elsewhere than he remembers: of the nine people both casts hold, somebody who is out is in the same part of the street in both only about a third of the time. Everybody moves on the hour. A story about him reaches about as many people on its first day, then stops sooner: fewer of the people he knows by name will have heard it. It does not cool in a day. The police follow a fixed timetable, a day slower and two hours longer in the cells. And four things he has today have no counterpart behind the bridge yet: how well a witness sees or hears him by the real rule, what the street calls him, how much each person likes or fears him, and the moment of catching two people talking about him.

Three more, found by the review and in run 3. Through the bridge only the damage deed is reported to the police: a blow, a weapon or a killing seen by a witness becomes talk and can bring DS Ellis, but never a statement or an arrest. The real week follows one deed, and the prototype has no act that damages a thing at all, so as the two stand nothing he does in the prototype would bring a constable after the swap (section 5, decisions 5 and 6). And the real town can be told only of what he does badly in sight of others: ten kinds of decent or open act have no call yet (section 10).

## 1. The people

| | Prototype | Real rules |
|---|---|---|
| How many | 28 named people, each with a look, a voice and a card (cast.js) | 41 people, 9 of them named (production/specs/hook-cast.json) |
| In both | 9: Ron Kirby, Sheila Dunn, Darren Milner, Alison Sedman, Father Walsh, Ada, June, Rita, Hal | the same 9 |
| Their ids | sheila, ron, darren, alison, walsh, ada, june, rita, hal | lena, rocco, sam, noor, emil, ada, june, rita, hal |
| Surnames | June Suddaby, Rita Welburn, Hal Metcalfe | June, Rita, Hal: no surname |
| Only here | 19 more, all named (Pauline Kitching, Kevin Needham, Terry Hodgson, Wayne Harrison, Brenda Laverack, Lee Drewery, Grace Rinaldi, Peter and Lily Tang, Susan Coverdale, Nora Cronin, Albert Suggitt, Sylvia Rennison, Dennis Iveson, Norman Dent, Julie Kettlewell, Shaun Hewson, DS Carol Ellis, PC Ibbotson) | 32 more, known by their work only (the dispatcher, the day and night drivers, people of the laundry, the pawn, the docks and the ferry, and so on) |
| The police | DS Ellis and PC Ibbotson are people who walk the street | Steps of the hour: her visit at nine, the constable at ten. Nobody of the cast. |
| Passers-by | Up to 16 walkers, three lads, three fares, six shopkeepers and a yard lad (rules.js, routines.js). They see him, and a passer-by carries what he saw to the first named person he stands near (gossip.js). | Not in the town behind the bridge: its talk is between the 41 (V4 says the same of the game). |

For the player: twelve of the prototype's 19 fit an unnamed job in the real cast by the words of the job (run 1's reading, by eye). Until names are settled, 32 people on the street would be "the dispatcher", "a dock hand". Five prototype people have no place in the real cast at all, the takeaway's keepers among them. Which names stand, and whether the five stay, is a canon question for him, not something the swap may decide. The five people who owe Mickey money (Dennis, Lee, Darren, Julie, Wayne) are in the prototype's money rules, which stay: only Darren is in the real cast under a name, so the other four wait on the names question.

## 2. Where people are (measured, M1 and M2)

M1. The nine people of both casts, asked at the half of every hour of a week: 9 times 168 hours, 1,512 in all. The two sides name places differently, so each prototype place was matched to an area of the cast file by eye, by name (the table is in measure.mjs).

| Person | Same place, of 168 | of those, away in both | Out in one, away in the other | In different places | At a prototype place with no counterpart |
|---|---|---|---|---|---|
| Hal | 147 | 105 | 20 | 1 | 0 |
| Ron Kirby | 137 | 49 | 16 | 9 | 6 |
| Father Walsh | 129 | 84 | 14 | 6 | 19 |
| Sheila Dunn | 123 | 91 | 28 | 17 | 0 |
| Ada | 106 | 106 | 61 | 1 | 0 |
| Rita | 93 | 49 | 70 | 5 | 0 |
| Alison Sedman | 91 | 91 | 50 | 0 | 27 |
| Darren Milner | 68 | 63 | 27 | 24 | 49 |
| June | 63 | 63 | 88 | 11 | 6 |
| All nine | 957 of 1,512 (63%) | 701 | 374 | 74 | 107 |

Most of the agreement is two people being away at the same time. Take those hours out: in the 811 hours when either side has the person out, the two sides have them in the same part of the street in 256, about a third. The matching by eye is cautious. If every one of the 107 hours at a prototype place with no counterpart were in truth the same ground, it would be 363 of 811, still under half.

- Ada is never out in the same place. The prototype keeps her at her window from 5:30 in the morning to 22:36, with chapel on Wednesday and the fish queue on Friday. The real rules have her out on the street from nine to six: her step, the laundry's front, the fish counter, the rank at four, and on Sunday the chapel and its hall.
- Ron, on a weekday. Prototype: the caff from 6:36, the rank from 8:06, the fish queue at 12:18, the rank, the takeaway's queue at 17:24, the rank from 18:30, home at 23:36. Real: the cafe at 7, the rank at 8, the fish shop's front at 12, the rank at 1, the quay at 5, the office at 7, off at 11; on Sunday the allotments.
- June and Rita are out for many hours on one side when they are away on the other (88 and 70 hours).
- Nine prototype places of these nine people were given no counterpart in the cast file. By their names on the prototype's map: bench, corner, fire, harbourdoor, pave, phone, tangs (the takeaway), tearoom and video. Two of them may be real ground under another name (harbourdoor by the harbour office, phone by the kiosk): not settled here, and counted as no counterpart.
- The other way round, by the names on the prototype's map (its 16 rooms and its spots, listed today): the cab office, the cafe, the fish shop, Rita's, Hal's shop, the laundry, the newsagent, the harbour office, the boarding house, the chapel, the market, the bus stop and the ferry have a room or a spot of a like name. The docks, the fish dock, the customs shed, the flats and the allotments have none. For the quay, the landing, the repair yard, the warehouse row and the kiosk the map has names that may be the same ground (pier, pontoon, yard, row1 to row3, phone): not settled here.

M2. When people move. The prototype's 28 people have 183 routine lines: 71 start on the hour and 112 at other minutes. The real cast's 41 people have 537 lines, every one on the hour.

For the player: people he has learned to find are somewhere else, and the street changes all at once on the hour, where today people drift in at odd minutes. The walking between places stays the prototype's own, so it will soften the hour's edge, but everybody still sets off together. The swap needs a table from the cast file's 30 places to spots on the prototype's map, and spots for the places it lacks.

## 3. How a story travels (measured, M3; rules read)

The rules, side by side:

| | Prototype (rules.js, gossip.js) | Real rules (the port: TownRounds.h, Gossip.h; the cast file) |
|---|---|---|
| Who talks | Any two named people who are out, awake, within 4.8 m on the street or 8 m indoors, not both walking | People their routines put in the same place that hour (the cast file's talking range is 6 m). By the earlier reading (V4, not re-read today) only people the cast file ties together talk: it holds 81 ties. |
| How often | Every 4 game minutes, by chance: 0.9 times a weight for how talkative and how close they are | A round every 6 game minutes |
| Each telling | 0.8 times as sure, 0.92 times as hot; the teller's own heat goes up | Less sure with each telling, and below a floor it is not passed on (V5, read in the Core on 18 November, not re-read today) |
| Fading | Heat fades with every ten minutes; it halves in about 20 game hours. How sure they are never fades. | How sure they are halves every 96 game hours, and a story is dropped under 0.03 unless it can never be forgotten (Gossip.h) |
| Who keeps quiet | Each person's own discretion (Sheila high, Darren low) | Mickey's own people handle his deeds privately (the note in TownRounds.h; the cast file says who they are). How that shows in the talk was not traced today. |
| Chance | Drawn fresh each time: two weeks differ | Seeded by the rules: the same week every time |

M3. One story, the same on both sides: he hit a man, seen by Darren alone on Tuesday at half past twelve, and nobody sees him again that week. How many people hold it at the end of each day. The prototype's town was run twenty times with twenty fixed seeds; its numbers are the least, the middle and the most of the twenty.

| End of | Prototype, of the 26 named people who can hear it | Real rules, of its 41 | Of the nine in both: prototype (middle), real |
|---|---|---|---|
| Monday | 0 | 0 | 0, 0 |
| Tuesday | 6 / 11 / 18 | 14 | 4, 5 |
| Wednesday | 23 / 24 / 25 | 22 | 8, 5 |
| Thursday | 23 / 24 / 25 | 23 | 8, 5 |
| Friday | 23 / 25 / 25 | 24 | 8, 5 |
| Saturday | 23 / 25 / 25 | 24 | 8, 5 |
| Sunday | 23 / 25 / 25 | 24 | 8, 5 |

On both sides every copy still names him at the week's end. The prototype has 28 named people, but its talk leaves out the two police (DS Ellis and PC Ibbotson, gossip.js line 74), so 26 can hear a story. Run 2 gave these numbers out of 28.

For the player: on the day itself the two towns are close (11 of 26 against 14 of 41 by Tuesday night). After that the prototype's story reaches nearly everybody who can hear it by Wednesday (24 or 25 of 26). The real one stops at 24 of 41, a little over half the street, and at 5 of the 9 people he knows best where the prototype reaches 8. So fewer familiar faces will bring a deed up, and more of the street stays ignorant of it. What the real town holds, it holds longer: the prototype's heat is half gone in a day, the real story's certainty lasts four. The prototype's "how loud his name is", which today brings DS Ellis (and, by the earlier note, Cammack's lads), is built on that heat and has no counterpart behind the bridge (section 6).

Limits of M3: one story, one witness, one seed of the real rules (they have only one), nobody watching him afterwards, and the prototype's passers-by left at their own behaviour. It measures reach, not what is said.

## 4. Seeing him, and knowing it was him (read, not measured)

| | Prototype (rules.js, seeing.js) | Real rules (the port's Perception.h) |
|---|---|---|
| How far | 4 m in the dark up to 48 m in full light, less in rain (by up to 30%) and in mist at night (22%); 14 m at least indoors; 34 m for a cab with its lamps on | Fixed distances: a shape at 35 m, a mark at 18, a face at 8; recognised at 25 m, but only by somebody who knows him |
| Which way they look | About 124 degrees, and wider for anybody within 3 m | 120 degrees, with a sharp middle of 60 and a rule of its own for a man standing still (V12) |
| How well | One number for clarity; with it a "face score" | Five rungs: someone, a silhouette, a mark, a face, recognised |
| Is it him | Named above a face score of 0.36 if they know who he is (familiarity over 0.5, or they know of the inheritance); else "a man", "a coat", "a cab" | The top rung, for those whose familiarity with him is 0.35 or more |
| Hearing him | A distance for what he is doing (standing, walking, running, the cab), larger in the small hours and smaller in rain and through a window; somebody who only hears a loud act remembers "a man" (seeing.js) | Loudness set against the street's own noise at that hour, and less through a wall (Perception.h). Not behind the bridge either. |
| Naming him later (run 3) | A witness who remembers "a coat" or "the cab" turns it into him once they learn whose coat or cab it is. One who saw "a man" does the same once they know who he is, if they saw his face well enough (a face score above 0.2, or sure above 0.6 and familiar above 0.55). His book, the names and the liking all follow (events.js `link`, lines 48 to 73; the numbers from rules.js). | A story names him only if its first witness recognised him (the top rung), or if it was told as a thing known (Gossip.h NamesHim, line 241; his A5 ruling of 30 September). A shape, a mark or a face is tied to him only by Suspecting, which is not behind the door. |

The real rule's rows pass in the browser copy (T1), but JavaScript cannot ask it yet: the bridge takes "how well" from the caller. So this difference is the main thing still to build for the swap, and it was not measured. For the player it will change who can name him and from how far. The light map and the rain stay the prototype's. And a witness who saw only the coat or the cab will not later come to name him, as they do today, unless Suspecting is put behind the door.

## 5. The police (read; the real side also from the scripted weeks)

| | Prototype (rules.js police, cast.js) | Real rules (the port's PoliceFile.h, TownWeek.h) |
|---|---|---|
| Who gives a statement | A witness who saw it, names him, is sure (0.55 or more), not afraid (under 0.5) and does not like him much (V8's reading; the numbers checked in rules.js today). Ten people never do: Sheila, Ron, Darren, Rita, Wayne, Lee, Hal, Dennis and the two police. | Seeing him do it is enough, unless they are on his side, have been talked round, or are on the cast file's never list. At nine the morning after. |
| When they come for him | The next day at nine; a constable walks down Quay Street to him, and he can run | At ten o'clock; in both scripted weeks that hold a deed, the morning after the statement. He is taken where he stands. |
| What reaches the police (run 3) | Any act a witness will give a statement on, violence included: a blow seen brings a statement, a constable and five hours in the cells | Only the week's one deed, and always as damage (TownWeek.h NineReports, lines 121 to 138). A sighting handed in through the bridge goes into the talk and never into a statement. |
| How many deeds the week follows (run 3) | Every act is its own event, with its own witnesses | One. The rules keep one deed's story and its witnesses, and a second would replace them (TownWeek.h Deed, lines 103 to 106). The bridge refuses a second deed for that reason. |
| In the cells | 4 game hours; 5 for violence; 2 more if he ran. He is billed 25.00, or 40.00 if he ran. | Through the bridge: 6 hours for the damage, then charged or bailed. No bill. The rules also hold 2 hours and a caution if he owns up, 8 for a wounding, 12 for a robbery and 22 otherwise, but no call of the bridge reaches those. Only the raw front door can, with a report and an arrest made by hand, as one scripted week of the tests does. |
| DS Ellis | On Thursday or Friday between ten and one, when his name is loud enough (2.2); asks up to five people | At nine, from the second day, whenever the rules find a reason (the street's talk of him is one, a body another) |

The real side, as the scripted weeks play it (the C# Core's own rows): a window put in on Tuesday at half past twelve with Darren watching. Three people find it at five that afternoon and one more at eight the next morning. Darren goes to the police on Wednesday at nine. DS Ellis comes on Thursday at nine, for the talk. A constable takes him on Thursday at ten, and he is charged.

Measured through the bridge in run 3 (checks T11 and T12, after the reviewer measured the same by hand). A blow seen by three people, one of whom recognised him: two days on 23 people hold the story, nobody has gone to the police, nobody has come for him, and DS Ellis came once, on the next morning at nine, for the talk. And the window with Darren watching, followed by a second deed that evening: before run 3 the second deed wiped out the first one's witness, so that Darren never went to the police; now the second deed is refused, and Darren goes on Wednesday at nine and the constable comes on Thursday at ten, as in the scripted week.

One thing neither run 2 nor the review said: the prototype has no act that damages a thing. Its 53 kinds (section 10) hold no window put in; the nearest is the cab put into something. So with the prototype as it stands, the bridge's deed has nothing to call it, and after the swap nothing he does would bring a statement or a constable. Decisions 5 and 6 put this to him.

For the player: the same deed is answered a day later and costs two more hours (six, not four). Darren, who never talks to the police in the prototype, does in the real rules. DS Ellis can come on any morning from Tuesday on, not only late in the week. There is no chase: the real rules take him where he stands, so the prototype's chase would have to stay as the prototype's own scene around the town's step, or go. The solicitor's bill is money, which stays the prototype's, but the real rules have no bill, so the two would disagree unless he rules on it (V10).

## 6. What each person thinks of him, and what the street calls him (read)

The prototype keeps, for every named person, how familiar he is to them, how much they like him and how much they fear him (events.js), and from what they know it works out what they call him, from "a man" up to his name, and what the street as a whole calls him (gossip.js). Debts read the fear and the liking (V14). The fighting ladder reads what each person knows of his violence (gossip.js). Talk reads them too (not traced today).

The real rules keep other things for each person: nerve, loyalty and suspicion (the port's Gossip.h and Suspicion.h). None of them is behind the bridge yet, and they do not mean the same.

For the player: this is the part of the swap with no clean answer today. If the prototype's liking, fear and names stay as they are, they would rest on the prototype's own memories, which the swap takes away. If they go, fights, debts and talk lose what they read. It needs a decision before step 4: either these three stay prototype rules fed from the town's facts (who knows what, from `town.knows()`), or the real counterparts come through the door first. Recommended: the first, because it changes least of what has been playtested.

## 7. The week's shape (read)

| | Prototype (rules.js story, state.js) | Real rules (asked of the browser copy today) |
|---|---|---|
| Starts | Monday 15:36, off the bus | Whenever the clock starts; the bridge is opened at 15:36 |
| Ends | Friday, from four in the afternoon | Sunday (day 7), with Sheila's question |
| Ada's tea | Between 18:30 and 21:36 | Wednesday: she asks at ten in the morning, the tea is that evening and is closed at eleven |
| Ron and the envelope | From 17:12 | At eight in the evening on an ask night, never while he is held; the first ask is on Monday night |
| The clock | One game hour is 45 real seconds | The town has no clock speed of its own (V1) |

For the player: the prototype's week is five days and its beats sit at its own hours. The real week is seven, and it will not be hurried. Tried today through the bridge: on Friday at half past four the real rules refuse Sheila's question, and on Sunday morning they take it. So the five-day week, which the earlier note (V18) recommends keeping, does not fit the real rules as they stand. Either the prototype's week grows to seven days, or the day of Sheila's question becomes something the game can set, which is a change to the Core and its golden rows. It is a choice about the week, so it is his.

## 8. The Ledger (read)

The prototype's Ledger is his own book: only what he himself saw and heard (ledger.js). That rule stays the prototype's. What feeds it changes.

- Who saw him do it: still worked out by the prototype's own geometry, so unchanged until the real rule for seeing is behind the bridge (section 4).
- Who says it to his face, and whom he catches talking about him. Today both come from the prototype's own town: when a story about him passes between two people within 18 m of him and he can see one of them, they turn to look and his book notes it (gossip.js). After the swap, who holds a story comes from the town (`town.knows()`). It says who first saw it and how many tellings away each holder is. It does not report each telling as it happens, so the moment of catching two people talking has nothing to start it. The town code knows each telling; the front door does not hand them out yet.
- The end screen's truth beside his book (a playtest view) reads the prototype's own minds today: who saw it, who was told, who holds it without knowing it was him. After the swap it would read the town's facts, which carry the same three and add how well the first witness saw him.

For the player: his book works as before but fills from a different town, and "two people stop talking as you pass" is lost unless that call is added before the swap.

## 9. Saves (read and tested; rewritten in run 3)

The prototype's save holds its own town: each person's mind, every event, who told whom (saving.js). After the swap it holds the town object the bridge hands it (BRIDGE.md).

Run 2 recommended that a save from before the swap should not be offered. That went against the prototype's own standing rule and is withdrawn. The prototype has kept every older save loading through every change (its CHANGELOG and DESIGN_NOTES say so each time, and it has a test for it, test/oldsave.mjs). Nothing forces its save version up: its restore already fills in what an older save lacks.

What is built (run 3: `openTownFromOldSave` in the bridge, check T12). A save with no town in it opens a fresh town at the save's clock. Each thing its people saw him do with their own eyes is told to that town at that minute, as a sighting at the rung their old memory supports (BRIDGE.md gives the reading). The call hands back what was told, what was left out with the reason for each, and what the player loses in plain lines.

What the player loses, measured on a save written by hand in the prototype's own shape (Wednesday 14:00, eight minds; T12):

- What people had only been told. The new town's talk starts again from those who saw. Two days on, a blow seen by three people was held by 23.
- What the 19 people with no match in the real cast saw (section 1).
- The decent and open acts, which the town cannot be told yet (section 10).
- The week's beats that are already past. A town opened on Wednesday at 14:00 holds Monday's ask as never delivered, Ron comes again on Wednesday night, and Ada does not ask him to tea at all that week, because she asks at ten on its day. His earlier answers to the asks are not carried over.
- Nothing of what each person thinks of him or what the street calls him: those stay the prototype's own (section 6). But they no longer rest on the same memories.

Still to do in step 4: the prototype's real old-save test, with a save from a real older build, in the page. If he would rather such saves were not offered, that is a scope choice for his list, with these costs stated. It is not the default.

## 10. What the town is told (run 3; read, and the table checked by the script)

The prototype's town knows 53 kinds of thing about him (kinds.js: 52 kinds of act, good and bad, and "word", something he was told). Each has a number for how newsworthy it is, how it reads (from menace to decent) and how grave a crime it is. The real town has no such list. Through the bridge it can be told two things: the one damage deed (`town.deed`), and a sighting under a name the caller picks (`town.saw`). Its own steps make the rest of its stories themselves.

The table lives in the bridge (PROTOTYPE_ACTS in wasm/one-sim-bridge.mjs). `one-sim.sh differences` checks it against the prototype's own kinds.js (M4, run 3: 53 kinds, 53 rows, none against the rule below).

| What the town is told | The prototype's kinds | How many |
|---|---|---|
| The deed (damage to a thing) | None. The prototype has no act that damages a thing. The nearest, the cab put into something (crash), is kept as a sighting. | 0 |
| A sighting, by `town.saw`, under the kind's own name with the event's number | night_out, coat_day, ran, parcel, pickup, drop, cab_night, talk_ellis, talk_press, stare, squareup, threat, shove, strike, weapon_out, weapon_used, kill, set_on, debt_paid, paid_info, bribe_try, lied, ran_police, bag_taken, rent_late, knocked, crash | 27 |
| Nothing: the real rules make this story themselves when their own step or call runs | job_yes and job_no (his answer to the night's ask), no_show (six o'clock, a night away), tea, tea_late and tea_snub (the tea's minutes and its close at eleven), arrested (ten's constable: who saw him taken), ellis_asked (nine's DS Ellis: whom she asked), choice_wind, choice_take and choice_silent (the week's end) | 11 |
| Nothing yet: an open or decent act, and the door has no call for one | cab_drive, fare, free_ride, chapel, asked_fire, beaten, patched, debt_forgive, good_word, rent_paid | 10 |
| Nothing: the real rules have a plain fact of their own for it, not behind the door | inherit (who he is), arrive (his arrival) | 2 |
| Nothing: never passed on in the prototype either | wash (private), noise (somebody heard, nobody seen), word (not an act) | 3 |

The rule behind the second and fourth rows. The door's sighting is always kept as a story about his hidden life (one_sim.cpp os_witness). That fits an act that reads badly, so the 27 kinds the prototype's own numbers read below nought are sightings. It does not fit a decent act: told as a sighting, a debt struck out would be kept quiet by Mickey's own people, and would raise suspicion in a listener of the day circle when it names him (Gossip.h KeepsHisDeeds and NamingReaches). So the 10 kinds that read nought or better have no home in the real town until the door has a call for an open act. The mill's own Witness already takes "not about his hidden life" (the game passes it for some stories), so that call is a change to the front door, not to the rules.

Three notes on single rows. The five crimes of violence (strike, weapon_out, weapon_used, kill, knocked) are sightings, so talk only (section 5). ran_police and bag_taken can only happen if the prototype keeps its own chase and its own constable (decision 4). And a sighting may not be named like one of the rules' own stories (the asks, an arrest, DS Ellis asking, the week's end, a threat, his name, his arrival): the bridge refuses those names.

What the real rounds pass on (read in run 3: Gossip.h Tick, lines 709 to 800, and TownRounds.h). Every six game minutes each person tells each person they are tied to, and are together with that hour, every story they hold, the surest first. A story is passed if it is sure enough (0.2 or more before and after the telling; each telling multiplies by the tie's weight and by 0.8), if the teller has not been silenced or held by a hook, and if it is news to the listener (stronger than what the listener already holds). Mickey's own people keep stories about his hidden life to themselves. Nothing is chosen by how newsworthy it is, and nobody is left out for having been part of the act. The prototype, by contrast, passes one story a telling, picked by heat times newsworthiness, never tells a person about an act they took part in or that was done to them, and keeps private kinds quiet (gossip.js lines 23 to 39).

Remarks to his face. In the prototype a person brings a story up to his face when its heat is high enough, picked by heat times newsworthiness, and a grudge of their own only after some time (gossip.js `comeback`, lines 118 to 151). Heat has no counterpart in the real rules (section 3). After the swap these remarks would have to be fed from `town.knows()` (how sure, how many tellings away), which is a design choice for step 4, or wait for the real rules' own street voice (StreetVoice, not behind the door).

For the player: after the swap the town learns of what he does badly in sight of others, and of nothing decent he does. A good deed (a debt struck out, a free ride, the rent paid) no longer travels unless the door gets the call for an open act first (decision 7).

## What was not measured, and why

- Seeing (section 4): no call on the front door for the real rule yet.
- The Ledger (section 8): read on both sides; nothing to run until the swap.
- The police on the prototype's side (section 5): its police.js loads only with the drawing library, which was not installed here. Read instead.
- A whole played week on both sides with a player in it: the prototype's player, fights and talk need the page. The prototype's own tests do this in a browser; they were not run here.
- The other 19 prototype people against the real cast's unnamed 32: no certain match to measure by.
- Whether the two sides would end the same week the same way (Sheila's answer, the endings): not compared.
- Section 10's table: checked for cover and for its one rule, not played. Which stories a real week ends up holding from a whole played week of the prototype's acts was not measured.
- Old saves (section 9): tried on a save written by hand in the prototype's shape, not on a save from a real older build.

## Decisions this list puts to him (none taken here)

1. Names: which of the prototype's 19 names go onto the real cast's unnamed people, and whether the five with no place in it stay (canon).
2. What each person thinks of him: stay the prototype's, fed from the town's facts (recommended), or wait for the real counterparts (section 6).
3. The week: five days as the prototype plays, or seven as the real rules run. The real rules refuse Sheila's question before Sunday, so five days needs the question's day made settable in the Core first. Recommended: five, as the earlier note argued, because it is the week that has been playtested; the cost is that change to the Core, which is the main session's.
4. The solicitor's bill and the chase: keep as the prototype's own, or drop to match the real arrest. The earlier note (V10) recommends the real arrest, with which the bill goes; it says nothing of the chase.

5. (run 3) Violence and the police. Through the bridge only the damage deed is reported. Either a call is added so that a blow, a weapon or a killing seen by a witness can be reported and he can be taken for it (over the front door's own report and arrest, held to the golden rows that exist for them), or the gap is accepted for the first swap: the town talks of his violence and DS Ellis may come, but nobody is taken for it. Recommended: accept it for the first swap and say so beside the page. The packaged game reports only the damage deed today as well (CrimeProbe.cpp makes one call to the deed and none to a report).
6. (run 3) Damage. The real week follows one deed, a thing damaged, and the prototype has no act that damages a thing. As the two stand, nothing he does in the prototype would bring a statement or a constable after the swap. Either the prototype gains the game's own deed (a window put in), or the cab put into something counts as damage, or decision 5's call is added, or the first swap goes out with a street that talks and a police that never comes. Recommended: the game's own deed in the prototype, with the swap or straight after it. It is new scope for the prototype, so it is his.
7. (run 3) Decent and open acts. Ten kinds have no home in the real town (section 10). Either the front door gets a call for an open act before the swap (recommended: it is small, and without it good deeds stop travelling), or the swap goes out without them.

The earlier note's three decisions (how long a game hour is, how far a story travels, each person's temperament) still stand beside these. M3 now gives the second one numbers.
