# The newsagent's shop, the next family after the ironmonger's: the gate (22 October 2026)

His message of 22 October: with item 7 blocked, Rita's night light, then the lamp's staining, then "the next shop family the same way as Rita's". After the ironmonger's, the newsagent's (west_north bay 0, no. 18) was chosen. Of the three designs that passed the other team's reviews, the tea rooms' carries an unfixed black slot through its door glass at night, cause not found. The newsagent's only open point was two old carton names in its 48-sample room pictures; the PC's 128-sample render replaces them.

## What was built (the ironmonger's way)

- **The design's own build, on the PC:** production/cloud-week/kit/shop-windows/build_shop.py --shop newsagent: assets, paper, front, display, then the room at 128 samples (22 min).
  - The printed goods needed Poly Haven's photographs fetched first (sw_prints.fetch_sources). Its build script did not call it.
  - **The room's words were read at full size.** The gantry's packs read BRANSTONE, MARSDEN, RAVENSDALE, SELWYN, DEVEREUX, WYNDHAM, HOLLINGWORTH, WYNYARD, TOWNLEY, RIVERMEAD, AVONLEA and ALDERLEY. The two old names that echoed real lager brands are gone from the pictures and their records.
- **For the game:** tools/art-recipes/front_for_game.py made the front and display ready, with the front's 19 panes recorded in production/specs/shop-fronts/newsagent-front-glass.json. The room's three pictures sit on F: under production/art/shop-rooms/newsagent-cloud_*.
- **Its lit box sign** (the target's 4.1 `lit: tubes`; the design lights the sign's face with the board's own emissive map at night, sw_gate.py, and its glb is the day state, PC-NA1):
  - front_for_game.py --night-glow puts that map into the front's glb as the fascia's emissive texture with a factor of 0.
  - The game sets the factor after dark (VignetteShot.cpp, the front's "night_glow"; first strength 0.7, the room's own night brightness).
  - Both game targets were built.
- **The street:**
  - terrace-front.py CLOUD_FRONTS takes west_north bay 0.
  - The self-test's check that the west bays run back down the street counts a cloud front's display pane where a bay has no fascia band of the recipe's.
  - The street was exported and imported again, and the glass baked again.
- **The shop file:** side -1; the street's own card name (newsagent_day); the front at street x 39.0; the display over x 36.35 to 39.70. It is lit at night by its design but shut at 5.30, so its card reads CLOSED.

## Round 1 (F:/LedgerTools/gate/new/newsagent-2026-10-22/r1)

- **Across the road by day: PASS.**
  - The front sits whole in the bay; both joins are closed; every word reads right.
  - The room lines up across all three lights, and the display is as the design has it.
  - Narrow points: the cornice is lost in the eave's shadow (the low row, as the ironmonger's); a faint shade step on each pilaster panel; the grey a little lighter than the design's.
- **Across the road at night: PASS.**
  - The box sign is lit, neither dead nor blown out (its red 215/88/68, 0.1% clipped, the letters readable). The lit room and display are in place, and the CLOSED card is red and legible.
  - Listed: the street lamp floods the front orange (as it did the old cream front); the door's pale hours fade against the lit room.
- **Square on by day: FAIL.** A greyer mottled band with a hard top edge round the right window post's foot and across the sill.
- **From the left by day: FAIL** on two points:
  - a hard-edged patch of grey vertical streaks on the stallriser;
  - a smeared, barcode-like strip, full height, at the left join.
- **Measured** (the game run once with the street's wear file moved aside; F:/LedgerTools/gate/new/newsagent-2026-10-22/nowear-test). Without it, the sill and the window post are clean, but the stallriser's patch stays.
  - **The band on the sill and post** is the street's wear layer (production/specs/street-wear.json): its splash and damp bands, placed for the bay's old joinery.
  - **The stallriser's patch** is the old scene's moss stain at the old front's foot (vignette-pieces decal_08_Moss001, x 37.95 to 38.85, 0.1 to 0.8 m up), a projected decal like the rest.
  - **The strip at the left join** is not a decal. Two brick piers overlap there, the ironmonger's behind its right pilaster and the newsagent's behind its left one, each reaching 60 mm past the bay's edge. Their faces lie in one plane and fight.
- **Fix, try 1 of each:**
  - **No street decals on the front.** The front's entry says "street_decals": false and the game turns decals off on its mesh (VignetteShot.cpp SpawnShopFront). Its wear is baked into its own paints, as Rita's and the ironmonger's are.
    - Rita's and the ironmonger's fronts still take the street's decals, since their gates passed that way (listed: one rule for the family to settle).
  - **The piers:** where the neighbour is a cloud front too, a pier stops at the bay's edge (terrace-front.py _cloud_shopfront). The two now meet at x 36.0; Rita's are unchanged.

## Round 2 (r2: no street decals on the front; the piers trimmed)

- **The strip at the left join, measured:** it stayed after the piers were trimmed. It is the street's own lead downpipe at the bay's edge (west_north_downpipe_bay0, x 36.00 to 36.07), whose 56 mm wide faces sample a thin slice of its texture and read as horizontal bands. It stood there before this front, unchanged; listed. The trimmed piers stay, since two overlapping coplanar faces are wrong anyway.
- **All ten views pass fresh reviewers:**
  - square on and from the left: the grime band, the moss patch and the sill's grime gone;
  - from the right;
  - across the road by day and at night: only the front's own surfaces changed against r1;
  - square on, from the left and from the right at night: the sign lit, red, nothing clipped, the card CLOSED;
  - reverse: the front out of frame, nothing else moved;
  - hook: a few pixels, the red sign under the gutter, nothing else moved.
- **Listed:**
  - the street lamp burns the pale front orange at night (as it did the old cream front);
  - the dove grey reads paler than the design's under the street's light;
  - the design's cornice is lost under the low row's eave (as the ironmonger's);
  - a hard horizontal step in the glass's reflection (the street's glass; the ironmonger's shows it too);
  - the door's pale hours fade against the lit room at night;
  - the downpipe;
  - the street's pale open end beyond the row.
- **The front reads showroom-clean without the street's grime;** its own wear is the next step (w1).
- **The last good pictures** are in F:/LedgerTools/gate/last-good/newsagent.
