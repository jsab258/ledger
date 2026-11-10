# The body solve on the processor (n09-8), 10 November 2026

Read and run 08:21 to 08:30 Swiss time. Sources: the installed UE 5.8 engine and plugin source on this PC (paths below), the crashed run's log.

## Why the 9 Nov run crashed
- `C:/LedgerTools/ai-video/out/solve-m2s1101d.editor.log`: 0.35 s after "Run start", ONNX Runtime's DirectML provider fails on its first command list (887A0020, driver internal error, DmlCommandRecorder.cpp line 371), then every call returns 887A0005 (device removed). The editor carried on for 36 minutes and ended on the D3D12 GPU crash.
- So the fault is at the first network call, before any frame count or picture size could matter: a shorter clip, the preview character off or a smaller picture cannot change it. Body only was already set (face off). These three of advisor 75's fixes were not run, as unable to matter.

## The processor path
- `E/Plugins/Marketplace/MetaHumanBodyTracker_5.8/Source/BodyTracker/Private/OfflineBodyTracker.cpp:610-630`: every network (keypoints, CHMR, Hue, Detectron2, SAM2) tries `NNERuntimeORTDml` on GPU first, `NNERuntimeORTCpu` second. No setting, console variable or flag chooses (grep of the plugin source: none).
- `.../BodyTracker/Private/NNEUtils.cpp:59-72`: the GPU try returns nothing when `UE::NNE::GetRuntime<INNERuntimeGPU>` finds no runtime of that name, and the CPU entry is then used.
- `E/Source/Runtime/NNE/Public/NNE.h:27-52`: `UE::NNE::UnregisterRuntime` is public.
- So: a scratch project outside the game, `C:/LedgerTools/mocap-solve` (source in `tools/ue/mocap-solve-project`), with one editor module (PostEngineInit) that unregisters `NNERuntimeORTDml` only when the editor is started with `-LedgerNNECpu`. Nothing on the PC changes; the game and mh-assemble are untouched. Built in 71 s.

## The run
- Command: `UnrealEditor.exe C:/LedgerTools/mocap-solve/MocapSolve.uproject -ExecutePythonScript=<repo>/tools/ue/mocap_solve.py -LedgerNNECpu -unattended -nosplash -nop4 -abslog=...` with MOCAP_VIDEO (the 81-frame clip m2-81f-s1101.mp4), MOCAP_NAME m2s1101e, MOCAP_QUIT 1.
- Log `C:/LedgerTools/ai-video/out/solve-m2s1101e.editor.log`: "NNECPUSWITCH GPU runtimes left: 0"; ingest, frame rate 24/1, Performance, diagnostics all ok; "Run start" 08:29:03 with no ONNX Runtime error after it.
- Result and time: see the section below, written when the run ends.

## Result (09:04)
- All stages ok (`C:/LedgerTools/ai-video/out/solve-m2s1101e.json`): pipeline 2,123 s (35.4 min) for 81 frames, about 26 s a frame on the processor (6 cores); no crash; export `/Game/MocapSolve/m2s1101e_Body` in the scratch project, 79 frames, 3.29 s, on Epic's `metahuman_base_skel`, 342 tracks. `get_number_of_processed_frames` read 0 (its meaning unread; the export holds the frames).
- It moves (`tools/ue/anim_motion_check.py`, `anim-check-m2s1101e.json`, 20 samples): head turns up to 19.6 degrees, pelvis 8.3 degrees and 1.1 cm, calf 7.4, thigh 5.1, arm 3.9. Whether it looks like the clip is not judged here: that is the experiment's verdict (a film beside the source, a fresh reviewer).
- Cost: about 35 minutes of processor a 3.4 s clip, so roughly 10 minutes of solve a second of motion; the card stays free (a solve may run beside other work, never beside a build or the night walk). Tokens: one session, no helpers, about US$3.
- No driver rollback or GPU-timeout change is needed for the experiment; neither goes to his page.
