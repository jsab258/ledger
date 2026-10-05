# LEDGER: the milestones

Outcomes, in order. The old roadmap and its 979-item feature checklist are in
production/archive/ROADMAP-checklist-to-2026-09-24.md: a reference to check
for missing basics at each milestone, not a gate.

## Now: one integrated encounter (Jafar, 24 September)

Visual work pauses until this exists. In the packaged build, with the new
player character:

1. The player commits a crime on the street by their own input.
2. A witness sees it through the real perception code.
3. What the witness knows spreads through the real gossip, and the
   conversation helper answers from the simulation's actual memory and
   knowledge of that day.
4. There is an audible consequence in the street.
5. The player talks to someone who knows, and is questioned about it.
6. The player quits the game completely, restarts it and loads the save from
   disk, and the town still knows.
7. The unwitnessed control, from an equivalent clean start: nobody sees it,
   and nobody knows.

When it passes, it becomes the regression the build runs.

PASSED 24 September: all seven hold in the packaged build, it is the build's
regression, and a playable version with the cast runs beside it.

## Next: a slice you can play, ten to fifteen minutes

Where it stands, 24 September evening: the street, three cast MetaHumans, the
crime, being seen, hearing about it later, typed talk answered aloud in the
cast's voices, quit and come back; 73 fps at his screen size. Not yet: the
packaged copy he plays, a spoken answer inside two or three seconds, plain
clothes, local line-writing.

Walk the street, talk to two or three people in their cast voices, commit the
crime, be seen, hear about it later, in the packaged build, and at 60 frames a
second at Jafar's screen size with the voice running. Conversation fast
enough to feel like talk. The router changes on the list: worked examples for
the paid router, typed orders answered as refusals, the game's own block
widened; the blind test of local line-writing, a priority because writing
lines is about 70 percent of the cost of talk.

## Then: a thirty-minute build for his friends

The block becomes the Hook: Mickey's interior, more buildings, more residents,
a session worth repeating. Before anyone outside his friends plays, whatever
the final model: every live AI call through a server of ours (the key never
ships; model and provider swappable there; a spending stop well below the
provider's cap; each copy's allowance counted), a notice that players are
talking to an AI, a way to report bad output, Steam's safeguards description,
and the content rule enforced on everything said live.

## The six stages, the longer arc

| stage | the milestone, his words | how it is judged |
|---|---|---|
| 1 | One street that looks right. | His eye, beside the Hook sheet. |
| 2 | One street that lives: residents on schedules, varied bodies, a face that moves and a voice, foley and an ambient bed. | His eye and ear; conversation latency inside its budget. |
| 3 | One street that knows me: the crime loop visible in a place that looks right. The milestone to protect if anything slips. | A witnessed crime reaching a second and a third resident within one in-game week, at frame budget, Core tests passing, arrest reachable from live play. |
| 4 | The player's shell: menus, save, settings, controls, the Ledger and the first hour. | His own UI and game-feel standard. |
| 5 | The block becomes the Hook. | The four Meridian Test conditions read off one session. |
| 6 | Then the town. | Hours of content without repetition; Meridian conditions 2 and 3 sampled. |

### Owed to the stages, with their specifics (Jafar, 1 October, from the rulings sweep, production/audits/rulings-sweep)

Each was ruled and never built or carried; it stays here with its specifics until it is on the builder's or the town's list and then built.

- **Stage 1, presentation** (D28): film grain, a slight chromatic aberration, lens dirt, a grade toward the period's film stock, and depth of field in conversation; only the engine's defaults run today (production/specs/unreal-look.json's post-process). Comes with the proof frame's grade (item 13).
- **Stage 2, moving traffic** (G4, 23 September: "in the street now, because a street with no traffic feels dead"): cars moving through the street, and the firm's cars driven by others; the traffic model is in the C# Core (Traffic.cs) and the old Unity build only, so its port into the game.
- **Stage 2, the street's people perceive, remember and gossip, as D25 says** (everyone perceives, remembers and gossips): the people seen in the street are "seen and not simulated" today (street-people.json); give them perception and memory in the game's spawn, or a ruling of his to remove them.
- **Stage 2, the voice experiment's first two steps** (24 September, cheapest first): per-line emotion taken from what the character feels (the talk program's mood, as a direction to the voice server), then paralinguistic tags; acted references and VoxCPM2 were the later steps and were tried.
- **Stage 2, the performance check against his target**: 60 frames a second at his screen (3440 by 1440) with the voice running, never below 30, logged by the route walk or the AI tester on every build; the last measurement is from 24 September, before the MetaHumans, the shop rooms and the cloth.
- **Stage 3, the crime layer's owed verbs, in order** (D56): order a man hurt, point a plan at a person, frame someone, lean on a witness, move a body, sanction crew, hit a rival's property, have someone vouch; then the press through a person, grassing, and combat's three gaps. Core first (the town), then the port (the builder).
- **Stage 3 and 5, the genre items ruled in** (G1 to G12, 23 September; canon): climbing low walls and fences (G1); crew acting on Tom's orders (G2); fists and improvised weapons (G3); short, skippable cutscenes (G6; the game has no sequencer module yet); the coat and its pockets (G9); buying, selling and fencing (G10); killing (canon). Most exist in the C# Core or the Unity build; none is ported.

The presentable milestone of 23 September was recorded complete; confirm it by
walking it. Business direction, provisional: sold once, an allowance of live
talk per copy (DECISIONS.md).
