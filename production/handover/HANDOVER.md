# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-25 17:22 (the hourly run)

**Next due:** 2026-11-30 13:00 (weekly stop at 90%, read 18:23 25 Nov; production/weekly-stop.json). Last row 18:26; page read 18:20: verdicts after 2026-11-25T12:58 UTC (none since), advisor after 2026-11-25T17:25:00+01:00 (none since); last ack 395 at 17:26.
**Uncommitted:** nothing of this session's; the office-print PNGs and three Kiln notes are not this session's, left alone.
**Stopped:** 2026-11-25 18:29 (the 17:22 run: weekly stop at 90%, read 18:23; advisor 395 acted on; KCD2 being seen one uncut sample; everything pushed; nothing running)

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
- 17:22 run: advisor 395 recorded and acked 17:26 (three build stages in playing order replace the one-shot; measuring only the five deciding rows; being seen next). KCD2 being seen: ibyJamin Parts 4, 5, 3 scanned whole (about 5.6 h of footage): one uncut sample (Part 4 at 2,572 s: hare red about 1 s, challenge within 1 s, clear about 16 s after; kcd2-being-seen-part4-2026-11-25.md, evidence on F: game-inputs/footage/wMk2tFAd26E). Pushed. Allowance 90% at 18:23: the weekly stop taken (stop file, last row 18:26 with every measuring row's state, page item weekly-stop-2026-11-25: switch the hourly task off until Monday 13:00).
- 15:52 run: advisors 393, 394; chases on foot L.A. Noire and Sleeping Dogs 5 of 5 each.

## In flight
- Nothing running; the browser pane holds Part 3 (QwbRkSwrQAk), viewport back to desktop.

## Next, in order (from Mon 30 Nov 13:00, after the reset)
0. Read his page (the weekly-stop item: close it once the task is on again), the advisor channel, and Monday's order (advisor 395: Mon 07:00 the full build plan and foundation pass by a cloud job if 4% or more was left; the PC's part comes with the new order). The stop file lapses by itself at 13:00 (nightly_walk.py); delete it then.
1. **Measuring, only the five deciding rows (advisor 395):** being seen first. KCD2 needs four more uncut samples: short single-incident clips from other players (search YouTube inside the pane, ytInitialData videoRenderer: "kingdom come deliverance 2 caught stealing", "caught lockpicking", "trespassing guard"), each read uncut by eye around the incident at 1 s with the hare box scan (scanHareP in the note's method: frame_sheet.js scanHare plus the parchment share; set the viewport to 1280x720 first, a hidden pane reports zero width; screenshots twice). Then crowd reactions from the same clips (who turns, how far, how long until they settle).
2. Chases on foot: Sleeping Dogs edges at 1 s for samples 1-4 and the loss rule (search 'Sleeping Dogs mission failed lost'); then GTA V by a shape method (wanted on foot in free roam, a cop's first run to lost or caught).
3. On foot: step length (a side-on stretch, heel gap over height); the second game's walk from RDR2 or Sleeping Dogs footage.
4. Crowd counts stay a lead. Photo counts (advisor 370) and the 1990 sources (headlamp reach, BS 5489-3:1989, our car braking) are leads for the loops now.
5. If he types "RDR2 drill starting": `python tools/drills/rdr2_record.py start` in the background; "RDR2 drill done": the same with stop (advisor 361). n23-4 voice trial waits for the loops (advisor 381). Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). History rewrite HELD for his word. Progress page daily (progress.json only).

## Footage tools
All in tools/drills/frame_sheet.js (sheet, SAVED EVIDENCE to F:/LedgerTools/game-inputs/footage/<id>/, RED SCAN for RDR2, HARE BOX SCAN for KCD2), each with its known faults. Stamp every time from Get-Date. Storyboard sprites for colour cues only; leg crops every 0.1 s read cadence.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 25 Nov 17:25-18:22: one PC thief playthrough (ibyJamin Parts 3-5, about 5.6 h) gave one being-seen sample: its time goes to quests, fights and travel. Red or orange runs are mostly fights (enemy marks on the compass) and lamp or fire light; look at each. A 1 s alarm can fall between 4 s steps: use 2 s. Part 3 streamed at about 1 frame a second (Parts 4-5 at 3-5).
- 25 Nov 11:33: GamesMediaLA uploads carry advert pods every two or three seeks (five in 12 min); set aside for Santosx07's. 10:57: the motion scan stalls when the player drops its source hidden; fixed with the player's own seek and play calls.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$7.11 this month (production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

