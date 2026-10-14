FAIL

# The launderette (Steam Laundry, east_parade bay 4, no. 9), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit. I did not read the street review of this shop or any other shop's review.

Read: CLAUDE.md, RULINGS.md (1, 2, 3 and 9 October), NOTES.md ("For the next nine shops", batch A's and batch B's lessons 16 to 41, "What batch B changed", the launderette's section), TARGET.md sections 3, 5.4 and 13 (B1 to B4, B12, B13), Rita's four reviews, `checks/check_steam_laundry_v1.json`, and the parts of sw_gate.py, sw_goods_b.py, sw_shops_laundry.py and sw_room_gen.py named below.

Looked at: the eight previews of 13 October; the four close gate frames (2560 x 1440) at 100 to 300 per cent; the check renders that remain (reflection-off frames, glass and room masks, object index, front-on-backdrop); the three 4096 room pictures; the wall clock's and the basket's 1k base colours beside the originals.

Measured, all in my scratchpad (nothing in the repository or the scratch folder was changed; no render was run): the parallax through the game's own `trace`; the baked cards; the glass luma; flat, black and burnt regions; both glbs (normal maps, UVs, part positions); the manifest's sha256 (all five files match).

**In short:** the room behind the glass works. It moves exactly as the game's rule says, it reads as a deep, lit launderette, and the far end at CLOSE_35_B is a wall, not a slab. The window reads as a launderette's at a glance.

But the near metre, which is what this view is for, does not hold at 100 per cent:
- the five towel stacks read as stacks of plaid cushions, not towels;
- the washing in the baskets is smooth untextured blobs, one of them a blue column like a box;
- two packets carry the name of a real British laundry-trade firm (BRIGHTWELL).

Three faults, eight narrow points, and one new finding from the shared gate.

## Faults, worst first

### 1. The towels read as plaid cushions, not folded towels

- **Where:** CLOSE_35_B day, the whole left half of the bed, 2560 frame (0-1290, 860-1440), preview (0-805, 540-900); CLOSE_35 day (615-1290, 790-1150), preview (385-805, 495-720). Night the same: CLOSE_35_B night_lit (450-1300, 880-1150).
- **What it looks like at 100 per cent:**
  - a check of about 2 cm cells in strong light and dark, so each top reads as tartan flannel;
  - every towel is a rigid slab of one thickness with the same small bevel on all four edges, so the stacks read as foam seat pads;
  - the sides carry a stretched band of the same picture (horizontal streaks), and the two border stripes run front to back near the left and right edges.
- **Cause:** `towel_atlas` (sw_goods_b.py) puts a 256 px crop of the 1024 px Fabric020 map over a whole 0.30 x 0.45 m top, at a contrast of 0.55 + 0.45 x the weave; `towel_box` is a box chamfered 12 mm; the sides take the tile's middle band.
- **Whose:** the builder. NOTES judgement L6 says the weave "reads as folded towels"; at the close cameras it does not. TRD-01 and DSP-03 pass because they measure silhouettes, not what the goods read as.
- **Exact fix (sw_goods_b.py and sw_shops_laundry.py):**
  - the weave at one sixth of its present size (cells about 3 mm) and a third of its contrast: g = 0.85 + 0.15 x the weave;
  - a terry pile: a fine bump (noise at about 600 a metre, 1 mm deep) baked into a real tangent-space normal map of 512 px, so GLB-01 still holds; roughness 1.0;
  - the folded edge to the street a half round of radius 23 mm (half the 49 mm towel), the other edges 5 mm;
  - each towel's width and depth jittered by up to 10 mm and its top sagging 3 mm in the middle, so a stack is soft, not machined;
  - one woven border band, 40 mm wide, across each towel 50 mm behind the folded edge, not two stripes front to back.
  - Then look again at CLOSE_35_B at 100 per cent in the box above.

### 2. The washing in the baskets is smooth blobs, with a blue column like a box

- **Where:** CLOSE_35 day (1310-1870, 1000-1300), preview (820-1170, 625-810); CLOSE_35_B day (1300-1680, 920-1150).
- **What it looks like:**
  - each heap is a smooth flat-coloured lump with no cloth, weave or creases;
  - the heaps stand on top of the baskets like caps;
  - in the left basket a pale blue column (the first lump, 0.072 at the foot and 0.15 high) stands under the cloth and reads as a box;
  - in the right basket a tan cone pokes a spike up through the mint sheet (CLOSE_35 day about 1700-1710, 1095-1110).
- **Cause:** `GB.heap` lumps with plain materials (laundry_a1 to b3: base colour only, no texture). DSP-03 tests pairs of groups, so a lump through another lump of the same object is not tested.
- **Whose:** the builder. NOTES lists it as a shortfall that "from CLOSE_35 reads as laundry". It does not at 100 per cent.
- **Exact fix:**
  - first search CATALOGUE.md and the CC0 libraries for a scanned pile of cloth or laundry, and use it at real size if one exists (CLAUDE.md, reuse first);
  - otherwise make the washing by Blender cloth simulation: in each basket three sheets of 0.9 x 0.7 m (40 x 30 quads, cotton preset, self-collision on, the basket's mesh as a collider at 3 mm), dropped from 0.3 m above the rim for 120 frames, applied, then given 2 mm thickness;
  - colour: the present colours times a cotton weave at a 3 mm cell (Fabric020 as in fault 1), with a normal map;
  - no standing column: the cloth fills the basket by itself, and nothing passes through another sheet (DSP-03 run inside the group too).

### 3. BRIGHTWELL is a real British firm in the laundry trade

- **Where:** CLOSE_35 day, the red BRIGHTWELL WASHING POWDER box (2048-2200, 1040-1264) and the blue BRIGHTWELL AUTOMATIC 3 kg packet (2088-2208, 1208-1424); CLOSE_35_B day (1683-1822, 853-1033).
- **Why it is a fault:** Brightwell Dispensers Ltd of Newhaven, East Sussex (founded 1947) makes laundry detergent dosing equipment for washing machines, soap dispensers and chemical dosing systems. A washing powder named BRIGHTWELL in a launderette window carries a real firm's name in its own trade. The brief and CLAUDE.md allow only invented makers.
  - The other five makers (HOLME, MEADOWS, ASHDOWN, LINDEN, FERNSIDE) came back as no known soap or detergent brand in my two searches. That check was not exhaustive.
- **Whose:** the builder. The blocklist checks (NEV-01, INV-05) can only catch names that are on the list.
- **Exact fix:**
  - rename the maker on both packets;
  - check the new name, and the other five, against Companies House and a web search for soap, detergent and laundry firms before use, and write the result in NOTES;
  - add BRIGHTWELL to the content blocklist so NEV-01 fails it from now on.

## Narrow points (each with its exact fix; none fails the view alone)

1. **The room's floor is a flat charcoal sheet.**
   - **Where:** most of the glass behind the display at both cameras. CLOSE_35 day (1728-1888, 864-1024): luma 29.3, standard deviation 0.5, high-pass 0.5. At night_lit: 39.6 and 1.3. Of the room's 32 px blocks in the glass, 181 at CLOSE_35 day and 160 at CLOSE_35_B day are dark and flat (luma about 30, standard deviation under 1).
   - The target's grey vinyl tile and worn path do not show. It reads as a floor, not a void (its edges meet the walls and the machines), which is why this is narrow.
   - **Cause:** Poly Haven rubber_tiles is a near-black texture (mean 33 of 255), and a multiplied tint (92, 94, 96) cannot make it grey. Its real tile is 0.5 m (the texture is 2.0 m with four tiles across), and FLOOR_TILE_M 1.0 halves it.
   - **Whose:** the builder.
   - **Fix:**
     - divide the floor's diffuse by its own mean and multiply by (150, 152, 150), so the joints stay and the floor's mean in the day picture is about 110;
     - FLOOR_TILE_M 1.2 for the target's 300 mm tile;
     - the worn path 10 per cent darker than that.
     - Check: the floor's 32 px blocks at CLOSE_35 day have a mean of 45 or more and a standard deviation of 2 or more.
     - Once the floor is pale, the 0.06 m strip of the gate's dark `reveal_floor` between the bed's back (v 0.55) and the card (0.61) may show as a line. Run the bed cover on to v 0.60, or give that strip the floor's colour.
2. **Two parts share a face plane at the window's door end.** This is the black-strip fault of Rita's try 2, between two glbs this time.
   - **Where:** CLOSE_35 night_lit, a darker vertical band x 648-688, the full height of the return wall (about y 200-1000), luma 59 against 76 beside it. It is also in the reflection-off day render (1280 frame x 324-344, 59 against 77). By day the glass's reflection hides it.
   - **Cause:** the display glb's `return_wall_l` (display x -1.685 to -1.675 = model x -0.710 to -0.700) has its face at model x -0.700. That is the same plane as the front glb's `door_jamb_r` face (x -0.750 to -0.700, d -0.20 to -0.30). Projecting d -0.20 and -0.30 into CLOSE_35 gives x 653 and 693, which is the band. `lobby_kick_w` and the lobby's two rails also end at x -0.700.
   - Cycles shades the shared faces dark; Unreal will flicker there. FRN-10 tests the front's parts only, and DSP-03 tests the display's parts only.
   - **Whose:** the builder (the kit's rule 1).
   - **Fix:**
     - `return_wall_l` and `return_wall_r` stand 1 mm inside the window zone: display x -1.674 to -1.664 and 1.664 to 1.674;
     - FRN-10's coplanar test runs over the front glb and the display glb together.
3. **The price cards stand before the wrong goods** (lesson 29 repeated).
   - **Where:**
     - CLOSE_35 day: POWDER 49p stands before HOLME SOAP FLAKES (1984-2064, 1315-1363), and SOAP FLAKES 58p before LINDEN WASHING SODA (2272-2360, 1392-1432);
     - CLOSE_35_B day: SOAP FLAKES 58p stands before FERNSIDE WASHING-UP LIQUID (1870-1895, 983-1012).
   - The cards stand at the bed's front edge, so the parallax moves each one under a neighbour.
   - **Whose:** the builder.
   - **Fix:** each card 8 mm in front of its own good, centred on it: SOAP FLAKES 58p at u 2.76, v 0.192 (the HOLME 1 kg packet); POWDER 49p at u 2.90, v 0.192 (BRIGHTWELL AUTOMATIC, renamed); BLEACH 42p before the bleach bottle.
4. **A cardboard box of fabric softener marked "1 litre".**
   - **Where:** the ASHDOWN box, CLOSE_35 day (2376-2560, 1096-1328): FABRIC SOFTENER, waves, "1 litre".
   - A litre is a liquid's measure, and in 1990 the product came in bottles.
   - **Whose:** the builder.
   - **Fix:** make ASHDOWN a bottle, "FABRIC CONDITIONER" (the British word) "1 litre", and give the step's fourth box a powder, for example "NON-BIOLOGICAL 2 kg".
5. **The two return walls are another material from the room's side walls.**
   - **Where:** CLOSE_35 day (550-790, 200-1000) and CLOSE_35_B day and night (about 1800-2000, 300-1000).
   - The tiled side wall turns into horizontal streaks with no vertical joints, with a visible change where the return wall meets the card. The gate's `wall_material` stretches one 8 px column of the picture along the wall's 0.61 m depth.
   - In the game the glb's `return_dado` is a flat colour (0.64, 0.63, 0.56 linear) with no tile at all.
   - **Whose:** the kit (the gate's material) and the builder (the glb's material).
   - **Fix:**
     - in the gate, sample the picture's own side-wall band by depth: columns 3885 to 4096 for the right wall and 0 to 211 for the left (the side wall's first 0.61 m), with v scaled by the wall's perspective at that depth, instead of one column;
     - in the glb, `return_dado` takes long_white_tiles at its real size (point 6), world-mapped, tinted as the room's dado.
6. **The dado tile is at 0.71 of its real size.** Poly Haven gives long_white_tiles as 1.27 m; WALL_TILE_M is 0.9. The result is a mosaic of 26 x 90 mm slivers (room picture back wall, beside the dryers; CLOSE_35 day 1560-1630, 480-750).
   - **Whose:** the builder.
   - **Fix:** WALL_TILE_M["steam_laundry"] = 1.27.
7. **The printed goods are clean flat graphics.**
   - Eight packets with flat icons (two drops, two sets of waves, a star, a sun, a triangle), perfect card edges, no wear (CLOSE_35 day 1900-2560, 1030-1440). This is the shared point (h), and this shop's to judge.
   - At close range they read as plausible 1990 packets in a computer's finish.
   - **Whose:** the builder (named in NOTES; printed pictures from CC0 photographs are owed).
   - **Fix:**
     - LINDEN gets its own picture, not ASHDOWN's waves;
     - three of the eight packets get crushed corners of 2 to 3 mm and a 5 per cent scuff on the front's lower band;
     - the CC0 photographs as NOTES already owes.
8. **The machines are plain** (the builder's named shortfall). At close range they read as 1990 coin-operated front loaders: a control strip, a dial, a blank coin plate and a round door, with no display. But washers and dryers are the same box.
   - **Whose:** the builder.
   - **Fix (before his page, not before merging):**
     - a soap drawer 0.22 x 0.07 m at the left of each washer's strip;
     - a coin slide with a stamped "50p" on each machine;
     - the dryers' doors at 0.42 m glass, as commercial dryers had.

**Known and owed, not counted:** 48 samples (128 on the PC); the game's glass, Lumen, exposure and TSR (PC-01 to PC-03); catalogue lines for the textures and models (NOTES "Owed").

## New, from the shared gate (named here; it does not decide this shop's verdict)

**The gate's `reveal_floor` stands in the lobby, in front of the shop door.**
- **Where:** CLOSE_35 day (393-550, 930-1170), preview (245-345, 580-730). It is a dark box 0.53 m high with a lit top, standing on the lobby floor in front of the door's lower half. By day its face reads luma 48 (standard deviation 1.2); at night it is 4.4, pure black.
- It hides the door's glass foot (198) and the letter plate (z 113). It shows in STREET_SQUARE as well, as a dark lower panel on the shop door. I note it but do not judge it there.
- **Cause:** sw_gate.py builds `reveal_floor` from gate y 0.02 to the card over the whole bay width, at z 0 to 0.55. The front's lobby runs from d +0.10 to the door leaf at d -0.23 to -0.28. So the slab fills the lobby from d -0.02 to -0.23.
  - Its projected corners in CLOSE_35 (x 403-620, y 961-1259) match the box.
  - The gate's room mask counts it as room. When I first measured black pixels over that mask, the 6,796 black pixels at CLOSE_35 night_lit were this box, not the window.
- **Whose:** the kit. Every shop with a recessed lobby (the grocer too) is likely to show it. The game has no such slab.
- **Exact fix:**
  - in sw_gate.py, build `reveal_floor` over the window zone from y 0.02 as now, but over the door zones only from behind the front's `door_hall_floor` (y 0.47);
  - the target's owner says what a door glazed from 198 mm shows below the card's bottom (0.55 above the footway). This is the X1 question (the card's bottom to the footway), and the launderette's door is the first to need it.

## Shared, known (named, not deciding)

- **(a) burnt orange bar in the night glass:** not seen. My own luma of the frames agrees with GLS-04: 0 px at CLOSE_35, 8 px at CLOSE_35_B.
- **(b) hot top corners of night_dark:** not in this view's frames. The night_dark picture's corners read 5.4 and 4.9.
- **(c) models' glass dropped:** not seen. The wall clock keeps its glass (DSP-07).
- **(e) sheets leaning to the glass:** not seen. The service card and the six price cards stand upright (DSP-05: 0 over 3 degrees).
- **(f) CLOSED at night:** the door's card is not in either close frame. The code turns it only in night_dark.
- **(g) child-size furniture:** this display has no furniture.

## Every legible word at 100 per cent (both close views, day and night)

| word | where | acceptable? |
|---|---|---|
| SERVICE WASHES | the glass | yes |
| SERVICE WASHES / LEAVE IT WITH US | the card on posts | yes |
| HOLME, SOAP FLAKES (twice) | packets | yes |
| for woollens | packet; 200 per cent | yes |
| BRIGHTWELL, WASHING POWDER | packet | **no: real firm (fault 3)** |
| BRIGHTWELL, AUTOMATIC, 3 kg | packet | **no: real firm (fault 3)** |
| MEADOWS, BIOLOGICAL POWDER | packet | yes |
| ASHDOWN, FABRIC SOFTENER, 1 litre | packet | the name yes; "1 litre" on a box, narrow 4 |
| LINDEN, WASHING SODA | packet | yes |
| LINDEN (part, cut by the next bottle) | bleach bottle | yes |
| FERNSIDE, WASHING-UP LIQUID (twice) | bottles | yes |
| TOWELS £3.50, BASKETS £4.25, POWDER 49p, SOAP FLAKES 58p, SERVICE WASH 35p a lb | price cards | yes (placement: narrow 3) |
| BLEACH 42p | price card; soft | yes |

- Not legible at 100 per cent: the room's cork-board cards, the wash-care chart, the parcels' tags and the clock's numerals. All are the project's own words in texts.json.
- No barcode, no modern packaging, no drink, no gambling, no child and no toy.
- The wall clock's URBAN / quartz mark is painted out; I looked at the 1k map at 100 per cent beside the original. Only a speck remains at the hub. The basket's map has no mark.

## Measured

**Parallax, through the game's own `trace` (imported from tools/ue/make_interior_material.py).** I worked out four room points myself: picture pixel to the room point, then a ray from each eye to the card plane.
- Each back-wall point lands 1.3595 m apart on the card between CLOSE_35 and CLOSE_35_B (656.7 card px = 2.0 x 4.5 / 6.62).
- `trace` sends every card point back to its picture pixel exactly, for example (2080.00, 1000.00) from both eyes.
- In the gate's baked day cards, each CLOSE_35 patch is found at the predicted place in the CLOSE_35_B card:
  - the dryer's ring (2900, 700) at offset (0, 0), correlation 0.998;
  - the parcel shelf (1500, 560) at (0, 0), 0.994;
  - the dryer's strip (2496, 1196) at (-1, 0), 0.968;
  - a tile patch at (-5, 0), 0.938, on the tiles' own repeat.
- The card's centre samples u 0.17190 and 0.49491: 1323.1 px apart against PRJ-02's 1322.1 and the target's 1321.93 ± 1.5.

**The glass (mean luma inside the glass, the room mask eroded 4 px):**

| frame | glass | room part | room, reflection off | display part | target floor (room, composite) |
|---|---|---|---|---|---|
| CLOSE_35 day | 73.6 | 52.1 | 48.5 | 139.5 | 33 |
| CLOSE_35 night_lit | 72.8 | 65.9 | 67.7 | 95.2 | 45 |
| CLOSE_35_B day | 81.9 | 56.7 | 48.7 | 146.0 | 33 |
| CLOSE_35_B night_lit | 70.8 | 66.3 | 68.3 | 83.2 | 45 |

- By day the room is readable, and the display is brighter than the room behind it, as in a shop.
- At night_lit the room (about 66) is far brighter than the brick beside the window (17.6 to 19.6). But the target keeps this shop dark at night, so its real night is night_dark, which is the street view's.
- Pure black (luma under 3) in the window's glass (the gate's own glass mask, eroded 4 px): 10 px and 1 px by day. At night_lit there are 1,159 and 1,490 px (0.05 and 0.06 per cent of the glass), in specks of 215 px or less at the frame's edges and the goods' dark edges; there is no patch.
- Burnt (a channel at 250 or more) in the whole frame: CLOSE_35 night 0.0035 and CLOSE_35_B night 0.0071, the same as PIC-05g.
  - The burnt pixels are the yellow and pink towel tops (CLOSE_35_B night 539-764, 917-1035 and 1000-1233, 948-1058) and the white washing (CLOSE_35 night 1320-1467, 1013-1091).
  - No arc, and no band under the head.
- Flat uniform tone: the floor (narrow 1). Smooth plaster and ceiling read as paint, not as a board.

**Export faults of Rita's kind, re-checked:**
- No height map as a normal map: the basket's map has mean (127, 127, 253) and the fascia's (128, 128, 255), blue 160 or more on 100 per cent.
- No textured primitive without TEXCOORD_0 in either glb.
- Shared face planes: one, between two glbs (narrow 2).
- No see-through slot from the close cameras (the front-on-backdrop renders show no white inside the front).
- The stand-in night light is not visible.
- The manifest's five sha256 match the files.

## The builder's named shortfalls

| shortfall (NOTES, check file) | my call |
|---|---|
| FAS-01c 1.88 against 2.0 (the box sign's letters) | not in the close frames; the street view's. On its numbers a narrow point |
| the machines are plain scripted boxes | narrow (point 8) |
| the cloth in the baskets | **FAULT** (fault 2) |
| printed goods by script; CC0 photo pictures owed | narrow (point 7) |
| the shop is dark at night | right by the target, not a shortfall |
| the sign's shadow on the board at night | not in the close frames; the street view's |
| 48 samples | owed (128 on the PC), not counted |

## The check rows: which I trust

- **Trusted, and repeated or confirmed here:** PRJ-01 to PRJ-03 (my `trace` test), GLB-01, FAS-03, PIC-05g, LIT-02b (no void at either close camera), CAM-01, DSP-07, the manifest.
- **Trusted on the files without repeating:** PIC-01 to PIC-06, SO-01 to SO-07, DSP-01, DSP-02, DSP-04 to DSP-06, ROOM-01 to ROOM-05, INV-01 to INV-06, FRN-01 to FRN-12, GLS-01, GLS-02, X-NOISE.
- **Pass, but do not prove what they say:**
  - TRD-01 and DSP-03's silhouette share: a towel stack and a heap pass by area while not reading as towels or washing (faults 1, 2);
  - NEV-01 and NEV-02: a blocklist cannot see a real firm that is not on it (fault 3);
  - FRN-10 and DSP-03's intersection test: each runs inside one glb, so the shared plane between the display and the front is missed (narrow 2);
  - FRN-08 and FRN-10: neither sees the gate's slab in the lobby, which is neither front nor glass;
  - PIC-06: the floor's variation in the picture (11.4) is gone in the composite at 0.15 (narrow 1);
  - the detail text of LIT-08, DSP-03 and DSP-04 still speaks of a lattice, trays, pads and chains (Rita's words; lesson 27).
- **The cloud's stand-ins only:** LIT-01, LIT-02, LIT-05, LIT-07, LIT-08, GLS-03, GLS-04, GLS-05, and the night half of PIC-05g (the gate's glass and spill, not the game's). PRJ-02 proves the gate's bake, not the game (PC-01).
- **Not repeated** (they need renders or the build's scenes): GLS-05, LIT-08's per-piece ratios, DSP-05, SO-07, FRN-07 and the front's own coplanar test.

## What is right

- **The projected room follows the game's rule exactly** (measured above). It reads as a deep, lit launderette from both cameras:
  - four washers under a shelf of brown-paper parcels;
  - three stacks of dryers;
  - a cork board with three pinned cards, a wash-care chart and a clock;
  - tiled dado and cream walls, three tubes.
- The back wall moves against the display between the two cameras. The seam between the bed and the room's floor is hidden by the goods and the dark floor.
- **The far end at CLOSE_35_B is a wall, not a slab.** The right side wall with its chart runs on to the glass (narrow 5 is its finish, not a gap).
- **The wicker baskets** are real scans at real size and read as baskets.
- **The service card** reads as a hand-lettered card on two wooden posts.
- **The cork board** reads as cork in a pine frame with pinned cards (the tea rooms' flat-slab lesson is learnt).
- **The machines** are period front loaders with no display.
- **Nothing is buried or through a shelf** among the display's groups. The goods are at real size and placed with sense: towels left, washing in the middle, powders on a step at the right.
- **Night:** no arc, no burnt band, the frame unlit by the spill; burnt share within the limit.
- **The door hardware stands where the target puts it,** measured in the front glb, since neither close camera frames it:
  - the bell's strip on the top rail, centred 90 mm in from the hinge stile (x -0.893 against the stile's inner edge at -0.803);
  - the letter plate in the bottom rail at z 113;
  - the hours plate top at 1380 under the OPEN card;
  - the 9 on the fanlight.
- From CLOSE_35 the side door, its pilaster, the lining and the shop door's pull show no black strip.

## What I cannot judge from the files

- **The game's glass, light and image:** reflections and the hand-over at 61 degrees, Lumen on the display, exposure, the card under TSR. The room reads a little soft at close range in the gate (the notices cannot be read), and the game may differ.
- **The shop door's foot, glass foot and letter plate as the game will show them:** the gate's slab hides them, and the target has not said what is behind a low-glazed door.
- **The OPEN / CLOSED card, the hours plate, the bell and the 9 in a picture:** neither close camera frames them. I checked them in the glb only.
- **The launderette's real night (night_dark):** the street view's.
- **Wear, grime and wet:** the game's layers.
- **The period prices** (WASH 90p, DRY 20p, SOAP 15p, 35p a lb): not researched.
