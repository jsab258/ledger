line: instruments and engine, jointly (the figure's pose readback)
spec: RUN 53, THE FIRST RUN THAT EVER PUT A FIGURE IN QUAY STREET, AND THE
  DONE LINE CONTRADICTS ITSELF.

    figure=STANDING  figureWhy=pose-evaluated
    figurePoseMaxBoneDeltaCm=0.000/overBones=65

  THOSE TWO CANNOT BOTH BE TRUE BY THE INSTRUMENT'S OWN DEFINITION. The pose
  test was built to need no threshold precisely because component-space
  transforms are seeded FROM the reference pose, so a figure that never
  evaluated reads delta EXACTLY 0 on every bone. It read exactly 0 on all 65.
  That is the bind pose, which the code is supposed to DESTROY the actor for,
  and instead it reported `pose-evaluated` and let it stand.

  SO THE FIGURE IN RUN 53 IS ALMOST CERTAINLY A T-POSE. The engine-specialist's
  own hand-back named this exact outcome in advance: the readback assumes a
  STOPPED single-node instance still evaluates at its set time, recalled at
  0.8 confidence, and "if that is wrong the run does not fail to build, it
  prints figurePoseMaxBoneDeltaCm=0.000 and destroys a perfectly good figure."
  What happened is the same fault with the opposite ending: it did not destroy.

  TWO BUGS, NOT ONE, AND THEY MUST BE FIXED IN THIS ORDER. First the DESTROY
  DECISION, because a contradiction on the done line is worse than either
  answer alone: a reader who greps `figureWhy=pose-evaluated` is told the
  opposite of what the number beside it says. Second the POSE ITSELF, which is
  why the delta is zero.
acceptance: on a frame where the anim demonstrably evaluated, the delta is
  nonzero and the word says so; on a planted bind-pose frame the actor is
  destroyed and the word says THAT; and no frame can print a word and a number
  that disagree, proven by a fixture that plants the disagreement and is
  refused
max_sessions: 1
status: READY 2026-09-16, filed at the ceiling of the budget Jafar set, NOT
  started. He ruled: spend what remains on the figure and nothing else, and
  send the frame.

  DO NOT FIX THE POSE FIRST. The contradiction is the cheaper and more
  dangerous of the two: it is what makes a future green line unreadable.
