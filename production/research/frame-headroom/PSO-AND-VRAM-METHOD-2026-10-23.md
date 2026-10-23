# First-use pipelines, loading flushes and card memory: the method, and this project's settings (23 October 2026)

Answers questions 2b, 2c and 1c of QUESTIONS-2026-10-23.md. Research only: nothing was changed.

Engine: UE 5.8.2 (CL 56702186), installed at C:/Program Files/Epic Games/UE_5.8. Source paths below are relative to its Engine/Source/Runtime folder. All sources were read on 23 October 2026. Measurements come from the newest packaged walk on this PC: build fd4003b, run at 15:31 local on 23 October. Its files are in F:/LedgerTools/played-game/Windows/LedgerProbe/Saved: Logs/LedgerProbe.log and Profiling/CSV/Profile(20261023_153157).csv. Card: AMD Radeon RX 6700, 10,194 MB, Adrenalin 26.10.1. Processor: Ryzen 5 5600X, 6 cores, 12 threads.

Sources read in full:
- [D1] "PSO Precaching", https://dev.epicgames.com/documentation/en-us/unreal-engine/pso-precaching-for-unreal-engine (5.8 docs)
- [D2] "Creating a Bundled PSO Cache", https://dev.epicgames.com/documentation/en-us/unreal-engine/manually-creating-bundled-pso-caches-in-unreal-engine
- [D3] "PSO Caches", https://dev.epicgames.com/documentation/en-us/unreal-engine/optimizing-rendering-with-pso-caches-in-unreal-engine
- [D4] "Asynchronous Asset Loading", https://dev.epicgames.com/documentation/en-us/unreal-engine/asynchronous-asset-loading-in-unreal-engine
- [D5] "Asset Management", https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine
- [D6] "Texture Streaming Configuration", https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine
- [D7] "Texture Streaming Overview", https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-overview-for-unreal-engine
- [D8] "Memory Insights", https://dev.epicgames.com/documentation/en-us/unreal-engine/memory-insights-in-unreal-engine
- [D9] "Low-Level Memory Tracker", https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-low-level-memory-tracker-in-unreal-engine
- [D10] "Stat Commands", https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine
- [D11] "Unreal Insights Reference" (trace channels), https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-reference-in-unreal-engine-5
- [M1] Microsoft, DXGI_QUERY_VIDEO_MEMORY_INFO, https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/ns-dxgi1_4-dxgi_query_video_memory_info
- [M2] Microsoft, IDXGIAdapter3::QueryVideoMemoryInfo, https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgiadapter3-queryvideomemoryinfo
- [M3] Microsoft, "Residency" (Direct3D 12), https://learn.microsoft.com/en-us/windows/win32/direct3d12/residency
- [M4] Microsoft DirectX blog, S. Pronovost, "GPUs in the task manager", 21 July 2017, https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/

Read only for their entries on pipelines and memory (searched, not read end to end):
- [R55] UE 5.5 release notes, https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-5-release-notes
- [R58] UE 5.8 release notes, https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes

---

## 2b. Unreal 5.x's method for first-use pipeline hitches on D3D12

### What a pipeline is and why its first use hitches
- A pipeline (PSO) bundles the shaders with the draw state the card needs. Creating one on demand "can take 100 or more milliseconds", so it has to be made long before it is used [D3].
- In 5.8, a draw that needs a pipeline that is not in memory starts building it. The command list then waits for that build before it is sent to the card. The wait is a dispatch prerequisite: `RHICmdList.AddDispatchPrerequisite(GraphEvent)` (RHI/Private/PipelineStateCache.cpp, about lines 4780-4845). So a slow build shows up as a wait in the render-submission (RHI) path, not as busy game or render threads.

### Two systems, used together
Unreal has two systems: automatic **PSO precaching**, and the older **bundled PSO cache**. Epic presents precaching as the main system: "the runtime PSO precaching system should be enough", with the bundled cache for "cases where you want to bundle a precreated PSO cache" [D2].

**1. PSO precaching** [D1]
- Covers mesh components. A primitive component requests every pipeline it could need, across all its passes (base, depth, shadow, velocity and so on), straight after loading (PostLoad) [D1]. In 5.8 a static or skinned mesh component created at run time also requests them when it is registered (Components/StaticMeshComponent.cpp line 883; SkinnedMeshComponent.cpp line 948). It requests them again when a mesh or material is set (StaticMeshComponent.cpp line 2401; MeshComponent.cpp lines 110 and 279).
- Pipelines are built on background threads [D1]. By default the pool uses 75% of hardware threads, with at least 2 [D1; PipelineStateCache.cpp lines 383-401].
- **If a pipeline is still building when the component is about to draw:** by default the engine delays the component's render proxy, so the object "skip[s] the draw until the PSO is ready" [D1]. In the 5.8 source this setting is `r.PSOPrecache.ProxyCreationStrategy`: 0 always create, 1 delay (default), 2 draw with the default material meanwhile (Engine/Private/PSOPrecache.cpp lines 34-41). The docs still give the older names, `r.PSOPrecache.ProxyCreationWhenPSOReady` and `...ProxyCreationDelayStrategy`. In 5.8 those are deprecated and converted to the new setting (PSOPrecache.cpp lines 43-92). Note: the old setting's help text says "0 (default)", but its variable starts at 1. Trust the code.
- **Global shaders:** with `r.PSOPrecache.GlobalShaders=1`, every global compute shader is precached at startup. Global graphics pipelines are precached only where Epic wrote a collector: Slate, deferred lights, Cascade particle simulation and volumetric fog [D1]. Other global graphics pipelines, such as most post-process and lighting passes, are not covered. Epic: "Most of the global graphic PSOs are created during the first few frames right after loading ... Using a very small PSO bundled cache to collect these global graphics PSOs can help" [D1].
- **Not covered, or only partly:** components that cannot be delayed (landscape is Epic's example) [D1]. Pass variants that are off by default in the 5.8 settings: dithered LOD fade-out, projected-shadow depth states, light-map policies, TranslucencyAll, and custom depth beyond explicit requests (Engine/Public/PSOPrecacheSettings.h). Materials that do not draw through a mesh pass processor (hair, Nanite, ray-tracing geometry updates) need their own collector [D1]. Nanite programmable-raster and Lumen card pipelines are not made required by default (`bNaniteProgrammableRasterRequired=false`, `bNaniteLumenCardRequired=false`, PSOPrecacheSettings.h). Niagara and Cascade particles are precached at asset load and at component time (`ParticlePrecachingTime=3`). On processors with 6 threads or fewer, they are precached only at proxy creation (BaseEngine.ini, `[/Script/Engine.PSOPrecacheSettingsManager]`). This PC has 12 threads, so the full setting applies.
- **Memory after precaching:** precached pipelines are deleted after they are built. They are then re-created from the driver's own compressed cache, and "the first retrievals ... can take a few milliseconds" [D1]. Options:
  - `D3D12.PSOPrecache.KeepLowLevel` keeps the D3D12 blobs [D1; D3D12RHI/Private/D3D12Pipelinestate.cpp lines 20-26].
  - `r.PSOPrecache.KeepInMemoryUntilUsed` keeps the last N pipelines in memory. In the code it works only on NVIDIA or Qualcomm (`ShouldKeepPrecachedPSOsForIHV`, PipelineStateCache.cpp lines 459-467), so it does nothing on this AMD card.
  - `r.PSOPrecache.KeepInMemoryForActiveMaterials` keeps every precached pipeline for as long as its material is loaded (Engine/Private/PSOPrecacheMaterial.cpp lines 38-44). It is on by default on Windows (Engine/Config/Windows/BaseWindowsEngine.ini, `[ConsoleVariables]`).
- **Loading screen:** Epic "highly recommend[s]" holding the first loading screen until outstanding precache work is done. Use `FShaderPipelineCache::NumPrecompilesRemaining()`, which counts both precaching and the bundled cache [D1].
- **Testing:** use `-clearPSODriverCache` for the first-run experience, and "consistently for all test runs that assess the smoothness of your game. Without it, hitches may be masked by the PSO cache built by the graphics driver" [D1]. Epic also advises limiting cores to a typical count (`-corelimit=n`, `-processaffinity=n`) [D1].
- **Precaching is off in the editor.** `IsPSOPrecachingEnabled()` returns false when the editor is compiled in (PipelineStateCache.cpp lines 4951-4959). Only the packaged game shows how it really behaves.

**2. The bundled PSO cache** [D2]
- Recording: run the packaged game with `-logPSO`. Each run writes `*.rec.upipelinecache` under Saved/CollectedPSOs.
- Converting: copy the stable shader keys (`.shk`) from Saved/Cooked/Windows/<Project>/Metadata/PipelineCaches. Run `UnrealEditor-Cmd <project> -run=ShaderPipelineCacheTools expand <rec files> <shk files> <out>.spc`. The output is named `<prefix>_<Project>_PCD3D_SM6.spc`.
- Bundling: put the `.spc` file in Build/Windows/PipelineCaches and cook again. The cook log must report a graphics pipeline count above 0.
- Prerequisites:
  - `[DevOptions.Shaders] NeedsShaderStableKeys=true` in the Engine ini.
  - `bShareMaterialShaderCode=True` and `bSharedMaterialNativeLibraries=True` in DefaultGame.ini.
  - `r.ShaderPipelineCache.Enabled=1`.
  - Once the cache is enabled, compute pipelines are added automatically at cook time [D2].
- At startup the file opens and compilation begins. `r.ShaderPipelineCache.StartupMode` sets how: 0 paused, 1 fast (default), 2 background, 3 precompile mask [D2; RenderCore/Private/ShaderPipelineCache.cpp lines 55-63]. Batch size and time per frame are set by `r.ShaderPipelineCache.BatchSize`/`BatchTime` (defaults 50 and 16 ms) and `BackgroundBatchSize`/`BackgroundBatchTime` (1 and 0) (ShaderPipelineCache.cpp lines 66-113).
- Checking coverage: the log should say "Opened FPipelineCacheFile ... with N entries". During play there should be no "Encountered a new graphics PSO" lines [D2].
- Epic's own rule: "never measure the performance of a build that does not have an up-to-date cache, or at least don't use those measurements in comparisons" [D2].

**How the two work together in 5.x**
- `r.ShaderPipelineCache.ExcludePrecachePSO=1` records only pipelines that precaching missed. The docs say this needs `r.PSOPrecache.Validation` [D2; RHI/Private/PipelineFileCache.cpp lines 133-139].
- `r.ShaderPipelineCache.PSOPrecacheIncludeMode` (default 2) controls which bundled entries are built: only those that were not precached when recorded (Missed, Untracked or Too late), plus every global-shader pipeline (ShaderPipelineCache.cpp lines 191-199).
- `r.ShaderPipelineCache.OnlyOpenUserCache` ships no bundled cache but still keeps a per-user cache [D2]. In 5.8 the user cache is saved by default only in Shipping builds (`SaveUserCache = ... && UE_BUILD_SHIPPING`, PipelineFileCache.cpp lines 157-162).

### Finding which pipeline missed
- **The CSV profile we already capture:**
  - `PSO/PSOMisses` and `PSO/PSOComputeMisses` count every first use of a pipeline that was not in memory, whether or not it was precached (PipelineStateCache.cpp lines 4094-4111 and 4816-4819). A count of 1 does not mean "not precached".
  - The event "PSO/Encountered new graphics PSO", and the log line "Encountered a new graphics PSO: <hash> (PSOPrecacheState: <state>)", are written only when precaching did not finish that pipeline (PipelineFileCache.cpp lines 3480-3505).
  - `PSO/GraphicsPSOHitch` and `PSO/GraphicsPSOHitchTime` record any run-time pipeline build over `r.PSO.RuntimeCreationHitchThreshold` (20 ms) [D1; PipelineStateCache.cpp lines 195-200 and 300-325]. The timed region is the driver build alone, `RHICreateGraphicsPipelineState` (lines 3923-3925).
- **Log:**
  - `-logpsodetails` prints each new pipeline's full readable description (PipelineFileCache.cpp lines 3135-3147). `r.ShaderPipelineCache.PrintNewPSODescriptors=1|2` does the same (lines 147-153).
  - The log category `LogPSOHitching` at Verbose names each run-time build over 20 ms, with its precache state. In Development builds it also gives the render breadcrumb path (PipelineStateCache.cpp lines 315-336; breadcrumbs exist in Development, RHI/Public/RHIBreadcrumbs.h line 26).
- **Validation:** `r.PSOPrecache.Validation` is 0 by default; 1 gives light counters; 2 gives full counters plus a "PSO PRECACHING MISS" log block naming the material, vertex factory, mesh pass and shader hashes [D1; Engine/Private/PSOPrecacheValidation.cpp lines 48-57]. It is read-only, so it must be set at startup (ini). `stat PSOPrecache` shows the counters [D1]. The result states mean [D1]:
  - Missed: never requested.
  - Too late: requested, but not ready in time.
  - Untracked: outside precaching (for example global shaders).
- **Unreal Insights:** add the timers "PSOPrecache: Missed" and "PSOPrecache: Too Late" to the frame view [D1]. The engine emits these scopes, with the pass and resource names nested inside where known (PipelineStateCache.cpp lines 3742-3771).

### What is new in 5.4 and later (as far as reached)
- 5.5 added asynchronous pipeline-cache consolidation, on by default (`r.pso.EnableAsyncCacheConsolidation`) [R55].
- 5.8 stopped precaching wave-op pipelines on cards that cannot use them, fixed a "PSO check with grooms", and reworded `r.PSOPrecache.GlobalShaders` after a "dynamic shader preloading" refactor [R58]. The source has a new `r.PSOPrecache.Mode` (0 full pipelines, the default; 1 preload shaders only) (PSOPrecache.cpp lines 110-116).
- 5.8 made `stat unit` show the card's memory used and budget on discrete cards [R58].
- The proxy-strategy rename above is in the 5.8 source. Which version introduced it was not found (unverified).

---

## 2b, part 3. FlushAsyncLoading during play

- **What causes it:**
  - `LoadObject` / `StaticLoadObject` first looks for the object in memory. If it is absent, it calls `LoadPackage` (CoreUObject/Private/UObject/UObjectGlobals.cpp, StaticLoadObjectInternal, from line 1409).
  - A synchronous `LoadPackage` queues the package on the async loader, then calls `FlushAsyncLoading(RequestID)`. This blocks the calling thread until that package and everything it needs are loaded (UObjectGlobals.cpp lines 1740-1765).
  - Older load paths go through `BeginLoad`, which flushes all async loading (lines 1890-1901).
  - Each flush records the CSV event "FlushAsyncLoading", a CSV timing stat and an Insights scope of the same name. When other loading is in progress, it also logs "FlushAsyncLoading(<id>): N QueuedPackages, M AsyncPackages" (CoreUObject/Private/Serialization/AsyncPackageLoader.cpp lines 275-303).
- **Why it hitches:** the game thread stops until the disk read, deserialising and PostLoad are done. Epic: a synchronous load "may be fine for smaller objects, but it could potentially stall your main thread for too long" [D4]. A second, less obvious cost: what was just loaded is drawn at once. Its components request their pipelines at PostLoad or registration, a frame or two before the first draw. That is too little time for precaching.
- **The professional fix:**
  - Hold soft references (`TSoftObjectPtr` / `FSoftObjectPath`). Load them ahead of need with `FStreamableManager::RequestAsyncLoad` and a completion callback [D4].
  - Or use the Asset Manager: Primary Assets and Asset Bundles, loaded with `LoadPrimaryAssets` at a chosen moment such as a loading screen [D5].
  - Keep a hard reference to anything that must stay loaded [D4].
  - The loading screen should then also wait for precaching to finish (above) [D1].
- **Finding what was loaded:**
  - Insights with `-trace=default,loadtime` gives package load events, including "LoadPackageInternal" with metadata [D11].
  - Each synchronous load also carries an IO-activity tag "Sync <package>" (UObjectGlobals.cpp line 1763).
  - In Development builds, `TrackAsyncLoadRequests.Enable=1` records the call stack of every load request. With the default `TrackAsyncLoadRequests.DumpAfterCsvProfiling=1`, it writes them to Saved/Profiling/AsyncLoadRequests_*.log when the CSV capture ends (AsyncPackageLoader.cpp lines 364-401). That file is written after every walk today, but it is empty ("Captured 0 unique callstacks") because tracking is off.
- **This project:** the C++ has about 60 synchronous load calls (`LoadObject` and the like), some of them during play. Examples: CrimeProbe.cpp lines 2790, 3996 and 7723; SliceCharacter.cpp lines 264-348. There is no async loading or Asset Manager use (grep of ue-probe/Source, 23 October).

---

## 2c. What this project's packaged build has on, and why the miss still happens

**Project files** (ue-probe/Config: DefaultEngine.ini, DefaultGame.ini, DefaultScalability.ini, DefaultInput.ini; no platform folder). None of them sets any pipeline, precache or pipeline-cache setting. All values below are the engine's, confirmed in the source or ini and, where marked, in the walk's log.

| Setting | Value in our package | Where it comes from |
|---|---|---|
| `r.PSOPrecaching` | 1 (on; D3D12 supports it) | PipelineStateCache.cpp line 211; D3D12RHI.cpp line 248 |
| `r.PSOPrecache.Components` / `.Resources` | 1 / 0 | PSOPrecache.cpp lines 18-31 |
| `r.PSOPrecache.ProxyCreationStrategy` | 1 (delay the draw) | PSOPrecache.cpp line 34 |
| `r.PSOPrecache.GlobalShaders` | 1 | BaseWindowsEngine.ini; log: "Set CVar [[r.PSOPrecache.GlobalShaders:1]]" |
| `r.PSOPrecache.KeepInMemoryForActiveMaterials` | 1 | BaseWindowsEngine.ini; log line at 13:30:52 UTC |
| `r.PSOPrecache.KeepInMemoryUntilUsed` | 0 (and ignored on AMD) | PipelineStateCache.cpp lines 430-467 |
| `r.PSOPrecache.Validation` | 0 (off: no miss details, `stat PSOPrecache` empty) | PSOPrecacheValidation.cpp line 47 |
| `r.PSOPrecache.Mode` | 0 (full pipelines) | PSOPrecache.cpp line 110 |
| `r.AsyncPipelineCompile` | 1 (all builds async) | PipelineStateCache.cpp lines 159-165 |
| `r.PSO.RuntimeCreationHitchThreshold` | 20 ms | PipelineStateCache.cpp lines 195-200 |
| Precache settings row | PCD3D_SM6, all defaults (12 threads > 6) | BaseEngine.ini, PSOPrecacheSettingsManager |
| `r.ShaderPipelineCache.Enabled` / `.LogPSO` | 1 / 1 (on in any non-editor build) | PipelineFileCache.h line 19; PipelineFileCache.cpp lines 113-125 |
| Bundled cache file | **none** | log: "Could not open FPipelineCacheFile: ../../../LedgerProbe/Content/PipelineCaches/Windows/LedgerProbe_PCD3D_SM6.stable.upipelinecache"; no Build/Windows/PipelineCaches folder; nothing in the package manifest |
| `NeedsShaderStableKeys` | not set (off) | DefaultEngine.ini |
| `bShareMaterialShaderCode` / `bSharedMaterialNativeLibraries` | True / **False** (the bundled cache needs True) | BaseGame.ini lines 115-116; DefaultGame.ini sets neither |
| `r.ShaderPipelineCache.SaveUserCache` | 0 in Development | PipelineFileCache.cpp lines 157-162 |
| `D3D12.PSO.DiskCache` / `.DriverOptimizedDiskCache` | 0 / 0 | log: "Not using pipeline state disk cache ..." |
| `D3D12.PSOPrecache.KeepLowLevel` | 0 | D3D12Pipelinestate.cpp line 20 |
| `r.NumBufferedOcclusionQueries` | 3 (the project's, 21 October) | DefaultEngine.ini |

**What the walk at 15:31 on 23 October shows** (measured: log plus CSV, build fd4003b):
- **During loading,** before the walk's capture begins, about 100 pipelines are first used without precaching. The log has 70 at 13:31:03 UTC and 30 at 13:31:04 UTC, all "(PSOPrecacheState: Missed)". In all: 104 graphics and 1 compute in this run, 107 and 1 in the standing run before it, and 113 and 1 in the nightly route walk.
- **At 5.42 s** (CSV row 393): the event "FlushAsyncLoading" fires. The log says "FlushAsyncLoading(356): 1 QueuedPackages, 0 AsyncPackages", which is one synchronous load request. The flush itself took 0.34 ms (`Exclusive/GameThread/FlushAsyncLoading`).
- **At 5.46 s** (row 394): "Encountered a new graphics PSO: 1109700143 (PSOPrecacheState: **Missed**)", with PSOMisses=1. So precaching had never requested this pipeline.
- **Row 395:** `PSO/GraphicsPSOHitch`=1 and `PSO/GraphicsPSOHitchTime`=**66.3 ms**. The driver took 66 ms to build that one pipeline. In the same row the game thread waited 61.5 ms and the render thread 46.2 ms (`Exclusive/.../EventWait`).
- **Row 396:** a frame time of **69.4 ms**, the run's worst frame. Its game (8.5), render (11.9), RHI (4.0) and card (13.8 ms) times are all normal. The time went on waiting for the pipeline.
- **Other misses in the same walk did not hitch.**
  - Row 1: 2 misses. Its frame is 6.9 ms; the capture's first frame, just before it, is 26.6 ms.
  - Row 257: 8 graphics and 4 compute misses, of which only 2 graphics were "new"; the worst frame near it is 18.5 ms.
  - Rows 297, 1337 and 1409: no frame near them is over 17 ms.
  - Pipelines that were precached come back fast, whether from memory or from the driver's cache. The one never requested did not.
- The PC had run this game many times before, so the driver's cache was warm. The never-requested pipeline still took 66 ms. Why the AMD driver's cache did not shorten it was not found (unverified).

**Why the miss still happens (2c's answer):**
1. The pipeline is outside what precaching requests ("Missed", not "Too late").
2. The project ships no bundled cache to catch what precaching misses. Epic names that cache as the remedy for exactly this, global graphics pipelines in particular [D1, D2].
3. Validation is off, so neither the log nor `stat PSOPrecache` names the material, pass or shader.
4. The miss comes right after a synchronous load. So whatever needs it is new, and too late for any warm-up.

---

## 1c. Setting and measuring a card-memory budget

**The budget comes from Windows, per process.**
- `IDXGIAdapter3::QueryVideoMemoryInfo` reports a **Budget** ("the OS-provided video memory budget ... that the application should target") and the process's **CurrentUsage**. Above the budget, "the application may incur stuttering" [M1]. Processes over budget "are intermittently frozen and paged-out" [M2].
- The budget "can fluctuate noticeably as background processes wake-up and sleep" [M3]. So other programs on the card shrink what the game may safely use.

**How Unreal uses it on D3D12** (WindowsD3D12Device.cpp lines 1832-1870):
- At startup it reads the Budget and takes 90% of it as its "total graphics memory".
- It sets the texture pool to `PoolSizeVRAMPercentage` of that figure (70%, BaseWindowsEngine.ini `[TextureStreaming]`). That applies only while `r.Streaming.PoolSize` is -1 (Engine/Private/Streaming/StreamingManagerTexture.cpp lines 1817-1843).
- Our log: "Texture pool is 5938 MB (70% of 8484 MB)". Then the High texture quality from the engine's BaseScalability.ini (`[TextureQuality@2]`: `r.Streaming.PoolSize=800`, `r.Streaming.LimitPoolSizeToVRAM=1`) replaced it: "Texture pool size now 800 MB".
- The pool holds UI, never-streamed and streamed textures [D6]. The streamer drops mips to fit [D7].
- `D3D12.AdjustTexturePoolSizeBasedOnBudget` (shrink the pool when over budget) is 0 (D3D12Texture.cpp line 23).

**The engine's own accounting, already in our CSV every frame.** `GPUMem/LocalBudgetMB` and `GPUMem/LocalUsedMB` are DXGI's Budget and CurrentUsage for the game process (RHI/Private/RHIStats.cpp lines 66-97; RHICore/Private/DXGIUtilities.cpp lines 56-69). Walk at 15:31, 23 October:
- Budget 9,427 MB. Game used: median 4,888 MB, peak 5,528 MB.
- Partial breakdown, from the CSV's own columns (median or held value):
  - render-target pool: 1,276 MB;
  - non-streaming texture mips (`TextureStreaming/NonStreamingMips`): **1,738 MB**;
  - streamed textures: 59 MB median, 185 MB peak, in an 800 MB pool;
  - transient render-graph memory: 256 MB median, 896 MB peak;
  - distance-field atlas: 256 MB, plus 16 MB indirection;
  - always-resident ray-tracing geometry: **120.6 MB**, although ray tracing is off for the street.
- The rest (buffers, the GPU scene, Lumen's surface cache, shadows) is not broken out in the CSV.

**Tools that say what fills it:**
- `stat RHI`: render-target, texture, buffer and uniform-buffer memory pools (RHI/Public/RHIStats.h lines 149-176) [D10].
- `stat D3DMemory`: budget, used, available, demoted (RHIStats.h lines 213-218).
- `stat D3D12Resources`, `stat D3D12Memory` and `stat D3D12MemoryDetails` (D3D12RHI/Private/D3D12Stats.h).
- `stat RenderTargetPool`, `stat Streaming`, `stat StreamingDetails`, `stat TextureGroup` [D10].
- `rhi.DumpMemory`, in builds with stats (RHI/Private/RHI.cpp line 109).
- `rhi.DumpResourceMemory [N] [summary] [Name=] [Type=] [csv]`: every RHI resource by size. Compiled into Development, not Shipping (RHI.cpp line 1037; RHI.Build.cs lines 30-34).
- `r.DumpRenderTargetPoolMemory` (RenderCore/Private/RenderTargetPool.cpp line 125).
- Memory Insights with `-trace=default,memory` on a Development package. It keeps video memory as its own root heap on desktop [D8].
- LLM: `-llm`, `-LLMCSV`, `stat LLMFULL` [D9].
- Feature pools to read alongside:
  - Nanite streaming pool, `r.Nanite.Streaming.StreamingPoolSize`, default 512 MB (Engine/Private/Rendering/NaniteStreamingManager.cpp line 57);
  - Lumen's surface-cache atlas, 4096 at our High (DefaultScalability.ini);
  - virtual shadow map pages, `r.Shadow.Virtual.MaxPhysicalPages` (its default was not read).

**Windows' counters** [M4]:
- Task Manager and the GPU counters are fed by the Windows video memory manager itself.
- A process's Dedicated Usage includes memory it shares with other processes. So "adding the memory utilized by each individual process will sum up to an amount ... larger than that utilized by the GPU".
- The adapter's total (the Performance tab; the `GPU Adapter Memory\Dedicated Usage` counter that tools/p1-packaged.ps1 reads) is the true card total.

**What the 6 GB line means.** PLAN.md (line 46) reads "dedicated memory 6 GB with the voice on the card". Under the method above, a budget is set for what our own processes allocate, against the OS budget on the target card, with room left for what else Windows runs.
- With the voice now on the processor, the measure to hold against the line is the game process's own usage: DXGI CurrentUsage, the CSV's `GPUMem/LocalUsedMB`, which is close to the game's per-process counter.
- The adapter total measures how quiet the PC is.
- This is a reading for the session to record, not a ruling.

---

## What this means for our stall (ranked)

1. **A pipeline that precaching never requested, built on first use at 5.46 s.** Established for the 23 October 15:31 walk. The 69 ms frame is a 66 ms driver build of one "Missed" graphics pipeline. The game and render threads wait for it. This matches the 22 October review's "PSOMisses=1" at the same moment; that it is the same pipeline in the older runs is a lead. Epic's fix, in order:
   - Name the pipeline: `r.PSOPrecache.Validation=2` set in the ini, `-logpsodetails`, `LogPSOHitching` at Verbose, or the Insights scope "PSOPrecache: Missed".
   - If it is a material pass that a default setting leaves out, switch that pass on (for example `r.PSOPrecache.DitheredLODFadingOutMaskPass`, `ProjectedShadows`, `TranslucencyAll`, `CustomDepth`).
   - If it is a global graphics pipeline, or anything else precaching cannot reach, ship a small bundled cache recorded with `-logPSO`, and let it compile before the walk starts.
2. **The synchronous load just before it.** Established as the trigger's position; the cause is a lead. One package is loaded on the game thread at 5.42 s. It costs only 0.3 ms, but whatever it brings is drawn at once, with no time to warm. Fix: find it (`TrackAsyncLoadRequests.Enable=1`, or `-trace=default,loadtime`). Then load it ahead with `RequestAsyncLoad` or the Asset Manager, while the street loads, so its pipelines are built before the walk.
3. **About 100 never-requested pipelines at every start.** Measured; whether they cost anything is a lead. They fall before the capture starts, so the walk does not see them, but a player would. Fix: the same bundled cache, plus a loading screen that waits until `FShaderPipelineCache::NumPrecompilesRemaining()` reaches 0 [D1].
4. **The 80 ms wait followed by compute and graphics misses (frame 1221, 22 October).** A lead, same kind. That capture was not reached today. The compute half would be covered too: once the bundled cache is enabled, compute pipelines are added at cook [D2].
5. **Our tests run on a warm driver cache.** Established as method. Epic asks for `-clearPSODriverCache` on every smoothness run [D1]. Our walks never used it, so first-run hitches may be larger than measured. Repeats with it are needed before claiming "every frame under 33.3 ms".
6. **Card memory leads** (1c). The game alone used a median of 4.9 GB and a peak of 5.5 GB on 23 October, under 6 GB. The biggest single block it can change is 1.74 GB of textures that never stream. Next are 1.28 GB of render targets and 121 MB of ray-tracing geometry kept although ray tracing is off. Which textures, and why they do not stream: `rhi.DumpResourceMemory` and `stat StreamingDetails` will say (a lead).

## Not reached, or unconfirmed
- Epic's tech blog "Game engines and shader stuttering: Unreal Engine's solution to the problem" (unrealengine.com). A bot-check page, then HTTP 403. It was not bypassed and not read.
- The 5.4, 5.6 and 5.7 release notes. The pages came back empty (5.7 showed 5.8's title). So the version that introduced `ProxyCreationStrategy` is unknown.
- The pages "Asset Loading Insights" and "Timing Insights" came back empty.
- The 21-22 October walk captures and walk-b414e8c.utrace were not found or opened. Only today's 15:31 run was measured, and the packaged build was fd4003b, not 35e10a9.
- Why a never-requested pipeline takes 66 ms on a PC with a warm AMD driver cache (Adrenalin 26.10.1): not researched; unverified.
- Whether MetaHuman hair (groom) pipelines are precached in 5.8: unverified. The CSV shows groom components ticking.
- Whether `-dpcvars` can set read-only settings such as `r.PSOPrecache.Validation`: unverified. Setting them in the ini is sure.
- What `memreport -full` includes on D3D12: not read in a primary source.
- A Microsoft page describing the `GPU Process Memory` and `GPU Adapter Memory` counter sets themselves: not found. The DirectX blog [M4] was used instead.
