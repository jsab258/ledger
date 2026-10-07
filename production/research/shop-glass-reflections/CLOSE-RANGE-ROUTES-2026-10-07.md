# Shop glass seen from two metres: the routes (7 October 2026)

**D** read at source (engine lines approximate; web pages via a helper today), **S** search summary, **I** inference.

## Why the cube fails up close

- At the hook camera a degree is 22 px, and 4.5 texels of a 512 cube: a texel spans about 5 px. Mirror-sharp needs about 2,500 a face (300 MB): clean is possible at 2 m, sharp is not (I).
- Nothing anti-aliases it: a Scene Colour HDR capture turns post-processing off before its views exist (SceneCaptureRendering.cpp ~748), so they get no anti-aliasing (SceneView.cpp ~1174-1178) and mip bias 0 (SceneVisibility.cpp ~5330-5351) (D [1]).
- A 75 mm brick course at 12.5 m is 1.5 texels at 512, past Nyquist: rings. At 1024 it is 3 texels (I).

## 1. What games and Epic do

- **Hardware ray tracing:** "the only way" to high-quality mirrors; RX 6000 qualifies (D [4]); Watch Dogs Legion's shop windows (D [12]). Here its scene alone cost 3.6 ms (D [2]).
- **Planar reflections:** Hitman 3's big windows, 007 First Light's mirrors (D [10, 11]). The scene renders twice (1.67 to 23 ms); the clip plane adds about 15% to every base pass (PS4; D [3, 9]). Thin Translucent glass takes them over Lumen's front layer (ForwardLightingCommon.ush ~553-564), only the scene's first (RendererScene.cpp ~3035), at ScreenPercentage (default 50) of the internal size (PlanarReflectionRendering.cpp ~456). Lumen never runs in their view (Lumen.cpp ~250-258) (D [1]): the terrace would return as dark as the unlit cube (I).
- **Lumen front layer** had all it needs: setting and toggle (D [7]), Allow=1 (0 at the engine's High) and opacity above 0 (FrontLayerTranslucency.cpp ~66-72, .usf ~182) (D [1, 2]). It traces the screen (the terrace is behind the camera), mesh distance fields for 1.8 m (LumenDiffuseIndirect.cpp ~24), then the coarse global field and surface cache (D [1, 4]): hence almost no street (I).
- **Screen-space reflections** see only the screen and yield to the front layer (ForwardLightingCommon.ush ~511) (D [1, 6]).
- **Cubes:** a flat mirror "will reveal the inaccuracies"; captures suit rough surfaces, whose prefiltered mips hide resolution; box shapes suit rectangular rooms (D [5]).

## 2. Anti-aliasing a 512 cube in 5.8

- **TSR inside the capture should run:** a Final Colour source keeps post-processing; cubes keep the TemporalAA flag (only 2D clears it, SceneCaptureComponent.cpp ~685); a persistent state makes the view real-time, so TSR runs jittered (SceneView.cpp ~1183-1195; SceneVisibility.cpp ~5249) (D [1, 8]). Its output carries exposure, bloom and grading (PostProcessTonemap.cpp ~251): neutralise them (I). The jitter cycle is 11 frames (SceneVisibility.cpp ~5255-5290): 24 passes. History: 40 to 100 MB while capturing (I).
- **Mips plus bias:** cube targets take bAutoGenerateMips (TextureRenderTargetCube.h ~54, D [1]), but magnified sampling stays on mip 0; a +1 bias gives a blurred 256 with fainter rings (I). Texture mip bias reaches it only globally (r.MipMapLODBias, SceneRendering.cpp ~1821, D [1]), blurring the main view too.
- **Additive compositing with rotation fails:** the cube path clears and copies each capture; composite mode reaches only 2D (SceneCaptureRendering.cpp ~1466, ~2076-2110) (D [1]).
- **Memory:** at 1024 the faces render as one 3072x2048 target, which the editor's scene textures keep (SceneTextures.cpp ~252-282, D [1]).

## 3. Recommendation, ranked

1. **TSR inside the 512 capture:** SCS_FinalColorHDR; Lumen and persistent state kept; after registering, TemporalAA and AntiAliasing flags on, Bloom, EyeAdaptation, LensFlares, Grain off; AutoExposureMethod Manual, bias 0, ApplyPhysicalCameraExposure off; bExcludeFromSceneTextureExtents on; 24 passes. **Accept** on the hook still by day, crops at 4x: the roofline a soft edge without regular steps; the reflected brick an even tone without rings; no seam at face edges; the cube dump's mean within 10% of today's; the game's peak during a catch at most 6.0 GB.
2. **Box projection:** meet the reflection ray with a plane at the opposite frontage before the lookup (I); accept if the reflected roofline matches the real one within 5 px from two spots 1 m apart.
3. **If 1 fails:** four 512 cubes a quarter texel apart (0.044 degrees, bCaptureRotation, lookup rotated back), averaged: four times the catch time, 38 MB more a window (I).
4. **One planar reflection**, if mirror sharpness is ordered (r.AllowGlobalClipPlane, ScreenPercentage 100): accept at 1.4 ms or less by night, the terrace within 30% of the main view's brightness.
5. **Hardware ray tracing:** no.

## Sources (read 7 October 2026; Epic pages 5.8, undated)

1. UE 5.8 engine source and BaseScalability.ini (local).
2. ue-probe/Config/DefaultEngine.ini, DefaultScalability.ini; CAPTURE-STEPS-2026-10-07.md.
3. Epic: https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine
4. Epic: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine
5. Epic: https://dev.epicgames.com/documentation/en-us/unreal-engine/reflections-captures-in-unreal-engine
6. Epic: https://dev.epicgames.com/documentation/en-us/unreal-engine/reflections-environment-in-unreal-engine
7. Epic: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
8. Forum, 14 Mar 2024: https://forums.unrealengine.com/t/anti-aliasing-with-scene-capture-2d/1752150
9. Forum, 4 Jun 2025: https://forums.unrealengine.com/t/topic/2593015
10. PCGH, Hitman 3, 1 Jun 2022: https://www.pcgameshardware.de/Hitman-3-Spiel-72804/Specials/Hitman-3-Raytracing-Nvidia-Geforce-AMD-Intel-Benchmarks-Review-1396024/
11. Aftermath, 007 First Light, 4 Jun 2026: https://aftermath.site/bond-007-first-light-mirrors-reflections-interview/
12. PCGamesN, 19 Aug 2019: https://www.pcgamesn.com/watch-dogs-legion/ray-tracing

## Tried the same evening (7 October, 20:05 to 20:50): set aside

The top recommendation, built and run three times in the editor's game mode with the cubes saved (-GlassCatchDump), Mickey's window (eg_bay0) against the afternoon's Scene Colour cube:
1. Final Colour, temporal anti-aliasing on, manual exposure 0, bloom, flares, grain, vignette and blur off, 24 passes: the roofline smooth and the brick's rings gone; a seam down the caught house where two faces meet; lit surfaces darker.
2. With the tone curve and local exposure also neutral: no change at all (the same medians to four places).
3. With the screen-space ambient occlusion and reflections also off: the seam gone; lit surfaces still dark.

Measured on the saved cube (median luminance, after against before): the sky 1.00, the house across the road 0.35, the road 0.39, the office 0.11. The sky is unlit and unchanged, so this is not an exposure scale: the Final Colour capture loses about two thirds of the light on the street's surfaces, which would empty the glass of the street again. Cause not found. By the two-tries rule the route is set aside, kept behind -GlassCatchAA (off by default). Next, if the glass is taken up again: the bExcludeFromSceneTextureExtents setting and Lumen's temporal history under jitter as suspects; then route 3 (four Scene Colour cubes rotated a quarter texel and averaged), which keeps today's light.
