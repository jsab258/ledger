line: instrument (tools/landed.py, the watcher every session trusts)
spec: tools/landed.py --contains is the sanctioned way to ask "has a run
  carrying my commit landed", named in CLAUDE.md's own CI rules as the thing to
  use instead of watching branch movement. On 2026-09-15 it was WRONG IN THE
  DIRECTION THAT KEEPS A SESSION WAITING FOREVER. Run 45 landed at 15:09Z as
  commit 22c922ee, "UE machine probe from cb0c55a2", carrying 72 files
  including every vignette still and four verdicts whose line 1 reads cb0c55a.
  With that commit merged into the working checkout, all three of
    python3 tools/landed.py --contains 0942cf1e
    python3 tools/landed.py --contains e1d19817
    python3 tools/landed.py --contains cb0c55a2
  printed "not yet: no run contains <sha>. 362 run(s) known, newest cb4767e".
  The count did not move either: 362 before the run landed and 362 after.
  THE CAUSE, read off its own docstring at line 11 rather than guessed: it
  waits for a `runs/<sha>.txt` record. Run 45 wrote verdicts and stills and did
  not write that record, so the watcher cannot see a run that plainly happened.
  WHY THIS IS WORSE THAN A WRONG NUMBER: a watcher that says "not yet" when the
  answer is "yes" is indistinguishable from a runner that has not returned, and
  the runner not returning is the exact condition this project lost sixty one
  hours to on 2026-09-11. A session following the documented procedure would
  have waited indefinitely beside landed evidence. The frame was found only
  because the session-start hook reported the checkout was behind origin and a
  human-shaped curiosity read the two new commits by hand.
acceptance: the watcher answers from what a run ACTUALLY LANDS rather than
  from a record type that run may not write. Both outcomes watched, ACCEPTING
  CASE FIRST: with 22c922ee in history, --contains cb0c55a2 must exit 0 and say
  which commit carries it; with a sha no landed run carries, it must still say
  "not yet" and must not invent a match. Its "N run(s) known" denominator is
  re-derived so it counts what it actually examined, and a window in which no
  run landed at all prints the words nothing measured rather than a stale
  count. Whether run 45 failing to write a runs record is itself a fault is the
  taker's second question, answered rather than assumed: if the record is meant
  to exist, the step that skips it is the bug and the watcher is innocent.
max_sessions: 1
status: READY 2026-09-15, filed the hour it was caught, and it is not a
  theoretical worry: it happened today and it hid a landed frame for as long as
  nobody looked past the tool. His standing rule of no new instrument this
  month unless one is retired does NOT bite here, because this repairs an
  instrument that already exists and adds none.
