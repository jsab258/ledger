# Lane handover: where the lane session stands

The one file a lane session starts from. Rewritten at each lane stop; cap 900 words. The lane is this week's second, machine-free session (his picks of 17 Nov about 16:05, advisor 202; RULINGS "7, 10 Nov", the 16 to 23 Nov part). It ends for good at Monday 23 November 07:00.

**Cloud lane, last run:** started 01:16 on 19 Nov, stopped 02:08. 4q, the full audit, is the lane's first item (his order 00:18, 19 Nov). Stage 1 done (production/audits/full-2026-11/INVENTORY.md, DECISIONS-TRACE.md, README.md). Stage 2: six of eleven reviews written (REVIEW-01, 02, 04, 07, 08, 11). Next run: the five remaining reviewers (03 research, 05 art, 06 Kiln and tools, 09 spending and pace, 10 licences, backup and disk) with work/REVIEWER-BRIEF.md, Opus at high, all at once if the ceiling allows; then stage 3 (AUDIT-REPORT.md, a fresh check, the Claude Doc "LEDGER: full audit"). After the report: 4n step 3 (review of the five synthesis files, now against the audit too; REVIEW-01 found the synthesis drops June, Philip Danby and Father Walsh) and the fix by a fresh Fable helper, then 4n step 4. 4p (GTA VI first read) beside them with one or two cheap helpers. Helpers read his page's rows from /home/claude/db (ArtifactData list with out_dir; not committed). Budget: 33% at 01:32 against a ceiling of 34.1%; check the newest main-session row before each wave.
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
