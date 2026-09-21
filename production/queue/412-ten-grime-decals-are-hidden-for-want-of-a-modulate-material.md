line: engine and art, jointly (the grime is the art lane, so it sits last)
spec: FILED BY THE RESIDENT ON THE RULING OF 2026-09-21 (`game-design/decision-2026-09-21-ruling-the-shortfall-is-zero-the-recount-is-not-a-repair-and-the-card-leaves-the-hero-frame.md`, item 20), AND
  ITS CONDITION WAS PROVED BEFORE FILING RATHER THAN ASSUMED, which the ruling
  required under CLAUDE.md rule 3.

  THE GREP, run over all 398 queue items: `modulate` returns EXACTLY ONE hit
  and it is the sentence the same batch just added to queue 223. Widened to
  `stain material|grime material|decal material|multiply material|blend
  material|M_*Decal`: ZERO hits over 398. So no item named this material
  before today and the item is genuinely owed rather than duplicated.

  WHAT IS TRUE NOW, measured in run 55: `piecesPainted=600/610`,
  `piecesUnpainted=10/610`,
  `paintUnpaintedWhy=...decal-needs-a-stain-material.10`,
  `decalQuadsHidden=10/20`, `paintRoutes=pack.580/tint.10/decal-card.10/
  decal-multiply.0`.

  THE TEN ARE FAIL-CLOSED, NOT BROKEN, and the engine says why in its own
  words at `VignetteShot.cpp`: "Pasting the grime opaque would make the count
  green and the picture worse." One opaque base material cannot do a multiply
  blend, because BLEND MODE IS A MATERIAL PROPERTY AND NOT AN INSTANCE
  PARAMETER. So `SetActorHiddenInGame(true)` hides them rather than pasting
  them, and that is the right refusal.

  THIS IS WHAT QUEUE 223 NOW DEPENDS ON ENTIRELY. Its acceptance is
  `piecesUnpainted=0`, and after the 2026-09-21 batch the only thing between
  the tree and that number is a second base material with a modulate blend
  mode for these ten stains.

  IT IS GRIME, AND GRIME IS THE STRATEGY PER CANON AND PER D53. So this is not
  cosmetic tidying: it is the first authored wear on the street, and D53's
  floor, when it gets a number, is the rule it is authored under.
acceptance: a second base material with a modulate blend mode exists and is
  named in the piece path; `decal-multiply` moves off zero in `paintRoutes`;
  `piecesUnpainted` reaches 0/610 with `decalQuadsHidden` falling by the same
  ten; and THE FRAME IS OPENED afterwards, because a grime decal that makes the
  count green and the picture worse is the exact failure the current refusal
  exists to prevent, and only a picture can tell those apart
max_sessions: 2
status: READY 2026-09-21, and it sits LAST of the three the ruling left the
  resident, per Jafar's order of that date: the visual slice first, the
  measurements beside it, the art lane behind both, and cut from the bottom.
  The grime is the art lane.

  RULED BY: the ruling above, item 20, whose grep condition is proved in the
  spec.
