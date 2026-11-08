# Review: Ron's end-to-end costing plan and the QA first steps (8 November 2026)

One fresh reviewer, read-only. Sources opened on 8 Nov: time-log.jsonl lines 336-337, 547-586; UNIT-COSTS-2026-11-02.md and its json; HOOK-GARMENT-LIST-2026-11-03.md; RECIPE.md and DECISIONS.md by grep; RULINGS.md; the QA proposal and PROPOSALS-REVIEW-2026-11-08.md; the night files, logs, CSV and tools named.

## Verdicts

- **RON-END-TO-END-PLAN-2026-11-08.md: PASS WITH FIXES** (8 faults). Window hours, the US$22 to 38 rate, 2.95/1.45, 1.61, 2.81, 1.99, 9.8, 29.0, 77.0, the voice R lines (1.2, 0.6, 0.3), 2 h hair, 2 h knit, 20 minutes, 3 h walk-off and US$0.12 all match. Nothing contradicts RULINGS (2027 line, API credit, efficiency).
- **QA-FIRST-STEPS-2026-11-08.md: PASS WITH FIXES** (6 faults). Confirmed: 14 consecutive legs toward (7.9, 4.6), D0 09:50 to 12:05, 2.11 m short, next "to" (8.47, 3.29), talk-open 12:19; 23 nights carry a path (25 folders, two empty); both logs' line 333 as quoted; walk.log has no command line; the 3b3454e CSV peaks at 6,126.5 MB, so OVER-LINE holds; route_walk.py lines 179, 242, 282, 389; slice-perf.py 26, 76 and 8 self-tests; perf-hook.py 113; workflow 50-57, 2111-2113.

## Faults: Ron plan

1. Lines 32, 33, 98: the plan quotes SHEET.md line 13 as "grey jumper; dark grey work trousers". The sheet was changed at 14:46 (the plan is 14:38, change not committed) and now reads navy jumper and jeans, "as Jafar passed them". Fix: mark the sheet question settled and remove it from "For the session".
2. Line 58: "Logged work kept" includes figures that are not logged: 1.33 h of R figures in the refit (0.33 judging, plus the knit's 1.0 against 0.35 logged) and the whole 0.9 h voice (RECIPE lines). Fix: call it "recorded work (logged plus RECIPE)".
3. Line 60: 4.2 to 5.0 h at US$22 to 38 gives US$92 to 190. Adding the 1 to 2 h set aside gives 114 to 266. "90 to 270" mixes the two. Fix: give one range and name its hours.
4. Line 35: "under 0.5 h" for hair has no basis. The only figure cited, about 2 h for the sky-light try across three people, gives about 0.67 h, and that try kept nothing (RECIPE line 1896). Fix: give the basis or say "not recorded", and put the sky-light share under set aside.
5. Line 48: the window's task (time-log line 551) names only Darren's fit and the office board. A Ron share of 0.5 to 0.75 breaks line 21's equal-split rule. Fix: name the exception and its basis (DECISIONS 7 Nov 19:18).
6. Line 81: Hook row 5 is 2.4 h E for three men (eight variants at 0.3 h each, line 9), so about 0.8 h a man, not "0.3 h E each". Fix: write "0.3 h E a variant, 2.4 h for the three".
7. Line 90: the 55.35 h are all logged hours inside windows of every kind (unit-costs json basis), not production hours. Fix: say so, or take the production-kind hours from the time log.
8. Line 38: the levers file is TALK-LEVERS-2026-11-06.md. Fix: cite 6 Nov.

## Faults: QA first steps

1. Line 94: launch_line_check.py's self-test has 10 cases plus 1 (11 in all), not 11 plus 1. Fix: write "10 cases plus 1".
2. Line 129: the 5,842.5 MB median on runs.jsonl line 368 is over all 1,800 frames, because perf-hook.py's read() uses drop=0. It is not "after the drop" (the recount gives 5,842.5 over 1,800). Fix: write "its median over all frames".
3. Line 51: only some later legs sit at x 8.4 to 8.5. The 14 entries span x 8.0 to 10.06 and z 1.16 to 3.41. Fix: write "most later legs return to about (8.45, 3.41)".
4. Lines 37-38: route_walk.py line 282 records "at" before each leg moves. The run's last entry therefore does not show where its final leg ended, and a run that arrives on its last leg would fire falsely. Fix: measure against the next entry's "at" when there is one, and add that self-test.
5. Line 98: launch_line_check.from_log() returns the first "Command Line:". Judging the last one needs a new reader. Fix: say so in "Where it goes".
6. Lines 138-143, 160: Step 3b changes the Unreal build machine's perf step, so it is outside "need no Unreal". The QA item is "for Monday's order" (orders/2026-11-02.md line 89). Fix: hold 3b until Monday's order has costed it, under the week's rules.
