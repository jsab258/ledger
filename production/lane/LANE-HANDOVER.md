# Lane handover: where the lane session stands

The one file a lane session starts from. Rewritten at each lane stop; cap 900 words. The lane is this week's second, machine-free session (his picks of 17 Nov about 16:05, advisor 202; RULINGS "7, 10 Nov", the 16 to 23 Nov part). It ends for good at Monday 23 November 07:00.

**Cloud lane, last run:** 05:16 to about 05:42, 20 Nov: 4t piece 4 built (tools/lane/gate/feel_numbers.py --dist DIR --out DIR [--refs FILE] [--ordinary]; test_feel_numbers.py; clumsy.py Proto.EXTRA_INIT lets a tool add a script before the page loads); reviewed and fixed (production/lane/REVIEW-4T-PIECE4-2026-11-20.md). Next: piece 8 (testing the testers, tools/lane/gate/plant/), then 4t is built. Run before that: 04:16 to about 04:35, 20 Nov: 4t piece 6 built (tools/lane/prototype/reviewers/panel/panel.py strip, pair, score; PANEL-PROMPT.md; ANCHORS.md; tests/test_panel.py); clumsy.py WORDS_JS and play.py SPOKEN_JS now read fixed boxes (#dialog), play.py charges half-typed lines once; reviewed and fixed (production/lane/REVIEW-4T-PIECE6-2026-11-20.md). Next: piece 4 (feel in numbers), then 8. Run before that: 03:16 to about 03:45, 20 Nov: 4t piece 5 built (tools/lane/gate/consequences.py, test_consequences.py; gate.py runs it on every build and lists rules "not reached" in the note; play.py keeps start_save, save_NNNN every 10 actions, final_save and the other people's spoken lines in the hidden folder); reviewed and fixed (production/lane/REVIEW-4T-PIECE5-2026-11-20.md). Next: piece 6 (the panel on recordings), then 4, 8. Run before that: 02:16 to about 02:38, 20 Nov: gate.py runs machine_checks.py (never passes without it); piece 3 breakers built in tools/lane/prototype/reviewers/breakers/ (BREAKERS.md, BREAK-PROMPT.md, replay.py; play.py now writes the seed as row 0, one session per --hidden folder; testers get a copy of play.py in PLAYDIR); reviewed and fixed (production/lane/REVIEW-4T-PIECE3-2026-11-20.md). Next: piece 5 consequence checker (reads the hidden actions.jsonl), then 6, 4, 8. Earlier run 01:17 to about 01:58, 20 Nov: 1c-rest done (late parts swept, check.py 0 faults); 4t pieces 1 (tools/lane/gate/machine_checks.py) and 2 (tools/lane/prototype/reviewers/players/) built, reviewed, fixed (production/lane/TESTING-SETUP-4T-2026-11-20.md has the state and what is open).  aim before the one-shot ends Saturday. Building the game for tests: python tools/lane/prototype/build.py --allow-changed --dist <scratch> (runs without the art; 404s are expected). From 21:00 Fri 20 Nov to 08:30 Sat only 4d, 4f, 4t; nothing in tools/lane/prototype/project/ or tools/lane/one-sim/ while the one-shot runs. 4d: no round4/ seen. Git: the lane branch carries merge commits from wip, so pull with --rebase=merges, never a plain rebase.
**Started:** (none yet)
**Stopped:** (none yet)
**Advisor read to:** (none yet; advisor rows carry +01:00 Swiss times) | **Last Lane row:** (none yet)
(Each run first runs `python tools/lane_gate.py` in C:\Users\Jafar\ledger-lane; at each item's end `python tools/lane_gate.py --history`: OVER means rewrite this file, set Stopped from Get-Date, stop.)

## The lane's rules (short; RULINGS and CLAUDE.md still hold in full)
- Only work that never touches the machine: the next order's research, plans, and code that needs no build to write; reviews of plans and specs; Kiln research and Kiln code review.
- Never: Unreal, the graphics card, builds, packaging, renders, drapes, Kiln runs or judge runs, captures, films, Blender, Marvelous, any game, deletes, the tester. No heavy local job of any kind.
- Never: simulated mouse or keyboard, computer use, UI Automation, a browser's interface. Research: no cookies or logins; an unreached source is listed, never used.
- Writes: only inside C:\Users\Jafar\ledger-lane (branch lane), and on F: only in F:\LedgerTools\lane-research. Never write in C:\Users\Jafar\ledger-local or anywhere else. Never copy, open or print a key, token or .env.
- Git: commit on branch lane only, files staged by name, the guards never skipped. Never push, never merge into wip or main, never rebase. The main session merges branch lane at its item ends.
- Staying current: after the gate's GO and the Started line, `git merge wip` once in the lane's worktree (local only; wip is in the same repository). On a conflict, `git merge --abort` and work on the older base; name it under "For the merge".
- Files the main session owns are never edited here: HANDOVER.md, NOW.md, FOR-JAFAR.md, DECISIONS.md, RECIPE.md, NOTEBOOK.md, FINDINGS.md, RULINGS.md, CLAUDE.md, production/time-log.jsonl, his page's items and the pace files. Lines meant for them go under "For the merge" below; the main session appends them when it merges.
- Never read F:\LedgerTools\tool-dev\judge (the held-back jobs). Kiln code is read, never run or changed; review findings go to production/lane/reviews/.
- His page: read the advisor channel by the same filtered queries as the main session; acknowledge nothing, answer nothing, publish nothing, open or close no item. One row an hour to the page's reports, beginning "Lane row": what the lane did, its spend (`python tools/lane_gate.py --spend HH:MM`), the rate (dollars an hour), the model.
- Asks for him never come from the lane: anything that needs him goes under "For the merge", and the main session decides whether it reaches his page.
- Helpers: machine-free only, within RULINGS' count; every brief forbids clicks, keys, computer use, machine work and the judge folder.
- Pace: may read C:\Users\Jafar\ledger-local\production\handover\pace-state.json (read only). Over 6 points ahead: no new token-heavy work or helpers. Never run tools/pace_line.py here (it writes the pace file).
- The night: hand over before 01:40 (the tester's walk); the gate holds the lane until the walk reports.
- Reference first and research first, as CLAUDE.md says; every plan names Mafia or Kingdom Come II's method, or "none found".

## Queue (in order; machine-free)
1. Parked cars, n16-9: review and finish production/research/phase2-plan/PLAN-PARKED-CARS-2026-11-17.md against its sources; the P9 blind silhouette test written as a reviewer's brief; the Blender script changes written but not run (code needing no build), marked "untested: needs the main session's run".
2. The games' numbers, n16-11: the method for UE4SS once per game (licence first, never beside Unreal, extract caps), with the licence note checked against ledger-v2/research/license-allowlist.md; the empty budget table ready to fill. Reference: production/research/aaa-reference/studies/12-tech-budgets.md. Nothing extracted or run here.
3. Street furniture and lamps (waiting item 4): from production/research/phase2-plan/TARGET-STREET-FURNITURE-2026-11-17.md, the build plan per piece (reuse first: what exists in the repository and catalogue), its checks, and any recipe code that needs no build.
4. Reviews of plans and specs: the other phase2-plan targets (fishmonger, empty unit), production/specs changes since 16 Nov, each by one fresh reviewer against its sources; findings in production/lane/reviews/.
5. Kiln code review: read-only reading of F:\LedgerTools\tool-dev\kiln (and its lanes' diffs) for faults, special cases and test gaps; findings in production/lane/reviews/, each naming the game item it unblocks. Kiln research (methods, papers) beside it.

## Done (newest first)
- (nothing yet)

## In flight
- (nothing)

## For the merge (the main session appends these where they belong, then empties this list)
- (nothing yet)
