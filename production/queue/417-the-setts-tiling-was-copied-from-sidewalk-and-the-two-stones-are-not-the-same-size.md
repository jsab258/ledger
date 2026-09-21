line: instruments (a number copied from a neighbour rather than measured)
spec: FOUND 2026-09-21 by the resident, looking at the shipped pack after the
  setts fetch landed at 1cebc0b6. `AssetLibrary.cs:1618` gives
  `AssetLibrary.Setts` a tiling of `new Vector2(8,8)`, which is EXACTLY what
  `AssetLibrary.Sidewalk` uses at :1588. It was copied when the surface was
  wired, and labelled as copied at the time, because no measurement existed.

  THERE IS NOW EVIDENCE IT SHOULD NOT BE THE SAME NUMBER. Both textures are
  2048x2048 and both came out of ambientCG's PavingStones category, but they
  are not the same stone. Cropped at the same fraction and viewed in one
  picture at one scale, setts.jpg (PavingStones115B) shows large rectangular
  dressed blocks in regular courses, and sidewalk.jpg (PavingStones067) shows
  smaller squarer blocks with moss in the joints: roughly two to three times
  the linear block size between them, by eye. At identical tiling that ratio
  goes straight into the frame.

  LOOKING IS WHY THIS ITEM EXISTS AND IT IS NOT ENOUGH TO CLOSE IT (rule 4: a
  picture is strong evidence that something is wrong and weak evidence of what
  or why). The number this needs is metres per texture tile, and it CANNOT be
  read here: `tools/citypack/catalogue.json` records only `id` and `sizes` per
  asset, with no physical dimension, and ambientCG's own asset page, which
  publishes one, is blocked from this container.

  IT MAY ALSO TURN OUT TO BE RIGHT. A real British street does lay a coarser
  block on the carriageway than on the footway, so a larger sett than paving
  slab is not automatically wrong. What is wrong today is that nobody measured
  it either way and the number arrived by copying.
acceptance: a metres-per-tile figure for setts, derived rather than copied, by
  either route: read ambientCG's published physical size for PavingStones115B
  and PavingStones067 through CI or the PC, where the host is reachable, and
  set the tiling from the ratio; OR render the street with an object of known
  dimension standing on the setts (the pack already relies on a 3.00 m lamp
  post and a 0.10 m manhole as scale references, `StreetVignette.cs:1512`) and
  measure the apparent block size against it. Whichever route, the printed
  number and its source go in the comment beside the tiling, replacing the
  words that currently say it was copied. If the answer is that 8,8 was right,
  the comment says so and names the measurement, because a number that happens
  to be correct and a number nobody checked look identical in the file.
status: READY 2026-09-21. Blocked on nothing here; the ambientCG half needs a
  reachable host, the render half needs a run. Not chased in the session that
  found it, under CLAUDE.md rule 11.
