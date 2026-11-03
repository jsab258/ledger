# The claim check's labels by a scripted labeller: trial spec (3 November 2026)

For n02-6-4-bulk-api, the plan's first use (PLAN-2026-11-02.md). Written before any call. Reference: none found (no game's method); the 3 November harm sort is the pattern.

## Questions, written first

1. Given the bench's own label definitions, the speaker's facts and the detail alone, how often does Haiku 5.5 give the gold label, exactly and on the line that matters, supported (stated, implied) against not (added, contradicted)?
2. Of the 42 invented held details, how many does it call supported, the direction that hides leaks? Does it call d062 (the one invented detail Haiku's check passes) contradicted?
3. Are its misses the 51 rows the first two labellers split on, or rows both agreed?
4. Only if 1 to 3 pass: of the new details it writes, how many keep their label on a blind relabel?

## The 238

F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl, built 30 September by ledger/ClaimBench/DetailBench.cs: 255 rows, less the 17 labelled "noclaim". The 238 are 111 tune (26 questions; 61 supported, 50 invented) and 127 held (31 questions; 85 supported, 42 invented).

One row: id (d001); card (lena = Sheila, rocco = Ron, sam = Darren); probe; detail (a phrase of about 32 characters: 118 the check refused, 87 it passed, 33 planted by changing a number or name); known (that speaker's 50 to 52 numbered facts, about 6,900 characters); label (stated, implied, added or contradicted); kind; half; labels (Opus 5.5, Sonnet 5, and Fable 5.1 only where the first two split: 51 rows).

## The method

- Held out: the 127 held rows are the measure, read once, nothing chosen on them. The 111 tune rows are the practice half for a second try's wording (two tries, then research). All 238 go in the first run, reported apart.
- Single calls (batch for stage 2). Request per row: id = the row's; model claude-haiku-5-5; system = DetailBench.cs's DetailRule word for word, then "Give the JSON first, on one line, and write nothing after it."; one user message, "WHAT THEY KNOW:\n" + facts + "\n\nTHE DETAIL:\n" + detail (the bench's own form, no question); max_tokens 1,500 (the answer is about 40; the rest is room for reasoning, as the harm sort's 160 ran out). Over 5% cut or unparsed is a setup fault: rerun once at 3,000, not a try.
- Stage 2, only if the bar holds: per question, one call asks for 8 new details, half supported but reworded, half with one added or wrong detail (NEARMISS wording, tools/checkers/gemini_training_data.py; no alcohol or gambling, no children, no real brands or people, nothing after 1992); each relabelled blind as above. Kept: the label equals the intention and is not among the 255. A fresh reviewer then reads 80 kept, blind (Gemini's 617 had 77 of 80).
- Measuring only: files in F:/LedgerTools/checkers/claim-labels-2026-11-03, marked so; train_checker.py never reads them (LOCAL-CHECKERS section 4).

## The bar (inferred; no source sets one)

On the 127 held, once: supported-or-not agrees on at least 115 (9 in 10; against gold Sonnet 5 had 105, Opus 5.5 121), and at most 2 of the 42 invented called supported (Opus 1, Sonnet 4, Haiku's check 1). Reported beside it: exact five-way match; the 187 undisputed rows against the 51 split. Below the bar, no Haiku label is kept.

## Worst-case cost (PRICE table, 2.5 characters a token)

Stage 1: 238 requests, 1.80 million characters, US$0.25 (US$0.43 if rerun at 3,000). Stage 2: 58 writes and at most 464 labels, US$0.52 (US$0.26 as a batch). Today's ceiling US$21.94, US$20.72 left.

## What could not be found or settled

- No source sets an agreement bar; Gemini's spot check (77 of 80) names no threshold.
- The plan's "238" is stated nowhere; it is 255 less 17 (LOCAL-CHECKERS, speed-sizes line).
- Gold is Claude-made and close to Opus's (equal on 120 of 127 held), so agreement flatters a Claude labeller. The only independent labels, Gemini's 617 (F:/LedgerTools/checkers/train3), are sentences, not details.
- Haiku is also the shipped check, so its labels share its blind spots (question 2 tests only d062); new details use the same three fact lists.
- api_batch.py cannot set `thinking`; SUCCESSORS-2026-10-07.md says Haiku 5.5 reasons by default (not re-checked); switching it off needs a change to params(). Haiku 5.5's price is the table's, not re-read.

## Stage 1's result (3 November, 21:43; raw F:/LedgerTools/checkers/claim-labels-2026-11-03: requests, answers, agreement.json)

238 single calls to claude-haiku-5-5 through tools/api_batch.py, US$0.10 (worst case US$0.25), every answer read (none cut at 1,500 tokens). Scored by tools/checkers/claim_label_trial.py.

| | Held (127, the measure) | Tune (111) |
|---|---|---|
| Same label exactly | 102 | 83 |
| Same side of supported against not | **114** (bar 115) | 96 |
| Invented called supported | **2 of 42** (bar at most 2) | 2 of 50 |
| On the 27 / 24 disputed rows | 20 | 12 |
| On the undisputed rows | 94 of 100 | 84 of 87 |

- **Below the bar by one row** on the held half (114 against 115), on the invented side at it; d062, the invented detail Haiku's own check passes, it calls contradicted. Between Sonnet 5 (105) and Opus 5.5 (121) on the same rows.
- **Decided, by the spec:** no Haiku labels are kept and stage 2 is not run. The held half has now been read, so a second try cannot be tuned or chosen on it; a second labeller (Sonnet 5.5, about US$0.40 worst case) would be a new try with a new held set, for the next harm sort or label need, not tonight.
