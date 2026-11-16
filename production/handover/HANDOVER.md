# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 15:52 (the hourly run)
**Next due:** 2026-11-16 17:52 (the hourly row; last row 16:52)
**Stopped:** 2026-11-16 17:06 (history past its point at an item's end; packing step 2's helper still building)
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

## Done this run (15:52 to 17:06; commits pushed to wip plus this stop's commit)
- Advisor 184 (recipe map, his pick A 14:48) acted on and acked: RULINGS 9 Nov records line (cap 4,900 held), DECISIONS; the map (claude.ai/artifact/PDhLE6yEQKYuHWbzy7Y3pH) reached with the Docs tools; F6's row updated with the ladder. From now each NOTEBOOK entry moving a step changes its row the same hour.
- n16-3 ladder done (SCREEN-N10-2026-11-16.md, previews -top-n4, -hill-n4): N=2 walk short because 17,000 frames at 16.5 ms cover only ~392 m at 1.4 m/s (walks now 22,000 frames); N=4 night walk 17.6 ms, peak 5.9 GB (under the card); N=4 stand top 14.1, hill 17.8 ms. The card holds to four street-lengths, crosses 6 GB by ten; ~0.3 ms per copy. Step 1 acceptance: -PerfHookCam=cam_nope ends the game (passed).
- Card-memory packing plan (advisor 177's gap taken): production/research/frame-headroom/PACKING-PLAN-2026-11-16.md, reviewed (pass with fixes, all taken). Step 0 done packaged (OWNER-DUMP-2026-11-16.md): 5,072 MB used against a 4,711 budget; run-time pictures 1,351 MB in 340 BGRA8 rows; Lumen 678; distance fields 463; shop fronts already compressed with mips. Step 1 first trial (Lumen 3584 / probe 16 by -Cvars, packaged): 160 MB saved settled; frame 11.6 against 10.9 ms in one run each.
- Kiln start check, try 2 (KILN-START-PLACEMENT-FIX-2026-11-16.md, engine copy F:/LedgerTools/tool-dev/kiln/engines/drapestudio/src, uncommitted there by design): limbs wrapped on their cross-section, most detailed mesh kept, stray pieces dropped; 17/17 tests; Tom's j3 better. Ron's trousers start (then slide to the ankles at the 10 mm stage); Ron's jacket and Darren's jacket refused at their collars (torso-height rule fitted on Tom; Darren's body file has no head or joints).

## Done the run before
- 14:07 to 14:52 (advisor 176 to 183, Kiln round 10, settings check, drive space, N=10 screen, bridge rewrite, breadth drapes try 1): git show c6b65dc11:production/handover/HANDOVER.md ('Done this run').

## In flight
- A helper (Opus, started 16:58 by the last session) is building packing step 2 in this repo: run-time pictures compressed at staging (BC1/BC5/BC3 beside each PNG, generalised import in VignetteShot.cpp, tools/bc1_pictures.py extended, stage_game_data.py), both targets, two editor screens (bc-hill, bc-hook). Its report: F:/LedgerTools/tool-dev/reports/PACKING-STEP2-2026-11-16.md. It may still be building when you start: check `Get-Process UnrealEditor*,Build*` and that report before any Unreal work; its edits are uncommitted in the working tree (read `git diff --stat`; do not stash or revert them).

## Next, in order
1. FIRST: verdicts after 2026-11-16T14:50:00Z; advisor after 2026-11-16T14:52+01:00 (all acked to 184). Hourly row due by 17:52.
2. Packing step 2: read its report when it lands; review with the gate (pictures beside the last good: lettering, dark gradients, normals), ci-checks, commit, push to wip by 00:30 so tonight's packaged build carries it and the walk measures it. If unfinished or failed, it is try 1 of 2.
3. Packing step 1 (Lumen atlas 3584, probe resolution 16): three packaged runs each, with and without (`tools/p1-packaged.ps1 -Only day-walk -Tag lumenhigh -Cvars "r.LumenScene.SurfaceCache.AtlasSize=3584,r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution=16"`; ~13 min each for the voice), only when no build runs; gate pictures hook and reverse; then into DefaultScalability.ini [GlobalIlluminationQuality@2]. The logo (T_GameAnimationSample_Logo, 18 MB) in the same walk.
4. Kiln: collar placement from the body's own neck (try 1; general, no special cases) and the slide-down at the 10 mm stage (trousers and skirt; try 1 used on the skirt), each through a helper per advisor 182; Darren's garment body needs a head or a joints file (search F: for his S6 body export first; else export one in Blender). Commit Kiln's engine changes where Kiln's folder keeps them (it is outside this repo).
5. Bridge live test once the heartbeat goes stale (alive at 16:40): dry run, then `schtasks /run /tn "LEDGER Marvelous open"`, read opens.jsonl and starts.jsonl. Close none of the four Marvelous copies.
6. n16-6: the packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 needs tonight's build (last night's copy 9ffd652 predates the switch).
7. cam_office screen (step 1's last acceptance) once no build or Kiln job loads the machine.
8. DAILY file by 19:00 with advisor 182's efficiency table (each improvement built/measured/not yet, with evidence and a day for the unbuilt), advisor 177's rows (hours logged against spend, session-start dollars against 15 Nov's US$15.83), 176's dollars against plan hours saved, 181's helpers' dollars per step by type and model, and `python tools/settings_check.py`. Space check by 23:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
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
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 0 of 2; slide-down at 10 mm 1 of 2 (the skirt's); packing step 2 1 of 2 (in flight).
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$10.70 from 14:09 to 14:45.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
