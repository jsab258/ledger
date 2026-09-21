line: instruments (a comment that claims a check the code does not do)
spec: FOUND 2026-09-21 by a builder wiring the setts surface, and confirmed by
  the resident: `grep -c VARIANTS tools/citypack/pack_check.py` returns 1, and
  that one hit is the assignment itself. NOTHING READS IT.

  ITS COMMENT CLAIMS OTHERWISE: "Checked for shape when present, never
  required." The first half is false today. A variant file could be any size,
  any shape, or corrupt, and this checker would pass the pack without a word,
  while its own text tells a reader that it looked.

  THAT IS THE SIGNATURE FAULT OF THIS PROJECT, one layer along from the one the
  same evening found in `content-gate.py`: an instrument whose SCOPE is
  narrower than its DESCRIPTION, so a reader trusts a check that never ran. The
  difference here is that no measurement is wrong; the claim about the
  measurement is.

  THE WORK IS ALREADY DONE ONCE. The same builder refactored the per-surface
  body of `audit()` into `inspect(logical, textures, found, sizes)` so that the
  new OPTIONAL list is checked by the SAME code as a required surface. Routing
  the variants through that same function is the fix, and the builder measured
  in advance that it would be green today: the five variant albedos and their
  ten `_n` and `_r` maps are all power of two (2048x2048, with brick_grey_b at
  2048x1024) between 1.4 and 8.3 MB, read with the tool's own `dimensions()`.

  SO THIS IS NOT A HUNT, IT IS ONE ROUTING LINE plus the denominator it should
  print. The builder left it deliberately under rule 11, one system per brief.
acceptance: the variants are walked by the same function that walks a required
  surface, with their count printed as a denominator on a clean run so a zero
  can be told from a never-walked; a planted broken variant is REFUSED, tested
  as the rejecting case with the accepting case first; and the comment is
  rewritten to describe what the code then actually does
max_sessions: 1
status: READY 2026-09-21. Instrument work under D45: a test, no review, no
  ruling record.

  IT IS NOT URGENT AND IT IS NOT NOTHING. Nothing is broken today, measured
  rather than hoped: every variant on disk would pass. What is wrong is that
  the pack could acquire a broken variant tomorrow and the checker would say
  the pack is fine, which is the state this item closes.
