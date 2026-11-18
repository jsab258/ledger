# Driving test drives (17 November 2026)

Written by the lane session. The tool is tools/lane/driving_drives.py, with tests in tools/lane/test_driving_drives.py.

## What it is

LEDGER's driving comes in stages. First a browser prototype (Fable's JavaScript game), then the Unreal car. What carries over is how the car behaves, never its physics settings: the same numbers feel different in a different physics engine. So both cars run the same fixed, scripted test drives, a script drives each one instead of a person, and both export the same telemetry. This tool turns that telemetry into the shared metric numbers (M1 to M10) and checks them:

- against target ranges, in three named sets: "game" (the default since his rulings of 18 Nov: fun and easy first, like open-world games that are not sims; real 1990 figures a floor only; automatic gearbox by default; every number provisional until next week's footage measurements), and two older alternatives from 17 Nov, "ordinary" (an ordinary 1990 small hatch, the real range widened by the allowed game departures) and "fast" (a 1990 fast hatch), and
- car against car: the Unreal result against the browser result.

The tool also has a small reference car written in Python: a simple bicycle model with linear tyres that stop at a grip limit, weight transfer, and simple roll and pitch springs. It is not the game's handling. It is only there to make test telemetry and to show what a car that runs the drives looks like.

## The drives

| Drive | What the script does | Numbers it gives |
|---|---|---|
| D1 | Full throttle from standstill on a flat road, no steering, until top speed settles (under 0.1 mph gained in 5 s), at most 150 s | M1 0 to 30 and 0 to 60; M2 top speed and speed after 100 m; M6 pitch under throttle |
| D2 | Hold 30, 50 or 70 mph until steady for 2 s, then full brake, no steering, to a stop; dry and wet | M3 braking distances, and wet over dry as a ratio; M6 pitch at 0.8 g braking; M7 front load share at 0.8 g |
| D3 | Hold 5 mph, then full right lock for a loop and a quarter | M4 turning circle, kerb to kerb |
| D4 | Cones every 18 m; hold 30 mph through them, then 32, 34 and so on until a run is not clean | Slalom: highest clean speed and yaw lag (support for M5) |
| D5 | Hold 30 mph, step the steering to a 2 degree road-wheel angle, release after 2 s | M5 response time (63%) and self-centring time |
| D6 | Follow a 40 m radius circle at slowly rising speed until the car slides wide, then lift off and counter-steer | M8 highest steady lateral g, slide onset speed, recovery time; M6 roll at 0.5 g |
| D7 | Hold 30 mph, then full lock and the handbrake at once for 0.6 s; then handbrake off, steering straight, full brake to a stop | M9 how far the car turned and how long the turn took to settle (turn rate under 0.1 rad/s from then on) |
| D8 | One second at rest, then full throttle to 90 mph, logging the camera | M10 camera distance, height, lag, field of view at 0, 30, 60, 90 mph |
| D9 | No run of its own: braking pitch and roll come from D2 and D6 | M6, M7 |

The exact controllers, gains, cone positions and end conditions are written in the module's opening notes and in each drive's notes. A port in JavaScript or Unreal copies them exactly; otherwise the numbers do not compare.

## The telemetry format

One file per run, named after the run: D1, D2-30, D2-50, D2-70, D2-wet-30, D2-wet-50, D2-wet-70, D3, D4-30, D4-32 and so on, D5, D6, D7, D8. Either CSV (a header row, then one row per sample; lines starting with "#" are notes, "# key=value" lines are settings such as the car's full-lock angle) or JSON lines (one object per line; an optional first line {"meta": {...}}).

One row per physics step (120 a second is the target, 60 at least). Metres, seconds, radians unless the name says otherwise. Seen from above, x is to the right and y is forward along the car's start direction, starting at 0, 0.

| Column | Meaning |
|---|---|
| t | seconds since the run started |
| x, y | car position, metres |
| heading | turn angle in radians, 0 facing forward, positive turned right; it keeps counting past a full turn |
| speed | speed, metres a second |
| yaw_rate | how fast it turns, radians a second, positive right |
| lat_g, long_g | sideways (positive right) and forward (braking negative) acceleration, in g |
| roll_deg | body roll, degrees, positive right side down |
| pitch_deg | body pitch, degrees, positive nose up |
| front_load_share | share of the weight on the front wheels, 0 to 1 |
| steer | steering actually applied after the car's own smoothing, -1 full left to +1 full right |
| throttle, brake | 0 to 1 |
| handbrake | 0 or 1 |
| phase | the drive's stage at that moment (approach, brake, step, release, circle, recover, turn, stop, rest, run, lock, cones, exit) |
| cam_dist, cam_height, cam_fov, cam_lag | camera distance behind and height (m), field of view (degrees), the game's own lag figure (s, optional); needed in D8 |
| wfl_x, wfl_y, wfr_x, wfr_y | optional: outer edge of each front tyre, for the turning circle |

Settings the drives need from the car: max_steer_deg (road-wheel angle at full lock) and wheelbase. Extra columns are allowed and ignored.

## How each car exports it

- Browser: every physics step, add one object with the columns above to a list; at the end of the run, save the list as JSON lines or CSV as a download, plus one results JSON with the numbers.
- Unreal: a small logger on the vehicle writes the same columns each fixed physics sub-step to a CSV in the project's Saved folder. Unreal works in centimetres with different axes, so the logger converts to metres and to the frame above.

## How to run it

From the repository folder:

- `python tools/lane/driving_drives.py reference --out FOLDER` runs every drive on the reference car and writes its telemetry and result.json.
- `python tools/lane/driving_drives.py metrics FOLDER --out result.json` reads a car's telemetry files and writes its numbers.
- `python tools/lane/driving_drives.py targets --out targets.json` writes the default game set; add `--set ordinary` or `--set fast` for the older sets.
- `python tools/lane/driving_drives.py compare result.json` checks numbers against the game set (or `--set ordinary`, `--set fast`, `--targets targets.json`).
- `python tools/lane/driving_drives.py compare unreal.json --against browser.json` checks Unreal against the browser.
- Tests: `python -m pytest tools/lane/test_driving_drives.py` (or `python -m unittest tools/lane/test_driving_drives.py`).

## Pass rules

- Against targets: a number passes when it lies inside its range, edges included. A "provisional" or "first" target with no number fails. A "placeholder" is reported and never fails.
- Car against car: a number passes when the gap is at most 5% of the browser's number, or an absolute allowance by unit if that is larger: 0.05 s, 0.3 m, 1 mph, 0.3 degrees, 1 percentage point, 0.02 g. A number missing on one side fails.

## Choices made here (17 November 2026)

- D1 runs until top speed settles, not 30 s: a 1990 hatch needs over a minute to get close to its top speed. 0 to 60 still comes from the first seconds.
- Slalom path amplitude 1.2 m, clean meaning the car's centre passes each cone at least 0.9 m to its side. At 1.8 m an ordinary car would need about 1 g at 30 mph, beyond its grip.
- Readings "at 0.5 g" and "at 0.8 g" are read off a straight line fitted to the run's samples, since a hatch brakes at about 0.65 to 0.7 g and may never reach 0.8 g.
- Camera lag is worked out from the distance data: extra distance at speed divided by speed. That is what a camera trailing by that many seconds shows.
- The handbrake drive pulls for 0.6 s and then brakes straight, so it measures a real handbrake turn (pull, release, stop) and how fast it settles, not an endless spin.
- The reference car meets every target in the ordinary set (it was retuned on 17 November for that set; it has a little spin damping once well sideways, as many game cars do). It is not retuned for the game set, so the reference command checks it against the ordinary set. That proves the tool, not any handling choice.
