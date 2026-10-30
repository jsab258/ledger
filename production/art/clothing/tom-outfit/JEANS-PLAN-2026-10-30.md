# Tom's jeans: the plan (30 October 2026)

His order C9: after the cuffs, the jumper, jeans and shoes by the game-garment skill. Reference first: Mafia's trousers (Study 6, production/research/aaa-reference/studies/06-characters-wardrobe.md: a median 9,566 triangles over 61 trousers at full detail, 5,396 to 23,022; textures mostly 1024; Kingdom Come II's hose 6,806) and the September research, read again today: production/research/clothing-pipeline/JEANS-2026-09-30.md (the seat, loops, pockets, hem), TROUSERS-AND-CAP-2026-09-29.md (the FreeSewing blocks) and SKINNING-TROUSERS-2026-09-29.md. How Mafia cuts and drapes its trousers was not read (none found); its numbers above are the target.

## The pattern

- **Block:** FreeSewing's Charlie (MIT; built on Titan, with belt loops and a fly; TROUSERS-AND-CAP: "use Charlie"), drafted by tools/meshgen/freesewing_draft.mjs at Tom's measures (F:/LedgerTools/bodies/MH_TomL1/measurements.json: waist 885 mm, seat 1,042, inseam 908, knee 399, cross seam 632, front 331, waist to floor 1,132). Charlie's leg runs straight down from the knee, which is the 1990 straight leg.
- **Ease:** seat about 8 to 10% over the seat's hull girth, knee about 20% (JEANS-2026-09-30, both I; a size-32 501 measures 42 in round the seat and 17.5 in at the knee, D). Charlie's own seat ease 5% and knee ease 15% are its defaults (TROUSERS-AND-CAP); the drafted seat and knee are measured against those targets before the drape and the option raised if short.
- **Drafted (30 October, 05:45; F:/LedgerTools/garments/tom/jeans/pattern/):** at Charlie's defaults the seat came out 1,094 mm round (+5% on his 1,042) and the knee 458 (+15%); at seatEase 9% and kneeEase 20% (charlie-jeans.json) the seat is 1,136 mm (44.7 in, +9%) and the knee 478 (18.8 in, +20%), on the plan's targets. The hem equals the knee (Charlie runs straight down from it): 478 mm, 18.8 in round, wider than the 501's 16 in (JEANS-2026-09-30, D [12]); the job tapers the outseam and inseam from the knee to a 16.5 in hem (419 mm), about 15 mm off each edge, Charlie having no hem option.
- **Pieces:** two fronts, two backs (each with its yoke as one piece at first; the yoke seam drawn in the normal map), the waistband in two halves; the fly, front pockets, back pockets, rivets and loops as baked detail at first, the loops modelled after the drape if the bake reads flat (JEANS-2026-09-30, 5: loops lie flat, 12 mm by 5 to 7 cm, about 2.5 to 3 mm thick; simulated loops jitter, so never simulated).
- **Length:** one soft break on the shoe; the hem a 2 to 3 cm band, several times stiffer in bending than the leg (JEANS-2026-09-30, 7). The shoes are not made yet, so the break is set against the floor at his heel and checked again with the shoes.

## The route

- **Drape:** Marvelous, on the straight avatar the jacket and jumper use, 20 mm particles while building, then 10 mm on the legs, 5 to 6 mm on the hem and waistband, Fitting last (the skill, step 3). Denim with buckling near nil (JEANS-2026-09-30 [22]). The seat on a smoothed collider if the drape sinks into the cleft (JEANS-2026-09-30, 1: the hull; Marvelous's own forum: change the avatar).
- **Under the jumper and jacket:** the waistband and seat are covered while he stands; seated, the back rises, so the waistband's top stays above the jumper's welt (checked in the sitting pose).
- **Game mesh:** about 9,600 triangles at LOD0 (Mafia's median), then 47, 25 and 9%; 1024 textures, cloth texel density checked against the skill's floor; denim twill as a tiling detail normal, not baked.
- **Weights:** the body's (skin_garment.py with the garment's recorded recipe, never retyped), checked per pose; the seat and crotch by SKINNING-TROUSERS's zones; 8 influences at LOD0 and LOD1, 4 below.

## The checks

The skill's, and beside them: the seat neither sinks into the cleft nor balloons (the September fault); the knee shows no latex-smooth tube and no frill at the hem; sitting, nothing passes through the bench or the body and the waistband stays shut at the back; walking, the hem does not pass through the shoes once they exist.

## The job (to write: tools/md-bridge/jeans.py, from tools/md-bridge/jumper.py's shape)

Charlie's front carries the fly extension and the slant pocket cut, and its back runs forward under the slant (its slantOut corner), with the pocket facing between them (charlie.frontPocketFacing). The first drape keeps that construction: front, back and facing per leg, mirrored, the facing sewn to the front's slant and to the back's extension, the fly sewn shut along the centre front; the waistband (charlie.waistband) sewn round the top. Placed on his avatar's own points (F:/LedgerTools/md-jobs/out/arrangement_points.json): the fronts on Leg_Front_R and _L, the backs on Leg_Back_R and _L, the waistband on Body_Front_Waist.

## Waiting on

The jumper's drape first (his order's sequence), then the jeans' job; both need Marvelous open (his ruling of 29 October: computer use only in Marvelous, after 10 minutes with no input).
