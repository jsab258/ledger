# AAA reference: the index and the coverage map

The index the study plan (STUDY-PLAN.md) names: every system Mafia: The Old Country and Kingdom Come: Deliverance II have, where its logic lives, and which study covers it. Each study ticks its systems off here and adds its own file beside this one. Numbers, structures and names only; the games' files stay on F:\LedgerTools\aaa-study and never enter git.

Made 25 October 2026 at set-up, from the installed copies (C:\Games). Measured, not recalled: every count below was read from the files that day.

## Set-up state

- **KCD2:** its archives are ordinary zip files; 99 archives indexed (one list per archive in F:\LedgerTools\aaa-study\kcd2\index), 10 of them from nine third-party mods installed in this copy. The readable data is unpacked to F:\LedgerTools\aaa-study\kcd2\unpacked: 31,150 files, 851 MB (tables, scripts and behaviour trees, both levels' layers, animation databases, English text). Unpacked with Python's zip reader (7-Zip is not installed; same result). Meshes, textures, sound and video stay packed until a study needs them. Warhorse's official tools are not installed: they come only through a Steam account that owns the game, and their licence covers individuals making mods, not companies or study (KCD2-OFFICIAL-TOOLS.md; the choice is Jafar's). Warhorse's public modding wiki documents where each system lives and was read instead. This copy is version 1.2 (Steam's is 1.5.6) and has nine third-party mods installed: recordings for the study are made with them off.
- **Mafia:** 29 container files, 47.3 GB, Unreal 5 (container format version 6). Eight content containers are encrypted; the engine's global container and one small optional container (56 MB) are in the clear. No published file key was found (sources in DECISIONS.md, 25 October), so FModel is installed (F:\LedgerTools\aaa-study\tools) but cannot open the packages yet.
- **Mafia, what could be read without the key:**
  - chunk ids are stored in the clear, so the first export index counts each container's packages and data kinds (F:\LedgerTools\aaa-study\mafia\containers.json): 139,791 packages, 28,761 bulk-data chunks and 7,137 shader chunks;
  - the global container lists every compiled object by name, 51,822 across 653 modules, engine included; the game's own 216 modules hold 12,956 of them (script-objects.json, game-modules.json).
  - Asset names and types wait for a key.

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

Where: **data** = tables and assets; **script** = behaviour trees, Lua, quest files; **code** = compiled. Mafia's code column names the module and its count of compiled objects (classes, structures and the like, each class's default object included); its data and Blueprint side is unknown until the key (marked *after key*).

| System | KCD2: where | Mafia: where | Study | Ticked |
|---|---|---|---|---|
| NPC daily life and schedules | data: level scheduler tables, smart objects, situations; script: AI/npc, AI/profession | code: H13SmartObjects 37, H13AIRoles 61, H13AIWorldState 41; data *after key* | 1 | |
| NPC brains and decisions | data: brain and subbrain tables; script: 1,400 AI trees | code: H13AICore 530, NeroAI 424, H13AIBehaviorTree 11 | 1 | |
| Perception and awareness | script: hearing subscriptions, nervousness flags | code: H13AIPerceptionAndAwareness 86, NeroAIPerceptionRuntime 3 | 1, 15 | |
| Group coordination and squads | data: situation roles | code: H13AICoordination 176, H13AISquads 15, NeroAICoordinationRuntime 27 | 1, 14 | |
| Crime: witnesses, reporting, arrest, punishment | data: crimes, crime roles; script: Crime.lua, AI/crime 308 | code: H13NPCReactions 53, NeroAIReactions 18 | 15 | |
| Reputation by place and faction | data: reputation tables, faction tree, renown | none seen by name: open blind spot | 11 | |
| NPC mood and anger | data: angriness, morale, nervousness | code: H13StateLayer 61 (unconfirmed) | 11 | |
| Random world events | data: RandomEvent tables, situation frequency | none seen by name | 1 | |
| Dialogue and choices | data: dialogue-system tables, English text; script: quests | code: H13Lexicon 31; data *after key* | 3 | |
| Barks (short lines in the street) | data: dialogue hearing, voice groups | code: H13Bark 79, H13BarkGame 6 | 3 | |
| Missions, jobs, story | script: 18,691 quest files; data: documents | code: H13MissionSystem 465, H13ChallengeSystem 108 | 16 | |
| Cutscenes and staging | data: cinematic clips 2,206, cutscene table | code: H13Sequencer 78, H13Cinematic 33 | 16 | |
| Melee and close combat | data: 48 combat tables | code: GameFeatureCQCRuntime 215 | 14 | |
| Guns, cover, aiming | (not in KCD2) | code: H13CoverSystem 115, NeroWeapons 11, H13DynamicTargeting 43, aim assist 34 | 14 | |
| Damage, hit reactions, health | data: hit reactions, damage types | code: H13DamageReactions 74, H13Impacts 82, H13Health 18, H13PhysicalAnimation 16 | 14 | |
| Abilities and effects | data: buffs, perks | code: H13GAS 188 (Unreal's ability system) | 11, 14 | |
| Doors, pick-ups, world interaction | data: door animation sets, picking, smart entities | code: H13InteractionSystem 85, H13WorldInteractions 86, H13EnvironmentInteraction 11 | 4, 7 | |
| Characters, faces, clothes | data: clothing tables, body layers, clothing presets, blood masks | code: H13OutfitCore 52, DNAFramework 80 (MetaHuman faces), SkeletalMerging 7 | 6 | |
| Locomotion and animation | data: 752 clips, 777 blend spaces, 94 animation databases, fragment tables | code: H13CapsuleChar 308, H13AnimCore 99, H13CharacterProceduralGround 20 (feet on the ground), H13MovementPrediction 4, H13AnimationSharing 21 | 7 | |
| Vehicles | (horses only) | code: H13Vehicles 525 | 9-13 | |
| Animals | script: AI/animal 98 | code: H13Animals 171 | (not LEDGER's) | |
| Sound and ambience | data: 309 sound banks, music | code: AkAudio 569 (Wwise), H13Audio 162, H13AudioAmbient 69 | 8 | |
| Interface and menus | data: 33 ui tables | code: NeroUI 1,120, NoesisRuntime 119 | 9-13 | |
| Saving | code only | code: H13SaveGame 94 | 9-13 | |
| Streaming the open world, budgets | data: level layers, distant-detail archives | code: H13WorldPartition 28, H13SignificanceSystem 42, H13MemoryBudget 21, H13StreamingAssistant 3 | 4, 5 | |
| Look: light, weather, post-process | data: engine config (42 files), time-of-day, weather profiles | code: H13RenderParametersDriver 9, H13Upscaler 42; data *after key* | 5 | |
| Economy and shops | data: shop table, money changes, item tables | none seen by name | 11 | |
| Time and needs (sleep, food) | data: skip-time, sleeping spots, food types, buffs | none seen by name | 11 | |
| Difficulty | data: game modes | code: H13DifficultySystem 37 | 9-13 | |
| Automated testing | script: 2,527 test quest files, autotest trees, feature tests | code: H13AutomatedTestSystem 21, NeroATS 21, H13Telemetry 30 | method only | |
| Minigames | data: minigame tables | none | not studied (not LEDGER's) | |

## Open blind spots

- **Mafia's data, Blueprints and levels:** all of them, until a key. The coverage map's Mafia column is the compiled side only.
- **KCD2's compiled side:** how the code runs its tables (schedules, crime judgement, reputation). A targeted code read is needed if a study finds the tables are not enough.
- **Behaviour seen in play:** none listed yet. Jafar's recordings of each game's first hour are still to come (STUDY-PLAN, set-up).
