# The launch peak of about 8 GB: phase, owner, likely cause, and the run that names it

Written 4 November 2026 by reading only, as a follow-on to F:/LedgerTools/scratch/card-peak-2026-11-04/DIAGNOSIS.md (a real block of about 2 GB, once a launch, cause unknown). Data: the series F:/LedgerTools/tmp/p1-packaged/packaged-day-stand-6c808a1-series-memory.jsonl, the same run's timed log (played-game Saved/Logs/LedgerProbe-backup-2026.11.04-08.27.52.log, in UTC, one hour behind the sampler) and its CSV. The packaged copy is a Development build (.github/workflows/ledger-probe-unreal.yml:605; log `config="Development"`).

## 1. Phase: the first frames after the street's load (high confidence)

| sampler (local) | game card MB | game private MB | log at that moment |
|---|---|---|---|
| 09:26:17 to :22 | 336 | 3,185 to 6,587 | Entry map loading the street (16.76 to 27.00) |
| 09:26:25 | 1,472 | 8,633 | last second of the load |
| **09:26:27** | **8,062** | **11,788** | load ends 26.999; pool 800 MB 27.099; frame 1 27.927; frame 16 (three MetaHumans) 28.54 |
| 09:26:30 | 5,792 | 9,653 | frames about 100 to 200 |

Sample times are truncated to the second and precede a counter call of about a second, so the peak reading falls between 27.0 and about 29.0: after the load, in the first rendered frames. Ruled out by time: engine start, the scalability change (High at 14.887, before the graphics device at 15.088) and the pipeline cache (finished 15.72, while the card read 336 MB). When the counter reads inside its call is unverified.

## 2. Owner: the game process itself (high confidence)

At the peak the sampled tree is the game alone (pid 40352); the launcher, its parent, is outside it. The rest of the card is 1,832 MB at and after the peak, so nothing else moved. The game's private memory falls with it: memory freed, not paged out.

The close's peak is the voice child, not the game. Pid 35392 joins at 09:27:14 ("LedgerVoice: started", 08:27:14.355). In the CSV the game's own DXGI use stays 5.40 to 5.45 GB to the last frame while its budget falls from 9,427 to 5,771 MB; its private memory is flat. The sampler counts children as the game (tools/p1-packaged.ps1:72-73).

## 3. Engine causes, ranked by fit (none confirmed)

On D3D12 every resource starts evicted and becomes resident when a submitted command list first uses it (D3D12Adapter.cpp:38-45; D3D12Resources.cpp:812-816). That explains the flat 336 MB during the load and the 4.3 GB that lands and stays at the first frames. The question is the 2.27 GB that leaves.

1. **Render-graph transient heaps grown by first-frame work** (first Lumen surface-cache fill, distance fields, sky capture, four MetaHumans' first frames). Card heaps (D3D12TransientResourceAllocator.cpp:44-56), freed after 16 unused end-of-frame cycles (RHICoreTransientResourceAllocator.cpp:41-46, 607-613; D3D12Adapter.cpp:1847). Steady 640 MB. Best fit; size unverified.
2. **Render-target pool elements used only at the start**, released after more than 10 unused frames above r.RenderTargetPoolMin (RenderTargetPool.cpp:374-389, 701). Steady 1,276 MB. Same timing fit; size unverified.
3. **Card buffer-pool blocks** freed 20 frames after last use (D3D12RHI.cpp:603-605). Weaker.
4. **Texture streaming's first update**: capped by the 800 MB pool. Low.

Ruled out: pipeline cache and pools sized before scalability (time); upload staging (UPLOAD heap, D3D12Allocation.cpp:1123, system memory on this card, unverified here); a loading movie (none plays); the glass cubes (loaded baked, VignetteShot.cpp:7250-7263).

## 4. The cheapest run that names it

A boot CSV, recording every frame from launch, with no sampler and no voice (the game exits before its voice starts). The launcher with the capture's switches minus -PerfHook:

`-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle -RenderOffScreen -ResX=3440 -ResY=1440 -windowed -ForceRes -nosplash -unattended -dpcvars=r.ScreenPercentage=55,t.MaxFPS=0,r.VSync=0 -ExecCmds="scalability 2" -csvCaptureFrames=900 -ExitAfterCsvProfiling`

- `-csvCaptureFrames=` starts a boot capture (CsvProfiler.cpp:5049, 5177-5184; outside Shipping, CsvProfilerConfig.h:16); `-ExitAfterCsvProfiling` exits after it (CsvProfiler.cpp:4309). Without -PerfHook the game starts no capture of its own (CrimeProbe.cpp:5302).
- Output: F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Profiling/CSV/Profile(date_time).csv. p1-packaged empties that folder; copy it out first.
- Read as text, per frame: GPUMem/LocalUsedMB (the game's DXGI use, every frame, D3D12RHI.cpp:614, RHIStats.cpp:92), TransientMemoryUsedMB (RHICoreTransientResourceAllocator.cpp:104), RenderTargetPoolSize, TextureStreaming/StreamingPool. Row 1 is start-up and load.
- **Confirms cause 1** if, where LocalUsedMB peaks (about 7.7 GB; DXGI reads about 0.3 GB under Windows' counter), TransientMemoryUsedMB stands about 2 GB above 640 and both fall within about 20 frames. **Cause 2** if RenderTargetPoolSize carries it. **Both ruled out** if neither moves; then the memory trace (`-trace=default,memory -tracefile=<F: path>`, VOICE-ON-CARD-TRACE-2026-10-25.md:7). If LocalUsedMB never peaks, the counter itself is in question.
- Then a one-switch test: add `r.RDG.TransientAllocator=0` to the -dpcvars list (RenderGraphPrivate.cpp:251-256, not read-only; DeviceProfileManager.cpp:737-753).

LLM (`-llm -llmcsv`) exists in Development (LowLevelMemTrackerDefines.h:26-29) but writes once a second (LLM.cpp:960-963), coarser than the CSV.

## Not reached or unverified

- The askreal-2026-11-04f log (the series run's own log was used).
- Get-Counter's timing inside its call; the live counter instance names.
- WDDM keeping commit for evicted memory and placing UPLOAD heaps in system memory: no Microsoft source read.
- r.RenderTargetPoolMin's value; a windowless Insights memory export.
- Every candidate's size: nothing was run.

## The boot profile, run (4 November, 14:18 to 14:21)

Five launches of the played copy (the 3 to 4 November build) with the note's switches (-csvCaptureFrames=900 -csvGpuStats -ExitAfterCsvProfiling, no -PerfHook; F:/LedgerTools/tmp/launch-peak-2026-11-04, Profile*.csv and run2 to run5). The game's own card use (GPUMem/LocalUsedMB, each frame) peaks at 6,086 to 6,224 MB at frames 13 to 15, the render-graph's temporary heap at 768 to 896 MB and the render-target pool at about 1,276 MB, then settles at 5,514 to 5,593 MB. **No launch showed the 2 GB spike.** So the leading cause is neither confirmed nor ruled out: without the capture's own steps (Sheila's walk-round, the cut to the hook camera, the game's voice starting, the forced clean-up) the first frames stay near 6.2 GB. Next: the same boot profile with -PerfHook=stand, as the captures run, until a launch shows the spike, then read the three columns at its frame.

## With the capture's steps (-PerfHook=stand), run (4 November, 16:19 to 16:20)

Three more launches of the same played copy, the same switches plus -PerfHook=stand (F:/LedgerTools/tmp/launch-peak-2026-11-04/perfhook, run1 to run3, command.txt): GPUMem/LocalUsedMB peaks at 6,103 to 6,174 MB at frames 18 to 22, the render graph's temporary heap at 768 MB there (896 at most), and settles at about 5,470 MB (run3 ended after 68 frames). No frame over 7,000 MB. **Eight launches in all, none with the spike.** So the 8.1 GB "launch peak" of the memory sampler series is not the game's own card use as the game counts it (DXGI, every frame from launch): it is in Windows' counter only, which also counts what is not the game's own (the note's section 3 lists DXGI about 0.3 GB under it in steady play). For the exit (CLOSE-D): the game's own card use at launch is at most 6.2 GB, in steady play 5.4 to 5.6 GB; the outside counter's once-a-launch rise is named as unexplained, not the game's frames.
