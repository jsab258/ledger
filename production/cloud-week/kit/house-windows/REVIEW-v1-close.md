FAIL

# House windows, the CLOSE view: fresh review, try 1 (cloud week 42, unit 8 part 2; 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the kit. One view only: the close cameras on `east_parade_bay0_upper_w1` (S22, white_grimy, N1 white voile, C2 cream curtains open, up_lounge_1 behind): `close` (the target's H_ALONG_30_NEAR, 19 degrees from the wall) and `close2` (1.5 m off the wall, 1.6 m along, 22 degrees), day and night_lit. I did not read REVIEW-v1-street.md.

Read: CLAUDE.md; RULINGS.md (3 Oct white frames, 1 and 2 Oct Poly Haven rooms, 8 Oct photographs win); TARGET.md sections 3 to 10; FIXES-APPLIED.md (head); NOTES.md; `checks/check_windows_v1.json`; the three shop close reviews (for the method); the parts of `hw_gate.py`, `hw_gate_run.py` and `hw_roomgen.py` named below; `tools/ue/make_interior_material.py` (`trace`).

Looked at: the four close previews; the four close gate frames (2560 x 1440) at 100 to 600 per cent; their masks and the night reflection-off frames; the 26 upper-room pictures; every placed model's base colour map (16 models, 23 maps), with the marked and lettering-like regions at 100 to 200 per cent.

Measured, all in my scratchpad (nothing in the repository or in the builder's scratch was changed): pane and frame luma per pane from the masks; the parallax through `trace` itself, against the frames; the four kit glbs (normal maps, texture coordinates, pane geometry, faces sharing a plane); the room pictures' clipping. **Test renders:** six small frames (1280 x 720, 16 samples, `nice -n 15`) with the gate's own code imported, unchanged but for one switch named in fault 1.

**In short.** The joinery is right: a box sash a joiner would recognise, white, with its lines. The room behind moves exactly as the game's rule says, nothing in it floats or is shrunk, no mark or lettering survives, and nothing breaks the content rule. But by day the gate's glass is a mirror at these angles: the net, the curtain and the room cannot be seen at all. That is a build fault in the gate's pane, not the sky, and it is what WB-01 failed on. At night the lit ceiling turns olive where the room picture clipped.

**2 faults, 4 narrow points.** This is try 1 of the CLOSE view.

## Faults, worst first

### 1. By day the pane is a mirror at any angle under 56 degrees from the wall: the net, the curtain and the room are invisible

- **Where:**
  - close2 day:
    - lower-right pane (1376-1522, 683-958): a flat grey at median 165, 95th percentile 169. No net, no fold, no curtain.
    - upper panes (1194-1495, 409-896): medians 18 and 33. Black reflection over the top, grey sky below.
  - close day: the whole window (1236-1376, 490-983) shows only reflections of the reveal's brick, the eaves and the sky.
  - The preview `hw-close-day` and `hw-close2-day` read as glass with nothing behind it.
- **Cause** (measured):
  - Every pane in the four glbs is a closed slab 2.5 mm thick (`glass__lower_L` in hw_S22.glb: 60 triangles, a front and a back face).
  - The gate's pane (`hw_gate.py` `make_glass_gate`) mixes Transparent and Glossy by a Fresnel node at IOR 1.789. Cycles inverts the IOR on a back face. Past asin(1/1.789) = 34 degrees of incidence the back face is total internal reflection: weight 1.0 x refl 1.0 by day.
  - So nothing passes the pane at less than 56 degrees from the wall.
  - At night (refl 0.2) the back face still takes 0.2.
  - MAT-04 passed because it renders a flat single-sided pane, not the kit's slab.
- **Proved by test renders** (the gate's own scene, cameras and cards; the frames are in my scratchpad):
  - **With the glass reflection off,** close2 shows the net plainly. The lower sash reads median 121 with soft folds, against the build's 165 flat.
  - **With only the back face's Fresnel removed**, the front face's F0 0.08 standing for both faces as target 5.1 says:

    | view | P/L, this fix | P/L, build | other |
    |---|---|---|---|
    | close2 | 0.67 | 0.36 | spread 152 |
    | close | 0.59 | 0.25 | D/L 0.31 |
    | bare window from across (WB-03) | 0.57 | 0.75 | |

    The white voile, its folds and the far cream curtain at the upper sash's edge all show (close2 test frame, lower sash about (600-780, 340-470) of 1280 x 720).
  - At night the dark windows at 51 degrees in `h-across0-bay2w0` read 29 and 64, against the build's 75 and 82.
- **Whose:** the builder: the gate's stand-in pane together with the kit's slab panes.
- **Exact fix:**
  1. In `make_glass_gate`, multiply the Fresnel factor by (1 - Geometry.Backfacing), so the back face is pure Transparent. That is 4 nodes: New Geometry, two Math nodes, relinked into the Mix's Fac.
  2. Render all 20 frames and the night reflection-off frames again, then run the check.
  3. Add a row GLS-06 that renders the kit's own `glass__lower_L` (the slab) in front of a lit card under a black sky at 20 and 70 degrees from the wall. The card must read at least 0.75 of itself.
  4. Rewrite MAT-04 to use the glb's pane node, not a plane.

### 2. At night the lit ceiling seen through the upper sash is olive, not tungsten: the room pictures clip around the pendant

- **Where:**
  - close2 night, upper-right pane (1342-1495, 409-758): mean (106, 102, 80). At (1430, 560) it reads (128, 128, 94), linear g/r 1.00, b/r 0.52.
  - 16.7 per cent of close2's glass pixels (19,600 of 117,447) and 4.4 per cent of close's read linear g/r of 0.9 or more. Tungsten-lit cloth and paint read g/r 0.55 to 0.80 (NIGHT-03).
  - It shows as a pale greenish-yellow pane in `hw-close2-night_lit` (preview about (800-850, 345-440)).
- **Cause:** in `up_lounge_1_night_lit.png` the ceiling near the rose reads (255, 253, 178). Red is clipped, so the hue goes yellow. The game's night gain (0.7 x 0.4 = 0.28) then darkens that clipped patch to olive.
- **Every lit-room picture clips.** Share of pixels with red at 250 or more:

  | room | red at 250 or more |
  |---|---|
  | up_lounge_1 | 2.79% |
  | up_bedroom_1 | 2.77% |
  | up_bedroom_3 | 2.22% |
  | up_lounge_3 | 2.21% |
  | gf_front_1 | 2.02% |
  | up_lounge_2 | 2.01% |
  | gf_front_3 | 2.01% |
  | gf_front_2 | 1.59% |
  | up_bedroom_2 | 1.50% |
  | up_landing_1 | 0.62% |
  | up_landing_2 | 0.55% |

- **Why NIGHT-03 passed:** it averages the whole pane, and only measures `h-across0-bay2w0` and the cottage. This is the shops' lesson again: a row that averages the glass misses a band.
- **Whose:** the builder (`hw_roomgen.py` night_lit lights and the 8-bit write).
- **Exact fix:**
  1. Before the 8-bit write of every night_lit picture, roll highlights off by scaling all three channels together wherever max(r, g, b) linear is over 0.85, to 0.85. Keep each picture's mean at 70 +-15 per cent (landings 40) by raising the pendant's fill, not its peak.
  2. Add a row PIC-13: no night_lit picture has more than 0.1 per cent of its pixels with a channel at 250 or more.
  3. Make NIGHT-03 measure per 32 px block of a lit pane: every block r > g > b, linear g/r at most 0.85.

## Narrow points

1. **A black notch at the head of the far jamb.**
   - **Where:**
     - close2 day: (1166-1182, 633-657), 548 px under luma 15 in the box (1140-1220, 600-690).
     - close day: (1244-1274, 637-659), 155 px.
     - close2 night: the same place.
   - The mask calls these pixels joinery (R 2), at luma 0: a joinery face that gets no light, about 35 x 35 mm.
   - **Cause:** the stand-in wall (`hw_gate.py`, the `e_pier_*` and `e_head_*` blocks) cuts the opening exactly at x +-0.425 and at the head's z. Those are the planes where the kit's outer and head linings end and run behind the brick, so faces share the brick's planes.
   - **Whose:** the builder (gate stand-in).
   - **Fix:** cut the stand-in opening 2 mm larger each side and at the head (x +-0.427, head + 0.002). Add a row JNR-01: by day no joinery pixel under luma 10 inside any window outline.
2. **The eaves' soffit reflects pure black in the top of the upper panes by day.** In close2 the upper-left pane's top 40 per cent reads 0 to 25. This is the builder's known shortfall (the stand-in `e_roof` overhang's underside is roofing in shade).
   - **Fix:** give the stand-in's 0.3 m overhang a soffit board in the house's paint (white_grimy, linear 0.66, roughness 0.48). A real painted soffit is lit by the street and reads grey in the glass, not black.
3. **The grimy paint has no grime band.**
   - Target 4.2 says 'grimy' is the lower rail and sill x 0.85 plus a grime band 30 mm high along the sill. Only the x 0.85 is built (`hw_gate.py` line 500), and only in the gate. At 100 per cent the bottom rail reads as clean as the top rail.
   - **Fix:** in the glb, set COLOR_0 to x 0.75 on `paint_joinery__lower_bottom_rail` over its lowest 30 mm (and on the oak sill's top). The target gives no number; 0.75 is a Judgement within its box shade, above KIT-09's floor of 0.25. The PC then gets it too.
4. **Two passing rows are not to be trusted until fault 1 is fixed.**
   - WB-02 passed (0.25) only because the pane was a mirror of dark things. My fixed test reads the bare window at 19 degrees **0.48** against 0.10 to 0.45.
   - WB-04 likewise: 0.06 to 0.07 in the build, 0.28 to 0.31 fixed (still inside 0.72).
   - **Fix:** re-measure both at the gate's 40 samples after the fix. If WB-02 stays over 0.45, the bright upper sky of the stand-in dome in the reflection is the cause. That is the stand-in's limit, to be judged on the PC (OWED-01), not a kit fault.

## The five failing rows

- **WB-01 (net windows 0.23 to 0.36): a FAULT in the build.** It is fault 1, not the sky's veil. With the fix: close 0.59, close2 0.67, inside 0.55 to 0.97. The row stands.
- **WB-03 (bare window from across 0.75; blue over red 4):**
  - **P/L:** a FAULT. The slab's back face adds a second reflection; fixed it reads 0.57, inside 0.35 to 0.70.
  - **Blue over red: a mis-set row.** The band comes from P8, a clear blue sky. The game's sky is the overcast photograph (15 Sep, D40; the Hook sheet), and its reflection is neutral (2 levels in my fixed test). New wording: "the pane's blue minus red within +-8 levels of the dome's own blue minus red in the reflected direction".
- **WB-07 (the flaking window 2.995 against 3.0): a mis-set row** for the one house the target painted darker on purpose.
  - The floor 3.0 comes from sound frames on film. white_flaking is linear luminance 0.58 against white_fresh's 0.81, with 12 per cent primer or bare timber.
  - New band for white_flaking: **2.2 to 9.0** (3.0 x 0.58 / 0.81 = 2.15). The other paints keep 3.0.
- **NIGHT-01 and NIGHT-02 (dark 43 to 82; lit over dark 1.3): partly fault 1, the rest a mis-set row and the stand-in's exposure.**
  - With the fix, the dark windows in `h-across0-bay2w0_night` read 29, 38, 55 and 64. The dark median falls from 67 to about 46; lit over dark is 2.5.
  - What remains is the rows themselves:
    - A dark window's white net beside a stand-in lamp is lit by the lamp as its frame is: frame L 98 to 100 at night. "Dark = 8 to 30 sRGB" (the room picture's mean) cannot hold for a net window.
    - The target's own gains (card 0.28, net 0.48) put a lit window at about its own frame's brightness (P/L 1.17). That is never 4 times a lamp-lit net.
  - **New rules, per window against its own frame at night:**
    - NIGHT-01: dark P/L at most 0.70; lit P/L at least 1.0 with r > g > b.
    - NIGHT-02: the lit median at least 2.0 times the dark median (sRGB).
  - The research's "10 to 100 times the lit paving" is the game's exposure. Add it as OWED-07 on the PC.

## What is right

- **The kit piece is a believable 1990 box sash** (close2 day at 300 to 600 per cent).
  - The far jamb shows the outer lining, the pulley stile, the parting bead and the staff bead as separate white members with dark gaps.
  - The meeting rail carries its dark underside (box shade 0.4) and the ogee horn below it.
  - The 22 mm bars are centred; the putty line runs round each pane; the white (grimy) frame follows the ruling.
  - The lines are there: D/L 0.06 to 0.07, 0.28 to 0.31 fixed; WB-04b dips 0.15 to 0.16.
  - The reveal's brick and the head soffit are mirrored in the glass as a real pane mirrors them.
- **The net and the curtain** (night, and day with the fix):
  - a gathered white voile with soft folds of varied pitch, its head casing at the meeting rail;
  - at night it is lit warm from behind, with the cream curtain seen behind it at the far side;
  - KIT-18's pitch 30 to 70 mm, no corrugation.
- **The room obeys `trace`.** Two ceiling points of up_lounge_1, both seen through the upper panes from both eyes:

  | room point (x, y, z) | card x from `close` | card x from `close2` | `trace` returns, from both eyes | the render rule's place | frame px, close / close2 |
  |---|---|---|---|---|---|
  | (-0.70, 0.30, 2.55) | 1.622 | 1.767 | (421.2, 67.7) | (421.2, 67.7) | (1320, 675) / (1249, 757) |
  | (-0.40, 0.15, 2.55) | 1.566 | 1.644 | (559.7, 35.6) | (559.7, 35.6) | (1327, 600) / (1296, 624) |

  - Over 4,147 room rays of close2's upper panes, the night reflection-off frame equals the picture x 0.276 at the median, the card's 0.28.
  - My camera model puts the near upper pane's corners within 2 to 18 px of the mask.
- **Stand-off and size:**
  - Every object is inside its budget (PIC-05; placed.json read).
  - Every piece is at scale 1.0: sofa 0.80 m, bench 0.89, side table 0.55 with the television on it, cabinet 1.18 with the clock and lamp on it.
  - Nothing floats or is buried. The upper rooms hold no bed, table or chair, as the budgets require.
- **No marks:**
  - television_02's blanked bezel (270-300, 450-548) and back panel are plain at 200 per cent;
  - wall_clock's dial shows numerals only;
  - mantel_clock_01's dial has only diamond marks;
  - side_table_01's gold band is brass hardware islands, not script;
  - the other twelve models' maps carry no lettering. The three artworks are replaced by prints.
- **Content:** no drink, gambling, child, toy or person. vintage_cabinet_01's glazed shelves are empty; the bookshelves are empty.
- **Export:**
  - both normal maps in every glb are real RGB (means 0.50, 0.50, 0.98 to 0.99);
  - every textured primitive has TEXCOORD_0;
  - faces sharing a plane occur only between variant cards never switched on together (the manifest: no site with two nets, two blinds or C1 with C2) and between abutting joinery contact faces;
  - no see-through slot in the close frames (FRM-01; my mask reads).

## Which rows to trust

- **Trusted** (read from the exported files or confirmed by me): KIT-01 to KIT-18, MAT-01 to MAT-03, PIC-01 to PIC-12 (PIC-04 and PIC-06 by my `trace` check), SITE-01 to SITE-04, CONTENT-01, NIGHT-04 to NIGHT-06.
- **Not trusted until fault 1 is fixed** (measured through the mirror pane): WB-01 to WB-06, WB-09, NIGHT-01 to NIGHT-03, GLS-04, and MAT-04 (it tests a plane, not the kit's slab). NIGHT-03 also misses fault 2.
- **Stand-ins only:**
  - the sky dome and its reflection (WB-02's margin, WB-03's colour);
  - the eaves (narrow 2);
  - the street lamps and the night exposure (NIGHT-01, NIGHT-02);
  - the brick, stone sill and head (the wall kit's).

## What I could not judge from the files

- **Hidden from both close views:** the curtain pole, brackets, finials, gathered head and hem (behind the head). The net's lace band and hem (behind the stone sill).
- **Not in the close views:** the S11, RC and RC2 pieces, and the cottages' windows (no GS_B close view rendered).
- **Not looked at in full:** the three prints at full size (seen only in the room pictures).
- **Owed on the PC:** the game's pane (opaque Default Lit, Lumen's reflections, the street cube) and the night exposure. The rooms at the target's 128 samples.
- **Not rendered:** the 14 views (NOTES.md).
- **Not settled:** whether WB-02 holds after the fix at 40 samples (narrow 4).
