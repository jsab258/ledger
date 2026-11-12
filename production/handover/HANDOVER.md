# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-12 12:52 (hourly run)
**Stopped:** 2026-11-12 13:02 (run 12:52: advisor 117 taken, garment hours reconstructed; pace +7.1, handed over). The gate at 12:52 reported a background job of the 10:22 run still running; no Unreal, Blender or Cascadeur was running: check its result first.
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
- **The lean start's page reads, filtered (advisor 97, 11 Nov; measured: the three full listings cost about 10,000 tokens a start):** never list advisor, advisor-acks or verdicts whole, nor with out_dir. Two queries for the advisor: advisor-acks ordered by "at" descending, limit 1; then advisor where "at" is after that ack's. Verdicts: a query where "at" is after the last page read, written in UTC (verdicts' "at" is UTC, e.g. 2026-11-11T11:50 for 12:50 Swiss; a Swiss time in the filter hid his 12:28 taps for 20 minutes, 11 Nov). Advisor messages carry +01:00 times: filter those in Swiss time. Open page items by a filter on items.json (answered items now live in archive.json, never read at the start). The task file still says the old reads: editing it was refused by the permission check, so it is his to change.
- **Advisor 113 (12 Nov):** of two tools that do the job, prefer the one the builder can drive without clicks. MetaTailor clicks allowed for its free test (his tap 07:17); CMU motion capture on the licence list.
- Helper briefs on one person carry "person <name>".
- **Advisor 117 (12 Nov):** every garment's work gets its own time-log window named "garment: <wearer> <garment> <step>" (tools/timelog.py start), so Monday's numbers and the Second Suit have measured hours. Motion: the 14B video route is dropped; next motion step (when pace allows) the CMU library, sit-down/stand-up and a lean, retargeted with Unreal's own retargeter, filmed packaged beside ours, research note first. Houdini on test for hair only (Darren's curls on its own renders first).

- **Advisor 111 (11 Nov 19:00):** before any second try on a fault, check the paid-tools sweep (production/research/paid-tools-sweep-2026-11-11.md) and research for a tool or method that already solves it. Monday's numbers: Sheila against Tom per garment and in total (hours, dollars, tries, set-asides, steps from a skill), and first-against-latest for every kind made more than once.
- **Launcher ruling (his tap 19:16, RULINGS 11 Nov, computer-use line):** the builder alone may click in the signed-in Epic launcher and fab.com in his Chrome, only to download his Fab library, add free items an order names, install engine updates and parts; each use a DECISIONS line.

## Run on 12 Nov, from 12:52
- Advisor 117 taken (ack 12:54): hours per garment reconstructed from commit gaps (Tom about 20 h, Sheila about 5 h), last section of MONDAY-NUMBERS-RAW-2026-11-12.md. Row 12:54. Pace +7.1, so the session handed over with no new heavy work.
- From the 10:22 run: Vellum 3 of 3 and Cascadeur test 4 set aside (notes in tool-tests-2026-11); Cascadeur starts with no click from C:/LedgerTools/cascadeur-portable (Trial to 25 Nov); test 5 not started. MetaTailor: method note and inputs ready (METATAILOR-METHOD-2026-11-12.md); his tap "done" 11:12 UTC seen, but computer use cannot be approved in a scheduled run: it needs a session he starts at the PC.

## Next, in order
1. FIRST: pace (+7.1 at 12:54: over +6, so no new token-heavy work or helpers until back within 6), verdicts after 2026-11-12T11:55Z, advisor after 12:30 Swiss (latest ack 117). Row 12:54.
1a. MetaTailor once he has allowed it (his page): the test as METATAILOR-METHOD-2026-11-12.md says, clicks after 10 idle minutes, build machine off.
2. d4a070b measured: steady 4,965 MB (was 5,172), peak 5,323, frame 17.05 ms (GPU 14.99); about 95 MB over Windows' budget. Confirm in tonight's walk log the line "shows its ... picture (..., BC1/srgb=yes)"; next for the gap: decals and scans.
6. n09-12 (game windows: only when the PC is idle and no Unreal runs): UE4SS-READING-2026-11-12.md: MIT; v4.0.0 is from today, so use an older proven release; support for SH2 (UE 5.1, unverified) and inZOI unconfirmed; one run per game, never beside Unreal, its files removed after.
7. Motion (advisor 117): CMU library route, research note first, when pace allows.
8. Advisor "eff" DAILY at 19:00; before 23:30 space for the night build; nothing touching Unreal 01:15 to 04:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Vellum on Tom's jumper, 3 of 3 (his yes for the third): set aside. Cascadeur test 4, 2 of 2: set aside (quick rig needs rig mode on in a scene with the model alone; render to video crashes).
- Computer use cannot be approved inside a scheduled run; any app beyond the task's settings needs his message in the conversation.
- Cutting video: no ffmpeg on this PC; Blender 5.2's video editor works headless (fit_method="FIT", media_type 'VIDEO' before FFMPEG; reverse frame by frame, its use_reverse_frames with offsets gave the wrong range).
- BC1 on dark night pictures (12 Nov, try 1): four colours a 4x4 block cannot hold a dark gradient; a checker shows on dark surfaces. Kept PNG.
- The test props' materials (12 Nov): read the render log for "Failed to compile Material" before judging any scripted material.

## In flight (carried)
- TomJeansTC stays held, never released. Session leftovers on F: and C: (tom-films, brick-flemish, ai-video/out, mocap-solve, texture-tools, drapestudio-test, pexels-6615631, metatailor 759 MB): as listed in git show a034fa9e1:production/handover/HANDOVER.md.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: as written at 10:25 (git show c8d0834c7:production/handover/HANDOVER.md, 'Kept as they are'), plus same-day packaged verdicts as an item (advisor 113), Drape Studio's cuffs, a per-piece worst-stretch check and cloth-on-cloth contact, and the true resize of Tom's jumper if he picks keep.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the test props' material compile 1 (passed); the scanned leak 2 (passed); the shop pictures' BC1 1 (passed, dark kept PNG); Cascadeur's start 0 (advisor 116: unresearched, does not count); the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; Sheila's colours 1 (fixed); her cardigan's left band 1 (passed); her blouse at the shoulders 1 (passed); her collar faults (c) passed at 2, (d) 2 of 2, set aside; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
