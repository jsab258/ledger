# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-05 05:21
**Stopped:** 2026-11-05 06:09 (history 276,000 tokens, over the hand-over point, at the sky's end)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 15 minutes. Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this morning (05:21 on)

- Summary, overview, progress page done and pushed; morning pictures looked at (nobody in the white layer; the woman in red heels by Mickey's stands stiff and wide-legged).
- **The night (his step 3): last review passed with narrow points, four final reviewers, packaged.** Listed, both tries spent: Mickey's near front too dark (fascia about 2, upper front 0.3 to 4), flat brown sky, unlit brick near pure red, the hill evenly lit. F:/LedgerTools/gate/new/corner-packaged-2026-11-05/review-night-*.md.
- The hill's frame cost read: none (57.9 fps; 57.5 before); card memory 5,952 MB (5,739), close to the 6 GB line, watched.
- Mickey's window by day and 9a passed packaged, one small reviewer (9a's evidence weak: barely visible). The window's picture is the new last good.
- **The sky and quay end (his step 4): second and last try passed in the editor, one small reviewer.** sky_seen_gain 3.5, sky_light_gain 5.306, new sea_specular 0.1. Reverse: high sky 222 to 193, low 211 to 174, far strip 219 to 191, sea 195 to 175, street unchanged. Listed: faint streaks in the hook sky, only with contrast raised. **Not packaged yet.** Both targets built; the glass re-baked for the new look (status OK, 16 windows).

## First, in this order (the next session)

1. Your start: the verdicts (hill-third-try-2026-11-04, unanswered at 05:50: yes means one try, about 1 hour, one review, on the three faults) and the advisor channel (nothing new at 05:50).
2. **His step 5, street-level wear** (the street-weathering skill). Then the gilt letters' metallic input and 9b to 9d as hours allow.
3. The sit's drop, diagnosed packaged (not a try): `python tools/route_walk.py --sit` on the played copy (by day, background, stay quiet), then the packaged log's LedgerSitFaceDrawn and LedgerSitNeck lines and the film's drop frames.
4. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Worst frame 23.29 ms in the 4 to 5 Nov perf step. Then the exit re-check (n02-3-4-exit) for 9 November, with the launch peak's CLOSE-D line (LAUNCH-PEAK-2026-11-04.md), the jacket's collar listed, speech's missed bar reported.
5. After tonight's packaged build: the sky by day and night in packaged pictures (`-PageShots=day` and `=night` as F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt), and the frame's cost. Check that the night's sea still reads now its reflection is cut: sea_specular also applies at night and no night picture was taken.
6. Still owed: a film of Tom walking for the slide; the lean start's week of quality counts (B) for Monday's overview; the corner's end page.
7. Each morning until mended: the nightly read-back task is stuck (its 3 Nov run still "running"): read the Needs-you page's verdicts and items into production/approvals/answers/<page id>/ and run `python tools/page_answers.py --nightly` by hand, or ci-checks fails after two days. It was done at 05:33 on 5 Nov. If it stays stuck, a stop needs his hands: an item on his page.

## Tried and failed, and why

- The sky's fog-off test: an unquoted -ExecCmds did nothing and looked like "fog has no effect"; quoted, sky and sea still barely moved, so the white was the dome and the sea's mirror, not haze.
- sea_specular first sat inside the TakesWater branch, which the sea never enters: it changed nothing. Moved out, same value; counted as the same second try, named in the summary to overturn.
- The hill: leaves alone read wintry; tight boughs read as pompoms; loose leaves read as flecks; big leaves read as triangles on roofs. The third try would pull the outermost leaves in further and cap the size per tree; test first whether the gaps are holes or far ground in haze.
- The night's first values: saturated fill turned unlit brick pure red; the higher haze read as dusk.
- Speech's third try: caching saves no time at this prompt size.
- The sit's drop: -25 measured in the editor, yet two reviewers see a face to the floor in the 3 Nov packaged film; not yet measured packaged.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.
- A slip this morning: stamps in the records were guessed an hour ahead; corrected from the clock and the files' times. Stamp from the PowerShell tool's Get-Date (from Git Bash, powershell.exe read the same here, but do not guess).

## In flight (carried)

- Corner step 9: 9a passed packaged; 9b, 9c (waiting), 9d planned; the gilt input.
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread.
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from Friday.
- The night walk lost Ron and Darren (13 of 15; Darren alone on 4 Nov): unexplained, not looked at. Sheila's subtitle shows Tom's question under her name with a stray quote mark (the walk's report, 0202 step-037): not looked at.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept.
- The street's export needs `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2 (without --block street it tries a render and stops); copy the glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk; Mickey's near front at night.
- Tries used: the hill 2 of 2, spent (his yes asked); the night 2 of 2, spent; the sky 2 of 2, spent; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2, passed; the sit's drop 0 (diagnosis only), review rounds 2 of 2; the collar 4, set aside; 9a 1 of 2, passed; the undressed rule 2 of 2 (passed its round).
- API spend today: none this session.
- The glass bake was rerun after the export; its local import showed 'Error opening file' warnings on some new names, its result line unread (the build machine imports it itself; Mickey's glass reads well packaged).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
