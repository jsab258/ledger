# Bollards (kit piece 3.4): build notes

11 October 2026, cloud week 42, built by the coordinating session from `production/cloud-week/targets/bollards/target.json` (kinds K1 to K6) with the first review's fixes (below) as the only departures: `build_bollards.py` (about 20 s), `check_bollards.py` (58 of 58 in `checks/check_v1.json`), `make_row.py` (a review aid: the six side by side, scratch only) and `render_bollards.py` (the two review views).

**Built** (each a solid of revolution, 64 sides, from the target's `profile_rz`, pivot the axis at the ground, z up): K1 the cast-iron domed street bollard (1081.7 high; the yard mouth), K2 the plain tapered iron bollard with its collar band and rolled foot ring (1049.6; the quay-end junction), K3 the round precast concrete bollard (850), K4 the steel tube bollard with its welded cap (1000; black by default, `--paint galvanised` for the dull zinc), K5 the bolted cast-iron chain post (1135, with its four hex nuts and studs on the 124 pitch circle at 45, 135, 225 and 315 degrees and two pairs of chain lugs with their eyes at z 420 and 840), K6 the quay mooring bollard (720). Materials: `paint_black` (24, 24, 26, the target's roughness), `concrete` (152, 150, 144, 0.9) for K3, `galvanised_steel` for K4 on request, `bare_steel` for the studs. Each .glb under 220 KB; the largest K5 at 6,272 triangles.

**Not built:** K7 (the horn cleat) and K5's chain (the quay's, not Quay Street's); the conditions (worn foot, chalk, rust at the foot, scuffs): the engine's masks; K1's second casting (BGE_a, not a model by the target's rule).

**Judgement:** K2's foot diameter 250 is the rolled ring's widest point (r 124.99 at z 11), not the radius at the ground (119 at z 0); the lug's D shape is a rectangle 40 x 55 with the eye (24) bored through, the target gives no outline for it (error +-30 per cent). The flat disc under each foot closes the solid at z 0.

## After the first review (REVIEW-v1-street.md, FAIL on one fault; try 2, 12 October)

The street view failed the piece on K6's head (the kit's raw polyline lathed unchanged: hard creases where the target says "soften into R10 or more, then a dome") and left five narrow points. Try 2 applies them, as named departures in `build_bollards.py` (`k6_profile`, `k5_profile`, `fillet`, `kind_profile`; the check reads `kind_profile`, so it checks the profile that was built, and compares it with the target's raw profile within 22 mm):

1. **K6** (fault 1): the rim's three corners (210, 590), (220, 630), (200, 670) become one bull-nose arc (centre r 158.3, z 624.2, radius 61.9); the top one dome of radius 425 centred on the axis at z 295 (within 4.5 mm of the target's point (110, 710)); R20 fillets at the barrel's shoulder (150, 470), (130, 510), the neck (130, 550) and the join to the rim; R10 on the flange (250, 40), (190, 60), (170, 80); R5 on its foot edge; every arc sampled at 12 degrees or less. 8,192 triangles.
2. **K5** (narrow point 1): the flange has a flat seat at z 42 (r 139 to 108) in place of the slope, then a cove to (100, 52), (95, 70), (91, 100); the four nuts stand on it (z 41.5 to 56) with their studs to z 70; check: each nut's underside at z 41.5 +-1.
3. **K5 lugs** (narrow point 2): cast D lugs: 55 high at the shaft, tapering to 36 at the eye's centre (22 from the shaft face), closed by a half-round of radius 18 about the eye (still 40 proud, a 6 mm wall round the 24 eye), edges eased 2 mm.
4. **K2b and K6b** (narrow point 3, now built): K2b the smaller tapered post with the low cone cap (950 high, the target's `profiles_final.US02_a`), K6b the upturned cannon with its muzzle swell and ball (982 high, its R6 corners rounded).
5. **Not modelled** (narrow point 4): K3's two mould lines and its pour line at z 400, K4's vertical weld seam and 2 mm cap weld bead: the engine's normal maps. **For the target** (narrow point 5): on the 1979 working quay at Ramsey the chain posts are thin plain painted steel tubes; K5's bolted, beaded cast post is the later marina type, as the target's section 11 says.

Eight models now (K1, K2, K2b, K3, K4, K5, K6, K6b), each under 270 KB; check 73 of 73 (`checks/check_v1.json`, overwritten by try 2). The second review is of the close view (K5's foot, its nuts and lugs).

## After the second review (REVIEW-v2-close.md, FAIL on one fault; fixes applied, not re-reviewed)

The close view of K5's foot failed the piece on one fault, the target's: the lower bead is built as the target draws it (a soft swelling 120 high and 14 proud that fades into the shaft), where LH_b's full-size panorama, re-projected and measured row by row, shows a full, nearly elliptical roll about 78 high and 18 proud with definite corners to the shaft, a quirk and a fillet ring. Two tries are spent; by Jafar's ruling of 9 October the review's exact fix is applied and the unit marked done "fixes applied, not re-reviewed":

1. **K5's lower bead** (`k5_profile`): the target's nine points (91, 278) to (90, 398) replaced by the review's elliptical roll (centre (88, 330), 21 x 40) to (109, 330), then the quirk (98.5, 364.6), (96, 365.5), the fillet ring to (96, 370) and a short cove to (90, 377.5); the bead now z 290 to 378. The target's own text and checks still describe the old bead: the review wrote them as changes to the target (`lower_bead` part and moulding), which are not applied here (no more target polishing).
2. **Narrow points applied:** the nuts are `bare_steel` (the target and LH_b), with the top corners chamfered 1.5; the studs 14 across (radius 7) with a 1.5 chamfer at the end; a washer 28 across and 2.5 thick under each nut on the seat (the nut and stud raised 2.5); the lugs' edges eased R3.
3. **Not applied:** the R6 fillet where each lug meets the shaft, and the 1.5 mm chamfers on the eyes' mouths (a boolean union with the shaft; for the engine's normal map).

Check 77 of 77 (`checks/check_v1.json`). K5 8,144 triangles, 288 KB.
