FAIL

# The ironmonger (west_north bay 1, no. 16), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer. I did not write the target or build the shop. I judged one view only: CLOSE_35 and CLOSE_35_B, by day and night_lit. I did not read the street view's review.

**Read:** CLAUDE.md; RULINGS.md (1, 2, 3, 8 and 13 October); NOTES.md (the first sections, "For the next nine shops", batch A, the ironmonger's own section and lessons 16 to 27); TARGET.md sections 3, 4.2, 5.8 and 13; Rita's four reviews; `checks/check_ironmonger_v1.json`. I also read the parts of `sw_gate.py`, `sw_ctx.py`, `sw_room.py`, `sw_display_gen.py` and `sw_front.py` named below.

**Looked at:**
- the close previews;
- the four close gate frames (2560 x 1440) at 100 to 500 per cent;
- the three 4096 room pictures;
- both glbs, including their texture maps;
- the clean maps of the twelve display models, against `blanking_report.json`.

**Measured,** with my own scripts in my scratchpad; nothing in the repository or SCRATCH was changed:
- the parallax, through the game's own `trace`;
- each frame pixel's ray, its reflection in the glass, and where it lands;
- the glass luma, the dark patches and the flat patches;
- the joins where the return walls meet the card;
- the normal maps and UVs in both glbs;
- the manifest's sha256 values.

**Missing check renders.** The gate's check renders were removed from `SCRATCH/shop-windows/ironmonger/gate/` while this review was running: the baked cards, the glass masks, the front and pieces masks, and the reflection-off renders. I worked from the eight frames, the glbs, the room pictures and the column PNGs. For the glass I built my own mask: each frame pixel's ray is cast to the glass's panes as the front glb gives them, and the mask is eroded by 6 px. For the room's composite I re-baked the card through `trace`. "Could not repeat" below lists the rows I could not measure again.

Pixel boxes are in the 2560 x 1440 frames unless marked "preview" (the 1600 JPEGs, 0.625 of the frame).

**In short:**
- **By day the window works.** The room behind the display moves exactly as the game's rule says (2 points checked through `trace`). It reads as a deep, stocked, lit ironmonger's. CLOSE_35_B shows no black slab at the far end. The door is as the target asks, except for the missing hours plate. Nothing in the near metre is buried or passes through a support.

**Three faults block:**
1. **At night a burnt orange bar lies across the glass in both close frames.** It is the gate's stand-in street lamp: the pool of light it throws on the far pavement shows in the night glass as a reflection. The builder's note says it is lamp light on the return wall. The ray geometry shows that note is wrong.
2. **The twelve light bulbs in the window have no glass.** The kit drops every glass mesh, so each bulb reads as a wire stalk on a screw cap.
3. **Two makers' marks are still in the display glb,** although the notes say they were painted out: a roundel reading QUALITY / POLYLUFT on the tyre pump, and a stamped maker's word on the trowels' handles.

There are also 9 narrow points. The most visible is the plain, untextured crate, trays and backing board, which repeats Rita's try 1 narrow point 6.

3 faults, 9 narrow points.

## Faults, worst first

### 1. At night the stand-in street lamp's pool burns a bar across the glass (both night frames); NOTES judgement I15 names the wrong cause

**Where:**

- **CLOSE_35 night_lit.**
  - A glowing orange bar runs across the right light at x 1410-1960, y 665-750 (preview 880-1225, 415-470).
  - It carries on at the same height across the right return wall, the window's jamb and the shop door's glass, to about x 2100.
- **CLOSE_35_B night_lit.**
  - The same bar crosses the left light at x 560-1070, y 670-775 (preview 350-670, 420-485).
  - It lies right over the glove shelf, so the gloves and the shelf read orange and burnt.

**Measured** (over the glass pixels in each box):

| frame | what | mean RGB | luma | share burnt (a channel at 250+) |
|---|---|---|---|---|
| CLOSE_35 night | the bar | 168, 113, 40 | 119 | 27 per cent |
| CLOSE_35 night | the glass just above it | | 72 | |
| CLOSE_35_B night | the bar | 171, 134, 81 | 138 | 24 per cent |
| CLOSE_35_B night | the glass just above it | | 62 | |
| CLOSE_35 day | the same box | | 53.8 | |
| CLOSE_35 day | the glass just above it | | 51.7 | |

- By day the same box is within 2 levels of the glass above it: there is no bar by day.
- The bar holds about 40 per cent of the burnt pixels that PIC-05g counts in these two frames (0.0082 and 0.0088, against a limit of 0.01).

**Cause (proved by ray):**
- I cast each band pixel's ray to the outer face of the glass (y_m −0.036) and reflected it.
- **CLOSE_35:** (1600, 700) lands on the far footway at street (42.0, +4.19), 0.96 m from the foot of the gate lamp at x 43. (1500, 690) and (1800, 700) land 2.04 and 1.62 m from it.
- **CLOSE_35_B:** (1000, 700) lands 0.48 m from the foot of the lamp at x 23, and (800, 720) lands 2.03 m from it.
- Pixels above and below the bar land 5.6 to 15.9 m from the lamps, outside their 92-degree cones, which reach about 4.85 m.
- So the bar is the reflection of each stand-in lamp's pool on the far footway and road. The lamps are `lamp_w` 50,000 Blender watts each (`gate_lights.json`).
- The night glass returns 0.2 x Fresnel. That is enough to burn a pool this bright, though not a real sodium pool.
- It is not light falling on the return wall. The bar crosses the return wall, the jamb and the door's glass at one height, and the lamps' cones cannot reach the near footway at all.

**The check misses it.** GLS-03 passes at p95 10.0 and 12.2, because the bar is about 2 per cent of the glass, under any p95.

**Whose:**
- **The kit:** `sw_gate.py`. The stand-in lamps, the far footway and the road are all visible to glossy rays.
- **The builder:** NOTES judgement I15 says the bar is "the street lamps' light coming through the night glass onto the display's right return wall ... not a lamp and not a reflection". That is wrong.
- The brief's condition (g), that the stand-in light must not be visible or burn the frame, fails.

**Exact fix:**
1. In `sw_gate.py`, beside `footway_glossy`, add a switch for the far side of the street: `if (extra or {}).get("street_glossy") is False: for n in ("road", "far_footway"): bpy.data.objects[n].visible_glossy = False`.
2. Write `{"street_glossy": false}` into `SCRATCH/shop-windows/ironmonger/gate_lights_extra.json`. For a quick re-render the existing knob also works: `LEDGER_GATE_NOGLOSSY=road,far_footway`.
3. Re-render CLOSE_35 and CLOSE_35_B night_lit (and night_dark, narrow point 8).
4. The game's own lamps and glass are owed on the PC (PC-02, PC-03).
5. Rewrite NOTES I15: "the bar is the gate lamps' pool on the far footway, reflected in the night glass; struck by taking the road and the far footway out of glossy rays".
6. **New check GLS-04, failing the build:** at night, at every camera, the largest connected patch of window-glass pixels that is 40 or more levels brighter than the reflection-off render is under 0.1 per cent of the glass. A p95 over the whole glass cannot see a band.
7. Expected after the fix: no orange bar, and PIC-05g about 0.005 at the two close night frames.

### 2. The twelve light bulbs in the window have no glass: wire stalks on screw caps (the near metre, both close views)

**Where:**
- **CLOSE_35 day:** the two bulb trays at the front of the bed, x 130-1000, y 1290-1440 (preview 80-625, 805-900).
- **CLOSE_35_B day:** x 655-810, y 985-1045.
- **What shows:**
  - each of the twelve "bulbs" is a ribbed metal screw cap;
  - a bare filament stem and support wire stand about 60 mm up out of it;
  - there is no envelope, highlight or reflection.
- At 100 per cent they read as pins or wire stakes in a tray, not as bulbs. They are among the goods nearest the eye in CLOSE_35.

**Cause:**
- `sw_room.GRoom.template` (which the display uses too) drops every mesh, or every face, whose material is glassy or BLENDED. Its docstring says: "glass meshes left out as the recipe did".
- Poly Haven's `lightbulb_01` has two materials: `lightbulb_01_glass` (transmission, alphaMode BLEND) and `lightbulb_01_base`. The envelope is the glass.
- In `ironmonger_display.glb` all 12 bulb nodes carry only `lightbulb_01_base` (read from the glb's JSON).
- The 12 bulbs on the room's shelf are cut the same way (seen at 200 per cent in CLOSE_35_B day, x 1840-2560, y 240-600).
- DSP-02 ("no alpha cut-out or blend") passes because the glass is gone. DSP-03's silhouette share was measured on the glassless bulbs.
- **A second fault with the same piece:** the cap is an Edison screw. A British ironmonger of 1990 sold bayonet-cap bulbs (B22). The NOTES itself says "a bayonet bulb is 0.105" and then places the screw-cap model. This is lesson 12's foreign fitting again.

**Whose:**
- **The kit:** the template rule.
- **The builder:** did not look at the bulbs at 100 per cent.

**Exact fix:**
1. **Keep the bulb's glass.** In `GRoom.template`, keep the glass mesh for models in a new `KEEP_GLASS` list, starting with `lightbulb_01`. Give it a Principled BSDF with base colour (1, 1, 1), roughness 0.05, IOR 1.5, Transmission Weight 1.0 and Alpha 1.0. There is no blend, so DSP-02 still holds.
2. **In the room's picture,** use `GRoom.mat(glass=True)`'s shadow-ray trick (lesson 19).
3. **Look at the glass's own map** at 100 per cent before use: "Lumen" was blanked on this model.
4. **Mend the cap.** Cut the screw thread and script a B22 cap: a plain 22 mm x 18 mm brass sleeve, two 2 mm pins at 180 degrees, and two solder contacts on the foot.
5. **New check DSP-05, failing the build:** every placed model keeps all the meshes of its glTF, unless a Judgement in NOTES names the one it drops. The row lists each model's mesh count against its source.

### 3. Two makers' marks left in the display glb (content rule; NOTES and INV-05 / INV-06 say they are gone)

**Where:**

**(a) The tyre pump's roundel.**
- It is a ring reading QUALITY / POLYLUFT round a three-pointed emblem.
- **In the frames:** CLOSE_35_B day x 2315-2335, y 1060-1082 (a 20 px roundel), and CLOSE_35 day x 1843-1856, y 810-823.
- **In the glb's 512 px map:** x 285-315, y 450-475.
- **In `tire_pump_diff_1k_clean.jpg`:** box [570, 893, 624, 957].
- The blanking box [570, 520, 664, 880] stops 13 px above it.
- NOTES lists "POLYLUFT (rotated), the roundel logo, the orange label" as painted out. The rotated word is gone; the roundel is not.

**(b) The trowels' handle stamp.**
- It is a stamped word (mirrored, "YOS…") on the wooden handle.
- **In `trowel_01_diff_1k_clean.jpg`:** box [838, 795, 922, 828].
- **In the glb's map:** x 419-461, y 397-414.
- The blanking box [672, 585, 752, 625] painted out a different mark, on the blade.
- It is on the four display trowels and on the eight on the room's right board.

**How visible:**
- Neither mark's words are legible at 100 per cent in the four frames.
- The pump's emblem does read as a logo badge.
- The near metre is real geometry, so a player can stand closer than 1.5 m.
- The content rule (no maker's name or mark on any good) has no size limit.

**Whose:** the builder (step 0's blanking). INV-06 tests only the listed boxes.

**Exact fix:**
1. Paint out the two boxes as the other boxes were done: the ring colour, carrying the map's own grain. Do the same in each model's normal-map companion.
2. Re-export `ironmonger_display.glb`.
3. Look at the eight trowels on the room's right board in `ironmonger_day.png` at 100 per cent. Re-render the room only if the stamp shows.
4. **INV-06 adds a second pass:** a contact sheet of every clean map at 1k with the boxes drawn, looked at by someone other than the builder (the way this review found both marks).

## Narrow points, most visible first (each with its exact fix)

### 1. The display's supports are flat-colour boxes and boards (Rita's try 1 narrow 6, repeated)

**What and where:**
- **The crate.** It is the largest flat patch in any close frame: CLOSE_35_B day x 1400-1981, y 989-1257, 85,931 px with a local standard deviation under 1.5 levels, at luma 115.
- **The backing board** ("the white board"). CLOSE_35 day x 60-880, y 740-1360; CLOSE_35_B day x 1000-1060, y 700-960, with high-pass sd 1.2.
- **The two trowel trays, the two bulb trays and the hung shelf.**
- Every one of these is a base-colour factor with no texture in the glb (`crate_wood`, `backing_board`, `bulb_tray`, `hung_card`). The crate reads as a cardboard box, and the board as a grey CG panel.
- **The return walls** are a single tone along their depth: sd 1.4 to 1.7 over 110-180 x 260-310 px. At CLOSE_35 the right one is a pale, even panel (x 1790-1987, y 288-574, luma 88).

**Fix:**
- **The crate, the trays and the hung shelf:** the room's own floor maps (Poly Haven `old_wooden_floor_03`, CC0, already in the build) on a 0.5 m tile, tinted to the deal colour (150, 113, 72), with a 3 mm bevel on every edge.
- **The backing board:** the room's `pegboard.png` (tan hardboard, 25 mm holes, 0.6 m tile). This is the trade's own fixture.
- **The return walls:** multiply their emission by the room's plaster map (Poly Haven `painted_plaster_wall`, already fetched) at the room's own tile, ±8 per cent.
- **Check:** no display support may carry a flat base-colour factor; each must have a texture.

### 2. The hung glove shelf hides the top of the pyramid, and its four cords end in mid-air

**Where:**
- **The shelf hides the pyramid's top.**
  - In `display_items.json` the shelf's underside is at w 0.62 and the pyramid's top at w 0.686. The shelf stands in front of the pyramid, at v 0.06-0.38 against the pyramid's v 0.40-0.50.
  - In CLOSE_35 day, the top two rows are under the shelf (x 440-600, y 850-910), and the top tin peeks up between the gloves (x 520-560, y 755-775).
- **The cords end in mid-air.**
  - They stop at w 1.75 (z 2.35 above the footway): 50 mm below the transom, and 0.07 to 0.37 m behind the glass, where there is nothing to hang from.
  - In CLOSE_35_B day their tops are seen ending against the room's wall, at (575, 175), (710, 215), (855, 110) and (980, 160).
- The code's own comment says "Nothing floats: a hung card hangs on four cords from the window head".

**Fix:**
- Lift the shelf so its underside is at w 0.76. That clears the sight line to the apex from both CLOSE_35 (w 0.742 at the shelf's front edge) and STREET_SQUARE.
- Hang it from a 12 mm black iron rod fixed to the back of the transom: v 0.04, w 1.79 to 1.80, u 0.18 to 1.00. The rear pair of cords slants forward to the rod.
- **New row:** every cord, wire or chain ends within 2 mm of a solid part.

### 3. Through the shop door's glass: a flat grey slab where the shop should be

**Where:** CLOSE_35 day, both panes of the shop door, x 2060-2200, y 440-880 (preview 1288-1375, 275-550).
- **By day:** 73 by day in the lower pane (77, 78, 77) and 59 in the upper.
- **At night:** 14 to 22.
- **What the rule would show there** (the card through `trace`): the room's right wall, its dado at luma 24 to 27 and its plaster at 90.

**Cause:** the rays meet `hall_wall_l`'s outer face 0.5 m behind the door. That face is `hall_plaster` (150, 142, 124), the side hall's material, not the shop's.

**Fix:** the face of `hall_wall_l` that looks into the shop takes the shop's finishes.
- **In the glb:** plaster (204, 206, 180) above footway z 1.55, and the dado (30, 62, 44) below.
- **In the gate:** the room picture's right-wall front column as emission, as the return walls take it.

### 4. White goods burn at night (the night test state)

**Where:**
- **The broom handles:** CLOSE_35 night x 1700-1880, y 590-960 (pure white, counted there inside fault 1's burnt patch); CLOSE_35_B night x 2233-2560, y 650-974 (about 5,400 px at 250 or more).
- **The hung shelf's top:** CLOSE_35 night x 31-883, y 816-965, 10,932 px.

**Fix:** as Rita's T16 did, before the spill is tuned:
- tone the `plastic_broom` handle's white to 0.80 of its map;
- set the hung shelf to (140, 120, 90), or give it narrow point 1's plank map.

### 5. The four cleaner tins are blank red cylinders

**Where:** CLOSE_35 day x 1405-1520, y 835-915; CLOSE_35_B day x 1416-1664, y 880-984. They are glossy red with pink lids and no label. They read as placeholders beside the labelled paint tins.

**Fix:** a label band from the project's own tin atlas (`sw_gen`, makers COLDWELL / HARTSIDE / ELMSTEAD / BRANTHAM), for example "HARTSIDE SCOURING POWDER", in the atlas's print. The target allows "blanked or the atlas's"; the atlas reads as stock.

### 6. Two price cards read wrong

**TORCH £8.50**
- **Where:** CLOSE_35_B day x 1935-2005, y 1350-1405, beside the brass blowtorch.
- To a British eye "TORCH" alone is a flashlight.
- **Fix:** make it BLOWLAMP £8.50.

**TINS 99p**
- **Where:** CLOSE_35 day x 720-785, y 1310-1365. It stands in front of the first trowel tray, at u 0.80.
- It gives a second price for the pyramid, which already has PAINT £2.99.
- **Fix:** delete it, leaving 11 cards.

### 7. No hours plate on the shop door

The brief's list for the door includes an hours plate. Rita's door has one (4.1 row 24). Target 5.8 gives the ironmonger's hours (Shops Act Judgement), but 4.1 made a plate only for Rita.

**Whose:** the target.

**Fix:**
- A 4.1 row for the ironmonger reading "MON-SAT 8.30-5.30 | WED 8.30-1 | SUN CLOSED".
- Gilt, at Rita's size (443 x 186 mm), on the shop door's lower pane at Rita's place: z base 1040 plus the baseline, d 39.
- GLS-01 and GLS-02 extended to it.

### 8. The dark shop's own night is not shown at close range

The target's review cameras at night are night_dark for a dark shop. The builder rendered night_dark only at STREET_SQUARE (I11).

**Measured instead:** the night_dark card through `trace`, over my glass mask, reads 11.0 at CLOSE_35 and 12.6 at CLOSE_35_B. That is just inside LIT-01's 10 to 35, with 16 to 22 per cent of the glass under 5.

**Fix:**
- Render CLOSE_35 and CLOSE_35_B night_dark, with the spill off and fault 1's fix applied, and add both to the preview set.
- LIT-01 also runs at the two close cameras.

### 9. MANIFEST-ironmonger.json carries Rita's description

Its `what` reads "the files of the narrow-points build (13 Oct, from the try 2 reviews; v3) ... rebuilt by build_ritas.py". The five sha256 values do match the files on disk.

**Fix:** "the ironmonger's batch A build of 13 October; the two glbs and three 4096 pictures are out of git, rebuilt by `build_shop.py --shop ironmonger`".

## The builder's named shortfalls, judged from the close view

| shortfall (NOTES, check file) | judged | why |
|---|---|---|
| The window is crowded: toolboxes and watering cans at 0.85, brooms at 0.80, bulbs at 1.25, the sprinkler in front of the second toolbox | narrow; accept as built | At 1.5 m the toolboxes and cans read at a believable size. The right end is not too full: the brooms, the pump and the hammer stand apart. DSP-04's longest bare run is 0.04 m. |
| No step ladder; 2 of 3 paraffin cans; tiers 0.4 and 0.8 not built; 1 of 3 watering cans in the room | narrow; accept | Nothing missing is seen from either close camera. The counter and the floor run hide the low tiers. |
| Pegboards with 44 and 36 tools, 37 per cent by bounding box | narrow; accept | From CLOSE_35 the left board reads as rows of hand tools (x 60-330, y 130-700). The right board reads as gloves, trowels, dustpans and traps (x 1490-1780, y 360-640). |
| Dark at night; the night_lit frames are the tests' state; night_dark only at STREET_SQUARE | narrow | Narrow point 8. |
| LIT-08: the blowtorch 0.47 and the pump 0.51 at CLOSE_35_B night | narrow; accept as the taste call it is | It is the test state, not the shop's own night. By eye the blowtorch reads as brass with highlights and the pump as a clean silhouette. I could not repeat the row (pieces masks removed). |
| LIT-02b: 1.02 per cent at CLOSE_35_B by day | narrow; accept | There is no void. The builder's largest patch is 0.31 per cent. My room-only composite through `trace` gives a share of 1.51 per cent and a largest patch of 0.38 per cent, made of dado shade. |
| FRN-10: the side door's top corner in the hood's shade | narrow; accept for this view | At close range the darkest cluster in CLOSE_35 day (x 2372-2419, y 420-464, 855 px) is the black door's top in the drip's shadow, not a strip. Neither close day frame has a long thin dark run. |
| 64 samples | owed | 128 samples on the PC. |
| The hanging board's iron and sway | not this view | Only its corner is in CLOSE_35 (KEYS CUT, cut at "K" and "C"). |
| I13: the bulb's glow set to zero | right | `lightbulb_01_base` carries an emissive map but no `emissiveFactor`, so it is 0. Nothing glows. |
| I15: the orange band is lamp light on the return wall | **wrong** | Fault 1. |

## The check rows: which I trust

**Trust: the game's assets and rule, repeated here or agreeing with what I measured.**
- **PRJ-01, PRJ-02, PRJ-03.** I repeated PRJ-02: the card's centre samples u 0.82820 and 0.50541, −1322.1 px. The parallax is checked under "Measured".
- **PIC-01 to PIC-06, X-NOISE.**
- **SO-01 to SO-07.**
- **ROOM-02 to ROOM-05.**
- **FRN-01 to FRN-05, FRN-07, FRN-09.**
- **FAS-01, FAS-01n, FAS-01c, FAS-02, FAS-03.** I repeated FAS-03: no textured primitive without TEXCOORD_0 in either glb.
- **GLB-01.** I repeated it: 13 normal maps in the display glb and 1 in the front, all real RGB maps. The lowest is the glove's: blue mean 211, 0.90 at 160 or more.
- **DSP-01, DSP-04, CAM-01.** The camera files agree.
- **LIT-06.**
- **The manifest.** The sha256 values match.

**Trust with a gap.**
- **DSP-02:** it holds only because the bulbs' glass was deleted (fault 2).
- **DSP-03:** its intersection test is fine (I checked the key pieces' boxes in `display_items.json`), but its silhouettes are of glassless bulbs.
- **INV-05 and INV-06:** they pass while two marks survive outside the boxes (fault 3).
- **NEV-02:** by eye; I agree, apart from the period questions below.

**Stand-ins only: the gate's light and glass, owed on the PC.**
- **LIT-02.** My composite at CLOSE_35 is 43.0 by day and 67.3 at night; the row says 47.4 and 67.3. Both are above the floors of 33 and 45.
- **LIT-05, LIT-07, LIT-08.**
- **GLS-03:** blind to a narrow burnt band.
- **PIC-05g:** passes at 0.0082 and 0.0088, about 40 per cent of it fault 1's band.
- **LIT-02b.**

**Could not repeat** (their renders were removed): FRN-10's pixel half, FRN-08, LIT-02b's own numbers, LIT-08, GLS-03, DSP-03's silhouette shares, and TRD-01.

## Measured

**The parallax, through the game's `trace`.** I solved for the card point that `trace` sends to a given picture pixel, from each camera, and then compared a 28 x 28 frame patch with the rule's own patch.

| picture point | CLOSE_35: card x | CLOSE_35_B: card x | shift on the card | frame pixel (CLOSE_35 / CLOSE_35_B) | frame against the rule |
|---|---|---|---|---|---|
| the till, (2395, 900) | 1.5394 m | 2.8989 m | 1.3595 m (656.7 card px) | (1113.7, 529.0) / (2187.8, 512.9) | offset (0, 0); correlation 0.81 / 0.85 |
| a drawer on the drawer wall, (1101, 768) | | | the same shift | | offset (0, 0); correlation 0.81 / 0.79 |

- The rule for a back-wall point is 2.0 x 4.5 / (2.12 + 4.5) = 1.3595 m.
- `trace` sends both card points back to (2395.00, 900.00).
- The day glass's reflection lowers the correlation; it does not move the patch.
- The back wall, the drawer wall and the side boards shift between the two frames as the rule says.

**The glass** (mean luma over my glass mask):

| frame | the frame itself | the room alone through `trace` (the target's floor) |
|---|---|---|
| CLOSE_35 day | 67.8 | 43.0 (33) |
| CLOSE_35_B day | 65.9 | 48.3 (33) |
| CLOSE_35 night_lit | 69.3 | 67.3 (45) |
| CLOSE_35_B night_lit | 74.9 | 77.7 (45) |

- The brick wall beside the window is 88 by day and 20 to 22 at night.
- So in the test state the lit glass is 3.4 times the wall at night. By day the room is readable and the glass is darker than the brick, as a shop window is.
- The shop is dark at night by the target. The night_dark composite is 11.0 and 12.6 (narrow point 8).

**Dark and flat regions over the glass:**
- **Under luma 12:**
  - By day: 0.06 and 0.08 per cent, largest patch 0.04 per cent.
  - At night: 4.0 and 1.8 per cent. These are the bed's front in shade and the window jamb's inner face, which is off the spill's channel. The largest patch is 0.50 per cent. There is no void.
- **Flat (local sd under 1.5 over 33 px):** the crate's front (86k px), the right return wall (38k px), the backing board, and the room's ceiling at night (narrow point 1).

**The joins between the return walls and the card:**
- **CLOSE_35_B, left wall:** the step is 0.1 to 4.4 levels at z 1.8 to 2.0, by day and by night. The join is not visible.
- **CLOSE_35, right wall:** 13 to 48 levels. That step is the edge of the room's right pegboard against the plaster, not a break in the wall (narrow point 1 covers its flat tone).
- The bed's back edge hides the 0.05 m between the bed (w 0) and the card's floor, so there is no gap.

**Every legible word at 100 per cent, both close views.** All are the project's own and acceptable unless marked. No word in either close view is a real firm's.

| what | the words |
|---|---|
| Price cards (hand-lettered) | PAINT £2.99, TINS 99p (narrow point 6), TROWELS £2.45, TOOL BOXES £6.95, OIL £1.15, CANS £3.95, SPRINKLER £3.75 (cut), BROOMS £2.25, TORCH £8.50 (narrow point 6), PUMP £4.50 and BULBS 40p (soft), GLOVES £1.30 (soft) |
| Paint tins (the project's own makers) | COLDWELL, EMULSION, MAGNOLIA, BRILLIANT WHITE; HARTSIDE, WHITE SPIRIT, METAL PRIMER; ELMSTEAD, WOOD PRESERVER, WOOD STAIN, DARK OAK; BRANTHAM, GLOSS PAINT, BLACK, WHITE |
| The door | OPEN by day, CLOSED at night (the 4.2 sign); 16 in gilt on the fanlight |
| The fascia's edge | "…IN" (from PARAFFIN) |
| The hanging board | "K" and "C" (KEYS CUT) |
| Not legible at 100 or 200 per cent | the drawer labels, the room's tin labels, the till's readout |

The two marks of fault 3 are not legible at 100 per cent.

**Rita's export faults:**

| fault | here |
|---|---|
| A height map exported as a normal map | none (GLB-01, repeated) |
| A textured primitive without UVs | none |
| Two parts in one face plane, giving a black strip | none seen at close: no long thin cluster under luma 8 in either close day frame |
| A see-through slot from an angle | none seen: no backdrop or sky inside the front at either close camera. I could not re-run FRN-08 itself. |
| The stand-in night light visible | the spill is invisible and the frame is not burnt, but the stand-in lamps are visible by reflection (fault 1) |

## What is right

**The room is the game's rule, pixel for pixel, and reads as a deep, lit, full ironmonger's.**
- The drawer wall has 60 drawers with brass label holders.
- The shelf unit has tins, oils and oil cans.
- The counter has the till, the measuring tape and the two toolboxes.
- The pegboards hold tools in rows, gloves, trowels and traps.
- The floor run has the bin, the cans and the cement bags.
- It moves true between the two cameras.
- From CLOSE_35_B the far end of the window is the left return wall, plaster over the green dado. It meets the card with no step and no black slab.

**The near metre, by day, reads as an ironmonger's window of the period.**
- the 36-tin pyramid of the project's own paints;
- weathered oil tins on a stepped crate;
- a brass blowlamp;
- galvanised watering cans;
- two green toolboxes;
- trowels raised on trays so the sill does not hide them;
- the pump, the sledgehammer and brooms against the end wall;
- hand-lettered price cards.

The Poly Haven scans (oil tins, toolboxes, cans, blowlamp, trowels) read as real, worn objects. Nothing is buried in a stand or passes through a support or a shelf (I checked the key pieces' boxes in `display_items.json`).

**Lit and shaded as a shop.** By day the sky lights the bed through the glass, and the goods fall off front to back. At night (the test state) there is no spill arc, no burnt head band, and dark mullions.

**The door matches the target:**
- the T1 leaf, with glass from 871 and the bar at 1423;
- the brass letter plate in the lock rail;
- the brass lever on the viewer's right stile;
- the brass kick plate;
- the green OPEN card by day and the red CLOSED card at night;
- the gilt 16 on the fanlight;
- the band above both doors;
- the black side door under its drip, with its knob and plate.

There are no black strips at the jambs. The bell is built where the target puts it: model x 0.958, on the top rail 90 mm from the hanging stile.

**The glass reads as glass by day.** The opposite houses and trees are reflected, the room shows through, and the night glass shows no double images.

**The content rule otherwise holds.** There is no drink, gambling, child or toy, no barcode and no modern packaging. The paraffin and the white spirit are fuel and solvent, not drink.

**Both glbs are clean exports.**

## What I cannot judge from the files

- **The game's own light and glass:** Lumen on the display, the glass's reflections and Fresnel at 61 degrees, the exposure, and the card under TSR (PC-01 to PC-07). The orange bar of fault 1 is the gate's. Whether the game's real lamps leave any glint is for the PC.
- **The removed check renders:** the rows listed under "Could not repeat".
- **The bell:** from CLOSE_35 the ray to it meets the window's jamb (it crosses the door plane at x 0.61, left of the glass at 0.86), and CLOSE_35_B does not frame the door. Its swing and sound are not in the files.
- **The period look of three goods** that read more 2010s than 1990 to my eye, but which I cannot date without a photograph:
  - the knit gloves with a grey dipped palm;
  - the sledgehammer's yellow fibreglass handle;
  - the slim track pump.

  No dated photograph of a 1985 to 1992 ironmonger's window was reached. That photograph, not my memory, should decide them. The room's own `wooden_broom` is the period choice if the display's three plastic brooms are found wrong.
- **Wear, grime and wet,** which come from the game's layers (D53).
- **Anything of the street view,** including the fascia's blue flakes seen at the frame's top right.
