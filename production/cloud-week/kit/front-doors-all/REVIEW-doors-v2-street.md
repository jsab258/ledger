PASS

# Front doors for every house kind (unit 9, part 2): fresh review, STREET view, try 2

14 October 2026. One view only: the street camera (target.json gate: 2 m left of the door, 3.5 m out, eye 1.6 m, lens 32). Judged: the 16 v2 street pictures (`*-street-*-v2-2026-10-13.jpg`: ten kinds in their first house, F1's two other houses, four hill doors) at full size; the 41 glb files and `houses.json`; `checks/check_doors_v2.json`; NOTES.md (try 2); TARGET.md section 16; against D3, D4, D5, D10, the Hook sheet and my try 1 review (`REVIEW-doors-v1-street.md`). The close view's reviews were not read. Nothing else was edited. One test render of my own was made in the scratchpad (T3's lower panel, below).

**Result: 0 faults, 4 narrow points.** Try 1's fault (T3 reads as a flush door) is fixed: T3 now reads as D4's two-panel moulded door. What is left of it (its left-hand outlines) is a narrow point with a tested fix. By Jafar's ruling of 9 October this is a PASS with the points below listed for the builder.

## Try 1, item by item

| try 1 item | now | where, and the measurement |
|---|---|---|
| Fault 1: T3's panels almost flat | **PARTLY FIXED** (now narrow point 1) | `T3-street`, lower panel, rows 740 to 770 and columns 750 to 770. Re-measured from `door_T3.glb`: each step a quarter-circle 6 deep over 6 (u 119.9 to 125.9 and 182.4 to 188.4), margin 6 below the face, field 12, flat margin 62.5. On the picture (max less min in the band, over the face's 183): top outlines 28 to 38 per cent dark (y 339, 384, 697, 726); foot outlines 16 to 21 per cent bright (y 604, 630, 803, 829); right-hand outlines 8.8 and 10.5 per cent (x 849, 831); left-hand outlines 2.1 and 1.4 per cent (x 680, 698). The first build's were 1 to 3 per cent everywhere. |
| 1: T2's nets slate grey | **FIXED**, overshoots (narrow point 2) | `T2-street` x 690 to 850, y 320 to 570: pale folded net, median 182 to 191 (was 69 to 88). |
| 2: five kinds cannot be locked | **FIXED** | Lever on a 40 x 170 backplate with a keyhole: `F4-street` x 660 to 705, y 575 to 640; `F5-street` x 655 to 700, y 638 to 692; `T3-street` x 852 to 880, y 618 to 665. KH1 under the bar pull: `T2-street` (662, 595); `F3-street` (660, 650). Measured in `HD2b.glb`: plate 40.0 x 170.0, keyhole liner centred 57.0 below the lever's axis. |
| 3: seven-segment digits | **FIXED** | T1 "17" (x 762 to 778, y 478 to 535), F2 "14", F3 "29", T2 "21": round bowls, a closed 4 with its diagonal, a curved 2. |
| 4: British numbering | **FIXED** | West odd and rising from the quay (17, 21, 29), east even (14), two digits. |
| 5: T2's hinge-stile fitting missing | **FIXED** | `T2-street` x 866 to 874, y 462 to 484, two small dark blocks as D3. Measured: `iron_hinge_fixing_1` and `_2`, each 20.0 x 25.0, 10.0 apart, centre u 753.0, v 1390.0, 8.0 proud, steel_dark. |
| 6: F6's reeded transom read as clear | **FIXED** | `F6-street` x 655 to 890, y 195 to 278: now a mid-grey obscure pane; at 3x the reeds show faintly. Both glass parts carry `glass_reeded` (roughness 0.35); base 2.8 and flutes 1.2 (4.0 in all), measured. |
| 7: neighbours alike, F1 twins | **FIXED** | Rendered CIELAB difference, F7 and F3: 18.4 (was 8.4). Twins gone (F1 maroon, navy and dark green). Table below. |
| 8: notch a machined rectangle | **FIXED** | `F4-street` x 852 to 878, y 958 to 972: an irregular pale chip at the hinge-side foot. Measured in `door_F7.glb`: `leaf_notch_bare` 127.8 wide, top edge up to 29.4 above the leaf's foot. |
| 9: scraper scrolls inward, feet float | **FIXED** | `T1-street` x 475 to 620, y 1050 to 1135: both scrolls outboard of their standards, curling outward. `BS1.glb`: feet -0.4 to 11.6, standards from -0.6, overall 403.8. |
| 10 to 14: the target's slips | **FIXED in target.json** (makers not: narrow point 3) | T3 border 62.5 (PL-T3-members passes); ring lap 4.8 stated; second cove at 62.5; F7 47 thick (measured: boards 22.0, ledges 25.4 with 0.4 sunk, face to back 47.0); reeded 2.8 + 1.2 (measured). |

## The builder's three departures from the reviews' wording

1. **The keyhole 70 below the pull's foot, not its centre: the builder is right.** HD3 is 270 long. At 70 below its centre the keyhole would sit at v 1166.6 on T2, under the bar (which spans v 1101.6 to 1371.6). Placed at v 1031.6 (T2) and 1050 (F3), it sits at an ordinary mortice-lock height and shows below the pull in both street pictures.
2. **The scraper's scrolls outboard and curling outward: the builder (and my try 1) are right.** In D10 (1024 px) the left scroll's spiral centre is at about (430, 270). The straight standard that carries the blade's end stands at x 470 to 510, so the centre is 60 to 70 px outboard. The scroll's top turns outward before it curls in. The right end is foreshortened and settles nothing. The close review's opposite reading does not match the left end.
3. **HD2a keeps its round rose, and HD2b and HD2c take the backplate: the builder is right.** D5 is F6's source. It shows the lever at the lock edge with a separate small lock under it (columns 766 to 771, rows 617 to 626 in the target's reading) and no long plate, so F6 stays lockable through LK3. T3, F4 and F5 had no lock, and now have the keyhole in the plate. This meets both reviews.

## PL-T3-street-dip: a narrow point, not a fault; the builder's reading half right

- **Right:** the camera stands 2 m left (gate `loc [-2.0, -3.5, 1.6]`). The cove's top meets the face with a vertical tangent, so a left-hand step's wall faces away. At 30 degrees a 6 mm step hides 6 x tan 30 = 3.5 mm of floor behind its lip. My own numbers on the picture agree with the row's: left 1 to 2 per cent, right 9 to 11, top and foot 16 to 38.
- **Wrong:** "D4's left-hand outlines show because its light is not flat", and "the engine's sun and shadow will show them".
  - D4 is also taken from the left of its right-hand door, in wet overcast light. Across its lower panel (rows 430 to 450) the left-hand outer outline dips 22 per cent (x 887: 145 against 185) and the inner one 5 per cent. D4's outlines are grooves between raised lines (dark and bright pairs at x 880 to 902 and 958 to 991), so each has a wall facing either side. T3's plain steps face only one way.
  - RULINGS 5 October: never sunshine in the friends' build. No sun will rescue these lines.
  - It is not a limit of the renderer. The builder's 1.4 x 1.4 groove is 0.3 px at this distance (about 4.6 mm a pixel across the leaf), which is why it gave only 3 to 6 per cent. A 5 x 3 mm groove gives 14 to 17 per cent in the same light (narrow point 1).
- **Why narrow:** the door reads at once as a two-panel moulded door with a small light under an arched outline, as D4. The top, foot and right-hand lines carry the panels, and the left-hand lines show as faint hairlines. A walking player sees the other side's lines from the right. It is a measurable shortfall against D4, and a known one the builder reported, not a misreading of the kind.

## Faults

None.

## Narrow points (worst first)

1. **T3's left-hand panel outlines barely show from the street camera (1 to 2 per cent; D4's 22 and 5).**
   - Where: `T3-street`, x 680 and 698, both panels.
   - Whose: the target's profile (`profile_dh`, plain steps), built as written.
   - Exact fix (target, then build): add a quirk at every outline. That is a square-bottomed groove 5 mm wide and 3 mm deep, cut into the higher surface with its inner edge on the outline, running all round each of the four outlines and following the upper panel's segmental head.
     - Outer outlines: in the face, u 114.9 to 119.9 and 692.9 to 697.9, and the same 5 mm above the head and below the foot.
     - Inner outlines: in the margin, 6 to 9 mm below the face, u 177.4 to 182.4 and 630.4 to 635.4, and likewise at head and foot.
     - Keep the 6 x 6 steps, the outlines and the 44 mm leaf. Keep PL-T3-street-dip at 10 per cent.
     - Correct NOTES.md's two claims above.
   - Tested: a cropped render of the lower panel in the review harness's own light (`review_render.light`, same HDRI, same camera, 48 samples, no review wall), with grooves cut by boolean over v 420 to 620.
     - As built, the left-hand outlines dip 3.0 and 2.2 per cent and the right-hand ones 12.1 (this matches the delivered picture within the wall's effect).
     - With 5 x 3 grooves: left 17.0 and 14.3, right 12.9 and 11.3.
     - With 4 x 3: left 17.9 and 14.9. With 6 x 4: left 19.5 and 14.8.
     - The review wall lowers the dips by about a fifth (the delivered right-hand 8.8 to 10.5 against 12.1 in the test), so the left-hand ones should still read about 11 to 14 per cent.
2. **T2's nets now read a little brighter than the white frame, and fold too evenly.**
   - Where: `T2-street`. The nets' median is 182 to 191. The transom bar's face (y 262 to 275) is 191 and the right jamb 147. In D3 the nets are 205 to 218 against the stile's 245 to 251, so 0.84 to 0.87 of the white. The folds repeat every 48 mm and read as a pleated blind more than a gathered net.
   - Whose: the builder's render aid (`render_doors.net_look`). Not in any file: the PC builds the real net.
   - Exact fix:
     - Scale the net card's brightness so that the four lights' median is 0.85 (0.80 to 0.90) of the transom bar's front face.
     - Space the folds at random 30 to 70 mm apart, with brightness 0.78 ± 0.11 as now.
     - Give GA-T2-nets-lit an upper bound: 0.80 to 0.90 of the transom bar's face, in place of "at least 0.75 of the jamb".
3. **The target's makers and its drawing still hold the old numbers.**
   - Whose: the target's. `td_*.py`, `make_target.py`, `make_doc.py` and `target_drawing.py` would undo section 16 if run again. The drawing is why the three `A3:*:mouldings_literal` extras still fail.
   - Exact fix: apply `target_changes_try2.py`'s corrections in those files: the ring 4.8 outside the opening, `reeded_section` on a 2.8 base, T3's profile and border 62.5, F7 47, BS1's mirrored list, LP2 chrome, the lever anchor, KH1 70 below the pull's foot, and the two recolours. Then re-run the self-check, so that regenerating reproduces `target.json`. The three literal extras should then pass.
4. **NOTES.md misdescribes F6's transom.**
   - It says the file has "no flutes" and that the pane "reads as a plain pale pane".
   - The file has `glass_fanlight_flutes` (4,506 vertices, `glass_reeded`, 1.2 proud of a 2.8 base), and the picture shows faint reeds at 3x.
   - Whose: the builder's.
   - Exact fix: that line to read "flutes 1.2 on a 2.8 base, in their own rough material glass_reeded; no texture; the PC gives it an obscure glass".

## What is right

- **Each kind reads as its door from across the street, in a British terrace of about 1990.**
  - T1 and F1 are the passed 3.1 doors.
  - F2 is six-panel with P2's chrome plate on the frieze rail.
  - F3 is two long panels with raked heads (D1).
  - F4 has three long lights with the wide lock stile (D2).
  - F5 is a flush door with a tall slit and its small plate under it (D2, D4).
  - F6 is a plain turquoise flush leaf with plate, lever, small lock and a chromed spyhole (D5 places, D9 hue).
  - F7 is six flat boards with V joints, nail heads in the door's paint and a thumb latch.
  - T2 has four lights over a low plate, a leaded fanlight (plain pane over crossed came with uprights, as D3), "21" on the top rail, the dark pull on the left stile and the two-part fitting on the right.
  - T3 is a white moulded door with a flat-topped small light under an arched outline (D4).
  - All sit beside the Hook sheet's dark doors in white frames. The one white door and the one turquoise give the street its few light notes.
- **The levers point to the door's middle** (F4 and F5 rightward, T3 and F6 leftward). The numerals read the right way round. The scraper is no longer mirrored. Nothing floats or fails to meet: fittings stand 0.4 into their faces, and KH1 is sunk (plate face 2.0 and blank 0.5 below the leaf).
- **No two neighbours match.** Kinds differ in every neighbouring pair, and each pair differs in at least two of plate, handle, latch and number (`houses.json`).
  - Rendered colour differences (CIELAB, medians of a plain patch of each leaf):
    - East: maroon/black 20.9, black/navy 19.6, navy/brown 26.9, brown/turquoise 32.3, turquoise/black 28.9.
    - West: navy/white 59.6, white/maroon 57.3, maroon/teal 29.0, teal/brown 18.4, brown/dark green 16.6.
  - Facing pairs within 4.6 m differ in paint class (the smallest rendered difference is 13.0, brown F4 against maroon T2).
  - Brown is used twice (F4 and F3), 13.5 m apart on opposite sides: no rule is touched.
  - The hill's four doors (F4 w1 deep teal, kept copy without the notch; T1 w2 black; F2 e1 dark green; F3 w0 brown) follow the target's table.
- **Legible words and numbers at 100 per cent, all 16 street pictures:** four, T1 "17", F2 "14", F3 "29", T2 "21". These are fictional placeholders of the target's four forms, and acceptable. There is no maker's name, firm, mark or plate text, no "Yale", and no other lettering. There is no drink, betting, person or child, nothing after 1992, and no UPVC or composite door beyond T3's 1990 moulded door, which the target asks for.
- **Rows I re-measured from the files, each agreeing with the check:**
  - FU-T2-hinge_fixing: u 753.0, v 1390.0, 2 x (20 x 25), gap 10, 8 proud.
  - DIM:F7:leaf_t: 47.0.
  - A4:T3:field_depth: 12.0, and the 6 over 6 cove, profile listed above.
  - PL-T3-members: 62.5.
  - FU-T1-scraper-BS1: 403.8 x 130.4 x 200.5.
  - FU-T2-keyhole-KH1: 205 below the pull's centre, 70 below its foot.
  - HD2b: plate 40 x 170, keyhole 57 below.
  - GLB:F6:reeded_glass_own_material: both parts, roughness 0.35.
  - KH1 pocket depths: plate -2.6 to -2.0, blank -2.4 to -0.5.
  - PL-T3-street-dip: my band measure agrees with the row (above).
  - GA-T2-nets-lit: my boxes give 1.24 to 1.30 of the jamb, the row 1.40, the same finding.
- **Export faults from Rita's shop: none in the 41 glb files** (12 doors with the two kept copies, 29 fittings).
  - There are no images or textures at all, so no height map can be exported as a normal map.
  - TEXCOORD_0 is on all 307 primitives, and all are triangles.
  - No shared face planes. My check: faces of different parts within 0.1 mm of each other's plane, facing the same way within 2 degrees, overlapping more than 1 mm². I ran it on every house assembled with its fittings at `mount_m` (levers mirrored), every fitting alone and both kept copies, and found none.
  - No see-through slot. I cast 1.4 million rays per house, all 12 houses, at 7 angles across (to ±70 degrees) and 5 up and down (to ±45), aimed at random points of the clear opening. Only the known 10 mm foot gap lets light through (heights 45 to 55 on F, 318 to 328 on T), which the PC's water bar covers. The keyhole pockets and the notch are blind.
  - No two-part bell push anywhere: BL1 is the one part `iron_bellpush`, BL2 is the reserve bell pull, and this unit's `door_T1.glb` holds no bell part. The 3.1 `door_T1.glb` holds only `iron_bellpush`. T2's two-part fitting is on the leaf's hinge stile, dark and plain, as D3.

## Cannot judge from these files

- The game's light, glass, nets and dark hall: T2's real net, F6's obscure glass and every transom depend on them.
- The wear layer: kept, tired and neglected differ here only by roughness and the notch. The doors are cleaner than the Hook sheet's street, as expected before the 4.5 layer.
- The gate's street frames (hook camera by day, reverse view, street at night, the two rows), which are not rendered. So I can't judge how the twelve doors sit together, wet, at night or in the Hook camera.
- The doors in motion, and T3's outlines as a player walks past from the right.
- The wall kit's reveals and plinth. The review walls are context.
