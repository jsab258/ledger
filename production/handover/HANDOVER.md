# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 08:07 (the hourly run)

**Row due:** at the next start (last row 08:10; page read 08:08; filter verdicts after 2026-11-24T07:08 UTC, advisor after 2026-11-24T08:10:00+01:00; last ack 2026-11-24-0745-338 at 08:10).
**Uncommitted:** nothing (08:07 run committed his page item, DECISIONS and this file); that commit, the 01:36 run's and da1cb7941 (the solid speeds) are NOT pushed: ci fails page-answers-fresh (see next step 0).
**Stopped:** 2026-11-24 08:09 (the 08:07 run: advisor 338 answered, his page item rewritten (v187); stopped on the pace rule, +24.4 points; no jobs of its own started)

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
- 21:36 run: advisors 334-336 recorded and acked (RULINGS at 4,899 of its cap; DECISIONS 23 Nov 22:00); NOTEBOOK's nine lessons; recipe map updated.
- Sleeping Dogs speeds method: the chase's distance readout toward the standing Naz; Enter on the fail screen restarts in about 6 s; tools/drills/marker_read.py (SLEEPING-DOGS-DRILL-2026-11-23.md).
- n23-3 voice alone, no game open: first heard 0.15 s median, worst 0.29 to 0.35 s (N23-3-QUESTIONS).
- Rows at 21:40 and 22:28. Pushed through 2541d1f1e; this handover's commit carries sample 4's note.
- 07:22 run: advisor 337 (for his dates question today) answered early: STATUS.md section 'Decides or a lead is enough'; six rows decide, about 29 h strict (drills 4.5, footage 24), 6.5 h as leads; acked 07:27; row 07:27; pace 35% vs 10.2% (+24.8). Listening extra rows unverified (sheet on the lane branch).
- 03:36, 04:22, 05:06, 05:51, 06:36 runs: page read, nothing new, a row each, pace +25 to +26; started nothing.
- 01:36 run: page read (nothing new), read-back refused again, his page item added, row 01:39; pace 34% vs 7.0% (+27).
- 23:51 run: **Sleeping Dogs on foot SOLID** (five samples each): sprint 5.5 m/s (5.5 x4, 5.6), jog 4.5 m/s (4.1 to 4.9); STATUS.md solid count three; drill note and NOTEBOOK entry; DAILY 23 Nov measuring line closed (about 2.2 drill hours). Committed da1cb7941, not pushed. Rows 23:56 and 00:53.

## In flight
- Nothing runs; no sdhdship.exe left (checked 00:47); drill frames read and deleted.

## Next, in order
00. Pace first: `python tools/pace_line.py <week> --fable <fable>`. 00:52 read 33% against 6.6% (+26.4): lean, no helpers; the 23:51 run stopped after its item on the pace rule (start nothing new while over 6 ahead).
0. **Push blocked: page-answers-fresh fails.** Cause (advisor 338, 08:08): the nightly task "LEDGER: read back page answers (nightly)" is switched off since 12 Nov; the session's own copy is refused by the safety check (two tries, 24 Nov 00:50 and 01:38). His page item page-read-back-2026-11-24 (v187) now asks one switch: Scheduled, switch it on, Run now. Never add an allow rule to the session's own permissions and never copy round the refusal. When the task has run (its answers folder dated today), `python tools/page_answers.py --index` if needed, ci to failed=none, push wip, close the item.
0b'. When he answers his dates question: follow it on STATUS.md's decides section (if he picks decides-only, footage for the six decides rows first).
1. Sleeping Dogs on foot is done (solid). Driving and fists in Sleeping Dogs still open: fists need about 60 fps (item 2).
2. Fists in Sleeping Dogs need about 60 fps (grabs here are 11 a second): recorder item or footage.
3. n23-3: order-swapped repeat pair (B then C) on measure-2026-11-24's dollar; the voice beside the game goes with question 3's packaged run (him away); cost per hour. Due Fri 27 Nov.
4. n23-4 voice scan; n23-7 (DAILY file each day with the measuring-hours line; credit row).
5. n23-1 rest: footage rows for GTA IV, GTA V, KCD2 on foot, fists, driving; reprice STATUS.md.
6. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30.
4p. Marvelous stays open (his word). No Unreal work until the browser prototype is done (advisor 288).
5p. History rewrite HELD for his word at the PC. Progress page daily (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 01:38: page read-back with out_dir refused again (Undermining Oversight); two tries used; asked on his page.
- 24 Nov 00:50: page read-back with out_dir refused by the permission check (Undermining Oversight); ci then fails page-answers-fresh; nothing pushed.
- 24 Nov 00:10: sample 5 rerun filmed a white window for all 305 s (every grab mean 255): the game likely not recovered after the forced close. Try 2 queued at once; a second white run sets the fault aside.
- 24 Nov 00:09: sample 5 lost: a queue started with a shell '&' was still alive though ps did not show it, so a second queue launched a second game 13 s later; the game is single-instance, both runs ended (20 and 0 frames) and the game was left running (closed by taskkill /T). Queue only with run_in_background, one at a time; check with PowerShell's process list, not ps.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

