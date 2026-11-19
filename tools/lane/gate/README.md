# The publish gate for the LEDGER loop prototype (4o, part b)

Written by the cloud lane, 19 Nov 2026, from his decision of 18 Nov 21:54 (advisor 233): "We need to a) avoid
having such issues in the prototype in the first place and b) if they still appear, catch them before it's
published to me." Nothing is published to him unless this passes. The driving study's gate is its sister,
in ../driving-gate/.

## The four parts

1. Scripted tests: the prototype's byte-for-byte build, Fable's tests and the lane's checks (gate.py runs them).
2. The clumsy newcomer (clumsy.py): a new game for every scenario, in headless Chromium, real key events, the
   game stepped by hand at 1/60 s through its own hook. Scenarios: walking into walls from two places in eight
   directions; ten corners found from the map; Tom walked at every thing the game draws on the street (lamp posts,
   bollards, bins, stalls, parked cars: read from the game's own data in map.js and render/sync.js), to catch
   things drawn but not solid; the cab driven into named things (lamp posts, bollards, parked cars, a moving car,
   walls) from 8 to 45 m, damage set to 0 before each crash so every crash is judged; keyboard steering on press,
   on release and on a straight switch from A to D, at a held speed; F pressed twelve times fast; a person
   held still and driven at; a pretend pad (stick and trigger); every shop door taken with E and its walls walked
   into; pause and resume; save and load; 300 random keys and back to play. Each checks rules in invariants.py:
   free again within 5 s of any stop, damage and a run-down told on screen within 1.5 s of the event frame (the
   game's own message lists read each frame, matched on the game's own lines for that event), steering eased
   (10% to 90% in at least about 0.1 s, no frame moving it more than a fifth of the way), drawn things solid, the camera's line to Tom
   clear of solid meshes, a person hit never killed and offered a choice, no page errors, no pause that nothing
   holds. A rule that was never reached in a full run fails ("tested something: ..."), and a check that could
   not be made (a target never hit, a box that kept opening) fails as "not reached", never passes.
3. The AI hands-on session: a fresh helper plays HANDS-ON-ROUTE.md (about 20 minutes, real controls, real time)
   with HANDS-ON-PROMPT.md, and writes HANDS-ON.md with BLOCKER, MAJOR and MINOR lines. gate.py reads it with
   --hands-on; without it the gate does not pass. A new BLOCKER or MAJOR line blocks; a line counts only when it
   starts with the marker, and "known blocker:" marks one accepted.
4. The note for him: gate.py writes NOTE.md, what to try and every known issue in plain words.

KNOWN.json lists failures accepted for now, each with its reason, so a round is judged on what it newly breaks.
Each key is the rule plus what the failure was about, as gate.signature() writes it ("camera clear | indoors:
Regent House", "keyboard steering eased | release"), so one accepted fault never hides another of the same rule.
It starts empty: the first round after his yes on the vision decides what goes in it.

## Run

    python -m pytest -q                                  # the gate's own checks (no browser)
    python clumsy.py --assets DIR [--out DIR] [--only cab_crashes,indoors]
    python gate.py --assets DIR --hands-on HANDS-ON.md --try "what the round added"

DIR holds the page's 13 pictures (see ../prototype/README.md). Outputs go outside the repository
(default ~/.cache/ledger-gate/). A full clumsy run takes about 4 minutes here.

## Limits (after the fixes of 19 Nov; the review is /production/lane/GATE-REVIEW-2026-11-19.md)

- Not real time: the game is stepped at 1/60 s, so frame pacing, hitches and camera jerk while driving are not
  measured. The "told" checks step one game frame per drawn frame so the page's own words run as in play, but the
  picture is off, so speech bubbles are counted from the game's list (within earshot), not from where they draw.
- Words only: sounds and the screen shake are not counted as telling. Overlapping or unreadable text is not checked.
- The props are read from the game's data code (map.js, render/sync.js). Something drawn some other way (the quay
  railings in render/extras.js, building details) is not walked at. Lamp posts on walls (brackets) are left out.
- The moving car is found in the drawn scene as a vehicle group, at whatever spot it has reached after 6 s.
- What happens after a run-down (police, gossip, the person getting up) is not followed; only one person is
  driven at, though others knocked down on the way are reported.
- Camera: one fixed distance is ignored near Tom (0.7 m on foot, 2.7 m in the cab); not tested while driving.
- Test setups: the cab keys are given, the cab and Tom are placed at the start of each line or spot, the cab's
  damage is set to 0 before each crash, the speed is held while steering is measured, and the person driven at is
  held still. Each is named in its result's steps.
