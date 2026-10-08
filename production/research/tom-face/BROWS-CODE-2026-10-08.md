# Tom's brows: what the plugin's code allows (8 October 2026)

A read-only reading of the MetaHuman plugin installed with UE 5.8 (Engine/Plugins/MetaHuman/MetaHumanCharacter; ue-probe has no plugin copy of its own). Paths are under its Source/ folder unless they say Content/. Nothing was run.

## 1. Yes: the brows have their own colour

Each groom slot (Hair, Eyebrows, Eyelashes, Beard, Mustache) is a separate item with its own "instance parameters". Brows and hair share nothing.
- The list: MetaHumanDefaultPipeline/Public/Item/MetaHumanDefaultGroomPipeline.h:26-42. Melanin (0-1, default 0.16), Redness (0-1, 0.0), Roughness (0-1, 0.25), Whiteness (0-1, 0.0), Lightness (0-1, 0.0), DyeColor (a colour). The real starting values come from each groom's own material (Private/Item/MetaHumanMaterialPipelineCommon.cpp:440-479).
- The brows use this class: WI_Eyebrows_M_Dense names Content/BuildPipeline/DefaultWardobePipeline/DefaultGroomPipeline, whose parent is MetaHumanDefaultGroomPipeline.
- At build, the Eyebrows item's Melanin, Redness, Whiteness and DyeColor are written into the face skin as EyebrowsMelanin, EyebrowsRedness, EyebrowsWhiteAmount and EyebrowsDyeColor (Private/Item/MetaHumanDefaultGroomPipeline.cpp:263-268). Roughness and Lightness reach only the strands.
- The character itself has no brow colour setting. The head model's lash colour (MetaHumanCharacter/Public/MetaHumanCharacterEyes.h:282, 285) is for lashes.

## 2. How a script sets it

Scripts can call get_instance_parameters (MetaHumanCharacterPalette/Public/MetaHumanCollectionBlueprintLibrary.h:333-334), set_float (:155-156) and set_color (:173-174). Each set first reads the item's current values, which exist only once that collection is built (Private/MetaHumanCollectionBlueprintLibrary.cpp:97-107; Private/MetaHumanInstance.cpp:709-714). The plain override call is C++ only (Public/MetaHumanInstance.h:330).

Only two collections are ever built: the preview, by assemble_for_preview (MetaHumanCharacterEditor/Private/MetaHumanCharacterEditorSubsystem.cpp:878), and a throw-away copy made by build_meta_human (Private/Subsystem/MetaHumanCharacterBuild.cpp:1448-1453, 1589). The character's own internal collection is never built.

Epic's own test (Content/Python/test_set_character_instance_params.py:25-154) gives the order. In the build step, after try_add_object_to_edit:
1. preview = get_preview_collection(ch) (Subsystem.h:558-559)
2. assemble_for_preview(ch) (:571-572)
3. preview.default_instance.get_instance_parameters(item_path=MetaHumanPaletteItemPath(item_key=the Eyebrows item)); set_float on "Melanin", "Redness", "Whiteness"
4. on_edit_preview_collection(ch) (:567-568) copies them into the character (Subsystem.cpp:816; MetaHumanInstance.cpp:407-408)
5. build_meta_human.

Warning: the preview is a copy taken at try_add_object_to_edit (Subsystem.cpp:1162). Step 4 overwrites the character's collection with it (MetaHumanCollection.cpp:469-491), so groom changes made to internal_collection after opening would be lost. In the build step, a fresh open of the saved character, the two match.

Does it survive assembly? Yes, through a build. The values are saved on the character (MetaHumanInstance.h:488-489) and copied into the build (MetaHumanCharacterBuild.cpp:162, 1506-1511). The build then bakes them into the face skin and the pre-baked brow texture (MetaHumanDefaultEditorPipeline/Private/MetaHumanDefaultEditorPipelineBase.cpp:1471-1491, 1526-1534, 1784-1870). Assembly puts them on the strands (MetaHumanDefaultPipeline/Private/Item/MetaHumanGroomPipeline.cpp:133-146). After that they are fixed in the built files, and a change needs a new build.

## 3. Why today's script does not reach it

make_cast_metahumans.py sets the values on internal_collection.default_instance after build_meta_human (lines 1213-1229, 1272-1277). By the code above that collection is never built. So the call should find no parameters, skip the rebuild and leave the face's brow layer at its default. recolour_hair (806-819) changes only the strand materials. Epic's shipped example_add_grooms.py (31-41) reads the internal collection the same way. Its own test uses the preview, so follow the test.

## 4. Not reached

- The log of builds N1-N4: ue-material.txt has been overwritten, and no editor log holds them.
- Settings stored only in binary asset files: the face material's default brow values and mask, and which detail levels show the painted layer.
- Whether pre-baked grooms are on. The setting's name is saved in BP_DefaultLegacyPipeline, which suggests on, and High inherits it. GroomTextureMinLOD is not saved in the brows' item, so it is probably the default of 5 (MetaHumanDefaultGroomPipeline.h:160).
