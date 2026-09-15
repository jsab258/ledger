line: instrument and channel (the studio's own brake)
spec: Jafar ruled on 2026-09-15 that a budget reading older than TEN HOURS
  means the day is unmeasured, and that the brief asks him for the reading as
  its first line with the studio holding at inbox-only until he answers. The
  ruling is recorded in production/budget.md stop condition 2,
  production/repo-move-triggers.md step 3, production/watchdog-prompt.md and
  .claude/agents/producer.md. NOTHING EVALUATES IT. Two tool changes are owed:
  ONE. tools/producer-check.py must require the reading line in the BRIEF
    register. SECTIONS today is HEADLINE, WHAT CHANGED, NEEDS YOU, NEXT
    VISIBLE THING, BUDGET, and a brief with no reading line passes. It is a
    LINE and not a NEEDS YOU item: it carries no options, no recommendation,
    no default and no deadline, because a day he does not answer is a day the
    studio does not spend.
  TWO. tools/morning-brief.py must evaluate ten hours. It carries
    BUDGET_STALE_DAYS = 2 and its own comment explains why: "The table's
    granularity is a DATE, not an instant, so 48 hours is read as two days."
    TEN HOURS CANNOT BE READ THAT WAY, so this item is blocked on the data
    before it is blocked on the code.
  THE DATA HALF, and it is the first thing the taker does: budget rows carry a
  DATE column and their time only in prose, as "Reported by Jafar at about
  04:1xZ", which is not a parseable instant and in that case not even a
  parseable time. The ruling adds takenAt=<ISO instant>, stamped by the
  RESIDENT when the reading arrives rather than asked of him, because when it
  arrived is what staleness means and asking him for a clock time would
  reintroduce the remembering he ruled away. A row with no takenAt reads
  UNMEASURED, never fresh.
acceptance: a brief with no reading line is REFUSED by producer-check and one
  with it PASSES, both watched, accepting case first. morning-brief prints
  UNMEASURED for a row whose takenAt is more than ten hours old, FRESH for one
  inside it, and UNMEASURED for a row carrying no takenAt at all, with the age
  printed beside the verdict and the three cases watched as three planted
  fixtures. A zero ships its denominator: the done line says how many rows
  were examined and how many carried takenAt. NO NEW INSTRUMENT IS ADDED and
  his standing rule does not bite: both tools exist, both already run, and
  this changes what they read rather than adding a reader.
max_sessions: 1
status: READY 2026-09-15, filed the hour it was ruled, and BLOCKED ON THE
  RULING ITSELF, which is the right way round and worth recording. His reading
  was fifteen hours old when he ruled, so the day was already unmeasured and
  his own rule forbids spawning a builder. The first thing his next reading
  buys is the checker that enforces the rule about readings.
