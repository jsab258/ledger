# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-08 08:22
**Stopped:** 2026-11-08 07:17
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop; his yes of 5 November). Each session runs `python tools/history_check.py` at the end of each item; when tools/history_check.py says OVER (since 5 Nov evening: past 250,000 tokens at an item's end falling 5 to 15 minutes before the next run, which really fires at :21; or past 400,000 whatever the clock; between the two it says UNDER, take the next item) it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Standing ways of working (the advisor's messages, within his rulings; carry this list across every rewrite; message 13)
- His yes of 6 Nov 11:40, until 13:00 Mon 9 Nov (RULINGS.md, DECISIONS 6 Nov 12:35; it stands over the task prompt's older words, which a scheduled run may not change): the waiting list's named items when the order's items wait; four helpers, none that may finish during a tester walk; work through the night with nothing touching Unreal from 01:15 to 04:30, stopping before 01:40 instead of 00:45, so nothing runs beside the walk (tools/fresh_gate.py holds starts till it reports). His schedule edit is done and checked (14:27): every hour, round the clock.

- While a session works, a short row to 'reports' at least once an hour, even when nothing is finished: what is in hand, what it waits on; the watchdog counts it as a sign of life (message 15).
- Stops line up with the next run: past 250,000 tokens stop only at an item's end 5 to 15 minutes before it; 400,000 hard (message 10; tools/history_check.py).
- The six measures' table in each morning's overview (message 11; tools/token_measures.py).
- Never stop a session for lack of work: when the item waits on a build or a review, the order's next item, then the fallback list (phase 3's port, phase 5's research); stop only at the size point or the night's Unreal jobs (message 12, point 1).
- A standing way from the advisor is recorded here the same hour and named in its acknowledgement (message 13).
- His yes of 7 Nov 07:07, the week's pace (RULINGS): at each start and each hourly row, read the usage tool and run `python tools/pace_line.py <percent>`. Over 6 points ahead: finish the item in hand, write the handover, stop; a session starting over 6 ahead sets Stopped and stops at once, one row saying so (the gate cannot read the meter).
- Each hourly row to 'reports' ends with the week's allowance, 'Allowance: 62% at 21:30': the session's own usage tool (mcp__ccd_session_mgmt__get_usage, deferred, Weekly all models), no picture or click, so every row (message 17). His aim: the week used close to 100% by Monday 13:00, not running out early. The card is his whole account, so beside it each row gives this session's and its helpers' list-price spend since the last row, `python tools/token_measures.py --spend HH:MM` (message 18): 'Allowance: 62% at 22:10, 0 since 21:27; my spend US$2.71 in that time'. Message 19, pacing to a line: on his page (keep-monday-share-2026-11-06), nothing acted on until his tap.

## The last session (06:22 to 07:18 on 8 Nov), done

- **Exit B's side-on film** (packaged, build 3b3454e): -TomWalkProof -TomWalkProofShots with 2 s spans, a picture each 1/30 s, F:/LedgerTools/gate/new/side-walk-2026-11-08 (side-walk.webp, 828 frames, sheet.jpg); measure as 5 Nov; about a third of frames bare wall (spans of 1 s would keep him in). Unreviewed, in CLOSE-BRIEF-2026-11-09.md line 23.
- **A speaker's sit-down**: -SitProof -MickeysInside failed never-seated on the same build (sit.log in speaker-sit-2026-11-08); sitting set aside 6 Nov, so not tried again; a speaker's walk and turn have no film tool: both named as gaps in the brief.
- **n02-9-iron-cover, try 1 of 2**: drawn cast tread (cover_iron, maps on F: game-inputs, gitignored), cover and frame fall with the footway, Ron's free-play spot 6.0 to 5.3; street re-exported and re-imported 179/179, both targets built, glass re-baked (16 windows); editor hook picture passed one small reviewer (F:/LedgerTools/gate/new/iron-cover-2026-11-08/review.json; mild shortfall: from the hook the lugs read close to a grille). Pushed to wip; tonight's packaged walk confirms.
- **n02-9-quay-end-stop read** (diagnoser): production/audits/phase1-exit/QUAY-END-DIAGNOSIS-2026-11-08.md: the hidden end wall (x -1.5 to -0.5) caused both stops; the spot (1, 0) works in one run (Ron at 1.04, 0.02), Darren held by the fish market railing's box; the ferry landing's 8 m trigger now reaches the rank (unchecked in play). Unwalked.
- Order notes: the three research proposals (QA, people alive, memory) were already made and reviewed overnight; their lines now say so. His page and the advisor read 07:05: nothing new. Rows 06:30, 07:17 (72%, pace about -5).
- A stray folder tree C:/c/Users/Jafar/AppData/Local/Temp/claude/... (empty now) was made by a Git Bash path handed to Python; its files moved to the scratchpad; the safety check refused removing C:/c, so it is his to delete (say so in the day's summary).

## First, in this order (the next session)

1. **The hourly row** (last 07:17) and his page (watch dressed-men-look-2026-11-08 and sonnet-blind-replay-2026-11-07: act at once on a tap); `pace_line.py`, `--spend 07:17`.
2. Name the stray C:/c folder in the day's summary's line for him (not yet written there).
3. Next work, nothing touching Unreal during the night's build and walk: the waiting list under his weekend yes; candidates: the quay spot's side effect (the ferry trigger at the rank) read in code; n02-9-pass-is-players-launch (a check that packaged passes ran on the player's launch line); the side-on film again with 1 s spans if the exit's reviewers want it. Else the fallback list.
4. Tonight: read the walk (the cover, Ron at 5.3, the office wall, Darren lost?), Sunday night's log lines into the brief; stop before 01:40, no Unreal 01:15 to 04:30.
5. Monday: n02-3-4-exit in the morning; 12:50 the weekly figure; `needs_you_page.py --archive`.

## Tried and failed, and why

- Hair's sky light: judged on one near middle frame; the same film at distance would have shown Darren's blond and Sheila's specks. Judge a setting at every distance and on everyone it touches before calling it.
- Darren's slits: pushed against the body file, which holds no head. Pose pictures draw cloth and body the same grey; they cannot show it.
- Hair's near colour: 'only the portrait tool restores the colour' was wrong: nothing to restore. Measure first. Light, not colour.
- Worn paint: flakes of geometry read as confetti at every cover and colour tried; far off, unseen. A chip needs a mask in the material, closed since 30 Oct.
- People apart: the 0.6 m test had existed since 2 November and never fired on anyone dressed: IsHidden on the body, not the figure. Why both walkers stop short of the quay's spot (-5, 0) at about x 0 is unread.
- The witnesses: taking people out of the lines alone changed almost nothing; the shop front's box was the cause. The nightly stage "onlookers" passed all along because it counts who was measured, not who was told. Rita, 3.9 m behind her own window, still cannot see Tom (the same box); left on purpose, since seeing means naming and reporting: for the exit's reviewer or the next order. Last night's six witness lines: lamp post C named as blocking at about 19 m, street_interior and the ironmonger's front at others.
- The hill's third try, inside the one try: the first far wood, big single masses, read as huge lumps; the second, tall trees, stood on stilts above the old crest; the third, lower, kept. Pulling leaves onto the hearts cures flecks but loses the broken edge: opaque leaf triangles at this range trade one fault for the other; a soft edge probably needs another method (cards or impostors, HILL-METHODS).
- The hill's gaps were real holes, proved with the haze off (`-ExecCmds=scalability 2,showflag.fog 0`).
- Flag stains: a mark's tint is multiplied by the picture's grey, a quarter; five drawn pictures with brown tints still measured an even grey darkening. The wet coat's reflection hides the colour. Drawing a stain again would be a third try.
- The sky's fog-off test: an unquoted -ExecCmds did nothing and looked like "fog has no effect"; quoted, sky and sea still barely moved, so the white was the dome and the sea's mirror, not haze.
- sea_specular first sat inside the TakesWater branch, which the sea never enters. The night's first values: saturated fill turned unlit brick pure red; the higher haze read as dusk.
- Step 9b's pipe: a scan of rust on white paint graded by its whole mean turned the paint blue; graded on the brightest quarter it reads as black iron.
- The dish's black wedge: not the arm, which moved while the wedge stayed put.
- Speech's third try: caching saves no time at this prompt size.
- The sit's drop: raising the pitch floor did almost nothing; measure before reasoning from a picture. The lift about the horizontal alone stands a turned, near-down head on its side. Levelling it exposed the head's quick turn.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.
- Ron's back, 7 Nov: a signed nearest-surface distance to the head's open lower edge read 9.6 mm through where the head is 6 cm away; check the unsigned distance first, measure from the side the fault is seen.

## In flight (carried)

- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waiting by its plan (next order).
- The walkers' turn at a pause is unjudged in stills: the left walker reads as turned toward the road in the 0156 walk's step-015, with a slight backward lean. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.
- Four editor picture runs on 5 Nov ended in a segmentation fault at exit after writing their pictures. Not looked at.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept. Two Poly Haven sources on F:/LedgerTools/polyhaven.
- For the corner's -PageShots in the editor: run tools/ue/stage_game_data.py, copy vignette-pieces.json to ue-probe, then the command in F:/LedgerTools/gate/new/street-level-2026-11-05/final/command-day.txt, MSYS_NO_PATHCONV=1, in the background; pictures in ue-probe/Saved/PageShots.
- The street's export needs `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2; copy the glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list (with n02-9-window-break's next try): n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-talk-cost-levers, n02-9-dress-the-cast, n02-9-session-model (his yes: one day on Sonnet under Monday's order), n02-9-window-break, n02-9-hair-card-colour. n02-9-dispatcher-voice made, unheard; Danny's and June's still wait on their page. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat, not a decal; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit.
- Tries used: hair colour 2 of 2, failed, set aside; worn paint 2 of 2, set aside; the office and sit on by default 2 of 2, the board's box passed; Darren's fit on S6 3 of 3 (his yes), passed review; Ron's hem 1 of 2, clean; Ron's collar 2 of 2 (points eased; the back made 8 Nov, passed review 04:44 on fa46ab0); the iron cover 1 of 2, small review passed (tonight's walk); the speaker's sit proof 1, not retried; the office camera in the walls 1 of 2, passed packaged 05:31 (small review; tonight's walk to confirm); the quay's spot 1 of 2, unjudged; the PCG count's start 2 of 2, passed; the tester's round 3 of 3 (his yes), 13 of 15, spent; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent, listed; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn at a pause 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses in the ladder 1 of 2; the hill 3 of 3, spent (his yes used); street-level wear's flag stains 2 of 2, listed, review rounds 2 of 2; the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 2 of 2, spent; the collar 4, set aside; 9a 1 of 2, passed; the gilt 1 of 2, passed; 9b 2 of 2 on the pipe, passed; 9d's wash 1 of 2, passed; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2, passed; 9d's roof breaks 2 of 2, passed; the undressed rule 2 of 2, passed.
- API spend: US$1.17 on 7 Nov, four -AskReal runs, each under its own US$0.60 cap; US$4.10 on 6 Nov.
- This stop came past 250k (254k), at an item's end before the 07:21 run; no helper running.
- Report times: read Get-Date before writing one. Slipped again on 7 Nov: the clock ran slower than this session guessed; never estimate a time.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
