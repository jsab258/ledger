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

## Checkpoints

- 09:10 Checkpoint 0. Read in; one-sim rebuilt here from nothing and passes everything (58 lines ok); the prototype builds; the core and the empty systems are wired in and the seeded week is unchanged except for the new saved part. Done: nothing on the checklist yet. Next: the bridge (4a) and all four stages in parallel. Broken: test same_week reports the new saved part "x" as different from round 5's record (expected; a new record is written when the build settles).
