# The research, and what governs each thing's look

WHAT THIS ANSWERS. Before authoring anything, two questions: which research
governs it, and which concept sheet governs it. This page routes both.

## The per-asset index

`game-design/research/GOVERNS.md` is the one to open. It covers seventeen
street-level asset families and, for each, names the concept sheet and the
panel within it, the research file and the line, and quotes what that research
actually says rather than paraphrasing it. It also states, in its own section,
what it does NOT cover, so absence reads as absence rather than as silence.

THE RULE IT EXISTS FOR, Jafar 2026-09-21: "Every authored asset's brief names
the concept sheet and the research that govern it, and follows them." And the
half that decides arguments: where a sheet or the research disagrees with
anything said in passing, INCLUDING A DIRECT REPLY, they win.

A CONCEPT SHEET GOVERNS LOOK, NOT GEOMETRY. Where a dimensioned drawing or a
spec exists, that is the geometry; the sheet is the reference for material,
wear, tone and silhouette character. This distinction is not pedantry: four
attempts at the lighting column were spent tuning to a proportion traced off a
sheet whose lamp is twenty-five pixels wide, and three traces of the same crop
gave three different answers.

## The approved concept sheets

They live on the `art/atlas-01` branch under
`production/art/atlas-01/concepts/`, not on `main`. Read one with

    git show origin/art/atlas-01:production/art/atlas-01/concepts/<name>.png

`hook.png` is the visual bar for phase A and is the sheet most briefs cite.

## The research itself

Forty-seven subdirectories here, one per question, each holding the summary,
the rechecks and the brief that was written from it. They were consolidated in
September 2026 so that the studio could read what governs an asset before
authoring it rather than after arguing about it. `game-design/research/` holds
the seven files GOVERNS.md reads; `ledger-v2/research/` holds the feasibility
and comparison work, and the LICENCE ALLOWLIST, which is law.

## What is not here

Canon. The world's facts are `canon.md` at the root and it outranks every page
in this directory. Research says what a 1990 British port town looked like;
canon says what is true in Meridian.
