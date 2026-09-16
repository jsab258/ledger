line: instruments (production/specs/vignette-scene.json shot order; reading
  for production/queue/276-settled-night-exposure-reference.md)
spec: Queue 276 step 1 asks for one held night condition rendered REPEATEDLY
  at one camera with the per-frame output luma printed until it stops moving.
  Four rows named pinset_night_1 to _4 now exist at one camera under one held
  night condition, and it is easy to read them as that series. THEY ARE NOT.
  They sit at shot indices 30, 33, 36 and 39, with two pin-rung shots between
  every pair, and the shot immediately before each of them is a PINNED day
  frame. Four renders each preceded by a different pinned exposure is a
  leak-detection interleave, which is what a setter row is for, and it cannot
  answer whether a night condition settles.
acceptance: 276 step 1 is run as consecutive rows of the one condition with
  nothing between them, the per-frame series printed, and the settling count
  and settled level named as last-wins; or, if that ordering cannot be had,
  the item says so and says what it would take
max_sessions: 1
status: READY 2026-09-16, filed so the wrong series is not adopted as the right one.

  THE FOUR ROWS AND WHAT SITS BETWEEN THEM, read off the spec:

      30  pinset_night_1            pin_setter_night
      31  vign_pin_003_afternight   pin_003    exposure_pin 0.03
      32  vign_pin_003_afterday     pin_003    exposure_pin 0.03
      33  pinset_night_2            pin_setter_night
      34  vign_pin_030_afternight   pin_030    exposure_pin 0.3
      35  vign_pin_030_afterday     pin_030    exposure_pin 0.3
      36  pinset_night_3            pin_setter_night
      37  vign_pin_300_afternight   pin_300    exposure_pin 3.0
      38  vign_pin_300_afterday     pin_300    exposure_pin 3.0
      39  pinset_night_4            pin_setter_night

  THEIR OWN LUMA, off the committed shot lines, shotMeanLuma, which is the
  frame on disk and not a re-render:

      pinset_night_1   0.0015   status=BLANK  shotBlank=yes
      pinset_night_2   0.1694   WROTE
      pinset_night_3   0.1796   WROTE
      pinset_night_4   0.1694   WROTE

  READ AS A SETTLING SERIES THIS SAYS NOTHING, and saying it says nothing is
  the finding. One frame is blank. The other three do not converge: 2 and 4
  agree to four decimals and 3 sits 6 per cent above both, and each of the
  three follows a different pinned exposure. A series whose every sample has a
  different predecessor measures its predecessors.

  ALL FOUR READ shotExposurePin=AUTO with shotExposurePinAsked=0.0000 and the
  engine's own clamp range 0.0300/8.0000, exactly as the 2026-09-10 ruling
  requires until 276 step 3 lands. Nothing here asks for that to change, and
  the forbidden derivation stays forbidden: no night pin is to be computed
  from a day pin by any ratio.

  WHAT 276 STEP 2 ALREADY ENTITLES US TO SAY, and it is worth saying now
  because it outranks the pin by that item's own words: on the evidence that
  exists, the night condition has NOT been shown to settle. That is not yet
  the finding step 2 wants, because this is not yet the series step 1 wants.
