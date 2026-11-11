# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-11 08:22 (hourly run)
**Stopped:** 2026-11-11 08:07 (history over its line, 270k, after the texturing verdict and the hourly row)
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
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Run on 11 Nov, 07:22 to 08:10
- Advisor 92 done: tools/fresh_gate.py runs round the clock for good (only the walk hold, 01:40 to its report or 03:30); a test sweeps 00:45 to 05:10 (commit 15dccba12, acked). Tonight's hourly runs should all go.
- n09-3 step 3: the four re-import commandlets ran clean 07:41 to 07:52 (40 glbTextures=OK, 6 PARTIAL with 1 to 3 unbound duplicates left, as the dry run said; logs F:/LedgerTools/tmp/cook-step3). Next: the cooked-picture test in tonight's packaged walk (memreport against MEMORY-WHERE-2026-11-08.md section 6), and whether asset_checks.py:867 now reads the fascias at 4096x512.
- n09-5 office exit, try 2 of 2 (commit c3ef4ff2b): a seated person asked to walk plays A_stand_up_MH (feet held, the idle back once the clip is in, the sit proof's slide), then StartWalkOff is asked again (BeginStandUp, StandUpTick; -NoStandUp turns it off). Game and editor targets build. Unproven: read tonight's walk log for "LedgerStandUp:" and "LedgerDay: ron walks"; a fault there is the last try, then set aside.
- -FilmOnlyTom is now its own step each frame before the phases (FilmOnlyTomTick) and hides anyone tagged LedgerUndressed at any distance, never actors attached to Tom. Untested: try it in the next Tom film.
- -ShopFrontSwap=<shipped>:<variant> (VignetteShot.cpp SpawnShopFront): draws a variant front imported beside the shipped one, for one run; logs ledgerShopFrontSwap.
- Texturing test finished (VERDICT-2026-11-11.md final): timber decided, today's wear stays (variant chandler-front-tcwear filmed in the editor's game, blind small reviewer: today's slightly, the tool's wear reads as piping; review.json in F:/LedgerTools/gate/new/timber-tcwear-2026-11-11). Crate: a manual step (Fab panel clicks), to the next order's waiting list. Proposed skill lines in the verdict (shopfront, street-weathering, game-garment) not yet applied: apply at most once today, in one edit.
- F: was 0.2 GB under its floor at 07:35; the pip download cache (286 MB) cleared, 20.1 GB free after: check again before tonight's build; ask him on his page if it fails (nothing else of ours is free to delete; gate/ is protected).
- No answers yet on tom-whole-person or launcher-metahuman-content (read 08:01).

## Next, in order
1. FIRST: pace (08:06: 28%, +4.1, two helpers at most); his page's answers and the advisor; act at once (Tom yes: close n09-2 in the order ledger with DECISIONS; launcher done: drop the fallback idle note).
2. Before 23:30: F: space for the night build (retention.py space); the night walk carries the re-import, the stand-up and the Tom switch; nothing touching Unreal 01:15 to 04:30.
3. n09-14: the API credit's month ends about today: close the item with its month's spend from production/api-spend.jsonl (US$1.15 of bulk text plus the 7 Nov talk runs) in the order ledger.
4. n09-6: one bridge run of GarmentCode's md_job_workjacket.py, Sheila step 1; n09-9 the launch check on every pass; n09-12 (UE4SS once per game, never beside Unreal).
5. Morning: read the walk report's first line (cast idles), the stand-up lines, and the memreport for n09-3.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Jeans with the tool's wear mask (11 Nov): the first film used a flat 140-grey failed bake (chain-n7/baked-2048/jeans_colour_ao.png) and judged the wiring; on the fair film (chain-n7/details/baked-2048) the mask still shows no wear and loses seams and pockets, since it knows nothing of the pattern. Set aside as a garment method.
- -FilmOnlyTom in the sit proof: no effect (fixed 08:00, untested).
- Timber with the generator's edge wear on the shipped front (11 Nov): outlines every moulding like piping; set aside, today's wear stays.
- Motion 1, rise from a chair (set aside 11 Nov 00:42 after 2 of 2): the figure faded mid-rise; a start frame would be a new method, research first.
- Clips over 81 frames lose the card (Vulkan device lost).

## In flight (carried)
- TomJeansTC stays held, never released; it now draws the details-stage colour map.
- F:/LedgerTools/gate/new/tom-films-2026-11-11 and -b; brick-flemish-2026-11-11 (the swapped brick files' originals in originals/; the packaged copy restored 06:37).
- C:/LedgerTools/ai-video/out (motion films and FBX); C:/LedgerTools/mocap-solve scratch project; mh-assemble test assets in /Game/MocapSolve and /Game/CaptureManager/Imports/m2s1101*_1 (the session's, unused).
- F:/LedgerTools/texture-tools (about 600 MB). F: had 20.7 GB free at 06:16, just above its floor: check before any render.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: the texturing test's crate and phase 2's Megascans (his clicks in the Fab panel, one batch); the start check's night window (00:45 to 05:10) against the round-the-clock rulings; the cast's look on our fallback idle if the launcher content stays off; Tom's trailing shoe in the about-turn; his soft-looking boots from the side; perching on the bench edge; the sit's hip skin flash (frame 50); the brick tile's weathering (soot, recessed grey mortar, arris wear, quoins); Flemish bond; the memory spike's fix; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags; the hill's trees; the title backdrop's white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot; the slate tile's 394 px a metre; the street's 788 asset faults; Tom's left foot in the turn; the office's light wear and night light; the traps note's proposals.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
