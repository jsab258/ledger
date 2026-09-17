line: engine and instruments, jointly (D41 visual; the blocker on the figure)
spec: RUN 54's NIGHT FRAME IS BLACK AND NOTHING ELSE CAN PROCEED UNTIL IT IS
  NOT. `ue-vign_camA_night.png` measures meanLuma 0.60 against run 53's 28.26
  on the same file by the same ruler. The figure is at the right place and the
  right size (projH 175.65 against 173 predicted, box x561..719) and cannot be
  seen at fourteen times brightening: no head, no shoulders, a faint smear.

  THREE CAUSES ARE REFUTED, each by a measurement rather than an argument, and
  they are recorded because each was believed by somebody here:

  1. NOT THE MATERIALS. `materialsStatus=PARTIAL` with
     `surfacesResolved=12/16` and the same four absent surfaces (card,
     interior, multiply, paint_yellow) in run 53 AND run 54. RUN 53 WAS NEVER
     WHOLE. The resident claimed the figure import's raise degraded the
     material step and committed that claim in 3aa06483; it is false and the
     correction is in this item and in the record.
  2. NOT A LEAKED EXPOSURE PIN. `shotExposurePin=AUTO` on the camA_night line
     in both runs, so no override carried over from an earlier shot.
  3. NOT A BRIGHT FIGURE PULLING AUTO-EXPOSURE DOWN. That was the resident's
     second hypothesis and the figure's own reading kills it:
     `coreMeanLuma=0.0` beside `ringMeanLuma=0.7`. The figure is as black as
     everything else. A lit object near the camera would read bright.

  WHAT IS STILL TRUE AND NARROWS IT: the three DAY frames are bit-identical
  between the runs. The lamps are still lit, `lampGlowLit=3/of=3`, in
  IDENTICAL pixel boxes with identical pixel counts, but the core halved
  (249 to 103) and the ring around it fell about 65-fold (71.2 to 1.1). Scene
  WHOLE, capture ALL. So the geometry, the materials and the day path are
  unchanged and only the NIGHT path lost its light.
acceptance: a night frame at a brightness in the bracket run 51 and run 53 sat
  in, with the cause of the collapse named by a printed reading rather than by
  elimination; and whatever is added prints on the night line so the next
  collapse is diagnosed from the verdict instead of from a crop
max_sessions: 1
status: READY 2026-09-17, filed at the budget ceiling, NOT started.

  DO NOT DISPATCH BEFORE THIS IS UNDERSTOOD. A run now buys another black
  frame, and Jafar's standing ask is a frame with a person standing in a lit
  street. The pose is not the blocker: it works, at 87.0230 cm of bone
  movement against a 0.0010 bound, latched on the first tick.

  WITHDRAWN 2026-09-17 12:2xZ, MEASURED AND REFUTED BY THE CONTROL LINES AT
  THE FOOT OF THIS ITEM. Left standing so the next reader sees what was believed:
  THE ONE CHANGE BETWEEN THE RUNS THAT TOUCHED THE NIGHT PATH AT ALL is the
  figure moving from x=17.5 to x=10.0, which is 6.00 m from the camera and
  exactly MIN_CAM_DISTANCE_M. That is the first thing to test and it is a
  HYPOTHESIS, not a finding: nothing here has measured it, and two hypotheses
  about this frame have already been refuted.

  A FOURTH CAUSE IS REFUTED, 2026-09-17 12:2xZ, AND IT IS THE ONE THIS ITEM
  NAMED AS THE FIRST THING TO TEST. The figure moving to 6.00 m cannot be the
  cause, because the identical scene with the identical figure photographs at
  both ends of the range within the same run. Read off run 54's own control
  lines, which nothing here had looked at: `kind=control` is
  `control_no_toggle`, defined at VignetteShot.cpp:4139 as "the same camera,
  the same condition, the same frame counts and NOTHING TOGGLED", so its two
  takes are the same picture twice.

  TWELVE CONTROL LINES EXAMINED, all lightStatus=MEASURED, one per night shot.
  Two agree with themselves (settle_night_2 at 0.00282, settle_night_4 at
  0.00405). TEN DO NOT, by 0.20 to 0.46 of whole-frame mean luma, and nothing
  falls in between. Three of those ten are POSITIVE, so it is not a progressive
  dimming. The worst is pinset_night_3 at -0.45548: 0.46185 on one take and
  0.00637 on the next.

  THE SAME SCENE LANDS ANYWHERE. cam_hook photographs settle_night_2 at 0.46449
  and pinset_night_3 at 0.00637, same camera, same street, same figure standing
  in the same place. THE FIGURE READS EXACTLY AS BRIGHT AS WHATEVER THE FRAME
  LANDED AT, monotonically across all eleven shots that carry a figure record:
  control-on 0.46585 with core 66.3, 0.26823 with 26.0, 0.21126 with 16.1,
  0.18404 with 12.4, 0.00637 with 0.0, 0.00222 with 0.0. The figure is not
  darkening the frame and is not being darkened by the frame; both readings are
  the same exposure, printed twice.

  SO THE BLACK FRAME IS NOT A LIGHTING FAULT AND NOT A CONTENT FAULT. The night
  capture lands at an arbitrary exposure, and vign_camA_night happened to land
  at the bottom of it. The clustering (0.006, 0.18, 0.21, 0.27, 0.32, 0.46)
  is what an unconverged auto-exposure looks like sampled at different instants,
  and `shotExposurePin=AUTO` is the condition that permits it rather than the
  proof it did not happen; refutation 2 above screened for a LEAKED PIN, which
  is a different question.

  WHY NOBODY SAW IT. The rig's own determinism check photographs a DAY frame:
  `rigRepeatOf=vign_camA_day`, `rigRepeatAfterShots=49/49`,
  `rigMeanLumaDelta=-0.0017`. The night path it never looks at is off by up to
  270 times that. FrameStats.h:1818 records why the check was built at all: run
  38's control differed by 0.0038 and that was judged enough to say "a rig whose
  output depends on when a frame was taken cannot compare frames". Ten of twelve
  night controls are 50 to 120 times past that reading.

  WHAT THIS CHANGES IN THIS ITEM: the hypothesis at the bottom is withdrawn, and
  the acceptance line's "cause named by a printed reading rather than by
  elimination" is now half answered. What is NOT answered: why the night capture
  does not converge when the day capture does, and what would make it. Also
  unexamined here: whether the night stills already committed under
  game-design/sim-shots/ are comparable to each other at all, which on these
  numbers they are not. FILED, NOT STARTED, per his standing order.
