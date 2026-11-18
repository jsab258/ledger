# Review: cloth remesh/untangle and strain-limit order notes

Date: 2026-11-18. Fresh reviewer, about 20 minutes. Files reviewed:
- production/research/lane/CLOTH-REMESH-AND-UNTANGLE-2026-11-18.md
- production/research/lane/STRAIN-LIMIT-ORDER-2026-11-18.md

## Verdict: PASS WITH FIXES

Every decision-bearing quotation checked was found in its cited source. The stated orders of operations for Narain 2012, Müller 2012, Wang 2010 and Bridson 2002 match the papers. The fixes below were small: one quote assigned to the wrong Vellum page, one paraphrase that read as a quote, one inference shown as a source statement, one overstated ARCSim timing rule, and unmarked estimates. The recommendations follow from the evidence.

## Claims checked (all read 2026-11-18)

1. Narain 2012 order and limitation (strain file s.1; remesh file s.1). Confirmed verbatim: "We perform strain limiting once at every time step before performing collision resolution"; "not aware of self-collision constraints"; "Collision resolution may thus cause the cloth to violate the strain limits in colliding regions." Remesh claims also confirmed: "can cause the cloth to penetrate obstacles or itself"; the face is moved back to where it "came from" using its pre-remesh displacement, with impact zones; new-vertex velocity "interpolated halfway"; position by minimising a generalised quadric error metric; collapse refusal conditions. One overstatement: "remeshing between collision passes, never in the middle of one". The paper says "remeshing must be performed between collision detection intervals" when continuous collision detection is used. Fixed.
2. Bridson 2003 inside-body handling (remesh file s.2). Confirmed: relaxation velocity toward the zero isocontour; a monotone map into [epsilon, tau]; "caught in between two body parts", not post-processed; per-part fields merged by the minimum. Confirmed.
3. Bridson 2002 order (strain file s.1). The note had not re-read it. The reviewer read it: strain limiting on velocities (Section 4) feeds the candidate velocities, and repulsions, collisions and impact zones follow (Section 5). "Collisions last" holds. Source link and date added.
4. Wang 2010 (strain file s.1). Confirmed verbatim: "We process boundary conditions simultaneously with strain limiting"; "projected back to the solid surface"; "enforcing one set of constraints does not cause the other to be violated"; self-collision "once every 64 iterations"; dragon about -60 percent against a [-5, 5] percent limit; 0.38 to 16.67 s per frame; collision detection 0.5 to 6 s. Confirmed.
5. Müller 2012 LRA (strain file s.1). Confirmed: Algorithm 1 runs local constraints, then LRA, then "apply collision and other constraints"; 3 to 5 iterations per frame; "get activated only when cloth is stretched"; Jacobi averaging; "less than 2% of overall simulation cost". Confirmed.
6. Houdini Vellum (both files). The solver node page confirms "interleaved between the constraint iterations", "After all constraints are performed, a final round of collision detection is done", "number of stacked layers + 2" and "Since collisions always pre-empt constraints, the result is cloth or hair stretching". The protrusions sentence and the "50 iterations and 5 collisions" example are on the vellumtips page, not the node page. Both pages are cited, so this is acceptable. "Protrusions" means cloth pushed out in the shape of the collider, not "local spikes". Fixed. The paneling/draping quotes (rest lengths reset, stitch-then-weld, Weld Frame Delay, Inflate Collisions, T-pose) and the intersect page (collider self-intersection leaves cloth "no where to go"; soft pins plus thickening) were confirmed.
7. Wētā Loki supplement (strain file s.1). Confirmed verbatim: "can invalidate collision resolution and lead to penetrations"; "the collision pass is unaware of the edge shrinking process"; "iterate between these passes until convergence"; "unify the constraints into a single solvable system". The authors match. Note that the source discusses an FEM edge-shrinking step, which the note applies by analogy to Kiln's edge repair. The analogy is reasonable.
8. Supporting quotes. Bender and Bayer 2008: all three quotes were confirmed. Magnenat-Thalmann and Volino 2005: the drape-recompute, refined-mesh, "millimeter collision thickness" and seams quotes were confirmed. "5 mm" is paraphrased from "Practical geometric accuracy is roughly limited by using 5-mm elements". Pixar Clean Cloth "armpits, chins, and elbows" and Minor 2018 "0.1s to 0.2s ... 30000 vertex mesh" were confirmed. Marvelous Designer arrangement points: the spiral "such as cuffs" was confirmed, but the "follow that volume's curves" quote was not verbatim. Replaced with the page's words. The Auto Sewing page does not say bands are wrapped before sewing. That sentence is now marked as an inference.

## Other checks

- Unreached sources: each file lists them. They are not used as evidence (Baraff 2003, Volino 2006, Ye 2012/2017, Goldenthal 2007, Thomaszewski 2009 and C-IPC are marked abstract-only or unverified). Where they are relied on, it is only for method shape, and the notes say so.
- Numbers: one unsourced number was found, a wrist radius of 25 to 35 mm. It is now marked as an estimate. The hour sizes in both files are now marked as estimates. Thresholds such as K = 8, tolerance 0.02, 30 mm and 1.2 times are presented as suggested checks, which is acceptable.
- Hour estimates: these look reasonable for an AI coder with existing tests. Remesh transfer is 4 to 6 h, signed-distance contact with side history 6 to 8 h, band wrapping 6 to 8 h, and the closing loop 6 to 10 h, broken down into parts. The cloth-cloth untangle at 2 to 4 days is plausible, and it is correctly placed last.
- Recommendations: both follow from the evidence. The strain note's Option B is the interleaved loop, ending on an outward-only push with contact points weighted heavy. Wang, Bender and Bayer, Vellum and Loki's first option support it. The remesh note's first two methods map directly to ARCSim's undo-displacement fix and to Bridson's signed-distance treatment.
- Style: no em-dashes or italics in either file. Neither file had a plain-English line for a non-programmer, so one plain summary line was added at the top of each.

## Fixes made

- Remesh file: added a plain summary line; corrected the ARCSim remesh-timing sentence; marked the wrist radius as an estimate; replaced the Marvelous Designer arrangement quote with the page's wording; marked the Auto Sewing sentence as an inference; marked the hours as estimates.
- Strain file: added a plain summary line; attached a source and read date to Bridson 2002 and stated its order; corrected the protrusions quote and its page, and reworded "spikes" to bulges; marked the smoothing pass as untested; marked all sizes as estimates; updated the unreached list.

## Left open

- Pixar global intersection analysis patents (US 6970171, US 7355600): expiry status is still unchecked. Check it before any implementation of method 6.
- Progressive Dynamics 2024 shell prolongation, and how it avoids penetration at transfer, remain unverified.
- XRTailor licence is still unchecked. The note already forbids taking its code.
- The frame-42 diagnosis (nearest-face push throwing points across the wrist) is a hypothesis. It needs the per-point push direction logged at frame 42, as the note says.
