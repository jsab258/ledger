# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 10:37 (the hourly run)

**Row due:** 11:46 (last row 10:46; page read 10:53; filter verdicts after 2026-11-24T09:40 UTC, advisor after 2026-11-24T10:30:00+01:00; last acks 342 to 346 at 10:41).
**Uncommitted:** nothing (commits 3ca4dcf5b and this one). Local commits since da1cb7941 NOT pushed: ci fails page-answers-fresh (next step 0).
**Stopped:** 2026-11-24 10:55 (the 10:37 run: advisors 342 to 346 in RULINGS and acked; being seen KCD2 first lead; on-foot method written; history 230k of 250k, the next footage try would cross it mid-piece)

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
- 10:37 run: **advisors 342 to 346** (his 32 decisions-page answers and corrections) in RULINGS: one sub-line under the release (map kept; clock 48 real minutes a game day, about 7 game weeks; pastimes; buyback; in/out lists; shipping; PEGI 18 within canon) and edits to replaced lines (no thinking sound; empty unit dressed; painted surrounds; photographs on shape; 2 s written line; one listening page; weekly stop **95%**, not 88%). Older lines tightened to keep 4,900; four enforcer openings repointed. Acked 10:41; DECISIONS 10:41. The keeper (cloud blueprint lane) reads RULINGS; no KEEPER-LOG exists here. Row 10:46.
- **Being seen**: KCD2 olf2KJN5VV8: hitting a horse to a guard's challenge about 14 s, a bystander in about 2 s (edited clip, lead); AlNbGAgF3EM no incident; vyA2Nm1BHyw (4 h stream) uses a debug console: leads only. RDR2 2uugZeY_mLQ: witness to wanted about 8 s; wanted held 53 s or more; the earlier 'cleared in 10 s' was a cut, withdrawn. STATUS row updated.
- **On-foot method** written (ON-FOOT-METHOD-2026-11-24.md): cadence x step-to-height ratio x community height, checked first on Sleeping Dogs' solid 5.5 / 4.5 m/s within 10%. First look at CGho8_UOzSk: camera behind or three-quarter; about 3.5 steps a second at a 0.1 s grid (too coarse).
- **Page copy**: he tapped 'done' on page-read-back at 10:39 and started the nightly task once by hand; that run (local_075af6d2...) has shown no activity since 10:39:57 (likely waiting on an approval in its own window); the task itself is still switched OFF. Told him in chat (NEEDS YOU).
- Earlier today (09:36 and 08:51 runs, crowd counts solid, first being-seen readings, readers) and 23 Nov: TRIED-ARCHIVE.md, 'Moved 24 Nov 10:57' (written 10:55).

## In flight
- Nothing of this session runs. His page-copy run (scheduled task 'LEDGER: read back page answers (nightly)') stalled since 10:39; it is his window, never approve for him.

## Next, in order
00. Pace: this week measuring may run to about 70% (advisor 339), story about 10 more; full pace on the deciding rows with up to four helpers; footage reading is the session's own (helpers never click). Finish target Sat 28 Nov. Allowance 44% at 10:41.
0. **Push blocked: page-answers-fresh fails.** The nightly task "LEDGER: read back page answers (nightly)" is off since 12 Nov; the session's copy is refused by the safety check (two tries). His page item page-read-back-2026-11-24 asks one switch. Never add an allow rule, never copy round the refusal. When the task has run (answers folder dated today): `python tools/page_answers.py --index` if needed, ci to failed=none, push wip, close the item.
1b. **On-foot speeds**: the Sleeping Dogs check first (ON-FOOT-METHOD's First look): cadence at 1/30 s seeks over 4 s of steady running (CGho8_UOzSk at about 564-617 s, or the no-commentary walkthroughs nDThIiEgyDA, q-XdObZ24eA), plus side-on footfalls for the step ratio; within 10% of 5.5 / 4.5 m/s or question the method. Then five runs a gait for KCD2, GTA V, RDR2; the walk from KCD2 or GTA V.
1c. **Being seen** (being-seen-readings, its Next): titled crime clips are edited; look for long uncut KCD2 sessions (streams, 'Part N' no-commentary); vyA2Nm1BHyw's first three hours by 10-minute sheets before 12,600 s (leads only); RDR2 IBsRlI5GfWs 73-77 s. Paste frame_sheet.js after each navigation; start sheet() without await (window.sres, poll after about 20 s; an awaited call closed the target); viewport 1600x900 before each screenshot; desktop after.
1d. Chases on foot (L.A. Noire, GTA V); crowd reactions Q3. Fists and driving as leads on two games each (advisor 341).

2. Fists (if kept deciding) need about 60 fps: the recorder item or footage.
3. n23-3: order-swapped repeat pair (B then C) on measure-2026-11-24's dollar; the voice beside the game goes with question 3's packaged run (him away); cost per hour. Due Fri 27 Nov.
4. n23-4 voice scan; n23-7 (DAILY file each day with the measuring-hours line; credit row).
6. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30.
4p. Marvelous stays open (his word). No Unreal work until the browser prototype is done (advisor 288).
5p. History rewrite HELD for his word at the PC. Progress page daily (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 10:43: an awaited sheet() call in javascript_tool failed 'target closed' (the call outlasted the tool); running it unawaited into window.sres and polling works.
- 24 Nov 09:40: full-size screenshots cropped the frame's right third until the viewport was set again (the pane drops it when its width changes): set it before each screenshot.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

