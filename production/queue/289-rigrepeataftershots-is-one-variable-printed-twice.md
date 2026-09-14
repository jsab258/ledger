line: instruments
spec: VignetteShot.cpp 2829 sets OfShots = GSpec.Shots.size() and
  passes it as BOTH ShotsBetween and ShotsAsked to RigDeterminismLine
  (FrameStats.h 966 to 968) at 2833, 2842, 2848, 2856 and 2863, so
  rigRepeatAfterShots has read 25/25 and 37/37 and can read nothing
  else: it cannot see a repeat that fired early. ShotsBetween becomes
  the count of shots actually photographed before the repeat was
  captured, read off the run's own shot counter at that moment;
  ShotsAsked stays the list length. The fixture in frame-stats-test.cpp
  plants a repeat taken after 3 of 5 and expects 3/5, beside the
  accepting N/N; the rig line's stat names which count is which.
acceptance: a committed run printing rigRepeatAfterShots=<n>/<N> from
  two different variables, the planted 3/5 fixture printed red on
  the old code and green on the new.
max_sessions: 1
status: READY 2026-09-14, filed by the ruling of 18:23Z from a
  verifier's finding, verified at the lines named. Not blocking.
