# D53. Grime is the strategy: a surface carries wear above a floor, and the floor is a number nobody has printed yet

CANON: none

`canon.md`, Tone, lines 55 to 56 read 2026-09-21: "Visual target: photoreal,
wet, overcast, grimy Britain. Weather and grime are the strategy, not
stylization." UNCHANGED by this record, which is why the directive above is
`none`. This record turns that line into a rule with a direction now and a
measured floor when the series exists.

Ruled by Jafar, 2026-09-21, first message, under "On the look", kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"Grime is the strategy, per canon, against the light period look that the
shader's art-direction line quotes. The two disagree and it has never been
recorded. Record it as a rule with a number in it, a stated floor for how much
wear a surface carries, so it is not re-litigated on every render. The facade
is the first thing authored under it."**

## The rule, as recorded

1. DIRECTION: wear over clean. Canon's line above and pillar 5
   (`vision-pillars-v2.md` line 19: "Photoreal grim Britain. Wet, overcast,
   sodium-lit, worn ... Density and wear carry frames") are the target. Any
   line in a shader, a material script, a prompt or a spec that describes a
   lighter or cleaner look than that is subordinate to canon, which outranks
   every document, and is corrected on sight, citing this record.
2. THE QUANTITY the floor is expressed in: WEAR COVERAGE, the fraction of a
   surface's visible area that carries wear authored as a separable layer, the
   wear decals of D28 step 7 (queue 055) and any wear mask the material
   carries. Printed per surface as one token with no spaces,
   `wearCoverage=<fraction>`, and per batch as a series: `wearCoverageN=<count>`
   and `wearCoverageMin=<fraction>/<surface>`, the surface at the minimum named
   because a median cannot see the one clean wall. A surface whose wear is
   baked into its albedo and cannot be separated prints `nothing measured` for
   this key and is judged by eye under D41; it does not print zero.
3. WHO PRINTS: the material station. `tools/ue/make_base_material.py` already
   prints per-surface wetness tokens as key=value (its wetness token check,
   near line 1658 when read 2026-09-21); it gains one key. A tool that measures
   the game: a test, no review (D45), with the instrument rules
   (`.claude/rules/instruments.md`: the statistic named, every zero with its
   denominator, every cap announced).
4. WHO SETS THE NUMBER, AND FROM WHAT: the director, as amendment A1 to this
   record, after the series is printed over the surfaces Jafar has accepted
   beside the Hook sheet (D23, D41: the sheet is the judge). The candidate is
   the minimum wear coverage among accepted surfaces; the amendment quotes the
   series it was read from. Rule 2 and the instruments file forbid any other
   order: printer first, real runs, then the bound.
5. UNTIL A1: the facade (queue 389 in the resident's log, "the first authored
   building facade, as the week's measured batch") is authored under the
   direction, with its wear as a separable layer so that its coverage can be
   printed, and prints `wearCoverage` with its batch. It is the first point in
   the series, not a surface judged against a floor that does not exist.

Point 5's consequence, that the facade's wear is authored separably rather
than only in the albedo, is drawn by the director from "a rule with a number
in it": a number needs a countable layer. It is not his sentence, and it is
named as the director's in the report so he can strike it.

## The gap, named rather than guessed

THE FLOOR HAS NO NUMBER. Nothing on main prints a wear quantity: a grep over
`tools/` (non-markdown) on 2026-09-21 for "dirt", "grime", "wearMask",
"wear_mask" and "weathering" hit the v1 2D vignette generator
(`tools/props/make_vignette_2d.py`, fbm noise scalars), the docstring of
`tools/props/fetch_visual.py`, and the imagegen prompt suffixes
(`tools/imagegen/prompts.json` lines 257 to 265: "soot and grime, uniform
weathering across the whole frame"), and nothing in the material script or the
UE probe. The prompt suffixes are the rule in words, which is consistent and is
not a number. What closes the gap: the key printed on one batch, the facade's,
read, then A1.

## The shader line he names, looked for and not found on main

"The shader's art-direction line" that quotes a light period look was not
found: grep for "art direction" and "art-direction" over `ue-probe/` (0 hits)
and `tools/ue/` (0); "period" over `ue-probe/` (0) and `tools/ue/` (1, a
checker period, unrelated); "light ... period" across all code (only the
prompt suffixes, which say "period-correct signwriting" and "worn period
fittings" and agree with canon). The nearest lines on main are
`ledger/Assets/Scripts/Game/Weather.cs:5` ("ART DIRECTION: STYLISED NOIR
(approved 2026-07-28 ...)", the Unity build D16 retired and the ceiling D14
retired) and `ledger/Assets/Resources/LedgerSky.shader:7-8` ("The one place
the art direction leans hardest (a low wet British sky over a port town)"),
which agrees with canon. The line he means is either cited in the research
delivery on its branch or sits in a binary material this grep cannot read.
UNRESOLVED and reported: the resident finds it when the consolidation lands
and marks it under D43 citing this record.

## What this does not decide

The number. The technique (decal, mask or both). The facade's design, which
is queue 389's and the art line's. Whether a second quantity (roughness or
albedo variance) is needed beside coverage: that is A1's to say from the
series, not this record's to guess.
