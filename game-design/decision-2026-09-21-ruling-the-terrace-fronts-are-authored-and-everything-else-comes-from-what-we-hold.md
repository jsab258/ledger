# Jafar's ruling, 2026-09-21 evening: City Sample is claimed, the terrace fronts are authored, everything else comes from what we hold

STATUS: LOG, 2026-09-21. NOT CURRENT once the queue items and file edits it
names have landed: from then the queue and the decision register are the
reading copies and this is the record of what he said and when. Written by the
resident as dictated text, which is the one category of authoring the resident
may hand-apply, and kept VERBATIM below because a paraphrase of a ruling is not
a ruling.

## His words, verbatim

"Claimed: City Sample.. No free British terrace kit exists on Fab. The good
ones cost eighteen to a hundred and fifty francs, and I am not buying. So the
terrace fronts are authored: in Blender from the atlas plans, under the grime
rule, the way Mickey's blockout was, dressed in free scanned materials.
Everything else comes from the free libraries and the kits we already hold,
including the British lamps. Go."

## What it decides, and what it amends

IT AMENDS THE KIT-FIRST RULING RATHER THAN REPLACING IT.
`decision-2026-09-21-ruling-kit-first-author-second.md` set the method: a
shopping list marking each item found, close enough or MISSING; assemble; make
it Meridian; and "assembly lines fill only the gaps marked missing". This
ruling is that method reaching its fourth step for one item. He did the
shopping himself, found no free British terrace kit on Fab, priced the paid
ones at eighteen to a hundred and fifty francs, and declined. So the terrace
front is a gap marked MISSING, confirmed by the only person who can confirm it,
and it goes to the authoring line. Nothing else changes: kit first still holds
for everything that is not a terrace front.

FOUR THINGS ARE SETTLED BY IT.

1. CITY SAMPLE IS CLAIMED. The manual step the 16:3xZ card asked him for is
   done. What it does NOT settle is the licence: the allowlist is law, and
   `ledger-v2/research/license-allowlist.md` line 2 admits "Fab purchases under
   the Fab Standard License". City Sample is a free claim rather than a
   purchase, so the letter of that line does not cover it even though the
   spirit plainly does. It is recorded as an OPEN LICENCE QUESTION below rather
   than assumed either way, because assuming is the one thing the allowlist
   forbids.

2. THE TERRACE FRONTS ARE AUTHORED, and he named the method precisely: in
   Blender, from the atlas plans, under the grime rule, the way Mickey's
   blockout was, dressed in free scanned materials. Every one of those five
   clauses points at something that already exists here, which is why this is
   an instruction and not a research task. The precedent is
   `tools/art-recipes/mickeys-blockout.py`: authored numbers live in
   `production/art/<commission>/data/*.json` on the art branch, the recipe
   builds geometry through `bpy.data` rather than `bpy.ops`, and `run-recipe.py`
   carries `--plan`, `--dry-run` and a selftest so the arithmetic and every
   printed string are covered without Blender. Blender is not installed in this
   container, so every bpy line ships UNRUN and the first run on his PC is its
   accepting case, exactly as Mickey's did.

3. THE GRIME RULE IS D53 AND ITS FLOOR IS STILL A GAP, WHICH IS NOT A BLOCKER.
   D53 point 5, read rather than remembered: "UNTIL A1: the facade is authored
   under the direction, with its wear as a separable layer so that its coverage
   can be printed, and prints `wearCoverage` with its batch. It is the first
   point in the series, not a surface judged against a floor that does not
   exist." So the terrace front is authored now, its wear separable, and it
   PRINTS the number that A1 will later be set from. Authoring it is how the
   floor comes to exist.

4. THE BRITISH LAMPS ARE ALREADY WIRED, AND THE RESIDENT GOT THIS WRONG FIRST.
   This section said the kit survey's dispatch had never been executed and that
   `MakeLamp` builds its own lamp geometry. BOTH ARE FALSE and the false text
   is left named rather than deleted. The resident read a stale document header
   instead of the code, which is CLAUDE.md rule 1's exact failure: the survey
   `game-design/agent-reports/kit-survey.md` still said "nothing in this report
   is wired" a month after its own dispatch landed, and that sentence was taken
   as evidence. Checked by command, all four:

   - `git log -S "city_kit_roads_light_curved_cross" -- WorldBuilder.cs`
     returns ONE commit, `71316fa1`, 2026-08-25, "The street gets furniture,
     and the gate that said it was reviewed was lying". The same day as the
     survey. All six kit lamp forms were wired that day.
   - `WorldBuilder.cs:3961 MakeLamp` calls
     `AssetLibrary.TryInstantiateProp(key, ...)` on the kit mesh, with
     `CastIronLamp(LampDistrict(x,z))` resolving six keys off a district flag.
     The canon mix he wants, cast swan necks on old streets and square sodium
     on newer roads, is the district lookup and it is live. The procedural
     boxes are the COUNTED FAIL-CLOSED FALLBACK, reached only on a miss.
   - The number exists and is landed: `game-design/sim-shots/verdict.txt`
     prints `kitBy=[lamp:354/354/0/0refused` with
     `kitByVariant=[lamp/curved:186/0, lamp/curved_double:4/0,
     lamp/curved_cross:3/0, lamp/square:149/0, lamp/square_double:8/0,
     lamp/square_cross:4/0` and heights 4.44..4.99..4.99, the survey's own
     targets, so the scale landed too.
   - The Unreal vignette is NOT missing its posts either. `vignette-pieces.json`
     carries 21 `E1_lighting_column` references: `lantern0..3` and four columns
     of five, `column{0..3}_base/_shaft/_neck0/_neck1/_neck2`, built by
     `StreetVignette.cs:1176 Columns()`. The resident quoted
     `VignetteShot.cpp`'s "a rectangle with an invisible lamp under it" as
     evidence of a missing post; read in full it is queue 333's PAST-TENSE note
     about the lantern HEAD's glass, since fixed by `kLampEmissiveUnitless`. It
     never described a missing column.

   SO HIS INSTRUCTION IS ALREADY SATISFIED IN UNITY, and the survey header has
   been corrected in place so the stale sentence cannot re-issue the dispatch a
   third time.

5. THE REAL LAMP GAP IS A DIFFERENT ONE AND IT IS HIS TO DECIDE. Measured from
   the kit FBX vertex data: all three kit lamp columns are 0.37 m SQUARE in
   section. The vignette's `E1_lighting_column` shaft is 0.114 m ROUND, which
   is the real diameter of a British lighting column. So dropping a kit lamp
   into the photoreal slice would trade a dimensionally correct round column
   for a four-sided one 3.2 times too fat, in the one frame whose whole purpose
   is to survive comparison with GTA6 and KCD2. The kit forms are right for the
   kit-built Unity town and wrong for the vignette. What the vignette has is a
   correct-dimension BLOCKOUT of five primitives; a photoreal 5 m round tapered
   column is held by NOTHING in the tree and by no kit in it. That is a
   fetch-or-author decision on the allowlist, in the same shape as the terrace
   fronts he just ruled on, and it goes to him as a card rather than being
   decided by the studio doing it.

## Measured tonight, so the work starts from facts and not from notes

- `grep -rn "lamp_post_01" ledger/Assets/Scripts/` returns NOTHING. The held
  lamp is CC0-1.0 from The Base Mesh, carries LOD0/1/2, and is imported to
  Unreal as `ue-probe/Content/Ledger/Props/SM_lamp_post_01.uasset`. A grep of
  `ue-probe/Source/` for it also returns nothing. So it is fetched, LOD'd,
  imported and PLACED BY NOTHING, in either layer: CLAUDE.md rule 6, built is
  not running, with the whole pipeline built and no call site.
- `MakeLamp` in `ledger/Assets/Scripts/Game/WorldBuilder.cs` builds lamp
  geometry itself and is called at eight sites (3043, 3044, 3066, and six hand
  placed at 3170 to 3175). It carries a `LampForm` enum already, which is the
  hook the three kit forms drop into.
- THE EARLIER NOTE THAT SAID "swan-neck lamps already held in a CC0 kit" WAS
  RIGHT ABOUT THE CONCLUSION AND VAGUE ABOUT THE EVIDENCE, and it is replaced
  here by the survey rows and the two greps above. Checked, not remembered.

## Open licence question, and it gates nothing tonight

City Sample's terms must be read and the allowlist amended BEFORE anything out
of it ships. Nothing tonight depends on it: the setts are ambientCG CC0, the
lamps are kits already held and already on the allowlist, and the terrace
fronts are authored here. The question is filed rather than answered because
ambientcg and Fab are both unreachable from this container and a licence is
not a thing to assume. It also brings forward the `.uasset` blind spot at
`tools/attribution-check.py:381`, whose own comment says the entry comes out
the day a `.uasset` appears that no script generated: City Sample IS that day.

## Where each piece went, a reading at each commit and not a promise

Filled in as things land. A line reading "not yet" is the truth at the newest
commit touching this file, not a plan.

- This record: landed with the commit that carries it.
- The lamps, the kit survey's unexecuted dispatch: not yet.
- The terrace front recipe and its authored data: not yet.
- Queue 403, the batch unit that queue 389 names as its blocker: not yet.
- The City Sample licence question and the `.uasset` blind spot: not yet.
