line: instruments
spec: CLAUDE.md rule 12 names game-design/sim-shots/ as the channel that works.
  Every file in it is from 2026-09-03 and from Unity, the engine D16 retired on
  2026-09-10. The live Unreal frames are written to production/d1-probe/. A reader
  who follows the rule reaches stale frames from the wrong engine.
acceptance: the documented channel carries the live engine's frames, or rule 12 and
  every pointer to it name the live path; and a reader can tell a frame's engine and
  commit WITHOUT running git log on it
max_sessions: 1
status: READY 2026-09-14. IT CAUGHT THE RESIDENT TODAY, which is the argument.

  WHAT HAPPENED, recorded because the incident is what makes this believable.

  The resident set out to obey rule 4, opened game-design/sim-shots/vign_camA_day.jpg
  and vign_camA_night.jpg, measured them, and reported THREE FAULTS to Jafar:

      "the day frame has no sun and casts no shadow anywhere"
      "the night frame is brighter than the day frame, 0.3014 against 0.2733"
      "the sodium has eaten all colour"

  ALL THREE WERE FALSE. Measured on the live Unreal frames from the same run:

      camA day    live 0.6410   stale 0.2734
      camA night  live 0.1115   stale 0.3014

  The live day is 5.7x the night, not darker than it. The hook frame carries a
  measured shadow step of +0.1867 against a null of 0.0013, seven times what queue
  206 asks for. Sodium-signature pixels are 5784 of 921600, 0.63 percent, not a
  flood. The resident then briefed a builder on those three faults and told it "the
  wet road already works, do not break it", when the Unreal probe has NO WETNESS AT
  ALL: the three wetness conditions read 0.6598, 0.6600 and 0.6598, inside the run's
  own null.

  THE FILES ARE NOT MISLABELLED. They are exactly what they say: sim stills from
  cb4767e, committed 2026-09-03 by 28a2d6e1. Nothing lied. The fault is that the
  DOCUMENTED PLACE TO LOOK and the PLACE THE LIVE ENGINE WRITES are different
  directories, and the rule points at the first.

  WHY IT IS RULE 3 AND NOT RULE 4. The resident did open an artifact. It opened the
  wrong one and never checked its date or its engine, then reasoned confidently from
  it for two hours and put the conclusions in front of Jafar. SUSPECT THE INSTRUMENT
  FIRST: a file under the documented evidence path, named for the camera and the
  condition, looked like the current street and was not.

  THE TWO CANDIDATE FIXES, and this item does not choose between them:

  1. CI writes the live Unreal frames INTO game-design/sim-shots/, so rule 12 stays
     true and one path is the answer. Costs a copy per run.
  2. Rule 12 and every pointer to it are re-aimed at production/d1-probe/, and
     sim-shots is marked as the Unity archive in its own README.

  EITHER WAY, ONE THING IS REQUIRED: a reader must be able to tell a frame's ENGINE
  and COMMIT without running git log on it. A sidecar naming both, or the commit in
  the filename, or a manifest beside them. The directory currently offers no way to
  know, and a picture that cannot say when it was taken is the same class of
  instrument as a verdict key with no denominator.

  CHECK FOR OTHER READERS OF THE STALE PATH before choosing: tools/report-frame.py,
  the brief photo sidecars and the dashboard all reference sim-shots, and any of them
  may be showing Jafar September 3rd frames as though they were current.
