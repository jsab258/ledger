# Results of the checks

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
