FAIL

# The grocer (east_parade bay 5, no. 11), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit.

I did not read the street view's review. Two things reached me by accident, and I say so plainly:
- one line of it, in a word search for ASHBY (it names the same tea firm as my narrow point 5, which I had already noted);
- a comment in the working copy of `sw_gate.py` (changed at 19:41, after these frames were rendered). It says the street review found the slab of my narrow point 13 and that a fix is in hand.

Neither changed what I measured.

**Read:** CLAUDE.md, RULINGS.md, NOTES.md ("For the next nine shops", batch A and B lessons, "Batch B" and the grocer's section), TARGET.md sections 3, 5.5, 6 and 13 (batch B), target.json's inventory, Rita's four reviews, `checks/check_grocer_v1.json`, and the parts of sw_gate.py, sw_display_gen.py and check_try2.py named below.

**Looked at:**
- the two close previews;
- the four close gate frames (2560 x 1440) at 100 to 300 per cent;
- the check renders (glass masks, room masks, reflection-off renders, front masks);
- the baked cards and the three 4096 room pictures;
- the display glb's embedded base colours;
- the till's cleaned 1k map.

**Measured, in my scratchpad (nothing in the repository or SCRATCH was changed):**
- the parallax, through the game's own `trace`;
- the glass's mean luma, day and night;
- dark patches and flat patches over the glass;
- burnt pixels;
- night reflection against the reflection-off renders;
- the display glb's parts and sizes;
- ray casts against the front glb;
- MANIFEST-grocer.json against the files.

**In short:**
- The projected room works and reads as a deep, lit grocer's: it moves exactly by the game's rule, with no black slab and no end of the picture at either camera.
- The front at close range is clean: no black strips, no see-through slots, no burnt frame at night.
- There is no drink anywhere.
- The near metre falls short in its scripted parts.
  - The tomatoes read as plastic toys. This is the very failure of 3 October that the target was written against; the target says to set them aside if they do.
  - Around the good scans (apples, onions, lemons, bananas, rolls, crates), the supports are untextured flat blocks: green slabs under the fruit and blank boards behind the tins.
  - The tins are a third too wide and too short.

**1 fault, 16 narrow points.**

## Faults

### 1. The tomatoes read as plastic toys (the 3 October failure "toys beside the scanned stock")

- **Where:**
  - CLOSE_35 day, the nearest goods in the frame: x 2060-2520, y 1270-1440 (preview 1290-1575, 795-900).
  - CLOSE_35 night_lit, the same place.
  - CLOSE_35_B day, x 1760-1970, y 960-1030.
- **What:**
  - 30 flattened lozenges, 79 to 88 mm wide and 52 mm high. An English salad tomato of 1990 is 50 to 65 mm across and nearly round.
  - Four flat reds (linear 0.41 to 0.67, 0.02 to 0.08, 0.01 to 0.02), roughness 0.3, with no texture or normal map.
  - Each has a flat green disc of 28 x 28 x 6 mm for a calyx.
  - At 100 per cent they read as children's play food: shiny red pebbles with green stickers.
  - At night their highlights are the largest burnt patch in CLOSE_35 night_lit (x 2228-2291, y 1309-1382: 1,572 pixels at 250).
- **Whose:** the builder.
  - The target's `inventory.scripted["script:tomatoes"]` says: "set aside after one try if it reads as toys". TARGET.md section 6 (F2) says the same.
  - NOTES G8 records the one try and that "from CLOSE_35 [they read] as glossy flattened spheres", but keeps them.
  - The rule's case has come, so the target's own instruction applies.
- **Exact fix:**
  - Set them aside, as the target says. Remove `script:tomatoes`, `tomato_tray` and the card "TOMATOES 45p lb" from the window, and add tomatoes to SCN-01's pending list beside the cabbage, potato, satsuma and pear.
  - Fill the tray's place (u 3.27-3.72, v 0.04-0.30) with 12 `food_apple_01` at scale 1.10, in one layer on a tray bed 0.06 high.
    - Recolour the apples' base-colour map to a Bramley green: hue-shift it so that its mean over the skin reads sRGB (150, 165, 75). Write the map as a new image; CC0 allows it.
    - Move the card "COOKERS 24p lb" to this tray. This also mends narrow point 6.
  - Then run `scenecheck`, DSP-03, DSP-05, DSP-06, TRD-01 and LIT-08, and render the two close frames.
  - If a recoloured scan is not wanted, a second tray of 15 `yellow_onion` with no new card is the cheaper fallback.

## Narrow points, most visible first (each with its exact fix)

### 1. The three backing boards are blank flat panels: the flattest tone in the window

- **Where:**
  - CLOSE_35 day: the middle board x 1264-1648, y 584-960; the right board x 2200-2560, y 596-1000.
  - CLOSE_35_B day: the left board x 4-312, y 560-1040; the middle board x 1093-1437, y 576-928; the right board x 1693-1904, y 571-864.
  - The same places at night.
- **Measured:**
  - The right board at CLOSE_35 day is luma 122, with a local standard deviation under 1 level over 27,673 pixels.
  - The left board at CLOSE_35_B day is luma 126 over 32,004 pixels (125 at night). It is the largest flat region of a light tone in either close frame.
  - The material `pyramid_board` is one flat colour (linear 0.305, 0.262, 0.188) on a 6-face box, with no grain and no print.
- **Whose:** the builder. The kit's batch A support was reused as a plain colour.
- **Exact fix:** make each board a maker's show card standing behind its pyramid.
  - A cream card ground, sRGB (232, 222, 196), with paper grain of 4 levels.
  - A 20 mm border in the colour of the pyramid's front tin's label.
  - The maker's name in the label font at 100 mm capitals, centred in the top 0.15 m above the top tin: HOLMFIELD (left), PENNYWELL (middle), KINGSMEAD (right).
  - A 16 mm deal edge.
  - Then re-measure: no window region of 10,000 pixels or more with a local standard deviation under 1 level, other than the room's floor (narrow point 16).

### 2. The tins are squat drums: 98 mm across and 86 mm high

- **Where:** every tin of the three pyramids. The nearest are at CLOSE_35 day x 2190-2560, y 600-1120 and CLOSE_35_B day x 0-330, y 560-1090. Beside them the jam jars are 75 mm across and 115 high, and the apples 84 mm.
- **Measured:** each pyramid is 0.68 m wide for 7 tins and 0.60 m high for 7 rows (`tin_pyramid_*`, display glb). The 1990 British food can (beans, soup, peas, peaches, rice pudding) was about 73 mm across and 110 high.
- **Whose:** the builder. DSP-06 (real size) tests only the Poly Haven pieces, so nothing caught it.
- **Exact fix:**
  - Make each tin 73 mm across and 110 high, with a 1.5 mm rolled rim top and bottom.
  - Keep 28 tins in rows of 7 down to 1, so each pyramid is 0.53 wide and 0.77 high on its 0.36 plinth (top at 1.13, under the 1.55 limit). The board becomes 0.56 x 0.80.
  - Add to DSP-06 a real-size line for the scripted goods: tins 73 x 110, jars 75 x 115, price cards 70 x 50 (each within 5 per cent).

### 3. The green "display paper" under the apples and lemons is a flat green block (the builder's own named shortfall)

- **Where:**
  - CLOSE_35_B day, the near crates: x 60-520, y 1100-1370 and x 600-950, y 1130-1250.
  - CLOSE_35 day, the lemon crates: x 1185-1640, y 1010-1160, RGB (85, 104, 67).
- **Measured:** `apple_bed_*` and `lemon_bed_*` are 6-face wedges (12 triangles) of one flat colour (linear 0.117, 0.216, 0.061), roughness 0.9, with no texture or normal map. At 1.5 m they read as green foam blocks, not paper or display grass.
- **Whose:** the builder.
- **Exact fix:** keep the slope, which is what lets the fruit show from the street, and change the surface to greengrocer's display grass, the period's green fringed matting.
  - The top carries a blade normal map: blades 1.5 mm wide on a 3 mm pitch, strength 0.6.
  - Base colour sRGB (46, 112, 52), varied by 8 per cent in patches of 0.05 m; roughness 0.45.
  - A fringe of blades 25 mm long hangs 20 mm over each crate's front rim.
  - Each bed fills its crate's inside, as narrow point 4 says.

### 4. The lemons stand on end like eggs, six to a crate, on a block in the middle of a half-empty crate

- **Where:** CLOSE_35 day, x 1120-1710, y 1000-1290.
  - Both ends of each red crate are empty: x 1125-1180 and 1365-1415, y 1000-1200 in the left crate, and the same in the right one.
  - The same at CLOSE_35_B day, x 1180-1690, y 900-1240.
- **Measured:** `lemon_bed_*` is 0.273 long in a crate 0.433 long. Every lemon stands with its long axis upright (box 80 x 80 x 95 mm).
- **Whose:** the builder.
- **Exact fix:**
  - The bed spans the crate's inner length and width (about 0.41 x 0.21).
  - The lemons lie on their sides, long axis along the window ±25 degrees, 12 to a crate in two layers (7 below, 5 above at the back), 24 in all.
  - Write 24 against the target's 12 in Changes after the build, and run DSP-03 for the half-seen rule.

### 5. ASHBY, one of the invented makers, is close to a real trading name

- **What:** "Ashbys" is a tea brand, a trading name of Keith Spicer Ltd, according to a web search on 14 October. I could not confirm whether it traded in 1990.
- **Where ASHBY appears:**
  - the window's CORNED BEEF and CHOPPED TOMATOES tins: CLOSE_35_B day x 0-330, y 640-1090, read "SHBY" at 100 per cent;
  - the PICCALILLI and PICKLED ONIONS jars;
  - the room's MALT VINEGAR bottles.
- **Whose:** the builder. No maker name in THIRD-PARTY.md or NOTES carries a record of a search.
- **Exact fix:**
  - Rename ASHBY to a name that returns no UK food or tea trader in a web search and in Companies House, and record that search in NOTES beside the list of makers.
  - Add "ashby" to `inventory.brand_blocklist`.
  - Search the other invented makers the same way once.

### 6. The card "COOKERS 24p lb" stands before red eating apples

- **Where:** the middle apple crate, CLOSE_35 day x 670-740, y 970-1030.
- **What:** all three crates carry the same red `food_apple_01`. A British cooking apple (a Bramley) is large and green.
- **Whose:** the builder.
- **Exact fix:** done by fault 1's fix. Otherwise the middle card reads "WORCESTER 26p lb", an eating variety's name and not a firm's.

### 7. CORNED BEEF and SARDINES on round cans

- **Where:** CLOSE_35_B day, the left pyramid, x 0-330, y 640-1090.
- **What:** in 1990 Britain, corned beef came in the tapered oblong tin opened with a key, and sardines in a flat oblong tin. On a round can the pair reads wrong to a British eye at 1.5 m.
- **Whose:** the builder (the label atlas).
- **Exact fix:** in the tin atlas, retitle those two tiles STEWED STEAK and PROCESSED PEAS (goods sold in round cans), keeping their colours. Oblong tins can come later, as their own scripted shape.

### 8. "PINK SALMON" reads "PINK SAL MON", and BLACKCURRANT touches its card's edge

- **Where:**
  - Every salmon tin, for example CLOSE_35 day x 2235-2325, y 955-1010 and the top tin of the middle pyramid (x 1395-1455, y 595-640).
  - In the atlas, `food_tins` row 3, column 4: the condensed face leaves a gap between L and M.
  - The price card "BLACKCURRANT JAM 59p" (the `price_cards` atlas, last tile): the word runs to the tile's right edge.
- **Whose:** the builder.
- **Exact fix:**
  - Set each label word letter by letter from the glyphs' ink boxes, with the gap between ink boxes 0.08 of the cap height, and test that no gap in a word exceeds 1.5 times the word's mean gap.
  - Set each card's text so that it keeps a 6 per cent margin on every side.

### 9. The label atlases are squashed to 512 x 512 in the display glb

- **What:** the glb carries every base colour at 512 x 512.
  - `food_tins` (1024 x 384) loses half its width.
  - `price_cards` (1024 x 512) and `jar_labels` (768 x 512) are squashed likewise.
  - So the tins' words are soft at 100 per cent in both close frames.
- **Whose:** the builder (the export).
- **Exact fix:** export the three label atlases at their own size, or padded to 1024 x 1024, never stretched. The glb is out of git, so its size is no reason to shrink them.

### 10. At night the yellow crates' top rims burn

- **Where:** CLOSE_35_B night_lit, x 0-550, y 1135-1387: 5,010 pixels with a channel at 250, the largest burnt patch in either close frame. A second patch is at x 581-854, y 1134-1255.
- **What:** PIC-05g passes (0.0051 against 0.01), but the rims read as glowing lines.
- **Whose:** the builder (per-shop toning, lesson 36).
- **Exact fix:** `d.tone(["plastic_crate_02*"], 0.85)`, then the two close night frames at 8 samples (lesson 33) and the whole gate.

### 11. At night the room's left wall has a lit band with a hard edge (the builder's own named shortfall)

- **Where:** CLOSE_35 night_lit, x 970-1240, y 600-860.
  - Across x 960 to 980 the dado goes from luma 39 to 96 within 20 pixels, then falls to 46.
  - The room picture shows the same at preview x 230-330, y 490-680.
- **Whose:** the builder. It is the low fill (`GB.add_fill`) reaching the side wall.
- **Exact fix:** make the fill an area light 3.0 x 0.4 m with a spread of 60 degrees, aimed at the gantry, so that it lights the shadow bands under the boards and not the side wall. Render day and night_lit again with `LEDGER_REUSE_CAL=1`, and re-read PIC-05 and LIT-02b.

### 12. The sauce and vinegar bottles have wine-bottle outlines

- **Where:** the shelves over the counter.
  - CLOSE_35 day x 1720-2330, y 360-520.
  - CLOSE_35_B day x 740-1240, y 360-520.
- **What:**
  - Brown sauce is dark red glass with a long neck and a pointed red cap; malt vinegar is olive glass with a long neck and a pointed cap.
  - Their labels read only in the 4096 picture.
  - At 100 per cent in the frames they are small dark long-necked bottles behind the counter of a shop that, in 1990, might have sold wine.
  - They are not drink, and the labels prove it, but the trade note says no bottle may read as drink.
- **Whose:** the builder (the room's scripted bottles).
- **Exact fix:**
  - Brown sauce: a squat bottle 190 mm high with a 25 mm neck and a flat black screw cap.
  - Malt vinegar: clear glass showing amber, with a flat screw cap.
  - Washing-up liquid: an opaque plastic bottle with a white push-pull cap.
  - Render the room's three states again.

### 13. A grey block fills the foot of the recessed lobby (the gate, not the shop)

- **Where:** CLOSE_35 day, x 310-445, y 930-1170 (preview 195-280, 580-730), RGB (51, 51, 51), with its top at (61 to 75). It is a dark block at night.
- **Cause:**
  - The gate's `reveal_floor` spans the whole card (model x −2.65 to 2.65) from y 0.02 to the card plane, z 0 to 0.55. In this shop it stands in the 0.6 m recessed lobby across its full width.
  - It hides the lobby floor, the shop door's foot and its letter plate (z 545).
  - My ray casts against the front glb find only the lobby's lining and floor there, and the room mask marks these pixels as "room" (the reveals).
- **Whose:** the kit (sw_gate.py, as committed and as these frames were rendered). The game has no such slab.
- **Exact fix:**
  - Build the floor reveal over the window zone only.
  - Over a door zone, start it behind the door leaf's back face (here y 0.581), never in front of it.
  - Note on the working copy: its new door-zone slab starts at y 0.47. In this lobby that is 60 mm in front of the leaf (y 0.53 to 0.58), so it would put a 0.55 m box against the foot of the door. Take y from the leaf, not a constant.
  - Then a ray test from the four cameras: no `reveal_*` part inside a lobby or in front of a door.

### 14. The room's floor crates hold onions where the target had potatoes

- **What:** ROOM-04 and G3 name it: onions are real stock and are not a stand-in for a scan. It is listed here only so that the swap is not forgotten when the potatoes come.
- **Exact fix:** when the potato scan comes, the three floor crates take it.

### 15. MANIFEST-grocer.json's "what" is Rita's text

- **What:** the field reads "...the narrow-points build (13 Oct...) ... rebuilt by build_ritas.py". The five hashes match the files on disk.
- **Whose:** the builder.
- **Exact fix:** write the grocer's own line: the batch B build of 14 October, rebuilt by `build_shop.py --shop grocer`.

### 16. Owed, for the record (the builder's own named shortfalls)

- Labels of type only on flat colour, the same layout on every tin. Owed: printed pictures from CC0 photographs.
- 48 samples against the target's 128.
- The room floor seen past the goods is a flat dark brown by day: CLOSE_35 day x 1705-2161, y 807-1257, luma 30, local standard deviation under 1. This is the linoleum at the day card's 0.15 and a grazing angle. It reads as a dark floor, not a void (luma 30 against LIT-02b's 12), so it is not a fault.

## Shared, known (the brief's list; none decides this verdict)

- **(a) the burnt orange bar in the night glass:** not seen. The night frame against the reflection-off render: mean −1.0, p95 3.6 (CLOSE_35) and 4.4 (CLOSE_35_B). The few patches 40 levels brighter (577 and 399 pixels) lie on the lemon crates' rims, not a band.
- **(c) glass parts dropped:** the till and the clock are in the room picture, too small at these cameras to judge their glass. DSP-07 says both kept their glass.
- **(e) cards leaning toward the glass:** not seen. The 14 price cards stand upright on stakes before their goods, and the boards stand upright behind the tins.
- **(f) CLOSED at night:** the door's card cannot be seen from either close camera.
- **(g) furniture shrunk:** no furniture in this display. The room's counter top is at 1.00 m, a shop counter's height.
- **(b) night_dark corners:** not in this view.

## The builder's named shortfalls: fault or narrow

| shortfall (NOTES, the grocer) | my call |
|---|---|
| the scanned produce pending (cabbage, potato, satsuma, pear) | **pending, not a fault.** Nothing stands in for them in the window. The room's floor crates hold onions (narrow 14). |
| no drink: tea and squash replaced | **right.** I read every atlas (tins, jars, bottles, packets) and every legible word in the frames: no drink, no lottery or betting, no barcode. The bottles' outlines are narrow 12. |
| gantry 147 tins and 100 packets against 160 and 90 | **narrow.** Not visible as a shortage at close range: the gantry reads full. |
| two bunches of bananas, not three | **narrow.** The crate reads full (CLOSE_35_B day, x 1820-2130, y 840-960). |
| tomatoes by script, one try | **FAULT** (fault 1): the target's own rule says to set them aside. |
| the green display paper reads too plasticky | **narrow** (narrow 3), with the fix. |
| the lifted dado and the left wall's lit patch | **narrow.** The dado still reads bottle green; the lit patch is narrow 11. |
| narrow passes LIT-02b 0.0095, LIT-08 0.65, PIC-05g 0.0051, PIC-05 0.0043 | **narrow.** I measured the same burnt shares (0.0038, 0.0051, 0.0032 by day at CLOSE_35_B). |
| printed goods by script, 48 samples | **narrow, owed** (narrow 16). |

## Measured

**Parallax, through `trace` itself** (`tools/ue/make_interior_material.py`, imported):
- The card's centre samples the picture at u 0.2028 from CLOSE_35 and 0.5968 from CLOSE_35_B: 1613.7 px of 4096 apart. PRJ-02 (1613.8) is confirmed.
- **Three room points**, solved through `trace` for the card point that shows them from each eye:
  - a top-shelf packet on the gantry at picture (1792, 525);
  - the bread basket at (1024, 1050);
  - the scale's dial at (2829, 1050).
- Each moves 656.7 card px, or 1.360 m on the card, for 2.0 m of eye travel (= 2.0 x 4.5 / 6.62).
- The gate's stored uv maps agree to the fourth decimal.
- In the baked day cards, each point's predicted patch is found at offset (0, 0) or (−1, 0), correlation 0.90 to 0.98. PRJ-03 is confirmed.
- **The picture's ends:** from both cameras the sampled u runs 0.0000 to 0.9999 with no clamping beyond the wall wedges. There is no end of the room's picture, and no black slab at CLOSE_35_B: under luma 12 is 0.0007 of the glass by day.
- At the window's door end, the display's return wall shows the room's cream plaster over the green dado (CLOSE_35 day, behind the door-end jamb, about x 440-620, y 150-970).

**The glass, mean luma** (frames at 2560; masks from the check renders):

| camera, state | all glass | room part (share) | display part | room part, reflection off | target floor (room composite) |
|---|---|---|---|---|---|
| CLOSE_35 day | 67.5 | 42.5 (0.60) | 109.9 | 36.9 | 33 |
| CLOSE_35_B day | 71.6 | 50.1 (0.61) | 109.9 | 38.9 | 33 |
| CLOSE_35 night_lit | 69.7 | 63.1 (0.60) | 84.9 | 65.0 | 45 |
| CLOSE_35_B night_lit | 69.8 | 66.4 (0.61) | 80.5 | 68.0 | 45 |

- **By day** the room is readable but dim beside the display: 36.9 and 38.9 without reflection, just over the floor of 33.
- **At night** the lit room is well above the wall beside it:
  - brick: 17.7 (CLOSE_35) and 20.6 (CLOSE_35_B);
  - render pilaster: 40.8 and 43.6;
  - the room seen through the glass: 63 to 68.
- **Pure black:** by day there is no dark patch in the glass larger than 2,420 pixels (0.09 per cent). That patch is a shadow at the back right of the room, beside the till (CLOSE_35 day x 2199-2364, y 420-585).
- At night the pixels under 12 are the glass mask's edges along the frame and the shade between tins (0.021 and 0.026 of the glass), not a void.
- **Flat tone:** narrow 1 (the boards) and 16 (the floor).

**The front at close range:**
- **By day:** 1,238 front pixels under luma 8 at CLOSE_35 and 19 at CLOSE_35_B. No line 40 pixels long or wider, and no black strip at any jamb, post or lining.
- **The lobby:** the cream panelled lining, the brass nosing and the black-and-white mosaic read well (CLOSE_35 day x 150-450, y 700-1300), apart from narrow 13.
- **At night:** the mullions and frame are lit only by the street (mostly under luma 8). There is no arc, no burnt head band and no glowing frame.

**Real sizes in the display glb:**
- apples about 84 mm;
- onions 78 to 86 mm;
- lemons about 60 x 95 mm;
- rolls 88 to 102 x 52 to 57 mm;
- jars 75 x 115 mm;
- price cards 70 mm wide;
- crates 0.455 x 0.365 x 0.229 (crate_02 at 0.9) and 0.433 x 0.238 x 0.239.

The tins are the exception (narrow 2), as are the tomatoes (fault 1).

**Legible words at 100 per cent, both close views.** All are the project's own and acceptable, except ASHBY (narrow 5):
- **Tins:** HOLMFIELD (often cut to "OLMFIELD"), PENNYWELL ("ENNYWELL"), DALTREY, KINGSMEAD, ASHBY ("SHBY"), BAKED BEANS, TOMATO SOUP, "condensed", GARDEN PEAS, SWEETCORN, SARDINES, "in oil", CORNED BEEF, PEACH SLICES, "in syrup", PINEAPPLE RINGS, RICE PUDDING, MUSHY PEAS, PINK SALMON (as "SAL MON").
- **Jars:** "BERRY JAM", "MALADE", HONEY, "ALILLI", ONIONS, "ANT JAM".
- **Cards:** ONIONS 19p lb, LEMONS 8p each, ROLLS 6 for 55p, EATING 32p lb, HONEY 69p, PICCALILLI 49p. APPLES 29p lb, COOKERS 24p lb, MARMALADE 55p and BLACKCURRANT JAM 59p need 200 per cent.
- **On the front:** the gilt 11 on the middle toplight.
- **In the room** (only in the 4096 picture): FERNSIDE, LANGDALE, MEADOWBANK, STANWICK, FERNLEY, TRENTHAM, OAKHAM, "WASHING-UP LIQUID", "BROWN SAUCE", "MALT VINEGAR", "SALAD CREAM", the packets' goods and weights. These are metric pack sizes, right for 1990.
- **The till's cleaned map at 1k, in quarters:** key legends (TOTAL, X, Y, Z, A, B, R, numbers) and receipt slips 2 to 3 px high. No maker's mark.
- **The display glb's eight Poly Haven base colours, as embedded** (crates, bananas, apple, lemon, onion, rolls, basket): no mark, no sticker.

**The content rule:**
- no alcohol (narrow 12 on outlines only);
- no gambling;
- no child;
- nothing after 1992;
- every brand invented (narrow 5).
- The tomatoes are the one thing that reads as a toy (fault 1).

## Check rows: which I trust

- **Trusted, and repeated or confirmed by me:**
  - PRJ-01, PRJ-02, PRJ-03 (my `trace` solve and the card patches);
  - LIT-02 and LIT-02b (my glass means and dark shares agree);
  - PIC-05g (I read the same shares);
  - GLS-04 (I found the same largest patches, 577 and 399 px);
  - FRN-08 and FRN-10 at the close cameras (no slot, no black strip by day);
  - DSP-07 and INV-05/06 for what I could look at;
  - DSP-01, DSP-05 (cards upright, nothing floats that I saw);
  - SO-06 and DSP-06 for the Poly Haven pieces;
  - PIC-04, PIC-01, FAS-03, GLB-01 (not repeated; they test files, and I saw nothing against them);
  - X-PRV, and MANIFEST's hashes (match).
- **Pass, but do not prove what the eye needs:**
  - DSP-06 does not test the scripted goods' size (the tins).
  - DSP-03 counts silhouettes, not whether a good reads as real (the tomatoes, the lemons on end).
  - INV-04 passes the tomatoes because the target lists them, but nothing tests the target's own "set aside if it reads as toys".
  - NEV-02's "no toys" is a statement, not a test.
  - FRN-10's 62 hidden coplanar overlaps I could not see either way.
  - DSP-04 (no run over 0.20 m) cannot see the empty ends of the lemon crates.
- **The cloud's stand-ins only (owed on the PC):** GLS-03, GLS-04 and GLS-05 (the gate's glass), LIT-01, LIT-05, LIT-07 and LIT-08 (the 100 W spill), the night part of PIC-05g, and CAM-01 (the gate's own cameras).

## What is right

- **The room is the game's rule, pixel for pixel,** and reads as a deep grocer's room.
  - It has a five-tier gantry of tins and packets, two baskets of rolls, a panelled counter with a brass lamp, a scale and a till, jars and bottles over it, side units of tins and packets, a clock, three battens and a worn linoleum floor.
  - It shifts as it should between the two cameras, with no seam where the display's bed meets it.
  - The far end of the window is the room's own wall, at both ends, by day and night.
- **The scans read as real goods:** the apples, onions, bananas, lemons and rolls, and the orange, red and timber crates. Each piece is at real size, and the apples are heaped on their slopes so that every one shows.
- **The jars' step** has six products of three jars each, with a hand-lettered card before each group. Every crate, tray and basket has its card on a stake, priced in pence a pound, as in 1990.
- **No drink anywhere:** the tea and squash are gone, and every label is the project's own.
- **The front at close range:**
  - the lobby's cream panelled lining, brass nosing and mosaic floor;
  - the bronze M2 frame with the glazed return at the door end;
  - the gilt 11;
  - no black strips;
  - a night frame lit only by the street.
- **The night:** the display is lit (median ratio 1.59 and 2.62 to the room), the room is brighter than the wall beside it, and there is no arc or band. Only the crates' rims and the tomatoes' highlights reach 250.

## What I cannot judge from the files

- **The game's own glass, light and image:** the day reflection (here the stand-in reflects the far side's buildings and footway), Lumen's light on the display at night, the exposure, the card under TSR, and the frame time.
- **The shop door at close range:** its glass foot, bell, OPEN or CLOSED card, hours plate, letter plate and handle are not in either close frame. The lining of the recessed lobby hides the door from CLOSE_35, and CLOSE_35_B does not frame it. They are the street view's to judge, and the gate's block (narrow 13) hides the door's foot anyway.
- **The lobby's glazed return seen from inside the lobby.** The display's return wall stands 10 mm behind that glass, so a customer in the doorway would see a painted wall, not the display. No close camera looks that way.
- **The scanned produce**, which is not yet fetched.
- **Wear, grime and wet,** which come from the game's own layers. Everything here is clean.
