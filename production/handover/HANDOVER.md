# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-04 15:21 (the hourly take-over, gate GO: "the last session stopped at 14:32; no turn written for 49 minutes")
**Stopped:** 2026-11-04 14:32 (the session before; this one still running)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity (real turns in the project's session logs; since 4 November 13:46 never the app's session list, which shows idle remote-controlled sessions as active), and works only when Stopped is later than Started and no turn has been written for 15 minutes. Each session runs `python tools/history_check.py` (its own log, by its id) at the end of each item; past 300,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**As of:** Wednesday 4 November 2026, 16:20 (Swiss time).

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this session (15:21 on)

- **The first real take-over worked** (DECISIONS 15:21): the gate said GO, the lean start cost 115,468 tokens over 6 steps (first step 84,432). Told him in one line.
- **Mickey's window's black reflection mended** (DECISIONS 15:36, commit 2059dc261): not the brick scans; the bake caught its first window (eg_bay0, Mickey's) on frame 0 after the 40 s load stall, the street unlit. The glass catch now also waits 90 drawn frames (VignetteShot.cpp); re-baked (16 windows, day and night; manifest 4 Nov); eg_bay0's day cube now lit. Pushed; tonight's build carries it (the runner imports the bake from F:).
- **Tom's jeans and boots passed packaged** (DECISIONS 15:44; order items done): one fresh final reviewer of the night walk's step pictures, no new fault.
- **Sitting failed two review rounds** (DECISIONS 15:44, 16:09, 16:17): in the packaged film's drop (frames 21, 22) the head reads below the shoulders, face to the floor. The editor measures the held face at -25 and the drawn Face part's head 0.0 degrees from the held one (new log line LedgerSitFaceDrawn, SliceCharacter.cpp, pushed), but that is the editor, not the packaged 3 Nov build. Two rounds spent: the drop is listed as a known fault (AT-RISK); the sit stays open.

## First, in this order (the next session)

1. Your start: `python tools/start_size.py <your log id>`, one line in DECISIONS. Commit the uncommitted records (DECISIONS 16:17, AT-RISK, this file) with your first work commit.
2. His page's answers (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8, collection verdicts): the corner's midweek item (corner-midweek-2026-11-04), unanswered at 16:15; act at once.
3. After tonight's packaged build (check the played copy's build-commit.txt is at or after ed73d29b3's successor with SliceCharacter's LedgerSitFaceDrawn): **Mickey's window photographed packaged by day** (-PageShots, the corner's cam_mickeys view, as the midweek gate did: F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/command-day.txt), one fresh reviewer beside F:/LedgerTools/gate/last-good/office/package-cam_mickeys-day.png; then Rita's view and the window back on his page's corner item if it passes.
4. **The sit's drop, diagnosed packaged** (not a try): `python tools/route_walk.py --sit` on the played copy (by day, left alone, start it in the background and stay quiet), then read the packaged log's LedgerSitFaceDrawn and LedgerSitNeck lines around the drop and look at the film's drop frames yourself. If the drawn head differs from the held one packaged, that is the fault to fix (a first try). If they agree, the reviewers' reading is what the eye sees: then the fault is how the drop looks from the front (the head rolled toward Ron), a first try at that.
5. **The launch peak, next run:** the boot profile with -PerfHook=stand added, repeated until a launch shows the 2 GB spike; read GPUMem/LocalUsedMB, TransientMemoryUsedMB and RenderTargetPoolSize at its frame (production/research/frame-headroom/LAUNCH-PEAK-2026-11-04.md, its last section). Then the exit's line for CLOSE-D.
6. Still owed: a film of Tom walking for the slide (Tom as played); Tom's jacket (collar, n02-3-2-collar-third) and jumper to pass packaged; Rita's view's faults into corner step 9 (STEP9-PLAN-2026-11-03.md) and the gilt letters' metallic input.
7. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Then the exit re-check (n02-3-4-exit) for 9 November.
8. The lean start's switch point (A3): this session's start 115,468 tokens; it reached 256k at 16:17 after about 55 minutes of work; set the point from the cost per step, tell him the number.
9. Every night before 00:45: the day's summary by 07:00 and the overview by 07:30 (FOR-JAFAR.md; the token audit's three shares first), the morning pictures, the progress page; today's summary lines (with the earlier session's: speech missed after its third try; the take-over mended and rehearsed; the corner page; the office passed; gilt decided as metal): the first real take-over; Mickey's window mended (to pass packaged); jeans and boots passed packaged; the sit's drop failed two rounds, listed.

## Tried and failed, and why

- Speech's third try (earlier today): caching saves no time at this prompt size.
- The sit's drop: the 2 Nov face hold measures -25 on the body and on the drawn face in the editor, yet two reviewers see a face to the floor in the 3 Nov packaged film; not yet measured packaged.
- My first guess for the window (the brick scans, then the walls' real values) was wrong; measuring every cube by one number found it.

## In flight (carried)

- Corner step 9 planned (STEP9-PLAN-2026-11-03.md): a kit with trims, material first; plus the gilt letters' metallic input (DECISIONS 14:10).
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread.
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes from Friday.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Stash@{0} (06:10 editor-rebuilt material files) kept.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers. Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own.
- Tries used: the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first); Mickey's window black 1 of 2; the sit's drop 0 (diagnosis only), review rounds 2 of 2.
- API spend today: US$0.56 (none this session).
- A Build.bat of the editor target once failed with OtherCompilationError (a CrimeProbe.h first-header message, 15:5x) and passed unchanged on the rerun; the game target prints the same message and succeeds.

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
