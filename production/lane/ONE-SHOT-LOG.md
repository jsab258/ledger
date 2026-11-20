# The one-shot's log

The one-shot of Friday 20 November 2026 (his decisions of 19 Nov 20:05 and 20:52): the whole design built into the browser prototype in one long session, against production/lane/parts-tree/ONESHOT-CHECKLIST.md. Kept current at each checkpoint so the next cloud lane run can continue exactly here. Started 08:47 Swiss time on Fable 5.2.

## How it is built (read this before continuing)

- The whole game sits on the round 6 prototype as systems, one file each, under tools/lane/prototype/project/src/game/. core.js says what a system may give (state, steps by the minute, hour and day, prompts, scenes, talk decisions, keys, test calls). Each system's saved state is G.x.<id>; a save from before the one-shot gets fresh ones and still loads.
- Each system has its numbers in game/tune/<id>.js (merged into the one tuning table as RULES.game.<id>), its kinds of act in game/kinds/<id>.js, its people in game/cast/<id>.js.
- Rules that Unreal will port are pure pieces in game/pieces/<name>.js, each with its cases in test/cases/<name>.json, run by `node test/pieces.mjs` (no browser). production/lane/ONE-SHOT-PORTING.md lists them.
- In-game tests of a system are test/game/<id>.mjs (the prototype's own harness).
- `python tools/lane/prototype/oneshot_dev.py --work DIR test NAME...` builds and runs chosen tests without pinning.
- The systems and who built them: town (the bridge to the real town code); feel, foot, fightx (moving, hiding, manners, fight defence, camera and screen faults); cars, fares; jobsx, crime (jobs with the hands); life, shops, way (the town's days, spending, finding the way); law (police); acts, endings, ledgerx (the story's spine and the Ledger); crew, rivals, rise, firm, dial (the rise); econ (money, debts and the pieces' glue).
- Keys newly given: Z walk slowly (held), M street manners, B sit, lean or smoke, N the watch, O throw a stone or rattle a bin, I the torch, H the horn (at the wheel), B look back (at the wheel, held), digits 1 to 9 crew orders, semicolon (held) a weapon out.

## The second run (20 Nov, from 10:13): one builder, read this first

- The first run saved only checkpoint 0. The second run built everything below, one part after another, and pushed after each.
- The bridge is in: src/game/town.js runs the game's real town code inside the page. build.py copies the loader, the bridge, the cast file and the built one-sim.wasm into the work folder's src/game/sim/ at build time (never into the repository). It needs the built town code at /home/claude/one-sim-work/wasm/one-sim.wasm: run tools/lane/one-sim/one-sim.sh setup, then wasm (about 5 minutes), or set LEDGER_ONE_SIM_WASM. What changed for the player: production/lane/ONE-SHOT-SIM-DIFFERENCES.md.
- Rules live in pieces (src/game/pieces/, 12 files, 491 cases in test/cases/, `node test/pieces.mjs`). production/lane/ONE-SHOT-PORTING.md lists them. A system holds wiring only.
- Systems written (all 21 have content now): town, feel, foot, fightx, cars, fares, jobsx, crime, life, shops, way, law, acts, endings, ledgerx, crew, rivals, rise, firm, dial, econ.
- In-game tests: test/game/lib.mjs is the shared start; town, foot, crime, work and rise each pass alone (`python oneshot_dev.py test game/NAME`). A written scene pauses the game: a test answers it (see `clear` and `answer` in work.mjs and rise.mjs) before stepping on.
- Systems talk through core.js on() and emit(): 'act' (every act), 'town.hour', 'crime.entered', 'crime.found', 'crime.damage', 'crime.holdup', 'foot.tail', 'foot.chase', 'fare.pickup', 'fare.done', 'cars.hit', 'cars.crash', 'cars.reckless', 'law.arrested', 'rivals.climbed', 'rivals.sitdown', 'act.end', 'acts.inspected', 'endings.done', 'fight.beaten', 'econ.week', 'jobs.ended'.
- Hooks added to the older files (search for "the one-shot" or "game/"): seeing.js (sighted, seen, target), events.js (acted), gossip.js (townPair), police.js (townEllis, custody), saving.js (beforeSave), money.js (flow), fares.js (fareNext, fareDrop, fare.pickup, fare.done), drive.js (cars.hit, cars.crash), routines.js (crowd), scenes.js (act1End; Sheila asks on Sunday), player.js (camera bands, the turn, slow walk, look back), ui.js (panels by keyboard, stuck subtitles, prompts clear of subtitles), work.js (fight.beaten).
- New keys in play: N the watch, M street manners, B sit or lean or smoke, O a stone, I the torch, Z held while moving walks slowly, Comma the paper map, Full stop how things stand, digits 1 to 7 crew orders; at the wheel H the horn, B held looks back, R has Pauline say the way again. In a panel: up, down, Enter.
- New people appear in written scenes by name only, with no body in the street yet: Keith Garbutt, the three rivals, the inspector, the trainer, the man at the lot, PC Harker, Ian Megginson.

## Checkpoints

- 08:56 Checkpoint 0. Read in; one-sim rebuilt here from nothing and passes everything (58 lines ok); the prototype builds; the core and the empty systems are wired in and the seeded week is unchanged except for the new saved part. Done: nothing on the checklist yet. Next: the bridge (4a) and all four stages in parallel. Broken: test same_week reports the new saved part "x" as different from round 5's record (expected; a new record is written when the build settles).
- 10:34 Checkpoint 1 (second run). The bridge in and tested; hold-ups designed (A41); twelve rule pieces, 491 cases. No part finished in play yet. Weekly 82% at 10:08 (no newer reading).
- 11:10 Checkpoint 2 (second run). Every system has content and an in-game test that passes: town, foot, crime, work, rise. The whole arc runs in a test from Act I's answer through the rise, the inspection and an ending to control again. Faults of 20 Nov mended: both cameras and the cab's view in their bands, the instant reverse, panels by keyboard, door prompts, Darren's line, stuck subtitles, prompts over subtitles. Next: the older tests re-run against the new town and their records re-made, the first hour's restaging (arrival by ferry is not done: he still gets off the bus), the gate. Broken or thin: see ONE-SHOT-REPORT.md when written. Weekly 82% at 10:08 (no newer main row).
