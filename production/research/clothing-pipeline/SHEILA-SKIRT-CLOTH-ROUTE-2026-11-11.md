# Sheila's skirt as Chaos cloth in the packaged game: the cheapest route (11 November 2026)

Follows DECISIONS 11 Nov 11:28 (route 3 of SHEILA-SKIRT-S4). Code and engine files read 11 Nov 2026 (engine: C:/Program Files/Epic Games/UE_5.8). Nothing was run.

## 1. What stops it today
- LedgerGarments.h:321-326 loads only a `USkeletalMesh` at `Garments/<Name>/SKM_<Name>`. make_cloth_garment.py makes a `UChaosClothAsset`, which is not one, so the row would log "NOT worn". Line 328 makes only a skeletal mesh component.
- make_cloth_garment.py:38 writes to `/Game/Ledger/Cloth/` in mh-dress. The build machine copies only mh-assemble's `Content/Ledger/MetaHumans` (ledger-probe-unreal.yml:393-396).
- A cloth path exists: LedgerJacket.h:87-146 `WearCloth` (cloth component following the body, per-slot materials, the body's physics asset as collision). Only the portrait tool calls it (MetaHumanPortrait.cpp:274). The suit jacket proved it in the editor (suit-jacket-ingame-2026-10-01/README.md), never in a packaged build.

## 2. Smallest change set (estimates, unverified)
1. **Meshes in Blender (1.0 h).** A static copy of the skinned skirt, and a coarse single-layer simulation mesh (outer layer only, a few hundred triangles). Kingdom Come II's skirt simulates through a 270-triangle proxy; Mafia runs 5 skirts at 2 iterations (studies/06, lines 45 and 50). The suit jacket tore when its whole mesh simulated (README line 26).
2. **make_cloth_garment.py (1.0 h).** Root folder from the environment, aimed at `/Game/Ledger/MetaHumans/Garments/SheilaSkirt/`; no timestamp in the DF_/CA_ names (lines 256-257), so the path stays fixed; a separate `_sim.fbx` for StaticMesh_SIM (line 268); the mh-assemble body path; a brown colour. Unverified: whether Epic's template has a ProxyDeformer node to drive the render mesh from a different simulation mesh (ClothAsset.h:251).
3. **Run in mh-assemble (1.5 h, two runs).** Free heights set from her hips (931 mm); cloth-garment.txt read.
4. **C++ (2.0 h, game target built first).** A row field `"cloth": "CA_SheilaSkirt"` sends the row to `LedgerJacket::WearCloth` in place of line 322, its `hides` and `Covered` still applied; the component named per garment; `ForceNextUpdateTeleportAndReset` (ClothComponent.h:124-125) when the game moves her.
5. **Row and import (0.5 h).** A garments.json row with the skinned FBX, `"hides": ["lower"]`, `"cloth"` and `"hold"`. import_garments.py still makes SKM_SheilaSkirt (the weight transfer's source; satisfies garments_shipped_check.py), not drawn for a cloth row. garments.json is already staged (stage_game_data.py:39): no new staging.
6. **Held packaged film and review (1.5 h).**

Total about 7.5 h.

## 3. Seated
- The game stands her today: "Sheila behind the counter" has no `"seated"` field (mickeys-office.json:60); only Ron's bench mark has one (line 64).
- Collision is not the physics asset alone: `SetCollideWithEnvironment` (ClothComponent.h:221) gathers the simple shapes (box, sphere, convex) of overlapping WorldStatic components, at most 32 per body (EnvironmentalCollisions.cpp:25-50, 85, 107). A chair with simple collision can hold the cloth if max distance at the back is about 30 cm or more (the drop is 303 mm). The office chair's collision: unverified.
- Cheap fallback: `GetClothOutfitInteractor` (ClothComponent.h:189), then `SetWeightedFloatPropertyValue("MaxDistance", -1, (0,0))` (ClothAssetInteractor.h:77; name from PBDSphericalConstraint.h:111). Radius is base plus range times weight (line 128), so 0 pins the cloth to its skinned shape. Trigger from `SeatPerson` (CrimeProbe.cpp:7895). It stops jitter but brings back route 1's back through the chair. Runtime effect unverified.
- Mafia's and Kingdom Come II's seated skirts: not found in study 06; their files not opened (unreached).

## 4. Risks
- Cloth has never run packaged here. Unverified: the cooked asset and the ChaosClothAssetEngine module in the packaged game; whether mh-assemble has the cloth plugins (neither MetaHuman project lists them).
- The two-layer shell under a proxy may let the inner layer cross the outer. The ragged band top stays open.
- Walking thigh pass-through (1,274 points) relies on her body's physics asset, unverified.
- Each regeneration leaves assets in the copied folder.
- Sitting has used its two tries. This route is the one researched new method on record.

## 5. Recommendation
Reuse WearCloth: build into mh-assemble's Garments folder, add a `"cloth"` row field and the C++ branch, use a coarse single-layer simulation mesh, film it held. Leave seated aside while her mark stands. If a seated mark comes, try chair collision first, with pinning as the fallback.
