# Tom's pale crown: causes and a two-try plan (n09-7), 9 November 2026

Research only; nothing run or built. E: is C:/Program Files/Epic Games/UE_5.8/Engine (5.8.2). All web pages read 9 Nov 2026.

**Already spent on this fault (not repeated):** voxel shadow scale 1 and 0.5, deep shadow maps, scalp painted dark (DECISIONS 3 Nov 10:39, 11:41, 11:59); cards everywhere (HAIR-TEST-RESULT-2026-11-08.md); IntegrationType 1, on the near-dark fault (HAIR-NEAR-DARK-2026-11-07.md, 19:15). **Counting rule:** these would be tries five and six on one fault. The session decides whether order n09-7 ("Tom's crown", 6 h) is his yes, or asks him once.

## What the project draws

- Tom: BP_MH_TomL1, groom WI_Hair_S_Clean (short), Melanin 0.75, Redness 0.08, Roughness 0.55 (tools/ue/make_cast_metahumans.py 721, 756-762). Whiteness and Lightness are not set, and their built values are unread (unverified).
- At his camera his hair is strands (face level 0, office-look log of 3 Nov).
- DefaultEngine.ini:104 sets the voxel shadow scale to 0. Sky lighting is at the engine default, type 2 (ini 105-106). Lumen runs in software (ini 46, 58).
- There are no virtual shadow maps: the code default is 0 (VirtualShadowMapArray.cpp:160-162) and the project does not set it.
- **Measured (8 Nov), crown median grey:** street by day 28, office by day 115, office at night 124. The band is 79-99. The fault shows indoors only.

## Causes, most likely first

1. **Indoor sky and bounce light on the strands, with no hair blocking it (likely, about 55%).**
   - With Lumen and type 2, each strand takes one sample from Lumen's radiance cache (E:/Shaders/Private/HairStrands/HairStrandsEnvironmentLighting.usf 160-166, 755-780).
   - The sample uses `InitHairTransmittanceMask()`: a hair count of 0 and full visibility (HairStrandsDeepTransmittanceCommon.ush 13-19). So no hair shades any other hair from this light.
   - The only blocking check, `r.HairStrands.SkyLighting.ScreenTraceOcclusion`, is off by default (Source/Runtime/Renderer/Private/HairStrands/HairStrandsEnvironment.cpp 66-67, 393).
   - Epic staff (4 and 24 Feb 2026, UE 5.7.2): hair indoors near windows is too bright because strands sample Lumen probes and the surface cache, which leak. Epic has "no good solution" yet and advises sky lighting in open spaces only. https://forums.unrealengine.com/t/hair-indirect-skylighting-appears-too-bright/2709070
   - This fits the street-against-office split. In the 3 Nov picture the frosting sits on the top of the head, facing the lit ceiling (F:/LedgerTools/gate/work/hair-crown/scalp-paint-day/lit.png, by eye).
   - Not yet measured: what share of the 115 this light makes.
2. **The scalp takes direct light through the hair (likely in part, about 25%).**
   - At scale 0 the voxel pass writes nothing on surfaces. Scale 1 gave 79 against 140; the paint brought it to 111 (3 Nov).
   - Every lever inside the current shadow method is spent.
   - Mafia's method is untried: virtual shadow maps with `r.HairStrands.Voxelization=0` (F:/LedgerTools/aaa-study/mafia/config, DefaultEngine.ini:165, 222). It changes every shadow in the game, so it stays outside these tries.
3. **Thin short strands let the scalp show (possible, about 10%).**
   - Coverage, and the voxel count behind self-shadow, both scale with strand radius (HairStrandsVoxelRasterCompute.usf 727-730).
   - Epic, "Groom Strands" (5.8): Hair Width is the width in cm; Hair Root Scale is a factor at each root, fading to the tip. https://dev.epicgames.com/documentation/en-us/unreal-engine/groom-strands-in-unreal-engine
4. **White highlights from the tubes (possible, about 7%).**
   - The 3 Nov reviewer saw "the strands' own unshadowed highlights". Roughness is already 0.55.
   - A thread on Lumen backlight found no fix and named no cvar (UE 5.5.4 and 5.6.1). https://forums.unrealengine.com/t/reflected-indirect-light-on-metahuman-hair-groom-is-too-strong/2533751
5. **The hair material (unlikely, about 3%).**
   - In one thread a user lowered the "Hair Cards" multiply in MF_Hair_SaltAndPeper to 0.08, and the poster confirmed it worked. That fix is for cards; Tom draws strands here. https://forums.unrealengine.com/t/metahuman-white-hair-if-not-super-close/2660465
   - Epic's override page: Melanin runs from 0 (white) to 1 (black); Whiteness is the share of grey hairs; Lightness is the greys' brightness. Nothing on crowns or the scalp. https://dev.epicgames.com/documentation/metahuman/hair-overrides?lang=en-US
   - With 28 in the street, colour is unlikely to be the cause.

**Rejected:**
- Scatter Scene Lighting only adds light (HairStrandsEnvironment.cpp 34-35, 499-521).
- `r.HairStrands.SkyLighting 0` leaves hair "broken and very dark" (the 2709070 thread above).

## Step 0: a measurement, not a try (about 20 min)

- The packaged copy at High, `-OfficeLook` (by day) and `-OfficeLook -OfficeLookNight`, each run twice: as shipped, and with `-dpcvars=r.HairStrands.SkyLighting=0` (HairStrandsEnvironment.cpp:38).
- The crown measured by the hair-crown method (F:/LedgerTools/gate/work/hair-crown).
- If the crown with it off is at or under 99, cause 1 leads: Try 1. Otherwise: Try 2.

## Try 1: sky light blocked by the hair (type 0, "AdHoc")

- **The change:** `r.HairStrands.SkyLighting.IntegrationType=0` (HairStrandsEnvironment.cpp 63-64, 336-340). Screened first by `-dpcvars`; if it passes, one line in DefaultEngine.ini after line 106.
- **How it differs from 7 Nov's type 1:**
  - It reads the same cache, but scales each sample by the hair counted along the path in the voxels (usf 376-399, 497-516, 557-583).
  - That count uses the Environment scale, which falls back to the global 2 (HairStrandsVoxelization.cpp 45, 49), not the zeroed Shadow scale.
- **Evidence:** one user's report on 5.3, "problem solved"; no Epic reply. https://forums.unrealengine.com/t/any-new-ways-to-solve-the-groom-and-skylight-strangely-white-look-problem/1852498
- **Unverified:** the effect on the cast, noise, cost.
- **Measure:**
  - Tom's camera: office by day, office at night, street by day.
  - Darren, Sheila and Ron in the 7 Nov wide film (about 2.6 m), where type 1 failed.
  - A talk close-up.
  - The hair passes, from the CSV.
- **Bar:**
  - Crown 79-99 in the office by day and at night; street 28 ± 10.
  - No more crown pixels over 200 than as shipped.
  - The cast within about 10 sRGB levels of as shipped (the plan's screen, unsourced).
  - Hair passes within 1 ms for one person.
  - A fresh reviewer per view finds no new fault.

## Try 2: thicker roots, Tom only

- **The change:** at Tom's spawn, call `UGroomComponent::SetHairRootScale` on his hair component, beside the scalp paint (SliceCharacter.cpp ~707). The function is not editor-only (Plugins/Runtime/HairStrands/Source/HairStrandsCore/Private/GroomComponent.cpp 1786-1795).
- A switch `-TomHairRoot=X` screens 1.5, 2 and 3 in one build; the values are unsourced.
- It touches no one else and no light.
- **Measure:** the same views as Try 1, plus side-on walking (watching for clumps and a helmet look).
- **Bar:** as Try 1, plus no thick or clumped look at about 1 m.

If both fail, the crown stays a known fault. Mafia's virtual-shadow route goes to his page as a whole-game choice, with its cost measured first.

## Not reached or unverified

- No Epic groom page covers root and tip colour or a scalp showing through. Read and not covering it: "Groom Asset Editor", "Groom Materials", "Hair Rendering and Simulation".
- Unverified: Tom's built Whiteness; whether type 0 is noisy at 3.1 m; whether root scale holds when packaged; whether ScreenTraceOcclusion helps (it traces scene depth, not hair).
- Kingdom Come II's hair figures are unverified.
