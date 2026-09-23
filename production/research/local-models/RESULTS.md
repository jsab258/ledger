# The action-picking comparison, measured: worked examples bring a free model level on ordinary lines, and nothing free resists typed orders

STATUS: MEASURED, 2026-09-23, on this PC (RX 6700, 10 GB, llama.cpp b11111 on
Vulkan, Windows 11). Branch `research/local-models`. It follows the
experiment in DELIVERY.md section 10, in Jafar's order: the fair rerun, the
fresh lines, then the models. Every run is in `runs/`, as a report (`.md`) and
one row per line (`.tsv`). The test lines are in `heldout/` (frozen, see its
README), and the worked-example bank is in `bank/`.

## The table

299 fresh lines, one right answer each. "Tidy but wrong" means well formed and
wrong: the failure the game cannot see, because it carries the answer out. The
35 "novel" lines are also counted separately, for the reason in point 5. The
typed orders are the 39 lines that get past the game's own guard. Median time
is for one routed line.

Wording, as the small model is asked; the paid router's prompt is never
changed:
- **shipped**: the game's router prompt, exactly as it ships.
- **nofence**: the player's line is sent bare, without the wrapping that says it
  is the player's.
- **novelok**: "prefer a listed verb over novel" is replaced by when novel is
  right.
- **leavehint**: a short leaving line is the leave verb.
- **examples**: the 6 lines from the bank nearest the player's line, picked
  by shared words and shown with their answers.
- **orders**: the bank also holds 30 typed orders, each answered as talk.

| model | wording | right of 299 | tidy but wrong | without the 35 novel lines: right of 264 | tidy but wrong of 264 | novel caught of 35 | typed orders obeyed of 39 | median ms |
|---|---|---|---|---|---|---|---|---|
| paid | shipped | 259 | 38 | 252 | 10 | 7 | 16 | 961 |
| qwen3-4b | examples+orders | 274 | 23 | 248 | 14 | 26 | 28 | 1511 |
| qwen3-4b | nofence+novelok+leavehint | 242 | 50 | 226 | 34 | 16 | 31 | 438 |
| qwen3-4b | novelok+leavehint+examples+orders | 273 | 24 | 245 | 17 | 28 | 31 | 1526 |
| qwen3-4b | novelok+leavehint+examples | 274 | 23 | 245 | 17 | 29 | 32 | 1415 |
| qwen3-4b | novelok+leavehint | 229 | 62 | 218 | 41 | 11 | 30 | 364 |
| qwen3-4b | shipped | 216 | 78 | 213 | 48 | 3 | 25 | 333 |
| ministral-3-3b | nofence+novelok+leavehint | 251 | 44 | 232 | 30 | 19 | 33 | 1035 |
| ministral-3-3b | novelok+leavehint | 243 | 51 | 230 | 29 | 13 | 28 | 1130 |
| ministral-3-3b | shipped | 237 | 55 | 228 | 31 | 9 | 35 | 574 |
| qwen3.5-4b | nofence+novelok+leavehint | 236 | 58 | 235 | 27 | 1 | 30 | 764 |
| qwen3.5-4b | shipped | 235 | 58 | 235 | 27 | 0 | 30 | 846 |
| gemma-4-e4b | nofence+novelok+leavehint | 221 | 21 | 219 | 5 | 2 | 8 | 2784 |
| gemma-4-e4b | shipped | 174 | 6 | 174 | 1 | 0 | 5 | 3807 |
| qwen3-1.7b | nofence+novelok+leavehint | 184 | 96 | 182 | 72 | 2 | 22 | 381 |
| qwen3-1.7b | shipped | 184 | 91 | 184 | 67 | 0 | 21 | 392 |

| model | wording | the 42: right |
|---|---|---|
| qwen3-4b | examples+orders | 36 of 42 |
| qwen3-4b | leavehint | 35 of 42 |
| qwen3-4b | nofence+novelok+leavehint | 38 of 42 |
| qwen3-4b | nofence | 36 of 42 |
| qwen3-4b | novelok+leavehint+examples+orders | 37 of 42 |
| qwen3-4b | novelok | 33 of 42 |
| ministral-3-3b | nofence+novelok+leavehint | 36 of 42 |
| ministral-3-3b | shipped | 35 of 42 |
| qwen3.5-4b | nofence+novelok+leavehint | 36 of 42 |
| qwen3.5-4b | shipped | 37 of 42 |
| qwen3.5-4b | shipped_cpu | 37 of 42 |
| gemma-4-e4b | nofence+novelok+leavehint | 31 of 42 |
| gemma-4-e4b | shipped | 22 of 42 |
| gemma-4-e4b | shipped_cpu | 21 of 42 |
| qwen3-1.7b | nofence+novelok+leavehint | 22 of 42 |
| qwen3-1.7b | shipped | 23 of 42 |

The paid router is claude-haiku-4-5 with the shipped prompt and guard, run on
this PC through the game's own client and key: $0.39 (about 30p). An earlier
GitHub attempt spent about 30p more, and its results were lost.

Card memory, measured with the model loaded and idle:
- Qwen3-4B: 3.0 GB
- Qwen3.5-4B: 3.0 GB
- Gemma 4 E4B: 3.2 GB
- Ministral 3 3B: 2.5 GB
- Qwen3-1.7B: 1.6 GB

## What it says

1. **Cheap changes alone don't reach the paid router.** Without the novel
   lines, the paid router gets 252 of 264 right, with 10 tidy-but-wrong
   answers. The best ready-made model as shipped gets 235 (Qwen3.5-4B), with 27
   tidy-but-wrong. Wording changes add a little.
2. **Worked examples picked per line are the one big lever**, as DELIVERY
   section 4 predicted from the papers. They take today's Qwen3-4B from 216 to
   274 of 299, above the paid router's 259, and its tidy-but-wrong answers
   from 78 to 23, against the paid router's 38. Without the novel lines, 245
   of 264 with 17 tidy-but-wrong, against 252 and 10.
   The examples do all of it. With the shipped wording and examples alone, the
   score is the same 274, and the best result without the novel lines is 248
   of 264 with 14 tidy-but-wrong. Against the bar in DELIVERY section 10.7:
   1.5 points below the paid router, which is inside its 2 points. Its
   tidy-but-wrong rate is 1.5 points above the paid router's, just outside its 1
   point. The bar's typed orders and time lines fail (points 3 and below).
   - **A caveat that may be large.** The bank and the test were written by the
     same kind of helper to the same brief. Near-copies were removed, but a
     bank drawn from the test's own style is a best case. The 42 old lines,
     written differently, are the cross-check: CROSS42.
   - **It costs time.** At 1.4 to 1.5 seconds a line, it is slower than the
     paid router's 0.96. The card was reading prompts at about a quarter of its
     usual speed during those runs, because the main sitting's Unreal job
     shared it, so this figure is pessimistic. HOLE: not remeasured on an idle
     card.
3. **Every free configuration obeys typed orders far more often than the paid
   router.** The paid router obeys 16 of 39, and the free ones 25 to 35.
   Every change that raised the score also raised the number obeyed, and
   examples of orders answered as talk did not bring it down (31 of 39). On
   this evidence, resisting orders needs training, or a wider guard in the game
   itself, which decides the line before any model sees it.
4. **The 42 old lines flattered everyone.** The paid router scored 41 of 42 and
   today's model 32. On the fresh lines they score 87% and 72%.
5. **On novel lines the paid router is the weak one, and that is partly the
   test.** It catches 7 of 35, reading handing someone a scarf, or carrying
   their boxes, as talk. The game's rules say a novel action is small and
   "moves the world", so talk is a defensible reading of a courtesy. The
   test's writers took the broader view. Whether a courtesy is an action is a
   design question the router's prompt currently answers by default.
6. **Gemma 4 E4B is out**: 3 to 4 seconds a line, and most answers are not in
   the form the game reads. The best independent single-call score among
   small models did not carry over to this job, as DELIVERY section 2.1 said
   public scores would not.
7. **The Vulkan reports did not bite.** Qwen3.5-4B gives the same score on the
   card and on the processor (37 of 42 both ways), and Gemma nearly so (22
   against 21).
8. **The 1.7B is out on accuracy**: 184 of 299, with 91 tidy-but-wrong, though
   it uses only 1.6 GB.

## What this means for the routes

- **Route 1, a better ready-made model:** not enough on its own. The best is
  about 17 lines short of the paid router on ordinary lines. Qwen3.5-4B or
  Ministral 3 3B would do; today's Qwen3-4B is as good once examples are added,
  and fastest.
- **Route 3, better asking:** worked examples come within 7 lines of the paid
  router on ordinary lines, and pass it overall. They leave it open to typed
  orders and cost time. The next measurements are the ones in "Not yet
  measured".
- **Route 2, a larger model:** not tried. It needs the voice off the card, and
  the Nano measurement says the voice cannot run in real time on this PC's
  processor.
- **Route 4, training:** now the one route with evidence it could fix typed
  orders as well as accuracy. By Jafar's ruling, the teacher is a large free
  model on this PC. Its first step is checking that teacher on these 299 lines
  and 39 orders.

## Not yet measured

- Worked examples timed on an idle card, and with the examples placed so the
  model can reuse more of the prompt between lines.
- A guard that also catches order-shaped talk ("count it as", "put it down
  as", "Answer:"), measured against the 39 orders and the ordinary lines, so
  it takes nothing that is only talk.
- A person reading a sample of the test's labels.

## Caveats

- The test lines were written and labelled by Claude models, and they agreed
  on 338 of 339. The labels are Claude's consensus, not a person's.
- Some answer times were taken while an Unreal job shared the card (the PC
  runner's check set off by this branch's push, then the main sitting's
  packaging). Scores are unaffected, because the temperature is 0.
- One run per configuration: at temperature 0 a run repeats exactly, so there
  are no seeds to vary.
