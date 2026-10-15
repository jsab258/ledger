FAIL

# Front doors for every house kind (unit 9, part 2): fresh review, STREET view, try 1

13 October 2026. One view only: the street camera (3.5 m out, 2 m along, eye 1.6 m). Judged: the 16 street pictures in `production/previews/cloud-week/front-doors-all/` at full size (the ten kinds in their first house, F1's two other houses, four hill doors), the models in `production/assets/cloud-week/front-doors-all/`, `houses.json`, and `checks/check_doors_v1.json`. Set against the target's photographs (D1 to D4, D9, D10 in `refs/front-doors-all/`), the Hook sheet, the 3.1 street reviews, and two dated photographs found for this review (end of file). The close view is another reviewer's; its review was not read. Nothing else was edited.

**Result: 1 fault, 14 narrow points.** The fault is the target's numbers, not the build. Everything else would pass at street distance.

## Fault

**1. T3's moulded panels are almost flat, so from the street T3 reads as a plain flush door with faint pencil lines. In D4 the two outlined panels are what you see first.** (The target's numbers.)
- Where: `T3-street-v1`, the upper and lower panels (x 680 to 850, y 330 to 810).
- Measured on the pixels, through the lower panel (rows 740 to 760, x 665 to 885), the render's outlines change brightness by 2 to 5 levels in 180, about 1 to 3 per cent. D4's right door, down its middle (`d4-...-three-doors.jpg`, columns 925 to 940), dips 50 to 80 levels at every outline, with a dark face next to a lit face: 14 to 40 per cent. D4 was taken in the same flat overcast light, from across the street, at 21.7 mm a pixel. Its lines are bold, so this is a profile problem, not the render's light.
- Cause, re-measured from `door_T3.glb` (leaf_frame vertices): each step is 3 mm deep over a 14 mm smoothstep (outer cove u 119.9 to 133.9, inner u 182.4 to 196.4), and the field lies 6 mm below the face. The steepest slope is 0.30, about 17 degrees, too gentle to cast any line under diffuse light. This is exactly the target's `profile_dh` (two 3 mm coves). The builder followed it.
- Exact fix (the target, then the build):
  - In T3's `mouldings.outside.profile_dh`, make each of the two steps 6 mm deep over 6 mm across instead of 3 over 14 (a quirked cove whose face is steeper than 45 degrees). The margin then lies 6 mm below the face and the field 12 mm below. Keep the outlines where they are (u 119.9 / 182.4 / 630.4 / 692.9 and the v values), and keep the leaf at 44.
  - Add a row: in the street view, every outline dips at least 10 per cent of the face's brightness, measured as above.
  - Re-render T3 street and close.

## Narrow points (worst first; none would be seen as wrong at this distance by itself)

1. **T2's nets read as four flat slate-grey panels, not as nets behind glass.**
   - Where: `T2-street`, the four lights, x 690 to 860, y 300 to 890. Median (69, 77, 88), about half the jamb's white (144). In D3 the nets are pale (196, 215, 195), close to the stile white (246), with vertical folds.
   - Whose: the builder's. `net_light1..4` is a flat card with a plain material `net_white`. The windows target's N1, which the T2 target names, is a flat card whose look comes from the weave and fold alpha (`net_voile`, NET_COMMON).
   - Fix: give the four cards the windows kit's net material (`net_voile`, N1 white) so the PC builds the same folded translucent net as the house windows. In the review render, light the card so it reads at least 75 per cent of the jamb's white, as D3's does.
2. **Five kinds can't be locked from the street, and the round-rose levers look like indoor door furniture.**
   - T2 and F3 have a bar pull only. T3, F4 and F5 have a lever on a round rose only. None of the five has a keyhole or a cylinder.
   - Where: `F4-street` x 660 to 710, y 585. `F5-street` x 655 to 705, y 650. `T3-street` x 855 to 880, y 630. At 4 m it shows mainly as a bright chrome L on a rose.
   - Whose: the target's. The photographs at 10 to 25 mm a pixel can't show a keyhole, and an unreached detail is not evidence that it is absent. The Sutton on Hull photograph of 1990 (below) shows a street-door lever on a long backplate.
   - Fix: give HD2b and HD2c a backplate 40 x 170 mm with a keyhole 57 mm below the lever's centre (sashlock furniture). Put KH1 70 mm below the bar pull's centre on T2 and F3.
3. **The house numerals are drawn in a 7-segment, digital-clock style, and at 4 m they are the most legible thing on their doors.**
   - Where: T1 "34" (x 760 to 775, y 475 to 535), F2 "246" (x 740 to 795, y 335 to 357), F3 "15", T2 "21". The open-topped 4 and square 3, 2 and 6 read as a display face on Victorian doors.
   - Whose: the builder's (the stroke font in `doors_lib`).
   - Fix: keep strokes, so still no real typeface, but give the digits round bowls: 3 with two round bowls, 4 closed with a diagonal, 2 with a curved neck, 5 and 6 with a round bowl. Strokes 6 mm on the 56 mm digits.
4. **The placeholder numbers break British street numbering.**
   - The west side carries both 34 and 21 two doors apart, and 15 as well, so odd and even are mixed on one side. 246 is impossible on a 48 m street.
   - The four numbers are fictional and allowed by the brief, so this is only a placeholder matter.
   - Fix, until the town's digits come: odd on one side and even on the other, rising from the quay, two digits at most. For example west 3 (T1), 7 (T2), 13 (F3), and east 4 (F2).
5. **T2's small dark two-part fitting on the hinge stile was never built.**
   - The target's T2 `small_fixings` (T2_hinge_fixing, u 753, v 1390, 20 x 60, 8 proud, sRGB 40, 40, 42) is in no part of `door_T2.glb` and no furniture file. No check row covers it, and NOTES.md doesn't mention it.
   - It can't be seen at 4 m, dark on maroon, but it is a target part left out quietly.
   - Whose: the builder's.
   - Fix: add it to `door_T2.glb` as two `steel_dark` boxes 20 x 25 x 8 mm, 10 mm apart, centred at u 753, v 1390. Add a PL/FU row and a wrong copy without it.
6. **F6's reeded transom reads as plain black glass, no different from a clear transom.**
   - Where: `F6-street` x 655 to 890, y 195 to 278. Median (21, 21, 19), with no streaks.
   - The flutes (pitch 6, 1.2 deep) come to 1.6 px at this distance, and they carry the same material `glass` as the clear panes. Reeded glass reads by obscuring what is behind it, which is a property of the material.
   - Whose: the builder's.
   - Fix: give `glass_fanlight` and `glass_fanlight_flutes` their own material, `glass_reeded`, so the PC gives them an obscure, rough-transmission glass. Keep the file free of textures (the shop windows' lesson).
7. **Two neighbours read as the same dark colour, and two F1 doors are twins.**
   - F7 (deep_teal, west_north_bay2) and F3 (dark_green, west_north_bay1) are neighbours. Rendered, they measure ΔE 8.4 (CIELAB). Every other neighbouring pair measures 15 to 60.
   - Separately, east_parade_bay0 and west_north_bay0 are the same kind, paint and four fittings (F1, maroon, LP1, HD1, LK2, KH1). Only the roughness differs, and the pictures can't tell them apart (`F1-street` against `F1-street-west_north_bay0`). They are not neighbours, so no rule is broken.
   - Whose: the target's street table.
   - Fix: west_north_bay1 F3 to brown, and west_north_bay0 F1 to dark_green. Checked: the neighbours become teal/brown (ΔE about 17) and brown/dark green (about 15). The facing classes still differ: brown, dark_neutral, faces turquoise, bright; dark green, dark_chroma, faces black, dark_neutral. Brown is used once elsewhere (east_parade_bay3, not a facing door). Maroon falls from three doors to two, and the twin is gone.
8. **The eroded notch on F4 and F7 is a crisp machined rectangle.**
   - Where: `F4-street` x 850 to 880, y 958 to 970. It reads as a pale fitted strip, not rot. F7's is mostly behind the reveal.
   - Whose: the builder's. The 130 x 25 x 3 box with its liner is within the target's numbers.
   - Fix: cut it with an irregular cutter. The top edge wanders ±5 mm, the ends taper to nothing over 25 to 40 mm, the depth goes from 3 mm in the middle to 0.5 at the ends, and the corners are rounded to r 4.
9. **The boot scraper's scrolls curl inward over the blade, and its feet float.**
   - Where: `T1-street` x 485 to 615, y 1050 to 1130. D10's scrolls sit outboard and curl outward. The builder flagged this.
   - Whose: the target's point list `standard_profile_xz`.
   - Fix: change one sign in `scraper()` so each scroll sits outside its standard.
   - Also, `BS1.glb`'s feet run from y 0.4 to 12.4, floating 0.4 mm above the ground, and the standards stop at 0 rather than 0.4 into it. Whose: the builder's. Fix: feet from -0.4 to 11.6 and standards from -0.4.
10. **The target was wrong (builder's 1): T3 border 65.** Right reading. Re-measured from the mesh, the flat margin is 62.5 at the sides (182.4 less 119.9). Invisible at 4 m. Fix (target): border 62.5 at the sides, or drop `border` as a member and let the outlines rule. PL-T3-members then passes.
11. **The target was wrong (builder's 2): the moulding ring's 4.8 mm lap.** Right call. The passed 3.1 bolection laps 4.8 outside the opening, and that lap is invisible here. Fix (target): `target_drawing.py` grows the ring 4.8 outward, so the literal row and the required row agree.
12. **The target was wrong (builder's 3): T3's second cove.** Right call. The profile list's d 76 to 90 contradicts the inner outline at d 62.5. Fix (target): the second cove at d 62.5 to 76.5, or to 68.5 once fault 1's 6 mm steps are applied.
13. **The target was wrong (builder's 4): F7's thickness.** The build is right that 22 + 25 can't make 38. The better fix is the leaf, not the ledges: 16 mm ledges are thin against Hasluck's. Fix (target): F7 leaf 47 (boards 22, ledges 25, braces 25). That fits the F frame, which already hangs F1's 50.8 leaf. Invisible from the street.
14. **The target was wrong (builder's 6): reeded glass 4.0 in all.** Right reading (2.8 base + 1.2 flutes). Fix (target): redraw `reeded_section` with a 2.8 base. Invisible.

(The builder's 5, the scraper's curl, is point 9. The builder's 7 and 8, the frame sets and the levers' anchor point, are right and need nothing.)

## What is right

- **Each kind reads as its door at 4 m, from the British terraces of the 1980s and 1990.**
  - T1 and F1 are the passed 3.1 doors.
  - F2's six panels have P2's horizontal brass plate on the frieze rail, now clear of both mouldings.
  - F3's two long panels have their heads raked up toward the muntin, as D1's left door.
  - F4's three long lights have the wider lock stile, as D2.
  - F5's tall slit has its small plate under it, as D2 and D4.
  - F6 is a plain flush turquoise leaf with a centre plate, lever, small lock and spyhole.
  - F7's six boards show V joints and three rows of nail heads, one per board at each ledge.
  - T2 has four equal lights with thin bars, stiles wider on the lock side (D3's 84/58), a low plate in the bottom rail and the bar pull on the left stile.
  - T3 has the small flat-topped light under its arched inner outline.
- **T2's leaded fanlight is right.** A plain upper pane over a band of crossed came with uprights under the points, the came reading pale against the dark hall as in D3.
- **The frames, the bell push and the step belong in the street.** White and grimed-white frames with plain transom lights, as on the Hook sheet and both 1990 photographs below. The bell push is one plain dark oblong on the right jamb. The 3.1 step is kept.
- **No two neighbours of the street order match** in kind or paint, in `houses.json` or the pictures, and each neighbouring pair differs in at least two of plate, handle, latch and number. Pairs facing each other within 4.6 m are in different paint classes. The hill's rows have no two consecutive doors alike.
- **Nothing is mis-turned or mirrored except the scraper's scroll** (point 9). Levers point to the door's middle (F6 and T3 are mirrored as they should be), and the numerals read the right way round.
- **Legible words and numbers at 100 per cent:** T1 "34", T2 "21", F2 "246", F3 "15". These are the target's four fictional placeholders and acceptable (but see points 3 and 4). There is nothing else in any street picture: no maker's name, firm, mark, plate text or "LETTERS". There is no drink, betting, person or child, and nothing after 1992. There is no UPVC or composite door where the target doesn't ask for one; T3 is D4's 1990 moulded door.
- **The paints match the dark classics of the Hook sheet,** with one white door and one turquoise. The turquoise is the target's owed line 1 for Jafar.
- **Rows I re-measured from the files, all agreeing with the check:**
  - DIM:T2 leaf 812.8 x 1948 x 50.8, z0 10.
  - PL-T2-light1 to 4: u 94 to 743.8; light1 v 205 to 598.6 (glass less its 6 mm slot, and the bead).
  - PL-F4-members: 184 / 114.3 / 90.4 / 200 / bars 36.
  - DIM:F6: stops 49 and 846.2, leaf x0 28.6 lapping 20.4 a side, transom underside 1970.6.
  - FU-F6-latch-LK3: u 798.1, v 836.4, 18 across.
  - DIM:F7 leaf_t 38 (boards 22, ledges 16); CV-F7-joints tongues 5.8 to 6.0; WR notch 130.6 x 24.9 x 2.9 on the hinge side.
  - BP-form: one part, 22 x 72.6 x 3 proud, corners r 1, groove 14 x 2 x 1, 8 mm below the middle.
  - FU-T1-number: 32.6 x 166.2.
  - PL-T3-members: the margin is 62.5, so it fails as the builder says.
  - T3 field 6 below the face.
- **Export faults from Rita's shop: none in any of the 41 glb files** (12 doors, 29 fittings).
  - No textures or images at all, so no height map can be exported as a normal map.
  - TEXCOORD_0 on every primitive. Every primitive is triangles.
  - No two parts share a visible face plane. My own check: coplanar within 0.1 mm, same facing, more than 1 mm² of overlap, with a wrong copy caught. Each door alone, and each house with its fittings placed at `mount_m` (levers mirrored), gives none. The only finding is the back faces of the flush plates' flap and liner (LP4, LP5, LP7), 0.1 mm apart and facing into the leaf, so never seen.
  - No see-through slot. I cast 1.87 million rays per house at angles out to ±70 degrees across and ±45 up and down, through the clear opening with the fittings in place. Only the known 10 mm foot gap lets a ray through, which the PC's water bar covers.
  - No two-part bell push anywhere. BL1 is one part, BL2 is one part, and the 3.1 `door_T1.glb` holds only `iron_bellpush`.

## Cannot judge from these files

- The game's light, glass and dark hall: every transom, T2's nets and F6's reeds depend on them.
- The wear layer: kept, tired and neglected differ here only by roughness and the notch.
- The street frames of the gate (hook_day, reverse_day, street_night, row_east, row_west), which are not rendered. So I can't judge how the twelve doors sit together in the Hook camera, at night, or against the wet street.
- The doors in motion.
- The wall kit's reveals and plinth: the review wall is context.
- The turquoise under the game's grade.

## Photographs used beyond the target's

- Church Street, Sutton on Hull: geograph.org.uk/photo/3452070, Bernard Sharp, CC BY-SA 2.0, taken 15 July 1990. Dark doors in white frames under dark transom lights, and a lever on a long backplate.
- Gisburn Street, Barnoldswick: geograph.org.uk/photo/705827, Dr Neil Clifton, CC BY-SA 2.0, taken 21 July 1990. A terrace street at street distance, pale replacement doors among dark ones.
- Also College Street (Butcher's Row), Sutton on Hull: geograph.org.uk/photo/3452018, Bernard Sharp, CC BY-SA 2.0, taken 12 August 1984.

The pages were opened and their dates read there. The downloads stay in the scratchpad, outside git.
