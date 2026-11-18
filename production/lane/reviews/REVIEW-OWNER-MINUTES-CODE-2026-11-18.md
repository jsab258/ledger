# Review: owner minutes code (18 November 2026)

Fresh reviewer, 18 November 2026, of tools/lane/owner_minutes.py and tools/lane/test_owner_minutes.py against production/lane/OWNER-MINUTES-MEASURE-2026-11-18.md (Function spec) and its review. Verdict: PASS WITH FIXES.

## Checked and confirmed

- All six spec cases have tests and pass: 200-word item answered (1.0 + 0.17, shown rounded as 1.2), 10-step ACTION (+10 minutes), answer with no item (tap counted, listed), no finished units ("none finished"), three batches on one day with two done, week edges [Monday 00:00, next Monday 00:00) in Swiss time.
- Item "added" is read as Swiss local; answer "at" ending in Z is converted to Swiss time, summer time from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October (checked at both edges).
- An item added Sunday night and answered Monday: reading falls in the first week, the tap in the second, and the tap is not wrongly listed as unmatched. No ids repeat across items.json and archive.json today (102 items); repeats would keep the items.json copy.
- Last week from the records: 49 items, 46 answers, about 48 asked minutes (items 38, taps 8, pictures 2). Items read 38, not the design's 36, because option labels are counted too, as the design's field list implies.
- Tests: 15 pass (11 before, 4 added).

## Findings

1. Fixed. A "steps" or "pictures" given as text was counted by its letters (a 20-letter step line became 20 steps). Now a list counts entries, text counts non-empty lines, anything else 0.
2. Fixed. An "at" with an offset such as +01:00 was treated as UTC, and one with a minus offset as Swiss time. Offsets are now converted properly.
3. Fixed. read_answers could count one answer twice if the same id had a timed file in two folders, and crashed on a file holding a list. Now one tap per id (earliest), non-dict files skipped; non-dict items skipped too.
4. Open. Stored answers stop at 15 Nov 21:09 Swiss time (verdicts folder, 84 files; the items folder holds 43 item copies with no time). At least 8 items closed 16 to 17 Nov have no stored answer, three of them real picks (marvelous-bridge, storage-remove-list, presentmon-licence). The week of 16 Nov shows taps 0. The main session must export the page database's verdicts from 16 Nov onward into that folder before Monday's audit runs, and check the mirroring step that stopped.
5. Open. Withdrawn ACTION items are counted in full: two withdrawn on 17 Nov add about 20 of the week's 32 hands minutes. The main session should decide whether withdrawn-before-done items count reading only.
6. Open (from the design review). Hands before 17 Nov are untagged, not zero; the line does not say so yet.
7. Open. Reports and advisor rows are not read by main(); they stay "n.m." until the caller passes them from the database.
8. Open, minor. main() crashes if --finished or --target has no number after it.

## For the main session

Merge the code as fixed. Mirror the answers from 16 Nov first, then run the audit line; decide finding 5 before the target goes on his page.
