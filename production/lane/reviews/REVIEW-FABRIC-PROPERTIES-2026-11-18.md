# Review: Fabric properties from public sources (2026-11-18)

Reviewed file: production/research/lane/FABRIC-PROPERTIES-PUBLIC-2026-11-18.md
Reviewer: fresh subagent, 2026-11-18. Every source below was re-read by the reviewer on 2026-11-18 at the URL the file gives.

## Verdict: PASS WITH FIXES

The numbers that decisions rest on match their sources, and every conversion is arithmetically right. Five small fixes were made in the file. Nothing found would change a Kiln value.

## Claims checked

1. Clyde, Teran, Tamstorf 2017, Table 2 (CTT17.pdf): canvas 294.0 g/m2, 0.53 mm, 108 x 56; cotton poplin 103.6, 0.18, 140 x 86; silk 83.0, 0.18; wool twill 480.6, 1.28, 32 x 28; denim twill 400.0, 0.66, 70 x 47. All match. Fitted values are not printed in the paper, and it says nothing about data licence. Both match the file.
2. Wang, O'Brien, Ramamoorthi 2011, Table 1: all ten densities match. The ACM notice (personal or classroom copies free; commercial use or redistribution needs permission) matches. The paper gives no terms for the database, so the file's "not cleared" status is correct. Fix: Table 1 does not give the denim's weave, so "twill" was removed.
3. Penava, Simic Penava, Knezic 2014: masses, thicknesses and all twelve E values match. Warp is 90 degrees and weft 0 degrees, as the file says. The 5.69 N at 1.10% cotton weft point matches (Table 2, elastic range). No licence statement is printed, so the file's "licence not checked" is correct.
4. Kim and Son 2006: all weights, T0, EMT, B and G values for the three fabrics match. The weave is not stated, as the file says.
5. XPBD (Macklin, Mueller, Chentanez 2016): the following all match. Alpha is inverse stiffness. Alpha-tilde = alpha / dt^2. The delta-lambda update is Eq. 18. Gamma = alpha-tilde x beta-tilde / dt. Eq. 28 sets compliance to the inverse of the Lame stiffness matrix. The cantilever runs at dt 0.008 with 20 iterations. The chain uses alpha 1e-8. The 64 x 64 cloth runs at 20 to 160 iterations with no dt given.
6. Arithmetic, checked in Python:
   - Penava Y = E x thickness: cotton 3,955 / 10,354 / 261, wool 4,629 / 12,416 / 97, polyester 2,942 / 1,298 / 120 N/m. All correct.
   - Low-load cross-check: 10,345 N/m and 113.8 N/m. Correct.
   - KES B conversion: 9.807e-5 N m, and wool 0.0593 gives 5.82e-6. Correct.
   - KES G conversion: 0.9807 N/m per degree = 56.19 N/m per radian, and 0.61 gives 34.3. Correct.
   - Ramaiah weight: 12.52 mg/cm2 = 125.2 g/m2. Correct, and the units are still marked unverified.
   - Fix: the file said bias was "20 to 50 times" lower than warp or weft. The data give about 10 to 130 times, so the line was corrected with the per-fabric ratios.
7. Houdini manual pages:
   - "A good starting point for clothing is 5 substeps" and the 0.01 thickness warning: match.
   - Smoothing default ten, collision passes 10, constraint iterations set by the geometry's diameter: match.
   - Default cloth density 0.1 with no units, and the "varying" mass mode: match.
   - Fix: added the solver page's note that its default substeps "can be very aggressive", with 2 or 5 suggested for cloth that is too stretchy.
8. Marvelous Designer: gravity "Default is -9800" with no unit printed, and time step defaults recommended. Matches.
9. CLO:
   - "The default value of the Particle Distance is 20": matches.
   - 20 mm for making a garment, under 5 mm for the finished garment, range 0.8 to 700: matches.
   - Fix: noted that the first page prints no unit for its 20.
10. Licences:
    - Wang 2011: as checked in item 2.
    - Clyde 2017: the paper states no licence. Correctly noted.
    - Miguel 2012: the paper was not reached. The file lists it as unreached and draws no numbers or terms from it. Correct.
11. Marking:
    - Unverified items are labelled: the nylon retailer weight, the Ramaiah units, the KES 500 gf/cm load, and Houdini's metre unit.
    - The bending (discrete-shell) and grid-edge formulas are clearly labelled as derived and not confirmed in a source.
    - Unreached sources are listed in section 5 and are not used as evidence.

## Fixes made in the file

- Added a one-line plain summary at the top.
- Wang denim: removed "twill" (not in Table 1).
- Bias-to-warp/weft ratio corrected from 20 to 50 to about 10 to 130.
- Houdini solver: added the default-substeps note.
- CLO: noted that one page prints no unit for its particle distance.
- Searched for em-dashes, en-dashes and italics: none found.

## Open (not reviewer errors, carried from the file)

- The Wang 2011 database terms, the Miguel 2012 paper and the Clyde 2017 supplement have not been read.
- The KES-FB1 maximum load and the discrete-shell bending constant still need a primary source before any number is locked.
- Stiffness for denim, nylon taffeta, melton and rib remains a gap.
- The reviewer read only the first 100,000 of 150,000 characters of the Houdini Vellum Solver page.
