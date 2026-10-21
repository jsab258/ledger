PASS

# Rita's front, the STREET view: fresh review, try 2 (cloud week 42, unit 7 part 2, 13 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the front. I judged the street view only and did not read the close review. Jafar's ruling of 9 October applies: a piece that fails only on narrow points (each a small detail with an exact fix) passes, with those points listed for the builder.

**What I read:**
- CLAUDE.md and RULINGS.md (1, 2, 3 and 8 October).
- My try 1 review, `REVIEW-v1-street.md`.
- NOTES.md in full: the try 2 section, the second pass, the judgements and "Where a review was wrong".
- TARGET.md sections 3, 4.1 to 4.3, 6 and 13.
- `checks/check_ritas_v2.json`, all 58 rows.
- The parts of `sw_gate.py` and `sw_front.py` that make what I saw: the glass, the spill, the piers, the side door and the hall.

**What I looked at:**
- The v2 previews `ritas-street-square-{day,night-lit}-v2`.
- The gate frames, all from 05:16 to 05:47 on 13 October, the newest: STREET_SQUARE and STREET_30, day and night_lit, at 2560 x 1440 and in crops up to 6 times.
- The gate's check renders: the glass mask, the room mask, the render with the glass's reflection off, and the front against a white backdrop.
- The cards baked through `trace`.
- The before-and-after sheet (v2) and the approved front (`rita-day-kit-2026-10-06.jpg`).
- The Hook sheet and P1.

**What I measured:**
- Rec.709 luma (0 to 255) over the gate's own glass masks, the fascia, the stallriser, the brick, the pavement, the fanlights and the toplight panes.
- Ray casts from the STREET_SQUARE eye into `ritas_front.glb` (imported with bpy), plus that glb's object bounds beside the side door.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview JPEG).

**Verdict: no fault blocks.**
- Both try 1 faults are fixed by day.
- Every try 1 narrow point is fixed, except the front row of jewellery. It is back in the display, but it sits below what the far pavement can see.
- Six narrow points remain, each with an exact fix. The first is new: try 2's side-door jambs widened a pure-black strip beside the side door from 24 to 53 mm. The cause is overlapping faces in the game's own glb, so it must be fixed before any picture goes to Jafar.

## 1. Try 1, item by item

| try 1 item | now | where, and the measure |
|---|---|---|
| **F1** fascia black-streaked, name hard to read | **FIXED by day; at night NOT FIXED** (now narrow point 4, see why there) | **By day:** a clean maroon board with a few pale flakes. RITA'S and PAWNBROKER read at both cameras (STREET_SQUARE x 429 to 1677, y 285 to 395; 1600: x 268 to 1048, y 178 to 247). FAS-01n: the normal map is a real one (mean 128, 128, blue 200 or more on 100 per cent). My measure at STREET_SQUARE: ground 66.2 (FAS-01c 61.4), stallriser 56.7, gilt letters p75 123.9, letters to ground 1.87 (FAS-01c 2.02; the masks differ). STREET_30: 77.8 against 56.9, 1.37 (try 1: 1.24); it reads at full size and at 1600. **At night** the letters are 11.8 against a ground of 12.0 (0.99; try 1: 1.15), and 1.25 at STREET_30. The gilt now reads a shade darker than the board |
| **F2** glass rows cut by the toplight bars | **FIXED** | WATCHES, JEWELLERY and LOANS stand whole at the head of the three lights: STREET_SQUARE x 945 to 1105, 1180 to 1380 and 1485 to 1590, y 523 to 548; STREET_30 about y 555 to 580. GLS-02: no ink point lies behind a bar, mullion or bead at either camera. At night they read as dark letters against the lit room, as gilt on glass does after dark. The toplights are clear glass |
| **N1** night stand-in light in front of the glass | **FIXED** | No white bar under the transom (LIT-07: head band at 250 or above 0.0000 at both cameras; try 1: 0.32 and 0.35). The mullion fronts are 17.5 (p95 32.7) against the display glass's 51.4. The frame and band are lit only by the lamps; nothing glows. Condition 3 (the pool) was my error: see section 2, item 5, and narrow point 5 |
| **N2** sky slot beside the right pilaster at STREET_30 | **FIXED in the gate** | x 1660 to 1680, y 330 to 890 now shows brick in shade, RGB (84, 60, 54) by day against the lit brick's (102, 78, 73), and (39, 9, 1) at night against (42, 12, 2). No sky. The game's street facade still has to close it (PC-04, owed) |
| **N3** the shop seen through the side door's fanlight | **FIXED** | The fanlight's pane (STREET_SQUARE x 470 to 620, y 525 to 562) shows a dark hall: luma 34.3 by day (sd 3.7) and 8.3 at night; 35.1 and 10.5 at STREET_30. FRN-09: none of 560 rays reaches the card |
| **N4** balls without UVs, not touching the ring | **FIXED** | The 4.1 gilt face lands: the seam and the worn gilt show at STREET_SQUARE x 269 to 410, y 314 to 437. Three rods run from the ring to the balls. FAS-03: no textured primitive lacks TEXCOORD_0 in any of the three glbs |
| **N5** thin on jewellery from the street | **PARTLY** (now narrow point 3) | The approved front row is back: 4 ring trays with 96 rings, 4 watch pads with 28 watches, 2 chains (INV-04). But from the far pavement it lies under the sight line over the window's bottom rail. Only a row of points shows at STREET_SQUARE x 905 to 1650, y 916 to 919; above it is the step's maroon front (y 890 to 916). The cause is in narrow point 3. My try 1 fix did not allow for the sight line |

**The builder's five "plainly bad things" of try 1:**
- The glass rows are fixed.
- The fascia is fixed by day; the night is narrow point 4.
- The frame no longer glows.
- The stock wall is at 0.9 to 1.0 scale (SO-06). From the street nothing on it reads oversized.
- The counter's jewellery is raked now, and it is behind the display, so the street cannot see it.

## 2. Where the builder says a review was wrong (NOTES, "Where a review was wrong", items for this view)

1. **Item 3: the front row's box, the close review's followed.** Right: that is the view it is seen from. Neither box shows from the far pavement, though (narrow point 3).
2. **Item 4: the hall 0.50 m deep, not my 1.2 m.** **The builder is right.** My depth ignored the card standing 0.58 m behind the wall face, so a 1.2 m box would have cut through it. The 0.50 m hall hides the card completely (FRN-09) and reads as a hall.
3. **Item 5: my condition 3 (the pavement pool no brighter than the lit glass) cannot be met.** **The builder is right; my condition was wrong.**
   - It compared a pale pavement with a window whose glass shows dark velvet and black plastic.
   - Any spill that lights the bed through the glass lights a pale pavement brighter than that: the builder measured 88.7 against 56.7.
   - The approved night shot has exactly such a pool.
   - Cutting the spill's channel down to the display was a fair stand-in. But the gate's night now has no pool at all: the pavement is 6.4, darker than the wall above it at 18.8. Narrow point 5 says what to do.
4. **Item 7: "one cause in two places" (my N2 and the close review's two slots beside the side door).**
   - **Right for the right pilaster.**
   - **Not right for the side door.** The slots there were never open: F1's own frame jambs, clipped to the slot, already filled u 350 to 423 and 1221 to 1294. In the glb they are `frame_jamb_R` at x -2.650 to -2.577 and `frame_jamb_L` at -1.779 to -1.706, white, front face at d 100. FRN-08 finds no backdrop there from any camera.
   - The black was the 24.4 fillers, whose fronts are coplanar with F1's jambs (try 1's previews show a 3-pixel black line at 1600). The try 2 jambs, also coplanar, made it 53 mm (narrow point 1).
5. **Item 8: try 1's NOTES blamed the wear map.** Acknowledged and right.
6. **Items 1, 2 and 6 (the stock wall's tiers, the vases, the boards)** are the close view's.
   - The television sets on two tiers read right through the window.
   - The open wall above them is hidden behind the transom and the glass rows.
   - The right board is seen only as a grazing wedge at STREET_SQUARE and not at all at STREET_30.
   - Nothing there looks wrong at 8.76 m.

**The two rows that fail on purpose:**
- **LIT-02b at STREET_30: not a fault.** The dark pixels are shelf shade, not a void: the shade under the upper tier and between the stock-wall shelves, STREET_30 day x 1204 to 1274, y 730 to 836. With the glass's reflection off they are RGB (15, 8, 5); in the real frame they are luma 15.2, and half of them are over 12. The row's rule wants changing (narrow point 6).
- **ROOM-02 (the right board 18 per cent covered): not a point from the street.** That board is not seen from either street camera in a way a player would notice. It is the close view's to judge.

## Faults, worst first

None.

## Narrow points, each with its exact fix

### 1. Pure-black strips beside the side door: overlapping coplanar parts (new in size, try 2)

- **Where:**
  - STREET_SQUARE day: x 433 to 443 and x 642 to 652, y 510 to 1058. That is luma 0 to 3, full height from the transom to the threshold (1600: x 271 to 277 and 401 to 408).
  - STREET_30: x 738 to 743 and 855 to 859.
  - Night: the same places.
- **What it looks like:** the buttermilk door appears framed by two black slits 53 mm wide, as if the frame did not meet the pilaster or the shop door's frame. Try 1 had the same line, 24 mm wide.
- **Cause:**
  - In `sw_front.py`, `side_filler_l/r` (oxblood, u 350 to 374.4 and 1269.6 to 1294, d 0 to 100) and `side_jamb_l/r` (white, u 374.4 to 403 and 1241 to 1269.6, d 0 to 100) overlap F1's own clipped frame jambs. Their front faces share F1's plane at d 100.
  - In Cycles, a point on one face is shadowed by the coincident face of the other box, so it renders black.
  - In the game the same glb will z-fight: oxblood against white over the fillers' 24 mm, flickering under TSR.
- **Why narrow and not a fault:** from 8.76 m it is 11 pixels of 2560 beside a door, where a dark reveal is plausible. The fix is three lines with no design question. From 1.5 m it may weigh more; that is the close view's call.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. In `sw_front.py`, after "trim at the shop transom", clip F1 at the fillers' inner faces: `lo + 0.0244` and `hi - 0.0244` (u 374.4 and 1269.6) instead of at the slot's edges. F1's own white jambs then stand at u 374.4 to 423.4 and 1220.6 to 1269.6, and the target's oxblood fillers at u 350 to 374.4 and 1269.6 to 1294, with no overlap.
  2. Delete `side_jamb_l/r` (lines 477 to 480). F1's jambs are the jambs.
  3. Re-export and re-render the four street frames.
  4. Add a row FRN-10:
     - No two meshes of the front overlap in volume: each part's box inset 1 mm, the DSP-03 test applied to the front.
     - In every gate frame by day, no pixel of the front is under luma 8 outside the glass, the two fanlights and the shop door's glass. Today about 12,000 pixels at STREET_SQUARE fail this.
  5. Note FRN-07 and FRN-08 cannot see this. Overlap leaves no gap and no backdrop.

### 2. The gate's night glass draws everything behind it two or three times

- **Where:**
  - **STREET_30 night**, the second light: the red projector reel at x 1240, y 697 has a ghost at x 1270, and the white vase at x 1313 a ghost at x 1350 (y 660 to 720). The whole display is doubled about 30 to 37 pixels sideways.
  - **STREET_SQUARE night**, the toplights over the window's first four panes (x 987 to 1232, y 426 to 478): eight stripes a pane (battens at luma 140 with ghosts at 85), reading as louvres. The same panes with the glass's reflection off show the three battens only, as the card does.
- **Measured:** over the window's glass at night, p95 of |frame minus the reflection-off render| is 32.9 at STREET_30 and 17.2 at STREET_SQUARE. By day, with all the reflection, it is 24.4 and 23.2.
- **Cause:**
  - `sw_gate.py` lines 172 to 189: at night the pane is Mix(0.2) of Transparent and a Glass BSDF.
  - The Glass BSDF refracts at each face of the closed 6 mm pane on its own. A ray that refracts at one face and passes the other unbent lands up to 0.13 to 0.32 m off on the card at 30 degrees, so each image comes with two 16 per cent ghosts.
  - By day the pane is all Glass BSDF: in and out, no ghost.
  - The game's `glass_specular_night` 0.2 scales reflection only; it refracts nothing.
- **What it is:** a gate stand-in; the game's asset is untouched. But the night pictures are not fit for Jafar's page until it is fixed.
- **WHOSE:** the builder (the gate).
- **EXACT FIX:**
  1. At night, replace the Glass BSDF in the mix with a Glossy BSDF (GGX, roughness 0.02, white).
  2. Drive the mix's factor with 0.2 times a Fresnel node at IOR 1.5, not the constant 0.2. The result is 0.2 of the pane's reflectance, nothing refracted.
  3. Leave the day glass as it is.
  4. Re-render both night street views and both night close views.
  5. Add a check row: at night, p95 of |frame minus reflection-off render| over the glass is at most 15 levels at every camera.

### 3. The jewellery front row cannot be seen from the far pavement

- **Where:** STREET_SQUARE day, the foot of all three lights (x 905 to 1650, y 890 to 919): a maroon band (the step's front face) with a row of points under it. The trays and pads do not read.
- **Cause:**
  - The eye is 1.60 m up and 8.76 m from the glass. The sight line over the bottom rail and bead (about z 0.637) falls 0.11 m a metre, so it meets the bed (w 0) about 0.34 m behind the glass.
  - On the front strip (v 0.04 to 0.22), anything lower than 28 mm (at v 0.04) to 8 mm (at v 0.22) is hidden. The trays, the rings and the pads stand 0 to 30 mm.
  - DSP-03 passes because it asks for half the silhouette "from CLOSE_35 or STREET_SQUARE".
- **What it is:** still narrow. The board, the balls and now the readable WATCHES / JEWELLERY / LOANS carry the trade from across the street. But the window is the shop's sign, and a pawnbroker's window shows its rings.
- **WHOSE:** the target (section 4.5 puts the strip flat at w 0 to 0.03), and my try 1 fix, which set the same box.
- **EXACT FIX:**
  1. A velvet riser under the front strip, raked 20 degrees: w 0.05 at v 0.04 rising to w 0.115 at v 0.22, meeting the step (w 0.12, v 0.24).
  2. The 4 trays, 4 pads, 2 chains and the small pieces lie on it as laid now. A raked pad is the period jeweller's way.
  3. Change DSP-03 so that every front-row piece shows at least half its silhouette from STREET_SQUARE itself.
  4. The close reviewer judges the arrangement.

### 4. At night the fascia's name is not readable from the street

- **Where:** STREET_SQUARE night, the board (x 429 to 1677, y 285 to 395). The gilt letters are 11.8 against a ground of 12.0, so the name shows only as a faint relief. STREET_30: 16.1 against 12.9.
- **Cause:**
  - The gilt is metal and mirrors the gate's black night world.
  - The board is lit only by the two assumed lamps, 9 and 11 m to the side.
  - The target asks for no light on the board.
  - A real unlit gilt board under sodium lamps also reads dark; what it does not do is read darker than its ground. The game's reflections of the lit street will differ.
- **What it is:** narrow, not a fault. The lit window, the grille and the three balls say "pawnbroker" at night, and the gate's lamps are not to be judged.
- **WHOSE:** the target's owner and the PC (not the builder).
- **EXACT FIX:**
  1. Add a row owed on the PC (PC-06): at night in the packaged game, from STREET_SQUARE, the RITA'S letters and the board's ground differ by a ratio of 1.3 or more either way.
  2. If the game does not give it, a light over the board is a look decision for Jafar's page, one line, from the target's owner.

### 5. The gate's night has no pool of light in front of the lit window; drop my condition 3

- **Where:** STREET_SQUARE night, the pavement in front of the window (x 860 to 1760, y 1075 to 1145). It measures 6.4, under the wall's 18.8 and far under the lit glass's 61.5. The approved night shot has a bright pool.
- **Cause:** my try 1 condition 3 (section 2, item 5), which the builder met by taking the pavement off the spill's channel.
- **WHOSE:**
  - me (the condition);
  - the builder (the gate);
  - the pool in the game is the game's (PC-02).
- **EXACT FIX:**
  1. Strike condition 3 from LIT-07. Conditions 1 and 2 stay: under 1 per cent burnt in the head band, and the mullion fronts darker than the display glass.
  2. Add the gate's `footway` plane, and nothing else, to `spill_receivers` in `sw_gate.py`. The window frame, mullions, band, front and lattice stay off the channel. The lattice will still cast its diamond shadow into the pool, as it should.
  3. Re-render the two night street views after point 2's glass fix.
  4. Show the pool on his page as "the gate's stand-in; the game's own is owed (PC-02)".

### 6. LIT-02b's limit at the street cameras measures shelf shade, not a void

- **Where:** STREET_30 day and night, x 1204 to 1274, y 730 to 836: the second light's lower left. These are 1.13 and 1.29 per cent of the room's glass pixels in small patches, the largest 0.63 and 0.67 per cent.
- **What it is:** the shade under the upper tier and between the shelves, RGB (15, 8, 5) with the reflection off. It is not a slab. At STREET_SQUARE the same row passes.
- **WHOSE:** the check (the target's row, run by the builder).
- **EXACT FIX:**
  1. At STREET_SQUARE and STREET_30, LIT-02b's limit becomes the largest connected patch of room pixels under luma 12: at most 1 per cent of the glass. Today 0.63 and 0.67 pass.
  2. Keep the 1 per cent share limit at CLOSE_35_B, the camera of the slab it was written for.
  3. No change to the dado or to the game's 0.15.

## What is right

**The front:**
- It reads as a British Victorian parade's timber shopfront:
  - two oxblood pilasters on plinths;
  - scroll consoles;
  - a 550 board under a 150 cornice;
  - the sill and a three-panel stallriser;
  - a 3L-9T window with the mullions carried up;
  - the band over both doors (the panel over the side door, three toplights over the shop door, the transom and the head).
- The proportions sit beside the Hook sheet's fronts and P1's heights.
- Oxblood, the yellowed white and the buttermilk side door belong with the Hook sheet's painted fronts.
- Nothing floats. The balls hang from their ring on rods, on a bracket that projects 0.85 m: the 96-pixel lean to the left at STREET_SQUARE is that projection's perspective, not a turned part.
- Nothing is mirrored and no text reads backwards.
- The vertical letter plate in the side door's centre muntin is a period form.

**The lettering:**
- RITA'S / PAWNBROKER, the two 5s on the board, and the 5 on the shop door's fanlight read by day from both cameras.
- WATCHES / JEWELLERY / LOANS read whole.
- So do the hours plate (MON-SAT 9-5.30 / WED 9-1 / SUN CLOSED) and OPEN by day.

**The window is glass with a lit, stocked room behind it.** None of it is a void or a white board.

| measure | STREET_SQUARE | STREET_30 | try 1 (SQ / 30) |
|---|---|---|---|
| day, glass mean luma | 57.9 (p5 26, p95 124) | 56.2 (p5 21, p95 129) | 49.8 / 46.0 |
| day, under 3 / under 12 / 250 or above | 0 / 0.10% / 0.06% | 0 / 0.80% / 0.05% | |
| day, largest uniform patch (9 px, sd under 1) | 2.4%: the brown dado between the tiers, luma 36 | 2.7%: the left return's plaster, luma 73 | 1.7% |
| brick beside, by day | 84.5: the glass is 0.69 of the wall, dimmer, as D5, P1 and P3 have it | 83.9 | 84 |
| night, glass between the lattice's bars | 61.5 | 59.0 | 66.8 |
| night, the window as seen, lattice included | 41.5 | 41.3 | 54.2 |
| night, brick beside | 18.8: the window is 2.2 times the wall as seen, 3.3 times between the bars | 20.1 | 21.6 |
| night, under 12 | 10% of the glass (the display's velvet and black plastic); 37% with the lattice (its bars) | 6% / 27% | |
| night, largest uniform patch | 0.12% | 0.09% | |

**At night:**
- The lattice reads as a plain period grille over a lit window.
- The room, the stock wall and the display are lit behind it.
- The frame is lit only by the lamps; no white bar, no glowing mullion.
- By day only the black rail and channel stand, and they are discreet.

**Against the before-and-after:**
- The new room is plainer than the approved one: real-size stock and flat boards.
- Through the window at street distance its back wall still reads as stocked shelves of sets, radios, clocks and boxed goods behind a display of vases, clocks, cameras and a boombox.

**Content:**
- No drink, gambling, child or person is shown.
- No firm's name or brand is legible in any of the four frames at full size. The only words are the project's own.

## The 55 check rows: which I trust

- **Trusted (45)**, as measured on the real pictures, meshes or files:
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-06, DSP-01, DSP-02, DSP-04;
  - INV-01 to INV-06, NEV-01, NEV-02;
  - FRN-01 to FRN-05, FRN-09;
  - FAS-01, FAS-01n, FAS-01c, FAS-02, FAS-03;
  - GLS-01, GLS-02, LIT-04, LIT-06;
  - ROOM-01, ROOM-02, CAM-01, X-PRV.
- **Pass but do not prove what they say (3):**
  - FRN-07 and FRN-08: an elevation and a backdrop cannot see two parts overlapping in one plane (narrow point 1).
  - DSP-03: "from CLOSE_35 or STREET_SQUARE" lets the front row pass while the street cannot see it (narrow point 3).
- **The cloud's stand-ins only (7):**
  - LIT-01 and LIT-02 are computed on the card's bake alone.
  - LIT-02b, LIT-05, LIT-07 and PIC-05g are measured on gate renders, whose glass, lamps and spill are stand-ins set by eye. LIT-05 and the night rows will move with narrow point 2's glass.
  - PRJ-02 is the gate's own `trace`, as the row says.
- The two failing rows are judged in section 2: neither is a fault.

## What I cannot judge from these files

**The game's glass:**
- the street and the sky in the panes (the Hook sheet's bar, RULINGS 3 October), the dirt, and the night hand-over;
- here the glass reflects only an empty gate.

**The game's light:**
- Lumen on the display, and the game's spill and its pool (PC-02).
- The exposure.
- The lamps' pools. The gate's two lamps are assumed and wash the wall evenly orange.
- How bright the display's whites are at night. The stand-in spill (175 Blender watts, by eye) clips the white vase, the blue-and-white vase and the standing frame: 1.5 per cent of the glass at 250 or above, STREET_SQUARE x 1022 to 1294, y 659 to 736.

**Wear on the front:**
- It is spotless. P1 is chipped and grimy.
- The D53 layer is owed on the PC (PC-05).

**The pictures at true size and in motion:**
- TSR on the lattice;
- the coplanar flicker in narrow point 1 if it is not fixed;
- the card's parallax as the player walks;
- 32-sample softness in the gate frames.

**Whether the game's street facade closes behind the pilasters (PC-04).**

**Next:** fix narrow points 1 and 2 first (the front's glb and the gate's night glass). Then 3, 5 and 6. Re-render the four street frames, and give narrow point 4 to the target's owner. None of this blocks the pass. Do not show the night pictures to Jafar until points 1 and 2 are fixed.
