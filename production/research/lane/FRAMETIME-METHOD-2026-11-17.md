# Frame time and GPU memory measurement of shipped PC games: method research

Date: 17 Nov 2026. Read-only web research, nothing downloaded or run. Pages were read through a fetch tool that returns summaries and short quotes, so "quoted" text below is as the tool returned it from the named page. Anything not read on a primary page is marked UNVERIFIED.

## 1. PresentMon: licence, release, capture method, rights

- Licence: MIT. The repository sidebar shows "MIT license" and the README describes an MIT-style licence, copyright Intel Corporation 2017 to 2024. https://github.com/GameTechDev/PresentMon (read 17 Nov 2026); https://raw.githubusercontent.com/GameTechDev/PresentMon/main/README.md (read 17 Nov 2026). The LICENSE.txt file itself could not be opened (blocked, see Unreached), so the exact licence text is UNVERIFIED beyond the sidebar and README.
- Latest release: the GitHub releases page marks v2.6.0 as "Latest", dated 21 Sep (year not shown on the page). https://github.com/GameTechDev/PresentMon/releases (read 17 Nov 2026). Wccftech's article on 2.6.0 is dated 26 Sep 2026, which fixes the year as 2026. https://wccftech.com/intel-rolls-out-presentmon-2-6-0-cutting-cpu-overhead-significantly/ (read 17 Nov 2026). Earlier releases: v2.5.1 (29 Jun), v2.5.0 (first released April 2026), v2.4.1 (16 Jan), v2.4.0 (11 Nov).
- newreleases.io says a v2.6.1 exists and is latest. https://newreleases.io/project/github/GameTechDev/PresentMon/release/v2.6.0 (read 17 Nov 2026). This conflicts with the GitHub page; v2.6.1 is UNVERIFIED.
- v2.6.0 notes: D3D12 pipeline state compilation metrics, OS flip events, CSV source ID and layer ID, lower service CPU use (up to 78 percent), "Improved AMD dedicated VRAM usage reporting", experimental Flash Injector removed. Same newreleases.io and releases pages (read 17 Nov 2026).
- No injection, ETW based: the README says the PresentData library does "low-level ETW event collection and analysis", and the console application "exports frame data to CSV". The console README has an option --etl_file, "Analyze an ETW trace log file instead of the actively running processes", and trace session options (--session_name, --stop_existing_session). https://raw.githubusercontent.com/GameTechDev/PresentMon/main/README-ConsoleApplication.md (read 17 Nov 2026). The doc does not use the word "injection"; that the console app never injects is inferred from the ETW design, not stated. The Flash Injector removed in 2.6.0 belonged to the GUI app, not the console app.
- Rights: the README troubleshooting section says an "Access denied" error means the user must be in the "Performance Log Users" group. The console README offers --restart_as_admin: "If not running with elevated privilege, restart and request to be run as administrator." The console README itself does not mention Performance Log Users. Practical reading: run as administrator, or add the user to Performance Log Users. Sources: README.md and README-ConsoleApplication.md above (read 17 Nov 2026).
- Useful options (console README): --process_name name, --process_id id, --timed seconds, --output_file path, --terminate_after_timed, --terminate_on_proc_exit, --v1_metrics, --v2_metrics, --no_track_gpu, --no_track_display, --track_frame_type. Same page (read 17 Nov 2026).

## 2. CSV column names

Important finding: the current console app has three header formats, chosen by flags. Source of truth is the code, https://github.com/GameTechDev/PresentMon/blob/main/PresentMon/CsvOutput.cpp and https://github.com/GameTechDev/PresentMon/blob/main/PresentMon/CommandLine.cpp (both read 17 Nov 2026, main branch, not a release tag; whether v2.6.0 matches main exactly is UNVERIFIED).

CommandLine.cpp: `args->mUseV2Metrics = false;` by default; `--v2_metrics` help text "Output a CSV using PresentMon 2.x metrics."; `--v1_metrics` help text "Output a CSV using PresentMon 1.x metrics."; if both are given, v1 is ignored.

### 2a. Default header (no flag), as in the console README table

Columns in the README table, in order (README-ConsoleApplication.md, main, read 17 Nov 2026):

Application, ProcessID, SwapChainAddress, PresentRuntime, SyncInterval, PresentFlags, VidPnSourceId, LayerIndex, AllowsTearing, PresentMode, FrameType, CPUStartTime (or CPUStartQPC, CPUStartQPCTime, CPUStartDateTime), MsCPUBusy, MsCPUWait, MsGPULatency, MsGPUTime, MsGPUBusy, MsGPUWait, VideoBusy, DisplayLatency, DisplayedTime, MsAnimationError, AnimationTime, MsClickToPhotonLatency, MsAllInputToPhotonLatency, InstrumentedLatency, MsBetweenPresents, MsInPresentAPI, MsBetweenDisplayChange, MsUntilDisplayed, MsRenderPresentLatency, MsBetweenSimulationStart, MsPCLatency, MsBetweenAppStart, PresentId.

In the code the default writes (after the common columns) a time column TimeInMs / TimeInQPC / TimeInDateTime / TimeInSeconds, then MsBetweenSimulationStart, MsBetweenPresents, MsBetweenDisplayChange, MsInPresentAPI, MsRenderPresentLatency, MsUntilDisplayed, MsPCLatency, CPUStartTime, MsBetweenAppStart, MsCPUBusy, MsCPUWait, MsGPULatency, MsGPUTime, MsGPUBusy, MsGPUWait, MsVideoBusy, MsAnimationError, AnimationTime, MsFlipDelay, MsAllInputToPhotonLatency, MsClickToPhotonLatency, MsInstrumentedLatency (several only with display, GPU or input tracking on). The README order and the code order differ; read the header row of each CSV rather than assume positions.

README descriptions (quoted as returned):
- MsBetweenPresents: "The time between this Present() call and the previous one, in milliseconds."
- MsBetweenDisplayChange: "How long the previous frame was displayed before this Present() was displayed, in milliseconds."
- MsBetweenAppStart: described as the time from the start of a frame until the CPU starts working on the next frame, in milliseconds.
- CPUBusy (MsCPUBusy): "How long the CPU spent working on this frame before presenting it."
- CPUWait (MsCPUWait): "How long the CPU spent waiting before starting the next frame."
- GPULatency (MsGPULatency): "How long it took from the start of this frame until the GPU started working on it."
- GPUTime (MsGPUTime): "The total amount of time that GPU was working on this frame."
- GPUBusy (MsGPUBusy): "How long the GPU was actively working on this frame."
- GPUWait (MsGPUWait): "How long the GPU was idle while working on this frame."
- DisplayLatency: "How long it took from the start of this frame until the frame was displayed on the screen."
- DisplayedTime: "How long the frame was displayed on the screen, or 'NA' if the frame was not displayed."
- MsAnimationError: "The difference between the previous frame's CPU delta and display delta."

### 2b. --v2_metrics header

From CsvOutput.cpp (read 17 Nov 2026): common columns, then CPUStartTime (or CPUStartQPC, CPUStartQPCTime, CPUStartDateTime), FrameTime, CPUBusy, CPUWait; with GPU tracking GPULatency, GPUTime, GPUBusy, GPUWait; VideoBusy; with display tracking DisplayLatency, DisplayedTime, AnimationError, AnimationTime, MsFlipDelay; with input tracking AllInputToPhotonLatency, ClickToPhotonLatency; InstrumentedLatency. The current README does not contain the word FrameTime at all, and does not define it (README read 17 Nov 2026). The v2.0.0 README listed CPUStartTime, CPUBusy, CPUWait, GPULatency, GPUBusy, VideoBusy, GPUWait, DisplayLatency, DisplayedTime, ClickToPhotonLatency, with no Ms prefix and no FrameTime. https://github.com/GameTechDev/PresentMon/blob/v2.0.0/README-ConsoleApplication.md (read 17 Nov 2026). The meaning of FrameTime is UNVERIFIED from docs (likely CPUBusy plus CPUWait, the CPU start to next CPU start interval, which matches MsBetweenAppStart; not confirmed).

### 2c. --v1_metrics header and old 1.x CSVs

From CsvOutput.cpp, legacy FrameMetrics1 writer (read 17 Nov 2026), lower-case "ms":
Application, ProcessID, SwapChainAddress, Runtime, SyncInterval, PresentFlags, Dropped, TimeInSeconds, msInPresentAPI, msBetweenPresents; with display tracking AllowsTearing, PresentMode, msUntilRenderComplete, msUntilDisplayed, msBetweenDisplayChange, msFlipDelay; with GPU tracking msUntilRenderStart, msGPUActive; optional msGPUVideoActive, msSinceInput, QPCTime, msDisplayTime, FrameId.

Note the case change: 1.x writes msBetweenPresents, 2.3 and later write MsBetweenPresents by default. A third-party fix confirms scripts broke on this. https://github.com/feanor91/overlay-perf/pull/1 (read 17 Nov 2026). Parse column names case-insensitively.

### 2d. Which column for frame time

- The PresentMon console README makes no recommendation (read 17 Nov 2026).
- GamersNexus (28 Oct 2025, PresentMon console v2.3.1): "MsBetweenPresents is unusable for per-frame calculations like animation error"; MsBetweenAppStart is PresentMon's best representation of "the literal time taken to create an individual frame start-to-finish" and better for testing hardware performance; MsBetweenDisplayChange is what the player sees and the only way to include generated frames. https://gamersnexus.net/gpus-gn-extras-cpus/problem-gpu-benchmarks-reality-vs-numbers-animation-error-methodology-white (read 17 Nov 2026).
- Recommendation for this team: record the default header; use MsBetweenAppStart as the frame time for comparison, keep MsBetweenPresents as a cross-check against older tools and old CSVs, and MsBetweenDisplayChange for what reaches the screen. Use MsCPUBusy and MsGPUBusy to tell CPU-bound from GPU-bound. Turn frame generation off in all games for a fair comparison.

## 3. GPU memory (VRAM)

- PresentMon console app: no GPU memory column in either header (CsvOutput.cpp and console README, read 17 Nov 2026).
- PresentMon Capture Application (the GUI, uses the PresentMon Service): metrics table includes "GPU Memory Size Used", CSV column GPUMemorySizeUsed, query type DF (Dynamic and Frame event), plus GPUMemorySize. It is device telemetry (whole graphics card), not per process. Capture writes pmcap-[exe]-YYMMDD-HHMMSS.csv and a stats file under the user's AppData "Intel\PresentMon\Capture". https://github.com/GameTechDev/PresentMon/blob/main/README-CaptureApplication.md (read 17 Nov 2026). Whether the GUI capture is free of injection is UNVERIFIED (the removed Flash Injector suggests the GUI once had an optional injector).
- Windows performance counters, per process: counter path "\GPU Process Memory(*)\Dedicated Usage" and adapter-wide "\GPU Adapter Memory(*)\Dedicated Usage" appear in a third-party issue, not a Microsoft doc. https://github.com/Loment-Lang/Loment/issues/1297 (read 17 Nov 2026). Instance names carry pid_NNNN and must be enumerated, not built by hand (Microsoft Q&A moderator, for the GPU Engine counters; suggests Get-Counter -ListSet 'GPU*'). https://learn.microsoft.com/en-us/answers/questions/5641645/how-to-get-the-special-process-gpu-usage-with-the (read 17 Nov 2026). A Microsoft reference page for the GPU Process Memory counter set was not found: exact counter names UNVERIFIED until listed on the PC with Get-Counter -ListSet 'GPU*' or typeperf -q.
- Known fault: Microsoft KB 4490156, "GPU process memory counters report incorrect values": the Performance Monitor "GPU Process Memory" counter and Task Manager Details "Dedicated GPU memory" can appear to leak (rising about 100 MB per hide and restore cycle), Windows 10 1709 and later; workaround is the Task Manager Performance pane or Windows Performance Toolkit (WPR/WPA). Updated 2026-02-12. https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/gpu-process-memory-counters-report-wrong-value (read 17 Nov 2026). Whether this still applies on Windows 11 is UNVERIFIED.
- What per-process "dedicated" means: Microsoft DirectX blog (21 Jul 2017): data "is gathered directly from VidSch and VidMm"; per-process values include memory shared across processes, so they overlap and sum to more than the card uses; dwm.exe can look inflated; the Performance tab is the accurate total. Needs a WDDM 2.0 driver or later. https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/ (read 17 Nov 2026).
- Recommendation: log "\GPU Process Memory(pid_N*)\Dedicated Usage" once a second with typeperf or Get-Counter alongside the PresentMon run, plus "\GPU Adapter Memory(*)\Dedicated Usage" for the whole card; report the peak and the median over the walk; for a cross-check on one run, a WPR trace read in WPA. Avoid hide and restore (alt-tab) during the walk because of KB 4490156. Treat the numbers as comparable between games on one PC, not as exact allocation.

## 4. CapFrameX

- Licence: MIT, "Copyright (c) 2018-2026 DevTechProfile", with bundled third-party licences (Open Hardware Monitor under MPL 2.0, WinRing0, OxyPlot and others). https://github.com/CXWorld/CapFrameX/blob/master/LICENSE (read 17 Nov 2026). Check the bundled components against the licence allowlist before use.
- Uses PresentMon: "CapFrameX combines Intel's PresentMon with hardware monitoring, frametime and FPS charts, and configurable overlays." Version 1.9.1 (stable build 1.9.1.5) updates PresentMon to 2.6.0. Overlay is RTSS (which does inject; capture does not need it). https://github.com/CXWorld/CapFrameX (read 17 Nov 2026); https://www.capframex.com/support (read 17 Nov 2026). A v1.9.2 beta exists per a search result title only, UNVERIFIED.
- Reports: min, max, average, percentiles (P1, P0.2 and others), x% low, x% low average, adaptive standard deviation, stutter time (frames over 2.5 times average, default) and low-FPS time (frames slower than 25 FPS, default). GitHub README above.
- Definitions, CapFrameX blog "Explanation of different performance metrics", Taxxor, 31 May 2020, updated 10 Aug 2022. https://www.capframex.com/blog/post/Explanation%20of%20different%20performance%20metrics (read 17 Nov 2026):
  - Percentile: "the value for which X% of all remaining values are smaller than this." P1 FPS means about 99 percent of frames ran at or above it. For P0.1 and P0.2 "you should have more than 1000 frames". Percentiles "are not about times, but only about frames."
  - 1% low (CapFrameX, time-weighted): sort frame times worst first and "the frametime values are added one by one until their sum reaches or exceeds 1% of the total benchmark time"; the FPS of the frame that crosses is the 1% low.
  - 1% low average: "the average of the lowest x% of values" (frames, not time).
  - FPS = 1000 / frame time in ms.
- Converting frame time to FPS flips the tails: "a 1% low into a 1% high and a P1 into a P99." So P1 FPS = 1000 / P99 frame time. https://www.capframex.com/blog/post/The%20challenge%20of%20displaying%20performance%20metrics%20as%20FPS (27 Jun 2020, read 17 Nov 2026).
- Common practice: GamersNexus says "we aren't using percentiles"; their 1% and 0.1% lows are averages of the worst 1% and 0.1% of frames (same as CapFrameX "1% low average"). GN page above (read 17 Nov 2026). A ComputerBase forum thread (16 Jan 2025) explains the same split and that GN and Hardware Unboxed "1% low" matches CapFrameX "1% low average". https://www.computerbase.de/forum/threads/unterschied-1-low-und-p1.2226326/ (read 17 Nov 2026; forum, secondary).
- Recommended for this team, stated in frame time (lower is better): median frame time; P99 frame time = the frame time that 99 percent of frames are at or below (nearest-rank on the sorted list); "1% low average" frame time = mean of the slowest 1 percent of frames. Always name the definition next to the number.

## 5. Anti-cheat

- No primary source found stating that ETW capture is blocked or banned by any anti-cheat. UNVERIFIED either way.
- CapFrameX's own README describes a diagnostic example where a capture failed due to "missing administrator rights, or an anti-cheat that blocked PresentMon". https://github.com/CXWorld/CapFrameX (read 17 Nov 2026). So blocking is at least considered possible by the CapFrameX authors.
- EA forum thread on Battlefield 2042's newer kernel anti-cheat: RTSS and MSI Afterburner overlays (injection based) stopped working; users mention PresentMon as a workaround. No official EA reply. https://forums.ea.com/discussions/battlefield-2042-technical-issues-en/re-new-anticheat-broke-all-3rd-party-app-support/6968866 (read 17 Nov 2026; user posts, secondary).
- Practical: for the comparison walk, choose single-player games, or run offline where possible; do not use RTSS overlays in games with kernel anti-cheat.

## 6. Benchmark run practice

- Repeatable route and length: GamersNexus "Does benchmark duration matter", 1 Feb 2018: runs from 30 seconds to 5 minutes by game; 30 seconds is reliable when run-to-run spread is low, longer runs (5 minutes for Overwatch) when it is high; each test "a minimum of 4 times and averaged"; first-pass stutter seen in one game (shader or driver), so first passes can differ. https://gamersnexus.net/guides/3219-bench-theory-does-benchmark-duration-matter-one-year-testing (read 17 Nov 2026).
- Spread and reruns: GamersNexus "How reliable are benchmarks", 16 Feb 2018: "When deviation runs high, we typically just run more test passes"; error bars on charts; a 99th percentile metric "is less accurate because it draws on fewer data points"; a stutter caused by starting the capture just before recording skewed one run. https://gamersnexus.net/guides/3240-bench-theory-reliability-standard-deviation-game-benchmarks (read 17 Nov 2026).
- 2025 practice: GN logs 30 seconds with the PresentMon console app, averages multiple passes, ignores VSync and VRR for hardware comparisons. GN animation error page above (read 17 Nov 2026).
- CapFrameX blog: for P0.1 and P0.2 have more than 1000 frames; 0.1% lows from few frames vary run to run; state tool and method. CapFrameX metrics blog above (read 17 Nov 2026).
- Digital Foundry method: not reached, UNVERIFIED. Intel's PresentMonLauncher article gives no run method (min, max, average FPS only). https://intel.com/content/www/us/en/developer/articles/technical/presentmonlauncher-dx12vulkan-benchmarking.html (read 17 Nov 2026).
- No source read here recommends the median specifically; reporting median plus P99 frame time is a reasonable choice but not sourced. UNVERIFIED as "professional practice".

Proposed procedure (team's own decision, built from the above): same PC, same resolution and settings class, VSync and frame generation off, frame cap off; one marked route of about 60 seconds walking a street at a fixed pace; load in, wait 30 seconds still, then do one discarded warm-up pass (shader compilation and streaming); then 4 recorded passes (more if the median varies more than about 3 percent between passes); capture with presentmon --process_name X --timed 60 --terminate_after_timed --output_file run_N.csv, started a few seconds before walking; report per pass median, P99 and 1% low average frame time from MsBetweenAppStart, and the median of the passes; log VRAM per second in parallel.

## Unreached

- https://github.com/GameTechDev/PresentMon/blob/main/LICENSE.txt (fetch permission not answered): licence text read only via sidebar and README.
- https://github.com/GameTechDev/PresentMon/blob/main/README-ConsoleApplication.md (blocked; the same file was read via raw.githubusercontent.com).
- https://newreleases.io/project/github/GameTechDev/PresentMon/release/v2.6.1 (blocked): v2.6.1 existence and date UNVERIFIED.
- GitHub API for the PresentMon repository (repository not configured for this session), so release dates with years were not read directly.
- https://github.com/Dy-Baby/PresentMon (rate limited): 1.x README table not read; 1.x columns taken from current code's legacy writer.
- A Microsoft Learn reference page for the "GPU Process Memory" and "GPU Adapter Memory" counter sets: not found. Confirm names on the PC with Get-Counter -ListSet 'GPU*'.
- Digital Foundry benchmark methodology: not searched in time.
- PresentMon README-CaptureApplication.md full metric table (only the memory rows were extracted).
