# Ron's plain clothes, modelled to a pattern: the report

8 October 2026, 07:12 to 08:44, branch lab. Details: NOTES.md; the review: REVIEW.md. Published as a private page: https://claude.ai/artifact/5rTRS2pewmoWbjXgcPLiPo

**In short.** The checks worked; the clothes did not. The jumper and trousers were modelled on Ron to a target written by a fresh helper, with no cloth simulation.
- **Body:** none of Ron's body comes through either garment.
- **Trousers:** match the target's outline within 1 cm in every view.
- **Jumper:** matches within 11.3 mm. It misses 1 cm by 1.3 mm at the neck rib.
- **The fresh reviewer failed it:** "the sleeves look like skin, and the trousers look like tracksuit bottoms". Most of what it names comes from the target itself, which an outline check cannot see.

## Numbers (final version, v27)

| Check | Result |
|---|---|
| Body points through the jumper / trousers | 0 of 10,318 / 0 of 7,069 |
| Trousers' outline, front / side / back | within 8.0 / 8.9 / 8.0 mm: **pass** |
| Jumper's outline, front / side / back | within 11.3 mm in each, average 1 to 2 mm: **fails by 1.3 mm** |
| Seams within 1 cm of the target's | 3 of 22; most 5 to 8 mm off on average, worse at their ends: **fail** |
| Fresh review against two photographs (Finland 1988; about 1989) | **FAIL** |

The target was tested against Ron's body and against its own pattern. That found seven faults, all fixed by its writer in 22 minutes:
- sleeves inside his forearm;
- the feet counted as trousers;
- a 2 to 4 cm step at the sleeve top;
- an elbow eased from a guessed arm size;
- a neck drawn with straight lines;
- and two smaller ones.

## The reviewer's faults, and where each comes from

1. **Sleeves skin-tight, muscles showing** (the target): the pattern leaves about 3 mm of ease on Ron's thick forearm.
2. **A ridge round the trousers below the jumper** (both): the target's own step at the seat line, larger in the model.
3. **Straight wide legs, no crease or break** (the target): a straight leg and a level hem 4 cm off the floor are its choices.
4. **Dark toe marks at the hems** (the model): the hem cuts through the bare feet.
5. **Spikes in the neck rib** (the model).
6. **Belly ridges** (both).
7. **Hem rib does not draw in** (the target): it is worn over trousers wider than the rib.
8. **Plain cuffs** (the model).
9. **Flat seat** (the target).

## Time

- Lab: 1 hour 31 minutes.
- Target helper: 46 minutes.
- Photo helper: 40 minutes. No free period photograph of a man in a plain crew-neck was found; the reviewer used the two nearest.
- Reviewer: 4 minutes.
- 28 model runs of 30 seconds each.

## Should this route go to the builder?

**Not as a way to make clothes.** Clothes built from outline rules pass the outline and fail the eye. The meshes are also not game garments: they are dense, unmapped and not skinned to the skeleton.

**Two parts are worth taking:**
1. **The body check.** Count Ron's points that show through a garment, and gate the builder's own clothes on zero before any review (Epic's free Sweater, the MakeHuman bases). It is exact and takes seconds.
2. **Test a target before building to it.** Check every covered point against the target's own outline, and every rule against its own pattern. That found seven faults in a written target in 22 minutes.

For knitwear, the look (ease, folds, a rib drawing in, a trouser's break) has to come from real garments or photographs; a rule cannot supply it.
