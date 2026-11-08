# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 09:22
**Stopped:** 2026-11-08 09:05
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 5 to 15 minutes before the next run, which fires at :21; or past 400,000 whatever the clock) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop.

## Standing ways of working (carry across every rewrite)
- His yes of 6 Nov 11:40, until 13:00 Mon 9 Nov: the waiting list's named items when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18).
- The week's pace (his yes 7 Nov): over 6 points ahead, finish the item, write this file, stop; a session starting over 6 ahead sets Stopped at once with one row.
- The six measures' table in each morning's overview (message 11; tools/token_measures.py).
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (phase 3's port, phase 5's research) (message 12).
- A standing way from the advisor is recorded here the same hour and named in its acknowledgement (message 13). Message 19, pacing to a line: on his page (keep-monday-share-2026-11-06), nothing acted on until his tap.

## This session (from 09:22 on 8 Nov), done
- His page and the advisor read at 09:24: nothing new since 07:45 (message 27 acknowledged by the last session). Row 09:26 (73%, pace 5 behind).
- The quay diagnosis's last two points read: quay-cast.json's -5 is the retired slice's, never loaded in play; the 8 Nov reverse picture shows nobody mid-road. Nothing to change.
- **n02-9-asset-check-gaps**, pushed 58c2305: tools/garments_shipped_check.py in the push checks (17 of 17 pass); street, kit, prop, shop and vehicle folders have budget kinds and a street-sweep piece (full report F:/LedgerTools/asset-checks, summary production/asset-checks/street-sweep-summary.json): 1,849 assets, 3,340 errors, mostly rule misfits, so failing the build on it waits for Monday's order (about half a day). Two tool faults mended on real files (memory: commandlets lack editor subsystems).
- **n02-9-record-caps** done, pushed cbe0dc5: doc-caps fails FINDINGS.md over 20 entries and this file over 1,800 words; FINDINGS merged 24 to 20, nothing dropped.
- The exit brief (CLOSE-BRIEF-2026-11-09.md) carries this morning's perf step (3b3454e: BELOW-60, 56.5 fps, 5,976 MB). Pushed.
- The sweep's 3,340 errors sorted for Monday (production/research/asset-checks/STREET-SWEEP-FIT-2026-11-08.md): about 2,580 misfits, about 700 real faults; one small review passed it with fixes, applied. Texture roles now read case-blind (misreadings 275 to 1; 145 packed maps on the wrong compression show as real; garments unchanged), in this stop's commit.
- Row 09:42 (74%, pace 4.2 behind). His page read 09:43: nothing new.

## Next, in order
1. The hourly row (last 09:42) and his page; pace and spend.
2. Waiting list under his weekend yes, nothing touching Unreal during the night's build and walk: candidates n02-9-flemish-brick (a look change: editor pictures and one review before tonight's build), n02-9-side-stories (25 to 40 for his page, Monday), or the fallback list.
3. Tonight: read the walk (the iron cover, Ron at 5.3, the office wall, the landing at the apron, Darren lost?); Sunday night's log lines into the brief; publish the progress page with the Tailor's interim line (tailor boss standing, not defeated: advisor message 27); stop before 01:40, no Unreal 01:15 to 04:30.
4. Monday: n02-3-4-exit in the morning; 12:50 the weekly figure; `needs_you_page.py --archive`; the Sonnet replay's folder on F:/LedgerTools/replay-2026-11-08 (about 0.5 GB, my own) deleted with one line after the order is written.

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- Times guessed three times this session (DECISIONS and the order got 09:45, 10:00, 10:05 when the clock read 09:35 to 09:56; all corrected). Run Get-Date in the same command that writes a time.
- The asset sweep (8 Nov): a -run=pythonscript commandlet has no StaticMeshEditorSubsystem (crash on the first static mesh); EditorStaticMeshLibrary answers -1 for unread counts, which passed every collision rule silently. Check a tool's readings against a known real value.
- Ron's back, 7 Nov: a signed nearest-surface distance to the head's open lower edge read 9.6 mm where the head is 6 cm away; check the unsigned distance first, measure from the side the fault is seen.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.
- People apart: the 0.6 m test had never fired on anyone dressed (IsHidden on the body, not the figure).

## In flight (carried)
- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waits by its plan (next order).
- The walkers' turn at a pause is unjudged in stills (the left walker turned toward the road, a slight backward lean, the 0156 walk's step-015). Sam's worst slip 51 cm, Lena's 49 cm: not looked at.
- Four editor picture runs on 5 Nov ended in a segmentation fault at exit after writing their pictures. Not looked at.

## Kept as they are
- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board), lasting copies on F:/LedgerTools/game-inputs; untracked shop-room files under production/art/shop-rooms are not this session's. Stash@{0} (06:10 editor-rebuilt material files) kept. Two Poly Haven sources on F:/LedgerTools/polyhaven.
- The corner's -PageShots in the editor: tools/ue/stage_game_data.py, copy vignette-pieces.json to ue-probe, then F:/LedgerTools/gate/new/street-level-2026-11-05/final/command-day.txt, MSYS_NO_PATHCONV=1, in the background; pictures in ue-probe/Saved/PageShots.
- The street's export: `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2; glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list for the next order, beyond the order file's own: Flemish bond with burnt headers; the memory spike's fix if the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit; the asset sweep's rules fitted to street pieces with a known list.
- Tries used: hair colour 2 of 2, set aside; worn paint 2 of 2, set aside; the office and sit on by default 2 of 2, the board's box passed; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; Mickey's window black 1 of 2, passed; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9b 2 of 2, passed; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its gate not tried.
- API spend: US$1.17 on 7 Nov, four -AskReal runs; none today so far.
- Report times: read Get-Date before writing one; never estimate a time.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
