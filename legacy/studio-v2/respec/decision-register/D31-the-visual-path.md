# D31: the visual path, in order, with the reason for each step. A SCHEDULING DOCUMENT: the route to the visual bar and not a reduction of it

STATUS: DECIDED 2026-09-14 by Jafar. The order and its five reasons are his
words, carried verbatim from D22. The placement of D28's ten steps inside that
order, the estimate's calibration and the pace rule are the director's reading
of the same day, and he reverts any line of it on one word. D27 binds the first
line above: the end state is pillar 5 of `ledger-v2/respec/vision-pillars-v2.md`,
photoreal grim Britain, and the bar this path serves is D23, the in-house Hook
sheet as a floor and not a ceiling. This record sits under stage 1 of
`production/stages.md` as the route inside that stage.

## The order, and the reason for each step, in his words

1. **Light and shadow first**, because it is most of the gap and shadows are
   what make a frame read as a photograph.
2. **Then surfaces**, meaning a real material library with roughness, normal
   and wear rather than colour maps.
3. **Then wetness**, because the reference street is wet and wet is mostly
   reflection.
4. **Then density of clutter** through the batch pipeline.
5. **Geometry detail LAST**, because it matters least and is the thing everyone
   reaches for first.

## D28's ten steps inside that order: one list, not two

D28's presentation steps are not a separate plan. They sit inside the order
above, and this table is the one list the week is worked from. "The visual
slice", where D26, D29 and D30 use the phrase, means this list. The last column
names the queue items that carry each step today, read 2026-09-14; a step with
none is named as owed and is the planner's to file, one deliverable each.

| order | D28 step | what it is, in his words | carried by |
|---|---|---|---|
| 1, light and shadow | 1 | Fix the exposure fault so the same camera and conditions give the same picture. | Queue 235, 219 and 208 are the spec (ruling of 2026-09-14). THIS STEP GATES THE JUDGING AND NOT THE WORK: nothing visual is judged until two photographs of one unchanged scene are the same picture; queue 235 records `rigDeterminism=DIFFERS rigDiffPixels=921600/921600` on the run on 83dec336. |
| 1, light and shadow | 2 | Light and weather: bring the sky down so the sun lands and the street has dark in it, measured against the in-house Hook sheet, with sodium lamps at dusk. | 205 (the sun-intensity series), 206 (set the sun and sky from the read curve), 224 (the sun's pitch against the spec), 240 (the shadow the instrument cannot see), 186 (the fog that hides the sky), 180 (rung 1). |
| 1, light and shadow | 3 | Post-processing: film grain, a vignette, bloom on the lamps, slight chromatic aberration, lens dirt, and a colour grade toward the period's film stock. | No queue item yet: a grep over `production/queue/` for grain, vignette, chromatic, film stock and colour grade names nothing of this. THE SOUND LANE OPENS AT THIS STEP (D26). |
| 1, light and shadow | 4 | Camera: field of view, slight head bob, motion blur, depth of field for close conversation. | No queue item yet: the same grep for head bob, field of view, depth of field and motion blur finds none. |
| 2, surfaces | 6 | The surfaces: a real material library with roughness, normal and wear. | 211 (worn materials), 223 (four surfaces with no maps), 196 (the flat grey furniture and the red box), 181 (rung 2); 176 is answered and stands as the finding that the near-white band is a kerb albedo, not exposure. |
| 2, surfaces | 7 | Wear and dirt through the decal system that already exists. | 055 (the G3 imperfection scatter), which carries the 2026-09-10 closure line and is re-opened by this record. |
| 3, wetness | 5 | Wire wetness. It is parsed and read by nothing, and the reference street is wet. | 186: a sky, a reflection source, and Wetness reaching the material, all three, because none works alone. See the adjacency note below. |
| 4, density of clutter | 8 | The twelve-package batch through all five stations, onto the street as real meshes, with cost per verified piece on the throughput ledger. | `production/art/fascia-01/` is package one and counts zero until station 4 is measured on the PC; `production/throughput.md` is the ledger; the batch order is the art line's, fascia first. |
| between 4 and 5 | 9 | Typography and the title card. | No queue item yet. Not a property of light, surface, water, clutter or geometry, so it sits where D28 numbered it: after the batch and before geometry. |
| 5, geometry last | 10 | The cab office from its Blender blockout, through GLB and the mesh route, standing on the street and photographed. | 182 (rung 3), `production/art/mickeys-cars/` (the design, D19), and the mesh route pilot package one proved. |

ONE ADJACENCY IS INVERTED BETWEEN THE TWO LISTS, AND IT IS RECORDED RATHER THAN
SMOOTHED OVER. D28 numbers wetness 5 and surfaces 6; D22 places surfaces second
and wetness third, and D22 says in its own words that D28 sits inside its order,
so the table follows D22. His sequence of 2026-09-09 (queue 211: the two trust
faults, then the sky, then wetness, then worn materials) agrees with D28. The
work does not change, only which of two adjacent steps is judged first, and the
work itself suggests the reconciliation: step 5 has two halves. The sky and the
reflection source (queue 186) are light and belong to order 1; the material half
of wetness is a roughness change and reads properly only once the surfaces
carry roughness, which is order 2. So it is WIRED when 186 lands and JUDGED
after the library. RAISED TO JAFAR as one line; the default until he rules is
as written here.

## What is deliberately excluded until the list is done

D28: more geometry, more unique buildings, animation polish. They are expensive
and read as improvements only after presentation is right. That is also why
geometry is fifth and last: it is the thing everyone reaches for first.

## The target frame

One screenshot of the street at dusk, wet, lamps lit, a figure in silhouette,
from the Hook sheet's own viewpoint (`cam_hook`), standing beside the sheet's
lower panel. That single frame is how Jafar judges whether this looks like a
real game, and D23 says what clearing it means: when he cannot say which way
the gap runs, the budget moves to stage 2.

## The estimate, and what kind of number it is

His words: **"Estimates are mine and untested: six to ten weeks to a frame I
would call convincing at a glance, against one measured piece of production
data, so the record says PLAN-TO-TEST rather than SCHEDULE."**

THIS RECORD SAYS PLAN-TO-TEST. NO GATE MAY READ THIS NUMBER AND NO PLAN MAY
QUOTE IT AS A DATE. It is not converted to a calendar date anywhere, including
here, and a document that quotes it as one is wrong.

What it stands against, named so the calibration is visible. The project's one
production cost measurement with a denominator is `production/throughput.md`,
pilot package one: 22 verified pieces crossed station 4 in one run on
2026-09-09; setup an UPPER BOUND of 22 engine-specialist, 7 instrument-builder
and 11 director spawns over 8 and 9 September, because the agent log cannot
split those days' spawns by line; the marginal cost of an import about 0.35
minutes of runner time per piece, measured over sixteen already-authored
assets; the cost of AUTHORING a piece unmeasured. One point is not a series
(rule 2), which is the whole reason the number is plan-to-test.

What dominates, per rule 7: the studio half, in sessions per step, and it is not
yet printed for any step of the list above. The runner's round trip is minutes
(2 min 07 s and 5 min 42 s, two samples) and does not dominate. What could blow
it up: a step whose instrument turns out to be wrong, which is the largest
hidden cost the 2026-09-14 ruling names and the reason no new instrument ships
this month unless one is retired in the same batch.

How the number gets tested rather than believed: each step prints its own cost
as sessions and runner minutes when it lands, on the throughput ledger's terms.
The first re-estimate is written when that series exists for the four steps of
order 1, and not before.

## Pace

His standing instruction, repeated 2026-09-14: "Do not wait for my verdict to
move to the next; my verdict adjusts, it does not gate." Step 1 is the one
exception and it gates only the judging: the work continues while the rig is
made deterministic, and nothing is judged until it is.

## Revisit when

A frame beside the Hook sheet where he cannot say which way the gap runs (D23),
which moves the budget to stage 2; or a gate failure that names this decision.
