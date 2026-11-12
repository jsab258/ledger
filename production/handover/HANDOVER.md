# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-12 22:37 (hourly run; gate GO: last stopped 20:29)
**Stopped:** 2026-11-12 23:51 (run 22:37: stopped at the history point).
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

## Run on 12 Nov, from 22:37
- Gate GO. Advisor 121 to 126 read and acked (eff not yet acked: item 1 done tonight, see below). No verdicts after 19:28Z.
- Done: the priority mark (advisor 126; `python tools/fresh_gate.py --priority-open ids` / `--priority-done`; production/handover/priority-open.json, ignored by git); SET NOW for 119 120 121: clear it only when his tools' rounds are done or set aside and his C: tap is acted on. C: survey (121): own leftovers deleted, Unreal's cache 7 days, one page item (c-drive-room-2026-11-12). Motionsmith round 1 and Loomwright hair round 1 (reports in production/research/tool-tests-2026-11/, plus TOOLCHAIN-FACTS.md, advisor 122). His picks 123 to 125: monthly model check in RULINGS; keys page item (talk-router-key-2026-11-12); the provider-neutral talk and bake-off on the 16 Nov waiting list. Today's 19:00 DAILY rows. Handover start (eff item 1): the gate's quiet time after a written stop is now 18 s, because the held quarter-hour run starts 30 to 50 s after a session ends (production/research/token-audit/HANDOVER-START-2026-11-12.md); check at this stop that the next run read GO.
- WRONG DELETE (mine, 23:02): C:/LedgerTools/ai-video/out held the real head-turn solve, its source video and the chair-rise control solve; no copy anywhere. Rule from now: grep the research notes for a folder's path before deleting it.

## Next, in order
1. FIRST: pace; verdicts after 2026-11-12T23:00Z, advisor after 22:25 Swiss (latest ack 126). Act on his two page taps (C: delete list; router key) at once. Ack eff after confirming the handover-start GO (idle_gaps' handover column), with the 19:00 rows.
2. Advisor 119/120 round 2, in order: Seamshift round 2 (Unreal scratch import of jumper_skinned.fbx, then his updates); Motionsmith round 2 (re-solve the kept stock clip, ai-video/stock/pexels-6615631, through tools/ue/mocap-solve-project, about 35 min of processor time, outside 01:15 to 04:30; then the head-turn and chair-rise jobs, the identity check, the stress clip); Loomwright hair round 2 (Darren's head and scalp exported from his MetaHuman, his reference photographs; groom on him in the editor); then Loomwright's cloth and streets. Each round: own time-log window; facts into TOOLCHAIN-FACTS.md; keep-or-drop for him after two or three rounds.
3. Advisor 118 while ahead: the CMU note's fresh review, then the method notes in DOUBLE-WEEK-PREP's order. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true.
4. d4a070b: confirm in tonight's walk log "shows its ... picture (..., BC1/srgb=yes)".
5. n09-12 (games' numbers, PC idle, no Unreal): UE4SS-READING-2026-11-12.md.
6. Nothing touching Unreal 01:15 to 04:30; space checked 23:00 (C: 47.8, F: 24.0 GB).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Vellum on Tom's jumper, 3 of 3 (his yes for the third): set aside. Cascadeur test 4, 2 of 2: set aside (quick rig needs rig mode on in a scene with the model alone; render to video crashes).
- Cutting video: no ffmpeg on this PC; Blender 5.2's video editor works headless (fit_method="FIT", media_type 'VIDEO' before FFMPEG; reverse frame by frame, its use_reverse_frames with offsets gave the wrong range).
- The test props' materials (12 Nov): read the render log for "Failed to compile Material" before judging any scripted material.

## In flight (carried)
- TomJeansTC stays held, never released. Session leftovers on F: and C: (tom-films, brick-flemish, ai-video/out, mocap-solve, texture-tools, drapestudio-test, pexels-6615631, metatailor 759 MB): as listed in git show a034fa9e1:production/handover/HANDOVER.md.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: as written at 10:25 (git show c8d0834c7:production/handover/HANDOVER.md, 'Kept as they are'), plus same-day packaged verdicts as an item (advisor 113), the provider-neutral talk program and its one bake-off (advisor 125), Drape Studio's cuffs, a per-piece worst-stretch check and cloth-on-cloth contact, and the true resize of Tom's jumper if he picks keep.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the test props' material compile 1 (passed); the scanned leak 2 (passed); the shop pictures' BC1 1 (passed, dark kept PNG); Cascadeur's start 0 (advisor 116: unresearched, does not count); the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; Sheila's colours 1 (fixed); her cardigan's left band 1 (passed); her blouse at the shoulders 1 (passed); her collar faults (c) passed at 2, (d) 2 of 2, set aside; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
