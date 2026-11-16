# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 20:17 (the hourly run)
**Row due:** 2026-11-16 22:12 (the hourly row; last row 21:12)
**Stopped:** 2026-11-16 19:51 (history at its point at an item's end; Kiln slide helper still running)
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

## Done this run (18:07 to 19:52; pushed to wip: bef9165fd, f00d4dbeb, 4d8bbc44b)
- Packing step 2 (run-time pictures compressed, BC1/BC5/BC3): fresh Sonnet reviewer pass at hill and hook (editor, same binary, 4.6 to 3.8 GB standing); in tonight's build.
- Packing step 1: Lumen atlas 3584 and probe resolution 16 in DefaultScalability.ini [GlobalIlluminationQuality@2]; packaged three walks each: about 186 MB less at the median, frame equal. Pictures: HOOK ONLY passed review (last night's copy predates -PerfHookCam and reads only cam_hook; the 'reverse' pair was the hook view: corrected in DECISIONS). Logo (T_GameAnimationSample_Logo) not done.
- n16-4 part 1: brick target (production/research/street-checks/N16-4-TARGET-2026-11-16.md, reviewed, fixes taken): Flemish, 86 mm courses (texture only; kit grid unchanged), occasional clustered darker headers (20-35%, no chequer, no gloss), greyer recessed mortar. tools/street_checks.py: width in ci (10.25 m PASS); --ends report-only: cam_A 9/21, cam_hook 9/21, cam_reverse 5/21 rays closed (known shortfall; how the quay end closes is taste: his page with pictures). Kit reuse waits for a placement spec.
- Kiln collar placement try 1 kept (KILN-COLLAR-FIX-2026-11-16.md): neck and shoulders from each body's skin; four of four breadth jobs start; Tom's regression within noise (stretch 1.518 vs 1.502). Committed in Kiln's own repo (376aac6).
- DAILY-2026-11-16.md written 18:22; hourly rows 18:09, 19:09; recipe map rows C1, C9, B9 updated.

## Done the runs before
- 15:52 to 17:06 and 14:07 to 14:52: git show 8a078e06f:production/handover/HANDOVER.md ('Done this run', 'Done the run before').

## In flight
- A diagnoser helper (Opus, started about 19:15) on Kiln's slide-down at the 10 mm stage, TRY 2 OF 2 for that fault: research note KILN-SLIDE-METHOD, fix, a height check in Kiln's drop check, reruns of Ron's trousers and Tom's j3; report F:/LedgerTools/tool-dev/reports/KILN-SLIDE-FIX-2026-11-16.md; edits uncommitted in F:/LedgerTools/tool-dev/kiln (commit them in Kiln's repo if kept). It waits while LedgerProbe/UnrealEditor runs. If not closed: set aside, listed.

## Next, in order
1. FIRST: verdicts after 2026-11-16T18:50:00Z; advisor after 2026-11-16T15:54+01:00 (nothing new since; all acked to 184). Hourly row due by 20:09 (last 19:09).
2. Read the Kiln slide report when it lands; record (DECISIONS, NOTEBOOK, recipe map row B9/D3), commit Kiln's repo if kept.
3. Tonight's build carries both packing steps and the n16-6 Sonnet switch: space check by 23:30 (F: 22 GB, floor 20); nothing in Unreal 01:15 to 04:30.
4. Tomorrow morning: the morning pictures (hook, reverse, night) against today's for both packing steps (reverse and night unverified); the walk's card-memory line against 5.07 GB packaged; then cam_office screen with the new copy (-PerfHookCam=cam_office -PerfHookShot on the packaged exe).
5. Kiln: Darren's arm line on his headless body (try 1 of 2); then M5 rounds (helpers, advisor 182).
6. n16-4 part 2: the brick at 86 mm with header flags and clustered darkening (route in the target, section 2), try 2 of the new method; the quay-end closure as a page item with pictures (batch with Tom's and Ron's looks); kit-reuse check once a placement spec exists.
7. Bridge live test once its heartbeat is stale; n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 on tonight's copy.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov 19:45: p1-packaged.ps1 runs write no pictures, and last night's packaged copy ignores -PerfHookCam (reads only cam_hook): check the log's 'stand at' line before trusting a view's name.
- 16 Nov 17:00: Kiln start check try 2 of 2: set aside as listed; two different faults remain (collar height rule, slide-down at 10 mm).
- 16 Nov: a timed walk at a faster frame rate ran out of frames before the route's end (frames x frame time x 1.4 m/s must exceed 422 m).
- 16 Nov: the profiler's LightCount/All is lights shaded per frame (DeferredShadingRenderer.cpp:2818), not lights lit; read the log's lit line.
- 16 Nov: by day no local light is lit; light counts need -PerfHookNight; captures longer than about 285 s crossed into the next part of the day until the clock hold.
- 16 Nov: three breadth drapes refused at Kiln's start check (cloth starts inside the body): try 1 of 2 for each.
- 16 Nov: the bridge start's UI Automation search took the Welcome window for the main one; rewritten (untested live).
- 16 Nov: a helper's 1.1 GB build took F: under its floor; build Rust on C:/LedgerTools/cargo-target.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick (new method) try 2 next.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$10.70 from 14:09 to 14:45.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
