# Live talk's two cost levers, measured (6 November 2026)

n02-9-talk-cost-levers, under his yes of 6 November (the waiting list's named items when the order's items wait). Reference: none found (COST-PER-HOUR-2026-11-02.md).

## Questions, written before any paid call

1. Replies on Haiku 5.5 against Haiku 4.5, on the same held newcomer questions through the game's engine and check: first sentence's time (median, under 2.0 s, worst), fall-backs and refusals, cost per line?
2. Do the replies keep voice and character? (One fresh reader, blind to the arm.)
3. How much of the briefing can be cached at all? The order of today's briefing puts what changes (memories, time, the bearing facts) in the middle, and a cache only reads an unchanged start.
4. Caching: over several lines of one talk, cache reads in each answer, cost per line, and does moving the stable part first change the replies?

## The method

ClaimBench `firsts --set held --early` (20 held questions, Lena, Rocco, Sam: 60 lines an arm), one line at a time, the game's switches (rules, plain fall-back, ladder and its judge, the check on Haiku 5.5, the fast checker). Beside the game: a screen, never the bar. Nothing ships without the night's build, the walk and a run inside the game. Capped in code (task talk-levers-2026-11-06, $5, within the day's ceiling), logged in production/api-spend.jsonl. Spent US$4.10, 14 runs, 3,377 calls; raw: F:/LedgerTools/latency/levers-2026-11-06. "Heard" is the first sentence's hand-over plus 0.2 s of voice (slow_turns.py's rule), the whole turn when it was held back.

## Measured (read 6 November)

| Arm | Runs | Median heard, s, by run | Under 2 s of 60 | Fall-backs of 60 | US$ a run |
|---|---|---|---|---|---|
| Shipped: replies Haiku 4.5, second draft Sonnet 5 | a, a2, a3 | 1.52, 1.57, 1.39 | 37, 34, 35 | 1, 1, 2 | 0.54, 0.58, 0.57 |
| Replies Haiku 5.5, thinking off, second draft Haiku 5.5 | b, b2 | 2.06, 1.95 | 27, 31 | 7, 8 | 0.16, 0.15 |
| Replies Haiku 5.5, thinking on | b3 | 3.55 | 2 | 2 | 0.10 |
| Replies Haiku 5.5, second draft Sonnet 5 | d | 2.36 | 23 | 5 | 0.42 |
| Briefing moved and cached, check not cached | c (head under the minimum), f | 1.92, 1.97 | 32, 31 | 4, 7 | 0.45, 0.23 |
| Briefing moved and cached, check cached | c2 (head under the minimum), e, e2 | 1.14, 1.84, 1.77 | 40, 33, 37 | 2, 2, 2 | 0.43, 0.23, 0.21 |

1. **Haiku 5.5 for replies: not kept.** A third of the cost, but fall-backs 7 and 8 of 60 against 1 or 2, and later first speech. Its thinking left on eats the 300-token allowance (replies of about three words). With Sonnet's second draft it costs about 0.42 and still falls back 5 times. Why the first drafts are refused more often: unread beyond the sample (it says more, 17 words against 15).
2. **The voice:** one fresh reader, blind, a3 against e2: 14 pairs better for cached, 11 for shipped, 35 level; plainly broken replies on both sides, one reasoning aloud in shipped (a3), one reading as an instruction in cached (e2) and one borderline in cached (TALK-LEVERS-BLIND-READ-2026-11-06.md). The shipped arms show the same kinds; this read does not separate them.
3. **What can be cached:** Haiku 4.5 caches only from 4,096 tokens. The first head (card, street, rules, card's facts, 16,000 characters) stayed under it: c read only Sonnet's and paid little. With the people's facts too, 19,176 characters, 4,881 tokens: written once, read on each later line.
4. **Cached with the check cached: kept (e, e2).** Cost down 61%, no time lost: three runs each pooled, median 1.48 s shipped, 1.19 s cached, under 2 s 59% and 61%, a cached line slower than a shipped one 47% of the time; the same arm's medians range 1.14 to 1.84, so only a large change would show. Fall-backs 2 of 60 against 1 or 2. Arm f, the same briefing with the check not cached, fell back 7 times and c 4; why is unexplained, so the two switches ship together.

**The hour.** At 15 replies: shipped $0.14, cached at best $0.055, since these runs ask one person 20 lines inside the cache's five minutes. A talk of four lines (worked out, not measured): about $0.077. A single line pays the write and costs a little more than today. Against the target of $0.05: still over in ordinary play.

## Not reached

Inside the packaged game: not run. It reaches the game on its first night's build, and a paid in-game run must confirm the time and the fall-backs, a second run settling it. A real hour's mix of talks. Whether the cache's minimum holds for characters with fewer facts: the head's size is not checked per card.

## Inside the packaged game (7 November, build e998e06, the same hour, the bar's own measure)

Each run: 30 lines from the held newcomer questions, -AskSet firsts-held.txt -AskNear, as run F; live on LEDGER's key, all three Pocket voices ready, no one walked away, nothing refused by the cap. Raw: F:/LedgerTools/latency/askreal-2026-11-07h, i, j, k. Questions, written before running: is the cache read inside the game; does the time or the fall-backs worsen; what does it cost.

| Run | Talk | Median first sound | Under 2.0 s | 4 s or more | Worst | Fall-backs | Timed out | US$ (price card) | Cache read / written |
|---|---|---|---|---|---|---|---|---|---|
| F (4 Nov, build 6c808a1) | not cached | 2.02 | 14 of 30 | 7 | 8.22 | 0 | 2 | 0.366 | none |
| J | not cached | 2.42 | 14 of 30 | 8 | 8.22 | 0 | 5 | 0.364 | none |
| H | cached | 2.04 | 14 of 30 | 6 | 8.21 | 1 | 2 | 0.295 | 360,789 / 127,866 |
| I | cached | 1.67 | 20 of 30 | 5 | 8.26 | 2 | 1 | 0.259 | 305,319 / 108,872 |
| K | cached | 1.58 | 21 of 30 | 4 | 8.22 | 0 | 1 | 0.248 | 348,626 / 114,702 |

Three cached runs pooled, 90 lines: median 1.78 s, 55 under 2.0 s, 15 at 4 s or more. Order: H, I, J, K; only J and K alternate, one run each, so the spread between runs (1.58 to 2.04 on the same talk) is as large as most of the gain.

- **The cache works inside the game** and costs about 27% less: mean US$0.267 against 0.365, so an hour of 15 replies about US$0.13 against 0.18 by these runs, more than the beside-the-game $0.077 worked out for a four-line talk, since these runs pass between three people. Not yet a real hour's mix.
- **Time did not worsen;** it read better in two of three runs. Why a saving in cost should save time was not read; fewer timed-out lines (4 in 90 against 7 in 60) may be part of it. The 8-second tail stays in every run.
- **Fall-backs:** 3 of 113 replies cached against 0 of 76 not. Too few to tell apart, and the nightly bench, 60 first questions, read 2 of 60 on both the night before the cache and the night with it. Listed, watched in the nightly bench.
- **The bar:** this was a cost lever, no try at the bar. Run F's miss stands as measured; these runs go to the exit's reviewer as raw numbers, who judges.

