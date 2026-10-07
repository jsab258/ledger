# Why the street's sky light is far darker than the sky seen (from Unreal 5.8's own code)

Lab test 1, 7 October 2026. Read from the installed Unreal 5.8.2 (`C:\Program Files\Epic Games\UE_5.8`, Build.version: 5.8.2, changelist 56702186, branch ++UE5+Release-5.8), the exact version the game runs, because the GitHub clone was refused (see NOTES.md). Paths below are relative to `Engine\`. D = read in the code; I = inference. The game's side is read from the lab branch at 39ae711a (`ue-probe/...`, `production/specs/unreal-look.json` in the builder's copy).

## The answer in five lines

1. By day the engine copies the dome into the sky light without loss: the real-time capture redraws the same sky-flagged dome with the same material, and the brightness scaling used to store it is undone before lighting (D, chain below).
2. The engine then multiplies that copy by the sky light's Intensity, and the game sets Intensity to sky_intensity 0.7 x sky_light_gain 0.58 = 0.41, while the dome itself is drawn at 0.7 x 13 = 9.1. So the street is lit by a sky 41% as bright as the one on screen, by the game's own numbers, not by an engine loss (D for the multiply; the numbers are the game's).
3. On top of that come three ordinary losses that make walls and faces look far darker than the sky: a wall or face sees at most half the sky; the default sky light makes everything below the horizon black; and Lumen blocks the sky by the street's own buildings (D for the defaults and Lumen's miss rule; I for the size).
4. Then the surface's own colour: brick reflects about 12 to 26% (the builder's own note), so even with a perfect sky light a sideways brick wall in a street sits roughly 10 to 30 times darker than the sky (I, arithmetic below). That part is physics and is what the reference sheet shows.
5. So the fix the code supports is the builder's own "one sky" option: sky light Intensity 1.0 (sky_light_gain about 1.43 at sky_intensity 0.7) so the light equals the dome, and the brick brought back to real albedo; plus a ground-coloured lower hemisphere for rays that leave the street (I).

## The chain, dome pixel to wall pixel

| Step | What the code does | Where |
|---|---|---|
| Game sets up the sky light | Captured Scene, real-time capture, intensity written per condition as SkyIntensity x SkyLightGain | `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:2961-2963`, `:3669-3670` |
| Game sets the dome's brightness | dome emissive = SkyIntensity x 1.0 x SkySeenGain (13 by day, 0.15 at night) | `VignetteShot.cpp:3411-3414`, `:444` |
| Capture draws only the sky-flagged meshes | "If there are any mesh tagged as IsSky then we render them only, otherwise we simply render the sky atmosphere itself." | `Source/Runtime/Renderer/Private/ReflectionEnvironmentRealTimeCapture.cpp:743-746` (D) |
| Each primitive is in the capture by default | `bVisibleInRealTimeSkyCaptures = true;` | `Source/Runtime/Engine/Private/Components/PrimitiveComponent.cpp:364` (D) |
| Capture stores the dome at a fixed scale | sky materials use `RealTimeReflectionCapturePreExposure` in the capture; it is `1 / 2^r.EyeAdaptation.CachedLightingPreExposure` (default 4 EV) | `Shaders/Private/BasePassPixelShader.usf:2482-2484`; `Source/Runtime/Renderer/Private/SceneRendering.cpp:2076`; `PostProcess/PostProcessEyeAdaptation.cpp:201-203, 240-243` (D) |
| That scale is undone for lighting | `SkyPreExposureInv = 1.0f / EyeAdaptation::GetCachedLightingPreExposure();` then `SkyLightColor = ... GetEffectiveLightColor() * SkyPreExposureInv * SkylightScale` | `SceneRendering.cpp:2091-2101` (D) |
| Intensity multiplies the copy | `LightColor(FLinearColor(InLightComponent->LightColor) * InLightComponent->Intensity)`; effective colour also x `r.SkylightIntensityMultiplier` (default 1) | `Source/Runtime/Engine/Private/Components/SkyLightComponent.cpp:274, 231-234, 85-88` (D) |
| Height fog in the capture | the capture adds height fog by the dome's depth, through the same fog function as the screen, so the day's 900 m fog cut-off leaves the 1,000 m dome unfogged in both; at night the cut-off is 0, so the dome is fogged in both alike | `ReflectionEnvironmentRealTimeCapture.cpp:913-958`; `Shaders/Private/ReflectionEnvironmentShaders.usf:1041-1072`; `Shaders/Private/HeightFogCommon.ush:397-401`; game: `VignetteShot.cpp:3603` (D) |
| Below the horizon is black | default `bLowerHemisphereIsBlack = true;` `LowerHemisphereColor = FLinearColor::Black;` becomes the proxy's `bLowerHemisphereIsSolidColor`; the capture then paints every downward direction that colour | `SkyLightComponent.cpp:313, 321, 267`; `ReflectionEnvironmentRealTimeCapture.cpp:978-990`; `ReflectionEnvironmentShaders.usf:445-452` (D). The game never sets it (`VignetteShot.cpp:3866-3870` says so). |
| Lumen: a ray that hits nothing takes the sky light | `TraceResult.Lighting += GetSkyLightReflection(ConeDirection, Roughness, ...) * TraceResult.Transparency;` and that function returns the cube x `View.SkyLightColor` | `Shaders/Private/Lumen/LumenTracingCommon.ush:50-61`; `Shaders/Private/ReflectionEnvironmentShared.ush:43-50` (D) |
| Lumen: a ray that hits a wall or the road takes that surface's light | so a wall's lower half of view returns the dark wet road, and the upper half is cut by the opposite terrace | `Shaders/Private/Lumen/LumenScreenProbeTracing.usf:655-668, 845-858` (D for the rule, I for the street) |
| No fog on the GI rays | `r.Lumen.HeightFogOnGI` default 0 | `Source/Runtime/Renderer/Private/Lumen/LumenTracingUtils.cpp:30-35` (D) |
| Ray brightness clamp | rays are clamped at MaxRayIntensity in pre-exposed units; the sky (about 3.7 before exposure) is far under it at the street's exposure | `LumenTracingCommon.ush:102-110` (D; the size I) |

The game runs software Lumen for light and reflections (`ue-probe/Config/DefaultEngine.ini:46-47, 58`).

## The arithmetic (I)

- Sky on screen by day: 0.7 x 13 = 9.1. Sky that lights: 9.1 x 0.406 = 3.7, so 41%.
- A brick wall facing across the street: it sees at most half the sky; with the opposite terrace (about 8 m high, 10 to 12 m away) taking most of the upper part from the ground floor, perhaps a quarter to a third of its view is sky. Albedo 0.12 to 0.26. Wall brightness about 0.41 x 0.3 x 0.2, roughly 2.5% of the sky seen: forty times darker. With a sky light equal to the dome, about 6%: sixteen times darker; the builder's note puts the reference sheet's sky-to-wall at about 7x, which the brick's ×2.7 gain was standing in for.
- A face in passing (Sheila outside a conversation) is the same case: upright, half its view the dark wet road, the other half partly the opposite terrace, then x 0.41. That is why "a face seen in passing is underlit" (FINDINGS) follows from the same numbers.

## What the code says to do (I)

1. Sky light Intensity = 1/0.7 of today's per-condition value (sky_light_gain 0.58 -> about 1.43), so the light equals the dome; then real albedos for brick and paint, as the builder's "one sky" option already proposes (production/research/aaa-street/WINDOWS-OTHER-DIRECTION-2026-10-04.md).
2. Set the sky light's lower hemisphere to the ground's colour (LowerHemisphereColor, or the flag off), so rays that leave the street downward, past the south end over the quay, do not return black.
3. Keep the night as it is in this respect: the dome and the capture are fogged alike there.
4. Measure before tuning: a grey card and a chrome ball in the hook frame (P20) give the wall-to-sky ratio directly.

## Not settled from code

- Lumen's real sky visibility in Quay Street (depends on the geometry and the distance fields); a frame must measure it.
- The auto-exposure's actual value per frame, and whether `r.EyeAdaptation.CachedLightingPreExposure` (default 4) ever clips: the engine warns on screen when exposure leaves roughly -8 to +12 EV (`PostProcess/PostProcessEyeAdaptation.cpp:245-279`); not seen in the game's logs here.
- The GitHub source was not reached; this rests on the installed 5.8.2 files only.

Files opened: the ones cited above, plus `Source/Runtime/Renderer/Private/PrimitiveSceneInfo.cpp`, `RendererScene.cpp`, `IndirectLightRendering.cpp`, `Lumen/Lumen.cpp`.
