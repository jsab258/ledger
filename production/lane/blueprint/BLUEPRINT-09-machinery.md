# BLUEPRINT 09: The machinery

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. How the game is made: Kiln, the art pipeline, one simulation, the port, tests, records.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 9.1 Kiln

His clothing pipeline, then props, vehicles, buildings and people modules.


### 9.1 Kiln

- How it works: His clothing pipeline, then props, vehicles, buildings and people modules. Paused now: after the Marvelous export, Kiln, hair and the crowd wait for the browser prototype's evening, and no Unreal work runs until the prototype is done (RULINGS 20 and 21 Nov).
- Standard: Three proofs before any other module (18 Nov): held-back garments pass; Ron walks the packaged game in a Kiln outfit; a garment costs a fraction of the old route Test: Kiln v1 checklist; held-back jobs
- Source: RULINGS 13, 14, 18 Nov (machinery: not met by the player; no coverage row). Designed in: Kiln design note; KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.1 Drape

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.2 Kiln-to-game adapter

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.3 Garment mesh chain (weld, retopology, layout, bake)

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.4 Skinning and pose tests

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.5 Import to Unreal

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.6 Packaged wear film and gate

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.7 Bend-back for posed bodies

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.1.8 Cloth hand-off in game (Chaos, for skirts)

- How it works: A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).
- Standard: The plan's stage check Test: the plan's stage check
- Source: KILN-TO-GAME-PLAN-2026-11-17 (machinery: not met by the player; no coverage row). Designed in: KILN-TO-GAME-PLAN
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.2 Art pipeline

MetaHuman casting, Blender kits, the asset plan, the catalogue.


### 9.2 Art pipeline

- How it works: MetaHuman casting, Blender kits, the asset plan, the catalogue.
- Standard: Every asset family follows the asset plan (3 Oct); reuse first Test: catalogue line per asset
- Source: RULINGS 3 Oct; CLAUDE.md (machinery: not met by the player; no coverage row). Designed in: asset plan; CATALOGUE
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.3 One simulation

The C# Core as source of truth, its C++ port in Unreal, its browser build in the prototype; one set of goldens.


### 9.3 One simulation

- How it works: The C# Core as source of truth, its C++ port in Unreal, its browser build in the prototype; one set of goldens.
- Standard: The port matches the C# goldens; 102,949 browser rows matched (19 Nov); town simulation frozen until C#'s replaces the prototype's Test: CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest; goldens identical
- Source: canon OPEN 1; RULINGS 18-19 Nov; advisor 249 (machinery: not met by the player; no coverage row). Designed in: ONE-SIM-METHOD-2026-11-19
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.4 Prototype to Unreal port

Each system proved in the prototype ported under the same tests (money, debts, jobs, fights, talk).


### 9.4 Prototype to Unreal port

- How it works: Each system proved in the prototype ported under the same tests (money, debts, jobs, fights, talk).
- Standard: Unreal ports its money, debts, jobs, fights and talk under the same tests (ruling 18-19 Nov; ONE-SHOT-PORTING.md) Test: same tests pass in both
- Source: RULINGS prototype line; advisor 254 (machinery: not met by the player; no coverage row). Designed in: ONE-SHOT-PORTING.md (to be written)
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.5 Testing and gates

The clumsy-player bot, scripted tests, the AI hands-on session, the panel of eight, the nightly packaged walk, the publish gate.


### 9.5 Testing and gates

- How it works: The clumsy-player bot, scripted tests, the AI hands-on session, the panel of eight, the nightly packaged walk, the publish gate.
- Standard: DESIGN §19; a play build reaches him only with a publish-gate pass and a known-issues note Test: gate.py passes; nightly walk report
- Source: DESIGN §19; RULINGS 18 Nov (machinery: not met by the player; no coverage row). Designed in: DESIGN §19; tools/lane/gate
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.6 The tuning table

One home for every number the browser, the Core and Unreal are tuned from.


### 9.6 The tuning table

- How it works: One home for every number the browser, the Core and Unreal are tuned from.
- Standard: Every rule's number in one table (DESIGN §19; Study 13) Test: S: no magic number outside the table
- Source: DESIGN §19 (machinery: not met by the player; no coverage row). Designed in: prototype rules.js
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.7 Records and guards

Doc caps, approvals, retention, git size guard, content and canon gates.


### 9.7 Records and guards

- How it works: Doc caps, approvals, retention, git size guard, content and canon gates.
- Standard: CLAUDE.md Records and Builds Test: guards run on every commit
- Source: CLAUDE.md (machinery: not met by the player; no coverage row). Designed in: tools/
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.7.1 Licence and terms record

- How it works: The allowlist and THIRD-PARTY.md: every source's licence recorded; decided by the sessions (19 Nov).
- Standard: The allowlist is law; licences never go to him (19 Nov) Test: every shipped file on the allowlist
- Source: CLAUDE.md; advisor 252 (machinery: not met by the player; no coverage row). Designed in: license-allowlist.md
- Status: machinery. Coverage row: none (group 9 is not met by the player).

### 9.7.2 Recipe and handover

- How it works: RECIPE.md and the handovers, so the method survives without the history.
- Standard: RECIPE rewritten each phase; monthly cold re-run (18 Nov) Test: monthly cold re-run judged by the gate
- Source: RULINGS 9, 18 Nov (machinery: not met by the player; no coverage row). Designed in: RECIPE.md
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.8 Talk bench

Choosing talk and voice models by the kind of moment, re-checked monthly.


### 9.8 Talk bench

- How it works: Choosing talk and voice models by the kind of moment, re-checked monthly.
- Standard: D48; monthly from 7 Dec, three candidates at most Test: bench scores
- Source: RULINGS 1 Oct, 12 Nov (machinery: not met by the player; no coverage row). Designed in: RULINGS
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.9 Feel measurement

Measuring sheets for driving and the other felt verbs and activity shares, from footage, outside only.


### 9.9 Feel measurement

- How it works: Measuring sheets for driving and the other felt verbs and activity shares, from footage, outside only.
- Standard: DRIVING-MEASUREMENT-METHOD: five samples a number, two independent measurers, clips played never downloaded Test: two measurers agree within the sheet's tolerance
- Source: DRIVING-MEASUREMENT-METHOD-2026-11-19; advisors 255 to 257 (machinery: not met by the player; no coverage row). Designed in: DRIVING-MEASUREMENT-METHOD; FEEL-MEASUREMENT-METHOD-2026-11-20 (pending)
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.10 Plan, forecast and spend

The dated plan, forecasts, hour coding, allowances and caps; a new system placed in PLAN.md first.


### 9.10 Plan, forecast and spend

- How it works: The dated plan, forecasts, hour coding, allowances and caps; a new system placed in PLAN.md first.
- Standard: No new system before its place in PLAN.md (29 Sep); re-plan from measured pace (19 Nov H3 A) Test: Monday audit
- Source: RULINGS; advisor 241 point 2 (machinery: not met by the player; no coverage row). Designed in: PLAN.md; order ledgers
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.11 Reference studies and re-checks

The 18 studies, unreached sources, re-checks (Study 17 review, GTA VI after a month).


### 9.11 Reference studies and re-checks

- How it works: The 18 studies, unreached sources, re-checks (Study 17 review, GTA VI after a month).
- Standard: Research method (13 Oct): primary sources, dated, unreached listed Test: a fresh reviewer per study
- Source: CLAUDE.md research method (machinery: not met by the player; no coverage row). Designed in: aaa-reference studies
- Status: machinery. Coverage row: none (group 9 is not met by the player).

## 9.12 Design records

canon, VISION, DESIGN and its addendum, BUILD-ORDER, this parts tree.


### 9.12 Design records

- How it works: canon, VISION, DESIGN and its addendum, BUILD-ORDER, this parts tree.
- Standard: canon outranks; DESIGN approved 19 Nov; every part has a standard (RULINGS line proposed in advisor 257) Test: tools/lane/parts-tree/check.py
- Source: canon OPEN 3; advisor 257 (machinery: not met by the player; no coverage row). Designed in: production/lane/synthesis/
- Status: machinery. Coverage row: none (group 9 is not met by the player).


## 9.13 The browser build's modules, data and test door

Added 23 Nov (keeper run 2) from TECH-PLAN.md sections 2, 3, 7, 8 and 9 (not yet through its fresh reviewer).

### 9.13.1 Layers and boundaries
- How it works: five layers (data, rule pieces, the town, systems, presentation), each calling only the layers below; systems talk by events or exported reads and never write another system's state; presentation reads state and writes only its own view state; input passes through one place that turns keys into intents. The real town is the C++ one-simulation built to WebAssembly (35 bridge calls); the prototype's own script town keeps only what it does not cover, and a fact lives in one town, never both. No teleports (people move only along the street graph or through a door), no pinned people, one clock (60 s a game hour; the prototype still has 45 and its goldens are re-recorded), every random draw takes the run's seed, faults stay in their system. Pure rule pieces port to Unreal.
- Standard: no layer calls upward; no fact in both towns; a person jumping over 3 m in one tick on screen is a fault. Test: S: import check; the position-jump guard; same seed, same week. Source: TECH-PLAN section 2; 9.3. Status: decided.

### 9.13.2 Data formats
- How it works: plain JSON records in the game's data folder: people (with a voice id and the live-talk card; can_die false for Tom), places, jobs (kind, giver, act and rung minimum, steps each with a place, a verb, three keys and a failure step, pay to pocket, tin or book, a Ledger line), lines (who, situation, text, a once field of day, week or game), scenes and happenings (fired on a state, never a clock time alone; a cool-down in real minutes), the Ledger (only what Tom saw, heard, was told or read) and the numbers (one tuning table, about 2,415 numbers today, none written outside it). Every record carries an id and a src naming its design row.
- Standard: every record has a src; no number or player-facing string in code. Test: S: data check; the numbers check fails the build. Source: TECH-PLAN section 3; 8.9; 9.6. Status: decided.

### 9.13.3 The test door and the one-shot's plumbing hour
- How it works: the page exposes a test door (window.LEDGER): screen() (subtitles, prompts, panel text, people drawn with screen position and facing), mix() (sounds by name with loudness at the listener), perf() (logic median, 99th and worst over 600 ticks), talk, seeded launch, a stepped clock, saves as hand-overs. The one-shot's first hour does plumbing before any story: check the ready-made start (wasm, art and packages made the day before, checked by size and hash), the fixed step and job queue until the 99.9th percentile is under 4 ms, the clock to 60 and the goldens re-recorded, the jump guard, faults on screen, the three probes, and the 650 to 800 written strings and 14 fares moved into data with their src. Throughput the plan needs: about 45 builder hours in the week; at the first one-shot's 45 to 55 minutes a story, 41 stories take about 34 hours, leaving about 11 for faults, content and the gate.
- Standard: plumbing done on day one; tests speak to the door by intent; no story changes its own check. Test: the hidden and staging checks (planned, not built: premortem way 29). Source: TECH-PLAN sections 7 to 9. Status: decided.
