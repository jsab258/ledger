# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 04:52 (the hourly run; the last session set its Stopped line at 04:33)

**A second session ran by mistake 01:07 to 01:40** (gate committed in Kiln 0241526; integrate worktree C:/LedgerTools/kiln-lanes/integrate with all four lanes merged; cmu_clips.py TRIM = 2, flips 0; cmu_ue_retarget.py written). All kept by the 02:52 session.
**Row due:** 2026-11-17 04:47 (last row 03:47; page and advisor read 03:46, night check 03:41 acked)
**Stopped:** 2026-11-17 04:33 (history past its point at an item's end: CMU step 4 run, its measure reader faulted, try 1 of 2; Kiln lane gates helper still running)
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

## Done the runs before
- git show 5606f2805:production/handover/HANDOVER.md ('Done this run' 23:32 to 00:20), and 9f155e60f, 983ad87da before it.

## Done the run 02:52 to 04:33
- git show d74c1862d:production/handover/HANDOVER.md ('Done this run (02:52 on)').

## Done this run (04:52 on)
- Page and advisor read 04:53, 05:07, 05:25, 05:41 (nothing new); rows 04:53, 05:34.
- n16-7: the "reader fault" was the clips' (source rig node x100); cmu_clips.py exports bones in cm (set cmu-2026-11-17-cm), tools/ue/cmu_bone_dump.py reads tracks in Unreal (d74c1862d). Diagnosis F:/LedgerTools/tool-dev/reports/CMU-RETARGET-FEET-DIAGNOSIS-2026-11-17.md. Try 1 of 2 on "CMU feet" (helper; cmu_ue_retarget.py, cmu_bone_dump.py, cmu_measure.py edited, UNCOMMITTED): slide 6/6 pass, flips 0, height 3/6, knees 1/6; 143_18 RoccoP2 passes all (F:/LedgerTools/game-inputs/cmu-2026-11-17-try1/measure). Try 2 (one hip-joint scale, pelvis Z offset) no better: fault SET ASIDE after 2 tries, try 1's settings committed.
- n16-8: round 4 on Darren in Unreal draws fully (preview loomwright-hair-r4-darren-2026-11-17.jpg); crown thin, hard hairline, square sideburns. Round 5 fixer (helper) writing F:/LedgerTools/tool-tests-2026-11/loomwright-r5. About 2.5 h of 8.
- n16-1: collar 'cannot fit where it sits' is the check's plane (KILN-COLLAR-RING-DIAGNOSIS-2026-11-17.md); try 1 of 2 built in lane-collar-plane 1b88925 (C:/LedgerTools/kiln-lanes/collar-plane): pattern check passes the three, gate not run. The 02:52 run's lane queue still runs (queue.log): main 76dc035 passes every band (donkey not made); jackets exit 3; trousers then skirt.
- n16-3: step 2 editor screen at N=10, 20 people passes (preview n16-3-scale10-top-2026-11-17.jpg). Packaged ladder (hook stand, N 1,1,1,2,4,10,10,10, tags scaleN-rI) waits in the background for the Kiln queue's "queue finished" (tools/scale_ladder.ps1; each run is p1-packaged.ps1 -Only day-stand -Tag scaleN -GameArgs '-ScaleTest=N'). The capture scale1-l1 (05:34) ran beside a drape: void.
- F: 18.8 to 20.2 GB by own leftovers. Progress page republished with 17 Nov. nightly_walk.py flags a perf line from another build. 17 Nov's real perf: memory 4,984 MB peak, card frame 18.44 ms against 14.86 (watch tonight).

## Next, in order
0. FIRST: verdicts after 2026-11-17T04:40:00Z; advisor after 2026-11-17T03:47:00+01:00 (last ack 03:47). Row due 06:34 (last 05:34).
1. Helpers' results, if this run stopped before they landed: read F:/LedgerTools/tool-dev/reports/CMU-RETARGET-FEET-DIAGNOSIS-2026-11-17.md (appended try notes), F:/LedgerTools/game-inputs/cmu-2026-11-17-try2/measure, F:/LedgerTools/tool-tests-2026-11/loomwright-r5/ROUND5-FIXER-2026-11-17.md, F:/LedgerTools/tool-dev/reports/KILN-COLLAR-RING-DIAGNOSIS-2026-11-17.md (its build appendix); whatever is missing, rerun from that note.
2. n16-7: "CMU feet" set aside after 2 tries (try 1 committed). Next, one genuinely different researched method: place the target's hip joints (not its hips bone) from the source's hip joints, e.g. a hip-joint-based pelvis (diagnosis report's end; RULINGS 7 Nov), research note first. Then a fresh look by eye at the passing pairs, idle variety and look-at, the packaged film.
3. n16-3: read the ladder's lines in production/research/pre-production/p1-packaged/runs.jsonl (labels packaged-day-stand-scaleN-rI; scale1-l1 is void); fit memory and card time against N; then the other views and people 0 to 40 at N=10 (METHOD-NOTE step 4); check tonight's perf line against 14.86 ms.
4. n16-1: when the lane queue says "queue finished", judge jackets, trousers, skirt in a helper (short verdict); merge passing lanes onto main (skirt: keep both constant blocks in mechanics.rs); gate lane-collar-plane (1b88925, built: pattern check lifts the three collar refusals, nothing else changes; copy C:/LedgerTools/cargo-target/kiln-collar-plane/release/drape-studio.exe to the runs exe folder and run regression_gate.py gate --allow-better, after the scale ladder, never beside a perf capture); then regenerate the gate's job scripts from the zip-marking writers and turn PAT_DRESSING_REFUSES on. Speed lane stays off.
5. n16-8: round 5's abc on Darren in Unreal (groom_on_darren.py, LEDGER_GROOM_DIAG=1 LEDGER_GROOM_DIAG_HIDE=0, offset 0,1.52,16.89), then Tom's crown.
6. n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 (not beside perf captures). DAILY file by 19:00. n16-4 quay-end page item batched with Tom's and Ron's looks.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov 00:10: three hair tries (13 Nov) changed the asset while every picture was a cold capture; a behind-the-head pixel test hid buried and missing hair alike. Hide the surroundings, look from the side, capture over ticks.
- 16 Nov 23:00: the Flemish anti-grid check passes only on some seeds (seed 7 fails, 3 passes); a photo tile reusing the drawn tile's darks must use its seed.
- 16 Nov 22:09: four stamps (a row and three DECISIONS lines) written without Get-Date, one 25 minutes off; read the clock in the same call that writes.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off); hair capture fault 4 (fixed); CMU route try 1 at step 3 of 5. 17 Nov 04:52 on: CMU measure reader 2 of 2 (the clips were wrong, not the reader); CMU source root scale 1 of 2 (fixed); CMU feet 2 of 2 (set aside, try 1 kept); Kiln collar ring 1 of 2 in flight; hair round 5 is a fixer round within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$14.04 from 23:32 to 00:03.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
