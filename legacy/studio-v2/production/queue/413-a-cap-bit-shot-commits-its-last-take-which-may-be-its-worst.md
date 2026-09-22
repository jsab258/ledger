line: instruments (the settle rule's stopping behaviour)
spec: FOUND IN RUN 56, 2026-09-21, ON THE HERO FRAME ITSELF, which is what
  makes it worth its own item rather than a line in queue 384.

  THE SETTLE RULE, landed that morning and proven by run 55: take the shot
  again until two successive takes agree within `kSettleMeanLumaBound`, cap at
  `kSettleTakesMax`, and THE COMMITTED FILE IS THE LAST OF THEM. That last
  clause is correct when the shot SETTLES, because the last take is then one of
  two that agree.

  IT IS ARBITRARY WHEN THE CAP BITES, and run 56 shows the cost. `vign_camA_night`,
  the frame Jafar is waiting on, read:

      shotSettleStatus=CAP-BIT shotSettleTakes=4/of=4
      shotSettleSeries=0.14473..0.11980..0.11392..0.32375
      shotSettleDelta=+0.20983

  Takes 1 to 3 converge: 0.14473, then 0.11980, then 0.11392, with deltas of
  -0.0249 and -0.0059. The third is within 0.0009 of the bound. THEN TAKE FOUR
  JUMPS TO 0.32375 and the cap bites, so the committed file is that one: a
  frame nearly THREE TIMES the brightness of the cluster the shot was
  converging on.

  THE RESIDENT OPENED THE FRAME AND MEASURED IT: mean luma 0.32330 over every
  second pixel, against the verdict's 0.32375, so the key is honest and the
  picture is the bright take. It reads as dusk rather than night: the sky is
  near-white in a frame whose condition is wet_night.

  WHAT THIS IS NOT. It is not the exposure fix failing. The fix converges 46 of
  49 shots in this run, up from 45. It is the STOPPING BEHAVIOUR on the shots
  the cap catches, and the instrument reports CAP-BIT honestly on its own line.

  THE QUESTION THE ITEM OPENS, and it should not be answered by taking the
  median without reading the series first: when the cap bites, is the best
  committed frame the LAST take, the take CLOSEST to its predecessor, the
  MEDIAN of the takes, or is the honest answer that NO frame from a CAP-BIT
  shot should be committed as evidence at all? Run 55's four cap-bit series and
  run 56's three are the beginning of the series that answers it, and two of
  run 55's were BISTABLE rather than slow, which a median would handle and a
  last-wins cannot.

  WHY THIS SHOT CAP-BIT AT ALL, WHICH IS A SEPARATE AND UNANSWERED QUESTION.
  `vign_camA_night` SETTLED in run 55 and did not in run 56, and the only
  change to that frame is that its three control quads moved to cam_B. The
  quads were bright patches the auto-exposure was metering. THAT IS A
  HYPOTHESIS AND NOTHING HERE HAS MEASURED IT; two hypotheses about this exact
  frame have already been refuted this month, so it is written as a question.
acceptance: the series of every CAP-BIT shot across runs 55 and 56 is printed
  together, and the choice of which take to commit is made FROM that series
  with the statistic named (last-wins, nearest-neighbour, median or refuse),
  never from reasoning about which sounds safest; and whichever is chosen, a
  CAP-BIT frame carries a key saying which take it is and how far that take sat
  from the others, so a reader can tell a settled frame from a salvaged one
max_sessions: 1
status: READY 2026-09-21. Instrument work under D45: a test, no review, no
  ruling record.

  IT IS NOT A BLOCKER ON THE FIGURE. The frame is legible, the figure is fully
  visible in it, and the card is gone. This is about whether the frame is
  COMPARABLE to another frame, which for a CAP-BIT shot it is not, and the line
  says so already.
