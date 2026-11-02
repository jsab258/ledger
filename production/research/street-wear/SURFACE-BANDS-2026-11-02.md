# Shopfront paint, gilt, joinery, slate, tiles and kiosk red: measured reflectance bands (2 November 2026)

Tags: **M** computed here from a source's data, **R** read at the source, **I** inferred. Every link was read on 2 November 2026.

## Questions

1. Dark gloss shopfront paint, fresh and weathered?
2. Gilt: gold's F0; gold paint's LRV?
3. White or cream gloss joinery, fresh and after ten seaside years?
4. Roof slate, dry and wet?
5. Glazed stallriser tiles: body and glaze?
6. The K6 kiosk's red?
7. Do the Mafia or Kingdom Come II studies give any?

## Method

- Spectra are read in memory and computed as in FLAGS-BRICK-BANDS: CIE 1931 2°, D65, 380 to 780 nm (M).
- Gold: R = ((n−1)² + k²)/((n+1)² + k²) from measured n and k, then the same sums (M).
- LRVs come from manufacturers (R). Their swatch colours are converted to linear and scaled to the LRV (M on R).
- **Specular in an LRV (I).** BS 8493 itself was not reached. A BS 8493 test report (Desso) states "specular component included", D65, 10° observer (R; https://www.specifiedby.com/desso/airmaster-carpets/Desso_AirMaster_Technical_LRV.pdf, read 2 November 2026, the review's fix 1). ECOSTRESS black alkyd gloss totals 0.036 to 0.043 (M), about a gloss surface's own 0.040 (n 1.5, M). Crown's pages give no method or finish, and their LRV equals the Lightness in Crown's own notation, so it is the colour's value rather than a gloss panel's (R, the review). So a gloss LRV probably holds about 0.04 of specular.
  - Base colour = LRV − 0.04, floor about 0.02 (I).
  - Unreal's Specular 0.5 (F0 0.04) supplies the rest. This suits default lit as the project runs it (r.Substrate 0, energy conservation off: UE 5.8 ShadingEnergyConservation.ush; the review).

## 1. Dark gloss paint

| BS 4800 (Crown Paints) | LRV (R) | Linear at LRV (M) |
|---|---|---|
| 20 C 40, dark navy | 6 | (0.045, 0.060, 0.103) |
| 18 B 29, blue-black | 6 | (0.053, 0.061, 0.068) |
| 18 C 39, deep blue | 9 | (0.042, 0.100, 0.137) |
| 18 B 25, slate blue (the Hook sheet's board) | 16 | (0.138, 0.165, 0.177) |
| 00 E 53, black | 4 | (0.039, 0.040, 0.041) |

- **Base colour, fresh (I):** navy 0.02 to 0.03; slate blue about 0.12.
- **Weathered (I):** chalking and grime lift and grey it to 0.03 to 0.06. Nothing measured was found.

## 2. Gilt

- **Gold's F0 (M):**
  - Babar and Weaver 2015: luminance 0.800, (1.057, 0.773, 0.308);
  - Olmon 2012: 0.799;
  - McPeak 2015: 0.809;
  - Johnson and Christy 1972: 0.767, (1.035, 0.728, 0.365).
- **Cross-checks.** physicallybased.info's gold, built from Babar, is (1.059, 0.773, 0.307) (R), which this computation reproduces. Epic's (1.000, 0.766, 0.336) is already in DRESSING-2026-10-04.
- **For the game (I):** metallic 1, base colour (1.00, 0.73 to 0.78, 0.31 to 0.37).
- **Gold paint: no LRV found.** It is bronze powder, that is brass flakes. physicallybased.info's brass, (0.910, 0.778, 0.423), luminance 0.78 (R, M), is an upper bound: UNVERIFIED.

## 3. Painted joinery

- **Fresh LRVs (Crown, R).**
  - White 00 E 55: 88.
  - Ivory 10 B 15: 81.
  - Magnolia 08 B 15 and cream 10 C 31: 77.
- **Fresh base colour (I).**
  - White about 0.84, (0.84, 0.85, 0.79).
  - Cream 0.73 to 0.77, (0.82, 0.73, 0.52).
- **Weathered, measured end (M; FLAGS-BRICK-BANDS).** London B012, white paint on brick, "weathered, rough": 0.515, (0.624, 0.499, 0.357).
- **Ten seaside years (I):** 0.50 to 0.70, yellowing toward that colour, darkest at sills. No measured weathering of gloss joinery was reached: UNVERIFIED.

## 4. Roof slate

| Sample | Y (M) | Linear (M) |
|---|---|---|
| London L001u, slate roofing shingle, grey, weathered | 0.099 | (0.109, 0.098, 0.080) |
| London L001d, slate, grey, "clear" | 0.089 | (0.091, 0.089, 0.083) |
| ECOSTRESS Ward92, grey slate, solid, Bangor, Pennsylvania | 0.095 | (0.092, 0.096, 0.099) |
| ECOSTRESS 0680, slate roof shingle, "weathered", "gray" | 0.172 | (0.184, 0.170, 0.159) |

- **Left out:** powdered slates (0.12 to 0.42) and fibre-cement slates (0.050, 0.061).
- **Dry, total:** 0.09 to 0.17, centre 0.10 (M). **As base colour** (the footnote's rule: Kotthaus's nadir values as they are, ECOSTRESS's hemispherical ones 0.02 to 0.04 lower; the review's fix 3): 0.06 to 0.15, centre 0.09 (L001u and L001d 0.089 to 0.099; Ward92 0.055 to 0.075; 0680 0.13 to 0.15).
- **Not found:** a Welsh or Westmorland sample. Their blue or green tint is UNVERIFIED.
- **Wet (I).** Lekner and Dorf (WET-OVERCAST section 2: 0.75 of dry at 0.08, 0.68 at 0.12) gives 0.065 to 0.11 total. Wet base colour is 0.045 to 0.09, and the film's 0.02 gives the shine.

## 5. Glazed tiles

- **Johnson Tiles, gloss wall tiles (R):** white LRV 86; cream 71 and 76. Their LRVs are "from Johnson Tiles' internal test reports", "for guidance only".
- **physicallybased.info's porcelain:** 0.743 (R, M), measurement not stated.
- **The glaze (I).** Clear glass, n about 1.5, F0 0.040 (M). A glaze is one smooth surface over an opaque body.
  - Use default lit, Specular 0.5, low roughness, base colour the body: white about 0.82, cream 0.67 to 0.72.
  - Not Unreal's clear coat (the review's fix 2): UE 5.8's ClearCoatBxDF (ShadingModels.ush) dims the base layer by (1 − F)², about 0.92, and keeps the base layer's own specular, and under sky light ClearCoatCommon.ush forces that layer to F0 0.08; a body of 0.82 would read about 0.83 in direct light and about 0.90 under sky. If clear coat is wanted anyway, set the body by a chart render.
  - A glaze does not weather. Dirt sits in joints and crazing.
- **Not found:** a measured patterned or period tile.

## 6. K6 kiosk red

- **Which red.** 538 Post Office Red served kiosks "up to about 1968". 539, "Postal Service Red", served them "after 1968"; about 1988 539 was renamed Currant Red and 538 became Cherry Red (lightstraw.uk, R; the review's fix 5). So a 1990 kiosk is 539.
- **Its value.**
  - No LRV for 539 was reached.
  - 538: LRV 10.71, RGB 160/57/59 (MyPerfectColor; snippet only, page 403), Y 0.107 (M).
  - W3Schools' "non official approximate" hexes: 538 #C41C22, Y 0.127 (M); 539 #D21E2B, Y 0.148 (M), far more saturated, linear (0.644, 0.013, 0.024). The two approximations of 538 differ by 0.02.
  - Nearest measured reds: Crown BS 4800 04 E 53 at 15 and 04 D 44 at 14 (R).
- **Band (I):** total 0.11 to 0.15; base colour 0.07 to 0.11. Neither example colour is 539 (the review's fix 4): the low end, (0.22, 0.026, 0.027), is MyPerfectColor's 538 at 0.067; the high end, (0.37, 0.040, 0.031), is BS 4800 04 E 53. The hue is UNVERIFIED as well as the value.
- **Weathered red** fades pinker and lighter (I).

## 7. Reference first

The aaa-reference studies give no albedo, LRV or F0 for these surfaces. None found.

## Target bands

Dry base colour as linear luminance; total reflectance (LRV or Y) in brackets.

| Surface | Base colour | Example linear | Tag |
|---|---|---|---|
| Navy gloss fascia, fresh | 0.02–0.03 (0.06) | (0.019, 0.025, 0.043) | R; base I |
| Navy, weathered | 0.03–0.06 | greyer | I |
| Slate-blue board | 0.12 (0.16) | (0.104, 0.124, 0.133) | R; base I |
| Gilt, metallic 1 (F0) | 0.77–0.81 | (1.00, 0.73–0.78, 0.31–0.37) | M |
| White gloss joinery | 0.84 (0.88) | (0.84, 0.85, 0.79) | R; base I |
| Cream gloss joinery | 0.73–0.77 (0.77–0.81) | (0.82, 0.73, 0.52) | R; base I |
| Joinery, ten years | 0.50–0.70 | (0.62, 0.50, 0.36) low end | M end; I |
| Slate, dry | 0.06–0.15, centre 0.09 (0.09–0.17) | (0.11, 0.10, 0.08) | M |
| Slate, wet | 0.045–0.09 (0.065–0.11) | | I |
| Tile body, default lit, Specular 0.5 | white 0.82; cream 0.67–0.72 | | R; base I |
| K6 red, 539 | 0.07–0.11 (0.11–0.15) | 538's (0.22, 0.026, 0.027) to 04 E 53's (0.37, 0.040, 0.031); 539's own hue unknown | UNVERIFIED |

- **Kotthaus's nadir values** stand as base colour; take ECOSTRESS's hemispherical ones 0.02 to 0.04 lower.
- **Rain (I)** leaves paint, gilt and glaze unchanged; only the film adds.

## Not reached

- **BS 8493 and its Annex A** (paywalled). So the specular in an LRV is unconfirmed; the Tarkett reports said to state it returned 404.
- **Refused pages.**
  - e-paint.co.uk's Lab and LRV pages (403; a retry was refused by this session's permission check).
  - MyPerfectColor (403).
  - Historic England list entry 1409553 (403). Its "Post Office Red 539" is from a search summary.
- **Others.** The Kotthaus paper (bot check; its Zenodo documentation was read instead, but its documentation PDF is over the fetch limit, so L001u "weathered" and L001d "clear" are unconfirmed: the review). Johnson's Polar White sheet (404). hextoral (403).

## Review

A fresh reviewer checked every number against its source on 2 November 2026: PASS WITH FIXES. It confirmed all eleven Crown LRVs and the swatch-scaled colours, the ECOSTRESS and Kotthaus values, the four gold F0 sets (within 0.002), physicallybased.info's gold, brass and porcelain, Johnson's LRVs and wording, the W3Schools hexes and the wet-slate arithmetic. Its six fixes are applied above: the LRV's specular (fix 1), the tile's shading model (2), slate's base column (3), the kiosk's example colours (4), the reds' renaming (5), ECOSTRESS 0404 (6).
- **Not found.** Gold-paint LRV; paint weathering; Welsh or Westmorland slate; period tiles; BS 381C Lab values.

## Sources

- Crown Paints: https://professional.crownpaints.com/colour/swatch/bs-20-c-40/, and likewise bs-18-b-29, bs-18-c-39, bs-18-b-25, bs-00-e-53, bs-00-e-55, bs-10-b-15, bs-08-b-15, bs-10-c-31, bs-04-e-53, bs-04-d-44
- ECOSTRESS: https://speclib.jpl.nasa.gov/library. Files under https://speclib.jpl.nasa.gov/ecospeclibdata/:
  - manmade.roofingmaterial.shingle.solid.all.0680uuusto.jhu.becknic.spectrum.txt
  - rock.metamorphic.slate.solid.vswir.ward92.jpl.perkin.spectrum.txt
  - manmade.generalconstructionmaterial.paint.solid.all.0402uuupnt.jhu.becknic.spectrum.txt, and likewise 0403, 0405 and 0406 (there is no 0404; the review's fix 6)
- Kotthaus, SLUM: https://zenodo.org/records/4263842 (LUMA_SLUM_SW.csv, 2013_LUMA_SLUM.pdf)
- CIE: https://files.cie.co.at/Publications-datasets/CIE_xyz_1931_2deg.csv, https://files.cie.co.at/Publications-datasets/CIE_std_illum_D65.csv
- Gold: https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/master/database/data/main/Au/nk/Babar.yml, and likewise Johnson.yml, Olmon-ev.yml, McPeak.yml
- physicallybased.info: https://api.physicallybased.info/materials
- Johnson Tiles:
  - https://www.johnson-tiles.com/catalog/pdf/kensington.cream.gloss.wall.tile.effect.rustic-structure.pdf
  - https://www.johnson-tiles.com/media/filer_public/0e/52/0e52b98a-ac10-46ce-a113-d829cd117be8/cristal_-_range_overview_bookletdownload_2021_1.pdf
- Kiosk paint: https://www.lightstraw.uk/ate/tec/paint/index.html
- Snippets only:
  - https://www.myperfectcolor.com/paint/386499-british-standard-colours-bs538-post-office-red
  - https://www.w3schools.com/colors/colors_british.asp
  - https://historicengland.org.uk/listing/the-list/list-entry/1409553
