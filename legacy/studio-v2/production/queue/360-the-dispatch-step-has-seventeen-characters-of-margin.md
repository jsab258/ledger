line: instruments (tools/workflow-size.py and the cook/staging steps of
  .github/workflows/ledger-probe-unreal.yml)
spec: `python3 tools/workflow-size.py` reads, today:

      workflow-size: 18 workflow(s), largest step 23167 chars
                     (17 under the largest ever accepted)

  SEVENTEEN CHARACTERS. The next person who adds a line to that step breaks
  dispatch, and dispatch is how every rendered frame in this project is
  produced. The sky builder of 2026-09-16 hit this: it could not add a second
  `Start-Process` step for the sky material and routed the second editor run
  through `make_base_material.py` instead, which is a good answer to the wrong
  question.

  AND THE BOUND IS NOT A MEASURED LIMIT, which is the part that matters and
  which the tool's own wording admits: "the largest ever ACCEPTED" is the
  biggest step that has HAPPENED to work, not the biggest that works. Nobody
  has printed the series. So the studio is 17 characters from a cliff whose
  position is unknown, and could already be past it in a way no run has
  exercised.
acceptance: either the real limit is established and named with what
  established it, or the largest step is brought down far enough that the
  margin stops being a number anyone has to think about; and the tool says
  which of the two happened. A run that cannot dispatch prints why rather than
  failing as a generic error
max_sessions: 1
status: READY 2026-09-16, filed and NOT started, under Jafar's standing rule:
  an audit finding is filed and the standing order resumes.

  DO NOT RAISE THE BOUND TO MAKE THE RED GO AWAY. It is not a threshold
  somebody chose; it is an observation of what has worked. Raising it asserts
  something about the platform that nobody here has tested, and the cost of
  being wrong is that a dispatch fails on the one channel this project can
  read.

  THE CHEAP HALF FIRST, and it needs no run: the step is largely inline
  PowerShell. Moving any of it into a committed `.ps1` that the step CALLS
  converts characters in the step into characters in a file with no such
  limit. `tools/workflow-size.py` already knows how to count, so the before
  and after are one command apart.

  WHY THIS IS NOT MERELY TIDYING. The failure mode is silent in the way this
  project has been bitten by before: a step that is too large does not
  announce that it is too large, and `.claude/rules/ci.md` already records
  that licence seats and shared runners "fail SILENTLY in the only channel you
  can read".
