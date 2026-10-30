# A body hidden face map for Tom, by script, in UE 5.8 (30 October 2026)

Read 30 October 2026: the installed UE 5.8 MetaHuman plugin source (paths under
`C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/MetaHuman/MetaHumanCharacter/Source/`, shortened below),
the engine's Kismet header, Epic's page [E1], and Tom's own assets and garments. D = read in the source or
measured here; I = inference; U = unverified.

## The questions

1. Where does the 5.8 build cut the body, and from what?
2. Which wardrobe item can carry a body map: can the default garment's be replaced, or a map-only item added?
3. How are several items' maps combined?
4. What do the pixels mean; which UVs, which pixel, which triangles go?
5. What else does the cut change (LODs, morph targets, weights, shrink)?
6. How does a script set a map (Python names, property access)?
7. What else does a rebuild change (face, skeleton, other parts)?
8. What does the game do with the build, and what can go wrong there?

## 1. Where the cut happens (D)

- Only in a production build, and only for pinned items: an Outfit item's map is queued at
  `MetaHumanDefaultEditorPipeline/Private/MetaHumanDefaultEditorPipelineBase.cpp` 1632-1664, a SkeletalMesh item's at
  1718-1744, both into `PipelineData.BodyHiddenFaceMaps` (`MetaHumanCharacterPipelineData.h` 44-46). The character
  build pins every selection of the character's instance (`MetaHumanCharacterEditor/Private/Subsystem/MetaHumanCharacterBuild.cpp`
  1589-1592) on a transient copy of the character's collection (1443-1452), whose quality is Production by
  default (`MetaHumanCharacterPalette/Public/MetaHumanCollection.h` 326).
- `TryRemoveHiddenGeometry` (EditorPipelineBase.cpp 677-753) converts the maps to images, combines them when there are
  several, and runs `RemoveAndShrinkGeometry` on every LOD of the generated body mesh, all material slots
  (762-763); the face mesh gets only head maps, and only on its skin slots (755-762).
- The editor's preview never cuts: it masks in the material (`mh.Character.PreviewHiddenFaces`,
  `MetaHumanCharacterEditorSubsystem.cpp` 129-131; `UpdateCharacterPreviewMaterialHiddenFacesMask`, 2062 of the .h).
  `export_geometry`'s body (F:/LedgerTools/bodies/MH_TomL1/MH_TomL1_Body.fbx) is that uncut preview mesh.

## 2. Which item carries it (D unless marked)

- The map is a property of an item's editor pipeline, never of the character or the build parameters:
  `UMetaHumanOutfitEditorPipeline::BodyHiddenFaceMapTexture` (`MetaHumanDefaultEditorPipeline/Public/Item/MetaHumanOutfitEditorPipeline.h` 82-90)
  and `UMetaHumanSkeletalMeshEditorPipeline::BodyHiddenFaceMapTexture` (`.../Item/MetaHumanSkeletalMeshEditorPipeline.h` 40-48),
  handed to the build if its texture has source data (OutfitEditorPipeline.cpp 168-197; SkeletalMeshEditorPipeline.cpp 45-69).
  Each also has a Head map. Epic's page says head faces cannot be hidden [E1]; the 5.8 source can, on the
  face's skin slots (above). Not used here.
- Slots: Outfits, Top Garment, Bottom Garment take only a Chaos Outfit Asset; SkeletalMesh takes a skeletal mesh
  (`MetaHumanDefaultEditorPipeline/Private/MetaHumanDefaultEditorPipelineBase.cpp` 276-293; names, `MetaHumanDefaultPipeline/Private/MetaHumanDefaultPipelineBase.cpp` 16-19).
- Epic's `WI_DefaultGarment` (the T-shirt and shorts) already carries one: its Outfit editor pipeline's
  BodyHiddenFaceMapTexture is `/MetaHumanCharacter/Optional/Clothing/DefaultGarment/ClothAssets/bodyShapeA/Textures/DG_BodyShapeA_BodyMask`
  (the asset's own strings; read back by the probe, below). Tom wears two copies of it in Outfits (variations
  None and None_1: the preset's and make_cast_metahumans.py's), so his built body is cut under shirt and shorts.
- **Replacing the default garment's own map: not in place.** It is engine plugin content and every MetaHuman
  shares it. A project copy can carry ours: `EditorAssetLibrary.duplicate_asset` copies the item with its
  instanced pipeline (the item's `Pipeline` is `EditAnywhere, Instanced`, `MetaHumanCharacterPalette/Public/MetaHumanWardrobeItem.h` 67-68;
  the outfit pipeline's `EditorPipeline` likewise, `MetaHumanDefaultPipeline/Public/Item/MetaHumanOutfitPipeline.h` 133-134),
  and Tom's second default-garment selection is swapped for the copy. Chosen (cheapest: no new mesh).
- **A map-only skeletal-mesh item: possible but not map-only.** Its principal asset must be a skeletal mesh,
  which the Optimized pipeline puts in the blueprint as a component following the body
  (`MetaHumanDefaultEditorPipelineLegacy.cpp` 138-147, `ApplySkeletalMeshAssemblyOutputToSkeletalMeshComponent`): an extra part
  in every Tom. Rejected while the copy route works.

## 3. Several maps (D)

`TryCombineHiddenFaceMaps` (`MetaHumanCharacterEditor/Private/MetaHumanGeometryRemoval.cpp` 22-182): the output is the
largest source size, nearest-pixel resampled; per pixel the lowest wins ("if any of the source maps wants to hide
this pixel, it will be hidden", 169-172); its thresholds are the defaults and its shrink distance the largest
asked. So Tom's cut is the union of the default garment's and ours.

## 4. The pixels (D)

- `FHiddenFaceMapSettings` (`MetaHumanCharacter/Public/MetaHumanGeometryRemovalTypes.h` 14-51): at or below
  MaxCullValue 0.1 cut; at or above MinKeepValue 0.9 kept; between, shrunk along minus the normal by up to
  MaxShrinkDistance (default 0: no shrink; engine units, cm, I). Black hidden, white shown, as Epic's page [E1].
  The page calls nothing in between; the source's grey band is the shrink.
- Sampled: R only on a single map (`SampleHiddenFaceMap` 326-331), the highest of R, G, B when combining (89-91).
  Read from the texture's source, top mip (184-210); the engine writes its own as linear (212-221).
- Which pixel: `floor(Wrap(U * Res, 0, Res - 1))`, V the same (`GetHiddenFaceMapPixelForUV` 333-340;
  `ShouldHideTriangle` 362-364). **Tom's body UVs sit in the second tile, u 1.0096 to 1.9904** (measured on the
  FBX); the wrap's period is Res - 1, so they land one pixel right of (u - 1) * Res. Rows run top down in the
  engine's V, which is 1 - Blender's v in an FBX Unreal wrote (checked against the default garment's map, below).
- Which triangles: cut only if every pixel it touches is at or below 0.1 (ShouldHideTriangle 342-402), the touch
  tested on its corners floored to pixels and with a rounded box test (232-323) that never counts the last
  column or row of its box. The map script ports this line for line and predicts each LOD's cut.

## 5. What the cut does to the body mesh (D)

`RemoveAndShrinkGeometry` (412-797), per LOD on the mesh description: the faces go (496-573); points are kept
while any kept face uses them; skin weights are remapped, not recomputed (745-760); morph targets lose removed
and shrunk points and empty ones are dropped (762-786); a LOD reduced from another is skipped (441-448). No
bone, no skeleton, no other mesh is touched (I, from the code: nothing there takes them).

## 6. Setting it by script (D, measured 30 October in the probe run)

- Python sees `unreal.HiddenFaceMapTexture` and `unreal.HiddenFaceMapSettings`, `MetaHumanSkeletalMeshPipeline`,
  `MetaHumanWardrobeItemFactory`, `TextureExporterPNG`; **not** `MetaHumanOutfitEditorPipeline` or
  `MetaHumanSkeletalMeshEditorPipeline`, which are wrapped as their exposed parent, `MetaHumanItemEditorPipeline`.
  So `get_editor_property("body_hidden_face_map_texture")` on the editor pipeline raises "Failed to find property"
  (F:/LedgerTools/bodies/MH_TomL1/hidden-faces/probe-try1.json). **The C++ name works**:
  `ep.get_editor_property("BodyHiddenFaceMapTexture")` returned the default garment's map, a `HiddenFaceMapTexture`
  (probe.json, try 2): DG_BodyShapeA_BodyMask, 4096 x 4096 8-bit grey (exported PNG), sRGB on, settings 0.1 / 0.9 / 0.
- Reaching it: `wi.get_editor_property("pipeline")` (private but EditAnywhere), then
  `.get_editor_property("editor_pipeline")`, then the struct, edited and set back.
- The engine's generic setters (`SetEditorProperty`, `Set*PropertyByName`) are `BlueprintInternalUseOnly`
  custom thunks (`Engine/Source/Runtime/Engine/Classes/Kismet/KismetSystemLibrary.h` 987-1076, 2094-2110): no help from Python (U).
- The swap on Tom: `col.try_add_item_from_wardrobe_item("Outfits", copy)`, then `set_single_slot_selection("Outfits", kept)`
  and `try_add_slot_selection(...)` for the copy (`MetaHumanCharacterPalette/Public/MetaHumanInstance.h` 219-225;
  `TryRemoveSlotSelection` is not script-callable, 260).

## 7. What else a rebuild changes (D, measured; F:/LedgerTools/bodies/MH_TomL1/hidden-faces/compare.json)

Nothing in the cut touches the face, skeleton, grooms, textures or materials (sections 1 and 5), but a rebuild
regenerates all of them from the character, so the game's build of 6 October (before/) was compared with the
side build of 30 October (after/), both exported as FBX with every LOD and the textures as PNG
(tools/ue/blender_compare_builds.py):

- Body: 341 bones, none moved (0.0 mm); every point kept sits where it was (0.0 mm). Faces LOD0 47,392 to
  19,613, LOD1 11,843 to 5,366, LOD2 5,468 to 2,628, LOD3 1,478 to 749: exactly the union the ported test
  predicted (60,816 - 41,203 = 19,613; 9,830; 4,004; 1,203). Points LOD0 25,328 to 10,674.
- Face: 874 bones, none moved; 19,285 / 4,065 / 903 / 243 points, every one where it was (0.0 mm).
- Blueprint: the same 21 references, but the replaced item's two clothing materials renamed
  (MI_WI_DefaultGarment_M_DG_bodyShapeA_Shirt/Short to MI_WI_TomL1_HiddenFaces_...; "short" kept, which
  LedgerGarments.h 188 reads). 83 assets either side; the 19 other material instances identical in every
  parameter (the hair recolour included).
- **Baked textures differ.** Body colour (T_Body_BC, 4096): 94% of pixels, by 1.5 steps of 255 on average,
  77 at most: the 6 October bake is soft, today's sharp (compare/T_Body_BC_before_after_diffx8.png); body normal
  (8192) 78%, mean 2.1, max 113. Face colour (T_Head_LOD1_BC): only a strip along its bottom edge, the neck
  where the head meets the body, 8.8% of pixels, mean 0.06, max 19.
- **The control build settles it** (`LEDGER_HF_CONTROL=1`: the same build, no map, nothing changed on the
  character, into /Game/Ledger/HiddenFacesControl; compare-before-control.json, compare-control-after.json):
  the control differs from 6 October's build in exactly those textures and nothing else (meshes, bones and
  materials identical), and from the map's build in nothing but the cut faces and the two renamed materials
  (textures identical to the pixel). **So the map changes only the covered body; any rebuild of Tom today, with
  or without it, re-bakes his body textures (sharper; the hands show it) and the neck strip of his face colour.**
  Why the 6 October bake was soft is not known (U: perhaps built before the body's full-size texture sources
  had come from Epic's service).

## 8. The game (D)

- `ue-probe/Content/Ledger/MetaHumans/MH_TomL1` is a junction to `F:/LedgerTools/mh-dress/Content/Ledger/MetaHumans/MH_TomL1`:
  Tom's character (`/Game/Cast/MH_TomL1`) and build live in the **mh-dress** project, not mh-assemble
  (which holds only a copy of the build, for import_garments.py).
- In the game Tom wears only his jacket unless `-WearHeld` names the jeans, jumper and boots (garments.json
  "hold"; `ue-probe/Source/LedgerProbe/Public/LedgerGarments.h` 89-102). A body cut under jeans and boots built
  over the game's copy would leave him without legs and feet in every ordinary run. **So the build here is a
  side build**, `/Game/Ledger/HiddenFaces/MH_TomL1`, the character file put back afterwards; building over the
  game's copy waits for the outfit to be passed (tools/ue/hidden_faces.py, `LEDGER_HF_BUILD_ROOT`).

## The map (D; F:/LedgerTools/bodies/MH_TomL1/hidden-faces/map/, tools/ue/blender_hidden_face_map.py)

- 4096 x 4096 8-bit grey, the default garment's size, so the build's union is pixel for pixel (a 2048 map is
  resampled to 4096 there, and the Res - 1 wrap moves it half a pixel). Painted on the whole body
  (MH_TomL1_Body.fbx, LOD0 32,334 points, 60,816 triangles) against the skinned game files of the jacket
  (v30-reskinned), the jeans (chain-n7) and the boots, at rest.
- Covered: the point's normal ray out meets the garment within 150 mm, or a ray in within 30 mm, or five of
  eight rays 50 degrees off the normal within 150 mm. Then the margins, each measured at the same angle round
  the limb or neck: **cuffs 30 mm** up the forearm from the cuff's edge; **collar 20 mm** below its top edge
  (the collar's top is 1.654 to 1.692 m, the body's neck ends at 1.588 m, so the whole body neck goes);
  **jeans hems 30 mm** above each hem's highest point (about 0.08 m, so above about 0.11 m); **boots 20 mm**
  below the boot's top at that angle (the top runs 0.11 m at the tongue to 0.155 m behind). The jeans and boots
  overlap by more than the two margins everywhere but a strip at the front of the ankle (0.09 to 0.11 m, under
  the tongue and the jeans), small enough to be taken as an island: the whole lower leg and foot go.
- A face is hidden when its three points are; hidden islands under 40 faces given back (3 faces), shown islands
  under 40 faces wholly inside hidden ones taken (148).
- Result, LOD0: 40,823 faces meant hidden; the engine's test ported line for line cuts 40,771 (52 kept: a pixel
  they share with a shown face stays white) and no face meant shown. LOD1 9,483 of 15,196, LOD2 3,821 of 6,632,
  LOD3 1,077 of 1,952. Kept: hands, a 30 mm band inside each cuff (686 faces), the crotch (398 faces: its rays
  escape between the jeans' legs, so it never counts as covered).
- UV check: read at 1 - v, the default garment's own map cuts 7,170 points between 0.79 and 1.59 m (pelvis,
  spine, upper arms, thighs: shirt and shorts), 97% of them inside ours; read at v it would cut the feet.
- With the default garment's map the build cuts the union: predicted LOD0 41,203 (the crotch's 398 among them),
  LOD1 9,830, LOD2 4,004, LOD3 1,203. Today's build, with the default garment's map only, has 47,392 of 60,816
  LOD0 faces (13,424 cut).

## The probe: skin through the garments (D; probe/*.json, tools/ue/blender_skin_through_probe.py)

Body points that come more than 1 mm through a garment they are covered by at rest (worst depth in mm), the
jacket, jeans and boots as the game wears them, posed in Blender from the shared skeleton. Poses: rest;
arms hanging, upper arms turned down 30, 40, 50 degrees from the bind pose (about 53 below level) with the
elbows bent 10, 10, 15 (30 is a natural hang; 40 and 50 push the arms into the hips); a stride; a hand-posed sit.

| body | rest | arms 30/10 | arms 40/10 | arms 50/15 | stride | sit |
|---|---|---|---|---|---|---|
| whole, uncut (export_geometry) | jacket 1 (1.4), jeans 2, boots 20 (5.7) | jacket 102 (16.8; elbows 6 at 2.7) | jacket 196 (14.9; elbows 15 at 4.7, forearms 45 at 8.5) | jacket 370 (21.6) | jacket 218, jeans 23 (crotch 15 at 5.8) | jacket 263 (forearms 117 at 12.0), jeans 90 (15.2) |
| game's now (default garment's cut) | boots 20 (5.7, shin at the boot's top) | jacket 35 (8.4; elbows 21 at 8.4) | jacket 58 (6.2; forearms 34 at 5.9) | jacket 25 (6.2) | jacket 61 (7.0) | jacket 54 (forearms 40 at 11.5), jeans 3 (7.2) |
| with our map | none | none | jacket 3 (3.6, right wrist) | jacket 2 (4.4, right wrist) | jacket 1 (4.8, right wrist) | none |

Every point left coming through is the right wrist inside the cuff's 30 mm margin, which is kept on purpose.
The crotch: the default garment's shorts already cut it in today's build (no jeans points at rest or in the
stride). Not measured: the head mesh. The jacket's collar (top 1.654 to 1.692 m) and the jumper's drawn
neckband (1.586 to 1.651 m) sit on the head's neck, above the body's (which ends at 1.588 m); skin through
them there is the head's, and 5.8 can cut the head too, on its skin slots (section 2), with a head map.

## Putting it back, and what is where

- The game's copy is untouched: its 83 files and Tom's character file hash the same as the copies in
  before/files (files-sha256.txt). Tom's character file was saved by each build run and put back from the copy
  (hash equal).
- In the mh-dress project, made by these runs: /Game/Ledger/HiddenFaces/MH_TomL1 (the build with the map, 83
  assets, 264 MB), /Game/Ledger/HiddenFacesControl/MH_TomL1 (the control, 83 assets), /Game/Ledger/Wardrobe
  (T_TomL1_BodyHiddenFaces, WI_TomL1_HiddenFaces). Nothing references them; delete them in the editor when done.
- To use it in the game, once the jeans, jumper and boots are worn by default: `LEDGER_HF_BUILD_ROOT=/Game/Ledger/MetaHumans`
  with tools/ue/hidden_faces.py's build step (it then keeps the item on the character); undone by copying
  before/files back with no editor open.

## Tries

- Probe, try 1: the snake-case property name failed on the unexposed editor pipeline; try 2, the C++ name, worked.
- Map, try 1: nothing painted, the body's UVs being in the second tile; try 2 wraps as the engine does. The
  crotch's coverage and the boots' closed shell were found by checking the first results, not by failing tries.
- Build: one try. Control build: one.

## Unverified

- Why the 6 October bake of the body textures was soft (section 7).
- The engine's generic property setters from Python (not tried).
- How the cut looks in the game: the measures are geometric, in Blender, on the exported meshes; the side build
  has not been put in the game, walked or photographed.

## Sources

- [E1] Epic, "Testing and Configuring your Parametric Outfit Asset", MetaHuman docs, undated, read 30 October 2026:
  https://dev.epicgames.com/documentation/metahuman/testing-and-configuring-your-parametric-outfit-asset (step 12; no resolution, grey values or margins given)
- Engine source as cited above, read 30 October 2026. Earlier notes: metahuman-body-to-blender-2026-09-28.md section 1;
  ../game-clothing-pipeline/WARDROBE-ITEM-ROUTE-2026-10-07.md; ../clothing-pipeline/PIPELINE-2026-09-30.md, FOOTWEAR-2026-09-30.md, JUMPER-2026-09-30.md.
- Not reached: no published margin rule for hidden face maps (as JUMPER-2026-09-30.md); no Epic page on scripting a map.
