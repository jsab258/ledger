# Ron's work trousers (the clothing session, 29 September): SET ASIDE

CLOTHES.md item 4, the first half. Ron's casting sheet: "dark grey work trousers; scuffed black leather boots". The references: production/reference/work-trousers-and-flat-cap-1990.md (Peter Fryer's Smith's Dock, 1990 to 1991); the research: production/research/clothing-pipeline/TROUSERS-AND-CAP-2026-09-29.md.

## The pattern

FreeSewing's Titan (MIT), at the settings of Charlie, the trouser built on it (Charlie's own front is cut away for its slanted pocket, which a sewn simulation cannot take; its pocket, fly and belt loops are placed from its draft instead). Ron's measurements (production/art/clothing/donkey-jacket-sewn/ron-measurements.json): seat 1185, seatBack 611, waist 1079, waistBack 488, waistToSeat 170, waistToUpperLeg 254, waistToKnee 599, waistToFloor 1142, crossSeam 748, crossSeamFront 391, knee 434, waistToHips 170. Options: knee to the knee (fitKnee), kneeEase 30% (Charlie's widest: 564 mm, straight to the hem), seatEase 7%, crotchDrop 4%, waistHeight 38% (the band's top 11 cm under his natural waist at the sides), waistAngle 15 degrees (the front 2 cm lower, under the belly; the back higher), lengthBonus -3% (the hem 3 cm off the floor, for a boot). Drafts: F:/LedgerTools/tmp/clothes/trousers (titan-ron-v4.json, charlie-ron-v2.json).

## How it is made (tools/meshgen/blender)

- sew_trousers.py: each row of the pattern laid round the body at its height, the ease that makes its length the pattern's width; the crotch seams down the body's own middle line to under the middle of the legs; below the ankle a circle of the pattern's width, lifted over the foot; the thighs parted 8 mm each for the collider (tailor.part_thighs: Ron's touch for 8 cm under the crotch).
- Sewn by projection, not by Blender's cloth (tailor.relax): each round every edge towards its pattern length, every seam towards shut, the waist held, the body kept out. Blender's sewing slid the trousers to the knees (nothing held them) and, held, pulled the legs up the calves; Blender's cloth, settling, let them through the body at the fly, a hip and a buttock. By projection every seam closes to 11 mm in 100 rounds, nothing inside the body.
- Welded, then settled by projection with a small step down each round (twelve length rounds a step, or the cloth stretches 8% and the hems reach the floor), pressed (tailor.press), the seat's hollows bridged (tailor.bridge_slices), the hems smoothed (tailor.smooth_edges_of).
- finish_trousers.py: the waistband (34 mm) above the top edge all round, a black belt through seven flat loops, a plain buckle, the fly shield (11 cm), Charlie's slanted front pockets, a welt on each back, worn creases (three soft folds behind each knee, the knees bagged, a fold above the hem); one render mesh (about 45,000 triangles), no simulation mesh: close trousers are skinned in games (the research).
- pose_trousers.py: skinned to his body walking, sitting and with a foot up a stair: the body's weights (each side on its own leg), smoothed; the belt, band and loops take the trousers' own weights, so they never part from the cloth.

## Reviews

- review-1.md: FAIL (the waist opening sitting, the body through the seat on the stair, ragged hems, thin and clean).
- review-2.md: FAIL (sitting, the stair, the hems cinching, the belt folding: all in the skinned poses).
- review-3.md: FAIL after the research (the skinned poses again). SET ASIDE under the two-tries rule, 29 September.
