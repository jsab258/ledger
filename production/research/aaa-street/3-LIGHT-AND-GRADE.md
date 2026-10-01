<!-- Research note 3 of 5 for production/research/aaa-street (1 October 2026). Written by a separate research helper given the problem; checked by the research session (see the last section). [D n] = documented in source n; [I] = inference or arithmetic. -->

# Damp overcast day and sodium night in UE 5.8, and what they cost on an RX 6700

1 October 2026. Research helper, about 30 minutes, read only. Marks: **[D n]** means documented in source n; **[I]** means my own inference or arithmetic. Most third-party sites were blocked by the egress proxy (TechPowerUp, TechSpot, Tom's Hardware, ComputerBase, 80.lv, gamegpu, GPUOpen, the Unreal forums and the Unreal blog), and the web-search budget ran out. So Epic's 5.8 documentation and Wikipedia were read in full. All benchmarks are from search summaries only. This note does not repeat evening-light-1990, photoreal-on-a-budget, shop-glass-reflections or 1990-on-film-stock.

## The main finding

The experiment that switched on every feature changed only 2.4% of pixels at 2.6 times the cost. Professional practice explains this: the look comes from **light values, exposure, sky brightness, wet materials and grading**, not from feature switches [I]. Epic's own night city in City Sample is lit by "only Directional Light, Sky Light, and Emissive Materials" [D13].

At night, inverse-square falloff gives pools of light by itself. A 35 W SOX lamp gives 4,550 lm (earlier note), which is about 362 cd if it spread evenly [I]. From a 6 m column:

- directly beneath, about 10 lux;
- 15 m along the road (half a 30 m spacing), about 0.5 lux;
- so roughly 20:1, or 4.3 stops between the pool and the gap [I].

British subsidiary-road standards give averages of 2 to 15 lux [D21]. **If the frame shows "one flat orange", something is filling the gaps.** The likely causes are the sky light, a tinted directional "moon", fog in-scattering, lights without inverse-square falloff or with very large radii, and auto or local exposure lifting the darks [I]. In our night frame the walls are evenly lit along the whole street, and a green jumper is still green, which means the main source is broad-spectrum fill, not the lamps [I].

**Check first [I]:** use the Lighting Only view. Turn the sky light, then the directional light, then the fog off one at a time. Confirm every lamp has inverse-square falloff, a lumen value and a radius of about 20 to 25 m. Set exposure to Manual.

## Overcast day

- **Sky source.** An HDRI sky lighting a single sky light is "the most common technique used in linear games for performance and memory reasons". It gives soft shadows, bounce and colour in one setup [D17]. Sky Atmosphere with Mie scattering raised above 1 (up to about 5) also gives soft overcast light [D17]. The cost of volumetric clouds is not documented [D14 area; Volumetric Cloud page has no figures].
  - Recommendation [I]: for a fixed overcast state, use an **unclipped overcast HDRI on a distant dome**, with intensity in cd/m² [D12]. Keep Sky Atmosphere for dusk only.
  - Do not use the HDRI Backdrop's ground projection: it stretches and shows parallax once the camera leaves its projection centre [D12].
- **Exposure.**
  - Heavy overcast is EV100 12 (ANSI tables) [D15].
  - "Overcast day" is 1,000 lux [D16], which is about EV100 9 at mid-grey [I].
  - So use Manual metering, or a range no wider than ±0.5 EV, at **EV100 10 to 12** [I]. Manual mode applies "a single, fixed exposure" [D6].
  - Epic: "Local exposure should always be set up when using Lumen GI", with contrast scales usually 0.6 to 1 [D6].
- **The sky's brightness decides everything.**
  - On a CIE overcast sky, the zenith is about three times as bright as the horizon (earlier note).
  - From a narrow street, the visible band of sky sits about 2 to 3 stops above mid-grey. It should look near-white but graded from horizon to zenith, never one flat white [I].
  - The street is lit from above, so it reads darkest under eaves and cars. Lumen's final gather gives this sky occlusion [D13].
  - Today's flat day suggests the fill is too even and the sky band has no tonal gradient [I].
- **Soft shadows.**
  - Keep the directional light faint (an overcast tip: about 7,200 K at low intensity) [D17], with a large source angle [I].
  - Virtual shadow maps give "realistic soft penumbra and contact hardening" [D13].
  - To restore shape, add fill lights (earlier note), not contrast.
- **Depth.** Use low-density exponential height fog with Start Distance at about 10 to 20 m, so that distant roofs separate from the street [I]. It costs about the same as two constant fog layers [D14]. Aerial perspective barely matters over a 42 m street [I].
- **Wetness.** This is the professional method: Lagarde's physically based wet surfaces (2013), used in Remember Me.
  - Porous materials darken more, and roughness falls towards that of water [D18].
  - Puddles fill the lowest points first, driven by height [D18].
  - In UE the usual approach is a global Material Parameter Collection for wetness, read by every master material [D19]. Puddles are vertex-painted with ripples [D19].
  - **Values to start from [I]:**
    - brick and asphalt: base colour × 0.5 to 0.7, roughness about 0.15 to 0.35 (damp, not flooded);
    - paint, metal and glass: hardly darkened;
    - puddles: roughness 0.02 to 0.05 with a flat normal;
    - kerb channels and dips: DBuffer decals, which can set roughness.
  - A damp day needs no rain particles. If rain is wanted, GPU Niagara rain near the camera costs very little, but I could not find a measured figure [I].
- **Reflections.**
  - Lumen traces reflection rays only below roughness 0.4 [D1].
  - Software Lumen traces the screen first, then distance fields and the surface cache. Only hardware ray tracing gives mirror-sharp reflections [D2].
  - Damp asphalt blurs reflections anyway, so **software Lumen is enough** [I]. Screen-space reflections save about 1 ms (Series S) [D1], but lose anything off-screen or at the screen's edge [I].

## Sodium night

- **Lights.**
  - Use spot lights, or point lights with an IES profile, in lumens or candela with inverse-square falloff [D5].
  - IES profiles are "very fast" and come in candela [D11]. Use a cut-off street-lantern profile [I].
  - The colour and colour-loss method is in the earlier note.
- **Shadows.** Our street has only about 3 to 5 lamps, so all of them can cast shadows [I]. Shadows from local lights are cheap only with Nanite geometry and cached static pages [D3]. One forum case without Nanite measured 22 ms against 0.02 ms [D22, search summary]. MegaLights is not needed at this light count. It can use virtual shadow maps per light, and its cost is constant but noisy [D10].
- **Exposure.**
  - A mid-grey surface under 15 lux equals EV100 of about 2.8 [I].
  - For a documentary night, fix exposure at **EV100 3 to 4**: pools a little under mid-grey, gaps near black [I]. This is darker than the earlier note's "2 to 3", so measure it.
  - The ANSI value for "night street scenes and window displays" (EV 7 to 8) describes bright city centres, not a sodium high street [D15, I].
  - Keep local exposure's shadow lift near none [I].
- **Night ambient.** Clouded skyglow should stay well under 1 lux, about a twentieth to a fiftieth of a pool [I].
- **Halos.**
  - Volumetric fog costs 1 ms on PS4 at High and 3 ms on a GTX 970 at Epic [D4].
  - A light that casts shadows costs about three times as much in the fog [D4].
  - Volumetric fog ignores IES profiles [D4].
  - **Cheapest option [I]:** volumetric fog only at night and at low density, with scattering from the nearest 2 to 4 lamps and no volumetric shadows. Alternatively, a glow card on each lamp head plus restrained bloom.
- **Windows.**
  - Shops: emissive at about 4,000 K (fluorescent), plus one rect light per lit shop window aimed at the pavement.
  - Houses: warm tungsten behind curtains, about 2,700 K, emissive only [I].
  - City Sample lights its night city with emissives through hardware Lumen [D13], which we cannot afford.
- **Wet-road streaks.** The long streaks under each lamp come mostly from each light's direct specular on a road of roughness 0.15 to 0.35 at grazing angles, not from the reflection pass. Keep Specular Scale at 1 and source radius at 0.1 to 0.2 m [I].

## Photographic look

- **Tonemapper.** The filmic defaults (Slope 0.88, Toe 0.55, Shoulder 0.26, Black Clip 0, White Clip 0.04) "match ACES". Epic advises grading with the Color Grading controls rather than a LUT, so the result is consistent on every display [D7].
- **LUTs.** The workflow: take a screenshot after tonemapping, grade it in Resolve, export a .cube file and apply it to the neutral LUT [D23]. A LUT is low dynamic range and applied after tonemapping, so set exposure and white balance first [I].
- **Grain.** UE 5.8 film grain has separate shadow, midtone and highlight intensities, a texel size and a texture [D8]. The period stock is in the earlier note.
- **What sells realism in UE5 shooters.**
  - Bodycam: deliberately degrading the image while overloading detail [D20].
  - Unrecord: muted, naturalistic light and the lens [D20].
- **Matching a reference photograph [I], in this order:**
  1. Mid-grey (put a grey card or ColorChecker prop in the scene and check it in Lighting Only).
  2. White balance: daylight about 6,500 K by day; keep daylight balance at night so the sodium stays deeply orange.
  3. Contrast.
  4. Saturation.
  5. Last: grain, vignette (slight) and halation; chromatic aberration and lens flares nearly off.

## Cost on the RX 6700

| Item | Figure | Source |
|---|---|---|
| Our everything-on test | 9 → 24 ms at 720p | brief |
| Hardware Lumen, measured on this PC | 3.6 ms | shop-glass note |
| RX 6700 compared with PS5 | about the same as the PS5's GPU (36 CUs, RDNA2) | [D24, search summary] |
| Lumen "High" | 60 fps on consoles; 1080p internal | [D1] |
| Lumen "Epic" | 30 fps; each level down costs about half | [D1] |
| Software Lumen, RX 6700 XT class, 1080p | 3 to 6 ms; hardware 10 to 14 ms | [D27, low reliability] |
| TSR | about 1.5 ms effective on PS5 (Fortnite); 0.79 → 0.43 ms at 100 → 50% | [D9] |
| TSR on RDNA | has fp16 paths for RDNA | [D9] |
| FSR 4 on RDNA2 | only unofficially (INT8 through OptiScaler); about 8% slower than FSR 3.1 | [D26, search summary] |
| UE 5.6 compared with 5.4 | RX 6700 XT +10 to 25% | [D25, search summary] |
| Shipped games, RX 6700 XT | Stalker 2 needs FSR to hold 60 fps at 1080p Epic; Hellblade 2 is under 60 at native 1080p High; KCD2 (CryEngine voxel GI, no ray tracing) runs above 60 at 1440p Medium | [D25, search summaries] |

**Settings for 60 fps [I]:**

- software Lumen at High;
- virtual shadow maps on Nanite geometry with caching;
- no hardware ray tracing;
- volumetric fog at night only;
- contact shadows on characters only;
- TSR or FSR 3.1 at 58 to 67% screen percentage.

What brought KCD2 to the bar was art, values and grading, not ray tracing [I].

## Sources

Epic documents are the UE 5.8 docs, undated, accessed 1 October 2026, read in full.
1. Lumen Performance Guide: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine
2. Lumen Technical Details: …/lumen-technical-details-in-unreal-engine
3. Virtual Shadow Maps: …/virtual-shadow-maps-in-unreal-engine
4. Volumetric Fog: …/volumetric-fog-in-unreal-engine
5. Physical Lighting Units: …/using-physical-lighting-units-in-unreal-engine
6. Auto Exposure: …/auto-exposure-in-unreal-engine
7. Color Grading and the Filmic Tonemapper: …/color-grading-and-the-filmic-tonemapper-in-unreal-engine
8. Post Process Effects: …/post-process-effects-in-unreal-engine
9. Temporal Super Resolution: …/temporal-super-resolution-in-unreal-engine
10. MegaLights: …/megalights-in-unreal-engine
11. IES Light Profiles: …/using-ies-light-profiles-in-unreal-engine
12. HDRI Backdrop: …/hdri-backdrop-visualization-tool-in-unreal-engine
13. City Sample: …/city-sample-project-unreal-engine-demonstration
14. Exponential Height Fog (also the Volumetric Cloud properties page): …/exponential-height-fog-in-unreal-engine

Other sources:

15. Wikipedia, "Exposure value", Table 2 (ANSI PH2.7-1973 and PH2.7-1986). Read in full.
16. Wikipedia, "Lux". Read in full.
17. World of Level Design, the UE5 HDRI guide and the UE4 overcast Sky Atmosphere guide, undated. Search summary only.
18. S. Lagarde, "Water drop 3a/3b: physically based wet surfaces", March and April 2013, seblagarde.wordpress.com. Search summary only.
19. 80.lv: Tony Kelly, "Rainy Japanese Environment in UE5"; Maarten Hof, "Rainy Neon Streets" (UE 5.1); both undated. Search summary only.
20. 80.lv, Reissad Studio, "Developing a Game With Realistic Graphics in Unreal Engine" (Bodycam), about 2024; Creative Bloq on Unrecord, 2023. Search summary only.
21. BS 5489-3:1992 listing (thenbs.com) and summaries of later editions. Search summary only.
22. Epic forums, "Virtual Shadow and Local Lights Performance", about 2022. Search summary only.
23. Unreal forums and versluis.com (October 2025) on the LUT and OCIO workflow. Search summary only.
24. Digital Foundry, "The PS5 GPU in PC Form? Radeon RX 6700 In-Depth", about 2023, via a NeoGAF thread. Search summary only.
25. TechPowerUp news on UE 5.6 against 5.4 (2025); TechSpot's Stalker 2 benchmark (November 2024); Hellblade 2 benchmarks (May 2024); DF and TechSpot on KCD2 (February 2025). Search summaries only.
26. TweakTown and PC Gamer on FSR 4 on RX 6000 through OptiScaler, 2025. Search summary only.
27. bitsoulhosting.com and strayspark.studio blogs, 2026, unclear authorship. Search summary only; low reliability.

## What I could not verify

- **All third-party benchmarks.** I could not open any of them, so none is measured on an RX 6700 (non-XT, about 10% slower than the XT [I]). The software and hardware Lumen figures in milliseconds come from low-reliability blogs.
- **Cost of the remaining features.** No source gave the cost of volumetric clouds, rain particles or convolution bloom.
- **Talks.** I could not reach the Fortnite virtual shadow map and Lumen blog numbers, AMD's GPUOpen guide, Lagarde's actual darkening values, or any Unreal Fest or GDC talk on night lighting or rain.
- **Whether SSAO is turned off when Lumen GI is on.** The page failed to load.
- **MegaLights' maturity in 5.8.** The page does not say. An earlier note called it production-ready.
- **My own numbers:** every EV, lux, roughness, spacing and attenuation figure marked [I], including the night EV100 of 3 to 4, which differs from the earlier note's 2 to 3. Settle it with a grey card in the game's own camera.
- **Lamp details:** the column height and spacing on a 1990 northern high street, and whether it used 35 W, 55 W or 90 W SOX.
## Checked by the research session (1 October 2026)

- **The arithmetic holds.** 4,550 lm over a full sphere is 362 cd. From a 6 m column that gives 10.1 lux beneath and 0.52 lux on the road 15 m along, which is 19.5 to 1, or 4.3 stops. Mid-grey at 15 lux is EV100 2.6 (incident-meter constant 250), close to the note's 2.8.
- **The game's own night settings, read but not run** (production/specs/unreal-look.json and the wet_night row of production/specs/vignette-scene.json, as on main today):
  - **The sky light.** The sky light that lights the street at night is sky_intensity 0.35 × sky_light_gain_night 1.0 = 0.35. By day it is 0.70 × 0.5 = 0.35. So the street gets the **same ambient sky light at night as on the overcast day**, before exposure. Only the sky as seen is cut, to 0.15.
  - **The fog.** At night it is denser (0.022 against the day's 0.004), may reach 45% opacity (against 10%), and is coloured orange-brown on purpose (fog_night_colour).
  - **The lamps.** They are look numbers, 300 lm of glow plus a 1,200 lm downward cone, not the 4,550 lm of a real lamp. The exposure is held at a fixed pin (0.4).
  - Together these match this note's diagnosis: broad, even fill (the sky light) and orange in-scattering (the fog) fill the gaps between lamps, and the held exposure lifts the whole street to one orange level.
  - **Not proved.** This is a lead to test, not a measurement. The first test is the one the note gives: the Lighting Only view, with the sky light, then the fog, switched off one at a time in the game's own camera.
