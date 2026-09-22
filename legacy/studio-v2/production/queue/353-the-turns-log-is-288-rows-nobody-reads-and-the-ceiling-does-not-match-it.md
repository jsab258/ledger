line: instruments (.claude/agent-turns.tsv, tools/spawn-cost.py, the agent
  definitions' maxTurns, and whatever at dispatch reads or ignores it)
spec: `.claude/agent-turns.tsv` holds 288 rows, one per finished spawn since
  2026-09-03, carrying agent, tier, turns and alines. ITS OWN HEADER SAYS the
  first row it writes "is read before any number from the turns log is quoted
  anywhere". Nothing quoted it: not the resident's two attempts to measure
  agent spend, not queue 336, not waste-lesson 9. AND WHEN IT WAS FINALLY
  READ, IT CONTRADICTED THE CEILING: 8 of 15 declared maxTurns values sit
  under their own role's observed peak.
acceptance: the relationship between a definition's maxTurns and a logged turn
  is established by running something rather than by reading a comment, the
  ceilings are set from the series either way, and the turns log is consulted
  by whatever step sets or quotes a budget
max_sessions: 1
status: READY 2026-09-16, found by the builder that Jafar's own ruling sent to
  fix the budgets. It found the library while looking for the number.

  THE SERIES, printed before any bound, from the log rather than from shape.
  n is rows, peak is max, median is median:

      role                 declared     n  median   peak
      artifact-reader            40     3      42     42
      claim-auditor              35     2    38.5     39
      content-wrangler           45     9      54     99
      dialogue-writer            35     1      12     12
      engine-specialist          45    75      63    133
      guard-tester               35     0       -      -
      instrument-builder         70    58    78.5    194
      integrator                 50     0       -      -
      measurement-auditor        35     0       -      -
      planner                    60     3      36     44
      producer                   30    35      11     37
      reach-auditor              35     0       -      -
      studio-director            40    73      14     72
      systems-builder            70    12      78    104
      world-designer            200     9     138    181

  8 under their own peak, 4 nothing measured, 3 ok. instrument-builder
  declares 70 and its MEDIAN run is 78.5.

  THE TENSION, AND IT IS NOT RESOLVED HERE. Four facts, each checked:

  1. tools/spawn-cost.py's docstring at line 41 says "`turns` is what
     `maxTurns` bounds". A docstring is a claim, not evidence.
  2. `maxTurns: 45` has been in engine-specialist's definition since
     2026-08-25 (it was 25 for one day before that). Traced through git.
  3. SIXTY FIVE engine-specialist runs exceed 45 turns, from 2026-09-05
     through today. That is impossible if 45 bounds this unit.
  4. AND TODAY ONE DIED AT 45. The harness reported agent a4c0cad6c63dca42a
     as stopping at "its 45-turn limit"; the log records turns=47 for that
     same agent, and the notification recorded 49 tool uses.

  So something enforced 45 today, the same ceiling has been declared for
  three weeks, and 65 runs went past it. Fact 3 and fact 4 cannot both be
  about the same quantity. WHOEVER TAKES THIS RUNS THE THING RATHER THAN
  ARGUING: the question is what the harness actually bounds and in what unit,
  and the resident could not settle it from inside the repository.

  THE RESIDENT'S OWN CLAIM IS OVERTURNED HERE and it belongs in this item.
  Earlier today the resident reported that "the declared values MATCH EVERY
  OBSERVED DEATH EXACTLY (40, 45, 70, 70)". Four deaths did match. The
  population does not: the same roles have 58 and 75 logged runs spending far
  more. FOUR MATCHING POINTS WERE READ AS A RULE WITHOUT LOOKING AT THE
  DISTRIBUTION THEY CAME FROM, which is the same fault as reading a peak as a
  description.

  AND IT IS JAFAR'S PATTERN AGAIN, THE FOURTH CLEAR INSTANCE: a declared value
  that nothing consults is decoration. The turns log is the decoration here,
  and the file that exists to stop a number being quoted unmeasured was itself
  never quoted. It sits beside goal-block-check being unwired, maxTurns being
  unread at dispatch, and light_probe being written 49 times and read zero.

  UNDER D45 a tool that measures the studio rather than the game: a test, no
  review. But the ceilings decide whether work completes, so a change to them
  wants the director already spawning on this batch.
