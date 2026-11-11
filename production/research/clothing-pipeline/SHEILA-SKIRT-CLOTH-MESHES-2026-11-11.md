# Sheila's skirt: cloth route step 1, the meshes (11 November 2026)

First step of SHEILA-SKIRT-CLOTH-ROUTE-2026-11-11.md only. Blender 5.2.2 headless, one script run in the end (two earlier tries of the sampling fixed; no fault left). Files in F:/LedgerTools/garments/sheila/skirt-cloth-2026-11-11/ ("F:"); no Unreal, nothing in git.

## Made
- F:sheila_skirt_static.fbx: the render mesh, rest pose, no armature, same 39,600 triangles as the skinned file (the reduced S4 skirt; its own detail kept).
- F:sheila_skirt_skinned.fbx: the chain's skinned file (skirt-s4-2026-11-11/skinned), copied unchanged.
- F:sheila_skirt_sim.fbx: static single-layer simulation mesh, no skin (the route's separate `_sim.fbx`).
- F:make_skirt_cloth_meshes.py, F:sheila_skirt_meshes.json, F:skirt-meshes-front.png and -side.png (render mesh grey, simulation mesh orange with wire).
- Names follow make_cloth_garment.py's NAME_static / NAME_skinned (NAME = sheila_skirt).

## Method
The simulation mesh samples the outer surface by rays from outside toward the skirt's axis: 24 around by 10 rows (11 rings), then joined as one tube.

## Measured
- Triangles: render 39,600 (19,800 points); simulation 480 (264 points).
- Largest distance from the render surface: 12.9 mm (sampled 36 points per triangle); mean 1.3, 95th percentile 5.2 mm; the 264 corners within 1.3 mm.
- Single layer: one connected piece, 0 non-manifold edges, Euler characteristic 0, exactly two boundary rings (48 edges): top and hem. No inner shell.
- Rings: top (waistband) at 100.0 cm, hem at 41.1 cm. Both sit 8 mm inside the render's edges (top 100.8, hem 40.3 cm), because the band lip is ragged.
- Hip line: the body's hip joints, 89.2 cm (the skin step's hip line, 0.892 m). The top ring is 10.8 cm above it, skinned.
- LEDGER_GARMENT_FREE: `89.2,40.3,<simMaxDistance>`: skinned above 89.2 cm, free to 40.3 cm at the hem (span 48.9 cm); the last value was not set here. The route's "931 mm" is the hip girth, not a height.

## Notes
- The simulation hem ring is at 41.1 cm; the free height may use 41.1 if the script wants the ring, not the render hem.
- Pictures judged by eye only; the render band's ragged top edge shows (known open fault).
