# The engine's bundled libraries and their licences

Shipped inside every package beside the game's other staged files (tools/ue/stage_game_data.py), because each library's licence asks for its notice to travel with binary copies; Epic's own staging adds only Engine/Source/ThirdParty/Licenses/NOTICES.txt, which carries FreeType's line alone. Copied 5 October 2026 from the installed engine's Engine/Source/ThirdParty/Licenses, matched to the versions the Shipping package carries (read from each DLL's file version). The research: production/research/engine-notices/NOTE.md.

| Library in the package | Version shipped | Licence | File here |
|---|---|---|---|
| libogg_64.dll | (no version stamped; Xiph.org Ogg) | BSD 3-clause, Xiph.org Foundation | ogg-LICENSE.txt |
| libvorbis_64.dll, libvorbisfile_64.dll | (no version stamped; Xiph.org Vorbis) | BSD 3-clause, Xiph.org Foundation | vorbis-LICENSE.txt |
| msquic.dll | 2.2.0 | MIT, Microsoft | msquic-LICENSE.txt |
| tbb12.dll, tbbmalloc.dll | 2022.3.0 | Apache 2.0, Intel (oneTBB) | onetbb-LICENSE.txt |
| onnxruntime.dll | 1.24 | ONNX Runtime 1.24.1 as the engine records it, with its third-party notices (ONNX: Apache 2.0) | onnxruntime-LICENSE.txt |
| DirectML.dll | 1.15.4 | Microsoft Software Licence Terms, DirectML | directml-LICENSE.txt |
| D3D12Core.dll | 1.618.5 | Microsoft Software Licence Terms, DirectX 12 Agility SDK (distributable code) | d3d12-agility-sdk-LICENSE.txt |
| GFSDK_Aftermath_Lib.x64.dll | 2.26 | NVIDIA's SDK licence; the engine's file for SDK 2025.5 holds only a header, so the older NVAPI and Aftermath text it carries is shipped | nvidia-aftermath-nvapi-LICENSE.txt |

Open, researched before any claim (FINDINGS.md): whether d3d12SDKLayers.dll is on the Agility SDK's distributables list (the list is in the SDK's package, not on this PC); the terms for xaudio2_9redist.dll and dbghelp.dll, Microsoft redistributables with no licence file in the engine; NVIDIA's terms for Aftermath SDK 2025.5.
