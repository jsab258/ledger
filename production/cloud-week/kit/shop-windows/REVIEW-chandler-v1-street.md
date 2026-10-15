PASS

# The ship chandler (east_chandler bay 0, no. 13), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not write the target, the kit or this shop. I judged the street view only (STREET_SQUARE and STREET_30, day and night_lit). I did not read the close view's review or any other shop's review. Jafar's ruling of 9 October applies: a piece that fails only on narrow points passes, with those points listed for the builder.

**What I read:** CLAUDE.md; RULINGS.md (1, 2, 3 and 8 October); NOTES.md ("For the next nine shops", batch A's and batch B's lessons 16 to 41, "Batch B" and the chandler's own section); TARGET.md section 3, table 5.6 and section 13 (B8, B9, B12, B13, T2-5, T2-16); Rita's four reviews; `checks/check_chandler_v1.json` (all 72 rows); the parts of `sw_gate.py`, `check_try3.py`, `check_shop.py` and `sw_ctx.py` behind what I saw.

**What I looked at:**
- The previews `chandler-street-square-{day,night-lit}`, the three room pictures, and Rita's approved front (`ritas-street-square-day-v3`).
- The gate frames STREET_SQUARE and STREET_30, day and night_lit, at 2560 x 1440, in crops up to 5 times.
- The Hook sheet.
- The 4.1 board as exported (`chandler_basecolour_worn.png`).
- The 1k clean base-colour map of each of the 13 placed models.

**What I measured:**
- Rec.709 luma (0 to 255) over the gate's own glass and room masks (`check_*_mask.png`, `check_*_room.png`), which are all still in the folder, so every measure below is repeated, not copied.
- The glbs' JSON and their normal maps.
- The front's member boxes (`front_members.json`) and the hanging sign's UVs in Blender.
- The kit's newer rows (`check_try3.py`: FRN-13, SIGN-01, DSP-09, DSP-10, DSP-11, FLT-01/02, INV-07, INV-08), run on this shop in memory. Nothing was written to the repository.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview).

**Verdict.** No fault blocks. The front reads as a British Victorian parade shopfront with a 1960s-70s aluminium refit, and the trade reads from across the street. The window is glass with a lit, stocked room behind it by day and at night. There are ten narrow points, each with an exact fix. The worst three:
1. The paint pyramid's backing board is pale primer grey. This is the fault the ironmonger's review found, and the kit's DSP-11 row was written for it.
2. The shop door's lower glass shows the gate's flat reveal slab (FRN-13 fails).
3. The door has no hours plate, although NOTES says it has one.

## Faults, worst first

None.

## Narrow points, most visible first (each with its exact fix)

### 1. The pyramid's backing board is a pale flat board, the palest field in the right light (DSP-11 fails)

- **Where:** STREET_SQUARE day, behind the pyramid of 21 paint tins: x 1515 to 1650, y 795 to 920 (1600: x 948 to 1030, y 497 to 575). At night the same board reads cream.
- **Measured:**
  - DSP-11 run on this shop: 5,039 visible pixels, mean luma 102.8 (p5 82.6, p95 124.9), against the wanted 25 to 45.
  - My own boxes: 115.7 (sd 1.0) on its lit left part and 85.5 on its right, by day; 109 to 116 at night.
  - It reads as a white card stood in the window, the same "primer grey" the ironmonger's board had.
- **Why it was missed:** `check_shop.py` runs DSP-11 only `if ctx.id == "ironmonger"`. DSP-09 also fails: `pyramid_backing` is a flat factor with no picture.
- **WHOSE:** the builder (the board's colour) and the kit (the row's scope).
- **EXACT FIX:**
  1. Give `pyramid_backing` the base colour sRGB (52, 46, 40), dark stained deal, roughness 0.8, with the room's timber picture, so DSP-09 passes.
  2. Re-render the gate's day and night_lit frames. DSP-11 at STREET_SQUARE by day must read 25 to 45.
  3. In `check_shop.py`, run DSP-11 for every display that has a `script:backing_board`, not only the ironmonger's.

### 2. The shop door's lower glass shows the gate's flat reveal slab (FRN-13 fails)

- **Where:**
  - STREET_SQUARE: the M1 door below the room's floor line, x 700 to 855, y 925 to 1015 (1600: x 437 to 534, y 578 to 634).
  - By day it is flat grey, luma 55.6, sd 1.3. A lit ledge sits above it at y 925 to 937 (luma 97.5).
  - At night it is near black: 6.2, sd 0.7, under a lit room.
- **FRN-13 run on this shop:**
  - 157 of 560 rays from STREET_SQUARE end on `reveal_floor_shop_door`, 131 of 560 from STREET_30, and 76 and 134 from the close cameras.
- **Why narrow from here:** from the far pavement it reads as the door's kick panel under a mid-rail.
- **Why it matters in the game:**
  - The slab is the gate's alone (`sw_gate.reveal_specs`); it is not in `chandler_front.glb`, so what the game shows there is not defined.
  - The cause is the target's: the M1 door is glazed from 198, while the card's floor stands 0.55 above the footway.
  - This is Jafar's open glass-foot question on Rita's door (871, 600 or about 1000) asked again for this door. From 8.76 m, the card's floor projects onto the door glass at about 0.62 m; from the close camera, at about 0.85 m.
- **WHOSE:** the target, and the gate (a flat 0.02 grey slab).
- **EXACT FIX (recommended, pending his answer on the glass foot):**
  - Give the chandler's M1 leaf an aluminium kick panel from z 28 to 650, glazed from 650, as the M2's panel to 600, raised 50 because of the 0.62 sight line.
  - FRN-13 at both street cameras then reads 0.
  - If he keeps the glass to 198, the front glb (not only the gate) must carry, in the door zone, a floor at the footway in the room's boards from the leaf back to the card, and a riser under the card's edge in the dado green (40, 84, 59). FRN-13 then counts that floor as floor.

### 3. No hours plate on the door, although NOTES says there is one

- **Where:** STREET_SQUARE day, the shop door's glass under the OPEN card, x 735 to 840, y 760 to 840. It is empty glass.
- **Measured:**
  - `front_members.json` has no hours member, only `door_sign_open`.
  - The check has no FRN-12 row.
  - NOTES "What was made" says "the OPEN card and the engraved hours card", and "Where a fresh reviewer should look first" says "the hours plate under the OPEN card".
  - TARGET T2-5 puts an hours plate on every shop's door, as on Rita's approved front ("MON-SAT 9-5.30 / WED 9-1 / SUN CLOSED").
- **WHOSE:** the builder (the claim and the missing part) and the kit (4.1 drew no chandler plate).
- **EXACT FIX:**
  1. Add a 4.1 hours plate for the chandler from the target's hours: "MON-SAT 8-5 / WED 8-1 / SUN CLOSED", 300 x 190, the launderette's engraved laminate style.
  2. Place it as FRN-12 places it: top z 1380, centred on the door, behind the glass at the OPEN card's depth (d 37).
  3. Add FRN-12 to this shop's check.
  4. Strike the claim from NOTES.

### 4. A flake of the board's wear sits on top of the I in SHIP, so it reads "SHİP"

- **Where:**
  - STREET_SQUARE x 892 to 903, y 296 to 303 (1600: about x 559, y 186).
  - STREET_30 x 1003 to 1013, y 380 to 386, where it shows plainly at 1600.
  - A second flake beside the interpunct after ROPE makes the dot read double (STREET_SQUARE x 925 to 940, y 352 to 358).
- **Cause:** on the 4.1 board (`chandler_basecolour`, 1 px a mm), the flakes are at about (2050, 108), 50 x 25 mm, directly over the I, and at about (2180, 352).
- **WHOSE:** the kit (4.1's wear for this board).
- **EXACT FIX:**
  1. In `make_fascias.py`, delete those two flakes from the chandler board's wear.
  2. Add a rule for every board: no flake whose centre lies within 60 mm above a capital's cap line inside that letter's width, and none within 30 mm of an interpunct.
  3. Re-export the board.

### 5. The side door's transom drip burns white: the timber parts carry the aluminium metal

- **Where:**
  - STREET_SQUARE day x 484 to 640, y 574 to 582: about 1,200 pixels at 255 (1600: the white bar over the navy side door, y 359 to 364).
  - STREET_30: 513 pixels.
- **Cause:**
  - The F1 frame (`frame_jamb_L/R`, `frame_head`, `frame_transom`, the stop beads) and the raised-and-fielded panel over the side door (`band_panel_*`) are timber joinery.
  - In the glb they carry `paint_alu_natural`: metallic 0.9, roughness 0.38.
  - The transom's top face mirrors the overcast sky at full white, and the panel reads as metal.
- **WHOSE:** the builder (the front's material map for `alterations.aluminium_refit`).
- **EXACT FIX:**
  1. Give those members a painted timber material: sRGB (176, 178, 180), metallic 0, roughness 0.5, as `paint_navy` is set.
  2. Keep `paint_alu_natural` for the M1 window, the M1 door and their beads and bars only.
  3. Add a check: in the day street frames, no front pixel outside the glass is at 250 or above.

### 6. STREET_30's left light is one flat stretch of bare plaster (FLT-02 fails)

- **Where:** STREET_30 day, x 1082 to 1174, y 551 to 701 (1600: x 676 to 734, y 344 to 438). It is the rear half of the room's left wall above the dado, luma 50.
- **Measured:** FLT-02 run on this shop gives 4.70 per cent of the glass as one patch of 9 x 9 standard deviation under 1, against the default 3.0. STREET_SQUARE gives 1.63 (the right wall's dado, luma 27). FLT-01, for the display's own pieces, passes at 0.34 and 0.33.
- **Why narrow:** it reads as a wall, not a void.
- **WHOSE:** the builder (the left wall's layout: the charts all hang on its front half).
- **EXACT FIX:**
  1. Move the coil board and the tide table to the left wall's last 1.2 m before the back wall (room picture x 290 to 360 of the 1600 room preview), at z 1.1 to 1.9, stand-off 0.05.
  2. Add two of the six chart designs beside them.
  3. Re-render the room and the gate. FLT-02 at STREET_30 must read under 3.0 per cent.

### 7. LIT-02b, the builder's open row: shade under the lowest board, not a void

- **Where:**
  - STREET_SQUARE day x 978 to 1038, y 800 to 858: the boots' floor seen through the lifebuoy's hole. It is luma 7.7 with the reflection off, but 22.7 in the beauty frame, where 31 per cent is under 12.
  - STREET_30 day x 1196 to 1230, y 708 to 836: the green dado behind the left jacket, 13.8 in the beauty frame.
- **Measured:**
  - My largest room-only patch is 0.79 and 0.95 per cent of the glass. The check reads 1.17 and 1.40; it decodes the room mask differently, so I could not repeat its exact number.
  - In the beauty frames the largest connected patch under 12 is 0.11 and 0.52 per cent.
- **Why narrow:** it reads as shade under a shelf and behind a hanging good, as the kit's lesson 6 means it to.
- **WHOSE:** the builder.
- **EXACT FIX:** the builder's own. Take the day fill to 50 W (its test read 0.0030), render the day picture alone (`LEDGER_ROOM_STATES=day LEDGER_REUSE_CAL=1`), then re-run the gate's day frames.

### 8. The door card reads OPEN at night, against the hours rule the kit now runs (SIGN-01 fails)

- **Where:** STREET_SQUARE night_lit, the card at x 750 to 800, y 705 to 735.
- **The rules disagree:**
  - The target's hours shut the chandler at 17:00 and light it at night "as the street file has it".
  - `sw_ctx` (NIGHT_HOUR 20) gives `open_at_night = False`, so SIGN-01 wants CLOSED at night_lit.
  - This gate predates the rule: its camera files carry no `door_sign`, and its card reads OPEN, following batch B's item 7, "a lit shop is open".
  - This is the reverse case of the shared finding (f).
- **WHOSE:** the kit (two rules) and the target's owner (lit and shut, or lit and open).
- **EXACT FIX:** re-run the gate's night frames with the current kit, so the card reads CLOSED and SIGN-01 passes. Only if the target's owner rules the lit chandler open does its Saturday hour move past 20:00 in target.json, with the card left OPEN.

### 9. From STREET_SQUARE the two sou'westers read as yellow hard hats

- **Where:**
  - STREET_SQUARE day x 1205 to 1258, y 645 to 705 and x 1405 to 1450, y 640 to 700 (1600: x 753 to 786, y 403 to 440 and x 878 to 906, y 400 to 438).
  - Each is a smooth dome with an even brim and a band: a builder's helmet at the window's centre, in its most saturated colour.
  - At STREET_30 the long back brim shows and they read better.
- **WHOSE:** the builder (the scripted pattern). The close view rules the hat itself.
- **EXACT FIX (helps both views):**
  - Make the back brim 1.8 times the front brim, sloping down 20 to 25 degrees.
  - Lower the crown to no more than 0.6 of the front-to-back brim radius, with a seam over it.
  - Hang chin ties 150 mm long.
  - Turn each hat 60 to 90 degrees on its cord, so the far pavement sees its profile.

### 10. The display's jackets are toned to burgundy-brown by day

- **Where:**
  - STREET_SQUARE day, the two display jackets, x 1120 to 1275 and 1365 to 1515, y 600 to 820.
  - They read dull burgundy beside the room's two jackets of the same model on the hooks board, which read orange (x 1200 to 1365, y 540 to 590).
- **Cause:** C11 tones them by 0.40 so that the night's red channel does not burn.
- **Why narrow:** the shape and straps still say "life jacket".
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Tone at 0.65.
  2. Run the two 8-sample close night frames (lesson 33).
  3. If PIC-05g stays at 0.01 or under, keep 0.65. If not, take the spill from 150 to 130 W and confirm LIT-08 at 0.6 or more.

## The check's rows: which I trust

- **The check is a day behind the kit.** It was made 14 October 18:15. Today's `check_shop.py` adds FRN-13, SIGN-01, DSP-09, DSP-10, INV-07, INV-08, FLT-01 and FLT-02 for every shop after Rita's.
- **My in-memory run of those rows on this shop:**
  - FRN-13 **fail** (point 2);
  - SIGN-01 **fail** (point 8);
  - DSP-09 **fail**: eight flat supports, the close view's except the backing board (point 1);
  - DSP-10 n/a;
  - INV-07 pass;
  - INV-08 pass (0 legible lines);
  - FLT-01 pass (0.34 per cent);
  - FLT-02 **fail** (4.70, point 6);
  - DSP-11, which the kit skips here, **fail** (102.8, point 1).
- **Exact fix:** run `python3 build_shop.py --shop chandler checks` with today's code, after the fixes above, as `check_chandler_v2.json`.
- **Trusted (repeated or agreeing with my own measure):**
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-04, SO-06, SO-07, DSP-01 to DSP-07, INV-01 to INV-06, NEV-01, NEV-02;
  - GLB-01 and FAS-01n: my own read of both glbs gives the fascia's normal map mean (127.5, 127.5, 254.9), and every display normal map blue 160 or more on 99.1 to 100 per cent;
  - FAS-03: 0 textured primitives without TEXCOORD_0 in either glb, 0 negative texCoord;
  - FRN-01 to FRN-05, FRN-07 to FRN-11, FAS-01, FAS-01c, FAS-02, GLS-01, GLS-02, TRD-01, NIT-01, CAM-01, X-PRV, ROOM-02, ROOM-03.
- **Pass but do not prove what they say:**
  - ROOM-01 and ROOM-05 count each `rubber_boots` placement as one pair. The Poly Haven model holds two pairs (a clean and a dirty pair, four meshes), so the room has 4 pairs (the target's 4) and the window 2 pairs (the target's 3), not 2 and 1. NOTES C1, B8 and B9 carry the same error. **Exact fix:** count boots as meshes / 2 and correct the three lines.
- **The cloud's stand-ins only:**
  - LIT-01 and LIT-02 are on the card's bake.
  - LIT-02b, LIT-05, LIT-07, LIT-08, PIC-05g, GLS-03 and GLS-04 are under the gate's glass, spill and lamps.
  - GLS-05 tests the gate's glass, not the game's.
  - PRJ-02 is the gate's own `trace`.

## The builder's named shortfalls, judged from the street

| shortfall | my judgement |
|---|---|
| the counts do not fit at real size (window: 3 coils of 5, boots, 2 small cans of 3) | **narrow, and the window still reads as a chandler's.** From 8.76 m: a lifebuoy, two jackets, three hung coils, four green boots, lanterns, oil tins, red oil cans and a pyramid of paint, with the room's rope on edge, paint, lanterns, buoy, jackets and lifebuoy behind. The boots are in fact 2 pairs (see the rows above) |
| LIT-02b at the day frames | **narrow** (point 7) |
| the sou'westers read as yellow hats | **narrow from the street** (point 9); the close view rules |
| charts and tide table drawn by script | **narrow.** Seen from the street only as two small sheets through the shop door at STREET_30; printed CC0 pictures are owed |
| the marker buoy 1.5 m tall at the left end | **not a fault from here.** Through the shop door it reads as a red marker buoy shown on its own tail weight |
| the mesh screens built and not shown | **right.** The lit night is the shop's night; the screens are the shut shop's |
| narrow passes (PIC-05g 0.0077 at CLOSE_35, LIT-08 0.80, GLS-04) | the close view's. At the street cameras PIC-05g reads 0.0005 to 0.0007 and GLS-04 reads 0 |
| 48 samples | no visible noise at street distance |

## Shared, known (named, not counted in this verdict)

- **(a) The burnt orange bar in the night glass:** not here. GLS-04 is 0 px at both street cameras and none shows.
- **(b) Hot top corners in night_dark:** not here. The corners read 4.7 and 5.0 against a mean of 16.6.
- **(c) Glass parts dropped:** not seen. The lanterns', the till's and the flashlight's glass are kept (DSP-07).
- **(e) Sheets leaning toward the glass:** nothing of the kind visible from the street. DSP-05 reads 0.
- **(f) CLOSED at night on a lit shop:** the reverse here. The card reads OPEN at night against the hours rule (point 8).
- **(g) Child-size furniture:** the display has no furniture. The room's counter reads a normal height from the street.

## What is right

**The front:**
- It reads as a Victorian parade's timber shopfront with a later aluminium window and door:
  - navy panelled pilasters on plinths and scroll consoles;
  - a 550 board under a timber cornice;
  - an aluminium M1 window of three lights with three toplights and the mullions carried up;
  - a tiled stallriser with a black plinth course;
  - the panelled F1 side door with its fanlight and the panel above it;
  - the aluminium shop door under a fanlight and three toplights;
  - the band over both doors, closed.
- Rita's lessons hold:
  - no black strip beside the side door: 0.08 per cent of the front under luma 8, no patch of 35 mm;
  - no sky slot at STREET_30: brick behind the right pilaster, FRN-08 0 px;
  - no stand-in light in the glass: head band 0 burnt, mullions 24.7 against glass 57.9.
- Its navy, grey and pale green tile sit with the Hook sheet's blue-grey, tiled Mickey's. Its proportions are Rita's approved front's.
- **Nothing is mirrored:**
  - Both faces of the hanging board map with their text the right way from outside; I checked the UV handedness.
  - The shop door's pull is on the lever stile and its hinges on the window side, as the target says.
  - The side door's lock is on the pier side.
- **The hanging sign is clear of the cornice:**
  - The board's inner edge stands 330 out, against the cornice's 300 and the consoles' 290.
  - The inner chain hangs at 380 to 401, so 80 mm clear.
  - Its wall plate stands on the brick above the cornice.
  - FRN-11 finds no pair that intersects.

**The lettering reads:**
- SHIP CHANDLER and ROPE · PAINT · CHARTS · TWINE: letters to ground 2.99 by day (FAS-01c; my boxes agree). At night the cream paint still reads against the dark board at both cameras.
- The two 13s on the board, the gold 13 on the fanlight, EST. 1879 on the middle toplight (whole: GLS-02, and seen), CHANDLERY on the hanging board, and OPEN.

**The window is glass with a lit, stocked room behind it.** No part of it is a void or a white board, apart from narrow point 1's board.

| measure (glass of the three lights, eroded) | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, mean luma | 52.7 (p5 20.4, p95 109.3) | 53.2 (p5 17.7, p95 112.8) |
| day, under 3 / under 12 | 0 / 0.62% | 0 / 1.40% |
| day, largest connected patch under 12 (beauty frame) | 0.11% | 0.52% |
| brick beside, day | 83.8: the glass is 0.63 of the wall, dimmer, as Rita's 0.69 and the photographs have it | 83.6 |
| night_lit, mean luma | 71.3 | 68.2 |
| brick beside, night | 20.9: the window is 3.4 times the wall | 21.0: 3.2 times |
| night, a channel at 250 or above | 0.89% (the white coil, the hats and the labels under the spill) | 0.99% |

**The trade reads from the street:**
- the board and the hanging CHANDLERY;
- a lifebuoy and two life jackets;
- three coils on pegs, boots, lanterns, oil tins, red oil cans and the paint pyramid;
- behind them, rope coils on edge, rows of paint, lanterns, a red marker buoy (through the door), the hooks board with jackets and a lifebuoy, and a pegboard of hardware.

**Content:**
- No drink, gambling, child or person.
- No flare or anything that reads as a weapon. The blowtorch reads as a tool.
- Nothing after 1992 at street distance.

**Every word legible at 100 per cent in the four frames:**
- SHIP CHANDLER, ROPE, PAINT, CHARTS, TWINE, 13 (three times), EST. 1879, CHANDLERY, OPEN.
- On the tins, in part: HULL PAINT, WHITE SPIRIT, TEAK OIL, DECK PAINT.
- All are the project's own or plain trade words. Acceptable.
- The makers PENHALE, TREGENNA and WESTHAVEN, the price cards and the charts are not legible from the street.
- Of the 13 models' clean 1k maps, none shows a mark that could read at street distance.

**For the close view** (not judged here): the compass's dial map keeps a line of script beside the rose (mirrored in the map, about "R.ADOLIER"). It is not on the blanking list and may be a maker's name; read it at 100 per cent.

## What I cannot judge from these files

- **The game's glass:** the street and the sky in the panes (the Hook sheet's bar, RULINGS 3 October), dirt, and the night hand-over. Here the glass reflects an empty gate.
- **The game's light:** Lumen on the display, the game's spill and its pool (PC-02), the street lamps' pools, the exposure and TSR.
- **What the game shows under the card through the shop door** (point 2): the reveal slab is the gate's only.
- **Wear and wet on the front:** it is spotless. The D53 layer is owed (PC-05).
- **Whether the street facade closes the 30 mm beside each pilaster** (PC-04).
- **Whether 2.54 m** (4.1's lowest edge of the hanging board, above the footway) meets the town's clearance over a footway. I did not research it.
- **What I could not repeat:** the check's exact LIT-02b patch shares (see point 7). Every other street measurement was repeated from the frames and masks still in the scratch folder.

**Next:** fix points 1, 2 (his glass-foot answer), 3 and 5 in the front and display. Re-render the gate's four street frames with today's kit, so point 8 and the newer rows come with it. Point 4 goes to the 4.1 board, and points 6, 7 and 10 to the room and the gate. Then run today's check as v2. None of this blocks the pass.
