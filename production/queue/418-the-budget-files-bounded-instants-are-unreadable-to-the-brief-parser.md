line: instruments (an honest notation the reader cannot parse)
spec: FOUND 2026-09-21 by the queue 370 builder while checking readers, and
  confirmed by the resident: `python3 tools/morning-brief.py --selftest` fails
  one assertion of 41, "its newest reading is row 2026-09-21c reading 19
  percent, UNMEASURED at nothing-measured hour(s)".

  THE DATA IS NOT WRONG. `production/budget.md` writes `takenAt=2026-09-21T19:2xZ`
  where the `x` means the minute is BOUNDED RATHER THAN EXACT, which is the
  honest form when the reading arrived inside a window rather than at an
  instant. Three of today's rows use it: 12:1xZ, 16:2xZ, 19:2xZ. The brief's
  parser wants a timestamp and reads the whole field as unparseable, so the
  freshness it computes is `nothing-measured` rather than a number.

  SO THE FAILURE IS THE READER'S, NOT THE WRITER'S, and the fix must not be to
  invent a precise minute the reading did not have. A false precision in a
  budget file is worse than an unmeasured freshness, and the ten-hour rule that
  governs whether the studio may spend at all is computed from this field.

  IT IS PRE-EXISTING AND NOT CAUSED BY TONIGHT'S ROW, checked rather than
  assumed: 12:1xZ and 16:2xZ predate 19:2xZ and carry the same notation, so the
  assertion has been failing since at least midday. Tonight's row perpetuates
  it rather than introducing it.

  LOW URGENCY FOR ONE MEASURED REASON: `tools/morning-brief.py` is RETIRED and
  nothing calls it (grep for importers returns none), and `ledger/verify.py`
  is green without it. This is a latent fault in a tool that would matter again
  the day the brief is revived.
acceptance: the parser reads a bounded instant and says what it did with it,
  either by widening to the bound's worst case (19:2xZ becomes 19:29Z when
  asking "is this older than ten hours", the answer that cannot make a stale
  reading look fresh) or by printing the words "bounded" beside the figure so a
  reader knows which kind of instant they have. Both outcomes tested, accepting
  case first, with a real bounded row from the live file as the accepting
  fixture and a planted exact row beside it. The ten-hour spend rule's own
  arithmetic is re-checked against whichever choice is made, and the choice is
  stated where the field is written, in budget.md's own header.
status: READY 2026-09-21. Filed and not chased under rule 11. Blocked on
  nothing.
