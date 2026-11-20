# Rules for Unreal to port, and where their tests are

The one-shot, 20 November 2026. Money, debts, jobs, fights and talk are not in the game's town code. Each is written here as a separate piece: pure functions (plain data in, plain data out, no clock, no random number but a seed handed in), with its test cases as data. Unreal ports a piece and must pass the same cases. The other rules the design adds are written the same way, so nothing in the browser's play code holds a rule of its own.

All paths are under tools/lane/prototype/project/.

| Piece | File | Cases | What it holds |
|---|---|---|---|
| money | src/game/pieces/money.js | test/cases/money.json (21) | Every pound as a flow between three pots, so no money comes from nowhere; what the fare book can hide; the wash and Sheila's warning; a fare's price; the week's costs; the firm's own fares; the rent's state; money in words. |
| debts | src/game/pieces/debts.js | test/cases/debts.json (17) | A debtor pays what his purse holds and the rest stays on the book; what each of the five does by how he is approached; what squeezing and letting go do to regard. |
| jobs | src/game/pieces/jobs.js | test/cases/jobs.json (20) | The job template: four job states and five step states; a spec's faults by the six laws; windows not minutes; failure that continues; no set piece twice in thirty minutes; minding. |
| fights | src/game/pieces/fights.js | test/cases/fights.json (52) | The eight rungs; the odds; the other man's nerve; guard, slip and counter; breath; the fall rule (fists never kill, a car never kills, water never kills); the five endings; things that break; a weapon only on a held input; fighter types; a simulated fight for the skill-beats-mashing and no-death checks. |
| talk | src/game/pieces/talk.js | test/cases/talk.json (38) | Only a plain yes is taken; what cannot be undone asks twice; a reply's timing; the claim check; lines not said twice; greetings by regard; haggling in three offers; calling on people; the friendship; a whole talk by pad. |
| eyes | src/game/pieces/eyes.js | test/cases/eyes.json (87) | What a watcher catches by distance, light and what he does (hiding, a turned back, a crowd, a torch, a new coat, marks); how far a noise carries; the horn; a thrown stone; manners; tails; chases; vaulting; searching; a hand in a pocket; finding an unseen deed; taking a parked car; trespass; casing. The canonical perception stays the town code's; this piece holds what the design adds and the front door does not yet offer. |
| law | src/game/pieces/law.js | test/cases/law.json (51) | When an arrest may land; what it costs in hours; DS Ellis's four stages and their signs; the challenge and its three answers; traffic stops; bought men; the office searched with notice; a street on edge; police after a deed; a car hit and the choice after it; the ambulance. |
| crew | src/game/pieces/crew.js | test/cases/crew.json (28) | Orders; the eight sent verbs; the two roads of recruiting; strain and the sign before a man breaks; the cut; a man at his side; what crew never do untold; fates. |
| rivals | src/game/pieces/rivals.js | test/cases/rivals.json (24) | A rival learns only through its own people; one rung at a time, each shown first; the three pressures and three answers; the Fixer; the sit-down. |
| rise | src/game/pieces/rise.js | test/cases/rise.json (53) | The four rungs from holdings; the name each person uses; doors that open on soft keys; the dial; a gun only through a person; the firm's board, ranks and accounts; the other firm; fronts; hold-ups. |
| story | src/game/pieces/story.js | test/cases/story.json (43) | Which act it is; Act II's beats on states; a dead week; the inspection's mornings and its result; the ending as a state (three shown, five built); Tom's reading from signs; when an ending may land; after the ending; week one's shape. |
| life | src/game/pieces/life.js | test/cases/life.json (57) | The calendar from 15 October 1990; who is out by hour, weather and day; cooling by kind; the paper; a shop's list, hours and purse; selling and the hot mark; getting rid of things; the nudge when lost; asking the way; the time; a skipped ride; paint; crash stages; street happenings by state; play time by activity. |

Run them: `node test/pieces.mjs` (no browser, under a second). 491 cases, all passing on 20 November.

How the pieces read their numbers: each imports its system's file under src/game/tune/ (plain data, imports nothing), which is merged into the one tuning table as RULES.game.<system>. Unreal reads the same table. A case's expected output therefore holds under the committed table; a tuned number may change a case, and the case is then changed on purpose, with its rule id.

How the game uses them: each system under src/game/ calls its piece and keeps only the wiring (state in the save, prompts, scenes, Ledger lines). The in-game tests are test/game/*.mjs (town, foot, crime, work, rise), run in the page through the game's own hook.

Not pieces, on purpose: the feel of a blow, of walking and of the car (frames, camera, sound); these are measured by the feel drills (tools/lane/gate/feel_numbers.py), and are the builder's to match in Unreal, not to port.
