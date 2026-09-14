line: art (the visual bar)
spec: Rung 2 of production/ladder.md. Every placed prop reads as the material it is
  meant to be, and the first batch of clutter is placed per
  production/art/atlas-01/PRODUCTION-CATALOGUE.md, in a frame Jafar can see it in.
acceptance: Jafar judges the frame. HIS EYE IS THE GATE and no number passes this rung.
max_sessions: 2
status: BLOCKED 2026-09-09 behind rung 1 (queue 180). Ruled by Jafar this morning as
  part of the visual-first ladder: "rung 2, props read as their materials and the
  first-batch clutter placed per the catalogue".
  WHAT IS ALREADY TRUE AND MUST NOT BE RE-DONE: 22 of 23 props are placed as real
  meshes with collision, proved by run 33 and recorded on production/throughput.md.
  This rung is about how they LOOK, not whether they are there.

  JAFAR ORDERED THIS NEXT, 2026-09-14, in his own words: "The materials are
  next: bins, kerbs and railings still render as untextured white, which is
  the material library item rather than a lighting one, and it is the loudest
  thing in the frame." That is this rung. THE STATUS LINE STILL READS BLOCKED
  BEHIND QUEUE 180 and a resident does not unblock a rung Jafar blocked; the
  dependency is raised to him rather than quietly dropped. Rung 1's frame did
  reach him tonight with its numbers, so the block may be spent, but that is
  his call or a director's.

  AND THE INSTRUMENT WILL TELL WHOEVER TAKES THIS THAT NOTHING IS WRONG.
  Run 622bc39 reads piecesPainted=600/610, piecesUnpainted=10/610,
  paintRoutes=pack.580/tint.10/decal-card.10/decal-multiply.0, and all ten
  unpainted are paintUnpaintedWhy=decal-needs-a-stain-material. By that key
  the street is 98 per cent painted. THE FRAME SHOWS WHITE BINS, WHITE
  RAILINGS AND NEAR-WHITE KERBS. Both are true: the key counts whether a
  piece RECEIVED a material instance, not whether the material RESOLVES to
  the surface it names. So piecesPainted is not evidence for this rung and
  must not be quoted as though it were, which is the exact shape of failure
  CLAUDE.md rule 6 is about (built is not running) one level in: assigned is
  not rendered.
  Queue 123 is DONE and proved THE STREET has its textures on run 25; that
  was the buildings, and it does not cover the props. Queue 176 (the near
  road renders near white) is the same family and may share a cause.
  A useful first question for whoever takes it: does a prop's material
  instance resolve its pack texture at run time, or does it fall back to the
  engine default, which is white? Queue 123's own title names that failure
  mode for the street; nothing has asked it of the props.
  THE CATALOGUE IS ON THE ART BRANCH, origin/art/atlas-01, and is read with git show
  rather than by merging or checking out that branch.
