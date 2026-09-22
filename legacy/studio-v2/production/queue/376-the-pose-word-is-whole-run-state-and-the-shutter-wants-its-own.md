line: instruments (the figure's pose readback)
spec: DICTATED BY THE DIRECTOR, 2026-09-16, as a named gap that does NOT block
  the batch it was found in.

  THE POSE WORD IS WHOLE-RUN STATE AND THE SHOT LINE HAS NONE. `figure=` and
  `figureWhy=` ride the materials DONE line, so they describe the run. The
  retry budget is 8 TICKS while the settle is 0.5 SECONDS
  (`kSettleAfterCondition`, VignetteShot.cpp:142) and `ApplyCondition` is
  re-entered every tick (:6122, :6128).

  SO BELOW ABOUT 16 FPS THE COUNT CARRIES ACROSS SHOTS, and a bind-pose destroy
  can fire AFTER the first lit frame is already on disk. The done line shows it
  (`figure=DESTROYED` beside `figureShownShots=1`) but nothing says WHICH frame
  had a figure in it and which did not. A reader looking at two night stills
  cannot tell them apart from the verdict.

  WHAT TO BUILD: a per-shot pose word, as of the shutter, on the figure
  segment, in the TESTED LAYER where the arithmetic and the string already
  live. Whole-run numbers stay on the done line; this is the per-sample half,
  which is the split `.claude/rules/instruments.md` states in as many words.
acceptance: every shot line carries whether the figure was posed, unproven or
  absent AS OF THAT FRAME, with fixtures for all three, accepting case first;
  and the done line keeps its whole-run word unchanged
max_sessions: 1
status: READY 2026-09-16, filed and NOT started. Named by the director as not
  blocking, and it is only reachable at all below about 16 fps.
