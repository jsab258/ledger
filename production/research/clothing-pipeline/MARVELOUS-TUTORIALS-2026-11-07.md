# Marvelous tutorials for game garments: what adds to the 1 November deep-dive (7 November 2026)

All pages read 7 November 2026 by fetch (answers came through a summariser, not raw text; so wording is the tool's, numbers are quoted from it). Marvelous help articles were read through the public Zendesk API (https://support.marvelousdesigner.com/api/v2/help_center/en-us/articles/ID.json), as the deep-dive did. Already in DEEP-DIVE-2026-11-01.md and not repeated: the DNA importer, 8-joint skinning, 2.5 to 5 mm collision thickness, the sweater collar, the leather-jacket "thickness off before retopology", Bezrodny's 2 to 3K triangles per piece, Epic's LOD percentages.

## 1. Particle distance

- Official [Particle Distance Setting, article 47358268602777](https://support.marvelousdesigner.com/hc/en-us/articles/47358268602777): range 0.8 to 700.0; about 20 mm while making the garment and dressing the avatar, "under 5 mm" once complete, for quality. No default stated.
- Marvelous [Unreal tips, 47358145573401](https://support.marvelousdesigner.com/hc/en-us/articles/47358145573401): raising particle distance lowers face count. No value given.
- Remeshing article [47358347315481](https://support.marvelousdesigner.com/hc/en-us/articles/47358347315481): a changed particle distance carries into a remeshed pattern.
- Whether artists change it again before export: not stated in any page read. Search-snippet only, unverified: a forum answer of 20 mm tri-mesh for draping, then 5 mm for a beauty pass before retopology; a Japanese note that 5 is the smallest value that simulates cleanly.

## 2. Collar on the neck when the head turns

- Not found in any official page or reached artist piece. The Unreal tips article says close-fitting garments are skinned to the body, with the body mesh's weights copied to the garment on Apply, then smoothed or painted by brush (same article).
- Same article: pattern pieces "should not be too close together or have any overlapping" (matters for weight painting); the 2D layout carries into Unreal's weight-painting view.
- Tides of Tomorrow spotlight (search snippet only, unverified): simulate with zero gravity so the in-engine garment does not keep creases from the T or A pose. Page body unreached (below).
- No stated method for high collars found.

## 3. Low-poly mesh from the drape

- Marvelous: Remeshing (Quad Grid mesh style from 2024.0) gives "aligned automatic Retopology" quads ([47358347315481](https://support.marvelousdesigner.com/hc/en-us/articles/47358347315481)). Rotating a pattern in the 2D window changes the grid direction; undo and reapply. EveryWear: "Quad Optimize option can achieve auto retopology" ([47358145573401](https://support.marvelousdesigner.com/hc/en-us/articles/47358145573401)); triangles work with Chaos Cloth, so no quad retopology is needed there; a Remesh node in the middle LOD collection reduces density.
- Manish Nautiyal, WWII trousers ([80.lv](https://80.lv/articles/how-to-create-wwii-inspired-trousers-with-marvelous-designer-zbrush)): flattened pattern to ZBrush, ZRemesh to quads; Maya "Transfer attribute by UVs" to bring UVs back and wrap it over the simulated mesh; thickness by ZBrush Panel Loops; low poly and UVs in Maya. No triangle counts, no particle distance. About 24 hours total. (Summariser also reported, unverified: quad meshing breaks down on diagonal or curved borders.)
- 80.lv [Exporting from Marvelous Designer](https://80.lv/articles/tutorial-exporting-from-marvelous-designer): steps are images; text says only "a quick Zremesher in Zbrush would do", aimed at animation and VFX, not game.
- Triangle counts for a hero or background character: none found in any source read (only Bezrodny's, already noted).

## 4. UVs and bake maps

- Marvelous USD export: Thick on, unified UV (Unreal tips). PBR Texture Generator makes normal, opacity, metalness, displacement maps from fabric in one click (same article).
- Artists: UVs made in Maya on the low poly (trousers piece above). Which maps come from which mesh: not stated in the pieces reached.
- Search snippets only, unverified: leave space between UV islands for thickness; export separate low and high files; bake stitches and wrinkles to normal or height; Polycount thread where name-based baking put sleeves on the bodice (page 403).

## 5. Avatar pose and arrangement points (official)

- [Avatar Editor, 47358128221337](https://support.marvelousdesigner.com/hc/en-us/articles/47358128221337): for Marvelous pose and motion files, set the avatar in a T-pose (IK Joint step; Reset Pose returns to it). A-pose not mentioned. An .AVT stores model, skeleton rig, sizing, pose, motion. "Re-fit the measurements when changing its Pose." Arrangement points other than the body's are symmetric by default; new ones start unassigned and need a Bounding Volume and X, Y; a saved .ARR on another avatar "may need readjustment".
- Search snippets, unverified in full: Auto Convert to Avatar (10639897 id 47358210639897) notes an A-pose human mesh; .arr files hold the blue arrangement points; ZPrj keeps arrangement points and bounding volumes.
- Arrangement tutorial 47358281785369 is video only, no transcript: unreached.
- Exporting for skinning to an existing skeleton: only the Unreal tips and MetaHuman USD articles (already in the deep-dive); nothing new.

## Not reached

Marvelous help HTML pages (403; API used); Polycount 2760622 (403); Reblium and Mauvemorn Notion pages (script-drawn, empty); Tides of Tomorrow spotlight body (title only); Marvelous magazine PDF (binary, unreadable); Gnomon workshops (paid video); ICVR Lightfall tutorial (forum summary only); Auto Convert and remaining search results beyond the first pages; search results 8 to 24 on particle distance not read.
