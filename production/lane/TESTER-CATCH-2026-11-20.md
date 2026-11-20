# Testers' catch record, 2026-11-20

Faults planted on purpose in a copy of the game (4t piece 8, his plan of 19 Nov), each in an area where our testing or he met a real fault before (the change itself made up); the game's own folder is never changed. Made by tools/lane/gate/plant/plant.py, run at 2026-11-20T06:32+01:00, no model.

Caught by at least one tester: 7 of 7 faults planted and tested.

## Per tester

| Tester | Caught | Planted for it |
|---|---|---|
| clumsy | 2 | 2 |
| consequences | 1 | 1 |
| feel | 2 | 2 |
| machine | 3 | 3 |

## Per fault

| Fault | What it does | Tester | Caught | What showed it |
|---|---|---|---|---|
| telling-leaves-no-memory | a person is told something but does not remember it | consequences | yes | a telling leaves a memory: 35 failed, clean at most 0; a telling leaves a memory / told event 1 by darren at minute 1045; no memory of it; a telling leaves a memory / told event 1 by grace at minute 1001; no memory of it; a telling leaves a memory / told event 1 by grace at minute 1005; no memory of |
| loaded-week-loses-its-hour | loading a saved week puts the clock back to the start | machine | yes | save and reload give back the same week: 1 failed, clean at most 0; save and reload give back the same week / saveText after the long run; restore in a fresh page; saveText again and compare all but time stamps |
| run-down-not-told | a person run down by the cab and no words on screen | clumsy | yes | a person hit: told on screen: 1 failed, clean at most 0; a person hit: told on screen / test setup: Father Walsh held still on the street, cab 14 m back at 4.5 m/s on a clear line, hold W; the game's message  |
| steering-snaps | the cab's steering jumps to full lock at a key press | clumsy | yes | keyboard steering eased: 3 failed, clean at most 0; keyboard steering eased / test setup: cab on open ground at (-2, 40), kept on its spot and its speed held at 9 m/s each frame; after D held 0.6 s,; keyboard steering eased / test setup: cab on open ground at (-2, 40), kept on its spot and its speed |
| steering-snaps | the cab's steering jumps to full lock at a key press | feel | yes | M5_yaw63_s: outside |
| jab-too-slow | a jab takes twice as long to land | feel | yes | C2_jab_contact_s: outside |
| camera-through-walls | the camera stays behind walls instead of coming in front of them | machine | yes | camera never inside a wall (every named place) / Ada's front room (street door); camera never inside a wall (every named place) / Chapel Lane (fare pick-up); camera never inside a wall (every named place) / Metcalfe's (street door); camera never inside a wall (every named place) / Peart's (street do |
| drink-in-a-line | a line that speaks of drink | machine | yes | content rule in the game's words: 1 failed, clean at most 0; content rule in the game's words / every prose string in the game's source (48 files in the planted copy |

## Missed, for the next loop's list

- none

The AI testers (player types, breakers, the panel) were not run on planted builds this time; they are tested in a loop: each planted build stays in its own folder under the run's output for a loop to serve them.

## What this says (lane note, 20 Nov)

Every machine tester caught the faults planted for it, with the evidence above, and nothing counted that also moved between the two clean runs. Seven of seven means these faults are coarse: each breaks its rule outright. Next week's run adds subtler ones from that week's real finds (a fault at only one named place, steering eased but too slowly, a line repeated once), so the catch rate measures something. The AI testers are tested on planted builds in the first loop after the one-shot.
