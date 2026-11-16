# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 22:37 (the hourly run)
**Row due:** 2026-11-16 23:40 (the hourly row; last row 22:40)
**Stopped:** 2026-11-16 22:24 (history past its point at an item's end; Kiln helpers still running: jackets, trousers finishing, speed, regression gate, pattern check: their reports land as files)
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

## Done this run (22:37 to now)
- Judge on the body standard: the judge's own jobs (Seamshift transfers, the Marvelous comparison drape) never pass Kiln's drape start, so they stay; the two held-back jobs now name the standard bodies (Tom's; Sheila's = C1's body under S4's head), README and HASHES re-made, hash check clean. Held-back patterns are still PENDING (made in Marvelous before 26 Nov), so no held-back pass and no 70% switch yet.
- Speed lane try 1 reported: no card port kept (exact order slower; coloured order 2.4-3.2x faster but crosses two bars by 0.15 mm and 4 mm). Try 2 (diagnoser, from 22:47): coloured order with a convergence fix; report LANE-SPEED-TRY2-2026-11-16.md in the lane; card free by 01:10.
- n16-4 brick, new method try 1: tools/photo_flemish_tile.py (uncommitted) cuts 198 real bricks from brick_wall_006 into the drawn bond; output F:/LedgerTools/game-inputs/brick-flemish-photo-n16-4 (seed 3); 12 checks pass; near-crop screen PASS (Sonnet: reads old; shortfalls a little orange, mortar wide and grey, faint halos). Packaged film by an importer helper (from 22:46) into F:/LedgerTools/gate/new/brick-photo-n16-4, files restored by 00:45.
- Space 22:40: C: 62.4, F: 20.9 GB, GO. Row 22:40.

## Done the runs before
- git show 983ad87da:production/handover/HANDOVER.md ('Done this run': Kiln slide, arm line, body standard; picks 185-188; brick try 2 set aside), and 7e2198b04 before it. The RULINGS models-line amendment waits for a session at his desk (the unattended run's permission check refused it).

## In flight
- Kiln regression gate helper (diagnoser, from about 21:48): all eight jobs, measured bands, failing exit; report F:/LedgerTools/tool-dev/reports/KILN-REGRESSION-GATE-2026-11-16.md; edits uncommitted in Kiln (python/ only).
- Kiln fixer lanes (his 187), worktrees C:/LedgerTools/kiln-lanes/{skirt,jackets,trousers,speed} (speed: his 188, the card port, from 22:09), branches lane-*; reports in each lane's reports-lane/LANE-*-2026-11-16.md; judge runs one at a time via F:/LedgerTools/tool-dev/judge-run.lock; merge into Kiln main only after the full judge run passes (all milestones and the held-back jobs, never named to a fixer).
- Body standard DONE 22:17 (Kiln 3d32458): standard bodies F:/LedgerTools/bodies/standard-2026-11-16; old body files now refused; lanes must merge 3d32458 and use them (jackets lane told; gate helper told to re-baseline on them). Pattern check (rings against girths, seam travel) still to build.

## Next, in order
0. KILN INTEGRATION (judge side done 22:40). Merge lanes one at a time, each only after the full judge run passes: lane-skirt (3b10d4b, 7d5daf0: skirt fixed, report reports-lane/LANE-SKIRT), lane-trousers (passes per piece; read its report, check its commit), then jackets and speed when they report. The regression gate (python/regression_gate.py, uncommitted in Kiln main) and the pattern check (Rust, uncommitted) land by their reports KILN-REGRESSION-GATE and KILN-PATTERN-CHECK; commit each after reading.
1. FIRST: verdicts after 2026-11-16T21:05:00Z; advisor after 2026-11-16T22:08:00+01:00 (all acked to 188 and the 22:08 watchdog). Hourly row by 23:09. On the held-back jobs' first full pass: Kiln to about 70% (his 188), say so in that row, record n16-5 and the rest of n16-3 as waiting in the order's ledger.
3. Kiln under 185 and the Fable review: (a) regression gate (in flight); (b) body standard done; pattern check (step 2) in flight; (c) passes per piece (step 3). Thursday checkpoint 19 Nov: held-back jobs once, M5 counts, faults traded. Kiln faults with two Opus tries spent go to a Fable helper next.
4. Tonight's build: both packing steps and the n16-6 switch; space check by 23:30 (F: 20.7 GB at 21:10, floor 20: check first, delete own leftovers only); nothing in Unreal 01:15 to 04:30.
5. Morning: the three morning pictures against today's (reverse and night verify both packing steps); the walk's card memory against 5.07 GB; cam_office screen on the new copy.
6. n16-4 brick, a genuinely different method (try 1 of it): photographed bricks cut into the drawn bond (keep flemish_tile.py's sizes, header map and checks); donors from N16-4-PHOTO-BRICK-READING-2026-11-16.md (no Flemish scan exists in the allowed libraries; CC0 candidates Poly Haven brick_wall_006 and church_bricks_02, ambientCG Bricks094, downloaded 21:27 to F:/LedgerTools/game-inputs/polyhaven and ambientcg; looked at: brick_wall_006 is English bond with real worn, chipped, separable bricks: the donor; cut stretchers from its stretcher rows and headers from its header rows into flemish_tile.py's layout); add a near-crop realism screen before any film. Quay-end closure as a page item with pictures (batch with Tom's and Ron's looks).
7. Bridge live test once its heartbeat is stale; n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 on tonight's copy.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov 22:09: four stamps (a row and three DECISIONS lines) written without Get-Date, one 25 minutes off; read the clock in the same call that writes.
- 16 Nov 21:25: a drawn brick tile passed twelve measured checks and still read newly built near the camera: offline measures cannot see a CG surface; judge near crops before filming.
- 16 Nov 21:00: the scan grade (match_rgb) works in linear light; a first grade in display values missed by about a fifth.
- 16 Nov 21:11: editing RULINGS from an unattended run (and rewording another ruling to keep the cap) was refused by the permission check.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick (new method) try 2 next.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$10.70 from 14:09 to 14:45.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
