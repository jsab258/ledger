# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 12:37 (the hourly run; the session started 11:54 set no Stopped line but wrote no turn for 39 minutes, so taken as stopped)
**Next due:** 2026-11-16 14:00 (the hourly row; last row 13:02)
**Stopped:** 2026-11-16 13:18 (history OVER at an item's end; all committed and pushed to wip; the Kiln round 10 helper still running, see In flight)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). The reset came at 13:00 today (meter 98% to 0%): the doubled line runs from 0 at Monday 13:00 to 95% by Wednesday 15:00, six helpers, full pace. week-shape.json's reset_at stays null until HE presses the spare reset (pace_line.py reads it for that press only).

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing.**
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page or the progress page: a publish is refused until the live page and each published file (items.json, progress.json) have been read in this session; read them to the scratchpad with out_dir, diff against the local copy, then publish.
- Advisors 111, 113, 117: paid-tools sweep before any second try; each garment its own time-log window.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Time log "tool loop: <tool> round n".
- **His pick A, 16 Nov 12:24 (advisor 174):** the breadth set's patterns come from FreeSewing and GarmentCode straight into Kiln's job format; Marvelous only for comparison drapes while its bridge is up; the bridge's auto-start fixed to recover by itself (dismiss a stray dialog, restart Marvelous in his signed-in session, retry) — that pick covers closing the Welcome window and restarting by script; the bridge is never raised on his page again. Own leftovers: deleted under RULINGS 29 Oct, never a page item (the page tool refuses one).
- **Held-back jobs never reach a fixer:** never name the two held-back garments in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).

## Done this run (12:37 to 13:10; commits b6cf8ce6c pushed, ac7eb0264 and this stop's commit)
- Advisor 173, 174, 175 acted on and acked. Four finished 12 Nov tool tests' outputs deleted (2.49 GB; F: 22.5 GB at 12:55). Page items f-room and marvelous-bridge closed; his page republished, 0 open. Page tool guard (needs_you_page.py selftest 15/15); retention limit for tool-tests-2026-11 and tool-dev/runs at 14 days, judge scripts, baselines and judge/ protected (dry check: 32 go in 15 days, 3 refused); RULINGS 29 Oct line points at both (4,900 of 4,900).
- Progress page published (version 43): week of 9 to 15 Nov, allowance 97% at 12:40 (closed at 98%), risks updated, phase 2 hours point 426 to 743 (last point less 21 h logged; not re-estimated), pictures to 16 Nov.
- n16-6: the game's own routing checked (no moment sent by the game; words-only rule plus deed and deal flags; newcomer questions to Sonnet 5, else Haiku 4.5). New measuring switch --core-model / LEDGER_TALK_CORE_MODEL in the talk helper (selftest 142/142); unset, as shipped.
- n16-1: job writers for Sheila's pleated skirt (tools/md-bridge/pleated_skirt.py, 233/233; GarmentCode fitted-skirt yoke, Penelope not installed; pleats as fold lines stitched at the yoke; Kiln has no pressing, no fold sign, no sitting drape) and Darren's nylon jacket (nylon_jacket.py, 117/117; drafted on Sam's C5 measures because S6 has no measurement file, draped on S6: the girth gap is unknown until S6 is measured in Blender). Jobs in F:/LedgerTools/garments/sheila|darren/kiln-breadth-2026-11-16/, not run.
- Bridge: heartbeat alive at 13:01 after the advisor's hand start (12:45). Diagnosis written: production/research/tool-tests-2026-11/BRIDGE-AUTOSTART-DIAGNOSIS-2026-11-16.md (cause most likely the Welcome window taken as the main window, start_bridge.ps1:94; four Marvelous copies running, lowest process picked; md_job.py:51's 90 s kill shorter than start_bridge.ps1:92-93's 120 s wait; starts.jsonl omits two results, :95 and :115).

## In flight (helpers launched about 12:56; their results arrive after this stop: take them from disk)
- **Kiln round 10 port** (Opus fixer, brief KILN-ROUND10-SPEED-BRIEF-2026-11-16.md from step 3; build target C:/LedgerTools/cargo-target; outputs F:/LedgerTools/tool-dev/runs/kiln-r10-*). Its report: F:/LedgerTools/tool-dev/reports/KILN-ROUND10-REPORT-2026-11-16.md. It uses the card: no local renders, Marvelous drapes or editor runs until no kiln/cargo process is left.
- **n16-3 step 2 C++: built and committed in this stop's commit** (both targets built by the helper; no editor or game run yet). Next: the editor screen once the card is free (no kiln/cargo process left): `"C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/Jafar/ledger-local/ue-probe/LedgerProbe.uproject" -game -LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle -ScaleTest=10 -ScalePeople=20 -PerfHook=stand -PerfHookCam=cam_scale_top -PerfHookShot -PerfHookShotName=scale-top -PerfHookFrames=300 -csvGpuStats -ExitAfterCsvProfiling -ExecCmds="scalability 2" -windowed -ResX=2560 -ResY=1440 -log=scale.log` (MSYS_NO_PATHCONV=1 from bash); then -PerfHookCam=cam_hill, then -PerfHook=walk -PerfHookRoute=scale. Accept per STEP2-DESIGN 'Acceptance' (nine copies on road lines, none over the street or approach, nonzero lights, picture MB, 20 people); ladder N=2, 4 first if memory pages.
- F: at 22.5 GB at 12:55 (floor 20).

## Next, in order
1. FIRST: verdicts after 2026-11-16T12:00:00Z; advisor after 2026-11-16T12:46+01:00 (all acked to 175). Hourly row due 14:00.
2. Take the two helpers' results (above). Kiln report: record the round in LOOP.md's way, time log, NOTEBOOK lines.
3. The bridge fix (n16-1, under his pick A): step 0 of the diagnosis (a bridge job probing Python's start-up hook) while the bridge is up, then the robust start (main window by handle, Welcome closed by a close message, the item invoked without opening menus, one Marvelous copy and one bridge, restart only a copy the task opened), md_job.py's timeout above 120 s, both starts logged. Test unattended per the diagnosis's plan. Close the extra Marvelous copies only if they are ones a task opened (never his).
4. Breadth: Kiln drapes Ron's jacket and trousers, Sheila's skirt, Darren's jacket once the card is free; measure S6 in Blender (F: room permitting) and re-carry Darren's jacket; Marvelous comparison drapes while the bridge is up. Ron's outfit plan steps 3 onward (straight-elbow body, boots proxy).
5. n16-6: the packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 for core moments (inside the day's API ceiling), against the shipped Sonnet 5, first-sound times and invented details; then other hosts wait on the router key (waiting list).
6. n16-3 step 1's acceptance (-PerfHookCam=cam_nope ends the game; cam_hill and cam_office screens) with step 2's editor screen above, card free.
7. The drive-space item: a costed lasting fix this week (per-run keeps, the new retention limits, and if still short a second drive's size and rough price as a money item on his page) (advisor 173).
8. The DAILY file by 19:00; space check by 23:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov: the bridge start's UI Automation search took the Welcome window for the main one (diagnosis, medium confidence); a mouse click on the menu item falls through to the toolbar, the keyboard route works (advisor 175). A scheduled run cannot be granted computer use.
- 16 Nov: a helper's 1.1 GB build took F: under its floor; build Rust on C:/LedgerTools/cargo-target.
- 16 Nov: a bash heredoc turned \b into a backspace in a Python regex (memory: patch backslash lines with a script file or Edit).
- 16 Nov: an unattended run may not edit the licence list or the project's settings.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the fix above is a genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed).
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$12.57 from 12:37 to 13:02.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run the scale test's editor screen while Kiln uses the card.
