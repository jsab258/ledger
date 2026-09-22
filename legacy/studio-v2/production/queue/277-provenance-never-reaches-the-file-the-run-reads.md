line: instruments
spec: exposure_pin_provenance exists in the scene and never reaches the piece list
  Unreal actually reads, so the run prints expPinProvenance=nothing-declared while
  a pin is in force.
acceptance: the piece list carries the provenance string, ParseSpec reads it, and
  the run line prints the named value instead of nothing-declared, with the
  accepting case run on the live file first
max_sessions: 1
status: READY 2026-09-14, found by a builder applying the pin ruling and reported
  rather than silently patched.

  THE GAP, WITH ITS SITES. StreetVignettePieces.cs line 496 writes exposure_pin
  per condition and no root-level provenance, so production/specs/vignette-pieces.json
  has no such key; ParseSpec at VignetteSpec.h line 415 leaves
  ExposurePinProvenance at its default; and VignetteShot.cpp line 2326 therefore
  prints expPinProvenance=nothing-declared on the run line.

  WHY IT IS NOT BLOCKING TODAY, and why it is still filed. The 2026-09-14 pin
  ruling's clause (d) needs the provenance to check that the live value is the
  one the file names. The builder resolved it by reading the string from
  production/specs/vignette-scene.json beside the piece-list path given on argv,
  FAIL-CLOSED: no file or no key and clause (d) goes red naming what was
  missing. It also prints both readings on one line
  (pieceListDeclares=nothing-declared) rather than hiding the difference. So the
  guard works and says what it could not see, which is the correct shape for a
  gap rather than a cover for one.

  WHAT IT COSTS UNTIL FIXED. The verdict of the first Unreal run under the pin
  ruling will say nothing-declared while 25 of 27 conditions carry a pin. A
  later reader of that verdict cannot tell from the verdict alone which value
  was in force or where it came from, and this project's own record is full of
  cases where the value was on the line and the word beside it said otherwise.
  That is the exact failure the leak fix was for.

  WHY THE BUILDER DID NOT FIX IT. The ruling's section 8 names four files and
  the generator would be a fifth. It reported instead of widening its own brief,
  which is the behaviour to keep.

  NOT A NEW INSTRUMENT. This carries an existing string into an existing file
  read by an existing parser, so it sits inside the standing rule that no new
  instrument ships this month unless one is retired.
