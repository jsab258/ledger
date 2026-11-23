# Scene judge: passed its mark, as a screen. 23 November 2026

**Did it pass?** Yes, by the mark written down first, but only as a screen, not as proof of taste. Given a disguised praised scene and a forgettable one from shipped games, it picks the praised one about 9 times in 10, in either order.

**Numbers** (40 pairs a model, neither scene recognised, both orders, after hints were scrubbed from the texts): Opus 36 right, 2 wrong, 2 split (95% of decided pairs); Sonnet 34 right, 3 wrong, 3 split (92%). Mark: 85%. First-shown scene chosen 53% and 54%. Longer scene chosen 60% and 59%, Opus exactly on the limit: length pulls, so scenes must be the same length. The models agree on 90%. A stakes-only judge (Sonnet, earlier unscrubbed texts) got 63%. All its misses fall on three of the eight praised scenes.

**What that means:** praised turns and losses are told from errands and set-ups. Why it chose was not checked.

**It cannot tell yet** great from merely good: the shelf has no middle tier. One model family only. 22 of the 40 scenes stayed recognisable however disguised, so only 18 count. Not yet tried on a LEDGER scene.

**On LEDGER's key scenes** (tools/ledger_pairs.py):
1. A fresh helper rewrites the scene to FORMAT.md, shelf length.
2. Build: paired with 4 praised and 4 forgettable clean shelf scenes, plus 4 control pairs, both orders.
3. Four fresh Opus and four fresh Sonnet judges, BRIEF-v1 word for word.
4. Score. A model that gets any control wrong both ways is not counted; rebuild and rerun. Floor: beats all 4 forgettable, both models. Against praised scenes: wins, splits, losses.

**Next:** add good-but-unpraised heavy scenes and test great against good.

Details: RESULTS.md, PLAN.md, set/, runs/.
