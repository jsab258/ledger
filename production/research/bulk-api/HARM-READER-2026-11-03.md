# The blind harm sort by a scripted reader on the API credit (3 November 2026)

For n02-6-4-bulk-api, the plan's third use (PLAN-2026-11-02.md: "text-only judgements now done by helpers ... each moves when a scripted reader agrees with the helpers' past verdicts on the same material, agreement measured, not assumed"). Reference: none found (no game's method; the source test's own harm sort is the material).

## Questions, written first

1. On the 64 invented sentences a helper has already sorted blind (the 37 of 27 October, F:/LedgerTools/checkers/try4/harm37-verdicts.json, and the 27 of the source test, F:/LedgerTools/checkers/source/harm-source-verdicts.json), how often does a scripted reader, given the same speaker's facts, question and sentence and nothing of where it came from, give the same verdict (HARMFUL, HARMLESS, NOT invented)?
2. How often does it agree on the line that matters for the speech bar, harmful against not harmful?
3. Where it disagrees, is it the helper's low-confidence calls, or something the reader gets wrong?
4. What does one verdict cost, against a helper's time on the same packet?

## The method

- The reader: Claude Sonnet 5.5 through tools/api_batch.py (single calls), not Haiku: Haiku is the check that let these sentences through, so it would judge its own misses.
- Its instructions are the harm sort's own definitions (SOURCE-TEST-2026-10-27.md, question 1): harmful is a person, place, time or event the facts lack, or a contradiction of them; harmless is opinion, overstatement or manner; NOT when the sentence is in fact supported. It answers in one word with a confidence flag and one line of reason.
- Its facts: each row's own context (F:/LedgerTools/checkers/train3/TEST3.json for the 37, the packet's "known" for the 27).
- The bar (inferred, no source sets one): harmful against not harmful in at least 9 of 10, and no disagreement outside the helper's low-confidence calls that a fresh look settles for the reader. Below that, the harm sort stays with a fresh helper.
- What this cannot settle: these labels are for measuring only; nothing made by a Claude model trains a checker (LOCAL-CHECKERS-2026-10-26.md, section 4: Anthropic's terms are unclear on it; his answer of 26 October trained the checker on Gemini's labels).

## Results (3 November; raw F:/LedgerTools/checkers/harm-reader-2026-11-03: requests, answers, agreement.json)

The first run cut most answers: the reader reasons before its verdict and 160 tokens ran out (46 of 64 unparsed; US$0.44). Run again with 700 tokens and the verdict asked for first: all 64 parsed (US$0.41). That second run is the measure.

| | The 37 (27 Oct) | The 27 (source test) | All 64 |
|---|---|---|---|
| Same verdict as the helper | 26 | 11 | 37 (58%) |
| Same side of harmful against not | 28 | 17 | 45 (70%) |

1. **Below the bar** (9 in 10 on the harmful line): the harm sort stays with a fresh helper.
2. **Why, from the disagreements:** the reader does not know the game is set in 1990, so "since the scheme finished last year" reads to it as a wrong date (three sentences the helper rightly passed); it reads by meaning where the helper read as a player hears, so "Will left you the office" is the will to it and a man called Will to the helper (four); it calls far more sentences supported (NOT: 14 against the helper's 3), Gemini's "invented" label and the helper both disagreeing.
3. **The helper's low-confidence calls** are 10 of the 27 disagreements.
4. **Cost:** about US$0.0064 a verdict at Sonnet 5.5's single-call price (half in a batch), against a helper's packet of 27 to 37 verdicts.

**Try 2, when a harm sort is next due** (both sets' disagreements are now seen, so tuning on them would flatter it): the reader told the game's date and to judge each sentence as a player hears it, run blind on the same packet the helper sorts, compared before either is used. Until then nothing moves off the allowance.

**Found on the way, mended:** tools/api_batch.py's "worst case" priced input at 3.5 characters a token; the requests measured 2.84 (495,828 characters, 174,565 tokens), so the first run's worst case (US$0.39) was under its cost (US$0.44) and the ceiling check was not safe. Now 2.5; its self-test 9 of 9.
