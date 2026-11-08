# Cooking the run-time pictures: costed plan (8 November 2026)

Order item n09-3. Plan only: nothing was run or edited. All sources were read 8 Nov 2026; code lines are VignetteShot.cpp unless named.
- "Today" is the 8 Nov 21:26 dump, in padded MB (MEMORY-WHERE-2026-11-08.md:136-163; RUNTIME-PICTURES-2026-11-08.md:30-60).
- "After" is inferred: block size times area, times 4/3 for mips, with every mip resident. That is an upper bound.
- Formats come from the engine's list (UE_5.8 TextureDefines.h:393-409). BC1 with mips at about 1 MiB per 1024² agrees with Epic's table (682 KB; https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-format-support-and-settings-in-unreal-engine).

## 1. Table

| Group (call site) | Today MB | Role: setting | After MB |
|---|---|---|---|
| Shop-room cards, 7 x 3 states (8446) | 630 | colour: TC_BC7, sRGB, stretched to 4096x2048 | shown only 210; cooked only 224; **both 75** |
| Mickey's room, 3 states (same loop) | 24 | same, 2048x1024 | 3 |
| Street drawn maps (7501) | 126 | colour TC_Default sRGB (BC1); _n TC_Normalmap (BC5); _r TC_Default, sRGB off (BC1) | 28 |
| Street photo maps, CityPack jpg (7524) | 264 | same as drawn maps | 59 |
| Scan maps (8798) | 317 | same; a file named twice becomes one asset | ~80 |
| Street decal cards (7472) | 105 | TC_BC7 sRGB (alpha), max 4096 | ~40 |
| Wear pictures (9069) | 29 | TC_BC7 sRGB | ~11 |
| Door card closed, decoded 7 times (8037) | 3.5 | TC_BC7, one asset | 0.2 |
| Tom's scalp (SliceCharacter.cpp:726) | 16 | TC_Default sRGB | 2.7 |
| Sky photograph (6406) | 8 | TC_BC7 sRGB | 2.7 |
| Not named by the dump | 423 | by role | 95-140 if staged pictures, else 423 |
| Stay decoded: 2x2 flats (6255, 9837); brick ID maps (8825) | ~0 plus the ID maps | ID maps: RGBA8, no mips, nearest | unchanged |
| **Run-time total** | **1,952** | | **~400-450** |
| Six worn fronts, cooked uncompressed (not run-time) | 268 | sides cut to a multiple of 4 | ~55-60 |

- **HDR:** no run-time picture is HDR. The sky is an 8-bit PNG (6406), and the glass cubes are already BC6H (import_glass_bake.py:142).
- **Expected peak (inferred): about 4,600-4,650 MB**, down from 6,152.
  - It is about 4,930 if the unnamed 423 MB is not reached.
  - It is about 4,400-4,450 with the worn fronts fixed too.

## 2. Answers

**Q1. Which groups to cook, and which stay decoded.**
- No picture's pixels are rewritten after load. The only pixel writes are the import copy (6196) and the 2x2 builders (6255-6261, 9837-9859).
- Tints and states go through material parameters (8571-8572, 8586, 8806-8809), so every file-backed group can be cooked.
- Three kinds stay decoded:
  - **The 2x2 flats**, which the code makes.
  - **The brick ID maps.** They are exact RGBA IDs read with nearest filtering (brick_ids.py:238; 8828), so compression or mips would corrupt them.
  - **The cropped vignette decals (9561).** The material has no UV offset (6119-6125), so they wait until the importer cuts the same rectangle.

**Q2. The shop cards.**
- Saving from loading only the shown state: 420 MB (630 to 210).
- Saving from cooking: 406 MB (to 224).
- Saving from both: 555 MB (to 75).
- Cooking needs stretching. 1855 is not a multiple of 4, which forces the texture uncompressed (Texture.cpp:4254-4263). A texture whose sides are not powers of two never streams (Texture.cpp:1841-1872, 1897-1922).
- StretchToPowerOfTwo (TextureDefines.h:178-194) keeps UV 0-1, so the material is unchanged (inferred).
- Loading only the shown state still matters once the cards are cooked. A texture bound to a material is streamed even at weight 0 (inferred).

**Q3. Compression per role.** It follows the base material's declared samplers: colour COLOR, normal NORMAL, roughness LINEAR_COLOR (make_base_material.py:445).
- TC_Default with sRGB off derives LINEAR_COLOR (:2377).
- TC_Masks derives MASKS (:2384), a mismatch, so roughness avoids it.

**Reference.**
- Both games cook textures and stream them through a pool: Mafia 1,500 MB at the 6 GB tier (12-tech-budgets.md:82), Kingdom Come II 4,096 MB (:41).
- Mafia's materials use colour, packed-mask and normal textures (05-visuals.md:38). Its decals are mostly 1024 px (:42).
- Neither study records the formats: none found.
- Their pool sizes do not fit as they stand. LEDGER's pool is 800 MB with 187 MB needed (MEMORY-WHERE:49), and about 420 MB more still fits.

## 3. Steps (about 15.5 hours)

1. **Name each run-time texture after its file** (0.5 h).
   - How: CreateTransient takes a name (Texture2D.h:342).
   - Touches: line 6182; SliceCharacter.cpp:726.
   - Check: step 6's dump names the 423 MB.
2. **Shown state only** (1.5 h).
   - How: load one state and bind it to DayTex, LitTex and DarkTex. ReDriveShopInteriors (8566) swaps it when the light changes or GShopsDark changes.
   - Touches: lines 8437-8447.
   - Check: a log line with each shop's state; editor pictures of the day and shopnight views.
3. **Importer** (5 h).
   - How: a new tools/ue/import_run_pictures.py, shaped like import_glass_bake.py.
     - The list comes from stage_game_data.wanted().
     - The role comes from the file-name ending; any alpha means BC7.
     - The settings in the table; StretchToPowerOfTwo where needed; mips from the texture group; streaming on.
     - Decal rectangles are cut beforehand.
     - An MD5 stamp with --check-fresh in ci-checks.
     - Added to make_base_material.py's import step.
   - Checks:
     - --selftest passes.
     - The run's own status line reads OK n/n.
     - Each texture's compression, sRGB and derived sampler are read back against its slot (make_base_material.py:519-555).
     - Asset-check rules 5, 6 and 8 pass. The CityPack normals are JPEG, so they need a rule-6 waiver with a DECISIONS line.
4. **Game reads the asset first** (3 h).
   - How: LoadObject by path, as LoadGlassBake does (1102-1106), falling back to ImportTexture.
   - Touches: the eleven sites and SliceCharacter.cpp:726. LedgerPaper.cpp:70 waits, since its UI pictures were not loaded at the peak.
   - Checks: the game target built locally; CoreTests and the regression set; a cooked/decoded count in the log; stage_game_data --list missing=0.
5. **Gate** (2 h; gate skill, sections 1-6).
   - Editor pictures at scalability 2 of: the hook by day and night, the reverse view, chandler@x, shopnight, the office's three, and -PageAt on one lettered card and on the sky.
   - One fresh reviewer per view, beside its last good picture, told what changed.
   - The session decides whether a visible change is a whole-frame look for his page.
6. **Packaged day walk** (1 h plus the build).
   - How: `tools/p1-packaged.ps1 -Only day-walk -Tag cookpics`, with memreport -full and rhi.DumpResourceMemory at frame 1100. That is after the plateau, so the peak frames stay unstalled (inferred).
   - Checks: the peak at about 4,650 or below; Transient Texture2D at about 50 or below; NonStreamingMips falls; the streaming need stays under 800 MB.
7. **Optional: the worn fronts** (1.5 h).
   - Why: 5410x550 is not block-aligned (Texture.cpp:4260; inferred).
   - Touches: their importer, not traced.
   - Check: the same walk's listtextures.
8. **Records** (0.5 h): DECISIONS, RECIPE, the time log.

## 4. Risks and the check that catches each

| Risk | Mitigation | Check |
|---|---|---|
| Banding: BC1 on smooth gradients | BC7 for the cards and sky | Zoomed crops by the shopnight and hook-night reviewers |
| Mip blur on lettering at distance or a slant (today's single mip shimmers instead) | TMGS_Sharpen on cards and signs | The -PageAt reviewer |
| sRGB colour shift: a map in the wrong space is off by a gamma curve (6188-6190) | | Step 3's readback fails; tools/surface_values.py before and after |
| Normals: whether the NORMAL sampler rebuilds Z the same from BGRA8 (unverified) | | The hook and reverse views |
| A stale asset | | --check-fresh and asset-check rule 8 |
| A hitch while a 4096 PNG decodes at a light change, between steps 2 and 4 (unmeasured; the walk covers day only) | | none |
| Streaming dropping top mips | | The StreamingPool column against the 800 MB pool |

## 5. Not reached or unverified

- **Unreached:** https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-compression-settings-in-unreal-engine gave only a table of contents on 8 Nov.
- **Unverified:**
  - mips for textures that are not a power of two;
  - the shop-room material's samplers;
  - the 423 MB's owners;
  - whether the scalp belongs under /Game/Ledger/MetaHumans;
  - the worn fronts' importer;
  - both games' compression formats.

## Fixes from the fresh review (8 Nov, COOK-PICTURES-REVIEW-2026-11-08.md: pass with fixes), binding on the steps above
1. The importer sets power-of-two mode, mips and compression itself and reads back the mip count; a fresh import turns mips off for non-power-of-two sides and compression off for sides not a multiple of four (TextureImportSettings.cpp:222-249). The same cause is taken as the worn fronts' (resize them to 5412x552, not cut).
2. A map's role comes from the spec's map order, as the game reads it, never from its file name (_nor_dx_2k, _rough_2k); the file list from stage_game_data.wanted() leaves out the ID maps, UI art, .hdr files and the cropped decal sources.
3. Step 2 keeps each card's light as today (night ? lit or dark as set : day; Mickey's card does not follow GShopsDark); steps 2 and 4 land together, so no picture is decoded at a light change.
4. Shop cards cook without mips (room-corner lines otherwise): 56 MB, not 75. The gate adds Tom's face (the scalp) and the brick corner; any visible change across the street goes to his page. The scalp texture is named by Rename() or through ImportTexture; the runner's BC7 encode time is budgeted in step 8's build.
