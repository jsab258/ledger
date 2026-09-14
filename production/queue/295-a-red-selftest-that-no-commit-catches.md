line: tools (the gate's own coverage)
spec: tools/runner/cards.py --selftest is RED on main right now and has been
  passing unnoticed because nothing runs it. Measured 2026-09-14:
  "cards selftest: 71 passed, 1 failed (72 case(s) run)", the failing case
  being accept/the-live-queue-has-a-ruled-this-week-section.
  WHY NOTHING CAUGHT IT: ledger/verify.py's TOOL_SELFTESTS (line 1326) holds
  exactly ten rows, inbox, inbox-read, bot config, outbox, supervise,
  executor, wake queue, checkout gate, brief and producer day. There is no
  cards row, so no commit has ever run it. A tool with a selftest that the
  gate does not call is a tool whose selftest is decorative.
  THE GENERAL SHAPE IS THE FINDING, not the one red case: nothing enumerates
  which tools HAVE a --selftest and compares that set against TOOL_SELFTESTS.
  The list is hand-maintained, so a tool gains a selftest and the gate never
  learns of it, silently, exactly as happened here.
acceptance: the red case diagnosed and either fixed or ruled as a known
  finding with its reason; cards added to TOOL_SELFTESTS; AND a check that
  enumerates every tools/**.py carrying a --selftest flag and fails when one
  is absent from TOOL_SELFTESTS, printing both counts with denominators so a
  future gap announces itself instead of waiting to be noticed. That third
  part is the one that stops this recurring, and without it this item fixes
  one instance of a class.
max_sessions: 1
status: READY 2026-09-14. Found by a builder that had been dispatched to fix
  the brief send, while confirming its own revert left the tree as it found
  it: it ran the neighbouring selftests to prove nothing had moved and one of
  them was already red. Reported under rule 11 rather than fixed in passing,
  which was correct: it is unrelated to the brief and would have ridden into
  that commit unexplained. Verified independently by the resident before
  filing, both the red and the absent row.
