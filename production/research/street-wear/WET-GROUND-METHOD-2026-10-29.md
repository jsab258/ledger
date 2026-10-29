# Wet ground at real albedo: one method (29 October 2026)

After the two tries set aside at 14:27 (DECISIONS.md). Builds on PUDDLES-2026-10-02.md, WET-ROAD-2026-10-08.md and lab/ROAD-NOTES.md without repeating them. Tags: **M** measured here, **R** read at the source, **I** inferred. Every link was read on 29 October 2026.

## Questions

1. How do shipped games and Epic make a wet street at real albedo read wet without a mirror or polished tile?
2. What do the Mafia and Kingdom Come II studies say about wet ground?
3. How should dark decals behave when the surface under them is brightened?
4. How is a lamp pool on brighter wet flags kept from burning out, with darkness kept between pools?
5. What should the game change, in order, each with a source and a check?

## The failure, measured (M)

Frames: this morning's previews (day at pin 2, a stop brighter than now), rounds 2 and 3b (F:/LedgerTools/gate/new/look), the Hook sheet (production/reference/hook-sheet.png, its own middle road). Scripts in the session scratchpad (wetmeasure.py, sheetmeasure.py, plainroad.py).

| | Morning | Round 2 | Round 3b | Sheet |
|---|---|---|---|---|
| Night, nearest pool on the flags: pixels with a channel ≥ 250 | 0.1% | 15.4% | 15.6% | |
| Hook middle road: dash to road, linear | 16.8 | 6.0 | 5.0 | 1.8 |
| Middle road, mean sRGB | 82/74/68 | 117/104/97 | 118/105/98 | 185/188/193 |
| 2c targets 152, 164, 183 | 169, 150, 186 | 178, 163, 192 | 178, 163, 193 | |

- The pool clipped once the flags' gain rose (round 2, wet floor still 0.10): the diffuse gain burned it, not the gloss (I from M).
- The sheet's dashes are fainter than the game's. The "milky" road is a warm, structureless sheet where the sheet's road carries the sky's cool colour (I).

## 1. How it is done

**Wet is two states, not one.**
- *Saturated stone* (Lagarde's "wet" zone): diffuse × lerp(1, 0.2, porosity); gloss = lerp(1, gloss, lerp(1, factor, 0.5 × wetness)), the 0.5 an empirical cap on the shine. Worn asphalt 0.12 becomes 0.08. The normal is unchanged (Water drop 3b, https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/; 2b, https://seblagarde.wordpress.com/2013/01/03/water-drop-2b-dynamic-rain-and-its-effects/) (R).
- *Water*: gloss 1, F0 0.02, normal blended to flat by the water's height (3b, 2b) (R).
- **In Unreal terms (I):** his gloss is specular power 2048^gloss (0.5 is power 45, 0.1 power 2; 3b). Through α = √(2/(n+2)) and roughness = √α, dry flags and asphalt at 0.69 to 0.83 become wet stone at **0.54 to 0.68**. The shine comes from the water's share, not the stone.
- **Where water stands.** Remember Me (named in 2a, https://seblagarde.wordpress.com/2012/12/27/water-drop-2a-dynamic-rain-and-its-effects/) used two flood levels: the height map's hollows, min(level, 1 − height), and painted puddles, saturate((level − mask)/0.4); the larger wins (2b) (R).
- **Detail under the film.** A thin layer keeps the surface's own normal; only thick water goes flat (3a, https://seblagarde.wordpress.com/2013/03/19/water-drop-3a-physically-based-wet-surfaces/; 3b) (R).
- **Variation is a cue:** surfaces dry unevenly; puddles outlast the ground (Water drop 1, https://seblagarde.wordpress.com/2012/12/10/observe-rainy-world/) (R).
- **Far Cry 6:** a puddle is a terrain decal whose alpha gradient writes the terrain's porosity, scattered by the road recipes; a wetness shadow map dries sheltered places (https://www.ubisoft.com/en-us/company/how-we-make-games/technologies/articles/simulating-tropical-weather-in-far-cry-6) (R).
- **Uncharted 4** (Brinck and Maximov, SIGGRAPH 2016): a flat core, a surface-tension rim, a saturated zone darkened without new normal or shine, dry ground. Known only through a README (https://github.com/brugr9/Wetness): secondary, UNVERIFIED.
- **Epic:** no page on wet surfaces was found. Lumen supports clear coat "with dual normals": only the top layer may be smooth, the bottom is assumed rough (https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine) (R).
- **Engine source, UE 5.8 on this PC (R):** the coat's F0 is hard-coded 0.04, scaled by the coat amount (ShadingModels.ush 406-407; ClearCoatCommon.ush 59-74). Lumen takes the coat's roughness for its traced ray (LumenMaterial.ush 677) and lights the bottom from screen probes with its own normal (LumenScreenProbeGather.usf 1519-1524). Clear coat is marked deprecated by Substrate since 5.7 (ShadingModels.ush 357); Substrate is off by default (RenderUtils.cpp) and the project sets none.

**The game today (R, project files):** from wetness 0.5 road, flags and kerb lose their relief (wet_film_from); roughness 0.06 to 0.15; one darkening of 0.72 for every surface (StreetMeshes.h WetDarken). That is Lagarde's puddle zone over the whole street: on dark colours it read wet, on real colours polished tile (I).

## 2. Reference first

- **Mafia** (studies/05-visuals.md; MAFIA-WEAR-2026-10-28.md; R and M there):
  - one global wetness drives roughness to 0.1 on flat ground, 0.2 on slopes; how its master scales this was not exported;
  - puddles are decals carrying roughness, height and occlusion, **no colour map**: tint (0.78, 0.65, 0.46), alpha 0.94, a 2×2 atlas; Palermo's streets hold 145 ground puddles and 13 edge-wetness decals;
  - all five decal masters take the global wetness;
  - at night, local exposure highlights 0.5, shadows 0.62.
- **Kingdom Come II:** rain is a screen layer to 150 m; no wet-ground material among 7,572.
- **Not found:** either game's albedos or wet gloss. Structure from Mafia (one global wetness, colourless puddles); values from Lagarde and the measured bands.

## 3. Decals on brighter ground

- **The engine's blend** is BaseColor × (1 − α) + colour × α (DBufferDecalShared.ush 513). Modulate falls back to translucent on DBuffer (https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-materials-in-unreal-engine) (R).
- So only black is relative: black at opacity 1 − k multiplies by exactly k. Any other colour adds a fixed amount.
- **M_LedgerWet writes a fixed colour,** WetTint 0.035 at strength 0.7 to 1.0 (make_wet_material.py; street_wear.py). On the morning's flags (about 0.03) its core read ×1.1 to ×1.2, invisible. On real flags (0.15) it reads ×0.23 to ×0.46: a dark cut-out, hard-edged by the sharpened core (CORE_FROM 0.30, CORE_GAIN 3) (M, arithmetic).
- **M_LedgerGrime** lays the stain × GrimeTint 0.2, not black, so its darkening also shifts with the ground (I).
- **The professional answers:** puddles with no colour (Mafia), or a decal that only feeds the surface's own wetness (Far Cry 6). Epic lets the receiving material read the DBuffer for its own blend, with Decal Response None to avoid applying it twice (same page).
- Water over stone already wet barely darkens it further. A puddle's darkness is the dark things it mirrors (3b; the sheet's right-hand puddles read 103 against their flags' 136, M).

## 4. Night pools on brighter flags

- **Albedo scales pool and gap alike** in linear light, so their true ratio holds. The film curve squeezes it: the pool climbs into the shoulder and clips (15.6%), the gap climbs out of the toe (the reviewer's 12 to 1 becoming about 5 to 1) (I from M).
- **Mafia's exposure moves lamps and dark alike;** the pool is the lamp-to-ambient ratio (studies/05-visuals.md) (R). So the lamps, not the exposure, should absorb the brighter flags; the exposure also sets the lit windows, which pass (I).
- **Local exposure** applies Highlight Contrast only where the blurred brightness is above middle grey; shadows take Shadow Contrast (PostProcessHistogramCommon.ush 279-308) (R). Epic advises 0.6 to 1 (https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-exposure-in-unreal-engine) (R); Mafia 0.5 at night. A pool three stops over middle grey at 0.75 drops to 2.25; the gaps do not move (I).
- **The lamp's glare.** Polished flags mirror the lamp head into the hot patch. Broken water gives glints along the lamp's vertical line instead (Water drop 4a, https://seblagarde.wordpress.com/2013/09/08/water-drop-4a-reflecting-wet-world/) (R).
- This keeps his ruling: pools of light with darkness between, lit windows, not one orange wash.

## 5. What to change, in order

A new direction, not the 8 October water level (one lobe of mixed roughness at the old dark colours): a two-lobe surface, tried first on the hook view's near flags and near lane, then the street, at the true exposure.

1. **Base colour: real dry values, darkened by porosity.** Asphalt 0.10 to 0.12 × 0.68 to 0.75; flags 0.21 to 0.37 × 0.50 to 0.65 (WET-OVERCAST-VALUES; FLAGS-BRICK-BANDS; Lagarde 3b). WetDarken's one 0.72 becomes a factor per surface. **Check:** base-colour view (surface_values.py): road 0.05 to 0.06, flags 0.11 to 0.20.
2. **Wet stone: rough, with its relief.** Roughness 0.54 to 0.68 (§1); wet_film_from no longer flattens it. **Check:** the roughness view within 20 m shows two groups, ≤ 0.05 and ≥ 0.45, under 10% between 0.2 and 0.39 (WET-ROAD's test; the 10% is I).
3. **Water as a coverage, in the clear coat.**
   - Coat = coverage c; coat roughness 0.02 to 0.05; top normal flat; bottom normal the stone's (ClearCoatBottomNormal; r.ClearCoatNormal 1, project-wide).
   - c from the surface's height against a water level, plus a painted mask for kerb channel, wheel paths and dished flags: Lagarde's two flood levels, margin 0.4, no metre-scale noise (ROAD-NOTES).
   - The coat's 0.04 is within about 17% of water's Fresnel at 10 to 20° above the road (ROAD-NOTES: 0.389 against 0.348; 0.155 against 0.133).
   - Mean c: road 0.4 to 0.6 (ROAD-NOTES' factor from the sheet); flags 0.2 to 0.35, a guess (I); paint lines 0 to 0.2, as raised thermoplastic sheds water (I, UNVERIFIED).
   - Fallback: ROAD-NOTES step 2, Specular 0.25 × c, in Default Lit.
   - **Checks:** 2c's three regions within 12 levels; middle road blue at least its red, as the sheet's (now 118/105/98); near-lane linear p90/p10 at least the sheet's 1.71 (M); middle dash to road between 1.8 and 6 (I).
4. **Decals relative.** Puddle decals write no colour, only roughness, normal and specular, or feed c through a DBuffer read as Far Cry 6's feed porosity. Darkening stains lay black at opacity 1 − k. **Check:** each ground decal's base-colour ratio to its surround changes by under 0.05 when the ground's gain is doubled (stain_check.py, twice).
5. **Night: the lamps take the albedo.** Divide lantern_pool_lumens (whichever night-gaps cone is in force) by the flags' new over old base colour, measured under the nearest lamp: about 2 to 4 (I). Then night highlight contrast 0.75, shadows 1. **Checks:** nearest pool's clipped share ≤ 2% (8 October rule; now 15.6%); C4 pool to gap 4 to 20 in linear light, near black ≤ 50% (NIGHT-GAPS-2026-10-29.md); lit windows within 5 levels of tonight's (I).
6. **Then the gate:** a fresh reviewer per view beside its last good picture; the packaged build last.

## Unverified, or not reached

- **Unverified:** Brinck's zones (secondary); the gloss-to-roughness conversion (a standard approximation, not Lagarde's); coverage on flags and lines; Mafia's master and puddle tint; the clear coat's cost, compile time and how decals reach its bottom layer; its future after Substrate; the lamp divisor; every threshold marked I.
- **Not reached:** Uncharted 4's slides (13 MB PDF, over the reader's limit); GDC Vault's Remember Me and Far Cry 6 talks (login); any Watch Dogs, Assassin's Creed or Last of Us wet-road talk (none found); Water drop 4b (never written, per its author); real photographs' pixels (the page reader cannot read them).

## Revised after review (29 October 2026, 15:02)

A fresh reviewer (WET-GROUND-METHOD-REVIEW-2026-10-29.md) passed this file with fixes; they stand here and win over the steps above where they differ:
1. **Step 3: the coat's top normal is not flat everywhere.** Lumen's diffuse reads the top normal, and under an overcast sky that diffuse is nearly all the light, so a flat top would lose the stone's relief again. The top normal blends from the stone's to flat by the water cover c, as Lagarde does.
2. **Step 2: the roughness check needs a view of c.** Under a clear coat the roughness view shows only the stone; a debug view of the cover (a material switch writing c to emissive) is made before the check is read.
3. **Step 4: decals cannot write the coat**, so only the route that reads the decal buffer into the surface's own wetness is left.
4. **Step 3's mean cover (road 0.4 to 0.6, flags 0.2 to 0.35) was set at 8 October's brighter exposure;** at the true exposure it misses 2c's own targets by about 30 levels, so c is re-derived against 2c at the true exposure before it is a target.
5. **Step 1: the wet base colour subtracts water's own 0.02**, and the flags' band has one home (FLAGS-BRICK-BANDS-2026-10-29.md, revised), not two.
6. **Step 5 changes one thing at a time:** the lamps' output alone first, measured by the project's pool_clip.py (clip at or under 2% in the nearest pool, pool to gap 4 to 20); the night's highlight contrast only if that fails.
The checks of steps 3 and 4 have no project tool yet; each is written before its step is tried.

## Step 3's build, planned (29 October 2026, evening)

- **Where it lives:** a ground-only copy of the street material (asphalt, flags, kerb), so the walls and fronts keep today's cheaper default-lit shading; the game picks it by surface (VignetteShot.cpp's street rows). Reason: a clear coat on the shared material would make every wall pay its cost; the frame-time step measures the copy (I).
- **The coat's amount c:** the material's existing water mask (the texture's grain and a broad noise against the water level, today on the asphalt only), extended to the flags and kerb with their own level; plus a painted channel along the kerb later (step 3's second half).
- **The two layers:** coat = c, coat roughness 0.03; the bottom layer's roughness the wet stone's (the look file's wet floor, 0.54 to 0.68 by step 2); the top normal eased from the stone's to flat by c (the review's fix 1) and the bottom normal the stone's, through Unreal's clear-coat bottom-normal output, which needs r.ClearCoatNormal on for the project (one shader permutation more; recorded when set).
- **Its checks:** tools/wet_ground_check.py road (the sheet's three regions, blue over red, the near lane's relief, the dash) on the hook and reverse day views, at the true exposure, after c is re-derived there (the review's fix 4); then the gate.
- **Not yet decided:** the flags' level and the painted channel; both measured, not guessed.
