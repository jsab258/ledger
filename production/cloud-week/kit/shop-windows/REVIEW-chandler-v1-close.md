FAIL

# The ship chandler, the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2; 15 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. One view only: CLOSE_35 and CLOSE_35_B, by day and night_lit. I did not read the street review of this shop or any other shop's review.

**Read:**
- CLAUDE.md and RULINGS.md (2 Oct, 3 Oct, 1 Oct, 9 Oct);
- in NOTES.md: "For the next nine shops", lessons 16 to 41, "Batch B" and the chandler's own section;
- in TARGET.md: section 3, table 5.6 and section 13 (to the end of batch A try 2);
- Rita's four reviews;
- `checks/check_chandler_v1.json`, all 72 rows;
- the chandler's display code (`sw_shops_chandler.display`), `sw_goods_b.souwester`, the gate's reveal and hall-face code, and `check_try3.py`'s row list.

**Looked at:**
- the seven 13 October previews;
- the eight gate frames, at 100 to 400 per cent;
- the reflection-off, mask and room check renders;
- the baked cards and the three room pictures;
- every placed model's 1k base colour map (the `_clean` copy where one exists).

**Measured** (scripts in my scratchpad; nothing in the repository or the scratch folder was changed):
- the parallax, through `trace` itself;
- glass luma, dark share, flat patches and burnt pixels on the frames;
- the glbs' normal maps and UVs, read from the files;
- the colours baked into the display glb;
- MANIFEST-chandler.json against the files.

**In short:** the projected room works, and the window reads as a ship chandler's. It has a lifebuoy, life jackets, rope, sea boots, hurricane lamps, compasses, oil tins and cans, a paint pyramid and a blowlamp, all at real size, with nothing buried and nothing through anything. The front's door parts are right and there are no black strips.

**One fault:** the two sou'westers, hung at eye height in the middle of the window, read as yellow builders' hard hats from both close cameras. The card beside them says SOU'WESTERS. That fault alone decides the FAIL. Its fix is one scripted mesh.

There are 13 narrow points. The most visible are:
- the life jackets are toned dull maroon in the game's own asset;
- the display rails hang on cords that stop 0.25 m short of the window head;
- the paint pyramid stands on a flat, untextured board (2.9 per cent of the glass);
- through the shop door's glass you see a bare hall wall and the gate's floor slab, dark at night.

**1 fault, 13 narrow points.** Try 1 of the close view.

## Fault

### F1. The sou'westers read as hard hats

- **Where (2560 frames; preview = x 0.625):**
  - CLOSE_35 day: left hat (1055-1220, 420-590), right hat (1590-1755, 380-590).
  - CLOSE_35_B day: (1088-1256, 392-584) and (1533-1680, 424-584).
  - Night: the same places.
- **What you see** at 100 per cent:
  - a rigid hemispherical shell with raised rib seams, which is a hard hat's crown;
  - a narrow flat rim at the front and sides;
  - one large flat lobe that, from 35 degrees, reads as a visor hanging down.
- The SOU'WESTERS £2.95 card (CLOSE_35 day 1740-1795, 365-410) names something the eye does not see. The builder says the same thing in its shortfalls.
- At night the two crowns are the window's largest burnt patches: 5,669 and 3,993 px at 250 in a channel, of the 28,486 that make PIC-05g's 0.0077.
- A chandler's window with two builders' helmets in its middle is the one thing here that reads as another trade.
- **Cause:** `sw_goods_b.souwester`. The code makes:
  - a crown that is a true hemisphere (h_c = r_c, 0.095 m at s 0.85) with six seams built as raised 1.6 mm rods;
  - a brim that is 25 mm wide and almost flat round the front and sides, with all its length in one back lobe (2.45 r_c, dropping 0.16 m);
  - `face=-1`, which turns that lobe straight into the shop, where from 35 degrees it reads as a peak.
- **Whose:** the builder (the shared helper in `sw_goods_b.py`; no other shop uses it yet).
- **Exact fix.** Change `souwester` and its call in `sw_shops_chandler.display`:
  1. **Crown:** an oblate dome, height 0.70 x r_c (0.058 m at s 0.85), on a 15 mm upright band. Four panels, not six. The seams are inset grooves drawn in the map: 1.5 mm dark lines at 0.6 of the base value, with no rods. Add 1.5 mm vertex noise so the oilskin is soft, not a shell.
  2. **Brim:** it goes all the way round and slopes down.
     - 55 mm wide at 30 degrees down over the front and sides, widening smoothly (cosine) to 130 mm at 45 degrees down at the back, which is the neck flap.
     - Four rows of stitching 6 mm apart, 4 to 28 mm in from the edge, drawn as lines at 0.6 of the base value.
     - The brim keeps its 3 mm thickness.
  3. **Chin ties:** two 3 mm cotton ties (200, 190, 160) from inside the brim at the ears (theta 0 and pi), 200 mm long. Each hat hangs by its ties knotted over the front rail, in place of the present strap to the crown. The hat tips so its crown faces the street at about 60 degrees: the whole brim and the long neck flap show from STREET_SQUARE and both close cameras.
  4. **Turn the hat about its axis** so the neck flap points along the window (face along +x for the left hat, -x for the right). From 35 degrees the profile then reads short front and long back.
  5. **Oilskin:** base (205, 165, 35) sRGB at 0.8 of the current value for the night (the crowns burn now), roughness 0.28. Add a CC0 crumple normal (ambientCG Leather or Fabric, strength 0.3, 0.15 m tile), with a catalogue line.
- **Check:** DSP-03 and DSP-05 again (the ties end on the rail, as DSP-10 asks). Then two 8-sample close night frames for PIC-05g, as lesson 33 says.

## Narrow points, most visible first (each with its exact fix)

### N1. The life jackets are toned dull maroon, in the game's asset, for the cloud's stand-in light

- **Where:** CLOSE_35 day, the display's jackets (1820-1920, 660-800 and 1060-1120, 580-720).
  - With the reflection off they read (59-62, 34-40, 33-38): hue 4 to 5 degrees, saturation 0.4, value 0.23. That is dusty maroon, like leather cushions.
  - The same model on the room's hooks board in the same frame (1756-1796, 430-520) reads (96, 47, 34): hue 13, saturation 0.64. That is life-jacket orange.
  - At night the display's jackets come back to orange-brown (93-102, 44-54, 32-39).
- **Cause:** `d.tone(jackets, 0.40)`, made to keep PIC-05g under the gate's 150 W spill.
  - I read the display glb itself: `life_jacket_diff_1k` there averages (87, 50, 40) against the source's (218, 102, 74).
  - `Lantern_01_brass` there is (229, 228, 204): x4.5 clipped toward white.
  - So the toning is in the game's asset, not only in the gate's render. Under Lumen the game would show maroon jackets and cream lanterns.
- **Whose:** the kit (lesson 36, "toned at build time") and the builder.
- **Exact fix:**
  - `chandler_display.glb` keeps every model's own base colour (tone 1.0, metal 1.0).
  - Any toning becomes a gate-only material multiplier, applied to the night frames only. The day frames render the jackets at 1.0.
  - Where PIC-05g then fails at night, it is a stand-in shortfall written under PC-02, not paint on the asset.
  - Lesson 36 is reworded: "tone in the gate's scene, never in the exported glb".

### N2. The display rails hang on cords that end in mid-air, and the jackets are not hung from anything

- **Where:**
  - CLOSE_35 night (reflection off, 2560): the back rail's left cord ends at (990, 240) and its right cord at (2072, 130), both against the room's lit wall and ceiling.
  - CLOSE_35_B night (reflection off): the front rail's right cord ends at (1875, 275) against the return wall's plaster. It is plain at 100 per cent.
- **Cause:** `gm.rod(..., (X(xx), rail_v, 1.55))` stops every cord at w 1.55, the display's height cap.
  - The window's lower lights run to model z 2.400 (`win_glass_lower_0`) and the bed is at z 0.600, so the transom's underside is at w 1.80: the cords stop 0.25 m short.
  - The life jackets touch the back rail's underside (top at rail_w - 0.013) with no hook, loop or cord. DSP-05 passes them because they touch.
  - DSP-10 (every cord ends on something), which the kit added after the ironmonger's close review, was not run on this shop.
- **Whose:** the builder.
- **Exact fix:**
  - Run the four rail cords to w 1.798, each ending in a 15 mm brass screw-eye (rod 2 mm, ring 15 mm) on the transom's underside.
  - Lower each jacket 30 mm and hang it by two 3 mm cord loops (40 mm across, round the rail) from its top edge, 0.15 m either side of its centre.
  - Run DSP-10 on this shop.

### N3. The paint pyramid's backing board, the bed and the compass riser are flat colours

- **Where:** CLOSE_35 day, the board (2015-2559, 902-1315). It is the largest flat patch in the window (9 x 9 px standard deviation under 1): 69,616 px, 2.9 per cent of the glass, mean luma 99. At night it is 3.4 per cent (mean 112).
  - The bed (`bed_board`, `bed_paint`) and the compass riser are flat factors with no picture. The bed reads as clean plastic pine under every good (CLOSE_35 day 600-2000, 900-1200).
- **Whose:** the builder.
  - DSP-09 (no flat support), DSP-11 (the backing board's luma) and FLT-01 (the display's largest flat tone, 1 per cent of the glass) are the kit's rows from the ironmonger's reviews. They were not run on this shop.
  - FLT-01 would fail at 2.9 per cent.
- **Exact fix:**
  - The backing board becomes painted plywood with a grain picture (the ironmonger's T2-2 board: painted, luma 25 to 45 by day) in a dark marine colour, (52, 70, 62).
  - The bed and the riser take the room floor's old_wooden_floor_02 picture at 0.8 of its value (a worn, oiled window bed).
  - Then DSP-09, DSP-11 and FLT-01 at 1 per cent.

### N4. Through the shop door's glass: the side hall's bare wall and the gate's floor slab, dark at night

- **Where:** CLOSE_35, the shop door's glass.
  - **Upper part** (360-500, 430-900): a flat plaster plane. By day it reads luma 91 to 102. At night it is 19 to 23 (23 to 27 with the reflection off), beside a lit room at 60 to 74.
  - **Lower part** (390-540, 930-1150): a grey box. By day it is 75; at night it is 8 with the reflection off.
  - So a lit shop showing OPEN has a dark door.
- **Cause:**
  - The upper plane is `hall_wall_r`, the outside face of the side door's hall (u 1274-1294, d 0 to -500, hall_plaster (150, 142, 124)).
  - The box is the gate's floor slab under the card (top at 0.55 above the footway), standing behind the flush door.
- **Whose:** the kit's 14 October fixes were not applied to this build. `sw_front` now puts `hall_face_dado` and `hall_face_plaster` on that face, and the gate paints it with the room's wall column (the ironmonger's close review, narrow 3). FRN-13 was written for the slab. The chandler's front (14 Oct 04:03) has neither, and FRN-13 casts its rays from the street cameras only. The card's floor at 0.55 is the target's known X1.
- **Exact fix:**
  - Rebuild the front and the gate on the current kit (hall faces in the glb and the gate, lit at night as the return walls are).
  - Run FRN-13 also from CLOSE_35 and CLOSE_35_B.
  - For the slab: either the X1 change for this shop's door zone (card to the footway, H 2.95, picture 4096 x 2280), or, until the target's owner decides X1, the shop-door floor slab's top at z 0.02 with the room's boards at the card's brightness.

### N5. The rope coils are loose rings of 2 to 2.6 turns, not hanks

- **Where:** CLOSE_35 day:
  - the yellow coil (1220-1400, 320-520);
  - the orange coil (1415-1530, 315-455);
  - the white coil (1790-2080, 250-505).
- **What you see:**
  - Each is about 1 to 1.6 m of rope in a perfect open spiral, with cut, unwhipped ends (the white coil's end at 1640-1665, 240-275).
  - It reads as rope, but as an offcut, not as stock sold by the hank.
  - The twisted-strand map reads well at 100 per cent.
- **Whose:** the builder.
- **Exact fix:** each coil becomes a hank:
  - 12 to 16 turns in 3 or 4 layers, rope radius kept;
  - outer diameter 0.30 to 0.36 m (big) and 0.22 (small);
  - three seizings of tarred twine (90, 70, 45), 2 mm, six turns, 10 mm wide, at 120 degrees round the coil;
  - both ends whipped (15 mm of white twine) and tucked under the last turn;
  - hung on its peg by the top seizing.
- Check DSP-05 (the coil's highest quarter on the peg) and DSP-03 again.

### N6. LIT-02b at CLOSE_35_B by day: shade under the shelving, not a void

- **Where:** CLOSE_35_B day, reflection off. The dark pixels are the lowest zone of the room's shelving (the red cans and the boots' floor) and the shaded dado at the room's left: 2560 (0-710, 580-840).
- **I repeated the row** on the check renders:

  | camera | share of the glass under luma 12 | largest patch |
  |---|---|---|
  | CLOSE_35_B | 0.0115 | 0.0019 |
  | CLOSE_35 | 0.0072 | 0.0022 |

  The largest patch is a fifth of the limit. There is no slab anywhere, and the far end of the window from CLOSE_35_B is the return wall (see "What is right").
- **Whose:** the room's dark dado, as the builder says.
- **Exact fix:** the builder's own third step:
  - the day fill (`FILL_W` by day) from 20 to 50 W (its test read 0.0076 to 0.0030);
  - the day picture rendered again alone (`LEDGER_ROOM_STATES=day LEDGER_REUSE_CAL=1`);
  - the gate's day frames again.

### N7. The rigging pegboard is mostly bare

- **Where:** CLOSE_35 night, the room's right wall (2255-2445, 70-640): six blocks, nine shackles, six cleats, a few short chains in four thin rows on a 1.6 x 1.1 board. Also in the room picture (1320-1450, 165-435 of the 1600 preview).
- **Whose:** the target (24 pieces) and the builder. ROOM-02 passes on the count alone.
- **Exact fix:** fill by rows across the board's full 1.6 m, each row's pieces 0.04 to 0.06 apart and 80 per cent of the width (Rita's ROOM-02 rule), at most 0.10 off the wall (SO-02):

  | height | pieces |
  |---|---|
  | z 1.95 | 8 wooden blocks, single and double sheave |
  | z 1.70 | 14 shackles of three sizes |
  | z 1.45 | 10 cleats |
  | z 1.15 | 6 hanks of small line |
  | z 0.85 | 4 lengths of galvanised chain hung in loops |

  That is about 42 pieces.

### N8. The charts are one cartoon repeated

- **Where:** CLOSE_35 (770-1010, 370-600), the room's left wall: THE WESTERN, THE ESTUARY and their neighbours. Each is the same flat buff land silhouette over flat blue water with a compass rose. (This is the shared point (h), and this shop's to judge. The builder names it as a shortfall.)
- **Whose:** the builder.
- **Exact fix:** six charts drawn by script in the Admiralty style, each from its own coastline seed. A test like PRT-04 checks that no two sheets share a coastline.
  - white ground (245, 243, 236);
  - buff land (232, 214, 160) with a 0.6 mm black coastline;
  - the 5 m and 10 m contours as blue lines (120, 160, 200), with the shallows filled (210, 228, 240);
  - 300 to 500 soundings as 1.5 mm numerals;
  - a magenta (165, 40, 120) compass rose;
  - a title block in the land and a border of latitude ticks.

### N9. A word survives on the compass card: a maker's mark by its place

- **Where:** `seadogs_compass_diff_1k_clean.jpg` box [503, 488, 546, 607]. It is a cursive word under the rose, in a compass card's maker's place: read mirrored, about "RADOLIER".
- It is not legible in any close frame (the dials are about 30 px). A player at 0.5 m could read it.
- INV-05 and INV-06 passed it. INV-08 (the second reader) was not run on this shop.
- **Whose:** the builder (step 0's blanking list).
- **Exact fix:**
  - add the box to `sw_assets.EXTRA_BLANK` for seadogs_compass, filled with the dial's own grey grain (ring about 128, 128, 128);
  - run INV-07 and INV-08 on this shop.

### N10. The door has no hours plate, and the target's hours and its lit night disagree

- **Where:** CLOSE_35 day, the shop door's glass under the OPEN card (405-450, 588-635): nothing.
  - T2-5 (14 Oct) puts an hours plate on every shop's door glass, as Rita's.
  - 4.1 drew none for the chandler (its small panels: the launderette's and the tea rooms' only), so FRN-12 did not run.
  - Its target hours are Mon to Sat 8 to 17, Wednesday to 13:00. The street file lights it at night, and the gate shows OPEN at night (the kit's rule 7: lit means open). TARGET 11 leaves this to the town.
- **Whose:** the target.
- **Exact fix:**
  - The town or the target's owner settles the chandler's hours first. Recommended: a port chandler that opens late, MON-SAT 8-8 / WED 8-1 / SUN CLOSED, so the lit, OPEN night is true.
  - Then a 4.1 row `hours_plate.chandler` (gold leaf on the glass, as Rita's), placed by FRN-12 under the card.

### N11. The paint tins are 16-sided

- **Where:** CLOSE_35 day (2180-2460, 940-1180). At 100 to 300 per cent the labels show vertical facet bands, and the tins' outlines are polygons.
- The labels read well and every name on them is the project's own.
- **Whose:** the builder.
- **Exact fix:** `GB.paint_tin(..., n=48)` with smooth shading on the sides, in the display and the room.

### N12. BLOWTORCH on the card

- **Where:** CLOSE_35_B day, the card before the blowlamp (about 1890-1920, 1010-1040).
- In a British shop of 1990 the brass paraffin lamp is a blowlamp, and the ironmonger's card was changed to BLOWLAMP for that reason (T2-2).
- **Whose:** the builder.
- **Exact fix:** card 9 reads `BLOWLAMP\n£7.25`.

### N13. The records

- **MANIFEST-chandler.json** names the right files (all six sha256 match the files on disk), but its "what" line is Rita's ("the narrow-points build ... rebuilt by build_ritas.py"). **Fix:** "the chandler's batch B build, 14 Oct; rebuilt by build_shop.py --shop chandler".
- **ROOM-05 says "rubber_boots 2 of 4" and NOTES says the window holds "ONE pair".** The model `rubber_boots` is two pairs (four meshes: clean and dirty, left and right), so:
  - the room shows four pairs, which is the target's count;
  - the window shows two pairs, against the target's three.
  - **Fix:** ROOM-05 counts pairs. NOTES C1 and the target's B8 and B9 read "4 of 4 pairs" (room) and "2 of 3 pairs" (window).

## Shared, known

None of (a), (b), (c), (e), (f) or (g) shows in the close frames:
- (a) The night glass has no orange bar: GLS-04's largest patch is 0.0176 per cent at CLOSE_35.
- (b) night_dark is not a close frame.
- (c) The glass of the lanterns, the till and the flashlight is kept, and the hurricane lamps' globes are see-through at 100 per cent.
- (e) No card leans toward the glass.
- (f) The door reads OPEN in the lit night.
- (g) There is no display furniture; the room's counter is 0.97 high.

N4's two causes are kit fixes that exist but were made after this build. They are not on the shared list, so I count them here as narrow points of this build.

## The builder's named shortfalls, judged

| shortfall (NOTES, check) | verdict |
|---|---|
| The sou'westers read as yellow hats until the card is read | **FAULT** (F1) |
| LIT-02b at the day frames (0.0117, 0.0140, CLOSE_35_B share 0.0115) | narrow (N6): shade, no void; the largest patch at CLOSE_35_B is 0.0019 |
| The target's counts do not fit at real size (room 2 of 4 jackets, 1 of 2 lifebuoys, no sou'westers, "2 of 4" boots; window 3 of 5 coils, "1 of 3" boots, 2 of 3 cans) | not a fault. The window still reads as a chandler's, and nothing looks short. The boots are miscounted in the shop's favour (N13). Room and window each read full enough for their size. |
| The charts and the tide table drawn by script | narrow (N8) |
| The marker buoy is 1.5 m tall (the target's size), at the back wall's left end | not seen from the close cameras; acceptable |
| The mesh screens are built and not shown | right: the target keeps them out of the lit night's way |
| Narrow passes: PIC-05g 0.0077 at CLOSE_35 night, LIT-08 lowest 0.80, GLS-04 0.0176 per cent | pass. PIC-05g's burnt pixels are the hats' crowns and the white and yellow coils' tops (F1's fix takes the largest). No arc and no burnt band. |
| 48 samples a pixel | owed, as the target says. The noise reads 0.39 on the ceiling and nothing in the frames is grainy. |

## Measured

**Parallax, by the game's `trace`, imported:**
- The card's centre samples the picture at u 0.17180 from CLOSE_35 and 0.49459 from CLOSE_35_B: 1322.1 px of 4096 apart. PRJ-02 is confirmed.
- **Back wall:**
  - A paint tin on the shelving, picture pixel (1300, 700), lands at card x 1.8466 m (from the low-x edge) from CLOSE_35 and at 3.2061 m from CLOSE_35_B: 1.360 m for 2.0 m of eye travel (2.0 x 4.5 / 6.62).
  - In the gate's baked day cards the patch round it is found in the CLOSE_35_B card at offset (0, 0), correlation 0.977. A second point, a room jacket (2600, 560), is also at (0, 0), correlation 0.999. PRJ-03's bake is confirmed.
- **Right wall:** the till, (3600, 700), moves 0.888 m. The back wall moves 1.360 m, so the depth parallax differs as it should.

**Glass luma (mean, whole glass, with the stand-in reflection; the room's share of the glass in brackets):**

| frame | glass | room part | display part | reflection off |
|---|---|---|---|---|
| CLOSE_35 day | 62.4 | 46.1 (57%) | 83.4 | 52.5 |
| CLOSE_35 night_lit | 68.2 | 57.7 | 83.2 | 69.7 |
| CLOSE_35_B day | 59.7 | 49.6 (61%) | 75.4 | 48.1 |
| CLOSE_35_B night_lit | 64.0 | 59.0 | 73.2 | 65.3 |

- Every value is over LIT-02's floors (33 by day, 45 at night).
- At night the lit glass is 3.4 to 4.1 times the brick beside it (16.5 at CLOSE_35, 19.8 at CLOSE_35_B).
- By day the glass sits below the brick (83 to 88), as a shop window does, and the room reads.

**No void, no flat slab:**
- Pure-black pixels (luma under 2) inside the glass: a few hundred specks at night (inside the boots and under goods), no patch.
- The largest flat tone in the display is N3's board.
- The largest flat tones in the room are natural surfaces:
  - the oiled floor in the right light by day (5.3 per cent of the glass at luma 30, faint board streaks);
  - the ceiling at night (4.3 per cent);
  - the right return wall from CLOSE_35_B (5.2 per cent, plaster with the room's map at plus or minus 8 per cent).
- There is no white board and no void.

**Night burn:** 0.0077 of CLOSE_35 night at 250 in a channel, PIC-05g repeated: the two hat crowns, the white coil with the right jacket's top, and the yellow coil. There is no arc and no burnt head band; the stand-in spill is not visible.

**Export faults from Rita's shop, rechecked from the files:**
- **Normal maps:** 11 in the display and front glbs. All are real tangent-space maps (blue mean 200 or more, red and green within 14 of 128).
- **UVs:** no textured primitive without UVs, in any of the three glbs.
- **Coplanar black strips:** none on the front (FRN-10; I looked at the door, the side door and the jambs at 300 per cent).
- **See-through slots:** none (FRN-08: 0 px from both close cameras).
- **Stand-in light or glass:** neither is visible as such.

**Every legible word at 100 per cent, both close cameras, day and night:**
- **Front:**
  - OPEN (the door card);
  - 13 (gold, the fanlight);
  - "CHAN" mirrored in the fanlight's glass: the reflection of the hanging sign's CHANDLERY, a true reflection of the shop's own sign;
  - the fascia's 13, cut at the frame's corner.
- **Display:**
  - the cards: LIFEBUOY £12.50, JACKETS £9.95, ROPE 85p a metre, SOU'WESTERS £2.95, LAMPS £4.20, COMPASS £5.50, OIL TINS £1.60, OIL CANS £1.35, PAINT £3.45, BLOWTORCH £7.25 (N12);
  - the tins:
    - the makers PENHALE, TREGENNA and WESTHAVEN;
    - the products MARINE VARNISH, ANTIFOULING, DECK PAINT, WHITE SPIRIT, BILGE PAINT, METAL PRIMER, TEAK OIL, HULL PAINT, EPOXY FILLER, BOAT VARNISH, BITUMEN PAINT and WHITE GLOSS;
    - the colours "clear gloss", red, "slate grey", grey, "red oxide", navy, yacht and black.
- **Room:** THE WESTERN and THE ESTUARY (soft); the tide table's lines are not legible.

All are the project's own shop words and numbers, and acceptable. WHITE SPIRIT is the British paint thinner, not drink. No real maker's name, firm or modern mark is legible in any frame. The one surviving mark is in a map and below legibility in the frames (N9).

**Content rule:**
- no drink, betting slip or lottery;
- no toy or child's thing;
- no flare;
- no barcode, flat screen or modern package (the small oil can's CLP diamond is painted out, and the cleaner tins' labels are the project's own).
- The boots are men's sea boots at real size. The blowlamp is a tool, not a weapon.

## The check rows: which I trust

- **Trusted, from geometry and files (several repeated by me):**
  - PIC-01 and PIC-04;
  - PRJ-01 to PRJ-03 (repeated);
  - SO-01 to SO-07, DSP-01, DSP-02, DSP-04, DSP-06 and DSP-07;
  - FRN-01 to FRN-11, FAS-01 to FAS-03, GLS-01 and GLS-02;
  - GLB-01 (repeated from the glbs), NIT-01;
  - INV-01 to INV-04, NEV-02, CAM-01, X-PRV;
  - the MANIFEST hashes (repeated).
- **Measured on frames, which I repeated:** LIT-02b (CLOSE_35 and CLOSE_35_B, the same numbers) and PIC-05g at CLOSE_35 night (0.0077).
- **The cloud's stand-ins, true only of the gate:** LIT-01, LIT-05, LIT-07, LIT-08, GLS-03, GLS-04, GLS-05 and PIC-05g at night. They rest on the gate's spill, strip lamp and glass; Lumen and the game's glass are owed (PC-01, PC-02).
- **Passing rows that missed something:**
  - DSP-05 passed the rails and jackets of N2 (a touch counts as hanging);
  - INV-05 and INV-06 passed the compass word of N9;
  - ROOM-02 passed a near-bare pegboard on a count (N7);
  - ROOM-05 miscounts the boots (N13);
  - DSP-03 sees no intersection but cannot see what a good reads as (F1).
- **Not run on this shop:** the kit's rows from the batch A try 2 reviews: FRN-13, SIGN-01, DSP-09, DSP-10, DSP-11, INV-07, INV-08, FLT-01, FLT-02 and LIT-01c. FRN-12 is n/a, since 4.1 drew no plate. Several of them catch N2, N3, N4 and N9.
  - **Fix:** the next check of this shop runs `check_try3.py`'s rows as the ironmonger's and the newsagent's do.

## What is right

- **The window reads as a ship chandler's at 1.5 m:**
  - the worn lifebuoy leaning on its edge with its grab line;
  - two life jackets;
  - three rope coils on pegs;
  - two pairs of green sea boots;
  - a wooden lantern and two hurricane lamps with see-through globes;
  - two open brass compasses on a riser;
  - four one-gallon oil tins and two long-spouted oil cans;
  - a pyramid of 21 marine paint tins with the project's own makers;
  - a brass blowlamp.
  - Every Poly Haven piece is at real size, scans not props, and none is buried, through a shelf or touching another (DSP-03, DSP-06). Each card stands before its goods or hangs by a cord from them.
- **The hats and the cards on cords are held.** The hats hang by a cord from the front rail to the crown, the coils by pegs, and the ROPE and JACKETS cards by short cords to their goods. Only the rails themselves and the jackets are not hung (N2).
- **The projected room behaves exactly as the game's rule says** and reads as a deep, lit room:
  - the shelving, the counter with the till and the hurricane lamp, the hooks board, the charts and the pegboard all shift true between the two cameras;
  - there is no seam where the bed meets the room's floor;
  - from CLOSE_35_B the far end is a plaster wall over the green dado, its dado line meeting the card's without a step.
  - There is no black slab, and the picture never ends.
- **By day the display is brighter than the dim room behind it.** At night the room is lit by its tubes, the display by the stand-in, and nothing burns.
- **The door:**
  - the M1 aluminium leaf glazed from 198 mm;
  - the chrome D pull on the lever stile;
  - the letter plate in the bottom rail, clear of the glass;
  - the gold 13 on the fanlight;
  - the green OPEN card;
  - the band of toplights above.
  - The bell hangs by the geometry where the target puts it (spring strip on the top rail, 90 mm in from the hinge stile). The jamb hides it from CLOSE_35, and CLOSE_35_B does not frame the door.
  - The side door, its letter plate, knob and fanlight (a dim hall) are clean.
  - There are no black strips anywhere.
- **The glass:** by day it shows sky and the street opposite. At night it shows reflection only, with no doubling (GLS-03 p95 7.8 and 6.8).

## What I cannot judge from the files

- **The game's own light and glass:** Lumen on the display, the glass's reflections and its Fresnel hand-over, the exposure, the card under TSR, the frame time; and so how the untoned jackets of N1 will sit at night in the game.
- **The bell:** it is hidden from both close cameras. Its swing and sound are not in the files.
- **Wear, grime and wet,** which come from the game's own layers.
- **Whether "RADOLIER" (N9) is a real firm:** I could not settle it from the files. Its place on the card is reason enough to paint it out.
- **Measurements I could not repeat:** GLS-03, GLS-04, GLS-05, LIT-08, DSP-03 and DSP-05's mesh tests, FRN-10's coplanar test and INV-06's box test. I judged those by eye only. The check renders they need are still in the scratch folder; I did not re-render anything.
