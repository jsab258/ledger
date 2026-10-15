# House windows target: fixes applied (cloud week 42, unit 8, 13 October 2026)

By the fixer, from TARGET-REVIEW.md (FAIL: 3 faults, 12 narrow points). Not re-reviewed. Nothing built, nothing committed. All paths are in this folder unless a line says otherwise. target.json status: "fixes applied, not re-reviewed".

**Self-check after the fixes** (self_check.py, run with the options named):
- offline: 402 pass, 0 fail, negative controls 27 of 27 caught (the first version: 342 pass, 14 of 14).
- `--live --previews`: 424 pass, 0 fail, 27 of 27 (the first version: 364 pass).
- `--live --previews --photos DIR` (adds the re-measure of the photographs): 424 pass, 0 fail, 27 of 27. This line is the one stored in target.json and printed in TARGET.md.
- Controls added (13): a brown frame on a timber house (SITE-04); WB-04b removed; the lit order with a landing first; paragon out of the blocklist; the television's maker's name in a string; television_02's marks back to the plate only; WB-04's limit back to 0.55; the cottage back rule back to 0.40 and 0.80; P1_a's row back to the stone-and-brick numbers; RC2's mullion 10 mm off centre; ArmChair_01 back in gf_front_2; NIGHT-01 back to an absolute 100; WB-08 without WB-04b.

## Faults

1. **Fault 1, coloured frames.** make_target.py SITE_PLAN: east_parade_bay1 white_fresh, east_parade_bay5 white_grimy, west_south_bay0 white_grimy, west_south_bay2 white_fresh, east_chandler_bay0 white_upvc; the other five unchanged; all ten houses white. hw_checks.py: SITE-04 now "white (white_fresh, white_grimy, white_flaking, white_upvc) 10 of 10 until Jafar's page rules otherwise"; OWED-05 carries the review's frame line with the photographs' mix; D13 added (the ruling stands over the tally until he answers) and D1's bronze question moved onto it. hw_data.py PAINTS: cream, olive, blue, brown and bronze marked "NOT USED ON ANY HOUSE" and kept as data. self_check.py: SITE-04 row, D13, D1 and OWED rows, and a control.
2. **Fault 2, white-board bands.** hw_measure.py: P1_a (435,396,451,447) with pane (437,399,449,444), P1_b (405,402,418,452) with (406,405,417,449), P1_e boxed the same way (435,489,451,540) with (437,492,449,537); L is now the 90th percentile of the outline minus the pane boxes for every window; P1_a's top-rows-out box and P8's four panes kept as extra records. Recorded rows: P1_a 0.93 / 0.65 / 76, P1_b 0.94 / 0.65 / 64, P1_e 0.90 / 0.52 / 109, P1_a top rows out 0.93 / 0.71 / 68; P1_c 0.30 (keeps its band). hw_checks.py: WB-01 P/L 0.55 to 0.97 with no median cap; WB-04 D/L at most 0.72; new WB-04b (dip at least 1 px wide to at most 0.60 of L); window states bare, net, draped (C2 by its net) and the frame class note in the gate and in WB-01 to WB-06; WB-08 includes WB-04b. The numbers quoted in the checks are built from the rows, and a self-check row compares them.
3. **Fault 3, television_02.** make_target.py MARKS: the review's sentence (rating plate and 'PARAGON Viewing System' on the front bezel, both painted out to the bezel's grey), status blank; `paragon` in the inventory's brand_blocklist (and in hw_data.py's longer list); hw_checks.py PIC-07 carries the new sentence; self_check.py rows and two controls. I looked again at every placed model's 1k base colour (see the list at the end).

## Narrow points

1. **Cottage budgets.** hw_common.py `budgets_for`: the eye is placed at the window (xc = card_cx - win_off_x), the mirror is taken about the window, and one pixel is the exact angle atan(tan(vfov/2)/720) (this reproduces the review's UP figures 0.617 / 1.20 exactly and its GF side, ceiling and floor figures to within 0.001 m). hw_rooms.py BUDGET back 0.38 true, 0.71 tolerated (this recomputation gives 0.387 and 0.723). In gf_front_2 ArmChair_01 is replaced by painted_wooden_bench (0.50). make_target.py: the GF visible_zone rows recomputed with the eye at the window. self_check.py: live recompute row rewritten (it passed on a hack before) plus rule rows.
2. **drawer_cabinet.** hw_rooms.py: up_bedroom_2 uses wooden_bookshelf_worn (0.58, tolerated); the marks entries of drawer_cabinet and ArmChair_01 corrected. Both new ids answer live at api.polyhaven.com/files/<id> and /info/<id>, are by Ulan Cabanilla and Kirill Sannikov, CC0 (Poly Haven's licence page), and I looked at their 1k maps at 100 per cent: no lettering. The three bedrooms still differ (checked).
3. **visible_zone x frame.** make_target.py: `rooms.visible_zone.x_frame` = "from the picture-left wall" and the `what` text; make_doc.py 3.3 says so.
4. **box_shade.** hw_data.py BOX_SHADE: keep_paint applies to white_fresh only; street-facing faces take 1.0; the depth law only for the faces that run into the wall (reveal-facing sides of linings, beads, pulley stiles and sash stiles). KIT-09 and the TARGET.md table follow.
5. **NIGHT-01.** hw_checks.py: the second form (pane median at least 4 times the dark windows' with r > g > b; no absolute 100). hw_data.py: absolute linear emissions for every curtain colour and blind (`night_lit_emission_linear`) and for the landing bulb (`LANDING_BULB`: card emission floor and the disc), each set to read a pane median of 0.19 linear (sRGB 121) square on; they are starting values, the second form is the acceptance. NIGHT-03 now asks r > g > b of a lit curtain (the brown one's g/r is 0.39, outside the net band), see the flags.
6. **Lit order.** hw_data.py LIT_ORDER (a fixed list, checked complete): the cottage front room west_south_bay1_gf_w1, the three lounges, a bedroom, the other cottage front rooms, the other bedrooms, the landings; counts by hour unchanged; at 20:30 no landing is lit. self_check.py: four lit-order rows and a control. See the flags: the review's fifth window is a landing.
7. **RC2.** hw_data.py RC2, make_target.py kinds["RC2"] and RC2_HOUSES (east_parade_bay4, both windows): transom at 0.66 x 1676.4 = 1106.4 (face 70), one fixed top light, a 70 mm mullion at x 0 from 60 to 1071.4, a side-hung left casement (stiles and rails 45, 4 mm gap, hinge on the left jamb), a fixed right light. hw_checks.py: KIT-12, KIT-14, KIT-15 and the others name RC2; per-kind nodes and files; D11 records both forms. self_check.py: coverage, centring, equal lights (330 each), transom, casement, pane count 3. target_drawing.py draws it (E-RC2, S-RC2); target_drawing.json rewritten.
8. **Arch segment.** hw_checks.py D14: brick kept by the 4 October decision (terrace-front.py ARCH_FANLIGHT False, line 1509), P8 shows a painted segmental head, a change reaches Jafar's page.
9. **Cottage sill.** hw_checks.py OWED-05 `lines`: the review's cottage-sill line, word for word.
10. **Reflections.** hw_checks.py OWED-06 with 1a's check, word for word.
11. **H_ALONG_15_ROAD.** hw_common.py CAMERAS and make_doc.py: "in the road, 1 m out from the kerb (2.6 m from the wall: the footway is 5.125 - 3.505 = 1.62 m wide)". The camera stays where it was (the other fix, moving it to 1.62 m, would change every figure that rests on it).
12. **Counts.** make_doc.py 7.4 and hw_checks.py could_not_settle now count the textures from the inventory (9, not 17); the self-check line carries its options (self_check.py main); the used-model count is 16.

## Other changes this made necessary

- The measured-windows sheet (production/previews/cloud-week/refs/house-windows/measured-windows-sheet.jpg) is redrawn with the new boxes. The other previews are untouched.
- make_target.py backdrop text (the hill's 48 windows): "white", not 70 / 20 / 10 per cent white, cream, olive, for the same ruling (see the flags).
- A writer's self-check row that could never fail (`... or True`, the lit table's shares) now tests the count at each hour.
- DECISIONS.md (5 entries) and RECIPE.md (1 entry) written; TARGET.md regenerated by make_doc.py; target.json regenerated by make_target.py and the self_check result written into it.

## Not done, and why

- Nothing in the review was left undone. Two things cannot be settled without a render: the absolute emissions (point 5) and WB-04b's 0.60 (no photograph here resolves a 6 mm line; it rests on 1a's profile, as the review says).

## Flags: where the review is wrong or leaves a gap

- **Narrow point 6 names the wrong window.** It lists east_chandler_bay0_upper_w1 as the fifth in the order, ahead of "the bedrooms, then the landings". That window is a landing (up_landing_2 in SITE_PLAN, and the review's own fault text calls it one), so the literal order lights a landing at 20:30, which is the fault. I put the chandler's bedroom window east_chandler_bay0_upper_w0 there. If the review meant another window, change LIT_ORDER in hw_data.py.
- **P1_e's box is not given in the review** ("the same way"). I took the stone head's end at y 484 plus 5 rows and the stone sill's start at y 540, as P1_a's box does; D/L comes to 0.52 (its upper sash is clear and dark, so D reads the room). The review's "photographs 0.62 to 0.71" for WB-04 covers P1_a and P1_b only; with P1_e the range is 0.52 to 0.71. The limit 0.72 is unchanged.
- **P8's blue over red** is 48 with the median of the four panes (the review reads 46, a mean). Both are inside WB-03.
- **Narrow point 1's side remark** (an eye 0.8 m in front of a ground window cannot see the right wall) does not hold: with the eye at the window, H_UNDER still sees the right wall (y 0.99 to 3.05), because the window is 0.8 m from that wall and the rays fan 21 degrees each side from 1.07 m. The recomputed rows stand.
- **A cottage has one room card for its two windows**, so west_south_bay1_gf_w1 cannot be lit while its neighbour gf_w0 (the same room, the same card) is dark. This is in the first version too and the review did not raise it. Not changed. Either light a cottage's two windows together or give each window its own card.
- **Only one street window is bare** (east_parade_bay3_upper_w1) under the review's own window states, so WB-02 and WB-03 have a sample of one. Listed in could_not_settle.
- **Backdrop paint.** The hill's 48 windows had a coloured mix (20 per cent cream, 10 olive) in their text. The review did not mention it; it is the same ruling, so it now says white. Change it back if he wants the mix.
- **NIGHT-03** asked every lit net or curtain for g/r 0.55 to 0.80; a brown curtain lit by tungsten is 0.39 and a green one has g above r, so the band is now for nets and the curtains and blinds are asked for their own colour (r > g > b). No green drawn curtain is lit at 20:30.

## Other lettering found on the placed models' base colours (looked at again at 100 per cent, 13 October)

Looked at: wooden_bookshelf_worn, painted_wooden_bench, ornate_mirror_01, hanging_picture_frame_01, _02 and _03 (the frame maps; the artwork maps are replaced), vintage_cabinet_01 (maps a and b), mantel_clock_01, Shelf_01, wall_clock, painted_wooden_cabinet, vintage_oil_lamp (body, glass, flame), Sofa_01, side_table_01, television_02, potted_plant_01 (pot and leaves), and the two replaced pieces drawer_cabinet and ArmChair_01.

- television_02: "PARAGON Viewing System" on the front bezel (x about 272 to 300, y 450 to 560, vertical), as the review says. The back panel's two plates read blank. Nothing else on the map.
- wall_clock: "URBAN quartz" on the dial, already in the marks entry (painted out).
- drawer_cabinet: three rows of faint lettering-like marks on the navy strip (x 255 to 725, y 0 to 110), as the review says; the piece is no longer used.
- Nothing else I can read at 100 per cent. Not letters: the side table's brass fittings along the top edge of its map, the cream strip with a hexagon pattern at the top of vintage_cabinet_01's map a, the oil lamp's rose pattern, the mantel clock's tick marks (no numerals), the plant pot (none).
