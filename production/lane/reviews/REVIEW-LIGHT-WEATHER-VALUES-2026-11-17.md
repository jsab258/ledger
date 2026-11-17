# Review: LIGHT-WEATHER-VALUES-2026-11-17.md (17 Nov 2026)

Fresh reviewer, against TARGET-LIGHT-WEATHER-2026-11-17.md, canon.md, RULINGS.md, the look file and the game code.

Verdict: FAIL (the headline fault rests on a wrong engine convention; the rest passes with fixes).

## Findings

1. The claimed night fault (pool only about 2:1 over fill) is wrong. Epic's current page says a spot light's lumens apply "only to the solid angle affected by the light", 2 pi (1 - cos half-angle), so a narrower cone is brighter; a 5.8 bug report confirms the spot light divides lumens by the cone's solid angle. The game sets the pools in lumens (VignetteShot.cpp, SetIntensityUnits Lumens, 167 lm, outer cone 46 deg, tilt 0, 4.83 m). Over the cone: 1.92 sr, 87 cd, 3.7 lux under the lamp, against the fill's 0.38 lux on the ground (0.4 lux directional at pitch -70; that part is right). Under-lamp to fill-only gap about 10:1, inside the doc's own 10:1 to 25:1 target. The doc's 0.57 lux is the full-sphere figure. Fix: strike Summary 4 and the "orange wash" claim; keep only "measure pool to gap in the night view"; do not lower night_fill_lux on this arithmetic (it is his 4 Nov corner note).
2. The 40 lm bulb is counted as 0.14 lux on the ground, but since 28 Oct its reach is 1 m (lantern_bulb_radius_m), so it adds nothing at 4.83 m. Fix: drop it.
3. Location is assumed, not canon. Canon names only Meridian, "a fictional British port town", no region or latitude; RULINGS gives none. The doc writes "north-east coast", 54.6 N and Tynemouth climate as fact, and the date 17 Nov as if canon. Fix: label 54.6 N and Tynemouth as a working assumption (decision line, or his page if it matters to canon), and state the longitude used.
4. Sun times check out. Recomputed (NOAA formula) at 54.6 N, 1.2 W, 17 Nov 1990: sunset 16:03, -3 deg 16:20, civil end 16:43, nautical end 17:27; 1 Nov 16:31 / 17:09; 1 Dec 15:46 / 16:29. All within 2 minutes; 1.8 deg further west adds 7 minutes. Fix: none beyond naming the longitude.
5. Photocell: source confirms 70 on, 35 off for the older SC 1000, 35/18 from Sept 2010. That the 1990 cell was this one is inferred. Fix: say "older cells (SC 1000)".
6. BS 5489-3:1992 class figures come through Fotios 2020, not the standard (BSI listing only reached). Already marked; fine.
7. SOX 35 W given as 4,770 lm here, 4,550 in the look file note. Fix: one figure, sourced.
8. Unverified list should drop "Unreal's spot lumen convention" once finding 1 is applied, citing Epic's page.

## Sources (read 17 Nov 2026)

- Epic, Using Physical Lighting Units: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine (cone solid angle; inverse squared falloff is physical distance falloff, the attenuation radius only clamps it; off, the light is unitless).
- UE forum, USpotLightComponent cone solid angle remapping, 5.8: https://forums.unrealengine.com/t/uspotlightcomponent-incorrectly-applies-intensityunits-cone-solid-angle-remapping-when-buseiesbrightness-is-enabled-distorting-physical-ies-intensity/2843472
- Royce Thompson SC 1000/SAV: https://streetlightonline.co.uk/Photocells/RoyceThompson/SC1000SAV.htm
- Local: canon.md line 17; unreal-look.json (night_fill_*, lantern_*); VignetteShot.cpp around lines 3030 and 3799.
