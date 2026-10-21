PASS

# The newsagent and tobacconist, the CLOSE view: fresh review, try 2 (cloud week 42, unit 7 part 2, stage 2; 15 October 2026)

Reviewer: a fresh reviewer who did not write the target, build the shop or write the try 1 review. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit (the shop is lit at night; its night_dark frame is the kit's extra view and was only looked at for burns). I did not read the street view's reviews. Two things reached me by accident before this file was written, and I name them so they can be weighed: the subject line of commit 691d8d9 (it says the street review found two carton names that echo lagers), and two lines of the street try 2 review that a search of the folder printed (they say NOTES had no newsagent try 2 section at 04:11). I read nothing else of either. Every finding below is my own measurement.

**Read:** CLAUDE.md; RULINGS.md (1, 2, 3, 8 Oct); NOTES.md ("For the next nine shops", the newsagent's batch A section, "Try 2 shared fixes", "Try 2, newsagent", which the builder added at 04:26 while I worked); TARGET.md sections 3, 5.9 and 13 (A7 to A9, T2-1 to T2-16); Rita's four reviews; my predecessor's REVIEW-newsagent-v1-close.md; `checks/check_newsagent_v2.json` (77 of 78, FLT-02 failing, a street row); MANIFEST-newsagent.json; DECISIONS.md lines 601 to 614.

**Looked at:**
- the three v2 close previews and the three v2 room previews;
- the five close gate frames (2560 x 1440, rendered 03:11 to 03:32 on 15 Oct) at 100 to 400 per cent;
- the check renders beside them (glass mask, room mask, reflection-off frames, pieces pass);
- the room picture (4096) at 100 to 400 per cent;
- the display's texture atlases;
- the display glb, imported in Blender (bpy 5.2.2) from a copy taken at 04:28.

Nothing in the repository or in the scratch folders was changed. My work files are in the session scratchpad (`nc2/`).

**In short.** Both faults of try 1 are fixed, and fixed properly:

- **The magazine board** leans back. All twelve covers lie on its front face and show. The papers lean back onto their risers.
- **Every printed good** is a photograph with real type: halftone papers with body columns, magazine covers with cover lines, photographic cards and postcards. The jars are glass with sweets inside.

The near metre now reads as a 1990 newsagent's window at 100 per cent. The room still obeys the game's rule pixel for pixel. The night burn, the orange lamp bar and the till's glyph are gone.

**0 faults, 8 narrow points.** The worst:

1. the postcard rack shows the same three cards on all three tiers;
2. two carton names legible in these frames echo lagers (already renamed in the code after the render, but not yet in any picture);
3. the cartons' "200 CIGARETTES" line is ghosted and cut by the top edge, and their ends are flat dark grey.

By Jafar's ruling of 9 October, a piece failing only on narrow points passes, with the points listed for the builder.

## Try 1, item by item

| try 1 item | now | where, and the measurement |
|---|---|---|
| **Fault 1:** the magazine board leaned toward the glass, a third of the covers were hidden behind it, two rows hung under it, and the papers leaned forward | **FIXED** | See the fault 1 notes below the table. |
| **Fault 2:** the printed goods were clip-art placeholders and the jars were painted plastic | **FIXED** | See the fault 2 notes below the table. |
| **Narrow 1:** two headlines lost their last word | **FIXED** | RAIN FORECAST FOR THE WEEKEND (CLOSE_35 day 40-225, 1085-1170) and NEW LIBRARY OPENS ON FRIDAY (CLOSE_35 day 880-975, 1140-1200) are whole. PRT-04 agrees. |
| **Narrow 2:** MERIDIAN MORNING STAR | **FIXED** | MERIDIAN MORNING GAZETTE (CLOSE_35 day 650-865, 1140-1170). "morning star" is in the blocklist. |
| **Narrow 3:** the cartons read as big packets | **FIXED** | 280 x 90 x 50 mm (glb), "200 CIGARETTES", and the 1990 band (MIDDLE TAR As defined by H.M. Government / DANGER: Government Health WARNING: CIGARETTES CAN SERIOUSLY DAMAGE YOUR HEALTH), legible at 160 per cent. They stand on their long edge (the 280 x 90 face to the street), not flat as I wrote; that reads right. Two print defects are new (narrow 3 below). |
| **Narrow 4:** the pads burnt at night | **FIXED** | See the narrow 4 notes below the table. |
| **Narrow 5:** cards on a wire ring with no pockets | **FIXED** | A chrome U pocket for each card, three deep, 6 mm apart, each card behind showing its top (CLOSE_35_B day 2290-2560, 430-1230). |
| **Narrow 6:** the checks could not see fault 1, and the records carried Rita's words | **FIXED** | DSP-05 is extended (0 float, 0 forward, 20 back-leaning sheets with their tops within 5 mm) and DSP-13 is added. DSP-03's wording and MANIFEST's "what" are this shop's. One new record point: narrow 6. |
| **Narrow 7:** the till's "Y" glyph | **FIXED** | At 400 per cent the readout shows "0 2 1 3.7 7 0" and only a faint smudge where the glyph was (room picture 1835-1860, 840-855). The readout's glass is now kept (DSP-07). |
| **Narrow 8:** 48 samples, not 128 | **PARTLY** | The room pictures are at 64 (PIC-01). Still owed on the PC (narrow 8). |
| **Narrow 9:** the curl and fold missing from NOTES and A9 | **FIXED** | T2-7 in TARGET.md, and the try 2 table in NOTES. |
| **Shared (a):** the lamp pool's orange bar in the night glass | **FIXED** | The try 1 bar's boxes (CLOSE_35 night_lit 1494-1898, 670-750; CLOSE_35_B night_lit 699-1021, 674-725) now read a mean of (81, 75, 66) and (83, 71, 66), with 0 px at red 250. GLS-04: 0.0003 per cent. |
| **Shared (c):** the glass of the till and the clock was dropped | **FIXED** | DSP-07: the glass is kept, 1 part each. |

**Fault 1 (the magazine board and the papers), measured on the vertices:**

- The board's foot is at the front (v 0.233, w 0) and its top at the back (v 0.55, w 0.466): it leans 35 degrees back.
- All 12 covers lean back 35.0 degrees, 2 mm off the board's face, in three rows (feet at w 0.027, 0.139 and 0.251).
- All 8 papers lean back 18.6 to 19.6 degrees. Their tops touch the riser (v 0.236 against 0.24) or the back board (0.366 to 0.369 against 0.37). Their feet rest on the 55 mm step and the 240 mm step, within 2 mm.
- In the frames, all 12 covers show:
  - CLOSE_35 day (1050-1510, 830-1140): THE WALKER, COUNTRY DIARY, PHOTO MONTHLY, COAST & SEA, FARMHOUSE COOKING, MOTOR WORLD, YACHT AND DINGHY, COTTAGE HOMES, GARDEN LOG, THE GARDENER'S YEAR, THE ANGLER'S WEEK, QUAYSIDE MODELLER;
  - the board's top edge is about 14 mm above the top row (DSP-13 reads 14.4).
- The pocket under the board at night is gone. CLOSE_35 night_lit's largest patch under luma 8 in the glass is now 892 px: the room's cover-board edge at (121-153, 426-684), not the board. CLOSE_35_B's is 2,409 px: the counter's end in shade at (1394-1412, 589-763).
- LIT-08 for the covers is 0.92 (it was 0.54).

**Fault 2 (the printed goods and the jars):**

- **Papers:** 0.281 x 0.193 m, bent sheets (404 triangles each). Each has a masthead, the date line "WEDNESDAY 17 OCTOBER 1990" (a Wednesday, as it should be), "PRICE 25p", a halftone photograph, a sub-deck, column heads and body type (CLOSE_35 day 0-1100, 1000-1440).
- **Covers:** each is a photograph with a masthead, cover lines and a date and price corner. There is no barcode.
- **Photographs:** PRT-01 counts 43 distinct photographs over 54 goods.
- **Cards** (CLOSE_35_B day 2290-2560, 430-1230): photographs with gilt and red greetings.
- **Postcards:** their captions now name their photographs (atlas read: THE JETTY is a jetty, A WATERFALL IN THE WOOD a waterfall).
- **Jars:** six glass shells, 116 mm across and 232 mm high with the lid, with the contents inside, screw lids and paper labels (CLOSE_35_B day 1740-2200, 1090-1440). The room's ten jars are glass too.

**Narrow 4 (the pads at night):**

- The yellow pad now reads (233, 203, 102), with a top value of 249. The A4 stack reads luma 215.
- PIC-05g: CLOSE_35 night_lit 0.0009 and CLOSE_35_B night_lit 0.0023 (try 1: 0.0070 and 0.0088).
- I measured the per-piece rule I asked for, from the pieces pass. The worst piece has 17.2 per cent of its pixels at 250 (CLOSE_35 night), so the rule would pass, but the row was not added (narrow 7).

The builder's try 2 notes claim nothing of try 1 was wrong. It followed every exact fix, and where it changed one I measured the result:

- the board at 35 degrees, not 40;
- the cartons on edge;
- the papers side by side, not overlapping.

## Faults

None.

## Narrow points, worst first, each with its exact fix

### 1. The postcard rack shows the same three cards on every tier (new)

- **Where:**
  - CLOSE_35 day, the rack at (1460-1610, 440-830): each of the three tiers shows, left to right, the hillside with a bench, the boardwalk and the river town. It is the same picture three times in a column.
  - CLOSE_35_B day (1640-1880, 370-940): each tier shows the boardwalk, the harbour and the misty hill, again in the same order.
  - At 100 per cent the column of identical boardwalks is the first thing the eye catches in the right-hand light. It is lesson 9, "no regular grid of the same thing".
- **Cause:** `postcard_rack` holds 72 cards (3 tiers x 8 pockets x 3 deep) from 12 designs, laid out the same way on each tier with the tiers' pockets lined up. PRT-01 tests distinct pictures within a kind, not their placement.
- **Whose:** the builder.
- **Exact fix:**
  1. The front card of pocket p on tier t is design (8t + p) mod 12. The two cards behind it are (8t + p + 4) mod 12 and (8t + p + 8) mod 12.
  2. Turn tier t by t x 22.5 degrees about the pole, so that the pockets do not stand in columns.
  3. Add to PRT-01: within one rack, no two front cards whose faces point within 30 degrees of each other carry the same design.

### 2. KESTRELL and CASTLEMERE, legible on the cartons in these frames

- **Where:**
  - CLOSE_35 day: KESTRELL at (255-425, 848-885), CASTLEMERE at (505-690, 828-862).
  - CLOSE_35_B day: KESTRELL at (788-845, 722-742).
  - Both are plain at 100 per cent.
- They are one letter from Kestrel lager, and seven letters shared with Castlemaine XXXX, both sold across Britain in 1990.
- They are not the real names and they sit on tobacco, so this is not a fault. But a player who knows the lagers reads them, and the content rule keeps drink out.
- The builder renamed them WYNYARD and RAVENSDALE at 04:28 (DECISIONS.md, 15 Oct; `sw_gen.py` lines 504 and 507; `display_items.json`) and put "kestrel" and "castlemaine" in the blocklist. That was after these frames were rendered, so no picture yet shows the new names and no check has run on them.
- The room's gantry packs still carry the old names (`rooms/texts.json`). They are illegible from both close cameras.
- SELWYN NAVY CUT I accept: "navy cut" is a cut of tobacco that many makers printed.
- **Whose:** the builder.
- **Exact fix:**
  1. Render the four close frames, and the street ones, again with the renamed display. Re-run INV-05, NEV-01 and the check.
  2. Rename the gantry's packs at the next room render (the PC's, at 128 samples).

### 3. The cartons' print: the "200 CIGARETTES" line is a pale ghost cut by the top edge, and the cartons' tops and ends are flat dark grey (new)

- **Where:**
  - Every carton's top strip, CLOSE_35 day (190-720, 755-985) at 160 per cent. "200 CIGARETTES" and "25 x 8" are printed pale on pale (cream on cream, grey on grey). The upper half of the letters is cut off by the carton's top edge, so each carton seems to carry a half-erased line.
  - The atlas shows the cause: `display_work/tex/cartons.png`, each 560 x 180 tile's top 10 px.
  - CLOSE_35_B day: the right stack's end at (962-976, 690-800) is a flat (50, 50, 49), against (146, 159, 177) on its own front band. The tops are the same dark grey. A carton's ends and top carry its colours and name; a dark grey end reads as a black box.
- **Whose:** the builder (`sw_gen.py` carton atlas; the carton mesh's UVs).
- **Exact fix:**
  1. Set the "200 CIGARETTES" and "25 x 8" line 4 mm (8 px) below the tile's top edge, with a 3.5 mm cap height. Ink it in the band's contrast colour: navy (24, 70, 120) on a cream ground, cream (236, 236, 232) on navy or red.
  2. Give the top (280 x 50) and the two ends (90 x 50) their own atlas tiles in the carton's ground colour, with the band's stripes and the brand name: along the top, and turned 90 degrees on each end.

### 4. The jars' contents: the humbugs read as an op-art zigzag and the mint imperials as grey pebbles (new)

- **Where:**
  - CLOSE_35_B day: HUMBUGS at (1763-1855, 1146-1331), black-and-white zigzag stripes wrapped on a cylinder.
  - MINT IMPERIALS at (2001-2101, 1192-1408): blue-grey cells with dark joints, like crazy paving.
  - The pear drops, sherbet lemons, toffees and fruit drops read as sweets.
- **Cause:** one cell texture (`sweets.png`) on a lathe at 0.94 of the radius, as my try 1 fix asked. Two of its six tiles do not look like their sweet.
- **Whose:** the builder.
- **Exact fix (in the window's six jars and the room's ten):**
  - **Humbugs:** pillow shapes about 18 x 14 mm, dark brown (70, 40, 25) with 2 mm cream (230, 220, 190) stripes.
  - **Mint imperials:** white discs 16 mm across (238, 236, 228), with soft grey (190, 190, 186) shading only where they meet. The tile's mean luma should be at least 200.

### 5. The stockroom door's mottle is too strong (the builder's own shortfall, confirmed)

- **Where:**
  - The room picture by day: the door leaf at (2860-3070, 650-1350) ranges from luma 61 to 87 (5th to 95th percentile) round a mean of 74, in blotches of about 6 cm.
  - It reads as stained or marbled paint at 100 per cent in CLOSE_35 night_lit (1270-1365, 405-740) and in CLOSE_35 day.
  - It is not a slab and not a fault.
- **Whose:** the builder.
- **Exact fix (the builder's, which I agree with):** at the next room render, set the blotches to 4 per cent at 6 cm and 2 per cent in the fine ones (from 10, 5 and 3), and keep the vertical brush streaks.

### 6. The display on disk is not the display in the frames or in MANIFEST

- `newsagent_display.glb` was rewritten at 04:28 for the renames (sha256 f8f9e188…). The frames were rendered from the file the check measured, and MANIFEST names that one (a33ae862…, 04:10).
- So the file a rebuild or the PC would take is not the one reviewed. Its triangle count is the same (21,888), so I took the geometry measurements above from the 04:28 copy. Only the names should differ.
- **Whose:** the builder.
- **Exact fix:** the re-render of narrow 2, then the check, then MANIFEST, so that the hash it names is the file in the pictures.

### 7. The per-piece burn row asked in try 1 (narrow 4) was not added

- PIC-05g still counts whole frames only.
- I measured it from the check's own pieces pass:
  - CLOSE_35 night_lit: worst piece 17.2 per cent of its pixels at 250 or more;
  - CLOSE_35_B night_lit: 16.1 per cent.
- The burnt spots are small and natural: THE WALKER cover's sky (CLOSE_35 night 1052-1110, 908-934, 782 px), and the top of the WITH SYMPATHY card's photograph on the spinner (CLOSE_35_B night 2347-2462, 441-536, 2,542 px).
- **Whose:** the kit (`check_shop.py`).
- **Exact fix:** add to PIC-05g: from the pieces pass, no display piece with more than 20 per cent of its own pixels at 250 or more, at each night frame.

### 8. 64 samples, not 128 (known, named)

- **Exact fix:** the PC's render at 128 samples before his page.

## What is right

- **The near metre is a newsagent's of 1990, in real geometry.**
  - Two grey stands of folded tabloids on their steps.
  - Six cartons of 200 on a timber stand.
  - Twelve magazines on a raked board.
  - A plinth with a pot of pens, a yellow pad, an A4 ream and a note pad, the pads at 0.95 and 1.0 of real size.
  - Six glass sweet jars with screw lids.
  - A wire spinner of greetings cards and a postcard rack, both chrome with pockets.
  - Six hand-lettered price cards: PAPERS ORDERED; SWEETS 2oz 25p; CARDS FROM 25p; MAGAZINES; STATIONERY; PENS & PADS.
- **The placement is clean.**
  - Everything stands on or leans against something (DSP-05).
  - Nothing passes through anything (DSP-03: 0 pairs).
  - The racks' bases clear the jars by 37 mm or more.
  - Nothing is buried.
- **By day, the goods are shaded by the glass's sky light** as in a shop: soft shadows under the cartons, and each row of covers shading the next.
- **The room obeys the game's rule.** I imported `trace` and took the camera files' eyes, using the card x 36.35 to 41.65 and z 0.65 to 3.05.
  - The PENSIONS & ALLOWANCES notice (picture 2496, 753) lands on card point (1.6167, 1.2317) from CLOSE_35 and (2.9763, 1.2317) from CLOSE_35_B. `trace` returns exactly that picture pixel from both.
  - Projected through each camera, it falls at frame (1152, 468) and (2267, 427). The notice is there in all four frames, day and night, within 2 px.
  - The back wall moves 1.360 m on the card for 2 m of eye travel. The wall clock on the right wall (picture 3304, 607; 3.34 m deep) moves 1.224 m. The two differ, so the room has depth.
  - There is no black slab at either end. From CLOSE_35_B the left end is the return wall's plaster over its dado, meeting the room's left wall. From CLOSE_35 the right end is the right return wall.
  - The bed meets the room's floor with no gap or dark line (CLOSE_35_B night 1600-2560, 900-1440).
- **The door is complete.**
  - The glass foot is at 871, with the bar at 1423.
  - TOBACCONIST & CONFECTIONER is on the upper pane, with the green OPEN card by day and the red CLOSED card at night (SIGN-01: the shop shuts at 17:30).
  - The hours plate MON-SAT 6-5.30 / SUN 7-12 is on the lower pane, matching the target's hours. It reads the right way round at night too.
  - 18 is on the fanlight.
  - The brass lever is on the right stile, the brass letter plate in the lock rail, and the brass kick plate at the foot.
  - The dark blue side door has its knob, plate and fanlight.
  - There are no black strips. FRN-10 finds 0 front pixels under luma 8 at either close camera. My own scan of the whole day frames found under 8 only:
    - the side door's black knob (CLOSE_35 day 2278-2292, 831-850);
    - the dark underside of the hood at the frame's top edge (2302-2327, 0-13);
    - room shade.
- **The night is lit, with no stand-in showing.**
  - There is no arc, no burnt head and no orange bar.
  - The room is about twice as bright as the wall beside it (table below).
  - The pavement wash at the frame's corner is luma 74, with a top value of 101.
- **The content rule holds.** There is no drink, betting slip, coupon, toy, person, barcode or modern packaging, and no maker's name on any good. The only near-misses are narrow 2.

## Measured

**Glass luma.** The three main lights, the check's glass mask eroded 4 px, in the frames as rendered (with the stand-in reflection):

| frame | glass mean | per light, L to R | under 8 | under 12 | any channel at 250+ (glass) | whole frame at 250+ |
|---|---|---|---|---|---|---|
| CLOSE_35 day | 86.1 | 88.4, 84.7, 78.2 | 0.02% | 0.05% | 0.28% (the stand-in's sky at the glass's top, 1342-1410, 4-124) | 0.0079 |
| CLOSE_35 night_lit | 87.6 | 91.7, 85.9, 72.2 | 0.09% | 0.17% | 0.14% | 0.0009 |
| CLOSE_35_B day | 76.4 | 91.8, 75.8, 72.9 | 0.02% | 0.13% | 0.11% | 0.0093 |
| CLOSE_35_B night_lit | 83.4 | 78.0, 81.2, 85.9 | 0.45% | 0.84% | 0.35% | 0.0023 |
| CLOSE_35 night_dark (extra view) | 13.8 | 14.0, 12.9, 14.3 | 28% | 45% | 0 | 0.0000 |

- **With the reflection off** (the check's 1280 renders):
  - the room's part of the glass reads 48.1 and 51.1 by day, against the floor of 33;
  - at night it reads 65.5 and 72.5, against the floor of 45;
  - the display's part reads 111 to 137.
- **The wall beside the glass:** the stallriser's median is 128 and 130 by day, and 45 and 43 at night. So at night the lit window is 1.9 to 2.0 times the wall, and by day the room reads through the stand-in reflection in every light.
- **Black:**
  - by day the largest patch under 8 in the glass is 253 px, the gantry upright's shade in the room (374-384, 420-496);
  - at night it is 892 px and 2,409 px of room shade (see fault 1 above).
  - There is no void.
- **Flat** (9 x 9 standard deviation under 1): the largest patches are painted surfaces in even light, not a void or a white board:
  - the room's plain ceiling and upper left wall, behind the reflection (CLOSE_35 day 130-858, 4-296, luma 50, 4.35 per cent of the glass; 7.3 per cent at night);
  - the right return wall's plaster and dado (1780-1995, 133-1000, luma 75 and 62);
  - the shop door's glass, which shows the plain wall behind it.
  - The display's own pieces have no flat patch (FLT-01: 0.00).

## Rita's export faults, looked for here

- **A height map exported as a normal map:** none (GLB-01, FAS-01n).
- **A textured primitive without texture coordinates:** none (FAS-03: 0 in both glbs).
- **Black strips where two parts share a plane:** none visible. FRN-10 finds 49 coplanar overlaps, all hidden, and none under luma 8 at either close camera. My scan agrees.
- **A see-through slot from an angle:** none (FRN-08: 0 px at both close cameras).
- **The doorway's floor block:** FRN-13 sends 0 of 2,240 close-camera rays onto a reveal slab. Through the door's glass I see a plain wall, not a box.
- **The stand-in night light or glass visible:** none.
- **The kept glass parts of models:** the jars, the till's readout and the clock read as glass, with no black inside.

## The builder's named shortfalls

| shortfall | verdict |
|---|---|
| FLT-02 fails at STREET_30 (3.05 per cent against 3.0) | the street view's. At close range the flat patches are painted wall, not a void. Not judged here |
| the stockroom door's mottle | narrow 5 |
| the two pads at 0.95 | right: within DSP-06's 0.9 to 1.1, and they read as pads |
| about 265 invented packs and no sliding glass | right, not a fault |
| 12 magazines | right |
| the shutter up, with no shut-up variant | right for the lit view |
| no firm's name on the pension counter; nobody behind the counter | right |
| 64 samples | narrow 8 |
| the gate's display spill and the tones (covers, cards and postcards 0.80 to 0.82, pads 0.70) | right. LIT-08's lowest is 0.83 (it was 0.54). PIC-05g's worst close frame is 0.0093 by day (the sill's white) and 0.0023 at night |

## Check rows: which I trust

- **Trusted** (data and geometry, and the ones I repeated):
  - PIC-01, PIC-04, PIC-06;
  - PRJ-01;
  - PRJ-02 and PRJ-03, confirmed through `trace` against the frames;
  - SO-01 to SO-07; ROOM-01 to ROOM-05;
  - INV-01 to INV-07; NEV-01, NEV-02;
  - GLB-01, FAS-01n, FAS-03;
  - FRN-01 to FRN-05, FRN-07, FRN-09, FRN-13;
  - DSP-01, DSP-02, DSP-05 (I repeated the leans and the contacts), DSP-06, DSP-07, DSP-09, DSP-12, DSP-13;
  - PRT-02 to PRT-04;
  - SIGN-01; CAM-01; X-PRV.
  - **DSP-03** I trust as an intersection test.
  - **PRT-01** tests distinct pictures within a kind, not where they are hung (narrow 1). It also allows the same photograph on a magazine and a card: GARDEN LOG and GET WELL SOON both use `garden_shrubs`.
- **Only the cloud's stand-ins** (the gate's light, glass and lamp; the game's own are owed):
  - LIT-01, LIT-02, LIT-02b, LIT-05, LIT-07, LIT-08;
  - GLS-03, GLS-04, GLS-05;
  - PIC-05g, FAS-01c, TRD-01, FLT-01, FLT-02;
  - the pixel halves of FRN-08 and FRN-10.
  - The day frames' street reflection appears on the window glass but not on the shop door's glass. That is the stand-in; the game's glass is owed.

## What I cannot judge from the files

- **The renamed cartons (WYNYARD, RAVENSDALE):** no picture shows them yet (narrow 2).
- **Try 1's frames:** they were overwritten, so I could not repeat try 1's own frame numbers. I compared against try 1's review and the 13 October previews.
- **The game's own glass, Lumen, exposure and TSR**, and the box sign's glow (PC-08).
- **The bell:** it hangs inside the top rail by the hinge stile, behind that stile from both close cameras. I cannot judge its look, its swing or its sound.
- **Wear, grime and wet** on the joinery (the D53 layer).
- **The night_dark state as a night:** this shop's night is night_lit. I only checked night_dark for arcs and burns, and found none.
- **Anything of the street view.**
