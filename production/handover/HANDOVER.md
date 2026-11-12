# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-12 08:52 (hourly run)
**Stopped:** 2026-11-12 09:48 (run 08:52: shop pictures BC1, measured 4,965 MB; gate far-ahead wait; his method rule and its check; Ron's cost table reviewed; Cascadeur and Vellum method notes; history at its point)
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

- **Advisor 111 (11 Nov 19:00):** before any second try on a fault, check the paid-tools sweep (production/research/paid-tools-sweep-2026-11-11.md) and research for a tool or method that already solves it. Monday's numbers: Sheila against Tom per garment and in total (hours, dollars, tries, set-asides, steps from a skill), and first-against-latest for every kind made more than once.
- **Launcher ruling (his tap 19:16, RULINGS 11 Nov, computer-use line):** the builder alone may click in the signed-in Epic launcher and fab.com in his Chrome, only to download his Fab library, add free items an order names, install engine updates and parts; each use a DECISIONS line.

## Run on 12 Nov, from 08:52
- n09-3 step 4, second change: shop rooms' day and lit-night pictures block-compressed (BC1) ahead of time by our own encoder (tools/bc1_pictures.py, 40 to 46 dB; 3.8 MB instead of 30.4 each; files on F: game-inputs, staged only while newer than their PNG); the game reads them as PF_DXT1 (VignetteShot.cpp ImportBc1Texture), PNG as fallback. Dark night pictures stay PNG (4x4 checker on dark surfaces, first small review; try 1's fix). Plan reviewed first; game target built; pushed d4a070b [package].
- Advisor 114 done: the gate waits free after a clean stop while the last pace reading (pace-state.json, written by pace_line.py) is over +6, at most 2 h after the stop. Advisor 116 done: his method rule in RULINGS, checked by tools/method_line_check.py. Acks 114 to 116 written; last row 09:19.
- Ron's cost table reviewed (pass, five fixes made). Cascadeur's settings.json is read-only (the runner's write refused); the set-aside does not count (advisor 116).
- Commits 98c103b, cd0f763, b4e78bd were held locally while the build ran (a push mid-build could disturb it): push them (checks first) if not yet on origin/wip.

## Next, in order
1. FIRST: pace (+5.1 at 09:18), verdicts after 2026-11-12T08:35Z, advisor after 09:25 Swiss (ack 116 at 09:36). Push the held commits if still local.
2. d4a070b measured: steady 4,965 MB (was 5,172), peak 5,323, frame 17.05 ms (GPU 14.99); about 95 MB over Windows' budget. Confirm in tonight's walk log the line "shows its ... picture (..., BC1/srgb=yes)"; next for the gap: decals and scans.
3. The Vellum third try on Tom's jumper (his yes 09:11, advisor 115): start from production/research/tool-tests-2026-11/VELLUM-METHOD-2026-11-12.md (done: drape pre-roll with soft seam springs, gravity off, then weld; substeps 5; no published knit values, so match Marvelous's by test); the try as advisor 115 says, same checks and table against Marvelous j3 posed; jacket only if the jumper matches. Heavy local job: never during a build's perf step or the night's build and walk. Its verdict file needs 'Method researched:'.
4. Cascadeur: CASCADEUR-METHOD-2026-11-12.md: no documented command line or start hook; its docs put settings.json (ScriptsDir) in the install's resources folder (Program Files: his yes needed); free exports .casc only. Then two proper tries.
5. MetaTailor test (Sheila d), clicks only after 10 idle minutes and not while the build machine runs (its wait-for-PC step): Sheila's blouse and cardigan carried from Tom's body (F:/LedgerTools/garments/sheila/...), clicks counted, against her refit's hours. Needs its method note first (advisor 116).
6. n09-12: UE4SS-READING-2026-11-12.md: MIT; v4.0.0 is from today, so use an older proven release; support for SH2 (UE 5.1, unverified) and inZOI unconfirmed; one run per game, never beside Unreal, its files removed after.
7. Motion: advisor 107 (a) and (d) as before.
8. Advisor "eff" DAILY at 19:00; before 23:30 space for the night build; nothing touching Unreal 01:15 to 04:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
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
