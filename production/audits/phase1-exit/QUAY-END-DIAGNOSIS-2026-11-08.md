# The quay end's stop: diagnosis (8 Nov, n02-9-quay-end-stop)

Read only. Line numbers are the 8 Nov working tree's; CrimeProbe.cpp carries an unrelated edit.

## The measure

"Both walkers" are Ron (rocco) and Darren (sam), not the pacing extras, who stay between x 6 and 31.5 (street-people.json:39-46, 57-64). "About x 0" was seen with the spot at (-5, 0) (HANDOVER.md:43; FINDINGS.md:28), so it describes the old spot, not the current code.

## 1. The halt at x 0

The cause is the invisible end wall: a box from x -1.5 to -0.5 that blocks only people (SliceCharacter.cpp:1495-1507, always on, :511).
- The walk test steps every half metre with a 30 cm capsule against anything that blocks people (CrimeProbe.cpp:7786, :7791, :7922-7934).
- From the street side it is blocked below x -0.2, so the walk ends "as far as is clear" near x 0 (:7972). Side steps of 0.6 to 1 m (:7959) cannot pass a 40 m wall.
- From the quay side it stops at -1.8: Ron walked from (-3.90, 0) to (-1.83, 0.33) (F:/LedgerTools/gate/new/office-sit-default-2026-11-07/walk-day/logs/LedgerProbe-backup-2026.11.07-14.45.48.log:2498).
- Teleports ignore the wall: Darren was placed at (-5, 0) and Ron at (-3.9, 0) (same log :2419-2420; the 1.1 m offset is CrimeProbe.cpp:8469).
- Navigation is ruled out: the walking map is built only with -LedgerNav (SliceCharacter.cpp:510), and the walks are straight lines (CrimeProbe.cpp:7938-7977).

On the current code the move answers it. The spot is (1.0, 0.0) (hook-cast.json:60-62, commit 245629b94; builds fa46ab0, 3b3454e).
- In the 8 Nov speaker-sit run, Ron walked the whole way and stood at (1.04, 0.02) (F:/LedgerTools/gate/new/speaker-sit-2026-11-08/sit.log:2750, :2770).
- Darren was refused at once, "0.6 m on by free_car_rail_slot", the hidden box at the fish market's railing (:2748; CrimeProbe.cpp:2638), then placed at (2.1, 0) (:2782). That is a separate stop.

Side effects, unverified in play:
- The landing triggers within 8 m of the quay (CrimeProbe.cpp:7680, :7693). That circle now reaches Mickey's rank, 7.5 m away.
- The tester's stand-off point 1.1 m east of Ron is Darren's offset spot, and walkers wait for Tom within 1.3 m ahead (PersonAnim.cpp:565-573).

## 2. Why the 7 Nov round ended there

It ran on 76db411, before the move (verdict written 20:11; move committed 21:58).
- 12:38: the aim for Ron was fixed at the fish front (F:/LedgerTools/gate/new/tester-round-2026-11-07/verdict.json:784-795). That walk never re-reads him (tools/route_walk.py:266-324), and he moved at 13:00 (hook-cast.json routine).
- 13:26 to 16:59: the rail-slot box held Tom at z 2.50, its face at 2.80 less his capsule (verdict.json:883-1015).
- 18:40: the new aim was (-3.91, 1.2), 1.1 m from Ron's quay reading (:1081-1092; route_walk.py:145-165).
- 19:22: Tom stopped at x -0.20 (:1136). Blocked legs swung him 2.5 m sideways and back (route_walk.py:293-304) until D3 01:57 (:1389).
- By then Ron was off the street ("lost sight", route_walk.py:381-382; verdict.json:73), and so was Darren (:78).
- From the morning stage at 10:08 to D3 01:57 is 15 h 49 m.

Unverified: from 17:22 to 17:56 the aims fit Sheila's spots, not Ron's. The round's game log was not found.

The 8 Nov night walk never reached the quay: Darren was lost with Tom held near (9, 5.5) (F:/LedgerTools/nightly/2026-11-08/walk.log:18). It cannot judge the move.

## Confidence

- Part 1: about 90%, from one run.
- Part 2: about 85%.
- What would confirm it: a packaged walk that greets Ron at (1, 0) between 17:00 and 19:00.

Not checked:
- the round's game log;
- whether sit.log is the packaged copy (the copy's stamp says 3b3454e);
- the engine's query-filter source (only its effect is seen in the logs);
- a person walking it.
