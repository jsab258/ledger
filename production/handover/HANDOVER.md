# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-04 20:21 (the hourly take-over, gate GO: "the last session stopped at 19:37; no turn written for 39 minutes")
**Stopped:** 2026-11-04 19:37 (an item's end: the corner's step 1, first part; history 180,000 tokens after a 118,000 start)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity, and works only when Stopped is later than Started and no turn has been written for 15 minutes. Each session runs `python tools/history_check.py` at the end of each item; past 200,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**As of:** Wednesday 4 November 2026, 19:37 (Swiss time). Committed and pushed to wip with this file (the corner's step 1, first part); ci-checks failed=none 93/93.

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this session (19:21 to 19:37)

- **The corner, his step 1, first part** (DECISIONS 19:45): a cast body whose worn garments do not replace both Epic's top and lower part is tagged LedgerUndressed (LedgerGarments.h); his page's pictures (-PageShots, all modes but dress) leave it out, -PageUndressed keeps them; play and the tester's walk keep everyone. Today: Ron, Sheila, Darren left out (log "3 undressed people left out"). Both targets built; editor day pictures taken (ue-probe/Saved/PageShots). The phone box's woman is a dressed stand-in, kept. The morning pictures (vignette mode) never showed the cast.
- One small reviewer (Sonnet), one round: hook, Mickey's, A, B clean; **reverse view fails**: a barefoot man in white vest and shorts by the Tea Rooms door (number 14) is still there, as in the midweek picture. He is not one of the three cast (only Lena, Sam, Rocco are MetaHumans); the three stand-ins left are martha-idle, leonard-idle, kate-idle (street-people.json; VignetteShot.cpp ~2400 to 2490 spawns them, GPeopleByGlb). Unverified guess: leonard-idle (a man, opposite pavement, walks to x 6 in free play). Review: scratchpad only (not kept); picture: ue-probe/Saved/PageShots/cam_reverse-day.png.
- Start of this session: 118,480 tokens over 9 steps (start_size.py).

## First, in this order (the next session)

1. Your start: `python tools/start_size.py <your log id>`, one line in DECISIONS, committed with your first work commit. His page has 0 open items (read 19:22).
2. **The Tea Rooms man** (step 1, first try at him): find which stand-in he is (look at the three glbs' textures or log each stand-in's place in PageShots), then tag that stand-in LedgerUndressed (or drop the white-bodied glb from the street until dressed); editor PageShots=day, reverse view, one small reviewer. Then step 1's second part: dress the cast by the garment skill, Ron first (RonJacket held; trousers to make).
3. Then his steps 2 to 5 in order (the hill, night readability, sky and quay end, street-level wear), each a piece with its own gate; the gilt letters' metallic input and 9b to 9d after, as hours allow.
4. Every night before 00:45: the day's summary by 07:00 and the overview by 07:30 (FOR-JAFAR.md; the token audit's three shares first), the morning pictures, the progress page. Today's summary lines: the hand-over point 200,000; the launch peak closed for the exit; speech missed after its third try; the take-over mended, rehearsed and real; the corner page; the office passed; gilt decided as metal; Mickey's window mended (to pass packaged); jeans and boots passed packaged; the sit's drop failed two rounds, listed; the jumper's place ruled (held); the jacket set aside (its collar back); painted timber on every front's joinery; **the undressed cast left out of his page's pictures (he can overturn it)**.
5. After tonight's packaged build (the played copy's build-commit.txt at or after this commit): Mickey's window photographed packaged by day (-PageShots=day as F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt), one fresh reviewer beside F:/LedgerTools/gate/last-good/office/package-cam_mickeys-day.png; then Rita's view and the window on his page at the corner's end page if it passes. 9a packaged: the night walk's pictures of the fronts, one small reviewer. The undressed rule packaged: the same day pictures' log line.
6. The sit's drop, diagnosed packaged (not a try): `python tools/route_walk.py --sit` on the played copy (by day, background, stay quiet), then the packaged log's LedgerSitFaceDrawn and LedgerSitNeck lines and the film's drop frames.
7. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Then the exit re-check (n02-3-4-exit) for 9 November, with the launch peak's CLOSE-D line (LAUNCH-PEAK-2026-11-04.md), the jacket's collar listed.
8. Still owed: a film of Tom walking for the slide; 9b and 9d of the corner; the lean start's week of quality counts (B) for Monday's overview.

## Tried and failed, and why

- Speech's third try: caching saves no time at this prompt size.
- The sit's drop: -25 measured in the editor, yet two reviewers see a face to the floor in the 3 Nov packaged film; not yet measured packaged.
- The collar: neck weights (v32 to v34), the head map, a corrective shape, the zip lowered: four tries, set aside; its back now seen in Sheila's talk, same cause.

## In flight (carried)

- Corner step 9: 9a passed in the editor, packaged tonight; 9b, 9c (waiting), 9d planned; the gilt input.
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread.
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from Friday.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Untracked shop-room files under production/art/shop-rooms are not this session's; left. Stash@{0} (06:10 editor-rebuilt material files) kept.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own; Tom's head clamp in talk.
- Tries used: the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2; the sit's drop 0 (diagnosis only), review rounds 2 of 2; the collar 4, set aside; 9a 1 of 2 (passed its round); the undressed rule 1 of 2 (the Tea Rooms man missed).
- API spend today: US$0.56 (none this session).
- A Build.bat of the editor target once failed with OtherCompilationError (a CrimeProbe.h first-header message) and passed unchanged on the rerun.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
