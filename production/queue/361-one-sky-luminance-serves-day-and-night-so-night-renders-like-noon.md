line: engine (VignetteShot.cpp kSkyLuminance and the dome's material instance;
  production/specs/vignette-scene.json's per-condition sky fields)
spec: run 50 bound the approved photograph as the sky and it WORKS: all four
  flags read, skyDomeMatIsSky=yes, and the photograph is what lights the
  street. IT ALSO MADE THE NIGHT FRAMES RENDER LIKE DAY, and the cause is one
  constant.

  MEASURED, same file, same ruler, one pass over both versions of
  ue-pinset_night_3.png:

      run 49 (lamps lit, no dome)   meanLuma= 43.6  maxLuma=250.6
      run 50 (dome bound)           meanLuma=142.9  maxLuma=255.0

  3.3 times brighter on a NIGHT condition. The sky band is blown white and the
  sodium lamps, which run 49 had just made the brightest warm thing in their
  own neighbourhood, are barely visible against it.

  THE CAUSE, READ IN THE CODE RATHER THAN INFERRED FROM THE PICTURE:
  `kSkyLuminance = 1.0f` at VignetteShot.cpp:384 is a GLOBAL CONSTANT, written
  into the dome's material instance once at build (:4582) and never again. It
  is not a condition field and nothing re-drives it.

  AND THE SCENE ALREADY CARRIES THE FIELD THAT SHOULD DRIVE IT. `sky_intensity`
  is per-condition (overcast_day 0.70, wet_night and pin_setter_night 0.35) and
  IS driven, but only into the SkyLight component at :2217. An unlit emissive
  surface renders at its own value regardless of any light in the scene, so the
  SkyLight's 0.35 scales what the capture contributes and does NOTHING to what
  the camera directly sees. The dome is at 1.0 in every condition.
acceptance: the dome's luminance is driven PER CONDITION through a write-on
  -change guard, on the precedent of ReDriveWetness and ReDriveLampEmissive
  which already do exactly this two and one condition-fields over; the value
  and the condition it came from are read back on the scene line; and a night
  row's meanLuma returns to the order of run 49's 43.6 while THE 10 ROWS WHOSE
  sky_intensity IS 1.00 ARE UNMOVED, the dome being 1.00 times a gain of 1.0
  there exactly as before, and every other row moves in proportion to its own
  sky_intensity; A MOVED 1.00 ROW IS A FAULT ELSEWHERE.

  (CORRECTED 2026-09-16 under D43, and the correction is the RESIDENT'S OWN
  ERROR rather than a builder's. This line read "while the day rows are
  unmoved", which asked for two incompatible things: holding day still while
  moving night needs the per-condition dome field the brief forbade. Counted
  rather than assumed: 33 conditions carry FOUR values of sky_intensity, 1.00
  on 10 rows, 0.70 on 13, 0.50 on 4 and 0.35 on 6, of which only 2 are night.
  So 21 of the 31 day rows move, each by its own value, and the 10 at 1.00 are
  THE CHANGE'S OWN NULL CONTROL, which did not exist as a concept when the
  line was written.) WHICHEVER FIELD DRIVES IT, the first value is a FIRST VALUE OF A
  SERIES and says so, exactly as kLampEmissiveUnitless does
max_sessions: 1
status: READY 2026-09-16, produced by run 50 and filed under Jafar's standing
  rule: a finding is filed and the standing order resumes.

  DO NOT READ THIS AS THE SKY HAVING BEEN A MISTAKE. The photograph binding is
  correct and the run proves every part of it: skyHdriBytes=2224812 where run
  49 read 0, skyHdriBoundAs names the mesh and the diameter and reports
  writes=15-on-change over photos=2, and all four reflection reads resolved on
  their first candidate spelling. The ambient moving was PREDICTED and RULED
  ACCEPTED before the run. What nobody sized was how far it would move, and
  the reason is one constant serving two times of day.

  THE LAMP DID NOT REGRESS AND THIS ITEM MUST NOT BE USED TO CLAIM IT DID.
  Night rows still read 2 to 3 lanterns lit, unchanged from run 49 at 9 rows
  with two or more. The DAY false positives fell from about 20 rows to 4,
  because a brighter and more uniform ambient stops a lamp head beating its
  ring by one byte of noise. Queue 358 is still the item for that test's
  missing margin; this run made its symptom rarer without fixing it.

  ONE THING NOT TO DO: do not reach for the SkyLight's intensity to fix this.
  It is already per-condition and already correct at 0.35; it governs the
  captured contribution and not the emissive surface the camera sees. Changing
  it would darken the lighting while leaving the blown sky exactly as it is.

## ANSWERED BY RUN 51, 2026-09-16, evidence commit 73c902b5

THE DRIVE FIRED: skyLumDriveAsked=4656/walked=32/skipped=4624,
skyLumDriveWrote=32/ofWalks=32/noInstance=0, readback set=0.700/got=0.700/
same=yes. Not one dead write.

THE BRACKET, on the exposure-pinned night frame, each number from its own
named evidence commit rather than from a filename:

    run 49  e1b4de77  no dome            meanLuma= 43.6   (floor)
    run 50  654dd381  dome at 1.0        meanLuma=142.9   (ceiling)
    run 51  73c902b5  dome per condition meanLuma= 47.4

INSIDE THE BRACKET AND ABOVE THE FLOOR, which is the right direction: the night
now has a sky that contributes a little light rather than none or noon. It did
NOT overshoot, so the double-coupling worry (dome 0.35 as the captured surface
AND SkyLight 0.35 scaling that capture, possibly compounding) did not bite at
this value. That is one point, not a curve.

THE NULL CONTROL HELD, and it is the strongest thing in this reading because
nobody designed it. Run 50 to run 51, whole-frame meanLuma:

    sky_intensity=1.000  ue-vign_fog_maxop0000.png       142.5 -> 142.5  (+0.1)
    sky_intensity=0.700  ue-vign_camB_day.png            115.4 -> 106.4  (-8.9)
    sky_intensity=0.500  ue-vign_grid_sky050_sun030.png  178.0 -> 171.7  (-6.3)

The 10 rows at 1.00 did not move. Everything else did. The change touched
exactly what it should.

WHAT THIS READING DOES NOT CLAIM: that 0.500 falling LESS than 0.700 means
anything. Those are different scenes with different amounts of sky in frame, so
whole-frame means are not comparable across conditions, and the ordering the
ruling predicted cannot be tested this way. A per-band reading grouped by
shotSkyIntensityRead is what would test it.

AND ONE ERROR CAUGHT BY TWO NUMBERS BEING IDENTICAL: the first bracket read
43.6 for BOTH run 49 and run 50, because the run 50 frame was pulled from
727d6a46, which is the commit that DISPATCHED run 51 rather than the one
carrying run 50's evidence. Run 50's frames landed later, in 654dd381. Two
identical numbers are the instrument-suspect signal (rule 3) and it fired
correctly.
