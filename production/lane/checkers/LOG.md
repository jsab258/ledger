# Checkers proven: log

The checkers session of Monday 23 Nov 2026 (scheduled task "LEDGER checkers proven before the one-shot"), Opus 5.5 at high effort. Aim: prove the checkers that will judge the one-shot against planted faults, before the one-shot starts (about Mon 7 Dec). Writes only here and in tools/lane/checkers/.

## How a later run continues

- Tools: tools/lane/checkers/variant.py builds a planted copy of the prototype outside the repository (the game's own folder is never changed) and runs the play stories, the machine checks, the clumsy run and the consequence checker on it. CLUMSY-PLAYER.md is the Sonnet clumsy player's card.
- Planted files are kept outside the repository (/home/claude/chk-secret/) while the checkers run and committed here only after scoring (planted-r1.json, planted-r2.json).
- Set-up on a fresh machine: one-sim.sh setup and wasm; the 13 pictures from the prototype's page into /home/claude/proto-assets; a clean build with oneshot_dev.py.

## Entries

- 13:18 Started. Budget: the newest Allowance reading is 95% at 12:08 on 22 Nov, last week's; the week reset at 13:00 today, so this week starts near nothing. Kept modest.
- 13:25 Set up: the town code built (wasi-sdk 34, .NET 8), the pictures fetched and checked, the clean build made. The machine has 2 cores, so runs go two at a time.
- 13:28 Clean build's own play stories (once each): S01 to S04 pass; S05 fails in its "runs" branch (12 lines: the constable's fresh call, walking to the landing, the hand-over) and S06 fails its "runs" branch as a result (3 lines). The log of 20 Nov says both passed twice then, so the branch head no longer holds all six stories here. These are counted as known clean failures: only new failing lines count as a catch.
- 13:29 Round 1: 17 faults planted (secret file), one build per fault plus three builds with five or six faults each (G1 to G3) for the slower checkers. Queue started: the stories on every single-fault build; the machine checks, the clumsy run and the consequence checker on the clean build twice and on G1 to G3.
- 14:05 Round 1 re-planned after two crashed pages (two browsers at once on two cores): one job at a time; the stories run on the three grouped builds and the clean build twice, then single-fault builds only where a group's chain is cut short. First AI player (story player, Opus, on G1) played 8.3 minutes and quit. The hidden-check harness written (spec and hidden.py, 6 tests passing).
- 17:40 Round 1 scored (ROUND-1.md): 7 of 17 caught; stories 3, machine 2, clumsy 2, consequence checker 0, AI 1. Mends written (machine_plus.py, story watchers overlay, BREAKER-MENDS.md); machine_plus calibrated on the clean build (all pass, fares after giving the keys in test setup). Round 2: 14 fresh faults in three builds (H1 to H3), plus round 1's G builds again with the mended stories; queue started 17:36.
- 19:10 Round 2 so far: stories on C0, H1 to H3 and the G builds with the watchers; machine_plus on all; three AI sessions with the mended briefs (two trapped by a pre-existing title screen that takes no keys). Fixes found by round 2 in the mends themselves, made after the runs and not counted: the content scan's quote pairing on the minified bundle, a 1990 words scan, the crowd threshold (a quarter, not half: rain thins it by design), the save watcher (parts emptied before the reload), the talk check names people it could not open.
- 21:05 Singles: news-goes-cold, flat-stair-night, talk-box-keeps-keys and run-down-kills run alone: none caught. The fixed watcher catches the debt book and the Ledger left out of the save, and passes the clean build. CHECKERS-PROVEN.md written.
- 21:20 Fresh Opus review of CHECKERS-PROVEN.md: ten points, fixed once (two round 2 probables added: the flat stair and the talk box; stories in round 1 now 4; the six new-check catches named; post-fix evidence copied to runs/postfix; noise listed in full; the S19 row; plain words in the top).
