# Wet overcast street: real values for the look calibration (29 October 2026)

His page of 29 October: the camera stays; check how bright the pavement, road and brick are, and how strong the daylight is, against real values and real photographs, then the street beside the Hook sheet. Tags: **M** measured or computed here, **R** read at the source, **I** inferred. Every link was read on 29 October 2026.

## Questions

1. Diffuse albedo, dry and wet, of aged asphalt, concrete flags, red and stock brick, painted render?
2. How much does wetting darken each?
3. Overcast daylight around noon, late October, 51.5 N: illuminance, sky luminance, EV100?
4. In a real exposed photograph of a wet overcast street, where do road, pavement, brick, sky and an 18% grey land (8-bit sRGB)?
5. How do Unreal's light units and exposure relate, and what exposure puts mid grey at mid grey under ~10,000 lux?
6. What do Mafia and Kingdom Come II use?
7. What are the game's current numbers in the same units, and what is non-physical?

## 1. Albedo

- **Asphalt:** fresh 0.05; old streets 0.11 to 0.12 (Pomerantz, Akbari, Chang, Levinson, Pon, LBNL-49283, pyranometer, solar albedo; https://eta-publications.lbl.gov/sites/default/files/lbnl-49283.pdf) (R). Fresh 0.04, worn 0.12 (Lagarde 2011, from Wikipedia's albedo page; https://seblagarde.wordpress.com/2011/08/17/feeding-a-physical-based-lighting-mode/) (R, secondary).
- **Concrete:** pavements 0.18 to 0.35 (LBNL-49283) (R); new 0.55 (Lagarde 2011); 0.51 linear (https://api.physicallybased.info/materials, from Lagarde) (R). No British flag measured; weathered flags taken as 0.20 to 0.35 (I).
- **Red brick:** linear (0.262, 0.095, 0.061) (physicallybased.info) (R), luminance 0.128 (M); its measurement is not stated: UNVERIFIED. Solar albedo overstates red brick's visible brightness (I).
- **Stock brick, render:** none reached (UNVERIFIED).

## 2. Wetting

Lekner and Dorf, "Why some things are darker when wet", Applied Optics 27(7) 1278, 1988 (https://www.wgtn.ac.nz/scps/about/staff/pdf/darkerwhenwet.pdf; all three scanned pages read). Their equations 1, 8, 9 and 11 evaluated here for water (n 1.33) on a mineral (n 1.5; n 2 differs by under 0.01) (M; p = 0.475 reproduces the paper's figure):

| dry | 0.05 | 0.08 | 0.12 | 0.20 | 0.30 | 0.35 |
|---|---|---|---|---|---|---|
| wet | 0.045 | 0.060 | 0.081 | 0.127 | 0.19 | 0.225 |
| ratio | 0.90 | 0.75 | 0.68 | 0.64 | 0.63 | 0.64 |

Measured pairs quoted in the paper (Ångström 1925): sand 0.182 to 0.091 (0.50), black mould 0.141 to 0.084 (0.60) (R). So rough solids lose 25 to 50%; surfaces under about 0.05 hardly darken. Lagarde's reading of the same curve, 0.68 at 0.12 (https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/), agrees (R). Water's own reflectance at normal incidence: ((1.33 − 1)/(1.33 + 1))² = 0.020 (M).

## 3. Daylight

- **Sun height** at local noon, 29 October, 51.5 N: 25.3° (M).
- **Measured irradiance:** EU PVGIS, satellite data SARAH-3, London (51.5 N, 0.12 W), hourly 2005 to 2023 (https://re.jrc.ec.europa.eu/api/v5_3/seriescalc?lat=51.5&lon=-0.12&startyear=2005&endyear=2023&outputformat=json&components=1&angle=0). Noon hours, 15 October to 12 November, overcast (direct beam under 5% of the total): 370 hours; global horizontal p10 53, p25 69, median 95, p75 135, p90 159 W/m² (M).
- **In lux:** at 110 to 115 lm/W for overcast skylight (Littlefair, Garston; from a search summary only: UNVERIFIED): p10 about 6,000, p25 7,900, median 10,900, p75 15,500, p90 18,300 lux (M). Heavy or rainy overcast is the lower quarter, 6,000 to 8,000 lux.
- **Cross-checks:** "A realistic horizontal illuminance for a (brightish) overcast sky is 10,000 lux" (Mardaljevic, Rendering with Radiance ch. 6; https://www.radiance-online.org/community/workshops/2003-berkeley/presentations/Mardaljevic/rwr_ch6.pdf) (R). Wikipedia's uncited "overcast day 1,000 to 2,000 lux" (https://en.wikipedia.org/wiki/Daylight) contradicts the measurements and is not used.
- **Sky luminance:** CIE standard overcast sky (Moon and Spencer; CIE 1955): L = Lz (1 + 2 sin γ)/3, horizontal illuminance 7πLz/9 (Mardaljevic, R; integral checked, M). At 6,000 to 18,000 lux: zenith 2,500 to 7,500 cd/m², horizon a third of that (M).
- **EV100:** ANSI PH2.7: "cloudy bright (no shadows)" 13, "heavy overcast" 12 (https://en.wikipedia.org/wiki/Exposure_value) (R). Incident meter, C 250: 6,000 lux is EV100 11.2, 10,900 is 12.1, 18,300 is 12.8 (M). Two real rainy-street exposures from their camera data (M): St Albans, 28 February 2020, 14:10, sun 25.1° (the height of late-October noon), f/22, 1/200 s, ISO 2500: **EV100 11.9**; Fletcher's Terrace, 16 December 2025, 11:14, phone: 12.3 (approximate).

## 4. Real photographs

Each Commons copy of a Geograph photograph viewed in the built-in browser, its pixels read in memory (nothing saved), boxes chosen by eye; mean sRGB, linear luminance as a share of the sky's (M). Processed JPEGs: bands, not exact values (I).

| Photograph | Sky | Wet road | Footway | Brick |
|---|---|---|---|---|
| A. "Low Pavement on a damp November morning", John Sutton, 21 Nov 2009, CC BY-SA 2.0 (https://commons.wikimedia.org/wiki/File:Low_Pavement_on_a_damp_November_morning_-_geograph.org.uk_-_1782266.jpg) | 255 (clipped) | setts 105 | flags with sky sheen 150; by shops 52 | red fronts, windows in: medians about 57 to 97 |
| B. "St Peter's Road, St Albans, in the rain", Bill Boaden, 28 Feb 2020, CC BY-SA 2.0 (https://commons.wikimedia.org/wiki/File:St_Peter%27s_Road,_St_Albans,_in_the_rain_geograph-6411694-by-Bill-Boaden.jpg) | 231 | along the street 170 to 186 (0.5 to 0.65 of the sky) | 123 to 127 (0.29) | red-brown garden wall 55/47/42; cream render 171 |
| C. "Fletcher's Terrace on a rainy morning", John Sutton, 16 Dec 2025, CC BY-SA 2.0 (https://commons.wikimedia.org/wiki/File:Fletcher%27s_Terrace_on_a_rainy_morning_-_geograph.org.uk_-_8213458.jpg) | 213 to 221 | 164/154/147 (0.53) | by the wall 104/99/89 | buff 156/123/93 |

The wet road seen along the street is the brightest thing below the sky, mirroring it; footways 100 to 150; brick 55 to 156 by colour and light. **The Hook sheet agrees on the ground:** its road 152 to 183 and wet flags 122/106/87 (R; unreal-look.json notes) lie inside these bands. An 18% grey lands near 118, X-Rite neutral 5 at 121 (M; MAFIA-WEAR-2026-10-28.md). No openly licensed 1985 to 1995 photograph was found (below).

## 5. Unreal's units

- Epic, "Using Physical Lighting Units" (https://dev.epicgames.com/documentation/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine): directional light in lux; sky light and emissive in cd/m²; auto exposure in EV100 (R).
- Engine source on this PC (UE_5.8) (R): r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange defaults to **0** (Engine/Source/Runtime/Engine/Private/SceneView.cpp line 202). When on, exposure limits are EV100 and the white point is 2^EV100 cd/m² (RenderUtils.h, EV100ToLuminance; lens attenuation 0.78, "1.0cd/m^2 becomes 1.0 at EV100"). When off, the limits are the white-point luminance itself (PostProcessEyeAdaptation.cpp, lines 661 to 668). Mid grey is 0.18 of the white point.
- So for a grey card to land at mid grey under E lux: EV100 = log2(E/π): 6,000 lux 10.9; 10,000 lux 11.6; 18,000 lux 12.5 (M).

## 6. Reference first

Mafia (R; studies/05-visuals.md, MAFIA-WEAR-2026-10-28.md): extended range on; day sun 7 to 15, sky 1.2 to 7 (real sun about 100,000 lux); day exposure compensation median +0.6, floor EV100 1; white balance 6,050 K. It too scales daylight down and lets exposure carry it: only ratios carry over. Its albedos were not read; Kingdom Come II's sun, exposure and albedos were not found. For albedo: none found; the real values above are the method.

## 7. The game now, in the same units

Derived from VignetteShot.cpp (ApplyCondition, the street's grade and wet writes), StreetMeshes.h (WetDarken), unreal-look.json, vignette-scene.json, quay-street.json, ps5-corner.json and the textures themselves (M):

| | Game | Real |
|---|---|---|
| Sun | 3.0 × 0.1 = 0.3 lux | no direct sun |
| Sky dome seen | sky photograph × 0.7 × 13: mean 4.2 cd/m² | 2,500 to 7,500 zenith |
| Horizontal light, open sky | about 14.8 lux (photograph integrated, 16° horizon clamp) | 6,000 to 18,000 lux |
| Exposure | pin 3.0 with the range setting off (the 29 October 02:08 verdict prints cvarExtendDefaultLuminanceRange=0): white point 3 cd/m², equal to EV100 1.58 | 10.9 to 12.5 |
| Road (asphalt), wet | 0.125 × 0.13 × 0.744 = **0.012** | 0.07 to 0.08 |
| Flags, wet | drawn picture 0.086 × 0.41 × 0.744 = **0.027** | 0.13 to 0.22 |
| Kerb, wet | 0.279 × 0.35 × 0.744 = 0.073 | as flags (I) |
| Red brick | scan × match × gain × house tint: **0.049** (sRGB 100/48/30); grey brick 0.052 | 0.10 to 0.20 |

Decals and the kit's dirt band darken further and are not counted.

Findings:
- **Light and exposure agree.** About 1/400 to 1/1,200 of real light, exposed about 10 stops brighter, as Mafia does; sun 2% of the light, right for overcast; an open grey card 0.65 stop above mid grey at pin 3 (log2(14.8/π) = 2.24 against 1.58). Not the fault.
- **The surfaces are:** road about 6 times too dark, flags 5 to 8, brick 2 to 4. The gains were tuned against frame pixels while the exposure moved (road 0.62, 0.22, 0.13: "darkness is what lets the reflections show", surface_gain_note_3_october), so they absorbed exposure.
- **The pin is not EV100 here:** 2 to 3 is log2(1.5) = 0.58 stop, not one. From the 28 October chart readings neutral 5 at pin 3 should read near 147, still above 110 to 135 (I; to be read). vignette-scene.json and DECISIONS (29 October 08:20) call it EV100 and one stop.
- **The road's film specular 0.115** is F0 0.009 (0.08 × Specular); water is 0.020, Specular 0.25 (M). It halves the sky's mirror, which the photographs show bright.
- Under the chart's light at pin 3 (its own curve, I): game flags about 33, brick 67 to 70, kerb 89, the road's diffuse part below the chart's black; at real albedo flags about 139, brick 121, road 90.

## Target values for the game

| Surface | Dry, linear | Wet, linear | Exposed photo, sRGB |
|---|---|---|---|
| Road, aged asphalt | 0.10 to 0.12 grey | 0.07 to 0.08 | 160 to 186 along the street (sky mirrored); 100 to 110 looking down |
| Flags, concrete | 0.20 to 0.35 | 0.13 to 0.22 | 100 to 150 |
| Red brick | luminance 0.10 to 0.20; colour about (0.26, 0.10, 0.06) | walls stay dry unless raining | 55 to 130 |
| Buff brick, render | UNVERIFIED | | buff about 156/123/93; cream render about 171 |
| 18% grey | 0.18 | | 117 to 121 |
| Sky | | | 213 to 255 |

Daylight: 6,000 to 18,000 lux, median about 11,000; rainy 6,000 to 8,000; EV100 11 to 12.8 (cameras 11.9 and 12.3).

## What it means for the work

1. Measure first, in the base-colour view (calibration check C6): road, flags, kerb, brick; expect about 0.012, 0.027, 0.07, 0.05.
2. Bring them into the real bands (two to eight times brighter); the camera stays.
3. The road's wet look from the water, not a black base colour: film specular toward water's 0.25; sky reflections bright, buildings' dark, as in photograph B.
4. Leave the light's scale; check its ratios (sun to sky; open grey card near mid grey).
5. Re-read neutral 5 at pin 3. Near 147 means the "one stop" was 0.58: a line for his page, the exposure being his ruling.
6. Then the street beside the Hook sheet, whose road and flags already sit in the real bands (I).

## Not read, or unconfirmed

Littlefair's overcast efficacy (search summary only; the lux figures rest on it); Krochmann's formula; CIE S 011 and CIE 144 road classes (Q0); BRE GN50's reflectance table (text not extractable) and BR 209; USGS and ECOSTRESS spectra of brick, asphalt and concrete (data not linked or not found); Engineering Toolbox and Decrolux tables (search summaries only); Twomey, Bohren and Mergenthaler 1986; where physicallybased.info's brick colour was measured; stock brick, render and kerb albedos; Epic's Auto Exposure page (engine source read instead). Photographs from 1985 to 1995: Geograph's search answered with a bot check (not passed) and Commons' search service refused further requests. The Hook sheet was not re-measured here; the chart was not read at pin 3; the game figures leave out decals, the kit's dirt and Lumen, and assume one emissive unit is 1 cd/m².

## Revised after review (29 October 2026, 09:10)

A fresh reviewer (WET-OVERCAST-VALUES-REVIEW-2026-10-29.md) passed this file with fixes; they stand here and win over the sections above where they differ.
1. The day's pin is now 4.000, one true stop darker than 2.000: the pin is plain luminance in this project (the run line's cvarExtendDefaultLuminanceRange=0), not EV100. Section 7's figures were worked at pin 3; redo them at 4. Item 5 of the work becomes: read neutral 5 at pin 4, expecting 110 to 135. The exposure is his ruling; no line for his page.
2. By day nothing overrides AutoExposureBias (VignetteShot.cpp sets it at night only), so the engine's default bias applies (+1 by the reviewer's reading). If so, an open grey card sits about 1.24 stops above mid grey, not 0.24, and "light and exposure agree" is unproven. Confirm the bias from a day run's own line before changing the light; then the chart reading decides.
3. Base colour is not measured albedo: wet albedo includes the water's own reflection (about 0.02), which the game's film specular already supplies, and dry albedo includes some specular. Wet base colour targets: road about 0.05 to 0.06, flags about 0.11 to 0.20. Add a lit check against the chart, not only the base-colour view.
4. Porous concrete flags and 1990 brick darkened by soot each need their own bands before they become targets (not yet found).

