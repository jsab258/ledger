# The playbook's five costliest traps, turned into checks or rules (8 November 2026)

For Monday 9 November's order. The traps follow the README's ranking as corrected by its review (REVIEW-2026-11-08.md, fault 1). Costs were re-read on 8 Nov in RECIPE.md (by line) and production/time-log.jsonl. Existing checks were read the same day in tools/ci-checks.sh, the tools named below and .claude/skills. Build costs are estimates against the playbook's figure for a check script: 0.3 to 0.5 h.

## 1. "Done" outside the player's game

**What happened.** The player character reached the packaged game three weeks after "done", because assets loaded by path were never cooked (RECIPE 598, 27 Oct). Masonry scans were missing from the shipped build for a month while the build machine stayed green (1718, 3 Nov). Two pieces passed only behind test switches (1885, 1916; 7 and 8 Nov). **Lost:** weeks; no hour figure.

**Covered already.** stage_game_data's selftest fails on unstaged spec files (in ci-checks). launch_line_check.py is run only by hand (packaged-walk skill): it is not in ci-checks, and route_walk.py does not call it. Nothing checks that assets loaded by path get cooked.

**Guards.**
- (a) route_walk.py writes the launch-line verdict into verdict.json, and TEST fails the run. Add `launch-line-selftest` to ci-checks. Must catch: the -TomSit seat proof (TEST, RECIPE 1916). Must pass: the night walk's log (PLAYER+WATCH). 0.5 h.
- (b) A cook-coverage row in stage_game_data --selftest: every `TEXT("/Game/…")`, `/MetaHumanCharacter/…` or `/Engine/…` literal in ue-probe/Source must sit under a DirectoriesToAlwaysCook entry, or be on a known list with a reason (84 literals in 8 files, counted 8 Nov). Must catch: the ini without its `/Game/Blueprints` line, against SliceCharacter.cpp's SandboxCharacter_CMC path (the 27 Oct case). Must pass: today's files. 0.5 h. Unverified: how many literals the cook reaches through references and so need the known list.

## 2. A chained session design tested piece by piece

**What happened.** On 3 Nov the chaining failed, because a scheduled run may not start another. On 7 Nov a restart killed the session at 00:14. The hourly WAIT runs were then counted as activity, so nothing started until about 10:45 (fresh_gate.py docstring; RECIPE 1877). **Lost:** "about ten hours" (1877). The time log has a gap from 00:13 to 10:47 (lines 536 to 537): idle wall clock, not work.

**Covered already.** fresh_gate --selftest has 23 cases, including that sequence. It is not in ci-checks.

**Guard.** Add `fresh-gate-selftest` to ci-checks with one property case: for any series of hourly runs after a last real turn, the gate must say GO within DEAD_MIN (120 min) plus one hour. Must catch: the 7 Nov series decided the old way. Must pass: a session writing a turn every 10 minutes for 8 hours (WAIT each hour). 0.5 h.

## 3. A vendor's searched locomotion adopted before its clips were measured

**What happened.** Four walking entries never passed the walk's slide. The clips themselves dragged planted feet 11 to 18 cm, and neither reference game uses search. **Lost:** about 8.9 h (3.5 + 3.5 + 1.2 + 0.7; RECIPE 1341, 1048, 962, 906; 22 to 26 Oct).

**Covered in part.** Since 28 Oct, order_ledger.py fails a push when a new item names no reference. That came after all four entries. Naming Mafia's or Kingdom Come II's chosen-clip walk would have exposed the conflict. No skill covers animation.

**Guard: a rule.** No automatic check is practical, because "adopted before measuring" is in no file a script can read. One line in the gate skill until an animation skill exists: "Before adopting a clip set or animation method, measure every clip's planted feet in its own frame and state the reference games' method; a method they do not use needs a written reason." 0.1 h.

## 4. Long renders before frame-free checks; only changed views reviewed

**What happened.** A 66-minute gate found 13 intersections that a two-minute test would have caught, and a 2-hour redo followed (RECIPE 1440, 13 Oct). Renders of 0.9 h and 1.6 h were thrown away, and 3 h of frames came before a coplanar sill was seen (1427, 14 Oct). The launderette's right view was first reviewed in round 3 (gate-launderette/GATE.md, 24 Oct), and the chandler's door faults went unseen for four rounds (23 Oct). **Lost:** about 7.5 h of renders (README, summed), plus extra review rounds that were never costed.

**Covered already.** Each kit family has a frame-free check (check_*.py under production/cloud-week). The gate skill runs automatic checks first (step 3) and makes "one full pass of every view at the gate's end" (step 1). Engine pictures now take minutes, so most of the render cost is gone (inferred).

**Guards.**
- Rule, gate skill step 1: "A piece's first round reviews every view it appears in (a shop: shop_views.py's four by day and four at night); later rounds review only the changed views." 0.1 h.
- Optional check: refuse a gate PASS while any of the piece's views has no reviewer file under F:/LedgerTools/gate/new/<piece>/r*/. Must catch: the launderette after round 2. Must pass: its round 5. 1 h. Unverified: whether reviewer files are named by view consistently.

## 5. Uncapped extraction; watchers that wait only for success

**What happened.** One study's 26 GB of exports filled the shared disk, and another game's combat files were never reached (RECIPE 449, 458; 28 Oct). A cook stopped and went unnoticed for two hours, because the watcher waited only for success (1130, 23 to 24 Oct). **Lost:** about 2 h of waiting, plus data never reached.

**Covered already.** `retention.py space` checks free space only when a job starts. The cap is a memory and a line in the brief. Wait loops are scattered (play.py, morning_pictures.py, route_walk.py, two voice benches) and share no helper.

**Guards.**
- `retention.py space --watch DIR --cap-gb N` polls the folder while the job runs, writes a STOP file and exits 1 once the folder is over the cap. Every extraction brief starts it. Must catch: a selftest folder over its cap (the 26 GB case scaled down). Must pass: the 48 MB sound extract against its 1.5 GB cap (RECIPE 420). 0.5 h.
- Rule, packaged-walk skill: "Every wait watches for the failure line and for the process ending as well as for success, and has a time limit." 0.1 h.

## Total

About 2.3 h, or 3.3 h with the optional views check. Each one extends an existing tool or skill.

## Unverified

- The RECIPE evidence files were not opened; the costs are RECIPE's own.
- The ranking mixes units: trap 1 is counted in weeks, trap 5 partly in lost data.
- Whether the -TomSit seat-proof log is still on disk to serve as a fixture was not checked.
