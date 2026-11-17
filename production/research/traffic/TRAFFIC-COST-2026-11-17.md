Method researched: production/research/aaa-reference/studies/04-street-world.md

# Background traffic in the friends' build: costed plan (17 November 2026)

For the order of 23 Nov. Written by a research helper, saved by the session. Nothing was built. Tags: [R] read in a file, [J] the helper's judgement, UNVERIFIED where no source confirms. Fresh review PASS WITH FIXES (REVIEW-TRAFFIC-COST-2026-11-17.md), fixes applied 17 Nov.

## 1. Ruling and dependency
- RULINGS cars line (17 Nov): parked cars first, then traffic from their kit in the friends' build once one car passes. An arcade car comes once the map grows. AAA driving is the end state.
- PLAN.md phase 4: "Traffic from the car kit (17 Nov)".
- Hard dependency: the hatchback passes P9's blind test, its gate and his look (n16-9; production/research/phase2-plan/PLAN-PARKED-CARS-2026-11-17.md, about 25 to 41 h, not counted here). His words on 8 Nov were "the other three after I've seen it". So traffic starts with one passed car, with variety from colour sets and invented plates (GTA V's method, asset-plan/SUMMARY.md §3). No box cars, no unapproved classes. If P9 fails, this item does not start.
- Canon: no real models or brands, no ice-cream van, no brewery dray (SUMMARY.md, special vehicles).

## 2. What the friends see [J unless marked]
- Quay Street: a 48 m road with a 6.0 m carriageway of two 3.0 m lanes [R: production/specs/vignette-scene.json, carriageway]. The kept parked places are on the east kerb at z 1.96 m [R: production/specs/street-vehicles.json].
- At most two moving cars in view, never two opposing cars beside the parked ones. The spawner holds the second car until the first has cleared.
- By day, one car passes about every 40 to 90 s. Density by hour from the project's own curve in ledger/Assets/Scripts/Core/Traffic.cs `BusynessAt` [R]: 1.0 at 07-10 and 17-20; 0.8 by day; 0.6 at 20-23; 0.35 to 02:00; 0.2 in the small hours, never zero.
- Speed: 15 to 20 mph (7 to 9 m/s), slowing near people. Traffic.cs gives 11 m/s on an open avenue, too fast for this street [J]. 2-VEHICLES.md line 199 calls for "walking-town speeds" [R].
- Night: dipped headlamps and tail lamps lit. Rain: wet paint tied to the street's wetness (2-VEHICLES.md line 198), tyre hiss, speed about 10% lower [J].

## 3. Method end to end, with references
Mafia parks nothing in its measured street, and its traffic is spawned [R: studies/04-street-world.md, 25 Oct]. Its lane format, density and vehicle files were never read (field-scans/CARS-2026-11-08.md). Kingdom Come II has no analogue for cars (coverage-audit-kcd2/DELIVERY.md line 562). Epic's City Sample runs traffic on Mass, lanes from ZoneGraph, spawners for traffic and parked cars; no counts or spawn rules given (https://dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-project-unreal-engine-demonstration, read 17 Nov 2026). Its content is outside the allowlist; only the method is read.

| Step | Method | Reference |
|---|---|---|
| Lanes | One spline per direction on the lane centres, entering and leaving behind the corner buildings. Mass and ZoneGraph are built for thousands of agents; one street has two lanes [J] | Mafia: spawned, format none found; City Sample: ZoneGraph lanes |
| Spawn and despawn | A pool of 4 car actors, never destroyed, appearing only at hidden ends, never in a camera's view. No two spawns on one stretch. Thinning by hour fixed by index | Mafia: rules none found; Traffic.cs `Spawn`, `SetHour` [R] |
| Movement | Kinematic, no physics: speed along the spline, wheels turned by distance; accel 2.6, brake 5.5 m/s², gap 1.6 m from Traffic.cs (to check against the walk) | none found in Mafia; 2-VEHICLES.md line 199: "a few kinematic cars on splines" [R] |
| Stopping for people | Port Traffic.cs's hazard rule: brake in time, never enter the box ahead holding a person or the player. Braking distance v²/2a, 7.4 m at 9 m/s. A blocked car waits; the spawner holds the rest. No contact ever | none found (Mafia's civilian reactions, studies/01, are not traffic) |
| Night lamps | Emissive head and tail lamps on the street's night state. At most one dipped spotlight per car near the camera, shadows off | Mafia's street lamps mostly shadowless, 25 of 39 (studies/05-visuals.md) [R]; car lamps none found |
| Sound | Positional engine loop and tyre hiss per car (CC0, licence and catalogue lines), over the distant-traffic bed (levels from studies/08-sound.md, not street-sounds.json) | studies/08-sound.md: cars "not studied"; none found |
| Budget | Significance Manager for tick rate and LOD (studies/12-tech-budgets.md line 76) | Mafia: CPU budget categories only (studies/12) |

## 4. What exists to reuse
- ue-probe `SpawnVehicles` (VignetteShot.cpp) and `ParseVehicles` (StreetMeshes.h): place glb cars from street-vehicles.json, log `vehiclesSpawned`.
- tools/art-recipes/car-model.py and tools/ue/import_vehicles.py; the coming car kit and its colour sets.
- ledger/Assets/Scripts/Core/Traffic.cs: about 1,406 lines of the old engine-free model, 75 mentions in CoreTests: yield-to-people, hour density, never-wedge. Not ported (pre-production/notes/H4b-systems-areas.md line 188). Port only yield and density, against C# goldens.
- The positional "traffic-distant" bed (production/specs/street-sounds.json).
- People's positions from the street's schedule (StreetPace.h, Schedule.h) for the yield check.

## 5. Steps, hours and checks (packaged nightly walk unless marked)
- S0, 1.5 h: one capped look at Mafia's traffic and spawner files (one extractor, space checked, own folder, key blanked). Check (paper, not the walk): a dated note with the files read, or "none found".
- S1, 2 h: lane splines, ends behind the corners. Check: splines clear the parked places by ≥ 0.5 m; ends hidden from the hook camera, reverse view and night view.
- S2, 6 h: pooled actor, kinematic movement, hidden spawn. Check: every spawn and despawn logs `inView=false` (100%); no car appears or vanishes within 60 m in view; no opposing pair beside the parked cars.
- S3, 5 h: yield port with goldens. Check: logged minimum car-to-person distance ≥ 1.0 m, zero overlaps; a scripted crossing stops the car; Soak and regression pass.
- S4, 2 h: density by hour, rain speed, wet paint. Check: a scripted hour sweep in the packaged game (each hour held 10 minutes) logs cars per hour following `BusynessAt` within ±1.
- S5, 3 h: night lamps. Check: night view shows lit lamps; night frame cost measured.
- S6, 3 h: sound, CC0 with a catalogue line. Check: the walk's sound log records each car loop's distance and level, within the mix's band; licence and catalogue lines present (ci).
- S7, 2.5 h: frame budget. Check: RX 6700, 3440×1440 at 50% TSR, High, packaged; two moving cars in view: GPU median ≤ +0.4 ms against the empty street, game thread ≤ +0.2 ms, slowest 1% ≤ 16.7 ms.
- S8, 4 h: gate with fresh reviewers, the three morning views beside the last good ones, RECIPE lines, his page (a frame with moving cars is a whole street frame).

**Total: about 29 h (range 24 to 36), after the sample car.**

## 6. Risks
1. The frame envelope is already over [R: pre-production/4-BUDGETS.md §4.5: base 7.5 ms planned against about 10.8 ms today], with no line for moving cars; their share comes from the 0.5 ms parked-cars line or the reserve. Night adds about 1.5 ms.
2. Who gives way past parked cars in a narrow street: UNVERIFIED against the Highway Code; the one-at-a-time spawner avoids it.
3. One car model repeated can read as clones; colour sets, plates and a second part-swapped look help.
4. The morning pictures need the same three views daily: traffic needs a fixed seed or an off switch for them.
5. The player standing in the road blocks a car for good; it waits; any horn is a later choice.
6. Two tries per fault, then research; a third needs his yes.

## Unverified or unreached
Mafia's traffic method beyond "spawned"; all speeds, gaps and the frame share (judgement); the give-way rule; City Sample read only for its method.
