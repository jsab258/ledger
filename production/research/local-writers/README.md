# Who writes the talk: the local line-writing blind test (L01), 25 September

Writing the lines is about 70 percent of what live talk costs
(production/research/runtime-ai-business). Jafar made a local writer a
priority: the best local writers that fit what the card has left write the
same lines as the paid model, shown to him without saying which is which.

## What was run

- **The writers.** The paid model the game uses for each character (the core
  model for Sheila, the ambient model for Ron and Darren), and the two local
  models already on this PC that fit the card beside the street and the voice
  (about 3.7 GB left, measured 24 September): Qwen3.5-4B and Ministral 3 3B,
  both Q4, both Apache-2.0, on llama.cpp over Vulkan, thinking off.
- **The moments.** Twelve: Sheila, Ron and Darren, four each (an opener, the
  window, a lure the content rule or canon must survive, pressure), with the
  memories and suspicion the live encounter gives them.
- **The same prompt for every writer.** The game's own system prompt
  (ConversationEngine.BuildSystemPrompt, the real cards with canon's names),
  one player line, the game's own validator after. `ledger/LineTest`.

## Where things are

- `lines.json`: each moment and its three answers under shuffled letters. The
  approval page shows only this.
- `letters.json` and `key.json`: which writer each letter was, the raw text
  before the validator, the time, and whether the validator changed it.
  **Not for Jafar before he has judged.**

## Measured (not the judgement, which is his)

| writer | median per line | slowest | content-rule hits | lines the validator changed |
|---|---|---|---|---|
| paid | 1.4 s | 2.6 s | 0 | 4 of 12 |
| Qwen3.5-4B | 2.7 s | 3.4 s | 0 | 0 of 12 |
| Ministral 3 3B | 3.3 s | 4.7 s | 0 | 12 of 12 |

Times are on an idle card, with no game running beside it; with the street
and the voice on the card the local writers would be slower. "Changed" is
mostly the validator taking out dashes and stage directions; a writer it has
to rescue on every line is worse than its final text shows. Neither local
model broke the content rule on these twelve; twelve is too few to say it
never would.

The claim check (ClaimCheck.cs) was not applied to any writer here, so
inventions show as written: this compares writers, not the guard.
