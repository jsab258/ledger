# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 06:22 (the hourly run; the last session set its Stopped line at 06:19)

**Row due:** 2026-11-17 09:30 (last 08:30; page and advisor read 08:27, advisor 189 acked 08:20)
**Stopped:** 2026-11-17 06:19 (history near its limit at an item's end; all helpers reported; the scale ladder waits in the background for the Kiln queue)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line runs from 0 at Monday 13:00 to 95% by Wednesday 15:00, six helpers, full pace. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page or the progress page: read the live page and each published file first (out_dir to the scratchpad), diff, then publish.
- Advisors 111, 113, 117: paid-tools sweep before any second try; each garment its own time-log window.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Time log "tool loop: <tool> round n".
- **Advisor 182 (his 14:12), trial from 16 Nov for two to three days:** Kiln rounds and their judging run in helpers that hand back a short verdict only (counts, reviewer's line, files); judged by history share and rework in the DAILY files against last week's 24%.
- **Advisor 181 (his 14:06):** helpers on the cheapest model that matches: reading, extraction, imports, log summaries, first screens, routine edits go to the project's Sonnet agents (extractor, importer, research-reader, small-reviewer), never general-purpose; Opus (diagnoser, research-synthesis, final-reviewer) for diagnosis, design, judged fixes, final reviews.
- **His pick A, 16 Nov 12:24 (advisor 174):** breadth patterns from FreeSewing and GarmentCode into Kiln's job format; Marvelous only for comparison drapes while its bridge is up; the bridge's start recovers by itself (closing the Welcome window, restarting by script) and is never raised on his page again. Own leftovers deleted under RULINGS 29 Oct, never a page item (the page tool refuses one).
- **Held-back jobs never reach a fixer:** never name the two held-back garments in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).

- **Advisor 189 (his 08:02, 17 Nov):** every hourly row names F:'s free room and the next 12 h's need (clear it that hour if short) and the gap to the line; `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported (1 GB a job); no delete outside retention.py without its protected list and readers checked; before 01:15 each night queue machine-free work for the allowed helpers. **Advisors 190-192 (his 08:20, 09:07, 09:25):** no new drives ever; superseded gate pictures and the Game Animation Sample copy (if unread) may go, list first (production/research/disk/CLEAROUT-LIST-2026-11-17.md); target a steady 1.4 points an hour day and night, each row giving the 6-hour rate and when 93% comes (he presses the spare reset near 93%; asleep near 93%: stay under 95%); when the current order waits on the machine, free helper places take the next order's machine-free work, recorded in the order ledger.

- **Before writing Stopped: end every background job of your own** (fresh_gate.py since 17 Nov holds starts up to 120 min while any session's background command still runs).

## Done the runs before
- git show 4b16a336e:production/handover/HANDOVER.md (04:52 to 06:19), d74c1862d, 5606f2805, 9f155e60f, 983ad87da.

## Done this run (06:22 on)
- Night walk's "Sheila is not on the street" (12, 16, 17 Nov) was the tester's: go_to swung beside her; greet read before the game placed people. route_walk.py: stop test in_reach (0.8 of talk reach, same side of the office wall), greet re-reads 15 s; selftest 23/23 (UNCOMMITTED until ci-checks; commit after the ladder). Report F:/LedgerTools/tool-dev/reports/SHEILA-MISSING-DIAGNOSIS-2026-11-17.md.
- n16-1: lanes judged (KILN-LANES-VERDICT-2026-11-17.md): skirt PASS, merged onto Kiln main 7838e29; jackets FAIL (own neck-base change bdc599d worsens j3, though bdc599d is also the likely donkey stand fix: KILN-DONKEY-STAND-DIAGNOSIS); trousers FAIL (per-piece solver passes). Gate fix f153caa (a baseline-known unmade job no longer exits 3). Lane fixes try 1 in a helper (report KILN-LANES-FIX1-2026-11-17.md; builds and gates only after the ladder).
- n16-5: plan written and reviewed, fixes taken (production/research/street-checks/N16-5-PLAN-2026-11-17.md and -REVIEW): 12 units, 14.5 h, launderette first. The 17 Nov walk did play the brick (played copy cf9d6ac, 01:42).
- n16-8: Darren's head remake HELD: export_mesh_fbx.py needs the full editor; the helper's launch of UnrealEditor.exe was refused by the permission system; not retried. No copy of his face mesh anywhere (C:, F:, backup).
- n16-7: hip-joint method 7 of 36 failing (try 1 9) after the measure floor fix; method stopped, kept default (dd2c46796); knee research in a helper. n16-3: ladder done (100 MB a street-length, +0.2 ms). n16-5: launderette no change 0.45 h; grocer to chandler checked 0.2 h; S1 running in a helper. Start-check fix pushed. Clear-out list, M5 step 1 code in helpers.

## Next, in order
0. FIRST: verdicts after the last read in UTC; advisor after 2026-11-17T09:30:00+01:00 (last ack 09:16). Row due 09:30.
1. Helpers' results if they landed after the stop: F:/LedgerTools/tool-dev/reports/KILN-LANES-FIX1-2026-11-17.md (lane fixes, try 1 of 2 each); S1 street wear (pictures in F:/LedgerTools/gate/new/, previews production/previews/n16-5-*; whole frame: his batched look before main), then S2; production/research/disk/CLEAROUT-LIST-2026-11-17.md (check it, then delete in daytime outside Unreal runs; one DECISIONS line, room in the row); m5-ron-trousers code; production/research/n16-7-knees-method-2026-11-17.md (review, then try).
2. n16-1: collar-plane lane's gate; re-take the baseline after the skirt merge.
3. n16-3: people 0 to 40 at N=10 packaged (no Unreal or drapes beside).
6. n16-8: the head export needs a full-editor run the permission system refused to a helper; ask in the next interactive moment or find an allowed route; then rerun round 5 at 60 roots/cm2.
6b. n16-1 zips: PARKED as F:/LedgerTools/tool-dev/runs/kiln-gate-jobs-2026-11-17/dressing-rule-and-jobs.patch (Kiln checkout restored so the lane gates keep their inputs): PAT_DRESSING_REFUSES true (mechanics.rs ~498, comment still says off) and regression_jobs.json pointing at F:/LedgerTools/tool-dev/runs/kiln-gate-jobs-2026-11-17/ (6 of 8 scripts with openings marked by lane-zips efdfb5b's check_openings). A helper's cherry-pick of efdfb5b onto main was refused by the permission system: not retried; lane-zips goes through the gate like any lane, then cargo test with the rule on and check_openings on all jobs, then commit and re-take the baseline.
7. n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 (not beside perf captures). DAILY by 19:00.

## Tonight's machine-free queue (advisor 189 item 4; start before 01:15, helpers as allowed)
1. Kiln M5 step 1 for Ron's work trousers: the turns record for MH_RoccoP2's standard body and the bend-back script (code and its tests; runs after the walk) per KILN-M5-RIGGING-METHOD-2026-11-17.md.
2. n16-7: research why the source's slightly crouched stands leave target knees bent (131_01, 113_15 Rocco; pelvis ruled out), a note with one candidate.
3. n16-5: the plan's roof runs R1-R4 checks written as scripts' inputs (no Unreal), from the slate-roofs skill.
4. n16-3: the people 0 to 40 ladder script at N=10 (tools/scale_ladder.ps1's pattern) ready to run after the walk.
5. Reviews of anything finished in the evening.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: in production/orders/2026-11-16.md section 3 (13 items) and git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off); hair capture fault 4 (fixed); CMU route try 1 at step 3 of 5. 17 Nov 04:52 on: CMU measure reader 2 of 2 (the clips were wrong, not the reader); CMU source root scale 1 of 2 (fixed); CMU feet 2 of 2 (set aside, try 1 kept); Kiln collar ring 1 of 2 in flight; hair round 5 is a fixer round within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$14.04 from 23:32 to 00:03.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
