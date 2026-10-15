FAIL

# The fish market (east_parade bay 1, no. 3), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not write the target, build the shop or review any other shop. One view only: CLOSE_35 and CLOSE_35_B, by day and in night_lit (the test state; the shop is dark at night). I did not read the street view's review or any other review of this shop or of the chandler.

Read: CLAUDE.md; RULINGS.md (1, 2, 3 and 9 October); NOTES.md (For the next nine shops, batch A and B lessons 16 to 41, What batch B changed in the shared kit, and the fish market's own section); TARGET.md section 3, table 5.2 and section 13 (B10, B11, B13); Rita's four reviews; `checks/check_fish_market_v1.json` (all 72 rows); `MANIFEST-fish_market.json`; the parts of `sw_shops_fish.py`, `sw_goods_b.py`, `sw_gate.py`, `sw_ctx.py`, `sw_room_gen.py` and `tools/ue/make_interior_material.py` named below.

Looked at: the two close previews; the four close gate frames (2560 x 1440, 14 Oct 08:32 to 09:18) whole and in crops at 100 to 300 per cent; the reflection-off, mask, room-mask and front-mask renders; the baked cards; the three 4096 room pictures; the display glb's own textures (ice, slab, tickets, lemon) and the label atlases (tins, jars, tickets, blackboard, price chart).

Measured (all in my scratchpad; nothing in the repository or SCRATCH was changed): the parallax through the game's own `trace`; the glass's luma by day and night; dark, black, flat and burnt pixels inside the glass; the ice's colour; the tickets' lean, the lemons' pose and the awning's parts from the glbs; UVs and normal maps of both glbs; the manifest's sha256 against the six files (all six match).

**In short.** The projected room works exactly as the game's rule says, the front and the doors are clean at close range, and the night is clean. But the near metre, which is what this view is for, does not read as a fishmonger's slab: with the fish pending, the window's stock is ice, and the ice reads as heaps of blue-grey paper pyramids, not as ice. That is one fault, and it is this shop's own. Twelve narrow points follow.

**1 fault, 12 narrow points.**

## Fault

### 1. The crushed ice reads as blue-grey paper shards, not ice (every close frame, day and night)

- **Where** (2560 frames; the previews are 0.625 of these):
  - CLOSE_35 day: all six trays' mounds and the bed between them, x 690 to 2400, y 900 to 1330. At 100 per cent one tray (x 1290 to 1480, y 1060 to 1150) is a scatter of separate, sharp-edged, pale blue pyramids with the white tray floor showing between them; the bed between the trays (x 900 to 1250, y 1000 to 1180) is a flat picture of drawn triangles and scratch lines that reads as crumpled foil or broken glass.
  - CLOSE_35_B day: the two near trays, x 0 to 730, y 1170 to 1400, the largest ice in the view: folded-paper or crystal-gem shapes.
  - CLOSE_35_B night_lit, same places: grey instead of blue, the same paper shapes.
- **Measured:** the ice by day is strongly blue: mean sRGB (169, 190, 212) in a CLOSE_35 tray, (166, 186, 206) in the CLOSE_35_B near tray, blue minus red 38 to 43 levels. Real crushed ice on a fishmonger's slab reads near-white with clear glints and grey shadows. The glb's `ice` material is an opaque picture at roughness 0.22, no transmission or wetness; the picture (`sw_goods_b.ice_png`) is a blue base (196, 210, 220) with 260 drawn triangles and 40 lines; each chunk (`ice_chunk`) is a regular octahedron 22 to 44 mm across; the mound (`ice_mound`) drops 380 of them at random heights in a dome, so the tray shows through and single chunks can hang in the air (DSP-05 tests the mound as one group, so it cannot see this).
- **Why it is a fault and not narrow:** no fish stand in the window (correctly: they are pending, and there is no stand-in of any kind in the display glb: its meshes are the bed, the slab, the ice bed, six trays, six ice mounds, eight lemons, the stakes, the tickets, the back panel and the two return walls). So the ice is most of what the near metre shows (the six mounds and the bed between the trays; not measured as a share). It is an obvious CG prop at the distance this view exists to judge, and when the fish come the ice will still show round them. The builder names it ("looked at full size; kept"); I judge it a fault.
- **Whose:** the builder, in the kit's shared helpers (`sw_goods_b.ice_png`, `ice_chunk`, `ice_mound`) and their use in `sw_shops_fish.py` (display and the room's chiller).
- **Exact fix:**
  - **Material** (one material for the window's ice and the chiller's): Principled, base colour sRGB (226, 232, 236), roughness 0.06, IOR 1.31, transmission weight 0.35 (or subsurface weight 0.5, radius 10 mm), coat weight 0.4 at roughness 0.03 for the wet film. In the glb keep base (226, 232, 236), roughness 0.06 (the game's ice shader takes the rest).
  - **Picture:** remove the 260 drawn triangles and the 40 lines from `ice_png`; keep the cloudy mottle on a base of (226, 232, 236), add 2 to 4 px white specks (245, 248, 250); the facets' shading must come from the geometry, not the picture.
  - **Shape and size:** chunks 8 to 18 mm (`sz = uniform(0.008, 0.018)`), each octahedron subdivided once with its corners pushed out by 0.15 to 0.30 of its radius at random, shading smooth with a 40 degree auto-smooth angle; under them a mound surface of their own (an ellipse dome of 64 x 48 quads, the same half axes and height, displaced 4 mm by noise) so that no tray floor shows through and every chunk rests on something (about 400 chunks a tray on top of it). The ice bed between the trays is made the same way, at 0.03 high.
  - **Acceptance:** at CLOSE_35 day at 100 per cent it reads as wet crushed ice; the ice's mean blue minus red is 12 levels or less; under 2 per cent of each mound's footprint shows tray floor; DSP-05 runs per chunk; PIC-05g stays at 0.01 or under in all four close frames (check it with two 8-sample frames first, lesson 33: the whiter ice will raise it).
  - The builder's own alternative (a CC0 photograph or scan of crushed ice) is also good, but needs research first: none is in the checked lists (ambientCG Ice001 and Ice002 are sheet and lake ice).

## Narrow points, most important first (each with its exact fix)

### 1. A real firm's name, FENWICK, is on three of the room's goods

- **Where:** `sw_shops_fish.TIN_DESIGNS` (herring fillets, smoked mussels) and `JAR_DESIGNS` (pickled herring). In the 4096 room picture at 100 per cent "ENWICK" can be read on a tin (fishmonger_day.png about x 1680, y 590); it cannot be read in any close frame or preview (the labels are about 4 px there).
- **Why:** Fenwick is a real British firm (the Fenwick department stores, trading in 1990, with their own food halls) and a well-known maker of fishing rods. The content rule allows no real firm's name anywhere. INV-05 and NEV-01 cannot catch it: no row checks invented names against real firms.
- **Whose:** the builder.
- **Exact fix:** replace FENWICK with a placeholder from the town's names (RULINGS 3 Oct: names are minted within canon; placeholders meanwhile), checked against the UK trade-mark register (class 29, preserved fish) and Companies House before use. Run the same check on SALTHOUSE, TIDEMARK and BRIGHTWATER. Add FENWICK to the INV-05 blocklist. Re-render the three room pictures. This must be done before the shop merges.

### 2. All eight lemons stand on their tips

- **Where:** CLOSE_35_B day, e.g. x 1169 to 1212, y 1053 to 1111 and x 1571 to 1612, y 1045 to 1095 (seen as upright eggs); every lemon in every close frame.
- **Measured:** each lemon is 74 x 75 x 95 mm with its long axis vertical (the Poly Haven model is authored standing; `d.piece("lemon", ..., rot=(0, 0, random))` only turns it about the vertical). A lemon cannot stand on its point on a 12 degree slab of ice.
- **Whose:** the builder.
- **Exact fix:** `rot=(radians(90), 0, uniform(0, 2 pi))` so each lemon lies on its side, resting at half its width (0.035) by `rest_z` and `settle_down` as now. Better still, when the fish come, halve three of them and put them by the fish, as a fishmonger does.

### 3. The room's walls are 27 x 90 mm vertical finger tiles, not the target's 152 mm square tiles

- **Where:** the whole back and side walls of the room; at close range the back wall reads as wire mesh or graph paper (CLOSE_35 day x 1400 to 2560, y 250 to 900; CLOSE_35_B day x 400 to 1800, y 100 to 650).
- **Measured:** in fishmonger_day.png the back wall's vertical joints repeat every 11.3 px (27 mm at 418 px a metre). The Poly Haven `long_white_tiles` texture holds 33 columns by 10 rows a repeat; `WALL_TILE_M` 0.9 makes each tile about 27 x 90 mm in a vertical stack. The target (5.2) says white glazed square tile 152 mm, grey grout, from the dated photographs; a narrow vertical stack is a recent fashion, not a 1990 fishmonger's.
- **Whose:** the builder (the repeat "set by eye").
- **Exact fix:** Poly Haven `square_tiles` (on the target's surfaces list) with the repeat set so one tile is 152 mm, grout (175, 175, 170), on every wall to the ceiling. Re-render the three pictures. Add a row: the wall's joint period measured in the picture is 152 mm plus or minus 10 per cent.

### 4. The window's end walls are not the shop's tile

- **Where:** CLOSE_35, the far light, x 560 to 800, y 100 to 1000 (by day and at night): horizontal stripes about 38 px apart with no vertical joints, which read as horizontal boarding beside the tiled side wall in the next light.
- **Measured:** the display glb's `return_wall_*_dado` and `_plaster` carry Rita's names and a plain buff (206, 204, 195) at roughness 0.9, so in the game the window's ends will be plain plaster in a tiled shop. In the gate they show the picture's front column stretched along the wall (`col_l_day.png`), which keeps the rows and loses the joints. The luma matches the room (65.8 against the side wall's 62.7 by day): there is no black slab.
- **Whose:** the kit (the return-wall rule was written for Rita's plaster and dado) and the builder (the glb material).
- **Exact fix:** in the glb, both return walls take the room's wall tile (point 3's material and tile size, rows at the room's heights), one finish from floor to ceiling. In the gate, their emission is that tile picture times the mean of the picture's front column (`col_l`, `col_r`) times the state's brightness, not the column stretched.

### 5. The tickets stand in a fixed zigzag, not before their goods

- **Where:** CLOSE_35_B day x 380 to 1900, y 980 to 1300 (the stakes behind and in front of the trays); all fourteen tickets.
- **Measured:** `uc = 0.22 + 0.22 k`, v alternating 0.10 and 0.44, whatever lies there: a regular grid of the same thing (lesson 9), and twelve fish prices stand over bare ice (lesson 29: a price card stands before its own goods). Their lettering is right and they lean back 6 degrees, as they should.
- **Whose:** the builder.
- **Exact fix:** when the fish come, one ticket for each fish, staked in the ice at the front of its tray (v 0.12, at the fish's u plus or minus 0.08), LEMONS beside the lemons, ICE FREE at an end; no fixed pitch. Until then, leave them.

### 6. "SMOKED" reads "SHOKED" from CLOSE_35

- **Where:** CLOSE_35 day, the word at x 1860 to 2420, y 100 to 250, the M at x 1930 to 2025: the M's middle V stops about a third of the way down, so at 100 per cent it reads as H. From CLOSE_35_B it reads SMOKED FISH.
- **Whose:** the kit (the glass rows' brush lettering).
- **Exact fix:** the M's middle vertex at 0.55 to 0.65 of the cap height from the top; check with `ocr_words.py` that SMOKED is read at CLOSE_35 day.

### 7. LIT-02b has almost no margin at the close day frames

- **Where:** the reflection-off frames: CLOSE_35 day 0.0094 of the glass under luma 12, CLOSE_35_B day 0.0099 (room share 0.0098), against 0.01. The dark pixels are the blackboard (CLOSE_35 x 1140 to 1250, y 360 to 520; CLOSE_35_B x 200 to 290, y 230 to 440) and the shadow line under the chiller's plinth (CLOSE_35 x 1394 to 1744, y 750 to 820; CLOSE_35_B x 428 to 702, y 786 to 882). Nothing is a void.
- **Whose:** the builder.
- **Exact fix:** the slate to (66, 76, 70), as the builder already says (lesson 35); the chiller's plinth faced in the body's white laminate or in stainless (sRGB 150 or more), with its dark joint to the floor 15 mm or less. Re-render the pictures with point 3.

### 8. PIC-05g has almost no margin at CLOSE_35_B by day (0.0098 against 0.01)

- **Where:** the near tray and its ice at the frame's lower left (x 181 to 667, y 1328 to 1439, 10,273 px) and the stand-in glass's sky reflection at the top of a light (x 1371 to 1469, y 0 to 110, 5,368 px). I repeated the count: 0.0051 and 0.0098 by day, 0.0021 and 0.0030 at night.
- **Whose:** the builder.
- **Exact fix:** after fault 1's fix, re-measure; if the share passes 0.01, tone the trays' white from (210, 212, 208) to (200, 202, 198) rather than greying the ice. The sky reflection is the stand-in glass's, not the shop's.

### 9. The chiller reads as a white kitchen counter

- **Where:** CLOSE_35 day x 1470 to 2160, y 580 to 800; the room pictures. A white base unit with a 0.2 m glass strip; its eight trays cannot be seen (the builder's named shortfall F8).
- **Whose:** the builder.
- **Exact fix:** with the fish: a serve-over front, the glass from z 0.80 to 1.20 sloping 25 degrees toward the room, the trays raked 10 degrees toward the street, so the card's camera (an 11 degree sight line) sees them. The chiller's depth stays 0.60 (the stand-off rule).

### 10. The floor just behind the display is a flat dark band by day

- **Where:** CLOSE_35 day x 1824 to 2432, y 864 to 1088 (92 blocks of 32 px with a deviation under 1 level, luma 42); CLOSE_35_B day x 800 to 1312, y 800 to 992 (luma 40). The quarry tiles show in the picture but are lost at the day card's 0.15. It is not black and not a board.
- **Whose:** the builder.
- **Exact fix:** grout (150, 140, 130) against the red tile, 20 mm as the target says (5.2), so the joints show at the day brightness. Re-render with point 3.

### 11. The wall clock hangs over the price chart (the room picture)

- **Where:** fishmonger_day.png about x 3590 to 3790, y 330 to 600: the clock covers the chart's "AT 2.60" column. It cannot be seen from either close camera.
- **Whose:** the builder.
- **Exact fix:** move the chart 0.30 m along the right wall toward the street, so the two outlines are at least 50 mm apart; add to SO-07 a check that no two flat-hung things overlap as seen from the card's camera.

### 12. Two check rows say less than they seem

- **DSP-05** measured "0 thin sheets": the fourteen tickets are one mesh, so the lean test never sees them. Split the tickets mesh into its cards before the principal-axes test (kit). I measured them myself: each top is 2.6 mm further from the glass than its foot (6 degrees back), which is right.
- **MANIFEST-fish_market.json**'s "what" text is Rita's ("rebuilt by build_ritas.py"). Write the shop's own line.

## Shared, known

- (a) the stand-in lamp's pool as a burnt bar in the night glass: **not present** (GLS-04: largest patch 3 px at CLOSE_35 and 1 px at CLOSE_35_B, repeated).
- (b) hot top corners in night_dark: not in this view (no close night_dark frame); PIC-03 reads 5.4 and 5.8.
- (c) glass parts of models dropped: **not present** (the clock keeps its glass; the lemon and the hose have none).
- (e) sheets leaning toward the glass: **not present** (the tickets lean back 6 degrees); the check gap is narrow point 12.
- (f) CLOSED on the door at night: the night_lit frames show OPEN, as the kit's rule for a lit state now says. The shop's real night (night_dark) is the street view's.
- (g) shrunken furniture, chairs, nets: **not present** (no furniture; the lemons are at 1.0).

## The builder's named shortfalls

| shortfall | my call |
|---|---|
| No fish | **Pending, not failed.** No stand-in of any kind exists (the display glb's meshes listed above). Without fish the window reads as a fishmonger's only by its glass lettering, tiled room and tickets; the slab itself would read as an emptied fishmonger's slab once the ice reads as ice. |
| The ice reads as blue-grey shards | **FAULT** (fault 1). |
| The chiller's trays hard to see in the day picture | Narrow (point 9). |
| LIT-02b at STREET_30 by day 0.0099 | The street view's; the blackboard is the same fix as narrow point 7. |
| PIC-05g at CLOSE_35_B by day 0.0098 | Narrow: a real pass, repeated (point 8). |
| Slab, ice bed and back panel as `support` pieces | Right: they are what the goods stand on. |
| Printed chart and tickets drawn by script; CC0 printed pictures owed | Narrow and owed: they read at this distance; the blackboard's "chalk" is a clean typeface and should break and smudge like chalk when the room is re-rendered. |
| 66 tins and jars (the target counts 24) | Right: 24 would be a gap on a 3 m shelf. |
| 48 samples | Owed (128 on the PC); picture noise reads 0.39. |

## Measured

**The parallax** (the game's `trace`, imported; card x 9.35 to 14.65, y 5.875, bottom 0.65; eyes 11.925 and 13.925, 3.755, 1.70):
- The card's centre samples the picture 1387.3 px apart between the two cameras: PRJ-02 confirmed.
- Three back-wall points (the hose's centre, picture (2488, 973); a jar on the lower shelf, (1500, 600); the cold-room door's lever, (2944, 1011)): each lands 656.7 card px apart between CLOSE_35 and CLOSE_35_B, 1.360 m on the card for 2.0 m of eye travel (2.0 x 4.5 / 6.62 = 1.360); `trace` sends each card point back to its picture pixel exactly.
- In the gate's baked day cards, each CLOSE_35 patch is found in the CLOSE_35_B card at offset (0, 0), correlation 0.980, 0.989 and 0.998; the picture's own patch (scaled 0.370) is found in both cards at (0, 0) or (0, 1), correlation 0.94 to 0.99. PRJ-03 confirmed.

**The glass** (the glass mask; luma):

| | CLOSE_35 day | CLOSE_35 night_lit | CLOSE_35_B day | CLOSE_35_B night_lit |
|---|---|---|---|---|
| whole glass, gate frame (stand-in reflection) | 85.6 | 85.3 | 87.9 | 85.4 |
| whole glass, reflection off | 76.6 | 87.4 | 76.1 | 87.4 |
| where the room shows, reflection off (floor: day 33, night_lit 45) | 48.9 | 68.4 | 48.0 | 66.2 |
| where the display shows, reflection off | 156.8 | 152.3 | 158.3 | 155.1 |
| under luma 12, reflection off (LIT-02b) | 0.0094 | 0.0105 | 0.0099 | 0.0105 |
| under luma 5, gate frame (pure black) | 0.0000 | 0.0005 | 0.0000 | 0.0002 |
| any channel at 250 or more, whole frame (PIC-05g) | 0.0051 | 0.0021 | 0.0098 | 0.0030 |

- The night's under-12 pixels are the dark inner sill under the bed, not the room (the room's share is 0.0011, as the check says).
- **The wall beside the glass:** the shop is dark at night by the target, so night_lit is a test state. In it the glass (85) is brighter than everything beside it: brick 18.9, pilaster 39.9, stallriser tiles 51.4 (CLOSE_35); side door 5.5, pilaster 17.9, stallriser 51.9 (CLOSE_35_B). By day the room reads (48 to 55) behind a bright display (157 to 184), as a shop window does.
- **Flat tones:** the largest flat patches in the glass are the floor behind the display by day (narrow point 10) and the painted ceiling at night (luma 32 to 44, top 250 px). There is no void and no white board.
- **The night glass:** |frame minus reflection off| p95 9.1 and 9.9, means 2.4 and 2.3; 10 and 1 px are 40 or more levels brighter. GLS-03 and GLS-04 repeated exactly.

**The export faults of Rita's shop:**
- **A height map as a normal map:** none. The lemon's map averages (127, 127, 248), with blue at 160 or more on every pixel; the fascia's is GLB-01's.
- **A textured primitive without UVs:** none (10 textured primitives in the display glb, 8 in the front glb; none without TEXCOORD_0, no negative texCoord).
- **Two parts in one plane, black strips:** none at close range. Under luma 8 there are only the side door's black knob (CLOSE_35_B x 2350 to 2364, y 841 to 860), the hose's coil and the blackboard. The jambs beside both doors are clean.
- **A see-through slot:** none. FRN-08 reads 0 px at both close cameras, and no frame shows one.
- **The stand-in night light seen as an arc or a burn:** no.

**Every legible word at 100 per cent** (both cameras, day and night):

| where | word | acceptable? |
|---|---|---|
| glass rows | SHELLFISH, SMOKED FISH, FRESH DAILY | yes; SMOKED reads "SHOKED" from CLOSE_35 (narrow 6) |
| door | OPEN; MON-SAT 7.30-2, WED 7.30-1, SUN CLOSED | yes, and they match the target's hours |
| fanlight | 3 | yes |
| tickets | COD 2.60 lb, PLAICE 2.90 lb, HADDOCK 2.45 lb, LEMONS 8p each (the rest are too small or turned away; the atlas also holds KIPPERS, WHITING, SKATE, HERRING, MACKEREL, CRAB, PRAWNS, COCKLES 1.00 pt, SMOKED COD, ICE FREE) | yes |
| blackboard | the prices 2.60 lb, 2.45 lb, 2.90 lb, 1.80 lb (the names are behind a mullion from CLOSE_35) | yes |

- **Nothing else is legible in the close frames:** not the tins, not the clock, not the price chart.
- **In the 4096 room picture at 100 per cent:** PILCHARDS, SARDINES, PASTE, TIDEMARK (in part), PRICE CHART, TODAY'S FISH. Also "ENWICK", a real firm's name (narrow point 1).
- **No mark on any model:** I read the display glb's lemon map at 100 per cent, and the clock and hose in the room picture. No maker's mark, sticker or modern mark is on any of them.

**The content rule holds** apart from narrow point 1:
- no drink, gambling, child, toy or weapon;
- nothing after 1992: no barcode, no plastic modern packaging;
- tinned fish and pastes only on the shelf.

## Which check rows I trust

- **Repeated or confirmed:** PRJ-02, PRJ-03 (three points), GLS-03, GLS-04, PIC-05g, LIT-02b's close numbers, FRN-10's pixel half, FAS-03, GLB-01 (the lemon's map), DSP-06 (the lemons at real size), DSP-07, X-NOISE (not repeated, consistent with the pictures), and MANIFEST (six of six sha256 match).
- **Trusted as worded, not repeated:** DSP-03 (nothing intersects; it agrees with every crop), SO-01 to SO-07, PIC-01 to PIC-06, FRN-01 to FRN-09, CAM-01.
- **The cloud's stand-ins, proving the gate and not the game:**
  - LIT-05, LIT-07 and LIT-08: the 80 W spill;
  - GLS-05: the gate's own glass;
  - LIT-01 and LIT-02: composites at the game's brightness values, but no Lumen;
  - PIC-05g's sky reflection;
  - PRJ-02: the gate's bake.
- **Rows that pass without measuring what their name says:**
  - DSP-05: the tickets go unmeasured (narrow 12).
  - INV-05 and NEV-01: no row checks invented maker names against real firms (narrow 1).
  - TRD-01 passes on trays and tickets: it measures size, not whether the goods read as the trade's (fault 1).
  - Nothing checks the wall tile's size against the target (narrow 3), or the pose of a placed model (narrow 2).
- **Pending, not failed:** SCN-01 and SCN-02.

## What is right

- **The projected room is the game's rule, pixel for pixel,** and reads as a deep, lit room. The shelf, the hose, the cold-room door and the blackboard move apart correctly between the two cameras.
  - There is no black slab and no end of the picture at either camera.
  - The display's white back panel meets the room's floor with no seam.
- **The near metre is clean in build:**
  - nothing intersects, nothing is buried, nothing floats as a group;
  - every piece is at real size, and the lemons are true scans;
  - the trays, slab and lip are where the target puts them, every tray and lemon in a light clear of the mullions.
- **The doors at close range match the target:**
  - The M1 aluminium door: glass from 198, the letter plate in the bottom rail, the chrome pull bar on the lever stile.
  - The green OPEN card on its cup, with the painted hours under it, and the 3 on the fanlight.
  - The dark F1 side door with its letter plate, knob and keyhole.
  - The jambs: no black strip anywhere.
- **The awning:** its rail meets its arm at the window end from CLOSE_35.
- **The glass and the night:**
  - no doubling, no burnt bar, no arc;
  - the display is lit at night without burning (LIT-08's lowest ratio is the lemons at 1.68), and the room behind is lit and readable.
- **The content rule holds,** except FENWICK. No fish was made by hand: the 3 October failure is not repeated.
- **The manifest names exactly the files reviewed.**

## What I cannot judge from the files

- **The fish** (pending; Sketchfab scans): whether the slab reads as a fishmonger's with them, and the tickets' final places.
- **The game's own light and image:** the glass's reflections and its Fresnel hand-over, Lumen's light on the display (and so whether the white trays and ice burn under the real spill), the exposure, the card under TSR, and the frame time.
- **The shop's real night at close range.** There is no close night_dark frame; the dark shop's night is the street view's.
- **The bell.** It hangs behind the door's top rail, which neither close camera frames clearly.
- **Wear, grime and wet,** which come from the game's own layers.
- **Measurements I could not repeat:**
  - LIT-02's room-only composite (I used the reflection-off frames instead);
  - LIT-08's per-piece ratios;
  - DSP-03's silhouette shares;
  - TRD-01;
  - FRN-10's coplanar-face geometry test;
  - GLS-05.
