# Sheila step 0: the body (11 November 2026)

Extraction for step 0 of SHEILA-REFIT-PLAN-2026-11-09.md. Files in F:/LedgerTools/garments/sheila/step0-2026-11-11/ (results.json, meas_C1.json, meas_S4.json, scripts). Blender 5.2.2 headless; no Unreal.

## 1. Files, and which one the game builds
- Body files: F:/LedgerTools/bodies/MH_LenaC1/MH_LenaC1_Body.fbx and MH_LenaS4/MH_LenaS4_Body.fbx (each with FullBody.fbx and measurements.json), from bodies/README.md.
- **MH_LenaS4/measurements.json is a copy of C1's** (its "body" field names the C1 file; chest 863.8, hips 930.6). The README says so ("measurements copied") but S4's body is a different body (below). Those numbers are not hers.
- Game side: C:/LedgerTools/mh-assemble/Content/Ledger/MetaHumans/MH_LenaS4/Body/SKM_MH_LenaS4_BodyMesh_DNA.uasset (3 Oct) has mesh 0 identical (0.0 mm, 30,455 points) to the same file in F:/LedgerTools/mh-dress. Its extents (top 1.413 m, x +-0.493) match MH_LenaS4_Body.fbx (1.413, +-0.493); C1's (approved-cast-2026-09-25, 30,455 points) matches the C1 FBX (1.496, +-0.514). So the S4 FBX is the built S4 body. Source: results.json.
- Unverified: that the street's Lena class (street-people.json line 82: /Game/Ledger/MetaHumans/MH_Lena/BP_MH_Lena) is the S4 build. The folder MH_Lena in mh-assemble (older take, 24 Sep) has a body top of 1.298 m, a third body. grep of DECISIONS.md for "Optimized" and "body_full_layout" found no match (Grep tool and grep).

## 2. Point count
- C1 FBX LOD0: 32,334 points (60,816 faces). S4 FBX LOD0: 32,334 (60,816). Men's: 32,334. Same LOD sizes (8,568; 3,974; 1,239). Not an Optimized (cut) build; body_full_layout.py not needed. Source: dump.py output.

## 3. C1 to S4 per point (shared order; LOD0, mm)
- All: mean 56.4, 95th 77.3, max 90.2; no identical point (0 of 32,334).
- Pelvis band 0.85-1.05 m: mean 70.4 (p95 75.1, max 79.5). Chest 1.25-1.45 m: mean 75.9. Thigh 0.50-0.85 m: mean 58.8.
- Worse than Darren's 37 mean / 64 at the pelvis. S4 is 83 mm shorter (body top 1.413 vs 1.496 m). A carry from C1 to S4 is needed; the C1 garments do not fit S4 as they are. Point order shared was assumed from equal counts and checked only by the distances being small (unverified by UV).

## 4. Her measures, S4 body (tools/meshgen/blender/body_measurements.py: tape girth round the convex torso slice, joints from the skeleton), mm; C1 beside
- Body top (neck join) 1413 (C1 1496); head mesh top 1685 (see 5), so standing height about 1685 (unverified: face DNA frame assumed equal to the body's). The plan's 1.50 m and the casting sheet should be checked against this.
- Chest 795.2 (C1 865.2 in this run); waist 813.9 (824.3); hips/seat 920.4 (963.8; the README's 931 is a copied number); waist to seat 150; inseam 793; waist to knee 544; waist to floor 1003; neck 476.9. Landmark heights S4: chest 1.233, waist 1.002, hips 0.852 m. Source: meas_S4.json, meas_C1.json.

## 5. Head
- Face DNA read headlessly with dna_mesh.py: C:/LedgerTools/mh-assemble/.../MH_LenaS4/Face/SKM_MH_LenaS4_FaceMesh_DNA.uasset, mesh 0 (11,977 points): lowest point 1.327 m, 1st percentile 1.364 m, top 1.685 m. The lower edge is 86 mm under the body's top edge (1.413): the overlap into the chest the plan warns of.

## Not reached
Which class the game spawns for her; UV check of point order; the casting sheet's height.
