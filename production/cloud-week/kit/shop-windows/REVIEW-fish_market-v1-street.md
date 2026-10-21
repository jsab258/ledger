PASS

# The fish market (east_parade bay 1, no. 3), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not write the target, the kit or this shop. I judged the street view only: STREET_SQUARE and STREET_30, by day, in night_dark (the shop's real night, STREET_SQUARE only) and in night_lit (the tests' state). I did not read the close view's review of this shop or any other review of the fish market.

One thing to declare: while checking the file name of this review, I opened the first 30 lines of another shop's street review (the chandler's) by mistake. Those lines name some newer kit rows, among them FRN-13 (the shop door's glass must not show the gate's reveal slab). I found narrow point 1 below by my own measurement. That row is also in TARGET.md section 13 (T2-16), which I had read before. I read nothing more of that review.

**What I read:**
- CLAUDE.md and RULINGS.md (1, 2, 3 and 8 October).
- NOTES.md: Rita's "For the next nine shops"; batch B's opening sections; the fish market's own section; lessons 28 to 41.
- TARGET.md: section 2 (P1), section 3, the fish market's table 5.2, and section 13 (B10 to B13, T2-16).
- Rita's four reviews.
- `checks/check_fish_market_v1.json`, every row.
- The parts of `sw_front.py` (the glass rows' placing) and `sw_gate.py` (the wall, piers, reveals and lights) that make what I saw.
- The fish market's lines in `sw_shops_fish.py` (the tins' makers, the lemons, the pilot lamp).

**What I looked at:**
- The 8 previews.
- The gate frames STREET_SQUARE (day, night_lit, night_dark) and STREET_30 (day, night_lit) at 2560 x 1440, in crops up to 8 times.
- The three room pictures at 4096.
- P1 (both previews), the 4.1 board (`fascias-fish-market-v3`), the Hook sheet, and Rita's approved front (`ritas-street-square-day-v3`).
- The Poly Haven `long_white_tiles` base colour.

**What I measured:** Rec.709 luma (0 to 255).
- I used the gate's own glass masks (`check_*_day_mask.png`, upscaled to 2560 and eroded 4 px), the front masks, and the reflection-off and backdrop renders. These are all still in the folder, so the numbers below are repeated, not copied.
- The two glbs' JSON, normal maps and UVs.
- The bounds of the front's and the display's parts (imported in Blender under `nice`).

Nothing in the repository or SCRATCH was changed apart from this file.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview).

## Verdict

**No fault blocks.** Seen from the far pavement, the front reads as a British Victorian parade shopfront with a later aluminium window and door, built from the 3.2 kit:
- panel pilasters, scroll consoles, a 550 board under a timber cornice;
- a sill and a white square-tiled stallriser;
- a 4L-4T window with the mullions carried up;
- the M1 shop door and the F1 side door;
- the band above both doors.

The board reads FISH MARKET / WET FISH / SHELLFISH / SMOKED by day and by night.

The window is glass with a readable room behind it:
- by day, a white-tiled fishmonger's room;
- in night_dark, an honestly dark shut shop with one small warm lamp.

Nothing in the window is a void or a white board. Rita's export faults are absent:
- the normal maps are real;
- no textured part lacks UVs;
- no coplanar black strip;
- no sky slot at STREET_30;
- the stand-in spill and glass do not show.

What the window does NOT do is show fish. The trade reads from the street through the lettering, the white tiles, the ice and the lemons, not through the goods. The fish are pending on Jafar's login (SCN-01, SCN-02, "pending, not failed"), so this is a known shortfall and not a fault of this build. Until the scans are in, the shop is not a finished fishmonger for his page.

There are nine narrow points, each with an exact fix (Jafar's ruling of 9 October: a pass with the points listed). The three that matter most:
1. The shop door's lower glass shows the gate's reveal slab: flat grey by day, black at night.
2. FRESH DAILY sits over the display's white back panel and nearly vanishes.
3. The eight lemons stand upright on their tips.

## Faults, worst first

None.

## Narrow points, most important first (each with its exact fix)

### 1. The shop door's lower glass shows the reveal slab under the room card (an opening with nothing behind it)

- **Where:** the M1 door's glass from its foot (z 198) up to about z 550, STREET_SQUARE, x 1705 to 1875, y 935 to 1020 (1600: x 1066 to 1172, y 584 to 638).
  - By day it is a flat blue-grey panel, RGB (55, 58, 63), luma 58 to 62, sd 5 to 10.
  - In night_lit it is black: luma 3.7, sd 0.7.
  - In night_dark it is black: luma 1.0 to 1.9, sd 0.5 to 0.9.
  - The rest of the door's glass shows the room and its terracotta floor.
- **Cause:**
  - The M1 leaf is glazed from z 198 (FRN-03).
  - The room card's floor stands 550 above the footway (TARGET section 3: "which the stallriser hides from the street"). The door has no stallriser.
  - So rays through the door's lowest 350 mm pass under the card and end on the gate's dark matt `reveal_floor` slab.
  - In the game the same rays pass under the card into whatever stands behind the facade. That is a hole in the game asset, not only in the gate.
- **Why narrow at this distance:** from the far pavement by day it reads as a solid lower panel of the door, and the shop is dark at night. The close view must judge it at 1.5 m, where it may read as a void.
- **WHOSE:** the target (the M1 door glazed to 198 in front of a card whose floor is at 550) and the kit. The kit's FRN-13 row (T2-16) was written after this build and was not run on it.
- **EXACT FIX (cheapest):**
  1. Make the M1 leaf's bottom rail a solid aluminium kick panel from z 28 to 560 (the card's floor plus 10 mm), in `alu_natural`. The glass then runs from 560 to 1968.
  2. The letter plate stays at z 113, now inside the panel.
  3. This also moves the door toward P1's half-glazed door: glass foot 0.413 of the leaf.
  4. Rebuild the front and re-render the four street frames.
  5. Add FRN-13 to this shop's check: 560 rays through the shop door's glass, and none ends on a reveal slab.

### 2. FRESH DAILY lies over the display's white back panel and nearly vanishes

- **Where:** STREET_SQUARE day, the fourth light's foot, x 1488 to 1650, y 846 to 872 (1600: x 930 to 1031, y 529 to 545); STREET_30 the same.
- **Measured:** the letters reach luma 213 (p95) against a ground of 184 (median), a ratio of 1.15. SHELLFISH reads 3.64 and SMOKED FISH 2.31.
  - The F and the R are the faintest. In the 1600 preview the row reads "RESH DAILY" at a glance.
- **Cause:**
  - The row stands where 4.1 put it: baseline 850 above the footway, ink z 0.82 to 0.98, at scale 0.80.
  - The display's `chiller_pad` (the white back panel, 0.30 high, 0.52 behind the glass) has its top edge on the glass at about z 0.97 from the far pavement, and at about z 1.10 from CLOSE_35.
  - So the white letters lie on a white board.
  - GLS-02 checks only bars, so it passes.
- **WHOSE:** the builder. The kit's `row_places` keeps 4.1's place without asking what lies behind the ink.
- **EXACT FIX:**
  1. Raise row 3 (FRESH DAILY) by 350 mm, to a baseline 1200 above the footway, at the same x and scale (ink about z 1.20 to 1.31).
  2. There it lies over the back wall's tiles (luma about 60 to 75) from both street cameras, and it clears the panel from CLOSE_35 as well.
  3. Write it as a per-row place in the target's `glass.lettering_places` for the fish market.
  4. Add a row to the shop check: at STREET_SQUARE and STREET_30 by day, each glass row's letters against the pixels round them read 2.0 or more, as FAS-01c's limit.

### 3. The eight lemons stand upright on their tips

- **Where:** STREET_SQUARE day, the window's foot, x 930 to 1640, y 860 to 910. There are eight upright yellow ovals, each about 20 x 27 px, like eggs in a row (1600: y 537 to 569).
- **Cause:**
  - Poly Haven's `lemon` is modelled standing on its end (69 x 69 x 95 mm).
  - `sw_shops_fish.py` line 421 turns each lemon only about z: `rot=(0, 0, random)`.
  - On a slab sloping 12 degrees, a lemon on its tip would roll over.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. `rot=(pi/2, 0, random)` (the long axis lies along the slab; the height is about 0.07 m).
  2. Settle each lemon down onto the ice bed (`settle_down`).
  3. Re-run DSP-03 and DSP-05.
  4. The close view judges them in detail.

### 4. The wall tile reads as narrow vertical "finger" tiles, not the target's 152 mm square tile

- **Where:** every frame through the window, for example STREET_SQUARE day x 1300 to 1460, y 640 to 720. The back and side walls show a fine vertical grid.
- **Measured:** in `fishmonger_day.png` (back wall x 1900 to 2500, y 600 to 1000) the tiles are about 27 mm wide and 90 mm tall, laid in stack bond. That is Poly Haven `long_white_tiles` (33 columns a repeat) at `WALL_TILE_M` 0.9 m.
- **Why it matters:**
  - From the far pavement the walls read as a fine mesh.
  - At 1:1 they read as a 1960s or 2010s finger mosaic, not the white glazed 6-inch square of a 1990 British fishmonger.
  - The target asks for "white glazed square tile 152 mm, grey grout".
- **WHOSE:** the target, which offers `long_white_tiles` "or square_tiles" beside "152 mm square", and the builder, who chose the long ones.
- **EXACT FIX:**
  1. In `sw_room_gen.py`, give the fish market Poly Haven `square_tiles` (or the script's own square tile) scaled so one tile is 152 mm, with grey grout, on the walls and dado.
  2. Re-render the three room pictures.
  3. Do it in the same render as point 6.
  4. Strike "long_white_tiles or" from the target's 5.2 row.

### 5. Slots between the pilasters' capitals and the frame (the kit's), and FRN-08 names them wrongly

- **Where:**
  - STREET_SQUARE: the left pilaster's capital, on its window side, x 884 to 890, y 430 to 478. It is a 2 to 3 px dark red line: the gate's brick pier in shade, RGB (37, 21, 17).
  - STREET_30: the right pilaster's capital, on its door side, x 2046 to 2054, y 428 to 456. It is a dark crescent beside the curved side of the capital.
  - FRN-08's own backdrop renders show them: 40 px at STREET_SQUARE (1280: x 443 to 444, y 216 to 238) and 15 px at STREET_30 (x 1026, y 214 to 228). I repeated both counts.
- **Cause:**
  - `pilL_core` and `pilR_core` stop at z 2.540.
  - The capital above them (z 2.54 to 2.85) has a curved side that leaves the frame line at u 350 and 5650.
  - So between z 2.55 and 2.79 there is a 3 to 5 mm gap into whatever stands behind the front. In the gate that is the pier; in the game it is the street facade (PC-04).
  - FRN-08 says this is "the bay's outer sliver beside the right pilaster". It is not: these are the capitals' inner sides.
- **What it is:** at 8.76 m it reads as a shadow joint, so it is narrow.
- **WHOSE:** the kit (the 3.2 pilaster as assembled). Every shop with this pilaster has it.
- **EXACT FIX:**
  1. Run each pilaster's core up from z 2.540 to 2.790, under the window head and the band's head.
  2. Keep its inner face 1 mm inside the frame line (x -2.651 and 2.651), so no face is shared (FRN-10).
  3. FRN-08 should then read 0 px at both street cameras without the gate's pier.
  4. Correct FRN-08's wording.

### 6. LIT-02b at STREET_30 by day passes by a hair (0.0099): the blackboard

- **Where:** STREET_30 day, the "TODAY'S FISH" board on the left wall, x 1207 to 1271, y 575 to 680. The largest dark patch is x 1216 to 1266, y 610 to 648.
- **Measured:**
  - On `check_STREET_30_day_norefl.png` I read the share under 12 as 0.0119, the same as the row.
  - My largest connected patch is 0.0061 (4-connected); the row's 0.0099 is probably 8-connected. Both are under 0.01.
- **What it is:** not a void. It is a chalkboard with chalk on it, a wooden frame, and the awning rail in front of it at STREET_30.
- **WHOSE:** the builder.
- **EXACT FIX:** the builder's own. Make the slate (66, 76, 70) when the room is next rendered (with point 4), and keep the row as it is.

### 7. The awning's arms are vertical, not the target's diagonal, and NOTES does not say so

- **Where:** `rail_awning_arm_l/_r` are 30 mm bars at x -2.636 to -2.606 and 0.656 to 0.686, z 2.098 to 2.790, standing in front of the window's jambs.
  - From STREET_SQUARE they hide against the jambs, so the black rail at z 2.06 to 2.10 reads as a bare bar across the lights.
  - It does match P1's black rail.
  - At STREET_30 the left arm shows as a dark rod in front of the jamb: x 1004 to 1009, y 520 to 609.
  - The parts meet: rail to arm 4 mm, arm to bracket 4 mm, bracket on the head's face. Nothing floats.
- **WHOSE:** the builder. The target says "two diagonal arms" and calls the arms a Judgement; NOTES F6 calls them a Judgement but does not say they were made vertical.
- **EXACT FIX:** record it in NOTES F6 and in the target's changes:
  > "the arms are vertical 30 mm bars in front of the jambs (z 2.10 to 2.79); from the far pavement the rail reads as P1's black bar".

  No geometry change is needed for the street view.

### 8. "FENWICK", a real firm's name, is one of the four makers on the shop's tins and jars

- **Where:** the room's shelf (`fishmonger_*.png`; `texts.json` lists FENWICK three times: HERRING FILLETS, SMOKED MUSSELS, PICKLED HERRING).
  - Not legible from either street camera: the tins are 6 to 8 px labels.
  - It may be legible from the close cameras and in the room pictures at 100 per cent.
  - Fenwick is a British department store firm (since 1882) and a fishing-tackle maker's mark.
- **WHOSE:** the builder (`sw_shops_fish.py` lines 25, 26 and 30; NOTES F7; ROOM-02's text).
- **EXACT FIX:**
  1. Replace FENWICK with an invented name that is not a registered UK company or trade mark (check Companies House and the UK IPO register first).
  2. Check SALTHOUSE, TIDEMARK and BRIGHTWATER the same way.
  3. Add FENWICK to the content blocklist so NEV-01 would catch it.
  4. Re-render with point 4.

### 9. The night set: STREET_30 in night_dark is not rendered, and the night_lit street preview shows a shut shop lit and OPEN

- **Where:** the gate has STREET_30 only in night_lit. The preview `fish_market-street-square-night-lit` shows:
  - the room at full light;
  - the door's card reading OPEN at night;
  - the stand-in pool on the pavement.

  The shop shuts at 14:00 and is never like this. The shop's real night at STREET_30 cannot be judged.
- **WHOSE:** the builder (the gate set for a dark shop; NOTES F9).
- **EXACT FIX:**
  1. Render STREET_30 in night_dark (one frame, about 5 minutes at 32 samples) and add its preview.
  2. Name the night_lit previews "...-night-lit-teststate-..." or keep them off Jafar's page. The night_dark preview is this shop's night.

## The builder's named shortfalls, judged at street distance

| builder's shortfall (NOTES, check file) | my judgement |
|---|---|
| No fish (SCN-01, SCN-02 pending) | **Pending, not a fault** (the brief). From the far pavement the goods say ice and lemons, not fish; the trade is carried by the board, the glass rows and the white tiles. No stand-in fish exists anywhere in the frames. Not for Jafar's page as a finished fishmonger until the scans are in. |
| The ice reads as angular blue-grey shards (CLOSE_35) | The close view's. From the street the six heaped mounds in otherwise empty trays read as trays of grey-blue gravel (STREET_SQUARE x 930 to 1640, y 870 to 910). The real fix is the fish (the ice goes under them) and the CC0 ice photograph the builder names. Narrow here, not counted twice. |
| The chiller's trays hard to see in the day room picture | Not a point from the street. The chiller reads as a long white counter with a sloping glass top, and there is nothing on its trays to see. |
| LIT-02b at STREET_30 by day 0.0099 | **Narrow** (point 6): the blackboard, not a void. |
| PIC-05g at CLOSE_35_B by day 0.0098 | The close view's. At the street cameras PIC-05g reads 0.0002 and 0.0007, and I find 0.17 and 0.11 per cent of the window's glass with a channel at 250 or above: nothing burnt. |
| Slab, ice bed and back panel are `support` pieces | Right: they are the table the goods stand on. But the back panel is what blanks FRESH DAILY (point 2). |
| Price chart and tickets drawn by script | Not legible from the street, so not a point here. |
| 66 tins and jars (target 24) | Right: from the street the shelf reads as stocked. |
| 48 samples | No noise seen at street distance (X-NOISE 0.39). Not a point. |

## Shared, known (from the first five shops' reviews; none decides this verdict)

- **(a) the burnt orange bar in the night glass:** not present. GLS-04 reads 0 px at both street cameras, and I repeated it (0 and 0). GLS-03 reads p95 2.2 and 2.5, repeated exactly. The night_dark glass has no bar (p95 25).
- **(b) hot top corners in night_dark:** not present (PIC-03: 5.4 and 5.8 against 27).
- **(c) the loader dropping glass parts:** not seen from the street. DSP-07 keeps the clock's glass.
- **(e) sheets leaning toward the glass:** not visible from the street. DSP-05 measured "0 thin sheets", so the tickets' lean was not tested; that is for the close view.
- **(f) CLOSED on a lit shop at night:** not present. This dark shop shows CLOSED in night_dark, which is right, and OPEN in the night_lit test state.
- **(g) child-size furniture, turned chairs, plastic curtains:** none in this shop.

## What is right

**The front:**
- It is a Victorian parade shopfront refitted in aluminium:
  - pale grey panel pilasters on plinths;
  - scroll consoles with a leaf;
  - a 550 board under a timber cornice;
  - the sill;
  - a white square-tiled stallriser with a black foot course;
  - a 4L-4T window with the mullions carried up through the toplights.
- The proportions match Rita's approved front, which comes from the same kit, and the Hook sheet's parade fronts.
- Pale grey, red and black belong beside the Hook sheet's white-fronted shop and Mickey's navy.
- **The band above the doors is built.** Over the shop door: three toplights, the transom, and a fanlight with the 3. Over the side door: a raised panel, the transom and a fanlight. FRN-07 finds no hole.
- **The side door's fanlight shows a dim hall** (FRN-09: no ray reaches the card).
- **The doors are handed as the target says.** The shop door has its hinges on the window side and the D pull on the right. The near-black F1 side door has its knob in the centre, its lock on the pier side, and a vertical letter plate in the centre muntin, as Rita's. Nothing is mirrored and no text reads backwards.
- **Nothing floats.** The consoles and the cornice meet the board, and the rail, arms and brackets meet each other and the head. I scanned the front for dark strips: by day only 61 px at STREET_SQUARE and 23 at STREET_30 are under luma 8, in two small patches (the side door's knob and keyhole). Under luma 20 there is only the side door's top rail in the transom's shade. There is no coplanar strip, as FRN-10 says.

**The lettering, all of it the shop's own and acceptable:**

| where | words |
|---|---|
| board | FISH MARKET / WET FISH / SHELLFISH / SMOKED. By day, letters to ground 2.54 (FAS-01c). In night_dark the painted (not gilt) letters still read clearly, unlike Rita's gilt. |
| glass | SMOKED FISH, SHELLFISH and FRESH DAILY in white hand lettering, the period fishmonger's style. No letter is crossed by a bar or the rail at either camera (GLS-02, and by eye up to 5 times). The rail clears SMOKED FISH's caps by about 30 mm. FRESH DAILY's contrast is point 2. |
| fanlight | 3 |
| door | OPEN by day (green card) and CLOSED in night_dark (red card); MON-SAT 7.30-2 / WED 7.30-1 / SUN CLOSED, which matches the target's hours. |
| room | The blackboard: TODAY'S FISH, COD, HADDOCK, PLAICE, KIPPERS and prices "2.60 lb" and so on. Only just legible at STREET_30 at 100 per cent. |

No tin label or ticket is legible from either street camera. No real firm's name, drink, betting, child or modern mark is legible in any street frame; FENWICK (point 8) is not legible from here. There is no barcode and no flat screen.

**The window, by day:**
- It is glass with a lit, readable room: the white tiles, the shelf of tins, the hose, the chiller counter and the blackboard.
- Below them is the slab with six trays, eight lemons and tickets.
- There is no pixel under 3 and no void. The largest flat 9-px patch is 2.4 per cent of the glass: the chiller's flat cabinet front at luma 52.
- The glass is a little dimmer than the brick beside it (0.91), as D5, P1 and P3 ask. It is brighter than Rita's (0.69) because of the white tiles and the white slab.

**The window, in night_dark (the shop's real night):**
- It is an honestly dark shut shop. The glass reads luma 16.0 against the lit brick's 17.3, inside the target's 10 to 35 (LIT-01's composite: 15.0).
- The room is seen dimly in the sodium wash. What is under luma 3 (2.6 per cent) is the hose coil, the blackboard and the cold-room door's black frame: real dark things in small patches, the largest 1.3 per cent. There is no slab and no white board.
- The pilot lamp reads as one small warm light at the chiller's left end, x 1043 to 1078, y 743 to 764, with its reflection in the glazed side-wall tiles at x 990 to 1011, y 733 to 751.
  - It is warm white rather than amber: core RGB (208, 209, 207), glow (141, 122, 93).
  - That fits the target's "2700 K glow lamp".
- The CLOSED card reads.

**Rita's lessons, checked here:**

| Rita's fault | here |
|---|---|
| height map as a normal map | No. The fascia's normal map is RGB, mean (127.5, 127.5, 255), blue 160 or more on 100 per cent; it is flat, so it carries no relief. The lemon's is (127, 127, 248). |
| textured primitive without UVs | No. 8 textured primitives in the front glb and 10 in the display glb, none without TEXCOORD_0, none with a negative texCoord. |
| coplanar black strips | No (see the front, above). |
| sky slot at STREET_30 | No. The pilasters' outer edges show brick at both cameras. The only gaps are point 5's. |
| stand-in light in front of the glass | No. No white band under the transom (LIT-07: 0.0000), and the mullions are darker than the glass. |
| night glass doubling | No (GLS-03 2.2 and 2.5, repeated). |
| side-door fanlight showing the shop | No (FRN-09). |
| front row under the sight line | No. The trays and lemons are seen from STREET_SQUARE itself (DSP-03 lowest 0.57). |

## Measured (my numbers)

Luma over the window's glass (the four lower lights from the gate's mask, eroded 4 px; the toplights from the front mask).

| | SQ day | 30 day | SQ night_dark | SQ night_lit (test) | 30 night_lit (test) |
|---|---|---|---|---|---|
| lower lights, mean (p5 / p95) | 77.0 (26.7 / 196.4) | 75.5 (26.9 / 197.2) | 16.0 (5.6 / 25.4) | 90.8 (30.3 / 165.7) | 83.5 (33.9 / 164.8) |
| toplights, mean | 41.7 (the ceiling and battens) | 42.0 | 12.1 | 47.0 | 44.0 |
| under 3 / under 12 | 0 / 0.52% | 0 / 0.31% | 2.62% / 22.2% | 0 / 0.22% | 0 / 0.01% |
| largest patch under 12 | 0.17% | 0.08% | 2.90% (the display's foot, unlit) | 0.05% | 0.01% |
| a channel at 250+ | 0.17% | 0.11% | 0 | 0 | 0 |
| largest flat patch (9 px, sd under 1) | 2.4% (the chiller front, 52) | 2.6% | 6.0% (the chiller front, 16) | 2.3% | 2.5% |
| brick beside | 84.3 | 85.3 / 83.4 | 17.3 | 19.1 / 17.6 | 19.1 / 17.5 |
| glass / brick | 0.91 | 0.89 | 0.92 | 4.8 | 4.4 |

Other measures:
- The display band at the window's foot (y 850 to 918) reads 180 to 193 by day: the white slab, trays and ice.
- The door's lower glass reads 58 to 62 by day and 1 to 4 at night (point 1).
- Glass rows by day, letters to ground: SHELLFISH 3.64, SMOKED FISH 2.31, FRESH DAILY 1.15.

**Rows I repeated and agree with:**
- LIT-02b's shares (0.0078 at STREET_SQUARE, 0.0119 at STREET_30).
- GLS-03 and GLS-04 (exact).
- FRN-08's 40 and 15 px (but not its wording: point 5).
- GLB-01, FAS-01n and FAS-03.
- FRN-10's dark-pixel half.
- LIT-01, within 0.5.
- The camera files match the defined eyes and aims (CAM-01).

## The 66 counted rows: which I trust

- **Trusted, measured on the real pictures, meshes or files:**
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-07, DSP-01, DSP-02, DSP-04, DSP-06, DSP-07;
  - ROOM-01, ROOM-02, ROOM-03, ROOM-05;
  - INV-01 to INV-06, NEV-02, GLB-01;
  - FRN-01 to FRN-05, FRN-09, FRN-10;
  - FAS-01, FAS-01c, FAS-03;
  - GLS-01, GLS-02, LIT-06, CAM-01, X-PRV.
- **Pass but do not prove what they say:**
  - NEV-01: a blocklist cannot know that FENWICK is a real firm (point 8).
  - TRD-01: it proves that the trays and tickets are big enough and seen, not that they say "fish"; SCN-02 holds that, pending.
  - FRN-08: the count is right and the label is wrong (point 5).
  - GLS-02: bars only, not what is behind the letters (point 2).
  - FAS-01n: a real but flat normal map.
  - DSP-05: no thin sheet was measured, so the tickets' lean is untested.
  - FRN-07: passes with the gate's piers standing in for the facade (PC-04).
- **The cloud's stand-ins only:**
  - LIT-01 and LIT-02 (the card's bake);
  - LIT-02b, LIT-05, LIT-07, LIT-08, GLS-03, GLS-04 and PIC-05g (gate renders under the stand-in glass, lamps and 80 W spill). LIT-05 and LIT-08 are measured in night_lit, which is not this shop's night;
  - GLS-05 (the gate's own glass);
  - PRJ-02 (the gate's own `trace`).
- **Pending:** SCN-01, SCN-02. **n/a:** FRN-06, FAS-02, LIT-03, PRV-01.
- **Not in this check:** FRN-13 (T2-16) was written after this build. Point 1 is what it would have found.

## What I cannot judge from these files

- **The game's glass.** The street and sky in the panes (the Hook sheet's bar, RULINGS 3 October), dirt, and the night hand-over. Here the day glass reflects almost nothing, and the window reads as an opening made legible by its lettering.
- **The game's light.**
  - Lumen on the display. The white slab reads 180 to 193 by day under the gate's sky.
  - The game's pilot lamp and sodium wash (owed).
  - Exposure.
  - The street lamps' pools: the gate's two lamps wash the wall evenly orange, and that context is not judged.
- **Wear on the front.** Apart from the board's flakes the front is spotless; the D53 layer is owed (PC-05).
- **Motion.** The card's parallax as the player walks, TSR, and the 32-sample frames.
- **The shop's real night from STREET_30** (point 9).
- **Whether the game's facade closes behind the pilasters and the capitals** (PC-04, point 5), and what the game shows under the card behind the door (point 1).
- **The fish, which are not in the files.** Whether the scans, once placed, read as cod, mackerel and plaice from 8.76 m is for the next review.

**Measurements I could not repeat:**
- FRN-07's elevation;
- DSP-03's and TRD-01's silhouette shares (I did not re-run the object-index pass);
- LIT-05, LIT-07 and LIT-08;
- PIC-05g at the close cameras;
- GLS-05.

**Next:**
- Fix points 1 and 2 on the front (one front rebuild, four street frames).
- Fix points 3, 4, 6 and 8 in one room-and-display render.
- Record point 7.
- Point 5 goes to the kit for every shop.
- Render point 9's frame.

None of this blocks the pass. The fish, when Jafar's login fetches them, are the change that makes this window a fishmonger's.
