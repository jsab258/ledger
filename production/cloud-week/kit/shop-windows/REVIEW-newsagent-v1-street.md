PASS

# The newsagent and tobacconist (west_north bay 0, no. 18), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. I judged the street view only (STREET_SQUARE and STREET_30, day and night_lit). I did not read the close review of this shop or the two ironmonger reviews. Jafar's ruling of 9 October applies: a piece that fails only on narrow points (each a small detail with an exact fix) passes, with the points listed for the builder.

**What I read:** CLAUDE.md; RULINGS.md (1, 2, 3, 8 October); NOTES.md ("For the next nine shops", the batch A preamble and the newsagent's own section); TARGET.md section 3, the newsagent's table (5.9) and section 13 (all three blocks, batch A included); Rita's four reviews; `checks/check_newsagent_v1.json` (61 rows); the parts of `sw_shops_news.py`, `sw_gen.py` and `sw_gate.py` that make what I saw; `target.json` shops.newsagent.

**What I looked at:** the previews `newsagent-street-square-{day,night-lit}`, `newsagent-room-{day,night-lit,night-dark}` (13 October); the four street gate frames (2560 x 1440, rendered 14 October 00:16 to 00:24, the newest) at full size and in crops up to 4 times; Rita's `ritas-street-square-day-v3`; the Hook sheet. I opened CLOSE_35 by day once, only to see the magazine board's geometry from another angle (narrow point 1); I did not judge the close view.

**What I measured:** my own pinhole projection from the gate's camera files (street z = height above the footway + 0.10; the west side's glass at y -5.255), Rec.709 luma 0 to 255, over the three lights' glass (each light inset 60 mm from its beads, z 0.68 to 2.36), the brick beside the bay, the shop door's glass, the stallriser, the box sign's face and the glass lettering; flat-patch and dark-patch searches; ray positions of the postcard rack's pole against the mullion; the two glbs' JSON (normal maps, UVs).

Pixel boxes are in the 2560 x 1440 gate frames.

**Verdict: no fault blocks.** The front reads, from the far pavement, as a 1990 newsagent and tobacconist in an old Victorian parade: the 3.2 kit's front altered the way such shops were (a lit box sign over the board, a roller-shutter hood), a window of papers, magazines, cartons, jars and cards in front of a lit shop with a cigarette gantry behind the counter. The glass is glass with a lit room by day and by night. Six narrow points remain, each with an exact fix; the first three are what a player could notice.

## Faults, worst first

None.

## Narrow points, each with its exact fix (most visible first)

### 1. The magazine board hides its own top row; from the street a bare grey band shows above the covers

- **Where:** STREET_SQUARE day, the middle light, x 1195 to 1395, y 821 to 852: a band of plain grey board (luma 93.8, standard deviation 4.1) about 0.13 m tall above the two rows of covers that show (MOTOR WORLD, CRAFT & MAKING, THE GARDENER'S YEAR, WEEKEND COOK over GARDEN LOG, YACHT AND DINGHY, COUNTRY DIARY, COAST & SEA). STREET_30 day, x 1200 to 1350, y 820 to 840: the same grey slope.
- **Cause:** the third row of four covers (STAMP CORNER, PUZZLE BOOK, MODEL RAILWAY NEWS, THE WALKER by the code's index) stands BEHIND the board: in CLOSE_35 day (x 1180 to 1470, y 885 to 910) only their top edges show over the board's top edge. In `sw_shops_news.py` (the magazine loop under "the magazines on a sloping board") each row's offset `off` is applied along (-cos 40, -sin 40) in (v, w), which is mostly down the slope (98 per cent) and hardly along the board's normal, so the covers do not lie on the board's face and the top row ends up behind it. DSP-03 passed because it counts the twelve magazines as one piece (57 per cent seen).
- **WHOSE:** the builder.
- **EXACT FIX:** put every cover on the board's front face: its centre at the board's face + 2 mm along the board's normal (-cos 40, +sin 40 in (v, w)), each lower row 4.5 mm further out along that same normal (so it hides the foot of the row above, as the comment intends); keep the rows' positions along the slope. Then make DSP-03 count each cover as its own piece: from STREET_SQUARE at least half of each of the 12 covers is seen, and from the street no more than 20 mm of bare board shows above the top row.

### 2. The postcard rack's pole stands exactly on the mullion's edge: the cards cling to the mullion (STREET_SQUARE) or float (STREET_30)

- **Where:** STREET_SQUARE day and night, the right mullion, x 1385 to 1475, y 655 to 835: three tiers of postcards stick out on both sides of the mullion with no pole or ring in sight. STREET_30 day and night, x 1310 to 1366, y 660 to 800: three tiers of cards hang in the air in front of the room's back door.
- **Measured:** the rack is at display u 2.30, v 0.42 (`sw_shops_news.py`, the rack loop). From STREET_SQUARE its 12 mm pole projects to x 1418.2, and the mullion's silhouette ends at x 1417.4: the pole is half behind the mullion's edge and does not read. From STREET_30 the pole projects to x 1341, onto the navy back door, and the rack's wire is (70, 70, 74): a dark rod on a dark door.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Move the postcard rack to u 2.38 (v 0.42 unchanged). From STREET_SQUARE the pole then projects to x 1436, 18 px clear of the mullion. Its base disc (r 0.12) stays 0.215 m from the nearest jar (u 2.57, v 0.32; clearance needs 0.178) and 0.06 clear of the magazine plinth's end at u 2.20.
  2. Make both racks' wire chrome-plated wire, as the period's spinners were: base colour (200, 200, 205), metallic 1.0, roughness 0.25.
  3. Add a DSP-03 clause: no rack's pole projects within 10 px of a mullion or jamb at STREET_SQUARE.

### 3. The room's back door reads as a flat dark slab through the glass, and darkens the shop door's glass

- **Where:** STREET_30 day, the middle light, x 1271 to 1337, y 583 to 802: luma 18.4, standard deviation under 1 over 6.7 per cent of the window's glass. It is the largest flat patch in either street camera; Rita's largest was 2.7 per cent. The same at night (5.6 per cent, luma 19.5). STREET_SQUARE day: the same door fills the left 60 per cent of the shop door's upper and lower panes, so the open shop's door glass reads 51.2 against the window's 63.6 (night: 40.7 against 76.5).
- **What it is:** a door, with a white architrave and a brass knob, so not a void. But its paint (40, 52, 90) in the room's light is near black, and from 8.76 m it reads as a dark opening at the centre of the window and behind the door.
- **WHOSE:** the builder (`sw_shops_news.py`, the stockroom door's `door_paint`; the target names no colour).
- **EXACT FIX:** repaint the stockroom door (96, 110, 140), roughness 0.4: still a painted blue door, about luma 40 at STREET_30, with the counter fronts. Then re-render the three room pictures and the four street frames. Check: no flat patch (9 px, standard deviation under 1) over 3 per cent of the glass at either street camera.

### 4. FAS-01c fails on its mask, not on the board: NEWSAGENT reads at both cameras, day and night

- **Where:** the box sign, STREET_SQUARE x 900 to 2120, y 300 to 390.
- **Measured:** with the cream (letters and rules: green at least 0.75 of red) separated from the red ground by colour, letters p75 against ground median: STREET_SQUARE 185.1 / 80.9 = 2.29 by day and 159.1 / 66.0 = 2.41 at night; STREET_30 2.15 and 2.40. Contrast by relative luminance: 3.54 and 3.12 (STREET_SQUARE), 3.35 and 3.10 (STREET_30). No pixel burns at night. The check's 1.87 comes from a mask that takes letter edges into its ground (97.9).
- **WHOSE:** the check (the target's row, run by the builder). The colours are 4.1's and need no change.
- **EXACT FIX:** for a box sign, FAS-01c separates letters from ground by colour (the 4.1 letter colour and ground colour, each pixel to the nearer), not by the letter alpha; keep the limit of 2.0. Today that reads 2.29 and 2.15.

### 5. At night the glass lettering barely separates from what is behind it

- **Where:** STREET_SQUARE night: TOBACCONIST & CONFECTIONER, ink p75 49 against 41 round it (1.20); the hours plate 48 against 34 (1.42); the 18 on the fanlight 55 against 50 (1.11). STREET_30 night: 1.03, 1.33 and 1.18. By day the same rows read at 3 to 7.7. The hours plate's "5.30" and "7-12" are lost where the white wall stands behind them.
- **What it is:** the shop is shut at night (CLOSED), and the hours are what a passer-by reads then. But the letters are lit only by the gate's assumed lamps, so this is Rita's PC-06 case on glass, not the builder's.
- **WHOSE:** the target's owner and the PC.
- **EXACT FIX:** add a row owed on the PC beside PC-06: at night in the packaged game, from STREET_SQUARE, each glass row's ink against the glass round it, a luma ratio of 1.3 or more either way. If the game does not give it, 4.1's glass art takes a 3 mm dark keyline (25, 25, 30) round every letter (the signwriter's outline), so the letters read against a lit room as well as a dark one.

### 6. Two printed titles carry a real publication's name (neither is legible from the street at 100 per cent)

- **MERIDIAN MORNING STAR** (`sw_gen.PAPER_NAMES`, on the left paper stand's upper step, STREET_SQUARE x 990 to 1035, y 825 to 835: legible only at 3 times) carries "Morning Star", the title of a real British national daily.
- **MODEL RAILWAY NEWS** (`sw_gen.MAGAZINE_TITLES`: the hidden third row of the board, and the room's left wall). From memory, not from a source I reached, this was a real British magazine's title.
- **WHOSE:** the builder (the invented strings). The brand blocklist did not hold them.
- **EXACT FIX:** rename them MERIDIAN MORNING GAZETTE and QUAYSIDE MODELLER, and add "morning star" and "model railway news" to the target's brand_blocklist. The close reviewer reads them at 100 per cent.

## Shared, known (from the gate and kit; they do not decide this verdict)

- **(a) The stand-in lamps' far-pavement pool in the night glass: seen.**
  - STREET_30 night: an orange band across the third light (x 1382 to 1532, y 817 to 855; R minus B 79, luma about 100).
  - The bottom of the shop door's lower pane (y 820 to 830, R minus B 137, peaks 246).
  - Not seen at STREET_SQUARE.
  - GLS-03 (p95 3.9) cannot see it.
- **(b) The night_dark picture's hot orange top corners: seen** in `newsagent-room-night-dark`, at both ceiling corners. Not in this shop's street frames, because the shop is lit at night.
- **(c) The model loader drops models' glass parts: applies.** CashRegister_01 and wall_clock both have a `_glass` material in their source. Neither is seen from the street.

## The builder's named shortfalls, judged from the street

| shortfall (NOTES and the check) | my judgement |
|---|---|
| about 265 invented packs, no Poly Haven pack, no sliding glass on the gantry | **not a fault.** From both cameras the gantry reads as a tobacconist's wall of packs behind the counter; no maker is legible at 100 per cent |
| 12 magazines not 24, papers 0.22 wide on stands, pads at 0.6 on a plinth, no eraser | **not a fault.** The stands, plinth and jars lift the goods over the sill's sight line and they read. The board's hidden row is **narrow point 1** |
| the shutter is up; the shut-up variant is not built | **not a fault** for the lit view the target asks for (see "for the target's owner") |
| the box sign's glb is the day state; the glow is put on by the gate (PC-08); FAS-01c 1.87 | **narrow (point 4):** the board reads, day and night |
| the pension counter has no firm's name | **right** |
| nobody behind the counter | **right** (no people) |
| the pictures at 48 samples | **not seen** at street distance; the 128-sample pictures are owed on the PC |
| the gate's spill at 105 W, the printed whites at 0.86 | **not a fault.** At night 0.26 per cent (STREET_SQUARE) and 0.63 per cent (STREET_30) of the glass is at 250 or above (white cards), and the papers read |
| LIT-08 (the magazines 0.54 of the room at CLOSE_35 at night) | **the close view's.** From STREET_SQUARE at night the covers read at 67.5 against the room above them at 49.7 |

## What is right

**The front:**
- It is the 3.2 kit's parts as the target lists them:
  - panel pilasters on plinths and scroll consoles;
  - the timber cornice;
  - the board, carrying 4.1's lit box sign (black returns, eight screws, the red face with NEWSAGENT and its two rules);
  - the sill and the three-panel stallriser;
  - the T1 window of three lights with the mullions carried up;
  - the T1 shop door: brass kick plate, letter plate, lever on the right, the bell on the top rail on the hinge side, OPEN / CLOSED;
  - the navy F1 side door: vertical letter plate, centre knob, lock;
  - the band above the doors: the fanlight with 18, the transom, the 70 mm of toplight under the hood, the raised panel and head over the side door;
  - the 2.2 roller-shutter hood with its three rails.
- The parade's later alterations (a box sign over the Victorian board, a shutter box) are exactly how a 1990 newsagent's front looked.
- The proportions match Rita's approved front: the same kit, the same heights.
- Dove grey, the yellowed-white frame, the red box and the navy side door sit with the Hook sheet's painted fronts.
- Nothing floats but the rack's cards (narrow point 2). Nothing is mirrored, and no text reads backwards.

**Rita's lessons held:**
- **No coplanar black strip.** The only dark lines under luma 16 are natural shade: the box sign's underside, 4 px at y 390 to 394, and the navy leaf under the side door's head, a gradient from 14 to 43.
- **No sky slot at STREET_30.** Brick meets both pilasters.
- **The glbs export cleanly.** The board's normal map is a real RGB map: flat, mean (127.5, 127.5, 255). Every textured primitive has TEXCOORD_0 and none has a negative texCoord (checked in both glbs).
- **The spill is invisible.** No white bar under the transom; the head band shows 0 at 250 or above; the mullion fronts (59) are darker than the glass (69).
- **The hall shows dark behind the side door's fanlight.**
- **The glass rows are clear of every bar** (GLS-02, and by eye).

**The window is glass with a lit room behind it:**

| measure (the three lights' glass) | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, mean luma (p5, p95) | 63.6 (23, 155) | 66.9 (19, 157) |
| day, under 3 / under 12 / 250 or above | 0 / 0.15% / 0.12% | 0 / 0 / 0.08% |
| brick beside, by day | 84.1 and 84.5: the glass is 0.76 of the wall, dimmer, as P1, P3 and D5 have it | 84.2 and 85.5 |
| night, mean luma | 76.5 | 79.5 |
| brick beside, at night | 20.7 and 18.9: the window is 3.7 times the wall | 20.7 and 19.5 |
| largest flat patch (9 px, sd under 1) | 2.6%: the pension counter's front, luma 31 | 6.7%: the back door (narrow point 3) |
| largest dark patch (under 12) | 0.04% | 0.00% |

- By day the room reads at both cameras: the gantry, the jars and till on the counter, the covers on the left wall, the pension counter's screen, the back door, the floor's chequer.
- At night the three battens light it white against the sodium street: a lit shop in a dark parade, as the 1 October ruling asks.

**The trade reads from across the street:**
- the box sign;
- TOBACCONIST & CONFECTIONER on the door;
- papers on two stands;
- the cartons;
- the magazines;
- the jars;
- the card spinner;
- the gantry of packs behind the counter.

TRD-01 agrees: papers 11 pieces, tobacco, sweets and cards each read.

**Every word legible at 100 per cent in the four frames, and each is acceptable:**
- NEWSAGENT;
- TOBACCONIST & CONFECTIONER;
- OPEN (day) and CLOSED (night);
- MON-SAT 6-5.30 / SUN 7-12;
- 18;
- the headlines TRAWLER BACK IN PORT, BUS FARES TO RISE IN MAY, RAIN FORECAST FOR THE, COUNCIL APPROVES NEW BRI(DGE), HARBOUR REPAIRS TO BEGIN, NEW LIBRARY OPENS ON;
- at the edge of legibility, MOTOR WORLD, CRAFT & MAKING, WEEKEND COOK and COUNTRY DIARY.

All are the project's own words or plain trade words.

Read only at 3 times, and all fictional:
- the mastheads (THE QUAYSIDE MAIL, WEST COAST DAILY, THE MERIDIAN HERALD, MERIDIAN EVENING NEWS, THE WEST COUNTRY CHRONICLE, and MERIDIAN MORNING STAR: narrow point 6);
- the jars (HUMBUGS, PEAR DROPS, MINT IMPERIALS);
- the cards (BIRTHDAY GREETINGS and others);
- PENSIONS & ALLOWANCES.

**Content:**
- No drink, betting slip, lottery, child, toy or person.
- No barcode, flat screen or modern packaging.
- No real firm's mark legible from the street.
- Tobacco is shown, which is allowed.

## The check rows: which I trust

- **Trusted** (measured on the real pictures, meshes or files, and I agree):
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-07, DSP-01, DSP-02, DSP-04;
  - ROOM-01 to ROOM-03, ROOM-05;
  - INV-01 to INV-06, NEV-01, NEV-02;
  - GLB-01, FAS-01n, FAS-03;
  - FRN-01 to FRN-05, FRN-07, FRN-09, FRN-10;
  - GLS-01, GLS-02, TRD-01, LIT-06, CAM-01 (the camera files match target.json's eyes and aims), X-PRV.
- **Pass but do not prove what they say:**
  - DSP-03: it counts the 12 magazines as one piece, so four hidden behind their board pass (narrow point 1); a pole hidden by a mullion passes (narrow point 2).
  - FAS-01: the board's maps are right, but the board is behind the box sign. The street reads the box's face, which FAS-01c measures.
  - FRN-08: the STREET_30 sliver is closed only by the gate's pier (PC-04).
  - GLS-03: a p95 over the whole glass cannot see a band that covers a few per cent of it (shared (a)).
- **The cloud's stand-ins only:**
  - LIT-01 and LIT-02 (the card alone);
  - LIT-02b, LIT-05, LIT-07, LIT-08, PIC-05g and GLS-03 (the gate's glass, lamps and spill, set by eye);
  - PRJ-02 (the gate's own `trace`).
- **The two failing rows:**
  - FAS-01c is narrow point 4.
  - LIT-08 is the close view's; it is not a point from the street.

## For the target's owner (not counted)

At night the shop shows CLOSED with all three battens on and the shutter up. That is the street file's choice (lit_at_night, west_north_interior0), and the target keeps it while its own hours shut the shop at 17:30. A 1990 newsagent shut for the night would usually have its shutter down. If the lit night stays, the target should say why (an evening's restocking, the next morning's rounds being marked up); if not, the shut-up variant is the night. This is a canon or scope question, not the builder's.

## What I cannot judge from these files

- **The game's glass:**
  - the street and the sky in the panes (the Hook sheet's bar, RULINGS 3 October), the dirt, and the night hand-over;
  - the gate's day glass is clear and reflects nothing.
- **The game's light:**
  - Lumen in the window and room;
  - the box sign's own glow, and its light on the hood and consoles (PC-08);
  - the spill's pool on the pavement (PC-02; the gate's pool is a stand-in, 107.6 against the glass's 69);
  - the exposure;
  - the lamps (assumed: they wash the dove-grey front brown at night).
- **Wear:** the front, sign and pavement are spotless. The D53 layer is owed (PC-05).
- **In motion:**
  - TSR on the toplights' thin strip and the racks;
  - the card's parallax as the player walks;
  - the gate frames' 32 samples (NOTES).
- **The game's street facade behind the pilasters (PC-04).**
- **Whether "Model Railway News" and "Morning Star" were real titles** is from memory, not a source reached (narrow point 6).

**Next:**
1. Fix narrow points 1 to 3 (the board's covers, the rack's place and wire, the back door's paint), the strings of 6 and the FAS-01c mask of 4.
2. Re-render the three room pictures and the four street frames.
3. Give point 5 to the target's owner.

None of this blocks the pass.
