FAIL

# The empty unit (east_parade bay 3, no. 7), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

I am a fresh reviewer. I did not write the target, build the front or read the close view's review. I judged STREET_SQUARE and STREET_30, by day and night_lit, and nothing else. Jafar's ruling of 9 October applies: a piece that fails only on narrow points passes, with those points listed.

**What I read:**
- CLAUDE.md and RULINGS.md (1, 2, 3 and 9 October).
- NOTES.md: "For the next nine shops", the empty unit's section (E1 to E6, its shortfalls) and batch A's lessons.
- TARGET.md: section 3, table 5.3, D10, LIT-03 and A13.
- The 4.1 fascia target's empty-unit paragraph (fascia-signs/TARGET.md, line 179) and its letting-board line (line 280).
- Rita's four reviews. I read the street reviews closely and skimmed the close ones.
- `checks/check_empty_unit_v1.json`, all 24 rows.

**What I looked at:**
- The two street previews (`empty_unit-street-square-{day,night-lit}-2026-10-13.jpg`). They match the gate frames: the mean absolute difference after downsizing is 1.8 levels.
- The four street gate frames in `ledger-scratch/shop-windows/empty_unit/gate/` (2560 x 1440, 14 Oct 00:50 to 00:55), at full size and in crops up to 4 times.
- The 4.1 board's basecolour and wear maps, and the exported worn basecolour.

**What I measured:**
- Rec.709 luma (0 to 255) over boxes in the 2560 x 1440 frames. All boxes below are in those frames.
- The local tone of the glass: the standard deviation (sd) in 32 px tiles.
- The dark components under luma 8.
- The contrast of the number 7.
- The 4.1 board's pale area.

## Verdict

**One fault blocks. It belongs to the target's 4.1 board, not to the builder.**
- **The fascia reads as camouflage from the far pavement.** Pale, smooth-edged blobs cover about a quarter of the bare board and break up the buff painted-out panel.
- **The rest of the front reads as an empty Victorian shop to let.** The bare timber front has its left console gone. The whitewashed panes read pale and blank, not black. The TO LET board sits askew, and the black doors stand in a bleached frame.
- **Four narrow points remain**, each with an exact fix.

## Faults, worst first

### F1. The fascia's paint loss reads as a camouflage pattern (day and night, both cameras). WHOSE: the target (the 4.1 board, `fascias/empty_unit/empty_unit_basecolour.png`, made by make_fascias.py's class 3 wear). The builder mapped it faithfully (FAS-01 pass).

**Where:**
- STREET_SQUARE: the board x 880 to 2140, y 290 to 385 (1600 preview: x 550 to 1340, y 180 to 245).
- STREET_30: x 990 to 2050, y 300 to 430.
- At night the pale blobs stand out even more against the dark ground.

**What is wrong:**
- There are about thirty large blobs, 150 to 500 mm across. Each has rounded lobes and a horizontal streak inside, and they are spread evenly over the whole board, including over the buff painted-out panel.
- From 8.76 m the board reads as a military camouflage print or a noise mask, not as old timber. It is the most visible thing on the front after the glass.
- 4.1's own words for this board are "bare soot-darkened timber, paint long gone, a few patches of old paint ... a painted-out patch [1105, 120, 4305, 420] ... loss 0.17".
  - The picture does the opposite: the dark ground looks like paint, and the pale blobs look like loss.
  - The buff panel is only half visible: 49.8 per cent of its pixels are buff, and blobs cut the rest.

**Measured:**
- In the gate frame the board's luma is 92.0 mean, with sd 45.3. Its 1st percentile is 20.2 and its 99th is 181.3, so the blobs are as bright as the whitewash below (179).
- In the texture, 27.6 per cent of the board is over luma 110.

**Exact fix (4.1 board, empty unit only):**
1. Regenerate the loss as weathering of real paint, not as noise blobs:
   - Each loss shape runs along the grain. Its length to height ratio is at least 4:1, and it is at most 40 mm high.
   - 70 per cent of the loss area lies within 80 mm of the board's bottom edge, its two ends, and the plank joints and nail heads.
   - The total loss is 0.08 of the board.
2. Keep the buff panel [1105, 120, 4305, 420] one continuous rectangle. It loses paint only within 30 mm of its own ragged edge.
3. Colour the loss as silvered timber at most 1.8 times the ground's luma. The old paint's remnants (the "few patches") should be small: at most 8 patches, each 30 to 120 mm.
4. Pass condition, at STREET_SQUARE by day:
   - outside the buff panel, the board's luma sd is at most 18;
   - no pale component outside the panel is over 60 x 60 mm.
5. Re-export the board and rerun FAS-01 and the gate's STREET_SQUARE day frame.

## Narrow points (each with its exact fix)

### N1. The street number 7 on the shop door's fanlight cannot be read. WHOSE: the target (4.1 paints every fanlight number cream, 194/188/171), and the builder (E3 kept that colour on whitewash).
- **Where:** STREET_SQUARE x 1775 to 1798, y 528 to 560. It is visible only as a faint mark at 4 times; at STREET_30 it is a speck.
- **Measured:** the 7's darkest 5 per cent is luma 147.2 against the whitewash's 170.3, a ratio of 1.16.
- **Fix:** for the empty unit only, paint the 7 in sign-writer's black (30, 30, 32) on the outside of the glass (d 37), at the same size and place. Pass: the ratio is 2.5 or more at STREET_SQUARE by day.

### N2. The whitewash is nearly a flat tone; it reads as frosted glass more than a hand-applied wash. WHOSE: the builder (E1's single anchor) and the 4.1 tile.
- **Where:** the three lights, x 915 to 1645, y 525 to 915.
- **Measured:**
  - By day the 32 px tiles have a median sd of 1.97, and each light's sd is about 6.
  - At night the median tile sd is 0.85, and 73 per cent of tiles are under 1.
  - The brush strokes the builder describes cannot be seen at this distance.
- **Not a void or a white card.** The day luma is 178.8 (LIT-03 asks for 150 or more), no pixel is clipped, and no pixel is black.
- **Fix:**
  - Anchor the tile per light, so the strokes stop at each bar and mullion.
  - Leave a thinner band 40 to 80 mm wide along every bar, mullion and the bottom rail, where a cloth does not reach: luma 25 to 35 lower by day.
  - Raise the swirl's contrast until each light's sd is between 10 and 16 at STREET_SQUARE by day, keeping the mean at 160 or above.

### N3. LIT-03's night number was met by turning down the gate's street lamps for this shop alone (E6: 42,000 W against 50,000 for every other shop). WHOSE: the builder, and the target's row.
- **What changing the lamp does:** it changes the stand-in, not the shop. The night frames of the shops are then no longer lit alike.
- **Measured:** the whitewash at night is 39.2 and the brick beside it 16.9, a ratio of 2.32. By day the same ratio is 178.8 / 84.0 = 2.13. The pale paint is behaving as pale paint under the same lamp.
- **Fix:**
  - Put the lamps back to 50,000 W.
  - Rewrite LIT-03's night bound as a ratio: the whitewash-to-brick ratio at night is at most 1.25 times the same ratio by day. At 42,000 W it is 1.09. The ratio does not depend on lamp power, so the row should pass at 50,000 W too; confirm after the re-render.

### N4. FRN-10 fails on a natural shade pocket, not on a black part. WHOSE: the check row (kit).
- **Where:** the patch is under the cornice's soffit, beside the right console: STREET_SQUARE x 2113 to 2163, y 266 to 305 (603 px under luma 8).
- **The other two dark runs are shade too:**
  - the line above the TO LET board (x 1423 to 1612, y 277 to 286) is its shadow on the fascia;
  - the black frame head over the shop door (x 1684 to 1895, y 587 to 626) is in the shade of the transom.
- **Coplanar faces:** none that a camera can see (0 of 46).
- **Not a fault in the picture:** at 100 per cent it reads as the dark recess it is, and the dark paint (46, 37, 30) is the target's.
- **Fix:** give FRN-10 a named exception for "the pocket under the cornice soffit within 150 mm of a console, on a face turned away from the sky". Mark the pocket owed to the PC's Lumen bounce, and rerun the row.

## What is right

- **The front reads as a closed-down Victorian shop in a port parade.**
  - Panel pilasters, the right scroll console and the left one gone (as 4.1 says), the timber cornice, the bare dark fascia, the boarded stallriser with its plate of fixings, and the T2 window of three lights and nine toplights.
  - The black T1 shop door has a brass letter plate and kick plate. The black four-panel F1 side door has a muntin letter plate and a knob. The band above the doors has three toplights, a fanlight and a fielded panel.
  - The proportions and the dark, worn palette sit with the Hook sheet's parade and with Rita's front.
- **The trade reads at once:** whitewash, TO LET and a dead fascia say "empty, to let". There is nothing in the window, as the ruling asks.
- **The glass is a pale blank by day, not black:**
  - window 178.8 by day (LIT-03 asks for 150 or more);
  - the lights are within 1 level of each other;
  - no pixel is under 3 or over 250 by night or day.
- **The glass is dim at night, in step with the lamps:** 39.2, against 16.9 for the brick beside it. Nothing glows through it, and no stand-in light or glass shows in it.
- **Every legible word at 100 per cent:**
  - "TO LET" (red on the white board, readable at both cameras, not cut by any bar): fine, generic.
  - "7" (barely legible, N1): fine as a street number.
  - Nothing else: no maker's name on the brass, no agent's name, no barcode, nothing after 1992.
- **Content:** no drink, gambling, children or people.
- **Rita's export faults are not repeated:**
  - The one normal map is a true tangent map (GLB-01 and FAS-01n). Note that the fascia's is flat, (128, 128, 255): the board's relief is only in its colour.
  - There is no textured primitive without UVs (FAS-03).
  - There is no visible coplanar pair; FRN-10's luma part is N4.
  - There is no see-through slot at STREET_30. The only backdrop is the bay's outer sliver of 18 px beside the right pilaster, which the gate's pier closes (FRN-08); I found none in the frame.
  - The hall behind the side door is closed (FRN-09).
- **Check rows I trust** (measured on the built meshes or the glb): GLB-01, FRN-01 to FRN-05, FRN-07, FRN-09, FAS-01, FAS-01n, FAS-03, GLS-01, GLS-02, NEV-01, NEV-02 and CAM-01.
- **Check rows that rest on the cloud's stand-ins:**
  - LIT-03, the stand-in lamps (N3);
  - FRN-10's luma half, which has no Lumen bounce (N4);
  - FRN-08, the gate's piers.

## The builder's named shortfalls

| Shortfall | Fault or narrow point | Why |
|---|---|---|
| Nothing behind the glass | Neither: correct | The ruling and the target ask for an opaque whitewash with no room. |
| Dark paint in shade (FRN-10) | Narrow point N4 | Shade, not a black part. |
| The lamp at 42,000 W | Narrow point N3 | The stand-in was changed to meet the number. |
| The strokes run across the bars | Narrow point N2 | It cannot be seen at street distance, but it is part of why the wash reads flat. |
| No peeling or ladder marks | Not needed | |

## What I cannot judge from the files

- The game's glass over the whitewash: its reflections of the sky and the street, by day and night. The cloud's pane is opaque and has no reflection. That reflection will change how the whitewash reads at both cameras (PC-02 and the game's whitewash material).
- The night under the game's lamps: pools with darkness between (the ruling of 1 October), against the gate's even wash. The black stallriser (1.5) and the black footway (5.8) at night are the gate's stand-in lamps, not the shop.
- Whether the agent's name and telephone number on the TO LET board are wanted. A 1990 board always carried them, but 4.1 leaves them blank until the town mints them.
- How the shop sits beside its neighbours in the parade (Rita's and the launderette); each gate frame shows one bay against plain brick.
