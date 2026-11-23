# Judge proof: results

23 November 2026, Swiss time. PLAN.md (the pass mark) was pushed at 22:48 (356ef694), before any judge ran. Brief: BRIEF-v1.md, unchanged throughout. Judges: fresh claude-opus-5-5 and fresh Sonnet subagents, 20 judgements each, the two orders of a pair never to the same judge. No Fable.

## The result: clean re-run on scrubbed texts (22:58)

Why a re-run: the fresh reviewer found wording in some rewrites that hinted at the label ("the mood is routine", "no choice changes the result", "the notebooks add little", mostly in forgettable scenes). One fresh Sonnet, given all 40 texts without labels, removed mood verdicts, commentary on a scene's importance and judgement adjectives by one rule for all (set/scenes.json keeps each scene's changes and pre-scrub text; 36 changes in admired scenes, 40 in forgettable). The scrubbed set was pushed (41d190bc) and all 40 clean pairs (both halves) were run again, both orders, by 8 fresh judges (4 a model). Same brief, same pass mark.

| Clean pairs, 40 a model | Opus | Sonnet | Mark |
|---|---|---|---|
| Admired chosen in both orders | 36 | 34 | |
| Forgettable chosen in both orders | 2 | 3 | |
| Orders disagree (tie) | 2 | 3 | |
| Accuracy on decided pairs | 94.7% | 91.9% | at least 85% |
| Decided share | 95% | 92.5% | at least 67% |
| Scene shown first chosen (80 judgements) | 52.5% | 53.8% | 40 to 60% |
| Longer scene chosen (70 judgements differing by 5+ words) | 60.0% | 58.6% | 40 to 60% |
| Same verdict, Opus and Sonnet | 90% (kappa 0.56) | | at least 70% |

PASS by the mark as written, with Opus's length figure exactly on the limit. The brief was not mended.

Length, looked at closer: admired and forgettable clean scenes average 349 and 348 words. When the admired scene was the longer one, the judges chose it 38 of 38 (Opus) and 36 of 38 (Sonnet); when the forgettable one was longer, 28 of 32 and 27 of 32. So length pulls about 10 to 15 points. FORMAT.md's equal length matters, and LEDGER scenes must be held to the shelf's length.

Where it went wrong: every wrong or split verdict, for both models, involves one of three of the eight admired scenes: S64 (an L.A. Noire case), S20 (a Sleeping Dogs hospital rescue whose admired label was inferred, not named by its source) and, for Sonnet only, S94 (a KCD2 quest). Whether the judges or the labels are wrong there cannot be told from this set.

## First runs on unscrubbed texts (22:49 to 22:50), kept for the record

Half A then half B, 16 judges (8 a model), 40 pairs a half, 20 clean and 20 with at least one recognised scene.

- Clean pairs pooled: Opus 38 right, 0 wrong, 2 ties; Sonnet 36 right, 1 wrong, 3 ties. On clean pairs, scene shown first 50% and 54%; longer scene 48% and 50% (46 judgements). (An earlier draft of this file gave position and length over all pairs, 51 to 54% and 59%; the mark is on clean pairs.)
- Pairs with a recognised scene: 94 to 95% of decided pairs, no higher than clean.
- The scrub cost a few points (100% to 94.7% for Opus, 97% to 92% for Sonnet), so the hints did some of the work, not most.

## Control: a stakes-only judge (22:50)

Fresh Sonnet (4 judges), half A, unscrubbed texts, asked only which scene has more at stake (BASELINE-BRIEF.md). Clean pairs: 63% of decided pairs (12 right, 7 wrong, 1 tie). Danger and loss alone explain little of the judge's score.

## What the test does not show

1. Great from good. The forgettable side is mostly errands, set-ups and filler; the admired side mostly turns and losses; the brief itself names errands as forgettable. The judge separates those kinds. A great heavy scene against a competent heavy scene was not tested: there is no middle tier on the shelf.
2. Small and linked samples: 40 clean pairs from 18 scenes (8 admired, 10 forgettable); scenes repeat across pairs and within a judge's 20.
3. Thin labels: several forgettable labels rest on one list or one reviewer, and three of the eight clean admired (S16, S20, S56) rest on one source each or on praise of a chapter, not the mission (set/SOURCES.md).
4. One family: disguise, scrub and judges are all Claude models. APPROACH wants a non-Claude judge; none was available here.
5. Memory: 22 of 40 scenes stayed recognised after three disguise passes, and Opus named the right game for most clean scenes at low confidence. Each game gives both labels, so the game alone does not tell the label, and recognised pairs scored no higher; but with scores near the ceiling, a memory effect cannot be ruled out.
6. Rewriters knew the labels when they wrote. The scrub removed explicit hints; what they chose to include could still lean.
