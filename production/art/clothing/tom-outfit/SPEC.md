# Tom's outfit: the specification (26 October 2026)

His order of 25 October, item 3, and his answer of 26 October: "start Tom's outfit to Study 6's target", made in Marvelous Designer on his own month (signed up 26 October; its licence read: production/research/game-clothing-pipeline/MD-LICENCE-2026-10-26.md).

## What he wears (his casting sheet, production/casting/tom-nowak/SHEET.md)

Day to day, the outfit the player sees most: **a zip-front cotton or nylon jacket for the rain, a plain jumper, jeans, leather shoes.** His one good suit (a plain dark two-piece, for the inheritance's business) is a second outfit, after this one passes. One suitcase: the same few things again and again.

## The body

MH_TomL1 (his face frozen 8 October), exported from the MetaHuman dressing project by tools/ue/export_dcc.py (geometry mode) into F:/LedgerTools/bodies/MH_TomL1/, in MetaHuman's reference pose, with its measurements (tools/meshgen/blender/body_measurements.py), as Ron's, Darren's and Sheila's were. It becomes the avatar in Marvelous Designer; no CLO avatar is used (its terms forbid shipping one).

## The target (Study 6, production/research/aaa-reference/studies/06-characters-wardrobe.md)

| Piece | Full-detail triangles | Textures | Moves |
|---|---|---|---|
| Zip jacket | 18,000 to 22,000 | 2048: colour and occlusion, normal, packed roughness | skinned; its hem on a short rigid chain at most, not cloth |
| Jumper | 15,000 to 20,000 (the piece to trim) | 2048 | skinned only |
| Jeans | 8,000 to 10,000 | 1024 to 2048 | skinned only |
| Shoes | about 6,000 | 512 to 1024 | rigid |

Four levels of detail at about 50%, 25% and 10%. Colour by material, not mesh: one layered garment material with tint, grime and wet values.

## The method

1. Patterns drawn in Marvelous Designer to his measurements (no CLO sample patterns, trims or buttons: our own), simulated on his body in the reference pose, its period details from the 1990 references (production/research/plain-1990-clothes).
2. Exported to our own files before the month ends (OBJ or FBX, quads, with the simulated folds), kept on F:/LedgerTools/garments/tom.
3. Brought to the target in Blender: topology to the triangle counts, folds baked into the normal map, UVs, textures.
4. Skinned to the MetaHuman skeleton: weights from his body, joints fixed by hand (the ruling of 30 September: garments are skinned meshes; only hems move).
5. Into Unreal on his body, the skin under each garment hidden.

## Accepted when

- It walks, stops, turns, sits and raises its arms in the game's camera with no clipping, holes or stiffness, judged by a fresh reviewer per view against RULINGS.md's clothing floor and the Hook sheet.
- Its counts and texture sizes are inside the table; its films and source files are recorded.
- No CLO avatar, sample, trim or AI feature went into it; every file exported before the month ends.

## State, 26 October

- Licence read (production/research/game-clothing-pipeline/MD-LICENCE-2026-10-26.md).
- His body exported (F:/LedgerTools/bodies/MH_TomL1: _Body.fbx, _FullBody.fbx) and measured: chest 1069, waist 885, hips 1042 mm, biceps 363, shoulder to shoulder 464, shoulder to wrist 612 (measurements.json; the neck to be taken from the full body).
- Marvelous Designer 2026.1 (Personal) is installed with its own Python 3.11; whether its script editor runs on this plan is checked when it is first opened.
- **The bridge into Marvelous** (his ruling: our own plug-in, his one click a session): tools/md-bridge, running since 26 October afternoon; its probe read Marvelous 2026.1.237's API (production/research/game-clothing-pipeline/MD-API-2026.1.237.json).
- **His body is the avatar:** imported at scale 10 (October's lesson: tools/md/jobs/grow_drape.py, production/research/clothing-pipeline/MD-AVATAR-ARRANGEMENT-2026-10-02.md), 109 arrangement points, 1.90 m; saved as F:/LedgerTools/garments/tom/MH_TomL1.avt for every later job. His neck, missing from the measurements, taken from it: 420 mm.
- **The first pattern begun:** FreeSewing's Brian block (MIT) drafted at his measurements (F:/LedgerTools/garments/tom/pattern/brian.json: back, front, sleeve), by October's drafter (tools/meshgen/freesewing_draft.mjs).
- **The zip jacket, first drapes (26 October, evening):** tools/md-bridge/zip_jacket.py cuts Brian at his size into the jacket's eleven pieces (two fronts, a whole back, two sleeves, rib bands at the hem in three parts, rib cuffs, a stand collar), places them on his arrangement points, sews its 25 seams by the API, drapes and exports (F:/LedgerTools/garments/tom/zip_jacket). Drape 1: the sleeves bunched at the elbow (each piece is centred on its point; the body pieces and sleeves started too high); drape 2, one point lower: a whole jacket, the cuffs onto the hands; drape 3 (production/previews/tom-zip-jacket-v3-2026-10-26.jpg): cotton twill and rib knit (only the cloth's physics, from Marvelous's stock library), the sleeves 40 mm shorter, a 10 mm mesh, 1,000 steps: a blouson bloused over its band.
- **The zip's tapes and the pockets' places, drape 4 (26 October, night; production/research/game-clothing-pipeline/ZIP-POCKETS-2026-10-26.md, step 1, after its fresh review):** two 12 mm tapes in a firmer canvas cloth at a 4 mm mesh, each the closure's whole length, sewn to the hem band's, the front's and the collar's front ends and to each other (the zip closed); the two hip welts' places written into the plan in pattern coordinates; 13 pieces, 29 seams, all sewn (production/previews/tom-zip-jacket-v4-2026-10-26.jpg). Next, per the review: the bake chain from tools/meshgen/blender/retopo_garment.py (finish_md_jacket.py is the tailored jacket's), the tape its own denser UV island, the ID mask packed into an existing map, about 10 to 16 hours.
- Next: the teeth, welts and stops built on the drape and baked; a fresh reviewer against 1990 references (production/research/plain-1990-clothes); then the game mesh, skinning and Tom in the game. Earlier note kept: the zip jacket's pieces from Brian (a zip front with its overlap, a hem band and cuffs in rib, a stand collar), as a job for October's chain (tools/md/make_jacket_job.py's format), arranged on his avatar's points, sewn, draped, exported; then finished and skinned in Blender (tools/md/finish_md_jacket.py, the skinning chain). Reuse first: production/research/clothing-pipeline holds the jacket, jumper and jeans research from September and October.
