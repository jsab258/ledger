# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-23 21:36 (the hourly run)

**Row due:** at the next start (last row 22:28; page read 22:57: nothing new; filter verdicts after 2026-11-23T21:40 UTC, advisor after 2026-11-23T22:35:00+01:00; last ack 2026-11-23-2235-336 at 22:55).
**Uncommitted:** nothing.
**Stopped:** 2026-11-23 23:12 (the 21:36 run: advisors 334-336 recorded; Sleeping Dogs speeds, three of five samples; history over its point)

(At each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 23 November (production/orders/2026-11-23.md, adopted by his tap 23 Nov 08:12 Swiss; runs to Mon 30 Nov 13:00). The measuring block (n23-1) leads; the normal line 0 to 90% by Mon 30 Nov 07:00 (week-shape.json inactive); `python tools/pace_line.py`.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, leading 'v1: N of 6', ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate, F:'s free room and the next 12 h's need, what fills each helper place.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page first, diff, then publish index.html with items.json.
- **His hands only when nothing else can (advisors 203, 204, 221):** an ACTION item needs only_you and a one-line tried; since 18 Nov 12:20 an open DECISION item needs "kind", one of CLAUDE.md's categories (money, sign-in, hands, licence-off-list, canon, story, scope, frame-look, person-look, taste, identity); needs_you_page.py refuses both otherwise. His own tools are not licences; deleting what nothing uses, guarded by a check, is not his decision.
- **Every standing ruling names its enforcer (advisor 205)** in production/rulings-enforcers.json the same day.
- **Kiln (RULINGS 13, 14, 18 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone; M7 count in every round report (0). Share: `python tools/token_measures.py --kiln-share`.
- **Fable (advisors 248, 250):** reset pressed 19 Nov; Fable at max for Kiln's hardest pieces, prototype, simulation, any Kiln fault failing two Opus tries (given problem, tries, numbers, no conclusion); his last reset untouched, never called for. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules:** F:/LedgerTools/tool-dev/LANE-RULES.md; every Kiln brief points to it.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Page read-back, daily (19 Nov):** query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci fails after 2 days).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his.
- **Measuring block in every row (advisors 292, 295):** read from measurements/STATUS.md (per aspect and game: planned, logged, state, open question); weekly points per measured hour, expected finish (estimate marked). Mafia is never a reference.
- **Progress page (advisor 275):** each refresh reads the live page and publishes only progress.json and changed files; never an old index.html, never plan.json. Helpers only as project types: settings_check flags catch-all helpers (target under 2%).

## Done today
- Earlier runs (13:07-21:03): order adopted, star reader, installed-game method, catalogue, n23-5 recipe rewrite, n23-3 first numbers, the fast film, Sleeping Dogs' opening scripted (watch_opening.py); GTA IV, GTA V, KCD2 copies NOT run (replaced unsigned launcher files, DECISIONS 23 Nov 20:30), their rows go to footage; do not re-ask him.
- 21:36 run: advisors 334, 335, 336 all recorded and acked. RULINGS now holds (within its 4,900 cap, 4,899): the one-shot waits for the complete blueprint, no early Unreal test; Kiln mission critical, Fable leads it on resuming; loops few, large, measured with a minimum-gain stop. Room came from removing replaced or repeated lines (DECISIONS 23 Nov 22:00). NOTEBOOK.md has the day's nine lessons; the recipe map (Claude Docs) has a new story-judge step, the rewritten loops step and Kiln's line.
- Sleeping Dogs speeds: the ruler is the chase's distance readout while Naz stands at 45 m (he stands from about 12 s after a checkpoint restart, for over 23 s); Enter on the fail screen restarts the chase in about 6 s; Shift is sprint (the game's own prompt). tools/drills/marker_read.py finds the green marker and tiles its numbers with grab times. Samples 1 to 3: sprint 5.5 m/s each; jog (W alone) about 4.4. Sample 4 lost (see Tried). SLEEPING-DOGS-DRILL-2026-11-23.md; STATUS.md on-foot 2.0 h logged.
- n23-3 voice alone, no game open: first heard 0.15 s median, worst 0.29 to 0.35 s (N23-3-QUESTIONS).
- Rows at 21:40 and 22:28. Pushed through 2541d1f1e; this handover's commit carries sample 4's note.

## In flight
- Nothing runs; no sdhdship.exe left (checked 23:11).

## Next, in order
00. Pace first: `python tools/pace_line.py <week> --fable <fable>`. 22:28 read 32% against 5.3% (+26.7): lean, no helpers.
1. Sleeping Dogs speed samples 4 and 5: tools/drills/watch_opening.py with --exe the Sleeping Dogs exe in C:\Games, --seconds 305 --every 2 --keys "45:enter,56:enter,82:enter,90:enter,98:enter,106:enter,114:enter,122:enter,130:enter,138:enter,266:enter,272:enter,282:walk4,290:run4", behind a wait loop for 610 idle seconds (never forced), one at a time; then tools/drills/marker_read.py <run folder> <scratch> and read the two sheets: speed = metres between the first and last readout change over the time between. Then the on-foot row's result (mean and spread of five) in STATUS.md and the drill note, and a NOTEBOOK entry (unit done).
2. Fists in Sleeping Dogs need about 60 fps (grabs here are 11 a second): recorder item or footage.
3. n23-3: order-swapped repeat pair (B then C) on measure-2026-11-24's dollar; the voice beside the game goes with question 3's packaged run (him away); cost per hour. Due Fri 27 Nov.
4. n23-4 voice scan; n23-7 (DAILY file each day with the measuring-hours line; credit row).
5. n23-1 rest: footage rows for GTA IV, GTA V, KCD2 on foot, fists, driving; reprice STATUS.md.
6. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30.
4p. Marvelous stays open (his word). No Unreal work until the browser prototype is done (advisor 288).
5p. History rewrite HELD for his word at the PC. Progress page daily (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 23 Nov 23:05: sample 4 lost: the opening's timing drifts a few seconds, the fail screen came after the 266 s Enter, so no restart. Fix: a second Enter at 272 s.
- 23 Nov 22:05: Esc at 256 s and 262 s both came after the chase failed (it fails within seconds if Wei stands); the pause menu was never reached. Not needed now: the game's prompt names Shift as sprint; no walk key found (W alone is a jog).
- 23 Nov 21:50: the distance readout moves with Naz while he runs; only the stretch where he stands is a ruler. A colour-only marker search is fooled by the market's green nets: marker_read.py adds shape.
- 23 Nov 21:52: the drill tool once left the game running a few seconds past its end; the queue line checks again after a 5 s pause.
- 23 Nov 20:39: the tool's own taps reset Windows' idle clock, so each run waits 10 minutes after the last; queue with a wait loop, never --force.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

