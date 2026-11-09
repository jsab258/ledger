# Cooking plan for picture memory on the card (9 November 2026)

Order item n09-3. Read-only: nothing was run, built or edited apart from this note. Everything below was read 9 November 2026 unless dated otherwise. "MB" is MiB, as in the engine's dumps. "(inferred)" marks a computed figure, not a measured one; "unverified" marks a claim no source here confirms. Revised the same day on the fresh review, COOKING-PLAN-REVIEW-2026-11-09 [RV]; the fixes are listed at the end.

Inputs: MEMORY-PLAN-2026-11-07 [MP], MEMORY-WHERE-2026-11-08 [MW], RUNTIME-PICTURES-2026-11-08 [RP], study 12 [S12], and the 8 November capture itself: F:/LedgerTools/tmp/memwhere-2026-11-08, its memreport [MR] (Entry-Windows-11.08-21.26.18/Pid36548_...memreport) and walk.log [WL].

## 0. Corrections to the inputs

- **There are seven worn fronts, not six, and their boards hold 22 textures (295.6 MB), not 20 (268 MB).** The seven are chandler, grocer, ironmonger, launderette, newsagent, Rita's and the tea rooms. Each board's maps are 5410x550, B8G8R8A8, one mip, not streamed, 13,760 KB each (the padded 5504 x 640 x 4; [MR] lines 1782-1803). The memreport's "uncompressed" list names 15 of them (colour, orm and emissive), 201.6 MB. The 7 normal maps are also B8G8R8A8 but carry "NO" in that list's last column, so they add another 94.1 MB. The 268 MB figure is the list's whole B8G8R8A8 total over 85 textures ([MR] line 3024), not the fronts alone.
- **Where the maps are made.** They are not made in tools/. tools/art-recipes/front_wear.py makes the paints' square atlases (4096, 2048, roughness 1024; production/specs/shop-fronts/*-front-wear.json), and those cook correctly as DXT1 with 13 mips ([MR] lines 1806-1807). The 5410x550 maps are the fascia boards: production/cloud-week/kit/shop-windows/sw_front.py, fascia_maps (lines 1219-1263) and build_front (lines 1298-1303). They are drawn at 1 px a mm on a 5410 x 550 mm board (line 762), from the files under F:/LedgerTools/sw-scratch/shop-windows/<shop>/. The orm is the source file used as it is (line 1303).
- **Import settings.** The fronts come in through tools/ue/import_vehicles.py import_glb (lines 67-99), which import_shop_displays.py and import_shop_rooms.py share. It sets no texture property, so every glb picture keeps Interchange's defaults. The other texture tools set only sRGB and compression: import_front_joinery.py set_kind (98-103), import_garments.py (66-70), make_cloth_garment.py (113-114). import_glass_bake.py (142-145) and hidden_faces.py (336-338) set more. No tool sets power-of-two mode, texture group or streaming on.
- **Why the cooked check passed.** tools/ue/asset_checks.py line 208 finds "not a power of two each side", but production/asset-checks/street-sweep-known.json (lines 949-950, 985, 990, 1079-1085) lists the fascia boards as known, so the check passes them.
- **Why the boards cook uncompressed (corrected on [RV] fix 1).** The reviewer read the cooked assets' name tables (ue-probe/Content/Ledger/ShopFronts/chandler-front-worn/.../Textures, 9 Nov):
  - the fascia colour and orm maps, and label rows such as 21_est-1879_rgba, carry **TC_EditorIcon** and **TMGS_NoMipmaps**;
  - the fascia normal carries **TC_Normalmap**;
  - the 4096 squares from the same glb carry TC_Default and TMGS_FromTextureGroup.

  So the 15 "YES" rows are uncompressed by setting: TC_EditorIcon is the engine's "Uncompressed (RGBA8)" (TextureDefines.h:400), and UTexture::IsUncompressed reads only CompressionSettings (Texture.h:2141-2144), which is why the list's last column says YES for them and NO for the normals. Only the 7 normals fell back to BGRA8 for want of 4x4 alignment ("BCN DXTC formats require 4x4 alignment", PixelFormat.h:451-455; every /Game/Ledger row in the list has a side that is not a multiple of four, all 65 checked by [RV]). That Interchange's glTF import itself picks TC_EditorIcon and no mips for non-power-of-two pictures is inferred from this pattern; its code was not read (unverified).
- **Engine source.** The installed engine is now 5.8.4 (Engine/Build/Build.version). Its Runtime/Engine and Renderer folders hold headers only: AsyncTextureStreaming.cpp, HairStrandsVoxelization.cpp and Texture.cpp are not on disk. Citations below are the installed headers and ini files, read 9 November. [MW]'s .cpp lines were read 8 November in 5.8.2 and could not be re-read; they are marked "8 Nov, 5.8.2".

## 1. Holders of picture memory over 20 MB (8 November capture, peak 6,152 MB)

| # | Holder | MB | Source |
|---|---|---|---|
| A1 | Shop-room cards, 7 shops x 3 states, 4096x1855, decoded at run time | 630 | [MW] s6; [RP] s3; VignetteShot.cpp:8437-8447 |
| A2 | 2048x2048 run-time maps: street drawn and photo maps, scans, scalp; 24 of the 60 have no named owner | 960 | [RP] s3-4 |
| A3 | 8 MB run-time rows: 2048x1024, 2048x927, 1024x2048 (photos, decal cards, Mickey's room, sky) | 128 | [RP] s3 |
| A4 | 1536x1536 scan maps | 81 | [RP] s3 |
| A5 | 1024x1024 run-time maps | 48 | [RP] s3 |
| A6 | 5650x460 decal cards (not cropped: they load at VignetteShot.cpp:7472) | 22.5 | [RP] s3 |
| A7 | Smaller run-time pictures together (each under 4 MB) | 82.5 | by subtraction from 1,952 |
| B1 | Fascia boards of the seven worn fronts, cooked uncompressed | 295.6 | [MR] 1782-1803 |
| B2 | Other glb pictures cooked uncompressed (signs, labels, tiles, display cards): 50 rows | 62.4 | [MR] 2938-3022: the /Game/Ledger rows, 263.9, less the fascia rows, 201.6 ([RV]) |
| C1 | Lumen surface cache: three lighting atlases at 64.3, depth 32.2, albedo, normal and emissive at 16 each | 273 | [MR] 4369-4383 |
| C2 | Lumen radiance cache atlases | 195 | [MR] 4368, 4373, 4377, 4379, 4412, 4417 |
| C3 | Distance fields: brick texture 256, global page atlas 64 (plus a 112 MB buffer) | 320 | [MR] 4366, 4372; [WL] 2107-2108 |
| C4 | TSR history: colour 102, guide 26.3, metadata 21, moire 6.6 | 156 | [MR] 4367, 4378, 4380, 4410 |
| C5 | Whole-scene shadow map, 8192x2048 | 33 | [MR] 4375 |
| C6 | Glass cubes, BC6H, never streamed, six of them | 49.5 | [MR] 1817-1822; import_glass_bake.py:144 |
| C7 | Hair voxel page texture in the transient heap, at the walk's peak only | 343-392 | [MW] s2 (8 Nov, 5.8.2) |
| C8 | Transient heaps held above need | up to 384 | [MW] s4.3, low confidence |

Under 20 MB and free to take: the template's logo, T_GameAnimationSample_Logo, 18 MB ([WL] 2147).

## 2. How the savings were worked out

Bytes per pixel: B8G8R8A8 4; BC1 and BC4 0.5; BC3, BC5 and BC7 1. A full mip chain adds a third (x 4/3). Each cooked size counts every mip as resident, so the streamer can only make the saving larger. The run-time sizes are the dump's padded sizes ([RP] s2). Colour, normal and roughness are taken as a third each wherever a group is a set of three maps ([RP] s1: "3 maps (colour, _n, _r)", scans "3 maps per entry"; inferred). The low saving assumes BC7 for colour, the high one BC1. Normals are BC5 (TC_Normalmap) and roughness BC1 (TC_Default, sRGB off) in both; BC5 is the same 1 byte a pixel as the BC7 linear the first draft named, so no figure moved ([RV] fix 4).

| # | Change | Kept MB | Saving MB | Computation |
|---|---|---|---|---|
| A1 | Cooked at 4096x2048 (resized), mips, streamed; colour BC1, or BC7 if banding shows | 112-224 | **406-518** | 21 x 4096 x 2048 x 0.5 or 1 x 4/3 |
| A2 | Cooked, mips, streamed: colour BC1 or BC7, normals BC5, roughness BC1 linear | 213-267 | **693-747** | 60 x (2.67 + 5.33 + 2.67)/3, or with colour at 5.33 |
| A3 | Same; decals with alpha BC7 | 21-43 | **85-107** | 16 x 1.33 to 2.67 |
| A4 | Resized to 2048x2048 (1536 is not a power of two), same compression | 32-40 | **41-49** | 9 x 3.56 to 4.44 |
| A5 | Same as A2 at 1024 | 11-13 | **35-37** | 12 x 0.89 to 1.11 |
| A6 | Resized to 4096x512, BC1 or BC7 | 3-5 | **17-20** | 2 x 1.33 to 2.67 |
| A7 | Same, each at its nearest power of two each side | 14-28 | **55-69 (unverified)** | 82.5 x 1/6 to 1/3. The rows are not named yet ([RP] s4), so their targets and directions wait on step 0's log; resizing up shrinks the saving |
| B1 | Resized at build to 4096x512, mips, streamed; colour, orm and emissive BC1 (colour BC7 if letters suffer), normals BC5 | 39-48 | **248-257** | 15 x 1.33 + 7 x 2.67 = 38.7; with BC7 colour 48.0. Holds only if compression is set explicitly: resizing alone leaves the 15 on TC_EditorIcon and the saving falls to about 94 ([RV] fix 1) |
| B2 | Each row resized to the nearest power of two on each side (table below), BC1, or BC7 for the _rgba rows and wherever alpha or lettering needs it, mips | 8.9-16.7 | **45.7-53.5** | Nearest sizes total 200.75 x 65,536 px = 12.55 Mpx. Low kept: BC1, the 15 _rgba rows (13.75 x 65,536 px) at 1 byte, x 4/3 = 8.9. High kept: all at 1 byte, x 4/3 = 16.7 |
| C7 | `r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim` 14 to 8 (name unverified in 5.8.4, see section 3) | | **about 256 off the peak** | [MW] s4.2: requested 512 to about 190, two 128 MB heap steps fewer (8 Nov, 5.8.2) |
| C2 | `r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution` 32 to 16, Epic's own High | about 70 | **about 124 (inferred)** | FinalRadianceAtlas 4352² to 2304² (72.25 to 20.25, saves 52), RadianceProbeAtlasTextureSource 4096² to 2048² (64 to 16, 48), DepthProbeAtlasTexture 4096² to 2048² (32 to 8, 24); assumes 128 x 128 probes, each probe's resolution plus a 2-texel border, layout unverified |
| C1 | `r.LumenScene.SurfaceCache.AtlasSize` 4096 to 3584, Epic's own High | | **64-79 (inferred)** | 0.234 of 192.9 + 32.2 + 48 (the area kept is 0.766, the saving 0.234), plus TraceRadianceAtlas if it follows (unverified) |

**B2's targets, row by row ([MR] lines; nearest power of two on each side; "down" shrinks the picture, "up" grows it).** If a lettering row loses strokes at the gate, that row alone rounds up instead; rounding every row up would keep 38.8 MB and save only 23.6 (the worst case).

| [MR] lines | Pictures | Source | Target | Direction |
|---|---|---|---|---|
| 2953 | newsagent postcards | 1215x1120 | 1024x1024 | down |
| 2954-2955 | tile_chandler, tile_steam_laundry | 1243x1050 | 1024x1024 | down |
| 2957 | cleaner_labels | 819x1024 | 1024x1024 | up |
| 2958 | newsagent cards | 1150x640 | 1024x512 | down |
| 2959 | lobby_floor_grocer | 1006x630 | 1024x512 | up across, down in height |
| 2960-2965 | Rita's balls, colour and orm (6) | 817x409 | 1024x512 | up |
| 2966 | lobby_floor_steam_laundry | 1006x330 | 1024x256 | up across, down in height |
| 2967-2972 | launderette box faces a and b, colour, emissive, orm (6) | 620x450 | 512x512 | down across, up in height |
| 2973 | drivers_board | 512x597 | 512x512 | down |
| 2975, 2977 | detergents, pinboard | 512x398, 512x438 | 512x512 | up |
| 2976 | 08_jewellery_rgba | 907x168 | 1024x128 | up across, down in height |
| 2978-2981 | ironmonger hanging board faces, colour and orm (4) | 550x380 | 512x256 | down |
| 2982, 2984 | jar_labels, farebook | 512x341, 512x354 | 512x256 | down |
| 2983 | bottle_labels | 341x512 | 256x512 | down |
| 2985 | 13_service-washes_rgba | 1067x144 | 1024x128 | down |
| 2988, 2992, 2999 | price_cards, accounts, bookings | 512x171, 512x170, 512x153 | 512x128 | down |
| 2989-2991, 2993, 2995 | hours and loans signs (grocer, Rita's x2, ironmonger), 16_tobacconist--confectioner_rgba | 450-550 x 148-186 | 512x128 | mixed, down in height |
| 2994 | 90_hours-chandler_rgba | 374x186 | 256x128 | down |
| 2996 | message_pad | 210x296 | 256x256 | up across, down in height |
| 3000-3001, 3003 | est-1879, est-1884, 25_hours-newsagent (rgba) | 475-478 x 121, 414x124 | 512x128 | up |
| 3002, 3004 | hours_steam_laundry, hours_tea_rooms colour | 300x190 | 256x128 | down |
| 3005 | 22_13_rgba | 197x188 | 256x128 | up across, down in height |
| 3006, 3009, 3010 | 19_16, 14_9, 10_5 (rgba) | 161x188, 117x188, 114x191 | 128x128 | down |

Whether each _rgba row really holds alpha was not read from the files (unverified); the import step sets CompressionNoAlpha only where it does not.

Safe total, A plus B: **1,626-1,858 MB** (first draft 1,621-1,856; only B2 moved). With the three look-gated settings (C7, C2, C1), **2,070-2,317 MB**. The peak would fall from 6,152 to about 4,294-4,526 MB with A and B alone (inferred), if nothing else moves. Step 1's share is an upper bound: the crop decals it leaves on the file path sit inside A2 and A3's unnamed rows, and their share is not known until step 0 names them (unverified).

**The streaming pool.** Cooked pictures leave the never-streamed figure (NonStreamingMips, 2,459 in [MW] s2) and enter the streamed pool. That pool needed 187 MB of its 800 ([MW] s2). Adding all of A's and B's kept sizes (454-685) could bring the need to about 641-872 MB (inferred). Over 800, the streamer drops top mips, which saves memory but blurs pictures. Hence a guard step (step 4).

## 3. The settings, named as the installed 5.8.4 headers name them

Installed 5.8.4 headers and ini under C:/Program Files/Epic Games/UE_5.8/Engine, read 9 November. The Python names in brackets are the usual snake-case of each property; they were not checked against the editor's Python stubs (unverified).

- **Block alignment:** "BCN DXTC formats require 4x4 alignment" (Source/Runtime/Core/Public/PixelFormat.h:451-455).
- **Non-power-of-two never streams:** "NeverStream should set !bIsStreamingPossible" for non-power-of-two sizes (Developer/TextureFormat/Public/Interfaces/ITextureFormat.h:175-191).
- **Compression: UTexture::CompressionSettings, enum TextureCompressionSettings** (compression_settings; Texture.h:1512; values in Engine/Classes/Engine/TextureDefines.h:393-404):
  - TC_Default, "Default (BC1 or BC3 with A)" (393); TC_Normalmap, "Normalmap (BC5)" (394); TC_Masks, "Masks (no sRGB)", "Same compression as Default" (395);
  - TC_Grayscale, "If SRGB is set, becomes uncompressed RGBA8; prefer BC4" (396); TC_Alpha, "Alpha (no sRGB, BC4)" (401);
  - TC_EditorIcon, "Uncompressed (RGBA8)", "Very high memory use; prefer BC7 or Default instead" (400); TC_BC7, "BC7 Compressed (BC7)" (404).
  - UE::TextureDefines::IsUncompressed lists the uncompressed ones, TC_EditorIcon among them (561-573); UTexture::IsUncompressed reads only this setting (Texture.h:2141-2144).
- **sRGB:** UTexture::SRGB (srgb; Texture.h:1573).
- **Alpha dropped on compressed output:** CompressionNoAlpha (compression_no_alpha; Texture.h:1322-1324).
- **Resize at build:** PowerOfTwoMode, shown as "Padding and Resizing" (power_of_two_mode; Texture.h:1393-1395), enum ETexturePowerOfTwoSetting: None, PadToPowerOfTwo, PadToSquarePowerOfTwo, StretchToPowerOfTwo, StretchToSquarePowerOfTwo, ResizeToSpecificResolution (TextureDefines.h:176-199). With **ResizeToSpecificResolution**, ResizeDuringBuildX and ResizeDuringBuildY give the size, zero keeping the source's (resize_during_build_x/y; Texture.h:1405-1411). The header calls the Pad and Stretch modes "nearest" (TextureDefines.h:185-195), but Texture.cpp is not installed, so whether "nearest" rounds up is unverified: if it does, 5410x550 becomes 8192x1024 and 5650x460 8192x512, four and two times B1's and A6's kept figures. The plan therefore uses ResizeToSpecificResolution with explicit sizes only.
- **Mips:** UTexture::MipGenSettings (mip_gen_settings; Texture.h:1425-1427), enum TextureMipGenSettings: TMGS_FromTextureGroup (TextureDefines.h:131), TMGS_NoMipmaps (156).
- **Streaming flag:** UStreamableRenderAsset::NeverStream (never_stream; StreamableRenderAsset.h:369-370).
- **LOD bias:** "number of mip levels to drop when cooking" (Texture.h:1506-1508). MaxTextureSize (Texture.h:1353-1355).
- **Texture group:** UTexture::LODGroup (lod_group; Texture.h:1542-1544), enum TextureGroup: TEXTUREGROUP_World, TEXTUREGROUP_WorldNormalMap, TEXTUREGROUP_WorldSpecular (TextureDefines.h:30-32), and Project01-48 for project groups (75-123).
- **Engine defaults for the World groups:** MaxLODSize 16384, LODBias 0 (Config/BaseDeviceProfiles.ini:190-192). The project has no DefaultDeviceProfiles.ini, so these apply.
- **Virtual textures:** VirtualTextureStreaming per texture (Texture.h:1609-1611).
- **Run-time pictures:** CreateTransient makes "1 mip level" (Texture2D.h:341-342).
- **Pool at High:** r.Streaming.PoolSize=800, LimitPoolSizeToVRAM=1, MipBias=0 (BaseScalability.ini:763-771).
- **Epic's High against the project's:**
  - GI: surface-cache atlas 3584, radiance-cache probe resolution 16 (BaseScalability.ini:369, 377, 387). The project sets 4096 and 32 (DefaultScalability.ini:27, 37), Epic's Epic values (BaseScalability.ini:424, 434).
  - TSR at High: history 100%, R11G11B10 already (BaseScalability.ini:74-78).
- **Hair voxel pages (C7):** the name `r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim` is in no installed 5.8.4 file (Source, Shaders and Config searched by [RV]); it rests on the 5.8.2 .cpp read 8 November. Unverified until step 5's log check.
- **Cooking:** /Game/Ledger is always cooked (ue-probe/Config/DefaultGame.ini:45), so cooked pictures placed under it are packaged without new config.
- **Compression follows each texture's bound sampler (corrected on [RV] fix 4).** The engine compares the sampler type a texture derives with the type its material expression declares; tools/ue/make_base_material.py mirrors the rule in derived_sampler_type (519-555): TC_Normalmap derives NORMAL, TC_Masks MASKS, TC_Grayscale GRAYSCALE or LINEAR_GRAYSCALE, TC_Alpha ALPHA, and TC_Default or TC_BC7 COLOR with sRGB on and LINEAR_COLOR with it off. The street's master material declares NormalMap as SAMPLER_NORMAL (lines 151, 459-464), so:
  - normals bound to a NORMAL sampler: **TC_Normalmap** (BC5). TC_BC7 linear would derive LINEAR_COLOR and mismatch;
  - roughness (LINEAR_COLOR): **TC_Default, sRGB off**;
  - colour: **TC_Default, sRGB on**, or **TC_BC7, sRGB on**;
  - the glb fronts' orm under Interchange's MI_Default_Opaque_DS: **TC_Default, sRGB off**, not TC_Masks. The front's 4096 roughness from the same import cooks as TC_Default linear and works; TC_Masks would derive MASKS, and the parent's sampler types were not reachable (the InterchangeAssets content was not found on disk);
  - emissive: **TC_Default, sRGB on**.
  - The import tool calls derived_sampler_type for every texture against each bound material's declared sampler type and refuses a mismatch.

Epic documentation, 5.8, read 9 November:

- Texture Streaming Configuration (https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine):
  - the pool "contains UI textures, NeverStream textures, cubemaps and streaming textures";
  - PoolSize is "the pool size in MB available for textures";
  - with UsePerTextureBias, each texture's mip bias runs "from 0 to MipBias, depending on the budget computation".
- Texture Format Support and Settings (https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-format-support-and-settings-in-unreal-engine): DXT packs "pixels into 4x4 blocks"; MaxLODSize ranges over powers of two. It says nothing on non-power-of-two sizes.
- Texture Streaming overview (https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-in-unreal-engine): general only.

Reference games ([S12], 25 October): Mafia, on the same engine family, ships streamed textures in explicit pools: textures 1,200-2,000 MB, 1,500 at a 6 GB card's level, virtual textures 323 MB ([S12] lines 11, 38, 82). Kingdom Come II gives 4,096 MB of textures at 6 GB ([S12] line 41), which does not fit LEDGER's 5,650 line ([MP] s1). The method copied is Mafia's: cooked, compressed, mipped and streamed textures in one sized pool. Its numbers are not taken. The pool stays at 800 unless step 4's check says otherwise, and [MP]'s ceiling of 1,000 is the upper bound.

**Virtual textures: not now.** The capture holds 0.06 MB of them ([MW] s6). Turning them on is project-wide, needs every sampler that reads them changed to a virtual one (unverified for the dynamic material instances the street uses), and adds a physical pool. Mafia's 323 MB pool serves a world of 27,680 cells ([S12] line 39), not one street. Revisit with the district's World Partition trial.

## 4. Look risk per change

- **A1-A7 (BC with mips):**
  - BC1 can band dark gradients (the shop cards at night) and block thin lettering. BC7 avoids both at twice the size, and its figure is already the low end of the range.
  - Mips change nothing near the camera and soften distant shimmer.
  - Resizing 1855 to 2048 or 1536 to 2048 stretches the picture inside UVs of 0 to 1, so nothing on screen moves.
  - Risk: low.
- **Streaming of textures bound only through dynamic material instances (all of A, the main look risk; [RV] fix 7):** whether the streamer gives them correct on-screen sizes is unverified. A texture held below its top mip while seen at the hook camera shows as blur. Each step's memreport is read for the new assets' Current/InMem size and UnknownRef column in `listtextures`, and the hook camera's crop is judged at full size beside the last good picture.
- **A cooked picture collected mid-walk ([RV] fix 5):** a cooked texture held only by a dynamic material instance can be garbage-collected, and the surface turns to its default. The loader roots each cooked asset or keeps it in a referenced array, as the code already does for transients (VignetteShot.cpp:6190-6195).
- **A silent fall back to the file ([RV] fix 6):** a stale or missing cooked asset brings back the full cost with no fault showing. Guarded by the log line, the count and the build check in steps 1 and 2.
- **A6 and the crop decals ([RV] fix 11):** the 5650x460 decal cards load at VignetteShot.cpp:7472, which has no crop, so A6 is cooked in step 1 like the rest. Cropping touches only the vignette card decals that ask for it (ImportTexture with a crop rect at 9561, the crop applied at 6169-6175). Those stay on the file path in step 1; they sit inside A2 and A3's unnamed rows, and step 0's log names them. Porting them later needs the same rule as LedgerSurface::CropPixels at import; a wrong crop shows at once. Risk: medium if ported, none if left.
- **B1:**
  - 4096 across a 5.41 m board is 0.76 px a mm, against 1 today.
  - At the walk's 1,892-px internal width, a board seen from 4 m fills well under 4,096 screen pixels (inferred; the camera's field of view was not read), so the top mip is rarely shown.
  - BC1 on sign-writing may block thin strokes; BC7 is the fallback.
  - Risk: low.
- **B2:** labels and signs with alpha need BC7 (or BC3) to keep clean edges. Rows resized down in height (the hours signs from 186 to 128, for example) may thin their lettering; such a row rounds up instead. Risk: low.
- **C7 (hair voxels):** hair transmittance and occlusion change. Too few pages for the grooms in view may drop hair occlusion or flicker (mechanism unverified). That is taste, beside the 2 November hair-shadow ruling (DefaultEngine.ini:89-104). Judged on the walk frames with the most people in view. His look.
- **C2 and C1 (GI):** coarser indirect light and reflections, a step to Epic's own High. The project chose Epic's GI at High by design (DefaultScalability.ini:1-5), so this is the session's GI decision, judged at the gate.

## 5. Order, biggest safe saving first, each with its packaged check

Every check is one packaged day walk at High, game alone, read two ways:

- the peak of GPUMem/LocalUsedMB after the load row, by tools/slice-perf.py, against the **5,650 MB line** ([MP] s4);
- the memreport run of [MW] s5 (line 123) for the owners. Its frame times are void.

Walks spread about 150 MB from run to run (6,041-6,192, [MW] s0). Three runs are needed only when a reading lands within 150 MB of the line. Then the gate's three views go beside the last good picture, with a fresh reviewer (CLAUDE.md "The gate").

**The cooked-picture test, used in steps 1 to 3 ([RV] fix 2).** `listtextures uncompressed` filters by compression setting, and it never listed the 7 BGRA8 normals, so it cannot prove the work done. The test reads `listtextures nonvt` instead (the memreport's own command, [MR] line 1695) and requires:

- no row under the step's folder (/Game/Ledger for step 3, /Game/Ledger/RuntimePictures for steps 1 and 2) in PF_B8G8R8A8;
- each resized row at its target size (the fascia rows 4096x512), NumMips above 1 and Streaming YES;
- for each new asset, Current/InMem at its top mip while it is in view at the hook camera, and the UnknownRef column recorded ([RV] fix 7).

0. **Name the 24 unowned 2048 rows and the rest (no saving).** One log line in ImportTexture (VignetteShot.cpp:6132) giving path, size, MB and the transient object's name. Also a cache in it keyed by path, sRGB and crop, which ends the double decodes [RP] s1 notes at 8798; their saving is unverified. This log also gives A7's rows their targets and names the crop decals step 1 leaves on the file path.
   - Check: the walk's log names all 353 rows of /Engine/Transient.
1. **Cook the run-time street, scan, wear, scalp and sky pictures (A2-A7): up to 926-1,029 MB, less the crop decals' share (unverified).**
   - A new import step in tools/ue reads the same lists as the game: quay-street.json, ps5-corner.json, street-wear.json, vignette-pieces.json, the scalp.
   - It makes /Game/Ledger/RuntimePictures assets, setting on every texture: CompressionSettings and SRGB by role as in section 3 (TC_Normalmap for normals, TC_Default sRGB off for roughness, TC_Default or TC_BC7 sRGB on for colour); MipGenSettings = TMGS_FromTextureGroup; NeverStream off; LODGroup TEXTUREGROUP_World, TEXTUREGROUP_WorldNormalMap or TEXTUREGROUP_WorldSpecular; and where a side is not a power of two, PowerOfTwoMode = ResizeToSpecificResolution with ResizeDuringBuildX/Y: 2048x2048 for the 1536 scans, 4096x512 for the 5650x460 decal cards, and A7's rows at the sizes step 0 names. It checks each texture's derived sampler type against its bound material and refuses a mismatch.
   - ImportTexture then loads the cooked asset first, roots it (or keeps it in a referenced array), and keeps the file path as its fallback. Its OutW/OutH/OutLoadedAs keep reporting the file's own size, or the line gains a "cooked" word and everything that reads it is updated in the same commit ([RV] fix 5).
   - One log line for each picture still decoded from file; a build check fails when any picture in the five lists lacks its cooked asset ([RV] fix 6).
   - Check: /Engine/Transient in rhi.DumpResourceMemory falls from 1,952 to about 630-700 (the cards plus what is left). The cooked-picture test passes for /Game/Ledger/RuntimePictures. The file-decode lines count zero outside the crop decals and the 2x2 textures (6255, 9837). StreamingPool need stays under 800. Peak about 5,120-5,230 (inferred).
2. **Cook the shop-room cards (A1): 406-518 MB.** The same tool and loader, at the one call site (VignetteShot.cpp:8440-8447), ResizeToSpecificResolution 4096x2048.
   - Check: no 30 MB transient row is left; the cooked-picture test passes; the file-decode count as in step 1. Peak about 4,600-4,820 (inferred).
   - Night look ([RV] fix 12): there is no night walk ([MW] s0). The cards' banding is judged on the packaged night-standing capture (as recorded in FINDINGS-2026-10-23) and the morning pictures' street-at-night view, with a full-size crop of a lit card beside the last good picture.
   - One material samples all three states (DayTex, LitTex and DarkTex, VignetteShot.cpp:8438-8446), so streaming keeps all three resident. Loading only the shown state ([MW]) would need that material changed, not only code; it is not counted here ([RV] fix 14).
3. **Import pass for glb pictures (B1 + B2): 294-311 MB.**
   - In import_vehicles.import_glb, after the import, each Texture2D under the destination gets every setting set explicitly, none left to Interchange ([RV] fix 1):
     - CompressionSettings and SRGB from its glTF slot: base colour TC_Default sRGB on (TC_BC7 sRGB on if letters suffer); normal TC_Normalmap; orm TC_Default sRGB off; emissive TC_Default sRGB on;
     - MipGenSettings = TMGS_FromTextureGroup (replacing Interchange's TMGS_NoMipmaps);
     - PowerOfTwoMode = ResizeToSpecificResolution with ResizeDuringBuildX/Y: 4096x512 for the fascia boards, the B2 table's size for the rest, capped by asset-budgets.json's texture_max;
     - NeverStream off, CompressionNoAlpha where the picture has no alpha;
     - the derived sampler type checked against each bound material, a mismatch refused.
   - The fascia rows leave street-sweep-known.json only once the re-imported asset reads 4096x512 in asset_checks.py's size record (blueprint_get_size_x/y, line 867). Whether that call returns the built size or the source's 5410x550 is unverified; if the source, the known rows stay and the check is changed to read the built size ([RV] fix 13). Python only.
   - Check: the cooked-picture test passes for /Game/Ledger: no PF_B8G8R8A8 row (the 7 normals included), the 22 fascia rows at 4096x512 with NumMips above 1 and Streaming YES. NonStreamingMips falls by about 296 + 62. Peak about 4,294-4,526 (inferred).
   - Cheapest of the three by far (inferred). The session may take it first, ahead of the size order.
4. **Pool guard (no saving; up to 200 MB cost).** After steps 1-3, read TextureStreaming/StreamingPool and whether the streamer is over budget. Raise r.Streaming.PoolSize from 800 to 1,000 ([MP]'s ceiling) only if the need tops 800 or pictures visibly soften.
   - Check: the pool's need is under its size, and the peak is still under 5,650.
5. **Look-gated, in order of size, each needing its look at the gate (C7, C2, C1): about 444-459 MB.**
   - Hair voxel pages 8. Check: the packaged game log holds `Set CVar [[r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim:8]]` (the form walk.log:405 shows for DensityScale.Shadow) and no unknown-variable line for it; requested transient memory in the hair frames about 190 ([MW] s4.2); the walk frames with the most people in view looked at for lost hair occlusion or flicker ([RV] fix 8).
   - Radiance-cache probe resolution 16. Check: the 4352x4352 Lumen.RadianceCache.FinalRadianceAtlas row ([MR] 4368, 72.25 MB; not the 2048x2048 second-cache row at 4379, 21 MB) reads 2304x2304 and 20.25 MB; RadianceProbeAtlasTextureSource 2048x2048 (16 MB) and DepthProbeAtlasTexture 2048x2048 (8 MB) ([RV] fix 9).
   - Surface-cache atlas 3584. Check: the lighting atlases read about 49 MB each.
   - With steps 1-3 done, none of these is needed to reach the line. They become headroom for the district.

Not proposed:

- TSR history (156): already at Epic's High settings.
- Distance fields (320): no installed source names the control that sizes the brick atlas. Measure with the district's scale test ([MP] s5 step 3).
- Shadow map (33): Epic's default cascade size (unverified).
- Glass cubes (49.5): whether cube textures stream in 5.8 is unverified.
- Transient heap settings (up to 384): unproven, [MW] s4.3.
- The 18 MB template logo: free to take whenever a level change allows.

## 6. Unverified and unreached

- **Unverified:**
  - that Interchange's glTF import itself chooses TC_EditorIcon and no mips for non-power-of-two pictures (the settings were read from the cooked assets; the import code was not);
  - what the Pad and Stretch power-of-two modes round to (Texture.cpp not installed); the plan avoids them;
  - the Python property names in section 3 (not checked against the editor's stubs);
  - whether each _rgba row holds alpha;
  - A7's rows, their targets and directions (named by step 0), and the share of the crop decals left on the file path in step 1;
  - the third-each split of colour, normal and roughness in A2-A5;
  - the 24 unowned 2048 rows' roles;
  - whether streamed textures set only through dynamic material instances get correct on-screen sizes, or load every mip (the streamer's "UnknownRef" handling, not read);
  - whether asset_checks.py's size record reads the built or the source size;
  - the radiance-cache and surface-cache layouts behind C2 and C1;
  - the hair setting's name in 5.8.4 and the hair figures, read on 5.8.2 .cpp lines now absent;
  - whether the shop cards still in use are 7 shops (21 rows) in every build;
  - all hours and costs.
- **Unreached:** the 5.8.4 engine .cpp files (not installed: AsyncTextureStreaming.cpp, HairStrandsVoxelization.cpp, Texture.cpp, ListTextures' code, the Lumen .cpp files). The Interchange glTF parent material (MI_Default_Opaque_DS) and its sampler types: the asset was not found on disk. Epic's 5.8 page on texture compression settings by name was not found at the URLs tried. The two pages above were read and said nothing on non-power-of-two sizes.

Tags: MP production/research/frame-headroom/MEMORY-PLAN-2026-11-07.md; MW MEMORY-WHERE-2026-11-08.md; RP RUNTIME-PICTURES-2026-11-08.md; RV COOKING-PLAN-REVIEW-2026-11-09.md; S12 production/research/aaa-reference/studies/12-tech-budgets.md; MR and WL in F:/LedgerTools/tmp/memwhere-2026-11-08 (seven-day scratch: copy the lines cited before it is cleared). Engine paths are under C:/Program Files/Epic Games/UE_5.8/Engine/.

## Review fixes applied (9 Nov)

1. Section 0's cause corrected: the 15 YES rows carry TC_EditorIcon and TMGS_NoMipmaps, only the 7 normals fell back for alignment; step 3 sets CompressionSettings, SRGB and MipGenSettings = TMGS_FromTextureGroup on every role; the "cause inferred" line removed from section 6.
2. Steps 1-3 check with `listtextures nonvt` (no PF_B8G8R8A8 row, target size, NumMips above 1, Streaming YES), not `listtextures uncompressed`.
3. Resize named as PowerOfTwoMode = ResizeToSpecificResolution with ResizeDuringBuildX/Y and each size given; B2's 50 rows given targets and directions and recomputed (41-52 to 45.7-53.5); A7's targets wait on step 0 and are marked unverified.
4. Compression chosen from the bound sampler: TC_Normalmap for normals, TC_Default sRGB off for roughness and the glb orm (not TC_Masks), emissive sRGB on, derived_sampler_type checked; no MB change.
5. The loader roots cooked textures; the surface line keeps the file's size or gains a "cooked" word, its readers updated in the same commit.
6. One log line per file-decoded picture, counted in steps 1 and 2, and a build check that every listed picture has its cooked asset.
7. Each step reads Current/InMem and UnknownRef for the new assets and judges the hook camera's crop at full size.
8. The C7 setting's name marked unverified in 5.8.4; its check reads the Set CVar line in the game log; the hair-occlusion look risk added.
9. C2's check names the 4352x4352 FinalRadianceAtlas row (expected 2304x2304, 20.25 MB) and the probe and depth atlases at 2048.
10. C1's wording: the saving is 0.234 of the atlases, not 0.766.
11. Section 4's A6 line: the 5650x460 cards are not cropped and are cooked; the crop decals stay on the file path, so step 1's figure is an upper bound.
12. Step 2's night look uses the packaged night-standing capture and the street-at-night view, with a full-size crop of a lit card.
13. The fascia rows leave street-sweep-known.json only once asset_checks.py reads 4096x512 for them.
14. The cards' one material keeps all three states resident; noted, no figure change.

Totals after the fixes: A plus B 1,626-1,858 MB (was 1,621-1,856); with C7, C2 and C1 2,070-2,317 MB (was 2,065-2,315); step 3 294-311 MB (was 289-309); peak with A and B about 4,294-4,526 MB.
