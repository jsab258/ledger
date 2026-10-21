# Pocket TTS on the processor, timed on the game's voice path (21 October 2026)

His order of 21 October, item 8: "Kyutai Pocket TTS on the CPU. ... Report first sound and full answer times; the 2-second bar stays until he rules."

## How

- Pocket TTS (Kyutai; code MIT, weights CC BY 4.0, kyutai/pocket-tts, Kyutai's terms accepted on this PC on 26 September), reinstalled in F:\LedgerTools\pocket-tts\env (Python 3.12, torch 2.14.1 CPU), its weights cached in F:\LedgerTools\hf.
- tools/voice-live/latency.py --lines 12 --prewarm --early --voice pocket: the game's own two helpers driven as the game drives them, the talk helper as its free stand-in (--fake: no model is called in development, his ruling of 29 September), the voice server tools/voice-live/pocket-server.py on half the processor's threads, the three cast voices learned first. The game was not running (the processor shared with nothing).
- Record: F:\LedgerTools\latency\pocket-2026-10-21.json.

## Measured (seconds after the player's line is sent; 12 lines)

| stage | median | slowest | fastest |
|---|---|---|---|
| first sound made by the voice | 0.13 | 0.26 | 0.11 |
| first sound heard (plus one frame and the sound card's buffer) | 0.16 | 0.30 | 0.15 |
| the first sentence's sound whole | 0.65 | 0.76 | 0.37 |

The voice server is ready 14 s after starting (16.6 s the first time, its weights read from disk).

## What this does and does not show

- The voice's own share is about a tenth of a second: on the processor it is not the bottleneck. The 2-second bar is then the talk model's time to its first checked sentence plus this.
- The full answer's time cannot be measured yet: it is the talk model's whole reply, and the only model test asked for (Gemini Flash) waits on his key in F:\LedgerTools\keys\google.txt (empty); the stand-in's replies are one short sentence.
- Not measured here: the game's frame time while Pocket speaks on the processor (on 2 October the card's voice took four of the twelve logical processors; P2's second measure), and the accent: Pocket was set aside on 26 and 28 September because its copies of the cast drifted American or away from the approved voices (DECISIONS.md). Its speed does not change that.
