line: art (a reference below the resolution of the question asked of it)

spec: MEASURED 2026-09-21 by the director, on the sheet's own pixels, after
  three round trips were spent tuning a lamp against it.

  `production/art/atlas-01/concepts/hook.png` is 1024x1536. Its street lamp
  occupies a 25px-wide, 8px-tall head on a 4px pole. At a sky baseline of
  mean 207.0 sd 4.29 over 1600px (patch x280-320 y700-740, clear of the lamp)
  and a cut 4 sigma below it, the trace over rows y742..789, window x230..276
  which nothing touches, reads:

    pole            x=237..240, 4px wide, dead straight from y=759 down
    head plus neck  y=751..758, EIGHT ROWS
    widest row      y=755 and y=756, x=238..261, 24px
    rows with more than one segment   0 of 39 dark rows

  THE ASPECT MOVES WITH THE THRESHOLD AND THAT IS THE FINDING. Three traces of
  the same crop: 25x11px (2.27:1, the authoring builder), 23x7px (3.3:1, the
  recipe's own lcSheetRef line), 24x8px (3.0:1, the 4 sigma trace above). The
  head is 8 rows tall at 4 sigma and 11 at a looser cut. A 37 percent swing in
  the denominator moves the target from 2.27 to 3.3, and attempt 4 of the
  lighting column was authored to hit 2.279 within a plus or minus 25 percent
  band that exists only because the ruler is this unstable. TUNING AGAINST IT
  AGAIN WOULD SPEND A ROUND TRIP ON A NUMBER THE REFERENCE CANNOT SUPPLY.

  WHAT THE SHEET DOES SETTLE, and it is not a number: 0 of 39 rows enclose sky,
  so the reference is a KINK with the lantern hanging off it, never an arch
  with a bare arm and a dropper. Attempt 4's render encloses sky in 105 of 139
  dark rows and attempt 3's in 126 of 160. That comparison is threshold-robust
  and normaliser-free, and it is the one the sheet can still adjudicate.

  THE SECOND THING IT SETTLES IS SCALE, NORMALISED BY THE ONE LENGTH BOTH
  IMAGES PIN, canon's 0.114 m shaft: the sheet's head and neck are 6.0
  pole-diameters wide and 2.0 tall, against attempt 4's 6.80 and 2.98. Width
  13 percent over, height 49 percent over. Both are ratios of measured pixel
  counts to a measured pixel count in the same image, so neither inherits the
  sheet's uncertain absolute scale.

acceptance: the atlas-01 lamp reference resolves the question it is asked. Any
  one of these discharges it, cheapest first, and the choice is Jafar's
  because a concept sheet is approved art:

    1. A HIGHER-RESOLUTION CROP OR RE-RENDER of the same lamp from the same
       sheet's source, at a size where the head is at least 80px across, so a
       1px threshold difference moves the aspect by under 2 percent rather
       than 37. State the measured swing across two thresholds to prove it.
    2. A PERIOD PHOTOGRAPH on the licence allowlist, named in
       game-design/research/GOVERNS.md beside the lamp family, used as the form
       reference with the sheet keeping tone and dressing.
    3. A RULING that the sheet governs character only (kink not arch, lantern
       hanging off the pole, photocell on the ridge) and that the proportions
       come from the spec, in which case the recipe drops
       sheetTargetAspect and the tolerance band with it.

  Whichever is chosen, lcSheetRef must print the measured swing across at
  least two thresholds beside its confidence, so a later reader can see the
  ruler's own error without re-deriving it. A single number with a
  confidence word is what let three attempts chase it.

status: READY 2026-09-21. Filed and not chased in the session that found it,
  under rule 11. The lamp column itself is batch b006-lighting-column-01 in
  production/throughput.md, attempt 4 OPEN rather than rejected, and the
  question of whether to spend a fifth round trip on it is with Jafar on a
  card rather than being settled by the studio spending.
