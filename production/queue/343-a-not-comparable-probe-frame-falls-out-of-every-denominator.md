line: instrument (VignetteShot.cpp MeasureProbe, the three failure paths;
  FrameStats.h LightProbeDoneLine)
spec: MeasureProbe has three ways to fail before a light is ever differenced.
  Two of them count. NO-FILE increments GProbeNoFile, UNDECODABLE increments
  GProbeNoFile, and NOT-COMPARABLE INCREMENTS NOTHING AND RETURNS. A light on
  that path is inside lightsProbed and inside no failure counter, so it is
  neither measured nor accounted for: it simply is not there. Every percentage
  on the done line is over a denominator that quietly excludes it.
acceptance: the third path carries its own counter, named for what it is, and
  the done line's arithmetic is printed so the buckets and the failures sum to
  lightsProbed with nothing falling between them
max_sessions: 1
status: READY 2026-09-16, found by the 329/332/337 builder and left unfixed on
  purpose to keep that diff reviewable, which was the right call.

  READ IN THE SOURCE, VignetteShot.cpp 3327 to 3350, the three paths in order:

      !bHaveFile            ++GProbeNoFile   EmitLightLine "NO-FILE"        return
      !DecodeBgra(...)      ++GProbeNoFile   EmitLightLine "UNDECODABLE"    return
      size mismatch or
      reference gone        (nothing)        EmitLightLine "NOT-COMPARABLE" return

  The line IS emitted, so the fault is visible to anyone reading all 48 light
  lines by hand. It is invisible to anyone reading the done line, which is the
  line the studio actually quotes.

  IT DID NOT FIRE ON RUN 48, and that is the whole reason it is worth filing
  now rather than after it does. A path that has never fired is a path whose
  absence from the totals nobody has had cause to notice, and the run that
  first exercises it is the run whose numbers will be quietly wrong. This is
  the same shape as queue 329 and 332: not a wrong number, a number whose
  denominator does not cover the case.

  WHAT IT WOULD TAKE: one counter and one key, plus the printed arithmetic on
  the done line so a future gap of this kind shows up as a sum that does not
  close rather than as a silence. Queue 330 already asks the done line to
  account for itself, so this may be one item rather than two; whoever takes
  330 should read this first.

  UNDER D45 a tool that measures the game: a test, no review.
