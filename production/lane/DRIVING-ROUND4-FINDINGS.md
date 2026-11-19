# Driving study, round 4: what a clumsy newcomer finds

19 Nov 2026

## What was run

A new automatic tester (tools/lane/driving-gate) played a saved copy of the round 3 page twice, keyboard first, then a pretend controller. It crashed into walls, bollards, a lamp post, parked cars and traffic at about 10 to 40 mph (16 crashes a run), reversed out, got out and in, wedged the car at full lock, pressed random keys, paused, resumed and reset. It ran the game's own physics, not real time on a real PC.

## The seven checks

1. Never stranded: FAIL. After a 41 mph hit on a traffic car and a 37 mph hit on a lamp post the car moved under 0.1 m on reverse and throttle. Only R mended it. Backspace put it on the road still dead (0.04 m) while saying "Back on the road". Four smaller hits (10 points) stranded it the same way. Once, after random keys, the undamaged car stuck until Backspace. Getting out and walking always worked.
2. Damage told: FAIL. Dents and crumples (5 to 30 mph) never show words. "The car will not drive on. R repairs it." shows for about 3 s after one big hit, then nothing. A car killed by smaller hits gets no message. The controller has no repair button.
3. Smooth on keys: PASS. Holding A takes the input to full in 0.17 s (10 frames); yaw builds over about 0.4 s, at most 0.04 rad/s a frame. One 0.16 rad/s jump not at a key change, probably a kerb, unconfirmed.
4. Smooth on pad: FAIL. Letting go of the stick at 30 mph swings the front wheels to about half opposite lock within 2 to 3 frames. Yaw jumps of 0.23 rad/s in a frame at stick 0.6 and 1.0, cause unconfirmed.
5. Camera clear: PASS. Never inside a wall or car in any step; no crash picture was one flat colour (largest 28 percent).
6. No errors, nothing frozen: PASS. No page errors except the blocked fonts. Pause and resume by Esc and by Start worked. The only frozen spells (up to 4.5 s) were the stranded cars.
7. Person hurt, never killed: NOT REACHED. The car met a lamp post or missed. The page's notes say a person cannot be hurt, only pushed aside.

## The owner's complaints

(a) Stranded by one hit on a pole: CONFIRMED at 35 mph and over, refuted below. Bollards at 12 and 17 mph left the car drivable; a lamp post at 37 mph killed it until R. Cause: damage.js Damage.hit sets power to 0; main.js handle sends Backspace to sim.recover, which does not mend; the only message comes from main.js afterStep, for one big hit only; input.js PAD_EVENTS has no repair.

(b) Keyboard steering jerky: NOT CONFIRMED as a snap. What may feel jerky: keys steer all or nothing (full lock in 0.17 s), and on letting go the driving help swings the wheels to a third of opposite lock for 0.15 s (vehicle.js handSteer, self-centring). On the stick it is quicker and bigger.

## Fixes, most important first

1. Never strand: Backspace also mends, or the wreck limps at walking pace. Gate: 0.5 m of movement within 5 s of every crash, no hidden key.
2. Repair on the controller, message worded for the device. Gate: a controller wreck recovers with pad buttons only.
3. A lasting line while the car is dead, however it got there. Gate: the line present in every dead row.
4. Damage stage in words after each dent or crumple. Gate: a message within 1 s of every hit over 5 mph.
5. Soften the opposite-lock swing on release. Gate: car steering changes under 0.15 of lock a frame after letting go.
6. Find the yaw jumps. Gate: same check with kerb contact logged.
7. Gate's own: stop without holding S (it reverses and blocks getting out); a clear run at a pedestrian; a controller crash over 35 mph.
