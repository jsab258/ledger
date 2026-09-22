line: instrument and channel (a silence nothing alarms on)
spec: a queued self-hosted run that is never claimed is invisible until a
  human looks. On 2026-09-15 run 45 sat QUEUED from 06:16:37Z with
  run_started_at equal to created_at, and the only thing that noticed was a
  resident checking the Actions API by hand at 07:10Z. This is the SECOND
  occurrence, and the cost is measured here off the landing commits rather
  than carried over from another item's number: THE LAST FRAME BEFORE THE GAP
  LANDED 2026-09-11T06:12Z AND THE NEXT ONE 2026-09-14T14:52Z. Three days and
  eight hours with no picture at all, over eleven probe landings walked. The
  briefs of the 12th and 13th went with it and the 12th's is still unsent
  (queue 303). Nothing in the tree reads "is there a queued run older than N
  minutes on [self-hosted, ledger-pc]".
  A NUMBER THIS ITEM DELIBERATELY DOES NOT REPEAT, because it did not
  reproduce: queue 291 and queue 303 both say "sixty one hours" beside the
  endpoints 2026-09-11 09:04 and 2026-09-14 17:47, and that span is eighty
  hours and forty three minutes, not sixty one. One of the two is wrong and
  which is not established here. The figure is about that workflow step's own
  run history and not about frames, so this item uses its own measurement and
  leaves the discrepancy named for whoever takes 291.
  THE DISCRIMINATING READING ALREADY EXISTS AND IS FREE. One push produces two
  runs at the same instant; the GitHub-hosted one completes and the
  self-hosted one does not. That pair is the alarm, and it separates "Actions
  is degraded" from "that label has no runner" without a second request.
  THE OTHER HALF, and it is why this is worse than it looks: the bot's
  liveness counter (botSweepPasses, botUptimeSec, botSweepWrittenAt) is
  written into an UNTRACKED directory on his machine and pushed by nothing. It
  reaches this side only when a step on the self-hosted runner copies it out,
  so the one file that would say "the machine is up, the service is not" is
  unreadable in exactly the situation it is for.
  HIS STANDING RULE BINDS THE ANSWER: no new instrument this month unless one
  is retired in the same batch. So the taker's first job is to find the
  retirement or to show that this rides an instrument that already exists.
acceptance: a reading that is red while a self-hosted run has been queued
  beyond a bound, and green otherwise, with BOTH outcomes watched and the
  ACCEPTING case first: a normally-served run must not raise it. The bound is
  MEASURED, not chosen: print the created-to-started series over the runs that
  exist before setting a number, per rule 2. A zero ships its denominator,
  which here is how many self-hosted runs were examined; a window with no
  self-hosted run at all prints "nothing measured" rather than green.
max_sessions: 1
status: READY 2026-09-15, filed while blocked by the fault it describes. NOT
  blocking on its own, and it must not be taken while the visual queue is
  moving: his order is the bins, then wetness, then the dusk frame.

  WHAT THIS ITEM IS NOT. It is not a licence to re-dispatch. A second queued
  run behind a runner that is not claiming proves nothing and confuses the
  ancestry check when the runner returns.

  A QUESTION THE TAKER MUST ANSWER RATHER THAN ASSUME: whether the alarm can
  ride the cheap checks that already run on every push, so that it costs no
  new scheduled thing. If it cannot, say so with the reason rather than
  quietly adding one.
