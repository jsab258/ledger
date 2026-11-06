# The Stutter on build 3641d53: diagnosis (6 November 2026)

Saved files only. [M] measured, [I] inferred, [U] unverified. Engine paths under UE_5.8/Engine/Source/Runtime.

## The measure was wrong three ways

- **One row late.** FrameTime in a row covers the frame before it (Core/Private/ProfilingDebugging/CsvProfiler.cpp:4369-4390; Launch/Private/LaunchEngineLoop.cpp:5704). All 19 spikes match the previous row's game or render thread within 4.1 ms [M].
- **Card memory is not steady.** The game's voice program (voice-server.py --prewarm, LedgerVoice.cpp:97) starts about 10 s before the capture and puts about 2 GB on the card inside it: the whole card rises from 7.5 GB to between 8.7 and 10.05 GB, the game's own figure staying near 6 [M]. All cast are on Pocket, yet that model always loads (voice-server.py:338) [M]. Corrects the 4 November memory diagnosis.
- **No present exists.** -RenderOffScreen removes the swap chain (D3D12RHI/Private/Windows/WindowsD3D12Viewport.cpp:34) [M]. Real play's present: unmeasured.

## 1. Kind A: the navigation rebuild on the game thread

- 7 of 8 spikes hold about 20 to 75 ms in Navigation_TickAsyncBuild, the game thread not waiting [M]: named, inside the game.
- The eighth (quietc, 192 ms): render thread 192, its stats total 11.5, card 8.3 [M]: a wait the stats do not name. (Corrected 6 Nov 15:50: the render thread's own stats sit one row earlier again: that row holds EventWait/Visibility 184 ms [M]. So the wait is named, the same as nomapc's 219 ms.) Also 6c808a1-series (196, 273).
- 13 of 15 stall moments fall while the voice program's memory jumps by gigabytes [M, windows drawn by eye]; the mechanism is [U].
- Against it as sole cause: 3 and 4 November runs with card steps inside show no stalls [M].
- Sampler: since 27161ea26 (4 November) about every 2.4 s, not 4.3, plus a process query. With card steps inside, old sampler 0 of 4 runs spiked, new 8 of 10 [M]; dates confound this. Whole-second stamps cannot place spikes; no frame-time peak at its cycle [M, weak].
- Pocket: stalls reach 33 ms without it, 75 with [M].
- Excluded [M]: CSV stalls (hasgtstalls 0, 23 files), garbage collection (no column, no log line), perf-hook (runs afterwards).

## 2. Kind B: the card goes over budget

- The program's second gigabyte drops Windows' budget to about 5.7 GB. All three walks go over at rows 622 to 682; the stall comes 3 rows later (render 55 to 96, card 37 to 127) [M]. Windows paging the game's memory [I] (D3D12RHI/Private/D3D12Adapter.cpp:1921-1925).
- The card then runs 1.1 to 1.4 ms slower to the end [M]: hence higher medians without the voice.
- Voice walks: the drop comes later (frames 1637 to 1762, 5.8 GB in use) or after the end, over by 11 to 138 MB, no stall. No-voice: over by 362 to 422 MB, at the walk's 6.1 GB peak [M].
- Other programs hold about 1.8 GB of the card, against 250 MB in the earlier no-voice walks [M]; which programs: [U].

## 3. Kind C: the same as A

The 40.5 ms frame's real row (1357) has 34.9 ms of navigation [M], during the load.

- The 6 to 12 ms steps: geometry gathered on the game thread (bDoFullyAsyncNavDataGathering false, NavigationSystem/Private/NavMesh/RecastNavMesh.cpp:550; RecastNavMeshGenerator.cpp:1874-1884; unset in DefaultEngine.ini) [M].
- Trigger: tasks pending in 1,622 of 1,800 standing rows [M]. Each person's LiveBodyBlock capsule counts for navigation (CrimeProbe.cpp:1096; ShapeComponent.cpp:61; PrimitiveComponent.cpp:3672), so moving people dirty tiles [I].

## 4. New or old

- **A and C: old.** 6c808a1-series has 70.5 ms of navigation and 273 ms on the render thread [M]. Standing navigation grew, 3.05-3.25 s to 3.93 s [M]; cause [U].
- **B: not separable.** 6c808a1 has no no-voice run. The load is old [M]; the game's peak rose about 200 MB [M], likeliest the new art (hill, roof, wash) [I].

## 5. Test and first try

**Test:** five walks, -Voice pocket -GameArgs -NoVoice (LedgerVoice.cpp:84), sampler running. Stalls gone: the program is the trigger. Stalls remain: sampler or game; next, sampler off.

**First try:** voice-server.py loads the card model only when a line needs it. Mafia or Kingdom Come II method (studies/12-tech-budgets.md): none found. If stalls remain: the capsule off navigation, as Character.cpp:83.

**Confidence:** B high; A and C being navigation high; trigger medium; sampler open.

## Not checked

Windows trace; other programs' card use; raw p4-walk-novoice-a,b and cache-novoice (summary lines only). Raw files used: 2 to 6 November.

## The rare freeze after try 2 (6 November, 15:50)

Scan of every frame file kept under F:/LedgerTools/tmp/p1-packaged for frames over 60 ms [M]. In a file, three rows belong together: the frame time at row n, the render and game threads' totals at n-1, the render thread's own named stats at n-2.

- nomapc row 395: frame 231, render 230, Visibility 219. quietc row 1436: frame 192, render 192, Visibility 184.
- The early captures (the voice on the card) show the same wait in runs of frames, 55 to 212 ms. novoicea, b, c: 74 to 90 ms. 6c808a1-series (196, 273 ms) does not: Visibility 6 and 7 there, a different wait.
- The render thread is waiting for its visibility tasks, which run on the shared worker threads. Why those tasks are late is not read: nothing in the file says what the workers were doing [I]. Candidates, unproven: the voice program on four threads taking cores (the machine has 6 cores, 12 logical), or a page fault in a worker.
- Five walks with the voice program off had none (gamenovoice), but one freeze in ten walks with the voice cannot be told from none in five. Twenty more walks count it (labels *-7bef7cf-rate*).

The count (6 November, 16:40) [M]: of twenty more walks, 19 had none over, and rate16 had one frame of 39.2 ms, with no visibility wait. With the first five that is 25 walks, 45,000 frames: one freeze of 231 ms, one of 39 ms. The voice ran through each capture, without a break, harder than play. At this rate a fix could not be told from luck in under about 75 walks, some 3.5 hours of the machine, and the cause is still a guess.
