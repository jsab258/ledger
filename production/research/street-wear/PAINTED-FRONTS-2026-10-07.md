# Painted shopfronts worn without projection stretch (7 October 2026)

D = read at source; S = search summary; I = inference.

## 1. Methods and costs

- **Projected decals (today).** In 5.8 a decal fades only along its throw, never by angle [1] (D). A ledge along the throw gets one picture row smeared front to back: tonight's chip box (0.565 to 0.655 m) spans the 0.60 m sill top (I). Epic: they "shear and distort when not aligned" [5] (D). Vertex colour reads 1 in a decal [1] (D). Cost: screen coverage [4] (D).
- **Angle fade: not built in, buildable.** A DBuffer decal may read SceneTexture WorldNormal [2], there the face normal rebuilt from five depth loads [2] (D); Epic names facing-direction decals as its use [4] (D). Opacity × saturate((dot(N, decal −X) − 0.7)/0.2) drops ledges (I).
- **Mesh decals.** Wrap edges, no stretch, cheaper [5] (D); usable (no Nanite here), but geometry per mark (I).
- **Material grime by mask.** Vertex colour into a Lerp [6] (D); a height gradient broken by noise [7] (D); The Last of Us Part I layers leaks by vertex colour [8] (S); City Sample's grunge is procedural in the material [9] (S). Nothing projects, so nothing stretches; one sample, ~20 instructions, 4 bytes a vertex (I).

## 2. Recommendation: grime in M_LedgerSurface; decals only on brick, render, ground

Half exists: kit pieces carry baked occlusion (R) and edges (G) in COLOR_0, but terrace-front.py reads only POSITION (~3075) and exports no colour (~8277; the GLB's 788,810 vertices have none); M_LedgerSurface reads neither vertex colour nor world position (D).

1. Recipe: carry the kit's COLOR_0 to the export meshes; B = the piece's exposure (1 stallriser, plinth, door leaf; 0.4 frames; 0 fascia), constant per piece; other meshes R 1, G 0. Make it the active and render colour.
2. Export with `export_vertex_color="ACTIVE"`: the default drops colour a material does not use [10] (D).
3. Import unchanged: Interchange keeps vertex colours, stored sRGB-encoded [3] (D); tune ramps on a test strip (I).
4. make_base_material.py (names into SurfaceBind.h): VertexColor; WearNoise, a tiling grey, sampled by UV0 (metres on each face's own axis, ledges too); WearAmount (default 0, unchanged), GroundZ, BandHeight 0.45 m; the decals' dust and chip tints. Per pixel, times WearAmount:
   foot = saturate((B·(1−(Z−GroundZ)/BandHeight)^1.5 − 0.6·noise)·4);
   chips = saturate((G − 0.45 − 0.5·noise)·6);
   ledge = saturate((normal.z − 0.7)·3)·0.5·noise; crevice = (1−R)·noise.
   Paint to undercoat by chips, to dust by max(foot, ledge), darker by crevice, rougher under dust (I). Height is per pixel, so coarse box doors band correctly.
5. PaintStreet: WearAmount 1 on paint and tile rows; GroundZ = footway.
6. Drop frontage_wear's dust, scuff and chip; TakesMarks back to 3 October; angle fade in M_LedgerGrime as insurance.

## 3. Acceptance

Packaged PageShots, full size, day and night: pawnbroker-left-shop (door feet, sill), pawnbroker-right-shop (stallriser, plinth). cam_mickeys-day starts at the sill: Mickey's foot needs a frame (D, looked at).
- Same frame, WearAmount 0 against 1: change only below 0.45 m on stallrisers, plinths, doors, on arrises, and as mottle on ledges; frames, fascia, glass, brass under 1% (I).
- Ledges: no line front to back; variation along and across a sill within 2:1 (I).
- Bands strongest at the pavement on all five feet, ragged top, on the doors' bottom rails.
- Stallriser's bottom 0.15 m at least 8 L* off its top (I); chips on the sill nose; no light streaks at night.

Unreached: no shipped UE5 game's method at source (ArtStation 403; 80.lv [11] summary only).

## Sources (read 7 October 2026)

1. UE 5.8 Shaders/Private/DeferredDecal.usf ~166, ~185. D
2. MaterialTemplate.ush ~3403, ~812–836; DBufferNormalReprojection.ush ~44–86; PostProcessDeferredDecals.cpp ~54; HLSLMaterialTranslator.cpp ~8265. D
3. InterchangeGenericAssetsPipelineSharedSettings.h ~111; StaticMeshBuilder.cpp ~1708. D
4. Epic, Decal Materials, UE 5.8 docs. D
5. Epic, Using Mesh Decals, UE 5.8 docs. D
6. Epic, Texture Blended Material for Vertex Weights Painting, UE 5.8 docs. D
7. PaulaReb, Smart Height Dirt, Epic forums, 23 March 2026. D
8. J. Benainous, The Last of Us Part I materials, ArtStation. S
9. City Sample Buildings, Fab. S
10. Blender 5.2.2 glTF exporter: __init__.py ~553; primitive_extract.py ~533, ~576. D
11. Paulygonn, Advanced Vertex Painting in UE5, 80.lv, 3 April 2023. S
