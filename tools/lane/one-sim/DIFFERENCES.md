# Where the prototype's own town differs from the real rules, and what the swap changes for the player (step 3b)

Task 4s, run 2, 19 November 2026. Nothing in the prototype's source was changed. The swap itself is step 4, a later round through the publish gate. Not yet seen by a fresh reviewer.

## What was compared, and how

- The prototype's side: its frozen JavaScript town as it stands in tools/lane/prototype/project/src (rules.js, cast.js, routines.js, seeing.js, gossip.js, events.js, ledger.js, police.js, state.js, clock.js). The readable source, read today. The earlier comparison (production/lane/PROTOTYPE-VS-DESIGN-2026-11-18.md, 18 rows) had to read a squeezed copy; its row numbers are given below as "V3", "V10" and so on, and its numbers were checked against the readable source wherever they are used here.
- The real side: the game's own town code as the browser copy runs it (one-sim.wasm), which gives the C# Core's answers on every row of the golden table. Numbers are from the port's own files, named each time.
- Measured where it could be: `tools/lane/one-sim/one-sim.sh differences` runs differences/measure.mjs, which loads the prototype's own rule files under Node, unchanged, beside the real town through the bridge, and asks both the same questions. Last run 17:11 UTC, 6 s. Three measurements, M1 to M3 below.
- Read, not measured, where no call exists yet to ask the real rule from JavaScript, or where the prototype's file needs the drawing library to load (police.js). Each such line says "read".

What stays the prototype's own after the swap, so is not compared: money, debts, jobs, fares, fights and talk, and its street (the map, walking, light, lines of sight, weather, the cab, the screens).

## The short answer

After the swap the player meets a larger, quieter, more regular street. More people (41, not 28), most of them without a name yet. People stand elsewhere than he remembers: of the nine people both casts hold, somebody who is out is in the same part of the street in both only about a third of the time. Everybody moves on the hour. A story about him reaches about as many people on its first day, then stops sooner: fewer of the people he knows by name will have heard it. It does not cool in a day. The police follow a fixed timetable, a day slower and two hours longer in the cells. And four things he has today have no counterpart behind the bridge yet: how well a witness sees or hears him by the real rule, what the street calls him, how much each person likes or fears him, and the moment of catching two people talking about him.

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

| End of | Prototype, of its 28 named | Real rules, of its 41 | Of the nine in both: prototype (middle), real |
|---|---|---|---|
| Monday | 0 | 0 | 0, 0 |
| Tuesday | 6 / 11 / 18 | 14 | 4, 5 |
| Wednesday | 23 / 24 / 25 | 22 | 8, 5 |
| Thursday | 23 / 24 / 25 | 23 | 8, 5 |
| Friday | 23 / 25 / 25 | 24 | 8, 5 |
| Saturday | 23 / 25 / 25 | 24 | 8, 5 |
| Sunday | 23 / 25 / 25 | 24 | 8, 5 |

On both sides every copy still names him at the week's end.

For the player: on the day itself the two towns are close (11 of 28 against 14 of 41 by Tuesday night). After that the prototype's story reaches nearly everybody with a name by Wednesday (24 or 25 of 28). The real one stops at 24 of 41, a little over half the street, and at 5 of the 9 people he knows best where the prototype reaches 8. So fewer familiar faces will bring a deed up, and more of the street stays ignorant of it. What the real town holds, it holds longer: the prototype's heat is half gone in a day, the real story's certainty lasts four. The prototype's "how loud his name is", which today brings DS Ellis (and, by the earlier note, Cammack's lads), is built on that heat and has no counterpart behind the bridge (section 6).

Limits of M3: one story, one witness, one seed of the real rules (they have only one), nobody watching him afterwards, and the prototype's passers-by left at their own behaviour. It measures reach, not what is said.

## 4. Seeing him, and knowing it was him (read, not measured)

| | Prototype (rules.js, seeing.js) | Real rules (the port's Perception.h) |
|---|---|---|
| How far | 4 m in the dark up to 48 m in full light, less in rain (by up to 30%) and in mist at night (22%); 14 m at least indoors; 34 m for a cab with its lamps on | Fixed distances: a shape at 35 m, a mark at 18, a face at 8; recognised at 25 m, but only by somebody who knows him |
| Which way they look | About 124 degrees, and wider for anybody within 3 m | 120 degrees, with a sharp middle of 60 and a rule of its own for a man standing still (V12) |
| How well | One number for clarity; with it a "face score" | Five rungs: someone, a silhouette, a mark, a face, recognised |
| Is it him | Named above a face score of 0.36 if they know who he is (familiarity over 0.5, or they know of the inheritance); else "a man", "a coat", "a cab" | The top rung, for those whose familiarity with him is 0.35 or more |
| Hearing him | A distance for what he is doing (standing, walking, running, the cab), larger in the small hours and smaller in rain and through a window; somebody who only hears a loud act remembers "a man" (seeing.js) | Loudness set against the street's own noise at that hour, and less through a wall (Perception.h). Not behind the bridge either. |

The real rule's rows pass in the browser copy (T1), but JavaScript cannot ask it yet: the bridge takes "how well" from the caller. So this difference is the main thing still to build for the swap, and it was not measured. For the player it will change who can name him and from how far. The light map and the rain stay the prototype's.

## 5. The police (read; the real side also from the scripted weeks)

| | Prototype (rules.js police, cast.js) | Real rules (the port's PoliceFile.h, TownWeek.h) |
|---|---|---|
| Who gives a statement | A witness who saw it, names him, is sure (0.55 or more), not afraid (under 0.5) and does not like him much (V8's reading; the numbers checked in rules.js today). Ten people never do: Sheila, Ron, Darren, Rita, Wayne, Lee, Hal, Dennis and the two police. | Seeing him do it is enough, unless they are on his side, have been talked round, or are on the cast file's never list. At nine the morning after. |
| When they come for him | The next day at nine; a constable walks down Quay Street to him, and he can run | At ten o'clock; in both scripted weeks that hold a deed, the morning after the statement. He is taken where he stands. |
| In the cells | 4 game hours; 5 for violence; 2 more if he ran. He is billed 25.00, or 40.00 if he ran. | Damage 6 hours, or 2 and a caution if he owns up; a wounding 8; a robbery 12; otherwise 22. Then charged, or bailed. No bill. |
| DS Ellis | On Thursday or Friday between ten and one, when his name is loud enough (2.2); asks up to five people | At nine, from the second day, whenever the rules find a reason (the street's talk of him is one, a body another) |

The real side, as the scripted weeks play it (the C# Core's own rows): a window put in on Tuesday at half past twelve with Darren watching. Three people find it at five that afternoon and one more at eight the next morning. Darren goes to the police on Wednesday at nine. DS Ellis comes on Thursday at nine, for the talk. A constable takes him on Thursday at ten, and he is charged.

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

## 9. Saves (read and tested)

The prototype's save holds its own town: each person's mind, every event, who told whom (saving.js). After the swap it holds the town object the bridge hands it (BRIDGE.md). A save from before the swap has no town in it. For the player: a week saved before the swap cannot be continued after it. The prototype's save version must go up, so that such a save is not offered.

## What was not measured, and why

- Seeing (section 4): no call on the front door for the real rule yet.
- The Ledger (section 8): read on both sides; nothing to run until the swap.
- The police on the prototype's side (section 5): its police.js loads only with the drawing library, which was not installed here. Read instead.
- A whole played week on both sides with a player in it: the prototype's player, fights and talk need the page. The prototype's own tests do this in a browser; they were not run here.
- The other 19 prototype people against the real cast's unnamed 32: no certain match to measure by.
- Whether the two sides would end the same week the same way (Sheila's answer, the endings): not compared.

## Decisions this list puts to him (none taken here)

1. Names: which of the prototype's 19 names go onto the real cast's unnamed people, and whether the five with no place in it stay (canon).
2. What each person thinks of him: stay the prototype's, fed from the town's facts (recommended), or wait for the real counterparts (section 6).
3. The week: five days as the prototype plays, or seven as the real rules run. The real rules refuse Sheila's question before Sunday, so five days needs the question's day made settable in the Core first. Recommended: five, as the earlier note argued, because it is the week that has been playtested; the cost is that change to the Core, which is the main session's.
4. The solicitor's bill and the chase: keep as the prototype's own, or drop to match the real arrest. The earlier note (V10) recommends the real arrest, with which the bill goes; it says nothing of the chase.

The earlier note's three decisions (how long a game hour is, how far a story travels, each person's temperament) still stand beside these. M3 now gives the second one numbers.
