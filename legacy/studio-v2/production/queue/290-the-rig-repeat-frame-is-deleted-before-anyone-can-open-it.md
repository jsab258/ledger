line: instruments (the evidence channel)
spec: Finish() in VignetteShot.cpp (2345 to 2354) deletes
  kRepeatPngLeaf at 2352 under the comment "THE PROBE'S SCRATCH FRAME
  IS NOT EVIDENCE", so the frame behind rigDiffPixels and
  rigMeanLumaDelta never reaches the committed channel and nobody can
  open the difference the headline number describes (CLAUDE.md rule
  12). The repeat frame is kept, staged BY NAME in the workflow beside
  ue-vign_camA_day.png (ci.md: stage outputs by name) with a per-run
  copy keyed by short sha; the light-probe scratch frame at 2351 stays
  deleted, and the comment says which of the two is evidence and why.
acceptance: a committed run whose tree carries the repeat frame beside
  its first frame, rigRepeatOf naming both files, and a difference
  image or histogram producible from the two committed files by a
  tool under tools/ on this machine.
max_sessions: 1
status: READY 2026-09-14, filed by the ruling of 18:23Z from a
  verifier's finding, verified at the lines named. Lands before or
  with the diagnostic run under 235, which is unreadable without it.
