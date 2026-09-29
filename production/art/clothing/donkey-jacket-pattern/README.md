# Ron's donkey jacket, cut from a pattern (from 29 September)

The route recommended to Jafar after the skin-shell jacket was set aside (../donkey-jacket-2026-09-29/review-3.md), carried on while he decides: production/research/clothing-pipeline/pattern-jacket-2026-09-29.md. FreeSewing (MIT) drafts a real pattern to Ron's own measurements; Blender sews and drapes it round his body; Unreal's cloth takes it as before.

Step 1, done: Ron's measurements taken off his exported body (tools/meshgen/blender/body_measurements.py; ron-measurements.json): chest 1231 mm, waist 1079, hips 1156, neck 442, biceps 442, wrist 217, shoulder to shoulder 446, shoulder to wrist 636, HPS to bust 333, HPS to waist (back) 471, waist to armpit 321, waist to hips 120. The shoulder slope reads 1 degree in his rest pose (the arms raise the shoulders), so the draft takes FreeSewing's usual 13 degrees for a man standing.

Drafted (tools/meshgen/freesewing_draft.mjs, which now takes the design's options as opt.NAME=VALUE):
- brian-ron.json: Brian (the menswear block, straight side seams) with chestEase 20% (the box clears his belly), lengthBonus 45% (the back 857 mm from the shoulder's high point, about 84 cm from the collar seam: the references' 81 to 90), bicepsEase 25%, cuffEase 60%: back 369 x 857 mm on the fold, front the same, the sleeve 636 mm long, 539 mm round the top, a shirt-flat cap (a dropped shoulder, as a work jacket's).
- simon-ron.json: Simon, for its collar and stand only (collarAngle 110, collarWidth 160%): the fall 439 x 79 mm, the stand 479 x 45 mm, near Brian's 466 mm neckline.

Next: the pieces cut (the back on the fold, two fronts each 4 cm over the centre for the overlap, two sleeves; the collar later, the solid collar on his upper back meanwhile), meshed flat at 10 mm with the flat layout kept as the cloth's rest shape, placed round him, sewn and draped; then the simulation and render meshes for Unreal.
