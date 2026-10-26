# Sheila and Ron on Pocket (26 October 2026)

His page of 26 October (the listening test, production/approvals/2026-10-26): Pocket passed his ear for Sheila (lena) and Ron (rocco); their prepared lines move with them, so neither sounds like two people; Darren (sam) keeps the cast voice on the card (Pocket's Darren drifted American). Order ledger item `o26-pocket-switch`.

## What was made

- **The voice program** (tools/voice-live/voice-server.py): Pocket is a third engine beside Nano and Sopro. production/specs/voice-engines.json gives lena and rocco to it. The program starts Pocket's own server (tools/voice-live/pocket-server.py, on its own Python, F:/LedgerTools/pocket-tts/env) beside it, forwards those characters' lines and passes on its streamed pieces; each engine prepares only its own voices before it says it is ready (pocket-server.py --who). If Pocket's Python is missing, Nano speaks for everyone, as before.
- **The settings are the listening test's own:** pocket-server.py with its defaults, learning each voice from the same cast clip, so the voice in the game is the one he passed.
- **The thinking sounds** (content/voice/acks/lena and rocco, "Let me think." and "Well, now."), made again in Pocket. Off in play since his ruling of 7 October (-PreparedAck brings them back), kept matching in case they return. The first takes of "Let me think." read Scottish to the accent check (0.97 and 0.91; the old card takes read English), so six more takes each were made and an English one kept (Sheila take 4, Ron take 1). Each is evened to the old ones' loudness (about -18.6 dB while speaking; Pocket's raw takes were 6 to 15 dB quieter), its lead silence cut, then tidied (tidy_acks.py: tail trimmed and faded; no holes). Checked after: all four PASS england (0.99 to 1.00, American 0.00); Whisper heard each word right.
- **The played game's voice folder was a month old.** The packaged game's Voice folder links to F:/LedgerTools/voice-portable, whose copy of the voice program dated from 1 October: the played game had never run the voice work since then, and would never have read the new engines spec. The program and spec are copied in now (the old copy kept as tools/voice-live-2026-10-01), and the build copies them from its own commit every time (.github/workflows/ledger-probe-unreal.yml, "the voice program kept current").
- **The size guard** (tools/git-size-guard.py) refused the four sounds though the build packages that folder from git; the folder joins its list of game inputs (200 KB a file), with two new self-test lines.

## Measured

**The voice program alone** (the packaged game's own Python and folder, three lines, the card idle): Sheila's and Ron's first sound 0.10 to 0.11 s; Darren's 1.70 s.

**In the packaged game** (F:/LedgerTools/played-game, last night's build, its refreshed voice folder; -AskScript=6, the stand-in talk, so the model's own time is not in it; F:/LedgerTools/latency/pocket-switch-2026-10-26/ask-packaged.json):

| Line | Who | First sound | Whole answer heard |
|---|---|---|---|
| 1 | Darren (card) | 2.75 s | 6.58 s |
| 2 | Sheila (Pocket) | 0.22 s | 3.53 s |
| 3 | Ron (Pocket) | 0.18 s | 2.99 s |
| 4 | Darren (card) | 2.52 s | 10.37 s |
| 5 | Sheila (Pocket) | 0.21 s | 6.20 s |
| 6 | Ron (Pocket) | 0.20 s | 6.61 s |

On 21 October, everyone on the card, the same script gave Sheila 2.16 and 3.07 s and Ron 2.37 and 3.13 s to first sound (F:/LedgerTools/latency/opener-2026-10-21/ask-card.json, the editor's game). Sheila and Ron now answer about ten times sooner; Darren is unchanged.

**Loudness:** live Pocket pieces sit within about 3 dB of Darren's (per-piece speaking level -22 to -27 dB against his -23), close enough not to act on.

## Not done, and open

- The frame stalls the voice caused on the card (set aside 25 October, VOICE-ON-CARD-TRACE-2026-10-25.md) are now Darren's alone; not measured again here.
- A friend's PC: Pocket's Python lives only on this PC (F:), so a copy of the game elsewhere would speak all three on Nano. Making Pocket portable belongs with a friends' build, not in this week's order.
- An unattended editor run of -AskScript needs -TalkHelper= pointing at a built talk program (the repo's own build of it is from 23 September); the packaged game carries its own and is the better place to measure anyway.

## Darren too (26 October, evening)

His page's pick A (VCTK p286, a Newcastle man of 23; production/casting/darren-milner/voice-2026-10-26/REVIEW.md) is Darren's voice in Pocket: his reference in game-design/pocket-voices/sam.wav (out of git; F:/LedgerTools/game-inputs holds it and the build copies it into the played game's voice folder), voice-engines.json gives sam to Pocket, pocket-server.py reads that folder before the cast clips; his two thinking sounds remade from the new voice and gated (England, every word, no holes). The same packaged test (F:/LedgerTools/latency/pocket-switch-2026-10-26/ask-packaged-all-pocket.json):

| Line | Who | First sound | Whole answer heard |
|---|---|---|---|
| 1 | Darren (Pocket) | 0.46 s | 3.84 s |
| 2 | Sheila | 0.24 s | 3.60 s |
| 3 | Ron | 0.19 s | 3.03 s |
| 4 | Darren | 0.21 s | 6.34 s |
| 5 | Sheila | 0.23 s | 6.24 s |
| 6 | Ron | 0.21 s | 6.60 s |

Darren on the card that afternoon: 2.75 and 2.52 s. Nothing of the cast's speech now runs on the graphics card (the card's voice stays loaded for the town's other speakers).
