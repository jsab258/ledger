PASS

# The ironmonger (west_north bay 1, no. 16), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. I judged the street view only (STREET_SQUARE and STREET_30, eye 1.6 m above the footway, 8.76 m from the glass). I did not read the close review. Jafar's ruling of 9 October applies: a piece that fails only on narrow points (each a small detail with an exact fix) passes, with those points listed for the builder.

**What I read:** CLAUDE.md; RULINGS.md (1, 2, 3 and 8 October); NOTES.md (the lessons "For the next nine shops", batch A's ironmonger section and lessons 16 to 25); TARGET.md sections 3, 5.8 and 13; Rita's four reviews; `checks/check_ironmonger_v1.json` (made 22:53, 58 of 61 pass); the parts of `sw_gate.py`, `sw_gate_run.py`, `sw_display_gen.py` and `sw_room_gen.py` that make what I saw.

**What I looked at:** the four street previews of 13 October (street square day, night_dark, night_lit; the three room pictures); the gate frames STREET_SQUARE (day, night_lit, night_dark) and STREET_30 (day, night_lit) at 2560 x 1440, whole and in crops up to 4 times; the Hook sheet; Rita's approved front (`rita-day-kit-2026-10-06.jpg`) and her v3 street preview; the 4.1 ironmonger board (`fascias-ironmonger-v2`) and the 4.1 hanging-sign sheet.

**What I measured:** Rec.709 luma (0 to 255) of the sRGB frames over the glass, the toplights, the door glass, the brick, the pavement, the stallriser, the side door and the fascia, with my own pinhole projection from the gate's camera files (my glass rectangles agree with the gate's glass mask: 290,476 of its 293,944 pixels); the fascia's letters against its ground by projecting the 4.1 base colour map; the front glb's 272 parts (bounds, and an inside test for the sign's chain links and board); both glbs' normal maps and UVs read from the files.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview JPEG).

**Verdict: no fault blocks.** The front reads, from the far pavement, as a British Victorian parade's ironmonger built from the 3.2 kit. The window is glass with a lit, stocked room behind it by day, and with an honestly dark room at night. The name, the trade lines, KEYS CUT, EST. 1884 and 16 read. The trade reads from the window. None of Rita's export faults is repeated. Ten narrow points remain. The first is the hanging sign: its near chain runs through the cornice and the console, and its board cuts into the pilaster's capital, in the game's own glb. The second is two hot orange corners in the toplights in the shop's real night.

## Faults, worst first

None.

## Narrow points, each with its exact fix (most visible first)

### 1. The hanging sign's near chain runs through the cornice and the console; the board cuts into the pilaster's capital

- **Where:**
  - STREET_30 day: the near chain leaves the arm at (1859, 338) and enters the cornice's top at (1859, 365); it does not come out again until the board's eye at (1859, 460).
  - The board's near edge stands against the capital and the console's foot from (1851, 463) to (1851, 527).
  - STREET_SQUARE day: the same chain shows over the console's leaf at x 2181, y 317 to 365. The board's near edge is at x 2174, y 369 to 459 (1600: x 1359, y 231 to 287).
  - At 100 per cent it is a line two to three pixels wide. In the game a player walks under this sign, and from below it will plainly look wrong.
- **Measured** on `ironmonger_front.glb` (model frame; y negative is out from the wall):
  - `sign_chain_0_*` stands at y -0.21. Links 08 to 14 (z 3.418 to 3.538) are inside `cor_cornice`, which projects 0.300. Links 15 to 24 (z 3.218 to 3.398) are inside `conR_body` and `conR_leaf`, which project to 0.293. So 0.34 m of chain is buried.
  - `sign_board_core` spans y -0.70 to -0.15 and z 2.61 to 2.99. Its near edge is inside `pilR_capital` (projects 0.175, z 2.54 to 2.85), `pilR_tablet` at z 2.62, and `conR_body` at z 2.90. That is 25 mm of board inside the joinery.
- **Cause:**
  - 4.1 puts the plate above the cornice over the pilaster, with an arm of 0.70 m and a board 0.55 wide. That leaves the board's near edge and its chain inside a cornice that projects 0.30 m.
  - No intersection test covers the front. SO-07 is the room's and DSP-03 the display's. FAS-02 checks positions only. Lesson 7 ("every placed thing goes through one intersection test") was not applied to the front.
- **WHOSE:** the target (4.1's 0.70 projection does not clear this kit's cornice) and the builder (placed without the test).
- **EXACT FIX:**
  1. Move the board out to y -0.33 to -0.88: its near edge is then 30 mm clear of the cornice's 0.300 and 37 mm clear of the leaf's 0.293. Keep x, z, the 4.1 faces and the 1.5 mm stand-off.
  2. Move the eyes, chains and rings to y -0.39 and -0.82, 0.06 in from each end as now.
  3. Run the arm to y -0.84, 20 mm past the far chain as now. Scale the brace and the scroll along y by 0.84 / 0.66 = 1.27. The plate does not change.
  4. Write the new projection (0.84) into the target's "Changes after the build".
  5. Add a row FRN-11: no mesh of the front intersects another, each mesh inset 1 mm (the SO-07 test). The sign's links, eyes, rings and board are included, and every chain stays 20 mm clear of the cornice, consoles and capitals.

### 2. In the shop's real night (night_dark) two hot orange corners glow in the toplights

- **Where:** STREET_SQUARE night_dark (the only real night of a shop that is dark at night):
  - the left end of the first toplight, x 905 to 940, y 425 to 485, luma 75.1 (RGB 131, 66, 0);
  - the right end of the sixth, x 1643 to 1652, y 425 to 485, luma 90.7;
  - the two return walls down the main lights, x 905 to 940 and 1643 to 1652, y 520 to 700, luma 38 and 35.
  - For comparison: the toplights' middle reads 16.2, the brick above the fascia 26.4 and the room's back wall 18.7.
  - In the 1600 preview (x 567 to 590, y 265 to 305) it reads as a light left on in a closed shop.
- **Cause:**
  - `ironmonger_night_dark.png` itself: its top front corners (x 0 to 60 and 4036 to 4096, rows 0 to 200) read 98.0 against a picture mean of 20.4.
  - The return walls take the picture's front columns (`col_l/col_r_night_dark`, top sixth RGB 165, 85, 0).
  - The wash light in the room rig (`sw_room_gen.py` line 239, `sw_room.py` line 1180) is the card's full width (5.3 m) at 0.9 of the height, so its two ends touch the side walls at the ceiling.
  - Street light through a window falls on the floor and the lower back wall, not into the top corners.
  - Every shop's night_dark picture has this (the pawnbroker's corners read 66 against 17.7, the tea room's 61 against 21.7). The builder's 30 per cent stronger wash (Judgement I12) makes the ironmonger's the worst.
- **WHOSE:** the kit (the room's light rig); the builder for I12.
- **EXACT FIX:**
  1. Make the wash light (W - 1.0) x 0.5 m (4.3 m for a 5.3 card), centred, at 0.6 of the height, tipped 30 degrees below the horizontal.
  2. Re-tune `sodium_ratio` to today's night_dark mean (20.4; LIT-01 at least 10).
  3. Re-render `ironmonger_night_dark.png` and the STREET_SQUARE night_dark frame.
  4. Add to PIC-03: the picture's top front corner columns are at most 1.5 times its mean. In the street frame at night_dark, no toplight strip is brighter than the brick above the fascia.

### 3. The three brooms lean heads down, and from the street they read as three white poles

- **Where:** STREET_SQUARE day, the right end of the window, x 1520 to 1640, y 705 to 915 (1600: x 950 to 1025, y 440 to 572). The heads (red and black) lie on the bed under the sill's sight line, so only a sliver shows at y 905 to 915. What reads is three white handles with red caps, like a stepladder or poles.
- **Cause:**
  - `layout_ironmonger` leans the plastic brooms head down on the bed (Judgement I8).
  - The sill hides the lowest 40 mm of the bed from the far pavement (lesson 22).
  - DSP-03 passes because the handles carry the silhouette.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Turn each broom end for end: the handle's foot on the bed at u 2.80, 2.88 and 2.96 (v 0.30 to 0.45), the head up against the right return wall, with heads 85 mm apart as now. They stay at 0.80 and lean on the return wall as now.
  2. Make DSP-03 measure the broom heads (the bristle mesh) from STREET_SQUARE: at least half seen.

### 4. The pyramid's backing board is primer grey, the palest flat field in the left light

- **Where:** STREET_SQUARE day, the left light, x 943 to 1140, y 753 to 907 (1600: x 590 to 713, y 470 to 567). It reads luma 86 to 111 (RGB 82, 87, 86: cold under the sky), 1.4 to 1.8 times the glass's mean.
- **What it looks like:** an unpainted panel standing in the window, hiding the left wall and the left of the drawer wall. The target asks for no backing board (`sw_display_gen.py` line 269, `rgb8(150, 150, 140)`). The bed beside it is the shop's dark green.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Paint the backing board the bed's dark green (30, 62, 44), roughness 0.75.
  2. Check that its visible pixels read luma 25 to 45 at STREET_SQUARE by day, so the tins' coloured labels stand out against it.

### 5. The stepped crate reads as a plain cardboard box, the window's largest flat tone

- **Where:** STREET_SQUARE day, x 1324 to 1506, y 845 to 884: luma 121.6 with a 9 px standard deviation under 1. At 2.2 per cent of the glass it is the largest uniform patch in the window.
- **Cause:** the crate is one untextured box per step in "weathered deal" (150, 113, 72).
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Give each visible face plank joints every 0.12 m: horizontal grooves 3 mm wide and 2 mm deep.
  2. Vary each plank's base colour by plus or minus 8 per cent, or use the room's CC0 Poly Haven wood texture at 1k.
  3. Accept when no 9 px uniform patch in the window covers more than 1 per cent of the glass.

### 6. A paint flake sits on the S of TOOLS, so the word reads "TOOLŜ"

- **Where:** STREET_SQUARE day, x 1033 to 1043, y 314 to 320, over the S. It is the same at STREET_30.
- **Cause:** in the 4.1 board's `ironmonger_basecolour_worn.png`, a blue-grey flake at map x 683 to 720, y 168 to 190 overlaps the letter's top.
- **WHOSE:** the kit (the 4.1 fascia set).
- **EXACT FIX:**
  1. Delete that flake.
  2. Add to the 4.1 wear script: no flake within 15 mm of a letter's outline in the name and trade rows.

### 7. The sledgehammer's yellow shaft and black grip read as a modern DIY-shed tool

- **Where:** STREET_SQUARE day, x 1622 to 1652, y 730 to 915 (1600: x 1014 to 1032, y 456 to 572), the brightest yellow in the window. The model carried a modern warning label, which the builder painted out (NOTES' table).
- **What it is:** a fibreglass shaft with a black rubber grip is the look of a post-1990s tool. A 1990 ironmonger's sledge would most often have a plain ash or hickory shaft. It is not clearly after 1992, so it is narrow.
- **WHOSE:** the builder (the model's look).
- **EXACT FIX:** in the cleaned base colour map, recolour the shaft and the grip to ash (sRGB 190, 150, 100), keeping the map's own luma variation as grain. Keep the head black.

### 8. The night_lit street preview is not this shop's night

- **Where:** `ironmonger-street-square-night-lit-2026-10-13.jpg`. It shows a lit room, a lit display and a bright pavement pool (luma 128 against the lit glass's 78), none of which the game shows for a shop that is dark at night (TARGET 5.8: lit_at_night false).
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. On Jafar's page, show `ironmonger-street-square-night-dark` as the night picture, after point 2's fix.
  2. If the night_lit picture is shown at all, caption it "the tests' state (lit room), not the game's night".

### 9. The check's three failing rows: none is a fault, and two of the rules want changing

**FRN-10** (patch of 26 x 20 px, about 0.11 x 0.09 m):
- **Where:** STREET_SQUARE x 2084 to 2109, y 600 to 619, luma 6.0; STREET_30 x 1796 to 1812, y 629 to 643.
- **What it is:** the black side door's top corner in the shade of the frame's transom hood. No coplanar faces stand there: the fillers (u 1706 to 1730.4) and F1's jambs (from 1730.4) abut and do not overlap, as lesson 1 asks. It reads as shade.
- **Rule change:** the row's pixel test skips parts painted darker than sRGB luma 40 (the side door is luma 36) wherever its geometry test finds no visible overlap.

**LIT-02b** (the STREET_30 day patch of 1.25 per cent, on the reflection-off render):
- **What it is:** the target's dark-green dado in shade. In the frame as rendered, the glass under luma 12 is only 0.46 per cent at STREET_30 by day (largest patch 0.16 per cent) and 0.35 per cent at STREET_SQUARE. The day picture's dado reads 85 to 105 at full brightness: it is paint, not a void.
- **Rule change:** a dark patch counts as a void only where the day picture under it averages under luma 40 at full brightness.

**LIT-08** (blowtorch and pump at CLOSE_35_B night_lit):
- **What it is:** a lit display at night is a state this shop never has.
- **Rule change:** LIT-08 applies only to shops with lit_at_night true. For the ironmonger it is n/a.

**WHOSE:** the check (the target's rows, run by the builder).

### 10. NOTES' "How the check went" for the ironmonger is out of date

- **What is wrong:**
  - NOTES says 55 of 61 and names PRJ-02 and PIC-05g as failing, with LIT-01 at 9.5. The check file (22:53) says 58 of 61: PRJ-02 passes at -1322.1 signed, PIC-05g at 0.0082 and 0.0088, LIT-01 at 11.5. The LIT-08 numbers also differ.
  - FAS-01c's detail says the stallriser is "225 per cent of the ground's". It is the ground that is 225 per cent of the stallriser.
- **WHOSE:** the builder.
- **EXACT FIX:** replace the section with the check file's rows, and turn FAS-01c's sentence round.

## The builder's named shortfalls (NOTES "Known shortfalls now" and the failing rows), judged at street distance

| builder's item | my judgement |
|---|---|
| the window crowded: toolboxes and cans at 0.85, brooms at 0.80, bulbs at 1.25, the sprinkler moved | **Not a point from the street.** Nothing reads small or crowded at 8.76 m. The brooms' heads are narrow point 3, which is a different cause. The bulbs are hidden by the sill there. The close view judges the scales |
| no step ladder, one paraffin can and one watering can fewer in the room, the 0.4 and 0.8 tiers not built | **Not a point from the street.** The counter and the display hide where they would be |
| pegboards about a third covered | **Not a point from the street.** The left board is a grazing wedge at STREET_SQUARE and the right board a narrow slice at STREET_30. Both read as tool boards |
| dark at night: night_lit is the tests' state, night_dark the real night | **Right, per the target.** The night_dark view is honestly dark (see "What is right"), except narrow point 2. Narrow point 8 covers which picture goes to his page |
| LIT-08: blowtorch and pump dark at CLOSE_35_B | **Narrow, and only the rule's** (point 9): the row should not apply to a shop that is dark at night |
| LIT-02b: dado shade over 1 per cent | **Narrow, and only the rule's** (point 9): paint, not a void |
| FRN-10: the side door's shaded corner | **Narrow, and only the rule's** (point 9): shade on near-black paint, no coplanar faces |
| 64 samples, not 128 | **Owed on the PC**, not a point. No noise shows at street distance |
| the hanging board black iron, unlit | **Right for a day shop.** But its geometry is narrow point 1, which the builder did not name |

## What is right

**The front.** From the far pavement it reads as a British Victorian parade's timber shopfront for an ironmonger:
- dark-green (30, 62, 44) fluted pilasters on plinths, with scroll consoles, a cream 4.1 board under a timber cornice, the sill and a two-panel stallriser;
- the T2 window: two lights and six toplights, the mullion carried up as a bar;
- the band over both doors: the fanlight with 16 and three toplights over the shop door, the fanlight and a raised-and-fielded panel over the side door, the transom and head;
- the half-glazed T1 shop door: hinges on the viewer's left and the lever on the right, as the target says, with the brass letter plate in the lock rail and the kick plate;
- the black F1 side door, with its centre knob, the lock on the pier side and the vertical letter plate in the muntin.
- Proportions and colours sit with Rita's approved front and with the Hook sheet's painted fronts.
- Nothing is mirrored, no text reads backwards, and KEYS CUT reads left to right on face a from both cameras.
- The parts meet: the fillers and F1's jambs abut, the pilasters meet the wall, and at STREET_30 there is no sky or slot beside either pilaster (FRN-08's few pixels are the bay's outer sliver, which the gate's piers close; PC-04 owed).
- The front is spotless, as Rita's is. The wear layer is owed on the PC (PC-05).

**The lettering.** These read at 100 per cent from both cameras: IRONMONGER, TOOLS & HARDWARE, PAINTS & PARAFFIN, KEYS CUT, EST. 1884 (whole in its toplight, no bar crosses it: GLS-02) and the 16 on the shop door's fanlight.

| measure | STREET_SQUARE | STREET_30 |
|---|---|---|
| fascia by day: ground / letters (mean; 25th percentile) | 136.9 / 75.8; 127.3 / 62.4, ratio 2.04 (FAS-01c 2.06) | 135.9 / 92.1; 125.5 / 77.1, ratio 1.63 |
| fascia at night_dark: ground / letters | 42.2 / 15.1, ratio 2.8: painted letters read at night (Rita's gilt did not; lesson 14 does not arise) | night_lit: 42.7 / 20.8 |

**The window is glass with a lit, stocked room by day and an honestly dark room at night.** It is never a void or a white board.

| measure | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, glass mean (p5, p95) | 61.6 (26.3, 123.3) | 62.0 (20.7, 124.2) |
| day, brick beside | 84.0: the glass is 0.73 of the wall, dimmer, as D5, P1 and P3 have it | 84.1: 0.74 |
| day, glass under 3 / under 12 / any channel at 250 or above | 0 / 0.35% / 0 | 0 / 0.46% / 0 |
| day, largest connected patch under 12 | 0.11% of the glass | 0.16% |
| day, largest uniform patch (9 px, sd under 1) | 2.2%: the crate's front face, luma 121.6 (point 5) | 2.6%: the right return wall's plaster beside the right pegboard, luma 88 |
| day, toplights; door glass | 54.0; 38.3 | 56.2; 52.7 |
| night_lit (the tests' state), glass; brick beside | 78.1; 22.5 and 18.8 (3.5 times the wall) | 78.5; 22.5 |
| night_lit, any channel at 250 or above | 0.27% (the white broom handles under the spill) | 0.44% |
| **night_dark (the real night)**, glass mean (p5, p95) | **12.3 (2.0, 25.6)**: 0.65 of the brick beside (18.9 and 17.8) and under the brick above (26.3), as a closed shop should be | not rendered |
| night_dark, glass under 3 / under 12 | 12.6% / 57%: the bed, the goods' feet and the floor in shade; above them the drawers, shelves and counter read 15 to 30 | |

Against the target's floors (composite day 33 or more, night_lit 45 or more, night_dark 10 to 35), the full frames give 61.6, 78.1 and 12.3. The day room reads: drawer wall, shelves of tins and oils, the counter with toolboxes and till, the left pegboard. The night_dark room reads, dimly, under the sodium wash.

**The trade reads from the street.** These say "ironmonger" before the board is read:
- the pyramid of 36 paint tins;
- two galvanised watering cans;
- the oil and cleaner tins on the crate, and the brass blowtorch;
- two toolboxes, and trowels raised on trays (lesson 22 applied: they show over the sill);
- the pump and the sledgehammer;
- behind them, the 60-drawer wall and the shelves of tins.

TRD-01's three families are confirmed by eye. Nothing anachronistic stands out beyond narrow point 7. The till is a plausible 1980s electronic register at this distance.

**Content.**
- No drink, gambling, child, toy or person is shown.
- Legible words at 100 per cent in the five street frames: IRONMONGER; TOOLS & HARDWARE; PAINTS & PARAFFIN; KEYS CUT; EST. 1884; 16; OPEN by day and CLOSED at night on the shop door. All are the project's own: acceptable.
- Not legible at 100 per cent: the tins' labels (at 300 per cent, fragments of the invented names such as ELMSTEAD and HARTSIDE), the 12 price cards, the drawer labels and the till's keys.
- No firm's name, maker's mark, barcode or modern packaging is legible anywhere.
- PARAFFIN is lamp and heater fuel, not drink.

**Rita's export faults, checked on the files:**
1. **A height map exported as a normal map:** not repeated. Every normal map in the two glbs (13 distinct images) is a real one; the fascia's mean is (127.5, 127.5, 254.9), with blue at 200 or more on 100 per cent.
2. **A textured primitive without UVs:** none, in either glb (272 and 64 primitives; no negative texCoord).
3. **Two parts sharing a face plane:** no black strip anywhere on the front. The only patches under luma 8 are thin cornice shade lines and the door corner of point 9.
4. **A see-through slot at STREET_30:** none.
5. **The stand-in night light or glass in view:** none. The spill is off in night_dark, and in night_lit the mullions and frame are unlit (LIT-07). No ghosting shows in the night glass at either street camera.

## The check rows: which I trust

**Re-measured, and I agree:**
- GLB-01, FAS-01n, FAS-03 (both glbs read by me);
- FAS-01, FAS-01c (my 25th-percentile ratio 2.04 against 2.06);
- GLS-01, GLS-02 (EST. 1884 and 16 whole);
- FRN-01, FRN-02, FRN-03, FRN-05, FRN-07, FRN-09 (the side fanlight shows the hall);
- NEV-01, NEV-02, INV-05 at street distance, TRD-01, CAM-01, X-PRV.

**Trusted as written, not re-measured** (the room and the display's inner rules are the close view's):
- PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
- SO-01 to SO-04, SO-06, SO-07;
- DSP-01, DSP-02, DSP-04;
- ROOM-02 to ROOM-05, INV-01 to INV-04, INV-06, LIT-06, FRN-04.

**Pass but do not prove what they say (3):**
- FAS-02: the positions are right, but the board and the near chain run through the capital, console and cornice (point 1).
- DSP-03: the brooms' handles carry their silhouettes while the heads are hidden (point 3).
- FRN-08: at the street cameras it passes on the gate's piers; the game's facade is owed (PC-04).

**The cloud's stand-ins only (8):**
- LIT-01 and LIT-02: the card's composite alone.
- LIT-02b, LIT-05, LIT-07, LIT-08, GLS-03 and PIC-05g: gate renders whose glass, lamps, spill and strips are stand-ins set by eye.
- PRJ-02: the gate's own `trace`, as the row says.

**The three failing rows:** FRN-10, LIT-02b and LIT-08 are judged in point 9. None is a fault.

## What I cannot judge from these files

- **The game's glass:** the street and the sky in the panes, the dirt, and the night hand-over. Here the glass reflects only an empty gate.
- **The game's light:**
  - Lumen on the display and the room;
  - the game's own street lamps (the gate's two are assumed, 10 m either side; they leave the pavement in front of this shop at 4.8 at night_dark and the display's foot black);
  - the exposure.
- **Wear, grime and wet on the front and the pavement** (PC-05, the D53 layer). P1 and the Hook sheet are grimier than this front.
- **The pictures in motion:** the card's parallax as the player walks, TSR, and the hanging board's sway (none is modelled).
- **Whether the game's street facade closes beside the pilasters** (PC-04).
- **GLS-03 and LIT-02b on their reflection-off renders.** Between my first listing (about 00:58 on 14 October) and 01:10, the gate's check renders were deleted from `ledger-scratch/shop-windows/ironmonger/gate/`: the masks, the reflection-off renders, the cards, the object index and the uv files. The frames and the camera files remain. My glass and front-mask measures were taken before they went; I could not re-measure GLS-03 myself.
- **Whether Jafar wants a fuller window.** A 1990 ironmonger often hung goods from the window head. This one, as the target asks, fills only the lower 0.96 m and lets the room carry the upper half. That is a taste line for his page, not a fault.

**Next:** this is try 1 of the street view, and it passes. Fix point 1 (the sign's geometry, in the game's glb) and point 2 (the night_dark wash, in the kit's room rig) before any picture of this shop goes to Jafar. Then fix points 3 to 7 and the rules of point 9, and re-render the two street frames and the night_dark view. Point 8 decides which night picture he sees.
