# Card memory for a whole district: proposal, 7 November 2026

Fixed 8 Nov after PROPOSALS-REVIEW-2026-11-08.md.

For Monday's order; nothing decided. Read 7 November unless dated. "5.4": Mafia's method, needing a check against 5.8.

- 5,810 to 6,089 MB are not peaks: each is a median after dropping 300 frames, at Highest [T, D].
- At High the first frames peak at 6,086 to 6,224 MB, eight launches, one build; settled about 5,500 [L].
- Once the game's voice started, Windows' budget for the game fell to 5,771 MB, one run [L]; 6,000 can exceed it.

## 1. Budget: High, peak frame, game alone

"Today": measured here, one boot run of 4 November, read by eye [C]; columns may overlap (unverified). Mark is the ceiling's.

|Category|Today MB|Ceiling MB|Mark|
|---|---|---|---|
|Never-streamed textures|2,365|1,000|first guess|
|Streamed textures|57 (pool 800)|1,000|a guess pending measurement: Mafia gives a 6 GB card a 1,500 MB pool [12], but 1,500 here would carry the total past 5,771; 1,000 is what the other ceilings leave|
|Render targets (includes shadow pages; their 256 MB unverified: the page format was not read [S])|1,276|1,300|measured here|
|Temporary heap|768 (896 most)|900|measured here [L]|
|Distance fields|264|350|first guess|
|Ray-tracing geometry, resident though tracing is off|221|100|first guess|
|All else: meshes, hair, buffers, Lumen's cache, Nanite|583 by subtraction|1,000|first guess|
|**Total**|**5,534**|**5,650**|under 5,771|

- Never-streamed textures read 1,738 on 23 October [P]: 627 of the settled figure's 646 MB rise (different captures). With card room left they escape the pool's cap [S].
- Kingdom Come II's 4,096 MB of textures (CryEngine) does not fit. Nanite: default 512 MB, root pages extra [R]; Mafia's 300 is 5.4. Virtual textures: our use unread.
- **It does not yet close.** The peak frame's 6,103 MB is 569 above settled, while textures, render targets and heap stayed put [C], against [L]'s two leading causes (one run).

## 2. Division and streaming

- Today: no World Partition in code or config; the street loads onto the Entry map [E, L]. Moving is the biggest job, unsized.
- The Hook: about 0.107 km² (computed from [A]). Epic's example, 256 m cells, 768 m radius [W], would hold the whole town: rejected.
- Mafia's grids: 128 m main, 32 m props [4]; street widths fit (14.7 against 10.25 m). 5.4; Epic warns more than one grid can hurt [W].
- Ranges, first guess: buildings 192 m, props 64 m; Mafia's encrypted, Kingdom Come II's unknown [12, 4]. 192 m covers about the Hook's area, so savings come from props, interiors, other districts.
- Merged distant versions per cell [W]; interiors and day, night, market states as data layers [4], 5.4. Kit reuse: Mafia's 78.5 uses per mesh [4].

## 3. Shed with distance

- **People under 10 m:** full, strand hair, never frozen (Mafia, setting names [12], 5.4).
- **10 to 30 m:** hair cards, lower detail; 30 m first guess. Cards and strands disagree in colour today [H]; an earlier seam needs his look.
- **30 to 70 m:** capped textures (`MaxLODSize` [R]), no hair shadows (Mafia: half distance).
- **Beyond 70 m:** frozen when unseen 3 s; set-piece crowds vertex-animated (Mafia, 5.4).
- **Strand-haired people at once:** 8, first guess; Kingdom Come II's 70 people in full detail within 150 m far exceeds a street's needs [12].
- Freezing saves time, not memory (inference). Memory falls through fewer distinct people, capped textures, stripped hair levels (`r.HairStrands.MinLOD=3` [R]).
- **World:** props unload at range, stop casting at a quarter distance (Mafia). Streamed textures lose top mips over budget [R]; never-streamed cannot.

## 4. Measuring a peak, per build

The highest `GPUMem/LocalUsedMB` in any frame after the load row, at High, against one line: the table's total ceiling, 5,650 MB. The QA proposal's night line takes the same measure and line. Not Windows' counter: [L] found its 8.1 GB never showed in the game's figure, but REHEARSAL-2026-11-07-D (line 15) records that this conflicts with [D] (the game's private memory moves too) and with the series; the conflict is open.

No new tool: the existing perf step asks `scalability 2` and captures from launch (`-csvCaptureFrames` [L]); `slice-perf.py` prints peak, budget and the table's columns beside its median. It reports, never fails. Three runs only when a reading crosses the line.

Faults caught: medians read as peaks; 627 MB of textures unseen for twelve days; Highest taken for the played level.

## 5. First three steps

1. **Mend the measure; run the diagnosis's confirm on 2c32629 [D].** About two hours plus a build's wait. Shows true peak, scatter, High against Highest.
2. **Name the owners** on the packaged copy: `rhi.DumpResourceMemory` [P], one memory trace from launch [V]. About half a day. Shows the 2,365 MB's contents, each person's and hair's share, the 569, any overlap.
3. **Scale test,** Kingdom Come II's idea [12]: a test-only switch adding street copies and people. Two to four days, may grow. Shows MB per street and person, so whether the district fits. "Nothing is multiplied" before his sample: the session must rule this allowed and record it in DECISIONS.md with its reason. World Partition's trial is sized after.

## 6. Still unknown

- Scatter; true peak; the moving budget (9,427, 7,128, 5,771 seen): step 1.
- Never-streamed contents; the 569; real MB for Lumen, Nanite, shadows (the 256 MB of shadow pages included): step 2.
- MB per person (a forum's 2.3 GB: unverified snippet [R]); per street: step 3.
- Grids, ranges, 300 MB Nanite on 5.8: World Partition's trial.
- Eviction, UE-305620 in 5.8 (forum, unverified [R]): a walk near a full card, reading Windows' paging events [V].
- Whether Windows' counter or the game's figure is the right peak: [L] against [D] and REHEARSAL-D, step 1.

Unreached [R]: Epic's Nanite Technical Details, MetaHuman LOD specifications, memreport, Texture Streaming Metrics; TechSpot (403). Unread: Epic's HLOD and Data Layers pages; Microsoft's CurrentUsage page [D]; the virtual shadow map page's texel format. No shipped per-category budget found. Lumen's ladder sections stay unverified.

Tags: R production/research/frame-headroom/MEMORY-READING-2026-11-07.md; D F:/LedgerTools/gate/new/card-memory-2026-11-07/diagnosis.md; T tools/slice-perf.py:26,76; C F:/LedgerTools/tmp/launch-peak-2026-11-04/perfhook/run2/Profile(20261104_161938).csv:20,600; production/research/frame-headroom/: L LAUNCH-PEAK-2026-11-04, P PSO-AND-VRAM-METHOD-2026-10-23, V VOICE-ON-CARD-TRACE-2026-10-25; 12, 4 production/research/aaa-reference/studies/ (25 October; 12 line 82 for the 1,500 MB pool, line 53 for the 70); A production/art/atlas-01/data/atlas.json; E ue-probe/Config/DefaultEngine.ini:18; H production/research/character-pipeline/HAIR-NEAR-DARK-2026-11-07.md; S UE 5.8 AsyncTextureStreaming.cpp:656-669, VirtualShadowMapCacheManager.cpp:1116-1125, VirtualShadowMapArray.cpp:2420; W https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine
