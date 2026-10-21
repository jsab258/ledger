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

## The game's frame time while Pocket speaks (packaged 00f81b1, the voice speaking without a break)

tools/p1-packaged.ps1 -Voice pocket (tools/voice-live/voice_load.py --pocket): the cast's lines one after another through Pocket on half the processor's threads, 1008 s of speech made in 400 s (0.40 of real time: flat out, far busier than a conversation), with nothing else running.

| run | median | slowest 1% | worst | over 33.3 | the card voice instead (P1, same build) |
|---|---|---|---|---|---|
| standing, day | 13.95 | 21.88 | 28.0 | 0 | 15.19 / 26.52 / 35.63 / 2 |
| walking | 13.17 | 33.95 | 174.7 | 3 | 14.38 / 26.00 / 30.34 / 0 |

Off the card the game runs faster on the median, but walking it stalls: 92.4 and 43.3 ms frames with the game's own threads short (game 10 and 6 ms, render 9 and 11, card 10 and 15), the processor busy elsewhere, and a 174.7 ms first frame. A first run overlapped this PC's checks and is not counted (worst 129 to 150 ms). Frames: F:/LedgerTools/tmp/p1-packaged/packaged-*-pocket2-00f81b1.csv.

## The opener, as an experiment (his order: "an instant in-character opener (a look and a word in under half a second) while the real line streams sentence by sentence")

The game's own prepared openers ("hmm, well now", "let me think", each with its own face animation and glance; off since his ruling of 7 October, -PreparedAck brings them back) played at the line's sending, in the editor's game: -AskScript=6 asks Darren, Sheila and Ron six lines down the player's own path (the stand-in talk, so the model's time is not in it), and the game itself records, from the line sent, the opener's start, the answer's first words and first sound, and the whole answer heard out (CrimeProbe.cpp AskScriptTick, its "opener" and "wholeAnswer" added today). Records: F:/LedgerTools/latency/opener-2026-10-21/ask-pocket.json and ask-card.json.

| voice | the opener's word and glance | the answer's first sound | the whole answer | the opener |
|---|---|---|---|---|
| Pocket, on the processor | 0.00 s (the same frame) | median 0.23 s (0.20 to 0.38) | median 4.99 s (3.06 to 6.53) | cut off by the answer every time, 0.2 to 0.3 s in, mid-word |
| the cast voice on the card | 0.00 s | median 2.81 s (2.16 to 3.25) | median 9.00 s (6.63 to 13.14) | heard whole (1.0 to 1.3 s), then a second of silence before the answer |

- With Pocket the voice is already as quick as the opener, so the opener only clips into the answer; with the card voice it fills the first second of the wait but not the second and a half after it. Neither changes the 2-second bar, which stays until he rules (the order's words); with no prepared openings (his 7 October ruling) the card voice's first sound is 2.8 s here, Pocket's 0.23 s, both before the talk model's own time.

## What this does and does not show

- The voice's own share is about a tenth of a second: on the processor it is not the bottleneck. The 2-second bar is then the talk model's time to its first checked sentence plus this.
- The whole answer with the real talk model cannot be measured yet: the times above are the stand-in's replies spoken; the only model test asked for (Gemini Flash) waits on his key in F:\LedgerTools\keys\google.txt (empty).
- Not measured here: the accent: Pocket was set aside on 26 and 28 September because its copies of the cast drifted American or away from the approved voices (DECISIONS.md). Its speed does not change that.
