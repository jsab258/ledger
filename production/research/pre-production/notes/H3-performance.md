> **Helper evidence note** for the pre-production review of 3 October 2026, kept as written by a read-only helper. Corrections found on checking are listed in ../SOURCES.md, "Corrections to the helper notes"; where they differ, the numbered sections govern.

# H3: Inputs for a per-asset performance budget (LEDGER, Quay Street)

Researcher's report, 3 October 2026, about 35 minutes. Repository read-only at /home/user/ledger (HEAD includes build-machine commit 3a6a220, 3 Oct 12:35). Nothing in the repository was changed.

Marks: **MEASURED** = a number printed by a run on Jafar's PC (Ryzen 5 5600X, AMD RX 6700 10 GB, UE 5.8). **ASSUMED / ESTIMATE** = written by a session or helper without a run. Web sources: **READ** = page fetched and its text read (through the fetch tool's extraction, which quotes but may summarise); **SNIPPET** = search-engine summary only; **UNREACHED** = blocked or not loaded, not evidence.

---

## The target (ruling)

- 60 fps at 3440x1440 on the RX 6700 (10 GB) with the voice running, never below 30, met by rendering smaller and upscaling (Jafar, 23 and 24 Sep; DECISIONS archive line 216; production/drafts/rulings-2026-10-03/RULINGS.md:41).
- Frame budget: 16.67 ms (60 fps); hard floor 33.3 ms (30 fps).
- Internal resolutions for 3440x1440 output (arithmetic): 50% = 1720x720 (1.24 MP); 55% = 1892x792 (1.50 MP); 58% = 1995x835 (1.67 MP); 67% = 2305x965 (2.22 MP, about 1080p's 2.07 MP); 70% = 2408x1008 (2.43 MP); 100% = 4.95 MP (1.34x a 2560x1440 frame).

---

## Part A: what the repository measured

### A1. Engine and rendering features in force (MEASURED from config and the probe's cvar print, 3 Oct)

| Item | Value | Source |
|---|---|---|
| Engine | Unreal Engine 5.8 (also a 4.0 install present) | production/d1-probe/ue-machine.txt (3 Oct, commit 5db99d5) |
| RHI | DX12, Shader Model 6 only | ue-probe/Config/DefaultEngine.ini |
| Global illumination / reflections | Lumen, software tracing (r.DynamicGlobalIlluminationMethod=1, r.ReflectionMethod=1, mesh distance fields on) | DefaultEngine.ini; cvarDynamicGI=1, cvarReflectionMethod=1 |
| Hardware ray tracing | Compiled in (r.RayTracing=True, skin cache shaders), OFF at runtime (r.RayTracing.Enable=0, r.Lumen.HardwareRayTracing=0) | DefaultEngine.ini |
| Lumen translucency front-layer reflections | On (1 Oct, shop glass) | DefaultEngine.ini |
| Virtual shadow maps | **OFF** (cvarVirtualShadows=0; nothing in DefaultEngine.ini sets it) | production/d1-probe/ue-vignette-verdict.txt line 206 |
| Nanite | Enabled engine-wide (cvarNanite=1), but **every mesh under /Game/Ledger has Nanite switched off** (audit: naniteAuditOn=0, CLEAN). Policy since 23 Sep: "every mesh is meant to draw its full triangles" | tools/ue/nanite_audit.py; tools/ue/import_*.py; probe verdict |
| Anti-aliasing / upscaler | r.AntiAliasingMethod=4 (TSR). No FSR plugin found in config | probe cvar print |
| Screen percentage | cvar 0 (default) in shots; the perf step forces r.ScreenPercentage=50 | ledger-probe-unreal.yml step "Time the slice" |
| Volumetric fog, contact shadows, bloom, AO, motion blur, auto exposure | all on (1) | probe cvar print |
| MegaLights / Substrate | absent / 0 | probe cvar print |
| Scalability | No DefaultScalability.ini: engine defaults. The packaged game's saved settings on the PC: "Highest", every group at 3 (Epic) | STREAMING-IN-GAME-2026-10-01.md |
| First-launch tuner | Steps render scale 100 -> 70 -> 55%, then drops a scalability level, until a frame is at most 16 ms | ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:59-76 |
| MetaHumans | Assembled with the **UE Optimized** pipeline at **High** quality (one build at Medium on 25 Sep when High ran out of memory); hair from the MetaHuman plugin's grooms | tools/ue/make_cast_metahumans.py:998-1002; assemble_metahuman.py:107-108 |
| Texture streaming pool | Not set in config (engine default for Epic texture quality). One test capped it at 600 MB | voice-latency/EVIDENCE-2026-10-01.md |

Note: the asset plan (production/research/asset-plan/1-BUILDINGS-AND-INTERIORS.md and 2-VEHICLES.md) prescribes Nanite static meshes for buildings and car bodies, and the aaa-street note recommends VSM on Nanite with caching. The game today runs Nanite off and VSM off (conventional cascaded shadow maps). This conflict is unresolved and changes every triangle budget below.

### A2. Frame times

**(a) The slice perf step, every build-machine run** (production/d1-probe/ue-perf-verdict.txt; history only back to 1 Oct because the history was imported on 30 Sep). Conditions: packaged build, `-LedgerSlice` (the playable street: 3 cast MetaHumans, 3 Mixamo stand-in people, the player character; cars kept off), standing still, 3440x1440 forced, **r.ScreenPercentage=50 (TSR)**, VSync off, uncapped, `-RenderOffScreen` (nothing presented to a display), 1500 frames after dropping 300, engine CSV profiler. Nano TTS (built-in voice) speaks on the same card through the capture (nanoRtfMedian 1.27-1.82). Scalability: the build machine's saved settings (stated elsewhere as Highest/Epic; not printed in the verdict).

| Date (run) | median ms | p95 | p99 | worst | fps | GPU median ms | frames > 16.7 | gpuMemMB (LocalUsed) |
|---|---|---|---|---|---|---|---|---|
| 1 Oct 18:04 | 13.42 | 14.97 | 16.72 | 19.03 | 74.5 | 11.79 | 15 | 4079 |
| 1 Oct 21:48 | 12.72 | 15.78 | 21.96 | 40.90 | 78.6 | 11.19 | 46 | 4149 |
| 2 Oct 11:42 | 12.94 | 15.64 | 17.36 | 25.26 | 77.3 | 11.32 | 23 | 3775 |
| 2 Oct 16:15 | 13.37 | **57.73** | **67.67** | 213.94 | 74.8 | 11.43 | 419 | 3805 (status BELOW-30; Nano RTF 1.79; cause not recorded) |
| 3 Oct 07:34 | 12.81 | 14.56 | 16.12 | 18.30 | 78.1 | 11.37 | 7 | 3715 |
| 3 Oct 12:35 (latest) | 13.32 | 15.05 | 16.73 | 19.62 | 75.1 | 11.43 | 15 | 3681 |

Range over the 20 runs 1-3 Oct: median 12.7-13.4 ms, GPU median 11.2-11.8 ms, p99 16.1-17.4 ms (except the outliers), local GPU memory 3.6-4.1 GB. Status MEETS on all but one run. The p99 already sits on the 16.7 ms line.

**(b) Earlier, 24 Sep** (production/research/nano-listening-test/card-timing-2026-09-24.md; build before MetaHumans fully in, before shop rooms and cloth): slice at 1280x720 8.4 ms median (120 fps), game 3.0 GB; at 3440x1440 SP50 11.8 ms (85 fps), 3.5 GB; same with Nano speaking 12.5 ms median, 16.0 ms slowest 1% (80 fps), game 3.5 GB + Nano 2.1 GB. Another 24 Sep reading: 79 fps, slowest 1% at 74, 4.6 GB (FOR-JAFAR archive line 90). ROADMAP "73 fps at his screen size" (24 Sep). Checklist sweep 29 Sep: "70.7 today" (conditions not stated).

**(c) Packaged game at full 3440x1440 (SP100), 30 Sep, title screen measure** (TitleScreen.cpp comments): Highest (Epic) 26.3-26.4 ms (~38 fps); High 15.1 ms; Medium 7.9 ms. Build machine, Highest at SP50 with voice: 14.3 ms.

**(d) Shots at 1280x720** (ue-vignette-verdict.txt, 3 Oct, median of engine frame deltas, 24 frames after 8 warm): street by day 8.1-9.1 ms; wet night 10.2-10.7 ms; the "corner" street 10.26 ms; the corner with every feature on (cinematic scalability, VSM, hardware ray tracing for Lumen, volumetric fog, contact shadows) 25.72 ms.

**(e) Ray-tracing scene compiled in and enabled but unused**: 5.13 -> 8.76 ms median at 1280x720, i.e. +3.6 ms (DefaultEngine.ini comment; commit 67f514be; date about 23 Sep).

**(f) Walk probes** (ue-walk / ue-slicewalk verdicts, 3 Oct): 960x540 viewport, SP default: median 6.89-6.98 ms, p95 15.4-15.5 ms, worst 88-91 ms, 22-23 frames over 33 ms per ~850 frames (hitches while walking, cause not recorded).

**(g) Per-MetaHuman GPU cost** (production/d1-probe/metahuman-cast/ue-mhcost.txt; file first appears in the 30 Sep import, run date and resolution NOT recorded): each MetaHuman standing 3.5 m in front of the camera in the street, uncapped, RHIGetGPUFrameCycles, 300 frames:

| Condition | GPU median ms | delta GPU ms | texture MB | delta tex MB |
|---|---|---|---|---|
| nobody | 9.52 | 0 | 2380 | 0 |
| Rocco | 9.83 | +0.31 | 2407 | +27 |
| Lena | 9.86 | +0.34 | 2415 | +35 |
| Sam | 9.89 | +0.36 | 2423 | +43 |
| all three | 10.15 | +0.63 | 2423 | +43 |
| MH_Test | 9.84 | +0.31 | 2428 | +48 |

So: about 0.2-0.35 ms GPU and 27-48 MB of texture memory per Optimized/High MetaHuman at 3.5 m, at an unrecorded resolution. Game-thread, animation and RigLogic CPU cost not measured.

**(h) Simulation**: 0.07 ms per simulated person per frame, measured in the Unity era (game-design/research/performance-budget.md), not the UE build. Animation, cloth and RigLogic costs in UE: unmeasured (townspeople-animation/DELIVERY.md table says so).

### A3. Memory

- Card: "about 9.4 GB usable" of the RX 6700's 10 GB (24 Sep, card-timing note).
- Game (slice CSV, GPUMem/LocalUsedMB): 3.6-4.1 GB, 1-3 Oct; texture RHI memory 2.38-2.43 GB in the MetaHuman cost probe.
- Game (Windows counters, packaged game in the street beside the AI tester, 1 Oct, resolution not stated): 4.8-6.1 GB dedicated; card total 7.7-9.3 GB in use (EVIDENCE-2026-10-01.md step 0). Same note, 2 Oct: 4.9 GB.
- System RAM of the game: not recorded anywhere found.

### A4. The voice (TTS) today

- Program: Chatterbox Nano voice server, PyTorch with DirectML **on the graphics card** (token loop and flow); "Today's voice stays: whole sentences, flow on the card" (STREAMING-IN-GAME-2026-10-01.md, status line). Earlier (24 Sep) the final waveform step ran on the processor because DirectML lacked complex numbers.
- Memory: alone, 2.7-2.8 GB dedicated + about 1 GB shared; beside the game it got only 1.40 GB dedicated + 2.03 GB shared and crashed in DirectML (1 Oct). 24 Sep: 2.1 GB beside the game.
- Contention: beside the game the voice's token step ran at 12.2-12.4 tokens/s on the card versus 80-93 alone; with the game's texture pool capped at 600 MB (r.Streaming.PoolSize=600, texture quality 0) it ran at 35.3-36.6 tokens/s, i.e. three times faster (2 Oct 10:36). First sound beside the game (game at 1280x720 windowed): 3.66 s median on the card; 3.44 s with the 600 MB pool; 4.40 s on four CPU cores (2 Oct 14:00).
- Frame caps (60 or 30) and half resolution did not change the voice's speed (STREAMING-IN-GAME note).
- Model files: Nano step graph 406 MB ONNX (102 MB int8); August export graphs about 3 + 3 + 2 GB fp32 (not used by the game). The talk model is a remote paid router, not local (DECISIONS 24 Sep line 12); local LLM tests used 3.0-3.2 GB of card (23-24 Sep) but are not in the game.
- Item 3 on the builder's list (decoder as 8-bit compiled graph on the processor) is still open: the voice may move partly off the card.

### A5. Assets as they are (MEASURED by me today from the GLBs in production/assets; counts from accessors, textures from embedded image headers)

| Asset | Triangles | Vertices | Materials | Embedded textures |
|---|---|---|---|---|
| Mixamo stand-in people (6) | 47,869-59,192 | 30-37k | 2 | 3-5 x 1024^2 |
| Player, tom-player | 56,258 | 35,787 | 3 | 8 x 1024^2 |
| Street (quay-street.glb, 112 meshes) | 183,416 total | 457,434 | per mesh | none (materials applied in Unreal) |
| Street clutter (bollard, bins, pillar box, pole, kiosk) | 950-7,548 each | | 1-5 | none |
| Parked hatchbacks (2 variants) | 15,294 each | 30,340 | 9 | none |
| Pawnbroker shop display | **203,355** | 229,628 | **48** | **83 x 512^2** |
| Poly Haven surfaces (brick, asphalt, concrete, pavement) | n/a | | | 2K JPG sets (diff, nor, rough, ao) |

Shop rooms behind the glass, garments and the current MetaHumans live on F:\LedgerTools and in the Unreal project, not in git: their triangle and texture figures were not available here.

### A6. People, cars and cloth in the build

- People in the playable street: 3 cast MetaHumans (Lena, Rocco, Sam) + 3 Mixamo stand-ins + the player (production/specs/street-people.json). Townspeople walking: two of the stand-ins have walks in free play only.
- Cars: two parked hatchbacks exist but are "kept off the street" (street-vehicles.json: vehicles 0). Moving traffic: not built.
- Cloth: Chaos cloth used only in tests (suit jacket skirt, 1 Oct; donkey jacket rounds). No cloth cost measured. Epic's showcase jacket "ran at about 30 fps" (game-clothing-pipeline note, citing a source).
- Hair: plugin grooms through the Optimized/High pipeline; strands vs cards at each LOD not recorded in the repository.

### A7. What the repository does not have

- No per-pass GPU breakdown (stat gpu / ProfileGPU / Insights) of any scene.
- No draw-call, primitive or triangle-in-frame counts.
- No measurement of the hook camera (the proof view), of the shop rooms, of night with lit windows, of moving people, cars or cloth.
- No measurement with the cast voice server (the slice-perf step runs Nano's built-in voice via nano_card_timing.py), and no system-RAM figure.
- The slice-perf step renders off-screen; presentation and compositor cost on the 3440x1440 desktop are excluded. A comment in the workflow says "The voice is not running here" while the code below it starts Nano; the verdict's slicePerfVoice line shows Nano did run.
- ROADMAP's own note (line 74) still says the last measurement is from 24 Sep; the build machine has in fact logged the slice at every run since at least 1 Oct.

---

## Part B: published sources

### B1. Epic documentation (UE 5.8 pages, undated; accessed 3 Oct 2026)

| Claim | Source | Mark |
|---|---|---|
| "Lumen targets 30 and 60 frames per second (fps) on consoles with 8ms and 4ms frame budgets at 1080p for global illumination and reflections on opaque and translucent materials, and volumetric fog." Epic scalability targets 30 fps; High targets 60 fps on current consoles; Medium targets Switch 2 and lower-end PCs. Lumen uses async compute on consoles. | https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine | READ (verbatim quotes) |
| Hardware RT: "fewer than 100,000 instances in the Ray Tracing Scene after culling" for good console performance. | same | READ |
| TSR: ~0.79 ms at r.ScreenPercentage=100 and ~0.43 ms at 50 (Valley of the Ancient, console); Fortnite Ch.4 on PS5/XSX: effective TSR cost 1.5 ms, async compute offsets ~0.5 ms; City Sample: 57.50 ms native 4K vs 33.37 ms at 1080p upscaled to 4K. Feed table: 4K at 50% and 1080p native both 124.4 MP/s at 60 Hz. | https://dev.epicgames.com/documentation/en-us/unreal-engine/temporal-super-resolution-in-unreal-engine | READ |
| VSM: 16k x 16k virtual, 128x128 pages; "Non-Nanite geometry is much more expensive to render into VSMs than Nanite geometry"; no ms or MB figures. | https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine | READ |
| Nanite: no per-triangle cost or memory figures on the overview; scene limit 16 million instances; "performance should be carefully measured for any combination of content and hardware". | https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine | READ |
| Texture streaming: r.Streaming.PoolSize in MB (0 = unlimited); no default sizes or per-VRAM recommendations on the page. | https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine | READ |
| Scalability reference: texture streaming pool by texture quality Low 200, Medium 400, High 700, Epic 1000 (MB); Epic shadows up to 4 CSM cascades. Page content looks carried over from UE4; treat the pool values as indicative. | https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-reference-for-unreal-engine | READ (fetch summary) |
| City Sample requirements: 12-core 3.4 GHz, 64 GB RAM, at least 8 GB VRAM, RTX 2080 / Radeon 6000 or higher. | https://dev.epicgames.com/documentation/unreal-engine/city-sample-project-unreal-engine-demonstration | READ |
| Draw calls: the only Epic numbers found are mobile (about 700 on Galaxy Tab S6, under 500 lower-end). No PC figure. | https://dev.epicgames.com/documentation/en-us/unreal-engine/guidelines-for-optimizing-rendering-for-real-time-in-unreal-engine | READ |

### B2. MetaHuman specifications

Source: Epic, "Platform Support and LOD Specifications for MetaHumans", https://dev.epicgames.com/documentation/metahuman/platform-support-and-lod-specifications-for-metahumans (undated). READ. Vertices, not triangles (triangles not given; for closed skin meshes roughly 2x vertices is a rule of thumb, unverified).

| Head LOD | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Vertices | 24,000 | 12,000 | 6,000 | 2,500 | 1,300 | 560 | 270 | 130 |
| Joints | 713 | 529 | 397 | 283 | 84 | 70 | 41 | 26 |
| Blendshapes | 669 at LOD0 only | | | | | | | |
| Skin influences | 12 | 12 | 12 | 8 | 8 | 8 | 4 | 4 |
| Animated maps | yes | yes | no from LOD2 | | | | | |

| Body LOD | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Vertices | 30,500 | 7,600 | 3,350 | 1,507 |
| Correctives | yes | yes | no | no |

Hair: strands 50,000 (LOD0), 25,000 (LOD1); hair cards 30,000 / 15,000 / 10,000 / 3,000 / 1,500 vertices (LOD0-4); hair mesh 500 / 250 / 100 (LOD5-7); facial hair strands 10,000 / 5,000; facial hair cards 15,000 down to 500; hair physics LOD0-2. Platform table: PC strands and cards, best LOD 0, max texture 8192.

Other MetaHuman facts:
- Head 8 LODs, body 4, synchronised by LODSync; "setting Forced LOD to 0 or 1 for a large number of MetaHumans (for example, a crowd) can negatively affect your game's performance"; `r.HairStrands.UseCardsInsteadOfStrands 1` for crowds. https://dev.epicgames.com/documentation/metahuman/controlling-metahuman-levels-of-detail-lods-in-unreal-engine READ.
- Assembly: UE Cine "average size is between 1 - 2 GB", strands on LOD0, textures up to 8K; UE Optimized "average size is under 100 MB", compressed textures, highest texture 2K, correctives switched by LOD, LODs "more aggressive"; Low = "hair cards, no correctives, and no physics". https://dev.epicgames.com/documentation/metahuman/assembly?lang=en-US READ; https://dev.epicgames.com/documentation/metahuman/metahuman-materials-and-textures?lang=en-US READ (scatter 512, animated basecolor delta 512, animated normal delta 1K by default).
- Crowds (5.8, Experimental): full actors near, Instanced Skinned Mesh far, no post-process anim BP (no correctives) far, grooms converted to cards, high LODs stripped; example "10 full-quality actors at close range but hundreds of instanced characters at a distance". Repo crowd note (casting/notes/crowd.md) marks these OPENED; not re-read today.
- Groom cost: Epic's Groom Scalability page (UE 5.8) gives no ms or memory figures; READ. Third-party "several milliseconds per character" for strands: strayspark.studio blog, SNIPPET, low reliability. Repo: 50 card-only MetaHumans ~800 MB VRAM for grooms (~16 MB each), RTX 3070, forum 16 Mar 2026 (repo marked OPENED/MEASURED by user; not re-read). James Roha "3-6 ms GPU per strand MetaHuman" (repo: SNIPPET, do not rely).
- Correctives off: ~40% editor fps with 32 LOD0 MetaHumans (forum 2024, Ryzen 5800X / RTX 4070 Ti Super; repo OPENED).
- Animation Budget Allocator default a.Budget.BudgetMs=1.0 game-thread (Epic doc via repo, OPENED).
- Chaos cloth: about 0.35 ms per cloth asset at LOD0 with under 300 sim vertices, PBD only, no self-collision (forum thread "How to setup low budget Chaos Cloth sim?", https://forums.unrealengine.com/t/how-to-setup-low-budget-chaos-cloth-sim/2701370), SNIPPET. No Epic cloth cost figure found.

### B3. Benchmarks on RX 6700-class cards

Almost every hardware site was UNREACHED (egress blocked): techpowerup.com, techspot.com, en.gamegpu.com, computerbase.de, tomshardware.com, dsogaming.com, notebookcheck.net, hardwaretimes.com, karanbenchmarks.in, low-poly.com. Everything below is SNIPPET and is not evidence by the project's rule; it should be re-read from Jafar's PC.

| Game (engine) | Card, settings | Figure | Source | Mark |
|---|---|---|---|---|
| KCD2 (CryEngine, no RT) | RX 6700 XT, native 1440p Medium | "well over 60 fps" | TechSpot, https://www.techspot.com/review/2952-kingdom-come-deliverance-2-benchmark/ | SNIPPET (page UNREACHED) |
| KCD2 | RX 6700 XT, 1440p maximum / Experimental | ~25 fps | GameGPU | SNIPPET |
| Mafia: The Old Country (UE5, 2025) | RX 6700 XT, 1440p | 59 fps (settings unknown) | search summary of gamegpu / others; TechPowerUp review 11 Aug 2025 UNREACHED | SNIPPET |
| Hellblade 2 (UE5) | RX 6700 XT, native 1440p max | ~25 fps | GameGPU Enhanced | SNIPPET |
| Silent Hill 2 remake (UE5) | RX 6700 XT, 1440p | ~41 fps all High; ~62 fps "optimized" | theframecoach.com | SNIPPET, low reliability |
| Stalker 2 (UE5) | RX 6700 XT | needs upscaling to hold 60 at 1080p Epic (repo, aaa-street 3-LIGHT) | repo citing search summaries | SNIPPET |
| 3440x1440 on RX 6700/6700 XT, UE5 | none found except a YouTube path-tracing video | n/a | | none |

The RX 6700 (non-XT, 36 CUs, 10 GB) is slower than the 6700 XT (40 CUs, 12 GB); the repo cites it as "about a PS5's GPU" (search summary). No direct RX 6700 non-XT UE5 benchmark was reached.

### B4. Published per-asset budgets

- Character triangles: "hero 30k-80k triangles with 3-5 LODs, hair cards 5k-15k" for PS5-class non-Nanite skinned meshes; NPCs 5k-25k (low-poly.com "polygon budgets by platform 2026", page UNREACHED; SNIPPET). Forum claims of 200-350k for heroes (SNIPPET).
- Draw calls on PC: "mid-range PCs comfortably manage 2,000-5,000 draw calls" under DX12 (blog/forum SNIPPET, low reliability).
- Cars: lyoshko "1980s Cars Pack" LOD0-3, 54-72k vertices; RenderHub 80s sedan 39,973 polygons; Sketchfab "Fairheaven LT '80" 19.7k triangles (repo aaa-street 4-VEHICLES, SNIPPET). Asset plan's own budget: 15-25k triangles plus wheels (ESTIMATE).
- Buildings: City Sample "seven million instanced assets", 7,000 buildings from thousands of modular pieces (Epic/press, SNIPPET for figures); modular kit on a 1 m grid at 1K texels per metre (repo 5-PROOF-FRAME D2, SNIPPET). Asset plan: three 4096x2048 trim sheets shared by all styles (ESTIMATE).
- Accessories (asset plan, ESTIMATE): bags and headwear 1-4k, scarf 1-2k, watch 0.5-1k, newspaper and stick under 1k triangles.
- No published per-asset VRAM budget for 8-12 GB cards was reached.

---

## Inputs I would use to derive the per-asset budget

1. **GPU frame budget.** 16.7 ms total; plan to about 14 ms GPU at the median so the p99 stays under 16.7 ms with the voice contending (today the p99 already touches 16.7 at a 11.2-11.8 ms GPU median). Measured baseline at SP50, Epic scalability, with the slice's content and Nano speaking: GPU 11.2-11.8 ms. Headroom for everything the proof view adds (rooms behind glass, 40-60 props, the hill, cars, more people, night): about 2-3 ms GPU at SP50, unless render scale (55%) or scalability (High: 15.1 ms at SP100 vs Epic 26.3) is spent.
2. **Fixed costs to subtract** (published, console, not this card): Lumen GI + reflections + volumetric fog 4 ms at 60 fps / 8 ms at 30 fps at 1080p internal (Epic); TSR about 0.4-1.5 ms; HW RT scene +3.6 ms (measured, keep off).
3. **Per-person GPU**: measured 0.2-0.35 ms each for an Optimized/High MetaHuman at 3.5 m (resolution unrecorded); CPU and animation unmeasured; Epic LOD table above for geometry; Optimized textures max 2K, under 100 MB per character; cards for anyone beyond the nearest few.
4. **Per-person memory**: measured 27-48 MB texture each; groom cards ~16 MB each (forum).
5. **VRAM envelope**: 9.4 GB usable; voice needs about 2.8 GB dedicated to run at full speed; game measured 3.6-4.1 GB (CSV) or 4.8-6.1 GB (Windows counters). A game budget near 5.5-6 GB including the texture pool, and a fixed r.Streaming.PoolSize, are the levers; a 600 MB pool made the voice three times faster.
6. **Triangle side**: with Nanite off and VSM off, every triangle is drawn into the base pass and the cascaded shadows at each LOD; budgets need LOD chains (Epic: 3-5 LODs typical for skinned). Current reference points: street 183k triangles total, stand-in people about 50k, cars 15k, clutter 1-7.5k, one shop display 203k with 48 materials (an outlier to fix first).
7. **Texture side**: 2K surfaces today; MetaHuman Optimized 2K; trim sheets 4096x2048 planned; the Epic texture-quality pool 1000 MB as the default ceiling.
8. **What must be measured before budgets are fixed**: one ProfileGPU / stat gpu capture of the hook camera at 3440x1440 SP50 and SP67, day and night, with the cast voice server running; draw calls and primitives (stat rhi / stat scenerendering); the same frame with Nanite on for buildings and VSM on, to settle the conflict in A1; one cloth garment on one walking person; one row of shop rooms; system RAM.

## Numbers I could not verify

- Every third-party benchmark in B3 (all SNIPPET; sites UNREACHED).
- Per-asset budgets from low-poly.com, draw-call ranges, strand hair "several ms", Chaos cloth 0.35 ms, groom 16 MB, correctives 40% (forum or blog; SNIPPET or repo-cited only).
- The scalability page's 200/400/700/1000 MB texture pool values for UE 5.8 (page looks UE4-derived).
- The date and resolution of the MetaHuman cost run (ue-mhcost.txt has none; first appears in the 30 Sep import).
- The scalability level of the build machine's slice-perf runs (not printed in the verdict).
- The resolution of the 1 Oct Windows-counter memory reading (4.8-6.1 GB).
- The cause of the 2 Oct 16:15 BELOW-30 run.
- "70.7 fps" of 29 Sep (no conditions recorded).
- Triangle counts for MetaHumans (Epic gives vertices only), shop rooms, garments and the new kits (not in git).
- The RX 6700 as "about a PS5 GPU" (repo, search summary).
