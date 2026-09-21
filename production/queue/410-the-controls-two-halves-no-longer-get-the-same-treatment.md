line: instruments (the control stopped being the same picture twice)
spec: FOUND BY THE RESIDENT 2026-09-21 READING RUN 55, and it is the instrument
  half of queue 384's landing.

  A `control_no_toggle` line exists to be THE SAME PICTURE TWICE: its own
  comment at the `BeginNextProbe` sequence -1 says "the same camera, the same
  condition, the same frame counts and NOTHING TOGGLED", and its delta is the
  run's own noise floor, which is why no epsilon had to be invented for "did
  this light reach a pixel".

  IT IS NO LONGER THAT, as of the settle loop landing. Read in
  `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp`, `AfterFrame`: the
  `if (GRepeating)` branch calls `SettleRecordTake` and returns to Warm for
  another take, so THE RIG REPEAT SETTLES. The `if (GProbing)` branch goes
  straight to `MeasureProbe` with no settle at all, so THE PROBE AND CONTROL
  RE-RENDER DOES NOT. The reference half is the committed frame, which settles.

  SO THE CONTROL NOW DIFFERENCES A SETTLED FRAME AGAINST AN UNSETTLED ONE and
  its delta measures the gap between two regimes rather than instability. Run
  55 reads 0 of 12 controls within 0.005 while the rig repeat reads 2 of 2
  within bound at a worst of 0.00061. Both are correct about different things.

  THE PROBE HALF IS DEMONSTRABLY UNSTABLE, measured run 54 against run 55 over
  the same twelve shots: `meanOffFull` moved by more than 0.005 on 4 OF 12,
  three of them by about 0.455, flipping between roughly 0.00639 and 0.46178.
  Those two values recur EXACTLY across different shots and different runs,
  which is the signature of a clamp rather than of a measurement.

  WHY IT MATTERS BEYOND TIDINESS: the light floor is built on the control being
  the noise floor. If the control's delta now carries a settle gap, then every
  "did this light reach a pixel" verdict derived from it carries that gap too,
  and the lamp and lantern readings in queue 332 and queue 361 rest on it.
acceptance: either the probe and control re-render runs the settle loop the way
  the shot and the repeat do, and the twelve control deltas are then read again
  and printed as a series; or the line stops being called a control and its key
  says in words what two things it differences, with every consumer of the
  light floor named and checked against the change. Whichever is chosen, the
  twelve deltas are printed BEFORE and AFTER so the change is a measurement and
  not an assertion
max_sessions: 2
status: READY 2026-09-21. Studio instrument work under D45, so a test and no
  review and no ruling record.

  DO NOT "FIX" THIS BY LOOSENING ANYTHING. The rig repeat's zero epsilon for
  IDENTICAL and the 0.005 settle bound both landed this morning and are proven
  by run 55; neither is to be touched to make a control line read better.

  RELATED AND NOT THE SAME: two of the four CAP-BIT night shots in run 55 are
  BISTABLE rather than slow, alternating between a clamp and a mid value
  (0.00637..0.18295..0.00637..0.19985). No cap size fixes those, and why they
  alternate is unknown. That is filed with this item because the clamp values
  are the same two numbers, so the two faults may share a cause.
