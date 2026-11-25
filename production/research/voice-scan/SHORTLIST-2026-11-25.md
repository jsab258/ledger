# n23-4 voice-model scan: the shortlist (25 Nov 2026, 04:05)

Built on: SCAN-READING-2026-11-25.md (first-pass reading, Sonnet reader, all figures and links there); QUESTIONS-2026-11-25.md; voice-latency/POCKET-SWITCH-2026-10-26.md.

## What the reading says for us
- Pocket: our install is already its newest release (pocket_tts 4.0.1, 21 Oct; checked in F:/LedgerTools/pocket-tts). Nothing newer to try. Its smaller English models (18M, 7M, 2M) came with 4.0.0; whether our voices use the new default model is a free check on the next voice run.
- No model in the window is shown keeping a northern, Scottish or Irish accent from a reference clip. The accent question stays open for every candidate; the accent checker screens it, his ear decides.
- No candidate publishes a first-audio figure on a Windows PC with a consumer card; every speed must be measured here.

## Shortlist (licence by the allowlist's principles: Apache 2.0 and MIT as Kokoro and Chatterbox already are)
1. ZONOS3-Mini (Zyphra, 11-12 Nov; weights Apache 2.0, code MIT; about 100M active, CPU build; clones from 5-60 s; streams; vendor first audio 80 ms H100, under 150 ms on a laptop chip). The only one with cloning, CPU running and a size near Pocket's. Lead candidate.
2. Phonon 31M (Gradium, about 22 Oct; Apache 2.0; 64.5 MB). Very fast on a CPU benchmark (28 ms against Pocket's 165 ms, hardware not stated), but cloning with the open weights is unconfirmed: tried only if its card shows cloning.
## Out, with the reason
- Fish Audio Drama 3: revenue cap, required branding and the hosted-service clause fall outside the allowlist's principles; 35B, a data-centre card.
- Ming-3.0-tts, Audio8-TTS-Realistic-Air: GPU-sized beside the game at High (the card budget is held); Ming "tiny" is 7.9B.
- Dia2: release year unverified; Breeze TTS 2: non-commercial weights; MOSS-TTS: nothing new.

## The trial (next)
The same 12 cast lines as latency.py --voice game, ZONOS3-Mini first, cloned from the cast's existing reference clips (lena, rocco, sam), on the processor beside the packaged game: first audio median and worst, the accent checker as a screen, one fresh reviewer, then a listening item on his page only if it beats Pocket on time without losing the accent. Downloading its weights is held for his yes in chat (the session's download rule); installed only into F:/LedgerTools.
