# Kiln: the nylon jacket's wrist, research in another direction

Written by the cloud lane, 18 Nov 2026, 06:16 to 06:45 (Swiss time). Machine-free research only. For the main session, after the wrist tangle was set aside at 06:13 following three routes (two engine fixes, then re-cutting the jacket to the game's body, which cleared most cloth from the body but not the wrist and opened a new seam gap).

Detail and every source, dated and marked primary or secondary:
- CUFF-START-METHODS-2026-11-18.md (how professional tools and published pipelines get a narrow cuff onto its limb at the start).
- UNTANGLE-PRIMARY-AND-PATENTS-2026-11-18.md (the classic untangling methods against a body, the Pixar patents' status, open code).
Earlier lane note this builds on: CLOTH-REMESH-AND-UNTANGLE-2026-11-18.md.

## Questions asked

1. How do professional garment tools and published draping pipelines put a sleeve end or rib cuff that is narrower than its limb round the limb at frame 0?
2. What do the classic untangling methods do when cloth is tangled with a solid body (not with itself), and at an open edge such as a hem?
3. Are Pixar's global intersection analysis patents still in force?

## What the research says, in plain words

- The fault is one of shape, not of force. Once the cuff closes beside the wrist instead of round it, the arm is outside the loop, and no stiffness, rest length or seam pull can bring it back in. That is why fixes inside the solver keep failing. Published untangling methods do repair tangles with moves after the fact, but for this exact shape Sun et al. 2016 name "an arm pushed into a sleeve" as unsolved; no placement workflow found relies on repairing it afterwards.
- Every working method makes sure the arm is inside the loop before the loop closes, in one of two ways:
  A. Wrap first. Marvelous Designer and CLO place pattern pieces by wrapping them round cylinders that run joint to joint along each limb; their help pages say pieces longer than the cylinder, "such as cuffs", are "arranged spiral" (primary, Marvelous help, read 18 Nov 2026). That the cuff therefore goes round the arm before simulation is the lane's reading of that line, not the page's words. A 2016 dissertation and US patent 9820519 do the same: "any garment can be abstracted as a number of cylinders".
  B. Shrink the body, then grow it back. Houdini's Vellum Drape documents "Inflate Collisions": start the body slightly deflated and inflate it over set frames to get a drape free of tangles (primary, SideFX docs). Huang et al., SIGGRAPH 2025, shrink the avatar onto its bones so limbs sit inside the sleeves, then inflate it back (primary, their paper). Their garment is already a closed 3D garment, and their solver (IPC-type, with continuous collision on every step) keeps it free of penetration; Kiln's XPBD has no such guarantee, so the growth must be slow and tested (see step 2). CLOTH3D grows the body shape over frames for the same reason.
- Shrinking the cloth from an enlarged start (rest length ramps: Vellum, Maya, Blender, Marvelous Shrinkage) only tightens a loop that already goes round the limb. Alone it is the route that has already failed here.
- The best public dataset pipeline, GarmentCodeData, places pieces flat beside the body and reports about 72% success; one named failure is "cuffs sticking out" (primary, arXiv 2405.17609v3). The 72% is overall success, not a cuff rate; the lane's reading is that flat placement plus sewing can lose cuffs even in published work, so the jacket's fault may be a weakness of the method rather than a Kiln bug alone.
- The numbers here: a closed cuff of 191.6 mm has a radius of 30.5 mm; a forearm of about 219 mm (still unverified) has 34.9 mm. The gap in radius is 4.4 mm, assuming a round arm; the wrist is closer to an ellipse. Wrapped at its true size the cuff would start inside the arm, so wrapping alone is not enough; it needs B (or the enlarged start) as well. A 191.6 mm cuff on a 219 mm arm ends about 14% stretched, which a rib knit can take and a woven nylon cannot.
- Untangling against a body: the Pixar patent US 6,970,171 (the Baraff, Witkin and Kass method, read in full) treats a body as having an inside cloth must always leave, holds cloth pinched between body parts still, and covers only closed intersection paths; open edges such as a hem are not covered. Sun et al. 2016 name "an arm pushed into a sleeve" as a case pushing along the body's surface direction cannot solve. Ye and Zhao 2012 extend contour minimisation to a mesh against a capsule, the usual forearm stand-in (abstract only). Full texts of the four classic papers were not reachable; see the detail file.
- Patents: US 6,970,171 (filed 10 May 2001) and US 7,355,600 (its continuation) are both expired at the end of their term, all fees paid (Google Patents, read 18 Nov 2026; expiry is Google's computation, not a legal finding). The earlier note's "check before implementing" is answered for global intersection analysis. The separate flypapering patents (US 2002/0118197, US 8,436,861) were not checked; check them before building flypapering.

## Recommended direction for the main session (one general rule, no special cases)

0. First, check the cuff itself: where it should sit on the arm (the landing girth, still unverified at 219 mm) and that its fabric is a stretch rib able to take about 14% at that girth. If the cuff is wider than the limb plus gap, step 1 alone may be enough; if the fabric cannot stretch, the pattern is the fault, not the drape.
1. Wrap at placement: assign each tube's pieces to a limb by their sewing links (sleeve to armhole, cuff to sleeve end), falling back to the body part nearest most of their points, and wrap them round that limb's axis (joint to joint), sharing the full circle between the pieces of a two-piece sleeve and a separate cuff in proportion to their widths, so the closing seams meet at frame 0. Wrap onto the shrunken limb's own cross-section (step 2), not a perfect circle. This puts the arm inside every sleeve ring by construction. Rough size: small to medium.
2. Grow the body: start the body collider pulled in toward its bones (or deflated by at least the gap between limb and ring radius plus cloth thickness, about 5 mm plus thickness for this cuff) and grow it back slowly over many frames with collision on, so the limb cannot slip through. A limit to test against: the body surface moves at most half the cloth's collision thickness per substep. Rough size: medium; the risk is tunnelling if the growth is fast.
3. Fallback if 2 is hard in Kiln: wrap at the larger of the true radius and the limb radius plus clearance, set rest lengths to the placed size, then ramp them down to true size.
4. Not recommended as a fix for this fault: pushing cloth out after the ring has closed beside the wrist (from body faces or from a capsule's axis) leaves the arm outside the ring; it is only a clean-up for small leftovers once steps 1 and 2 hold. Global intersection analysis is free to use, but it is for cloth against cloth and ignores open edges.

How this sits with the tries rule: the three spent routes were all repairs after a bad first frame. Wrapping at placement and growing the body change how a garment is put on, for every garment, so the main session may judge it a new method rather than a fourth try of the old fix; if it judges it a further try of the same item, it needs his yes first (CLAUDE.md), and this file is the research to put beside that ask. The lane makes no ask itself.

What would count as proof: winding count of every sleeve ring round its limb axis equal to one at frame 0 and at the end, on the nylon jacket and on the held-back garments' sleeves and trouser legs, with no cloth inside the body at the end.

## Unreached (never used as evidence)

Full texts of Baraff, Witkin, Kass 2003; Volino and Magnenat-Thalmann 2006; Ye and Zhao 2012; Ye et al. 2017. Optitex placement help (login), Style3D and Browzwear placement pages (not found), Fuhrmann et al. full paper (abstract only), the licences of XRTailor and ContourCraft code (not reached). Details in the two source files.
