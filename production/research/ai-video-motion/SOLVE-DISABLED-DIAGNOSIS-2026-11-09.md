# Why StartPipeline answers DISABLED (n09-8), diagnosis

All sources read 2026-11-09, read-only. `E` = `C:/Program Files/Epic Games/UE_5.8/Engine`. No program run. DLL strings read with a small Python reader.

## Was the measure wrong?
No. `can_process()` is a real UFUNCTION (`E/Plugins/MetaHuman/MetaHumanAnimator/Source/MetaHumanPerformance/Public/MetaHumanPerformance.h:494-495`), and StartPipeline's DISABLED value is its refusal (`:65-70`). The reason text, `GetCannotProcessTooltipText`, is C++ only (`:608`), so Python cannot read it.

## Causes, likeliest first
1. **The commandlet has no graphics device (likely, about 80%).** The run loaded `NullDrv` (`C:/LedgerTools/ai-video/out/solve-m2s1101c.editor.log:917`). Later lines say "RHI D3D12: no" (`:1205`) and "No or only dummy dynamic RHI" (`:1759`). The Performance DLL's refusal list holds `CannotProcessInvalidRHI`, "please ensure that the RHI is set to {1}" (`.../Binaries/Win64/UnrealEditor-MetaHumanPerformance.dll`, offset 0x117df0). MetaHumanCore has the setting `mh.Core.CheckRHI`, "restricts processing to RHIs known to be supported", with "DirectX 12" as the supported name, and it imports `GDynamicRHI` (`UnrealEditor-MetaHumanCore.dll` 0x39280, 0x3b220, 0x40a58, 0x50da0). The check itself is `FMetaHumanSupportedRHI::IsSupported` (`.../MetaHumanCore/Public/MetaHumanSupportedRHI.h:15`). Commandlets never render unless `-AllowCommandletRendering` is given (`E/Source/Runtime/Core/Public/Misc/App.h:406`, `CoreGlobals.h:296`). This project's full editor picks D3D12 ("Using Default RHI: D3D12", `C:/LedgerTools/mh-assemble/Saved/Logs/MHAssemble.log`). The order of its checks is **unverified** (no body shipped).
2. **Missing authoring objects (unlikely).** This refusal exists (DLL 0x117e80). The content it looks for is installed, for example `E/Plugins/MetaHuman/MetaHumanAnimator/Content/GenericTracker/Chin.uasset`, and MetaHumanCore names `GenericTracker/Chin.Chin` (0x3ffb8).
3. **Footage or range invalid (unlikely).** The footage was accepted and the end frame read 80 (`solve-m2s1101c.json`, diagnostics stage).
4. **Focal length: ruled out.** None of the refusal texts mentions it (DLL 0x116bd0 to 0x117fc0). The body path works out its own focal length every run (`E/Plugins/Marketplace/MetaHumanBodyTracker_5.8/Source/MetaHumanBodyTracker/Private/Nodes/OfflineCameraCalibrationNode.cpp:53,94`; `MetaHumanBodyTracker.cpp:214`). `FocalLength` is VisibleAnywhere (`MetaHumanPerformance.h:387-388`) and belongs to the face path's "Estimate" button (DLL 0x113cd0).

## Next run
- **Python:** no change is needed for CanProcess. The property names are correct (`input_type` 180, `footage_capture_data` 185, `body_tracking` 324, `face_tracking` 314). Two lines would help: log `can_process()` and stop before `start_pipeline()` when it is false. Afterwards, check the log for "Using Default RHI: D3D12".
- **Launch:** a full editor is needed, not the commandlet: `UnrealEditor.exe` (not `-Cmd`), `-ExecutePythonScript=<full path>`, `-unattended -nosplash`, no `-nullrhi`. Epic's page says "Python scripts should be executed using the UnrealEditor executable" and shows only `-ExecutePythonScript` (https://dev.epicgames.com/documentation/metahuman/python-scripting-for-metahuman-animator). Epic's ReadMe says everything except level sequence export "could be invoked in an unattended version of the engine" (`.../MetaHumanAnimator/Content/Python/ReadMe.txt:7`).
- **If blocking stalls:** use the start-up-script-with-tick pattern (`tools/ue/request_metahuman_textures.py:13-20`). The editor closes when an `-ExecutePythonScript` script returns. **Unverified** whether a blocking run gets through all five body stages.
- **Second choice:** the commandlet with `-AllowCommandletRendering` (**unverified** for this pipeline). Setting `mh.Core.CheckRHI=0` under NullRHI is not advised, because the body tracker's neural nets use render-graph code (`.../BodyTracker/Private/NNEUtils.cpp:99-130`).
- **Risk after it starts:** this PC has an AMD Radeon RX 6700 (Win32_VideoController). An RX 6700 XT user hit a D3D12 crash in this plugin (forum post 32, https://forums.unrealengine.com/t/2729293.json, all 54 posts).

## Not reached or not checked
- The body of `UMetaHumanPerformance::CanProcess`; no .cpp ships.
- Whether MetaHumanCore skips its "Unsupported RHI" log line in commandlets; the line is absent from the run's log.
- Epic's Blueprint and mono pages: not re-read.
