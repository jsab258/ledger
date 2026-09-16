line: instrument (FrameStats.h MeasureLightDelta and LightProbeDoneLine,
  VignetteShot.cpp the probe pass)
spec: THE LIGHT PROBE'S OWN CONTROL SAYS ITS READINGS ARE NOT READINGS, AND
  NOTHING PAIRS THEM. control_no_toggle toggles nothing, so its delta IS the
  floor. Run 47 at vign_camA_night, read off the committed verdict:

    light control_no_toggle          deltaMeanFull=0.25060
    light lantern0                   deltaMeanFull=0.00010
    light lantern1                   deltaMeanFull=0.25060
    light lantern2                   deltaMeanFull=0.25060
    light lantern3                   deltaMeanFull=0.25060
    light east_parade_interior0      deltaMeanFull=0.14893
    light east_parade_interior2      deltaMeanFull=0.15494
    light east_parade_interior5      deltaMeanFull=0.25060

  Four of the eight read the control's number TO FIVE DECIMALS. A probe that
  changed nothing moved the frame as much as turning a lantern off did, so
  those four deltas carry no information about their lights at all.

  AND THE DONE LINE IS BUILT ON A THRESHOLD THE CONTROL CLEARS TRIVIALLY.
  lightsReachedFrame is computed from D.RoseAtLeast[0] > 0, one pixel rising
  by one code value. A control moving a quarter of the luma range satisfies
  that, so lightsReachedFrame=30/42 on run 47 and 36/42 on run 46 are counts
  standing on a floor that swamps them. THE HEADER'S OWN COMMENT PREDICTED
  THIS: "the control line beside it is what says whether that edge means
  anything in this run". The control was built. Nothing reads it.

  THE CONTROL IS NOT ALWAYS LARGE, which is what makes the unpaired reading
  dangerous rather than merely noisy. deltaMeanFull for control_no_toggle by
  shot: run 47 camA +0.25060, camB -0.00003, pinset_1 +0.09596, pinset_2
  -0.37873, pinset_3 -0.00000, pinset_4 -0.00925; run 46 +0.03179, -0.00001,
  +0.00054, +0.01632, -0.06091, -0.03060. Some shots have a usable floor and
  some do not, and today the done line cannot tell them apart. Several lights
  also read BRIGHTER with the light off (lantern0 at camB_night, -0.16492).

  TWO CANDIDATES, NEITHER MEASURED HERE AND NEITHER EXCLUDED. All six probed
  shots run shotExposurePin=AUTO with shotExposurePinRead=0.0300/8.0000, and
  the probe's own deltaPixelsDarkerWithLightOn flag, whose rule is
  auto-exposure-suspected-if-large, is already firing at 332097/921600. And
  the off-frame means cluster at 0.00151 and 0.00152, the same value as queue
  325's BLANK shots' shotMeanLuma=0.0015, so the blank-frame fault may be
  landing in probe frames too. The light lines carry NO exposure key, so a
  reader cannot tell which it is.
acceptance: lightsReachedFrame is decided against control_no_toggle's own
  distribution for THAT shot rather than against a fixed one-code-value edge,
  and a shot whose control exceeds its lights reports NO-READ with both
  numbers rather than a count; the light line carries the exposure pin state
  it was taken under; and the done line separates shots with a usable floor
  from shots without, with both counts. Both outcomes watched: a planted probe
  whose control is larger than every light must report NO-READ, and a run with
  a quiet control must still count. Under D45 this is a tool that measures the
  game: a test, no review, no ruling record.
max_sessions: 1
status: READY 2026-09-16, found by the builder sent to do queue 319, while
  checking 319's premise rather than while looking for this. It outranks 319's
  surviving clause: 319 adds a reading nobody has, this one says an existing
  reading is not trustworthy, and a false green is worse than a blank. Sits
  with 325 and 324 ahead of the dusk frame.
