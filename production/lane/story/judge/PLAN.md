# Judge proof: plan and pass mark, written before any judge ran

23 November 2026, about 22:50 Swiss time. Committed and pushed before the first judgement.

## The set

40 scenes from eight shipped games (RDR2, KCD2, GTA V, GTA IV, The Witcher 3, Sleeping Dogs, L.A. Noire, Watch Dogs: Legion), 20 admired and 20 forgettable, each game giving both kinds (2 and 3, or 3 and 2), so knowing the game alone does not tell the label. Rewritten to FORMAT.md (recipe versions 1, 2 and the third, clue-targeted pass). Sources and reasons per scene: set/SOURCES.md.

## The recognition screen and what it found

Three screens, each by fresh Opus and Sonnet asked to name game and mission. Version 1: Opus named the game of all 40. After version 2: 28 recognised by the rule (right game at confidence 50 or more, or the right mission). After the third pass: 22 recognised (12 admired, 10 forgettable), 18 clean (8 admired, 10 forgettable). Opus still named the right game for most scenes at low confidence, which is harmless here because each game gives both labels. The famous admired scenes stay recognisable from their plot alone; disguising further would change the story being judged. So the recognised scenes are not dropped from the run but are kept out of the pass mark: they are judged too, to measure how much memory adds.

## Halves and pairs

The scenes are split at random into halves A and B, each with 10 admired (4 clean) and 10 forgettable (5 clean). In each half: all 20 clean-by-clean pairs, plus 20 pairs drawn at random from the rest (at least one scene recognised), so 40 pairs a half. Each pair is shown in both orders, to fresh Opus and fresh Sonnet judges (claude-opus-5-5 and the current Sonnet; no Fable), 20 judgements to a judge, the two orders of a pair never to the same judge.

Stage 1: brief version 1 on half A. If it passes, half B is run with the same brief as a confirmation and the two pooled. If it fails, the brief is mended once (BRIEF-v2.md) and run on half B, which no judge has seen; the result on half B is the result.

## Measures

- A pair's verdict for one judge model: admired (both orders pick it), forgettable (both orders pick it), or tie (the orders disagree).
- Decided share: pairs not tied. Accuracy on decided pairs: admired verdicts over decided. Strict accuracy: admired verdicts over all pairs.
- Position bias: share of all single judgements that pick the scene shown first.
- Length bias: share of single judgements, among pairs differing by 5 words or more, that pick the longer scene.
- Agreement: share of pairs where Opus and Sonnet give the same verdict (admired, forgettable or tie), and Cohen's kappa on those three classes.
- Memory: the same accuracies on pairs with at least one recognised scene, reported beside, never gating.

## Pass mark (on clean-by-clean pairs of the deciding stage)

The judge passes only if all hold, for each of the two judge models:
1. accuracy on decided pairs at least 85%;
2. decided share at least two in three;
3. position bias between 40% and 60%;
4. length bias between 40% and 60%;
and for the panel:
5. Opus and Sonnet give the same verdict on at least 70% of pairs.

Honest size: 20 clean pairs in a stage (40 pooled). At 20 pairs, 85% means 17; the uncertainty is about plus or minus 15 points, so a pass is a sign, not a proof, and a near miss is reported as such.
