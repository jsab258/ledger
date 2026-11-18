# Review: K2 sim-port faults, lane share proposal, prototype system checks (18 Nov 2026)

Fresh reviewer, reading only, about 10 minutes. No builds or browser runs.

## A. production/lane/K2-SIM-PORT-FAULTS-2026-11-18.md

Verdict: PASS WITH FIXES

Checked against the code:
- Slip 2: PoliceFile.cs 261 sets `e.Day = day` on a raise (the file says 262, one line off), and VisitCouldBe (491 to 498) tests `e.Day <= day`. Confirmed.
- Slips 1a/1b: EllisComes (335 to 341) takes no `now` and records the visit at once; Fresh (348) refuses any reason already visited; FromJson (545 to 554) drops repeat reasons. ConstableComes (101 to 113) does guard InTheCells. TownWeek.NineEllis (120 to 131) never calls TakeIn. Confirmed.
- Slip 3: SpellCouldBe (504 to 515) uses the latest call or visit day plus 22 hours. Custody.TakenAt exists (Custody.cs 40, 81). Confirmed.
- FINDINGS.md lines 9 and 18 are the suspicion and police faults. Confirmed.
- "None shows today" for the police fault is backed: the only Report call in the port is TownWeek.h 135 to 136 with Offence::Damage, and Detective() needs Wounding or worse (PoliceFile.cs 181). The file does not cite this, though.
- Hour estimates: 10 to 13 h for the police fix and 2.5 to 3 h cloud for suspicion look reasonable for the scope described.

Fixes:
1. Plain-words point 2 says "Neither shows in the game today", then the suspicion section says a person can greet him coldly and talk warmly; say the suspicion mismatch can show today, small.
2. Back the police "does not show" claim with its evidence: the port only ever reports Offence::Damage (TownWeek.h 135 to 136), and Detective() starts at Wounding.
3. Slip 2's line is PoliceFile.cs 261, not 262.
4. Plan B's wiring step: say whether the game's Ellis and Taken handlers in CrimeProbe.cpp (around 7793 to 7802) need changing when NineEllis starts taking him in; if so, that is PC work the cost line leaves out.

## B. production/lane/LANE-SHARE-PROPOSAL-2026-11-18.md

Verdict: PASS WITH FIXES

Checked: 16 log lines, 17 Nov 17:28 to 18 Nov 00:31; summed run time 268 min (4.5 h) holds, but it sums two runs that overlapped at 20:17. Tests: 16 + 15 + 21 + 57 + 26 + 12 = 147 holds (the prototype's 6 not counted). One FAIL review (LIGHT-WEATHER-VALUES) holds. "205 / 1.7 = about 120 hours" matches the order of 16 Nov, line 5.

Fixes:
1. Items done is overstated: the queue shows 29 done (A to G, 1 to 12, 14 to 19, B12, G4, G1, 22), not about 31; the kinds (12 + 8 + 7 + 2 + 2 = 31) need recounting to match.
2. "Each with a fresh review" is overstated: the first run (parked cars, item 1) has no review in the log or in reviews/; say so.
3. Say the 4.5 h is summed run time, with two runs in parallel at 20:17.
4. The "about 67 actions" and "about 15 picks" cannot be recounted from the log as written; mark them [est.] or state how they were counted.
5. CLAUDE.md's weekly split is 70% production, 10% independent review, 20% his: say plainly the lane's 10% is not the review 10%, so Decision 2 is not misread.
6. CLAUDE.md records time per task with tools/timelog.py; the proposal measures the share by dollars; say how the two are reconciled or why dollars win.
7. CLAUDE.md itself (not only RULINGS) says one production session and "never unattended lanes"; Decision 1 should name that the rule text changes if he picks A.
8. Decision 3 (what to do when the queue is dry) is not money, canon, story or scope; decide it as a session rule and drop it from his page.

## C. tools/lane/prototype/tests/systems_test.py and README "Per-system checks"

Verdict: PASS WITH FIXES

Checked: LEDGER_MANUAL and LEDGER_NORENDER are read by the published bundle (src/bundle/part-02.js, the frame loop: `window.LEDGER_MANUAL||AT(e)` and `!window.LEDGER_NORENDER`). The tests set them on the page and use only window.LEDGER; nothing edits the bundle. Assertions are concrete (event counts, witness lists, memory sources, exact money fields, save fields, version refusal), page errors fail every test, and the missing-assets case skips rather than passes. The known restore bug is an expectedFailure, which is right.

Fixes:
1. README "Gossip told behind his back adds one": the test plants a told memory by hand (test_2c), it does not run gossip; say so.
2. README fare check: say the cab and passenger are placed at the drop by hand, so only payment at the drop is tested, not the ride.
3. test_1c's last step forces every person's face-knowledge to 0.9; the README says so, but the test name claims the street learns; rename or comment it as a threshold check.
4. test_2a recomputes the counts with the report's own rule (TRUTH_JS), so it catches drift, not a wrong rule; add one hand-counted case with known numbers.
5. setUpClass finds fare places by a regex on minified names (`Fa=` ... `function C2`); note it breaks on any rebuild of the bundle and point stage 1 at replacing it.
6. Tests depend on run order (1a feeds 1c, 2c, 3a); keep that stated at the top (it is) and fail with a clear message if 1a's coat_day event is missing in 2c (now an AttributeError on None).
