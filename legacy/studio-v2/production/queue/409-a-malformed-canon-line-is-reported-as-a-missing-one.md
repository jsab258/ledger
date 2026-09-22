line: instruments (a guard that cannot tell absence from malformation)
spec: FOUND BY THE RESIDENT 2026-09-21 WHILE IT COST HIM THE DETOUR IT
  DESCRIBES, and filed rather than chased per CLAUDE.md rule 11.

  `tools/canon-register-check.py` refused four records with:

      A3 D49 date=2026-09-21 VIOLATION=no-CANON:-line-on-a-record-dated-
      2026-09-16-or-later

  ALL FOUR RECORDS CARRIED A `CANON:` LINE. What they did not carry was the
  machine vocabulary. `DIRECTIVE_RE` at line 106 is
  `^CANON:\s*(none|edits\s+\S.*)$`, so the directive is EXACTLY `none` or
  `edits <something>` and nothing else, and all four had written prose after
  the keyword: "none. D18's content rule is unchanged", "none changed. D19
  ...", and one that opened with a citation of canon.md instead.

  SO THE MESSAGE STATES A FALSITY WITH A RECORD NAME ON IT. "No CANON: line"
  and "a CANON: line this parser cannot read" are different facts with
  different fixes, and the tool printed the first while the second was true.
  The resident read the message, believed it, and went looking for four
  missing lines that were all present. The correct reading came from opening
  the regex, which is rule 3: suspect the instrument first.

  IT IS THE SHAPE THIS PROJECT ALREADY NAMES. A guard that cannot tell nothing
  from malformed is the same family as a zero with no denominator: both report
  a clean absence where the truth is an unread presence.
acceptance: a record whose `CANON:` line is absent and a record whose `CANON:`
  line is present but unparseable produce DIFFERENT messages, each naming what
  it actually found, and the malformed case QUOTES the line it could not read
  so the writer can see the gap between what they wrote and the vocabulary;
  both cases are in the selftest with the accepting case first, and the
  vocabulary itself is printed by the tool so a writer can learn it without
  opening the regex
max_sessions: 1
status: READY 2026-09-21, FILED AND NOT STARTED. Studio work under D45, so no
  director and no ruling record when it is taken. It sits in the studio's third
  behind the visual slice, the measurements and the art lane, per his order.

  THE FOUR RECORDS ARE ALREADY CONFORMANT: the resident reformatted D49, D53,
  D56 and D58 to `CANON: none` with every word of their prose preserved on the
  lines below, and the checker now reads PASS assertionsHeld=3/3 violations=0
  with missingCANONline=0 of 13 records dated 2026-09-16 or later. So this item
  is about the INSTRUMENT and there is no content left to fix.
