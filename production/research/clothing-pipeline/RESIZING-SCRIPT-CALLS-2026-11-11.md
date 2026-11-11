# Resizable outfit: script-callable calls (item n09-6, read 11 Nov 2026)

Source only, UE 5.8.4, files read, nothing run. P = Engine/Plugins, S = Engine/Source/Runtime. "Python-exposed" means FUNC_BlueprintCallable or BlueprintEvent, no ScriptNoExport (P/Experimental/PythonScriptPlugin/Source/PythonScriptPlugin/Private/PyGenUtil.cpp:1615-1625). Struct fields count only if BlueprintVisible (PyGenUtil.cpp:1609, 1774-1793). Nothing was run, so runtime behaviour is unverified.

## 1. Calls from editor Python

(a) ChaosClothAsset
- No Python-exposed call builds a cloth asset from a skeletal mesh, static mesh or USD. The import nodes are graph nodes only: SkeletalMeshImport (P/ChaosClothAssetDataflowNodes/.../Public/ChaosClothAsset/SkeletalMeshImportNode.h:18,25), StaticMeshImport (StaticMeshImportNode.h:19), USDImport (P/ChaosClothAssetUsdDataflowNodes/.../Private/ChaosClothAsset/USDImportNode_v3.h:18).
- UChaosClothAssetToolset.CreateClothingAsset and 5 siblings carry only meta=(AICallable), no BlueprintCallable (P/Experimental/Toolsets/ChaosClothAssetToolset/.../Private/ChaosClothAsset/ClothAssetToolset.h:55-135). Not Python-exposed. Its plugin is off by default and the functions only attach an existing cloth/outfit asset to a skeletal mesh.
- UChaosClothAssetFactory is a UFactory (P/ChaosClothAsset/Source/ChaosClothAssetTools/Public/ChaosClothAsset/ClothAssetFactory.h:16-28; class marked Experimental). Via the asset-tools create call, non-interactive runs (-unattended, commandlet, GIsRunningUnattendedScript) embed DF_EmptyClothAssetTemplate and return an empty cloth asset (ClothAssetFactory.cpp:29-39). Interactive runs open a template picker (ClothAssetFactory.cpp:41-51).
- Interchange route, USD only: UInterchangeManager (ScriptedImportAssetAsync, S/Interchange/Engine/Public/InterchangeManager.h:693-694; ImportAsset :647-648; GetInterchangeManagerScripted :487-488) with UInterchangeChaosClothAssetPipeline (BlueprintReadWrite bImportClothAssets, bImportSimulationMeshes, bImportRenderMeshes, DataflowGraphAsset; P/Interchange/Extensions/ChaosClothAsset/Source/Import/Public/InterchangeChaosClothAssetPipeline.h:15-46) and UInterchangeOpenUSDChaosClothAssetPipeline (OpenUSDChaosClothAsset/.../Public/*Pipeline.h:15-41). It only picks up scene nodes tagged "ClothRoot" (InterchangeChaosClothAssetPipeline.cpp:41-45, tag set at InterchangeOpenUSDChaosClothRootAssetSchemaHandler.cpp:1180), so a plain FBX is not covered. Both Interchange plugins: EnabledByDefault false, Experimental.

(b) Outfit asset
- UChaosOutfitAsset is BlueprintType (P/ChaosOutfitAsset/Source/ChaosOutfitAssetEngine/Public/ChaosOutfitAsset/OutfitAsset.h:17) with no UFUNCTION; Build is native only (:26).
- UChaosOutfitAssetFactory creates one, but its create step calls SetDataflowFromTemplatePicker (ChaosOutfitAssetEditor/Private/ChaosOutfitAsset/OutfitAssetFactory.cpp:23-37). That returns at once with no graph when non-interactive (P/Dataflow/Source/DataflowEditor/Private/Dataflow/AssetDefinition_DataflowAsset.cpp:231-236); interactive it shows a modal picker.
- UChaosClothAssetBase::SetDataflow/GetDataflow are plain C++ (ClothAssetBase.h:309-315). The Dataflow slot is FDataflowInstance, a plain USTRUCT() with no BlueprintVisible field (S/Dataflow/Engine/Public/Dataflow/DataflowInstance.h:208-209). It is probably not a Python struct (unverified), so the graph cannot be assigned by property.
- UDataflowAgentToolset.CreateDataflowCompatibleAssetFromTemplate, AssignDataflowTemplate, ListDataflowTemplatesForAssetClass: AICallable only, not Python-exposed (P/Experimental/Toolsets/DataflowAgent/.../Private/DataflowAgentToolset.h:296-311). Same for its ListVariables/AddVariable/SetVariable (:164-204). Plugin EnabledByDefault false, NoRedist.
- Workaround, unverified: duplicate an existing OA_ asset (its embedded graph copies), or let the Interchange pipeline's DataflowGraphAsset set the graph for cloth assets.

(c) Re-run a graph (UDataflowBlueprintLibrary, S/Dataflow/Engine/Public/Dataflow/DataflowBlueprintLibrary.h, all BlueprintCallable)
- RegenerateAssetFromDataflow(Asset, bRegenerateDependentAssets) :61-62, calls FDataflowInstance::UpdateOwnerAsset (DataflowBlueprintLibrary.cpp:70-78). This is the call the MetaHuman pipeline itself uses after setting variables (P/MetaHuman/MetaHumanCharacter/.../MetaHumanOutfitEditorPipeline.cpp UpdateOwnerAsset(true), after line 100).
- EvaluateTerminalNodeByName(Dataflow, TerminalNodeName, ResultAsset) :43-44, impl .cpp:12-38.
- EvaluateDataflow(Dataflow, Asset) :54-55. Its impl returns bHasError, so true means an error occurred (.cpp:40-68, return at 64).

(d) Variables and node inputs
- OverrideDataflowVariableBool/Int/Float/Object/ObjectArray (+Bool/Int/Float arrays), by asset and name :68-118; read back with GetDataflowVariableList :120-121. These set per-asset overrides (e.g. TargetBody, ResizableOutfit, StripSimMesh) without touching the shared graph. Name and string overrides exist in C++ only (DataflowInstance.h:118-124); the pipeline uses OverrideVariableName for OverrideBodySizeName (MetaHumanOutfitEditorPipeline.cpp:~100).
- UDataflowEditorBlueprintLibrary (P/Dataflow/Source/DataflowEditor/Private/Dataflow/DataflowEditorBlueprintLibrary.h:19-32): AddDataflowNode, ConnectDataflowNodes, AddDataflowFromClipboardContent, SetDataflowNodeProperty(Graph, Node, Property, StringValue). These edit the graph itself, so duplicate a template first.

## 2. Outfit nodes (P/ChaosOutfitAsset/Source/ChaosOutfitAssetDataflowNodes/Private/ChaosOutfitAsset/*.h); none flagged Experimental unless stated

- MakeOutfit (MakeOutfitNode.h:20): in cloth assets (add pins); out Outfit.
- MakeSizedOutfit (MakeSizedOutfitNode.h:19): in SizedOutfitSources[] (SizedOutfitSource.h:26-50: SourceAsset, SizeName, SourceBodyParts, NumResizingInterpolationPoints, default 1500 per OutfitCollection.h:65, max 5000); out Outfit, OutfitCollection.
- FilterSizedOutfit (FilterSizedOutfitNode.h:19): in Outfit, SizeName, TargetBody; out Outfit, OutfitCollection, SizeName. Empty SizeName: size chosen from the TargetBody's measurements (:41-49).
- GetOutfitBodyParts (GetOutfitBodyPartsNode.h:30) and ExtractBodyPartsArrayFromBodySizeParts (:56): in Outfit; out BodySizeParts / BodyParts.
- GetOutfitRBFInterpolationData (GetOutfitRBFInterpolationDataNode.h:18): in Outfit, BodySizeIndex, BodyPartIndex; out InterpolationData.
- GetOutfitClothCollections (GetOutfitClothCollectionsNode.h:14, Experimental): in Outfit, LOD Index; out ClothCollections, Num LODs.
- SetOutfitClothCollection (SetOutfitClothCollectionNode.h:15, Experimental): in Outfit, ClothCollection, indices; out Outfit.
- OutfitQuery (OutfitQueryNode.h:20): in Outfit, flags bBodyPartMustExist, bMeasurementsMustExist, bInterpolationDataMustExist; out bHasAnyValidPieces, bHasAnyValidBodySizes.
- GetOrMakeOutfitFromAsset (:21), GetOutfitAsset (:18), GetClothAsset (:18), MergeOutfits (:17): asset in, Outfit out.
- OutfitAssetTerminal (OutfitAssetTerminalNode.h:18): in Outfit; button ConvertToSkeletalMesh (a Dataflow function property opening a Save dialog, OutfitAssetTerminalNode.cpp:36-60; not a UFUNCTION).
- Cloth-side resizing nodes (P/ChaosClothAssetDataflowNodes/.../Public/ChaosClothAsset/): ApplyResizing (ApplyResizingNode.h:13, Experimental): in cloth collection, TargetSkeletalMesh (must have matching vertices with the source, :28), SkeletalMeshLODIndex, InterpolationData, bForceApplyToRenderMesh, SourceSkeletalMesh, bSkipCustomRegionResizing, bSavePreResizedSimPosition3D (:28-57). CustomRegionResizing (CustomRegionResizingNode.h:29, Experimental); EnableUVResizing (EnableUVResizingNode.h:9, Experimental).
- GenerateRBFResizingWeights is in the MeshResizing plugin; the MakeResizableOutfit template uses it (found only as binary strings in the .uasset).
- Template variables, binary strings only: ResizeOutfitTemplate holds TargetBody, ResizableOutfit, StripSimMesh, TransferSkinWeights, GenerateLOD0Only, OverrideBodySizeName, ResizeUVs, CustomRegionResizing, Prune/Relax/Hammer/Clamp/NormalizeSkinWeights.

## 3. MetaHuman character side

- Subsystem UFUNCTIONs, all BlueprintCallable (P/MetaHuman/MetaHumanCharacter/Source/MetaHumanCharacterEditor/Public/MetaHumanCharacterEditorSubsystem.h): TryAddObjectToEdit :528, GetPreviewCollection :558, OnEditPreviewCollection :567, AssembleForPreview :571, CanBuildMetaHuman :776, BuildMetaHuman(Character, Params) :787. Build params: Subsystem/MetaHumanCharacterBuild.h:25-75 (PipelineType, PipelineQuality, AbsoluteBuildPath, NameOverride, CommonFolderPath, bEnableWardrobeItemValidation; BlueprintReadWrite).
- UMetaHumanInstance.Assemble :143, TryAddSlotSelection :224, SetSingleSlotSelection :219 (MetaHumanInstance.h). These select an item already in the collection.
- Adding a wardrobe item: TryAddItemFromWardrobeItem / TryAddItemFromPrincipalAsset are plain C++ (MetaHumanCharacterPalette.h:85,94); Items is a bare UPROPERTY() (:224). Not Python-exposed. No script call adds an outfit to a character.
- Fit: MetaHumanOutfitEditorPipeline.cpp:49-100 makes a new UChaosOutfitAsset, sets the resize graph, overrides TargetBody = the character's merged head+body mesh and ResizableOutfit = the OA_ asset, then UpdateOwnerAsset. Size choice: FindClosestBodySize by measurements (CollectionOutfitFacade.cpp:592-638; names Hip, Bust/Chest, Underbust, Waist, Neck to Waist, Rise, Inseam at :219-231), read from UChaosOutfitAssetBodyUserData (BodyUserData.h:19-20, VisibleAnywhere; written by the MetaHuman subsystem at MetaHumanCharacterEditorSubsystem.cpp:2133, 2210, 5030). Warp: RBF interpolation (not vertex correspondence for the garment). Sample points are generated from the source body's LOD0 mesh description at make time (Outfit.cpp:425-436); ApplyResizing deforms sim or render points with FRBFInterpolation::DeformPoints (ApplyResizingNode.cpp:86,107). The target body must have vertices matching the source body (ApplyResizingNode.h:28).
- Bake: Production quality (collection default, MetaHumanCollection.h:325) bakes the outfit with ExportToSkeletalMesh (MetaHumanOutfitEditorPipeline.cpp:141-146); Preview keeps the outfit asset plus body (:152-156). The editor sets the preview collection to Preview (MetaHumanCharacterEditorSubsystem.cpp:1163). Whether BuildMetaHuman always runs Production: not confirmed. ExportToSkeletalMesh itself is C++ only (ClothAssetBase.h:359).

## 4. Not reachable from script

- Attaching a Dataflow graph to a new cloth or outfit asset (picker is modal; setter not exposed).
- Adding a wardrobe item or outfit to a character's collection; creating the wardrobe item's pipeline binding.
- Outfit to skeletal mesh export outside a full character build (the terminal's button is a dialog).
- Setting a body's measurements (EditConst data), and reading fit quality from the outfit.
- The cloth asset from FBX or a plain mesh (needs the graph's import node with its picker, or USD with a ClothRoot).
- Toolset functions (AICallable) are not Python-exposed.

## Smallest script-only route: none found end to end

Closest partial route, each step unverified at runtime:
1. Python: import a ClothRoot USD with the Interchange cloth pipeline (needs both Interchange plugins on), or duplicate an existing CA_ asset.
2. Duplicate an existing OA_ asset (from the Resizable Outfit template); SetDataflowNodeProperty on the copy's graph to point its sources at the garment and bodies.
3. RegenerateAssetFromDataflow on the OA_ asset (several minutes for RBF weights).
4. Create a second outfit by duplicating a Resize-template asset; OverrideDataflowVariableObject for TargetBody and ResizableOutfit, bools for StripSimMesh and TransferSkinWeights; RegenerateAssetFromDataflow.
5. Measure: no script call turns the resized outfit into a mesh, so the measuring step needs the editor's Convert button or a built character; the pipeline's Production assembly is the only baked output.
