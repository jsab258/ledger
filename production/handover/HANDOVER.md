# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 20:22
**Stopped:** 2026-11-08 21:06
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 5 to 15 minutes before the next run, which fires at :21; or past 400,000 whatever the clock) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted by his tap 8 Nov 17:17; runs to 13:00 Monday 16 November). The order of 2 November's time ends 13:00 Monday 9 November.

## Standing ways of working (carry across every rewrite)
- Standing since his 8 Nov tap (RULINGS 6 Nov): the waiting list when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- **Every time stamp from PowerShell's Get-Date at the moment of writing, never estimated**.
- The week's pace (his yes 7 Nov): over 6 points ahead, finish the item, write this file, stop. Now behind (79% at 19:28, 4.5 behind): full pace.
- **Advisor 28 (his words 13:55):** until Monday 07:00 keep up to FOUR helpers busy on no-Unreal work Monday's order needs; no busywork. **Advisor 29 (14:32):** Monday at full speed, session plus four helpers, until the 13:00 reset; read the meter at 12:50.
- **Advisor 33 (19:55):** any hourly reading over 2 points behind the line: at once the session on Unreal work and four helpers on the order's no-Unreal parts, pulled forward in order, round the clock; the hour's row names what was pulled forward; within 2 points carry on; over 3 ahead, two helpers.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Run 20:22 to about 21:10 on 8 Nov
- His five taps (19:34) acted on: RULINGS within its cap (4,896: the field-scan rule widened by him; story drafts wait until built; page items at most two batches a day; the two shops built in phase 2); keep-or-drop K1 to K7 kept, K8 and K9 dropped (archive); the ten canon points as recommended; page cleared (0 open). Advisors 31 to 33 acked.
- Four field scans (production/research/field-scans): people in motion (reading: try Epic's experimental single-camera body capture, 3 to 6 h), hair (cards at play distance, strands in talk), the crowd (few near people, Epic's MetaHuman Crowds tried small, MB per person measured), cars (our own scripted hatchback; DECISIONS). Unreached pages marked there.
- **n09-4 done**: the PS5 gap list and the scoreboard on the progress page (published 20:35).
- n09-6: GarmentCode licence read; pattern code only (DECISIONS 20:40); lab test passed its own checks (four patterns, DXF exports read back): production/research/clothing-pipeline/GARMENTCODE-LAB-2026-11-08.md; files on F:/LedgerTools/garmentcode-lab. **The Marvelous import trial failed to start:** opened Marvelous 20:54; the bridge found no Plugins menu (a start-up dialog in front, unseen); computer use cannot be granted in a scheduled run; Marvelous closed 21:00.
- n09-9: study 13 read against the test plan, three changes, no check added. n09-11: the cache writes found (N09-11-CACHE-AND-TOOLS); the overview's cache line fixed (7 Nov US$35.28). n09-7: hair test plan written (production/research/hair/HAIR-TEST-PLAN-2026-11-08.md).
- Pushed c60e20c30 and ab608b335 (ci 97/97). n09-3: where card memory goes, read (MEMORY-WHERE-2026-11-08.md): the peak is hair strands' voxel texture plus run-time pictures.
- Rows 20:28 (-4.1), 21:02 (81%, -3.5).

## Next, in order
1. His page and the advisor; the hourly row. His page's next batch (at most two a day): (a) the unused connectors and skills to switch off in his account (N09-11-CACHE-AND-TOOLS finding 4, about US$35 a week); (b) Marvelous in the scheduled task's computer-use settings, or the import trial waits for a session he starts. Each with a NEEDS YOU message.
2. n09-3 by MEMORY-WHERE-2026-11-08.md (DECISIONS 21:06): its memreport capture in one packaged day walk, then cook the run-time pictures (about 0.8 to 0.95 GB); the hair voxel's 256 MB inside n09-7's test.
3. Tonight (no Unreal 01:15 to 04:30): read the walk (the dressed men's first walk, the iron cover, the office wall, the legs and launch lines, the memory peak line); the day's summary (his five taps and the rulings, the four scans, the hatchback route, phase 2's plan done, the cache line fixed, the GarmentCode result); stop before 00:45. F: was 18.3 GB free at 21:00, under its 20 GB floor, falling by itself (0.28 GB of it the lab): find the writer before any build.
4. Monday, full speed to 13:00: n09-1 the exit in the morning (production/audits/phase1-exit/CLOSE-BRIEF-2026-11-09.md); 12:50 the weekly figure; `needs_you_page.py --archive`; n09-2 by its survey (production/research/tom-whole-person/N09-2-SURVEY-2026-11-08.md); n09-7 by the hair test plan (about 95 min of Unreal); n09-3 and on.
5. The street sweep's editor run once F: has room.

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- The Marvelous bridge from a scheduled run (8 Nov 20:56, 21:00): Marvelous opened by script showed something in front of its menu; a scheduled run cannot be granted computer use to see it.
- Times guessed (8 Nov): up to an hour ahead of the clock; again at 20:50 and 21:15 (corrected).
- The perf reader on a real capture read a 1.8-billion MB peak (8 Nov): the profiler's closing metadata row; only the real file showed it.
- The street sweep's editor run refused at 19.5 to 19.9 GB on F: (8 Nov): own leftovers only about 0.2 GB; left alone.

## In flight (carried)
- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waits by its plan.
- The walkers' turn at a pause is unjudged in stills. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); FOR-JAFAR.md's one-line change is not this session's; untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: Flemish bond with burnt headers; the memory spike's fix if the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot (stop within talk reach or move the spot); the slate tile at about 394 px a metre against the 410 to 614 band; the street's 788 real asset faults by size; Tom's left foot in the turn into the run; the office's light wear and hard night light; the traps note's remaining proposals.
- Tries used: hair colour 2 of 2; worn paint 2 of 2; the office and sit on by default 2 of 2; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; Mickey's window black 1 of 2, passed; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9b 2 of 2, passed; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its fitted rules 1 (offline only); the jumpers' knit 2 of 2, passed review and his look; Darren's neckband 1 of 2, passed review and his look; the stuck-legs line 1, passed review; the launch line 1, passed review with one fix; the clothes' release 1 (tonight's walk); Tom's turn foot 0 (old, listed); n09-14's batch 2 of 2, passed review; the memory peak reader 1 (the metadata row found and fixed within it), passed small review.
- API spend: US$1.17 (7 Nov); US$1.15 (8 Nov); none since 19:22.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date.
