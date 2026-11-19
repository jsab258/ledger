# The loop prototype's publish gate: findings (19 Nov 2026, second run after the review's fixes)

Lane, task 4o part b. The gate is in tools/lane/gate/ (README there). Run on the prototype as published
(page version 1795032844-05a0, rebuilt here byte for byte), a fresh new game for every scenario, 19 Nov,
about 9 minutes. A fresh reviewer checked the first run against the game's source
(production/lane/GATE-REVIEW-2026-11-19.md); this second run is after the gate's own faults were fixed.

## What the gate now does differently

- "Told on screen" reads the game's own message lists every frame from the frame of the crash or the hit:
  the subtitles, the Noted line when it is really up, the Noted lines still waiting, the newspaper, and what
  people within earshot say. It matches only the game's own lines for that event, taken from its source
  (kinds.js and talk_lines.js), and a test fails if that wording changes.
- Crashes aim at named things the game draws: lamp posts, bollards, parked cars, a moving car, and walls. The
  cab's damage is set back to 0 before each crash, so every crash is judged.
- Tom walks at every one of the 88 things drawn on the street, to catch things drawn but not solid.
- Steering is judged on the key going down, the key coming up, and a straight switch from A to D, at a steady
  speed. It passes only if the turn builds up over at least about 0.1 s and no one frame jumps more than a fifth.
- A check that could not be made fails as "not reached". The gate never passes without the hands-on write-up.

## Real faults in the game (all confirmed in this run)

1. A crash is not told in words. 11 crashes that did damage (bollards, parked cars, walls, a moving car, 12 to
   26 mph): none showed a line about it within 1.5 s. The game's only words are the Ledger's "Noted" line, and
   only when someone saw it. After 4 crashes the screen showed only "Noted in the Ledger: N things", which does
   not say what happened; in 3 the game's own crash line was waiting but never came up in time; in the rest
   nothing at all. Steps: put the cab 9 to 36 m from a bollard, parked car or wall, hold W.
2. Lamp posts are drawn but not solid. The cab drove straight through all 3 lamp posts aimed at (20 to 28 mph),
   and Tom walked through 29 of 30 (the 30th stands by the bus shelter, which stopped him first). So no lamp post
   crash could ever be judged. Steps: stand 2.6 m from any lamp post, face it, hold W.
3. Parked cars are not solid on foot. Tom walked through all 7. The cab does hit them. Steps: stand 4 m from a
   parked car, face it, hold W.
4. Keyboard steering snaps, three ways: the turn goes from nothing to full in one frame when D goes down, from full
   to nothing in one frame when it comes up, and from full left to full right in one frame on a switch from A to D.
   This is his "jerky keyboard steering".
5. A person knocked down is not told on screen in time: the game's own line was waiting at once but did not show
   within 1.5 s. No choice is offered (the only prompt is "Get out"); his ruling of 18 Nov is not built yet.
6. Driving at one person (Ron Kirby, held still, the cab from 14 m back) also knocked down two others nobody aimed at
   (Darren Milner and Kevin Needham). Nothing said so.
7. A pad moves neither Tom nor the cab (by design it works only the Ledger). "Every input device usable" fails.
8. Indoors, the camera hides Tom behind a near wall at Regent House (the boarding house), walking into the wall
   nearest the camera; a solid 0.72 m from Tom.

What passes: never stuck on foot, in corners, indoors (36 pushes in 9 rooms) or in the cab after any of 10 hits;
the cab is stopped by bollards and parked cars; a person hit is hurt (0.49 of 1), not killed; out of the cab
onto open ground; pause and resume; save and load; back to play after 300 random keys; no page errors.

## Still not measured (the README's Limits)

- Real time: frame pacing, hitches and camera jerk while driving. Sound and screen shake are not counted as telling.
- Things drawn some other way than the street props list (the quay railings, building details) are not walked at.
- What happens after a run-down (police, gossip, getting up).
- The camera check still ignores a fixed distance near Tom and is not run while driving.

## For the main session

- Nothing to merge into the game; the gate is lane tooling. The hands-on part has a helper send key presses to a
  headless browser in the cloud; CLAUDE.md's "Helpers never send clicks or keys" comes from rulings about
  computer use on his PC (29 and 30 Oct), which this is not, but the line's owner may want to say so.
- KNOWN.json is now keyed by rule plus what it was about (for example "keyboard steering eased | release").
