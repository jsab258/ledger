Method researched: N16-4-TARGET-2026-11-16.md checked against N16-4-READING-2026-11-16.md, TERRACE-KIT-TABLE-2026-10-29, BRICK-COLOUR-2026-10-08, MAFIA-KIT-2026-10-28, studies/04-street-world.md, RECS-BY-PHASE-2026-11-06, PIECES-DRAFT-2026-11-08, orders/archive/2026-11-02.md, DECISIONS archive 3 Nov, review.json of 11 Nov, vignette-scene.json, previews d6 and d7. All read 16 Nov 2026.

# Fresh review: N16-4 target (16 Nov 2026)

**Verdict: PASS WITH FIXES.** The sources are cited honestly and most numbers trace end to end. Three faults need fixing before any check is built: the colour space is mixed up, the dark-header distribution test contradicts itself, and the street-ends ray fan misses the vanishing point on the two morning cameras. A few smaller points are listed too.

## Claims checked end to end

| # | Claim in target | Source line | Finding |
|---|---|---|---|
| 1 | Course pitch 86 mm ± 3; 85.0 and 86.9 on Levenshulme 1994; reviewer 85-87; brick + perpend 216-224 | TERRACE-KIT-TABLE line 33 ("85 to 88 mm: 85.0 on the upper wall, 86.9 beside the door; the reviewer ... 85 to 87. Brick plus joint 216 to 224"); kit grid 75 mm at line 67 | **Supported.** "One photograph" is correctly stated, as is the M confidence. The photograph is 1994, outside the 1988-92 window, but it is used only for brick size, so that is acceptable. |
| 2 | 11 Nov tile 75-80 mm | review.json ("course pitch is about 14-15 px against a door about 380 px high, so about 75-80 mm") | **Supported.** |
| 3 | Joint width 8-10 mm, confidence H | READING B5: buildingconservation "0.3 inches (8mm)" for Victorian machine-pressed bricks; Designing Buildings "typically 10 mm" | **Overstated (confidence only).** The 8 mm figure is for pressed facing bricks, and 10 mm is a modern general figure. No period terrace was measured. M is the right confidence. The 7-11 mm band itself is reasonable. |
| 4 | Dark headers about 8% of the Hook sheet's near-wall pixels against our 0.8% | orders/archive/2026-11-02.md line 267; DECISIONS 3 Nov 20:31 ("0.8% of its pixels against 8%") | **Supported.** |
| 5 | Dark-header share 20-35% of headers = about 7-12% of brick face | Arithmetic: header face 102.5 / (215 + 102.5) = 0.32 of brick area. 0.20-0.35 x 0.32 = 6.5-11.3%. The sheet's 8% of pixels (mortar included) works out to about 25-30% of headers. | **Supported as inference.** The arithmetic holds and L confidence is stated. The source is concept art plus a by-eye "many, not all". |
| 6 | Dark headers 0.45-0.70 of stretcher luminance | P Hull 1986 by eye; Wikipedia "grey-blue" | **Overstated.** No measurement exists. The L tag is present, but the band reads as a pass/fail bar. It should be marked provisional until d7 is measured (open question 3). |
| 7 | Mortar sRGB 115-170 = linear about 0.17-0.40 | Arithmetic: sRGB 115 gives linear 0.171; sRGB 170 gives 0.402 | **Supported (conversion correct).** The band itself is inference (I, L, stated). Reviewer's rough pixel read of d7 (Hull 1986), uncalibrated JPEG: mortar median sRGB about 165/146/133, luminance about 149, inside the band. Mortar saturation measured about 0.20, above the target's ≤ 0.15 (d6 also about 0.22; JPEG bleed from bricks is likely). |
| 8 | Mortar lighter than brick by luminance ratio 1.3-2.5 | P by eye; I | **Ambiguous.** The ratio's space is not named. On d7 the ratio is 1.55 in sRGB values and about 2.6 in linear, so the same photograph passes or fails depending on the space. Against albedo brick 0.26/0.095/0.061 (luminance 0.128), the mortar band 0.17-0.40 implies ratios of 1.3-3.1, so the band and the ratio only partly agree. |
| 9 | Stretcher "near-wall frame mean ±10% of 0.37/0.19/0.13 **linear**" and hue 12-18° | review.json: "near-wall mean RGB about 0.30/0.14/0.11 against 0.37/0.19/0.13 today", with no space given. BRICK-COLOUR line 9: Hook sheet Mickey's wall 91/53/40 sRGB, S 0.56, hue 15° (confirmed: hue 15.3°, S 0.56). | **Wrong label and internal conflict.** review.json does not say "linear". Read as display values, 0.37/0.19/0.13 = 94/48/33, close to the sheet's 91/53/40, so it is most likely sRGB. Taken as linear, as the target says, it is sRGB 164/121/101, hue 18.8°, which fails the target's own 12-18° band even though the row says it is "not faulted for hue". The albedo 0.26/0.095/0.061 (physicallybased.info, linear) has hue 14.7° in sRGB but 10.3° when computed on linear values. The row mixes spaces. |
| 10 | Width = 2 x (3.0 + 0.125 + 2.0) = 10.250 m; channel inside the carriageway (starts at 2.745) | vignette-scene.json street.carriageway.half_width_m 3.0, kerb.width_m 0.125, footway.width_m 2.0, channel.width_m 0.255 (3.0 - 0.255 = 2.745); cam_hook note "the channel starts at 2.745"; studies/04 line 57 "10.25 m"; line 83 "5.125 m either side" | **Supported.** Note: the blocks in the file carry no frontage z, so "front to front" is inferred from the road cross-section, which assumes the facade stands at the back of the footway. The check should state that assumption, or read placed fronts once they exist. |
| 11 | Camera yaws cam_A 0, cam_hook 20.4, cam_reverse 200.4; road "runs past" the blocks | vignette-scene.json cameras (yaw_deg); street.length_note "the road runs past them at both ends"; length 48.0 | **Supported.** |
| 12 | Mafia: world noise 31% of plaster placements, swaps 22%, wear geometry 28% of storey bands, corner/quoin 3 meshes 176 placements | MAFIA-KIT lines 117, 85/118, 120, 44 | **Supported.** |
| 13 | Mafia street: 18-19 facade pieces, 2 families, about 150 meshes, about 2,350 placements, about 15 uses, **88% kit** | studies/04 line 29 (measured street: 2,350 / 150 / 15 / 18-19 / 2 families); line 28 (88% kit belongs to the **whole main-street group**, about 100 buildings) | **Overstated / misattributed.** The 88% is not a figure for the measured street. |
| 14 | Arris arithmetic: 0.17 px/mm at 10 m, 0.34 at 5 m (1440 px, 46°) | 2 x 10 x tan 23° = 8.49 m, and 1440 / 8,490 = 0.170 | **Supported.** |
| 15 | RECS lines 66, 106, 111; PIECES-DRAFT lines 42, 58, 62, 139 | Read: s04-04, s04-01 "No check found", s04-06 "open"; Flemish "Reference: none found. Guess 4 to 8 h"; checks 3-5 h; shells step 3 | **Supported.** |
| 16 | Hull 1986 (d7): Flemish, headers duller in places, pale grey-cream mortar near flush; Hull 1982 (d6): headers barely darker, pale mortar | Previews looked at full size | **Supported by eye.** Both are tight crops (540 x 900, 480 x 912) of single doorways, which is a small sample for a "share" judgement. |

## Numbers presented as more certain than their sources allow

- Joint width H should be M (row 3).
- Dark-header darkness 0.45-0.70 and gloss roughness 0.05-0.12 are tagged L and U but written as pass bands. They should be labelled provisional until the d7 pixel measure is done.
- The target says "no pixel measure was possible in this run", but a rough PIL read of d6 and d7 took this reviewer a few seconds. The measure should be done before the bands are fixed. The mortar saturation ≤ 0.15 in particular is already in doubt (about 0.20 measured, uncalibrated).
- The "88% kit" figure is attributed to the wrong scope (row 13).

## Testability of the three checks

**Width (a): testable.** It has a pass case (today's file, 10.250 m), two fail cases (7.250 and 16.250 m), a boundary case and a missing-field case. Its only gap is the frontage assumption in row 10.

**Kit reuse (b): testable in form, but the pass fixture is not shown to pass.**
- In TERRACE-KIT-TABLE section 4, house C's gable (#9) appears once. Under "no kit mesh used once unless flagged", the A/B/C pass fixture fails unless the gable is flagged.
- Uses per mesh for three houses is not worked out against the bar of 4.
- "Becomes failing once the shells step starts" names no trigger the tool can read. Nothing in a file switches the result from a printed notice to a failure.

**Street ends (c): two faults in the design.**
1. The ray fan is "the central ±10° of the view", but cam_hook and cam_reverse are turned 20.4° off the street axis. The street's vanishing point lies outside that fan (the sheet's vanishing point is 478 px right of centre). The rays would hit the parade facades and pass without ever testing the end of the street. The fan should be centred on the street axis and clipped to the frame.
2. The pass fixture places a closer "across the road at x 50", but the rule requires the closer to be hit "before the road's modelled end", which is x 48 in this file. As written, the pass fixture breaks its own rule.

The picture half (a box of at most 20% sky pixels plus a fresh reviewer) is testable.

**Dark-header distribution (brick table): contradictory as written.**
1. A 1 m window holds about 35 headers (11.6 courses x about 3 headers per metre). At a share of 0.27, pure random placement already gives a standard deviation of about 7.5 points, so "s.d. ≥ 8" barely separates clustered from uniform.
2. The clustering asked for (patches of 0.5-2 m) raises the dark share among a dark header's diagonal neighbours above the overall share. That can break the "within ±8 points" anti-chequer rule. The two requirements pull against each other.

The fault named in review.json was near-regular spacing. That is better tested by the absence of a periodic peak in the dark-header map's autocorrelation, with clustering judged as a variance ratio against the binomial expectation.

## Reference-first rule

**Honoured.** The wall method copies Mafia's (world noise, swaps, wear geometry, corner pieces, MAFIA-KIT cited). The brick-specific method says "none found" for Mafia. Kingdom Come II is given as "none found (its material talks unreached)". Strictly, an unreached source is "not reached", not "none found", and the wording should say so. The checks take Mafia's and Kingdom Come II's measured numbers from studies/04 and say where they fit only in kind. The try count is honestly left as U.

## Fixes (one line each)

1. Name the colour space for every colour number: relabel review.json's 0.37/0.19/0.13 (most likely display sRGB, not linear) and make the hue band and the frame-mean band agree.
2. Name the space (sRGB or linear) of the mortar-to-brick luminance ratio, and reconcile it with the mortar albedo band.
3. Replace the dark-header distribution test: no periodic autocorrelation peak for the anti-grid part, and a variance ratio above the binomial expectation for clustering; drop the diagonal-share rule, which conflicts with clustering.
4. Street ends: centre the ray fan on the street axis (clipped to the frame), not the view centre, and put the pass fixture's closer at or before the road's modelled end.
5. Kit reuse: work the A/B/C fixture's numbers against the bars (gable #9 used once, uses per mesh against 4), and name the file or flag that turns "no placement spec" into a failure.
6. Move Mafia's 88% kit share to its true scope (the main-street group of about 100 buildings, not the measured street).
7. Joint width confidence H to M; mark dark-header darkness and gloss bands provisional until d7 is measured, and run that PIL measure (it is possible now; mortar saturation already reads about 0.20 against ≤ 0.15).
8. Width check: state that the facade line is taken as the back of the footway (blocks carry no frontage z).
9. Kingdom Come II brick method: "not reached" rather than "none found".
