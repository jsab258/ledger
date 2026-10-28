# Asset checks: web sources (read 28 Oct 2026)

Every page below was read in full in the browser pane. All Epic pages were titled "Unreal Engine 5.8 Documentation". Summaries are in my own words. "Same" means the URL given just above.

## 1. Epic's Data Validation, Asset Audit, Validate Assets

- The Data Validation plugin is on by default. Its stated uses are naming conventions, space and performance budgets, and dependency faults (https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine, read 28 Oct 2026).
- Editor entry points (same, read 28 Oct 2026):
  - In the Content Browser: Asset Actions > Validate Assets, and Asset Actions > Validate Assets and Dependencies.
  - On a folder: Validate Assets in Folder.
  - For the whole project: Tools > Validate Data...
- **Epic's documented headless line is exactly `UnrealEditor-Cmd.exe <PROJECT_NAME>.uproject -run=DataValidation`.** The page lists no other arguments. By default the commandlet runs only C++ rules; Blueprint and Python rules need the system extended, and Epic does not say how (same, read 28 Oct 2026).
- There are two ways to write a rule (same, read 28 Oct 2026):
  - (a) Override `IsDataValid` on your own class.
  - (b) Subclass `UEditorValidatorBase` in C++, Blueprint or Python and implement `CanValidateAsset` and `ValidateLoadedAsset`. `ValidateLoadedAsset` must call `AssetPasses` or `AssetFails` on every path. `IsEnabled` returns `bIsEnabled` by default.
- Registration and where results appear (same, read 28 Oct 2026):
  - C++ and Blueprint validators are found automatically when the editor starts.
  - Python validators must call `AddValidator` on `UEditorValidatorSubsystem`.
  - Validation runs in CI, on save (on by default) and from the menus. Results go to the Message Log in the editor or to the console in CI.
- `UEditorValidatorBase` C++ API (https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/DataValidation/UEditorValidatorBase, read 28 Oct 2026):
  - Calls to report results: `AssetPasses`, `AssetFails`, `AssetWarning`, `AssetMessage`, `GetValidationResult`.
  - Virtual functions to override: `IsEnabled`, `PostAssetValidation` and `GetAssetsToValidateFromChangelist`.
  - Blueprint events: `K2_CanValidate`, `K2_CanValidateAsset`, `K2_ValidateLoadedAsset`.
  - C++ implementations, which take `(FAssetData, UObject*, FDataValidationContext&)`: `CanValidateAsset_Implementation` and `ValidateLoadedAsset_Implementation`.
  - The engine ships `UEditorValidator_Material` and `UEditorValidator_Localization`.
- Project Settings (`UDataValidationSettings`) offers `bValidateOnSave`, `bLoadAssetsWhenValidatingChangelists`, `bEnableMaterialValidation` and `MaterialValidationPlatforms` (https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/DataValidation/UDataValidationSettings, read 28 Oct 2026).
- The commandlet class's API lists no switches (https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/DataValidation/UDataValidationCommandlet, read 28 Oct 2026):
  - It exposes virtual hooks a project can subclass to add its own: `ProcessCommandLine(Tokens, Switches, Params)`, `GetAssetsToValidate`, `FilterAssetsToValidate`, `SetupValidationSettings` and `ProcessValidationResults`.
  - It also has a static `ValidateData(FullCommandLine)` that runs without commandlet mode.
- Asset Audit window:
  - It opens from Tools > Audit > Asset Audit (https://dev.epicgames.com/documentation/en-us/unreal-engine/preparing-assets-for-chunking-in-unreal-engine, read 28 Oct 2026).
  - It is a chunk and size inspector, not a rule checker. "Add Chunks" fills it, and right-clicking a chunk gives Size Map (disk or editor memory) or the Reference Viewer (https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-and-creating-chunks-in-unreal-engine, read 28 Oct 2026).
- An Epic-hosted talk with a measured gain: "Enhanced Validation: Lessons From a Custom AAA Implementation" (LightspeedLA, Unreal Fest Bali, posted 11 Mar 2026).
  - They extended validation to actors and capped the search depth into Level Instances.
  - The abstract reports going "from multiple build breakages a day" to about two or three support requests a week.
  - It also mentions a coming "Fixer framework" for self-service fixes.
  - I read the abstract only and did not watch the video (https://dev.epicgames.com/community/learning/talks-and-demos/2Kqx/unreal-engine-enhanced-validation-lessons-from-a-custom-aaa-implementation, read 28 Oct 2026).

## 2. Naming: Epic vs Allar

- Epic's pattern is `[AssetTypePrefix]_[AssetName]_[Descriptor]_[OptionalVariantLetterOrNumber]`, offered "only a recommendation" (https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects, read 28 Oct 2026).
- Epic's prefixes (same, read 28 Oct 2026):
  - Materials and textures: M_, MI_, PPM_, T_, HDR_.
  - Meshes and physics: SM_, SK_, PHYS_, PM_.
  - Blueprints and data: BP_, ABP_, AC_ (actor component), BI_, WBP_, DT_, CT_, E_, F_.
  - Animation: SKEL_, Rig_, AS_, AM_, BS_, LS_.
  - Niagara: FXS_, FXE_, FXF_.
  - Epic gives **no texture suffixes** and no rules on folders, spaces or characters.
- Allar's guide. The `main` branch is still headed UE4; the `v2` branch is marked as a draft. The tables are the same on both (https://raw.githubusercontent.com/Allar/ue5-style-guide/main/README.md and https://raw.githubusercontent.com/Allar/ue5-style-guide/v2/README.md, read 28 Oct 2026).
  - Pattern: `Prefix_BaseAssetName_Variant_Suffix`, with two-digit variants starting at 01.
  - Prefixes: S_ (static mesh; the guide notes many use SM_), SK_, SKEL_, M_, MI_, MF_, MPC_, PP_, PM_, PHYS_, T_, TC_, RT_, BP_, BPI_, BPFL_, ABP_, A_ (anim sequence), AM_, AC_ (anim composite), BS_, CR_, WBP_, PS_. Enums take E and structs F or S, with no underscore.
  - Texture suffixes: _D, _N, _R, _A, _O, _E, _B, _S, and _M for both mask and metallic (the clash is in the guide itself). Packed maps stack the letters in channel order (the guide's example is _ERO), so an ORM pack is _ORM.
  - Identifiers: never whitespace, backslash, symbols or "Any Unicode character"; target `[A-Za-z0-9_]+`.
  - Folders: PascalCase, no spaces, no Unicode, Maps in a folder called Maps, no folders named Assets, Meshes or Textures, no empty folders.
  - Textures: power-of-two sides (non-square allowed, UI exempt), at most 8192, and the right Texture Group.
  - Meshes: UVs present, non-overlapping lightmap UVs, LODs, collision on every mesh, correct scale.
- Where they differ:
  - SM_ vs S_; AS_ vs A_; BI_ vs BPI_; E_ vs E; F_ vs F/S; PPM_ vs PP_.
  - **AC_ means actor component for Epic but animation composite for Allar.**
  - Epic has Niagara prefixes and Allar does not.
  - Allar adds texture suffixes and rules on characters and folders.

## 3. Budgets checked by machine

- **Nanite** (https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine, read 28 Oct 2026):
  - Epic says to enable it wherever supported; the named exception is a sky sphere.
  - Only Opaque and Masked materials are supported; Translucent falls back to a default material with a warning.
  - No Morph Targets. World Position Offset (WPO) works but is limited.
  - Not supported: Forward rendering, VR stereo, MSAA, lighting channels, distance culling.
  - 16 million instance cap; needs DX12 with SM6.
  - The page lists Nanite Skeletal Mesh (no geometry LODs; animation LODs instead) but also says Nanite applies to Static Meshes and Geometry Collections, which conflicts.
- Nanite foliage is Beta, and aggregate geometry (hair, leaves, grass) defeats Nanite's scaling (https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-naniteenabled-content, read 28 Oct 2026).
- **Textures:**
  - Power-of-two sizes stream and get mips, and "Non-power of two sizes are never streamed". Some GPUs cap textures at 8192 (https://dev.epicgames.com/documentation/en-us/unreal-engine/textures-in-unreal-engine, read 28 Oct 2026).
  - Refinement: non-power-of-two textures can have mips if Mip Gen Settings is changed from NoMipMaps, but streaming still needs power of two, and compression needs a top mip that is a multiple of 4. The page also documents Power of Two Mode padding, Maximum Texture Size (0 means the platform maximum), Texture Group and Never Stream (https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-asset-editor-in-unreal-engine, read 28 Oct 2026).
- **Skeletal LODs** (https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletal-mesh-lods-in-unreal-engine, read 28 Oct 2026):
  - Generated with the Reduction plugin; regenerating overwrites imported LODs.
  - Controls: Bones and Sections to Prioritize, Lock Mesh Edges, Bones to Remove, Max Bone Influence per LOD.
  - Termination criteria by percent or maximum triangles or vertices. Memory follows vertices.
  - **No triangle numbers.**
- MetaHuman mapping: the face uses LODs 1/3/5/7 and the body 0 to 3. No counts are given (https://dev.epicgames.com/documentation/en-us/metahuman/metahuman-lods-in-uefn, read 28 Oct 2026).
- **FBX collision and LODs** (https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine, read 28 Oct 2026):
  - Collision shapes are recognised by name: `UBX_`, `UCP_`, `USP_` or `UCX_` + `[RenderMeshName]_##`, matching the render mesh name exactly.
  - Boxes and spheres fail on non-uniform scale, so UCX is preferred. Hulls should not intersect.
  - In a multi-mesh file only the first mesh's collision imports.
  - `SOCKET_` marks sockets. LODs share a pivot. The page says the pipeline uses FBX 2020.2.
- Simple collision means primitives and convex hulls; complex collision is the triangle mesh. "Use Complex As Simple" stops the object from simulating (https://dev.epicgames.com/documentation/en-us/unreal-engine/simple-versus-complex-collision-in-unreal-engine, read 28 Oct 2026).
- Lightmap UVs are generated on import by default from UV0 into UV1. Charts are repacked but never split, so a bad UV0 gives a bad lightmap (https://dev.epicgames.com/documentation/en-us/unreal-engine/generating-lightmap-uvs-in-unreal-engine, read 28 Oct 2026).
- **No Epic triangle budget** for characters or props was found. Nanite's stated principle is to draw about as many triangles as there are pixels (working-with-naniteenabled-content, above).
- Studio talks:
  - Respawn's GDC session (Cole O'Brien) used automated validation to keep visual regression minimal during a USD migration. No numbers (https://schedule.gdconf.com/session/building-a-usd-pipeline-for-apex-legends/922058, read 28 Oct 2026).
  - LightspeedLA's gain is in section 1.

## 4. Python validators

- **The 5.8 Python names have changed.** `can_validate_asset`, `validate_loaded_asset` and `can_validate` are marked deprecated, renamed to `k2_can_validate_asset(asset)`, `k2_validate_loaded_asset(asset) -> DataValidationResult` and `k2_can_validate(usecase)`. The helpers are `asset_passes`, `asset_fails` and `asset_warning` (https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorValidatorBase?application_version=5.8, read 28 Oct 2026).
- The subsystem offers `add_validator`, `remove_validator` (call it at shutdown), `is_object_valid` and `validate_assets_with_settings`, which is used "from either the UI or a commandlet". `validate_on_save` is deprecated in favour of the setting (https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorValidatorSubsystem?application_version=5.8, read 28 Oct 2026).
- In `ValidateAssetsSettings`, `load_assets_for_validation` defaults to False, which skips unloaded assets. Other fields include `capture_warnings_during_validation_as_errors` and `validation_usecase` (https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ValidateAssetsSettings?application_version=5.8, read 28 Oct 2026).
- `DataValidationUsecase` values: NONE, MANUAL, COMMANDLET, SAVE, PRE_SUBMIT, SCRIPT (https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/DataValidationUsecase?application_version=5.8, read 28 Oct 2026).
- How Python starts (https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python, read 28 Oct 2026):
  - `init_unreal.py` in any Python path (for example Content/Python) runs immediately when the editor finds it.
  - Project Settings startup scripts run after the startup level loads.
  - The headless form is `-run=pythonscript -script=<file>`, which loads no level.
- The community pattern is a `@unreal.uclass()` subclass with `@unreal.ufunction(override=True)` overrides, then `get_editor_subsystem(EditorValidatorSubsystem).add_validator(instance)`. These examples are from 2020 and use the old two-argument signature (https://unrealcommunity.wiki/asset-validator-python-pddba19x, https://gist.github.com/DashW/289fe98d89ee45a01814f1d7224b7751, read 28 Oct 2026). A newer post overrides the `k2_` names (https://tianc377.github.io/posts/UnrealPythonAssetValidator/, read 28 Oct 2026).
- **Limitation:**
  - A user's Python validators work in the GUI editor but could not be made to run in `-run=DataValidation`. The thread has no replies and is marked Unresolved (https://forums.unrealengine.com/t/python-validators-registration-for-unrealeditor-cmd-exe/2293556, read 28 Oct 2026).
  - A pythonscript that called `validate_assets_with_settings` checked far fewer assets than the commandlet. No answer was posted (https://forums.unrealengine.com/t/data-asset-validation-python-vs-cpp-commandlets/672144, read 28 Oct 2026).
  - Treat Python validators as **not run by `-run=DataValidation`** until a probe shows otherwise.

## Not reached

- GDC Vault (including the AC Origins world-data validation talk, 1025054): it redirected to a maintenance page, and an archive copy was refused by the permission check.
- The Virtuos "Asset Health Metrics" session on schedule.gdconf.com: 404.
- stevestreeting.com's Unreal asset validation post: 403.
- Epic's tutorial "Data Validation: What you need to know" (learning/tutorials/ZkP): 404.
- Lyra's validators: no public page found, and Epic's GitHub needs sign-in.
- The 5.x "Unwrapping UVs for Lightmaps" page and the `UPythonScriptPluginSettings` API page both redirected to the docs home.

## Unverified

- Any `-run=DataValidation` switch beyond the bare line.
- Whether `init_unreal.py` runs under `-run=DataValidation` or `-run=pythonscript`, which decides whether a registered Python validator takes part. A probe validator that logs would settle it.
- Whether Blueprint validators run in the commandlet.
- Whether the Interchange importer honours UCX_ names exactly as the FBX page describes.
- Whether Nanite Skeletal Mesh is production-ready in 5.8.
- The year of the Respawn session.
- My inference that the forum's gap in item 4 came from `load_assets_for_validation` defaulting to False.
