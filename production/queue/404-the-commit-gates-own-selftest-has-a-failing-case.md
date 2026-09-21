line: instruments (the measurement of the studio itself)
spec: FOUND 2026-09-21 BY A BUILDER WORKING ON SOMETHING ELSE, confirmed by the
  resident, and filed rather than chased per CLAUDE.md rule 11.

  `bash .claude/hooks/selftest.sh` reports `74 passed, 1 failed`. The failing
  case is `the block line still declares the exclusion and that it bit`, which
  belongs to `verify-gate.sh`'s suite.

  IT PREDATES TODAY, established rather than assumed. `git status --porcelain
  .claude/hooks/` on 2026-09-21 returns ONE path, `log-agent-stop.sh`, which is
  queue 370's edit; `verify-gate.sh` is NOT modified in the working tree, and
  its newest commit is 9e49c53c. So nothing in today's six-builder batch
  touched the file whose assertion is failing.

  WHY IT MATTERS MORE THAN AN ORDINARY RED. `verify-gate.sh` is the PreToolUse
  hook that blocks a commit when files changed after the last green verify. It
  is the gate that holds this project's "never commit on a red" rule, and on
  2026-09-21 it was the gate refusing the resident's commits all afternoon. A
  gate with a failing case in its own suite is the shape CLAUDE.md rule 5b
  exists for: the accepting half is the half that goes unrun, and here some
  half is failing and nobody noticed.

  WHAT IS NOT YET KNOWN, and it is the first thing to measure rather than
  argue: whether the case fails because of the CODE or because of the TREE
  STATE. The assertion is about the gate's block line declaring an exclusion
  and that it bit, and the tree on 2026-09-21 carried fifty-odd paths of
  builder work, so a selftest that reads live tree state would fail for a
  reason that is not a fault in the gate. A selftest whose result depends on
  what happens to be uncommitted is itself the fault, one layer along, and
  that is the more likely finding of the two.
acceptance: the failing case is run against a CLEAN tree and against a dirty
  one, and the result of each is printed, so "the gate is broken" and "the
  selftest reads state it should not" are told apart by measurement rather
  than by reading the code; then whichever it is, is fixed, with the accepting
  case run first and a planted rejecting case beside it
max_sessions: 1
status: READY 2026-09-21, FILED AND NOT STARTED. It is studio work and it sits
  in the studio's third, behind the visual slice, the measurements and the art
  lane, per Jafar's order of 2026-09-21. It is NOT urgent in the sense of
  blocking: the gate still refuses commits on a red verify, which is its job,
  and the resident confirmed that behaviour working repeatedly the same day.
