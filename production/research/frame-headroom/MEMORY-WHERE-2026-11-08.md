# Where the walk's card-memory peak sits and what holds it (8 November 2026)

Order item n09-3, diagnosis only, read-only. Nothing was run but Python readers over files already on disk; no game, editor or build. Engine citations are the installed source, C:/Program Files/Epic Games/UE_5.8 (5.8.2), read 8 November. "MB" in the CSV columns is MiB (the engine divides by 1024 twice). Numbers marked (inferred) are computed, not measured.

Data read: the 50 walk captures in F:/LedgerTools/tmp/p1-packaged/packaged-day-walk-*.csv with their -memory.jsonl series and .log files; the stand captures beside them; the eight boot captures in F:/LedgerTools/tmp/launch-peak-2026-11-04/ (from launch, with distance-field and ray-tracing columns the walks lack). No memreport, rhi.DumpResourceMemory, ListTextures, memory trace or LLM output exists anywhere on F: (searched).

## 0. Is the measure wrong?

Partly, in four places. The peak itself is real.

- **There is no night walk.** tools/p1-packaged.ps1 (lines 11-14, 85-89) makes three captures: day stand, night stand, day walk. The 6,1xx MB peaks are all day walks; the eight night stands peak at 5,263 to 5,607 MB. "Night" describes when some runs happened (3b3454e at 05:09), not the scene.
- **The range is wider than reported.** Over the 42 walks of 3641d53 and 7bef7cf the peak runs from 6,041 (rate19) to 6,192 MB (rate10), not 6,104 to 6,163. 3b3454e reads 6,127.
- **The peak is not a single bad sample.** It is a plateau of about 600 frames (about 10 s), and the CSV figure is queried every frame (D3D12RHI.cpp:614 calls UpdateMemoryStats; D3D12CommandContext.cpp:751; DXGIUtilities.cpp:69, 111 reads CurrentUsage).
- **Two rows of MEMORY-PLAN-2026-11-07's table are likely wrong.** The render-target row's "shadow pages, 256 MB": this project draws classic shadow maps. r.Shadow.Virtual.Enable defaults to 0 (VirtualShadowMapArray.cpp:161-162), nothing sets it, and CrimeProbe.cpp:4777 says so. So no virtual-shadow page pool is allocated. The "ray-tracing geometry resident, 221 MB" row: RayTracingGeometry/TotalAlwaysResidentSizeMB is bookkeeping. It sums sizes whether or not the geometry is evicted (RayTracingGeometryManager.cpp:909-918, 1108). IsRayTracingEnabled() is false with r.RayTracing.Enable=0 in dynamic mode (RenderUtils.cpp:1903-1912), and the engine's own help says all ray-tracing geometry is evicted then (RayTracingGeometryManager.cpp:101-102). Whether the 221 MB is on the card is unverified, and probably not.
- The walks' levels: textures, shadows and view distance at High; global illumination, reflections and shading at 3. The log's "Current Scalability Settings" shows this. It is by design: the project's High carries Epic's GI and reflections (ue-probe/Config/DefaultScalability.ini:1-5, 18-27). Pool 800 MB (CSV metadata streamingpoolsizemb). 3440x1440 at 55%.

## 1. Phase: the walk on the street, as people come within hair-strand range

Confidence: high.

The capture starts after the walk-round, the voice start and a forced clean-up: "capture starts 2.0 s after the street settled" (CrimeProbe.cpp:5301, 5326-5329). So the walks contain no launch, no camera cut and no office visit. The camera moves 1.4 m/s from cam_hook (-3.00, -1.60) along yaw 20.4 (CrimeProbe.cpp:5361-5362). At the walk's frame rate, frame 560 is about 9.7 s and about 13.5 m out (inferred from summed FrameTime).

Seen in every one of the 50 walks, and in no stand:

| Frames (lazye; others within about 15) | Walked (inferred) | What changes | LocalUsedMB |
|---|---|---|---|
| 0 | 0 m | street settled | 5,643 |
| 214 | 4.9 m | hair-strand passes begin; requested transient memory 110.5 to 511.5 MB; heap 640 to 768 | +128 |
| 383 | about 8 m | heap 768 to 896 | +128 |
| 536-558 | about 13.5 m | streamed textures' need 102 to 187 MB (Rocco at the rank is about 1 m away at that point) | +64, +32, +64 |
| **558** | **13.5 m** | **peak** | **6,163** |
| 807-816 | about 19.5 m | hair-strand passes end | |
| 821-827 | | heap back to 640 (16-cycle release, RHICoreTransientResourceAllocator.cpp:41-46, 597-627); card -256 | 5,875 |

- The hair-strand passes (GPU/HairStrandsVisibility and the rest) run in 570 to 641 frames per walk. They overlap the "requested over 300 MB" frames by 97 to 99%, and the heap's growth frame for frame. The stands show no strand frame and no heap growth.
- Most walks peak at frames 556-579. Six peak at 752-775, still inside the window.
- The rest of the climb (about 160 MB, in 64/32 MB steps beside the streamed textures' need) stays after the window. That is why the walk settles about 230 MB above where it started (inferred: streamed mips or buffer-pool blocks kept).
- The launch is a separate peak, not in these numbers. The boot captures read 6,086 to 6,224 MB at frames 13-22. There too the hair passes run and requested transient memory is 511.5 MB at the peak frame.

## 2. What the columns say holds the memory at the peak

lazye, frame 558, 6,163 MB.

| Holder | MB | Source |
|---|---|---|
| Textures outside streaming (TextureStreaming/NonStreamingMips) | 2,459 | every non-render-target, non-UAV texture, less streamed residency (RHICoreStats.cpp:107-121; StreamingManagerTexture.cpp:790-799; AsyncTextureStreaming.cpp:1136, 1215) |
| Render-target pool (RenderTargetPoolSize) | 1,276 | flat in every capture; includes Lumen's surface-cache atlases (LumenSurfaceCache.cpp:236-290), about 240-350 at atlas 4096 (inferred from the formats at lines 103-106); no virtual-shadow pool (section 0) |
| Render-graph transient heaps (TransientMemoryUsedMB) | 896 | of which requested 511.5 (TransientMemoryAliasedMB is the requested high-water mark, RHICoreTransientResourceAllocator.cpp:89-100; used is the summed heap capacity, :619) |
| Streamed textures' need (TextureStreaming/StreamingPool) | 187 | the column is the required size, not the 800 MB cap (StreamingManagerTexture.cpp:1989-1990); the cap is never approached |
| Shaders | 9 | |
| Distance fields | about 272 | atlas 256 + indirection 8-16; boot captures only, not in the walk CSV |
| Ray-tracing geometry | 214-221 counted | probably not resident (section 0) |
| **Not in any column** | **about 1,064** | by subtraction, after distance fields (inferred): meshes, MetaHuman morph targets and skin cache, groom data, GPU scene, Lumen buffers, buffer pools, swap chain. The data cannot split it. |

Nanite: no column. Nanite was switched off for the street (DefaultEngine.ini:121-123); whether its pool is allocated is unknown. Skeletal meshes: only a tick count (25 components).

**What the 896 MB heap holds at the peak (inferred, strong).** The hair voxel page texture is a render-graph 3D texture: 14³ pages of 32³ voxels = 448³, PF_R32_UINT, 6 mips (HairStrandsVoxelization.cpp:93-100, 841-853, 918-928). 3D textures are eligible for the transient heap (RenderGraphBuilder.cpp:522-535). That is 343 MiB at the top mip and 392 MiB with mips; the measured jump in requested memory is 401 MiB. A heap is at least 128 MB, sized to the next power of two of its first allocation (RHICoreTransientResourceAllocator.cpp:20-25, 557-558; .h:653-656). Hence the two 128 MB steps.

**What the 2,459 MB holds (inferred, medium).** The game decodes pictures at runtime into uncompressed BGRA8 textures with one mip, never streamed and kept rooted (VignetteShot.cpp:6132, 6182-6194; engine Texture2D.cpp:1291-1353). That covers:

- the street sidecar's 58 maps: 487 MB (surface 264, drawn 126, decals 97; read from production/assets/street/quay-street.json and the staged files' headers);
- seven shop cards, three states each, 4096x1855: 609 MB (VignetteShot.cpp:8437-8446; production/specs/shop-interiors.json lines 79-439);
- Tom's scalp paint and the sky photographs: about 32 MB.

Together about 1,130 MB. The glass cubes are BC6H (tools/ue/import_glass_bake.py:142), about 104 MB for day and night (inferred). The rest, about 1,200 MB, is unnamed: MetaHuman and other cooked textures marked never-stream, UI, engine defaults.

## 3. Game alone or other processes

Confidence: high that the CSV counts the game process alone.

GPUMem/LocalUsedMB is the game process's DXGI CurrentUsage (DXGIUtilities.cpp:69, 111; RHIStats.cpp:92). Microsoft's page defining its per-process scope was not read; the data supports it.

- The sampler's whole-card figure runs 1.4 to 2.2 GB above the game's figure.
- The voice child's card use reads 0 in these walks.
- Windows' per-process counter for the game and its children reads above the game's own figure at the peak: 117 MB (lazye), 212 (rate01), 360 (3b3454e). In the 3b3454e day stand it reads about 950 MB above. That gap is unexplained.

The game's budget (LocalBudgetMB) falls from 9,427 to about 7,740 MB in most walks, and to 5,671-5,691 in 3641d53 novoice a-c. Those three crossed the budget for 1,118-1,178 frames, with 88-96 ms frames about five frames after crossing. So the 5,650 line has real consequences.

## 4. The three biggest likely savings

1. **Runtime-decoded pictures: about 800-950 MB (inferred).** No cvar reaches a CreateTransient texture: one mip, no compression, no streaming, so no mip bias or MaxLODSize applies. The engine's controls apply only once these are cooked texture assets:
   - CompressionSettings: BC1/BC7 for colour, TC_Normalmap (BC5) for normals, TC_Masks or TC_Grayscale (BC4) for roughness;
   - MipGenSettings, with NeverStream off;
   - LODGroup with MaxLODSize in DefaultDeviceProfiles;
   - then r.Streaming.PoolSize (TextureStreamingHelpers.cpp:119-123).

   A game-code-only part: load only the shown light state of each shop card, saving about 406 MB (inferred). Confirm the size first with the run in section 5: memreport's `listtextures uncompressed` should list about 1,100 MB of B8G8R8A8 transient textures. Confirm the saving with one packaged walk after the change: NonStreamingMips should fall from 2,459 toward about 1,400-1,600, and the peak by the same.
2. **Hair voxel page texture: about 256 MB off the walk's peak (inferred from the measured mechanism).** Runtime cvar `r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim` (default 14, HairStrandsVoxelization.cpp:96, 100). At 8 the texture is 73 MiB, so the requested total is about 190 instead of 512. Or `r.HairStrands.Voxelization=0` (:33-34, 143-145) removes it, along with hair transmittance and occlusion. Confirm in one packaged walk with `-Cvars "r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim=8"`:
   - TransientMemoryAliasedMB in frames 214-827 reads about 190;
   - TransientMemoryUsedMB stays 640;
   - the peak falls to about 5,880-5,910.

   The hair's look changes. That is a taste matter, beside the 2 November hair-shadow ruling (DefaultEngine.ini:89-104).
3. **Transient heaps held above need: up to about 384 MB (low confidence).** Every capture but one holds 640 MB of heaps for 102-110 MB requested. The 3b3454e day stand held 256 MB for the same 110.5 MB and read 410 MB lower. But Windows' counter did not fall in that run, so the saving is unproven. The boot captures request the voxel texture at launch, so saving 2 may also shrink this. Controls:
   - `RHI.TransientAllocator.MinimumHeapSize` (128, startup-only; RHICoreTransientResourceAllocator.cpp:20-25);
   - `RHI.TransientAllocator.GarbageCollectLatency` (16, startup-only; :41-46);
   - `r.RDG.TransientAllocator` (0/1/2, runtime; RenderGraphPrivate.cpp:249-256).

   Confirm in the same run as saving 2: the settled TransientMemoryUsedMB, together with Windows' per-process counter.

Smaller or none:
- Lumen's atlas at Epic's High of 3584 instead of the project's 4096 (DefaultScalability.ini:27; BaseScalability.ini:377): about 55-80 MiB (inferred).
- Virtual-shadow pages: none, the feature is off.
- Ray-tracing geometry: probably none (section 0).

## 5. What is missing, and the one capture that fills it

Missing:
- an owner list for the 2,459 MB and for the about 1,064 MB in no column;
- the 64 MB steps' owner;
- whether the 221 MB of ray-tracing geometry is resident;
- why heaps stay at 640;
- the gap between DXGI and Windows' counter;
- the launch peak's 570 MB.

`memreport -full` runs all the needed dumps (BaseEngine.ini [MemReportFullCommands], from line 2408):
- rhi.DumpMemory and rhi.DumpResourceMemory, with Lumen, Shadow, Hair, MorphDeltasVB, SkinCache and TextureCube summaries;
- listtextures uncompressed;
- r.DumpRenderTargetPoolMemory.

Resource tracking exists in Development builds (RHI.Build.cs:31-34). `-csvExecCmds=<frame>:<command>` runs a command at a chosen capture frame (CsvProfiler.cpp:5203-5230; LaunchEngineLoop.cpp:1479). The one run, on the packaged copy, nothing else on the card:

`powershell -File tools/p1-packaged.ps1 -Only day-walk -Tag memwhere -GameArgs '-csvExecCmds="560:memreport -full,561:rhi.DumpResourceMemory all,1100:memreport -full"'`

- Frame 560 is the peak; frame 1100 is the settled walk.
- Reports land in F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Profiling/MemReports; copy them out before the next capture.
- That run's frame times are void (memreport stalls). Its memory sampler still gives Windows' counter beside it.

Not checked or not reached:
- Microsoft's CurrentUsage page;
- the cooked never-stream flags of MetaHuman textures;
- whether -dpcvars reaches startup-only cvars (DeviceProfileManager.cpp:737-760 was not followed into the console manager);
- Lumen's direct and final lighting atlas formats (sizes above assume 4 bytes a texel);
- the build machine's perf CSVs (its step stands still at r.ScreenPercentage=50 with no scalability set, and keeps only the verdict line; .github/workflows/ledger-probe-unreal.yml:2060-2128).
