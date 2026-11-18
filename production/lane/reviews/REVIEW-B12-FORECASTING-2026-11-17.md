# Review: B12 forecasting tool and note (17 Nov 2026)

Fresh hostile reviewer, 17 Nov 2026, no web. Files: tools/lane/forecast.py, tools/lane/test_forecast.py, tools/lane/forecast_example_plan.json, production/lane/B12-FORECASTING-METHOD-2026-11-17.md.

Verdict: PASS WITH FIXES (applied).

## What holds

- Monte Carlo is right: every planned item draws its own past ratio (with replacement), the drawn hours are summed, 20,000 runs, sorted, nearest-rank P50 and P80. Seeded (1990 by default); the same inputs give the same numbers. Tests check a single ratio gives an exact answer, a two-ratio case gives known percentiles, many items centre on the mean ratio, and repeat runs match.
- Time-log pairing: each start pairs with the next stop; a stop with no open start is ignored (none in the real log); a start with no stop is closed at the next start and counted (16 in the real log, matching the note). The final event in the log is a stop, so nothing is left open at the end.
- Note against tool, rerun today on the real log: 12.99 h coded, 157 h open plan, ratios 0.49, 0.07, 0.06, n09-1 and n09-13 with no hours, P50 32.5 h and P80 43.4 h alone, P50 168.7 h and P80 294.2 h with 4.3 added. All match.
- The note is honest that three ratios, two of them clearly missing hours, give no real forecast. Plain words, no em-dashes, no italics.

## Faults found and fixed

1. A backwards interval was added as negative hours. Line 570 of the time log has a stop 0.27 h before its start (task "n02-9-pass-is-players-launch"); the tool silently subtracted it. Now skipped and counted as "backwards_intervals_skipped". Effect: unmatched hours 246.75 to 247.01. New test.
2. Few data points were not flagged in the output. The tool now warns when there are fewer than 8 own ratios (the note's own bar for B12 medium) and when any ratio is under 0.25 (a sign of missing hours). New test.
3. Note updated to match: 247.01 h, the backwards pair, the warnings, 12 of 12 tests.

## Left as is (judgement, not faults)

- An unclosed start is charged up to the next start, which can include idle time (one is 5.4 h, line 341). It is counted and named; dropping such intervals would be equally defensible. Worth a look once coded logging starts.
- Aliases match only at the start of a task name, so names like "tool loop: kiln round 1 (n16-1)" will not match by code. The main session should use aliases or put the code first, as the note already asks.
- An outside ratio such as 4.3 weighs the same as one finished item; the note says so.

Tests: python3 -m pytest -q tools/lane/test_forecast.py, 12 passed.
