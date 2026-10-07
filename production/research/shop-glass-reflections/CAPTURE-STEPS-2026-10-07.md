# The stair-stepped roofline in the caught glass (7 October 2026)

**The fault.** From the office camera, two metres from Mickey's window by day, the roofline of the single-storey terrace across the road comes back in the panes as large regular stair steps, about 0.7 degrees each (about 20 px at 2560 x 1440). His order of 7 October named it ("the ragged white strip").

**Tried and ruled out, by measurement (the two tries):**
1. The cube at 1024 a side instead of 256: the steps unchanged.
2. The capture's dynamic shadows off: unchanged.
With the caught reflection off, the live reflection shows the same roofline smooth. The glass material has no normal map.

**Research (a fresh agent, read-only, the UE 5.8 source and Epic's documentation):**
- Every scene capture runs without Lumen unless told otherwise: the cube capture's constructor sets its global illumination and reflections to none (Engine/Private/Components/SceneCaptureComponent.cpp, about lines 1319-1324; Renderer/Private/SceneCaptureRendering.cpp, about 799-801). Our capture never overrides its post-process settings.
- So the sky light in the capture is shaded by distance-field ambient occlusion. That runs whenever the GI method is not Lumen (DeferredShadingRenderer.h, about 474), with no temporal history in a cube capture (DistanceFieldLightingPost.cpp, about 306), and is not switched off by the dynamic-shadows flag (DistanceFieldAmbientOcclusion.cpp, about 1000-1006).
- Mesh distance fields are 5 cm voxels capped at 256 a side per mesh (DistanceFieldAtlas.cpp, about 69-80). The street's long merged meshes therefore get 12 to 16 cm voxels: about 0.6 to 0.75 degrees at 12 m, the measured step. Epic's guidance: break large meshes up for distance fields (https://dev.epicgames.com/documentation/en-us/unreal-engine/mesh-distance-fields-in-unreal-engine).
- The sky light's 128 px real-time cube (90/128 = 0.70 degrees) matches the angle too, but would need near-mirror surfaces to stay that crisp.
- Ruled out from source: internal resolution (forced to 100% in captures), mips (one), filter and format, and the reflection vector's precision.

**The professional fix:** light the capture as the main view is lit, with Lumen in its post-process settings, a persistent view state and several frames to converge. Too costly for fifteen windows on this card.

**The third and last try, 7 October 15:00:** distance-field AO off in the window captures. The steps unchanged; undone. **Set aside** by the two-tries rule, named in the day's summary. Directions left, for whoever takes it up: first the split test (export the 256 or 1024 cube with FImageUtils::ExportRenderTargetCubeAsHDR, ImageUtils.h about line 460: are the steps in the cube's own pixels, or made in sampling it?); then the sky light's real-time cube at 512 instead of 128; then Lumen in the captures (costly).
