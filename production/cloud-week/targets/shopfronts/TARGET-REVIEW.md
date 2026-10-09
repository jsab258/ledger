FAIL

# Shopfronts target: fresh review (cloud week 42, 9 October 2026)

Reviewer: a fresh target reviewer who did not write the target and will not build it. Read: REVIEW-BRIEF.md, BRIEF.md, canon.md, RULINGS.md, TARGET.md, target.json, the author tools, every preview in production/previews/cloud-week/refs/shopfronts/, the kit README, FRONTAGE-2026-10-06.md, the fascia target, the front-door target (F1), SCENE-SLOTS.md, photographs.md, terrace-fronts.md, tools/art-recipes/terrace-front.py (refits, door sides, the grocer), the Hook sheet and the three game previews.

**Eleven faults.** The worst are on every front from the street: the shop door's glass starts at the wrong height because a photograph edge was mis-measured; the plinth's head moulding that P1 plainly shows was dropped; the pilasters stand 10 to 15 mm proud of the frames beside them; the "scrolled" console is not drawn as a scroll; and the shop door's letter plate sits in its glass.

## How this was checked

- **P1 at its source.** api.polyhaven.com/info/leadenhall_market read today: Andreas Mischok, taken 2019-05-19, CC0 (Poly Haven), no NoAI mark. The 16k .hdr (405 MB) was downloaded to scratch. The writer's measure_leadenhall.py was re-run on it from a scratch copy, with outputs sent to scratch. All 44 stored rows, columns and the notice came back identical (0.00 px). The tool reproduces; the faults below are about which edges it snapped and how they were scaled.
- **Scripts re-run on a scratch mirror.** self_check.py gives 427 of 439 pass, 0 fail, 12 reported, as stated. target_drawing.py drew 45 drawings and 6 overlays. The repository's files were not touched (target.json md5 unchanged).
- **Re-measured myself** on the 16k file (in the same virtual view: yaw 90, f 2400): the door's glass foot, the window stile, the shaft's return, the plinth's head, the capital, the crown, the sill and the notice. Enlarged crops were made in scratch only. The door view carries bar lettering and was never saved.
- **The network.** No route from this cloud today to Wikimedia Commons, Geograph, Flickr, archive.org, Historic England, buildingconservation.com, HathiTrust, Gutenberg, Openverse, the Library of Congress or legislation.gov.uk. Only Poly Haven and ambientCG answered. I opened the five other British street HDRIs on Poly Haven (urban_street_01 to 04, bethnal_green_entrance): none shows a shopfront. So the writer's statement that P1 is the only reachable photograph of a British period front holds. What that leaves unsettled: the console's real form, timber plinth heights on provincial parades, 1970s aluminium sections and a provincial fascia's slope. Every fault below is found on P1 itself, in the target's own numbers, or against the other targets and the street's files.

## Faults, worst first

### 1. The shop door's glass starts at 700, from a mis-snapped edge; P1 shows the glass level with the window sill

- **Photograph:** P1, the shop door in the unmasked view, rows 0 to 220, columns 440 to 540 of the virtual image. There is no preview of the door because its glass carries lettering, so self-check group 2 could never re-measure it.
- **What is wrong:**
  - `door_glass_bottom` is stored at row 95.66 with a snap strength of **1.5**; every other edge is 5 to 30. That row is inside the dark glass. The glass foot (glass to bead to lock rail) is a clear luminance step at rows 126 to 130.
  - The writer's own snap, aimed there (expect 128, window 6, same span), finds **row 128.93, strength 12.2**.
  - Glazed from = (547.01 − 128.93) / (547.01 + 827.74) = **0.304 of the leaf**, which is 798 mm on P1's 2624 leaf. Scaled to a 2040 leaf that is **620**.
  - P1's window sill top, measured on the window's own plane, is **844**: its foot row is 559.29, giving 1.8666 mm/px; see fault 10.
  - So in P1 the door's glass starts at the sill line, within 46 mm. That is also what the earlier research reads from Coventry ("its bottom panel the stallriser's height").
  - The target's 700 matches neither. Its own rule R6 (tolerance 8 per cent) fails on the true edge: 0.343 against 0.304, 12.8 per cent off.
  - From the street, on every timber front, the door's glass line stands 100 mm above the window's sill line beside it.
- **Amendment:**
  - `parts.shop_door.dims`: `glazed_from` 600 (level with the sill top 600), `bottom_rail` [0, 230], `lower_panel` [230, 490], `lock_rail` [490, 600], `glazed_fraction_of_leaf_from` 0.294.
  - `photo.features.door_glass_bottom.y` 128.93. `derived_mm.door_glazed_from_fraction` 0.304.
  - R6: photo 0.304, target 0.294.
  - D2: "600, level with the sill, as P1 shows (0.304 of the leaf = 620 on 2040) and as Coventry says; the scene's 1.0 loses".
  - Check "glazed from": expected 600 ± 3.
  - New check, per shop with a T1 or M2 door: "shop door glass foot minus window sill top = 0 ± 5".
  - Save a door preview masked to joinery (the glass filled flat above row 120, every sticker and notice masked) so that rows 128.9, 531.6 and 547.0 become re-measurable.

### 2. The shop door's letter plate is placed in the glass

- **Where:** `parts.shop_door.dims.furniture.letter_plate` is z 800, "on the lower panel's centre". But the lower panel is 230 to 590 and the glass starts at 700. The furniture check enforces z 800, so a correct build would fail it. The drawing simply leaves the plate out (target_drawing.py draws none on the shop door), so self-check group 5 never saw the clash.
- **Amendment:**
  - With fault 1's rails: letter plate 250 × 40 centred at **z 545 in the lock rail** (490 to 600), 35 clear above and below. Without fault 1: z 645 in the 590 to 700 lock rail.
  - The furniture check becomes [1000, 545].
  - The P1 alternative's octagonal knob goes "on the lock rail at z 545", not at 780.

### 3. The plinth's head moulding: P1 shows a large hollow moulding and a band; the target draws a flat slab and drops the base mould saying "P1 shows none"

- **Photograph:** P1-leadenhall-pilaster-plinth.jpg, the top block (preview rows 35 to 130); in the virtual image, rows 53 to −46, columns −1305 to −1150.
- **What P1 shows:** between the third step and the shaft is a hollow (cavetto) moulding. It is 77.5 px (134 mm) tall and its arris runs in from column −1302.5 to −1282.5, about 37 mm. A flat band 17.5 px (30 mm) tall sits on top, and the shaft stands just behind it. Scaled by 800/1123 that is a moulding 95 high setting back about 26, and a band 21 high.
- **What the target says:**
  - `plinth_stepped_side` ends in a vertical face 680 to 770 and a 30 mm weathered top.
  - `meets` and section 5 drop the kit's base mould on every variant because "P1 shows none, the plinth's cap takes the shaft directly (Photo)". The photograph says the opposite.
  - This is exactly the moulding fault the front door failed on. It shows at eye height on all twenty pilasters.
- **Amendment** (numbers for today's d values; shift with fault 4):
  - `plinth_stepped_side`: (0, 0) (150, 0) (150, 504) (146, 504) (146, 631) (142, 631) (142, 684) (132.8, 691.2) (125.0, 711.8) (119.8, 742.6) (118, 779) (118, 800) (0, 800). This is a cavetto from d 142 at z 684 to d 118 at z 779 (a quarter-ellipse centred at (142, 779), 24 by 95), then a band at d 118 to 800, with the shaft (110) standing 8 behind it.
  - Panel and flute variants: restore the kit's base ogee (pilaster.py's), 25 proud of the shaft face by 60 high at z 800 to 860, returned on the free side.
  - Strike "P1 shows none" from `meets` and section 5.
  - The check "profile fit" also covers `plinth_stepped_side` and the base ogee (Hausdorff ≤ 1.5).

### 4. The pilasters have almost no relief: shafts 10 to 15 mm proud of the frames beside them, and a capital that hardly flares

- **Photograph:** P1, the shaft's right side at rows −1500 to −1440 (shaft_return_outer).
- **What P1 shows:**
  - The 117 mm that D3 measured is the painted return between the shaft's face and the next surface beside it.
  - A further dark return runs to about column −1029 before the teal frame. The frame's own foot row (559.3, against the pier's 604.1) puts the glazed frame about 330 mm behind the pier's face.
  - P1's capital (P1-leadenhall-pilaster-capital.jpg) flares well out: its cream band reaches column −1327.5 and its top slab −1347.5, against the shaft's −1270. After allowing for off-axis displacement that is roughly 50 to 100 mm per side.
- **What the target does:**
  - It puts the shaft at d 110 but keeps the window jambs at 95, the shop-door frames at 100 and the F1 frame face at 100. Only 10 to 15 mm of return shows beside the frames, which reads as flush from the street.
  - Its capital's "flare" rises 90 but moves out only 14 (d 114 to 128). On the shaft it reads as a band, not a cap.
- **Amendment:**
  - Shaft face d **140**; plinth front d **180**. Every pilaster plan and side profile shifts +30 in d, and the downpipe then stands 12 behind the shafts.
  - Capital: die face 144, the hollow flare from 144 to **172** over its 90, abacus front **175**, ovolo top back to 172, top face **350 × 175**. The console's toe (0 to 74) still stands wholly on it; the board's bed mould (132) stays.
  - Checks: shaft proud 140, plinth proud 180, capital top [350, 175].
  - New check: "shaft face minus the front face of every frame beside it (window jamb, door frame, F1 frame) ≥ 40".
  - D3 reworded: "P1's 117 is the shaft's return beside the next surface; the scene's 0.10 loses".

### 5. The "scrolled" console is not drawn as a scroll

- **Where:** `parts.console.profiles.side_silhouette`, and `variants.scroll` ("S-curve, volute on each side").
- **What is wrong:**
  - The 53-point outline is one sweep from the toe (d 74) out to d 180 under a flat top. It has no volute at either end.
  - The "volute" is a spiral groove cut into a flat side face at (d 34, z 82), behind the toe's outline, not the outline rolling into an eye.
  - Close up and in side view along the street, all twenty consoles will read as plain corbels with a decal spiral. That contradicts the target's own words.
  - No photograph supports either form (D11, and the network; see above).
- **Amendment** (Judgement, same 240 × 180 × 550 envelope, toe 240 × 60 on the capital unchanged):
  - Redraw `side_silhouette` so that the outline forms an **upper volute**: eye at (d 126, z 470), outer radius 54. The front reaches d 180 at z 470, rolls back over the top through (126, 524) and into the eye in 1.25 turns.
  - Under that, a concave waist, narrowest d 62 at z 130.
  - Then a **lower volute** rolling the other way: eye at (d 46, z 62), outer radius 30, reaching d 76 at z 62.
  - Keep the cap block 180 deep at z 528 to 550.
  - The side grooves follow the outline 8 mm inside it, 5 wide and 4 deep, each ending in an eye boss 16 across and 3 proud. The leaf is kept.
  - The "volute" and "silhouette" checks follow the new numbers. Add the console to `could_not_settle` as the first piece to check against a reached photograph.

### 6. No hinge side is given for any door, so a mirrored door passes every check

- **Where:** `parts.shop_door.dims.hinges` gives a count and sizes but no side. F1 is "left-hand hinges seen from outside" (front-door target) and is mapped into the bay by translation only. target_drawing.py puts every shop door's lever on the leaf's right, in all ten fronts.
- **What the approved model shows:** in Rita's front in the game today (rita-day-kit-2026-10-06.jpg), the shop door's lever is on its left, the side-door side, so it is hinged on the window side. The side door's knob is on its right, so it is hinged on the pier side.
- **Amendment:**
  - Add `shops[].shop_door_hinge_viewer` and `shops[].side_door_hinge_viewer`. The rule, from Rita's: the shop door is hinged on the window side with its lever toward the side door (the grocer: window side). F1 is hinged on the pier side, so it is used as drawn where the door end is on the viewer's left and mirrored where it is on the right. State this in `side_door_slot.mapping_from_F1`.
  - New check per shop: "lever and letter-plate side of each leaf = the table's".

### 7. The roller shutter's curtain is set at the glass plane, inside the frames

- **Where:** `alterations.roller_shutter.numbers.curtain_front_d` 30.
- **What is wrong:**
  - Lowered (the night variant), the curtain would pass through the mullions (front 92), the transom (nose 100), the head, the door frame (100), the sill (nose 150) and the stallriser (125).
  - One curtain over window and door cannot stop on the sill in one part and reach the footway in the other.
  - The rails sit "on the frames", so their front is at about 135, still behind the sill's nose.
  - The newsagent's glazing note says the hood "hides the toplights' top 100", but the hood (z 2550 to 2850) hides 240 of the toplights' 310.
- **Amendment:**
  - Curtain plane **d 170** (20 clear of the sill's nose), running to the footway across window and door.
  - Guide rails 50 × 40 at **d 150 to 190**, z 0 to 2550, on steel spacer brackets bolted through the frames into the pilaster core (bolt heads visible).
  - Hood 300 high × **210** deep (z 2550 to 2850).
  - Glazing note: "the hood hides the toplights above 2550; 70 shows".
  - New check: "curtain plane ≥ sill nose + 15 and within the hood's depth; the lowered variant intersects no frame".

### 8. The cornice's ends at every party-wall gap are not defined

- **Where:** `parts.cornice` stops 54 short of each party line, leaving a 108 gap for the downpipe. Nothing says how the end is finished; the lead upstands are "not geometry".
- **Why it matters:** along the parade there are two exposed ends at every one of nine party walls. They are seen end-on from the street, as the kit sheet shows (shopfront-kit-2026-10-06.jpg, top left).
- **Amendment:** each end is closed by a mitred return of the full 19-point section back to the wall, 215 deep. The lead apron is dressed down over the return with a 25 upstand. New check: "cornice end is a closed return; Hausdorff ≤ 1.5 to the section turned 90 degrees".

### 9. The newsagent's board is dove grey here but cream in the fascia target

- **Where:** the fascia target's newsagent `old_board.colour` is cream (222, 209, 175), shown as a 95 mm ring at the ends and 40 mm above and below the box sign. This target paints `shops[newsagent].paints.fascia_board` dove grey (150, 152, 150).
- **Why it matters:** the board's face texture is the fascia target's, so the board's edges, ends and bed mould would be a different colour from its face.
- **Amendment:** newsagent `fascia_board` paint is `cream` (222, 209, 175); the piers, consoles and cornice may stay dove grey.

### 10. Several numbers labelled "Photo" are not what P1 shows (no build value changes beyond faults 1 and 4, but the evidence table must be true)

- **Window stile 145:**
  - `stile_right` (column −952.7) snapped onto a bar of the cast grille.
  - The teal stile ends at column −992 (re-snap −993.0, strength 5.4). That is 42 px, **78 mm** at the window's plane.
  - The decision (jamb 50, "not followed") stands, but the 145 must go.
- **Sill top 883, R3 0.18:**
  - This used the pier's foot row (604.06) and a "wall plane" 117 behind the pier.
  - The window has its own foot row (bottom_rail_foot 559.29), which gives 1.8666 mm/px and a sill top of **844**.
  - R3 becomes 0.172; R1 becomes 1123/844 = 1.330 against the target's 1.333.
  - The mullion becomes 92.1 × 1.8666 = 172 (D5's decision stands).
- **Crown 446, R8 0.859, D7's "three times taller":**
  - Members above eye level and proud of the plane are drawn taller in a wall-plane re-projection, by Δ·p/(D − p).
  - At Δ ≈ 3.5 m above the eye and D ≈ 4.27 m, that adds 130 to 270 mm for a 150 to 300 projection.
  - So the true crown is somewhere 170 to 300, a ratio of 0.35 to 0.6, and not measurable by this method.
  - Mark R8 "not measurable", drop the 'tall' variant's photographic basis, and make the corona's 0.35 Judgement. D7's choice of 150 stands.
- **Capital 301, R4:**
  - The flare's and abacus's undersides lie inside the 174 px, adding roughly 30 to 60 mm.
  - Mark it "upper bound"; 310 stands as Judgement.
- **Fascia field "between the gilt keylines":** `fascia_field_top` (−1989.7) is the crown's lowest fillet. The keyline sits about 65 px lower. Rename it "the board between the crown and the capital top".
- **Amendment:**
  - Correct `photo_measurements.json` (door_glass_bottom 128.93; stile_right −993.0) and `photo.derived_mm`.
  - Scale the window rows with the window's own foot row.
  - Add to the scale note: "parts above eye level and proud of the plane are drawn taller by Δ·p/(D − p); the crown and the capital are not measurable this way".

### 11. Check STA-03's arithmetic contradicts its own variant

- **Where:** "skirting 100 + 3 courses of 152.4 + cap 42.8 + joints = 525" adds up to 600 plus joints. `variants.tile_square` is 100 + 2 × 155.4 + 79.2 + 35 = 525.
- **Amendment:** the measure text becomes "skirting 100 + two courses at 155.4 pitch + one half course at 79.2 + cap 35 = 525", expected 525 ± 2.

## Notes (narrow points; none alone would fail the target)

- **The plinth at 800, and which source wins.** The earlier research does not contradict 800. Kensington and Chelsea (read on 6 October) asks only that the stallriser not rise above the pilaster's base. P1's corrected R1 (1.330) matches the target's 1.333. But it rests on one market-hall pier, and it breaks a line in the approved model: Rita's in the game today has the plinth top level with the stallriser top. Keep 800, and name it in the summary as a visible change to his model.
- **Carrying a London arcade's proportions.** P1 is fit for what it measures near eye level:
  - plinth against sill;
  - door glass against sill;
  - shaft width;
  - the foot strip;
  - the order of members.

  The target is right to refuse P1's market-hall specifics: the crown, the heavy mullion, the stile, single piers and the absence of consoles. Where P1 and the earlier research differ (mullion, fascia slope, door glazing), the earlier research and the fascia target win, except on the door, where P1 corrected and Coventry agree (fault 1).
- **Group 4 overlay is circular.** It lays the measured instance back on the crops it was measured from; the writer says so. Add an overlay of the target's own Rita elevation (D1) on the re-projected P1 elevation, at one scale (the shaft width), and list where they differ.
- **The laundry's aluminium refit departs from the recipe.** SHOPFRONT_REFITS has no east_parade 4, while the ironmonger is listed as a refit there. Only the ironmonger is named in `could_not_settle`; add the laundry beside it. terrace-fronts.md's laundry vent pipe through the fascia band would collide with the box sign; that is a fascias or town question.
- **Kick plate and foot strip overlap.** T1 doors carry both a 170 kick plate and a 30 foot strip over its foot; P1 shows a strip only. Choose, or say the strip covers the plate's foot.
- **The drawings omit some states.** D2 does not show the empty unit's whitewash, the laundry's box sign or the tea room's panel. Reviewers of the drawing cannot see those states.
- **P1's scale notice.** It is England's statutory no-smoking sign, whose 2007 minimum size was A5, which supports the A5 assumption. This is from memory: legislation.gov.uk was unreached.

## The twelve reported departures: do they hold?

| reported line | holds? |
|---|---|
| shaft proud 110 vs the scene's 0.10 (D3) | The direction holds; the reading of P1 does not (fault 4: 117 is the return beside the next surface) |
| glazed from 700 vs the scene's 1.0 (D2) | The scene loses, rightly; the value does not hold (fault 1: 600) |
| mullions 62 in front of the glass vs the kit's 48 (D5) | Holds (Cornwall's 40 to 70) |
| grocer: no side door | Holds (BAY_WITHOUT_SIDE_DOOR = 5; terrace-fronts.md item 2): a fascias question |
| grocer: window centre 35.497 | Holds (follows from the above) |
| door rows not re-measurable on a preview | True, and it hid fault 1; add the masked door preview |
| scale: no second dimension | Holds as a statement; the notice's statutory size supports A5 (unchecked) |
| R8 crown 0.859 vs 0.273 | The departure (150 kept) holds; the photo value does not (fault 10) |
| D5 mullion 70 vs 164 | Holds (P1's mullion is a market hall's; 172 at the right plane) |
| D7 cornice stays 150 | Holds (fixed by the fascia target and the signs' brackets at 3.60) |
| D10 pairs at the party wall | Holds (the scene's fact) |
| D11 scroll by Judgement | Holds as a statement; the scroll as drawn does not (fault 5) |

## What is right

- **Sources.** They are honest and dated: P1 and P2 are CC0 and reached today, the unreached list is true, and nothing NoAI is used. No real brand, numeral or lettering appears in any preview; I checked the edges of the transom, sill, plinth and fascia crops enlarged. The door view with bar lettering was correctly kept out of the repository.
- **Method.** The re-projection, the A5 scale and the plane ratio are sound. The camera height (1044) agrees from the pier's and the door's foot rows. The plinth's steps, the shaft width (290), the door leaf (2624), the foot strip (29) and the transom bar (39) are real edges, and they reproduce exactly from the 16k file.
- **The ten fronts.** They agree with the fascia target and the trades of 3 October on bay, street x, door end and board. Their 1990 states are believable and varied:
  - original and repainted;
  - metal replacement (fish, laundry, chandler; Mickey's in painted steel on patterned tile);
  - a 1930s refit;
  - box signs and a flat panel;
  - a shutter;
  - a whitewashed empty unit with a console gone.

  Metal fronts beside older frontage, patterned tile and recessed lobbies with tiled floors are as photographs.md establishes.
- **The joins.** The party-wall pairs, the downpipe chase, the console's toe on the capital, the fascia between the consoles, the cornice's soffit on the board, the F1 mapping (x, y, z, trims) and the zones all add up, and the self-check proves them on all ten.
- **Buildable from target.json alone.** Every part has a section or plan as point lists:
  - capital;
  - cornice;
  - sill with throat and weathering;
  - T1, T2, M1 and M2 mullions;
  - toplight bar;
  - beads;
  - jambs;
  - transoms;
  - threshold;
  - leaf stile;
  - raised field;
  - stallriser panel and tile sections.

  Fixings, wear, paints (sRGB, roughness, metal) and variants are all stated.
- **What the checks catch from the street.** A console off its capital (the toe inside the capital's top, at most 1 above). A cornice not capping the fascia (soffit gap 0). Wrong zones or a mirrored bay at the zone level (per-shop u ranges and street x). The door's glazing height (once its value is corrected). What they miss is covered by the new checks in faults 1, 3, 4, 6, 7 and 8.
- **Questions honestly raised.** Mickey's door x, the grocer's fanlight number, the ironmonger, twelve against ten fronts, the Hook sheet's recessed Mickey's door, and the downpipe.
