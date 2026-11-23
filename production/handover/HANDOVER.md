# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-23 20:07 (the hourly run)

**Row due:** at the next start (last row 20:26; page read 20:51: nothing new; filter verdicts after 2026-11-23T18:26 UTC, advisor after 2026-11-23T19:44:00+01:00; last ack 2026-11-23-2026-eff written 20:26 stamp).
**Uncommitted:** nothing.
**Stopped:** 2026-11-23 21:03 (the 20:07 run: the fast film ruled fit for speeds; Sleeping Dogs opening got through by script and a first walk and run filmed; advisor efficiency review acked; history near its point)

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
- Earlier runs (13:07-19:27): order adopted, star reader, installed-game method, catalogue, n23-5 recipe rewrite (pushed 8b3580705), n23-3 first numbers; see the day's commits.
- 20:07 run: advisor's efficiency review (19:44) acked 20:26: the drills no longer wait on the recorder. play.py walk --film --fast (pushed 45354ec65): 48 grabs, about 27 new pictures a second in our build, each within about 30 ms (FILM-RULER-2026-11-23.md). DAILY-2026-11-23 carries the measuring-hours line (every DAILY file from now). Recorder item's reasons updated on his page (only for quick moves now).
- Sleeping Dogs: tools/drills/watch_opening.py (fixed timed taps and walk/run holds, film, stops at his touch, closes the game). Opening got through on try 2 of 2: control in the night-market chase at about 254 s after launch; drill 1 filmed a 4 s walk at 258 s and a 4 s run at 265 s (about 11 grabs a second in this game, each about 85 ms). SLEEPING-DOGS-DRILL-2026-11-23.md; STATUS.md on-foot row 0.9 h logged.
- GTA IV, GTA V, KCD2 copies NOT run: replaced unsigned launcher files; a safety line kept despite his 16:10 ruling (DECISIONS 23 Nov 20:30). Their rows go to footage. Say so plainly if he asks; do not re-ask him.

## In flight
- Nothing runs. Sleeping Dogs closed by the tool (check no sdhdship.exe before any build).

## Next, in order
00. Pace first: `python tools/pace_line.py <week> --fable <fable>`. 20:24 read 27% against 4.1% (+22.9): lean, no extra helpers.
1. Sleeping Dogs walk and run speeds from drill 1's frames (F:/LedgerTools/tmp/drills/sdhdship-opening-2026-11-23-2055, walk4-* and run4-*, times in times.jsonl rows with "hold"): first measure a length in the game itself (the market's herringbone paving brick, or the on-screen distance to Naz while he stands), then Wei's progress per frame; code reads, two sheets by eye. Then four more runs for five (each run restarts from launch, keys as the 2055 run: Enter 45, 56, every 8 s 82-138, walk4 258, run4 265; about 7 min each; only after 10 idle minutes, and the tool's own keys count as use). Whether Shift changes the gait: compare walk4 and run4 frames.
2. Drill rows next in Sleeping Dogs: a punch (fists row) needs about 60 fps: grabs here are 11 a second, so fists stay on the recorder item or footage.
3. n23-3 (paused): order-swapped repeat pair (B then C) on measure-2026-11-24's dollar; voice alone (latency.py without --live, --voice game, --prewarm; free); cost per hour. Due Fri 27 Nov.
4. n23-4 voice scan; n23-7 (DAILY file each day with the measuring-hours line; credit row).
5. n23-1 rest: footage rows for GTA IV, GTA V, KCD2 on-foot/fists/driving; reprice in STATUS.md with today's drill hours.
6. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30.
4p. Marvelous stays open (his word). No Unreal work until the browser prototype is done (advisor 288).
5p. History rewrite HELD for his word at the PC. Progress page daily (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 23 Nov 20:31: a game started by the tool from the background is not handed the front; no key went (by design); fixed by play.focus before the first tap.
- 23 Nov 20:39: the tool's own taps reset Windows' idle clock, so the next run waits 10 minutes after the last; queue runs with a wait loop, never --force.
- 23 Nov 20:08: the walk-speed check against Tom's 160 cm/s was impossible: the game writes no player position. Judge our build's speed on screen against a known length, as in the installed games.
- 23 Nov 19:1x: ClaimBench --moment sends every held question to Haiku (a bench-only rule); the game's routing is arm C (--model claude-sonnet-5 --reply-thinking-off). Sonnet 5 beat 5.5 tonight, one run each, not settled.
- 23 Nov 17:3x: a caption-box detector run twice at once fought over the video's position; run one scan at a time. Silent detail videos: read their caption strip by frames.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

