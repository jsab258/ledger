# What fills a fresh session's start, and the first cuts (advisor 97, part 1; 11 November 2026)

Measured on the 11:22 session (log bfe1b4b5), from the app's context reading at 11:23 (after the lean start's reads) and the log's tool results. Prices: tools/token_audit.py's table (Opus 5.5: cache write 1 h US$8 per million tokens, cache read US$0.20).

## Before
| Part | Tokens | Source |
|---|---|---|
| System prompt | 4,960 | context reading |
| Built-in tools' descriptions | 23,606 | context reading |
| Connector (MCP) tools | 14,123 | context reading |
| Skills list | 9,982 | context reading |
| CLAUDE.md and memory | 8,780 | context reading |
| Fixed part, before any read | 61,451 | sum |
| HANDOVER.md | about 2,900 (10,360 characters) | log |
| RULINGS.md and NOW.md | about 8,100 (29,326 characters) | log |
| Page listings: advisor, advisor-acks, verdicts (out_dir lists of 103, 93 and 60 files) | about 9,900 (35,517 characters) | log |
| ArtifactData's loaded description | not measured | |
| Messages at the reading, all of the above with the session's own text | 54,037 | context reading |
| Whole context at 11:23 | 119,901 | context reading |

Characters to tokens at about 3.6 per token: an estimate, not a count.

What a start's tokens cost: written to the cache once (about US$0.96 for 120,000 tokens) and re-read on every later step (US$0.024 a step for the same 120,000). So each 10,000 tokens cut saves about US$0.08 at the start and US$0.002 a step, about US$0.60 over a 300-step session (step count from this week's sessions: not measured here; advisor 96's audit gives it).

## Cuts made today
1. **Page listings to filtered queries** (about 9,900 tokens): the advisor read becomes two queries (the newest ack, then messages after it) and verdicts a query after the last page read. Written into the handover's standing ways, which every session reads. The task file's own wording could not be changed: the edit was refused by the permission check, so that is his to do (or to allow). After: not measured until the next start; expected under 1,000 tokens.
2. **Answered page items archived**: items.json from 172 KB to 18 KB (40 done items to 12; archive.json holds the rest, never read at the start). The start already filtered items.json, so the saving there is small; the page's own publish carries the smaller file.

## Not cut, and why
- RULINGS.md (4,900-word cap, his to change) and the handover (1,800-word cap) are read whole by his 4 Nov lean-start ruling.
- The skills list (9,982 tokens) and connector tools (14,123): switching off what is never used. Whether it can be done for this project alone is being checked before it goes on his page (advisor 97, part 2b).
