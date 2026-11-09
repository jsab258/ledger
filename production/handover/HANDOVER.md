# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-09 19:07
**Stopped:** 2026-11-09 18:18 (stopped on his word in the chat; the 15:31 session was stopped by him at 16:40 without a handover; this stop committed its finished work)
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 10 to 20 minutes before the next run, which fires at :21; past 400,000 too unless under 10 minutes to the run; past 550,000 whatever the clock; 9 Nov, advisor 52) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted by his tap 8 Nov 17:17; runs to 13:00 Monday 16 November). The order of 2 November's time ends 13:00 Monday 9 November.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, his anger 07:32, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; every session and all allowed helpers keep working on everything else; no session stops for the night. Space checked before the night build by 23:30. Six helpers while behind the line (his tap 07:17).
- Standing since his 8 Nov tap (RULINGS 6 Nov): the waiting list when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- **Every time stamp from PowerShell's Get-Date at the moment of writing, never estimated**.
- **Advisor 33 (19:55):** any hourly reading over 2 points behind the line: at once the session on Unreal work and four helpers on the order's no-Unreal parts, pulled forward in order, round the clock; the hour's row names what was pulled forward; within 2 points carry on; over 3 ahead, two helpers.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- **Never filmed (his word 08:35, 9 Nov, advisor 51):** he never films or performs anything; never propose it in any plan, item or report. Motion footage fallback and control: free online video whose licence allows commercial use and changes (Pexels, Pixabay; each site's licence read in full against the allowlist, each clip's source and licence recorded; nothing from sites forbidding download). Into RULINGS with his next tap.
- **Advisor 64 (9 Nov):** any session that ends a turn with no goal still running (a resumed old session, a pasted message answered) writes this file's Stopped line from Get-Date first. The gate now takes a session with no turn for 30 minutes and no background job of its own as stopped (120 while its job runs).
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Runs on 9 Nov (earlier: git log)
- To 12:30: Tom's close, whole and boots views passed fresh final reviews on played copy 09701ac (F:/LedgerTools/gate/new/tom-whole-2026-11-09/r3); the video runtime proven (TOOLS-2026-11-09.md); helpers' plans committed (phase 2 revised, the cooking plan, street life, door passage, Ron's costs, SHOTS-AND-PROMPTS, interpolator licences, GarmentCode, published numbers).
- 13:00 to 15:31 nobody worked: the hourly task named the 2 Nov order, whose time had ended. On his yes (15:30) the task's prompt now follows the newest adopted order; its copy is HOURLY-TASK.md, checked by tools/order_current_check.py (in ci-checks). DECISIONS has the line.
- 15:31 to 16:40 (stopped by him mid-run): the start-frame switches (-PageBackdrop, -PageDressIds, Tom's walk-proof start place and push lines), both targets built; Tom's start frame taken; motion 2 seed 1101 at 81 frames finished 17:30 (C:/LedgerTools/ai-video/out/m2-81f-s1101.webm, 6,015 s), not yet looked at. Four route notes from helpers (COMFYUI-ROUTES, PLUGIN-SOLVE-ROUTE, START-FRAME-ROUTE, WORKFLOW-STUDY). Progress page updated for phase 2. All committed at this stop (18:18) on his word.
- His page and advisor not read since about 16:40.

## Next, in order
1. Read his page's verdicts and advisor; act at once.
2. n09-2, Tom by Tuesday: his page with the four views (close, whole, boots from r3; the talk view), the walk 8 Nov and sit 6 Nov films reused, shortfalls first (collar edge, crown, boots read as slip-ons, plain jeans, smooth cloth); tonight's walk is the packaged pass.
3. n09-5 the office exit: tonight's walk runs the town's hours; copy its game log (F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Logs) before the morning pictures overwrite it; grep LedgerWalkOff for "out through the office door" and "cannot walk".
4. n09-8: check the 81-frame motion 2 clip (stills by Blender's sequencer: identity, feet, camera), then motions 3 and 1 with their start frames; RIFE to C:/LedgerTools/ai-video for 60 fps; the plugin's solve. If sd-cli unattended is refused again, his page.
5. n09-3: the cooking plan's step 3 (the shop-front import pass), then its packaged memreport check.
6. n09-7 the crown: Step 0 with its control; tries 5 and 6 under the amended rule.
7. The order's rest (n09-6 Sheila step 1 and the GarmentCode lab test, n09-9, n09-12).

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- An ack stamped 09:40 without Get-Date (9 Nov, true 09:29); corrected.
- The office exit read from a sit walk: the route never sends anyone out of a room, so it proves nothing about the exit (9 Nov 12:24); read tonight's walk instead.
- sd-cli run unattended: refused by the session's safety check (9 Nov 10:30); not worked round; he allowed it in the session.

## In flight (carried)
- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waits by its plan.
- The walkers' turn at a pause is unjudged in stills. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); FOR-JAFAR.md's one-line change is not this session's; untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: Flemish bond with burnt headers; the memory spike's fix if the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot (stop within talk reach or move the spot); the slate tile at about 394 px a metre against the 410 to 614 band; the street's 788 real asset faults by size; Tom's left foot in the turn into the run; the office's light wear and hard night light; the traps note's remaining proposals.
- Tries used: hair colour 2 of 2; worn paint 2 of 2; the office and sit on by default 2 of 2; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the tester's round 3 of 3 (his yes), spent; the dish 2 of 2, spent; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its fitted rules 1 (offline only); the clothes' release 1, passed packaged 9 Nov; Tom's turn foot 0 (old, listed); Tom's page-size talk view 1 of 2 (tester size), then the game's own picture; the office exit 1 of 2 (door route, seated flag), unproven (no walk-out in the sit walk); Tom's chest skin 1 of 2, passed review packaged 09701ac; the boots 5 (his yes), passed review packaged 09701ac; the crown 4, a fifth needs his yes; .
- API spend: US$1.17 (7 Nov); US$1.15 (8 Nov); none on 9 Nov to 13:00.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date.
