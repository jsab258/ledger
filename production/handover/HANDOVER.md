# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-11 11:22 (hourly run)
**Stopped:** 2026-11-11 10:25 (history 351k past its point after the surfaces item ended; handover uncommitted, the work's commit already pushed)
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
- **Advisor 91 (10 Nov):** the Monday numbers carry the builder's share of the account's weekly meter: its week's logged dollars divided by the dollars one meter point costs, measured in stretches when the builder ran alone (night hours; 9 to 10 Nov gave about 8 points for its logged spend), method and uncertainty stated; the rest of the points are everything else on his account.
- **The lean start's page reads, filtered (advisor 97, 11 Nov; measured: the three full listings cost about 10,000 tokens a start):** never list advisor, advisor-acks or verdicts whole, nor with out_dir. Two queries for the advisor: advisor-acks ordered by "at" descending, limit 1; then advisor where "at" is after that ack's. Verdicts: a query where "at" is after the last page read. Open page items by a filter on items.json (answered items now live in archive.json, never read at the start). The task file still says the old reads: editing it was refused by the permission check, so it is his to change.
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Run on 11 Nov, 09:22 to 10:30
- His launcher step done (tap 09:41, checked 09:46): Unreal 5.8.4, MetaHuman optional content 5.8 GB, engine source present; item closed. F: room: his yes, 29 own review folders deleted (6.3 GB, F: 24.6 GB); advisor 93 acked: such own leftovers need no page item from now on.
- Tom's surfaces try 3 (painted colour maps, tools/meshgen/paint_fabric_colour.py, maps in F:/LedgerTools/garments/tom/surfaces-2026-11-11/painted): whole view PASS, boots view FAIL (jeans pinstripe close up, the boots' welt pale and glossy, jacket unchanged): a new fault, no fourth try (RULINGS 7 Nov); set aside, rows back to the morning look, re-imported (garmentsShipped PASS), pushed 239a373b0. Reviews: production/research/game-clothing-pipeline/reviews/TOM-TRY3-*.json.
- import_garments.py: every import clears the instance's old overrides first (a restored row had kept try 2's grain: this morning's 08:58 restore may have shipped stale try-2 parameters until now); opt-in detail_off_tape.
- Sheila (helpers): step 0 (shared 32,334 layout, carry needed, S4 chest 795 / waist 814 / hips 920); step 1 blouse carried and skinned (F:/LedgerTools/garments/sheila/blouse-s4-2026-11-11; 5 collar points 3.5 mm in the head mesh); step 2 skirt carried and skinned with faults (band top ragged, 2 of 2 clear tries; walk 40 mm through the forward thigh; seated back through the chair, the known 29 Sep fault, routes costed in SHEILA-SKIRT-S4-2026-11-11.md, none chosen).
- GarmentCode work jacket: 18 pieces, 35 seams, kept on re-import in Marvelous (GARMENTCODE-LAB-2026-11-09.md); twist unseen until a drape. The bridge was alive (no UI start).
- n09-9: picture tools write launch.txt (launch_line_check.stamp); p1-packaged.ps1 films not yet.
- n09-6's resizing test (due today, Wednesday) not started: Unreal was blocked until 09:46.

## Next, in order
1. FIRST: pace (10:24: 30%, +4.8, two helpers at most); his page and the advisor.
2. n09-6: Epic's resizing test on Tom's garments (due today; plan RESIZING-READING-2-2026-11-09.md, nine steps), now that the MetaHuman content is back. Also confirm the cast's approved idle returns with the content (tonight's walk).
3. Sheila: the skirt's route is a choice after two failed fits: research one different method (about 2 h) or list it; step 3 cardigan from Tom's jumper game file (shared layout), step 4 shoes from Ron's boots; the blouse's head clearance (clear_layers --head); the binder's 40,000-triangle limit passed through skin_garment.
4. Before 23:30: space for the night build (F: 24.5 GB); nothing touching Unreal 01:15 to 04:30. The walk carries n09-3's re-import, n09-5's stand-up, the Tom switch.
5. n09-9: the launch stamp in p1-packaged.ps1's films; n09-12.
6. Morning: the walk report (cast idles), the stand-up lines, the memreport for n09-3.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Tom's surfaces by painted maps (11 Nov, try 3): denim streaks evenly spaced and continuous with no diagonal read as pinstripe close up; a dark jacket hides lightness speckle; a grain tile reaches the boot's welt. Three tuning passes on the welt changed nothing (cause misread). Listed for the next order.
- Tom's surfaces by shared tiles (11 Nov, 2 of 2): sheen chalked jeans, violet jacket; one roughness tile over every slot.
- Jeans with the tool's wear mask (11 Nov): set aside as a garment method.
- Motion 1, rise from a chair (set aside 11 Nov 00:42 after 2 of 2).
- Clips over 81 frames lose the card (Vulkan device lost).

## In flight (carried)
- TomJeansTC stays held, never released; it now draws the details-stage colour map.
- F:/LedgerTools/gate/new/tom-films-2026-11-11 and -b; brick-flemish-2026-11-11 (the swapped brick files' originals in originals/; the packaged copy restored 06:37).
- C:/LedgerTools/ai-video/out (motion films and FBX); C:/LedgerTools/mocap-solve scratch project; mh-assemble test assets in /Game/MocapSolve and /Game/CaptureManager/Imports/m2s1101*_1 (the session's, unused).
- F:/LedgerTools/texture-tools (about 600 MB). F: had 20.7 GB free at 06:16, just above its floor: check before any render.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: the texturing test's crate and phase 2's Megascans (his clicks in the Fab panel, one batch); the start check's night window (00:45 to 05:10) against the round-the-clock rulings; the cast's look on our fallback idle if the launcher content stays off; Tom's trailing shoe in the about-turn; his soft-looking boots from the side; perching on the bench edge; the sit's hip skin flash (frame 50); the brick tile's weathering (soot, recessed grey mortar, arris wear, quoins); Flemish bond; the memory spike's fix; Tom's head clamp in talk; Tom's jeans close-up weave, jacket cloth and boots' welt (surfaces set aside 11 Nov); the GarmentCode generator writing its output folder; Sheila's skirt band; Mickey's near front at night; stains on wet flags; the hill's trees; the title backdrop's white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot; the slate tile's 394 px a metre; the street's 788 asset faults; Tom's left foot in the turn; the office's light wear and night light; the traps note's proposals.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
