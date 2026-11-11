# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-11 07:22 (hourly run)
**Stopped:** 2026-11-11 06:49 (history near its hard stop, 344k of 400k, after Tom's page item and the texturing verdict's brick row)
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

## Run on 11 Nov, 05:21 to 06:48
- Nothing ran 00:50 to 05:15: fresh_gate.py answers WAIT to every run from 00:45 to 05:10, against the round-the-clock rulings of 9 Nov; acked to the advisor (night checks 03:41, 04:40); on the waiting list, not changed (it codes his 4 Nov ruling).
- The cast's bind pose (night walk: Ron arms out; Lena, Sam, Rocco "0 parts that can speak"): the launcher's 5.8.4 update of 9 Nov dropped the MetaHuman plugin's Optional folder (diagnosis production/research/ron-apose). Fix try 1 of 2: our cooked A_stand_idle_MH as the idle list's last fallback (CrimeProbe.cpp kLiveIdles); packaged 0037444 logs all three playing it. Tonight's walk must confirm (the night report now names any cast member with no idle). The real fix is his: launcher-metahuman-content-2026-11-11 on his page (NEEDS YOU sent 05:55).
- Tom's page (n09-2): tom-whole-person-2026-11-11 on his page 06:45 (NEEDS YOU sent): the three stills of 9 Nov plus walk 422-458 and sit-crop 51-86 from build 0037444, each film passed by a fresh final reviewer (review-page/review.json in F:/LedgerTools/gate/new/tom-films-2026-11-11-b). Waiting for his tap.
- -FilmOnlyTom (new, CrimeProbe.cpp): hides everyone over 2 m from Tom each second; it did not run in the -TomSitProof mode (no log line) and kept an undressed Lena within 2 m in walk frames 1-120. Before the next film: call it where the sit proof ticks, or hide LedgerUndressed and placeholders whatever the distance.
- Texturing test (production/research/texture-pipeline/VERDICT-2026-11-11.md; row 2026-11-11-0650 v2): jeans decided, today's method stays (two fresh reviewers, clear winner; the first film was on a blank failed bake, fixed in garments.json; the garment check now fails flat maps). Brick filmed in the packaged street views (swap method: BRICK-FILES-2026-11-11.md): new better but not a clear winner, reads newly built; the shared brick waits for his look after a weathering pass.
- Fab item closed (answered done 20:49, 10 Nov).

## Next, in order
1. FIRST: pace from get_usage (06:50: 27%, +3.8, two helpers at most). Read his page: answers to tom-whole-person and launcher-metahuman-content; act at once (a yes on Tom: close the item, DECISIONS, n09-2 done in the order ledger; a no: his note to the waiting list unless broken).
2. Texturing test, the rest by this evening: (a) timber in the game beside today's paint-wood edges: trace the chandler front's paint files as BRICK-FILES did (a cheap extractor), then the same swap-for-one-run in the packaged copy, restoring after; one fresh reviewer; the cornice stays a listed shortfall. (b) the crate: from his Fab library through the editor's Fab plugin (memory: Fab needs Jafar signed in; a sign-in prompt becomes an ask, never a workaround), then beside the kit master. (c) finish the verdict file and one row.
3. n09-3 step 3: the re-import (four commandlets, COOK-STEP3-CODE-2026-11-09.md), then the cooked-picture test in a packaged walk.
4. n09-5 the office exit: seated people never walk; next a stand-up (A_sit stand clip, then StartWalkOff once off GSeated), an editor screen, then the night walk's log.
5. n09-6: one bridge run of GarmentCode's md_job_workjacket.py, Sheila step 1; n09-9 the launch check on every pass; n09-12 (UE4SS once per game, never beside Unreal).
6. Tonight: the walk tests the cast's fallback idle; read the report's new first line.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Jeans with the tool's wear mask (11 Nov): the first film used a flat 140-grey failed bake (chain-n7/baked-2048/jeans_colour_ao.png) and judged the wiring; on the fair film (chain-n7/details/baked-2048) the mask still shows no wear and loses seams and pockets, since it knows nothing of the pattern. Set aside as a garment method.
- -FilmOnlyTom in the sit proof: no effect (above).
- Motion 1, rise from a chair (set aside 11 Nov 00:42 after 2 of 2): the figure faded mid-rise; a start frame would be a new method, research first.
- Clips over 81 frames lose the card (Vulkan device lost).

## In flight (carried)
- TomJeansTC stays held, never released; it now draws the details-stage colour map.
- F:/LedgerTools/gate/new/tom-films-2026-11-11 and -b; brick-flemish-2026-11-11 (the swapped brick files' originals in originals/; the packaged copy restored 06:37).
- C:/LedgerTools/ai-video/out (motion films and FBX); C:/LedgerTools/mocap-solve scratch project; mh-assemble test assets in /Game/MocapSolve and /Game/CaptureManager/Imports/m2s1101*_1 (the session's, unused).
- F:/LedgerTools/texture-tools (about 600 MB). F: had 20.7 GB free at 06:16, just above its floor: check before any render.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: the start check's night window (00:45 to 05:10) against the round-the-clock rulings; the cast's look on our fallback idle if the launcher content stays off; Tom's trailing shoe in the about-turn; his soft-looking boots from the side; perching on the bench edge; the sit's hip skin flash (frame 50); the brick tile's weathering (soot, recessed grey mortar, arris wear, quoins); Flemish bond; the memory spike's fix; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags; the hill's trees; the title backdrop's white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot; the slate tile's 394 px a metre; the street's 788 asset faults; Tom's left foot in the turn; the office's light wear and night light; the traps note's proposals.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 1 of 2; Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 1, the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
