# Tom's zip jacket: the zip and the pockets (26 October 2026)

The question: how to add a zip and pockets to Tom's 1990 cotton blouson (scripted in Marvelous Designer 2026.1, then a skinned game mesh of 18,000 to 22,000 triangles, 2048 maps, no cloth). Every web source was read on 26 October 2026. "Measured" means checked on this PC; "UNVERIFIED" means no source confirms it; "(I)" marks our inference.

## 1. How games show a zip and pockets

- **Geometry for the silhouette, maps for the rest.** Thunder Cloud Studio decides what is "modeled with polygons on LOD0 and which should be baked" by the silhouette, since normal maps "can't alter the silhouette" (https://thundercloud-studio.com/article/topology-for-low-poly-game-characters/).
- **Floating detail is the standard bake.** Polycount's wiki: floaters work because the normal map "stores the direction the surface is facing rather than real depth"; for occlusion, make the floater a separate object casting no shadow (http://wiki.polycount.com/wiki/Normal_Map_Modeling, modified 26 November 2025). Marmoset (Joe Wilson, 19 December 2025): "You can float details on top of the surface"; height and position bakes suffer (https://marmoset.co/posts/toolbag-baking-tutorial/).
- **CLO's own advice for a game zip is the maps.** Its community manager, on retopologising an MD zipper: for a game, "you might want to integrate the zipper directly on the maps instead of having more geometry". MD's retopology skips trims; custom low-poly zipper parts can be imported (https://support.marvelousdesigner.com/hc/en-us/community/posts/48268519616537, 11 July 2023).
- **Pockets that shape the outline are geometry.** Remedy kept a separate render mesh, or "the silhouette of the pockets and the front part of the jacket would have been lost" (Henrik Enqvist, 29 April 2010, https://www.gamedeveloper.com/programming/the-secrets-of-cloth-simulation-in-i-alan-wake-i-).
- A portfolio piece (not a game) put "the zippers which couldn't be baked down" on alpha cards (Shaafi Ahmad, 80.lv, 5 August 2020, https://80.lv/articles/making-a-dress-and-a-leather-jacket-in-marvelous-designer/).
- **Measured, Mafia: The Old Country:** jackets of 14,186 to 30,693 triangles, most one mesh section with one material; a second appears only for a strap or holster (F:/LedgerTools/aaa-study/mafia/study-6/garment_meshes.csv). Trims get no material of their own. Whether its buttons and pockets are modelled was not opened (UNVERIFIED); its period has no zips.
- **At our budget (I):** welts and zip teeth rise 1 to 3 mm, below the outline at a third-person camera: baked. The pull stands 5 to 10 mm proud and catches light: a small mesh, about 200 triangles. The tape: a strip a few rows wide. Under 1,000 triangles in all. No AAA source on zip pulls was found.

## 2. A zipper by script in MD 2026.1?

- **No documented function makes one.** CLO's API list has 18 zipper functions, all getting or setting a *style*: type (plastic, metal, nylon...), teeth as "Texture" or "OBJ", width, weight, tape thickness, slider, puller and stopper files (https://developer.marvelousdesigner.com/list.html). The changelog, ending at 2025.1.201, never mentions zippers (https://developer.marvelousdesigner.com/changelog.html).
- **The manual makes them by hand:** Zipper tool, click the garment or pattern, double-click each end, repeat on the other side; slider, puller and stopper come with it. The tape is its own pattern with particle distance, fold and physics (support.marvelousdesigner.com articles 47358168494745 "Create Zippers", 2 April 2026; 48920706512665 "Zipper Style"; 47358231940889 "Zipper Tape Properties"). Our own low-poly parts can be registered as OBJs (47358323508377, 2 April 2026).
- **Measured, undocumented:** the running program lists `utility_api.GenerateZippersFromObj`, and its export options carry `zipperList` (MD-API-2026.1.237.json, our probe of 26 October). Neither is in CLO's docs; arguments and meaning UNVERIFIED. Printing its docstring through the bridge is one line; build nothing on it without CLO's word.
- **A zipper made once by hand does not fit.** It belongs to particular pattern edges and would not survive the script recutting the fronts at every pattern change (I). Reuse would mean a hand step each run (script, save, Jafar draws it, script reloads with the documented `ImportZprj`).
- What MD's zipper adds is a stiff, heavy centre-front line and tape geometry; two scripted tape strips give both (I).

**Answer:** no MD zipper. Two scripted tape strips in MD; teeth, stops and pull added in Blender.

## 3. Pockets

**In MD** pockets are extra pieces sewn on. Documented calls: `CreatePatternWithPoints` (welt or bag), `CreateInternalShapeWithPoints` (the slit), the `AddSeamlinePairGroup` overloads that sew to an internal shape, `SetPatternLayer` and `LayerClonePatternPiecePos` (the manual's Layer Clone, for "details made with multiple layers"; support article 47358338558745). MD's "Pockets" lesson is video only. October's tailored jacket already made flaps and a chest welt as pieces lying over the fronts (tools/md/jaeger_spec.py).

**A 1990 cotton blouson** had two hip welts in the fronts, no flaps, no chest pocket, a zip open or under an optional flap, and rib at hem, cuffs and often the collar.
- Neue Mode S21230, men's blouson, catalogue Autumn/Winter 1990/91: "knit cuffs, knit band at hem", knit band or standing collar, "Zipper with optional cover flap, welt or jetted pockets"; flapped breast pockets only on the parka view (https://vintagepatterns.fandom.com/wiki/Neue_Mode_S21230; its text says S21240).
- Marks & Spencer T16/27, 'St Michael' corduroy zip jacket, about 1983, made in the UK, 75% cotton: "a slit pocket on both the LH and RH", knitted waist (https://msheritage.access.preservica.com/uncategorized/SO_d13aab1c-0c20-4daa-b360-ef9b79034c66/).
- Read by a helper only: Kwik Sew 1673 (1987) and 2161 (1992), McCall's 3277 (1987), Burda 5001 (about 1990): all front welt pockets; Kwik Sew 2161 also a zip-pocket view (vintagepatterns.fandom.com).
- The Harrington differs: today "two diagonal frontal pockets with a single button closure" (https://ch.baracuta.com/products/baracuta-g9-harrington-jacket-brcps3001ut3124-309); not a 1990 source.

**For the game** a welt changes neither drape nor outline, so it is not simulated but baked from a floating high-poly welt (I).

## 4. The route

1. **zip_jacket.py:** add two zip tapes (about 12 mm wide, the front's length, sewn between the front edges and into the collar) with a firmer stock cloth's physics; write the welts' places in pattern coordinates (two hip welts about 150 by 15 mm) into the job's spec. Scripted; 1 to 2 hours once, then a 10 to 20 minute drape.
2. **Drape and export as now.** Each piece's UV island is its flat pattern, so a pattern coordinate finds its 3D point on the drape (finish_md_jacket.py already uses these islands).
3. **Blender bake sources:** one modelled tooth arrayed along the tape's centre line; the welts' lips and slit built at their pattern coordinates on the drape, floated 1 to 2 mm; top and bottom stops. Scripted once, 3 to 5 hours; minutes a run.
4. **Game mesh as planned,** the tape kept as a 2 to 3 row strip; bake normal and occlusion at 2048 from drape plus floaters, and an ID mask (cloth, tape, teeth, welt) for colour and roughness. 1 to 2 hours to set up; about 10 minutes a run.
5. **The pull:** one low-poly pull and slider (about 200 triangles), made once by script and kept on F:, at the collar, skinned wholly to the nearest chest or neck bone, in the jacket's own mesh and material. About 1 hour once.
6. **Gate:** a fresh reviewer per view against the 1990 references; teeth and welts read at the game camera; counts inside the table.

All times are estimates (I). **Nothing is done by hand each run.** Three one-line choices go to DECISIONS.md: metal or plastic teeth and colour; slant or upright welts; the optional zip flap.

**Not chosen:** an MD zipper drawn by hand each run (a click each run; CLO says its trims escape retopology); alpha-card zips (a portfolio method; masked edges shimmer at distance, I); simulated pockets (cost without visible gain at our camera, I).

## Unverified

- `GenerateZippersFromObj`; whether `zipperList` exports zipper geometry.
- That baked teeth and welts read at our camera (step 6 checks it).
- British high-street welts of 1990, slant or upright; metal or plastic teeth (the dated patterns are German and American; the British item is 1983).
- Whether our packed roughness map has room for a metal mask, if the teeth are metal.

## Not reached

- MD's "Pockets" lesson (video only).
- A studio talk or AAA breakdown on game zips: none found in three searches.
- British mail-order catalogues of 1989 to 1991; the Westminster Menswear Archive refused the connection (helper's report).
- polycount.com threads (not tried; behind Cloudflare in September).
- support.marvelousdesigner.com and vintagepatterns.fandom.com refused the plain fetch (403, 402) but were read in the browser.
