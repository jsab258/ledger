line: tools (the record), process
spec: production/NOW.md is 34,838 WORDS in 75 dated blocks, and the hourly
  INBOX AND RESUME trigger's step 4 says to read it FIRST, before the queue,
  because "it says what is already moving, which is the thing a fresh wake
  would otherwise duplicate or abandon". A fresh session cannot do that. It
  reads the top block and stops, which means the instruction is discharged by
  luck rather than by design: the newest block happens to be at the top.

  THIS IS THE FAULT THE PROJECT HAS ALREADY FIXED ONCE, in the file with the
  strongest claim to being read. CLAUDE.md went from 16,291 words to 1,990 on
  2026-09-01 under task production/queue/013, on the reasoning that "a
  document nobody holds in their head is a document nobody reads", and nothing
  was deleted: 1,316 lines moved into casebooks with a checker proving every
  moved line present. NOW.md is 34,838 words, which is more than twice what
  CLAUDE.md was when it was cut, and it is named in a wake prompt as the FIRST
  thing to read.

  AND THE FILE SAYS IT ABOUT ITSELF, at line 9: "Keep it current or delete it.
  A stale NOW is worse than none, because it looks like a live state." 74 of
  its 75 blocks describe states that are over.

  WHAT IS NOT CLAIMED: that anything in it is wrong. The blocks were true when
  written and several record sequences with their instants that would be
  unreconstructible otherwise (the 19:20Z hold and its 19:42:59Z lift is one).
  This is a placement fault, not a truth fault, and the remedy is the 013
  remedy: move, do not delete, and prove the move.

  ONE THING TO CHECK BEFORE ACTING, because it decides the shape: the
  publish-glance workflow's own comment says "NOW.md is no longer read by any
  generator, so it is no longer a trigger", and production/next-three.json
  replaced it as the map's source. Confirm that by grep rather than by quoting
  the comment, since a comment is not evidence. If it holds, NOTHING MACHINE
  READS THIS FILE and the only reader is a session or a human, which makes the
  cut cheap and the argument for it stronger.
acceptance: NOW.md holds only what is ACTUALLY MOVING, with every retired
  block moved intact to a log under production/ and a checker proving each
  moved line present in the destination by reading the original OUT OF GIT
  rather than off disk, which is the mechanism task 013 used. The word count
  prints so it cannot quietly grow back, the way ledger/verify.py prints
  CLAUDE.md's. Both outcomes watched: the checker must go red on a planted
  missing line, tested before it is trusted.
max_sessions: 1
status: READY 2026-09-15, found by trying to follow the wake trigger's own
  step 4 and discovering the instruction is not executable as written. Not
  urgent and not ahead of anything Jafar asked for; it is filed because the
  next session will hit it too and will also work around it silently.
