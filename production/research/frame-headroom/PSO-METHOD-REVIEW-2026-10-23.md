# Review of PSO-AND-VRAM-METHOD-2026-10-23.md, pipeline part (23 October 2026)

Fresh reviewer. This checks the facts that the two-step plan relies on: naming the missed pipeline, then a precache setting or Epic's bundled cache. The card-memory part (1c) was not reviewed.

## Sources and when they were read
- Engine source, UE 5.8.2, C:/Program Files/Epic Games/UE_5.8/Engine/Source. Read 23 Oct 2026. Paths below are relative to that folder unless they say otherwise.
- [D1] PSO Precaching, [D2] Creating a Bundled PSO Cache, [D3] PSO Caches (all labelled 5.8 docs). Fetched 23 Oct 2026. Limitation: the fetch tool returns a summary with short quotes, not the raw page, so these pages were not read word for word. Anything that rests on the docs alone is marked that way.
- Project files, read 23 Oct 2026: ue-probe/Config/DefaultEngine.ini, ue-probe/Config/DefaultGame.ini, .gitignore, tools/p1-packaged.ps1, .github/workflows/ledger-probe-unreal.yml, and the packaged game's log (F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Logs/LedgerProbe.log).
- The AMD driver cache folders under %LOCALAPPDATA%, listed 23 Oct 2026.

## Step 1: naming the missed pipeline

1. **`r.PSOPrecache.Validation`: confirmed.**
   - Default 0. Value 1 gives light counters; value 2 gives full counters and the miss log. It is read-only (Runtime/Engine/Private/PSOPrecacheValidation.cpp 47-56).
   - It is compiled into a packaged Development game (Runtime/Engine/Public/PSOPrecacheFwd.h 22). The material, vertex-factory and pass detail in the miss log needs tracking, which is on in Development and off in Shipping and Test (PSOPrecacheValidation.h 15).
   - The value is read on every use, never cached (PSOPrecacheValidation.cpp 157-180). So a value set at startup holds for the whole run.

2. **The `-ini:Engine:[SystemSettings]:r.PSOPrecache.Validation=2` override: confirmed.**
   - This is the engine's own command-line syntax (Runtime/Core/Private/Misc/ConfigCacheIni.cpp 2317-2410, with its markers at 1714-1724). It works in every build except Shipping (ConfigCacheIni.h 57).
   - The engine applies the Engine ini's [SystemSettings] section at Runtime/Launch/Private/LaunchEngineLoop.cpp 2814. The renderer starts later, at line 3171.
   - "Read-only" only blocks typing the setting at the console (Runtime/Core/Private/HAL/ConsoleManager.cpp 3221-3223). Values from an ini are not checked for read-only (Runtime/Core/Private/Misc/ConfigUtilities.cpp 322-366).
   - Check: the log should show `Set CVar [[r.PSOPrecache.Validation:2]]`.
   - **The note's line 231 is now settled: `-dpcvars` also reaches read-only settings.** It uses the same path (Runtime/Engine/Private/DeviceProfiles/DeviceProfileManager.cpp 719-775, not in Shipping) and is applied before the renderer starts (LaunchEngineLoop.cpp 2857). tools/p1-packaged.ps1 already passes `-dpcvars` (line 84), so adding the setting there is the simplest route.

3. **`-logpsodetails`: confirmed, but it gives shader hashes, not names.**
   - It works outside Shipping (Runtime/RHI/Private/PipelineFileCache.cpp 3135-3147). It prints the full description only for pipelines that precaching did not finish (3480-3500).
   - The description lists shader hashes, not shader names. Turning a hash into a name needs the cook's `.shk` files, which exist only if NeedsShaderStableKeys was on for that cook. The commandlet then does it: `ShaderPipelineCacheTools dump <file>.shk -outputhash=<hash>` (Editor/UnrealEd/Private/Commandlets/ShaderPipelineCacheToolsCommandlet.cpp 2964).
   - D1 does not mention this option.

4. **`-LogCmds="LogPSOHitching Verbose"`: confirmed.**
   - The log category is compiled in at every level and logs at Log by default (Runtime/RHI/Private/PipelineStateCache.cpp 46). The hitch line is Verbose and is written for any run-time pipeline build over 20 ms (195-200, 310-336).
   - `-LogCmds` is read in every build except Shipping (Runtime/Core/Private/Logging/LogSuppressionInterface.cpp 516-519).
   - For a pipeline that precaching never requested, the "Resource" and "Pass" fields come out as "Unknown". Only the breadcrumb path places it (PipelineStateCache.cpp 4827-4835).
   - `r.RDG.Events=3` adds render-graph pass names to the breadcrumbs (Runtime/RenderCore/Private/RenderGraphPrivate.cpp 276-284). Whether that improves this particular line is unverified.

5. **The plan misses this: Validation does not name every miss.**
   - The "PSO PRECACHING MISS" block is written only from certain callers:
     - mesh draw commands (Runtime/Renderer/Private/MeshPassProcessor.cpp 1283-1286);
     - decals (PostProcessDeferredDecals.cpp 771);
     - lights (LightRendering.cpp 2940);
     - translucent lighting (TranslucentLighting.cpp 2061);
     - Nanite (NaniteCullRaster.cpp 3535, 3649);
     - volumetric fog (VolumetricFog.cpp 1003);
     - Slate (SlateRHIRenderingPolicy.cpp 1425, 1474).
   - A post-process or other global graphics pipeline gets no block. The engine's "Missed" only means "not on the precache list" (PipelineStateCache.cpp 3127-3131), so such a pipeline still shows as "Missed".
   - So if no block appears for the pipeline at 5.46 s, treat it as a global pipeline and name it from the LogPSOHitching breadcrumbs. The answer is then the bundled cache, not a precache setting.

6. **`TrackAsyncLoadRequests.Enable=1`: confirmed, but the plan does not say how to set it.**
   - The setting exists in Development, defaults to 0 and is an ordinary setting, not read-only (Runtime/CoreUObject/Private/Serialization/AsyncPackageLoader.cpp 28, 364-369).
   - When the CSV capture ends, it writes Saved/Profiling/AsyncLoadRequests_<time>.log (398-401, 516-539).
   - Set it with `-dpcvars=TrackAsyncLoadRequests.Enable=1`.
   - Synchronous loads are recorded too, with priority 2147483647 (UObjectGlobals.cpp 1751-1764). That number is how to pick them out.
   - Package names are printed even without symbols. The package also ships LedgerProbe.pdb (Binaries/Win64), so the call stacks should resolve.

7. **`-clearPSODriverCache` on D3D12 with an AMD card: confirmed, with an open question.**
   - When the renderer starts, it deletes the files in %LOCALAPPDATA%\AMD\DxCache, %LOCALAPPDATA%\AMD\DxcCache, LocalLow\AMD\DxCache and LocalLow\AMD\DxcCache (Runtime/D3D12RHI/Private/Windows/WindowsD3D12Device.cpp 1201-1245, 1388-1391). It deletes files only, not subfolders.
   - On this PC those folders hold only files. AMD\DxcCache was last written at 15:29-15:30 on 23 Oct, during the walk.
   - On AMD it does not touch %LOCALAPPDATA%\D3DSCache; it clears that folder only on Qualcomm.
   - Unverified:
     - whether Adrenalin 26.10.1 also keeps DX12 pipelines in D3DSCache;
     - whether a game started from this session (a packaged app, per the memory note on private AppData writes) deletes the real folders or a private copy.
   - Check: after a cleared start, the file count in AMD\DxcCache should drop, seen from the runner or from Explorer.

8. **The plan misses this: the diagnostic run disturbs the timing.**
   - Validation=2, `-logpsodetails` and the load-request call-stack capture all add work (AsyncPackageLoader.cpp 486-498).
   - `-clearPSODriverCache` makes every pipeline build cold.
   - So keep the naming run separate from the walk that is measured.

## Step 2: a precache setting, or the bundled cache

9. **`r.PSOPrecache.ProjectedShadows`: confirmed, with conditions.**
   - It exists, defaults to -1 (the engine's default, which is off) and is read-only (Runtime/Engine/Private/PSOPrecacheSettings.cpp 115-124).
   - It is read once and then kept (252-277), so it must be set at startup: [SystemSettings] in DefaultEngine.ini, or `-dpcvars` for a test.
   - It only acts when virtual shadow maps are off (Runtime/Renderer/Private/DepthRendering.cpp 921). The code default for `r.Shadow.Virtual.Enable` is 0 (VirtualShadowMaps/VirtualShadowMapArray.cpp 161-162), and no project or engine ini sets it, so the setting would act here. This is worked out from the config; no log line shows it.
   - **Wrong in the note (line 216):** the setting is `r.PSOPrecache.TranslucencyAllPass`, not "TranslucencyAll" (PSOPrecacheSettings.cpp 51-60).
   - `r.PSOPrecache.CustomDepth` defaults to mode 1, which already covers components that ask for custom depth.
   - All of these per-pass settings are read-only and read once. They can also be set per platform in [/Script/Engine.PSOPrecacheSettingsManager] (Engine/Config/BaseEngine.ini 3970-3981). D1 names none of them.

10. **`[DevOptions.Shaders] NeedsShaderStableKeys=true`: confirmed.**
    - It goes in the Engine ini or in Config/Windows/WindowsEngine.ini (Editor/UnrealEd/Private/Cooker/ShaderLibraryCooking.cpp 260-279). D2 says the same.
    - It only takes effect when the shared shader library is in use (line 256).

11. **`bShareMaterialShaderCode=True`: confirmed as needed, and already on.**
    - It is the engine default (Engine/Config/BaseGame.ini 116). The packaged log shows "Loaded Shared Shader Library LedgerProbe".
    - The run-time cache exists only when the library is on (Runtime/RenderCore/Private/ShaderPipelineCache.cpp 766-775).

12. **`bSharedMaterialNativeLibraries=True`: overstated (note line 134, "the bundled cache needs True").**
    - D2 lists it. In 5.8 it changes only Apple (Metal) shaders: the code that reads it is Metal-only (RenderCore/Private/Shader.cpp 2258-2274; Engine/Private/ShaderCompiler/ShaderCompiler.cpp 3750-3768).
    - Native archives need a shader format that supports them. The default is no (Developer/TargetPlatform/Public/Interfaces/IShaderFormat.h 64), and only Metal says yes (MetalShaderFormat.cpp 185).
    - On Windows it is harmless and not needed.

13. **`r.ShaderPipelineCache.Enabled`: confirmed; there is no need to set it.**
    - It defaults to 1 in every build that is not the editor (Runtime/RHI/Public/PipelineFileCache.h 19; PipelineFileCache.cpp 112-117).
    - A Development build opens the bundled cache at startup (LaunchEngineLoop.cpp 3197-3205, 3668). Today's log already shows it trying: "Could not open FPipelineCacheFile ... LedgerProbe_PCD3D_SM6.stable.upipelinecache".
    - D2's step "set it to 1" is already met.

14. **`-logPSO` in a Development build: confirmed.**
    - It switches on the recording of every pipeline used (ShaderPipelineCache.cpp 143-148, 202-212). D3D12 keeps the file cache alongside precaching (Runtime/D3D12RHI/Private/D3D12RHI.cpp 247).
    - The file lands in the package's own Saved folder: F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/CollectedPSOs/<branch>-CL-<number>-LedgerProbe_PCD3D_SM6_<id>.rec.upipelinecache (PipelineFileCache.cpp 2288-2292).
    - The log prints "Base name for record PSOs is ...".

15. **The plan misses this: the recording is written only when the game exits cleanly.**
    - Automatic saving is off in 5.8 (ShaderPipelineCache.cpp 114-119 and 135-141).
    - The file is written in three cases:
      - when the engine exits (LaunchEngineLoop.cpp 5141, then ShaderPipelineCache.cpp 1785-1796 and 968-978);
      - on the console command `r.ShaderPipelineCache.Save` (231-241, 276-280);
      - when the app is deactivated (665-675).
    - The walk's `-ExitAfterCsvProfiling` exits cleanly by default (Runtime/Core/Private/ProfilingDebugging/CsvProfiler.cpp 4309-4312; csv.ForceExit defaults to 0, 117-122).
    - But tools/p1-packaged.ps1 kills the game if it is still running after 8 minutes (lines 99-102). A killed run leaves no file. Check that the file exists after each recording run.

16. **The `.shk` files and the expand command: confirmed.**
    - The cook writes them to Saved/Cooked/Windows/LedgerProbe/Metadata/PipelineCaches as ShaderStableInfo-Global-PCD3D_SM6.shk and ShaderStableInfo-LedgerProbe-PCD3D_SM6.shk (ShaderLibraryCooking.cpp 583-592; RenderCore/Private/ShaderLibrary/ShaderCodeLibraryUtilities.cpp 100).
    - The command is `UnrealEditor-Cmd.exe <LedgerProbe.uproject> -run=ShaderPipelineCacheTools expand <*.rec.upipelinecache> <*.shk> <name>.spc`. Wildcards are expanded and the output name must end in .spc (ShaderPipelineCacheToolsCommandlet.cpp 100-125, 1110-1117, 2896-2902).
    - Pass both `.shk` files, taken from the same cook as the package that made the recording.
    - The commandlet is an Unreal editor process, so it must not overlap a runner build.

17. **The `.spc` name and folder: confirmed, with an exact name.**
    - The cook searches the project's Build/Windows/PipelineCaches folder for `*LedgerProbe_PCD3D_SM6.spc` (ShaderLibraryCooking.cpp 436-438). So the file name must end exactly in `LedgerProbe_PCD3D_SM6.spc`.
    - From it the cook builds Content/PipelineCaches/Windows/LedgerProbe_PCD3D_SM6.stable.upipelinecache (470-480). That is the file the game looks for (PipelineFileCache.cpp 2196).
    - The cook log should show "Running UShaderPipelineCacheToolsCommandlet". D2 adds a line "Wrote N binary PSOs (graphics: X ...)", whose graphics count must be above 0; that line comes from the docs only.

18. **The plan misses this: as things stand the `.spc` will not reach the build machine.**
    - ue-probe/Build/ is ignored by git (.gitignore line 109), and the cooks run on the runner from the repository.
    - The `.shk` files are also in the runner's own copy: ledger-local has no Saved/Cooked folder (checked 23 Oct).
    - The plan must say two things:
      - how the `.spc` gets to the runner: un-ignore Build/Windows/PipelineCaches and commit the file, which the 1 MB push guard allows only if it is small enough; or stage it from F:, as the street meshes are;
      - where the `.shk` files are fetched from.
    - The size of the `.spc` is unverified.

19. **Stable keys at cook time: confirmed that nothing else is needed on Windows beyond items 10 and 11.**
    - Each material's keys are written when that material is saved during the cook (Runtime/Engine/Private/Materials/Material.cpp 3128-3133; MaterialInstance.cpp 3479). So the first cook after switching the setting on must save every material again: a full cook, not an incremental one.
    - Unverified: whether `BuildCookRun -cook`, as the workflow calls it (ledger-probe-unreal.yml 566-569), does a full cook in 5.8.
    - Check the cook log for "Saved scl.csv ... ShaderStableInfo-LedgerProbe-PCD3D_SM6.shk" and the file's size.

20. **Compute pipelines: wrong (note lines 61 and 220).**
    - By default the cook adds only Niagara compute pipelines: `r.ShaderPipelineCacheTools.IncludeComputePSODuringCook` defaults to 2, "adds only Niagara PSOs" (ShaderPipelineCacheToolsCommandlet.cpp 73-79, 2199-2219).
    - Other compute pipelines get into the cache only if a recording caught them.

21. **`FShaderPipelineCache::NumPrecompilesRemaining()`: confirmed, with two cautions.**
    - It counts the bundled cache's remaining work plus every active precache request. It stays at 1 or more while a cache file is being worked through (ShaderPipelineCache.cpp 864-890; PipelineStateCache.cpp 5167-5175).
    - The cache compiles on the render thread, one batch per frame: in fast mode, 50 pipelines or 16 ms (ShaderPipelineCache.cpp 72-101, 1733-1752). So the wait must check once per frame, not loop and block.
    - A count of 0 covers only what is known at that moment. Precaching for anything loaded later, such as the synchronous load at 5.42 s, starts later.

22. **`r.ShaderPipelineCache.StartupMode` value 3: wrong for the 5.8 code (note line 62).**
    - The setting's help text lists 0 to 2, and the code treats any other value as 1 (ShaderPipelineCache.cpp 55-63, 1733-1752). D2 still lists 3.
    - The plan does not use it.

23. **`r.ShaderPipelineCache.PSOPrecacheIncludeMode`, default 2: confirmed.**
    - The cache builds only entries recorded as not precached, plus every global entry (ShaderPipelineCache.cpp 191-199, 1055-1077).
    - So the pipeline at 5.46 s, recorded as "Missed", will be built.

24. **`r.ShaderPipelineCache.ExcludePrecachePSO`: minor.** D2 says it needs Validation; the 5.8 code needs only precaching (PipelineFileCache.cpp 133-139, 3609-3615). The plan does not use it.

Small drifts in line numbers that change nothing: SaveUserCache is at PipelineFileCache.cpp 159-164 (the note says 157-162). PrintNewPSODescriptors is at 151-157 (the note says 147-153).

## What the plan must add
- Set Validation, and TrackAsyncLoadRequests, with `-dpcvars` in the walk script, and look for the "Set CVar" lines in the log. Use a separate run for naming, not the measured walk.
- If no "PSO PRECACHING MISS" block names the pipeline at 5.46 s, take it as a global pipeline and go to the bundled cache.
- Recording runs must exit cleanly, or run `r.ShaderPipelineCache.Save` before exit. Check that the .rec file exists afterwards.
- Do a full cook after switching on NeedsShaderStableKeys. Fetch the `.shk` files from the runner's copy. Name the output `<prefix>_LedgerProbe_PCD3D_SM6.spc`, and solve how it reaches the runner (item 18).
- Write the startup wait as a per-frame check. Confirm the cache opened: "Opened FPipelineCacheFile ... with N entries".
- Drop `bSharedMaterialNativeLibraries` as a requirement. Do not count on the cache covering compute pipelines beyond Niagara and whatever was recorded.
