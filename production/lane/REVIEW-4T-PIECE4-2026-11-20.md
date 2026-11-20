# Review of 4t piece 4, feel in numbers (20 Nov 2026)

Reviewer: a fresh Opus helper at high effort, reading the code and running it (tests 6 of 6; its own run reproduced the first run). Verdict: PASS WITH FIXES (2 must, 3 should, 6 minor). The fists and steering measures and the frame hold were found sound: the game's step is exactly 1/60 s each frame, the camera code runs (follow time constant measured 0.103 s against 0.1035 predicted by the game's smoothing), hiding the scene changes no measured value, holding the cab on its spot does not change its turn rate.

| # | Finding | Kind | Fixed |
|---|---|---|---|
| 1 | The cab's bands were the 17 Nov ordinary-hatch set; since his 18 Nov ruling the driving sheet's default is the game set (M5 0.15 to 0.25 s and 0.4 to 0.9 s; M10 5 to 6.5 m, 1.6 to 2.0 m, 0.1 to 0.25 s). The steering was reported outside when it is inside | MUST | Yes: game set by default, the old set kept behind --ordinary |
| 2 | The cab camera drill drove nowhere (street traffic in the cab's space) and no fault said so; lag silently not measured | MUST | Yes: cars are in the clear-line search; the straight is searched again just before; up to three tries; a cab that is not clear or does not reach 90% of the held speed is a fault, never a number. Rerun: try 2 drove, lag 0.103 s |
| 3 | M10 measured at 9 m/s; the sheet's field-of-view band is at 30 mph | SHOULD | Yes: held at 13.4 m/s, judged against 64 to 70 degrees (measured 87: the view does not widen with speed) |
| 4 | W5, W6, W7 do not match the method's definitions | SHOULD | Renamed to say what they are (W5_cam_flat_m and W5_cam_straight_m, W6_cam_up_m, W7_cam_follow_tau_*); the method's own numbers listed as not measured |
| 5 | Gaps against the task (90-degree corner, contact window, miss recovery, hook, fight camera wall, close-in, shake) | SHOULD | Listed in every report under "Not measured by this tool (yet)" |
| 6 | Frame counting consistent and matching the sheets | MINOR | Nothing to fix |
| 7 | Frame hold sound; game code timed by the real clock is not held, no drill uses it | MINOR | Nothing to fix |
| 8 | Holding the cab's place does not distort the turn rate; full lock instead of the sheet's 2-degree step, harmless here | MINOR | Noted |
| 9 | The fist drills run with the suitcase back in his hand, unsaid; lost if a drill broke | MINOR | Yes: said in the drill's steps; put back in a finally after every drill |
| 10 | Props for the clear-line search come from the repository source, not the tested build | MINOR | Open (the same as the machine checks; a build from the same tree is the normal case) |
| 11 | Verdicts honest; half-frame tolerance written down | MINOR | Nothing to fix |

Known after the fixes: the cab's wedged flag can stay set from the drill before at a new spot (seen once on try 1 while the cab drove at 13.3 m/s); the check stays conservative and the retry passes.
