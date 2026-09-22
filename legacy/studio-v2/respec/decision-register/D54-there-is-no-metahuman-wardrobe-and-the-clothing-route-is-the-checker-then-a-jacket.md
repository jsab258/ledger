# D54. There is no MetaHuman wardrobe; the clothing route is garment meshes on the shared skeleton, a checker first, then one jacket moved. Stage 2, nothing bought

CANON: none

Ruled by Jafar, 2026-09-21, first message, under "On bodies and movement, both
for stage 2", kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"There is no MetaHuman wardrobe. It ships one unnamed outfit, so the question
I was told to answer by opening MetaHuman Creator does not exist. Epic's own
documentation says clothing does not need skinning at all, which removes the
first named break in the clothing line. The route is: fourteen of eighteen
bodies already wear separate garment meshes on one shared skeleton, Blender's
weight transfer is on the PC, the clean script destroys clothing in four lines,
and the checker cannot tell a working coat from a ruined one. Build the
checker, then move a jacket between bodies. Nothing is bought. It waits for
stage 2."**

## What is decided

The route, in his order: (1) THE CHECKER, a tool that tells a working garment
from a ruined one. A tool that measures: a test, no review (D45); tested on the
case it should pass and on a planted ruined case, both watched (rule 5b); it
prints bodies examined, garments found, garments intact. (2) ONE JACKET moved
between two bodies through Blender weight transfer, verified by the checker,
shown in a frame. Both at stage 2 (`production/stages.md`, rung 4: people on
the street with varied bodies), and none of it before the visual slice (D29's
line for the whole stage). Nothing is bought: Mixamo garments are part of
Mixamo characters (D46; the allowlist line 6), Blender is already on the PC
(ruling of 2026-09-09, "the Blender that was always there"), no new tool
enters.

D46 left clothing undecided in as many words ("Nothing about ... rigging,
animation retargeting or clothing"). This record decides the route; it does
not touch D46.

## What is his, from the research, and not re-verified here

That MetaHuman ships one unnamed outfit; that Epic's documentation says
clothing does not need skinning; that fourteen of eighteen bodies wear
separate garment meshes on one shared skeleton; that "the clean script
destroys clothing in four lines"; that "the checker cannot tell a working coat
from a ruined one". Which script and which checker he means are not named in
his message and are not identified here; the research delivery that found them
is on its branch. What main holds, for the count: `game-design/research/
inhabited-street.md:225`, "Component drawables (separate garment meshes) |
HAVE, ON 11 OF 16" (25 Aug), and D46's eighteen `.fbx` bodies (2026-09-16).
Eleven of sixteen in August and fourteen of eighteen now are two readings on
two dates; they are not reconciled here, and the checker he orders is what
reconciles them, by counting.

The question "I was told to answer by opening MetaHuman Creator" was not found
on main: grep for "MetaHuman Creator" over the tree returned only his message,
and neither of the two 2026-09-16 outbox messages carries it (both read). It is
in the research delivery on its branch; its mark lands with the consolidation.

## Corrections under D43, with sites

- `production/specs/vignette-bill-of-materials.md` lines 466 to 467: "The
  character wardrobe is contemporary (F1, F2), against a 1988 to 1992 setting,
  and there is no free re-dress route." The second clause is false by this
  ruling. Dictated one-line fix for the resident: replace "and there is no free
  re-dress route" with "and the free re-dress route is D54's: garment meshes
  on the shared skeleton, moved by Blender weight transfer, checker first, at
  stage 2".
- `production/quality-ladder.md` line 134, "period wardrobe stays the research
  row the BOM named": still true, and D54 is the route that row's next rung
  cites when the planner re-opens it at stage 2. No edit.

## What this does not decide

What the period wardrobe contains: the art lane's six character concept
sheets (queue 393 in the resident's log) are what the clothing line aims at.
Faces (D2). MetaHuman for anything else.
