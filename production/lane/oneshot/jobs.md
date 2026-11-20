# One-shot builder "jobs": jobs done with the hands

Systems jobsx (the job template and the job list) and crime (the verbs). Stopped at 09:45 Swiss time on the budget rule: the main row of 09:31 read 72% against the one-shot's ceiling of 72.0% at that minute. Everything is committed and pushed (branch oneshot-jobs).

## Where it stands

- Rule pieces, under Node: job_template 31 of 31 cases, crime_rules 104 of 104 (node test/pieces.mjs). The expected values were written from the design, not from the code.
- In the game, test/game/jobsx.mjs: its first six checks pass (the six laws as data over all 11 jobs; every family and every channel of A17 used; three keys each; lines of about 22 words; all 67 routes through the 11 jobs reach their end with a Ledger line a step and no system fault). The other eleven checks (Ron's offer taken in talk, the wait at a window, the carry's three routes, settling by the clock, variety, the arrangement, purses, save and load) are written and have NOT yet run to the end: the test browser was killed for memory four times while nine builders tested at once.
- test/game/crime.mjs is not written. The verbs in crime.js have been built and compile into the game, and have not been played once. Treat every crime verb as untested in the game.
- The existing tests that touch src/jobs.js (week, town, nights, watch2) were not rerun; src/jobs.js itself is unchanged.

## Part by part

- 3.5.6 Job template and step states: built; pieces job_template passes; in game the first six checks of game/jobsx pass.
- 3.5.7 How jobs reach him: built shallow; channels counter, street, message, phone and car are in the data and checked (ER-REACH-01); the message lines themselves not yet seen in play.
- 3.5.1 Carries: built shallow (the Friday envelope, the Sunday holdall, three routes each in the data); the route test is written, not yet run.
- 3.5.2 Collections, 1.6.4 Fronting up: built shallow (Harrison's thirty and Iveson's eighty as jobs; outcomes reached by script); fronting up itself is the existing ladder.
- 2.8.1 The five debtors: built shallow as talk decisions (Darren pays in what he hears, Wayne in goods off Rita's shelf, Julie works it off, Iveson leaned on with the receipt, Lee stands as before); untested in play.
- 2.8.2 Partial payment and the book: built; rule passes its golden rows (debtPays, debtInKind); in the game it replaces the story's collection through G.hooks.yielded; that check is written, not yet run.
- 1.6.1 Getting in, 3.5.3 Break-in sites: built shallow (Iveson's cabin, Rita's back room, unit 2 on the warehouse row; key, back way from the owner's routine, or force); rule passes; untested in play. No interiors: Tom stays at the door and what is inside is within reach of it.
- 1.6.2 Searching and taking, 1.6.12 the torch in searches: built shallow; rule passes (table times, twice as long in the dark without G.tom.torchOn); untested in play.
- 1.6.3 Lifts and the hot mark: built shallow; rule passes; the mark is used only by the fence's price so far.
- 2.7.6 Fencing with A30's haggle: built shallow; rule passes (0.4 of an honest price, three offers at most, only prices spoken); the scene untested.
- 1.6.13 Lifting from a pocket: built shallow (Iveson, Wayne, Dent, Metcalfe each carry one thing); rule passes; untested in play.
- 1.6.14 Damage by hand: built shallow (six things; the kind is town 'deed'); rule passes; untested in play.
- 1.1.6 Tailing on foot, 3.5.4 Tails, minding and lifts content: built shallow (two tails, one minding, one lift job); rule passes (ER-TAIL-01, 02); untested in play. The target "arriving" is judged by his standing still in sight for four seconds, which is thin.
- 1.6.5 Minding: built shallow (recorded as the act stood_with); untested in play.
- 1.6.11 Casing: built shallow; hours are read from the owner's own week (ER-CASE-01 as a golden row); untested in play.
- 1.6.7 Getting rid of things: built shallow (the water, the sink with nobody looking, the Washeteria remembers); blood is a flag here (G.x.crime.blood) that no watcher reads yet.
- 1.6.9 Coat, pockets and storage: built shallow; rule passes (ER-POCKET-01); G.x.crime.carried is kept current for searches; the drawer and the shed are in the save, the save test not run.
- 1.6.6 Getting ready: built shallow (the locked drawer's menu at the office only; which car and who comes are not in it).
- 4.11.1 Yard dogs: built shallow (one dog, at the scrapyard gate; scraps from the chip shop; no verb harms it, as a golden row); untested in play.
- 2.9.1 The asks: built shallow (nights five and seven as template jobs; nights one and three stay the story's own).
- 2.9.2 Keeping or ending the arrangement: built shallow (G.x.jobsx.arrangement: 'kept', 'ended' or null; event 'jobs:arrangement').
- 7.14 Variety: built; rule passes (ER-JOB-06); offers are held back inside thirty minutes; the in-game check is written, not yet run.

## Known faults

- Nothing in crime.js has been walked in the game; expect first-run faults at the door positions (they were set from the map's numbers, not tried on foot), in the scenes that use choices, and in the tail's ending.
- Ian Megginson is not in the prototype's cast: the ironmonger at his counter cuts the keys in his place.
- A job's first line sets the story's to-do (G.story.objective), which the spine may overwrite and the other way round.
- The owner's two warnings inside a place are subtitles, not yet the ground rules of part 2.2.6.

## Needs from others

- test/harness.mjs (the manager's port line): its comment swallowed the rest of the line, so no browser test started. Fixed on this branch in one line; other builders will have fixed it too, so expect a small merge clash there.
- Law: a constable's search should read G.x.crime.carried and send emit('police:searched', { took: [things] }); the jobs then end as "taken" and the things leave his pockets.
- Foot: G.tom.torchOn is read by searches; blood (G.x.crime.blood, coatBlood) wants to be a give-away in seeing.
- Spine: scenes.js collect() should use the purse rule (pieces/crime_rules debtPays) instead of being wrapped through G.hooks.yielded; the Ledger's Open list could show carried words (crime_rules carriedWords) and live jobs (G.x.jobsx.runs).
- Rise: 'jobs:recruit' { who: 'julie', road: 'need', use: 'drive' } is sent when Julie is let work off her debt.
- Next run: finish running test/game/jobsx.mjs alone on a quiet machine, write test/game/crime.mjs (its plan: each site entered three ways, table search times with and without the torch, pocket limits, a lift felt and not felt with the head turn first, damage known by morning, three offers at most, a tail never ending on distance, casing lines against the routines, the dog, storage across save and load), then rerun week, town, nights and watch2.
