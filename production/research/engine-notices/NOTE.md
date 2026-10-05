# What a game shipping the engine's bundled libraries owes their makers (5 October 2026)

Asked by phase 0's exit review (point 12): the Shipping package's NOTICES.txt carries only FreeType's line, while the package ships nine third-party libraries beside the engine. Read from this PC; nothing here rests on memory or a summary.

## Method

1. The package's own manifests (ue-probe/Packaged/Windows/Manifest_*_Win64.txt) list every shipped file; each DLL's file version and maker read from its version resource.
2. How the engine stages notices: Engine/Source/Programs/AutomationTool/Scripts/CopyBuildToStagingDirectory.Automation.cs, lines 1822 to 1833, copies Engine/Source/ThirdParty/Licenses/NOTICES.txt into the package root "for necessary third party library attribution". That file holds FreeType's line alone. It is Epic's choice of what to stage; it does not change what each library's own licence asks.
3. Each library's licence, from the engine's Engine/Source/ThirdParty/Licenses folder (992 files), matched by version; Epic's .tps records (e.g. Engine/Source/ThirdParty/Windows/AgilitySDK/1.618.5/AgilitySDK.tps) give the source and the licence link.

## What each licence asks of a binary copy

| Library | Licence | Asks of a binary copy |
|---|---|---|
| Ogg, Vorbis (Xiph.org) | BSD 3-clause | "Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials" |
| MsQuic 2.2 | MIT | the copyright and permission notice included in all copies or substantial portions |
| oneTBB 2022.3 (tbb12, tbbmalloc) | Apache 2.0 | a copy of the licence with the work, and any NOTICE file's attributions |
| ONNX Runtime 1.24 | as recorded by the engine, with ONNX under Apache 2.0 | the licence and its notices with the work |
| DirectML 1.15.4 | Microsoft Software Licence Terms | distribution as permitted by its section 1; its notices not removed |
| DirectX 12 Agility SDK 1.618.5 (D3D12Core, d3d12SDKLayers) | Microsoft Software Licence Terms | "the object code form of the software listed in the distributables file list"; that list is in the SDK's NuGet package, not on this PC |
| NVIDIA Aftermath 2.26 | NVIDIA SDK licence | its copyright notices kept; the engine's file for SDK 2025.5 holds only a header |
| XAudio2 9 redistributable, DbgHelp | Microsoft redistributables | no licence file in the engine; not read |

## Done

The licence texts copied into production/licences/engine (with a README matching each DLL), staged into every package by tools/ue/stage_game_data.py, named on the credits page, and checked by tools/attribution-check.py --package: a library shipped with neither its licence beside it nor an open entry fails the build.

## Open

- Whether d3d12SDKLayers.dll is on the Agility SDK's distributables list. Epic stages it on purpose (AgilitySDK.Build.cs, lines 64 to 75: a mismatched layer DLL in PATH crashes the engine). The list is read from the SDK's package next.
- The terms of the XAudio2 9 redistributable and of DbgHelp as shipped by the engine.
- NVIDIA's terms for Aftermath SDK 2025.5; until read, the older NVAPI and Aftermath text the engine keeps is shipped.
