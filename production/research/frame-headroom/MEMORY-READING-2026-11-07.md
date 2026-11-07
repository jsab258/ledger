# Card memory for a district: first-pass reading (7 Nov 2026)

Reading only; no synthesis, no recommendation. All links read 7 Nov 2026. "Src" = installed source, C:\Program Files\Epic Games\UE_5.8, read 7 Nov 2026. Engine 5.8 facts below come from that source or from Epic's pages (current version, not version-pinned by the fetcher: unverified for 5.8 where noted).

## What home already answers (not re-read)

- Diagnosis (F:/LedgerTools/gate/new/card-memory-2026-11-07/diagnosis.md): six builds read 5,810 to 6,089 MB; no lasting growth, the swing most likely scatter (medium confidence, step never repeated on one build). The figure is DXGI use of the game alone, voice excluded. The step ran the texture pool at 1000 (Highest); play at High is 800 and read about 5,600 standing, 5,850 walking.
- production/research/frame-headroom/FINDINGS-2026-10-23.md: game alone median 4.6 to 5.1 GB, peaks 5.6 to 6.8 GB walking; cast voice on the card adds about 2.3 GB.
- LAUNCH-PEAK-2026-11-04.md: eight boot captures; the game's own card use peaks at 6.1 to 6.2 GB in frames 13 to 22, then settles about 5.5 GB. Render-graph transient heap 768 to 896 MB, render-target pool about 1,276 MB at the peak. The "8 GB launch peak" was Windows' counter only. Candidate causes (transient heaps, render-target pool) never confirmed.
- Study 12 (read 25 Oct): Mafia (UE 5.4) pools: textures 2,000 MB, virtual textures 323 MB, Nanite 300 MB; texture pool by quality 1,200/1,500/2,000/2,000 MB; Mafia's auto-detect puts a 6 GB card at level 1 (1,500 MB). KCD2 (CryEngine, not Unreal): textures 4,096 MB at 6 GB, 5,120 at 8, 8,192 at 12; mesh pool 768 MB. Both keep people in full detail by distance (KCD2: 70 within 150 m; Mafia: freeze unseen beyond 70 m, never within 10 m; hair shadows to half distance). No per-category card-memory totals from either game.
- Study 4: Mafia's Palermo main grid is 73 cells at 128 m plus 33 always-loaded and 7 coarser; props grid 32 m; 27,680 runtime cells game-wide; Quay Street is one 48 m street. Cell sizes in metres for other levels not read; KCD2 cell sizes not known.
- Method taken from Mafia's 5.4 config (pool values, scalability ladder, significance rules) needs checking against 5.8: Mafia's exact cvar names and defaults were read in 5.4 config files; see 5.8 values below where they differ.

## Q1 World Partition and streaming

- Whole world is one persistent level cut into grid cells; the 2D runtime-hash grid is default; Epic warns more than one grid can hurt performance. Epic's own example: cell 256 m, loading range 768 m radius around a streaming source; defaults not stated on the page. Player controllers are streaming sources by default. https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine
- Always loaded: actors with "Is Spatially Loaded" off, and anything referenced from the level blueprint; actors referencing each other load together. Data layers switched off keep their actors unloaded. Same page.
- HLODs are generated per cell by a build step; no cell sizes or distances given. `wp.Runtime.MaxLoadingLevelStreamingCells` caps concurrent cell loads (no default stated). Same page.
- Not read: Epic's HLOD and Data Layers pages; any town-scale number in metres from a shipped Unreal game other than Mafia's 128 m/32 m grids (home).

## Q2 Texture streaming pool and virtual textures

- `r.Streaming.PoolSize` is the pool in MB; default -1 (engine default size); 0 unlimited per Epic. Src Engine/Private/Streaming/TextureStreamingHelpers.cpp:119-123. It holds UI, never-stream and cube textures as well as streaming ones (Epic: https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine).
- Scalability ladder in 5.8: pool 400 / 600 / 800 / 1000 / 3000 MB for levels 0, 1, 2, 3, Cine; levels 0 to 2 set LimitPoolSizeToVRAM=1 (pool capped to card memory), 3 and Cine 0. Src Engine/Config/BaseScalability.ini:740-794. Level 0 uses MipBias 16, level 1 MipBias 1.
- Over budget: with `r.Streaming.UsePerTextureBias` (default 1, src helpers.cpp:202-205) each texture gets a mip bias between 0 and `r.Streaming.MipBias` as needed to fit; textures lose their top mips rather than failing. Epic page above is the same. Whether anything else changes at a hard limit: unverified.
- `r.Streaming.PoolSize.VRAMPercentageClamp` default 1024 MB (src helpers.cpp:325-330); how it combines with PoolSize on D3D12: unverified.
- Virtual textures have their own physical pools (Project Settings, Virtual Texture Pool; per-format fixed pools; auto-grow flag for cooked builds is `r.VT.PoolAutoGrow`). Each pool is a least-recently-used cache; at 100% residency visible tiles are dropped (extra IO, flicker); residency mip bias, if switched on, lowers resolution globally, the largest bias from any pool applying to all VT sampling. Tiles: 128 texels (streaming VT), up to 1024 for runtime VT. Defaults for pool size not stated. https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-texture-memory-pools-in-unreal-engine
- Not reached: Epic's Texture Streaming Overview, Metrics, Building pages.

## Q3 Nanite, Lumen, virtual shadow maps: card memory

- Nanite streaming pool: default 512 MB, excludes root pages; Epic's note warns root pages come from the same buffer and to be careful near the GPU resource limit (typically 2 to 4 GB). Src Engine/Private/Rendering/NaniteStreamingManager.cpp:57-64. Epic's Nanite page gives no memory figures: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine. The Nanite Technical Details page returned no text (unreached). Mafia's pool of 300 MB (home) is below this default.
- Virtual shadow maps: one physical page pool for all lights; page is 128 x 128 texels (src Shaders/Shared/VirtualShadowMapDefinitions.h:13-14). `r.Shadow.Virtual.MaxPhysicalPages` code default 2048 (src Renderer/Private/VirtualShadowMaps/VirtualShadowMapArray.cpp:174-180); scalability sets 512 (levels 0, 1), 2048 (level 2), 4096 (level 3), and 8192 at a further section (BaseScalability.ini:146, 181, 219, 257, 295; the last section's name unverified). Texel format not read, so MB per page is not stated here. Over the pool, Epic says corruption (checkerboard, missing shadows) with a warning in log. https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine
- Lumen: surface cache atlas `r.LumenScene.SurfaceCache.AtlasSize` code default 4096 (src Renderer/Private/Lumen/LumenScene.cpp:127-130); scalability values 2048, 3584, 4096, 4096 (BaseScalability.ini:335, 377, 424, 472; section names not matched, unverified). Card max resolution 256 at the lowest listed (line 340). Epic: static meshes get 12 cards by default, skeletal meshes six; software tracing range 200 m default; Epic's time targets only (8 ms epic / 4 ms high at 1080p internal on consoles). https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine and https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine. A runtime compression switch exists (src LumenSurfaceCache.cpp:29-33).
- Measured MB on an 8 to 12 GB card for Lumen, Nanite or VSM alone: not found in any primary source. Two third-party figures exist and are unverified: a blog claiming the 4096-page VSM default suits linear games, not open worlds, and that 16384+ pages is 1 GB+ (https://www.strayspark.studio/blog/virtual-shadow-map-optimization-open-worlds-ue5-7, seen only as a search snippet, not read). An UE forum report: an 8 GB card on an ARK port into 5.5 fell to 200 ms+ GPU frames once near budget; its memreport shows 2,615 MB transient memory requested, 640 MB used after aliasing, 7,317 MB non-transient, many resources evicted. Epic staff: eviction starts at 70% of budget (one-minute idle), at 100% the idle threshold drops to one second; a ray-tracing build gate had made residency priority a no-op, tracked UE-305620. https://forums.unrealengine.com/t/unrecoverable-200ms-gpu-frame-time-after-nearing-local-vram-budget-pc-d3d12-resources-appear-to-page-to-shared-and-not-page-back-when-local-is-available-possibly-related-to-r-rdg-transientallocator/2642549 (a forum thread; staff statements, but the engine fix status for 5.8 unverified). The 640 MB transient figure matches the 640 MB steady value in home's launch-peak note.

## Q4 Detail levels, hair and MetaHuman, crowds

- Epic: MetaHumans use 8K textures; `MaxLODSize` in device profiles caps texture resolution per platform (no values given). Strand grooms at LOD 0 and 1 "use a lot of memory"; `r.HairStrands.MinLOD=3` strips hair LODs at cook; `r.HairStrands.UseCardsInsteadOfStrands=1` forces cards (nothing shows if none exist). Nanite does not support skeletal meshes. https://dev.epicgames.com/documentation/en-us/metahuman/requirements-and-configuration-settings-for-metahumans-in-unreal-engine
- Scalability: `r.SkeletalMeshLODBias` 2, 1, 0, 0, 0 by effects/view-distance ladder (BaseScalability.ini:111-127; section name unverified).
- Epic's Platform and LOD Specifications page (triangle counts per LOD, per-platform tables) was fetched but returned no text: unreached. No official per-person memory figure found.
- Community, unverified: about 2.3 GB per character at LOD 0 (one forum estimate); LOD 0 about 60k and LOD 1 about 40k triangles for a face; groom LOD tied to the face LOD; 50 MetaHumans sharing one card groom, rigid bindings cost about 3 ms render-thread time. Source: search result only, thread pages not read (https://forums.unrealengine.com/t/high-render-thread-cost-of-groom-bindings-even-on-rigid-mode/2725272, https://forums.unrealengine.com/t/optimizing-metahumans-5-2-1/1327489).
- Shed with distance, from home: Mafia and KCD2 significance rules (Study 12); Unreal 5.8 has Significance Manager and Animation Budget Allocator plugins (home, checked on disk).

## Q5 Published budgets from shipped games on 8 to 12 GB cards

- None found per category. Study 12 holds the only per-pool numbers (Mafia, KCD2 above).
- TechSpot's VRAM-use article (PIX measurements, Far Cry 6 5.7 GB average / 6.2 GB peak per a search summary) returned HTTP 403: unreached, not evidence.
- Unreal Fest 2024 "Optimizing UE5: Advanced Rendering, Graphics Performance, and Memory Management" (Epic): only a German written summary and a video link were reachable; no numbers in the written part. The "22 GB scene in 500 MB" streaming-VT claim is unverified. https://forums.unrealengine.com/t/talks-and-demos-optimizing-ue5-advanced-rendering-graphics-performance-and-memory-management-unreal-fest-2024/2657970
- No GDC Vault written talk with a per-category card budget was reached.

## Q6 Peak against average; how studios measure

- memreport: snapshot, written to Saved/Profiling/MemReports with `-full`; the texture list sorts largest first; `rhi.DumpResourceMemory` lists only the top 50 unless `all`; evicted resources lack the Resident flag. From a search summary of forum posts, not read in full: unverified. Epic's memreport page returned only a contents list (unreached).
- Timeline of card memory: CsvProfiler GPUMem/LocalUsedMB per frame (home, LAUNCH-PEAK; src RHIStats.cpp:92 per home). A forum answer says the CSV value comes from the RHI side and is not an exact VRAM reading: unverified; home notes it reads DXGI use.
- Memory Insights: trace with `-trace=default,memory` from process start (packaged builds must be Development); LLM tags per-frame for RenderTargets, SceneRender, UObject, about 1 ms for the others; no peak-finder, but the highest point on Total Allocated plus an Active Alloc query at that time lists live allocations; export to CSV/TSV from the right-click menu. https://dev.epicgames.com/documentation/en-us/unreal-engine/memory-insights-in-unreal-engine
- Per-build checks by studios: no source found. Home's own series (six builds, scatter 5,810 to 6,089) shows the single-sample spread in this project; the diagnosis proposes three runs per build.

## Not reached or unverified

- Epic pages that returned no usable text: Nanite Technical Details, MetaHuman Platform and LOD Specifications, memreport command page, Texture Streaming Overview/Metrics.
- TechSpot (403). Strayspark and forum threads on MetaHuman cost seen only as search snippets.
- Measured per-feature MB for Lumen, Nanite and VSM on 8 to 12 GB cards; per-person MetaHuman memory from Epic; any per-category budget from a shipped game besides Study 12; GDC/Unreal Fest slide numbers; Epic's HLOD and Data Layer pages.
- VSM page texel format, hence MB per page; section names for the Lumen and shadow ladder rows noted above.
