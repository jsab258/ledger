MetaTailor free test: Tom's jumper onto Sheila's S4 body (12 Nov 2026, 12:30 to 13:40)

Method researched: METATAILOR-METHOD-2026-11-12.md (the vendor's steps as read: import avatar, import cloth with a category, place, fit, export FBX). Run on his word in the chat ("go now", 12:55), clicks in MetaTailor only (his ruling of 12 Nov). Try 1 of 2. Nothing enters the game.

## What was done
- Avatar: Sheila's S4 full body (body and head, LOD0, her 341-bone skeleton) from F:/LedgerTools/bodies/MH_LenaS4/MH_LenaS4_FullBody.fbx, re-saved by Blender headless. The body file alone has no head; the head gives the neckline something to fit against.
- First import: the body came in lying on its back (Blender's default FBX keeps the up direction in a node rotation that MetaTailor's reader ignores). Fixed in one go: hierarchy flattened, transforms applied, axes baked into the points (bake_space_transform). Same for the jumper. Files: F:/LedgerTools/tool-tests-2026-11/metatailor-test/sheila_s4_body_flat_yup.fbx, tom_jumper_static_yup.fbx.
- In MetaTailor 2.7 (free, signed in): new project, Custom Avatar Import (materials, parts, landmarks auto-placed), Import Cloth (category Shirts clicked; whether it took over the default Jackets was not confirmed), automatic pose warp, confirm, fit with its default stages (unpenetrate, tuck-in, shrinkwrap, pull-out, apply visibility, tweak weights), Export FBX (1 of 5 free exports) with its defaults (scale x100; avatar, clothes, skin weights).
- Export: F:/LedgerTools/tool-tests-2026-11/metatailor-test/mt-export-1/mt-export-1.fbx (4.9 MB).
- Measured in Blender headless with the refit's checks (scratchpad script measure_fit.py, copied to F:/LedgerTools/tool-tests-2026-11/metatailor-test/measure/), the same way on yesterday's Blender carry (step 1 of the Sheila refit, before its bands and neck work). Against MetaTailor's own exported body too: same numbers (3,024 vs 3,022 body points through).

## Results (rest pose)
| Check | MetaTailor | Blender carry (11 Nov, step 1) |
|---|---|---|
| Cloth points inside the body, over 1 / 3 mm | 6 / 6 (deepest 27.8 mm) | 56 / 44 (deepest 40.1 mm, the crew band in the neck) |
| Body points out through the cloth, over 3 mm | 3,022: left arm 1,653, right arm 1,234, trunk 135; deepest 39.9 mm | 299 (trunk 289, arms 10); deepest 39.5 mm |
| Neck hole | 177 x 99 mm, clear of the head (closest 2.6 mm, none inside) | 138 x 44 mm, none inside |
| Welt front / back (median per 15-degree sector) | 64.7 / 90.0 mm | 72.5 / 66.7 mm (Tom's own: 76.9 / 74.6 by this measure) |
| Cuffs left / right | 40.6 / 39.2 mm | 67.3 / 67.6 mm (Tom's own: 74.6 / 75.0) |
| Crew band | 25.2 mm | 30.7 mm (Tom's own: 29.2) |
| Gap to body, median chest / waist / hip | 27.9 / 32.0 / 8.3 mm | 11.6 / 30.9 / 28.1 mm |
| Skin | 90 bones, every point weighted, up to 21 bones per point; bends to itself at rest (0.0 mm) | not yet skinned at this step |
| Mesh | 19,480 triangles kept; points split along seams (10,383, welds back to the original 9,860); both materials kept; second UV set lost (one left) | unchanged |
- Pictures: F:/LedgerTools/tool-tests-2026-11/metatailor-test/measure/compare-metatailor-above-blender-below.jpg (preview production/previews/metatailor-test-2026-11-12.jpg), metatailor-neck-strip.jpg. Seen: the backs of both upper arms stand out of the sleeves; a torn flap stands up behind the neck and over the left shoulder with holes in it; the back hem hangs lower in a curve.
- MetaTailor's own view hid this: "Apply Visibility" hides the body under the clothes, so only dark strips on the upper arms showed in the app.

## Verdict
FAIL at its defaults on the refit's checks: body through the sleeves ten times the Blender carry's, cuffs squashed to about half, the back welt stretched, a torn flap at the back neck. Better only on cloth inside the body (6 against 56) and a neck hole clear of the head. The blouse step was not run (the method: only if the jumper alone fits).
- Clicks: 33 in all (20 on the path that worked; 8 lost to the body lying down; 5 looking at layers and Pose Match afterwards). Minutes: about 22 preparing, 11 in the app, 35 measuring and recording, against the Blender refit's 3.2 h for the whole chain (bands, cardigan cut, layers, skin), so not like for like.
- Free version: the viewport is stamped "noncommercial use only"; the Unreal, Unity and Character Creator exports are Pro; FBX, GLTF and GLB are free. Whether a free export may ship is unverified (terms unread); Pro would be needed for any game use.

## Not tried (try 2, listed)
- Pose Match: a manual mode where the body's joints are dragged by eye to the garment's pose (the panel offers it as "Redo Pose Match"). The arms leaving the sleeves at the back point to an arm-angle mismatch between Tom's and Sheila's poses that the automatic pose warp did not close. Dragging joints by screenshot is slow and imprecise and needs his PC idle; advisor 113 prefers tools driven without clicks. Not tried; Marvelous and the Blender chain stay the refit method.
- Its sculpt brushes (push/pull, shrinkwrap, relax) could mend the strips by hand, garment by garment: hand work, not a method that repeats.

## Unverified
- Which category took (Shirts or the default Jackets); MetaTailor's terms of service; whether 21 bones per point survives the engine's import limit.
