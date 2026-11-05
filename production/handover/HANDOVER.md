# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-05 13:21
**Stopped:** 2026-11-05 14:00 (history 266,000 tokens, past the 200,000 point, at step 9b's end)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 3 minutes (15 without a written stop; his yes of 5 November). Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this session (13:21 on)

- **The gilt letters are metal**, first try: they were never the decal; they are the street's own street_gilt row. It wears the kit's opaque master (it has a metallic input), gold's colour in the look file's gilt_metal_rgb. One small review, PASS WITH NOTES (night gold dim, above 2:1). Committed.
- **Step 9b**, tries 2 of 2 on the pipe's tint: sills, doorsteps and coping on a new stone_dressing row, gutters and downpipes on a new rainwater row, Poly Haven scans (tools/art-recipes/dressing_tiles.py; the sandstone's moulded bands cut off). Street exported, on F: game inputs, imported locally; glass rebaked (13:56, 16 windows). One small review, PASS WITH NOTES (faint vertical striping and a cool tint on the sills, rust barely seen). Doorsteps seen in no view. Committed, pushed to wip.

## First, in this order (the next session)

1. Your start: the verdicts and the advisor channel. Read 13:59: nothing new.
2. **In the working copy, not committed, not looked at:** 9d's first fault, the even streaks over every upper wall. They are the full-height "wash" decal on every bay, not the brick's streak (only the chandler has one). tools/street_wear.py now 0.30 + 0.23 x wear (was 0.45 + 0.35); street-wear.json regenerated. His 2 October words ("wear that reads at a glance across every facade") weigh against going further. Try 1 of 2: pictures by `python tools/shop_views.py <out> --shop mickeys@6.0` (and --night, MSYS_NO_PATHCONV=1), beside F:/LedgerTools/gate/new/corner-9b-2026-11-05/r2-*, one small reviewer, commit or `git checkout` both files; rerun the glass bake if ci says stale.
3. 9d's other two: the kiosk's flat side (panels from its own front), the roof (slate scan row, party-wall breaks, pots from the kit). production/art/corner/STEP9-PLAN-2026-11-03.md.
4. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Worst frame 23.29 ms in the 4 to 5 Nov perf step. Then the exit re-check (n02-3-4-exit) for 9 November, with the launch peak's CLOSE-D line (LAUNCH-PEAK-2026-11-04.md), the jacket's collar listed, speech's missed bar reported.
5. After tonight's packaged build: **the sit**: `route_walk.py --sit` on the played copy, with one fresh final reviewer of the drop's frames (19 to 26) beside the 2026-11-05-1135 film; no try left, so a new fault is listed. The walk's deed and wait failed last time because a window of his had the front: no meaning for the sit. Then the sky, street-level wear, the hill, the gilt and 9b by day and night in packaged pictures (`-PageShots=day` and `=night` as F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt), one review each covering the final wear in the hook, reverse and night views, and the frame's cost. **Read card memory: 5,952 MB on 5 Nov before the hill's 15% more geometry, against the 6 GB line.** Over the line: cut HILL_FAR_WOOD_LEAVES or a tree row first. Check that the night's sea still reads now its reflection is cut: sea_specular also applies at night. Check too that the kit master drew the gilt in the packaged game (log line LedgerGilt).
6. Still owed: a film of Tom walking for the slide; the lean start's week of quality counts (B) for Monday's overview; the corner's end page.
7. Each morning until mended: the nightly read-back task is stuck (its 3 Nov run still "running"): read the Needs-you page's verdicts and items into production/approvals/answers/<page id>/ and run `python tools/page_answers.py --nightly` by hand, or ci-checks fails after two days. Done at 05:33 on 5 Nov. If it stays stuck, a stop needs his hands: an item on his page.

## Tried and failed, and why

- The hill's third try, inside the one try: the first far wood, big single masses, read as huge lumps; the second, tall trees, stood on stilts above the old crest; the third, lower, kept. Pulling leaves onto the hearts cures flecks but loses the broken edge: opaque leaf triangles at this range trade one fault for the other; a soft edge probably needs another method (cards or impostors, HILL-METHODS).
- The hill's gaps were real holes, proved with the haze off (`-ExecCmds=scalability 2,showflag.fog 0`): the ridge's ground lies below the line of sight over the top tier.
- Flag stains: first too faint (a mark's tint is multiplied by the picture's grey, a quarter, so tints printed near black, yet the masks were weak); broad ones read as leaf shadows; five drawn pictures with brown tints still measured an even grey darkening, with no brown shift, hard-edged and lobed. The wet coat's reflection hides the colour. Drawing a stain again would be a third try.
- The sky's fog-off test: an unquoted -ExecCmds did nothing and looked like "fog has no effect"; quoted, sky and sea still barely moved, so the white was the dome and the sea's mirror, not haze.
- sea_specular first sat inside the TakesWater branch, which the sea never enters: it changed nothing. Moved out, same value; counted as the same second try, named in the summary to overturn.
- The night's first values: saturated fill turned unlit brick pure red; the higher haze read as dusk.
- Step 9b's pipe: a scan of rust on white paint graded by its whole mean turned the paint blue; graded on the brightest quarter it reads as black iron.
- Speech's third try: caching saves no time at this prompt size.
- The sit's drop: raising the pitch floor did almost nothing, and my camera theory was wrong; measure before reasoning from a picture. The lift about the horizontal alone stands a turned, near-down head on its side.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.

## In flight (carried)

- Corner step 9: 9a passed packaged; the gilt and 9b packaged tonight; 9c waiting; 9d begun (next steps).
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread.
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from Friday.
- The night walk lost Ron and Darren (13 of 15; Darren alone on 4 Nov): unexplained, not looked at. Sheila's subtitle shows Tom's question under her name with a stray quote mark (the walk's report, 0202 step-037): not looked at.
- Two of today's editor picture runs ended in a segmentation fault at exit (exit 139) after writing all their pictures; two ended clean. Not looked at.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept. Two Poly Haven sources on F:/LedgerTools/polyhaven.
- For the corner's -PageShots in the editor: run tools/ue/stage_game_data.py, copy vignette-pieces.json to ue-probe, then the command in F:/LedgerTools/gate/new/street-level-2026-11-05/final/command-day.txt, MSYS_NO_PATHCONV=1, in the background; pictures in ue-probe/Saved/PageShots, about 2 to 3 minutes a run.
- The street's export needs `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2 (without --block street it tries a render and stops); copy the glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast, n02-9-session-model. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat, not a decal; the hill's trees by another method.
- Tries used: the hill 3 of 3, spent (his yes used); street-level wear's flag stains 2 of 2, listed, review rounds 2 of 2; the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 2 of 2 (the eyes' level, spent), one review owed on its packaged film; the collar 4, set aside; 9a 1 of 2, passed; the gilt 1 of 2, passed its round; 9b 2 of 2 on the pipe, passed its round; 9d's wash 1 of 2, not yet looked at; the undressed rule 2 of 2 (passed its round).
- API spend today: none this session.
- The glass bake was rerun after the hill's export (10:07, 16 windows, fresh); not imported locally (the build machine imports it itself).
- His page and the advisor channel were last read 13:59; nothing new.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
