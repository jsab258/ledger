# UE4SS and the engines of four reference games

Research done 17 Nov 2026, read-only, nothing downloaded or run. Every claim below carries its link and "read 17 Nov 2026". Anything not confirmed from a page read in full is marked UNVERIFIED.

Important limit on this research: from this cloud session the GitHub API and the GitHub web pages for UE4SS-RE/RE-UE4SS were blocked (the session is not allowed that repository), and PCGamingWiki, SteamDB's API, the Steam store API, docs.ue4ss.com by direct fetch and jsDelivr were refused by the proxy. Raw files on raw.githubusercontent.com could be read, and so could some pages through the web reader. So release asset names and sizes, and the CustomGameConfigs folder listing, are unreached (see the list at the end). These should be checked from Jafar's PC before anyone relies on them.

## 1. UE4SS latest release

- Latest stable tag: v3.0.1, dated 2024-02-14 in UE4SS's own changelog (the header reads "v3.0.1 / 2024-02-14"). Source: https://raw.githubusercontent.com/UE4SS-RE/RE-UE4SS/main/assets/Changelog.md (read 17 Nov 2026). The GitHub releases page marks v3.0.1 as "Latest", dated "14 Feb" (year not shown in what the reader returned). Source: https://github.com/UE4SS-RE/RE-UE4SS/releases (read 17 Nov 2026).
- Previous: v3.0.0, 2024-02-04 (same changelog).
- Rolling pre-release: tag "experimental-latest", shown on the releases page as published "29 Dec" with 6 assets, marked Pre-release. The year was not shown; since today is Nov 2026 it cannot be 29 Dec 2026, so it is 29 Dec 2025 or earlier. Exact year UNVERIFIED. Source: https://github.com/UE4SS-RE/RE-UE4SS/releases/tag/experimental-latest (read 17 Nov 2026).
- The next versions, v4.0.0 and v4.1.0, are both marked "TBD" in the changelog, so they are not released yet (same changelog link, read 17 Nov 2026).
- Asset names and sizes: UNVERIFIED. The releases page reports only counts (6 assets for v3.0.1 and for experimental-latest). The API JSON (https://api.github.com/repos/UE4SS-RE/RE-UE4SS/releases) and the expanded-assets pages were blocked. Not guessed here.

Engine versions supported:
- UE 5.1: first added in v2.1.0 (2023-01-02, "Unreal Engine 5.1 Support (only tested on demo game)") and fixed in v2.1.1-HotFix (2023-01-03, "Fixed UE 5.1 compatibility"). So v3.0.1 covers 5.1. Source: the changelog above (read 17 Nov 2026).
- UE 5.2 and 5.3: added in v3.0.0 ("Added support for UE Version 5.2 and 5.3 games"). Source: releases page (read 17 Nov 2026).
- UE 5.4, 5.5, 5.6, 5.7, 5.8: listed only under v4.0.0, which is still TBD: "Added support for UE Version 5.4 - (UE4SS #503)", "Added support for UE Version 5.5 - (UE4SS #708)", "Added support for UE Version 5.6 - (UE4SS #977)", "Added support for UE Version 5.7", "Added support for UE Version 5.8". The same lines appear in the experimental-latest notes. Source: changelog lines 105 to 111, and the experimental-latest page (both read 17 Nov 2026).
- Plain meaning: the stable v3.0.1 does not officially support 5.4 or later. A 5.4 or 5.6 game needs the experimental build.
- Shipping builds: v4.0.0 adds "basic support for Development/Debug/Test built Unreal Engine games" (set DebugBuild to true). Shipping is the normal target. Same changelog (read 17 Nov 2026).
- .usmap dumping: the mappings dumper has been in UE4SS since v2.1.0 (keybind Ctrl+Numpad 6 from v2.2.0). README: "Generate .usmap mapping files for unversioned properties". Sources: changelog and https://raw.githubusercontent.com/UE4SS-RE/RE-UE4SS/main/README.md (read 17 Nov 2026).

## 2. Engine of each game

- Silent Hill 2 (2024): Unreal Engine 5.1.
  - CUE4Parse's game list puts it under 5.1: "GAME_SilentHill2Remake = GAME_UE5_1 + 4". Source: https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/CUE4Parse/UE4/Versions/EGame.cs (read 17 Nov 2026).
  - Backed up by a Nexus mod's install steps for UE4SS: "Set MajorVersion to 5", "Set MinorVersion to 1". Source: https://www.nexusmods.com/silenthill2/mods/315 (read 17 Nov 2026).
  - SteamDB lists the engine as "Unreal Engine", release 8 October 2024. Source: https://steamdb.info/app/2124490 (read 17 Nov 2026).
  - No developer statement of the minor version found. Developer-level confirmation UNVERIFIED.
- inZOI: Unreal Engine 5.6 now (it launched on 5.4).
  - Official Krafton news, 2026.03.04: "Following the official release of Unreal Engine 5.6, inZOI will be undergoing updates to its engine." Source: https://playinzoi.com/en/news/9774 (read 17 Nov 2026).
  - Fan news site, 29 Apr 2026: the patch "upgrades the game to the latest Unreal Engine 5.6", and the ModKit was updated for 5.6. Source: https://thesimstree.com/en/news-about-the-sims/tst-news/inzoi-receives-major-april-29-update-ue-5.6,-new-careers,-and-business-management.html (read 17 Nov 2026).
  - Player forum post (not official) describes the move as "from 5.4 to 5.6". Source: https://forum.playinzoi.com/t/topic/10434 (read 17 Nov 2026).
  - CUE4Parse: "GAME_InZOI = GAME_UE5_6 + 14" (EGame.cs link above, read 17 Nov 2026).
  - The 29 April date being the live change comes from a fan site, not Krafton. Treat it as likely, not certain.
- Mafia: The Old Country (2025): Unreal Engine 5.4.
  - CUE4Parse: "GAME_MafiaTheOldCountry = GAME_UE5_4 + 12" (EGame.cs link above, read 17 Nov 2026).
  - SteamDB lists the engine as "Unreal Engine", release 7 August 2025. Source: https://steamdb.info/app/1941540 (read 17 Nov 2026).
  - Epic's developer interview confirms UE5 but could not be read (site error): https://www.unrealengine.com/en-US/developer-interviews/mafia-the-old-country-making-the-old-feel-new-with-unreal-engine-5. The minor version from a developer is UNVERIFIED.
- Kingdom Come: Deliverance II: CryEngine (a heavily customised version).
  - PC Gamer, 3 Feb 2025: "one of the very few games to use Crytek's CryEngine". Source: https://www.pcgamer.com/hardware/kingdom-come-deliverance-2-performance-analysis-scalable-frame-rates-decent-graphics-and-barely-a-stutter-in-sight (read 17 Nov 2026).
  - Fan wiki: engine "CryEngine", "heavily customized version", release 4 February 2025. Source: https://kingdomcomedeliverance.wiki.gg/wiki/Kingdom_Come:_Deliverance_II (read 17 Nov 2026).
  - UE4SS, FModel and CUE4Parse do not apply to this game at all. It needs CryEngine tools, which this note does not cover.

## 3. Evidence that UE4SS works on each UE game

- CustomGameConfigs folder: could not be listed (GitHub blocked). Probing guessed folder names on raw.githubusercontent.com ("Silent Hill 2", "inZOI", "Mafia The Old Country" and variants) all returned 404, while "Kingdom Hearts 3" returned 200. That only shows those exact guessed names are absent. It does not prove the games are missing. UNVERIFIED. The changelog's list of configs added for v4.0.0 (Abiotic Factor, Psychonauts 2, Lies of P, Project Silverfish, Whiskerwood, StarRupture, The Talos Principle 2, Phantom Blade Zero) names none of the three. Source: changelog lines 162 to 176 (read 17 Nov 2026). The docs page names only Kingdom Hearts 3 as an example: https://docs.ue4ss.com/custom-game-configs.html (read 17 Nov 2026).
- Silent Hill 2: works.
  - Nexus mod 315 (ending tracker) says "This mod requires UE4SS" and recommends v3.0.1 "As of Feb 25, 2025". Source: https://www.nexusmods.com/silenthill2/mods/315 (read 17 Nov 2026; the date is the one stated on the page).
  - A Vortex extension for Silent Hill 2 (2024) installs UE4SS and supports UE4SS script and Blueprint mods (page shows no date). Source: https://nexusmods.com/site/mods/963 (read 17 Nov 2026).
  - Fits with UE 5.1, which stable v3.0.1 supports.
- inZOI: worked on the 5.4 build.
  - Nexus mod 243, "UE4SS packaged for inZOI": "This is the experimental version of UE4SS packaged for inZOI". Its file name carries the UE4SS build v3.0.1-389 and a Unix timestamp that works out to about 4 April 2025 (worked out from the file name, not stated on the page). Source: https://nexusmods.com/inzoi/mods/243 (read 17 Nov 2026).
  - A Vortex extension for inZOI auto-installs UE4SS (no date shown). Source: https://nexusmods.com/site/mods/1241 (read 17 Nov 2026).
  - After the move to 5.6 (spring 2026), whether UE4SS works is UNVERIFIED. It would need an experimental build with 5.6 support.
- Mafia: The Old Country: no evidence found. The mods found are pak mods in Paks/~mods (Sportskeeda, undated: https://sportskeeda.com/esports/how-use-mods-mafia-the-old-country) and Engine.ini tweaks (Gamepressure, 14 Apr 2026: https://www.gamepressure.com/download/mafia-the-old-country-ultimate-engine-tweaks-anti-stutters-more-/z01536a), both read 17 Nov 2026. Neither mentions UE4SS. UNVERIFIED. It also needs a UE4SS build with 5.4 support, and the game has Denuvo (see 5).
- GitHub issues on UE4SS mentioning these games: not searchable from here (blocked). UNVERIFIED.
- PCGamingWiki: unreachable.

## 4. Do stat unit, stat gpu and memreport exist in Shipping builds?

Mostly no.
- Epic's build configuration reference (UE 5.9 docs): Shipping "strips out console commands, stats, and profiling tools". Test is "the Shipping configuration, but with some console commands, stats, and profiling tools enabled." Source: https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configurations-reference-for-unreal-engine (read 17 Nov 2026).
- Engine source, Build.h, as quoted on Epic's forum on 23 Feb 2016 (an older engine, but the same rule):
  ```
  #elif UE_BUILD_SHIPPING
  	#if WITH_EDITOR
  		#define STATS 1
  	#else
  		#define STATS 0
  	#endif
  ```
  Source: https://forums.unrealengine.com/t/is-scope_cycle_counter-optimized-out-of-release-builds/56209 (read 17 Nov 2026). The current engine source is behind Epic's GitHub login and was not read, so the current Build.h is UNVERIFIED.
- Even in Test builds a forum reply (19 Jul 2016) says only "Stat FPS" and "Stat UNIT" should work. Source: https://forums.unrealengine.com/t/stats-not-enabled-in-test-build-docs-say-they-should-be/359234 (read 17 Nov 2026).
- A 2016 forum post shows Build.h with "#define ALLOW_CONSOLE 1" in the Shipping block, while console functions in PlayerController.cpp are cut by "!UE_BUILD_SHIPPING". Source: https://forums.unrealengine.com/t/allow-console-define-usage/380486 (read 17 Nov 2026). So re-enabling the console with a mod gives a prompt, but the stat counters are compiled out.
- memreport: no direct quote found for Shipping. UNVERIFIED, but it falls under "console commands ... stripped" above.
- Plain meaning: frame time and GPU memory from these Shipping games must come from outside tools (PresentMon, the GPU vendor's overlay, Windows Task Manager GPU memory, RenderDoc or PIX where anti-tamper allows), not from Unreal's own stats.

## 5. DRM and anti-cheat now

- Silent Hill 2: no third-party DRM found. SteamDB (record updated 27 Oct 2026) lists no Denuvo and no anti-cheat: https://steamdb.info/app/2124490 (read 17 Nov 2026). The Steam store page read showed only the age gate, with no DRM notice: https://store.steampowered.com/app/2124490/SILENT_HILL_2/?l=english (read 17 Nov 2026). Sportskeeda (undated) says "free of Denuvo as well as any other anti-piracy measure": https://www.sportskeeda.com/esports/does-silent-hill-2-remake-denuvo-protection (read 17 Nov 2026). The game uses the Epic Online Services SDK (SteamDB). PCGamingWiki not reached.
- inZOI: Denuvo removed before Early Access (26 Mar 2025). Director Hyungjun Kim said the Early Access build "will not include Denuvo". Source: https://www.videogameschronicle.com/news/inzoi-developer-is-removing-denuvo-drm-from-the-game-following-player-backlash (read 17 Nov 2026). Current store-page DRM: UNVERIFIED (Steam and PCGamingWiki not reached). Anti-cheat: none found, UNVERIFIED.
- Mafia: The Old Country: Denuvo. SteamDB: "3rd-Party DRM Denuvo Anti-tamper, 5 Activations per 24 hours machine activation limit". No anti-cheat listed. Record updated 13 Nov 2026. Source: https://steamdb.info/app/1941540 (read 17 Nov 2026).
- Kingdom Come: Deliverance II: no DRM. Warhorse's PR head said on 6 Nov 2024 that the game has neither Denuvo nor any other DRM. Source: https://www.gamespark.jp/article/2024/11/08/146789.html (article 8 Nov 2024, read 17 Nov 2026), repeated on https://kingdomcomedeliverance.wiki.gg/wiki/Kingdom_Come:_Deliverance_II (read 17 Nov 2026). The Steam page read showed only the age gate: https://store.steampowered.com/app/1771300 (read 17 Nov 2026). Whether that is still true today is UNVERIFIED, since PCGamingWiki could not be reached.

## 6. Offline route: FModel and CUE4Parse

- What they are: CUE4Parse is a C# library for reading UE4 and UE5 archives and packages, with support for "UTexture2D, UAnimSequence, UStaticMesh, and many more". FModel is the archive explorer built on it. Sources: https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/README.md and https://raw.githubusercontent.com/4sval/FModel/master/README.md (read 17 Nov 2026).
- All three UE games have their own entries in CUE4Parse's game list (SH2 5.1, Mafia 5.4, inZOI 5.6), which usually means someone has opened their packages with it. EGame.cs link in section 2 (read 17 Nov 2026).
- The numbers the team wants are fields CUE4Parse reads from the source files (read 17 Nov 2026):
  - Static mesh LOD count and per-LOD geometry: FStaticMeshRenderData has "public FStaticMeshLODResources[]? LODs", plus "ScreenSize" (the LOD switch distances) and "NaniteResources". Each LOD has "NumVertices", "Sections" and an "IndexBuffer". Triangles are the index count divided by three. Sources: https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/CUE4Parse/UE4/Assets/Exports/StaticMesh/FStaticMeshRenderData.cs and https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/CUE4Parse/UE4/Assets/Exports/StaticMesh/FStaticMeshLODResources.cs
  - Skeletal mesh bones and LODs: USkeletalMesh reads "ReferenceSkeleton" and "LODModels"; FReferenceSkeleton holds "FinalRefBoneInfo" (bone count is its length). Sources: https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/CUE4Parse/UE4/Assets/Exports/SkeletalMesh/USkeletalMesh.cs and https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/CUE4Parse/UE4/Assets/Exports/Animation/FReferenceSkeleton.cs
  - Texture size and format: FTexturePlatformData reads "SizeX", "SizeY", "Format" and the mips. Source: https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/CUE4Parse/UE4/Assets/Exports/Texture/FTexturePlatformData.cs
- Caveats:
  - For Nanite meshes the classic LODs are only the fallback mesh. The real triangle count sits in the Nanite data, and whether CUE4Parse exposes a simple total there is UNVERIFIED.
  - Encrypted paks need the game's AES key. Unversioned packages need the .usmap. That is why UE4SS would be run once. For Mafia (5.4, Denuvo) and inZOI (now 5.6) that run needs the experimental UE4SS build.
  - These tools show the asset budgets (triangles, bones, LODs, texture sizes). They cannot give frame time or GPU memory. Those come from running the game with outside tools.
- Licences, from the LICENSE files:
  - CUE4Parse: Apache License 2.0 ("Apache License, Version 2.0, January 2004"). Source: https://raw.githubusercontent.com/FabianFG/CUE4Parse/master/LICENSE (read 17 Nov 2026).
  - FModel: GNU General Public License version 3 ("Version 3, 29 June 2007"), the same on the master and dev branches. Sources: https://raw.githubusercontent.com/4sval/FModel/master/LICENSE and https://raw.githubusercontent.com/4sval/FModel/dev/LICENSE (read 17 Nov 2026).
  - Neither was checked against the project's licence allowlist in this note. Using them only as offline tools on the team's own PC, without shipping their code, is the usual case. The allowlist decides.
- Separate point, not legal advice: the games' licence terms on reverse engineering and asset extraction were not read. That is a scope and legal question for Jafar.

## Unreached (17 Nov 2026)

- https://api.github.com/repos/UE4SS-RE/RE-UE4SS/releases (blocked: repository not enabled for this session; web reader permission timed out)
- https://github.com/UE4SS-RE/RE-UE4SS/releases/expanded_assets/experimental-latest and .../v3.0.1 (asset names and sizes; blocked)
- https://github.com/UE4SS-RE/RE-UE4SS/tree/main/assets/CustomGameConfigs (folder listing; blocked)
- UE4SS GitHub issues search for the three games (blocked)
- docs.ue4ss.com by direct fetch (proxy 403; one page read through the web reader)
- PCGamingWiki pages for all four games (proxy 403, and not in search results)
- Steam store API appdetails for all four games (proxy 403)
- https://www.unrealengine.com/en-US/developer-interviews/mafia-the-old-country-making-the-old-feel-new-with-unreal-engine-5 (site error)
- https://www.nexusmods.com/silenthill2/mods/380 (site error)
- Current Unreal Engine source (Build.h) on Epic's private GitHub (needs an Epic-linked login)
- inZOI ModKit docs page did not state its engine version: https://mod-docs.playinzoi.com/docs/modkit-docs/modkit/how-to/getting-started/01install
