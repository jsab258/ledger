line: instruments (the measurement of the studio itself)
spec: RAISED BY JAFAR 2026-09-16, AND HE NOTES IT IS THE THIRD AUDIT TO SAY IT.
  His instruction: "The split cannot be computed at all until the spawn log
  records what a session touched, not just who ran and why. Three audits have
  now said this. Add the column before claiming the ratio again, or stop
  printing the number."

  WHAT THE LOG HAS AND WHAT IT LACKS. `.claude/agent-log.tsv` records the day,
  the agent and the reason. It has NO COLUMN NAMING A FILE. So every reading
  of game work against studio work is a count of ROLE NAMES, and the error in
  that proxy cannot be measured from the log that produces it: an
  engine-specialist repairing an instrument counts as game work, an
  instrument-builder adding a gameplay readback does not.

  THE SIZE OF THE ERROR IS KNOWN AND IT IS NOT SMALL. 25 August read 32/110 by
  role. 5 September read 12/27 by role on a day that queue item 111 counted
  the real work at 1. A proxy that can read twelve where the answer is one is
  not a noisy measurement, it is a different quantity wearing the name.

  THE CLAIM IS ALREADY WITHDRAWN. The other branch of his instruction was
  taken on the day he gave it, across all three sites that printed it:
  `gameShareDay` in ledger/verify.py's footer, the prose sentence in
  tools/morning-brief.py that he actually reads, and that file's `splitStudio`
  and `splitGame` verdict keys. The counting is untouched, so the day this
  item lands the ratio does not have to be rebuilt from nothing.
acceptance: the spawn log carries a column naming what each session touched,
  populated by the mechanism that writes the row rather than by a promise; and
  a split computed from it is printed WITH the count of rows the column could
  not answer for, so a partial column cannot read as a complete one
max_sessions: 2
status: LANDED 2026-09-21. CORRECTED UNDER D43, AND THE FALSE LINE IS NAMED
  RATHER THAN DELETED: this read "READY 2026-09-16, filed and NOT started" until
  tonight, while commit cbadeeb3 of 2026-09-21T13:39Z had ALREADY added columns
  7 and 8 to .claude/agent-turns.tsv, the --work-split mode and 828 lines of
  tools/spawn-cost.py. A resident briefed a builder on that false line hours
  later. THAT IS THE THIRD STALE-STATUS INCIDENT OF THE DAY, after
  kit-survey.md's "nothing in this report is wired" re-issuing a dispatch that
  landed in August and the Epic card's ruled premise sitting in WAITING, and it
  is the queue-file form of learning.md L38: a line nobody updates sends the
  studio back over finished ground. What the resumed session added was the half
  genuinely missing, the split's SECOND denominator, and that half is real: the
  buckets counted stop-log rows (sessions=297) while this item's own sentence
  names the SPAWN log (749 rows), so a spawn that never reached SubagentStop sat
  in no bucket and on no side, and answerable=11/297 could be misread as a share
  of every session there has ever been. It is not.

  ONE CLAUSE OF THE ACCEPTANCE CANNOT BE MET LITERALLY AND THE REASON IS SOUND.
  It says "the spawn log carries a column". It cannot: .claude/agent-log.tsv is
  written at SubagentStart by .claude/hooks/log-agent.sh, and at SubagentStart a
  spawn has touched nothing. The column lives on the STOP log, joined on
  agentId, filled by tools/spawn-cost.py reading the session's own transcript
  rather than by anything the agent says about itself, which satisfies "by the
  mechanism that writes the row rather than by a promise" exactly. The cost of
  that correctness is a coverage gap, and the gap is now counted rather than
  hidden: spawnRowsCumulative=749 rowsCarryingAnId=219/749
  spawnIdsWithNoStopRow=12/146 stopIdsWithNoSpawnRow=163/297, with that last
  number split at the instant the agentId column began and reading
  sinceThatInstant=0, which says the start hook is NOT currently missing spawns.
  Previously that 163 was unexplained and could have read as a live failure.

  THE ITEM'S OWN SIZE-OF-ERROR NUMBERS ARE NOT REPRODUCIBLE and are left
  standing rather than quietly replaced: it says the role proxy read "12/27
  where the answer was 1"; the measured proxy error over the 11 answerable
  sessions is disagree=2/11. Those are not the same quantity and n=11 is too
  small to overturn a hand tally, so both are recorded.

  Superseded text follows: READY 2026-09-16, filed and NOT started before the
  visual slice, per
  his instruction and per CLAUDE.md rule 11.

  THE HARD PART IS NOT THE COLUMN, IT IS WHO FILLS IT. A column an agent
  writes about itself is an attendance register with an extra field, which is
  the fault this item exists to fix, one layer along. That is the design
  question this item opens with and it should not be answered by adding a
  field and hoping.
