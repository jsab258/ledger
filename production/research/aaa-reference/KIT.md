# AAA study kit

12 October 2026. Cloud week 42, queue unit 6.1. Marks: **[R]** page itself read on 12 Oct 2026; **[S]** search summary only, page not reached, a lead and not evidence; **[I]** inference. Source keys are listed at the end.

## 0. Before any step

- **The doc "LEDGER AAA Reference Study" was not reached.** Nine Google Drive searches (title, full text, shared) returned nothing by that name. The kit therefore follows QUEUE.md 6.1: four studies, namely schedules, crime and witnesses, reputation, dialogue. If the doc names others, the same method applies.
- **His ruling (11 October, given 12 October): route B, both games.** He accepts the legal risk (RULINGS.md; frontier-ai-uses/3-LEGAL.md, at its top). Study only: nothing from either game enters LEDGER or git, only our own written findings and numbers. KCD2 goes through Warhorse's own modding tools wherever they cover the need; Mafia through FModel (section 3). Whether Steam's licence for the modding tools allows study beyond making mods was not reached.
- **Still stop at a key.** The ruling does not cover breaking encryption: if Mafia's archives ask for a key, stop and ask him (section 3, step 5).
- **Asked of him on 12 October:** may the session on the PC read the opened files itself? They would pass through Anthropic's servers, which section 1 rules out as written. The alternative is that only he reads them. Until he answers, section 1 stands.

## 1. What it is for, and the rule

The kit shows where to look in two finished games so that the four studies start at the right file instead of guessing. It teaches ideas to be rebuilt from LEDGER's own code and assets, never material to be copied.

**Nothing extracted goes into git.** It stays on the PC under `F:\LedgerTools\reference-other-games\` (named in retention.json, outside the repository), and no row, line, picture or file from either game is pasted into a note, a ruling, a prompt or a model. Reasons, from 3-LEGAL.md: game licences usually forbid it; Swiss, UK and EU law give no study exception for it; US courts have enforced such licences; anything that protects the game's files (Steam's wrapper, an anti-cheat) may not be broken; uploading another firm's material to a cloud model is itself a copy; and RULINGS.md (1 Oct) already keeps other games' screenshots out of the repository. Notes written afterwards say what the idea is, in the study's own words.

## 2. Kingdom Come: Deliverance II (KCD2)

**Route, step by step**
1. Own KCD2 on Steam with the key activated. The Steam app "Kingdom Come: Deliverance II Modding tools" then appears in the library [R K1: KM-A-55].
2. Install it on a Steam library on F: (nothing large on C:), near the drive's root (Windows paths stop at 255 characters). It needs the .NET 6 Desktop Runtime for Workspace Setup and .NET Framework 4.8 for Skald [R K1: KM-A-55].
3. Run `Tools\ModdingWorkspaceSetup\WorkspaceSetup.exe`; it links (needs administrator rights) or copies the game's paks into the tools' folders [R K1: KM-A-55].
4. Open `Tools\Skald`, press PAKs, point it at the root. It opens quests, dialogue and text from the paks [R K1: KM-A-18]. Skald is Warhorse's own quest and dialogue editor.
5. Anything else is by hand. A pak is a zip archive [R K1: KM-A-3 says a mod pak is "a zip file, renamed to .pak, with 0 compression"; K4 says the game's paks are ZIP-based]. Read files in place; if a copy is needed, it goes only to `F:\LedgerTools\reference-other-games\kcd2\`.
6. Not recommended: community extractors (K4 Omni Pak Searcher, licence not stated) and any DLL or executable from a third party, unrun by this research. The repository K2 also holds extracted game files and game DLLs. They were not opened and must not be used.

**Folder layout** (game root) [R K1: KM-A-55, KM-A-56, KM-A-92, KM-A-18; K2; K6]
- `Data\`: `Tables.pak` (database tables, 1,738 files at build 1.5), `Scripts.pak` (Lua, 26,415 files), plus others [R K2]. Inside the tables pak the path is `Libs\Tables\<group>\<table>.xml`, for instance `rpg\rpg_param.xml` [R K6, build 1.5.2].
- `Data\Levels\<level>\` (trosecko, kutnohorsko) holds `level.pak` and `recast.pak`.
- `Localization\`: `<language>_xml.pak` for text, `<language>.pak` for voices.
- `Mods\` (with `mod.manifest`, optional `mod_order.txt`); `kcd.log` in the root.
- The game loads only paks and loose `.cfg` files; the tools' development build also loads loose files [R K1: KM-A-55].

**Where each system is reported to live**

| System | Reported place | Source |
|---|---|---|
| Schedules | Tables `LEVEL/scheduler` and `ai/SchedulerAlias`; scheduler links inside each level's `level.pak` tables; quest "Effects" can change NPC schedules | R K1: KM-A-12, KM-A-92, KM-A-30 |
| NPC behaviour | `ai/` tables (brain, subbrain, situation, NPCState..., AIConceptSignalDatabase (new format, patchable since 1.2)); Lua bindings named XGenAIModule, Soul, Calendar | R K1: KM-A-12; K2 |
| Crime | Table `rpg/crime` (new format, patchable since 1.2); each crime in rpg/crime.xml (fine, jail, expiration, isSpreadable); its tuning in ai/script_params.xml; the logic mostly in AI behaviour trees [R K1: KM-A-27]; "crime volumes" in entity Lua such as `AnimDoor.lua` in `Data\Scripts`; punishment buffs such as `crime_punishment_pillory_medium` in `rpg/buff.xml` | R K1: KM-A-12, KM-A-15, KM-A-16, KM-A-27 |
| Witnesses | No reached source says where. Lead: isSpreadable and the crime_* memory values (KM-A-27) [I] | not reached |
| Reputation | `rpg/reputation_condition`, `reputation_change`, `faction_label`, `FactionTree` (new format, patchable since 1.2), plus `renown_flag`, `relationship_flag`, `social_class` | R K1: KM-A-12 |
| Dialogue | Lines are localized strings in `<language>_xml.pak`, rows of id, ignored cell, text; a community README names `text_ui_dialog.xml` as the dialogue table (stock layout not spelled out); the structure is a quest "concept graph" of XML from `data\Quests\Final\barbora.xml` down | R K1: KM-A-91, KM-A-30; R K5 |

Standing per town and per group is reported by kcd2.org [S3]; the project's own coverage-audit-kcd2 says the same.

## 3. Mafia: The Old Country (FModel)

Engine: Unreal Engine 5 [S7]. CUE4Parse lists the game as `GAME_MafiaTheOldCountry = GAME_UE5_4 + 12`, so it is read as a UE 5.4 base with its own changes [I]; the entry arrived in the commit "Farlight84 and Mafia fixes", 14 August 2025 (date from GitHub's commit search) [R F4].

1. **Download.** `FModel.zip` from the latest GitHub release, "FModel Aug 2026" (tag aug-2026, published 2 Aug) [R F2, F1]. Windows only; .NET 10 or later; up to 2 GB RAM; extract the zip before running; log in `Output\Logs` [R F1].
2. **Directory.** Directory > Selector. Pick the game if detected; else open "Add Undetected Game", give Name and Directory, press Add Game, then OK [R F3]. The directory is the game's archive folder; install guides put it at `Content\Paks` [S12].
3. **Version setting.** In the same window, "UE Versions". Wiki: "might be the most important setting of all"; archive or package errors usually mean it is wrong [R F1: Settings Explanation]. Choose the entry naming the game. Whether the drop-down shows it under that name was not read [I]. If it is missing, FModel is probably too old [I].
4. **Mapping file.** Needed when the game ships IoStore files (`.utoc`/`.ucas`) [R F9]; Mafia mods are reported as `.pak`, `.ucas`, `.utoc` [S9], so expect to need one [I]. A published file exists: folder "Mafia The Old Country", file `Mappings.usmap` (no date or UE version shown) [R F5]; the FModel Discord's game-compatibility forum is also named [S8]. Then Settings > "Local Mapping File (drag & drop)" [R F3] (a restart is advised [S8]). FModel's compatibility lists (F8) do not mention the game [R]. Dumpers (F6; UE4SS, Dumper-7 and JMap in F9) attach to the running game. Every mapping file, the published one included, is dumped from the running game, which 3-LEGAL.md leaves out; his route B covers using one.
5. **Key.** Whether Mafia's archives are encrypted: not established; no reached source says. If FModel asks for a key, stop: decrypting with any key, found or published, breaks protection, which 3-LEGAL.md forbids. FModel's key list (F7) had no row for the game and points to a cracking forum, which this kit does not follow.
6. **Read.** After OK the archives load. Packages > Search finds assets by name. Properties export as `.json` [R F2, F3]. Save to `F:\LedgerTools\reference-other-games\mafia\`. Lower-level tools: repak for `.pak` and retoc for `.utoc/.ucas` (UE 5.3+ well supported) [R F10, F11].

The game's internal folder names were not reached. An unreached interview is said to call it story-led [S7]; this is a lead only.

## 4. Checklists (one per study)

**A. Schedules**
- KCD2 first: `scheduler` and `SchedulerAlias` tables; one level's `level.pak` tables; then the `ai/` tables; then quest Effects (KM-A-30).
- Mafia first: Search "schedule", "routine", "spawn"; open the level maps' actor lists.
- Question: how is a day written, and what bends it after a crime? (KCD2's town reaction is in coverage-audit-kcd2.)

**B. Crime and witnesses**
- KCD2 first: KM-A-27 "Crime" (Warhorse's own article); `rpg/crime`; `AnimDoor.lua` crime volumes; buffs such as `crime_punishment_pillory_medium`; then `ai/` signals for who noticed what.
- Mafia first: Search "wanted", "police", "alert", "witness". Stop after one hour with a one-line "not there".
- Question: what is recorded, who holds it, when does it fade?

**C. Reputation**
- KCD2 first: `reputation_*`, `FactionTree`, `faction_label`, `renown_flag`; then `rpg_param.xml` (global thresholds) [I].
- Mafia first: Search "reputation", "respect", "standing".
- Question: per person, per group or per town, and what reads it? LEDGER has ruled out one global number (coverage-audit-kcd2).

**D. Dialogue**
- KCD2 first: `<language>_xml.pak` string table; `text_ui_dialog.xml`; the quest graph under `data\Quests\Final`; Skald's dialogue view.
- Mafia first: Search "subtitle", "dialog", "conversation"; string tables and `.locres` (general Unreal knowledge, no source reached [I]); voice audio only listed, never kept.
- Question: how a line is chosen and gated, not what it says. Written lines never leave the study folder.

## 5. Reading list

**5a. Reached (all read 12 Oct 2026)**
- K1, KM-A-55 The Modding Tools: the Steam tools app, folders, development build, web server, Sandbox.
- K1, KM-A-3 and KM-A-12: mod layout, table patching, the table list by category (NPC, crime, reputation, schedule, AI).
- K1, KM-A-27 Crime: crimes, fines, jail, the fields expiration and isSpreadable, which the page does not explain, and crime memory values such as crime_longTermMemoryTrespassExpiration (rpg/crime.xml, ai/script_params.xml), the logic mostly in AI behaviour trees.
- K1, KM-A-91: text and voice paks, string ids. KM-A-92: level data and schedulers. KM-A-30: the quest graph. KM-A-18: Skald. KM-A-15 and KM-A-16: Lua, rules, buffs. KM-A-87: Workshop rules. KM-A-56: installing mods.
- Warhorse's Lua binding docs: Tools\modding\docs\ in the modding tools (KM-A-55). K2's copy is not used.
- K5: layout of localization rows and the dialogue table. K3 (Warbox, MIT): tool for editing tables. K7: Lua and pak basics (KCD1 era).
- F1: FModel wiki, Settings Explanation. F8: FModel's compatibility list. F10, F11: repak and retoc. F5, F6, F7 and F9 are cited in section 3 only and are not reading. They hold mapping files dumped from games, a DLL to inject into a game, a published key with a link to a cracking forum, and guides to finding keys.

**5b. Talks and articles: leads only, not reached [S]**
- GDC 2025 Game AI Summit, Matej Marko, "Combining GOAP and MBTs to Create NPCs' Behaviors for KCD2": gdcvault.com/play/1035576.
- GDC 2026 (10 March), Petr Smrcek, "Supporting Thousands of NPCs in KCD & KCD2": schedule.gdconf.com session 915120.
- Perforce podcast "Everything Is Connected", Petr Nohejl on Warhorse's quest tool Scout: perforce.com/resources/podcasts/p4/in-development/everything-is-connected.
- Unreal Engine developer interview on Mafia: The Old Country [S7]. No Digital Dragons session was found for either game.

## 6. Not reached

- The doc "LEDGER AAA Reference Study" (Google Drive, 9 searches).
- 24 web hosts: warhorse.youtrack.cloud (official wiki, read via snapshot K1 instead); deepsilver.com; press.plaion.com and presse.plaion.com; cryengine.com; steamcommunity.com; forum.kingdomcomerpg.com; nexusmods.com and wiki.nexusmods.com; kcd2.org; modding.wiki; gdcvault.com; schedule.gdconf.com; youtube.com; unrealengine.com; en.wikipedia.org; web.archive.org; tcrf.net; unofficial-modding-guide.com; docs.ue4ss.com; fmodel.app; gildor.org; api.github.com (FModel releases, 403).
- Not found by any source: Mafia's internal folder names, whether its archives are encrypted, any Hangar 13 talk, any Digital Dragons talk, where KCD2 records witnesses.

## Sources

**[S] leads:** S3 https://kcd2.org/en/post/kcd2-reputation; S7 https://www.unrealengine.com/developer-interviews/mafia-the-old-country-making-the-old-feel-new-with-unreal-engine-5; S8 https://tcrf.net/Help:Contents/Finding_Content/Game_Engines/Unreal_Engine_5/Mappings; S9 https://vgtimes.com/games/mafia-the-old-country/files/; S12 https://www.sportskeeda.com/esports/how-use-mods-mafia-the-old-country.

**[R] read:** F1 https://github.com/4sval/FModel and /wiki; F2 https://github.com/4sval/FModel/releases; F3 https://github.com/4sval/FModel/tree/dev/FModel; F4 https://github.com/FabianFG/CUE4Parse/blob/master/CUE4Parse/UE4/Versions/EGame.cs and /commit/67752a8; F5 https://github.com/TheNaeem/Unreal-Mappings-Archive; F6 https://github.com/TheNaeem/UnrealMappingsDumper; F7 https://github.com/FModel/Unreal-Game-Keys; F8 https://github.com/FModel/Game-Compatibility; F9 https://github.com/Dmgvol/UE_Modding; F10 https://github.com/trumank/retoc; F11 https://github.com/trumank/repak; K1 https://github.com/muyuanjin/kcd2-mod-docs/tree/main/official-wiki (snapshot of https://warhorse.youtrack.cloud/articles/KM, exported 2026-06-23); K2 https://github.com/muyuanjin/kcd2-mod-docs; K3 https://github.com/vawser/Warbox; K4 https://github.com/Omniscye/Omni-Pak-Searcher; K5 https://github.com/Vyachean/kcd2-dual-subtitles; K6 https://github.com/pino1536/Kingdom-Come-Deliverance-II-Mods; K7 https://github.com/benjaminfoo/kcd_coding_guide.
