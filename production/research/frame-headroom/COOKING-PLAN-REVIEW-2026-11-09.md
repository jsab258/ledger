# Review of COOKING-PLAN-2026-11-09 (9 November 2026)

A fresh reviewer checked the plan against MEMORY-WHERE-2026-11-08 [MW], RUNTIME-PICTURES-2026-11-08 [RP], MEMORY-PLAN-2026-11-07 [MP], the code it names, the installed engine (UE 5.8.4, Build.version) and the 8 November memreport [MR] in F:/LedgerTools/tmp/memwhere-2026-11-08. Read-only. Nothing was run but Python readers over files on disk. Read 9 November.

## Verdict: pass with fixes

The diagnosis, the order and the sizes hold. Every MB figure was recomputed and is right. The fixes below are about how the import is set up and how it is checked. Fixes 1 to 4 must be made before step 3 or step 1 is built. Without them, part of the saving would be lost, or the check would pass while normals stayed uncompressed.

## What was checked and holds

- **Arithmetic.** All rows were recomputed with BC1 at 0.5, BC5 and BC7 at 1 byte a pixel, and x 4/3 for mips:
  - A1 112-224 kept / 406-518 saved; A2 213-267 / 693-747; A3 21-43 / 85-107; A4 32-40 / 41-49; A5 10.7-13.3 / 35-37; A6 2.7-5.3 / 17-20; A7 82.5 by subtraction (1,952 less 1,869.5), 55-69 saved.
  - B1 38.7 / 48.0 kept, 248-257 saved. B2 62.4 MB (summed from [MR] 2938-3022: the /Game/Ledger rows 263.9 less the fascia rows 201.6), 41-52 saved.
  - The totals 1,621-1,856 and 2,065-2,315, and the step peaks 5,123-5,226, 4,605-4,820 and 4,296-4,531, all add up.
  - The pool's need, 642-876, also adds up: kept 455-689 plus 187.
  - 13,760 KB a fascia map is the padded size, 5504 x 640 x 4 (128-multiples, the [RP] s2 rule), so 22 rows give 295.6 MB.
- **Counts in [MR].** The 22 fascia rows at 1782-1803 are right (grocer has no orm; launderette and newsagent carry an emissive), and so are the 15 YES rows. Every /Game/Ledger row in the uncompressed list has a side that is not a multiple of 4 (all 65 checked).
- **C1, C2, C4.** The [MR] rows at 4366-4417 match the table. C2's 52 + 48 + 24 = 124 holds at 4 bytes a texel for R11G11B10 and 2 for R16.
- **Header and ini citations** were checked line by line and are all correct:
  - PixelFormat.h:451-455 and ITextureFormat.h:175-191;
  - TextureDefines.h 30-32, 127-174, 176-199, 393-404 and 561-573;
  - Texture.h 1322-1324, 1353-1355, 1393-1411, 1506-1508, 1542-1544 and 1609-1611;
  - StreamableRenderAsset.h:370 and Texture2D.h:341-342;
  - BaseScalability.ini 74-78, 377, 387, 424, 434 and 763-771;
  - BaseDeviceProfiles.ini 190-192, DefaultScalability.ini 27 and 37, DefaultGame.ini:45.
  - There is indeed no DefaultDeviceProfiles.ini.
- **Can run-time pictures be cooked?** Yes, with named exceptions. Every large row is a file decoded by ImportTexture (VignetteShot.cpp:6132-6195) and nothing else: no row's pixels are changed after decode. The only other CreateTransient calls are the 2x2 textures built in code (6255, 9837), which have nothing to cook. The crop is applied only on the vignette card-decal path (9514-9561). The 5650x460 street decals come through 7472, which has no crop.
- **Look risks** are named for every change, and every step has a packaged check.

## Fixes

1. **Correct the cause in section 0, and set compression on every role in step 3.** The name tables of the cooked assets (read with Python from ue-probe/Content/Ledger/ShopFronts/chandler-front-worn/.../Textures) show two settings:
   - the fascia colour and orm maps, and the label rows such as 21_est-1879_rgba, carry **TC_EditorIcon** and **TMGS_NoMipmaps**;
   - the normal carries TC_Normalmap;
   - the 4096 squares from the same glb carry TC_Default and TMGS_FromTextureGroup.

   So Interchange's non-power-of-two import set the 15 YES rows uncompressed on purpose. Only the 7 normals fell back to BGRA8 for want of 4x4 alignment. This also explains the list's YES/NO column: UTexture::IsUncompressed reads only CompressionSettings (Texture.h:2141-2144).

   Step 3 must therefore set CompressionSettings explicitly on every role. Base colour today names only "sRGB": it needs TC_Default, or TC_BC7 sRGB. MipGenSettings must be set to TMGS_FromTextureGroup explicitly. Resizing alone would leave all 15 uncompressed, and B1's saving would fall to about 94 MB. Emissive should be sRGB. Remove the "cause inferred" line from section 6.
2. **Step 3's check cannot see the normals.** `listtextures uncompressed` filters by setting, and it never listed the 7 BGRA8 normals. Check instead in `listtextures nonvt` that:
   - no /Game/Ledger row is PF_B8G8R8A8;
   - the resized fascia rows read 4096x512 with NumMips above 1 and Streaming YES.

   Apply the same test to /Game/Ledger/RuntimePictures in steps 1 and 2.
3. **Name the resize mode and sizes exactly.** Use PowerOfTwoMode = ResizeToSpecificResolution with ResizeDuringBuildX/Y set per picture: 4096x512 for the fascia boards, 4096x2048 for the cards, 2048x2048 for the scans, 4096x512 for the 5650x460 decals.
   - The header calls Stretch and Pad "nearest" (TextureDefines.h:186-193), but the code behind it (Texture.cpp) is not installed. If those modes round up, 5410x550 becomes 8192x1024 and 5650x460 becomes 8192x512, four and two times B1's and A6's figures (unverified either way).
   - For B2 and A7, give each row's target size and its direction (up or down), then recompute. 819x1024 up to 1024x1024 grows; 1150x640 down to 1024x512 shrinks.
4. **Choose compression from the sampler each texture is bound to.** Section 3's last bullet is wrong for the street's normals. make_base_material.py declares NormalMap as SAMPLER_NORMAL (lines 151 and 459-464), which is what TC_Normalmap derives (derived_sampler_type, 519-555). TC_BC7 linear would derive LINEAR_COLOR.
   - Use TC_Normalmap (BC5, the same 1 byte a pixel, so no MB change) wherever the sampler is NORMAL, and TC_Default with sRGB off for roughness (LINEAR_COLOR).
   - For the glb fronts' orm under Interchange's MI_Default_Opaque_DS, use TC_Default with sRGB off, not TC_Masks. The front's 4096 roughness from the same import cooks as TC_Default linear and works. TC_Masks derives a MASKS sampler, and the parent's sampler types were not reachable (the InterchangeAssets content was not found on disk).
   - The new import tool should call derived_sampler_type against each bound material's declared type and refuse a mismatch.
5. **Root the cooked textures, and keep the surface line's meaning.** A texture loaded on the new path is referenced only by a dynamic material instance. The code roots transients for exactly this reason (VignetteShot.cpp:6190-6195), so the loader must root the cooked asset or keep it in a referenced array, or it can be collected mid-walk and surfaces turn to their defaults. ImportTexture's OutW/OutH/OutLoadedAs today report the file's own size. Either keep that, or add a "cooked" word to the line, and update anything that reads it in the same commit.
6. **Make the file fallback visible.** A stale or missing cooked asset brings back the full cost without any fault showing. Do three things:
   - log one line for each picture still decoded from file;
   - have steps 1 and 2's checks count those lines (zero expected outside the crop decals and the 2x2 textures);
   - add a build check that every picture in the five lists has its cooked asset.
7. **Check the streaming of textures bound only by material instances.** The plan leaves this unverified, and it is the main look risk. In each step's memreport, read the Current/InMem size and the UnknownRef column of `listtextures` for the new assets. A texture held below its top mip while seen at the hook camera means blur. Judge that crop at full size beside the last good picture.
8. **The C7 setting's name is not in any installed 5.8.4 file.** Source, Shaders and Config were all searched; the name rests on the 5.8.2 .cpp read on 8 November. The packaged check must find `Set CVar [[r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim:8]]` in the game log (walk.log:405 shows the same form for DensityScale.Shadow), with no unknown-variable line. Add a look risk: too few pages for the grooms in view may drop hair occlusion or flicker (unverified mechanism). Look at the walk frames with the most people in view.
9. **C2's check names an ambiguous row.** Two rows are called Lumen.RadianceCache.FinalRadianceAtlas: 4368 at 4352x4352 and 72.25 MB, and 4379 at 2048x2048 and 21 MB (the second cache). Name the 4352 row, expected 2304x2304 and 20.25 MB. Also expect RadianceProbeAtlasTextureSource at 2048 (16 MB) and DepthProbeAtlasTexture at 2048 (8 MB).
10. **C1's wording.** "0.766 of 192.9 + 32.2 + 48" should read 0.234 of it. 0.766 is the share kept, the saving is 0.234. The figures themselves (63.9, or 78.9 with TraceRadianceAtlas) are right.
11. **Section 4's A6 line.** The 5650x460 cards are not cropped (7472). Cropping touches only the vignette decals at 9561, which sit in the unnamed buckets. Say which rows step 1 leaves on the file path, so that step 1's 926-1,029 is not over-counted.
12. **Step 2's night look.** There is no night walk ([MW] s0). Name the packaged night stand capture for the cards' banding check, with a full-size crop of a lit card beside the last good picture.
13. **The known-list removal in step 3.** asset_checks.py reads its size from blueprint_get_size_x (line 867). Whether that returns the built (resized) size or the source size is unverified. Remove the fascia rows from street-sweep-known.json only once the re-imported asset reads 4096x512 there. Otherwise the check fails on the source's 5410x550.
14. **A note on the cards (no figure change).** One material samples all three states (DayTex, LitTex and DarkTex, VignetteShot.cpp:8438-8446), so streaming keeps all three resident. [MW]'s "load only the shown state" would need that material changed, so it is not a pure code change. The plan rightly does not count it.

## Not reached

- Texture.cpp, ListTextures' code and the hair and Lumen .cpp files: not installed.
- The Interchange glTF parent material's sampler types: the asset was not found.
- Epic's page on texture compression settings by name.
