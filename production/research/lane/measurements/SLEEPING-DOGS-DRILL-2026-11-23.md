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

## Drill 1 read (23 Nov 21:40 to 21:50 Swiss, by eye on two labelled contact sheets of the legs, 44 and 50 grabs)
- **W alone (walk4):** a jog, not a walk, all 4 s (heels flick up behind, arms pumping). Step rate about 3.4 a second (soles seen up at about 0.29 s steps; one sample, read by eye at a 90 ms grab step against a 290 ms step, so ±0.4). A lead, not solid.
- **W with Shift (run4):** a faster run, and at about 1.0 to 2.1 s the run key carried Wei over the cardboard and round a hanging net in an automatic vault and turn (grabs 13 to 26): in this game the run key also does the free-running. So run4 is not a clean straight run; a speed run needs open ground.
- **Speed not readable from this drill:** the distance-to-Naz readout (45 m to 32 m in walk4) mixes in Naz's own running, and nothing in view has a known length. The ruler has to come from a still target (the readout while Naz stands, or a checkpoint marker) or a counted run of paving over open ground. A slow walk needs its own key (none found on W alone): look up the game's controls page before the next run.
- Next runs (each about 7 min from launch, after 10 idle minutes): hold W and W+Shift on the open quay after the chase, not in the market lanes.
Hours: 0.2 measuring (reading).
