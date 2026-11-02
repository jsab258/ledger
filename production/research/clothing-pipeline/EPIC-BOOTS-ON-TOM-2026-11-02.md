# Epic's boots on Tom by script (2 November 2026)

Read 2 November: UE 5.8 source here (SDK = Engine/Plugins/MetaHuman/MetaHumanSDK/Source/MetaHumanSDKEditor/Private; MHC = Engine/Plugins/MetaHuman/MetaHumanCharacter/Source); the package's two lists; this PC's run of 24 September (F:/LedgerTools/mh-dress: fab-clothes.json, fab-closure.txt, ue-material.txt); Epic [E1][E2]. D read or measured, I inference, U unverified.

Questions: (1) installing from Python, and where; (2) wardrobe and fit; (3) the build's result; (4) the game; (5) steps, risks.

## 1. Installing (D)

- The importer is a factory, `UMetaHumanPackageFactory`, for ".mhpkg" (SDK/Import/MetaHumanPackageFactory.cpp 37, 45-48). No UFUNCTION or subsystem: `UMetaHumanAssetManager::ImportArchive` is plain C++ and refuses clothing (SDK/ProjectUtilities/MetaHumanAssetManager.cpp 763-768). An `unreal.AssetImportTask` on the file finds the factory by extension: this PC imported oa_boots so on 24 September in 33 s (fab-clothes.json). The class is wrapped for Python, UFactory having BlueprintReadWrite fields (Factory.h 334-335; PyGenUtil.cpp 1627-1645, 1769-1772); its Python name untried (U).
- The assets land under the import's destination folder (PackageFactory.cpp 233-240), each FileList.json entry copied as a file (SDK/Import/MetaHumanImport.cpp 455-499). A folder other than the source, /Game/Outfits/Boots, gets redirects and every asset re-saved (220-254, 359). So `destination_path="/Game/Outfits/Boots"` keeps Epic's paths. Epic: drag the file "into the ... folder" [E1]; Fab's Add To Project uses /Game/Fab/MetaHumans [E2], which this project refuses (make_cast_metahumans.py NOAI_ROOTS; attribution-check.py 887-891).
- Needs the Chaos Outfit Asset editor (PackageFactory.cpp 189-194), loaded with the MetaHuman Creator plugin (MetaHumanCharacter.uplugin 125). Its summary window (301-314) did not stop September's run.
- Precaution (I): a `destination_name` other than oa_boots, which matches OA_Boots in that folder but for case.

## 2. Wardrobe and fit (D)

- No shoes slot: Outfits (several at once, hidden from the UI), Top and Bottom Garment (both into Outfits), SkeletalMesh (MHC/MetaHumanDefaultPipeline/Private/MetaHumanDefaultPipelineBase.cpp 16-19, 112-134); Outfits takes a Chaos Outfit Asset (MHC/MetaHumanDefaultEditorPipeline/Private/MetaHumanDefaultEditorPipelineBase.cpp 276-287).
- As hidden_faces.py's `wear()` (394-418): `try_add_item_from_wardrobe_item("Outfits", WI_OA_Boots)` (MetaHumanCharacterPalette.h 93-94), then `try_add_slot_selection` (MetaHumanInstance.h 224-225), his two default garments kept. Done here on 24 September: Rocco dressed "WI_OA_Sweater,WI_OA_Jeans,WI_OA_Boots", built Optimized High in 110 s (ue-material.txt lines 1, 5).
- Fitted: the build resizes the outfit onto his merged head and body from the nearest of four source sizes, weights transferred from it (EditorPipelineBase.cpp 466-499, 1590-1610; Item/MetaHumanOutfitEditorPipeline.cpp 61-131, 221-227).

## 3. The built result

- A separate skeletal mesh, not merged, not simulated (D): baked "because Outfits can't yet be cooked" (OutfitEditorPipeline.cpp 141-153), render vertices only (ChaosClothAssetTools/.../SkeletalMeshConverter.cpp 55-65), saved as MH_TomL1/Clothing/MH_TomL1_Outfits_N (EditorPipelineBase.cpp 2084-2105), a component following the body (MetaHumanDefaultEditorPipelineLegacy.cpp 366-399). Only the editor preview simulates. Manifest: bPhysics false.
- Levels: the cloth asset's (SkeletalMeshConverter.cpp 27); its 16 static meshes are four sizes by LOD0-3, so four (I).
- Feet: the item has no body hidden-face map (the Manifest's warning; MetaHumanCharacterTypesVerification.cpp 44-73); a mask, f_bodymask_shs_boots, ships unused. Tom's game build already cuts lower legs and feet (HIDDEN-FACES-2026-10-30.md).
- Triangles: not in the lists. lod0VertCount 49,104 is the last skeletal mesh's (MetaHumanAssetManager.cpp 254-268), and the only ones are the four CombinedSkelMesh bodies (fab-clothes.json): a body's count (D). Measured after the build (U).
- It references the package's material and textures (27 packages in September, fab-closure.txt): the game needs them.

## 4. The game

- Now (D): TomBoots is our mesh following the body (LedgerGarments.h 296-309), hiding "shoes", any outfit part under 25 cm (369-376, 448-453); raise 17 mm; contact decals from sole_footprints.py's footprints (118-148).
- Through the wardrobe: TomBoots held, or its "shoes" would hide Epic's ankle boot (I). A hold also drops the soles and raise, laid only after the mesh loads (283-302, 457-465): a code change, an entry with no mesh that still lays them. LayContact spares only the body and LedgerGarment_ parts (142-145): add Epic's part, or the decal darkens its welt. Soles and raise re-measured on the built boot exported as FBX (hidden_faces.py `export_fbx`); the plugin raises nothing, offsetting only the bare foot to the floor (MetaHumanCharacterEditorSubsystem.cpp 7894).
- His ruling: dark laces. Set on the built material as `recolour_cloth` does (make_cast_metahumans.py 101-113; parameter U).

## 5. Steps (one editor at a time, mh-dress)

1. `retention.py space`; no runner build or night job due.
2. Back up Tom: Cast/MH_TomL1.uasset and Ledger/MetaHumans/MH_TomL1 (today's cut build; the only backup is 6 October's uncut) to F:, hashed.
3. Editor run 1: the import task above, `automated`, `save` off; confirm WI_OA_Boots loads. One package a run (24 September ran out of memory).
4. Run 2: hidden_faces.py's build step adapted: boots worn, side build to /Game/Ledger/EpicBoots; record its levels, vertices, materials, dependencies; export FBX. Character file put back.
5. Measure toe, top, sole depth, the jeans' hem; sole_footprints.py on the FBX.
6. Game: ue-probe/Content/Outfits a junction to mh-dress's, gitignored; "Outfits" in ledger-probe-unreal.yml's copy list (419); a THIRD-PARTY.md row and attribution-check entry; the LedgerGarments change; garments.json.
7. Run 3: the same build over /Game/Ledger/MetaHumans, the item kept.
8. Gate, packaged walk, his page (a whole person).

Rejected (I): the side build's boot exported as TomBoots's FBX; import_garments.py runs in mh-assemble on C:, which would need Epic's material too.

## Risks

- Tom's game copy rebuilt whole: a fault reaches every run. Step 2 first.
- The jeans' hem, draped over the old boots, may clip Epic's.
- Weights re-transferred each build: the toe box may follow the toe joints.
- An editor during the runner's build breaks it.

## Not checked

Triangles, levels, boot height, sole depth, lace parameter, the factory's Python name, the name clash, the look on Tom.

## Sources (read 2 November 2026)

- E1 https://dev.epicgames.com/documentation/metahuman/packaging-your-outfit-asset-with-metahuman-manager
- E2 https://dev.epicgames.com/documentation/metahuman/buying-metahumans-from-fab
- Not found: an Epic page on scripting a wardrobe.
