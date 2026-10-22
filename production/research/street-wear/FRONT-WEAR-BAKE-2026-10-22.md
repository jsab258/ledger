# A cloud shopfront worn at the foot: research after try 1 (22 October 2026)

After Rita's front wear, try 1, failed its gate (production/audits/gate-ritas-front/GATE.md, 22 October). Read and measured on 22 October 2026.

D = read at the source in full; M = measured here; I = inference; U = unverified.

## The questions

1. Why did the street's own material draw her oxblood darker than the front's own material, in the same colour?
2. What is the professional method for wear on one unique piece (a hero front), rather than a kit?
3. Which Blender tools give that method without a person at the screen?
4. How does the glTF chain carry the result into the game, and does it keep the approved paint?
5. What should the foot look like?

## 1. The colour shift, measured

- **The capture is repeatable** (M). BEFORE and NEW of the across-the-road view, unchanged parts of the frame: brick, cream render, the fish shop's fascia and pilaster, the next shop's stallriser. They agree to 0.1% in linear light. The road agrees to 1.2%: its reflections hold her front. So the shift is in her paint, not the camera or the light.
- **The shift is larger than the gate record says** (M). Her pilasters lost 21% of red and 37 to 39% of green and blue; the cornice 20% and 33 to 34%. The gate record's 8 to 17% came from other patches.
- **It is mostly missing sky reflection** (M, I). Model each patch as albedo × k plus a grey reflection s. Before: k 0.89, s 0.028. New: k 0.81, s 0.010. So the street's material shows about a third of the glTF material's reflection, and about 10% less diffuse light.
- **Every setting matches** (M, read in the editor from the assets; scratchpad dump of 22 October):
  - both are Default Lit and opaque;
  - roughness 0.45 (her map 115/255);
  - specular 0.5: glTF IOR 1.5 at SpecularFactor 1 gives F0 0.04;
  - no normal map: the glTF's switch off, the street's default flat;
  - no AO in either.
- **Two suspects ruled out** (M):
  - the faces' winding: 14 of 31,584 oxblood triangles are wound backwards, none by area, and no node has a negative scale;
  - the camera's exposure: see the first point.
- **One difference is left.** The front's own instances are two-sided (glTF doubleSided); the street's material is one-sided. Why that would remove two thirds of the reflection is **not found** (U).
- **Conclusion.** The cause is not isolated. Any method that swaps her paint's material carries an unknown colour risk. A method that keeps the glTF material, which passed four day views and five night views, does not.

## 2. The professional method for a unique piece

Adobe's Substance 3D Painter, the industry's texturing tool, makes wear as masks from maps baked from the model itself, then paints the result into the piece's own textures. All read 22 October.
- **Dirt generator** [1] (D): builds grime in crevices, along edges and on flat areas from **curvature and ambient occlusion**, with **position** and **world-space normal** maps required. Its output is a black-and-white mask, refined by a grunge texture (level, contrast, grunge amount and scale, triplanar projection so no UV seams show) and by further masks the artist layers on top.
- **Metal Edge Wear** [2] (D): wear on the parts most likely knocked: edges from curvature, kept out of recesses by **ambient occlusion masking**, broken by grunge.

The street's kit uses the other family of methods (material grime by height and noise; projected decals; production/research/street-wear/PAINTED-FRONTS-2026-10-07.md). Those suit many pieces sharing a material. A unique piece is baked (I).

## 3. The same maps in Blender (5.2, headless through bpy)

Read in the bundled 5.2 manual, 22 October.
- **Render baking** [3] (D):
  - Cycles bakes shaders to the active Image Texture node of each material, for "export to game engines";
  - an **Emit** bake records exactly what a shader computes;
  - a **margin** extends the edge pixels past each UV island, against seams under filtering and mip-mapping;
  - it needs a UV map.
- **Ambient Occlusion node** [4] (D): the occlusion of the hemisphere, "for example to add weathering effects to corners". **Inside** detects convex rather than concave shapes, so it finds the edges that chip. **Only Local** limits it to the object itself.
- **Bevel node** [5] (D): rounded normals at edges. It is costly, so the manual suggests it mainly for baking.
- **Position** (D): object coordinates are the front's own frame, z above the footway (production/cloud-week/kit/shop-windows/sw_ctx.py). So the foot band is a function of the model, not of where it stands.

## 4. Into the game

- **The exporter** (D, Blender 5.2 io_scene_gltf2):
  - a Principled base colour fed by an image becomes **baseColorTexture**;
  - a roughness fed by an image (through Separate Color) becomes **metallicRoughnessTexture**: pbr_metallic_roughness.py, `__gather_metallic_roughness_texture`;
  - PNG is kept as PNG (`export_image_format` AUTO).
- **The import** (M, the editor's own record of her paints): each paint is a MaterialInstanceConstant of Interchange's MI_Default_Opaque_DS. Its texture switches (bHasBaseColorTexture and others) are off while the glb carries no texture. With a texture, the same master draws texture × factor (U until measured).
- **Colour fidelity** (I): an 8-bit sRGB texel of her oxblood returns within 0.5% in linear light. Block compression can move a flat colour. Measure the clean paint above the band against BEFORE; if it moves, raise the texture's compression to BC7.

## 5. The target

- **The front's own design** (production/cloud-week/kit/shop-windows NOTES.md, PC-05, and REVIEW-v2-close.md, narrow 9: W1, from its dated photograph):
  - foot grime to 150 mm along the whole front, 20% darker;
  - a band 150 mm round the door lever, 10% darker;
  - chipped edges on the shop door's bottom and lock rails and on the sill's nose.
- **Try 1's reviewers**, on what real door feet look like: warm, darker, damp-edged. Pale dust on cream reads as frost.
- **So the grime darkens and warms.** It never lightens a pale paint.

## Method chosen (try 2)

A recipe bakes Rita's front's wear into a texture for her three paints. It writes a second copy of the front ("ritas-front-worn"); the shop file names which copy the game stands, so it is reversible in data.
- **The mask**, in the front's frame, from: height (the foot band, ragged by a 3D noise); ambient occlusion (dirt in corners near the foot); ledges facing up (light dust); convex edges by inside-occlusion (chips, only in W1's regions); distance from the lever (the hand band).
- **The colour**: the paint darkened toward a warm grime, roughness toward matt.
- **The output**: one texture set per paint (colour and roughness), over a new unwrap of that paint's faces alone, its unused ground filled with the clean paint; every other material is left as it was.
  - **Why one set per paint, measured at the gate:** a first build put all three paints in one 4096 atlas on a black ground. Narrow faces seen at a slant read the picture's smaller copies (mip levels), where the black bled in as hairlines along the mouldings (square view, 22 October). It also matches the industry's tool: Substance Painter's Texture Set List lists a model's materials, each texture set tied to one material [7] (D). That one material always gets exactly one set is not stated there (U).

The method is in the recipe; the numbers live in a spec beside the front's glass record.

**Acceptance:**
- **The approved paint is unchanged.** Patches above 0.6 m and away from the lever are within 1.5% of BEFORE in linear light, same camera.
- **The foot is darker, not lighter.** The bottom 150 mm is 15 to 30% darker on average. No band pixel on cream or buttermilk is more than 2% lighter than the clean paint above it.
- **W1's band and chips** are visible in the square and left views.
- **Then the gate.** One fresh reviewer a view: across, left, square and right by day, and the hook by day. Night views are checked for no change.

## Unreached

- Adobe's generators overview page (helpx.adobe.com/substance-3d-painter/features/effects/generators.html): HTTP 403. Its Experience League pages [1][2] were read instead.

## Sources

1. Adobe, Dirt generator, Substance 3D Painter docs, https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/effects/generators/dirt, read 22 Oct 2026. D
2. Adobe, Metal Edge Wear, Substance 3D Painter docs, https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/effects/generators/metal-edge-wear, read 22 Oct 2026. D
3. Blender 5.2 manual, render/cycles/baking.rst (bundled with the Blender MCP, F:/LedgerTools/blender_mcp/mcp/blmcp/data/manual), read 22 Oct 2026. D
4. The same manual, render/shader_nodes/input/ao.rst. D
5. The same manual, render/shader_nodes/input/bevel.rst. D
6. Blender 5.2 io_scene_gltf2, blender/exp/material/pbr_metallic_roughness.py lines 200 to 250, and __init__.py lines 353 to 375. D
7. Adobe, Texture Set List, Substance 3D Painter docs, https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/interface/texture-set/texture-set-list, read 22 Oct 2026. D
