# Fable 5.2 against Opus 5.5, a blind replay (9 to 10 November 2026)

The advisor's messages 70 to 74 (9 Nov): re-test when a new model arrives (RULINGS 9); clothing first; verdict on his page by 17:00 Tuesday 10 Nov, cap about 5% of the week. Method copied from the 8 Nov Sonnet replay (production/research/token-audit/SONNET-BLIND-REPLAY-2026-11-08.md).

## Set-up (9 Nov 22:33 to 22:41, a helper)

- Copies: C:/LedgerTools/replay-2026-11-09/, `git clone --shared` with a sparse checkout at the commit before each fix, other history removed; DECISIONS, NOTEBOOK, RECIPE, FOR-JAFAR left out. About 63 MB each, 10 copies.
- Problems and start commits: cuffs 7dd408b09 (before the elastic rule entered the order and the skill); neckband 0f67e7e0c; head clearance c33250a0d (before the first of its three tries); control, the 8 Nov gate fix, e88bf2856.
- Briefs: BRIEFS.md there, word for word the same per model. Key, label map and run costs in key/ (kept from runs and judge).
- Model confirmed: Fable 5.2 is offered to helpers in this session; his plan shows a separate weekly Fable meter (0% at 22:24, 8% at 23:15, 15% at 00:14).
- Resets (advisor 74): the usage reading shows no reset count, rule or mid-week use; unknown without his hands. His two stay unspent.

## Result (judged blind, then unblinded with key/MAPPING.md, 10 Nov 00:30)

| Problem | Opus 5.5 high | Fable 5.2 high | Extra | Judge |
|---|---|---|---|---|
| cuffs | 7.5, usable, builds the cuff onto the drape (the method that worked) | 6, sizes the cuff to the solver's floor, no elastic or freeze | Opus max 8.5 (best: keeps triangles, UVs, seams); Fable xhigh 6 | Opus better |
| neckband | 5, partial (leans the band in rather than shortening each column) | 5, partial, same miss | | equal |
| head clearance | 8.5 (wrong body and head mesh found first pass; 3 mm floor thin) | 9 (same, plus a pose-wise measure) | | equal, leaning Fable |
| control: gate fix | 7, catches 46 of 48 real WAIT runs (misses an older wording) | 9, catches 48 of 48, also fixes lines lost at the reader's 1 MB edge | | Fable better |

All four problems: every run named the right cause class; none ran on real meshes (no Blender or Marvelous by design). Verdicts: judge/clothing-verdict.md, judge/control-verdict.md (one fresh Opus final-reviewer each, labels only; the control checked on the real session logs).

Cost (helper tokens; time):

| | Opus high | Fable high |
|---|---|---|
| tokens, four problems | 781,348 | 1,161,772 (1.49x) |
| wall time | 3,210 s | 6,617 s (2.1x) |
| top settings on the cuffs | Opus max 528,114 tok, 3,506 s, 8.5 | Fable xhigh 556,933 tok, 4,340 s, 6 |

At list prices (Fable twice Opus per token) Fable high cost about three times Opus high for the same problems. In the plan's meters the night took the week from 8% to 16% (the replay most of it, with the crown measurement and the solve's diagnosis) and Fable's own weekly meter to 15%: the 5% cap was overshot by about 3 points. Dollars per run are not split out (input and output not separated in the notifications; unverified).

## What it says

- Clothing: Fable is not better at our hardest discipline; Opus led on the cuffs, tied the neckband, nearly tied the head clearance. Anthropic's claim that Fable high matches Opus max at half the cost is not borne out here: Opus max was the best cuffs run at a similar token count to Fable xhigh's, which scored 6, no better than Fable high.
- Code on real data: Fable's gate fix was the only one correct on all real logs, one sample.
- Two of Fable's five runs started their own reviewers unasked; Fable was slower and dearer on every problem.
- Recommendation: no switch of the session or clothing; Fable 5.2 only as the escalation model for code and tool faults after two failed Opus tries (the tries rule's one different method), re-tested at the next model. Unverified: one sample per problem; the picture-judging task (advisor 72a) was not run, to stay near the cap.

## Runs (helper tokens and wall time from the task notifications)

| Run | Model, effort | Tokens | Seconds |
|---|---|---|---|
| cuffs | Fable high / Opus high | 343,950 / 244,617 | 2,594 / 1,253 |
| neckband | Opus high / Fable high | 215,667 / 310,072 | 759 / 1,424 |
| head clearance | Fable high / Opus high | 358,542 / 220,386 | 2,046 / 1,014 |
| control | Opus high / Fable high | 100,678 / 149,208 | 184 / 553 |
| cuffs extra | Fable xhigh; Opus max | 556,933; 528,114 | 4,340; 3,506 |
| judges | Opus final-reviewer, control; clothing | 65,431; 71,001 | 124; 274 |

Labels to models: key/MAPPING.md. Partway, the week went from 8% (22:24) to 12% (23:15), and to 16% by 00:14, with the replay, the crown measurement and the solve diagnosis together; the replay alone is not split out yet.

## Not done

- The picture-judging task (advisor 72a), held back for the cap.
- No run's method was tried on the real meshes or in Marvelous.
