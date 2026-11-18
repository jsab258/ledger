# Review: Kiln wrist, research in another direction (18 Nov 2026)

Reviewed file: production/research/lane/KILN-WRIST-ANOTHER-DIRECTION-2026-11-18.md
Checked against: CUFF-START-METHODS-2026-11-18.md, UNTANGLE-PRIMARY-AND-PATENTS-2026-11-18.md, and two cited pages fetched today (the Marvelous Designer arrangement page and the Huang et al. 2025 paper PDF).
Reviewer: fresh subagent, about 12 minutes, outside-only.

## Verdict: PASS WITH FIXES

The core finding holds and follows from the evidence: the cuff fault is one of topology (the arm outside the loop), and the working methods put the limb inside the ring before it closes (wrap at placement, or shrink the body and grow it back). The arithmetic and the patent dates are right. Several claims are stated more strongly than the sources allow, and step 5 of the recommendation works against the file's own main point. Two practical gaps matter for a custom XPBD draper.

## What was checked and is right

- Arithmetic: 191.6 / (2 x pi) = 30.49 mm, shown as 30.5. 219 / (2 x pi) = 34.86 mm, shown as 34.9. The ring at true size does start inside a round arm of that girth.
- Patent dates: US 6,970,171 filed 10 May 2001, granted 29 Nov 2005; US 7,355,600 a continuation, filed 24 Mar 2005, same earliest date. Twenty years from 10 May 2001 is 10 May 2021. Google's adjusted expiry 12 Aug 2022 is 459 days later (checked: 365 + 94 days). Both expired at end of term with fees paid. The file rightly says expiry is Google's computation, not a legal finding.
- Marvelous Designer page, fetched: "Patterns that the length are longer than the Bounding Volume, such as cuffs, get arranged spiral." Quote matches.
- Pixar patent summary (body has an inside cloth must leave, pinched cloth held still, closed paths only), Sun et al. 2016 arm-in-sleeve failure, GarmentCodeData 72% and "cuffs sticking out", CLOTH3D shape transition, Vellum Inflate Collisions: all match the source files.

## Fixes

1. Marvelous and CLO claim is overstated. The help page says only that patterns longer than the volume, such as cuffs, are arranged in a spiral. That a cuff "goes round the arm before any simulation" is the source file's own reading (marked SECONDARY there) but appears in the summary under "(primary, Marvelous help)". Mark it as a reading of the page; the page does not say the spiral closes a full ring.

2. Huang et al. 2025: the paper does not call the skeleton shrink a heuristic (checked in the PDF). It says the limbs "are surrounded by the corresponding sleeves or trouser legs at the beginning of the optimization" and makes no promise about the end. Reword to that. Also add two facts that limit transfer to Kiln: their garment is already a closed 3D garment from a source avatar (retargeting, not draping flat pieces), so the sleeve tube already exists; and their no-penetration guarantee comes from the IPC barrier with continuous collision, which an XPBD solver with discrete contact does not have. So B works for Kiln only after A, and only with slow growth.

3. "No professional tool or paper found tries to repair this with forces after the fact" is too strong. The whole untangling literature (Baraff, Witkin and Kass; Ye et al. 2017; Sun et al. 2016; Cha 2022) repairs tangles after the fact, including tangled starting states. Say instead that these methods are built for cloth against cloth or for small penetrations, and the one paper testing the arm-in-sleeve case (Sun et al.) names it as unsolved.

4. GarmentCodeData: "the jacket's fault is a known weakness of the method" is the source file's SECONDARY reading. The 72% is overall success, not a cuff rate, and "cuffs sticking out" is described as misalignment, not confirmed as the arm-outside-loop fault. Mark as a reading. "Best public dataset pipeline" is an opinion; drop or mark it.

5. Recommendation step 5 contradicts the file's main point. If the ring has closed beside the wrist, pushing cloth out from the capsule axis clears the penetration but leaves the arm outside the loop, which is the fault. It can only help where the ring already encloses the axis and merely dips into the skin. Say so, and stop attributing the radial push to Ye and Zhao: only their abstract was read, and the radial push is the helper's own "practical reading".

6. "No live patent blocks global intersection analysis" is broader than what was checked. Only the two GIA patents were checked. The related flypapering application (US 2002/0118197) and the pose-based flypapering patent US 8,436,861 were seen as titles only, status not checked. Say "the two global intersection analysis patents are expired; related Pixar flypapering patents were not checked".

7. Deflation amount assumes a round arm. The gap is 4.4 mm, not about 5 mm (fine as a rounding, but say 4.4). More important: a wrist is closer to an ellipse. For any convex cross-section, pulling the surface in uniformly by d shortens its girth by 2 x pi x d, so a 4.4 mm deflation makes the girth 191.6 mm whatever the shape; but a circular ring of radius 30.5 mm will not contain that deflated ellipse (for a 1.5 to 1 wrist of 219 mm girth the long half-axis is about 41 mm, still about 37 mm after deflation). So in step 1 the cuff should be wrapped onto the deflated limb's own cross-section (an offset of the limb surface), not onto a circle, or the body pulled in toward the bone (as Huang does) by more than the long half-axis minus the ring radius. Add this.

8. End state in tension is not discussed. If the 219 mm girth is right, the finished cuff is stretched about 14% over the arm. Woven nylon will not do that; a rib or elastic cuff would. In XPBD a stiff stretch constraint fighting body contact gives jitter or push-through at the end. Step 4 (measure the girth) should also check where the cuff should sit (wrist rather than forearm) and that the cuff material is set as stretchy. This belongs before any of steps 1 to 3.

9. Step 1 wrap rule needs the multi-panel case. The source formula maps one panel's width to the full circle. A jacket sleeve is often two pieces (top and under sleeve) plus a separate cuff tube. Each panel in a ring should take an angle in proportion to its share of the ring's total width at that height, with seams meeting at the joins. Also, "nearest body part" is ill-defined for pieces laid flat away from the body; assigning by the sewing links (cuff sewn to sleeve, sleeve sewn to armhole) is more reliable. Add both as notes to step 1.

10. Step 2 growth speed: give a number for the proof run, for example body growth per substep no larger than half the cloth thickness or collision margin, so discrete XPBD contact cannot tunnel. The file names the risk but leaves no limit to test against.

## Not faults

- The tries-rule paragraph is careful and correct: the lane makes no ask and leaves the judgment to the main session.
- The proof test (winding count of one round each limb axis at frame 0 and at the end, no cloth inside the body) is a good, general check and should stay.
