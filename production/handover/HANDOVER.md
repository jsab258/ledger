# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-25 05:37 (the hourly run)

**Row due:** 05:48 (last row 04:48; page read 04:44; filter verdicts after 2026-11-25T03:44 UTC, advisor after 2026-11-24T23:55:00+01:00; last ack 373 at 23:55; nothing new since).
**Uncommitted:** nothing; work pushed with this file.
**Stopped:** 2026-11-25 05:03 (the 03:37 run: live talk measured inside the packaged game, real questions 1.73 s median, voice 0.05 s; voice-model scan shortlisted; 1990 gaps set aside; the ruler check found no ruler; footage impossible while the pane is hidden, so stopped at the item's end with nothing else runnable before he is up; nothing running)

(At each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 23 November (production/orders/2026-11-23.md, adopted by his tap 23 Nov 08:12 Swiss; runs to Mon 30 Nov 13:00). The measuring block (n23-1) leads; the normal line 0 to 90% by Mon 30 Nov 07:00 (week-shape.json inactive); `python tools/pace_line.py`.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, leading 'v1: N of 6', ending 'Allowance: N% at HH:MM (this week the newest reading, no pace clause: advisor 366); my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate, F:'s free room and the next 12 h's need, what fills each helper place.
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
- 03:37 run: **live talk inside the packaged game** (n23-3, -AskSet=FILE with firsts-held.txt): real questions 1.73 s median, 17/30 under 2 s; voice share about 0.05 s; fall-backs uncounted (set LEDGER_TALK_TRANSCRIPT); at most US$1.10 (N23-3-QUESTIONS). **Voice scan** (n23-4): voice-scan/SHORTLIST-2026-11-25.md, ZONOS3-Mini first; Pocket already newest. **1990 gaps** set aside for the loops (DECISIONS 03:50). **Ruler check** not run, no ruler. My 17 unused tester pictures of 04:49 deleted.

## In flight
- Nothing running; no helper, no game, browser pane closed. Sleeping Dogs Part 1 (1aFCDYV4gEw): coarse frames at 88-156 s show the opening's alley run, not read finer. The pane opened hidden at 03:45 (nobody at the PC): footage waits for him to be up.

## Next, in order
000. **Footage needs the pane shown:** check `tabs_context` first; while it says hidden, do 6a/6b below, not footage.
00. Pace: 80% at 04:46; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set "**Next due:** 2026-11-30 13:00", one page item (switch off the scheduled task ledger-daily-fresh-session, Code tab, Scheduled; on after Monday 13:00), stop all work. Full pace until then (advisors 359, 366: no pace-line holds).
0. If he types "RDR2 drill starting": `python tools/drills/rdr2_record.py start` in the background; on "RDR2 drill done": the same with stop; read the frames by his card (advisor 361).
1. **On foot, the walk:** cadence done (solid). Step length still unread: a side-on stretch, heel gap over height (none seen in rzz5BOoJ9Rc); then KCD2's walk is first person, so the second game's walk is RDR2 or Sleeping Dogs footage.
3. **Chases on foot:** Sleeping Dogs Santosx07 Part 1 (1aFCDYV4gEw: a 5-10 s sheet over 80-240 s for the opening run's start and end), then Part 3 (night-market chase; ids in sleeping-dogs-foot-chase-clips), then L.A. Noire's scripted chases; the GTA V star scan only by a shape or template method (third try needs the 7 Nov rule's researched method).
4. **KCD2 being seen with crowd reactions** (one town crime clip serves both): ibyJamin Part 4 (wMk2tFAd26E) or 5 (AK8xLkS1Cfs), hare scan with the parchment filter (drop hits above 12% beige); first check by eye that this player shows the behaviour icon at a known alarm. If none by the week's end, say so in STATUS.
4a. **Photo counts (advisor 370):** two tries used; the different method: the OS 1:2,500 legend (are lamps drawn?), then period footage of northern side streets by eye. Quay Street stays at 34 m. 5. 1990 sources: footfall from the reader's file; headlamp reach now a lead (period-lamps-reach-2026-11-25.md); BS 5489-3:1989 and the 1987 Highway Code table unreached; our car braking flag (8-11 m against the Code's 14 m) unchecked.
6. n23-7 DAILY-2026-11-25 by 19:00 (add the API line: US$1.10 tonight).
6a. **n23-2 ruler check** (STATUS 25 Nov 04:49): find a ruler without Unreal: the Quay Street lamp spacing (34 m in code; read the lamps' positions from the street spec or export), then film a walk lamp to lamp (play.py start, Enter x15, `walk forward N --film --fast`, him away 10 min) and compare with the true 160/420 cm/s. Tries used: 0.
6b. **n23-4 trial:** ZONOS3-Mini: its weights download raised in chat when he is at the PC (file, source, size), then the 12 cast lines beside the game against Pocket. **n23-3:** a repeat in-game held run with LEDGER_TALK_TRANSCRIPT to count fall-backs; Sonnet 5.5 inside the game needs its talk program built with it (after the prototype); the recommendation by Fri 4 Dec, one fresh reviewer first.
0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only).

## Footage tools
All in tools/drills/frame_sheet.js (each with its known faults): sheet, SAVED EVIDENCE (pane screenshots copied to F:/LedgerTools/game-inputs/footage/<id>/ with index.json and upload date), RED SCAN (RDR2 flag), HARE BOX SCAN (KCD2). Stamp every time from Get-Date: guesses ran 10-25 min ahead today too. YouTube storyboard sprites ("playerStoryboardSpecRenderer" in the watch page) show a whole video in a few images, for colour cues only. Leg crops every 0.1 s (csheet in the 25 Nov walk note's method) read cadence.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 25 Nov 04:08: a code read said the game cannot ask a question list; wrong: -AskSet=FILE sits 60 lines below the built-in six (read the whole function). 04:49: the ruler check has no ruler (no position line, no marking sizes on record).
- 25 Nov 03:41: Git Bash's date agreed with PowerShell tonight; a wait keyed on "bash is an hour behind" fired early. Key waits on PowerShell's Get-Date.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$5.41 this month (production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

