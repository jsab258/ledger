# Cloth weight maps by script, UE 5.8 (29 September 2026)

The problem: the jacket's max distance must vary. It should be about 1 to 1.5 cm on the chest, back and shoulders, rising to several centimetres towards the hem. All of it has to be set by editor Python, with no hand painting.

Sources: the installed engine's own source at `C:\Program Files\Epic Games\UE_5.8\Engine\...` (read 29 September 2026; paths below are relative to `Engine\`), plus the web pages listed at the end (all read 29 September 2026). D means documented, with the source given. I means my inference.

## Answer in one paragraph

The cleanest route is new in 5.8 and needs no vertex order at all. It uses two generic Dataflow nodes: a **Linear Gradient Sampler** (gradient by height) feeding a **SamplerToAttribute** node, which writes a float attribute called `MaxDistance` into the cloth collection's `SimVertices3D` group. A float attribute in that group *is* a cloth weight map. SimulationMaxDistanceConfig then reads it, with Low/High giving centimetres. The same pair of nodes can also write an `InpaintMask` map, which makes TransferSkinWeights compute the skirt's skin weights by smoothing down from the waist instead of copying them from the thighs. Everything is set with the three functions we already use: add node, connect, set property.

## 1. Ways to supply a weight map without painting

**A. Generate it inside the graph from positions (recommended).**
- D: `FDataflowLinearGradientFloatSamplerNode` (display name "Linear Gradient Sampler") has one struct property, `Gradient` (type `FDataflowLinearGradientFloatSampler`), with fields `StartPoint`, `StartValue`, `EndPoint`, `EndValue` and `bClamp`. It outputs `Sampler`. Source: `Plugins\Dataflow\Source\DataflowNodes\Private\Dataflow\SamplerNodes\DataflowGradientSamplerNode.h`.
- D: 5.8 also has other samplers in the same folder: DistanceFromPlane, DistanceFromBox, DistanceFromSphere, Remap, Clamp, SmoothStep, Step, Multiply, Add, OneMinus, Mesh, Texture and more.
- D: `FDataflowSamplerToAttributeNode` (display name "SamplerToAttribute") has the input `Collection` and the input `Sampler` (type `FDataflowSamplerTypes`, which accepts a float or a vector sampler). Its properties are `AttributeName` (string), `VertexGroup` (struct `FScalarVertexPropertyGroup` with one field `Name`), `bSaveAsColor`, `bUseDefaultValue` and `DefaultValue`, plus an optional `VertexSelection` input. For a group without a `Vertex` position, it samples at `RenderPosition`, or else at `SimPosition3D`, and writes the result with `AddAttribute<float>(AttributeName, VertexGroup.Name)`. Source: `Plugins\Dataflow\Source\DataflowNodes\Private\Dataflow\DataflowSamplerToAttributeNode.h/.cpp`. The older `FloatSamplerToAttribute` is marked "DEPRECATED 5.8" in the same header.
- D: a cloth weight map is simply a user-defined float attribute in group `SimVertices3D`. `HasWeightMap` and `GetWeightMap` look up exactly that, and any name that is not a reserved `Sim...` schema name counts. Sources: `Plugins\ChaosClothAsset\Source\ChaosClothAsset\Private\ChaosClothAsset\CollectionClothFacade.cpp` (HasWeightMap, GetWeightMap) and `ClothCollection.cpp` (HasUserDefinedAttribute).
- D: SimulationMaxDistanceConfig's `MaxDistance` is `FChaosClothAssetWeightedValue`, with fields `bIsAnimatable`, `Low`, `High` and `WeightMap`. The value used is Low + weight × (High − Low), and weight 0 means Low. The default is `{true, 0, 100, "MaxDistance"}`. `MaxDistance.WeightMap` is also an input pin. Sources: `Plugins\ChaosClothAssetDataflowNodes\...\Public\ChaosClothAsset\SimulationMaxDistanceConfigNode.h` and `WeightedValue.h`.
- I: nothing depends on vertex count or order, so it survives any change to the Blender mesh. Positions are the sim mesh's rest positions in centimetres, in the static mesh's own space.
- I: keep the sampled values between 0 and 1. The WeightMap node clamps, but SamplerToAttribute does not.

**B. Carry the weights on the simulation static mesh itself (also scriptable, works through the importer).**
- D: when StaticMeshImport has `SimMeshSection` = -1 (the default), it converts the mesh with `FMeshDescriptionToDynamicMesh` and then `BuildSimMeshFromDynamicMesh`. The first turns every per-vertex float attribute that is not reserved into a named weight layer. The second copies every weight layer into a sim weight map *of the same name*, looked up through each vertex's source index, so order does not matter. Sources: `Plugins\ChaosClothAssetDataflowNodes\...\Private\ChaosClothAsset\StaticMeshImportNode.cpp` lines 93–104; `Source\Runtime\MeshConversion\Private\MeshDescriptionToDynamicMesh.cpp` ("find weight attribs", "initialize weight layers"); `Plugins\ChaosClothAsset\...\ClothGeometryTools.cpp` ("Copy scalar weight maps").
- D: Geometry Script can write such an attribute from Python through `unreal.GeometryScript_WeightMaps`: `find_or_add_mesh_weight_map`, `set_mesh_weight_map_values` (a scalar list, with `skip_gaps`), `set_mesh_constant_weight_map_value` and `set_mesh_selection_weight_map_value`. `GeometryScript_ListUtils.convert_array_to_scalar_list` builds the list, and `copy_mesh_to_static_mesh` writes the layers back as vertex float attributes (`FDynamicMeshToMeshDescription::ConvertWeightLayers`). Sources: `Plugins\Runtime\GeometryScripting\Source\GeometryScriptingCore\Public\GeometryScript\MeshWeightMapFunctions.h`, `ListUtilityFunctions.h`, `Private\MeshAssetFunctions.cpp` lines 316–324, and `DynamicMeshToMeshDescription.cpp` line 1327.
- D: those attributes are saved with the mesh, because only attributes flagged Transient are skipped. Source: `Source\Runtime\MeshDescription\Private\MeshAttributeArray.cpp`.
- I: this route breaks if `SimMeshSection` is set to a section, because the section path goes through a skeletal model that carries no weight layers. It also breaks when the FBX is reimported (the attribute is lost), so the script must run after every import.

**C. Set the WeightMap node's own array.**
- D: `FChaosClothAssetWeightMapNode` keeps its weights in a snapshot (`Snapshots`, of type `FDataflowToolNodeSnapshotSet`, with fields `ActiveSnapshot` and `Snapshots`). The snapshot holds the weights together with the mesh positions and faces they were made on; if the mesh has changed, it remaps them by position. `VertexWeights` (a `TArray<float>`) is read **only when there is no active snapshot**. Sources: `...\Public\ChaosClothAsset\WeightMapNode.h` and `WeightMapNode.cpp` (`GetWeightsFromActiveSnapshot`); `Plugins\Dataflow\Source\DataflowNodes\Public\Dataflow\DataflowToolNode.h`.
- D: Epic's own 5.8 converter fills a fresh WeightMap node's `VertexWeights` by code. The values are 0 to 1, indexed by **SimVertices3D after `CleanupAndCompactMesh`**, and the converter can only do this because its import records `SimImportVertexID`. Source: `Plugins\ChaosClothAssetEditorCore\Source\ChaosClothAssetEditor\Private\ChaosClothAsset\LegacyClothingConverter.cpp` (`CreateWeightMapNodes`).
- D: StaticMeshImport builds sim vertices per UV island and then welds seams and compacts, and it does not set `SimImportVertexID` (only SkeletalMeshImport does). Sources: `ClothGeometryTools.cpp` (`BuildSimMeshFromDynamicMesh`) and `SkeletalMeshImportNode.cpp`.
- I: so the order of `VertexWeights` is not Blender's order and cannot safely be computed outside Unreal. Avoid this route.
- D: a wrong count only produces a warning ("… vertex weights in the node: N … vertices in the cloth: M"), and then only the first min(N, M) values are applied. Source: `WeightMapNode.cpp`.

**D. Vertex colour, texture and transfer.**
- D: 5.8 adds `VertexColorToAttribute`, according to an Epic staff forum answer dated 29 May 2026. In source, it reads colour from `RenderColor`, which exists only on render vertices, so its output is a render attribute. Source: `Plugins\Dataflow\Source\DataflowNodes\Private\Dataflow\DataflowVertexColorToAttributeNode.cpp`.
- D: getting that attribute onto the sim mesh means using the WeightMap node's `Transfer` with `TransferType` = UseRenderMesh. That transfer runs from a button (`FDataflowFunctionProperty Transfer`, which calls `OnTransfer`), not during evaluation. Source: `WeightMapNode.h/.cpp`.
- I: the button cannot be pressed from Python, so this route is not fully scriptable.
- D: `TextureToAttribute` (new in 5.8) can write a sim attribute by sampling a texture through the sim UVs. Source: `DataflowTextureToAttributeNode.h/.cpp`. This is possible, but more work than route A.
- D: the WeightMap node's Transfer from another collection (Use2DSimMesh, Use3DSimMesh or UseRenderMesh) is the same button. The 5.8 node-reference page for WeightMap describes the Transfer property but says nothing about scripting.

**E. Selections.**
- D: `SelectionToWeightMap` turns a selection into a two-value map. `ProceduralSelection` offers only SelectAll and Conversion. The `Selection` node stores explicit `Indices`, which again depends on vertex order. Source: the headers of the same names in `...\Public\ChaosClothAsset\`.
- I: selections are useful for kinematic sets, not for gradients.

## 2. Controlling skin weights (skirt on the pelvis, not the thighs)

- D: TransferSkinWeights has no bone include or exclude list. Its properties are `TargetMeshType`, `RenderMeshSourceType`, `SkeletalMesh`, `LodIndex`, `Transform`, `TransferMethod` (ClosestPointOnSurface or InpaintWeights), `RadiusPercentage`, `NormalThreshold`, `LayeredMeshSupport`, `NumSmoothingIterations`, `SmoothingStrength`, `InpaintMask` and `MaxNumInfluences`. Sources: `...\Public\ChaosClothAsset\TransferSkinWeightsNode.h`; 5.8 node reference.
- D: `InpaintMask` (default map name "InpaintMask") marks vertices whose weights are "computed automatically instead of … copied". The mask is read as a weight layer of the sim mesh, and a non-zero value forces inpainting. Sources: the header, `TransferSkinWeightsNode.cpp` lines 381–394, and `Plugins\Runtime\GeometryProcessing\...\Operations\TransferBoneWeights.h` (`ForceInpaintWeightMapName`).
- I: an InpaintMask of 1 below the hip line should make the skirt take a smooth extension of the waist weights (mostly pelvis and spine). One user reported InpaintMask did not solve a different case, a collar picking up head weights (forum, 29 August 2026), so test it before relying on it.
- D: the `SkeletalMesh` source can be any skeletal mesh. The template's note says the node "also sets the cloth asset skeleton". Source: `DF_StaticMeshClothTemplate` strings.
- I: a Blender-made source works too: either the garment itself, skinned with the skirt on the pelvis, or a body copy with the thigh weights moved to the pelvis. It must use the MetaHuman body skeleton, with `TransferMethod` = ClosestPointOnSurface.
- D: `DF_SkeletalMeshClothTemplate` has no TransferSkinWeights node. Its nodes are SkeletalMesh_SIM / SkeletalMesh_RENDER feeding SkeletalMeshImport_SIM / SkeletalMeshImport_RENDER (`FChaosClothAssetSkeletalMeshImportNode_v2`), then WeightMap_MaxDistance and SimulationMaxDistanceConfig. SkeletalMeshImport copies the garment's own skin weights into both render and sim. Sources: the template's name strings; `ClothDataflowTools.cpp` (render bone weights); `ClothGeometryTools.cpp` (sim bone weights from the "Default" skin weights).
- D: the skeletal importer carries **no** float weight maps (`NumWeightMapLayers` returns 0). Source: `ClothDataflowTools.cpp`.
- I: with that template, max distance would therefore still come from route A, which works on any collection.

## 3. Examples found

- D: an Epic staff answer (29 May 2026) describes VertexColorToAttribute, then a WeightMap node with a "Use Render Mesh" transfer and Map Override "Add". This is the UI route.
- D: Epic's C++ converter shows weight maps set by code: `VertexWeights` on a new node, `OutputName`, and the node spliced in with `Graph.Connect`. It also notes that `AddNewNode` needs the **USTRUCT name** (for example `FChaosClothAssetWeightMapNode`), not the display name. Source: `LegacyClothingConverter.cpp`.
- D: the experimental `ChaosClothAssetToolset` functions are `UFUNCTION(meta=(AICallable))` only. Source: `Plugins\Experimental\Toolsets\ChaosClothAssetToolset\...\ClothAssetToolset.h`.
- I: those toolset functions are probably not reachable from Python.
- D: no Epic Python sample sets cloth weight maps. The forum question "how to make weights from Vertex Color" (22 April 2025) has no answer.

## 4. Pitfalls

- D: `set_dataflow_node_property` finds a **top-level** property by name (`FindPropertyByName`) and parses the text with `PropertyValueFromString`. A nested path like `MaxDistance.Low` will not resolve, so set the whole struct. Source: `Plugins\Dataflow\Source\DataflowEditor\Private\Dataflow\DataflowEditorBlueprintLibrary.cpp`.
- I: text that lists only some of a struct's fields leaves the other fields unchanged.
- D: `connect_dataflow_nodes` replaces whatever was already connected to that input. Source: `Source\Runtime\Dataflow\Core\Private\Dataflow\DataflowGraph.cpp` (`FGraph::Connect`).
- D: `DF_StaticMeshClothTemplate`'s name table includes `DataflowToolNodeSnapshot`, `ActiveSnapshot` and `VertexWeights`, and its comment says the MaxDistance map "must be painted first".
- I: the template's WeightMap_MaxDistance may hold snapshot data from Epic's preview mesh, which would be remapped onto our jacket. Either neutralise it, or put the sampler *after* it.
- D: with no stored weights and `MapOverrideType` = ReplaceChanged, the WeightMap node passes an existing map of the same name through unchanged. Source: `AddWeightMapNode.cpp` (`CalculateFinalVertexWeightValues`).
- D: names are cleaned by `MakeWeightMapName`, which turns spaces and special characters into `_` and trims leading and trailing `_`. A leading `_` is reserved for internal maps. The name must match on three nodes: the WeightMap node's `OutputName`, the SamplerToAttribute node's `AttributeName`, and `MaxDistance.WeightMap`. Source: `WeightedValue.h`.
- D: StripUserAttributes (in the template) removes sim maps that no property references. Source: `StripUserAttributesNode.h`.
- I: `MaxDistance` survives because it is referenced; `InpaintMask` will be stripped, which does no harm.
- D: vertices whose max distance is below the threshold become kinematic, and the template's long-range attachment takes its fixed ends from `KinematicVertices3D`. Sources: `ClothGeometryTools.cpp` (`GenerateKinematicVertices3D`); `LegacyClothingConverter.cpp` comment.
- I: if max distance is never 0, nothing is kinematic and the tethers have no anchors. Consider Low = 0 with weight 0 on a collar or neck band, or pass a selection to `InKinematic`.
- D: in 5.7, TransferSkinWeights split a garment along its UV seams (forum, 5 December 2025; no Epic reply).
- I: watch the seams after regenerating.

## The most promising scripted route (UE 5.8)

This works on either template, and all names come from the installed source. Heights are examples only; measure the real hip and hem heights on the sim mesh.

1. Add the gradient node. Node type `FDataflowLinearGradientFloatSamplerNode`. Set `Gradient` = `(StartPoint=(X=0,Y=0,Z=<hip height cm>),StartValue=0.0,EndPoint=(X=0,Y=0,Z=<hem height cm>),EndValue=1.0,bClamp=True)`.
2. Add the attribute node. Node type `FDataflowSamplerToAttributeNode`. Set `AttributeName` = `MaxDistance` and `VertexGroup` = `(Name="SimVertices3D")`.
3. Connect gradient `Sampler` → SamplerToAttribute `Sampler`.
4. Put the SamplerToAttribute node into the collection chain, so the map exists before SimulationMaxDistanceConfig reads it. Either:
   - put it after WeightMap_MaxDistance and before its consumer: WeightMap_MaxDistance `Collection` → SamplerToAttribute `Collection` → (next node) `Collection`; or
   - put it before WeightMap_MaxDistance, and neutralise that node by setting `VertexWeights` = `()` and `Snapshots` = `(ActiveSnapshot=-1,Snapshots=())`. (I: the text format for these two is my inference.)
5. Set WeightMap_MaxDistance `OutputName` = `(StringValue="MaxDistance")`, so the name sent to `MaxDistance.WeightMap` matches.
6. On SimulationMaxDistanceConfig, set `MaxDistance` = `(bIsAnimatable=True,Low=1.0,High=8.0,WeightMap="MaxDistance")`. Weight 0 (chest, back, shoulders) then gives 1 cm and weight 1 (hem) gives 8 cm. Use Low=0 plus a collar band if tether anchors are needed.
7. Optional, for the skirt's skin weights: a second gradient or Step sampler feeding a second SamplerToAttribute, with `AttributeName` = `InpaintMask`. It goes *before* TransferSkinWeights. Keep `TransferMethod` = InpaintWeights and `InpaintMask` = `(WeightMap="InpaintMask")`, the default.
8. Regenerate with `regenerate_asset_from_dataflow`.
   - I: it evaluates the whole graph again; the editor's own cache may still show old values.

Not yet run on this PC. The first things to check are whether the gradient node's `Gradient` struct accepts text through `set_dataflow_node_property`, and the order of the nodes around WeightMap_MaxDistance in our copy of the template.

## Web sources (all read 29 September 2026)

- [WeightMap node reference, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/node-reference/Dataflow/WeightMap)
- [TransferSkinWeights node reference, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/node-reference/Dataflow/TransferSkinWeights)
- [StaticMeshImport node reference, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/node-reference/Dataflow/StaticMeshImport)
- [Forum: vertex colours for cloth constraints (Epic staff answer 29 May 2026)](https://forums.unrealengine.com/t/can-unreal-engine-dataflow-assets-use-vertex-colors-for-cloth-constraints-instead-of-manual-painting/2380975)
- [Forum: weights from vertex colour (22 April 2025, unanswered)](https://forums.unrealengine.com/t/chaos-cloth-how-to-make-weights-from-vertex-color/2469368)
- [Forum: excluding bones in TransferSkinWeights (29 August 2026)](https://forums.unrealengine.com/t/chaos-cloth-transferskinweights-can-you-exclude-specific-bones-from-influencing-a-region/2747277)
- [Forum: 5.7 UV-seam split after TransferSkinWeights (5 December 2025)](https://forums.unrealengine.com/t/ue-5-7-malignant-bug-convert-to-skeletal-mesh-or-transferskinweights-chaos-cloth-asset-will-cause-the-clothing-model-to-separate-according-to-uv/2682224)
- [Forum: Chaos Cloth updates 5.8 discussion (July 2026)](https://forums.unrealengine.com/t/tutorial-chaos-cloth-updates-5-8/2729420)
