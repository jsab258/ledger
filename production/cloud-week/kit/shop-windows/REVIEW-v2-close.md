PASS

# Rita's shop, the CLOSE view: fresh review, try 2 (cloud week 42, unit 7 part 2, 13 October 2026)

Reviewer: a fresh reviewer who did not write the target, build the shop or write try 1's review. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit. I did not read either street review.

Read: CLAUDE.md, RULINGS.md, NOTES.md (try 2, with its list of where it says a review was wrong), TARGET.md sections 3, 4, 6 and 13, TARGET-REVIEW.md (briefly), REVIEW-v1-close.md, `check_ritas_v2.json`, and the parts of sw_gate.py, sw_front.py, sw_display.py and sw_room.py named below.

Looked at: the two v2 close previews; the four close gate frames (2560 x 1440, the newest, 05:31 to 05:42) at 100 to 300 per cent; the check renders; the baked cards; the three 4096 room pictures; the v2 before-and-after sheet; the approved night shot (rita-night-kit-2026-10-06.jpg); try 1's close previews.

Measured and tested, all in my scratchpad (nothing in the repository or SCRATCH changed):
- the parallax, through `trace` itself;
- the display glb for intersections;
- ray casts through the side door's black lines, and a test render with one part moved 1 mm;
- the night luma of the goods through the lattice's gaps;
- the room's shelves and the till from placed.json;
- MANIFEST.json against the six files.

**In short:** every one of try 1's five faults is either fixed or turns out not to be a fault.
- **By day the near metre now reads as a pawnbroker's window.** There are rings, watches and chains in front; radios, clocks, cameras and binoculars on the tiers; nothing buried and nothing through a shelf.
- **The far end of the window is now a wall, not a black slab.**
- **The night arc and the burnt frame are gone.**
- **The two black lines beside the side door are still there, and wider.** They are not openings, though: two parts were built in the same plane. Moving them 1 mm apart clears them (tested).

What is left is eleven narrow points. The most visible is at night: the goods on the middle tier and on the step are dark shapes in front of a bright room. By Jafar's ruling of 9 October this is a PASS with the points listed below. Points 1 to 3 should be fixed before his page.

0 faults, 11 narrow points.

## Try 1's review, item by item

| try 1 item | now | where in the v2 pictures (2560 frames unless said), measurement |
|---|---|---|
| Fault 1: goods buried in pedestals, vases through a shelf | **FIXED** | No pedestals. brass_vase_01 stands on the top tier with nothing above it (CLOSE_35 day 2008-2232, 176-776). The portable cassette players stand whole on the middle tier (CLOSE_35 day 2232-2416, 952-1064; CLOSE_35_B day 1256-1352, 840-920). The pocket watches lie on their pads (CLOSE_35 day 1062-1118, 1130-1152). My own test on ritas_display.glb: 149 piece meshes; no piece vertex inside any board by more than 3 mm; no piece with vertices both above and below a board inside its footprint. DSP-03 agrees (0 of 14 pairs, lowest silhouette 0.75). |
| Fault 2: not a pawnbroker's window | **FIXED** (by day) | The front row is back: 4 ring trays of 24, 4 watch pads, 2 chains, with the spectacles, lighter, magnifier and cigarette case (CLOSE_35 day 640-2440, 1040-1440; CLOSE_35_B day 1520-1970, 1008-1136). The middle tier holds stock at real size: alarm clocks, the cassette player, the mantel clock, binoculars, the two portable players and a standing frame (CLOSE_35_B day 100-1500, 740-1060). The top tier holds three vases, the boombox, the projector, the horse and one frame. DSP-04: the longest empty run is 0.163 m. The scripted watches are still crude at 100 per cent (narrow 7). |
| Fault 3: the black slab from CLOSE_35_B | **FIXED** | The return wall shows plaster over a brown dado, with the dado line at y ≈ 590 where it should be (CLOSE_35_B day 1690-2050, 130-1040). Try 1's box (1830-2050, 100-1020) now has mean luma 76.3 (try 1: 36; 69.3 with the reflection off, against the room beside it at 50.8). LIT-02b at CLOSE_35_B: 0.18 per cent by day, 0.15 per cent at night. |
| Fault 4: the white arc, the burnt head band and the burnt frame | **FIXED** | No arc and no clipped band under the head in either night frame. Pixels at 250 or more: 0.42 per cent (CLOSE_35 night) and 0.80 per cent (CLOSE_35_B night); try 1 had 3.3 and 3.1. What remains is white goods: the white vase (CLOSE_35 night 1278-1338, 580-649), the blue-and-white vase and a standing frame's mount (CLOSE_35_B night 398-514, 450-526 and 79-202, 594-659). The mullions are lit only by the street lamps. |
| Fault 5: two open slots beside the side door | **NOT FIXED, and its cause was wrong**; now narrow point 2 | The two black lines are still there and wider: 6 to 9 px at 2560, against 2 to 3 in try 1 (4 to 5 px in the preview, against 1 to 2). They are not slots. Try 1's fix, built as worded, widened them. |
| Narrow 1: the day glass shut out the sky | **FIXED** | The pane passes shadow rays by day. The velvet tops read maroon, not black: CLOSE_35_B day, step 68, middle tier 92, top tier 73, bed 65 (luma). |
| Narrow 2: the side boards were bare | **PARTLY** | Left board covered 66 per cent (ROOM-01). The right board is 18 per cent (ROOM-02 fails): narrow point 6. |
| Narrow 3: stock-wall scales 0.45 to 1.45 | **FIXED** | Scales 0.906 to 1.000, the television sets at 1.0 (SO-06). Following it left the stock wall plainer: narrow point 4. |
| Narrow 4: the room seen from 1.05 m above its floor; the counter's jewellery | **PARTLY** | The counter's bed is raked 25 degrees. From both close cameras the case is behind the top tier's goods, so I could not judge it here. The card's bottom to the footway is for the target's owner (all shops), as the target's X1 says. |
| Narrow 5: CASH LOANS on the counter's front | **FIXED** | It is on the back wall above the counter and moves with the wall. It reads only at 200 per cent: narrow point 10. |
| Narrow 6: plain boxes on square posts | **FIXED** | The velvet has sheen and a cloth normal map, the edges are bevelled, and the posts are thin round black rods (CLOSE_35_B day, under each tier). |
| Narrow 7: clip-art prints | **FIXED** | Harbour photographs in white mounts (CLOSE_35 day 1890-2080, 820-1040; CLOSE_35_B day 16-240, 570-790). No person in them. |
| Narrow 8: the bell read as a lampshade | **FIXED in the model, not seen** | Measured on ritas_front.glb: lip 70 mm, height 55 mm, crown loop, clapper under the lip. The display's door-end return wall now hides it from CLOSE_35, and CLOSE_35_B does not frame the door. It also hangs in the wrong place: narrow point 9. |
| Narrow 9: paint and wear | owed | It is in the target (W1) for the game's wear layer (D53), on the PC. |
| Narrow 10: the unrecorded highlight shoulder | **FIXED** | PIC-05 is measured before the shoulder: 0.0052 by day, 0.0011 at night. The shoulder is named in NOTES (judgement 19) and in the target. |
| Narrow 11: 64 samples | owed | 128 samples on the PC. |
| Narrow 12: no record of the versions reviewed | **FIXED** | MANIFEST.json: the sha256 of all six files (three glbs, three pictures) matches what is on disk. |
| Narrow 13: flat ceiling battens | **FIXED** | The fittings are 0.025 deep (SO-03) and read as tubes. |

## Faults

None.

## Narrow points, most visible first (each with its exact fix)

### 1. At night the middle tier and the step are dark shapes in front of a bright room

- **Where:** both night frames, the middle tier and the step.
  - CLOSE_35 night_lit: x 900-2400, y 780-1200.
  - CLOSE_35_B night_lit: x 0-1300, y 750-1200.
  - The alarm clocks, the mantel clock, the cassette players, the binoculars and the cameras do not read. The bed's front row and the top tier do read.
- **Measured** (CLOSE_35_B, luma, night counted only through the lattice's gaps):

  | what | by day | at night |
  |---|---|---|
  | alarm clock's white dial | 129 | 33 |
  | cassette player | 97 | 26 |
  | mantel clock dial | 111 | 25 |
  | video camera on the step | 57 | 31 |
  | room floor just behind them | 67 | 95 |
  | watch pads on the bed | 101 | 83 |

  The goods are a third as bright as the room behind them. The approved night shot (rita-night-kit-2026-10-06) is a low stepped bed lit end to end.
- **Cause:**
  - The display is stacked shelves. The middle tier (v 0.18-0.53) covers the whole step, and the top tier (v 0.22-0.53) covers the middle tier.
  - The only light is the head spill: 0.10 behind the wall face, z 2.30, 62 degrees down. Each tier shades the one below it.
  - The card lights nothing, by the game's rule.
  - Try 1's night frames show the same thing. Try 1's review did not raise it. Moving the spill 0.12 m back for the street review made it a little worse.
  - I weighed this as a fault. It is narrow because nothing looks broken: it reads as a head-lit set of shelves in front of a lit shop. LIT-05 passes, and the fix is bounded.
- **Whose:**
  - **The builder:** opaque stacked tiers with a single head light.
  - **The target:** 4.5's zones stack the tiers over the same depth, and 4.6 keeps one rect light.
- **Exact fix:**
  - **(a) Two strip lights** in the display, on the display's light channel:
    - each a rect 3.20 x 0.02 m, 8 mm under the front edge of a tier board: middle tier at v 0.20, w 0.377; top tier at v 0.24, w 0.727;
    - facing down, tipped 30 degrees toward the back, 3000 K;
    - strength set by (b).
    - The game's display entry takes the same two strips (shop-interiors.json, pawnbroker display lights), to be measured on the PC with PC-02.
  - **(b) A new check, LIT-08:** at night_lit, from CLOSE_35 and CLOSE_35_B, each display piece's mean luma over the lattice's gaps is at least 0.6 of the room's mean luma seen round it. PIC-05g stays at or under 0.01.

### 2. Two black lines the full height of the side door (try 1's fault 5, re-diagnosed)

- **Where:** CLOSE_35 day, about 10,400 px of luma 0 to 2.
  - Between the pilaster and the side door: x 117-123 at y 300, running to 183-188 at y 900.
  - Between the side door and the shop door's frame: x 261-269 at y 300, running to 319-326 at y 900.
  - Preview: x 73-76 and 159-168 at y 188.
- **Cause (tested):** there is no opening.
  - FRN-07 finds 0 uncovered pixels on the elevation. FRN-08 finds 0 backdrop pixels from CLOSE_35.
  - Ray casts from CLOSE_35's eye through every black pixel hit white joinery first.
  - F1's own frame jambs (`frame_jamb_L`, `frame_jamb_R`) were never missing. They are clipped to the slot with their front face at d 100 (model y −0.100).
  - Try 2's added boxes (`side_jamb_l/r`, white) and the fillers (`side_filler_l/r`, oxblood) put their front faces in that same plane, overlapping F1's jambs by up to 41 mm a side.
  - Cycles draws coincident faces black. Unreal will flicker between the two (white and oxblood, on a 12 mm strip each side).
  - In try 1 only the fillers overlapped (12 mm), hence the thinner lines. Try 1's review read the result as open slots.
  - **Test:** the same crop rendered with `side_jamb_*` and `side_filler_*` moved 1 mm back has 0 dark pixels.
- **Whose:**
  - **Try 1's review:** the wrong cause.
  - **The builder:** boxes added in the same plane as F1's frame. FRN-08 looks for backdrop showing through, not for black.
- **Exact fix:**
  - In sw_front.py, `side_jamb_*` and `side_filler_*` run from d 0 to 99, not 100. Deleting the two `side_jamb_*` boxes also works, since F1's jambs already close u 374.4-403 and 1241-1269.6.
  - **A new check, FRN-10, failing the build:**
    - no faces of two different parts of the front lie within 0.5 mm of the same plane while overlapping by more than 1 mm²;
    - no pixel of the front under luma 5 in the CLOSE_35 and CLOSE_35_B day frames.

### 3. At night the gate's glass doubles everything behind it

- **Where:**
  - CLOSE_35 night_lit:
    - a second red projector reel about 66 px to the left of the real one (about 1010-1070, 520-600);
    - a second white vase about 75 px to the right of the vase (about 1355-1430, 470-700).
  - CLOSE_35_B night_lit: the middle tier's goods look half see-through, for example the alarm clock at 100-250, 940-1110.
- **Cause:**
  - Each pane is a closed 6 mm slab, 12 faces, model y −0.036 to −0.030.
  - The gate's night glass mixes 0.8 Transparent with 0.2 Glass BSDF on both faces. A ray that bends at one face and passes straight through the other comes out bent by up to about 20 degrees, so about 0.3 of each pixel is a shifted picture.
  - By day the slab is all Glass BSDF, so there is no ghost. The game's glass is the game's.
- **Whose:** the builder (sw_gate.py, the gate's glass).
- **Exact fix:**
  - For both states, replace the Glass BSDF with a thin glass that does not bend light: `Mix(Transparent BSDF, Glossy BSDF (GGX, roughness 0.02, colour 1.0), factor = refl x Fresnel(IOR 1.5))`, with refl 1.0 by day and 0.2 at night.
  - Check: the red reel appears once in CLOSE_35 night_lit.

### 4. The room's stock wall reads plainer than the approved room, and the left board's clocks stand in a row

- **Where:** ritas-room-day-v2 and the before-and-after sheet. From the close views, the stock wall behind the top tier (CLOSE_35 day 1170-1890, 335-640). The builder lists it as a known shortfall.
- **Measured** from placed.json:
  - Along their length the shelves are full: each run is 76 to 93 per cent occupied, and the longest gap is 0.13 m. So the builder is right that more pieces at real size will not fit.
  - The empty look comes from height: small goods 0.10 to 0.25 m tall stand on boards 0.45 to 0.50 m apart.
  - There is bare wall above the upper television sets (x −1.9 to 0.9, z 2.21-2.40), since the top tier was cut.
  - The approved picture had five full-width tiers.
  - The left board's six wall clocks are the same model, at one height, in a row: the regular-grid look the third review failed on 3 October.
- **Whose:** the target (tier spacing and counts), following try 1's narrow 3.
- **Exact fix:**
  - On both television boards (z 1.35 and 1.80), a riser shelf 0.20 high and 0.20 deep against the wall, in every run beside and between the sets.
  - Fill the risers from the same pool at 0.9 to 1.0 (cameras, alarm clocks, cassette players, binoculars, the toolbox) to the same 85 per cent along their length, about 14 more pieces.
  - Put one cardboard_box_01 on top of each upper set.
  - The six wall clocks go in two staggered rows (z 1.55 and 1.85, ±0.05). Each shows a different time (turn its hand meshes) at a scale of 0.9 to 1.0, never more than three in a line.

### 5. The till passes up through the shelf above the counter

- **Where:**
  - CLOSE_35_B day, about 680-760, 495-560: the till's top shows above the board, with the board across it (seen at 300 per cent).
  - Room picture 2150-2350, 850-1000.
  - Try 1's room has the same fault.
- **Measured** (placed.json):
  - CashRegister_01: x 0.28-0.72, y 3.99-4.45, z 1.05-1.47.
  - The z 1.35 television board: x −1.9-0.9, y 4.15-4.495, z 1.325-1.35.
  - The till rises 0.12 m through the board and into the box standing on it.
- **Whose:** the builder. sw_room.py stands the till at cy0 + 0.32, under the board.
- **Exact fix:**
  - End the z 1.35 television board at x 0.20. Its pieces right of 0.20 move to the risers of point 4.
  - Add the room's placed goods and fixtures to an intersection test, SO-07: no room mesh intersects another, 2 mm tolerance.

### 6. The right board is 18 per cent covered (ROOM-02 fails)

- **Where:**
  - The room picture's right wall: the lower third of the board is bare.
  - From the close view, the right edge of CLOSE_35 day (2210-2560, 0-640).
- **The builder's claim:** it is right that doubling the counts reaches 0.88 of 4.93 m², and cannot reach 60 per cent with slim tools. Try 1's count list was an example that could not meet its own number. The builder is wrong to stop at the example: the point was a covered board.
- **Whose:** try 1's review (the arithmetic) and the builder.
- **Exact fix:**
  - Fill the board by rows across its full 2.9 m, each row's tools 0.04 to 0.06 m apart, from the same six models at 0.9 to 1.0 (about 60 tools):
    - saws at z 1.85-2.10;
    - hammers and pipe wrenches at 1.40-1.80;
    - pliers and adjustable wrenches at 0.95-1.35;
    - combination wrenches and the planes at 0.50-0.90.
  - ROOM-02 then measures each row: at least 80 per cent of the board's width filled. An area share by bounding box does not measure slim tools.

### 7. The scripted watches and chains read as tokens and beads at 100 per cent

- **Where:** CLOSE_35 day.
  - The watch pads (1680-1915, 1280-1385): plain white discs in gold or silver rims, with no marks or hands.
  - The chains (for example 1320-1405, 1195-1230): a row of 18 separate beads.
  - The four Poly Haven pocket watches beside them have real dials.
- **Whose:** the approved recipe's scripted forms, kept by the builder.
- **Exact fix:**
  - **Dials:** a dial map painted by script, 256 px: 12 hour marks, two hands at a random time, four grounds (white, cream, black, champagne).
  - **Chains:** 60 links of 4 x 1.2 mm, each turned 90 degrees to the last, 2.4 mm apart, along the same arc.
  - The rings stay as they are; they read as rings.

### 8. LIT-02b fails at STREET_30 (1.13 per cent by day, 1.29 at night), but there is no void

- **Where:** the STREET_30 check frames with the reflection off.
  - The dark pixels are a scatter of shade lines under the stock wall's shelves.
  - The largest is one patch under the middle tier in the middle light, about 35 x 10 px of 1280.
  - Nothing like try 1's slab, which was a third of the window.
- **Whose:** the check's wording (try 1's review, fix 3c): a share of dark pixels counts the room's own dark shade under the day card's 0.15 as if it were a void.
- **Exact fix:**
  - LIT-02b's limit becomes a slab test: the largest dilated patch, as the row now measures it, is at most 1 per cent of the window's glass where the glass shows the room. STREET_30 is at 0.63 and 0.67 per cent; try 1's slab was about 33 per cent.
  - The share stays in the row's text as information.

### 9. The bell hangs on the hinge stile, behind it, not on the top rail

- **Measured** on ritas_front.glb (model x):
  - spring strip −0.853 to −0.833;
  - hinge stile −0.868 to −0.753;
  - top rail −1.538 to −0.868.
- The strip is on the stile, 90 mm from the leaf's edge, so the bell (−0.878 to −0.808) is hidden behind the 115 mm stile.
- The target puts it on the top rail, 90 mm from the hanging stile, where it shows in the upper pane's top corner.
- **Whose:** the builder.
- **Exact fix:** centre the strip at model x −0.958 (on the rail, 90 mm in from the stile's inner edge), with the bell 80 mm below as now.

### 10. CASH LOANS on the back wall is a grey smear

- **Where:**
  - CLOSE_35 day about 1350-1520, 525-560.
  - CLOSE_35_B day about 260-430, 515-550.
  - The words read only at 200 per cent. The card (188, 182, 168) hangs in the shadow under the z 1.35 board, and the day card's 0.15 flattens it.
- **Whose:** the builder.
- **Exact fix:** paper (235, 232, 222), ink (25, 25, 50), hung 0.05 m lower.

### 11. The projector has a continental two-pin plug

- **Where:** CLOSE_35_B day 773-797, 707-740: a round two-pin plug at the end of the flex, readable at 100 per cent.
- A British pawnbroker whose notice says ALL ELECTRICAL GOODS TESTED fits a three-pin 13 A plug (BS 1363).
- **Whose:** the model.
- **Exact fix:** coil the flex behind the projector so the plug is hidden, or replace it with a scripted 13 A plug: 51 x 45 x 25 mm, black, three flat pins.

**Known and owed, not counted:**
- the joinery's wear (W1, the D53 layer);
- 128 samples;
- the game's glass, Lumen, exposure and TSR (PC-01 to PC-03);
- the room's floor at the bed's height (for the target's owner);
- catalogue lines for the Lake Pier HDRI and ambientCG Fabric034 (CATALOGUE.md is outside the unit).

## The builder's claims that a review was wrong (NOTES, try 2)

1. **Television tiers at 1.35 and 1.80 against a top tier at 2.05: right.** The upper sets' tops stand at 2.2114 (placed.json), and cutting the top tier over them is a fair answer.
   - Right also that "about 12 more pieces" will not fit along the shelves: they are 76 to 93 per cent full.
   - But neither the counts nor more pieces cure the plain look. The tier spacing does (point 4).
2. **Both brass vases (1b) against one brass vase (2d), and the boombox: right.** The review contradicted itself. The boombox stands 0.47 m with its aerial and cannot go under a 0.335 clearance. Following 2d, with the boombox on the top tier, reads well (CLOSE_35 day).
3. **The front row's box, close against street: right,** and it makes no difference (20 mm at most).
4. **The hall 0.50 m deep, not 1.2: right by the geometry.** The card stands 0.58 m behind the wall face. From CLOSE_35 the side door's fanlight shows a dim hall and none of the room (FRN-09: 0 of 560 rays reach the card).
5. **The pavement pool: I cannot judge it from the close view.** The gate's spill lights only the display, and the game's pool is owed (PC-02).
6. **60 per cent against doubled counts: right on the arithmetic, wrong to stop there.** See point 6.
7. **"Fault 5 and street N2 are one cause": wrong for the side door.** There was never a gap. Two parts were built in the same plane (point 2). The street sliver I did not judge.
8. **The fascia's wear map:** not in the close view. Not judged.
- **Judgement 26 (LIT-02b counts only the glass that shows the room): right.** Dark velvet and black plastic are goods, not voids. Measured that way, CLOSE_35_B passes clearly.

## The two failing rows

- **LIT-02b at STREET_30: a narrow point.** There is no void (point 8).
- **ROOM-02: a narrow point.** The right board is a room detail seen at the edge of CLOSE_35 (point 6).

## Measured

**Parallax.** The game's own `trace`, imported:
- The card's centre samples the picture at u 0.17180 from CLOSE_35 and 0.49459 from CLOSE_35_B: 1322.1 px of 4096 apart. PRJ-02 is confirmed.
- **My point:** the stock wall's wall clock, picture pixel (2496, 800).
  - By the rule it lands on card column 2110.4 from CLOSE_35 and 1453.7 from CLOSE_35_B, row 582.3 in both.
  - That is 656.7 card px, or 1.360 m on the card for 2.0 m of eye travel (2.0 x 4.5 / 6.62). `trace` sends both card points back to (2496.0, 800.0).
  - In the gate's baked day cards, the CLOSE_35 patch is found in the CLOSE_35_B card at offset (−1, 0), correlation 0.971.
- **A second point,** the boombox (1833, 600): found at (0, 0), correlation 0.996.
- **Recomputing** a 46 x 51 card-pixel patch round the clock through `trace` and the build's own sampler gives a mean difference of 0.000 and a largest of 0. PRJ-03 is confirmed.

**Legible words at 100 per cent, both close views, day and night.** Nine distinct words:
- WATCHES, JEWELLERY, LOANS (CLOSE_35_B's JEWELLERY loses its second L to the sky's reflection);
- OPEN by day, CLOSED at night;
- MON-SAT, WED, SUN;
- "No." on the tickets.

Numbers: 5, 9-5.30, 9-1, the tickets' four-digit numbers (soft) and the clocks' numerals.

All are the project's own and acceptable.
- **At 200 per cent:** CASH LOANS.
- **At 300 per cent:** "B", "90" and "HIGH FIDELITY" on the cassette player's tape label. These are generic words, not a maker's.
- **I looked hard at** the cassette players, the boombox, the portable players, the cameras, the clocks, the till and the toolbox. No maker's name or modern mark is legible.

## What is right

- **By day the near metre is a pawnbroker's window.** Rings in navy trays, watches on pads, chains, small valuables and the tobacco pieces lie in front. Radios, clocks, cameras and binoculars stand on the tiers; vases, the boombox and the projector are on top. Each has its ticket, all at real size.
- **The Poly Haven goods read as real objects:** the clocks, cameras, cassette players, boombox, binoculars, brass vase, jug and flashlight.
- **The furniture now reads as velvet** over thin rods, not as boxes.
- **Nothing is buried, nothing passes through a board,** and every piece shows.
- **The room behaves exactly as the game's rule says** and reads as a deep, lit room. The stock wall, back door and side boards shift between the two cameras. There is no seam where the display meets the room. By day the display is brighter than the dim room behind it, as a shop window is.
- **The far end of the window from CLOSE_35_B** is a plaster wall over a brown dado, meeting the room without a step.
- **Night:** no arc, no burnt head, the frame lit only by the street. The CLOSED card is turned and the lattice is down.
- **The door matches the target:**
  - glass from 871, with the bar at 1423;
  - the lever on the left stile, the brass letter plate in the lock rail, the brass kick plate;
  - the OPEN card by day and CLOSED at night;
  - the gilt hours plate and the gilt 5 on the fanlight;
  - the band above both doors.
  - The side door's fanlight shows a dim hall.
- **The content rule holds:** no drink, gambling, child, toy or weapon in the display, and nothing after 1992. The cigarette case and lighter are allowed.
- **MANIFEST.json names exactly the files reviewed.**

## What I cannot judge from the files

- **The game's glass, light and image:** the glass's reflections and its hand-over at 61 degrees, Lumen's light on the display (and so what point 1's strips must be in lumens), the exposure, the card under TSR, the frame time.
- **The side door in Unreal:** whether the shared plane of point 2 shows as flicker. After the fix it is moot.
- **The bell:** it is not visible from either close camera. Its swing and sound are not in the files either.
- **Wear, grime and wet,** which come from the game's own layers.
- **The counter's raked jewellery,** which is behind the top tier from both close cameras.
- **Anything of the street view,** and Jafar's open question on the glass foot (871, 600 or about 1000), which is his.
