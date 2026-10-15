PASS

# The ironmonger (west_north bay 1, no. 16), the CLOSE view: fresh review, try 2 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer. I did not write the target or build the shop. I judged one view only: CLOSE_35 and CLOSE_35_B, by day, night_lit and (CLOSE_35 only) night_dark. I did not read the street view's reviews. A comment in `sw_gate.py` (near lines 585 and 604, dated 15 October) quotes two of its narrow points; I read it in passing, after my own night_dark measure.

**Read:** CLAUDE.md; RULINGS.md (1, 2, 3 and 8 October); NOTES.md ("For the next nine shops", the ironmonger's batch A section, "Try 2 shared fixes", "Try 2, ironmonger"); TARGET.md sections 3 and 5.8 and the 13 and 14 October rows of section 13; the headings and faults of Rita's four reviews; my try 1 review (REVIEW-ironmonger-v1-close.md); `checks/check_ironmonger_v2.json`. I also read the parts of `sw_display_gen.py` (`layout_ironmonger`) and `sw_gate.py` (night lights, glossy switches) named below.

**Looked at:**
- the v2 close previews (day, night_lit, night_dark);
- the five close gate frames (2560 x 1440) at 100 to 600 per cent;
- the three 4096 room pictures (preview and frames);
- the display glb: its 45 pictures, materials and meshes.

**Measured,** with my own scripts in my scratchpad; nothing in the repository or SCRATCH was changed:
- the parallax, through the game's own `trace` (two picture points);
- the glass luma over the gate's glass masks, split into room and display by the gate's pieces render;
- dark, flat and burnt patches; the bar boxes of try 1; GLS-04 against the reflection-off renders;
- the joins of the return walls and the card;
- the door's panes;
- contacts between display pieces (a world-space BVH over the glb);
- the blanking boxes and every picture of the display glb.

**The frames moved while I worked.** At 04:01 on 15 October a builder started `build_shop.py --shop ironmonger gate` again; it re-baked the four close cards at 04:01-04:02, and the front glb on disk was rewritten at 03:50. Before anything else was overwritten I copied the 14 October frames, masks and camera files to my scratchpad and checked them by sha256 (CLOSE_35_day a6d34d3a..., CLOSE_35_night_lit dd94f494..., CLOSE_35_night_dark 7f73ca51..., CLOSE_35_B_day ddd8477d..., CLOSE_35_B_night_lit f75a8956...). Everything below is about those files. The display glb I measured is the 14 October one (sha256 dedec6f7..., as the manifest says).

Pixel boxes are in the 2560 x 1440 frames unless marked "preview" (the 1600 JPEGs, 0.625 of the frame). Luma is Rec. 709, as the kit's checks use.

**In short:**
- **All three try 1 faults are fixed.** The orange bar is gone from both night frames, the twelve bulbs have glass and bayonet caps, and the pump's roundel and the trowels' stamp are painted out.
- **The room still moves exactly as the game's rule says.** It reads as a deep, lit, full ironmonger's, with no black slab at CLOSE_35_B. The door now has its hours plate and shows the shop's own wall through its glass.
- **No faults.** There are 5 narrow points, the worst first:
  1. a real trade name, "Polybubble" with a registered-mark sign, survives twice on the sprinkler's top. It is not legible from either camera;
  2. at the shop's own night (night_dark) the whole display is near black in front of a lit room. This is the gate's stand-in light; the kit's fix is already written;
  3. the green backing board of the pyramid is a flat field at close range, 6.1 per cent of the glass;
  4. two of the three leaning brooms rest on nothing, 23 mm short of the next broom;
  5. FLT-01, the builder's one failing row: the room's counter front is three plain panels.
- Under Jafar's ruling of 9 October this is a PASS, with these points listed for the builder. Point 1 is the content rule and must be applied before the shop merges.

0 faults, 5 narrow points.

## Try 1, item by item

| try 1 item | now | where and how measured |
|---|---|---|
| Fault 1: the stand-in lamps' pool burns an orange bar across the night glass | **FIXED** | CLOSE_35 night_lit, try 1's box x 1410-1960, y 665-750: luma 52.9 against 58.1 just above; 0.4 per cent of it burnt. Try 1: 119 against 72, 27 per cent burnt. CLOSE_35_B night_lit, box x 560-1070, y 670-775: 51.4 against 61.8 above; 0.85 per cent burnt. Try 1: 138 against 62, 24 per cent. The day frames' same boxes are 55.6 and 54.2, so night now matches day. I repeated GLS-04 exactly: CLOSE_35 a largest patch of 276 px (0.0116 per cent of the glass), CLOSE_35_B 1596 px (0.0651 per cent). The CLOSE_35_B patch (x 1072-1156, y 1143-1187) is a faint grey reflection of the near footway under the second trowel tray, not a bar. Cause struck as asked: `street_glossy` false, at night only (`sw_gate.py` lines 588-595). NOTES judgement I15 still carries its wrong sentence ("not a lamp and not a reflection"). It is covered only by the section's "superseded" head note: strike the sentence. |
| Fault 2: the bulbs have no glass, and screw caps | **FIXED** | CLOSE_35 day x 60-1000, y 1290-1440 and CLOSE_35_B day x 640-940, y 975-1065: clear envelopes with filaments, standing in their trays. The glb: all 12 bulbs keep the glass part (`pane_see_through`: KHR transmission 1.0, roughness 0.05, no alpha blend). Each has a scripted B22 cap: collar, sleeve, two pins, two contacts and an insulator (84 parts). Scale 1.0 at a 0.064 pitch. |
| Fault 3: the pump's roundel and the trowels' handle stamp | **FIXED** | In the glb's own 1k maps (the pictures the game gets), the pump box [570, 893, 624, 957] is the ring grey (154) in the diffuse map and flat in the normal map. The trowel box [838, 795, 922, 828] holds no word in either map. But a third word of the same kind was missed: narrow point 1. The trowel box is a flat fill (sd 3.1 against 14.5 to 15.8 for the handle's wood around it): see narrow point 1's fix. |
| N1: the supports are flat colour (crate, board, trays, shelf, return walls) | **FIXED, but the board is PARTLY** | **The crate** (CLOSE_35_B day x 1400-1981, y 989-1257): planked deal with nails and HARTSIDE stencilled. High-pass sd 17.8; 2 per cent of pixels with a 9 px sd under 1. Try 1: 85,931 px at sd under 1.5. **The trowel blocks:** high-pass sd 17.4. **The hung shelf's front:** 14.3. **The right return wall** (CLOSE_35 day x 1790-1987, y 288-574): high-pass sd 7.05, against try 1's 1.4 to 1.7; it now reads as plaster. **The backing board** is now dark green plywood rather than my pegboard. The street review's luma of 25 to 45 is met, but the board is flat at close range: narrow point 3. |
| N2: the glove shelf hides the pyramid's top, and its cords end in mid-air | **FIXED** | **CLOSE_35 day:** the apex tin is whole under the shelf (about x 478-556, y 793-849). **CLOSE_35_B day:** the four cords end on a black rod under the transom (x 500-850, y 60-150). DSP-10 agrees. |
| N3: through the shop door's glass, a flat grey slab | **FIXED** | CLOSE_35, shop door. **Upper pane:** plaster at luma 87.2 by day and 86.5 at night_lit. **Lower pane:** the dado (52, 56, 50), luma 54.6 by day and 27.7 at night_lit, behind the hours plate. Try 1: grey 73 and 59. The shop's own finishes, as asked. FRN-13 agrees. |
| N4: white goods burn at night (the test state) | **PARTLY; accepted** | **CLOSE_35_B night_lit:** the three handles still burn, 8,851 px at 250 or more, at x 2163-2560, y 414-1000. Try 1 had about 5,400; there are more now because the brooms stand upright at full size. **CLOSE_35 night_lit:** the hung shelf's top has 4,334 px at x 234-877, y 722-802 (try 1: 10,932). **Accepted:** PIC-05g repeats at 0.0027 and 0.0050 (limit 0.01), the handles keep their shading, and night_lit is only the tests' state for this dark shop. Not counted. |
| N5: the cleaner tins are blank red | **FIXED** | CLOSE_35_B day x 1455-1720, y 885-1010: HARTSIDE SCOURING POWDER 500 g, ELMSTEAD BRASS POLISH 250 ml, COLDWELL WASHING SODA 1 kg, BRANTHAM DISINFECTANT 1 litre. |
| N6: TORCH and TINS 99p | **FIXED** | BLOWLAMP £8.50 at CLOSE_35_B day x 1860-1935, y 1335-1400. The atlas holds 11 cards, with no TINS. |
| N7: no hours plate | **FIXED** | CLOSE_35 day, the shop door's lower pane, x 2065-2175, y 730-800: MON-SAT 8.30-5.30 / WED 8.30-1 / SUN CLOSED in gilt. It reads correctly at night_lit too. |
| N8: the dark shop's night is not shown at close range | **PARTLY** | CLOSE_35 night_dark is rendered and is a preview. **The room part** of its glass is 16.0 (LIT-01c says 15.6; 10 to 35 wanted). **CLOSE_35_B night_dark was not rendered;** LIT-01c reads it by a composite (15.5). The new frame shows a fresh problem: narrow point 2. |
| N9: the manifest carries Rita's description | **FIXED** | Its `what` now names the ironmonger's try 2. The display glb's and the three pictures' sha256 match the files. The front glb's no longer matches: it was rewritten at 03:50 on 15 October by the builder now at work, not by try 2. |
| Checks I proposed | mostly built | GLS-04, DSP-07 (keeping the glass), DSP-09 (no flat support) and DSP-10 (cords) were all built. INV-06's second pass, a contact sheet of every clean map read by someone other than the builder, was not built: INV-07 tests only the boxes, and point 1's word lies outside every box. |

The try 2 notes make no claim that the close review was wrong, so there was no such claim to test.

## Faults

None.

## Narrow points, most important first (each with its exact fix)

### 1. A real trade name, "Polybubble" with a registered-mark sign, survives twice on the sprinkler's top (content rule; apply before merge)

**Where:**
- **In `garden_sprinkler_01_diff_1k_clean.jpg`,** the glb's own picture:
  - a black printed "Polububble®" at about [45, 945, 135, 962];
  - a moulded "Polybubble" at about [225, 900, 350, 930].
- The blanking box [30, 960, 210, 996] painted out the line under the first word and stops at its foot. This is the miss the pump's roundel had at try 1.
- **On the model:** both words lie on the yellow body's top face (normal 0, 0.27, 0.96, facing up), at display x 1.29 and 1.18.
  - The printed word is about 53 x 6 mm.
  - The moulded word is about 65 x 16 mm.

**In the frames:**
- **CLOSE_35 day:** near x 1750-1790, y 1010-1030.
- **CLOSE_35_B day:** near x 2110-2260, y 1365-1415. Here it shows at most as one or two dark dashes 2 to 3 px high.
- Neither word is legible at 100 per cent from either camera.
- The near metre is real geometry, so a player at the glass, about 0.6 m away, would see the printed word about 12 px high.

**Why it matters:**
- "Polybubble" is a real product name: the Polycell range's bubble wrap, sold under that name (nxp.nz, officemax.co.nz).
- A POLY BUBBLE trademark was filed in 1978 (Conform Plastics Limited, trademark.justia.com).
- The content rule allows no real firm's name or mark anywhere.

**Why it is narrow and not a fault:**
- It is not legible, or even readable as a badge, at either review camera.
- The fix is exact.
- Try 1 counted its two surviving marks as a fault: the pump's roundel read as a logo badge in the frames, and the notes said both were gone.

**Whose:** the builder (step 0's blanking boxes) and the kit (INV-07 cannot see a word outside its boxes).

**Exact fix:**
1. Add two boxes to `sw_assets.EXTRA_BLANK_T2` for `garden_sprinkler_01`: [40, 935, 140, 964] and [220, 895, 355, 932]. Paint them in the ring yellow (194, 153, 58) carrying the map's own grain, in the diffuse, normal and ARM maps, as the other boxes.
2. While there, **refill the trowel's box** [838, 795, 922, 828] with the map's own pixels from [838, 830, 922, 863] (the same handle wood), feathered 4 px. Do the same in the trowel's normal and ARM maps. The flat fill would show as a smooth patch on the handle at arm's length.
3. Re-export the display glb.
4. **A second pass for INV-07,** failing the build: a contact sheet of every placed model's clean base map at 1k, with the boxes drawn, read word by word by someone other than the builder before the gate. Record it in the row as done, by whom and when. It found this word in ten minutes.

### 2. At the shop's own night (night_dark) the display is near black in front of a lit room (the gate's stand-in light)

**Where:** CLOSE_35 night_dark, the whole left light's lower half and the bed, x 6-1334, y 581-1434 (preview 4-834, 363-896; the bottom left of `ironmonger-close-35-night-dark-2026-10-14-v2.jpg`).

**Measured** (split by the gate's own pieces render):

| part of the glass | mean luma |
|---|---|
| the room | 16.0 |
| the display | 4.3 |
| the brick beside the window | 15.2 |

- 75 per cent of the display's pixels are under luma 5.
- One connected patch under luma 5 is 25.6 per cent of the glass.
- Lifted by a gamma of 2.2, every good is there (the pyramid, gloves, trowels, crate, cans), so this is darkness, not a void.

**Why it reads wrong:** the room is lit by the target's "faint sodium wash through the front", yet the goods a metre nearer that light get none of it. In the gate the spill is off for a dark shop, and the stand-in lamps stand across the street with cones that do not reach the front.

**Why it is narrow:** the lights are the gate's stand-ins, and the game's own lamps on the display are owed on the PC (PC-02). Nothing in the shop's models or pictures has to change. The kit already holds the fix, written on 15 October after these frames were made.

**Whose:** the kit (`sw_gate.py`).

**Exact fix:**
1. Render the night_dark frames with the night_dark display wash already in `sw_gate.py`:
   - sodium (1.0, 0.25, 0.0);
   - 4.3 x 0.5 m, 0.02 m outside the glass, at 0.6 of the card's height, tipped 30 degrees into the window;
   - on the display's own light channel;
   - invisible to the camera, glossy and transmission rays.
2. Set `wash_w` so that, at CLOSE_35 night_dark, the display part's mean luma over the glass is 0.6 to 1.0 of the room part's (here 9.6 to 16), and no patch under luma 5 exceeds 1 per cent of the glass.
3. Render CLOSE_35_B night_dark as well (the half of try 1's narrow point 8 still owed).
4. **New row LIT-01d,** failing the build: those two numbers at STREET_SQUARE, CLOSE_35 and CLOSE_35_B night_dark.
5. Until then, keep the CLOSE_35 night_dark preview off his page.

### 3. The pyramid's green backing board is the largest flat field in the window at close range

**Where:**
- **CLOSE_35 day,** x 6-477, y 830-1372 (preview 4-298, 519-858):
  - the largest flat patch in either close day frame (9 px sd under 1): 6.1 per cent of the glass, at luma 37.5;
  - left of the pyramid, 89 per cent of the board's pixels are that flat.
- **CLOSE_35_B day,** right of the pyramid, x 1000-1060, y 700-960: 79 per cent.

It reads as a plain dark-green CG panel, the try 1 "white board" in a darker tone. The street review's own row, DSP-11, holds it to luma 25 to 45, and it passes at 44.5. FLT-01 (limit 1 per cent for this shop) is run only at the street cameras, so it does not see the board at close range.

**Whose:** the builder (the board's material) and the target (FLT-01's cameras).

**Exact fix:**
1. Make the board vertical matchboard of the period: boards 95 mm wide, each with a 3 mm V-joint (joint colour (14, 30, 21)), painted (26, 54, 38). Raise the plywood grain in `painted_png("backing_ply", ...)` from 0.6 to 1.2. Keep DSP-11's 25 to 45.
2. Run FLT-01 at CLOSE_35 and CLOSE_35_B on the display's pieces, limit 1 per cent. Today it reads 6.1.

### 4. Two of the three leaning brooms rest on nothing

**Where:** CLOSE_35_B day, the three handles x 2050-2560, y 230-1300, their heads at the top right, about x 2400-2560, y 330-420. At CLOSE_35 the heads overlap in projection (x 1740-1960, y 430-480).

**Measured in the glb** (world-space nearest distance from each piece's top quarter to any other part):

| piece | nearest part to its top quarter |
|---|---|
| broom 1 (`plastic_broom.002`) | 4.0 mm, the right return wall |
| broom 2 (`.003`) | 23 mm, broom 1 |
| broom 3 (`.004`) | 23 mm, broom 2 |
| the sledgehammer | 4.0 mm, the wall |

- Each broom stands on its handle end (0 mm from the bed) and leans 13 degrees with its feet 0.11 m apart, so brooms 2 and 3 would fall 23 mm onto the next.
- The gap does not show from either camera.
- DSP-05 passes them on their feet alone: its rule asks a point of the lowest half to touch, and nothing of a leaning piece's top.

**Whose:** the builder (`layout_ironmonger`) and the kit (DSP-05).

**Exact fix:**
1. In `layout_ironmonger`, set the heads 0.087 apart (not 0.11); 0.11 x cos 13 degrees less the 23 mm gap leaves 1 mm.
2. Set the first broom at `wall_x - 0.001` (not 0.004), and the sledgehammer too, so each top rests within 1 mm of what is behind it.
3. **DSP-05 adds:** a piece tilted more than 3 degrees from upright must also have a point of its top quarter within 2 mm of another part.

### 5. FLT-01, the builder's one failing row: the room's counter front is three plain panels

**Where:** CLOSE_35 day x 880-1170, y 600-760 (preview 550-731, 375-475), and CLOSE_35_B day at the right, behind the brooms. Three flat brown rectangles:
- 66 per cent of pixels with a 9 px sd under 1;
- high-pass sd 2.65;
- luma 47.6.

It reads as a plain cupboard, not a varnished counter. It is in the room's picture, so it moves true with the rule, and it is not a void.

**Whose:** the builder (the room's counter).

**Exact fix:**
1. At the next room render, give the counter's front the room's own floor wood (Poly Haven `old_wooden_floor_03`, CC0, already fetched) on a 0.5 m tile tinted to the counter's colour.
2. Add a 20 mm bolection moulding round each of the three panels.
3. Re-render the three pictures (48 minutes); FLT-01 at STREET_30 then falls under 1 per cent (it reads 2.06 now).
4. Do it with the next room pass, not as a pass of its own.

## The builder's named shortfalls, judged from the close view

| shortfall (NOTES, check file) | judged | why |
|---|---|---|
| FLT-01 fails at STREET_30 (2.06 per cent, the counter front) | narrow | Point 5. |
| PIC-05g and DSP-11 pass narrowly (0.0050; 44.5 against 45) | accept | I repeated PIC-05g: 0.0027 and 0.0050. DSP-11 meets its limit; the board's flatness is point 3. |
| Every display piece at 1.0 of its size; goods moved, not shrunk | right | At 1.5 m the toolboxes, cans, pump and brooms read at a believable size. The right end is full but not crowded. DSP-04's longest bare run is 0.02 m. |
| No step ladder; 2 of 3 paraffin cans; tiers 0.4 and 0.8 not built; 1 of 3 cans in the room | narrow; accept | Nothing missing is seen from either close camera. |
| Pegboards with 44 and 34 to 36 tools | narrow; accept | They read as rows of hand tools and of gloves, trowels, dustpans and traps (CLOSE_35 day x 60-330, y 130-700; x 1490-1780, y 360-640). |
| Dark at night: night_dark is the real night; night_lit is the test state | right | Point 2 is the stand-in light's problem, not the shop's. |
| LIT-08 n/a for a dark shop | accept | At night_lit the blowlamp reads as brass and the pump as a clean silhouette. |
| LIT-02b counts dark only over a picture of luma 40 or more | accept | Without the rule change my raw share under luma 12 is 0.07 and 0.08 per cent of the glass by day (largest patch 0.02 and 0.04): it passes either way. |
| FRN-10 skips parts painted under luma 40 | accept for this view | No thin dark run on either door or jamb at close range (CLOSE_35 day x 2000-2560, y 0-1300 at 100 per cent). FRN-10's darkest front pixels are 1.0 and 5.0, in patches under 35 mm. |
| 64 samples | owed | 128 samples on the PC. |
| The hanging board | not this view | |

## The check rows: which I trust

**Trust: the game's rule or assets, repeated here or agreeing with what I measured.**
- **PRJ-01 to PRJ-03:** my parallax repeat, under "Measured".
- **GLS-04:** repeated to the pixel.
- **DSP-07:** the glb's bulbs and caps.
- **DSP-09, DSP-10, DSP-11, DSP-06.**
- **INV-07:** for the boxes it tests.
- **SIGN-01:** the camera files say OPEN by day and CLOSED in both night states, and the frames show it.
- **FRN-13:** by eye at CLOSE_35.
- **FRN-03, FRN-08, GLB-01, FAS-03, CAM-01.**
- **The manifest,** apart from the front glb rewritten today.

**Trust with a gap.**
- **DSP-05:** passes two brooms that lean on nothing (point 4).
- **INV-05, INV-06, INV-07:** pass while "Polybubble" survives outside every box (point 1).
- **FLT-01:** run only at the street cameras (point 3).
- **LIT-01c:** measures the room only; the display at night_dark reads 4.3 (point 2).
- **PIC-05g's text:** "try 1: night frames 0.033 and 0.031" is Rita's figure; the ironmonger's try 1 row read 0.0082 and 0.0088.

**Stand-ins only: the gate's light and glass, owed on the PC.**
- GLS-03, GLS-04 and GLS-05;
- LIT-01, LIT-01c, LIT-02, LIT-05 and LIT-07;
- PIC-05g.

**Could not repeat:**
- CLOSE_35_B night_dark, which was not rendered;
- the 14 October baked cards, re-baked at 04:01 on 15 October during this review. I used my own `trace` instead;
- TRD-01's and DSP-03's silhouette shares, which I took from the row.

## Measured

**The parallax, through the game's `trace`.** For two picture points I solved for the card point that `trace` sends to them from each camera, and projected it into the frame. I then correlated a 40 x 40 frame patch with the rule's own patch, which samples the picture through `trace` for every pixel.

| picture point | CLOSE_35: card x, frame px | CLOSE_35_B: card x, frame px | shift on the card | frame against the rule |
|---|---|---|---|---|
| the till (2395, 900) | 1.5394 m, (1114, 530) | 2.8989 m, (2188, 513) | 1.3595 m | correlation 0.87 and 0.81, offsets of 1 px or less |
| a drawer (1101, 768) | 0.5479 m, (458, 446) | 1.9074 m, (1496, 465) | 1.3595 m | |

- The rule for a back-wall point is 2.0 x 4.5 / (2.12 + 4.5) = 1.3595 m.
- `trace` sends every solved card point back to its picture pixel to 0.01 px.

**The glass** (mean luma over the gate's glass mask, eroded 6 px; split into room and display by the gate's pieces render):

| frame | the whole glass | the room part | the display part | the brick beside the window |
|---|---|---|---|---|
| CLOSE_35 day | 64.5 | 56.7 | 79.6 | 82.6 |
| CLOSE_35_B day | 66.2 | 55.9 | 94.4 | 87.5 |
| CLOSE_35 night_lit (the tests' state) | 61.9 | 67.8 | 52.2 | 16.3 |
| CLOSE_35_B night_lit | 73.9 | 74.8 | 73.9 | 20.8 |
| CLOSE_35 night_dark (the shop's own night) | 11.7 | 16.0 | 4.3 | 15.2 |

- By day the room is readable: well above the target's composite floor of 33, and darker than the brick, as a shop window is.
- In the lit state the room is 4.2 and 3.6 times the wall.
- The shop is dark at night by the target. Its room reads 16.0 there, inside 10 to 35, while its display does not (point 2).

**Dark and flat patches over the glass.**
- **Under luma 12 by day:** 0.07 and 0.08 per cent, largest patch 0.02 and 0.04 per cent. No void and no slab at CLOSE_35_B.
- **At night_lit:** 4.6 and 1.4 per cent. The largest is 1.3 per cent at CLOSE_35 (x 129-423, y 1107-1358), the bed's front and the bulb tray in shade; under luma 5 it is 0.1 per cent.
- **Flat (9 px sd under 1), the largest patches:** CLOSE_35 day 6.1 per cent, the board (point 3); then the room's ceiling (3.4 and 3.7 per cent, and 5.5 and 11.0 per cent at night_lit, a cream board ceiling at luma 50 to 56). Next come the room floor and the right return wall's upper part (2.0 per cent). A plain ceiling is a natural flat; it is not a point.

**The joins between the return walls and the card.**
- **CLOSE_35_B, the left wall:** steps of 0.1 to 2.4 levels at z 1.8 to 2.6 above the crown, by day and night. The join does not show.
- **CLOSE_35, the right wall:** steps of 1.4 to 19.6 levels by day at z 2.0 to 2.6 (lower down the brooms stand in front of it), made by the day glass's tree reflection and the room's pegboard edge. At night they are 2.5 to 9.7.
- No gap shows between the bed's back edge and the card's floor in either day frame (the bed ends at v 0.55, the card stands at 0.61).

**Burnt pixels (any channel at 250 or more), share of the frame:**

| frame | burnt share |
|---|---|
| CLOSE_35 day | 0.0002 |
| CLOSE_35 night_lit | 0.0027 |
| CLOSE_35_B day | 0.0000 |
| CLOSE_35_B night_lit | 0.0050 |
| CLOSE_35 night_dark | 0.0000 |

There is no spill arc, no burnt head band and no stand-in lamp visible in either night frame.

**Every legible word at 100 per cent, both close views.** All are the project's own and acceptable. No legible word is a real firm's.

| what | the words |
|---|---|
| Price cards (hand-lettered) | OIL £1.15, BULBS 40p, TROWELS £2.45, GLOVES £1.30, CANS £3.95, PUMP £4.50, SPRINKLER £3.75, PAINT £2.99, TOOL BOXES £6.95, BROOMS £2.25, BLOWLAMP £8.50 |
| Paint tins (the project's makers) | COLDWELL EMULSION MAGNOLIA / BRILLIANT WHITE; HARTSIDE WHITE SPIRIT, METAL PRIMER RED OXIDE; ELMSTEAD WOOD PRESERVER DARK OAK, WOOD STAIN TEAK; BRANTHAM GLOSS PAINT BLACK / WHITE |
| Cleaner tins | HARTSIDE SCOURING POWDER 500 g; ELMSTEAD BRASS POLISH 250 ml; COLDWELL WASHING SODA 1 kg; BRANTHAM DISINFECTANT 1 litre (metric packs were usual by 1990) |
| The crate | HARTSIDE; "& OI…" of PAINTS & OILS, behind the cleaners |
| The door | OPEN by day, CLOSED at both nights; the hours plate; 16 in gilt on the fanlight |
| The room | COLDWELL on a shelf tin (CLOSE_35_B, x 2405-2455, y 485-520) |
| The fascia's corner | "…IN" (the street view's) |
| Not legible at 100 or 200 per cent | the drawer labels, the till's readout, the sprinkler's "Polybubble" (point 1) |

**Rita's export faults:**

| fault | here |
|---|---|
| A height map exported as a normal map | none: the display glb's normal maps are RGB, flat blue in the boxes |
| A textured primitive without UVs | none (FAS-03) |
| Two parts in one face plane, giving a black strip | none at close: the doors, jambs and side door are clean at 100 per cent (CLOSE_35 day x 2000-2560, y 0-1300) |
| A see-through slot from an angle | none: no backdrop or sky inside the front at either close camera (FRN-08: 0 px at both) |
| The stand-in night light or glass visible | no: the spill is invisible, the lamp pool is out of the glass, the frame is not burnt |

**The content rule:** no drink, gambling, child or toy, no barcode, no modern packaging. White spirit, paraffin, washing soda and disinfectant are goods of the trade, not drink. The one breach is point 1.

## What is right

**The room is the game's rule, pixel for pixel, and a full ironmonger's.**
- the drawer wall of 60 drawers with brass label holders;
- the shelf unit of tins, oils and oil cans;
- the counter with the till, the measuring tape and the toolboxes;
- the pegboards in rows;
- the dustbin, cans and cement bags.

It moves true between the two cameras. From CLOSE_35_B the window's far end is the left return wall, plaster over the green dado, meeting the card with no step and no black slab.

**The near metre reads as a 1990 ironmonger's window,** with every scan at its own size:
- the 36-tin pyramid of the project's paints, whole under the lifted glove shelf;
- six gloves on a deal shelf hung by four cords from an iron rod under the transom;
- twelve clear bulbs with bayonet caps in deal trays;
- trowels on stepped blocks;
- two green cantilever toolboxes;
- a planked, nailed and stencilled crate with weathered oil tins, four labelled cleaners and a brass blowlamp;
- galvanised watering cans, the sprinkler and the pump;
- the sledgehammer with an ash shaft;
- three brooms stood heads up, as shops stand them;
- eleven hand-lettered price cards.

Nothing is buried or passes through a support (DSP-03, and the glb's contacts).

**Lit and shaded as a shop.** By day the sky lights the bed through the glass and the goods fall off front to back. In the lit test state there is no arc, no burnt band, and dark mullions.

**The doors match the target.**
- The T1 leaf: glass from 871 with the bar at 1423, the brass letter plate in the lock rail, the brass lever, the kick plate.
- The green OPEN card by day and the red CLOSED card at night.
- The gilt hours plate on the lower pane and the gilt 16 on the fanlight.
- The black side door under its drip, with its knob and plate.

There are no black strips at the jambs. The bell is on the top rail 90 mm from the hanging stile (FRN-03); 4 of FRN-13's 4,480 rays through the door's glass end on it.

**The glass reads as glass by day** (the opposite houses and trees in it, the room through it). The night glass now reflects only the dark street.

**The records are honest.** Every change of try 2 is named in NOTES with its row. The one failing row is reported, not hidden.

## What I cannot judge from the files

- **The game's own light and glass:** Lumen on the display, the street lamps' real light on a dark shop's goods (point 2's real answer), the glass's reflections and Fresnel at 61 degrees, the exposure, and the card under TSR (PC-01 to PC-07).
- **The new frames being rendered now** (the builder's gate run of 04:01 on 15 October) and the front glb rewritten at 03:50. I judged the 14 October files by their hashes.
- **CLOSE_35_B night_dark,** which was not rendered.
- **The bell's swing and sound.** Neither close frame shows the bell clearly (it is seen at most through the door's glass), and CLOSE_35_B does not frame the door.
- **The period look of three goods** that read more 2000s than 1990 to my eye, but which I cannot date without a photograph:
  - the knit gloves with a grey dipped palm;
  - the slim track pump;
  - the travelling sprinkler's yellow casting.

  No dated photograph of a 1985 to 1992 ironmonger's window was reached. That photograph, not memory, should decide them.
- **Wear, grime and wet,** which come from the game's layers (D53).
- **Anything of the street view.**
