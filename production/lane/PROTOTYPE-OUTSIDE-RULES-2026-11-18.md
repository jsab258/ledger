# Prototype numbers still outside LEDGER.rules (18 Nov 2026, second round)

Rewritten 18 Nov 12:40 for Fable's second round of 18 Nov (page version 1794997640-def7, ledger.js 17830684...). The first version of this note (12:05, first round, version 1794992731-61ca) listed the ladder, the schedules, the traits, the act table and the story and talk numbers as outside; Fable's second round moved all of those in. This version replaces it.

Status: for the record and for the real game's port. The prototype's simulation is frozen after the current Fable round (his ruling of 10:28), so nothing here asks for a new round.

## What moved in

The rules table (project/src/rules.js, window.LEDGER.rules) now has 32 sections and, by Fable's count, 1,313 numbers: the first round's 20 sections plus ladder (the confrontation ladder), crowd, story, talk, asks, shops, tom, traffic, driving, kinds (the 52 kinds of thing the town can know), people (28 people's traits) and schedules (the 28 weekly schedules). cast.js now reads each schedule with week('name').

Checked here, not taken on trust:

- Fable's own guard, tools/numbers.mjs left, runs in the cloud and passes: every number outside rules.js in the 22 rule files is one its record (tools/numbers_kept.json) allows, by reason.
- The lane's rule checks (tools/lane/prototype/tests/rules_test.py): of 112 rows, 85 now read the rules table (67 before) and 27 still search a source file (45 before). The 18 rows re-pointed: 1.21, 1.21b, 1.21c (act table), 1.23 (assumed nerve), 2.11 (Tuesday push), 4.03, 4.05 (debts), 5.01 (statements), 5.10 (the lads), 6.06, 6.07, 6.07b (schedules), 6.08, 6.08b, 6.08c (traits), 7.02, 7.05, 7.07 (talk). Each now checks the table's value and, where the rule is a comparison in code, that the code reads that entry.
- Two numbers changed in the move, by the round's retiming, not by the move itself: Ron goes back to the rank after Tang's at 18:30 (was 17:54), and Sheila's caff lunch runs to 14:18 (she was back at 13:06). The rows hold the new numbers and say so.

## Still outside, carrying a number (Fable's record, 375 numbers)

From tools/numbers.mjs left on the published build, by reason: 58 unit conversions, 69 indexes and plain arithmetic, 29 text and layout, 53 places on the map, 84 camera and controls, 82 how people and things look. The biggest files: player.js 96 (80 camera and controls), cast.js 60 (looks), routines.js 37, drive.js 30 (23 places on the map), scenes.js 26, state.js 20.

Not counted at all:

- The numbers 0, 1 and 2 in the rule files (1,053 of them), left unexamined; Fable says most mean none, all, both, half or a flag, and "a handful are small rule values (one metre, two seconds)". Example found by the lane: gossip.js "hop: m.hop + 1" (row 2.06).
- Files outside the 22 rule files: main.js (autosave every 75 real seconds, row 8.04), saving.js (account save chunks of 150,000 characters, row 8.02), map.js, the render folder, audio.js, the Ledger screen's drawing. Save format is a format constant rather than a rule; the autosave interval is a rule a port would want in a table.
- Inside the rule files but not in the table: state.js's save version 4 (rows 6.02 and 8.01) is one of state.js's 20 counted numbers; clock.js's weather list (row 6.05) is words, so the counter never sees it.

## The lane's rows still outside

With a number: 2.06 (hop +1), 4.06 (Julie's slate, a spoken line), 4.11 (job pays sixty, a spoken line; its pay is in the table, row 4.11b), 5.03 (the ten who never make a statement, a flag per person in cast.js), 6.02 and 8.01 (save version), 6.05 (weather list), 8.02 (save chunk), 8.04 (autosave).

Behaviour or text only, nothing to move: 1.07, 1.14b, 2.05, 2.10, 3.01, 3.02, 3.04, 3.05, 3.06, 3.07, 4.04, 4.16, 4.17, 7.01, 8.01b, 8.03, 8.05, 8.06.

## For the real game's port

- The table is the prototype's whole tuning surface now; a port can read rules.js as data (it evaluates in Node to plain JSON) instead of hunting through code.
- Worth carrying across as table entries although the prototype keeps them in code: the autosave interval, the never-makes-a-statement flag (as a per-person trait beside nerve and discretion), and the small 1s and 2s that are rules (the hop count).
- Fable's open point that matters for the port (NOT_DONE.md item 1): walks are timed to fit with Tom away or at the rank only; anywhere else a long walk in his sight can still be given up. Either rows big enough for any walk at real pace, or a walker finishes the walk begun before turning for the next place (a routines logic change, his decision).
