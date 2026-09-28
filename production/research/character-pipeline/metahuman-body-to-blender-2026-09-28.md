# A MetaHuman's whole body into Blender (28 September 2026)

## Recommendation (confidence: high on the code path, medium until run)

Stay inside Unreal. With the character open for editing (`MetaHumanCharacterEditorSubsystem.try_add_object_to_edit`), call
`unreal.MetaHumanCharacterExportBlueprintLibrary.export_geometry(character, p)` with `p = unreal.MetaHumanGeometryExportParams()`, `p.project_path`, `p.body_skeletal_mesh = True`, `p.full_body_skeletal_mesh = True`, `p.overwrite_existing_assets = True`; then FBX-export the new `<Name>_Body` / `<Name>_FullBody` skeletal meshes as we already do. Free, Unreal licence, no clicking. Check it with the same waist-up vertex count that found the gap.

## 1. What the 5.8 API does (facts, read in the installed engine source, UE 5.8, 28 Sept 2026 [S3]; names also on [S1], [S2])

- The cut happens only in the build: `RemoveAndShrinkGeometry` runs in `MetaHumanDefaultEditorPipelineBase.cpp` (about line 740), and only when an outfit or skeletal-mesh wardrobe item in the assembly carries a body hidden face map. The setting is on the item, not the build: `UMetaHumanOutfitEditorPipeline.BodyHiddenFaceMapTexture` and `UMetaHumanSkeletalMeshEditorPipeline.BodyHiddenFaceMapTexture` (`FHiddenFaceMapTexture`: Texture; Settings `MaxCullValue` 0.1, `MinKeepValue` 0.9, `MaxShrinkDistance`). `MetaHumanCharacterEditorBuildParameters` has no keep-hidden-faces switch.
- The editor preview hides covered skin only through its material (`UpdateCharacterPreviewMaterialHiddenFacesMask`, console variable `mh.Character.PreviewHiddenFaces`); the preview's body mesh keeps every face.
- `export_geometry` duplicates that preview mesh (`CharacterData->BodyMesh`) into a new asset, skeleton and skin weights included. `full_body_skeletal_mesh` merges head and body (`CreateCombinedFaceAndBodyMesh`, needs both DNAs) and attaches the body's measurements as `ChaosOutfitAssetBodyUserData`, the data Unreal's outfit resizing reads. It fails unless the character is open for editing.
- Inference: a build with no garment should keep the torso; ours probably still had a garment selected in the character's collection, or the old mesh was not replaced. Not worth chasing: this route skips the build.

## 2. body.dna into Blender

- **Poly Hammer Character DNA add-on** [S4]: GPL-3.0 (allowed; a tool we do not ship). The free base imports head and body DNA; Blender 4.5 and 5.2; MetaHuman 5.6 to 5.8; release 0.13.8 published 22 Sept 2026. Operator `import_dna` with `include_body` picks up body.dna beside head.dna; callable from Blender Python (inference; headless untested). Catch: the compiled OpenRigLogic bindings (py311/py313) are not in the GitHub source; the install comes from Poly Hammer's extension server after **creating an account**, which only Jafar may do. It also asks for metrics consent.
- **Epic OpenRigLogic** [S5]: MIT, branch 5.8, last push 10 Sept 2026. DNA reader with Python bindings built by CMake/SWIG; `GeometryReader` gives vertex positions, UVs, normals, layouts, skin weights, blend shapes. We would build it with the PC's Visual Studio and write our own Blender import script (mesh, armature, weights). Free, fully scriptable, about a day's work and our own bugs.
- **MetaHuman DNA Calibration** [S6]: its own "MetaHuman DNA Calibration License" (not on the allowlist), Python 3.7/3.9, and says it is not updated for 5.6 characters. Reject.
- **Unreal's DNA import** (`DNAAssetImportFactory`, RigLogic plugin [S3]) makes a UDNA asset to attach to an existing mesh, not a mesh. `import_body_whole_rig(character, body_dna, head_dna)` [S1] loads a DNA onto a character, which then feeds the recommended route; useful only for DNA from elsewhere.

## 3. Other routes

- DCC Export: head and body DNA plus textures "for use in a DCC application such as Maya or Houdini" [S2]; no FBX, no Blender. The 5.8 release notes add textures to it, nothing for Blender [S7].
- Conforming the template (`get_mesh_for_body_conforming_from_dna`, `conform_body_to_target`, `set_body_mesh` [S1]) would rebuild a body we already have; unnecessary.

## Ranking (cost, then scriptability)

1. `export_geometry` then FBX: free, fully scripted, Unreal-only. **Recommended.**
2. OpenRigLogic plus our own Blender script: free (MIT), fully scripted, a day's work.
3. Poly Hammer free add-on: free (GPL), probably scriptable, needs an account Jafar creates.
4. DNA Calibration: rejected (licence, outdated).

## Sources

- [S1] MetaHuman Creator Python scripting, undated: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine
- [S2] MetaHuman Creator Export tool, undated: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-export-tool-in-unreal-engine
- [S3] Installed UE 5.8 source, read 28 Sept 2026: Engine/Plugins/MetaHuman/MetaHumanCharacter/Source (MetaHumanCharacterExportBlueprintLibrary.h/.cpp, MetaHumanCharacterEditorSubsystem.cpp, MetaHumanGeometryRemoval.h, MetaHumanOutfitEditorPipeline.h, MetaHumanDefaultEditorPipelineBase.cpp); Engine/Plugins/Animation/RigLogic/Source/RigLogicEditor
- [S4] https://github.com/poly-hammer/meta-human-dna-addon (README and LICENSE.md, undated; release 0.13.8, 22 Sept 2026); https://www.polyhammer.com/blog/free-character-dna-addon-openriglogic (12 July 2026); https://docs.polyhammer.com/character-dna-addon/ (undated)
- [S5] https://github.com/EpicGames/OpenRigLogic (MIT; pushed 10 Sept 2026)
- [S6] https://github.com/EpicGames/MetaHuman-DNA-Calibration and its LICENSE, undated
- [S7] https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine, undated (MetaHuman 5.8 released 17 June 2026: https://forums.unrealengine.com/t/metahuman-5-8-released/2729288)
