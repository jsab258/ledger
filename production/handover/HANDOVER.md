# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-06 11:22
**Stopped:** 2026-11-06 06:07
(The session started 06:21 set no Stopped line; no turn written for 175 minutes, taken as stopped.)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop; his yes of 5 November). Each session runs `python tools/history_check.py` at the end of each item; when tools/history_check.py says OVER (since 5 Nov evening: past 250,000 tokens at an item's end falling 5 to 15 minutes before the next run, which really fires at :21; or past 400,000 whatever the clock; between the two it says UNDER, take the next item) it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Standing ways of working (the advisor's messages, within his rulings; carry this list across every rewrite; message 13)
- His yes of 6 Nov 11:40, until 13:00 Mon 9 Nov (RULINGS.md, DECISIONS 6 Nov 12:35; it stands over the task prompt's older words, which a scheduled run may not change): the waiting list's named items when the order's items wait; four helpers, none that may finish during a tester walk; work through the night with nothing touching Unreal from 01:15 to 04:30, stopping before 01:40 instead of 00:45, so nothing runs beside the walk (tools/fresh_gate.py holds starts till it reports). His schedule edit is done and checked (14:27): every hour, round the clock.

- While a session works, a short row to 'reports' at least once an hour, even when nothing is finished: what is in hand, what it waits on; the watchdog counts it as a sign of life (message 15).
- Stops line up with the next run: past 250,000 tokens stop only at an item's end 5 to 15 minutes before it; 400,000 hard (message 10; tools/history_check.py).
- The six measures' table in each morning's overview (message 11; tools/token_measures.py).
- Never stop a session for lack of work: when the item waits on a build or a review, the order's next item, then the fallback list (phase 3's port, phase 5's research); stop only at the size point or the night's Unreal jobs (message 12, point 1).
- A standing way from the advisor is recorded here the same hour and named in its acknowledgement (message 13).

## This session (11:22 on), done

- **The Stutter, both tries spent.** Voice program's card model loaded only when needed; the walking map built only with -LedgerNav. On build 7bef7cf, 25 packaged walks, 45,000 frames: 2 over 33.3 ms, one 231 ms (nomapc, a wait on the visibility tasks, 219 ms), one 39 ms (rate16); standing worst 24.2. Set aside as a missed bar, no third try asked: at one in 25 walks a fix cannot be told from luck in under about 75 walks. Card peaks near 10 GB in 4 of the 25, not looked at further. The exit's brief and the at-risk row carry all of it. In a frame file: frame time at row n, threads' totals at n-1, render thread's own stats at n-2.
- **His yes of 11:40** (whole allowance) acted on; his schedule edit done and checked, every hour round the clock. The 145 recommendations scheduled, reviewed (RECS-BY-PHASE-2026-11-06.md: done 11, in order 9, open 107, ignore 18). Study B's first notes (thin) and inZOI's files noted. Handover numbers reported in 'reports' (14:45).
- **Rita's broken window: two tries, set aside, not passed, in the game** (DECISIONS 17:20; review F:/LedgerTools/gate/new/window-break-2026-11-06/try2/review.json). By day it reads as smashed; the rim reads as a drawn outline; at night it hardly reads. Disturbed goods not begun.
- **Build asked at the end of this session:** it carries the window; let it finish before local GPU work or captures. It also carries the near pictures in -SmashShot: `-SmashShot=<folder>`, about 4 minutes, in the editor add "-ExecCmds=scalability 2,r.SetRes 2560x1440w" for full size; the editor crashes at exit after its pictures, known.

## First, in this order (the next session)

1. Your start: the verdicts and the advisor channel, read 17:20 to here; nothing open on his page; acknowledgements through 15. An hourly row to 'reports'.
2. **While the build runs (no captures, no GPU work):** by the waiting list under his yes, one at a time: the dispatcher's voice (n02-9-dispatcher-voice: VCTK p280, his pick of 24 Sep; the clip folder still holds p233; VOICE-PERMISSIONS-2026-09-24.md, voice-alternatives-2026-09-24); then study B and the clothes from Silent Hill 2 and inZOI's files (capped: F: holds about 27 GB, floor 20 GB; one extractor; FModel's key on F: only; helpers no clicks).
3. **When the build lands, n02-4-corner-pages:** the corner's end page, from -PageShots=day and =night on the played copy (F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt; about 2 minutes each, off-screen; copy from the played copy's Saved/PageShots), every frame looked at full size, a fresh final reviewer, shortfalls first, no white base layer. His page, NEEDS YOU, recommending only what would pass in 2026.
4. Hair cards against strands if time remains (n02-9-hair-cards-vs-strands, needs Unreal).
5. **Night:** nothing touching Unreal 01:15 to 04:30; stop before 01:40; C++ pushed before 01:30.
6. **Tomorrow morning, tonight's walk (`python tools/corner_people.py`, passing the walk's backup log; the newest log holding the lines may be a later picture run):** closest standing must be over 0.60 m; if under, try 2 of 2. Read the "cannot walk ... here by, 0.6 m on by" lines for what shuts Sam in at Rita's step (about (17.68, 4.01)). Watch the route stages after the walking map's removal, and the window in the step pictures. Name in the summary: the 3.5 hours lost to the sign-out on 6 Nov (07:30 to 11:05); the Stutter's rare freeze; the window set aside. The summary, overview with shares and six measures, progress page: the nightly read-back by hand if stuck.
7. **n02-3-4-exit for 9 November** by the brief, one final reviewer per exit, up to four helpers, its result on his page; latest night's "to add" lines first. Speech's missed bar, the jacket's collar, the sit's head swing, the rare freeze are listed. The lean start's quality counts for Monday's overview (only this week's, as QUALITY-LASTWEEK-2026-10-27.md counted last week's). Faster builds: coldCookMinutes 5.68, 3.5, 3.6 since the cache change, with today's two to read: five, then record. The build machine's perf step read 54.5 fps on 7bef7cf against 57.7 before; if the session's or the helpers' work did not overlap it, look at why.
8. Monday about 12:50: read the weekly figure on the usage tool, before its 13:00 reset: `--allowance`. Monday `needs_you_page.py --archive`. When a try is set aside: `python tools/token_measures.py --thrown "what" --since HH:MM`.

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
- Waiting list (with n02-9-window-break's next try): n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast, n02-9-session-model (his yes: one day on Sonnet under Monday's order), n02-9-window-break. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat, not a decal; the hill's trees by another method; the title menu's backdrop shows the woman in the white base layer; the sit's head swing; Ron's hand in the sit.
- Tries used: people apart 1 of 2; the tester's morning 1 of 2, passed; martha-idle's place 1 of 2; walkers' turn at a pause 1 of 2; the witnesses' sightlines 2 of 2, spent; heard-only witnesses in the ladder 1 of 2; the hill 3 of 3, spent (his yes used); street-level wear's flag stains 2 of 2, listed, review rounds 2 of 2; the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 2 of 2, spent; the collar 4, set aside; 9a 1 of 2, passed; the gilt 1 of 2, passed; 9b 2 of 2 on the pipe, passed; 9d's wash 1 of 2, passed; 9d's kiosk 1 of 2, listed; 9d's roof 2 of 2, passed; 9d's roof breaks 2 of 2, passed; the undressed rule 2 of 2, passed.
- API spend: none this session.
- Uncommitted on purpose (no notes-only commits; goes with the next work commit): this file.
- Report times: read Get-Date before writing one.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than four helpers at once until 13:00 Mon 9 Nov, two after; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage, or guess a tool's name; let a helper stop a process; work while another LEDGER session works.
