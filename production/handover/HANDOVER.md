# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-12 06:52 (hourly run)
**Stopped:** 2026-11-12 08:28 (run 06:52: crate closed; leak stain passed on try 2; one-picture shop rooms measured; Cascadeur set aside; his five answers acted on; history past its point)
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
- **Advisors 64 and 68 (9 Nov):** never end a turn while work remains: while a long job runs, work other items, read his page and the advisor every 15 minutes, check the job. A session ending a turn with no goal running writes Stopped first. The gate starts the next session after 30 quiet minutes even while a job runs, naming the job; that session leaves the card alone until it ends.
- **The Stopped line is the last thing a session writes (advisor 104, 11 Nov):** row and closing message first; turns after it hold the next start.
- **Advisor 91 (10 Nov):** the Monday numbers carry the builder's share of the account's weekly meter: its week's logged dollars divided by the dollars one meter point costs, measured in stretches when the builder ran alone (night hours; 9 to 10 Nov gave about 8 points for its logged spend), method and uncertainty stated; the rest of the points are everything else on his account.
- **The lean start's page reads, filtered (advisor 97, 11 Nov; measured: the three full listings cost about 10,000 tokens a start):** never list advisor, advisor-acks or verdicts whole, nor with out_dir. Two queries for the advisor: advisor-acks ordered by "at" descending, limit 1; then advisor where "at" is after that ack's. Verdicts: a query where "at" is after the last page read, written in UTC (verdicts' "at" is UTC, e.g. 2026-11-11T11:50 for 12:50 Swiss; a Swiss time in the filter hid his 12:28 taps for 20 minutes, 11 Nov). Advisor messages carry +01:00 times: filter those in Swiss time. Open page items by a filter on items.json (answered items now live in archive.json, never read at the start). The task file still says the old reads: editing it was refused by the permission check, so it is his to change.
- **Advisor 113 (12 Nov):** of two tools that do the job, prefer the one the builder can drive without clicks. MetaTailor clicks allowed for its free test (his tap 07:17); CMU motion capture on the licence list.
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

- **Advisor 111 (11 Nov 19:00):** before any second try on a fault, check the paid-tools sweep (production/research/paid-tools-sweep-2026-11-11.md) and research for a tool or method that already solves it. Monday's numbers: Sheila against Tom per garment and in total (hours, dollars, tries, set-asides, steps from a skill), and first-against-latest for every kind made more than once.
- **Launcher ruling (his tap 19:16, RULINGS 11 Nov, computer-use line):** the builder alone may click in the signed-in Epic launcher and fab.com in his Chrome, only to download his Fab library, add free items an order names, install engine updates and parts; each use a DECISIONS line.

## Run on 12 Nov, from 06:52
- Crate unit closed (packaged pass at build da19e5b, small review; tray found by eye). Pushed 4e3e4b8 [package] (green): M_LedgerStain's third way (UseColourAlpha) and shop rooms loading one picture of three: memory steady 5,541 to 5,172 MB, peak 5,873 to 5,538 (under 5,650). Same run's frame time 17.9 to 24.6 ms (GPU 15.7 to 22.7) while the PC was in use (input 2 min before); tonight's build re-measures: if it holds, diagnose the change (BindInteriorPicture, the stain material) before anything else.
- Leak test: try 2 passed (run-shaped scan leak_tculfbnc, 0.55 x 1.1 m under Mickey's gutter, east_parade_bay0, owner leak_test); pushed 5bf6b49 for tonight's walk. Known shortfall: faint at the hook camera.
- His page: all answered (CMU licence, MetaTailor clicks, advisor-relay ruling, program installs, nightly task off); 0 open; RULINGS at its cap 4,900. Advisor 113 acked.

## Next, in order
1. FIRST: pace (+5.0 at 07:34), verdicts after 2026-11-12T07:21Z, advisor after 07:17 Swiss (ack 113 at 07:33). Last row 07:34.
2. Tonight's build: the frame-time question above (perf line ue-perf-verdict.txt, gpuMedianMs against 15.7), memory again; the walk carries the leak.
3. n09-3 step 4 next: STEP4-NEXT-PLAN-2026-11-12.md (route A, compress at staging, shop pictures first); one fresh reviewer on the plan first; the engine's compressor via a commandlet before any new tool.
4. MetaTailor test (Sheila d), clicks allowed only after 10 minutes idle (he was at the PC around 07:40-08:20): carry Sheila's blouse and cardigan from Tom's body, count the clicks, compare with her refit's hours.
5. Cascadeur 4 and 5: set aside after 2 tries (empty ScriptsDir both ways); one researched different method (~2 h): a start-up argument or a script under the install's own resources/scripts (needs his yes if it writes under Program Files).
6. Motion: CMU licence now allowed (raw ASF/AMC or BVH for sitting and idles when an item needs it); advisor 107 (a) and (d) as written at git show a034fa9e1 (handover 5c).
7. Advisor "eff" DAILY at 19:00; before 23:30 the space for the night build; nothing touching Unreal 01:15 to 04:30.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- The scanned leak (12 Nov, try 1 of 2, passed on 2): a square scan whose coverage runs full width to its top edge prints a box unless tight under a ledge; first laid on a bay too far from any camera to judge.
- Cascadeur (12 Nov, 2 of 2, set aside): started directly and through Explorer, ScriptsDir empty both times; the build machine's write did not reach the settings Cascadeur reads.
- The test props' materials (12 Nov, passed on try 1's fix): masks through linear-colour samplers fail to compile silently in a commandlet; read the render log for "Failed to compile Material" before judging any scripted material.

## In flight (carried)
- TomJeansTC stays held, never released. Session leftovers on F: and C: (tom-films, brick-flemish, ai-video/out, mocap-solve, texture-tools, drapestudio-test, pexels-6615631, metatailor 759 MB): as listed in git show a034fa9e1:production/handover/HANDOVER.md.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: as written at 10:25 (git show c8d0834c7:production/handover/HANDOVER.md, 'Kept as they are'), plus same-day packaged verdicts as an item (advisor 113), Drape Studio's cuffs, a per-piece worst-stretch check and cloth-on-cloth contact, and the true resize of Tom's jumper if he picks keep.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the test props' material compile 1 (passed); the scanned leak 2 (passed); Cascadeur's start 2 of 2, set aside; the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; Sheila's colours 1 (fixed); her cardigan's left band 1 (passed); her blouse at the shoulders 1 (passed); her collar faults (c) passed at 2, (d) 2 of 2, set aside; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
