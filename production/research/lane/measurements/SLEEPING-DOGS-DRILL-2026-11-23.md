# Sleeping Dogs drill: the opening and a first walk and run (23 Nov 2026, 20:26 to 21:05 Swiss)

Built on: INSTALLED-METHOD.md (openings by fixed key scripts, two tries; the drill steps), FILM-RULER-2026-11-23.md (the fast film), advisor 333 and the efficiency review of 23 Nov 19:44.

Tool: tools/drills/watch_opening.py (starts the game, a FIXED list of timed taps and walk/run holds written before each run from the previous run's frames, films the game's own window, stops at his first touch, closes the game). Frames: F:/LedgerTools/tmp/drills/sdhdship-opening-2026-11-23-*.

## Runs
| run | keys | what happened |
|---|---|---|
| 2026 | none | logos, then "press any key" from about 37 s |
| 2031 | Enter 45, 56, 64 | no key sent: the game was not in front (a game started from a background process is not handed the front); the tool now brings it forward as the tester does |
| 2032 (opening try 1) | Enter 45, 56, 64 | title, autosave notice, then the first-time setup at about 78 s, where the keys had run out |
| 2043 (opening try 2) | Enter 45, 56, then every 6 to 9 s from 82 to 138 | through the setup and the opening scenes; control in the night-market chase from about 254 s ("Follow Naz", a 20 s countdown, a distance to Naz in metres on screen); mission failed at about 285 s ("You lost Naz") |
| 2055 (drill 1) | as 2043, then walk 4 s at 258, run 4 s at 265, Enter at 300 | walk and run filmed; Wei moved down the market; no fail screen this time (he kept up); Enter at 300 did nothing visible |

## What it gives
- The opening is got through by a fixed script in about 4 minutes (two tries used, both kept within the rule; the second succeeded to the first controllable moment). There is no game save yet; each drill run starts from launch (about 4.3 minutes) unless a checkpoint save appears.
- In this game the fast film grabs at about 11 to 12 a second, each grab taking about 81 to 91 ms (the window gives its picture slowly), so a frame's moment is known to about 45 ms. Enough for a speed over 4 s (about 2%), not for starts and stops.
- Not yet measured: the walk and run speeds. A distance is needed on screen: the market's herringbone paving, or the distance-to-Naz readout while Naz stands still. Next: measure the paving brick in this game first (its own model in view), then read Wei's progress per frame.
- Holding W alone already moves Wei at a jog in the chase; whether Shift changes the gait needs the frames compared side by side.

Hours: 0.65 measuring (drills), logged in STATUS.md.
