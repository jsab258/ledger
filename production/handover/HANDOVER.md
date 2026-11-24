# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-24 23:51 (the hourly run)

**Row due:** 00:58 (last row 23:58; page read 00:26; filter verdicts after 2026-11-24T21:58 UTC, advisor after 2026-11-24T23:45:00+01:00; last acks 371-373 at 23:54-23:55).
**Uncommitted:** nothing; work pushed with this file.
**Stopped:** 2026-11-25 00:28 (the 23:51 run: advisors 371-373 recorded; walk upload speed settled; RDR2 ladder solid; two tries each on photo counts and the GTA V star scan; history at 225k, short of the point but too little room left for a footage item; both helpers finished, nothing running)

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
- 23:51 run: **advisors 371-373** in RULINGS (gossip on rules; Quay Street lamps two at ~34 m; Monday's paper playthrough first; fares at the late-1991 tariff; brain re-run V1-V4 plus hybrid, V5 dropped; only build-shaping gaps before the one-shot) and acked; the keeper reads RULINGS. **GTA V walk:** the upload plays at real time (brightness scan: one game day in ~2,900 s against 2,880 s); Franklin and a townsperson at the same pace both ~2.5 steps/s at 1,652 s (lead; the 3.3 at 360 s likely a mis-read). **RDR2 ladder:** witness to wanted SOLID as a spread 2-106 s, median ~33.5 s (eight uncut, four players; fresh review applied); deed to flag 1-5 s and wanted to lawmen 7-10 s leads. **Braking flag:** our C# traffic stops in 15-22 m at 30 mph (longer than 14 m); the prototype car's distance is emergent, needs a run (cloud lane's). **Photo counts try 2:** four Hull photos, no lamp spacing; method questioned (OS plans draw lamps; NLS behind a human check). **Chases on foot:** GTA V star scan set aside after two tries; Sleeping Dogs Part 2 holds no chase.

## In flight
- Nothing running. Browser pane on Sleeping Dogs Part 2 (viewport desktop).

## Next, in order
00. Pace: 79% at 23:51; **the weekly stop is 90%** (advisor 352): at the newest reading of 90% finish the step, commit, push, one row, write production/weekly-stop.json {"until": "2026-11-30T13:00", "reading": N}, set "**Next due:** 2026-11-30 13:00", one page item (switch off the scheduled task ledger-daily-fresh-session, Code tab, Scheduled; on after Monday 13:00), stop all work. Full pace until then (advisors 359, 366: no pace-line holds).
0. If he types "RDR2 drill starting": `python tools/drills/rdr2_record.py start` in the background; on "RDR2 drill done": the same with stop; read the frames by his card (advisor 361).
1. **On foot, the walk (GTA V, rzz5BOoJ9Rc, real-time upload):** four more stretches at 0.1 s by which sole shows (re-read 360 s beside 1,652 s; then about 1,260, 2,460, 3,060 s) for five samples; the pane's viewport is 1024 wide (canvas sheets 4 cells of 256). Then a fresh small-reviewer. Step length: a side-on stretch, heel gap over height.
3. **Chases on foot:** Sleeping Dogs Santosx07 Parts 1 and 3 (night-market chase; ids in sleeping-dogs-foot-chase-clips), then L.A. Noire's scripted chases; the GTA V star scan only by a shape or template method (third try needs the 7 Nov rule's researched method).
4. **KCD2 being seen with crowd reactions** (one town crime clip serves both): ibyJamin Part 4 (wMk2tFAd26E) or 5 (AK8xLkS1Cfs), hare scan with the parchment filter (drop hits above 12% beige); first check by eye that this player shows the behaviour icon at a known alarm. If none by the week's end, say so in STATUS.
4a. **Photo counts (advisor 370):** two tries used (4 Hull photos, no lamp spacing); the different method: the OS legend first (does 1:2,500 draw lamps?), then NLS plans if reachable without the human check, else period footage of northern side streets by eye. Quay Street stays at 34 m by his ruling. 5. 1990 sources the recheck moved (period-braking-lamps-2026-11-24.md: 30 mph 23 m, 1987 edition unverified; beam reach and BS 5489-3:1989 not reached): crowd counts (period footage, footfall records), headlamp reach (period lighting regulations), car braking against the Highway Code (flag: ours 8-11 m at 30 mph against its 14 m, unchecked).
6. n23-3 Q2-Q3 need a free machine with him away; n23-4 voice scan; n23-7 DAILY-2026-11-25 by 19:00.
0b. Next night walk Mon 30 Nov 01:30 (held while the stop file holds). 4p. Marvelous stays open. No Unreal work until the browser prototype is done (advisor 288). 5p. History rewrite HELD for his word. Progress page daily (progress.json only).

## Footage tools
All in tools/drills/frame_sheet.js (each with its known faults): sheet, SAVED EVIDENCE (pane screenshots copied to F:/LedgerTools/game-inputs/footage/<id>/ with index.json and upload date), RED SCAN (RDR2 flag), HARE BOX SCAN (KCD2). Stamp every time from Get-Date: guesses ran 10-25 min ahead today too. NEW: YouTube's storyboard sprites (in-page fetch of /watch?v=ID, "playerStoryboardSpecRenderer"; L1 80x45, one frame per 5 s; URL storyboard3_L<n>/M<k>.jpg?sqp=...&sigh=<that level's rs$ token>) show a whole video in a few images: too small to tell missions; use for colour cues before seeking.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 25 Nov 00:22: GTA V wanted-star pixel test (two boxes, white counts, blob widths): the ammo count moves into the stars' slot when no stars show; set aside after two tries.
- 25 Nov 00:19: maps.nls.uk answers with a human check (HTTP 405): not passable by the session.
- 25 Nov 00:15: photo counts try 2 (captioned archives): 4 dated photos, all Hull; text readers cannot look at an image they have not fetched.
- 25 Nov 00:15: my record times ran up to 25 min ahead again (corrected): Get-Date before every written time.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: about US$5.41 this month (production/api-spend.jsonl).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

