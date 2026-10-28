# Study 13: Production pipeline (28 October 2026)

How Mafia: The Old Country and Kingdom Come: Deliverance II organise, name and tune their content, read from their file indexes and tables, beside LEDGER's repository, Unreal project and specs. Our own words and numbers. Raw notes on F:/LedgerTools/aaa-study: mafia/study-9-10-13/notes (naming_counts.txt), kcd2/study-9-10-13/NOTES.md and its CSVs; read 28 October 2026. Tags: **M** measured, **R** read, **I** inferred, **N** a name only.

**The short answer.** Both studios keep tuning out of code.
- **Mafia:** 611 data tables outside its text folders (most of them tuning, I), 2,453 text tables, 3,748 data assets and 149 curves. Its settings, camera modes and input timings are all data (Studies 9 and 10). 92% of its own non-map assets carry a short type prefix, mostly Epic's usual ones.
- **Kingdom Come II:** 87,600 rows in 1,243 schema-checked XML tables. 98.7% of its file names are snake_case.
- **LEDGER:** half way. Its street, cast, look and rooms are JSON specs. But its camera, reach and settings are C++ constants, it has no data tables or curves, and 23% of its own Unreal assets carry a type prefix.

The improvements: a tuning home in the catalogue, a naming rule with a check, and settings as data.

## The numbers

| | Mafia | Kingdom Come II | LEDGER |
|---|---|---|---|
| Own content | 139,154 packages in one game folder plus plugins (M) | 809,387 files, 111.85 GB, in 89 own archives (M) | 2,565 Unreal assets in Content/Ledger; about 2,050 more in Epic's sample, MetaHuman and character folders, not counted (M) |
| Top folders | 51; median depth 5, deepest 10 (M) | dialog 280,344; textures 166,432; objects 127,804 (M) | 15 folders by kind (M) |
| Type prefix | 91.7% of non-map assets; 60.1% Epic's usual ones; 185 prefixes (M) | none: type by extension and suffix (M) | 23% (582) (M) |
| Case slips | 16 prefixes written two ways (MI 11,805, Mi 30) (M) | 35.1% of names have capitals (M) | |
| Variants in names | _a.._z 12,973; _NN 3,770; sizes such as 90x240cm 803 (M) | 14 texture suffixes cover 99.6% (M) | mixed (M) |
| Data tables | 3,064: text 2,453, others 611 (M) | 1,243 XML tables, 87,600 rows, 13 schemas (M) | none (M) |
| Data assets; curves | 3,748; 149 (M) | none readable (M) | none (M) |
| Player settings | 122 rows in 4 tables (M) | not in data | 22 lines in C++ (R) |
| One key-value table | | rpg_param: 323 values in 93 families (M) | |
| Numbers in code | not read (compiled) | not read | about 220 numeric constants in the game's C++, 356 in the C# Core (M, by declaration lines) |
| Specs as data | | | production/specs: 42 entries, 55 files; 18 JSON named by the game or its staging (M) |

## Folder structure

- **Mafia:** one game folder, then by discipline (M): maps 45,898, animation 22,781, environment 19,396, audio 15,429, text 9,238, characters 8,629. Within a discipline it goes by family, then piece (Environment/Buildings/Elements/Doors/DoorWing90x240cm_01/). Tuning sits beside its system (Camera/Curves, Game/NeroSettingsDataTables). The game's own code is 216 modules; the studio's shared plugins are kept apart from the game's.
- **Kingdom Come II:** by data kind: table libraries (rpg, item, ai, combat, ui), scripts, animations, levels with layers named by a GUID (3,562 of 3,562), localisation.
- **LEDGER:**
  - the repository: production/ (32 entries), 125 research folders, 127 tools;
  - the Unreal project: Content/Ledger by kind (Kit, People, ShopFronts, ShopRooms, Street, Props...);
  - the catalogue names one home per kind of fact, but has no row for tuning numbers.

## Naming conventions

- **Mafia:**
  - type, family, variant, side or number: BP_CameraMode_Aim_Firearm_Left, MI_DoorWing90x240cm_VBlend2_01_b;
  - kit pieces carry their size (803 names).
  - The slips are few: 16 prefixes written two ways, and one misspelt table row ("Praecisone"). A check would catch both.
- **Kingdom Come II:** snake_case on 98.7% of names, though 35.1% use capitals. Type comes from the extension and a suffix: _diff on 42% of textures, _lodN on 22% of meshes.
- **LEDGER:**
  - 582 of 2,565 of its own Unreal assets carry Epic's prefixes. The rest keep their source's names: grooms, Blender pieces called "street", "hall", "glass".
  - Tools mix underscores (41 names) and hyphens (65). Research folders are all lower case (125 of 125).
- **Mafia's counts by type** (own content, M): textures 12,632; material instances 11,805; static meshes 10,637; animation sequences 7,204; montages 2,974; Blueprints 3,892; voice lines 25,360; input actions 166; mapping contexts 22.

## How tuning lives in data

- **Mafia: one pattern everywhere.** A system's settings name its table, and each row holds a rule and its numbers.
  - The camera manager names the camera table (Study 9).
  - The settings tables hold each setting's default, range, step and help text (Study 10).
  - Difficulty is six tables (player, enemy, aim assist, wingman, loot, duels), named in DefaultGame.ini (R).
  - Input timings sit on each action's trigger (R).
  - Curves carry shapes code would bury: camera distance by pitch, lens by speed.
- **Kingdom Come II: tables under a schema.** One schema with primary keys; 363 binary twins (caches, I). rpg_param holds 323 numbers, such as sight radius 50, pickpocketing distance 2.4 and attack charging cooldown 1.4 (R). Per-perk tables override them without touching the base.
- **LEDGER:**
  - Specs: the street, cast, sounds, look, office and shop rooms, checked against their homes (homes_check.py, the spec tests).
  - C++ constants: the camera (arm 3.2 m, offsets 0.45 and 0.55 m, hide within 55 cm), the reaches (3.5 and 2.2 m), walk and run speeds, and every settings line. Only the office camera reads a spec.

## For LEDGER

1. **Adopt: a "tuning numbers" row in CATALOGUE.md's homes table.**
   - Home: production/specs/tuning/ (camera, input, interface, talk), staged with the game as stage_game_data.py requires.
   - A check fails the build when a spec's number is also a C++ constant.
   - It serves CLAUDE.md's "one home per fact"; Study 9's camera numbers go there first.
2. **Adopt: rows in order, each a rule over Tom's state and its numbers.** This is our design, after Mafia's tables, for Study 9's four camera rows; the same shape later suits prompts and the interface's visibility.
3. **Adopt: a naming rule for new Unreal assets of our own, with a check in CI.**
   - Epic's prefixes (T_, M_, MI_, SM_, SK_, AS_, AM_, BP_, DA_, DT_, NS_), then family, variant, _NN, and sizes in kit names.
   - Case is checked.
   - Imports (MetaHumans, Megascans, Epic's sample) keep their names in their own folders.
   - Rules alone have not held (CLAUDE.md); it serves the catalogue and RECIPE.md's scaling.
4. **Adapt: settings as data.** A settings spec (default, range, step, help text) read by LedgerSettings, in place of 22 hard-coded lines, before Study 10's width and scale come.
5. **Adapt: snake_case for new tools only;** renaming old ones would be churn.
6. **Ignore:** binary twins and GUID layer names (an engine's need), and Unreal data tables for now. JSON is diffable in git and readable by the C# Core; tables pay only when designers tune in the editor.

## Coverage map

Add a row "Pipeline: folders, naming, tuning in data" (Mafia: 611 non-text tables, 3,748 data assets, 149 curves; Kingdom Come II: 1,243 schema tables), ticked 28 October (Study 13).

## Open blind spots

- Mafia's source-side checks and folder rules do not ship. Asset-registry tags such as asset status and validation hint at them (N).
- How either studio tunes in the editor: no talk was read for it.
- Kingdom Come II: 8 tables that do not parse are missing from the row count.

## Sources (read 28 October 2026)

- **Mafia:** the package index (139,791 names) and prefix counts, game-modules.json (REFERENCE.md), DefaultGame.ini, this study's camera, settings and input exports.
- **Kingdom Come II:** 89 Warhorse archive indexes (the mods' 10 left out), Libs/Tables, its schemas, rpg_param.xml, the engine configs.
- **LEDGER:** ue-probe/Content and Source, ledger/Assets/Scripts/Core, production/specs, CATALOGUE.md.

## Review

The same fresh reviewer (28 October): pass with fixes, all applied: case and snake_case shares, the 611 tables' tuning share inferred, data assets and own-content counts re-measured, the camera table named by its manager, LEDGER's asset, spec and constant counts and their rule, the port link dropped, REFERENCE.md added. Cost: within Study 9's.
