# The hill: methods, assets, order (4 October 2026)

Research helper, about thirty minutes, reading only. Extends asset-plan/5-VEGETATION-AND-DISTANCE.md (its bands, kit and species are not repeated). Marks: **O** opened, **S** search summary, **I** inference.

## Three findings first

1. **The grey veil is the sky's, not the fog's.**
   - In the installed 5.8 source, `r.SupportSkyAtmosphereAffectsHeightFog` defaults to 1 and the fog's `SkyAtmosphereAmbientContributionColorScale` to white (O).
   - VignetteShot.cpp never sets the scale, and raises Mie tenfold, nearly isotropic (O).
   - So near-white sky light is added whatever the fog's colour, which fits unreal-look.json's "no longer govern the hill's veil" (I).
2. **Software Lumen stops at 200 m.**
   - "Lumen Scene only covers 200 meters", extendable "up to 800 m" with Lumen Scene View Distance; beyond it "only Screen Traces" (O, 7). Half the hill loses bounce light and goes flat (I).
   - Instanced foliage is in Lumen's surface cache "only if the mesh is using Nanite" (O, 7).
3. **Poly Haven has no British broadleaf** (O, API).
   - tree_small_02 is tagged *Burkea africana*; jacaranda is subtropical; the island trees name no species.
   - Broadleaves must be grown (Sapling with ambientCG leaves) and baked to impostors.

## Methods, ranked (cost on the RX 6700 at 3440×1440, unmeasured, I)

| # | Method | Evidence | Cost |
|---|---|---|---|
| 1 | **Own the fog colour**: sky contribution scale to black; colour from the concept; or an **Inscattering Color Cubemap** of the CC0 overcast sky, "to make distant, heavily fogged scene elements match the sky" | engine header O; 1 O | Already paid ("similar to two layers of constant density height fog", O) |
| 2 | **Local Fog Volumes over the crest**, so only the crest fades; fog cards as the alternative | 2, 3 O | "Similar to dynamic lights", tile-culled: about 0.1–0.3 ms |
| 3 | **Octahedral impostor trees** from the engine's Impostor Baker (Plugins/Experimental, off by default), upper hemisphere: "8 triangles with 9 vertices" against a billboard's 72; "three captured frames" blended; Fortnite bakes at 2048 | 4 O | Under 0.2 ms for a few hundred |
| 4 | **Leaf-card trees** (Sapling, 3–8k triangles) on the nearest tier only. A 10 m tree is 165–220 px tall at 125 m and 50–70 px at 400 m; a 12×12 frame at 2048 (about 170 px) suffices only past about 150 m | I | About 0.5 ms for 40 trees |
| 5 | **House modules** from the street kit, instanced, with its materials plus macro variation. Windows reflect the sky, with frames and nets. Past 250 m, HLOD Simplified (needs World Partition) or terrace-block impostors | 9 S; I | About 0.3–0.6 ms for 200 houses |
| 6 | **Local contrast in haze**: Ghost of Tsushima's bilateral-grid tonemapper, about 250 µs at 1080p on PS4. UE's Local Exposure splits "a base layer and a detail layer"; Detail Strength is the lever | 5, 6 O | Small |
| 7 | Nanite Foliage: "Experimental ... use caution when shipping" | 8 O | Not now |
| 8 | Volumetric fog: 1 ms on PS4 High, 3 ms on a GTX 970 Epic | 10 O | Too dear |
| 9 | Distance tint in materials (Firewatch) | S | Fights Lumen |

## Free assets

All are CC0. Neither licence page mentions AI (O, 11, 12).

| Asset | Use | Size |
|---|---|---|
| ambientCG **LeafSet027** (maple; sycamore is one) | Sycamore | 2K 11.7 MB |
| **LeafSet016** green oak / **LeafSet012** autumn oak | Oak | 12.2 / 8.3 MB |
| **LeafSet017**, **LeafSet029** | Ivy | 11.0 / 9.8 MB |
| **LeafSet025** garden, **LeafSet026** grass, **LeafSet019** needles | Hedges, lawns, conifers | 14.1 / 6.7 MB / — |
| Poly Haven **shrub_02** | Garden shrubs, LODs | 52k polys; glTF 0.76 MB + 1K maps 1.8 MB |
| **fern_02**, **grass_medium_02** | Banks, verges | 6k / 1.0M polys |
| **pine_tree_01**, **fir_tree_01** | Crest plantation, decimated and baked | 17.4M / 7.9M polys; pine .blend 571 MB: F: only |
| **island_tree_01/02/03** | Perhaps windswept crest scrub, by eye | 3.7M / 1.8M / 4.8M polys; 02: glTF 40.7 MB + 2K maps 79 MB |
| Avoid | tree_small_02, jacaranda, the Namaqualand set | — |
| **Sapling Tree Gen** 0.3.7 | GPL-3.0, "Blender 4.4 and newer" (O, 13); untested on our 5.2 | — |

## What to try, in order

1. **Fog colour (0 ms):**
   - set the sky contribution scale to black;
   - re-pick the colour from the concept's slope and crest;
   - measure saturation (target 26) and band contrast;
   - second try: the cubemap.
2. **Lumen Scene View Distance** to about 450 m; measure the cost.
3. **Two or three Local Fog Volumes** at the crest.
4. **Trees:**
   - a sycamore and an oak at three ages, from Sapling, as impostors; about 30 on the hill;
   - crest conifers from pine_tree_01 (space check first).
5. **Houses:**
   - the hill out of the 25 MB GLB, as instanced kit modules;
   - the distance window material;
   - stone retaining walls;
   - garden tiles (lawn, hedge, shrub_02).
6. **If the bands are still flat:** Detail Strength 1.1–1.3, watching for ringing.

**Budget:** about 0.5–1.2 ms of the 2.5 (I). Measure before and after each step.

## Unreached or unverified

- **Unreached:** shaderbits.com, the Medium impostor article, Project Hillside, the Tsushima streaming PDF.
- **Not watched:** the GDC Horizon and Tsushima talks.
- **Not found:** KCD2's method.
- **Not checked:** World Partition; any RX 6700 figure.

## Sources (4 October 2026)

Epic pages at dev.epicgames.com/documentation/en-us/unreal-engine/:

1. exponential-height-fog-in-unreal-engine
2. local-fog-volumes-in-unreal-engine
3. magnopus.com/blog/mastering-fog-four-levels-of-fog-in-unreal-engine (15 January 2025)
4. impostor-baker-plugin-in-unreal-engine
5. advances.realtimerendering.com/s2021/jpatry_advances2021/ (Patry, SIGGRAPH 2021)
6. auto-exposure-in-unreal-engine
7. lumen-technical-details-in-unreal-engine
8. nanite-foliage
9. documentation.simplygon.com/SimplygonSDK_10.3.500.0/ue5/concepts/hlod.html (S)
10. volumetric-fog-in-unreal-engine
11. api.polyhaven.com; polyhaven.com/license
12. ambientcg.com/api/v2/full_json; docs.ambientcg.com/license
13. extensions.blender.org/add-ons/sapling-tree-gen

Engine source: ExponentialHeightFogComponent, SkyAtmosphereRendering.
