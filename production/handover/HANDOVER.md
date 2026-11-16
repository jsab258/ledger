# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 14:07 (the hourly run)
**Next due:** 2026-11-16 15:45 (the hourly row; last row 14:45)
**Stopped:** 2026-11-16 14:52 (history past its point at an item's end; all committed and pushed to wip; nothing running)
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

## Done this run (14:07 to the stop; commits 7deea67b0, 642c62dfe pushed, and this stop's commit)
- Advisor 176 to 183 acted on and acked: RULINGS 1 Nov (credit pays for scripted checks), 8 Nov models (181), 9 Nov records (183's Monday audit file, first 23 Nov 12:50); 178 and 179 withdrawn (nothing written). DECISIONS entries for each. RULINGS at 4,900 of 4,900 (trimmed wording each time).
- Kiln round 10 recorded (LOOP.md, NOTEBOOK, time log): 2.2 to 2.7x faster, output byte for byte; the card port not made (the judged jobs run on the Drape Studio engine).
- tools/settings_check.py (advisor 182 item 2): 19 settings read, all OK at 14:20; SETTINGS-SWEEP-2026-11-16.md lists what a script cannot read (app-held task mode, enabled tasks, session effort).
- Drive space (advisor 173): production/research/disk/F-USAGE-2026-11-16.md and DRIVE-SPACE-FIX-2026-11-16.md: run outputs are only 2.5 GB; F: is held by protected lasting things; next steps 2 to 4 there (per-job caps, the gate pictures' superseded list for one batched tap, whether the Game Animation Sample copy on F: is still read). No second drive (his 1 Nov ruling: no new hardware).
- Kiln's design note: cost-per-garment table started (advisor 177), baseline 5.8 h for Ron's and Darren's 7 to 8 Nov refits.
- n16-3 step 2 screened at N=10 (SCREEN-N10-2026-11-16.md, previews 2026-11-16-scale-top-n10.jpg and -hill-n10.jpg): nine copies in the Hook, none over the street; 18 to 19 ms medians; card memory 5.5 to 6.15 GB, peaks 6.05 (day walk) and 6.74 GB (night walk): over the card. The night walk ran into morning (LIGHTS-OFF-DIAGNOSIS-2026-11-16.md): the clock now holds once a capture's camera is placed (bPerfHookClockHeld, CrimeProbe.cpp), both targets built, verified at N=2 and committed in this stop's commit.
- n16-1 bridge: start_bridge.ps1 rewritten under pick A (BRIDGE-AUTOSTART-FIX-2026-11-16.md; selftests 17/17, md_job 6/6, dry run read-only); heartbeat now carries the bridge's pid (takes effect at the bridge's next start).
- n16-1 breadth drapes, first run (helper, F:/LedgerTools/tool-dev/reports/KILN-BREADTH-DRAPES-2026-11-16.md): Sheila's skirt ran (144 s; body through 3 at yokeBack, deepest 13 mm; cloth inside 7 over 3 mm; worst stretch 4.59 yokeBack); Ron's jacket, Ron's trousers and Darren's jacket refused at Kiln's start check (cloth already intersecting the body: sleeveR, frontR, collar).

## In flight
- Nothing running. The N=2 night walk read (SCREEN-N10-2026-11-16.md): clock hold verified (41 lights lit at start and end), median 16.5 ms, card memory 5.15 GB, peak 5.71 GB; no 'walk ended' line printed at N=2, to read in its log before N=4.

## Next, in order
1. FIRST: verdicts after 2026-11-16T13:45:00Z; advisor after 2026-11-16T14:20+01:00 (all acked to 183). Hourly row due by 15:45.
2. Why N=2's walk printed no end line (grep scale2-walk-night.log for the walk's points); then N=4 (same night walk, -ScaleTest=4), then the stand views at the lowest N that stays under the card line; write the ladder into SCREEN-N10-2026-11-16.md. Then the card-memory packing plan (advisor 177, before people multiply), and the packaged walk.
3. Breadth drapes, try 2 for the three refused jobs: research how Kiln's start check and the job writers place pieces (round 8 noted start placements skipped for added pieces; KILN-ROUND10-REPORT; the job writers in tools/md-bridge/donkey_jacket.py-style writers, nylon_jacket.py), then a general placement fix (an offset or a pre-pass pushing pieces outside the body), no special cases, run through a helper per advisor 182. Sheila's skirt: the yoke through the body and its 4.6 stretch are the first faults (try 1 of 2). Then S6 measured in Blender for Darren.
4. Bridge live test once the heartbeat goes stale (or at Marvelous's next start): `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/md-bridge/start_bridge.ps1 -DryRun`, then `schtasks /run /tn "LEDGER Marvelous open"`, then read opens.jsonl and starts.jsonl. Four Marvelous copies are open (3988, 5736, 6292, 23092); with none named the start does nothing: close none that the task did not open.
5. n16-6: the packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 for core moments (inside the day's API ceiling).
6. n16-3 step 1's acceptance (-PerfHookCam=cam_nope ends the game; cam_office screen).
7. DAILY file by 19:00 with advisor 182's efficiency table (each improvement built/measured/not yet, with evidence and a day for the unbuilt), advisor 177's rows (hours logged against spend, session-start dollars against 15 Nov's US$15.83), 176's dollars against plan hours saved, 181's helpers' dollars per step by type and model, and `python tools/settings_check.py`. Space check by 23:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov: a 1,800-frame walk covers only about 30 m; the scale walk needs about 17,000 frames for 422 m.
- 16 Nov: by day no local light is lit; light counts need -PerfHookNight; captures longer than about 285 s crossed into the next part of the day until the clock hold.
- 16 Nov: three breadth drapes refused at Kiln's start check (cloth starts inside the body): try 1 of 2 for each.
- 16 Nov: the bridge start's UI Automation search took the Welcome window for the main one; rewritten (untested live).
- 16 Nov: a helper's 1.1 GB build took F: under its floor; build Rust on C:/LedgerTools/cargo-target.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 1 of 2 (three jobs); skirt yoke 1 of 2.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$10.70 from 14:09 to 14:45.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
