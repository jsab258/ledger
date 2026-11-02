# Tom's hair shadow in Mickey's office (2 November 2026)

The fault, seen in the films F:/LedgerTools/tmp/ai-tester/film/2026-11-02-0900 (frames 20-26, 46-51) and 2026-11-02-0829: Tom's hair throws a hard, black, dotted shadow. It falls on the wall like a ponytail, and on his thigh, hand and chest, with no head or body shadow around it.

The engine's source was read on this PC on 2 November ("E:" is C:/Program Files/Epic Games/UE_5.8/Engine); nothing was run.

## 1. Which path draws the hair's shadow, and why hard, black and grainy

- **Strands, not cards.** Strands never enter a light's shadow map; only cards and meshes do (E:/Plugins/Runtime/HairStrands/Source/HairStrandsCore/Private/GroomComponent.cpp:1056-1057).
- **A separate screen pass.** With classic shadow maps, each shadowed light gets a screen pass after its own shadow (E:/Source/Runtime/Renderer/Private/ShadowRendering.cpp:2493-2505). The pass uses a deep shadow map only if the light has "Cast Deep Shadow". That setting is off by default: the constructor never sets it (LightComponent.cpp:432-452), and only the talk key sets it, under -TalkShadow (LedgerTalkLight.h:167). Otherwise the pass ray-marches the hair's voxels (HairStrandsTransmittance.cpp:943-944, 1023-1035). Voxels exist only for strands (GroomManager.cpp:1303-1306, 1329), so the hair is drawn as strands. This is inferred from the path; the groom's level-of-detail table was not read.
- **Hair alone.** The office's tubes and lamps cast shadows only from "cinematic" pieces (VignetteShot.cpp:7602-7606, 7819, 8307). The engine leaves every other piece out of their shadow maps (Renderer/Private/LightSceneInfo.cpp:502-505). The cast are marked cinematic (VignetteShot.cpp:2276-2281). Tom is not (SliceCharacter.cpp:652-735; the property's name is absent from BP_MH_TomL1.uasset), so his head and body throw nothing. The voxel pass checks neither that filter nor lighting channels (ShadowSetup.cpp:6484-6488; HairStrandsDeepShadowMask.usf:459-563). The hair therefore throws a shadow with no head around it, which reads as a ponytail.
- **Black.** The pass computes light = saturate(1 - hair count) (usf:544). The count is scaled by a density that defaults to 2 (HairStrandsVoxelization.cpp:39, 54; usf:527; HairStrandsVoxelPageTraversal.ush:265). One unit of hair removes the tube's light entirely, with no gradual falloff.
- **Grainy.** The voxels are point-sampled from a start jittered per pixel, meant to "converge with TAA without any denoiser" (usf:425-428, 437-455, 496); motion leaves the dots.
- **The office's raised shadow cap is not involved:** the voxel pass reads no shadow map, only the light's position (HairStrandsTransmittance.cpp:549).

## 2. What Epic and shipping games do

- **Epic's groom page** (https://dev.epicgames.com/documentation/en-us/unreal-engine/groom-scalability-and-performance-with-unreal-engine, read 2 November): "By default, all shadows cast by grooms are produced by their voxelization". Where a groom's shadow is unneeded, voxelization "can be disabled on the asset or the instance"; important lights "opt-in to cast Deep Opacity Shadow".
- **Not found:** an Epic MetaHuman page on hair shadows.
- **Mafia** (F:/LedgerTools/aaa-study/mafia/config, read 2 November) ships `r.HairStrands.Voxelization=0` (DefaultEngine.ini:222). It draws virtual shadow maps, which take strands directly. It also has its own hair-shadow setting, absent from stock Unreal (line 221), and casts hair shadows to half distance (DefaultGame.ini:666).
- **Kingdom Come II** uses hair cards, which cast as masked geometry (unverified).

## 3. The levers, the first to try first

1. **`r.HairStrands.Voxelization.DensityScale.Shadow 0`** in DefaultEngine.ini [SystemSettings].
   - It feeds only the hair's shadow on solid surfaces and hair in Lumen's reflections (usf:527; Lumen/LumenHairTracing.ush:98). The hair's self-shadow uses a separate scale (HairStrandsDeepTransmittanceMask.usf:322).
   - At 0 the count is 0 and nothing is written (usf:544, 558). This is certain from the source. Cost: none.
   - Also: hair darkens no skin or wall under any light, sun included (a fringe's shadow on a forehead is lost). 0.5 is lighter but still dotted. The office's raise-only switch cannot lower it (CrimeProbe.cpp:4598).
   - Test: at High, film the sit and the wall walk before and after, then a face in sun (-FaceAB).
2. **Mark Tom's worn MetaHuman and garments cinematic**, as the cast are (VignetteShot.cpp:2276-2281).
   - His head and body then shadow the office and the shop windows' light, and the hair's shadow merges into the head's. The dotted black rim at the hair's outline remains.
   - Cost: unmeasured. Tubes cast through six-sided maps (ShadowSetup.cpp:6434). Measure it as on 26 October.
3. **Cast Deep Shadow on the office's lights.**
   - A filtered shadow with transmittance (kernel 4, HairStrandsTransmittance.cpp:36-37) and no dots, and better hair self-shadow. Still hair-only.
   - Cost: a 2048 map per light (HairStrandsDeepShadow.cpp:13). The talk key measured 1.99 ms with its shadow.
4. **The groom's HairShadowDensity override** (GroomDesc.h:40-43). Lighter, but it scales every use of the voxels, so the hair's self-shadow and Lumen look lighten too.
5. **Voxelization off, or the groom's shadow off** (GroomManager.cpp:1309, 1329). This removes the shadow, but with classic maps the hair loses all self-shadow (HairStrandsTransmittance.cpp:783): the pale hair of 28 September. Mafia does it only with virtual shadow maps.
6. **Ruled out:** r.Shadow.MaxResolution, the light's radii and bias, contact shadows, and r.Shadow.Virtual.*.

## Not checked

The groom's per-level geometry type (binary asset); which office light throws the shadow; every lever untested, every cost unmeasured.
