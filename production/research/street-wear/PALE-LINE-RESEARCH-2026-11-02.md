# The pale line at contacts on the wet ground (2 November 2026)

For the one try allowed in the ground's material (SHOES-PLAN-2026-10-30.md, tries 2 and 3). **R** read in UE 5.8's source on this PC (Engine/Shaders/Private, Engine/Source/Runtime) or Epic's pages, all read 2 November 2026; **M** measured; **I** inferred. Substrate is off (RenderUtils.cpp 2068-2070), so the legacy clear coat applies.

## Questions

1. Which pass draws the line; how does the coat get its reflection; what occludes it at a contact?
2. Why a thin bright band at the contact?
3. What can the ground's material do, ranked?
4. Which settings act on it, as second options?

## 1. The pass (R)

- The line is the coat's reflection, added in the Lumen composite: the coat takes the traced reflection weighted by F = EnvBRDF(0.04, coat roughness, NoV) × coat; the bottom layer takes the screen probes' rough specular (ClearCoatCommon.ush 59-73; DiffuseIndirectComposite.usf 246-253).
- One ray per pixel, with the coat's roughness and top normal (LumenMaterial.ush 677; LumenReflections.usf 366-386). Epic: "a single reflection ray is cast per pixel" (https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine).
- **Nothing occludes it.** Short-range AO multiplies only the bottom's rough specular (DiffuseIndirectComposite.usf 650; comment at 333); screen-space AO is off under Lumen's gather (478-484); material AO multiplies only diffuse (LumenScreenProbeGather.usf 1444-1446).

## 2. Why a thin bright band (R, I)

- A screen-traced ray that goes behind a surface by over 0.5% of its depth is no hit (HZBTracing.ush 204-213; LumenReflectionTracing.cpp 54, 62; LumenReflectionTracing.usf 185-197). Epic: screen traces give up when "the ray passes behind a surface" (https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine).
- Just in front of a toe the reflected ray aims at the sole's underside, which the camera never sees. The fallback traces only static, instanced and landscape meshes (same page), so it takes the sky (LumenReflectionTracing.usf 846-860); the coat's 0.15 is under the radiance cache's 0.2 (LumenReflections.cpp 66-68). Farther out, rays meet the toe's visible front and the boot's dark reflection returns: a line, not a patch (I).
- The fallback starts 5 cm along the ray (LumenDiffuseIndirect.cpp 25; LumenReflectionTracing.cpp 1053; .usf 587-596, 720-728): a traced occluder nearer than that is passed by (I).
- **Try 3 re-read:** the stand-ins were never traced. The small-mesh cull reads the distance field's own bounds (DistanceFieldObjectManagement.cpp 439, 628-633), not BoundsScale; a half-sole cylinder's radius is near 8 cm against 30 (LumenMeshSDFCulling.usf 212-214; .cpp 25-27, 608). Drawn, they sat inside the sole, unseen by the screen too. So try 3 does not show the line "at any contact" (I).
- Today's hook picture (1600 px, M, weak): no pale line at the lamp post, bin, railings or shop base; pale reflections under the woman's heels. Skinned contacts, not static ones.
- The Fresnel (about 0.07 × coat at 60°, I) sets the line's strength, not its place.

## 3. Levers in the ground's material, ranked

1. **Cut the coat where the decal buffer marks a contact.** The DBuffer Texture node reads, per pixel, what decals laid (MaterialTemplate.ush 3511-3536; MaterialExpressionDBufferTexture.h 13-18). Re-lay M_LedgerContact (riding the sole joints, LedgerGarments.h LayContact) a few centimetres past the sole's outline; in M_LedgerGround, contact = saturate(DBufferC.r / 0.6) (contact decal roughness 0.6, puddles 0.02: make_contact_material.py 26, make_wet_material.py 31), ClearCoat × (1 − contact). Coat 0 removes the top reflection (ClearCoatCommon.ush 71-73); the stone's rough sheen stays, darkened by short-range AO. Most likely; about 3 hours. **Look:** a soft dull patch round each sole, like a contact shadow; puddles and street unchanged. **Test:** try 3's close-ups with and without; the band's peak no brighter than the floor beside it; the three gate views unchanged away from feet; frame time.
2. **The same cut from foot positions** in a Material Parameter Collection, only if the DBuffer read fails packaged; more code, fixed number of feet.
3. **One-lobe water** (Default Lit, Specular 0.25 × cover): its traced reflection is unoccluded too (DiffuseIndirectComposite.usf 227-243), but the held decal's Specular 0 would reach it (DBufferDecalShared.ush 525). Undoes a gated look; last.
4. **Coat roughness or strength everywhere:** dims the whole street (29 October: coat 0.3 darkened every region). Not recommended.

- **No effect:** material AO (§1); DistanceToNearestSurface (no skinned meshes; cells about 10 to 20 cm, LumenScene.cpp 69-77, I); a specular-occlusion input (none outside Substrate).
- **Epic's wet examples:** none found (forum threads only).

## 4. Settings, second options (R; costs unmeasured unless said)

- Lumen Scene Detail above 3.75 (post-process) brings the cull under the stand-ins' radius (LumenMeshSDFCulling.cpp 608): re-opens try 3; every small mesh traced; the 5 cm start remains.
- r.Lumen.Reflections.HierarchicalScreenTraces.RelativeDepthThickness and HistoryDepthTestRelativeThickness (0.005), raised: rays just behind the toe hit it. Free; false hits behind railings, posts, limbs, street-wide.
- r.Lumen.DiffuseIndirect.SurfaceBias (5), lowered: finds low static occluders; shared with GI, leaks risked; not skinned meshes.
- Hardware Lumen traces skinned meshes at "a large cost" (Epic); its scene alone cost 3.6 ms here (DefaultEngine.ini).
- Short-range AO settings: no effect on the coat.

## Not checked

- Which trace each pixel took (a shader define, LumenReflectionTracing.usf 212, 678, 879; the engine is not edited). Console checks first: r.Lumen.Reflections.SpecularScale 0 should remove the line; RelativeDepthThickness 0.05 should narrow it.
- The band at kerbs, walls and bins at full size; its width.
- That a ray starting inside a distance field hits at once (LumenSoftwareRayTracing.ush 185-226 reads so).
- The DBuffer read on a clear coat packaged; the patch's size; every cost.

## Checked before building (the session, 2 November)

- The raw decal buffer stores metallic, specular, roughness in r, g, b (DBufferDecalShared.ush 431-435), but the material's DBuffer Texture node returns DBufferC reordered as roughness, metallic, specular, one minus coverage (MaterialTemplate.ush 3524 and 3532; MaterialExpressionDBufferTexture.h: "R is Roughness"). So the node's **R** is right: contact = saturate(R / 0.6).
