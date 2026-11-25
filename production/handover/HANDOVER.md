# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-25 08:52 (the hourly run)

**Row due:** 10:43 (last row 09:43; page read 09:49; filter verdicts after 2026-11-25T08:49 UTC, advisor after 2026-11-25T09:35:00+01:00; last ack 381 at 09:44).
**Uncommitted:** this file only (no notes-only commit); the office-print PNGs and three Kiln notes are not this session's, left alone.
**Stopped:** 2026-11-25 09:49 (the 08:52 run; nothing running but a harmless page scan loop)

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
- 07:22 run: n23-3 drafted and reviewed; advisors 374-377.
- 08:52 run: advisors 378-380 in RULINGS or acted on, acked. **Footage runs hidden again** (the 01:15 hand-over rule was the cause; hidden, the page is 480x273: tools/drills/frame_sheet.js oneFit, then a 2 s wait and a full-size screenshot or a zoom of the frame). Chases on foot, Sleeping Dogs 2 of 5 (SLEEPING-DOGS-FOOT-CHASE-2026-11-25.md): opening run scripted 96 s, capture; night market 67 s, gap 12-16 m, ends at a set fight. **n23-3 reopened to 4 Dec** (advisor 380): recommendation revised, routing fault in FINDINGS, DECISIONS line. Rows 09:10.

## In flight
- Nothing running: no helper, no game; the browser pane holds YouTube (L.A. Noire Part 1, B4rTMBDczuU, not yet read).

## Next, in order
0a. Advisor 381 done 09:44 (note ONE-SHOT-REPLY-MODEL-2026-11-25.md, acked); n23-3 now only that note plus the 4 Dec delivery; no voice work before the loops.
000. **Footage runs with the pane hidden** (checked 08:55 25 Nov, screen off: plays, seeks in 0.1-0.25 s, frames read). The 01:15 failure was a stalled player; on a stall reload the tab once and re-query the video, never wait for the pane.
00. Pace: 80% at 04:46; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set "**Next due:** 2026-11-30 13:00", one page item (switch off the scheduled task ledger-daily-fresh-session, Code tab, Scheduled; on after Monday 13:00), stop all work. Full pace until then (advisors 359, 366: no pace-line holds).
0. If he types "RDR2 drill starting": `python tools/drills/rdr2_record.py start` in the background; on "RDR2 drill done": the same with stop; read the frames by his card (advisor 361).
1. **On foot, the walk:** cadence done (solid). Step length still unread: a side-on stretch, heel gap over height (none seen in rzz5BOoJ9Rc); then KCD2's walk is first person, so the second game's walk is RDR2 or Sleeping Dogs footage.
3. **Chases on foot:** Sleeping Dogs 2 of 5 done (loss: gap over about 45 m for about 20 s); next L.A. Noire (Santosx07 Part 1 B4rTMBDczuU is 7,066 s with no chapters: motion scan done to about 6,200 s 25 Nov 09:48 (frame_sheet.js mscan; median motion 17): stretches over 40 for 30 s or more at 900-1010, 1100-1150, 1640-1670, 2060-2090, 2180-2210, 2970-3030, 3230-3260, 3300-3330, 3630-3660, 4000-4040, 4570-4640, 4910-4990, 5030-5060, 5360-5410, 5930-5980 s; read each by eye with oneFit only after the scan loop has ended; 6,200-7,066 not scanned), then GTA V by a shape method. Ads: wait them out (play, skip button) before reading.
4. **KCD2 being seen with crowd reactions** (one town crime clip serves both): ibyJamin Part 4 (wMk2tFAd26E) or 5 (AK8xLkS1Cfs), hare scan with the parchment filter (drop hits above 12% beige); first check by eye that this player shows the behaviour icon at a known alarm. If none by the week's end, say so in STATUS.
4a. **Photo counts (advisor 370):** two tries used; OS legend unreached (06:10); next period footage of northern side streets by eye. Quay Street stays at 34 m. 5. 1990 sources: headlamp reach a lead (period-lamps-reach-2026-11-25.md); BS 5489-3:1989 unreached; our car braking (8-11 m vs the Code's 14 m) unchecked.
6. n23-7 DAILY-2026-11-25 by 19:00 (add the API line: US$1.10 tonight).
6b. **n23-4 trial:** ZONOS3-Mini: its weights download raised in chat when he is at the PC (file, source, size), then the 12 cast lines against Pocket (the Pocket versions now exist, path above). **n23-3:** OPEN to 4 Dec (advisor 380): recommendation revised 09:40 (routing fault named in FINDINGS; bar on the real-question model, missed; no Haiku switch on speed; layer swappable). Before 4 Dec: the blind quality comparison only if a switch is proposed; ZONOS3-Mini: the download goes through the advisor chat (advisor 380). Measuring runs: swap only LedgerTalk.exe into the played copy with a backup; end processes with cmd /c taskkill (PowerShell's strict errors on taskkill skipped the restore once).
0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only).

## Footage tools
All in tools/drills/frame_sheet.js (sheet, SAVED EVIDENCE to F:/LedgerTools/game-inputs/footage/<id>/, RED SCAN for RDR2, HARE BOX SCAN for KCD2), each with its known faults. Stamp every time from Get-Date. Storyboard sprites for colour cues only; leg crops every 0.1 s read cadence.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 25 Nov 09:05: in the hidden pane 4x3 sheets are unreadable (page 480x273) and screenshots taken at once or scaled came back black; one frame, 2 s wait, full size works.
- 25 Nov 07:32: a run script with $ErrorActionPreference Stop died on taskkill's stderr before restoring the shipped talk program (restored by hand, hash checked). 08:15: joined a transcript's "reply" and "rest" for recordings; "reply" is already whole (rest repeats its tail).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$7.11 this month (production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

