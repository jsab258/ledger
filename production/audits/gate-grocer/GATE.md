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
