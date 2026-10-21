FAIL

# The empty unit (east_parade bay 3, no. 7), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, 15 October 2026)

**Reviewer.** I did not write the target or build the shop. I judged one view only: CLOSE_35 and CLOSE_35_B, by day and night_lit. I did not read the street view's review.

**Read.**
- CLAUDE.md and RULINGS.md (as briefed).
- NOTES.md: "For the next nine shops", "For the next shops" and the empty unit's own section (E1 to E6 and its shortfalls).
- TARGET.md: sections 3 and 5.3, D10, LIT-03, and A13 in "Changes after the build".
- Rita's two close reviews (the lessons).
- `checks/check_empty_unit_v1.json`.
- The code: `sw_front_extras.late_empty_unit` (the whitewash), `sw_front.make_glass_rows` (the number) and `sw_variants` (the boarded stallriser).
- The 4.1 manifest's two empty_unit entries.

**Looked at.**
- The two close previews.
- The four close gate frames (2560 x 1440, made 14 Oct 00:57 to 01:03), at 100 to 300 per cent.
- The 4.1 whitewash tile and the build's composite of it.
- The street preview, only to find the letting board. It hangs on the fascia, which is outside both close frames.

**Measured** with Pillow in my scratchpad; nothing in the repository or SCRATCH was changed. Luma is Rec. 709 on the sRGB values.

**In short:** the joinery, the doors and the night are right at close range. The whitewash is not. The 4.1 tile's cloth swirls, wiped patches and clear margin were flattened away when it was composited, so at 1.5 m every pane is a near-flat pale tone with about one level of detail. The brief names that tone as "the white board".

**Count:** one fault, three narrow points.

## Fault

### 1. The whitewash reads as a flat pale board, not as whiting on glass

**Where.** The rectangles below are inside the lights, in the 2560 frames.

| frame | light | box (x, y) | mean | std | detail in 16 px blocks |
|---|---|---|---|---|---|
| CLOSE_35 day | left | (608-848, 192-992) | 179.0 | 3.1 | 0.95 |
| CLOSE_35 day | middle | (960-1488, 112-1040) | 179.6 | 2.7 | 0.78 |
| CLOSE_35 day | right | (1616-2560, 0-1248) | 179.1 | 3.4 | 0.65 |
| CLOSE_35_B day | left | (0-896, 0-1216) | 179.2 | 2.5 | 0.59 |
| CLOSE_35_B day | middle | (1040-1616, 96-1104) | 179.5 | 3.3 | 0.84 |

- The brick beside the window has 17.1 levels of detail in 16 px blocks. The panes have under 1.
- At night the lights read 38.6 to 40.3 with 0.53 levels of detail.
- At 100 per cent (CLOSE_35 day, 1500-2140 by 250-610) the pane is a soft grey fog. It shows no cloth swirl, no streak, no thin patch and no edge where the whiting stops at a bead. These panes are about 65 per cent of both close frames.

**Why.**
- The 4.1 tile (`window_whitewash_rgba.png`, 3250 x 1800, mean alpha 0.797) keeps all its character in its alpha: the circular cloth swirls, about 15 wiped patches, and a clear margin at its edge. Its colour is almost flat: RGB mean (228, 222, 206), std 3.5.
- The build (E1) composites that alpha over a ground of (214, 212, 204), within 14 levels of the whiting's own colour. So everything the alpha drew disappears. The composite has a std of 3.6 levels, a range of 210 to 231 and a mean gradient of 0.22.
- It is also halved to 1625 x 900, which gives 2 mm a pixel. At CLOSE_35 the near glass is about 1.2 mm a screen pixel, so the tile is soft as well as flat.
- The builder's fourth shortfall (the strokes run across the bars) cannot even be seen, because there are no strokes to see.

**Whose:** the builder (judgement E1). The target is silent on the ground colour.

**Exact fix** (in `sw_front_extras.late_empty_unit`):
1. **The ground.** Change (214, 212, 204) to (104, 110, 116), the grey-blue of an unlet shop's glass in P6. Keep the tile's alpha and keep the pane opaque, so there is still no see-through slot and no room.
2. **Full size.** Do not resize the composite. Keep 3250 x 1800 at one pixel a millimetre.
3. **Each pane on its own.** Map each light, toplight and door pane to its own window of the tile: its own size in millimetres, at its own offset, so that no two neighbours repeat. Multiply the alpha by an edge ramp running from 0 at the bead to 1 at 20 mm in, so the whiting stops short of every bar. That closes the fourth shortfall too.
4. **Re-run LIT-03.** My estimate is a day mean of about 157 at STREET_SQUARE: (0.8 x 221 + 0.2 x 107) x 0.8, the ratio the gate gives now. The limit is at least 150. Night must stay at 40 or under. If day falls below 150, lift the ground to (124, 128, 132), not the tile's colour.
5. **Add a row** (the kit's rule 15: check what the eye sees). At CLOSE_35 day, inside each lower light:
   - the mean std in 16 px blocks is at least 3 levels;
   - the 1st percentile of luma is at least 25 levels under the median, so the wiped patches show.

   Today the first reads 0.6 to 0.95, and the 1st percentile sits 6 to 10 under the mean.

## Narrow points

### N1. The house number 7 is cream on cream, and on the other door's fanlight

**Where.** CLOSE_35_B day, the glyph at (2205-2240, 225-290).

**What is wrong.**
- The 4.1 row 12 paint is cream (225, 218, 197). The whitewash under it is (228, 221, 206). The glyph reads 143 to 178 against a pane of about 175, so the number shows only by its edge shading.
- The flaking leaves its top bar a small ring, so at 100 per cent it reads as a hook more than a 7.
- 4.1's manifest puts this row on the **side-door fanlight** (x 21.82, baseline z 2.18). There, cream paint stands on clear glass over the dark hall, which is what it was drawn for. The build put it on the shop door's fanlight (about x 22.8), which it whitewashes. That move is not named in NOTES.md (E3 says only "on the glass's outside").

**Whose:** the builder.

**Exact fix.**
- Place row 12 as 4.1 does: side-door fanlight, x 21.82, z 2.18, d 37.
- Leave that one fanlight clear, with the kit's reflection-only glass. The hall that FRN-09 checks is already behind it.
- If the number must stay on the shop door's fanlight, ink it black (35, 36, 40).

### N2. The stallriser's twelve screws are white specks

**Where.**
- CLOSE_35 day: a row from (896, 1248) to (1352, 1424).
- CLOSE_35_B day: (344-1600, 1216-1408).

**What is wrong.** `sw_variants` (boarded) gives the ply sheet's screws the material "white". On the dark board (46, 37, 30) they read as bright pin-points, like noise, not as screw heads.

**Whose:** the kit. The boarded variant is used by this shop only.

**Exact fix.** Paint the screws over in the stallriser's paint (46, 37, 30, roughness 0.6), as a sheet painted after fixing would be. Or make them zinc-plated steel (150, 150, 148), metallic 1.0, roughness 0.45.

### N3. No glass over the whitewash

**What is wrong.** The pane is a matte quad (roughness 0.9). At 35 to 61 degrees off the glass by day, real glass would lay a faint sheen of the street over the whiting. Here there is none. The builder names the glass as owed to the PC (the game's whitewash material). For the cloud's frames it is cheap to show.

**Whose:** the builder, and owed to the PC.

**Exact fix.** Add a clear coat to the whitewash material: Principled coat weight 1.0, coat roughness 0.02, coat IOR 1.5. Keep it to reflection only, as the kit's rule 2.

## The builder's named shortfalls: fault or narrow

- **"Nothing behind the glass."** Not a fault: the target asks for no room. The room criteria of this view (the display, the parallax by `trace`, the black slab at CLOSE_35_B, the seam) do not apply. No display or room exists, and none was judged.
- **"Dark paints in shade" (FRN-10's one failure).**
  - The failing patch is at STREET_SQUARE, which is not this view.
  - At the close cameras FRN-10 finds 0 dark patches of 28 px or more. I agree: CLOSE_35 has 34 px under luma 8, and CLOSE_35_B has 4,776 px.
  - I looked at the largest dark runs at 300 per cent: (2127-2344, 327-811) and (2249-2287, 820-1164). They are the shop door's rebate and glazing-bead shade, 4 to 5 px wide. That is natural joinery shade, not a coplanar strip.
  - For this view: a narrow point at most, with no fix needed.
- **"Lamp 42,000 W against 50,000."** Not a fault. It is the gate's stand-in light; the game's lamps are owed (PC-02).
- **"Strokes run across the bars."** Part of Fault 1, and its per-pane fix (step 3) closes it.

## What is right

**The joinery at close range.**
- The T2 window's bleached-white beads, mullions, transom and toplight bars are crisp and correctly shadowed (CLOSE_35 top, 350-1000 by 0-300).
- The panel pilaster and its capital are in bare timber, and the fascia's worn edge shows at the top right of CLOSE_35_B.
- No black strips anywhere.
- No see-through slot. FRN-08 reads 0 px at both close cameras, and I saw none.

**The shop door (T1).** Black.
- Hinge on the viewer's left, a brass lever on the right.
- A brass letter plate in the lock rail, clear of the glass.
- The glass foot at the rail, and a brass kick plate with its screws at the foot.
- The jambs are clean.
- No OPEN/CLOSED card and no hours plate, correctly for a unit to let.
- The bell sits on the top rail inside; it cannot be seen from outside, as it should be.

**The side door (F1).** Black and four-panelled.
- A centre knob and a nightlatch cylinder on the lock stile.
- A pale frame with a clean joint against the shop door's frame.

**The night.**
- No stand-in arc and no burn: 0 px with any channel at 250, and the brightest pixel is luma 54.7.
- Nothing glows through the glass.
- The pale panes catch the street lamps at 38.6 to 40.3 against the brick's 18.6. That is right for pale whiting under sodium, and it is what LIT-03's night limit allows.

**The content rule.** Nothing in view breaks it: no goods, drink, betting, toys or people.

**Every legible word at 100 per cent in the two close views:** only "7", the shop's own fictional house number, which is acceptable. No maker's name is on any fitting. The letting board (TO LET) and the fascia are outside both close frames.

**The export faults found in Rita's shop:**
- Height map exported as a normal map: GLB-01 and FAS-01n pass (blue mean 256).
- Textured primitive without UVs: FAS-03, 0.
- Coplanar black strips: FRN-10, none visible at close.
- See-through slot: FRN-08, 0 px at close.
- Visible night stand-in light: none.

None of the five repeats here.

## Check rows

**Trusted (measured on the meshes, files or rays):** GLB-01, FAS-01n, FAS-03, FRN-01 to FRN-05, FRN-07, FRN-08, FRN-09, GLS-01, GLS-02, CAM-01, X-PRV, and NEV-01 (a text scan).

**Only the cloud's stand-in:**
- **LIT-03.** The gate's lamps and exposure. It also measures only a mean, so it passed a flat pane. That is why Fault 1 needs its own row.
- **FRN-10's luma part.** The stand-in light decides the shade.

**A statement, not a measurement:** NEV-02.

## What I cannot judge from the files

- The game's whitewash material, glass reflection, Lumen, exposure and TSR, and the game's own night lamps (owed to the PC).
- The front's glb (7.0 MB, outside git): I judged it only through the renders and the check.
- The letting board and the fascia: outside both close frames, so they are the street view's to judge.
- The bell: hidden, as it should be.
- The side door's letter plate stands upright in its upper-left panel. That is the F1 asset's own fitting, shared with the other shops, and the target gives only "250 x 40". I leave it to the target's owner, not as a fault of this shop.
- The frames' sample count: NOTES gives 32 samples for these gate frames, the brief 64. The panes' flatness is in the tile composite itself, not noise, so this does not change the verdict.
- I ran no OCR. The words were read by eye at 100 to 300 per cent.
