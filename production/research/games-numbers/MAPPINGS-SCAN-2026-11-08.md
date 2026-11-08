# Mappings scan: inZOI and Silent Hill 2 (read 8 Nov 2026)

Order item n09-12, research half. Nothing downloaded or run. Rows to fill in the budget study (production/research/aaa-reference/studies/12-tech-budgets.md): triangles, bones, LODs, texture sizes for these two games; none of them filled yet except the hair and LOD figures below.

## 1. inZOI: mappings file
- A working .usmap exists but is not in a public archive. The Simblr tutorial by Lyralei (uploaded 6 Jul 2025) names the file "5.4.4-0+UE5-BlueClient.usmap", hosted by her as "INZOI Mapping Resource.zip", credited to a sharer on the FModel Discord. https://simblr.cc/inzoi/tutorial/5526-inzoi-tutorial-finding-meshes-that-are-not-available-in-modkit-and-edit-them.html (read 8 Nov 2026).
- Game version: not stated. The file name suggests Unreal 5.4.4. The tutorial says FModel needs the game added by hand (UE version GAME_UE5_5) and the file may need replacing after updates. A file from July 2025 is very probably not matched to the current (Nov 2026) game: unverified.
- Terms or licence: none stated. The AES key is also in that tutorial (not copied here; not needed to be copied by this note).
- The Unreal Mappings Archive (https://github.com/OutTheShade/Unreal-Mappings-Archive, read 8 Nov 2026) has no inZOI folder. It states no licence on the page.
- FModel Discord forum (where mappings are shared per TCRF): not reachable without a login, so unreached.

## 2. Silent Hill 2 (2024)
- No published .usmap found. The Mappings Archive has no Silent Hill 2 entry (only Silent Hill f, folder 1.1.3, a different game). Same link, read 8 Nov 2026.
- Searches found only Nexus mods needing UE4SS (e.g. https://www.nexusmods.com/silenthill2/mods/24, snippet only: its UE4SS from Feb 2025; page itself not read in full). Game folder given there: SILENT HILL 2/SHProto/Binaries/Win64. Unverified.
- Whether the game's paks are encrypted (AES key need): not found.

## 3. UE4SS and the dumper
- Repository: https://github.com/UE4SS-RE/RE-UE4SS (read 8 Nov 2026). README: "Targeting UE versions from 4.7 to 5.8"; not plug-and-play, game-specific signatures (AOBs) may need updating.
- Licence: MIT, copyright Narknon 2022. https://raw.githubusercontent.com/UE4SS-RE/RE-UE4SS/main/LICENSE (read 8 Nov 2026). Use, copy, modify, sell allowed with the notice kept; no warranty.
- Injection: a proxy DLL (default dwmapi.dll) copied into the game's Binaries/Win64 folder; the game loads it at start and UE4SS "will automatically be injected"; alternatively UE4SS.dll injected by a separate injector. https://docs.ue4ss.com/print.html (read 8 Nov 2026; only first 100,000 of 231,759 characters read). So it does run inside the game process, and the game must be running to dump.
- Dump: "Dumpers for File Parsing" generates .usmap; default key Ctrl+Numpad 6. Output goes beside the shipping exe (per TCRF via search snippet; TCRF page itself unusable, see below).
- Works on inZOI or SH2 per its own issues: not confirmed. Only indirect: a Nexus page for an "experimental UE4SS for inZOI" (https://nexusmods.com/inzoi/mods/243) was in a search result; the page returned 403, unreached. Krafton removed Denuvo from inZOI (https://simscommunity.info/2025/03/26/inzoi-denuvo-statement-krafton/, snippet only). Anti-cheat on either game: unverified.
- Alternative dumper: TheNaeem's Unreal Mappings Dumper, MIT, an injected DLL writing Mappings.usmap beside the shipping exe; its README warns of bans on anti-cheat games. https://github.com/TheNaeem/UnrealMappingsDumper (read 8 Nov 2026). Also injects.
- Running either means launching the game with a DLL loaded in it: a game-process change, not a read-only step.

## 4. Published character budgets
inZOI, official ModKit docs (mod-docs.playinzoi.com), read 8 Nov 2026:
- Hair, LOD0 about 40,000 triangles (hair plus scalp); LOD2 about 15,000; LOD4 about 170 (hair only, no scalp); LOD1 reuses LOD0, LOD3 reuses LOD2; varies by hairstyle. https://mod-docs.playinzoi.com/docs/modkit-docs/modkit/project/caz/hair/03-structure. (A search snippet said "170 for LOD0"; the page says LOD4. Page governs.)
- Head: inZOI LOD range 0 to 4 (MetaHuman's 0 to 7 trimmed). No triangle or bone count. https://mod-docs.playinzoi.com/docs/modkit-docs/modkit/how-to/caz/head/01overview
- External assets page: no numeric limits, only "smaller is better", Nanite recommended. https://mod-docs.playinzoi.com/docs/modkit-docs/modkit/how-to/getting-started/04usingexternalassets
- Texture 2K or smaller recommended, from a June 2025 AMA: search snippet only, page (https://playinzoi.com/news/8751) returned no body. Unverified.
- Body or whole-character triangles, bone counts: not found.
Silent Hill 2: no triangle, bone, LOD or texture figures found in the searches (reviews and interviews only). Not found, not fully searched (no Bloober talk or Digital Foundry page read).

## Could not reach or use
- FModel Discord (login). Nexus pages (403). TCRF mappings page: fetched, but its text carried instructions aimed at an AI (payment, shutdown); ignored, page not used as evidence, only as a search snippet pointer. docs.ue4ss.com last 131,759 characters unread. ModKit pages with the original URL 404; alternate URLs worked.
