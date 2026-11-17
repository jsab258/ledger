# Traffic cost: background cars now, an arcade car next, AAA driving last (17 November 2026)

Reviewed 17 Nov 2026: PASS WITH FIXES, applied.

Research helper, about twenty minutes, read only apart from this file. Answers his car stages of 17 November (canon, "What LEDGER is not"; RULINGS, "Cars (17 Nov)"). Marks: [READ] read at the source today; [SS] search result only; [I] the helper's inference; [M] measured in the project; est. an estimate. Sources at the end, read 17 Nov 2026.

## The answer in brief

- Stage 1 (cars passing at the street's end, from the parked-car kit): est. 38 hours machine-free (range 33 to 43) and 47 on the PC (range 40 to 55). It starts only after the parked hatch passes his gate (n16-9), as his ruling says. The kit checklist (section 5) adds est. 10 to 20 machine-free and 6 to 12 PC hours, charged to the kit, not to traffic.
- Method: our own lane splines with a simple "follower" car that slides along them, no physics. ZoneGraph plus Mass (MassTraffic) is built for a city and is wrong for two cars. Chaos Vehicles waits for stage 2.
- Rate: about one vehicle every 60 to 90 seconds by day at the street's end, at most two in view; every 2 to 3 minutes in the evening, every 5 to 10 minutes late at night (est., section 2).
- Budget: fits by day, tight at night. Est. 0.2 to 0.4 ms by day and 0.3 to 0.6 ms at night, of the 2.5 ms and 1.4 ms spare. No new textures; headlamps cast no shadows.
- Stage 2 (arcade car), ROUGH: 150 to 300 hours. Stage 3 (AAA driving), ROUGH: 1,000 to 2,500 hours.

## 1. How professional games do light background traffic

| Game or source | What it does | What LEDGER takes |
|---|---|---|
| Midtown Madness 2 and Midnight Club (Joe Adzima, Game Developer, 2001) [READ] | Cars follow spline "rails" along lane points. A fixed pool fills a bubble round the player. Each car checks only the car ahead in its lane. Only a car in a collision switches to full physics, then tries to rejoin its rail. | The whole method in small. Physics only when hit is the bridge to stage 2. |
| GTA style ambient traffic (Shamus Young, 2015) [READ] | Few cars simulated at once; cars appear and vanish just out of sight; no lasting record of them. | Spawn and remove out of view: the side road leaves frame both ways. |
| Mafia (study 04; TALKS.md 4.3) [READ] | No parked cars in Mafia's measured street, traffic spawned; for The Old Country the director says the town is not "bustling city streets with traffic". | A top studio kept a small dense town nearly free of traffic. Ours is a light touch. |
| Sleeping Dogs (Audiokinetic interview) [READ] | A "distant traffic loop" is one of about 12 ambience layers, its volume set by time of day and the number of traffic cars. | A distant traffic bed on the same clock as the visible cars. |

## 2. How many cars, how often

- DfT: in 2016 an average urban minor road carried about 2,200 vehicles a day [READ]. 1990 traffic was lower overall [I]; the 1990 figure was not reached.
- Buchanan's Traffic in Towns (1963) surveyed about 50 residential streets carrying 10 to 1,500 vehicles an hour [READ].
- Reading for the road at Quay Street's end [I]: a quiet port side road, below average. About 1,000 vehicles a day, mostly 07:00 to 19:00, gives about one a minute by day.

| Time (game clock) | One vehicle on average every | At most in view |
|---|---|---|
| 07:00 to 09:30, 16:30 to 18:30 | 40 to 60 s | 2 |
| Rest of the day | 60 to 90 s | 2 |
| 19:00 to 23:00 | 2 to 3 min | 1 |
| 23:00 to 06:00 | 5 to 10 min | 1 |

The asset plan's line ("one moving vehicle every minute or so", 2-VEHICLES.md) agrees. A car crossing the street's end at 20 to 30 mph is in view about 3 to 4 seconds [I]: quiet, not empty. All rates live in one data file, his to change. Stage 1 uses the hatch and its second variant only; buses are scenery (genre ruling).

Later options, each a separate item: a stopping delivery van (est. +16 to 24 PC hours), a minibus, the minicabs to and from the rank (est. +10 to 15 hours), a car pulling into a bay and becoming a parked car (est. 3 machine-free, 5 PC, plus save, reload and seed rules for a car that was not there before).

## 3. The Unreal 5.8 method

Chosen: splines plus a simple follower actor.

- Lanes: a spline each way on the side road, tagged with speed, give-way points and stop lines. Our own small lane data, not ZoneGraph.
- The follower: moves along its spline by distance, keeps a gap to the car ahead, eases to a stop, turns its wheels from distance travelled, lights brake lamps when slowing. No physics. Well under 0.05 ms of game thread for three cars [I].
- Determinism: the timetable comes from the seed and the game clock, so same-seed runs match, as PLAN's weather proof asks of witnesses.
- A pool of three cars, spawned and removed out of view.

Rejected for now:
- ZoneGraph plus Mass (MassTraffic): built for The Matrix Awakens; called "very complex" on Epic's forum, and ZoneGraph cannot be generated or changed at run time [READ]. Mass's cheap instanced animation is marked experimental [READ]. Right for hundreds of cars, wrong for two.
- City Sample: content never used (outside the allowlist); its code read as method only.
- Chaos Vehicles for background cars: costs more and can wobble [I]. Kept for stage 2. Epic's online docs are now at 5.9 and also describe Chaos Modular Vehicles, which build a car from breakable parts [READ]; whether 5.8 has it is checked on the PC.
- Nothing bought (16 Sep).

Giving way: a box ahead of each car checks for a person or the player in the road. The car slows, stops and waits. Still blocked after about 3 seconds, one short horn; after about 10, a second (est.). It never drives through or round a person; it waits, as a real driver would.

Sound:
- Per car: an engine loop pitched by speed, a pass-by, a tyre layer blending dry to wet from the one saved wetness value, a plain horn. Plus the distant traffic bed.
- Freesound has CC0 sounds (a puddle splash checked [READ]), but two of three car recordings checked were CC BY [READ], which D26 does not allow (sound is CC0 only); the allowlist is silent on sound effects. Each file's licence is read at download.

## 4. The frame and card budget

From PLAN.md: median 16.7 ms, p99 25 ms, 6 GB on the card with the voice; about 2.5 ms spare by day and 1.4 ms at night, shared.

| Cost | Day, est. | Night, est. | Note |
|---|---|---|---|
| Drawing 1 to 2 cars at a far level of detail, base pass and shadow cascades | 0.1 to 0.2 ms | 0.1 to 0.2 ms | Nanite and virtual shadows are off, so a moving car redraws into each shadow cascade (4-BUDGETS 3). |
| Lumen reacting to a moving car | 0.05 to 0.1 ms | 0.05 to 0.1 ms | [I], not measured anywhere. |
| Headlamps, unshadowed lights or lit lamp cards | none | 0.1 to 0.2 ms | Shadow-casting headlamps not allowed. |
| Game thread, sound, lanes | under 0.05 ms | under 0.05 ms | Off the graphics card. |
| Total | 0.2 to 0.4 ms | 0.3 to 0.6 ms | Up to 0.6 of the night's 1.4 ms, about 45 percent. |

Anchor: one MetaHuman at 3.5 m measured 0.31 to 0.36 ms and three together 0.63 ms [M, 4-BUDGETS 4.5]; 4-BUDGETS allocates 0.5 ms to six parked cars in view [I]. One or two 40,000-triangle cars (asset-budgets.json) at a far level of detail should sit well below one MetaHuman, hence 0.1 to 0.2 ms [I].

Card memory: the 16 Nov packing plan measured 5,072 MB against a 4,711 MB line at the peak, already over. So moving cars reuse the parked kit's variants and trims; extra memory is a few MB of sound [I].

Verdict: measured with the frame ruler (n16-11, PresentMon) on a wet night before acceptance. If night costs more than 0.4 ms, first make the headlamps lit lamp cards with no real lights, then halve the night rate; if still over, no traffic after 23:00.

## 5. The car kit's first build: checklist so stages 2 and 3 redo nothing

The kit is a scripted loft (tools/lane/car_loft.py; its Blender side untested). Today it makes one body mesh and plain tyres for the silhouette test. The first real build should produce:

1. Wheels separate, each pivoting at the wheel's centre, spinning about the axle; hub, tyre and trim as parts.
2. One source, two exports. The kit keeps each panel, wheel and glass piece as its own mesh in the source file and assembles two exports from it: a skinned mesh with wheel bones for Chaos Vehicles (a root bone at the car's centre on the ground, one bone per wheel at the hub, named the same on every platform), and loose parts for Modular Vehicles if 5.8 has it. Which one stage 2 uses is decided when stage 2 starts. Stage 1 turns the wheel bones.
3. Arches cut with room for the wheel to rise about 8 to 10 cm (est.).
4. Simple collision: one box plus arch shapes, at most 6 hulls (asset-budgets.json "car").
5. The body split along real panel lines (bonnet, boot or hatch, doors, bumpers, wings), each piece with its hinge pivot placed, welded shut in stage 1. These are the pieces item 2 exports both ways.
6. Damage-ready topology: even edge spacing on panels so dents can deform them.
7. Glass as one piece per window.
8. An interior slot: a socket and set bounds per platform, first the dark simple interior, later a full one, the shell unchanged.
9. Named sockets: lamps (front, rear, brake, indicators, reverse), exhaust, driver's seat and hands, door handles, horn, engine sound source, plates, camera mounts (chase, bonnet, interior).
10. Lamp lenses in their own material slot, their glow switched by a value.
11. Material slots as planned (paint, glass, chrome, black plastic, rubber, lens, plate, interior).
12. Weight and size data beside each platform (wheelbase, track, wheel radius) for physics.
13. Lanes in our own data that the follower, AI drivers and physics cars all read; kerbs and drains built as real geometry so a physics wheel meets them.

Cost: est. 10 to 20 hours machine-free and 6 to 12 on the PC, charged to the kit item, not to traffic.

## 6. What the simulation must know

The game's core is what people notice and remember (seven perceivable slots per act).

- Stage 1, cheapest honest version: passing drivers are not witnesses. Each car is still a perception event: noise (engine and tyres raise the street's loudness for a few seconds, so a scuffle may go unheard), light (headlamps briefly light the street at night) and cover (a car briefly blocks sight lines).
- A horn at the player standing in the road makes people near look at him: a noticeable act by the player.
- Later, cars that belong to people (the firm's, police, minicabs) become evidence: a car leaving fast fills the flight slot, its colour, kind and part of the plate are remembered.
- This is a bounded town task (C# core, with goldens): est. 6 hours machine-free and 2 on the PC; the decision recorded with it, inside canon.

## 7. Stage 1 hours, est.

| Work | Machine-free | On the PC |
|---|---|---|
| Lane data and timetable design | 4 | 3 |
| Follower car (gap, stop, wheels, brake lamps) | 8 | 6 |
| Spawner and pool, seeded by clock | 4 | 2 |
| Giving way and horn | 6 | 6 |
| Perception events (bounded town task) | 6 | 2 |
| Sound: sourcing, loops, wet blend, bed | 4 | 6 |
| Night lamps, wet look on moving cars | 1 | 4 |
| Moving-car fittings beyond the kit checklist | 2 | 4 |
| Tests: tester walk, soak (no stuck or overlapping cars), save and reload, frame ruler day and night | 3 | 10 |
| Gate pictures and fresh review | 0 | 4 |
| Total | 38 (range 33 to 43) | 47 (range 40 to 55) |

Not included: the car kit and its second variant (2-VEHICLES.md: 4 to 6 days), the checklist additions (section 5), the later options (section 2).

## 8. Stages 2 and 3, ROUGH

ROUGH: first ranges for scale, not plans. They assume the checklist was followed.

| Stage | ROUGH hours | What drives the cost |
|---|---|---|
| 2. Simple arcade car | 150 to 300 | Handling tuning by feel (many short checks with him); getting in and out with a MetaHuman (the likely overrun); a chase camera; background cars switching to physics when hit. |
| 3. AAA driving | 1,000 to 2,500 | Handling depth (weight transfer, wet tyres); damage (dents, panels off, glass and lamps); AI drivers who react, and police chases; a full interior and first-person view with layered engine sound. The bar is Mafia or GTA, made by large teams over years [I]. |

The biggest risk in both is handling feel, won by iteration, not code.

## Sources (all read 17 Nov 2026)

1. Joe Adzima, "AI Madness: Using AI to Bring Open-City Racing to Life", Game Developer, 24 Jan 2001. https://www.gamedeveloper.com/programming/ai-madness-using-ai-to-bring-open-city-racing-to-life
2. Shamus Young, "Grand Theft Simulated Traffic", 17 May 2015. https://www.shamusyoung.com/twentysidedtale/?p=26762
3. DfT, Annual road traffic estimates 2016. https://assets.publishing.service.gov.uk/media/5a821e47e5274a2e8ab57965/annual-road-traffic-estimates-2016.pdf
4. DfT, Road traffic estimates in Great Britain 2024, by road type. https://www.gov.uk/government/statistics/road-traffic-estimates-in-great-britain-2024/road-traffic-estimates-in-great-britain-2024-traffic-in-great-britain-by-road-type
5. DfT, traffic statistics methodology review, stratification project. https://assets.publishing.service.gov.uk/media/63333774d3bf7f567b3e6207/traffic-statistics-methodology-review-stratification-project.pdf
6. Traffic in Towns (Buchanan, 1963), Appendix 1. https://trafficintowns.uk/index.php/book/appendix1/residential-access-streets
7. Epic forum, "Tutorial: ZoneGraph Quick Start Guide". https://forums.unrealengine.com/t/tutorial-zonegraph-quick-start-guide/573924
8. Epic docs (5.9), Chaos Modular Vehicles overview. https://dev.epicgames.com/documentation/en-us/unreal-engine/chaos-modular-vehicles-overview
9. Epic docs (5.9), Chaos Vehicles. https://dev.epicgames.com/documentation/de-de/unreal-engine/chaos-vehicles
10. Epic docs (5.9), Overview of Mass Gameplay. https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-gameplay-in-unreal-engine
11. Epic forum, "Chaos vehicle fps drop problem". https://forums.unrealengine.com/t/chaos-vehicle-fps-drop-problem/1353155
12. Audiokinetic, interview with Sleeping Dogs' sound team. https://blog.audiokinetic.com/interview-with-sleeping-dogs/
13. Freesound 563021 (CC0). https://freesound.org/s/563021
14. Freesound 425528 (CC BY 3.0). https://freesound.org/s/425528
15. Freesound 274460 (CC BY 4.0). https://freesound.org/people/conleec/sounds/274460
16. Project files: canon.md; RULINGS.md; PLAN.md; license-allowlist.md; asset-plan/2-VEHICLES.md; pre-production/4-BUDGETS.md; frame-headroom/PACKING-PLAN-2026-11-16.md; aaa-reference/studies/04-street-world.md and TALKS.md; weapons-spec.md 4.1; tools/lane/car_loft.py and car_loft_blender.py; asset-budgets.json.

## Unreached (never evidence)

- DfT's 1990 flow for urban minor roads (TRA03): not reached.
- Epic's "how to set up vehicles" page (wheel bone rules): search only; the checklist's bone points are [I] until read on the PC.
- Every millisecond for moving cars is an estimate; nothing has been measured on his card. The review's "static meshes 0.6 ms" anchor was not found in 4-BUDGETS, so the measured MetaHuman figure is used instead.
