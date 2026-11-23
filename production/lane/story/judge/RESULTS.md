# Judge proof: results

Run 23 November 2026, 22:50 to 23:20 Swiss time, after PLAN.md was pushed (356ef694). Brief: BRIEF-v1.md, unchanged throughout. Judges: fresh claude-opus-5-5 and fresh Sonnet subagents, 20 judgements each, the two orders of a pair never to the same judge; 32 judges in all (16 a model). No Fable.

## Clean pairs (both scenes passed the recognition screen): the pass mark

| | Half A Opus | Half A Sonnet | Half B Opus | Half B Sonnet | Pooled Opus | Pooled Sonnet |
|---|---|---|---|---|---|---|
| Pairs | 20 | 20 | 20 | 20 | 40 | 40 |
| Admired chosen in both orders | 19 | 19 | 19 | 17 | 38 | 36 |
| Forgettable chosen in both orders | 0 | 1 | 0 | 0 | 0 | 1 |
| Orders disagree (tie) | 1 | 0 | 1 | 3 | 2 | 3 |
| Accuracy on decided pairs | 100% | 95% | 100% | 100% | 100% | 97% |
| Decided share | 95% | 100% | 95% | 85% | 95% | 93% |

Over all 160 judgements per model (clean and recognised pairs):
- Position: scene shown first chosen 51% (Opus), 54% (Sonnet). Half A 48% and 53%; half B 54% and 56%.
- Length: longer scene chosen 59% for both (104 judgements a model where the two differ by 5 words or more). Half B Opus alone was 62%. Admired scenes average 365 words, forgettable 363, so this is not label in disguise. Controlled for label: accuracy 97% (Opus) and 95% (Sonnet) when the admired scene was longer, 89% and 87% when the forgettable one was longer. A small length pull, or noise (46 to 58 judgements each side).
- Agreement, Opus and Sonnet same verdict: clean pairs 90% in each half; all pairs 90% (A) and 95% (B). Cohen's kappa is low on clean pairs (near 0 in half A) only because nearly every verdict is "admired" for both: with almost no spread, kappa says little. Kappa on all pairs: 0.39 (A), 0.78 (B).

Against the pass mark (pooled, the deciding result since half A passed and half B confirmed it): accuracy on decided pairs 100% and 97% (mark 85%); decided 95% and 93% (mark 67%); position 51% and 54% (mark 40 to 60%); length 59% and 59% (mark 40 to 60%, inside by one point); agreement 90% (mark 70%). PASS. The brief was not mended; no second brief was needed.

## Recognised pairs (at least one scene the screen named): memory measured, not gating

| | Half A Opus | Half A Sonnet | Half B Opus | Half B Sonnet |
|---|---|---|---|---|
| Accuracy on decided pairs | 95% | 94% | 94% | 94% |
| Decided share | 95% | 90% | 90% | 90% |

No higher than on clean pairs. Memory of famous scenes did not lift the score; the judge did as well on scenes nobody recognised.

## Control: a stakes-only judge

Fresh Sonnet, half A, asked only which scene has more at stake (BASELINE-BRIEF.md). Clean pairs: right on 63% of decided pairs (12 admired, 7 forgettable, 1 tie); all pairs 69%; longer scene chosen 75%. So danger and loss alone explain a little of the judge's score, not most of it: the full brief adds about 35 points on clean pairs.

## What the test does not show

1. Great from good. The forgettable side is mostly errands, set-ups and filler missions; the admired side mostly climaxes and character turns. The judge can tell those apart. Whether it can tell a great heavy scene from a merely competent heavy scene was not tested: there is no middle tier on the shelf.
2. Small samples: 40 clean pairs a model, from 18 clean scenes (8 admired, 10 forgettable). Scenes repeat across pairs, so the pairs are not independent. With 38 of 38, the true rate is very likely above 90%, but on a narrow set.
3. Labels: several forgettable labels rest on one list or one reviewer (set/SOURCES.md). The judge agreeing with them is partly agreement with thin labels.
4. Disguise was done by Claude models and judged by Claude models; one family throughout. APPROACH wants a non-Claude judge; none was available to this run.
5. The famous admired scenes could not be disguised from Opus without rewriting their stories (22 of 40 still recognised after three passes). The clean admired scenes are the less famous ones: three KCD2 quests, a Sleeping Dogs hospital rescue, two Watch Dogs: Legion story missions, a GTA IV revenge scene and an L.A. Noire case.
6. Judges saw 20 pairs each; a scene could appear in several of one judge's pairs.
