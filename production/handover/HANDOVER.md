# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 06:22 (the hourly run; the last session set its Stopped line at 06:19)

**A second session ran by mistake 01:07 to 01:40** (gate committed in Kiln 0241526; integrate worktree C:/LedgerTools/kiln-lanes/integrate with all four lanes merged; cmu_clips.py TRIM = 2, flips 0; cmu_ue_retarget.py written). All kept by the 02:52 session.
**Row due:** 2026-11-17 08:17 (last 07:17; page and advisor read 07:10, advisor 07:09 pace guard acked)
**Stopped:** 2026-11-17 06:19 (history near its limit at an item's end; all helpers reported; the scale ladder waits in the background for the Kiln queue)
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

- **Advisor 189 (his 08:02, 17 Nov):** every hourly row names F:'s free room and the next 12 h's need (clear it that hour if short) and the gap to the line; `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported (1 GB a job); no delete outside retention.py without its protected list and readers checked; before 01:15 each night queue machine-free work for the allowed helpers. Target: on the line by 07:30 on 18 Nov.

## Done the runs before
- git show 4b16a336e:production/handover/HANDOVER.md (04:52 to 06:19), d74c1862d, 5606f2805, 9f155e60f, 983ad87da.

## Done this run (06:22 on)
- Page and advisor read 06:23, 06:37 (nothing new); row 06:23.
- Night walk's "Sheila is not on the street" (12, 16, 17 Nov) was the tester's: go_to swung beside her; greet read before the game placed people. route_walk.py: stop test in_reach (0.8 of talk reach, same side of the office wall), greet re-reads 15 s; selftest 23/23 (UNCOMMITTED until ci-checks; commit after the ladder). Report F:/LedgerTools/tool-dev/reports/SHEILA-MISSING-DIAGNOSIS-2026-11-17.md.
- n16-1: lanes judged (KILN-LANES-VERDICT-2026-11-17.md): skirt PASS, merged onto Kiln main 7838e29; jackets FAIL (own neck-base change bdc599d worsens j3, though bdc599d is also the likely donkey stand fix: KILN-DONKEY-STAND-DIAGNOSIS); trousers FAIL (per-piece solver passes). Gate fix f153caa (a baseline-known unmade job no longer exits 3). Lane fixes try 1 in a helper (report KILN-LANES-FIX1-2026-11-17.md; builds and gates only after the ladder).
- n16-5: plan written and reviewed, fixes taken (production/research/street-checks/N16-5-PLAN-2026-11-17.md and -REVIEW): 12 units, 14.5 h, launderette first. The 17 Nov walk did play the brick (played copy cf9d6ac, 01:42).
- n16-8: Darren's head remake HELD: export_mesh_fbx.py needs the full editor; the helper's launch of UnrealEditor.exe was refused by the permission system; not retried. No copy of his face mesh anywhere (C:, F:, backup).
- n16-7: research note for a hip-joint-placed pelvis in a helper (production/research/n16-7-hip-joint-pelvis-method-2026-11-17.md).
- n16-3: scale ladder running from 06:31 (8 captures; tools/scale_ladder.ps1).
- n16-10: guards already shown firing 16 Nov (GUARDS-FIRING-2026-11-16.md); DAILY due by 19:00.

## Next, in order
0. FIRST: verdicts after the last read in UTC; advisor after 2026-11-17T08:15:00+01:00 (last ack 08:20). Row due 08:17.
1. Helpers' results if they landed after the stop: KILN-LANES-FIX1-2026-11-17.md (jackets, trousers lane fixes, try 1 of 2 each), the n16-7 hip-joint note.
2. After the ladder (runs.jsonl lines packaged-day-stand-scaleN-rI): fit memory and card time against N; then ci-checks, commit route_walk.py with DECISIONS, push wip on failed=none.
3. n16-1: lane gates (fixer), then the collar-plane lane's gate; re-take the baseline after the skirt merge (the pleated skirt now hangs).
4. n16-5: the launderette in Unreal per the plan (first front; its hours set the ratio).
5. n16-7: try the hip-joint method (try 1 of the new method).
6. n16-8: the head export needs a full-editor run the permission system refused to a helper; ask in the next interactive moment or find an allowed route; then rerun round 5 at 60 roots/cm2.
6b. n16-1 zips: PARKED as F:/LedgerTools/tool-dev/runs/kiln-gate-jobs-2026-11-17/dressing-rule-and-jobs.patch (Kiln checkout restored so the lane gates keep their inputs): PAT_DRESSING_REFUSES true (mechanics.rs ~498, comment still says off) and regression_jobs.json pointing at F:/LedgerTools/tool-dev/runs/kiln-gate-jobs-2026-11-17/ (6 of 8 scripts with openings marked by lane-zips efdfb5b's check_openings). A helper's cherry-pick of efdfb5b onto main was refused by the permission system: not retried; lane-zips goes through the gate like any lane, then cargo test with the rule on and check_openings on all jobs, then commit and re-take the baseline.
7. n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 (not beside perf captures). DAILY by 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov 00:10: three hair tries (13 Nov) changed the asset while every picture was a cold capture; a behind-the-head pixel test hid buried and missing hair alike. Hide the surroundings, look from the side, capture over ticks.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off); hair capture fault 4 (fixed); CMU route try 1 at step 3 of 5. 17 Nov 04:52 on: CMU measure reader 2 of 2 (the clips were wrong, not the reader); CMU source root scale 1 of 2 (fixed); CMU feet 2 of 2 (set aside, try 1 kept); Kiln collar ring 1 of 2 in flight; hair round 5 is a fixer round within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$14.04 from 23:32 to 00:03.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
