# Is the scene judge proven? 23 November 2026

**Yes, for one job, by the mark written down first.** Shown two disguised scenes from shipped games, one praised by players and critics and one called forgettable, it picks the praised one almost every time, in either order.

**Numbers** (40 pairs a model, neither scene recognised, both orders): Opus 38 right, 0 wrong, 2 undecided; Sonnet 36 right, 1 wrong, 3 undecided (mark: 85% of decided pairs). First-shown scene chosen 51% and 54%; longer scene 59%, inside the 40 to 60% limit by one point. The two models agree on 90% of pairs. A judge asked only which scene has more at stake got 63%, so the brief measures more than danger. Recognised scenes scored no higher, so memory is not doing the work.

**It can tell** a scene with people, a want, a cost and a turn from an errand or set-up. It will catch a key scene that has slid into filler.

**It cannot tell yet** great from merely good: the shelf has no middle tier. One model family only. The most famous scenes could not be disguised (22 of 40 recognised).

**On LEDGER's key scenes** (tools/ledger_pairs.py):
1. A fresh helper rewrites the scene to FORMAT.md, same length.
2. Build: paired with 4 praised and 4 forgettable clean shelf scenes, plus 4 control pairs, both orders.
3. Four fresh Opus and four fresh Sonnet judges, BRIEF-v1 word for word.
4. Score. A judge that fails a control is not counted. Floor: beats all 4 forgettable, both models. Against praised scenes: wins and ties. A screen, never a verdict of greatness.

**Next:** add good-but-unpraised heavy scenes and test great against good.

Details: RESULTS.md, PLAN.md, set/, runs/, LOG.md.
