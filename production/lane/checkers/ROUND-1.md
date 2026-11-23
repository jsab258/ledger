# Round 1: the checkers as they stand, on 17 planted faults

23 Nov 2026, 13:29 to 17:20 Swiss time. Planted file: planted-r1.json (kept outside the repository until scored). Builds: one per fault, and three with five or six faults each (G1, G2, G3) for the slower checkers. The checkers were given only the built page. Raw results: runs/.

How a catch was judged: a failure on the planted build that the clean build did not have, whose evidence points at the planted fault (read by this session from the evidence, the checkers never saw the planted file). Pre-existing faults the checkers found are not catches; they are listed apart.

What ran: the six play stories that exist (S01 to S06) as in-game tests on the clean build (twice) and G1 to G3; the machine checks on the clean build and G1 to G3; the clumsy run on the clean build, G2 and G3; the consequence checker in its own run on the clean build, G1 and G2 and over two played sessions on G1; five AI sessions (story player and explorer, Opus; clumsy player, money cheat and talk spammer, Sonnet), 6 to 20 minutes each, on G1, G2 or G3.

## Per fault

| # | Fault (kind) | Caught by | Missed by, and why |
|---|---|---|---|
| 1 | second-fare-unpaid (passes on the scripted path) | nobody | stories play one fare; machine checks drive no fares; money cheat never found a cab |
| 2 | passer-by-fare-unpaid (a fare that never pays) | nobody | as above |
| 3 | yard-dead-end (soft lock at night) | stories (S05 dark branch: cannot leave the yard, hand-over never reached) | machine "never stuck" visits named places by day only |
| 4 | lines-repeat (people repeat one line) | nobody | stories check no repeats; consequence checker's own run hears 11 to 15 lines; its run over a played session flagged only a pre-existing repeat; AI players did not name it |
| 5 | witness-forgets-on-load | machine (save and reload give back the same week) | stories: S06 passed from the loaded save |
| 6 | cab-sticks-after-post | clumsy (indirect: later crashes "not reached"); stories S02 probable (the stop beside the parked car failed) | |
| 7 | pause-menu-swallows-keys | clumsy (pause and resume by Escape; back to play after key spam); AI clumsy player at minute 1.4; stories (S01 on G2: "the AI notice never shows again", found by the fresh review) | the AI clumsy player was then trapped and tested nothing else |
| 8 | empty-night-street | nobody | no checker counts people; the explorer wrote only "a dark side street with nothing in it" |
| 9 | debts-not-saved | nobody | the machine compares a save with a re-save, both without the debt book; its idle day changes no debt |
| 10 | heads-turn-in-data-only (a check that tests the wrong thing) | nobody | S01 reads the mind's look value, not the drawn head |
| 11 | hints-nag (a control: a story line aims at it) | stories (S01) | |
| 12 | drink-line (content) | nobody | the machine's content scan refused the build ("source does not match", 34 of 40) and never ran, on the clean build too |
| 13 | teen-in-crowd (no children) | nobody | the machine reads P.age or P.def.ageYears; the game keeps P.def.age, so no crowd age was ever read |
| 14 | slow-step (frame rate) | machine (logic step 0.82 ms against 0.15 on the clean build) | the rule also fails on the clean build against its stored baseline, so only the size of the jump tells |
| 15 | ada-talk-no-leave (soft lock in talk) | nobody | "no box that cannot be closed" only sees boxes the idle run opens; no talk with Ada happened |
| 16 | count-doubles-money | stories (S06: the flows ledger does not balance, every branch) | |
| 17 | bollard-not-solid | nobody | clumsy reads the props from the repository's source, not the build's, and passes Tom at 0.33 m (0.64 on the clean build) |

Caught: 7 of 17 (41%). By checker: stories 4 (5 with S02's probable; the pause menu's S01 line added after the fresh review); machine 2; clumsy 2; consequence checker 0; AI players 1 (the Sonnet clumsy player); Opus player types 0.

## False alarms and noise on the clean build

- Stories: S05's "runs" branch fails on the clean build both times (12 lines) and S06's "runs" with it; the branch head no longer holds what the log of 20 Nov says passed. Two browsers at once crashed the page in S01 twice; a passer-by blocked the story driver for 171 s in one run. On G1 S05 passed where the clean build failed: the stories are the same twice on one build, but any change to the code moves the chain.
- Machine: on the clean build the content scan is "not reached", the frame rate fails against its stored baseline (0.15 against 0.09 ms), and the camera fails at four named places. A gate on these would never pass.
- Clumsy: seven failing lines on the clean build (keyboard steering eased three times, cab stuck after a hit, two crashes not reached, a pause nothing holds); "everyone knocked down is told" failed on G2 and G3 and not on the clean build (noise).
- Consequence checker: none, and next to nothing reached in its own run.
- AI players: no false alarms that replay showed wrong, but most of their 40 or so faults are real faults of the current build (the T box ignores Escape, "Morning" at dusk, the camera flips overhead, shop fronts that look open, the talk box keeps the E key), which is useful and is not a catch.

## Mended for round 2 (once)

- tools/lane/checkers/machine_plus.py: content in the built ledger.js itself; ages as the game keeps them; the crowd counted every hour against the game's own table; six fares in a row; every talk (street and windows) left by Escape; the pause menu by keys; frame rate against a twin build measured in the same run.
- tools/lane/checkers/overlay/test/stories/play.mjs: two watchers at the end of every story: a save and reload give back the same game (debts, Ledger, money, flags, memories, as the game holds them), and no line of five words or more said twice.
- BREAKER-MENDS.md: coverage duties for every breaker and the clumsy player (do paying things twice, five people, every door both ways, past midnight, save and Continue), a new second-time tester card, a line for the player types.
- The harness: run checks one at a time, twice, and off the scripted path (HIDDEN-CHECKS-SPEC.md).
