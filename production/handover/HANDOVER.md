# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 23:22
**Stopped:** 2026-11-08 23:27
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 5 to 15 minutes before the next run, which fires at :21; or past 400,000 whatever the clock) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted by his tap 8 Nov 17:17; runs to 13:00 Monday 16 November). The order of 2 November's time ends 13:00 Monday 9 November.

## Standing ways of working (carry across every rewrite)
- Standing since his 8 Nov tap (RULINGS 6 Nov): the waiting list when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- **Every time stamp from PowerShell's Get-Date at the moment of writing, never estimated**.
- The week's pace (his yes 7 Nov): over 6 points ahead, finish the item, write this file, stop. Now behind (79% at 19:28, 4.5 behind): full pace.
- **Advisor 28 (his words 13:55):** until Monday 07:00 keep up to FOUR helpers busy on no-Unreal work Monday's order needs; no busywork. **Advisor 29 (14:32):** Monday at full speed, session plus four helpers, until the 13:00 reset; read the meter at 12:50.
- **Advisor 33 (19:55):** any hourly reading over 2 points behind the line: at once the session on Unreal work and four helpers on the order's no-Unreal parts, pulled forward in order, round the clock; the hour's row names what was pulled forward; within 2 points carry on; over 3 ahead, two helpers.
- **Advisor 39 (22:45):** through the night four helpers busy on the order's no-Unreal parts in the order's sequence (n09-4's Gantt and forecast, n09-9, n09-10, n09-11, n09-13, GarmentCode, hair and people-alive research); each night row names what they ran; Monday 07:00 to 13:00 full speed, four helpers, aim near 100% at 13:00 with useful work only.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Run 23:22 on 8 Nov (earlier runs: git log)
- Page read 23:23: no new verdicts. Advisor 40 (more helpers when behind: six) acked; first in the morning batch as one tap, A recommended, his chat answer A noted; until his tap, four at most. Row 23:24 (version 1).
- The morning batch's records paste: the tools it touches found (post-commit backup hook, morning_pictures.py, token_audit.py's records pattern, doc-caps); CLAUDE.md at 1,622 of 1,625, so the paste must add no words net (written into the batch file).
- n09-10: the two skill additions reviewed (pass with four small fixes, all made, facts checked): N09-10-SKILLS-REVIEW-2026-11-08.md; DECISIONS 23:26. Still to be proven by their next repeat.
- n09-6: first reading for Wednesday's resizing test: outfits are baked to a skeletal mesh per character at build time in 5.8.2 (engine line checked), nothing resizes at run time; licence terms of Epic's Techwear outfit not reached; Parametric Asset Setup and Getting Started pages not reached: RESIZING-READING-2026-11-08.md.
- Waste: a helper repeated the study-13 check of the test plan, already done in c60e20c30 (the order's line had not said so); its file was restored, the line corrected. Search the commit log for a file's name before briefing.

## Next, in order
1. His page and the advisor; the hourly row. Monday's first page batch from production/approvals/needs-you/morning-batch-2026-11-09.md (advisor 40's helpers first, then hair, Marvelous task, unused tools, one combined CLAUDE.md paste for advisors 34 and 37), one NEEDS YOU message first; the hair pictures full size on the page after a fresh check (his-page skill).
2. The night: if a run starts before 00:45, helpers per advisor 39 only on short no-Unreal parts that finish by 00:30 (n09-6's resizing test plan from RESIZING-READING, the two unreached Epic pages first); stop before 00:45. No Unreal 01:15 to 04:30.
3. Morning: read the walk (the dressed men's first walk, the iron cover, the office wall, the legs and launch lines, the memory peak line); the overview by 07:30 with the token shares; the morning pictures.
4. Monday, full speed to 13:00: n09-1 the exit (production/audits/phase1-exit/CLOSE-BRIEF-2026-11-09.md); 12:50 the weekly figure; `needs_you_page.py --archive`; n09-2 by its survey (production/research/tom-whole-person/N09-2-SURVEY-2026-11-08.md); after the exit, Unreal: n09-3's cooking plan, n09-8's two code additions and film, n09-12's UE4SS run (not beside Unreal).

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- The editor commandlet from PowerShell (8 Nov 21:38): -EnablePlugins=A,B unquoted became an array and the editor never started; quote every argument. Not a try.
- The Marvelous bridge from a scheduled run (8 Nov 20:56, 21:00): Marvelous opened by script showed something in front of its menu; a scheduled run cannot be granted computer use to see it.
- Times guessed (8 Nov): up to an hour ahead of the clock; again at 20:50 and 21:15, and at 22:40 to 22:54 (all corrected). Get-Date before every stamp, no exceptions.
- The perf reader on a real capture read a 1.8-billion MB peak (8 Nov): the profiler's closing metadata row; only the real file showed it.
- The street sweep's editor run refused at 19.5 to 19.9 GB on F: (8 Nov): own leftovers only about 0.2 GB; left alone.

## In flight (carried)
- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waits by its plan.
- The walkers' turn at a pause is unjudged in stills. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); FOR-JAFAR.md's one-line change is not this session's; untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: Flemish bond with burnt headers; the memory spike's fix if the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit; the tester's morning run at Sheila's spot (stop within talk reach or move the spot); the slate tile at about 394 px a metre against the 410 to 614 band; the street's 788 real asset faults by size; Tom's left foot in the turn into the run; the office's light wear and hard night light; the traps note's remaining proposals.
- Tries used: the hair method test 1 (decided: strands); hair colour 2 of 2; worn paint 2 of 2; the office and sit on by default 2 of 2; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; Mickey's window black 1 of 2, passed; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9b 2 of 2, passed; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its fitted rules 1 (offline only); the jumpers' knit 2 of 2, passed review and his look; Darren's neckband 1 of 2, passed review and his look; the stuck-legs line 1, passed review; the launch line 1, passed review with one fix; the clothes' release 1 (tonight's walk); Tom's turn foot 0 (old, listed); n09-14's batch 2 of 2, passed review; the memory peak reader 1 (the metadata row found and fixed within it), passed small review.
- API spend: US$1.17 (7 Nov); US$1.15 (8 Nov); none since 19:22 (hair runs: stand-in talk).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date.
