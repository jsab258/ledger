# Upper windows and facades (research, 4 October 2026)

Extends asset-plan/1 and the shop-glass and shop-window notes. O opened, S search summary, I inference.

## Diagnosis (I, quay-street.json)

- Joinery albedo 0.82, brick luminance 0.12: frames should be 6.8x the wall; at 2.2x the sash gets a third of the wall's light. **Dim frames and dark reveals are one fault: an over-occluded recess.** Suspects: distance fields at 5 cm voxels, capped at 128 a side unless Distance Field Resolution Scale exceeds 1 [1 O]; short-range AO [1 O] on baked AO; reveal normals.
- Emissive net cards ignore shading: every pane one tone, the 8% reflection lost over them.
- Rubbed brick is the wall's hue at 1.3x value.

## Methods, ranked by fit, then cost

1. **Upper glass as one opaque Default Lit material.** Specular 1 (F0 0.08, both faces), roughness 0.02–0.05, so Lumen traces it (default limit 0.4 [2 O]); opaque keeps Nanite (Opaque and Masked only [3 O]). Base colour = lace × 0.65 over a dark room (0.03): nets lit by Lumen, shaded by the reveal. Emissive = the interior-mapped room (M_LedgerInterior's math) × (1 − Fresnel), near zero by day. A 0.5–1° normal tilt per pane ID, so panes catch different sky [4 S]; dirt roughens edges. Expected: sky atop near panes, eaves below, far panes mirrors by Fresnel (I). Cost: 2–3 samples, no extra pass (I).
   - Clear Coat (coat F0 0.04 [5 O]; Lumen's bottom layer "assumed to have a rough value" [2 O]) only if nets need their own roughness; dearer (I).
2. **Fallback reflection**: a mid-street cubemap, emissive × Fresnel; nearly free, frozen.
3. **Nets**: one lace sample; vertical gather folds as a brightness wave every 3–5 cm; scalloped hem. No parallax: a net 3 cm behind glass moves under a pixel at 10 m (I). By hash: none, half-net, full net, drawn curtains, venetian blind. Shaders lerp a curtain layer over the room [6 S]; so does SCS [7 O].
4. **White joinery**: albedo 0.75–0.82 (BS 4800 00 E 55 white, LRV about 88 [8 S]; whiteboard 0.87, paper 0.79–0.88 [9 O]); roughness 0.3–0.45; no gain above 1. Real 3–5 mm chamfers (free under Nanite) or baked trim bevels, so edges catch the sky; curvature and AO in vertex colour for corner dirt and flaking (I).
5. **Gauged arch**: red rubbers are "a soft, orange colour", joints "no more than 1 or 2 mm" [11 O], "bedded in pure lime putty, producing neat white radiating lines" [10 O]. Ring as its own mesh, UVs unrolled along the arc onto a voussoir strip: radial joints and per-voussoir tone follow (I). Orange, about 1.5x the wall's value, 10–15 mm proud so the extrados casts a line (I). Plainer houses: rough arches [10 O], by seed.
6. **Reveals**: brick wrapping with continuous UVs (closers in Flemish bond); DF Resolution Scale 2–4 on facade meshes (cap becomes 256) [1 O], checked in the distance-field and Lumen Scene views; sill top brightest, drip shadow below; soot, never black (I).
7. **Plinth, string course**: masonry-trim strips; engineering-brick or painted plinth 450–600 mm (I).
8. **POM**: near brick only; its loop cost "will not be easily trackable" [12 O].

**Costs**: front-layer translucency reflections "increase GPU cost" [2 O]; interior mapping 1–2 samples; planar reflection 1.7–23 ms (shop note); chamfers about 0 ms; DF scale 2 about 8x that mesh's DF memory (I).

## How studios build facades

City Sample: 24 kits, 2,000+ meshes [13 O]; windows by cubemaps, POM, interior mapping [13 S]. SanXia Street: two trims, masonry and joinery [14 O]. Godillon's London: "trim sheet material and vertex painting are doing all the heavy lifting" [15 O]. Hitman: material library, edge decals [16, 17 O].

## Free assets (CC0; APIs read today)

- **No lace** on either site: our own picture, or drawn.
- ambientCG: SurfaceImperfections003, smudges (2K JPG 19 MB); Smear007, wipes (2K 29 MB); Leaking decals under sills (4K JPG 5–22 MB); PaintedWood009C (2K 28 MB).
- Poly Haven: white_planks_clean, painted grain (1.8 m, 4K 7 MB); large_sandstone_blocks, sills and plinths (3 m, 4K 9 MB); church_bricks_03, rubber donor (1.2 m, 4K 9 MB); urban_street_01, London overcast HDRI for the fallback (4K 29 MB); modular_metal_gutter (glTF 2K 6 MB).

## Third try, in order (a few hours)

1. Lumen views on the hook frame; raise DF scale where reveals fill; remeasure.
2. Upper glass to method 1; drop the emissive net cards and upstairs translucent pane (shops keep theirs).
3. terrace-front.py writes pane IDs; tilt and dirt from them.
4. Arch ring: own mesh, arc UVs, voussoir strip drawn by the generator.
5. 3 mm chamfers on joinery, sills, arch.
6. stat gpu before and after; frames, glass and wall measured against the sheet.

**Needs the full kit**: baked-bevel trims, sash and door variants, the room atlas, house seeds, the cubemap.

## Unreached

KCD2, Division, Watch Dogs and Assassin's Creed Syndicate window methods; City Sample's window materials (doc silent). No frame cost measured.

## Sources

1 UE 5.8 source: DistanceFieldAtlas.cpp, LumenScreenProbeGather.cpp. 2 Lumen GI and Reflections doc; Scene.cpp. 3 Nanite doc. 4 Autodesk, Blender forums. 5 ClearCoatCommon.ush. 6 Fab shaders. 7 SCS blog, 2025. 8 e-paint.co.uk. 9 physicallybased.info. 10 Taylor, buildingconservation.com, 2003. 11 Shaw, localsurveyorsdirect.co.uk. 12 ParallaxOcclusionMapping.uasset. 13 CG Channel, 2022. 14 Chen, 80.lv, 2020. 15 Godillon, 80.lv, 2024. 16 Olsen, GDC 2021. 17 Carreras, 80.lv, 2019.
