line: instruments (the figure's silhouette reading)
spec: FOUND BY THE BUILDER THAT WROTE THE INSTRUMENT, re-reading its own diff,
  and filed rather than fixed in place because the fix reaches a second
  consumer.

  `MeasureFigurePatch` reuses `LampRingPadPx`, which pads the core box by its
  LONGER side. For a lamp head, which is roughly square, that is a tight
  annulus. For a FIGURE, which is tall and thin, it is not: an 18 by 60 pixel
  person gets 60 pixels of pad on every edge, so 1080 core pixels are read
  against a ring of 15480. THAT IS 14 TO 1, and it reaches about a
  figure-height of road out to each side and a figure-height of sky above.

  SO `ringMeanLuma` IS NOT WHAT THE NAME SUGGESTS. It is the general
  brightness of this part of the street, not what is directly behind the
  shoulders. The silhouette answer is still a real comparison and the reading
  is not wrong; it is answering a slightly different question from the one a
  reader of the key will assume, which is the failure mode CLAUDE.md rule 2
  is about: say which statistic the number is OF.

  WHY IT WAS NOT FIXED IN PLACE, and this is the part that makes it an item
  rather than an edit: `LampRingPadPx` IS SHARED WITH THE LAMP. Changing the
  pad rule changes the lantern's annulus too, and the lamp's lit reading and
  its whole night series were measured with the current one. A second copy of
  the arithmetic is the other obvious move and it is worse: a duplicated
  helper is the site nobody fixes.

  WHAT IS ALREADY TRUE AND KEEPS THIS HONEST MEANWHILE: both rectangles print
  in pixels on every figure line (`box=x..../y....` and `ring=x..../y....`),
  so the ring is re-derivable from the line rather than taken on trust, and
  the 14 to 1 is visible to anyone who reads it.
acceptance: the pad rule the figure uses is chosen from a PRINTED SERIES over
  real frames rather than inherited, and whichever way it falls the lamp's own
  annulus is either unchanged or re-measured with its night series re-read;
  and the key says which neighbourhood it is a statistic of
max_sessions: 1
status: READY 2026-09-16, filed and NOT started. The visual slice comes first.

  DO NOT SET THE PAD FROM AN ARGUMENT. There are no frames with a figure in
  them yet, so there is no series, and "pad by the shorter side" is a rule
  nobody has measured either. This item opens when the first figure frames
  exist.
