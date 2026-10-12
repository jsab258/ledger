FAIL

# Paper, cards, boards and plates (units 4.2 to 4.4): review v2, CLOSE view

12 October 2026. Second and last close review, of the ninth set (v9), by a fresh reviewer: the close crops, the full PNGs at 1:1 to 8x, the height maps under a raking hillshade, the ORM maps, the glyph manifests, and the code where a cause needed naming. `checks/check_v2.json` had not landed.

**Verdict: FAIL.** The first review's twelve findings are mostly fixed, and the hand cards now read as written by a person. Four faults remain that a person would see:

- 86 of 129 height maps are clipped flat at plus or minus 1.28 mm;
- no lettering anywhere is anti-aliased;
- the placed poll-tax stickers have round lobes, a thick even rim and a stray square;
- enamel chips are drawn over the bolt heads.

## The first close review's findings, as seen now

1. Torn bills, inner holes: **fixed**. Every loss reaches the edge, and the lost paper lies 0.1 mm below the face.
2. No rolled edge on straight sides: **fixed**. The fall-off now runs on all sides, but it is clipped (finding 1).
3. Hand letters jumping: **fixed**. The baseline residual sd is 0.12 to 0.22 mm on the SA lines and the slope is under 1.6 degrees; SB1 reads as handwriting.
4. Ballpoint like felt-tip: **fixed** (a thin, varied line). See narrow point 9.
5. Sleeve weather inside the glass: **fixed**. C01a_B has four tabs, C02_A two, neither has beads.
6. S01n_D confetti: **partly fixed**. The flakes are at the edges (97 per cent), but they read as an even nibbled fringe on every edge. Narrow point 6.
7. Bead rings: **fixed** (lens, crescent, highlight).
8. String and knot: **fixed**.
9. Star tab: **fixed**.
10. Rust and lime: **fixed** for rust. The lime is redrawn to the street review's numbers and passes; see narrow point 7.
11. Enamel chips: **partly fixed**. They are rounded and ringed, but drawn over the bolts and over each other (finding 4).
12. Cockle as noise: **fixed** (wrinkles, bubbles, ripple), but clipped (finding 1).

v1's narrow points:

- The door-card steps are not the pixel scale but binarised lettering (finding 2). Lost-paper height: fixed. The rest stand.

## What passes

- **Processes at 1:1:** letterpress, screen, litho, toner (no halftone), even Courier, felt-pen pooling.
- **Fixings:** one top-left tab per card; four corner tabs on the A3s and P02_A; two on C02_A; sleeve bands and ties.
- **Wear:** the plastic sign's scratches; the boards' rust; the bills' tear lines read as torn paper (M01_C's strip torn to a point).
- **Words and dates:** every date on its right 1990 weekday; no wrong word, mirroring or content-rule breach. ORM sensible.

## Findings, worst first

1. **Height maps clipped at plus or minus 1.28 mm (fault).**
   - WHAT: 86 of 129 height maps have pixels at 0 or 65535. These are flat plateaus whose edge is a crease under light.
   - WHERE (worst):
     - SA cards: 1 to 22 per cent of each card's area (21 on SA06_B);
     - K07a to K07d, K01, K02, K05, K06a, K06c and K08, at both ends;
     - the glass bills' curled foot (C01a_B is flat at 1.28 over its last 5 mm; also C02_A, P04, J01, D01 and P02_A);
     - lifted corners;
     - every bolt or screw head (+2.0 mm dome);
     - the enamel roll on H01 and H02, squeezed to a 1.28 mm cubic fall-off instead of the target's 6 mm radius.
   - WHOSE: maker (one scale, 25600 units/mm, for heights the target's own warp, curl, lift and bolts exceed).
   - EXACT FIX:
     - Per picture, units_per_mm = 25600 if max|h| ≤ 1.27 mm, 8192 if ≤ 3.99, else 4096. Write it to the manifest and to `height_units_per_mm` in placed_decals.json.
     - H01 and H02: the roll is h(d) = -(6 - sqrt(36 - (6 - d)²)) mm for d < 6 mm.
     - New check row: fail any height map with a pixel at 0 or 65535.

2. **No lettering is anti-aliased (fault).**
   - WHAT: ink-to-paper edges jump in one pixel.
     - K05_B has 5 pixels between luminance 48 and 160, against 124,000 ink and paper pixels.
     - 64 of 83 items have 90 per cent or more of their edges as single-pixel jumps.
     - At 2 px/mm, at the door, every curve shows 0.5 mm stair-steps. Seen on K05, K06a, K06c, K08, K03a and K04, and the 4 px/mm K09 tickets.
   - WHERE: paper-close-cards (K05, K01); K03a and K03b at 4x.
   - WHOSE: maker. `paste_block` builds a bool mask at the item's scale, and `block_coverage` re-binarises it with `smoothstep((blur - 0.5) * 1.6 + 0.5)`.
   - EXACT FIX:
     - Render each glyph patch at s times the scale (s = 4 where ppm ≤ 6, else 2: `glyph_patch_cached(..., ppm * s, ...)`). Paste at that scale and average each s × s block to a coverage of 0 to 1.
     - In `block_coverage`, blur that coverage at sigma 0.35 px. Then cov = clip(blur - (0.5 - bias) + jitter + 0.5, 0, 1): no smoothstep, no × 1.6. Rim and pool are taken from the same coverage.
     - Test per clean class-A picture: at most 50 per cent of edges (pixels two apart differing by over 0.7 of the ink-paper contrast) are a single step of over 0.6 of the contrast.
     - Re-run the check. The reader's nearest-colour rule keeps the 0.5 contour, so readings should hold.

3. **Poll-tax stickers P05_C and P05_D, placed at SF4 at 1.25 and 1.85 m (fault).**
   - WHAT, three things:
     - (a) P05_D's loss has a round bay of about 16 mm radius round "OLL" and a square notch. These are the round lobes of the second street review, back. `cut_protrusions` removes the residue of a disc opening, so every cut is a disc arc. On a 95 mm sticker the 32 mm disc shows (3 cuts on each sticker; also 1 to 5 cuts on M01, P03, B01, F01, F02 and T01).
     - (b) The pale rim is an even 1.3 mm band with square corners. `ndi.grey_dilation` uses a square of 2 × int(1.3 × ppm) + 1 px.
     - (c) P05_C has a bright 2.6 mm square with a dot at x 62 to 65 mm, y 46 to 49 mm from the top. It is a 0.04 mm² speck of loss whose square rim was drawn.
   - WHOSE: maker (`loss_and_tears`).
   - EXACT FIX:
     - (a) For each tongue T, take the pixels of T touching the kept body and the two of them farthest apart, A and B. Flip only the pixels of T on the far side of line AB, and leave all others as before the opening. Then jag AB like a tear segment (3 levels, 6 per cent). Run `tear_tests` on the final mask's outline (traced and simplified at 0.5 mm), not on the drawn lines: it must be 0.
     - (b) The rim is `distance_transform_edt(~lost) ≤ w`, with w = 0.4 + 0.8 × value_noise(6 mm) mm, at least 1 px.
     - (c) Before the rim, drop lost components under 1 mm².

4. **Enamel chips drawn over the bolt heads and over each other (fault, small).**
   - WHAT: on H02_C (placed at eye level on the quay post) and H01_B and H01_D, brown chips with light rings lie on top of the grey bolt heads. Three to six chips per bolt overlap, each ring crossing the next, so a cluster reads as frog-spawn.
   - WHOSE: maker. `enamel_plate` draws `bolt_head` before `chips`; each chip is ringed and tinted on its own.
   - EXACT FIX:
     - Draw the chips first and the bolt heads (with their rust rings) last.
     - In `chips`, gather every chip's coverage into one mask, then ring and tint the union once.
     - Test: no chip or ring pixel inside a head's 9 mm radius; no ring pixel inside any chip.

5. **Letting boards' foot bites end in needles (minor; does not fail alone).**
   - WHAT: L04_C (west pier, 2.15 m), L02_C and L03n_C. The ragged top throws spikes 1 to 3 px wide and 8 to 15 mm tall, which read as thorns.
   - WHOSE: maker (`peel_bites`).
   - EXACT FIX: run `cut_protrusions` (with fix 3a) on each bite at sizes 2, 4 and 8 mm. Cap the jag at 1.0 mm. Test: `protrusions_left` = 0.

## Narrow points (each passes)

6. **S01n_D (2.53 m):**
   - The flakes nibble every letter and border edge evenly (a "distressed font"). FIX: start runs only inside 3 to 6 clusters, each 40 to 120 mm along the plate and at random; no flakes outside them; flakes 2.5 to 5 mm; share as now.
   - The chalky patches are soft white blobs. FIX: drop the patches; lighten the ground by 3 per cent at the top, falling to 0 at the foot, and add 0.1 roughness.
7. **Lime** (S01n_D, H01_D, H02_C): the runs are rods of even width with a round bead and a T-shaped head. S01n_D's long run is 3.2 degrees off vertical. FIX:
   - each run's half-width follows value noise at 5 mm, between 0.8 and 2.5 mm;
   - the centreline wanders ±0.6 mm over 15 mm;
   - the splat is a 5 to 9-lobed blob;
   - the angle is at most 3.0 degrees, measured.
8. **P01_B (held):** the foot tear is a staircase (two 20 mm runs, one horizontal and one vertical, meeting square). FIX: redraw any tear line with two consecutive segments, each within 10 degrees of an axis, meeting at 80 to 100 degrees.
9. **Ballpoint blot:** a perfect disc in the line's own colour, like a pin head on the d of "Reward" (SA06). FIX: 0.5 to 0.8 mm, elongated 1.5 to 1 along the stroke, 0.2 mm past the end, 15 per cent darker.
10. **v1's narrow points:** the cards' tabs end at the card edge; P03_B's rain hairlines; the even POLICE band; Patrick Hand's 9. These stand.

## What I cannot judge

- **The lit look:** how the engine uses height (normal or parallax), and whether a card behind glass should have height only at or below 0.
- **True on-screen magnification** at the doors.
- **The art slots,** which are stand-ins.
- **The check's v2 result,** which had not landed.
- **Period photographs at 1:1:** there are none, so process and wear judgements remain Judgement.
