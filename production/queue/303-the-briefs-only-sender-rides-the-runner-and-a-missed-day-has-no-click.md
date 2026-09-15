line: tools and channel
spec: --send-brief runs as a step of
  .github/workflows/ledger-install-supervisor-task.yml (line 683) on
  the self-hosted runner, keyed on today in UTC, with a one-day
  recovery since queue 291. A brief that misses its day by more than
  one run of that step is unsendable from anywhere in the tree: the
  remedy the dossier prints, --send-brief <day> from his PC, has no
  caller (the day argument is parsed at telegram-bot.py 3616 to 3618
  and nothing passes one). The 12th is that case: sixty-one hours
  with no run, no brief on the 13th to recover from, and it stays in
  BRIEFS WRITTEN AND NEVER SENT until somebody types the command on
  his machine. Add a workflow_dispatch input to the EXISTING step, a
  day, empty by default, passed as the day argument the sender
  already takes. No second sender, no new step, no new instrument.
  The outbox brief register is retired (291) and is not the answer:
  it carries no buttons and its record is zero catches and two
  duplicates.
acceptance: a dispatch with the input set to a day whose brief is
  unsent produces exactly one receipt for that day with buttons=2/2;
  a second dispatch for the same day prints ALREADY SENT and sends
  nothing; both watched on the live path, accepting first. Whether
  the 12th's brief itself goes is the Producer's call, not this
  item's.
max_sessions: 1
status: READY 2026-09-15, filed by the ruling of 00:52Z. Not blocking.
