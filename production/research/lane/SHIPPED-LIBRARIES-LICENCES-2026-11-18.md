# Shipped libraries and their licences (18 November 2026)

In plain words:
1. XAudio2 (the sound library) may be given out with the game; Microsoft asks for no credit line, but players must accept terms that protect Microsoft, and the game must not be just a wrapper around it.
2. The debug layer (d3d12SDKLayers.dll) and its settings tool must come out of any copy given to anyone; a new small tool lists them.
3. DbgHelp (the crash helper) is the real problem: the copy Epic ships carries a pre-release Windows build number (25291), and Epic's own record points at a different SDK; until a Debugging Tools for Windows copy replaces it, or its terms are read, it should not go out.
4. NVIDIA's crash tool (Aftermath) may be given out as its .dll only; NVIDIA asks for no credit line, but its current terms list four open-source parts whose notices should travel with it, and the text for the exact version shipped is still not read.
5. Sheila's voice in play comes from a VCTK clip (p267), not Parler-TTS; but the old Parler clip and a line spoken from it are still copied into the friends' voice folder.

Asked by FINDINGS.md line 21 and production/research/engine-notices/NOTE.md (5 October). Read from the cloud on 18 November 2026; nothing from the owner's PC. Each claim carries its source and the page's own date. "Not read" means the source was not reached; nothing here is guessed from memory.

## 1. XAudio2 9 redistributable (xaudio2_9redist.dll)

- Microsoft's developer guide: "Developers can redistribute this version of XAudio 2.9 with their apps." It also says the DLL is not intended for Xbox or UWP apps. The page gives no licence terms. https://learn.microsoft.com/en-us/windows/win32/xaudio2/xaudio2-redistributable (footer "Last updated on 2021-06-16"; metadata updated 2025-04-29; read 18 Nov 2026)
- The NuGet package Microsoft.XAudio2.Redist, latest 1.2.13, updated 10 April 2025. https://www.nuget.org/packages/Microsoft.XAudio2.Redist (read 18 Nov 2026)
- Its licence, "MICROSOFT SOFTWARE LICENSE TERMS, MICROSOFT XAUDIO 2.9 REDISTRIBUTABLE", section 2, distributable code. https://www.nuget.org/packages/Microsoft.XAudio2.Redist/1.2.13/License (version 1.2.13; read 18 Nov 2026, through a summarising fetch, not a full verbatim copy). It asks, of anyone distributing it:
  - add significant primary functionality in the application;
  - require distributors and end users to agree to terms that protect it and Microsoft at least as much as the licence does;
  - indemnify Microsoft against claims about the application (not claims based solely on the unmodified distributable code);
  - not use Microsoft's trademarks to suggest endorsement; not put the code under a licence requiring source disclosure;
  - not remove, minimise, block or modify any notices of Microsoft or its suppliers in the software (section 4(c)).
  - No attribution or credit line is asked. The licence page lists no distributable files by name.
- For the game: allowed. Put the licence text beside the DLL (not required for attribution, but it keeps the package's rule of one licence per library and records the terms). The end-user terms condition means a copy given out needs player-facing terms at least as protective; the game has none yet (open, below).
- Which package version Epic took is not read (Epic's .tps for XAudio2 is on the PC).

## 2. DbgHelp (dbghelp.dll, file version 10.0.25291)

- Microsoft, DbgHelp versions: "The redistribution policies make it possible for people to include the Debugging Tools For Windows installer in their own packages and releases." and "Note: The DbgHelp.dll file that ships in Windows is not redistributable." No per-version table. https://learn.microsoft.com/en-us/windows/win32/debug/dbghelp-versions (dated 2025-07-14; read 18 Nov 2026)
- Microsoft, Calling the DbgHelp library: "the best strategy is to install a copy of the library from the Debugging Tools For Windows package in the application directory logically adjacent to the software that calls it." SymSrv.dll and SrcSrv.dll, if needed, must sit in the same folder. https://learn.microsoft.com/en-us/windows/win32/debug/calling-the-dbghelp-library (last updated 2025-09-10; read 18 Nov 2026)
- Microsoft, Download debugging tools: Debugging Tools for Windows comes with the Windows SDK and WDK; the page says nothing on redistribution and lists no version numbers. https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools (last updated 2025-11-07; read 18 Nov 2026)
- What 10.0.25291 most likely is: Windows build numbers and SDK numbers share one series. Build 25290 was a Windows 11 Insider Dev Channel build from the rs_prerelease branch, compiled 28 January 2023, released 1 February 2023 (https://www.betawiki.net/wiki/Windows_11_build_25290, read 18 Nov 2026; a community wiki, not Microsoft). So 25291 sits in the early-2023 pre-release branch. It is most likely from an Insider Preview SDK, WDK or debugger package of that month, not a released Windows SDK. UNVERIFIED: no page found names a package carrying 10.0.25291; the Windows SDK archive page (developer.microsoft.com/windows/downloads/sdk-archive, linked from Microsoft's debugger page) was not reached (the fetch timed out).
- What Epic records: a forum post of 22 October 2026 on Epic's forum (UE 5.8.0, Engine/Binaries/ThirdParty/DbgHelp/dbghelp.dll) says the adjacent dbghelp.tps declares "Windows 10 SDK_10.0.19041.0", LicenseFolder=None, a EULA link to Microsoft's EWDK licence terms, and redistribution audiences Licensees/Git/P4 only. No reply, no answer from Epic. https://forums.unrealengine.com/t/ue-5-8-bundled-dbghelp-10-0-25291-1000-versus-sdk-10-0-19041-tps-metadata-package-and-notices-clarification/2843927 (posted 22 Oct 2026; read 18 Nov 2026). This is a third party's reading of the .tps, not read here; the .tps itself is on his PC.
- Whether Epic ships the redistributable copy: not established. The version (25291) disagrees with the record (19041), and the record's licence link is the EWDK's, whose terms were not read. Preview-build terms commonly differ from release terms, but those terms were not read, so that is not a finding.
- For the game: do not give out this copy until one of these is done: (a) replace it with dbghelp.dll from a released Debugging Tools for Windows (current Windows SDK), which Microsoft's two pages back for the application folder, and keep its licence beside it; or (b) read the terms for the 25291 package once it is identified. Removing it outright is not advised without a test: the engine's crash reporting calls it, and Windows' own copy would then load from the system, which is allowed to be used but not shipped (behaviour not tested).

## 3. NVIDIA Nsight Aftermath (GFSDK_Aftermath_Lib.x64.dll)

- NVIDIA's licence page, docs version v2026.3, last updated 21 July 2026: https://docs.nvidia.com/nsight-aftermath/CopyrightAndLicenses/index.html (read 18 Nov 2026, through summarising fetches). It asks:
  - Supplement: "The following portions of the SDK are distributable under the Agreement: the .dll / .so files." Everything else, unless named, is for internal use only (1.2).
  - 1.2(i): "Your application must have material additional functionality, beyond the included portions of the SDK."; the distributable portions "shall only be accessed by your application".
  - 1.2: distribution terms must be consistent with the agreement, protect NVIDIA's IP and users' privacy and legal rights; known non-compliant use must be reported to NVIDIA.
  - No NVIDIA credit line is asked for the DLL. The notice "This software contains source code provided by NVIDIA Corporation." is required only for modified sample source code (the game ships none). No endorsement claims; no removal of NVIDIA's notices; no reverse engineering (2.1); no use that would put it under an open-source licence (2.5).
  - Third-party components: "The Nsight Aftermath SDK makes use of third-party libraries": JSON for Modern C++ (MIT, Niels Lohmann), FlatBuffers (Apache 2.0, Google), Microsoft DirectX Shader Compiler (University of Illinois/NCSA), xxHash (BSD-style, Yann Collet). The page does not say which of these are inside the DLL. Their licences ask for their notices with binary copies, so the safe course is to ship them with the DLL.
- Aftermath 2025.5's release notes page (metadata dated 26 February 2026) says nothing on licence or DLL version. https://developer.nvidia.com/nsight-aftermath/getting-started/release-note-v2025.5 (read 18 Nov 2026)
- Not read: the licence text for 2025.5 itself (what the engine ships, DLL 2.26). The v2026.3 text is the nearest read. The engine's own file for 2025.5 holds only a header (NOTE.md).
- For the game: replace the old NVAPI-era text (nvidia-aftermath-nvapi-LICENSE.txt) with the Aftermath SDK licence and its third-party notices, taken from the 2025.5 SDK package on the PC (NVIDIA's download page) or, failing that, the v2026.3 page above, marked as such.

## 4. DirectX 12 Agility SDK (D3D12Core.dll, d3d12SDKLayers.dll)

- Microsoft's getting-started guide: "To ship your game, you must include the D3D12Core.dll you used to build your game"; "Remember to also remove the debug layer (D3D12SDKLayers.dll) from your application's installer." https://devblogs.microsoft.com/directx/gettingstarted-dx12agility/ (20 April 2021; read 18 Nov 2026)
- Microsoft's D3D12 redistributable spec lists what each SDK publishes: D3D12Core.dll ("components needed on end user machines for applications shipping with redist"), D3D12SDKLayers.dll (debug layer), d3dconfig.exe and headers; the debug layer "should not be installed on end user machines"; import libs need not be redistributed. https://microsoft.github.io/DirectX-Specs/d3d/D3D12Redistributable.html (undated; servicing from 9 Feb 2021; read 18 Nov 2026)
- The licence on NuGet ("MICROSOFT SOFTWARE LICENSE TERMS, MICROSOFT DIRECTX", read for 1.616.1): distributable is the object code listed in "the distributables file list in the software"; the same three conditions as XAudio2 (significant functionality, protective end-user terms, indemnity); no credit line; notices not removed. https://www.nuget.org/packages/Microsoft.Direct3D.D3D12/1.616.1/License (read 18 Nov 2026). Version 1.618.5, the one the engine ships, is listed on NuGet dated 5 December 2025 (https://www.nuget.org/packages/Microsoft.Direct3D.D3D12/1.616.1, read 18 Nov 2026); its own licence page was not read.
- The distributables file list itself is inside the NuGet package and was not read (no page shows it). Whatever it says, Microsoft's guide and spec both say the debug layer does not go to players.
- For the game: drop d3d12SDKLayers.dll (and d3dconfig.exe if present) from any copy given out. The debug layer's only role in a release package is Epic's guard against a mismatched copy in PATH (NOTE.md); a release run does not load it.

## 5. Parler-TTS in shipped voices (the repository's records)

- game-design/voice-picks.json, "lena": speaker "parler-d", "a voice designed from a written description by Parler-TTS mini v1 (Apache-2.0)", his blind pick of 25 September.
- production/specs/in-game.json line 6: Sheila's voice is "p267, his yes of 30 September ... the old pick D, lena.parler-d, leaned American". production/specs/voice-engines.json: Sheila (lena) speaks through Pocket since 26 October.
- How the game picks her clip (tools/voice-live/voice-server.py clip_for): the first .wav by name, then .mp3. game-design/picked-clips holds lena.p267.wav and lena.parler-d.mp3, so lena.p267.wav (VCTK) is used. Pocket's override folder game-design/pocket-voices is not in the repository (it may exist on the PC; not read), so the records show no lena override.
- But tools/voice-live/make_portable.py copies the whole picked-clips folder, and production/casting/in-game-2026-09-25/voice, into the friends' portable voice folder. THIRD-PARTY.md line 93 says that casting folder's lines (sheila-dunn.wav) were spoken from "Sheila's designed D". So a Parler-derived clip and a line spoken from it travel in the portable copy, though the records show neither is what Sheila speaks from in play.
- THIRD-PARTY.md line 99 already carries a Parler-TTS row (Apache-2.0). Whether the portable build's player ever hears sheila-dunn.wav is not shown by the records.
- Answer: the records show no voice in play designed with Parler-TTS; two Parler-derived files are still shipped in the portable voice folder.

## Still open

- DbgHelp: which package 10.0.25291 comes from, and its terms; the .tps on the PC to be read first-hand.
- Aftermath 2025.5's own licence text (in the SDK package on the PC).
- The Agility SDK's distributables file list (in the 1.618.5 NuGet package; the engine's copy is on the PC).
- XAudio2 package version Epic took (its .tps on the PC).
- Player-facing terms: Microsoft's (XAudio2, DirectX, DirectML) and NVIDIA's terms each require that people given the game agree to terms at least as protective. The game has none. A licence and scope question for him before any copy leaves his PC.
- Not reached: the Windows SDK archive page (timed out).

## For the main session

1. Licence folder (production/licences/engine): add xaudio2-redist-LICENSE.txt (the 1.2.13 NuGet licence, or the one matching Epic's version); replace nvidia-aftermath-nvapi-LICENSE.txt with nvidia-aftermath-LICENSE.txt holding the Aftermath SDK licence and its four third-party notices; add a dbghelp line in README.md saying it is blocked from given-out copies until replaced by a Debugging Tools for Windows copy.
2. tools/attribution-check.py: move xaudio2_9redist.dll from LIBRARY_OPEN to LIBRARY_NOTICES once its file is in; rename the Aftermath file there; keep dbghelp.dll open with the new reason (pre-release 25291 build, .tps says 19041 and EWDK terms); make d3d12sdklayers.dll (and d3dconfig.exe) a failure for any package meant to be given out, not an open note.
3. The step to drop the debug layer: before a copy leaves his PC, delete Engine/Binaries/Win64/D3D12/D3D12SDKLayers.dll (wherever the manifest puts it) and d3dconfig.exe from the copy, never from the build machine's package, then run python tools/lane/release_libs.py on the copy's manifest; it must print no DROP line. Better still, do it in the staging step (tools/ue/stage_game_data.py or the packaging script) for a "give-out" package only.
4. Voices: drop lena.parler-d.mp3 and the 25 September casting folder from make_portable.py's copy, or keep THIRD-PARTY.md's Parler row as their credit.
5. Needs you (licence and scope): player terms for any copy given out; recommendation: a short end-user licence written before the first copy leaves his PC.

The tool: tools/lane/release_libs.py (tests tools/lane/test_release_libs.py, 8 passed on 18 Nov 2026). It reads a manifest or file list and reports files to drop, libraries with their licence file and read status, and unknown DLLs; exit code 1 until all is clean.
