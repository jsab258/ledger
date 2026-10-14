PASS

# The grocer (east_parade bay 5, no. 11), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. I judged the street view only (STREET_SQUARE and STREET_30, day and night_lit). I did not read the close review of this shop or any other shop's review before writing this.

**Verdict.** No fault of this shop's own. Seven narrow points, each with an exact fix (Jafar's ruling of 9 October: a pass, with the points listed for the builder).

The front reads as a 1930s refit of a Victorian parade shop and as a grocer's from across the street. The window is glass with a lit, stocked room behind it, by day and at night. The fascia reads at both cameras, day and night.

**One shared fault of the gate's must be fixed before any street picture of this shop goes to Jafar.** The gate's dark filler block (`reveal_floor`) stands in the recessed lobby. It hides the lobby floor, the threshold, the door's kick panel and its letter plate behind a flat dark box (see "Shared, known"). It is the kit's, not this shop's. The game's own front is right: I rendered the glb without the gate, and the door foot, letter plate and chequered lobby floor are all there.

**What I read:**
- CLAUDE.md and RULINGS.md (1, 2, 3, 8 and 9 October).
- NOTES.md: "For the next nine shops" (lessons 1 to 27), Batch B's shared changes, and the grocer's own section in full.
- TARGET.md section 3, table 5.5, and "Changes after the build" (B5 to B7, B12, B13).
- Rita's four reviews.
- `checks/check_grocer_v1.json`, all 71 rows.
- The parts of `sw_gate.py`, `sw_front.py` and `sw_shops_grocer.py` that make what I saw.

**What I looked at:**
- The seven previews `grocer-*-2026-10-13.jpg`.
- The four street gate frames at 2560 x 1440, at full size and in crops up to 4 times.
- The gate's check renders: the glass masks, the room masks, the reflection-off renders and the front-only backdrop.
- The two glbs, read with bpy and as glTF JSON.
- The label atlases and the 4.1 fascia map.
- The Hook sheet, and Rita's approved front (v3 street preview).

**What I measured:**
- Rec.709 luma (0 to 255) over the gate's own glass masks (eroded 4 px), the brick, the block in the lobby, the boards, the fascia, the 11 and the lobby.
- Flat patches: local standard deviation over 9 or 7 px.
- A repeat of GLS-03 and GLS-04 from the full-size reflection-off renders.
- UVs and normal maps read straight from the glbs.
- A quick Cycles render (24 samples) of `grocer_front.glb` alone from both street eyes, to see the lobby without the gate.

Pixel boxes are in the 2560 x 1440 gate frames. "1600" marks the preview JPEG (x 0.625).

## Faults (this shop's own), worst first

None.

## Narrow points, each with its exact fix

### N1. The lobby has no lamp: the target's pendant opal globe is not built and not named

- **Where:** STREET_SQUARE night_lit and STREET_30 night_lit, the lobby (SQ x 559 to 778, y 500 to 1060; 1600: x 349 to 486, y 312 to 663).
  - The recess reads dark: the soffit band is luma 4.5, the cream lining 30.2.
  - Only the room seen through the door glass lights it (53.8).
- **What the target asks:** TARGET.md 5.5 "lights", night_lit: "the three battens on and a pendant opal globe in the lobby (2700 K, 60 W)".
- **What was built:**
  - The front glb has no lamp; no kit file mentions a pendant or globe.
  - NOTES does not list it among the judgements or the shortfalls.
  - Its "look first" line says the lobby's left wall is "lit by the fill". What is lit is the room's left wall, seen through the door.
- **Why narrow:** at night the window, the door glass and the fascia still say "lit grocer's". But the lit lobby is the shop's welcome at night, and the target names it.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. In the grocer's front (`sw_front.py` lobby part), add a pendant at the soffit's centre (x_m -2.151, y_m 0.20):
     - a 70 mm brass ceiling rose;
     - a 150 mm brass rod;
     - a 200 mm opal globe, bottom at z 2.00 above the lobby floor.
  2. In the gate's night_lit:
     - put a 2700 K point light of 4 Blender watts (radius 0.08) inside the globe. That is the room tubes' 30 W scaled by 700 lm against a T12's 5,000 lm.
     - make the globe's shell emissive so its pixels read 180 to 240 at STREET_SQUARE;
     - keep the globe dark by day.
  3. Owe the game's own light on the PC (a PC row beside PC-02).
  4. Add a row FRN-13: when the target's night_lit names a lobby lamp, the front carries it and the night_lit frames show it at 180 to 249.

### N2. The tin pyramids stand against three bare grey boards: the flattest, palest things in the window

- **Where:** STREET_SQUARE day, the exposed corners of the three backing boards, y 705 to 815 (1600: y 441 to 509):
  - board 1: x 845 to 903 and 932 to 996;
  - board 2: x 1238 to 1295 and 1327 to 1389;
  - board 3: x 1645 to 1705.
  - STREET_30 day: x 1084 to 1126, 1302 to 1342, 1559 to 1689 (y 707 to 798).
- **Measured:**
  - By day the corners are luma 100 to 128 with a standard deviation of 1.0 to 4.7. Together they are about 5 per cent of the glass at STREET_SQUARE: patches flat under sd 3 and over luma 85 make 6.8 per cent, the third plinth's face included.
  - At night they reach 90 to 157 (board 2: 157). The glass mean is 65.8 by day and 77.5 at night.
- **Cause:** the glb has `pyramid_backing_0/1/2`, each 0.72 x 0.62 x 0.012 m at v 0.538 to 0.55, in an untextured `pyramid_board`, sRGB (150, 140, 120). Each pyramid is one tin deep, so the board hides the hollow back. But the board is a rectangle behind a triangle, and its two bare corners read as a blank card.
- **Why narrow:** the pyramids, apples and gantry carry the window. The boards are props, not the room reading as a white board (the "white board" fault).
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. In `sw_shops_grocer.py`, make each backing board stepped to the pyramid's outline: seven strips, row r (0 at the foot, 7 - r tins), each strip the row's width plus 10 mm and one tin high, 12 mm thick, at the same v and in the same colour. The tins then hide the board from STREET_SQUARE.
  2. Check: at STREET_SQUARE by day, the pale flat patches inside the glass (sd under 3 over 7 px, luma over 85, saturation under 55) fall from 6.8 per cent to under 2 per cent.
  3. If a showcard is wanted instead, it is a printed, hand-lettered card of the pyramid's own invented maker. It is never a blank board.

### N3. No hours on the door, though NOTES says there is an hours plate under the OPEN card

- **Where:** STREET_SQUARE day, the door glass under the OPEN card (OPEN at x 680 to 725, y 707 to 730; the space below, x 640 to 760, y 735 to 800). There is nothing there.
- **Cause:**
  - 4.1's fascia manifest draws `small_panels` only for the launderette, the tea rooms and the letting board. So `sw_front.py` (line 1271) places no `door_sign_hours_plate`, and FRN-12 does not run for this shop.
  - NOTES says "the OPEN card and 4.1's hours card" (What was made) and "the hours plate under the OPEN card" (look first). Neither exists.
  - Rita's door, the model (RULINGS 2 Oct), carries its hours.
- **WHOSE:** the target (4.1's set) for the missing plate; the builder for the NOTES lines.
- **EXACT FIX:**
  1. 4.1 (`make_fascias.py`) draws `hours_plate.grocer`, 300 x 190 mm, a signwriter's card in the board's lettering and colours: "OPEN 8 - 5.30 / WED 8 - 1 / CLOSED SUNDAY" (the target's hours).
  2. The front then places it with no code change: top z 1380, under the OPEN card. FRN-12 holds it.
  3. Until then, strike the two NOTES lines.

### N4. The right wall's packets, one of each in turn, read as a bookcase from the street

- **Where:** STREET_SQUARE day, through the third light (x 1650 to 1720, y 590 to 720; 1600: x 1031 to 1075, y 369 to 450). Room picture `grocer_day.png`, the right unit.
  - Seventy-five tall, narrow packets stand face out, shoulder to shoulder, each a different product from its neighbour, with white tops in a row.
  - From the pavement this is a shelf of book spines.
  - The gantry is shelved the same way (one of each in turn), but its tins and wider packets still read as a grocer's.
- **WHOSE:** the builder (the room).
- **EXACT FIX:**
  1. On the right unit, stand the packets in facings of one product: 4 to 6 alike side by side, 15 mm between facings, the same 75 in all.
  2. Do the same on the gantry's packet runs.
  3. Add a room row: along each board, at least 70 per cent of neighbouring goods are the same product as their neighbour.
  4. Re-render the room pictures. The street frames follow through the card.

### N5. At night, through the shop door, a lit patch with a hard straight edge on the room's left wall (the builder's own named shortfall)

- **Where:** STREET_SQUARE night_lit, the shop door's glass (x 730 to 770, y 750 to 840). There the dado reads luma 80, against 40 at x 630 to 700 beside it, with a vertical edge. In the room picture `grocer_night_lit.png` it is the patch under the left unit (1600 preview x 230 to 320, y 490 to 640).
- **Cause:** G12's low fill, an invisible area light 0.4 m up and 2.1 m in front of the gantry at 30 W in night_lit, reaches the left wall. The left unit's board cuts it off sharply.
- **Why narrow:** it is seen only through the door and reads as the corner of an alcove. A light without a source is still a giveaway.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Light-link the fill (`GB.add_fill`) to the gantry, its goods, the back wall and the floor in front of it, so no fill reaches the side walls. Or set the fill's spread to 60 degrees and its width to the gantry's 2.6 m.
  2. Check: in `grocer_night_lit.png`, the left wall's dado under the unit is within 15 per cent of its luma 0.3 m to either side.

### N6. Two invented makers may not be safe names: ASHBY and DALTREY

None of these names is legible from the street: at 100 per cent no word on a good or ticket can be read. These are the names on the label atlases (`rooms/tex/food_tins.png`, `food_packets.png`, `jar_labels.png`, `grocer_bottle_labels.png`), checked against what I know of British firms of 1990. No register was reached, so none is verified.

- **ASHBY:**
  - Tins: corned beef, chopped tomatoes. Jars: piccalilli, pickled onions. Bottle: malt vinegar.
  - I believe there is a real tea merchant's brand "Ashbys" (Ashbys of London, which claims roots in 1850).
  - I could not verify that it traded in Britain in 1990.
  - A tea merchant's name on a grocer's goods is the worst place for a collision.
- **DALTREY:**
  - Tins: garden peas, pineapple rings.
  - Not a firm I know. It is the surname of Roger Daltrey of The Who, famous in 1990. A living famous person's name on a tin reads as a joke or a reference.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Rename both in `sw_shops_grocer.py` (TIN_DESIGNS, JAR_DESIGNS, BOTTLE_DESIGNS): for example ASHBY to ASHLOW and DALTREY to DARNBY.
  2. Search each new name on the Companies House register and the UK trade marks register (both free online) before use, and write the result in NOTES.
  3. Add the old two to the INV-05 word list. A whole-word blocklist cannot know a firm, which is why ASHBY passed.
- **The rest, with what I can and cannot say:**
  - **KINGSMEAD** (sweetcorn, rice pudding, jams): not a firm I know. It is near Kingsmill, Allied Bakeries' real bread brand of 1987, but a different word on different goods: keep.
  - **OAKHAM** (cornflour, custard powder): a town. The brewery Oakham Ales was founded in 1993, after the window and a drink maker: keep.
  - **No firm known to me, not verified:** HOLMFIELD, PENNYWELL, MEADOWBANK, STANWICK, FERNLEY, TRENTHAM, LANGDALE, FERNSIDE.
  - **The price cards' words** (APPLES, COOKERS, EATING, ROLLS, LEMONS, ONIONS, TOMATOES, BANANAS, the six jar products, prices from 8p each to 69p) are the shop's own and are fine. Pence a pound is right for 1990.

### N7. Something does stand in for the pending potatoes: onions in the room's floor crates

- **Where:** the room's three floor crates under the gantry: 54 yellow_onion where the target loads potatoes (G3, ROOM-04).
  - From the street they are not seen: the display hides the crates, and the card's camera sees only their sides.
  - The window itself has nothing standing in for the cabbage, potato, satsuma or pear. The onions, tomatoes, apples, lemons and bananas there are all on the target's list.
- **Why narrow:** a crate of onions is a true grocer's good, and G3 names it. But NOTES' shortfall line and SCN-01 say "nothing stands in for them", which is not quite so.
- **WHOSE:** the builder (the record).
- **EXACT FIX:**
  1. In NOTES' "Known shortfalls" and SCN-01's detail, add: "the room's three floor crates hold 54 onions in the potatoes' place (G3)".
  2. When the scans come, load the potatoes into those crates as the target says.

## Shared, known (not this shop's; none of them decides the verdict)

- **The gate's dark filler block stands in the recessed lobby (the launderette's finding): PRESENT HERE. The kit's.**
  - **Where:**
    - STREET_SQUARE day: a flat box of luma 43.3, sd 4.4, RGB (42, 43, 46) at x 559 to 778, y 938 to 1061 (1600: x 349 to 486, y 586 to 663).
    - STREET_SQUARE night: luma 4.4, a black hole in the doorway.
    - STREET_30 day: x 816 to 933, y 882 to 982, where its top and front faces read as a solid box standing in the door.
  - **What it hides:**
    - the chequered green-and-cream lobby floor with its terrazzo field (`lobby_floor_grocer`), except its first 0.12 m behind the nosing;
    - the terrazzo threshold;
    - the door's bronze kick panel and its letter plate (z 525 to 565).
    - The door looks blocked by a crate.
  - **Cause:** `sw_gate.py` line 367, `slab("reveal_floor", -W/2, W/2, 0.02, ycard + 0.02, 0.0, 0.55)`. It runs the whole card width and fills the lobby (0.6 deep) to 0.55 high.
  - **The game is right:** my render of `grocer_front.glb` alone shows the door foot, letter plate and floor.
  - **The checks miss it:** FRN-06, FRN-08 and FRN-10 cannot see it, because their masks treat gate objects as not the front, and it is above luma 8 by day.
  - **EXACT FIX (the kit, every shop):**
    1. Run `reveal_floor` across the window zone only: x_m from the window's u0 to u1 (here -1.644 to 2.65), never across the door zone. Behind a door stands the door.
    2. Add a gate row: in an object-index pass from every review camera, no pixel of a gate object (`reveal_*`, `card`, `return_wall_*`) lies inside the door zone below the door's glass foot.
    3. Re-render the four street frames.
    4. Do not show this shop's street pictures to Jafar before that.
- **(a) The burnt orange bar in the night glass: not present.** I repeated GLS-03 and GLS-04 from the full-size renders: p95 2.6 and 3.0, with 0 px at 40 levels or more above the reflection-off render at either street camera.
- **(b) Hot top corners in night_dark: not present.** The corners read 6.6 against a mean of 17.9; the counter lamp is the one warm point.
- **(c) Dropped glass parts:** the till's and the clock's glass are kept (DSP-07). They are too small to judge at street distance.
- **(e) Sheets leaning toward the glass: not seen.** The 14 price cards are 4 mm boxes standing upright, and the pyramid boards are vertical (glb bounds).
- **(f) CLOSED at night: fixed here.** The door reads OPEN in night_lit, which fits a winter's dark afternoon before 17:30, the shop's hours.
- **(g) Child-size furniture: none in this display.** The room's goods are at 0.90 to 1.00 (SO-06).
- **Not a letter of the list:**
  - The night pavement is lit across the whole frame (104.5 in front of the window), not as a pool. It is the gate's stand-in, and the game's own is owed (PC-02).

## The builder's named shortfalls, at street distance

| shortfall (NOTES and the check) | my judgement |
|---|---|
| scanned produce pending (SCN-01) | **pending, not judged.** Nothing is modelled for the four in the window. The room's crates hold onions for the potatoes (N7) |
| no drink: tea and squash replaced by dry goods and sauces | **right, not a shortfall.** From the street nothing reads as drink: the bottles over the counter read as sauce bottles among jars (STREET_SQUARE x 1230 to 1600, y 545 to 660); there is no can, glass or wine shape |
| gantry 147 tins and 100 packets against 160 and 90 | **narrow, not even a point from the street.** The gantry reads full |
| two bunches of bananas; tomatoes by script | **not a fault from the street.** The bananas read; the tomatoes read as tomatoes at 100 per cent (a little long and glossy at 2 times) |
| the green display paper shows under the fruit | **not a fault from the street.** It reads as a greengrocer's green display matting at the crates' rims. Whether it looks plastic is the close view's |
| the room lit to a lifted dado; a lit patch with a straight edge in night_lit | **the dado: right.** It reads bottle green, (26, 31, 26) by day and (33, 42, 31) at night beside the patch. **The patch: narrow (N5)** |
| narrow passes: LIT-02b STREET_30 day 0.0095; LIT-08 CLOSE_35_B 0.65; PIC-05g 0.0051; PIC-05 0.0043 | **not faults.** At the street cameras the under-12 pixels are shelf shade (largest patch 0.36 per cent at SQ); the burnt pixels at night (0.22 per cent of the glass at SQ) are on tin tops and the bananas. LIT-08 is the close view's |
| printed goods drawn by script, pictures from CC0 photographs owed | **not judged from the street.** The labels read as coloured bands. The flat icons on the packets (stars, suns, waves) are the close view's |
| 48 samples in the room pictures (target 128) | **not seen from the street.** The ceiling and walls read clean |

## What is right

**The front.**
- It reads as a British parade shopfront given a 1930s refit:
  - cream render pilasters on plinths;
  - plain block consoles with three bosses;
  - the timber cornice;
  - a bottle-green glass fascia with a chrome edge and the period's three-line ends;
  - a bronze M2 window, glazed from 600, with six toplights;
  - a glossy bottle-green slab stallriser with a chrome capping and black joints;
  - a recessed lobby with a panelled cream lining;
  - the bronze M2 door with its three toplights and the 11 on the middle one.
- The proportions sit with Rita's approved front and the Hook sheet's parade: a 550 board, a 6.0 m bay and the window head at 2.85.
- Bottle green and cream are a grocer's colours and belong beside the Hook sheet's painted fronts.
- Nothing is mirrored and no text reads backwards. The door is handed as the target says: the pull bar on the left stile, the butts on the right.
- No part floats, and none fails to meet. At STREET_30 there is no slot beside either pilaster: brick meets them at both ends. FRN-07 finds 0 uncovered pixels, and FRN-08's 51 px at SQ is the bay sliver the gate's pier closes.
- No dark patch of 5 px or wider lies on the front by day. The only pixels under luma 12 in the bay are shelf shade inside the room.

**Rita's export faults, none repeated:**
- the fascia's normal map is a real one (mean 127.9, 127.9, 254.8, read from the glb);
- all 4 textured primitives of the front and all 38 of the display carry TEXCOORD_0, and none points at -1;
- no coplanar black strip (FRN-10, and my own scan);
- no see-through slot;
- the spill cannot be seen (no white bar under the transom; LIT-07 0.0000), and the night glass doubles nothing (GLS-03 2.6 and 3.0, repeated).

**The lettering.**
- FAMILY GROCER and HIGH CLASS PROVISIONS read at both cameras:
  - by day, letters to ground 3.47 at SQ and 3.52 at STREET_30 (FAS-01c 3.32);
  - at night 6.45 and 7.07: cream letters on a dark board, better than Rita's gilt.
- The 11 reads whole on the middle toplight (GLS-02: no ink behind a bar). By day it is gilt on dark glass. At night it is dim orange (p95 70) against the lit toplight, readable by its shape; the game's own is owed (lesson 14, PC-06).
- OPEN reads by day and, as a silhouette, at night.
- Every legible word in the four street frames at 100 per cent: FAMILY GROCER, HIGH CLASS PROVISIONS, 11, OPEN. All are the shop's own. No firm's name, maker's mark, barcode or modern mark is legible.

**The window is glass with a lit, stocked room behind it.** None of it is a void or a white board.

| measure (glass mask of the three lights, eroded 4 px) | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, glass mean luma | 65.8 (p5 19, p50 53, p95 145) | 67.8 (p5 19, p95 147) |
| day, under 3 / under 12 / a channel at 250 | 0.01% / 0.49% / 0.003% | 0.01% / 0.80% / 0.002% |
| day, largest flat patch (9 px, sd under 1) | 2.1%: the right wall's plaster, luma 56.5 | 2.7%: the dado in shade, luma 22.6 |
| day, room pixels only, reflection off (target composite floor 33) | 40.8 (65% of the glass shows the room) | 43.3 |
| day, brick beside | 84.5: the glass is 0.78 of the wall, dimmer, as P1 and P3 have it | 84.4 |
| night_lit, glass mean | 77.5 (p5 18, p95 157) | 82.1 |
| night_lit, room pixels only, reflection off (floor 45) | 78.5 | 86.7 |
| night_lit, brick beside | 22.3: the window is 3.5 times the wall | 21.4 |
| night_lit, under 12 / a channel at 250 | 2.35% (shade under the display) / 0.22% | 2.02% / 0.19% |

**The trade reads from the street.** It is a grocer's:
- the board;
- three tin pyramids;
- three crates of apples on green matting;
- lemons, a tray of tomatoes, onions and bananas;
- jars on the step and rolls in a basket;
- behind them a stocked gantry of tins and packets, a counter with a dial scale, a till and a brass lamp, and a wall clock.

TRD-01's counts agree with what I see. The greengrocery's staples (potatoes, cabbage) are the pending scans, so for now the window reads more "grocer with fruit" than greengrocer. That is pending, not a fault.

**Content.**
- No alcohol: no bottle, can or label reads as drink.
- No gambling, child, toy or person.
- No tobacco shown.
- Nothing after 1992: no barcode is visible, and nothing flat-screen or modern.

**The builder's look-first items:**
- the green fascia: right;
- the recessed lobby: right in the glb, hidden in the gate (shared);
- the number 11: right;
- the lifted dado at night: reads bottle green, with one hard patch (N5);
- the hours plate: does not exist (N3).

## The check rows: which I trust

- **Trusted (50)**, as measured on the real pictures, meshes or files:
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-04, SO-06, SO-07;
  - DSP-01, DSP-02, DSP-03, DSP-04, DSP-05, DSP-06, DSP-07;
  - ROOM-01 to ROOM-04;
  - INV-01 to INV-04, INV-06;
  - NEV-02;
  - GLB-01, FRN-01 to FRN-05, FRN-07;
  - FAS-01, FAS-01n, FAS-01c, FAS-03;
  - GLS-01, GLS-02, GLS-05;
  - TRD-01, LIT-06, CAM-01, X-PRV.
  - I repeated GLB-01/FAS-01n, FAS-03 and FAS-01c myself, and they agree.
- **Pass but do not prove what they say (6):**
  - **FRN-06:** the lobby is right in the glb, but no row looks at it in the frames, where the gate's block hides its lower 0.55 m.
  - **FRN-08 and FRN-10:** their masks treat gate objects as not the front, so a gate box standing in the doorway passes both (shared).
  - **INV-05 and NEV-01:** word lists match words, not firms; ASHBY passed (N6).
  - **ROOM-05:** "SHORT ... plastic_crate_02 0 of 3" is right, but it does not say the crates hold onions for the potatoes (N7).
- **The cloud's stand-ins only (10):**
  - LIT-01 and LIT-02 are computed on the card's bake. My reflection-off room means agree: 40.8 and 43.3 by day, 78.5 and 86.7 at night.
  - LIT-02b, LIT-05, LIT-07, LIT-08, PIC-05g, GLS-03 and GLS-04 are measured under the gate's glass, spill and lamps. I repeated GLS-03 and GLS-04.
  - PRJ-02 is the gate's own `trace`, as the row says.
- **Pending:** SCN-01. **N/A, rightly:** SO-05, FAS-02, LIT-03 and PRV-01.
  - FRN-09 (the hall behind a side door) and FRN-11 (a hanging sign) are absent because the shop has neither. FRN-12 is absent because 4.1 drew no hours plate (N3).

**Measurements I could not repeat:**
- LIT-01 and LIT-02 on the card's bake alone: I measured the room pixels of the reflection-off renders instead.
- DSP-03's silhouette shares: the object-index picture is there, but its colour key is not.
- LIT-08: the close view's.

## What I cannot judge from these files

**The game's glass:**
- the street and sky in the panes and in the glass fascia (the Hook sheet's bar, RULINGS 3 October);
- the dirt.

**The game's light:**
- Lumen on the display, and the spill and its pool (PC-02);
- the exposure;
- the street lamps;
- the lobby lamp once built (N1).

**Wear:**
- The front is spotless: the cream render and the green slabs show no grime. The Hook sheet and P1 are grimy.
- The D53 layer is owed on the PC (PC-05).

**The lobby's lower 0.55 m in the gate frames:**
- I saw it only in my own quick render of the glb (24 samples, a grey sky, no room behind).
- The lobby floor's look under the game's light is owed.

**The pictures in motion:**
- TSR, and the card's parallax as the player walks.
- The gate frames are 32 samples a pixel (NOTES' times), not the 64 the brief names.
- Through the door the room's floor shows 0.55 m too high, the method's known cost. A kick panel to 0.60 hides almost all of it from the street.

**The pending produce (the Sketchfab scans):**
- cabbage, potato, satsuma and pear.

**For the close reviewer, noticed in passing:**
- The shop bell (`bell_brass`, y_m 0.716 to 0.786) hangs behind the card plane (y_m 0.58). It cannot be seen in the gate or in the game.

**Next:**
1. The kit: fix the reveal floor (shared) and re-render the four street frames.
2. The builder: N1 to N7. N1 and N2 are the ones a player sees.
3. The target's owner: 4.1's hours plate (N3).

None of these blocks the pass. Do not show the street pictures to Jafar until the reveal floor is fixed.
