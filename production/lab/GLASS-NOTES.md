# The shop glass's stair steps: the cause and the fix

Lab, 8 October 2026, from 11:22. For the builder. Code read on origin/wip at 73d61fae and in the installed UE 5.8.2. It builds on the builder's own research, production/research/shop-glass-reflections/CLOSE-RANGE-ROUTES-2026-10-07.md and CAPTURE-STEPS-2026-10-07.md. Every line below was opened in this session.

## In short

- **The steps are in the caught picture itself.** The window's cube is a Scene Colour capture. The engine gives such a capture no post-processing, so no anti-aliasing at all. At 512 a face, every edge of the house across the road is a staircase of hard texels, and the hero windows magnify each texel to about five pixels. Bilinear sampling softens a texel but cannot remove a step drawn into the texels.
- **1024 a face was clean,** by the builder's own test, but it pushed the card past 10 GB. That is the editor keeping its scene buffers at the cube's size, and the engine has a setting for exactly that.
- **The fix:** turn that setting on for every glass capture and catch the two hero windows at 1024. The light stays exactly as it is today, because it is still the Scene Colour capture.

## 1. Why the caught street is stair-stepped

1. **Our capture is Scene Colour.** ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:6851 sets `Cap->CaptureSource = ESceneCaptureSource::SCS_SceneColorHDR`. The anti-aliased Final Colour route is off unless `-GlassCatchAA` is given (:6881).
2. **The engine turns post-processing off for that source.** Engine/Source/Runtime/Renderer/Private/SceneCaptureRendering.cpp:747-751: for `CaptureSceneColor`, `ViewFamily.EngineShowFlags.PostProcessing = 0`.
3. **Without post-processing there is no anti-aliasing.** Engine/Source/Runtime/Engine/Private/SceneView.cpp:1174-1178: `bWillApplyTemporalAA = Family->EngineShowFlags.PostProcessing || bIsPlanarReflection`; if not, `AntiAliasingMethod = AAM_None`. So each cube face is rasterised once, with one sample a texel.
4. **The resolution is below the detail.**
   - The hero windows are caught at 512 a face (production/specs/unreal-look.json:101, glass_cube_hero_size; the rest at 256, :99).
   - At the hook camera a texel spans about 5 px, and a 75 mm brick course at 12.5 m is 1.5 texels: past the Nyquist limit, so it rings (CLOSE-RANGE-ROUTES, "Why the cube fails up close").
   - The roofline's aliasing steps are therefore five-pixel stairs on screen.
5. **The sampler cannot help.** VignetteShot.cpp:7024 samples the cube bilinear (`Rt->Filter = TF_Bilinear`), which blurs a block but keeps the step, because the step is in the data.

## 2. Why 1024 a face ran out of memory

- **The engine renders a cube capture's six faces into one tiled target** (SceneCaptureRendering.cpp:1912-1926, using the face offsets at :1632). Its size is the face size times the last offset plus one: 1536 × 1024 at 512, **3072 × 2048 at 1024**. That is larger than the street's own view of 2560 × 1440.
- **The editor sizes its scene textures to the largest view it has rendered, and keeps that.** Engine/Source/Runtime/Renderer/Private/SceneTextures.cpp:279-282 ("Grow": `max(LastExtent, DesiredFamilyExtent)`), recorded in its history at :303-309.
  - After one 1024 catch, every scene buffer of the main view (G-buffer, Lumen's, the post chain's) stays at 3072 × 2048, about 1.7 times the pixels, for the rest of the session.
  - The 10 GB the builder saw fits that.
- **The capture has a setting for this.** Engine/Source/Runtime/Engine/Classes/Components/SceneCaptureComponent.h:115-121, `bExcludeFromSceneTextureExtents`: "Setting this for a single-use capture will avoid influencing other scene texture extent decisions and avoid a possible ongoing increase in memory usage". The renderer then keeps the capture's request out of the history (SceneTextures.cpp:304-309, `bExcludeFromHistoryUpdate`).
- **Our code sets it only on the set-aside anti-aliased path** (VignetteShot.cpp:6917, inside `if (!bNoAA)`). The default Scene Colour capture never had it, so the 1024 test grew the editor's buffers.

## 3. The fix

**Step 1: two lines and one number.**
1. **VignetteShot.cpp:** move `Cap->bExcludeFromSceneTextureExtents = true;` from :6917 to before the `if (!bNoAA)` block (beside :6851), so every glass capture has it.
2. **production/specs/unreal-look.json:101:** set `glass_cube_hero_size` from 512 to 1024. That is the two hero windows only (:100, glass_cube_heroes); the rest stay at 256.
3. **Keep Scene Colour.** The capture's light stays exactly today's, and the anti-aliased route's lost two-thirds (below) never comes into it.

**Memory.** A 1024 face cube of half-floats is 48 MB, so 96 MB for the two windows. The tiled render target and its scene textures exist only while a window is being caught (twelve frames). Whether that transient peak stays within the card is the test's first number.

**Accept** (the builder's own acceptance for this item, CLOSE-RANGE-ROUTES §3.1):
- The hook still by day, cropped at 4×: the roofline a soft edge without regular steps, and the reflected brick an even tone without rings.
- No seam at the faces' edges.
- The cube dump's mean (`-GlassCatchDump`) within 10% of today's. It should be the same: same source, same light.
- The game's peak memory during a catch at most 6.0 GB.
- Memory back at its level before the catch once the round ends. This last one is new: it is what the setting buys.

**Step 2, only if 1024 is not clean enough:** the builder's route 3. Four Scene Colour cubes, a quarter texel apart in rotation, are averaged, which supersamples while keeping today's light.

## 4. The anti-aliased route's lost light: three suspects ruled out

The Final Colour capture came back with the sky unchanged but lit surfaces at a third. The code rules out three causes; none is needed for step 1.

1. **Pre-exposure.** Our capture turns EyeAdaptation off (VignetteShot.cpp:6934), so pre-exposure is not relevant (Engine/Source/Runtime/Renderer/Private/PostProcess/PostProcessEyeAdaptation.cpp:213-232) and stays at the 1 it starts from (:1528, :1539), as in the Scene Colour capture. In any case an exposure scale would have dimmed the sky too.
2. **One history shared by the six faces.** Each face has its own view state (Engine/Source/Runtime/Engine/Private/Components/SceneCaptureComponent.cpp:407-425; SceneCaptureRendering.cpp:754-755).
3. **Lumen's use of the last exposure.** It only scales lights set to blend inversely with exposure (Engine/Shaders/Private/Lumen/LumenSceneDirectLighting.ush:231; LumenSceneDirectLighting.cpp:1244).

Still open, as the builder named them: Lumen's temporal history under the jitter. A cube capture with post-processing also works out its own exposure from all six faces (SceneCaptureRendering.cpp, the comment after :775), worth a look if the route is ever taken up.
