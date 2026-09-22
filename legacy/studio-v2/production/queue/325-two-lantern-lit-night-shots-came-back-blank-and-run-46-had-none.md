line: engine (VignetteShot.cpp capture path), art (the visual bar)
spec: RUN 47 WROTE 41 OF 43 SHOTS AND RUN 46 WROTE 43 OF 43. The two that did
  not are pinset_night_2 and pinset_night_3, both camera cam_hook, both
  condition pin_setter_night. Measured off the committed verdict, not
  inferred:

    run 46 (c7f2cc01)   status=WROTE 43   status=BLANK 0
    run 47 (bf6fc61a)   status=WROTE 41   status=BLANK 2

    the blank shot        shotMeanLuma=0.0015  shotNonBlackPct=17.73
    its working sibling   shotMeanLuma=0.2439  shotNonBlackPct=100.00
      (pinset_night_1, SAME condition, SAME wetness, SAME capture path)

  IT IS NOT A WETNESS FAULT AND THE INSTRUMENT SAYS SO. Both blank rows carry
  shotWetness=0.9000, shotWetnessOnPieces=0.9000 and shotWetnessAgrees=yes, so
  the per-condition re-drive reached those frames; what failed is the picture,
  not the parameter. The done line agrees: wetnessRedriveWrote=10030/of=10370
  with every refusal bucket but notOurRoute at zero.

  AND IT IS TWO OF THE FOUR SHOTS AT ONE CONDITION, not all four.
  pinset_night_1 and pinset_night_4 wrote normally. A condition that was
  simply wrong would take all four. That pattern, plus shotNonBlackPct at
  17.73 rather than 0.00, says a PARTIAL frame rather than a failed capture:
  something was on screen and most of it was not.

  WHAT IS NOT DIAGNOSED AND MUST NOT BE GUESSED. Run 47 is the first run
  carrying the new 2K pack, and the pack's files grew a lot on the surfaces it
  replaced (kerb.jpg 1.15MB to 5.86MB, metal_n.jpg 1.57MB to 8.36MB). A
  longer stream before a dark night shot is A PLAUSIBLE STORY AND NOT A
  READING, and this item records it as the first thing to test rather than as
  the cause. The other candidates, neither excluded: the wetness re-drive at
  0.9 costs writes on a night condition that the day conditions do not, and
  the capture path was already noted as adopting run-wide once candidate A
  fails once (shotCaptureViaStat), which is a per-run adoption this item has
  not read the history of.

  WHY IT MATTERS NOW RATHER THAN EVENTUALLY. pin_setter_night is ONE OF ONLY
  TWO CONDITIONS IN THE SPEC THAT LIGHT THE LANTERNS (the other is wet_night;
  33 conditions carry the field and 2 set it true). Jafar's dusk frame is
  "lamps lit, wet road, a figure in silhouette. That is the picture I judge
  by." So the shots that failed are the exact family that frame belongs to,
  and a frame that renders black half the time is not a frame anybody can
  judge.
acceptance: the cause is NAMED with the measurement that names it, not with a
  story; the fix is shown by a run in which all 43 shots write, with the
  blank count printed beside its denominator so a zero cannot read as
  nothing-measured; and the rejecting case is watched, meaning a run that
  still blanks must report BLANK and not silently carry the previous run's
  file forward under its own name (ci.md). If the cause is streaming, the
  instrument gains whatever key distinguishes "the frame was not ready" from
  "the frame was black", because today shotBlank=yes cannot tell those apart.
max_sessions: 1
status: READY 2026-09-16, found by reading run 47's shot statuses against run
  46's rather than by looking for it. AHEAD OF THE DUSK FRAME, with 319 and
  324, because all three are about whether a lantern-lit night frame can be
  trusted. Under D41 the frame itself is ungated; this is not a look, it is a
  frame that does not exist, so it keeps its review.

CORRECTED AND REORDERED 2026-09-16 02:05Z, BEFORE ANYONE TOOK IT. The item
above says to diagnose the blank frames. THAT CANNOT BE DONE, because the
frames are not in the repository and never have been:

    commits that ever touched production/d1-probe/ue-pinset_night_*.png     0
    commits that ever touched production/d1-probe/ue-vign_*.png            29
    shot files the run 47 verdict NAMES with a byte count                  43
    of those, missing from disk                                            4
      (ue-pinset_night_1.png through _4.png, and ONLY those four)

  THE CAUSE IS ONE GLOB. `.github/workflows/ledger-probe-unreal.yml` line 1968
  stages `git add -A -- 'production/d1-probe/ue-vign_*.png'`. The four pinset
  shots write `ue-pinset_night_*.png`, which that pattern does not match. So
  all four have been rendered and discarded on every run since they entered
  the spec, INCLUDING the two that wrote normally this run at 1367920 and
  1278041 bytes.

  WHAT THIS CORRECTS IN THE ITEM ABOVE. The BLANK status IS new: run 46 read
  43 WROTE and run 47 reads 41 WROTE and 2 BLANK, and that comparison stands
  because it is made on the VERDICT, which is committed. What is NOT new is
  the absence of the pictures. The item's acceptance asks for a cause named by
  a measurement, and the measurement needs the frames.

  AND IT IS NOT A FAILURE OF ci.md's RULE, WHICH MAKES IT WORTH RECORDING.
  That rule says stage outputs BY NAME and never `git add <directory>`, and
  line 1968 obeys it. A by-name stage still goes blind when a new shot family
  arrives with a name the pattern does not cover, and nothing was watching the
  join. The durable fix is not a wider glob, it is a check that every file the
  verdict NAMES is a file that got committed, with both counts printed so a
  zero cannot read as nothing-measured.
acceptance ADDENDUM, and this half comes FIRST: every `file=` the vignette
  verdict names is present in the commit, proven by a check that prints
  namedFiles=N/committed=M and fails when they differ; the planted rejecting
  case is a verdict naming a file nobody staged, which is today's live tree
  and therefore free. Only once the frames land can the BLANK cause be
  diagnosed, and the run that lands them is the one that supplies the
  evidence. Under D45 the checker is a tool: a test, no review, no ruling.

RUN 48 SETTLES THE SHAPE OF IT, 2026-09-16. The staging fix worked and the
frames are in the repository for the first time, so the second half is finally
diagnosable. And the first thing the frames say is that THE BLANK IS NOT
DETERMINISTIC:

    run 46 (c7f2cc01)   43 WROTE   0 BLANK
    run 47 (bf6fc61a)   41 WROTE   2 BLANK   pinset_night_2, pinset_night_3
    run 48 (c36857c0)   42 WROTE   1 BLANK   pinset_night_1

  A DIFFERENT SHOT, AND FEWER OF THEM. Same condition, same camera, same
  capture path. A fault deterministic to a shot or to a scene would take the
  same shots every run; this moves. That is a timing or streaming race, and it
  removes the candidate this item named first, that the bigger 2K textures
  cause it deterministically. They may still make it MORE LIKELY, which is a
  different claim and is not measured.

  THE FRAMES ARE NOW ON DISK AND COMMITTED: 43 named, 43 present, 43 tracked,
  0 missing, and tools/verdict-shot-files.py's waiver EXPIRED BY ITSELF because
  run 48's verdict carries a different sha. It reads
  shotFilesWaiverApplies=no shotFilesUnwaivedFaults=0, green because there is
  nothing left to forgive rather than because anything was excused.
