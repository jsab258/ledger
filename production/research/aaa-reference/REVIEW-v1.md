FAIL

# Review of KIT.md v1 (queue unit 6.1)

12 October 2026, by a fresh reviewer. Sources were read through raw.githubusercontent.com and git. GitHub's web pages, including FModel's release page, were blocked.

**Asked versus done.** It does what 6.1 asks: KCD2's paks, folder layout and the four systems; FModel's version setting, mapping file and keys; one checklist per study; a reading list; an honest list of what was not reached; and nothing from either game in git. The gap is that it misses the official Crime article (fault 4).

**Spot-checks (19 [R] facts).** These were **confirmed**: KM-A-55 (the tools app, .NET 6 and 4.8, linking or copying, 255-character paths, only paks and .cfg loaded); KM-A-3, word for word; the KM-A-12 table names; KM-A-15, 16, 18, 30, 91, 92 and 56; K2's counts and DLLs; K3 to K6; F4 (`GAME_UE5_4 + 12`, commit 67752a8, 14 Aug 2025); F1 (.NET 10, 2 GB, "might be the most important setting of all"); F2's tag aug-2026 of 2 Aug; F3's labels, the "0x" plus 64 and "Local Mapping File (drag & drop)"; F5; F7 (no Mafia row, points to cs.rin.ru); F8; F9; F10.
**Not confirmed:** the kit's reading of "since 1.2" in KM-A-12 (fault 3).
**Unreachable:** F2's release title and FModel.zip.

**Facts without a source, and search summaries.** No weight-bearing fact lacks a source. One [S] carries too much weight (fault 7).

**The legal conflict.** Section 0 is honest. It puts the conflict first, quotes 3-LEGAL.md fairly, stops all work until he rules, and recommends the narrowest route. But it rules out key-finders and dumpers while letting a key or mapping file made by someone else through (faults 1 and 2). The rule against git is sound, but the folder it names is wrong (fault 5).

**Unsafe to put in the repository.** There is no key in the kit. It does name a cracking forum as the place keys are published, and it links a mapping file taken from the game as something to use. K2 (extracted game files and game DLLs) carries a warning, but the reading list still sends readers into it.

## Faults, worst first

1. **WHAT:** It treats decrypting Mafia's archives with a "published key" as allowed. Decrypting with any key breaks protection, which 3-LEGAL.md forbids everywhere. It also points readers to a cracking forum. **WHERE:** section 3 step 5; section 6; section 0 option B. **FIX:** Replace step 5 from "Published keys:" to its end with: "If FModel asks for a key, stop: decrypting with any key, found or published, breaks protection, which 3-LEGAL.md forbids. FModel's key list (F7) had no row for the game and points to a cracking forum, which this kit does not follow." Delete "cs.rin.ru;" from section 6. Change option B to "(B) both games (3-LEGAL.md calls unpacking closed; Mafia has no publisher's tools)".
2. **WHAT:** "Use only a published file" hands the dumping step to a stranger, because the archive's mapping file was dumped from the running game. **WHERE:** section 3 step 4. **FIX:** Replace "3-LEGAL.md leaves such attachments out, so use only a published file." with "Every mapping file, the published one included, is dumped from the running game, which 3-LEGAL.md leaves out, so using one is part of his ruling."
3. **WHAT:** On KM-A-12, "new" means the new table format and "supported since 1.2" means it can be patched since 1.2. The page does not say these tables arrived in 1.2. **WHERE:** section 2 table, the NPC behaviour, Crime and Reputation rows. **FIX:** Change "from patch 1.2", "(new, since 1.2)" and "(since 1.2)" to "(new format, patchable since 1.2)".
4. **WHAT:** It misses KM-A-27 "Crime", which is in the same snapshot. That article says crime is "mainly in AI Behavioral trees", defines each crime in rpg/crime.xml (fine, jail, expiration, isSpreadable) and sets crime memory in ai/script_params.xml. **WHERE:** section 2 Crime and Witnesses rows; section 4 B; sections 5a and 6. **FIX:** Add to the Crime row "each crime in rpg/crime.xml (fine, jail, expiration, isSpreadable); its tuning in ai/script_params.xml; the logic mostly in AI behaviour trees [R K1: KM-A-27]". Set the Witnesses lead to "isSpreadable and the crime_* memory values (KM-A-27) [I]". Put KM-A-27 first in B and add it to 5a.
5. **WHAT:** F:\LedgerStudy is not named in retention.json. F:\LedgerTools\reference-other-games is named there, protected, for exactly this. **WHERE:** sections 1, 2 step 5 and 3 step 6. **FIX:** Replace each "F:\LedgerStudy\" with "F:\LedgerTools\reference-other-games\", and "(the tools drive, outside the repository)" with "(named in retention.json, outside the repository)".
6. **WHAT:** The reading list sends readers to K2's copy of Warhorse's Lua binding docs, in a repository of extracted game files and DLLs. The tools ship those docs themselves (KM-A-55). **WHERE:** section 5a, the K2 line. **FIX:** Replace it with "Warhorse's Lua binding docs: Tools\modding\docs\ in the modding tools (KM-A-55). K2's copy is not used."
7. **WHAT:** An unreached interview decides in advance that three Mafia studies will find nothing. **WHERE:** the end of section 3; section 4 A and C. **FIX:** Replace the section 3 sentence with "An unreached interview is said to call it story-led [S7]; this is a lead only." Delete "Probably absent [I]." and "Likely absent [I]."
