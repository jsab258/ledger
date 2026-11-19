# Driving gate: the clumsy player

An automated newcomer for the browser driving study (Quay Run). It plays a saved copy of the published page in
headless Chromium, keyboard first and then a simulated standard-mapping controller, crashes, reverses, gets out
and back in, wedges the car, spams buttons, pauses and resets, and after each scenario checks:

1. Never stranded: after any stop the player can move again within 5 s (car under throttle or reverse, or on
   foot). Fails for every stuck car and when the whole run's count of stranded stops is over zero. When the car
   will not move it then tries, in order and with nothing mended or moved by the gate: get out and walk;
   Backspace (pad: Back) on the car as the crash left it, F (pad: Y) to get back in, throttle; R, throttle. It
   records what worked and what the screen said after each.
2. Damage told and recoverable: a message counts only if it appears at or after the hit (within 3 s) and speaks
   of damage or what to do (words like damage, dent, crumple, will not drive, repair). A car that will not drive
   on must say what to do.
3. Smooth on keys: on the page's own frame loop at 60 Hz, at a held 30 mph (W pressed or let go every 3 frames),
   each move is judged on its own: press A, release, press D, release, press A, A to D, D to A, release. Each
   move of the key input, the car's steering and its yaw rate must take at least 0.1 s from 10% to 90%, and no
   60 Hz frame may change steering by more than 0.15 of full lock or the yaw rate by more than 0.15 rad/s.
   Rows after a collision are left out (speed falling by more than 1.5 mph in one frame).
4. Smooth on pad: the same for the car's steering and yaw rate with the stick at 0.25, 0.6 and 1.0: pushed over
   80 ms, let go at once (as a released stick springs back), pushed the other way, swung left to right. The
   stick value itself is not judged.
5. Camera clear: every step, the line from the car (or the person) to the camera is tested against the page's
   own camera collision world; more than 0.5 m of the camera past a solid counts. Pictures after the big crashes
   and the wedge are checked for one flat colour filling over 60% of the frame.
6. No page errors (console errors, uncaught exceptions), menu pause and resume work, and the longest stretch of
   pressing with nothing moving is reported.
7. A person hit by the car: a walker is held still and driven at at about 12 mph (up to 16 walkers, until one is
   touched). Passes only if the person is hurt, not killed, and a message appears within 3 s. No person touched
   fails as not reached. Other people touched on the way are counted.

Crash lines are aimed at named kinds of thing at each speed (a pole, a parked car, a wall) and the report names
what each really hit (wall, lamp post, post, bollard, parked car, traffic, police car).

## Run

    node --test                         # the pure measures, on made-up data (lib.test.js)
    node gate.js <saved page.html> <out folder>

The page is only read: it is served from memory by a tiny local server, Google Fonts are blocked (the cloud
cannot reach them), and nothing is written to it. The out folder gets report.json (every number and every
failure with the exact steps) and three pictures. Keep the out folder outside the repository. Exit code 1 means
at least one invariant failed. A run takes about 10 minutes here.

## How it drives

Software graphics draw about 4 frames a second here, so the gate holds the page's own frame loop
(window.QR.hold) and advances the world itself, in two ways (driver.js explains both):

- Steering is measured on the page's real frame loop: page.js catches requestAnimationFrame before the page
  loads, and the gate calls the page's own frame function with timestamps 1/60 s apart, drawing skipped. So the
  page itself polls the pad, takes button presses, ramps the keys through Input.step and steps the world.
- Everything else uses the gate's copy of that loop (window.QR.run with the page's Input.step), polling once per
  1/60 s frame and stepping at 1/120 s. The page has no exposed step that reads input. The copy differs only in:
  gear up and down flags always off (automatic gearbox), no look-back or right-stick look passed to the camera.

Keys are real key events sent by Playwright; the controller is a fake navigator.getGamepads put in before the
page loads. Messages are read from the page's message line (#toast) at every step, so each has the game time of
the step that showed it.

## Limits

- Not real time: it measures the game's logic, not frame pacing on a real PC. A stall or uneven frames caused by
  drawing would not show, and the camera's drawn smoothness is not judged.
- The car is placed at the start of each crash line (window.__place mends it first); a newcomer would get
  there by driving. After a crash nothing is mended or moved by the gate.
- The page's own collision world is the limit of what the gate can see. Static crash lines and the camera check
  both use the camera's collision world (walls, buildings, lamps, posts, bollards; not parked cars or traffic,
  which are too low for it). Anything drawn but not solid there, or solid but not drawn, is not found, so
  "camera clear" is close to always true by construction. Parked-car lines are aimed from the cars' own
  positions; traffic is hit only by chance.
- A message stays on screen for a set number of real milliseconds; the gate steps the game faster than real
  time, so how long a message stays up in game time is not measured, only when it appears.
- Damage in words is read from the message line only; pictures are kept but not judged for dents or smoke.
- The person rule judges the page's walker object (state, any hurt or dead flag); a game that shows a hurt
  person only in pictures would need the rule extended.
- It reads the page's test object window.QR and the bundle's requestAnimationFrame use; if a later round
  renames them the gate stops at load.
