# NOW

Where the game stands, 2026-09-22, at the end of the second sitting on his PC.

1. THE SAFEGUARD IS REAL NOW, AND WATCHED. The Unreal build had not run once
   since the studio was paused: the workflow's second step called a script
   that went to the archive with it, so five pushes in a row failed there and
   skipped the build. The script is back, the probe watches it, and a green
   run takes nine minutes. Then a line that does not compile was pushed ON
   PURPOSE: the build failed, the verdict step failed, the run went red. A
   push runs the checks and a failed build fails the run, both seen rather
   than assumed.
2. A MEMORY SURVIVES BEING SAVED AND RELOADED. The save format is the memory
   markdown, and the C++ port had only the writing half. Reading is ported
   and held by thirty-eight golden rows against the real C#. An outside
   reader compiled both engines and ran 45 identical inputs through them, and
   found four disagreements nothing would have caught - a space before a
   timestamp, NaN as an importance, the smallest integer as a day, and a
   non-breaking space after a heading. All four fixed.
3. RUMOURS IN FLIGHT DO NOT SURVIVE A RESTART YET, and that is the next
   piece. It needs the save's own JSON ported, which is its own few hours.
   Until it lands there is no witnessed-and-control pair and no regression
   from one, and nothing automated reads the crime verdict, so a run with a
   dead input path would still push green.
4. THE TERRACE'S GROUND FLOOR IS ACCEPTED. Two attempts, both looked at. The
   shopfront's four parts separate: three glazed lights with mullions, a
   frame, a transom across glass and door alike, a lighter stallriser, and a
   side door in its own paint. Still busy where the two doors meet, and the
   toplight does not separate from the glazing under it.
5. THREE CHECKS COULD ONLY PASS ON A MACHINE THAT NEVER BUILDS. Found in one
   afternoon and all fixed: the Core suite cut a fixture by a bare newline,
   the canon gate matched its exemptions with the wrong slash so canon.md
   screened itself, and the attribution sweep walked the Unreal build's own
   ignored output. All three were green in CI the whole time.
