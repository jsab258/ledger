FAIL

# The tea rooms (west_north bay 2, no. 14), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. I judged the street view only (STREET_SQUARE and STREET_30, day and night_lit). I did not read the close review of this shop or any other shop's review. Jafar's ruling of 9 October applies: a piece that fails only on narrow points passes, with the points listed for the builder.

**What I read:** CLAUDE.md; RULINGS.md (1, 2, 3, 8 October); NOTES.md ("For the next nine shops", Batch A's opening, the tea rooms' section, "For the next shops"); TARGET.md section 3, section 5.7, section 8 (D5) and section 13 with batch A's A10, A11 and A14; target.json `shops[tea_rooms]`; Rita's four reviews; `checks/check_tea_rooms_v1.json` (all 64 rows); `MANIFEST-tea_rooms.json`; the 4.1 manifest's entries for this shop; the scratch folder's `blanking_report.json`, `display_items.json`, `front_members.json`, `rooms/texts.json`.

**What I looked at:**
- The previews `tea_rooms-street-square-{day,night-lit}-2026-10-13.jpg` (they match the gate frames: mean difference 1.9 and 1.1 levels after resizing) and the room night_dark preview.
- The four gate frames (13 October, 23:14 to 23:29): STREET_SQUARE and STREET_30, day and night_lit, 2560 x 1440, whole and in crops at 2x to 8x.
- Rita's v3 street preview and the Hook sheet.
- Every base-colour map of the 14 placed models at 100 per cent, region by region (item d below); the 21 images inside `tea_rooms_display.glb` and the 5 inside `tea_rooms_front.glb`; the room's menu and notice pictures.

**What I measured:**
- My own projection of the front's members (`front_members.json`) through each gate camera's file. The glass rectangles land on the frame's panes to the pixel. Luma is Rec.709 on the sRGB values, 0 to 255.
- Glass, curtains, brick, fascia, number, stallriser, mullion fronts and pavement; dark, burnt and flat patches.
- Both glbs' JSON: UVs, normal maps, node bounds and scales; the seat and top heights of the chair and table models from their vertices.
- The manifest's hashes: the two glbs and three room pictures in the asset folder are the ones the manifest names.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview). "u" is the display's distance along the window from its centre (the glb's x), "w" the height above the bed, "v" the depth behind the glass.

**Verdict: one fault blocks.** The window's table and chairs are at children's sizes under a full-size tea set, so the window's centrepiece reads as a doll's tea table. The front, the lettering, the glass and the lit room are good. Seven narrow points follow, each with an exact fix.

## Faults, worst first

### F1. The window's table and chairs are children's furniture under full-size china

- **Where:**
  - STREET_SQUARE day and night: the middle light, x 1150 to 1415, y 750 to 925 (1600: x 719 to 884, y 469 to 578).
  - STREET_30 day and night: x 1190 to 1360, y 755 to 890.
- **What it looks like:**
  - The table's top stands level with the shop door's lever (y 810 to 860 at STREET_SQUARE), although the bed is 0.60 m above the footway.
  - The teapot is a third of the table's height.
  - The chairs' seats are at the curtains' hems.
  - From the far pavement the set reads as a doll's or a child's tea party in the window, not a café table laid for two. With "no children" in the content rule, child-size furniture is the wrong thing to show.
- **Measured** (from `display_items.json`, the display glb's nodes and the models' vertices):
  - `round_wooden_table_02` is scaled 0.628 on every axis. Its 0.80 m top becomes 0.50 m, which is what the builder meant. But its 0.746 m height becomes **0.468 m**, the height of a child's table. A café table is 0.72 to 0.76 m.
  - Both `painted_wooden_chair_01` are at 0.75. The 0.956 m chair becomes 0.717 m, and its seat drops from 0.43 m to **0.33 m**, a child's seat height. An adult's chair seat is 0.42 to 0.47 m.
  - The teapot, cups, saucers, sugar bowl and menu stand are at 1.0.
  - NOTES T7 names the table's 0.50 m top and the chairs' 0.75, but not the heights they cause.
  - The target's own zones assume a full-height table: the tea set's zone starts at w 0.75. The target's note "scaled to a 0.55 m cafe table (the model is 0.80)" is ambiguous, because a uniform scale also lowers the table.
  - No check covers it: SO-06 measures the room's models only. DSP-03 and TRD-01 pass, because they prove the pieces are seen, not that they are the right size.
- **WHOSE:** the builder (the uniform scales). The target's note is to be reworded. The kit lacks a display scale check.
- **EXACT FIX:**
  1. **Table:** scale `round_wooden_table_02` by (0.628, 1.0, 0.628) in glTF axes (x, y up, z). The top stays 0.50 m across, and its top is at w 0.746.
     - The laminate disc moves to w 0.746 to 0.758.
     - Raise the teapot and lid, both cups and saucers, the sugar bowl and the menu stand by 0.277 m, so they stand on w 0.758.
  2. **Chairs:** set both `painted_wooden_chair_01` to scale 1.0 (0.956 m high, seat 0.43 m).
     - Keep them turned as now, backs outward.
     - The left chair runs from u -0.76 to -0.22, the right from 0.22 to 0.76.
     - Both run from v 0.105 to 0.535 (centre z -0.32). That keeps them behind the curtain rods' plane (v 0.078) and inside the 0.55 bed.
     - The seat fronts tuck under the 0.25 m radius of the table's top, at least 80 mm clear of the scaled pedestal and feet (u ±0.14).
     - If DSP-03 finds a contact, move each chair 0.04 m outward. Their outer ends then stand behind the café curtains, as chairs do in a café window.
  3. **Target note** (section 5.7 and target.json `display.items[round_wooden_table_02].note`): "the top scaled to 0.50 m across (0.55 touched the glass); the height stays the model's 0.746".
  4. **New check DSP-05:**
     - Every display model is at 0.9 to 1.1 of its real height, each exception named.
     - Furniture is at its standard heights: a café table's top 0.72 to 0.76 m, a chair's seat 0.42 to 0.47 m.
     - SO-06's 0.6 floor stays for the room's goods only.
  5. Re-run DSP-01, DSP-03, DSP-04 and TRD-01, and re-render the four street frames.
  6. **Acceptance:** at STREET_SQUARE by day the table's top projects above the door's lever (1.35 against 1.0 m above the footway).

## Narrow points, each with its exact fix

### N1. At night the door says CLOSED while the shop is lit, set and open

- **Where:**
  - STREET_SQUARE night: the red CLOSED card on the shop door's upper pane, x 752 to 797, y 707 to 730 (1600: x 470 to 498, y 442 to 456).
  - STREET_30 night: the same card.
- **Why it matters:** the target lights this shop at night because it is open: hours 6:30 to 22:00, and "night_lit: three battens on ... open to 22:00". The table is laid and the urn is on. The gate swaps the glb's OPEN for CLOSED in every night frame, which is Rita's rule (lit, but shut). The target's door rule is "closed when the shop is shut".
- **WHOSE:** the builder (the gate's night sign rule) and the kit.
- **EXACT FIX:**
  1. The door sign follows the shop's hours, not day and night. A shop that is lit at night because it is open past the night view's hour (`lit_at_night` true and closing after 20:00: the tea rooms) shows OPEN in night_lit, and CLOSED only in night_dark.
  2. A shop lit at night but shut (Rita's) keeps CLOSED.
  3. Write the rule into the kit (`sw_gate.py`, the night sign swap) and into "For the next shops".
  4. Add a PC row: the game's door sign follows the hours at the hour shown.

### N2. The hours card is missing from the shop door

- **Where:** STREET_SQUARE day, the door's lower pane, x 700 to 847, y 745 to 862: clear glass. Rita's approved front carries its hours plate under the OPEN sign.
- **Why it matters:**
  - The target (door.sign) asks for "the hours plate (4.1) on the glass beside it".
  - 4.1 drew it: `hours_plate.tea_rooms`, a 300 x 190 card in marker pen, "MON-SAT 6.30 AM - 10 PM / SUN 8 AM - 12 NOON".
  - The front glb carries only five images, and that card is not among them.
  - From the street its words cannot be read (17.5 mm caps are 4 px), but a white card taped under the sign is one of the details that say "a working shop".
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Place 4.1's `hours_tea_rooms_basecolour/_orm/_height` as a 300 x 190 card inside the door's lower pane: centred at u 1797, its top at z 1380 above the footway (37 mm under the glazing bar), d 38 (behind the glass, as GLS-01 allows).
  2. Taped corners, no frame.
  3. FRN-03 gains a line: the hours card is present and at its place.

### N3. The café curtains' folds are a regular corrugation, and at night they are an opaque grey band

- **Where:** STREET_SQUARE day and night, the left light x 905 to 1140 and the right light x 1420 to 1655, y 722 to 854 (1600: y 451 to 534).
- **By day:**
  - Every fold has the same pitch and depth, and the scallops repeat exactly.
  - At 100 per cent the panels read as a corrugated sheet or a radiator more than as gathered cotton.
- **At night:**
  - The curtain band measures 50.2 (left) and 50.0 (right). The room above it measures 102.9 and 68.4: ratios of 0.49 and 0.73.
  - A lit café's cotton half-curtains glow from behind. Here they read as dull grey boards across the lower half of a lit window. This is the shop's main night picture.
- **WHOSE:** the builder (`script:cafe_curtain`).
- **EXACT FIX:**
  1. **Folds:**
     - Draw each fold's pitch from 55 to 95 mm and its depth from 12 to 28 mm (seeded).
     - Let the hem's scallops follow the folds.
     - Give each panel a 3 to 8 mm sag between its rings.
  2. **Cloth:**
     - Mix a Translucent BSDF at 0.25 into the cotton, so the room's battens light it from behind.
     - In the game, the same through a two-sided foliage (subsurface) shading model, subsurface colour the cloth's cream.
  3. **Acceptance:** at STREET_SQUARE night_lit the curtain band is at least 0.8 of the room above it in each light. PIC-05g must still pass.

### N4. The brown dado behind the table is a flat field

- **Where:**
  - STREET_SQUARE: the back wall between the counter's end and the hatch (room x 0.45 to 1.2, z 0 to 1.1), seen behind the teapot and chairs.
  - The largest patch of 9 x 9 windows with a standard deviation under 1:
    - **3.98 per cent of the glass** by day, x 1211 to 1391, y 694 to 832, luma 26.6;
    - 3.65 per cent at night, luma 46.8.
  - STREET_30: 5.48 per cent by day (x 1195 to 1359, y 697 to 815) and 5.49 per cent at night.
  - Rita's passing try 2 measured 2.4 and 2.7 per cent.
- **What it is:**
  - Not a void: it is dark-brown paint, honestly lit. But it is the largest textureless area in the window.
  - It also swallows the dark walnut pedestal (LIT-08).
- **WHOSE:** the builder (the room).
- **EXACT FIX:**
  1. Make the back wall's dado (z 0 to 1.1, the whole width the counter does not cover) vertical matchboard, the 1980s café's own dado:
     - boards 89 mm wide;
     - V-joints 3 mm wide at 0.6 of the paint's value;
     - the plaster map's grain at 0.3;
     - a 45 mm dado rail at z 1.10 in the same brown (120, 74, 44).
  2. **Acceptance:** the largest flat patch is at most 2.5 per cent of the glass at both street cameras, day and night.

### N5. Two price tickets stand at the chairs' feet

- **Where:** STREET_SQUARE day, x 1173 to 1190 and x 1347 to 1363, y 905 to 917: `price_card_3` (u -0.46 to -0.39) and `price_card_1` (u 0.29 to 0.36), each in front of a chair's legs.
- **Why it matters:** from the street they read as tickets on the chairs, which is how a second-hand furniture shop prices its window. The other two tickets stand by the cakes, as they should.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Move `price_card_3` to u -1.58 to -1.51 (left of the carrot cake's stand).
  2. Move `price_card_1` to u 0.70 to 0.77 (left of the strawberry cake's plate).
  3. Keep no ticket within 0.10 m of a chair or the table.
  4. DSP-04 still passes: the chairs and the table fill the bed's middle.

### N6. The window table is a Victorian walnut occasional table, not the research's Formica café table

- **Where:** STREET_SQUARE day, the pedestal, x 1255 to 1305, y 822 to 898. It is a panelled box with burr-walnut panels on four splayed legs. From the street it reads as a plant stand under a pale disc.
- **Why it matters:**
  - The target's research keeps "Formica tables". Its notes say "a 1980s caff". It chose `round_wooden_table_02` and asked only that "a laminate top replaces the wood".
  - It is also the one piece that fails LIT-08.
- **WHOSE:** the target.
- **EXACT FIX:**
  1. Extend the note: "a laminate top and a black cast-iron-look base replace the walnut".
  2. Pedestal and legs base colour sRGB (28, 28, 30), roughness 0.5, metallic 0.
  3. Keep the laminate (160, 142, 106) top.
  4. LIT-08 then measures the table by its top (see N7).

### N7. LIT-08 measures a table's base as if it were goods

- **What it is:**
  - LIT-08 fails on one piece: the walnut pedestal reads 0.28 (CLOSE_35) and 0.21 (CLOSE_35_B) of the room behind it.
  - From the street at night the pedestal reads as dark wood under a lit top, which is what dark wood does under a lamp above it (STREET_SQUARE night x 1255 to 1305, y 822 to 898).
  - The row was written for Rita's black goods on tiers, which must read at night. A table's base is furniture under a lit top, not goods.
- **WHOSE:** the check.
- **EXACT FIX:**
  1. LIT-08 measures furniture (tables, chairs, stands) by its top surface only, and names those pieces in the row.
  2. The rest of the row is unchanged.
  3. The builder's two tries on the pedestal can stop there.

## Shared, known (from the gate and the kit; not this shop's verdict)

- **(a), seen.** At STREET_30 night an orange bar runs across the right light under the curtain's hem: x 1385 to 1535, y 822 to 858, RGB (146, 81, 22), luma 87 to 91, no channel at 250. The reflected ray from the STREET_30 eye through that glass meets the far pavement about 8 m along the street. This is the gate's stand-in lamp's pool mirrored in the glass. GLS-03's one failing frame (STREET_30, p95 16.7) is very likely this. It is not seen at STREET_SQUARE.
- **(b), seen.** The room's night_dark picture has hot orange top corners (the preview's top left and top right). The shop is lit at night, so night_dark is not in any street frame.
- **(c), not seen from the street.** The till's readout glass, the clock's glass and the frames' glass are too small at 8.76 m to show whether they were dropped. That is for the close view.
- **(e), not seen.** The window card hangs flat on the glass's inside on its two cups, and the menu board and the price tickets stand square. Nothing leans toward the glass and nothing hides goods.

## (d) Maker's marks: every placed model's base colour at 100 per cent

I read each map at 100 per cent, region by region, and zoomed 2x to 8x on every printed area, comparing each with its original where the builder cleaned it. **No legible maker's mark, firm or place name survives on any of the 14 models.**

| model | maps read | what is there |
|---|---|---|
| CashRegister_01 | `_diff_1k_clean`, `_glass_diff_1k` | The cleaned plate, banknote, slogans and receipts are gone. What is left is generic: key numerals, TOTAL, X Y Z, A B R, a digit strip "0 2 1 3 7 7 0". Two faint printed roundels (map x 140 to 250, y 45 to 125 and x 767 to 832, y 270 to 330) and five 4-letter key labels at the right edge (x 982 to 1002, y 245 to 395) cannot be read even at 8x, and in the room picture they are a few pixels. Acceptable. The glass map is dust only |
| wall_clock | `_diff_1k_clean` | URBAN / quartz is gone. A 2-pixel dash is left where the U was; it cannot be read. Plain 1 to 12 numerals |
| vintage_electric_kettle | `_diff_1k` | The dial reads THERMOMETER, °F, °C and the numbers: no maker. Acceptable |
| tea_set_01 | `_diff_1k` | Floral transfers and gold rings; every base disc is plain, with no backstamp |
| hanging_picture_frame_01, _02, _03 | frame maps and `_artwork_diff_1k_clean` | 01 and 03 carry the same invented sailing print; 02 carries the Lake Pier harbour crop (CC0) in a white mount. Its two pier signs are blank, and no place is named. The original painting and photograph are gone |
| carrot_cake, strawberry_chocolate_cake, hamburger_buns, metal_jug, painted_wooden_chair_01, potted_plant_04, round_wooden_table_02 | `_diff_1k` | No print of any kind |

The display glb's own images (its 512 px copies of the six display models' maps, the menu stand, the price cards and the window card) carry only the project's words. The front glb's images are the 4.1 board, its normal and ORM maps, the 14 and the OPEN sign.

## The builder's named shortfalls, judged from the street

| shortfall (NOTES, check file) | my judgement |
|---|---|
| the room is sparse: no tables in the picture, a serving room rather than a dining room | **narrow, the target's (the method's limit):** free tables smeared, so they are only in the window. From the street the counter, urn, cups and menu board say café. No fix in the card; tables in a walked room are the PC's |
| two cake domes; the plates as scripts; the table 0.50 m, not 0.55 | the domes and plates are **not points from the street**. The 0.50 m top is right, **but the scale behind it is fault F1** |
| no steamed glass | **owed to the PC**, not a point |
| the window card's and the menu board's lettering are the project's own | **right as it is**: both read and both are fictional |
| the whites and the bed toned for the night gate | **not a point**: the china and curtains read white and the chairs pale grey from the street |
| LIT-08 fails on the walnut pedestal | **narrow, the check's (N7)**. The table's base is also N6, the target's |
| GLS-03 fails at STREET_30 (16.7) | **shared, known (a)**: the far pavement's stand-in pool mirrored in the lower right light |
| night_dark's wash 70 per cent stronger (mean 23) | **not seen from the street** (the shop is lit at night). PIC-03 passes; (b) is the kit's |
| the stand-in lamps out of glossy rays; the spill at 150 W | **gate stand-ins**: not a point |
| 48 samples | **narrow, owed**: no noise shows at street distance; 128 on the PC |

## What is right

**The front:**
- It reads at once as a timber shopfront in a Victorian parade, kept by a 1980s caff:
  - fluted brown pilasters on plinths, with capital blocks;
  - scroll consoles with leaf carving;
  - a timber cornice;
  - the brown acrylic panel in a white timber frame over the old cream board, whose flaking ends show beside the consoles;
  - the rendered stallriser and the sill;
  - a 3L-6T window with the mullions carried up;
  - the band over both doors (the fielded panel over the side door, three toplights over the shop door, the transom and the head).
- Proportions and colours sit beside Rita's approved front and the Hook sheet's painted fronts.
- Nothing floats, nothing is mirrored, and no text reads backwards.

**The doors:**
- The shop door has its lever on the viewer's left and hinges on the right. The brass kick plate, the letter plate in the lock rail and the bell on the top rail all show through the glass.
- The dark-brown side door has its centre knob and its vertical letter plate.
- The side door's fanlight shows a dark hall, not the shop (FRN-09).

**Lettering:**

| what | STREET_SQUARE | STREET_30 |
|---|---|---|
| fascia by day: ground / letters (p75) / ratio | 68.7 / 183.8 / 2.68 | 74.7 / 185.8 / 2.49 |
| fascia at night: ground / letters (p75) / ratio | 18.7 / 58.0 / 3.10 | 18.7 / 58.0 / 3.10 |
| the 14 by day: fanlight / figures | 50.5 / 193.9 | 71.8 / 211.6 |
| the 14 at night: lit fanlight / dark figures | 65.4 / 26.1 | 111.0 / 49.3 |

- The fascia's painted letters keep reading at night; Rita's gilt letters went dark.
- At night the 14 reads as dark figures against the lit fanlight.
- No bar crosses a letter (GLS-02).

**The glass and the room** (my glass rectangles, eroded 3 px: the three lights and six toplights):

| measure | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, glass mean | 89.1 (p5 26, p95 194) | 89.0 (p5 29, p95 193) |
| day, the room above the curtains: left, middle, right light | 66.5, 59.0, 89.3 | |
| day, brick beside (left, right) | 84.4, 84.1 | 84.1, 85.3 |
| day, under 3 / under 12 / any channel at 250 | 0 / 0.02% / 0 | 0 / 0.02% / 0 |
| night, glass mean | 71.2 (p5 35, p95 139) | 67.6 (p5 38, p95 113) |
| night, brick beside (left, right) | 16.4, 19.3 | 16.5, 19.5 |
| night, window against wall | 3.7 to 4.3 times | 3.5 to 4.1 times |
| night, under 3 / under 12 / any channel at 250 | 0.02% / 0.64% / 0.28% | 0 / 0.59% / 0.30% |
| night, largest dark patch (under 12) | 0.26% | 0.20% |
| largest flat patch, day / night | 3.98% / 3.65% (the dado: N4) | 5.48% / 5.49% (N4) |

- By day the room reads dimmer than the wall in the left and middle lights (0.70 to 0.79 of the brick), as D5 asks. Only the white window card and the hatch lift the right light to the wall's level.
- At night the room is lit and about four times the wall. There is no void and no white board.
- The burnt pixels at night number 962 at STREET_SQUARE: 0.03 per cent of the frame, in line with PIC-05g's 0.0003. The largest are the teapot's top (342 px) and the table's laminate in the spill (160 px); the rest are small highlights on the china and the strawberries.

**The trade reads from the street:**
- the fascia and the window card;
- a table laid for tea (at the wrong size: F1);
- cakes at both ends of the bed;
- behind them a counter with cups on two shelves, a kettle, a mechanical till, a tea urn, a chalk menu and a serving hatch with its roller half down.

**Period:**
- a chalk menu at 1990 prices (TEA 25p, COFFEE 35p, TOAST 30p);
- a tea urn, a mechanical till, T12 battens and a cream-and-brown chequer floor;
- nothing after 1992: no barcode, no screen, no plastic packaging.

**Content:**
- No drink, gambling, tobacco or person is shown, and no firm's name or mark.
- Every word legible at 100 per cent in the four frames is the project's own and acceptable:
  - BREAKFASTS, LUNCHES & TEAS and Tea Rooms (fascia);
  - 14 (fanlight);
  - OPEN by day, CLOSED at night (door; see N1);
  - BREAKFASTS / LUNCHES / TEAS (window card);
  - TODAY'S MENU / TEA 25p / COFFEE 35p / TOAST 30p (the menu board, just legible).
- The price tickets, the menu stand's card, the notices and the till's keys cannot be read from the street. Read in their source pictures, they are all fictional words and prices: TEAS FROM 25p, CAKES 40p, TOAST 30p, HOME MADE, TABLES BOOKED, OPEN 6.30 - 10, CAKES MADE HERE, THANK YOU, LUNCH 12 - 2, EGG & CHIPS £1.80, SOUP 65p, TEACAKE 40p.

**Rita's export faults, none repeated here:**
- **Height map as normal map:** none. The fascia's normal is a real map (mean 127.5, 127.5, 255); the six display normal maps have blue means of 236 to 254.
- **Textured primitives without UVs:** none (4 in the front, 20 in the display, all with TEXCOORD_0).
- **Coplanar black strips:** none. My count of front pixels under luma 8 by day is 305 at STREET_SQUARE and 297 at STREET_30. All are the 4-pixel shade lines under the cornice's end blocks (x 351 to 404 and 1692 to 1746, y 275 to 279) and, at STREET_30, the side door's iron knob. This agrees with FRN-10.
- **See-through slot at STREET_30:** none. Both ends show brick, by day and by night.
- **Stand-in night light or glass visible:** none. The head band is clean and the mullions do not glow. The toplights show the three battens once each, with no ghosts.

## The check rows: which I trust

- **Trusted, measured on the real pictures, meshes or files (45):**
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-04, SO-07;
  - DSP-01, DSP-02, DSP-04;
  - ROOM-01, ROOM-02, ROOM-05;
  - INV-01 to INV-06 (my own reading of every map agrees);
  - NEV-02, GLB-01;
  - FRN-01, FRN-02, FRN-04, FRN-05, FRN-07, FRN-08, FRN-09, FRN-10 (my dark count agrees);
  - FAS-01, FAS-01n, FAS-01c (my ratio 2.68 against its 2.54), FAS-03;
  - GLS-01, GLS-02, LIT-06, CAM-01, X-PRV.
- **Pass but do not prove what they say (5):**
  - SO-06 measures the room only; the display's 0.628 and 0.75 are outside it (F1).
  - DSP-03 and TRD-01 prove the table set is seen, not that it is the right size (F1).
  - NEV-01 reads names only; it cannot see a child-size set (F1).
  - FRN-03 does not look for the hours card (N2).
- **The cloud's stand-ins only (9):**
  - LIT-01 and LIT-02 are the card's composite alone.
  - LIT-02b, LIT-05, LIT-07 and PIC-05g are measured on gate renders, whose glass, lamps and spill are stand-ins. My own night frame numbers agree with PIC-05g.
  - PRJ-02 is the gate's own `trace`.
  - GLS-03 fails on the shared stand-in (a).
  - LIT-08 fails on the wrong measure (N7).
- **n/a (5):** SO-05, FRN-06, FAS-02, LIT-03, PRV-01, each rightly.

## What I could not repeat, and what I cannot judge

**Measurements I could not repeat:** the gate's check renders and the baked cards have been removed from the scratch folder. Only their camera files remain. So I could not repeat:
- GLS-03 (it needs the reflection-off renders);
- LIT-02b (the room-only and reflection-off renders);
- LIT-01 and LIT-02 (the card composites);
- LIT-05 on the check's own glass mask. My lower-glass mean at night is 72.1, on a different zone;
- FRN-08's backdrop renders;
- DSP-03's and TRD-01's object-index passes;
- PRJ-02 and PRJ-03 (the cards).

I did measure the following myself, on the frames and files that remain: the glass, the lettering, the burnt share, the dark and flat patches, FRN-10's dark count, and the glbs' maps, UVs and scales.

**What I cannot judge:**
- **The game's glass:** the street and sky in the panes, the dirt, the steam the research asks for, and the night hand-over.
  - In the gate the white curtains are the brightest thing on the front by day: 187 to 190, against 171 for the cream paint of the mullions and 84 for the brick. The gate lights cloth behind clear glass as brightly as paint outside.
  - Suggested PC row: by day from STREET_SQUARE the curtain band reads at most 0.9 of the outside cream paint. If it does not, it is a look decision for Jafar's page.
- **The game's light:** Lumen on the display, the game's spill and its pool on the pavement (the gate's footway reads 124 at night: a stand-in, PC-02), the lamps' pools and the exposure.
- **Wear:** the front is spotless; the Hook sheet's street is grimy and wet. The D53 layer is owed (PC-05).
- **Motion:** TSR, the card's parallax as the player walks, and the curtain's sway.
- **(c), the dropped glass parts:** the close view's.

**Next:**
1. Fix F1: the table's height, the chairs at real size, and DSP-05.
2. Then N1 to N5 (the builder's), N6 (the target's owner) and N7 (the check).
3. Re-render the four street frames and send them to try 2 of the street view.
