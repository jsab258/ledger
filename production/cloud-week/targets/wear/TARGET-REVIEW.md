FAIL

# Review of the wear target (cloud week 42, unit 4.5)

Fresh target reviewer, 8 October 2026. I did not write this target and will not build it. I read REVIEW-BRIEF.md, BRIEF.md, canon.md, RULINGS.md, TARGET.md (all 1,174 lines), target.json, both scripts, SUMMARY.md section 8, 4-SIGNAGE-AND-WEAR.md family B, BRICK-COLOUR-2026-10-08.md, tools/make_wear_masks.py, production/specs/street-wear.json and vignette-scene.json, and the wear layer in tools/art-recipes/terrace-front.py. I looked at every preview, the Hook sheet (enlarged two to four times, gable, parade, sills, downpipes, channel) and the three street frames of 7 and 8 October.

What I ran (outputs only in the scratchpad):

- `self_check.py` on a scratch copy (REPO pointed at the repository, `--no-overlays`): `self_check: passed=700/700 failed=0`, the same as the target states.
- `target_drawing.py`: 7 scenes, 23 kinds, 3,609 polygons. I looked at the kind sheets and the 2 m wall bay.
- The target's own `measure()` on nine masks I made deliberately wrong (fault 4).
- Sources reached: Poly Haven `api/info` for urban_street_02 and 03, peeling_painted_wall, aerial_asphalt_01, plaster_brick_01 and concrete_wall_003. Authors, dates, sizes and CC0 all match. I downloaded the asphalt_02 2k diffuse map to check M03. ambientCG's metadata API confirms that ChewingGum001, Leaking005, RoadLines006 and SurfaceImperfections003 are PBRProcedural and AsphaltDamageSet001 is photogrammetry. Commons, Geograph, archive.org and the ambientCG image host refuse (HTTP 000), as the target says.

Re-measured on the previews:

| What | Target | Re-measured | Verdict |
|---|---|---|---|
| M18, Hook sheet gable foot | course 11 px = 75 mm; black band 0.33 m; salt band 0.26 to 0.46 m | course 10.5 to 11 px; band rows 668 to 712 (0.30 to 0.33 m); grey-white bricks 0.32 to 0.49 m | Agrees |
| M17, sill-bracket streak | 0.45 m long, 0.10 m wide; column 0.97, darkest bricks 0.8 to 0.9 | course 24 px = 3.1 mm/px; core 60 to 90 mm wide at 0.66 to 0.91 of the flanks (median about 0.8), visible for about 0.30 m | Agrees as a measurement; the target's streaks are far heavier (fault 2) |
| M04, oil drip dots | 13.7 / 16.9 mm at rel 0.75 / 0.85 | 11.2 / 15.1 mm. In-band density depends on the minimum dot area (mine: 338 per m² at 36 mm² and up; the target: 154 per m² at 70 mm² and up) | Agrees within method |
| M07, dark/pale flag ratio | 0.58 | 0.54 | Agrees |
| M05, reinstatement seam tone | "about 0.5" | 0.63 to 0.77 | Disagrees (fault 11) |
| M03, sealed crack width | 40 to 90 mm | 15 / 37 / 62 mm (p10 / p50 / p90) | Disagrees (fault 11) |
| Kerb and channel, urban_street_03 | (no measurement) | channel setts 1.4 × the road's luminance; kerbside asphalt 0.95 × the open road | Contradicts gutter_grime (fault 5) |
| Soot-blackened garden wall, urban_street_03 | (no measurement) | sooted panel 0.37 to 0.48 × the cleaner panel | Missing (fault 1) |

## Faults, worst first

### 1. The wear that reads "across every facade" has no kind and no owner, and the target's own soot photograph is never measured

**Where.** The Hook sheet (gable, parade, right-hand building) and `ph-urban_street_03-garden-wall-soot-streaks.jpg`.

**What the sources show.**
- On the sheet, the facades read grimy mainly through the brick body:
  - Sooted, darker lower walls.
  - A dark, desaturated head under the gable verge. I measured column medians in columns 15 to 170, rows 40 to 170 against rows 250 to 600. Over the top 0.6 to 0.9 m the luminance is 0.55 to 0.70 of the body, and the saturation is 0.26 to 0.45 against 0.60 to 0.70.
  - The feet.
- The target's own preview of urban_street_03 shows a soot-blackened stock-brick panel beside a cleaner one, measured in 500 × 130 px boxes:
  - Sooted panel: median sRGB 90/81/74, L* 35.1. Cleaner panel: 146/128/108, L* 54.8. The luminance ratio is 0.37 to 0.48.
  - Under the coping, a band about 0.4 m deep is a further ×0.80.
- The preview is credited in section 10 but has no M number. Yet section 9 says the "1990 soot level ... every reachable photograph is 2018 to 2026 and cleaner", and S2 says the 2019 streets have "no soot on the brick".
- None of the 23 kinds carries:
  - whole-wall soot;
  - the head band under eaves, verges and copings;
  - the darker lower wall.

  Section 4 names no other family that owns them.
- Section 1 also misses the wear layer that already exists in `tools/art-recipes/terrace-front.py` (the `WEARS` block):
  - a noise patch multiply (`WEAR_PATCH_DEPTH`);
  - a foot rise (`WEAR_SPLASH_M`, `WEAR_SPLASH_DEPTH`);
  - tall-noise "water paths down from the top";
  - per-house looks (`HOUSE_LOOKS`: sooted 0.60/0.56/0.56).

  Nothing says whether the new L0 foot bands replace that foot rise or multiply on top of it.

**Amendment.**
- (a) Add M21 (garden wall, the numbers above; method: median luminance of the two panels and a row profile in 20 px bands) and M22 (the sheet's gable head, the numbers above).
- (b) Add kind 24, `wall_soot`, at L0 in the brick and render materials, per house:
  - **States:** as built, sooted, or cleaned in the 1980s (the existing house set). The sooted state is an albedo multiplier of 0.45 with saturation × 0.6 (Photo M21: 0.37 to 0.48).
  - **Head band:** under every eaves gutter, verge, coping and string course, × 0.60 at the head (Sheet M22 0.55 to 0.70; Photo M21 0.80), back to 1.0 over 0.6 to 0.9 m. The lower edge is ragged by courses (75 mm steps, amplitude 0.05 to 0.15 m).
  - **Lower wall:** × 0.85 from 0 to 1.2 m on sooted houses (Sheet, right-hand building; Judgement).
  - **Checks:**
    - a head-band profile at heights below the head (0.1, 0.5, 0.9 m) with ranges;
    - `mask_std` of the house mottle;
    - the sooted/clean luminance ratio 0.35 to 0.55 on the composed brick.
- If the brick family is to own this instead, write that hand-over in section 1 with these numbers. Note that HOUSE_LOOKS' sooted look (about 0.57) is lighter than M21's 0.37 to 0.48.
- (c) In section 1, record the terrace-front wear layer. State that `wall_foot_splash` replaces its foot rise (set to 1.0 where this target's foot band is applied) and that its head water paths give way to `wall_soot`'s head band, so no foot or head is darkened twice.

### 2. The streaks are darker, longer and denser than any source, and they cite the Hook sheet for streaks it does not show

**Where.** The Hook sheet's gable, parade and right-hand building, enlarged; M16; M17.

**What the sources show.**
- Enlarged two to four times, the sheet shows no rain streaks under any sill, coping, verge or gutter.
- The target's own D2 admits "no streak was measured on the sheet". Yet the kinds cite it:
  - streak_sill length: "Sheet shows streaks reaching the next opening";
  - streak_coping length: "Sheet: gable streaks run 1 to 3 m";
  - M17's reading: "The Hook sheet bar is heavier";
  - S4: "wall feet, streaks, wet flags".
- The only streak photographs give these numbers:
  - M16: rivulets 0.09 to 0.45 m.
  - M17: 0.45 m; my re-measure about 0.30 m at a core of 0.66 to 0.91.
  - The new M21: the coping band about 0.4 m.
- The target sets the following, with no source:
  - **streak_sill:** length p50 0.8 m and p90 1.4 m, multiplier 0.55, under every sill.
  - **streak_coping:** 1.4 to 4.0 fingers per metre, each 0.6 to 2.5 m long at 0.55, under every eaves gutter, coping and string course.
- Repeated on every opening and every eaves line, that is the medieval look of "streaks under every ledge", not the sheet's 1990 street. It is the most likely way for this family to turn cartoonish.

**Amendment.**
- (a) Delete the three sheet citations and the word "streaks" from S4. Label the darkness Judgement from Jafar's words of 2 October. Add a section 7 entry: "M17 (0.8 core, 0.3 to 0.45 m) against his 'not faint marks': length follows the photographs, darkness nudged darker."
- (b) **streak_sill:**
  - streak_length_m p10 / p50 / p90 = 0.15 / 0.35 / 0.60 m (M16, M17);
  - a 0.8 to 1.4 m end streak under 1 sill in 8 only (a sill with a broken drip; Judgement);
  - brick multiplier 0.70, painted brick 0.75, render 0.72;
  - present under 50 to 70 % of sills, not every sill;
  - checks: streak_length_m_p90 0.3 to 0.9, streak_length_m_p50 0.12 to 0.45.
- (c) **streak_coping:**
  - one finger per leaking joint, with 1 joint in 3 or 4 leaking (0.3 to 1.0 fingers per metre);
  - full-height runs of 1.5 to 3.0 m only under leaking gutter joints and hopper heads, 0 to 2 per house;
  - the continuous darkening under eaves and verges is `wall_soot`'s head band (fault 1), not fingers.

### 3. No order in which the kinds are put together, and no floor: wall feet go black and the sheet's salt band comes out dark

**Where.** `hook-sheet-gable-foot-target-on-sheet.jpg`: the grey-white bricks at 0.33 to 0.49 m lie inside the splash band's 0.85 to 0.45 levels.

**What happens.**
- The target gives one ordering sentence only ("damp sits on top of the splash band").
- Applied as written, at a brick foot beside a downpipe, splash (0.20) × damp (0.50) × algae (0.40) gives 0.04 of the clean albedo. The sheet's darkest foot is 0.12 to 0.30.
- If the salt mark (replacing, at 0.6) goes down before the splash darkening, the sheet's grey-white band comes out dark brown. If it goes after, it stays pale. Nothing says which.
- The same applies on the ground: stains, gutter grime, oil, gum, puddles.

**Amendment.** Add a section 4 rule and a `compose` block to target.json.
- **Walls:**
  1. L0 in the material, multiplicative, in this order: `wall_soot`, `wall_foot_damp`, `wall_foot_splash`, `paint_fade`.
  2. L1 darkening decals, multiplicative: streaks, algae, rust.
  3. Replacing marks last, each over the colour already darkened: salt_bloom, render_patch, paint_flake, poster_remnant, bird_dropping.
- **Ground:**
  1. Flag tone class.
  2. pavement_stain and halos.
  3. gutter_grime.
  4. road_patch, road_crack, tyre_scuff, road_blot, road_oil.
  5. gum and cig_end.
  6. Puddles (WET-ROAD) on top.
- **Floor:** the product of darkening multipliers on any texel is clamped at 0.15 of the clean albedo on walls (Sheet M18's darkest is 0.12 to 0.30) and 0.35 on the ground. Only crack cores, gum and oil-dot cores may go below it.
- **New check:** a composed 2 m brick foot beside a downpipe (splash, damp, algae and salt at house wear 1.0):
  - luminance ratio to the clean wall at 0.1 m between 0.12 and 0.30;
  - the salt bricks at 0.35 m at 0.57 to 0.75 or above (M18's salt band).

### 4. The checks in target.json cannot catch a wrong mask: too uniform, regular, a plain stripe, or placed wrongly

**What I tested.** I ran every mask check of a kind, with the target's own `measure()`, on masks made deliberately wrong. Results:

| Kind | Wrong mask | Result |
|---|---|---|
| wall_foot_splash | perfectly straight, uniform gradient with no ragged top (the target's own "Not modern": "no uniform gradient ending in a straight line") | **passes all 4** (tile_seam is 0 because a uniform tile has no column difference) |
| wall_foot_damp | uniform gradient | **passes all 3** |
| gutter_grime | uniform band | **passes all 3** |
| streak_sill | two identical, symmetric bars and nothing else ("no neat symmetrical streak pairs") | **passes all 9** |
| streak_coping | identical fingers at an identical 0.4 m spacing ("no identical fingers at identical spacing") | **passes all 6** |
| gum | a 2 × 2 grid of identical discs | **passes all 4** |
| road_oil | a lattice of identical dots | **passes all 5** |
| salt_bloom | one uniform 0.09 m stripe ("salt follows bricks, not rectangles") | **passes all 4** |
| paint_fade | white noise at texel scale | fails only on edge width, by chance |

Further:
- No check looks at placement: where a decal sits, its rotation, its distance from the kerb, how often one variant repeats in the frame. All 89 mask checks run on a single mask.
- The `check_measures` text in target.json disagrees with the code. The text gives edge_10_90 as "0.8 × peak / median |gradient|" and streak extents as "4 sigma"; the code uses 0.95 × peak / the 90th-percentile gradient, and sqrt(12 × variance). A builder who implements from target.json alone gets different numbers.

**Amendment.** Add to target.json:
- (a) **Ragged top**, `top_edge_std_mm`: the standard deviation along x of the height where the mask crosses 0.5 (0.3 for damp and gutter). Ranges: splash 15 to 60, damp 40 to 150, gutter 20 to 70, salt 20 to 70. Plus `column_mean_cv` of at least 0.08 for all four foot kinds.
- (b) **salt_bloom**, `brick_patch_share`: brick cells 0.215 × 0.075 m on the stated 0.0375 m bond, mean mask above 0.4 in 35 to 75 % of the band's cells, internal standard deviation under 0.15.
- (c) **streak_sill:** `end_streak_length_ratio` (longer over shorter) 1.15 to 2.5; `end_streak_width_ratio` of at least 1.1; 3 to 7 rivulets (components at threshold 0.25, at least 0.1 m long).
- (d) **streak_coping:** `finger_spacing_cv` 0.25 to 0.8 at the head row; finger length CV of at least 0.25.
- (e) **Scattered kinds:** Clark-Evans nearest-neighbour ratio R 0.7 to 1.3 for road_oil and cig_end, 0.5 to 1.1 for gum (clustered); `size_cv` of at least 0.25.
- (f) **paint_fade:** `dominant_wavelength_m` from the radially averaged power spectrum, 0.5 to 2.0.
- (g) **Placement checks on the placed street** (street-wear.json):
  - streak decals' origin within 0.03 m of a sill or feature's lower edge, roll 0 ± 3°;
  - L0 band origin at the pavement line ± 0.02 m;
  - road_oil band centre 0.9 to 1.6 m from the kerb, axis within ±10° of it;
  - no gum on the carriageway and none within 0.4 m of a wall;
  - in the hook camera's frame, no variant over 40 % of a kind's visible decals, and no two placements with the same variant and seed within 6 m along one wall;
  - tiled L0 kinds' x phase different on neighbouring houses.
- (h) Rewrite the `check_measures` text to match the code exactly.

### 5. gutter_grime contradicts its own photograph and the scene's own note on the channel

**Where.** `ph-urban_street_03-kerb-flags-channel-view.jpg`; vignette-scene.json `street.channel`; the Hook sheet's right channel.

**What the sources show.**
- In the photograph (dry):
  - The channel setts read 138/132/132, luminance 0.236. The asphalt reads 0.161 to 0.170, so the channel is 1.4 × the road.
  - The asphalt from 0 to 0.6 m off the kerb is 0.95 × the open road.
- The scene says the channel course is "in the kerb's own concrete rather than asphalt ... reads as a different material in every British street photograph".
- On the sheet (wet): the strip between the inner yellow line and the kerb is about 0.7 × the road, and the kerb face is a dark line.
- The target's rule is "a continuous dark band the width of the channel" at mask 0.9 × multiplier 0.5 to 0.55, on the asphalt and kerb_granite surfaces only. That makes the channel darker than the road, the opposite of both. It is also against the target's own era rule ("nearer the photograph for ground marks"). Section 7 records no disagreement.

**Amendment.**
- Add a surface row `channel_concrete`: sRGB 150/146/140, Judgement within Photo 138/132/132.
- gutter_grime tone on it: multiplier 0.85 at mask 1, so the channel stays 1.2 to 1.5 × the open road when dry.
- The asphalt fringe: 0.85 (Photo 0.95 dry; with the wet factor about 0.7, the sheet).
- The darkest grime goes in a 20 to 40 mm line in the kerb–channel and channel–asphalt joints (multiplier 0.35) and in the gully piles: 0.4 m radius, mask 0.8, colour 70/62/52, Judgement.
- Put the kerb-face tyre scuff in numbers: +8 L*, 0.05 to 0.12 m up, 0.3 to 1.5 m long, 1 per 10 m.
- Add a tone check: `channel_over_road` of at least 1.15 dry.
- Record photograph against sheet in section 7.

### 6. Wet and dry: tones measured on the wet sheet are used as dry, then darkened again; salt that "vanishes when wet" contradicts the wet sheet it was measured on

**What the sources show.**
- The Hook sheet is wet (RULINGS 3 October: "the wet street dark, glistening").
- M18 (foot 0.12 to 0.30), M19 (patch) and M20 (stains) are therefore wet-state ratios. The target uses them as the dry tone and then applies its wet multipliers on top: splash 0.20 × 0.75 = 0.15 wet, below the sheet's midpoint.
- salt_bloom's wet setting (× 0.45, "mostly vanishes ... leaves a dull darker patch") turns the sheet's grey-white band dark in the game's usual weather (drizzle and rain, never sun: RULINGS 5 October). Yet the band was measured on that same wet sheet.
- pavement_stain's dry note, "dry: lighter by a third", contradicts its dry multiplier of 1.0.

**Amendment.**
- State in section 4 that Sheet ratios are the wet target, with dry = sheet ratio / wet factor:
  - wall_foot_splash brick_red dry 0.27 (wet 0.75 gives 0.20);
  - pavement_stain flag_concrete dry 0.48 (wet 0.8 gives 0.38);
  - road_blot dry 0.56 (wet 0.9 gives 0.5).
- salt_bloom: wet albedo_mult_on_tone 0.9, roughness_delta −0.1 in drizzle and damp; 0.6 only in heavy rain with water running down the wall.
- pavement_stain: delete "lighter by a third", or make the dry multiplier match it.

### 7. Iron has no wear, though section 1 lists it as missing and the sheet shows it

**What the sources show.**
- Section 1 says "downpipes have no rust or green".
- No kind carries `iron_black` except bird droppings. rust_bleed and paint_flake list only masonry, timber and render.
- The sheet's gable downpipe shows paint loss and rust over 7 % of its length:
  - pale ochre 141/102/72 on paint 50/40/37;
  - patches 20 to 110 mm (columns 199 to 203, rows 100 to 700, 6.8 mm/px).
- Its cellar grate on the left pavement is rust red-brown.
- M13 (rusty_painted_metal) is metal, but it is used only to scale masonry streaks.

**Amendment.** Add kind `iron_wear` (L0 in the iron material, plus L1 at collars), or name the furniture and terrace-kit families as owners with these numbers.
- **Surfaces:** iron_black on downpipes, hopper heads, railings, gully and cellar grates, bollards.
- **Paint loss and rust:** 5 to 10 % of length or area (Sheet 7 %), colour 141/102/72 (Sheet), patches 20 to 110 mm (Sheet), concentrated at collars, brackets, the shoe and the lowest 0.3 m.
- **Rust streaks below collars:** 24 mm wide (p50), aspect 4 to 12, 16 mm edges (Photo M13).
- **Grates:** rust-brown 110/60/35 in the recesses, the bar tops polished darker grey (Judgement).
- **Checks:** coverage 0.05 to 0.10; blob_eqd p50 20 to 60 mm.

### 8. Kinds the earlier research and the target's own photographs list are dropped without a word

**What is missing.**
- 4-SIGNAGE-AND-WEAR.md (B2, B4 L2, B5) lists four kinds the target neither includes nor rejects:
  - broken and worn double yellow lines (also the target's own preview note: "worn yellow line");
  - ghost marks of removed signs and brackets;
  - buffed graffiti;
  - worn paint on door kick plates and handles (handles appear only as words in paint_fade).
- The sheet's sills are olive, lichened stone: 95 to 112 / 82 to 89 / 62 to 70, L* about 36. The target's stone_sill is 170/166/158, L* 68, and no kind puts lichen or algae on horizontal stone.
- The target's own urban_street_03 previews show in-situ concrete and bitmac infill in the flagged footway: the kerbside strip, and the patch at the bottom of the ortho. flag_patch_crack handles flags only.

**Amendment.** Add each as a kind with numbers, or name its owner in section 4 with a reason. Suggested numbers (Judgement unless stated):
- **`line_wear`:** 10 to 30 % of the line lost in cracks and gaps 20 to 300 mm; ragged edges 5 to 15 mm; faded toward 200/170/90; dirt film; mask checks on loss share and gap size.
- **`sign_ghost`:** 0 to 1 per facade, 0.3 to 2.0 m. A rectangle 5 to 10 L* paler or cleaner than the wall, with 2 to 4 filled holes 10 to 20 mm across and rust_bleed tails.
- **`graffiti_buff`:** 0 to 1 per 20 m. Flat rectangles 0.3 to 1.5 m in a mismatched paint, ± 10 L* from the wall. Or reject it in section 7 with a reason.
- **Handle and push wear:** a dark, greasy halo 0.1 to 0.25 m around handles, letter plates and push zones at 0.9 to 1.2 m, multiplier 0.75; door edges worn to undercoat.
- **`stone_top_lichen`:** 40 to 80 % of sill and coping tops, olive 103/88/65 (Sheet), patches 10 to 60 mm.
- **`footway_infill`:** 1 to 3 per 48 m footway, 0.6 to 3 m long, one flag row wide; bitmac 70/68/66 or in-situ concrete 150/145/140; its own texture.

### 9. Honesty about sources: several statements are wrong or unrecorded

**The problems.**
- **S1's "same in 1990"** says "only shape and share are taken from them, never their colour". But the following colours come from S1 scans:
  - brick_painted 152/108/93 (M08);
  - render_cream (M12);
  - paint_flake on render (M10);
  - rust_bleed (M14);
  - algae_downpipe and wall_foot_damp on render (M15).
- **S2** says 2019 London has "no soot on the brick". The target's own preview shows soot-blackened stock brick (fault 1).
- **plaster_brick_01 (M15):** Poly Haven's record, read today, tags it 'sewer', 'tunnel' and 'trimsheet'. Its green band is a waterline in a trim sheet, not a pavement wall foot. The target still says "photographed in unknown places", and cites it as agreeing with the splash profile ("Photo M15 ... agrees").
- **M03 and M05** record no tone, yet tones are cited to them: sealed crack "L* about 10", seam "about 0.5".
- **Section 6** cites flag_concrete as "Photo M07 (concrete_pavement_02 median 134/123/110)". M07 is urban_street_03, and no measurement of concrete_pavement_02 is recorded.
- **`ph-asphalt_02-road-sealed-crack.jpg`** shows the right half of the map, with an open hairline only. The sealed crack (x 100 to 350 of the 2k map) is not in the preview, so a reviewer cannot check M03 from it.
- **Seven S1 files are never measured:** concrete_pavement, pavement_01, pavement_02, painted_worn_brick, concrete_moss, dirty_concrete and brick_wall_006.

**Amendment.**
- Rewrite S1's line to list the colours taken from scans, each with why it holds for 1990 paint and render (or mark it Judgement).
- Delete "no soot on the brick" from S2.
- State plaster_brick_01's tags. Remove "Photo M15 agrees" from the splash profile. Relabel the render tones of wall_foot_damp and algae_downpipe as Judgement, coloured from a waterline.
- Record the tone values in M03 and M05 (fault 11 has mine).
- Cite M07's dark class 133/130/130 for flag_concrete, or record the concrete_pavement_02 measurement.
- Re-crop the crack preview to the left half of the map.
- List the seven unmeasured files as "looked at, not used".

### 10. Placement anchors not located, and rules in words only

**What a placer cannot find.** Several rules depend on places the target never gives in numbers:
- "the quay end";
- "kerbside standing places";
- "the rank";
- "the loading apron of the fishmonger and ship's chandler";
- "junction mouth";
- "the bus stop".

Kerbside standing places matter most: the street has double yellow lines along both kerbs (sheet and frames). road_oil and road_blot hang on standing places that are not defined anywhere.

**Rules in words only.**
- "heavier at door steps, downpipe feet" (splash);
- the kerb-face scuff, the channel weeds and the gully piles (gutter_grime);
- "near the quay" (salt_bloom, bird_dropping).

**Amendment.**
- Give x ranges from vignette-scene.json:
  - the quay end (Mickey's bay and the west terraces' quay gable);
  - the rank (its length and x);
  - bay 1's loading apron and the chandler's (x 40 to 46);
  - standing places: say where vehicles stand on a double-yellow street (the rank, loading, and a stated count of illegally parked places, for example 3 to 5 east and 2 to 3 west, 5.5 to 6 m each; 2-VEHICLES.md);
  - the yard entrance (x 21 to 24) as the only junction mouth;
  - the bus stop: zero until it is placed.
- Put the words into numbers:
  - splash: height × 1.2 and strength × 1.15 within 0.6 m of a door or downpipe;
  - weeds 0.05 to 0.15 m across, 1 per 6 to 10 m;
  - salt at weight 1.0 within 12 m of the quay end;
  - the kerb scuff and gully piles as in fault 5.

### 11. Re-measured numbers that disagree with the target

**What I measured.**
- **road_patch seam:** the target uses a multiplier of 0.55 and cites "M05, about 0.5". Profiles across the seam on `ph-urban_street_02-road-reinstatement-ortho.jpg` give 0.63 to 0.77 of the road, brown-shifted: 125/110/103 on 138/126/123. The infill is 0.93.
- **road_crack main width:** the target says 40 to 90 mm. On the full asphalt_02 2k scan (Poly Haven, CC0), per-row widths below 0.7 of the surface are p10 / p50 / p90 = 15 / 37 / 62 mm. The core L* is 13 on 36.8, which agrees with the target's darkness.
- **cig_end:** the tone table is white only. M06's own kerb strip shows about 4 tan cork tips in 10 (9 tan and 15 white bits), tan median 177/140/110.

**Amendment.**
- road_patch: seam multiplier 0.70 with tint 125/110/103; infill multiplier 0.93.
- road_crack: main_crack_width_mm 15 to 60 (p50 35).
- cig_end: add a tan-filter row 177/140/110 for 40 % of ends.

### 12. Era and content wording

**The slips.**
- tyre_scuff bans "skid marks from ABS-era stops (long straight stripes)". This is backwards: straight locked-wheel skid stripes are the pre-ABS mark, and most cars in 1990 had no ABS.
- paint_flake: "stallrisers where bags and pushchairs knock". A pushchair implies a child; canon's content rule is "no children anywhere".
- gum: "Chewing gum was as common in 1990 as now" has no source.
- poster_remnant: "1.0 x 0.75 m ... A1". A1 is 0.594 × 0.841 m; 1.0 × 0.75 m is about quad crown.

**Amendment.**
- tyre_scuff: say that straight skid pairs are period-correct, then exclude them by scope (or allow 0 to 1 faint pair). Do not call them modern.
- paint_flake: replace "pushchairs" with "shopping trolleys and sack barrows".
- gum: replace the claim with "gum staining existed in 1990 but grew later; tiers kept low (Judgement)".
- poster_remnant: write "double crown 0.76 × 0.51 m or quad crown 1.02 × 0.76 m".

## Narrow notes (not counted)

- **Colour per channel.** Section "How to read this" gives a scalar lerp "with the mark's dirt tint", but no tint is stored. Say that the builder applies the per-channel ratio mark_lin / surface_lin. It carries over to the street's real brick and paint, as the B1 check implies.
- **One surface per decal.** Say how a decal knows its surface: the placer picks the tone row from the wall's material, and decals that cross two surfaces are split at the joint.
- **Glazed tiles.** Mickey's stallriser is glazed tile in the sheet and the street. Add a `tile_glazed` tone row: splash multiplier 0.6 with grime in the joints, Judgement.
- **Self-check tolerances.** B1 accepts an implied multiplier anywhere within a factor of 1.6 either way, and C's splash fit allows a mean error of 0.17. Both are loose, though every row actually matches within 2 %.
- **asphalt_dry 91/86/82** is the mean of the three mid scans, not their median (89/86/80).

## What is right

- **Each kind is complete in form.** All 23 have:
  - a rule of place, with feature, surfaces, heights and side weights;
  - a decal frame;
  - an envelope in metres;
  - density with units;
  - a tone table per surface (sRGB, linear multiplier, ΔL*);
  - wet and dry in numbers;
  - a texel scale with the screen's px/m;
  - seeded variants;
  - checks.

  The kinds are drawn and checked by scripts that run. Both scripts reproduce the stated result (700/700), and the drawing reads target.json alone.
- **The measurements I re-made agree:**
  - M18, the sheet's gable foot: course, black band, salt band;
  - M07, the flag tone ratio;
  - M04, oil dot sizes;
  - M17 as a measurement.
- **Ground wear is low in contrast and broad, as M02 measures,** with no faint-everywhere strength. The gum and stain split (D4) reads the sheet's brown blots correctly as stains.
- **The sources are honest about reach and licence:**
  - ambientCG's procedural creation is verified, and the brief's claim is corrected;
  - the unreached hosts are confirmed;
  - Poly Haven authors, dates and CC0 are verified on six records;
  - nothing is NoAI;
  - no brand, cypher or council name appears;
  - previews are under 300 KB and 1200 px;
  - no alcohol, gambling or children in any preview I opened (the kerb litter is cigarette ends and paper).
- **The era rules are mostly right:** no tactile or block paving, no anti-skid colour, no spray utility marks, no 2000s litter, no American markings, invented poll-tax posters only. Tobacco ends are kept and drink litter is excluded.
- **The texel rule is right:** at least 6 texels across the smallest feature, never above 1,122 px/m, and LOD fades for sub-2-pixel features beyond 6 to 8 m. These are the right engineering limits.
- **The disagreements D1 to D5 are recorded.** "Could not settle" names the right gaps: gum density, 1990 soot level, streak-to-sill ratio, salt.
