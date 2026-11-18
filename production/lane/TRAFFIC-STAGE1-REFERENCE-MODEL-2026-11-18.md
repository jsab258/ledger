# Traffic stage 1: the reference model and its golden traces (18 November 2026)

Lane item 62. Machine-free part of traffic stage 1 (TRAFFIC-COST-2026-11-17.md, section 7: lane data and timetable 4 h, follower 8 h, spawner and pool 4 h, giving way and horn 6 h, est.), done ahead so the PC part is a port checked against numbers, not tuning by eye. Stage 1 still starts only after the parked hatch passes his gate (n16-9).

## What it is, in plain words

A small program that says exactly how the background cars at the street's end behave: when each car comes, how fast it goes, how it keeps its distance from the car in front, how it slows for the mouth of Quay Street, how it stops for a person in the road and when it sounds its horn. It writes seven reference recordings (golden traces). The Unreal car, a plain object sliding along a spline with no physics, must replay those recordings within small tolerances. That is the same rule as the simulation port (C# goldens) and the driving feel study (scripted drives): behaviour carries over, never engine settings.

## The rules (the behaviour of record)

1. Timetable. Each game hour, each lane draws its own arrival times from a seeded random stream keyed by (seed, game day, game hour, lane). Gaps are random with the band's average (Poisson arrivals), never under 4 s in one lane. Average gap, both directions together: 50 s in the rush hours (07:00 to 10:00, 16:00 to 19:00), 75 s by day and 06:00 to 07:00, 150 s in the evening (19:00 to 23:00), 450 s at night. Bands are whole game hours because a game hour lasts only 30 real seconds. Gaps are in real seconds of unpaused play and each lane's stream is drawn one car at a time with no end, so cars keep coming however long talk holds the clock; a wait that jumps hours simply skips those hours' cars. A new game day gives new keys, so day 2 is not a replay of day 1. Rates live in rates.json, his to change.
2. The pool. Three cars at most. A due car spawns out of view at the lane's start if a pool place is free, the lane start is clear (12 m) and the number of cars on the road and not yet past the view is under the band's limit (2 by day, 1 in the evening and at night). Otherwise it waits up to 10 s, then is dropped. A car is removed once fully past the lane's end, out of view.
3. Each car draws its own desired speed (8.9 to 12.5 m/s, 20 to 28 mph, est. for a 30 mph town road), its variant (hatch or its second variant) and one of 8 colours, from its own stream, so changing the rates never changes which car is which.
4. The follower is the Intelligent Driver Model with the published city values (Treiber and Kesting, Traffic Flow Dynamics, Table 11.2: time gap 1.0 s, minimum gap 2 m, acceleration 1.0 m/s2, comfortable braking 1.5 m/s2, exponent 4). Above its desired speed (entering a speed cap) it uses a hybrid: the Improved IDM's gentle free-road slow-down with the plain IDM's following term. That is not the full published Improved IDM; it brakes slightly harder, the safe side. Braking is capped at 6 m/s2. Fixed step 0.1 s (the game's fixed clock step), the standard ballistic update, and a car never rolls backwards.
5. Speed cap: from 60 m before the mouth of Quay Street to its far side, the desired speed is at most 8.9 m/s (20 mph). The car eases towards it (it reaches about 9.2 m/s, not exactly 8.9: the model approaches the cap gently).
6. Giving way: a person in the lane within 30 m ahead is a standing obstacle 1.5 m short of the person; the car eases to a stop about 2 m behind that. Once stopped (under 0.3 m/s), one horn after 3 s and a second after 10 s, then silence; it never drives round or through. When the person leaves it pulls away.
7. A person who steps out inside the stopping distance: the car halts dead 0.3 m short, never moving backwards; a person standing beside the car's body holds it where it is. Either logs one emergency stop (unphysical and rare; stage 2's physics replaces it), which the simulation can treat as a noticeable act; the horns then follow as in rule 6.
8. Brake lamps on when slowing harder than 0.3 m/s2 or standing. Wheels turn by distance over a 0.2876 m radius (a 175/70 R13 tyre).

## Files (tools/lane/traffic/)

- traffic_model.py: the model; lanes.json (lane lengths, view window, the speed cap, all marked placeholder until measured on the PC), rates.json, cars.json.
- make_goldens.py writes goldens/: G1 free road, G2 following, G3 person in the road with both horns, G4 speed cap, G5 the day's timetable (seed 1990, day 1), G6 a whole game day's event log, G7 emergency stop, G8 a stress run of the pool (one car every 10 s, a person blocking one lane for 60 s across an hour change: queueing, the full pool, waiting, dropping, horns). `--check` fails if they drift.
- test_traffic_model.py: 59 checks, all passing in about 2 s: the random numbers' known values, the rates over many days, the minimum gap, no overlap and the pool and view limits over 40 seeded game days, same seed same day, cars keep coming for 30 minutes on a held clock, day 2 differs from day 1, no car waits 20 s with nobody in the road, horns at 3 and 10 s, stopping short of a person, one emergency stop and no creeping while held, the clamp never moves a car backwards, a person beside the body holds the car, car identities unchanged when rates change, the goldens current.

## What the PC session does with it

1. Measure the side road's real lane lengths, view window and the mouth of Quay Street from the level; put them in lanes.json; run make_goldens.py.
2. Write the follower actor and spawner in Unreal to these rules: SplitMix64 and the key mixing exactly as in traffic_model.py (a few lines of C++), the 0.1 s fixed step, and the same order in every tick: the hour from whole milliseconds (30,000 ms a game hour), new lane streams on an hour change, due arrivals moved lane by lane to the waiting list, the waiting list sorted by (due time, lane, day, hour, number) and tried in that order, then all accelerations from the old state, then moves, clamps and horn counts car by car, then events and removals in car order. The fourth power as r2 times r2; the horn timer as whole steps.
3. A small automation test replays G1 to G7 and passes within: position 0.05 m, speed 0.02 m/s, event times 0.1 s, arrival times 1 ms. Then the tester's walk, soak, save and reload and the frame ruler as in the costing.

This should take the PC part's follower, spawner and give-way rows down from est. 14 h towards est. 8 to 10 h (assumption: the port is mechanical; untested).

## For the town task (not done here)

Each car is a perception event in stage 1 (TRAFFIC-COST section 6): noise while passing, headlamp light at night, brief cover of sight lines; a horn at the player is a noticeable act. The model's event log (spawn, horn, emergency stop, despawn) is the hook list. Their loudness, light and duration values belong to the bounded town task in the C# Core with its own goldens; the lane does not touch the Core.

## Limits and open points

- All lane distances are placeholders until measured. Desired speeds and the horn timings are estimates, not measured; his data files to change.
- Floating point: arrival times are rounded to whole milliseconds; the log function in C++ could, very rarely, round one arrival a millisecond differently. The tolerance allows 1 ms.
- No physics, no turning cars, no junction traffic, no vans or minicabs (later options in the costing).
- Fresh review: production/lane/reviews/REVIEW-TRAFFIC-STAGE1-MODEL-2026-11-18.md, PASS WITH FIXES; all ten fixes applied and the goldens regenerated. The book's Table 11.2 was read through the publisher's sample chapter by this run; the reviewer could not reach it.
- Licences: the IDM is a published model (no code taken); SplitMix64 is public domain (Vigna). Nothing new to add to the allowlist.

## Sources (read 18 Nov 2026)

1. M. Treiber, A. Kesting, Traffic Flow Dynamics, Springer, chapter 11 sample (Table 11.2, city values; the Improved IDM; braking limits). https://www.traffic-flow-dynamics.org/res/SampleChapter11.pdf
2. Treiber, Hennecke, Helbing, "Congested traffic states in empirical observations and microscopic simulations", Physical Review E 62, 1805 (2000), via the summary at https://en.wikipedia.org/wiki/Intelligent_driver_model
3. Zhou, Zheng, Tian, Jiang, Zhang, "Twenty-Five Years of the Intelligent Driver Model" (arXiv 2506.05909v2, revised 23 Nov 2025): the equations; collision-free while the braking limit is not reached. https://arxiv.org/pdf/2506.05909
4. Project files: TRAFFIC-COST-2026-11-17.md (rates, method, horn timings), HATCH-CLASS-AND-PLATES-2026-11-17.md (tyre size), production/research/game-clock/NOTE-2026-09-30.md (2 game minutes a real second; 0.1 s fixed step).
5. SplitMix64: Sebastiano Vigna's public-domain reference (constants as in Java's SplittableRandom); the first outputs from state 0 are checked in the tests. Not re-read today: unverified beyond the matching test values.
