line: instrument (FrameStats.h MeasureLightDelta and the probe walk,
  VignetteShot.cpp the probe pass)
spec: The probe measures a light by photographing the frame with that light
  OFF and diffing. A frame that failed to render is also dark, and the
  instrument cannot tell those apart, so A BROKEN CAPTURE SCORES AS AN
  ENORMOUS CONTRIBUTION. Queue 326's new floor catches a blank CONTROL, which
  is why vign_camA_night correctly reads NO-READ, and it is BLIND to a blank
  LIGHT frame under a good control.

  FOUR OF THE SIX READS THAT SURVIVE 326's FLOOR ARE THIS FAULT, measured off
  run 47's committed verdict:

    shot             light                  meanOnFull   meanOffFull
    pinset_night_1   east_parade_interior0    0.24388       0.00152
    pinset_night_1   east_parade_interior2    0.24388       0.00152
    pinset_night_4   lantern2                 0.19480       0.00151
    pinset_night_4   east_parade_interior0    0.19480       0.00152

  0.0015 is queue 325's BLANK signature (its two blank shots read
  shotMeanLuma=0.0015). The pairs also carry pairwise identical histograms,
  which is the same tell that condemned the camA control. So the numerator
  326 ships is not yet a number to report, and this item is what makes it one.

  THE RULE, and it uses the shot line's OWN structural test rather than a new
  threshold: run FrameStats::Measure on every decoded probe frame, control
  included, and a frame whose structural Blank is true (one colour bucket, or
  no non-black pixel) is NEVER handed to MeasureLightDelta. No signature
  threshold, nothing keyed on 0.0015, because a number chosen from four
  samples is the fault this project names in rule 2.
acceptance: a blank probe frame's light line prints
  lightStatus=BLANK-PROBE-FRAME carrying that frame's shotMeanLuma,
  shotDistinctBuckets and shotNonBlackPixels as PixelLine prints them; a blank
  CONTROL makes the shot NO-CONTROL with the words blank-control-frame on its
  floor line; the done line prints lightProbesBlank=k over frames decoded, so
  a zero ships its denominator. BOTH OUTCOMES: a planted single-bucket Off
  buffer is refused and counted, and a planted TWO-bucket near-black Off
  buffer is MEASURED and not refused, which is the accepting case and stops
  the guard becoming a ratchet that eats every dark night frame. Under D45 a
  tool that measures the game: a test, no review, no ruling record.
max_sessions: 1
status: READY 2026-09-16, filed by the 22:25Z ruling's section 10 as item A.
  ORDERED BEHIND THE CARRYING RUN and ahead of 319. It may be the same fault
  as queue 325's second half; the ruling says A is still owed as an instrument
  even if it is, because 325 asks why frames blank and this asks that a blank
  frame never be read as a measurement.
