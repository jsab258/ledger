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
- Page and advisor read 04:53 and 05:07 (nothing new); row 04:53.
- n16-7: the "reader fault" was the clips': the source rig node carried x100 (Blender's default scaling), so the retargeted pelvis sat about -96 m. cmu_clips.py exports bones in cm (new set F:/LedgerTools/game-inputs/cmu-2026-11-17-cm), tools/ue/cmu_bone_dump.py reads tracks inside Unreal, cmu_measure.py reads them (d74c1862d). Pelvis right now; all six pairs FAIL: feet slide 7.6-18.4 cm over source, height 2-16.5 cm, knees bent at last stand, one-frame foot/ball spikes (113_15, 131_01). Diagnoser out: report F:/LedgerTools/tool-dev/reports/CMU-RETARGET-FEET-DIAGNOSIS-2026-11-17.md. Tries on "CMU feet": 0 of 2.
- F: 18.8 to 20.2 GB by own leftovers (DECISIONS 05:05). Every remaining old gate/new folder is named by a record or tool: kept.
- Kiln: the 02:52 run's lane queue is still running by itself (F:/LedgerTools/tool-dev/runs/kiln-gate-2026-11-17-lanes, queue.log): main 76dc035 passes every band (donkey not made, known); jackets with the check off: 15 outside; jackets, trousers, skirt gates in turn from 05:03 (about 42 min each).
- Progress page republished with 17 Nov's pictures (and 11 Nov's, missing). The walk report's card-memory line was the night before's: nightly_walk.py now flags a line from another build. Real 17 Nov line: memory 4,984 MB peak (under 5.07 GB), card frame 18.44 ms against 14.86 (watch tonight).
- Hair round 4 on Darren running in the editor from 05:18 (F:/LedgerTools/tool-tests-2026-11/loomwright-r4/ue).

## Next, in order
0. FIRST: verdicts after 2026-11-17T02:46:00Z; advisor after 2026-11-17T03:41:00+01:00. Row due 04:47 (last 03:47).
1. Kiln: read the lane-gates report; merge each lane whose gate passes onto main (skirt: keep both constant blocks in mechanics.rs), re-take the baseline when a job newly made (donkey_jacket); fix the collar 'where it sits' refusal by the report's general fix (try 1); then regenerate the gate's six job scripts from the zip-marking writers and turn PAT_DRESSING_REFUSES on. Speed lane stays off. Held-back first pass: Kiln to about 70% (his 188).
2. n16-7: step 4 RAN 04:30 (ue_result.json DONE, 6 of 6 exported, auto rig, root Hips, Root Motion op off by name; no BadPelvisHeight; F:/LedgerTools/game-inputs/cmu-2026-11-17/ue). The measure FAILS ON ITS READER, not judged yet: Blender reads Unreal's export with the armature object 'root' at scale 0.01 and pelvis as first bone; rest is right (pelvis 92.8 cm) but pose locations come out about 100 times too large (slide 45 m). Try 1 of 2 (scale every location key by 0.01) put the pelvis at 0 cm: wrong. Second try or, better, a genuinely different method: read world bone positions inside Unreal (AnimPoseExtensions at each frame in a commandlet, write JSON) and give cmu_measure.py a JSON reader for the target. Then the measured check, a fresh look by eye, a packaged film. Probe script: the session scratchpad's probe_ue_fbx.py (copy it if needed).
3. n16-8: round 4 job (F:/LedgerTools/tool-tests-2026-11/loomwright-r4) on Darren in Unreal with groom_on_darren.py warmed captures (LEDGER_GROOM_DIAG=1, ~60 ticks), side, front, behind, beside today's strands; tip colour import; then Tom's crown. About 2 h of 8 used.
4. Morning: the three morning pictures (04:15 task) against yesterday's; the walk's card memory against 5.07 GB; FOR-JAFAR day summary by 07:00, overview by 07:30.
5. n16-4 rest: quay-end closure page item with pictures, batched with Tom's and Ron's looks.
6. n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 on tonight's copy.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov 00:10: three hair tries (13 Nov) changed the asset while every picture was a cold capture; a behind-the-head pixel test hid buried and missing hair alike. Hide the surroundings, look from the side, capture over ticks.
- 16 Nov 23:00: the Flemish anti-grid check passes only on some seeds (seed 7 fails, 3 passes); a photo tile reusing the drawn tile's darks must use its seed.
- 16 Nov 22:09: four stamps (a row and three DECISIONS lines) written without Get-Date, one 25 minutes off; read the clock in the same call that writes.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off); hair capture fault 4 (fixed); CMU route try 1 at step 3 of 5.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$14.04 from 23:32 to 00:03.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
