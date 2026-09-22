line: art (the visual bar) and engine, jointly
spec: production/d1-probe/ue-vign_camA_night.png, written by run 46 on
  64103f7b, carries in the middle of the shot a piece reading as a
  FOUR-QUADRANT PRIMARY-COLOUR CARD, green and yellow over red and blue,
  mounted on the lamp post, plus TWO TEXTURE SWATCHES apparently floating in
  mid-air against the left-hand brick wall. Both are in the frame a judge
  would look at.
  WHAT IS NOT DIAGNOSED AND MUST NOT BE GUESSED: whether these are spec pieces
  rendering wrong or geometry that does not belong in the scene at all. The
  spec HAS card-shaped piece kinds (flat_cards, shop_cards,
  _lit_interior_card, and "card" appears as a value ten times in
  production/specs/vignette-pieces.json), so a spec piece with an unbound or
  default material is the likelier of the two and a four-quadrant primary
  grid is what several engines draw when a texture fails to bind. But a
  picture is strong evidence that something is wrong and weak evidence of
  what, which is CLAUDE.md rule 4, so the taker MEASURES which pieces those
  are before deciding anything.
  WHY IT MATTERS NOW RATHER THAN EVENTUALLY: Jafar's third item for the visual
  slice is a dusk frame, "lamps lit, wet road, a figure in silhouette. That is
  the picture I judge by." Neither a colour calibration card nor a floating
  swatch belongs in the picture he judges by, and the night condition is the
  one that frame will be taken in.
acceptance: each object is IDENTIFIED BY NAME out of the spec or shown to be
  absent from it, with the count of pieces examined beside the count found, so
  a zero can tell nothing from fine. If they are spec pieces with a material
  fault, the fix is the material and the accepting case is the same shot with
  them reading as whatever they are meant to be; if they do not belong in the
  scene, the fix is placement and the accepting case is the same shot without
  them, with a check that says which pieces were removed and why. Both
  outcomes watched, and the frame opened rather than a gate read.
max_sessions: 1
status: READY 2026-09-15, found while reading run 46's night still under the
  07:55Z ruling's section 9 order, and not while looking for it. AHEAD OF THE
  DUSK FRAME in his order, because the dusk frame is taken in this condition.
  NOT A REGRESSION FROM THE WETNESS BATCH and it is worth saying so: the
  wetness rung touched the albedo and roughness of four ground surfaces and
  nothing about placement or about these pieces. Whether these objects were in
  earlier night stills is the taker's first cheap check, out of git.

MEASURED 2026-09-15 BY THE RESIDENT, the item's own first cheap check plus
three leads. This does not do the item; it removes the guesses it warned
against.

THE CARD IS NOT NEW AND IS NOT A WETNESS REGRESSION. One rectangle
(487,298)-(613,423), read off the run 46 frame and applied IDENTICALLY to
three committed versions of ue-vign_camA_night.png, with a brick control at
(30,60)-(130,200) in the same frames:

    frame               meanR  meanG  meanB   chromaSpread   brick control
    run 46 (HEAD)        38.3   36.6   20.8      68.81            5.12
    run 45 (22c922ee)    43.3   41.3   24.3      77.43            5.53
    older  (835602f2)    31.6   29.7   16.2      57.00            6.11

  chromaSpread is the mean over texels of (max channel minus min channel),
  0..255. A saturated primary card reads 57 to 77 where brick in the same
  frame reads 5 to 6, so the object is present in all three and predates the
  wetness batch by at least three runs. The item's "NOT A REGRESSION FROM THE
  WETNESS BATCH" is now measured rather than reasoned.

  MY SWATCH RECTANGLES DID NOT SEPARATE THE SWATCHES FROM BRICK: (140,300)-
  (255,420) read chroma 6.36 against the control's 5.12, which is no
  separation at all. Either the rectangles are in the wrong place or the
  swatches are genuinely low-chroma. They were read off a displayed image by
  eye, which is the exact fault instruments.md names, so they are reported as
  a failed localisation and not as a finding. The taker needs a better one.

THREE LEADS, none of them a diagnosis.
  1. The spec has exactly 10 pieces with surface "card" (indices 496 to 505)
     and NONE is a colour grid by name: 4 are C6_fascia_lettering, 3 are
     C11_lit_interior_card, 3 are G6_fly_posters. All shop signage. So the
     "likelier of the two" reading in the spec above (a spec card piece with
     a default material) has to name WHICH of those ten, or look elsewhere.
  2. The scene line (verdict line 186) reads propStandIns=1/40. One prop of
     forty renders as a stand-in. A stand-in quad is the shape a floating
     swatch has, and one is fewer than the two swatches seen, so it cannot
     explain both. Worth opening before the card pieces are.
  3. decalQuads=20/20 on the same line, all placed.

ANSWERED 2026-09-16, and the swatches this item could not localise are the
run's own control quads. An artifact-reader matched the verdict's projected
boxes to the card and both swatches, and the resident re-measured the three
from ue-vign_camA_day.png: the card at x488..614 shows four saturated colours
(within-quad channel spread 148.4), and the two swatches at x309..437 and
x130..261 are UNIFORM PALE FALLBACKS at spread 10.2 and 16.1. This item's
hand-read rectangle (487,298) to (613,423) matches the projected box
x488..614 y298..422 to within two pixels, which is why the eye-chosen
rectangle for the card worked and the ones for the swatches did not: the
swatches are not a different material, they are the same instrument failing
to load its texture, so there was no chroma separation to find. The
measurement that this item reported as a failure was correct and its target
was wrong.

  So this item's question is closed and the FAULT it uncovered is queue 339.
  Nothing here is spec geometry: controlQuadVisibility is
  hidden-for-every-shot-whose-camera-is-not-the-one-they-were-placed-from,
  and the quads are built in code, which is why ruling out the 10 pieces
  tagged surface card was correct and led nowhere.

  RULED 2026-09-21: the controls move to cam_B by
  LedgerSurface::ControlCameraId(); closes on the first landed run whose
  vign_camA_night line reads shotWholeFrameIncludesControlQuads=no and whose
  still, opened, carries no card and no swatch.
