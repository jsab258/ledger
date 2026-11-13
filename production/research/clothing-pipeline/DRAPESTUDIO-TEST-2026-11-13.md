# Drape Studio re-test, 13 November 2026 (advisor 129, his ask 08:27)

Method researched: production/research/clothing-pipeline/DRAPESTUDIO-TEST-2026-11-11.md and -10.md (10 and 11 Nov), the same jobs, body and checks; checked.

## Verdict: nothing to re-test yet. His tool has not changed since the 11 November test; the jumper run today is byte-identical to that day's. Every number, fault and improvement in DRAPESTUDIO-TEST-2026-11-11.md stands as it is.

## Setup
- His folder, C:/Game Dev Tools/DrapeStudio (the earlier C:/DrapeStudio path no longer exists): newest file 11 Nov 10:14 (a build-progress note); the program (release build) dated 11 Nov 09:47, the one tested on 11 Nov from 11:24 on; its notes (AUTOMATION.md 11 Nov 09:47, MECHANICS.md 10 Nov 21:59) unchanged. No change claimed since 11 Nov 15:41, so no claimed change to test.
- One run to prove it: Tom's jumper job (job_run1.py, only the output folder changed), same body, DRAPE_STUDIO_EXE unset. Work folder F:/LedgerTools/drapestudio-test-2026-11-13.

## Numbers
| | 11 Nov run 1 | 11 Nov run 1b | 13 Nov |
|---|---|---|---|
| time | 246 s | 241 s | 239 s |
| its own check | ok, 326 edges over, worst 6.06 | same | ok, 326 edges over, worst 6.06 |
| drape file | | byte-identical to run 1 | byte-identical to run 1 |

## Not run, and why
The jacket, jeans, layering (68 min) and the pattern import were not run again: the same program on the same inputs gives the same files (proved twice on 11 Nov and again today), so a re-run would only repeat the 11 Nov numbers. The listed faults stand by name: cuffs bunching while its check says ok; time 2.0x (jumper), 5.8x (jacket), 2.6x (jeans) against Marvelous; the jacket's upper sleeves letting the arm through; the jeans' waistband high and flaring; FreeSewing's marks imported as pieces, names lost; layering fails (jumper through the jacket).

## For the renewal decision (about 20 Nov)
As of today Drape Studio passes the jumper only (cuffs aside), not the jacket's sleeves, the jeans' waistband or layering: by the advisor's rule (all three garments plus layering), keep Marvelous. A full round runs the day his folder changes.

Cost: about 15 minutes of session time, one 4-minute run; no API spend.
