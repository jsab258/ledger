# Results of the checks

## 18 November 2026, lane round 5 (talk that does not repeat; a debtor who stands): the AI playtester before and after

Checks (test/talk5.mjs, all pass): Ron's own dock line once a day across talks and again the next day; a shared
line said on the Hook is not repeated there for a week but is free over the bridge on Copper Row; a week of
talks with ten people on the Hook hears no shared line twice; asked about tea, Brenda answers about tea and Ron
in his own words; asked about Sunday, Ron answers the question, not with his dock line; Grace and the priest
never name themselves; the detective never claims a lifetime on the street; agreeing replies still come day
after day; the memory is saved with the story. Lee, fronted up, stands at the threat saying Cammack's lot are
behind him and it comes to blows at the shove; without the backing he gives way at the threat. The seeded week:
with the new memory set aside, the save is the same as round 4's part for part (new record written).

AI playtester, newcomer's first hour (round 4, then round 5; one run each; three runs of round 5's builds during
the round gave a longest stretch of 9.1, 12.0 and 10.8 min, so the noise is about 3 min):

| measure | round 4 | round 5 |
|---|---|---|
| waiting | 39% | 41% |
| walking | 29% | 26% |
| talking | 24% | 25% |
| driving | 6% | 5% |
| kinds of activity | 6 | 7 (fighting) |
| new things, minutes 0 to 30 / 30 to 60 | 71 / 6 | 69 / 14 |
| longest stretch with nothing new | 7.9 min | 10.8 min |
| tense moments per 30 minutes | 18.0 | 19.5 |
| fights, pursuits, escapes | 0, 0, 0 | 1, 0, 0 |
| lines heard more than once in the hour's talks | 11 (the weather from four people) | 4 (sign-offs and greetings only) |

Lee stood and it came to blows in the first half hour (21 min). The sweep's one prompt fault (a lad and Darren at
night, as round 4) and one words-on-screen overlap (the to-do over the Noted note, seen in rounds 3 and 4) are not
new. Live AI talk is untested here.

## 18 November 2026, lane round 4 (a debt that can come to blows): the drills and the AI playtester before and after

Drills (test/melee4.mjs, all pass): alone, a man of nerve 0.56 gives way at the shove; with three men watching
(0.18 more) the same man stands and it comes to blows, saying why; face is capped at 0.24; a timid man (0.30)
still gives way in front of six; shoved against a wall with nowhere to go, the 0.56 man comes off it swinging.
G with nothing to hand does nothing; G by a thing takes 0.5 s and brings it out as a weapon. Drill M7 (sheet
C12): chair breaks after 2 blows (band 1 to 3), brick 3 (2 to 5), dustbin lid 4, wheel brace not in 25 (like
the sheet's pipe, at least 20). A lid picked up before a fight keeps its count across two fights and breaks on
its fourth blow, then stays broken.

AI playtester, newcomer's first hour (round 3, then round 4; one run each, run-to-run noise about 3 min on the
longest stretch):

| measure | round 3 | round 4 |
|---|---|---|
| waiting | 46% | 39% |
| walking | 22% | 29% |
| talking | 24% | 24% |
| driving | 5% | 6% |
| kinds of activity | 6 | 6 |
| new things, minutes 0 to 30 / 30 to 60 | 69 / 4 | 71 / 6 |
| longest stretch with nothing new | 13.5 min | 7.9 min |
| tense moments per 30 minutes | 15.0 | 18.0 |
| fights, pursuits, escapes | 0, 0, 0 | 0, 0, 0 |

Every debtor the newcomer fronted up still gave way (Darren at the shove with four watching: nerve 0.30 and
0.24 face is under a shove; Wayne at the shove; Lee, Julie and Dennis at the threat, by when Tom's name had
grown from the Darren shove seen by four). No new fault in the sweep. Live AI talk is untested here.

## 18 November 2026, lane round 3 (fists with weight): the drills and the AI playtester before and after

The melee feel sheet's drills, run in the build through the test hook at 1/60 s (test/melee3.mjs), against the
sheet's bands (production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md):

| drill | before (round 2) | after (round 3) | band |
|---|---|---|---|
| jab, start to contact | 0.20 s | 0.28 s | 0.25 to 0.40 |
| heavy, start to contact | 0.55 s | 0.70 s | 0.63 to 0.85 |
| hit-stop jab / heavy | none | 0.05 / 0.10 s (measured in 1/60 s steps) | 0.025 to 0.05 / 0.06 to 0.12 |
| man's reaction to a jab / a heavy | 0.28 / 0.70 s | 0.60 / 1.13 s | 0.5 to 0.7 / 0.9 to 1.3 |
| Tom busy after a heavy lands (freeze not counted) | about 0.61 s | 0.48 s | 0.35 to 0.50 |
| men swinging at once (three men, 20 s) | up to 3 | 2 | 1 to 2 |
| gap between two men's swings starting | no rule | 0.47 s at least | at least 0.40 |
| longest wait between one man's swings | up to about 2.6 s | 1.7 s in the drill | at most 2.5 |
| enemy wind-up readable before it lands | 0.50 s | 0.52 s at least | 0.45 to 0.80 |
| jabs from full to too tired | never (breath came back between jabs) | 9 | 6 to 10 |
| too tired to full | not measured | 6.2 s | 4 to 8 |
| a man struck with a wall behind him | nothing | hits it, 1.18 s reaction | (the design's wall) |

The newcomer's first hour (seed 19901120; times are estimates of a human's pace; two runs of the same build):

| | before (round 2) | after (round 3), two runs |
|---|---|---|
| talking | 23% | 24%, 24% |
| walking | 29% | 23%, 22% |
| waiting | 40% | 48%, 46% |
| driving | 6% | 3%, 5% |
| job actions and fronting up | 3% | 2%, 2% |
| kinds of activity | 5 | 6, 6 (fronting up) |
| new things, minutes 30 to 60 | 5 | 7, 4 |
| longest stretch with nothing new | 11.4 min | 10.5, 13.5 min (run to run the playtester varies by about 3 min) |
| tense moments per 30 minutes | 7.5 | 15.0 (one fronting-up counted once: 7 choices under pressure, 3 risks of being seen, 20 sightings) |
| fights, pursuits, escapes | 0 | 0 (all five debtors gave way at a stare, square-up or threat) |

A scripted fight sample outside the hour (two young men set on Tom at night): 16 to 28 s, Tom landed 6 to 10
blows and took 5 or 6, blocked 4 to 8; onlookers stopped and called out ("Leave him, he's had enough!"); once
Tom was beaten, once they gave way. The panel's report: production/lane/REVIEWS-round3.md in the repository.
Waiting rose; the empty stretch is within the playtester's variation. The next round should let a debt come to
blows in the first hour.

## 18 November 2026, lane round 2 (the carry under watch): the AI playtester before and after

Same playtester (seed 19901120), a newcomer's first hour. Times are estimates of a human's pace.

| | before (round 1) | after (round 2) |
|---|---|---|
| talking | 13.1 min, 22% | 13.9 min, 23% |
| walking | 19.2 min, 32% | 17.3 min, 29% |
| waiting | 22.3 min, 37% | 23.8 min, 40% |
| driving | 5.4 min, 9% | 3.6 min, 6% |
| job actions (the night carry) | none | 1.6 min, 3% |
| kinds of activity in the hour | 4 | 5 |
| new things, minutes 0 to 30 / 30 to 60 | 59 / 3 | 70 / 5 |
| longest stretch with nothing new | 11.8 min | 11.4 min |
| tense moments per 30 minutes | 6.0 (all sightings) | 7.5 (12 sightings, 3 risks of being seen: the carry past the constable at 28 m) |
| pursuits, fights, escapes | 0 | 0 (the newcomer kept to the dark by chance; the chase is tested in watch2) |
| prompt names someone else (sweep) | 3 | 5 (all a nearer person within Tom's facing, as the rule says; the crowd stood differently) |

The night job is now reached in the first half hour and is the moment six of eight simulated reviewers named
as the most exciting. Waiting is still the biggest share; the target of about ten activities per 30 minutes is
not near. The panel's report is production/lane/REVIEWS-round2.md in the repository.

## 18 November 2026, lane round 1 (the eight fixes): the AI playtester before and after

Both builds played the same day by the same playtester (the lane's tools/lane/prototype/playtester/, seed
19901120): a newcomer's first hour, then a walk-up to every person at four times of day. Times are estimates
of a human's pace; the playtester's own waiting is counted as waiting.

| | before (page of 12:00) | after (round 1) |
|---|---|---|
| talking | 21.8 min, 36% | 13.1 min, 22% |
| walking | 15.0 min, 25% | 19.2 min, 32% |
| waiting | 21.8 min, 36% | 22.3 min, 37% |
| driving | 1.8 min, 3% | 5.4 min, 9% |
| new things, minutes 0 to 30 / 30 to 60 | 52 / 11 | 59 / 3 |
| longest stretch with nothing new | 10.7 min | 11.8 min |
| tense moments per 30 minutes | 5.5 | 6.0 (all: seen out at night; no fights, chases, escapes) |
| prompt names someone other than the person in front | 10 | 3 (all three: two people standing on one spot) |
| a reply repeated word for word within one talk | in most talks (Sheila 4, Ron 3, Kevin 4, Ada) | none |

Talk is now well under half the hour (the canon pillar's target) and driving tripled; waiting and the longest
empty stretch are about the same (shorter talks leave the newcomer more idle). The target of about ten distinct
activities per 30 minutes is not near: the hour still holds four kinds (walk, talk, drive, wait). The reviewer
panel's verdict is in the repository's production/lane/REVIEWS-round1.md.

18 November 2026, second round. Run on the published build (`ledger.js` checksum in `BUILD.md`).

## The same week, before and after the numbers were moved

One full scripted week, seed 19901015, on a clock the test owns (`test/same_week.mjs`).

- The page as published earlier on 18 Nov (numbers still in their own files): whole digest
  `d45ae942a389fab4d9a4`, three runs, the same each time.
- The build with every number moved into `rules.js`, nothing else changed: `d45ae942a389fab4d9a4`.
  All 19 parts of the save the same: 88 events, 153 stories passed on, 140 Ledger entries, pocket £68.60.
- Record: `test/golden/week_published_18nov.json`.
- After the retiming and the fixes the week is meant to differ, and has a new record, `test/golden/week.json`:
  whole digest `6e859584cd20ea3d7ab0`, two runs the same: 91 events, 197 stories passed on, 151 Ledger
  entries, pocket £68.00.

## Numbers still written outside rules.js

```
ok   src/seeing.js             0 left
ok   src/gossip.js             3 left (3 indexes, counts and plain arithmetic)
ok   src/events.js             7 left (7 indexes, counts and plain arithmetic)
ok   src/ledger.js             1 left (1 indexes, counts and plain arithmetic)
ok   src/money.js              1 left (1 unit conversions)
ok   src/fares.js              3 left (3 text and layout)
ok   src/jobs.js               0 left
ok   src/police.js            13 left (2 indexes, counts and plain arithmetic, 2 text and layout, 4 unit conversions, 5 places on the map)
ok   src/routines.js          37 left (19 how people and things look, 9 indexes, counts and plain arithmetic, 5 unit conversions, 4 places on the map)
ok   src/talk.js               9 left (2 unit conversions, 3 indexes, counts and plain arithmetic, 4 text and layout)
ok   src/talk_lines.js         3 left (2 unit conversions, 1 indexes, counts and plain arithmetic)
ok   src/scenes.js            26 left (8 unit conversions, 5 places on the map, 13 text and layout)
ok   src/work.js              12 left (2 indexes, counts and plain arithmetic, 9 unit conversions, 1 places on the map)
ok   src/fight.js             18 left (2 text and layout, 15 indexes, counts and plain arithmetic, 1 camera and controls)
ok   src/clock.js              4 left (2 unit conversions, 2 indexes, counts and plain arithmetic)
ok   src/kinds.js              8 left (8 unit conversions)
ok   src/cast.js              60 left (60 how people and things look)
ok   src/measures.js          17 left (13 unit conversions, 4 indexes, counts and plain arithmetic)
ok   src/light.js              7 left (7 indexes, counts and plain arithmetic)
ok   src/state.js             20 left (9 indexes, counts and plain arithmetic, 5 places on the map, 2 camera and controls, 4 unit conversions)
ok   src/player.js            96 left (80 camera and controls, 5 text and layout, 10 places on the map, 1 indexes, counts and plain arithmetic)
ok   src/drive.js             30 left (3 indexes, counts and plain arithmetic, 23 places on the map, 1 camera and controls, 3 how people and things look)
PASS: every number outside src/rules.js is one the record allows
```

The numbers 0, 1 and 2 are not counted above: 1,053 of them were left in place, unexamined.

## Every walk against its row

```
PASS: all 145 walks fit their rows, with Tom away and with Tom at the rank, with a quarter to spare
```

## Arrivals, 26 game hours, twice (`LEDGER.check.arrivals()`, `test/arrivals.mjs`)

- Tom away: indoors at Regent House: Mon 15 Oct, 3.42pm to Tue 16 Oct, 5.43pm. 153 walks set off, 150 arrived, 0 given up for another place, 3 still on their way at the end, longest walk 88 game minutes, stood still: 0, pause never ended: no. PASS.
  - Still on their way when the 26 hours ended: Lee Drewery to away from the Hook (set off Tue 16 Oct, 5.30pm); Nora Cronin to the chapel (set off Tue 16 Oct, 5.36pm); Shaun Hewson to away from the Hook (set off Tue 16 Oct, 5.30pm).
- Tom standing at the rank: Mon 15 Oct, 3.42pm to Tue 16 Oct, 5.42pm. 153 walks set off, 142 arrived, 0 given up for another place, 11 still on their way at the end, longest walk 192 game minutes, stood still: 0, pause never ended: no, Tom put back at the rank 1 time(s) after the game put him to bed. PASS.
  - Still on their way when the 26 hours ended: Ron Kirby to the Golden River (set off Tue 16 Oct, 5.24pm); Darren Milner to Quay Street, the quay end (6, 29) (set off Tue 16 Oct, 3.36pm); June Suddaby to the ferry landing (-42, 57) (set off Tue 16 Oct, 4.00pm); Terry Hodgson to the Golden River (set off Tue 16 Oct, 4.30pm); Lee Drewery to away from the Hook (set off Tue 16 Oct, 5.30pm); Susan Coverdale to the ferry landing (-55, 61) (set off Tue 16 Oct, 5.12pm); Nora Cronin to the chapel (set off Tue 16 Oct, 5.36pm); Albert Suggitt to Quay Street (-6, -63) (set off Tue 16 Oct, 2.24pm); Dennis Iveson to Iveson's yard (-98, 30) (set off Tue 16 Oct, 3.06pm); Norman Dent to the Golden River (set off Tue 16 Oct, 3.54pm); Shaun Hewson to away from the Hook (set off Tue 16 Oct, 5.30pm).

The whole results, walk by walk, are in `results/arrivals.json`.

## Nights (`LEDGER.check.nights()`, `test/nights.mjs`)

- Tuesday night arrivals with Tom at the rank, Tue 16 Oct, 10.00pm to Wed 17 Oct, 7.00am: 29 walks set off, 19 arrived, 0 given up, stood still: 0.
- Self-test: a person held on the spot is caught by the check.
- Night of Tue 16 Oct: Tue 16 Oct, 10.00pm to Wed 17 Oct, 6.00am. 1 pause(s), 0 with no resume.
  - Wed 17 Oct, 4.24am: dead on his feet: to bed, resumed: dead on his feet: to bed: done
- Night of Wed 17 Oct: Wed 17 Oct, 10.00pm to Thu 18 Oct, 6.00am. 1 pause(s), 0 with no resume.
  - Thu 18 Oct, 4.24am: dead on his feet: to bed, resumed: dead on his feet: to bed: done
- Pause that never ended: none. Watchdog faults: 0. PASS.

## The gossip, before and after the retiming

The same seeded week on each build; each cell is before then after. One week each, not an average.

| Day | Sightings | Stories passed on | Furthest story (tellings) | Pairs of named people who met |
| --- | --- | --- | --- | --- |
| Mon 15 Oct | 161 then 98 | 11 then 16 | 2 then 3 | 14 then 27 |
| Tue 16 Oct | 6 then 11 | 52 then 87 | 4 then 5 | 48 then 79 |
| Wed 17 Oct | 0 then 0 | 31 then 18 | 8 then 6 | 43 then 69 |
| Thu 18 Oct | 2 then 3 | 31 then 14 | 9 then 4 | 53 then 73 |
| Fri 19 Oct | 0 then 0 | 22 then 53 | 5 then 8 | 54 then 82 |
| Sat 20 Oct | 0 then 0 | 6 then 9 | 5 then 8 | 17 then 29 |
| The week | 169 then 112 | 153 then 197 | 9 then 8 | 62 then 95 |

Met in the week after, not before (43): ada + albert; ada + june; ada + nora; ada + walsh; albert + alison; albert + brenda; albert + nora; albert + walsh; alison + julie; alison + kevin; brenda + nora; brenda + susan; brenda + terry; darren + lee; darren + nora; darren + norman; dennis + grace; dennis + julie; dennis + rita; dennis + shaun; dennis + sheila; dennis + wayne; grace + kevin; grace + lee; julie + kevin; julie + lee; julie + nora; julie + sheila; june + lee; june + susan; kevin + norman; lily + norman; lily + terry; nora + ron; nora + sylvia; norman + peter; norman + ron; norman + susan; norman + terry; pauline + terry; peter + terry; rita + shaun; rita + sheila.

Met in the week before, not after (10): ada + darren; albert + kevin; albert + susan; alison + darren; alison + dennis; alison + june; alison + sylvia; darren + julie; june + kevin; lee + susan.

## The measures, from one full week played by a script

Not a person: `test/week.mjs` plays the week through the test hook. The file is `measures.json`.

- Ledger opens per hour of play: 14.1 (7 opens). Median seconds open per visit: 0.9.
- Find the fact: keyboard 4 of 4 found; pad not played.
- Talks: 13, slip unfolded in 46 in 100. Noted lines shown: 10, followed by an open within 60 seconds: 30 in 100.
- Tab pressed in the first hour: yes. Lines said per Tab open: 0.84. Turns from suggestions: 98 in 100.
- Entries: 188, struck through: 13, with no source event: 0.

## The tests

All run on the published build.

| Test | What it checks | Result |
| --- | --- | --- |
| `npm run numbers` | no number outside `rules.js` beyond the recorded ones | PASS |
| `npm run walks` | every walk fits its row with a quarter to spare, both cases | PASS (145 walks) |
| `test/same_week.mjs` | the seeded week gives the recorded save, part for part | PASS (19 parts) |
| `test/week.mjs` | one full week by script, thirteen checks, no error, no pause fault | PASS |
| `test/arrivals.mjs` | both arrivals checks over 26 game hours | PASS |
| `test/nights.mjs` | Tuesday night arrivals, the self-test, both nights' pauses | PASS |
| `test/town.mjs` | 19 checks: seen, ladder, police, tea, second ask, the yard, Ellis, the lads, saving | PASS |
| `test/ledger_rules.mjs` | 14 checks: "Nobody saw" never taken out; `/` and a letter | PASS |
| `test/layout.mjs` | slip, subtitles and Ledger over a talk at four window sizes | PASS |
| `test/files.mjs` | the files beside the page list, read, zip and save | PASS |
| `test/talk.mjs` | live talk with a stand-in: working, off, refused, a broken rule | PASS |
| `test/oldsave.mjs` | a save from the page published in the first round loads, Ledger rebuilt | PASS |
| `test/eyes.mjs` | the town's eyes setting off and on (prints what it finds) | ran, no error |
