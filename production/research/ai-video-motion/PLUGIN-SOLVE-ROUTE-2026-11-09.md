# Markerless body solve without the editor UI: route notes (item n09-8)

Read 2026-11-09. Read-only. No program started. Local root: `E` = `C:\Program Files\Epic Games\UE_5.8\Engine\Plugins`.

## Short answer
The body plugin has no Python or Blueprint API of its own. It is a pipeline extension that the MetaHuman Animator Performance asset calls. The scripted route is therefore the Performance asset's own API (process_monocular_performance.py plus export), with `body_tracking` switched on. One export step looks blocked for scripts (section 2, item B). Whether it runs in a commandlet is unverified.

## 1. Steps (Epic documentation)
Pages read 2026-11-09 through the fetch tool (it returns a model's summary, not verbatim text; see "Not reached"):
- Overview: https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine. Experimental in 5.8, Windows only. Needs MetaHuman Animator, Live Link Hub, Capture Manager Editor, and the plugin from Fab.
- Ingest: https://dev.epicgames.com/documentation/metahuman/metahuman-animator-01-import-your-footage-in-unreal-engine. Mono Video Ingest in Live Link Hub makes a capture data asset (image sequence). The default transcoder is Windows Media Framework. FFmpeg "can reduce the risk of invalid FPS". The page gives no frame-rate rule.
- Process and export: https://dev.epicgames.com/documentation/metahuman/metahuman-animator-02-process-and-export-your-animation-in-unreal-engine. New MetaHuman Performance asset, Footage Capture Data set. Body only: Facial Tracking off, Body Tracking on, Head Movement Mode Disable. Click Process, then Export Animation. Skeleton choice: Existing Skeleton (a MetaHuman skeletal mesh, retargeted automatically) or Performer Skeleton (new mesh, for non-MetaHuman characters).
- Blueprint page: https://dev.epicgames.com/documentation/metahuman/process-and-export-metahuman-animation-with-blueprints-in-unreal-engine. Set input type mono, set footage capture data, set blocking processing, StartPipeline(scripted = true), then GetExportAnimationSequenceSettings and ExportAnimationSequence. "Setting the variable without the plugin enabled has no effect." It says process_monocular_performance.py is the Python equivalent.
- Scripting overview: https://dev.epicgames.com/documentation/metahuman/scripting-and-automating-metahuman-animator-in-unreal-engine. Python suits headless runs; the page does not mention commandlets and states no GPU needs.

Processing runs five pipeline stages (0 to 4: camera calibration, body detection, 2D keypoints, pose estimation, finalise), `E\Marketplace\MetaHumanBodyTracker_5.8\Source\MetaHumanBodyTracker\Private\MetaHumanBodyTracker.cpp:51,94,127,155,187`.

## 2. What is exposed (installed files)
Plugin `E\Marketplace\MetaHumanBodyTracker_5.8\`: `MetaHumanBodyTracker.uplugin` (beta, experimental, modules MetaHumanBodyTracker, BodyTracker, Segmentation, MetaHumanBodyOptimizer). Source is shipped; binaries too. There is no Python folder. The only UCLASS/USTRUCT are `AMetaHumanBodyDriverActor` (`Private\MetaHumanBodyDriverActor.h:14`), `UMetaHumanSMPLX` (`Private\MetaHumanSMPLX.h:12`) and `SAM2WeightsRow` (`Segmentation\Private\SAM2WeightsRow.h:21`). No UFUNCTION anywhere in the plugin. It registers a modular feature (`MetaHumanBodyTrackerModule.cpp:12`); `ExtendPipeline` is C++ only (`MetaHumanBodyTracker.h:13`).

The scriptable surface is in the MetaHuman Animator plugin:
- `UMetaHumanPerformance` (`E\MetaHuman\MetaHumanAnimator\Source\MetaHumanPerformance\Public\MetaHumanPerformance.h`):
  - `InputType` (line 180) with setter `SetInputType` (503); enum `EDataInputType::MonoFootage` (39).
  - `FootageCaptureData` (185) with `SetFootageCaptureData` (499). It rejects footage with an invalid frame rate and sets null (comment at 497).
  - `bBodyTracking` (324) with `SetBodyTracking` (534); `bFaceTracking` (314, BlueprintReadWrite); `bAutoBodyHeight` (329); `BodyHeight` (333); `BodyDetectionConfidence` (340); `BodyTrackingConfidence` (347); `bEnableFootLocking` (352); `bSkipPreview` (304); `MonoSmoothingParams` (417); `HeadAllowedRotation*` (399, 406).
  - `SetProcessingRange(int32, int32)` (520); `SetBlockingProcessing(bool)` (531); `StartPipeline(bool bInIsScriptedProcessing = true)` returning `EStartPipelineErrorType` (486, enum at 65); `CancelPipeline` (489); `IsProcessing` (492); `CanProcess` (495); `ContainsAnimationDataType` (555); `GetNumberOfProcessedFrames` (563).
- `UMetaHumanPerformanceExportUtils` (`...\Public\MetaHumanPerformanceExportUtils.h`): `GetExportAnimationSequenceSettings` (302), `ExportAnimationSequence(performance, settings)` (310), `ExportLevelSequence` (314). `CanExportBodyAnimation` (326) is C++ only.
- `UMetaHumanPerformanceExportAnimationSettings` (48): `bExportBody` (96), `bExportFace` (90), `ExportSkeleton` (101; `ExistingSkeleton` or `PerformerSkeleton`, enum near line 30), `TargetSkeletonOrSkeletalMesh` (106), `BodyRetargeter` (111), `BodyUnsolvedBehavior` (118), `bShowExportDialog` (71), `PackagePath`/`AssetName` (131,135), `ExportRange` (84).
- Ingest: `UCaptureManagerIngestBlueprintLibrary` (`E\VirtualProduction\CaptureManager\CaptureManagerEditor\Source\CaptureManagerIngestBlueprint\Private\CaptureManagerIngestBlueprintLibrary.h:105`). `IngestMonoVideoSync(VideoFilePath, AudioFilePath, Slate, TakeNumber, Params, OutErrorMessage)` returns `UFootageCaptureData*` (153); doc says ".mp4 or .mov" (143). Params struct `FCaptureManagerConversionParams` (36: image format Png/Jpg, rotation Auto). Python usage shown in `...\CaptureManagerEditor\Content\Python\example_ingest_scan.py:77` (`cm.ingest_mono_video_sync(video, audio, slate, take_num, params)` returns a tuple of asset and error).

Two open points in the scripted export (header facts, no .cpp shipped, so behaviour unverified):
- A. `SourceSkeletalMesh` and `SMPLSourceSkeletalMesh` (`ExportUtils.h:139,144`) are `UPROPERTY(Transient)` only, with the comment "Required for body export... Scripted callers must set it manually." Without BlueprintReadWrite or EditAnywhere they are probably not reachable from Python. Possibly `GetExportAnimationSequenceSettings` fills them; unverified. The meshes come from `IMetaHumanBodyTrackerInterface::MakeMHSkeletalMesh` (`MetaHumanBodyTrackerInterface.h:115`), C++ only.
- B. The Epic export script (`E\MetaHuman\MetaHumanAnimator\Content\Python\export_performance.py:21-40`) sets a face skeleton and never body fields, so it is face-only. No body example ships.

## 3. Epic Python examples (all under `E\MetaHuman\MetaHumanAnimator\Content\Python\`)
- `process_monocular_performance.py:8-58`: creates a Performance (`MetaHumanPerformanceFactoryNew`), sets `input_type` MONO_FOOTAGE and `footage_capture_data`, then `process_shot`. Does not set body tracking.
- `process_performance.py:33-58`: `set_blocking_processing(True)`, `start_pipeline()`, checks `StartPipelineErrorType.NONE`. Its depth-footage mode needs an identity.
- `export_performance.py`: anim sequence and level sequence export (section 2, B). Comment in `process_performance.py:62`: level sequence export "not supported in headless mode".
- `create_capture_data.py`: only LiveLinkFace and HMC archives via `MetaHumanCaptureSourceSync`; not mono video. Use the CaptureManager ingest library instead.
- Not read: the docs page "Python scripting for MetaHuman Animator" (found by search only).

## 4. Commandlet or full editor
No statement either way in Epic's pages or the plugin's source (no match for "commandlet" in the plugin). Hints:
- Neural nets run through NNE with runtime order `NNERuntimeORTDml` (GPU), `NNERuntimeORTCpu` (CPU): `MetaHumanBodyTracker\Private\Nodes\OfflineBodyTrackerNode.cpp:98,216,324`, `OfflineCameraCalibrationNode.cpp:39`. One stage is forced to CPU: `OfflineBodyTrackerNode.cpp:321`.
- `BodyTracker\Private\NNEUtils.cpp:290-333` uses render-graph builders and `FRHICommandListImmediate`. A render context therefore looks needed for the GPU path.
- Epic's scripts call a blocking process on the main thread (`process_performance.py:49-51`). Blocking behaviour across five stages is unverified (`StartPipelineStage`, `MetaHumanPerformance.h:690`, has no shipped body).
- Unverified, from general engine knowledge: `-run=pythonscript` normally starts without a rendering device. Project memory says editor subsystems may be None there. Safer first test is `UnrealEditor.exe <project> -ExecutePythonScript=<full path> -unattended -nosplash` on a normal GPU editor launch (an editor without clicks), not the commandlet.

## 5. Forum thread (pages 1 to 3)
https://forums.unrealengine.com/t/epic-games-metahuman-animator-markerless-motion-capture-plugin/2729293 , pages 1, 2, 3, read 2026-11-09 (summarised by the fetch tool). Posts to 7 Oct 2026.
- Frame rate 0: p1 Doraemon231 (19 Jun), check Capture Data metadata FrameRate, may be 0, set the right value. p2 Arata_5656 (27 Jun): Live Link Hub exports every capture at 1 FPS. p2 TactileVisions (27 Jun, confirmed by Arata_5656): set the same frame rate in the footage capture data asset and in the image media source asset, then select it in the Performance. p2 Mobin0913191: changing only the capture data file did not help. p3 shivagoud1356 (22 Jul): "Capture data frame rate is zero", Img Media Source frame rate 0 and 2x2 resolution; no fix given. Epic page: FFmpeg transcoder lowers invalid-FPS risk (source above).
- D3D device removed: p2 AJMarrento (RX 6700 XT) and others on RX 6000. Fix by ZenPigeonGames and AJMarrento (25 Jun): AMD driver 24.6.1 with clean install, block Windows Update from replacing it, set `r.RayTracing` to False in DefaultEngine.ini. Ciprian_Stanciu: close all other Unreal editors; also saw VRAM rise about 3 GB on a 10-second clip. p3 Hasan_Kuchkarov (31 Aug), RTX 5070, UE 5.8.2: DXGI_ERROR_DEVICE_REMOVED at stage 4, same job reportedly works on an RTX 5090 with 5.8.0; no fix.
- Long footage: p2 TactileVisions: GPU crash at stage 4/5 on long footage; workaround is to analyse smaller parts. p3 Ciprian_Stanciu (1 Aug): a 20,000-frame clip reached about 340 GB committed memory; chunks of about 3,000 frames work.
- Jumps between chunks: Ciprian_Stanciu raised `InnerWindow` from 192 to about the clip's frame count. Confirmed in the installed source: `BodyTracker\Public\OfflineBodyTracker.h:152` (`static constexpr int InnerWindow = 192`). A C++ change to a plugin in the engine folder, so not a script fix; not recommended here, listed only as the user fix.
- Smoothing: Ciprian_Stanciu: only face gets smoothing; he added a rolling-average animation modifier after export (his own tool, not shown).
- Other: Smart App Control blocks the unsigned plugin DLLs (p1 wpxm8767, p3 Zarsky); Http-403 / MD-0011-0 install errors fixed by launcher update or clearing the launcher web cache (p2 tcsyoussef). Not relevant to the PC if the plugin already loads.
- Not in the thread: Python, command line, commandlet.

## 6. Script plan for `C:/LedgerTools/ai-video/out/m2-try1.webm` (exists, checked)
1. Convert webm to mp4 (the ingest call accepts .mp4/.mov per its header comment, line 143). No ffmpeg.exe found under F:\LedgerTools (glob, 2026-11-09); locate one first. Keep 24 fps constant.
2. Editor launch with Python plugin, MetaHuman Animator, Capture Manager Editor and the body plugin enabled, in a scratch project.
3. `cm = unreal.CaptureManagerIngestBlueprintLibrary`; `params = unreal.CaptureManagerConversionParams()`; `cd, err = cm.ingest_mono_video_sync(mp4, "", "m2try1", 1, params)`. Check `cd` is not None and `cd.get_editor_property("metadata").frame_rate` is 24 (not 0 or 1; section 5 fix: set it by hand and match the image media source).
4. Create the Performance as in `process_monocular_performance.py:16-27`, then `set_body_tracking(True)`, `set_editor_property("face_tracking", False)`, optional `set_editor_property("body_height", ...)` and `auto_body_height`.
5. `set_blocking_processing(True)`; `start_pipeline()`; log the returned error; poll `get_number_of_processed_frames()` and `contains_animation_data_type(...)` (enum name for body unverified).
6. Export: `s = unreal.MetaHumanPerformanceExportUtils.get_export_animation_sequence_settings(perf)`; set `show_export_dialog=False`, `export_body=True`, `export_face=False`, `export_skeleton=EXISTING_SKELETON` or performer skeleton, `target_skeleton_or_skeletal_mesh` (an assembled MetaHuman mesh), `package_path`, `asset_name`; `unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(perf, s)`.

Unverified: whether the Python names above exist (they follow the engine's snake-case rule and the shipped scripts); whether `body_tracking` via a setter works in a headless launch; whether step 5 finishes all five stages when blocking; whether `GetExportAnimationSequenceSettings` fills the transient skeletal-mesh fields (item A, the likeliest stop); whether it runs under a commandlet; DirectML on this PC's GPU (RX 6000 faults above apply only if the card is AMD; card not checked here).

## Not reached or limited
- Fetch results are model summaries. Ingest page and Blueprint page were read to character 100,000 of about 265,000 and 513,000; the rest is unread.
- Forum pages 1 to 3 were summarised, not read post by post; no page 4 link seen.
- Pages not read: "Python scripting for MetaHuman Animator", "Python scripting for Capture Manager", Hardware Requirements, Capture Device Requirements.
- Fab listing not fetched. No `.cpp` for UMetaHumanPerformance or the export utils ships, so export behaviour is unread.
