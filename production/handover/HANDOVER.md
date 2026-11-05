# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-05 09:21
**Stopped:** 2026-11-05 10:10 (history 220,000 tokens, over the hand-over point, at the hill's third try's end)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 15 minutes. Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this session (09:21 on)

- **The hill's third try (his yes, 07:22): spent, in the editor, one review. Not packaged.** Flecks 258 to 109 by day, gaps mostly gone, roof triangles reduced; the reviewer records a new blocking fault: crowns are clean lumps, pompoms and stacked pads, worse than the last good picture. Kept, listed; no fourth try without his yes. Item closed on his page. F:/LedgerTools/gate/new/hill-third-2026-11-05/r3/review.json. Street faces 427,854 to 493,866, GLB 59 to 68 MB, copied to game inputs and imported locally.
- **The page-read hook (advisor's messages 05 and 06), acknowledged, reported:** tools/page_read_hook.py after each tool step, silent unless his page's verdicts or advisor reads are over 45 minutes old. Seen firing live. It costs about 1.1 s a step, about 20 minutes a day. **The fast path (tools/page_read_hook.sh, 0.12 s) is written but NOT switched on: the permission check refused the one-line settings change.** Never go round that refusal (no shell write to .claude/settings.json); it is on his page, page-check-speed-2026-11-05.

## First, in this order (the next session)

1. Your start: the verdicts and the advisor channel. If page-check-speed-2026-11-05 is yes: try the one Edit once, the command becoming `sh "$CLAUDE_PROJECT_DIR/tools/page_read_hook.sh"`; refused again, give him that line by a NEEDS YOU message. Git may give the .sh Windows line ends on a later checkout, which breaks sh: test it first. If no: delete the .sh file and its mention in the .py's docstring. Close the item either way.
2. The gilt letters' metallic input and 9b to 9d as hours allow (production/art/corner/STEP9-PLAN-2026-11-03.md).
3. The sit's drop, diagnosed packaged (not a try): `python tools/route_walk.py --sit` on the played copy (by day, background, stay quiet), then the packaged log's LedgerSitFaceDrawn and LedgerSitNeck lines and the film's drop frames.
4. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Worst frame 23.29 ms in the 4 to 5 Nov perf step. Then the exit re-check (n02-3-4-exit) for 9 November, with the launch peak's CLOSE-D line (LAUNCH-PEAK-2026-11-04.md), the jacket's collar listed, speech's missed bar reported.
5. After tonight's packaged build: the sky, street-level wear and the hill by day and night in packaged pictures (`-PageShots=day` and `=night` as F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt), one review each covering the final wear in the hook, reverse and night views, and the frame's cost. **Read card memory: 5,952 MB on 5 Nov before the hill's 15% more geometry, against the 6 GB line.** Over the line: cut HILL_FAR_WOOD_LEAVES or a tree row first. Check that the night's sea still reads now its reflection is cut: sea_specular also applies at night.
6. Still owed: a film of Tom walking for the slide; the lean start's week of quality counts (B) for Monday's overview; the corner's end page.
7. Each morning until mended: the nightly read-back task is stuck (its 3 Nov run still "running"): read the Needs-you page's verdicts and items into production/approvals/answers/<page id>/ and run `python tools/page_answers.py --nightly` by hand, or ci-checks fails after two days. Done at 05:33 on 5 Nov. If it stays stuck, a stop needs his hands: an item on his page.

## Tried and failed, and why

- The hill's third try, inside the one try: the first far wood, big single masses, read as huge lumps; the second, tall trees, stood on stilts above the old crest; the third, lower, kept. Pulling leaves onto the hearts cures flecks but loses the broken edge: opaque leaf triangles at this range trade one fault for the other; a soft edge probably needs another method (cards or impostors, HILL-METHODS).
- The hill's gaps were real holes, proved with the haze off (`-ExecCmds=scalability 2,showflag.fog 0`): the ridge's ground lies below the line of sight over the top tier.
- Flag stains: first too faint (a mark's tint is multiplied by the picture's grey, a quarter, so tints printed near black, yet the masks were weak); broad ones read as leaf shadows; five drawn pictures with brown tints still measured an even grey darkening, with no brown shift, hard-edged and lobed. The wet coat's reflection hides the colour. Drawing a stain again would be a third try.
- The sky's fog-off test: an unquoted -ExecCmds did nothing and looked like "fog has no effect"; quoted, sky and sea still barely moved, so the white was the dome and the sea's mirror, not haze.
- sea_specular first sat inside the TakesWater branch, which the sea never enters: it changed nothing. Moved out, same value; counted as the same second try, named in the summary to overturn.
- The night's first values: saturated fill turned unlit brick pure red; the higher haze read as dusk.
- Speech's third try: caching saves no time at this prompt size.
- The sit's drop: -25 measured in the editor, yet two reviewers see a face to the floor in the 3 Nov packaged film; not yet measured packaged.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.

## In flight (carried)

- Corner step 9: 9a passed packaged; 9b, 9c (waiting), 9d planned; the gilt input.
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread.
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from Friday.
- The night walk lost Ron and Darren (13 of 15; Darren alone on 4 Nov): unexplained, not looked at. Sheila's subtitle shows Tom's question under her name with a stray quote mark (the walk's report, 0202 step-037): not looked at.
- Two of today's editor picture runs ended in a segmentation fault at exit (exit 139) after writing all their pictures; two ended clean. Not looked at.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept.
- For the corner's -PageShots in the editor: run tools/ue/stage_game_data.py, copy vignette-pieces.json to ue-probe, then the command in F:/LedgerTools/gate/new/street-level-2026-11-05/final/command-day.txt, MSYS_NO_PATHCONV=1, in the background; pictures in ue-probe/Saved/PageShots, about 2 to 3 minutes a run.
- The street's export needs `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2 (without --block street it tries a render and stops); copy the glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast, n02-9-session-model. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night; stains on wet flags through the coat, not a decal; the hill's trees by another method.
- Tries used: the hill 3 of 3, spent (his yes used); street-level wear's flag stains 2 of 2, listed, review rounds 2 of 2; the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 0 (diagnosis only), review rounds 2 of 2; the collar 4, set aside; 9a 1 of 2, passed; the undressed rule 2 of 2 (passed its round).
- API spend today: none this session.
- The glass bake was rerun after the hill's export (10:07, 16 windows, fresh); not imported locally (the build machine imports it itself).
- His page and the advisor channel were last read 09:59 to 10:02.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
