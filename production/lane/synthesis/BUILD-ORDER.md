# LEDGER: the build order

18 November 2026. The browser prototype rounds that build DESIGN.md: the core loop end to end first, then deeper. Then what the Unreal game takes over, and when. Nothing starts before "Vision approved:".

## How a round works

- One cloud run of under an hour builds one round. A second short run plays it and reviews it.
- Each round names its design question, the DESIGN section it builds, the study lines it carries, the experience rules it must meet and the measure it should move (ruling 18 Nov).
- A round is done when its rules pass, a fresh reviewer has read it, and the two runs below have been played. A round that fails repeats; it is not carried forward. A round that proves too big for one run is split in two under the same number; the order does not change.
- A build reaches him only with a publish-gate pass and a known-issues note.
- No polish. Art, animation detail, performance, voices, clothes and faces are never the browser's work (his decision of 17 Nov).
- The prototype stays on its allowlist line (three.js, esbuild, acorn, puppeteer-core). Nothing else is recommended.
- The rounds and the prototype stage need their place in PLAN.md through the Monday order (ruling 29 Sep; waiting items 16, 21 and 22).

## The measures

Two whole-session runs, played by the AI playtester as a newcomer and then read by the panel of eight reviewer cards:
- The evening run: one game day, from waking through the night's job to the next morning. About 20 minutes at a person's pace.
- The week run: Act I, Monday to Sunday. About two hours at a person's pace. From stage B.

The first-hour run of rounds 1 to 5 is kept beside them, so the old numbers still compare.

| | Measure | Round 5 (first hour) | Target |
|---|---|---|---|
| M1 | Thumbs up from the panel. The main number. | 2 of 8 | 4 of 8 for an evening, 5 of 8 for a week, 6 of 8 before Unreal multiplies anything |
| M2 | Tense moments per 30 minutes, and their mix (ER-TENS-01) | 19.5; 28 of 39 were one kind | at least 12, from four or more sources, none over half |
| M3 | Retellable moments per 30 minutes (ER-TENS-02). New: the playtester marks them, the panel's "most exciting moment" confirms. | about 1 in the hour | 1 in the first 30 minutes, then 2 an hour |
| M4 | Activity mix: kinds per 30 minutes, talk share, waiting share (ER-CORE-06) | 7 kinds in the hour; talk 25%; waiting 41% | about 10 kinds per 30; talk under 30%; waiting under 10% |
| M5 | Empty minutes: the longest stretch with nothing new, and minutes with nothing new, nothing tense and nothing chosen (ER-CORE-05) | 10.8 minutes longest | no stretch over 5; at most 5 empty minutes in 30 |

## Stage A: one evening that holds

The core loop, end to end, inside the frozen town: no change to seeing, gossip, routines or police statements.

Rounds 9 and 10 meet ER-EYES-01 to 04 and 08 by showing the frozen rules' own outputs; the beat constable is a new verb above the simulation (ruling 18 Nov, new verbs welcome), not a change to statements or custody. Any rule that needs the town changed waits for the switch and is listed in the round's known-issues note.

Round 7 builds the first hour as DESIGN restages it, the recommended answer to QUESTIONS 4, and flips to his approved staging if he picks it. Round 8 tests the cab as the day's main verb as a prototype question, not adopted (QUESTIONS 6): it measures whether fares stay fresh, and his answer to QUESTIONS 6 decides, with the week run's numbers beside it.

| Round | Builds, and its question | DESIGN | Study lines | Rules it must meet | Should move |
|---|---|---|---|---|---|
| 6. The gate | The clumsy-player bot, the checks it can see, the known-issues note. Fixes what it finds on foot and in the cab: a car that always backs out, eased steering on keys, the camera out of walls. Can a build be proved safe before he touches it? | §19, §17, §5 | aaa-s02-05, s16-02, s09-05, s10-03, s10-06, s13-01 | ER-CORE-01 to 04; ER-CAM-01; ER-INPUT-01 to 03; ER-DRIVE-01, 02, 06, 07, 08; ER-SCREEN-01, 02; ER-SAVE-02; ER-TALK-05 | The gate passes. Stuck events and prompt faults at zero. |
| 7. Hands first | The ferry, the walk up the quay, Sheila's six lines spread across the things, the first fare by minute three with Pauline's directions, the debt book and Darren's choice, hints on hesitation. Does a first verb inside three minutes keep the impatient player and the GTA player? | §15 to 7:00; §5 radio | s02-01, s02-02, s02-03, s02-07, s02-08, s02-10, s16-06, s16-08, s16-11 | ER-FIRST-01 to 03; ER-JOB-01, 02; ER-DRIVE-09; ER-TALK-06 | M1: the two who quit at minutes 3 and 5 stay. First verb under 3 minutes. |
| 8. Fares that are play | Fares drawn from routines; a fare within 30 seconds; three wrinkles first (the talker, the parcel, the runner); the soft edge. Do fares end the waiting? | §5 fares; §4; §1 | s02-01, s02-06, s11-07, s16-01, s16-04, s16-10 | ER-CORE-05 to 08; ER-JOB-03 to 06 | M4: waiting from 41% to under 20%, driving under 25%. M5: longest stretch under 5 minutes. |
| 9. The carry | Night one as the designs have it: Ron's ask with the no that is asked twice, the coat and pockets, three routes, the constable's challenge, search and chase, the man at the landing, the witness's walk shown. Is this the moment a friend retells? | §15, 7:00 to 11:30; §3; §6; §8 beat; §2 walk | s01-03, s03-09, s05-03, s07-05, s08-04, s08-06, s11-01, s15-09, s16-02, s16-03, s16-04 | ER-EYES-01 to 04; ER-POL-02, 04; ER-NIGHT-01; ER-SND-01; ER-JOB-03, 04; ER-CORE-02, 03 | M3: one in the first 30 minutes. M2: chases and escapes above zero. |
| 10. The count and the morning after | The count with Sheila and her warning; the Ledger's Money and Open parts; the morning it comes back; a save after every deed and step; "wait until". Do the tin, the book and the comeback make the next evening wanted? | §9; §10; §2; §17 saving; §6 | s02-04, s02-09, s11-03, s11-05, s11-06, s16-05, s16-07 | ER-MONEY-01 to 04; ER-LEDG-01 to 03; ER-SAVE-01; ER-EYES-08; ER-JOB-04, 07; ER-FIRST-04 | M1 on the evening run. The tester answers "what next, and where" from the Ledger. |
| 11. An evening that holds | Nothing new. Tunes rounds 6 to 10 against the evening run; closing lines that vary; the clock measured. Is one whole evening worth a thumb from half the panel? | §1; §3; §11 | s03-02, s03-04, s03-05, s03-08, s11-11 | All of stage A's; ER-TALK-01, 02, 04, 07; ER-TENS-01, 02 | M1: 4 of 8. M4 and M5 at target. ER-FIRST-04: the town visibly knows him by minute 30 (the Meridian Test). |

Then his first hands-on of the loop, 15 to 30 minutes.

## The one-simulation switch

Not a cloud round. It needs his PC or the build machine, and it is waiting item 21 for the order of 23 November.

- The real C# Core, built for the browser, replaces the prototype's own rules: seeing and naming on five rungs, gossip and its fading, who reports, custody, Ellis, debts and purses, the arrangement and the landing, the first week and its end, waiting, Sheila's trust.
- Its test: the 102,960 golden answers identical in the browser build, and the seeded week recorded again.
- Its licence line (the browser runtime, not yet on the allowlist) is already on the waiting list. The fallback is the prototype's own rules checked against the same golden answers.
- It carries the study lines that are the Core's own: no broadcast through a faction (aaa-s01-02), places in a routine with a cap and an owner (s01-04), and the crowd's clock windows (s01-05).
- Until the switch the town simulation stays frozen (ruling 18 Nov). Stage A is built to need no change to it.
- After the switch, a rule the Core lacks and the browser has proved (fares, the wash, rent, the beat constable, cars and people, the dial, talk that cools by kind) goes to the town task as golden rows written from DESIGN, then into the Core, and the C++ port then matches. One simulation, never two.
- Before the switch his answer to QUESTIONS 3 is wanted: the Core has every person at one middle temper. The switch builds to the recommended answer and flips if he picks otherwise.

## Stage B: a week that holds

Act I, whole, on the real simulation.

| Round | Builds, and its question | DESIGN | Study lines | Rules it must meet | Should move |
|---|---|---|---|---|---|
| 12. Break-ins, lifts and rain | Rooms by privacy and hour, the warnings, three keys to a lock, a hot thing, Rita's back room; rain as cover, from one wetness value. Can a room be robbed three ways, and does a hot thing feel hot? | §4; §6; §9 | s15-01 to 08, s04-05, s04-07, s05-04, s08-03, s11-04, s11-08 | ER-JOB-03; ER-NIGHT-02, 03; ER-EYES-02; ER-CORE-03 | M2 mix; M4 kinds. |
| 13. The witness and the arrest | Reaching a witness first (talked round, paid, threatened); the statement; the constable next morning; custody as hours; the street saying it saw. Is the minute between seen and reported the best minute in the game? | §2 walk; §8; §11 | s01-01, s01-03, s02-05, s15-10, s15-12 | ER-EYES-04 to 06, 09, 10; ER-POL-01, 03, 05 (provisional, C5); ER-TALK-03; ER-CORE-04 | M3. The old complaint "arrests lead nowhere" gone. |
| 14. Fights, one against one | Closing in with no lock-on, the wider fight view, the kerb fall, beaten Tom, things to hand. Built to the recommended answer of QUESTIONS 2; flips if he picks otherwise. Does a street fight read and weigh? | §7; §17 fight row | s14-01 to 06, s14-09, s14-12 to 14, s08-08, s09-02 | ER-FIGHT-01, 02, 04 to 07; ER-CAM-02 | The melee drills all in band. M2 mix. |
| 15. Fights, the three gaps | Outnumbered, running away, the police arriving; other men's nerve. Does a fight end five ways? | §7 odds | s14-07, s14-08, s14-10 | ER-FIGHT-02, 03; ER-POL-02, 04 | M2: fights and escapes. M3. |
| 16. Cars and people | His canon ruling: the hit, hurt by speed and intent, stop and help or drive off, the chase, damage with no dead end, the firm's name and fares. Does a hit become a choice and a story? | §5; §17 car row | s09-06 only; the rest is his ruling of 18 Nov and the driving study | ER-DRIVE-01 to 08, 10; ER-FIGHT-05 (a car strike is never a blow); ER-POL-04 | The gate. M3. |
| 16b. The cab under pressure | The other wrinkles: the tail, the wait, the hurry. A car in the mirror, an engine kept running, the last ferry in four minutes. Is the cab tense without a crash? | §5 fares | none of the 145 | ER-DRIVE-02, 04, 09; ER-JOB-06 | M2: new sources. M4 kinds. |
| 17. The two lives | Ada's tea against the second ask; Alison's question from the back seat. Does week one pull his two lives apart? | §15 from 29:00; §16 Act I; §11 staging | s03-07, s07-06, s09-04, s16-04, s16-12 | ER-JOB-04; ER-TALK-03, 06 | M3: two an hour. |
| 18. Ellis, trust and Sunday | Ellis asking, and people saying so; Sheila's trust and the real book; her question with the answer asked twice; the name ladder heard. Does the week end on a choice that matters? | §8; §14; §16 Act I | s03-03, s16-09, s16-12 | ER-RISE-02; ER-TALK-03; ER-POL-05; ER-END-03, asked of the week | M1 on the week run. |
| 19. Side stories and the way | Three of the 32 drafts (one light, one grey, one dark); asking the way; landmarks and signs. Are stories found and finished with no marker? | §4 | s03-01, s16-05, s16-06, s16-11 | ER-JOB-01, 02, 05; ER-LEDG-03 | M5. Each place reached within 3 minutes. |
| 20. A week that holds | Nothing new. Tunes against the week run. | §1; §3 | none: tuning round | All of stages A and B | M1: 5 of 8. M4 and M5 at target across the week. |

Then his play of the week, and the first hand-overs to Unreal.

## Stage C: the rise

Act II. Each round is played inside a run of three game weeks.

| Round | Builds, and its question | DESIGN | Study lines | Rules it must meet | Should move |
|---|---|---|---|---|---|
| 21. Crew on orders | With me, wait, watch, fetch, take, drive, lean; a first recruit by need or by hook. Does a man at his shoulder change the odds and the risk? | §12 | s15-15, s16-04 | ER-CREW-01 to 04 | M2: new sources (the odds). |
| 22. The firm | The board, a third car, the cold-store contract, a first front, a first round, clothes and the name. Is a growing firm felt with no screen of numbers? | §12 board; §14; §9 | s01-06, s06-07, s11-03, s15-03, s15-11 | ER-RISE-01 to 03; ER-MONEY-01 to 04 | M1. The tester lists three changes a rung. |
| 23. The Widow | Her eyes, her ladder: the tax at the dock gate, a man poached. Does a rival who goes after his people feel fair and close? | §13 | s11-02 | ER-RIV-01 to 03; ER-EYES-05; ER-CREW-03 | M3. |
| 24. Agar | Paper: the licence, the solicitor's letter, the inspection of the cars. Can pressure with no fists be tense? | §13 | s11-02 | ER-RIV-01 to 03 | M2 mix. |
| 25. Cammack | Trouble on Quay Street that brings heat he did not earn. Can he clear his name by acting? | §13; §8 | s11-02 | ER-RIV-01 to 03; ER-POL-01 | M3. |
| 26. The owed verbs, first | Have a named man hurt through a named man; point a plan at a person; send men at a rival's property. Is the man he sent the risk? | §12 orders | s15-15 | ER-CREW-03, 04; ER-EYES-05 | M3. |
| 27. The owed verbs, the rest | Frame; lean on a witness; move or hide a body; dock, expel or beat; vouch; the press through Alison. | §12; §11; §7 death | s15-12, s15-13, s15-14 | ER-EYES-05, 06; ER-TALK-03 | M2 mix. |
| 28. The Fixer and the sit-down | True reads, a meeting, one truce; a sit-down, in his own cab if he likes: accept, defy, counter. | §13; §16 Act II | s16-12 | ER-RIV-03; ER-TALK-03 | M1. |
| 29. Weapons, guns and the dial | Carried weapons; guns as events; the four states. Only after fists have passed his play. Does one shot change the town for good? | §7 | s14-10, s14-11, s10-05 | ER-FIGHT-08, 09; ER-POL-05; ER-EYES-07 | M3. Guns and deaths stay rare at War. |
| 30. An Act II that holds | Nothing new. Tunes against three game weeks. | §14; §16 | none: tuning round | All so far | M1: 6 of 8. |

## Stage D: the end

| Round | Builds, and its question | DESIGN | Study lines | Rules it must meet | Should move |
|---|---|---|---|---|---|
| 31. The inspection | The letter; one item a morning; Sheila's help; Ellis's trade; the successor's offer. Do five mornings feel like the whole game coming due? | §16 Act III; §9 | s16-12 | ER-MONEY-04; ER-END-02 | M3. |
| 32. The endings and their signs | Tom's reading; every sign; the endings at the count he rules (QUESTIONS 1). Did he see each cost coming? | §16; §10 | s16-02, s16-09 | ER-END-01 to 03; ER-CORE-03 | The tester predicts the ending the state gives. |
| 33. A whole playthrough | Nothing new. A scripted run from the ferry to an ending, and the panel on its record. | all | none: tuning round | All | M1: 6 of 8, from the first hour to the ending. |

One revision pass sits outside the numbering: after the first read of GTA VI (it releases on 19 Nov; systems only, no story; studied from the outside only, ruling 17 Nov). It may revise DESIGN §5, §7 and §17 and add or reorder rounds.

## What the Unreal game takes over, and when

A system enters Unreal only after its round has passed its rules, its run has held its measure, and he has played it once. What carries over is behaviour, proved by the same tests on both sides, never the browser's own settings.

| Part | Proved in the browser at | Unreal takes it | Held equal by |
|---|---|---|---|
| The experience rules and the clumsy player | Round 6 | Now: the next packaged build and every one after (ruling 18 Nov) | The same rule ids in the AI tester's walk. ER-START-01 and ER-PERF-01 can only be met by a packaged build. |
| The camera's rows, the street's sound, the interface's sizes and switches | Not browser work (no polish) | Phases 2 to 4, where their study lines are already kept: aaa-s08-01, s08-02, s08-05, s08-07, s09-01, s09-03, s09-07, s10-02, s10-04, s10-07, s13-02 | ER-CAM, ER-SND-01 and ER-SCREEN on the packaged build |
| The first minutes on foot: the arrival, the walk-round at the things, Darren's debt, the carry, the morning after | Rounds 7, 9, 10 | Phase 3 (make thirty minutes hold) and phase 4 (the friends' candidate): the on-foot cut of DESIGN §15 | The same beats and lines; ER-FIRST and ER-EYES-08 on the packaged build |
| The Ledger | Round 10 | Phase 3, "a useful office and ledger" | ER-LEDG; the same entries from the same seeded evening |
| The simulation | The switch | It is already the Core; the C++ port is checked against it | The golden answers, letter for letter |
| Rules the Core lacks: fares, the wash, rent, the beat, cars and people, the dial | Rounds 8 to 16 and 29 | The town task, as golden rows from DESIGN; then the port | Golden rows |
| Fists | Rounds 14, 15 | Phase 3's fight lab test, then the crime and combat phase | The melee drills C1 to C15 on both: the bands, not the settings |
| The cab, fares, traffic, cars and people | Rounds 8, 16 and 16b, with his driving study (the cab's weight in the day is decided by his answer to QUESTIONS 6, not adopted before) | With the first town, when the map grows (the arcade car of his 17 Nov ruling); AAA driving the end state, costed for him first | The scripted drives D1 to D8 within 5%; ER-DRIVE |
| Police, break-ins, fencing | Rounds 12, 13 | The crime and combat phase | Golden rows; ER-POL; every job outcome scripted |
| Crew, the firm, the rivals | Rounds 21 to 28 | The empire and docks phases | Golden rows; ER-CREW; ER-RIV |
| Acts II and III and the endings | Rounds 26 to 33 | The story phase | Every ending by a scripted route; ER-END |
| Guns and the dial | Round 29 | Last, after melee has passed his play | ER-FIGHT-08, 09 |

If he chooses the grey Hook in Unreal after the friends' evening (the open skeleton decision of 18 Nov), its nightly walk from the arrival to an ending takes its beats from these rounds.

## What it costs

29 rounds, each about an hour and a half of cloud time with its play and review: about 45 hours if every round passed first time. Past estimates ran two to five times over, so 80 to 200 hours is the honest range. That is still well under the scope draft's 270 to 500, because after the switch the Core brings most of the town's rules whole. No new money: it runs inside the lane's share of the week.
