line: instruments and reporting, jointly
spec: FOUND WHILE WITHDRAWING THE SPLIT ON JAFAR'S ORDER, and it is the half
  the withdrawal does not reach.

  THE TOOLS NOW REFUSE THE RATIO. `ledger/verify.py`'s footer prints the
  withdrawal marker unconditionally, and `tools/morning-brief.py`'s prose and
  verdict keys do the same, each with selftest rungs proving the marker cannot
  move with the number.

  BUT THE LIVE BRIEF IS HAND-WRITTEN AND UNCHECKED FOR THIS. `morning-brief.py`
  has been RETIRED since 2026-09-09 (the refusal is at :2436, in code rather
  than in a comment), so no brief it composes has reached Jafar since. The live
  path is a Producer turn writing `production/briefs/<day>.md`, checked by
  `tools/producer-check.py`. And there, `RULES_NO_REGISTER = ("split",
  "filedline")` takes the split rule out of EVERY register's enforced list, so
  nothing checks a hand-written brief for it in either direction. A Producer
  could write "nine sessions went to the studio and two to the game" tomorrow
  and every gate would pass it.

  A SECOND DOCUMENT POINTS AT THE RETIRED NUMBER. `production/sunday.md`
  section 5 instructs the weekly summary that "ledger/verify.py's footer prints
  gameShareDay and fableShareAll as COUNTS OF SPAWNS". It prints a withdrawal
  marker there now. Nothing generates the Sunday summary, so nothing computes
  the ratio today; the instruction is simply pointed at a number that is gone.

  WHAT IS NOT WRONG, checked rather than assumed: today's brief,
  `production/briefs/2026-09-16.md`, carries no split sentence at all, so there
  is nothing to correct retroactively.
acceptance: a hand-written brief or weekly summary that states the studio
  versus game split as a ratio is REFUSED by the gate that reads it, with the
  accepting case (a brief stating the withdrawal) proven first; and
  production/sunday.md names the marker rather than a count
max_sessions: 1
status: READY 2026-09-16, filed and NOT started, per CLAUDE.md rule 11: the
  finding is filed and the standing order resumes.

  WHY THIS IS SMALL BUT NOT SKIPPABLE. Jafar's instruction was "add the column
  before claiming the ratio again, or stop printing the number." The tools have
  stopped. A path where a human can still write it is the same claim arriving
  by a different door, and it is the door that actually reaches him.
