# 33 kinds of seeded greyscale wear mask, each with its rule of place, size and shape in metres, density, tone per surface, wet and dry look, texel scale and checks, from 27 measurements on CC0 photographs and the Hook sheet; facade-wide soot and the dark head under every roof edge are now kinds of their own, streaks follow the photographs, wet and dry are kept apart, and nothing from 2000s Britain or America is in it.

Wear on Quay Street (the Hook, Meridian; 1990, Britain, port town) for unit 4.5. Written 8 October 2026, cloud week 42, by the wear target writer. Companion files in this folder: `target.json` (every number below, for a script), `target_drawing.py` (draws each kind's shape envelope at real scale from `target.json` alone), `self_check.py` (tests the target against its own photograph measurements and for internal consistency, runs the composition and placement checks and refuses deliberately wrong masks). Previews of the measured photographs are in `production/previews/cloud-week/refs/wear/`. This is the target's second and last pass after the review of 8 October (`TARGET-REVIEW.md`, 12 faults); section 11 says how each was answered.

Self-check: `self_check: passed=1142/1142 failed=0 (A structure, B tone, C photographs, D envelopes, E composition and wrong masks, F placement; 33 kinds)` (last run 2026-10-08).

## How to read this

- Every number carries its kind: **Photo** (measured on a photograph or scan; ledger id M01 to M27 in section 3, with method and error), **Sheet** (measured on the Hook sheet, our own mood bar, not a photograph), **Read** (printed in a repository record or a standard), **Derived** (arithmetic on the others), **Judgement** (mine, bounded by the measured numbers; the first things to change on the builder's evidence).
- Units: metres unless a name ends `_mm`. Tones: sRGB 0 to 255 for colour; a linear-light multiplier on the surface's albedo; L* is CIE D65. Masks are greyscale 0 to 1 (0 nothing, 1 the kind's full effect).
- A mask is not a colour. The builder colours it by surface from each kind's `tone` table. For a **darkening** mark (multiplier below 1) the builder applies, per channel in linear light, `albedo_c = surface_c * lerp(1, ratio_c, mask * strength)` with `ratio_c = mark_lin_c / surface_lin_c`: the mark's dirt tint travels in its stored colour, so the same ratios carry over to the street's real brick and paint (the brick and shopfront families' colours win where they differ). For a **replacing** mark (multiplier 1.0: salt, patch, gum, paper, ochre iron) `colour = lerp(colour so far, mark_lin, mask * strength)`. Strength is the house's wear (0.55 to 1.0, `production/specs/street-wear.json`) times the side weight in each kind's rule (and, for wall_soot, the house's state weight).
- **One surface per decal.** The placer picks the tone row from the material under the decal's origin; a decal that crosses two surfaces (a wall and its stallriser, a channel and the road) is split at the joint and each part takes its own row. Wet and dry are explained in section 4: every multiplier in a tone row is the DRY value; the Hook sheet is a wet street.
- The four layers of the asset plan (SUMMARY.md section 8): **L0** in the materials (height-gradient foot bands, the head under roof edges, facade-wide soot, broad mottle), **L1** rule-placed wall decals, **L2** ground marks written once into the ground's virtual texture, **L3** a few hand-placed hero decals (the Hook sheet's pale patch on the left gable; Mickey's wall foot). Each kind below says which.

## 1. What the street has today, and what is missing

Read from `tools/street_wear.py`, `tools/make_wear_masks.py`, `production/specs/street-wear.json`, and looked at in `production/previews/morning-hook-day-2026-10-08.jpg`, `morning-reverse-day-2026-10-08.jpg`, `front-foot-wear-2026-10-07.jpg` and the Hook sheet.

- **Built:** eight kinds (puddle, streak, algae, splash, wash, damp, oil, soot), 159 decals over 13 houses, one picture a kind (three for streaks and puddles), masks cut from ambientCG's Leaking005 and SurfaceImperfections003/012. ambientCG's metadata (reached today) says all three are generated (PBRProcedural or PBRApproximated), not photographs of wear.
- **On the frames of 8 October:** the brick reads new and even; no foot band on any brick wall (the Hook sheet's gable foot is black to 0.33 m); no streaks under any sill or coping; the stallriser feet carry a faint noisy fringe and the front-foot picture's 'chip box' (a rectangular band, 0.565 to 0.655 m) is the only paint wear; the footways are clean even slabs of one tone with no stain, no patch, no crack, no gum, no ends; the road has puddles and lines but no oil, no scuff, no reinstatement, no crack; kerbs and gully are clean; downpipes have no rust or green.
- **Missing, by kind:** 25 of the 33 below do not exist at all (salt_bloom, rust_bleed, paint_flake, paint_fade, render_crack, render_patch, poster_remnant, bird_dropping, gum, cig_end, pavement_stain, flag_patch_crack, road_blot, tyre_scuff, road_patch, road_crack, gutter_grime, iron_wear, grate_wear, line_wear, sign_ghost, graffiti_buff, handle_wear, stone_top_lichen, footway_infill); the other 8 exist in a weaker form (wall_foot_splash is today's splash and the recipe's foot rise, wall_foot_damp is the damp, streak_sill is the streak, streak_coping is the wash, algae_downpipe is the algae, road_oil is the oil, wall_soot is the recipe's patch noise and house looks, wall_head_band is the recipe's head water paths). Today's soot (chimney-stack tops) and puddles are outside this family or have their own research (WET-ROAD).
- **The wear layer that already exists in `tools/art-recipes/terrace-front.py`** (`_wear()`, read in full on 8 October; it multiplies over the map before `_wetten()` and replaces no texture): (1) a patch noise, `WEAR_PATCH_SCALE` 0.45 cycles per metre, the dirtiest patch x `WEAR_PATCH_DEPTH` 0.28, on every surface in `WEARS` (brick_red, brick_grey, slate, stone, paving, kerbstone); (2) a foot rise on the surfaces with splash on (brick, slate, stone): x `WEAR_SPLASH_DEPTH` 0.55 at the pavement rising to 1.0 at `WEAR_SPLASH_M` 1.5 m; (3) tall-noise 'water paths down from the top', `STREAK_DEPTH` 0.70, from `STREAK_FROM_Z` 3.6 m to `STREAK_FULL_Z` 6.4 m; and (4) per-house looks as vertex colours: `HOUSE_LOOKS` (an orange-red stock, a purple-brown, a sooted black-brown 0.60/0.56/0.56, a cleaned front) and `HOUSE_SET_FACTOR` (as built 0.90, sooted 0.74, cleaned 1.0/0.97/0.93). **Nothing may be darkened twice**, so this target says which of them its kinds replace:

| the recipe's | what this target does with it |
|---|---|
| per-house brightness: HOUSE_LOOKS (sooted look 0.60/0.56/0.56, about 0.57) and HOUSE_SET_FACTOR (0: 0.90, 1: 0.74, 2: 1.0 / 0.97 / 0.93) | the looks keep their hue and their own value spread; the brightness each set carried is taken over by wall_soot's state: set 1 sooted (x 0.42 at mask 0.9, about x 0.48 on average), set 0 as built (weight 0.35, about x 0.82), set 2 cleaned (weight 0, the warm shift kept). The builder divides a sooted house's look by its own mean so nothing is darkened twice; the photograph is 0.37 to 0.48, the recipe's 0.57 was lighter (D8). |
| patch noise: WEAR_PATCH_SCALE 0.45 cycles/m, WEAR_PATCH_DEPTH 0.28 (the dirtiest patch x 0.28), on every surface in WEARS | wall_soot's mottle IS this job, with a measured depth (mask std 0.07 around 0.90; Photo M21): set WEAR_PATCH_DEPTH to 1.0 where wall_soot is applied (brick and render walls). Paving and kerbstone keep the recipe's patches (ground kinds have no mottle). |
| foot rise: WEAR_SPLASH_M 1.5, WEAR_SPLASH_DEPTH 0.55 (x 0.55 at the pavement rising to 1.0 at 1.5 m), on the surfaces with splash True | wall_foot_splash replaces it (set WEAR_SPLASH_DEPTH to 1.0, so the rise is 1 everywhere, where this target's foot band is applied); wall_foot_damp supplies the broad part to 1.2 m and wall_soot's lower wall the last 10 %. |
| head water paths: tall noise STREAK_ACROSS 6.0 / STREAK_DOWN 0.35, STREAK_DEPTH 0.70, STREAK_FROM_Z 3.6, STREAK_FULL_Z 6.4 | wall_head_band gives the head under every roof edge and streak_coping the leaking-joint fingers: set STREAK_DEPTH to 1.0, so the recipe's streaks give way and no head is darkened twice. |
| _wear() then _wetten() | kept: wear first, the wet multipliers of each kind (section 4) on top, once. |

In short: `wall_foot_splash` replaces the foot rise (set `WEAR_SPLASH_DEPTH` to 1.0 where this target's foot band is applied), `wall_head_band` and `streak_coping` replace the head water paths (set `STREAK_DEPTH` to 1.0), `wall_soot` replaces the patch noise and the brightness of the house looks. The hue and value spread of the looks stay.

- **Why they read as faint:** one picture a kind, strength 0.4 to 1.0 everywhere, and edges softer than a photograph's. The measured road is low contrast (4 to 12 % of the area marked) but its marks are many and of several sizes; the measured walls have a hard-edged flake (0.4 mm) beside a soft damp blotch (19 mm). The target gives each kind its own edge.

## 2. Sources

Photographs for measuring only, from free licences; none is placed in the game, traced into a texture or fed to an image model. All are modern (2018 to 2026); for each the table says why the wear it shows would look the same in 1990, or not.

| id | what | URL | date read | author | licence | date taken or published | what it shows | used |
|---|---|---|---|---|---|---|---|---|
| S1 | Poly Haven texture scans (CC0), diffuse maps 2k/4k, metric dimensions from the site's asset record | https://polyhaven.com/ and https://api.polyhaven.com/files/<id> | 2026-10-08 | various, per file below | CC0 1.0 | published dates per file below | Close, flat-lit, de-lit scans of worn surfaces at a known metric size (1 to 30 m): the wear's shape, size, share and albedo. The place is not given by the site (tags only: for plaster_brick_01 the site's tags are plaster, rough, old, moss, sewer, tunnel, trimsheet), 2018 to 2026. Used for measuring; none is placed in the game, traced into a texture or fed to an image model. | yes |
| S2 | Poly Haven HDRI panoramas of London streets (CC0), Andreas Mischok: urban_street_02 (8k, taken 2019-08-18), urban_street_03 (8k, 2019-09-07), urban_street_01/04, birbeck_street_underpass, bethnal_green_entrance, limehouse (4k) | https://polyhaven.com/hdris, https://api.polyhaven.com/files/<id>, https://api.polyhaven.com/info/<id> | 2026-10-08 | Andreas Mischok | CC0 1.0 | taken 2019, per list below | Real London streets (an estate road and a residential street) re-projected here to ground ortho tiles and wall views. Used to measure ground wear (oil, litter, flags, reinstatement, the channel, the yellow line), the soot-blackened garden wall (M21) and the sills' streaks (M17, M23). | yes |
| S3 | ambientCG metadata API (CC0): creation method of each asset | https://ambientcg.com/api/v2/full_json | 2026-10-08 | ambientCG (Struffelproductions) | CC0 1.0 | n/a | Reached; the images and downloads were NOT (the download redirect and the thumbnail hosts f003.backblazeb2.com and acg-media.struffelproductions.com answer 403 through this cloud's proxy). The metadata says ChewingGum001/002, Leaking001 to 019 and RoadLines006 to 035 are PBRProcedural (generated), SurfaceImperfections001/003 and Scratches003 PBRProcedural, SurfaceImperfections007/012 and Sticker001 PBRApproximated: NOT photographs of real wear, contrary to the brief. Only AsphaltDamageSet001 (atlas), Moss001 and ManholeCover003 to 011 are photogrammetry. The repo's masks (tools/make_wear_masks.py) are made from Leaking005, SurfaceImperfections003 and 012: all procedural or approximated. | metadata only (creation methods) |
| S4 | The Hook sheet (repository file, pass 4) | production/previews/hook-sheet-2026-10-05.jpg | 2026-10-08 | the project | the project's own | 2026-10-05 | The mood bar: wall feet, dark heads under verges, wet flags, brown stains, a downpipe with paint loss, a wet street (RULINGS 3 October). Not a photograph (generated picture); measured only as 'Sheet'. It shows NO rain streaks under any sill, coping, verge or gutter (looked at enlarged 2 to 4 times), so nothing about streaks is taken from it. | yes |
| S5 | Repository records: production/research/asset-plan/SUMMARY.md section 8 and 4-SIGNAGE-AND-WEAR.md, street-wear/PAINTED-FRONTS-2026-10-07.md and WET-ROAD-2026-10-08.md, aaa-street/BRICK-COLOUR-2026-10-08.md, tools/street_wear.py, tools/make_wear_masks.py, production/specs/street-wear.json, ledger/Assets/StreamingAssets/Decals | repo | 2026-10-08 | the project | the project's own | 2026-10-01 to 08 | What exists: eight kinds, one picture each (three streaks), masks from procedural CC0 maps, house wear 0.55 to 1.0. Also read: tools/art-recipes/terrace-front.py (the wear layer: patch noise, foot rise, head water paths, per-house looks; section 1) and production/specs/vignette-scene.json, vignette-pieces.json, 2-VEHICLES.md, hook-cast.json (places). | yes |
| S6 | Search summaries (leads only, no number used from them): Keep Britain Tidy 2017 gum staining on 99 % of main shopping streets; BRE Digest 245 rising damp 'in excess of 1 m' and heritage guidance 0.5 to 1.5 m; sill-run-off mechanism (patent text) | keepbritaintidy.org; designingbuildings.co.uk (DG 245); patents.google.com (DE7911046U1) | 2026-10-08 | various (summaries only) | n/a | n/a | Directions for what to read once the network opens. | no (leads) |
| S7 | Poly Haven info API records (CC0 metadata): api.polyhaven.com/info/<id> for plaster_brick_01, concrete_pavement_02, asphalt_02 | https://api.polyhaven.com/info/<id> | 2026-10-08 | Poly Haven (metadata) | CC0 1.0 | n/a | Authors, dates, sizes, categories and tags. plaster_brick_01: tags plaster, rough, old, moss, sewer, tunnel, trimsheet; asphalt_02: tags asphalt, cracked, road, tarmac road, gritty, weathered, grey, cracking, tar, cracks; concrete_pavement_02: tags concrete, sidewalk, urban, city, pavement, street, footpath. | metadata only (tags, authors, dates) |

**Authors and dates, per file (S1, Poly Haven textures, all CC0, published date from the site's record; place not given by the site):**

- `aerial_asphalt_01`: Rob Tuytel, 2020-08-10
- `asphalt_01`: Dario Barresi and Charlotte Baglioni, 2022-10-04
- `asphalt_02`: Rob Tuytel, 2020-08-06
- `asphalt_03`: Barresi and Baglioni, 2023-02-09
- `asphalt_04`: Jenelle van Heerden and Sergej Majboroda, 2023-11-16
- `asphalt_06`: Jan Martens, 2024-12-03
- `road_damaged`: Dimitrios Savva, 2026-06-26
- `road_damaged_2`: Dimitrios Savva, 2026-07-03
- `concrete_pavement_02`: Charlotte Baglioni, 2024-03-29
- `concrete_pavement`: Charlotte Baglioni, 2024-02-20
- `pavement_01`: Rob Tuytel, 2019-06-18
- `pavement_02`: Dario Barresi and Charlotte Baglioni, 2023-02-14
- `peeling_painted_wall`: Dimitrios Savva, 2024-11-21
- `painted_worn_brick`: Dimitrios Savva, 2024-04-09
- `rebar_reinforced_concrete`: Amal Kumar, 2025-01-28
- `damaged_plaster`: Amal Kumar, 2025-07-31
- `concrete_wall_003`: Dimitrios Savva and Rico Cilliers, 2021-08-24
- `preconcrete_wall_001`: Dimitrios Savva and Rico Cilliers, 2021-08-12
- `cracked_concrete_wall`: Dimitrios Savva and Rico Cilliers, 2022-12-01
- `concrete_layers`: Amal Kumar, 2024-05-02
- `plaster_brick_01`: Rob Tuytel, 2018-06-18
- `mossy_brick`: Amal Kumar, 2024-12-10
- `brick_moss_001`: Dimitrios Savva and Rico Cilliers, 2021-06-29
- `concrete_moss`: Rob Tuytel, 2024-10-24
- `rusty_painted_metal`: Amal Kumar, 2025-03-18
- `asbestos_sheet_02`: Amal Kumar, 2025-04-01
- `dirty_concrete`: Rob Tuytel, 2021-01-12
- `brick_wall_006`: Jan Burghardt, 2023-04-11

**Looked at, not used** (S1 files that appear in the author list but were never measured): `concrete_pavement` (Charlotte Baglioni, 2024-02-20); `pavement_01` (Rob Tuytel, 2019-06-18); `pavement_02` (Dario Barresi and Charlotte Baglioni, 2023-02-14); `painted_worn_brick` (Dimitrios Savva, 2024-04-09); `concrete_moss` (Rob Tuytel, 2024-10-24); `dirty_concrete` (Rob Tuytel, 2021-01-12); `brick_wall_006` (Jan Burghardt, 2023-04-11). Downloaded as 2k diffuse maps during the survey of Poly Haven's brick, plaster, concrete and pavement scans; none was measured and no number, colour or shape in this target comes from them. They are listed so the S1 author list is complete and a reader does not look for a measurement that does not exist.

**S2, the panoramas (Andreas Mischok, CC0, London; taken and published dates from the site's record):** urban_street_02 (taken 2019-08-18 about 06:45 UTC, published 2019-08-29; overcast; an estate road with brick walls, a wrought-iron fence, litter and a utility reinstatement; 8k used), urban_street_03 (taken 2019-09-07 about 07:46, published 2019-09-26; overcast; a residential street with patched flags, granite kerb, cobble channel, oil-dripped asphalt, stock-brick walls; 8k used), urban_street_01 (taken 2019-08-18, resurfaced street, not used for numbers), urban_street_04 (taken 2019-09-14, sunlit stucco Kensington, not used), birbeck_street_underpass (taken 2019-08-18, graffiti wall, sun-blown, not used for numbers), bethnal_green_entrance (taken 2019-08-18, block paving and leaves, not used), limehouse (taken 2019-05-19, a 1980s-90s Docklands development, clean: the contrast case, not used for numbers). Camera height 1.6 m assumed and proved by the 75 mm yellow line (M04).

**Why the 2019 and later wear is or is not the 1990 wear:** see each source's 'same in 1990' line in `target.json` sources. In short, physical wear (cracks, paint loss, damp, moss, rust, oil drips, kerb litter, flags replaced after utility work, sealed asphalt cracks) looks the same in 1990; what differs is amount (1990 walls sootier, pavements dirtier, cars leakier, and no wash-down culture) and a few 2000s additions that must not appear (section 4).

**Unreached (the network refused, so nothing from them is evidence):**

- commons.wikimedia.org, geograph.org.uk, archive.org, flickr.com, historicengland.org.uk: CONNECT refused (HTTP 000/403), tested 2026-10-08.
- ambientCG image and download hosts (ambientcg.com/get redirect, f003.backblazeb2.com, acg-media.struffelproductions.com): 403. ambientCG Bricks073C/075B/079/094/097, Concrete038/039, PavingStones036/149, Plaster007, Tiles038 are therefore unread.
- Once the network opens, read: Geograph photographs of Hull, Grimsby, Hartlepool, Sunderland, Liverpool dock streets 1985 to 1995 (wall feet, rain streaks, salt bloom, fly-posters, gum on shopping-street flags); BRE Digest 245 full text; Keep Britain Tidy / Defra litter survey 2002 for gum per square metre; British Library 'Britain in the 1980s' street photographs; Historic England archive, John Gay and Eric de Mare collections for soot-blackened brick.
- Poly Haven's info API WAS reached (8 October) and gives the tags above; the site gives no place for any scan, so 'photographed in unknown places' stands for every S1 file.

**Leads only (search summaries, no number used):** Search summaries (leads only, no number used from them): Keep Britain Tidy 2017 gum staining on 99 % of main shopping streets; BRE Digest 245 rising damp 'in excess of 1 m' and heritage guidance 0.5 to 1.5 m; sill-run-off mechanism (patent text)

## 3. Measurements, with method and error

**M01. Dry asphalt albedo on eight scans.** Files: asphalt_01; asphalt_02; asphalt_03; asphalt_04; asphalt_06; road_damaged; road_damaged_2; aerial_asphalt_01.

- Method: Central 70 % of each 2k diffuse map; per-channel median; L* from sRGB D65.
- Error: +/-3 sRGB levels (JPEG, unknown colour cast of each scan); scans are de-lit albedo.
- Values: `{"asphalt_01": {"median_srgb": [89, 80, 70], "L_median": 34.5}, "asphalt_03": {"median_srgb": [81, 67, 56], "L_median": 29.5}, "asphalt_06": {"median_srgb": [150, 141, 127], "L_median": 59.0}, "asphalt_02": {"median_srgb": [87, 86, 80], "L_median": 36.3}, "asphalt_04": {"median_srgb": [130, 126, 123], "L_median": 53.1}, "road_damaged": {"median_srgb": [73, 56, 45], "L_median": 25.2}, "road_damaged_2": {"median_srgb": [88, 64, 48], "L_median": 29.4}, "aerial_asphalt_01": {"median_srgb": [97, 92, 97], "L_median": 39.7}}`
- Reading: Worn dry asphalt spans L* 25 to 59; the per-channel median of the three mid scans (asphalt_02 87/86/80, aerial_asphalt_01 97/92/97, asphalt_01 89/80/70) is 89/86/80, L* 37 (the first pass used their mean, 91/86/82).

**M02. Wear marks on a 30 m x 30 m worn road scan (aerial_asphalt_01).** Files: aerial_asphalt_01 4k, 7.32 mm/px.

- Method: L* smoothed 44 mm (removes the aggregate), minus L* smoothed 0.88 m; dark marks = deficit beyond a threshold; connected components; linear = aspect > 6 and length > 0.5 m; cross-profile averaged about the skeleton of the 16 linear marks.
- Error: Thresholds +/-1 L*: share 4.6 % (dL 4) to 23.5 % (dL 1.5). Widths +/-15 mm (7 mm pixel). The tile is a tileable processed scan: spacing of features is the photographer's tile, not a street.
- Values: `{"share_dL1.5": 0.235, "share_dL2.5": 0.125, "share_dL4": 0.046, "blob_eqd_mm_p10_50_90_dL2.5": [160.0, 223.0, 488.0], "blob_n_per_100m2_dL2.5": 99.8, "blob_n_per_100m2_dL4": 40.9, "linear_n_dL2.5": 16, "linear_per_100m2": 1.78, "linear_len_m_p10_50_90": [1.7, 4.0, 8.6], "scuff_fwhm_mm": 90, "scuff_peak_dL": -9.5, "scuff_profile_mm": [0.0, 15.0, 29.0, 44.0, 59.0, 73.0, 88.0, 103.0, 117.0, 132.0, 146.0, 161.0, 176.0, 190.0], "scuff_profile_dL": [-9.53, -8.11, -5.84, -3.94, -2.63, -1.74, -1.21, -0.67, -0.25, -0.01, 0.22, 0.53, 0.68, 0.77]}`
- Reading: Real road wear is low contrast and broad: 4 to 12 % of the area is marked, blobs about 0.22 m, tyre scuffs about 90 mm wide and 2 to 8 m long, with soft edges about 70 mm.

**M03. Cracks in a worn asphalt scan (asphalt_02, 3 m x 3 m).** Files: asphalt_02 2k, 1.46 mm/px.

- Method: First pass: counted by eye on the 1400 px montage with a 3.0 m scale: one sealed crack the full 3.0 m, six hairlines 0.2 to 1.8 m, total about 7.3 m. Second pass (the review re-measured it and was right): on the full 2k map (1.46 mm/px, 3.0 m across) the sealed crack lies at x about 250; per row (every second row, 1015 rows), the width of the run below 0.7 of the surface median luminance around the darkest smoothed (2 px) pixel in columns 60 to 420.
- Error: Length +/-30 % (by eye); width +/-3 mm (1.46 mm pixel, 2 px smoothing); the patch was chosen by its photographer as a cracked road, so it is the worst case. Threshold 0.5 to 0.8 of the surface gives p50 23 to 40 mm.
- Values: `{"crack_m_per_m2": 0.8, "main_crack_width_mm": [15, 60], "hairline_width_mm": [2, 6], "detected_local_width_mm_p10_50_90": [2.9, 6.6, 12.1], "main_crack_width_mm_p10_50_90": [14.6, 35.2, 58.6], "surface_srgb_median": [87, 86, 80], "surface_L_star": 36.3, "core_L_star": 15.8, "core_L_star_unsmoothed": 13, "core_over_surface_luminance": 0.23, "rows_with_crack": 1015}`
- Reading: A cracked road carries 0.8 m of crack per m2; typical road 0.1 to 0.4 (Judgement). The sealed main crack is 15 / 35 / 59 mm wide (p10 / p50 / p90), not 40 to 90 mm, and its core is 0.23 of the surface (L* 13 to 16 on 36).

**M04. Oil drip speckle on asphalt in a London residential street (urban_street_03, 8k panorama, ground ortho-rectified).** Files: urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: Panorama re-projected to a top-down ortho tile at 3 mm/px with camera height 1.6 m; scale proved by the yellow kerb line: 24 to 26 px = 72 to 78 mm (line is 75 mm). Dots = pixels darker than 0.85, 0.75, 0.65 of a 25 px median; components of 4 px or more.
- Error: Height 1.6 +/-0.1 m gives +/-6 % on areas and +/-6 % on lengths; dot sizes +/-2 mm (3 mm pixel); threshold changes density by a factor 2.5 (167 to 67 per m2).
- Values: `{"dots_n_rel0.85": 222, "region_m2": 1.33, "per_m2_rel0.85": 167.0, "per_m2_rel0.75": 68.0, "eqd_mm_p10_50_90_rel0.85": [10.6, 16.9, 29.4], "eqd_mm_p10_50_90_rel0.75": [10.3, 13.7, 21.4], "luminance_ratio_in_dots": 0.7, "in_band_per_m2_rel0.75": 153.0, "in_band_per_m2_rel0.85": 377.0, "note_region": "per_m2_* are over the whole 1.33 m2 region of the view, which includes clean asphalt around the dotted band; in_band_* divide by the band's own area (length x width, central 90 % of the dots)", "band_length_m_visible": 1.83, "band_width_m": 0.32}`
- Reading: A parked car's drip band: about 0.3 m x 1.8 m (at least), dots 17 mm, 0.7 of the road's luminance, 154 per m2 inside the band at the darker threshold (379 at the lighter).

**M05. Utility reinstatement in asphalt (urban_street_02, ortho tile).** Files: urban_street_02 8k, Andreas Mischok, taken 2019-08-18.

- Method: Ortho tile 3 mm/px, h 1.6 m: rectangle spans 370 x 360 px; seam a dark line 10 to 17 px wide; grass tufts at 3 corners. Second pass (the review re-measured it): luminance profiles across the left seam (mean of 210 rows), seam core against the road's median in a 350 x 600 px open patch; seam colour by 5 px; infill median of x 170 to 330, y 560 to 780; the damp fringe in three boxes.
- Error: +/-0.1 m on size (height), +/-10 mm on seam; luminance ratios +/-0.05 (JPEG, 8 bit, the line is 3 to 5 px wide).
- Values: `{"w_m": 1.0, "h_m": 1.1, "seam_mm": [30, 50], "seam_ratio": [0.63, 0.77], "seam_srgb": [125, 113, 100], "road_srgb": [139, 127, 123], "infill_ratio": 0.92, "damp_fringe_ratio": [0.8, 0.86]}`
- Reading: A cover reinstatement is about 1.0 x 1.1 m with a dark seam of 30 to 50 mm that reads 0.63 to 0.77 of the road (not 0.5), brown-shifted (125/113/100 on 139/127/123); the infill is 0.92 to 0.93 of the road; a damp fringe of 0.80 to 0.86 runs along three edges.

**M06. Litter along the kerb and on the road (urban_street_02, rectilinear view yaw -165, pitch -20).** Files: urban_street_02 8k.

- Method: Pieces counted by eye on a marked picture (automatic bright-blob detection also hit aggregate glints and was rejected): kerb strip about 22 pieces over 5 m of kerb, band 0.3 m deep; road 10 pieces over 13.6 m2. Detected bright bits (aggregate included) had size 7.6, 11.2, 27.7 mm at p10/50/90. Second pass: the same kerb strip (x 150 to 1100, y 225 to 320 of the view) re-segmented by luminance against a 31 px median and colour; each bit classed tan when R - B > 45 on its mean colour.
- Error: +/-35 % on counts; 8k pixel at 7 m is 5 mm.
- Values: `{"kerb_per_m_of_kerb": 4.4, "kerb_band_depth_m": 0.3, "road_per_m2": 0.7, "piece_mm_p10_50_90": [7.6, 11.2, 27.7], "tan_bits": 4, "bits": 13, "tan_share": 0.31, "tan_share_range": [0.31, 0.46], "tan_median_srgb_in_view": [215, 171, 145], "tan_srgb_albedo": [177, 140, 110], "note_tan": "4 of 13 bits are clearly tan (R - B > 45), 6 of 13 with the borderline ones; the reviewer counted 9 of 24 (0.38) and a tan median 177/140/110 on his exposure; the view's exposure is brighter, the ratios R:G:B agree (1 : 0.79 : 0.62)"}`
- Reading: The kerb gathers about 4 pieces per metre; open road about 0.7 per m2 (a scruffier estate road; a 1990 shop street would be at or above this). About 4 in 10 filter tips are tan cork-pattern (0.31 to 0.46), the rest white.

**M07. Patched flags (urban_street_03, ortho tile of the footway, camera-to-footway 1.48 m).** Files: urban_street_03 8k.

- Method: Six slab samples by rectangle, mean linear luminance and sRGB; dark slabs 0.20 to 0.24, pale 0.34 to 0.42 (same light); shares and cracks by eye over about 18 slabs.
- Error: Luminance ratio +/-0.08; shares +/-10 points; slab size +/-15 % (height of the footway).
- Values: `{"dark_over_pale": 0.58, "dark_srgb": [133, 130, 130], "pale_srgb": [181, 172, 168], "mid_srgb": [176, 165, 161], "share_dark": 0.55, "share_pale": 0.3, "share_mid": 0.15, "cracked_slab_share": 0.11, "slab_m": [0.6, 0.7], "insitu_strip_srgb_in_view": [161, 153, 149], "insitu_strip_texture_std": 14, "dark_slab_srgb_in_view": [136, 132, 131], "pale_slab_srgb_in_view": [182, 172, 168]}`
- Reading: A 1990-style patched footway has a 0.58 luminance ratio between old and replacement flags and about 1 flag in 9 cracked. The same ortho shows a rough in-situ concrete strip at the kerbside (161/153/149 in the view, texture std 14 against about 5 on the flags): M07b, the basis of footway_infill.

**M08. Flaking paint (peeling_painted_wall, 1.8 m, 0.88 mm/px).** Files: peeling_painted_wall 2k, Dimitrios Savva, 2024-11-21.

- Method: Lab k-means (k=2, five seeds) on 512 px, nearest-centroid on 1024 px; minority cluster = loss; components of 3 px or more; edge width = 0.8 x contrast / median boundary gradient.
- Error: Share +/-2 points; sizes +/-1 mm (1.76 mm px at 1024); edge width limited by one pixel (0.4 mm means 'hard edge').
- Values: `{"loss_share": 0.063, "flakes_per_m2_ge10mm": 38.0, "eqd_mm_p10_50_90": [11.6, 17.2, 37.8], "eqd_mm_max": 249.0, "aspect_p50_p90": [2.9, 5.6], "edge_10_90_mm": 0.38, "paint_srgb": [152, 108, 93], "loss_srgb": [128, 110, 94]}`
- Reading: Flakes are small (17 mm), many (38 per m2), aspect about 3, with hard edges.

**M09. Craquelure in old paint/render (preconcrete_wall_001, 4 m; cracked_concrete_wall, 1 m).** Files: preconcrete_wall_001 2k, 1.95 mm/px, Savva and Cilliers 2021; cracked_concrete_wall 2k, 0.49 mm/px.

- Method: Dark-line detection (L below 10 px local mean by 6 to 8 L*), elongated components >= 40 mm, Zhang-Suen skeleton length; cell size and flake size by eye on the montage.
- Error: Length +/-30 % (blur merges and splits); width includes blur (true hairline 3 to 8 mm).
- Values: `{"preconcrete_len_m_per_m2": 5.68, "preconcrete_width_mm_p10_50_90": [3.9, 7.8, 14.1], "cracked_concrete_len_m_per_m2": 4.14, "cracked_concrete_width_mm_p10_50_90": [1.4, 2.8, 4.1], "cell_m": [0.14, 0.23], "flake_eqd_mm_by_eye": [45, 115], "flakes_per_m2_by_eye": [4, 8]}`
- Reading: Map cracking runs 4 to 6 m per m2 of affected render in cells 0.14 to 0.23 m.

**M10. Large paint/render loss (rebar_reinforced_concrete, 2 m).** Files: rebar_reinforced_concrete 2k, Amal Kumar, 2025-01-28.

- Method: As M08, k=3; exposed clusters 0 and 2.
- Error: Share +/-5 points.
- Values: `{"exposed_share": 0.395, "patch_eqd_mm_p10_50_90": [38.0, 108.0, 311.0], "patch_max_m": 1.29, "edge_10_90_mm": 10.5, "paint_srgb": [176, 111, 101], "exposed_srgb": [118, 101, 90]}`
- Reading: A neglected painted wall can lose up to 40 % of its paint in patches 0.1 to 0.3 m with edges about 10 mm soft.

**M11. Render loss revealing brick (damaged_plaster, 1.85 m).** Files: damaged_plaster 2k, Amal Kumar, 2025-07-31.

- Method: As M08, k=3; exposed brick = cluster 1.
- Error: +/-4 points.
- Values: `{"exposed_share": 0.18, "per_m2_ge30mm": 8.8, "eqd_mm_p10_50_90": [33.0, 67.0, 294.0], "max_mm": 453.0, "edge_10_90_mm": 11.4, "brick_srgb": [121, 90, 69], "render_srgb": [163, 150, 136]}`
- Reading: Render loss: 18 % of the area, patches 67 mm median, up to 0.45 m, edges 11 mm.

**M12. Damp and mould blotches on painted render (concrete_wall_003, 3 m).** Files: concrete_wall_003 2k, 2.93 mm/px, Savva and Cilliers, 2021-08-24.

- Method: As M08, k=3; cluster 2 = dark blotch, clusters 0+2 = yellow stain and blotch.
- Error: +/-4 points.
- Values: `{"blotch_share": 0.125, "blotch_per_m2_ge30mm": 8.8, "blotch_eqd_mm_p10_50_90": [33.0, 42.0, 171.0], "blotch_max_mm": 510.0, "blotch_edge_mm": 19.5, "stain_share": 0.493, "stain_edge_mm": 22.9, "clean_srgb": [222, 205, 182], "stain_srgb": [205, 175, 140], "blotch_srgb": [144, 124, 97]}`
- Reading: Damp blotches: 12 % of the wall, median 42 mm, p90 171 mm, 19 mm soft edge; cream render goes to 144/124/97 (x0.45 on Y).

**M13. Dark corrosion streaks (rusty_painted_metal, 2.2 m).** Files: rusty_painted_metal 2k, Amal Kumar, 2025-03-18.

- Method: As M08, k=3, cluster 1 = dark streaks.
- Error: +/-4 points; metal not masonry: geometry only.
- Values: `{"share": 0.133, "per_m2": 7.6, "length_mm_p50_p90": [116.0, 774.0], "width_mm_p50_p90": [24.0, 147.0], "aspect_p50_p90": [3.9, 11.9], "edge_10_90_mm": 15.6, "dark_srgb": [53, 33, 27], "paint_srgb": [123, 66, 48]}`
- Reading: Run-off streaks: 24 mm wide (p50), aspect 4 to 12, edges 16 mm.

**M14. Rust trickle from a fixing and rust drops (asbestos_sheet_02, 1.8 m).** Files: asbestos_sheet_02 2k, 0.879 mm/px, Amal Kumar, 2025-04-01.

- Method: Rust = (R - B) > 45 and R > 90 on a crop; trickle rows and widths read from the mask; also by eye.
- Error: +/-30 %.
- Values: `{"trickle_length_mm_at_least": 520, "trickle_width_mm": [5, 20], "drops_mm": [30, 90], "rust_share": 0.0036, "rust_srgb_median": [108, 78, 59], "drops_srgb": [140, 60, 30], "base_srgb": [116, 108, 100], "dL_vs_base": -10.2}`
- Reading: A rust trickle is 5 to 20 mm wide and at least 0.5 m long, with drops 30 to 90 mm at its end.

**M15. Moss in joints and the algae gradient at a plastered wall foot.** Files: mossy_brick 2k, 1.45 m; brick_moss_001 2k, 2.24 m; plaster_brick_01 2k, 2.7 m, Rob Tuytel, 2018-06-18.

- Method: As M08 for moss (green cluster); for plaster_brick_01 the row profile of green excess (G - mean(R,B)) and L*, rows 1024 to 2048 are the plaster (lower 1.35 m).
- Error: Shares +/-3 points; profile +/-2 greens.
- Values: `{"mossy_brick_moss_share": 0.169, "mossy_brick_patch_eqd_mm_p10_50_90": [5.5, 10.2, 31.5], "mossy_brick_edge_mm": 6.7, "brick_moss_001_share": 0.121, "brick_moss_001_eqd_mm_p10_50_90": [5.5, 13.1, 43.4], "brick_moss_001_edge_mm": 9.5, "moss_srgb": [[55, 57, 9], [74, 72, 23]], "foot_green_excess_lowest_0.45m": 26, "green_excess_above": 15, "foot_L_from_to": [47, 26], "foot_band_m": 0.45, "foot_srgb_at_0.3m": [97, 96, 41], "foot_srgb_at_0": [62, 64, 14], "plaster_brick_01_poly_haven_tags": ["plaster", "rough", "old", "moss", "sewer", "tunnel", "trimsheet"], "plaster_brick_01_poly_haven_categories": ["brick", "plaster-concrete", "wall", "man made", "dirty", "outdoor"], "tags": "Poly Haven's record (api.polyhaven.com/info/plaster_brick_01, read 8 October): tags plaster, rough, old, moss, sewer, tunnel, trimsheet; categories brick, plaster-concrete, wall, man made, dirty, outdoor"}`
- Reading: Moss fills 12 to 17 % of a wet brick wall as joint lines (mossy_brick and brick_moss_001: physical, a wall). The plaster_brick_01 gradient (the lowest 0.45 m olive-green and 20 L* darker) is NOT a pavement wall foot: Poly Haven tags it 'sewer', 'tunnel' and 'trimsheet', so its green band is a waterline in a trim sheet; the target uses it only as a waterline's colour (Judgement) and no longer cites it as agreeing with the splash profile.

**M16. Drip streaks hanging from a horizontal joint (concrete_layers, 1.55 m, 0.757 mm/px).** Files: concrete_layers 2k, Amal Kumar, 2024-05-02.

- Method: L* minus its 12 px mean < -1.5 / -2.5; vertical opening (3 x 1); components with height >= 4 x width and >= 60 mm.
- Error: Counts +/-40 % (stronger streaks only; by eye 10 to 15 per metre); widths +/-2 mm.
- Values: `{"detected_per_m_of_joint": 7.7, "width_mm_p10_50_90": [10.6, 15.1, 19.7], "length_mm_p10_50_90": [78.0, 87.0, 137.0], "by_eye_length_m_max": 0.45}`
- Reading: Individual rivulets are 10 to 20 mm wide, 0.09 to 0.45 m long, 8 to 15 per metre of joint, both dark and lime-pale.

**M17. Streak under a sill bracket on yellow stock brick (urban_street_03, yaw 105, bay window).** Files: urban_street_03 8k.

- Method: Scale from brick courses (75 mm gauge, 30 px at 2x crop); column under the central bracket 40 px wide, 180 px long; mean luminance of the column against flanks 0.97; darkest bricks 0.80 to 0.90. Re-measured by the review: course 24 px = 3.1 mm/px, core 60 to 90 mm wide at 0.66 to 0.91 of the flanks (median about 0.8), visible for about 0.30 m.
- Error: Size +/-30 % (by eye on courses), tone +/-0.05.
- Values: `{"width_m": 0.1, "length_m": 0.45, "column_Y_ratio": 0.97, "darkest_brick_Y_ratio": [0.8, 0.9], "length_m_review": 0.3, "core_width_mm_review": [60, 90], "core_Y_ratio_review": [0.66, 0.91]}`
- Reading: On a maintained 2019 London stock-brick wall the sill-bracket streak is faint and short: 0.06 to 0.10 m wide, 0.30 to 0.45 m long, 3 to 20 % darker at the core (0.66 to 0.91 at the darkest bricks). The Hook sheet shows no streaks (enlarged 2 to 4 times), so nothing about streak length or density is taken from it; length follows this photograph and M16, darkness is nudged darker by Judgement (D6, section 7).

**M18. Hook sheet, left gable foot (mood bar, not a photograph).** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Column-median luminance profile of columns 15 to 170, rows 380 to 730; brick course from autocorrelation (11 px = 75 mm, so 6.8 mm/px); wall reference rows 430 to 600.
- Error: +/-1 course (75 mm); tone +/-0.05. The sheet is a WET street (RULINGS 3 October): these are wet-state ratios; dry = ratio / the wet multiplier (section 4).
- Values: `{"mm_per_px": 6.8, "wall_median_srgb": [107, 52, 32], "dark_band_rows": [668, 716], "dark_band_height_m": 0.33, "dark_band_Y_ratio": [0.12, 0.3], "salt_band_courses": [2, 3], "salt_band_height_m": [0.15, 0.22], "salt_band_from_foot_m": [0.26, 0.46], "salt_band_Y_ratio": [0.57, 0.75], "salt_band_srgb_bright_quartile": [107, 91, 83], "salt_band_mean_srgb": [81, 60, 52]}`
- Reading: The sheet's foot: 0.33 m black band (0.12 to 0.30 of the wall), a 0.15 to 0.22 m grey-white band on its upper flank (0.26 to 0.46 m), a ragged top stepping by courses.

**M19. Hook sheet, pale patch on the left gable.** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Patch size from courses: 3.8 courses high, about 1.3 brick lengths wide; colour mean of its core.
- Error: +/-30 %. Wet-state colours (the sheet is wet): the target's dry patch colour is derived from them once (render_patch).
- Values: `{"patch_srgb": [175, 140, 92], "patch_L": 60.6, "wall_L": 26.6, "dL": 34.0, "size_m": [0.28, 0.3]}`
- Reading: A buff mortar patch 0.3 m square, 34 L* lighter than the wall.

**M20. Hook sheet, right pavement stains and road blots.** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Colour of one brown stain 85/60/44 against flag 136/129/131; sizes relative to a 0.6 m flag by eye.
- Error: +/-30 % size; 5 per 10 m2 by counting 7 stains over about 14 m2.
- Values: `{"stain_srgb": [85, 60, 44], "stain_L": 27.6, "flag_srgb": [136, 129, 131], "flag_L": 54.7, "dL": -27.1, "stain_size_m": [0.15, 0.45], "stains_per_10m2": 5, "oil_blots_on_road_m": [0.1, 0.2], "stain_over_flag_luminance": 0.236, "stain_Y": 0.0534, "flag_Y": 0.226}`
- Reading: The mood bar's pavement carries brown stains 27 L* darker than the flags, 0.15 to 0.45 m, about 5 per 10 m2. Luminance ratio of the stain to the flag 0.236 (Y 0.053 against 0.226): a wet-state ratio; dry = 0.236 / 0.80 = 0.30.

**M21. Soot-blackened stock-brick garden wall beside a cleaner panel (urban_street_03, rectilinear view yaw -125).** Files: urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: Rectilinear view 34 degrees wide; scale from the brick courses (22 px = 75 mm, 3.4 mm/px). Sooted panel = box x 20 to 520, y 590 to 720; cleaner panel = box x 590 to 1090, y 590 to 720 (500 x 130 px each, below the coping, same light); median sRGB and L* of each, mean linear luminance of each, HSV saturation of the median colours; row profile in 20 px bands (relative to each panel's mean); a second pair of boxes shifted 10 px and a reviewer's pair gave 0.37 to 0.48.
- Error: Luminance ratio +/-0.05 (box choice; JPEG); band profile +/-0.05; scale +/-1 course.
- Values: `{"sooted_srgb": [92, 81, 73], "clean_srgb": [146, 129, 110], "sooted_L_star": 35.2, "clean_L_star": 55.0, "luminance_ratio_median_pixel": 0.377, "luminance_ratio_mean_linear": 0.398, "luminance_ratio_range_two_measurers": [0.37, 0.48], "saturation_hsv_sooted": 0.207, "saturation_hsv_clean": 0.247, "saturation_ratio": 0.84, "linear_ratio_per_channel": [0.372, 0.375, 0.427], "head_band": {"depth_m": 0.4, "sooted_rows_0.15_to_0.55_m_below_coping_over_panel_mean": [0.83, 0.88], "clean_panel_same_rows": [1.03, 1.13], "extra_factor_on_sooted": [0.77, 0.8]}, "profile_sooted_20px_bands": [0.74, 1.0, 0.88, 0.87, 0.83, 0.85, 0.88, 0.88, 0.93, 1.03, 1.14, 1.1, 1.1, 1.04, 1.04, 1.06, 0.99, 0.99], "profile_clean_20px_bands": [0.71, 1.02, 1.03, 1.12, 1.13, 1.12, 1.08, 0.97, 1.03, 1.06, 1.02, 0.84, 0.81, 1.03, 1.03, 1.03, 1.0, 0.98]}`
- Reading: Soot is real and facade-wide on this 2019 street: the sooted panel is 0.377 of the cleaner one in luminance (0.37 to 0.48 by two measurers), nearly neutral per channel (0.37 / 0.37 / 0.43 in linear light), saturation 0.84 of the cleaner panel's (the review's 0.6 is not what this photograph shows); under the coping a band about 0.4 m deep is a further x 0.77 to 0.80 on the sooted panel only.

**M22. Hook sheet: the dark head under the left gable's verge, and the lower wall of the right-hand cottage (mood bar, not a photograph).** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Head: column medians of columns 15 to 170 in 20 px row bands from the verge down (rows 10 to 230), linear luminance relative to the body (rows 250 to 600); HSV saturation of the median colours; scale 6.8 mm/px from the 75 mm course (11 px). Lower wall: right-hand cottage, columns 1490 to 1590, body rows 380 to 430 against rows 436 to 500 and 516 to 572 in 8 px bands; the course there is about 17 px (4.4 mm/px).
- Error: +/-0.05 in luminance ratio; +/-1 course in height; the sheet is a generated picture and wet (RULINGS 3 October).
- Values: `{"body_srgb": [103, 52, 33], "head_srgb_rows_40_170": [68, 46, 38], "head_luminance_ratio_rows_40_170": 0.609, "head_saturation_ratio": 0.65, "head_saturation": [0.44, 0.68], "head_ratio_by_depth_m": {"0.0 to 0.2": 0.5, "0.34 to 0.48": 0.56, "0.61": 0.62, "0.75": 0.75, "0.88 to 1.0": 0.8, "1.16": 0.945, "1.4": 1.0}, "band_ratios_20px": [[10, 0.71, 0.34], [30, 0.5, 0.24], [50, 0.5, 0.29], [70, 0.56, 0.41], [90, 0.56, 0.45], [110, 0.62, 0.38], [130, 0.75, 0.54], [150, 0.8, 0.59], [170, 0.8, 0.55], [190, 0.95, 0.65], [210, 0.79, 0.6], [230, 1.01, 0.62]], "lower_wall_ratio": 0.9, "lower_wall_ratio_range": [0.84, 0.93], "lower_wall_height_m": [0.17, 0.77], "foot_ratio_0.04_to_0.18m": [0.22, 0.66]}`
- Reading: The sheet's walls grime through the brick body, not through streaks: a dark, desaturated head under the verge (x 0.50 to 0.62 over the top 0.2 to 0.75 m, 0.75 to 0.80 at 0.9 to 1.0 m, 1.0 by 1.4 m, saturation 0.65 of the body's) and, on the right-hand cottage, a lower wall about 0.90 of the wall above (0.84 to 0.93, 0.17 to 0.77 m up) with a darker foot. All wet-state values.

**M23. Rain streaks under sills on a maintained 2019 stock-brick terrace (urban_street_03, five rectilinear views).** Files: urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: Five views 40 degrees wide (yaw 30, 60, 90, 105, 120; pitch 14; the yaw-105 view is M17's). (1) By eye at full size: sill and ledge lower edges (painted stone sills, brackets, heads and cornices) with brick below, and whether a streak is clearly visible under each. (2) A column test on every white sill edge that has 0.4 m of brick below it (13 edges in four views): scale from the brick courses under the edge (75 mm), the darkest 80 mm wide column 80 to 380 mm below the edge over the median column of the same edge. The preview holds the yaw-60 view (4 of the 13 edges).
- Error: Counts by eye +/-3; column ratio +/-0.03 (brick texture std 0.02 to 0.09); scale +/-30 % (course autocorrelation, 2.3 to 6.8 mm/px).
- Values: `{"views_yaw": [30, 60, 90, 105, 120], "edges_by_eye": 30, "clear_streaks_by_eye": 1, "share_with_clear_streak": [0.03, 0.15], "column_test_edges": 13, "min_over_median_p10_25_50_75_90": [0.877, 0.914, 0.948, 0.976, 0.989], "edges_below_0.90": 2, "edges_below_0.85": 0, "darkest_column_ratio": 0.865}`
- Reading: On this maintained street almost no sill carries a visible streak: 1 of about 30 edges by eye (M17), 2 of 13 with a column darker than 0.90, none darker than 0.85. That is 3 to 15 % of sills and 0 to 15 % darkness. It is the cleanest end of the range (S2), so the target keeps the length (M16, M17) and raises the share to 15 to 60 % (typical 35 %) and the darkness to x 0.70 by Judgement (D6); the review's 50 to 70 % has no source.

**M24. Channel setts and the strip beside them against the open road (urban_street_03, rectilinear view yaw -80, pitch -25).** Files: urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: Median linear luminance of boxes in the preview: channel setts x 250 to 550, y 372 to 388; the asphalt strip beside the channel x 250 to 750, y 432 to 470 (the first 0.1 to 0.6 m off the kerb); the open road x 100 to 800, y 560 to 760; row profiles in 5 px bands. The review measured 0.236 for the setts against 0.161 to 0.170 for the asphalt.
- Error: +/-0.1 in the ratio (the setts are narrow and sloped; JPEG); same exposure for all boxes.
- Values: `{"channel_Y": [0.23, 0.29], "channel_srgb": [142, 137, 137], "road_Y": 0.17, "road_srgb": [114, 114, 120], "channel_over_road": [1.35, 1.7], "channel_over_road_review": 1.4, "strip_Y_rows_430_to_475": [0.155, 0.165], "strip_over_road": [0.91, 0.97], "strip_over_road_review": 0.95, "sheet_strip_over_road_wet": 0.7}`
- Reading: The channel is LIGHTER than the road, 1.35 to 1.7 x (the scene says it is 'in the kerb's own concrete rather than asphalt'), and the asphalt 0 to 0.6 m off the kerb is 0.91 to 0.97 of the open road. On the wet Hook sheet the strip between the inner yellow line and the kerb reads about 0.7 of the road (D7).

**M25. Paint loss and rust on the Hook sheet's gable downpipe; the gully grate of urban_street_03.** Files: production/previews/hook-sheet-2026-10-05.jpg; urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: Sheet: the pipe is columns 204 to 210 (about 48 mm wide at 6.8 mm/px; the pipe is 68 mm round), rows 100 to 720; ochre pixels = R > 95, R - B > 35, G > 70, R > 1.3 B; share of rows with ochre, patch heights by connected rows, median colour; the review's measure (columns 199 to 203) gave 7 %. Photograph: the grate in the oil-speckle ortho tile (x 235 to 395, y 160 to 280): pixels with R > B + 18, R > G + 8, luminance 30 to 120; slots black.
- Error: Share +/-2 points (a 7 px wide pipe, JPEG); patch sizes +/-7 mm (one pixel).
- Values: `{"loss_share_of_length": [0.048, 0.07], "patches_mm_long": [20, 61, 20, 156], "ochre_srgb": [125, 86, 64], "ochre_srgb_review": [141, 102, 72], "paint_srgb": [45, 33, 26], "paint_srgb_review": [50, 40, 37], "patch_rows_from_top": [122, 380, 521, 626], "grate_bar_srgb_in_view": [125, 109, 103], "grate_bar_R_minus_B": 22, "road_srgb_in_view": [114, 114, 120]}`
- Reading: The sheet's downpipe carries paint loss over 5 to 7 % of its length in patches of 20 to 160 mm, pale ochre (125 to 141 / 86 to 102 / 64 to 72) on near-black paint, at the shoe, a collar and a joint. The photographed gully grate is dull red-brown (R - B only 22) with black slots, not bright rust.

**M26. The worn yellow line (urban_street_03, ortho tile, camera 1.6 m).** Files: urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: The line's centre fitted by a quadratic through the yellow pixels (R - B > 45, R > 110); for each column the yellow pixels over the nominal 75 mm strip (25 px along the normal); loss = 1 - mean coverage; gaps = runs of columns with coverage under 0.6; colour of the pixels 5 px inside the yellow mask.
- Error: +/-8 points on the loss (the edge pixels blend with the road); gap lengths +/-6 mm.
- Values: `{"loss_share": 0.22, "loss_share_range": [0.14, 0.3], "gaps": 8, "gap_mm_median": 15, "gap_mm_largest": 515, "top_edge_raggedness_std_mm": 79, "line_thickness_px_p10_50_90": [14, 25, 28], "yellow_core_srgb_in_view": [230, 208, 154], "yellow_core_srgb_albedo_estimate": [181, 162, 120], "road_srgb_in_view": [114, 114, 120]}`
- Reading: About 22 % (14 to 30) of a street yellow line is lost in chips and gaps (most about 15 mm, one 0.5 m), its edge ragged, its colour a faded, dirt-filmed cream-yellow (about 181/162/120 as albedo, against the scene's fresh 199/168/46).

**M27. Weathered concrete paving flag albedo (concrete_pavement_02).** Files: concrete_pavement_02 2k, 1.8 m, Charlotte Baglioni, 2024-03-29.

- Method: Central 70 % of the 2k diffuse map: per-channel median, luminance percentiles, L* of the median luminance.
- Error: +/-3 sRGB levels; a scan, de-lit albedo.
- Values: `{"median_srgb": [134, 122, 110], "L_star": 52.0, "Y_p10_p50_p90": [0.137, 0.202, 0.296], "m07_dark_class_srgb": [133, 130, 130], "m07_dark_class_L_star": 54}`
- Reading: A weathered flag is 134/122/110, L* 52: the same luminance as M07's dark class (133/130/130, L* 54) in a warmer hue; the target takes the scan's hue for the albedo.

## 4. Rules that apply to every kind

**Scene and camera** (from SCENE-SLOTS.md and vignette-scene.json): Quay Street, the Hook, Meridian; 48 m, 6.0 m carriageway (two 3.0 m lanes, crossfall 1:40, crown 75 mm above the channel), footways 2.0 m (1:40), kerb upstand 0.125, channel course 0.255 wide. East side: six-bay Victorian shop parade, 6 m bays, faces WEST (the wet side in the UK's prevailing south-westerly). West side: shop block (north half) and plain terraces (quay end), faces EAST. Eye height 1.65 to 2.0 m, vertical field of view 46 to 60 degrees, frame [2560, 1440] px, so one screen pixel subtends 0.557 mrad: 1122 px per metre of mask at 1.6 m, 816 at 2.2 m (the nearest ground the camera sees), 180 at 10 m. A mask texel finer than the screen's is wasted; a coarser one shows.

**Texel rule:** each kind states its smallest feature and the px/m it needs: at least 6 texels across the smallest feature, never above the screen's 1122 px/m at 1.6 m. Features that fall under 2 screen pixels at 10 m (rust trickles, cracks, rivulets, oil dots, cigarette ends) keep their texels but the builder fades their strength or widens them beyond 6 to 8 m (each kind's note).

**Sides:** the east parade faces west, the wet side in the UK's prevailing south-westerly (Judgement, no number): streaks, algae, flaking and rust get weight 1.0 there, 0.6 to 0.8 on the west block (which faces east and is drier but sooted).

**Wet and dry (corrected after the review):** The Hook sheet is a WET street (RULINGS 3 October: 'the wet street dark, glistening'), so every ratio measured on it (M18 the foot, M19 the patch, M20 the stains, M22 the head and lower wall, M25 the pipe) is a wet-state ratio. The photographs are dry. A tone row's albedo_mult_linear is the DRY value: dry = sheet ratio / the kind's wet multiplier; the wet look is dry x wet multiplier, applied once (the first pass used sheet ratios as dry and then darkened them again). Dry sources give dry rows directly (M21 soot, M16/M17 streaks, M24 channel). Weather: the game's usual weather is drizzle and rain, never sun (RULINGS 5 October).

| kind | surface | sheet ratio (wet) | dry multiplier | wet multiplier | dry x wet | source |
|---|---|---|---|---|---|---|
| wall_foot_splash | brick_red | 0.2 | 0.27 | 0.75 | 0.203 | Sheet M18 (0.12 to 0.30, middle 0.20): dry 0.27 x wet 0.75 |
| pavement_stain | flag_concrete | 0.236 | 0.3 | 0.8 | 0.240 | Sheet M20: 0.236: dry 0.30 x wet 0.80 = 0.24 |
| road_blot | asphalt_dry | 0.5 | 0.56 | 0.9 | 0.504 | Sheet M20 (blots read black): wet 0.50 = dry 0.56 x 0.90 |
| wall_head_band | brick_red | 0.5 | 0.56 | 0.9 | 0.504 | Sheet M22 (0.50 over the top 0.2 m): dry 0.56 x wet 0.90 = 0.50 |

Wet stone is 0.68 of dry albedo and roughness 0.45; water 0.04 (Read: WET-ROAD-2026-10-08.md). salt_bloom keeps 0.9 of its brightness in drizzle and damp (the wet sheet shows it grey-white) and falls to 0.6 only in heavy rain with water running down the wall. The first pass's 'dry: lighter by a third' note on pavement_stain is deleted (its dry multiplier is the stated 0.30).

**Order, floor and colour (the `compose` block of target.json; self_check part E runs it):** Marks are applied to the clean albedo in a fixed order, then clamped at a floor, then the replacing marks are laid. A darkening mark (albedo_mult_linear < 1) multiplies per channel by lerp(1, ratio_c, mask x strength) with ratio_c = mark_lin_c / surface_lin_c (the dirt tint travels in the stored mark colour; linear light); a replacing mark (multiplier 1.0) is lerp(colour, mark_lin, mask x strength) over the colour already darkened. Strength = house wear (0.55 to 1.0) x the side weight x, for wall_soot, the state weight. One surface per decal: the placer picks the tone row from the material under the decal's origin and a decal that crosses two surfaces is split at the joint.

- **Walls**, in this order: (1) L0 in the material, multiplicative: `wall_soot`, `wall_head_band`, `wall_foot_damp`, `wall_foot_splash`, `paint_fade`; (2) L1 darkening decals, multiplicative: `streak_sill`, `streak_coping`, `algae_downpipe`, `handle_wear`; (3) replacing marks last, each over the colour already darkened: `salt_bloom`, `render_patch`, `render_crack`, `paint_flake`, `poster_remnant`, `bird_dropping`, `rust_bleed`, `sign_ghost`, `graffiti_buff`, `stone_top_lichen`, `iron_wear`. The review listed rust with the darkening marks; its tone table (first pass) is a replacing colour, so it is laid with the replacing marks, after the streaks it hangs under.
- **Wall floor 0.15:** The product of the darkening multipliers on any texel is clamped at 0.15 of the clean albedo's luminance (the colour is scaled up to it, hue kept) before the replacing marks. The Hook sheet's darkest foot is 0.12 to 0.30 of its wall (M18). Unclamped, a sooted foot beside a downpipe stacks soot 0.42 x damp 0.5 x splash 0.27 x algae 0.40 = 0.02; at house wear 1.0 on a cleaned wall, splash x damp x algae is 0.05.
- **Salt:** salt_bloom is a replacing mark laid AFTER all darkening: its grey-white bricks (Sheet M18 0.57 to 0.75 of the wall and above) stay pale; laid before the darkening they would come out dark brown (check composed_salt_ratio, and the order test in part E).
- **Ground**, in this order: `flag_patch_crack`, then `footway_infill`, then `pavement_stain`, then `gutter_grime`, then `road_patch`, then `road_crack`, then `tyre_scuff`, then `road_blot`, then `road_oil`, then `gum`, then `cig_end` (stage names: 1 flag tone class (and infill); 2 pavement_stain and halos; 3 gutter_grime; 4 road_patch, road_crack, tyre_scuff, road_blot, road_oil; 5 gum and cig_end; 6 puddles (WET-ROAD), on top, outside this target).
- **Ground floor 0.28:** 0.28 of the clean surface albedo (dry). The review proposed 0.35; the sheet's own brown stain is 0.236 wet = 0.295 dry (M20), so 0.35 would clamp the sheet's measured mark (D12). Only crack cores, gum and oil-dot cores may go below it. Exempt from both floors: `road_crack`, `gum`, `road_oil`.
- **Not composed on a wall or the ground:** `line_wear`, `grate_wear`: line_wear is the loss mask over the lines family's own paint layer (the road under it is composed as above); grate_wear and iron_wear act on the iron objects' own materials, not on a wall or the ground (iron_wear is listed with the replacing marks only for the order of marks on a downpipe that stands on a wall).
- **House state** (`wall_soot` strength): sooted 1.0, as built 0.35, cleaned 0.0 (Judgement; houses by brick_set 1, 0, 2 of street-wear.json (7, 4, 2 of 13)).

**Places (x in metres along the street, from the quay end; the numbers behind every 'near the quay', 'the rank', 'standing places' in the rules):** x runs along the street from the quay end (x 0, the quay beyond it) to the inland end (x 48); the east side is the shop parade, which faces west; the west side faces east (vignette-scene.json street.length_m 48; blocks start_x_m)

| place | side | x range or value | what stands or acts there | source |
|---|---|---|---|---|
| quay_end | both | [0, 9] | salt_bloom and bird_dropping weight 1.0 within 12 m of the quay end (x 0 to 15); 0.4 elsewhere | vignette-scene.json blocks (east_parade start_x_m 3.0, 6 bays of 6 m; west_south start_x_m 3.0) |
| rank | east | [3, 9] | 1 to 2 cars | 2-VEHICLES.md (Jafar 22 September: the rank holds one or two cars); hook-cast.json (Ron keeps Mickey's door and the rank) |
| fishmonger_apron | east | [9, 15] | 1 delivery van | SCENE-SLOTS.md trades: bay 1 is the fishmonger (x 9 to 15); 2-VEHICLES.md: one delivery van outside the fishmonger or grocer |
| grocer_apron | east | [33, 39] | 1 delivery van | SCENE-SLOTS.md: bay 5 grocer (x 33 to 39) |
| chandler_apron | east | [40, 46] | the ship's chandler's loading | SCENE-SLOTS.md: east_chandler, a ship's chandler (x 40 to 46) |
| yard_entrance | west | [21, 24] | the only junction mouth; dropped kerb centre x 22.5 m, crossover 3.0 m; bollards at x [20.7, 24.3] | vignette-scene.json street.dropped_kerb, held_props |
| gully | east | 12.0 | grate 0.4 m square, x 12.0 | vignette-scene.json street.gully (in front of the fishmonger) |
| empty_unit | east | [21, 27] | whitewashed, to let | SCENE-SLOTS.md: bay 3, an empty unit to let, whitewashed |
| west_blind_gable | west | [20, 21] | blind gable beside the yard | vignette-scene.json: west_south ends at x 21 beside the yard entrance |

**Standing places.** The street has double yellow lines along both kerbs (vignette-scene.json paint.double_yellow: two 100 mm bands 100 mm apart, 0.25 m from the kerb face), so nothing stands legally. Vehicles stand at the rank, at the loading aprons and, illegally, in private places of 5.5 to 6 m each (2-VEHICLES.md: 6 to 9 vehicles in the hook view: 1 to 2 on the rank, 4 to 6 private cars, 1 delivery van). Oil and blots belong at these places only; never in the yard entrance. Declared places: rank (east, x [3, 9], [1, 2] vehicles); fishmonger loading (east, x [9, 15], [0, 1] vehicles); private east (east, x [15, 33], [2, 4] vehicles); grocer loading (east, x [33, 39], [0, 1] vehicles); chandler loading (east, x [40, 46], [0, 1] vehicles); private west south (west, x [3, 21], [1, 2] vehicles); private west north (west, x [24, 42], [1, 1] vehicles). Excluded: the yard entrance (x 21 to 24), the gully (x 12 +/- 1.0) and the pillar box (x 27, east footway). **Bus stop:** vignette-scene.json not_emitted_from_this_file: E17_bus_shelter is not emitted; the street has no bus stop. Zero gum and zero litter tier 'bus stop' until one is placed.

**Words that became numbers:** door and downpipe splash: within 0.6 m of a door or downpipe: wall_foot_splash height x 1.2 and strength x 1.15 (capped at 1); weeds: gutter_grime: 0.05 to 0.15 m across, 1 per 6 to 10 m of kerb in the open stretches; salt: weight 1.0 within 12 m of the quay end, 0.4 elsewhere; kerb scuff and gully piles: gutter_grime geometry: scuff +8 L*, 0.05 to 0.12 m up the face, 0.3 to 1.5 m long, 1 per 10 m; pile 0.4 m radius, mask 0.8, colour 70/62/52, at the gully (x 12) and one per 20 m.

**Placement checks** (target.json `placement_checks`; `check_placement()` in self_check.py runs them on a list of placed decals, and part F runs them on a conforming street and on deliberately wrong ones):

- **P1, streak decals hang from their feature:** decal origin within 0.03 m (vertically) of the sill's or feature's lower edge and within its width; roll 0 +/- 3 degrees (review 8 October, fault 4g).
- **P2, L0 bands start at the pavement line:** band origin at the pavement line (the kerb foot for gutter_grime) within 0.02 m (review 8 October, fault 4g).
- **P3, oil lies under a standing car:** band centre 0.9 to 1.6 m from the kerb; long axis within 10 degrees of the kerb's (review 8 October, fault 4g; M04).
- **P4, gum only where feet go:** none on the carriageway and none within 0.4 m of a wall (review 8 October, fault 4g).
- **P5, no variant dominates the frame:** no variant over 40 % of a kind's visible decals (review 8 October, fault 4g).
- **P6, no repeated variant and seed along a wall:** no two placements of one kind with the same variant and seed within 6 m along one wall (review 8 October, fault 4g).
- **P7, tiles are out of phase:** tiled L0 kinds' x phase differs by at least 0.1 m (modulo the tile) on neighbouring houses of one side (review 8 October, fault 4g).
- **P8, oil and blots only at standing places:** x inside a declared standing place (places.standing_places); never in the yard entrance (review 8 October, fault 10).
- **P9, no gum or ends at a bus stop:** zero at a bus stop (there is none) (review 8 October, fault 10).

**Era rules (1990, Britain, an old port quarter):**

- Heavy: 1990 walls were sootier and 1990 pavements dirtier than any modern panorama measured (the 2019 London photographs are the cleanest end of the range, though their brick does show soot, M21). Where a photograph and the Hook sheet disagree, the sheet governs the mood of wall feet and heads (a WET street: converted to dry, section 4) and the photographs govern what the sheet does not show (streaks, M23) and the ground.
- Nothing later than 1990, or unusual in an old quarter then (Judgement on each): no tactile or blister paving, red or green anti-skid surfacing, thermoplastic bus lanes, pressure-washed stripes, bike-lane green, spray utility markings, cycle stands, wheelie-bin lines, vape and mask litter, QR-code stickers, anti-bird spikes, uPVC white fronts.
- No American marks: no wide white parking T-markings, no painted crosswalk zebras in white 12-inch bars, no manhole lids with US castings, no fire-hydrant paint, no yellow centre-line pairs, no graffiti throw-ups in bubble-letter style (the street's graffiti are the canon's five tags, in another family).
- No alcohol or gambling traces: no bottles, cans, bar-mats, betting slips or scratch cards in the litter (canon content rule). Tobacco ends are allowed.

**Content rule (canon):** no alcohol or gambling traces (no bottles, cans, tops, bar mats, betting slips or scratch cards in any litter or poster remnant); tobacco is allowed; nothing that implies a minor anywhere (no marks, litter or objects of that kind); no cypher, crown or makers' marks. 'LITTER' is fine on a bin; this family writes no words.

## 5. The kinds

| id | layer | decal frame (m) | density | px/m (min / use) | variants |
|---|---|---|---|---|---|
| `streak_sill` | L1 rule-placed wall decal | 1.6 x 1.7 | 0.15 to 0.6 share of sills that carry a set (typical 0.35) | 600 / 800 | 6 |
| `streak_coping` | L1 rule-placed wall decal | 6.0 x 3.0 | 0.3 to 1.0 fingers per metre of feature length (typical 0.6) | 250 / 300 | 5 |
| `wall_foot_splash` | L0 in the material | 2.0 x 0.75 | 1.0 to 1.0 full length of every pavement-side wall (typical 1.0) | 320 / 400 | 5 |
| `wall_foot_damp` | L0 in the material | 2.0 x 1.6 | 0.3 to 0.8 share of wall length (typical 0.5) | 120 / 200 | 4 |
| `salt_bloom` | L1 rule-placed wall decal | 2.0 x 0.9 | 1.0 to 3.0 patches per metre of foot length (typical 2.0) | 300 / 400 | 4 |
| `rust_bleed` | L1 rule-placed wall decal | 0.3 x 1.1 | 0.5 to 1.0 per iron fixing (typical 0.85) | 1000 / 1120 | 5 |
| `algae_downpipe` | L1 rule-placed wall decal | 0.9 x 1.4 | 0.8 to 1.0 per downpipe foot (typical 1.0) | 400 / 600 | 5 |
| `paint_flake` | L1 stamp decal on timber and render; part of L0 on stallrisers | 1.0 x 1.0 | 0.03 to 0.1 share of painted surface lost (typical 0.063) | 800 / 1000 | 6 |
| `paint_fade` | L0 in the material | 2.0 x 2.0 | 0.3 to 1.0 whole painted area (typical 0.6) | 20 / 40 | 3 |
| `render_crack` | L1 rule-placed wall decal | 1.8 x 1.8 | 3.0 to 6.0 metres of crack per m2 of rendered wall (map-cracked patches only) (typical 4.5) | 1000 / 1120 | 6 |
| `render_patch` | L1 stamp decal | 0.7 x 0.8 | 0.5 to 3.0 patches per 10 m of facade (typical 1.5) | 400 / 600 | 6 |
| `poster_remnant` | L1 stamp decal | 1.1 x 0.9 | 0 to 2 sites per facade (typical 1) | 300 / 400 | 5 |
| `bird_dropping` | L1 stamp decal | 0.4 x 0.55 | 0.2 to 1.2 per metre of ledge (typical 0.6) | 600 / 800 | 4 |
| `gum` | L2 ground | 2.0 x 2.0 | 0.5 to 8.0 per m2 of footway (typical 2.5) | 500 / 700 | 8 |
| `cig_end` | L2 ground | 2.0 x 2.0 | 3 to 6 per metre of kerb (band) and per m2 (aprons, open) (typical 4.4) | 750 / 1000 | 10 |
| `pavement_stain` | L2 ground | 1.0 x 1.0 | 3 to 10 blots per 10 m2 of footway (typical 6) | 250 / 400 | 6 |
| `flag_patch_crack` | L2 ground | 3.0 x 2.4 | 0.3 to 0.5 share of flags (typical 0.45) | 800 / 1120 | 6 |
| `road_oil` | L2 ground | 2.6 x 0.6 | 0.5 to 1.0 speckle bands per standing place (typical 0.8) | 600 / 1000 | 5 |
| `road_blot` | L2 ground | 1.2 x 1.2 | 1 to 3 dark blots per standing place (typical 2) | 250 / 400 | 5 |
| `tyre_scuff` | L2 ground | 3.0 x 1.0 | 1 to 2 scuffs per junction mouth (typical 1.5) | 100 / 150 | 4 |
| `road_patch` | L2 ground | 1.8 x 1.8 | 1 to 3 per 48 m street (typical 2) | 250 / 400 | 5 |
| `road_crack` | L2 ground | 3.0 x 3.0 | 2 to 5 stamps per 48 m street (typical 3) | 800 / 1120 | 5 |
| `gutter_grime` | L2 ground | 2.0 x 0.75 | 1.0 to 1.0 continuous along the kerb (typical 1.0) | 300 / 500 | 4 |
| `wall_soot` | L0 in the brick and render materials: one seamless tile per house, strength by the house's state; replaces the recipe's patch noise and the house look's brightness | 4.0 x 4.0 | 0.3 to 0.6 share of houses in the sooted state (typical 0.54) | 12 / 25 | 4 |
| `wall_head_band` | L0 in the brick and render materials, hung from each feature's lower edge by the distance below it | 2.0 x 1.5 | 1.0 to 1.0 share of each eaves, verge, coping and string-course length (typical 1.0) | 100 / 160 | 4 |
| `iron_wear` | L0 in the iron material | 0.08 x 2.4 | 0.04 to 0.08 share of the pipe's area lost to paint (typical 0.06) | 300 / 400 | 4 |
| `grate_wear` | L0 in the grate's iron material | 0.4 x 0.4 | 1.0 to 1.0 per grate (typical 1.0) | 800 / 1000 | 3 |
| `line_wear` | L2 ground | 3.0 x 0.075 | 0.1 to 0.3 share of the line lost (typical 0.18) | 800 / 1120 | 6 |
| `sign_ghost` | L1 rule-placed wall decal | 2.2 x 1.0 | 0.0 to 1.0 ghosts per facade (typical 0.5) | 600 / 800 | 4 |
| `graffiti_buff` | L1 rule-placed wall decal | 1.6 x 1.3 | 0.0 to 1.0 patches per 20 m of facade (typical 0.4) | 300 / 400 | 4 |
| `handle_wear` | L1 stamp decal on doors | 0.6 x 0.6 | 0.8 to 1.0 per handle, plate or push zone (typical 0.9) | 120 / 200 | 4 |
| `stone_top_lichen` | L1 stamp decal on the top face | 1.0 x 0.2 | 0.4 to 0.8 share of the sill or coping top covered (typical 0.6) | 600 / 800 | 4 |
| `footway_infill` | L2 ground | 0.8 x 3.2 | 1 to 3 infills per 48 m of footway (typical 2) | 800 / 1120 | 6 |

### `streak_sill`: Rain streaks under window sills

- **Layer:** L1 rule-placed wall decal (projected, normal-faded)
- **Where (the rule):** Origin on the sill's lower edge. A set holds two end streaks under the sill's two ends, which differ in length (longer over shorter 1.15 to 2.5) and in width (wider over narrower at least 1.1); 3 to 7 thin rivulets from brackets, joints and chips along the sill; and a faint wash. One set in 8 has a long end streak of 0.8 to 1.4 m (a sill with a broken drip). Everything runs straight down, tilted at most 3 degrees. Never rotate a streak. The continuous darkening under a gutter, verge or coping is wall_head_band, not this kind.
  - Feature: the lower edge of a window sill, upper floors and shop transom ledges alike; a set under 15 to 60 % of sills (typical 35 %), never under every sill
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0 to 0.6 below the sill's lower edge (0.8 to 1.4 for a long end streak); stop at the next ledge, string course or door head if nearer
  - Sides: East parade fronts face west, the wet side of a British port: weight 1.0. West block fronts face east: weight 0.7. Gable ends facing the street: 0.8.
  - Footfall and wet: Not footfall. Wet climate: always present; darker and glossier when wet; the lower half dries first.
  - Density: 0.15 to 0.6 share of sills that carry a set (typical 0.35) [Photo M23: of about 30 sill and ledge edges counted by eye in five views of urban_street_03, one carries a clear streak (M17); a column test on 13 edges finds one darker than 0.90 under 2 and none darker than 0.85 (3 to 15 %). That street is maintained 2019 brick, the cleanest end of the range (S2), so the target raises it for an uncleaned 1990 street and Jafar's 'not faint marks' of 2 October: Judgement. The reviewer's 50 to 70 % is not measured anywhere and is kept as the upper bound (D6)]
  - With house wear: share of sills with a set x wear; strength x wear; length x (0.8 + 0.2 x wear)
- **Decal frame:** x -0.8 to 0.8 m, y -1.7 to 0.0 m; origin: origin = the middle of the sill's lower edge; y is up, so runs fall to negative y; decal is yaw-faced to the wall, not rotated
- **Shape and size (real units):** envelope primitive `streak_set`; envelope parameters `{"sill_width_m": [0.9, 1.2], "end_streaks": {"n": 2, "width_frac_of_sill": [0.05, 0.1], "length_m": [0.15, 0.6], "min_length_ratio": 1.3, "min_width_ratio": 1.4, "long_end": {"prob": 0.125, "length_m": [0.8, 1.4]}, "src": "Photo M17 (0.10 m wide, 0.30 to 0.45 m long) and M16 (0.09 to 0.45 m); the long end is Judgement (1 sill in 8)"}, "rivulets": {"n": [3, 7], "width_m": [0.01, 0.03], "length_m": [0.14, 0.4], "src": "Photo M16 (10.6 to 19.7 mm wide, 8 per metre of joint, 0.09 to 0.45 m long)"}, "wash": {"height_m": [0.1, 0.3], "overhang_m": 0.1, "level": 0.18, "src": "Judgement"}, "wander_m": [0.005, 0.03], "taper": 0.55, "fade_exponent": 1.4, "core_level": 0.9, "head_fraction_full": 0.12, "length_note": "every length_m here is the VISIBLE length (the part of a run at or above mask 0.25, as a photograph shows it); the drawn run continues, fading, to about 1.7 times as far"}`
  - Geometry numbers: `{"streak_width_to_sill_width": {"end": [0.05, 0.1], "rivulet": [0.01, 0.03], "src": "Photo M17 (0.10 m on a sill about 1.2 m wide) and M16; Judgement"}, "streak_length_m": {"p10": 0.15, "p50": 0.35, "p90": 0.6, "src": "Photo M16 (rivulets 0.09 to 0.45 m) and M17 (0.30 to 0.45 m); the long end streak (0.8 to 1.4 m, 1 sill in 8) is Judgement and lies outside p90"}, "aspect_length_to_width": [3, 30], "edge_10_90_mm": [12, 40], "edge_src": "Photo M13 15.6 mm, M12 19 mm (soft-edged stains)", "darkest_at": "the head, directly under the sill; the mask falls as exp(-(t/L)^1.4) down the run (never darkest at the bottom: the 4 October review failed that)", "branching": "a rivulet may split once in its lower half with a 12 to 25 degree fork, one in four streaks", "asymmetry": "the two end streaks differ in length and width: no symmetric pairs (checks end_streak_length_ratio and end_streak_width_ratio)", "edge_for_envelope_mm": 20}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [112, 76, 66] | dirty darker brown | 0.7 | -7 | Judgement, nudged darker than Photo M17 (darkest bricks 0.80 to 0.90, column 0.97) because 1990 brick was sootier and Jafar asked for 'not faint marks' (2 October); length follows the photographs (D6) |
  | brick_painted | [152, 108, 93] | [118, 100, 89] | grey-brown dirt | 0.75 | -6 | Judgement, as brick_red |
  | render_cream | [214, 200, 178] | [195, 170, 142] | grey-brown dirt | 0.72 | -10 | Judgement; Photo M12 stained cream is 144/124/97 against 222/205/182 clean (x0.45 on Y) after damp, not rain run-off |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.3, "note": "wet film darkens the run by about a fifth and makes it glossier than the dry wall around it"}`. [Read: WET-ROAD-2026-10-08.md (wet stone x0.68 albedo, roughness 0.45); Judgement for walls. The tone multipliers are dry values (Photo M16, M17 are dry photographs)]
- **Texel scale:** smallest feature 10 mm; mask needs at least 600 px/m, use 800; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: mask 1.6 m x 1.7 m at 800 px/m is 1280 x 1360; at 10 m the fine rivulets are 2 screen pixels so keep them at 0.15 to 0.4 strength
- **Variants:** 6 seeded masks; they differ by 3 end-streak width pairs x 2 rivulet layouts (3 or 6 rivulets); one variant in 8 carries a long end streak; mirror in x allowed; no rotation; strength, length and tint from the house seed [Derived: asset plan note 4 asks 4 to 6 masks a kind]
- **Why 1990 Britain:** Rain streaks are weather, not fashion; what dates a street is how heavy they are: uncleaned brick and render, no drip-tray flashings or plastic sills on this old-quarter parade (Judgement; no 1990 photograph reached). Length and density follow the 2019 photographs, which are the cleanest end of the range; only the darkness is raised.
- **Not modern, not American:** No clean white rendered strips beneath dark streaks, no neat symmetrical streak pairs of equal length, no uniform streaks across the whole sill width, no streak under every sill.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | streak_aspect_p50 | streak_aspect | mask | `{"thr": 0.25, "min_length_m": 0.1, "stat": "p50"}` | 3 | 30 | Judgement |
  | streak_width_mm_p50 | streak_width_mm | mask | `{"thr": 0.25, "stat": "p50"}` | 10 | 140 | Photo M16/M17 |
  | streak_length_m_p90 | streak_length_m | mask | `{"thr": 0.25, "stat": "p90"}` | 0.3 | 0.9 | Photo M16/M17 (reviewer's range): the end streaks, with one long end in 8 |
  | streak_length_m_p50 | streak_length_m | mask | `{"thr": 0.25, "stat": "p50"}` | 0.12 | 0.45 | Photo M16: rivulets 0.09 to 0.45 m; M17 0.30 to 0.45 m |
  | vertical_within_deg | verticality_deg | mask | `{"thr": 0.25, "min_length_m": 0.2}` | 0 | 12 | Derived: gravity (placed tilted at most 3 degrees; a streak's own wander adds the rest; forks, which leave at 12 to 25 degrees, are shorter than 0.2 m) |
  | fade_ratio_tail_over_head | fade_ratio | mask | `{"thr": 0.25}` | 0.0 | 0.6 | Derived: darkest at the head |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.3, "band_hi": 0.9, "axis": "x"}` | 12 | 45 | Photo M12, M13 |
  | coverage_of_decal_at_0.25 | coverage | mask | `{"thr": 0.25}` | 0.01 | 0.1 | Derived: 2 end streaks 0.08 m x 0.15 to 0.6 m + rivulets over the 1.6 x 1.7 m frame |
  | peak_mask | mask_max | mask | `{}` | 0.8 | 1.0 | Judgement |
  | end_streak_length_ratio | end_streak_length_ratio | mask | `{"thr": 0.25, "head_m": 0.2}` | 1.15 | 2.5 | Judgement (reviewer 8 October): no symmetric pairs |
  | end_streak_width_ratio | end_streak_width_ratio | mask | `{"thr": 0.25, "head_m": 0.2}` | 1.1 | 3.0 | Judgement (reviewer 8 October): no symmetric pairs |
  | rivulet_count | rivulet_count | mask | `{"thr": 0.25, "head_m": 0.2, "min_length_m": 0.1}` | 3 | 7 | Photo M16 (8 per metre of joint, thinned to a sill); reviewer's 3 to 7 |

### `streak_coping`: Fingers under leaking joints in copings, ledges, string courses and gutters

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** One finger per leaking joint, with 1 joint in 3 or 4 leaking (coping joints every 0.6 to 0.9 m, so 0.3 to 1.0 fingers per metre of feature). Fingers differ in length (lognormal 0.25 / 0.55 / 1.4 m) and spacing (spacing CV 0.25 to 0.8). Full-height runs of 1.5 to 3.0 m only under leaking gutter joints and hopper heads, 0 to 2 per house. The continuous darkening under eaves, verges and copings is wall_head_band (the head, Sheet M22 and Photo M21), not fingers. Straight down, no rotation.
  - Feature: under a leaking coping joint, a leaking eaves-gutter joint or stop-end, a hopper head, a chimney-stack coping: the places where water leaves the feature in one line
  - Surfaces: brick_red, brick_painted, render_cream, stone_sill
  - Height: 0 to 1.4 below the feature, 1.5 to 3.0 for a full-height run under a leaking gutter joint or hopper head; stop at the next opening
  - Sides: East parade (west-facing): 1.0; west block: 0.7; gables: 0.9
  - Footfall and wet: Wet climate only; the fingers sit on top of the head band (Jafar, 2 October: 'not faint marks')
  - Density: 0.3 to 1.0 fingers per metre of feature length (typical 0.6) [Derived: joints every 0.6 to 0.9 m (1.1 to 1.7 per metre), 1 in 3 or 4 leaking; Photo M16 gives 8 detected rivulets per metre of one concrete joint, which is not a coping]
- **Decal frame:** x -3.0 to 3.0 m, y -3.0 to 0.0 m; origin: origin = the middle of the stamp on the feature's lower edge (a 6.0 m run of feature); runs fall to negative y; stamp where the joints leak
- **Shape and size (real units):** envelope primitive `streak_set`; envelope parameters `{"span_m": [4.0, 6.0], "fingers": {"n_range": [3, 6], "width_m": [0.04, 0.16], "length_m_lognormal": [0.25, 0.55, 1.4], "spacing_cv": 0.5, "full_height": {"prob_per_stamp": 0.25, "length_m": [1.5, 3.0]}, "src": "Photo M21 (the coping band 0.4 m deep) and M16 (rivulets 0.09 to 0.45 m); the long runs are Judgement"}, "wash": {"height_m": [0.1, 0.25], "overhang_m": 0.0, "level": 0.18}, "wander_m": [0.004, 0.015], "taper": 0.6, "fade_exponent": 1.2, "core_level": 0.85, "head_fraction_full": 0.18, "length_note": "every length_m here is the VISIBLE length (the part of a run at or above mask 0.25); the drawn run continues, fading, to about 1.8 times as far"}`
  - Geometry numbers: `{"streak_length_m": {"p10": 0.25, "p50": 0.55, "p90": 1.4, "src": "Photo M21 (coping band 0.4 m), M16/M17 (0.09 to 0.45 m); Judgement above 1 m. The first pass cited the Hook sheet's 'gable streaks run 1 to 3 m': the sheet shows no streaks (D2, D6)"}, "streak_width_m": {"p10": 0.04, "p50": 0.09, "p90": 0.16, "src": "Photo M17 (0.10 m); Judgement"}, "aspect_length_to_width": [3.0, 40], "edge_10_90_mm": [25, 70], "edge_src": "Judgement: wider streaks have softer edges (Photo M13: 15.6 mm for 24 mm wide streaks; scaled)", "darkest_at": "the head; coverage between fingers is the faint wash only", "irregularity": "spacing CV 0.25 to 0.8 at the head row and length CV at least 0.25: no identical fingers at identical spacing", "edge_for_envelope_mm": 40}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [111, 76, 66] | dirty darker brown | 0.7 | -7 | Judgement (as streak_sill): fingers sit on the head band, which supplies the heavy part |
  | brick_painted | [152, 108, 93] | [118, 100, 89] | grey-brown dirt | 0.75 | -6 | Judgement |
  | render_cream | [214, 200, 178] | [195, 170, 141] | grey-brown dirt | 0.72 | -10 | Judgement; Photo M12 |
  | stone_sill | [170, 166, 158] | [146, 141, 131] | soot grey | 0.7 | -9 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.3}`. [Read: WET-ROAD-2026-10-08.md; Judgement]
- **Texel scale:** smallest feature 40 mm; mask needs at least 250 px/m, use 300; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 5 seeded masks; they differ by finger count (3, 4, 6), joint rhythm, one with a heavy stop-end blotch, one with a full-height hopper run; mirror allowed; stamp along the feature at the leaking joints (not seamless) [Derived]
- **Why 1990 Britain:** Cast-iron and asbestos-cement gutters leaked at their joints, which is why the fingers hang from joints; a PVC replacement run may sit among them (Judgement: no 1990 photograph reached).
- **Not modern, not American:** No identical fingers at identical spacing; no stained zone ending in a ruler-straight horizontal line (the head band's lower edge steps by brick courses).
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | streak_aspect_p50 | streak_aspect | mask | `{"thr": 0.25, "min_length_m": 0.2, "stat": "p50"}` | 3.0 | 40 | Judgement |
  | streak_length_m_p50 | streak_length_m | mask | `{"thr": 0.25, "stat": "p50"}` | 0.25 | 1.2 | Photo M21/M16, Judgement |
  | vertical_within_deg | verticality_deg | mask | `{"thr": 0.25}` | 0 | 10 | Derived: gravity (the decal is placed tilted at most 3 degrees; a finger's own wander adds up to 7) |
  | fade_ratio_tail_over_head | fade_ratio | mask | `{"thr": 0.25}` | 0.0 | 0.6 | Derived |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.3, "band_hi": 0.9, "axis": "x"}` | 20 | 80 | Judgement |
  | coverage_of_decal_at_0.25 | coverage | mask | `{"thr": 0.25}` | 0.005 | 0.12 | Derived: 3 to 6 fingers 0.04 to 0.16 m x 0.25 to 1.4 m over the 6.0 x 3.0 m frame |
  | finger_spacing_cv | finger_spacing_cv | mask | `{"thr": 0.25, "head_row_m": 0.12}` | 0.25 | 0.8 | Judgement (reviewer 8 October): no identical fingers at identical spacing |
  | finger_length_cv | finger_length_cv | mask | `{"thr": 0.25, "head_m": 0.2}` | 0.25 | 1.5 | Judgement (reviewer 8 October) |

### `wall_foot_splash`: Pavement splash and grime band on walls, stallrisers and door bottoms

- **Layer:** L0 in the material (height gradient) plus L1 decal for the ragged top edge
- **Where (the rule):** A band from the pavement upward. Full strength from 0 to 0.24 m, 0.85 at 0.33 m, 0.45 at 0.49 m, 0.15 at 0.61 m, gone by 0.75 m; the top edge is ragged and steps in brick-course heights (75 mm) on brick, in small blotches on painted timber. Within 0.6 m of a door or a downpipe the band is 1.2 x higher and 1.15 x stronger (strength capped at 1). It REPLACES the foot rise of the recipe's wear layer (section 1) and is multiplied after wall_soot and wall_foot_damp (section 4).
  - Feature: the foot of every wall that meets the pavement: brick walls, stallrisers, pilaster plinths, door leaves' bottom rails, door steps
  - Surfaces: brick_red, brick_painted, render_cream, timber_paint_dark, timber_paint_light, stone_sill, tile_glazed
  - Height: 0 to 0.75 above the pavement (the Hook sheet gable: black to 0.33 m, half gone at 0.49 m); x 1.2 within 0.6 m of a door or downpipe
  - Sides: Both sides; heavier on the east parade where the pavement is wetter (north-facing step shadow not modelled)
  - Footfall and wet: Footfall and wet: strongest at shop doors and the quay-end corner where people stand; splash is wet-pavement spatter from boots and rain bounce.
  - Density: 1.0 to 1.0 full length of every pavement-side wall (typical 1.0) [Derived: it is continuous]
  - With house wear: height x (0.8 + 0.2 x wear); strength x wear; x 1.2 height and x 1.15 strength (capped at 1) within 0.6 m of a door or downpipe
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 0.75 m; origin: origin = pavement line at the left end of a 2.0 m tile; y up the wall; tiles in x
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.24, "level": 1.0}, {"h_m": 0.33, "level": 0.85}, {"h_m": 0.49, "level": 0.45}, {"h_m": 0.61, "level": 0.15}, {"h_m": 0.75, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.04, 0.12], "wavelength_m": [0.15, 0.6], "src": "Sheet M18: ragged top stepping by brick courses"}, "fingers": {"n_per_m": 3, "length_m": [0.05, 0.25], "width_m": [0.02, 0.08]}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.24, 0.33, 0.49, 0.61, 0.75], "mask": [1.0, 1.0, 0.85, 0.45, 0.15, 0.0], "src": "Sheet M18 (wet): luminance ratio 0.12 to 0.19 below 0.24 m, 0.30 at 0.33 m, 0.57 at 0.49 m, 0.85 at 0.61 m, 0.95 above 0.8 m, inverted through the sheet's wet 0.20 (0.27 dry x 0.75 wet); the row 'plaster_brick_01' tagged 'sewer, tunnel, trimsheet' (M15) is not evidence for the profile"}, "profile_tolerance": 0.15, "edge_10_90_mm": [200, 450], "edge_src": "the whole fall-off, Sheet M18: 1.0 at 0.24 m to 0.15 at 0.61 m; inside it the ragged top steps by one 75 mm course (Sheet M18)", "ragged_step_mm": [30, 120], "tileable": "horizontally, seamless, 2.0 m period; vertical profile fixed", "top_edge_std_mm": {"range": [15, 60], "level": 0.5, "src": "Judgement (reviewer 8 October): ragged, never a straight line"}, "edge_for_envelope_mm": 40}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [60, 50, 44] | soot black-brown | 0.27 | -21 | Sheet M18: the sheet is a WET street (RULINGS 3 October), so its foot ratio 0.12 to 0.30 (mid 0.20) is the wet value; dry = 0.20 / 0.75 (the wet multiplier below) = 0.27; Judgement for the choice of the middle (photographs show none on the maintained estate brick, M17) |
  | brick_painted | [152, 108, 93] | [87, 74, 63] | dirty brown | 0.4 | -17 | Judgement |
  | render_cream | [214, 200, 178] | [152, 129, 107] | dirty brown | 0.4 | -26 | Judgement (the first pass cited the plaster_brick_01 gradient, which is a trim-sheet waterline, M15) |
  | timber_paint_dark | [52, 64, 88] | [42, 47, 59] | grimed dark | 0.55 | -8 | Judgement; Fresh Fish review: foot 8 L* below top (PAINTED-FRONTS-2026-10-07.md) |
  | timber_paint_light | [222, 218, 206] | [162, 151, 133] | dirty grey-brown | 0.45 | -24 | Judgement |
  | stone_sill | [170, 166, 158] | [121, 115, 106] | soot grey | 0.45 | -20 | Judgement |
  | tile_glazed | [172, 166, 150] | [137, 132, 116] | grimed tile with dark joints | 0.6 | -13 | Judgement (narrow note of the review): glazed tile does not stain like brick, grime sits in the joints; the shopfront family's own tile values win |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.75, "roughness_delta": -0.35, "note": "splash band glints when wet; the Hook sheet's foot reads black and slightly shiny. Dry multiplier x 0.75 = the sheet's 0.20"}`. [Sheet (wet); Read WET-ROAD]
- **Texel scale:** smallest feature 25 mm; mask needs at least 320 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: tile 2.0 m x 0.75 m at 400 px/m = 800 x 300
- **Variants:** 5 seeded masks; they differ by top-edge noise seed, finger count, two with a door-step notch; tile horizontally [Derived]
- **Why 1990 Britain:** Splash and soot at wall feet were normal on uncleaned brick: traffic grime and the soot of the coal era. A pristine foot is the modern giveaway (Judgement; the Hook sheet is the evidence: its gable foot is black to 0.33 m).
- **Not modern, not American:** No clean wall foot beside a dark pavement; no uniform gradient ending in a straight line.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | foot_profile | foot_profile | mask | `{"points": [[0.05, 0.85, 1.0], [0.2, 0.85, 1.0], [0.33, 0.6, 1.0], [0.49, 0.25, 0.65], [0.61, 0.03, 0.35], [0.78, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Sheet M18 |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 500}` | 200 | 450 | Sheet M18: 1.0 at 0.24 m falling to 0.15 at 0.61 m (the whole fall-off); the ragged step inside it is 75 mm |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived |
  | top_edge_std_mm | top_edge_std_mm | mask | `{"thr": 0.5, "source": "bottom"}` | 15 | 60 | Judgement (reviewer 8 October): the top edge crosses 0.5 at heights that vary along x |
  | column_mean_cv | column_mean_cv | mask | `{"source": "bottom", "from_m": 0.3, "to_m": 0.78}` | 0.08 | 1.0 | Judgement (reviewer 8 October): not a uniform band |
  | composed_foot_ratio | composed_foot_ratio | composition | `{"state": "cleaned", "height_m": 0.1}` | 0.12 | 0.3 | Sheet M18 (the darkest foot 0.12 to 0.30 of the wall; review 8 October): splash, damp, algae and the floor on a cleaned house at house wear 1.0, 0.1 m up beside a downpipe |
  | composed_wall_min_ratio | composed_wall_min_ratio | composition | `{"state": "sooted"}` | 0.149 | 1.0 | the wall floor 0.15 (compose block): a sooted foot beside a downpipe never goes below it |

### `wall_foot_damp`: Soot and damp at wall feet: rising damp, tide-line and algae gradient

- **Layer:** L0 in the material (soft, broad) plus L1 decal on masonry
- **Where (the rule):** Where a wall is damp (3 walls in 10 to 8 in 10): a broad, soft, mottled darkening from 0.3 m to 1.2 m with a damp 'tide line' at 0.8 to 1.2 m and a green tint in the lowest 0.45 m on render. It is multiplied BEFORE wall_foot_splash (section 4), so the foot is damp x splash, and only above 0.75 m is it alone. Plus black soot streaks 0.3 to 1.0 m long running up from the foot beside downpipes.
  - Feature: brick and rendered walls standing directly on the pavement without a damp-proof plinth; heaviest on the quay-end and the shaded gables
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0.15 to 1.2 above the pavement; strongest 0.3 to 0.9
  - Sides: West block (faces east, drier but sooted): 1.0; east parade: 0.9; gable ends facing the street (shaded): 1.1
  - Footfall and wet: Wet climate; port town (tide-borne salts, see salt_bloom). Not footfall.
  - Density: 0.3 to 0.8 share of wall length (typical 0.5) [Judgement: share of wall length with an active damp band (the Hook sheet's left gable shows none above 0.8 m); BRE DG 245 (search summary only) places rising damp 0.5 to 1.5 m, more than 1 m on unprotected masonry]
  - With house wear: height x wear; strength x wear
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 1.6 m; origin: origin = pavement line; y up the wall; tiles in x
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.3, "level": 0.8}, {"h_m": 0.8, "level": 0.5}, {"h_m": 1.2, "level": 0.15}, {"h_m": 1.5, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.1, 0.3], "wavelength_m": [0.3, 1.2]}, "fingers": {"n_per_m": 1.5, "length_m": [0.15, 0.5], "width_m": [0.04, 0.15]}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.3, 0.8, 1.2, 1.5], "mask": [0.8, 0.8, 0.5, 0.15, 0.0], "src": "Judgement bounded by the search lead BRE DG 245 (0.5 to 1.5 m); plaster_brick_01's green band (M15, a trim-sheet waterline) is not evidence for it"}, "profile_tolerance": 0.2, "edge_10_90_mm": [700, 1500], "edge_src": "the whole fall-off, 0.8 at 0.3 m to 0.15 at 1.2 m; Judgement (the plaster_brick_01 gradient length is a trim-sheet waterline, M15, and is not used)", "mottle": "low-frequency noise at 0.3 to 0.6 m wavelength, amplitude +/- 0.2 of the mask", "tileable": "horizontally, 2.0 m period", "top_edge_std_mm": {"range": [40, 150], "level": 0.3, "src": "Judgement (reviewer 8 October)"}, "edge_for_envelope_mm": 150}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [89, 67, 57] | damp brown | 0.5 | -12 | Judgement; Sheet M18 grey salt band sits just above |
  | brick_painted | [152, 108, 93] | [105, 92, 78] | damp grey-brown | 0.62 | -10 | Judgement |
  | render_cream | [214, 200, 178] | [148, 142, 86] | damp olive-brown | 0.45 | -23 | Judgement, coloured from a waterline: plaster_brick_01 (M15) is tagged 'sewer, tunnel, trimsheet' by Poly Haven, so its green band is a waterline in a trim sheet, not a pavement wall foot |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.15}`. [Judgement]
- **Texel scale:** smallest feature 75 mm; mask needs at least 120 px/m, use 200; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by tide-line height and noise seed; tile horizontally [Derived]
- **Why 1990 Britain:** Rising damp and sooted feet were the normal condition of unrestored Victorian masonry (Judgement); a later damp-proof course stops the damp but does not clean the brick.
- **Not modern, not American:** No sharp horizontal tide line; no even gradient.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | foot_profile | foot_profile | mask | `{"points": [[0.15, 0.5, 1.0], [0.6, 0.3, 0.7], [1.2, 0.02, 0.35], [1.6, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Judgement |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 1200}` | 700 | 1500 | Judgement: 0.8 at 0.3 m falling to 0.15 at 1.2 m |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | top_edge_std_mm | top_edge_std_mm | mask | `{"thr": 0.3, "source": "bottom"}` | 40 | 150 | Judgement (reviewer 8 October) |
  | column_mean_cv | column_mean_cv | mask | `{"source": "bottom", "from_m": 0.6, "to_m": 1.5}` | 0.08 | 1.0 | Judgement (reviewer 8 October) |

### `salt_bloom`: Salt bloom (efflorescence) on brick, lime runs and white tide-marks

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** A pale band of whitened bricks sitting on the upper flank of the dark foot band: 2 to 3 brick courses (0.30 to 0.525 m, Sheet M18: 0.15 to 0.22 m at 0.26 to 0.46 m, desaturated), each brick whitened or not (35 to 75 % of the band's bricks), so the top is ragged by bricks; plus 0 to 2 lime runs per sill: thin pale lines 5 to 20 mm wide and 0.1 to 0.5 m long. It is laid AFTER every darkening mark (section 4), so the band stays pale.
  - Feature: low brickwork near the quay, the quay-end corner and the quay-facing gables; below leaking sills and copings as thin white lime runs
  - Surfaces: brick_red, brick_painted
  - Height: 0.30 to 0.525 above the pavement (band, three courses); runs 0 to 0.5 below their source
  - Sides: Quay end (x 0 to 15: within 12 m of the quay end at x 3) and the west block's quay gable: weight 1.0; elsewhere 0.4 (section 4, places)
  - Footfall and wet: A port-town (salt-laden air and tidal ground water) effect. Salt is fully visible dry; in drizzle and damp it keeps about 0.9 of its brightness (the Hook sheet, a wet street, still shows it as grey-white bricks, M18); only in heavy rain with water running down the wall does it fall to 0.6.
  - Density: 1.0 to 3.0 patches per metre of foot length (typical 2.0) [Sheet M18: whitened bricks fill 2 courses of the 7-course affected foot; Judgement]
  - With house wear: strength x wear
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 0.9 m; origin: origin = pavement line; the band starts at 0.25 m; follows brick bond offsets
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.27, "level": 0.0}, {"h_m": 0.31, "level": 0.7}, {"h_m": 0.52, "level": 0.7}, {"h_m": 0.58, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.03, 0.1], "wavelength_m": [0.2, 0.7]}, "brick_patches": {"brick_m": [0.215, 0.075], "fill_fraction": 0.55}, "fingers": {"n_per_m": 1.0, "length_m": [0.1, 0.5], "width_m": [0.005, 0.02]}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.27, 0.31, 0.52, 0.58], "mask": [0.0, 0.0, 0.7, 0.7, 0.0], "src": "Sheet M18 overlay (the grey-white bricks lie between 0.26 and 0.46 m above the foot, on the upper flank of the dark band, 2 to 3 courses, desaturated)"}, "profile_tolerance": 0.3, "edge_10_90_mm": [8, 60], "edge_src": "Sheet M18 patches follow brick edges (hard); fringe soft", "top_edge_std_mm": {"range": [20, 70], "level": 0.4, "src": "Judgement (reviewer 8 October)"}, "brick_cells": {"brick_m": [0.215, 0.075], "bond": "stretcher bond: each course offset by half a brick (0.1075 m); the first pass wrote 0.0375 m, which is half a course height, not a bond offset", "patch_cell_mean_above": 0.4, "share_of_band_cells": [0.35, 0.75], "internal_std_below": 0.15, "src": "Sheet M18: whitened bricks fill about half the band's bricks; Judgement (reviewer 8 October)"}, "edge_for_envelope_mm": 25}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [150, 138, 128] | dull grey-white | 1.0 | 16 | Sheet M18 band (107/91/83 bright quartile of a 81/60/52 mean on a 107/52/32 wall; the sheet is wet, the wet factor below is 0.9, so the dry colour is the same within the error); mark replaces, mixed at mask x 0.7 |
  | brick_painted | [152, 108, 93] | [190, 182, 170] | chalky white | 1.0 | 25 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.15, "note": "powdery, rougher than the brick"}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.1, "note": "drizzle and damp (the game's usual weather, RULINGS 5 October): the band stays pale, as the wet Hook sheet shows it (Sheet M18)", "heavy_rain_running_water": {"albedo_mult_on_tone": 0.6, "roughness_delta": -0.3, "note": "only with water running down the wall: salts dissolve and the patch goes dull"}}`. [Sheet M18 (wet street, band still grey-white); Judgement for the heavy-rain case]
- **Texel scale:** smallest feature 20 mm; mask needs at least 300 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by patch layout, run count; stamps that follow the brick bond (offset by half a brick, 0.1075 m, every course) [Derived]
- **Why 1990 Britain:** Efflorescence is as old as brick; on an uncleaned port-town wall re-pointed in hard cement mortar it shows more (Judgement; the Hook sheet shows it).
- **Not modern, not American:** Not white paint, not graffiti-buffing grey patches; salt follows bricks, not rectangles.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_decal_at_0.4 | coverage | mask | `{"thr": 0.4}` | 0.04 | 0.17 | Derived: three courses of 65 mm x 55 % brick fill over the 0.9 m frame (0.11 to 0.13) |
  | ragged_edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 200}` | 15 | 100 | Sheet M18 (patch top edge ragged 30 to 100 mm) |
  | peak_mask | mask_max | mask | `{}` | 0.5 | 0.85 | Judgement |
  | foot_profile | foot_profile | mask | `{"points": [[0.15, 0.0, 0.05], [0.38, 0.12, 0.75], [0.8, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Sheet M18 |
  | top_edge_std_mm | top_edge_std_mm | mask | `{"thr": 0.4, "source": "bottom"}` | 20 | 70 | Judgement (reviewer 8 October): salt follows bricks, not a ruler line |
  | column_mean_cv | column_mean_cv | mask | `{"source": "bottom", "from_m": 0.26, "to_m": 0.5}` | 0.08 | 2.0 | Judgement (reviewer 8 October) |
  | brick_patch_share | brick_patch_share | mask | `{"brick_w_m": 0.215, "brick_h_m": 0.075, "from_m": 0.3, "to_m": 0.45, "cell_mean_above": 0.4}` | 0.35 | 0.75 | Sheet M18 and the reviewer: 35 to 75 % of the band's brick cells whitened |
  | brick_cell_std | brick_cell_std | mask | `{"brick_w_m": 0.215, "brick_h_m": 0.075, "from_m": 0.3, "to_m": 0.45, "cell_mean_above": 0.4}` | 0.0 | 0.15 | Judgement (reviewer 8 October): a whitened brick is flat inside |
  | composed_salt_ratio | composed_salt_ratio | composition | `{"state": "cleaned"}` | 0.57 | 2.2 | Sheet M18: the whitened bricks read 0.57 to 0.75 of the wall and above it (review 8 October); laid after the darkening they stay pale; not above 2.2 (not white) |

### `rust_bleed`: Rust bleed from iron fixings

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** A small dense dot at the fixing (3 to 12 mm), a diffuse brown halo (0.04 to 0.10 m), and a trickle running straight down 0.15 to 0.8 m, 5 to 20 mm wide, occasionally splitting into 2 and with detached drops at the end.
  - Feature: every visible iron fixing: bracket, railing foot, bolt, nail head, shopfront bracket, gutter and downpipe bracket, hinge, letter-plate screw, safe-grille, ties
  - Surfaces: brick_red, brick_painted, render_cream, stone_sill, timber_paint_light
  - Height: 0 to 0.8 below the fixing
  - Sides: Both; heavier on the west-facing (wet) east parade: 1.0, west block 0.8
  - Footfall and wet: Wet; rust runs only after rain and shows strongest when the wall is just drying
  - Density: 0.5 to 1.0 per iron fixing (typical 0.85) [Judgement: most fixings on a 1990 wall are old enough to bleed; galvanised and stainless fixings are 2000s]
- **Decal frame:** x -0.15 to 0.15 m, y -1.0 to 0.1 m; origin: origin = the iron fixing; the trickle falls to negative y
- **Shape and size (real units):** envelope primitive `streak_set`; envelope parameters `{"fixing": {"dot_mm": [3, 12], "halo_m": [0.04, 0.1], "halo_level": 0.18}, "trickle": {"n": [1, 2], "width_m": [0.005, 0.02], "length_m": [0.15, 0.8], "src": "Photo M14: trickle >= 0.52 m long, 5 to 20 mm wide; drops 30 to 90 mm"}, "drops": {"n": [0, 3], "eqd_mm": [30, 90]}, "wander_m": [0.003, 0.02], "taper": 0.3, "fade_exponent": 0.9, "core_level": 1.0, "head_fraction_full": 0.2}`
  - Geometry numbers: `{"streak_width_mm": {"p10": 5, "p50": 10, "p90": 20, "src": "Photo M14"}, "streak_length_m": {"p10": 0.15, "p50": 0.35, "p90": 0.8, "src": "Photo M14 (>= 0.52), Judgement"}, "aspect_length_to_width": [10, 120], "edge_10_90_mm": [8, 25], "edge_src": "Photo M13 15.6 mm; M14 trickle edges", "edge_for_envelope_mm": 10}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [128, 62, 28] | orange-brown | 1.0 | -8 | Photo M14 rust (108/78/59 median, drops 140/60/30) made more saturated on a red wall; mixed at mask x 0.7 |
  | brick_painted | [152, 108, 93] | [140, 72, 34] | orange-brown | 1.0 | -11 | Photo M14 |
  | render_cream | [214, 200, 178] | [150, 80, 38] | orange-brown | 1.0 | -39 | Photo M14 |
  | stone_sill | [170, 166, 158] | [140, 84, 46] | orange-brown | 1.0 | -27 | Photo M14 |
  | timber_paint_light | [222, 218, 206] | [150, 90, 48] | orange-brown | 1.0 | -43 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.2, "note": "darker, redder when wet"}`. [Judgement]
- **Texel scale:** smallest feature 5 mm; mask needs at least 1000 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: mask 0.2 m x 1.0 m at 1120 px/m = 224 x 1120; at 10 m a 10 mm trickle is under 2 screen pixels: scale width x1.5 beyond 6 m (builder's LOD)
- **Variants:** 5 seeded masks; they differ by one trickle, two trickles, trickle + drops, long thin, halo only; no rotation [Derived]
- **Why 1990 Britain:** Mild-steel fixings and cast iron rusted freely and the stain sits on the masonry; stainless and plastic fixings do not bleed (Judgement).
- **Not modern, not American:** No plastic-looking orange; no stain without an iron source above it.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | streak_aspect_p50 | streak_aspect | mask | `{"thr": 0.25, "min_length_m": 0.08, "stat": "p50"}` | 8 | 120 | Photo M14 |
  | streak_width_mm_p50 | streak_width_mm | mask | `{"thr": 0.25, "stat": "p50"}` | 4 | 36 | Photo M14 (blurred by the 10 mm edge) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.3, "band_hi": 0.9, "axis": "x"}` | 6 | 45 | Photo M13/M14 |
  | vertical_within_deg | verticality_deg | mask | `{"thr": 0.25}` | 0 | 8 | Derived: gravity |

### `algae_downpipe`: Algae and green damp at downpipes, gully corners and gutter leaks

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** Dark damp patch with green tinge 0.3 to 0.9 m wide at the downpipe shoe rising 0.4 to 1.2 m, wider and greener low down; below a leaking joint a vertical green-black run 0.1 to 0.3 m wide, 0.5 to 1.5 m long; in mortar joints it shows as green lines (moss in joints).
  - Feature: downpipe shoes and hoppers, leaking gutter joints, the corner where wall meets gully, shaded north-facing and gable faces, the wall foot beside a downpipe
  - Surfaces: brick_red, brick_painted, render_cream, stone_sill
  - Height: 0 to 1.2 at shoes; 0 to 1.5 below a leaking joint
  - Sides: East parade (west-facing, wet): 1.0; west block 0.6; gables 1.0
  - Footfall and wet: Wet climate; strongest in shade
  - Density: 0.8 to 1.0 per downpipe foot (typical 1.0) [Derived: every shoe]
- **Decal frame:** x -0.45 to 0.45 m, y 0.0 to 1.4 m; origin: origin = foot of the downpipe shoe on the pavement; y up
- **Shape and size (real units):** envelope primitive `blob_field`; envelope parameters `{"region_m": [0.9, 1.4], "anchor": "bottom_centre", "blobs": {"n": [1, 3], "eqd_m": [0.12, 0.25, 0.55], "aspect": [1.0, 3.5], "orient": "vertical"}, "joint_moss": {"share": 0.12, "src": "Photo M15: moss fills 12 to 17 % of brick area as joint lines"}, "run": {"n": [0, 2], "width_m": [0.05, 0.2], "length_m": [0.4, 1.4]}}`
  - Geometry numbers: `{"blob_eqd_mm": {"p10": 120, "p50": 250, "p90": 550, "src": "Judgement bounded by Photo M12 (damp blotches p50 42 mm, p90 171 mm, max 0.51 m) and Photo M15"}, "moss_patch_eqd_mm": {"p10": 5.5, "p50": 10.2, "p90": 31.5, "src": "Photo M15 (mossy_brick: 5.5, 10.2, 31.5 mm; brick_moss_001: 5.5, 13.1, 43.4 mm)"}, "edge_10_90_mm": [15, 80], "edge_src": "Photo M12 19 mm and 23 mm; Photo M15 6.7 to 9.5 mm for moss at joints", "edge_for_envelope_mm": 25}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [62, 67, 34] | green-black | 0.4 | -15 | Photo M15 (moss 55/57/9, 74/72/23) |
  | brick_painted | [152, 108, 93] | [84, 93, 58] | olive green-grey | 0.55 | -12 | Judgement |
  | render_cream | [214, 200, 178] | [142, 145, 77] | olive green | 0.45 | -23 | Judgement, coloured from a waterline: plaster_brick_01's green band (M15) is a trim-sheet waterline ('sewer, tunnel, trimsheet'), not a pavement wall foot; Photo M15 moss (mossy_brick) is the green |
  | stone_sill | [170, 166, 158] | [120, 131, 88] | olive green | 0.55 | -15 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.3, "note": "wet algae is darker, greener and slicker"}`. [Judgement]
- **Texel scale:** smallest feature 10 mm; mask needs at least 400 px/m, use 600; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 5 seeded masks; they differ by blob count and layout, run on/off, joint moss on/off; no rotation (rises from the foot) [Derived]
- **Why 1990 Britain:** Algae and moss on a leaking gutter are weather; the 1990 detail is cast-iron hoppers with cracked shoes that left permanent green-black patches.
- **Not modern, not American:** No bright lawn green; no even green wash.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 1500}` | 100 | 450 | Judgement/Photo M12 |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 12 | 100 | Photo M12/M15 |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.06 | 0.4 | Derived |

### `paint_flake`: Flaking and cracked paint on painted fronts

- **Layer:** L1 stamp decal on timber and render; part of L0 on stallrisers
- **Where (the rule):** Loss concentrates at the horizontal surfaces and the lowest 0.5 m (sills, rails, door bottoms, stallriser feet), where water lies: patches 10 to 250 mm (median 17 mm flakes, a few larger sheets), hard-edged, showing undercoat, bare wood or old colour; crazing (craquelure) cells 0.14 to 0.23 m across on old render paint. Share of a worn painted surface: 3 to 10 %, up to 40 % on a neglected sill or door foot. Door edges (the leading edge, 15 to 30 mm wide, 0.6 to 1.0 m long) wear through to undercoat the same way.
  - Feature: painted sills, window frames' lower rails, door bottoms and kick plates, stallrisers, fascia ends and undersides, pilaster plinths, painted render and painted brick
  - Surfaces: timber_paint_dark, timber_paint_light, brick_painted, render_cream
  - Height: mostly 0 to 0.9 and on sills at any height; fascias get edge chips only
  - Sides: East parade (wet) 1.0; west block 0.8; empty unit (bay 3, whitewashed, to let) 1.4 (neglected)
  - Footfall and wet: Footfall: door bottoms and kick plates (boots) and stallrisers where shopping trolleys and sack barrows knock; wet: sills and rails.
  - Density: 0.03 to 0.1 share of painted surface lost (typical 0.063) [Photo M08 (peeling_painted_wall 6.3 %, +/- 2 points); neglected up to 0.40 (Photo M10 39.5 %)]
  - With house wear: share x (wear / 0.78)^2
- **Decal frame:** x 0.0 to 1.0 m, y 0.0 to 1.0 m; origin: 1.0 m square tile, seamless
- **Shape and size (real units):** envelope primitive `flake_field`; envelope parameters `{"area_m": [1.0, 1.0], "flakes": {"density_per_m2": [30, 45], "eqd_mm": [11.6, 17.2, 37.8], "aspect_p50": 2.9, "big_sheets": {"n_per_m2": [0.3, 1.0], "eqd_mm": [80, 250]}, "src": "Photo M08"}, "craquelure": {"cell_m": [0.14, 0.23], "width_mm": [3, 8], "length_per_m2": [3.0, 6.0], "src": "Photo M09 (5.7 m per m2 detected)"}}`
  - Geometry numbers: `{"flake_eqd_mm": {"p10": 11.6, "p50": 17.2, "p90": 37.8, "max": 249, "src": "Photo M08"}, "flake_aspect_p50": 2.9, "flakes_per_m2": 38, "flake_src": "Photo M08", "edge_10_90_mm": [0.3, 3], "edge_src": "Photo M08: flake edges are hard (0.4 mm); a mask must be near-binary, 1 to 2 texels of softness only", "crack_cell_m": [0.14, 0.23], "crack_width_mm": [3, 8], "crack_length_m_per_m2": [3, 6], "edge_for_envelope_mm": 1}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | timber_paint_dark | [52, 64, 88] | [140, 120, 95] | bare timber and grey undercoat | 1.0 | 25 | Photo M08 loss colour 128/110/94 against paint 151/107/92 (about the same L*, hue shifts); Judgement for dark paint: bare wood is lighter |
  | timber_paint_light | [222, 218, 206] | [120, 100, 78] | bare timber and old colour | 1.0 | -43 | Judgement |
  | brick_painted | [152, 108, 93] | [110, 84, 70] | brick or old render showing | 1.0 | -12 | Photo M08/M10 (substrate 118/101/90) |
  | render_cream | [214, 200, 178] | [160, 150, 132] | grey render showing | 1.0 | -19 | Photo M10 render under pink paint: 118/101/90 against 176/111/101 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.78, "roughness_delta": -0.25, "note": "bare wood and render absorb water and go dark; paint stays glossy: the flake reads stronger when wet"}`. [Judgement]
- **Texel scale:** smallest feature 10 mm; mask needs at least 800 px/m, use 1000; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: tile 1.0 m square at 1000 px/m; also drives a height/normal chip (the flake edge is a step of 0.2 to 0.5 mm)
- **Variants:** 6 seeded masks; they differ by flake density x craquelure on/off x one big sheet; tile seamlessly; rotation in 90 degree steps allowed on flat faces [Derived]
- **Why 1990 Britain:** Oil-based paints on timber and render crazed and flaked in exactly this way (Judgement); factory-finished and uPVC fronts do not (Judgement: rare on an old port quarter in 1990). A 1990 front is repainted 'a shade off each time' (brand bible), so old colour shows through.
- **Not modern, not American:** No uPVC-white perfect frames; no flake with a soft blurred edge.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 60}` | 10 | 30 | Photo M08 |
  | blob_eqd_mm_p90 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p90", "min_area_mm2": 60}` | 25 | 80 | Photo M08 |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.03 | 0.15 | Photo M08 (6.3 %) plus craquelure |
  | count_per_m2 | count_per_m2 | mask | `{"thr": 0.5, "min_area_mm2": 60}` | 20 | 60 | Photo M08 |
  | craquelure_m_per_m2 | role_length_per_m2 | envelope | `{"role": "craquelure"}` | 3.0 | 7.0 | Photo M09 (5.7 m per m2) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 0.2 | 4 | Photo M08 |
  | tile_seam | tile_seam | mask | `{"axis": "xy"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |

### `paint_fade`: Faded, chalked and dirt-filmed paint

- **Layer:** L0 in the material (low-frequency tint), not a decal
- **Where (the rule):** A slow large-scale lightening and desaturation of paint, strongest on reds and blues, patchy at 0.5 to 2 m wavelength; chalking leaves a pale film that rubs away at handholds.
  - Feature: painted fascias, shopfront timber, render, sign boards; the upper parts and the street-facing south-west faces
  - Surfaces: timber_paint_dark, timber_paint_light, brick_painted, render_cream
  - Height: all heights; strongest 2.0 to 4.0 m (sun and rain exposure), weakest at the foot where splash dominates
  - Sides: East parade (west-facing, afternoon sun and rain): 1.0; west block: 0.7
  - Footfall and wet: Not footfall; the film of grime makes it a dull, slightly lighter and greyer version of the paint.
  - Density: 0.3 to 1.0 whole painted area (typical 0.6) [Judgement; asset plan: reds fade to pink before blues]
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 2.0 m; origin: 2.0 m square tile, seamless (a low-frequency field)
- **Shape and size (real units):** envelope primitive `mottle`; envelope parameters `{"wavelength_m": [0.5, 2.0], "level_range": [0.2, 0.8]}`
  - Geometry numbers: `{"mask_wavelength_m": [0.5, 2.0], "mask_std": 0.2, "edge_10_90_mm": [200, 2000], "edge_src": "Judgement", "edge_for_envelope_mm": 400}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | timber_paint_dark | [52, 64, 88] | [78, 86, 104] | dull faded blue-grey | 1.0 | 9 | Judgement; PAINTED-FRONTS-2026-10-07 wants 8 L* spread |
  | timber_paint_light | [222, 218, 206] | [204, 198, 184] | dirty cream | 1.0 | -7 | Judgement |
  | brick_painted | [152, 108, 93] | [160, 124, 112] | pink-faded | 1.0 | 5 | Judgement; Photo M08 pink paint 152/108/93 |
  | render_cream | [214, 200, 178] | [204, 192, 170] | dull cream | 1.0 | -3 | Photo M12 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.15, "note": "chalked paint is rougher"}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.2, "note": "wet paint regains depth of colour"}`. [Judgement]
- **Texel scale:** smallest feature 200 mm; mask needs at least 20 px/m, use 40; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 3 seeded masks; they differ by noise seed; tile seamlessly 4 m [Derived]
- **Why 1990 Britain:** Oil gloss on timber chalked and dulled within 5 to 8 years in coastal weather; 1990 fronts were repainted rarely. Perfectly saturated, uniform colour is a modern (acrylic, factory-finished) tell.
- **Not modern, not American:** No uniform factory colour; no saturated primary colour on a front last painted in the 1980s.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | mask_std | mask_std | mask | `{}` | 0.08 | 0.2 | Judgement: levels 0.2 to 0.8 |
  | dominant_wavelength_m | dominant_wavelength_m | mask | `{}` | 0.5 | 2.0 | Judgement (reviewer 8 October): the mottle's wavelength is 0.5 to 2.0 m, not texel noise |
  | tile_seam | tile_seam | mask | `{"axis": "xy"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "reach_mm": 1500}` | 150 | 3000 | Judgement |

### `render_crack`: Cracked render and stucco

- **Layer:** L1 rule-placed wall decal (plus a normal/height scratch)
- **Where (the rule):** Diagonal cracks step out from the top corners of openings at 30 to 60 degrees, 0.2 to 0.9 m long; a shear crack along the render/brick change; and map (craquelure) cracking in patches 0.3 to 1.2 m across with cells 0.14 to 0.23 m. Width 2 to 8 mm; darker than the render by 12 to 25 L*, with a light fringe where the edge is lifted.
  - Feature: rendered and stuccoed surfaces (painted render bays, shopfront render, the whitewashed empty unit), the corners of door and window openings, joints between render and brick, gable render
  - Surfaces: render_cream, brick_painted
  - Height: any; openings' corners and 0.0 to 1.5 where impact and damp act together
  - Sides: Both; whitewashed empty unit 1.5
  - Footfall and wet: Wet climate: water enters and the crack gets a dark damp margin
  - Density: 3.0 to 6.0 metres of crack per m2 of rendered wall (map-cracked patches only) (typical 4.5) [Photo M09 (5.7 m/m2) and cracked_concrete_wall (4.1 m/m2), detected; whole-wall average 0.15 to 0.6 m/m2 (Judgement)]
  - With house wear: number of corner cracks 0 to 2 per opening by wear
- **Decal frame:** x -0.9 to 0.9 m, y -0.5 to 1.3 m; origin: origin = the top corner of an opening (corner cracks leave it upward and outward)
- **Shape and size (real units):** envelope primitive `crack_set`; envelope parameters `{"corner_cracks": {"n_per_opening": [1, 2], "length_m": [0.2, 0.9], "angle_deg": [30, 60], "width_mm": [2, 8], "branch_prob": 0.25, "step_m": 0.03}, "map_cracking": {"patch_m": [0.3, 1.2], "cell_m": [0.14, 0.23]}, "region_m": [1.2, 1.2]}`
  - Geometry numbers: `{"crack_width_mm": {"p10": 2, "p50": 4, "p90": 8, "src": "Photo M09 (3.9, 7.8, 14.1 mm detected at 1.95 mm/px incl. blur) and cracked_concrete_wall (1.4, 2.8, 4.1 mm at 0.49 mm/px); true width 2 to 8"}, "crack_length_m_per_m2_in_mapped_patch": [3.0, 6.0], "cell_m": [0.14, 0.23], "edge_10_90_mm": [1, 6], "edge_src": "Photo M09: cracks are hairline sharp", "edge_for_envelope_mm": 1.5}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | render_cream | [214, 200, 178] | [120, 108, 92] | dark brown-grey | 1.0 | -35 | Photo M12/M09 |
  | brick_painted | [152, 108, 93] | [66, 52, 44] | dark brown-grey | 1.0 | -27 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.7, "roughness_delta": -0.3, "note": "cracks wet and dark; a damp margin 10 to 30 mm wide"}`. [Judgement]
- **Texel scale:** smallest feature 2 mm; mask needs at least 1000 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: cracks need 1120 px/m (1 texel = 0.9 mm); beyond 6 m they alias, so fade the decal out by 8 m (LOD) and carry the same cracks as a 0.2 to 0.4 low-pass 'dark line' in the L0 material
- **Variants:** 6 seeded masks; they differ by corner crack left/right, corner with branch, shear crack, map-cracked patch, map-cracked patch 2, one long vertical [Derived]
- **Why 1990 Britain:** Sand-cement render cracks from drying shrinkage and thermal movement; lime plaster over brick crazes. It is old building behaviour, not period styling.
- **Not modern, not American:** No perfectly straight computer cracks; no tapering 'lightning' bolts; branches at 25 degrees or less.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | crack_width_mm | crack_width_mm | mask | `{"thr": 0.5}` | 1.5 | 10 | Photo M09 |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 0.8 | 8 | Photo M09 |
  | crack_length_m_per_m2_of_frame | crack_length_per_m2 | mask | `{"thr": 0.5}` | 0.3 | 3.5 | Derived: mapped patch 4.5 m/m2 over its share of the frame, plus 1 to 4 corner cracks |

### `render_patch`: Render patches, missing render, repointing and replacement bricks

- **Layer:** L1 stamp decal (with a height step) and hand placement for the hero patch
- **Where (the rule):** Repair patches: buff or pale-grey rectangles with irregular corners, 0.2 to 0.45 m across, 0 to 3 per 10 m of facade, often at a former fixing, pipe or cable. Render loss: ragged patches 30 to 300 mm (median 67 mm, a few to 0.45 m) revealing brick, concentrated at the foot and arrises. Replacement bricks: single bricks 0.215 x 0.065 m of a different colour.
  - Feature: walls: where render fell and brick shows; patch repairs in fresher, paler mortar or render; repointing in hard grey cement; odd replacement bricks
  - Surfaces: brick_red, render_cream, brick_painted
  - Height: repair patches 1.0 to 3.5; render loss 0 to 1.2
  - Sides: Both; the pale high patch on the left gable of the Hook sheet is the hero (L3, by hand)
  - Footfall and wet: Footfall: arrises and door jambs, bumped by trolleys and bikes
  - Density: 0.5 to 3.0 patches per 10 m of facade (typical 1.5) [Sheet M19: one patch visible in the whole 14 m left gable; Judgement]
- **Decal frame:** x -0.35 to 0.35 m, y -0.45 to 0.35 m; origin: origin = patch centre
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.2, 0.45], [0.2, 0.4]], "ragged_mm": [10, 40], "drip_tail": {"length_m": [0.05, 0.15], "width_m": [0.02, 0.05]}, "loss_blobs": {"eqd_m": [0.033, 0.067, 0.294], "n_per_m2": [4, 9], "src": "Photo M11"}}`
  - Geometry numbers: `{"patch_size_m": {"w": [0.2, 0.45], "h": [0.2, 0.4], "hero_sheet": [0.28, 0.3], "src": "Sheet M19 (3.8 courses x about 1.3 brick lengths, +/-30 %)"}, "loss_eqd_mm": {"p10": 32.5, "p50": 67, "p90": 294, "max": 453, "src": "Photo M11 (damaged_plaster)"}, "edge_10_90_mm": [8, 25], "edge_src": "Photo M11 11.4 mm; patch edges are crisp, with a soft smear below", "edge_for_envelope_mm": 12}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [188, 168, 126] | pale buff mortar | 1.0 | 27 | Sheet M19 is wet: patch 175/140/92 (L* 60.6) on a wall of L* 26.6 (+34); fresh mortar loses about 25 % of its luminance when wet (wet multiplier below), so the dry patch is L* about 69 and the dry difference on the target's brick (L* 42) about +28 |
  | render_cream | [214, 200, 178] | [150, 140, 126] | grey patch | 1.0 | -22 | Photo M11 (exposed render/brick 163/150/136 to 121/90/69) |
  | brick_painted | [152, 108, 93] | [170, 150, 120] | pale buff | 1.0 | 13 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.1}`; wet: `{"albedo_mult_on_tone": 0.75, "roughness_delta": -0.15, "note": "fresh mortar and bare render absorb water and darken strongly, so the patch reads less pale when wet"}`. [Judgement; the tone above is the dry value derived from the wet sheet, used once]
- **Texel scale:** smallest feature 10 mm; mask needs at least 400 px/m, use 600; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 6 seeded masks; they differ by rectangular, L-shaped, tall thin (a cut chase), square with a drip tail, loss cluster, single replacement brick [Derived]
- **Why 1990 Britain:** Patch repairs in the wrong mortar were everywhere: 'contrasting wall repairs' in photographs.md R07 (Marshall, Newtown Square, Hull, 1989).
- **Not modern, not American:** No tidy colour-matched repair; no laser-straight edge; no cleaned-grey cement repointing of the whole wall.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 800}` | 30 | 350 | Photo M11, Sheet M19 |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 6 | 30 | Photo M11 |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.1 | 0.6 | Derived |

### `poster_remnant`: Fly-poster remnants and glue ghosts

- **Layer:** L1 stamp decal (colour supplied by the sign family's own posters; this kind is the paper-and-paste mask)
- **Where (the rule):** Layers of torn paper: a rectangle 0.4 to 1.0 m across (a poster sheet of double crown, 0.76 x 0.51 m, or quad crown, 1.02 x 0.76 m), 20 to 70 % intact, torn along diagonal edges and lifted at the top; thin pale paste ghost around it; a few bare corners and strips. Invented local campaigns only (RULINGS 3 Oct: poll-tax posters, never real parties).
  - Feature: hoardings, the blank side gable, boarded windows, the empty unit's glass and door, the shuttered bay, electrical boxes at the quay end
  - Surfaces: brick_red, render_cream, timber_paint_dark, timber_paint_light
  - Height: 0.9 to 2.6 (as high as a person's arm reaches with a ladder-free paste brush)
  - Sides: Both; heaviest on the empty unit (bay 3) and the quay-end gable
  - Footfall and wet: Footfall; paper swells and sags when wet: wet poster is darker, translucent and hangs lower
  - Density: 0 to 2 sites per facade (typical 1) [Judgement]
- **Decal frame:** x -0.55 to 0.55 m, y -0.45 to 0.45 m; origin: origin = site centre
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.4, 1.0], [0.3, 0.75]], "ragged_mm": [20, 120], "drip_tail": {"length_m": [0.0, 0.0], "width_m": [0.0, 0.0]}, "layers": {"n": [2, 4], "intact_fraction": [0.2, 0.7]}, "loss_blobs": {"eqd_m": [0.02, 0.05, 0.15], "n_per_m2": [5, 15]}}`
  - Geometry numbers: `{"sheet_size_m": [[0.76, 0.51], [1.02, 0.76]], "edge_10_90_mm": [2, 10], "edge_src": "Judgement: torn paper edge is hard", "paste_ghost_width_mm": [10, 40], "sheet_names": "double crown 0.76 x 0.51 m, quad crown 1.02 x 0.76 m (the first pass said 'A1', which is 0.594 x 0.841 m)", "edge_for_envelope_mm": 4}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [196, 186, 168] | paper and paste | 1.0 | 33 | Judgement |
  | render_cream | [214, 200, 178] | [176, 164, 144] | dirty paper | 1.0 | -13 | Judgement |
  | timber_paint_dark | [52, 64, 88] | [186, 176, 158] | paper and paste | 1.0 | 45 | Judgement |
  | timber_paint_light | [222, 218, 206] | [172, 162, 142] | dirty paper | 1.0 | -20 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.6, "roughness_delta": -0.4, "note": "wet paper is dark, slightly translucent, glossy"}`. [Judgement]
- **Texel scale:** smallest feature 20 mm; mask needs at least 300 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 5 seeded masks; they differ by intact fraction 20/40/70 %, layer count, torn corner, one strips-only; no rotation [Derived]
- **Why 1990 Britain:** Fly-posting was common on empty units and hoardings (Judgement); wheatpaste layers built up over months. No QR codes, no digital print gloss, no vinyl stickers.
- **Not modern, not American:** No glossy A3 sheet, no cable ties, no printed vinyl.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 3000}` | 120 | 800 | Judgement |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 2 | 14 | Judgement |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.25 | 0.75 | Derived |

### `bird_dropping`: Gull droppings on ledges, sills and rooftop edges

- **Layer:** L1 stamp decal (small), hand-placed beside the quay
- **Where (the rule):** White splashes on horizontal surfaces and runs 0.05 to 0.30 m down the face below; pavement splats 30 to 120 mm under perches at the quay end.
  - Feature: ledges, sill tops, fascia tops, window heads, chimney coping, street lamp tops, bollard tops, the pavement under a favourite perch
  - Surfaces: stone_sill, brick_red, iron_black, flag_concrete, timber_paint_dark
  - Height: ledges at any height; pavement splats at ground
  - Sides: Quay end (x 0 to 15: within 12 m of the quay end) and the quay-facing side 1.0; inland end 0.4
  - Footfall and wet: Wet washes them to a pale grey smear
  - Density: 0.2 to 1.2 per metre of ledge (typical 0.6) [Judgement (a port with gulls); no photograph measured]
- **Decal frame:** x -0.2 to 0.2 m, y -0.5 to 0.05 m; origin: origin = the ledge edge above; runs fall to negative y
- **Shape and size (real units):** envelope primitive `blob_field`; envelope parameters `{"region_m": [0.4, 0.5], "anchor": "top_centre", "blobs": {"n": [1, 3], "eqd_m": [0.03, 0.06, 0.12], "aspect": [1.0, 2.5], "orient": "vertical"}, "run": {"n": [0, 1], "width_m": [0.01, 0.03], "length_m": [0.05, 0.3]}}`
  - Geometry numbers: `{"blob_eqd_mm": {"p10": 30, "p50": 60, "p90": 120, "src": "Judgement"}, "edge_10_90_mm": [3, 12], "edge_src": "Judgement", "edge_for_envelope_mm": 6}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | stone_sill | [170, 166, 158] | [226, 224, 214] | white with grey centre | 1.0 | 21 | Judgement |
  | brick_red | [140, 87, 70] | [218, 214, 204] | white with grey centre | 1.0 | 43 | Judgement |
  | iron_black | [35, 35, 36] | [216, 214, 206] | white | 1.0 | 72 | Judgement |
  | flag_concrete | [134, 123, 110] | [214, 210, 200] | white | 1.0 | 32 | Judgement |
  | timber_paint_dark | [52, 64, 88] | [218, 214, 204] | white | 1.0 | 59 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.4, "note": "glossy and translucent when wet"}`. [Judgement]
- **Texel scale:** smallest feature 10 mm; mask needs at least 600 px/m, use 800; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by single splat, splat with run, pair, scatter; rotation allowed only on horizontal surfaces [Derived]
- **Why 1990 Britain:** Timeless (Judgement). No bird spikes or netting on this street.
- **Not modern, not American:** No bird-spike strips; no netting; no 1970s-modern white-stained cladding.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 300}` | 25 | 100 | Judgement |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 2 | 20 | Judgement |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.01 | 0.2 | Derived: 1 to 3 splats 30 to 120 mm across in 0.4 x 0.55 m |
  | peak_mask | mask_max | mask | `{}` | 0.7 | 1.0 | Judgement |

### `gum`: Chewing gum on the pavement

- **Layer:** L2 ground (stamped into the ground's virtual texture)
- **Where (the rule):** Poisson-disc scatter on the footway with density weighted by footfall; discs 11 to 35 mm, trodden flat; never on the road, rarely on the kerb top; clusters of 2 to 4 within 0.3 m near doors.
  - Feature: pavement flags, densest in front of shop doors and at the kerb crossing points, around bins, outside the cab office rank (there is no bus stop on the street yet: zero)
  - Surfaces: flag_concrete, kerb_granite
  - Height: ground
  - Sides: East footway (shops) 1.0; west footway 0.7; none on the carriageway, none within 0.4 m of a wall (nobody walks there), rarely on the kerb top
  - Footfall and wet: Footfall is the driver. Wet changes nothing in position; the stain darkens and glints.
  - Density: 0.5 to 8.0 per m2 of footway (typical 2.5) [Judgement, kept low: gum staining existed in 1990 but grew later; no 1990 figure was reached (search lead only: Keep Britain Tidy 2017 found gum staining on 99 % of main shopping streets, no per-m2 figure); no photograph measured (the 2019 London panoramas show a low-gum residential street). The first pass's 1 to 12 per m2 is lowered. The bus stop is zero until one is placed]
  - Density tiers: `{"shop door apron (1.5 m radius)": [4, 8], "kerb crossing": [2, 5], "open footway": [0.5, 2], "wall foot strip": [0, 0.3], "bus stop": [0, 0]}`
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 2.0 m; origin: a 2.0 m ground tile (4 m2) at the typical density 2.5 per m2; the builder scatters stamps by the density tier, this is the reference tile
- **Shape and size (real units):** envelope primitive `points`; envelope parameters `{"shape": "disc", "eqd_mm": [11, 20, 35], "aspect": [1.0, 1.5], "per_m2": [0.5, 8.0], "cluster": {"prob": 0.5, "n": [2, 4], "radius_m": 0.3}, "ring": {"width_mm": 3, "level": 0.4}}`
  - Geometry numbers: `{"eqd_mm": {"p10": 11, "p50": 20, "p90": 35, "src": "Judgement; Sheet M20 pavement spots 150 to 400 mm are stains, not gum"}, "edge_10_90_mm": [1, 4], "edge_src": "Judgement: a gum disc has a hard edge and a slightly paler rim", "edge_for_envelope_mm": 2}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [62, 58, 54] | dark grey-black, paler rim | 1.0 | -28 | Sheet M20: dark pavement spots L* 27.6 on flags L* 54.7 (-27); Judgement for gum itself |
  | kerb_granite | [128, 126, 122] | [66, 62, 58] | dark grey-black | 1.0 | -26 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.3, "note": "glossy against the matte flag: roughness 0.45 against 0.85"}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.45, "note": "roughness 0.25; glints under the street lamps"}`. [Judgement]
- **Texel scale:** smallest feature 12 mm; mask needs at least 500 px/m, use 700; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: one stamp sheet of 8 gum discs, each 64 x 64 texels for a 40 mm square (1600 px/m local) is fine; ground virtual texture needs 700 px/m at least on shop aprons
- **Variants:** 8 seeded masks; they differ by disc, oval, with-a-tail, pair, with-a-pale-rim, pink-tinted (rare), black-and-flat, tiny; free rotation and mirror (it lies flat) [Derived]
- **Why 1990 Britain:** Gum staining existed in 1990 but grew later, so the tiers are kept low (Judgement; no 1990 photograph with gum reached). The mark itself is grey-black and the shape does not change.
- **Not modern, not American:** No tactile paving studs nearby; no wheelie-bin lines; no 'Gum Targets' campaign stencils.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 80}` | 14 | 28 | Judgement |
  | count_per_m2_open_footway | count_per_m2 | mask | `{"thr": 0.5, "min_area_mm2": 80}` | 0.5 | 8.0 | Judgement (lowered from 1 to 12) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 0.8 | 5 | Judgement |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.0001 | 0.006 | Derived: 10 x 3.1e-4 m2 over 4 m2 |
  | nn_ratio | nn_ratio | mask | `{"thr": 0.5, "min_area_mm2": 80, "area": "frame"}` | 0.5 | 1.1 | Judgement (reviewer 8 October): gum clusters near doors; a grid of identical discs is rejected |
  | size_cv | size_cv | mask | `{"thr": 0.5, "min_area_mm2": 80}` | 0.25 | 1.2 | Judgement (reviewer 8 October): discs differ in size |

### `cig_end`: Cigarette ends, matchsticks and small litter

- **Layer:** L2 ground (stamped), plus PCG-scattered instances at the kerb band
- **Where (the rule):** Two bands: (1) kerb band, 0 to 0.3 m from the kerb foot, 3 to 6 pieces per metre of kerb, piled at gully grates; (2) doorway aprons, 4 to 10 per m2 within 1.2 m of a shop door; open footway and open road 0.3 to 1.0 per m2. Each end 8 mm x 25 to 30 mm; white filter or tan filter, some burnt-orange, some flattened. Tobacco is allowed (canon).
  - Feature: the kerb foot (channel) and the strip 0 to 0.3 m inside it, shop doorways and their steps, the cab-office rank, under bins, drain grates, the pavement edge by the wall
  - Surfaces: flag_concrete, asphalt_dry, kerb_granite
  - Height: ground
  - Sides: East footway (shop doors) 1.0; west 0.7; kerb band both sides; none on the carriageway beyond 1.0 m of the kerb except the open-road density
  - Footfall and wet: Footfall + wind + runoff: ends drift to the channel and bunch at gullies; wet makes them dark, soggy, and paler tobacco-brown.
  - Density: 3 to 6 per metre of kerb (band) and per m2 (aprons, open) (typical 4.4) [Photo M06 (urban_street_02, counted by eye: 22 pieces over 5 m of kerb = 4.4 per m; road 0.7 per m2; +/-35 %)]
  - Density tiers: `{"kerb band per metre of kerb": [3, 6], "shop door apron per m2": [4, 10], "open footway per m2": [0.3, 1.0], "open road per m2": [0.2, 0.8]}`
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 2.0 m; origin: a 2.0 m ground tile (4 m2) at 4 per m2; the kerb band is separate (per metre of kerb)
- **Shape and size (real units):** envelope primitive `points`; envelope parameters `{"shape": "rect", "mix": [{"name": "end", "share": 0.5, "w_mm": [6, 8, 10], "l_mm": [18, 26, 32]}, {"name": "fragment", "share": 0.25, "w_mm": [4, 6, 8], "l_mm": [5, 8, 11]}, {"name": "matchstick", "share": 0.1, "w_mm": [3, 4, 5], "l_mm": [30, 40, 48]}, {"name": "scrap", "share": 0.15, "w_mm": [12, 22, 40], "l_mm": [14, 26, 46]}], "per_m2": [0.3, 10], "band": {"length_m": 2.0, "depth_m": 0.3, "per_m": [3, 6]}}`
  - Geometry numbers: `{"piece_size_mm": {"eqd_p10": 8, "eqd_p50": 11, "eqd_p90": 28, "src": "Photo M06 detection of bright bits: 7.6, 11.2, 27.7 mm"}, "cig_dimensions_mm": [8, 27], "cig_src": "Read/Judgement: UK cigarette 8 mm across, butt 25 to 30 mm", "edge_10_90_mm": [0.8, 3], "edge_src": "Judgement", "piece_mix": {"src": "Photo M06: pieces of 7.6 / 11.2 / 27.7 mm (p10 / p50 / p90) are cigarette ends (8 x 27 mm), paper scraps and matchsticks in the shares stated: ends 50, fragments 25, matchsticks 10, paper scraps 15 %; Judgement for the shares"}, "edge_for_envelope_mm": 1.5}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [228, 222, 208] | white filter, tan tip | 1.0 | 36 | Photo M06 (bright litter on grey surfaces); Judgement |
  | asphalt_dry | [89, 86, 80] | [232, 228, 216] | white filter | 1.0 | 54 | Photo M06 |
  | kerb_granite | [128, 126, 122] | [222, 214, 198] | white filter | 1.0 | 33 | Judgement |

  - Also on flag_concrete: tan cork-pattern filter tip, 40 % of the marks, sRGB [177, 140, 110] [Photo M06: 4 of 13 litter bits in the kerb strip are clearly tan (9 of 24 by the reviewer, 6 of 13 with borderline pieces: 31 to 46 %); tan median 177/140/110]
  - Also on asphalt_dry: tan cork-pattern filter tip, 40 % of the marks, sRGB [177, 140, 110] [Photo M06]
  - Also on kerb_granite: tan cork-pattern filter tip, 40 % of the marks, sRGB [177, 140, 110] [Photo M06]
- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.55, "roughness_delta": -0.3, "note": "soaked ends go dull brownish-grey, not white"}`. [Judgement]
- **Texel scale:** smallest feature 8 mm; mask needs at least 750 px/m, use 1000; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 10 seeded masks; they differ by straight end, bent end, flattened, burnt-tip, matchstick, small paper scrap, blank paper packet corner (no brand marks), paper wrapper corner, leaf, pair; 4 in 10 ends tan, 6 white; free rotation and mirror [Derived]
- **Why 1990 Britain:** Smoking was normal in the street and doorways; filter tips were tan 'cork-pattern' (4 in 10 in Photo M06) or white; no vaping debris, no blister packs, no coffee-cup lids. Paper and wrapper scraps only: no cans, bottles or tops (canon: no alcohol), no betting slips.
- **Not modern, not American:** No face-mask litter, no vape pods, no energy-drink cans, no takeaway coffee cups.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 30}` | 8 | 22 | Photo M06 |
  | count_per_m2_open_footway | count_per_m2 | mask | `{"thr": 0.5, "min_area_mm2": 30}` | 0.3 | 10.0 | Photo M06, Judgement |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 0.6 | 4 | Judgement |
  | nn_ratio | nn_ratio | mask | `{"thr": 0.5, "min_area_mm2": 30, "area": "frame"}` | 0.7 | 1.3 | Judgement (reviewer 8 October): ends are scattered, not on a lattice |
  | size_cv | size_cv | mask | `{"thr": 0.5, "min_area_mm2": 30}` | 0.25 | 1.5 | Judgement (reviewer 8 October) |

### `pavement_stain`: Dark and brown stains on the flags; grime halos round drains; wet-looking joints

- **Layer:** L2 ground
- **Where (the rule):** Stains: irregular blots 0.08 to 0.45 m, 3 to 10 per 10 m2 of footway; grime halo round every drain and cover: a ring 0.15 to 0.35 m wide, dark and gradually fading; flag joints 3 to 10 mm wide darker than the flag by 8 to 20 L* and 2x wider where water stands.
  - Feature: open flags (random), shop doorways and steps (spilled water, wet boots), under downpipe outfalls, around gully grates and cast-iron covers (halo), along the footway edge by the kerb, flag joints
  - Surfaces: flag_concrete, kerb_granite
  - Height: ground
  - Sides: East 1.0; west 0.9
  - Footfall and wet: Footfall + wet: stains read strongly when wet (the Hook sheet's brown blots are rust and mud wash) and are the same marks, a little lighter, when dry.
  - Density: 3 to 10 blots per 10 m2 of footway (typical 6) [Sheet M20 (7 stains in about 14 m2 of the right pavement: 5 per 10 m2); Judgement]
- **Decal frame:** x -0.5 to 0.5 m, y -0.5 to 0.5 m; origin: origin = stain or drain centre
- **Shape and size (real units):** envelope primitive `blob_field`; envelope parameters `{"region_m": [1.0, 1.0], "anchor": "centre", "blobs": {"n": [1, 3], "eqd_m": [0.08, 0.18, 0.45], "aspect": [1.0, 3.0], "orient": "free"}, "halo": {"width_m": [0.15, 0.35], "level": 0.5}, "joints": {"width_mm": [3, 10], "level": 0.6}}`
  - Geometry numbers: `{"blob_eqd_mm": {"p10": 80, "p50": 180, "p90": 450, "src": "Sheet M20 (relative to a 0.6 m flag: 0.15 to 0.7 of a flag width); Photo M12 blotch p50 42 mm, p90 171 mm"}, "edge_10_90_mm": [8, 60], "edge_src": "Sheet M20 ragged but wet-soft; Photo M12 19 mm", "edge_for_envelope_mm": 25}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [91, 64, 47] | brown, rust and mud | 0.3 | -23 | Sheet M20 is wet: stain 85/60/44 (Y 0.053) on flag 136/129/131 (Y 0.226) is a luminance ratio of 0.236 (L* 27.6 on 54.7); dry = 0.236 / 0.80 (the wet multiplier below) = 0.30. The first pass used 0.38 and the review's 0.38 wet / 0.48 dry: both are above the measured ratio (D10) |
  | kerb_granite | [128, 126, 122] | [98, 90, 82] | dark brown-grey | 0.5 | -14 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0, "note": "dry: the mark at its stated multiplier 0.30, matte"}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.4, "note": "wet: darker and shiny, 0.30 x 0.80 = 0.24 = the sheet's wet ratio; puddles sit on top (separate puddle masks)"}`. [Sheet M20 (wet); Read WET-ROAD-2026-10-08]
- **Texel scale:** smallest feature 30 mm; mask needs at least 250 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 6 seeded masks; they differ by blot, double blot, drain halo (round), drain halo (rectangular, grate 0.4 m), downpipe outfall splay, joint set; free rotation [Derived]
- **Why 1990 Britain:** Rust-brown stains from bits of old iron grating, unswept dirt and tobacco/tea spills were normal; bleach-clean pavements (pressure-washed) are 2000s.
- **Not modern, not American:** No pressure-washed pale patches, no fresh stripe-shaped cleaning lines.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | role_blob_eqd_mm | envelope | `{"role": "blob", "stat": "p50"}` | 80 | 300 | Sheet M20 |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 8 | 80 | Sheet M20/Photo M12 |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.01 | 0.3 | Derived: blobs 0.1 to 0.4 m across, with or without a drain halo |
  | peak_mask | mask_max | mask | `{}` | 0.6 | 1.0 | Judgement: blob levels 0.75 to 1.0 |
  | composed_ground_min_ratio | composed_ground_min_ratio | composition | `{}` | 0.279 | 1.0 | compose.ground floor 0.28: pavement_stain and gutter_grime stacked at mask 1 on a kerb never go below it |

### `flag_patch_crack`: Patched, mixed-tone and cracked flags

- **Layer:** L2 ground (flag tone variation) plus L1 hairline-crack decal
- **Where (the rule):** Per flag, pick a tone class: dark weathered (55 %), pale replacement (30 %), mid (15 %). Replacement slabs sit in runs of 1 to 4 along a trench line or around a cover. About 1 flag in 9 has a hairline crack (2 to 4 mm) across a diagonal or in a Y; 1 in 30 has a corner chipped off.
  - Feature: the footway: flags replaced after utilities work, rocking flags, tree-root or traffic-cracked flags, crossovers in concrete, the slab beside a cover or service plate
  - Surfaces: flag_concrete
  - Height: ground (replacement slabs sit 0 to 8 mm proud or sunk)
  - Sides: Both footways; west footway 1.0, east 0.9 (the parade's pavement was more recently relaid at shopfronts)
  - Footfall and wet: Footfall and heavy traffic at crossovers; wet reveals tone difference more (the dark slabs are the dirty ones)
  - Density: 0.3 to 0.5 share of flags (typical 0.45) [Photo M07: 45 % of visible flags non-dark in the patched stretch (pale 30 %, mid 15 %)]
- **Decal frame:** x 0.0 to 3.0 m, y 0.0 to 2.4 m; origin: a 3.0 x 2.4 m footway sample; tone classes are per-flag data
- **Shape and size (real units):** envelope primitive `slab_grid`; envelope parameters `{"slab_m": [0.6, 0.6], "region_m": [3.0, 2.4], "tone_shares": {"dark": 0.55, "pale": 0.3, "mid": 0.15}, "crack_fraction": 0.11, "joint_mm": [3, 8]}`
  - Geometry numbers: `{"slab_classes": {"dark": {"srgb": [134, 129, 128], "share": 0.55, "mask_level": 0.0, "src": "Photo M07 (133/130/130 class colour 134/129/128)"}, "mid": {"srgb": [156, 147, 144], "share": 0.15, "mask_level": 0.5, "src": "Judgement: between"}, "pale": {"srgb": [173, 164, 161], "share": 0.3, "mask_level": 1.0}}, "slab_size_m": [0.6, 0.6], "slab_src": "Photo M07 (about 0.6 to 0.7 m, +/-15 %); Read: BS 7263 flags 600 x 600 or 450 x 600 mm, pre-metric 24 in x 18 in", "dark_to_pale_luminance_ratio": 0.58, "ratio_range": [0.5, 0.7], "crack_width_mm": [2, 4], "joint_width_mm": [3, 8], "edge_10_90_mm": [1, 8], "edge_src": "Photo M07: slab edges are crisp; tone change is flat per slab", "edge_for_envelope_mm": 4}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [173, 164, 161] | pale replacement flag | 1.0 | 16 | Photo M07: pale 173/164/161 (mean of two slabs, linear) on dark 134/129/128 (mean of four slabs): luminance ratio dark/pale 0.584 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.68, "roughness_delta": -0.4, "note": "wet stone x0.68 (Read: WET-ROAD); cracks and joints hold water and go black"}`. [Read WET-ROAD-2026-10-08]
- **Texel scale:** smallest feature 3 mm; mask needs at least 800 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: flag tone is per-flag data; only the hairline cracks need 1120 px/m
- **Variants:** 6 seeded masks; they differ by tone class per flag is data (per-flag attribute) not a texture; crack decals: Y-crack, diagonal, corner chip, two hairlines, none, long straight [Derived]
- **Why 1990 Britain:** Concrete flags (not block paving) with irregular utility replacements: the old-quarter footway of the period (Judgement; the 2019 street of M07 shows the same fabric). Tactile paving came into UK use only from about 1990 to 1991 (unverified), and block-paved footways are later: none on this street.
- **Not modern, not American:** No tactile paving, no block paviors on the footway, no uniform new slabs.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | tone_ratio | tone_ratio | flag data | `{"dark_over_pale": true}` | 0.5 | 0.7 | Photo M07 |
  | crack_flag_share | crack_flag_share | flag data | `{}` | 0.05 | 0.2 | Photo M07 (11 %) |

### `road_oil`: Oil drip speckle under standing cars

- **Layer:** L2 ground (virtual texture)
- **Where (the rule):** One band per standing car: 0.3 m wide x 1.0 to 2.5 m long, 120 to 260 dots per m2 inside it (counted at the darker threshold; the lighter threshold counts 2.5 times as many), dots 11 to 29 mm, centred 0.9 to 1.6 m from the kerb (beneath the engine); the band lies along the car, so its long axis is parallel to the kerb (free yaw only within +/-10 degrees). Blots and scuffs are separate kinds.
  - Feature: standing places: the engine position of each vehicle that stands at the kerb (the rank, the loading aprons, the private places; section 4 places)
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Kerbside standing both sides; the rank (east, x 3 to 9) 1.5; the loading aprons (east x 9 to 15 and x 40 to 46) 1.3; none in the yard entrance (x 21 to 24)
  - Footfall and wet: Traffic: strongest where vehicles stand; wet: dots look darker and slicker.
  - Density: 0.5 to 1.0 speckle bands per standing place (typical 0.8) [Photo M04 (one band per car; 154 dots per m2 inside the band at rel < 0.75, 379 at rel < 0.85); Judgement]
- **Decal frame:** x 0.0 to 2.6 m, y -0.3 to 0.3 m; origin: origin = start of the drip band on the engine line; x along the car (parallel to the kerb), y across it
- **Shape and size (real units):** envelope primitive `speckle_band`; envelope parameters `{"length_m": [1.0, 2.5], "width_m": 0.32, "dot_eqd_mm": [10.6, 16.9, 29.4], "density_per_m2": [120, 260]}`
  - Geometry numbers: `{"dot_eqd_mm": {"p10": 10.6, "p50": 16.9, "p90": 29.4, "src": "Photo M04 (rel luminance < 0.85, n 222 in 1.33 m2)"}, "band_width_m": {"p5_95": 0.32, "src": "Photo M04"}, "band_length_m": {"visible": 1.83, "src": "Photo M04, cut by the frame: at least"}, "edge_10_90_mm": [2, 8], "edge_src": "Photo M04: the dots are crisp", "edge_for_envelope_mm": 6}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [89, 86, 80] | [74, 72, 72] | dark grey-black | 0.7 | -6 | Photo M04: dots at 0.70 of the luminance around them |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.25, "note": "oil film glossier than dry asphalt: roughness 0.65 against 0.9"}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.5, "note": "roughness 0.15 inside dots; against wet stone 0.45; reads as small bright reflective specks at grazing angles"}`. [Read WET-ROAD-2026-10-08 + Judgement]
- **Texel scale:** smallest feature 10 mm; mask needs at least 600 px/m, use 1000; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: stamp 2.6 m x 0.6 m at 1000 px/m; at 10 m the dots are 2 screen px, so beyond 8 m swap to a 0.3 strength smooth band
- **Variants:** 5 seeded masks; they differ by band length 1.0, 1.5, 2.0, 2.5 m and one broken in two; free mirror; yaw within +/-10 degrees [Derived]
- **Why 1990 Britain:** Older cars dripped more oil, so a drip band under every standing place is a 1990 marker (Judgement); the 2019 band of M04 is therefore the lighter end of the range.
- **Not modern, not American:** No cleaned-up bay, no new black-top without stains; no EV-era clean parking spaces.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | dot_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 50}` | 10 | 30 | Photo M04 |
  | dots_per_m2_of_frame | count_per_m2 | mask | `{"thr": 0.5, "min_area_mm2": 50}` | 15 | 170 | Photo M04: 154 per m2 inside the band, a band of 0.32 x 1.0 to 2.5 m inside the 2.6 x 0.6 m frame |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 1 | 14 | Photo M04: dots are crisp |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.002 | 0.03 | Derived: dots 17 mm across, 154 per m2 over 0.32 m x 1 to 2.5 m |
  | peak_mask | mask_max | mask | `{}` | 0.7 | 1.0 | Judgement |
  | nn_ratio | nn_ratio | mask | `{"thr": 0.5, "min_area_mm2": 50, "area": "hull"}` | 0.7 | 1.4 | Judgement (reviewer 8 October): dots are scattered, not on a lattice; hull area, so the edge effect lifts R a little |
  | size_cv | size_cv | mask | `{"thr": 0.5, "min_area_mm2": 50}` | 0.25 | 1.5 | Photo M04 (10.6 / 16.9 / 29.4 mm: CV 0.4) |

### `road_blot`: Oil blots and smears, and broad dark patches on the road

- **Layer:** L2 ground (virtual texture)
- **Where (the rule):** Two tiers. Dark blots 0.10 to 0.20 m, black, irregular, 1 to 3 per standing place (the Hook sheet's black blots beside the yellow lines); broad low-contrast patches 0.15 to 0.5 m (median 0.22 m), 0.4 to 1.0 per m2 of trafficked carriageway, 3 to 6 L* darker than the road around (Photo M02); strongest in the wheel paths (two bands 0.15 m wide, 1.5 m apart, along each lane).
  - Feature: standing places (the rank, loading aprons, the private places), where lorries stop, the first metre beyond a gully grate (x 12)
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Both; the rank (east, x 3 to 9) 1.5; the loading aprons (east x 9 to 15 and x 40 to 46) 1.3
  - Footfall and wet: Traffic; wet: dark blots read as shiny black; the broad patches nearly vanish (wet asphalt is dark everywhere).
  - Density: 1 to 3 dark blots per standing place (typical 2) [Sheet M20 (dark blots), Photo M02 (broad patches: 100 per 100 m2 at dL* 2.5, 41 at dL* 4)]
  - Density tiers: `{"dark blots 0.10 to 0.20 m, per standing place": [1, 3], "broad low-contrast patches 0.15 to 0.5 m, per m2 of trafficked road": [0.4, 1.0]}`
- **Decal frame:** x -0.6 to 0.6 m, y -0.6 to 0.6 m; origin: origin = the middle of the blot group
- **Shape and size (real units):** envelope primitive `blob_field`; envelope parameters `{"region_m": [1.0, 1.0], "anchor": "centre", "blobs": {"n": [1, 3], "eqd_m": [0.1, 0.2, 0.45], "aspect": [1.0, 2.2], "orient": "free"}}`
  - Geometry numbers: `{"blob_eqd_mm": {"p10": 100, "p50": 200, "p90": 450, "src": "Sheet M20 (0.10 to 0.20 m) and Photo M02 (p10 160, p50 223, p90 487 mm at dL 2.5)"}, "edge_10_90_mm": [10, 60], "edge_src": "Photo M02 (the whole-tile mark edge is soft, about 70 mm); Sheet M20 blots ragged but crisp: 10 to 25 mm", "edge_for_envelope_mm": 20}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [89, 86, 80] | [67, 64, 63] | black-grey, glossy | 0.56 | -9 | Sheet M20 (road blots read black on a grey road) is wet: wet 0.50 = dry 0.56 x 0.90 (the wet multiplier below); Photo M02 for the paler broad patches (0.85 to 0.9 at the low tier) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.25}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.45, "note": "against wet stone (0.45) the blot is a slick: roughness 0.1 to 0.15"}`. [Read WET-ROAD + Judgement]
- **Texel scale:** smallest feature 40 mm; mask needs at least 250 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 5 seeded masks; they differ by single blot, double blot, smear (aspect 2), ring of small blots, one broad pale patch; free yaw [Derived]
- **Why 1990 Britain:** Oil and brake-dust blots under standing vehicles are normal on any 1990 carriageway (Judgement).
- **Not modern, not American:** No spill-kit absorbent granules; no fresh clean black-top.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 5000}` | 120 | 450 | Sheet M20, Photo M02 |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 8 | 70 | Sheet M20, Photo M02 |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.02 | 0.35 | Derived: 1 to 3 blots 0.1 to 0.45 m across in 1.2 x 1.2 m |
  | peak_mask | mask_max | mask | `{}` | 0.6 | 1.0 | Judgement |

### `tyre_scuff`: Tyre scuffs on arcs, and wheel-path polish

- **Layer:** L2 ground (virtual texture)
- **Where (the rule):** Long soft arcs: one scuff 1.7 to 8.6 m long (the stamp holds 1.7 to 2.8 m; chain stamps for more), 0.09 m wide at half depth, soft edges (10 to 90 % about 70 mm), 4 to 9 L* darker at the centre line; 1 to 2 per junction mouth, 0.05 to 0.15 per metre of kerb elsewhere; curving toward the direction vehicles turn.
  - Feature: the yard entrance (x 21 to 24, the only junction mouth) and the quay-end corner (x 0 to 9), the kerb where vehicles pull in, the rank's pull-up
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Both kerbs; the quay-end corner 1.5
  - Footfall and wet: Traffic; wet: the scuff vanishes into the wet dark road.
  - Density: 1 to 2 scuffs per junction mouth (typical 1.5) [Photo M02 (16 linear marks per 900 m2 of open asphalt = 1.8 per 100 m2); Judgement for a junction]
- **Decal frame:** x -1.5 to 1.5 m, y -0.5 to 0.5 m; origin: origin = the middle of the arc; x along the chord
- **Shape and size (real units):** envelope primitive `scuff_arc`; envelope parameters `{"length_m": [1.7, 2.8], "width_mm": 90, "full_length_m_photo": [1.7, 8.6]}`
  - Geometry numbers: `{"fwhm_mm": {"v": 90, "tol": 15, "src": "Photo M02 (16 features, cross-profile, 7.3 mm/px)"}, "length_m": {"photo": [1.7, 8.6], "p50_photo": 4.0, "stamp": [1.7, 2.8], "src": "Photo M02"}, "edge_10_90_mm": [45, 120], "edge_src": "Photo M02: 10 to 90 % about 70 mm +/-20", "peak_dL": {"typical": [-9.5, -4], "src": "Photo M02 (selection-biased)"}, "edge_for_envelope_mm": 6}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [89, 86, 80] | [78, 74, 73] | darker road | 0.75 | -5 | Photo M02: scuff deepest -9.5 L* (selection-biased; typical -4 to -9) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0, "note": "no change: the scuff is invisible on wet asphalt (strength x 0.3)"}`. [Judgement]
- **Texel scale:** smallest feature 90 mm; mask needs at least 100 px/m, use 150; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: soft 70 mm edges: 150 px/m is enough
- **Variants:** 4 seeded masks; they differ by arc radius 2, 3, 5 m and one near-straight; mirror in x [Derived]
- **Why 1990 Britain:** Rubber scuffs from turning vehicles are the same in any decade (Judgement); straight skid pairs from locked wheels are the pre-ABS mark and may appear 0 to 1 at the quay-end corner.
- **Not modern, not American:** No 'wheelie' donuts. Straight locked-wheel skid pairs are the period-correct mark (most 1990 cars had no ABS), but they are out of scope for this stamp: at most 0 to 1 faint straight pair at the quay-end corner, as a second variant; never call it modern.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | streak_length_m_p50 | streak_length_m | mask | `{"thr": 0.3, "stat": "p50"}` | 1.2 | 3.2 | Photo M02 (stamp holds 1.7 to 2.8 m) |
  | streak_aspect_p50 | streak_aspect | mask | `{"thr": 0.3, "min_length_m": 0.5, "stat": "p50"}` | 5 | 60 | Photo M02: 90 mm wide, 1.7 to 8.6 m long (an arc's rod-equivalent length is shorter than its arc length) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "reach_mm": 250}` | 45 | 120 | Photo M02: 70 mm +/- 20 |
  | peak_mask | mask_max | mask | `{}` | 0.6 | 0.8 | Derived: five-to-ten nested soft ribbons |

### `road_patch`: Patched asphalt: trench and cover reinstatements

- **Layer:** L2 ground (virtual texture) with a 2 to 12 mm height step
- **Where (the rule):** Reinstatement: a rectangle 0.5 to 1.2 m wide, 1.0 to 6.0 m long (trench) or 0.9 to 1.2 m square (cover), edges 30 to 50 mm dark seam with grass or weed at corners; slightly darker and smoother, or paler and rougher, than the old surface; 1 to 3 along the 48 m street.
  - Feature: carriageway: trench reinstatements across the lane and along the channel, round covers and gully grates, pothole patches
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Both lanes; the channel strip along the kerb more often
  - Footfall and wet: Traffic: wheel paths; wet: seams hold water and read black
  - Density: 1 to 3 per 48 m street (typical 2) [Photo M05; Judgement]
- **Decal frame:** x -0.9 to 0.9 m, y -0.9 to 0.9 m; origin: origin = patch centre; the seam is the ring
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.9, 1.2], [0.9, 1.2]], "ragged_mm": [20, 60], "seam_mm": [30, 50], "infill_level": 0.23}`
  - Geometry numbers: `{"cover_reinstatement_m": {"w": 1.0, "h": 1.1, "tol": 0.1, "src": "Photo M05 (ortho 3 mm/px)"}, "seam_mm": [30, 50], "seam_src": "Photo M05", "edge_10_90_mm": [5, 25], "edge_src": "Photo M05", "infill": {"luminance_ratio": 0.93, "mask_level": 0.23, "src": "Photo M05: infill 132/122/120 against road 139/127/123 (Y ratio 0.92)"}, "seam_ratio": {"range": [0.63, 0.77], "src": "Photo M05 (two measurers)"}, "edge_for_envelope_mm": 15}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [89, 86, 80] | [78, 71, 66] | dark brown-shifted seam | 0.7 | -6 | Photo M05 (re-measured): the seam reads 0.63 to 0.77 of the road, brown-shifted 125/110/103 on 138/126/123; the first pass's 'about 0.5' was not a measurement. The infill is 0.93 of the road (M05): mask level 0.23 x (1 - 0.70) = 0.07 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.1}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.35, "note": "seam is a gutter; water collects and reflects as a thin dark line"}`. [Read WET-ROAD + Judgement]
- **Texel scale:** smallest feature 30 mm; mask needs at least 250 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: the seam is 30 to 50 mm wide: 400 px/m gives 12 to 20 texels
- **Variants:** 5 seeded masks; they differ by cover reinstatement square, trench across lane, trench along channel, pothole patch, patch with weeds at the corners; free yaw within +/-15 degrees of the street axis [Derived]
- **Why 1990 Britain:** Utility reinstatements with a bitumen seam and no hot-rolled infill are the normal state of an old-quarter street (Judgement). Coloured anti-skid surfacing and thermoplastic patches are not part of this street.
- **Not modern, not American:** No red or green anti-skid; no uniform black new surface; no spray-painted utility markings (white, blue or pink).
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | patch_eqd_mm | blob_eqd_mm | mask | `{"thr": 0.2, "stat": "p50", "min_area_mm2": 100000}` | 800 | 1500 | Photo M05 (1.0 x 1.1 m cover): infill counted at 0.2 |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 3 | 40 | Photo M05 |
  | coverage_of_frame | coverage | mask | `{"thr": 0.2}` | 0.25 | 0.6 | Derived: a 0.9 to 1.2 m patch in a 1.8 x 1.8 m frame (infill counted at 0.2) |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived: the seam is level 1 |

### `road_crack`: Cracks in the asphalt: a sealed main crack and hairlines

- **Layer:** L2 ground (virtual texture) with a 1 to 4 mm height groove
- **Where (the rule):** A cracked section: one sealed main crack 1.6 to 2.4 m long, 15 to 60 mm wide (p50 35 mm; tar overband), running roughly along or across the lane; 2 to 5 hairlines 2 to 6 mm wide, 0.3 to 1.2 m long, branching at 12 to 25 degrees. In the worst stretches 0.8 m of crack per m2 (Photo M03); typical road 0.1 to 0.4 m per m2 (Judgement), so place the stamp sparsely: about 1 per 10 to 20 m of carriageway.
  - Feature: carriageway: the worst stretches near the channel and the crown, along trench edges, round covers; sealed cracks along old joints
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Both lanes; the channel strip along the kerb more cracked
  - Footfall and wet: Traffic and frost: wet: cracks hold water and read black
  - Density: 2 to 5 stamps per 48 m street (typical 3) [Judgement; Photo M03 for the stamp's own content (0.8 m per m2)]
- **Decal frame:** x -1.5 to 1.5 m, y -1.5 to 1.5 m; origin: origin = the middle of the cracked section; the main crack runs roughly vertically (along the lane)
- **Shape and size (real units):** envelope primitive `crack_lines`; envelope parameters `{"region_m": [2.5, 2.5], "note": "the cracked section is 2.5 x 2.5 m (0.8 m per m2, Photo M03); the decal frame is 3 x 3 m", "main": {"length_m": [1.6, 2.4], "width_mm": [15, 60]}, "hairlines": {"n": [2, 5], "length_m": [0.3, 1.2], "width_mm": [2, 6], "branch_prob": 0.3, "step_m": 0.03}}`
  - Geometry numbers: `{"crack_length_m_per_m2": {"worst": 0.8, "tol": 0.25, "typical": [0.1, 0.4], "src": "Photo M03 (counted by eye, 7.3 m in 9 m2)"}, "main_crack_width_mm": {"p10": 15, "p50": 35, "p90": 60, "src": "Photo M03 re-measured on the full 2k scan: per-row widths below 0.7 of the surface 15 / 35 / 59 mm (p10 / p50 / p90); the first pass's 40 to 90 mm was read by eye"}, "hairline_width_mm": [2, 6], "edge_10_90_mm": [1, 12], "edge_src": "Photo M03: hairlines are crisp, the sealed band's edge a few mm soft", "edge_for_envelope_mm": 2}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [89, 86, 80] | [43, 42, 41] | black sealed crack | 0.25 | -19 | Photo M03: the crack core is Y 0.021 on a surface of 0.092 (L* 15.8 smoothed at 3 mm, 13 raw, on L* 36.3): ratio 0.23 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.1}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.4, "note": "cracks hold water: roughness 0.04 in the groove"}`. [Read WET-ROAD (water 0.04) + Judgement]
- **Texel scale:** smallest feature 3 mm; mask needs at least 800 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: hairlines need 1120 px/m; fade the stamp's hairlines out by 8 m (LOD), keep the sealed main crack
- **Variants:** 5 seeded masks; they differ by main crack along the lane, across the lane, curved, with a branch, hairline-only [Derived]
- **Why 1990 Britain:** Sealed bitumen cracks and hairlines on worn road asphalt are the same in any decade (Judgement).
- **Not modern, not American:** No perfectly straight computer cracks, no pothole with square edges.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | crack_length_m_per_m2_of_frame | crack_length_per_m2 | mask | `{"thr": 0.5}` | 0.3 | 1.2 | Photo M03: 0.8 in the 2.5 x 2.5 m section, diluted by the 3 x 3 m frame |
  | crack_width_mm | crack_width_mm | mask | `{"thr": 0.5}` | 2 | 40 | Photo M03: hairlines 2 to 6 mm, main 15 to 60 mm; the median lies between |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 1 | 15 | Photo M03 |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived: cracks are level 1 |

### `gutter_grime`: Channel, kerb-foot and gully grime; the channel is lighter than the road

- **Layer:** L2 ground (virtual texture) plus L0 kerb material
- **Where (the rule):** Photo M24 (dry): the channel setts read 1.4 x the open road's luminance and the asphalt 0 to 0.6 m off the kerb 0.95 x the open road, so the channel is LIGHTER than the road and the fringe barely darker. Channel body: x 0.85 (mask 0.23). Asphalt fringe 0.255 to 0.55 m, ragged: x 0.92 at most (mask 0.12 at the edge falling to 0). The darkest grime is two lines 20 to 40 mm wide in the kerb-channel and channel-asphalt joints (x 0.35, mask 1.0). Gully piles (grit, leaf mulch, litter): 0.4 m radius, mask 0.8, colour 70/62/52, at the gully (x 12) and one more per 20 m. Weeds in the channel: 0.05 to 0.15 m across, 1 per 6 to 10 m in the open stretches. Kerb-face tyre scuff: a pale polished streak +8 L*, 0.05 to 0.12 m up the face, 0.3 to 1.5 m long, 1 per 10 m of kerb. One surface per decal: the channel rows use channel_concrete, the fringe asphalt_dry, the kerb face kerb_granite (split at the joint).
  - Feature: the kerb channel course (0.255 m wide, SCENE-SLOTS, in the kerb's own concrete), the joints either side of it, the strip of asphalt 0.3 m beyond it, the kerb face, gully grates (x 12)
  - Surfaces: channel_concrete, asphalt_dry, kerb_granite
  - Height: ground to 0.125 (kerb upstand); the mask's y runs from the kerb foot into the carriageway
  - Sides: Both kerbs; the west side's dropped crossover (x 21 to 24, centre 22.5) is cleaner (strength 0.5) but has a scuffed taper block
  - Footfall and wet: Wet climate and runoff: the channel is where the street's dirt goes; wet it reads as a darker, glossy gutter line (the sheet's strip between the inner yellow line and the kerb reads about 0.7 of the road, wet).
  - Density: 1.0 to 1.0 continuous along the kerb (typical 1.0) [Photo M24; Judgement for piles, weeds and scuffs]
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 0.75 m; origin: origin = the kerb foot; y runs from the kerb foot into the carriageway (channel 0 to 0.255 m, fringe to 0.58 m); tiles along x
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.03, "level": 1.0}, {"h_m": 0.05, "level": 0.23}, {"h_m": 0.235, "level": 0.23}, {"h_m": 0.26, "level": 1.0}, {"h_m": 0.28, "level": 0.12}, {"h_m": 0.45, "level": 0.09}, {"h_m": 0.58, "level": 0.0}], "top_edge": {"step_m": 0.0, "amplitude_m": [0.06, 0.16], "wavelength_m": [0.3, 0.8], "ragged_from_m": 0.28}, "joint_lines_mm": [20, 40], "fingers": {"n_per_m": 1.0, "length_m": [0.05, 0.2], "width_m": [0.03, 0.12]}}`
  - Geometry numbers: `{"band_width_m": {"channel": 0.255, "fringe": [0.1, 0.3], "src": "SCENE-SLOTS channel course 0.255 m; Photo M06 kerb litter band 0.3 m"}, "height_profile": {"h_m": [0.0, 0.03, 0.05, 0.235, 0.26, 0.28, 0.45, 0.58], "mask": [1.0, 1.0, 0.23, 0.23, 1.0, 0.12, 0.09, 0.0], "src": "Photo M24: channel body x 0.85, joints x 0.35, fringe x 0.92 at its darkest; axis here is distance from the kerb foot"}, "profile_tolerance": 0.15, "edge_10_90_mm": [15, 300], "edge_src": "Judgement: the joint lines are hard (about 25 mm), the grime fades into the asphalt over the fringe (0.12 at 0.28 m to 0 at 0.58 m)", "tileable": "along the kerb, 2.0 m period", "top_edge_std_mm": {"range": [20, 70], "level": 0.06, "src": "Judgement (reviewer 8 October)"}, "multiplier_note": "mask level m on a surface gives 1 - m x 0.65: 0.23 = x 0.85, 0.12 = x 0.92, 1.0 = x 0.35", "pile": {"radius_m": 0.4, "mask": 0.8, "srgb": [70, 62, 52], "src": "Judgement (reviewer 8 October)"}, "weeds": {"across_m": [0.05, 0.15], "per_m_of_kerb": [0.1, 0.17], "src": "Judgement (reviewer 8 October); Photo M24 shows a weed at the kerb foot"}, "kerb_scuff": {"delta_L_star": 8, "srgb": [147, 145, 141], "up_m": [0.05, 0.12], "length_m": [0.3, 1.5], "per_10_m": 1, "note": "a replacing mark: the kerb_granite 128/126/122 moved +8 L*", "src": "Judgement (reviewer 8 October)"}, "edge_for_envelope_mm": 12}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | channel_concrete | [116, 111, 108] | [71, 67, 63] | dark grit and film on the channel | 0.35 | -19 | Photo M24: the channel reads 1.4 x the road after its grime; at mask 1 (the joint lines) x 0.35 (reviewer 8 October), body mask 0.23 = x 0.85 |
  | asphalt_dry | [89, 86, 80] | [53, 50, 48] | black grit and mulch | 0.35 | -16 | Judgement; Photo M24: the fringe reads 0.95 of the open road dry (mask <= 0.12 = x 0.92 or better); Sheet: grimed channel and drain covers |
  | kerb_granite | [128, 126, 122] | [100, 95, 86] | dark grey | 0.55 | -12 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.55, "note": "the channel is a darker glossy line; roughness 0.04 in standing water"}`. [Read WET-ROAD (water 0.04); Judgement]
- **Texel scale:** smallest feature 25 mm; mask needs at least 300 px/m, use 500; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by fringe noise seed (4 seeds); tile along the kerb. The gully piles, weeds and kerb-face scuffs of the rule are separate small stamps placed by the rule (their numbers are in the geometry), not part of the tile [Derived]
- **Why 1990 Britain:** Channels were swept rarely; cast-iron gully grates with silt traps; weeds. No mechanical-sweeper streak patterns (2000s). The kerb-course concrete reads lighter than the road in any decade (Photo M24, scene note).
- **Not modern, not American:** No uniform dark band darker than the road; no sharp yellow-line edge exactly on the channel line unless the lines family says so.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | foot_profile | foot_profile | mask | `{"points": [[0.12, 0.15, 0.32], [0.2, 0.15, 0.32], [0.3, 0.03, 0.2], [0.45, 0.0, 0.14], [0.65, 0.0, 0.05]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Photo M24 (levels), Derived |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 300}` | 15 | 300 | Judgement: the joint lines are hard (20 to 40 mm wide, about 25 mm for 10 to 90 %), the fringe fades 0.12 to 0 over 0.3 m |
  | top_edge_std_mm | top_edge_std_mm | mask | `{"thr": 0.06, "source": "bottom"}` | 20 | 70 | Judgement (reviewer 8 October) |
  | column_mean_cv | column_mean_cv | mask | `{"source": "bottom", "from_m": 0.3, "to_m": 0.6}` | 0.08 | 2.0 | Judgement (reviewer 8 October) |
  | channel_over_road | channel_over_road | composition | `{"surface": "channel_concrete"}` | 1.15 | 1.8 | Photo M24: 1.4 (1.35 to 1.7); reviewer's floor 1.15 |
  | fringe_over_road | fringe_over_road | composition | `{"surface": "asphalt_dry"}` | 0.85 | 0.99 | Photo M24: 0.95 (0.91 to 0.97) |

### `wall_soot`: Facade-wide soot: the sooted wall body, its metre-scale mottle and the darker lower wall

- **Layer:** L0 in the brick and render materials: one seamless tile per house, strength by the house's state; replaces the recipe's patch noise and the house look's brightness (section 1)
- **Where (the rule):** Strength by state: sooted 1.0, as built 0.35, cleaned 0.0 (Judgement; the Hook sheet's near walls read as built). At strength 1 the albedo multiplier is 0.42 with the per-channel tint of Photo M21 (sooted 92/81/73 against cleaner 146/129/110: linear ratios 0.37 / 0.37 / 0.43), luminance 0.377 of the cleaner panel in one measurement and 0.37 to 0.48 in two, colour saturation 0.84 of the cleaner panel (HSV; the sheet's head reads 0.65). The mask is a metre-scale mottle (wavelength 0.5 to 2.0 m, std 0.07) around a mean level 0.90, plus the darker lower wall: the level rises by 0.10 below 0.7 m and is back to the body by 1.2 m, which is x 0.88 on the wall above (Sheet M22b, lower wall about x 0.90 over 0.3 to 0.7 m up on the right-hand cottage). The mask is for the whole wall including above 4 m (the builder repeats the 4 m row).
  - Feature: every brick, painted-brick and render wall surface of a house from the pavement to the wall head; one state per house: sooted, as built, or cleaned in the 1980s (the existing brick_set 1, 0, 2 of street-wear.json)
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0 to the wall head; the lower-wall rise 0 to 1.2 m
  - Sides: Both sides; the state, not the side, decides (east parade 1.0, west block 1.0): house states are sooted 7, as built 4, cleaned 2 of 13 (street-wear.json brick_set 1, 0, 2)
  - Footfall and wet: Not footfall: deposit from coal smoke and traffic on uncleaned brick (Judgement; Photo M21 proves the state survives in 2019). Wet: the sooted wall reads a little darker.
  - Density: 0.3 to 0.6 share of houses in the sooted state (typical 0.54) [Derived: street-wear.json gives 7 of 13 houses brick_set 1 (HOUSE_SET_FACTOR 'sooted'); the other 6 are as built (4) or cleaned (2)]
  - With house wear: strength = state weight; the house wear (0.55 to 1.0) scales the mottle's contrast, not the state
- **Decal frame:** x 0.0 to 4.0 m, y 0.0 to 4.0 m; origin: origin = the pavement line at the left end of a 4.0 m tile; y up the wall to 4.0 m (the builder repeats the 4.0 m row above); tiles in x
- **Shape and size (real units):** envelope primitive `soot_wall`; envelope parameters `{"tile_m": [4.0, 4.0], "mean_level": 0.9, "mottle_std": 0.07, "wavelength_m": [0.5, 2.0], "lower_wall": {"full_to_m": 0.7, "zero_at_m": 1.2, "extra_level": 0.1, "src": "Sheet M22b"}}`
  - Geometry numbers: `{"mottle_wavelength_m": [0.5, 2.0], "mask_std": [0.04, 0.14], "mean_level": 0.9, "tint_linear_ratio": [0.372, 0.375, 0.427], "multiplier": 0.42, "sooted_over_cleaner": {"photo_M21": [0.377, 0.48], "chosen": 0.42, "src": "Photo M21 (two measurements 0.377 and 0.37 to 0.48); the recipe's HOUSE_LOOKS sooted look is about 0.57, lighter than the photograph"}, "saturation_ratio": {"photo_M21": 0.84, "sheet_M22": 0.65, "src": "Photo M21 (the review's 0.6 is not what the photograph measures: 0.21 against 0.25 in HSV saturation)"}, "lower_wall_ratio": {"measured": 0.9, "composed": 0.88, "src": "Sheet M22b measured 0.90 (0.3 to 0.7 m up); the review's 0.85 was Judgement"}, "edge_10_90_mm": [300, 2000], "edge_src": "Judgement: a broad mottle", "tileable": "horizontally, seamless, 4.0 m period; vertical profile fixed (rows from the pavement up)", "edge_for_envelope_mm": 100}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [93, 56, 48] | soot grey-brown | 0.42 | -15 | Photo M21: sooted stock brick 92/81/73 against 146/129/110, luminance 0.377 (0.37 to 0.48), per-channel ratios kept; dry photograph |
  | brick_painted | [152, 108, 93] | [101, 71, 65] | soot grey-pink | 0.42 | -17 | Photo M21 ratios on a painted surface; Judgement |
  | render_cream | [214, 200, 178] | [144, 135, 127] | soot grey-cream | 0.42 | -24 | Photo M21 ratios on a render surface; Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.1, "note": "a sooted wall reads a little darker when wet"}`. [Judgement; M21 is a dry photograph]
- **Texel scale:** smallest feature 300 mm; mask needs at least 12 px/m, use 25; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: tile 4 m x 4 m at 25 px/m = 100 x 100; the lower-wall rise needs 25 px/m at least
- **Variants:** 4 seeded masks; they differ by mottle seed; mirror in x; the state (strength) comes from the house, not the variant [Derived]
- **Why 1990 Britain:** Soot on uncleaned brick was normal in a coal-and-traffic town; stone and brick cleaning of fronts in the 1980s produced the cleaned state (Judgement, from memory: no 1990 photograph reached). Photo M21 shows a sooted panel beside a cleaner one in 2019, so the state survives long after the coal fires.
- **Not modern, not American:** No uniform clean brick on every house; no even grey wash; soot is patchy in metre-sized areas and darker at the foot.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | mask_mean | mask_mean | mask | `{}` | 0.82 | 0.97 | Derived: mean level 0.90 plus the lower-wall rise over 4 m |
  | mask_std | mask_std | mask | `{}` | 0.04 | 0.14 | Judgement: mottle std 0.07 plus the lower-wall rise |
  | mask_max | mask_max | mask | `{}` | 0.95 | 1.0 | Derived: 0.90 + 0.10 at the foot |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | dominant_wavelength_m | dominant_wavelength_m | mask | `{}` | 0.5 | 4.0 | Judgement: mottle wavelength 0.5 to 2.0 m on a 4 m tile (the tile's own fundamental is 4 m) |
  | foot_profile | foot_profile | mask | `{"points": [[0.2, 0.85, 1.0], [0.5, 0.85, 1.0], [1.6, 0.7, 0.97], [3.0, 0.7, 0.97]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Sheet M22b (lower wall) and Photo M21 |
  | composed_soot_ratio | composed_soot_ratio | composition | `{}` | 0.35 | 0.55 | Photo M21 (0.377 to 0.48): the composed brick of a sooted house over the cleaned one, wall above 2 m |

### `wall_head_band`: The dark head under eaves, verges, copings and string courses

- **Layer:** L0 in the brick and render materials, hung from each feature's lower edge by the distance below it (a 2.0 m seamless-in-x strip); ragged by brick courses
- **Where (the rule):** Multiplier at mask 1: 0.56 on a wall that is as built or cleaned (Sheet M22, wet 0.50 to 0.62 over the top 0.2 to 0.75 m of the gable, divided by the wet 0.90), and 0.80 on a sooted wall (Photo M21: a further x 0.80 under the coping of the sooted panel; the soot already carries the common darkening, so nothing is darkened twice). Depth profile by distance below the feature: 1.0 to 0.2 m, 0.85 at 0.4 m, 0.70 at 0.6 m, 0.38 at 0.75 m, 0.20 at 0.95 m, 0 by 1.15 m (Sheet M22: 0.75 to 0.80 at 0.9 to 1.2 m, 1.0 by 1.4 m wet) for a gable verge or eaves gutter; a coping or string course takes the same profile scaled by 0.3 in depth (Photo M21: a band 0.4 m deep). The lower edge is ragged by courses: 75 mm steps, its standard deviation along x 20 to 100 mm. It REPLACES the recipe's head water paths (STREAK_DEPTH, section 1).
  - Feature: the lower edge of every eaves gutter, gable verge and barge, chimney-stack and parapet coping, and string course on a brick, painted-brick or render wall; not under a window sill (streak_sill)
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0 to 1.15 below the feature (0 to 0.35 below a coping or string course)
  - Sides: Both sides; gables facing the street 1.0, the east parade 1.0, the west block 0.9
  - Footfall and wet: Wet climate: roof run-off and the gutter's overflow wash the head; the Hook sheet's gable and the right-hand cottage both show it.
  - Density: 1.0 to 1.0 share of each eaves, verge, coping and string-course length (typical 1.0) [Sheet M22 (gable verge), Photo M21 (coping): continuous, not fingers]
  - With house wear: strength x wear; depth x (0.8 + 0.2 x wear)
- **Decal frame:** x 0.0 to 2.0 m, y -1.5 to 0.0 m; origin: origin = the feature's lower edge at the left end of a 2.0 m tile; y runs DOWN the wall (negative); tiles in x
- **Shape and size (real units):** envelope primitive `head_band`; envelope parameters `{"levels": [{"h_m": 0.2, "level": 1.0}, {"h_m": 0.4, "level": 0.85}, {"h_m": 0.6, "level": 0.7}, {"h_m": 0.75, "level": 0.38}, {"h_m": 0.95, "level": 0.2}, {"h_m": 1.15, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.12, 0.3], "wavelength_m": [0.3, 0.7], "src": "Judgement: ragged by courses (peak excursion of the noise before it is rounded to 75 mm steps; the edge's standard deviation comes out at 20 to 100 mm)"}, "depth_scale": {"gable_verge_or_eaves": 1.0, "coping_or_string_course": 0.3}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.2, 0.4, 0.6, 0.75, 0.95, 1.15], "mask": [1.0, 1.0, 0.85, 0.7, 0.38, 0.2, 0.0], "src": "Sheet M22 (wet ratios 0.50 at 0.0 to 0.2 m, 0.56 at 0.34 to 0.48, 0.62 at 0.61, 0.75 at 0.75, 0.80 at 0.88 to 1.0, 0.945 at 1.16, 1.0 at 1.4 m) divided by the wet 0.90 and inverted through the dry 0.56; 'distance below' is the axis here"}, "profile_tolerance": 0.2, "edge_10_90_mm": [300, 900], "edge_src": "Sheet M22: the whole fall-off from 0.3 to 1.05 m", "ragged_step_mm": [30, 120], "multiplier": {"as_built_or_cleaned": 0.56, "sooted": 0.8, "src": "Sheet M22 / Photo M21"}, "top_edge_std_mm": {"range": [20, 100], "level": 0.5, "src": "Judgement"}, "tileable": "horizontally, seamless, 2.0 m period", "edge_for_envelope_mm": 100}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [101, 68, 57] | dark brown head | 0.56 | -10 | Sheet M22 (wet 0.50 to 0.62) divided by the wet 0.90; Photo M21 0.80 on the sooted state (by_house_state) |
  | brick_painted | [152, 108, 93] | [116, 88, 77] | dirty pink-brown head | 0.62 | -10 | Judgement |
  | render_cream | [214, 200, 178] | [180, 160, 135] | dirty cream head | 0.62 | -14 | Judgement |

  - House-state multipliers at mask 1 (the brick_red row is the as-built value; the sooted wall already carries the common darkening): as built 0.56, cleaned 0.56, sooted 0.8 [Sheet M22 on a wall that is not sooted; Photo M21 on the sooted panel].
- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.1, "note": "the sheet is wet: dry = sheet ratio / 0.90"}`. [Sheet M22 (wet); Photo M21 (dry)]
- **Texel scale:** smallest feature 75 mm; mask needs at least 100 px/m, use 160; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: tile 2.0 m x 1.5 m at 160 px/m = 320 x 240; the 75 mm course step is 12 texels
- **Variants:** 4 seeded masks; they differ by ragged-edge seed (course steps), the depth scale (verge, coping); mirror in x; tile in x [Derived]
- **Why 1990 Britain:** A dark head under the roof edge is run-off and dirt on uncleaned brick (Judgement; the Hook sheet shows it on the left gable and the right-hand cottage). A cleaned or newly painted front has less of it.
- **Not modern, not American:** No clean wall to the roof edge; no ruler-straight lower edge; no head band without the roof edge it hangs from.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | composed_head_ratio | composed_head_ratio | composition | `{"state": "cleaned"}` | 0.45 | 0.65 | Sheet M22 (wet 0.50 to 0.62, dry 0.56): the head 0.1 m below the feature on a cleaned house |
  | composed_head_ratio_sooted | composed_head_ratio | composition | `{"state": "sooted"}` | 0.28 | 0.48 | Photo M21: x 0.80 on the sooted wall's x 0.48: no darker than the floor |
  | foot_profile | foot_profile | mask | `{"points": [[0.1, 0.85, 1.0], [0.5, 0.55, 0.9], [0.9, 0.05, 0.35], [1.3, 0.0, 0.05]], "axis": "rows_from_top"}` | 0.0 | 1.0 | Sheet M22 (inverted): distance below the feature |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 900}` | 300 | 900 | Sheet M22: the whole fall-off |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | peak_mask | mask_max | mask | `{}` | 0.95 | 1.0 | Derived |
  | top_edge_std_mm | top_edge_std_mm | mask | `{"thr": 0.5, "source": "top"}` | 20 | 100 | Judgement (reviewer 8 October): ragged by courses |
  | column_mean_cv | column_mean_cv | mask | `{"source": "top", "from_m": 0.3, "to_m": 1.15}` | 0.08 | 1.0 | Judgement (reviewer 8 October) |

### `iron_wear`: Paint loss and rust on downpipes, railings, hopper heads and bollards

- **Layer:** L0 in the iron material (the patches) plus L1 at collars (the streaks)
- **Where (the rule):** Paint loss and rust over 4 to 8 % of the length or area, in patches of 20 to 110 mm (p50 45 mm, Sheet M25), 40 % of them in the lowest 0.3 m (the shoe), 30 % within 0.08 m of a collar or bracket, 30 % anywhere. Below 4 in 10 collars a rust streak: width p50 24 mm, aspect 4 to 12, 0.10 to 0.30 m long, 16 mm edges (Photo M13). The patch colour is a pale ochre, 141/102/72 on the wet sheet's near-black paint 50/40/37 (Sheet M25), 152/110/78 dry.
  - Feature: downpipes (68 mm round, vignette-scene.json), hopper heads, the guard-railing panel (x 10 to 12), bollards (x 20.7 and 24.3), lamp-column bases, pillar box, letter-box and bracket ironwork
  - Surfaces: iron_black
  - Height: 0 to 2.4 m of a downpipe from the pavement, then the same rule on the first-floor pipe
  - Sides: East parade (wet) 1.0; west block 0.8; the gable downpipe at the quay end (the sheet's) is the hero reference
  - Footfall and wet: Splash and knocks at the foot (boots, trolleys); wet: collars and joints where water lies.
  - Density: 0.04 to 0.08 share of the pipe's area lost to paint (typical 0.06) [Sheet M25: 4.8 % of the pipe length at a strict threshold, 7 % by the reviewer's]
- **Decal frame:** x -0.04 to 0.04 m, y 0.0 to 2.4 m; origin: origin = the foot of the pipe (the shoe) on the pavement, x = the pipe's centre line; y up the pipe
- **Shape and size (real units):** envelope primitive `iron_set`; envelope parameters `{"pipe_width_m": 0.075, "length_m": 2.4, "collars_m": [0.6, 1.5, 2.3], "patch_share": [0.04, 0.08], "patch_eqd_mm": [20, 45, 110], "placement": {"foot_lowest_0.3m": 0.4, "collar_within_0.08m": 0.3, "anywhere": 0.3}, "streaks": {"prob_per_collar": 0.4, "width_mm_lognormal": [14, 24, 40], "length_m": [0.1, 0.3]}}`
  - Geometry numbers: `{"patch_eqd_mm": {"p10": 20, "p50": 45, "p90": 110, "src": "Sheet M25 (patches 20 to 156 mm long on a 48 mm wide pipe, as pixels)"}, "streak_width_mm": {"p10": 14, "p50": 24, "p90": 40, "src": "Photo M13 (24 mm p50)"}, "edge_10_90_mm": [3, 25], "edge_src": "Photo M13 16 mm for the streaks; Judgement 3 mm for chipped paint", "edge_for_envelope_mm": 4}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | iron_black | [35, 35, 36] | [152, 110, 78] | pale ochre bare iron and rust bloom | 1.0 | 36 | Sheet M25 is wet: ochre 141/102/72 (the review) or 125/86/64 (this pass) on paint 45 to 50 / 33 to 40 / 26 to 37; dry = the review's 141/102/72 divided by the wet 0.85 in luminance = 152/110/78, used once; replaces, mixed at mask x 0.9 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.2, "note": "rust is darker and redder when wet; paint stays glossy"}`. [Judgement; Sheet M25 is wet]
- **Texel scale:** smallest feature 20 mm; mask needs at least 300 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: frame 0.08 m x 2.4 m at 400 px/m = 32 x 960
- **Variants:** 4 seeded masks; they differ by patch seed, collar streaks on/off, one pipe with a cracked shoe (foot cluster); no rotation (the pipe is vertical) [Derived]
- **Why 1990 Britain:** Cast-iron downpipes were repainted rarely; the paint loss and rust at the shoe and the joints is the normal state of an old-quarter pipe (Judgement; the Hook sheet shows it). Plastic downpipes are 1970s on and do not rust.
- **Not modern, not American:** No pristine black pipe on every house; no plastic-looking orange; no rust on stainless fixings.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.05 | 0.14 | Sheet M25 (4.8 to 7 % of the pipe lost) plus the streaks |
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 120}` | 20 | 90 | Sheet M25: patches 20 to 110 mm (on a 75 mm pipe neighbouring patches merge, so the measured median is a little above the drawn 45 mm) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 3 | 25 | Photo M13 / Judgement |
  | peak_mask | mask_max | mask | `{}` | 0.8 | 1.0 | Judgement |
  | foot_concentration | role_share_below | envelope | `{"role": "patch", "below_mm": 300, "of": "count"}` | 0.25 | 0.6 | Sheet M25 / Judgement: 40 % of the patches (by count, in quotas) are in the lowest 0.3 m |

### `grate_wear`: Rust and polish on gully and cellar grates

- **Layer:** L0 in the grate's iron material
- **Where (the rule):** Rust-brown in the slots' sides and recesses (mask 0.9), bar tops polished by wheels and feet (mask 0.1, darker grey), 6 to 12 rust flecks of 8 to 25 mm on the bar tops. The photograph's gully grate reads dull red-brown on its bars (125/109/103 on a tone-mapped view where the road is 114/114/120) with black slots (Photo M25).
  - Feature: the gully grate in the channel (0.40 m square, x 12.0), cellar and coal-hole grates in the footway (the sheet's left pavement), service-box lids
  - Surfaces: iron_grate
  - Height: ground
  - Sides: Both sides; the east gully (x 12) is the measured one
  - Footfall and wet: Wet and wheels: recesses hold water and silt; the bar tops are polished.
  - Density: 1.0 to 1.0 per grate (typical 1.0) [Derived: every grate]
- **Decal frame:** x 0.0 to 0.4 m, y 0.0 to 0.4 m; origin: origin = the grate's corner; a 0.4 m square; the slots run along y
- **Shape and size (real units):** envelope primitive `grate`; envelope parameters `{"size_m": 0.4, "strips": 16, "slot_level": 0.9, "bar_top_level": 0.1, "flecks": {"n": [6, 12], "eqd_mm": [8, 25], "level": 0.8}}`
  - Geometry numbers: `{"slot_mm": 25, "bar_mm": 25, "edge_10_90_mm": [1, 10], "edge_src": "geometry of the casting: hard edges (Photo M25)", "edge_for_envelope_mm": 2}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | iron_grate | [58, 54, 52] | [100, 72, 56] | dull rust-brown | 1.0 | 10 | Photo M25 (dull red-brown, R-B 22 on the photograph) and the sheet's rust red-brown (review); Judgement for the saturation: between the two |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.3, "note": "rust darker when wet; bar tops glint"}`. [Judgement]
- **Texel scale:** smallest feature 8 mm; mask needs at least 800 px/m, use 1000; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: 0.4 m square at 1000 px/m = 400 x 400
- **Variants:** 3 seeded masks; they differ by fleck seed, bar tops polished or rusted, one with a silt line along the slots; mirror allowed [Derived]
- **Why 1990 Britain:** Cast-iron grates with silt traps rusted and silted in any decade (Photo M25 is a 2019 photograph of one).
- **Not modern, not American:** No polymer or galvanised steel grates; no bright orange rust.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.35 | 0.7 | Derived: the slots are half the grate |
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 200}` | 50 | 160 | Derived: 8 slots 25 x 400 mm (eqd 113 mm) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 1 | 12 | Photo M25: hard edges |
  | peak_mask | mask_max | mask | `{}` | 0.85 | 1.0 | Judgement |

### `line_wear`: Worn double yellow and white lines: paint lost in cracks, gaps and chips

- **Layer:** L2 ground (virtual texture); the lines family's colour and geometry are the base, this mask is the loss
- **Where (the rule):** Photo M26: 22 % of the nominal 75 mm strip was lost (10 to 30 %: 8 gaps in 4 m, most about 15 mm, one about 0.5 m, plus ragged chips on both edges). Cross gaps the full width of the line, 1.2 to 2.4 per metre, lengths 20 / 60 / 300 mm (p10 / p50 / p90); edge chips 5 to 15 mm deep, 20 to 150 mm long, 3 to 8 per metre; specks 4 to 9 mm. The paint that remains is faded and filmed with dirt (the surface colour 195/168/100). The mask is the LOSS: 1 shows the road.
  - Feature: the two yellow bands of each kerb's double line (100 mm each, 100 mm apart, 0.25 m from the kerb face, vignette-scene.json) and the white dashed centre line; one instance per band, different seeds
  - Surfaces: line_yellow, line_white
  - Height: ground
  - Sides: Both kerbs' double yellows; heavier (x 1.3) where tyres run on them at the yard entrance (x 21 to 24) and the quay-end corner; the centre line is 0.7
  - Footfall and wet: Traffic and wet: tyres and grit wear the paint; wet the exposed road is dark, the paint stays bright.
  - Density: 0.1 to 0.3 share of the line lost (typical 0.18) [Photo M26 (22 +/- 8 %); reviewer 10 to 30 %]
- **Decal frame:** x 0.0 to 3.0 m, y -0.0375 to 0.0375 m; origin: origin = the start of a 3.0 m length of line, y = the line's centre; tile along x; one instance per 100 mm band
- **Shape and size (real units):** envelope primitive `line_loss`; envelope parameters `{"line_width_mm": 75, "length_m": 3.0, "cross_gaps": {"per_m": [1.2, 2.4], "length_mm_lognormal": [20, 60, 300]}, "edge_chips": {"per_m": [2, 6], "depth_mm": [5, 15], "length_mm": [20, 150]}, "specks": {"per_m": [8, 20], "eqd_mm": [4, 9]}}`
  - Geometry numbers: `{"gap_length_mm": {"p10": 20, "p50": 60, "p90": 300, "src": "Photo M26 (gaps 3 to 55 mm, one 0.5 m); reviewer 20 to 300 mm"}, "edge_ragged_mm": [5, 15], "edge_10_90_mm": [2, 15], "edge_src": "Judgement: paint chips are hard-edged; the 3 mm pixel and JPEG soften them", "edge_for_envelope_mm": 3}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | line_yellow | [195, 168, 100] | [92, 88, 82] | road showing through the lost paint | 1.0 | -32 | Photo M01 asphalt (89/86/80) a little dirtier |
  | line_white | [190, 188, 182] | [92, 88, 82] | road showing through the lost paint | 1.0 | -39 | Photo M01 |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.4, "note": "the exposed road is dark and glossy; the paint edge shows"}`. [Read WET-ROAD + Judgement]
- **Texel scale:** smallest feature 4 mm; mask needs at least 800 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: a line is 75 mm to 100 mm wide: 1120 px/m gives 84 to 112 texels; beyond 6 m fade the specks
- **Variants:** 6 seeded masks; they differ by gap seed; one with a long (0.3 m) gap, one with heavy edge chipping; mirror in x; tile along the line [Derived]
- **Why 1990 Britain:** Thermoplastic and paint lines wore the same in 1990 (Judgement); the colour is a municipal yellow, not the 2000s hazard yellow (the scene's own 0.78/0.66/0.18).
- **Not modern, not American:** No pristine thermoplastic lines; no red or green bus-lane paint; no American double centre line.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.1 | 0.3 | Photo M26 (22 %), reviewer 10 to 30 % |
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 150}` | 15 | 150 | Photo M26 / reviewer: gaps 20 to 300 mm (chips and gaps; specks under 150 mm2 left out) |
  | size_cv | size_cv | mask | `{"thr": 0.5, "min_area_mm2": 150}` | 0.25 | 2.0 | Judgement: gaps differ |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 2 | 15 | Judgement |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived |

### `sign_ghost`: Ghost marks of removed signs and brackets

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** A rectangle 0.3 to 2.0 m wide and 0.15 to 0.8 m high, 5 to 10 L* paler or cleaner than the wall around it, with 2 to 4 filled holes 10 to 20 mm across (paler filler) and, at half the holes, a short rust_bleed tail. Ragged edges 5 to 20 mm. 0 to 1 per facade (typical 0.5).
  - Feature: walls where a sign, a board or a bracket was removed: former shop fascias on the empty unit (east bay 3, x 21 to 27), the side of the chandler, gable ends, lamp-bracket positions
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 1.5 to 3.5 (fascia and sign height)
  - Sides: Both; the empty unit (bay 3) 1.5
  - Footfall and wet: Not footfall; wet: the cleaner rectangle reads stronger when the wall around it is wet and dark.
  - Density: 0.0 to 1.0 ghosts per facade (typical 0.5) [Judgement (reviewer 8 October: 0 to 1 per facade)]
- **Decal frame:** x -1.1 to 1.1 m, y -0.5 to 0.5 m; origin: origin = the ghost's centre
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.3, 2.0], [0.15, 0.8]], "ragged_mm": [5, 20], "level": 0.6, "holes": {"n": [2, 4], "eqd_mm": [10, 20], "level": 1.0}}`
  - Geometry numbers: `{"patch_size_m": {"w": [0.3, 2.0], "h": [0.15, 0.8], "src": "Judgement (reviewer 8 October)"}, "hole_eqd_mm": [10, 20], "edge_10_90_mm": [3, 25], "edge_src": "Judgement: a cleaner rectangle has a soft, dirt-drawn edge", "edge_for_envelope_mm": 12}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [187, 118, 96] | cleaner, paler brick | 1.0 | 14 | Judgement (reviewer 8 October: 5 to 10 L* at the rectangle's mask 0.6, so 14 L* at mask 1) |
  | brick_painted | [152, 108, 93] | [191, 136, 118] | cleaner paint | 1.0 | 12 | Judgement |
  | render_cream | [214, 200, 178] | [238, 222, 198] | cleaner render | 1.0 | 8 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.15}`. [Judgement]
- **Texel scale:** smallest feature 10 mm; mask needs at least 600 px/m, use 800; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by size, hole count (2 to 4), with or without rust tails, a bracket stub (one dark hole 30 mm); no rotation [Derived]
- **Why 1990 Britain:** Removed shop signs left cleaner, paler rectangles and plugged fixing holes on any old wall (Judgement; 4-SIGNAGE-AND-WEAR.md lists them).
- **Not modern, not American:** No vinyl-ghost outlines; no spray-painted utility marks.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.03 | 0.8 | Derived: 0.3 to 2.0 m x 0.15 to 0.8 m in a 2.2 x 1.0 m frame (thr 0.5 sees the 0.6 rectangle) |
  | hole_count | role_count | envelope | `{"role": "hole"}` | 2 | 4 | Judgement (reviewer 8 October) |
  | hole_eqd_mm_p50 | role_blob_eqd_mm | envelope | `{"role": "hole", "stat": "p50"}` | 10 | 22 | Judgement (reviewer 8 October) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 3 | 25 | Judgement |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived: the holes are level 1 |

### `graffiti_buff`: Buffed graffiti: flat patches of mismatched paint

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** A flat rectangle 0.3 to 1.5 m wide and 0.3 to 1.2 m high in a mismatched matt paint, +/- 10 L* from the wall, hard-edged with ragged corners 5 to 25 mm. 0 to 1 per 20 m of facade. The tags themselves belong to the signage family (canon's five tags); this is only what is left when one is removed.
  - Feature: the lower 0.5 to 2.5 m of walls where a tag was painted over: ground-floor brick, render and stallriser-height panels, side gables, the roller shutter's neighbour
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0.5 to 2.5
  - Sides: Both; the west block's blind gable and the yard entrance 1.2
  - Footfall and wet: Not footfall; wet: matt paint darkens less than brick, so the patch reads paler when wet.
  - Density: 0.0 to 1.0 patches per 20 m of facade (typical 0.4) [Judgement (reviewer 8 October)]
- **Decal frame:** x -0.8 to 0.8 m, y -0.65 to 0.65 m; origin: origin = the patch's centre
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.3, 1.5], [0.3, 1.2]], "ragged_mm": [5, 25], "drip_tail": {"length_m": [0.0, 0.0], "width_m": [0.0, 0.0]}}`
  - Geometry numbers: `{"patch_size_m": {"w": [0.3, 1.5], "h": [0.3, 1.2], "src": "Judgement (reviewer 8 October)"}, "edge_10_90_mm": [2, 20], "edge_src": "Judgement: a paint edge is hard", "edge_for_envelope_mm": 8}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [108, 66, 52] | dull matt brown paint | 1.0 | -10 | Judgement (reviewer 8 October: +/- 10 L*) |
  | brick_painted | [152, 108, 93] | [127, 90, 77] | dull matt paint | 1.0 | -8 | Judgement |
  | render_cream | [214, 200, 178] | [238, 222, 198] | fresh cream emulsion | 1.0 | 8 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.1}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.1, "note": "matt paint darkens less than brick"}`. [Judgement]
- **Texel scale:** smallest feature 20 mm; mask needs at least 300 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by size, aspect, one with a second coat's overlap (a darker strip 0.1 m along one edge); no rotation [Derived]
- **Why 1990 Britain:** Councils and shopkeepers painted out tags with whatever paint was to hand; mismatched patches are the look of an old quarter (Judgement).
- **Not modern, not American:** No pressure-washed pale shapes (2000s); no colour-matched, invisible repair.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 50000}` | 300 | 1500 | Judgement (reviewer 8 October) |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.1 | 0.9 | Derived: 0.3 to 1.5 m x 0.3 to 1.2 m in a 1.6 x 1.3 m frame |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 2 | 20 | Judgement |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived |

### `handle_wear`: Hand and push wear around door handles, letter plates and push zones

- **Layer:** L1 stamp decal on doors
- **Where (the rule):** A dark greasy halo 0.10 to 0.25 m (p50 0.17) around the handle, letter plate or push zone at 0.9 to 1.2 m, multiplier 0.75, taller than wide (aspect 1 to 1.8). Door edges worn to undercoat belong to paint_flake (its rule: 15 to 30 mm wide).
  - Feature: door handles, thumb-latches, letter plates and push plates of shop and side doors (shop door 0.90 x 2.04, side door 0.838 x 1.981, letter plate 0.25 x 0.04 at 1.0 m, SCENE-SLOTS)
  - Surfaces: timber_paint_dark, timber_paint_light
  - Height: 0.9 to 1.2
  - Sides: Both; shop doors 1.0, side doors 0.8
  - Footfall and wet: Footfall: hands, not boots; wet: the grease halo reads darker and glossier.
  - Density: 0.8 to 1.0 per handle, plate or push zone (typical 0.9) [Judgement (reviewer 8 October)]
- **Decal frame:** x -0.3 to 0.3 m, y -0.3 to 0.3 m; origin: origin = the handle's centre
- **Shape and size (real units):** envelope primitive `halo`; envelope parameters `{"eqd_m": [0.1, 0.17, 0.25], "aspect": [1.0, 1.8], "core_fraction": 0.5, "core_level": 1.0, "outer_level": 0.6}`
  - Geometry numbers: `{"halo_eqd_mm": {"p10": 100, "p50": 170, "p90": 250, "src": "Judgement (reviewer 8 October)"}, "edge_10_90_mm": [25, 90], "edge_src": "Judgement: a grease halo fades", "edge_for_envelope_mm": 50}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | timber_paint_dark | [52, 64, 88] | [47, 55, 74] | greasy dark grime | 0.75 | -4 | Judgement (reviewer 8 October: x 0.75) |
  | timber_paint_light | [222, 218, 206] | [203, 191, 163] | greasy grey-brown | 0.75 | -9 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.1}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.2}`. [Judgement]
- **Texel scale:** smallest feature 50 mm; mask needs at least 120 px/m, use 200; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by size, aspect, one with a second smaller halo (a push plate above the handle); no rotation [Derived]
- **Why 1990 Britain:** Painted doors showed hand grease around the handle in any decade (Judgement); brass and steel plates were polished by hand until the paint around them grew dark.
- **Not modern, not American:** No sensor plates, no keypad wear, no uPVC doors.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 3000}` | 80 | 290 | Judgement (reviewer 8 October) |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.015 | 0.4 | Derived: a 0.10 to 0.25 m halo in a 0.6 m square |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 20 | 100 | Judgement |
  | peak_mask | mask_max | mask | `{}` | 0.85 | 1.0 | Derived: the core is level 1, softened by the 50 mm edge |

### `stone_top_lichen`: Lichen and algae on the horizontal tops of stone sills and copings

- **Layer:** L1 stamp decal on the top face (0.2 m deep, along the sill)
- **Where (the rule):** 40 to 80 % of the top face covered in olive-green patches of 10 to 60 mm (p50 25 mm), merging into larger crusts toward the back and the ends where water lies; olive 103/88/65 on the wet sheet (115/98/73 dry; the sheet's sills read 95 to 112 / 82 to 89 / 62 to 70 wet, L* about 36).
  - Feature: the horizontal top faces of stone and cast-stone window sills and copings, gate-pier caps, step treads
  - Surfaces: stone_sill
  - Height: the tops of sills and copings at any height
  - Sides: East parade (wet) 1.0; west block 0.7; shaded gables 1.0
  - Footfall and wet: Wet climate: lichen and algae need standing damp; not footfall.
  - Density: 0.4 to 0.8 share of the sill or coping top covered (typical 0.6) [Sheet (olive lichened sills); reviewer 8 October]
- **Decal frame:** x 0.0 to 1.0 m, y 0.0 to 0.2 m; origin: origin = the back corner at the left end of the sill's top face; x along the sill, y toward the viewer; stamped along longer sills
- **Shape and size (real units):** envelope primitive `patch_cover`; envelope parameters `{"region_m": [1.0, 0.2], "share": [0.4, 0.8], "eqd_mm": [10, 25, 60], "aspect": [1.0, 1.6]}`
  - Geometry numbers: `{"patch_eqd_mm": {"p10": 10, "p50": 25, "p90": 60, "src": "Judgement (reviewer 8 October: 10 to 60 mm); Photo M15 moss patches 5.5 / 10 / 32 mm"}, "edge_10_90_mm": [2, 12], "edge_src": "Photo M15: moss edges 6.7 to 9.5 mm", "edge_for_envelope_mm": 4}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | stone_sill | [170, 166, 158] | [115, 98, 73] | olive lichen | 1.0 | -26 | Sheet: olive 95 to 112 / 82 to 89 / 62 to 70 (middle 103/88/65) on the sheet's sills, a WET street; dry = that divided by the wet 0.80 in luminance = 115/98/73, used once |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.1}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.3, "note": "lichen darkens and goes slick when wet; the sheet is wet: dry colour about 1/0.8 brighter than the sheet's"}`. [Judgement]
- **Texel scale:** smallest feature 10 mm; mask needs at least 600 px/m, use 800; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: the sill's top is 0.15 to 0.25 m deep; 1.0 m x 0.2 m at 800 px/m = 800 x 160
- **Variants:** 4 seeded masks; they differ by share 0.4, 0.6, 0.8; seed; crusts at the ends; mirror in x [Derived]
- **Why 1990 Britain:** Lichen and algae on stone are slow, so an uncleaned 1990 sill carries decades of it (Judgement; the Hook sheet's sills are olive).
- **Not modern, not American:** No freshly cleaned pale stone on every sill; no painted-white sills on the uncleaned stone ones.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.4 | 0.85 | Sheet / reviewer: 40 to 80 % |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 2 | 14 | Photo M15 |
  | mask_std | mask_std | mask | `{}` | 0.3 | 0.52 | Derived: a two-level mask at 40 to 80 % share |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived |

### `footway_infill`: Bitmac and in-situ concrete infill in the flagged footway

- **Layer:** L2 ground (virtual texture); the infill's own texture comes from its material, this mask is its extent
- **Where (the rule):** 1 to 3 per 48 m of footway, 0.6 to 3.0 m long, one flag row wide (0.55 to 0.65 m), ragged edges 5 to 15 mm; bitmac 70/68/66 or in-situ concrete 150/143/136 with a rough aggregate surface. Photo M07b: the in-situ strip at the bottom of the urban_street_03 flags ortho reads 161/153/149 on the tone-mapped view where the dark flags read 136/132/131, with a rough texture (std 14 against about 5 on flags).
  - Feature: the footway where flags were lifted for a trench or a cover and the gap was filled with bitmac or poured concrete: strips one flag row wide, and the kerbside strip
  - Surfaces: flag_concrete
  - Height: ground (0 to 6 mm sunk)
  - Sides: Both footways; east 1.0, west 0.9 (the parade's pavement is more recently relaid)
  - Footfall and wet: Footfall and trenches; wet: bitmac darkens and glints less than flags; concrete reads paler.
  - Density: 1 to 3 infills per 48 m of footway (typical 2) [Judgement (reviewer 8 October); Photo M07b (one strip and one patch in about 4 m of footway)]
- **Decal frame:** x -0.4 to 0.4 m, y -1.6 to 1.6 m; origin: origin = the infill's centre; the long side along the footway (yaw 0 or 90)
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.55, 0.65], [0.6, 3.0]], "ragged_mm": [5, 15], "drip_tail": {"length_m": [0.0, 0.0], "width_m": [0.0, 0.0]}}`
  - Geometry numbers: `{"patch_size_m": {"w": [0.55, 0.65], "h": [0.6, 3.0], "src": "Judgement (reviewer 8 October); Photo M07 (flags 0.6 to 0.7 m)"}, "edge_10_90_mm": [3, 20], "edge_src": "Judgement: a cut edge is hard, with a soft dirt line", "edge_for_envelope_mm": 8}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [70, 68, 66] | bitmac infill | 1.0 | -23 | Judgement (reviewer 8 October). In-situ concrete variant: 150/143/136 (Photo M07b, 161/153/149 on the tone-mapped view) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.1}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.3, "note": "bitmac darkens little when wet, concrete as the flags"}`. [Judgement]
- **Texel scale:** smallest feature 5 mm; mask needs at least 800 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: the mask is the extent only; frame 0.8 m x 3.2 m
- **Variants:** 6 seeded masks; they differ by length (0.6, 1.2, 3.0 m), bitmac or in-situ concrete (variants 3 to 5), a hairline crack from the edge; yaw 0 or 90 [Derived]
- **Why 1990 Britain:** Utility trenches were reinstated with bitmac or concrete, not new flags, in an old-quarter footway (Judgement; Photo M07b shows the same practice in 2019).
- **Not modern, not American:** No coloured resin or block-paved infill; no tactile paving.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 100000}` | 600 | 2200 | Derived: 0.6 x 0.6 to 0.6 x 3.0 m |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.1 | 0.8 | Derived: 0.6 x 0.6 to 3.0 m in a 0.8 x 3.2 m frame |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 3 | 25 | Judgement |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived |

## 6. Surfaces and colours

| surface | albedo sRGB | plain name | source |
|---|---|---|---|
| brick_red | [140, 87, 70] | weathered red facing brick | Read: one measured brick, production/research/aaa-street/BRICK-COLOUR-2026-10-08.md (0.262/0.095/0.061 linear) |
| brick_painted | [152, 108, 93] | painted brick or masonry, dull red-pink or cream | Photo M08 (peeling_painted_wall paint 152/108/93, a 2024 acrylic scan): Judgement for 1990 oil paint, see S1 in section 2 |
| render_cream | [214, 200, 178] | cream or whitewashed render | Photo M12 (concrete_wall_003 clean paint 222/205/182, a 2021 scan) pulled 4 % toward weathered: Judgement for 1990 limewash and oil paint, see S1 |
| timber_paint_dark | [52, 64, 88] | dark navy or deep-red shopfront paint (stallriser, pilaster, fascia) | Judgement; the Hook sheet's Mickey's blue |
| timber_paint_light | [222, 218, 206] | cream or white painted timber and window frames | Judgement |
| stone_sill | [170, 166, 158] | pale grey stone or cast-stone sill and coping | Judgement (pale grey stone or cast-stone). The Hook sheet's sills are olive, lichened stone (95 to 112 / 82 to 89 / 62 to 70, L* about 36): that is this surface after stone_top_lichen, not before it |
| flag_concrete | [134, 123, 110] | concrete paving flag, weathered | Photo M27 (concrete_pavement_02 scan, median 134/122/110, L* 52.0); its luminance agrees with M07's dark class (133/130/130, L* 54, urban_street_03); the hue is the scan's (warmer than the cool-grey photograph) |
| asphalt_dry | [89, 86, 80] | worn road asphalt, dry | Photo M01: per-channel median of the three mid scans (asphalt_02 87/86/80, aerial_asphalt_01 97/92/97, asphalt_01 89/80/70) is 89/86/80; the first pass used their mean, 91/86/82 |
| kerb_granite | [128, 126, 122] | granite or concrete kerb | Judgement |
| iron_black | [35, 35, 36] | black painted cast iron (downpipe, railing) | Judgement |
| channel_concrete | [116, 111, 108] | the channel course: kerb-quality concrete setts or a concrete channel block, weathered | Photo M24: the channel setts read 1.4 x the open road's luminance (0.236 against 0.161 to 0.170) in urban_street_03; the albedo is the road's (Y 0.095) x 1.4 / 0.85 (the grime multiplier) = Y 0.157. The reviewer's 150/146/140 would give 3.0 x the road: against the measurement, see D7 |
| line_yellow | [195, 168, 100] | weathered municipal yellow line paint (the scene's own 199/168/46 faded and dirt-filmed) | Photo M26: the line reads 230/208/154 on the tone-mapped view where the road reads 114/114/120 and has albedo 89/86/80; converted by the road's ratio it is about 181/162/120. Judgement: the more saturated 195/168/100, between that and the scene's 199/168/46 (vignette-scene.json paint.double_yellow) |
| iron_grate | [58, 54, 52] | cast-iron gully or cellar grate, bare, grey-black | Judgement; Photo M25 (the gully grate in urban_street_03: bars read dull red-brown 125/109/103 on the tone-mapped view, slots black) |
| tile_glazed | [172, 166, 150] | glazed stallriser tile, cream with a dark and ochre pattern (Mickey's) | Judgement: the Hook sheet's Mickey's stallriser is patterned glazed tile; the shopfront family's own tile colours win where they differ |
| line_white | [190, 188, 182] | weathered white road line paint (the sheet's dashed centre line) | Judgement; the Hook sheet's centre line; the lines family's own colour wins |

These are references for the tone tables only (the street's own brick and paint colours belong to the brick and shopfront families and win where they differ; the multipliers carry over).

## 7. Where the photographs, the sheet and the books disagree, and what was chosen

- **D1.** brief ('Leaking001-006, ChewingGum001-002 ... are photographs of real wear') against ambientCG's own metadata (creationMethod PBRProcedural): chose the metadata: these are generated, so they are not measured; they may still be used as CC0 shapes by unit 4.5 but never as evidence.
- **D2.** Hook sheet (black foot band 0.33 m at 0.12 to 0.30 of the wall, wet; a dark head under the verge; NO streaks anywhere) against the 2019 London photographs (maintained brick: faint streaks, no foot band on the estate wall; but soot, M21): chose the sheet for feet and heads (it is the mood bar; the 2019 walls are cleaned or maintained), converted from wet to dry (foot x 0.27 dry = 0.20 wet; head x 0.56 dry = 0.50 wet), and the photographs for streaks (the sheet shows none): the first pass said 'no streak was measured on the sheet' and then cited the sheet for streak length; that is withdrawn.
- **D3.** existing masks (high-contrast, 0.4 to 1.0 strength everywhere, 8 kinds) against Photo M02/M04 (real road wear is low contrast: dL 2 to 9, marks 5 to 12 % of the area): chose the photographs for the road and pavement: the mask peaks are 0.7 to 0.9 but the marks cover little of the area (a drip-band stamp 0.2 to 3 % of its frame, a tyre-scuff arc a few per cent, the whole road 4 to 12 %).
- **D4.** asset plan note 4 ('gum is densest at doors, the dark spots on the sheet's right pavement') against the sheet's right-pavement spots, which are reddish-brown stains 0.15 to 0.45 m (rust and mud), not gum: chose two kinds: gum (11 to 35 mm, grey-black) and pavement_stain (brown blots), so the sheet's spots are read as stains.
- **D5.** asset plan note 4 / make_wear_masks.py (streaks: three crops of one procedural map) against Photo M16/M17 (rivulets 10 to 20 mm, bracket streaks 0.06 to 0.10 m x 0.3 to 0.45 m, many of different length): chose a streak set per sill that has one: two unequal end streaks, 3 to 7 rivulets, a faint wash.
- **D6.** the review (streaks under 50 to 70 % of sills, x 0.70, 0.15 / 0.35 / 0.60 m) and the first pass (every sill, x 0.55, 0.8 m p50) against Photo M23 (1 clear streak under about 30 sill edges, none darker than 0.85 in the column test: 3 to 15 %) and M17 (0.66 to 0.91 at the darkest bricks): chose length from the photographs (M16, M17: 0.15 / 0.35 / 0.60 m, one end streak in 8 at 0.8 to 1.4 m); share between the photographs and the review: 15 to 60 % of sills, typical 35 % (the photographs' street is maintained, the cleanest end; the review's 50 to 70 % has no source and is the upper bound); darkness x 0.70 (the review's), nudged darker than the photographs (0.80 to 0.90) by Judgement from Jafar's 'not faint marks' of 2 October: M17 (0.8 core, 0.3 to 0.45 m) against his 'not faint marks': length follows the photographs, darkness nudged darker.
- **D7.** the first pass (gutter_grime: a dark band the width of the channel, x 0.5) and the review (channel_concrete 150/146/140, x 0.85) against Photo M24 (channel 1.35 to 1.7 x the road dry; strip beside it 0.91 to 0.97), the scene note ('the channel in the kerb's own concrete ... a different material') and the wet sheet (strip about 0.7 of the road, kerb face a dark line): chose the photograph for dry values and the scene note: the channel is lighter than the road. The review's colour is the wrong albedo: 150/146/140 (Y 0.289) is 3.0 x the road's albedo (89/86/80, Y 0.095); with the grime x 0.85 it would read 2.6 x the road against the measured 1.4. The albedo is the road's x 1.4 / 0.85: 116/111/108 (Y 0.162). The sheet's 0.7 is a wet, glossy reading and is not a mark multiplier.
- **D8.** the review's sooted state x 0.45 (Photo M21 0.37 to 0.48) and the recipe's HOUSE_LOOKS sooted look (0.60/0.56/0.56, about 0.57) against Photo M21 (0.377, 0.37 to 0.48 by two measurers): chose x 0.42, the middle of the photograph's range; the recipe's 0.57 is lighter than the photograph and its brightness is handed to wall_soot (section 1).
- **D9.** the review's sooted saturation x 0.6 against Photo M21 (HSV saturation 0.207 sooted against 0.247 cleaner = 0.84; linear per-channel ratios 0.37 / 0.37 / 0.43) and Sheet M22 (head 0.65): chose the photograph's per-channel ratios (nearly neutral, a little less saturated); the 0.6 belongs to the sheet's head, not to the photographed sooted panel.
- **D10.** the review (pavement_stain dry 0.48, wet 0.8 giving 0.38) and the first pass (0.38 dry) against Sheet M20: the brown stain 85/60/44 on flag 136/129/131 has a luminance ratio of 0.236 (Y 0.053 against 0.226): chose dry 0.30 x wet 0.80 = 0.24, the sheet's own ratio, used once; neither 0.38 nor 0.48 is what the sheet shows.
- **D11.** the review's lower wall x 0.85 on sooted houses (Judgement) against Sheet M22 (right-hand cottage lower wall 0.90, range 0.84 to 0.93): chose 0.88 composed (mask rise 0.10 on a body of 0.90 at x 0.42), inside the measured range; the review's 0.85 is at its edge.
- **D12.** the review's ground floor 0.35 of the clean albedo against Sheet M20 (the sheet's own stain is 0.236 wet = 0.295 dry, below 0.35) and Photo M24/M05 (marks 0.70 to 0.92): chose a ground floor of 0.28 (dry): above the sheet's darkest measured ground mark, so the sheet's stains pass unclamped and only stacks go lower; the walls' 0.15 follows the review (the sheet's darkest foot is 0.12 to 0.30 of its wall).

## 8. The automatic check, and how to run everything

`target.json` carries a flat `checks` list (171 entries, each with its kind, a name, the measure, its parameters, a min, a max, the source and where it applies). Unit 4.5's check imports `measure(mask, px_per_m, measure_id, **params)` from `self_check.py` and runs each check of a kind on the generated mask (float 0..1, row 0 at the top of the decal frame, frame as the kind's `mask.frame_extent_m` says; `foot_profile` through `foot_profile_check`). Each check carries `applies_to`: `mask` (the 155 checks unit 4.5 runs on a generated mask), `envelope (drawing polygons)` (5 checks that only the drawing can run, because they need polygon roles), `flag data` (2 checks on the flag tone classes) or `composition (compose block)` (9 checks that apply the order, floor and colour rule of section 4 to several kinds' masks: `compose_walls()` and `composition()` in self_check.py). **The text below is `self_check.MEASURE_DOCS` word for word** (self_check part A tests that `check_measures` in target.json equals it), so a builder implementing from target.json alone gets the numbers `measure()` gives. Measures:

- `coverage`: share of decal pixels with mask >= thr (default 0.5)
- `blob_eqd_mm`: equivalent diameter (mm) = 2 sqrt(area / pi) of the 8-connected components of mask >= thr (default 0.5) with area >= min_area_mm2; stat p50 (default) or p90 over the components
- `count_per_m2`: number of 8-connected components of mask >= thr with area >= min_area_mm2, per m2 of the decal frame
- `edge_10_90_mm`: 10 to 90 % edge width, relative to the mask's own peak: 0.95 x peak / the 90th percentile of |gradient| (per metre; one axis if axis is x or y), taken over pixels with band_lo x peak < mask < band_hi x peak (defaults 0.1 and 0.9) that lie within reach_mm (default 60) of the contour at half the peak; 0 if the peak is below 0.2
- `streak_aspect`: median over the 8-connected components of mask >= thr (default 0.3) with rod length >= min_length_m of rod length / rod width; rod length = sqrt(12 x variance) along the major axis, width likewise along the minor axis
- `streak_width_mm`: stat (p50 default, p10 or p90) over those components of the rod width in mm
- `streak_length_m`: stat (p50 default, p10 or p90) over those components of the rod length in m
- `verticality_deg`: largest deviation of a component's major axis from vertical (degrees) over the components of mask >= thr (default 0.3) with rod length >= min_length_m (default 0.1 m)
- `fade_ratio`: per component of mask >= thr (default 0.3) taller than 150 mm: mean mask over its last third of rows / its first third; median over components
- `foot_profile`: mean mask per row of the whole decal width, at each point [height_m, min, max], mean of three rows: axis rows_from_bottom counts height up from the frame's bottom row (the pavement line), rows_from_top counts down from its top row (the feature's lower edge); the check passes when at least 80 % of the points are inside their bounds
- `tile_seam`: mean |mask(first column) - mask(last column)| (rows for axis y; the larger of the two for xy) divided by the mean absolute difference of adjacent columns (rows) inside the tile: about 1 when seamless
- `mask_max`: maximum mask value
- `mask_std`: standard deviation of the mask
- `mask_mean`: mean of the mask
- `top_edge_std_mm`: standard deviation along x, in mm, of the far edge of the band: for each column the row farthest from the source edge (source bottom: the pavement line, the frame's bottom row; source top: the feature's lower edge, the top row) where mask >= thr; columns without such a row are left out; 0 if fewer than 60 % of the columns have one
- `column_mean_cv`: coefficient of variation (std / mean) across x of the column means of the mask over the rows from_m to to_m (m) measured from the source edge (source bottom or top)
- `brick_patch_share`: share of brick cells whose mean mask is above cell_mean_above (default 0.4): cells brick_w_m x brick_h_m in stretcher bond (courses brick_h_m high from the pavement line, each course offset by half a brick), only courses lying wholly between from_m and to_m, only whole cells inside the frame
- `brick_cell_std`: mean over the cells counted as whitened in brick_patch_share (same cells, same parameters) of the standard deviation of the mask inside the cell
- `end_streak_length_ratio`: longer over shorter rod length of the leftmost and rightmost components of mask >= thr (default 0.25) whose top lies within head_m (default 0.2) of the frame's top edge (the sill's lower edge); 0 if there are fewer than two
- `end_streak_width_ratio`: wider over narrower rod width of the same two end components
- `rivulet_count`: number of the components between those two end components, in x order, with rod length >= min_length_m (default 0.1)
- `finger_spacing_cv`: std / mean of the gaps between the centres of the runs of mask >= thr (default 0.25) along the row head_row_m (default 0.12 m) below the frame's top edge; 0 if fewer than three runs
- `finger_length_cv`: std / mean of the rod lengths of the components of mask >= thr whose top lies within head_m of the top edge; 0 if fewer than three
- `nn_ratio`: Clark-Evans ratio of the components of mask >= thr (area >= min_area_mm2; at least 4): mean nearest-neighbour distance of their centroids / (0.5 / sqrt(n / A)), A the frame area (area frame) or the convex hull of the centroids (area hull); about 1 for random scatter, above 1.3 for a lattice, below 0.8 for clusters; 0 if fewer than four
- `size_cv`: std / mean of the equivalent diameters of the components of mask >= thr with area >= min_area_mm2 (at least 4)
- `dominant_wavelength_m`: wavelength 1 / (k x f) in m of the annulus with the largest summed power in the 2-D power spectrum of the mask minus its mean, annuli of width f = 1 / the shorter side of the frame (m), k = 1, 2, 3, ... the annulus index (the zero-frequency annulus is left out)
- `tone_ratio`: mean luminance of the dark-slab class over the pale-slab class in the generated flag colour map (check applies to the flag colour result, not the mask)
- `crack_flag_share`: share of flags carrying a crack in the generated flag attributes
- `crack_width_mm`: median of 2 x distance-transform - 1 along the Zhang-Suen skeleton of mask >= thr (mm)
- `crack_length_per_m2`: skeleton length (m) of mask >= thr per m2 of the decal frame
- `role_length_per_m2`: envelope polygons only (drawing check): path length of the polygons with the named role per m2 of the frame
- `role_blob_eqd_mm`: envelope polygons only (drawing check): equivalent diameter of the polygons with the named role (stat p50 or p90)
- `role_count`: envelope polygons only (drawing check): number of polygons with the named role
- `role_share_below`: envelope polygons only (drawing check): share (by polygon area, of=area, or by count) of the polygons with the named role whose centroid lies below below_mm of the frame's bottom edge
- `composed_foot_ratio`: composition (compose block, self_check.compose_walls): the luminance of a composed 2 m brick foot beside a downpipe (wall_soot, wall_foot_damp, wall_foot_splash, algae_downpipe in the stated order, then the floor, at house wear 1.0, dry, in the state given) over the clean wall's, mean over x 0.6 to 1.4 m at height_m (default 0.1)
- `composed_salt_ratio`: composition: luminance over the clean wall's of the composed foot at the whitened bricks (salt mask > 0.4) between 0.30 and 0.52 m, after the replacing marks
- `composed_wall_min_ratio`: composition: the lowest luminance over the clean wall's anywhere on the composed foot before the replacing marks (the floor is working when it is not below the wall floor)
- `composed_soot_ratio`: composition: mean luminance of the sooted house's composed wall (soot state weight 1.0) over the cleaned house's (weight 0.0), rows from 1.3 m up
- `composed_head_ratio`: composition: luminance over the wall's of the composed head band at depth 0.1 m below the feature, wall_soot in the given state first, mean over x
- `channel_over_road`: composition: luminance of the channel_concrete albedo after the channel body's gutter_grime (mean over the channel rows 0.06 to 0.23 m) over the asphalt_dry albedo's
- `fringe_over_road`: composition: luminance of the asphalt_dry albedo after the gutter_grime fringe (mean over rows 0.30 to 0.45 m) over the unmarked asphalt_dry albedo's
- `composed_ground_min_ratio`: composition: the lowest luminance over the clean surface's of a kerb_granite texel under pavement_stain and gutter_grime together (at mask 1), after the ground floor

```
/home/user/.bpyenv/bin/python target_drawing.py OUT_DIR      # polygons (mm) in wear_envelopes.json, scene_*.png and kind_*.png sheets in OUT_DIR
/home/user/.bpyenv/bin/python self_check.py                  # prints the result line, writes it to target.json under self_check, writes the two overlays
```

**What the self-check does** (A to F): A structure (every part present, numbers in order, every cited measurement id exists, every surface has a tone, the compose block, places and placement checks exist, the measure text equals the code, no word that implies a minor, the source statements the review asked for); B tone (each mark colour is the surface times its multiplier within 12 %, its dL* follows, where a photograph or the sheet quoted a dL* the two agree within 14, no single mark is below its floor, the sheet-derived rows give the sheet's ratio once); C the photographs (the measurements are re-made from the reduced previews and must come back within their stated errors: the drip band, flags, paint flake, craquelure, tyre scuffs, the soot panel, the sheet's head, lower wall and downpipe, the sill column test, the channel against the road, the yellow line's loss, the sealed crack's width, the reinstatement's seam and the tan share of the litter; the drip-band envelope is laid on the main photograph with the scale fitted on one dimension only and holds at least 90 % of the dots found; the splash profile is laid on the Hook sheet's gable foot with the scale fitted on the 75 mm brick course alone, wet multiplier included, mean error 0.15 or less in luminance ratio against the sheet's own scatter of about 0.1); D envelopes (each kind is drawn at its texel scale, three variants and two seeds, rasterised with its stated edge softness, and every mask and envelope check of the kind is run on it; the median of the six runs must be inside the range); E composition and wrong masks (the compose rule is applied to drawn masks: the composed foot, the floor, the salt order, the soot state, the head, the channel and the ground floor; and masks made deliberately wrong, the nine of the review and more, must each be refused by at least one of their kind's mask checks, the refusing checks being listed in target.json under self_check.wrong_masks_refused); F placement (the nine placement checks pass on a conforming placed street and each is refused when its rule is broken, with no other rule affected).

**Overlays:** `ph-urban_street_03-oil-drip-speckle-target-on-photo.jpg` (the target's drip band in cyan on the photograph, the dots found in red), `hook-sheet-gable-foot-target-on-sheet.jpg` (the splash profile's heights as lines on the gable foot) and `hook-sheet-gable-head-target-on-sheet.jpg` (the head band's depths as lines under the verge).

**Honesty about the checks' ranges.** The ranges come from the stated target numbers, and where my first envelope did not meet its own range I did one of two things and wrote it down: corrected the envelope (wash level below the streak threshold, rust halo level, tyre-scuff profile, dot density counted inside the band instead of over the whole region, Voronoi cracks in place of a jittered grid, wrapped copies for tiles) or corrected a range I had set carelessly (the foot kinds' edge width is the whole fall-off 0.3 to 1.2 m, not the 75 mm step inside it). Nothing was passed by widening a range beyond what the photograph measurements allow.

**Single masks.** The ranges are tested on the median of six drawn masks (self_check part D, which the review reproduced). For the checks added or amended in this pass, 78 to 100 % of 30 single drawn masks (6 seeds x 5 variants, measured separately and not kept as a script) fall inside their range: wall_head_band top edge 97 % and column cv 86 %; streak_sill end ratios 89 to 99 % and rivulets 97 %; streak_coping 95 to 100 %; salt_bloom 92 to 100 %; line_wear loss 89 %; iron_wear 95 to 97 %; the lowest are wall_foot_damp's top edge 78 % and column cv 81 %, and gum's clustering 79 % and size spread 88 % (ten discs in 4 m2 are few). The first-pass kinds' ranges were not re-tuned; a few pass only 55 to 80 % of single masks (rust_bleed, pavement_stain coverage, render_patch, road_blot), so unit 4.5 should apply them to the median of a small batch, or widen them on its own evidence.

## 9. What the target could not settle

- Gum density per m2: no photograph with gum was reached; the 2019 London panoramas show low-gum residential streets. Tiers are Judgement and kept low (gum staining grew after 1990). Read Keep Britain Tidy / Defra litter surveys and Geograph shopping-street photographs when the network opens.
- 1990 soot level on Quay Street's brick: every reachable photograph is 2018 to 2026 and cleaner. Photo M21 measures a sooted 2019 panel at 0.377 of a cleaner one (0.37 to 0.48); how many of the street's houses were sooted in 1990 (7 of 13 here, from the existing house sets) and how sooted is Judgement; the head and foot strengths are set from the wet Hook sheet and converted to dry.
- Sill streaks in 1990: the photographs (M23) give 3 to 15 % of sills with a visible streak on a maintained 2019 street; the 1990 share (15 to 60 %, typical 35 %) and darkness (x 0.70) are Judgement from Jafar's 'not faint marks' (D6). Streak width as a fraction of sill width is bounded by M16 and M17, not measured.
- Salt bloom height and share: only the Hook sheet shows it; the rule for a port is Judgement (BRE 245 search lead).
- Fly-poster, bird-dropping, paint fade, sign ghosts, buffed graffiti, handle wear, stone lichen share and footway infill: no measured photograph; shapes and shares are Judgement (the review's suggested numbers where it gave them).
- Iron wear: one pipe on the sheet (M25) and one gully grate in a 2019 photograph; the grate's rust colour is between the photograph's dull brown and the sheet's red-brown.
- Camera height for the panorama measurements (1.6 m) is proved only by the 75 mm yellow line (+/-6 %).
- The brief said ambientCG's gum and leaking assets are photographs; the metadata says procedural: unit 4.5 may use them as CC0 shapes only.
- The recipe hand-over (section 1) is written against terrace-front.py as read on 8 October; the builder checks the constants before changing them.

## 10. Credits for the previews

All previews are reduced (JPEG, at most 1200 px on the long side, under 300 KB) from CC0 files read on 8 October 2026, for measurement only; named `<ref>-<place>-<what>.jpg` (ref `ph` = Poly Haven; `hook-sheet` = the project's own sheet). Scale is stated where it is fixed.

| file | scale | credit |
|---|---|---|
| `hook-sheet-downpipe-paint-loss.jpg` | 3.89 mm per pixel | the project's own Hook sheet (production/previews/hook-sheet-2026-10-05.jpg), a reduced crop; a generated mood picture, not a photograph |
| `hook-sheet-gable-foot-and-patch.jpg` | 3.4 mm per pixel | the project's own Hook sheet (production/previews/hook-sheet-2026-10-05.jpg), a reduced crop; a generated mood picture, not a photograph |
| `hook-sheet-gable-head-band.jpg` | 2.27 mm per pixel | the project's own Hook sheet (production/previews/hook-sheet-2026-10-05.jpg), a reduced crop; a generated mood picture, not a photograph |
| `hook-sheet-right-cottage-lower-wall.jpg` | 1.1 mm per pixel | the project's own Hook sheet (production/previews/hook-sheet-2026-10-05.jpg), a reduced crop; a generated mood picture, not a photograph |
| `ph-aerial_asphalt_01-road-tyre-scuffs.jpg` | 7.32 mm per pixel | Poly Haven texture aerial_asphalt_01, Rob Tuytel, CC0; 30000 mm across the full map |
| `ph-asbestos_sheet_02-rust-bleed-fixings.jpg` | 0.879 mm per pixel | Poly Haven texture asbestos_sheet_02, Amal Kumar, CC0; 1800 mm across the full map |
| `ph-asphalt_02-road-sealed-crack.jpg` | 1.46 mm per pixel | Poly Haven texture asphalt_02, Rob Tuytel, CC0; 3000 mm across the full 2048 px map; the crop is the left part of the map (x 0 to 800, y 200 to 1200) and holds the sealed crack at about x 250 (the first pass showed the right half, which has an open hairline only) |
| `ph-concrete_layers-drip-streaks.jpg` | 1.29 mm per pixel | Poly Haven texture concrete_layers, Amal Kumar, CC0; 1550 mm across the full map (resized to 1200 px) |
| `ph-concrete_wall_003-damp-mould-blotches.jpg` | 2.5 mm per pixel | Poly Haven texture concrete_wall_003, Dimitrios Savva and Rico Cilliers, CC0; 3000 mm across the full map |
| `ph-damaged_plaster-render-loss.jpg` | 1.54 mm per pixel | Poly Haven texture damaged_plaster, Amal Kumar, CC0; 1850 mm across the full map |
| `ph-peeling_painted_wall-paint-flake.jpg` | 1.5 mm per pixel | Poly Haven texture peeling_painted_wall, Dimitrios Savva, CC0; 1800 mm across the full map |
| `ph-plaster_brick_01-wall-foot-algae.jpg` | 2.25 mm per pixel | Poly Haven texture plaster_brick_01, Rob Tuytel, CC0; 2700 mm across the full map |
| `ph-preconcrete_wall_001-craquelure-flakes.jpg` | 1.95 mm per pixel | Poly Haven texture preconcrete_wall_001, Dimitrios Savva and Rico Cilliers, CC0; 4000 mm across the full map |
| `ph-rusty_painted_metal-rust-streaks.jpg` | 1.83 mm per pixel | Poly Haven texture rusty_painted_metal, Amal Kumar, CC0; 2200 mm across the full map |
| `ph-urban_street_02-kerb-litter-view.jpg` | see note | Andreas Mischok, Poly Haven urban_street_02 (CC0, taken 2019-08-18) |
| `ph-urban_street_02-road-reinstatement-ortho.jpg` | 3 mm per pixel | Andreas Mischok, Poly Haven urban_street_02 (CC0, taken 2019-08-18) |
| `ph-urban_street_03-bay-sill-bracket-streak.jpg` | see note | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-facade-sills-no-streaks.jpg` | see note | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-flags-patched-ortho.jpg` | 4 mm per pixel | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-garden-wall-soot-streaks.jpg` | see note | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-kerb-flags-channel-view.jpg` | see note | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-oil-drip-speckle.jpg` | 3 mm per pixel | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-oil-drip-speckle-target-on-photo.jpg` | 3.0 mm per pixel | overlay of the target's drip band on the main photograph; photograph credit as above |
| `hook-sheet-gable-foot-target-on-sheet.jpg` | 6.8 mm per pixel on the sheet | overlay of the splash profile on the Hook sheet (the project's own file) |
| `hook-sheet-gable-head-target-on-sheet.jpg` | 2.3 mm per preview pixel (6.8 mm per sheet pixel, tripled) | overlay of the head band's depth profile on the Hook sheet gable under the verge (the project's own file) |

## 11. What changed after the review of 8 October (the second and last pass)

The fresh target reviewer's FAIL (`TARGET-REVIEW.md`, 12 faults) is answered here, fault by fault; where a number of the review is not what a measurement shows, the measurement is given instead and the disagreement is in section 7.

1. **Facade-wide soot and the dark head had no kind and no owner.** Measured (M21: the garden-wall panels, sooted 0.377 of the cleaner, 0.37 to 0.48; saturation 0.84, not the review's 0.6; M22: the sheet's head 0.50 to 0.62 over the top 0.2 to 0.75 m, the right-hand cottage's lower wall 0.90) and made two kinds, `wall_soot` (state weights sooted 1.0 / as built 0.35 / cleaned 0.0, x 0.42, mottle, lower wall) and `wall_head_band` (x 0.56 dry on a wall that is not sooted, x 0.80 on a sooted one, depth profile, ragged by courses, coping scale 0.3). Section 1 records the terrace-front wear layer (patch noise, foot rise, head water paths, house looks) and says which each kind replaces, so no foot or head is darkened twice; the sooted look's 0.57 is lighter than the photograph's 0.42 (D8).
2. **Streaks darker, longer and denser than any source, citing a sheet that shows none.** The three sheet citations and the word 'streaks' in S4 are gone, S4 now says the sheet shows none, D2 is rewritten and D6 added. streak_sill: visible length 0.15 / 0.35 / 0.60 m (M16, M17), one end streak in 8 at 0.8 to 1.4 m, x 0.70 brick, 0.75 painted, 0.72 render, end streaks unequal (checks end_streak_length_ratio, end_streak_width_ratio, rivulet_count 3 to 7). The share of sills with a set is 15 to 60 % (typical 35 %) because the photographs (M23: 1 clear streak in about 30 sill edges, none darker than 0.85 in 13 column tests) show 3 to 15 % on a maintained 2019 street and the review's 50 to 70 % has no source; streak_coping is one finger per leaking joint, 0.3 to 1.0 per metre, full-height runs only under leaking joints and hoppers, the continuous darkening being the head band.
3. **No order of marks and no floor.** A `compose` block (section 4): walls L0 soot, head, damp, splash, paint fade; L1 streaks, algae, handle wear; replacing marks last (salt included, so the band stays pale: the order test in part E shows 1.37 against 0.57 of the clean wall when it is laid first); floor 0.15 on walls; ground in the review's order with a floor of 0.28 rather than 0.35 (the sheet's own stain is 0.295 dry, D12). New checks composed_foot_ratio 0.12 to 0.30 (0.19 measured), composed_wall_min_ratio, composed_salt_ratio, composed_soot_ratio.
4. **Checks that cannot catch a wrong mask, no placement checks, check text unlike the code.** New measures, all in `measure()`: top_edge_std_mm, column_mean_cv (the four foot kinds and the head band), brick_patch_share and brick_cell_std (salt), end_streak_length_ratio, end_streak_width_ratio, rivulet_count, finger_spacing_cv, finger_length_cv, nn_ratio, size_cv, dominant_wavelength_m (paint_fade). Part E builds the nine deliberately wrong masks of the review (and a head band, a flat soot and a cig_end lattice) and every one is refused, by the checks listed in target.json. Nine placement checks (`placement_checks`, part F) pass on a conforming street and each is refused when broken. `check_measures` is now `self_check.MEASURE_DOCS` itself and part A tests that the two are identical.
5. **gutter_grime contradicted its photograph and the scene note.** Rebuilt on a `channel_concrete` surface: M24 measured the channel 1.35 to 1.7 x the road and the strip beside it 0.91 to 0.97. Channel body x 0.85, fringe x 0.92 at its darkest, joint lines x 0.35, gully piles (0.4 m, mask 0.8, 70/62/52), weeds, kerb scuff +8 L*; checks channel_over_road 1.15 to 1.8 (1.47) and fringe_over_road. The review's colour 150/146/140 would put the channel at 2.6 to 3.0 x the road, against the measured 1.4, so the albedo is 116/111/108 (D7).
6. **Wet and dry mixed.** Section 4 states that every Sheet ratio is a wet value and dry = ratio / wet multiplier, used once: splash 0.27 (x 0.75 = 0.20), pavement_stain 0.30 (x 0.80 = 0.24: the sheet's stain measures 0.236, not the review's 0.38, D10), road_blot 0.56 (x 0.9 = 0.50), head band 0.56 (x 0.9 = 0.50), render_patch's dry colour derived from the wet sheet. salt_bloom wet 0.9 (drizzle, damp), 0.6 only in heavy rain with running water. pavement_stain's 'lighter by a third' is deleted. Part A (A27) tests dry x wet = the sheet's ratio.
7. **Iron had no wear.** Kinds `iron_wear` (paint loss 4 to 8 % of a downpipe, patches 20 / 45 / 110 mm, pale ochre, 141/102/72 on the wet sheet and 152/110/78 dry, rust streaks below collars: M25, M13) and `grate_wear` (rust in the slots, polished bar tops, the photographed grate's dull red-brown).
8. **Dropped kinds.** Added as kinds with numbers: `line_wear` (M26: 22 % of a yellow line lost, gaps 20 / 60 / 300 mm), `sign_ghost`, `graffiti_buff`, `handle_wear`, `stone_top_lichen` (olive 103/88/65 on the wet sheet, 115/98/73 dry, 40 to 80 %), `footway_infill` (bitmac 70/68/66 or in-situ concrete, M07b); a `tile_glazed` row for the splash. Nothing is rejected.
9. **Source statements.** S1's 'same in 1990' now lists every colour taken from a scan with why it holds or Judgement; 'no soot on the brick' is gone from S2 (M21 shows soot); plaster_brick_01's Poly Haven tags (plaster, rough, old, moss, sewer, tunnel, trimsheet) are stated (M15, S7) and 'agrees' is removed, its render tones relabelled Judgement; M03 and M05 record their tones; flag_concrete cites M27 (concrete_pavement_02 measured: 134/122/110, L* 52); the crack preview is re-cropped to the left of the map; the seven unmeasured files are listed as looked at and not used.
10. **Places not located.** A `places` block with x ranges from vignette-scene.json (quay end, rank x 3 to 9, fishmonger apron 9 to 15, chandler 40 to 46, yard entrance 21 to 24, gully 12, standing places with counts 5.5 to 6 m each, bus stop zero) and the words made numbers: splash x 1.2 height and x 1.15 strength within 0.6 m of a door or downpipe, weeds 1 per 6 to 10 m, salt weight 1.0 within 12 m of the quay end.
11. **Three numbers that disagreed.** Re-measured and accepted: road_patch seam x 0.70 (0.63 to 0.77) with tint 125/113/100 and infill 0.93 (mask 0.23, checks at 0.2); road_crack main width 15 to 60 mm (15 / 35 / 59 mm on the full 2k map; core 0.23 of the surface); cig_end tan filter row 177/140/110 for 40 % (M06: 31 to 46 %).
12. **Era and content wording.** tyre_scuff no longer calls straight skid pairs modern (they are pre-ABS and out of scope: 0 to 1 at the quay-end corner); the wording slip in paint_flake (a word that implied a minor) is replaced by shopping trolleys and sack barrows; the gum claim is replaced by 'gum staining existed in 1990 but grew later', the tiers lowered (open footway 0.5 to 2 per m2, door apron 4 to 8, bus stop 0); poster sizes are double crown 0.76 x 0.51 m and quad crown 1.02 x 0.76 m; the content-rule sentence in section 4 and one litter-variant name are reworded; part A (A25) searches target.json and TARGET.md for every word of that kind.
13. **Narrow notes (not counted by the review).** Per-channel tint stated (the builder applies mark_lin / surface_lin per channel); one surface per decal stated; `tile_glazed` row added; B1 now accepts an implied multiplier within 12 % (was a factor 1.6) and C15 allows 0.15 (was 0.17) while using the wet multiplier; asphalt_dry is the median 89/86/80 of the three mid scans (the first pass used their mean).

