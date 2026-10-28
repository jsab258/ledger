# How Mafia layers wear, grades and fogs its town, and the method for LEDGER (28 October 2026)

His order of 28 October (D11), for Mickey's office and one shop front first. The method is copied, never the assets.

Tags: **M** measured (counted by a script), **R** read (a value in a file), **I** inferred; all read 28 October 2026. WEAR/ is F:/LedgerTools/aaa-study/mafia/wear-2026-10-28/; EXP/ is the 25 October exports, F:/LedgerTools/aaa-study/mafia/exports/. Revised the same evening after a fresh review (section "Review applied").

## Questions

1. Wear layers in order, with counts, values, decals per facade, where they sit. 2. Trim sheets. 3. Grade and fog by time of day. 4. A small office-like interior. 5. The method: recipes, calibration, numeric checks, hours.

## What was read, and how

- **Reused:** the 25 October exports (material library 3,828 files, lighting 392, Palermo's cells and packed sublevels, config). Cooked masters keep parameter names, defaults, functions and textures, not their wiring.
- **New export** (JSON only): Palermo's main facade family, windows, modular plaster, the Opera: 1,003 files, 17 MB, including 89 texture property files, no images (M). 28 MB written in all (cap 500 MB; F: GO).
- **The key:** read from F: for the run only, never shown or written; aesKeys.mainKey blanked and checked BLANK; WEAR/ holds no key-shaped string.
- **Rule learned:** a post-process value counts only where its override flag is on or inherited; every value below was checked.

## 1. How a Mafia town surface gets its wear

Four layers, in order. Most wear lives in the materials, not in decals.

**Layer 1: one tiling base material.** M_SMOpaque, 318 instances (M; WEAR/summary/instances.json): colour, one packed map (height, roughness, occlusion), normal, two tints placed by a mask channel ("Tint Mask Adjustments", most often (0, 2, 5, 1), 7 of 57), a roughness offset (median +0.19, set in 8) and tiling (median 1.5, set in 10) (R, M). Wall textures authored at 4,096 px (106 of 186) or 2,048 (73) (M).

**Layer 2: wear built into the building kit's masters**, the main wear layer (M; WEAR/summary-new/):
- **Facade plaster, two layers by vertex paint:** M_GeneralVertexColor_2_Layer_Tint (35 instances). Palermo's main street paints its facades with two instances (35 and 39 overrides in the main-street pack; R). _a: fine plaster tiled 2 (normal 0.3) over fine plaster with the mortar's normal and packed map, tiled 1.5 (normal 1.2); _b: coarse plaster tiled 1 over rough mortar tiled 5 (normal 2.0) (R). Both keep the height-blend defaults (0, 1, 1); the medians 0.20/0.70/0.77 come from only 7, 13 and 10 of 35 instances (M). Roughness offsets: base −0.30 to +0.26 (8 of 35), second layer 0 to 1 (9 of 35) (M). World-position noise tints streaks in all 35; the main street's two use streak tiling 10.7 by 11.1, power 0.56 (R; reading as streaks is I).
- **Plaster over plaster:** M_GeneralVertexColor_2_Layer (67): clean or coarse plaster over rugged plaster (second layer rugged in 33 of 65) (M).
- **Plaster over mortar, masked:** M_General_2_Layer_MaskBlend_VC (40 in the library, 7 more here): a blend from one texture channel (blue in 22 of 40) times vertex colour ((3.0, 2.6, 0.2, 2.1) in 9 of 40), broken by world noise; an optional flood line (on in 1 of 40) (R, M).
- **Painted joinery:** M_General_1_Layer_Paint_Chipped (48: shutters, frames, doors): paint over wood from a trim sheet. Medians (M): "Paint Fade Intensity" 0.89, "Weathering Opacity" 0.66, "Weathering Roughness Add" 0.98, "Dirt Mask Intensity" 1.25, "Dirt Roughness" 0.80, "Wood Mask Edge" 2.3, "Paint Cracks Tiling" 3, "Paint Roughness" 0.32.
- **Vertex colour:** 366 of 611 exported building meshes carry it; 88 of 96 facade-blend slots sit on them (M).

**Layer 3: decals.** Five decal masters, all deferred and translucent, writing colour and roughness, four of them a normal; four have an atlas tile; all have an angle limit and the global wetness and snow hooks (R). **Two methods** (M; WEAR/scripts/street_groups.py):
- **(a) A drawn stain picture**, for leaks and rust: 266 of the 285 leak stains on street walls use their own picture, 168 of them one instance (M_Decal_NoNormal, height-to-opacity on), 71 three plain ones (M_Decal_Simple); only 19 use a mask. Rust leaks: height-to-opacity on, tint (0.78, 0.69, 0.64, 0.8) (R).
- **(b) A mask over a tiling material or a roughness map**, for plaster grunge (175 placements), puddles (159), ground leaks, stained plaster and water lines. Inside the mask the material repeats once in 417 placements, twice in 69, three times in 8 (M). Plaster grunge uses the wall's own lime-plaster textures, alpha 1 to 2, normal mostly 1.5 (range −2 to 5); puddles carry no colour map, only roughness, tint (0.78, 0.65, 0.46), alpha 0.94, a 2×2 atlas (R).

**Counts** (M; WEAR/summary/palermo_decals.csv): 2,461 decals in 41 cells. The densest cell (878) is underground (catacombs, cistern, crypt, sewers); 252 more tunnel decals lie outside it. Street kinds outside it: 1,147, 754 on walls, 335 on the ground. On walls: leak stains 285 (38%), plaster grunge 164 (22%), rust leaks 47, stained plaster 33, ground leaks 27, water lines 23, plaster patches 20, small signs 49. On the ground: puddles 145, leak stains 78, edge wetness 13.

**Sizes** (M; full size = twice the default half-size of 128 × 256 × 256 cm, times scale; R, engine source DecalComponent.cpp, confirmed by the review), tall by wide: leak stain 5.4 by 5.1 m, plaster grunge 4.2 m square, rust leak 2.1 by 0.55 m, ground leak 2.5 by 6.6 m, puddle box 5.1 m (the shape a quarter-atlas tile); projection depth median 15 cm.

**Per wall** (M; street kinds only; grouping I: same facing within 10°, plane within 40 cm, within 15 m): 274 wall groups, **median 1 decal a wall, p90 6**, max 46; 54% of walls carry one. Study 4's street: 8 decals in 73 m (R).

**Where they sit** (M; street kinds, 595 wall decals with a street level, taken as the lowest ground-standing prop within 6 m): the decal box's bottom edge at or below 30 cm 30%; 30 cm to 1.5 m 18%; 1.5 to 4 m 21%; above 4 m 32%. These are box edges, not mark edges: 122 boxes reach over 30 cm below the street (leak boxes' p10 −1.8 m), so boxes at the base are mostly full-height leak stains. Bottom-edge medians: leaks 0.9 m, stained plaster 2.7 m, rust 2.6 m, plaster grunge 3.6 m, ground leaks 3.9 m, water lines 7.0 m. Sort order 0 on 2,228; fade-out screen size median 0.044.

**Layer 4: detail normals are rare.** At most 6 of 318 main-master instances (switch on in 3) and 3 of 40 masked two-layer ones; off by default in the facade blend master (M, R).

**Texture cost.** Mafia's device profile ships base colour and normal one mip down and masks two ("Base Albedo", "Base NormalMap" LODBias 1, "Base Masks" 2, decals 1; R; EXP/../config/DefaultDeviceProfiles.ini, [GlobalDefaults]); shipped sizes confirm it (M). This closes Study 5's open question on the in-game cap.

## 2. Trim sheets

- **Library:** 33 trim-sheet instances, 118 textures: floors, wall tiles, wallpaper, windows, fabrics, rope, paper, wood (M).
- **Rule** (WEAR/scripts/trim_by_texture.py): a slot is trim if its material's name has a TS or Trim token, or any material in its instance chain uses a T_TS or T_Trim texture.
- **Which meshes** (M): 70 slots, 30 distinct materials (18 found by name only). Mainly **window joinery**: 39 of 95 window-folder slots, 27 on the wood-elements sheet under the chipped-paint master, which paints over it; the rest Opera mouldings and floors, rope, beams. Facades are tiling plaster, not trim.
- **Sheet sizes:** square, 2,048 px authored, 1,024 shipped; rope 1,024/512; the basic window sheet 1,024 by 512 (M).
- **Texel density** (trim texture size × tiling × 100 / the slot's UV density in cm per UV unit; M, formula I): 52 slots with a sized trim texture, median **1,177 px/m authored, 589 shipped** (p10 802/401, p90 2,392/1,196). The narrower name-only rule in meshes.json gives 24 slots, 1,171/586, p90 1,478/739. Facade blends: 758/379 (88 slots).
- **Against our budget** (research/pre-production/4-BUDGETS.md): 512 px/m at walking distance, 1,024 where the camera comes within about 2 m (interiors). Mafia ships facades below 512 and trim near it (I).

## 3. Colour grade and fog

**Fixed, BP_TOD's post-process, overrides on** (R; EXP/Lighting/BP_TOD.json): bloom threshold 1.0, bloom sizes 1, 2, 3 and 6 at tint 0.066; film white clip 0.2; auto exposure metering 70 to 80% of the histogram, limits −3 to +1 EV100, "speed down" 3 (adapting into a darker scene); local exposure blurred-luminance blend 0.3 at a 40% kernel; motion blur 0.05. Film grain 0.035 is stored without its override: **unverified** (BP_TOD's functions not decompiled). Fog component: falloff 0.1, inscattering 0.15, volumetric fog on, 80 m. Sun: source angle 1°, indirect lighting 1.75.

**The grade is a small "colour head"** blended in by each preset (R): contrast 1.1, shadow contrast 0.9, offset (lifted blacks) 0.0125. Palermo's saved state shows 1.065, 0.935 and 0.008125: the head at 0.65 (R; arithmetic M). No grade names a LUT (M).

**By time of day** (M, medians of 103 presets, n under 10 marked; EXP/Lighting/PresetAssets, F:/LedgerTools/aaa-study/study-5/mafia_tod_presets.csv):

| | Day 10 to 17 h (60) | Dawn, dusk (22) | Night 21 to 05 h (21) |
|---|---|---|---|
| Exposure compensation, median (p10 to p90) | +0.6 (−0.25 to +2.25) | +1.35 (+0.5 to +2.85) | +3 (+1.0 to +3.9) |
| Exposure floor, EV100 | 1 | 0.5 | 1 |
| White balance (film temperature) | 6,050 K | 5,575 K | 5,000 K |
| Tint | −0.075 | −0.1 | −0.1 |
| "Film shadows" / "film highlights" | 0.9 / 0.85 | 0.9 / 0.8 (n 7) | 0.61 / 0.5 (n 7) |
| Colour head blend | 0.5 | 0.5 | 0.5 |
| Vignette | 0.33 | 0.4 | not set |
| Sun intensity, temperature | 10, 6,500 K | 10, 6,000 K | 0.026, 6,500 K |
| Height fog density | 0.0115 | 0.03 | 0.035 |
| Second fog density, falloff | 0.02, 0.28 | 0.1, 0.3 | 0.02, 0.2 |
| Fog colour multiply | 2.4 | 1.25 (n 9) | 0.25 |
| Fog maximum opacity | 0.5 | 0.8 (n 6) | 0.5 |
| Volumetric scattering distribution | 0.63 | 0.55 (n 8) | 0.65 (n 4) |

Palermo's saved state (R, a night, I): fog 0.035, second fog 0.02, volumetric 50 m; exposure bias 3.9; floor 1.0 (inherited from BP_TOD's override); local exposure highlight contrast 0.5, shadow contrast 0.62; vignette 0.

**How it changes:** each story beat has its own preset; five 0-to-1 curves in BP_TOD suggest cross-fades (I). Config: auto exposure with extended range, candela units, no lens flare or motion blur by default (R); "tonemapper quality 4" is set only at the lowest post-process level, so High and Epic keep the engine's default (R).

**Rooms get their own volume.** In the Opera rooms' cell (priority 1, blend 2 m) only two values are live: gamma (1, 0.978, 0.976) and shadow gamma (1, 0.936, 0.855), a warm shift strongest in the shadows (R). Its stored white balance 7,000 K, saturations 0.8/1.2, gain and highlight contrast have no override and do nothing (R). A disabled "Siciliano" volume is a film mode, not the town's look (I).

## 4. A small interior: the Opera's back rooms

No small shop or office is placed in Palermo's cells; the Town Hall's rooms (Floor 1 A to F, Floor 2 A to H) exist only as packed sublevels not placed in the exported cells (M). The nearest readable rooms are the Opera's.
- **Surfaces** (M): the street's masters again (vertex-paint two-layer 15 and 5, painted plaster, bare wood, a patterned-plaster trim sheet).
- **Decals** (M): within 25 m of the rooms, 172 (153 on walls): leaks 64, fresco pattern 60, red plaster patches 14, rug damage 5 (floor); wall centres 1.4 to 4.7 m up, median 2.2 m; width 2.4 m.
- **Light** (M; WEAR/scripts/opera_lights.py): 57 lamp lights, 49 with shadows set off. Single wall lamps (35): median 0.05 cd, 3,000 to 3,500 K, reach about 1 m, mostly 80° spots. Doubles (18): 0.125 cd. Ceiling four-ways: 0.01 cd. Also 35 placed spots, median 0.1 at about 5.5 m reach; 32 of them store no unit (unverified) and keep the default shadows. Mafia's scale is not physical (Study 5): only ratios carry over (I).

## 5. The method for LEDGER

**LEDGER now** (R): M_LedgerSurface (colour, normal, roughness, tiling, a grade); M_LedgerKit (world-aligned detail, a dirt band from the base, rain streaks, a "top" growth on faces turned to the sky); facade and office wear painted in Blender. 177 projected decals: 140 through M_LedgerGrime (colour and opacity only; tools/ue/make_grime_material.py), the 37 puddles through **M_LedgerWet**, which already writes colour, roughness, normal, specular and opacity from a mask picture (tools/ue/make_wet_material.py; VignetteShot.cpp). No material in tools/ue reads vertex colour, and the room recipe drops colour attributes on import (shop-room.py).

### Step 0: the calibration scene (once, then for every new piece)

- **Props:** the engine's SM_ColorCalibrator (UE_5.8/Engine/Content/EditorMeshes/ColorCalibrator): chrome ball, grey ball (clear-coated, albedo unknown), two clear-coat balls and a colour-checker grid stored as 16-bit linear values (R: the mesh's name table names five materials; a skin ball material sits in the folder, on no mesh). Mafia keeps the same kit for lighting review: a ColorChecker plane, an 18% grey sphere and Epic's chrome ball (R; EXP/Lighting/BP/BP_ColorChart.json); not placed in Palermo (M).
- **Scene:** a level made by script, in three states: the street by day and at night under a lamp pool (the scene specs' lights with the look file's gains, exposure and white balance) and Mickey's lit room (its own spec); photographed at High through the game's camera and exposure.
- **Reference values:** X-Rite's ColorChecker 24 L*a*b* (D50), charts made since November 2014 (https://babelcolor.com/index_htm_files/ColorChecker24_After_Nov2014.txt, linked from https://babelcolor.com/colorchecker-2.htm; both read in full 28 October 2026), converted by Bradford to D65 sRGB (M; WEAR/summary/colorchecker_after2014_srgb.json; reproduced exactly by the review). Neutrals, sRGB (linear): white 241, 242, 235 (0.88); neutral 8: 201 (0.59); 6.5: 161, 163, 163 (0.36); **neutral 5: 121, 121, 121 (0.19)**; 3.5: 84 (0.09); black 50 (0.03). BabelColor reports that the third neutral from the left (neutral 6.5) "is often recommended" for grey balance; neutral 5 is the most neutral after conversion, so C3 checks both.

| Check | What is measured | Pass (tolerances I, fixed after the first run) |
|---|---|---|
| C1 chart | base-colour view, all 24 patches against the table | ΔE2000 mean ≤ 2, worst ≤ 4; else Epic's offset recorded once and used from then on |
| C2 exposure, day | neutral 5 as displayed; the grey ball only after its base colour is read in the editor | neutral 5 at 110 to 135; six neutrals in order, each step ≥ 8 levels; white ≤ 250, black ≥ 20 |
| C3 white balance, day | neutral 5 and neutral 6.5, red/green/blue | each within 4 levels; at night the warmth recorded (red minus blue), not failed |
| C4 night pool | a chart neutral in the pool and between pools, in linear light | pool at least 4 times the dark between |
| C5 chrome ball | its reflection | brightest highlight ≥ 240 and on the key light's side within 30°; under 1% of its pixels at 0 |
| C6 each new piece | base-colour, roughness views; texel density | albedo 0.03 to 0.88; plaster, brick, wood median 0.09 to 0.36; density within 20% of 512 px/m outside, 1,024 inside |

Study 5's exposure numbers are kept beside ours (the presets: day −0.25 to +2.25, night +1.0 to +3.9, p10 to p90; floor 1.0 EV100; R), not copied: our light is physical, so the scene compares displayed values, never settings (I).

### The layer recipe, shared by both

1. **One decal material for both methods, built from M_LedgerWet** (reuse first; not a new one): its colour, roughness, normal and opacity wiring, with (a) a drawn stain picture and height-to-opacity for leaks, streaks and rust, (b) a mask over a tiling roughness or colour map, tiled 1 to 2, for grunge and damp. Check: a stain differs from its wall by ≥ 0.1 in the roughness view and darkens the base colour by ≤ 40% (I).
2. **Decal density by Mafia's street count:** median 1 a wall, at most 6 where the player looks; leak stains about two in five. Check: count by kind per wall.
3. **Wear in the material first**, decals only for particular marks. Check: no wall's base colour uniform: brightness varies ≥ 10% across a wall at 5 m (I).
4. **No detail normals** unless a gate asks (Mafia: at most 9 of 358). Check: none added.

### Mickey's office (the first use)

Reference: section 4; WEAR-2026-10-25.md's ranked target.
- **O1 smoke:** Mafia places second layers by vertex paint; our pipeline carries none, so the smoke is painted into the room recipe's texture by height, as its other wear is: full at the ceiling, none 1.2 m above the floor, yellow-brown, roughness 0.1 lower (I). Mafia's height-blend values are no target (set in 7 to 13 of 35; the main street keeps defaults); the edge is broken by the plaster's own texture. Check: ceiling red-over-blue ≥ 1.15 times a pale wall's.
- **O2 decals, 10 to 14** (4 walls and a floor, at most 6 a wall; the earlier research's 10 to 20): pale patches behind the calendar and notices, grime at the switch, push plate and handle (15 to 25 cm), base scuffs at the skirting, the damp stain and head marks kept. The carpet path as one or two floor decals that darken and roughen the pile, as the Opera's rug decals do: a new direction after the two set-aside tries, only under his set-aside rule. Check: count by kind, ≤ 6 a wall, each through C6.
- **O3 door and frame:** Mafia's chipped-paint medians as the target (fade 0.89, weathering 0.66, dirt 1.25, dirt roughness 0.8, wood edge 2.3), painted from the props' occlusion and edge masks already made. Check: bare or worn paint 3 to 10% of the door leaf, all within 5 cm of an edge or the handle (I).
- **O4 the room's grade:** a room volume with a 2 m blend and only Mafia's live values: gamma (1, 0.978, 0.976), shadow gamma (1, 0.936, 0.855). Check: neutral 5 in the room shadows warmer (red minus blue) by 3 to 8 levels, neutrals in order, none clipped (C2), then the Hook sheet.
- **Light:** unchanged (it passed). Mafia's small lamps mostly cast no shadows; ours keep theirs inside by his yes of 26 October (WEAR-2026-10-25.md, "Shadows raised only inside").

### One shop front: the chandler (east_chandler_bay0)

The one standalone shop front with every part (stall riser, pilasters, fascia, transom, two doors); 8 decals now: two splash bands, two washes, two damp bands, two sill streaks (M).
- **S1 decals** through step 1: sill streaks as drawn pictures lengthened to the fascia or stall riser (1.5 to 2.5 m, I), one rust leak under the gutter's end (Mafia's 2.1 m tall by 0.55 m), threshold grime, the base band kept. Check: 8 to 10 on the bay, ≤ 6 a wall, leaks and streaks about two in five.
- **S2 joinery:** a paint-over-wood variant of M_LedgerKit by Mafia's chipped-paint layer, on one wood trim sheet that does not yet exist: made or sourced with its licence line, and a UV remap in the generator. Check: 512 px/m within 20%; worn paint 3 to 10% of the joinery, at edges.
- **S3 brick:** per-house tint and wear stay; a world-noise streak tint in the brick material (Mafia: 10.7 by 11.1, power 0.56). Check: streaks shift brick brightness 5 to 15% across a bay in the base-colour view (I).
- **S4 glass:** unchanged. Mafia's building windows use an opaque fake glass with grunge build-up (roughness 0.08 to 0.2, specular 0.5 to 0.8; R), answering Study 5's open window point; ours stays as ruled.

**Each new piece:** placed beside the chart and balls in the three states; C6 passed before any gate picture.

### Estimate (I)

Done means the packaged build walked by the AI tester. Calibration scene, script and three states: 6 to 8 h. Step 1 from M_LedgerWet: 2 to 3 h. The office, O1 to O4 with pictures, reviewers and the packaged walk: 8 to 12 h. The chandler, with the wood trim sheet and its licence line: 8 to 12 h. **About 25 to 35 hours**, two tries each; one office wear round took 45 minutes to an afternoon, the light fix most of a day. No Unreal run while the build machine builds.

## Not read, or unconfirmed

The masters' wiring and vertex-colour channels; BP_TOD's functions (film shadows and highlights, colour-head blend, film grain); the albedo of Mafia's grey sphere and of Epic's grey ball and chart (C1, C2 measure Epic's); 606 decals' location materials (partly exported); Mafia's real light scale. The street level is a proxy and the per-wall grouping a rule of thumb; Opera room decals are not separated from the walls around them. Kingdom Come II was not part of this dive.

## Review applied (fresh reviewer, 28 October evening; scratchpad/mafia-wear/REVIEW.md)

Pass with fixes; each fix re-measured from the kept files (new scripts street_groups.py, trim_by_texture.py, opera_lights.py; override flags read). F1: the room's live grade is the warm gamma only (O4); film grain unverified. F2: per wall on street kinds, median 1; 30% of boxes at the base. F3: leaks are drawn pictures; two decal methods. F4: O1 takes no Mafia height values; smoke painted by height. F5: step 1 builds on M_LedgerWet. F6: no skin ball; C2 on neutral 5. F7: the quote concerns neutral 6.5; C3 checks both. F8: trim numbers reproduced, rule stated. Seventeen smaller corrections made in place. Every step has a numeric check; estimate 17 → 25 to 35 hours.
