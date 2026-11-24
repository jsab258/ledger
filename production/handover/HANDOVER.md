# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 21:36 (the hourly run)

**Row due:** 22:46 (last row 21:46; page read 21:52; filter verdicts after 2026-11-24T20:52 UTC, advisor after 2026-11-24T21:35:00+01:00; last ack 365 at 21:50).
**Uncommitted:** this file only; work pushed.
**Stopped:** 2026-11-24 22:00 (the 21:36 run: advisors 364-365 done; n23-3 cost closed; history near its point, no room for a scan)

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
- 21:36 run: **advisor 364** RULINGS cleaned whole (4,900 to 4,869; record production/records/rulings-cleanup-2026-11-24.md; the 4,000 aim not reached); page item closed. Three questions to him in ack 364 (Kiln vs 'stopped: procedural tailoring'; friends' evenings 1 Nov vs 21 Nov; talk C# helper vs 19 Nov port): **watch the advisor channel for his answers and apply them** (each answer replaces its line; record in the cleanup file). **Advisor 365**: the people's brain level an open question in RULINGS (back at 4,900 exactly); the cloud lane's brain job runs it, not ours. **n23-3 Q4 closed** without code: talk-runs.jsonl holds tokens per model; per-model dollars add up; prices re-read (PRICES-2026-11-24.md), rate card unchanged.
- 19:37 run: advisors 361-363 (RDR2 drill recorder: tools/drills/rdr2_record.py, his card in advisor 361; Frank fully written; a temper each); **RDR2 being seen SOLID** (median ~70.5 s, five samples; review d); KCD2 being seen shortfall (story walkthroughs hold no witnessed crime); foot-chase-candidates-2026-11-24.md. Detail in TRIED-ARCHIVE.md, 24 Nov 22:00.

## In flight
- Nothing running.

## Next, in order
00. Pace: 75% at 21:37; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set "**Next due:** 2026-11-30 13:00", one page item (switch off the scheduled task ledger-daily-fresh-session, Code tab, Scheduled; on after Monday 13:00), stop all work. Full pace until then (advisor 359).
0. If he types "RDR2 drill starting": run `python tools/drills/rdr2_record.py start` in the background at once; on "RDR2 drill done": `python tools/drills/rdr2_record.py stop`; then read the frames by his card (advisor 361) and fold usable trials into being seen, crowd reactions and chases on foot.
1. **Chases on foot (deciding):** GTA V first: a whole-session scan of the wanted stars (top right; calibrate on one known spell first, as the hare scan was) over the PS4 walkthrough asdZoAycD1o (71,588 s, uploaded 11 Oct 2026, likely cut between missions: about 1.2 h to scan at 4 s, so start it at a run's beginning) and any uncut console free-roam session; on-foot spells only. Sleeping Dogs: "Meet the New Boss" ends in a run from police to a limo; Santosx07's ~13-min parts name no mission: frame-sheet parts ~20-28 (ids in sleeping-dogs-foot-chase-clips-2026-11-24.md). L.A. Noire chases end in tackles: a lead for chase length only.
2. KCD2 being seen: find in the browser pane BlackTorito TV's trophy-run parts for crime trophies, the ibyJamin thief series, pmWPl64nqhg; scan whole; skip menu frames.
3. On-foot cadence leads; crowd reactions Q3 leads on two games.
4. n23-3: Q2 second half and Q3 (voice under the game's load; player's line to first word inside the packaged game) need a free machine with him away, outside the night jobs; then a fresh reviewer on the results. The probes' "I'm Tom": waiting list.
5. n23-4 voice scan; n23-7 (DAILY-2026-11-25 by 19:00 with the advisor's restored rows; credit row). Advisor 320 (backup's 28 GB on C:): two tries used; research before a third.
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only; publish the LIVE index.html read back).

## Footage tools
All in tools/drills/frame_sheet.js (each with its known faults): sheet, SAVED EVIDENCE (pane screenshots copied to F:/LedgerTools/game-inputs/footage/<id>/ with index.json and upload date), RED SCAN (RDR2 flag), HARE BOX SCAN (KCD2). Stamp every time from Get-Date: guesses ran 10-25 min ahead today too. NEW: YouTube's storyboard sprites (in-page fetch of /watch?v=ID, "playerStoryboardSpecRenderer"; L1 80x45, one frame per 5 s; URL storyboard3_L<n>/M<k>.jpg?sqp=...&sigh=<that level's rs$ token>) show a whole video in a few images: too small to tell missions; use for colour cues before seeking.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 24 Nov 21:55: a Sonnet reader by web fetch cannot read YouTube (watch pages return the footer only; channel pages go to a consent page): KCD2's BlackTorito TV and ibyJamin parts not found (kcd2-crime-clips-2026-11-24.md; one candidate pmWPl64nqhg, xGarbett, "caught pickpocketing"). Find clips in the built-in browser pane yourself, as the 19:37 run did.
- 24 Nov 20:50: KCD2 story walkthroughs (two PS5 sessions, ~5 h) hold no witnessed crime; orange hits in the hare box are menu tabs. Search trophy-run parts named for crime trophies instead.
- 24 Nov 20:05: the 360p red scan caught a flashing RDR2 wanted spell on one row only (the word mostly white or pink); look at every short hit, or count bright pixels in the word's own box.
- 24 Nov 19:55: a hidden browser pane unloads the YouTube video mid-scan (duration null) and long waits close the call: re-query the video each step, a 5 s watchdog (movie_player.seekTo, playVideo), polls under 35 s; a quality change mid-scan changes the frame size (compute the box each step).
- 24 Nov 19:55: two scans in one page fight over the video; reload the page before starting another.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$5.41 this month (production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

