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

## Round 3 (r3: the curtains solid)

- **Square on, from the right, from the left and across the road by day: PASS.** The curtains' folds are clean.
  - Listed: the solid cloth now shades the ring cake under it a little; the shop door's upper pane is mostly reflection by day; the kick plate reads brown where the design's is brass.
- **Across the road at night: FAIL** on two points.
  - **A, the black slot in the shop door's glass:** the design's own open point.
    - **Measured:** it is in the room picture itself. The counter stops 0.10 m short of the left wall, and the gap renders near-black (values 0 to 5 at its core, in the design's pictures and the PC's).
    - **Fix, try 1:** a filler of the counter's own base and top runs it to the wall (sw_shops_tea.py; the scene checks pass), and the room is rendered again.
  - **B, a burnt white sliver at the window's left edge:**
    - **The cause:** the window's light panel at its default place, the card's middle (27.0) and 3.7 m wide, has its end against the window's left return (26.30) and burns it. The same fault was Rita's second try of 21 October.
    - **Fix, try 1:** the panel over the window alone, as hers (spill_x 27.975, spill_width 2.6, just behind the glass).
  - The room's first re-render closed the counter's gap. A second, narrower dark gap stood above it, where the cup shelves stopped 0.10 m short of the wall, so the shelves now run to just clear of the wall and its dado rail (0.035 m; the scene checks pass), and the room was rendered a third time.

## Round 4 (r4: the counter and shelves to the wall, the window's light over the window)

- **Across the road at night:** both r3 faults fixed. The door's slot now reads about 16, the counter's shaded end, where it read 1 to 3; the window's left edge, 230 before, now reads about 60.
  - **A new fault, FAIL:** the door's number 14 on the fanlight went pale and ghostly (its digits 80 to 88 against a wall of 70 to 110; 35 before).
  - **The cause:** the number is see-through as the design exported it (glTF BLEND). Unreal lights a see-through surface from its light volume, which ignores the lighting channels that keep the window's light off the front. Once the light panel hung just behind the fanlight, it lit the number.
  - **Fix, try 1 of this fault:** the number written as a cut-out (front_for_game.py --mask=glass_row_20), lit as the front is; the front was imported again.
- **Square on at night: PASS.** The room and the curtains are lit but not burnt (curtains' top 1% at 240, nothing clipped); the curtain folds are smooth.
  - Listed: harder shadows than the design's, the cards dark under the lamp's orange.

## Round 5 (r5, the night set, taken 02:23 before the build machine's night run)

- **The number 14 reads dark and solid again:** its box's mean 65.6 against 90.6 in r4 and 62.9 in r3.
- **Across the road at night: PASS** (r5). The 14 is solid dark brown and reads the right way round, there is no slot in the door glass, and the window's left edge peaks at 241 with nothing clipped.
  - Listed: the kick plate reads brown, not the design's brass; the toplights show no ceiling tubes; the cornice strip on the slates.
- **From the left at night: FAIL** (r5). The window's last toplights showed black over the lit room.
  - **The cause:** the tea rooms' window stands at the bay's end, where the room's card ends (29.65). From a slant through its last toplights, the eye passes over the display's side linings (their tops 0.35 m under the window head) and beyond the card's end into nothing. Rita's and the newsagent's windows end inside their cards' width, so they show the room there.
  - **Fix, try 1:** the display's side linings run up to the window head, as a shopfitter's are (front_for_game.py --display --raise=return_plaster:0.45; their tops from 2.95 to 3.40 m).
- **From the right at night: FAIL** (r5). Saw-tooth vertical stripes (about every 20 px) crossed the hand-lettered window card hung on the glass; absent in r3.
  - **The cause:** they came with round 3's move of the window's light panel to just behind the glass, where it grazes the card. It is the light's own shadow map at a grazing angle.
  - **Fix, try 1 of that fault:** the panel casts no shadows (spill_shadows false, the option made for Rita's goods).
  - Listed: the window's left side wall is the brightest surface in that frame (239, not clipped); the fanlight's 14 reads faint from that slant against its dark glass.

## Round 6 (r6: the number solid, the linings to the head, the window light without shadows; every view retaken)

- **From the right at night: FAIL.** The window card's stripes are gone (their ripple 1.07 to 0.35), and the 14, the door glass and the window's ends are clean.
  - But two toplights over the middle light read near-black (means 8 and 13), there since r1 and not named before: from below at a slant the eye passes over the room's card into nothing.
- **From the left at night: FAIL.** The far toplights now show the raised lining (fixed), but the same two middle toplights stay black.
  - And with no shadows, the window's light reached through the party wall and lit the ironmonger's shut display (its crate 8 to 23, its tins 4 to 13).
- **Fixes:**
  - **The middle toplights:** the display gets a head board in its linings' plaster at their top, glass to card, as Rita's display has (front_for_game.py --head). This is try 1 of the middle-toplight fault, try 2 of the black-toplight fault from the left.
  - **The stripes and the leak:** shadows back on (the leak's cause removed), with the panel's own shadow bias and slope bias at 2.0 against the engine's 0.5 (spill_shadow_bias, spill_shadow_slope_bias; VignetteShot.cpp SpawnShopSpill; both game targets built). This is try 2 of the stripes fault.

## Round 7 (r7: shadows back with the bias, the head board at the linings' top)

- **Measured against r6:**
  - the ironmonger's display is dark again (9.7 to 3.9);
  - the window card is clean with shadows on, so the stripes' try 2 holds;
  - the middle toplights are still dark (about 10).
- **The cause of the last:** the board stood at the raised linings' top, 3.50 m above the crown, while the room's card stops at 3.05. A rising line through the toplights passes over the card's top and under the board, into the gap.
- **Try 2 of that fault:** the board at the card's own top (2.35 in the display's frame, whose bed is 0.70 above the crown). Its first placement (2.45, a frame misread) was rebuilt before any picture.

## Round 8 (r8: the head board at the room's top; the final state)

- **The middle toplights** show the head board (means 37 to 48 where they were about 10).
- **From the right at night: PASS.** The card is clean, the toplights show the board, and there is no slot.
  - Narrow point: a ragged shadow edge on the near chair's rail since the larger bias, reading as worn paint.
- **From the left at night:** both r6 faults are fixed (toplights 44 with nothing near-black; the ironmonger's display dark, 3.4).
  - The reviewer failed it on the depth of the shadows under the table and the cake stand, near-black with little fill.
  - That look is the window light's with shadows on: rounds 4 and 5 had it, and their reviewers listed it as a shortfall (square on at night r4, "hard chair and table shadows"; from the left r5, "hard light-and-shadow bands").
  - By the gate's rule (a known shortfall fails nothing alone) it passes with it listed. **Owed:** a soft fill light under the window head, shadowless, with a short reach so it cannot touch the next shop.
- **Across the road at night, square on at night, reverse, hook: PASS** (r8).
  - Across at night: the 14 solid, no slot, all nine toplights cream, both ends clean, nothing new clipped, the ironmonger's display unchanged.
  - Square at night: the card evenly lit, the curtains bright without burning.
  - Reverse: the front whole between the end house and the ironmonger's.
  - Hook: a sliver of the front behind the lamp post and the crates.
  - Narrow points listed: a ragged shadow edge on the near chair's rail; a fine stepped shadow edge on the right curtain; the cake stand's lower tier lit under the upper one.
- **The day views** (across the road, square on, from the left and from the right) passed in r3. Measured between r3 and r8, their differences are small:
  - across the road: a neighbouring roof's wet sheen at the frame's left edge, which varies between runs;
  - from the right: the wet pavement's sky reflection, and a little in the toplights, where the board now stands;
  - square on and from the left: means under 1 level, no large blocks.
  - So their r3 verdicts stand.
- **The gate's end: all ten views pass.** The last good pictures are r8's (F:/LedgerTools/gate/last-good/tea-rooms).
- **Listed:**
  - deep shadows under the table and cake stand at night (a soft, short-reach fill light owed);
  - the cornice above the low eave (one fix owed for the row's three fronts);
  - the kick plate brown, not brass;
  - no ceiling tubes in the toplights;
  - the street's downpipe at the corner.

## Its front's wear (w1, w2)

- **Made:** tools/art-recipes/front_wear.py with the passed settings and this front's own places (production/specs/shop-fronts/tea-rooms-front-wear.json): the door at the viewer's left, its handle, its rails, and the cream sill's nose. Paints: the brown, the cream and the dark brown side door.
- **w1:**
  - from the left, across the road and square on: PASS;
  - **from the right: FAIL.** The lock rail's chips ran round all four of its edges and joints, a dotted frame. On the ironmonger's and newsagent's this was a watch point.
  - **Across the road at night: FAIL** on the same frame, and on the sill's chips running in two unbroken rows its whole width (its nose and the window's bead), an even row.
  - **Fixes, try 1 of each:** no chips on the lock rail; the sill's chips on its nose alone, below the bead, by the door and at the far end.
- **w2: all ten views pass.**
  - by day: across the road, square on, from the left, from the right (the lock rail clean, the sill's chips in two sparse clusters, the grime soft-topped road dirt, the clean paint unshifted);
  - at night: across the road, square on, from the left, from the right;
  - the street's reverse and hook cameras.
- **Listed:**
  - the chips read grey-taupe rather than old wood, flat with no raised edge;
  - the plinth's grime leans cool grey and follows its moulding;
  - at night the wear barely shows under the lamp's orange.
- **The last good pictures** are now w2's (F:/LedgerTools/gate/last-good/tea-rooms). Preview: production/previews/tea-rooms-2026-10-23.jpg (day above, night below).
