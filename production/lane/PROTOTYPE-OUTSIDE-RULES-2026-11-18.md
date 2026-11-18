# Prototype numbers still outside LEDGER.rules (18 Nov 2026)

Read from Fable's readable source of 18 Nov (tools/lane/prototype/project/src, page version 1794992731-61ca). The rules table is project/src/rules.js, shown in the page as window.LEDGER.rules: 20 sections (time, seeing, noise, memory, gossip, naming, police, money, prices, jobs, fares, light, weather, ticking, rest, beaten, ledger, routines, watching, noticing). Fable's own list of what is still outside is project/NOT_DONE.md item 4. This note checks that list and adds what it leaves out.

Status: for the record and for the real game's port. The prototype's simulation is frozen after the current Fable round (his ruling of 10:28), so nothing here is a new round.

## How the counts were made

Rough counts only: numeric literals other than 0 and 1, outside comments, per file. They include colours, sizes, indexes and text, so they overstate the rule numbers. Line numbers are from the 18 Nov source.

## By file

### fight.js (about 190 literals): the confrontation ladder

The whole ladder: rungs, reach, timings, damage, weapons. None of it reads rules.js.

- Line 28 to 35: weapon damage table (cosh 1.7, flick knife 2.1, brick 1.6, chair 1.5, wheel brace 1.8, cargo hook 1.9, dustbin lid 1.1).
- Line 58 to 63: who Tom fronts up to: within 3.6 m and within 1.2 rad of where he faces.
- Line 499: a blow's damage, 0.23 heavy or 0.125 light, times 1.7 with a weapon, less 0.3 per hurt.

### cast.js (about 390 literals): the people

Traits and weekly schedules for 28 named people, and their looks. Traits and schedules are data and could stay data, but they are rule numbers the town runs on.

- Line 17 to 20: Sheila's nerve 0.95, venal 0, talk 0.15, discretion 0.92 (rule 6.08).
- Line 34 to 40: Sheila's schedule, office 07:30, caff 12:30, office 13:06, off 18:12 (rule 6.07).
- Line 173 to 175: schedule rows for named days only (chapel on Wednesday at 08:00, window 09:12, fish queue on Friday at 10:00).
- The nostmt flag (10 people never make a statement, rule 5.03) is set per person here.

### routines.js (about 125 literals): the inner numbers of walking and the crowd

- Line 115 to 116 and 138: the crowd's talk 0.5 and nerve 0.6, then nerve drawn from 0.3 to 0.7; line 128: 16 crowd people.
- Line 407: a walk goes by the route nodes only when more than 6 m; line 410: each walker's lane offset, 0.7 m either side.
- Line 286 and 461: shops open 08:00 to 18:00 (both copies).

### scenes.js (about 185 literals): story timings and how lines move people

- Line 553: striking out a debt, regard +0.5 (rule 4.05); line 382, 484, 518: other regard moves (+0.4 or +0.1 at Ada's tea, +0.3, +0.2).
- Line 1111: a debtor pays if fear over 0.45, or regard over 0.3 and owing 15.00 or less (rule 4.03).
- Line 1633: Cammack's lads at loudness over 1.2 (rule 5.10); line 1660: statements taken at 04:00 from Tuesday (rule 5.01); line 1668: the Tuesday push at 08:45 (rule 2.11).

### talk.js (about 75 literals): talk coefficients

- Line 191 to 202: the mood words given to the model (regard above 0.35, 0.1, below -0.4, -0.12; fear above 0.5, 0.25).
- Line 395: a person tells what they know when regard is above -0.35, or fear above 0.45, or bought; line 465: a threat in talk, fear +0.4.
- Line 253: a live reply is cut to 380 characters and three sentences (rule 7.05); line 899: each exchange passes 1.5 game minutes (rule 7.07).

### kinds.js (about 110 literals): the act table

52 kinds, each with severity, value and crime level (rules 1.21, 1.21b, 1.21c). Line 18 to 22: inherit 0.5, 0, 0; line 229 to 232: kill 1, -1, 3. Not named in NOT_DONE.md.

### Others not named in NOT_DONE.md

- player.js (about 170 literals): shop and stall hours, for example line 41 fish 07:24 to 17:24, line 44 Tang's 17:00 to 23:36; the camera and movement numbers beside them.
- main.js: line 742, autosave every 75 real seconds (rule 8.04).
- state.js: line 5, save version 4 (rules 6.02 and 8.01). saving.js: line 25, account save chunks of 150,000 characters (rule 8.02).
- clock.js: line 31 to 32, the night and day weather lists (rule 6.05); the weather's own numbers are in rules.js.
- seeing.js: line 198, a person with no nerve set counts as 0.5 (rule 1.23). Otherwise seeing.js reads only rules.js.
- drive.js (about 100 literals): traffic, mostly spawn timing and car sizes. Not rules in the sense of the town, but numbers a port needs.
- render/, map.js, audio.js, ledger_screen.js: geometry, layout and sound; not rules.

## The lane's rule-check rows that fall outside

tests/rules_test.py has 112 static rows: 67 read rules.js, 45 search a readable source file (marked outside_rules).

Outside and carrying a number: 1.21, 1.21b, 1.21c (kinds.js); 1.23 (seeing.js default nerve); 2.06 (gossip.js, hop +1); 2.11, 4.03, 4.05, 5.01, 5.10 (scenes.js); 5.03, 6.06, 6.07, 6.07b, 6.08, 6.08b, 6.08c (cast.js); 6.02, 8.01 (state.js); 6.05 (clock.js); 7.02, 7.05, 7.07 (talk.js); 8.02 (saving.js); 8.04 (main.js).

Outside with no number to move (a behaviour or a line of text): 1.07, 1.14b, 2.05, 2.10, 3.01, 3.02, 3.04, 3.05, 3.06, 3.07, 4.04, 4.06, 4.11, 4.16, 4.17, 7.01, 8.01b, 8.03, 8.05, 8.06.

## Suggested order for moving them into rules.js

One at a time, each followed by the lane's checks (rules_test.py, the system tests, and the build reproducing its own new checksum), and each row in rules_test.py turned from outside_rules to rules in the same step.

1. Single numbers in scenes.js, talk.js, main.js and seeing.js (rules 1.23, 2.11, 4.03, 4.05, 5.01, 5.10, 7.05, 7.07, 8.04, and the talk mood thresholds). Small, each used once, and each already has a check.
2. Shop hours (player.js and the two copies in routines.js), merged into one entry, since two copies of 08:00 to 18:00 already exist.
3. The crowd's defaults in routines.js and the walk numbers (6 m, 0.7 m lane).
4. The act table in kinds.js: move severity, value and crime per kind into a rules section, keeping the text in kinds.js. The 52-kind count check guards it.
5. Traits and schedules in cast.js: the largest data move; best done by the real game's port as data files rather than inside rules.js. The schedule and trait rows (6.06 to 6.08c, 5.03) guard it.
6. The confrontation ladder in fight.js last: about 170 numbers, and the combat design is still open for the real game.

Save version, save chunk size and the weather lists (state.js, saving.js, clock.js) are format constants rather than rules and can stay where they are.
