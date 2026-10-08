# The wet road's near-white mirror: why, the target, the change

Lab, 8 October 2026, 11:10 to 11:22. For the builder. Code read on origin/wip at 73d61fae and in the installed UE 5.8.2 (C:\Program Files\Epic Games\UE_5.8). Numbers come from production/lab/road/road_numbers.py, which reruns them. Published sources are in production/lab/road-sources.md (a helper's search, D = read at source, S = summary only, I = computed).

## In short

- **The flat normal itself is not the fault.** A flat, smooth film at Specular 0.5 is optically a sheet of water, and the engine renders it as one: 0.39 of the sky at 10° above the road, against water's Fresnel of 0.35.
- **The fault is that our road is all film.** A wet chipped road is only partly under unbroken water: the stone tops pierce it. The Hook sheet's road asks for 0.41 to 0.60 of what we reflect.
- **The change:** lower the asphalt's Specular when it is a film, from 0.5 to about 0.13. The engine's micro-occlusion rule then halves every reflection on the road. Roughness and the flat normal stay, so the reflections stay sharp.
- **First,** one number in the look file. **Then,** the same mean, broken up by the asphalt's own grain.
- **What remains:** the reverse view's centre needs less (0.60) than the hook's near lane (0.41). That is the sky dome, not the road (see "What the road cannot fix").

## 1. Why the road is a flat mirror (our code)

1. **The look file turns the film on, and turns the water level off.**
   - production/specs/unreal-look.json:13 sets `wet_film_from` to 0.5, and :107-108 set `water_level_day` and `water_level_night` to 0.0. The level was set aside at 10:05 today.
   - The day view runs at wetness 0.85 (production/specs/vignette-pieces.json:27, overcast_day).
2. **The game swaps the asphalt's relief for a flat normal** (ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp):
   - `bFilm = C.Wetness >= GLook.WetFilmFrom` (:7929);
   - the level is 0 (:7935);
   - `bFlat = bFilm && Level <= 0.0` (:7937);
   - the flat texture goes into the normal map (:7939).
3. **The roughness goes nearly to a mirror.**
   - VignetteShot.cpp:7916 sets Wetness by `LedgerStreet::WetnessParamFor` (ue-probe/Source/LedgerProbe/Public/StreetMeshes.h:288-296). With the look file's asphalt floor of 0.06 (unreal-look.json:116) and wetness 0.85 that gives 0.948 (I).
   - M_LedgerSurface's roughness is `Lerp(RoughnessMap.R, 0.08, Wetness)` (tools/ue/make_base_material.py:249, :3715), so the road sits at about 0.08 to 0.10.
4. **The reflectance stays at the dielectric default.**
   - The material's Specular is `Lerp(0.5, 0.25, water mask)` (make_base_material.py:3917, :3945). With the water level at 0 that is 0.5, so F0 is 0.04.

## 2. What the engine does with it (UE 5.8.2)

- **Lumen's reflections are scaled by the energy-conserving GGX reflectance** (Engine/Shaders/Private/DiffuseIndirectComposite.usf:635-641, applied at :651-653). The energy conservation is on by default: `r.Shading.EnergyConservation` defaults to 1 (Engine/Source/Runtime/Renderer/Private/ShadingEnergyConservation.cpp:17-19).
- **The reflectance formula** is `E = W·(E.x·F0 + E.y·(F90 − F0))` (ShadingEnergyConservationTemplate.ush:62), with `F90 = F0RGBToMicroOcclusion(F0)` (:84), which is `saturate(50·F0)` (ShadingCommon.ush:161).
  - At grazing angles the F90 term dominates.
  - F90 is full for any F0 of 2% or more, that is any Specular of 0.25 or more. That is why the water level's Specular 0.25 changed nothing at grazing.
  - Below that, the engine treats the shortfall as shadowing and scales the grazing reflection down in proportion. The older path carries the same rule and comment ("Anything less than 2% is physically impossible and is instead considered to be shadowing", BRDF.ush:409, :598).
- **Computed with that formula at roughness 0.10 (I):**

| Above the road | Water, Fresnel | Ours, Specular 0.5 | Specular 0.25 | Specular 0.15 |
|---|---|---|---|---|
| 5° | 0.584 | 0.577 | 0.569 | 0.341 |
| 10° | 0.348 | 0.389 | 0.377 | 0.226 |
| 15° | 0.212 | 0.247 | 0.232 | 0.139 |
| 20° | 0.133 | 0.155 | 0.138 | 0.083 |
| 25° | 0.087 | 0.100 | 0.082 | 0.049 |

So our road is a pond.

## 3. What a wet road should reflect (published measurements)

- **Water's Fresnel is the ceiling** (n = 1.333, unpolarised): 0.72 at 3°, 0.58 at 5°, 0.35 at 10°, 0.21 at 15°, 0.13 at 20° (I; road-sources.md). It applies only where the water is deep enough to cover the stone tops: a puddle.
- **A wet chipped road is not a puddle.**
  - UK chipped asphalt has 1.0 to 1.8 mm of texture, and in ordinary rain the water stays below the stone tops (the builder's sources, WET-ROAD-2026-10-08.md 1-3, D).
  - The wet stone between is darker and shinier, but not a mirror: diffuse brightness about halved when wet (Lekner and Dorf 1988, D), the specular coefficient up 3 to 12 times its dry value after flooding (Pattanapakdee and Chotigo, CIE x046:2019, D).
- **The model this supports:** reflectance ≈ f × Fresnel(angle) + (1 − f) × the wet stone's own, where f is the share of the surface under unbroken water.
- **What no source gives.** No source reached measures f, or the sky reflection of wet asphalt at 3 to 20° (road-sources.md, "unreached"). The road-lighting tables (CIE 47's W classes; Q0 0.11 to 0.25) assume a viewer at 1° under overhead lamps, so they do not apply here. **So f comes from the Hook sheet, and it lands where the physics allows.**

## 4. The target, per view

The gate's own readings (production/audits/sky-2026-10-08/GATE-SKY-REVIEW.md:17-18) are taken back to scene-linear light through the engine's inverse film curve (TonemapCommon.ush:227-256, default curve). The road is almost all reflection (asphalt surface gain 0.13), so the factor below is how far its reflection must fall.

| View | Region | Below the horizon | Now | Sheet | Linear now → sheet | Factor needed |
|---|---|---|---|---|---|---|
| Hook, day | near lane (about x 0.18-0.32, y 0.80-0.92) | 18-22° | 207 | 152 | 0.640 → 0.260 | **0.41** |
| Reverse, day | centre | about 20-25° | 196 | 164 | 0.509 → 0.305 | **0.60** |
| Reverse, day | middle | builder's region | 222 | 183 | 0.948 → 0.404 | **0.43** |

The angles come from the cameras: cam_hook 2.2 m up, cam_reverse 1.7 m, both pitched −3.4° with a 46° vertical view (vignette-pieces.json:22, :24). Rows 0.80 to 0.92 of the frame lie 17.7 to 21.3° below the horizon.

**Accept:**
- each region within 12 levels of the sheet (the builder's own test, WET-ROAD-2026-10-08.md §4);
- the hook's whole road region still near 41% of the sky (now 43.4%; sky_regions.py "road" reads 160 against the sheet's 162 today, so the average is already right; only the near lane and the reverse's near road are too bright);
- the night hook checked by eye.

## 5. The change

**Step 1, one number (the asphalt's film specular):**
- **make_base_material.py:3917:** replace the lerp's constant A pin (0.5) with a scalar parameter `FilmSpecular`, default 0.5. That is the material exactly as today for every surface that sets nothing.
- **VignetteShot.cpp, beside :7937:** where the asphalt becomes a film (`bFilm && Rw.Base == "asphalt"`), set `FilmSpecular` from a look-file key `film_specular` (proposed 0.13). Every other condition and surface gets 0.5.
- **The engine's effect:** F0 0.0104, so F90 = 0.52, and every reflection on the road is scaled to about half (×0.44 to ×0.53 by angle). Nothing else changes: roughness, the flat normal, the colour, the sky light.

Predicted (I, from the engine's ratio at each region's angle, through the inverse and forward film curve):

| film_specular | Hook near lane (152) | Reverse centre (164) | Reverse middle (183) |
|---|---|---|---|
| 0.50 (today) | 207 | 196 | 222 |
| 0.15 | 172 (+20) | 155 (−9) | 199 (+16) |
| **0.135** | **165 (+13)** | **147 (−17)** | **194 (+11)** |
| 0.125 | 159 (+7) | 141 (−23) | 189 (+6) |
| 0.115 | 153 (+1) | 135 (−29) | 185 (+2) |

**Step 2, the same mean, broken up by the grain** (if step 1 reads as dark glass): Specular = 0.25 × c per texel.
- c is 1 in the asphalt's hollows and about 0.25 on its stone tops.
- Use the material's existing grain (the base colour's luminance, make_base_material.py's water-level `grain` and `grain_s`) with **no world noise.** The metre-scale noise is what made today's pools blobby.
- Set the threshold so the mean of c equals film_specular / 0.25.
- This is Epic's documented route for small-scale specular shadowing, a cavity term multiplying Specular. Keep roughness and the flat normal: varying roughness is what read pale and matte at 0.28.

## What the road cannot fix

- **The three regions need factors of 0.41 to 0.60.** One road value cannot put all three within 12 levels: 0.13 to 0.135 is the best compromise, at worst about ±15.
- **The difference is the sky each mirrors.** The hook's near lane and the reverse's centre lie at the same angle (about 20° below the horizon), but they mirror opposite arcs of the dome. The builder measured the dome at 16° as 0.46 to 1.39 of its zenith by direction (WET-ROAD-2026-10-08.md §3; CIE overcast 0.52), repeated below 16° (sky_horizon_clamp_deg 16).
- **Do not tune the road per view.** If the reverse's centre reads dark after step 1, check which arc of the dome it mirrors, as the builder's own research asks. That is a sky question.

## Not checked here

- Lumen's reflection-ray band (roughness below 0.4) and the sky's capture: the builder's citations, not re-read.
- The local-exposure and tone settings beyond the default film curve. The predictions above assume the default curve and the pinned exposure, so they are for steering; the frame decides.
