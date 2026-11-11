# Sheila's blouse carried and skinned to MH_LenaS4 (11 November 2026)

Step 1 of SHEILA-REFIT-PLAN-2026-11-09.md. Files in F:/LedgerTools/garments/sheila/blouse-s4-2026-11-11/ ("F:" below). Blender 5.2.2 headless. About 0.4 h.

## What was done, and the tries
- Source: F:/LedgerTools/garments/sheila_blouse/sheila_blouse.blend, object "CardiganRender" (the blouse; 40,732 triangles).
- Carry C1 to S4 (carry_garment.py, defaults): try 1 of 2, passed. Mean move 75.2 mm, 380 points pushed out, at most 5.7 mm (F:carry/carry.json).
- Skin (skin_garment.py --piece-attr none, S4's own Body.fbx): try 1 failed. bind_garment.py reduces anything over 40,000 triangles, and skin_garment.py then stops on the changed point count. Try 2: the blouse reduced to 39,600 triangles (19,810 points), surface moved at most 0.41 mm (F:reduced/), then skinned: passed.
- Out: **F:skinned/sheila_blouse_s4_skinned.fbx**.

## Checks
- skin.json: notButtons empty; uvReordered true; skirt rule touched 0 points (blouse foot 0.983 m, hips 0.892 m); 65 bones (F:skinned/skin.json).
- Triangles: 39,600 at LOD0, twice Tom's jumper (19,480); no lower LODs made.
- Body through cloth, points over 3 mm inside, counted by horizontal ray parity (my own script, F:scripts/parity_check.py; F:pose/parity-check.json): rest 71 (deepest 7.4 mm, the tucked foot's front at 0.99 m); arms down 1,044 (25.2 mm); walk 665 (20.6 mm); seated 880 (25.0 mm). Mostly cloth inside the lowered arms (718, 374, 607) or the trunk's sides, 1.1 to 1.3 m. **None is in the Shown region in any pose** (F:pose/regions.json).
- pose_skinned.py's sign test read 653 / 1,557 / 1,218 / 1,400 (about 93 mm deep): collar points off the body's open neck top, the known open-mesh fault (F:pose/pose-test.json).
- Head mesh (face DNA), at rest: 52 collar points inside it, 5 over 3 mm, deepest 3.5 mm, z 1.392 to 1.432 (F:pose/parity-check.json). Not cleared.

## Shown and Hidden (described only; nothing changed in the FBX or in Unreal)
Shown: the stand and flat collar, plus the front inside the cardigan's V (neck sides ±75 mm at z 1.439 down to mid-chest at z 1.23, 30 mm overlap under its band), two of five buttons: 7,910 triangles. Hidden: the rest, 31,690 (F:pose/shown-region.json). The V's low point is unverified (no cardigan yet).

## Colour
Already near-white cream (1.0, 0.96, 0.84 linear), but the material is named "M_KnitBeige": rename at import. Judge in the game's light.

## Tool changes described (not made)
- skin_garment.py should pass --tris to bind_garment.py, or name the cap when it stops.
- pose_skinned.py's inside test lies at open edges; parity would fix it.
