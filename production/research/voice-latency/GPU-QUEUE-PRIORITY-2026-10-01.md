# Would a high-priority card queue keep the voice fast beside the game? (1 October 2026)

Research note, about 30 minutes, for the question left open at the end of STREAMING-IN-GAME-2026-10-01.md: is it worth two weeks to move the voice into the game so it can have a high-priority card queue? Sources are listed at the end with dates. Nothing was run on the graphics card; only installed files and Windows' own diagnostic report were read.

## First, a correction about this PC

The question said the card is NVIDIA. It is not. Windows reports **AMD Radeon RX 6700**, driver 32.0.21045.5002 (17 August 2026), on a Ryzen 5 5600X (6 cores, 12 threads). The earlier note also says RX 6700. The DirectX report (dxdiag, read today) says:

    Hardware Scheduling: DriverSupportState:AlwaysOff Enabled:False

So **hardware-accelerated GPU scheduling (HAGS) is not available on this card with this driver.** Windows' older software scheduler decides whose work runs on the card. AMD officially supports HAGS only on the RX 7000 series and newer (secondary sources, 2026). NVIDIA's own tools for this problem (CUDA in Graphics, the In-Game Inferencing SDK) need an NVIDIA card and HAGS, so they do not apply on this PC.

## Short answer

- **A high-priority queue in a separate process will not help.** Microsoft's specification says the HIGH priority only ranks a queue against **other queues in the same process**. Only GLOBAL_REALTIME ranks against other programs, and it needs administrator rights, so it cannot be shipped to players.
- **Inside the game, a HIGH queue might help, but nothing documents that it does on AMD cards without HAGS.** That has to be measured, and it can be measured cheaply without the two-week move (step 3 below).
- **The measurements point first at waiting, not at priority.** The compiled step reads its scores back to the processor after every token (`bind_output("scores","cpu")` in nano_step_graph.py), so every token is one full trip to the card and back. Next to a game that keeps the card busy with roughly 26 ms frames, each trip waiting about 60 ms fits "our small job waits behind the game's frame packets". If that is the cause, the fix is fewer trips: keep the token choice on the card and read tokens back in batches. That can be tested in Python in half a day, and it needs no move into the game.
- **The processor half is a separate cause** that a card queue cannot fix: Unreal starts 10 worker threads on this 12-thread CPU, and a token loop on the processor is limited by memory speed. Unreal 5.8 has launch options to pin the game to fewer cores, which makes this cheap to test too.

## 1. Can ONNX Runtime's DirectML provider use a queue we create?

**Yes.** `OrtDmlApi::SessionOptionsAppendExecutionProvider_DML1(OrtSessionOptions*, IDMLDevice*, ID3D12CommandQueue*)` takes a DirectML device and a D3D12 queue that we create ourselves. The queue must be DIRECT or COMPUTE, and the DirectML device and the queue must come from the same ID3D12Device (onnxruntime.ai DirectML page; dml_provider_factory.h on main). There is also an older free function, `OrtSessionOptionsAppendExecutionProviderEx_DML`, which takes the same device and queue; the header says to use the OrtDmlApi version instead. Which release first added OrtDmlApi was not confirmed in the time available. A 2021 issue (#9164, about 1.8) predates it.

**What is installed.** onnxruntime is not in C:\LedgerTools\chatterbox-nano\env-dml: that environment holds only torch-directml, with its own DirectML.dll. The ONNX Runtime the earlier note used is in **F:\LedgerTools\voice-env-export**:

- onnxruntime-directml **1.24.4** (onnxruntime.dll file version 1.24.20260316.2), with onnxruntime_providers_shared.dll.
- **DirectML.dll 1.15.4** (241025-1615, dml-1.15) next to it. The documentation says the provider currently uses DirectML 1.15.2.
- The DLL exports `OrtGetApiBase`, `OrtSessionOptionsAppendExecutionProvider_DML` and `OrtSessionOptionsAppendExecutionProviderEx_DML`, and it contains the provider-API name "DML" (reached through `GetExecutionProviderApi("DML", ORT_API_VERSION, …)`).
- It also contains these session settings: `ep.dml.enable_graph_capture`, `ep.dml.enable_cpu_sync_spinning`, `ep.dml.disable_graph_fusion`, `ep.dml.disable_memory_arena`, `ep.dml.enable_graph_serialization`.
- No C/C++ headers are installed with it, and no import library.

**Reachable from a small C++ program without NuGet.**

- Load onnxruntime.dll with `LoadLibrary` and look up `OrtGetApiBase` with `GetProcAddress`; no .lib file is needed.
- Use `onnxruntime_c_api.h` and `dml_provider_factory.h` from the GitHub tag **v1.24.4**, so they match the DLL's API version (MIT licence).
- `d3d12.h` and `DirectML.h` are already in the installed Windows SDK 10.0.26100.
- Create the IDMLDevice by calling `DMLCreateDevice1` from **the DirectML.dll beside onnxruntime.dll** (load it by full path), not Windows' System32 copy, so both use the same DirectML version.
- Python cannot pass a queue: the Python provider options are only `device_id`, `performance_preference`, `device_filter` and `disable_metacommands`.

**What ONNX Runtime does by default.** It creates its own queue with `Type = DIRECT` (COMPUTE only on compute-only devices), `Flags = DISABLE_GPU_TIMEOUT`, and **no priority set**, so NORMAL (dml_provider_factory.cc on main). So today the voice's work goes to the **same 3D engine as the game's drawing**.

Also note: Microsoft has put DirectML in "sustained engineering". It is supported, but new work goes into Windows ML.

## 2. Does Windows honour queue priority between processes?

- **D3D12_COMMAND_QUEUE_PRIORITY_HIGH counts only within the process.** In Microsoft's "Command Queue Dynamic Priority" specification, HIGH maps to process priority HIGH and **global priority DEFAULT**. Process priority is "a non-yielding boost relative to other contexts within the same process"; global priority is "relative to other apps in the system". Only GLOBAL_REALTIME maps to global HARD_REALTIME. **A HIGH queue in the voice's own process therefore gains nothing against the game.**
- **GLOBAL_REALTIME** "must be sufficiently privileged". If the rights are missing, or the card or driver cannot give the needed preemption, creation fails; it is never silently downgraded (D3D12_COMMAND_QUEUE_PRIORITY reference, updated 2024-02-22). Windows' driver certification has a test that such queues "are able to preempt lower-priority workloads" (HLK, 2020-03-09), so a certified AMD driver should accept it when run with administrator rights. Players cannot be asked to run the game as administrator, so this is **evidence only, not something to ship**.
- **The process-wide card priority.** `D3DKMTSetProcessSchedulingPriorityClass` (gdi32, since Vista; classes IDLE to REALTIME) sets a process's priority with Windows' card scheduler. OBS uses REALTIME with it so that OBS "would be deprioritized by Windows over fullscreen games" no longer happens, and it falls back with "not admin?". So the top class needs administrator rights, and a real program has used it to win the card back from a fullscreen game. It can be called from Python (ctypes), which makes it the cheapest cross-process test.
- **HAGS.** Microsoft (2020-06-30): with HAGS, "Windows continues to control prioritization" while the card's own scheduling processor handles time slices and context switches. Without HAGS (this PC), a high-priority thread on the processor does that work. The dynamic-priority API (`ID3D12CommandQueue1::SetProcessPriority/SetGlobalPriority`) needs a hardware-scheduling feature check, so it is not usable here.
- **NVIDIA.** Not this PC. For the record: NVIDIA's In-Game Inferencing SDK 1.7.0 (updated 2026-08-14) exposes three modes (prioritise graphics, prioritise compute, balance) that it calls "hints to the GPU scheduling hardware", needs driver 575 or later, needs HAGS for CUDA, and runs **in the game's process** on the game's D3D12 device.
- **No published measurement** was found of HIGH or GLOBAL_REALTIME between processes on AMD RDNA2 under Windows. On Linux, SteamVR's high-priority queue on AMD needs special rights, and its async reprojection needs Polaris or newer for 3D preemption. That shows the hardware can preempt; it is not a Windows measurement.

## 3. Other reasons a second process's small card jobs wait while a game draws

- **Time-slicing per engine.** Microsoft (2017): "When a process gets a time slice of an engine, it gets to use all of that engine's underlying cores". An engine runs one process's work at a time. Our DIRECT queue shares the 3D engine with the game, and a token waits for the game's turn to end or be preempted. Windows 8's preemption model asks for mid-packet preemption, but how fine it is depends on the hardware (GPU Preemption, 2025-07-18). With one round trip per token and about 26 ms game frames, a wait of 1 to 2 frames per token (about 60 ms) is what this would look like. **Remedy:** fewer round trips per token (whole loop on the card, tokens read back every 8 to 16), a COMPUTE queue (it may land on AMD's separate compute engine, though Unreal also uses async compute), or a higher priority.
- **Video memory budget.** "If an application doesn't stay within its budget, the process will be intermittently frozen to allow other applications to run"; DWM and the foreground program come first (Residency, updated 2025-06-14). The RX 6700 has 10 GB. The game at 3440×1440 Highest plus a 406 MB step graph and its cache may push the voice, a background process, over its budget. This has not been checked; Windows' own counters can show it (step 0).
- **The processor-side scheduler and wake-up.** Without HAGS, the scheduler runs as a high-priority thread on the processor, and our thread sleeps on a fence and must be woken. With the game busy on most cores, both can be late. ONNX Runtime has `ep.dml.enable_cpu_sync_spinning` (spin instead of sleep), which is in the installed DLL.
- **Present, flip and DWM.** The DWM's work is high priority (GPU Preemption page). A fullscreen flip-model game bypasses most composition. No source found showing present or flip timing slows another process's compute directly; it is lower on the list.
- **Not likely the cause:** the game's GPU load as such. Half resolution and frame caps changed nothing, but each was tried alone, and the uncapped half-resolution game probably still kept the card full. **One combined run (half resolution and 30 fps together, so the card is mostly idle) would settle it.**

## 4. The processor half, and how shipped products run their AI

- **Unreal takes every core.** On Windows, Unreal 5.8 starts `logical cores - 2` worker threads, so 10 here (WindowsPlatformMisc.cpp, `NumberOfWorkerThreadsToSpawn`), plus the game, render, RHI and audio threads. The installed 5.8 source has launch options to limit this: `-corelimit=N` (GenericPlatformMisc.cpp) and `-processaffinity=N` / `-processaffinityphysical=N` (LaunchWindows.cpp). With `-processaffinity=8` the game runs on logical processors 0 to 7, which leaves cores 4 and 5 (processors 8 to 11) for the voice.
- **A token loop on the processor is limited by memory speed.** Every token reads all the weights; "token generation… is largely bandwidth-bound" (hardware-corner, 2026-08-26). At about 40 tokens a second, the step's roughly 400 MB of fp32 weights is about 16 GB/s of a dual-channel DDR4 system's roughly 40 to 50 GB/s in practice, and all six cores share one 32 MB L3 cache with the game. **If that is the limit, neither priority nor affinity will fix it; only smaller weights would** (fp16 or int8 for the processor path).
- **Windows QoS:** processes that are not in focus get a lower QoS, but on mains power the effect is mostly on frequency choice. It is a one-line opt-out (`SetProcessInformation` ProcessPowerThrottling, EXECUTION_SPEED off). The expected effect on this desktop is small (Quality of Service, 2025-07-14).
- **How shipped products do it:**
  - **NVIDIA ACE / In-Game Inferencing:** in the game's process, as C++ plugins. "NVIGI must get the D3D direct queue that your game is using for graphics", so that inference runs "using the game's D3D12 device and command queue" (NVIDIA blog, 2025-02-20). The reason given is scheduling AI alongside the frame rather than against it. inZOI ships ACE's small language model on the card in-process, using about 1 GB of video memory (secondary sources).
  - **Unreal's own NNE:** runs in-process. Its RDG runtime puts inference into the frame's render graph, and its ORT-DirectML runtime runs in the game process.
  - **Inworld and Convai:** mainly cloud. Inworld's newer "Runtime" offers optional on-device inference (secondary, 2026).
  - **Community Unreal plugins** (llama.cpp-based, 2026): mostly in-process on Unreal tasks. Some use a local server in a separate process (Ollama over HTTP).
  - No studio's published reasoning for out-of-process was found.

## Cheap experiment plan (about 2 to 3 days, before the two-week move)

The aim is to separate four causes: per-token waiting, priority, video memory, and processor contention. Every run uses the real packaged game in the street, as before, and is measured idle and beside the game.

**Step 0. No code, about 1 hour.** While the voice loop runs beside the game, read Windows' counters (`typeperf`):

- `\GPU Engine(*)\Utilization Percentage`, for the voice's and the game's process: does the voice run on engtype_3D or engtype_Compute?
- `\GPU Process Memory(*)\Dedicated Usage` and `Shared Usage` for the voice, and `\GPU Adapter Memory(*)\Dedicated Usage`: has the voice's model been pushed out to shared memory?

Also do the one combined run, half resolution with a 30 fps cap.

**Step 1. Python only, about half a day,** in the existing compiled-step script:

- (a) `ep.dml.enable_cpu_sync_spinning=1`.
- (b) **The pipelining test:** bind `scores` to the card, feed a fixed token, run 64 steps without reading anything back, then sync once. Time the `run_with_iobinding` return separately from the completion, to confirm Run does not block.
- (c) `D3DKMTSetProcessSchedulingPriorityClass` from the voice process: HIGH, then REALTIME, which needs administrator rights (Jafar would start it). Also lower the *game's* class to BELOW_NORMAL from the voice. Record the status code and tokens a second for each.

**Step 2. Processor half, about 1 hour.** Start the game with `-processaffinity=8 -corelimit=4`, pin the voice to processors 8 to 11, and measure the processor loop. Then run the voice beside only a memory-bandwidth load, without the game.

**Step 3. Small C++ test, about 1 to 2 days, only if steps 0 to 2 leave it open.**

- One program loads onnxruntime.dll and DirectML.dll from voice-env-export and creates its own D3D12 device.
- It runs the same 406 MB step graph on our own queue in each combination: DIRECT or COMPUTE, and NORMAL, HIGH or GLOBAL_REALTIME.
- Run it (i) beside the game, which is the cross-process case, and (ii) beside a stand-in "game" in the **same program**: a NORMAL queue repeatedly submitting about 26 ms of heavy dispatches. Case (ii) is the honest proxy for "the voice inside the game with a HIGH queue", and it needs no Unreal work.
- Record the stand-in's frame time too.

**What would justify the two weeks:**

- In-process HIGH (3-ii) restores at least 75 compiled steps a second (80% of the idle 92), and the stand-in's frame time grows by no more than about 2 ms.
- Cross-process NORMAL, step 1(b) and step 1(c) without administrator rights do not restore it.
- Step 2 shows the processor half is solved by reserving cores.

**What would argue against:**

- Step 1(b) restores near-idle speed beside the game. Then the cure is in-graph sampling and batched readback in the existing separate process: days, not two weeks.
- Or in-process HIGH changes nothing, because the AMD driver without HAGS ignores in-process priority, or preemption is too coarse.
- Or only GLOBAL_REALTIME or REALTIME helps; these need administrator rights and cannot ship.
- Or step 0 shows the voice evicted from video memory. Then priority is beside the point and the cure is smaller weights or a reservation.
- Or step 2 shows the processor loop is limited by memory speed. Moving in-process will not change that.

## Money, licences, scope

- **No money involved.**
- **Licences:**
  - ONNX Runtime and its headers are MIT.
  - DirectML.dll is Microsoft's redistributable under its own licence. Shipping it inside the game means checking that licence against the allowlist; it is already in the voice's environment, but not in the game.
  - NVIDIA's In-Game Inferencing SDK and ACE use NVIDIA's licence and NVIDIA cards; they are not relevant on this PC, and any later use is a licence and scope decision.
  - Optional for step 0: Microsoft's free Windows Performance Analyzer (GPUView-style timelines). Windows' own `wpr.exe` can record, but viewing needs the download, which needs Jafar's yes as a download.
- **Scope:**
  - Any result that depends on administrator rights (GLOBAL_REALTIME, REALTIME process class) is a diagnosis, never a shipped setting.
  - HAGS cannot be turned on for this card with this driver.

## Sources (dates as shown on the page)

- ONNX Runtime, DirectML Execution Provider (undated; DirectML 1.15.2; "sustained engineering"): https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html
- ONNX Runtime source, dml_provider_factory.h (main, read 2026-10-01): https://github.com/microsoft/onnxruntime/blob/main/include/onnxruntime/core/providers/dml/dml_provider_factory.h
- ONNX Runtime source, dml_provider_factory.cc, own queue DIRECT, no priority (main, read 2026-10-01): https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/core/providers/dml/dml_provider_factory.cc
- ONNX Runtime source, dml_session_options_config_keys.h (main, read 2026-10-01): https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/core/providers/dml/dml_session_options_config_keys.h
- ONNX Runtime issue #9164 (2021-09-23): https://github.com/microsoft/onnxruntime/issues/9164
- D3D12_COMMAND_QUEUE_PRIORITY (ms.date 2018-12-05, updated 2024-02-22): https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_command_queue_priority
- DirectX-Specs, ID3D12CommandQueue Dynamic Priority (undated spec, read 2026-10-01): https://microsoft.github.io/DirectX-Specs/d3d/D3D12_CommandQueue_Dynamic_Priority.html
- HLK, D3D12 Global Realtime Command Queue Priority (2020-03-09): https://learn.microsoft.com/en-us/windows-hardware/test/hlk/testref/f00f5cec-0845-479f-a9b1-7791d8f7c99a
- D3DKMTSetProcessSchedulingPriorityClass (ms.date 2022-04-14): https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/d3dkmthk/nf-d3dkmthk-d3dkmtsetprocessschedulingpriorityclass
- OBS commit "libobs-d3d11: Set maximum GPU priority" (undated on page): https://github.com/obsproject/obs-studio/commit/ec769ef008b748f7dfba211daec9eb203ea4bea0
- Microsoft DirectX blog, Hardware Accelerated GPU Scheduling (2020-06-30): https://devblogs.microsoft.com/directx/hardware-accelerated-gpu-scheduling/
- Microsoft DirectX blog, GPUs in the Task Manager (2017-07-21): https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/
- GPU Preemption, Windows drivers (ms.date 2024-12-18, updated 2025-07-18): https://learn.microsoft.com/en-us/windows-hardware/drivers/display/gpu-preemption
- Residency, Direct3D 12 (ms.date 2018-05-31, updated 2025-06-14): https://learn.microsoft.com/en-us/windows/win32/direct3d12/residency
- Quality of Service, Win32 (ms.date 2025-07-14): https://learn.microsoft.com/en-us/windows/win32/procthread/quality-of-service
- NVIDIA In-Game Inferencing SDK 1.7.0, GPU Scheduling for AI (updated 2026-08-14): https://docs.nvidia.com/nvigi-sdk/1.7.0/docs/nvigi_core/docs/GpuSchedulingForAI.html
- NVIDIA blog, ACE characters with the In-Game Inferencing SDK (2025-02-20): https://developer.nvidia.com/blog/bring-nvidia-ace-ai-characters-to-games-with-the-new-in-game-inference-sdk/
- NVIDIA TensorRT for RTX, Simultaneous Compute and Graphics (undated, "latest"): https://docs.nvidia.com/deeplearning/tensorrt-rtx/latest/inference-library/compute-graphics.html
- SteamVR for Linux issue #660, high-priority queue permission (undated in summary): https://github.com/ValveSoftware/SteamVR-for-Linux/issues/660
- songplayer issue #154, WDDM priority between processes (2026-09-13): https://github.com/zbynekdrlik/songplayer/issues/154
- hardware-corner, memory bandwidth and token speed (2026-08-26): https://www.hardware-corner.net/memory-bandwidth-llm-speed/
- AMD HAGS support on RX 7000 only (secondary, 2026): https://www.pcbuildadvisor.com/what-is-hardware-accelerated-gpu-scheduling-complete-2026-guide/ ; this PC's own dxdiag ("DriverSupportState:AlwaysOff") is the primary evidence.
- inZOI on-device model, about 1 GB of video memory (secondary): https://thegameswiki.com/inzoi/wiki/smart-zoi
- Inworld Runtime, optional on-device (secondary, 2026): https://loreweaver.ink/insights/inworld-convai-alternatives/
- Unreal NNE overview (Epic docs, undated): https://dev.epicgames.com/documentation/en-us/unreal-engine/neural-network-engine-overview-in-unreal-engine
- Unreal Engine 5.8 installed source (read 2026-10-01): Engine/Source/Runtime/Core/Private/Windows/WindowsPlatformMisc.cpp (NumberOfWorkerThreadsToSpawn), GenericPlatformMisc.cpp (-corelimit, -physicalcorelimit), Launch/Private/Windows/LaunchWindows.cpp (-processaffinity, -processaffinityphysical).
