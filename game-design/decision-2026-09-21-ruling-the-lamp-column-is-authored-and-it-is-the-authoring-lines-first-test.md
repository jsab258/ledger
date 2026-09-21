# Jafar's ruling, 2026-09-21 late evening: author the lamp column, and make it the authoring line's first test

STATUS: LOG, 2026-09-21. NOT CURRENT once the queue item, the batch row and the
authored asset it names have landed: from then the queue, the throughput ledger
and the decision register are the reading copies and this is the record of what
he said and when. Written by the resident as dictated text, which is the one
category of authoring the resident may hand-apply, and kept VERBATIM below
because a paraphrase of a ruling is not a ruling.

## His words, verbatim

"Budget: total 17, Fable 19, taken now.

A. Author it, and treat it as the first test of the authoring line before the
terrace fronts: if a lamp column comes out right in Blender, the facades are
the same method at scale. Period matters: a 1990 working port mostly has
concrete or steel swan-neck columns with sodium lanterns, not Victorian
heritage lamps. There is a free Victorian Street Lamp by Rosbergen Designs on
Fab if you want to compare, but do not wait on it."

## What it decides

1. THE CARD IS ANSWERED: option A of the lamp column card, author it. That card
   offered A author, B keep the blockout, C fetch, with the studio recommending
   A and defaulting to B. He took the recommendation. The card leaves WAITING
   for the register in the same commit as this record.

2. IT IS PROMOTED FROM AN ASSET TO A PILOT, and this is the part that is his
   and not the studio's. The card asked only whether one column should be
   authored. He answered that and then reframed it: "the first test of the
   authoring line before the terrace fronts: if a lamp column comes out right
   in Blender, the facades are the same method at scale." So the deliverable is
   TWO THINGS, an asset and a verdict on a method, and the second is the
   reason it goes first.

3. SO IT IS A BATCH, and that is not a studio embellishment but the direct
   consequence of 2. Queue 403 landed the batch unit hours ago and the week's
   first unknown in his own order is "what a unit of content costs". A pilot
   whose purpose is to price a method must be priced. It gets its own batch row
   in `production/throughput.md` under the unit 403 defined, with a BEFORE
   reading taken before authoring starts and an AFTER reading when it resolves,
   and a rejected attempt shows in `attemptsRejected` rather than as silence.
   IT IS THE SMALLER, FASTER BATCH AHEAD OF THE FACADE, which is why putting it
   first costs the week nothing and tells us the method's price early.

4. THE PERIOD IS RULED AND IT OVERRULES THE OBVIOUS REFERENCE. "A 1990 working
   port mostly has concrete or steel swan-neck columns with sodium lanterns,
   not Victorian heritage lamps." That is a canon-shaped constraint arriving
   with the ruling, and it is the OPPOSITE of what an image search for a
   British street lamp returns. The authored column is a plain concrete or
   steel swan-neck carrying a sodium lantern. No fluting, no ladder bar, no
   scroll, no ornament.

5. THE FAB ASSET IS A REFERENCE, NOT A SOURCE, and he said so in the same
   breath as ruling its style out: "if you want to compare, but do not wait on
   it". It is not on the critical path and nothing may block on it. IF ANY PART
   OF IT WERE EVER TO SHIP that is a separate question with the same open
   answer as City Sample: `ledger-v2/research/license-allowlist.md` admits "Fab
   purchases under the Fab Standard License" and a free claim is not a
   purchase, so the letter of the allowlist does not yet cover either. Nothing
   in this ruling needs that settled, because what ships here is authored.

## What the studio already knows, measured rather than remembered

- THE BLOCKOUT IT REPLACES IS ALREADY DIMENSIONALLY RIGHT, which is why this is
  a finish job and not a design job. `production/specs/vignette-pieces.json`
  carries 21 `E1_lighting_column` references: `lantern0..3` at x = 8, 18, 28,
  38 m and four columns of five pieces, `column{0..3}_base`, `_shaft` (4.7 m),
  `_neck0/1/2` (three pitched cylinders on a quarter circle), built by
  `ledger/Assets/Scripts/Core/StreetVignette.cs:1176 Columns()`. The shaft is
  0.114 m round, the real diameter of a British lighting column.
- THE KIT LAMPS STAY OUT OF THIS FRAME and the measurement is why: the three
  city-kit columns are 0.37 m SQUARE in section, 3.2 times too fat and the
  wrong shape. They remain correct for the Unity town, where 71316fa1 wired all
  six forms on 2026-08-25 and the landed verdict counts
  `kitBy=[lamp:354/354/0/0refused`.
- THE PRECEDENT FOR THE CONVERSION EXISTS AND IS NAMED: `production/art/fascia-01`
  (the fascia cornice and console, BOM C15) is the only prior instance on this
  street of a procedural box becoming an authored mesh without moving anything,
  and the terrace-front spec already uses it as its template. The recipe
  precedent is `tools/art-recipes/mickeys-blockout.py`, which builds geometry
  through `bpy.data` rather than `bpy.ops` and ships `--plan` and a selftest so
  the arithmetic and every printed string are covered without Blender.
- BLENDER IS NOT INSTALLED IN THIS CONTAINER, so every line touching `bpy`
  ships UNRUN and the first run on his PC is its accepting case, exactly as
  Mickey's did. That is a fact about the route, not a reason to avoid it, and
  it is part of what this pilot is measuring.

## Where each piece went, a reading at each commit and not a promise

- This record and the budget row 2026-09-21c: landed with the commit carrying them.
- The lamp card moved from WAITING to the register: landed with the same commit.
- The queue item for the authored column: not yet.
- Its batch row in `production/throughput.md` with a BEFORE reading: not yet.
- The authored column itself: not yet.
