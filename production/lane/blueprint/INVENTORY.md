# INVENTORY: everything the game needs made, counted

Blueprint preparation item (c), 23 Nov 2026, blueprint preparation session (Opus 5.5). Counts for the browser game the one-shot builds (the whole design, his clock of 60 s a game hour, about 7 game weeks, 15 to 20 hours of play). "In the prototype" was counted from tools/lane/prototype/project/src on 23 Nov (a Sonnet helper parsed the data with scripts; method per row in its notes). "Needed" comes from the design's own figures; where the design gives none, the row says how the number was reached.

Sources: ONE-SHOT-PROMPT.md (sections 1, 4, 5, 13 to 17, 25, 29, 31 to 39), DEFINITIONS-2026-11-21.md (L-01, G6, G7, F15, P34, RT2-08, RT2-10, RT2-14, RT2-16, RT2-19, P45), FIT-CHECK-2026-11-21.md (F16, F19, F20, scope question 4), RULINGS.md on wip (street lines 30 Sep; clock 21 Nov), canon.md (no children, content rule), NUMBERS-RUN.md (repeat fixes P1 to P4), SOUND-PLAN.md (sound count), first one-shot pace from ONE-SHOT-LOG.md.

## 1. The budget

About 45 Fable-builder hours in the one-shot's week (premortem way 7). The first one-shot passed 6 of 41 stories in about 7.5 hours, 45 to 55 minutes a story early on, building the systems as it went. At that pace the 41 stories alone take about 34 hours, and TECH-PLAN's plumbing hour and the gate take about 4 more. That leaves about 7 hours for content. Content that would cost more than that has to arrive ready as data (TECH-PLAN section 3) before 7 Dec.

How hours were estimated: loading and wiring ready data is about 0.5 hours per kind of record plus a check run (one-shot ONE-SHOT-LOG shows a story's check-and-fix loop at about an hour); writing content inside the one-shot is taken at about 400 checked lines an hour (writing, tagging each line's situation and cool-down, the content-rule and period check, and fixing what the check finds). Both are estimates; the first is from the log's pace, the second is a judgement and should be measured on the first make-ahead batch.

## 2. The count

| Thing | Needed | In the prototype | How it is made | One-shot hours if ready ahead | One-shot hours if made in it |
|---|---|---|---|---|---|
| Principals (named, with card, look, schedule, ties) | 13 plus Tom | 8 on the map, 4 rival heads as names only | written (cards), looks from the look tables, schedules from the casting sheet | 0.5 | 3 |
| Firm's people (Pauline, Kevin, Terry) | 3 | 3 | written | in the row above | 0.5 |
| Regulars (the thirty, ruling of 30 Sep) | 30 | 16 | written; debtors and crew among them | 0.5 | 5 |
| Minor named people (trainer, car-lot man, two constables, retired doctor, other firm's owner, inspector, landlord's agent, cold-store shift manager, deckhand, caff owner, two bought officers, glazier) | 14 | 1 (PC Ibbotson) | written | 0.3 | 2 |
| Rival men (a lieutenant and three men for each of three rivals, RT2-08) | 12 | 3 unnamed lads | written, with routines | 0.3 | 2 |
| Fare people (G7: at least 40, two rides each) | 40 people, 80 rides | 14 rides (7 named) | written | 0.5 | 4 |
| Passers-by: distinct bodies on the street at once | 25 to 35 at the busiest hour (G9), about 60 distinct looks over a day | 16 walkers plus 13 others, looks rolled from 11 male and 9 female tops | generated from the prototype's look tables, adults only (canon) | 1 (tables grow) | 1 |
| Kept extras (a passer-by who saw a deed gets face, coat, home, routine, RT2-10) | about 10 to 20 in a playthrough | 0 | generated at run time | in systems | in systems |
| Own street lines, the 12 most-seen (L-01) | 12 x 60 = 720 | about 150 among Ron, Darren, Ada, Sheila and others | written | 0.5 | 1.8 |
| Own street lines, everyone else named and talking (L-01: 30 each) | about 59 people x 30 = 1,770 | about 120 | written | 0.5 | 4.4 |
| Shared street lines, by situation (NUMBERS-RUN P3) | about 400: 120 everyday, 40 weather, about 24 for each of about 8 common situations, 6 for each rare one | 56 shared plus 36 barks | written | 0.3 | 1 |
| Fare talk (two rides a fare person, about 3 lines a ride) | about 240 | 24 | written | in fares | 0.6 |
| Scene lines (staged first hour, Act I asks, 8 Act II beats, 5 Act III mornings, the rival scenes, endings, arrest, hospital, count variants, licence hearing) | about 60 scenes, about 1,500 lines | 16 scenes in scenes.js and about 35 in game/, about 400 lines | written | 1 | 5 |
| Side stories (F15: about 25, 22 to 28, 3 to 5 steps, about 12 minutes each) | 25, about 30 lines each = 750 | 4 | written as job graphs | 0.5 | 3 |
| Street happenings (G6 at least 60 over 8 kinds; NUMBERS-RUN P1: 80 for a 20-hour player) | 80, about 8 lines each = 640 | 6 | written | 0.5 | 2.5 |
| Jobs (carries, collections, break-ins, lifts, tails, minding, sit-downs, the 8 sending verbs; each a graph with three keys to every lock) | about 40 authored jobs, at least 10 break-in sites (P34), at least 2 for each Act II place (RT-03) | 2 night jobs plus 11 templates | written as data graphs; steps reuse the systems' verbs | 1 | 5 |
| Debts (OSP s25) | 5 debtors, each with 3 keys (Iveson) or a manner | 5 in the book | written | in jobs | in jobs |
| Ledger texts (each kind of act the town can know: truth and Tom's own wording) | about 150 kinds | 111 | written | 0.3 | 0.5 |
| Letters and notes (opening letter, rent arrears, notice to quit, solicitor's letter, licence hearing, customs inspection, the Act III VAT letter, notes left at the office, answering-machine messages) | about 15 letters, about 20 notes and messages | 3 letters | written | 0.3 | 0.5 |
| The paper (twice a week for 7 weeks, about 5 headlines and one short story each) | 14 issues, about 70 headlines | 5 headlines | written; most headlines follow the town's deeds by template | 0.3 | 0.5 |
| Named places (PLACE_LIST) | about 45, of them about 19 in the story (F16) | 45 in game/tune/way.js | from the prototype | 0 | 0 |
| The road plan (G1: about 620 by 400 m, quay road 540 m, Quay Street 48 m with its climb, north road 338 m, Chapel Lane 240 m, cold-store road 380 m, dock road 350 m, Basin Road 353 m, warehouse row 350 m, foot-only cuts, 6 vault places) | 1 map | partial: 233 walking nodes, 57 buildings, 14 zones; docks and the full loop not at G1's lengths | built in map.js data (geometry and walking graph) | 2 | 8 |
| Enterable rooms (P34: at least 24; 8 named places with back rooms and upstairs, at least 14 rooms; at least 10 break-in rooms, each entered three ways; each with a usable object) | 24 or more | 17 | built from room kits in map.js | 1 | 5 |
| Phone boxes (RT2-19) | 3 | not counted | from the prototype's props | 0.1 | 0.2 |
| Cars: firm cars 2 rising to 5, the other firm's 2, the patrol car, traffic (all fictional, automatic) | about 6 body kinds | the cab and traffic | from the prototype kit (tools/lane car kits) | 0.3 | 2 |
| Clothes: three outfits for Tom plus a dark night coat (OSP s32) | 4 | outfit system exists | from the prototype's tailor | 0.2 | 0.5 |
| Animals (P45: gulls, pigeons, a few cats, yard dogs, one dog loose; never hurt) | 5 kinds | gulls by sound only | generated (simple figures, sound) | 0.5 | 1.5 |
| Sounds (SOUND-PLAN.md section 4) | 118 sound kinds | 17 named effects, 4 loops, a score | browser synthesis now (no files) | 1 | 4 |
| Live talk sheets (cards for live talk, written fallback lines above) | one per talking named person, about 72 | 28 cards | written | in people | in people |

Totals:
- People: about 112 named or written (14 principals and firm with Tom, 30 regulars, 14 minor, 12 rival men, 40 fare people, a few overlapping), plus generated passers-by. The FIT count of 35 to 48 named people did not include fare people, rival men or the minor people the design added since.
- Lines: about 6,000 written lines (720 + 1,770 + 400 + 240 + 1,500 + 750 + 640), plus about 150 Ledger texts, 35 letters and notes, 70 headlines. The prototype has about 650 to 800.
- Hours if everything is ready ahead: about 13.5 (sum of the column). Hours if made inside the one-shot: about 64, which with the 34 hours of stories is more than twice the week.
- Even ready ahead, 34 (stories) + 4 (plumbing and gate) + 13.5 (wiring content) is about 52 hours against about 45. The week fits only if stories go faster than last time: at 40 minutes a story (the plumbing, the fixed step and the data folder exist to make that possible) they take about 27 hours and the total is about 45. If the first day's pace is slower than 40 minutes a story, the ruled cut applies: the docks go first (his ruling of 28 Oct).

## 3. What does not fit

1. Writing the lines inside the one-shot. About 6,000 lines at about 400 an hour is about 15 hours alone, twice the 7 hours left. They must be written ahead.
2. The full map at G1's lengths and the 24 rooms (about 13 hours if built inside). The chase loop (1,528 m) and the docks depend on it.
3. Everything together: about 64 hours inside against about 7 free. Even with the stories done faster than last time, content cannot be made inside the week.
4. Voiced lines are not in this count: the browser game speaks in subtitles with a tone per speaker (audio.js `voice`). Voices belong to the builder's pipeline for the Unreal game and are not one-shot work.

## 4. What to make ahead (before 7 Dec)

In order of what blocks most stories:

1. People files for all about 112 (cards, looks, schedules, ties, kind, `can_die`), in TECH-PLAN's people format. Owner: the town and story work (casting sheets exist for the 41 in hook-cast.json; the rest are written from DEFINITIONS and the story pick). About 1 cloud day.
2. The line tables: 720 + 1,770 own lines, about 400 shared lines by situation, each line a record with situation and cool-down; checked against the content rule (no alcohol, no gambling, no children, period words for 1990) by a fresh checker. About 2 cloud days with checks.
3. The map at G1's lengths with the walking graph, the docks and the 24 rooms. About 1 to 2 cloud days; the prototype's map.js is the start.
4. 80 happenings, 40 fare people and their 80 rides, 25 side stories, about 40 jobs, all as data graphs with `src` fields. About 2 cloud days.
5. Scenes: the staged first hour already exists; the 8 Act II beats and 5 Act III mornings wait on the story pick (STORY-FINAL did not reach the bar; story v3 is running), so these are the last to be made and the riskiest. If the story is not picked by about 2 Dec, the one-shot builds Act II's systems with placeholder beat text marked as such, and the beats arrive as data later.
6. Letters, notes, the paper's 14 issues, Ledger texts. Half a day.
7. Sound recipes (SOUND-PLAN.md's list as synthesis settings). Half a day.

Each batch is checked by a fresh reviewer against its design rows before it lands, and counted by the data check of TECH-PLAN section 8 (every record has a `src`; counts compared with this file).
