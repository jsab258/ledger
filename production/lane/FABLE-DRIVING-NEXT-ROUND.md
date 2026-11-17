# Fable driving study: next round prompt (17 November 2026)

For Jafar: paste everything below the line into the same Fable chat, after round one is finished. Nothing above the line needs pasting.

---

Fable, this is round two of the driving study. Round one gave the car simple driving. This round makes that car measurable and tunable, so its behaviour can later be matched by the real game's car in Unreal. What carries over to Unreal is behaviour measured by fixed scripted test drives, never your physics settings, because the same settings feel different in a different physics engine. So the drives, the numbers and the export format below matter more than anything else this round.

## First

Read your round one code and keep what works. Change it only where this round needs it. Do not start again from nothing.

## Project facts

- Britain, 1990. Left-hand traffic: cars keep to the left side of the road. Right-hand-drive cars: the driver sits on the right.
- Speeds in mph on screen; distances in metres.
- No real car brands or models, in names, badges or shapes. The car is an ordinary fictional small family hatchback of the period.
- No alcohol or gambling, shown or spoken of. No children anywhere.

## What to build this round

### 1. Tune the car toward the first targets

The default car is an ordinary 1990 small family hatchback: tune it to the ordinary set. Put both sets in the code in one clearly named block, `FIRST_TARGETS`, with a comment saying "first targets from the feel-targets sheet (game band: the real range widened by the allowed game departures); replace whole when the sheet changes". Keep it in one place so it can be swapped whole. A setting chooses the set by name ("ordinary" by default, or "fast"), and the results screen checks against the chosen set. Tune the default car until every number lands inside the ordinary set.

```
FIRST_TARGETS, set "ordinary" (the default car)
M1   0 to 30 mph                                   3.6 to 6.0 s
     0 to 60 mph                                   13 to 17 s
M2   top speed                                     90 to 100 mph
     speed after 100 m from standstill             40 to 46 mph
M3   braking distance, dry, full brake, braking only (no thinking distance)
       from 30 mph                                 9.5 to 14 m
       from 50 mph                                 25.5 to 38 m
       from 70 mph                                 51 to 75 m
     wet braking distance as a multiple of dry     1.5 to 2.0 (each speed)
M4   turning circle, kerb to kerb                  9.0 to 10.5 m
M5   steering: time to 63% of settled yaw rate
       after a step steer at 30 mph                0.20 to 0.35 s
     self-centring: release to yaw rate under 5%   0.6 to 1.2 s
M6   body roll at 0.5 g steady cornering           3 to 6 deg
     pitch at 0.8 g braking                        2 to 5 deg
     pitch under full throttle                     0.5 to 2.25 deg
M7   front load share at 0.8 g braking             75 to 82 %
M8   highest steady lateral grip (40 m circle)     0.70 to 0.85 g
     recovery after counter-steer                  0.5 to 1.0 s
M9   handbrake turn from 30 mph: yaw turned        90 to 150 deg
       time for the turn to settle                 1.2 to 2.0 s
M10  camera: distance behind                       5 to 7 m
     camera height                                 1.6 to 2.2 m
     camera position lag                           0.1 to 0.3 s
     field of view at 0 mph                        60 to 65 deg
     field of view at 30 mph                       62 to 68 deg
     field of view at 60 mph                       66 to 74 deg
     field of view at 90 mph                       70 to 80 deg

FIRST_TARGETS, set "fast" (a 1990 fast hatch; everything not listed as "ordinary",
except 0 to 30 and speed after 100 m, which have no target in this set)
M1   0 to 60 mph                                   8 to 9 s
M2   top speed                                     118 to 122 mph
M3   braking from 30 / 50 / 70 mph                 8.5 to 12 / 24 to 33 / 47 to 65 m
M6   body roll at 0.5 g                            2 to 4.5 deg
M8   highest steady lateral grip                   0.82 to 0.90 g
```

Pitch and roll targets are sizes: the sign is ignored when checking. The export keeps its signs (pitch nose up positive, so braking pitch is negative; roll right side down positive), and the results compare the size, as our tool does.

Every other number the drives produce (wet distances in metres, slalom, slide onset speed, widening of the field of view) has no target yet: measure it, show it, export it, but do not tune toward it.

### 2. Fixed physics step and repeatable results

- Physics runs at a fixed 120 steps a second, separate from drawing. Each frame, run as many 1/120 s steps as the time owed, carry the remainder over, and cap the steps per frame so a slow frame cannot spiral.
- Drawing runs at 60 fps; keep it there.
- Deterministic: the same drive gives exactly the same numbers on every run. No random numbers in the physics or the drives; no use of frame time inside the physics; start every drive from the same reset state.

### 3. Scripted test drives D1 to D8, from a menu

A Drives menu runs each drive, or all of them in order. Inputs come from the script, never from the player, and the script sets the input every physics step. While a drive runs, show its name, its stage and the live numbers on screen; at the end, show its results beside the target ranges, green inside, red outside.

The world for the drives: a large flat test ground. Seen from above, x is to the right and y is forward along the car's start direction. Every drive starts with the car at rest at x = 0, y = 0, facing +y. Heading is 0 facing +y and positive when turned right (clockwise from above). The car's position is its centre of mass.

Shared controllers (use these exactly, so the numbers compare with the Unreal car later):

- Speed hold to a target v_t (m/s): e = v_t - speed; I = I + e * dt, kept between 0 and 10; throttle = clamp(0.5 * e + 0.1 * I, 0, 1); brake = clamp(0.3 * (-e - 0.5), 0, 1).
- Steady: |speed - v_t| < 0.25 m/s for 2 s in a row.
- Pure pursuit steering toward a point on a path: look-ahead ld = max(4, 0.6 * speed) m; alpha = angle from the car's nose to the point, positive to the right; wheel angle = atan(2 * wheelbase * sin(alpha) / ld); steer = clamp(wheel angle / full-lock wheel angle, -1, 1).
- Steer is -1 (full left lock) to +1 (full right lock).

The drives (the stage names in brackets go into the telemetry "phase" column):

- D1 straight run (run): full throttle, no steering, from rest. Ends when speed has gained less than 0.1 mph over the last 5 s (after at least 10 s), or at 150 s. Gives 0 to 30 and 0 to 60 mph times, top speed, speed after 100 m, largest pitch in the first 5 s.
- D2 braking, three runs at 30, 50 and 70 mph, then the same three with the wet-grip setting applied (approach, brake). Wet braking uses a wet-grip setting in the tuning panel (a grip multiplier, used for these runs), not a wet road surface or wet visuals: speed hold to the set speed; once steady, full brake at once, throttle 0, steer 0, until speed is 0.01 m/s or less. Braking distance is the distance travelled from the first brake step to the stop. Pitch and front load share at 0.8 g are read off a straight line fitted to the last second before braking plus the braking samples from 0.5 s after the brake until speed falls under 1 m/s, against forward g, then read at -0.8 g.
- D3 turning circle (approach, lock): speed hold at 5 mph; once steady, full right lock (+1), speed hold on, until the heading has turned 1.25 full turns. Fit a circle to the outer edge of the outer front tyre over the last full turn; the turning circle is its diameter.
- D4 slalom, run at 30 mph, then 32, 34 and so on in 2 mph steps up to 50, stopping after the first run that is not clean (approach, cones, exit): 8 cones on the line x = 0 at y = 250, 268, 286 and so on (every 18 m). The path is x = 1.2 * cos(pi * (y - 250) / 18) from y = 241 to y = 385, and x = 0 before and after. Speed hold at the run's speed, pure pursuit to the point on the path at y + ld. "cones" runs from y = 241 to y = 385. Clean means the car's centre passes each cone on its own side (+x for the first cone, then alternating) at least 0.9 m from the cone. Ends 40 m after y = 385. Gives the highest clean speed, and at 30 mph the delay between steer and yaw rate that lines them up best (0 to 1 s).
- D5 step steer (approach, step, release): speed hold at 30 mph; once steady, set steer to the value that gives a 2 degree road-wheel angle (2 / full-lock angle in degrees), speed hold on; after 2 s set steer to 0, speed hold on, for 4 s more. Gives the time from the step until yaw rate first reaches 63.2% of its settled value (the average over the last 0.5 s of the step), and the time from release until yaw rate stays under 5% of that settled value.
- D6 steady circle, slide and recovery (circle, recover): a 40 m radius circle with its centre at x = 40, y = 0, driven clockwise (turning right). Pure pursuit to the point on the circle ld metres of arc ahead of the car. Target speed 6.7 m/s (15 mph) for the first 10 s, then rising by 0.15 m/s every second. Slide onset: after 10 s, the car is more than 2 m outside the circle. From then on: throttle 0, brake 0, wheel angle = slip angle - 0.2 * yaw rate (slip angle: the direction the car is moving relative to its nose, positive right, in radians), converted to steer as above; ends 6 s after onset, or at 150 s. Gives the highest steady lateral g (0.5 s average while within 2 m of the circle), the speed and lateral g at onset, the recovery time (onset until slip angle stays under 2 degrees and yaw rate under 0.1 rad/s for 0.5 s; the time counted is when that 0.5 s began), and roll at 0.5 g (straight line through roll against lateral g while within 2 m of the circle, read at 0.5 g).
- D7 handbrake turn (approach, turn, stop): speed hold at 30 mph; once steady, at once: steer +1, handbrake on, throttle 0, brake 0, for 0.6 s (turn). Then handbrake off, steer 0, full brake (stop), until speed is under 0.5 m/s and yaw rate under 0.1 rad/s, or 8 s after the pull. Gives the yaw turned (heading change, in degrees, at the moment the turn settled) and the time the turn took to settle: from the handbrake pull to the moment after which yaw rate stays under 0.1 rad/s to the end of the run.
- D8 camera run (rest, run): 1 s at rest, then full throttle, no steering, until 90 mph or 180 s. Gives camera distance and height at rest, the lag (the median, over samples above 10 m/s, of (distance at that moment minus distance at rest) divided by speed), field of view at 0, 30, 60 and 90 mph, and the widening from 0 to 90.

### 4. Export: results JSON and telemetry

Each drive offers two downloads; "Run all" offers one zip or a set of downloads.

Telemetry, one file per run, named D1, D2-30, D2-50, D2-70, D2-wet-30, D2-wet-50, D2-wet-70, D3, D4-30, D4-32 (and so on), D5, D6, D7, D8, as .csv (header row, then one row per physics step; first lines may be comments such as "# max_steer_deg=32" and "# wheelbase=2.4") or .jsonl (one JSON object per line; an optional first line {"meta": {"max_steer_deg": 32, "wheelbase": 2.4, "car": "browser-round2"}}). Always include max_steer_deg (road-wheel angle at full lock, degrees) and wheelbase (m) in the meta. One row per physics step, columns exactly:

```
t                 seconds since the run started
x, y              position, metres (frame above)
heading           radians, 0 facing +y, positive turned right; keeps counting past +-pi
speed             m/s, never negative
yaw_rate          rad/s, positive turning right
lat_g             sideways acceleration of the body in g, positive to the car's right
long_g            forward acceleration of the body in g, braking negative
roll_deg          degrees, positive right side down
pitch_deg         degrees, positive nose up
front_load_share  share of the weight on the front axle, 0 to 1
steer             steering applied after the car's own smoothing, -1 to +1
throttle, brake   0 to 1
handbrake         0 or 1
phase             the drive's stage name
cam_dist          horizontal distance from the car's position to the camera, m
cam_height        camera height above the road, m
cam_fov           horizontal field of view, degrees
cam_lag           your camera's own lag figure, seconds (optional)
wfl_x, wfl_y, wfr_x, wfr_y   outer edge of the front left and front right tyre's
                  contact patch, world metres (the side away from the car's middle)
```

Results JSON, one file for all drives run:

```
{"car": "browser-round2", "format": "ledger-driving-result-1", "target_set": "ordinary",
 "metrics": {
  "M1.0_30_s": ..., "M1.0_60_s": ...,
  "M2.top_speed_mph": ..., "M2.speed_at_100m_mph": ..., "M2.top_speed_settled": true,
  "M3.brake_30_m": ..., "M3.brake_50_m": ..., "M3.brake_70_m": ...,
  "M3.wet_brake_30_m": ..., "M3.wet_brake_50_m": ..., "M3.wet_brake_70_m": ...,
  "M3.wet_ratio_30": ..., "M3.wet_ratio_50": ..., "M3.wet_ratio_70": ...,
  "M4.turning_circle_m": ...,
  "M5.yaw_63_s": ..., "M5.self_centre_s": ...,
  "M5.slalom_max_clean_mph": ..., "M5.slalom_yaw_lag_s": ...,
  "M6.roll_deg_at_0_5g": ..., "M6.pitch_brake_deg_at_0_8g": ..., "M6.pitch_throttle_deg": ...,
  "M7.front_load_brake_pct_at_0_8g": ...,
  "M8.max_steady_lat_g": ..., "M8.slide_onset_mph": ..., "M8.slide_onset_lat_g": ..., "M8.recovery_s": ...,
  "M9.handbrake_yaw_deg": ..., "M9.handbrake_settle_s": ...,
  "M10.cam_dist_m": ..., "M10.cam_height_m": ..., "M10.cam_lag_s": ...,
  "M10.fov_0_deg": ..., "M10.fov_30_deg": ..., "M10.fov_60_deg": ..., "M10.fov_90_deg": ...,
  "M10.fov_widen_deg": ...
 }}
```

Use null for a number a drive could not produce (for example a turn that never settles). The wet ratio is the wet braking distance divided by the dry one at the same speed. M3 pitch and front load use the average of the three dry braking runs. Our own tool reads both files and works the numbers out again from the telemetry, so the telemetry must be exact.

### 5. Tuning panel

A panel, opened with a key and a menu button, with every handling and camera setting as a live slider or number box: mass, centre of mass position and height, grip, tyre stiffness, steering lock, steering speed and return speed, engine power and traction limit, drag, brake strength and front to rear split, handbrake grip, roll and pitch stiffness and damping, wet grip factor, camera distance, height, lag, field of view at rest and at speed, and anything else your model uses. Changes act at once. Buttons: save settings as JSON, load settings JSON, reset to defaults, and "export settings and results", which writes one JSON holding the full settings and the latest results together, with the date and a short name.

### 6. Game controller

Support a game controller with the browser Gamepad API, using the standard mapping:

- Use controllers whose `mapping` is "standard". Left stick: axes 0 (sideways, used for steering) and 1 (up and down, unused).
- Right trigger: button 7, read as an analogue value (`buttons[7].value`, 0 to 1) for throttle. Left trigger: button 6 (`buttons[6].value`) for brake.
- Handbrake: button 0 (A, or cross on PlayStation layouts), with button 5 (right bumper) also working.
- Settings in the tuning panel: stick dead zone (default 0.10), steering curve (an exponent, default 1.5, so small stick moves steer gently), trigger dead zone.
- Handle controllers connecting and disconnecting while the game runs.
- Show an on-screen note until a controller is seen: "Controller not detected yet: press any button on it". Most browsers only report a controller after one of its buttons is pressed.
- Keyboard keeps working: digital keys are smoothed into analogue values (steering ramps in and returns to centre at set rates; throttle and brake ramp), with those rates in the tuning panel.
- Show on screen which input is active (Keyboard or Controller), switching to whichever was used last.
- Scripted drives ignore player input completely while they run.

### 7. Changelog note

At the top of the game's notes, add a short dated "Round two" note: what changed, which targets the car now meets, and which it does not yet meet, with the numbers.

## Not this round

These are the features for later rounds. List them in your notes as planned, but do not build any of them now.

1. Handling tuned by feel in many short sessions with Jafar, after the numbers pass.
2. Getting in and out of the car with a walking character, door and seat animation included.
3. A finished chase camera: collision with walls, look-behind, and smoothing on bumps.
4. Background traffic cars that drive on simple lanes and switch to full physics only when hit.
5. Deeper handling: load moving side to side as well as front to back, per-wheel tyres and suspension.
6. Wet road visuals: puddles, spray and the look of a wet surface (wet grip itself is already a tuning setting this round).
7. Damage: dents, panels coming off, glass and lamps breaking.
8. AI drivers who give way, react to the player and to danger, and use horns.
9. Police chases.
10. A full interior and a first-person driving view.
11. Layered engine sound: pitch with engine speed, gear changes, tyre squeal at the grip limit, impact sounds.

When this round is done, send back: the results JSON from "Run all", the telemetry files, the settings JSON, and the changelog note.
