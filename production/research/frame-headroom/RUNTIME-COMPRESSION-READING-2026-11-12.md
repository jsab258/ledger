# Runtime texture compression, reading notes (12 Nov 2026)

Source: installed Unreal 5.8.2, root `C:\Program Files\Epic Games\UE_5.8\` (paths below are under it; all read 12 Nov 2026). No web pages used. No recommendation.

## 1. Block-compressed transient texture from CPU pixels, packaged build

- `UTexture2D::CreateTransient(SizeX, SizeY, Format, Name, ImageData)` accepts any EPixelFormat, not only BGRA8: it sizes the buffer from `GPixelFormats[Format]` block size and bytes, and copies in `ImageData` if given (`Engine/Source/Runtime/Engine/Private/Texture2D.cpp:1291-1354`). It is not editor-guarded. So a texture whose pixels are ALREADY BC1/BC3/BC7 can be created at run time.
- It refuses sizes not a multiple of the block (4x4 for BC): `Texture2D.cpp:1304-1309` ("Size specified isn't valid for block-based pixel format"). 4096x1855 fails (1855 % 4 = 3); it would need padding to 1856 or a resize. It creates exactly one mip (`Texture2D.cpp:1341`).
- Compressing from RGBA at run time is not in the packaged engine:
  - `TextureCompressor` is in `Engine/Source/Developer/`. UBT adds `Source/Developer` directories only when `bBuildDeveloperTools` is on (`Engine/Source/Programs/UnrealBuildTool/Configuration/UEBuildTarget.cs:5084-5089`); `ModuleHostType.Developer` compiles only for Editor and Program targets (`.../Descriptors/ModuleDescriptor.cs:794-795`).
  - Its Build.cs lists Core, ImageCore, OpenColorIOWrapper, TextureBuildUtilities, TextureFormat; no type setting (`Engine/Source/Developer/TextureCompressor/TextureCompressor.Build.cs:5-26`).
  - Runtime modules reference it only inside editor branches: `Engine.Build.cs:404-433` (`if (Target.bBuildEditor == true)`, adds TextureCompressor at line 430) and `Launch.Build.cs:212-220` (comment "loaded when WITH_EDITOR=1", line 216).
  - `TextureFormatDXT` (BC1/3 via nvTextureTools; `Developer/TextureFormatDXT/TextureFormatDXT.Build.cs:5-26`) and `TextureFormatIntelISPCTexComp` (BC6/BC7 family; `.../TextureFormatIntelISPCTexComp.Build.cs:5-31`) are Developer-folder modules, so the same rule applies.
  - Oodle Texture: the plugin file says "Deprecated Oodle Texture plugin, now built into Engine", no modules (`Engine/Plugins/Developer/TextureFormatOodle/TextureFormatOodle.uplugin:9,15-16`); the module is `Engine/Source/Developer/TextureFormatOodle/Source/TextureFormatOodle.Build.cs`. Developer folder, so editor/cook side (Build.cs body not read; UNVERIFIED beyond its location).
- Not confirmed: whether a Development-game target with `bBuildDeveloperTools=true` would link these; the project's target rules were not read. UNVERIFIED.

## 2. Engine-supported runtime path to compressed textures

- Interchange runtime (`Engine/Plugins/Interchange/Runtime/Interchange.uplugin`, module entries "Type": "Runtime", e.g. lines 26-81). In its texture factory the non-editor branch `SetupTexture2DSourceDataFromBulkData_Runtime` (`.../Import/Private/Texture/InterchangeTextureFactory.cpp:1505-1576`) takes the raw-format pixel format of the source (`GetPixelFormatForRawImageFormat`, line 1513) and copies with `FImageCore::CopyImage` (line 1569). No compressor call in this branch. Output is uncompressed, one mip.
- Interchange DDS translator exists (`.../Texture/InterchangeDDSTranslator.cpp`; DXGI format mapped to the "closest raw format", lines 300, 383), so it decodes DDS to raw formats; whether it keeps BCn at run time was not read. UNVERIFIED.
- `FImageUtils::CreateTexture2DFromImage` (`Engine/Source/Runtime/Engine/Private/ImageUtils.cpp:1391-1409`) also makes an uncompressed transient texture.
- No glTF runtime plugin exists in `Engine/Plugins` (Glob `**/*glTF*.uplugin`: none found).
- Net from source read: no shipped runtime compressor found. Pre-compressed data (made offline, e.g. as DDS or raw blocks) fed to `CreateTransient` is the only route seen. Nothing here proves a hand-added extra mip works; UNVERIFIED.

## 3. Memory arithmetic, 4096x1855 (block data only, no GPU alignment or padding)

Mip sizes (floor halving): 4096x1855, 2048x927, 1024x463, 512x231, 256x115, 128x57, 64x28, 32x14, 16x7, 8x3, 4x1, 2x1, 1x1 (13 levels).

- BGRA8, mip 0: 4096 x 1855 x 4 = 30,392,320 B (28.98 MiB). Full chain: 10,128,079 texels x 4 = 40,512,316 B (38.63 MiB).
- BC1 (8 B per 4x4 block), mip 0: 1024 x ceil(1855/4)=464 = 475,136 blocks = 3,801,088 B (3.63 MiB). Chain: 633,533 blocks = 5,068,264 B (4.83 MiB).
- BC7 (16 B per block), mip 0: 7,602,176 B (7.25 MiB). Chain: 10,136,528 B (9.67 MiB).
- BC3 equals BC7 in size (16 B). Same figures hold at 1856 rows.
- Ratios: BC1 mip 0 is 1/8 of BGRA8 mip 0; BC7 is 1/4. The mip chain adds about one third.

## 4. Importing PNGs as cooked assets, streaming

- Cooked textures are ordinary UObjects; binding by path is the normal `LoadObject`/soft-path mechanism. No texture-specific source read for this. UNVERIFIED by source.
- Streaming eligibility, `UTexture::IsPossibleToStream` (`Engine/Source/Runtime/Engine/Private/Texture.cpp:1833-1890`):
  - false if `NeverStream` or `LODGroup == TEXTUREGROUP_UI` (1836);
  - false if platform data has exactly 1 mip (1861-1864);
  - false if more than one mip but width or height is not a power of two (1869-1872: "we can only stream pow2 textures at the moment");
  - false if `MipGenSettings == TMGS_NoMipmaps` (1887, editor-only data).
- So 4096x1855 cooked with mips would be non-power-of-two: it keeps mips (mip count is not what is refused) but never streams, so its whole chain stays resident. Comment at `Texture.cpp:676-679` confirms NeverStream is no longer set at import for non-pow2; the runtime check does it. Whether the cook pads to pow2 (PadForPow2) was not read; UNVERIFIED.
- Streaming of a runtime `CreateTransient` texture: it has 1 mip, so `IsPossibleToStream` is false (1861); `bNotOfflineProcessed = true` (`Texture2D.cpp:1338`).
- A 4096x2048 or 4096x1024 pow2 resize would pass the pow2 test; this is arithmetic from line 1869 only, not tested.

## 5. Virtual textures

- `FVirtualTexture2DResource` needs pre-built VT data: `check(InVTData)` (`Texture2D.cpp:1600-1601`). Cooked VT data is produced by the build; `Texture.cpp:681-682` shows the editor forcing VT when the larger side exceeds `GetMaximumDimensionOfNonVT()`. No runtime path from raw PNG pixels to VT was found. Runtime Virtual Textures (the RVT feature) render material output into a VT; not read, and not an image-import path as far as the source read shows. UNVERIFIED.
- `VirtualTextureStreaming` is also tied to `IsVirtualTexturingEnabled()` (`Texture.cpp:687`); the project's setting for it was not read.

## Not reached / not read
- Web docs (none opened).
- Project's `Target.cs` and config (virtual texture setting, bBuildDeveloperTools).
- `TextureFormatOodle` and nvTextureTools module bodies; D3D12 RHI support for PF_BC7 (assumed standard, unchecked).
- Engine cook-side mip generation for non-pow2 textures.
