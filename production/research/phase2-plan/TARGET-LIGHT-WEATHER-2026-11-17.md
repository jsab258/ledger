Method researched: WET-OVERCAST-VALUES-2026-10-29.md

# Target: light by real values and weather life (17 Nov 2026)

Waiting item 7 of the order of 16 Nov, section 3. What the street's light and weather must read and measure; not the build. Tags: M measured, R read at the source, I inferred, UNVERIFIED not confirmed. "Read 17 Nov" means re-read today. Project files carry their own dates.

**Questions.** 1) Real values for a wet overcast street by day and at dusk. 2) Sodium and mercury lamps of 1990 Britain. 3) What each weather state changes, with the studies' numbers. 4) What exists and what is missing. 5) The reviewer's checks.

**Reference first.** Mafia: no running weather; each checkpoint names a time-of-day preset, 103 presets; one global wetness (0 default) drives roughness to 0.1 flat and 0.2 on slopes; puddles are 232 decals in Palermo (studies/05-visuals.md, 11-systems.md). Mafia's lamp: key spot 1.5 cd, 20 m, 80 deg, 4500 K, plus a bulb point 0.45 cd reaching 1 m; a second lamp 4 cd, 15 m, 2400 K; night exposure compensation +2.75 to +4.0; night fog 0.035 to 0.05. Kingdom Come II: 31 weather profiles a level, 15 weighted (sum 5.1), rain chance 0.3 to 1.0, rain-capable in about 35% of weighted draws; weather filters 2,289 scheduler links (1,399 sun-only, 890 rain-only); rain is a screen layer to 150 m (40 m at low); town lights reach a median 4.3 m, warm orange; no wet-street material among 7,572 (studies/05-visuals.md, 01-npc-life.md, 11-systems.md, read 17 Nov). Neither game gives an albedo: for values, none found, the method is measured real data.

## 1. Real values, day and dusk

| Quantity | Value | Source |
|---|---|---|
| Overcast light, noon, late Oct, 51.5 N | 6,000 to 18,000 lux, median about 11,000; rainy 6,000 to 8,000 (M from satellite irradiance; the lux step rests on an efficacy seen only in a search summary: UNVERIFIED) | street-wear/WET-OVERCAST-VALUES-2026-10-29.md |
| EV100 | 11 to 12.8; two real rainy-street exposures 11.9 and 12.3 | same |
| Sky luminance (CIE overcast) | zenith 2,500 to 7,500 cd/m2, horizon a third | same |
| Aged asphalt | dry 0.10 to 0.12, wet 0.07 to 0.08; wet base colour 0.05 to 0.06 | same, revised section |
| Concrete flags | dry 0.20 to 0.35, wet 0.13 to 0.22; wet base colour 0.11 to 0.20 | same; FLAGS-BRICK-BANDS-2026-10-29.md |
| Red brick | luminance 0.10 to 0.20; walls stay dry unless raining | same |
| How much wet reads darker | rough stone keeps 0.63 to 0.68 of dry between 0.12 and 0.35; porous about half; under 0.05 hardly darkens (Lekner and Dorf 1988, computed) | WET-OVERCAST-VALUES §2 |
| Photographs, 8-bit | wet road along the street 170 to 186 (0.5 to 0.65 of the sky); footways 100 to 150; brick 55 to 130; 18% grey 117 to 121 | same §4 (three Geograph photographs, 2009 to 2025) |
| Lagarde's game rule | diffuse x lerp(1, 0.3, wetness); gloss x up to 2.5; standing water specular 0.02 | https://seblagarde.wordpress.com/2013/01/03/water-drop-2b-dynamic-rain-and-its-effects/ (read 17 Nov) |
| Dusk | No measured British dusk street value reached. Dark limit of civil twilight 3.4 lx (clear sky); very dark overcast 100 lx | https://en.wikipedia.org/wiki/Lux (read 17 Nov; tertiary) |

Dusk sky luminance, dusk EV100 and a lit-street lux: UNVERIFIED. The summary's day EV100 11 to 12 and lamp-lit night 2 to 3 are the helper's own starting points ("mine"; evening-light-1990/SUMMARY-2026-09-29.md). The sky is "fully dark about 20:00" in autumn at 53 to 54 N, and 1990 summer time ending 28 Oct: both from memory, UNVERIFIED. A cloudy town sky glows dull orange from the lamps, up to about ten times brighter near cities (Kyba, via Live Science 2015, secondary).

## 2. Lamps of 1990 Britain

- **Low-pressure sodium (SOX):** virtually monochromatic, average 589.3 nm; warm-up a dim red or pink glow, bright yellow "within a few minutes"; above 100 and up to 206 lm/W; 35, 55, 90, 135, 180 W; no colour temperature given (https://en.wikipedia.org/wiki/Sodium-vapor_lamp, read 17 Nov). Chromaticity (0.569, 0.430), linear about (1.0, 0.25, 0.0), already in unreal-look.json (lantern_linear_rgb). 35 W about 4,550 lm and nominal 1,700 to 1,800 K: a maker listing and the summary, not read at source: UNVERIFIED. Red and black cars read alike (Wikipedia caption).
- **Mercury (MBF):** 35 to 55 lm/W; colour rendering 15 to 25 uncoated, 50 to 60 phosphor-coated; uncoated "distinctly greenish"; wattages 50 to 1,000 W (https://en.wikipedia.org/wiki/Mercury-vapor_lamp, read 17 Nov). Colour temperature: not given: UNVERIFIED. Which lamp Quay Street's 1990 council used: UNVERIFIED (our canon sets SOX, RULINGS 22 Oct).
- **Spacing and pool:** no primary source reached. BS 5489 part 2 (1987) and part 3 (1989) hold the tables; the 1992 edition lists spacing at 10 and 12 m mounting heights (search listing only: UNVERIFIED). Wikipedia's Street light gives no figure for the period. The project's own: four columns, 10 m staggered, 20 m a side, light 4.83 m up, 35 W lantern, pool spot 22 to 46 deg (scene file, look file). Real spacing for 5 m columns in a subsidiary street: UNVERIFIED; judgement only.
- **Games' scale, not physical:** Mafia's 1.5 cd and 20 m; ours 40 lm bulb and 167 lm pool against a real 4,550 lm. Only the ratio lamp to ambient carries over (Study 5).

## 3. What each weather state changes

States per the 5 Oct and 7 Oct rulings: dry overcast, drizzle, rain; day and night now, four or five states with transitions later; no moving sun.

| Item | Numbers found | Source |
|---|---|---|
| Wetness ramp | Lagarde: wet-level speed up/down light 0.6/0.2, moderate 0.75/0.2, heavy 1.0/0.2; puddle fill 0.1/0.05, 0.3/0.05, 0.7/0.05 (time unit not stated; drying is 3 to 12 times slower than wetting). Rain intensity 0.33, 0.66, 1.0; ripple layers at 0.25, 0.5, 0.75; puddle margin 0.4 | Lagarde page, read 17 Nov |
| Old prototype ramps | rain 0.08/s; wetness up 0.25/s, down 0.012/s (about 83 s to dry); days roll 55% dry, 30% drizzle (0.35), 15% rain (0.9). Unity code, an old build: whether it still governs anything: UNVERIFIED. No real-world drying time was found (UNVERIFIED) | ledger/Assets/Scripts/Game/Weather.cs |
| Puddles | Mafia decals with height, roughness, occlusion; ours: set aside 8 Oct, standing water waits on the corner list; roughness 0.02, flat normal, opaque core, in kerb channel and dips; Lumen weak at roughness 0.2 to 0.39 | 05-visuals.md; aaa-street/PUDDLES-2026-10-02.md; SKILL §5 |
| Sound | Rain bed mix -33.5 LUFS against -36.5 day and -39.5 night; rain on pavement, awning, gutter -37 day, -42 night, -47 rain, near; wet step as splash layer over the dry step; three rain layers, one intensity, drizzle by turning them down; one rain parameter fades rain layers, road hiss and gulls | 08-sound.md (28 Oct); cloud-week/sound/NOTES.md |
| Who is out | KCD2: weather filters links (above); a townswoman sits on a bench in sun, indoors in rain. Mafia: none. Own proposal: rain halves spawned voices and activity (I, Study 8). Adopt: weighted profiles feeding routines (Study 11). Umbrellas, hurrying, doorway sheltering: no number in any study; UNVERIFIED | 01-npc-life.md; 11-systems.md |
| Wear | Salt bloom keeps 0.9 of its brightness in drizzle, 0.6 only in heavy rain with running water; rust runs after rain | cloud-week/targets/wear/TARGET.md |

## 4. Exists and missing

**Exists** (unreal-look.json, vignette-scene.json): conditions overcast_day (wetness 0.85, sky 0.70, fog 0.004, exposure pin 4.000 plain luminance, one stop down, never brightened) and wet_night (wetness 0.90, fog 0.022, max opacity 0.45, lanterns and windows on); ground coat M_LedgerGround, wet_darken 0.57, water level 0.85, road water on 53%; film specular 0.25; lantern 40 lm, bulb 1 m, pool 167 lm, cone 46 deg, light 4.83 m; night fill 0.4 lux warm; night pin 0.4; the weathering skill and its checks; rain sounds and three rain layers.

**Missing:** a weather state with ramps in the Unreal game (every condition is fixed wet; the Unity Weather.cs is not the game); drizzle and rain as separate states; drying look (damp, dark patches under eaves first: I); standing water in dips; rain streaks and ripples in Unreal; a dusk state (no values, no preset); lamps coming on with warm-up; rain-driven spawn thinning, umbrellas, doorway shelter; sound by state. Unmeasured: C4 (pool at least 4x the gap), the 24-patch chart error, chrome ball.

## 5. Checks and views

- Chart read in the open road before any change: neutral 5 at 110 to 135 by day (tools/chart_read.py). Surface boxes in band, base and lit (surface_values.py). Exposure and camera untouched.
- Each state in the three morning views plus dusk, beside the last good picture, the Hook sheet and KCD2 frames; the road's three regions within 12 levels (wet_ground_check.py); no sky mirrored across the whole road.
- Night: nearest pool's clipped red 2% or less (pool_clip.py); pools against gaps in stops (measure_night_pools.py); darkness between pools; near-black share reported, not failed.
- Ramps: logged wetness against time for wetting and drying; drying slower than wetting; no pop at a state change (frame-to-frame luminance step).
- Sound: bed mixes within 1.5 LU; rain parameter fades layers; one fresh reviewer per view; packaged walk by the AI tester; nothing passes in the editor.
- Sunshine, shadows from a sun, alcohol, gambling or children anywhere fail it.

## Open questions

1. Real 1990 lamp type and spacing for the street: judgement unless a dated photograph is found.
2. The drying time of wet stone: a real measure is needed, or the look is set by eye against photographs.
3. Dusk values: one measured source or a camera EXIF series (as the day's two photographs gave).

## Sources read 17 Nov 2026

The skill, the furniture target, Studies 1, 5, 8 (rows), 11 (rows), RULINGS look section, WET-OVERCAST-VALUES, PUDDLES, SODIUM-IN-RGB-READING (3 Nov), evening-light-1990 summary, unreal-look.json, vignette-scene.json, Weather.cs; the three Wikipedia pages and Lagarde's page above (through the fetch tool's reader).

## Unreached

BS 5489 text (BSI paywall; listing only); any primary 1990 council lamp record; mercury colour temperature; a measured dusk street; Littlefair's efficacy at source; period photographs (Geograph refused automation earlier); any figure for people's umbrella, hurry or shelter behaviour; Wikipedia's Street light, last 44,749 characters.
