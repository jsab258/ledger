line: instrument (FrameStats.h LightProbeDoneLine, VignetteShot.cpp
  ShouldProbeShot)
spec: Until queue 334, a shot's eligibility for the light probe was a pure
  function of its CONDITION, so no instrument ever had to say which rows were
  skipped or why. 334 gives a ROW the power to decline the pass. The done line
  carries GSkippedOff and GSkippedBudget and has no third bucket, so six rows
  that the SPEC declined will be counted as six rows whose conditions turned
  the lights off. Two different facts under one number.
acceptance: a third bucket on the done line for rows the spec declined, named
  so it cannot be read as a condition with its lights off, with all three
  buckets summing to the rows not probed and that arithmetic printed
max_sessions: 1
status: READY 2026-09-16, found by the 334 builder and outside its brief.

  THIS IS THE SAME SHAPE AS QUEUE 329 AND 332, which is why it is worth one
  line now rather than after the next run: a frame that failed to render and a
  frame with the light off are different facts the instrument could not tell
  apart, and a row that declined the pass and a condition with its lights off
  are different facts the instrument cannot tell apart either. Every one of
  these has cost a false number in the channel.

  IT LANDS WITH 334 OR IMMEDIATELY AFTER IT. Before 334 there is nothing to
  count, so this cannot be tested on an accepting case until those rows exist.

  UNDER D45 a tool that measures the game: a test, no review.
