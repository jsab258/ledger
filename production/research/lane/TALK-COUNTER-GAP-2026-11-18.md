# The talk counter's gap: $0.327 against $0.241 (18 November 2026)

## Question

Run D (2 November, 30 lines): $0.241 by the talk program's price estimate, $0.327 by its budget counter (api-spend.jsonl line 8). Why, and which does the bill follow?

## The counters' rules

- One price card for both (LlmClient.cs 96-113): Sonnet 5 $2/$10, Haiku 4.5 $1/$5, Haiku 5.5 $0.10/$0.50 per million in/out; no caching in run D. Prices cannot explain the gap.
- Estimate (CostTracker.cs 14-44): only what the conversation code records; unknown models skipped (38).
- Counter (BudgetedClient.cs): reserves a worst case (82-96), settles to the reply's tokens (104-115): success is never counted twice. A stopped stream settles at what it used (155-159); a request cancelled before the reply begins is charged its guessed prompt, characters / 4 x 1.1 + 50 (162-166, 61-66); one cancelled after the reply began but before its first event settles at nothing; a throwing call or broken stream keeps its worst case (117-123, 152-166).

## Where the estimate stops recording

- Abandoned turns: at 8 seconds (14 once a first sentence is heard) the talk program cancels the turn with a brush-off (TalkHelper/Program.cs 1134-1176), as on any failure (1199-1205). Cancelled drafts record nothing (ConversationEngine.cs 1932-1937, 1955; outer catch 1973-1981), nor do checks in flight (1999-2000). The counter counts them; whether the provider bills them is likely but unconfirmed (no billing page read).
- Broken streams: the estimate records only the retry; the counter keeps the broken one's worst case too (1939-1959).
- Stopped early looks, uncounted by design (ClaimCheck.cs 545-549).

## Arithmetic

Run D's estimate reproduced: $0.1610 + $0.0300 + $0.0505 = $0.2415.

| Run | Counter | Estimate | Gap | Lines | Replies | Gap per line without reply |
|---|---|---|---|---|---|---|
| B (Sonnet 5) | 0.4092 | 0.3293 | 0.0799 | 20 | 15 | 0.0160 |
| C (Haiku 4.5) | 0.2757 | 0.2183 | 0.0574 | 30 | 23 | 0.0082 |
| D (Haiku 4.5, 3 escalated) | 0.3274 | 0.2415 | 0.0859 | 30 | 23 | 0.0123 |
| E (10 Sonnet, 15 Haiku) | 0.3756 | 0.3367 | 0.0389 | 30 | 25 | 0.0078 |
| F (Haiku 4.5) | 0.3999 | 0.3664 | 0.0335 | 30 | 28 | 0.0168 |

Sources: api-spend.jsonl lines 6-9, 13; IN-GAME-2026-11-02.md. One draft's input: Sonnet 5 about 7,920 tokens ($0.0158, run D's three calls); Haiku 4.5 about 6,220 ($0.0062, plus checks of $0.001 to $0.002). B, C and D each match one abandoned draft per such line. Run D records two brush-offs; its other five lines without a reply are not identified (transcript not reached), and the column assumes each abandoned a draft, by timeout or walk-away (Program.cs 1148-1164). E fits one Haiku draft per cut reply; F's two timeouts cost twice that each: more calls per timeout, or another cause (unverified).

## Explanation, ranked

1. Turns abandoned by timeout, walk-away or failure: counted by the counter, never by the estimate. Fits B to E within about a cent, F at twice. Unconfirmed.
2. Broken streams: $0.008 (Haiku) to $0.019 (Sonnet) extra each on the counter.
3. Prompts cancelled before an answer: the guess runs about 3 % high for replies, about a fifth low for Haiku 5.5 checks; under a cent either way.
4. Latent, not in run D: suggestions are recorded under the dated model name (Suggest.cs 213), priced at nothing by the estimate.

## Which the bill follows

Most likely the counter, if abandoned turns are billed; it may run slightly high. If so, $0.12 an hour is low by a quarter to a third: about $0.16 on run D's ratio.

## Recommendation

- Check, no edit: at the next monthly API credit reading the sessions already make ("Last credit month US$10.80 of US$200 used"), compare the counter's api-spend.jsonl total for that month with the provider's figure. If the provider's is closer to the counter's, quote the counter.
- For the main session's next talk item: log each request's id and usage reply, and mark abandoned turns.

## Not verified

- Run D's transcript (F:/LedgerTools/latency/askreal-2026-11-02d): not reachable; brush-offs in C unknown; B had at least one (IN-GAME-2026-11-02.md line 34).
- Whether the provider bills abandoned turns or a stream stopped before its first event.
- Prices: the card's comment says read 16 November 2026; search snippets of 18 November agree on Haiku 5.5 (techenclave.com); no page read in full.
- Code read is today's, not run D's build.
