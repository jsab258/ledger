# Review: how Lumen reflects the wet road's clear coat, 29 October 2026

Fresh reviewer, read-only; all read or measured 29 October 2026. Engine paths under C:/Program Files/Epic Games/UE_5.8/Engine/.

## 1. Engine citations: CONFIRMED

Nine checked:
- Traced roughness is the coat's: LumenMaterial.ush:677, via ClearCoatCommon.ush:16-19 (CustomData.y); GGX sampled at it (LumenReflections.usf:317-385).
- Max roughness to trace 0.4 (Scene.cpp:658; fade LumenReflectionsCombine.ush:12-16).
- Combine: `Bottom*(1-F) + Top*F`, F = EnvBRDF(0.04, coat roughness, NoV) × ClearCoat (ClearCoatCommon.ush:59-74); bottom from screen probes (DiffuseIndirectComposite.usf:248-252).
- No distance field for a sky material (StaticMeshSceneProxy.cpp:340).
- A miss reads the sky light at roughness 0, the sharpest mip (LumenReflectionTracing.usf:859; LumenTracingCommon.ush:50-58).
- Also LumenReflections.cpp:52-70, IndirectLightRendering.cpp:2245, ReflectionEnvironmentRealTimeCapture.cpp:745.

Missing: the base diffuse is also cut, by lerp(1, 1-F, ClearCoat) (ClearCoatCommon.ush:36).

## 2. Geometry: horizon CONFIRMED; angles and mapping CORRECTED

- Pitch -3.4°, 46° lens (vignette-scene.json:794-798): f 1696 px, horizon row 820.8 of 1440. Right.
- 2.7° to 7.3° is the centre column's. Across the box's columns (700-1000): 2.5° to 7.2°, 17 to 50 m; Schlick F 0.81 to 0.53 at full coat.
- In the frame (1600x900, scaled 0.625), above the horizon in those columns stand the end terrace, the parade's far end and the hill town (131/109/99 to 143/128/120; sky 239/239/241). Right.
- "The same angle above" holds only at infinity. The eye is 2.2 m above the mirror plane, so the reflection sits 4.4 m below the direct view, about 5° at 50 m. The rays reach the street's end 0 to 4 m up: they mirror the far road, the footway and the terrace's ground floor (rows about 753-891, 110/88/78), not the upper storey or the hill town.
  - The red pillar box is reflected inside the box.
  - At F about 0.65 and full coat this band predicts 90/71/63 against the measured 83/71/64; the report's band predicts 117/105/98.
  - "Not a fallback" stands; "hill town" is wrong.

## 3. Conclusion: PARTLY SUPPORTED

Supported: Lumen traces a flat 0.03 coat correctly. Exposure is ruled out (sky 239 against the sheet's 245; above-horizon band 143/128/120 against 134/121/115); fog at the far end is already matched (unreal-look.json fog_note).

NOT SUPPORTED, "physically right" and "cannot be reproduced":
- (a) Wet asphalt is no flat mirror. A broader lobe or tilted normals gather sky above the terrace; the report's own table leaves this unmeasured. On 2 October a 0.30 road read "satin and pale" (unreal-look.json wet_floor_note_2_october).
- (b) The coat amount is the water mask (tools/ue/make_base_material.py:4005, 4030), unmeasured; F assumes coat 1.
- (c) The stone shows through at (1 − F·coat), 20 to 47% at full coat.
- (d) The sheet's road box reads 170/170/172, brighter than anything above its horizon (134/121/115): no flat mirror either (lobe, haze or paint, untested).

Aside: the sheet mirrors the frame. Unmirrored, the box lands on Mickey's window (108/108/102). wet_ground_check.py does not name the box its 185/188/193 came from.

## 4. Settings: CONFIRMED

DefaultEngine.ini:46-48, 58, 62; no r.Substrate (default 0, RenderUtils.cpp:2068-2071). DefaultScalability.ini:10, 11, 14. Defaults: ScreenTraces 1 (LumenReflectionTracing.cpp:19), MaxRoughnessToTrace −1 (LumenReflections.cpp:109-110), DistantScreenTraces 1 (LumenReflectionTracing.cpp:138), FarField 0 (LumenScene.cpp:85-86), 200 m (Scene.cpp:592, 597). No runtime override in ue-probe/Source.

## Verdict: PASS WITH FIXES

1. Parallax-corrected mapping: far road, footway, the terrace's ground floor; drop "hill town".
2. Angles across the box's columns: 2.5° to 7.2°, 17 to 50 m.
3. Soften the sheet sentence: a flat 0.03 coat cannot give its far road; a broader lobe is untested (one frame each at coat roughness 0.15 and 0.3).
4. Check the coat amount over the box (ClearCoat buffer view) and the base colour's share.
5. Note the sheet is mirrored; name the middle-road target's box.
