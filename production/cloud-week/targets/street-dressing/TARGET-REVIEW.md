FAIL

# Street dressing, nine families: fresh target review (cloud week 42, unit 13, part 2)

Reviewed 13 October 2026 on branch cloud/week-42 at 05f7d43 by a fresh reviewer who did not write the targets and will not build them. Brief: production/cloud-week/targets/REVIEW-BRIEF.md; the writer's task: production/cloud-week/targets/BRIEF.md and Jafar's words of 12 October. Rulings read in full: RULINGS.md, canon.md; scene read: production/specs/vignette-scene.json, vignette-pieces.json, hook-cast.json, SCENE-SLOTS.md, the shopfronts target's shop zones, tools/art-recipes/terrace-front.py and south-quay/south_quay_geom.py.

| family | verdict | faults | narrow points |
|---|---|---|---|
| phone box | FAIL | 3 | 5 |
| bus stop | PASS | 0 | 6 |
| A-board | PASS | 0 | 4 |
| skip | FAIL | 1 | 5 |
| bench | FAIL | 1 | 3 |
| telegraph pole | FAIL | 3 | 2 |
| bicycle | FAIL | 1 | 2 |
| milk crates | FAIL | 1 | 3 |
| pallets | FAIL | 1 | 2 |

WHOSE: every fault below is the target writer's to fix in the family's make_target.py (it regenerates target.json and TARGET.md), unless the line says otherwise. Scene-file and town changes are named as owed lines, not made here.

How I checked: every self_check.py and target_drawing.py re-run in a scratch copy of the repository (all pass offline: phone box 113, bus stop 105, A-board 142, skip 76, bench 95, pole 73, bicycle 68, crates 76, pallets 75 rows; every negative control caught); 34 recorded photograph rows re-measured from my own downloads of the originals with my own edge finder and the writer's boxes (phone box 13, A-board 8 on the 2.6 degree turned copy, bus stop 7, skip 6 on the 7.2 degree turned copy): every one within 0.7 px of the record (mine sit about 0.5 px lower throughout, a half-pixel convention, well inside every tolerance); 23 Geograph pages opened (titles, taken dates and CC BY-SA 2.0 confirmed on each, listed per family); Poly Haven's file records and base colours read for four crates; the awning mesh, the quay geometry and the scene's pieces measured for every slot.

## 1. Phone box: FAIL

### Faults, worst first

**Fault 1. The move from east x 16.5 rests on a wrong clearance, and that wrong number is the one put on his page.**
- Place: phone-box/target.json placement.reasons[1], owed O1, TARGET.md "Where it stands", DECISIONS.md 13 Oct 07:00 (phone box) line.
- The target says the scene's kiosk "leaves 2.0 - 0.55 - 0.89 = 0.56 m of footway". The scene's 0.55 m set-back is to the kiosk's centre from the kerb's back edge: production/specs/vignette-pieces.json kiosk_plinth stands at z 3.675 with a 0.914 plan, so its faces are at 3.218 and 4.132, and the strip between its back and the stallriser face (4.975) is 0.843 m. The target's own 890 box at the same centre leaves 0.855 m. Both are over the 0.68 m a walker needs. There is no walking-width reason to move it.
- The other reason ("before Rita's window ... a kiosk must not stand in front of it") is an inference, not a ruling: the box stood there on 2 October when he ruled both "the KX100 phone box stays" and "Rita's window is the model".
- Exact fix: keep the scene's slot: east x 16.5, centre z 3.675 (0.55 m from the kerb's back edge to the centre), the door facing the shopfront (+z, as the scene's kiosk_door at z 4.132 does), the back sheet to the road; placement.kiosk_face_z_m [3.230, 4.120], clear_strip_mm 855 behind it, 105 mm to the kerb's back edge in front. Drop O1, or if the writer still wants the move, rewrite it with true numbers ("0.86 m now, 0.96 m there") and every consequence in faults 2 and 3. Correct the DECISIONS line's reason in the same commit.

**Fault 2. The new slot (east x 23.5) collides with the empty unit's awning and stands across its shop door.**
- Place: placement (x 23.5, faces z 4.085 to 4.975, height 2192).
- awning_02 hangs at east x 24.0 (x 22.5 to 25.5) from the fascia's underside, 2.95 m above the crown, projecting 1.735 m (vignette-scene.json held_props; vignette-pieces.json prop_awning_02_1). Measured on ledger/Assets/Props/base-mesh/awning_02.glb (Blender): its canopy falls 0.995 m over 1.577 m, then a valance to 1.318 m below its top. Over the box's front edge (1.04 m out from the wall) the canopy is about 2.29 m above the crown; the lid's top there is about 2.27 to 2.28 m (the footway's 0.07 to 0.09 m plus 2192): 15 to 25 mm apart. The fascia package makes that awning the empty unit's mark (production/art/fascia-01/01-SPEC-fascia-package.md: "Bay 3 (x=24) is the only bay with an awning and no fascia lettering").
- The valance hangs 1.63 to 1.96 m above the crown between z 3.39 and 3.55, inside the walkers' strip in front of the box: the strip clear at head height is 3.55 to 4.085 = 0.53 m, under 0.68.
- The box covers x 23.055 to 23.300 of the empty unit's shop-door slot (x 22.294 to 23.300, centre 22.797: shopfronts target, shops[empty_unit].centres_street_x_m).
- The target's neighbour list names the lamp column, the pillar box and the dustbins but not the awning or the doors; its placement rows test only the target's own numbers (stallriser line minus depth), so no row could fail on any of this.
- Exact fix: the slot of fault 1. Whatever slot is chosen, add a placement row that tests the kiosk's box (with its 2192 height) against every piece in vignette-pieces.json within 2 m, wall props included, and against the shopfronts target's door zones, and measures the clear strip at 2.0 m above the footway.

**Fault 3. The move ignores the town's kiosk place and the meetings that depend on it.**
- Place: placement; nothing in the target mentions production/specs/hook-cast.json.
- places.kiosk is at x 16.5, z 4.3, "beside kiosk_plinth (16.5, 3.67)"; schedule lines meet there (kiosk/ritas_step, kiosk/fish_counter); DECISIONS 30 Sep records that Marta steps onto Rita's step (x 18.0) so that "her friendship with Alison at the kiosk still meets". At x 23.5 the place would be 5.5 m from Rita's step, and z 4.3 lies inside the moved box (4.085 to 4.975). The hook frame, composed with the box at 16.5, is not mentioned either.
- Exact fix: the slot of fault 1 removes this. If a move is ever put to him, it carries a town handover (move places.kiosk with it, outside the box, and re-check the kiosk/ritas_step meetings) and a hook-frame picture before and after.

### Narrow points
1. S1 is misdescribed. P1's middle band is black, not a red-pink handle panel; the only coloured part is a separate pull standing beyond the left edge at band height (about x 388 to 405, y 405 to 435 on the 1024 copy). S2's door has the full-width coloured panel. Fix: S1 "shows": "the band black, a separate pink pull on the left edge (post-1991)"; say that the band's height is taken from P1 and the panel's form from S2. No number changes.
2. The slot's words contradict its numbers ("back 0.05 m clear ... set back 1.14 m" against kiosk_face_z_m [4.085, 4.975] and 0.96 m). Fix: one set of numbers, from fault 1.
3. The p1 preview's upper pane still shows the operator logo's blue and red shapes as blobs through the blur. Fix: fill that region flat with its median colour, as the header was.
4. No builder check for the place. Fix: add "C9: the kiosk stands at x 16.5 +-0.05, centre z 3.675 +-0.05, door to +z".
5. N8: P1 gives 163 mm (48 px) but 172 is kept without a named source, and 172 sets the photograph's scale. Fix: use 163 (Photo, +-35) or name the source of 172.

### What is right
- The geometry is well measured: all 13 P1 rows reproduce (within 0.6 px); the lid with its 100 mm skirt, the 270 mm header, the band at 906 to 1051, the 172 mm open foot and the 40 mm posts follow the photographs over the 29 September script, each disagreement written down (W1 to W6).
- No operator's mark, crown or card; the plain word Telephone is put to him (O2); the 1985 to 1991 yellow handle colour rests on three written sources; clear glass with a smoked variant; the payphone and coin housing are marked Judgement.
- Sources reached and free: I opened S1 (5269043, "Former KX100 Telephone Box in Monks Risborough", taken 4 Jan 2017), S2 (5558709, Paythorne, 19 Jul 2017) and S3 (5314484, Chesham Road, 17 Feb 2017): all CC BY-SA 2.0. S1 and S3 carry removal notices (the interior is Judgement, as the target says).

## 2. Bus stop: PASS (narrow points to fix before building)

No fault. Placement, rules and the photograph rows hold; six narrow points, each with its fix. Point 1 would be a fault if left: it is a photograph-against-standard disagreement settled on a misread measurement.

### Narrow points
1. **The pole's width against the flag contradicts P1, and the target misreports it.** Place: N2 ("P1's pole is 7 to 8 px wide = 50 mm ... too coarse to read, so the standard is kept"). On the 640 px copy the writer measured, the white pole is 13 to 14 px wide (edges x 543.5 and 556.5 at rows 200 to 225; 543.5 and 557.5 at rows 395 to 410); on the 800 px original it is 16 to 17 px. Against the flag's 45.6 px that is 0.30 (+-0.03); the target builds 76 / 300 = 0.25. The plate's 300 is itself assumed, so the photograph fixes only the ratio: with a 76 mm pole the plate would be about 255 mm, outside N3's +-30. Fix: N2 = 89 mm (3 1/2 inch tube; 13.5 px x 6.56 = 89), kind Photo, +-10; add features pole_l (x 543.5, box [536, 200, 550, 225]) and pole_r (x 556.5, box [550, 200, 564, 225]); restate N3 as Judgement 300 with a source error of +-50, and say that N4 to N7 and N10 scale with it (give each a source error 17 percent wide, keeping the builder's tolerances as they are in a separate field).
2. **The pole's paint bands contradict P1.** At the target's own scale (flag top row 70.6 = 3000 mm, 6.56 mm per px), the white length above the case starts at row 175 (about 2310 mm), not 2118, and directly under the case a black band runs from row 376 to row 392 (about 1000 to 890 mm) before the lower white (to row 443.5, 554 mm). Fix: pole_upper black 2310 to 3000; pole_white 554 to 2310; a new part pole_ring, paint_black, 890 to 1008; add features white_top (row 175, box [540, 165, 560, 185]) and ring_bottom (row 392, box [540, 384, 560, 400]).
3. **The case's middle bar is missing.** P1 shows a thin dark bar across the window at row 284.5 (about 1597 mm), 2 to 3 px (about 15 mm) high, with a small dark fixing at each end; the card's top edge sits just below it (row 299, about 1502 mm). Fix: case_mid_bar, case_green, 220 x 15 x 4 at z 1590 to 1605 in the rebate behind the clear sheet, with two 8 mm round heads at x -105 and 105.
4. **The flag's back face is not written** (the borders exist only on -y). Fix: state it; Judgement: double-sided, the same border and BUS over STOP on +y, as a stop flag is read from both directions.
5. **The operator's name is a placeholder that must not reach his page.** The bus company is on the town's naming list (DECISIONS 3 Oct); RULINGS 3 Oct: placeholders never on his page. Fix: keep "WEIGHHOUSE MOTOR SERVICES" as a separate texture layer, blank in any picture for his page, and add a handover line for the town to mint the operator.
6. **Wording.** "beyond the west block's end (x 39)": west_north runs to x 42 (vignette-scene.json blocks); the stop is 4 m past it. "Rita's ... lie below it": Rita's is on the east side. No number changes.

Type-5 note: "detail/the card has no logo" tests that a sentence is present in the text, so it cannot fail on a logo; the builder's C4 is the real check.

### What is right
- The slot is the cast's stop (hook-cast.json bus_stop x 46.0, z -4.3); on the footway join between x 44 and 48 (terrace-front.py footway_*_join), clear of the lamp column at x 38 and with the hooded bin B3 2.0 m away; no shelter on a 2.0 m footway, which is plausible and recorded.
- The flag faces the northbound bus on the left-hand side of the road; the old-style enamel flag and green case follow S1 over the 29 September script (W1 to W4); the timetable's stops are all on atlas-01; no real operator, route or logo.
- All 7 P1 rows reproduce (within 0.6 px). Sources opened: S1 (5668101, "Old-style bus stop sign in Fulbrook", 16 Jan 2018), S2 (1981245, Amwell Terrace notice, 25 Jul 2010), S3 (4340832, Highland Place, Aberdare, 5 Feb 2015): CC BY-SA 2.0. A larger original of S1 (800 x 737) exists on its page and would sharpen every row.

## 3. A-board: PASS (narrow points)

No fault. The board, its slot and its face meet the rules; four narrow points.

### Narrow points
1. **An assumed size with a 2.5 percent band.** N1 (600 +-15) is assumed and sets P1's scale; I looked at the whole of S1: the board stands on asphalt beside a grating, with no object of known size. N2, N4, N5, N8, N10 and N11 inherit it. Fix: N1 Judgement 600 with a source error of +-100 (a pavement board 500 to 700 wide); mark the six as "Photo, scaled on the assumed width" with source errors 17 percent wide, keeping the builder's tolerances in their own field.
2. **The fish market's door is misplaced in the reasons.** placement.fish_door_x_m 9.4 comes from the cast's note; the shopfronts target puts the fish market's shop door at x 10.294 to 11.300 (centre 10.797) and its side door at 9.35 to 10.294. The board (x 14.23 to 14.67) is 2.9 m from the shop door, not 5 m; the conclusion holds. Fix: 10.797 and 2.9 m.
3. **A second screw eye is missing.** S1 shows a screw eye in the left edge too, level with the right one (about x 65, y 262 on the 480 x 640 copy). Fix: f_eye_l and r_eye_l mirrored to x -312 to -296 at z 588 to 598; the chain stays on the right only, as S1 shows.
4. **Wording.** "its back leaf's feet 0.063 m clear of the stallriser line": with the faces along the pavement (yaw 90) it is the leaves' side edges that face the stallriser. No number changes.

### What is right
- The slot: east x 14.45 against the fish market's stallriser (window x 11.30 to 14.65), 1.16 m clear on the kerb side, 0.157 m from the party pilaster, clear of the awning (x 10.5 to 13.5) and of the kiosk at 16.5; the scene's placeholder line did leave 0.64 and 0.54 m (checked).
- Construction from S1 (ply leaf, flared foot arch, hinged top, chain, bare edge strip) with the period stated honestly; the fish list is fish and prices only, cod sourced (ONS 1990), the rest marked invented; no shop name, no drink, no betting; out only in the market's hours.
- All 8 P1 rows reproduce on the turned copy (within 0.7 px). Sources opened: S1 (3671864, "A sandwich board sign outside the...", 14 Sep 2013; its board names a real contractor, blurred in the preview), S2 (6913397, Beach Bus, 4 Aug 1978: the preview shows only the wheel, the bus side and the blurred card, no people), S3 (2783627, Bath, 27 Jan 2012), S4 (2808162, The Shambles, York, 13 Apr 1984): all CC BY-SA 2.0.

## 4. Skip: FAIL

### Faults, worst first

**Fault 1. The skip in the road carries none of the end markings the law required in 1990.**
- Place: parts (SK1), wear, "For the builder"; the target names lamps and a permit for a skip on the highway but not markings.
- The Builders' Skips (Markings) Regulations 1984 (SI 1984/1933, made under s.139(4) of the Highways Act 1980; read on legislation.gov.uk, 13 Oct): from 1 January 1986 each end of every builder's skip any part of which stands on a highway other than a footway or verge must carry a marking of two plates of equal size and shape, to BS AU 152:1970 (the rear marking plate standard), red fluorescent and yellow reflex-reflecting stripes as Schedule 1's diagram shows; each plate as near an outer edge of the end as the skip allows, the inner edges equidistant from the skip's long axis, the upper edges level with the skip's top edge and not more than 1.5 m above the ground, never on a lid. This skip stands in the west carriageway with its south end facing the hook camera (x -3, about 24 m away, some 20 degrees left of its axis, well inside the frame): four striped plates are among the first things a 1990 British skip in the road shows, and research first was owed (CLAUDE.md).
- Exact fix: read Schedule 1's diagram (the original PDF of SI 1984/1933) for the plate size and stripe angle; add parts mark_s1, mark_s2, mark_n1, mark_n2 on the two upper end plates as Schedule 2 places them; material marking_red_yellow (red fluorescent stripes on yellow reflex, the stripe pattern a texture with its numbers from the diagram); a check row that both ends carry two plates with upper edges at the rim and at most 1500 mm high; a wear line (scuffed, one plate cracked).

### Narrow points
1. **"TEL 555 0142" reads American.** 555 is the American screen convention. Fix: a British number with an STD code in the range British drama used before 1995, e.g. "TEL. 0632 960142", or a short local number with the town's code once the town mints one.
2. **The cone move is based on a misreading and would collide.** The scene's cones stand on the west footway, 0.35 m behind the kerb face (vignette-pieces.json prop_traffic_cone_01_0 and _02_0 at z -3.35), not inside the skip's length; the skip (z -2.70 to -1.00) does not touch them. Moved to x 20.7 and 24.3 at that depth they would stand inside the bollards there (prop_decorative_bollard_02_0 and _1, z -3.40 to -3.60). Fix: drop the move; if cones are wanted at the skip's road ends, give them z -1.85 (in the carriageway, on the skip's centre line) at x 20.7 and 24.3, and note they are off the drawn street since 3 October (terrace-front.py HELD_PROPS_OFF_STREET).
3. **Error bands narrower than the assumed scale.** N1 (1200 +-100, 8 percent) sets the scale, yet N2 3016 is +-150 (5 percent) and N3 1848 +-120. Fix: source errors of at least +-250 and +-155, builder tolerances kept separate.
4. **The road's fall.** The skip's 1690 width sits across a 1 in 40 crossfall (42 mm). Fix: say the floor lies on the road's camber and tilts with it (1.4 degrees, the kerb side low), so the builder neither sinks one side nor floats the other.
5. **The accent budget.** About 3.6 square metres of saturated yellow in the hook frame (art-direction R-B4: the frame's share above saturation 0.6 is to stay non-zero and under 0.078, with the pillar box). Fix: state the skip's share in the hook frame from a quick render, or name the orange or faded blue-green variant for the sample if the share is large.

### What is right
- The 2 October ruling (skip off until real) is met: the target makes it real, keeps it off until the gate and asks him (one owed line). The hexagonal profile, rim, rib and lugs come from S1 over the scene's box (W1 to W3); the firm and number are invented and the photograph's firm painted out in both previews; lamps lit at night in the lantern colour; contents never a person or a drink.
- The slot before the yard mouth leaves 1.0 m of its own lane and the whole other lane; the skip on the double yellow lines under a permit is a fair Judgement; skips in British streets in 1990 are plain fact (the 1984 Regulations themselves show it).
- All 6 P1 rows reproduce on the turned copy (within 0.7 px). Sources opened: S1 (6875634, "Skip, Dunstanburgh Castle", 15 Jun 2021), S2 (1144136, University Street, Belfast, 26 Jan 2009), S3 (1116404, "Crossroads and Skip", 11 Jan 2009): CC BY-SA 2.0. "Tideway Skip Hire" returned no real firm in a web search.

## 5. Bench: FAIL

### Faults, worst first

**Fault 1. The slot is in the road, not on the quay apron.**
- Place: placement (x -9.0, z 2.5), reasons[1] ("the quay apron south of x 0 is open ground"), not_settled ("south_quay_geom.py was not read in this unit").
- I built tools/art-recipes/south-quay/south_quay_geom.py (build(), plain Python): Quay Street runs on south of x 0 as its own 6 m carriageway to the junction at x -30 (arm N from x -2.0 to -21.2, then the junction); the apron's setts begin at about x -33.1 and run to the cope at x -70. The point (-9.0, 2.5) lies on road_quay_street_south (asphalt, 0.5 m inside the east kerb face); the bench's far end (z 3.4) is on footway_northeast_corner. The bench would stand in the east lane, 47 m in front of the reverse view.
- The placement row "it stands south" (x < 0) cannot tell the apron from the road, so it passed.
- Exact fix: centre x -40.0, z 0.0, facing -x (the basin): I checked that the footprint (600 x 1800) lies only on apron_setts (level 0.05 m above the crown) with nothing standing within 1 m, 30 m from the cope, clear of the fish boxes, rings and bollards at the quay edge. Replace the "stands south" row with one that builds south_quay_geom and tests that the footprint plus 1 m lies on apron_setts. Correct reasons[1] and [3] and the DECISIONS line ("the apron's exact extents were not read").

### Narrow points
1. "the reverse view sees its back": at x -40 the bench is 78 m from cam_reverse and small; say so (or drop the claim). The view the bench serves is the player's walk to the quay.
2. Noticed, not this unit's: the town's own "quay" place (hook-cast.json places.quay, x -5.0, z 0.0, "the quay apron") is also on the road arm. A town line, worth a handover.
3. The left leg does not fit the photograph. In p1-poole-bench-target-on-photo.jpg the drawn left leg (about x 50 to 70 of 420) falls about 35 px inside the photograph's left leg, which flares out at the slat end (the left end is seen obliquely); only the right end supports "146 mm in from the slat end". Fix: say the inset rests on the right end alone and make it Judgement +-60, or draw the leg's flare outward at the foot as the plain preview shows it.

### What is right
- Keeping the bench off the 2.0 m footway (the scene file's own reasoning, and the 2.4 m arithmetic) is right; timber slab legs from S1 over the asset plan's cast ends (photographs win, W1 to W3); slats, gaps and bolt heads all numbered; no plaque; the 1990 council bench is a stated Judgement and plausible.
- Sources opened: S1 (2693537, "Poole: a bench with a harbour view", 6 Nov 2011), S2 (2672444, Chiswick House park bench, 28 Oct 2011, rightly set aside as heritage ornament), S3 (2029816, Saundersfoot harbour wall, 20 Aug 2010): CC BY-SA 2.0.

## 6. Telegraph pole: FAIL

### Faults, worst first

**Fault 1. It puts back what the 3 October composition took off the street, without recording the conflict or asking him.**
- Place: summary line, "What already exists" (says the pole stands at x 12 in terrace-front.py), placement; no owed line.
- DECISIONS 2026-10-03 (the proof view, step 2.1, composition, under his order of 3 October): "the telegraph pole and its drop wires taken off the street ... the pole was the strongest vertical in the left third, with wires across the sky the sheet does not have" (also the comment above CLUTTER_ADDED in tools/art-recipes/terrace-front.py). The Hook sheet governs composition (RULINGS 21 Sep). The pole is not at x 12 today; it has been off since 3 October.
- At west x 33.0 the pole is 36 m from cam_hook (x -3, z -1.6, yaw 20.4), about 24 degrees left of the axis: in the left third again, 8 m tall (about 12.5 degrees of a 46 degree frame), with two wires crossing the street at 6.1 to 7.7 m against the sky; and 5 m in front of cam_reverse, on its right.
- Exact fix: record the conflict in TARGET.md and DECISIONS; the pole stays off the street until he rules; add an owed line with the hook and reverse pictures with and without it: "Put a telegraph pole with two wires across the street back at the far end, though it came off on 3 October because the Hook sheet has none? (recommended: No, unless the hook picture shows it does not cross the sky)".

**Fault 2. The slot stands inside the west shops' litter bin.**
- Place: placement (west x 33.0, z -3.725, foot 230 across).
- vignette-pieces.json prop_swing_bin_1 is at west x 33.0, z -3.65, 0.33 x 0.32 (held_props DRESSING, 24 September: "the west shops' own bin"; the drawn street puts its litter-bin model there, terrace-front.py CLUTTER_FOR_HELD). The pole's foot (x 32.885 to 33.115, z -3.610 to -3.840) is inside it. The placement rows test the lamp columns only.
- Exact fix: x 32.4 (the foot 0.32 m clear of the bin's south side, 5.6 m from the column at x 38 west, in front of the ironmonger's window at x 30.35 to 33.70 and 1.2 m short of its door), the anchors moved with it (east parade at x 29.4 and 34.9); add a row testing the foot against every piece in vignette-pieces.json within 1 m.

**Fault 3. The two west wires land in the air above a one-storey roof.**
- Place: parts facade_west (a stand-in slab 8.5 m high), anchor_w3 and anchor_w4 at 6.45 to 6.65 m, wires w3 and w4.
- Since 3 October the drawn west_north is one storey under a 35 degree pitch (vignette-scene.json west_north.drawn: storey 3.4 m, so eaves about 3.5 m above the crown at the frontage, ridge about 6.3 m four metres back). Anchors at 6.5 m on the frontage line hang about 3 m above the eaves; the 3 October note gives the same reason for the old pole ("drop wires ran to first-floor fronts the cottages ... no longer have").
- Exact fix: set facade_west to the drawn row (0 to 3.5 m and the roof plane), land w3 and w4 on the eaves course at about 3.3 m above the pavement (anchors under the gutter) and recompute their sag and length, or drop them and keep the two across wires; add a row that every anchor lies on a modelled wall below its eaves.

### Narrow points
1. "in the span of the grocer's bay (east x 27 to 39)": bay 4 (x 27 to 33) is the launderette and bay 5 (x 33 to 39) the grocer; the across wires land on both. Wording.
2. The 5.5 m minimum over a road is recorded as unread: keep it in not_settled until a page is reached.

### What is right
- The pole's form (cap, bracket with knobs, steps on alternate sides, taper) follows S1 and S2 over the 29 September ring and stubs (W1 to W3); wires as sagging polylines with real lengths; no owner's plate or mark; wear and a lean seed.
- Sources opened: S1 (2630310, "Telegraph pole in Wilmott Close", 21 Sep 2011), S2 (1385902, "Telegraph pole in Percy Road", 21 Jun 2009): CC BY-SA 2.0; the preview's crop shows no plate or car.

## 7. Bicycle: FAIL

### Faults, worst first

**Fault 1. Parts every street bicycle shows are missing or left to textures.**
- Place: variants BI1 and BI2 parts (35 kinds: frame tubes, fork, bars, grips, stem, saddle, seat post, wheels as hub, spokes and tyre segments, mudguards, chainring, cranks, pedals, bell); "For the builder": "the rear carrier, lamp and chain guard are not modelled (they are textures and decals); the chain is not modelled".
- Missing: brakes and their levers (none at all), the chain and the rear sprocket (the drive ends at the chainring), the chainguard, the rims (said to be "not separate"), mudguard stays, a rear reflector, and the rear carrier that S1's own row lists among what it shows. A chain and a carrier cannot be textures; a bicycle with no brakes and no chain reads wrong close up and from a few metres.
- Exact fix (numbers Judgement unless S1 or S3 shows otherwise, each to be marked): a chain as geometry (12.7 mm pitch, 8 wide, 6 thick) from the chainring to an 18-tooth sprocket 73 mm across on the rear hub; a chainguard of sheet steel over the top run (60 deep, 1 thick, from 40 mm behind the chainring's front to the sprocket); roadster brakes front and rear (8 mm rods from two 120 mm bar levers to stirrups under each rim, or side-pull callipers with a 60 mm reach if the type is changed); rims 25 wide, 10 deep, as their own ring; two 5 mm stays per mudguard to the drop-outs; a rear carrier of 10 mm tube with a 340 x 130 platform at 780 mm over the rear wheel and two stays to the drop-outs; a red reflector 60 across on the rear mudguard; each with a row in the self-check.

### Narrow points
1. **The slot's neighbours are misread.** "a bicycle there blocks no shopfront and no door (the side door is at x 25.5)": x 25.5 is on west_north. The drawn cottages are built by terrace-front.py's plain-row rule (a door at bay start + 1.5 m, windows at + 3.3 and + 5.1, mirrored by BAY_DOORS_ON, the west rows turned), which by my reading puts a door near x 13.5 and a cottage window near x 15.9 (sill 0.9 m) beside the slot; the scene file's own layout puts a door at 16.5 and a window at 14.1. Either way the wall at x 14.1 to 15.9 is not blank. Fix: read the drawn openings, state them in the slot, keep the grip's contact on brick and both tyres clear of a door's jamb.
2. **S1 is an interior.** Its page ("Rusty bicycle at Pant y Celyn Baptist...") shows a machine resting in a ruined chapel room "maybe 50 years". Fix: say so in S1's period; the roadster for 1990 stays a Judgement (an older rider's bicycle, plausible in a port town), with a 1980s utility frame named as the alternative.

### What is right
- An adult's bicycle only (frame, wheel size, no basket or stabilisers) under the content rule; no badge, transfer or lettering; the lean (12 degrees, grip and pedal on the wall) and its 1.64 m of clear footway are worked out; no pixel fit was forced on oblique pictures, which is said plainly.
- Sources opened: S1 (2932507, 6 May 2012), S2 (4155634, "Pig and Bicycle", 1 Sep 2014), S3 (4811433, "Bike in the Porch", Nuffield Place, 21 Sep 2014, an interior, rightly not used): CC BY-SA 2.0.

## 8. Milk crates: FAIL

### Faults, worst first

**Fault 1. The stack stands across the grocer's shop door.**
- Place: placement (x 38.0, "the grocer's side-door end", 50 mm from the stallriser line).
- The grocer (bay 5) has no side door (terrace-front.py BAY_WITHOUT_SIDE_DOOR = 5); its shop door is the outer 1006 mm at the high-x end, x 37.644 to 38.650 (centre 38.147), in a 600 mm recessed lobby (shopfronts target, shops[grocer]). The stack (x 37.796 to 38.204, z 4.627 to 4.925) stands in the lobby's mouth. The placement rows test only that the stack lies inside x 33 to 39 and the strip to the kerb.
- Exact fix: x 37.30 (x 37.096 to 37.504), against the window's stallriser (x 33.35 to 37.644), 0.14 m from the door's jamb, the strip to the kerb unchanged (1.50 m); add a row testing the stack against the shopfronts target's door zones.

### Narrow points
1. **The dairy's placeholder name is moulded into every crate and bottle.** The dairy is on the town's naming list (DECISIONS 3 Oct); RULINGS 3 Oct: placeholders never on his page. Fix: band lettering and bottle embossing as a separate swappable layer (a normal and colour decal, not mesh), blank in any picture for his page; a handover line for the town to mint the dairy.
2. **"4 m from the chandler's door at x 40":** the chandler's doors are at x 43.70 to 45.65 (shopfronts target). Wording.
3. **Colour.** S1 shows a blue crate; red is taken from the rejected Poly Haven crate. Fix: record red as Judgement (dairies used many colours) or take S1's blue.

### What is right
- The Poly Haven claim is confirmed: plastic_crate_01's base colour (1k, read 13 Oct) carries a "GALLER STORAGE" print twice; I also looked at plastic_crate_02, plastic_crate_03 and wooden_crate_01's base colours at 1k: no print. Only the measured box is used, which is the right call.
- Glass pint bottles (milk only) for 1990, the delivery stated as a Judgement and plausible; no float drawn under the cars ruling; no real dairy, cow, price or logo; the preview masks the photograph's band and blurs the bottles.
- Source opened: S1 (6898849, "Cotteswold Dairy Tewkesbury milk crate...", 14 Jul 2021): CC BY-SA 2.0; its real dairy's name is masked in the preview.

## 9. Pallets: FAIL

### Faults, worst first

**Fault 1. The pallets stand where no floor is modelled.**
- Place: placement (both pallets at z -5.7 to -6.7, behind the building line in the yard mouth, x 21.0 to 22.33).
- vignette-scene.json (west_north's note): "The 3.0 m between west_south's end at x=21.0 and this block's start at x=24.0 is the YARD ENTRANCE, and it is a gap in the data rather than a modelled object"; vignette-pieces.json has no piece under x 21.5 to 23.0, z -5.6 to -6.8. The target gives no floor level; its rows test the barrier line and the crates only.
- Exact fix: either (a) an owed line for the scene's owner: a yard floor of setts at the footway's back level (0.100 above the crown) from x 21.0 to 24.0, z -5.125 back to the blocks' depth, built before the pallets return; or (b) move the sample onto modelled ground. State the floor level in the slot and add a row that every pallet foot lies on a modelled surface.

### Narrow points
1. **Two checks cannot fail on what their names say.** "reuse/the scene's large pallet (2.00 x 1.10) is not this target's size" tests that a string is in the scene's note; "detail/no mark: no text, no stamp part" tests part names only, so a stamp in the texture passes. Fix: compare the scene's held dims_m with the target's bbox; scan the texture spec and the materials' notes for a stamp, owner or IPPC mark.
2. **The plain pallet is a stated departure** (1990 pallets mostly carried owners' marks): keep it, and say in the slot that the plain board is a choice for the no-real-marks rule.

### What is right
- The 2 October ruling (pallets off until real) is met: made real from a photograph, off until the gate, one owed line. A 1000 x 1200 x 144 stringer pallet, seven top boards from P1's width-over-pitch (0.545, spread 0.06), no mark; leaning on the gable is how S1 shows pallets and reads as a pallet, not a slab.
- Source opened: S1 (2660949, "Pallets and fish-boxes, Maiden Street...", 20 Oct 2011): CC BY-SA 2.0; the preview's fish boxes show arrows only, no name.

## Across the set

### What is right
- One shared library (sd_lib, sd_check, sd_doc, sd_photo, sd_family) instead of nine copies; every family's self-check rebuilds its geometry from target.json's parts, and all 245 wrong copies are caught when re-run (I read the shared ones and a sample of each family's against their rows, not every one). target_drawing.py draws every family from target.json alone.
- Each target says where it used a later photograph for construction only, marks assumed sizes as Judgement, reads RULINGS.md and canon in full, records the 2 October ruling for the skip and pallets with an owed line, and keeps every real firm, operator, dairy, maker and mark out of text, data and previews (the blocklist scan passes; I found no real name in any target, and in the 16 previews, all of which I looked at, no person, plate, house number, drink or child; the one leftover is the phone box logo's coloured blobs, narrow point 1.3).
- Every recorded photograph row I re-measured (34) reproduces within 0.7 px; every Geograph source I opened (23 pages) matches its stated title, date and CC BY-SA 2.0 licence.

### Checks that cannot fail on what matters (one note for the shared library)
- Placement rows in every family test the target's own placement numbers (stallriser line minus depth, set-back plus radius); none reads vignette-pieces.json, the wall props or the shopfronts target's door zones, apart from the bus stop's bin and the pallets' crates. Every collision in this review (awning, doors, bin, road, missing floor) passed. Fix once in sd_check: a placement row that loads vignette-pieces.json and the shopfront zones and tests each placed footprint, with its height, against them, with a negative control that puts the piece on a known neighbour.
- The photograph rows are partly true by construction: the parts were made from the same pixels at the same fitted scale, so they catch drawing slips (the controls prove it) but never the assumed scale; "fitted on height only" tests a label; the previews rows test the writer's own yes/no flags, so the phone box's logo blobs passed.

### What I could not check
- The drawn street in Unreal: I read the scene file, vignette-pieces.json, the recipes and the awning mesh, but did not open the engine; the cottage openings beside the bicycle are my reading of terrace-front.py's rule, not a built plan.
- Schedule 1's plate size in the 1984 skip Regulations (the diagram is in the PDF; the operative text was read).
- The skip's share of the accent budget (no render).
- The self-checks' --live and --previews options (I re-measured independently and looked at every preview instead); the pole, bench, bicycle, crate and pallet photograph rows (the bicycle and pole have none); the KX100 hobby pages S4 and S5 (their numbers agree with the Wikipedia page the target cites).
- Whether "Galler" is a real firm (the target treats it as one and uses nothing from it, so either way nothing changes).
