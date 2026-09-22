line: instruments (the figure patch's nothing-measured exits)
spec: FOUND BY THE DIRECTOR READING THE DIFF, 2026-09-16, and it is a small
  true thing rather than a fault in a reading.

  `FrameStats.h:2511-2515` carries a seventh nothing-measured exit,
  `this-figure-has-no-ring-pixel-on-this-frame`, which CANNOT BE REACHED: after
  clipping, the ring rectangle always contains the core rectangle, and
  :2476 has already refused an empty core before control gets there.

  THE HEADER SAYS SIX AND THE TEST PLANTS SIX. So the code, the comment and the
  fixtures already agree with each other and disagree only with the unreachable
  branch sitting between them.

  WHY IT IS WORTH AN ITEM AT ALL. An exit that cannot fire is a claim about the
  world that nothing tests, and the engine half's own hand-back cited this exit
  as the place a figure a hundred times TOO LARGE would land. If that is true
  the branch is reachable and the analysis above is wrong; if the analysis is
  right, then an oversized figure lands somewhere else and nobody knows where.
  ONE OF THOSE TWO IS FALSE and the item is to find out which.
acceptance: either the exit is shown reachable by a planted fixture that hits
  it, or it is removed and the header's six becomes six everywhere; and
  whichever way it falls, the record says where a figure a hundred times too
  large actually exits
max_sessions: 1
status: READY 2026-09-16, filed and NOT started.
