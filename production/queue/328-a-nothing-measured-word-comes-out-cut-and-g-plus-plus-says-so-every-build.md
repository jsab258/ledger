line: instrument (FrameStats.h RigDeterminismLine)
spec: `RigDeterminismLine` writes the words
  "nothing-measured/the-first-frames-mean-luma-is-zero" into a 48-byte region.
  It is 51 bytes. g++ -Wall PRINTS THIS ON EVERY BUILD and has for at least as
  long as the batch that found it:

    FrameStats.h:1446:88: warning: 'nothing-measured/the-first-f...' directive
    output truncated writing 51 bytes into a region of size 48
    note: '__builtin_snprintf' output 52 bytes into a destination of size 48

  PRE-EXISTING, CONFIRMED BY COMPILING HEAD'S OWN COPY (the same warning at
  line 1003 there), so it is not queue 326's and 326 correctly left it alone
  under rule 11.

  WHY IT IS WORSE THAN AN ORDINARY TRUNCATION. The thing being cut is a
  NOTHING-MEASURED WORD. This project's whole instrument discipline rests on a
  never-ran case printing the words "nothing measured" so a zero cannot read
  as a clean result (rule 3b). A nothing-measured word that arrives truncated
  is the one string in the file that must never be ambiguous, arriving
  ambiguous, and it does so silently: no announcer, no cut marker, nothing in
  the emitted line to say it was shortened.

  AND THE COMPILER HAS BEEN SAYING SO THE WHOLE TIME, which is the second half
  of the finding. This is not a fault nobody could see. It is a fault printed
  in plain text on every single build, in a project whose own casebook records
  that -Wformat-truncation was invisible under -fsyntax-only and therefore
  went unread for weeks. It was read this time only because a builder
  compiling for another reason looked at what scrolled past.
acceptance: the string fits its region or the region fits the string, decided
  by PRINTING the length series for every shape RigDeterminismLine can build
  and sizing from it, never by adding bytes until the warning stops (rule 2);
  and the line gains the same self-announcing cut marker the light lines have,
  so a future overrun says so instead of ending mid-word. Both outcomes
  watched: the nothing-measured shape emitted whole and asserted character for
  character, and a planted overlong shape proven to announce. Additionally,
  and this is the durable half: a check that the four g++ test binaries build
  with ZERO -Wformat-truncation warnings, with the count printed beside its
  denominator, so the next one cannot hide in the scrollback. Under D45 a tool
  that measures the game: a test, no review, no ruling record.
max_sessions: 1
status: READY 2026-09-16, found by queue 326's builder while compiling for
  another reason and reported rather than absorbed. Behind 325's second half,
  queue A and 319, but ahead of anything cosmetic: it is three bytes of fix
  and a permanent guard against a whole class the casebook already knows
  about. Queue 310 is its sibling on the exposure-pin line and should be read
  beside it; 310 is a reachable cap, this is a live one.
