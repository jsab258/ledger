FAIL

# House windows (unit 8), the STREET view: fresh review, try 1 (cloud week 42, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the kit. I judged the street view only: the Hook view, cam_A and the reverse view, by day and at night, and the gate's street-distance frames (H_ACROSS_0 from the far kerb, the cottages' along-30 view). I did not read the close review. Jafar's ruling of 9 October applies: a piece failing only on narrow points passes, with the points listed.

**Read:** CLAUDE.md; RULINGS.md (3 Oct white frames and the proof view's bars, 1 and 2 Oct, 8 Oct photographs win, 1 Oct night); TARGET.md sections 1 to 10; FIXES-APPLIED.md; NOTES.md; `checks/check_windows_v1.json` (all 60 rows and the measurements); `hw_manifest.json`; `hw_gate.py` (the pane, the card bake, the card strengths); three shop street reviews for their lessons; `unreal-look.json` (night sky, room glow).

**Looked at:** the six street previews; the gate frames at 2560 x 1440, whole and in crops at 2x to 5x (Hook, reverse, cam_A day and night, H_ACROSS_0 day and night, the cottages' along-30 day and night, and the reflection-off night frames); the Hook sheet; the 13 rooms' day and night_lit pictures as a sheet and the television, the dresser and the framed prints at 100 to 400 per cent.

**Measured** (luma Rec.709 on sRGB, 0 to 255; P the pane median, L the joinery's 90th percentile, as the gate does; boxes in the 2560 gate frame unless marked "1600", the preview):
- every window in the six street frames from the frame and its mask, with the reflection-off night frames beside;
- two test renders of my own (Hook and cam_A by day, the glass's reflection off, 1280 x 720, 16 samples, niced, the builder's own scene code, my own folder) and a small Blender test of the gate's pane on a closed glass slab and on a single plane;
- the trace rule at six card points against the baked cards;
- the four glbs' JSON: panes, normal maps, UVs, the planes of net, curtain and card.

**Verdict: one fault blocks, and a second follows from it and from the target's night numbers.** By day, at every street angle, the panes are mirrors: no net and no room shows, because the gate's glass turns into a total mirror at the back face of each 2.5 mm glass slab. The frames, the sashes, the rooms and the nets themselves are good. When the glass is fixed they show (proved by render below).

## Faults, worst first

### F1. By day every pane seen from the street is a mirror: the nets and rooms behind it vanish

- **Where:**
  - **Hook day.** The near window east_parade_bay0_upper_w0, box (1898, 147, 1996, 464) (1600: 1186, 92, 1248, 290). It has a full-height greyed net (N2) and reads as four grey mirror panes, P 106, P/L 0.52, with no net to be seen. Its neighbour bay0_w1, box (1624, 305, 1677, 543) (1600: 1015, 191, 1048, 339), has a lower-sash voile and open cream curtains, and shows neither.
  - **The Hook sheet** shows the opposite: "every upstairs window is PALE, white frames over white nets".
  - **cam_A day.** The two cottage windows west_south_bay0 read black: gf_w1 box (281, 546, 347, 726) P 11, P/L 0.07; gf_w0 box (417, 558, 465, 713) P 17, P/L 0.11 (1600: 176, 341, 217, 454 and 261, 349, 291, 446). Each has a white lower-sash voile.
  - **Cottages' along-30, day.** west_south_bay2_gf_w1, box (1143, 218, 1338, 1222), mirrors the parade's brick and windows opposite: P 34, P/L 0.18.
  - **Reverse day.** Every parade window at 9 to 15 degrees from the wall is the same.
- **Measured: the reflection takes light away, which glass cannot do.**
  - With the glass's reflection off (my renders, same scene), cam_A's cottage panes read 83 and 80 (P/L 0.56 and 0.51), and the voile, the clear upper sash and the dim room show plainly. With the reflection on they read 17 and 11.
  - The Hook's bay1_upper_w1 reads 104 with the reflection off and 55 with it on. bay2_upper_w0 reads 81 and 54.
  - Real glass at those angles reflects 10 to 17 per cent and passes the rest: a pane can never read darker than about 0.85 of what lies behind it.
- **Cause, proved.**
  - The lab's panes are closed slabs (60 triangles: a front face and a back face 2.5 mm apart).
  - The gate's pane (`hw_gate.make_glass_gate`: Mix of Transparent and Glossy by a Fresnel node at IOR 1.789) treats the back face as glass-to-air. Cycles' Fresnel node inverts the IOR on a back face, so beyond the critical angle (34 degrees from the normal, that is any view under 56 degrees from the wall) it returns 1. The back face becomes a perfect mirror and nothing passes.
  - My test (a white card of display 0.735 behind the pane):

    | angle from the wall | single plane | the slab as built | the slab with the fix below |
    |---|---|---|---|
    | 20 degrees | 0.66 | **0.002** | 0.66 |
    | 35 degrees | 0.70 | **0.003** | 0.70 |
    | 60 degrees | 0.71 | 0.66 | 0.71 |
    | 80 degrees | 0.71 | 0.68 | 0.71 |

  - MAT-04 passed because it renders "a flat pane" (one plane), not the kit's slab.
  - **At night the same back face mirrors the sky at the 0.2 weight.** At H_ACROSS_0 night the dark empty flat's clear upper sash (east_parade_bay3_upper_w0, about (1830, 566, 2040, 890)) reads 75 with the reflection and 16 without. That is brighter than the lit lounge beside it (bay2_upper_w0, about (1190, 566, 1370, 890), clear part 64). In the Hook night, the dark bay0_w0 reads 71 against 50 without the reflection. Much of NIGHT-01's and NIGHT-02's failure is this (F2).
- **What it costs the review:** every day row measured under 56 degrees from the wall was measured on a mirror. WB-01's failure is this fault, not the band or the sky. WB-02, WB-04, WB-04b, WB-05 and WB-09 passed on the mirror and are not evidence until re-run.
- **WHOSE:** the builder (the gate's pane, NOTES decision 9, chosen over the target's 5.1 stand-in). The kit's slab panes expose it.
- **EXACT FIX:**
  1. In `hw_gate.make_glass_gate`, add a Geometry node and make the mix factor Fresnel x refl x (1 - Backfacing). The slab's back face is then fully transparent, and only the front face reflects. Leave the glbs as they are.
  2. Re-render all 20 gate frames and the previews. The card bakes do not change and can be kept.
  3. Re-run the check.
  4. **New row GLS-06:** render the kit's own `glass__lower` node, exported as it is, at 15, 20, 35 and 50 degrees from the wall in front of an emission card of 0.5. The card through the pane must read at least (1 - F_front(angle)) of its own, less 0.03. The slab fails it today: 0.003 against about 0.66.
  5. MAT-04 is re-done on the kit's slab, not on a single plane.
  6. **Acceptance:**
     - cam_A day: west_south_bay0's two windows reach P/L 0.45 or more (0.51 and 0.56 with the reflection off, now 0.07 and 0.11).
     - Hook day: bay0_upper_w0's net is visible, with P/L 0.55 or more (0.59 with the reflection off).
     - WB-01 to WB-05 and WB-09 are re-measured and reported again.

### F2. At night the street does not show which windows are lit

- **Where:**
  - **Hook night.** The lit lounge east_parade_bay0_upper_w1 (1624, 305, 1677, 543) reads P 82 beside the dark landing bay0_upper_w0 (1898, 147, 1996, 464) at P 71: 1.2 times.
  - **Reverse night.** Of the cottage windows (1029 to 1229, 757 to 890; 1600: 643 to 768, 473 to 556), the three lit ones read 52, 57 and 92 and the dark ones 25 to 50. From the street I cannot pick the lit ones out.
  - **H_ACROSS_0 night (h-across0-bay2w0).** The lit RC (bay2_w0) has a warm net (122) under a clear sash that reads 64: a glowing lower half under a dark upper half.
  - NIGHT-02 reads 1.3 against at least 4. Jafar's night (1 October) is "pools of lamp light with darkness between, lit windows".
- **Three causes, measured:**
  1. **F1's back face**, as above: it mirrors the night sky into every pane under 56 degrees, about 25 to 60 levels on a dark pane.
  2. **The lit room is four times dimmer than its own net.** In the same lit window, the clear glass reads 0.26 to 0.31 of the lit net (linear):
     - h-across0 bay2_w0: net 0.195, clear 0.052;
     - Hook bay0_w1: 0.226 against 0.070;
     - close bay0_w1: 0.199 against 0.055.

     The lit card is the night_lit picture x 0.7 x 0.4 = 0.28 (the target's 9; `hw_gate.BRIGHTNESS`), while the net glows 0.48. A dark room's card is x 0.7: two and a half times the lit one's gain. The same light passes through the net and lights the room, so the room seen through clear glass cannot be a quarter of the net.
  3. **The dark band cannot hold for a window with a net.** A dark window's net is lit by the game's own night sky light (`sky_light_gain_night` 0.15, the gate's too). With the reflection off it reads 46 to 54, about 0.6 of its frame's L, while the clear glass of a dark room reads 16 to 17, which is honest. NIGHT-01's "dark: 8 to 30" counts the net and so cannot be met by any net window.
- **WHOSE:** the builder for cause 1 (F1); the target for causes 2 and 3 (sections 7.1 and 9, NIGHT-01 and NIGHT-02).
- **EXACT FIX:**
  1. F1's fix.
  2. **Target 7.1 and 9:** a lit room's card is the night_lit picture x 1.0, no longer x 0.7 x 0.4. Measured on the reflection-off frames, this puts a lit window's clear glass at 0.6 to 0.8 of its lit net (linear): Hook bay0_w1 0.61, h-across0 bay2_w0 0.79. The PC's M_LedgerInterior Brightness for a lit house room at night follows (OWED-04 measures it).
     - **New row NIGHT-07:** in every lit window, the clear glass's median (linear) is 0.5 to 1.0 of its lit net's, curtain's or blind's median, at H_ACROSS_0 night.
  3. **NIGHT-01:** DARK means the clear (net-free) glass reads 8 to 35, and a dark window's net reads at most 0.7 of its own frame's L at night. Measured with the reflection off: clear 16 to 17; nets 0.51 to 0.64.
  4. **NIGHT-02:** the lit windows' median pane luma is at least 2.5 times the dark windows' (linear at least 6), like for like. The reason is the game's own night sky light on a dark net, as measured above. From the frames with the reflection off and the lit card at 1.0 I expect about 2.6 to 2.8: lit about 105 to 115, dark median 41. The old 4 rested on a dark pane with no lit net in it.
  5. **Acceptance:**
     - At the Hook night, the lit windows' median reads at least 2.5 times the dark windows' median.
     - In the reverse view, the two lit windows of west_south_bay2 (a net, and a net with louvres) read above every dark cottage window. With the reflection off they already read 61 and 86 against at most 48.
     - The lit cottage window behind a drawn brown curtain (bay1_gf_w1) may stay dim: a lined brown curtain glows little.

## Narrow points, each with its exact fix

### N1. WB-03, the bare window from across, is a mis-set row (target)

- **What:** P/L 0.75 (band 0.35 to 0.70) and blue over red 4 (at least 10), from h-across0-bay3w1 at 69 degrees. The window is east_parade_bay3_upper_w1, box (1185, 565, 1374, 893). It reads as pale glass reflecting a grey sky over the empty room. That is what the Hook sheet's upper panes do.
- **Why the band is wrong:** it came from P8, a rear seen from below under a clear blue sky. The game's sky is overcast and neutral (the scene file's dome, the Hook sheet). This view is at 21 degrees from the normal, so F1 does not touch it: it is the band, not the build.
- **EXACT FIX (target section 9 and WB-03):**
  - P/L 0.35 to 0.90 (P3_d 0.36, P8 0.49 to 0.59, P6_up 0.89 with sky in its glass).
  - Replace "blue over red at least 10" with "blue minus red at least -3": the pane is no warmer than the neutral dome it reflects.
  - Whether a room is behind the glass is WB-06's job (it passes).

### N2. WB-07 misses by 0.005 on the flaking-paint house (target)

- **What:** east_parade_bay3_upper_w1 reads 2.995; the other five read 3.40 to 7.34.
- **Why:** its paint is white_flaking (linear 0.60 against white_fresh's 0.82, and 12 per cent flaked to primer). The band's floor of 3.0 sits at 0.8 of the lowest photograph (P1, 3.75) taken for sound white.
- **EXACT FIX (WB-07):** the floor is 3.0 for white_fresh and white_upvc, and 2.5 for white_grimy and white_flaking. 2.5 is 3.0 x 0.66/0.82 for the grimy paint, rounded up so that a dull frame still reads clearly above its brick. The ceiling stays 9.0.

### N3. The stand-in lamps burn the cottage window heads and frames to flat orange; GLS-05 excuses it (kit)

- **Where:**
  - The cottages' along-30 night (frame h-along30-gf2w1_night): the frame of west_south_bay2_gf_w1, box (1144, 372, 1336, 1221). **11.2 per cent of its joinery pixels are clipped** to flat orange (R 250 or more, B under 140): 7,123 of 63,641.
  - Reverse night: orange cones lie over the cottage window heads (1600: about 635 to 680 and 735 to 790 across, 455 to 520 down). They are hot but not clipped (R at most 185), so they pass as pools.
- **Measured:** GLS-05 found these pixels on window paint (7,367 in that frame, 30 in cam_A night, 1 in the Hook night) and "not counted" them.
- **Why it matters:** the game holds clipped pixels in the nearest pool to 2 per cent (his order of 8 October, `lantern_pool_lumens`). This is the shops' known stand-in-lamp fault on a white frame.
- **EXACT FIX:**
  - GLS-05 counts window joinery too: at most 2 per cent of any window's joinery pixels may be burnt.
  - The gate's cottage-side lamps are cut until no window's joinery is more than 2 per cent clipped (today 11.2 per cent on west_south_bay2_gf_w1). The paving calibration (150) is kept for the parade side.
  - Shared kit: write the same rule into the shop gate.

### N4. The shops' night pane may carry the same back-face mirror (kit)

- **What:** `sw_gate.py`'s night pane is the same Fresnel mix (IOR 1.5, x 0.2). If the shop glbs' panes are closed slabs, every shop pane seen under 48 degrees from the wall at night carries a 20 per cent mirror of the sky. That is the "grey sky patch" the shop checks list as a real reflection.
- **EXACT FIX:** the same (1 - Backfacing) on the shop gate's night pane, and GLS-06 run on one shop pane.

## What is right

- **Frames and joinery.** Every frame is white (the 3 October ruling): white_fresh, grimy, flaking and the satin upvc are distinct but all white.
  - The 2/2 and 1/1 sashes read as Victorian box sashes at street distance: meeting rail, glazing bar, a dark line round each pane, stone sills, no black strip at any sill.
  - The two replacement forms read as plain white 1980s casements (P6, P7, P11), period-right for 1990.
- **Nets, where the glass lets them through.**
  - From the far kerb (H_ACROSS_0, 51 to 69 degrees, untouched by F1) by day the nets read as pale veils with soft, uneven folds, not corrugation or a white card. The upper sash over a lower voile is clear, with the room behind.
  - The Hook at night shows the full-height net's soft folds.
  - The lit windows are warm (r > g > b; NIGHT-03), with the open curtains standing at the sides.
- **Night glass.** No orange bar in any pane; no hot corners in any night_dark room (PIC-03b, and I looked); no lit stand-in lamp in the glass.
- **Parallax.** I computed the trace rule myself at three card points each for the Hook's bay0_upper_w0 and the across view's bay3_upper_w1. The baked cards match the room pictures at those points within 3 levels (mip filtering). From the Hook the window shows the landing's left wall; from across it shows the ceiling at the back wall's top: both as the target's visible zones say.
- **Rooms.** All 13, day and night_lit, looked at:
  - Content rule: no bottle, can, glass of drink, betting slip, toy or child's thing. The dresser in lounge 2 and bedroom 1 is empty behind its glass. The prints are plain sea and coast.
  - Lettering: none reads, including the television at 400 per cent, its bezel blank where PARAGON was.
  - Anachronisms and scale: nothing after 1992 (a 1980s CRT, a paper-shade pendant, vertical louvres, a venetian and a roller blind). No piece reads child-size: the sofa, bench and cabinets are at scale 1.0.
- **Exports.** Every normal map is a real RGB normal map (blue 0.98 to 0.99, red and green 0.50). Every textured primitive has TEXCOORD_0. No bump is exported. The net, curtain and card planes are at 235, 254, 262 and 270 mm, in front of one another as the target orders, so no two parts share a face plane. No see-through slot: the near window's box holds only glass, joinery and brick in the mask (FRM-01 agrees). No part floats.

## Rows: which I trust and which are stand-ins

- **The five failing rows:**

  | row | what it is | why |
  |---|---|---|
  | WB-01 | a FAULT in the build | F1, proved by render |
  | WB-03 | a mis-set row | N1 |
  | WB-07 | a mis-set row | N2 |
  | NIGHT-01 | a fault in the build (F1) and a mis-set row (F2, causes 2 and 3) | the stand-in night sky is the game's own 0.15, so it is not the excuse |
  | NIGHT-02 | the same as NIGHT-01 | as NIGHT-01 |

- **Trusted:**
  - KIT-01 to KIT-18: read from the glbs, and I re-checked the panes, normal maps, UVs and card planes.
  - MAT-01 to MAT-03.
  - PIC-01 to PIC-12: the pictures, and the parallax I re-traced.
  - SITE-01 to SITE-04, NIGHT-03 to NIGHT-06, PIC-03b, FRM-01.
  - WB-08, as a render of the old fault.
- **Not evidence until re-run after F1:**
  - WB-01, WB-02, WB-04, WB-04b, WB-05, WB-09, NIGHT-01, NIGHT-02 and GLS-04: all measured through the back-face mirror.
  - WB-06 for any window it read under 56 degrees from the wall.
  - MAT-04: a single plane, not the kit's pane.
- **Stand-ins only, whatever they read:**
  - WB-03 and WB-07 (the dome and the stand-in brick);
  - GLS-05 (the stand-in lamp);
  - all absolute night levels (the gate's sky and lamps).

## What I cannot judge from the files

- **The game's pane.** The glbs' `glass_house` is OPAQUE (base 0.03, specular 2.0). The nets and the room card stand behind it as separate cards. In Unreal they will be seen only if the PC builds the pane the target's 5.1 way (lace and room folded into the pane's own material) or as see-through. The gate shows neither: OWED-01, and a risk the PC must close before the first Unreal frame.
- **The engine's light on the glass.** Lumen's reflections, the street cube and the night exposure are not in the cloud.
- **The 14 gate views not rendered:** H_ACROSS_30; the cottages from across; the along-15 and road views.
- **The rooms at the target's 128 samples.**
- **The wall kit.** The arches, the reveal's brick returns and the painted heads are boxes in the gate: the Hook sheet's arched heads are not this unit's.
- **The Hook sheet's own street.** The gate's street is stand-in boxes, so only the windows themselves were set beside the Hook sheet.
