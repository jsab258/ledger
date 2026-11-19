# Driving measurement method: measuring other games' cars from public video (19 November 2026)

Step two of his four-step driving plan, part (b). The games are in DRIVING-REFERENCE-GAMES-2026-11-19.md and wait for his approval. The targets being filled are M1 to M10 of FEEL-TARGETS-DRIVING-2026-11-17.md. This file says how professionals measure a vehicle from video, how each metric is measured here, which behaviours are written down as experience rules, and the sheet the builder fills in on his PC.

Outside only: clips are played in Chrome on YouTube and never downloaded; no game is run, opened or extracted for this. Only our own numbers are kept: a number read in someone else's video description or article is a lead, never a result.

Tags: [READ] read at the source on 19 Nov 2026; [I] our own judgement, not read today; [UNREACHED] title only.

## In short

- The professional method is forensic speed-from-video: two fixed marks a known distance apart, the frames between them counted, the error worked out from both. Its biggest lesson: count across many frames, since one frame between marks can mean an error of about 76% and ten frames about 7%.
- Every number here: at least five samples, two measurers working separately, the middle value and the spread reported; a disagreement over 10% (times, distances) or 3 degrees (angles) is measured again.
- Time on the PC: about 2 hours 15 minutes per game for the first measurer (clip check, M1 to M10, the behaviours) and about 1 hour 50 minutes for the second, who reuses the clip check and minute marks; a contrast game about half. Six shortlisted games and two contrast games: about 15.5 hours for the first measurer and 12.5 for the second, about 28 hours in all. If only four games and the two contrast games are approved, about 20 hours.

## 1. How professionals measure a vehicle from video

- UK police practice (Forensic Capability Network example statement, undated): two fixed features (a lamp post and a lane line), their distance from a survey (51.8 m), 27 frame intervals (1.8 s), so 64 mph, stated as 64 plus or minus 0.65 mph. The frame gaps on a 15 fps camera were uneven (0.08, 0.08, 0.04 s) and were checked. The main error was placing the car's leading edge on the mark, not the timing. [READ] https://fcn.police.uk/docs/speed-estimation-video-fsa-dig-301-mg22c-sfr2-examplepdf/download
- Beauchamp, Pentecost, Koch and others, SAE 2021-01-0887, "Speed Analysis from Video: A Method for Determining a Range in the Calculations" (2021): speed is distance over time, errors combined by standard error propagation. With one frame between positions the speed range was about plus or minus 76%; with ten frames about plus or minus 7%. Frame gaps on nominal 30 fps cameras varied from 0.023 to 0.044 s. [READ] https://jsheld.com/uploads/Speed-Analysis-from-Video-A-Method-for-Determining-a-Range-in-the-Calculations.pdf (abstract https://saemobilus.sae.org/content/2021-01-0887 )
- Polito, Amped Software, "Measure Speed from Surveillance Video", 12 Dec 2023: scale from a known flat object, mark the tyre's contact point each frame, check the real frame times (a nominal 25 fps stream had 0.10 s and 0.05 s gaps). Timing is often harder than distance. [READ] https://blog.ampedsoftware.com/2023/12/12/measure-speed-from-surveillance-video
- Camera matching from one frame (University of Illinois CS445, lecture 13, Fall 2019): vanishing points of lines at right angles give the focal length; heights come from the horizon and an object of known height. [READ] https://courses.grainger.illinois.edu/cs445/fa2019/lectures/Lecture%2013%20-%20Camera%20Model%20and%20Single%20View%20Metrology%20-%20CP%20Fall%202019.pdf
- Measuring responsiveness from video (Mick West, Game Developer, 16 Jul 2008): film at 60 fps, step frame by frame, count from the input to the first response. GTA IV was about 10 frames. [READ] https://www.gamedeveloper.com/design/measuring-responsiveness-in-video-games . Here the input is not visible on screen, so response is counted from the front wheels turning, not from the key.
- Two measurers and angles (Kinovea reliability study, Sensors 20(11):3154, 2 Jun 2020): angles measured from video by two observers agreed within about plus or minus 2.5 degrees; one observer repeating agreed within about 5 degrees. Under 2 degrees is good, 2 to 5 needs care, over 5 may mislead. [READ] https://pmc.ncbi.nlm.nih.gov/articles/PMC7308968
- Body roll per g as a measure (HP Academy, undated): roll angle plotted against sideways acceleration; the slope is the roll gradient. [READ] https://www.hpacademy.com/courses/professional-motorsport-data-analysis/cornering-performance-suspension-stiffness-and-balance
- Not found: any published method for measuring another game's handling from footage; any table of errors from video compression or repeated frames. This method is put together from the forensic and camera-matching practice above.

## 2. The scales

- Road markings. UK (Traffic Signs Manual chapter 5, Department for Transport, 2019 edition): centre line at 40 mph or less, 4 m mark and 2 m gap (6 m from start to start); over 40 mph, 6 m and 3 m (9 m); warning lines the same pairs. [READ] https://assets.publishing.service.gov.uk/media/5c4ace6ded915d38a0611abc/traffic-signs-manual-chapter-05.pdf . US (MUTCD 2009, 3A.06): broken lines 10 ft marks, 30 ft gaps (12.2 m start to start). [READ] https://mutcd.fhwa.dot.gov/htm/2009/part3/part3a.htm . Games do not always copy real markings [I], so each game's dash is first measured against its own car before it is used as a ruler.
- The car itself: the length and wheelbase of the car in the clip, from the real model it copies where there is one; for invented cars, its length is set from its markings in a clear side view, and stated as estimated.
- Lamp post spacing and kerb stones: only after they are measured once against the car in the same game.

## 3. The rules for every number

- Clip check first: open "Stats for nerds" (right-click on the video) and write down the frame rate; only 60 fps clips give timings. Check the normal game camera (behind the car, no cinematic or bonnet camera), no mods named in the title or description, and no edit cuts inside the sample. Note the minute marks of each scene needed.
- Frame stepping: pause, then "." steps one frame forward and "," one back (desktop only) [READ, vidIQ, undated] https://vidiq.com/blog/post/youtube-frame-by-frame/ . Before using a clip, check that one step is one frame: step 60 times and see the clock move one second. If not, that clip is used for sizes only.
- Count frames, never read the clock: a time is the number of steps between two frames, divided by 60.
- Spread the count: no time sample over fewer than 10 frames (a sixth of a second); shorter events are measured as distances over a longer stretch.
- Pixel measures: take a screenshot of the paused frame (a picture of one frame, not the video) and measure pixels in an image viewer at 100%. Screenshots stay on F: in the lane research folder, never in git, and are deleted once the numbers are written down.
- At least five samples per number, from at least two clips where possible. Two measurers work separately (the builder and a fresh helper given the same minute marks but not the first measurer's numbers). Report the middle value (median) and the lowest and highest. If the two medians differ by more than 10% (or 3 degrees for angles), both measure again; if they still differ, report both and mark it uncertain.
- Speedometer readings: where the game shows speed, read it at each frame used; check it once against road markings (a speedometer can be wrong or in a different unit).

## 4. Each metric (M1 to M10)

- M1 acceleration (0 to 30 mph, 0 to 60 mph). With a speedometer: the frame the car first moves to the frame the speedometer shows 30 (and 60); count the steps. Without: mark the frame the car passes each dash start; speed between dashes is the dash module over the time; plot speed against time and read when it reaches 30 mph. Only straight, flat pulls from standstill. Five pulls. About 10 minutes.
- M2 top speed and speed after 100 m. Speedometer, or dash timing at the end of a long straight. Speed after 100 m: count 100 m of markings from standstill (about 17 UK small dashes). Three to five runs. About 5 minutes.
- M3 braking from 30, 50 and 70 mph. Speed at the frame the brake lights come on (or the nose first dips); distance to rest counted in dashes and parts of a dash, or in car lengths. Note wet or dry. Five stops for at least one starting speed. About 10 minutes.
- M4 turning circle. A full-lock U-turn or full-lock circle at walking pace: measure the outer front wheel's path across the road in car lengths, kerb to kerb. Also record whether the car turns round on a two-lane street in one go. Five turns. About 10 minutes.
- M5 steering response and self-centring. At about 30 mph on a straight: the first frame the front wheels turn, then the frame the car's heading has changed by most of its final turn (the nose crosses a mark at 63% of the final angle). Self-centring: the frame the wheels start to straighten to the frame they are straight. Hard to see; done on screenshots of the frames. Five samples. About 15 minutes.
- M6 roll and pitch. Roll: on frames where the camera is level and directly behind, the angle of the roof line or rear window's bottom edge against the road's horizon, at a steady bend (sideways acceleration from speed squared over the bend's radius, the radius from the road's lanes). Pitch: from a side view, the angle of the sill line under hard braking and full throttle, against the same car at rest. Five of each. About 15 minutes. Expect plus or minus 2.5 degrees between measurers.
- M8 grip and recovery. Grip: the fastest steady speed round a bend of known radius (from lanes or a roundabout) before the car slides wide; sideways g is speed squared over radius divided by 9.81. Recovery: the frame the tail steps out to the frame the car runs straight again. Five of each. About 10 minutes.
- M9 handbrake turn from about 30 mph. Speed at the start; the car's turn in degrees (from the road's lines before and after); frames from the start of the slide to the car settled. Speed lost. Five turns. About 10 minutes.
- M10 camera. Distance and height: from a frame with the car square on, the car's known width in pixels and the screen width give the field of view and distance (focal length in pixels equals the car's pixel width times distance over its real width; with three vanishing points, the field of view directly). Lag: frames between the car starting a hard pull away and the camera starting to follow. Field of view at 0, 30, 60 and 90 mph (where reached): measure the same at each speed; widening shows as the car shrinking on screen at the same distance. Five frames per speed. About 10 minutes.

M7 (front load under braking) cannot be seen on screen and is not measured; M11 and M12 are covered by the behaviours below and by ear.

## 5. Behaviours to record as experience rules

For each game, watch for each case at least three times and write one plain line per case: what happens, how long it takes, and whether the player has to do anything.

1. After a hard crash: does the car stop dead, bounce, spin? How long until control returns? Does the driver react? Is the car still drivable, and how much speed and steering is lost?
2. A stuck player: car on its roof, wedged against a wall, nose in a ditch. What gets him moving: he flips it himself, the game rights it, he walks away and takes another car? How long is the wait?
3. Damage shown and mended: dents, lights, smoke, a wheel; at what impact; does the steering pull? Where and how is it mended (a garage, a spray shop, never), and how long it takes.
4. People in the road: do pedestrians step back, dive, shout, run? Does a hit person fall, get up, call the police? What do onlookers do? Watch for anything a 1990 British town would do differently. (LEDGER's rule: a car hurts badly and never kills.)
5. The camera in tight spaces: in an alley, under an arch, against a wall, reversing out of a dead end: does it pull in, swing, clip through, lose the car? How long does it take to settle?
6. Leaving and entering the car: how long from key press to driving away, and from stopping to standing.
7. Police and witnesses after a crash: who notices, how fast.

## 6. The measuring sheet (the builder fills it in on his PC)

One sheet per game per measurer, saved as a text file in production/research/lane/measurements/ (the folder is made when the first sheet is filled). Play in Chrome on YouTube, never download. Clip check first; then the numbers; then the behaviours.

```
Game:                     Measurer:            Date:
Clip check (5 min a clip)
  Clip title and link:
  Frame rate (Stats for nerds):     One step = one frame? (yes/no)
  Normal camera? Mods named? Edit cuts? Speedometer on screen?
  Minute marks: pull away __  hard stop __  full-lock turn __
                handbrake turn __  bend __  crash __  tight space __
Numbers (five samples each; write each sample, then the middle and the spread)
  M1  0-30 mph s: _ _ _ _ _   0-60 mph s: _ _ _ _ _       method: speedo / dashes
  M2  top mph: _ _ _          mph at 100 m: _ _ _ _ _
  M3  start mph / stop m: _/_ _/_ _/_ _/_ _/_            wet or dry:
  M4  circle in car lengths: _ _ _ _ _   one-go U-turn on two lanes? yes/no
  M5  turn-in s: _ _ _ _ _    self-centre s: _ _ _ _ _
  M6  roll deg / g: _/_ _/_ _/_ _/_ _/_   brake pitch deg: _ _ _ _ _   throttle pitch deg: _ _ _ _ _
  M8  grip g: _ _ _ _ _       recovery s: _ _ _ _ _
  M9  turn deg / settle s / mph lost: _/_/_ (x5)
  M10 distance m: _ _ _ _ _   height m: _ _ _ _ _   lag s: _ _ _ _ _
      field of view deg at 0 / 30 / 60 / 90 mph: _ / _ / _ / _
Behaviours (one line each, with the minute mark)
  Hard crash:      Stuck:      Damage and mending:     People in the road:
  Tight camera:    In and out of the car:      Police and witnesses:
Notes: anything that did not fit; any number marked uncertain and why.
```

How long it should take: clip check about 5 minutes a clip, four or five clips a game, about 25 minutes; the numbers about 95 minutes; the behaviours about 15 minutes. About 2 hours 15 minutes a game for the first measurer; the second measurer reuses the clip check, about 1 hour 50 minutes. A contrast game, measured for M1 to M3 and M10 only, about half. The six-game shortlist plus two contrast games: about 15.5 hours for the first measurer, 12.5 for the second, about 28 hours for both.

## 7. What comes out

A filled table, game by game, beside the game set's targets in FEEL-TARGETS-DRIVING section c2: each number with its median, spread, sample count and the two measurers' medians. Where the measured games disagree with the provisional targets, the targets sheet is changed with the evidence, and the change is recorded for him. The behaviours become experience rules for the driving study's next round. The Fable round (step three) waits for both.
