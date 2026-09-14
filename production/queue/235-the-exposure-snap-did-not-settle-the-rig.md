line: instruments
spec: Two photographs of one unchanged scene are the same picture, which the
  rig still cannot do, so that every cross-frame number it prints is void.
acceptance: rigDeterminism=IDENTICAL with rigDiffPixels=0/921600 on a run whose
  shot list contains both night and day conditions
max_sessions: 2
status: READY 2026-09-10 08:30Z. THE ACCEPTANCE TEST BUILT FOR THIS CAUGHT IT,
  which is the good half and the reason this is a queue item and not a disaster.

  THE READING, from the run on 83dec336:
    rigDeterminism=DIFFERS rigDiffPct=100.00 rigDiffPixels=921600/921600
    rigMeanLumaFirst=0.6102 rigMeanLumaRepeat=0.9562 rigMeanLumaDelta=+0.3460
    rigMaxAbsChannelDiff=177/255 rigRepeatOf=vign_camA_day rigRepeatAfterShots=25/25
  The FIRST shot of the run and the SAME camera and condition photographed again
  as the last thing the run does differ by a THIRD OF THE LUMA RANGE, on every
  pixel, with a worst channel difference of 177 of 255. That is not drift. That
  is a different picture.

  SO EVERY CROSS-FRAME NUMBER IN THIS RUN IS VOID, exactly as in run 38, and the
  twelve-cell sky grid CANNOT BE READ FROM IT. The whole point of the grid was
  to find the sky level, and the run that was supposed to answer it says its own
  numbers are not comparable. Nothing is concluded about sky level from this run.

  THE EXPOSURE SNAP DID NOT FIX WHAT IT WAS BUILT FOR. AutoExposureSpeedUp and
  SpeedDown at 10000 were landed to make adaptation instant. Adaptation is still
  visibly incomplete: five frames of twenty five are blown, at up to
  604972/921600 pixels clipped, and one frame is nearly black at 0.0623.

  THE ORDER IS THE EVIDENCE AND IT IS PARTIAL, stated as partial rather than
  rounded up into a theory. Blown frames sit at shots 3, 5, 10, 12 and 17.
  THREE OF THE FIVE IMMEDIATELY FOLLOW A DARK FRAME: shot 2 night 0.1112 then
  shot 3 at 0.9402; shot 4 night 0.0384 then shot 5 at 0.9591; shot 16 at
  0.0623 then shot 17 at 0.9695. That is the signature of an adaptation that has
  not come back from darkness. IT DOES NOT EXPLAIN SHOTS 10 AND 12, which follow
  ordinary day frames at 0.6241 and 0.6203, so the mechanism is not established
  and a second cause is live.

  WHAT NOT TO DO. Do not raise the snap speed again on the strength of this: the
  rate is already 10000 and the fault survived it, so the next change must be
  read off a printed series rather than guessed. Do not reorder the shot list to
  avoid dark frames, which hides the fault rather than fixing it and would also
  break C6's requirement that shot order is not monotone in sky.

  THE HONEST NEXT RUNG is to pin the exposure rather than its rate, which needs
  AutoExposureMinBrightness and MaxBrightness set equal, and which queue 219
  already names. The cost is that the rig can then never judge an adaptation
  moment, and that cost was accepted in writing when the rate was snapped.

  RULED 2026-09-14: the acceptance render is dispatched AFTER the pin batch, with
  rigRepeatOf on a pinned day condition. IDENTICAL there is step 1 met on that
  condition and says nothing about night, which stays at auto.

  RULED 2026-09-14 18:23Z (decision-2026-09-14-ruling-the-null-series-
  follows-the-judged-row.md, section 13). The post-pin run 32bae70 read
  DIFFERS 784509/921600, +0.0034, ratio 1.0053 (verdict line 323) on
  the pinned camA repeat, while the nine identical-input frames at
  cam_hook spread 0.0002 (line 319). A verifier's diagnosis names
  sub-pixel anti-aliasing sampling as the cause of the pixel COUNT
  (histogram shouldering at one and two codes, gradient-correlated, no
  one-pixel shift improves the match); the project's own FrameStats.h
  316 to 320 already says temporal AA moves pixels by a code value or
  two and measures a control for it; nothing under ue-probe, tools or
  .github pins the AA method or jitter (zero hits) and
  DefaultEngine.ini has no RendererSettings section. The camA delta of
  +0.0034 (ratio 1.0053) is NOT explained by that cause, whose ratio
  the verifier measured at 1.0000 on two pairs: a second cause is live,
  and the first frame after the scene build is a candidate, not a
  finding. NEXT STEP, THE CHEAPEST DECISIVE MEASUREMENT: one diagnostic
  run with the anti-aliasing method set to none for the probe, the
  method printed on the scene line so the run says what it rendered
  with, the same shot list, its frames neither judged nor captioned;
  read rigDiffPixels and rigMeanLumaDelta. Zero pixels differing proves
  the count is AA and the acceptance above becomes reachable by pinning
  the method; a surviving delta on camA has the second cause. The
  acceptance is then set from that printed series, never loosened by
  prose. Needs 290 first so the repeat frame can be opened. Whether
  "one picture" for JUDGING means pixel-identical or within the null
  floor is Jafar's, on the card the ruling dictates.

  ONE CANDIDATE WAS TESTED ON 2026-09-14 AND THE TEST DID NOT REACH IT.
  The 18:23Z ruling named "the first frame after the scene build" as a
  candidate for the camA delta. The dispatch was written to test it: the null
  group at cam_hook grew to nine and now contains vign_hook_day, an early
  shot, so if early frames drift the nine-frame spread should widen and
  hook_day should be the outlier. Run 622bc39 read
  nullSpreadMeanLuma=0.0002, max=vign_grid_sky100_sun003 0.5402,
  min=vign_grid_null_repeat 0.5400. The spread held at 0.0002, hook_day sits
  inside it and is NOT the outlier, and the group spans shot 5 to shot 43.
  THAT WEAKENS "EARLY FRAMES DRIFT" AND DOES NOT TEST "THE FIRST FRAME".
  vign_hook_day is shot 5 of 43; the rig repeat is of vign_camA_day, which is
  SHOT 1, and it is at cam_A while the null group is at cam_hook. So the one
  frame the candidate is about was not in the group that tested it. Reading
  this as "the candidate is refuted" would be the error, and it is written
  down here so nobody makes it.
  MEANWHILE THE DELTA GREW: rigMeanLumaDelta +0.0034 on 32bae70 to +0.0045 on
  622bc39, with rigDiffPct 85.12 to 86.69, while the seven fog rows'
  band.skyCentre.meanLuma reproduced ACROSS the two runs to four decimals on
  all four shared rungs. So whatever moves camA does not reach a band
  statistic. A test that isolates shot 1 is what this item still owes, and
  290 is still needed first so the two frames can be opened.
