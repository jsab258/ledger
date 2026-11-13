# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-13 08:52 (hourly run; gate GO: the last session stopped at 08:08)
**Stopped:** 2026-11-13 09:14 (run from 08:52: his router tap, Drape Studio re-test and Seamshift round 3 done; pace +8.8, over 6 ahead, so no new heavy work; rows 0900, 0915; verdicts read to 07:37Z, advisor to 09:13).
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted by his tap 8 Nov 17:17; runs to 13:00 Monday 16 November).

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, his anger 07:32, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; every session and all allowed helpers keep working on everything else; no session stops for the night. Space checked before the night build by 23:30. Six helpers while behind the line (his tap 07:17).
- Standing since his 8 Nov tap (RULINGS 6 Nov): the waiting list when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- **Every time stamp from PowerShell's Get-Date at the moment of writing, never estimated**.
- **Advisor 33 (19:55):** any hourly reading over 2 points behind the line: at once the session on Unreal work and four helpers on the order's no-Unreal parts, pulled forward in order, round the clock; the hour's row names what was pulled forward; within 2 points carry on; over 3 ahead, two helpers.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- **Advisors 64 and 68 (9 Nov):** never end a turn while work remains; while a long job runs, work other items and read the page and advisor every 15 minutes. A session ending a turn with no goal running writes Stopped first.
- **The Stopped line is the last thing a session writes (advisor 104, 11 Nov):** row and closing message first; turns after it hold the next start.
- **Advisor 91 (10 Nov):** Monday's numbers carry the builder's share of the weekly meter (its logged dollars over the dollars per meter point, measured on night hours when it ran alone), method and uncertainty stated.
- **The lean start's page reads, filtered (advisor 97, 11 Nov):** never list advisor, advisor-acks or verdicts whole, nor with out_dir. Two queries for the advisor: advisor-acks ordered by "at" descending, limit 1; then advisor where "at" is after that ack's. Verdicts: a query where "at" is after the last page read, written in UTC (verdicts' "at" is UTC, e.g. 2026-11-11T11:50 for 12:50 Swiss; a Swiss time in the filter hid his 12:28 taps for 20 minutes, 11 Nov). Advisor messages carry +01:00 times: filter those in Swiss time. Open page items by a filter on items.json (answered items now live in archive.json, never read at the start). The task file still says the old reads: editing it was refused by the permission check, so it is his to change.
- **Advisor 113 (12 Nov):** of two tools that do the job, prefer the one the builder can drive without clicks.
- Helper briefs on a person carry "person <name>".
- **Advisor 117 (12 Nov):** every garment's work gets its own time-log window named "garment: <wearer> <garment> <step>" (tools/timelog.py start), so Monday's numbers have measured hours. Next motion step when pace allows: the CMU library retargeted with Unreal's retargeter, research note first.

- **Advisor 111 (11 Nov 19:00):** before any second try on a fault, check the paid-tools sweep (production/research/paid-tools-sweep-2026-11-11.md) and research for a tool or method that already solves it. Monday's numbers: Sheila against Tom per garment and in total (hours, dollars, tries, set-asides, steps from a skill), and first-against-latest for every kind made more than once.
- **Launcher ruling (his tap 19:16, RULINGS 11 Nov, computer-use line):** the builder alone may click in the signed-in Epic launcher and fab.com in his Chrome, only to download his Fab library, add free items an order names, install engine updates and parts; each use a DECISIONS line.

## Run on 13 Nov, from 08:52 (this session)
- His tap 'router' (07:37Z) acted on: item closed, his key file in place (%LOCALAPPDATA%\LEDGER\router-key.txt), page republished with nothing open; the talk bake-off waits for the next order. Advisor 128 (Cascadeur stays) on the waiting list for 25 Nov.
- Advisor 129, Drape Studio re-test: his folder (now C:/Game Dev Tools/DrapeStudio; C:/DrapeStudio is gone) unchanged since before the 11 Nov test; one jumper run byte-identical to 11 Nov's; the rest not re-run. production/research/clothing-pipeline/DRAPESTUDIO-TEST-2026-11-13.md.
- Advisor 130, Seamshift round 3 (his 08:44 build): six of seven faults fixed and confirmed by our own measures; still failing Heavy sitting (328), front shoulder saw-tooth, small bare patch, README line; new: a pullover over a blouse loses up to 14% at a cuff and the crew band. 'Round 3' in production/research/tool-tests-2026-11/SEAMSHIFT-ROUND1-2026-11-12.md; preview seamshift-round3-2026-11-13.jpg. Round 1's cuff 'shrink by a third' was our script's measuring (corrected in the report and DECISIONS).
- Rows 0900, 0915; acks 128 to 130.
- Loomwright hair: the bare head is our Unreal picture's fault, cause not found (tries: 1, width).

## Next, in order
1. FIRST: pace; verdicts after 2026-11-13T07:37Z, advisor after 09:13 Swiss (latest ack 0857-130).
2. Advisor 127: his tools' next rounds start only when his folder for that tool changes (C:/Game Dev Tools/<tool>; compare dates). Each round: identity case, real inputs, the feedback's checks, beside the last round's numbers. For Loomwright hair first research (dated note) how an unbound groom draws in a SceneCapture2D and whether the Maya conversion flips it inside its bounds (compare guide points with the USD), before run 9. No keep-or-drop item yet.
3. Otherwise the order's work: advisor 118 while ahead (the CMU note's fresh review once pace is within 6, then the method notes in DOUBLE-WEEK-PREP's order). Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true.
4. n09-12 (games' numbers, PC idle, no Unreal): UE4SS-READING-2026-11-12.md.
5. Nothing touching Unreal 01:15 to 04:30. Tonight's walk: no game piece changed today (tool tests only, scratch).
6. Leftovers of mine: C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/motionsmith-r2, loomwright-r2 (ue to ue8 about 50 MB), loomwright-cloth, loomwright-street, seamshift-r3, F:/LedgerTools/drapestudio-test-2026-11-13 (keep while rounds continue).
7. Folder dates at 09:13 for the next rounds: DrapeStudio 11 Nov 10:14, Loomwright 12 Nov 13:26, Motionsmith 12 Nov 15:04, Seamshift 13 Nov 08:47 (round 3 done on it).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Vellum on Tom's jumper, 3 of 3 (his yes for the third): set aside. Cascadeur test 4, 2 of 2: set aside (quick rig needs rig mode on in a scene with the model alone; render to video crashes).
- The test props' materials (12 Nov): read the render log for "Failed to compile Material" before judging any scripted material.

## In flight (carried)
- TomJeansTC stays held, never released. Session leftovers on F: and C: (tom-films, brick-flemish, ai-video/out, mocap-solve, texture-tools, drapestudio-test, pexels-6615631, metatailor 759 MB): as listed in git show a034fa9e1:production/handover/HANDOVER.md.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: as written at 10:25 (git show c8d0834c7:production/handover/HANDOVER.md, 'Kept as they are'), plus same-day packaged verdicts as an item (advisor 113), the provider-neutral talk program and its one bake-off (advisor 125), Drape Studio's cuffs, a per-piece worst-stretch check and cloth-on-cloth contact, and the true resize of Tom's jumper if he picks keep; about 25 Nov (Cascadeur's trial end, advisor 128): uninstall or keep, by whether Motionsmith's next round fixes the leg rule, one line with a recommendation; the talk bake-off with the router key (in place since his 08:37 tap).
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the test props' material compile 1 (passed); the scanned leak 2 (passed); the shop pictures' BC1 1 (passed, dark kept PNG); Cascadeur's start 0 (advisor 116: unresearched, does not count); the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; Sheila's colours 1 (fixed); her cardigan's left band 1 (passed); her blouse at the shoulders 1 (passed); her collar faults (c) passed at 2, (d) 2 of 2, set aside; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
