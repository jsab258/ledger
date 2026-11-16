# Fresh review: card-memory packing plan (n16-3), 16 November 2026

Reviewed: PACKING-PLAN-2026-11-16.md (921 words), against the sources its first line names, git history (read-only, 16 Nov) and the installed engine, C:/Program Files/Epic Games/UE_5.8 (Build.version 5.8.4, changelist 58902052). The 5.8.4 install now holds the Renderer and Engine .cpp files that COOKING-PLAN s0 said were missing, so the engine questions below were checked in source. Nothing was run; no game, editor or build.

**Verdict: pass with fixes** (list at the end). The numbers mostly trace to their sources and the arithmetic holds; one commit hash is wrong, two "unverified" points are settled by the engine source, one source is misquoted, and the per-person section disagrees with the project's existing budget home.

## 1. Numbers checked

Correct against source:
- Section 1, 8 Nov column: 1,322 (1,952 less 630), 630, 866, Lumen 678, distance fields 461, TSR 156, shadows 41, hair 89, MetaHuman shared 66, logo 18 (MEMORY-WHERE s6 l.144-155); heaps 640/896 and voxel texture 343-392 (s1 l.28-29, s2 l.57). Lumen split 273/195 is COOKING-PLAN s1 rows C1-C2 (l.34-35).
- Shop cards ~55: 630 less 369 (5,541 to 5,172) less 207 (5,172 to 4,965), orders 2026-11-09 l.49. Cooked ~560: 866 less 296 + 62 plus kept 48-65 (COOKING-PLAN l.58-59) gives about 555-570.
- Today: 5,016 steady, 5,298 peak (ue-perf-verdict.txt); 5,149 and 5,706 (SCREEN-N10 l.39); Windows' budget 4,861-4,879 (orders l.49); 165 MB a copy is (6,151 - 5,161)/6 (SCREEN-N10 l.40-41).
- Step 1 sums: 280 is A3+A4+A5+A6 (128+81+48+22.5) and 82.5 is A7 (COOKING-PLAN l.27-31); 960 to ~160 is 60 x 2.67 MB (BC1 colour, BC5 normal, BC1 roughness, one mip).
- Step 2: ~190 = C2 about 124 + C1 64-79 (COOKING-PLAN l.61-62). Engine confirms the check: final probe resolution = probe + 2 x (1 << (mips-1)) (Renderer/Private/Lumen/LumenScreenProbeGather.cpp:719-722), atlas = probes x final resolution (LumenRadianceCache.cpp:1530), so 128 x 34 = 4352 at 32 and 128 x 18 = 2304 at 16; probe atlas 128 x 32 to 128 x 16 (LumenRadianceCache.cpp:1452). Epic's High is atlas 3584 and probe resolution 16 (Engine/Config/BaseScalability.ini:377, 387); the project sets 4096 and 32 (ue-probe/Config/DefaultScalability.ini:27, 37).
- Step 3: 8 pages a side = 256 cubed x 4 bytes = 64 MiB (73 with mips) against 343-392; ~256 off the peak is the heap's two 128 MB steps (MEMORY-WHERE s4.2).
- Expected totals: 5,016 less 1,108-1,288 gives 3.73-3.91 GB steady; 5,706 less 1,108 less 256 gives 4.34 at the top of the walking range. Consistent.
- Study 12 l.41, 82 (pools), l.48-53 (people rules): quoted correctly.

Wrong or unsourced:
- **Commit c621d85 is not step 3.** c621d85 is "n09-11: the gate starts the next session ... GarmentCode lab test". Step 3's code is **34b1a2000** (9 Nov). Fix the hash.
- **ue-material.txt l.35-46** should be **l.35-49** (Rita's worn and the tea rooms are on 47-49), and the file is ue-probe/ue-material.txt (gitignored, last written 12 Nov 06:31). Five of those lines read PARTIAL with 1-3 textures left unset (chandler-front-joinery, chandler-front-worn, grocer-front, launderette-front-worn, newsagent-front-worn): the ~560 should say some front textures were left untouched.
- **BC5 "formats CreateTransient accepts, STEP4-NEXT-PLAN"** misquotes the source: STEP4-NEXT-PLAN names PF_DXT1, PF_DXT5 and PF_BC7 only. The engine settles it the other way round: UTexture2D::CreateTransient takes any EPixelFormat and only checks block alignment and data size (Engine/Private/Texture2D.cpp:1291-1323), so BC5 is accepted. What stays unverified is the material side (a normal sampler reading a transient BC5), not the format. Cite Texture2D.cpp, drop "(unverified)" on the format.
- **"Hair voxel ... name unverified in 5.8.4"** is now verified: `r.HairStrands.Voxelization.Virtual.VoxelPageCountPerDim`, default 14, a plain runtime console variable (Renderer/Private/HairStrands/HairStrandsVoxelization.cpp:96, 100), used per frame for the 3D texture's size (l.841, 922-924). Remove it from step 3's check wording and from section 6.
- Step 1's ~900-1,080 MB: the stated sums give about 1,060-1,080; the 900 floor has no stated basis (presumably the PNG exceptions). State it or drop it.
- Section 1 leaves about 256 MB of the dump's named, non-transient resources (4,583 less the rows listed, 4,327) in no row. One line, or a footnote.
- Section 2 omits step 4a's peak (5,873 to 5,538) and its commit 4e3e4b8; small, but the plan quotes the steady pair only.
- Section 5: baked outfit "4.9-5.3 MB" leaves out MH_Test_Outfits at 10.14 MB (RESIZING-VERDICT l.15). "8 near (Epic's suggested ring)" stretches CROWD-DISTANCE l.10, which is about eight simplified full-actor MetaHumans in total on screen, not eight near people with strands. 8 x 50 + 25 x 20 = 900, above the 800 the line divides.

## 2. Built against unbuilt

Checked with `git log --grep n09-3` and `git log -- production/research/frame-headroom`:
- Step 3 built (34b1a2000, code; the re-import's lines exist in ue-probe/ue-material.txt) and measured only as the build machine's peak fall 6,332 to 5,822 on e82fe35, which contains 34b1a2000 (checked with merge-base). That the re-imported assets were in e82fe35's cook is not shown by git (Content is untracked); the plan's "not seen in a dump" is right.
- Step 4 built and measured: 4e3e4b8 (one shop picture of three) and d4a070b (BC1). Correct.
- Not built, confirmed by an empty search of the history since 8 Nov: naming the 353 rows, the street/scan/decal/sky/scalp pictures, pool guard, Lumen and hair settings, heap settings, logo; no packaged dump since 8 Nov. The plan has none of these the wrong way round.

## 3. The order

The plan's own arithmetic is right: about 100, 95, 85, 36 MB an hour. But steps 1 and 2 are within 5% of each other, step 1's 10 hours is the least certain figure in the plan, and the measured steady gap over Windows' budget is about 150 MB (5,016 against about 4,870). Step 2 alone (about 190 MB steady, two ini lines, 2 h) closes that gap. Recommended: step 2 first, with the logo in the same packaged walk (one check for both), then step 1, then step 3 (his look, 2 Nov hair ruling). Step 0 stays first.

## 4. Missing against a professional memory budget

- **Category ceilings and a reserve.** The plan lists holders and savings but sets no ceiling per holder (pictures, Lumen, distance fields, people, district, reserve). Mafia keeps a 10% card spare in its base console profile (study 12 l.18); none is named here.
- **Distance fields, 461 MB, not addressed.** COOKING-PLAN s5 said no control was found; 5.8.4 source names it: `r.DistanceFields.BrickAtlasMaxSizeZ`, default 32 = 256 MB target, render-thread-safe (Renderer/Private/DistanceFieldStreaming.cpp:38-42; mips dropped past it, l.806-807). The street imports at distance-field scale 2 (ue-material.txt streetImport lines). This is also the likely part of the 165 MB per copy; the plan should list it as a candidate step and split the per-copy growth by holder in step 0's dump.
- **Streaming and mips.** Route A gives one mip and no streaming, so the far copies hold full size; the plan says cooked assets "belong with World Partition" but gives no step or date. A budget names when the run-time pictures move to cooked, streamed textures and what pool size they then need (187 of 800 today).
- **Per-person basis.** The project's home for this is pre-production/4-BUDGETS.md l.172-174: principal person at most 100 MB, at most 3 near; passer-by at most 15 MB unique, at most 12; strands only on two people within 5 m. Section 5's "8 near with strands at 40-50 MB" contradicts that home without saying so. Either derive from it or state the change and its reason; the RULINGS 30 Sep ladder (0, 5, 10, 20) is the right measure and should be the basis, not the 24 Sep figures.
- Hours: steps 0-4 at 15.5 h plus builds are about 40% of n16-3's 40 h, which also has to build the rough whole street. Worth a line.

## 5. Fixes (pass with these)

1. Step 3's commit c621d85 to 34b1a2000; ue-material lines 35-49; note the five PARTIAL fronts.
2. Hair voxel setting verified: cite HairStrandsVoxelization.cpp:96, 100 (5.8.4); remove "unverified" from step 3 and section 6.
3. BC5: cite Texture2D.cpp:1291-1323 (any format, alignment only); the open risk is the material's normal sampler, not CreateTransient.
4. State the basis of step 1's 900 floor or use 1,060-1,080.
5. Order: step 2 (with the logo in its walk) before step 1, since it closes the measured 150 MB gap over Windows' budget in 2 h.
6. Add distance fields (BrickAtlasMaxSizeZ, DistanceFieldStreaming.cpp:38-42) as a candidate, and split the per-copy growth by holder in step 0.
7. Section 5: start from 4-BUDGETS l.172-174 or say why it changes; fix "Epic's suggested ring" wording; keep the total inside 800.
8. One line of category ceilings with a reserve.

## 6. Words: 921 against 900

Cut about 120 to make room for the fixes:
- Section 3 (105 words) to two sentences: the method is COOKING-PLAN s3's; route A is the nearest equivalent, far copies keep full size. About 60 saved.
- Section 6's fourth bullet repeats section 4's risks (heaps, hair setting, BC5, growth per copy): drop it, about 20 saved (the hair setting is settled anyway).
- Line 5's commit-history caveat goes once the hash is fixed from git: about 15 saved.
- Section 1's Source column repeats the first line's list; keep only the section numbers: about 25 saved.
