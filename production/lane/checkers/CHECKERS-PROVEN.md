# Checkers proven

23 Nov 2026, the checkers session (Opus 5.5): the one-shot's checkers run blind on planted faults, mended once, run again. Detail below, ROUND-1.md and runs/.

## In plain words

Before the mend the checkers caught 7 of 17 planted faults (41%). Mended, they caught 11 of those 17 (65%). On 14 fresh faults planted after the mend they caught 4 (29%); fixes that round 2 showed the mends needed, made afterwards and not counted, bring that to 6 of 14. They probed what the mend did not aim at: plan by 29%.

Per checker, round 1 then round 2: stories 3 of 17, 3 of 14; new machine checks 6 of 17, 1 of 14 (3 fixed); gate machine checks 2, 0; clumsy run 2 of 11, 1 of 9; new watchers 1, 0 (1 fixed); consequence checker 0 of 12; AI players 1 of 17, 1 of 14.

What still slips through: faults off the path a story plays (a fare paid only when stopped exactly, a stair with no prompt at night, news that goes cold while the scripted chain still tells it); anything judged by what the game records rather than what a person sees or hears (heads turning only in the game's mind, silent voices, a death booked at the hospital); repeated lines; a talk nobody reaches that cannot be left; things drawn half solid; a camera fault in a room no check visits.

The go or no-go threshold is sound only on three conditions. A check counts as working only when it passes twice and off the scripted path too (hidden.py enforces this). What already fails on today's build is listed first (S05's chase branch, six machine lines, seven clumsy lines), so only new work counts. And since stories caught under a third of the fresh faults, a go also needs no new blocker from the machine checks, the watchers and the AI players.

The giant prompt must carry: every menu, the title screen and every box worked by keys alone (today's title screen takes none and ended two AI sessions); the test hook kept by name; sounds recorded only when they really play, and the drawn head's turn readable; a warning that hidden twins replay each story a second time, by another route, after Save and Continue, and at night; and the faults the AI players found today (listed below).

## Catch rates

| Checker | Round 1, before the mend | Round 1's faults, mended checkers | Round 2, fresh faults | Round 2 with the later fixes |
|---|---|---|---|---|
| Play stories (S01 to S06 as in-game tests) | 3 of 17 | 3 of 17 | 3 of 14 | 3 of 14 |
| Story watchers (new) | none | 1 of 17 | 0 of 14 | 1 of 14 |
| Machine checks, the gate's (unchanged) | 2 of 17 | 2 of 17 | 0 of 14 | 0 of 14 |
| Machine checks, mended (machine_plus, new) | none | 6 of 17 (7 with one probable) | 1 of 14 | 3 of 14 |
| Clumsy run | 2 of 11 | 2 of 11 (not re-run) | 1 of 9 | 1 of 9 |
| Consequence checker | 0 of 12 | not re-run | not run | |
| AI players and breakers | 1 of 17 (5 sessions) | not re-run | 1 of 14 (3 sessions) | |
| Any checker | 7 of 17 (41%) | 11 of 17 (65%) | 4 of 14 (29%) | 6 of 14 (43%) |

"Of N" counts the faults on the builds that checker ran on. Grouped builds were used for the slower checkers; four faults that a group's other fault may have hidden were run again alone (none was caught alone).

## Round 2, per fault

| Fault (kind) | Caught by | Missed by, and why |
|---|---|---|
| drop-off-needs-exact-stop (passes on the scripted path) | nobody | the story driver and the fare calls both stop on the spot; no AI player reached a fare |
| news-goes-cold (a witness who forgets) | nobody, also alone | the first week's news chain is scripted and still told it |
| long-lines-not-kept (a person repeats) | nobody | the watcher looks inside one story; repeats need an evening |
| flat-stair-night (soft lock) | nobody, also alone | no story goes up the stair at night; the machine visits named places by day |
| handbrake-sticks (a car that sticks) | stories (S02), clumsy (cab stuck after every crash) | |
| talk-box-keeps-keys (keys swallowed) | not shown, also alone; the story player's "holding S left him in the same place" after a talk may be it | the talk check closes the box but never walks afterwards |
| rain-empties-streets (an empty street) | machine_plus (the crowd counted each hour) | |
| ledger-not-saved (a save loses a step) | stories (S03 Day book, S04 Ron unnamed, S06 People) | the watcher, by a flaw in the mend (fixed after: caught alone) |
| voices-silent (tests the wrong thing) | nobody | every check reads the sound record |
| text-me-line (1990) | nobody (the fixed scan catches it) | no 1990 word list read the built game |
| kids-line (no children) | nobody (the fixed scan catches it) | the mended scan paired quotes wrongly in the minified build |
| run-down-kills (a car never kills) | nobody, also alone | clumsy checks the moment of the hit; the death is booked at the hospital |
| long-subtitles-stick | stories (S01 layout), AI story player | |
| flat-camera-in-wall | nobody | no check puts the camera in the flat |

Round 1's faults with the mended checkers: newly caught drink-line and teen-in-crowd (content and ages as the game keeps them), passer-by-fare-unpaid (six fares in a row, all unpaid; second-fare-unpaid probable on the same evidence), empty-night-street (the crowd by hour), witness-forgets-on-load (the watcher). Still missed: lines-repeat, heads-turn-in-data-only, ada-talk-no-leave (the talk check never opened Ada; it now names whom it could not open), bollard-not-solid, debts-not-saved (caught alone after the watcher fix).

## False alarms

- Stories on the clean build: S05's chase branch fails both times (12 lines) and S06's with it. Two browsers at once crashed pages twice; a passer-by blocked the story driver once under load. The same build gives the same result twice, but any code change can move a branch either way (G1 and one single passed S05 where the clean build failed).
- The gate's machine checks fail six lines on the clean build (content "not reached", frame rate against a stored baseline, four camera places). The clumsy run fails seven; "everyone knocked down is told" came and went between builds.
- machine_plus: the crowd check at half the table failed three builds on wet days (rain thins the crowd by design); at a quarter, after the fix, only the planted empty streets fail.
- AI players: no claim found false, but nearly all their faults are real faults of today's build, not planted ones.

## Faults the AI players found in today's build (for the giant prompt)

The title screen takes no keys after Save and quit (two sessions ended there); the pause menu's highlight and focus differ, and Down counts land on the wrong item; the T choice box and the opening choice box ignore Escape; the key that opens a talk is typed into its box; "Morning" at dusk and day to night in three minutes of play; the camera flips overhead or into walls near cars and walls; subtitles stack the same line twice; the Ledger shows "Source: event 3" and names a person twice in one note; Ron answers a "No" with nothing; shop fronts, the doctor's and the solicitor's look open and are not; the yard and the dock are black at night with Tom invisible; one character under two names.

## Can each playthrough check pass while what it proves is broken?

Yes for every one of the 41 as written, in at least one way; the column says the likeliest way and what the hidden twin adds. S01 to S06 are judged from their tests and this proof; S07 to S41 are not written yet and are judged from their prose in ONE-SHOT-PROMPT.md. "Record" means a value the game keeps, not something drawn or heard.

| Story | The likeliest way it passes while broken | The hidden twin adds |
|---|---|---|
| S01 Off the ferry | heads read from the mind's look value and voices from the sound record (planted: both passed) | the drawn head's turn; sound actually playing; a talk with every person met, left by Escape |
| S02 The first fare | one fare, one route, a driver that stops on the spot (planted: unpaid later fares and a 2 m drop-off passed) | a second and third fare; a stop a car length off; a passer-by's fare |
| S03 The debt book | the book read in the same session it was changed (planted: a save without the debt book passed) | save, quit, Continue, then the book and Money read again |
| S04 The first ask | Ron's ask staged at a fixed hour and place | the ask met at another hour, after a reload, after walking away and back |
| S05 The carry | branches fixed to one route each; the chase branch already fails on today's build | each branch by another route; the constable's beat watched from elsewhere |
| S06 It comes back | the news chain is one scripted road (planted: news going cold in 40 minutes passed every story) | the same night told by other witnesses; the count done twice; the morning after a reload |
| S07 The day shift | wrinkles drawn from a seeded list, checked once each | a whole day of fares: no wrinkle twice running, every fare paid |
| S08 Lee stands | timings from the game's own fight record | timings from the drawn body; the fight from another side |
| S09 An evening that holds | crowd numbers read from the game's list | people counted on the street every hour, in rain and dry (the mended crowd check) |
| S10 The witness's walk | her walk read from her plan, not seen | the walk seen from Tom's place; the call made late |
| S11 Statement and arrest | the arrest staged at the named hours | the same deed on another day; a reload between statement and arrest |
| S12 Break-ins | noise reach read from the rule | the sound heard at that distance in the mix that plays |
| S13 An unseen deed | the finder fixed by name | the routine moved a day; a reload before the finding |
| S14 Lifts and the fence | the fence's memory read from her mind | her next-day line on screen, after a reload |
| S15 Tails | looks back read from a timer | the drawn head turning; a tail lost and found by the Ledger |
| S16 Fists and the street | breakage counts from records | the drawn break; a second fight in the same place |
| S17 Beaten and mended | marks read from flags | the mark seen at 20 m by a watcher, after a reload |
| S18 Moving and hiding | reaches read from the rule (the sound record again) | the footstep heard at the reach; the shape caught as drawn |
| S19 A taken car and a chase | the chase on one road | the chase on another road; the car that sticks after a knock (planted: passed the stories) |
| S20 A car hurts, never kills | a hit staged at one speed | hits at several speeds, nobody dead after any (planted: a death booked at the hospital passed the clumsy run) |
| S21 Two lives on one night | both nights scripted in one order | the other order; a reload between |
| S22 Calling on people | a call offered at the one hour tested | calls outside the hours (no prompt); a talk that can be left |
| S23 The week's end | a week of waiting with the wait key | a week played with fares and talk; the street at night counted |
| S24 to S36 (Ellis, the rise, the end) | long chains that can only be reached by staged saves | each reached from a played save made by a twin; endings after a reload |
| S37 Tom never dies | checked on the story's route | the long machine run and every breaker session |
| S38 No meter or marker | checked on the screens the story sees | every screen the AI players saw |
| S39 No child anywhere | checked on people the story met | every person's age as the game keeps it, and every line the built game holds |
| S40 No alcohol or gambling | checked on lines the story heard | every line the built game holds (the mended content scan) |
| S41 Never five minutes with nothing new | checked on the story's straight way | the AI players' patience logs over 20 minutes |
