# KCD2: Warhorse's official modding tools, and how to set them up for reading the data

25 October 2026. Research helper for the AAA study (STUDY-PLAN.md, KIT.md). Marks: **[R]** primary page read in full on 25 Oct 2026; **[M]** measured on this PC on 25 Oct 2026 (folder listings and the zip directories of the game's archives only; no file inside an archive was opened or copied); **[C]** community source; **[S]** search summary only, not evidence; **[I]** inference. Source keys (W1, E1...) are listed at the end.

**The finding that changes the plan.** The Modding Tools' own licence says: "This license is for your personal and non-commercial use as an individual only. Companies are not entitled to use the Modding Tools. You shall not use the Modding Tools for any purpose other than developing UGC for the Game." [R E1]. So the official tools do not cover a studio studying the data for its own game. KIT.md had listed this as not reached; it is reached now. The public documentation wiki (W1) can be read with no account and no install, and it answers most of question 5.

## Q1. What Warhorse has released

| Item | Publisher | Where | Released / version | Size | Terms | What it does |
|---|---|---|---|---|---|---|
| **Kingdom Come: Deliverance II Modding tools**, Steam app 2429020 | Warhorse; licensed by PLAION GmbH | Steam only. It is a Steam "Tool" whose parent is the game (1771300), and it has no store page: the app's store address redirects to the store front [R W1 KM-A-55; R/C T1; M] | Launched with patch 1.2 on 13 Mar 2025 [R N1, N2, P1]. Public build 22816715, updated 20 Apr 2026, the day of patch 1.5.5 [C T1]. The game itself is at 1.5.6 (25 Jun 2026) [R N3] | Installed depot 16,570,292,908 bytes (about 16.6 GB), download 8,850,914,320 bytes (about 8.9 GB) [C T1]. Not stated by Warhorse | Modding Tools EULA (E1) | Separate install with the same folders as the game. It includes a development build of the game (debug commands, loads loose files, a local web server on localhost:1403 with debug pages and an API browser), **Editor.exe** (Warhorse's CryEngine Sandbox), the two main levels' source files (Data/Levels), Developer.pak (source files the game does not ship), Lua binding docs (Tools/modding/docs), a database structure DLL (Tools/GeneratedDatabase), ResourceCompiler (which also makes paks), RemoteConsole, TraceServer, plug-ins for 3ds Max and Maya, and the four tools below [R W1 KM-A-55]. Steam's launch menu offers Workspace setup, Editor, Game and Workshop uploader [C T1] |
| **WorkspaceSetup.exe** (Tools/ModdingWorkspaceSetup) | Warhorse, inside the tools | Modding Tools | Not stated | Not stated | E1 | Links (needs administrator rights) or copies every pak from the installed game into the tools. A manual copy of the Data/, Localization/ and Levels/*/ paks also works [R W1 KM-A-55] |
| **Excel add-in** (Tools/modding/excelAddin, installed from ExcelDbAddin.DbAndXsdSupport.vsto) | Warhorse, inside the tools | Modding Tools; needs Microsoft Excel | Not stated | Not stated | E1 | Opens most game tables, and per-type "views" such as weapons or armour within the item table, reading **either extracted XML or the paks directly**. Saves changes as table patches in a mod, and can save text into the localisation paks [R W1 KM-A-86] |
| **Skald** (Tools/Skald) | Warhorse, inside the tools | Modding Tools; .NET Framework 4.8 | Not stated | Not stated | E1 | Quest, dialogue and localisation editor; "PAKs" opens a project straight from the game's paks [R W1 KM-A-18] |
| **Smid** (Tools/Smid) | Warhorse, inside the tools | Modding Tools; .NET Framework 4.8 | Not stated | Not stated | E1 | Editor for NPC clothing, body parts, materials, armour, weapons and presets; "Load from PAKs" [R W1 KM-A-14, KM-A-55] |
| **SteamWorkshopUploader** | Warhorse, inside the tools | Modding Tools; .NET 6 Desktop Runtime | Not stated | Not stated | E1 + Steam's Workshop agreement | The only way to upload a mod to the Workshop. It needs an activated KCD2 key; copies borrowed through sharing or a free weekend "might not work" [R W1 KM-A-85] |
| **KCD2 Modding wiki**, project "KCD2 Modding (KM)" at warhorse.youtrack.cloud | Warhorse; linked from the publisher's modding page | Public web, no account needed. 78 articles, first written 12 Nov 2024, last updated 14 Sep 2026 [R W1, read through YouTrack's public API because the pages need JavaScript] | Living document | n/a | None stated on the wiki | The official documentation: mod layout, the **full list of 300+ database tables with their kind** (KM-A-12), about 1,000 RPG constants exported 14 Jan 2025 (KM-A-20), stats (KM-A-21), crime (KM-A-27), quest graph (KM-A-30), scheduler link grammar (KM-A-93), level data (KM-A-92), STORM (KM-A-32 to 34), inventory presets (KM-A-90), items (KM-A-17, KM-A-89), localisation (KM-A-91), Lua (KM-A-15) |
| **"Modding in Kingdom Come: Deliverance 2"** | Deep Silver / PLAION (publisher) | deepsilver.com | Last updated 14 Mar 2025 | n/a | Its own UGC rules; the EULA prevails | Installing mods, load order, the tools, packing paks, rules for user content [R D1] |
| **Steam Workshop** for the game | Steam / Warhorse | Steam | Since patch 1.2, 13 Mar 2025 | n/a | Workshop guidelines (W1 KM-A-87) + Steam's agreements | Distributing and installing mods [R N2, W1 KM-A-56] |

Not found, each looked for:
- **Data or table schemas as a separate release.** None. The schemas ship inside the game: Tables.pak holds 13 .xsd files, among them `database.xsd` and `schema0.xsd`, not one per table [M], and the tools add a structure DLL [R W1 KM-A-55].
- **A localisation tool on its own.** None. Skald and the Excel add-in handle text [R W1 KM-A-18, KM-A-86, KM-A-91].
- **An official GitHub.** None. Warhorse's website links to no GitHub [R H1]. A GitHub user named "WarhorseStudios" has no name, no company and no repositories, so it is not established as Warhorse's [R G1]. The organisation "warhorse" is an unrelated security-tooling group [R G2].
- **The tools on GOG or Epic.** None. GOG sells the game but lists no modding tools [R G3], and Warhorse says the tools come only through Steam [R W1 KM-A-55]. Epic was not checked.
- **Warhorse's own forum.** Its Modding category is from the first game; the newest topic is from 2021 [R F1].

## Q2. Does any of them read the paks, or is unpacking with zip tools the documented way?

- **The official tools read the paks directly.** WorkspaceSetup links or copies them; the Excel add-in reads "either extracted XML files, or PAKs"; Skald opens projects from the paks; Smid has "Load from PAKs" [R W1 KM-A-55, KM-A-86, KM-A-18, KM-A-14]. **None of them is an unpacker.** ResourceCompiler makes paks [R W1 KM-A-55].
- **What Warhorse documents about zip tools is packing, not unpacking.** A pak is "a zip file, renamed to .pak, with 0 compression" [R W1 KM-A-3]. Total Commander and Windows 10's Explorer make paks the game will load; "ZIP archives created by 7zip don't work" [R W1 KM-A-58; D1]. No Warhorse page gives steps for unpacking the game's own paks. Two pages treat unpacked data as normal: Smid's "unless you have unpacked PAK files", and the Excel add-in's "extracted XML files" [R W1 KM-A-14, KM-A-86].
- **Measured on this install (version 1.2):** the game's paks are ordinary zip archives, mostly Deflate-compressed with a few stored files, and none is encrypted. Python's standard zip reader lists them. Tables.pak has 1,620 entries, Scripts.pak 23,277 and IPL_GameData.pak 10,454 [M]. So any zip reader can read them (7-Zip included). The 7-Zip warning is only about making paks for mods [I from M + W1].

## Q3. What the terms say about modding and extracting data

Read as written; this is not legal advice. Jafar lives in Switzerland, and the game EULA hands residents of Switzerland to the law of their own country (E2 §18).

- **Modding Tools EULA** (PLAION; no date shown) [R E1]:
  - **Personal use only.** The licence is "for your personal and non-commercial use as an individual only. Companies are not entitled to use the Modding Tools."
  - **Mods only.** The tools may be used for no "purpose other than developing UGC for the Game", and only "for the use in the Game only".
  - **No commercial use.** No reverse engineering, copying or derivative works of the tools; no commercialising "the results from the Modding Tools".
  - **The tools are CryEngine.** Crytek owns the engine and may enforce the licence.
  - **Term.** The licence runs from first download or use, PLAION may revoke it at any time, and it ends at once on any breach. The game's EULA also applies.
- **Game EULA on Steam** ("January 2025") [R E2]:
  - **Private use.** The game is "used solely for private purposes" (§1). Use is "personal, non-commercial" (§3). It is supplied "for domestic and private use" (§13c).
  - **What §5 forbids.** You may not "copy or reproduce, translate, reverse engineer ... disassemble, decompile display or distribute any part of the Game ... or create derivative works", or "alter or modify" it. You may not use "any unauthorized process or software that intercepts, collects, reads, or 'mines' information generated or stored by the Game". You may not obtain materials "through any means not intentionally made available".
  - **Distribution.** The game is to be "distributed and rented exclusively by authorized traders" (§1).
  - **Unreached copy.** It points to a copy at legal.kingdomcomerpg.com/eula, which returned 404 (unreached).
- **Deep Silver's general EULA** (July 2025, for PLAION games in general) [R E3]:
  - It has the same personal, non-commercial and no-reverse-engineering terms (§4, §8).
  - Its only modding carve-out is a revocable licence to use "certain modkits ... to create UGC" (§7).
- **The publisher's UGC rules** [R D1]:
  - Mods may not be sold or put behind a paywall.
  - Creators keep ownership, but PLAION gets broad rights to the mods.
  - Mods must be separate from official content.
  - The EULA prevails over these rules.
- **Workshop guidelines** [R W1 KM-A-87]: only your own original work, and compliance with Steam's rules.
- **In short:**
  - The terms allow modding by an individual, through the tools, for KCD2.
  - Nothing grants extracting data for study.
  - The tools' licence expressly excludes companies and every purpose other than making mods.
  - The game's licence forbids copying, reverse engineering and "mining" the game's stored data.
  - Jafar's ruling of 11 Oct (RULINGS.md) accepts the legal risk of opening the files. But "through Warhorse's official modding tools wherever they cover the need" now meets a licence that does not cover this need. That is his to decide (licences), not the session's.

## Q4. Steam only, and the owner's account

- **Steam only.** In Warhorse's words, the tools are "only available through Steam and need KCD2 key to use"; once a KCD2 key is activated, the tools are "automatically ... added to your Steam library" [R W1 KM-A-55]. **Installing them needs the owner's own Steam account, owning the game.** Claude must not sign in to it.
- **On this PC [M]:**
  - **Steam has neither app.** Steam is installed, but its only library (C:\Program Files (x86)\Steam) has no install record for the game (1771300) or the tools (2429020).
  - **The C:\Games copy is not a Steam install, and is old.** Its version is 1.2 (system.cfg), while Steam's game is at 1.5.6 [R N3].
  - **Its folder names download sites.** It holds `IGG-GAMES.COM.url`, `PCGAMESTORRENTS.COM.url`, `OneHack.Us.txt` and `_INSTALL TUTORIAL.txt`. Those are the names of third-party download sites, not of a store.
  - **The tools cannot be set up against this copy.** They need the activated key. Their development build follows Steam's current version, so linking 1.2 paks into 1.5.x tools would very likely mismatch [I].
  - **Third-party mods are installed.** Its Mods folder holds nine of them, deployed by the Vortex manager. They do not change the base paks, but they change what the game does in play, so any recording for the study should be made with them off.

## Q5. Where the systems live (Warhorse's wiki, checked against this 1.2 install)

Paths inside archives are as listed by the archive's directory [M]. The wiki writes them as `Data/libs/Tables/...`, which is the same place.

| System | Where | Source |
|---|---|---|
| **NPC schedules** | **Scheduler links** between entities in each level, exported to `Data/Levels/<level>/level.pak` → `tables/ai/scheduler.xml` (60 MB in kutnohorsko), beside `smartobjectanimations.xml` and `dogpoints.xml`. Aliases are in `Tables.pak` → `Libs/Tables/ai/SchedulerAlias.xml`. The **link grammar** (time window, variation, role in/out, sex, priority, sequence, attraction and repulsion, quest tag, buff tag, angriness, NPC count limits, social class, sun/rain, home, urgency, behaviour name) is in KM-A-93. Quests switch schedules on and off through "Schedule" concept nodes and Effects (KM-A-30). The behaviours themselves are likely the XML under `Scripts.pak` → `AI/npc`, `AI/profession`, `AI/situation`, `AI/world` [M folder names; I that these are behaviour trees]. The situation tables are `ai/situation*`. Level entities are in `level.pak` → `objects_mission0.xml`. To see the links in context, the Editor and the level sources from the tools are needed | R W1 KM-A-93, KM-A-92, KM-A-12, KM-A-30; M |
| **Crime and witnesses** | The crimes table, `Libs/Tables/rpg/crime.xml`, holds fine (in tenths of a groschen), jail, expiration, importance, isSpreadable, isViolent and scaling with social class. Tuning values are in `Libs/Tables/ai/ScriptParams.xml`, named `script_params.xml` on the wiki (e.g. `crime_longTermMemoryTrespassExpiration`). **The logic is in behaviour trees**, `Scripts.pak` → `AI/crime/` (308 files at 1.2), including files named for eye witnesses, arrest, home trespass, angriness and stash checks [M]; these names are leads to read. **How news of a crime spreads and fades** is in the RPG constants, which live in `rpg/rpg_param.xml` (defaults in code): `InformationExpirationBase` (multiplied by the crime's expiration), `InformationBroadcastPeriod` (spread through a faction subtree each day), the steal "perceptible volume" times, and the `PerceptionPriorCrime*` values. Doors and other entity Lua spawn the "crime volumes" NPCs react to (`Scripts/Entities/Doors/AnimDoor.lua`). Punishments are buffs in `rpg/buff.xml`. STORM gives souls crime contexts and roles (`hasSoulCrimeRole`, `addContext crime_...`). A game context such as `crime_disabledTrespassReactions` turns reactions off | R W1 KM-A-27, KM-A-20, KM-A-15, KM-A-16, KM-A-31, KM-A-33; M |
| **Reputation** | In `Libs/Tables/rpg/`: `reputation_change`, `reputation_condition` and `reputation_notification`, plus `FactionTree.xml` (new format since 1.2), `faction_label`, `renown_flag`, `relationship_flag`, `social_class` and the angriness tables. The constants cover NPC, faction and superfaction weights, propagation time, distance and cap, the icon thresholds, the local-hero threshold, and the decay of faction angriness. The STORM task "reputations" (`IPL_GameData.pak` → `Libs/Storm/reputations/`, with `setReputation`) sets starting reputation per world, quest and group | R W1 KM-A-12, KM-A-20, KM-A-32, KM-A-34; M |
| **Shops and items** | Shops are in `Libs/Tables/shop/shop.xml` (new format). Items are in `item/item.xml`; edit the base file, not the `item__*.xml` parts. **Stock** comes from inventory presets: `InventoryPreset.xml` and 170 `InventoryPreset__*.xml` parts [M], with the selection modes All, OneChild, AmountCount and AmountFraction; `clothing_preset` and `weapon_preset` are also involved. The barter, restock and repair constants are in the RPG list. Prices are stored in tenths of a groschen, and there are formulas for quality and wear (KM-A-89) | R W1 KM-A-90, KM-A-17, KM-A-89, KM-A-20, KM-A-12; M |
| **Quests** | The concept graph, a visual node language, starts at `Scripts.pak` → `Quests/Final/Barbora.xml` (the wiki says `data\Quests\Final\barbora.xml`), with the per-area graphs under `Quests/Final/Barbora/` (e.g. `kutnohorsko.xml`). It has Definition, State and Effect nodes, assets resolved to level entities, and objectives and markers. Dialogue lives in the graph; its text is in `Localization/<language>_xml.pak`. NPC souls are `Libs/Tables/rpg/soul__*.xml` (one part per quest or area, 290 files including the binary .tbl copies) [M]. Skald is the official viewer | R W1 KM-A-30, KM-A-18, KM-A-91; M |
| **NPC set-up as a whole** | STORM ("Soul-to-role manager") in `IPL_GameData.pak` → `Libs/Storm/storm.xml`. Rules made of selectors and operations, in the tasks abilities, characters, names, reputations and roles, assign stats, contexts, inventories, dialogue roles, appearance and names to every soul at load or spawn | R W1 KM-A-32 to 34; M |

## Sources (all read 25 Oct 2026 unless marked)

- **W1** Warhorse, KCD2 Modding wiki: https://warhorse.youtrack.cloud/articles/KM-A-1 (index). Read through the public API https://warhorse.youtrack.cloud/api/articles. All 78 article texts were fetched; the ones cited above were read in full. Images were not viewed.
- **D1** Deep Silver/PLAION, "Modding in Kingdom Come: Deliverance 2", last updated 14 Mar 2025: https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/modding-in-kingdom-come-deliverance-2
- **E1** Modding Tools EULA (PLAION): https://store.steampowered.com/eula/2429020_eula_0
- **E2** Game EULA, January 2025: https://store.steampowered.com/eula/1771300_eula_0
- **E3** Deep Silver general EULA, July 2025: https://www.deepsilver.com/about/eula
- **P1** PLAION press release, 13 Mar 2025: https://press.plaion.com/PATCHED-PRIMPED-READY-TO-MOD
- **N1 to N3** Warhorse's Steam announcements for app 1771300, read through Steam's news API (https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1771300): "Official Modding is Coming" (12 Feb 2025); "Official Modding now available ... on Steamworks!" and "Patch 1.2 is here" (13 Mar 2025); "Patch 1.5.6" (25 Jun 2026, the latest patch listed). The tools' own app 2429020 has no news.
- **T1 [C]** SteamCMD info mirror (community copy of Steam's app data): https://api.steamcmd.net/v1/info/2429020. Gives the type, parent, build, date, depot sizes and launch options. Steam's store API returns no store page for 2429020 [R].
- **H1** Warhorse Studios website: https://warhorsestudios.cz/ (no modding or GitHub link)
- **G1 to G3** https://api.github.com/users/WarhorseStudios; https://api.github.com/orgs/warhorse/repos; GOG catalogue https://catalog.gog.com/v1/catalog?query=like:kingdom%20come
- **F1** Warhorse forum, Modding category: https://forum.kingdomcomerpg.com/c/modding/12
- **[S]** Press and community pages seen only as search summaries (rpgsite, VGC, Shacknews, kcd2.org, Nexus "ModForge"); not used as evidence.

## Not reached, or not done

- https://legal.kingdomcomerpg.com/eula, the address the game EULA names for its current text: 404 (the root and other paths too).
- The tools' own files (Lua docs, Developer.pak, GeneratedDatabase, schemas), the Excel add-in's table coverage, and the debug pages on localhost:1403 were not seen, because the tools are not installed. Their size and build come only from the community mirror (T1).
- Epic Games Store, Warhorse's Discord servers and the full 1.2 patch notes were not checked.
- Images on the wiki were not viewed (e.g. the KM-A-55 Steam screenshot and the Excel add-in screenshots).
- Not established:
  - whether WorkspaceSetup can link paks from a non-Steam or older copy [I: very likely not];
  - whether the wiki's 1.2-era table names all hold at 1.5.6 (KIT.md counts 1,738 table files at 1.5 against 1,620 here at 1.2).
- Nothing was downloaded, installed or signed into, and the game was not run. This helper listed only the zip directories of Tables.pak, Scripts.pak, IPL_GameData.pak and kutnohorsko's level.pak. The builder indexed all 99 archives and unpacked eight archives' readable data the same day (REFERENCE.md).
