# Review: STEP4-NEXT-PLAN-2026-11-12 (12 Nov 2026)

Fresh reviewer, read only. Engine root C:/Program Files/Epic Games/UE_5.8/Engine/Source; game code ue-probe/Source/LedgerProbe/Private.

## 1. Claims
- No compressor in a packaged game: **supported**. The reading cites UEBuildTarget.cs:5084-5089, ModuleDescriptor.cs:794-795 and Engine.Build.cs:404-433. Not re-read here.
- CreateTransient takes BC formats with ready-made blocks, sizes a multiple of 4, one mip: **supported**. Runtime/Engine/Private/Texture2D.cpp:1298-1354 sizes the buffer from GPixelFormats, refuses non-block sizes at 1304-1309, requires an exact byte count at 1320-1324, and adds one mip at 1336-1340.
- Non-power-of-two cooked textures never stream: **supported**, Texture.cpp:1858-1872.
- BC1 is 1/8 and BC7 is 1/4 of BGRA8, and 3.8 against 30.4 MB: **supported**, reading section 3.
- 7 shop pictures x 30 MB, about 180 MB saved: **supported**. RUNTIME-PICTURES section 3 gives 30.00 MB each (padded), and 7/8 of 210 MB is 184 MB.
- Steady 5,172 MB, peak 5,538 MB, budget about 4,870 MB: **unsupported by the two sources**. These come from the build's perf line, which neither source holds.
- "1.9 GB to 0.3-0.5 GB": **wrong as worded**. The plan itself says 420 MB has already been cut, so about 1.5 GB is left. About 430 MB in the 8 Nov dump has no owner (RUNTIME-PICTURES section 4). Some pictures do not pass through ImportTexture (LedgerPaper.cpp:70, which uses FImageUtils). Maps tagged _n and _r need BC5 and BC4, which the plan does not name.

## 2. Gaps in route A
- **The commandlet route costs more than stated.** The compressor is reached through ITextureFormatManagerModule and ITextureFormat::CompressImage (Developer/TextureFormat/Public/Interfaces/ITextureFormat.h:640), which is C++ only. Python cannot call it. That means a new C++ editor commandlet that fills in FTextureBuildSettings, not "no new tool". The plan's 60 lines do not cover it. texconv is the cheaper choice once its allowlist record is written.
- **Mips by hand are not needed for a first step.** The game makes one mip today (VignetteShot.cpp:6243), so one BC mip keeps the look unchanged apart from block artefacts. Leave mips out of the shop step. If added later, the mips below 2048x928 are not multiples of 4 and need block-rounded byte counts per mip. This is unverified.
- **Upload.** Hand the blocks to CreateTransient's ImageData argument. Do not use the Lock and Memcpy of BGRA at 6258-6265, which assumes 4 bytes per texel. The crop path (6266 onward) cannot work on blocks: pictures that are cropped must stay on PNG.
- **sRGB.** SRGB is set after CreateTransient (6253). With ImageData, UpdateResource already runs inside CreateTransient (1342-1345), before SRGB is set. Either pass no data and lock, or set SRGB and call UpdateResource again. Compress the colour files as sRGB.
- **Staging and git.** A BC1 shop file is 3.8 MB, over the 1 MB push guard. Write it to F:/LedgerTools/game-inputs, where stage_game_data.py:168-178 already reads, and add it to wanted(). Otherwise the packaged game does not have it.
- **Padding.** Pad 1855 to 1856 with a repeated row, and keep the UVs as they are.

## 3. First step
Shop pictures only, measured on the perf line, look compared at true size: sound and small. Two cheaper choices: texconv in place of the commandlet, and no mips. 184 MB does not close the 300 MB gap alone. State that the 16 MB scan and street maps come next.

## 4. Verdict
**Go with changes:**
1. Use texconv after its allowlist record, not the commandlet, or cost the commandlet as new C++.
2. Shop step without mips.
3. Upload through ImageData, then set SRGB and call UpdateResource again. PNG fallback for cropped pictures.
4. DDS files on game-inputs and in wanted().
5. Restate the gain from about 1.5 GB, and name BC5 and BC4 for _n and _r maps.
