# Sheila's skirt carried and skinned to MH_LenaS4 (11 November 2026)

Step 2 of SHEILA-REFIT-PLAN-2026-11-09.md. Files in F:/LedgerTools/garments/sheila/skirt-s4-2026-11-11/ ("F:"). Blender 5.2.2 headless. About 0.3 h.

## Done, and tries
- Source: sheila_skirt.blend, "SkirtRender" (57,344 triangles; a 2.46 mm shell, point i outer, i+13,568 inner).
- Carry C1 to S4: try 1 passed; mean move 61.3 mm, at most 4.7 mm pushed (F:carry/carry.json).
- Clear over the skinned blouse: try 1 turned the band top inside out (74 faces flipped). Try 2 (F:scripts/shell_follow.py: inner layer follows the outer): 3 flips left. **Open fault: the band's top front is ragged**, neighbours pushed -2.6 to +12.5 mm, worst edge 3.1 to 14.2 mm (F:clear2/compare.json). Two tries spent. Hidden by a cardigan: unverified.
- Reduced to 39,600 triangles for the binder's cap (moved at most 0.085 mm); skin_garment.py --piece-attr none --skirt-from 0 --skirt-pelvis 0.7: try 1 ran clean.
- Out: **F:skinned/sheila_skirt_s4_skinned.fbx** (19,800 points, 39,600 triangles, no lower LODs).

## Checks (F:skinned/skin.json; F:pose/parity-check.json, seat-drop.json, pictures)
- notButtons empty; uvReordered false, correctly (one UV layer, "pattern", already first); 24 bones.
- Points over 3 mm inside the body (ray parity): rest 0. Walking 1,274 (deepest 40.5 mm): the forward thigh through the front (a hole in the picture), the back calf through the back hem. Seated (tailor's sit, 85 degrees; the game's own angle unverified): 197, deepest 15.8 mm, 126 the thighs at the hip fold.
- Seated hem: the front lies over the lap to the knees (z 0.966); knees show, as they should. **Back and sides hang straight down: 4,022 points (20%) below the seat (0.784 m), the back hem 303 mm below it**, through the chair.

## The known 29 September fault, skinned
Routes (costs estimated, unverified):
1. Skinned, the desk hiding it: 0 h build, about 1 h to film her seat's views; the walking hole and the back through the chair stay visible from behind or the side.
2. Flap joints (Mafia's coat, about 20): extra bones and an animation graph on the garment in LedgerGarments; about 6 to 10 h, a path no garment row has.
3. Chaos cloth via code: make_cloth_garment.py writes to mh-dress, rows draw skinned meshes only; about 8 to 12 h, and the chair is outside cloth's collision.
None chosen.

## Tool changes described (not made)
- clear_layers.py should move a shell's two layers together.
- skin_garment.py should pass --tris to the binder.
