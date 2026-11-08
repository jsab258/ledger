# Opus against Sonnet, a blind replay (8 November 2026)

His yes of 8 Nov 07:34 (sonnet-blind-replay-2026-11-07; the advisor's message 26). Five recent finished items, each redone twice from its own starting commit, once on Opus 5.5 and once on Sonnet 5.5, each run in its own light copy on F (F:/LedgerTools/replay-2026-11-08, briefs in BRIEFS.md, copies `git clone --shared` with a sparse checkout, 27 to 74 MB each). Same brief word for word; no Unreal, no clicks. Judged by one fresh Opus reviewer (final-reviewer) with the runs labelled X and Y at random and model names stripped, against the accepted work and the source itself (judge/verdict.json; the key was kept outside the judge's reach).

## Result

| Item | Kind | Opus | Sonnet | Judge |
|---|---|---|---|---|
| gate-fix | code fix with tests | 9, usable | 3, not usable | Opus far better: Sonnet's detector misses all 32 real WAIT runs (real logs are ~690 KB, over its 256 KB limit, and contain the prompt's words "REHEARSAL GO"); its selftest passed only on made-up logs |
| quay-diag | diagnosis from code and logs | 8 | 7 | equal, leaning Opus: both find the end wall; Opus alone found the landing trigger reaching Mickey's door (a real fault, fixed today); Sonnet got Ron's 7 Nov position wrong but caught a stale -5.0 in quay-cast.json |
| lumen-source | engine-source research | 9 | 7 | Opus better: both right on the three answers; Opus adds that the 30 cm per-mesh floor is off at the shipped High level, so 20 cm applies |
| cover-review | review of pictures | 7 (FAIL) | 6 (PASS) | equal: Sonnet's PASS matches the accepted verdict but is thin (missed the resize, no crops); Opus looked properly, but failed it on two narrow points |
| cover-tread | small asset step | done | done | not judged: with Sonnet below the bar on three of four, the fifth could not change the outcome |

Cost (the runs' own token counts; list prices, Sonnet half of Opus per token): Opus 676,308 tokens, 1,248 s; Sonnet 545,312 tokens, 642 s. Sonnet's runs cost about 40% of Opus's and took half the time. The whole replay, runs, judge and this session from 08:26 to 08:56: about US$17.60 at list prices, one point of the week (72% to 73%), inside the 3% cap.

## What it decides

- The advisor's bar (Sonnet matches on at least 4 of 5 at clearly lower cost) is not met: Sonnet matched on one or two. Tuesday's real day on Sonnet does not run (n02-9-session-model).
- The split it shows, for Monday's order: Sonnet keeps what his 3 Nov ruling already gives it (extraction, first-pass reading, routine imports, first-round small reviews: the cover review was its equal). Code that must work on real data, diagnosis and engine research stay on Opus: Sonnet's gate fix was plausible, self-tested and wrong, the most expensive kind of fault.
- Unverified: one sample per kind; a second replay could move the review and diagnosis rows either way.

## A lesson for every code fix

Both gate fixes passed their own selftests; only running the detector on the real logs showed one of them catches nothing. A fix to a tool that reads real files is checked on those real files, read-only, before it counts.
