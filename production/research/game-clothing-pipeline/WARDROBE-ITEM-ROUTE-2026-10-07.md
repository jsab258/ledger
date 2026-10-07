# A made garment on a cast MetaHuman: the wardrobe-item route (7 October 2026)

Research for CLOTHES.md item 1 (Ron's plain outfit, F:/LedgerTools/garments/ron_plain_outfit), read-only, from the UE 5.8 MetaHuman Character plugin's source and Epic's forum. Paths are under `Engine/Plugins/MetaHuman/MetaHumanCharacter/Source` unless named otherwise; line numbers approximate.

## The finding

- The **Outfits, Top Garment and Bottom Garment** slots take only a Chaos Outfit Asset; a skeletal mesh goes in the separate **"SkeletalMesh"** slot (MetaHumanDefaultEditorPipelineBase.cpp 276-292; MetaHumanDefaultPipelineBase.cpp 16-19).
- **Outfit Asset (rejected):** a production build always re-transfers weights from the body (bTransferSkinWeights, EditorPipelineBase.cpp 498; OutfitEditorPipeline.cpp 74), wiping a garment's own weights; it needs a static mesh, a Cloth Asset dataflow and the Beta Outfit Asset, and is turned back into a skeletal mesh at build anyway (OutfitEditorPipeline.cpp 140-151).
- **Skeletal-mesh wardrobe item (recommended):** the build passes the mesh through untouched, weights, LODs and materials kept (SkeletalMeshEditorPipeline.cpp 30-43). Its editor pipeline carries a **body hidden-face map** (SkeletalMeshEditorPipeline.h 40-48); the build cuts those faces out of the body on every LOD (EditorPipelineBase.cpp 739-764, 1719-1742) for the items the character build pins (MetaHumanCharacterBuild.cpp 1592). The Optimized pipeline adds the garment as a component under Body in BP_MH_ with the leader pose set in its construction script (EditorPipelineLegacy.cpp 138-147, 401-410).
- **Attached in the game (today's LedgerGarments.h, SetLeaderPoseComponent):** keeps the weights but nothing hides the body underneath; faces are removed only at build.

## The steps

1. Import the FBX in the face project (import_garments.py), then LODs: `unreal.SkeletalMeshEditorSubsystem.regenerate_lod(mesh, 4)`. Epic's check wants 4 LODs or more, a MetaHuman-compatible skeleton, under 100k vertices, materials assigned (MetaHumanSDK VerifyMetaHumanSkeletalClothing.cpp 67-95).
2. A body mask on the body's UVs (white shown, black hidden, a grey edge band shrunk), `T_<garment>_bmask`; white margins under cuffs, neck band and the welt-to-waist overlap.
3. The wardrobe item, as the editor makes it (SMetaHumanCharacterEditorWardrobeToolView.cpp 770-790): `create_asset("WI_RonJumper", folder, unreal.MetaHumanWardrobeItem, unreal.MetaHumanWardrobeItemFactory())`; `principal_asset`; `pipeline` = `unreal.new_object(unreal.MetaHumanSkeletalMeshPipeline, wi)` (its edit hook makes the editor pipeline, MetaHumanWardrobeItem.cpp 13-26, 57-67); on `editor_pipeline`, `body_hidden_face_map_texture` = a HiddenFaceMapTexture with its settings (MetaHumanGeometryRemovalTypes.h 14-63).
4. In make_cast_metahumans.py: the white base layer off with `default_instance.set_single_slot_selection(slot, unreal.MetaHumanPaletteItemKey())` for Outfits, Top Garment and Bottom Garment (a null key clears the slot, MetaHumanInstance.cpp 417-440); the garment on with `col.try_add_item_from_wardrobe_item("SkeletalMesh", wi)` and `try_add_slot_selection(MetaHumanPipelineSlotSelection(slot_name="SkeletalMesh", selected_item=key))` (Epic's examples/example_add_clothing.py 10-18, another slot); rebuild at Optimized High.
5. The game: BP_MH_ carries the garment; mark built-in garments in garments.json so LedgerGarments::Wear does not add them twice, and keep its hide rule (LedgerGarments.h 166) from hiding a built-in jumper under a held jacket, which would now leave a hole.

## Risks and the experiment first

- An all-black mask leaves the body whole in 5.8; with several garments each wardrobe item's cull, keep and shrink values must be set (forums.unrealengine.com/t/fully-hidden-metahuman-body-becomes-visible-after-assembly/2833124, 21 and 24 September 2026).
- Removed skin shows as holes wherever cloth moves off the body (the outfit's seated lap and arms up).
- Unverified: whether Python can set the private `pipeline` and `editor_pipeline` properties; the Python names of the namespaced structs. OptimizeBoneCounts strips unweighted bones (Legacy.cpp 414).
- **The experiment, Ron only, about an hour, once his outfit passes its review:** the script calls succeed; BP_MH_RoccoP2 holds the two garment components following Body; the body's triangle count drops on LODs 0 to 3, no skin through or holes walking, seated, turned and arms up; the garment's weights unchanged after the build; the packaged build loads it.
