# Ron's measures, steps 1 and 2 of RON-END-TO-END-PLAN-2026-11-08.md (8 November 2026)

Extraction only. Read on 8 November 2026. Tags: **measured** (copied or summed from a named output), **inferred** (arithmetic or a reading on measured figures), **not recorded**. Dollars are API-price equivalents from the token audit, a measure and not a bill. No dollar-per-hour rate is applied here. No API was called; no key was read.

## Step 1: dollars and hours, 2 to 8 November

**Command.** `python tools/token_audit.py --since 2026-11-02 --until 2026-11-09 --out <scratchpad folder>` (the output redirected so no repository file changed; the tool otherwise writes to production/research/token-audit/). Result line: 14,590 steps, US$1,262.99, history share 41% (measured). Of that, 400.95 USD (4,780 steps) lies in no time-log window.

**Hours.** production/time-log.jsonl, 587 lines, read whole. Hours are stop minus start, or to the next start where no stop exists (tools/token_audit.py `task_windows`, the same rule the audit books by).

**Recount of helpers.** A helper's steps carry their own timestamps, and the audit books each step to the window open at that time, so a helper working in parallel on other work lands in whatever window is open. The recount reads each helper's own description (its .meta.json) and lists its cost in the window it was booked to (script run read-only on the session logs, 7 Nov 15:00 to 8 Nov 12:00, Swiss time). A helper whose description names neither Ron nor Darren is listed as "names neither". The main session's steps are not split by person: the logs carry no person tag (not recorded).

### 1a. Time-log windows about the dress-the-cast work (Ron and Darren)

| Window (7 Nov unless stated) | Logged h | Audit US$ (item row) | of which main session | of which helpers | Source line in time-log | Tag |
|---|---|---|---|---|---|---|
| 15:21-17:07 "n02-9-dress-the-cast, n02-9-front-edge-wear, hair" (three clauses) | 1.77 | 10.69 (130 steps) | 10.25 | 0.45 | 547-548 | measured |
| 17:40:27-18:08:43 "Darren on his own body; office and sit pictures" | 0.47 | 2.22 (28) | 2.08 | 0.14 | 549-550 | measured |
| 18:42:14-20:11:42 "Darren's second fit, both hems; office board checked" | 1.49 | 6.29 (63) | 4.05 | 2.24 | 551-552 | measured |
| 21:32:28 to 22:41:13 "Darren's third try, Ron's collar points" (no stop; ended by next start) | 1.15 | 17.07 (180) | 6.60 | 10.47 | 553 | measured |
| 22:41:14-23:19:13 "whole-person films and review" | 0.63 | 2.96 (45) | 1.87 | 1.09 | 555-556 | measured |
| 8 Nov 00:22-00:40 "n02-9-dress-the-cast" (logged stop 00:40; the audit's window ends 00:24 at the next start, line 559) | 0.30 (0.03 as the audit reads it) | 1.02 (18) | 0.77 | 0.25 | 557-558 | measured |
| **Sum of the six** | **5.81** | **40.25** | **25.62** | **14.24** | | measured (sum) |

Overlap note (measured from the log): line 554 starts "n02-9 research for Monday" at 22:41:13, one second before line 555, so it holds 1 s; lines 559-560 (00:24-00:38, n02-research-proposals) lie inside the 00:22-00:40 window. Hours are task-hours, not wall-clock.

### 1b. Helpers recounted by their own description (the audit's per-window dollars are not floors for Ron or Darren)

| Helper (description) | Own span (Swiss) | US$ | Booked to | Names | Tag |
|---|---|---|---|---|---|
| Carry Tom's jeans, jumper to Ron, Darren importer | 15:27-15:29 | 0.32 | 15:21 window | Ron and Darren | measured |
| Review worn paint on Mickey's front | 15:35 | 0.12 | 15:21 window | neither | measured |
| Review office and sit pictures | 17:40-17:41 | 0.24 (0.14 in the 17:40 window, 0.11 in no window) | 17:40 window / none | neither | measured |
| Diagnose Darren's chest slits | 19:16-19:25 | 2.24 | 18:42 window | Darren | measured |
| Diagnose the quay end's stop | 21:32-21:38 | 1.87 | 21:32 window | neither | measured |
| Seven research helpers (districts in memory, people look alive, studios do QA, published mappings, three proposal writers) | 22:16-22:29 | 8.59 (0.59+0.54+0.57+0.17+2.48+2.45+1.79) | 21:32 window | neither | measured |
| Final review: Darren dressed | 23:11-23:13 | 0.53 | 22:41 window | Darren | measured |
| Final review: Ron dressed | 23:11-23:13 | 0.56 | 22:41 window | Ron | measured |
| Review three research proposals | 8 Nov 00:23-00:25 | 0.75 (0.25 in the 00:22 window, 0.50 in proposals) | 00:22 window | neither | measured |
| Final review of Ron's collar back | 8 Nov 04:42-04:43 | 0.70 | no window | Ron | measured |
| Page check of the dressed men | 8 Nov 04:45-04:47 | 0.62 | no window | Ron and Darren | measured |

Recount result (inferred, sums of the rows above):
- The 21:32 row's 10.47 of helper dollars are all helpers naming neither (1.87 + 8.59 = 10.46, rounding 0.01). Its main-session 6.60 is not split: that session also briefed those helpers (not recorded).
- Helper dollars in 1a naming Ron or Darren: 0.32 + 2.24 + 0.53 + 0.56 = 3.65. Helper dollars outside any window naming them: 0.70 + 0.62 = 1.32.
- Main-session dollars in the six windows: 25.62, not split by person or by clause (not recorded).
- Dollars for the six windows with the helpers naming neither removed: 25.62 main + 3.65 named helpers = 29.27 inside the windows; 30.59 with the two out-of-window Ron reviews (1.32). Tag: inferred. The main-session part still contains front-edge wear, hair, the office board and the research briefing.

### 1c. Knit and neckband windows (8 Nov; task text names no person; the plan reads them as both men)

| Window | Logged h | Audit US$ | Steps | Source line | Tag |
|---|---|---|---|---|---|
| 10:44-10:50 plan from Mafia's sweater, CC0 route | 0.10 | 1.67 | 23 | 579-580 | measured |
| 10:50-10:55 CC0 knit searched, fetched, looked at | 0.08 | 0.90 | 12 | 581-582 | measured |
| 10:55-10:59 knit and rib tiles | 0.07 | 0.45 | 5 | 583-584 | measured |
| 10:59-11:05 UV scale measured, step 3 recipe | 0.10 | 1.13 | 14 | 585-586 | measured |
| **Sum** | **0.35** | **4.15** | 54 | | measured (sum) |

All 54 steps are main-session; no helper step lay in these windows (recount, measured). The log's last line (587, 15:24:24, n02-9-qa-lean) is a later task. No time-log window covers the knit work after 11:05: not recorded.

### 1d. Other time-log rows that name Ron or Darren (not the dress-the-cast work)

| Window | Logged h | Audit US$ | Names | Source line | Tag |
|---|---|---|---|---|---|
| 2 Nov 13:36-14:24 "n02-4-corner-people: idle breaks ... Ron's moustache strands kept ... n02-6-3 research helper" (five clauses) | 0.81 | 58.86 (759 steps; largest kind reviewing by helpers) | Ron's moustache (hair) | 337-338 | measured |
| 2 Nov 14:24-14:48 "Sheila's hand into her hip ..., Ron's spot; study C ..." (several clauses) | 0.39 | 31.83 (322) | Ron's spot | 339-340 | measured |
| 4 Nov 20:21-20:30 "the Tea Rooms man (Darren) kept out of page pictures" | 0.15 | 2.68 (51) | Darren, page pictures | 464 | measured |
| 5 Nov 18:21-18:28 "the walk's lost Ron and Darren traced to the tester's clock" | 0.12 | 2.36 (29) | both, walk | 494 | measured |
| 8 Nov 06:50-07:05 "n02-9-iron-cover: cast tread, fall, Ron's spot; quay-end diagnosis brief" | 0.25 | 6.71 (128) | Ron's spot | 567-568 | measured |
| Audit rows only: "n02-9-dress-the-cast" with no clause, all windows booked there | | 1.02 | | | measured |

No row names Ron's hair alone, his voice or his routine: not recorded. No row of 2 to 8 Nov is tagged by person; all splits above are by task text only.

Not covered by 2 to 8 Nov: the 7 Oct windows (line 32 start 18:32:43 to 33 stop 20:32:16, 1.99 h, "Ron's outfit third try and review, the records"; 40 start 21:50:00, 0.75 h, "sitting works (Ron seated)"; 58 start 05:08:00 on 8 Oct, 0.82 h, "Ron's rank spot moved"), which predate the audit's window. No token audit for them: not recorded (dollars).

## Step 2: work before 5 October, from git (read-only `git log`)

Git gives commit times, not hours worked. Each bound below is elapsed time between two commits, inferred, and is an upper bound on work only if nothing else was done between them, which commit text does not show. The repository's first commit is 9 Jul 2026 07:17 (`git log --reverse`, measured). The time log begins 5 Oct (plan; not re-read here). Hours of work: **not recorded** unless a row says otherwise.

| Item | Commit evidence (command) | Bound, hours (I) | Tag |
|---|---|---|---|
| Ron's casting folder, all history | `git log --format=... -- production/casting/ron-kirby/`: 10 commits; first 34a785957 24 Sep 23:13 ("sheets with concept portraits for Sheila Dunn, Ron Kirby and Darren Milner"); last before 5 Oct 5d80bbe8a 30 Sep 14:59; then 757c41de6 8 Nov 14:54 | 5.7 days elapsed from first to last pre-October commit (about 136 h elapsed); work hours not recorded | inferred |
| Concept sheet and casting names | 34a785957 24 Sep 23:13; the commit before it (d85a16a70) 22:42 | commit gap 0.52 h to the previous commit; the commit holds three people's sheets | inferred |
| Rocco/Ron body and face from the plugin's shipped people | DECISIONS 24 Sep line 18 ("Rocco from Jorge"); approved as concept "Ron Kirby C1" in e51b35cb1, 25 Sep 22:07 (`git log -S"Ron Kirby C1 (too young)"`) | not boundable: no commit holds the making. Body export MH_RoccoP2 date not in git read | not recorded |
| Face frozen as Ron P2 | RULINGS text dates it 30 Sep (plan). First commit adding the string "P2" to DECISIONS.md or RULINGS.md: 9ddea5ebf 1 Oct 21:28 (`git log -S"P2"`; the string may not be Ron's) | not boundable | not recorded |
| First donkey jacket, worn by Ron and Darren in the game | 99d6ba413 25 Sep 01:11; previous commit 4fb0463a4 01:10, before that 0affb95a6 00:33 | 0.6 h elapsed since 00:33 (the jacket's time before that is in no commit) | inferred |
| Jacket's later tests (Marvelous), Ron's body | 719751abd 2 Oct 10:33 ("proof jacket drapes on Ron's own body"); 753da87e5 11:42 blind review FAIL; 404511115 15:16 | commit span 10:33 to 15:16 = 4.7 h elapsed, other work included | inferred |
| Ron's voice (p227 kept; Pocket set aside) | DECISIONS 25 Sep line 41 and 28 Sep line 85 (voice work); the pick "Ron stays on the game's own engine" first in 00d30612c 30 Sep 08:25 | not boundable | not recorded |
| STREET-LINES.md (159 lines) | one commit, 69fac1615 30 Sep 09:15 (`git log -- production/casting/ron-kirby/STREET-LINES.md`, count 1); previous commit 89168d218 08:18 | 0.95 h elapsed from the previous commit; commit also holds the talk's grounding change and the thirty regulars | inferred |
| STREET-LINES approval | 5d80bbe8a 30 Sep 14:59 (casting folder's last pre-October commit) | no bound | not recorded |
| Routine rows in hook-cast.json | `git log -- production/specs/hook-cast.json`: 23 commits; first 3d31ddc53 28 Sep 16:20; first containing the string "routine": same commit (`git log -S'"routine"'`); previous commit 14d155b43 16:13 | file exists from 28 Sep 16:20; routine rows' own hours not boundable (the commit's title is about what the town heard) | not recorded |
| Face and body records DECISIONS 28 to 30 Sep (Ron lines: 29, 30 Sep entries on card, claim check, street lines, "Mickey's heart") | 175 commits touch DECISIONS.md between 20 Sep and 5 Oct (`git log --since=2026-09-20 --until=2026-10-05 -- DECISIONS.md`) | not boundable per line | not recorded |

## Darren's same rows beside Ron's (the repeat)

Darren's folder production/casting/darren-milner/ has 8 commits, first 34a785957 24 Sep 23:13 (the same commit as Ron's sheet), last 39cdf3f06 26 Oct 16:35 ("Darren in Pocket, the Newcastle voice"). Darren's S6 pick: DECISIONS 30 Sep, first in 00d30612c 30 Sep 08:25 (`git log -S"Darren is S6"`); S6 face in the game 74dbd477f 2 Oct 12:35. Darren's body (MH_SamP2 or the like) and face records before 5 Oct: not recorded as hours.

| Row | Ron | Darren | Tag |
|---|---|---|---|
| Windows naming only that person (logged h; audit US$) | 8 Nov 00:22-00:40 "Ron's collar try 2": 0.30 h; 1.02 US$ (the audit's window is 2 min) | 7 Nov 17:40-18:08 "Darren on his own body": 0.47 h; 2.22 US$. 7 Nov 18:42-20:11 "Darren's second fit": 1.49 h; 6.29 US$ | measured |
| Window naming both | 21:32-22:41 "Darren's third try, Ron's collar points": 1.15 h; 17.07 US$ (10.47 of it helpers naming neither); 22:41-23:19 whole-person films and review: 0.63 h; 2.96 US$ | same two windows | measured |
| Shared 15:21-17:07 window (dress, front wear, hair) | 1.77 h; 10.69 US$ | same window | measured |
| Helpers naming the person (US$) | Final review Ron dressed 0.56; Final review of Ron's collar back 0.70 (8 Nov 04:42, no window) | Diagnose Darren's chest slits 2.24; Final review Darren dressed 0.53 | measured |
| Helpers naming both (US$) | Carry jeans, jumper to Ron, Darren importer 0.32; Page check of the dressed men 0.62 | same | measured |
| Equal-split of the six dress windows by the plan's rule (hours) | the plan's own rows give Ron 1.98 to 2.23 h logged (plan lines 43-56); not recomputed here | not computed in the plan or here | inferred (plan's figure copied) |
| Knit and neckband (0.35 h; 4.15 US$) | named on neither; plan says both men | named on neither | measured, shared |
| Outcomes in the 7 Nov 23:19 stop note | "Ron fails on the head mesh through the collar's back" | "Darren passed review" | measured (line 556) |
| Pre-5 Oct commits, casting folder | 10 commits, first 24 Sep 23:13, last pre-October 30 Sep 14:59 | 8 commits, first 24 Sep 23:13 | measured |
| Hair, voice, routine hours | not recorded | not recorded | not recorded |
| Page pictures/walk rows | 5 Nov walk row 0.12 h, 2.36 US$ (both); 8 Nov "Ron's spot" 0.25 h, 6.71 US$ | 4 Nov "Tea Rooms man (Darren)" 0.15 h, 2.68 US$ | measured |

## Unread or unreached

- The main-session dollars of the six dress windows cannot be split by person or by clause (no person tag in the logs).
- Time-log lines after 587: none existed at reading.
- Ron's body-export date, Ron's face freeze date and every pre-October hour: not recorded; git gives commit times only.
- The helpers recount reads descriptions only; helpers' result text was not read.
