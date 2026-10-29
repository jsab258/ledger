# How Lumen reflects the wet road's clear coat, 29 October 2026

All read 29 October 2026. (R) read in a primary source, (M) measured, (I) inferred. Engine paths under C:/Program Files/Epic Games/UE_5.8/Engine/.

## Questions

1. Which roughness does Lumen trace for a clear coat, by which methods, at what thresholds?
2. Does a ray meant for the sky see the dome, the sky light's cube or neither; can a distance limit return brick?
3. What do Epic's pages say?
4. Which fixes are used, and which are Epic's?
5. What do this PC's settings say?

## 1. Clear coat in Lumen

- One ray per pixel, sampled from GGX at the coat's roughness about the top normal: TopLayerRoughness is the coat's (Shaders/Private/Lumen/LumenMaterial.ush:677; ClearCoatCommon.ush:16-19; LumenReflections.usf:317-387) (R). At 0.03 it is in effect a mirror (I).
- Traced below Max Roughness To Trace, 0.4 by default (Source/Runtime/Engine/Private/Scene.cpp:658; LumenReflectionsCombine.ush:12-23) (R). The 0.6 stone is not traced; its rough specular comes from the screen probes (LumenScreenProbeTileClassication.ush:31; DiffuseIndirectComposite.usf:250-252) (R).
- Mix: traced × F + bottom × (1 − F), F = EnvBRDF(0.04, coat roughness, NoV) × coat (ClearCoatCommon.ush:59-74; ShadingModels.ush:407) (R). At 2.7° to 7.3° Schlick gives F 0.80 to 0.53 (M).
- Order: a screen trace on the depth buffer, thickness 0.005 of depth (LumenReflectionTracing.usf:73-225; LumenReflectionTracing.cpp:19, 54) (R); mesh distance fields for about 2 m, then the global distance field (technical details page) (R), to Max Trace Distance, 200 m (Scene.cpp:597; LumenDiffuseIndirect.cpp:228-231) (R); a linear "distant screen trace" past the Lumen scene, to 2 km (LumenReflectionTracing.cpp:138-157; .usf:808-841) (R); then the sky light (.usf:856-860) (R). The radiance cache is off for reflections, and only above roughness 0.2 (LumenReflections.cpp:52-70) (R).

## 2. The sky

- Software traces cannot hit the dome: Is Sky means no distance field (Source/Runtime/Engine/Private/StaticMeshSceneProxy.cpp:340) (R). A miss reads the sky light's cube at its sharpest mip (LumenTracingCommon.ush:50-62) (R); Epic staff: Lumen "falls back to the skylight on a miss" (forum t/2678227) (R).
- The project's sky light is captured scene, real time (ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:3058-3059); the dome is unlit, two-sided, is-sky (tools/ue/make_sky_material.py:100-102) (R). With an Is Sky mesh present the real-time capture renders those meshes only (Source/Runtime/Renderer/Private/ReflectionEnvironmentRealTimeCapture.cpp:745-746) (R): the cube is the photograph times the light's intensity, sky_intensity × 1.4286 (VignetteShot.cpp:3806; production/specs/unreal-look.json:21) (R).
- A distance limit does not turn sky into brick: a ray with no hit falls through to the sky (I). The end terrace (about 50 m) and the hill (110 to 200 m) lie inside 200 m and on screen, so rays aimed at them hit them (I).

## 3. Epic's pages

- Lumen GI and Reflections (https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine): clear coat supported "with some limitations", only the top layer smooth, one ray per pixel; "Lumen Reflections replace Screen Space Reflections" (R).
- Lumen Technical Details (https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine): screen traces first, then "a more reliable method"; Lumen Scene 200 m (up to 800 m), beyond it screen traces only; Far Field to 1 km needs HLOD1; hardware ray tracing "the only way to achieve high quality mirror reflections" (R).
- Sky Lights (https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-lights-in-unreal-engine): real-time capture takes the atmosphere, clouds, height fog and "Sky Dome Meshes with an unlit material tagged as IsSky" (R).
- No Epic page on wet roads was found (searched).

## 4. Fixes

| Fix | Source | Kind | Here |
|---|---|---|---|
| Is Sky dome, real-time sky light | Sky Lights page; forum t/2034552 | Epic and community | already in place (R) |
| Reflection capture | forum t/615633, snippet only | community, unverified | no effect: under Lumen GI the composite skips captures (IndirectLightRendering.cpp:2245) (R) |
| SSR instead of Lumen reflections | DiffuseIndirectComposite.usf:227-241 | engine option | screen only, sees the same far end (I) |
| Far field | technical details; LumenReflectionHardwareRayTracing.cpp:103 | Epic, hardware tracing only | what is mirrored lies inside 200 m (I) |
| Hit lighting | technical details | Epic | sharper, not more sky (I) |
| Grazing sky term in the material | none from Epic; the shop glass's cube term (unreal-look.json glass_cube_note) | own practice | artistic, unmeasured (I) |
| Rougher water lobe | none read today | method | reaches higher, toward sky (I) |

## 5. Settings on this PC

- ue-probe/Config/DefaultEngine.ini: r.DynamicGlobalIlluminationMethod=1, r.ReflectionMethod=1 (46-47); r.GenerateMeshDistanceFields=True (48); r.Lumen.HardwareRayTracing=0 (58); r.RayTracing.Enable=0 (62); no r.Substrate, so the legacy clear coat (Source/Runtime/RenderCore/Private/RenderUtils.cpp:2068-2072) (R).
- DefaultScalability.ini [ReflectionQuality@2]: r.Lumen.Reflections.Allow=1, DownsampleFactor=1, ScreenSpaceReconstruction.NumSamples=5 (7-17) (R).
- Unset (engine defaults): r.Lumen.Reflections.ScreenTraces 1, MaxRoughnessToTrace −1 (post process 0.4), RadianceCache 0, SmoothBias 0, DistantScreenTraces 1, r.LumenScene.FarField 0 (LumenScene.cpp:86), trace and scene distances 200 m (R).
- The dome: engine sphere 2,000 m across, no shadow (VignetteShot.cpp:414-415, 6486-6487) (R).

## Most likely cause

A flat mirror 3° to 8° below the horizon shows what stands 0° to 8° above it, same direction. The middle-road box (tools/wet_ground_check.py:37) lies 2.7° to 7.3° below the horizon (row 821 of 1440, from cam_hook's 3.4° upward pitch and 46° lens, production/specs/vignette-scene.json:794-798), 17 to 47 m out (M). In today's hook frame (production/previews/morning-hook-day-2026-10-29.jpg) the band above the horizon in those columns reads 137/117/108, nearest the horizon 126/99/87: the end terrace and the hill town; the sky above them 239/240/241 (M). Lumen mirrors what is there: the street's closed end, not a fallback, warms the far road (I). The sheet is a painting, not a measurement (I).

Checks before tuning, one frame each: r.Lumen.Reflections.Allow 0; r.Lumen.Reflections.ScreenTraces 0; r.Lumen.Reflections.VisualizeTraces 1 (Epic staff, t/2678227); the end terrace and hill hidden (I).

## Not reached

UE-358623, UE-350323 (403); Nguyenova, "Rendering Wet Roads in Driving Simulations" (CESCG 2021, too large); t/615633 and the Lumen feedback thread (snippets only); Lagarde not re-read; trial 2's frame (uncommitted) not measured.

Forums: https://forums.unrealengine.com/t/lumen-reflection-from-skydome-cuts-off/2034552 ; https://forums.unrealengine.com/t/lumen-reflections-break-when-the-normals-dont-match-the-pixel-depth-information/2678227 ; https://forums.unrealengine.com/t/how-can-i-increase-lumen-reflection-max-distance-on-water/615633

## Revised after review (29 October 2026, 22:50)

A fresh reviewer (LUMEN-COAT-REFLECTIONS-REVIEW-2026-10-29.md) passed this report with fixes; they stand here and win over the text above where they differ:
1. **What the far road mirrors.** The mapping "the same angle above the horizon" ignored the camera's 2.2 m height: the reflection sits about 4.4 m below the direct view, about 5 degrees at 50 m. So the middle-road box mirrors the far road, the footway and the terrace's ground floor (rows about 753 to 891, reading 110/88/78), not the hill town; the red pillar box shows reflected inside the box, and the corrected band predicts the road at about 90/71/63 against the measured 83/71/64.
2. **The angles** across the box's own columns: 2.5 to 7.2 degrees below the horizon, 17 to 50 m out.
3. **Not yet shown: "physically right" and "the sheet cannot be reproduced".** Untested: a broader water lobe (the coat at roughness 0.15 and 0.3, one frame each), the coat's real amount over the box (the water mask, while the Fresnel figures assumed a full coat), and the stone's own share (20 to 47% at full coat; the coat also cuts the stone's diffuse, ClearCoatCommon.ush:36). The sheet's own far road (170/170/172) is brighter than anything above its horizon (134/121/115), so the sheet is no flat mirror either: a lobe, haze or paint, untested.
4. **The Hook sheet is the mirror image of the game's frame**; tools/wet_ground_check.py's sheet values were read in the sheet's own boxes (sheetmeasure, 29 October: middle road 1440 to 1560 x 760 to 840, near road 1100 to 1300 x 980 to 1060 of its 2048x1088), which are the game's left-hand road once mirrored; that is now written beside the check.
