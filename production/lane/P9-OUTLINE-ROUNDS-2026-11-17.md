# Parked cars: the plan reviewed, the loft generator, and two outline rounds (17 November 2026)

Lane session, n16-9, queue item 1. Machine-free: nothing built in Blender or Unreal, nothing rendered on the PC.

## 1. The plan checked against its sources (PLAN-PARKED-CARS-2026-11-17.md)

Corrections the main session should carry into the plan when it next touches it (the lane does not edit it):
- Plates, section 3: year letters never used are I, O, Q, U and Z (the plan leaves out Q). Characters in 1990 were 79 mm high and 57 mm wide, stroke 14 (V796), not the 2001 font's 50 mm. Source and the rest: production/research/lane/HATCH-CLASS-AND-PLATES-2026-11-17.md.
- Sizes, section 3: the class ranges measured from eight real cars: height 1,370 to 1,450 (plan 1,360 to 1,420), wheelbase 2,430 to 2,550 (plan from 2,450), length to 4,250 (plan to 4,200). Wheelbase over length 0.60 to 0.645 (no real car reached 0.66).
- Tax disc: round, about 75 mm, on the nearside (left) of the windscreen; the lower corner is custom (UNVERIFIED).
- Section 5 hours and the order's 12 h: the plan's own judgement stands (25 to 41 h for the first car). This run takes part of step 1 (the loft generator, written and tested as pure Python) and step 2's brief, so roughly 4 to 6 h of steps 1 and 2 are done machine-free; the Blender side still needs its first run.
- "His silhouette answer": none found here either; the P9 brief below is the blind test as written in 3-PROOFS.md and 2-VEHICLES.md 3.6.
- Reference games: unchanged ("none found" for numbers; Mafia spawns traffic, parks none).

## 2. What was made

- tools/lane/car_loft.py: the twelve stations (nose tip, bumper face, headlamp, front axle, screen base, roof front, B-pillar, roof back, rear axle, hatch base, tail, tail tip), each a nine-point half cross-section with the same topology (shoulder, inward lean of the glass, sill tuck), from about 30 numbers; class-range checks; a triangle estimate against the 40,000 budget (about 16,800 at two subdivision levels with wheels and details); flat SVG outlines (side, front, three-quarter). Run: `python tools/lane/car_loft.py` (prints PASS or each failure).
- tools/lane/test_car_loft.py: 16 tests, all pass here (Python 3.13).
- tools/lane/car_loft_blender.py: UNTESTED, needs the main session's run. Bridges the stations into one mesh, paint and glass slots, subdivision, arches by boolean, weighted normals, UV0 and UV1, glb export, and the four P9 renders untextured (--render-p9). Its docstring has a four-step first-run checklist.
- production/lane/P9-BLIND-BRIEF.md: the reviewer's brief, word for word, with pass and fail read as numbers.

## 3. Two outline rounds (a screen, not P9)

Flat outlines from car_loft.py, three views each (front and rear outlines are identical without lamps), a fresh helper per round with the brief's questions, no other context.

| Round | Shape | Best guess | Sure | Region, years | Read as |
|---|---|---|---|---|---|
| 1 | hatch glass at 52 degrees ending 0.30 m before the tail | Ford Sierra Sapphire 4-door | 15 | Europe (Britain or West Germany), 1984 to 1992 | a three-box saloon: the short deck behind the hatch reads as a boot |
| 2 | hatch at 56 degrees, ending 0.10 m before the tail | Volvo 740 estate | 20 | Europe (Sweden or Britain), 1982 to 1992 | an estate: long flat roof into an upright tail |

Both pass the brief's numbers (under 50, Europe, overlapping 1985 to 1991), but neither reads as a hatchback, and round 2's first guess is on the named-at-a-glance list (Volvo 740), even at 20. The two rounds are used (two tries); the next look is the real P9 on the Blender renders.

Findings for the build (both reviewers):
- The roof is too long and flat; the tail needs a hatch that falls from the roof, between round 1 and round 2. Not tried in a round: ROUND3_PROPOSAL in car_loft.py (roof falls 60 mm to a 40-degree hatch ending 0.14 m before the tail, nose 20 mm higher, screen base 60 mm forward); it passes every check; its side outline is p9-outlines-2026-11-17/round3-proposal-side.svg and reads as a hatch by the lane's eye. Recommended as the shape for the first Blender run (`HatchParams(**ROUND3_PROPOSAL)`).
- Flat sides with no shoulder line; the nose has no bumper or grille plane. The bumpers and nose module come at step 3; a shoulder crease could be one more section point (would change the topology, so decide before shape keys).
- Front view: the body sits high over thin tyres. Partly the flat drawing (no bumper below the body), partly real: keel at 0.22 m; check it against the arches in the first render.
- The three-quarter drawing's wheels show through the body (a fault of the flat drawing only, not the shape).

## 4. For the main session to merge or decide

- Merge tools/lane/ (three files) and these two production/lane files as they are; nothing else touched.
- Decide: first Blender run with ROUND3_PROPOSAL (recommended) or the default.
- Plan corrections in section 1 into PLAN-PARKED-CARS when the item next runs.
- RECIPE line (the main session owns RECIPE.md): "A fictional vehicle's body: loft about twelve cross-sections of fixed topology from class numbers measured off real cars (dimensions only), check ratios in code, and screen flat outlines with a blind reviewer before any 3D render; a short deck behind the rear glass reads as a saloon, a flat roof into an upright tail as an estate."
