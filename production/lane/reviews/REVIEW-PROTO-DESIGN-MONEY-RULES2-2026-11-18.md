# Review: prototype against design, money in dollars, rules round two, rules test (18 Nov 2026)

A fresh reviewer, 18 Nov 2026, branch lane-2026-11. Read in the code and documents only; no web. Nothing committed. Nothing in the Core, game-design/, production/specs/, canon.md, RULINGS.md or the prototype's src/ was edited.

## A. PROTOTYPE-VS-DESIGN-2026-11-18.md: PASS WITH FIXES

Checked rows 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18 on both sides.

- Confirmed in the code: LiveClock.h "two game minutes a real second (the town, 29 September)"; CrimeProbe.cpp ClockTick holds the clock while the talk box is open or a live line is pending; hook-cast.json talk_range_m 6.0 and 81 ties; TownRounds.cs 6 minutes; Gossip.cs HopDecay 0.8, MinConfidenceToShare 0.2, half-life 96 hours, drop under 0.03, Nerve and Loyalty 0.5; PoliceFile.cs WouldReport (nerve 0.4, OnHisSide 0.575), LoudAt 3, TalkNoSoonerThan 3; Custody.cs 6/2, 8, 12, 22 hours; Wallet.cs 120; Debts.cs forgiving +0.15; GameController.cs Wallet 250, Sam 120, Rocco 60; Campaign.cs takings 220.
- Prototype values match the rules read and the bundle (45 s hour, 4.8/8 m, 0.42 and 0.38, x0.8, 0.12 heat floor, 3.2 m at 35 percent, 23.50, 18.00 rent late from Saturday, the ten nostmt names).
- Row 9: the cast file's ids (victor, tibor, drago) map to Wayne, Susan Coverdale and Dennis in the cloud-week town notes, so the C# list is right.
- Rulings cited exist and say what is claimed: 1 Oct (Ron and Sheila never; a neighbour reports unless on his side or talked round), 29 Sep (first week's nine designs stand), 30 Oct (hard opening from nothing). The 17 Nov "one simulation" clause is his decision recorded in DECISIONS.md (17 Nov 22:38), not a RULINGS.md line; the note cites it correctly as DECISIONS. Canon-first ordering is applied correctly (row 12, the five-rung ladder).
- Three owner decisions, each with a recommendation: within the limit. Decision 3 is scope he left open on 29 Sep (town-traits draft, line 6). Decision 1 is borderline: by the note's own method the clock comes from the prototype, and RULINGS 30 Oct says to decide feel details oneself; it is kept for him because it bears on the approved first hour. Left as is.
- Fault: decisions 1A and 2A pull against each other. The "13 of 13 by minute 30" figure behind row 5 was measured at the 30-second hour, and 7 of the 13 landed only at minute 30 itself (first-hour-2026-09-29.md); at 45 seconds it may fail under the one-retelling rule. Fixed: row 5 says so, and one line after the decisions says the measurement must be re-run before both are taken.
- Fault: row 7 said 31 people; the rules read was corrected to 28 named people. Fixed.
- Fault: row 14 said the prototype has only pay-in-full or refuse; the bundle also pays half when a debt demand is met at rung 2 of the fighting ladder (`VS(i,t>=3?1:.5)`). Fixed.
- Fault: the closing note said the "drink" beat is not in the Core; it is also in two CoreTests checks (Program.cs 4642, Program.Part3.cs 1403). Fixed. The finding itself (it breaks the content rule) stands and should still go to FINDINGS.md.
- Row 9's open question (why the customs officer never reports) is answered in the town notes; fixed to say so.

## B. MONEY-IN-DOLLARS-LIST-2026-11-18.md: PASS WITH FIXES

- "Currency is £" is at game-design/roadmap-history.md line 1624, as claimed.
- Twelve rows spot-checked by line: all right (how-to-play 64, 83; empire-roster 41, 51; counterparty-purses 63; balance-economy 95; balance-open 34; roadmap-history 1071; production-plan-audio-art 118; tier2-batch-1.json 2720; setting-britain 79; the-gap 38). Empire-roster 41 and setting-britain 79 paraphrase a table row or a wrapped line, with the right content.
- Counts: the 38 production-plan lines and the 67 real-world lines add up. But a grep of the text files finds 123 money lines, not 118: missed were three table headers holding game money (balance-findings-economy 79 "avg$", balance-findings-open 14 "racket $", combat-spec 243 "$cost") and two lines describing the switch (setting-britain 29 and 77). Seven further hits are "$" as a pattern sign, not money. Fixed: the five rows added and the counts set to 123, 52, 4 and 67, with the correction dated.

## C. Round two of PROTOTYPE-RULES-READ-2026-11-18.md: PASS

- Joined part-01 and part-02 per MANIFEST.json; the joined file's sha256 matches the manifest.
- Twenty search strings checked with a fixed-string count; all found, each once except `sched:[` (30, as stated) and the 90 m check (2, as stated). The lane offset (-0.7 to 0.7, times 0.6 when used) gives the stated -0.42 to 0.42.
- The Ron-stop hypothesis is supported by the code: G2 sets `pauseT=Math.max(pauseT, .9+1.6*sev)` only for a moving witness within 26 m; night_out has severity 0.35 (1.46 s); attention fills at (0.45 + 1.4 clarity) x 1.5 a second and on reaching 1 resets and calls G2 again on the same two-hour event, so the pause is topped up every 0.36 to 1.3 s; k_ returns early while pauseT is above 0 and the person moving. It remains a reading, not a run, as the note says; its proposed confirming test is sound.
- Outside round two, two rows were imprecise and were corrected in place: 1.23 (a walking witness pauses whatever their nerve; only a standing one steps back if timid) and 4.03 (the ladder's half payment).

## D. tools/lane/prototype/tests/rules_test.py: PASS

- Run: 115 passed, 11 skipped (the live layer, no pictures), before and after the fixes.
- Every static row's number was compared with its rules-file row: no contradiction. The live expectations (Monday 15:36, 45 s, 23.50, the five debts, Ron's day, the three trait sets, 28 named, ten nostmt including the constable, save version 4, heat x e^(-300/1700), a 7-hour hold and 40.00 bill for the arrest of a man who struck an officer) all follow the rules file.
- Minor: row 1.23's name repeats the old wording ("timid people step back"); the search string is unaffected.

## Rules held

No em-dashes or italics found in the four files; third person throughout. Alcohol and gambling words appear only where a fault is being reported or the filter's word list is quoted, which is internal, not shown in the game.

## Fixes applied

1. PROTOTYPE-VS-DESIGN: row 5 caveat, the decisions 1 and 2 line, row 7 (28), row 14 (half payment), row 9 (Coverdale), the CoreTests note.
2. MONEY-IN-DOLLARS-LIST: five rows added, counts corrected.
3. PROTOTYPE-RULES-READ: rows 1.23 and 4.03 corrected, each marked as by review.
