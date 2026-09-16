line: instrument (FrameStats.h MeasureLightDelta and the lightfloor line,
  VignetteShot.cpp the probe pass)
spec: Each lantern-lit shot renders a no-toggle CONTROL: the same scene
  photographed twice with nothing changed. Its purpose is to supply the floor
  a real light must beat. But nothing ever asks the control the one question
  it is uniquely able to answer, WHICH IS WHETHER ITS OWN TWO FRAMES AGREE. A
  control whose two renders differ more than the light being measured makes
  every read in that shot meaningless, and the shot still reports
  FLOOR-USABLE.
acceptance: the lightfloor line carries the control's own self-agreement as a
  number, named as a statistic; a shot whose control disagrees with itself by
  more than the surplus it is certifying reads NOT-USABLE rather than
  FLOOR-USABLE; and lightsAboveFloor's denominator excludes those shots the
  way it already excludes NO-READ ones
max_sessions: 1
status: READY 2026-09-16, filed from run 48's committed verdict.

  MEASURED, NOT INFERRED. Every control line in run 48, its two means and the
  gap between them, all 6 of 6:

      shot             ctlMeanOn   ctlMeanOff    gap      verdict it got
      vign_camA_night    0.09639     0.09643    0.00004   (usable)
      vign_camB_night    0.18893     0.02395    0.16498   FLOOR-USABLE
      pinset_night_1     0.00152     0.18486    0.18334   NO-READ
      pinset_night_2     0.16936     0.00152    0.16784   NO-READ
      pinset_night_3     0.17959     0.15386    0.02573   FLOOR-USABLE
      pinset_night_4     0.16938     0.16934    0.00004   FLOOR-USABLE

  TWO OF SIX CONTROLS AGREE WITH THEMSELVES. The two that do read 0.00004.
  The next value up is 0.02573, a factor of 640, so the bound has a printed
  gap under it rather than a chosen number.

  WHAT IT COSTS, on run 48's own numbers. lightsAboveFloor=17/28. Eight of the
  seventeen are queue 329's blank-off-frame fault. SIX MORE ARE THIS ONE, all
  in vign_camB_night, whose control disagrees with itself by 0.16498 while the
  surpluses it certifies are smaller than that:

      vign_camB_night  lantern0 lantern2 lantern3
      vign_camB_night  east_parade_interior0  interior2  interior5

  THREE OF THE SEVENTEEN SURVIVE BOTH FAULTS. They are pinset_night_4's three
  window practicals, and not one lantern anywhere. So the run's real reading is
  3 of 28, and the two faults together account for 14 of the 17.

  WHY THE SIGNED MEAN IS THE WRONG STATISTIC FOR THIS, and the instrument
  already prints the right one beside it. lightFloorCtrlMeanFull is a SIGNED
  mean over the frame, so two renders can differ everywhere and still cancel
  to nothing. pinset_night_4's control reads gap 0.00004 and in the same line
  lightFloorCtrlMovedAtLeast=155931/... of 921600: 16.9 per cent of its pixels
  moved between two renders of an identical scene. The gap is the right
  screen for a gross failure and the MOVED histogram is the right one for the
  noise floor, and a shot needs both. Say which each is.

  NOT THE SAME ITEM AS 329, and neither subsumes the other. 329 is a light
  frame that failed to render. This is a control that is not trusted to be a
  control. Run 48 shows both, in different shots, and either alone would still
  leave a false number in the channel.

  UNDER D45 this is a tool that measures the game: a test, no review, no
  ruling record.

  RULED 2026-09-16 (06:35Z ruling, section 2): both statistics, each for
  its own question. The signed gap (lightFloorCtrlMeanFull) is the
  exposure-state screen; the MOVED histogram stays the per-edge floor.
  The screen is RELATIVE, from this item's own sentence, and no absolute
  bound is set: a light whose mean fell below minus the control's absolute
  gap reads EXPOSURE-SWUNG; a light whose rise over the gap does not
  exceed the gap reads VOID-CONTROL; the rest are MEASURED and take the
  326 edge test; a shot that certified nothing reads NOT-USABLE. Every
  bucket prints beside lightsProbed. Run 48's 48 lines are the fixtures:
  measured 3/42, lanterns 0/24, buckets 14/8/7/10. The 0.001 proposed
  above is withdrawn; the column keeps printing.
