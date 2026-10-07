# The claim check's successor to Haiku 4.5 (7 October 2026)

The talk task of 7 October, item 3, second check: the claim check runs on Claude
Haiku 4.5, which will retire; run it on its likely successors on the existing
labelled details, and say which keeps its accuracy and speed.

## What was found first (read 7 October, the API's own model list and pages)

- **Haiku 4.5**: active, retirement "not sooner than October 15, 2026", with at
  least 60 days' notice promised (the deprecations page). No notice has come yet.
- **Haiku 5.5** (`claude-haiku-5-5`): released 7 October, the same day. $0.10 in
  and $0.50 out per million tokens for prompts up to 100,000 tokens, a tenth of
  Haiku 4.5's $1 and $5; adaptive thinking, on unless told otherwise (default
  effort medium); thinking can be turned off. Retirement not before 7 October 2027.
- **Sonnet 5.5**: $2 and $10, twice Haiku 4.5; thinking can only be turned off
  as `between_tools`.
- So the likely successors are Haiku 5.5, as the same line, and Sonnet 5.5, the
  step up. Haiku 5.5 was tried four ways, since thinking is what costs speed.

## How it was measured

- **On LEDGER's key, over the API, as the game calls it** (ClaimBench
  `successors --key`, every call timed, every run logged in
  production/playtest/talk-runs.jsonl). The same prompts as the live check
  (`ClaimCheck.RequestVerify`, `ClaimCheck.CheckAsync`), only the model and its
  thinking changed.
- **The labelled details**: the held-out half of the detail bench of 30 September
  (F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl), 127 details
  labelled apart by two labellers and a third, blind to any check: 85 true
  (stated or implied), 42 invented (added or contradicted). Each put to the
  check's second look, as the live check does: how many true details it
  refuses, how many invented ones it lets through.
- **The whole check**: 30 labelled replies of the 28 September bench's held half,
  15 invented and 15 honest, through the list and its second looks.
- One run each, so a difference of one or two items is within a run's noise.

## What came back

| model and thinking | true details refused | invented details passed | a second look, median / slowest tenth | whole check: invented replies caught | honest replies flagged | whole check, median / slowest tenth |
|---|---|---|---|---|---|---|
| **Haiku 4.5, today** | 23/85 (27%) | 3/42 (7%) | 0.84 / 0.92 s | 15/15 | 4/15 | 2.22 / 3.01 s |
| Haiku 5.5, thinking off | 22/85 (26%) | 6/42 (14%) | 0.70 / 1.01 s | 13/15 | 7/15 | 1.85 / 2.42 s |
| Haiku 5.5, thinking at low effort | 22/85 (26%) | 0/42 (0%) | 0.99 / 1.87 s | 14/15 | 3/15 | 3.98 / 6.91 s |
| Haiku 5.5, thinking at its default | 26/85 (31%) | 0/42 (0%) | 1.05 / 2.11 s | 13/15 | 3/15 | 5.42 / 7.41 s |
| **Haiku 5.5, the list without thinking, the second looks at low effort** | 23/85 (27%) | 1/42 (2%) | 0.97 / 1.99 s | 14/15 | 4/15 | 2.13 / 3.87 s |
| Sonnet 5.5, thinking off, low effort (a sample: 40 details, 10 replies) | 12/27 (44%) | 1/13 (8%) | 1.60 / 3.58 s | 5/5 | 1/5 | 3.39 / 5.81 s |

**The other half, to double the sample** (the tuning half: 111 details, 61 true
and 50 invented, and 30 replies of the 28 September bench's tuning half), Haiku
4.5 against the split only:

| model and thinking | true details refused | invented details passed | a second look, median / slowest tenth | whole check: invented replies caught | honest replies flagged | whole check, median / slowest tenth |
|---|---|---|---|---|---|---|
| **Haiku 4.5, today** | 32/61 (52%) | 2/50 (4%) | 0.84 / 0.92 s | 15/15 | 6/14 (one unchecked) | 2.38 / 3.21 s |
| **Haiku 5.5, the split** | 23/61 (38%) | 2/50 (4%) | 0.95 / 1.83 s | 15/15 | 6/15 | 2.15 / 3.12 s |

**Both halves together:** Haiku 4.5 refused 55 of 146 true details (38%) and
passed 5 of 92 invented (5%); the split refused 46 (32%) and passed 3 (3%). On
the whole check Haiku 4.5 caught 30 of 30 invented replies and flagged 10 of 29
honest ones; the split caught 29 of 30 and flagged 10 of 30, its median the
faster on both halves, its slowest tenth from even to 0.9 s slower.

Cost of the measuring: US$1.57 of the task's three dollars (five runs, logged).

## What it says

- **Haiku 5.5 with thinking off is the fast one and the weak one:** a fifth faster
  than Haiku 4.5, but it let twice as many invented details through and flagged
  almost half the honest replies.
- **Thinking buys the accuracy back and costs the speed:** at low effort it passed
  no invented detail at all, but the whole check took nearly twice as long, which
  the voice's path cannot spare (the check sets the floor of the first sound,
  production/research/invented-claims/CHECK-FLOOR-PROPOSAL-2026-10-07.md).
- **The split keeps both:** the list (which runs on every line, and on the first
  sentence) without thinking, the second looks (which run only on what the list
  flagged) at low effort. Over both halves it refused fewer true details than
  Haiku 4.5 (32% against 38%) and passed fewer invented ones (3 of 92 against 5),
  missed one invented reply of thirty that Haiku 4.5 caught, ran the whole check a
  little faster at the median and up to 0.9 s slower in its slowest tenth, at a
  tenth of the price.
- **Sonnet 5.5 is no successor here:** dearer, slower, and on its sample it
  refused nearly half the true details.

## Recommendation

**Haiku 5.5 as the split**: the list with `thinking: disabled`, the second looks
with `thinking: adaptive` and effort low, when Haiku 4.5's retirement notice comes
(or sooner, for the price). Before switching: the talk program's `CheckerModel` set apart from the
small-talk writer (`Models.Ambient` is both today); the request carrying the
thinking (`LlmRequest.Thinking`, added on branch `talk`), and the relay letting
`thinking` and `output_config` through (it strips every other field today); the
first sentence's check timed on the real path, since its tail matters most.
