# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 12:37 (the hourly run; the session started 11:54 set no Stopped line but wrote no turn for 39 minutes, so taken as stopped; a background job of the last session still runs: the card left alone until it ends, then its result taken)
**Next due:** 2026-11-16 12:07 (the hourly row; then near 99% by 12:55, never 100%; about 12:50 the week's numbers and the progress page publish; set it at every stop)
**Stopped:** 2026-11-16 11:52 (history near its hard limit at an item's end; all committed and pushed to wip)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). Until Monday 13:00 the advisor 168 pacing applies: near 99% by 12:55, never 100%; start nothing that cannot finish by 12:55.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). Write it with ArtifactData and see its version. "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing.**
- Pace rules: RULINGS 7, 10 Nov and 13 Nov; the 16 Nov reset week runs a doubled line from 13:00 Monday, six helpers, no busywork; rows name any hour with no session (advisor 140/143).
- Never end a turn while work remains (advisors 64, 68; the stop hook enforces it); the Stopped line is the last thing written (advisor 104).
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Advisors 111, 113, 117: paid-tools sweep before any second try; the tool driven without clicks; each garment its own time-log window.
- **Kiln (RULINGS 13 Nov; by design 14 Nov, now in RULINGS):** serves LEDGER; every module and fix names the game item it unblocks; no special cases ('special cases: none' in each report); held-back jobs at every milestone from M5; M7 the finish line, its count in every round report (0 so far). Time log "tool loop: <tool> round n". Caps: clothing about 20 h (12.6 spent), hair about 8 h. Its share this week is set by his answer to the advisor's 07:40 evaluation (held at 23% in the order).
- **He no longer develops any of his tools (advisor 146):** the copies under F:/LedgerTools/tool-dev are their only line of development.
- **Held-back jobs never reach a fixer:** never name the two held-back garments in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked in judge/HASHES.txt, 22 files, verified 07:10).

## Done this run (10:07 to 11:44; commit 8777b50a6 pushed, the rest in this stop's commit)
- Page: no verdicts after 2026-11-16T07:50Z; advisor 171 (99% at 12:55 is the line, preparation pulled forward), 172 (M6's outfit is Ron's donkey jacket and work trousers; every passed breadth garment into garments.json; Monday audit counts Kiln garments in the game) and the 11:10 watchdog note (set reset_at when the meter drops) all acked; last advisor read 11:36, nothing after 11:10+01:00. Rows 1008 and 1107 (1107 corrected at 11:15 after the review).
- n16-6 leg 1 done and reviewed (BAKEOFF-SONNET55-2026-11-16.md, review pass with fixes taken): Sonnet 5.5 (thinking between_tools) about 0.5 s sooner at the median than Sonnet 5, tails mixed, invented and answerable fall-backs equal by two labellers; Sonnet 5.5 needs its thinking set (26 of 60 empty without); --reply-thinking-off sends between_tools (CoreTests 5,254). The game's own routing of newcomer questions is unchecked (the bench's moment rule is words-only). US$2.62 of the task's US$4.00, all in api-spend.jsonl.
- n16-3 step 1: cam_office defined (staff view); cam_hill and cam_office in production/specs/measure-cameras.json, read after vignette-scene.json and staged; both targets built. Step 2: design saved (STEP2-DESIGN-2026-11-16.md, core about 14 h, not 8); tools/scale_test_layout.py (selftest 476) wrote scale-test.json at N=10 (9 copies in the Hook, the walk the three nearest slots, 422 m).
- n16-1: Marvelous opened by its task; the bridge would not start (two tries, a researched children-only walk, a further run refused by the safety check): his click asked on his page (marvelous-bridge-2026-11-16, NEEDS YOU sent). ast-grep installed and credited. Kiln round 10 step 2 measured by the session: card path 10.6 ms against 122.8 ms a step (12 threads), contact 31%: port next.
- n16-2: Ron's outfit plan (production/art/clothing/RON-KILN-OUTFIT-PLAN-2026-11-16.md: 17 to 21 h of garment work against 10 h; the jeans-to-trousers swap is his look at the gate); step 1 measures (full body equals the Body set in every girth; brian-ron.json stands); step 2 the Titan trouser draft (F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/).
- Progress page: a week's-numbers section (index.html) and data for 9 to 15 Nov (progress.json weeks[0]); its allowance row says "to be read at 12:50". Not yet published.

## In flight
- Ron's job writers landed and committed (donkey_jacket.py 88/88, work_trousers.py 37/37; jobs generated in F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/, not run). Next for them: Kiln drapes them (plan step 6) once the straight-elbow body exists (step 3, Blender, needs F: room); the helper notes the stand and fall overlap at Neck_Back and the trousers job was generated with --settle.
- F: is at about 18.6 GB (retention reads 20.0 at its rounding): under the 20 GB floor for builds, renders and Blender. None of my leftovers is safely deletable (old tool-test outputs are cited as evidence in their reports). Before 23:30 the night build's space check needs room: if F: still reads under 20, put a one-tap item on his page (old tool-test outputs in F:/LedgerTools/tool-tests-2026-11, about 3 GB, with the reports kept).
- His page: one open item, marvelous-bridge-2026-11-16. On "done": check heartbeat.json is fresh, close the item, start the breadth patterns (Ron's jacket and trousers first, then Sheila's skirt, then the held-back two, never named to a fixer). On "retry": run tools/md-bridge/start_bridge.ps1 once (the nested children walk, untested).

## Next, in order
1. FIRST: verdicts after 2026-11-16T07:50:00Z; advisor after 2026-11-16T11:10+01:00 (all acked). Hourly row due 12:07.
2. About 12:50: read the weekly figure (get_usage), put it in progress.json weeks[0] "Allowance used" and a phase 2 hours-to-go point (last 447 to 764 on 9 Nov; this week's time log recorded about 21 h of phase 2: mark the method), run tools/progress_page.py, publish production/progress-page/index.html to https://claude.ai/artifact/EEcWMTp5E9VqKrQsC8KBdk with progress.json and today's three street/ pictures (the tool prints the map). When the meter drops: reset_at in production/week-shape.json, say so in the row.
3. From 13:00 (doubled line, six helpers): Kiln round 10 step 3, the port of the vendored hybrid path into Kiln (brief KILN-ROUND10-SPEED-BRIEF-2026-11-16.md steps 3 to 7; build target C:/LedgerTools/cargo-target, never F: while F: is low); Ron's outfit steps 3 onward (Blender needs F: room: the straight-elbow body and boots proxy); n16-3 step 2's C++ (-ScaleTest, -ScalePeople, -PerfHookRoute=scale, -PerfHookWalkM; stage scale-test.json; one editor run at N=10) and step 1's acceptance (-PerfHookCam=cam_nope ends the game; cam_hill and cam_office screens), all once F: has room; n16-6 next: the packaged run with Sonnet 5.5 for core moments (needs the game to send between_tools: a game change, then run G's way), and checking which model the game itself sends newcomer questions to.
4. The DAILY file by 19:00; read-back of page verdicts every two days (last 16 Nov 07:00).
5. Space check by 23:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov: the bridge start's UI Automation search timed out on a fresh Marvelous (also 8 Nov); a scheduled run cannot be granted computer use, and the safety check refuses a third start: ask his click early.
- 16 Nov: a helper's 1.1 GB build took F: under its floor; the space check reads free space before a job, not its size. Build Rust on C:/LedgerTools/cargo-target.
- 16 Nov: a routing claim drawn from the bench (all newcomer questions to Haiku) was wrong for the game; check the game's own call.
- 16 Nov: an unattended run may not edit the licence list or the project's settings.
- Rounds 7 to 9: measure each check's cost on the real job; prove a new check on a fail and a pass control first.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the Marvelous bridge start (2 of 2, his click asked).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept (autostash used for rebases, applied back each time).
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed). F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body; use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since. Model spend US$7.77 from 07:52 to 08:53 (token_measures --spend).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
