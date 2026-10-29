# Flags, brick and render: measured reflectance bands (29 October 2026)

Answers points 4 and 7 of the wet overcast review. Tags: **M** measured or computed here, **R** read at the source, **I** inferred. Every link was read on 29 October 2026.

## Questions

1. Visible reflectance of weathered concrete paving flags, dry and wet?
2. Red brick, clean, and as sooted by 1990?
3. London stock and buff brick?
4. Painted render and pebble-dash?
5. How far does wetting darken these porous surfaces?
6. Do the Mafia or Kingdom Come II studies give any of these?

## Method

- **London spectra.** Kotthaus, Smith, Wooster and Grimmond 2014, ISPRS J. Photogramm. 94, 194–212. The paper was read in full (https://centaur.reading.ac.uk/36997/1/IJPRS_Kotthaus_2014_albedo_emissivity.pdf), and its data too (https://zenodo.org/records/4263842, LUMA_SLUM_SW.csv). It covers 74 samples "obtained from construction sites across London", measured in a laboratory: nadir view, two lamps, against Spectralon (R).
- **American spectra.** ECOSTRESS library 1.0, man-made class (https://speclib.jpl.nasa.gov/library; files under /ecospeclibdata/). These are Johns Hopkins samples, measured as directional-hemispherical reflectance (R).
- **Computation (M).** Each spectrum was read in memory; nothing was saved.
  - Luminance reflectance Y = Σ R·S·ȳ / Σ S·ȳ, from 380 to 780 nm in 1 nm steps.
  - Tables: the CIE 1931 2° observer and illuminant D65 (https://files.cie.co.at/Publications-datasets/CIE_xyz_1931_2deg.csv, …/CIE_std_illum_D65.csv). The white point came out at x 0.3127, y 0.3291.
  - Linear sRGB: XYZ through the standard matrix.
  - Several ECOSTRESS files start at 420 nm and were held flat below it. Y is unaffected; blue moves slightly.
- **Solar against visible (M).** Kotthaus's albedo column is solar-weighted.
  - Grey concrete C004: solar 0.37, visible Y 0.370.
  - Red brick B004: solar 0.31, visible Y 0.150.
  - So solar albedos stand for grey materials but double red brick's visible value.

## 1. Concrete flags

| Sample | State | Y |
|---|---|---|
| London C002 | new | 0.186 |
| London C008 | weathered, rough | 0.211 (linear 0.238, 0.208, 0.163) |
| London C003, C001 (cement) | weathered | 0.243, 0.257 |
| London C005 | weathered | 0.329 |
| London C004, C006 | weathered, grey and white | 0.370 (0.399, 0.368, 0.309), 0.378 |
| ECOSTRESS 0598, 0424 | runway, weathered; "slightly soiled" | 0.257, 0.258 |
| ECOSTRESS 0092 | runway, weathered | 0.333 |

- **Band (M).** The nine weathered samples span 0.21 to 0.38, median 0.258.
- **Caveat (I).** The paper does not say which samples were flags. It says only that concrete serves "roads and pavements (often as tiles)" (R).
- **Stone near the flags (M).** Sandstone: 0.20 to 0.45 (S003, S001, S005). Weathered granite kerbs: 0.34 and 0.43 (G002, G003).

## 2. Red brick

| Sample | Description | Y | Linear sRGB |
|---|---|---|---|
| ECOSTRESS 0412 | "smooth, weathered, and red" | 0.093 | (0.206, 0.065, 0.032) |
| ECOSTRESS 0413 | "smooth, bare, and red" | 0.098 | (0.211, 0.070, 0.038) |
| physicallybased.info | in hand | 0.128 | (0.262, 0.095, 0.061) |
| ECOSTRESS 0097 | smooth-faced building brick | 0.149 | (0.225, 0.132, 0.100) |
| London B004 | red clay, weathered | 0.150 | (0.286, 0.116, 0.084) |
| London B013 | "extremely weathered", mortar on face | 0.210 | (0.314, 0.187, 0.136) |

- **Band.** Clean or weathered: 0.09 to 0.15, centre about 0.13 (M). Mortar-smeared or light-red brick reaches 0.21 to 0.27.
- **Soot.** No measurement of soot-darkened British brick was found. The London samples date from about 2013, decades after smoke control (I).
- **Inference (I, with measured end points).** Treat soot as a dark film over a fraction f of the face: R = (1 − f)·R_brick + f·0.04.
  - The 0.04 is measured: ECOSTRESS black ashen cinders read 0.041, black alkyd paints 0.036 to 0.043 (M).
  - At f 0.3 the brick reads 0.08 to 0.12. At f 0.7, "soot-blackened", it reads 0.055 to 0.075.
  - Colour greys as well: (0.25, 0.10, 0.07) at f 0.5 becomes (0.145, 0.07, 0.055).
- **A London hint (I).** Weathered red ceramic roof tiles read 0.077 to 0.116, against 0.173 for a new red tile (M). They are different tiles.

## 3. Stock and buff brick

- **A wall-reflectance table** gives London stock 0.25, Fletton 0.30, light-grey brick 0.40, white gault 0.70 and blue engineering brick 0.15 (https://help.iesve.com/ve2021/appendix_a___tables.htm) (R). It cites no source, and it is an interior table: UNVERIFIED.
- **London samples (M).** B014, yellow/grey clay, "weathered, dusty": 0.362, linear (0.453, 0.351, 0.207). Whether it is a stock is not stated. B001, a yellow cement brick: 0.280.
- **Band.** Clean or weathered: 0.25 to 0.36.
- **Sooted, by the same film model (I).** 0.19 to 0.26 at f 0.3; 0.10 to 0.14 at f 0.7. London stocks were notoriously blackened, so 0.10 to 0.15 is the 1990 default (I).

## 4. Render

- **Painted, weathered (M).** B012, brick painted white, "weathered, rough": 0.515, linear (0.624, 0.499, 0.357), a dirty cream. B010, painted beige and grey: 0.497.
- **Fresh (R, no source given: UNVERIFIED).** White paint 0.75 to 0.85; light yellow 0.60 to 0.70; light plaster 0.40 to 0.45 (https://www.engineeringtoolbox.com/light-material-reflecting-factor-d_1842.html).
- **Pebble-dash.** No measurement was found.
  - Nearest proxy: London's quartzite-conglomerate road dressing, a bound aggregate, at 0.21 to 0.25 (M).
  - Inferred (I): unpainted 0.15 to 0.30; painted 0.40 to 0.55, below flat paint because the pebbles shadow one another.

## 5. Wetting

- **Rough solids.** Lekner and Dorf's model (in hand) loses 32 to 37% between 0.12 and 0.35.
- **Porous surfaces** darken more.
  - Sand loses 50% (Ångström, quoted there).
  - Engineering Toolbox lists sand at 0.38 to 0.42 dry and 0.22 to 0.28 wet (R, no source).
  - Wet concrete "0.10 to 0.20" and wet pervious concrete "about 0.15": search summaries only, UNVERIFIED.
- **Wet brick.** Isomi, Sakai and Watanabe 2020 (Trans. AIJ 85(777) 1367; https://www.jstage.jst.go.jp/article/aijs/85/777/85_1367/_article/-char/en): red brick changed most sharply within 5 minutes of drying (R, abstract only).
- **Used here (I).**
  - Above about 0.12: wet is 0.50 (porous) to 0.65 (rough) of dry.
  - Below 0.12: the upper end is Lekner and Dorf's table (0.75 at 0.08, 0.90 at 0.05).
  - Wet base colour: subtract about 0.02, the water film's own reflection.

## 6. Reference first

The Mafia and Kingdom Come II studies (aaa-reference, 05-visuals.md included) give no brick, pavement or render albedo. None found.

## Target bands

Each band is visible luminance reflectance, linear: measured total reflectance unless marked I.

| Surface | Dry | Example linear sRGB | Wet | Wet base colour | Source |
|---|---|---|---|---|---|
| Concrete flags, weathered | 0.21–0.37, centre 0.26 | (0.24, 0.21, 0.16) to (0.40, 0.37, 0.31) | 0.11–0.24 | 0.09–0.22 | Kotthaus; ECOSTRESS (M); wet I |
| Red brick, clean or weathered | 0.09–0.15 | (0.21, 0.07, 0.03) to (0.29, 0.12, 0.08) | 0.05–0.10 | 0.03–0.08 | ECOSTRESS; Kotthaus (M); wet I |
| Red brick, sooted, 1990 | 0.08–0.12 | (0.15, 0.07, 0.055) | 0.04–0.08 | 0.02–0.06 | film model (I) |
| Red brick, soot-blackened | 0.055–0.075 | (0.10, 0.06, 0.05) | 0.03–0.06 | 0.01–0.04 | film model (I) |
| Stock or buff, weathered | 0.25–0.36 | (0.45, 0.35, 0.21) | 0.13–0.23 | 0.11–0.21 | IESVE (unsourced); B014 (M) |
| Stock, sooted, 1990 | 0.10–0.15 | (0.16, 0.13, 0.09) | 0.05–0.10 | 0.03–0.08 | film model (I) |
| Painted render, weathered | 0.45–0.55 | (0.62, 0.50, 0.36) | rain only | | B010, B012 (M) |
| Painted render, fresh | 0.60–0.85 | | | | UNVERIFIED |
| Pebble-dash, bare or painted | 0.15–0.30 or 0.40–0.55 | | | | I |

- **Base colour (I).** Kotthaus's nadir view, with the lamps off axis, mostly misses the specular peak, so those values stand nearly as base colour. ECOSTRESS values are hemispherical, so take them 0.02 to 0.04 lower (review point 5).
- **8-bit sRGB base colours (M)**, material colours rather than frame pixels:
  - flags 134/126/112 to 169/163/151;
  - red brick 125/72/50 to 146/96/82;
  - stock 179/160/126;
  - weathered paint 207/187/161.

## Not reached or unverified

- **Refused by the server.** USGS splib07 (CloudFront 403). BRE Digest 310 and an IES floodlighting table (a bot check, not passed).
- **Paywalled or failed.**
  - Mansfield 1989, a London soiling thesis (403).
  - Beloin and Haynie 1975, brick soiling (paywalled).
  - The MDPI 2023 and Zhang 2015 pervious-concrete papers (403).
  - Uchida, Yamada and Makita on wet concrete (site under maintenance).
  - The full text of Isomi 2020 (transfer broke off).
- **Not read.** CIBSE LG10 and LG11, BS 8206-2, BR 209, CIE 94, Historic Scotland's stone-cleaning reports, Twomey et al. 1986.
- **Read, nothing usable.** Krupiński 2021: no brick table.
- **Unconfirmed.** The IESVE table's source. Whether B014 is a stock. Which concrete samples were flags. Whether the faces measured were the weathered ones.
- **Not found at all.** No soot-darkened brick or pebble-dash has been measured. Every band for them is inference.

## Revised after review (29 October 2026, 12:55)

A fresh reviewer (FLAGS-BRICK-BANDS-REVIEW-2026-10-29.md) passed this file with fixes, re-deriving its luminances within 0.001 and recomputing C004 and B004 in full. Its fixes stand here and win over the sections above where they differ:
1. **Red brick, clean or weathered: 0.09 to 0.21, centre 0.15**, not 0.09 to 0.15. Every London red clay brick sample reads 0.150 to 0.265, and B004 (Table C.1, "with cement") was kept while B013 was dropped for the same mortar; the sooted rows move up with it.
2. **The 1990 soot rows are provisional.** They use unequal film fractions (red 0.3, stock 0.7) on an unsourced claim; at 0.3 for both, sooted stock would read 0.19 to 0.26. Until a measured sooted brick is found, the soot rows guide by eye only and are not targets.
3. **Base colour for red brick: 0.02 to 0.04 below the table's sRGB examples**, by this file's own rule (hemispherical values include some specular).
4. **The stock band rests on one sample** (B014); treat it as a guide.
