line: instrument (VignetteSpec.h NullSeriesLine and AppliedFieldsUnreal)
spec: The run's noise floor is read off THE LARGEST set of measured frames
  sharing one applied-field fingerprint. The fingerprint carries field VALUES
  and no condition id, and queue 334 adds six night rows at one camera. Those
  six join the four pinset_night rows into a group of TEN, which overtakes the
  day group of SEVEN that the floor has been read off until now. So landing 334
  as ruled would silently move the floor every grid cell is quoted against from
  a day group onto a night group, and 334 exists precisely because nobody knows
  whether that night condition is stable.
acceptance: the null group's choice is not size alone, or the line says which
  group it took and what else was available with both spreads, so a reader can
  see the floor move rather than inherit it
max_sessions: 1
status: READY 2026-09-16, found by the 334 builder and re-checked line by line
  by the resident before being written down.

  THE THREE FACTS, EACH READ IN THE SOURCE:

  1. VignetteSpec.h:2624 AppliedFieldsUnreal formats
     sun/sunI/skyI/hdri/fog/fogMaxOp/lant/prac/expPin/wet. THERE IS NO
     CONDITION ID IN IT. Two differently named conditions with the same field
     values are one group.

  2. wet_night and pin_setter_night differ in EXACTLY TWO of thirteen fields,
     id and note. The eleven that decide the fingerprint are identical:
     exposure_pin, fog_density, fog_max_opacity, hdri, hdri_bom, lanterns,
     sky_intensity, sun, sun_intensity, wetness, window_practicals.

  3. VignetteSpec.h:2696 NullSeriesLine, its own comment: "THE GROUP: the
     largest set of measured frames sharing one applied fingerprint. Largest,
     because the noise floor is read off the widest set of frames the run
     renders identically."

  WHAT IT COSTS, measured off run 48's committed verdict by the 334 builder and
  not estimated. The verdict would stay CLEAR, so this does not block the batch:

      day group now      nullSpreadMeanLuma 0.0001  vs skyStep 0.0193   193x
      night group then   spread 0.0102              vs skyStep 0.0193   1.9x
      GroundP05          0.0007..0.0028             vs step 0.0304      43x..10.9x
      GroundP50          0.0000..0.0047             vs step 0.0345      unbounded..7.3x

  The night spread 0.0102 is 0.1796 minus 0.1694 over pinset_night_2, _3 and
  _4; pinset_night_1 was BLANK and is excluded, so that spread is over three
  frames and not four.

  THE MARGIN FALLS FROM 193x TO 1.9x AND THAT IS THE FINDING. A verdict that
  is CLEAR by a factor of two is one bad night render from NO-READ, and
  nullSeriesVerdict reading NO-READ voids every grid cell in the run. The
  contingency is the exact thing 334 is asking: if the six night frames do not
  repeat as tightly as the pinset ones, the spread crosses 0.0193 by itself.
  An item that measures whether a thing is stable should not first make the
  whole run's floor depend on that thing being stable.

  AND THE FUNCTION ALREADY WARNS ABOUT THE CATEGORY MIX in its camera case,
  which is why this is a gap rather than a new idea.

  NOT DECIDED HERE, and it wants the director who ruled 334 rather than a
  builder: whether the settling rows declare themselves out of the null
  grouping the way they already declare themselves out of the light probe,
  whether the group choice stops being size alone, or whether the line simply
  prints the runner-up group and its spread beside the winner so the move is
  visible. The third is the cheapest and measures the most.

  UNDER D45 a tool that measures the game: a test, no review. But it is
  entangled with 334, which is structural, so it lands with that review.

  RULED 2026-09-16 (08:04Z ruling, section 3): the group choice stops being
  size alone. The floor is the largest identical-input group whose no-sky
  family holds a sky-only pair; the six settle rows and the four pinset rows
  are outside it by their own fields, no per-shot key. nullSeriesBySizeAlone
  prints what size alone would have kept, with its spread and SAME-AS-KEPT
  or DIFFERS-FROM-KEPT. The null-cell-is-last check is restated to the last
  shot of the reference cell's family (section 4); the 06:35Z placement of
  the six after it stands. The test's six assertions are upheld unchanged.
  One instrument-builder pass in VignetteSpec.h and vignette-spec-test.cpp,
  covered by that record's stamp. Acceptance is met when the suite is green
  on the live file and the planted cases print the words in section 3.
