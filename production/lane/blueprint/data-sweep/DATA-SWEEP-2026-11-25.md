# Blueprint data sweep, 24 to 25 November 2026

Job: find every blueprint part whose content the one-shot must build exactly but which the blueprint gives only in words (class B), or whose data exists in the project without the blueprint pointing to it (class C), and group them into the data files the one-shot needs, in the order the keeper should make them. One pass, by the data-sweep job (Opus 5.5, five Sonnet readers, one fresh Opus reviewer), on lane-2026-11 at 0f900ad9.

Files beside this one: DATA-SWEEP.csv (one row a part: class, data file, fields, size, source, maker, effort, stale clock, depends_on, note, and any class changed by the check), REVIEW-40.csv (the reviewer's blind classes), SUMMARY.md.

## 1. The count

The chapters hold 437 entries, not 424: the status file's 424 predates 8.11 (three parts), 8.12 (three) and 9.13 (three) added in keeper run 2, and 5.11.1 to 5.11.4 are four reference entries with no status line. All 437 are in the CSV.

| Class | Meaning | Parts |
|---|---|---|
| A | buildable exactly from the part as written | 162 |
| B | words only where data is needed | 84 |
| C | data exists in the project, the part does not point to it | 84 |
| D | needs no data (process, test, machinery, shipping, out, Unreal-only, reference) | 107 |

So 168 parts (38%) would leave the one-shot guessing today. Half of those (the C parts) need only a keeper's conversion and a path; the other half need the data made.

A-class parts can still lean on a set another file makes (a rule "for every person's routine" is exact, but the routines are made elsewhere). The depends_on column names that file, so the keeper can see which exact rules are waiting on which data.

## 2. The independent check

A fresh Opus reviewer classified 40 parts drawn at random (seed 20261124), blind to the readers' classes.

- Exact agreement: 29 of 40 (73%).
- Agreement on what matters, whether the part needs a data file (B or C) or not (A or D): 36 of 40 (90%).

The pattern of the errors, and the fix:
1. A against D (3 of the 11): the brief let a fully stated game rule be D; the reviewer called it A. Both mean no data file. Fixed across the whole sheet: every D whose status is a game status (decided, ruled, pending, unmeasured, sourced, measured) and whose note is not a test, process or shipping matter became A (54 parts moved, all marked in the changed column).
2. The rule over an unlisted set (3 of the 11, the only errors that change the work): CLK-03 (every routine within walking reach of the next place), 1.7.3 (the board and the ranks), 6.1.1 (every usable object's prompt) were D but need a list. All three now C. Across the sheet the same shape is handled by depends_on; a keyword scan of the remaining A and D parts found 31 more of that shape, all leaning on files already in the list below (routines, places, rooms, vehicles), so no new file was needed.
3. B against C where a file holds part of the data (4 of the 11: 7.16, 1.6.8, RT-10, 3.1.1): both mean data must be made; the reviewer's call was taken.
4. RT2-17 (B to A): the two police stop points resolve from the G1 road table.

All 11 disagreements were settled to the reviewer's class. The reviewer's other findings, kept below: the prototype's positions are on a different plan from G1 and cannot be lifted as they are; several C sources disagree with the part (prototype boxing hall 17:00 to 22:00 against 18:00 to 21:30; launderette closing 20:00 against 23:00; hook-cast.json's older placeholder ids against canon's 44 people), so C means "reconcile and point", not only "point".

## 3. The data files the one-shot needs, in priority order

Order is by how badly a guess would hurt: a file other files hang positions or people on comes first; a file that waits on the story pick comes last. Hours are the readers' rough estimates for the keeper, summed from the CSV (shared parts split evenly); they are estimates, not measured, and the line tables are probably low.

| # | File | Format and fields | B | C | Parts | Source to start from | Maker | Hours |
|---|---|---|---|---|---|---|---|---|
| 1 | map.json plus map-topdown.svg (already asked of the keeper) | JSON in metres, origin at the ferry landing as G1: roads (id, name, centre line points, width, pavements, kerb), plots (id, outline, building, storeys, use), doors (id, plot, x, y, facing, number, street, locked), street name plates, lamp columns, quay ladders and bollards, the six vault places with heights, street-as-weapon points, phone boxes (3), cab ranks (2), police stop points and posts, rival bases (3), props at Study 4's 5 per 10 m; the walking graph. The SVG drawn from the JSON, never by hand | 9 | 6 | 1.1.8, 1.3.5, 1.6.1, RT2-19, RT2-08, 4.1.1, 4.1.2, 4.1.3, FIT-G1, 4.2.1 to 4.2.4, 4.4, OUT-08 | DEFINITIONS-2026-11-21 G1 (13 roads, end points, widths, features by distance: the only G1 data); production/specs/terrace-fronts.md, vignette-scene.json, vignette-pieces.json (Quay Street, street-local metres); production/art/atlas-01/data/atlas.json (the older adopted plan: 38 blocks, 12 landmarks); prototype map.js (a different, older plan, about 15 to 20% of G1, not reusable as is) | design (plots, doors), keeper (roads, Quay Street) | 46 |
| 2 | rooms.json | per room: id, door, plot, floor, outline, furniture and objects (id, kind, x, y, prompt id), containers (contents per job, search time), locks (key holder, ways in: three per break-in room), states by rung (Mickey's office) | 8 | 3 | GV-01, 1.6.2, 2.12.5, 3.5.3, 4.3.1, 4.3.2, 4.3.4, 4.3.5, 4.3.6, FIT-P34, 7.16 | production/specs/mickeys-office.json, shop-interiors.json; prototype map.js ROOMS (17); production/cloud-week/town/HOMES.md. Missing outright: the ten break-in rooms, three rival bases, Iveson's hut, the chapel hall and priest's house, the boxing hall, the doctor's terrace | design | 31 |
| 3 | people/ (one file a person, TECH-PLAN section 3) plus ties.json | id, cast_id, name, age, kind, look, temperament (nerve, dutiful, willingness, keepsQuiet), card, voice, can_die; one tie list for the cast | 9 | 7 | 1.3.12, RT2-13, 2.5.3, 2.6.8, 2.8.1, 2.10.2, 2.10.4, 2.11.1, 2.12.3, 2.14, 2.15.1, 2.15.3, RT2-05, 3.2.1, 3.2.2, 3.2.3 | production/specs/hook-cast.json (41 sheets, older ids), production/cloud-week/town/people.json (44 people, 1,162 facts, 27 secrets, 220 rumours), game-design/town-traits-draft-2026-09-29.md (temper figures for 41). Missing: the rivals' three lieutenants and nine men, two bought officers, the other minicab firm's owner, the cold-store deputy, the dock gun seller, the landlord's agent, the car-lot man, the stitching doctor, five fighter kinds' capacities. INVENTORY puts the total at about 115 | keeper (from cast), design (the missing roles) | 32 |
| 4 | routines.json | per person: rows of [from game time, place id, act, days], with the 200 m walking-reach rule checked on the 120 s hour; the cleaner at six, the first dock worker and every finder named by 2.5.5 | 0 | 2 | 2.1.1, CLK-03 (plus about 30 A parts that lean on it: casing, sends, traces, crew signs) | hook-cast.json routines; prototype cast.js sched rows | keeper | 6 (low: about 115 people) |
| 5 | places.json plus timetables.json | places: id, name, kind, plot or door, owner, opening hours by day, label text, district at the edge (six by landmark); timetables: shop hours, shifts, the ferry, the market Thursday, match Saturday, 5 Nov, 11 Nov, Christmas, the rounds' days | 6 | 7 | RT2-14, 1.6.15, 1.7.3, 2.2.6, 2.15.2, 2.17, 4.1.4, 4.3.3, 6.9, 7.16, 2.1.6, FIT-G10, RT2-09 | prototype game/way.js PLACE_LIST (45 places, older plan positions); DEFINITIONS G3, G10; production/research/shop-hours-1990/; shop-interiors.json. Reconcile hours that disagree | keeper, design (labels, door numbers) | 23 |
| 6 | tune.json (one table, every number once, on the new clock) | key, value, unit, source row; realSecondsPerGameHour 120; every real-time figure derived from the old 60 s (or the prototype's 45 s) recomputed | 7 | 15 | 1.1.1, 1.1.2, 1.1.6, 1.2.1, 1.2.4, 1.3.8, 1.3.10, 1.3.11, RT-10, RT-11, 1.4.3, 1.4.4, 2.1.5, 2.2.4, 2.4.2, 2.5.2, 2.5.4, 4.5.1, 5.8.1, 6.1.5, RT-04, 9.6 | prototype rules.js and game/tune/*.js (2,415 numbers, still at 45 s); production/specs/camera.json; FEEL-TARGETS-DRIVING-2026-11-17; TRAFFIC-STAGE1 reference model; weapons-spec.md. Missing: firearm hit chance and timings (footage), crowd step-aside distances (footage), sound reach for acts beyond six, report strengths | keeper; research for the footage numbers | 30 |
| 7 | police.json | the beat constable's route (waypoints on map.json, times), the patrol car's route, stop points, posts, stages and their signs, response time per deed, search rules | 6 | 0 | 2.6.1, 2.6.5, 2.6.6, 2.6.7, 2.6.10, FIT-G5 | prototype police.js and game/law.js; KERBSIDE-RULES-1990. Needs map.json first | design | 10 |
| 8 | crowd.json | passers-by count by place and hour (the parade front's bands exist; every other street does not), a spawn rule per camera frame (4 to 10 at busy bands), the 1990 look tables for adults, repeat distance | 4 | 1 | 2.1.2, FIT-G9, 3.2.4, 5.1.5, GD-02 | production/specs/street-people.json; DEFINITIONS G9; the measuring lane's crowd counts (24 Nov: 5 to 10 in busy views, 0 to 3 quiet). The 1990 pavement study (CLOUD-FIGURES B4) is owed | design, research | 15 |
| 9 | vehicles.json | firm cars by rung (make, colour, plate), the other firm's two, the patrol car, traffic kinds, the car lot's stock, the boot's slots and contents | (in people and rooms rows) | | 2.15.1, GV-01, 1.2.9, GV-02 (depends_on) | production/specs/street-vehicles.json, mickeys-office.json | keeper, design | about 4 (not summed in the CSV) |
| 10 | lines/ (records by TECH-PLAN section 3) | id, who or speaker kind, situation, text, once; own lines for the 12 most seen (60 each) and about 57 others (30 each); landmark direction lines for chases and the way; the shared bank converted | 3 | 7 | GV-03, 2.4.3, 2.12.4, 3.6.3, 3.6.4, 3.6.5, 3.6.6, FIT-L01, 6.7, 7.7 | production/cloud-week/lines/lines.json (1,626 lines, own lines only for Ron, Darren, Walsh, June); production/specs/suggested-lines.json; prototype talk_lines.js. About 2,000 own lines missing (INVENTORY: about 5,300 lines in all still to write) | design | 28 (low) |
| 11 | jobs/, fares.json, happenings.json, side-stories/ | job graphs (steps, place, verb, three keys, fail); 40 fare people and 80 rides; 60 to 80 happenings over 8 kinds; 25 side stories with step lines; rivals' pressures and harms with places | 10 | 4 | 3.5.1, 3.5.2, 3.5.4, GD-08, RT-03, 3.4.1, FIT-G7, 2.10.3, RT-06, 3.7, FIT-G6, 7.4, 7.14, 3.3 | prototype jobs.js (7 templates), fares.js (14 rides), scenes.js (6 happenings); game-design/side-stories-2026-11-08.md (32 drafts); game-design/counterparty-purses-spec.md | design | 78 |
| 12 | ledger-texts.json | per kind of act: truth wording and Tom's wording; slot texts; step entries; the sign list | 0 | 5 | 6.1.3, 6.2.1, 6.2.2, 6.2.3, 6.2.5 | prototype ledger.js, game/ledgerx.js (111 kinds), ledger_screen.js | keeper | 8 |
| 13 | letters-and-print.json | letters and notes (solicitor, VAT, notice to quit, licence hearing, office notes), the paper (14 issues, the paper's name), poster and sign texts, the six owed brand names | 1 | 2 | 2.4.5, 4.9, 6.10 | production/specs/town-news.json, brand-bible-v1.md; production/cloud-week/2d/paper and 2d/fascias | keeper, design | 8 |
| 14 | ui-text.json plus content-words.json | prompts for every usable object, menus, save slots, hints, keys and pad map, subtitles' unit, the AI notice and privacy wording, one line per accessibility option, the sound-cue word table, credits; the content word list | 4 | 8 | 1.6.8, 3.6.7, 6.1.1, 6.1.2, 6.4, 6.5, 6.6, 10.4, 10.11, 8.4.1, AX-08, 8.8 | prototype ui.js, player.js, talk.js (BANNED); production/handovers/6y-hints.md; production/specs/credits.json; ledger/Assets/Scripts/Core/ContentWords.cs; content/rules/slurs-v1.json; PRIVACY-CHECK-2026-11-21 | keeper, research (privacy wording at build date) | 13 |
| 15 | paper-map.svg | the hand-drawn paper map, gated to what Tom knows, drawn from map.json | 0 | 1 | 6.3 (and 4.1.3) | map.json once made; prototype map view | design | 4 |
| 16 | light-weather.json | per hour exposure and colour, the night brightness floor, weather profiles with weights and effects, wet-road drying, the colour grade | 2 | 5 | 2.1.4, 4.7, 4.8, 5.3.3, 5.4.1, 5.4.2, 5.4.3 | production/lane/LIGHT-WEATHER-VALUES-2026-11-17.md; prototype light.js (on the old clock: the dark part is now about 28 of 48 real minutes). The grade itself is written nowhere | keeper, design | 11 |
| 17 | sounds.json | the sound list with files or synthesis recipes, surfaces and gaits, hour states and caps, reverb for the eight room kinds, the radio (tune list, programme, presenter lines, the pirate station's name) | 2 | 3 | 5.5.1, 5.5.2, 5.5.3, 5.5.4, 5.7.1 | production/cloud-week/sound/manifest.json (97 files); SOUND-PLAN.md | keeper, design | 10 |
| 18 | scenes/ (last: waits on the story pick) | id, when (a state, never a clock time alone), who, where, beats; the first hour; Act I's week; Act II's beats; Act III's mornings; the landing nights; comic scenes and an evening's light moment; the close per ending | 5 | 7 | 2.9.1, 3.1.1, 3.1.2, 3.1.3, 3.1.6, RT-02, 3.2.7, 3.5.5, 5.8.2, 7.1, GD-05, 7.15 | prototype hour1.js, acts.js, rivals.js, endings.js; production/cloud-week/first-30-minutes/DRAFT.md; production/lane/story/ (the frame being made); game-design/warehouse-fire-2026-09-29.md | design (story lane), keeper | 44 |
| 19 | schemas.json | the record formats of every file above, so the data check can test them | 0 | 1 | 9.13.2 | TECH-PLAN.md section 3 | keeper | 2 |
| - | economy (separate job; not to be duplicated) | prices, wages, fares, purses, fence rates, money curve | 8 | 1 | 1.6.3, 1.6.10, 2.7.3, 2.7.5, 2.7.6, 2.7.8, GD-07, FIT-G8, FIT-F24 | production/lane/blueprint/economy/ (due Thu 26 Nov) | the economy job | - |

Nineteen files (some of them folders of records), about 400 keeper hours at the readers' estimates, of which map, rooms, people, routines and places (the first five) are about 140 and hold the positions and people everything else names.

## 4. Built on the map file already asked for

The keeper is already asked for the map in metres plus a top-down drawing. This sweep widens it: the same file must carry every door with its number and street, the street name plates at every end (Marcellus SC, his ruling of 30 Sep), the six vault places with heights, ladders and bollards along the 540 m quay, the three phone boxes, the two ranks, police stop points and posts, the three rival bases and the props, because 15 parts and about 30 exact rules point at those places. Rooms, places, routines, police routes and the paper map are all keyed to its door and plot ids, so it is made first and its ids frozen before the others start. The prototype's map.js is a different plan (Quay Street drawn 252 m long against the built 48 m; quay road 288 m against 540 m) and should be mined for room contents and props, not positions.

## 5. Referred to by the blueprint but held by no file

1. Plots, doors, door numbers and rooms for any street except Quay Street; any top-down drawing of the G1 plan (the atlas drawings are on F: and are of the older plan).
2. The six vault places' positions and heights (1.1.8, OUT-08); ladders and bollards along the quay (4.2.1, 4.2.4).
3. The ten break-in rooms, the three rival bases, Iveson's hut, the chapel hall, the priest's house, the boxing hall and the doctor's terrace (FIT-P34, 4.3.5, 4.3.6, 7.16, 4.3.4).
4. A lock and key table for any room (1.6.1, 3.5.3).
5. The rivals' lieutenants and men, two bought officers, the other firm's owner and four minor roles (2.10.2, 2.6.8, 2.15.3, RT2-05); the stitching doctor (1.3.11).
6. The beat constable's and the patrol car's routes (2.6.1, 2.6.7).
7. Passer-by counts for any place but the parade front and the fish dock; the 1990 pavement study (CLOUD-FIGURES B4).
8. About 2,000 own street lines; the landmark direction lines for chases (GV-03); 40 fare people and 80 rides; 60 to 80 happenings; about 40 authored jobs.
9. The colour grade (5.4.3), reverb values for eight room kinds (5.5.4), the radio's tunes, programme and presenter lines, and the pirate station's name (5.7.1).
10. Six brand names and the poll-tax poster texts (4.9); the paper's name (2.4.5).
11. Wording for the AI notice and privacy page (3.6.7, 10.11), one line per accessibility option (AX-08), the sound-cue word table (8.4.1), keys beyond the nine named (6.6).
12. Firearm hit chance and timings, crowd step-aside distances (footage not yet measured).
13. The 300-line red-team set for RT-15 (not confirmed in ledger/LineTest); ONE-SHOT-PORTING.md, which 9.4 names but which the part says is still to be written; the watermark method for generated speech (8.12.3).
14. The five new names in Mickey's real book and the envelope contents for Act I nights five and seven (RT-02, 3.1.6).

## 6. Parts on the old clock (stale)

A game day is now 48 real minutes (2 real seconds a game minute, 120 a game hour). These 34 parts state or rest on 60 s a game hour (24-minute days), or on the prototype's 45 s: FIT-G3, 2.1.1, 2.4.2, 2.4.4, 2.6.5, 3.1.1, 3.1.2, 3.1.3, 3.4.2, RT-19, 4.7, 6.1.5, 7.1, 7.2, 7.3, 7.4, RT-04, FIT-F13, FIT-F15, FIT-F16, 7.11, 7.13, CLK-01 to CLK-07, RT2-21, 8.11.2, 9.6, 9.13.1, 9.13.3. The CSV's note column gives the old and new figure where the readers worked it out (for example CLK-02's hurry: 90 real seconds becomes 180; the evening 6 real minutes becomes 12; Act II's five weeks need re-checking against the play-time target, since each week now takes twice the real time). INVENTORY.md and TECH-PLAN.md are also written on the 60 s hour. The tuning table (9.6) still holds 45.

## 7. Parts against the PEGI 18 and fights decisions

RT2-11 (the camera turns away; no kick or finisher animation), 1.3.5 ("nothing shown at length", "no finisher shown at length"), 5.9 ("light gore at most", "never a beating at length"), 10.2 (a PEGI 16 target, naming a blow on a downed man as what pushes to 18) and 5.2.2 (reads as if the downed-man limits were unset) contradict the 24 Nov decisions: PEGI 18, fights fully animated including a blow on a man who is down. The chapters are not edited here; the keeper should fold the decisions in.

## 8. Limits of this pass

One pass, as asked. The readers checked the project's files by search, not by reading each in full, so a C call says the data is there in substance; how complete it is was spot-checked by the reviewer (who found several partial or disagreeing). The hours are the readers' estimates. The CSV is the record; this page is its grouping.
