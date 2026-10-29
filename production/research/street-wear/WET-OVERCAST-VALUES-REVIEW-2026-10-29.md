# Review: wet overcast values (29 October 2026)

A fresh reviewer's check of WET-OVERCAST-VALUES-2026-10-29.md against its sources. Every link was read on 29 October 2026; the engine source was read on this PC (UE_5.8). M measured or computed by the reviewer, R read at the source, I inferred.

**Verdict: PASS WITH FIXES.** Nearly every number re-derives, and the main conclusion stands: the ground and the brick are several times darker than real. Four fixes are needed before it is a target. The pin is out of date. The day's exposure bias was left out. The targets mix measured albedo with base colour. Porous and sooted surfaces need their own bands.

## Findings

1. **Sources CONFIRMED (R, M).**
   - LBNL-49283 (https://eta-publications.lbl.gov/sites/default/files/lbnl-49283.pdf): fresh asphalt 0.05; an old street 0.11; aged asphalt about 0.12; 16 concrete streets 0.18 to 0.35. These are solar values from a pyranometer (ASTM E1918) on Californian streets.
   - Lagarde 2011 (0.04, 0.12, 0.55, from Wikipedia): the page itself says these "include some specular".
   - physicallybased.info: brick (0.262, 0.095, 0.061). Its sources are Wikipedia and acoustics tables, so UNVERIFIED is right.
   - Lekner and Dorf: all pages read. The equations and the Ångström pairs check; p = 0.475 is the paper's own value for water. The reviewer re-ran the model, and every cell of the wetting table reproduces.
   - Lagarde 2013: 0.68 at 0.12.
   - PVGIS: the same call, re-run in memory, gives 370 hours (11:10 and 12:10 UTC) and 53, 69, 95, 135 and 159 W/m², exactly as the file has them.
   - Mardaljevic: the 10,000 lux sentence and 7πLz/9.
   - Wikipedia, Exposure value: 13 and 12 (ANSI PH2.7); C = 250 for a flat sensor. Wikipedia, Daylight: 1,000 to 2,000 lux, uncited.
   - Epic's units page. Engine: the extended range defaults to off, and PostProcessEyeAdaptation.cpp lines 659 to 668 treat the pin as a plain luminance.
   - Camera data (Commons API): EV100 11.92 and 12.28. Sun heights 25.3° and 25.1°.
   - Photographs B and C, re-read in the built-in browser with the reviewer's own boxes. B: sky 233, road 162 to 173 (0.52 to 0.55 of the sky), footway 124 to 126, render 177. C: sky 204 to 228, buff brick about 155/127/96. All inside the file's bands.
   - Littlefair's efficacy is still UNVERIFIED (the journal page was refused). Dervishi and Mahdavi's measured fit (https://www.aivc.org/sites/default/files/p_2222.pdf; Ev = 120·Ee + 450) gives 6,800 to 19,600 lux for the same hours, about 8% more. The band holds.

2. **The game's numbers CONFIRMED (M).**
   - Sun 0.3. The sky light is 0.7 × 1.4286 = 1.0 times the captured dome.
   - The dome (the 8-bit PNG, decoded to linear, × 9.1) integrates to 4.22 cd/m² and 14.8 lux.
   - WetDarken 0.744. Road 0.012; flags 0.026 to 0.027; kerb 0.073.
   - Brick: the untinted meshes are 0.065, the tinted houses 0.038 to 0.056.
   - *Fix:* give the brick as 0.04 to 0.065. Compare the dome's mean with the real sky's mean (2Lz/3, so 1,600 to 4,900 cd/m²), not with its zenith.

3. **The pin is out of date.**
   - *The file says:* pin 3, white point 3, EV 1.58; vignette-scene.json and DECISIONS "call it EV100 and one stop"; item 5 says re-read at pin 3 and put a line on his page.
   - *Found:* the spec now holds 4.000, with a plain-luminance note, and DECISIONS 08:55 records the correction.
   - *Fix:* redo section 7 and the "chart's light" values at pin 4 (log2 4 = 2.0). Item 5 becomes: read neutral 5 at pin 4 and expect 110 to 135. Drop the page line.

4. **The day's exposure bias is left out.**
   - *The file says:* "an open grey card 0.65 stop above mid grey … Light and exposure agree … Not the fault."
   - *Found:* by day nothing overrides AutoExposureBias (VignetteShot.cpp lines 4246 and 4247, and 10381 and 10382, set it at night only). The engine default, r.DefaultFeature.AutoExposure.Bias, is 1.0 (SceneView.cpp lines 196 to 199; Scene.cpp lines 516 to 519), and no project ini sets it. The shader multiplies exposure by 2^bias (PostProcessEyeAdaptation.usf lines 179 to 193).
   - So by day the effective white point is half the pin: at pin 4, an open grey card sits about 1.24 stops above mid grey, not 0.24. The office zeroes its bias (CrimeProbe.cpp lines 4510 and 4511); the street does not.
   - *Fix:* confirm the bias from a day-only run's ppAutoExposureBias (the last line printed came from a night shot). Restate the grey-card line. Let the chart reading at pin 4, not the sums, decide whether light and exposure agree.

5. **The targets mix measured albedo with base colour.**
   - Lekner and Dorf's wet albedo (1 − A) includes the water film's own reflection, R_l, about 0.02 with light falling straight down. In Unreal the film specular supplies that.
   - So the wet base colour is about 0.02 lower: road 0.05 to 0.06 (not 0.07 to 0.08), flags 0.11 to 0.20 (M). Taken this way, the base colour falls to 0.49 to 0.59 of dry. "Under 0.05 hardly darken" holds only when the film's own reflection is counted in.
   - Dry albedos also include specular (Lagarde says so). A rough surface at the default Specular adds about 0.06 seen head-on (Unreal's EnvBRDF approximation, M), so dry base colours sit below the bands, asphalt most of all.
   - *Fix:* label the bands "measured total reflectance" and give base colour separately. Beside C6's base-colour view, add a lit check of each surface against neutrals 5 and 3.5 under the same light. The gap remains (the road four to five times too dark).

6. **Porous surfaces darken more.**
   - The paper fits rough solids. It says porous media follow the other model (Twomey, Bohren and Mergenthaler), and its sand pair loses 50%.
   - Lagarde 2013 lets fully porous surfaces fall to 0.2 of dry (Gu et al.; Nakamae et al.).
   - *Fix:* widen the flags' wet band downward (I), and name the model behind each band.

7. **The brick of 1990.**
   - The west rows are "soot-blackened" (ps5-corner.json). The clean-brick band of 0.10 to 0.20 is inferred and has no source.
   - *Fix:* give clean and sooted brick separate bands, or hold brick out of item 2 until a source is found.

8. **Smaller points.**
   - (a) "Road 100 to 110 looking down" comes from photograph A's stone setts, not asphalt. Mark it I.
   - (b) The photographs give red brick 55 to 97; nothing supports the 130.
   - (c) "EV100 11 to 12.8" is the flat incident-meter convention. Unreal's grey-card rule, log2(E/π), is 0.33 stop lower. Say which one is meant.
   - (d) PVGIS values come from satellite data, not measurement.
   - (e) "Rainy is the lower quarter" is inferred. Mark it I.
   - (f) "Tuned while the exposure moved" does not fit: the pin stood at 2.000 through all of the road's October cuts.
   - (g) The camera EVs are framing-dependent reflected exposures; St Albans used −0.3 EV of compensation, and Fletcher's Terrace's December sun was far lower. They give the order of magnitude only.
   - (h) The model gives a loss of 32 to 37% at 0.12 to 0.35; the 50% is sand.

9. **Not checked (by the file or the reviewer).** The DONTNOD PBR chart's values (they exist only as a picture); measured wet and dry pairs for concrete and brick (Twomey et al. 1986; Gu et al.); a visible-light source for asphalt; the CIE road classes (Q0 is for a driver's view, not an albedo, so low priority).
