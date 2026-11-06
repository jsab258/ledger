# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-06 11:22
**Stopped:** 2026-11-06 06:07
(The session started 06:21 set no Stopped line; no turn written for 175 minutes, taken as stopped.)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop; his yes of 5 November). Each session runs `python tools/history_check.py` at the end of each item; when tools/history_check.py says OVER (since 5 Nov evening: past 250,000 tokens at an item's end falling 5 to 15 minutes before the next run, which really fires at :21; or past 400,000 whatever the clock; between the two it says UNDER, take the next item) it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Standing ways of working (the advisor's messages, within his rulings; carry this list across every rewrite; message 13)
- His yes of 6 Nov 11:40, until 13:00 Mon 9 Nov (RULINGS.md, DECISIONS 6 Nov 12:35; it stands over the task prompt's older words, which a scheduled run may not change): the waiting list's named items when the order's items wait; four helpers, none that may finish during a tester walk; work through the night with nothing touching Unreal from 01:15 to 04:30, stopping before 01:40 instead of 00:45, so nothing runs beside the walk (tools/fresh_gate.py holds starts till it reports). The schedule's own hours wait on his hands: hourly-round-clock-2026-11-06 on his page.

- Stops line up with the next run: past 250,000 tokens stop only at an item's end 5 to 15 minutes before it; 400,000 hard (message 10; tools/history_check.py).
- The six measures' table in each morning's overview (message 11; tools/token_measures.py).
- Never stop a session for lack of work: when the item waits on a build or a review, the order's next item, then the fallback list (phase 3's port, phase 5's research); stop only at the size point or the night's Unreal jobs (message 12, point 1).
- A standing way from the advisor is recorded here the same hour and named in its acknowledgement (message 13).

## Since 11:22 (this session)

- **The app was signed out from about 07:30 to 11:05** (advisor's message 14); the 06:21 session was cut off with no Stopped line. About 3.5 hours lost: name them in tomorrow's summary. Its uncommitted Stutter records (DECISIONS 07:17 and 07:30, the at-risk row, the order's line, NOW, runs.jsonl, the diagnosis file) are kept and go with this work's commit.
- **Its test finished: five walks with the game's voice program off, 0 frames over 33 ms, worst 22.3 to 25.2 ms** (runs.jsonl, labels *-gamenovoicea to e), against 3 of 4 and 3 of 3 walks over the line before. The program is the trigger.
- **The Stutter, try 1 of 2, in hand:** voice-server.py loads the card's model only at the first line Pocket and Sopro do not take; copied to F:/LedgerTools/voice-portable for the local measure.
- His page: whole-allowance-2026-11-06 raised, yes recommended (message 12, point 2), NEEDS YOU sent.

## Done before that (05:22 on)

- **Day's summary, overview (token shares, six measures), read-back by hand, progress page (its bosses brought up to date by hand, they stood at 3 Nov) all done for 6 Nov.** Commits c5704d319, 00bead1a8, pushed; ci-checks failed=none.
- **The 5 to 6 Nov night, build 3641d53, all of Thursday's work:** walk 15 of 15, so the tester's morning fix (`morning_step`) held: done. 57.7 fps, worst frame 23.27 ms, card 5,960 MB (5,952 before): under the 6 GB line; no cut made. LedgerGilt and LedgerStainless log "worn as metal". 0 of 163 frozen; 11 walks set off, all stood; "2 of the street's people come to look at the window"; Lena Notice 0.40; Rocco and Sam showed they knew.
- **The corner's packaged views passed**, fresh final reviewers: F:/LedgerTools/gate/new/corner-packaged-2026-11-06 (all ten pictures, review-hook-day.json, review-hook-night.json, review-reverse.json). Work matches the editor within 0.2 of 255. Three flags judged not faults: the kiosk woman wears beige trousers (cam_B-day); the lamp woman stands beyond the stack that hides her legs (cam_reverse-day); a walker's backward lean, narrow. These pictures are the corner's end page's starting material. Not passed against the bar (not narrow): Mickey's near-black window and dark night front, hill crowns, stretcher bond, few people and no cars, empty far end, the road's pale band, the sea at night a smooth brown band, the Ironmonger's corner very dark at night.
- **People apart, try 1 of 2:** Rocco and Sam stood 41 cm apart at D0 17:00, both stopped short of the quay at about (0, 1.7). StandBlockedAt skipped anyone whose body IsHidden, and a dressed person's body is hidden from the start, so its 0.6 m test never saw them; it now asks the figure. Both targets built, pushed; unproven until tonight's walk.
- **Sitting set aside, its face met** (order updated): packaged film F:/LedgerTools/tmp/ai-tester/film/2026-11-06-0553, face at most 10 degrees down, nothing touched, crown-on head gone. One fresh final reviewer: head side-on at frames 19 to 22, swinging front by 24, about half a second, perhaps the copied motion newly on show; Ron's fingertips through his shorts at frame 68. Listed for the exit; named in the summary. The route's talk-open FAIL in --sit runs is that route's own (Sheila out of reach, same in the editor).
- **A walk that cannot start now logs what stops it** (StartWalkOff); `tools/corner_people.py` prints those lines and the closest two standing. No behaviour change. The exit's brief is filled with the 6 Nov evidence; each "to add on the 9th" is the latest night's.
- Rita's broken window on the waiting list (n02-9-window-break). Slips recorded in DECISIONS: nightly_package.py run with a help flag (it did nothing: played copy current; origin/wip unchanged), timelog.py with no arguments, a guessed tool name. A helper stopped another helper's waiting process and made stray temp files, removed; briefs now forbid stopping processes.

## First, in this order (the next session)

1. Your start: the verdicts and the advisor channel. Read 06:07, nothing new (messages to 11; nothing open on his page). The advisor's messages all have acknowledgements through 11, taken from the old handover.
2. **Before tonight's build, little in the game can be judged.** What can move today, in this order:
   a. The lean start's quality counts (B) for Monday's overview: only this week's, counted as production/audits/lean-start/QUALITY-LASTWEEK-2026-10-27.md counted last week's; that file exists, do not count last week again.
   b. The advisor's message 10: late today or tomorrow morning report idle minutes, sessions, cost per step, start and end share beside 5 Nov's in 'reports' (`python tools/handover_cost.py 2026-11-06`; 5 Nov: idle mean 44 min, 577 in all, a start US$1.06, end US$0.66, 42% of the day), and move 250,000 or 400,000 if they say so.
   c. The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from today (last build coldCookMinutes=3.6, coldBuildMinutes=3.3; read production/d1-probe/ue-build.txt in git history for the rest).
   d. Then corner work under his note of 4 Nov, his order: night readability and Mickey's front are the listed gaps, tries spent on the night; check the tries below before starting anything. Otherwise the fallback (phase 3's port; U7 was looked at and not ported; thin, prefer exit preparation): the exit's reviewers' reading of old faults in CLOSE-2026-10-22.md.
3. **Tomorrow morning, tonight's walk (`python tools/corner_people.py`, passing the walk's backup log; the newest log holding the lines may be a later picture run):** closest standing must be over 0.60 m; if under, try 2 of 2. Read the "cannot walk ... here by, 0.6 m on by" lines for what shuts Sam in at Rita's step (about (17.68, 4.01)). When a walk is impossible the person is held 12 s and then placed: in view that reads as a jump, the plan's "walk off instead of vanishing": first try on it once the cause is read. Watch for route stages lost because people now keep 0.6 m apart. With those read, n02-4-corner-people can close or be listed.
4. n02-3-3-stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Then n02-3-4-exit for 9 November by the brief, one final reviewer per exit, at most two at a time, its result on his page; latest night's "to add" lines filled first. Speech's missed bar, the jacket's collar and the sit's head swing are listed.
5. n02-4-corner-pages: the corner's end page, from the latest packaged pictures, -PageShots=day and =night on the played copy (F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt; about 2 minutes each, off-screen; copy from the played copy's Saved/PageShots), every frame looked at full size, shortfalls first, no white base layer (they are left out). `-PageShots` leaves the 3 undressed out by itself.
6. Monday about 12:50: read the weekly figure on the usage tool, before its 13:00 reset (49% on Thursday 22:24): `--allowance`. When a try is set aside: `python tools/token_measures.py --thrown "what" --since HH:MM`.
7. Each morning until mended: the nightly read-back task is stuck: read the Needs-you page's verdicts and items with ArtifactData's out_dir into production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8 and run `python tools/page_answers.py --nightly`, or ci-checks fails after two days. Done 05:24 on 6 Nov. If it stays stuck, a stop needs his hands: an item on his page.

## Tried and failed, and why

- People apart: the 0.6 m test had existed since 2 November and never fired on anyone dressed: IsHidden on the body, not the figure. Why both walkers stop short of the quay's spot (-5, 0) at about x 0 is unread.
- The witnesses: taking people out of the lines alone changed almost nothing; the shop front's box was the cause. The nightly stage "onlookers" passed all along because it counts who was measured, not who was told. Rita, 3.9 m behind her own window, still cannot see Tom (the same box); left on purpose, since seeing means naming and reporting: for the exit's reviewer or the next order. Last night's six witness lines: lamp post C named as blocking at about 19 m, street_interior and the ironmonger's front at others.
- The hill's third try, inside the one try: the first far wood, big single masses, read as huge lumps; the second, tall trees, stood on stilts above the old crest; the third, lower, kept. Pulling leaves onto the hearts cures flecks but loses the broken edge: opaque leaf triangles at this range trade one fault for the other; a soft edge probably needs another method (cards or impostors, HILL-METHODS).
- The hill's gaps were real holes, proved with the haze off (`-ExecCmds=scalability 2,showflag.fog 0`).
- Flag stains: a mark's tint is multiplied by the picture's grey, a quarter; five drawn pictures with brown tints still measured an even grey darkening. The wet coat's reflection hides the colour. Drawing a stain again would be a third try.
- The sky's fog-off test: an unquoted -ExecCmds did nothing and looked like "fog has no effect"; quoted, sky and sea still barely moved, so the white was the dome and the sea's mirror, not haze.
- sea_specular first sat inside the TakesWater branch, which the sea never enters. The night's first values: saturated fill turned unlit brick pure red; the higher haze read as dusk.
- Step 9b's pipe: a scan of rust on white paint graded by its whole mean turned the paint blue; graded on the brightest quarter it reads as black iron.
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
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast, n02-9-session-model (his yes: one day on Sonnet under Monday's order), n02-9-window-break. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat, not a decal; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit.
- Tries used: people apart 1 of 2; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn at a pause 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses in the ladder 1 of 2; the hill 3 of 3, spent (his yes used); street-level wear's flag stains 2 of 2, listed, review rounds 2 of 2; the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 2 of 2, spent; the collar 4, set aside; 9a 1 of 2, passed; the gilt 1 of 2, passed; 9b 2 of 2 on the pipe, passed; 9d's wash 1 of 2, passed; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2, passed; 9d's roof breaks 2 of 2, passed; the undressed rule 2 of 2, passed.
- API spend: none this session.
- Uncommitted on purpose (no notes-only commits; goes with the next work commit): this file.
- His page and the advisor channel were last read 06:07. Report times: read Get-Date before writing one. Reports 2026-11-06-0550 and -0608 written.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
