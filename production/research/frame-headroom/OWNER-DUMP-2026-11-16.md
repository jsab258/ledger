Method researched: MEMORY-WHERE-2026-11-08.md section 5

# Owner dump of today's packaged walk, 16 November 2026 (extraction only)

Read 16 Nov 2026. Numbers only; no judgement of what to do.

## 0. Sources and how read

- A = F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Profiling/MemReports/Entry-Windows-11.16-16.34.29/Pid29212_Entry-Windows-16-16.34.29.memreport (frame 560, the peak; 7,204 lines).
- B = the same folder, Pid29212_Entry-Windows-16-16.34.38.memreport (frame 1100, the settled walk; 7,204 lines).
- LOG = F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Logs/LedgerProbe-backup-2026.11.16-15.34.48.log. The file named LedgerProbe.log was overwritten at 16:46 by a later run (1,289 lines, no dump); the backup holds this walk. It carries the full `rhi.DumpResourceMemory all` of frame 561 (l.1396-6825: 5,425 named resources). The reports hold only the top 50 per dump plus summaries. Frame 1100's log lines hold command events only (l.6835-6843), no resource list, so frame 1100 has no full list.
- Command line of the run (LOG l.27): packaged, `scalability 2`, 3440x1440 at r.ScreenPercentage=55, -PerfHook=walk, csvExecCmds 560 memreport -full, 561 rhi.DumpResourceMemory all, 1100 memreport -full.
- Counts and sums were made by a small Python parse of those files (read only). The 1,226 listtextures rows parsed with none left over, in both dumps.
- A's Process Physical Memory: 3,217.25 MB used, 3,946.20 peak (A l.11). B: 3,195.43 used, 3,946.20 peak (B l.11).

## 1. listtextures nonvt (A l.1700-2949, B l.1700-2949; 1,226 rows each; totals A l.2929-2948, B same)

Total in memory: A 1,703.81 MB, B 1,802.80 MB (on disk 3,892.26 both). Texture2D objects (obj list, A/B l.742): A 1,612,504 KB = 1,574.7 MB, B 1,718,020 KB = 1,677.8 MB.

By format (rows, MB in memory; A l.2930-2937, B same lines):

| Format | A rows | A MB | B rows | B MB |
|---|---|---|---|---|
| PF_B8G8R8A8 | 350 | 1,328.39 | 350 | 1,328.39 |
| PF_DXT1 | 513 | 136.80 | 513 | 177.58 |
| PF_BC6H | 49 | 111.88 | 49 | 111.88 |
| PF_BC5 | 211 | 65.71 | 211 | 104.09 |
| PF_DXT5 | 88 | 57.76 | 88 | 76.59 |
| PF_G8 | 8 | 1.66 | 8 | 1.66 |
| PF_FloatRGBA | 5 | 1.23 | 5 | 1.23 |
| PF_BC7 | 1 | 0.38 | 1 | 1.38 |

By texture group (A l.2938-2948; B same lines): World 1,585.95 / 1,617.18; WorldNormalMap 55.47 / 75.39; Character 38.67 / 57.82; CharacterNormalMap 10.96 / 29.06; WorldSpecular 10.25 / 20.85; Skybox 2.25 / 2.25; UI 0.14; CharacterSpecular 0.09; Bokeh 0.02 (A / B).

Streamed against not, transient against cooked (by parse of the rows; the flag is the row's "Streaming" column):

| Part | Rows | A MB | B MB |
|---|---|---|---|
| /Engine/Transient, not streamed | 340 | 1,350.61 | 1,350.61 |
| Cooked or engine, not streamed | 82 | 134.91 | 134.91 |
| Cooked or engine, streamed | 804 | 218.29 | 317.28 |

All 340 transient rows are group TEXTUREGROUP_World, 1 mip, none streamed. 333 are PF_B8G8R8A8 and 7 are PF_DXT1.

### Largest 20 (in memory; A l.1703-1722, B l.1703-1722)

A: l.1703 /Game/Levels/LevelPrototyping/Textures/T_GameAnimationSample_Logo, 6000x6000, PF_DXT1, 1 mip, 18.00 MB. Then 19 rows, each /Engine/Transient.Texture2D_n, 2048x2048, PF_B8G8R8A8, 1 mip, 16.00 MB (l.1704-1722, ids 2147479474 to 2147480757). The dump has 60 such rows at 16.00 MB (l.1704-1763), so ranks 2 to 61 tie; the first 19 in file order are shown.

B: l.1703 MH_RoccoP2/Body/Baked/T_Body_N, in memory 4096x4096, PF_BC5, 14 mips, streamed, 21.38 MB (A holds it at 2048x2048, 5.375 MB, l.1809). l.1704 T_Body_SRMF, 4096x4096, PF_DXT5, 14 mips, streamed, 21.38 MB (A 5.375 MB, l.1810). l.1705 the logo, 18.00 MB. Then 17 of the 60 transient 2048x2048 PF_B8G8R8A8 rows at 16.00 MB (l.1706-1722). Next largest cooked: T_Body_BC 4096x4096 PF_DXT1 13 mips 10.69 MB at B (A 2048x2048, 2.69 MB, l.1843).

### PF_B8G8R8A8

350 textures, 1,328.39 MB in memory (1,333.75 MB on disk), in both dumps (A l.2930, B l.2930). Of them 333 are /Engine/Transient, 1,322.61 MB; 17 are cooked or engine, 5.78 MB (FastBlueNoise_vec2 4.00 MB, hair and mustache maps, placeholders, 1x1 defaults, micro_knit_front_H 1024x1024 11 mips).

### Shop fronts

- Textures under /Game/Ledger/ShopFronts/ (111 rows): PF_DXT1 77, PF_DXT5 27, PF_BC5 7. None is PF_B8G8R8A8. Every row has more than one mip (4 to 13). In memory 38.87 MB at A, 55.44 MB at B (A l.1767-2872, B l.1770-2872).
- The largest: ritas-front-worn_oxblood_basecolor and _white_joinery_basecolor, 4096x4096 in memory, PF_DXT1, 13 mips, 10.69 MB each (A l.1767-1768; B l.1770-1771).
- Other rows whose names hold front, shop or sign, outside that folder: 355 rows (PF_DXT1 256, PF_BC5 98, PF_B8G8R8A8 1); all with more than one mip. The one B8 row is the engine's clothing micro_knit_front_H. In memory 12.59 MB (A), 38.47 MB (B).
- The seven transient PF_DXT1 4096x1856 rows (4.00 MB each, 28.00 MB, 1 mip; ids 2147480329-2147480375; A l.1814-1820, B l.1816-1822) are block-compressed with one mip. Their names do not say what they are.

### The 340 run-time rows (the plan's 353)

The dump names every one only as /Engine/Transient.Texture2D_<number>; the prefix "Texture2D" holds all 340, 1,350.61 MB (the same in A and B). Owners are not named. By size (A l.1704-2611; ids 2147479313-2147481509; 1 mip each):

| Format and size | Rows | Each MB | MB |
|---|---|---|---|
| B8G8R8A8 2048x2048 | 60 | 16.00 | 960.00 |
| B8G8R8A8 1536x1536 | 9 | 9.00 | 81.00 |
| B8G8R8A8 2048x1024 | 10 | 8.00 | 80.00 |
| B8G8R8A8 1024x1024 | 12 | 4.00 | 48.00 |
| B8G8R8A8 2048x927 | 5 | 8.00 | 40.00 |
| DXT1 4096x1856 | 7 | 4.00 | 28.00 |
| B8G8R8A8 5650x460 | 2 | 11.25 | 22.50 |
| B8G8R8A8 512x512 | 20 | 1.00 | 20.00 |
| B8G8R8A8 1024x512 | 6 | 2.00 | 12.00 |
| B8G8R8A8 878x878 | 3 | 3.06 | 9.19 |
| B8G8R8A8 682x1024 | 3 | 3.00 | 9.00 |
| B8G8R8A8 1152x512 | 4 | 2.25 | 9.00 |
| B8G8R8A8 1024x2048 | 1 | 8.00 | 8.00 |
| B8G8R8A8 508x762 | 4 | 1.50 | 6.00 |
| B8G8R8A8 400x220 | 7 | 0.50 | 3.50 |
| B8G8R8A8 1024x256 | 3 | 1.00 | 3.00 |
| B8G8R8A8 416x416 | 3 | 0.69 | 2.06 |
| B8G8R8A8 900x450 | 1 | 2.00 | 2.00 |
| B8G8R8A8 268x1024, 900x260 | 1 each | 1.50 | 3.00 |
| B8G8R8A8 1024x204, 1024x170 | 1 each | 1.00 | 2.00 |
| B8G8R8A8 280x564 | 1 | 0.94 | 0.94 |
| B8G8R8A8 2x2 | 173 | 0.004 | 0.68 |
| B8G8R8A8 1024x102, 256x256 | 1 each | 0.50, 0.25 | 0.75 |

In the full resource list (LOG, frame 561) the same 340 rows (1,350.61 MB) have flags: "None" 163 rows 1,316.69 MB; "Resident" 177 rows 33.93 MB. The 60 rows of 2048x2048 are mixed between both flags (A l.1252-1302 shows "Resident" and "None" at 16.00 MB).

### listtextures uncompressed (A l.2951-2982)

20 rows, 6.94 MB; PF_B8G8R8A8 4.04 MB (A l.2974-2979); same in B.

## 2. RHI, render targets, buffers (A and B, same line numbers)

rhi.DumpMemory (l.1224-1248): Texture 2D 1,586.441 (A) / 1,699.484 (B); UAV texture 957.582 both; render target 2D 393.562; texture cube 110.273; vertex buffer 242.149 / 242.506; index buffer 41.743; structured buffer 128.341 / 127.913; byte-address buffer 91.053 / 91.056; reserved buffer uncommitted 12,270.500; reserved buffer committed 16.500; bindless heap 31.830; uniform buffer 0.640; RT acceleration structure 0.000; "total" 15,874.775 (A) / 15,987.751 (B) (l.1247).

Direct 3D 12 block (A l.219-240, B same): transient heaps 896.000 (A) / 640.000 (B); buffers 201.049 / 201.503; UAV buffers 12,589.244 / 12,588.716 (UAVBuffer stand-alone 12,399.000 both); textures 1,697.777 / 1,810.820; UAV textures 957.582; render targets 396.062; TOTAL 16,738.277 / 16,595.246. RHI transient: texture memory requested 1,165.406 / 540.941; buffer memory requested 255.188 / 63.875; memory requested 1,420.594 / 604.816; aliased 511.500 / 101.750; used 896.000 / 640.000 (A l.111-115 of the stat block, lines 237-241 in the file).

Render target pool (A and B l.4317-4405): 1,275.711 MB total, 1,165.336 used, 87 targets, in both. Largest: distance field brick texture 256.000; TSR history colour 102.000; Lumen radiance cache final atlas 72.250; Lumen radiosity indirect lighting, direct lighting, final lighting 64.312 each; global distance field page atlas 64.000; radiance probe source 64.000; radiosity trace atlas 64.000; whole-scene shadow map 33.062; Lumen scene depth 32.188; depth probe atlas 32.000; TSR history guide 26.250.

Tracked RHI resources (A l.1251-1306, B l.1251-1306): A 7,057 with info, 26,299 tracked; non-transient 3,607.522 MB; "transient" 6,174.542 MB (total 9,782.064). B 6,009 with info, 23,655 tracked; non-transient 3,683.926; "transient" 2,193.175 (total 5,877.101). LOG (frame 561): 5,425 named, non-transient 3,660.964; transient 6,174.542 (total 9,835.505) (LOG l.6822-6825). The "transient" here is the transient-heap bookkeeping, not the /Engine/Transient pictures.

Summaries (A l.1309-1387; B same lines), MB and entries:

| Holder | A | B |
|---|---|---|
| Lumen (all names starting Lumen) | 678.00 (105) | 678.13 (93) |
| Distance fields (name DistanceFields) | 273.47 (15) | 273.47 (15) |
| Global distance field (LOG, by name; not in a summary line) | 189.50 (22) | not in dump |
| TSR (LOG by name) | 155.81 (4) | not in dump |
| Shadow | 41.06 (4) | 41.06 (4) |
| GPUScene | 16.38 (5) | 16.38 (5) |
| Nanite | 0.31 (6) | 0.31 (6) |
| Skin cache | 20.72 (222) | 20.75 (225) |
| Hair (name holds Hair; groom, voxel not named) | 177.76 (1,048) | 177.83 (1,049) |
| Virtual texture | 0.06 (1) | 0.06 (1) |
| Virtual physical texture, volumetric fog, subsurface, texture cube, morph deltas | 0 | 0 |
| Tangents buffer | 5.42 (110) | 5.42 (110) |
| Index buffer (name) | 14.75 (262) | 14.81 (263) |
| Vertex buffer (name) | 21.83 (390) | 21.83 (390) |
| Tex-coord buffer | 4.13 (110) | 4.13 (110) |

Lumen split by name in the full list (LOG): radiance cache 201.12 (22 rows); Lumen.Scene* 208.88 (9; direct lighting 64.31, final lighting 64.31, depth 32.19, albedo, normal, emissive 16.00 each); radiosity 152.62 (6); screen probe gather 62.00 (16); reflections 42.56 (6); tile shadow downsample atlas 8.00; translucency volume 1.50; rest under 1.

Meshes: static mesh total 141.852 MB (256 objects; A l.528, B same); skeletal mesh 31 objects, Res 40.731 M (41,708.84 KB), vertex memory 29.779 MB, index 6.906 MB (l.544-545); GPU skin cache total used 9.696 (A) / 9.722 (B) MB (l.450); body setups 265 objects, 172,404 KB; texture cube objects 34, 112,904 KB. The largest static meshes: grocer-display 18,907 KB, mickeys fittings 15,126 KB, street_foliage_dark 14,766 KB, street_foliage 9,683 KB (A l.1434-1440, ResExcKB). Streaming pool: 800.000 MB set, "used streaming pool wanted" 168.277 (A) / 67.621 (B) (stat block lines 426-428 of its section). Texture memory used (stat, l.550) 1,681.505 (A) / 1,794.548 (B).

Ray tracing acceleration structure memory: 0.000 MB in the RHI line (l.1236) and in the D3D12 and Vulkan lines.

Hair voxel texture: no row by that name in either dump (Hair rows total 177.76, above). Ledger of unnamed memory: A's "texture memory requested" falls from 1,165.406 to 540.941 at B (arithmetic: 624.465).

## 3. Lines that name a total GPU figure

| Line | A | B |
|---|---|---|
| Used Video Memory (D3D, l.262) | 5,072.066 | 4,952.066 |
| Total Video Memory (Budget) (l.264) | 4,710.605 | 4,710.605 |
| Demoted Video Memory (l.258) | 361.461 | 241.461 |
| Total System Memory (Budget) (l.263) | 15,579.023 | 15,579.023 |
| D3D12 TOTAL (l.226) | 16,738.277 | 16,595.246 |
| rhi.DumpMemory total (l.1247) | 15,874.775 | 15,987.751 |
| Render-target pool total (l.4405) | 1,275.711 | 1,275.711 |

Arithmetic from those lines: A used video memory less the budget = 361.461 (equals A's demoted figure); B 241.461 (equals B's). Used video memory less tracked non-transient less transient heaps: A 5,072.066 - 3,607.522 - 896.000 = 568.544; B 4,952.066 - 3,683.926 - 640.000 = 628.140. This is a subtraction, not an owner list.

## 4. Plan section 1 against the dump

Plan = PACKING-PLAN-2026-11-16.md section 1 (8 Nov measured MB, today's MB). Dump numbers are A (frame 560) unless marked; the full-list rows are frame 561 (LOG). Disjoint split of the 5,425 full-list rows (priority in the order listed; sum 3,660.96): /Engine/Transient textures 1,350.61 (340); Lumen 678.00 (105); DistanceFields 273.47 (15); GlobalDistanceField 189.50 (22); TSR 155.81 (4); Shadow-named 33.06 (3); Hair-named 177.76 (1,048); skin cache 20.72 (222); Nanite 0.31 (6); logo 18.00 (1); GlassBake owners 108.00 (32); /MetaHumanCharacter owners 68.06 (92; 72.19 before hair rows are taken out); other owner-bearing textures 166.80 (745); other owner-bearing buffers 159.31 (2,413); owner None, rest 261.54 (377; includes T_Body_N 21.38, T_Body_SRMF 21.38, T_Body_BC 10.69, slate window texture 20.38, particle textures 32.25 + 16.12 + 8.12, front-layer translucency 29.81, stochastic lighting 26.25, GPUScene 16.38, scene colour 13.25).

| Plan holder | Plan MB (today) | Dump MB | Difference (dump - plan) |
|---|---|---|---|
| Run-time pictures: maps, scans, decals, sky, scalp | ~1,320 | 1,322.61 (333 transient PF_B8G8R8A8 rows; all 340 are 1,350.61) | +2.61 |
| Run-time pictures: shop cards | ~55 | 28.00 (7 transient DXT1 4096x1856 rows; names not given) | -27.00 |
| Cooked textures and meshes | ~560 | 502.17 (GlassBake 108.00 + MetaHumanCharacter 68.06 + other textures 166.80 + other buffers 159.31); 555.62 with the three T_Body textures | -57.83; -4.38 |
| Lumen (surface cache 273, radiance 195) | 678 | 678.00 (radiance cache 201.12; Scene*, radiosity, others as in section 2; no "surface cache" name) | 0.00 |
| Distance fields | 461 | 462.97 (273.47 + 189.50) | +1.97 |
| TSR | 156 | 155.81 | -0.19 |
| Shadows | 41 | 41.06 (summary) | +0.06 |
| Transient heaps, walking | 896 | 896.000 (A l.219) | 0 |
| Transient heaps, steady | 640 | 640.000 (B l.219) | 0 |
| Hair voxel texture | 343-392 of the peak | not in dump (no row by that name) | - |
| People: hair | 89 | 89.44 (owner None, name begins Hair, 550 rows); 177.76 for all rows with Hair in the name | +0.44 |
| People: MetaHuman shared | 66 | 68.06 (72.19 before hair rows are removed) | +2.06 |
| Logo | 18 | 18.00 | 0 |
| Outside the dump at peak | ~670 | 568.54 (A arithmetic, section 3); B 628.14 | -101.46 |
| Windows' budget for the game | ~4,870 | 4,710.605 (D3D total video memory budget, A and B) | -159.40 |
| Count of run-time rows | 353 | 340 (A l.1704-2611) | -13 |
| Run-time pictures total (8 Nov) | 1,952 | 1,350.61 | -601.39 |
| Of them 16 MB each (2048x2048) | 60 | 60 | 0 |
| Of them 30 MB each (4096x1855 BGRA8) | 21 | 0 (7 DXT1 4096x1856 at 4.00 MB each) | - |
| Plan check: "no PF_B8G8R8A8, mips above 1" for fronts | - | fronts in /ShopFronts/: no B8, all more than one mip (section 1) | - |

Not read or not in the dump: owners of the 340 /Engine/Transient rows; the hair voxel size; the heap contents; frame 1100's full resource list (only its top 50 and summaries); any ray-tracing geometry (shown as 0.000); Windows' own counter beside the dump (the plan's 4,870).
