line: instruments (tools/wake-queue.py; production/wakes/)
spec: Jafar, 2026-09-21 ("ONE CHECK"): "Project threads on the new Claude
  Code projects feature wait out a usage limit and resume on their own
  when it resets. Say whether the wake system can do the same, so a limit
  no longer needs my reading to restart work."

  WHAT tools/wake-queue.py ACTUALLY DOES, read in full at filing time: it
  is a TURN-BOUNDARY mechanism. A due record on disk under
  production/wakes/ is drained by .claude/hooks/wake-drain.sh, registered
  as the Stop hook, which fires at the end of a turn WITHIN A RUNNING
  SESSION and can block that turn from ending (up to BLOCK_CAP=3
  cumulative blocks per record) until the record is discharged. Its own
  docstring is explicit about what it does not solve: "WHAT CANNOT BE
  FIXED FROM INSIDE THIS REPOSITORY... the scheduler's delivery
  semantics," and its fix is only that a wake landing mid-turn is not
  lost, not that a session can be revived after it has stopped running
  entirely.

  THE QUESTION IS ABOUT A DIFFERENT FAILURE MODE. A usage-limit stop is
  not a turn boundary inside a live session; it is the SESSION ITSELF
  unable to take another turn until the limit resets, which could be
  hours away. The wake-drain hook cannot fire because nothing is running
  to fire it on, and nothing in tools/wake-queue.py schedules a NEW
  session to start later. This item's job is to determine, by reading how
  sessions here are actually started, the platform's cron and trigger
  mechanism referenced in the wake-queue.py docstring (trig_... triggers
  with cron schedules bound to persist_session) and
  tools/runner/executor.py's dispatch path, whether ANY existing
  mechanism restarts a session once a usage limit clears, distinct from
  wake-queue.py's turn-boundary role.

  CLAUDE.md rule 13 already states the studio's own practice for this:
  "On a limit, parse the reset from the notice and arm for it," meaning
  today a session that hits a limit is expected to arm a wake for the
  reset time before it ends, which then depends on something ELSE
  starting a new session at or after that wake's due time. Whether that
  something else exists, and whether it behaves the way Claude Code's own
  projects-feature usage-limit wait works, is the actual open question.
acceptance: a plain yes or no answer, evidenced rather than asserted:
  EITHER a mechanism is found, named, with its file and how it is
  triggered, that starts a new session after a usage-limit reset with no
  person acting in between, OR none is found and the item states exactly
  what was checked (the platform trigger and cron mechanism,
  tools/runner/executor.py, tools/wake-queue.py, .claude/hooks/,
  .claude/settings.json) and why each does or does not cover a full
  session restart rather than a turn boundary; the answer is recorded in
  production/wakes/README.md, its own file names this as the place, "or
  queue 398", with a dated entry, distinct from the existing "why this
  folder exists" section rather than merged into it
max_sessions: 1
status: READY 2026-09-21, filed as studio-third work, taken at a
  checkpoint. Not gated on the visual slice or the measurements. This is a
  read-and-report item; it does not build a new mechanism even if the
  answer is no, per CLAUDE.md rule 11, a question is a question, answer
  it, offer the work separately. This is this week's work.
