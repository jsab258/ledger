FAIL

# Rita's front, the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, 13 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the front. I judged the street view only. The close view is another reviewer's.

**What I read:** CLAUDE.md; RULINGS.md (1, 2, 3 and 8 October); NOTES.md; TARGET.md sections 3, 4 and 6; TARGET-REVIEW.md; `checks/check_ritas_v1.json`; and the parts of `sw_front.py`, `sw_gate.py` and `check_ritas.py` that make what I saw.

**What I looked at:**
- `ritas-street-square-{day,night-lit}`.
- STREET_30 day and night (the 2560 x 1440 gate PNGs, at full size and in crops).
- The three room pictures and the before-and-after sheet.
- The approved front (`rita-day-kit` and `rita-night-kit`, 6 October).
- The Hook sheet, P1 and P3, and 4.1's Rita board (`fascias-ritas-v3`).

**What I measured:**
- My own script (pinhole projection from the gate's camera files; Rec.709 luma, 0 to 255) over the glass of the three lights, the head band, the mullions, the toplights, the fascia, the stallriser, the brick beside, and the pavement.
- The exported `ritas_front.glb`'s JSON and textures.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview JPEG).

**Two faults block.**
1. The fascia board renders as black-streaked wood with the name hard to read. The cause is in the game's own asset: the height map went into the glb as its normal map.
2. The glass rows read "W TCHES", "JEW ELLERY" and "OANS".

The rest are narrow points with exact fixes. The worst of them is the night stand-in light. It pokes through the glass and makes the burnt bar and the glowing frame. The window itself passes: it is glass with a lit, stocked room behind it by day and by night, with no void and no flat board.

## Faults, worst first

### F1. The fascia reads as black-grained wood; RITA'S / PAWNBROKER lose most of their contrast (day and night, both cameras)

- **Where:**
  - STREET_SQUARE day and night: the board, x 417 to 1685, y 279 to 399 (1600: x 261 to 1053, y 174 to 249).
  - STREET_30: x 728 to 1603, y 305 to 482.
  - The board shows wavy black streaks over its whole length, like zebra-grained timber, not paint. 4.1's own board (`fascias-ritas-v3-2026-10-12.jpg`) is a clean maroon ground with a few flakes.
- **Measured (day, STREET_SQUARE):**
  - The board's ground is luma 34.2. 26 per cent of its pixels are under 20.
  - The stallriser, in the same oxblood under the same sky, is 55.6.
  - The gilt letters reach 47.6: a letter-to-ground ratio of 1.39. STREET_30 gives 1.24. The 4.1 base colour has 2.8 (gilt 154.7, ground 55.5).
  - At night the letters are 6.8 and the ground 5.9, so the name cannot be read at all.
- **Cause, from the glb:**
  - The material `fascia_ritas` has `normalTexture` = image 1, `ritas_height`. That is the 16-bit grey height map (mean 0.526), not a normal map.
  - Read as a tangent normal, grey gives x = y = z, about 0.05. Once normalised, that points 55 degrees off the face, and the sign flips with the grain. This produces the black streaks.
  - The glTF exporter turned the Bump node in `sw_front.py` (lines 660 to 666) into this normal texture.
- **NOTES.md names the wrong cause.** It blames the wear map. But `ritas_wear.png` is almost empty (mean 0.3 of 255), and neither it nor the Multiply node that applies it is in the glb at all.
- **The game shows the same streaks.** The game imports this same glb, so this is not a gate artefact.
- **The check misses it.** FAS-01 passes because it checks only that the maps are in the glb and that the mapping is right.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. In `sw_front.py`, stop linking the Bump node into the exported material. Then either:
     - leave the board without a normal (relief of 1.3 mm or less does not read at 8.76 m); or
     - convert `ritas_height.png` into a real tangent-space map `ritas_normal.png`:
       - h in mm = (H - 32768) / 25600, at 1 px a mm;
       - n = normalize(-dh/dcolumn, +dh/drow, 1), green up as glTF reads it;
       - RGB = 127.5 (n + 1);
       - linked through a Normal Map node.
  2. If the 25 per cent wear darkening is wanted, bake it into the base colour. The Mix node does not survive export.
  3. Re-export the front and re-render the four street pictures.
  4. Add two rows to FAS-01:
     - every `normalTexture` in the glb is RGB, with a mean within 10 levels of (128, 128, 255) and blue at 200 or more on 99 per cent of pixels;
     - in STREET_SQUARE by day, the board's ground luma is within 15 per cent of the stallriser's, and letters to ground is 2.0 or more.

### F2. The glass rows are cut by the toplight bars: "W TCHES", "JEW ELLERY", "OANS"

- **Where:** STREET_SQUARE day and night, the toplight row at y 455 to 480.
  - WATCHES: x 942 to 1100.
  - JEWELLERY: x 1180 to 1380.
  - LOANS: x 1487 to 1592.
  - 1600: y 284 to 300.
  - Each 4.1 row is laid across its light's three toplights, so two 28 mm bars cross every row:
    - the A of WATCHES is hidden;
    - the W of JEWELLERY is split;
    - the L of LOANS sits behind the bar and its S is half cut.
  - Read from the pavement, the shop's trade lettering looks misspelt. A player would see it as wrong at first look.
- **WHOSE:** the target.
  - It asks for 4.1's rows (drawn 715, 904 and 490 mm wide, for a window with one toplight a light).
  - It also asks for the 3.2 toplight rule (nine panes of 327 mm).
  - It never says where on the glass the rows go.
  - The builder saw it and left it to the target's owner, rightly.
- **EXACT FIX (recommended):**
  - Move the three rows from the toplights to the head of the three main lights.
  - Centre the ink on each light: u 2868, 3975 and 5082 mm from the bay's left, which is street x 18.132, 17.025 and 15.918.
  - Baseline at 2250 above the footway, at 4.1's sizes:
    - the cap top is at about 2336, below the transom's glass edge at 2400;
    - the tallest display piece stands at about 1790;
    - each row fits inside its light's 1037 mm of clear glass.
  - Leave the toplights clear glass.
  - GLS-01 already allows rows anywhere on the glass. Gilt letters across the head of the main pane is the usual shop practice. This is my judgement: no photograph of a 1990 pawnbroker's glass was reached.
  - Add a check: at STREET_SQUARE and STREET_30, no ink pixel of a glass row lies behind a bar, mullion or bead.

## Narrow points, each with its exact fix

### N1. The night stand-in light pokes through the glass: the burnt-white bar, the glowing frame and the over-bright pavement

**What the picture shows (STREET_SQUARE night and STREET_30 night):**
- A pure-white bar runs under the transom across all three lights (STREET_SQUARE: y 518 to 532, x 900 to 1680; 1600: y 324 to 333). In the head band (z 2250 to 2390), 32 per cent of the pixels are at 250 or above at STREET_SQUARE and 35 per cent at STREET_30.
- The mullion fronts glow (x 1143 to 1159 and 1401 to 1417, y 580 to 860). Their visible pixels reach p95 228 at night, against 182 under the overcast sky by day.
- The pavement in front of the window measures 113 at night (x 860 to 1760, y 1075 to 1145). That is nearly its day value (119), and brighter than the lit glass between the grille's bars (66.8) or the display zone (62.1).

**Cause:**
- `sw_gate.py` (lines 339 to 348) puts the 3.2 x 0.18 m rect light at y_m -0.02, tipped 28 degrees from the horizontal, so it spans y_m -0.099 to +0.059.
- So it stands 50 to 70 mm in front of the glass (d 30 to 36), and 7 mm in front of the mullion fronts (d 92). Its emitting face is seen from the street and it lights the frame from in front.
- NOTES.md says the frame glows because of "the spill as the game will light it". It does not: the stand-in is in the wrong place.

**What it is:** The game's asset is not affected, so this is narrow. But the night pictures are not fit for Jafar's page until it is fixed.

**WHOSE:** the builder (the gate).

**EXACT FIX:**
1. Put the spill's centre at y_m +0.10 and z 2.30, so the whole rect stands at least 50 mm behind the glass's inner face.
2. Set `ro.visible_camera = False`.
3. Re-render both night views.
4. Re-measure LIT-05 on the glass only, with the mullions, frame and beads masked out. Today it is 45.4 against the floor of 45. Its zone currently includes the glowing mullions.
5. Require all of these:
   - the head band's share at 250 or above is under 1 per cent;
   - the mullion fronts are darker than the display glass beside them;
   - the pavement pool is no brighter than the lit glass.
6. If LIT-05 then falls short, raise the spill's strength. Do not move it forward.

### N2. A see-through slot at the window end in STREET_30 (day and night)

- **Where:** a vertical sliver 6 to 7 px wide at x 1668 to 1674, y 320 to 900. It runs beside the right pilaster's shaft, then the console and the cornice.
  - By day it shows the HDRI.
  - At night it shows the world's blue (13, 15, 25 against the brick's 26, 5, 2).
- **Cause:**
  - The pilaster's shaft and core stop at x 2.970 m, and the console and cornice at 2.946 to 2.953.
  - The gate's wall opening is the full bay (±3.0), and nothing stands behind it.
  - FRN-07 only draws u 350 to 5650, so it cannot see the bay's outer 30 to 54 mm.
- **WHOSE:** the builder (the gate's context). The game's street facade must close the same gap; that is owed on the PC.
- **EXACT FIX:**
  - In `sw_gate.py`, add a brick pier behind each pilaster: x_m ±2.65 to ±3.0, y 0 to 0.30, z 0 to 3.56, in the wall's brick material.
  - Extend FRN-07 to u 0 to 6000 against the wall.
  - Add a PC row: no sky pixel inside the bay's outline at STREET_30.

### N3. The side door's fanlight shows the pawnshop

- **Where:** STREET_SQUARE day, x 444 to 641, y 510 to 586 (1600: x 278 to 400, y 319 to 366).
  - A wall clock and the pegboard of the shop's left wall are seen through the fanlight over the buttermilk side door, by day and at night.
  - The side door leads to the stair for the flat above, not into the shop.
  - The room card spans the side door's slot (card x 15.35 to 20.65; the side door is x 19.706 to 20.65).
- **WHOSE:** the target. Nothing is specified behind the side door, and the card covers the whole width between the pilasters.
- **EXACT FIX:** a hall behind the side door, in the gate and in the game. Either:
  - an opaque box over u 350 to 1294, 1.2 m deep from the frame's back face, with plaster walls and a ceiling at half the room's brightness, unlit at night; or, at least,
  - a backing plane 0.25 m behind the fanlight in a dark hall colour (sRGB 52, 46, 40) that hides the card.

### N4. The three balls carry no UVs, and do not touch their ring

- **No UVs:**
  - `bmesh.ops.create_uvsphere` is called without `calc_uvs=True` (`sw_front.py` line 549).
  - So the glb's `sign_ball_1` to `_3` have no TEXCOORD_0, and their materials point their textures at `texCoord: -1`, which is invalid glTF.
  - The 4.1 gilt face maps cannot land. The balls render as flat, matte olive spheres (STREET_SQUARE x 256 to 420, y 312 to 441), and the game's import may reject or mis-map them.
  - FAS-02 says "each ball carries its 4.1 face map". The material does reference the map, but the map cannot land.
- **No contact with the ring:**
  - The ring is at x -2.853 to -2.797 m, z 3.122 to 3.178.
  - Each top ball's surface is 38 mm from it (centre distance 0.168, radius 0.13).
  - From the street this reads as joined. From under the sign it would not.
- **WHOSE:** the builder.
- **EXACT FIX:**
  - `create_uvsphere(..., calc_uvs=True)`, then re-export.
  - Add three 10 mm rods from the ring to each ball's top.
  - Add a check row: every textured primitive carries TEXCOORD_0, and every `texCoord` is 0 or more.

### N5. From the street the window is thin on jewellery, so it reads more like a second-hand shop than a pawnbroker's

- **Where:** STREET_SQUARE day, the display, x 900 to 1680, y 700 to 930.
  - Three sparse tiers: the middle tier holds five pieces over 3.35 m, and the bed's front is a row of navy pedestals.
  - From 8.76 m you see vases, clocks and cameras. Nothing reads as rings, chains or watches; the trade is carried by the balls and the board.
  - The approved display (`rita-day-kit-2026-10-06.jpg`) had ring trays and watch pads across the bed's front.
  - The builder dropped them (NOTES judgement 6). The target keeps the display "as built", changing only marked models, and the scripted trays carry no marks.
- **WHOSE:** the builder.
- **EXACT FIX:**
  - Put the approved display's scripted ring trays, watch pads and chains back along the bed's front: w 0 to 0.04, v 0.05 to 0.20, u 0.10 to 3.25, under the pieces of the target's table.
  - The close reviewer judges the arrangement.

## The builder's five "plainly bad things", judged at street distance

| builder's item | my judgement |
|---|---|
| glass rows 'W TCHES', 'JEW ELLERY', 'OANS' | **FAULT (F2)**, the target's |
| fascia wear darkens the board | **FAULT (F1)**, but the cause is the height map exported as a normal map, not the wear |
| window frame glows white at night | **narrow (N1)**, but the cause is the stand-in light poking 50 to 70 mm through the glass, not the game's spill |
| stock-wall goods scaled up to 1.45 | **not seen as wrong from the street.** A mantel clock nearly a television's width shows only to a careful eye at 8.76 m. It is the close view's to judge. Exact fix if that view fails it: cap the scale at 1.15 and let the target raise its counts |
| counter jewellery a row of points | **not seen from the street at all**: the display stands in front of the counter. The close view's |

## What is right

- **The front as a whole:**
  - It reads as a Victorian parade's timber shopfront: pilasters, consoles, a 550 board, the cornice, the sill, a panelled stallriser, and a 3L-9T window with the mullions carried up.
  - The proportions sit beside the Hook sheet's fronts and P1's height ratios.
  - The band above the doors is built and closes the hole the target review found. It matches the approved front: the panel over the side door, three toplights over the shop door, and the transom and head.
- **Colours:** oxblood, yellowed white and the buttermilk side door belong with the Hook sheet's painted fronts.
- **The doors are handed right:**
  - the shop door's lever on the left and its hinges on the right;
  - the side door's centre knob, with the lock on the pier side;
  - nothing is mirrored, and no text reads backwards.
- **The door's small signs read:** the hours plate ("MON-SAT 9-5.30 / WED 9-1 / SUN CLOSED", the period's early closing), OPEN by day and CLOSED at night, and the 5 on the fanlight.
- **The window is glass with a lit, stocked room behind it.** I checked for black voids, white boards and flat colour:
  - **By day:**
    - The mean luma over the glass is 49.8 at STREET_SQUARE and 46.0 at STREET_30 (p5 24 and 18, p95 90 and 92).
    - No pixel is under 3, and only 0.4 and 1.4 per cent are under 12.
    - The largest uniform patch (9 px standard deviation under 1) is 1.7 per cent of the glass: a piece of dado.
    - The brick beside reads 84, so the glass is dimmer than the wall by day, as D5 and P1 and P3 ask.
  - **At night:**
    - The glass reads 54.2 with the grille, and 66.8 between its bars. The brick beside reads 21.6 and 19.8: the window is about three times the wall.
    - What is under 12 at night is the grille's lattice (29 per cent of the glass at STREET_SQUARE), not a void.
  - The stock wall, the pegboards and the lit back room read from both cameras.
- **The grille:**
  - At night it reads as a plain period lattice over a lit window.
  - By day only the black rail and channel stand, and they are discreet.
- **The three balls** hang at the door end, at the right height, as a triangle. They and the board say "pawnbroker" from across the street.
- **Content:** no alcohol, gambling or child is shown. No firm's name or brand is legible at street distance. I read both cameras at full size; the only words are CASH LOANS, ALL ELECTRICAL GOODS TESTED, OPEN / CLOSED, the hours, the 5s and the board.

## The 41 check rows: which I trust

- **Trusted (35)**, as measured on the real pictures, meshes or files:
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-05, DSP-01, DSP-02, INV-01 to INV-06, NEV-01, NEV-02;
  - FRN-01 to FRN-05, FRN-07 (for u 350 to 5650 only: see N2);
  - GLS-01, LIT-04, LIT-06, CAM-01, X-PRV.
- **Pass but do not prove what they say (2):**
  - FAS-01: the maps are in the glb, but the height map went in as the normal map and the wear map is absent (F1).
  - FAS-02: the balls' places are right, but their face maps cannot land without UVs (N4).
- **The cloud's stand-ins only (4):**
  - LIT-01 and LIT-02 are computed on the card's bake alone, with no display, frame, glass or lattice. My render measures agree with them within 3 levels by day.
  - LIT-05 is measured on the render, but under the misplaced spill, and the glowing mullions are inside its zone. On the glass alone it is 45.4 against 45 (N1).
  - PRJ-02 is the gate's own `trace`, as the row itself says.

## What I cannot judge from these files

- **The game's glass:** the street and the sky in the panes (the Hook sheet's bar, RULINGS 3 October) and the dirt. Here the glass reflects only an empty gate.
- **The game's light and picture:**
  - Lumen on the display, and the game's spill and its pool on the pavement (the approved night shot also has a bright pool).
  - The exposure.
  - The street lamps' pools. The gate's two lamps are assumed and wash the wall evenly orange; the context is not to be judged.
- **Wear on the front.** It is spotless here. The game puts the foot's dust band in M_LedgerSurface (DECISIONS 7 October), and the 3.2 kit left wear out.
- **The pictures at true size and in motion:**
  - TSR on the lattice (diamonds about 28 px wide at 8.76 m; they may shimmer further off);
  - the card's parallax as the player walks;
  - 64-sample softness.
- **Whether the game's street facade closes behind the pilasters (N2).**

**Next:** fix F1 and F2 (the target's owner settles F2's place), and N1 to N4. Re-export, re-render the four street pictures, and send them to try 2 of the street view.
