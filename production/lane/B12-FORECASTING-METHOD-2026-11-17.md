# B12 Estimating and forecasting: method and first tool (17 Nov 2026)

Written by a lane helper, 17 Nov 2026. [M] = measured today from the repository. [READ] = read at source today, [SS] = search snippet only, [I] = inference.

## Why B12 is low

Phase 1 ran 4.3 times over its plan. Phase 2's 426 to 743 hours come from plan figures, not from what past work really cost. The cost of one complete person is not yet measured. A plan made the same way as the one that ran 4.3 times over will likely run over again.

## The professional method

1. Reference class forecasting (Flyvbjerg, after Kahneman and Tversky). Do not build the estimate only from the inside, task by task. Look at a class of similar past projects, see how far their actuals ran past their plans, and apply that "uplift" to the new plan. The uplift is chosen for the risk you will accept: a P50 uplift gives a 50% chance of finishing within it, a P80 uplift an 80% chance. Used by the UK Treasury's optimism-bias guidance and by transport agencies. [SS] Flyvbjerg, "From Nobel Prize to Project Management: Getting Risks Right", 2006, arxiv.org/abs/1302.3642; [SS] PMI, "Planning for the planning fallacy".
2. Evidence-based scheduling (Joel Spolsky, 26 Oct 2007). Our best reference class is our own history. For each finished task keep planned hours and actual hours; actual divided by planned is its "velocity" (here: the ratio). To forecast, run a Monte Carlo: give every new task a randomly drawn past ratio, add up, repeat many times; the spread of the sums is the forecast. [SS] joelonsoftware.com/2007/10/26/evidence-based-scheduling/; [SS] Wikipedia, "Evidence-based scheduling".
3. P50 and P80. P50 is the total that half the simulated outcomes stay under; P80 the total that four in five stay under. Many owners set the budget at P80 and hold the gap between P50 and P80 as contingency. [SS] Galorath, "2025 Industry Report on Cost, Schedule, and Risk"; [SS] open-exam-prep.com, AACE PSP "Risk outputs, confidence dates, contingency".

Unreached: none of the pages were fetched in full in the 11-minute budget; every source above is a search result only, so none of their claims count as evidence until read.

## What the tool does

tools/lane/forecast.py (standard library only; tests in tools/lane/test_forecast.py, 12 of 12 pass [M]).

- Reads production/time-log.jsonl, pairs each "start" with the next "stop", and sums hours per task name. A start with no stop is closed at the next start and counted. A pair that runs backwards in time is skipped and counted.
- Reads a planned-hours file (JSON or CSV: code, planned hours, done or not).
- Matches log tasks to plan items by the item code at the start of the task name (for example "n16-3 ..."). A plan item can list extra name prefixes ("aliases") for tasks logged without the code.
- For each finished item: ratio = actual / planned. Outside ratios can be added (for example phase 1's 4.3).
- Monte Carlo: 20,000 runs, seeded, so the same inputs always give the same P50 and P80.
- Warns when there are fewer than 8 own ratios or a ratio under 0.25 (a sign of missing hours).
- Prints matched ratios, matched and unmatched logged hours, finished items with no logged hours, and the forecast.

Example plan: tools/lane/forecast_example_plan.json, planned hours from the orders of 9 Nov (finished n09 items) and 16 Nov (open n16 items, 157 h in all).

## First result on real data: matching does not yet work

- Logged hours that carry an item code: 12.99 h. Logged hours with no code: 247.01 h [M]. About 95% of the log cannot be put against any item.
- Finished n09 items with any coded hours: three. Their ratios: 0.49, 0.07 and 0.06 [M]. Two finished items (n09-1, n09-13) have no coded hours at all [M]. 16 starts had no stop, and one pair ran backwards in time and is skipped [M].
- Those ratios say the work took a tenth of its plan. That is false: phase 1 ran 4.3 times over. The log is missing most of the time, not the work being fast [I].
- So the forecast from the log alone (P50 32.5 h, P80 43.4 h for a 157 h plan [M]) is meaningless. With phase 1's 4.3 added as a fourth ratio it gives P50 168.7 h, P80 294.2 h [M], but that is one outside number doing all the work; it is shown only to prove the tool runs.

What the main session must fill:

1. From now on, every time-log start names its item code first ("n16-3 ..."), helpers' time included (CLAUDE.md already says helpers' time goes against their item).
2. Add aliases in the plan file for past tasks logged under names like "tool", "advisor", "study" or "n02-9-..." where the item is known, so past hours count.
3. Keep the done flags current in the plan file as items close; carried-over items keep their original plan hours and gain the new item's hours.
4. Phase 1's per-item plans and actuals, if they exist anywhere, entered as finished items: that gives a real reference class instead of one 4.3.

## What counts as proof that B12 rises to medium

- At least 8 finished items with coded actuals and plans, so the ratios are our own.
- Two consecutive weekly orders forecast at P80 by this tool on the Monday (the forecast written into the order, dated), and each order's real logged total landing under its P80.
- If either lands over P80, B12 stays low and the ratio pool is checked for missing hours before anything else.

## One line for the recipe map

B12: low. Method and tool ready (reference class plus evidence-based scheduling, P50/P80 Monte Carlo, 12 tests pass); 95% of logged hours carry no item code, so no honest forecast yet; medium after two weekly orders land under their P80.
