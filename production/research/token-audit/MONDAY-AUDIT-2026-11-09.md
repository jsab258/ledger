# Monday's audit figures, week 2 to 8 November 2026 (n09-11)

Read 9 November 2026. Counts and quotes only. Dollars are API-price measures, not a bill. Last week = 26 October to 1/2 November (AUDIT-2026-10-26_to_2026-11-02.md).

## 1. Process share (line: 15%)

| Measure | This week | Last week | Source |
|---|---|---|---|
| "records and reports" (session steps touching DECISIONS, FOR-JAFAR, RECIPE, NOW, FINDINGS, RULINGS, CLAUDE, MEMORY, orders, progress page, approvals, time log) | US$182.86 of 1370.21 = 13% (1,702 of 16,431 steps) | US$167.74 of 2222.29 = 8% (1,182 of 21,633 steps) | `python tools/token_audit.py --since 2026-11-02 --until 2026-11-09`, table "By kind of work" |
| Reviews of records, handover, rules written by helpers | not measured | not measured | Helpers are classed by their own description (reviewing/research/building), not by what they review; no field marks a review as "of records" |
| Records inside "building" steps (e.g. page items, handover edits done by a helper) | not measured | not measured | Same: the kind is set by tools used |

The 13% is a floor for the stated scope only; against the 15% line it is the audit's own figure, with the two unmeasured parts left out.

## 2. Tries per fix

Source: HANDOVER.md "Tries used" (cumulative list, not date-limited to 2 to 8 Nov) and thrown-tries.jsonl. Faults the list marks "passed" (closed): 16.

| Closed fault | Tries |
|---|---|
| Darren's fit on S6 | 3 |
| Ron's collar | 2 |
| PCG count's start | 2 |
| 9b | 2 |
| jumpers' knit | 2 |
| n09-14's batch | 2 |
| iron cover; office camera; Martha's trousers; people apart; tester's morning; Mickey's window; Darren's neckband; stuck-legs line; launch line; memory peak reader (10 faults) | 1 each |

Total 23 tries over 16 closed faults: **mean 1.44**. Last week: not measured (that week's audit and reading carry no per-fault tries count). Listed as spent or set aside, not closed: tester's round 3, dish 2, witnesses' sightlines 2, hill 3, speech 3, Tom's crown 4, collar 4. Open at 1 of 2 or 2 of 2 without a "passed" mark are not counted.

## 3. Repeats made from a skill

| Measure | This week | Last week | Source |
|---|---|---|---|
| Skills existing | 9 (six made 2 Nov; shopfront, slate-roofs added 8 Nov; his-page, gate etc. among the six) | 0 | `.claude/skills`, DECISIONS 2 Nov 17:00, 8 Nov 14:54 |
| DECISIONS entries 2 to 8 Nov that name a skill as the method used for a piece | 4: 2 Nov 22:43 (street-weathering method, five surface bands); 7 Nov 17:40, 18:45, 21:28 (Darren and jumpers, "by way of the garment skill's refit section") | 0 | DECISIONS.md |
| Commits that change a skill (not a repeat) | about 10 (gate, packaged-walk, weathering, his-page, speech-bench, asset-import, shopfront, slate-roofs, game-garment) | 0 | `git log --since=2026-11-02` |
| Pieces made by a skill, as a count | not measured: no commit or DECISIONS field says "made from skill X"; shopfront and slate-roofs were written from the work already done, so none of their pieces came after them | | |

## 4. Spend per day (API-price measure)

| Day | US$ | Steps | History share | Opus share | Reviewing share |
|---|---|---|---|---|---|
| Mon 2 Nov | 413.79 | 4,278 | 45% | 98% | 22% |
| Tue 3 Nov | 351.80 | 3,538 | 53% | 98% | 27% |
| Wed 4 Nov | 114.87 | 1,636 | 35% | 96% | 8% |
| Thu 5 Nov | 68.89 | 812 | 21% | 98% | 10% |
| Fri 6 Nov | 84.01 | 1,093 | 24% | 87% | 14% |
| Sat 7 Nov | 94.16 | 990 | 26% | 96% | 3% |
| Sun 8 Nov | 242.67 | 4,084 | 30% | 95% | 12% |
| **Week** | **1,370.21** (days sum 1,370.19) | 16,431 | 40% | | |

Last week: US$2,222.29, 21,633 steps, history 53%. Source: `python tools/token_audit.py --shares 2026-11-0N` for each day; full week in the audit's `AUDIT-2026-11-02_to_2026-11-08.md` (written to the session scratch folder, not the repository).

Other week figures from the same audit: building 41%, reviewing (helpers) 18%, building (helpers) 14%, research (helpers) 5%, research 4%, replies 3%, helpers' briefing 1%; steps in no time-log task 33% (15% after gap-filling).
