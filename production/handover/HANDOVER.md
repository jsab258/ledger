# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-05 05:21
**Stopped:** 2026-11-05 00:23 (the night's stop; a short session, history about 130,000 tokens)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 15 minutes. Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

(00:21 session, to the night's stop only: no game work, no try spent, nothing committed. Read the page and the advisor: all acknowledged, the hill unanswered. wip pushed at the 23:19 commit, night jobs set, drives C: 137 GB and F: 28 GB free.)

## Done on the evening of 4 November (22:21 on)

- Advisor's two messages acted on and acknowledged: the cast is NOT dressed this week (kept out of his frames; n02-9-dress-the-cast on the waiting list); his page's old items archived (needs_you_page.py --archive, Mondays).
- **The hill (his step 2): two rounds spent, listed, third try asked** (item hill-third-try-2026-11-04 on his page). Both reviewers: clearly better than the last good; new faults: flecks at the crest, sky-coloured gaps in the hillside (perhaps fogged far ground, not established), dark triangles on roofs. Kept in the game.
- **The night (his step 3): try 2 set, round 1 passed with narrow faults.** Near black 45% in the hook view (was 66%), clip 0.08%.
- **The sky (his step 4): try 1 kept.** Hook, A, B, Mickey's pass; reverse fails his words: sea and quay's edge still near white, seen sky only about 20 levels darker, no cloud form. No new fault.

## First, in this order (the next session)

1. Your start: read the advisor channel and the verdicts (hill-third-try-2026-11-04, unanswered at 00:22: act on it at once; yes means one try, about 1 hour, one review, on the three faults). The start is already measured (110,462 tokens; about 56,000 the app's own): its DECISIONS line and this file's short-session note are uncommitted, go with your first work commit.
2. The next morning, before anything else if it is morning: the day's summary and overview (FOR-JAFAR.md; the token audit's shares first), the morning pictures (nobody in the white layer: they use the vignette scene, not the page mode; look), the progress page. Summary lines for 4 Nov: the hand-over point 200,000; the launch peak closed for the exit; speech missed after its third try; the take-over mended, rehearsed and real; the corner page; the office passed; gilt decided as metal; Mickey's window mended (to pass packaged); jeans and boots passed packaged; the sit's drop failed two rounds, listed; the jumper's place ruled (held); the jacket set aside (its collar back); painted timber on every front's joinery; the undressed cast left out of his page's pictures; the cast's clothes moved to Monday's list by the advisor; **the hill's real trees and houses, listed at two rounds, third try asked; the night's warm sky and fill, replacing 29 October's stop on fills; the day's sky greyer, the quay end still white.**
3. After the night's packaged build (played copy's build-commit.txt at or after this commit): pictures by day and night (`-PageShots=day`, `-PageShots=night` as F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt). Then: **the night's second and last review round** (one final reviewer per view: hook, reverse, A, B, beside F:/LedgerTools/gate/new/hill-2026-11-04/r2 and its review-night.md's three faults; editor try 2 pictures in F:/LedgerTools/gate/new/night-2026-11-04/r2). Mickey's window by day beside F:/LedgerTools/gate/last-good/office/package-cam_mickeys-day.png; 9a's fronts, one small reviewer; nobody undressed in the reverse view. **The frame's cost of the hill: read it from the walk's perf step (the 427,854-face street, GLB 59 MB, F:/LedgerTools/game-inputs); a fall against the budget is a new fault.** Before-the-hill GLB: F:/LedgerTools/gate/quay-street-before-hill.glb.
4. **The sky and quay end's second and last try:** the reverse view's sea and horizon near white come from the haze over far water and the sea's own value, not the sky's gain; look at fog_cap_gain_day, fog_start_day_m and the south-quay water before changing the gain again; the dome's cloud form is washed out too (sky_seen_gain 7 gave only about 20 levels; the tone curve's shoulder). Measured at 00:22 on the hill's r2 reverse day picture (which may predate the sky's try 1, so re-measure on the newest): above the skyline the frame runs a smooth 235 to 240 with almost no variation (spread under 1.5 levels), 14% of the frame at 235 or more; no cloud form survives. The values in play: fog colour 1.3/1.33/1.38, density gain 3.5, cap gain 5, start 75 m, cut-off 900 m, dome at 1,000 m (so fog should not cover the dome itself: that points at the dome's gain and the tone curve for the sky, and at the fog for the sea, not established). First, not a try: one reverse picture with the fog off, to split the two. Pictures, one small review, then packaged.
5. His step 5, street-level wear. Then the gilt letters' metallic input and 9b to 9d as hours allow.
6. The sit's drop, diagnosed packaged (not a try): `python tools/route_walk.py --sit` on the played copy (by day, background, stay quiet), then the packaged log's LedgerSitFaceDrawn and LedgerSitNeck lines and the film's drop frames.
7. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Then the exit re-check (n02-3-4-exit) for 9 November, with the launch peak's CLOSE-D line (LAUNCH-PEAK-2026-11-04.md), the jacket's collar listed.
8. Still owed: a film of Tom walking for the slide; the lean start's week of quality counts (B) for Monday's overview; the corner's end page.

## Tried and failed, and why

- The hill: leaves alone read wintry; tight boughs read as pompoms; loose leaves read as flecks; big leaves read as triangles on roofs. The third try would pull the outermost leaves in further and cap the size per tree; test first whether the gaps are holes or far ground in haze.
- The night's first values: saturated fill turned unlit brick pure red; the higher haze read as dusk.
- Speech's third try: caching saves no time at this prompt size.
- The sit's drop: -25 measured in the editor, yet two reviewers see a face to the floor in the 3 Nov packaged film; not yet measured packaged.
- The collar: four tries, set aside; its back now seen in Sheila's talk, same cause.

## In flight (carried)

- Corner step 9: 9a passed in the editor, packaged tonight; 9b, 9c (waiting), 9d planned; the gilt input.
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread.
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from Friday.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept.
- The street's export needs `--root C:/Users/Jafar/ledger-local --block street --out <folder> --export-glb production/assets/street/quay-street.glb` on Blender 5.2 (without --block street it tries a render and stops); copy the glb and json to F:/LedgerTools/game-inputs, then import_street.py.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers, n02-9-dress-the-cast. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk.
- Tries used: the hill 2 of 2, spent (his yes asked); the night 2 of 2, its second review owed; the sky 1 of 2; the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2; the sit's drop 0 (diagnosis only), review rounds 2 of 2; the collar 4, set aside; 9a 1 of 2 (passed its round); the undressed rule 2 of 2 (passed its round).
- API spend today: US$0.56 (none this session).
- The glass bake was rerun after the export; its local import showed 'Error opening file' warnings on some new names, its result line unread (the build machine imports it itself; check the packaged glass).
- Night pictures' second try and the frame's cost are unreviewed; nothing here has passed packaged.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
