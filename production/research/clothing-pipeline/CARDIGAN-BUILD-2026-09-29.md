# Building a 1990 cardigan and blouse that read clean (research note, 29 September 2026)

The clothing session asked for this after Sheila's cardigan and blouse failed two blind reviews. A separate helper was given the problem, not a theory, and worked for about thirty minutes, read only. Every source was read on 29 September 2026. **D** means documented, with its source; **I** means the helper's inference. "Search summary" means only a search engine's summary was seen. It does not repeat SHEILA-CLOTHES-2026-09-29.md. DROPS, Purl Soho, ArtStation and polycount refused, and no schematic drawing was seen.

## In short

- **Third attempt (I, from A):**
  - **V point:** level with her underarm, about 18–19 cm below the side of the neck. That is a few centimetres above the bust, not mid-chest.
  - **Buttons:** seven. The top one sits just under the V point and the first 1.5 cm above the hem. Space the rest evenly: (V height above hem − 1.5) ÷ 6, about 5.5–6 cm.
  - **Band:** one continuous band of 25–30 mm, hem to hem round the back neck.
  - **Neck:** the knitted neck edges 13–15 cm apart at the shoulder line, so the band's inner edge lies against her neck. The back neck dips 2–2.5 cm at the centre, so the band's top sits at the base of her neck.
  - **Cuffs and welt:** 5 cm cuffs, drawn in to about 19–20 cm round; 5 cm welt.
- **Draw the edges; do not cut for them (I).** Make the opening one smooth spline on the knit surface and sweep the band along it, with the shell's border tucked under. Plane cuts through a smoothed offset skin leave zigzag borders, and the band copies them.
- **The round collar lies over the cardigan (D [C1], search summary [C6]).** Draft it flat, 5–6 cm wide, with a shoulder overlap of 1–1.5 cm for "virtually no collar stand" [C2]. Its ends meet at the throat, inside the V (I).
- **The blouse in the V is a flat panel with a placket,** its top button just under the collar [C4] (D). With blouse buttons 7.5–10 cm apart (search summary [C5]), one or two show (I).
- **Cuffs** are closed ribbed tubes with a rolled rim (I).
- **Sitting:** weight her back below the waist to the pelvis and lower spine, with no thigh weight (I; see [L1]).
- **Games** shape clothing over the body or simulate it, then clean the borders; it follows the body's edge flow (D [G6][G9]). No dated breakdown of a knitted cardigan was found.

## A. The real garment

- **V depth and buttons (D).**
  - **Bernat's leaflet 137 [K4]:** the neck shaping starts at 12 in and the raglan armhole at 14 in, so the V point is 5 cm below the underarm. Rib 1½ in. The last buttonhole is "2 rows below start of neck shaping".
  - **A Columbia-Minerva collared cardigan [K5]:** the underarm is at 12 in and the front shaping starts at 14 in. Rib 2 in at the hem and cuffs. The fifth button is "½ inch below first neck dec".
  - **The Craft Yarn Council's collared cardigan [K3]:** the V starts 2½–4 in above the armhole. Rib 2 in at the hem and cuffs. Six buttons, "the first one at 1/2" from lower edge, the last one at beg of neck shaping and the others evenly spaced between".
  - **Elizabeth Smith [K6]** puts the last buttonhole where the V shaping ends.
  - **I:** on a plain buttoned cardigan the V point sits within about 5 cm of the underarm, and the top button marks it. Our V, to mid-chest, is too deep; that is why the buttons crowd low.
- **Neck (D [K7], 2024).** A V-neck's width should be "30-40% of the body's cross-back width and no wider than 18 cm", or cardigans slip off the shoulders. The back neck is about 2.5 cm deep. For the Craft Yarn Council's small size, the cross-back is 37–38 cm and the armhole depth 16.5–17.5 cm [K8]. **I:** for Sheila, neck edges 13–15 cm apart.
- **Bands (D [K3][K6]).** Stitches are picked up along the fronts and round the neck and worked in rib. **I:** 2.5–3 cm wide.
- **Collar with a cardigan (D).** Round collars were "perfect for layering under a sweater. They flipped out over the sweater and layered on top" [C1]. To draft one: an overlap of 1–1.5 cm at the armhole, a collar 6 cm wide, and the neckline lowered 1 cm at the back and 2 cm at the front [C2]. A bigger overlap gives a higher stand [C3].
- **The blouse front (D).** The top of the top button sits ¼ in below the collar [C4].

## B. How character artists do it

- **Tinko Wiezorrek (D [G6], 80.lv, 2017)** simulated each piece in Marvelous Designer and then sculpted it into shape, or sculpted the whole garment. He copies "the edge flow of the underlying figure on the clothing", and advises skinning and posing the models yourself.
- **Blender Studio (D [G9]).** The base mesh is duplicated body faces (or a shrinkwrap), given thickness with Solidify, with the border loops cleaned before detailing.
- **Topology (search summary [G8]).** Loops run at the neckline, armholes and hems. Thickness is modelled only at the edges that show, such as collars and cuffs. Folds that change the silhouette stay in the geometry.
- **Covered layers (D [G7]; [L1]).** The body or layer underneath is hidden or deleted.
- **Sitting (search summary; [L1]).** It is fixed with weights and pose-driven correctives. No studio account of a seated cardigan was found.

## C. Fixing our method by script (I, except where marked)

1. **The shell as lofted rings, not a copy of her skin.** At each height, take her hull, set it out 28 mm and give it a fixed number of columns. Trim each ring at the front edge and neckline given by the spline. The hem, V and neck then fall on clean rows. The sleeves are rings along the arm.
2. **The opening as one spline.** It runs from the hem at the centre front to the V point at the underarm, to the side of the neck, round the back neck (dipped 2.5 cm), and down the other side. Sample it every 8–10 mm and snap each sample with `BVHTree.find_nearest`, which gives the position and the normal (D [B2]). Sweep a 29 × 6 mm rectangle along it with bmesh, set square to the surface; Curve to Mesh would also sweep a profile (D [B1]), but it needs the tilt set. Run the shell's edge 8 mm under the band. Give the band a rolled inner edge, to end the frayed double lip.
3. **The collar.** Draft it in 2D: the neckline at the base of her neck, 5.5 cm wide, with round ends meeting at the throat. Lay it with Shrinkwrap in Outside Surface mode, 2–3 mm off the cardigan and blouse (D [B1]). Lift only its first 5–8 mm, by 3–4 mm. It is 2 mm thick with a rolled edge. Build it after the cardigan.
4. **The blouse.** A panel across the V from each level's chest hull, set out 5 mm, so it spans the cleavage. A 25 mm placket raised 1.5 mm, with two 10–11 mm buttons. Hide her skin under it.
5. **The cuffs.** A closed tube of 24–32 columns, 5 cm long and ribbed, its rim rolled 1 cm inside. The sleeve narrows over 8–10 cm and overhangs the cuff by 5 mm.
6. **Sitting.** The back below the waist blends from the lower spine to the pelvis, with no thigh weight and no curtain behind the seat. The front hem, from the side seam forward, takes 20–30% of each thigh. Test seated before the reviewer.

## Sources (all read 29 September 2026)

- [K3] Craft Yarn Council, "Springtime Knit Cardigan", craftyarncouncil.com/april00_knitproj_lg.html (page © 2007).
- [K4] Bernat, *Six Classics for Women*, leaflet 137, "V-Neck Cardigan", freevintageknitting.com (undated).
- [K5] Columbia-Minerva, *Casual Quick Hand-Knits* vol. 735, cardigan 735-6, freevintageknitting.com (undated).
- [K6] Elizabeth Smith Knits, "Frontbands and Buttonholes" (undated; site © 2020).
- [K7] C. Mountain-Manipon, "How to Design Sweater Necklines", sistermountain.com (14 August 2024).
- [K8] Craft Yarn Council, women's size chart, /standards/woman-size (undated).
- [C1] D. L. Sessions, "1950s Tops and Blouse Styles", vintagedancer.com (6 February 2014).
- [C2] Müller & Sohn, "Pattern construction for Peter Pan collar", muellerundsohn.com (4 December 2023).
- [C3] Pattern Studio 101, "Shoulder overlap & collar standing" (undated).
- [C4] Itch to Stitch, "Proper placements for buttons & buttonholes" (27 August 2017).
- [C5] Search summary: fibrecalcs.com, dressed-in-a-dress.com (undated).
- [C6] Search summary: aol.com and yahoo.com styling articles on Peter Pan collar blouses (undated).
- [G6] T. Wiezorrek, "Game Characters: Modeling, Clothes, Materials", 80.lv (13 March 2017).
- [G7] Unity Discussions, "How is character clothing done on mid-tier games?" (posts of 19 September; year not shown).
- [G8] Search summary: polycount and thundercloud-studio.com on garment retopology (undated; pages refused).
- [G9] J. Kaspar, "Creating Clothing Basemeshes", Blender Studio (undated).
- [B1] Blender manual bundled with the Blender MCP: Curve to Mesh; Shrinkwrap (undated).
- [B2] Blender Python API bundled with the Blender MCP: `mathutils.bvhtree` (undated).
- [L1] Our notes: SHEILA-CLOTHES, SEATED-SKIRT, SKINNING-TROUSERS (29 September 2026).
