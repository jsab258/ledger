# Breakers (lane task 4t, piece 3)

Written by the cloud lane, 20 Nov 2026. Four players whose only aim is to break the build, on Sonnet, once per loop, each a fresh helper through the same play.py as the player types (the screen and the keys, nothing else; one server per helper, its own --hidden folder). Unlike the player types they are not looking for fun and have no patience budget: they play until the session's time is up (default 30 minutes each) and report every crash, soft lock and piece of nonsense they can make happen. Like the player types they are blind to the design documents, canon and our intentions: what they find must come from what the game lets a person do.

Method, as the research file says (production/research/lane/AI-PLAYTESTING-METHODS-2026-11-20.md): goal-driven agents who hunt one class of fault each find more than one agent hunting everything, and every claim is replayed by machine before it counts (replay.py), because a model's report of a fault is a lead, not evidence.

## A. The money cheat
- Aim: more money than the game means Tom to have, or money from nothing: paid twice for one job, money paid out that comes back as cash, a fare paid with nobody in the cab, money kept through a save and reload that should have gone, a pocket below nothing, money that is not whole pence.
- Tricks to try: repeat the same paying action fast; save and reload around a payment (the pause menu); quit a scene half way and start it again; pay and walk away; pay with the talk box open; drive off mid-fare.

## B. The story skipper
- Aim: reach a later part of the story without the earlier part, or end up where the story can no longer go on (a soft lock): an aim that names a person who is gone, a place that cannot be reached, a scene that never ends, a choice that leads nowhere.
- Tricks to try: ignore every aim and wait out whole days; go to the aim's place before being told; close every scene the moment it opens; pick the last choice every time, then the first every time; sleep or wait through every time the game names.

## C. The runner-over
- Aim: break the rules about people and the cab: someone killed, someone who stays on the ground for ever, the same person hit again and again with nothing happening, people inside walls or the cab, the cab inside a building or under the ground, Tom out of the cab while it still moves, the camera inside a wall.
- Tricks to try: drive at people, at crowds, at walls, at full speed into corners; get out while moving; reverse into people; park on the pavement; drive into water or off any edge.

## D. The talk spammer
- Aim: make talk say nonsense, repeat itself, contradict what happened, break the period (anything wrong for the time and place the game itself shows), or break the content rule; make the talk box stick open or eat the keys.
- Tricks to try: talk to the same person twenty times; type nonsense, very long lines, numbers, other languages, words from later decades than the game's; ask about things that have not happened; open talk while driving, while someone is hurt, during a scene; spam the talk key and Escape together.

## What each breaker returns
JSON only:

{"type": "money cheat", "minutes_played": 0, "faults": [{"n": 0, "minute": 0, "class": "money | soft lock | stuck | people | cab | camera | crash | talk | period | content | other", "what": "...", "shot": "...", "steps": "..."}], "tried_and_held": ["what the game resisted, one line each"]}

"n" is the action number play.py gave with the screen where the fault showed (each answer carries it). A fault with no n cannot be replayed and counts as unconfirmed.

## How a claim becomes a finding
replay.py reads the breaker's report and its --hidden folder's actions.jsonl (with the session's seed), replays the same actions in a fresh game up to the fault's action, and first checks that it reached the same game (day, clock, money, Tom's place). Then by class:
- crash, stuck, camera, content: a machine test that sees the whole claim (a new page error while that action ran; Tom walked off four ways; the line from Tom to the camera; the content word list against the words on screen). Fails: REPRODUCED. Holds: NOT REPRODUCED.
- money, people: a machine test that sees only part of the claim (money: whole pence, a real number, the pocket never below nothing; people: inside a solid for 1.5 s, or under 18). Fails: REPRODUCED. Holds: NEEDS A LOOK, since "paid twice" or "a person left on the ground" cannot be seen at one moment.
- cab, soft lock, talk, period, other: no machine test yet: NEEDS A LOOK.
For every NEEDS A LOOK the replayed screenshot is saved beside the original, and the panel (piece 6) or the loop's judge decides from both. A replay that went another way is NOT REPRODUCED with the reason. Only REPRODUCED faults, and NEEDS A LOOK faults the panel confirms, reach the loop's top three; nothing a breaker says is taken on its word. Words are not compared with the logged ones; the replay's state check stands in for that.
