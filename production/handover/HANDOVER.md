# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-07 12:21
**Stopped:** 2026-11-07 12:07
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

## The last session (10:47 on 7 Nov), done

- **Windows restarted the PC at 00:14 and killed the 23:22 session** at its last turn (the event log; the advisor's message 20 said about 02:00). The start check then stood aside until he cleared it about 10:45, each WAIT run reading as activity to the next. Fixed in tools/fresh_gate.py, self-test 23 cases; acknowledged. **Its first real test is the next restart.**
- **His yes of 07:07, a tenth kept for Monday:** RULINGS, tools/pace_line.py, the standing way above. RULINGS at 4,799 of 4,800: anything new needs a line out first.
- **The night's walk (build e998e06):** 13 of 15, the tester's own: "lost sight of Sheila" at 0.93 m, a reading of the position file without Tom (inferred; not captured), and skipping her talk brought Tom to Darren in his hours at the docks. tools/route_walk.py reads again: **tonight's walk tests it; try 1 of 2.** People apart passed: closest 2.86 m, 0 of 83 frozen, 2 came to look.
- **The cached talk confirmed inside the game, US$1.17, stays on (TALK-LEVERS' last section):** cached 2.04, 1.67, 1.58 s, not cached 2.42 s; about 27% cheaper; fall-backs 3 of 113 against 0 of 76, kept against the old handover's "revert if worse" for its stated reasons (DECISIONS 11:40), so **watch the nightly bench's "that's all I know".** Pooled cached 1.78 s, 15 of 90 at 4 s or more. Speech stays set aside: **no rewording; the exit's reviewer judges all five runs.**
- **The corner's end page is on his page,** item corner-end-2026-11-07, open, NEEDS YOU sent 11:50. Its published look at phone width was not checked (the browser pane is signed out). Keep = close it by the skill; n02-4-corner-pages then done; his note, if any, goes on the waiting list unless it is the direction asked.
- **Marvelous's tutorials, a helper's first read (MARVELOUS-TUTORIALS-2026-11-07.md):** official: about 20 mm while dressing, under 5 mm finished; a T-pose for pose files. No collar method, no triangle counts. Read through a summariser, so its wording is the tool's: not primary reading by the rule, not reviewed; nothing rests on it.
- The day's summary, overview, progress page: all written late. `--spend` now reads across midnight.

## First, in this order (the next session)

1. **His tap on corner-end-2026-11-07,** the hourly row with allowance, `pace_line.py` and `--spend`.
2. **Tonight's walk, tomorrow morning:** 15 of 15 expected. Town-Sheila or Town-Darren failing again: try 2 of 2, read the tester's path first. **Card memory:** the perf line read 6,089 MB last night (5,844 at 17:45, 5,960 the night before), its first time over 6,000, with the voice's card model already lazy. Tonight's reading settles noise or not; if over 6,000 again, one diagnoser on what grew between 2af162e and 3b548c1, before the exit (his 6 GB line counts the game alone; the reading's own scope also to check).
3. **Sunday's summary and overview by 07:00 and 07:30,** shares and six measures; progress page; nothing Unreal 01:15 to 04:30; stop before 01:40.
4. **While nothing else is due, the fallback list, by the standing way:** the waiting list's named items under his yes (window-break's next try needs his yes first; hair-cards-vs-strands at Tom's camera and night's talk, not yet reached; session-model is for Monday's order, not now), phase 5's research. Port rows W3 to W6, U1, U5 change the game: after the exit. Nothing game-changing after Sunday's build, so the exit judges what was walked.
5. **n02-3-4-exit for 9 November,** run Monday morning on Sunday night's build by the brief, one final reviewer per exit, up to four helpers, the result on his page; its "to add" lines first (Exit C's five runs are in). Speech's missed bar as measured with the new runs beside, the jacket's collar, the sit's head swing, the rare freeze, and the corner reviews' list are listed. The lean start's quality counts: to 6 Nov in QUALITY-THISWEEK-2026-11-06.md, its Monday column to fill.
6. Monday about 12:50: read the weekly figure on the usage tool, before its 13:00 reset: `--allowance`. Monday `needs_you_page.py --archive`. When a try is set aside: `python tools/token_measures.py --thrown "what" --since HH:MM`.

## Tried and failed, and why

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

## In flight (carried)

- Corner step 9: 9a to 9d passed packaged in review (6 Nov); 9c waiting by its plan (next order).
- The walkers' turn at a pause is unjudged in stills: the left walker reads as turned toward the road in the 0156 walk's step-015, with a slight backward lean. Sam's worst slip 51 cm, Lena's 49 cm: not looked at.
- Four editor picture runs on 5 Nov ended in a segmentation fault at exit after writing their pictures. Not looked at.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept. Two Poly Haven sources on F:/LedgerTools/polyhaven.
- For the corner's -PageShots in the editor: run tools/ue/stage_game_data.py, copy vignette-pieces.json to ue-probe, then the command in F:/LedgerTools/gate/new/street-level-2026-11-05/final/command-day.txt, MSYS_NO_PATHCONV=1, in the background; pictures in ue-probe/Saved/PageShots.
- The street's export needs `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2; copy the glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list (with n02-9-window-break's next try): n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast, n02-9-session-model (his yes: one day on Sonnet under Monday's order), n02-9-window-break, n02-9-hair-card-colour. n02-9-dispatcher-voice made, unheard; Danny's and June's still wait on their page. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat, not a decal; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit.
- Tries used: the tester's position reading 1 of 2, unwalked; Martha's trousers 1 of 2, passed; the dish 2 of 2, spent, listed; people apart 1 of 2, passed; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn at a pause 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses in the ladder 1 of 2; the hill 3 of 3, spent (his yes used); street-level wear's flag stains 2 of 2, listed, review rounds 2 of 2; the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 2 of 2, spent; the collar 4, set aside; 9a 1 of 2, passed; the gilt 1 of 2, passed; 9b 2 of 2 on the pipe, passed; 9d's wash 1 of 2, passed; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2, passed; 9d's roof breaks 2 of 2, passed; the undressed rule 2 of 2, passed.
- API spend: US$1.17 on 7 Nov, four -AskReal runs, each under its own US$0.60 cap; US$4.10 on 6 Nov.
- This stop came at about 360,000 tokens, past the point, lined up with the next run; no helper running.
- Report times: read Get-Date before writing one. Slipped again on 7 Nov: the clock ran slower than this session guessed; never estimate a time.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
