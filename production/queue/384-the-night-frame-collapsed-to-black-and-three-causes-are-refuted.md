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
status: LANDED 2026-09-21 at run 55 (commit 2490b864). The cause is named by a printed reading, the fix is proven by the rig repeat at 0.00061 on a NIGHT shot, and 45 of 49 shots settle. What remains is filed elsewhere: the control instrument, the two bistable shots, and queue 223. Was READY 2026-09-17, filed at the budget ceiling, NOT started.

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

  RUN 53 HAS THE SAME FAULT, SO IT PREDATES THE FIGURE RAISE ENTIRELY, read
  2026-09-17 13:1xZ out of 4696d113 and compared against 341ea3b2 key by key.

  TWELVE CONTROLS IN EACH RUN, THE SAME TWELVE SHOTS. Run 53: 4 agree within
  0.005, 8 disagree, worst 0.45541. Run 54: 2 agree, 10 disagree, worst 0.45548.
  So this item's opening sentence, that run 54's night frame collapsed, is a
  reading of ONE SHOT in a run whose whole night pass was already unstable, and
  run 53 was unstable too while it was being called the good run.

  WHICH SHOT PHOTOGRAPHS STABLY IS NOT A PROPERTY OF THE SHOT. Of the twelve in
  both runs, ONE (settle_night_4) is stable in both. Four change class between
  the runs: pinset_night_2 and settle_night_3 and settle_night_6 are stable in
  53 and not in 54, settle_night_2 the other way. A fault that moves between
  runs on identical shots is a race, not a scene property, and no amount of
  looking at the street will find it.

  AND THE STREET IS PROVABLY UNCHANGED BETWEEN THE RUNS. vign_camA_night's
  control photographs its OFF frame at 0.31688 in run 53 and 0.31692 in run 54,
  the same picture to four decimals. Only the ON frame moved, 0.11054 to
  0.00222. Whatever the figure raise did, it did not darken this scene: run 54
  renders it at 0.3169 in its own off-frame.

  WHAT THIS RETIRES. The comparison at the top of this item, meanLuma 0.60
  against run 53's 28.26 or 43.6, is not a like-for-like reading and neither
  number should be quoted again: 43.6 is run 49's sky floor (queue 361), and run
  53's camA_night figure reads coreMeanLuma=25.6 ringMeanLuma=42.6, which is a
  figure-ring statistic and not a frame mean. The budget file carried the same
  false pair in its 2026-09-17c note and is corrected under D43.

  THE ACCEPTANCE LINE ABOVE IS NOW WRONG IN ITS FIRST HALF. "A night frame at a
  brightness in the bracket run 51 and run 53 sat in" cannot be the test, because
  run 53's own bracket was the race's output. The test is the CONTROL: twelve
  controls agreeing with themselves within some bound read off a printed series,
  before any night brightness is compared to any other. Still filed, still not
  started.

  ORDERED AHEAD OF THE FIGURE BY JAFAR, 2026-09-17 13:1xZ: "The night exposure
  fault comes before the figure, since a figure cannot be judged in a frame
  whose exposure is random." So this item is not the studio's to reorder under
  D44. It is also item 1 of D28's own list, "fix the exposure fault so the same
  camera and conditions give the same picture", which has been open since
  2026-09-14 and was never closed. Still not started, per the same message.

  THE CAUSE IS FOUND AND IT IS NAMED BY A PRINTED READING, 2026-09-21, which
  is the half this item's acceptance line was still owed. THE COMMITTED FRAME
  IS THE ONLY FRAME IN THE RUN PHOTOGRAPHED WITH EYE ADAPTATION LIVE.
  `HoldExposureSpeedsForProbe` at VignetteShot.cpp:4430 sets
  AutoExposureSpeedUp and AutoExposureSpeedDown to 0.0f for the whole light
  probe pass, READ AND CONFIRMED IN THE CODE BY THE RESIDENT. So each night
  shot is photographed once for the file with the speeds at 10000, and then
  eight more times with them frozen.

  THE TWO POPULATIONS, off run 54's own committed verdict at d900f0d:
  96 FROZEN takes (12 night shots x 8), within-shot spread PEAK 0.00036 and
  MEDIAN 0.00021, no shot over 0.0004, and four of the twelve repeating to
  five decimals exactly. 12 LIVE takes, one per shot: 0.00282, 0.00405, then
  0.20487 through 0.45548. NOTHING FALLS BETWEEN 0.00405 AND 0.20487, a gap
  of a factor of 50.

  So the rig repeats itself to four decimals across eight takes and thirty
  seconds when nothing is adapting, and only the frame with adaptation live
  lands anywhere. THAT ALSO ANSWERS WHAT THIS ITEM COULD NOT: why a shot
  changes class between runs. Each shot inherits whatever exposure the
  previous shot's probe pass froze, is then disturbed by its own condition
  re-apply and sky-epoch bump, and is photographed 32 frames later, mid
  flight. The two shots that agreed both agreed AT THE TOP (0.4645 and 0.4658
  against 0.4617): they are the two that started already converged.

  IT IS EXPOSURE AND NOT LIGHTING, by a reading rather than by elimination:
  darkerThanSkyMedianPct=100.0000 on both the bright and the dark frames, and
  sky, ground and figure all scale together.

  THE FIX, IN THE TREE AND NOT YET RUN: convergence is a CONDITION. The
  capture re-takes until two successive takes agree within
  kSettleMeanLumaBound, cap kSettleTakesMax, and the committed file is the
  LAST take. A re-take returns to Warm and NOT to ApplyShot, so the condition
  is not re-applied and the sky epoch is not bumped: take two is a take of the
  same settled scene rather than a new disturbance of it. Arithmetic, decision
  and every string are in FrameStats.h where g++ runs them; VignetteShot.cpp
  supplies live state only. The resident compiled and ran
  ue-probe/tests/frame-stats-test.cpp independently: 267 check(s), 0 failures.

  THE BOUND IS 0.005 AND IT IS A PEAK, NOT A MEDIAN AND NOT A TARGET. It is
  the largest converged residual this project has ever printed (0.00405),
  rounded up to the next half decade, and it sits in an empty gap below the
  smallest fault ever printed (0.20487). Run 53 separates in the same place.
  Nothing exits non-zero on it: grepped, no .py, .yml or .sh reads any settle
  key, so it is a reading and not a gate. NO EXISTING BOUND WAS LOOSENED; the
  determinism check keeps its zero epsilon for IDENTICAL.

  WHAT IS STILL OWED AND ONLY A RUN CAN BUY IT: a LIVE-against-LIVE series at
  night. Every pair in the record has one frozen half. The loop prints
  shotSettleSeries for all 49 shots, which IS that series, and the constant
  comes down to it once it lands.

  THE DETERMINISM CHECK NOW REPEATS TWO SHOTS, the first of the run and the
  first whose condition reads sun OFF, the family read off Condition::SunOn
  and never off a shot's name. A target with no frame behind it prints
  NO-SUCH-SHOT or NO-FIRST-FRAME with its family, so a run that photographed
  no night shot cannot read as a run that checked the night path.

  RULED BY THE RESIDENT, 2026-09-21, ON THE ONE RESIDUAL RISK THE BUILDER
  RAISED. A re-take rewrites the shot's PNG, so a re-take that produces no
  file where the first take did makes the shot read NO-FILE and the step exit
  non-zero, where today it would commit a random frame. The builder offered
  about four lines of backup-and-restore insurance. IT IS DECLINED. A loud
  NO-FILE is the better failure: this project's own rule is that a run which
  measured nothing must say so, and committing a random frame is precisely the
  silent wrong answer this whole item exists to stop. The insurance would also
  add untestable code to the one layer that cannot compile in the container,
  against evidence that the risk is small (run 54 landed 145 of 145 captures,
  with the 25 second ceiling and the HighResShot fallback already in place).

  THE ACCEPTANCE LINE, REWRITTEN BY THE RESIDENT, replacing the first half
  this item already marked wrong: the twelve `light control_no_toggle` deltas
  collapse from the 0.20..0.46 band to under kSettleMeanLumaBound, and
  `rigRepeatsShots` names a NIGHT shot. Until a run prints both, this is a fix
  in the tree and not a fixed fault.

  STATUS: the fix is IN THE TREE, UNCOMMITTED AND UNDISPATCHED. Every engine
  side edit is unverifiable until CI, which the builder says plainly.

  A SEPARATE FINDING, FILED AND NOT CHASED, per CLAUDE.md rule 11. THE DAY
  PATH IS NOT CLEAN EITHER, IT IS ONLY SMALL. Run 54 reads
  rigDeterminism=DIFFERS rigDiffPixels=677980/921600 which is 73.57 percent of
  the frame, rigMaxAbsChannelDiff=43/255, rigMeanLumaDelta=-0.0017. The day
  check has been reading as fine because its NUMBER is small, which is not the
  same as identical, and the check's own rule says any nonzero here means a
  cross-shot comparison is partly a comparison of the rig. Filed here; it does
  not generate its own work in this session.

  AND A CONCLUSION THAT REACHES BACKWARDS, recorded because it changes what
  the archive is worth: the night stills already committed under
  game-design/sim-shots/ ARE NOT COMPARABLE TO EACH OTHER, and no fix here
  makes an old file comparable. Every night judgement made before this lands
  was made against a moving target, which is what Jafar said on 2026-09-17
  when he ordered this ahead of the figure.

  RUN 55 LANDED 2026-09-21 13:55Z AT COMMIT 2490b864, whose subject names the
  dispatch sha 4421af2b; ancestry confirmed with `git merge-base --is-ancestor`
  rather than by branch movement or run name.

  THE FIX WORKS AND THE ACCEPTANCE THAT PROVES IT IS THE RIG REPEAT.
  `rigRepeatsShots=vign_camA_day/day..vign_camA_night/night`, so a NIGHT shot
  is repeated and the blind spot is closed. `rigRepeats=2/of=2`,
  `rigRepeatsWithinBound=2/of=2`, `rigRepeatsWorstMeanLumaDelta=0.00061` on
  `vign_camA_night`. THE SAME NIGHT CAMERA PHOTOGRAPHED AT OPPOSITE ENDS OF THE
  RUN NOW AGREES TO SIX TEN-THOUSANDTHS, against a 0.20 to 0.46 band before.
  `settleSettled=45/of=49`, `settleNoFile=0/of=49`, so the declined
  backup-and-restore risk did not materialise on a single shot of 49.

  THE ACCEPTANCE THE RESIDENT WROTE INTO THE DISPATCH WAS THE WRONG TEST, and
  it is corrected here rather than quietly dropped. It said the twelve
  `light control_no_toggle` deltas must collapse under 0.005. THEY READ 0 OF 12
  WITHIN BOUND, and that is not a failure of the fix: THE CONTROL'S TWO HALVES
  NO LONGER GET THE SAME TREATMENT. Read in the code: `AfterFrame`'s
  `if (GRepeating)` branch calls `SettleRecordTake` and returns to Warm, so the
  repeat settles; the `if (GProbing)` branch goes straight to `MeasureProbe`
  with no settle at all. So the control now differences a SETTLED committed
  frame against an UNSETTLED probe re-render, and its delta measures the gap
  between two regimes rather than instability.

  THE FROZEN HALVES ARE NOT STABLE EITHER, measured run 54 against run 55 over
  the same twelve shots: the probe-side (`meanOffFull`) value moved by more
  than 0.005 on 4 OF 12 SHOTS, three of them by about 0.455, flipping between
  roughly 0.00639 and 0.46178. Those two numbers recur exactly across shots and
  runs, which is what a clamp looks like rather than a measurement.

  SO THE CONTROL NEEDS THE SETTLE LOOP ON ITS PROBE HALF, or it needs to stop
  being called a control. That is filed as its own item; it is NOT a reason to
  doubt the fix, and the rig repeat is the reading that answers queue 384.

  FOUR SHOTS HIT THE CAP AND ALL FOUR ARE NIGHT SHOTS. `settleCapBit=4/of=49`,
  `settleTakesMax=4`. Their series, which name two different failures:
    0.00637..0.18295..0.00637..0.19985   BISTABLE, alternating clamp to mid
    0.13620..0.05921..0.13383..0.22981   BISTABLE
    0.46505..0.18407..0.23145..0.27467   DRIFTING DOWN, deltas shrinking
    0.22965..0.21739..0.20541..0.18929   DRIFTING DOWN, deltas not shrinking
  A larger cap would probably catch the two drifters and will NEVER catch the
  two that alternate. The instrument marks all four CAP-BIT and says on their
  own lines that they may not be compared to another frame, which is the
  behaviour wanted; what is not yet known is why two shots are bistable.

  WHAT THE FRAME SHOWS, OPENED BY THE RESIDENT RATHER THAN READ OFF A KEY
  (rule 4). `ue-vign_camA_night.png` is legible for the first time: wet road,
  brick on the left, dark tiled wall on the right, lamps lit, fog, AND A FIGURE
  STANDING ON THE FOOTWAY. `ue-pinset_night_3.png` went from 155,155 bytes to
  1,353,003 bytes, which is what a near-black frame becoming a real image looks
  like on disk.

  THE FRAME IS SPOILED BY A DIFFERENT AND OLDER FAULT, and the separation of
  causes is clean: a FOUR-QUADRANT COLOUR CARD sits across the figure's torso
  and its legs render flat yellow. `surfacesAbsent=card/interior/multiply/
  paint_yellow` with `surfacesResolved=12/16`, IDENTICAL to run 54 and run 53.
  The colour card IS the unresolved `card` surface and the yellow IS
  `paint_yellow`. That is queue 223, READY since 2026-09-09 and never started,
  and it is now the only thing between Jafar and a judgeable figure frame.

  THIS ITEM'S ORIGINAL QUESTION IS ANSWERED AND THE ITEM IS DONE. What remains
  belongs to other items: the control's probe half, the two bistable shots, and
  queue 223's four surfaces.
