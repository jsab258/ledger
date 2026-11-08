# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 16:22
**Stopped:** 2026-11-08 16:06
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 5 to 15 minutes before the next run, which fires at :21; or past 400,000 whatever the clock) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop.

## Standing ways of working (carry across every rewrite)
- His yes of 6 Nov 11:40, until 13:00 Mon 9 Nov: the waiting list's named items when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- The week's pace (his yes 7 Nov): over 6 points ahead, finish the item, write this file, stop. Now behind (77% at 15:50, 4.6 behind): full pace.
- **Advisor 28 (his words 13:55):** until Monday 07:00 keep up to FOUR helpers busy on no-Unreal work Monday's order needs; no busywork. **Advisor 29 (14:32):** Monday at full speed, session plus four helpers, until the 13:00 reset; read the meter at 12:50.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## This session (15:22 to the stop on 8 Nov), done and pushed (last commit: the two self-tests in the build checks)
- His page and the advisor read 15:24 and 15:50: nothing new, nothing open on his page. Row 15:30 written (version 2).
- **n02-9-qa-lean step 2 done:** the night report says which launch the walk ran on (launch_line_check last_command_line/describe; route_walk's verdict "launch", only from a log written during this walk; nightly_walk's line). Real logs: the 4 Nov office log reads "a test launch: -mickeysinside", the 7 Nov walk PLAYER+WATCH. Small review passed with one fix, made. Step 3 (card memory at its peak) held for Monday (it changes the build's perf step).
- **The stuck-legs line's review:** code passed; my 15:00 numbers were wrong, corrected everywhere: fires on 16 of 20 nights with a path; Sheila's spot missed on 6 of 13 mornings since 24 Oct (five at 1.31 m, one 1.44 m).
- **Ron's and Darren's clothes were still held in the player's game** (garments.json hold "until a packaged walk and his page"; every dressed picture was a -WearHeld run), found by the office review. Released 16:30 after his two yeses: **tonight's walk is their first in the player's game; if it shows a fault, the hold returns.**
- Fresh reviews for the exit, both in its brief: the office by day and night (no new fault); Tom's side-on walk film (no slide or pop; the turn into the run's flat left shoe).
- Ron's plan: steps 1, 2 and 5 measured (unit-costs/RON-MEASURES, TALK-PER-PERSON); step 3, the audit's By person table.
- Notes for Monday: playbook/TRAPS-TO-CHECKS-2026-11-08.md (the cheap two now in the build checks, 97); phase5-procedural/OPEN-QUESTIONS-ANSWERS-2026-11-08.md.
- Tom's turn foot diagnosed: old (24 Oct), likely Epic's start clip; a known narrow shortfall.
- Progress page published 16:05 (version 34; the Tailor's interim line, the office's review); progress.json uncommitted, rides with the next work commit. Rows 15:30 and 16:07 written.

## Next, in order
1. His page and the advisor; the hourly row.
2. Helpers (up to four, no Unreal), only real work: the turn's foot fault's fix candidates are for Monday's order (no try spent yet); the traps note's remaining proposals wait for the order; the waiting list's inZOI and Silent Hill 2 file reads need F: room (19.5 GB, floor 20). If nothing real remains, fewer helpers, not busywork.
3. The street sweep's real editor run once F: has room (`python tools/retention.py space --job "asset sweep" --drives CF` first; after tonight's 03:30 retention, never 01:15 to 04:30): LEDGER_CHECK_PIECE=street-sweep through the commandlet (tools/ue/asset_checks.py docstring, full paths, MSYS_NO_PATHCONV=1), read its line (expect errors 0 and known about 788, or name the difference), then `python tools/ue/asset_checks.py --known-from F:/LedgerTools/asset-checks/street-sweep.json`; commit.
4. Tonight (the progress page is done; republish only if the walk changes a boss): read the walk (the iron cover, Ron at 5.3, the office wall, the landing at the apron, Darren lost?, **the two men dressed in the player's game for the first time**, the legs line and the new launch line); Sunday night's log lines into the exit brief; publish the progress page with the Tailor's interim line (advisor 27: tailor boss standing); the day's summary's lines for today's decisions (jumper colours, Ron's sheet, the neckband, his two taps, the knit download, the sweep fitted, the skills, the clothes released, the launch line); stop before 01:40.
5. Monday: full speed to 13:00 (advisor 29); n02-3-4-exit in the morning (the brief now holds the office's and the walk film's reviews); 12:50 the weekly figure; `needs_you_page.py --archive`; the Sonnet replay's folder on F:/LedgerTools/replay-2026-11-08 (about 0.5 GB, my own) deleted with one line after the order is written.

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
