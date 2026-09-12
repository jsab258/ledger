# 265: the next district spec asks for children, and D18 forbids them

STATUS: READY
OPENED: 2026-09-12

## The fault, measured

`production/art/concept-copper-row-2026-09-10/copper-row-sheet-2026-09-10.json`
is the spec the 2026-09-11 wake record tells the studio to run next, by
appending its SENTINEL-ENTRY block to `production/d1-probe/RUN-IMAGEGEN` and
pushing. Two of its four items summon children in the POSITIVE half of the
prompt:

    copper_row_weighhouse_lane         HITS: lads, pram
    copper_row_weighhouse_lane_s2      HITS: lads, pram
    copper_row_weighhouse_end          clean
    copper_row_weighhouse_end_s2       clean
    itemsWithChildTerms=2/4
    negative prompt names any child term: False

The phrases are "two lads loitering by the gutter" and "shoppers in anoraks and
headscarves pulling tartan shopping trolleys, a woman with a pram".

D18 line 18 is absolute and is not a preference: "NO CHILDREN ANYWHERE: none
rendered, none in the crowd". A pram in a market crowd is an infant in the
crowd. "Lads" in this register reads as boys or youths and will render as
such often enough to matter over four items and two seeds each.

## Why the negative prompt does not save it

The spec's own note says so, and it is the better authority than any reasoning
here: "A negative vetoes but cannot summon: the Hook sheet's negative named
pleasure marina and yacht and the picture still came back a pleasant basin,
because a veto cannot put the trawlers in." The converse is what bites here. The
negative list carries no child term at all, and even if one were added, the note
also records that "'no people' in it asks the model to push away the phrase
rather than the people". So the fix is in the positive half or it is not a fix.

## Why this is worth an item rather than a quiet edit

It would have run. The wake record's instruction is a two-step append and push,
written before D18's cost was being felt, and nothing between that instruction
and the run reads the prompts for content-rule terms. The same rule had to be
enforced by hand on the Fairview sheets on 2026-09-10, and on 2026-09-12 a
session rebuilt the removed half back in without noticing. That is three
separate occasions where D18 depended on somebody happening to look.

## Done looks like

1. The two positive prompts carry no child-summoning noun. The market crowd is
   written from adults: traders, shoppers, a porter, a delivery driver. The
   pram and the lads go, and what replaces them is named rather than deleted,
   because a market morning with nobody in it is its own failure.
2. A check that reads every prompt about to run against the D18 term list and
   refuses the run, by item id, before any picture is made. It ships with both
   outcomes run, accepting case first: the two clean Copper Row items are the
   accepting fixture and the two dirty ones are the rejecting fixture, which
   means this item's own evidence is the test data.
3. The term list lives where D18 lives, not in the checker, so the rule and its
   enforcement cannot drift apart.

## What this does not decide

Whether Copper Row runs at all, and whether the Weighhouse is minted into canon
as a landmark. Both are director calls, and the second touches canon, which is
Jafar's to approve.
