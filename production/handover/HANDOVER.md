# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 17:22
**Stopped:** 2026-11-08 16:29
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

## Run 17:22 on 8 Nov: his new order adopted
- **His yes to adopt-order-2026-11-09 at 17:17 (verdict 16:17Z).** Done and pushed (6bdf73ccb, ci 97/97): production/orders/2026-11-09.md is the running order (n09-1 to n09-14, to Mon 16 Nov 13:00); every older open, carried and set-aside line closed in production/orders/archive/2026-11-09.md naming the n09 item or waiting-list line it folded into; nine groups nothing covers (K1 to K9) carried for his one keep-or-drop tap, **keep-or-drop-2026-11-08** (page version 60; items, ack and report rows written). On his answer: "yes" drops K8 and K9 (dropped, naming Jafar) and keeps the rest carried over; "keep-all" keeps all nine; then close the item.
- Section 1 is in RULINGS.md (4,894 of 4,900): tries up to four by the 7 Nov rule (none asks him), four helpers standing, models by the 8 Nov replay. **CLAUDE.md could not be edited from the automatic run (refused as self-modification):** its "70% production, 10% review, 20% kept" and "two tries means two" lines are stale; RULINGS wins meanwhile, as does it over the scheduled prompt's "a third needs his yes". Needs a desktop turn: put it with Monday's items on his page.
- The progress page's carried list is now empty (progress.json refreshed from the new order); republish tonight.
- n09-10 (skills) given to one helper at about 17:40 (notes: production/research/skills/N09-10-SKILLS-2026-11-08.md; skills under .claude/skills).
- n09-14: 35 requests (3 backstories, 32 side-story outlines, Sonnet 5.5) sent about 17:50 as one batch, worst case $0.66; its id in production/api-batches.jsonl: collect with `python tools/api_batch.py --fetch <id> production/research/bulk-api/n09-14/ANSWERS.jsonl --what "n09-14 ..."` (production/research/bulk-api/n09-14/BRIEF.md), then one review (Opus) against canon, then his page (story: the [invented] facts and five canon gaps: Ron's dock years 30 or 40, Sheila from 1959 before minicabs, Darren's bed, Mickey's age, a real town named in Darren's sheet). The text uses about $1 of about $190 left: 'credit near used' cannot be met by it; further use is a scope question for Monday's order.
- Hourly row written (stamped 18:15 in error; written about 17:45) (78%, pace -4.7, US$7.91 since 17:22).
- Earlier today, done and pushed: n02-9-qa-lean step 2; Ron's and Darren's clothes released into the player's game (16:30, his yeses): tonight's walk is their first; a fault brings the hold back.

## Next, in order
1. His page and the advisor (keep-or-drop-2026-11-08 first); the hourly row with its Allowance line.
2. n09-14's batch: fetch, review once, his page (above). n09-13 done: on his page as parked-cars-route-2026-11-08 (two open items now: that and keep-or-drop).
3. Tonight (no Unreal 01:15 to 04:30): read the walk (the dressed men's first walk, the iron cover, the office wall, the legs and launch lines); the progress page republished; the day's summary's lines (the order adopted, jumper colours, the neckband, his taps, the clothes released, the launch line); stop before 00:45.
4. Monday, full speed to 13:00: n09-1 the exit in the morning (one fresh reviewer per exit on the newest build; production/audits/phase1-exit/CLOSE-BRIEF-2026-11-09.md); 12:50 the weekly figure; `needs_you_page.py --archive`; n09-14 before the credit ends about 11 Nov; then n09-2 (Tom on his page by Tuesday), n09-3 and on in order.
5. The street sweep's editor run once F: has room (after tonight's retention; `python tools/retention.py space --job "asset sweep" --drives CF` first), as tools/ue/asset_checks.py's docstring says.
6. F:/LedgerTools/replay-2026-11-08 (about 0.5 GB, my own) deleted with one line.

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
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
- Tries used: hair colour 2 of 2; worn paint 2 of 2; the office and sit on by default 2 of 2; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; Mickey's window black 1 of 2, passed; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9b 2 of 2, passed; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its fitted rules 1 (offline only); the jumpers' knit 2 of 2, passed review and his look; Darren's neckband 1 of 2, passed review and his look; the stuck-legs line 1, passed review; the launch line 1, passed review with one fix; the clothes' release 1 (tonight's walk); Tom's turn foot 0 (old, listed).
- API spend: US$1.17 on 7 Nov; none on 8 Nov.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
