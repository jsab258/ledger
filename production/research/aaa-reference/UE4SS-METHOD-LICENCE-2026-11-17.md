# UE4SS method and licence: first-pass reading (read 17 Nov 2026)

For item n16-11 (numbers from the games' files). Reading only; nothing installed, downloaded or run. Needs of the budget table, from studies/12-tech-budgets.md (read 17 Nov 2026): frame time, card memory, draw distance, people counts and update budgets, shadow-light budgets, measured in a street. Its open blind spots: measured frame times in a street, cell sizes and distances, shader counts.

Fetches went through a summarising reader, not raw text; wording below is as returned, so quotes are UNVERIFIED against the page itself unless stated.

## 1. UE4SS (RE-UE4SS)
- Licence: MIT, "Copyright (c) 2022 Narknon". Use, change, share and sell freely; copyright and permission notice must stay in copies; no warranty, no liability. https://raw.githubusercontent.com/UE4SS-RE/RE-UE4SS/main/LICENSE (read 17 Nov 2026). Not a lawyer's reading. The project allowlist (license-allowlist.md) was not checked by this helper.
- Latest release: v4.0.0, marked "Latest", dated "12 Nov" (year not shown by the reader; presumably 2026, UNVERIFIED). Notes add UE 5.4, 5.5, 5.6, 5.7, 5.8 and UE 4.7 to 4.10; v3.0.0 notes mention 5.2 and 5.3. https://github.com/UE4SS-RE/RE-UE4SS/releases (read 17 Nov 2026). Six assets listed; names not read.
- Stated range "UE 4.7 to 5.8", with the warning it is not plug-and-play and signature patterns may need updating per game. https://github.com/UE4SS-RE/RE-UE4SS and https://docs.ue4ss.com/ (read 17 Nov 2026).
- Distribution: source on GitHub (build with MSVC, CMake 3.22+, Rust 1.73+) and prebuilt binaries under Releases (a normal and a "zDEV" build); binaries go in the game's Binaries/Win64. Same pages.
- Whether a given game works with v4.0.0 is not known: UNVERIFIED for all four games.

## 2. Engines
- Kingdom Come: Deliverance II: CryEngine, not Unreal (a search summary and press only; no developer page read) - UNVERIFIED primary. Search result links: https://www.gamepro.de/artikel/kingdom-come-deliverance-2-nicht-auf-unreal-engine-5,3427554.html (not opened). Study 12 already treats it as CryEngine from its own files.
- Silent Hill 2 remake: Unreal Engine 5 (VGC headline, snippet only): https://videogameschronicle.com/news/silent-hill-2s-remake-runs-on-unreal-engine-5-and-has-a-rebuilt-combat-system. Minor version UNVERIFIED.
- Mafia: The Old Country: Unreal 5.4 per Study 12 (from its own files, 25 Oct); not re-confirmed from a public page today.
- inZOI: Unreal 5 assumed; version UNVERIFIED (search found nothing).
- CryEngine tool for frame/budget numbers: not confirmed. CryEngine's manual URL redirected to https://www.cryengine.com/docs/ which was not read; its profiling tools and licence are UNVERIFIED. Study 12 reached KCD2 numbers by reading its config files, not by a runtime tool. UE4SS does not apply to CryEngine.

## 3. What UE4SS can report
- Read: Lua API UObject page lists `ProcessConsoleExec(string Cmd, nil Reserved, UObject Executor)` ("Calls UObject::ProcessConsoleExec with the supplied params") and `CallFunction`. https://docs.ue4ss.com/lua-api/classes/uobject.html (read 17 Nov 2026).
- Docs home lists a Lua API, C++ mod API, live property viewer/editor, dumpers, a "Universal UE Mods" feature said to unlock the game console, and a Blueprint modloader. https://docs.ue4ss.com/ (read 17 Nov 2026). The reader said the page does not mention ExecuteConsoleCommand or key binds.
- NOT confirmed: that stat unit, stat gpu, stat rhi, memreport, r.ScreenPercentage, view-distance or LOD commands are listed or work through UE4SS in shipped builds. Pages tried returned 404 (docs.ue4ss.com console-command cheat sheet, available-mods, executeinegamethread). No official page found documenting stat commands. UNVERIFIED. Shipping builds often strip console and stat code; whether these four do is not known.
- The live property viewer could read object properties (e.g. scalability or view-distance values) rather than frame times; frame/GPU timings from it are UNVERIFIED.

## 4. EULA / terms (Steam EULA pages, read 17 Nov 2026, through the reader)
- Mafia: The Old Country: https://store.steampowered.com/eula/1941540_eula_0 - "Unauthorized copying, alteration, reverse engineering, decompiling" prohibited. The reader inferred the game from an FAQ link to mafia.2k.com/the-old-country; app id match UNVERIFIED.
- Kingdom Come: Deliverance II: https://store.steampowered.com/eula/1771300_eula_0 - may not "reverse engineer, derive source code from, modify, disassemble, decompile". App id assumed to be KCD2, UNVERIFIED; the reader did not name the game.
- Silent Hill 2 remake: EULA text not reached (the search surfaced another game's EULA, app 2379620, not used). UNREACHED.
- inZOI: Krafton has a separate mods policy ("Mods are permitted in inZOI" within limits, no direct monetisation, per a search summary only); page https://playinzoi.com/clause/mods_policy returned only a title. The reverse-engineering clause is UNREACHED. Note: that policy covers sanctioned mods, not game-file study.
- Result 4244160 in a search was an unrelated publisher's EULA; not used.

## 5. Anti-cheat and online checks
- No official statement read for any of the four. Mafia EULA reader: no explicit anti-cheat clause, but breach can restrict access to the game or online account. Denuvo: a search snippet says Silent Hill 2 remake has none; Krafton removed Denuvo from inZOI (news: https://game8.co/articles/latest/inzoi-dev-apologizes-for-including-denuvo-drm-removes-it-from-game, snippet only). Denuvo is DRM, not UE4SS-specific. Kernel anti-cheat in any of the four: UNVERIFIED.
- The UE4SS GitHub page showed no anti-cheat warning (reader).

## Unreached or unverified list
docs.ue4ss.com console cheat sheet, available-mods and executeinegamethread pages (404); UE4SS release asset names and year; KCD2, SH2 and inZOI developer engine statements; Mafia engine version public source; CryEngine docs and licence; SH2 EULA; inZOI mods policy and EULA body; any official anti-cheat statement; project licence allowlist check; whether UE4SS runs on any of the four games.
