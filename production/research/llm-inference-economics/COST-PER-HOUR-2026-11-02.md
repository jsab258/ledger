# Live talk's cost per hour of play, measured again (2 November 2026)

His order of 2 November, n02-7-3-talk-cost-hour: "Live talk's cost per hour of play measured again (15 replies an hour), with what would bring it down." Reference: none found. The earlier measure: SUMMARY.md in this folder (September: $0.36 to $1.08 an hour at twenty conversations; target $0.05).

## Questions

1. What does a reply cost in the packaged game today, by model, on real token counts?
2. What is that per hour at 15 replies?
3. What would bring it down, ranked, with what each needs before it is used?

## Measured

Source: the talk program's own end line (its CostTracker, real input and output tokens per model, priced at the game's own price card, ledger/Assets/Scripts/Core/LlmClient.cs Models.Cost) in the in-game speech runs of this morning, the packaged game, the cast's real talk (production/research/voice-latency/IN-GAME-2026-11-02.md; transcripts F:/LedgerTools/latency/askreal-2026-11-02c and -d, read 2 November).

| Run | Lines | Calls | Haiku 4.5 (replies) | Haiku 5.5 (the claim check) | Sonnet 5 (core replies) | Total | Per line |
|---|---|---|---|---|---|---|---|
| C (try 2) | 30 | 74 | 30 calls, 187,957 in / 1,045 out: $0.193 | 44 calls, 226,040 / 4,954: $0.025 | none | $0.218 | $0.0073 |
| D (try 2 with the escalation, as built) | 30 | 86 | 25 calls, 155,466 / 1,100: $0.161 | 58 calls, 268,603 / 6,329: $0.030 | 3 calls, 23,761 / 298: $0.051 | $0.241 | $0.0080 |

- **Per hour at 15 replies (run D, as built): about $0.12.** Run C, without the escalation: $0.11. The budget counter's own figure is higher ($0.327 for run D); why is unexplained (the speech-bench skill's review, 2 November: the code settles each reserve to the tokens used, so reserving does not explain it; unverified which figure the bill follows).
- Against the target of $0.05 an hour: about 2.4 times over (September's figure was 7 to 20 times).
- **Small talk only:** the runs' lines are small talk (the speech-bench review, 2 November), so nearly every reply went to Haiku 4.5. Real questions go to Sonnet 5 at twice its price per token; an hour with real questions costs more, measured with the next run of real questions.
- **Input is almost all of it:** a reply call on Haiku 4.5 sends about 6,200 tokens and gets back about 44; the briefing (rules and character card) is the bulk and is sent again with every call. Nothing is cached: the client sets no cache marker (LlmClient.cs).

## What would bring it down, ranked

1. **Cache the briefing (the free win, still not taken).** The stable part of every call (rules, the character card) marked for caching; cache reads cost a tenth of input. Minimums (the API reference, read 2 November): Haiku 4.5 caches from 4,096 tokens, Sonnet 5 from 1,024, Haiku 5.5 from 512. At about 6,200 tokens a call, all three now qualify (September's 1,900-token briefing did not on Haiku). Estimate (unverified): input cost down about 70% over a talk of several lines within the cache's five minutes; per hour about $0.04 to $0.05. Needs: one marker in the client on the stable system block, and a measured run (cache_read_input_tokens in each answer).
2. **Replies on Haiku 5.5 instead of Haiku 4.5.** A tenth of the price ($0.10 / $0.50 against $1 / $5 per million tokens; its tokenizer counts about 30% more). The claim check already moved to Haiku 5.5 on 8 October after keeping Haiku 4.5's accuracy at the same median speed. Estimate (unverified): the replies' share from $0.16 to about $0.02 a run of 30; per hour about $0.05 alone, about $0.02 with caching. Needs: the replies' own check before switching (voice and character kept, the Long Pause's 2 s bar kept), as the check's switch had.
3. **Fewer calls per reply** (2.9 now: written, cleared, drafted, checked). Smaller and riskier: each call guards something.

Together, 1 and 2 would bring an hour under the $0.05 target (estimate). Both are new work, so they go on the next order's waiting list with this note; neither is switched on in the running week.

## Not reached

- A run with caching on (nothing changed in the game).
- How the hour splits across the cast's and the street's lines over a real hour of play (the runs are 30 asked lines, not an hour).
