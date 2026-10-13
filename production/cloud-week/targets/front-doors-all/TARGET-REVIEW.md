FAIL

# Front doors for every house kind: fresh target review (cloud week 42, unit 9, 13 October 2026)

Reviewer: a fresh subagent. I did not write this target and will not build it. I read REVIEW-BRIEF.md, BRIEF.md, RULINGS.md (in full), canon's content rule, TARGET.md, target.json, the self-check and drawing scripts, the 3.1 folder (target, departures.py, build_door.py, the close review v2, HANDOVER row 3.1) and the street files. I opened 8 Geograph pages and the Commons file myself, downloaded the files the writer measured (same sizes as recorded), and measured them again. I re-ran `self_check.py` offline (461 pass, 0 fail, 48 of 48 controls, as recorded) and `target_drawing.py` (10 kinds drawn), and I ran some extra wrong copies against the self-check. Nothing in the repository was changed except this file.

**Result: 4 faults, 11 narrow points.** Faults 1 to 3 would be seen by a reviewer of the built doors, or would stop a script from building them. Fault 4 is the checks.

## Faults, worst first

### Fault 1. F6 and frame FF6 are built from an indoor landing door, and FF6 cannot be built or opened (whose: the target's)

- **Where.** D5 (`Hazlehead_I,_Provost_Graham_Avenue_(SC_1141987).png`); TARGET.md sections 2, 5 (F6), 10 (W1); target.json `kinds.F6.frame_change` and `frame_sets.FF6`.
- **The source is indoors.** The Commons file page, read through the API on 13 October, describes D5 as "View of hallway and door inside one of Hazlehead I blocks". The whole frame shows a carpeted landing, a plant on a side table and a large floor number "4" on the wall. The target calls it a "council flush door" and never says it is indoors. FF6 is taken from it: a 762 leaf "seen whole" in a 117.6 white lining with "stops planted on the inside face". That is how an internal door sits in a lining. It is not how a street door sits in its frame.
- **D9 is not a flush door.** In D9 (2876894, the door under the canopy, column 396) the face is pale grey-teal from row 583 to 619 (about 85,122,130, which reads as glass) and turquoise only from row 621 to 640. It reads as a half-glazed door. Using its hue is fine, but "flush doors under small concrete canopies" is wrong.
- **FF6 contradicts the target's own rule.** With the side stops behind the leaf, the door would have to open outward onto the footway. W5 and 3.1 say every door opens inward with its hinges inside. The leaf's head also still laps 20.4 behind the transom: the leaf top is at z 1991 and the transom underside at 1970.6, and the self-check requires that lap. So the head stop is in front of the leaf while the side stops are behind it, and the leaf could open neither way. It is not "shown whole" at the head either.
- **A script cannot build it from target.json.** `frame_sets.FF6` still carries F's lapped rebate [22, 53], stop_depth 74 and jamb_face 101.6, although its jambs show 117.6. The planted stop has no section or depth anywhere in the data; "22 wide" appears only in prose.
- **The checks miss it.** I ran a copy with the F6 leaf at 838 (wider than FF6's 765.2 clear) and every row of the self-check passed. The control named "F6: the leaf 838 wide in the planted-stop frame" actually sets 700.
- **Exact fix.**
  1. Recommended: F6 goes in frame set F unchanged. Leaf 838 x 1981 x 44, lapping 20.4 behind each stop and the transom; jambs show 49; visible face 797.2 x 1960.6. Place LP4, HD2a and the spyhole by D5's fractions of the visible face. Delete FF6 and W1.
  2. If the narrower leaf and wide white frame are wanted, cite an outdoor photograph for them: D4's middle door (Frederick Street, 1990) is a flush door in a white frame about 5.7 px (about 120 mm) wide. Then make FF6 a lapped frame: stops in front as F (rebate 22 x 53, stop 74), clear between stops 765.2, leaf 806.0 (765.2 + 2 x 20.4) with leaf_x0 44.6, jamb_face 117.6. Add a geometry row that fails unless leaf w = clear + 40.8 (+0, -2).
  3. Rewrite D5's source row: "an indoor landing door of a 1960s tower block (Commons description); used for the flush face and its plate, lever, lock and spyhole only, not for the frame". Rewrite D9's row: "a half-glazed council door; its lower panel's hue only".
  4. Fix the control so it really sets 838.

### Fault 2. T2 does not match D3: stiles too wide, fanlight pattern and number wrong, and D3's box takes in the dark gap and brick (whose: the target's)

- **The box.** D3 (2321423, 658 x 1024). The leaf's edges lean about 1 px every 40 rows (left edge 44.9 at row 445 to 47.4 at row 549; right edge 120.1 to 122.5). The recorded box [45.75, 443.75, 124.25, 633.75] takes its left edge from the top and its right edge from the foot. At mid-height that box is about 3 px (4%) wider than the leaf, and its right side covers columns 122 to 124: luminance 15, 54 and 110, which is the dark gap and the first brick. The gate measures the leaf's own face only.
- **The stiles.** Measured row by row on the leaf's own face (row 470: left edge 45.4, glass 53.7 to 115.3, right edge 121.1; row 549 agrees within 0.5 px), at 10.07 mm per px:
  - the white beside the glass (stile plus bead) is 84 mm on the lock (left) side and 58 mm on the hinge (right) side;
  - the glass is about 625 mm wide.
  The target gives 93.9 visible plus a 10 mm bead (103.9 of white) on both sides and 564 of glass. Its record D3_stiles (9.75 px each side) passes only because the right stile's record [114.5, 124.25] includes the gap and brick. The writer's own overlay (`d3-…-target-on-photo.jpg`) shows the drawn lights stopping about 4 px short of the glass on the right.
- **The fanlight.** D3's fanlight (x 42 to 122, rows 376 to 436) is not a diamond lattice. The upper 54% is one plain pane (rows 376 to 408). Below it is a band of crossed diagonals forming lozenges at a 14.3 px (about 145 mm) pitch (rows 408 to 427). At the foot is a strip with an upright under each lozenge point (rows 427 to 436). The target and drawing fill the whole light with 95 x 70 diamonds.
- **The number.** D3 shows small numerals centred on the leaf's top rail: the writer masked them in the preview, box [299, 323, 365, 353]. NM4 (a number painted on the fanlight, "Judgement") contradicts the photograph.
- **Exact fix.**
  - D3_leaf: record the box per row on the leaf's own edges (row 470: [45.4, 442.6, 121.1, 634.1]). D3_stiles: left_px [45.4, 53.7], right_px [115.3, 121.1] at row 470.
  - T2 stiles: stile_left 94.0 and stile_right 69.0 (visible 73.6 and 48.6, plus the 10 mm bead, gives 84 and 59 of white). All four lights u0 94.0 to u1 743.8.
  - T2 fanlight: one plain pane over the upper 144 of the 267 light. Under it, a band 83 high of crossed diagonal cames at a 145 pitch across the 772 (5 whole lozenges, half lozenges at the ends). Then a horizontal came 40 above the foot with an upright under each lozenge point. Came 6 wide (keep).
  - T2 number: small metal numerals 30 high, centred on the visible top rail at v 1898.6 (Photo D3, size ±10). NM4 becomes a reserve.
  - Live check: D3 edge tolerance 1.5 px (not 3.5), measured per row.

### Fault 3. T3 does not match D4: the light's head, the mouldings, the lower panel and the lever (whose: the target's)

- **Where.** D4 (689253, 640 x 550), the white door on the right; T3 in TARGET.md section 5 and target.json.
- **The light's head is flat, not semicircular.** The dark light runs from column 558.5 to 568 and row 362.7 to 383.3. Row 363 is already dark over 8 of its 9.5 px, and rows 361 and 362 are bright. So the head rises at most 1 px (about 22 mm), with slightly rounded top corners. The target and drawing give it a semicircular head, which would rise about 4.5 px (97 mm). The arch D4 shows belongs to the moulding round the light: its line lies on row 358 in the middle and row 359 at the sides.
- **Each panel has two outlines, not one 14 mm cove.** The centre column profile (563) dips at rows 352.5 and 358.5 above the light, at 388.5 below it, and at rows 401, 405, 416 and 419.5 round the lower panel. Rows 375 and 410 dip at columns 551 and 554 on the left and 573.5 and 576 on the right. So each panel has an outer outline and an inner outline with a margin of about 70 to 85 mm between them.
- **The lower panel is as wide as the upper one.** Both share the outer lines at columns 551 and 576. The target's lower panel (u 234.8 to 642.3, 407.5 wide) mixes the inner outline's columns with the outer outline's rows. It comes out 160 mm narrower than the upper panel (566).
- **The lever's box is off the leaf.** HD2c's record [581, 394, 583, 398] lies on the dark reveal, which reads 35 to 60 at every row. The leaf ends at column 578.5 to 579.5, and the recorded leaf box's right edge (581) includes the same 2 px of reveal. The lever is the dark mark at columns 577 to 578.5, rows 388 to 396.
- **Exact fix** (v = (434.5 − row) x 21.66; u centred on the leaf, because the door is seen a little obliquely):
  - small_light: flat head, top corners r 20, 218 x 446, u 297.4 to 515.4, v 1109 to 1555. Delete "semicircular head".
  - upper_panel: keep the outer outline, and add an inner outline u 182.4 to 630.4, from v 996 up to a segmental head (crown v 1646, springing 22 lower).
  - lower_panel: outer outline u 119.9 to 692.9 (as wide as the upper panel's), v 325 to 726; inner outline u 182.4 to 630.4, v 401 to 639.
  - The margin between the outlines: a flat raised border with the 14 mm cove at each line.
  - HD2c: v 910 (not 823). D4_T3_handle box [577, 388, 578.5, 396]. D4_T3_leaf box right edge 579.0.
  - The gate's T3 close camera then moves to about 0.92 m.

### Fault 4. Rows that cannot fail, and controls that test something other than their name (whose: the target's)

- **Constant rows.**
  - `self_check.py` line 407, the ten "from 60 degrees the lap closes the 1.6 mm margin" rows, compares constants: LAP 20.4, or a literal 22.0 for F6, against 8. They never read the frame or the leaf.
  - Line 391 ends `or k == "F6"`, so F6's visible-face row always passes.
  - Line 432, "FF6: the leaf's 1.6 mm margins", uses a literal 762.0, not the kind's leaf width.
  - Line 615, "no placed model", is a literal True.
  - In check_31, the part-word row unions `{"added"}` into what it tests.
- **Records with nothing to compare.** The six PH-* records in target.json have `expect: null`, so the builder's check has nothing to compare against.
- **Controls that test something else.**
  - "F6: the leaf 838 wide…" sets 700, and an 838 leaf passes everything (Fault 1).
  - "F4: a bar 25 mm instead of 40": F4's bar is 36, and the control makes it 21.
  - "a house given a knocker, a bell pull and a lion's head together" sets only a knocker.
- **Exact fix.**
  - Compute the angle rows from target.json: stop_edges_x against leaf_x0 and leaf_x0 + w, and the stop depth, with a 60 degree ray in plan.
  - Delete `or k == "F6"` and test F6 against its own frame.
  - Replace 762.0 with `T["kinds"]["F6"]["leaf"]["w"]`.
  - Delete the literal-True row and the `| {"added"}`.
  - Give each PH record its fractions and tolerances, or move them out of the builder's list.
  - Make the three controls do what their names say (838; "a bar 21 mm instead of 36"; add BL2 to the house).
  - Recount the totals in TARGET.md's first line.

## Narrow points (each a small detail with an exact fix)

1. **Maker's name and the lock's name.**
   - `td_furn.py` line 2 says "the 'Yale-type' lock is a rim night latch". Change it to "the lock is a rim night latch".
   - Section 9 says "rim night latch" is the only name for the lock anywhere. Yet "cylinder lock" appears in TARGET.md lines 21, 120, 381 and 413 and in target.json. Change each to "rim night latch", and in the P1 row write "a rim night latch".
   - NM-maker scans target.json only. Extend it to TARGET.md and the folder's .py prose. Leave the blocklist itself, and in the control use `BLOCKLIST[0]` rather than a second spelled-out name.
2. **Bell push.** T1's parts table says iron_bellpush is "kept", but 3.1 built it with r 6 corners and no groove (build_door.py line 664). BL1 needs corners of at most r 1 plus the 14 x 2 x 1 groove. Change the row to "changed: rebuilt square-cornered (r 1, was r 6), groove added", and add "corners r 1 (3.1 built r 6)" to for-the-builder item 1. BP-form does catch r 6, which is good.
3. **F2's numerals run behind the transom.** NM1 on F2 at v 1943, 56 high, reaches v 1971. The visible top is v 1960.6, so 10.4 mm of the digits is hidden. Set v 1922 (the visible top rail's middle).
4. **The plugged keyhole has no place in the data.** F1 and F2 keep 3.1's plugged keyhole, but furniture has no entry for it; F2's position exists only as "0.606" in prose. Add a keyhole entry: F1 u 782.8, v 1151 (3.1); F2 u 782.8, v 1188 (0.606 x 1960.6); head 15, slot 8 (D11).
5. **D2's box includes the sill.** D2_F5_leaf's foot (row 363) takes in two pale sill lines: rows 360 to 362 at (176,166,113) and rows 365 to 366, against the khaki leaf (134,125,78), which ends at row 359.5 to 360. The same box fault as Fault 2, smaller in effect. Set the box to [561, 280.5, 594.5, 360]. Then F5's slit becomes v 870 to 1789 (was 914.9 to 1806.1), LP7 v 772 (was 819.9) and HD2b on F5 v 1048 (was 1087.2). These changes are bigger than the stated ±24.
6. **D5's lock and foot.** D5 has a small dark lock under the lever (columns 766 to 771, rows 617 to 626), which F6 lacks. Add an 18 mm dark cylinder at u 743, v 845 (D5). D5's leaf runs to row 982 (the mat starts at 984), not 970. The ratio is unchanged (0.388), but the plate and lever rise by 15 mm.
7. **F3's panel heads are shaped.** In D1 the teal door's two long panels have raked or curved heads rising toward the muntin: the left panel's top line runs from (47.5, 526.7) to (56.7, 522.9). The target makes them square. Give each panel head a rise of 50 mm from its outer corner to the muntin (Photo D1, ±25).
8. **A fitting on D3's right stile.** D3 shows a small dark two-part fitting on the hinge stile (columns 116.5 to 118.5, rows 492.5 to 498.5, about 25 x 60, v about 1390). Either add it as a small dark fitting or write down what it is not.
9. **Owed line 2 names only Hull.** D2 (Railway Street, 1987) also shows a door frame and window frames painted mustard on its left house. Add "and D2" to owed line 2 and to W6.
10. **Two pale doors side by side.** The neighbour rule compares paint ids only, so west_south_bay1 (white_gloss 226,224,214) and west_south_bay0 (cream 222,212,184) are two of the street's three light doors side by side. Add "and in paint class" to AD-adjacent. Repaint west_south_bay0 maroon: its neighbours are white_gloss and deep_teal, and the doors facing it are navy and brown, so the class differs from all of them.
11. **The boot scraper is in words only.** BS1's form is written as "two end standards 200 high with scroll tops"; D10 shows scrolled standards and a blade with a notched underside. Give the standard a side profile as a point list (a bar 25 x 12, a scroll of radius 35 on top) and the blade's underside notch, all Judgement.

## The rows I measured again

Measured on the files the writer measured (same pixel sizes), first with the writer's box, then the gate's way: the leaf's own face only.

| record | writer's box (px) | the gate's way (px) | effect |
|---|---|---|---|
| D3_leaf | [45.75, 443.75, 124.25, 633.75], 78.5 wide | edges lean; row 470: 45.4 to 121.1 (75.7), top 442.6, foot 634.1 | 4% too wide (Fault 2) |
| D3_stiles | left [45.75, 55.5], right [114.5, 124.25] | left [45.4, 53.7], right [115.3, 121.1] | 84 and 58 of white, not 99 and 99 |
| D3_rows | lights 449.5 to 613.75 | agree within 1 px (bright bar 3 to 3.5 px, a dark bead line 1.5 to 2 px under each bar) | sound |
| D4_T3_leaf | [545, 345, 581, 434] | [545.3, 345.5, 578.5 to 579.5, 434.5]; columns 580 to 583 are reveal | 2 px too wide (Fault 3) |
| D4_T3_light | [559, 363, 568, 384] | [558.5, 362.7, 568, 383.3], flat head | box right, head shape wrong |
| D4_T3_handle | [581, 394, 583, 398] | off the leaf; lever at [577, 388, 578.5, 396] | v 910, not 823 |
| D2_F5_leaf | [561, 280.5, 595.5, 363] | [561, 280.5, 594.5, 360]; rows 360 to 366 are the sill | F5 too high by 40 to 50 (narrow point 5) |
| D2_F5_slit | [574, 287, 582.8, 324.5] | agrees | sound |
| D5_leaf | [450, 137, 775, 970] | [449, 137, 776.5, 982] | ratio sound (0.388); +15 on the fittings |
| D4_slit leaf_box | [345, 332, 370, 408] | [345.5, 334.5, 368.5, 407.5]; rows 332 to 333 are the transom rail, columns 369 to 373 the jamb | rows only, no number taken; slit 0.336 to 0.925 of the leaf |

## What is right

- **Pages and licences.** I opened each page myself:

  | ref | page | taken | licence |
  |---|---|---|---|
  | D1 | Carrville Terrace (7292055) | 1975-01-22 | CC BY-SA 2.0 |
  | D2 | Terraced housing in Railway Street (2238747) | 1987-08-09 | CC BY-SA 2.0 |
  | D3 | Terraced House - Ratcliffe Street, Levenshulme (2321423) | 1994-06-10 | CC BY-SA 2.0 |
  | D4 | Nos. 34, 32 and 30, Frederick Street (689253) | 1990-04-10 | CC BY-SA 2.0 |
  | D6 | Rensburg Street, Kingston upon Hull (7982731) | 1982-03-19 | CC BY-SA 2.0 |
  | D8 | Brazil Street, Kingston upon Hull (3462940) | 1986-06-08 | CC BY-SA 2.0 |
  | D9 | Newburn Council Houses (2876894) | 1989-08-01 | CC BY-SA 2.0 |
  | D10 | Old Town, Poole: in search of the boot scraper (3911943) | 2014-03-30 | CC BY-SA 2.0 |
  | D5 | Commons file (API) | 1987 | CC BY 4.0, Miles Glendinning, 4000 x 2646, 1920 px copy 1920 x 1270 |

  Every title, date and licence is as recorded. Nothing is marked NoAI.
- **The bell push.** The handover's fix is written first and plainly. BL1 is one part, with no bezel, button, ring or bright element, on T1 only. BP-form fails a bezel, a brass push and the 3.1 build's r 6 corners (I ran that copy). No kind or variant has a two-part push.
- **Reuse of 3.1.** The self-check compares T1, F1, LP1, LK1, LK2, BL1 and frame sets T and F with 3.1's target.json plus departures.py, and it passes. I checked F2's six-panel numbers against 3.1's option_six_panel: every rail and panel matches, and they sum to 1981.0. LK1 at u 745.8 is 3.1's.
- **The street.** I re-derived it from terrace-front.py `plan_street`, and the 12 doors, their x positions, openings, steps and the four modernised houses (from the windows target) match the table. Every pair of neighbours differs in kind, paint and at least 2 slots. Every facing pair within 4.6 m (8 pairs, distances as stated) differs in paint class. Every kind used exists in the table, every kind is used, and the hill's 12 doors keep their rule. quay-street.json holds only the export's materials (the old stand-in door paints), so it neither confirms nor contradicts the order. The builder will need to export again.
- **Rulings.** Frames stay white or grimed white, as ruled for windows on 3 October. The painted Hull surrounds are recorded as a disagreement and owed to Jafar as a line, not adopted. The bright doors are limited to three and owed as a line. All three owed lines carry a recommendation.
- **Content and previews.** No people, children, drink, betting, firm names, house numbers or plates appear in the previews. D4's estate-agent board and D5's floor number are outside the crops, and the masks are on the numerals and plaques. All previews are within the size limits.
- **Modern stock only where the evidence allows.** T3 is the one modern moulded door, and D4 (1990, "mostly modernised with double glazing") shows one beside replacement windows. It goes on the cottage the windows target modernised.
- **Overlays.** F5's slit, plate and lever and F4's three lights sit on D2 in the overlays. The scripts run and the drawing comes from target.json alone.

## What I could not check

- P1's and P2's source pages (only their previews, as for the writer).
- Hasluck's page images: I did not open archive.org.
- `self_check.py --live` (it fetches the files again; I fetched and measured them myself instead).
- The colour values from D6 to D8 (slides, used for hue only).
- The Hook sheet: I did not reopen it.
- Anything in Unreal or the gate's renders: nothing is built yet.
- D9's door is 6 px wide, so "half-glazed" is my best reading, not a certainty.
