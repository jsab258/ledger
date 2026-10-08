# 23 kinds of seeded greyscale wear mask, each with its rule of place, size and shape in metres, density, tone per surface, wet and dry look, texel scale and checks, from 20 measurements on CC0 photographs and the Hook sheet; real road and pavement wear is low-contrast and broad, wall feet and streaks follow the Hook sheet's heavier mood, and nothing from 2000s Britain or America is in it.

Wear on Quay Street (the Hook, Meridian; 1990, Britain, port town) for unit 4.5. Written 8 October 2026, cloud week 42, by the wear target writer. Companion files in this folder: `target.json` (every number below, for a script), `target_drawing.py` (draws each kind's shape envelope at real scale from `target.json` alone), `self_check.py` (tests the target against its own photograph measurements and for internal consistency). Previews of the measured photographs are in `production/previews/cloud-week/refs/wear/`.

Self-check: `self_check: passed=700/700 failed=0 (A structure, B tone, C photographs, D envelopes; 23 kinds)` (last run 2026-10-08).

## How to read this

- Every number carries its kind: **Photo** (measured on a photograph or scan; ledger id M01 to M20 in section 3, with method and error), **Sheet** (measured on the Hook sheet, our own mood bar, not a photograph), **Read** (printed in a repository record or a standard), **Derived** (arithmetic on the others), **Judgement** (mine, bounded by the measured numbers; the first things to change on the builder's evidence).
- Units: metres unless a name ends `_mm`. Tones: sRGB 0 to 255 for colour; a linear-light multiplier on the surface's albedo; L* is CIE D65. Masks are greyscale 0 to 1 (0 nothing, 1 the kind's full effect).
- A mask is not a colour. The builder colours it by surface from each kind's `tone` table. For a **darkening** mark (multiplier below 1): `albedo = surface * lerp(1, albedo_mult_linear, mask * strength)` with the mark's dirt tint; for a **replacing** mark (multiplier 1.0, salt, patch, gum, paper): `colour = lerp(surface, mark_srgb, mask * strength)`. Strength is the house's wear (0.55 to 1.0, `production/specs/street-wear.json`) times the side weight in each kind's rule.
- The four layers of the asset plan (SUMMARY.md section 8): **L0** in the materials (height-gradient foot bands, broad mottle), **L1** rule-placed wall decals, **L2** ground marks written once into the ground's virtual texture, **L3** a few hand-placed hero decals (the Hook sheet's pale patch on the left gable; Mickey's wall foot). Each kind below says which.

## 1. What the street has today, and what is missing

Read from `tools/street_wear.py`, `tools/make_wear_masks.py`, `production/specs/street-wear.json`, and looked at in `production/previews/morning-hook-day-2026-10-08.jpg`, `morning-reverse-day-2026-10-08.jpg`, `front-foot-wear-2026-10-07.jpg` and the Hook sheet.

- **Built:** eight kinds (puddle, streak, algae, splash, wash, damp, oil, soot), 159 decals over 13 houses, one picture a kind (three for streaks and puddles), masks cut from ambientCG's Leaking005 and SurfaceImperfections003/012. ambientCG's metadata (reached today) says all three are generated (PBRProcedural or PBRApproximated), not photographs of wear.
- **On the frames of 8 October:** the brick reads new and even; no foot band on any brick wall (the Hook sheet's gable foot is black to 0.33 m); no streaks under any sill or coping; the stallriser feet carry a faint noisy fringe and the front-foot picture's 'chip box' (a rectangular band, 0.565 to 0.655 m) is the only paint wear; the footways are clean even slabs of one tone with no stain, no patch, no crack, no gum, no ends; the road has puddles and lines but no oil, no scuff, no reinstatement, no crack; kerbs and gully are clean; downpipes have no rust or green.
- **Missing, by kind:** 17 of the 23 below do not exist at all (salt_bloom, rust_bleed, paint_flake, paint_fade, render_crack, render_patch, poster_remnant, bird_dropping, gum, cig_end, pavement_stain, flag_patch_crack, road_blot, tyre_scuff, road_patch, road_crack, gutter_grime); the other 6 exist in a weaker form (wall_foot_splash is today's splash, wall_foot_damp is the damp, streak_sill is the streak, streak_coping is the wash, algae_downpipe is the algae, road_oil is the oil). Today's soot (chimney-stack tops) and puddles are outside this family or have their own research (WET-ROAD).
- **Why they read as faint:** one picture a kind, strength 0.4 to 1.0 everywhere, and edges softer than a photograph's. The measured road is low contrast (4 to 12 % of the area marked) but its marks are many and of several sizes; the measured walls have a hard-edged flake (0.4 mm) beside a soft damp blotch (19 mm). The target gives each kind its own edge.

## 2. Sources

Photographs for measuring only, from free licences; none is placed in the game, traced into a texture or fed to an image model. All are modern (2018 to 2026); for each the table says why the wear it shows would look the same in 1990, or not.

| id | what | URL | date read | author | licence | date taken or published | what it shows | used |
|---|---|---|---|---|---|---|---|---|
| S1 | Poly Haven texture scans (CC0), diffuse maps 2k/4k, metric dimensions from the site's asset record | https://polyhaven.com/ and https://api.polyhaven.com/files/<id> | 2026-10-08 | various, per file below | CC0 1.0 | published dates per file below | Close, flat-lit, de-lit scans of worn surfaces at a known metric size (1 to 30 m): the wear's shape, size, share and albedo. Photographed in unknown places (the site gives none), 2018 to 2026. Used for measuring; none is placed in the game, traced into a texture or fed to an image model. | yes |
| S2 | Poly Haven HDRI panoramas of London streets (CC0), Andreas Mischok: urban_street_02 (8k, taken 2019-08-18), urban_street_03 (8k, 2019-09-07), urban_street_01/04, birbeck_street_underpass, bethnal_green_entrance, limehouse (4k) | https://polyhaven.com/hdris, https://api.polyhaven.com/files/<id>, https://api.polyhaven.com/info/<id> | 2026-10-08 | Andreas Mischok | CC0 1.0 | taken 2019, per list below | Real London streets (an estate road and a residential street) re-projected here to ground ortho tiles and wall views. Used to measure ground wear (oil, litter, flags, reinstatement) and one sill streak. | yes |
| S3 | ambientCG metadata API (CC0): creation method of each asset | https://ambientcg.com/api/v2/full_json | 2026-10-08 | ambientCG (Struffelproductions) | CC0 1.0 | n/a | Reached; the images and downloads were NOT (the download redirect and the thumbnail hosts f003.backblazeb2.com and acg-media.struffelproductions.com answer 403 through this cloud's proxy). The metadata says ChewingGum001/002, Leaking001 to 019 and RoadLines006 to 035 are PBRProcedural (generated), SurfaceImperfections001/003 and Scratches003 PBRProcedural, SurfaceImperfections007/012 and Sticker001 PBRApproximated: NOT photographs of real wear, contrary to the brief. Only AsphaltDamageSet001 (atlas), Moss001 and ManholeCover003 to 011 are photogrammetry. The repo's masks (tools/make_wear_masks.py) are made from Leaking005, SurfaceImperfections003 and 012: all procedural or approximated. | metadata only (creation methods) |
| S4 | The Hook sheet (repository file, pass 4) | production/previews/hook-sheet-2026-10-05.jpg | 2026-10-08 | the project | the project's own | 2026-10-05 | The mood bar: wall feet, streaks, wet flags, stains. Not a photograph (generated picture); measured only as 'Sheet'. | yes |
| S5 | Repository records: production/research/asset-plan/SUMMARY.md section 8 and 4-SIGNAGE-AND-WEAR.md, street-wear/PAINTED-FRONTS-2026-10-07.md and WET-ROAD-2026-10-08.md, aaa-street/BRICK-COLOUR-2026-10-08.md, tools/street_wear.py, tools/make_wear_masks.py, production/specs/street-wear.json, ledger/Assets/StreamingAssets/Decals | repo | 2026-10-08 | the project | the project's own | 2026-10-01 to 08 | What exists: eight kinds, one picture each (three streaks), masks from procedural CC0 maps, house wear 0.55 to 1.0. | yes |
| S6 | Search summaries (leads only, no number used from them): Keep Britain Tidy 2017 gum staining on 99 % of main shopping streets; BRE Digest 245 rising damp 'in excess of 1 m' and heritage guidance 0.5 to 1.5 m; sill-run-off mechanism (patent text) | keepbritaintidy.org; designingbuildings.co.uk (DG 245); patents.google.com (DE7911046U1) | 2026-10-08 | various (summaries only) | n/a | n/a | Directions for what to read once the network opens. | no (leads) |

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

**S2, the panoramas (Andreas Mischok, CC0, London; taken and published dates from the site's record):** urban_street_02 (taken 2019-08-18 about 06:45 UTC, published 2019-08-29; overcast; an estate road with brick walls, a wrought-iron fence, litter and a utility reinstatement; 8k used), urban_street_03 (taken 2019-09-07 about 07:46, published 2019-09-26; overcast; a residential street with patched flags, granite kerb, cobble channel, oil-dripped asphalt, stock-brick walls; 8k used), urban_street_01 (taken 2019-08-18, resurfaced street, not used for numbers), urban_street_04 (taken 2019-09-14, sunlit stucco Kensington, not used), birbeck_street_underpass (taken 2019-08-18, graffiti wall, sun-blown, not used for numbers), bethnal_green_entrance (taken 2019-08-18, block paving and leaves, not used), limehouse (taken 2019-05-19, a 1980s-90s Docklands development, clean: the contrast case, not used for numbers). Camera height 1.6 m assumed and proved by the 75 mm yellow line (M04).

**Why the 2019 and later wear is or is not the 1990 wear:** see each source's 'same in 1990' line in `target.json` sources. In short, physical wear (cracks, paint loss, damp, moss, rust, oil drips, kerb litter, flags replaced after utility work, sealed asphalt cracks) looks the same in 1990; what differs is amount (1990 walls sootier, pavements dirtier, cars leakier, and no wash-down culture) and a few 2000s additions that must not appear (section 4).

**Unreached (the network refused, so nothing from them is evidence):**

- commons.wikimedia.org, geograph.org.uk, archive.org, flickr.com, historicengland.org.uk: CONNECT refused (HTTP 000/403), tested 2026-10-08.
- ambientCG image and download hosts (ambientcg.com/get redirect, f003.backblazeb2.com, acg-media.struffelproductions.com): 403. ambientCG Bricks073C/075B/079/094/097, Concrete038/039, PavingStones036/149, Plaster007, Tiles038 are therefore unread.
- Once the network opens, read: Geograph photographs of Hull, Grimsby, Hartlepool, Sunderland, Liverpool dock streets 1985 to 1995 (wall feet, rain streaks, salt bloom, fly-posters, gum on shopping-street flags); BRE Digest 245 full text; Keep Britain Tidy / Defra litter survey 2002 for gum per square metre; British Library 'Britain in the 1980s' street photographs; Historic England archive, John Gay and Eric de Mare collections for soot-blackened brick.

**Leads only (search summaries, no number used):** Search summaries (leads only, no number used from them): Keep Britain Tidy 2017 gum staining on 99 % of main shopping streets; BRE Digest 245 rising damp 'in excess of 1 m' and heritage guidance 0.5 to 1.5 m; sill-run-off mechanism (patent text)

## 3. Measurements, with method and error

**M01. Dry asphalt albedo on eight scans.** Files: asphalt_01; asphalt_02; asphalt_03; asphalt_04; asphalt_06; road_damaged; road_damaged_2; aerial_asphalt_01.

- Method: Central 70 % of each 2k diffuse map; per-channel median; L* from sRGB D65.
- Error: +/-3 sRGB levels (JPEG, unknown colour cast of each scan); scans are de-lit albedo.
- Values: `{"asphalt_01": {"median_srgb": [89, 80, 70], "L_median": 34.5}, "asphalt_03": {"median_srgb": [81, 67, 56], "L_median": 29.5}, "asphalt_06": {"median_srgb": [150, 141, 127], "L_median": 59.0}, "asphalt_02": {"median_srgb": [87, 86, 80], "L_median": 36.3}, "asphalt_04": {"median_srgb": [130, 126, 123], "L_median": 53.1}, "road_damaged": {"median_srgb": [73, 56, 45], "L_median": 25.2}, "road_damaged_2": {"median_srgb": [88, 64, 48], "L_median": 29.4}, "aerial_asphalt_01": {"median_srgb": [97, 92, 97], "L_median": 39.7}}`
- Reading: Worn dry asphalt spans L* 25 to 59, median of the mid scans (asphalt_02, aerial_asphalt_01, asphalt_01) 91/86/82, L* 37.

**M02. Wear marks on a 30 m x 30 m worn road scan (aerial_asphalt_01).** Files: aerial_asphalt_01 4k, 7.32 mm/px.

- Method: L* smoothed 44 mm (removes the aggregate), minus L* smoothed 0.88 m; dark marks = deficit beyond a threshold; connected components; linear = aspect > 6 and length > 0.5 m; cross-profile averaged about the skeleton of the 16 linear marks.
- Error: Thresholds +/-1 L*: share 4.6 % (dL 4) to 23.5 % (dL 1.5). Widths +/-15 mm (7 mm pixel). The tile is a tileable processed scan: spacing of features is the photographer's tile, not a street.
- Values: `{"share_dL1.5": 0.235, "share_dL2.5": 0.125, "share_dL4": 0.046, "blob_eqd_mm_p10_50_90_dL2.5": [160.0, 223.0, 488.0], "blob_n_per_100m2_dL2.5": 99.8, "blob_n_per_100m2_dL4": 40.9, "linear_n_dL2.5": 16, "linear_per_100m2": 1.78, "linear_len_m_p10_50_90": [1.7, 4.0, 8.6], "scuff_fwhm_mm": 90, "scuff_peak_dL": -9.5, "scuff_profile_mm": [0.0, 15.0, 29.0, 44.0, 59.0, 73.0, 88.0, 103.0, 117.0, 132.0, 146.0, 161.0, 176.0, 190.0], "scuff_profile_dL": [-9.53, -8.11, -5.84, -3.94, -2.63, -1.74, -1.21, -0.67, -0.25, -0.01, 0.22, 0.53, 0.68, 0.77]}`
- Reading: Real road wear is low contrast and broad: 4 to 12 % of the area is marked, blobs about 0.22 m, tyre scuffs about 90 mm wide and 2 to 8 m long, with soft edges about 70 mm.

**M03. Cracks in a worn asphalt scan (asphalt_02, 3 m x 3 m).** Files: asphalt_02 2k, 1.46 mm/px.

- Method: Counted by eye on the 1400 px montage with a 3.0 m scale (automatic ridge detection failed on the aggregate and was abandoned): one sealed crack the full 3.0 m, six hairlines 0.2 to 1.8 m, total about 7.3 m.
- Error: +/-30 % on length; the patch was chosen by its photographer as a cracked road, so it is the worst case.
- Values: `{"crack_m_per_m2": 0.8, "main_crack_width_mm": [40, 90], "hairline_width_mm": [2, 6], "detected_local_width_mm_p10_50_90": [2.9, 6.6, 12.1]}`
- Reading: A cracked road carries 0.8 m of crack per m2; typical road 0.1 to 0.4 (Judgement).

**M04. Oil drip speckle on asphalt in a London residential street (urban_street_03, 8k panorama, ground ortho-rectified).** Files: urban_street_03 8k, Andreas Mischok, taken 2019-09-07.

- Method: Panorama re-projected to a top-down ortho tile at 3 mm/px with camera height 1.6 m; scale proved by the yellow kerb line: 24 to 26 px = 72 to 78 mm (line is 75 mm). Dots = pixels darker than 0.85, 0.75, 0.65 of a 25 px median; components of 4 px or more.
- Error: Height 1.6 +/-0.1 m gives +/-6 % on areas and +/-6 % on lengths; dot sizes +/-2 mm (3 mm pixel); threshold changes density by a factor 2.5 (167 to 67 per m2).
- Values: `{"dots_n_rel0.85": 222, "region_m2": 1.33, "per_m2_rel0.85": 167.0, "per_m2_rel0.75": 68.0, "eqd_mm_p10_50_90_rel0.85": [10.6, 16.9, 29.4], "eqd_mm_p10_50_90_rel0.75": [10.3, 13.7, 21.4], "luminance_ratio_in_dots": 0.7, "in_band_per_m2_rel0.75": 153.0, "in_band_per_m2_rel0.85": 377.0, "note_region": "per_m2_* are over the whole 1.33 m2 region of the view, which includes clean asphalt around the dotted band; in_band_* divide by the band's own area (length x width, central 90 % of the dots)", "band_length_m_visible": 1.83, "band_width_m": 0.32}`
- Reading: A parked car's drip band: about 0.3 m x 1.8 m (at least), dots 17 mm, 0.7 of the road's luminance, 154 per m2 inside the band at the darker threshold (379 at the lighter).

**M05. Utility reinstatement in asphalt (urban_street_02, ortho tile).** Files: urban_street_02 8k, Andreas Mischok, taken 2019-08-18.

- Method: Ortho tile 3 mm/px, h 1.6 m: rectangle spans 370 x 360 px; seam darker band 10 to 17 px; grass tufts at 3 corners.
- Error: +/-0.1 m on size (height), +/-10 mm on seam.
- Values: `{"w_m": 1.0, "h_m": 1.1, "seam_mm": [30, 50]}`
- Reading: A cover reinstatement is about 1.0 x 1.1 m with a dark seam of 30 to 50 mm.

**M06. Litter along the kerb and on the road (urban_street_02, rectilinear view yaw -165, pitch -20).** Files: urban_street_02 8k.

- Method: Pieces counted by eye on a marked picture (automatic bright-blob detection also hit aggregate glints and was rejected): kerb strip about 22 pieces over 5 m of kerb, band 0.3 m deep; road 10 pieces over 13.6 m2. Detected bright bits (aggregate included) had size 7.6, 11.2, 27.7 mm at p10/50/90.
- Error: +/-35 % on counts; 8k pixel at 7 m is 5 mm.
- Values: `{"kerb_per_m_of_kerb": 4.4, "kerb_band_depth_m": 0.3, "road_per_m2": 0.7, "piece_mm_p10_50_90": [7.6, 11.2, 27.7]}`
- Reading: The kerb gathers about 4 pieces per metre; open road about 0.7 per m2 (a scruffier estate road; a 1990 shop street would be at or above this).

**M07. Patched flags (urban_street_03, ortho tile of the footway, camera-to-footway 1.48 m).** Files: urban_street_03 8k.

- Method: Six slab samples by rectangle, mean linear luminance and sRGB; dark slabs 0.20 to 0.24, pale 0.34 to 0.42 (same light); shares and cracks by eye over about 18 slabs.
- Error: Luminance ratio +/-0.08; shares +/-10 points; slab size +/-15 % (height of the footway).
- Values: `{"dark_over_pale": 0.58, "dark_srgb": [133, 130, 130], "pale_srgb": [181, 172, 168], "mid_srgb": [176, 165, 161], "share_dark": 0.55, "share_pale": 0.3, "share_mid": 0.15, "cracked_slab_share": 0.11, "slab_m": [0.6, 0.7]}`
- Reading: A 1990-style patched footway has a 0.58 luminance ratio between old and replacement flags and about 1 flag in 9 cracked.

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
- Values: `{"mossy_brick_moss_share": 0.169, "mossy_brick_patch_eqd_mm_p10_50_90": [5.5, 10.2, 31.5], "mossy_brick_edge_mm": 6.7, "brick_moss_001_share": 0.121, "brick_moss_001_eqd_mm_p10_50_90": [5.5, 13.1, 43.4], "brick_moss_001_edge_mm": 9.5, "moss_srgb": [[55, 57, 9], [74, 72, 23]], "foot_green_excess_lowest_0.45m": 26, "green_excess_above": 15, "foot_L_from_to": [47, 26], "foot_band_m": 0.45, "foot_srgb_at_0.3m": [97, 96, 41], "foot_srgb_at_0": [62, 64, 14]}`
- Reading: Moss fills 12 to 17 % of a wet brick wall as joint lines; on render the lowest 0.45 m goes olive-green and 20 L* darker.

**M16. Drip streaks hanging from a horizontal joint (concrete_layers, 1.55 m, 0.757 mm/px).** Files: concrete_layers 2k, Amal Kumar, 2024-05-02.

- Method: L* minus its 12 px mean < -1.5 / -2.5; vertical opening (3 x 1); components with height >= 4 x width and >= 60 mm.
- Error: Counts +/-40 % (stronger streaks only; by eye 10 to 15 per metre); widths +/-2 mm.
- Values: `{"detected_per_m_of_joint": 7.7, "width_mm_p10_50_90": [10.6, 15.1, 19.7], "length_mm_p10_50_90": [78.0, 87.0, 137.0], "by_eye_length_m_max": 0.45}`
- Reading: Individual rivulets are 10 to 20 mm wide, 0.09 to 0.45 m long, 8 to 15 per metre of joint, both dark and lime-pale.

**M17. Streak under a sill bracket on yellow stock brick (urban_street_03, yaw 105, bay window).** Files: urban_street_03 8k.

- Method: Scale from brick courses (75 mm gauge, 30 px at 2x crop); column under the central bracket 40 px wide, 180 px long; mean luminance of the column against flanks 0.97; darkest bricks 0.80 to 0.90.
- Error: Size +/-30 % (by eye on courses), tone +/-0.05.
- Values: `{"width_m": 0.1, "length_m": 0.45, "column_Y_ratio": 0.97, "darkest_brick_Y_ratio": [0.8, 0.9]}`
- Reading: On a maintained 2019 London brick wall the sill-bracket streak is faint: 0.10 m x 0.45 m, 3 to 20 % darker. The Hook sheet bar is heavier; the target sits between.

**M18. Hook sheet, left gable foot (mood bar, not a photograph).** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Column-median luminance profile of columns 15 to 170, rows 380 to 730; brick course from autocorrelation (11 px = 75 mm, so 6.8 mm/px); wall reference rows 430 to 600.
- Error: +/-1 course (75 mm); tone +/-0.05.
- Values: `{"mm_per_px": 6.8, "wall_median_srgb": [107, 52, 32], "dark_band_rows": [668, 716], "dark_band_height_m": 0.33, "dark_band_Y_ratio": [0.12, 0.3], "salt_band_courses": [2, 3], "salt_band_height_m": [0.15, 0.22], "salt_band_from_foot_m": [0.26, 0.46], "salt_band_Y_ratio": [0.57, 0.75], "salt_band_srgb_bright_quartile": [107, 91, 83], "salt_band_mean_srgb": [81, 60, 52]}`
- Reading: The sheet's foot: 0.33 m black band (0.12 to 0.30 of the wall), a 0.15 to 0.22 m grey-white band on its upper flank (0.26 to 0.46 m), a ragged top stepping by courses.

**M19. Hook sheet, pale patch on the left gable.** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Patch size from courses: 3.8 courses high, about 1.3 brick lengths wide; colour mean of its core.
- Error: +/-30 %.
- Values: `{"patch_srgb": [175, 140, 92], "patch_L": 60.6, "wall_L": 26.6, "dL": 34.0, "size_m": [0.28, 0.3]}`
- Reading: A buff mortar patch 0.3 m square, 34 L* lighter than the wall.

**M20. Hook sheet, right pavement stains and road blots.** Files: production/previews/hook-sheet-2026-10-05.jpg.

- Method: Colour of one brown stain 85/60/44 against flag 136/129/131; sizes relative to a 0.6 m flag by eye.
- Error: +/-30 % size; 5 per 10 m2 by counting 7 stains over about 14 m2.
- Values: `{"stain_srgb": [85, 60, 44], "stain_L": 27.6, "flag_srgb": [136, 129, 131], "flag_L": 54.7, "dL": -27.1, "stain_size_m": [0.15, 0.45], "stains_per_10m2": 5, "oil_blots_on_road_m": [0.1, 0.2]}`
- Reading: The mood bar's pavement carries brown stains 27 L* darker than the flags, 0.15 to 0.45 m, about 5 per 10 m2.

## 4. Rules that apply to every kind

**Scene and camera** (from SCENE-SLOTS.md and vignette-scene.json): Quay Street, the Hook, Meridian; 48 m, 6.0 m carriageway (two 3.0 m lanes, crossfall 1:40, crown 75 mm above the channel), footways 2.0 m (1:40), kerb upstand 0.125, channel course 0.255 wide. East side: six-bay Victorian shop parade, 6 m bays, faces WEST (the wet side in the UK's prevailing south-westerly). West side: shop block (north half) and plain terraces (quay end), faces EAST. Eye height 1.65 to 2.0 m, vertical field of view 46 to 60 degrees, frame [2560, 1440] px, so one screen pixel subtends 0.557 mrad: 1122 px per metre of mask at 1.6 m, 816 at 2.2 m (the nearest ground the camera sees), 180 at 10 m. A mask texel finer than the screen's is wasted; a coarser one shows.

**Texel rule:** each kind states its smallest feature and the px/m it needs: at least 6 texels across the smallest feature, never above the screen's 1122 px/m at 1.6 m. Features that fall under 2 screen pixels at 10 m (rust trickles, cracks, rivulets, oil dots, cigarette ends) keep their texels but the builder fades their strength or widens them beyond 6 to 8 m (each kind's note).

**Sides:** the east parade faces west, the wet side in the UK's prevailing south-westerly (Judgement, no number): streaks, algae, flaking and rust get weight 1.0 there, 0.6 to 0.8 on the west block (which faces east and is drier but sooted).

**Wet and dry:** wet stone is 0.68 of dry albedo and roughness 0.45; water 0.04 (Read: WET-ROAD-2026-10-08.md). Each kind states its own wet albedo multiplier and roughness change; dirt marks darken a further 10 to 25 % when wet, salt and paper change most.

**Era rules (1990, Britain, an old port quarter):**

- Heavy: 1990 walls were sootier and 1990 pavements dirtier than any modern panorama measured (the 2019 London photographs are the cleanest end of the range). Where a photograph and the Hook sheet disagree, the target sits between them, nearer the sheet for walls (the sheet is the mood bar) and nearer the photograph for ground marks.
- Nothing later than 1990, or unusual in an old quarter then (Judgement on each): no tactile or blister paving, red or green anti-skid surfacing, thermoplastic bus lanes, pressure-washed stripes, bike-lane green, spray utility markings, cycle stands, wheelie-bin lines, vape and mask litter, QR-code stickers, anti-bird spikes, uPVC white fronts.
- No American marks: no wide white parking T-markings, no painted crosswalk zebras in white 12-inch bars, no manhole lids with US castings, no fire-hydrant paint, no yellow centre-line pairs, no graffiti throw-ups in bubble-letter style (the street's graffiti are the canon's five tags, in another family).
- No alcohol or gambling traces: no bottles, cans, bar-mats, betting slips or scratch cards in the litter (canon content rule). Tobacco ends are allowed.

**Content rule (canon):** no alcohol or gambling traces (no bottles, cans, tops, bar mats, betting slips or scratch cards in any litter or poster remnant); tobacco is allowed; no children's marks (no chalk hopscotch, no play drawings); no cypher, crown or makers' marks. 'LITTER' is fine on a bin; this family writes no words.

## 5. The kinds

| id | layer | decal frame (m) | density | px/m (min / use) | variants |
|---|---|---|---|---|---|
| `streak_sill` | L1 rule-placed wall decal | 1.6 x 1.7 | 0.35 to 0.8 sets per metre of facade wall (typical 0.55) | 600 / 800 | 6 |
| `streak_coping` | L1 rule-placed wall decal | 4.0 x 2.6 | 1.4 to 4.0 fingers per metre of feature length (typical 2.5) | 250 / 300 | 5 |
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
| `gum` | L2 ground | 1.0 x 1.0 | 1.0 to 12.0 per m2 of footway (typical 4.0) | 500 / 700 | 8 |
| `cig_end` | L2 ground | 1.0 x 1.0 | 3 to 6 per metre of kerb (band) and per m2 (aprons, open) (typical 4.4) | 750 / 1000 | 10 |
| `pavement_stain` | L2 ground | 1.0 x 1.0 | 3 to 10 blots per 10 m2 of footway (typical 6) | 250 / 400 | 6 |
| `flag_patch_crack` | L2 ground | 3.0 x 2.4 | 0.3 to 0.5 share of flags (typical 0.45) | 800 / 1120 | 6 |
| `road_oil` | L2 ground | 2.6 x 0.6 | 0.5 to 1.0 speckle bands per standing place (typical 0.8) | 600 / 1000 | 5 |
| `road_blot` | L2 ground | 1.2 x 1.2 | 1 to 3 dark blots per standing place (typical 2) | 250 / 400 | 5 |
| `tyre_scuff` | L2 ground | 3.0 x 1.0 | 1 to 2 scuffs per junction mouth (typical 1.5) | 100 / 150 | 4 |
| `road_patch` | L2 ground | 1.8 x 1.8 | 1 to 3 per 48 m street (typical 2) | 250 / 400 | 5 |
| `road_crack` | L2 ground | 3.0 x 3.0 | 2 to 5 stamps per 48 m street (typical 3) | 800 / 1120 | 5 |
| `gutter_grime` | L2 ground | 2.0 x 0.75 | 1.0 to 1.0 continuous along the kerb (typical 1.0) | 300 / 500 | 4 |

### `streak_sill`: Rain streaks under window sills

- **Layer:** L1 rule-placed wall decal (projected, normal-faded)
- **Where (the rule):** Origin on the sill's lower edge. Two end streaks start under the sill's two ends (where the sill sheds its water); 3 to 7 thin rivulets start at brackets, joints and chips along the sill; a faint wash spans the sill. Everything runs straight down (gravity), tilted at most 3 degrees. Never rotate a streak.
  - Feature: the lower edge of every window sill, upper floors and shop transom ledges alike; one set per sill
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0 to 1.6 below the sill's lower edge; stop at the next ledge, string course or door head if nearer
  - Sides: East parade fronts face west, the wet side of a British port: weight 1.0. West block fronts face east: weight 0.7. Gable ends facing the street: 0.8.
  - Footfall and wet: Not footfall. Wet climate: always present; darker and glossier when wet; the lower half dries first.
  - Density: 0.35 to 0.8 sets per metre of facade wall (typical 0.55) [Judgement: one set per sill, sills about 1.25 to 2.8 m apart along the parade (a 6 m bay with two or three openings)]
  - With house wear: set count fixed; strength x house wear (0.55 to 1.0 in street_wear.json); length x (0.7 + 0.3 x wear)
- **Decal frame:** x -0.8 to 0.8 m, y -1.7 to 0.0 m; origin: origin = the middle of the sill's lower edge; y is up, so runs fall to negative y; decal is yaw-faced to the wall, not rotated
- **Shape and size (real units):** envelope primitive `streak_set`; envelope parameters `{"sill_width_m": [0.9, 1.2], "end_streaks": {"n": 2, "width_frac_of_sill": [0.06, 0.14], "length_m": [0.5, 1.4], "src": "Photo M17 (bracket streak 0.10 m x 0.45 m) widened for the wet side; Judgement"}, "rivulets": {"n": [3, 7], "width_m": [0.01, 0.03], "length_m": [0.15, 0.6], "src": "Photo M16 (10.6 to 19.7 mm wide, 8 per metre of joint, 0.09 to 0.45 m long)"}, "wash": {"height_m": [0.1, 0.3], "overhang_m": 0.1, "level": 0.18, "src": "Judgement"}, "wander_m": [0.005, 0.03], "taper": 0.55, "fade_exponent": 1.4, "core_level": 0.9, "head_fraction_full": 0.12}`
  - Geometry numbers: `{"streak_width_to_sill_width": {"end": [0.06, 0.14], "rivulet": [0.01, 0.03], "src": "Judgement bounded by Photo M16, M17"}, "streak_length_m": {"p10": 0.35, "p50": 0.8, "p90": 1.4, "src": "Judgement; Photo M17 gives 0.45 m on a dry modern street, Sheet shows streaks reaching the next opening"}, "aspect_length_to_width": [4, 30], "edge_10_90_mm": [12, 40], "edge_src": "Photo M13 15.6 mm, M12 19 mm (soft-edged stains)", "darkest_at": "the head, directly under the sill; the mask falls as exp(-(t/L)^1.4) down the run (never darkest at the bottom: the 4 October review failed that)", "branching": "a rivulet may split once in its lower half with a 12 to 25 degree fork, one in four streaks", "edge_for_envelope_mm": 20}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [100, 67, 58] | dirty darker brown | 0.55 | -11 | Judgement between Photo M17 (0.8 to 0.97, modern London) and Sheet M18 (0.12 to 0.30 at the foot); 1990 walls are sootier |
  | brick_painted | [152, 108, 93] | [110, 93, 83] | grey-brown dirt | 0.65 | -9 | Judgement |
  | render_cream | [214, 200, 178] | [182, 159, 133] | grey-brown dirt | 0.62 | -14 | Judgement; Photo M12 stained cream is 144/124/97 against 222/205/182 clean (x0.45 on Y) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.3, "note": "wet film darkens the run by about a fifth and makes it glossier than the dry wall around it"}`. [Read: WET-ROAD-2026-10-08.md (wet stone x0.68 albedo, roughness 0.45); Judgement for walls]
- **Texel scale:** smallest feature 10 mm; mask needs at least 600 px/m, use 800; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: mask 1.4 m x 1.6 m at 800 px/m is 1120 x 1280; at 10 m the fine rivulets are 2 screen pixels so keep them at 0.15 to 0.4 strength
- **Variants:** 6 seeded masks; they differ by 3 end-streak widths x 2 rivulet layouts (3 or 6 rivulets); mirror in x allowed; no rotation; strength, length and tint from the house seed [Derived: asset plan note 4 asks 4 to 6 masks a kind]
- **Why 1990 Britain:** Rain streaks are weather, not fashion; what dates a street is how heavy they are: uncleaned brick and render, no drip-tray flashings or plastic sills on this old-quarter parade (Judgement; no 1990 photograph reached).
- **Not modern, not American:** No clean white rendered strips beneath dark streaks, no neat symmetrical streak pairs of equal length, no uniform streaks across the whole sill width.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | streak_aspect_p50 | streak_aspect | mask | `{"thr": 0.25, "min_length_m": 0.1, "stat": "p50"}` | 4 | 30 | Judgement |
  | streak_width_mm_p50 | streak_width_mm | mask | `{"thr": 0.25, "stat": "p50"}` | 10 | 140 | Photo M16/M17 |
  | streak_length_m_p90 | streak_length_m | mask | `{"thr": 0.25, "stat": "p90"}` | 0.4 | 1.3 | Judgement/Photo M17: the end streaks (the two longest per sill) |
  | streak_length_m_p50 | streak_length_m | mask | `{"thr": 0.25, "stat": "p50"}` | 0.12 | 0.8 | Judgement/Photo M16: rivulets 0.09 to 0.45 m |
  | vertical_within_deg | verticality_deg | mask | `{"thr": 0.25}` | 0 | 8 | Derived: gravity |
  | fade_ratio_tail_over_head | fade_ratio | mask | `{"thr": 0.25}` | 0.0 | 0.6 | Derived: darkest at the head |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.3, "band_hi": 0.9, "axis": "x"}` | 12 | 45 | Photo M12, M13 |
  | coverage_of_decal_at_0.25 | coverage | mask | `{"thr": 0.25}` | 0.02 | 0.12 | Derived: 2 end streaks 0.1 m x 0.5 m + rivulets over the 1.6 x 1.7 m frame |
  | peak_mask | mask_max | mask | `{}` | 0.8 | 1.0 | Judgement |

### `streak_coping`: Streaks and wash under copings, ledges, string courses and gutter joints

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** Fingers of dirt hang from the feature's lower edge; they are heaviest under joints (coping joints every 0.6 to 0.9 m, gutter joints, stop-ends, hopper heads) and under the lowest point of a sagging gutter. A continuous soft wash sits between fingers. Straight down, no rotation.
  - Feature: under chimney-stack copings, parapet and gable copings, cornices, string courses, eaves gutters at their joints and stop-ends, hopper overflows
  - Surfaces: brick_red, brick_painted, render_cream, stone_sill
  - Height: 0 to 2.5 below the feature (to 3.0 under a leaking gutter joint); stop at the next opening
  - Sides: East parade (west-facing): 1.0; west block: 0.7; gables: 0.9
  - Footfall and wet: Wet climate only; the wash is the street's most visible 'wear at a glance' (Jafar, 2 October)
  - Density: 1.4 to 4.0 fingers per metre of feature length (typical 2.5) [Judgement; Photo M16 gives 8 detected per metre at a concrete joint, thinned for building scale]
- **Decal frame:** x -2.0 to 2.0 m, y -2.6 to 0.0 m; origin: origin = the middle of the feature's lower edge; runs fall to negative y
- **Shape and size (real units):** envelope primitive `streak_set`; envelope parameters `{"span_m": [1.5, 4.0], "fingers": {"n_per_m": [1.4, 4.0], "width_m": [0.04, 0.2], "length_m": [0.6, 2.5]}, "wash": {"height_m": [0.25, 0.6], "overhang_m": 0.0, "level": 0.18}, "wander_m": [0.01, 0.05], "taper": 0.6, "fade_exponent": 1.2, "core_level": 0.85, "head_fraction_full": 0.18}`
  - Geometry numbers: `{"streak_length_m": {"p10": 0.6, "p50": 1.3, "p90": 2.5, "src": "Judgement; Sheet: gable streaks run 1 to 3 m"}, "streak_width_m": {"p10": 0.04, "p50": 0.1, "p90": 0.2, "src": "Judgement"}, "aspect_length_to_width": [3.5, 40], "edge_10_90_mm": [25, 70], "edge_src": "Judgement: wider streaks have softer edges (Photo M13: 15.6 mm for 24 mm wide streaks; scaled)", "darkest_at": "the head; coverage between fingers about 0.3 near the head and 0 by 0.8 m down", "edge_for_envelope_mm": 40}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [99, 68, 58] | dirty darker brown | 0.55 | -11 | Judgement |
  | brick_painted | [152, 108, 93] | [111, 93, 83] | grey-brown dirt | 0.65 | -9 | Judgement |
  | render_cream | [214, 200, 178] | [180, 157, 130] | grey-brown dirt | 0.6 | -15 | Judgement; Photo M12 |
  | stone_sill | [170, 166, 158] | [136, 131, 122] | soot grey | 0.6 | -13 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.3}`. [Read: WET-ROAD-2026-10-08.md; Judgement]
- **Texel scale:** smallest feature 40 mm; mask needs at least 250 px/m, use 300; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 5 seeded masks; they differ by finger count (3, 5, 8), joint rhythm, one with a heavy stop-end blotch; mirror allowed; tile along the feature by joint rhythm (not seamless: stamp) [Derived]
- **Why 1990 Britain:** Cast-iron and asbestos-cement gutters leaked at their joints, which is why the fingers hang from joints; a PVC replacement run may sit among them (Judgement: no 1990 photograph reached).
- **Not modern, not American:** No identical fingers at identical spacing; no stained zone ending in a ruler-straight horizontal line.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | streak_aspect_p50 | streak_aspect | mask | `{"thr": 0.25, "min_length_m": 0.3, "stat": "p50"}` | 3.5 | 40 | Judgement: visible length at mask 0.25 is 0.4 to 1.2 m on fingers 0.04 to 0.2 m wide |
  | streak_length_m_p50 | streak_length_m | mask | `{"thr": 0.25, "stat": "p50"}` | 0.6 | 2.2 | Judgement |
  | vertical_within_deg | verticality_deg | mask | `{"thr": 0.25}` | 0 | 8 | Derived: gravity |
  | fade_ratio_tail_over_head | fade_ratio | mask | `{"thr": 0.25}` | 0.0 | 0.6 | Derived |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.3, "band_hi": 0.9, "axis": "x"}` | 20 | 80 | Judgement |
  | coverage_of_decal_at_0.25 | coverage | mask | `{"thr": 0.25}` | 0.03 | 0.2 | Derived: 4 to 10 fingers 0.1 m x 1.0 m over the 4.0 x 2.6 m frame |

### `wall_foot_splash`: Pavement splash and grime band on walls, stallrisers and door bottoms

- **Layer:** L0 in the material (height gradient) plus L1 decal for the ragged top edge
- **Where (the rule):** A band from the pavement upward. Full strength from 0 to 0.24 m, 0.85 at 0.33 m, 0.45 at 0.49 m, 0.15 at 0.61 m, gone by 0.75 m; the top edge is ragged and steps in brick-course heights (75 mm) on brick, in small blotches on painted timber. Heavier at door steps, downpipe feet and where the pavement is lowest.
  - Feature: the foot of every wall that meets the pavement: brick walls, stallrisers, pilaster plinths, door leaves' bottom rails, door steps
  - Surfaces: brick_red, brick_painted, render_cream, timber_paint_dark, timber_paint_light, stone_sill
  - Height: 0 to 0.75 above the pavement (the Hook sheet gable: black to 0.33 m, half gone at 0.49 m)
  - Sides: Both sides; heavier on the east parade where the pavement is wetter (north-facing step shadow not modelled)
  - Footfall and wet: Footfall and wet: strongest at shop doors and the quay-end corner where people stand; splash is wet-pavement spatter from boots and rain bounce.
  - Density: 1.0 to 1.0 full length of every pavement-side wall (typical 1.0) [Derived: it is continuous]
  - With house wear: height x (0.8 + 0.2 x wear); strength x wear
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 0.75 m; origin: origin = pavement line at the left end of a 2.0 m tile; y up the wall; tiles in x
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.24, "level": 1.0}, {"h_m": 0.33, "level": 0.85}, {"h_m": 0.49, "level": 0.45}, {"h_m": 0.61, "level": 0.15}, {"h_m": 0.75, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.02, 0.08], "wavelength_m": [0.15, 0.6], "src": "Sheet M18: ragged top stepping by brick courses"}, "fingers": {"n_per_m": 3, "length_m": [0.05, 0.25], "width_m": [0.02, 0.08]}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.24, 0.33, 0.49, 0.61, 0.75], "mask": [1.0, 1.0, 0.85, 0.45, 0.15, 0.0], "src": "Sheet M18: luminance ratio 0.12 to 0.19 below 0.24 m, 0.30 at 0.33 m, 0.57 at 0.49 m, 0.85 at 0.61 m, 0.95 above 0.8 m, inverted through the 0.20 multiplier; Photo M15 (algae/damp band 0.45 m, gone by 0.6 m) agrees"}, "profile_tolerance": 0.15, "edge_10_90_mm": [200, 450], "edge_src": "the whole fall-off, Sheet M18: 1.0 at 0.24 m to 0.15 at 0.61 m; inside it the ragged top steps by one 75 mm course (Sheet M18)", "ragged_step_mm": [30, 120], "tileable": "horizontally, seamless, 2.0 m period; vertical profile fixed", "edge_for_envelope_mm": 40}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [52, 43, 37] | soot black-brown | 0.2 | -24 | Sheet M18: foot Y ratio 0.12 to 0.30 of wall; Judgement 0.20 (photographs show none on the maintained estate brick, M17) |
  | brick_painted | [152, 108, 93] | [87, 74, 63] | dirty brown | 0.4 | -17 | Judgement |
  | render_cream | [214, 200, 178] | [152, 129, 107] | dirty brown | 0.4 | -26 | Judgement; Photo M15 (plaster foot L* 47 to 26) |
  | timber_paint_dark | [52, 64, 88] | [42, 47, 59] | grimed dark | 0.55 | -8 | Judgement; Fresh Fish review: foot 8 L* below top (PAINTED-FRONTS-2026-10-07.md) |
  | timber_paint_light | [222, 218, 206] | [162, 151, 133] | dirty grey-brown | 0.45 | -24 | Judgement |
  | stone_sill | [170, 166, 158] | [121, 115, 106] | soot grey | 0.45 | -20 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.75, "roughness_delta": -0.35, "note": "splash band glints when wet; the Hook sheet's foot reads black and slightly shiny"}`. [Sheet; Read WET-ROAD]
- **Texel scale:** smallest feature 25 mm; mask needs at least 320 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: tile 2.0 m x 0.75 m at 400 px/m = 800 x 300
- **Variants:** 5 seeded masks; they differ by top-edge noise seed, finger count, two with a door-step notch; tile horizontally [Derived]
- **Why 1990 Britain:** Splash and soot at wall feet were normal on uncleaned brick: traffic grime and the soot of the coal era. A pristine foot is the modern giveaway (Judgement; the Hook sheet is the evidence: its gable foot is black to 0.33 m).
- **Not modern, not American:** No clean wall foot beside a dark pavement; no uniform gradient ending in a straight line.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | foot_profile | foot_profile | mask | `{"points": [[0.05, 0.85, 1.0], [0.2, 0.85, 1.0], [0.33, 0.6, 1.0], [0.49, 0.25, 0.65], [0.61, 0.03, 0.35], [0.78, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Sheet M18, Photo M15 |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 500}` | 200 | 450 | Sheet M18: 1.0 at 0.24 m falling to 0.15 at 0.61 m (the whole fall-off); the ragged step inside it is 75 mm |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived |

### `wall_foot_damp`: Soot and damp at wall feet: rising damp, tide-line and algae gradient

- **Layer:** L0 in the material (soft, broad) plus L1 decal on masonry
- **Where (the rule):** Where a wall is damp (3 walls in 10 to 8 in 10): a broad, soft, mottled darkening from 0.3 m to 1.2 m with a damp 'tide line' at 0.8 to 1.2 m and a green tint in the lowest 0.45 m on render. It sits on top of the splash band and only above 0.6 m is it alone. Plus black soot streaks 0.3 to 1.0 m long running up from the foot beside downpipes.
  - Feature: brick and rendered walls standing directly on the pavement without a damp-proof plinth; heaviest on the quay-end and the shaded gables
  - Surfaces: brick_red, brick_painted, render_cream
  - Height: 0.15 to 1.2 above the pavement; strongest 0.3 to 0.9
  - Sides: West block (faces east, drier but sooted): 1.0; east parade: 0.9; gable ends facing the street (shaded): 1.1
  - Footfall and wet: Wet climate; port town (tide-borne salts, see salt_bloom). Not footfall.
  - Density: 0.3 to 0.8 share of wall length (typical 0.5) [Judgement: share of wall length with an active damp band (the Hook sheet's left gable shows none above 0.8 m); BRE DG 245 (search summary only) places rising damp 0.5 to 1.5 m, more than 1 m on unprotected masonry]
  - With house wear: height x wear; strength x wear
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 1.6 m; origin: origin = pavement line; y up the wall; tiles in x
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.3, "level": 0.8}, {"h_m": 0.8, "level": 0.5}, {"h_m": 1.2, "level": 0.15}, {"h_m": 1.5, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.05, 0.2], "wavelength_m": [0.3, 1.2]}, "fingers": {"n_per_m": 1.5, "length_m": [0.15, 0.5], "width_m": [0.04, 0.15]}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.3, 0.8, 1.2, 1.5], "mask": [0.8, 0.8, 0.5, 0.15, 0.0], "src": "Judgement bounded by Photo M15 (green/dark band 0.45 m on plaster) and the search lead BRE DG 245 (0.5 to 1.5 m)"}, "profile_tolerance": 0.2, "edge_10_90_mm": [700, 1500], "edge_src": "the whole fall-off, 0.8 at 0.3 m to 0.15 at 1.2 m; Photo M15 gradient length; Judgement", "mottle": "low-frequency noise at 0.3 to 0.6 m wavelength, amplitude +/- 0.2 of the mask", "tileable": "horizontally, 2.0 m period", "edge_for_envelope_mm": 150}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [89, 67, 57] | damp brown | 0.5 | -12 | Judgement; Sheet M18 grey salt band sits just above |
  | brick_painted | [152, 108, 93] | [105, 92, 78] | damp grey-brown | 0.62 | -10 | Judgement |
  | render_cream | [214, 200, 178] | [148, 142, 86] | damp olive-brown | 0.45 | -23 | Photo M15: plaster L* 47 to 26 over the lowest 0.5 m; green excess 25 against 14 above |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.85, "roughness_delta": -0.15}`. [Judgement]
- **Texel scale:** smallest feature 75 mm; mask needs at least 120 px/m, use 200; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by tide-line height and noise seed; tile horizontally [Derived]
- **Why 1990 Britain:** Rising damp and sooted feet were the normal condition of unrestored Victorian masonry (Judgement); a later damp-proof course stops the damp but does not clean the brick.
- **Not modern, not American:** No sharp horizontal tide line; no even gradient.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | foot_profile | foot_profile | mask | `{"points": [[0.15, 0.5, 1.0], [0.6, 0.3, 0.7], [1.2, 0.02, 0.35], [1.6, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Judgement bounded by Photo M15 |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 1200}` | 700 | 1500 | Judgement: 0.8 at 0.3 m falling to 0.15 at 1.2 m |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |

### `salt_bloom`: Salt bloom (efflorescence) on brick, lime runs and white tide-marks

- **Layer:** L1 rule-placed wall decal
- **Where (the rule):** A pale band of whitened bricks sitting on the upper flank of the dark foot band, 2 to 3 brick courses high (0.15 to 0.22 m) from 0.26 m, broken into brick-sized patches with a ragged top at 0.46 to 0.7 m; plus 0 to 2 lime runs per sill: thin pale lines 5 to 20 mm wide and 0.1 to 0.5 m long.
  - Feature: low brickwork near the quay, the quay-end corner and the quay-facing gables; below leaking sills and copings as thin white lime runs
  - Surfaces: brick_red, brick_painted
  - Height: 0.26 to 0.70 above the pavement (band); runs 0 to 0.5 below their source
  - Sides: Quay-end and the west block's quay gable: 1.0; elsewhere 0.4
  - Footfall and wet: A port-town (salt-laden air and tidal ground water) effect; strongest when the wall is drying, so weakest in a long wet spell and invisible on a wet wall (it dissolves and darkens).
  - Density: 1.0 to 3.0 patches per metre of foot length (typical 2.0) [Sheet M18: whitened bricks fill 2 courses of the 7-course affected foot; Judgement]
  - With house wear: strength x wear
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 0.9 m; origin: origin = pavement line; the band starts at 0.25 m; follows brick bond offsets
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.22, "level": 0.0}, {"h_m": 0.26, "level": 0.6}, {"h_m": 0.46, "level": 0.6}, {"h_m": 0.56, "level": 0.1}, {"h_m": 0.7, "level": 0.0}], "top_edge": {"step_m": 0.075, "amplitude_m": [0.03, 0.1], "wavelength_m": [0.2, 0.7]}, "brick_patches": {"brick_m": [0.215, 0.075], "fill_fraction": 0.55}, "fingers": {"n_per_m": 1.0, "length_m": [0.1, 0.5], "width_m": [0.005, 0.02]}}`
  - Geometry numbers: `{"height_profile": {"h_m": [0.0, 0.22, 0.26, 0.46, 0.56, 0.7], "mask": [0.0, 0.0, 0.6, 0.6, 0.1, 0.0], "src": "Sheet M18 overlay (the grey-white bricks lie between 0.26 and 0.46 m above the foot, on the upper flank of the dark band, 2 to 3 courses, desaturated)"}, "profile_tolerance": 0.3, "edge_10_90_mm": [8, 60], "edge_src": "Sheet M18 patches follow brick edges (hard); fringe soft", "edge_for_envelope_mm": 25}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | brick_red | [140, 87, 70] | [150, 138, 128] | dull grey-white | 1.0 | 16 | Sheet M18 band (107/91/83 bright quartile of a 81/60/52 mean on a 107/52/32 wall); mark replaces, mixed at mask x 0.6 |
  | brick_painted | [152, 108, 93] | [190, 182, 170] | chalky white | 1.0 | 25 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.15, "note": "powdery, rougher than the brick"}`; wet: `{"albedo_mult_on_tone": 0.45, "roughness_delta": -0.3, "note": "mostly vanishes: salts dissolve; leaves a dull darker patch"}`. [Judgement]
- **Texel scale:** smallest feature 20 mm; mask needs at least 300 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by patch layout, run count; stamps that follow the brick bond (offset by 0.0375 m every course) [Derived]
- **Why 1990 Britain:** Efflorescence is as old as brick; on an uncleaned port-town wall re-pointed in hard cement mortar it shows more (Judgement; the Hook sheet shows it).
- **Not modern, not American:** Not white paint, not graffiti-buffing grey patches; salt follows bricks, not rectangles.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | coverage_of_decal_at_0.4 | coverage | mask | `{"thr": 0.4}` | 0.04 | 0.12 | Derived: a 0.14 m band x 2.0 m x 55 % brick fill over 1.8 m2 |
  | ragged_edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 200}` | 15 | 100 | Sheet M18 (patch top edge ragged 30 to 100 mm) |
  | peak_mask | mask_max | mask | `{}` | 0.5 | 0.85 | Judgement |
  | foot_profile | foot_profile | mask | `{"points": [[0.15, 0.0, 0.05], [0.38, 0.12, 0.6], [0.8, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Sheet M18 |

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
  | render_cream | [214, 200, 178] | [142, 145, 77] | olive green | 0.45 | -23 | Photo M15 (plaster foot 97/96/41 to 62/64/14) |
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
- **Where (the rule):** Loss concentrates at the horizontal surfaces and the lowest 0.5 m (sills, rails, door bottoms, stallriser feet), where water lies: patches 10 to 250 mm (median 17 mm flakes, a few larger sheets), hard-edged, showing undercoat, bare wood or old colour; crazing (craquelure) cells 0.14 to 0.23 m across on old render paint. Share of a worn painted surface: 3 to 10 %, up to 40 % on a neglected sill or door foot.
  - Feature: painted sills, window frames' lower rails, door bottoms and kick plates, stallrisers, fascia ends and undersides, pilaster plinths, painted render and painted brick
  - Surfaces: timber_paint_dark, timber_paint_light, brick_painted, render_cream
  - Height: mostly 0 to 0.9 and on sills at any height; fascias get edge chips only
  - Sides: East parade (wet) 1.0; west block 0.8; empty unit (bay 3, whitewashed, to let) 1.4 (neglected)
  - Footfall and wet: Footfall: door bottoms and kick plates (boots) and stallrisers where bags and pushchairs knock; wet: sills and rails.
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
  | brick_red | [140, 87, 70] | [205, 184, 140] | pale buff mortar | 1.0 | 33 | Sheet M19: patch 175/140/92 (L* 60.6) on a wall of L* 26.6 under the sheet's light (+34); albedo set to 205/184/140 so that the L* difference on the target's brick albedo (L* 42) is also about +33 |
  | render_cream | [214, 200, 178] | [150, 140, 126] | grey patch | 1.0 | -22 | Photo M11 (exposed render/brick 163/150/136 to 121/90/69) |
  | brick_painted | [152, 108, 93] | [170, 150, 120] | pale buff | 1.0 | 13 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.1}`; wet: `{"albedo_mult_on_tone": 0.75, "roughness_delta": -0.15, "note": "fresh mortar and bare render absorb water and darken strongly, so the patch reads less pale when wet"}`. [Judgement]
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
- **Where (the rule):** Layers of torn paper: a rectangle 0.4 to 1.0 m across (poster sheet 0.75 x 0.5 m or 1.0 x 0.75 m, A1 or double crown), 20 to 70 % intact, torn along diagonal edges and lifted at the top; thin pale paste ghost around it; a few bare corners and strips. Invented local campaigns only (RULINGS 3 Oct: poll-tax posters, never real parties).
  - Feature: hoardings, the blank side gable, boarded windows, the empty unit's glass and door, the shuttered bay, electrical boxes at the quay end
  - Surfaces: brick_red, render_cream, timber_paint_dark, timber_paint_light
  - Height: 0.9 to 2.6 (as high as a person's arm reaches with a ladder-free paste brush)
  - Sides: Both; heaviest on the empty unit (bay 3) and the quay-end gable
  - Footfall and wet: Footfall; paper swells and sags when wet: wet poster is darker, translucent and hangs lower
  - Density: 0 to 2 sites per facade (typical 1) [Judgement]
- **Decal frame:** x -0.55 to 0.55 m, y -0.45 to 0.45 m; origin: origin = site centre
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.4, 1.0], [0.3, 0.75]], "ragged_mm": [20, 120], "drip_tail": {"length_m": [0.0, 0.0], "width_m": [0.0, 0.0]}, "layers": {"n": [2, 4], "intact_fraction": [0.2, 0.7]}, "loss_blobs": {"eqd_m": [0.02, 0.05, 0.15], "n_per_m2": [5, 15]}}`
  - Geometry numbers: `{"sheet_size_m": [[0.75, 0.5], [1.0, 0.75]], "edge_10_90_mm": [2, 10], "edge_src": "Judgement: torn paper edge is hard", "paste_ghost_width_mm": [10, 40], "edge_for_envelope_mm": 4}`
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
  - Sides: Quay-end and the quay-facing side 1.0; inland end 0.4
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
- **Where (the rule):** Poisson-disc scatter on the footway with density weighted by footfall; discs 12 to 30 mm, trodden flat; never on the road, rarely on the kerb top; clusters of 2 to 4 within 0.3 m near doors.
  - Feature: pavement flags, densest in front of shop doors, at the kerb crossing points, at the bus stop and the newsagent's door, around bins and benches, outside the cab office rank
  - Surfaces: flag_concrete, kerb_granite
  - Height: ground
  - Sides: East footway (shops) 1.0; west footway 0.7; zero under 0.4 m of the wall (nobody walks there)
  - Footfall and wet: Footfall is the driver. Wet changes nothing in position; the stain darkens and glints.
  - Density: 1.0 to 12.0 per m2 of footway (typical 4.0) [Judgement; search lead only: Keep Britain Tidy 2017 found gum staining on 99 % of main shopping streets (no per-m2 figure reached); no photograph measured (the 2019 London panoramas show a low-gum residential street)]
  - Density tiers: `{"shop door apron (1.5 m radius)": [8, 12], "kerb crossing and bus stop": [5, 8], "open footway": [1, 3], "wall foot strip": [0, 0.5]}`
- **Decal frame:** x 0.0 to 1.0 m, y 0.0 to 1.0 m; origin: a 1.0 m ground tile; the builder scatters stamps by the density tier, this is the reference tile at the typical density
- **Shape and size (real units):** envelope primitive `points`; envelope parameters `{"shape": "disc", "eqd_mm": [12, 20, 32], "aspect": [1.0, 1.5], "per_m2": [1.0, 12.0], "cluster": {"prob": 0.3, "n": [2, 4], "radius_m": 0.3}, "ring": {"width_mm": 3, "level": 0.4}}`
  - Geometry numbers: `{"eqd_mm": {"p10": 12, "p50": 20, "p90": 32, "src": "Judgement; Sheet M20 pavement spots 150 to 400 mm are stains, not gum"}, "edge_10_90_mm": [1, 4], "edge_src": "Judgement: a gum disc has a hard edge and a slightly paler rim", "edge_for_envelope_mm": 2}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [62, 58, 54] | dark grey-black, paler rim | 1.0 | -28 | Sheet M20: dark pavement spots L* 27.6 on flags L* 54.7 (-27); Judgement for gum itself |
  | kerb_granite | [128, 126, 122] | [66, 62, 58] | dark grey-black | 1.0 | -26 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.3, "note": "glossy against the matte flag: roughness 0.45 against 0.85"}`; wet: `{"albedo_mult_on_tone": 0.9, "roughness_delta": -0.45, "note": "roughness 0.25; glints under the street lamps"}`. [Judgement]
- **Texel scale:** smallest feature 12 mm; mask needs at least 500 px/m, use 700; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: one stamp sheet of 8 gum discs, each 64 x 64 texels for a 40 mm square (1600 px/m local) is fine; ground virtual texture needs 700 px/m at least on shop aprons
- **Variants:** 8 seeded masks; they differ by disc, oval, with-a-tail, pair, with-a-pale-rim, pink-tinted (rare), black-and-flat, tiny; free rotation and mirror (it lies flat) [Derived]
- **Why 1990 Britain:** Chewing gum was as common in 1990 as now; the mark is the same grey-black and the shape does not change (Judgement; no 1990 photograph with gum reached).
- **Not modern, not American:** No tactile paving studs nearby; no wheelie-bin lines; no 'Gum Targets' campaign stencils.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 80}` | 14 | 28 | Judgement |
  | count_per_m2_open_footway | count_per_m2 | mask | `{"thr": 0.5, "min_area_mm2": 80}` | 1.0 | 12.0 | Judgement |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 0.8 | 5 | Judgement |
  | coverage_of_decal | coverage | mask | `{"thr": 0.5}` | 0.0001 | 0.006 | Derived: 4 x 3.1e-4 m2 |

### `cig_end`: Cigarette ends, matchsticks and small litter

- **Layer:** L2 ground (stamped), plus PCG-scattered instances at the kerb band
- **Where (the rule):** Two bands: (1) kerb band, 0 to 0.3 m from the kerb foot, 3 to 6 pieces per metre of kerb, piled at gully grates; (2) doorway aprons, 4 to 10 per m2 within 1.2 m of a shop door; open footway and open road 0.3 to 1.0 per m2. Each end 8 mm x 25 to 30 mm; white filter or tan filter, some burnt-orange, some flattened. Tobacco is allowed (canon).
  - Feature: the kerb foot (channel) and the strip 0 to 0.3 m inside it, shop doorways and their steps, the cab-office rank, under bins, drain grates, the pavement edge by the wall
  - Surfaces: flag_concrete, asphalt_dry, kerb_granite
  - Height: ground
  - Sides: East footway (shop doors) 1.0; west 0.7; kerb band both sides
  - Footfall and wet: Footfall + wind + runoff: ends drift to the channel and bunch at gullies; wet makes them dark, soggy, and paler tobacco-brown.
  - Density: 3 to 6 per metre of kerb (band) and per m2 (aprons, open) (typical 4.4) [Photo M06 (urban_street_02, counted by eye: 22 pieces over 5 m of kerb = 4.4 per m; road 0.7 per m2; +/-35 %)]
  - Density tiers: `{"kerb band per metre of kerb": [3, 6], "shop door apron per m2": [4, 10], "open footway per m2": [0.3, 1.0], "open road per m2": [0.2, 0.8]}`
- **Decal frame:** x 0.0 to 1.0 m, y 0.0 to 1.0 m; origin: a 1.0 m ground tile at 4 per m2; the kerb band is separate (per metre of kerb)
- **Shape and size (real units):** envelope primitive `points`; envelope parameters `{"shape": "rect", "size_mm": [[6, 8, 10], [18, 26, 32]], "per_m2": [0.3, 10], "band": {"length_m": 2.0, "depth_m": 0.3, "per_m": [3, 6]}}`
  - Geometry numbers: `{"piece_size_mm": {"eqd_p10": 8, "eqd_p50": 11, "eqd_p90": 28, "src": "Photo M06 detection of bright bits: 7.6, 11.2, 27.7 mm"}, "cig_dimensions_mm": [8, 27], "cig_src": "Read/Judgement: UK cigarette 8 mm across, butt 25 to 30 mm", "edge_10_90_mm": [0.8, 3], "edge_src": "Judgement", "edge_for_envelope_mm": 1.5}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [228, 222, 208] | white filter, tan tip | 1.0 | 36 | Photo M06 (bright litter on grey surfaces); Judgement |
  | asphalt_dry | [91, 86, 82] | [232, 228, 216] | white filter | 1.0 | 54 | Photo M06 |
  | kerb_granite | [128, 126, 122] | [222, 214, 198] | white filter | 1.0 | 33 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.55, "roughness_delta": -0.3, "note": "soaked ends go dull brownish-grey, not white"}`. [Judgement]
- **Texel scale:** smallest feature 8 mm; mask needs at least 750 px/m, use 1000; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 10 seeded masks; they differ by straight end, bent end, flattened, burnt-tip, matchstick, small paper scrap, blank crisp-packet corner (no brand marks), sweet-wrapper corner, leaf, pair; free rotation and mirror [Derived]
- **Why 1990 Britain:** Smoking was normal in the street and doorways; filter tips were tan 'cork-pattern' or white; no vaping debris, no blister packs, no plastic bottle caps in numbers, no coffee-cup lids. Paper and wrapper scraps only: no cans, bottles or tops (canon: no alcohol), no betting slips.
- **Not modern, not American:** No face-mask litter, no vape pods, no energy-drink cans, no takeaway coffee cups.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | blob_eqd_mm_p50 | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 30}` | 8 | 22 | Photo M06 |
  | count_per_m2_open_footway | count_per_m2 | mask | `{"thr": 0.5, "min_area_mm2": 30}` | 0.3 | 10.0 | Photo M06, Judgement |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 0.6 | 4 | Judgement |

### `pavement_stain`: Dark and brown stains on the flags; grime halos round drains; wet-looking joints

- **Layer:** L2 ground
- **Where (the rule):** Stains: irregular blots 0.08 to 0.45 m, 3 to 10 per 10 m2 of footway; grime halo round every drain and cover: a ring 0.15 to 0.35 m wide, dark and gradually fading; flag joints 3 to 10 mm wide darker than the flag by 8 to 20 L* and 2x wider where water stands.
  - Feature: open flags (random), shop doorways and steps (spilled water, wet boots), under downpipe outfalls, around gully grates and cast-iron covers (halo), along the footway edge by the kerb, flag joints
  - Surfaces: flag_concrete, kerb_granite
  - Height: ground
  - Sides: East 1.0; west 0.9
  - Footfall and wet: Footfall + wet: stains read strongly when wet (the Hook sheet's brown blots are rust and mud wash). Dry: faint.
  - Density: 3 to 10 blots per 10 m2 of footway (typical 6) [Sheet M20 (7 stains in about 14 m2 of the right pavement: 5 per 10 m2); Judgement]
- **Decal frame:** x -0.5 to 0.5 m, y -0.5 to 0.5 m; origin: origin = stain or drain centre
- **Shape and size (real units):** envelope primitive `blob_field`; envelope parameters `{"region_m": [1.0, 1.0], "anchor": "centre", "blobs": {"n": [1, 3], "eqd_m": [0.08, 0.18, 0.45], "aspect": [1.0, 3.0], "orient": "free"}, "halo": {"width_m": [0.15, 0.35], "level": 0.5}, "joints": {"width_mm": [3, 10], "level": 0.6}}`
  - Geometry numbers: `{"blob_eqd_mm": {"p10": 80, "p50": 180, "p90": 450, "src": "Sheet M20 (relative to a 0.6 m flag: 0.15 to 0.7 of a flag width); Photo M12 blotch p50 42 mm, p90 171 mm"}, "edge_10_90_mm": [8, 60], "edge_src": "Sheet M20 ragged but wet-soft; Photo M12 19 mm", "edge_for_envelope_mm": 25}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | flag_concrete | [134, 123, 110] | [101, 72, 54] | brown, rust and mud | 0.38 | -19 | Sheet M20: stain 85/60/44 (L* 27.6) on flag 136/129/131 (L* 54.7) |
  | kerb_granite | [128, 126, 122] | [98, 90, 82] | dark brown-grey | 0.5 | -14 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0, "note": "dry: lighter by a third, matte"}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.4, "note": "wet: darker and shiny; puddles sit on top (separate puddle masks)"}`. [Read WET-ROAD-2026-10-08 + Judgement]
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
  - Geometry numbers: `{"slab_classes": {"dark": {"srgb": [134, 129, 128], "share": 0.55, "mask_level": 0.0}, "mid": {"srgb": [156, 147, 144], "share": 0.15, "mask_level": 0.5, "src": "Judgement: between"}, "pale": {"srgb": [173, 164, 161], "share": 0.3, "mask_level": 1.0}}, "slab_size_m": [0.6, 0.6], "slab_src": "Photo M07 (about 0.6 to 0.7 m, +/-15 %); Read: BS 7263 flags 600 x 600 or 450 x 600 mm, pre-metric 24 in x 18 in", "dark_to_pale_luminance_ratio": 0.58, "ratio_range": [0.5, 0.7], "crack_width_mm": [2, 4], "joint_width_mm": [3, 8], "edge_10_90_mm": [1, 8], "edge_src": "Photo M07: slab edges are crisp; tone change is flat per slab", "edge_for_envelope_mm": 4}`
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
  - Feature: kerbside parking positions (the engine position of each parked car), the rank outside the cab office, the loading apron of the fishmonger and ship's chandler
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Kerbside standing both sides; the rank (east, quay end) 1.5; the loading apron 1.3
  - Footfall and wet: Traffic: strongest where vehicles stand; wet: dots look darker and slicker.
  - Density: 0.5 to 1.0 speckle bands per standing place (typical 0.8) [Photo M04 (one band per car; 154 dots per m2 inside the band at rel < 0.75, 379 at rel < 0.85); Judgement]
- **Decal frame:** x 0.0 to 2.6 m, y -0.3 to 0.3 m; origin: origin = start of the drip band on the engine line; x along the car (parallel to the kerb), y across it
- **Shape and size (real units):** envelope primitive `speckle_band`; envelope parameters `{"length_m": [1.0, 2.5], "width_m": 0.32, "dot_eqd_mm": [10.6, 16.9, 29.4], "density_per_m2": [120, 260]}`
  - Geometry numbers: `{"dot_eqd_mm": {"p10": 10.6, "p50": 16.9, "p90": 29.4, "src": "Photo M04 (rel luminance < 0.85, n 222 in 1.33 m2)"}, "band_width_m": {"p5_95": 0.32, "src": "Photo M04"}, "band_length_m": {"visible": 1.83, "src": "Photo M04, cut by the frame: at least"}, "edge_10_90_mm": [2, 8], "edge_src": "Photo M04: the dots are crisp", "edge_for_envelope_mm": 6}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [91, 86, 82] | [75, 72, 72] | dark grey-black | 0.7 | -6 | Photo M04: dots at 0.70 of the luminance around them |

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

### `road_blot`: Oil blots and smears, and broad dark patches on the road

- **Layer:** L2 ground (virtual texture)
- **Where (the rule):** Two tiers. Dark blots 0.10 to 0.20 m, black, irregular, 1 to 3 per standing place (the Hook sheet's black blots beside the yellow lines); broad low-contrast patches 0.15 to 0.5 m (median 0.22 m), 0.4 to 1.0 per m2 of trafficked carriageway, 3 to 6 L* darker than the road around (Photo M02); strongest in the wheel paths (two bands 0.15 m wide, 1.5 m apart, along each lane).
  - Feature: kerbside standing places, the rank, loading aprons, where lorries stop, the first metre beyond a gully grate
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Both; the rank (east, quay end) 1.5; the loading apron 1.3
  - Footfall and wet: Traffic; wet: dark blots read as shiny black; the broad patches nearly vanish (wet asphalt is dark everywhere).
  - Density: 1 to 3 dark blots per standing place (typical 2) [Sheet M20 (dark blots), Photo M02 (broad patches: 100 per 100 m2 at dL* 2.5, 41 at dL* 4)]
  - Density tiers: `{"dark blots 0.10 to 0.20 m, per standing place": [1, 3], "broad low-contrast patches 0.15 to 0.5 m, per m2 of trafficked road": [0.4, 1.0]}`
- **Decal frame:** x -0.6 to 0.6 m, y -0.6 to 0.6 m; origin: origin = the middle of the blot group
- **Shape and size (real units):** envelope primitive `blob_field`; envelope parameters `{"region_m": [1.0, 1.0], "anchor": "centre", "blobs": {"n": [1, 3], "eqd_m": [0.1, 0.2, 0.45], "aspect": [1.0, 2.2], "orient": "free"}}`
  - Geometry numbers: `{"blob_eqd_mm": {"p10": 100, "p50": 200, "p90": 450, "src": "Sheet M20 (0.10 to 0.20 m) and Photo M02 (p10 160, p50 223, p90 487 mm at dL 2.5)"}, "edge_10_90_mm": [10, 60], "edge_src": "Photo M02 (the whole-tile mark edge is soft, about 70 mm); Sheet M20 blots ragged but crisp: 10 to 25 mm", "edge_for_envelope_mm": 20}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [91, 86, 82] | [64, 61, 60] | black-grey, glossy | 0.5 | -11 | Sheet M20 (road blots read black on a grey road); Photo M02 for the paler broad patches (mult 0.85 to 0.9 at the low tier) |

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
  - Feature: junction mouths and the corner at the quay end, the kerb where vehicles pull in, the turn into the yard, the rank's pull-up
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
  | asphalt_dry | [91, 86, 82] | [78, 75, 74] | darker road | 0.75 | -5 | Photo M02: scuff deepest -9.5 L* (selection-biased; typical -4 to -9) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0, "note": "no change: the scuff is invisible on wet asphalt (strength x 0.3)"}`. [Judgement]
- **Texel scale:** smallest feature 90 mm; mask needs at least 100 px/m, use 150; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: soft 70 mm edges: 150 px/m is enough
- **Variants:** 4 seeded masks; they differ by arc radius 2, 3, 5 m and one near-straight; mirror in x [Derived]
- **Why 1990 Britain:** Rubber scuffs from turning vehicles are the same in any decade (Judgement).
- **Not modern, not American:** No skid marks from ABS-era stops (long straight stripes) and no 'wheelie' donuts.
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
- **Shape and size (real units):** envelope primitive `rect_patch`; envelope parameters `{"patch_m": [[0.9, 1.2], [0.9, 1.2]], "ragged_mm": [20, 60], "seam_mm": [30, 50], "infill_level": 0.55}`
  - Geometry numbers: `{"cover_reinstatement_m": {"w": 1.0, "h": 1.1, "tol": 0.1, "src": "Photo M05 (ortho 3 mm/px)"}, "seam_mm": [30, 50], "seam_src": "Photo M05", "edge_10_90_mm": [5, 25], "edge_src": "Photo M05", "edge_for_envelope_mm": 15}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [91, 86, 82] | [68, 64, 60] | dark seam, darker infill | 0.55 | -10 | Photo M05 seam (dark, about 0.5); Judgement for the infill (mask 0.55 x this) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.1}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.35, "note": "seam is a gutter; water collects and reflects as a thin dark line"}`. [Read WET-ROAD + Judgement]
- **Texel scale:** smallest feature 30 mm; mask needs at least 250 px/m, use 400; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: the seam is 30 to 50 mm wide: 400 px/m gives 12 to 20 texels
- **Variants:** 5 seeded masks; they differ by cover reinstatement square, trench across lane, trench along channel, pothole patch, patch with weeds at the corners; free yaw within +/-15 degrees of the street axis [Derived]
- **Why 1990 Britain:** Utility reinstatements with a bitumen seam and no hot-rolled infill are the normal state of an old-quarter street (Judgement). Coloured anti-skid surfacing and thermoplastic patches are not part of this street.
- **Not modern, not American:** No red or green anti-skid; no uniform black new surface; no spray-painted utility markings (white, blue or pink).
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | patch_eqd_mm | blob_eqd_mm | mask | `{"thr": 0.5, "stat": "p50", "min_area_mm2": 100000}` | 800 | 1500 | Photo M05 (1.0 x 1.1 m cover) |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 3 | 40 | Photo M05 |
  | coverage_of_frame | coverage | mask | `{"thr": 0.5}` | 0.25 | 0.6 | Derived: a 0.9 to 1.2 m patch in a 1.8 x 1.8 m frame |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived: the seam is level 1 |

### `road_crack`: Cracks in the asphalt: a sealed main crack and hairlines

- **Layer:** L2 ground (virtual texture) with a 1 to 4 mm height groove
- **Where (the rule):** A cracked section: one sealed main crack 1.6 to 2.4 m long, 40 to 90 mm wide (tar overband), running roughly along or across the lane; 2 to 5 hairlines 2 to 6 mm wide, 0.3 to 1.2 m long, branching at 12 to 25 degrees. In the worst stretches 0.8 m of crack per m2 (Photo M03); typical road 0.1 to 0.4 m per m2 (Judgement), so place the stamp sparsely: about 1 per 10 to 20 m of carriageway.
  - Feature: carriageway: the worst stretches near the channel and the crown, along trench edges, round covers; sealed cracks along old joints
  - Surfaces: asphalt_dry
  - Height: ground
  - Sides: Both lanes; the channel strip along the kerb more cracked
  - Footfall and wet: Traffic and frost: wet: cracks hold water and read black
  - Density: 2 to 5 stamps per 48 m street (typical 3) [Judgement; Photo M03 for the stamp's own content (0.8 m per m2)]
- **Decal frame:** x -1.5 to 1.5 m, y -1.5 to 1.5 m; origin: origin = the middle of the cracked section; the main crack runs roughly vertically (along the lane)
- **Shape and size (real units):** envelope primitive `crack_lines`; envelope parameters `{"region_m": [2.5, 2.5], "note": "the cracked section is 2.5 x 2.5 m (0.8 m per m2, Photo M03); the decal frame is 3 x 3 m", "main": {"length_m": [1.6, 2.4], "width_mm": [40, 90]}, "hairlines": {"n": [2, 5], "length_m": [0.3, 1.2], "width_mm": [2, 6], "branch_prob": 0.3, "step_m": 0.03}}`
  - Geometry numbers: `{"crack_length_m_per_m2": {"worst": 0.8, "tol": 0.25, "typical": [0.1, 0.4], "src": "Photo M03 (counted by eye, 7.3 m in 9 m2)"}, "main_crack_width_mm": [40, 90], "hairline_width_mm": [2, 6], "edge_10_90_mm": [1, 12], "edge_src": "Photo M03: hairlines are crisp, the sealed band's edge a few mm soft", "edge_for_envelope_mm": 2}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [91, 86, 82] | [48, 47, 46] | black sealed crack | 0.3 | -17 | Photo M03: sealed crack L* about 10 on a surface of L* 36 (mult about 0.3) |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": -0.1}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.4, "note": "cracks hold water: roughness 0.04 in the groove"}`. [Read WET-ROAD (water 0.04) + Judgement]
- **Texel scale:** smallest feature 3 mm; mask needs at least 800 px/m, use 1120; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m. Note: hairlines need 1120 px/m; fade the stamp's hairlines out by 8 m (LOD), keep the sealed main crack
- **Variants:** 5 seeded masks; they differ by main crack along the lane, across the lane, curved, with a branch, hairline-only [Derived]
- **Why 1990 Britain:** Sealed bitumen cracks and hairlines on worn road asphalt are the same in any decade (Judgement).
- **Not modern, not American:** No perfectly straight computer cracks, no pothole with square edges.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | crack_length_m_per_m2_of_frame | crack_length_per_m2 | mask | `{"thr": 0.5}` | 0.3 | 1.2 | Photo M03: 0.8 in the 2.5 x 2.5 m section, diluted by the 3 x 3 m frame |
  | crack_width_mm | crack_width_mm | mask | `{"thr": 0.5}` | 2 | 40 | Photo M03: hairlines 2 to 6 mm, main 40 to 90 mm; the median lies between |
  | edge_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9}` | 1 | 15 | Photo M03 |
  | peak_mask | mask_max | mask | `{}` | 0.9 | 1.0 | Derived: cracks are level 1 |

### `gutter_grime`: Gutter, channel and kerb-foot grime; litter band

- **Layer:** L2 ground (virtual texture) plus L0 kerb material
- **Where (the rule):** A continuous dark band the width of the channel, plus a ragged dark fringe on the asphalt 0.1 to 0.3 m wide; piles of grit, leaf mulch and litter at gully grates (0.4 m radius); kerb face scuffed by tyres to a pale polished streak at 0.05 to 0.12 m up; weeds in the channel at 1 per 6 to 10 m in the open stretches.
  - Feature: the kerb channel course (0.255 m wide, SCENE-SLOTS), the kerb face, gully grates, the strip of asphalt 0.3 m beyond the channel
  - Surfaces: asphalt_dry, kerb_granite
  - Height: ground to 0.125 (kerb upstand)
  - Sides: Both kerbs; the west side's dropped crossover (x 22.5) is cleaner but has a scuffed taper block
  - Footfall and wet: Wet climate and runoff: the channel is where the street's dirt goes; wet it reads as a black gleaming gutter line.
  - Density: 1.0 to 1.0 continuous along the kerb (typical 1.0) [Judgement; Photo M06 (kerb strip litter) and the Hook sheet's grimed drain covers]
- **Decal frame:** x 0.0 to 2.0 m, y 0.0 to 0.75 m; origin: origin = the kerb foot; y runs from the kerb foot into the carriageway; tiles along x
- **Shape and size (real units):** envelope primitive `foot_band`; envelope parameters `{"levels": [{"h_m": 0.1, "level": 0.9}, {"h_m": 0.25, "level": 0.7}, {"h_m": 0.45, "level": 0.2}, {"h_m": 0.6, "level": 0.0}], "top_edge": {"step_m": 0.0, "amplitude_m": [0.03, 0.1], "wavelength_m": [0.3, 1.5]}, "fingers": {"n_per_m": 1.0, "length_m": [0.05, 0.2], "width_m": [0.03, 0.12]}}`
  - Geometry numbers: `{"band_width_m": {"channel": 0.255, "fringe": [0.1, 0.3], "src": "SCENE-SLOTS channel course 0.255 m; Photo M06 kerb litter band 0.3 m"}, "height_profile": {"h_m": [0.0, 0.1, 0.25, 0.45, 0.6], "mask": [0.9, 0.9, 0.7, 0.2, 0.0], "src": "Derived: channel 0.255 m plus fringe; axis here is distance from the kerb foot"}, "profile_tolerance": 0.2, "edge_10_90_mm": [250, 600], "edge_src": "Judgement: grime fades into the asphalt (the whole fall-off)", "tileable": "along the kerb, 2.0 m period", "edge_for_envelope_mm": 100}`
- **Tone on each surface** (the surface's own albedo from section 6; mark colour at mask 1; multiplier on its linear albedo; L* change):

  | surface | surface sRGB | mark sRGB | plain name | albedo multiplier | dL* | source |
  |---|---|---|---|---|---|---|
  | asphalt_dry | [91, 86, 82] | [64, 61, 58] | black grit and mulch | 0.5 | -11 | Judgement; Sheet: grimed channel and drain covers |
  | kerb_granite | [128, 126, 122] | [100, 95, 86] | dark grey | 0.55 | -12 | Judgement |

- **Wet versus dry:** dry: `{"albedo_mult_on_tone": 1.0, "roughness_delta": 0.0}`; wet: `{"albedo_mult_on_tone": 0.8, "roughness_delta": -0.55, "note": "the channel is a wet black line; roughness 0.04 in standing water"}`. [Read WET-ROAD (water 0.04)]
- **Texel scale:** smallest feature 25 mm; mask needs at least 300 px/m, use 500; the screen resolves 1120 px/m at 1.6 m and 180 at 10 m.
- **Variants:** 4 seeded masks; they differ by fringe noise seed; gully pile; tile along the kerb [Derived]
- **Why 1990 Britain:** Channels were swept rarely; cast-iron gully grates with silt traps; weeds. No mechanical-sweeper streak patterns (2000s).
- **Not modern, not American:** No sharp yellow-line edge exactly on the channel line unless the lines family says so.
- **Checks** (run on a generated mask; measure ids in section 8):

  | check | measure | applies to | parameters | min | max | source |
  |---|---|---|---|---|---|---|
  | foot_profile | foot_profile | mask | `{"points": [[0.05, 0.7, 1.0], [0.25, 0.4, 0.9], [0.45, 0.02, 0.4], [0.62, 0.0, 0.08]], "axis": "rows_from_bottom"}` | 0.0 | 1.0 | Derived |
  | tile_seam | tile_seam | mask | `{"axis": "x"}` | 0.0 | 1.6 | Derived: seam difference / inner adjacent difference, 1 when seamless |
  | profile_10_90_mm | edge_10_90_mm | mask | `{"band_lo": 0.1, "band_hi": 0.9, "axis": "y", "reach_mm": 500}` | 250 | 600 | Judgement: 0.9 at 0.10 m falling to 0.2 at 0.45 m: grime fades into the asphalt |

## 6. Surfaces and colours

| surface | albedo sRGB | plain name | source |
|---|---|---|---|
| brick_red | [140, 87, 70] | weathered red facing brick | Read: one measured brick, production/research/aaa-street/BRICK-COLOUR-2026-10-08.md (0.262/0.095/0.061 linear) |
| brick_painted | [152, 108, 93] | painted brick or masonry, dull red-pink or cream | Photo M08 (peeling_painted_wall paint, 152/108/93) |
| render_cream | [214, 200, 178] | cream or whitewashed render | Photo M12 (concrete_wall_003 clean paint, 222/205/182) pulled 4 % toward weathered |
| timber_paint_dark | [52, 64, 88] | dark navy or deep-red shopfront paint (stallriser, pilaster, fascia) | Judgement; the Hook sheet's Mickey's blue |
| timber_paint_light | [222, 218, 206] | cream or white painted timber and window frames | Judgement |
| stone_sill | [170, 166, 158] | pale grey stone or cast-stone sill and coping | Judgement; Poly Haven concrete_pavement-like greys |
| flag_concrete | [134, 123, 110] | concrete paving flag, weathered | Photo M07 (concrete_pavement_02 median 134/123/110) |
| asphalt_dry | [91, 86, 82] | worn road asphalt, dry | Photo M01 (median of asphalt_02, aerial_asphalt_01, asphalt_01: 87/86/80, 97/92/97, 89/80/70) |
| kerb_granite | [128, 126, 122] | granite or concrete kerb | Judgement |
| iron_black | [35, 35, 36] | black painted cast iron (downpipe, railing) | Judgement |

These are references for the tone tables only (the street's own brick and paint colours belong to the brick and shopfront families and win where they differ; the multipliers carry over).

## 7. Where the photographs, the sheet and the books disagree, and what was chosen

- **D1.** brief ('Leaking001-006, ChewingGum001-002 ... are photographs of real wear') against ambientCG's own metadata (creationMethod PBRProcedural): chose the metadata: these are generated, so they are not measured; they may still be used as CC0 shapes by unit 4.5 but never as evidence.
- **D2.** Hook sheet (black foot band 0.33 m at 0.12 to 0.30 of the wall; heavy streaks) against the 2019 London photographs (clean brick, streak 0.8 to 0.97, no foot band on the estate wall): chose the sheet for walls (it is the mood bar, and the 2019 walls are cleaned or maintained): foot multiplier 0.20, the middle of the sheet's 0.12 to 0.30; streak multiplier 0.55, between the photographs (0.8 to 0.97) and the sheet's foot (0.2), because no streak was measured on the sheet.
- **D3.** existing masks (high-contrast, 0.4 to 1.0 strength everywhere, 8 kinds) against Photo M02/M04 (real road wear is low contrast: dL 2 to 9, marks 5 to 12 % of the area): chose the photographs for the road and pavement: the mask peaks are 0.7 to 0.9 but the marks cover little of the area (a drip-band stamp 0.2 to 3 % of its frame, a tyre-scuff arc a few per cent, the whole road 4 to 12 %).
- **D4.** asset plan note 4 ('gum is densest at doors, the dark spots on the sheet's right pavement') against the sheet's right-pavement spots, which are reddish-brown stains 0.15 to 0.45 m (rust and mud), not gum: chose two kinds: gum (12 to 32 mm, grey-black) and pavement_stain (brown blots), so the sheet's spots are read as stains.
- **D5.** asset plan note 4 / make_wear_masks.py (streaks: three crops of one procedural map) against Photo M16/M17 (rivulets 10 to 20 mm, bracket streaks 0.1 m x 0.45 m, many of different length): chose a streak set per sill: two end streaks, 3 to 7 rivulets, a faint wash.

## 8. The automatic check, and how to run everything

`target.json` carries a flat `checks` list (93 entries, each with its kind, a name, the measure, its parameters, a min, a max and the source). Unit 4.5's check imports `measure(mask, px_per_m, measure_id, **params)` from `self_check.py` and runs each check of a kind on the generated mask (float 0..1, row 0 at the top of the decal frame, frame as the kind's `mask.frame_extent_m` says). Each check carries `applies_to`: `mask` (the 89 checks unit 4.5 runs on a generated mask), `envelope (drawing polygons)` (2 checks that only the drawing can run, because they need polygon roles) or `flag data` (2 checks on the flag tone classes). Measures:

- `coverage`: share of decal pixels with mask >= thr (default 0.5)
- `blob_eqd_mm`: equivalent diameter (mm) of 8-connected components of mask >= thr with area >= min_area_mm2; stat p50 or p90
- `count_per_m2`: components per m2 of decal (or of the named region) at thr, area >= min_area_mm2
- `edge_10_90_mm`: 10 to 90 % edge width of the mask relative to its own peak: 0.8 x peak / median |gradient| (per m; one axis if axis is x or y) on pixels with band_lo x peak < mask < band_hi x peak within reach_mm (default 60) of the half-peak contour
- `streak_aspect`: median over components (mask >= thr, length >= min_length_m) of PCA length / PCA width (4 sigma ellipse extents)
- `streak_width_mm`: median PCA width (mm) of those components
- `streak_length_m`: median PCA length (m) of those components
- `verticality_deg`: largest deviation of a component's major axis from vertical (degrees) over components of length >= 0.1 m
- `fade_ratio`: mean mask over the last third / first third of the streak length along the fall line, per component, median
- `foot_profile`: mean mask per row at heights above the foot: points are [height_m, min, max]; the mask's bottom row is the foot
- `tile_seam`: mean |mask(first col) - mask(last col)| (and rows for axis y) divided by the mean absolute difference of adjacent columns (rows) inside the tile: about 1.0 when the tile is seamless
- `mask_max`: maximum mask value
- `mask_std`: standard deviation of the mask
- `tone_ratio`: mean luminance of the dark-slab class over the pale-slab class in the generated flag colour map (check applies to the flag colour result, not the mask)
- `crack_flag_share`: share of flags carrying a crack in the generated flag attributes
- `crack_width_mm`: median of 2 x distance-transform - 1 along the Zhang-Suen skeleton of mask >= thr (mm)
- `crack_length_per_m2`: skeleton length (m) of mask >= thr per m2 of the decal frame
- `role_length_per_m2`: envelope polygons only (drawing check): path length of the polygons with the named role per m2 of the frame
- `role_blob_eqd_mm`: envelope polygons only (drawing check): equivalent diameter of the polygons with the named role

```
/home/user/.bpyenv/bin/python target_drawing.py OUT_DIR      # polygons (mm) in wear_envelopes.json, scene_*.png and kind_*.png sheets in OUT_DIR
/home/user/.bpyenv/bin/python self_check.py                  # prints the result line, writes it to target.json under self_check, writes the two overlays
```

**What the self-check does** (A to D): A structure (every part present, numbers in order, every cited measurement id exists, every surface has a tone); B tone (each mark colour is the surface times its multiplier, its dL* follows, and where a photograph or the sheet quoted a dL* the two agree within 14); C the photographs (the measurements are re-made from the reduced previews and must come back within their stated errors; the drip-band envelope is laid on the main photograph with the scale fitted on one dimension only, the 75 mm yellow line, and holds at least 90 % of the dots found; the splash profile is laid on the Hook sheet's gable foot with the scale fitted on the 75 mm brick course alone, mean error 0.17 or less in luminance ratio); D envelopes (each kind is drawn at its texel scale, three variants and two seeds, rasterised with its stated edge softness, and every check of the kind is run on it; the median of the six runs must be inside the range).

**Overlays on the main photograph:** `ph-urban_street_03-oil-drip-speckle-target-on-photo.jpg` (the target's drip band in cyan on the photograph, the dots found in red) and, for the sheet, `hook-sheet-gable-foot-target-on-sheet.jpg` (the splash profile's heights as lines on the gable foot).

**Honesty about the checks' ranges.** The ranges come from the stated target numbers, and where my first envelope did not meet its own range I did one of two things and wrote it down: corrected the envelope (wash level below the streak threshold, rust halo level, tyre-scuff profile, dot density counted inside the band instead of over the whole region, Voronoi cracks in place of a jittered grid, wrapped copies for tiles) or corrected a range I had set carelessly (the foot kinds' edge width is the whole fall-off 0.3 to 1.2 m, not the 75 mm step inside it). Nothing was passed by widening a range beyond what the photograph measurements allow.

## 9. What the target could not settle

- Gum density per m2: no photograph with gum was reached; the 2019 London panoramas show low-gum residential streets. Tiers are Judgement. Read Keep Britain Tidy / Defra litter surveys and Geograph shopping-street photographs when the network opens.
- 1990 soot level on Quay Street's brick: every reachable photograph is 2018 to 2026 and cleaner. The wall-foot and streak strengths are set from the Hook sheet (mood), between sheet and photograph by a stated factor.
- Streak width as a fraction of sill width: no photograph with a measured sill and streak pair was reached beyond M17; the fractions are bounded by M16/M17, not measured.
- Salt bloom height and share: only the Hook sheet shows it; the rule for a port is Judgement (BRE 245 search lead).
- Fly-poster, bird-dropping, paint fade: no measured photograph; shapes are Judgement.
- Camera height for the panorama measurements (1.6 m) is proved only by the 75 mm yellow line (+/-6 %).
- The brief said ambientCG's gum and leaking assets are photographs; the metadata says procedural: unit 4.5 may use them as CC0 shapes only.

## 10. Credits for the previews

All previews are reduced (JPEG, at most 1200 px on the long side, under 300 KB) from CC0 files read on 8 October 2026, for measurement only; named `<ref>-<place>-<what>.jpg` (ref `ph` = Poly Haven; `hook-sheet` = the project's own sheet). Scale is stated where it is fixed.

| file | scale | credit |
|---|---|---|
| `hook-sheet-gable-foot-and-patch.jpg` | 3.4 mm per pixel | the Hook sheet (the project own mood bar, repo file) left gable, cropped and doubled; brick course 22 px = 75 mm |
| `ph-aerial_asphalt_01-road-tyre-scuffs.jpg` | 7.32 mm per pixel | Poly Haven texture aerial_asphalt_01, Rob Tuytel, CC0; 30000 mm across the full map |
| `ph-asbestos_sheet_02-rust-bleed-fixings.jpg` | 0.879 mm per pixel | Poly Haven texture asbestos_sheet_02, Amal Kumar, CC0; 1800 mm across the full map |
| `ph-asphalt_02-road-sealed-crack.jpg` | 1.46 mm per pixel | Poly Haven texture asphalt_02, Rob Tuytel, CC0; 3000 mm across the full map |
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
| `ph-urban_street_03-flags-patched-ortho.jpg` | 4 mm per pixel | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-garden-wall-soot-streaks.jpg` | see note | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-kerb-flags-channel-view.jpg` | see note | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-oil-drip-speckle.jpg` | 3 mm per pixel | Andreas Mischok, Poly Haven urban_street_03 (CC0, taken 2019-09-07) |
| `ph-urban_street_03-oil-drip-speckle-target-on-photo.jpg` | 3.0 mm per pixel | overlay of the target's drip band on the main photograph; photograph credit as above |
| `hook-sheet-gable-foot-target-on-sheet.jpg` | 6.8 mm per pixel on the sheet | overlay of the splash profile on the Hook sheet (the project's own file) |

