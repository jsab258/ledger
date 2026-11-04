# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's (his rulings of 4 November: the lean start; the hourly task); the phase's items are NOW.md's and the order's; this file holds only what is in flight, what was tried and failed and why, the next steps in order, and the tries used.

**Started:** 2026-11-04 13:41 (started by Jafar himself with the goal; his message at 13:38: the hourly take-over failed, fix and test it, no stop at the size until a take-over has worked)
**Stopped:** 2026-11-04 14:32 (an item's end, history about 600,000 tokens, past the 300,000 line)
(His rulings of 4 November, RULINGS.md: the hourly task "LEDGER: the hourly fresh session" (ledger-daily-fresh-session) runs at :15 from 05:15 to 00:15; each run first runs `python tools/fresh_gate.py`, which reads only this file and the project's own activity (real turns in the project's session logs; since 4 November 13:46 never the app's session list, which shows idle remote-controlled sessions as active), and works only when Stopped is later than Started and no turn has been written for 15 minutes. Each session runs `python tools/history_check.py` (its own log, by its id) at the end of each item; past 300,000 tokens it rewrites this file, sets Stopped from Get-Date and stops. Nothing works from 00:45 to 05:10.)

**As of:** Wednesday 4 November 2026, 14:32 (Swiss time).

**The goal:** his order of 2 November (production/orders/2026-11-02.md), until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it.

## Done this session (13:37 on)

- **The hourly take-over mended** (his message 13:38; DECISIONS 13:46): the 12:15 run stood aside on an idle remote-controlled "Ledger Builder" session in the app's list, the 13:15 run on the app's untimed bookkeeping appended to two idle old logs. tools/fresh_gate.py now counts only timed user and assistant turns (helpers' logs too), this run's own left out by CLAUDE_CODE_SESSION_ID; the task's prompt no longer consults the app's list. tools/history_check.py reads its own session's log by the same id (it took the newest file, the same flaw). **A take-over worked in rehearsal** (DECISIONS 14:23): the hourly run of 14:21 passed the mended gate (REHEARSAL GO), set a stand-in handover's Started line, read this file and NOW.md, and ended; only this session was left out of the activity count, standing in for the stopped one. Told him in one line at 14:23. The rehearsal files are deleted; the gate reads this file again. This stop is the first real take-over.
- **Speech's third try failed at its screen, and is spent** (DECISIONS 13:59 and 14:02): the check's fixed text cached was read from the cache (median 4,286 tokens a check) and saved no time (paired median 0.00 s, 62 held sentences, US$0.16). Run G inside the game not spent. Speech reaches the exit as a missed bar (run F, 2.02 s), told to him 14:06; n02-3-1-speech set aside; FINDINGS rewritten. The switch ships off, kept for the waiting list's cost lever.
- Gilt letters decided as real metal (DECISIONS 14:10; one line in the day's summary). Last week's four quality counts made (QUALITY-LASTWEEK-2026-10-27.md, folded into QUALITY-WEEK-2026-11-04.md). This session's start: first step 90,151 tokens, the skill list still 9,158 (skillOverrides do not reach his account's synced skills).
- **The corner's midweek page published** (his page, item corner-midweek-2026-11-04, NEEDS YOU sent 14:17; DECISIONS 14:18; production/audits/gate-corner/GATE-MIDWEEK-2026-11-04.md): five views photographed packaged, one fresh final reviewer each; hook day, hook night and reverse day passed (0 new faults) and are on the page; Rita's view (flat kiosk side, flat roof slab, even brick streaks) and Mickey's window (its street reflection flat black since the scans reached the packaged game: a regression) held back, named on the page as being fixed. One decision: the direction. Gilt letters decided as metal (14:10). The passed packaged pictures are now the corner's last good (package-*-2026-11-04.png).
- **Mickey's office passed packaged** (DECISIONS 14:25; n02-3-3-office done): by day and night, two fresh reviewers, 0 new faults, the five fixes hold. **The launch's card peak** (production/research/frame-headroom/LAUNCH-PEAK-2026-11-04.md, a diagnoser's note plus five boot profiles): placed in the first rendered frames, the game's own; the close's rise is the voice program loading onto the card; five launches without the capture's steps peak at 6.1 to 6.2 GB and settle at 5.5 to 5.6 GB, no spike. **Tom as played** read from the night walk's log: his MetaHuman in three garments on Epic's motion-matching sample (the at-risk list updated).

## First, in this order (the next session)

1. Your start: `python tools/start_size.py <your log id>`, one line in DECISIONS; and the first real take-over: one line in DECISIONS and tell him in one line that a take-over has worked (his message of 4 Nov 13:38 asked for that line).
2. His page's answers (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8, collection verdicts): the corner's midweek item (corner-midweek-2026-11-04) if he has answered; act at once.
3. **Mickey's window's reflection gone black** (a regression, the corner's; first try): find why the glass's reflection shows the street flat black in the packaged game since the brick scans reached it (the glass's baked reflection, -PageShots=bake, CrimeProbe.cpp 'THE GLASS BAKE', likely predates the scans or does not stage them; compare F:/LedgerTools/gate/last-good/office/package-cam_mickeys-day.png with F:/LedgerTools/gate/new/corner-midweek-2026-11-04/r1/cam_mickeys-day.png); mend, photograph packaged after the night's build, one fresh reviewer.
4. **The launch peak, next run:** the boot profile with -PerfHook=stand added (the capture's steps), repeated until a launch shows the 2 GB spike; read GPUMem/LocalUsedMB, TransientMemoryUsedMB and RenderTargetPoolSize at its frame (the note's last section says how). Then the exit's line for CLOSE-D.
5. **Fresh reviewers still owed (AT-RISK):** the night walk's pictures for Tom's jeans, boots and sitting (sitting packaged = n02-3-3-sitting); a film of Tom walking for the slide (Tom as played).
6. **Rita's view's faults** (the kiosk's side, the roof slab, the brick streaks) into the corner's steps: corner step 9 (STEP9-PLAN-2026-11-03.md, trims and material first) and the gilt letters' metallic input.
7. The Stutter: proposed to close as not reproduced (AT-RISK row); the exit's reviewer decides. Then the exit re-check (n02-3-4-exit) for 9 November.
8. The lean start's switch point (A3), from your own log's cost per step and this handover's cost; tell him the number.
9. Every night before 00:45: the day's summary by 07:00 and the overview by 07:30 (FOR-JAFAR.md; the token audit's three shares first), the morning pictures, the progress page; today's summary lines: speech missed after its third try (told him); the take-over mended and rehearsed; the corner page; the office passed; gilt decided as metal (his to overturn); this session ran at effort xhigh (the app refuses a session changing its own).

## Tried and failed, and why

- The hourly take-over's first check (4 Nov 11:11 to 13:21): stood aside on idle sessions (above); mended.
- Speech's third try: caching saves no time at this prompt size; the wait is the service's before its first word.

## In flight (carried)

- Corner step 9 planned (STEP9-PLAN-2026-11-03.md): a kit with trims, material first; plus the gilt letters' metallic input (DECISIONS 14:10).
- Phase 3's port U8: whether the night walk's session lines show no "loadRefused" is still unread (the walk's route folder kept only verdict.json).
- The faster-builds try 1 (the cache on C: at 10 GiB, 3 Nov): measure over five builds' coldCookMinutes (the workflow's own log line) from Friday.

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board); lasting copies on F:/LedgerTools/game-inputs. Stash@{0} (06:10 editor-rebuilt material files) kept.
- Waiting list: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files, n02-9-front-edge-wear, n02-9-talk-cost-levers (now with the check's cache as evidence). Worth adding at the next order: Flemish bond with burnt headers; the memory spike's fix if it is the game's own.
- Tries used: the reaction walk's delay 1; Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 3 of 3, spent; the office's damp stain outline would be a third try (his yes first).
- API spend today: US$0.56 (run F 0.40, the cache screen 0.16).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
