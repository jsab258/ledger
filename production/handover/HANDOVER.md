# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 19:37 (the hourly run)

**Row due:** 21:55 (last row 20:55; page read 20:47; filter verdicts after 2026-11-24T19:47 UTC, advisor after 2026-11-24T20:15:00+01:00; last ack 363 at 20:16).
**Uncommitted:** nothing after this commit; pushed to wip.
**Stopped:** 2026-11-24 19:05 (the 17:51 run: advisors 358-360 done; RDR2 being seen set aside at four clean samples on the third review; history past its point)

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
- 19:37 run: **advisors 361-363**: 361 a recorder for his RDR2 drill (tools/drills/rdr2_record.py: `start` when he types "RDR2 drill starting", `stop` on "RDR2 drill done"; only the open game window, never the game's start, keys or files; frames to F:/LedgerTools/game-inputs/footage/rdr2-drill-<stamp>/; then read per block as his card in advisor 361 says). 362 Frank fully written in the key scenes (RULINGS story line). 363 a temper for every named person; his story yes after the next story pass (RULINGS; the dials check on Monday's people-data follow-up). Efficiency review (advisor, 19:44) acknowledged: scan first, Sonnet readers find clips; DAILY 25 Nov must restore the measuring-hours line, solid numbers, dollars per solid number, the Opus share and the skipped rows.
- **RDR2 being seen SOLID** (review-being-seen-rdr2-2026-11-24-d.md): 41.5, 70.5, 70.5, 84, 97 s, median ~70.5 s; the 84 s from 2FIC Gaming's 6 Nov 2018 stream ZkTHGLvWCYM (cart theft); a 47 s ride-then-wait spell kept out. Solid count four. RECIPE entry written.
- His page: one open DECISION, rulings-room-2026-11-24 (A recommended: enforced rulings move word for word to a second file; B cap 6,000; C keep squeezing). RULINGS stands at exactly 4,900.
- **KCD2 being seen: shortfall** after ~1 h: HARE BOX SCAN (frame_sheet.js) calibrated on vyA2Nm1BHyw; A56UfjfcsYc (4 h PS5) and N1uLUFEjydo (trophy run Pt 3) scanned whole: menus, tutorials, fights; no witnessed crime.
- Chases on foot: foot-chase-candidates-2026-11-24.md (15 unverified rows; mission lists).

## In flight
- Nothing running. The browser pane's tab holds a stopped scan only.

## Next, in order
00. Pace: 74% at 20:22; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set "**Next due:** 2026-11-30 13:00", one page item (switch off the scheduled task ledger-daily-fresh-session, Code tab, Scheduled; on after Monday 13:00), stop all work. Full pace until then (advisor 359).
0. If he types "RDR2 drill starting": run `python tools/drills/rdr2_record.py start` in the background at once; on "RDR2 drill done": `python tools/drills/rdr2_record.py stop`; then read the frames by his card (advisor 361) and fold usable trials into being seen, crowd reactions and chases on foot.
1. **Chases on foot (deciding):** GTA V first: a whole-session scan of the wanted stars (top right; calibrate on one known spell first, as the hare scan was) over the PS4 walkthrough asdZoAycD1o and any uncut console free-roam session; on-foot spells only (frames at 2 s). Sleeping Dogs: Santosx07 PS4 parts holding "Meet the New Boss" (police escape on foot). L.A. Noire chases end in tackles: a lead for chase length only.
2. KCD2 being seen: later parts of BlackTorito TV's PS5 trophy run (pickpocket, lockpick, thief trophies: find the part by title or chapters), then the thief-titled ibyJamin series; scan whole; filter menu frames (skip when the top band holds the menu tab row).
3. On-foot cadence leads; crowd reactions Q3 leads on two games.
4. n23-3: per-model tally in ClaimBench before the per-model rows; prices re-read with dates. The probes' "I'm Tom": waiting list.
5. n23-4 voice scan; n23-7 (DAILY-2026-11-25 by 19:00 with the advisor's restored rows; credit row). Advisor 320 (backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only; publish the LIVE index.html read back).

## Footage tools
All in tools/drills/frame_sheet.js (each with its known faults): sheet, SAVED EVIDENCE (pane screenshots copied to F:/LedgerTools/game-inputs/footage/<id>/ with index.json and upload date), RED SCAN (RDR2 flag), HARE BOX SCAN (KCD2). Stamp every time from Get-Date: guesses ran 10-25 min ahead today too.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 20:50: KCD2 story walkthroughs (two PS5 sessions, ~5 h) hold no witnessed crime; orange hits in the hare box are menu tabs. Search trophy-run parts named for crime trophies instead.
- 24 Nov 20:05: the 360p red scan caught a flashing RDR2 wanted spell on one row only (the word mostly white or pink); look at every short hit, or count bright pixels in the word's own box.
- 24 Nov 19:55: a hidden browser pane unloads the YouTube video mid-scan (duration null) and long waits close the call: re-query the video each step, a 5 s watchdog (movie_player.seekTo, playVideo), polls under 35 s; a quality change mid-scan changes the frame size (compute the box each step).
- 24 Nov 19:55: two scans in one page fight over the video; reload the page before starting another.
- 24 Nov 19:00: a sample kept despite a solid red stage while another was dropped for one; review c caught it. Write the inclusion rule first.
- 24 Nov 18:55: the KCD2 hare colour scan counts menu icons and adverts as alerts; needs a menu filter.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$5.41 this month (8, 16, 23 Nov US$0.95, 24 Nov US$0.69; production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

