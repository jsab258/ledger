# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 18:22
**Stopped:** 2026-11-08 19:06
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 5 to 15 minutes before the next run, which fires at :21; or past 400,000 whatever the clock) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop.

## Standing ways of working (carry across every rewrite)
- Standing since his 8 Nov tap (RULINGS 6 Nov): the waiting list when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- The week's pace (his yes 7 Nov): over 6 points ahead, finish the item, write this file, stop. Now behind (77% at 15:50, 4.6 behind): full pace.
- **Advisor 28 (his words 13:55):** until Monday 07:00 keep up to FOUR helpers busy on no-Unreal work Monday's order needs; no busywork. **Advisor 29 (14:32):** Monday at full speed, session plus four helpers, until the 13:00 reset; read the meter at 12:50.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Run 18:22 to 19:06 on 8 Nov
- **Advisor 31 (18:15)** put to him as clothing-route-and-scans-2026-11-08 (yes recommended; acked). On his yes: the landscape-scan rule into RULINGS.md (cap 4,900: trim first), into n09-6 Epic's parametric outfits as backbone (Wednesday's resizing test) and a 2 to 4 h GarmentCode lab test (pygarment, MIT: check the allowlist first), and three scans this week by helpers (people in motion, hair, the crowd; about 1 h each). Waiting list until then.
- **n09-14:** try 2 sent with thinking off ("between_tools", Sonnet 5.5 thinks by default and spent try 1's limits); all 35 whole, US$0.51 (US$1.15 both). One review: 34 pass, Sheila's after cutting three content-rule lines (drink/gambling). Texts and ten canon points on his page as story-texts-canon-points-2026-11-08 (18:38). Order line updated; still open: most of the month's credit unused (ends about 11 Nov; today's ceiling about US$47).
- **n09-2 part:** survey of Tom's four views and the plan for his page: production/research/tom-whole-person/N09-2-SURVEY-2026-11-08.md (talk close-up is oldest, 4 Nov; jacket set aside).
- **n09-4 part:** production/research/phase2-plan/PIECES-DRAFT-2026-11-08.md drafted, reviewed once (pass with fixes), all twelve fixes applied by a helper (not yet read by the session): about 240 to 385 h without cars against the 2.00W ceiling (about 240 h); six open questions for him inside it. Not yet on the progress page or his page.
- Progress page republished (18:41, the new order, no carried items). Replay copies on F: deleted (about 460 MB; briefs and verdict kept). F: still 19.9 GB (needs 20) for the street sweep.
- Hourly row 18:42 (79%, pace -4.1, US$5.77 since 18:22). Pushed to wip, ci 97/97.

## Next, in order
1. His page and the advisor (open: keep-or-drop-2026-11-08, parked-cars-route-2026-11-08, clothing-route-and-scans-2026-11-08, story-texts-canon-points-2026-11-08; act on each tap as its item says); the hourly row.
2. n09-4: read the fixed draft once; put its open questions to him as at most three one-line taps (scope only; detail folded); then the pieces onto the progress page (progress_page.py and progress.json) with their weekly numbers.
3. n09-14: decide within the order whether more bulk text is worth the remaining credit before about 11 Nov (only text the order's items need; waiting list otherwise).
4. Tonight (no Unreal 01:15 to 04:30): read the walk (the dressed men's first walk, the iron cover, the office wall, the legs and launch lines); the day's summary's lines (the order adopted, jumper colours, the neckband, his taps, the clothes released, the side stories, phase 2's draft); stop before 00:45.
5. Monday, full speed to 13:00: n09-1 the exit in the morning (one fresh reviewer per exit on the newest build; production/audits/phase1-exit/CLOSE-BRIEF-2026-11-09.md); 12:50 the weekly figure; `needs_you_page.py --archive`; then n09-2 by the survey's plan (Tom on his page by Tuesday), n09-3 and on.
6. The street sweep's editor run once F: has room (after tonight's retention; `python tools/retention.py space --job "asset sweep" --drives CF` first).

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- Bulk batch on Sonnet 5.5 with no thinking setting (8 Nov 18:00): hidden thinking spent max_tokens; send thinking {"type": "between_tools"} (api_batch.py passes it).
- A content rule told as "never spoken of" still got "does not drink" (8 Nov): denials count; tell the model so.
- Counting nights from the folder list (8 Nov 15:00): count denominators from the files.
- A Python heredoc with "\b" lost its backslash (8 Nov 16:20, the memory's known trap): write such scripts with Write to the scratchpad.
- Rows claimed but never written (8 Nov 11:22 to 13:16): a row exists only when ArtifactData returns its version.
- The street sweep's editor run refused at 19.5 GB on F: (8 Nov 14:30 and 15:40): own unreferenced leftovers only about 0.2 GB; left alone.

## In flight (carried)
- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waits by its plan (next order).
- The walkers' turn at a pause is unjudged in stills. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept. This file rides with the next work commit.
- Waiting list for the next order, beyond the order file's own: Flemish bond with burnt headers; the memory spike's fix if the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot (stop within talk reach or move the spot); the slate tile at about 394 px a metre against the 410 to 614 band; the street's 788 real asset faults by size; Tom's left foot in the turn into the run; the office's light wear and hard night light; the traps note's remaining proposals.
- Tries used: hair colour 2 of 2; worn paint 2 of 2; the office and sit on by default 2 of 2; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; Mickey's window black 1 of 2, passed; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9b 2 of 2, passed; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its fitted rules 1 (offline only); the jumpers' knit 2 of 2, passed review and his look; Darren's neckband 1 of 2, passed review and his look; the stuck-legs line 1, passed review; the launch line 1, passed review with one fix; the clothes' release 1 (tonight's walk); Tom's turn foot 0 (old, listed); n09-14's batch 2 of 2, passed review.
- API spend: US$1.17 on 7 Nov; US$1.15 on 8 Nov (n09-14, two batches).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
