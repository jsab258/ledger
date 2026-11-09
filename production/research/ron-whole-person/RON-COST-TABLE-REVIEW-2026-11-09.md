# Review of Ron's cost table draft (n09-5, 9 November 2026)

Fresh first review of RON-COST-TABLE-DRAFT-2026-11-09.md against RON-PRE-OCTOBER-2026-11-08.md, production/time-log.jsonl (618 lines; first line 5 Oct), production/api-spend.jsonl (21 lines), `git log`/`git show`, and production/research/token-audit/ (plus unit-costs/RON-MEASURES-2026-11-08.md, which the draft's dollars really come from). Read only; nothing run but git reads and short Python sums.

## Verdict: pass with fixes

Most hours reproduce. The faults are one wrong time-log figure, one mislabelled line, a count that mixes whole shared windows into "Ron-named" totals, dollars that the token-audit files cannot bear out, a bounding method that is not an upper bound as labelled, and missing rows.

## Numbers checked

Match their source:
- TL 32-33 = 1.99 h; TL 58-59 = 0.82; TL 337-338 = 0.81; TL 339-340 = 0.39; TL 494-495 = 0.12; TL 547-548 = 1.77; 549-550 = 0.47; 551-552 = 1.49; 555-556 = 0.63; 557-558 = 0.30; knit 579-586 = 0.35. TL 553 = 1.15 h only as start to the next start (22:41:13): the line has no stop of its own.
- API: 21 lines, none names Ron; backstory 0.6419 + 0.5067 = 1.1486 (1.15) for 35 calls each run.
- Git (committer dates): face 3.5 (7 sittings), facts 2.7 (5), card 3.5 (7), routine 6.4 (8, 15 commits), voice 3.2 (6), jacket 5.4 (8), commit lists and first/last hashes all exist. Draft's sums: 2.08, 7.21, 26.7 all add correctly.

Not borne out:
- TL 567-568 is 06:50-07:25 = 0.58 h, not 0.25. The 0.25 is the token-audit window (06:50-07:05) in RON-MEASURES. The 1.46 total for routine spots (0.82 + 0.39 + 0.25) should read 1.79 on the log, and "6.71 for TL 567-568" is for 15 minutes of a 35-minute window.
- "TL 40 sitting 0.75" is wrong. TL 40-41 (21:50-23:32) is 1.70 h; the 0.75 h is TL 38-39 ("sitting clips", 21:05-21:50). The draft calls it unresolved; the log resolves it. TL 40's task also names wear and front decals, TL 38 overlaps the Talk task (TL 36-37), so neither is Ron-only.
- PRE row "voice acting tests, 3 sittings, 1.5": commits 9d01a83ea (20:41) and d4f64668d (21:22) on 29 Sep are 41 minutes apart, so 2 sittings, 1.19 h (0.31 h less). That makes voice 4.7 into 4.4 and the 26.7 total into 26.4.
- Dollars 58.86 (moustache), 30.59, 25.62, 40.25 (as a six-window sum), 6.71: none is in the token-audit files except as bare numbers 40.25, 6.29, 6.71, 4.15 in the 26 Oct-2 Nov audits, which cannot cover 7-8 Nov windows. 58.86, 30.59 and 25.62 appear only in RON-MEASURES. The draft's claim of "token-audit API-price equivalents" is not checkable from the token-audit folder; cite RON-MEASURES instead and mark them unverified here.
- "Ron-named helpers 1.58 = 0.32 + 0.56 + 0.70": the 0.32 is a helper naming Ron and Darren (RON-MEASURES line 31). Also the same 0.56 + 0.70 sit in the Collar row, so they are listed twice in the table (the totals count them once).

## Counting faults

- "Recorded hours, Ron-named windows 7.21 h" adds whole windows of which Ron is one clause: TL 32 (also CC0 route, 1.1's faults, glass), TL 40, TL 58 (doorway probe, office rebuild), TL 339 (Sheila's hand, study C), TL 337 (five clauses, 58.86 dollars incl. research helpers), TL 553 and 555-556 (Darren's third try; Darren passed review). It reads as Ron's cost; it is a ceiling of windows touching Ron. Say so in the Totals line, or give no sum.
- TL 553-558 hours are moved from Jumper to Collar and counted once; the Jumper row still prints them. Fine, but the Jumper row's "Ron's share 1.98-2.23" and the RECIPE 1.15 are alongside them with no rule for which counts.
- TL 554 and TL 555 start one second apart (22:41:13 and 22:41:14) and TL 553 has no stop: windows overlap, so "task-hours" cannot be summed to a person's time. The draft says so once; the Totals do not follow it.

## Parts of the person: missing or thin

Present: body, face, hair, moustache, jumper and jeans, hem, boots, donkey jacket, collar, voice, street lines, card, facts, routine, sitting, office exit, reviews, backstory, API.
Missing or wrong:
- Jeans/trousers are folded into Jumper; no row of their own.
- Boots: row holds only "not recorded; Tom's refit". Whether Ron has boots, and the 1 Oct Darren-boots swap, are not said.
- Pre-October clothes and body work other than the donkey jacket: 1-4 Oct commits naming Ron (6d604f51c "Ron's chest no longer a hole" 3 Oct; 719751abd Marvelous jacket on Ron's body 2 Oct; 05c47cda0 "Ron's arms let down"; lab test 3 "Ron's pattern") are outside every PRE row, so Body and Clothes show "not recorded" while git has candidates.
- Helpers' hours as a column (the standing rule: helpers' time against their item); only dollars appear.
- Jafar's own minutes (taps, looks) are named "not recorded" in places but have no row.
- Packaged-build walks and the tester's pass for Ron (the gate that makes a piece pass) have no row.
- Office exit: the n09-1 order log, named as unread. Sitting: the 8 Nov failed sit proof has no hours.
- Voice after 1 Oct (recording, the 4 Oct and later voice work) and talk-line tone are absent.
- No grand total hours-plus-dollars line stating what one complete person cost, which was the table's purpose.

## Is the pre-log bounding method sound?

Partly. Sitting spans from `git log` with a 90-minute break are reproducible (six of seven rows matched exactly), and the rows say they are not additive. But:
- It is not an upper bound as labelled "bounded, upper": the 0.5 h floor for one-commit sittings is invented, and work before a sitting's first commit or between commits that does not commit is invisible, so it can be low as well as high. It is an indicator, not a bound.
- Path filters are not a person filter: STREET-LINES (1 commit) and routine (whole 41-person file) cannot be separated; commits cbe276499 and 5d80bbe8a appear in three rows (card, facts, street lines), so the 26.7 counts one sitting up to three times.
- Voice's span starts 31 Jul with CI/machine commits, yet 3.2 h is taken as Ron's.
- Row coverage stops at the paths chosen; see the missing 1-4 Oct work above. The cut at 5 Oct matches the log's first line, which is right.
- Fix is cheap: report each commit once across rows (a set union of sittings), and give a low-high pair per part.

## Fixes

1. Change TL 567-568 to 0.58 h (log) and say the 0.25 h and 6.71 dollars belong to the audit window 06:50-07:05; recompute routine spots 1.46 to 1.79 and the 7.21 total to 7.54.
2. Replace the "TL 40 sitting 0.75" with the true lines: TL 38-39 = 0.75 h (sitting clips), TL 40-41 = 1.70 h; state that neither is Ron-only; resolve the "unresolved" note.
3. Correct PRE: voice acting tests 2 sittings, 1.19 h, not 3 and 1.5; voice 4.4, bounded total 26.4.
4. Source dollars to RON-MEASURES-2026-11-08.md, not the token-audit folder; mark 58.86, 30.59, 25.62 unverified here. State in INP-derived rows that the 2 Nov token audits end at 2 Nov.
5. Do not print the 0.32 (Ron and Darren) as "Ron-named"; list 0.56 + 0.70 once; keep 0.62 page check out.
6. Rename the recorded total "windows touching Ron (a ceiling, not Ron's time)" or drop the sum; add the share of clauses per window where the task text allows.
7. Relabel pre-log hours "indicative span, floor 0.5 h", not "upper"; count shared commits once (union of sittings) and give a low-high pair per part.
8. Add rows or explicit "none" lines for: jeans, 1-4 Oct Ron clothes/body commits, helpers' hours, Jafar's minutes, tester/packaged walks, post-1 Oct voice.
9. Read the n09-1 order log for the office exit, or state the part as unread and unmeasured in the totals.
10. Add a closing line: what is known (hours range, dollars range) and what is not, for one complete person.
