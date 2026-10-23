# The grocer's, the parade's next shop: the gate (23 October 2026)

His message of 22 October: "the next shop family the same way as Rita's". The west row's three passed designs are in. Of the other team's remaining shops, each passed its street review and failed its close review on one fault:
- the chandler's: sou'westers that read as hard hats;
- the fish market's: no fish, which waits on scans behind his Fab sign-in;
- the launderette's: a powder named like a real firm;
- the grocer's: scripted tomatoes that read as plastic toys, which its own target says to set aside.

The grocer's (east_parade bay 5, no. 11) is the simplest, and it stands on the parade, where the hook camera looks.

## What was built

- **The close review's fault fixed in the design's own script** (sw_shops_grocer.py): the tomatoes are set aside. Their tray holds the scanned onion at its real size (the target's DSP-06), under its own card, SPANISH ONIONS 22p. The other narrow points (flat supports, wide tins) are listed, not changed.
- **Built on the PC:** assets, paper, front, display; the room at 128 samples (24 min).
- **The tea rooms' lessons applied from the start:**
  - the glass lettering cut-out (--mask);
  - the display's linings to the head and a head board at the room's top (--raise, --head);
  - the window's light over the window alone, just behind the glass, its shadows kept with a larger bias;
  - no street decals.
- **The street:** CLOUD_FRONTS takes east_parade bay 5. Its self-test learned two things:
  - a recessed lobby's door glass stands up to 0.8 m back;
  - a cloud front may have no side door. The grocer's has none, and the parade's spec names this bay as its one without.
- **The shop file:**
  - side +1; the street's own card name (int23_grocer);
  - the display over the window zone, street x 33.35 to 37.644;
  - the front at x 36.0;
  - lit at night, shut at 5.30, so its card reads CLOSED.

## Round 1 (F:/LedgerTools/gate/new/grocer-2026-10-23/r1)

- **Across the road by day: FAIL.** The joins, door, lobby, glass, room and display are right, and the onions read as real. But the glass fascia read pale grey, not bottle green (175,183,178 against the design's 42,58,53).
  - **The cause:** it came in nearly a mirror (roughness about 0.13), and from below it catches the overcast sky.
  - **Fix, try 1:** the fascia dulled to satin, not metal, roughness 0.45 (front_for_game.py --dull).
- **Square on by day: FAIL.** The room is a true box, and every card is spelled right and stands before its goods. But the third bread roll floated in the air beside the basket's lid.
  - **The cause:** the basket model's lid leans on its right side, and the rolls were set at the lid's top, not the rim.
  - **Fix, try 1:** the lid left out; the rolls across the basket's rims at its own height, as the target asks.
  - The reviewer also judged the jars glossy and plastic-looking, as in the design; listed.

## Rounds 2 and 3 (r2: the satin fascia; r3: the lid left out)

- **Measured, not reviewed:**
  - At satin 0.45 the fascia reads greener but still pale grey-green from below.
  - With the lid gone, the third roll stood in the air beside the rim. The rolls model is a fixed row of three, 0.36 m long, and the basket only 0.21 across, so no rim can hold all three.
- **Try 2 of each fault:**
  - **The fascia:** near-matte (roughness 0.8), with its specular reflectance cut to 0.2 (KHR_materials_specular; front_for_game.py --dull=fascia_grocer:0.8:0.2).
  - **The rolls:** the basket left out; the row lies on a low deal board on the bed, between the apples and the lemons, every roll on wood.

## Round 4 (r4: the fascia near-matte, the rolls on a board)

- **Across the road by day:** the fascia reads bottle green (51,78,62 against the design's 42,57,53), and the rolls rest on their board.
  - **A new fault, FAIL:** FAMILY GROCER's last R was cut straight at its right edge. It was there in r1 too, hidden by the grey glare.
  - **The cause:** in the sign's own picture, built by the design's fascia generator on this PC. Each block's letters are drawn on a canvas 24 mm wider than the block's box. On this machine the word runs a little wider than where the box was measured, so the R ran off the canvas.
  - **Fix, try 1:** the canvas's margin 80 mm (production/cloud-week/2d/fascias/fascia_paint.py text_layers). The sign was rebuilt with the R whole, the front rebuilt and imported, every view retaken (r5).

## Round 5 (r5: the R whole)

- **Across the road by day: PASS.** The last R is whole (26 px against the first R's 25), clear of the fascia's panel joint. No new fault.
  - Narrow points, not failing: FAMILY GROCER sits about 4.5 px right of the fascia's centre; the rolls are small pale lumps at this distance.
- **Square on by day:** passed on r4; r4 to r5 differs only at the R, so the pass stands.
- **From the left by day: FAIL.** A grey smoke trails up and to the left of the jar lids on the jar step, over the dark room behind (x 1300 to 1580, y 925 to 1010).
  - **Measured:** it is in r1, r4 and r5 alike, so it is steady, not a run's chance; faintly in the square view too, straight up there; not at night, where the room behind is lit.
  - The lids are gold metal (metallic 0.8, roughness 0.35); the jars have no see-through material, and nothing of the display stands behind them, only the room's unlit picture.
  - Three short launches, one setting off in each (F:/LedgerTools/gate/new/grocer-2026-10-23/smoke-test): with the anti-aliasing off, and with bloom off, the smoke stays; with see-through surfaces hidden (the window's glass), it is gone and the lids are crisp. So it is drawn on the glass, in its reflection, not on the jars.
  - Four more launches, the glass kept: Lumen's live reflection on the glass (its front layer) off, its screen traces off, the translucency lighting volume off, and its reprojection off: the smoke stays in each. The glass's baked street picture at strength 0: gone.
  - **The cause:** each window's street picture is caught half a metre out from the pane with the pane hidden, so it also sees in through the pane at a slant; the grocer's shows its own display just past the street half (F:/LedgerTools/game-inputs/glass-bake/day/street_glass_eg_bay5.hdr), and the glass's slanting lookup reached the brightest goods there, the sunlit lids.
  - **Fix, try 1:** every catch leaves out each shop part wholly behind its pane (VignetteShot.cpp MakeGlassCapture), and the glass was baked again.
- **Its wear, in the same round:** the front worn the west row's way (production/specs/shop-fronts/grocer-front-wear.json): dirt and splash at the foot of the cream and the green slab, grime round the door's pull, chips on the cream plinths alone (a chip region may now name its paints).
  - The bake's first try made the bronze flat brown: front_wear bakes colour and roughness and writes a paint non-metallic, so the bronze (metallic 0.9) lost its metal. The bronze is left clean (try 2).
- Every view retaken as r6, with the night views and the street's two cameras, which r5 did not reach.
- **From the right by day: PASS.** No new fault; the shop is pixel for pixel r4's, the glass's reflected roofs aside.
  - Narrow points, not failing: a soft white streak over the near apples (the glass's reflection; gone without the glass); the room's ceiling tubes grey by day.
  - Design-level points for its makers, not faults: COOKERS on red apples, where a 1990 grocer would show green Bramleys; the lemons stand on end.

## Round 6 (r6: the catch leaving out what stands behind each pane; the wear)

- **Measured before review:** the grocer's catch left out 1 part where its neighbours' left out 7 or 8, and its day cube still held its own display.
  - **The cause:** its glass row holds the lobby's door glass too, 0.6 m back, so the row's middle stood 0.3 m behind the window, and the display, flush with the window, counted as in front.
  - **Fix, try 2 (the last under the two-tries rule):** the pane's plane is its street face, not its middle. Rebaked and every view retaken as r7; r6 not reviewed.
- **The wear, seen in r6:** chips on the left plinth, a dirtier right plinth, the green slab still green with a darker foot.

## Round 7 (r7: the pane's street face; every view retaken)

- **Measured before review:** the grocer's catch now leaves out 8 parts, as its neighbours' do, and its day cube holds no goods of its own.
- **But the smoke is still on the lids** in the left view (crop unchanged against r5). So the jars in the stored picture were not its cause: try 2 failed too.
- **Set aside** under the two-tries rule, and named in FINDINGS.md (the glass line) and the day's summary. What is known:
  - It needs the glass's stored reflection: gone with its strength at 0.
  - It stays with anti-aliasing, bloom, Lumen's front layer, its screen traces, the translucency volume and its reprojection each off, and with the jars left out of the picture.
  - Next, research in another direction: a GPU capture of the glass's draw and the frame's later passes, not another setting.
- **Kept, though it did not cure the smoke:** every catch leaves out the shop parts wholly behind its pane. A reflection holds only what is in front of the glass, and the street cameras are reviewed with it in this round.
- The brief now lists the smoke as a known shortfall. Ten views are reviewed, one reviewer each.
- **Across the road by day (r7): PASS.** The wear reads as real weathering: chips on the plinths' edges and mouldings (18% of the left plinth), splash on the lobby cheek thinning out about 0.6 m up, and a soft dust band about 15 cm high at the stallriser's foot. Nothing brighter anywhere. The glass is 0.65 levels from r5 on average. No new fault.
- **Square on by day (r7): PASS.** No wear in shot (the frame ends at the clean bronze sill). The glass is unchanged against r5 (PSNR 48.8 dB). The jar smoke is faint here, within 0.3 of a level of r5. No new fault.
- **From the left by day (r7): FAIL**, on a fault the earlier rounds missed. The hours lettering (MON-SAT 8-5.30 / WED 8-1 / SUN CLOSED) hung in the air at the lobby's mouth, at the front's plane, 0.56 m in front of the door that carries its OPEN card. It reads as lettering on the lobby's cream cheek, where the design has none.
  - **The cause:** in the front builder (production/cloud-week/kit/shop-windows/sw_front.py make_glass_rows), a shop whose hours row was made like Rita's took her plate's depth, 39 mm, after the lobby's depth was taken off. Her door is flush with the frame; the grocer's stands 0.6 m back. Only the grocer and the launderette have recessed lobbies.
  - **Fix, try 1:** the plate stands 39 mm behind the door's own glass (39 - lobby depth). The front was rebuilt, readied (--mask, --dull) and worn again; the plate now sits at 0.561 m, on the door's lower pane.
  - **Also, a narrow point fixed:** the left plinth's chip region took in the lobby's cheek, flecked evenly to a level top 0.6 m up. It now stops at the plinth (-2.655 m), and the cheek keeps its dirt and splash.
  - The wear itself reads as real chipped paint and street dirt. The glass is unchanged against r5, the jar smoke aside (set aside).
- **From the right by day (r7): PASS.** The right plinth's chips sit on its arrises and tiers, and the stallriser's foot has a soft dirt wash across the slab joint. The middle and right lights' reflection is one softer roofline where r5 overlaid two. No goods in the reflection, no smoke here. No new fault.
  - Narrow points, not failing: the reflected roofline's stair-steps are plainer now the overlay is gone (the same steps); a faint haze above it, 3% darker.
- **The street's reverse camera (r7): PASS.** The grocer's lies just out of frame. Other windows' glass is the same or slightly cleaner (the fish shop's panes no longer grey in their lower half, its own goods now left out of its picture). No new fault.

## Round 8 (r8: the hours plate on the door; the cheek's chips gone)

- **Measured against r7:** the hours plate stands on the door's lower pane behind its glass, below the OPEN card, in both views that see the lobby. The cheek is clean cream, with its foot dirt.
  - Square on: identical to r7 (no tile over noise), so its pass stands.
  - From the right: the shop is unchanged. Only the glass's reflected roofline differs, back to r5's overlaid layers (a run-to-run change already passed in r5), so its pass stands.
- **The street's hook camera (r7): PASS.** The grocer's sits cleanly in the parade, lettering the right way round; the lobby is hidden here, so r8's change cannot show. Mickey's, the fish shop's and Rita's glass reflect a little differently since every window was caught again, and none is worse. No new fault.
- **From the left by day (r8): PASS.** The floating hours are gone from the cheek, which reads as a plain painted panel with a little grime at its foot. The plinth keeps its chips. No new fault.
- **Across the road by day (r8): PASS.** The hours stand wholly within the door's glass, centred under the OPEN card, the right way round, veiled as lettering behind glass is, not glowing. The cheek's dots and the floating plate's shadow are gone. No new fault.
- **Across the road at night (r8): PASS.** Lit and shut by its design: the room and display lit, a soft warm pool on the pavement fading to the kerb, nothing blown, the door card CLOSED, the hours on the door's lower pane. The wear shows only when brightened. No new fault.
  - Narrow point, not failing: the CLOSED card is dim at night (its letters about 30 to 36 on a card of 15), the right word but only a dim red tag at full size.
  - Known: the street lamps' orange on the cream and the green (the stallriser near black); the room lit brighter than the design's night render, not clipping.
- **Square on at night (r8): PASS.** The room and display lit as designed, the glass near invisible but for a faint reflected lamp column, nothing clipped, soft shadows with no saw-tooth or stripes, the rolls all on their board. No new fault.
- **From the left at night (r8): PASS.** The room and display lit and clear, nothing blown, the lobby's cheek clean, the r1 floating hours gone, the glass unchanged against r1. No new fault.
  - Narrow points, not failing: the tins' facets show more under the night light's hard shadows (with the known wide tins); pinkish smears under the room picture's crates.
- **From the right at night (r8): FAIL.** The left tin pyramid shows hard vertical stripes under the window's night light (x 240 to 800, y 620 to 1150; a jump from 51 to 154 in one pixel along a label at row 690). By day the same tins step by 10 to 18 and read smooth. The design's night render shades them softly, so this is worse than the design.
  - **The cause:** the design's tins are 16-sided and flat-shaded (food_tin_labels and tin_metal, 2,581 and 15,888 flat faces in its own glb). Under strong, hard light each face reads as its own stripe.
  - **Fix, try 1:** the display readied with its tins smoothed by angle (front_for_game.py --smooth=food_tin_labels,tin_metal). Each corner takes the mean normal of the tin faces meeting at its point within 30 degrees, so the sides round and the rims stay sharp. 32,256 of 56,448 tin corners now carry rounded normals; every other part keeps its own.
  - Every view retaken as r9.

## Round 9 (r9: the tins smoothed)

- **Measured against r8:** the tins read round under the night light; the night views changed most, the day views little (1 to 16 tiles of 80 px over 20 levels).
- **One change not of this round's making:** in the day view from the right, a dark speckled wedge on the launderette's left pilaster (about x 1930 to 1950, y 400 to 1100). In r1 to r8 the strip read as brick and cream (mean 130,119,95); in r9 it is 96,88,71. Nothing near it changed. It reads as a shadow that varies from run to run, so the day views are taken again after the west row's eaves round, before they are reviewed.
- The night views are reviewed on r9, one reviewer each.
- **From the left at night (r9): PASS.** The tins on all three pyramids now shade smoothly from lit to shadowed side and read round, closer to the design's night render. There is no seam, label line, dark facet or ring, and the rims stay sharp. Everything else is run noise. No new fault.
- **From the right at night (r9): PASS.** The fault is gone. At row 690 the label now rises smoothly, 39 to 221 over 30 px, where r8 jumped 54 to 162 in one pixel. The facet lines are gone from every tin on all three pyramids, the rims stay crisp, and brightness is unchanged elsewhere. No new fault.
  - Narrow points, not failing: the tins' outlines still 16-sided at 4x zoom; the lids charcoal where the design's night render shows them light grey.
- **Square on at night (r9): PASS.** Only the three pyramids changed: their stripes are gone (a stripe measure fell 3.24 to 2.64, 2.51 to 2.33 and 3.61 to 3.04, the rest being lettering and edges). The rims stay crisp, and everything else is at noise level. No new fault.
- **Across the road at night (r9): PASS.** The tins shade smoothly with sharp rims; their stripe measure fell 30 to 40% on the outer pyramids. The rest of the view is unchanged (0.15 levels on average outside the window). No new fault. All four night views pass on r9.
