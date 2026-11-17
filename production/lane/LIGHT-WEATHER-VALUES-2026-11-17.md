# Light and weather: real values for the target (17 Nov 2026)

## Review correction (fresh review FAIL, 17 Nov; REVIEW-LIGHT-WEATHER-VALUES-2026-11-17.md). Read this first; it overrides the text below.

- The "possible fault" (pool only about 2:1 over the night fill, an orange wash) is withdrawn. It used the wrong Unreal rule: a spot light's lumens fill only its cone (Epic, Using Physical Lighting Units; UE 5.8 forum report on spot light cone solid angle, both read 17 Nov by the reviewer). Checked by the lane: 167 lm in a 46 degree outer cone is about 87 cd, so about 3.7 lux under a lamp 4.83 m up, about 10 times the 0.38 lux fill. Do not lower night_fill_lux on this note (it comes from his 4 Nov corner note); only measure pool to gap in the night view.
- The 40 lm bulb reaches only 1 m since 28 Oct, so it adds nothing on the ground.
- Canon names only Meridian, a fictional British port town, with no region or latitude. The north-east coast, 54.6 N (longitude 1.2 W used), Tynemouth weather and the 17 Nov date are working assumptions, not canon; 1.8 degrees further west moves the sun times about 7 minutes later. Sun times re-computed by the reviewer within 2 minutes.
- The 70 lux on, 35 off photocell figures are for the SC 1000 cell; that 1990 lamps used it is a guess.
- SOX 35 W: 4,770 lm here, 4,550 in the look file note; the main session keeps one figure with its source.


Paper only. Feeds TARGET-LIGHT-WEATHER-2026-11-17.md, its dusk, lamp and drying gaps. Every web source read 17 Nov 2026. "Computed" means arithmetic on a read source; "judgement" means no source.

## Summary

1. A November dusk on the north-east coast runs from sunset at about 16:00 to full dark at about 17:25 (GMT); the light falls about 200 times in the 40 minutes after sunset.
2. Street lamps of the time switched on at about 70 lux, near sunset under cloud; low-pressure sodium glows red first and turns full yellow over about 8 to 15 minutes.
3. A real side street was lit to an average of 3.5 to 6 lux, the dimmest point 1 to 2.5 lux; the cloudy sky adds only about a hundredth of a lux, so between pools it is truly dark.
4. (Withdrawn after review.) The pool under our lamps is about 10 times the night fill, inside the real 10 to 25 range; measure pool to gap in the night view, change nothing on this note.
5. A wet road in November takes roughly 3 to 14 hours to dry, puddles days; with rain on about 12 days a month the street is rarely fully dry.

## Units the look file takes

From unreal-look.json and vignette-scene.json (not edited): lamps in lumens, game-scaled (40 lm bulb, 167 lm pool, 4.83 m up); colour as linear RGB; night_fill_lux in lux; exposure_pin as plain luminance, not EV100 (day 4.0, one stop twice the pin; night 0.4); wetness, water level, wet_darken 0 to 1. RULINGS: day one stop darker, never brightened (29 Oct); wetting and drying (5 Oct); pools with darkness between (1 Oct). Real lux carries over only as ratios.

## Numbers

| Quantity | Value | Unit | Source |
|---|---|---|---|
| Sunset, 54.6 N, 17 Nov 1990 | 16:01 | GMT | computed (standard solar formula, about 2 min) |
| Sun 3 deg down / civil end / nautical end | 16:19 / 16:42 / 17:26 | GMT | computed |
| Same on 1 Nov; 1 Dec | sunset 16:30, civil end 17:08; sunset 15:45, civil end 16:28 | GMT | computed |
| Clear-sky light at 0, -3, -6, -12 deg | 759, 79, 3.4, 0.008 | lux | [1] (spline of MacInnis et al. 1995, secondary) |
| Overcast at sunset | 75 to 400 | lux | judgement (0.1 to 0.5 of clear; [2] says overcast can briefly exceed clear) |
| Overcast sky luminance at sunset | about 25 to 130 | cd/m2 | computed, L = E / pi |
| EV100 at sunset / just after / about 10 min after | 12 / 9 to 11 / 7 | EV100 | [3] ANSI PH2.7; [4] |
| EV100 lit night street | 2 to 3 (typical to bright); ANSI 7 to 8 for bright streets and window displays | EV100 | [4]; [3] |
| EV100 city at night, dim street | 3; 3 to 5 | EV100 | [5] (BeamNG guide) |
| Lamp switch-on level, old UK cells | on 70, off 35 | lux | [6] |
| SOX colour | linear (1.0, 0.22, 0.0) | linear RGB | computed from (0.569, 0.430); file holds (1.0, 0.25, 0.0) |
| SON colour | 2000 K, Ra 35; linear about (1.0, 0.26, 0.01) | K; linear RGB | [7]; computed (Planck approximation) |
| SOX 35 W output | about 4,770 (37 W x 129 lm/W, modern SOX Plus) | lm | [8] |
| SON 50 W / 70 W (1987, 1976 Thorn) | 3,500 / 5,800; warm-up 3 / 5 min | lm; min | [7], [9] |
| SOX warm-up | red neon glow first, full output 8 to 15 | min | [10] |
| BS 5489-3:1992 classes 3/1, 3/2, 3/3 | average 10, 6, 3.5; minimum 5, 2.5, 1.0 | lux | [11] |
| Average to minimum on the road | 2:1 to 3.5:1 | ratio | computed from [11] |
| Under-lamp to midpoint (SOX, 5 to 6 m column) | about 10:1 to 25:1 | ratio | judgement |
| Cloud-lit sky at night near a town | 0.003 to 0.011 (partly cloudy, small town); Berlin cloud brightens sky 10.1 times | lux | [12]; [13] |
| Pool to sky ratio, real | about 300:1 or more (3.5 lux to 0.01) | ratio | computed |
| Shop tubes | UK preference White 3500 K (halophosphate Ra 55); Warm White 3000 K Ra 52 | K | [14] |
| Tungsten room lamp | 2700 to 2800 | K | judgement (not read) |
| Tube colour, linear | 3500 K (1.0, 0.57, 0.26); 3000 K (1.0, 0.48, 0.15); 2700 K (1.0, 0.42, 0.10) | linear RGB | computed |
| Potential evaporation, November, near York | 14.9 to 24.1 (1995 to 1998), so 0.5 to 0.8 a day | mm/month | [15] (Met Office MORECS) |
| Water left on asphalt after it drains | 0.1 to 0.3 (texture depth 0.2 to 0.8) | mm | judgement on [16] |
| Road drying, film | 3 to 14 | hours | computed |
| Puddle 5 to 20 mm | 6 to 40 days at that rate; lasts to the next rain | days | computed |
| Rain days 1 mm or more, Tynemouth, Nov | 11.5 (1961 to 90); 12.2 (1991 to 2020) | days | [17] |
| Nov rain; sunshine; max/min | 58.8 mm; 67 h; 9.0 / 4.3 C (1961 to 90) | | [17] |
| Relative humidity | not found | % | UNVERIFIED |

## Findings

Dusk. Light falls tenfold from sunset to the sun 3 degrees down (18 minutes here in November), then twentyfold more by civil end [1]. No measured British overcast twilight was reached; overcast near sunset is sometimes brighter than clear [2], so its factor is judgement.

Lamps. 1990 cells switched on at about 70 lux; councils moved to 35/18 around 2010 [6]. Under cloud that is near sunset (judgement), clear about 18 minutes after. SOX lamps glow red, then full yellow over 8 to 15 minutes [10]. SON came to Britain from 1976, sold to replace mercury [7][9]; canon keeps SOX. In linear RGB the two lamps are nearly one colour; the difference is on surfaces: SOX shows no colour at all, SON (Ra 35) keeps some.

Lit streets. BS 5489-3:1992 asked 3.5 to 10 lux average, minimum 1 to 5 [11]; the 1989 figures were not reached. Cloud-lit night sky near a town is about a hundredth of a lux [12], up to tenfold over a city [13].

Our night, by arithmetic (UNVERIFIED). If Unreal converts spot-light lumens as if shining all round (recalled, not read today), the 167 lm pool gives about 0.57 lux under the lamp at 4.83 m, the 40 lm bulb about 0.14; the night fill about 0.38 lux on the ground. Pool to fill about 2:1, under one stop, against 10:1 to 25:1 real under-lamp to midpoint and about 300:1 lamp to sky. That would make the orange wash RULINGS 1 Oct forbids, and bears on the unmeasured C4.

Wet ground. No measured drying time was reached. November evaporation near York, 15 to 24 mm a month [15], dries a 0.1 to 0.3 mm film in 3 to 14 hours; wind and traffic speed it [18], night slows it. Puddles outlast the next rain; with rain about one day in 2.6 the street is damp most of a November week.

## What it changes in the target

- Section 1 dusk row: replace "no value" with the table above; a dusk state could run sunset to civil end (about 40 minutes), picture exposure judgement 2 to 3 stops darker than day, so pin 0.5 to 1.0 (computed from day 4.0); night pin 0.4 stays.
- Section 2: add the 70 lux switch-on, warm-up red then yellow over 8 to 15 minutes, BS classes as the pool ratios.
- Section 3: drying as real hours: wetness down 0.07 to 0.33 per game hour, up to full in 5 to 15 minutes of rain (judgement); puddle level down over days, not minutes; drying 20 to 100 times slower than wetting, not Lagarde's 3 to 12.
- Section 5 check: measure pool to gap and pool to fill in the night view before touching night_fill_lux; target under-lamp to midpoint at least 10:1 (judgement on [11]).

## Unverified

Overcast twilight factor; humidity; 1989 BS figures; a measured drying time; Unreal's spot lumen convention; tungsten colour; the 1990 lamp of a northern side street; SOX 35 W lumens of 1990 lamps (the 4,770 is a modern sheet).

## Sources (read 17 Nov 2026)

1. https://download.osmand.net/wiki/File:Twilight_illumination_by_sun_altitude_luxes_2_r_1.svg
2. Lee and Hernandez-Andres, Applied Optics 44(27), 2005: https://colorimaginglab.ugr.es/pages/pdfs/ao_2005_5704/!
3. https://en.wikipedia.org/wiki/Exposure_value (Table 2, ANSI PH2.7)
4. https://www.kenrockwell.com/tech/ev.htm
5. https://documentation.beamng.com/modding/lighting/pbl/
6. https://streetlightonline.co.uk/Photocells/RoyceThompson/SC1000SAV.htm
7. https://lamptech.co.uk/Spec Sheets/D SHP Thorn SONT50.htm
8. https://www.assets.lighting.philips.com/is/content/PhilipsLighting/fp928145500018-pss-en_gb
9. https://lamptech.co.uk/Spec Sheets/D SHP Thorn SONE70.htm
10. https://vintagestreetlights.com/history/lps.html
11. Fotios, Lighting Research and Technology 52(5), 2020: https://eprints.whiterose.ac.uk/id/eprint/151808/1/Fotios%202019%20Curr
12. Jechow et al. 2017: https://ar5iv.labs.arxiv.org/html/1705.04968
13. Kyba et al., PLoS ONE 2011: https://doaj.org/article/76138bef7cc1440fa360ea5f9ecb6957
14. https://lamptech.co.uk/Documents/FL%20Colours.htm
15. https://intarch.ac.uk/journal/issue11/3/morecs.html
16. Sanz Garcia et al., BJRBE 16(3), 2021: https://bjrbe-journals.rtu.lv/bjrbe/article/download/bjrbe.2021-16.530/556/543
17. https://www.metoffice.gov.uk/research/climate/maps-and-data/location-specific-long-term-averages/gcybg0mzy
18. Hoffmann, Nutz, Blab, PIARC 2014: https://proceedings-andorra2014.piarc.org/content/actes/72_eng.pdf

Unreached: Spitschan 2016 at PMC (captcha; Nature copy has no twilight lux); BS 5489 texts; SABRE SOX page; SWOV road drying report; TRID asphalt rainfall record; a 1000bulbs SOX sheet; Napier thesis past its first third.
