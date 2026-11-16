Method researched: MEMORY-READING-2026-11-07, MEMORY-PLAN-2026-11-07, MEMORY-WHERE-2026-11-08, COOK-PICTURES-PLAN-2026-11-08, COOKING-PLAN-2026-11-09 and review, COOK-STEP3-CODE-2026-11-09, STEP4-NEXT-PLAN-2026-11-12, studies/12-tech-budgets.md, DECISIONS (n09-3), orders/2026-11-09.md l.49, SCREEN-N10-2026-11-16, d1-probe/ue-perf-verdict.txt, d1-probe/metahuman-cast/ue-mhcost.txt, CROWD-DISTANCE-2026-11-09, RESIZING-VERDICT-2026-11-11, pre-production/4-BUDGETS.md; engine 5.8 source as cited.

# Card-memory packing plan (n16-3), 16 November 2026

Read 16 Nov 2026; plan only. M = measured, I = inferred. Reviewed the same day (PACKING-PLAN-REVIEW-2026-11-16.md, pass with fixes, all taken).

## 1. Where the ~5.1 GB stands

No owner dump since 8 Nov (peak 6,152 MB, MEMORY-WHERE s6). Today = that dump less the falls measured since.

|Holder|8 Nov MB (M)|Today MB|
|---|---|---|
|Run-time pictures: street maps, scans, decals, sky, scalp|1,322|~1,320 (I; MEMORY-WHERE s6)|
|Run-time pictures: shop cards|630|~55 (I: less measured 369 + 207; orders l.49)|
|Cooked textures and meshes|866|~560 (I: fronts re-imported, ue-material.txt l.35-49; five front rows PARTIAL with some textures unset; not seen in a dump)|
|Lumen (surface cache 273, radiance 195)|678|same|
|Distance fields; TSR; shadows|461; 156; 41|same|
|Transient heaps|640 steady, 896 walking; hair voxel texture 343-392 of the peak (I, strong)|same|
|People: hair 89, MetaHuman shared 66|155|same|
|Logo 18; outside the dump ~670 at peak (I)|~690|same|

Now: build machine steady 5,016, peak 5,298 (ue-perf-verdict.txt); editor, two street-lengths, 5,149 steady, 5,706 walking (SCREEN-N10). Windows' budget for the game about 4,870 (orders l.49): about 150 MB over it.

## 2. Built and measured

- 9 Nov step 3, glb import pass (34b1a2000): build machine at Highest, peak 6,332 to 5,822 (orders l.49). Fronts at 4096x512 with mips: unconfirmed.
- 12 Nov step 4: one shop picture of three, steady 5,541 to 5,172; BC1 shop pictures by tools/bc1_pictures.py (d4a070b), to 4,965, peak 5,323. Build machine's step, not the played High.
- Not built: naming the 353 run-time rows; the street, scan, decal, sky and scalp pictures; pool guard; hair voxel and Lumen settings; distance fields; heaps; logo.

## 3. Reference method

Mafia and Kingdom Come II ship cooked, block-compressed, mipped textures streamed through one sized pool, keep about 10% of the card spare, and draw people in full only near (study 12 l.38-53). The method fits; their pool sizes do not. Compressing at staging (12 Nov) is the nearest step inside our run-time files, not the method: far copies keep full size until textures are cooked and streamed with mips, planned with World Partition (n16-3's rough street, a step and date set there).

## 4. Steps, in order

Ceilings (with 10% of the card, ~600 MB, kept spare): run-time pictures 450, cooked textures and meshes 600, Lumen 500, distance fields 300, heaps 640, people 800, street copies the rest.

Each check: one packaged walk at High by p1-packaged.ps1 (day walk, night stand), peak and settled GPUMem by slice-perf.py, memreport at frame 1100 (MEMORY-WHERE s5); three runs within 150 MB; hook and reverse at full size beside the last good picture.

0. **Owner dump on today's packaged copy** (1.5 h; no saving). Confirms section 1's inferred rows and the fronts (listtextures nonvt: no PF_B8G8R8A8, mips above 1); names the 353 rows; splits the ~165 MB per street copy by holder.
1. **Lumen at Epic's High, the logo in the same walk** (~210 MB, 2.5 h, ~85 MB/h; closes the ~150 MB over Windows' budget first). Radiance probe resolution 16, surface atlas 3584 (COOKING-PLAN C1-C2). Check: the 4352 atlas reads 2304 (LumenScreenProbeGather.cpp:719-722, LumenRadianceCache.cpp:1530). Risk: coarser indirect light, judged at the gate.
2. **Compress the remaining run-time pictures at staging** (~1,060-1,080 MB, ~10 h, ~105 MB/h). Extend bc1_pictures.py with BC5 normals and BC3 alpha decals, padded to fours (the engine takes any format, checking only block alignment and size: Texture2D.cpp:1291-1323); ID maps and cropped decals stay PNG. Sums: 960 to ~160; 280 to ~65; 82.5 to 14-28. Check: /Engine/Transient under ~350 MB; PNG decodes only on named exceptions. Risks: BC1 on lettering and dark gradients; the material's normal sampler reading BC5; silent fallback to PNG.
3. **Hair voxel pages 14 to 8** (r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim, default 14, HairStrandsVoxelization.cpp:96-100; ~256 MB, walking peak only, 1.5 h). Check: requested transient ~190. Risk: hair occlusion; his look (2 Nov hair ruling).
4. **Distance-field brick atlas** (r.DistanceFields.BrickAtlasMaxSizeZ, default 256, DistanceFieldStreaming.cpp:38-42; saving unmeasured, 1.5 h): only after step 0 shows the 461 MB's split. Risk: Lumen's far detail.
5. **Heap settings** (0-384 MB, unproven, 2 h): only if the walking peak stays above target.

Steps 0-3: about 15.5 h. Expected (I): steady 3.7-4.0 GB, walking peak 3.8-4.3 GB, against Windows' ~4,870. Room left: about 800 MB steady at worst.

## 5. Budget per person

The home is 4-BUDGETS l.172-174: at most 3 principal people near (27-43 MB of textures measured, up to 100 MB each), strands on two within 5 m, passers-by at most 15 MB unique each, card grooms up to 16 MB. This plan keeps it. Supporting figures: each further MetaHuman +5 to +8 MB of textures (ue-mhcost.txt, 24 Sep, older cast: unverified today); baked outfit 4.9-5.3 MB (RESIZING-VERDICT l.12-18); skin cache ~2.5 MB at LOD0 (forum figure, disputed: unverified).

In 800 MB: 3 near at about 100 MB (300) plus passers-by at about 20 MB with their card grooms (about 25, 500): about 28 people. Street copies share the room at ~165 MB each from four to ten street-lengths (I, SCREEN-N10).

## 6. Unknown, and what settles it

- Today's owners at the played High: step 0.
- MB per person packaged: the RULINGS 30 Sep ladder (0, 5, 10, 20), memreport and r.SkinCache.PrintMemorySummary at each.
- The ~670 MB outside the dump: rhi.DumpMemory beside Windows' counter.
