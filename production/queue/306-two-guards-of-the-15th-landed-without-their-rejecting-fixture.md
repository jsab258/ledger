line: instrument (ledger/verify.py and tools/producer-check.py selftests)
spec: Two guards landed on 2026-09-15 with their accepting case run on the
  live tree and their rejecting cases never run. Both are the class the
  instrument rules name: a guard read is not a guard run, and the test line
  fixed by hand at 00:52Z the same night (a logical-not that could not fire)
  is what a plain-looking condition can do.
  ONE. ledger/verify.py:served_marker_provenance(), queue 256 step 2. It is
  running (called once, inside producer_register(), red on any failure) and
  the live marker passed it. Its name occurs twice in the file, the
  definition and the call; no fixture drives a marker that should be
  refused, although the docstring says `root` exists so the rejecting case
  can be pinned to a synthetic tree. Plant, on a synthetic root, accepting
  case first: a `none` marker (accepted with its own token); a 12-character
  prefix where a 40-hex sha is required; a well-formed sha no object
  answers; a real commit that is NOT an ancestor of HEAD; a `printedBy`
  naming no publish-glance run id; a `servedUrl` that is not the origin
  producer-check.py sets. One line moves with it: the guard reads
  tools/producer-check.py from ROOT.parent rather than from `repo`, so a
  synthetic root cannot carry its own copy of the tool and the origin case
  cannot be planted; read it from `repo`.
  TWO. tools/producer-check.py's research ladder. On 2026-09-15 it read
  researchVerbatimWaiverBit 10/10 instead of 5/10 for ten minutes, because
  its second rung dropped `pre_move` and so toggled two contributors at
  once, crediting a linkfloor finding to the research waiver. The builder
  carried `pre_move` and the ruling of 05:43Z made the rung count by rule
  name. No fixture has a file on BOTH lists, so nothing in the suite would
  go red if either repair were undone. Plant one file named on both
  RESEARCH_VERBATIM and PRE_MOVE_MESSAGES, carrying one banned word and no
  link, marker naming a served commit: the research bit must read 1 with
  exactly one finding removed and that finding `banned`; the pre-move bit
  must read 1 with `linkfloor` removed; and toggling the research list off
  must leave the pre-move numbers unchanged.
  No new instrument: fixtures inside two suites that exist, per the reading
  of the monthly rule in the rulings of 2026-09-14 (20:01Z) and 2026-09-15
  (00:52Z and 05:43Z).
acceptance: the live tree still accepted by the provenance guard with the
  same token shape (markerProvenance=ok/commit-<12>/ancestor-of-HEAD/...),
  then each of the six planted markers refused with its own named token; the
  both-lists file graded with the two bits reading 1/1 each and the rules
  named; every count printed with its denominator; accepting case first in
  both suites, both watched.
max_sessions: 1
status: READY 2026-09-15, filed by the ruling of 05:43Z
  (game-design/decision-2026-09-15-ruling-the-forty-are-waived-by-name-and-the-walk-back-stands-as-his-number.md,
  section 8). Not blocking that batch: every refusal branch of the provenance
  guard was read and each returns red, so an untested branch there fails
  loud rather than silent, and the research ladder's repair is a no-op on
  the live number by construction (the ruling requires that number printed
  before and after). Cheap, and owed.
