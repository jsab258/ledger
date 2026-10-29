# Review: flags, brick and render bands (29 October 2026)

A fresh reviewer's check of FLAGS-BRICK-BANDS-2026-10-29.md. Read 29 October 2026: the Kotthaus paper in full with Table C.1, the SLUM file, twelve ECOSTRESS files, the CIE tables, the IESVE and Engineering Toolbox pages, Isomi's abstract. Data and paper were read in memory over plain HTTP, before the web-fetch-only rule arrived; nothing was saved. M measured, R read, I inferred.

**Verdict: PASS WITH FIXES.** Every luminance and colour re-derives to the third decimal. The faults lie in which samples set the bands, and in labels.

## Faults

1. Red brick sits below London's own bricks: B004 0.150, B013 0.210, B011 0.263, B008 0.265, against two American bricks at 0.093 and 0.098. B013 is dropped for mortar, yet Table C.1 lists B004 "with cement" too. *Fix:* widen to 0.09–0.21, centre about 0.15, or justify the exclusions; redo the soot rows (f 0.3: 0.08–0.16; f 0.7: 0.055–0.09).
2. physicallybased.info's 0.128 sits unmarked in the brick table and sets the centre. *Fix:* mark it UNVERIFIED; take the centre from measured samples.
3. The 1990 soot defaults use different films: red brick f 0.3, stock f 0.7, on the unsourced "notoriously blackened". Stock at f 0.3 is 0.19–0.26; f 0.7 gives 0.10–0.14, not 0.15. *Fix:* one f for both, or name rows by f; tag the claim I.
4. The stock band has one measured sample, B014 (0.362). B001 is a new cement brick, not a stock; IESVE's 0.25 is unsourced. *Fix:* tag the band I.
5. "Measured total reflectance" fits ECOSTRESS only; Kotthaus states his spectra are not hemispherical. *Fix:* label each source's geometry.
6. The 8-bit "base colours" are dry reflectances unchanged; red brick 125/72/50 is ECOSTRESS, which the file's own rule lowers by 0.02 to 0.04. *Fix:* call them reflectance, or apply the rule (on red brick it strips most green and blue: test it lit first).
7. Engineering Toolbox's sand keeps 0.52 to 0.74 of dry, midpoint 0.62: the rough figure. The porous 0.50 rests on Ångström's single pair. *Fix:* say so.
8. The black alkyd paints are gloss, so their 0.04 is mostly surface reflection. *Fix:* cite the matte cinders (0.041) alone; soot's base colour is nearer 0.01 to 0.02 (I).
9. C005 is cement in Table C.1, like C001 and C003. *Fix:* label it.
10. Flags: text 0.21 to 0.38, table 0.21–0.37. *Fix:* one figure.
11. G002 and G003 are "granite with cement"; nothing calls them kerbs, and weathered G004 (0.525) is left out. *Fix:* drop "kerbs" or add G004.
12. Painted render rests on painted brick (B010 0.497, B012 0.515) and is widened beyond them. *Fix:* tag I.
13. The red "sooted" colour is f 0.5 (Y 0.085), not the row's f 0.3. *Fix:* give f 0.3's colour.
14. Engineering Toolbox does not say its values are visible; its one definition is solar. *Fix:* say units unstated.
15. Render's 0.45–0.85 lies outside C6's plaster pass range (median 0.09 to 0.36, MAFIA-WEAR-2026-10-28.md). *Fix:* reconcile before C6 runs.
16. Labels: 0424 is "slightly soiled", not weathered; ECOSTRESS samples belong to the National Photographic Interpretation Center, measured at JHU; the quartzite is new; "points 4 and 7" should read revision item 4 and review points 6 and 7. *Fix:* correct them.
17. Unlisted leads (search summaries only, UNVERIFIED): Brimblecombe and Grossi 2005 on blackening; Watt, Jarrett and Hamilton 2008 on London reflectance loss. Either could set f. *Fix:* list them.

## Confirmed (R)

- Kotthaus: 74 London samples; nadir view, two lamps, Spectralon; albedo solar-weighted (ASTM G173). Lamp angles are not given, so "off axis" is I. C004 0.37, B004 0.31.
- ECOSTRESS: directional hemispherical; 0092, 0424 and the paints start at 420 nm.
- IESVE, Engineering Toolbox: numbers as quoted, unsourced. Isomi: abstract only, no ratios.
- Wet and soot cells re-derive; wet, soot and pebble-dash are marked I or UNVERIFIED. Section 6 holds.

## Re-measured (M)

CIE 1931 2°, D65, 1 nm, 380 to 780 nm. White point x 0.3127, y 0.3291. Σ S·ȳ = 10,567.05.

- **C004.** Σ R·S·ȳ = 3,914.84; Y = 3,914.84 / 10,567.05 = 0.370. By band (weight × mean R): 0.031×0.321 + 0.224×0.351 + 0.459×0.373 + 0.244×0.387 + 0.042×0.390 = 0.0099 + 0.0786 + 0.1710 + 0.0945 + 0.0165 = 0.3705.
- **B004.** Σ = 1,585.21; Y = 0.150. By band: 0.0028 + 0.0218 + 0.0590 + 0.0548 + 0.0116 = 0.1500. The solar 0.31 is double.
- **Checks.** Both unchanged at 10 nm; 0092 zeroed below 420 nm: 0.3325 (held flat 0.3326).
- **The rest** match to ±0.001: C001 to C008, B001, B010, B012 to B014, S001, S003, S005, G002, G003, 0598, 0092, 0424, 0097, 0412, 0413, 0101, 0402 to 0406. Roof tiles 0.077 to 0.116 (new 0.173); quartzite 0.206 to 0.253; 8-bit colours as quoted; medians: flags 0.258, red brick 0.128.
