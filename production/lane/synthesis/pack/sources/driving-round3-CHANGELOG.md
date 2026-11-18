# Quay Run: changelog

## Round three, 18 November 2026

Round two made the car measurable and met all 28 targets of the "ordinary" set (telemetry digest 165dc939). Since then the direction changed: LEDGER is not a driving sim. Its cars should feel fun and easy first, the way open-world games that are not sims do it: more grip, quicker turn-in, shorter braking, forgiving slides. The 1990 character comes second, carried by the engine sound, the body sway, the look, and an ordinary hatch being slow next to a fast car. This round retunes the default car to a new "game" target set and finishes the camera, the sound and the sense of speed (part A), then adds the full driving prototype: on foot, traffic that reacts, damage stages and a police chase (part B).

Round two's test ground, drives D1 to D8, exports, tuning panel, controller support and determinism are kept. What carries over to the real game is still the behaviour the scripted drives measure, never these physics settings.

### Part A: what changed

- `FIRST_TARGETS` in src/targets.js has a third set, "game", and it is the default. "ordinary" and "fast" stay as reference sets. The results screen checks against the chosen set and shows the ordinary set beside it. The numbers are provisional and sit in one block, easy to swap whole.
- The default car is retuned until every number lands inside the game set: about a third more power (0 to 60 in about 11 s), sideways tyre grip up from 0.92 to 0.98 and lengthways from 0.96 to 1.43, wet grip up from 0.63 to 0.72 of dry, yaw inertia down from 1250 to 720 kg m2, the centre of mass down from 0.52 to 0.44 m, softer springs and anti-roll bars so the body still leans and dives, more steering lock (38.5 degrees), quicker steering, anti-lock on the brakes, and a handbrake that lets the rear tyres go in both directions.
- Automatic gearbox and the mild driver aids are the defaults, remembered unless the player changes them (G and K still switch). Mild aids are now three things: gentle traction control, anti-lock brakes (new), and a stability nudge that waits 1.5 s after the handbrake so a handbrake turn can finish.
- The scripted drives measure the car a player gets, so they now run with the mild aids. A switch on the Drives screen reruns them on the bare car; those numbers are in the tables below.
- Tyre model: a wheel that is locked while the road slides under it now grips the same in every direction (it is a block of rubber, not a rolling tyre). A new setting, handbrake drag, sets how much lengthways grip the rear tyres keep while the handbrake is held.
- Two faults found and fixed while tuning the handbrake turn. First, the car's own measure of how far it is sliding read zero when it slid exactly broadside, so the anti-lock took a sideways slide for straight-line braking and let the brakes off for a tenth of a second. Second, lengthways tyre slip was measured against speed along the wheel only; as a sliding car swung through broadside that measure froze and the tyres pushed the wrong way for a moment. It is now measured against the speed of the road under the tyre in any direction. For a rolling tyre the two are the same.
- Chase camera: it keeps out of walls, other cars and lamp posts with a margin, pulling in fast and easing back out; where its own lag would carry it through a corner of a building it follows less late instead. Look-behind on a button (B, or LB). Free look on the right stick, swinging back behind the car about 1.5 s after the stick is let go. The point it looks at follows the body's height only slowly and partly, so kerbs and bumps do not shake the view. It lags a turn slightly and looks a little into the corner. Field of view widens with speed to the game numbers. A light shake starts above 50 mph, and an impact gives a short jolt sized by the impact; one setting turns all shake off. D8 measures distance, height, lag and field of view as before.
- Sound, all made in the page, no outside files: the engine in three layers crossfaded by revs and load (idle, on throttle, off throttle with an overrun burble) from one firing-pulse train, about 28 Hz at idle up to about 210 Hz at the change-up point for a four-cylinder, with a short dip at each automatic gear change; tyre squeal that starts at 80 percent of the grip limit and rises with slip; road noise rising with speed with a wet hiss; wind; impact sounds in four sizes by impact speed (tap, thump, crunch, crunch with glass); separate volume settings for engine, tyres and world.
- Sense of speed without changing real speed: the wider view and the shake, wind and road noise, the camera's lag, and a little motion blur at the edges of the view that can be switched off. No speed lines or other arcade effects.
- Automatic gearbox: with the foot hard down a long way under the power it now goes down two gears at once instead of one at a time. Found on Hill Road (a 1 in 5 climb), where a car asked for power at 20 mph in third lost speed for over a second while it hunted. The published drives never reach that case, so their numbers and the digest are unchanged by it.
- "Save this page to play with a controller" on the menu saves the whole page as one file. Opened in Chrome or Edge, the saved copy sees a controller, which the Claude view does not allow. The Controls screen says which of the four cases applies: blocked in this view, waiting for a button press, in use, or connected in a layout that is not standard.

### Game targets the default car meets: 28 of 28

Automatic gearbox, mild driver aids, default settings. The last column is the bare car, with the aids off.

| Key | Measured | Result | Game target | Ordinary set, for reference | Aids off |
| --- | --- | --- | --- | --- | --- |
| `M1.0_30_s` | 0 to 30 mph | 3.75 s | 3 to 4.5 | 3.6 to 6, inside | 3.75 s |
| `M1.0_60_s` | 0 to 60 mph | 11.22 s | 10 to 14 | 13 to 17, outside | 11.22 s |
| `M2.top_speed_mph` | Top speed | 105.6 mph | 95 to 110 | 90 to 100, outside | 105.6 mph |
| `M2.speed_at_100m_mph` | Speed after 100 m | 49.8 mph | 44 to 52 | 40 to 46, outside | 49.8 mph |
| `M3.brake_30_m` | Braking from 30 mph, dry | 9.53 m | 8 to 11 | 9.5 to 14, inside | 8.43 m |
| `M3.brake_50_m` | Braking from 50 mph, dry | 25.58 m | 22 to 30 | 25.5 to 38, inside | 22.86 m |
| `M3.brake_70_m` | Braking from 70 mph, dry | 48.44 m | 44 to 58 | 51 to 75, outside | 43.96 m |
| `M3.wet_ratio_30` | Wet over dry at 30 mph | 1.42 x | 1.3 to 1.6 | 1.5 to 2, outside | 1.26 x |
| `M3.wet_ratio_50` | Wet over dry at 50 mph | 1.42 x | 1.3 to 1.6 | 1.5 to 2, outside | 1.29 x |
| `M3.wet_ratio_70` | Wet over dry at 70 mph | 1.38 x | 1.3 to 1.6 | 1.5 to 2, outside | 1.29 x |
| `M4.turning_circle_m` | Turning circle, kerb to kerb | 9.33 m | 8.5 to 9.8 | 9 to 10.5, inside | 9.33 m |
| `M5.yaw_63_s` | Step steer: time to 63% of yaw rate | 0.182 s | 0.15 to 0.25 | 0.2 to 0.35, outside | 0.182 s |
| `M5.self_centre_s` | Self-centring: release to under 5% | 0.675 s | 0.4 to 0.9 | 0.6 to 1.2, inside | 0.675 s |
| `M6.roll_deg_at_0_5g` | Body roll at 0.5 g | -4.28 deg | 3.5 to 6 | 3 to 6, inside | -4.28 deg |
| `M6.pitch_brake_deg_at_0_8g` | Pitch at 0.8 g braking | -3.13 deg | 2.5 to 5 | 2 to 5, inside | -2.97 deg |
| `M6.pitch_throttle_deg` | Pitch under full throttle | 2.17 deg | 1 to 2.5 | 0.5 to 2.25, inside | 2.17 deg |
| `M7.front_load_brake_pct_at_0_8g` | Front load share at 0.8 g braking | 76.9 % | 72 to 82 | 75 to 82, inside | 76.8 % |
| `M8.max_steady_lat_g` | Highest steady lateral grip | 0.892 g | 0.82 to 0.92 | 0.7 to 0.85, outside | 0.892 g |
| `M8.recovery_s` | Recovery after counter-steer | 0.417 s | 0.3 to 0.8 | 0.5 to 1, outside | 0.417 s |
| `M9.handbrake_yaw_deg` | Handbrake turn: yaw turned | 136.4 deg | 120 to 180 | 90 to 150, inside | 136.1 deg |
| `M9.handbrake_settle_s` | Handbrake turn: time to settle | 1.450 s | 1 to 1.6 | 1.2 to 2, inside | 1.433 s |
| `M10.cam_dist_m` | Camera distance behind | 5.80 m | 5 to 6.5 | 5 to 7, inside | 5.80 m |
| `M10.cam_height_m` | Camera height | 1.80 m | 1.6 to 2 | 1.6 to 2.2, inside | 1.80 m |
| `M10.cam_lag_s` | Camera position lag | 0.165 s | 0.1 to 0.25 | 0.1 to 0.3, inside | 0.165 s |
| `M10.fov_0_deg` | Field of view at 0 mph | 62.0 deg | 60 to 65 | 60 to 65, inside | 62.0 deg |
| `M10.fov_30_deg` | Field of view at 30 mph | 67.8 deg | 64 to 70 | 62 to 68, inside | 67.8 deg |
| `M10.fov_60_deg` | Field of view at 60 mph | 74.2 deg | 70 to 78 | 66 to 74, outside | 74.2 deg |
| `M10.fov_90_deg` | Field of view at 90 mph | 80.4 deg | 76 to 86 | 70 to 80, outside | 80.4 deg |

Pitch and roll keep their signs in the files (nose up positive, right side down positive); targets are checked by size.

### Game targets it does not meet: none

None. Every targeted number is inside its range.

Against the ordinary set, for reference only: 16 inside, 12 outside. That is expected: the game set asks for a quicker, grippier car than the ordinary set describes.

With the driver aids switched off in the drives (the bare car), 24 of 28 game targets are met. Outside: braking from 70 mph, dry 43.96 m against 44 to 58; wet over dry at 30 mph 1.26 x against 1.3 to 1.6; wet over dry at 50 mph 1.29 x against 1.3 to 1.6; wet over dry at 70 mph 1.29 x against 1.3 to 1.6. Without anti-lock the brakes use more of the tyres' grip (on a wet road the wheels lock), which shortens the dry stops by about a tenth and the wet ones by a little less, so the wet to dry ratio falls.

Closest to an edge of its range: pitch under full throttle (2.17 in 1 to 2.5), recovery after counter-steer (0.417 in 0.3 to 0.8), handbrake turn: time to settle (1.450 in 1 to 1.6), pitch at 0.8 g braking (3.13 in 2.5 to 5). A check that nudges all 67 handling settings at random by up to 3 percent at once (test/robust.mjs) put a number outside its range in 0 of 40 trials.

Character, measured (test/character.mjs): at the limit the front tyres slip 7.8 degrees more than the rear at 0.88 g, so the front lets go first; lifting off mid-corner tightens the path by 10 percent (12 in the wet) with the tail moving 1.4 degrees; power mid-corner opens the path by 20 percent; a 60 mph lane change on the keys swings the tail 11 degrees dry and 12 wet and settles in about 0.9 s. Nothing snaps or spins in these checks.

### What fought, and how it was chosen

1. Braking distance against the handbrake turn's stop. The game set wants 8 to 11 m from 30 mph, which caps straight-line braking at about 1.1 g, and it wants the handbrake turn to settle within 1.6 s, which needs about 1.2 g while the car slides. Chosen: the anti-lock holds each tyre at about three quarters of its grip (about 1.03 g on a dry road, and it leaves room to steer under full braking), while a locked, sliding tyre uses all of its grip. Side effects: a car thrown sideways with its wheels locked stops a little sooner than one braked in a straight line, and with the aids off the dry stops are about a tenth shorter.
2. Highest steady lateral grip against the same stop. Cornering grip may not pass 0.92 g, so sideways tyre grip stays at 0.98, yet the car has to slide to a stop sideways at about 1.2 g. Chosen: the locked-wheel rule. A rolling tyre grips 0.98 sideways; a locked one grips with its lengthways figure (1.43, less what the curve shape takes off once sliding) in whichever direction it slides.
3. Handbrake yaw against handbrake settle. A car that stops sooner has less time to come round, and in a turn the outer rear wheel carries the load, so its drag while locked holds the nose back. Chosen: the handbrake drag setting at 0.7 (the rear tyres keep 70 percent of their lengthways grip while the lever is held, and 29 percent sideways), and a low yaw inertia.
4. Visible lean and dive against staying on four wheels. With game levels of grip and the old centre of mass at 0.52 m, the sliding car went up on its two outer wheels and took about a tenth of a second longer to settle. Chosen: centre of mass down to 0.44 m with softer springs, which keep the lean and the dive inside their ranges.
5. Wet braking ratio against wet grip. The ratio of wet to dry braking distance wants 1.3 to 1.6. Because the anti-lock holds the same share of grip wet and dry, the ratio is simply one over the wet grip factor, so that factor is 0.72 and cannot rise much further without leaving the range.

### Measured, no target (nothing tuned toward these)

| Key | Measured | Result | Game target | Ordinary set, for reference | Aids off |
| --- | --- | --- | --- | --- | --- |
| `M2.top_speed_settled` | Top speed settled inside 150 s | yes | no target | no target | yes |
| `M3.wet_brake_30_m` | Braking from 30 mph, wet | 13.54 m | no target | no target | 10.64 m |
| `M3.wet_brake_50_m` | Braking from 50 mph, wet | 36.43 m | no target | no target | 29.41 m |
| `M3.wet_brake_70_m` | Braking from 70 mph, wet | 67.07 m | no target | no target | 56.60 m |
| `M5.slalom_max_clean_mph` | Slalom: highest clean speed | 34 mph | no target | no target | 34 mph |
| `M5.slalom_yaw_lag_s` | Slalom at 30 mph: steer to yaw delay | 0.042 s | no target | no target | 0.042 s |
| `M8.slide_onset_mph` | Slide onset speed | 43.2 mph | no target | no target | 43.2 mph |
| `M8.slide_onset_lat_g` | Lateral g at slide onset | 0.892 g | no target | no target | 0.892 g |
| `M10.fov_widen_deg` | Field of view widening, 0 to 90 mph | 18.4 deg | no target | no target | 18.4 deg |

In the slalom at 30 mph the car pulls a peak of 0.74 g between the cones, and the script's pure pursuit steering passes 1.1 to 1.4 m wide of them where the path asks for 1.2 m. Highest clean speed 34 mph; with 2 percent less sideways tyre grip it is 32 mph, so read it as a narrow pass.

Braking starts on the row where the car has been steady for 2 s, and steady allows 0.25 m/s either side of the set speed: the dry runs start from 30.34, 50.33, 70.34 mph and the wet runs from 30.34, 50.33, 70.34 mph, each still easing down toward its set speed.

## Part B: the full driving prototype

Everything here runs in the same 120 steps a second as the car, is the same on every run, and has an automatic test (test/partb.mjs for the simulation, test/r3b.mjs for the page).

### What was added

- On foot. A walking figure, third person only. Keys: W and S walk forward and step back, A and D turn, Shift runs. Controller: the left stick walks where it points as seen on screen, A runs. The camera follows the person the way it follows the car, closer and lower, and blends between the two while getting in or out.
- One button gets in and out (F or Enter; Y on a controller). On foot within about two metres of a front door: the last step to the door is walked for the player, then open, sit, close, drive. In the car and stopped: open, step out, close. The car is held on its brakes while its driver is out.
- From the wrong side: both ways were built. The default is slide across (in through the passenger door, over to the wheel), because it is quick and keeps the player moving; "Walk round" is a setting.
- The car has two real front doors now: panels cut out of the body shell and hung on hinges at their front edge, with the opening behind them. The driver in the seat is a separate piece, there only when someone is in the car.
- Traffic that reacts. Drivers keep left, stop at junctions and give way as before, and now also obey one set of traffic lights (added so that there is a red light to run), stop for a person in the road and sound the horn after about 3 s, brake and sound the horn when the player cuts in, swerve a little when braking alone will not avoid a slow crash, and pull in to the kerb and stop for a police car with its lights on.
- A car that is hit goes on to the same full physics as the player's car, then either collects itself and drives on, or stays where it stopped with hazard lights and smoke, by the damage it took.
- A car left standing in a lane (the player's with the player out of it, a wreck, a parked car shoved into the road) is gone round where there is room: drivers stop well back from it, wait until nothing is coming the other way, and pass on the other side. The police car on patrol does the same. Nobody pulls out while the player is standing in the road beside the driver's door, which in a right-hand-drive car parked on the left is the road side. Where parked cars narrow the road, and on the approach to the zebra crossing, nobody goes round: they queue.
- Nobody waits for ever. A driver who has not moved for a minute (a minute and a half near the player's car) with nobody there to see it gives up and is put down elsewhere in town, the way a crashed car already was. The police car on patrol follows the same rule. While the player is watching, they stay where they are.
- Damage in stages, decided by the closing speed at the first touch of an impact and counted in points, for every car on full physics. It shows on the player's car (dents, broken lamps, a hanging bumper, cracked glass, smoke) and is felt (steering pull, lost power, a car that will not go). R still repairs.
- One police car of a made-up town police: a white hatch with a plain blue band, the word POLICE and two blue roof lamps. No real force, crest, motto or colour scheme is copied. It is the player's car with the same settings.
- A chase: started by the test button or by reckless driving in its sight; it follows the path the player drove, tries to stay close, and gives a light nudge when it can. When the player comes past it the other way it turns round in the road. Besides "stopped beside it for 3 s" there are two more ways to be caught, which close the gaps in that rule: stopped in plain sight where the road does not reach, 6 s after the police car has stopped as near as it can get; and on foot, within 8 m of it for 3 s. It never drives at a person. On screen there is only a blue light at the edge of the view, on the side the police car is, while it can see the player. No map. The end of a chase is said in two words ("Caught" or "You got away"), which is there for testing and can go.
- Sound for all of it: other drivers' horns placed by distance and side, a siren, door, footsteps, other cars' crashes heard from a distance, and the player's own engine fading as they walk away from the car.

### On foot, getting in and out

- Getting out: 1.45 s (open 0.4, step out 0.65, close 0.4).
- Getting in at the driver's door: 1.57 s (the last step to the door, then open 0.4, sit 0.75, close 0.4). From 1.1 m away: 1.99 s. The target was 1.5 to 2.5 s.
- From the wrong side. Both were built; the default is slide across: in through the passenger door and over to the wheel, 1.72 s. The setting "Walk round" goes round the nearer end of the car to the driver's door on foot, 5.23 s.
- Getting in is called off by moving away, until the moment of sitting down; a door left ajar swings shut. Getting out is refused while the car is moving. With no room to open the driver's door the player gets out through the other one.

### Traffic that reacts

- Counts: 8 cars driving, 19 parked, 10 people on the pavements, 10 loose crates, one police car. Up to 5 cars on the full physics model at once (the player's, the police car and 3 that have just been hit); everything else runs on rails.
- A person stepping out: the driver stopped 2.4 m short from 16 mph and sounded the horn 2.89 s after stopping, then drove on once the person had gone.
- Cut up by the player: braked from 18 to 0 mph and sounded the horn, touching at 4.4 mph.
- A slow crash coming: moved 1.2 m aside and missed.
- The police car with its lights on: pulled 0.60 m in to the kerb and stopped from 18 mph; the police car passed without touching after 4.2 s and the driver moved off 2.0 s later.
- Hit by the player: the car goes on to full physics, then drives on after 3.0 s (a 3 mph bump) or 5.2 s (a 9 mph dent), or stays for good with hazard lights and smoke (crumpled at 22 mph).
- Traffic lights (one set, at the crossroads of Back Street and Hill Road) so that there is a red light to run. Traffic obeys them.
- The player's car left standing in a lane, with the player out of it, is treated as one more parked car. On an open street a driver stops about 5 m back (a car cannot move sideways without moving forward), waits until nothing is coming the other way for 60 m and nobody is about to turn in, and goes round 2.8 m out from the lane's line. In the test 3 drivers went round it in 173 s, the first after 100 s; nobody waited more than 14 s and nobody touched it or sounded a horn at it. The police car on patrol does the same (first after 162 s). Wrecks and cars shoved into the road are gone round the same way.
- Getting out of a right-hand-drive car on the left of the road puts the player in the road, 1.4 m out from the middle of the car. While they stand there nobody pulls out past them (2 drivers waited behind for 150 s in the test); 5 s after they reached the pavement the first driver was past the car.
- Where there is no room, nobody goes round: beside parked cars (they already narrow the road to one line) and on the approach to the zebra crossing. Drivers queue behind the car. Nobody waits for ever: a driver who has not moved for 60 s with nobody there to see it (90 s within 45 m of the player's car) gives up and is put down elsewhere in town, the way a crashed car is. In the test the first gave up after 124 s and 2 did in 240 s. While the player is watching they stay: 4 cars queued and the longest wait was 206 s when the test ended.
- A person standing in the road stops the police car as well: on patrol it braked from 19 mph and stood 2.5 m short.

### Damage stages

The stage is decided by the closing speed at first touch (how fast the car and what it hits come together), not the road speed.

| Scene | Closing speed, mph | Stage | Speed before, mph | 0.15 s after (0.3 s for the wall), mph | Lost |
|---|---|---|---|---|---|
| square into a parked car | 2.8 | no damage | 2.8 | 0.4 | 86% |
| square into a parked car | 9.9 | dented | 9.9 | 4.7 | 53% |
| square into a parked car | 21.8 | crumpled | 21.8 | 9.5 | 56% |
| square into a parked car | 39.7 | will not drive on | 39.7 | 17.2 | 57% |
| glancing along a wall at 5.7 degrees | 3.0 | no damage | 29.9 | 29.0 | 3% |
| glancing along a wall at 19.5 degrees | 10.0 | dented | 30.0 | 22.7 | 24% |

- Crumpled: the steering pulls 0.9 degrees at the wheels toward the damaged side (hands off at 30 mph the car is 2.1 m off line after 2 s) and a hit on the nose leaves the engine at 88%.
- Will not drive on: from about 35 mph in one hit, or 8 dents, or 3 crumples, or a mix (a dent is 1 point, a crumple 3, the end is at 8).
- The body shows it: dents sized by the closing speed, lamps break near a dent, a crumple hangs the bumper at that end and cracks the glass, smoke from the bonnet. R repairs.

### Police chase

- Starts from the test button (Y, or the menu), or from reckless driving where the police car can see it: hitting a car at 5 mph or more, running the red light, or passing within 30 m at more than 45 mph. It sees up to 75 m where no building is in the way.
- The police car is the player's car with the same settings, automatic gearbox and mild aids. It follows the path the player drove, corners at about half the grip the car has, and plans its speed so that it can stop when the player does.
- Caught: stopped within 9 m of it for 3 s, or the car will not drive on and it arrives. Scripted, standing still: caught after 5.2 s. Wrecked 57 m ahead of it: caught at 14.8 s.
- Caught, the other ways. Held up: the police car has stopped with the player in plain sight within 40 m (a kerb, traffic or a car left in the way between them) and the player is not moving either; after 6 s that counts. Scripted, the player stopped on the quay 14 m from where the road goes: caught at 13.9 s. On foot: within 8 m of the police car for 3 s. It comes by the road, draws level with a person on the pavement and stops; it never drives at them (scripted: caught at 4.9 s, its bodywork never nearer than 5.9 m).
- Doubling back does not shake it off: when the player comes past the other way it turns round in the road, a three-point turn at walking pace, where the road is clear of junctions and parked cars. Scripted: the turn began 7.1 s into the chase, took 5.7 s, and the player, who had stopped 40 m up the road, was caught at 26.8 s. Where it cannot turn it goes round the block.
- In traffic it does not barge. It waits for anyone already crossing a junction, passes drivers who have pulled in for it on the crown of the road, slows to walking pace if its own corner would clip one, and goes out onto the other side of the road only when nothing is coming there.
- Escape: out of its sight for 20 s. Out of sight it drives to where it last saw the player and on the way they were going, inside an area that shrinks as the 20 s run out. Scripted, flat out on a dry road: last seen at 5.7 s, escaped at 25.7 s.
- The nudge: on a straight, behind a player holding a steady speed, it closes up and touches at walking pace. Scripted at 20 mph: touched at 2.5 mph after 5.9 s; the player went from 19.8 to 20.9 mph and stayed straight.
- 54 chases with the demo driver standing in for a player, at three levels of pace on three roads, 180 s limit: 39% escaped, 39% caught, the rest were still going. Typical time to escape 26 s, to be caught 56 s. 58 nudges, the hardest at 3.4 mph (dents start at 5).

| Driver | Road | Chases | Escaped | Caught | Still going | Typical length, s | Gap while in sight, m | Nudges |
|---|---|---|---|---|---|---|---|---|
| steady | dry | 6 | 1 | 3 | 2 | 45 | 34 | 5 |
| steady | damp | 6 | 1 | 2 | 3 | 159 | 13 | 22 |
| steady | wet | 6 | 0 | 3 | 3 | 150 | 13 | 14 |
| brisk | dry | 6 | 4 | 2 | 0 | 27 | 50 | 0 |
| brisk | damp | 6 | 1 | 3 | 2 | 53 | 39 | 7 |
| brisk | wet | 6 | 2 | 3 | 1 | 76 | 28 | 5 |
| flat out | dry | 6 | 6 | 0 | 0 | 26 | 54 | 0 |
| flat out | damp | 6 | 3 | 2 | 1 | 70 | 46 | 4 |
| flat out | wet | 6 | 3 | 3 | 0 | 68 | 45 | 1 |

The demo driver never stops of its own accord and never doubles back, so "caught" here means held up by traffic with the police car behind, and "still going" means the police car stayed on its tail to the time limit. A person will do better and worse than this in ways the table cannot show.

### Cost

- The simulation alone, in Node on the build machine: 22 ms of work per second of play with the police car on patrol, 18 ms in a chase. That is 0.30 ms of a 16.7 ms frame.
- Drawing adds one police car, one figure on foot, two doors and four light poles to the round two picture. The frame time on a real PC is not measured here: "Measure frame time" in Settings does it, and its second lap now runs with the police car chasing.

### What fought in part B, and how it was chosen

1. "About 30 to 60 percent of speed lost" in a dent, against what a collision does. Square into a car of the same weight, half the speed goes by momentum alone, which is inside the range. A wall takes all of the closing speed, and a glancing hit takes about a fifth. Chosen: the collisions stay physical, the stage is decided by closing speed, and the table above shows all three cases.
2. A light nudge against never denting the player. Closing up gently takes several seconds of straight road at a steady speed, and a player who brakes turns a gentle touch into a dent. Chosen: the police car plans for the speed the player will be doing in a moment, closes the last metres at under 3 mph, and gives the nudge up when the player brakes. The cost: nudges are rare, most of all on a dry road where a quick driver is always speeding up or slowing down.
3. Staying close against running into the back of the player. The first version closed the gap as fast as a simple rule allowed and hit the player at up to 22 mph on a wet road. Chosen: it never closes faster than it could brake off again in the room it has, planning with a third of the braking the car can really do.
4. The same car against being possible to escape. With the same power and grip it is as fast as the player on the straights; if it also cornered and braked as hard, nobody would get away. Chosen: it takes bends at a little under half the grip and brakes early. Both numbers (CORNER_G and A_PLAN in src/police.js) were set against the demo driver, not by hand.
5. Pulling in for the police against being in its way. A driver who pulls in and stops is still in the police car's lane. Chosen: the police car goes past on the crown of the road, and oncoming drivers pull in as well.
6. Traffic lights a driver can see. Beside the stop line the poles stood round the corner of the buildings from the drivers they are for. Chosen: the poles stand at the building line, two metres before the stop line, and each lamp has a hood with cheeks so that the side street's lights do not show.
7. Going round a car left in the road against meeting someone head on. Rail traffic cannot reverse, so two drivers nose to nose in one lane stay there. Chosen: a driver goes round only when the other side is clear for 60 m and nobody is about to turn into it (the police car's route counts, from further off when its lights are on); once properly out it carries on, because a car cannot move sideways standing still; and the driver coming the other way holds back 14 m and leaves room beyond the obstruction as well. Drivers go 2.8 m out from the lane's line, which leaves a metre beside the car they pass. Where parked cars narrow the road, or the zebra crossing is ahead, nobody goes round at all.
8. Never jamming for ever against never cheating in view. Some knots cannot be untied by driving. Chosen: the give-up rule above, which only acts where the player cannot see it. The cost: a queue behind the player's own car, beside parked cars, stays for as long as the player looks at it.
9. The police car in tight places. Leaving it among traffic for hours (test/soakb.mjs), with a chase called every minute beside a car left in the road, found three faults, now fixed. It could not back off while its lane driver held the wheel: the lane driver asked for first gear every time the car asked for reverse, so it sat still. The test button could put it down at 18 mph on top of a junction, or in the path of a driver going round something. And a chase that ended out on the crown of the road left it wedged between the queue and the car. It now looks behind before backing, makes room behind a car it has stopped too close to (straight away in the pause after a chase, before a queue forms), waits for a gap like any other driver, and if it is already out beside the car it carries on round. In a chase it goes onto the other side of the road only when nothing is coming there, and near something it is steering round it looks along the line the car is really on, so its own corner is not swung into a driver who has pulled in for it.
10. A look ahead that measured along the car instead of along the road. "Is the other side clear" looked down a strip set by the way the car was pointing; a driver standing at a slight angle looked down the wrong strip and pulled out in front of the police car. It is measured along the lane now, and a car on the crown of the road counts as being in the way.

### Left running

Beyond the scripted checks, the town was left to itself for hours in Node (nothing drawn), to look for jams, wedged cars and camera faults. The numbers of the final build:

- Traffic alone (test/soak.mjs), 25 minutes: nobody stood still for more than 15 s.
- Traffic with the police car, a chase called every minute against a player who stays put (test/soakb.mjs), 15 minutes in each of six set-ups, 15 chases each:

| Where the player's car is | Road | Stops of 45 s or more | Longest stop, s | Drivers who gave up | Police car went round the car | Caught |
| --- | --- | --- | --- | --- | --- | --- |
| On the quay, off the lanes | damp | 0 | 20 | 0 | not in its way | 15 of 15 |
| On the quay, off the lanes | wet | 0 | 19 | 0 | not in its way | 15 of 15 |
| In a lane on an open street | dry | 0 | 19 | 0 | 6 times | 15 of 15 |
| In a lane on an open street | damp | 0 | 24 | 0 | 3 times | 15 of 15 |
| In a lane beside parked cars | dry | 31 | 90 | 13 | no room | 14 of 15 |
| In a lane just past the zebra crossing | dry | 25 | 90 | 12 | no room | 15 of 15 |

  In all six the police car never touched anything at 5 mph or more, was never damaged and never had to be put down elsewhere. The last two rows are the give-up rule doing its job: there is no room to go round, so drivers queue, and nobody waits longer than 90 s unseen.
- The camera (test/camsoak.mjs), 40 minutes of laps, 18 of them with the police car on the player's tail: never inside a wall, a car or a post, and no jump of more than 0.35 m in one step (the largest was 0.30 m).
- The demo driver on many routes (test/fuzz.mjs), two hours: one contact, at 3 mph, when it ran into the back of a car that stopped for the lights.

### What does not feel right yet

- Nobody has driven this tune by hand or played part B. Every number here comes from scripted drives and automatic checks. The feel, the sound by ear, a real controller and the frame rate on a real PC are still to be judged by a person.
- The low yaw inertia that the handbrake numbers ask for may feel darty on the keys at speed. The 60 mph lane change on the keys stays under control in the checks, but that is the first thing to try by hand.
- A sideways slide with locked wheels stops sooner than straight braking. That follows from the provisional numbers and may feel odd.
- The engine layers are synthesis, not recordings: correct in pitch and behaviour, plain in tone.
- Getting in and out: the timing is as asked, the look is plain. The figure is made of boxes, its hands do not reach the door, and it passes through the sill a little as it sits.
- The chase is all or nothing. While the police car can see the player, a steady driver does not shake it; once it has lost sight it rarely finds the player again, because its search is simple. The overall escape rate hides that split. This is the part most in need of a person's hands.
- "Caught" only ends the chase. Nothing follows from it; the police car moves off on patrol again a few seconds later.
- Traffic that is hit shows no dents, only hazard lights and smoke, and neither does the police car. A wrecked car stays where it stopped until the player is out of sight and 60 m away, so several wrecks at one junction can block it for a while.
- A person on foot cannot be hurt. Traffic stops for them, and a car that slides into them pushes them aside.
- A car left in a lane beside parked cars, or just before the zebra crossing, blocks that lane. Nobody goes round, nobody sounds a horn at an empty car, and the queue only clears when the player moves the car or stops looking. That is honest about the room there is, but it may look as if the traffic has stopped thinking.
- On foot the chase is thin. The police car comes by the road, stops level with the player and that is "Caught"; out of its sight for 20 s is "You got away". Nobody gets out of the police car.
- In heavy traffic the police car is patient to a fault: it waits for junctions to clear and for a gap before going round anything, which costs it seconds a player can use.
- The demo driver, which stands in for a player in the chase statistics and drives the frame-time laps, follows traffic too closely: in two hours of unattended laps it ran into the back of a car that stopped for the lights once, at 3 mph.

### Not in this round, as agreed

A full interior (the camera is third person only), weapons from the car, more than one police car at once, and new car models: the police car is the player's hatch in another livery, and traffic uses the four body styles it already had.

### What could not be done, and why

- No hand driving, no walking about by hand, no real controller and no listening. There is no person in the loop here, and the PC this chat is linked to is the LEDGER machine, which is not operated from here.
- No frame rate on a real PC. The build machine draws in software, which says nothing about a graphics card. "Measure frame time" in Settings measures it on the machine it runs on; its second lap now includes the police car chasing with its lights on.
- No chase statistics for a person. The demo driver stands in at three levels of pace. It never stops, never doubles back and is cautious on a wet road, so the table is a guide to the balance and no more.

### The published run

- Default settings, automatic gearbox, mild driver aids, target set "game", 16 telemetry files, 65476 physics steps.
- Telemetry digest: 53053f08. Run all drives on the page with the default settings and the results screen shows the same digest if every row of every file is identical.
- Files: round3/results.json, round3/settings.json, round3/telemetry/<run>.csv, and this note. Round two's files stay under round2/.
