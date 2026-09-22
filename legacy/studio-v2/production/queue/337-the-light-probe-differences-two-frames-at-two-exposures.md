line: instrument (VignetteShot.cpp the probe pass at BeginNextProbe and the
  per-shot exposure write at 2102; FrameStats.h the floor line)
spec: The probe toggles a light and re-enters the Warm phase with the
  exposure rate snapped to 10000, so every OFF frame is photographed
  after the loop has re-adapted to a scene with one light fewer. Under
  AUTO every difference is the light plus the loop's answer, and run 48
  shows it: seven lights whose OFF frame came back brighter across
  831241 to 921600 of 921600 pixels, and no lantern measured in either
  direction, 0 of 24. The value cannot be pinned (VignetteShot.cpp 356
  to 358, the 2026-09-10 ruling, queue 276); a DIFFERENTIAL measurement
  needs only the two frames at one value, whatever it is.
acceptance: AutoExposureSpeedUp and SpeedDown written to 0 at the start of
  the probe pass, after the reference frame is on disk and before the
  control's re-render, restored by the per-shot write on the next shot;
  the floor line carries lightProbeHoldAsked and lightProbeHoldRead for
  both speeds; the verdict is the six controls' signed gaps, read
  against run 48's two agreeing controls (about 0.00005, decaying MOVED
  histogram) and its two shifted ones (+0.16498, +0.02572). Both
  outcomes are readable: the gaps collapse on every non-blank shot, or
  the read speeds show a clamp or the gaps stay. No night pin, no
  exposure_pin change, no determinism gate; void as an absolute
  reference. If the engine does not hold at zero, the next rung is
  reading the adapted value back from the view state and pinning both
  clamps to it for the pass, which is a readback and not a derivation.
max_sessions: 1
status: READY 2026-09-16, filed by the 06:35Z ruling section 5. Rides the
  same dispatch as 329 and 332, in the same builder's hands. Under D45 a
  tool that measures the game: a test, no review.

  NUMBERED 337 AND NOT 335, WHICH IS THE NUMBER THE RULING DICTATED. 335 and
  336 were filed by the resident while this ruling was being written, so the
  number was taken before the record naming it existed. Nothing else about
  the item is changed: the text above is the ruling's section 10 verbatim.
  Recorded here rather than silently renumbered, because a ruling that names
  a file and a tree that does not have it is the kind of mismatch a later
  session reads as a missing item.
