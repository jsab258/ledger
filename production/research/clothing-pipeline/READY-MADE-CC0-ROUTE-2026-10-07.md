# Ready-made CC0 garments for Ron: the refit route (7 October 2026)

After review 3 [14]. D = read at source; S = search summary; I = inference. Figures: my script, on MakeHuman's base body hm08 [6].

## 1. Licences

- **Fisherman Sweater** and **Wool Pants** (Margaret Toigo, December 2017): every .mhclo and .obj says `author MRT`, `license CC0`; the pack index, MargaretToigo, CC0 [1–3, D]. No readme. Nothing restricts game or AI use (I).
- hm08 is CC0 since 2020 [4, D]; MakeHuman's fitting code is AGPL-3 [5, D]: use its formula, not its code (I).

## 2. Shape

**Sweater:** 2,126 points, all quads, for subdivision; **one missing quad, centre front chest** [1, D]. Red rib knit, own knit normal map, pattern-piece UVs (D).
- Sleeve, armpit to cuff: 41.5, 33.5, 30.5 (elbow), 26.9, 22.2, 17.0 cm, narrowing; ease 9 to 11 cm upper arm, 3 to 4 cm forearm and cuff [6]. Cuff and sleeve one mesh: no staircase (I).
- Torso ease only 1.6 to 2.8 cm [6], close-fitting (loose is 10 to 15 [9, D]); on his skin, 30 September, a second skin [7, D].
- Verdict: plain 1990 crew-neck once recoloured and loosened; the slim body is the modern giveaway (I).

**Trousers:** 1,372 points, all quads; hems 39 cm; **a small hole at the fly** [2, D]. Charcoal wool.
- Ease: mid-thigh 9.4 cm, knee 13.1, seat 3.9; crotch 3.6 to 6 cm below the body's [6]: not leggings.
- Verdict: plausible; the hem tapers where 1990 work trousers ran straight [13] (I).

## 3. Method and pitfalls

1. **MakeHuman's fit:** three base-body points, weighted, plus an offset scaled per axis [5, D]. Offsets never grow with girth, so a heavy body's contours print (I). The .obj sits on the maker's body: fit through the .mhclo [6].
2. **Carry onto a smoothed form, not the skin,** as Epic's resizer (~1,500 samples) [11] and Roblox's cages [10, D] do. Surface Deform needs a close, valid target; Mesh Deform carries a coarse cage; Shrinkwrap *Outside* moves only points inside, *On Surface* makes leggings [8, D].
3. **Keep the design:** Smooth Corrective, rest *Original Coordinates*, removes the carry's distortion [8, D]; a studio morphs garments to four bodies and bakes folds into normal maps [12, D].
4. **Skin:** body weights only where close and aligned, the rest filled [15, D]; loose parts from the form; the panel binding that walked [11].

## 4. A one-hour try

1. Pin inputs, credit (5 min); fill both holes, open edges exactly 4 and 3 (5).
2. fit_mhclo.py, its form, `--field-sigma` ~0.7 dm, not 0.25 (I) (10).
3. Torso to hull plus 2.5 cm; legs straight below the knee; Smooth Corrective; Shrinkwrap Outside 5 mm (15).
4. Subdivide once; 3 mm turned-in edges (5); skin_garment.py panel binding (10).
5. Recolour; five poses, two lights (10).

**Accept only if, in every pose:** sleeve circumference never rises down the arm; upper arm his plus 6 cm; cuff 3 to 10 mm off the wrist; last four sleeve rings planar within 3 mm; jumper 10 cm over chest and belly, slices convex; trouser mid-thigh his plus 8 cm, knee 1.22 times his [11], hem at least the knee less 2 cm, no seat cleft; crotch 3 to 6 cm below his; no face stretched over 40% seated or 30% arms up; welt rising 3 cm arms up; no skin through; a fresh blind review.

**Recommended (I):** try it. The trousers bring a designed shape; the sweater its sleeves, cuffs, neck and UVs, but not a loose torso.

## Sources (read 7 Oct 2026 unless dated)

1. toigo_fisherman_sweater files (F:, 30 Sep)
2. toigo_wool_pants files (F:, 30 Sep)
3. Pack index entries (2017)
4. hm08 base.obj header (2020)
5. MakeHuman proxy.py, GitHub
6. My script; bodies README (29 Sep)
7. Fitter run j1 pictures (30 Sep)
8. Blender 5.2 manual, deform modifiers
9. Craft Yarn Council, Body Sizing
10. Roblox, Caging best practices
11. TAILORED-FIT (30 Sep), TROUSERS-AND-CAP (29 Sep), suit jacket READMEs (1 Oct)
12. Chopin, NPC clothing for Tides of Tomorrow (26 Aug 2026)
13. plain-1990-clothes NOTE (Smith's Dock, 1990–91)
14. RON-OUTFIT-REVIEW-3 (7 Oct)
15. Abdrashitov et al., Robust Skin Weights Transfer (2023)
