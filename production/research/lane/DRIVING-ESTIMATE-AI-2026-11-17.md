# Driving estimate for an AI builder: stage 2 arcade car and stage 3 AAA driving (17 November 2026)

Reviewed 17 Nov 2026: PASS WITH FIXES, applied.

Research helper, about twenty minutes. Answers his note of 17 Nov on TRAFFIC-COST-2026-11-17.md: "Seriously doubt 1k-2.5k h. We have to take advantage of our efficiency principle here". Marks: [READ] read at the source today; [SS] search result only; [I] the helper's inference; [M] measured in this project; est. an estimate. Sources at the end, read 17 Nov 2026. Metric and drive names (M1 to M12, D1 to D8) as the shared list and the feel-targets sheet.

## Summary

- Recommended route: a hybrid. Unreal's own physics (Chaos) carries the car's body, its collisions and the world; our own handling model (tyres, steering, brakes, engine, suspension springs) is the browser car's model carried into Unreal as a small C++ part that runs at a fixed step, checked by golden rows exactly as the simulation's port is. Not Chaos Vehicles tuned to match. The decision is confirmed on the PC at stage 2's start with one short trial (section 1).
- Stage 2 (arcade car), on top of the browser feel rounds: est. 100 to 220 hours, most likely about 150. Medium-low confidence. A lean stage 2 (seated by a cut instead of a full get-in) est. 85 to 180.
- The browser feel rounds before it: est. 25 to 45 hours, charged to the browser prototype, not to stage 2.
- Stage 3 (AAA driving), on top of stage 2, for four platforms with one shared interior shell: est. 430 to 900 hours, most likely about 650 (450 to 950 with four full interiors). Low confidence: the biggest parts (damage, police chases, getting in and out) have no measured LEDGER rate yet.
- Both stages together: est. 530 to 1,120 hours, most likely about 800.
- Against the rough figures: stage 2 is about a third below 150 to 300 at the middle (150 against 225). Stage 3 is well below 1,000 to 2,500: its top (900) sits under the old bottom, and its middle (650) is about a third of the old middle (1,750). The old 1,000 to 2,500 did not say "on top of stage 2". If the old figure meant the whole job, the fair comparison is stage 2 plus stage 3: est. 530 to 1,120, still about half the old range. His doubt holds for stage 3. For stage 2 the old range was not far off, because its cost is mostly MetaHuman motion and in-game testing, where LEDGER's measured rates are already AI rates.
- The largest saving is not typing speed. It is that feel is won in the browser in quick rounds, then carried over by a port the project already knows how to prove, so Unreal tuning shrinks to a few check rounds instead of months of tuning by feel.

## 1. The open question: tune Chaos Vehicles (A) or carry the browser model over (B)

### What shipped games did

| Game or source | What it shows | Mark |
|---|---|---|
| GTA V (Rockstar's own engine) | A simplified traction-curve model, not a tyre simulation: "the engine simplifies very complex matters into only sets of two or three variables"; grip given in g; one value acts as the slip angle. Each car is a row of data (power, grip curve, brakes, centre of mass, roll bars). | [READ] modders' published guide |
| Cyberpunk 2077, update 2.0 (2023) | The studio reworked driving in its own engine rather than tuning it: "speed-sensitive steering", "all engines have torque curves now", vehicles feel heavier from how gravity is applied as the suspension moves, "a full pass on adjustments to braking force", better reactions to kerbs. Police chases and AI chases added at the same time. | [READ] CD Projekt's notes |
| Watch Dogs 2 (2016) | Ubisoft brought in Reflections (the Driver studio) to fix the first game's driving; they used their own long-standing handling tool, V-Edit; "we're not delivering a super-realistic thing". | [READ] TechRadar |
| Just Cause 4 (GDC 2019) | Avalanche's own vehicle physics; the talk argues the usual "magic formula" tyre model suits arcade handling less well and proposes a simpler one with fewer values. | [READ] GDC listing |
| Criterion, "Vehicle Feel Masterclass" (GDC 2018) | Sixteen years of handling lessons from one studio: feel is a craft built over many games. | [READ] GDC listing |
| Assetto Corsa Competizione (Unreal 4) | Kunos ran its own physics engine inside Unreal: "it also paired very well with our proprietary physics engine". | [READ] Epic interview |
| Sleeping Dogs, Mafia | No source on their driving code was reached today. | unreached |

Pattern [I]: every open-world game reached uses its own handling model, data-driven per car, usually simpler than real tyre physics and tuned for feel. The one Unreal game reached with serious driving brought its own physics. No shipped open-world game using Chaos Vehicles with a public report on it was found.

### Chaos Vehicles today (Unreal 5.x)

- Epic's own page calls it "Unreal Engine's lightweight system for performing vehicle physics simulations" and says no more about its tyre model or limits [READ, 5.9 docs].
- Creep at rest: a car on flat ground slowly slides forward even with the handbrake on (5.3.2, Feb 2024 to Mar 2025). Friction, damping and centre of mass made no difference; one cause found was thrusters, another floating-point drift far from the world's centre; the only fix was a hand-tuned counter-push; no Epic reply [READ].
- Jitter at rest and on slopes is a recurring forum topic (several threads, 5.0 to 5.7) [SS].
- Clutch: "no torque converter or clutch slip behavior"; the reply agrees "the current clutch system is simple" and points to Modular Vehicles for anything more (July 2025) [READ].
- Tyre model: a 5.5 user wanted to replace the default friction code with a Pacejka formula; no Epic answer [READ]. A 2026 tutorial blog claims 5.7 has a "Pacejka-style formulation" and that a good-feeling car still needs "a physics-literate engineer for 6-10 weeks"; its author shows only a prototype, so this is weak evidence [READ, unverified].
- Fixed step: frame-rate-bound physics makes cars shake or bounce; the fix is Chaos's asynchronous (fixed-step) physics, which a 2025 article uses for its own suspension forces [READ, teaser only].
- Chaos Modular Vehicles (cars built from engine, gearbox, clutch, axle and wheel modules, and from separate breakable parts): needs the mesh split into parts ("a more difficult setup") [READ]. Its commit list from Sep 2025 to Apr 2026 is mostly crash and stale-pointer fixes, all landing "(FINALLY!)" in the 5.8 branch [READ, forum post].

Does 5.8 matter? Only for Modular Vehicles, which become usable there for the first time with eight months of fixes [READ]. 5.8 was released in June 2026 [SS]; its release notes did not load today (unreached), so no 5.8 change to Chaos Vehicles is known. The recommended route does not depend on either.

### The two routes, costed

A. Tune Chaos Vehicles until D1 to D8 give the browser's results.
- Set-up on the kit's skinned hatch: est. 4 to 8 h. Fix creep and jitter: est. 4 to 12 h, with no promise.
- Matching: Chaos has its own tyre, clutch and steering rules, different from the browser's. Matching is curve-fitting a closed box: each round is change values, package, run eight drives, read. Kiln's measure-and-tune rounds took 0.72 to 1.70 h each, median 0.92 [M, 10 rounds]. 15 to 40 rounds: est. 15 to 60 h.
- Some drives may never match (D6 slide and recovery, D7 handbrake, the clutch), forcing custom code anyway.
- Stage 2 handling: est. 25 to 80 h, wide because the end is uncertain. Stage 3 depth (load-sensitive grip, wet, a real clutch) means Modular Vehicles or custom code: est. 60 to 150 h more.

B. Carry the browser model into Unreal, the hybrid way.
- The model is a pure step: (state, inputs, fixed time step) in, new state out, no browser calls. The browser rounds export golden rows from it: the drives' traces and single-rule rows (tyre force against slip, steering ratio against speed, brake force, torque against rpm).
- The C++ copy is a header that compiles without Unreal, checked with g++ against the rows before Unreal sees it: the exact pattern of CoreGolden.h and tools/port-golden-check.sh, which the simulation port already uses [M]. The project's port rate is 0.25 to 1 h a rule with 0 mismatches (RECIPE.md section 10) [M]; port task windows in the time log ran 0.07 to 0.80 h each, median 0.20, helpers' time on top [M, 15 windows]. A handling model of about 15 to 25 rules: est. 4 to 25 h.
- In Unreal: a Chaos rigid body for the car (Chaos keeps collisions, mass and contacts with the world); four wheel ray or shape casts for the ground; our forces applied in the fixed-step physics callback; wheel visuals. Est. 10 to 20 h, the hardest code, given to Fable.
- Two checks: the pure model matches to 1e-6; the in-engine drives match the browser within a tolerance (for example braking distance within 3 percent), because Unreal's ground contact is not the browser's.
- Stage 2 handling: est. 20 to 45 h. Stage 3 depth is more rows in the same model, tuned in the browser first: est. 25 to 60 h.

Recommendation: B, the hybrid. Its cost is bounded and its proof is the method LEDGER already trusts; A starts cheaper but its matching has no known end and its stage 3 path is a rewrite. One cheap guard at stage 2's start: a 3 to 4 h trial on the PC of Chaos's async physics callback on a bare body, to confirm the fixed step and force hooks behave as read; if it fails twice, fall back to A for stage 2 and record it. Chaos Vehicles may still serve hit background cars cheaply, but the same model at low detail is simpler [I].

## 2. LEDGER's measured rates used here

From production/time-log.jsonl (5 Oct to 17 Nov, 28 working days, 387 tasks, 240.5 logged hours, all kinds; the production kind alone 224.9 h) and RECIPE.md:

| Rate | Figure | What it is |
|---|---|---|
| Port with goldens | 0.25 to 1 h a rule; windows 0.07 to 0.80 h, median 0.20 (15) | RECIPE 10; time log, phase 3 port tasks [M] |
| Tuning round | 0.72 to 1.70 h, median 0.92 (10 Kiln rounds) | measure, change, re-run, judge [M] |
| Motion try | 1 to 3.5 h a try | RECIPE 8 (walk, sit) [M] |
| Sitting a MetaHuman on a seat | 12.4 h over 19 windows, median 0.55 | everything named sit or seat [M] |
| Epic's MetaHuman walk route | 3.9 h, set aside after two tries | 24 Oct [M] |
| Camera rows | 5.1 h over 8 windows | the talk camera [M] |
| A fix found by the tester | 0.1 to 0.6 h | RECIPE 12 [M] |
| Performance round | 4 to 12.5 h | RECIPE 11 [M] |
| Stage 1 traffic plan | 85 h counted (38 + 47) | TRAFFIC-COST section 7, est. |
| First-estimate overrun | parked car 12 h became 25 to 41; Ron's garments 10 became 17 to 21; scale-test core 8 became 14 | DECISIONS.md 16 to 17 Nov [M] |

The overrun line matters: guessed items ran 1.5 to 2 times over; counted step-by-step items landed near their count (Kiln M5 counted 41.5 h against its 46 h budget). The ranges below are counted, and their tops carry about 1.5 times the bottoms.

Human-studio ceilings below are est. [I] except where marked: hours a small professional team would spend, given only as an upper bound.

## 3. Stage 2: the arcade car, by component

One platform (the hatch), drivable by the player, chase camera, getting in and out, cosmetic damage, background cars that switch to physics when hit, the simulation noticing the car.

| Component | Reused or generated | Work left | Est. hours | Human ceiling |
|---|---|---|---|---|
| Handling and tyre model | browser model and golden rows; CoreGolden pattern | port, fixed-step forces, wheel casts (section 1, B) | 20 to 45 | 240 to 400 (the blog's 6 to 10 weeks, unverified) |
| Scripted drives in Unreal | feel-targets sheet D1 to D8; the tester's runner | drive inputs, M1 to M10 logging, comparison with the browser's results | 8 to 15 | 40 to 80 |
| Tuning by feel | browser rounds did the tuning | 3 to 6 Unreal check rounds at about 1 h, his short playtest each | 6 to 15 | 150 to 300 |
| Damage | kit's split panels, lamp and glass slots | lamps and glass break, a dirt and scrape layer by impact speed (M11) | 4 to 8 | 40 to 80 |
| Interior | kit item 8, the dark simple interior (charged to the kit) | fitting only | 0 to 4 | 40 to 80 |
| Camera | talk camera's lessons; M10 targets | chase camera: lag, height, field of view by speed, wall avoidance | 6 to 12 | 40 to 80 |
| Engine and road sound | stage 1 car sounds; MetaSounds (Epic's) | rpm-pitched engine, gear change, tyre squeal from slip (M12), impacts | 4 to 10 | 40 to 80 |
| Getting in and out | sitting work, seat spots, CMU capture (allowlisted 12 Nov) | door opens, enter clip or cut, seated pose with hands on the wheel, exit | 20 to 40 | 120 to 240 |
| Traffic interplay | stage 1 follower and lanes | hit cars go physical; followers give way to the player's car; horn | 8 to 16 | 60 to 120 |
| Simulation hooks | stage 1 perception events | reckless driving as a noticeable act; the car remembered (colour, kind); a town task with goldens | 6 to 12 | 40 to 80 |
| Testing | packaged walk, soak, SaveChaos, frame ruler | driving route in the night walk; save and reload in and out of the car | 10 to 18 | 60 to 120 |
| Gate and review | the gate skill | pictures, fresh reviewers | 4 to 8 | 20 to 40 |
| Total | | | 96 to 203, stated as 100 to 220 | about 900 to 1,700 |

Getting in and out is the likely overrun, as the traffic file said: the sit alone took 12.4 h over three weeks, and a car seat in a moving body is harder [I]. The lean version sits the driver by a short cut (door opens, cut, seated), est. 8 to 15 h, and takes stage 2 to 84 to 178, stated as 85 to 180.

## 4. Stage 3: AAA driving, by component

On top of stage 2. Four platforms (est.: hatch, saloon, van, police car), each a shared body base with trims. The bar is the outside study of Mafia and GTA: their behaviour measured from footage, never their files.

| Component | Reused or generated | Work left | Est. hours | Human ceiling |
|---|---|---|---|---|
| Handling depth | the same model, extended in browser rounds first | load-sensitive grip, combined slip, wet (from the saved wetness value), surfaces, clutch and gearbox, no ABS (1990) | 25 to 60 | 1,000 to 2,000 |
| Platforms' handling | kit weight and size data per platform; data-driven rows like GTA's | one row set per platform from its measurements | 12 to 24 | 200 to 400 |
| Tuning by feel | per-platform targets; drives in every nightly build | 4 to 8 rounds per platform at about 1 h, his playtests | 15 to 40 | 400 to 800 |
| Damage and deformation | kit's even panel topology, hinge pivots, split panels | dents that deform panels, doors and bonnet that hang and fall, glass, steering pull and smoke, damage saved | 60 to 120 | 2,000 to 4,000 |
| Interior per platform | the interior slot; car kit and loft scripts | first-person view; one shared shell with per-platform dashboard, seats and trim; working gauges | 25 to 50 (shared shell) or 40 to 100 (four full) | 800 to 1,600 |
| Camera | stage 2 camera | bonnet and interior views, chase framing, crash and pursuit cameras | 15 to 30 | 200 to 400 |
| Engine and road sound | procedural engine from rpm, load and throttle | layered intake, exhaust and gearbox per platform; tyres per surface and wetness; inside muffling; pass-bys | 30 to 60 | 600 to 1,200 |
| Getting in and out | stage 2's work; CMU capture; seat spots | both sides, driver and passenger, hands on wheel and gear lever, per platform seat fit | 50 to 100 | 1,000 to 2,000 |
| AI drivers who react [I] | stage 1 lanes and follower; stage 2 physics switch; the handling model at low detail | drivers who brake, swerve, give way, hoot and pull over for a police car; physics on contact | 40 to 80 | 1,500 to 3,000 |
| Police chases [I] | AI drivers; the town's police and perception | pursuit driving, a search pattern after sight is lost, roadblocks, losing the police, the town's simulation knowing the chase (the second biggest item) | 50 to 100 | 2,000 to 4,000 |
| Pedestrians reacting to cars | stage 1 giving way; the walk and idle clips; perception events | people stepping back from the kerb, jumping clear, shouting after a fast car | 10 to 20 | 150 to 300 |
| Lights and weather on the player's car | kit lamp sockets and lens slot; the saved wetness value; stage 1 night lamps | headlamps that light the road with unshadowed lights or a projected light pattern (no shadow-casting lamps, as TRAFFIC-COST rules), measured within the 1.4 ms night spare; brake and indicator lamps; police lamps and siren; spray and splash on a wet road; rain on the windscreen and wipers; mirrors drawn cheaply at a low rate | 25 to 50 | 400 to 800 |
| Simulation hooks | town's perception and the Ledger | car as evidence: part of the plate, colour and kind remembered; police know the car; parking and hit-and-run consequences; town task with goldens | 20 to 40 | 200 to 400 |
| Testing | stage 2 drives and walks | AI-car soak, SaveChaos with cars, drives in CI nightly | 30 to 60 | 400 to 800 |
| Performance | frame ruler, packing plan | several physics cars inside the budget; 2 to 4 rounds of 4 to 12.5 h | 10 to 40 | 200 to 400 |
| Gate and his reviews | the gate skill | per platform and per feature | 15 to 30 | 100 to 200 |
| Total | | | 432 to 904 (shared shell), stated as 430 to 900; 447 to 954 (four full interiors), stated as 450 to 950 | about 11,000 to 22,000 |

Police chases and damage carry most of the uncertainty: no LEDGER rate exists for either, so their ranges are judgement from the stage 1 follower's count and the port rate [I].

## 5. Assumptions

1. The browser prototype exists, its handling model is a pure fixed-step step function, and its feel rounds (est. 25 to 45 h) end with him content before stage 2 starts.
2. The hybrid's trial (section 1) passes: Chaos's fixed-step callback accepts our forces at a steady step on the PC.
3. The car kit's checklist (TRAFFIC-COST section 5) was followed: wheel bones, split panels with hinges, even topology, the interior slot, sockets, weight and size data.
4. Hours are builder hours as the time log counts them, helpers charged to the item. Packaged builds and the night walk run in their usual slots; waiting for them is not counted.
5. Fable writes the fixed-step integration, damage deformation and pursuit AI, at its price (US$0.267 a step on 17 Nov, against US$0.075 for Opus helpers, DAILY-2026-11-17) [M].
6. His playtests are short (10 to 15 minutes) and one per round; nothing waits on them (CLAUDE.md).
7. Four platforms at stage 3. Each extra platform adds est. 25 to 50 h (handling row, tuning, interior trim, seat fit, sound layer).
8. Car-jacking and running people down are canon and menace questions for him, not costed here. People getting out of the way of cars is costed (its own stage 3 row).
9. The overrun rule: tops are about 1.5 times bottoms, from the measured overrun of guessed items.

## 6. What would lower the numbers further

- More feel rounds in the browser first: each browser round is minutes to run, an Unreal round is about an hour with a package. Moving 10 Unreal rounds to the browser saves est. 8 to 15 h across the stages.
- Fable on the hardest code only (fixed-step forces, deformation, pursuit AI): fewer failed tries; two tries then research still holds.
- The model written once in C# in the Core's style: the Core already runs in the browser through .NET WebAssembly (SIM-IN-BROWSER-2026-11-17.md), and the C# golden table plus the C++ port is the existing pipeline. Saves a hand copy and its drift, est. 5 to 10 h; needs the .NET-in-the-browser licence line he has been asked about.
- One shared interior shell for all platforms, with per-platform dashboards: saves est. 15 to 50 h.
- Reuse across platforms: platforms as rows of data plus kit lofts, not hand work. The fourth platform should cost a third of the first [I].
- Lean getting in and out: a cut for stage 2 (saves 12 to 25 h); full clips only for the driver's door at stage 3, passenger by cut (saves est. 20 to 40 h).
- Damage by stage instead of free deformation: four authored damage states per panel swapped by impact (saves est. 30 to 60 h, looks less AAA).
- Police chases kept short and local to the map (a few streets), not motorway pursuits: the map is small.
- Procedural engine sound from one synth with per-platform values: it needs no recordings, so the CC0-only sound rule is met by having nothing to license.
- Not shown here as a saving: tuning by feel cannot be skipped. It is the biggest risk in both stages and it is won by rounds with him, not by code.

## Sources (all read 17 Nov 2026 unless marked)

1. Epic docs (5.9), Chaos Vehicles. https://dev.epicgames.com/documentation/unreal-engine/chaos-vehicles
2. Epic forum, "Issue with Chaos Vehicle constantly moving/sliding a tiny bit forward no matter what" (5.3.2, 2024 to 2025). https://forums.unrealengine.com/t/issue-with-chaos-vehicle-constantly-moving-sliding-a-tiny-bit-forward-no-matter-what/1671087
3. Epic forum, "Realistic Vehicle Simulation: ChaosVehicle vs Chaos Modular Vehicle?" (July 2025). https://forums.unrealengine.com/t/realistic-vehicle-simulation-chaosvehicle-vs-chaos-modular-vehicle/2608108
4. Epic forum, "chaos vehicle dynamics tire model" (5.5, Sep 2025). https://forums.unrealengine.com/t/chaos-vehicle-dynamics-tire-model/2653655
5. Epic forum, "Chaos Modular Vehicle: please Epic give us some light", post 13 (commits Sep 2025 to Apr 2026, 5.8 branch). https://forums.unrealengine.com/t/chaos-modular-vehicle-please-epic-give-us-some-light/2654488/13
6. StraySpark, "Chaos Vehicles masterclass: shipping a racing game 2026" (unverified, prototype only). https://www.strayspark.studio/blog/chaos-vehicles-masterclass-shipping-racing-game-2026
7. F. Grenoville, "Taming Chaos: stable vehicle suspensions with async physics in UE5", DEV teaser (Sep 2025). https://dev.to/fgrenoville/taming-chaos-stable-vehicle-suspensions-with-async-physics-in-ue5-319l
8. CD Projekt, Cyberpunk 2077 Update 2.0 notes. https://cyberpunk.net/en/news/49060/update-2-0
9. TechRadar, "How the developers of the Driver series are turning their hand to Watch Dogs 2". https://www.techradar.com/news/gaming/how-the-developers-of-the-driver-series-are-turning-their-hand-to-watch-dogs-2-1325821
10. GDC 2019 listing, Hamish Young, "Vehicle Physics and Tire Dynamics in Just Cause 4". https://gdconf.com/news/get-under-hood-just-cause-4s-vehicle-physics-gdc-2019
11. GDC Vault, Matthew Harris (Criterion), "Vehicle Feel Masterclass" (2018). https://gdcvault.com/play/1025383/Vehicle-Feel-Masterclass-Balancing-Arcade
12. Epic interview, Assetto Corsa Competizione (2019). https://www.unrealengine.com/developer-interviews/assetto-corsa-competizione-leans-into-realism-to-create-the-ultimate-racing-sim
13. eddlm, GTA V handling guide (modders' published analysis). https://eddlm.github.io/Handling-Tools/guide
14. Epic forum, "Talks and Demos: Driving Around: Exploring Chaos Vehicles" (2022). https://forums.unrealengine.com/t/talks-and-demos-driving-around-exploring-chaos-vehicles/547903
15. [SS only] Epic forum threads on Chaos Vehicle jitter at rest and on slopes; GameFromScratch "Unreal Engine 5.8 Released"; Wccftech on Watch Dogs 2 moving from simulation to arcade driving.
16. Project files: production/time-log.jsonl (durations computed today); RECIPE.md sections 8, 10, 11, 12; DECISIONS.md 16 to 17 Nov; production/research/token-audit/DAILY-2026-11-17.md; production/research/lane/TRAFFIC-COST-2026-11-17.md, SIM-IN-BROWSER-2026-11-17.md, CAR-METHOD-LANDSCAPE-2026-11-17.md; ue-probe/Source/LedgerProbe/Public/CoreGolden.h; tools/port-golden-check.sh; tools/lane/car_kit.py; ledger-v2/research/license-allowlist.md (items 3, 8, 11).

## Unreached (never evidence)

- Unreal 5.8 release notes: the page loaded empty. No 5.8 Chaos Vehicles change is known.
- Mafia: The Old Country's Epic interview: refused by the site. Sleeping Dogs' driving: no developer source found.
- The full Grenoville article (only its teaser loaded).
- No shipped open-world game with a public report on using Chaos Vehicles was found.
- Chaos Vehicles' default tyre model: not stated in any source read; the engine source on the PC would settle it.
