# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-11 05:21 (hourly run; the 00:22 session set no Stopped line, taken as stopped after 34 idle minutes)
(The session started 10 Nov 20:22 set no Stopped line; no turn for 76 minutes, taken as stopped by the gate; its background job still ran on the card at this start.)
**Stopped:** 2026-11-10 19:54 (history past its point at the Discord item's end; motion 2 filmed and reviewed, his tap acted on, scan sent; sd-cli still making motion 3 on the card, see Next 1b)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted by his tap 8 Nov 17:17; runs to 13:00 Monday 16 November). The order of 2 November's time ends 13:00 Monday 9 November.

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

## Runs on 10 to 11 Nov (earlier: git log, TRIED-ARCHIVE)
- 00:22 to 00:45: fresh start; page and advisor read, nothing new; row 2026-11-11-0023 v1; pace +6.3, light work only. Motion 1 try 2 ended and failed like try 1: set aside. Verdict row 00:48, pushed.

## Next, in order
1. FIRST: `python tools/pace_line.py <weekly %>` from get_usage (19:24: 24%, +7.1). Over 6 ahead: no new token-heavy work or helpers, but his priority items and card or processor jobs still run (his tap 19:28, RULINGS 7, 10 Nov).
1b. THE MOTION EXPERIMENT: DONE 11 Nov 00:48 (verdict production/research/ai-video-motion/VERDICT-2026-11-11.md, row 2026-11-11-0048 v2): keep the route for small gestures over clean bodies; no more card time on whole-body moves; a start-frame try for large moves only after research. Ack advisor 89 with it if not yet acked (check advisor-acks 2026-11-10-1840-89).
2. THE TEXTURING TEST (his yes 16:58; MAP-2026-11-10.md is the plan; verdict on his page Wednesday 12:00, or a row by then saying the evening). Next, in order: (a) jeans: after the night walk and from 04:30, film Tom packaged with -WearHeld=TomJeansTC beside the last good film without it , one fresh final reviewer; memory by memreport listtextures (T_TomJeansTC_*). (b) brick: build_mc2.py's out3/ into Unreal beside the street's brick (a card job: allowed now by his 19:28 tap), and beside Megascans Brick Wall Worn once his Fab tap lands. (c) timber: F:/LedgerTools/texture-tools/timber: wear_k0.85.json makes the mask; the cornice set aside and listed; next: Unreal beside today's paint-wood edges. (d) prop and Megascans: asked (fab-megascans-five-2026-11-10, five links); on Done, download through the Fab plugin. Advisor 82's rule: next RULINGS tap; apply it meanwhile.
3. n09-3 step 3: the re-import (four commandlets, order in production/research/frame-headroom/COOK-STEP3-CODE-2026-11-09.md), then the cooked-picture test in a packaged walk.
4. n09-2, Tom's page by Tuesday: after the night walk and from 04:30, film his side walk and sit on the new build, a fresh final reviewer each, then the page item with the three stills and two films, shortfalls first; NEEDS YOU after.
5. n09-5 the office exit: seated people never walk; the next step is a stand-up (A_sit stand clip, then StartWalkOff once off GSeated) before his LedgerDay move out of the office, an editor screen first, then the night walk's log.
6. n09-6: one bridge run of GarmentCode's md_job_workjacket.py, Sheila step 1; n09-9 the launch check on every pass; n09-12.

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- Motion 1, rise from a chair (set aside 11 Nov 00:42 after 2 of 2): both tries the man sat at the left edge despite the prompt, began to rise and faded out by frame 31 to 45, leaving only the chair (try 2: inputs/m1b, seed 2202, 100 min of card, sheet out/m1b-81f-s2202-t2v-frames/sheet.jpg). Text-to-video does not hold a figure through a rise at this model size; listed in the verdict row; a start frame (image-to-video) would be a new method, research first.
- Motion 3's solve (m3s1101, 41 min processor): feet hold (about 1 cm drift), jitter under 1 px, but the hands stop about 18 cm short of the face and both knees bend 20 to 25 degrees with the trunk leaning back, where the source stands straight; not usable as is, arm timing only (REVIEW-M3-FILM-2026-11-10.md). The source barely moves itself (hands rise about 2 cm).
- Clips over 81 frames lose the card (Vulkan device lost); 81 is the proven length (archive, 11 Nov).

## In flight (carried)
- The card is free since 00:41. C:/LedgerTools/ai-video/out holds the motion films and FBX (keep until the verdict).
- TomJeansTC: held test jeans in tonight's build (mh-assemble /Game/Ledger/MetaHumans/Garments/TomJeansTC); never released without his look; M_LedgerGarmentPacked now carries the WearMap branch (off unless WearOn).
- F:/LedgerTools/texture-tools (about 600 MB): tools, proof, jeans, brick, timber.
- C:/LedgerTools/mocap-solve: the CPU solve's scratch project (in use; holds m2s1101e's capture, performance and body clip).
- mh-assemble holds test assets in /Game/MocapSolve and /Game/CaptureManager/Imports/m2s1101*_1 (made by this session; nothing uses them).

## Kept as they are
- Uncommitted on purpose: this file, RECIPE.md's texturing lines and TRIED-ARCHIVE.md (commit with the next work); the office prints (copies on F:/LedgerTools/game-inputs); FOR-JAFAR.md's one-line change is not this session's; untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: Flemish bond; the memory spike's fix; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags; the hill's trees; the title backdrop's white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot; the slate tile's 394 px a metre; the street's 788 asset faults; Tom's left foot in the turn; the office's light wear and night light; the traps note's proposals.
- Tries used (older ones: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): the office exit 1 of 2 (door route, seated flag), unproven (no walk-out in the sit walk); Tom's chest skin 1 of 2, passed review packaged 09701ac; the boots 5 (his yes), passed review packaged 09701ac; the crown 4, Step 0 measured, listed known fault; the solve: commandlet 2, full editor 2 (GPU crash, then the CPU route passed 10 Nov); Drape Studio's jumper 2 of 2, spent (slid down the body both times); motion 3's clip 2 of 2 (passed at 81); motion 1's clip 2 of 2, set aside; the motion film tool 3 runs to working (tool work); texturing test: jeans masks 2 (game mesh, then high drape, passed offline), brick 2 (bond right, flat; then grain and edges, passed offline), timber edge wear 1 (cornice blotchy), the cornice 2 of 2, set aside, worn paint and edge chips: the timber chain is their third try, allowed by his 16:58 yes.
- API spend: US$1.15 (8 Nov); none on 9 or 10 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date.
