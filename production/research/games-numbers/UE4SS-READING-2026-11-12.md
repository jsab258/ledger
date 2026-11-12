# UE4SS reading (read 12 Nov 2026)

Read only; nothing downloaded or run.

## 1. Licence and release
- Licence: MIT, (c) 2022 Narknon; commercial use allowed, notice kept. https://raw.githubusercontent.com/UE4SS-RE/RE-UE4SS/main/LICENSE (read 12 Nov 2026).
- Latest stable: v4.0.0, published 2026-11-12 01:50 UTC (the same day as this note: very new, little community testing; unverified in the field). https://api.github.com/repos/UE4SS-RE/RE-UE4SS/releases/latest (read 12 Nov 2026). Also an "experimental-latest" pre-release. https://github.com/UE4SS-RE/RE-UE4SS/releases (read 12 Nov 2026).
- Assets, with sizes and sha256 digests shown by GitHub's API: UE4SS_v4.0.0.zip 8,758,673 bytes (sha256 251ad0d1...c81e45); zCustomGameConfigs.zip 423,798 bytes; zDEV-UE4SS_v4.0.0.zip 39,134,774 bytes; zMapGenBP.zip 27,568 bytes. Only these four of "6" assets were listed; two unlisted.
- Zip contents: not read (not listed on any page reached). Release notes say the UE4SS files go in a `ue4ss` folder beside the game exe; only the proxy dwmapi.dll stays in Win64. https://github.com/UE4SS-RE/RE-UE4SS/releases/tag/v4.0.0 (read 12 Nov 2026).
- Signing: no signed binaries or separate checksum file. GitHub's own sha256 digests exist per asset; commit signatures only.

## 2. Engine support
- Release notes: UE 4.7 to 4.10, 5.4 to 5.8 (4.21 and earlier via an optional build). Notes mention 5.1+ and 5.3 only in breaking-change lines, so 5.1 support is unconfirmed. Same release page.
- Silent Hill 2 remake: Unreal Engine 5.1, per one PC review snippet (Neowin, via search, not read in full). https://www.neowin.net/amp/silent-hill-2-pc-reviewthe-definitive-way-to-re-visit-the-foggiest-town-ever-seen/ Unverified. Whether v4.0.0 handles 5.1 is unverified. The earlier scan found Nexus SH2 mods that use UE4SS (Feb 2025 build), which suggests older UE4SS worked: unverified.
- inZOI: .usmap name suggests 5.4.4 (earlier scan); the Simblr tutorial told FModel to use GAME_UE5_5, so the version is unclear. Search results show a community UE4SS package for inZOI (nexusmods.com/inzoi/mods/243, 403, unread). Unverified.
- Custom configs: community game configs live in the repository's assets/CustomGameConfigs folder (also the zCustomGameConfigs.zip release asset). The folder listing has neither inZOI nor Silent Hill 2 (only Silent Hill f and Townfall). https://github.com/UE4SS-RE/RE-UE4SS/tree/main/assets/CustomGameConfigs (read 12 Nov 2026; page said the list may be incomplete). Per-game AOB or layout needs: unknown.

## 3. Dumps
- Object dump: Ctrl+J, writes UE4SS_ObjectDump.txt; setting LoadAllAssetsBeforeDumpingObjects (default 0; warned to crash the game if play continues past the menu). https://docs.ue4ss.com/feature-overview/dumpers.html (read 12 Nov 2026).
- .usmap: Ctrl+Numpad 6 (or Dumpers tab in the GUI, or Lua DumpUSMAP); Blueprint types included by default. Output file name and folder are not on that page: unconfirmed (earlier scan: beside the exe, via snippet). v4.0.0 adds a .jmap dumper and an SDK header generator.
- Keys are editable in Mods/Keybinds/Scripts/main.lua.
- FModel reading meshes with the .usmap: not confirmed here (a docs "generating usmap" page was 404). The earlier scan has FModel working with an inZOI .usmap per the Simblr tutorial. FModel shows mesh details in its viewer; whether it lists exact triangle, bone and LOD counts: unverified.

## 4. Anti-cheat and launchers
- inZOI: Denuvo Anti-Tamper in the demo and early access; Krafton said it would be removed (March 2025). No anti-cheat found; current state unverified. https://simscommunity.info/2025/03/26/inzoi-denuvo-statement-krafton/ and https://www.pcgamesn.com/inzoi/denuvo-removed (search results only, not read in full). inZOI officially points to mods in its ModKit, but Krafton does not guarantee mod stability.
- Silent Hill 2: Steam page names no anti-cheat, Denuvo or launcher. https://store.steampowered.com/app/2124490/SILENT_HILL_2/ (read 12 Nov 2026; the page text may omit DRM notes). Unverified beyond that.

## 5. Footprint (for clean removal)
- Per release notes and docs: dwmapi.dll in Binaries/Win64 plus a `ue4ss` folder (older layout: files beside the exe, plus a Mods folder). The dump files land in that folder or beside the exe. A full file list (e.g. UE4SS-settings.ini, log) was not read: unverified. Remove by deleting those items; record a before-and-after file list of the Win64 folder.

## Not reached
- Nexus pages (403/not fetched), FModel Discord, the zip's contents, docs.ue4ss.com usmap guide (404), full UE4SS install page.
