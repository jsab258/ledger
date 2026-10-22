# The ironmonger's shop, the next family Rita's way: the gate (22 October 2026)

His message of 22 October: with item 7 blocked, Rita's night light, then the lamp's staining, then "the next shop family the same way as Rita's, since I've kept her front". The ironmonger's was chosen because its design passed both of the other team's reviews at try 2 (production/cloud-week/kit/shop-windows/REVIEW-ironmonger-v2-*.md), as did the newsagent's and the tea rooms'. It is also the nearest and largest of the three in the street's reverse view.

## What was built (Rita's way, 21 October)

- **The design's own build, on the PC.** production/cloud-week/kit/shop-windows/build_shop.py --shop ironmonger: assets, paper, front, display, then the room at 128 samples (day 8 min, night_lit 7 min, night_dark about 5 min).
- **For the game.** The front and the display were made ready by tools/art-recipes/front_for_game.py (15 panes recorded in production/specs/shop-fronts/ironmonger-front-glass.json). The room's three pictures sit on F: under production/art/shop-rooms/ironmonger-cloud_*.
- **The street.**
  - terrace-front.py CLOUD_FRONTS takes west_north bay 1, its first west front. A west bay is the same bay turned a half turn, so the front's frame maps as for Rita's.
  - The bay is no longer a metal refit: the design is a timber front.
  - The checks now count a cloud front's display pane on the west row.
  - The brick piers behind the end pilasters take the row's own brick (grey on the west).
  - The street was exported and imported again.
- **The shop file** (production/specs/shop-interiors.json, "ironmonger"):
  - side -1;
  - its card's decal is the street's own name for the bay's card (production/art/shop-rooms/ironmonger_day; the first picture had no front, because a new name matched nothing);
  - the front at street x 33.0, the display over the window zone x 30.35 to 33.70;
  - shut at night by the design (no window light, the night_dark picture).
- **The glass** baked again and fresh.
- **The page cameras.** They take -PageShop=ironmonger -PageShopX=32.0 -PageShopSide=-1; without the last two they framed Rita's shop.

## The gate, round 1 (F:/LedgerTools/gate/new/ironmonger-2026-10-22/r1)

- **Square on: PASS.** Every label reads right and is spelled right; the room reads as a real box behind the goods and matches the passed design. The near-black ends of the window match the design's own dark green.
- **Across the road: FAIL.** The KEYS CUT board's iron bracket stood on the roof. The design fixes it to brick above the cornice (plate 3.6 to 3.9 m), but this row is single-storey with its eave at 3.4 m.
  - **Fix, try 1:** the plate on the door-end pilaster's capital (2.55 to 2.85 m), the arm at 2.70, a short drop, the board's foot at 2.22 m. It is in the design's own script, keyed by shop (sw_front.py PC_SIGN_MOUNT; the target is not edited). The front was rebuilt.

## Round 2 (r2)

- **From the left: PASS.** The joins are tight, the board's plate is on the capital, and every display item is on its bed.
- **Across the road: FAIL** on a new fault: small dark blocks stood up through the gutter at both ends of the front.
  - **The cause:** the brick piers behind the end pilasters, made for Rita's two-storey row, rise to 3.60 m, through this row's 3.4 m eave.
  - **Fix, try 1:** the piers stop just under each row's own eave; Rita's (eave 6.2 m) are unchanged. The blocks are gone in the next pictures.

## Round 3 (r3)

- **Across the road: PASS.** The board hangs from the capital, the gutter is clear, the joins are closed and the lettering is right. Points to watch:
  - a faint green sliver, 1 to 2 px, at the gutter's lip above each end pilaster;
  - the cornice lost in the eave's shadow;
  - a plainer bracket than the design's.
- **From the right: PASS.** The room narrows truly towards the eye and nothing slides. Seen in the frame, not the shop's: a cast member in the white base layer stands on the tea room's pavement although people are hidden (the clothes fault, listed; the hide flag misses the cast at their posts).
- **Square on at night: PASS.** A dark, shut window lit only by the street; nothing shines. The display reads darker against the room than in the design.
- **Across the road at night: FAIL.** The door's card read OPEN on a shut shop; the design's passed night picture shows CLOSED.
  - **The cause:** the design turns the card over for a shut shop's night picture (sw_gate.py), but in the game the front is one fixed model and its card was always OPEN. Rita's has the same fault: she shuts at 5.30.
  - **Fix, try 1:**
    - each cloud front's "door_sign" slot becomes swappable;
    - the CLOSED face (the design's K03b_A) is named by the shop file and staged into the packaged copy;
    - ReDriveShopInteriors shows it at night unless the shop is open_at_night (VignetteShot.cpp).
  
  Both game targets were built. Rita's night views are retaken with it.

## Round 4 (r4: the card turns at night; glass baked again)

- **Rita's two night views: PASS.** Her card reads CLOSED, dark red, where OPEN was; nothing else of hers moved. Her last good night pictures are now these.
- **Reverse by day: PASS.** The plain maroon front is replaced by the design; the lettering is right, the joins and the gutter are clean.
- **Across the road at night: FAIL.** The CLOSED card read as a pale, almost white tag (red:green 1.8; the design's card 4.7; Rita's in the game 4.65).
  - **Measured:** the OPEN face at night in r3 read the same pale warm colour (1.46), whichever face it showed.
  - **The cause:** the card's material was see-through (glTF BLEND, as the design exported it). In a dark shop the room's picture behind it glows through and outshines the card's own colour; in Rita's lit shop it does not show.
  - **Fix, try 2 of the night-card fault:** the card written as cut-out (glTF MASK at 0.5) by tools/art-recipes/front_for_game.py cut_out_cards, also on Rita's fronts and in front_wear.py. Both fronts were imported again.

## Round 5 (r5: the cards cut-out)

- **Across the road at night: PASS.** The card reads CLOSED, solid red with pale letters (red:green 4.37 against the design's 4.7); a shut, dark shop; only the card changed since r4.
- **Rita's two night views: PASS.** Her card reads CLOSED the right way round, lit from the street, as faint as the gilt hours beside it. Her last good night pictures are now these.
- **Hook by day: FAIL.** The ironmonger's strip is clean: the board hangs from the capital, the roof is untouched. But Rita's card, about 5 x 10 px from this camera, washed out to grey by day (its greenest pixel 126,133,109 against 62,102,73 before). Up close by day it reads OPEN, green and sharp.
  - **The cause:** the cut-out (MASK) at a few pixels' size.
  - **Fix, try 1 of this new fault:** the card written OPAQUE. Its picture is transparent only at the corners and the hole (293 of 88,000 pixels), which carry the card's own colour. Both fronts were imported again.

## Round 6 and 7 (the card opaque; then satin)

- **Opaque card (r6), measured.** At night the cards read as in r5 (his red:green 4.37, Rita's 7.09). By day, up close, they read OPEN, green. From the hook camera, Rita's card is still grey (its greenest pixel 128,135,111).
- **Satin card, try 2 (r7):** roughness 0.7 changed nothing at the hook (129,136,113). So it is not the card's own gloss. It is the door glass's reflection over a card now drawn behind it as a solid; the see-through card had been drawn over the glass.
- **Set aside after two tries and listed.** Rita's door card, a few pixels wide from the hook camera, reads as a grey smudge behind its glass by day; up close it reads OPEN.
- **Kept:** the cards opaque (they fixed the night); the satin undone (the design's roughness 0.35).

**The gate's end: all eight views pass.**
- Square on (r1), from the left (r2), from the right (r3), across the road (r3), square on at night (r3), reverse (r4), across the road at night (r5).
- Hook by day: the ironmonger's strip clean; its one fault, Rita's card at that distance, is listed above, so by the gate's rule it fails nothing alone.
- **The last good pictures** are in F:/LedgerTools/gate/last-good/ironmonger. Preview: production/previews/ironmonger-2026-10-22.jpg (day above, night below).
- **Owed, Rita's way:** the wear on his front (the design's W1 for every front).
