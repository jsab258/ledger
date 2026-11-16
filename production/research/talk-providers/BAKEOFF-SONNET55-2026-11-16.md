# n16-6 bake-off, leg 1: Sonnet 5.5 against today's Sonnet 5 (16 November 2026)

Questions written before any paid call (speech-bench skill, step 1). Method: METHOD-NOTE-2026-11-16.md section 5 and its review's changes. Reference: none found for live talk; study A (inZOI) is the outside reference (order of 2 November, n02-3-1-speech).

## Questions

1. On a newcomer's real questions, is Sonnet 5.5's first sentence sooner than Sonnet 5's (median first-sentence time, how many under 2.0 s, the worst)?
2. Does Sonnet 5.5 invent more or fewer details (the engine's invented count per turn, judged by the game's whole check, ClaimCheck.CheckAsync, on the same facts and prompts)?
3. Does it fall back to "that's all I know" more or less often where the person could answer?
4. What does a reply cost on each (the run's own cost line, the price card's figures; Sonnet 5 and 5.5 are both priced at US$2 / US$10 a million on the card, read 28 Sep and 7 Oct: to be read again before any cost reaches his page)?
5. Small talk beside: the same figures on the held set's small-talk lines, never instead.

## How it is measured

- The bench's `firsts` on the held newcomer set (firsts-held.txt, twenty questions, the same set as the in-game run F of 4 November), to Sheila, Ron and Darren: 60 turns an arm.
- The game's own talk settings mirrored: the early hand-over (--early, as CrimeProbe starts the talk program), the ladder and its judge, the cached briefing and checks, the check on Haiku 5.5 (TalkHelper CheckerDefault), the fast checker at his open cut-off.
- Arm A, today's game: models by moment (--moment): real conversation on Sonnet 5, small talk on Haiku 4.5. Arm B: every line on Sonnet 5.5 (--model). The bar is read on the questions the game sends to the core model (arm A rows whose model is Sonnet 5), the same questions in both arms; the rest is small talk, reported beside.
- One turn at a time (--parallel 1), so turns do not slow each other; the arms run back to back on the same machine and network.
- This is a screen beside the game, not the bar: a winner goes into the packaged game (run G's way: -AskSet firsts-held.txt -AskNear) before any figure reaches his page.

## Money

- His plan's API credit: the month runs from about the 12th (api_batch.py BILLING_DAY 12; unconfirmed until the bill shows). No paid call is logged since 8 November, which was last month. Assumed credit left US$200 (the console figure is his to read): over 26 days left, today's ceiling is about US$7.69.
- The bake-off's task "bakeoff-2026-11-16" is capped at US$4.00 in code (ClaimBench KeyTaskCaps); each arm at US$1.00 (--cap). Each run goes to production/api-spend.jsonl.

## Results

Raw runs: F:/LedgerTools/town-scratch/bakeoff-2026-11-16/<arm>/ (firsts.jsonl, run.log). Times are the first sentence handed over (--early); a turn whose first sentence was held back counts its whole turn. "Caught in drafts" is the engine's LastInvented: details the check refused in a draft, before a redraft (so a cost in time, not a detail let through).

| Arm | Model | Median first sentence | Under 2.0 s | 90th pct | Worst | Held back | Fell back | Caught in drafts (turns) | US$ (60 turns) |
|---|---|---|---|---|---|---|---|---|---|
| A, done 10:19 | Haiku 4.5 (the game's moment rule) | 1.81 s | 32 of 60 | 6.62 s | 16.14 s | 4 | 0 | 49 (36) | 0.250 |
| B, done 10:25 | Sonnet 5.5, no thinking field (invalid: 26 empty drafts) | 4.51 s | 1 of 60 | 5.69 s | 10.40 s | 33 | 1 | 15 (12) | 0.412 |
| C, done 10:32 | Sonnet 5, no thinking field (as the game sends it) | 2.50 s | 19 of 60 | 6.52 s | 14.52 s | 9 | 4 | 54 | 0.349 |
| A2, done 10:38 | Haiku 4.5, the repeat of A | 1.54 s | 35 of 60 | 4.69 s | 10.84 s | 5 | 2 | 54 | 0.194 |
| B2, done 10:45 | Sonnet 5.5, thinking at its lowest (between_tools) | 1.89 s | 30 of 60 | 6.93 s | 9.46 s | 8 | 6 | 62 | 0.359 |
| C2, done 10:52 | Sonnet 5, thinking off | 2.33 s | 26 of 60 | 5.87 s | 10.38 s | 4 | 4 | 79 | 0.343 |
| C3, done 11:00 | Sonnet 5, thinking off (second pair, run first) | 2.61 s | 24 of 60 | 7.09 s | 10.39 s | 5 | 3 | 61 | 0.356 |
| B3, done 11:06 | Sonnet 5.5, between_tools (second pair) | 2.09 s | 29 of 60 | 5.96 s | 13.98 s | 7 | 6 | 54 | 0.354 |

Spent US$2.62 of the task's US$4.00 (US$1.91 before the second pair), all logged in production/api-spend.jsonl.

## What leg 1 says (a screen beside the game, not the bar)

- Sonnet 5.5 against the model it would replace, both with thinking at their lowest (B2 against C2): first sentence 0.44 s sooner at the median (1.89 against 2.33 s), 30 against 26 of 60 under 2.0 s, the worst 9.5 against 10.4 s, fewer details caught in drafts (62 against 79), the same price (cache hits half Sonnet 5's), but 6 fall-backs to "that's all I know" against 4. The two runs of the same Haiku arm (A, A2) differ by 0.27 s at the median and 3 under 2.0 s, so the speed gain is about the noise's size: one more pair of runs, or the packaged game, decides it.
- Sonnet 5.5 cannot simply replace Sonnet 5 in the game: the game sends no thinking field, and with none Sonnet 5.5 returned 26 empty replies of 60 (arm B). Its thinking must be set (between_tools) wherever it is used; the switch exists for the bench only (--reply-thinking-off).
- Haiku 4.5, which the game's moment rule actually uses for these questions, is the quickest and cheapest here (1.54 to 1.81 s, about US$0.004 a turn); whether its replies are as good is not measured by this bench (the fall-back count only).
- Not reached: a blind reader's judgement of reply quality on each arm (the order's "invented details" is counted only as the check's catches in drafts, plus fall-backs); the other providers (Google's and OpenAI's small models, an open model on a fast host, a local model), which need their keys (the router key is on the waiting list); the packaged in-game run of any winner.
- The second pair (C3 then B3, order swapped) repeats the median gain: Sonnet 5.5 0.52 s sooner at the median (2.09 against 2.61 s), 29 against 24 under 2.0 s; over both pairs 0.44 and 0.52 s, larger than the 0.27 s between two runs of one arm. It also falls back more in both pairs (12 against 7 of 120 "that's all I know"), but mostly where that is right: B3's six are five on questions nobody could answer and one partly; on answerable questions it is 3 against 3 over both pairs. The tails do not agree: the 90th percentile was worse for Sonnet 5.5 in the first pair (6.93 against 5.87 s) and better in the second (5.96 against 7.09 s), the worst turn better then worse (9.46 against 10.38 s, 13.98 against 10.39 s), and its first sentence was held back more (15 against 9); the Haiku repeat moved the 90th percentile by 1.9 s and the worst by 5.3 s. So only the median gain is consistent, on one run of 60 correlated turns per arm.
- The fall-backs against the held set's fixed labels (firsts-answerable-held.jsonl: 23 of the 60 card-question pairs answerable, 25 partly, 12 not): on questions the person can answer, Sonnet 5.5 fell back 3 times over both pairs (B2: Sheila to the greeting and to the opening time, Darren to the opening time; B3: none), Sonnet 5 also 3 times (C2: 1, C3: 2); Sonnet 5.5's extra fall-backs are on questions only partly answerable or not. Computed offline from the runs, no calls.
- The final replies judged by the two labellers (ClaimBench firsts-label, on his subscription, not the API; label.log and firsts-labelled.jsonl in each arm's folder): invented details found by both labellers, Sonnet 5.5 1 (B2) and 3 (B3) of 60, Sonnet 5 1 (C2) and 2 (C3); disputed 8 and 2 against 13 and 7; fall-back where the person could answer at least partly (48 pairs), Sonnet 5.5 3 and 1, Sonnet 5 2 and 3. Over both pairs: invented 4 against 3 of 120, fall-backs on answerable 4 against 5 of 96. No difference in what the newcomer hears at this size; the median speed gain is the one consistent difference.
- Next for leg 1: the packaged run with Sonnet 5.5 for the core moments (run G's way), before anything reaches his page. Both after the reset.

Findings so far:
1. On the bench, the moment rule (TalkMoment.Of on the question's words alone) makes all twenty held newcomer questions small talk, so arm A ran on Haiku 4.5. The game itself also passes a deed or evidence, a standing deal and its own moment (TalkHelper Program.cs line 1122), any of which makes a line Conversation and so Sonnet 5: which model the in-game runs (F, 4 Nov) used is unchecked (corrected after the review).
2. Arm B is not a valid measure of Sonnet 5.5: 26 of its 60 replies were empty ("..."), because Sonnet 5.5 thinks by default and the game sends no thinking field, so its thinking spent the draft's 300 tokens (ConversationEngine.ValidateReply turns an empty draft into "..."). Fixed for the bench: with --reply-thinking-off, Sonnet 5.5 is sent its lowest setting, "between_tools" (it refuses "disabled"); CoreTests case added. B is run again so.
3. Arm C (Sonnet 5 on every line, today's core model) is added so Sonnet 5.5 is compared with the model it would replace.
4. Prices read again 16 Nov at https://platform.claude.com/docs/en/about-claude/pricing: Sonnet 5 and 5.5 US$2 in, US$10 out; cache hits Sonnet 5.5 US$0.10, Sonnet 5 US$0.20; Haiku 4.5 US$1 / US$5; Haiku 5.5 US$0.10 / US$0.50 under 100,000 tokens. The game's price card agrees.
5. The timing runs shared the processor with an Unreal build (10:16 to about 10:22) in arm A's first minutes; arm A is repeated (A2) as a check on noise.

## How each arm was run (added after the review)

Every arm: `dotnet run --project ledger/ClaimBench -c Release --no-build -- firsts --set held --key --task bakeoff-2026-11-16 --cap 1.00 --early --ladder --judge-ladder --cache-briefing --cache-checks --checker claude-haiku-5-5 --fast-checker --parallel 1 --dir <arm folder>`, plus: A and A2 `--moment` (no thinking switch, as the game); B `--model claude-sonnet-5-5`; C `--model claude-sonnet-5`; B2 and B3 `--model claude-sonnet-5-5 --reply-thinking-off`; C2 and C3 `--model claude-sonnet-5 --reply-thinking-off`. The invented counts are the check's catches in drafts, not judged final replies. Review: BAKEOFF-SONNET55-REVIEW-2026-11-16.md (pass with fixes, all taken).
