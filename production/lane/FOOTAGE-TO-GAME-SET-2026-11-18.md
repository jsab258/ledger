# From footage to the game set: turning frame measurements into numbers (18 November 2026)

Written by the cloud lane for the main session, to run in one pass next week. It takes the frames planned in section (e) of production/research/lane/FEEL-TARGETS-DRIVING-2026-11-17.md and turns them into replacement numbers for the provisional game set (section c2 of that file; the set named "game" in tools/lane/driving_drives.py).

His rulings it serves (18 Nov, RULINGS Cars line): fun first, like open-world games that are not sims; 1990 by sound, sway, look and relative speed; real figures a floor; game-band targets; automatic gearbox.

The outside-only rule binds every step: watch the videos in the browser, step frames, take screenshots. Never download a video, never open or extract a game's files, never get around copy protection. The cloud cannot open YouTube, so this is run on the PC.

## 1. Before measuring

- Games and weight. The band comes from the open-world games that are not sims: GTA V, GTA IV, Mafia III, Sleeping Dogs, The Getaway (videos 1 to 12 in section e). Forza Horizon 4 (13 to 15) is open world but tuned for racing: use it where it shows the HUD speed of a period car (13 to 15) and as a check, not as one of the games whose median sets the band, unless fewer than three of the others give that metric. Mafia: The Old Country (16) is general feel only and never sets a number.
- Which car. In each game measure its ordinary small or compact car (the class the player meets most in a town), not a sports car. Note the car's on-screen name in the sheet; it does not appear anywhere in LEDGER.
- Footage checks, per clip: unmodded (no mod menu, no custom speedometer, no graphics mod that changes the field of view); not an edited cut across the moment being measured; frame rate read from the player's "Stats for nerds" (30 or 60). Reject a clip that fails any check and say so.
- The sheet. One line per sample in a new file production/research/lane/FOOTAGE-MEASUREMENTS-<date>.md: game, video number, timestamp, metric, raw readings (frame numbers, pixel lengths), the worked number, its uncertainty. Screenshots go to the research folder production/retention.json names, file name game, video ID, timestamp. Only the reduced previews the git rules allow are committed.

## 2. Shared methods

- Time: count frames between the two events and divide by the frame rate. Each end is uncertain by one frame, so a time is good to plus or minus 2 divided by the frame rate (0.07 s at 30 fps, 0.03 s at 60 fps). Step with the full stop and comma keys at 0.25x.
- Speed with a HUD (Forza Horizon 4 only, and GTA or Mafia only if the game's own HUD shows it): read it off the frame. Check the unit (mph or km/h). A HUD reads to 1 mph and may trail the car a little: plus or minus 1 mph.
- Speed without a HUD: count road-marking repeats passing a fixed screen point (for example the rear bumper) over a counted number of frames. Speed = repeats times repeat length divided by time. Uncertainty: half a repeat at each end.
- Scale. In order of preference: (1) a road-marking repeat of known length: UK warning line 6 m (40 mph or less) or 9 m (above), US broken lane line 12.2 m (3.0 m line plus 9.1 m gap); (2) the car's own wheelbase or length, measured in pixels in a side or near-side view and set from its class (a compact about 2.4 to 2.6 m wheelbase and 3.8 to 4.2 m long, a saloon about 2.7 m and 4.5 to 5 m, est.); (3) lane width (UK town lane about 3 to 3.65 m, US 3.6 m, est.). Before trusting markings in a game, check them against the car's length once per game; if they disagree by more than 15%, use the car and say so.
- Angle: measure the line in question (roofline, sill, bonnet edge) against the horizon or a long straight building edge in the same frame, in pixels, and turn it into degrees with atan of rise over run. First check that the camera does not itself roll (the horizon stays level against the screen edges); if it rolls, measure against the horizon, not the screen. Good to about plus or minus 1 degree.
- Heading (which way the car points): from a fixed view, the angle between the car's long axis and the road edge; in a chase view, how far the vanishing point of the road slides across the screen. Use for M5 and M9.
- Samples: aim for 5 samples per game per metric, from at least 2 clips; 3 is the least that counts for that game. A metric needs at least 3 games (2 if only two show it at all) to set a band.

## 3. From samples to a band (every metric)

1. Per game: the median of that game's samples.
2. Centre: the median of the per-game medians (each game counts once, however many samples it gave).
3. Half-width: the largest of (a) half the spread of the per-game medians (highest minus lowest, halved, capped at the centre's 25%), and (b) the measurement uncertainty from section 2, and (c) the minimum stated per metric below. Band = centre minus half-width to centre plus half-width.
4. Floor: clip the band to the real-1990 floor in section c2 of the feel-targets file (for example 0 to 60 never over 17 s; braking never longer than 14, 38, 75 m; roll never under 3 deg). If clipping removes more than half the band, the games are telling us something: note it in the sheet and keep the clipped band.
5. Relative speed: the ordinary car's band must leave the fast hatch and the big saloons clearly quicker (0 to 60 at least 1.5 s apart, top speed at least 8 mph apart). If not, shift the ordinary band, not the floor, and say so.
6. Round to the precision the old band used (0.5 s for 0 to 60, 0.1 s under 5 s, 0.5 m under 15 m, 1 m above, 0.5 deg, 0.01 g, 1 mph).
7. State the uncertainty: the measurement uncertainty, the number of games and samples, and the spread.

When the games disagree (the highest per-game median more than 1.5 times the lowest): do not average blindly. Use the games closest to the ruling's "fun and easy, not a sim" for the centre (GTA V, Mafia III, Sleeping Dogs for ease and grip; GTA IV is the upper limit for sway only, The Getaway for British street camera), and record that choice in the sheet and one line in DECISIONS.md.

When a metric cannot be measured (too few games, no clean clip, or an uncertainty wider than the provisional band itself): keep the provisional band, mark it "provisional, not measurable from footage" in the feel-targets file, and say so in the summary. Never fill a gap with a number from memory.

## 4. Metric by metric

### M1 acceleration (0 to 30 and 0 to 60 mph)
- Frames: a pull away from standstill on a straight, full throttle. Best: Forza Horizon 4 video 13 (HUD speed); then Mafia III video 2 and Sleeping Dogs video 10 by markings. Videos 14 and 15 show a big saloon and a fast hatch: use them only for the relative-speed check (step 5 of section 3), never for the ordinary car's band.
- How: frame of first movement to first frame showing 30 mph, then 60 mph. Without a HUD, speed from marking repeats over each half-second window, and the time where it passes 30 mph read off a line through those speeds.
- Samples: 5 per game. Uncertainty: plus or minus 2 frames, plus 1 mph on the HUD (about 0.1 s near 30 mph); without a HUD about plus or minus 15%.
- Minimum half-width: 0.5 s (0 to 30), 1.5 s (0 to 60). Floor: never slower than 6 s and 17 s. Relative speed rule applies.

### M2 top speed and speed after 100 m
- Frames: the same pull aways, continued; a long straight for top speed (Forza Horizon 4 videos 14 and 15 have top-speed runs of a period saloon and fast hatch: relative-speed check only, not the ordinary band).
- How: speed after 100 m: count 100 m of markings from the start (about 17 UK 6 m repeats or 8 US repeats) and read the speed there. Top speed: the HUD value once it stops rising for 5 s. Without a HUD top speed is usually not measurable in town footage: keep provisional.
- Samples: 3 per game. Uncertainty: plus or minus 1 mph on the HUD; plus or minus half a repeat in distance (about 1 mph at 45 mph).
- Minimum half-width: 4 mph (after 100 m), 7 mph (top). Floor: not under 40 and 90 mph; stay at least 8 mph under the fast hatch's top speed.

### M3 braking from 30, 50, 70 mph, and wet
- Frames: hard stops in a straight line: GTA V video 7, GTA IV video 4, Mafia III video 2, Sleeping Dogs video 10, The Getaway video 11 (UK warning lines), Forza Horizon 4 video 13.
- How: speed just before the brake (HUD or markings over the last 10 frames), the frame the brake lights come on or the nose dips, the frame the car stops; distance in marking repeats under the car. Scale every stop to the target speed by distance times (target over start speed) squared, using only stops that start within 20% of the target speed. Wet: the same in rain, where a clip shows it; ratio = wet over dry at the same speed in the same game.
- Samples: 5 dry stops per game across the speeds; wet only if found. Uncertainty: half a repeat each end (plus or minus 3 to 6 m) plus the speed error squared: often 15 to 20%. If the uncertainty is wider than the band, keep provisional.
- Minimum half-width: 1.5 m, 4 m, 7 m. Floor: never longer than 14, 38, 75 m; wet never under 1.3 times dry. Wet rain clips are rare: expect wet to stay provisional.

### M4 turning circle
- Frames: a full-lock U-turn or three-point turn in a street of known width: Mafia III video 2, Sleeping Dogs video 10, The Getaway video 11.
- How: the outer front wheel's widest arc against the road width (from markings or lane widths): diameter = road width used for a half circle. Count only turns at walking pace with the wheels visibly at full lock.
- Samples: 3 per game. Uncertainty: about plus or minus 0.5 m.
- Minimum half-width: 0.5 m. Floor: never wider than 10.5 m; no one-go U-turn kerb to kerb on a 7.3 m street. Likely few clean samples: keep provisional if under 2 games.

### M5 steering response and self-centring
- Frames: a quick lane change or turn-in at about 30 mph in a chase view, where the front wheels can be seen turning (GTA IV video 4, GTA V video 8, Mafia III video 2).
- How: frame the front wheels start to turn (the step) to the frame the car's turn rate (vanishing-point slide per frame, or heading change per frame) reaches 63% of its steady value. Self-centring: frame the wheels straighten to the frame the heading stops changing.
- Samples: 5 per game. Uncertainty: plus or minus 2 frames on each event, so plus or minus 0.07 s at 30 fps, comparable to the whole band: only 60 fps footage counts here.
- Minimum half-width: 0.05 s and 0.2 s. Floor: never slower than 0.35 s and 1.2 s. Expect this to stay provisional unless 60 fps chase-view clips show the wheels clearly; say so.

### M6 roll at 0.5 g, pitch at 0.8 g braking, pitch under full throttle (sizes)
- Frames: roll: a steady bend or a 90 degree junction turn seen from behind (GTA IV videos 4 to 6 as the upper limit, GTA V, Mafia III, Sleeping Dogs). Pitch: side or three-quarter views during the M3 stops and M1 pull aways.
- How: roll: roofline against the horizon at the steadiest point of the bend. Lateral g there = speed squared over (radius times 9.81), radius from the road's curve against its width (a UK 90 degree town junction is about 6 to 10 m radius, est.). Scale the roll to 0.5 g by roll times 0.5 over that g (a straight line through zero), using only bends between 0.3 and 0.8 g. Pitch: the sill or roofline against the horizon at the steadiest part of the stop or pull away; for braking scale to 0.8 g by the stop's mean deceleration (start speed squared over twice the distance).
- Samples: 5 per game per angle. Uncertainty: plus or minus 1 degree per reading, plus the g estimate (about 25%).
- Minimum half-width: 1 degree (roll), 1 degree (brake pitch), 0.5 degree (throttle pitch). Floor (reversed, sway carries 1990): never under 3, 2 and 0.5 degrees; GTA IV's per-game median is the top, never the centre.

### M7 front load at 0.8 g braking
- Cannot be seen in footage: load on an axle is not visible.
- Keep the provisional 72 to 82%. If M6 brake pitch moves a lot, check it is still consistent: more brake pitch usually goes with more front load (est.). Never above the real 82%.

### M8 highest steady lateral grip and recovery
- Frames: the fastest steady run round a bend or roundabout of known radius (Forza Horizon 4 Edinburgh, video 13; GTA V; Mafia III); slides with a counter-steer catch (Mafia III video 3, GTA IV video 5).
- How: grip: speed through the bend held for at least 1 s without running wide, radius from the bend against road width; g = speed squared over (radius times 9.81). Take the highest such sample per game; it is a lower bound (players are rarely at the limit), so say so beside the band. Recovery: frame the front wheels visibly counter-steer to the frame the heading stops changing and the car runs straight.
- Samples: 5 bends and 3 slides per game. Uncertainty: speed error doubled plus radius error: about 15 to 20% on grip; plus or minus 2 frames on recovery.
- Minimum half-width: 0.05 g and 0.2 s. Floor: never under 0.70 g or slower than 1.0 s. Understeer stays the ordinary car's habit, whatever the games do.

### M9 handbrake turn from about 30 mph
- Frames: handbrake turns: GTA IV vs V video 6, Sleeping Dogs video 9, Mafia III video 3.
- How: heading before the pull (along the road) to heading once the car stops rotating (for example facing back = 180 degrees), from the road edges; time from the frame the rear steps out to the frame rotation stops. Use only turns entered at 25 to 40 mph.
- Samples: 5 per game. Uncertainty: plus or minus 10 degrees, plus or minus 2 frames.
- Minimum half-width: 20 degrees and 0.2 s. Floor: never less than 90 degrees or slower than 2.0 s. It should still cost speed.

### M10 camera (distance, height, lag, field of view at 0, 30, 60, 90 mph)
- Frames: the chase view at rest and at steady speeds: The Getaway video 11 (the best British street camera), GTA V video 8, Mafia III videos 1 and 2, Sleeping Dogs video 9, Forza Horizon 4 video 13.
- How, field of view: first read it from the game's own settings screen if the footage shows one. Otherwise, at rest, use the car: its width on screen w (pixels) out of the screen width P, the car's width W (from its class, about 1.6 to 1.8 m, est.) and the camera distance D give the half-angle; with two unknowns, take D from the car's length foreshortening against a marking of known length behind it. This at-rest reading is the weakest; if neither the settings screen nor the markings give it, keep the provisional 60 to 65 degrees at rest and measure only the widening ratios below, which need no scale. Widening with speed: far-off scenery (the skyline, distant buildings) does not change size when the camera pulls back, only when the field of view widens, so the ratio of a far object's pixel width at rest to that at speed gives tan(new half-angle) over tan(old half-angle). Read it at 30, 60 and 90 mph.
- How, distance and height: distance from the car's pixel width once the field of view is known. Height: the angle down from the horizon to where the car's tyres meet the road, times the distance (height = distance times tan of that angle).
- How, lag: at a steady speed after a hard pull away, the extra distance (the car looks smaller than at rest, after the field-of-view change is taken out) divided by the speed, in seconds: the same definition the tool uses.
- Samples: 3 at rest and 3 at each speed per game. Uncertainty: about 10% on distance and height, plus or minus 2 degrees on field of view, plus or minus 0.05 s on lag.
- Minimum half-width: 0.5 m, 0.2 m, 0.05 s, 2.5 degrees. No real-car floor; the widening with speed should stay at least as strong as the provisional band, since it is how relative speed reads.

M11 and M12 are not part of the game set: unchanged.

## 5. Checklist

1. Clips checked (unmodded, unedited at the moment, frame rate noted); rejects listed.
2. Every sample on the measurement sheet with its frames, pixels, worked number and uncertainty.
3. Per metric: per-game medians, centre, half-width, floor clip, relative-speed check, rounding, uncertainty stated.
4. Disagreements and unmeasurable metrics named; their provisional bands kept and marked.
5. A fresh reviewer checks the sheet's arithmetic and the bands against the screenshots before anything is changed.
6. Then, in one commit:
   - production/research/lane/FEEL-TARGETS-DRIVING-2026-11-17.md: section c2's table and the "game bands the drives check" table in (f), each changed number marked "measured <date>" with its uncertainty, the rest still "provisional"; the In short line updated.
   - tools/lane/driving_drives.py: GAME_SET with the new limits; if every number is measured, the status word for the game set from "provisional" to "measured" and SET_NOTES["game"] to match (keep the words "game band" in the note: tools/driving_feel_check.py looks for them).
   - tools/lane/test_driving_drives.py: GAME_BANDS to the same limits (and the status word if changed); run python -m pytest -q tools/lane/test_driving_drives.py and tools/driving_feel_check.py; both must pass.
   - One DECISIONS.md line: the game set measured from footage, which games, what stayed provisional.
7. Then the browser car is tuned to the new set in the next driving round.
