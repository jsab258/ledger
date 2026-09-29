# Blender-made perms as MetaHuman wardrobe grooms, all by script (UE 5.8, Blender 4.5): research note, 29 September 2026

**The problem.** Jafar's ruling of 29 September: the hair for Sheila ("a short shampoo-and-set perm", greying brown) and Darren ("a grown-out perm with bleached tips") is to be made in Blender (free), not bought, and judged on his page. The cast script assigns hair from the MetaHuman Character plugin's own library; none is right. Needed: a scripted route from curls grown in Blender to a groom in the character's hair slot. About thirty minutes of research by a separate helper given the problem; saved here by the builder (the helper cannot write files). "Mine" marks the helper's inference. Epic's MetaHuman pages carry no dates and are labelled by the version they state. All sources accessed 29 September 2026. Earlier research: faces-and-hair-2026-09-28.md.

## 1. Which head to author on

- Epic's Groom Starter Kit (Maya, UE 5.6+) grooms on SKM_MH_Groom_Head, which "should be assigned to both Source and Target Skeletal Mesh" for MetaHuman Creator use; the Houdini Advanced Kit gives the same rule for SKM_MH_Character_Head, the character's own head. [E1][E2]
- Fab's requirements: the binding needs the same mesh as source and target, matching where the curves sit, with UVs matching MetaHuman's. [E3] Binding transfer between meshes is UV-based ("assumes both the Source and Target meshes share the same UV mapping"). [E4]
- Hair is fitted to each face when the item is prepared, the first time it is worn. [E5] Mine: the plugin fits it by a UV transfer from the binding's source mesh; for two one-off haircuts, author each on that character's own head.
- Head out by script: MetaHumanCharacterExportBlueprintLibrary.export_geometry(..., head_skeletal_mesh=True) makes the head a project asset [E6]; mine: then an AssetExportTask to FBX, LOD0. Alternative (mine): a library binding's source_skeletal_mesh is the head Epic's own haircuts were made on.

## 2. What the Alembic must contain

- UE 5.8: only groom_version_major and groom_version_minor are required; groom_guide, groom_group_id, groom_root_uv, groom_id, groom_color are optional. No root UV: a spherical mapping is generated. No width: 1 cm fallback (fat strands); a plain width is converted to groom_width. Guides are generated if none. [E7]
- Blender 4.5's exporter writes one curves object with a point count per strand and widths = radius x 2, no UVs and no groom_* properties (Poly curves as linear, Catmull-Rom as Catmull-Rom). [B1] Mine: the importer accepts files without the version tags in practice (UE 5.3). [V1] Hair Curves export to Alembic from Blender 4.2 on. [B2]
- Y-up: export scale 100; import in Unreal with rotation X=90, scale Y=-1. [V1] Export only the curves (a mesh in the file opens the mesh dialogue). [V1] Objects at the world origin; enough points per strand. [F1]

## 3. Import, bind and wear it by Python

- Plugins Groom and Alembic Groom Importer; project setting Support Compute Skin Cache. [E8]
- Import: AssetImportTask with GroomImportOptions.conversion_settings [E9] (reported ignored from Python in 2022 [F2]: check the result).
- Bind: GroomBlueprintLibrary.create_new_groom_binding_asset(groom, skeletal mesh, points, source mesh, matching section) [E10], or a GroomBindingAsset's groom, source_skeletal_mesh, target_skeletal_mesh then build(). [E11]
- Wardrobe item: unreal.MetaHumanWardrobeItem (principal_asset = the binding, pipeline, thumbnail) [E12]; the groom pipeline MetaHumanDefaultGroomPipeline (baked groom texture for far LODs, ombre support). [E13] Mine: duplicate a library item and swap its principal_asset, keeping the hair material setup.
- Wearing: character.internal_collection.try_add_item_from_wardrobe_item("Hair", item) returns a key for a MetaHumanPipelineSlotSelection passed to default_instance.try_add_slot_selection; colour through assemble_for_preview, get_instance_parameters, set_float/set_color; build with build_meta_human (OPTIMIZED). [E6] Epic's example: Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Python/examples/example_add_grooms.py; read it first. Mine: bleached tips through the material's ombre parameters.
- Cost: strands alone are legal; cards or meshes are the fallback; curve count drives cost; Auto LOD reduces curves with distance [E14]; a third party puts strands at several ms per character [S1]; the Hair Card Generator is experimental and editor-only. [E15] Mine: short cuts at 20 to 30 thousand curves with Auto LOD and no simulation may hold 60 fps; measure.

## 4. Pitfalls

- Hair under the chin on customised MetaHumans (forum threads August 2025 to September 2026, unsolved). [F3]
- Binding hung at 100% CPU from wrong import transforms (UE 5.6). [F4] Mine: curves must sit exactly on the source mesh's rest pose.
- Not following the head: no binding, or the skin cache off. [E8] Invisible or fat strands: width missing or unscaled [E7]; set HairGeometrySettings hair_width_override and hair_width in cm. [E16] Metres against centimetres. [S1]
- 5.8 known issue: packaging with MetaHuman Manager drops parent materials on grooms from outside the plugin. [E17]
- Mine: Blender 5.x reworked the hair node assets; use 4.5's.

## Recipe (the helper's)

1. Plugins and skin cache on; export_geometry the character's head; AssetExportTask to FBX.
2. Blender: import the FBX and apply transforms; a hair Curves object on the head (surface and UV map); Generate, Interpolate, then Curl, Clump or Frizz, then Shrinkwrap (procedural_hair_node_assets.blend).
3. Apply; resample to 16 to 32 points, Poly; radius about 0.00004 m; export Alembic, selected curves only, scale 100.
4. Unreal: AssetImportTask with rotation (90, 0, 0), scale (1, -1, 1); check bounds against the head; hair_width_override; LOD Auto; no simulation.
5. create_new_groom_binding_asset(groom, head, 100, head, 0).
6. Duplicate a library hair wardrobe item; principal_asset = the new binding.
7. try_add_item_from_wardrobe_item, try_add_slot_selection; assemble_for_preview; colour and ombre.
8. build_meta_human (OPTIMIZED); render; play four characters under stat gpu.

## Sources

- E1 Groom Starter Kit (MetaHuman docs, UE 5.6+): https://dev.epicgames.com/documentation/en-us/metahuman/groom-starter-kit
- E2 Houdini Groom Advanced Kit: https://dev.epicgames.com/documentation/metahuman/houdini-groom-advanced-kit
- E3 Asset Format and Structure Requirements for MetaHumans on Fab: https://dev.epicgames.com/documentation/metahuman/asset-format-and-structure-requirements-for-metahumans-on-fab
- E4 Setting Up Bindings for Grooms (UE 5.8): https://dev.epicgames.com/documentation/unreal-engine/setting-up-bindings-for-grooms-in-unreal-engine
- E5 Hair and Clothing Tools: https://dev.epicgames.com/documentation/metahuman/hair-and-clothing-tools
- E6 MetaHuman Creator Python Scripting (UE 5.8+): https://dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine
- E7 Using Alembic for Grooms (UE 5.8): https://dev.epicgames.com/documentation/unreal-engine/using-alembic-for-grooms-in-unreal-engine
- E8 Hair Simulation and Rendering Quick Start (UE 5.8)
- E9 GroomImportOptions / GroomConversionSettings, Python API 5.7
- E10 UGroomBlueprintLibrary::CreateNewGroomBindingAsset (UE 5.8 API)
- E11 GroomBindingAsset, Python API 5.7; E12 MetaHumanWardrobeItem, Python API 5.7; E13 UMetaHumanDefaultGroomPipeline (5.7 API)
- E14 Groom Scalability and Performance (UE 5.8); E15 Hair Card Generator in Dataflow (5.8, experimental); E16 HairGeometrySettings, Python API 5.7; E17 MetaHuman 5.8 Known Issues
- B1 Blender source abc_writer_curves.cc, v4.5.0 (July 2025); B2 Blender 4.2 release notes, Import and Export (July 2024)
- V1 J. Versluis, Daz hair to Unreal groom, 18 April 2024, updated 26 May 2025
- F1 Groom Exporter forum thread (2022 to August 2024); F2 XGen groom conversion settings from Python (June 2022); F3 groom binding in the wrong place on a customised MetaHuman (August 2025 to September 2026); F4 UE 5.6 groom binding bug (June 2025)
- S1 StraySpark, Blender hair to Unreal (29 July 2026)
