Method researched: 12-tech-budgets.md; 04-street-world.md; MEMORY-PLAN-2026-11-07.md; MEMORY-WHERE-2026-11-08.md
Reference: studies/12-tech-budgets.md; studies/04-street-world.md

# The street budget and scale test: method note (n16-3), 16 November 2026

Written by a helper from the project's notes, read 16 Nov 2026; nothing built or run. Unreviewed: one fresh reviewer checks it against its sources before step 1. "Est." is an estimate; "unverified" is not confirmed from a source or a measure.

**The method copied.** Kingdom Come II ships a performance-test quest that fills Kuttenberg with 1,000 to 2,500 people, far more than play needs (studies/12, "How a dense town holds its frame"); MEMORY-PLAN-2026-11-07.md §5 step 3 turns that into a test-only switch adding street copies and people. Mafia packs each street group into one kit actor (studies/04, "Unique buildings against kit"), so the copies are made that way, and Mafia's split of memory into named categories (studies/12, "Memory and streaming") sets how results are filed. Their numbers are used only where marked as fitting.

## 1. What "a district" means here

| Measure | The built street | The Hook, a district | Source |
|---|---|---|---|
| Area | - | 0.107 km² | atlas.json lines 70-123; MEMORY-PLAN §2; re-computed here (shoelace, 106,700 m²) |
| Road length | 48 m | about 500 m: Quay Street inside the Hook about 363 m, Harbour Board approach about 110 m, Mickey's yard lane about 28 m | atlas.json lines 555-620, 1020-1079; computed here from route points, unverified |
| Street-lengths | 1 | about 10 | the line above |
| Fronts | 10 shop units planned, 8 built; 10.25 m front to front | about 100 to 140, both sides at one front per 6 to 8 m, est. | studies/04 line 57; PIECES-DRAFT-2026-11-08.md line 28; Mafia's 8 m plot, studies/04 line 16 |
| Rooms | Mickey's office walked into; shop rooms are pictures | enterable only where the story goes; shells elsewhere | studies/04 target 5 |
| People | the cast and walkers | 0, 5, 10, 20 visible (phase 5's load counts) | PLAN.md line 41 |
| Cars | none passed | not set; Mafia parks none, spawns traffic | studies/04 line 50; n16-9 open |

**Faked cheaply, no art.** A switch `-ScaleTest=N` places N-1 copies of the built street's own static meshes, one instanced group per kit mesh per copy (Mafia's packed street actor), along the Hook's road lines through the atlas transform (atlas.json line 2009). `-ScalePeople=M` adds M stand-in walkers from existing bodies, walking, no talk. Measured at N = 1, 2, 4, 10 (the Hook) and 15 (Mafia's top loading range is 1.5 times its base, studies/12 line 9); people at 0, 5, 10, 20 and 40 at N=10 (40, twice phase 5's top count, is this note's choice, in Kingdom Come II's spirit).

Copies share every texture, so they under-count memory. Unique fronts are added by arithmetic: MB per one-off front from Rita's front in the owner dump (step 5) times the district's one-offs at Mafia's kit share (88% kit elements, studies/04 line 28). Cars are not faked: n16-9's hatchback, once passed, is measured alone and added.

**Precondition.** A DECISIONS.md entry before the switch is built, ruling it allowed against "nothing is multiplied": measurement only, never shipped, never on his page (MEMORY-PLAN §5 step 3; PIECES-DRAFT line 37).

## 2. Views and measures

**Views** (camera ids in production/specs/vignette-scene.json lines 788-827):
1. Hook camera by day (cam_hook).
2. Reverse view (cam_reverse).
3. Street at night (cam_hook with `-PerfHookNight`, CrimeProbe.cpp line 5356).
4. The hill: no camera exists; a new cam_hill at the street's end (x about 44) looking up the climb to the bend and backdrop (atlas.json lines 2035-2121), where copies are least hidden.
5. Interior: Mickey's office camera (P15); its definition was not found in production/specs under a camera name, check first.
6. Day walk (`-PerfHook=walk`, 1.4 m/s from the hook camera, CrimeProbe.cpp lines 5298-5306), for streaming and hitches.

**Measures per capture**, all columns already in the game's CSV (header of F:/LedgerTools/tmp/perf-csv/20261116-0148-9ffd652.csv, read 16 Nov):
- FrameTime, GPUTime, GameThreadTime, RenderThreadTime, RHIThreadTime (the CPU/GPU split);
- GPU/* per pass, grouped by tools/perf-hook.py lines 25-35;
- RHI/DrawCalls, RHI/PrimitivesDrawn;
- GPUMem/LocalUsedMB and GPUMem/LocalBudgetMB (Windows' budget, per frame);
- TextureStreaming/NonStreamingMips, StreamingPool, WantedMips, ResidentMeshMem; Streaming/NumLevelsLoading;
- shadowing lights within 40 m, from the game's LedgerPerfHookLight line (CrimeProbe.cpp line 5430).

**Memory by owner** (Lumen, distance fields, run-time pictures, cooked textures, render targets, hair, Nanite, virtual shadow maps): `memreport -full` and `rhi.DumpResourceMemory all` fired at chosen frames with `-csvExecCmds="<frame>:<command>"` (MEMORY-WHERE-2026-11-08.md lines 116-127); those runs' frame times are void. Today Nanite holds 0.3 MB and virtual shadow maps are off (MEMORY-WHERE line 160), so Mafia's 300 MB Nanite pool does not fit as a target yet.

**Unattended, existing tools first.** tools/p1-packaged.ps1 runs 1800-frame captures on the packaged copy at 3440x1440, High, the game's 55%, voice beside it, reads Windows' counters, writes runs.jsonl; `-Only`, `-Tag`, `-GameArgs` carry the new switches; it refuses while the build machine, an editor or a game runs (lines 11-33). Additions: perf-hook.py gains the thread, budget and streaming columns (it lacks them, lines 100-120); PerfHook gains `-PerfHookCam=<id>` (it reads only cam_hook, line 5338). The build machine's perf step stands still at 50% with no picture level (workflow lines 2132-2134; nightly_walk.py line 198), so it is not used for these budgets.

## 3. Budgets per view (the same at every view unless shown)

| Measure | Target | Source | Fits? |
|---|---|---|---|
| Median frame | ≤ 16.7 ms | RULINGS line 63; PLAN.md line 46 | ours |
| Slowest 1% | ≤ 25 ms | PLAN.md line 46 | ours |
| Every frame | ≤ 33.3 ms | RULINGS line 63; slice-perf.py lines 15-19 | ours |
| GPU median | ≤ 14.0 ms (1.7 ms spare accepted, re-set in phase 2) | perf-hook.py line 24; RULINGS line 63; measured spare 0.19 to 0.27 ms, EXIT-D-REVIEW line 25 | ours |
| Game and render thread medians | ≤ 14.0 ms each | this note's choice; none found in the studies | unverified |
| People's update and animation | ≤ 3 ms | Mafia 3 ms; Kingdom Come II 3.5 ms, 2.5 at 60 fps on PS5 (studies/12 lines 49, 54) | the lower, for 60 fps |
| Shadowing local lights | ≤ 8 a frame within 40 m | Kingdom Come II, 6 in its performance mode (studies/12 lines 25-26, 81) | first cap |
| Strand-haired people at once | 8 | MEMORY-PLAN §3, first guess; Kingdom Come II's 70 within 150 m is far above a street's needs | first guess |
| Card memory, peak | ≤ 5,650 MB | MEMORY-PLAN §4; slice-perf.py line 37 | ours |
| Card memory, steady | ≤ LocalBudgetMB (about 4,870 MB, 12 Nov) | n09-3 notes, orders/2026-11-09.md line 49 | the real target |
| Streamed texture pool | 1,000 MB | MEMORY-PLAN §1; Mafia's 1,500 MB at 6 GB (studies/12 line 82) would pass the budget | Mafia's too big |
| Never-streamed textures | 1,000 MB | MEMORY-PLAN §1 | first guess |
| Render targets / heap / distance fields | 1,300 / 900 / 350 MB | MEMORY-PLAN §1 (two measured, one guessed) | ours |
| Draw calls | reported, no target | none found | - |
| Draw distance | buildings 192 m, props 64 m | MEMORY-PLAN §2; Mafia's metres encrypted (studies/12 line 40) | first guess |

Night and walk share the frame targets; PLAN.md line 46 already counts night 1.1 ms tighter.

## 4. Steps, in order

No card step between 01:15 and 04:30 or beside another Unreal job. Before each: the space check, Runner.Worker absent twice a minute apart, close_games.py naming nothing, Marvelous and Blender named if they hold the card (packaged-walk skill §2).

| # | Step | Acceptance check | Est. h | Card |
|---|---|---|---|---|
| 0 | DECISIONS.md entry for the switch | present before any code | 0.25 | no |
| 1 | `-PerfHookCam`, cam_hill, perf-hook.py's columns | build-local.ps1 "both targets built"; perf-hook.py --selftest; unknown camera ends the game (line 5353) | 3 | compile |
| 2 | `-ScaleTest=N`, `-ScalePeople=M`, test-only | a log line names copies, instances, meshes, people; an editor screen at N=10 shows copies on the road lines, none through the street (screen only) | 8 | one editor run |
| 3 | Packaged build (nightly_package.py) | the played copy's stamp names the commit (packaged-walk §5) | 0.5 + wait | build machine |
| 4 | Ladder: six views × N 1, 2, 4, 10, 15, no people; then 0 to 40 people at N=10 on hook and walk (about 40 captures, about 3 min each) | each line 1800 frames, High, a launch verdict, nothing else on the card | 3 (about 2 h card) | yes |
| 5 | Owner dumps: hook and walk, N=1 and N=10, peak and settled | reports copied to F: scratch; holders sum to within 10% of LocalUsedMB | 2 | yes |
| 6 | Arithmetic and budget note: MB and ms per copy and per person, unique-front add-on, the Hook at 10 and 15; one fresh reviewer | every number traced to its capture | 5 | no |
| 7 | The done line: the N=10 day walk is the packaged walk measuring budgets; the real street (switch off) walked that night | no new fault from the test code | 0.5 | night job |

About 22 h est., leaving about 18 h of n16-3's 40 for the rough street. Records run 2 to 4 times plan figures (PIECES-DRAFT line 26).

**Pass or fail.** Pass: at N=10 with 20 people, every view meets every section 3 target, peak and steady memory included. Fail: the measured gap, the holder growing per copy, and its next step (likely World Partition's trial, unsized, MEMORY-PLAN §2, and distant versions), never written up as another plan. The rough street is then built inside the 1-copy budget less the measured growth.

## 5. n09-3's last measure, folded in

- n09-3's last reading: build d4a070b, steady 4,965 MB, peak 5,323, about 95 MB over Windows' budget of about 4,870; frame 17.05 ms, GPU 14.99 (orders/2026-11-09.md line 49).
- Newest perf line: peak 5,395, settled 5,023, median 17.29 ms, GPU 15.18 (production/d1-probe/ue-perf-verdict.txt; its build not named in the file).
- Both are the build machine's standing step (50%, no picture level), not the played High at 55%. Step 4's N=1 hook capture re-takes the measure at played settings with the voice; the N=10 capture is "the last measure at that scale".
- n09-3 closes in n16-3 on: peak and steady under LocalBudgetMB at N=10, or the gap per holder from step 5.

## 6. Risks, and what was not reached

**Risks**
- Instanced copies sharing textures may read low on memory and draw calls against a street built front by front; the add-on is inferred.
- Fixed cameras hide most copies, so GPU time may stay flat while memory and CPU grow; the hill and walk views catch that.
- Without World Partition everything stays loaded (MEMORY-PLAN §2): a worst case, not the shipped district.
- The voice runs on the processor (Pocket, default since 3 Nov, p1-packaged.ps1 lines 44-49).
- The double week keeps the card busy; Kiln or Marvelous may hold it. F: stood at 19.7 GB against its 20 GB floor on 15 Nov (commit d3ce57a).
- Mafia's numbers are Unreal 5.4; ours 5.8.2.

**Not reached or not read**
- Mafia's cell sizes and loading distances (encrypted); measured street frame times for either game; Mafia's animation budget file; Kingdom Come II's props and cell sizes (studies/12 and 04, blind spots).
- Epic's Nanite Technical Details, memreport and Texture Streaming Metrics pages, TechSpot (403) (MEMORY-PLAN §6); Epic's HLOD and Data Layers pages unread.
- No web page or game file was opened for this note; the office camera's definition is unverified.

## 7. Changes from the fresh review (16 Nov; these bind over the text above)

The review (METHOD-NOTE-REVIEW-2026-11-16.md, pass with fixes) found the method would read low; all fourteen of its fixes are taken. The ones that change the method:

1. The walk runs along the copies: a walk-length switch and a route laid on the Hook's road lines, so the day walk leaves the 48 m street.
2. Each copied piece brings its own lights (lamps, lit windows); the light count is logged at the walk's start and end.
3. Copies do not share every picture: each copy decodes its own shop pictures and takes another built unit's textures, so the largest holder (run-time pictures, 1,952 MB) grows as a district's would. One-off fronts are counted from the piece list, not from the 88% figure.
4. People are measured on the CSV's animation and movement columns; Kingdom Come II's figure at 60 fps is 2.5 ms, not 3.
5. The deliverable is cost per copy and per person on every view, with the lever named for each gap; the baseline already misses by a little (GPU 13.79 of 14.0 ms, frame over 16.7 ms, steady memory about 95 MB over), so pass or fail alone would not steer.
6. Three launches each at N=1 and N=10 (launch peaks already spread about 140 MB), the slope fitted over the whole ladder.
7. Steady memory judged against a fixed 4,870 MB with no other program on the card (Marvelous and Kiln closed for steps 4 and 5); the 25 ms target on the true 99th percentile; the reverse, hill and office views run as single stands with a camera switch; a fixed office camera added to the scene's camera list; the owner dump's acceptance names which totals must agree.
8. Authority: the scale switch rests on n16-3's adopted text (his tap of 15 Nov 21:08) as well as MEMORY-PLAN section 5, against PLAN's stop on whole-street sweeps (DECISIONS 16 Nov).
9. Hours: about 26 h estimated with these fixes and about 4 h of card time. At the records' 2 to 4 times this is more than the item's 40 h with the rough street, a risk named in the week's rows; the test is cut to the views that decide first (hook, walk, night) if it runs long.
