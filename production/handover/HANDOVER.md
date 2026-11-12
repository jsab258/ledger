# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-12 02:21 (hourly run)
**Stopped:** 2026-11-12 01:37 (run 01:36: pace +6.3, over 6 ahead, so no new work; page and advisor read, nothing new since 20:26; nothing running)
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
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

- **Advisor 111 (11 Nov 19:00):** before any second try on a fault, check the paid-tools sweep (production/research/paid-tools-sweep-2026-11-11.md) and research for a tool or method that already solves it. Monday's numbers: Sheila against Tom per garment and in total (hours, dollars, tries, set-asides, steps from a skill), and first-against-latest for every kind made more than once.
- **Launcher ruling (his tap 19:16, RULINGS 11 Nov, computer-use line):** the builder alone may click in the signed-in Epic launcher and fab.com in his Chrome, only to download his Fab library, add free items an order names, install engine updates and parts; each use a DECISIONS line.

## Run on 11 Nov, 20:21 to 20:40
- Advisor 112: progress page republished (version 42), phase 2's bosses, efficiency bosses, hours to go; keep its data published nightly.
- The crate's offline chain done (VERDICT-2026-11-11.md, last section; F:/LedgerTools/texture-tools/crate): scan cut to 1024, TextureCraft green paint at 0.6 over the scan, edge wear (timber recipe) and dirt at 0.8, maps in out1024/; repeatable. Traps: dirt 0.5 shows nothing; paint at full opacity reads as plastic.
- Space for tonight checked: GO.

## Next, in order
1. FIRST: pace (stopped at +7.1: nothing new and heavy until back within 6), page verdicts (UTC filter after 19:38Z), advisor after 20:20 (Swiss).
2. The crate in Unreal beside the scan as it comes (FBX at F:/LedgerTools/texture-tools/crate/in/crate.fbx, maps out1024/ and as-it-comes/; no generic prop importer: import_cap.py's FbxImportUI pattern into a test path, editor pictures as screens), one small reviewer, card memory in a packaged walk. Then the other four downloads by the brick's and timber's tests.
3. Tool tests (PLAN-2026-11-11.md): Houdini Vellum test 2 (Tom's jumper against Marvelous, OBJ frames); MetaTailor (advisor 110: Sheila's blouse and cardigan carried from Tom's beside ours, same checks, time, clicks needed) once his account exists (check first; if not, a page item); Cascadeur tests 4 and 5: start route decided 02:35 (a module in a user folder on F: named by its ScriptsDir setting, written through the build machine; fallback his click; PLAN's last section).
4. Sheila (d): only the 7 Nov rule's one different method (MetaTailor or a Marvelous drape); then a fresh final reviewer and her page as a whole person, fault listed.
5. Advisor "eff" (19:45): DAILY-2026-11-12.md is started (interim from 01:00); at 19:00 rerun its three commands for the window to 19:00 (tools/idle_gaps.py and tools/shell_reads.py, new tonight), fill the rows, then: if handover waits pass 30 minutes a day, research an immediate next start (one tap, exact lines); pictures under 120; file reading against this tool's baseline 424,185 tokens (a one-tap guard if not down a third). Then ack "2026-11-11-1940-eff".
5b. Done 02:23: on his page (pause-nightly-answers-task-2026-11-12); close it on his tap.
5c. Advisor 107: (c) done 02:23: CMU's own terms read at source over plain http (commercial products allowed, no resale of the data); licence item on his page (cmu-motion-licence-2026-11-12), raw ASF/AMC or cgspeed BVH once he says yes. (a) Pexels 6615631 reversed (fallback Pixabay 165019): download, look at frames for whole body and feet, then the CPU solve beside the AI clip's (after 04:30).
6. Advisor 107's motion routes, one at a time (a, c, d as written there).
7. Before 23:30: space for the night build; nothing touching Unreal 01:15 to 04:30. n09-12 (UE4SS, never beside Unreal); n09-3 step 3 after Monday's exit.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Collar try 2 (11 Nov): a lift with a fixed 12 mm reach left points 17 mm under the knit, which show as strips in the game; set a lift's reach from the measured depth.
- The collar lift (11 Nov, try 1 on (c)/(d)): the shards are the cardigan's neckband above the collar, not under it; lifting the collar 2.5 mm moved 915 points (up to 14 mm) and left both faults.

## In flight (carried)
- TomJeansTC stays held, never released; it now draws the details-stage colour map.
- F:/LedgerTools/gate/new/tom-films-2026-11-11 and -b; brick-flemish-2026-11-11 (the swapped brick files' originals in originals/; the packaged copy restored 06:37).
- C:/LedgerTools/ai-video/out; C:/LedgerTools/mocap-solve; mh-assemble /Game/MocapSolve and /Game/CaptureManager/Imports/m2s1101*_1 (the session's, unused).
- F:/LedgerTools/texture-tools (about 600 MB); F:/LedgerTools/drapestudio-test-2026-11-11 (the retest).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: as written at 10:25 (git show c8d0834c7:production/handover/HANDOVER.md, 'Kept as they are'), plus Drape Studio's cuffs, a per-piece worst-stretch check and cloth-on-cloth contact, and the true resize of Tom's jumper if he picks keep.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; Sheila's colours 1 (fixed); her cardigan's left band 1 (passed); her blouse at the shoulders 1 (passed); her collar faults (c) passed at 2, (d) 2 of 2, set aside; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
