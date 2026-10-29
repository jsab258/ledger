# Keeping the night readable between the lamps (29 October 2026)

Through the player's camera at night, 87% of the frame is near black (luma under 10 of 255). Tried and failed: exposure one stop up (84%), a black offset of 0.0125 (62%; milky at 0.025), the night sky light up to ten times (no change), and a faint moon from two directions (flat, or like late dusk). Tags: **M** measured, **R** read, **I** inferred. All read 29 October 2026.

## Questions

1. How do Mafia and Kingdom Come II keep a lamp-lit street readable between lamps? What carries the gaps: sky, moon, fog, grade, local exposure, bounce?
2. What does Unreal 5.8 document for night exteriors?
3. What does a real 1990 British sodium street look like between lamps?
4. One third design, with settings, checks, cost and what is unverified.

## Our night, measured first

- **Re-measured from tonight's trial frames** (session scratchpad, exposure/ed-night-*.png; M), near black:
  - as it is: 87.2%
  - sky light ×10: 87.2%
  - moon 0.6: 75.9%
  - moon 1.5: 38.9%
  - moon 3.0: 23.0%

  The near pavement (the frame's bottom third) is 100% near black. This morning's street-at-night view is 66.1%.
- **Why (R, M):** each pool is a spot with cones of 22° and 46° (unreal-look.json).
  - Unreal measures these angles from the axis, and the light reaches zero at the outer one (engine source: SpotLightComponent.cpp; DynamicLightingCommon.ush).
  - From 4.83 m up, the light stops 5.0 m from the lamp's foot. Lamps stand 20 m apart on each side, staggered, so about 10 m of each pavement gets no direct light.
  - What is left is bounce, and a sky light at 0.35 × 0.15 of a dome itself drawn at 0.15. Ten times almost nothing still lands in the tone curve's toe, at 0 to 1 of 255.
- **The night pin (0.4) is in cd/m², not EV100.** The project sets no extended luminance range, and the engine's default is off (SceneView.cpp; R; not checked at run time).

## 1. The two games

**Mafia**, studied as The Old Country (Unreal 5.4), from the project's extracts (F:/LedgerTools/aaa-study/study-5/). Mafia: Definitive Edition runs on another engine and was not studied.
- **A moon carries the gaps, under a visible moon disc** (M; 12 presets with the moon on):
  - moon light median 0.015 (0 to 1.5), 26° to 50° up;
  - a disc in the sky in 11 of 12 (median 0.2);
  - moonlight at 7,500 K under a 4,500 K white balance, so it reads blue;
  - the sky picture at 0.007 against the day's 2.0.
  - Two presets are moonless; one is named "NoMoonlight". Palermo's saved moon is 0.014 (R).
- **Its street lamp throws wide** (R; 39 lamps): a key spot of 1.5 cd with an outer cone of **80°**, reaching 20 m, no shadows, bounce doubled (indirect 2.0), fog scattering 2.5.
- **Then the grade:**
  - exposure compensation +3.05;
  - fog median 0.0425;
  - local exposure: shadows 0.62, highlights 0.5;
  - colour-head offset 0.008 to 0.0125 (MAFIA-WEAR-2026-10-28.md).
- Not reached: its lamp's height and its Blueprint multiplier (×3), so its pool-to-moon ratio is only roughly 7 to 21 (I). No developer talk was found, and Epic's Mafia interview refused access (403).

**Kingdom Come II** (CryEngine).
- Its time-of-day values cannot be read (Study 5).
- It ships a half-moon sky texture (M).
- Its 381 "ambient" lights and 267 fog-only lights are nearly all in cutscene layers (325 and 260; M).
- Its open-world night was not reached. CryEngine's time-of-day pages render by script and could not be read.

**Answer (I):** Mafia's gaps come from a moon, which a disc in the sky justifies, and from wide, shadowless lamps with doubled bounce. The grade and local exposure only raise light that is already there.

## 2. Unreal 5.8's documents

- **Auto Exposure:**
  - Local Exposure "should always be set up when using" Lumen.
  - Shadow and highlight contrast "between 0.6 and 1"; curves by average scene luminance.
  - An exposure compensation curve keyed on average scene EV100.
  - Ours is off at night (the default, 1.0; Scene.cpp).
- **Sky Lights:** real-time capture takes in the atmosphere, height fog and unlit sky domes, but not volumetric fog. A recapture costs at least 120 ms.
- **Physical Lighting Units:** a directional light is in lux; a sky light is cd/m² times its picture. In lumens a narrower cone is brighter. Engine source: candela = lumens ÷ (2π(1 − cos outer)).
- **Volumetric Fog:**
  - each light has its own scattering intensity;
  - a shadowed local light costs about three times as much;
  - about 1 ms on PS4 at High;
  - no IES profiles in the fog.
- **Sky Atmosphere:** a moon is a second directional light (sun index 1) with a disc of 0.568°. Moonlight at the zenith is "0.26 Lux".
- **Spot Lights:** full strength inside the inner cone, falling to the outer cone. A separate bounce scale. IES for the shape alone.

## 3. A real 1990 British sodium street

- **No photograph is held,** so no real near-black share was measured (unverified). The evening-light note's four proxies are links, not downloaded.
- **Period lanterns light the gaps themselves.** Thorn EMI's British sodium lantern patent (US4450509, filed 1982; R):
  - the peak is **60° to 65° from straight down**, at least 200 cd per 1,000 lamp lumens;
  - from straight down to 30°, at most 80% of the peak;
  - under BS 4533, semi-cut-off beams reach 75° and cut-off beams 65°.
- **On our street (I):** under a lamp against its 60° ring is about 8 to 1 for one lamp. With the neighbours added, mid-gap is about **4 to 8 times darker than under a lamp**, not black. The 1 October figure of 20 to 1 assumed light thrown equally all round.
- **The sky cannot do it.** Berlin's overcast sky is 10.1 times its clear moonless sky, with examples of 1.4 and 0.43 mcd/m² (Kyba 2011; R). A uniform 1.4 mcd/m² sky gives about 0.004 lux on the ground (I), about a thousandth of a lit street. It shows as a glow behind the roofs; it does not light the pavement.
- **BS 5489-3:1992's averages** (3.5, 6 and 10 lux) come from a search summary only. Its minima were not reached.

## 4. Recommendation: the lamps carry the gaps

One design, from the period lantern and Mafia's wide key spot. No moon: an overcast sky cannot justify one, and both moon tries failed. No sky fill: it is unphysical at readable levels.

**Try 1** (all else as now: pin 0.4, bias 0, sky 0.15, fog 0.2, no moon, no lift, shadows on):
- **Cone:** `lantern_pool_cone_deg` 22/46 → **60/75**, full strength to 60° and cut off by 75° (semi-cut-off).
- **Brightness:** `lantern_pool_lumens` 500 → **1,215**. This keeps 261 cd on the axis, so the pool beneath is unchanged.
- **Reach:** the pool's attenuation radius 18 → **25 m**, a new look-file value. The engine's window, (1 − (d/r)⁴)², takes about 27% at a gap's middle (11 m) at 18 m, and about 8% at 25 m (DeferredLightingCommon.ush).
- **Predicted (I):** mid-gap about 1.8 lux against about 11 beneath, about 6 to 1. The hill, 110 to 200 m away, stays beyond every lamp.

**Try 2,** only if near black stays above 50% while C4 passes: night local exposure shadow contrast 0.8 (Epic 0.6 to 1, Mafia 0.62). If instead the ratio falls under 4, the outer cone goes to 70°.

**Checks:**
1. **Near black** (Rec.709 luma under 10) at the player's camera, empty street, scalability 2, 2,560 × 1,440, as tonight: **≤ 50%** (now 87.2%; the readable moon gave 39%; the limit is I). Also report the morning night view (66.1%).
2. **C4 in linear light,** using the calibrator in the packaged game, beneath the lamp at x 8 and halfway to the next: the pool **4 to 20 times** the gap (now about 150 to 5 as displayed; the band is I).
3. **Nearest pool's clipped red ≤ 2%** (rule of 8 October). Mickey's view must not go black, and his fascia lettering must stay at least 2 to 1.
4. **Night, not dusk:** the hillside's mean luma within 3 levels of tonight's. Then a fresh reviewer judges the new frame beside tonight's and the moon-1.5 frame.
5. **Frame time** inside the 60 fps budget, since wide shadowed spots cost more.

**Cost:**
- a trial switch for the cone and reach (as -LanternPoolLumens= is), a local build, captures, measures and a reviewer: **3 to 5 hours**;
- the packaged C4 reading and the morning views: 1 to 2 more;
- try 2: 1 to 2.

**Unverified:**
- the 6-to-1 prediction and the 50% limit (arithmetic, not run);
- Lumen's bounce or noise;
- the cost of a 75° shadowed spot;
- lamp post C's column glare, already in FINDINGS (lit in either cone);
- the C4 band, without a measured real photograph;
- the pin's units at run time;
- Mafia's lamp height and multiplier.

If the plain spot reads as a flat wash, next is a hand-written IES profile of the patent's shape: our own data, so no licence question.

## Not reached

- Epic's Mafia interview (403).
- Any Hangar 13 or Warhorse talk on night lighting.
- CryEngine's time-of-day pages.
- Kingdom Come II's time-of-day values.
- The White Rose road-lighting paper (its PDF could not be decoded).
- BS 5489-3:1992's tables.
- Any real 1990 night photograph.

## Sources (read 29 October 2026)

Epic's pages were read through a page reader, every section heading confirmed:
- https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-exposure-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-lights-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-atmosphere-component-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/spot-lights-in-unreal-engine

Also:
- UE 5.8 source on this PC (SpotLightComponent.cpp, SceneView.cpp, Scene.cpp, DynamicLightingCommon.ush, DeferredLightingCommon.ush).
- Thorn EMI, US4450509, https://patents.google.com/patent/US4450509
- Kyba and others, PLoS ONE 6(3) e17307, 2011, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0017307
- Project files: Study 5's raw tables; MAFIA-WEAR-2026-10-28.md; evening-light-1990; aaa-street/3-LIGHT-AND-GRADE.md; unreal-look.json; vignette-scene.json; VignetteShot.cpp; order o28c-d11-look.
