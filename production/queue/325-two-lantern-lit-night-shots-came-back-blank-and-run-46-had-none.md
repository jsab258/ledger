line: engine (VignetteShot.cpp capture path), art (the visual bar)
spec: RUN 47 WROTE 41 OF 43 SHOTS AND RUN 46 WROTE 43 OF 43. The two that did
  not are pinset_night_2 and pinset_night_3, both camera cam_hook, both
  condition pin_setter_night. Measured off the committed verdict, not
  inferred:

    run 46 (c7f2cc01)   status=WROTE 43   status=BLANK 0
    run 47 (bf6fc61a)   status=WROTE 41   status=BLANK 2

    the blank shot        shotMeanLuma=0.0015  shotNonBlackPct=17.73
    its working sibling   shotMeanLuma=0.2439  shotNonBlackPct=100.00
      (pinset_night_1, SAME condition, SAME wetness, SAME capture path)

  IT IS NOT A WETNESS FAULT AND THE INSTRUMENT SAYS SO. Both blank rows carry
  shotWetness=0.9000, shotWetnessOnPieces=0.9000 and shotWetnessAgrees=yes, so
  the per-condition re-drive reached those frames; what failed is the picture,
  not the parameter. The done line agrees: wetnessRedriveWrote=10030/of=10370
  with every refusal bucket but notOurRoute at zero.

  AND IT IS TWO OF THE FOUR SHOTS AT ONE CONDITION, not all four.
  pinset_night_1 and pinset_night_4 wrote normally. A condition that was
  simply wrong would take all four. That pattern, plus shotNonBlackPct at
  17.73 rather than 0.00, says a PARTIAL frame rather than a failed capture:
  something was on screen and most of it was not.

  WHAT IS NOT DIAGNOSED AND MUST NOT BE GUESSED. Run 47 is the first run
  carrying the new 2K pack, and the pack's files grew a lot on the surfaces it
  replaced (kerb.jpg 1.15MB to 5.86MB, metal_n.jpg 1.57MB to 8.36MB). A
  longer stream before a dark night shot is A PLAUSIBLE STORY AND NOT A
  READING, and this item records it as the first thing to test rather than as
  the cause. The other candidates, neither excluded: the wetness re-drive at
  0.9 costs writes on a night condition that the day conditions do not, and
  the capture path was already noted as adopting run-wide once candidate A
  fails once (shotCaptureViaStat), which is a per-run adoption this item has
  not read the history of.

  WHY IT MATTERS NOW RATHER THAN EVENTUALLY. pin_setter_night is ONE OF ONLY
  TWO CONDITIONS IN THE SPEC THAT LIGHT THE LANTERNS (the other is wet_night;
  33 conditions carry the field and 2 set it true). Jafar's dusk frame is
  "lamps lit, wet road, a figure in silhouette. That is the picture I judge
  by." So the shots that failed are the exact family that frame belongs to,
  and a frame that renders black half the time is not a frame anybody can
  judge.
acceptance: the cause is NAMED with the measurement that names it, not with a
  story; the fix is shown by a run in which all 43 shots write, with the
  blank count printed beside its denominator so a zero cannot read as
  nothing-measured; and the rejecting case is watched, meaning a run that
  still blanks must report BLANK and not silently carry the previous run's
  file forward under its own name (ci.md). If the cause is streaming, the
  instrument gains whatever key distinguishes "the frame was not ready" from
  "the frame was black", because today shotBlank=yes cannot tell those apart.
max_sessions: 1
status: READY 2026-09-16, found by reading run 47's shot statuses against run
  46's rather than by looking for it. AHEAD OF THE DUSK FRAME, with 319 and
  324, because all three are about whether a lantern-lit night frame can be
  trusted. Under D41 the frame itself is ungated; this is not a look, it is a
  frame that does not exist, so it keeps its review.
