line: art (the authoring line's first pilot: E1_lighting_column /
  E2_sodium_lantern_head, Blender geometry authored, VERIFY not reachable in
  this container)
spec: Jafar's ruling 2026-09-21, kept verbatim at
  game-design/decision-2026-09-21-ruling-the-lamp-column-is-authored-and-it-is-the-authoring-lines-first-test.md,
  then corrected the same evening by a message routed through the Producer:
  the column's FORM comes from the approved in-house Hook sheet
  (production/art/atlas-01/concepts/hook.png on origin/art/atlas-01) and
  game-design/research/art-direction.md, not from his first reply, which was
  general knowledge and stood down where the project's own material is more
  specific. Both were read directly for this task, not taken on report.

  WHAT LANDED: tools/art-recipes/lighting-column.py, a recipe that builds the
  column (base, shaft, a swept-tube neck, lantern body, recessed lens, a
  shallow pitched canopy roof, a small photocell housing) plus three wear
  patches (rain streak on the shaft, road spray at the base, staining below
  the lantern on the neck's dropper), through bpy.data only, never bpy.ops,
  mirroring tools/art-recipes/mickeys-blockout.py's method. Dimensions are
  read at run time from production/specs/vignette-scene.json
  (lighting.column, lighting.lantern), never retyped, and cross-checked every
  run against production/specs/vignette-pieces.json's actual column0/lantern0
  coordinates (`python3 tools/art-recipes/lighting-column.py -- --plan --root
  <repo>` prints crossCheckAgree=10/10 today). The neck departs from the
  blockout's naive "quarter circle of radius=outreach_m" reading, per the
  Hook sheet's long, shallow, gentle arc: a TRUE circular arc of 1.5x that
  radius (constant curvature, so "shallower" is closed-form, not observed on
  one number: see neck_arc()'s docstring), printing today
  authoredArcTotal_m=1.7303 against naiveQuarterArc_m=0.7854 (longer) and
  authoredCurvature_perM=1.3333 against naiveQuarterCurvature_perM=2.0000
  (shallower), while the two pinned endpoints (shaft top at mounting_height_m,
  lantern centre at outreach_m/mounting_height_m-lantern_height_m/2) do not
  move. wearCoverage prints per surface, D53 point 2's shape, minimum named:
  wearCoverageMin=0.000000/lantern (the lantern housing carries no authored
  wear in this pilot, by choice, not by inability to separate it; base,
  shaft and neck each carry a real nonzero fraction). All ten parts pass a
  pure-Python manifold and outward-normal check
  (manifoldParts=10/10); the checker itself was tested against three planted
  faults (an open box, a degenerate face, a reversed winding) and caught all
  three before this was written down.

  WHAT DID NOT LAND, AND WHY IT COULD NOT HERE: Blender is not installed in
  this container (`python3 -c "import bpy"` raises ModuleNotFoundError,
  checked, not assumed). Every line touching bpy in the recipe (materials,
  mesh instancing, camera/light setup, the two authored shots under
  overcast_day and wet_night, the render loop, the .blend save) ships UNRUN.
  The pure layer, everything above, is covered: `--plan` prints the whole
  plan with no Blender anywhere, and `--selftest` passes 48 of 48 against the
  live spec files as the accepting fixture, synthetic paths and malformed
  JSON as the rejecting ones (no pinned snapshot of a live value anywhere in
  it, the exact fault class queue 416 names).

  A REAL BUG WAS CAUGHT BY THIS PROCESS BEFORE IT SHIPPED, worth recording
  because it is the argument for the method: a first draft built the neck as
  a cubic Bezier between the same two pinned endpoints. It LOOKED gentler but
  its printed peak curvature (5.8819 per m) was HIGHER than the naive quarter
  circle's (2.0000 per m), because a Bezier's curvature is not constant and
  spikes where two unaligned tangents are reconciled. The plan output showed
  `shallowerThanNaive=no` on the first run, which is why the geometry was
  rebuilt as a true circular arc (constant curvature, so the comparison is
  closed-form rather than a hope). Printing both numbers and reading them,
  rather than trusting the description "long and shallow," is what caught it.

  NAMED AND NOT BUILT: the Hook sheet also carries a wall fixture on the
  Harbour Office, a dark conical bracket lamp with a WIRE CAGE GUARD over a
  warm bulb, mounted under the eaves. It is a real, different asset the
  street will need and it is explicitly out of scope here (Jafar: "That is a
  wall fixture, a real thing the street will need, and it is not this
  asset. Do not build it; name it in your queue item as a separate asset the
  sheet already specifies"). No spec entry exists for it yet in
  production/specs/vignette-scene.json's `lighting` block; one would need
  authoring before a recipe could read it, the same discipline this file
  followed for the street column.
acceptance: a REAL Blender run, on a machine that has Blender, is the
  accepting case this pilot cannot supply itself, exactly as
  tools/art-recipes/mickeys-blockout.py's first run was for atlas-01:

    blender --background --factory-startup --python tools/art-recipes/lighting-column.py \
        -- --out <dir> --root <repo> --run-sha <sha> --studio-sha <sha>

  Passing means: exit 0, status=RAN in <dir>/lighting-column-verdict.txt line
  1, objectsBuilt=10/10-planned, manifoldParts=10/10 (this should not change
  between the pure check and the built scene; if it does, that is itself a
  finding), previewsWrote=4/4 (hero_full and head_detail, each under
  overcast_day and wet_night), and a nonzero lighting-column.blend. Then,
  because looking is not measuring but is still required (CLAUDE.md rule 4):
  open every still and the .blend, and compare the rendered column against
  the Hook sheet's foreground column at the same crop this task used
  (production/art/atlas-01/concepts/hook.png, street panel) for silhouette,
  darkness of the steel, the neck's long shallow read against a tight hook,
  the canopy's shallow flat profile against a bowl or box, and the sodium
  lens colour. A taste question, not a mechanical one: it goes to Jafar as a
  card through the Producer if it needs a decision, per this brief's
  standing instruction, not decided here.

  A SEPARATE, SMALLER ACCEPTANCE: the Harbour Office wall bracket lamp named
  above gets its own spec entry and its own commission once the street needs
  it; this item does not ask for it, only names the gap so it is not lost.
status: READY, blocked on Blender being available on the machine that runs
  it, which this container does not have. Not chased further in this
  session under CLAUDE.md rule 11: the finding (a bug the pure-Python check
  caught that the description alone would have missed) is filed above and
  the standing order resumes. The batch row for this pilot is
  production/throughput.md, BATCH b006-lighting-column-01, opened this
  session with a BEFORE reading; VERIFY and the AFTER reading are what this
  item is waiting on.

---

DIRECTOR'S NOTE, 2026-09-21, ADDED AT REVIEW AND NOT BY THE BUILDER.

THE FLAT-COLOUR CHOICE STANDS, and its reason is sound: wiring a UV-mapped
texture into unrun bpy code is more failure-prone than a flat colour, and this
recipe's bpy layer was already carrying new unproven code in the HDRI world and
the light placement. That argument does not depend on what the pack holds.

THE ENUMERATION UNDER IT WAS WRONG BY ONE, AND THE ONE IT DROPPED IS THE
RELEVANT ONE. The report listed 17 distinct base surfaces in
`ledger/Assets/StreamingAssets/CityPack/textures` and omitted `metal`. Checked
at review: there are 18, `metal.jpg` is present, and this recipe's own spec
source, `production/specs/vignette-scene.json` under `lighting.column`, names
`surface: "metal"`. So the spec the recipe reads at run time asks for a surface
the pack already holds, and the decision to ship flat colour was taken without
that in view.

WHAT THAT CHANGES IS THE FOLLOW-UP, NOT THE DECISION. Not "find out whether a
textured metal read matters" but "the surface exists and the spec already names
it, so wire it ONCE A REAL BLENDER RUN HAS PROVED THE BPY LAYER WORKS AT ALL".
Ordered after the first real run and never before it, for precisely the
builder's own stated reason.

THE COUNT MATTERS BEYOND THIS ASSET. `--measure-pack` prints 18 and the
citypack selftest reads `filesExamined=18/18`, so two live instruments already
agree on 18. A hand enumeration that disagrees with two instruments is this
project's signature fault, and it is why the brief said verify rather than
trust. The builder applied that rule correctly to the piece count, where it
caught a real error of the resident's, and did not apply it to its own list.

