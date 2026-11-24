# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 14:06 (the hourly run)

**Row due:** 15:55 (last row 14:55; page read 14:58; filter verdicts after 2026-11-24T13:00 UTC, advisor after 2026-11-24T15:00:00+01:00; last ack 354 at 14:59).
**Uncommitted:** nothing (this stop's commit, pushed if ci ends failed=none).
**Stopped:** 2026-11-24 15:02 (the 14:06 run: advisors 352-354; RDR2 4 of 5; history past its point)

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
- 14:06 run: **push unblocked**: his page's answers read back by this session (ArtifactData query of verdicts with out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then page_answers.py --index); 15 commits pushed 14:13. The nightly copy task stays off (his).
- **Advisor 352**: weekly stop 90% until Mon 30 Nov 13:00 (RULINGS 7/10 Nov line, NOW.md). **353**: each row carries measuring hours and the meter's rise; first estimate about 5 points a measuring hour (upper bound). **354**: the stop-file route, done in part: tools/nightly_walk.py now ends before packaging or the AI tester while production/weekly-stop.json holds ({"until": "2026-11-30T13:00"}), self-test 35/35. All acked 14:27 and 14:59.
- **Being seen**: KCD2 stream vyA2Nm1BHyw is modded (a mod list and a wanted overlay at 2,625 s): leads only. Compass colours from two guides: white searching, yellow noticing, red combat (kcd2-compass-icons-2026-11-24.md). KCD2 clips read (AlNbGAgF3EM PS5, wLgaIdxZI3M, 39yKmjz13Ts): no sample. **RDR2 4 of 5 uncut samples**: 1drjFJjei8g (65 s), ks7t4W22p3U No8 PS5 (71 s; witness to wanted 106 s at a remote ranch), -gj2OL_TeG8 No9 PS5, two in Valentine (71 s and 42 s; witness to wanted 10 and 44 s). Three of four from one player (LordGedi). Method: the HUD-corner flag sheet, 48 cells at 40 s (RECIPE chapter 1); ads pause it, it resumes.
- **n23-3 repeat pair** (B then C): Sonnet 5.5 median 1.27 s, 41/60 under 2 s; Sonnet 5 2.09 s, 29/60; pooled over two days 1.41 against 1.64 s. US$0.69 (task measure-2026-11-24). N23-3-QUESTIONS-2026-11-23.md.

## In flight
- Nothing runs. The browser pane is on YouTube.

## Next, in order
00. Pace: 63% at 14:55; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row saying so, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set this file's "**Next due:** 2026-11-30 13:00" line (the gate then holds starts at WAIT), put one item on his page (switch off LEDGER: the hourly fresh session, Code tab, Scheduled; on after Monday 13:00), and stop all work.
0. Advisor 354's rest: say in the next row the route taken (the stop file holds the night walk, done; the hourly task needs his switch, about US$0.46 a held run, up to four an hour). Each row: measuring hours this run and the meter's rise (advisor 353).
1. **RDR2 being seen, sample 5**: the LordGedi PS5 series' unread parts (No3 NsBRalZza9M, No4 EF7TwaM9q_g, No6 vhJXGyjhH-4, No10 8q0sla5lgeQ, No11 BsmPLcJ2PRg, No12 BNiEtuMviwU, No13 KvZfR0IU9ms); prefer a second player for the fifth (otherwise four of five from one player, stated beside the number). Then one fresh reviewer on the five against being-seen-readings-2026-11-24.md before the row is called solid.
2. KCD2 being seen stays leads this week (titled clips show the talk after a catch; no uncut console session with crimes found). Only if time remains before 90%: long "KCD2 PS5 no commentary" sessions with crime themes, read with the compass crop.
3. n23-3: cost per hour (question 4) can be computed now from the bench's dollars and turn counts; the voice beside and inside the packaged game (question 3) needs Unreal and a free machine with him away, not before the prototype (advisor 288) unless the order says so.
4. On-foot cadence leads (GTA V, KCD2, RDR2 footage); chases on foot leads (L.A. Noire, GTA V); crowd reactions Q3 (advisor 341: leads on two games).
5. The bench's held probes say "I'm Tom": a follow-up for the story lane (the lead is Frank since advisor 348); put it on the order's waiting list; do not edit the bench set mid-measure.
6. n23-4 voice scan; n23-7 (DAILY file 19:00 with the measuring-hours line; credit row). Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 14:35: a shell append with no input waited for ever (moved to the background, then stopped); write files with a heredoc, Write or Edit only.
- 24 Nov 14:17: the KCD2 stream was taken as unmodded until a mod list showed at 2,625 s: check any PC stream for mod lists, consoles or overlays before reading an incident.
- 24 Nov 12:41: the 11:53 plan priced a scripted KCD2 run against a copy already ruled out; search DECISIONS for a program's name before pricing any run in it. Always Get-Date before a timestamp.
- 24 Nov 10:43: long awaited javascript_tool calls fail 'target closed'; start unawaited into window.sres and poll. The pane drops the 1600x900 viewport when its width changes: set it before each screenshot.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$5.41 this month (8, 16, 23 Nov US$0.95, 24 Nov US$0.69; production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

