# Fresh review of Ron's cost table draft (12 November 2026)

Checked: RON-COST-TABLE-DRAFT-2026-11-09.md (the version with the 9 Nov fixes) against production/time-log.jsonl, the docstring of tools/timelog.py (not run), git log, DECISIONS.md.

## Verdict: pass with fixes listed

## (1) Numbers
Recomputed from the log: TL 32-33 1.99, 38-39 0.75, 40-41 1.70, 58-59 0.82, 337-338 0.81, 339-340 0.39, 494-495 0.12, 553 to next start 1.15, 555-556 0.63, 557-558 0.30, 567-568 0.58. All match. Sums 2.08, 1.79, 3.69, 9.24 and 26.4 add correctly. The 0.25 h/6.71 dollar audit-window split is stated honestly. Dollars were not rechecked (source RON-MEASURES; the draft marks three unverified).

## (2) Double counting and sharing
- TL 557-558 (00:22-00:40) overlaps TL 559 (00:24, n02-research-proposals); not noted. TL 554/555 and TL 553's missing stop are noted.
- Collar 2.08 h is mostly Darren's third try (TL 553 names "Darren's third try, Ron's collar points"). It is presented as "Collar" hours; it is a shared window and the ceiling label is the only protection.
- TL 38-39 and TL 40-41 are 7 Oct night windows and sit beside TL 32 the same evening; no overlap found.
- The Jumper row still prints Ron-named 0.63 + 0.30 beside the Collar row: a reader may add both. State "see Collar" in the hours cell.

## (3) Unrecorded parts: what git can bound
- Boots: not unknown. Git shows Ron's boots passed before 30 Oct (b7f3b3ec6, 12:06: "Ron's boots for Tom") and were carried to Sheila 11 Nov (DECISIONS 11-11 12:33). Ron's own boots are therefore real; making span not bounded from the messages read (needs the earlier boots v1-v3 commits).
- Sitting: the draft covers 7 Oct only. Git adds Ron seated in Epic's bench idle (01e14f296, 2 Nov 12:16), sitting review (5b1bd727d, 2 Nov 08:50), and the office exit try 2 (c3ef4ff2b, 11 Nov; 5555707ba, 9 Nov). Each is a commit time only; roughly 3 to 6 further hours of sittings, shared with Tom, Sheila, Rita.
- Office exit: n09-1 commits 825dabf7e (9 Nov 04:04), 5e49a2cc4 (06:27), 5555707ba (07:28), c3ef4ff2b (11 Nov 07:59) bound about 1.5 to 4 h on a 90-minute break rule, all shared with other people. The draft says "order log unread"; the git bound is available.
- Hair: commits 40c27abff and abf5ea449 (7 Nov) are the hair try 2, shared with Darren and Sheila; not Ron-bound.
- Body, hem: DECISIONS search found no Ron-specific lines; stay unrecorded.
- Post-5 Oct wear, collar tries 1-4 (e.g. 55a362413, 2 Nov 12:30 "collar fourth try") are not in the table's hours at all.

## (4) Measured versus estimated
Honest on the whole: recorded, bounded and inferred are labelled, no grand total. Weak points: "about 3 to 8 for about 5 reviews" and "about 0.39 in runs H to K" are inferred figures sitting in a dollars column; mark them "estimate" in the cell. The 26.4 h git figure counts shared commits up to three times and is labelled so, but is still large next to 9.24; keep the "not added" line.

## Fixes
1. Add boots evidence (30 Oct pass) to the Boots row.
2. Add sitting (2 Nov) and collar tries 1-4 to their rows, or say they are outside the table.
3. Replace "order log unread" with the git bound for the office exit.
4. Note the TL 557/559 overlap.
5. Mark inferred cells "estimate".
