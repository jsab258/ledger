line: instruments (ledger/verify.py, director_cadence and _cadence_scope)
spec: Two verify runs minutes apart with NO COMMIT between them read the gated
  line count as 156 and then as 0. The first refused the commit; the second
  allowed it. A commit gate whose reading moves by 156 lines while nothing is
  committed is a gate nobody can act on, because a red one cannot be
  distinguished from a red one that will be green if you wait.
acceptance: the two readings are explained, and whatever explains them is
  printed on the line so a future reader sees the cause rather than the
  discrepancy; or the gate is shown to be correct both times and the item says
  why
max_sessions: 1
status: READY 2026-09-16, observed once and NOT reproducible after the fact,
  which is why it is filed with both readings rather than diagnosed.

  THE TWO READINGS, verbatim from the runs:

      11:0xZ  DIRECTOR NOT SPAWNED: 156 GATED line(s) of 922 changed work
              line(s) (63 tracked + 859 untracked in 3 new file(s)) vs 100
              threshold
              workByScope=scripts:0/ledgertools:61/ledger:156/tools:705/
                          workflows:0/githooks:0/claude:0/ueprobe:0/content:0

      11:2xZ  director cadence ok
              linesGated=0/766

  766 is 922 minus 156, so the whole gated portion left the count.

  WHAT IS PARTLY EXPLAINED. Between the runs a builder ran
  `git add -N tools/canon-register-check.py`, an intent-to-add with no content
  staged, to satisfy verify's own tools_tracked check. That file is 703 lines,
  and 859 untracked minus 703 is exactly 156, so the add-N plainly moved that
  file from the untracked bucket to the tracked one.

  WHAT IS NOT EXPLAINED, AND IS THE ITEM. The 156 was reported under the
  `ledger` SCOPE, which the table at verify.py:3699 defines as the `ledger/`
  catch-all after the ledgertools carve-out. At that instant NO untracked path
  was under `ledger/`: the untracked files were a wake record under
  `production/wakes/` and the new tool under `tools/`. So either an unmatched
  path is falling into the `ledger/` catch-all, or the untracked count is
  being attributed to a scope it does not belong to. Both are wrong in the
  same direction: work that is ungated by D45 being counted against the gate
  that D45 exists to narrow.

  WHY IT MATTERS MORE THAN ITS SIZE. This gate decides whether a commit may
  happen. On the run that read 156 the resident held roughly twenty files of
  finished work, correctly, on a number that was probably not real. A gate
  that refuses on a phantom teaches a resident to re-run it until it agrees,
  which is exactly the habit that makes a real refusal get ignored.

  FIRST COMMAND FOR WHOEVER TAKES IT: `_cadence_scope` with a path under
  neither `ledger/` nor any other listed prefix, and see which bucket it
  lands in. The table's own comment says "order is load-bearing, first match
  wins, and the catch-all keeps the game", so the catch-all's behaviour on a
  non-ledger path is the question.

  UNDER D45 a tool that measures the game: a test, no review. But it is the
  COMMIT gate, so a change to it wants a director at landing on the same
  reasoning the 06:35Z ruling used for the ue-probe line count.
