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

QUANTIFIED ON RUN 48, 2026-09-16, and the fault is live rather than historical.
Queue 326's floor shipped and its first real run reads lightsAboveFloor=17/28
over 4 usable shots of 6. EIGHT OF THOSE SEVENTEEN READS ARE THIS FAULT:

    shot             light                    meanOffFull   counted as
    vign_camA_night  lantern2                   0.00075       YES
    vign_camA_night  lantern3                   0.00075       YES
    vign_camA_night  east_parade_interior2      0.00075       YES
    pinset_night_3   east_parade_interior2      0.00152       YES
    pinset_night_3   east_parade_interior5      0.00152       YES
    pinset_night_4   lantern0                   0.00152       YES
    pinset_night_4   lantern1                   0.00152       YES
    pinset_night_4   lantern2                   0.00152       YES

  CORRECTED 06:40Z FROM FIVE TO EIGHT, and the correction is itself the lesson.
  The first count filtered on the literal string 0.00152, which is the black
  level the pinset camera writes. camA_night writes its blanks at 0.00075, a
  different number for the same condition, and three reads were missed by
  matching a VALUE where the test is a THRESHOLD. There is no value in the
  whole 48-line series between 0.00152 and 0.02392, a factor of 15.7, so the
  threshold has a printed gap under it rather than a guess.

  So the true count is at most 9 of 28, and 17/28 must not be quoted until this
  lands. AT MOST, because a second and separate fault removes six more: see
  queue 332, which this item does not cover and must not be assumed to.

  AND THE FLOOR CAUGHT THE OTHER HALF, which is worth recording because it says
  the design is right and only incomplete: pinset_night_2's CONTROL itself came
  back at meanOffFull=0.00152, and that shot correctly reads NO-READ. A blank
  control is caught; a blank light frame under a good control is not. Exactly
  the asymmetry this item was filed for, now with both sides observed in one
  run.
