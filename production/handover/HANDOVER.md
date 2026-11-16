# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 23:32 (the hourly run)
**Row due:** 2026-11-17 00:29 (the hourly row; last row 23:29)
**Stopped:** 2026-11-16 23:30 (history past its point at an item's end, the brick in the game; the regression gate and jackets lane helpers still running, their reports land as files)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line runs from 0 at Monday 13:00 to 95% by Wednesday 15:00, six helpers, full pace. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing** (broken twice this run: two guessed times in DECISIONS and an ack, corrected; read the clock before writing any time).
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page or the progress page: read the live page and each published file first (out_dir to the scratchpad), diff, then publish.
- Advisors 111, 113, 117: paid-tools sweep before any second try; each garment its own time-log window.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Time log "tool loop: <tool> round n".
- **Advisor 182 (his 14:12), trial from 16 Nov for two to three days:** Kiln rounds and their judging run in helpers that hand back a short verdict only (counts, reviewer's line, files); judged by history share and rework in the DAILY files against last week's 24%.
- **Advisor 181 (his 14:06):** helpers on the cheapest model that matches: reading, extraction, imports, log summaries, first screens, routine edits go to the project's Sonnet agents (extractor, importer, research-reader, small-reviewer), never general-purpose; Opus (diagnoser, research-synthesis, final-reviewer) for diagnosis, design, judged fixes, final reviews.
- **His pick A, 16 Nov 12:24 (advisor 174):** breadth patterns from FreeSewing and GarmentCode into Kiln's job format; Marvelous only for comparison drapes while its bridge is up; the bridge's start recovers by itself (closing the Welcome window, restarting by script) and is never raised on his page again. Own leftovers deleted under RULINGS 29 Oct, never a page item (the page tool refuses one).
- **Held-back jobs never reach a fixer:** never name the two held-back garments in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).
- The page tool (tools/needs_you_page.py) now also refuses install, setting and click asks (his_hands marks safety-check needs) and more than two batches of open items a day.

## Done this run (22:37 to 23:31)
- Judge on the body standard: the judge's own jobs (Seamshift transfers, the Marvelous comparison drape) never pass Kiln's drape start, so they stay; the two held-back jobs now name the standard bodies (Tom's; Sheila's = C1's body under S4's head), README and HASHES re-made, clean. Their patterns are still PENDING (Marvelous, before 26 Nov): no held-back pass, no 70% switch yet.
- Kiln pattern check committed (Kiln 3ec9c73, 34 tests): the 'cannot be put on' rule (closed waists, zips sewn as plain seams; six of eight jobs) is a flag (PAT_DRESSING_REFUSES false) until the job writers mark zips (SetSeamlineZipper) and flies. Sheila's skirt band cannot slip over her hips: the skirt's fall is the solver's.
- Speed lane: try 1 kept nothing; try 2 (lane-speed 49599c4, aa0ef11, switch off) is about 2x with SOR 1.1 inside every bar, but tuned on the judging jobs with thin margins (0.37 mm hang, 2.3 mm drop). Not merged until the regression gate's eight jobs pass with it (and the held-back jobs once they run); CREDITS must name wgpu and pollster first. Tries 2 of 2: any third needs a genuinely different method.
- n16-4 brick, new method try 1 PASSED its packaged film and is IN THE GAME from tonight's build: tools/photo_flemish_tile.py (real bricks from Poly Haven brick_wall_006 in the drawn Flemish bond, seed 3, 12 checks pass); near-crop screen and small review PASS (hook_day better, camA better, night and reverse equal). brick_red's scan entry (ps5-corner.json) names production/assets/scanned/photo_flemish_n16_4/* on F: game inputs, covers 2.72, match_rgb 0.556/0.376/0.316, tones map dropped; brick_4 still on the rubbed arches. Evidence: production/research/street-checks/N16-4-BRICK-PHOTO-2026-11-16.md. Commits df95b6c8e, 9f155e60f (wip, pushed, checks 103/103).
- Space 22:40: C: 62.4, F: 20.9 GB, GO (retention plan frees almost nothing; F: tight). Rows 22:40, 23:29.

## Done the runs before
- git show 983ad87da:production/handover/HANDOVER.md ('Done this run': Kiln slide, arm line, body standard; picks 185-188; brick try 2 set aside), and 7e2198b04 before it. The RULINGS models-line amendment waits for a session at his desk.

## In flight
- Kiln regression gate helper (diagnoser, from about 21:48, the previous session's): all eight jobs, measured bands, failing exit; report F:/LedgerTools/tool-dev/reports/KILN-REGRESSION-GATE-2026-11-16.md (not yet written at 23:31); its edits uncommitted in Kiln main python/ (run_job_script.py, regression_gate.py, regression_jobs.json, test_regression_gate.py).
- Lanes: skirt (3b10d4b, 7d5daf0) and trousers (f1251c0: passes per piece, trousers byte-identical at 0.49 of the work, Tom j3 better 1.396, 79/14) reported, waiting for the gate; jackets (bdc599d neck base from skin; Darren's underarm seams jam 27 mm, listed) still running at 23:00; speed done (above).

## Next, in order
0. FIRST: verdicts after 2026-11-16T22:00:00Z; advisor after 2026-11-16T22:09:00+01:00 (nothing new to 23:29). Row due by 00:29.
1. Kiln integration: when KILN-REGRESSION-GATE lands, read it, commit the gate's python files in Kiln main, then merge lanes one at a time, each only after the gate passes on the merged tree: trousers, skirt, jackets, then speed's switch tested (off by default). Lanes must sit on 3d32458's standard bodies. On the held-back jobs' first full pass (patterns pending): Kiln to about 70% (his 188), say so in that row, record n16-5 and the rest of n16-3 as waiting.
2. Kiln under 185 and the Fable review: (c) passes per piece = the trousers lane. Job writers to mark zips and flies, then PAT_DRESSING_REFUSES on. Thursday checkpoint 19 Nov: held-back jobs once, M5 counts, faults traded. Faults with two Opus tries spent go to a Fable helper.
3. Tonight's build carries the new brick, both packing steps and the n16-6 switch; nothing in Unreal 01:15 to 04:30.
4. Morning: the three morning pictures against today's (the brick now differs on every brick wall: judge it there, and its shimmer in motion from the walk); the walk's card memory against 5.07 GB; cam_office screen on the new copy. The brick's shortfalls (a little orange, mortar wide and grey, gable streaks weaker, Flemish faint) are listed, not failing.
5. n16-4 rest: quay-end closure as a page item with pictures (batch with Tom's and Ron's looks); then n16-4 can close on tonight's walk.
6. Bridge live test once its heartbeat is stale; n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 on tonight's copy.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov 23:00: the Flemish anti-grid check passes only on some seeds (seed 7 fails, 3 passes); a photo tile reusing the drawn tile's darks must use its seed.
- 16 Nov 22:09: four stamps (a row and three DECISIONS lines) written without Get-Date, one 25 minutes off; read the clock in the same call that writes.
- 16 Nov 21:25: a drawn brick tile passed twelve measured checks and still read newly built near the camera: offline measures cannot see a CG surface; judge near crops before filming.
- 16 Nov 21:00: the scan grade (match_rgb) works in linear light; a first grade in display values missed by about a fifth.
- 16 Nov 21:11: editing RULINGS from an unattended run (and rewording another ruling to keep the cap) was refused by the permission check.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off).
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$10.70 from 14:09 to 14:45.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
