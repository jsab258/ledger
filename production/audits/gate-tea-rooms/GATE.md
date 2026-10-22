# The tea rooms, the third of the west row's shops: the gate (23 October 2026)

His message of 22 October: "the next shop family the same way as Rita's". After the ironmonger's and the newsagent's, the tea rooms' (west_north bay 2, no. 14) is the last of the three designs that passed the other team's reviews. That team left one open point: a black slot through its shop door's glass at night, cause not found.

## What was built (the newsagent's way)

- **The design's own build, on the PC:** build_shop.py --shop tea_rooms: assets, paper, front and display, then the room at 128 samples (24 min). The furniture is full size, as the design's second try fixed it.
- **For the game:**
  - front_for_game.py made the front ready (16 panes, production/specs/shop-fronts/tea-rooms-front-glass.json) and the display.
  - The room's three pictures went to production/art/shop-rooms/tea-rooms-cloud_*.
  - Its sign is painted, so it has no night glow.
- **The street:**
  - CLOUD_FRONTS takes west_north bay 2. Every bay of the west row is now a cloud front.
  - Three self-test checks assumed the row's own shopfront parts. They now count a cloud front's display pane and door glass as its shopfront and door, and every cloud front as a timber front.
  - Exported and imported again; the glass baked again.
- **The shop file:**
  - side -1; the street's own card name (tea_room_day); the front at street x 27.0;
  - no street decals, as the newsagent's;
  - lit at night and open to 22:00, so its card reads OPEN at night (open_at_night).

## Round 1 (F:/LedgerTools/gate/new/tea-rooms-2026-10-23/r1)

- **Across the road by day: FAIL.**
  - **The display stood about 1.95 m left of its window.** The window card, curtain and cake were in the left light, and the table showed behind the shop door's glass.
  - **A near-black band ran down the right light's right edge.**
  - **The cause:** the tea rooms' doors stand at the viewer's left, so its window zone is u 2300 to 5650 (street x 26.30 to 29.65; sw_ctx zones). The shop file took the newsagent's zone, u 350 to 3700, copied with the entry. The band is the window's end with no display return wall standing there.
  - The page cameras had the same error: -PageShopX=26.0 aimed at the wrong window middle.
  - **Fix, try 1:** the display at x 26.30 to 29.65 and the cameras at the window's middle, 27.98. The glass was baked again and every view retaken. The square-on review of the first pictures was stopped as void.

## Round 2 (r2: the display in its window, the cameras at its middle)

- **Across the road by day:** the reviewer found both r1 faults gone; the display, room, sign and joins match the design.
  - It failed the view on one point: the cornice cuts through the eaves, its top a 2 to 3 px tan strip on the slates, and the cornice band is hidden behind the gutter.
  - **It is not new.** The design's cornice tops out at 3.55 m and this single-storey row's eave is at 3.4 m. The ironmonger's gate listed it (r3: a sliver at the gutter's lip, the cornice lost in the eave's shadow), and so did the newsagent's (r2: the cornice lost under the low row's eave). It shows more here because the cornice is light tan.
  - My brief left it out of the known list; it is added for the remaining views.
  - By the gate's rule (a known shortfall fails nothing alone), the view passes with it listed. **Owed, one fix for all three west fronts:** cut each front just under the row's eave and re-gate their across views.
- **Square on by day: FAIL.** The display sits right: table, chairs, cakes, plant and lettering all as the design has them, and the room reads as a box. But dark saw-tooth triangles ran down the café curtains' fold ridges on both sides.
  - **Measured:** the curtains are dense (18,172 and 16,860 faces) with consistent, smooth normals, so the cause is not coarse geometry.
  - **The cause:** the design gives the cloth half transmission (KHR_materials_transmission 0.5). The game draws that see-through, and a folded see-through sheet's triangles are not sorted by depth, so back folds draw over front ones.
  - **Fix, try 1:** front_for_game.py --display writes the curtain solid (SOLID_CLOTH, solid_cloth). The display was imported again and every view retaken (r3).
