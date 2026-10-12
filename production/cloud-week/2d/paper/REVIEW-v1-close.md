FAIL

# Close review, first try: paper, cards, boards and plates (FINAL2)

12 October 2026. A fresh reviewer, CLOSE view: the paper-close-* crops, the full PNGs at 1:1, the height and ORM maps, and the glyph manifests. checks/ was still empty.

**Verdict: FAIL.** The print processes read right at 1:1. Two maker bugs show on almost every item, though: every torn bill is a hole inside a 10 mm frame of paper that has not torn, and no plate, sign or board has a rolled edge along its straight sides. The hand cards also do not read as written by a person.

## What passes

- **Processes:** letterpress P03_B (darker rim, mottle, impression in the height map); screen P01_B (flat); litho F01 (rule cut round SUNDAYS); photocopies P04, J01, C02 (toner, speckle, streaks, no halftone); typed H03 (even Courier, as the target asks).
- **Plate relief:** S01 raised 3 mm, S02 1.5 mm, S03 flat, with draft and a rounded top.
- **ORM:** sensible values throughout.
- **Words:** no wrong word, mirroring or content-rule breach seen.

## Findings, worst first

1. **Torn bills: every loss is a hole inside a 10 mm frame of paper (fault).**
   - WHAT: no loss reaches the sheet's edge. A scan of the alpha finds 0 edge-touching losses on B01, F01, F02, G01, G02, M01, P01, P02, P02-named, P03, P03-named, T01, T01-named, T01s and T03-named.
     - M01_C (placed on SF2) has lost its foot, but a 9 to 10 mm strip stays down both sides and along the bottom.
     - F01_B has two L-shaped holes whose inner outline steps square round the text.
     - The edge bites have become inner holes too.
   - WHOSE: the maker. `paper_wear.shape_loss` opens the loss with `border_value=0`, which wipes out all loss within 10 mm of the edge; the paper opening (`border_value=1`) keeps the strip.
   - FIX: pad the mask 11 px (`np.pad`, mode `edge`) before both openings and crop after. In A and B, shrink the whole patch to clear the protected window instead of clipping ray by ray. Accept at 0 inner losses over 0.2 per cent of the sheet.

2. **Plates, signs and boards: no rolled edge on the straight sides (fault).**
   - WHAT: the height rolls off only at the rounded corners (H01_B row 30: 0, 493, 13676…). Halfway along a side it stays at 32768 to the last pixel. Lit, each piece gets a bevel at four corners and knife edges between. The -10 per cent edge shading shows only at the corners too.
   - WHERE: S01n_D, S02n_C, S03n_C, H01, H02_C, L02_C and the other boards.
   - WHOSE: the maker. `paper_render.rolled_edge` runs `distance_transform_edt(alpha > 0.5)`, which does not count the image border as background.
   - FIX: `d = ndi.distance_transform_edt(np.pad(alpha > 0.5, 1))[1:-1, 1:-1]`. S01's arris is the target's 2 mm, not 4.

3. **Hand cards: the letters jump about one by one (fault).**
   - WHAT: each glyph gets its own baseline and size.
     - SA06 line l2 (cap 4.4 mm): baselines 77.51 to 79.90 mm, em 6.02 to 7.39 mm.
     - The l of "Black" sits 1.3 mm high, the u of "Smudge" 0.8 mm; on SB1 the y of "keys" stands well above its neighbours.
     - It reads as a hand font made to bounce. A person's line drifts smoothly, with letters the same size within a word.
   - WHERE: the SA01 to SA15 body lines, the K07 small lines, SB1. The 22 mm felt cards pass.
   - WHOSE: the target. `hand_styles` set ballpoint baseline sd 0.6 mm and size sd 0.06; `jitter_glyphs` draws each glyph independently.
   - FIX: baseline = a slope per line (sd 0.5 degrees) + one wave (0.4 mm, 60 to 120 mm long) + per-glyph sd 0.03 x cap. Size sd 0.025 per glyph times a per-word sd of 0.03. Rotation sd 0.8 degrees. Re-run needed_ppm and the 20-seed check.

4. **Ballpoint reads as felt-tip (fault, moderate).**
   - WHAT: the SA body strokes are 0.8 to 0.9 mm wide and even, with no pressure and no blots (SA06_B "Smudge" at 1:1). A ballpoint line is 0.3 to 0.45 mm.
   - WHOSE: the target (Patrick Hand's own stroke, and `emb_mm` may not go below 0) and the maker (pressure and blots not visible).
   - FIX: allow `emb_mm` down to -0.25 and draw ballpoint at -0.2. Density along the stroke 0.75 to 1.0. A 0.6 mm blot at 1 stroke end in 10.

5. **Sleeve weather on sheets inside the glass (fault).**
   - WHAT: C01a_B, taped inside SF2 with four tabs, also has a sleeve band at the top (which cuts off its top tabs), water beads and fog. C02_A, inside the same glass, has beads and no tabs. Rain cannot reach inside a window.
   - WHOSE: the target gives both items the `notice_sleeve` table; the maker added tabs on top.
   - FIX: `WEAR_OVERRIDE[("C01a","B")] = "glass_bill"`, as already done for P02. C02 on SF2: no beads, ties or fog; two tabs at the top corners. Record both in the target.

6. **S01n_D, the placed plate: the flaking is confetti (fault, moderate).**
   - WHAT: hundreds of sharp light-grey polygons are spread evenly over every stroke and the border, the middles of strokes included. They read as terrazzo. There is no rim of lifted paint, and the white ground is untouched.
   - WHOSE: the maker; the answer to street finding 10 overshot. The table says paint lifts first at the raised edges, share 3 to 6 per cent.
   - FIX: at least 80 per cent of the flaked area within 2 mm of a raised edge, in runs of 3 to 8 flakes, 6 to 25 mm long. Share 3 to 6 per cent of the letter and border area. A 0.4 mm rim at 0.8x the paint's value. 1 per cent chalky patches on the ground.

7. **Water beads are outlined rings (minor fault).**
   - WHERE: C03_A (and C01a, C02).
   - WHOSE: the maker.
   - FIX: a filled lens, 2 to 6 mm, no outline: the paper under it enlarged 1.08x, a darker crescent (-12 per cent) on the lower 0.3 R, a highlight (r 0.2 R, +35 per cent) at the upper left.

8. **String-hung cards: the string and knot are paper-coloured (fault, small).**
   - WHAT: on K01 A to C and K06a_B the knot is (236,236,236) on a card of (240), so no string shows. On K06a it cuts a notch out of the sucker.
   - WHOSE: the maker; the target says (150,150,146).
   - FIX: a string 1.0 mm wide and an 8 mm knot in (150,150,146), drawn over the sucker and straight up to the top edge.

9. **Star cards: the tab is clipped to the star (fault, small).**
   - WHAT: on K07a to K07d only a 15 mm triangle of tab shows, inside the top-left point; the rest is at alpha 0. The star has no visible fixing, and the triangle reads as a stain.
   - WHOSE: the maker; the target says part of the tab passes the card's edge.
   - FIX: draw the whole tab; off the star, (196,164,84) at alpha 0.5.

10. **Rust and lime look airbrushed (minor fault).**
    - WHAT: the screw haloes are even, soft orange glows (L01 to L04, H01, S01). The rust runs are straight rods of even width (L02_C: 2 mm by 60 mm), so screw and run read as a pin. H01_D's lime is a soft white beam about 20 degrees off vertical; S01n_D's is a soft glow.
    - WHOSE: the maker.
    - FIX:
      - Halo: a 2 to 4 mm ring at 0.5, weighted 3 to 1 below.
      - Runs: 4 to 6 mm wide at the screw, tapering to 1 mm, wandering up to 2 mm, opacity 0.35 falling to 0.05.
      - Lime: within 3 degrees of vertical, (235,235,228) at 0.85, a hard ragged edge, 1 to 3 drips.

11. **Enamel chips are black splats (minor fault).**
    - WHERE: H01_D, the lower-left bolt.
    - WHOSE: the maker.
    - FIX: rounded, scalloped chips: a 0.5 to 1 mm ring of ground coat (190,190,185) round dark steel, rusty in classes C and D.

12. **Cockle is noise over the whole sheet (minor; I cannot judge it lit).**
    - WHAT: F01_B's height map is ±1 mm blobs every 12 to 40 mm. Under a raking light every bill would look crumpled.
    - WHOSE: the maker (the numbers are the target's).
    - FIX: 4 to 10 vertical wrinkles (50 to 300 mm long, 3 to 8 mm wide, 0.4 to 1.5 mm high), 2 to 4 paste bubbles (20 to 60 mm), and a ripple of no more than 0.15 mm.

## Narrow points (they pass)

- **Door cards at 2 px/mm (K01, K05, K06a, K06c, K09a):** the edges show steps once enlarged, and the tab's edge steps by a whole pixel. Fix: draw the tab at 4x and average it down.
- **Tabs on rectangular cards** end at the card's edge; the picture has no margin. This is the target's geometry.
- **P03_B's rain runs** are 1 px hairlines.
- **C01a's POLICE band** is a perfectly even solid.
- **Patrick Hand's 9** has a tail, so "99p" comes close to "qqp".
- **Lost paper's height** is -0.87 mm. It should be about -0.1 mm, the paper's thickness.

## What I cannot judge

- **The lit look:** how the height maps look in the engine (findings 2 and 12).
- **The game's real magnification** at the windows.
- **The art slots,** which are stand-ins.
- **The automatic check,** whose result had not landed.
- **Period photographs:** none at 1:1, so my process judgements are Judgement too.
