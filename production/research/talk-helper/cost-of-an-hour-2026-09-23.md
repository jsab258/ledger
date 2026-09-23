# What an hour of talk costs on the paid model, 23 September (night)

Measured, not estimated: 24 real calls through `ledger/TalkHelper`, the slice's
conversation run beside the game - the real ConversationEngine, the canon
cards, the output guard - to the slice's three talkers at noon on the fish
market's pavement, eight lines each, one continuing conversation per person
(`cost-session-lines-2026-09-23.json` in, `cost-session-2026-09-23.json`
out). Prices are the game's own table (ledger/Assets/Scripts/Core/LlmClient.cs):
Haiku 4.5 $1/$5 per million tokens in/out for the ambient tier (Rocco, Sam),
Sonnet 5 $3/$15 for the core tier (Lena).

| | calls | tokens in | tokens out | US$ |
|---|---|---|---|---|
| Rocco and Sam (ambient, Haiku 4.5) | 16 | 30,364 | 1,119 | 0.036 |
| Lena (core, Sonnet 5) | 8 | 19,447 | 386 | 0.064 |
| **the conversation** | **24** | **49,811** | **1,505** | **0.100** |
| the router's read of each typed line (paid test, 42 lines, $0.045) | 24 | | | 0.026 |
| **all of it** | | | | **0.126, about half a US cent a line** |

Replies came back in 1.7 s at the median, 3.2 s at worst; none timed out.

## An hour of play

How much a player types in an hour is not known yet; three honest guesses:

| a player who says | lines an hour | US$ an hour |
|---|---|---|
| a little | 30 | 0.16 |
| a fair amount | 60 | 0.31 |
| a lot | 120 | 0.63 |

A core-tier character (Sonnet) costs about three times an ambient one per
line (0.8 US cents against 0.25 before the router). And a line costs more
the longer a conversation runs, because every call carries the conversation
so far.

## What it means for a released game

- A 30-hour playthrough at "a fair amount" is about **US$9 per player**, paid
  by whoever pays the API bill: at a US$30 price that is roughly a third of
  the price before the platform's cut, spent again on every player, with no
  ceiling if someone talks for 100 hours.
- **The input dominates**: 50,000 tokens in against 1,500 out. Every call
  resends the character's card and the conversation. The client uses no prompt
  caching today; caching the fixed part of each prompt is the obvious first
  saving, and the card and instructions are most of it.
- The router's share is small (about a fifth), and the research session is
  testing local models for exactly that job.
- The recorded, pre-voiced street talk (barks, remarks, overheard gossip) costs
  nothing to run; only what the player types does.
