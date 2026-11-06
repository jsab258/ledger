# inZOI key and Silent Hill 2 mappings: public sources, 6 November 2026

All pages read 2026-11-06 through a page-reading tool (summaries of fetched pages, not raw page text: unverified in that respect). Nothing downloaded or run. No key appears in this note.

## Questions

1. inZOI (installed folder name: inZOI.v0.10.1). Is an AES key for its pak/utoc containers publicly published, for which build, where, and does the page name the exact version? Write the key to F: only if a version is stated or plainly fits.
2. Silent Hill 2 (2024, Unreal 5.1). Is a .usmap for this build publicly offered (where, who, terms, size, build)? Or can a tool generate one locally from the running game (name, licence, source, without fetching or running)?

## Answers: question 1

- A key is published. Source: https://simblr.cc/inzoi/tutorial/5526-inzoi-tutorial-finding-meshes-that-are-not-available-in-modkit-and-edit-them.html (read 2026-11-06). The page is dated uploaded and updated 6 July 2025. It states no game version for the key. It says the key "can change upon updates" and points to a cs.rin.ru forum thread (Keys section) for the current one. The same page names a mappings file, "5.4.4-0+UE5-BlueClient.usmap" (engine 5.4.4, game project BlueClient), and tells FModel users to select UE 5.5; no version of the game is tied to either.
- A web search result snippet also repeated a key as "currently the key" (undated). Search snippet only: unverified.
- Installed build: folder name inZOI.v0.10.1. Files in the install name a date code "251126" (inside plugin data file names), which suggests a build later than the July 2025 page (inference, unverified). Containers not opened.
- Match of the published key to 0.10.1: no page read states a matching version; the page is about 16 months older than the install's data. The match is unverified and not plainly fitting.
- Result: no file written; F:\LedgerTools\aaa-study\keys\inzoi-key.txt was not created.
- Other places checked: https://github.com/FModel/Unreal-Game-Keys (read 2026-11-06): lists only one game (BattleCore Arena); inZOI is not in it.

## Answers: question 2

- Public .usmap for Silent Hill 2 (SHProto): none found.
  - https://github.com/TheNaeem/Unreal-Mappings-Archive (read 2026-11-06): about 79 game folders; the only Silent Hill entry is "Silent Hill f". No SHProto. The page states no licence. (Search listing gave last push 8 Jan 2026, unverified.) The same archive has no inZOI/BlueClient folder.
  - Not reached: the FModel Discord Game Compatibility forum (named by https://tcrf.net/Help:Contents/Finding_Content/Game_Engines/Unreal_Engine_5/Mappings as a place for uploaded mappings); it needs a Discord sign-in, so it is listed as unreached. Nexus Mods pages for Silent Hill 2 were not read; no mappings seen in their search snippets.
- Generating locally (not fetched, not run; each needs the game started with a DLL injected or loaded next to it):
  - UnrealMappingsDumper by TheNaeem, https://github.com/TheNaeem/UnrealMappingsDumper (read 2026-11-06). Licence stated MIT (licence text not seen on the page). Injected DLL; writes Mappings.usmap into the game's executing directory; aimed at UE5, should work on recent UE4. Last update date not shown. Whether it works on Silent Hill 2's 5.1 build: unverified.
  - UE4SS (RE-UE4SS), https://github.com/UE4SS-RE/RE-UE4SS (read 2026-11-06). Licence stated MIT. Loaded as a proxy DLL (default dwmapi.dll) placed in the game's Binaries\Win64 folder; has a dumper that generates .usmap (credits the tool above); targets UE 4.7 to 5.8; may need per-game signature updates. Works on this game: unverified (a search result mentioned a Silent Hill 2 mod guide setting UE4SS to major version 5, snippet only).
  - Also named by https://tcrf.net/Help:Contents/Finding_Content/Game_Engines/Unreal_Engine_5/Mappings (not read in full; search summary only): a fallback of another game's mappings on the same engine version, which the project already found fails for Mafia (FILES-2026-11-06.md).

## Not reached or unconfirmed

- https://forums.nexusmods.com/topic/13512503-inzoi-modding-guides-resources/page/2 : HTTP 403, unreached.
- The cs.rin.ru key thread the simblr page cites: not opened (forum, likely needs sign-in); URL not fetched. inZOI key per version: unverified.
- FModel Discord compatibility forum: unreached (sign-in).
- Raw page text was not seen; the tool returned summaries.

## Added by the session, 20:58: measured

The key on the first page above, though its page states no version, opens the install: the project's reader mounted 36 of 37 containers and listed 258,469 files (the one left is the unencrypted global container); the same reader with Mafia's key mounted 18 of 19 as a control. So the match is measured, not inferred. It is kept on F: only. A first quick header test said it did not open, but that test also failed on Mafia with a working key, so it was the test at fault. Silent Hill 2's mappings: left listed; the only way found runs the game with a tool injected, not done without his word.
