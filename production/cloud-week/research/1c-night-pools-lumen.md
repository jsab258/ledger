# Night street lighting in Unreal 5 with Lumen: pools of light, darkness between (research note 1c, 8 October 2026)

**Summary line:** By number the 8 October night is no longer one orange wash; it is the opposite, with about 70% of the ground near black where real night streets sit only 3 to 5 stops from pool to gap, so the fix is a long-throw second light on each lamp plus a small sky fill, with the red clip cured in the grade and a softer pool core, for about 0.5 ms (a guess, to measure).

Marks: **[SHOWN]** read at its source, or measured by me on a file I reached. **[CLAIMED]** an earlier repository note's reading, not re-read. **[SS]** web search summary only, never evidence. **[I]** my inference or arithmetic.

## 1. The question

His ruling of 1 October: "pools of lamp light with darkness between, lit windows, not one orange wash." The near lamp's pool clipped red (his order of 11:10, 8 October: 2% of the flags or less). What do professionals do, what does our night get wrong, and what is the cheapest fix that a fresh reviewer, judging through the game's own camera and exposure, will pass?

**What I could reach.** The repository (audits, notes, code, specs, the probe verdict of build 69d0948). Poly Haven's API and four of its CC0 night-street photographs, which I measured. Almost nothing else: the proxy refused dev.epicgames.com, Wikipedia, blogs and press (403), and WebFetch fails on DNS. Every Epic and web claim below is therefore [SS] or [CLAIMED]. Section 7 lists what to read from the PC.

## 2. The professional method

**Real lamps and levels.**
- Low-pressure sodium (SOX): 35 W gives 4,550 lm; 55 W gives 7,800 lm; 90 W gives 13,600 lm [SS, Philips sheets 2010 to 2023]. SOX is near one colour (589 nm), nominal 1,700 to 1,800 K [CLAIMED, evening-light-1990]. High-pressure sodium (SON): 70 W about 5,600 lm; 150 W about 15,000 lm (13,500 minimum); about 2,000 K; colour rendering about 25 [SS].
- Period columns: estates of the 1970s to 1986 used 5 m columns with 35 W SOX and 6 m columns with 55 W [SS, streetlightonline.co.uk pages]. Spacing: not found. The 1989 code for minor roads, BS 5489-3, was current from 31 August 1989 to August 1992 [SS, BSI catalogue]; its figures were not reached.
- Later standards show the intent. EN 13201-2:2015 pedestrian classes: P4 average 5 lx, minimum 1 lx; P5 3 and 0.6; P6 2 and 0.4 [SS]. A real street is meant to be fairly even: average to minimum about 5:1, 2.3 stops. Earlier repo arithmetic: about 10 lx under a 35 W lamp, 0.5 lx midway, 4.3 stops [CLAIMED, aaa-street note 3].
- Sky: clear full moon 0.05 to 0.3 lx; a cloudy city night about 0.3 lx on one proxy measurement; cloudy city zenith 27 mcd/m2 against 4.3 for a clear full moon [SS, Bevy docs, Wikipedia table, Potsdam and Brno papers]. So skyglow is 30 to 100 times below a pool, 5 to 6.6 stops [I].
- **Real photographs, measured by me [SHOWN].** Four CC0 HDR photographs by Greg Zaal from Poly Haven (street_lamp, preller_drive, cobblestone_street_night, vignaioli_night; 2k, hashes match Poly Haven's). Method: decode the Radiance file, luminance 0.2126/0.7152/0.0722, weight by cos(latitude), ground = 10 to 80 degrees below the horizon (script kept in cloud scratch, not committed). In scene-linear light, pool-to-gap (95th over 10th percentile) is **3.0, 3.3, 4.9 and 5.2 stops** (99th over 10th: 3.6 to 6.8). The share of ground more than 4 stops under its own 95th percentile is **5%, 5%, 26% and 43%**. None is British sodium, and their white balance is unknown; they show how much darkness a camera sees in a lit street, not the lamp colour. The brightest 2% of ground has red to green 0.95 to 2.05, blue 0.17 to 0.78 of green.

**Physical units in Unreal.**
- Point, spot and rect lights take lumens or candela only with inverse-square falloff. Directional lights are lux; sky light and emissive are cd/m2. Beam width does not change total lumens [SS, Epic].
- A spot's lumens become candela through its cone: cd = lm / (2 pi (1 - cos outer half-angle)) [CLAIMED: the 8 October note read SpotLightComponent.cpp; its 465 cd for 750 lm at 42 degrees reproduces, I checked]. Ours: 500 lm at 46 degrees is 261 cd, 11.4 lx straight down from 4.78 m [I]. That is already the strength of a real 35 W lamp.

**Exposure.**
- Pin it, as we do. Min equal to Max switches adaptation off [SS, Epic API]. Epic: always set up Local Exposure with Lumen; the earlier note adds, keep its shadow lift low so gaps stay dark [CLAIMED, evening-light-1990]. Compensation on automatic exposure also lifts the sky; forums prefer lowering the sky light [SS].
- Units: Min/Max are cd/m2, or EV100 when the project's extended luminance range is on [SS]. **Our verdict prints that setting as 0, and our night pin as 0.4 [SHOWN, production/d1-probe/ue-vignette-verdict.txt]: the pin is a brightness in cd/m2, not EV100.** On the day scene the ladder says larger is darker (pin 0.3 gave mean luma 0.66, 3.0 gave 0.19) [SHOWN, vignette-scene.json]. Night 0.4, day 2.0: the night is metered 2.3 stops more sensitive than the day [SHOWN numbers, I].

**Sky light and moon.** At night the sky light is the gap's floor. Keep it at skyglow level, about 5 to 6 stops under a pool [I]. A real-time captured sky light photographs the sky meshes, atmosphere and height fog [CLAIMED, SKY-AND-HAZE note], so a very dark dome gives near-zero fill.

**Lumen at night.**
- Direct light from every local light is computed normally; Lumen's own cache keeps a limited number of lights per tile (ours: `r.LumenScene.DirectLighting.MaxLightsPerTile=8` [SHOWN, DefaultScalability.ini]). That limit shapes bounce, not the direct pool [I].
- Small bright emissive surfaces make noise; Epic says so in its emissive page [SS, German and Spanish versions]. Use real lights for strong sources, emissive for windows and lamp glass.
- Lumen reflections trace only below roughness 0.4 [CLAIMED, note 3, D1]. Our wet road is 0.06 to 0.15 [SHOWN, unreal-look.json]: inside.
- Final gather, short-range AO and screen-trace cvars: I could not confirm defaults for 5.8. See section 6.

**Light shape, size, profiles.** Attenuation radius should end where the light is below the sky floor: our 18 m [SHOWN]. Source radius sets highlight size on wet ground; small gives a streak [SS, UE 4.27 lighting basics]. A real lantern throws most light down and along the road, little above horizontal [CLAIMED, earlier note]. IES profiles are fast and in candela [CLAIMED, D11]. An IES file is plain text, so we can write our own by script: no licence question, and we need no outside library [I].

**Fog and halos.** Volumetric fog: 1 ms on PS4 High, 3 ms on a GTX 970 at Epic [SS, 4.27 docs]; a shadow-casting local light costs about three times as much in it; "Volumetric Scattering Intensity" 0 takes a light out [SS]. Local fog volumes are cheaper and have no volumetric shadows [SS]. Cheapest halo: bloom on the lamp glass [I].

**Windows.** Epic's City Sample is lit at night by sun, sky and emissive windows only, through Lumen [CLAIMED, D13; SS press]. Real lit windows run 6 cd/m2 (shop windows 50), 10 to 100 times the lit pavement [CLAIMED, 8 October glass note, Novak 2025]. Interior-mapped rooms (Spider-Man) [SS]. A few real rect lights only where a window spills onto the pavement [CLAIMED].

**Shadowed lights on an RDNA 2 card.** I found no per-light figure. Local-light virtual shadow maps are cheap when cached on Nanite or static geometry, costly otherwise [CLAIMED, D3; one forum case, 22 ms against 0.02 ms, itself [SS] in that note]. MegaLights is production-ready in 5.8, hardware ray tracing recommended [SS, release notes]; our ray-tracing scene cost 3.6 ms and is off [SHOWN, DefaultEngine.ini]. Not a cheap fit. Our night frame costs 10.2 to 10.7 ms against 8.1 to 9.1 by day at 1280x720 [SHOWN, H3 note, 3 October].

**How shipped games do it.** Thin. Cyberpunk: physically based lights, very dense light counts, capsule area lights (SIGGRAPH 2021) and a GDC 2022 talk, "Bringing Light to Night City" [SS, listings only; contents not reached]. Mafia: a deferred renderer with many dynamic lights; KCD2 night never goes fully black because its voxel GI bleeds [SS, press]. No reached talk gives pool numbers. Ours come from first principles and the photographs above.

## 3. What our night likely gets wrong, ranked

**Shown** (pictures and measurements; the tool is tools/measure_night_pools.py, run on production/previews/morning-night-*.jpg, JPEG, 1600 px):
- The bottom third (7 and 8 October frames): **68 to 73% of pixels under 16 of 255 in every channel**; the tool's near-black share (luminance under 0.005) is 0.72 to 0.80; median luminance 0.0000 to 0.0003; the foreground road 94 to 95% under 16. The bottom third's 95th percentile is 0.10 to 0.16; the pool box's is 0.36 to 0.56. The tool's "spread" reads 16 to 17 stops, an artefact: the 10th percentile is zero.
- The pool beside Mickey's: mean RGB (135 to 145, 61 to 67, 3 to 8); red 5% clipped in the morning frame, 0% in the packaged evening frame (my box, not the audit's).
- The sky: (15, 11, 7) morning, (33, 26, 20) evening. No halos at the lamp heads. Lit windows near cream.

**Ranked.**
1. **The gaps are too dark by 3 to 4 stops [I].** Our lamp is a cone that stops at 46 degrees: 11.4 lx under it, about 0.03 lx at 10 m (glow 40 lm, 3.2 cd, unshadowed) plus sky 0.35 x 0.15 = 0.0525 [SHOWN values]. That is about 8.8 stops lamp-only against 3 to 5 in photographs and standards. Earlier fixes cut pool lumens (1,800, 1,100, 750, 500) and moved the camera a stop; none lifted the gap.
2. **The red clips first, by design.** Lamp (1.0, 0.25, 0.0): red 4 times green. Red hits 250 at about luminance 0.38; a neutral light clips near 1.0, so clip comes about 1.4 stops early [I]. The pool measures red to green about 5:1 in linear, blue zero; photographs of lit streets gave 1 to 2 [SHOWN, mine]. A pure spectral colour sits outside sRGB, so the chosen clip decides how red it looks [I].
3. **The pool core is flat and hot.** Inner cone 22 degrees gives a plateau about 2 m wide, then a cone edge [SHOWN values, I].
4. **Fill and sky glow are missing.** Dark dome, weak sky light, fog at (0.03, 0.02, 0.012) [SHOWN]. No gradient to separate roofs [SHOWN picture].
5. **Cost risk, not look.** One shadowed spot per lamp, shadowed room rects and spill rects per shop, glass catch [SHOWN, VignetteShot.cpp]. Worst 99th-percentile frame 46.8 ms on 8 October, blamed on the glass catch [SHOWN, FOR-JAFAR].
6. **Units are mixed.** Lamps in lumens; windows, sky and lamp glass in unitless gains. So every level was tuned by eye and the relative levels cannot be reasoned about [SHOWN code, I].

## 4. The fix that fits LEDGER, cheapest first

Do each, shoot the hook night frame, measure (section 5), keep only what helps. Two tries each, then research.

1. **Split test, 0.5 h.** `-NightTest=sky`, `=fog`, `=both` already exist [SHOWN]. Add a Lighting Only frame. Read scene-linear values (Pixel Inspector) at three spots: pool centre, road midway between lamps 1 and 2, facade at eaves. Pass for the later steps: pool to midway 4 to 5 stops in scene light.
2. **Grade for the clip, minutes.** Night highlights saturation down 20 to 30% in the post-process volume (Color Grading, Highlights, Saturation) [I; name to check]. Target: clipped red on the flags 2% or less *and* green at 250 or more under 0.5%.
3. **Sky floor.** Night sky light gain 0.15 to 0.30 (one stop) [I, to try]; fog colour and dome slightly warmer and brighter so the roofline separates by 1.5 stops. Keep the exposure pin at 0.4 and the bias at 0.
4. **Long-throw skirt, one light per lamp.** Unshadowed spot, straight down, **800 lm, inner 45, outer 80 degrees**, same colour, source radius 5 to 10 cm. Drop the pool spot 500 to 350 lm; make the cone 15 and 55. Arithmetic [I]: peak about 12.5 lx (now 11.4); 10 m along about 0.24 lx; 5.7 stops before sky and bounce; assumes linear falloff between the cones. Nothing is above the lamp's own height, so the upper storeys stay dark. Check leak into shop rooms; if it leaks, put it on a lighting channel that excludes the rooms.
5. **Lamp colour try.** (1.0, 0.40, 0.03), red to green 2.5, one number [I]. Reviewer judges against photographs from the PC; period accuracy against yellower looks is his call.
6. **Own IES file** (script): peak 60 to 70 degrees from straight down, about 60% at nadir, 5% at 85, nothing above 90 [I, design intent]. Replaces steps 4 and 5's light shape with one asset.
7. **Halo.** Bloom on the lamp glass first. Volumetric fog only if the night frame stays under about +0.5 ms; scattering from the skirt only, no volumetric shadows [I].
8. **Later, one day:** audit every night level into units (lumens, cd/m2) so exposure is one physical number.

**Cost [I, all to measure with ProfileGPU]:** four more unshadowed spots, 0.1 to 0.4 ms at 3440x1440 upscaled; grade and fill, nothing; the halo 0.5 ms or more. Keep shadowed local lights in view at or under 8 [I].

## 5. Verify with numbers from the game's own camera

Same camera, same pin, packaged build. Use tools/measure_night_pools.py after one repair: print the share under 16 of 255 and the median, and stop quoting the p95-over-p10 spread (zero floor). Then a fresh reviewer.

| Test | Pass | Now |
|---|---|---|
| Clipped red, flags under the near lamp (pool_clip.py boxes) | 2% or less | 0.5% (audit) |
| Green 250 or more, same boxes | under 0.5% | not measured |
| Pool to gap: median luminance of a box on the flags under lamp 1 over a box on the road midway between lamps 1 and 2 | 3.5 to 6.5 stops (photographs, 99th over 10th: 3.6 to 6.8) | 7 to 8 (my boxes) |
| Bottom third, share under 16 of 255 | 45% or less (photographs: 5 to 43% four stops under the 95th) | 68 to 73% |
| Road gap median | 10 to 30 of 255, not black | 0 to 4 |
| Pool colour: brightest 2% of flags, red to green (linear) | 1.5 to 3 | about 5 (pool box) |
| Lit windows: median luminance over the pool box | 2 stops or more; blue at 0.35 of red or more | to measure |
| Sky just above the roofs over the roof tops | 1.5 stops or more | not measured |
| Night GPU, hook camera, packaged | at most day plus 1.0 ms; worst 99th percentile under 33 ms | 46.8 ms |

The thresholds from photographs are [SHOWN] as to the photographs, [I] as to the display; the tonemapper's toe makes display spreads larger than scene spreads.

## 6. To check on the PC

- `SpotLightComponent.cpp`, `ComputeLightBrightness`: the cone formula; the OuterConeAngle limit (I recall 80 degrees; unverified) and the falloff between inner and outer (arithmetic in step 4 assumes linear).
- `PostProcessEyeAdaptation.cpp`, `EV100ToLuminance`: what 0.4 means in EV100 (about plus 1.7 by the 12.5 constant; I recall a 1.2 factor in Epic's own, unverified).
- Defaults in 5.8: `r.LumenScene.DirectLighting.MaxLightsPerTile`, `r.Lumen.ScreenProbeGather.ShortRangeAO.*`, `r.Lumen.ScreenProbeGather.MaxRayIntensity` (I could not confirm it exists), `r.Lumen.Reflections.MaxRoughnessToTrace`, post-process Final Gather Quality, Lumen Scene Lighting Quality, Lumen Scene View Distance.
- `r.MinScreenRadiusForLights` (0.03 on forums [SS]): far lamps might drop out.
- Lamp spots: `bUseInverseSquaredFalloff` on; Specular Scale; Min Roughness; lighting channels.
- The height-fog component's volumetric flag (the verdict says `r.VolumetricFog=1` only as the system switch).
- `r.MegaLights` name: the verdict prints `cvarMegaLights=absent`, so the name differs in 5.8.
- Post-process Colour Grading highlights saturation's exact property (`ColorSaturationHighlights`).
- A stat that nothing in the repo has: ProfileGPU, `r.Shadow.Virtual.Stats 1`, at night, day against night.

## 7. Sources

Reached: [SHOWN]. **Repo files** read 8 October 2026: GATE-NIGHT.md, pool_clip.py, SUMMARY-2026-09-29.md (evening light), NIGHT-2026-10-08.md, 3-LIGHT-AND-GRADE.md, SKY-AND-HAZE-2026-10-02.md, H4a-visual-areas.md, H3-performance.md, measure_night_pools.py, unreal-look.json, vignette-scene.json, DefaultEngine.ini, DefaultScalability.ini, VignetteShot.cpp, production/d1-probe/ue-vignette-verdict.txt (build 69d0948, 8 Oct), FOR-JAFAR.md, the night previews. **Poly Haven**, reached 8 Oct 2026, CC0: https://api.polyhaven.com/files/ and /info/ for the four assets; https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/{street_lamp,preller_drive,cobblestone_street_night,vignaioli_night}_2k.hdr (captured 2016 to 2023). Not shipped; reference only.

Not reached, [SS] only (search summaries 8 Oct 2026, dates as the summaries gave): Epic, Using Physical Lighting Units; Auto Exposure; EV100ToLuminance and LuminanceToEV100 API pages; Volumetric Fog; Local Fog Volumes; MegaLights and the 5.8 release notes; Virtual Shadow Maps; Emissive Material Input (dev.epicgames.com/documentation/en-us/unreal-engine/...). UE-218856 and UE-221111 (issues.unrealengine.com). Philips and Signify SOX and SON data sheets (assets.lighting.philips.com, 2010 to 2024). EN 13201-2:2015 table via performanceinlighting.com. BSI catalogue entry, BS 5489-3:1989 (knowledge.bsigroup.com). streetlightonline.co.uk Survivors pages (undated). Bevy light_consts docs; Wikipedia orders of magnitude (illuminance); Potsdam sky brightness (arxiv.org/abs/1307.2038); Brno overcast measurement (amper.ped.muni.cz). GDC Vault listing 1027959 (Cyberpunk 2077, GDC 2022); SIGGRAPH 2021 "Area Light Sources in Cyberpunk 2077". Automaton Media on Spider-Man interiors (2023). Press on Mafia: Definitive Edition and KCD2.

**To read from the PC or once the network opens:** the Epic pages above; Lagarde and de Rousiers, "Moving Frostbite to Physically Based Rendering 3.0" (2014), section 4.3, light units; the Cyberpunk talks; BS 5489-3:1989 from a library; Philips originals; engine files `SpotLightComponent.cpp`, `PostProcessEyeAdaptation.cpp`, `LumenSceneDirectLighting.cpp`.
