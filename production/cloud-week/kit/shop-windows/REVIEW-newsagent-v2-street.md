PASS

# The newsagent and tobacconist (west_north bay 0, no. 18), the STREET view: fresh review, try 2 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. This review judges the street view only: STREET_SQUARE and STREET_30, by day and at night. I did not read either close review of this shop. Jafar's ruling of 9 October applies: a piece that fails only on narrow points (each a small detail with an exact fix) passes, with the points listed for the builder. This is try 2 of this view; a third failure would set the shop aside.

**What I read:**
- CLAUDE.md, and RULINGS.md (1, 2, 3 and 9 October).
- NOTES.md: "For the next nine shops", the newsagent's batch A section, "Try 2 of the first three shops" and "Try 2 shared fixes".
- TARGET.md: section 3, the newsagent's table (5.9), and section 13 (batch A, and the 14 October rows T2-1 to T2-16).
- Rita's four reviews, and my own try 1 review (REVIEW-newsagent-v1-street.md).
- `checks/check_newsagent_v2.json` (78 rows counted, 77 pass, 5 n/a).
- The code behind what I saw: `sw_shops_news.py` (the back door, the jars, the racks), `sw_prints.py`, `sw_gen.py`, and `check_try3.py` (DSP-12, DSP-13).

**NOTES.md has no section "Try 2, newsagent"** (as of commit abf93c6, 04:11 on 15 October). There is a shared try 2 table and an ironmonger try 2 section, but no newsagent one. So the builder's own account of what it did for this shop, what it left and why, and any claim that a review was wrong, was not there to read. I judged the work from the target's T2 rows, the check file, the code and my own measurements (narrow point 7).

**What I looked at:**
- The v2 previews: street-square day, night-lit and night-dark; the three room pictures. The 13 October previews were open beside them.
- The gate frames rendered for try 2 (15 October, 02:55 to 03:32): STREET_SQUARE day, night_lit and night_dark, and STREET_30 day and night_lit, at full size and in crops up to 4 times.
- The Hook sheet.
- The three v2 street previews match these frames (mean difference 1.2 to 2.0 levels, which is JPEG noise).

**What I measured:**
- My own pinhole projection from the camera files (street z = height above the footway + 0.10; glass at y -5.255). It lands the mullion centres at x 1151.7 and 1408.3, and the glass mask's gaps at 1138 to 1164 and 1394 to 1420.
- Rec.709 luma, 0 to 255, over the three lights' glass (the gate's glass mask, and that mask eroded 14 px, about 60 mm), the brick either side, the shop door's panes and the box sign.
- Flat-patch search (9 px, sd under 1) and dark-patch search (under 12).
- The glass lettering's ink against its ground.
- The postcard rack's pole, by pixel row.
- The jars' saturation.
- The two glbs' JSON (normal maps, UVs, glass materials).
- The room pictures, where a street patch comes from.

Pixel boxes are in the 2560 x 1440 gate frames.

**Verdict.** No fault blocks.
- The front still reads, from the far pavement, as a 1990 newsagent and tobacconist in an old Victorian parade. It is unchanged from try 1, which passed it.
- The window is glass with a lit room behind it by day and by night.
- Try 1's three visible points are fixed or mostly fixed:
  - the magazine board's bare band is gone;
  - the postcard rack stands clear of the mullion on a pole that shows;
  - the back door is no longer a flat slab.
- The papers now look like folded papers, and no real title is left.
- Seven narrow points remain, each with an exact fix. Points 1 to 3 are what a player could notice.

## Try 1, item by item

| try 1 item | now | where and how measured |
|---|---|---|
| **1. The magazine board hid its top row; a bare grey band showed** | **FIXED** | STREET_SQUARE day, the middle light, x 1200 to 1395, y 812 to 915: three rows of four covers on the board's front face. All twelve mastheads show. Each upper row shows about two thirds of its height above the row below (top row about 103 px of a 155 px cover at 4x). The board shows about 3 px above the top row, about 13 mm (DSP-13: 14.4 mm, limit 20). |
| **2. The postcard rack's pole stood on the mullion's edge; cards clung to it or floated** | **FIXED** | STREET_SQUARE day: the pole is a light rod at x 1435 to 1436 (luma 78 to 101 against 35 to 45 round it). The mullion's edge is at 1419/1420, so 15.5 px clear (my projection: 1436.1 against 1416.9). STREET_30 day: the pole runs from the top tier down to the bed, x about 1352; the cards hang on it. The wire reads as chrome. DSP-12 does not measure this rack (narrow point 6). |
| **3. The back door was a flat dark slab and darkened the shop door's glass** | **PARTLY** | STREET_30 day, x 1272 to 1325, y 600 to 780: luma 28.3, sd 2.8 (try 1: 18.4, sd under 1). It is no longer a flat patch, and it reads as a blue door in a white architrave. But it is still well under the 40 asked, and its new mottle reads as sponged paint in the room picture. The shop door's panes at STREET_SQUARE day read 54.8 (upper) and 42.9 (lower) against the window's 68.9. See narrow point 1. |
| **4. FAS-01c failed on its mask, not on the board** | **FIXED** | The row now separates the letters by colour: 2.22. My measure, by colour: STREET_SQUARE 2.27 by day and 2.42 at night; STREET_30 2.14 and 2.49; no pixel at 250. |
| **5. At night the glass lettering barely separates from what is behind it** | **the target's and the PC's** (PC-10 is now in the target, T2-10); not for this verdict | Measured again, STREET_SQUARE night_lit, ink p75 against ground: TOBACCONIST & CONFECTIONER 1.10, the hours 1.14, the 18 1.04 (try 1: 1.20, 1.42 and 1.11). This is slightly worse, because the lighter back door now stands behind the letters. In night_dark they read at 3.45, 5.20 and 2.81. I now advise the 3 mm keyline (25, 25, 30) rather than waiting for the PC. |
| **6. Two printed titles carried real publications' names** | **FIXED** in the build | MERIDIAN MORNING GAZETTE (the right stand, lower step) and QUAYSIDE MODELLER (the board, bottom right) are both in the picture. "morning star" and "model railway news" are in the brand blocklist. The room's 24 titles (prints_used_room.json) and the texts carry neither. The old strings are still in `sw_gen.py` (narrow point 3). |
| (a) shared: the stand-in lamps' pool burned into the night glass | **FIXED** | STREET_30 night, try 1's band (x 1382 to 1532, y 817 to 855): R minus B is 6.6 (try 1: 79). The foot of the door pane reads 20.9, with R minus B 8.3 (try 1: peaks 246). GLS-04 finds 0 px at both street cameras. |
| (b) shared: night_dark's hot corners | **FIXED**, with a new reflection (narrow point 5) | The room night_dark corners read 5.8 and 5.6. The toplight strips at STREET_SQUARE night_dark read 20.8 to 22.1 against the brick's 24.3. |
| (c) shared: the loader dropped the models' glass | **FIXED** | DSP-07: CashRegister_01 2 of 2 meshes and wall_clock 4 of 4, glass kept. From the street the till and the clock read normally (STREET_30, the clock at x 1420, y 575 to 620). |
| For the target's owner: a lit shop at night with CLOSED and the shutter up | **still open** (not counted) | The target keeps the lit night. A night_dark street preview now exists, also with the shutter up. Which of the two nights is this shop's is still the owner's question (canon or scope). |

## Faults, worst first

None.

## Narrow points, each with its exact fix (most visible first)

### 1. The back door is still dark from STREET_30, and its paint reads as sponged, not painted (try 1's point 3, partly fixed)

- **Where:**
  - STREET_30 day, the middle light, x 1265 to 1345, y 575 to 800: luma 28.3 against the glass's 73.8. The try 1 fix expected about 40.
  - STREET_SQUARE day: the same door fills the left 60 per cent of both panes of the shop door, which read 54.8 and 42.9 against the window's 68.9.
  - In the room picture (`newsagent_day`, x 2854 to 3097, y 627 to 947) the door is a cloudy blue marble: mean 74, sd 7.7. Its two raised panels hardly show.
- **Cause:** `sw_shops_news.py`, the stockroom door. The base (96, 110, 140) is right, but the mottle is `1 + 0.10 x (6 cm blotches) + 0.05 x (2 cm) + 0.03 x (brush)`. A 10 per cent cloud reads as a sponge effect, not as gloss paint.
- **WHOSE:** the builder.
- **EXACT FIX:**
  - Base colour (124, 140, 176). It is still a mid-to-dark painted blue, about 1.9 times the linear albedo.
  - Mottle amplitudes 0.03 (6 cm) and 0.015 (2 cm); keep the brush marks at 0.03 and the roughness at 0.4.
  - Re-render the three room pictures and the street frames.
  - **Check:** STREET_30 day, the door's luma 36 to 44; in the room picture, the door's 9 px sd median under 2.0 (today 3.04).

### 2. The sweet jars read grey from the street

- **Where:** STREET_SQUARE day, the third light, x 1453 to 1553, y 867 to 917.
  - The six jars read as glass with pale grey or green contents.
  - HSV saturation: mean 0.09, p90 0.19. The 13 October jars read p90 0.31 in the same box.
  - STREET_30 day, x 1385 to 1450, y 845 to 885: the same.
- **Cause:** `sw_shops_news.py` puts jars 0 to 2 (HUMBUGS, PEAR DROPS, MINT IMPERIALS: two near-white, one pale green) in the front row (v 0.20). The coloured ones (FRUIT DROPS, SHERBET LEMONS; TOFFEES is brown) stand behind them, half hidden. The clear shell then greys what is left.
- **WHOSE:** the builder.
- **EXACT FIX:** front row FRUIT DROPS, SHERBET LEMONS, PEAR DROPS; back row HUMBUGS, MINT IMPERIALS, TOFFEES (swap the content and label indices; nothing moves). **Check:** STREET_SQUARE day, that box's p90 saturation at least 0.30.

### 3. Two invented cigarette makers echo real British lagers, and are legible at 100 per cent from both cameras

- **Where:** the cartons on the left stand. STREET_SQUARE day x 965 to 1035, y 765 to 800, and STREET_30 day x 980 to 1090, y 755 to 800, read MARSDEN, SELWYN, **KESTRELL**, **CASTLEMERE**, HOLLINGWORTH and ALDERLEY.
- **What it is:**
  - KESTRELL is one letter from Kestrel, a lager sold across Britain in 1990.
  - CASTLEMERE shares its first seven letters with Castlemaine XXXX, the most advertised lager of those years.
  - Neither is a real cigarette, so the content rule is not broken on its face. But a British player reads a drink's name in a tobacconist's window. The rule says no real firm's name and no drink, and this is the cheap side of that line.
  - My knowledge of these two lagers is from memory, not from a source I reached.
- **Also:** `sw_gen.py` still holds MODEL RAILWAY NEWS (MAGAZINE_TITLES, line 480) and MERIDIAN MORNING STAR (PAPER_NAMES, line 499). This build does not use them; a rebuild that calls the old atlas maker would.
- **WHOSE:** the builder (the strings); the target (the blocklist).
- **EXACT FIX:**
  1. In `sw_gen.PACK_BRANDS`, rename KESTRELL to BRAMHALL and CASTLEMERE to LANGDALE. Keep their colours and sub-lines.
  2. Add "kestrel" and "castlemaine" to `inventory.brand_blocklist`.
  3. Replace the two old strings in `sw_gen.py` with QUAYSIDE MODELLER and MERIDIAN MORNING GAZETTE.

### 4. FLT-02 fails on a painted dado, not a void

- **Where:**
  - STREET_30 day, x 1387 to 1451, y 711 to 813, luma 40: the right wall's grey dado under the cork board. FLT-02 measures 3.05 per cent of the glass against 3.0; I measure 2.89.
  - STREET_SQUARE day, x 1495 to 1570, y 733 to 834, luma 31: the pension counter's front, 2.29 per cent (2.38 in the row; try 1: 2.6).
- **What it is:**
  - Try 1's 3 per cent was set to catch the back door. The door is now out of it.
  - What remains is a wall in shade, which any plain wall becomes at 9 m once the card is sampled with mips. In its own picture the dado is textured: 9 px sd median 1.47, only 11 per cent flat.
  - The pension counter's front is different: it is flat in its own picture (94 per cent of it under sd 1). It is a brown panel with no grain, as is the main counter's front.
- **WHOSE:** the check (the limit is my try 1 number) and the builder (the counter fronts).
- **EXACT FIX:**
  - FLT-02 counts a patch only where the room picture under it is itself flat (9 px sd under 1 at the picture's own resolution, read through `trace` the way LIT-02b reads its luma-40 picture test). Keep the 3.0 per cent.
  - Give both counters' fronts and panels the room's wood map (DSP-09's rule, carried to the room's fixtures).
  - **Check after:** FLT-02 under 3.0 at both street cameras, and no fixture face in the room pictures more than 50 per cent flat.

### 5. In night_dark, the stand-in wash shows as an amber panel in the pension counter's screen

- **Where:** STREET_SQUARE night_dark, x 1500 to 1644, y 625 to 673: luma 44.9 (R 79, G 39, B 1) against the glass's 13.1 and the brick's 17. That is 2.3 per cent of the glass, and the brightest thing in the dark shop.
  - In the room picture (`newsagent_night_dark`) it is a sharp trapezoid across the lower half of the clear screen: 55.3 against the picture's mean of 18.0.
  - It is the try 2 wash light (W - 1.0 x 0.5 m, tipped 30 degrees) reflected in the screen's glass.
- **Why only narrow:** the target lights this shop at night, so night_dark is not its street night. But the night_dark picture is one of the game's three, and a street preview of it now exists.
- **WHOSE:** the builder (the room render; the kit's wash is shared).
- **EXACT FIX:**
  - In the night_dark room render, set the wash light's `visible_glossy` to False, or give the pension screen roughness 0.15.
  - Add to PIC-03: in the night_dark picture no connected patch inside the back wall's rectangle (940, 426 to 3156, 1429) above twice the picture's mean over 0.2 per cent of the picture.

### 6. DSP-12 does not measure the postcard rack, the rack it was written for

- **Where:** `check_try3.news_rows`. The row reports one pole only: "card_rack pole at x 1580 to 1623 px, 32 px from the nearest mullion". That is the card spinner by the jamb. `postcard_rack_frame` is a support group in `display_items.json`, but no line for it appears, so it was not found in the loaded glb or had no vertices in w 0.05 to 0.45.
- The rack itself is right (item 2 above: 15.5 px clear).
- **WHOSE:** the builder (the check).
- **EXACT FIX:** look up each rack's frame by its group's objects as loaded (match on the name's stem, since a glb import can suffix it). Fail the row if any rack named in `display.items` is missing from its output. Expected: postcard_rack at about x 1430 to 1442, about 15 px clear.

### 7. The newsagent's try 2 has no section in NOTES.md

- **Where:** NOTES.md ends with the ironmonger's try 2. There is no "Try 2, newsagent": no item-by-item account of the two try 1 reviews, no named shortfalls for try 2, and no note of FLT-02's failure or why it was left.
- **WHOSE:** the builder (records).
- **EXACT FIX:** write the section in the ironmonger's form before the stage closes. It needs:
  - each item of both try 1 reviews: what was done and how it was measured;
  - FLT-02, and which night is this shop's;
  - the times;
  - where a second reviewer should look.

## Looked for and not found (the changes of try 2)

- **The printed goods** (T2-8): eight folded papers, four to a stand, with halftone photographs and headlines set whole. Every headline legible from the street is whole (PRT-04 agrees).
  - The twelve covers are crops of landscape photographs under white serif mastheads. From 8.76 m they read as magazines on a sloping rack, quieter and greyer than 1990 covers were. That is a taste remark, not a point.
  - No flat clip-art remains.
- **The glass of the models kept:** nothing black or missing on the till or the clock (c above). The jars' new glass is narrow point 2.
- **The sheets' lean:**
  - papers, covers and cartons lean back and rest on what is behind them;
  - nothing leans toward the glass;
  - nothing floats at either camera.
- **Furniture sizes:** the pads at 0.95 to 1.0 lie on the plinth at the board's foot; the pot of pens stands before QUAYSIDE MODELLER. Both read as stationery and do not hide a cover's title.
- **The lamp pool setting:** no orange band in the night glass (a above). The pavement's white band in front of the front is the gate's spill pool, as in try 1 (PC-02).
- **The doorway floor block:** through the shop door's glass there is no dark box. The lower panes show the back door and the floor at both cameras, and FRN-13 finds 0 of 1120 rays on a reveal at each street camera.
- **The night sign:** OPEN by day; CLOSED in night_lit and night_dark, as the hours (shut at 17:30) ask.
- **The front:**
  - The only dark runs under luma 16 at either camera are natural shade: the box sign's underside, 4 px at y 390 to 394; the side door's leaf under its head, x 1931 to 2103, y 601 to 621; the knob.
  - No coplanar strip.
  - No sky slot at STREET_30: brick meets both pilasters.
  - Both glbs export cleanly: one normal map in the front (mean 127.5, 127.5, 255), two in the display (blue 160 or more on 99.9 and 100 per cent); no textured primitive without TEXCOORD_0; no negative texCoord.

## What is right

**The front** is try 1's, which passed:
- the 3.2 kit as the target lists it: panel pilasters on plinths, scroll consoles, the timber cornice, the 4.1 lit box sign (red face, cream NEWSAGENT and its rules, black returns), the sill, the three-panel stallriser, the T1 window of three lights with nine toplights;
- the T1 shop door: kick plate, letter plate, lever, bell, OPEN / CLOSED, TOBACCONIST & CONFECTIONER, the hours;
- the navy F1 side door with its fanlight, head and panel;
- the roller-shutter hood and rails.

It sits with Rita's approved front and the Hook sheet's painted fronts. Its wear is owed on the PC (PC-05).

**The window is glass with a lit room behind it:**

| measure (the three lights' glass) | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, mean luma (inset 60 mm; p5, p95) | 68.9 (23, 181) | 71.0 (26, 185) |
| day, under 3 / under 12 / 250 or above | 0 / 0.13% / 0.02% | 0 / 0 / 0.01% |
| brick beside, by day | 83.8 and 83.8: the glass is 0.82 of the wall, dimmer, as P1, P3 and D5 have it | 83.8 and 84.4 |
| night_lit, mean luma | 86.0 | 89.3 |
| brick beside, at night | 19.8 and 17.5: the window is 4.3 to 4.9 times the wall | 19.8 and 17.7 |
| largest flat patch (9 px, sd under 1), by day | 2.29%: the pension counter's front, luma 31 | 2.89%: the right wall's dado, luma 40 (narrow point 4) |
| largest dark patch (under 12), by day | 0.03% | 0 |
| night_dark, mean luma (not this shop's night) | 13.1 (brick 17.0): an honestly dark shop, room readable; the composite LIT-01 12.8 lies in the target's 10 to 35 | not rendered |

- By day both cameras read the gantry of packs, the jars and till on the counter, the covers on the left wall, the pension screen, the back door, the clock, the cork board, the cards and the chequer floor.
- At night the three battens make a white-lit shop in a sodium-lit parade.

**The trade reads from across the street:**
- NEWSAGENT on the box sign;
- TOBACCONIST & CONFECTIONER on the door;
- eight papers on two stands;
- six cigarette cartons;
- twelve magazines;
- six sweet jars (greyer than they should be: narrow point 2);
- the postcard rack and the card spinner;
- the gantry of about 265 packs behind the counter.

TRD-01 agrees (papers and magazines 20 pieces, tobacco 6, sweets 1, cards 2).

**Every word legible at 100 per cent in the five street frames, and whether it is acceptable:**
- NEWSAGENT; TOBACCONIST & CONFECTIONER; OPEN (day); CLOSED (night); MON-SAT 6-5.30 / SUN 7-12 (day); 18 (day). The project's own words or plain trade words: acceptable.
- Carton makers MARSDEN, SELWYN, HOLLINGWORTH and ALDERLEY: invented, acceptable. KESTRELL and CASTLEMERE: narrow point 3.
- Mastheads THE QUAYSIDE MAIL and THE MERIDIAN LANTERN; at the edge, WEST COAST DAILY and MERIDIAN EVENING NEWS. Invented, acceptable.
- Headlines TRAWLER BACK IN PORT, LIGHTS TO BE FITTED ON THE QUAY and BUS FARES TO RISE IN MAY; at the edge, RAIN FORECAST FOR THE WEEKEND, COUNCIL APPROVES NEW BRIDGE and HARBOUR REPAIRS TO BEGIN. Invented, acceptable.
- Magazines at the edge of legibility: FARMHOUSE COOKING, MOTOR WORLD, YACHT AND DINGHY, COTTAGE HOMES, THE WALKER and QUAYSIDE MODELLER. Invented, acceptable as far as I know.
- PENSIONS & ALLOWANCES (at the edge). Plain words, no firm's name: acceptable.
- Read only at 3 to 4 times: the carton sub-lines, MERIDIAN MORNING GAZETTE, THE WEST COUNTRY CHRONICLE, WEST COAST BULLETIN, THE ANGLER'S WEEK, COUNTRY DIARY, the jar labels and the price cards. None is a real firm's that I know.

**Content:** no drink shown or named (but see narrow point 3), no betting slip, lottery, child, toy or person, no barcode, flat screen or modern packaging. Tobacco is shown, which is allowed.

## The builder's named shortfalls, judged from the street

No newsagent try 2 list exists (narrow point 7). From the check file and the target's T2 rows:

| shortfall | my judgement |
|---|---|
| FLT-02 fails (3.05 per cent at STREET_30) | **narrow** (point 4): a painted dado in shade, not a void |
| ROOM-05: 0 of the 8 Poly Haven cigarette_pack (a real brand's model) and 265 invented packs instead of 100 | **right**: the gantry reads full and no maker is legible |
| 64 samples, not 128 | **not seen** at street distance (X-NOISE 0.39) |
| the shut-up variant (shutter down) is not built | **not a fault** for the lit night the target keeps; the owner's question stands |
| the box sign's glow is the gate's (PC-08), the glass and lamps the cloud's | **owed on the PC**: the board reads day and night (point 4 of try 1, fixed) |

## The check rows: which I trust

- **Trusted** (measured on the real pictures, meshes or files, and I agree):
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-07;
  - DSP-01, DSP-02, DSP-04 to DSP-07, DSP-09, DSP-13;
  - ROOM-01 to ROOM-05;
  - INV-01 to INV-07, NEV-01, NEV-02;
  - GLB-01, FAS-01n, FAS-01c (my 2.27), FAS-03;
  - FRN-01 to FRN-05, FRN-07, FRN-09, FRN-10, FRN-13;
  - GLS-01, GLS-02, GLS-04, SIGN-01, TRD-01, PRT-01, PRT-02, PRT-04, FLT-01, CAM-01, X-PRV.
- **Pass but do not prove what they say:**
  - DSP-12: it measures the card spinner, not the postcard rack (point 6).
  - DSP-03: its detail does not say whether the twelve covers count as twelve pieces (try 1's gap). My own look shows every cover at least two thirds seen, so nothing hangs on it now.
  - FAS-01: the board's maps are right, but the board is behind the box sign.
  - FRN-08: the STREET_30 sliver is closed only by the gate's pier (PC-04).
  - PRT-03: the captions cannot be read from the street.
- **The cloud's stand-ins only:**
  - LIT-01, LIT-02 and LIT-02b (the card alone, the gate's exposure);
  - LIT-05, LIT-07, LIT-08, PIC-05g, GLS-03 and GLS-05 (the gate's glass, lamps and spill);
  - PRJ-02 (the gate's own `trace`).
- **The failing row:** FLT-02 is narrow point 4.

## What I cannot judge from these files

- **The builder's own account of the newsagent's try 2** (point 7): whether it claims a review was wrong anywhere, and why FLT-02 was left.
- **Try 1's street frames were overwritten.** `gate_old` keeps only CLOSE_35_B. Try 1 is compared through its 13 October previews and my try 1 numbers, not frame against frame.
- **The game's glass:** the street and the sky in the panes, the dirt, and the night hand-over. The gate's day glass reflects nothing.
- **The game's light:**
  - Lumen in the window and room;
  - the box sign's own glow (PC-08);
  - the spill's pool on the pavement (PC-02);
  - the exposure;
  - the lamps;
  - whether the glass lettering reads at night (PC-10).
- **Wear:** the front, sign and pavement are spotless; the D53 layer is owed (PC-05).
- **In motion:** TSR on the toplights and the rack wires, and the card's parallax as the player walks.
- **The street facade behind the pilasters** (PC-04).
- **Which night is this shop's** (lit, as the target keeps, or the shut-up variant): the target owner's question.
- **Kestrel and Castlemaine** as lagers sold in Britain in 1990 are from memory, not a source I reached (point 3).

**Next:**
1. Points 1 to 3: the back door's paint, the jars' order, the two carton names and the old strings.
2. Point 4: the rule, and the counters' wood.
3. Points 5 and 6: the wash's reflection, and DSP-12.
4. Point 7: the notes.
5. Re-render the three room pictures and the street frames.

None of this blocks the pass.
