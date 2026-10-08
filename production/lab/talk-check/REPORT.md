DO NOT SWITCH: the local checker is less accurate than Haiku 5.5 and no faster where it matters.

# The talk check on other models (lab test 6, 8 October 2026)

16:20 to {END}, branch lab. Spent: $0.00 of the $2 (no API was called).

## What was run

- **The labelled sets and selection of 7 October's Haiku 5.5 run** (production/research/invented-claims/SUCCESSORS-2026-10-07.md; ledger/ClaimBench/Successors.cs on wip):
  - **Details:** the held half of detail-gold.jsonl, 127 details (85 true, 42 invented).
  - **Replies:** 30 from the 28 September bench's held sets, 15 invented and 15 honest.
- **The local checker:** LettuceDetect's TinyLettuce Ettin 68M (KRLabsOrg/tinylettuce-ettin-68m-en, MIT, 277 MB; downloaded with your yes). It runs on this PC's CPU, 6 threads, isolated in F:\LedgerTools\pylib\lettuce. It is not a prompted model: it marks the parts of a sentence that the character's known facts do not support. So "the same prompts" means the same inputs here: the known facts, the player's line, and the detail or the reply's first sentence.
- **First sentence only,** as ordered: of each reply, only sentence 1 went to the checker. Only about 3 (by word overlap) of the 15 invented replies have their invented detail in sentence 1, so a first-sentence check can catch at most those; Haiku's whole-reply figures below are not like for like on replies.
- **Gemini:** {GEMINI}

## The table

| model, setting | true details refused | invented details passed | detail check median / slowest tenth / slowest | first sentences: invented replies caught | honest replies flagged | first-sentence median / slowest | cost |
|---|---|---|---|---|---|---|---|
| **Haiku 5.5, the split** (7 Oct, held half; replies are the whole check) | 23/85 (27%) | 1/42 (2%) | 0.97 / 1.99 s | 14/15 (whole reply) | 4/15 (whole reply) | whole check 2.13 / 3.87 s | US$0.10 and $0.50 per million tokens in and out |
| Haiku 5.5, thinking off (7 Oct) | 22/85 (26%) | 6/42 (14%) | 0.70 / 1.01 s | 13/15 (whole reply) | 7/15 (whole reply) | whole check 1.85 / 2.42 s | the same |
| **TinyLettuce 68M, local CPU, its own threshold** | 8/85 (9%) | 25/42 (60%) | 1.30 / 1.81 / 11.6 s | 3/15 | 0/15 | 0.37 / 0.41 s | $0 |
| **TinyLettuce 68M, threshold chosen on the tuning half** (0.004: to pass at most 2 of 50 invented there) | 70/85 (82%) | 4/42 (10%) | 1.63 / 1.86 / 2.13 s | 13/15 | 11/15 | 0.33 / 0.35 s | $0 |

## Recommendation

**Do not switch: keep Haiku 5.5 as the split** (7 October's recommendation stands).
- **Accuracy:** the local checker is much worse at either setting.
  - At its own threshold it lets 60% of invented details through (Haiku 5.5: 2%).
  - Set strict enough to stop them, it refuses 82% of true details (Haiku 5.5: 27%), and it flags 11 of 15 honest first sentences.
  - It cannot tell an invented detail from a true one in LEDGER's speech: a model trained on other people's question-answering data, used without training on LEDGER's own facts.
- **Speed:** it is faster only on the short first sentence (0.33 s on the CPU), and slower than Haiku per detail (1.3 to 1.6 s against the long fact list).
- **The rule** was to switch only if accuracy is no worse and it is faster. It fails the first half outright.
- **What could change that, for later:** the research's own route (frontier-ai-uses HE, item 3). Fine-tune such an encoder on true and false sentences generated from LEDGER's simulation, not on Claude's output, then check it on this bench. Untried here.

Files: production/lab/talk-check/local_check.py and local_sweep.py (rerun with `python -S`); results in F:\LedgerTools\lab\talk\.
