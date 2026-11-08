# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: production/handover/TRIED-ARCHIVE.md.

**Started:** 2026-11-08 11:22
**Stopped:** 2026-11-08 13:17
(His rulings of 4 November: the hourly task (ledger-daily-fresh-session) first runs `python tools/fresh_gate.py`, which reads only this file and the project's activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop). At each item's end `python tools/history_check.py`: OVER (past 250,000 tokens at an item's end 5 to 15 minutes before the next run, which fires at :21; or past 400,000 whatever the clock) means rewrite this file, set Stopped from Get-Date, stop.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop.

## Standing ways of working (carry across every rewrite)
- His yes of 6 Nov 11:40, until 13:00 Mon 9 Nov: the waiting list's named items when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18).
- The week's pace (his yes 7 Nov): over 6 points ahead, finish the item, write this file, stop; a session starting over 6 ahead sets Stopped at once with one row.
- The six measures' table in each morning's overview (message 11; tools/token_measures.py).
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (phase 3's port, phase 5's research) (message 12).
- A standing way from the advisor is recorded here the same hour and named in its acknowledgement (message 13). Message 19, pacing to a line: on his page (keep-monday-share-2026-11-06), nothing acted on until his tap.

## This session (11:22 to 13:16 on 8 Nov), done
- His page and the advisor read 11:22, 12:17 and 13:08: nothing new (message 27 already acknowledged; side-stories-2026-11-08 still unanswered). Rows 11:22 (74%, 5.1 behind), 12:17 (5.6 behind), 13:16 (6.1 behind; spend US$8.60 since 11:22).
- **n02-9-knit-and-neckband, built and passed review** (order line updated): garments.json's RonJumper and DarrenJumper carry the CC0 knit (detail tiling 2.0 and 1.8, strength 1.0), our rib as a second detail on the rib part (import_garments.py: DetailRibNormal, DetailRibOn off by default, so other garments draw as before), Ron navy 0.021/0.026/0.061, Darren maroon 0.115/0.013/0.019. Darren's neckband shortened to 22 mm above its seam (tools/meshgen/blender/lower_neckband.py; F:/LedgerTools/garments/darren/on_s6/darren_jumper_band). Round 1 (build 29d97de) failed both men on the rib running round the bands; the tile turned a quarter with its slopes (T_KnitRibAcross_Detail_Normal.png); round 2 (build 5ed8f38) passes both, no new fault. Films and reviews: F:/LedgerTools/gate/new/knit-2026-11-08 (r2/). Film script used: four packaged runs with -FaceAB -MouthFilm -PreparedAck -WearHeld=..., near and -MouthFilmWide -MouthFilmDeg=180/225/135 (the launch lines in each view's dress-test.log).
- **His look is on his page**: item knit-jumpers-look-2026-11-08 (added 13:15, yes recommended, four pictures), published version 57, items collection written. **The NEEDS YOU message for it is sent in this session's last chat message.**

## Next, in order
1. The hourly row (last 13:16) and his page: verdicts for side-stories-2026-11-08 and knit-jumpers-look-2026-11-08; act at once on a tap (close with `needs_you_page.py --close`, publish (read the live page and its items.json first), items collection "done", DECISIONS "HIS ANSWERS OF ..."; a yes on the jumpers: progress.json's Tailor stays standing with the interim line (advisor 27), the shortfalls stay listed; a note goes on the waiting list).
2. Order's items all wait or are done; the waiting list's next named items under his weekend yes, in the order file's order; else the fallback list (phase 3's port, phase 5's research). Nothing touching Unreal 01:15 to 04:30.
3. Tonight: read the walk (the iron cover, Ron at 5.3, the office wall, the landing at the apron, Darren lost?, and now the jumpers walked in build 5ed8f38 or later); Sunday night's log lines into the exit brief; publish the progress page with the Tailor's interim line; the day's summary's lines for today's decisions (the jumper colours; Darren's neckband lowered; the side stories and the jumpers on his page; the knit fetched, named as a download); stop before 01:40.
4. Monday: n02-3-4-exit in the morning; 12:50 the weekly figure; `needs_you_page.py --archive`; the Sonnet replay's folder on F:/LedgerTools/replay-2026-11-08 (about 0.5 GB, my own) deleted with one line after the order is written.

## Tried and failed, and why (newest; older ones in TRIED-ARCHIVE.md)
- The rib tile ran round the bands (8 Nov 12:30): a band's UVs need not run the body's way; turn a normal tile with its vectors (new R = old G, new G = -old R for a quarter anticlockwise) and check lit shading against the original turned.
- His page's publish was refused three times (8 Nov 10:33): the live page and its items.json must each be read in the session first (Artifact read, then read with path items.json), then the publish goes. Read both before the first publish of a session.
- The rib tile's first slope was garbled (0.037 instead of about 0.6): look at a lit preview of any generated normal before it counts.
- Times guessed three times on 8 Nov morning: run Get-Date in the same command that writes a time (this session's stamps were also a minute or two ahead and corrected).
- The asset sweep (8 Nov): a -run=pythonscript commandlet has no StaticMeshEditorSubsystem; EditorStaticMeshLibrary answers -1 for unread counts. Check a tool's readings against a known real value.
- Ron's back, 7 Nov: a signed nearest-surface distance read 9.6 mm where the head is 6 cm away; check the unsigned distance first.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.

## In flight (carried)
- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waits by its plan (next order).
- The walkers' turn at a pause is unjudged in stills. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.
- Four editor picture runs on 5 Nov ended in a segmentation fault at exit after writing their pictures. Not looked at.

## Kept as they are
- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board), lasting copies on F:/LedgerTools/game-inputs; untracked shop-room files under production/art/shop-rooms are not this session's. Stash@{0} (06:10 editor-rebuilt material files) kept. Poly Haven sources on F:/LedgerTools/polyhaven (now with knitted_fleece).
- The corner's -PageShots in the editor: tools/ue/stage_game_data.py, copy vignette-pieces.json to ue-probe, then F:/LedgerTools/gate/new/street-level-2026-11-05/final/command-day.txt, MSYS_NO_PATHCONV=1, in the background; pictures in ue-probe/Saved/PageShots.
- The street's export: `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2; glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list for the next order, beyond the order file's own: Flemish bond with burnt headers; the memory spike's fix if the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit; the asset sweep's rules fitted to street pieces with a known list.
- Tries used: hair colour 2 of 2, set aside; worn paint 2 of 2, set aside; the office and sit on by default 2 of 2, the board's box passed; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2; Ron's collar 2 of 2 (back passed review 8 Nov 04:44); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1; the office camera in the walls 1 of 2, passed packaged (tonight confirms); the quay's spot 1 of 2, unjudged; the landing's own place 1 of 2, unwalked; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses 1 of 2; the hill 3 of 3, spent; flag stains 2 of 2, listed; the night 2 of 2; the sky 2 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try; Mickey's window black 1 of 2, passed; the sit's drop 2 of 2; the collar 4, set aside; 9a 1 of 2; the gilt 1 of 2; 9b 2 of 2, passed; 9d's wash 1 of 2; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2; roof breaks 2 of 2; the undressed rule 2 of 2; the asset sweep's tool 2 runs to working, its gate not tried; the jumpers' knit 2 of 2, passed review; Darren's neckband 1 of 2, passed review.
- API spend: US$1.17 on 7 Nov, four -AskReal runs; none on 8 Nov so far.
- Report times: read Get-Date before writing one; never estimate a time.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
