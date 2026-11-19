# The publish gate for the LEDGER loop prototype (4o, part b)

Written by the cloud lane, 19 Nov 2026, from his decision of 18 Nov 21:54 (advisor 233): "We need to a) avoid
having such issues in the prototype in the first place and b) if they still appear, catch them before it's
published to me." Nothing is published to him unless this passes. The driving study's gate is its sister,
in ../driving-gate/.

## The four parts

1. Scripted tests: the prototype's byte-for-byte build, Fable's tests and the lane's checks (gate.py runs them).
2. The clumsy newcomer (clumsy.py): a new game for every scenario, in headless Chromium, real key events, the
   game stepped by hand at 1/60 s through its own hook. Scenarios: walking into walls from two places in eight
   directions; ten corners found from the map; the cab driven into whatever ends twelve straight lines (8 to 45 m
   away, so about 10 to 30 mph); keyboard steering on press and on release; F pressed twelve times fast; a person
   held still and driven at; a pretend pad (stick and trigger); every shop door taken with E and its walls walked
   into; pause and resume; save and load; 300 random keys and back to play. Each checks rules in invariants.py:
   free again within 5 s of any stop, damage and a run-down told on screen within 1.5 s, the camera's line to Tom
   clear of solid meshes, a person hit never killed and offered a choice, no page errors, no pause that nothing
   holds. A rule that was never reached in a full run fails ("tested something: ...").
3. The AI hands-on session: a fresh helper plays HANDS-ON-ROUTE.md (about 20 minutes, real controls, real time)
   with HANDS-ON-PROMPT.md, and writes HANDS-ON.md with BLOCKER, MAJOR and MINOR lines. gate.py reads it with
   --hands-on; without it the gate is not complete and does not pass.
4. The note for him: gate.py writes NOTE.md, what to try and every known issue in plain words.

KNOWN.json lists failures accepted for now, each with its reason, so a round is judged on what it newly breaks.
It starts empty: the first round after his yes on the vision decides what goes in it.

## Run

    python -m pytest -q                                  # the gate's own checks (no browser)
    python clumsy.py --assets DIR [--out DIR] [--only cab_crashes,indoors]
    python gate.py --assets DIR --hands-on HANDS-ON.md --try "what the round added"

DIR holds the page's 13 pictures (see ../prototype/README.md). Outputs go outside the repository
(default ~/.cache/ledger-gate/). A full clumsy run takes about 4 minutes here.

## Limits (from the fresh review of 19 Nov, /production/lane/PROTOTYPE-GATE-FINDINGS.md)

- The "told on screen" checks read the words the page shows between steps; the page refreshes them only when it
  draws, and the word lists are guesses at the game's wording. They are provisional until they read the
  game's own message list from the hit frame on.
- Crash targets are chosen with the game's own collision map, so things that are drawn but not solid (the lamp
  posts) are never aimed at; drawn against solid is not compared yet.
- Not real time: frame pacing and camera jerk while driving are not measured. Sound-only messages are not heard.
- Traffic, parked cars and top-speed crashes are not aimed at; what happens after a run-down is not followed.
- Test setups: the cab keys are given, the cab and Tom are placed at the start of each line or spot, and the
  person driven at is held still. Each is named in its result's steps.
