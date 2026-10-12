FAIL

# Paper, cards, boards and plates (units 4.2 to 4.4): review v2, STREET view

12 October 2026. Second and last street review of the seventh build (v7), by a fresh reviewer. I looked at the contact sheets and SB1, at every placed picture at street distance (0.8 to 1.5 px/mm) over brick and dark glass, at close-ups at 2 to 6 px/mm where needed, at placed_decals.json and at the photographs.

**Verdict: FAIL.** Most fixes worked. But the new torn-paper outline is a chain of round lobes: from the pavement it reads as a cloud, not torn paper, on every torn bill (finding 1). The bird lime on the placed DANGER sign reads as a white icicle (finding 3).

## The first review's findings, as seen now

1. Icicles: **fixed**. The outline that replaced them is new fault 1.
2. Imprint island: **fixed**. On the placed class-B bills, 66 to 84 per cent of the bottom edge is untouched.
3. P02 at SF9: **fixed** (P02_A, four tabs).
4. OPEN/CLOSED fold: **fixed** (no fold or smudge; three seeds). See narrow point 4.
5. SB1 as one template: **still present** (60.4 per cent bare glass, measured). The target's, named in NOTES. See finding 2.
6. Same bottom-edge loss: **fixed** (66 to 100 per cent of the class-B loss within 120 mm of the lower corners).
7. Board grime and foot: **fixed**. See narrow point 5.
8. Grey smudges: **fixed**.
9. V-notches: **partly fixed**. The bites are now semicircles (M01_B left edge 583 to 633 mm; M01_C top 121 to 157 mm, right 73 to 133 mm). Part of finding 1.
10. S01n_D blots: **fixed** at street distance.
11. Tabs on card faces: **still present**. The target's cue; passes.
12. Rain runs: **partly fixed**. Still invisible at 1.5 px/mm on P02_B, P03_B and G02_B; passes.
13. Empty fields on M01, B01, H01: **still present**. The target's; passes.
14. Held number 960 335 (L01's) on L03n and L04: **still present**. The target's; passes.

## What passes

- **Words.** All 435 lines, rebuilt from the glyph manifests: no wrong word, no content-rule breach, every date on its right 1990 weekday.
- **Stock, colour, process.** Still one 1990 town's paper; the boards and plates are in proportion with the photographs.
- **Fixings.** Four corner tabs on the A3s in windows (J01, D01, C01a, P02 at SF9); one top-left tab or the sucker on every hand card; nothing mirrored or turned.

## Findings, worst first

1. **Torn paper is drawn as round lobes (fault, new, made by the fix of v1 findings 1 and 9).**
   - WHAT: every loss outline is a chain of round bulges 15 to 40 mm across, with no corner and no straight run; edge bites are semicircles. At 0.8 px/mm it reads as a cloud, a jigsaw edge or a splat. Torn paper has straight runs meeting at sharp corners and teeth. The pale rim and the paste ghost are right.
   - WHERE (placed):
     - M01_C on SF2: the whole lower third, plus the bites at the top and right.
     - M01_B on the west pier: the left-edge semicircle and both lower corners.
     - P02_B and P03_B on SF2: the lower corners.
     - P05_C and P05_D on SF4.
   - WHERE (worst, not placed): T01_B lower right (a five-fingered splat), T01_C, B01_C, G02_C and F01_C.
   - WHOSE: the maker (bill_pasted loss; the 20 mm disc openings round every corner).
   - EXACT FIX:
     - (a) Make each loss the region between the sheet's edge and one **tear line**: an open polyline from a point on the edge to another point on the edge. It has 4 to 12 segments, each 12 to 70 mm long. At each vertex the line turns 15 to 75 degrees off its base heading, with the sign alternating at every vertex. One vertex in four is a tooth: a turn of 90 to 140 degrees, then back within 5 to 25 mm. Edge bites are the same walk with 2 to 4 segments, leaving and meeting the edge at 30 to 70 degrees.
     - (b) Then add a midpoint-displacement jag, 3 levels deep, with amplitude 6 per cent of the segment length. Then the 0.5 to 1.5 mm fibre fringe and the pale rim, as now.
     - (c) Remove the 20 mm disc openings. Instead, cut off at its base any paper or loss protrusion longer than 1.5 times its base width. This still forbids v1's icicles.
     - (d) Keep the shares, the lower-corner rule and the ghost as they are.
     - Test, count 0 for each:
       - After 3 mm smoothing, no 40 mm stretch of a tear line turns more than 150 degrees in one direction. Today's lobes turn 180 to 270 degrees within 40 to 60 mm.
       - No protrusion is longer than 1.5 times its base.
       - Every tear line of 60 mm or more has at least two vertices turning 60 degrees or more.

2. **The newsagent's board, and every shop card, are in one hand (fault; the target's, named in NOTES; it does not fail alone).**
   - WHAT: SB1 is unchanged (one face, one layout, no overlaps, 60.4 per cent bare glass). The same Patrick Hand also letters the grocer's stars (K07a to d), the fish tickets (K09a to f), the launderette (K06a, K06c), K05 and SA15: every shop has the same writer.
   - WHERE: SB1_B; SA01 to SA15; the K-cards named above.
   - WHOSE: the target (its §5.7 card lines and card_board table). Applied in the maker as a recorded override, like WEAR_OVERRIDE.
   - EXACT FIX, using only faces already in production/fonts:
     - (a) Five writers, each declared per card in the glyph manifest (`hand_shear_deg`, `hand_xscale`, `emb_mm`) so that the reader and the check draw the same:
       - W1: Patrick Hand as now.
       - W2: shear +12 degrees, x-scale 0.88, emb -0.25.
       - W3: shear -4, x-scale 1.12, emb -0.10.
       - W4: all capitals, felt_black, emb 0, x-scale 0.95.
       - W5: shear +6, x-scale 1.0, all sizes 1.25 times.
     - (b) Per shop: K07a to d W3; K09a to f W4; K06a and K06c W2; K05 W5; K01 and SA15 W1. On SB1, no two cards that touch or overlap share a writer.
     - (c) SB1 layouts: heading cap 6 to 11 mm; body cap 3.5 to 6 mm; line pitch 1.7 to 2.3 times the cap. Centre four cards. The text fills 50 to 85 per cent of each card's height.
     - (d) The board decal becomes 600 x 440 mm, keeping its lower-left corner at u 1.95, z 0.90. Rows of 4, 4, 4 and 3, with gaps of -15 to +8 mm. At least six overlaps of 5 to 25 mm, the newer card on top. Bare glass at most 35 per cent (test).

3. **The bird lime is a white icicle (fault, minor but seen from the quay).**
   - WHAT: a translucent white wedge hangs from the top edge, and the letters show through it.
     - On H02_C (placed, SF8) it is 33 to 37 mm wide at the top edge, at 92 to 128 mm from the left. It narrows to 5 mm by 57 mm down, then runs as a thin line to a bead at 112 mm, across the D of DANGER.
     - On S01n_D (placed, SF7) there are two smaller wedges, about 25 mm wide and 45 mm long, at about 358 and 779 mm from the left.
   - Lime lands as a splat and runs down in narrow, opaque runs, not a cone.
   - WHOSE: the maker (the close review's lime numbers, drawn as a cone).
   - EXACT FIX:
     - On the top edge, an irregular splat 8 to 20 mm across, (235,235,228) at opacity 0.9, with a core of (150,150,135) covering 20 to 40 per cent of it.
     - From the splat, 1 to 3 runs. Each run is 2 to 5 mm wide, with its width within ±30 per cent along its length (no taper from a wide top). Each is 20 to 90 mm long, within 3 degrees of vertical, at opacity 0.85 to 0.95, and ends in a 3 to 5 mm bead.
     - Test: no lime wider than 8 mm anywhere more than 10 mm below the top edge.

**Narrow points (each passes):**

4. **The plastic sign's scratches** (K03a and K03b; maker). They are evenly strewn straight white sticks and show on class A too (K03b_A). Fix:
   - Class A: none.
   - Class B: 6 to 12 scratches at opacity 0.25 to 0.4.
   - 70 per cent of them within 25 mm of the bottom edge or 20 mm of the hole, and within 25 degrees of horizontal.
5. **The letting boards' foot bites are symmetric grey mounds** (L02_C, L03n_C, L04_C; maker). Fix: give the top edge of each bite a ragged polyline, as in 1(a) at 1/4 scale, and run a 0.5 mm lifted-paint rim (the paint colour times 1.08) along it.
6. **v1 points 11 to 14** stand as above. They are the target's and pass.

## What I cannot judge from the files

- The maps under the game's light; fluorescence, the wet look and glass reflections.
- The decals at true size on the built walls; the string, sucker and sleeves in 3D.
- The art pictures of G01, T01 and T02 (not yet made).
- The automatic check: checks/check_v2.json had not landed.
