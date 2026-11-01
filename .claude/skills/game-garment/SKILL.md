---
name: game-garment
description: The one skill for LEDGER clothing. Make a game-ready garment for a LEDGER MetaHuman the professional way (Marvelous Designer pattern and drape, detail in Blender, the bake chain, skinned in Unreal), each step checked against the reference numbers and the Hook sheet. Use for any new garment or outfit, rebuilding part of one (cuffs, hems, collars, toes), fixing a fault seen in the game, refitting a garment to another body, material variants for the crowd, checking a garment against RUBRIC.md before the packaged walk, planning the Hook's garment list, and exporting everything from Marvelous before the subscription month ends.
---

# Game garment

Jafar's order of 28 October 2026 (C6, C7): Mafia's own art page says its clothes were made in Marvelous Designer, sculpted in ZBrush and finished in Unreal; copy the method, never the assets. This skill is that method on this PC. Research behind it: production/research/game-clothing-pipeline/PIPELINE-2026-10-28.md (the professional pipeline) and MAFIA-JACKET-2026-10-28.md (one Mafia jacket at wrist, collar and hem; both reviewed, their fixes applied here). Before starting, read the garment's spec (production/art/clothing/<who>/SPEC.md) and the records of any earlier tries (BAKE-PLAN, RIB-CUFFS, SLEEVE-END).

**Reference first** (RULINGS 28 Oct): every target below starts from Mafia's or Kingdom Come II's number; where none exists the step says "none found".

**Two tries, then ask**, per step: after two failed tries, research and write what failed and why; a third try needs Jafar's yes. The bake route for cuffs (his page, 28 Oct) is the fallback only after the Marvelous rib fails twice (his order C9).

**Always** (his rulings; none of these bends):
- Check what is already in the game and on F: (LedgerTools\garments, production/specs/garments.json) before making or fetching anything; reuse or refit first.
- Accurate to Britain in 1990; plain everyday makes, every one fictional; no real brand mark anywhere.
- Nothing of CLO's ships or enters git: Marvelous's avatars, sample garments, patterns and trims stay on this PC. Nothing of Mafia's or Kingdom Come's either: their published method, never their files.
- Computer use is for Marvelous only, and only the builder uses it; helpers never click.
- A garment passes only in the packaged game, walked by the tester; offline checks are necessary, never enough.
- Whole-person looks go to Jafar at their checkpoint (see "Checkpoints and measures"); a single piece does not.

**Requests this covers**, for example: "make Ron's plain outfit"; "fix Tom's collar so his throat doesn't show"; "refit Tom's jumper to Darren"; "drape the jeans so the hem rests on the boots"; "three material variants of the zip jacket for the crowd"; "check this garment against the rubric before the walk"; "draft a 1990 donkey jacket at Ron's measures"; "list the Hook's basic garments by need, with hours"; "export every finished garment before the month ends". Steps 1 to 9 below make or remake a garment; a refit or variant reruns only the steps it changes.

## 1. Reference and pattern

- Dated 1990 photographs (production/research/plain-1990-clothes); the pattern drafted at the wearer's measures (tools/meshgen/freesewing_draft.mjs, or the bridge's drafters in tools/md-bridge). Marvelous's own templates are CLO Samples, licensed only while subscribed: look at them, never build on them.
- **Check:** pattern girths against body plus ease (SPEC.md); Marvelous's inspection report (areas, particles, layers, seams) against the plan; a fresh reviewer against the references.

## 2. Avatar and pose: drape straight, pose after

- The drape body with straight elbows (tools/md/pose_body.py --keep-arms --straight-elbows), skin offset 3 mm; the finished drape bent back to the reference pose with the body's own weights (tools/md/unpose_garment.py).
- **Check** (tools/md-bridge/sleeve_wrap.py --joints): every sleeve covers 90% or more of the circle to its end; the arm's centre line crosses no cloth.

## 3. Drape

- The bridge job: `python tools/md-bridge/md_job.py JOB.py` drops it in LedgerTools\md-jobs and waits; if the bridge's heartbeat is stale it starts the bridge itself (tools/md-bridge/start_bridge.ps1, his ruling of 30 Oct), so nobody clicks. Marvelous must be open; it is closed for game builds. Particle distance 20 mm while building, then 10 mm on the body and 5 to 6 mm on bands, cuffs, collar and sleeve ends; Fitting quality last.
- Seams welded with weldType FULLY_WELDED (2) when the export needs one mesh; never DEFAULT_WELDED (1, deprecated).
- Marvelous's simulation differs run to run. Keep each job file with its drape number (drape 25a) and its settings in the BAKE-PLAN; judge a change by running the old and the new settings twice each and comparing the measures below, never one lucky run against another. Keep the best drape's exported OBJ: a later run may not reproduce it.
- **Check:** no edge over 1.2 times its pattern length outside seams (the project's mark, anchored on Marvelous's Fit Maps scale, red at 120%); body through cloth 0 beyond 1 mm; cloth inside the body 0 beyond the skin offset; the silhouette against the reference.

## 4. Rib cuffs, bands and hems (Marvelous's elastic)

- Elastic on the band's gathered edge: Strength 10 (CLO's default and recommended), Ratio 100 x band length / edge length; a rib fabric with its Stretch adjusted, weft only; the band's rest round 0.90 to 0.95 of the collision floor (body girth + 2 pi x (skin offset + clearance)): Tom's wrist 200 to 212 mm against a 223 mm floor if the 2.5 mm clearance is per side, 194 to 204 mm against 215 if it is the total (unverified; measure it first); body frozen; the band sewn late (200 steps Normal, then 100 Fitting); 6 mm particles on band and sleeve end.
- Placement on the straight-elbow body: the cuff's arrangement at Y 0, offset 30 (drape 19's best); offset 40 failed (drape 20).
- What failed before, so it is not repeated: drapes 9 to 20 cut the cuff at 197 mm, sewed it to the 231 mm sleeve end (0.85), then shrank its width to 85% in 3D, about 168 mm, 0.75 of the floor: asked below the floor, it gripped into a lump at the seam.
- In the game mesh every open end is closed as Mafia's jacket closes its sleeve: the edge runs over a lip (about 0.46 cm) into an inner facing (about 9.5 cm deep) closed by a nearly flat cap, so no inside shows; loops close up near the edge; the rib's ridges in the normal map.
- **Check:** band centre within 30 mm of the limb's axis; gap to skin 10.5 mm or less; cover 90% or more; no crossing; no point inside; no lump or slit at talk distance (4.4 m), judged by a fresh reviewer.

## 5. Zipper and topstitch

- The project's own teeth (tools/md-bridge/zip_floaters.py) or Marvelous's Zipper tool with our own OBJ teeth; topstitch by Marvelous's topstitch calls in the project's own style. Both only in the high model, baked into maps. No CLO trim in any shipped file.
- **Check:** teeth = length / pitch; 8 px or more per tooth, or a tiling teeth normal.

## 6. Detail in Blender (in place of ZBrush)

- tools/meshgen/blender/import_md_drape.py (weld, pieces); a multires sculpt pass for seam puckers and wear; thickness last (Solidify), as an offset inner wall only where the inside shows. Detail split as Mafia splits it: the silhouette and edges in the mesh; seams, stitch lines, pocket flaps and wrinkles in the normal map.
- **Check:** no non-manifold edge; the openings expected (neck, hem, two sleeve ends); boundaries within 0.05 mm of the plan.

## 7. Game mesh and UVs

- tools/meshgen/blender/retopo_pieces.py and uv_pack_low.py. Marvelous's Game-Ready Export scenario is a 15 mm triangle remesh, UV packing and a 2048 bake, with no retopology, levels of detail or skinning; its retopology tools and EveryWear are window-only (no API call; a "Quad" mesh type can be set by SetMeshType, untested). So the bake chain stays the route and the export is a one-off comparison.
- **Check:** triangles: LEDGER's target 18,000 to 22,000 for a jacket (Study 6; Mafia's lounge jacket 19,131 at full detail, its tops a median 21,994); seams shared, all of them; cloth texel density 1.5 px/mm or more at 2048 (the project's choice, above Mafia's jacket at about 1.2 px/mm; floor 0.9); no UV overlap; padding 8 px.

## 8. Bake, texture and wear

- tools/meshgen/blender/zip_bake.py (normal, occlusion, ID); the ID-tinted garment material in Unreal (tint, tape, teeth; grime and wet values); wear and seams drawn in the normal map, as Mafia draws stitch lines and pocket flaps.
- **Check:** bake hits 97% or more; ID areas within 1%; normals over 60 degrees off under 1% per piece; colour under the street's light against the Hook sheet's palette; the clothing floor (RUBRIC.md).

## 9. Skinning, levels of detail, the game

- tools/meshgen/blender/skin_garment.py: the body's weights, at most 8 influences a point at the top two levels of detail and 4 below (Mafia's jacket: up to 8 at LOD0 and LOD1, mean 5.1, on twist and helper joints, 4 below; Unreal's limit is 8); the elbow's weights taken from the body, not widened by hand (Mafia's jacket, re-measured: the crook's blend 4 to 6 cm, the point's 5 to 8). The cuff's and collar's closed edges kept down to the third level of detail (Mafia keeps its cuff detail to LOD2). Levels of detail: LEDGER's target about 50, 25 and 10% (Mafia keeps a median 47, 25 and 9%; its jacket 19,131 down to 1,505). Imported by tools/ue/import_garments.py into the MetaHuman project; listed in production/specs/garments.json with what it hides.
- **Check:** points over 3 mm inside the body counted per pose (rest, arms down, arms up, walking, sitting) and the worst edge stretch; RUBRIC.md lines 9 to 11; one fresh reviewer per view at talk (4.4 m) and street (3 to 28 m) distance, through the packaged game's camera; the AI tester's packaged walk.

## Records, every garment

- DECISIONS.md one line per material choice; the garment's BAKE-PLAN with each try's numbers; RECIPE.md's clothing chapter gains what this garment taught (setting-free).
- Nothing of Mafia's or CLO's in git or in any shipped file (the licence allowlist's never-ship list: Marvelous's own avatars, sample garments, patterns and trims; zipper parts read as trims); Marvelous closed after each garment session (it holds 6 GB of the card).

## Checkpoints and measures

- **Jafar sees** each whole-person look (all of one character's pieces together, in the packaged game's camera at talk and street distance) before it is called done, and any third try. He is not an artist: show pictures side by side with the reference, say in one line what changed, and ask one question.
- **Fresh reviewers** judge against RUBRIC.md line by line, pass or fail with the frame; the tester walks the packaged game last.
- **Measures**, one line per garment in production/art/clothing/LOG.md: hours including helpers' time, tries per step, faults first found in the packaged game, whether reviewers passed it first time, and Jafar's verdict. Read the last lines of the log before planning a new garment; the pattern of faults says which checks to add.