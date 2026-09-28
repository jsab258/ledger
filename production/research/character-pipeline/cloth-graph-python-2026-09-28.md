# Unreal's cloth graph from Python, checked on this PC (28 September 2026)

The 24 September try (production/research/clothing-pipeline/TRIED-2026-09-24.md) found "in 5.8 the graph's inputs are protected from Python"; the 27 September research (clothing-and-face-lighting-2026-09-27.md) says the graph is scriptable. Checked in the installed engine, UE 5.8, 28 September:

- `Engine/Plugins/Dataflow/Source/DataflowEditor/Private/Dataflow/DataflowEditorBlueprintLibrary.h` declares, each `UFUNCTION(BlueprintCallable)` and so reachable from Python as `unreal.DataflowEditorBlueprintLibrary`:
  - `AddDataflowNode(Dataflow, NodeTypeName, BaseName, Location)`
  - `ConnectDataflowNodes(Dataflow, FromNodeName, OutputName, ToNodeName, InputName)`
  - `AddDataflowFromClipboardContent(Dataflow, ClipboardContent, Location)`: a whole graph pasted from its copied text
  - `SetDataflowNodeProperty(Dataflow, NodeName, PropertyName, PropertyValue)`: a property set from a string
- The templates are installed:
  - `ChaosClothAsset/Content/`: DF_StaticMeshClothTemplate, DF_SkeletalMeshClothTemplate, DF_ClothSolver, ClothAssetTemplate.
  - `ChaosOutfitAsset/Content/`: MakeResizableOutfitTemplate, ResizeOutfitTemplate, OutfitAssetTemplate.

So the route is: a copy of DF_StaticMeshClothTemplate with our render and simulation meshes set as its inputs; then MakeResizableOutfitTemplate pairing the cloth with the body it was made on; then ResizeOutfitTemplate per build with Strip Sim Mesh false (Epic's 5 August 2026 forum answer, cited in the 27 September research).

Documented: the four functions and the templates, read from the installed files. Not yet run: whether SetDataflowNodeProperty reaches the inputs the 24 September try found protected (that try named no function); that is the first thing to run.
