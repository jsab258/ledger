# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 16:37 (the hourly run)

**Row due:** 17:49 (last row 16:49; page read 17:05; filter verdicts after 2026-11-24T16:05 UTC, advisor after 2026-11-24T16:12:00+01:00; last ack 357 at 16:56).
**Uncommitted:** nothing after this commit; pushed to wip.
**Stopped:** 2026-11-24 17:19 (the 16:37 run: advisors 356 and 357 done; RDR2 being seen not solid on review, four spells' edges saved; history near its limit)

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
- 16:37 run: **advisor 356**: RULINGS back under its cap (4,896) by notation only (ranges 4-6, advisor numbers off date labels; enforcer keys follow); cap item closed; pushed. **Advisor 357** (RDR2 installed): the copy in C:/Games is NOT run (RDR2.exe fails Rockstar's signature, Launcher_with_cracktro.exe and 1911.dll unsigned; the 23 Nov 20:30 safety line); one money item on his page, rdr2-store-copy-2026-11-24 (footage recommended). Progress page refreshed (live index kept; progress.json and 24 Nov pictures). DAILY-2026-11-24.md written (n23-7).
- **RDR2 being seen: fresh review NOT SOLID** (review-being-seen-rdr2-2026-11-24.md): nothing saved, 1drjFJjei8g edited with unknown platform, No13 maybe the solid-red case. Since then edges SAVED for No8, No9 x2, No13 (F:/LedgerTools/game-inputs/footage/<id>/, index.json each, uploads 9 and 13 Mar 2025); the readings' solid-red claim corrected.
- **n23-3 question 4** from the bench totals: Sonnet 5.5 about US$0.0057 a line, US$0.09 an hour at 15 replies (a floor: first questions); per-model rows need a per-model tally in ClaimBench.
- Earlier runs today: advisor 355 in RULINGS; RDR2 five readings; n23-3 repeat pair.

## In flight
- Nothing runs. The browser pane is on YouTube No9.

## Next, in order
00. Pace: 67% at 16:49; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set "**Next due:** 2026-11-30 13:00", one page item (switch off the scheduled task ledger-daily-fresh-session, Code tab, Scheduled; on after Monday 13:00), stop all work.
0. Read the verdict on rdr2-store-copy-2026-11-24 (footage or store). A row is owed at 17:49.
1. **RDR2 being seen to SOLID:** replace 1drjFJjei8g (edited) and decide on No13 (or replace it): read LordGedi No3, No4, No6 (or a second player's uncut console session) for riding-off spells; save every edge the new way (below); then one fresh final-reviewer (no clicks) against the readings and the saved pictures.
2. KCD2 being seen, five uncut samples (footage found none unmodded so far; long console sessions, compass crop); report the shortfall plainly if none within about 1 h.
3. On-foot cadence leads; chases on foot leads (L.A. Noire, GTA V); crowd reactions Q3 leads on two games.
4. n23-3: per-model tally in ClaimBench before the per-model rows; prices re-read with dates. The probes' "I'm Tom": waiting list.
5. n23-4 voice scan; n23-7 (DAILY tomorrow by 19:00; credit row). Advisor 320 (backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only; publish the LIVE index.html read back, not the local one, which differs).

## Saving footage evidence (works, 24 Nov 17:10)
In the pane: define draw(vid, t) (seek, wait for readyState 4, draw the frame on a fixed canvas the pane's width, yellow label of id and time), wait 2 s, then computer zoom region [0,0,800,450] at scale 0.5: the result names a file in the session's tool-results folder; copy it to F:/LedgerTools/game-inputs/footage/<id>/<t>-<label>.png and list it in index.json with the upload date (meta itemprop uploadDate). Without the 2 s wait the capture lags one draw; trust only the label.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 17:08: posting crops from the YouTube page to a local receiver (127.0.0.1) is refused by the pane ("Unsafe attempt to load URL"); the receiver was deleted. Use the pane's own saved captures.
- 24 Nov 16:52: the installed RDR2 is a modified copy; not run (safety line). Do not price drills in it.
- 24 Nov 15:58: changing his rulings' meaning is refused by the PC's safety check; notation-only tightening passed at 16:43 (advisor 356).
- 24 Nov 15:44: a plain backward seek stalled the video; wait for 'seeked' and readyState before drawing.
- 24 Nov 14:17: check any PC stream for mod lists, consoles or overlays before reading an incident.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$5.41 this month (8, 16, 23 Nov US$0.95, 24 Nov US$0.69; production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

