# TECH-PLAN: how the browser build is put together

Blueprint preparation item (a), written 23 Nov 2026 by the blueprint preparation session (Opus 5.5), for the one-shot that starts about Mon 7 Dec 13:00 (his ruling of 21 Nov, 10:42). Purpose: the one-shot builds the game, not plumbing. Everything here is either already in the prototype (and says where), or a rule the one-shot follows from its first hour.

Sources: tools/lane/prototype/ (code read and run on 23 Nov), production/lane/ONE-SHOT-PROMPT.md, ONE-SHOT-LOG.md, ONE-SHOT-CHECK-1 and -2 (20 Nov), ONE-SHOT-PORTING.md, ONE-SHOT-SIM-DIFFERENCES.md, premortem/PREMORTEM-2026-11-21.md, tools/lane/one-sim/ (README, BRIDGE, PROGRESS), tools/lane/gate/machine_checks.py, RULINGS.md on wip (clock 60 s a game hour, 21 Nov), BLUEPRINT-08-technical.md.

Words: "measured" means run on 23 Nov in this session and the method is given; "target" means a budget the one-shot must meet, not yet shown.

## 1. Measured on the current prototype (23 Nov)

Build: tools/lane/prototype/ at lane-2026-11 head, built with oneshot_dev.py (one-sim wasm rebuilt from source here, 423,015 bytes, the same size PROGRESS.md records), the 13 picture files read from the published page. Built folder 6.7 MB, ledger.js 2.36 MB. Measuring scripts: headless Chrome through the project's own test/harness.mjs, scripts kept in the scratch work folder (bp.mjs, bp2.mjs, bp3.mjs), not committed. The cloud machine has 2 cores and draws with SwiftShader (software), so every frame figure below is a floor on a software renderer, not a PC figure.

| What | Measured | Method |
|---|---|---|
| Page open to title screen | 3.2 s | harness launch to `window.LEDGER` ready and the loading cover hidden, 960 by 540 |
| New game to control | 9.3 s | click New game, read the letter, skip the ferry shot with Escape; the ferry shot itself is 20 s when not skipped |
| Logic step (one 1/60 s tick, no drawing) | median 0.10 ms, 95th 0.40 ms, 99th 6.6 ms, 99.9th 20.9 ms, worst 71.6 ms | 21,600 ticks (6 real minutes, Mon 15:36 to 23:36), `LEDGER.tick(1/60)` timed one by one |
| Logic step, mean by hour | 0.07 to 0.35 ms; worst single tick 34.5 to 40.7 ms in two other runs | 600 ticks at each of 8 hours |
| Ticks over 4 ms | 334 in 6 real minutes (about one a second) | same run |
| People alive in the sim | 38 in `G.people` (28 named plus walkers and others); the separate crowd list holds 29 figures, so the two overlap and were not added | `LEDGER.G.people`, `G.crowd` |
| People near Tom at 17:05 Monday, Quay Street bus stop | 7 within 26 m, 13 within 120 m | the rescaled design band for that hour is 12 to 20 over Quay Street's 100 m parade front (BLUEPRINT-02, FIT-G9); GD-02's "at least 25 in the busiest view" is a PENDING judgement figure |
| Frame, software, low quality, 960 by 540 | 367 to 370 ms, 121 draw calls, 70 thousand triangles | `LEDGER.benchmark()` (40 frames, readPixels each) |
| Frame, software, high quality, Quay Street 17:05 | 620 ms, 246 draw calls, 199 thousand triangles | same; another high run at the ferry gave 630 to 819 calls and 208 to 423 thousand triangles |
| Save | 24,000 to 32,000 characters, written in 0.7 ms | `LEDGER.saveText()` |

Earlier figures, not re-measured here: his PC (RX 6700, Chrome, High) gave 11.5 ms a frame at 2298 by 1252 with 541 draw calls on the 18 Nov build (project/DESIGN_NOTES.md); the town in wasm costs 17 to 22 ms per game day for 41 people in Node (one-sim/PROGRESS.md). No PC frame figure exists for the one-shot build of 20 Nov.

What the numbers say:
1. The average logic cost is tiny; the spikes are the fault. One tick in 100 costs over 6 ms and one in 1,000 over 20 ms, so at 60 frames a second the player meets a dropped frame about every 2 seconds and a visible hitch about every 17 seconds, before any drawing. The first spike lands on the first tick after New game (40 ms). Cause not yet traced (candidates: path planning, the town's hourly call, garbage collection); finding it is the first item of the one-shot's plumbing hour, with the tool below.
2. The crowd is about at the rescaled band (13 within 120 m against 12 to 20 over 100 m) but thin close up (7 within 26 m). The frame budget below is set for a stress case of 25 or more people on screen (match day reaches about 30, GD-02's placeholder is 25), not for today's 7 near Tom.
3. Software frame times cannot judge feel (premortem way 33); the PC check in section 7 is the only real frame figure.

## 2. Modules and their boundaries

The prototype already has the right bones (src/game/core.js `register({...})`, 29 systems loaded by src/game/systems.js, pure rule pieces). The one-shot keeps them and makes the boundaries rules, not habits.

Layers, each allowed to call only the layers below it:

1. Data (no code): people, places, jobs, lines, scenes, happenings, fares, numbers. Plain files (section 3). Nothing else holds a written line, a price or a place.
2. Rule pieces (src/game/pieces/*.js): pure functions, no clock, no randomness of their own (a seed is handed in), no reading of the screen. Each has JSON cases in test/cases/ (491 passing on 20 Nov). These are the parts that port to Unreal (premortem way 39).
3. The town (wasm one-sim, the game's own C++ held to the C# goldens): who talks to whom, what each person knows, deeds and witnesses, Ellis, the week. Reached only through the bridge (one-sim-bridge.mjs, 35 calls). The prototype's own JavaScript town (routines.js, seeing.js, gossip.js) keeps only what the real town does not yet cover (ONE-SHOT-SIM-DIFFERENCES.md lists it: talk among the other 19 named people, where people stand by hour, how well a witness sees, violence reaching the police, decent acts, regard and names, ask timing, passers-by). Today both rule sets decide who goes to the police; that is the first double owner to remove. Rule: a fact lives in one of the two towns, never both; the bridge file names which.
4. Systems (src/game/<id>.js, one per system): each registers `fresh`, `loaded`, `step(dt)`, `minute(t)`, `hourly`, `daily`, and talks to others only by `emit`/`on` with named events or exported read functions. A system never writes another system's state (`G.x.<other>`); dead_rules.mjs already lists events emitted with no listener and saved fields never read; it counted 217 on 20 Nov (DEAD-RULES-1345.md, "the aim is zero"); the plumbing hour brings it to zero and the build keeps it there.
5. Presentation (src/render/, ui.js, audio.js): reads state, never writes rule state. It may write only its own view state (camera, figures, sound voices). Input goes through one place (player.js and the key handler), which turns keys into intents that systems read.

Boundary rules the one-shot follows from hour one:
- No teleports. Story beats may not set a person's position (CHECK-1 and CHECK-2 found Father Walsh, Ron, the constable, the courier placed by assignment). People move only by walking along the street graph or by entering through a door; a beat that needs someone somewhere schedules them early enough to walk. A guard in core.js logs any position jump over 3 m in one tick for a person on screen as a fault.
- No pinned people. `keep(R,'rank')`-style pins are refused by the guard; a person held for a beat is held by a schedule row with a reason.
- One clock. Game time advances only in clock.js from the fixed step (section 5); the value of a game hour lives once in rules (`RULES.time.realSecondsPerGameHour`), set to 60 by his ruling of 21 Nov (the prototype still has 45; changing it is a one-line change plus re-recording goldens).
- Every random draw takes the run's seed. Same keys, same save, same result (the story rule of ONE-SHOT-PROMPT).
- Faults stay in their system. `guard()` already catches a throwing system and logs it (FAULTS, cap 200). New rule: FAULTS must be empty at the end of every story, and a fault in a step function shows on screen in test builds (the patrol-car chase threw a ReferenceError every frame unseen, CHECK-2).

## 3. Data formats

One folder, src/data/, plain JSON (or JS modules exporting a plain object when comments help). Ids are lower-case words; names are what players read. Every record carries `id`, and a `src` naming the design row it comes from (blueprint or DEFINITIONS id), so the coverage check can trace it.

People (`data/people/<id>.json`, one file a person; extends today's cast.js shape):
- `id, cast_id, called, name, age, sex, role, kind` (principal, firm, regular, minor, rival_man, passer); `cast_id` is the real town's id (hook-cast.json uses its own ids, mapped today by PROTOTYPE_TO_CAST, for example sheila to rocco), `called` how people refer to someone unnamed
- `voice` (voice id for the builder's pipeline), `look` (today's look object), `nerve, venal, talk, discretion` (0 to 1, the prototype's), and the real town's `temperament {nerve, dutiful, willingness}` and `keepsQuiet`
- ties are not kept per person: one list for the whole cast in the real town's form, `[a, b, strength, "place hh:mm days; ..."]` (hook-cast.json), so the wasm town reads it unchanged
- `sched: [[fromHour, where, act, days?]]` (today's schedule rows)
- `lines: {own: [...], greet: [...], close: [...], situations: {<situation>: [...]}}`
- `card: {who, speak, life, fire, rivals, secret}` (live talk's sheet)
- `can_die: bool` (Tom false; killable principals name `fallback_role`)

Places (`data/places.json`): `{id, name, kind (street, room, door, spot, dest), x, z, y?, room?, opens: [[days, from, to]], owner, ways_in: [...], objects: [...]}`. map.js keeps the geometry (NODES, BLD); places.json holds the names and hours, so a written line names a place by id.

Jobs (`data/jobs/<id>.json`): `{id, kind (carry, collection, break_in, lift, tail, minding, fare, sit_down, send), giver, act_min, rung_min, offer: line ids, steps: [{id, at: place, verb, keys: [three ways], fail: next step}], pay: {pocket|tin|book, pence | band}, ledger: line id}`. The three keys to every lock are three entries in `keys`.

Lines (`data/lines/*.json`): every spoken or written line is a record `{id, who (person id or a speaker kind), situation, text, words, once: day|week|game, tokens: [...]}`. The record carries its own cool-down so repeats are judged by data, not by code. Shared street lines are records with `who` a speaker kind (man, woman, older man, older woman, docker, shopkeeper) and a `situation` from a fixed list (the line table, FIT F19). Live talk keeps its prompt in the person's card and falls back to these records.

Scenes and happenings (`data/scenes/<id>.json`): `{id, when: state condition (never a clock time alone), who, where, beats: [{say: line id} | {choose: [...]} | {walk: who, to}], sets: [state flags], once, cool_real_minutes}`. Happenings use the same shape with `kind` and the repeat rules of DEFINITIONS G6.

The town's memory: kept by the real town (seven slots a person, five-rung identification, per-person permanent memory, the canon moat), saved inside the game save as the town's own text (about 17,000 characters, BRIDGE.md). The Ledger keeps only what Tom saw, heard or was told, as records `{t, kind, who, where, source (saw, heard, told, read), text}`.

Numbers: rules.js and game/tune/*.js (2,415 numbers today). Rule kept: no number written outside them (tools/numbers.mjs fails the build).

## 4. Save system

Kept from today (saving.js): one JSON object, a version number (now 4, older refused), localStorage plus the account database in 150,000-character chunks, the newer of the two chosen by its time stamp, an autosave every 75 s.

Changes for the full game:
- Rotating autosaves: three, plus one at each act start, never overwriting the only good save (BLUEPRINT-08 AX-07).
- Version step with a converter, not a refusal, from version 5 on: each version change ships a function from the old shape to the new, with a test that loads every saved story save (story-saves) after the change.
- Save size target under 200,000 characters at week 7 (measured 24,000 to 32,000 on day one; the town alone about 17,000). Checked by the soak run.
- Save and reload must give back the same week (the gate's existing check in machine_checks.py) and the same next 10 minutes of play from the same keys.
- Saves never hold derived state (who is on screen, figure positions); `loaded()` rebuilds it.

## 5. How the simulation and the renderer share state

Today: one mutable object `G`; the logic runs on frame time (dt clamped to 0.05 s), so walking slows when the frame rate falls while the clock does not (ONE-SHOT-LOG, checkpoint 4); the cab steps at 120 a second inside its own loop.

Plan:
- Fixed logic step of 1/60 s (an accumulator: the frame's elapsed time is banked and spent in whole steps), at most 5 steps a frame (beyond that the game slows rather than spirals). The cab keeps its 120 a second inner step. Today Tom's own movement, the fight step and the traffic run on frame time outside the logic loop, and the speed-up (`G.fast`) cuts a fast frame into 4 larger steps; all of these move into the fixed step, and speed-up runs more fixed steps rather than bigger ones. Speeds, timings and chases no longer depend on the frame rate (ONE-SHOT-PROMPT section 40: "walking and every timing independent of the frame rate").
- The renderer reads `G` after the steps and draws, placing each figure between its last two step positions by the leftover fraction (interpolating), so movement stays smooth. It never writes `G`.
- Heavy work leaves the frame: the town's hourly call, path planning for more than 3 people, and gossip passes are spread over frames (a small job queue with a per-frame time allowance of 2 ms), so no single tick goes over budget. This is the fix for the spikes in section 1.
- Headless mode stays: `LEDGER_NORENDER` and `LEDGER_MANUAL` with `LEDGER.step(seconds)` run the same logic without drawing, which is how stories and soaks run fast.

## 6. Performance budgets

At 60 frames a second a frame is 16.7 ms. Set figures (BLUEPRINT-08 8.1.1): 60 frames a second at 3440 by 1440 on his RX 6700, never under 30, in rain and at night; Study 12 gives a median frame of 16.7 ms, worst 25 ms, ceiling 33.3 ms. Those were set for the Unreal game; the browser game takes the same figures. Rows marked "proposed here" have no source and are this plan's proposal:

| Budget | Target | Today |
|---|---|---|
| Frame with 25 or more people on screen, rain, night, 3440 by 1440 | median 16.7 ms, worst 25 ms, never over 33.3 ms (BLUEPRINT-08, Study 12) | 11.5 ms with few people at 2298 by 1252 (18 Nov build); not measured crowded |
| Logic per frame, 99.9th percentile over at least 6,000 ticks | 4 ms (proposed here) | 20.9 ms (cloud, 2 cores) |
| Logic per frame, median | 1 ms (proposed here) | 0.10 ms (cloud) |
| Town step (real town, per game hour, with its work spread) | 2 ms a frame at most (proposed here) | 17 to 22 ms per game day in Node, about 1 ms per game hour on average |
| Draw calls, busiest view | 1,000 (proposed here) | 246 to 819 (cloud, high, few people) |
| Triangles, busiest view | 1.5 million (proposed here) | 199 to 423 thousand |
| Page open to title | 5 s on his PC from the published page (proposed here; BLUEPRINT-08 sets no load time) | 3.2 s from a local folder |
| New game to control | 20 s with the ferry shot (control at 0:20, BLUEPRINT-07), under 2 s after it | 9.3 s with a skip |
| Load a week-7 save to control | 5 s (proposed here) | not measured |
| Memory (JS heap) at week 7 | 1 GB (proposed here) | not measured |
| Save size at week 7 | 200,000 characters (proposed here) | 24,000 to 32,000 on day one |

How 25 or more people fit: figures beyond 26 m (28 m at High) already switch to a lower model (render/sync.js); targets add a third step (a flat card beyond 60 m), one shared skeleton per body type, and crowd figures drawn together in one call each (instancing), so draw calls grow by about 3 a person near and less than 1 far. Each budget is a row the gate reads, and a build fails at the budget itself. Separately, the existing check that fails a build 1.5 times slower than the accepted one (SLOWER_FAILS in machine_checks.py) stays, against a frozen baseline changed only with a reviewer's line (premortem way 32). The gate's present 8 ms logic-step limit (TICK_BUDGET_MS) is replaced by the 4 ms 99.9th percentile row.

## 7. What the first one-shot lost time on, and how this plan prevents it

From ONE-SHOT-LOG.md, the two checks and the premortem:

| Lost to | Evidence | Prevented by |
|---|---|---|
| Rebuilding tools on every fresh cloud run | wasm build about 5 minutes after setup; a full test pass took 572 s under load; art fetched again each run (premortem way 67) | A ready-made start: the wasm, the art and node_modules made the day before and kept on the published page's files; the one-shot's first command checks them by size and hash (build.py --check-assets already does the pictures). On 23 Nov the whole setup took about 8 minutes here. |
| Stories passing on thin systems | 6 of 41 stories in about 7.5 hours; check 1 found "hints real in play, the other seven thin" | Stories judged by screen and sound (section 8), not by game values; no story may change its own check (the one-shot changed S01, S02 and S05 against the prompt's wording to pass); a fresh helper plays three stories every 2 hours, as before. |
| Teleports and pins standing in for behaviour | Walsh, Ron, constable, courier placed by assignment; back.js one hard-coded run | Boundary rules in section 2, enforced by the position-jump guard. |
| Faults unseen | chase code threw every frame | FAULTS empty at each story's end; faults on screen in test builds. |
| Frame-rate-bound movement | walking slows with frame rate | Fixed step (section 5). |
| Old tests breaking on new parts | gate6.mjs written for the old cab | Tests speak to the hook (`window.LEDGER`) by intent, never by setting speed or place each frame. Today `goTo` puts Tom at a place at once (hook.js, test only); a `walkTo` that walks him along the street graph is added for stories, and `goTo` stays only for setting up a test. |
| Prompt too big to hold | 170 KB prompt (premortem way 8) | Details by file: the prompt names the blueprint chapters and this plan; data lives in src/data, not in the prompt. A fresh session answering 20 random rules must get 18 (the premortem's own guard). |
| Two game rule sets joined at 9 people | ONE-SHOT-SIM-DIFFERENCES.md | One owner per fact (section 2, layer 3). |
| Three browsers at once crashing | CHECK-1 | Test runner holds two pages at most; the work lock in build.py stays. |
| Feel tuned at a third of real speed | premortem way 33 | Timings are tested on the stepped clock (exact), and feel is checked once per loop on his PC by the advisor's normal route; the one-shot never tunes feel from cloud frame times. |

Throughput this plan needs: about 45 Fable-builder hours in the week (premortem way 7; way 11 adds that another project shares the account). The first one-shot built its systems first (about 10:13 to 13:37) and then took 25 to 57 minutes a story (S01 to S06: 51, 25, 43, 35, 57, 52, about 44 on average); counting the checks and the cab work, its overall pace was about 75 minutes a story. 41 stories at 44 minutes is about 30 hours; at 75 minutes about 51, more than the week. The week fits only near the faster pace, with the systems and plumbing ready on day one; hence the ready-made start and the data folder (INVENTORY.md section 1 does the full sum).

## 8. The hidden-check harness's hooks

The hidden and staging checks are planned, not built (premortem way 29). What the game must expose so a check the builder never sees can judge it:

- `window.LEDGER` stays the only test door (hook.js today: read, person, goTo, prompts, press, talk, written, job, fare, cab, ledger, measures, saveText, restore, step, tick, benchmark, and `LEDGER.game.<id>`). The hidden checks use only what a player meets plus these reads; they never call into a system directly and never read `LEDGER.G`, the raw state the hook also hands out (CHECK-1 named reading it as a thin spot).
- Screen reads: `LEDGER.screen()` returns what is on screen in words: subtitles and their speaker, prompts, panel text, the Ledger page open, and the list of people drawn with their screen position and whether their head faces the camera (from the rendered skeleton, not from `mind.look`, premortem way 31). A black frame test: the share of near-black pixels in a 64 by 36 read-back, so a camera inside a wall fails.
- Sound reads: `LEDGER.mix()` returns the sounds playing now by name with their loudness at the listener. The `MIX` log in audio.js records today only how loud a sound was asked for, and only for effects and voices; it is extended to every loop and timed sound and to the level where Tom stands (SOUND-PLAN step 1).
- Determinism: `launch({seed})` with the stepped clock (test/harness.mjs `VIRTUAL`) and the rule that two runs from the same save with the same keys give the same record.
- Saves as handovers: every story ends by leaving a named save; hidden checks start from those saves.
- Faults and dead rules: `LEDGER.game` FAULTS list empty; `dead_rules.mjs` at zero.
- Budgets: `LEDGER.perf()` returns the logic step's median, 99th, 99.9th percentile and worst over the last 6,000 ticks or more, and the frame's, so the harness can fail a budget without a separate tool. On his PC the frame figure comes from PresentMon through tools/lane/frametime_summary.py; allowlist item 12 names the study games, so using it on LEDGER's own build needs that line widened first (a licence line, routed the usual way, not by this session).
- Data checks: every line, scene and job record has a `src`; a check counts records against INVENTORY.md and lists missing ones.

## 9. First hour of the one-shot (plumbing, done before any story)

1. Check the ready-made start (wasm, art, node_modules) by hash; build.
2. Switch to the fixed step and the job queue; re-run the tick timing (6,000 ticks or more) until the 99.9th percentile is under 4 ms; bring dead_rules to zero.
3. Set the clock to 60 s a game hour; re-record the goldens (same_week).
4. Add the position-jump guard, faults-on-screen, `LEDGER.screen()`, `LEDGER.mix()`, `LEDGER.perf()`.
5. Move lines, places and fares into src/data with `src` fields (today's 650 to 800 written strings and 14 fares carry over).

Each step has its test; nothing in this list needs Jafar.
