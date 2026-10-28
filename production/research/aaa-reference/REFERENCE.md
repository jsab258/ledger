# AAA reference: the index and the coverage map

The index the study plan (STUDY-PLAN.md) names: every system Mafia: The Old Country and Kingdom Come: Deliverance II have, where its logic lives, and which study covers it. Each study ticks its systems off here and adds its own file beside this one. Numbers, structures and names only; the games' files stay on F:\LedgerTools\aaa-study and never enter git.

Made 25 October 2026 at set-up, from the installed copies (C:\Games). Measured, not recalled: every count below was read from the files that day.

## Set-up state

- **KCD2:** its archives are ordinary zip files; 99 archives indexed (one list per archive in F:\LedgerTools\aaa-study\kcd2\index), 10 of them from nine third-party mods installed in this copy. The readable data is unpacked to F:\LedgerTools\aaa-study\kcd2\unpacked: 31,150 files, 851 MB (tables, scripts and behaviour trees, both levels' layers, animation databases, English text). Unpacked with Python's zip reader (7-Zip is not installed; same result). Meshes, textures, sound and video stay packed until a study needs them. Warhorse's official tools are not installed: they come only through a Steam account that owns the game, and their licence covers individuals making mods, not companies or study (KCD2-OFFICIAL-TOOLS.md; the choice is Jafar's). Warhorse's public modding wiki documents where each system lives and was read instead. This copy is version 1.2 (Steam's is 1.5.6) and has nine third-party mods installed: recordings for the study are made with them off.
- **Mafia:** 29 container files, 47.3 GB, Unreal 5 (container format version 6). Eight content containers are encrypted; the engine's global container and one small optional container (56 MB) are in the clear. A published file key was found the same afternoon (its source is recorded in STUDY-PLAN.md, set-up) and kept in F:\LedgerTools\keys\mafia-aes.txt, never in git. It decrypts every container's name index, and the names match the package counts taken before the key. FModel is installed (F:\LedgerTools\aaa-study\tools), set to Unreal 5.4 with the key, and runs on the .NET 10 runtime on F:. It mounts the archives, reads the text resources, and opens packages with the published mappings file (TheNaeem's archive, the game's 4 December 2025 update; source and checks in STUDY-PLAN.md, set-up record). Every kind tried opened: data tables, animation sequences and montages, material instances, static and skeletal meshes, and AI state trees.
- **Mafia, read before the key:**
  - chunk ids are stored in the clear, so the first export index counts each container's packages and data kinds (F:\LedgerTools\aaa-study\mafia\containers.json): 139,791 packages, 28,761 bulk-data chunks and 7,137 shader chunks;
  - the global container lists every compiled object by name, 51,822 across 653 modules, engine included; the game's own 216 modules hold 12,956 of them (script-objects.json, game-modules.json).
- **Mafia's first export index, with the key** (F:\LedgerTools\aaa-study\mafia\index, one name list per container plus SUMMARY.json, PAKS.json, PREFIXES.json):
  - every one of the 139,791 packages named: 139,154 are the game's own content, 637 the engine's;
  - main folders: maps 45,898 (the open world's cells 27,680, distant-detail 13,053, prologue 2,438); animation 22,781 (faces 13,410, gameplay 4,314, scripted 3,396, cinematic 1,484); environment 19,396 (props 7,138, locations 4,838, buildings 4,177, vegetation 2,241); Wwise audio assets 15,429; text 9,238; characters 8,629; materials 3,828; cinematics 1,981; vehicles 1,540; world interactions 1,480; effects 1,274; AI 595;
  - asset types read from the name prefixes (382 of them), by the usual meaning of each: textures 12,680, material instances 11,843, static meshes 10,645, animation sequences 7,204, Blueprints 3,892, data assets 3,748, data tables 3,064, montages 2,974, state trees and other AI assets in the AI folder;
  - the .pak files hold the sound itself (107,869 Wwise sound files and 91,407 sound banks), plus config files and plug-in descriptions: 203,981 names in all.

| Container | Packages | Size (package data only; the index files add 6.1 GB) |
|---|---|---|
| pakchunk400 | 80,135 | 20.2 GB |
| pakchunk200 | 17,090 | 7.7 GB |
| pakchunk0 | 14,661 | 3.0 GB |
| pakchunk100 | 13,607 | 2.0 GB |
| pakchunk300 | 5,733 | 1.6 GB |
| pakchunk6 | 5,505 | 3.5 GB |
| pakchunk5 | 2,900 | 2.1 GB |
| pakchunk80 | 160 | 1.0 GB |

## Where KCD2's logic lives (the first index)

- **Daily schedules:** each level's own scheduler table (Kuttenberg's region 60.1 MB, 64,529 smart hubs with 117,225 activity links; Trosky's 21.4 MB, 21,633 hubs with 42,562 links), plus 12 scheduler layers. The NPC brains that follow them: the ai tables (brain, subbrain, situation, smart objects; 623 files with their parts) and the AI behaviour trees (AI/npc 221, AI/profession 102, AI/situation 39).
- **Crime:** a crimes table (30 crimes), the crime-role table on each soul, a 170-line crime system script, and 308 crime behaviour trees. Their names show witnesses, hearing, trespass escalation, arrest, frisking, punishment.
- **Reputation:** reputation changes (203 rows), conditions and notifications, the faction tree, renown and relationship flags.
- **Quests:** 18,691 quest files (and 16 pictures).
- **Dialogue:** 23 dialogue-system tables plus 11 English text files (33 MB).
- **Combat:** 48 tables in 92 files (attacks, blocks, perfect blocks, ripostes, zones).
- **Items and clothing:** 47 item tables in 263 files, including body layers and clothing presets; 8 clothing tables (blood masks, hiding groups, morphs).
- **Character state:** 97 rpg tables in 476 files (skills, perks, buffs, stats). Table files come as a readable copy, a binary copy and per-area parts, so files outnumber tables.
- **Compiled side:** what the executable does with these tables (how a schedule entry becomes a walk, how a crime is judged) is in code, not data. Any such system LEDGER needs gets a targeted code read (STUDY-PLAN, coverage map).

## The coverage map

Where: **data** = tables and assets; **script** = behaviour trees, Lua, quest files; **code** = compiled. Mafia's code column names the module and its count of compiled objects (classes, structures and the like, each class's default object included); its data side is now named by folder, read file by file in each study.

| System | KCD2: where | Mafia: where | Study | Ticked |
|---|---|---|---|---|
| NPC daily life and schedules | data: level scheduler tables, smart objects, situations; script: AI/npc, AI/profession | code: H13SmartObjects 37, H13AIRoles 61, H13AIWorldState 41; data: AI roles 97, state trees 196, spawner definitions 422 | 1 |data side 25 Oct, studies/01-npc-life.md |
| NPC brains and decisions | data: brain and subbrain tables; script: 1,400 AI trees | code: H13AICore 530, NeroAI 424, H13AIBehaviorTree 11 | 1 |data side 25 Oct (Study 1); code not read |
| Perception and awareness | script: hearing subscriptions, nervousness flags | code: H13AIPerceptionAndAwareness 86, NeroAIPerceptionRuntime 3 | 1, 15 |constants 25 Oct (Study 1); trespass 28 Oct (Study 15) |
| Group coordination and squads | data: situation roles | code: H13AICoordination 176, H13AISquads 15, NeroAICoordinationRuntime 27 | 1, 14 |KCD2 28 Oct (Study 14: no attacker cap in its data); Mafia's coordination files not exported (F: full) |
| Crime: witnesses, reporting, arrest, punishment | data: crimes, crime roles; script: Crime.lua, AI/crime 308 | code: H13NPCReactions 53, NeroAIReactions 18 | 15 |witness side 25 Oct (Study 1); arrest, search, punishment, theft, trespass, fencing 28 Oct (Study 15) |
| Reputation by place and faction | data: reputation tables, faction tree, renown | none seen by name: open blind spot | 11 |KCD2 25 Oct (Study 1); Mafia: none, confirmed 28 Oct (Study 11) |
| NPC mood and anger | data: angriness, morale, nervousness | code: H13StateLayer 61 (unconfirmed) | 11 |KCD2's rates 28 Oct (Study 11) |
| Random world events | data: RandomEvent tables, situation frequency | none seen by name | 1 | |
| Dialogue and choices | data: dialogue-system tables, English text; script: quests | code: H13Lexicon 31; data: text 9,238 (scripted, systemic, handcrafted, cinematic), 2,452 lexicon assets | 3 | |
| Barks (short lines in the street) | data: dialogue hearing, voice groups | code: H13Bark 79, H13BarkGame 6 | 3 | |
| Missions, jobs, story | script: 18,691 quest files; data: documents | code: H13MissionSystem 465, H13ChallengeSystem 108 | 16 |states and counts 28 Oct (Study 11); the rest Study 16; openings side 28 Oct (Study 2) |
| Cutscenes and staging | data: cinematic clips 2,206, cutscene table | code: H13Sequencer 78, H13Cinematic 33 | 16 |opening lengths 28 Oct (Study 2) |
| Melee and close combat | data: 48 combat tables | code: GameFeatureCQCRuntime 215 | 14 |28 Oct, studies/14-combat.md (KCD2's tables; Mafia's fists and names, its close-combat files not exported, F: full) |
| Guns, cover, aiming | (not in KCD2) | code: H13CoverSystem 115, NeroWeapons 11, H13DynamicTargeting 43, aim assist 34 | 14 |names only 28 Oct (Study 14); guns come last |
| Damage, hit reactions, health | data: hit reactions, damage types | code: H13DamageReactions 74, H13Impacts 82, H13Health 18, H13PhysicalAnimation 16 | 14 |28 Oct, studies/14-combat.md; Mafia's damage and hit-stop values not read (F: full) |
| Abilities and effects | data: buffs, perks | code: H13GAS 188 (Unreal's ability system) | 11, 14 |punishments as effects 28 Oct (Study 15); melee side 28 Oct (Study 14) |
| Doors, pick-ups, world interaction | data: door animation sets, picking, smart entities | code: H13InteractionSystem 85, H13WorldInteractions 86, H13EnvironmentInteraction 11 | 4, 7 |animation side 25 Oct (Study 7); the rest Study 4; street side 25 Oct (Study 4); locks 28 Oct (Study 15) |
| Characters, faces, clothes | data: clothing tables, body layers, clothing presets, blood masks | code: H13OutfitCore 52, DNAFramework 80 (MetaHuman faces), SkeletalMerging 7 | 6 |25 Oct, studies/06-characters-wardrobe.md |
| Locomotion and animation | data: 752 clips, 777 blend spaces, 94 animation databases, fragment tables | code: H13CapsuleChar 308, H13AnimCore 99, H13CharacterProceduralGround 20 (feet on the ground), H13MovementPrediction 4, H13AnimationSharing 21 | 7 |25 Oct, studies/07-animation.md |
| Vehicles | (horses only) | code: H13Vehicles 525 | 9-13 | |
| Animals | script: AI/animal 98 | code: H13Animals 171 | (not LEDGER's) | |
| Sound and ambience | data: 309 sound banks, music | code: AkAudio 569 (Wwise), H13Audio 162, H13AudioAmbient 69 | 8 | |
| Interface and menus | data: 33 ui tables | code: NeroUI 1,120, NoesisRuntime 119 | 9-13 |first appearances 28 Oct (Study 2) |
| Saving | code only | code: H13SaveGame 94 | 9-13 |both games 28 Oct (Study 11); opening saves and checkpoints 28 Oct (Study 2) |
| Streaming the open world, budgets | data: level layers, distant-detail archives | code: H13WorldPartition 28, H13SignificanceSystem 42, H13MemoryBudget 21, H13StreamingAssistant 3 | 4, 5, 12 |budget side 25 Oct, studies/12-tech-budgets.md; streaming side 25 Oct, studies/04-street-world.md |
| Look: light, weather, post-process | data: engine config (42 files), time-of-day, weather profiles | code: H13RenderParametersDriver 9, H13Upscaler 42; data: lighting 392, TODP assets 104 (by the prefix, time-of-day profiles), materials 3,828 | 5 |settings side 25 Oct, studies/05-visuals.md |
| Economy and shops | data: shop table, money changes, item tables | none seen by name | 11 |both games 28 Oct (Study 11) |
| Time and needs (sleep, food) | data: skip-time, sleeping spots, food types, buffs | none seen by name | 11 |time, sleep, weather 28 Oct (Study 11); food not studied |
| Difficulty | data: game modes | code: H13DifficultySystem 37 | 9-13 | |
| Automated testing | script: 2,527 test quest files, autotest trees, feature tests | code: H13AutomatedTestSystem 21, NeroATS 21, H13Telemetry 30 | method only | |
| Tutorials and onboarding | data: hint and tutorial tables (Study 2) | data: tutorial assets and prompts (Study 2) | 2 | 28 Oct (Study 2) |
| Minigames | data: minigame tables | none | not studied (not LEDGER's) | |

## Open blind spots

- **Mafia's data, Blueprints and levels:** named, counted and openable, not yet read: each study reads its own files. The mappings file is older than the installed game, so a package of a kind not yet tried may still fail; any that does is listed here. Most of the Mafia column's data entries are still blank.
- **KCD2's compiled side:** how the code runs its tables (schedules, crime judgement, reputation). A targeted code read is needed if a study finds the tables are not enough.
- **Behaviour seen in play:** none listed yet. Jafar's recordings of each game's first hour are still to come (STUDY-PLAN, set-up).
