# Driving gate: the clumsy player

An automated newcomer for the browser driving study (Quay Run). It plays a saved copy of the published page in
headless Chromium, keyboard first and then a simulated standard-mapping controller, crashes, reverses, gets out
and back in, wedges the car, spams buttons, pauses and resets, and after each scenario checks:

1. Never stranded: after any stop the player can move again within 5 s (car under throttle or reverse, or on
   foot). When the car will not move it records what does work (Backspace reset, R repair) and whether the
   screen said so.
2. Damage told and recoverable: after a hit the screen says the damage in words; a car that will not drive on
   says so and what to do.
3. Smooth on keys: steering input, the car's steering and its yaw rate are read every physics step while A and D
   are tapped and held at 30 mph. A snap is 10% to 90% of the move within 2 frames at 60 Hz; a jerk is a yaw-rate
   change over 0.15 rad/s in one frame that is also 3 times the typical change. Rows after a collision are
   left out (speed falling by more than 1.5 mph in one step).
4. Smooth on pad: the same with the stick at 0.25, 0.6 and 1.0, moved over 80 ms, and 1.0 at once.
5. Camera clear: every step, the line from the car (or the person) to the camera is tested against the page's
   own camera collision world; more than 0.5 m of the camera past a solid counts. Pictures after the big crashes
   and the wedge are checked for one flat colour filling over 60% of the frame.
6. No page errors (console errors, uncaught exceptions), menu pause and resume work, and the longest stretch of
   pressing with nothing moving is reported.
7. A person hit by the car: one walker is held still and driven at around 10 mph; what happens to them is
   recorded.

## Run

    node --test                         # the pure measures, on made-up data (lib.test.js)
    node gate.js <saved page.html> <out folder>

The page is only read: it is served from memory by a tiny local server, Google Fonts are blocked (the cloud
cannot reach them), and nothing is written to it. The out folder gets report.json (every number and every
failure with the exact steps) and three pictures. Keep the out folder outside the repository. Exit code 1 means
at least one invariant failed. A run takes about 10 minutes here.

## How it drives

Software graphics draw about 4 frames a second here, so the gate holds the page's own frame loop
(window.QR.hold) and advances the world itself in 1/120 s steps through the page's own hook (window.QR.run),
doing what the frame loop does each step: read the controller, take button presses, ramp the keys through the
page's Input object, step. Keys are real key events sent by Playwright; the controller is a fake
navigator.getGamepads put in before the page loads. Targets are found, not hard-coded: straight lines that end
in something solid at the right distance for each speed, read from the page's camera collision world.

## Limits

- Not real time: it measures the game's logic, not frame pacing on a real PC. A stall caused by drawing would
  not show.
- The car is placed at the start of each crash line (window.__place mends it first); a newcomer would get
  there by driving.
- What is hit depends on what lies at the end of each line (wall, lamp, bollard, parked car, traffic); the
  report names it. Thin things such as lamps are hit only when a line happens to end on one.
- Damage in words is read from the page's message line (#toast) only; pictures are kept but not judged for
  dents or smoke.
- It reads the page's test object window.QR; if a later round renames it the gate stops at load.
