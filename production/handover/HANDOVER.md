# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 14:06 (the hourly run)

**Row due:** 13:42 (last row 12:42; page read 13:30; filter verdicts after 2026-11-24T12:30 UTC, advisor after 2026-11-24T13:35:00+01:00; last ack 351 at 13:32).
**Uncommitted:** nothing (this stop's commit). Local commits since da1cb7941 NOT pushed: ci fails only page-answers-fresh (next step 0).
**Stopped:** 2026-11-24 13:34 (the 12:37 run: advisors 348-351 done and acked; the lead renamed Frank Nowak in canon and RULINGS; Needs you republished empty; the KCD2 scripted plan withdrawn (copy not run); one KCD2 stream incident read as leads; history 233k of 250k, the next item would cross it)

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
- 12:37 run: **advisor 348** (his canon picks): the lead is **Frank Nowak** (ladder new owner, Nowak, Frank, Frankie; Tom and Tommy gone where seen or heard, internal id may stay); story frame: Danny Cammack the opponent, Ron inside unless Frank pays, Ron and Sheila count at the end, Mickey's envelope holds the night's fares. canon.md cast, ladder, NAMES and OPEN 2 lines; RULINGS one line. **349**: Needs you republished 13:02 with nothing open (audit, recorder, nightly-copy items closed). **350**: measuring may run to the 95% stop; cloud jobs stop at 80%. **351**: printed things finished as 2D before Unreal; the paper map his sample after Monday (order's waiting item 6). All acked (times corrected to 13:32 from Get-Date; guessed 13:03 and 13:12 first). Row 12:42.
- **The 11:53 plan withdrawn (DECISIONS 12:41):** the KCD2 and GTA V copies are never run (23 Nov 15:26 and 20:30: replaced unsigned program files). Being seen stays footage; on-foot for KCD2 and GTA V stays cadence leads; Sleeping Dogs and our build are the only drill games.
- **KCD2 being seen, vyA2Nm1BHyw** (uncut live stream, 11 Jan 2026): one incident at 1,014 to 1,060 s (likely after taking a horse, deed unseen): notice to alarm about 8 s, alarm to hostile about 3 s, search about 21 to 25 s to a guard on him. Compass colours UNVERIFIED. Notes in being-seen-readings-2026-11-24.md; STATUS row 62.
- Earlier today: the 11:37 run (advisor 347, on-foot tries 1 and 2, RDR2 step) and before: TRIED-ARCHIVE.md.

## In flight
- Nothing of this session runs. His page-copy run (scheduled task 'LEDGER: read back page answers (nightly)') stalled since 10:39; it is his window, never approve for him.

## Next, in order
00. Pace: 52% at 12:40; measuring may run to the 95% stop by Mon 30 Nov 07:00 (advisor 350); full pace on deciding rows, up to four helpers; footage reading is the session's own (helpers never click).
0. **Push blocked: page-answers-fresh.** His 10:39 run of 'LEDGER: read back page answers (nightly)' stopped at a permission prompt in its own window and was interrupted (session local_075af6d2, error_during_execution); the task is still switched OFF. He tapped Done; never ask him the same again (advisor 349). Find a route needing no approval in another window; never add an allow rule or copy round the safety check. When fresh: `python tools/page_answers.py --index`, ci to failed=none, push wip.
1b. **KCD2 being seen from footage:** first verify the compass icon colours (the game's help or a guide read in full, by a research-reader); then vyA2Nm1BHyw 2,100 to 12,600 s at 75 s steps for incidents (a console appears at 12,600 s). Sheet: crop the frame's top-centre 640x360 into a 3x3 grid on a 1600x900 canvas (method in the being-seen notes), compass readable at 1 s steps; start the call unawaited into window.sres and poll. Then more uncut streams; five incidents owed per game (RDR2 too).
1c. On-foot: cadence leads only for GTA V, KCD2, RDR2 (footage); Sleeping Dogs solid. Then chases on foot (L.A. Noire, GTA V footage); crowd reactions Q3. Fists and driving as leads on two games (advisor 341).
3. n23-3: order-swapped repeat pair (B then C) on measure-2026-11-24's dollar; the voice beside the game with question 3's packaged run (him away); cost per hour. Due Fri 27 Nov.
4. n23-4 voice scan; n23-7 (DAILY file each day with the measuring-hours line; credit row).
6. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30.
4p. Marvelous stays open (his word). No Unreal work until the browser prototype is done (advisor 288).
5p. History rewrite HELD for his word at the PC. Progress page daily (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 12:41: the 11:53 plan priced a scripted KCD2 run against a copy already ruled out; search DECISIONS for a program's name before pricing any run in it. Ack times guessed again (13:03, 13:12): Get-Date before every timestamp.
- 24 Nov 11:46: step length from following-camera footage (tries 1 and 2 of the on-foot check, both used): runs have no double support; side-on stretches swing the camera and the foot leaves the picture at landing. Guessed clock times (12:00 to 12:16) corrected from Get-Date: always Get-Date.
- 24 Nov 10:43: an awaited sheet() call in javascript_tool failed 'target closed' (the call outlasted the tool); running it unawaited into window.sres and polling works.
- 24 Nov 09:40: full-size screenshots cropped the frame's right third until the viewport was set again (the pane drops it when its width changes): set it before each screenshot.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

