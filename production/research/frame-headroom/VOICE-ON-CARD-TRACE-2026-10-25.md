# The frame spike with the cast voice on the card: a trace of the moment (25 October 2026)

His order of 25 October, item 4: "then the frame spike while the voice speaks (42 to 55 ms)". On 23 October the spike was measured with Pocket on the processor (43.9 to 54.8 ms, one frame each, at about 5.4 s into the walk) and set aside after two tries, its next step a trace of that moment (FINDINGS-2026-10-23.md). Tonight the voice is the cast's own, on the graphics card, as his friends' evening will have it.

## The capture

- tools/p1-packaged.ps1 -Only day-walk -Tag trace25b -VoiceSeconds 300, with the game's own switches `-trace=default,gpu,memory -tracefile=...` passed from PowerShell in the same session (the first try this evening, trace25, lost them through `powershell -File` and wrote no trace).
- The packaged game (F:/LedgerTools/played-game), High, his screen size at 55%; the cast voice speaking without a break (voice_load.py, whole sentences, the game's default).
- Result (production/research/pre-production/p1-packaged/runs.jsonl, packaged-day-walk-trace25b): median 13.11 ms, slowest 1% 60.3, **worst 441.9 ms, 4 frames over 33.3**; card memory in all peaks at 9,554 MB. The earlier run this evening without a trace: worst 238.6, 11 over 33.3.
- Trace: F:/LedgerTools/scratch/trace/walk-cast-2026-10-25.utrace (2.0 GB), read with Unreal Insights' own export (`TimingInsights.ExportTimingEvents`, run headless with -NoUI -AutoQuit -ExecOnAnalysisCompleteCmd; the command's quotes must sit after the equals sign, so it is started from PowerShell).

## What the trace shows

| Card frame | Its length | The game's own drawing inside it | The rest |
|---|---|---|---|
| 78.77 s | 503.5 ms | 16.1 ms | 487 ms |
| 93.28 s | 79.4 ms | 7.9 ms | 72 ms |
| 93.37 s | 41.0 ms | 8.6 ms | 32 ms |
| 96.14 s | 90.9 ms | 8.9 ms | 82 ms |
| 98.70 s | 33.8 ms | 9.2 ms | 25 ms |

- In the 442 ms game frame, every processor thread waits on the card: the game thread on the render thread (431 ms), the render thread on occlusion results (425 ms), a worker on the card ("waiting for the GPU for occlusion queries"), the RHI thread idle (421 ms).
- On the card, the frame's work is submitted at 78.79 s but its scene starts only at 79.26 s and takes 16 ms. For 487 ms the card ran work that was not the game's.
- The game's own slow card frames are different: 26 to 29 ms frames whose own drawing fills most of them (21.6 to 27.0 ms), none over 33.3.
- **So, with the cast voice on the card, the spikes are the card being shared:** the voice's work (another process) holds the card for up to half a second while the game's frame waits in line. It is not the game's drawing, and not the processor (the 23 October spike with Pocket on the processor was the processor oversubscribed at one moment of the walk).
- Not yet shown directly: which of the voice's passes holds the card (the token loop, the flow decoder or the vocoder). The voice's own log was not timed against the trace.

## What it means

- His friends play on his PC with the voice on the card (his answer of 25 October). In play the voice speaks only while someone answers, so the stalls come then, a half-second freeze at worst, not all the time; voice_load speaks without a break, the worst case.
- The voice decision on his page (Needs you 2) bears on this too: with the voice on the processor (Pocket), the card stalls go and the 23 October processor spike remains.

## Research (a helper, read 25 October; its notes and proxy tests in the session's scratch folder)

- **This card's driver refuses hardware scheduling** (dxdiag: "DriverSupportState: AlwaysOff"), so Windows itself shares the card between the two programs, and the setting would change nothing.
- **Pre-emption is coarse here:** the card reports compute pre-emption at the boundary of a whole batch of work (a "DMA buffer"): a running batch cannot be stopped, only those waiting (Microsoft, "GPU preemption", and the DXGI compute pre-emption granularity page).
- **The voice runs on the card's compute engine** (torch-directml), and Unreal 5.8 turns on async compute for AMD by default (D3D12Adapter.cpp), so some of the game's passes share that engine with the voice; Unreal makes every queue at normal priority (D3D12Device.cpp).
- **A program may set its own priority on the card** (D3DKMTSetProcessSchedulingPriorityClass), checked here for every class from a normal session; torch-directml itself offers no queue, priority or flush setting.
- **Vendors' advice** for machine learning beside rendering: short dispatches, interleaving, async compute with a low-priority hint (NVIDIA only); Microsoft's DirectML timeout guide: shrink the dispatch. No AMD document found.
- **Proxy tests** (a stand-in workload, not the game): a task on the compute engine waited up to 38 ms beside the stand-in voice; 12 ms with the voice at idle priority; 7 ms with the voice reading back a small result after each 11 ms layer. A task on the 3D engine never stalled.
- **Ranked levers:** the game off async compute; the voice at idle priority; the voice's work in bounded pieces (a read-back after each layer or slice); pauses or idle-window scheduling; less card memory for the voice.

## Two tries (same capture as above: the packaged walk, the cast voice without a break)

| Run | Median | Slowest 1% | Worst | Frames over 33.3 | Card median |
|---|---|---|---|---|---|
| Before (trace25b; the earlier run this evening) | 13.11 | 60.3 | 441.9 (238.6) | 4 (11) | 9.63 |
| Try 1: the voice at idle priority on the card (LEDGER_VOICE_CARD_PRIORITY=idle; the setting took, status 0) | 13.47 | 69.6 | 339.4 | 10 | 11.77 |
| Try 2: and the game off async compute (-DisableAsyncCompute) | 14.17 | 39.0 | 118.0 | 6 | 13.44 |

- Try 1 changed nothing that the run-to-run spread does not cover.
- Try 2 cut the worst frame to 118 ms and the slowest 1% to 39 ms, at about 2 ms more on the card's median frame, but six frames still pass 33.3 ms.
- **Set aside after two tries (his rule).** Nothing is changed by default: the voice's priority switch stays off unless set, and the game keeps async compute.

## Where the next go should look (research, not a try)

1. **Card memory.** In every run the card's memory in all peaked at 9.5 to 10.1 GB on a 10 GB card (the game 5.8, the voice 2.1, the rest Windows and other programs). Near the top, Windows pages one program's data out to make room for the other's, and a frame waits for its data to come back. That alone could hold the card for hundreds of milliseconds. Next: read the paging events (Windows' own GPU trace) at a spike, or run once with the voice's memory cut.
2. **The voice's work in bounded pieces** (the proxy's best result): a small read-back after each layer, the decoder and vocoder in slices.
3. The voice decision on his page (Needs you 2) settles this too if the voice moves to the processor.
