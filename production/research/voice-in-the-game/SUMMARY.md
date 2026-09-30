# Putting the voice inside the game

Research, 30 September 2026, by a separate research helper.

(The helper returned its text; the session that asked for it saved it here after checking its figures from the project's own records: the game at 3.5 GB and Nano at 2.1 GB of the card, and Nano's 1.3 seconds of work per second of speech beside the game, measured 24 September; the watermark decision D50; and the game's existing sound queue. It added the processor figure in "Cost on this PC" from the same measurement.)

Today the voice is a separate Python program; a copy for a friend's PC must carry it inside.

## How shipped games do it, in order

1. **Convert** the model into portable files (ONNX, or GGUF for the llama.cpp family) in three or four pieces: one reads the sentence, one makes each next sound token with a running memory, one turns tokens into sound. Each character's voice is prepared in advance.
2. **Shrink** the weights (half size or 8-bit), then re-check behaviour, including when it stops talking.
3. **Run** the pieces with a small inference library inside the game, on its own thread, streaming short pieces of sound to the speaker (LEDGER already has that last part).
4. **Pack** library and model files with the game; test on a machine with nothing installed.

Epic's speech-to-face model runs this way inside Unreal 5.8, as do commercial Unreal voice plugins. NVIDIA packaged Chatterbox Turbo for games by January 2026, for its own cards and under its own licence. Local voices in released games are still rare: two of NVIDIA's showcase games used cloud voices, and PUBG's AI teammate speaks locally only on NVIDIA cards.

## What fits LEDGER

Keep today's voice, Chatterbox Nano, and run it on the processor inside the game, preferably through the ONNX runtime Unreal already ships for the mouth solver. Why: the card is shared with the street, and beside the game Nano on the card fell behind speech (1.3 seconds of work per second of speech, measured 24 September); the Python card library it uses was last updated in 2024; and this route adds nothing to install. If the processor is too slow, fall back to the card with August's technique of keeping the model's memory there; that needs the runtime called directly.

## Cost on this PC

- Processor: nothing on the card; under about 1.5 GB of ordinary memory (my estimate). Speed unmeasured: the maker claims three times faster than speech on 8 cores; Pocket TTS, similar in size, runs nine times faster than speech on an 8-core Ryzen in its C++ port (its author's figure). What this PC has measured is Nano in Python on the processor: about 1.9 seconds of work per second of speech on 24 September, slower than speech. That includes Python's own overhead, so a converted model should do better, but by how much is unmeasured; it is the first thing to time.
- Card: Nano used 2.1 GB beside the game (measured 24 September).

## Licences

- Chatterbox (all sizes) and its Perth watermarker: MIT, weights included; our rule keeps the watermark.
- ONNX Runtime: MIT; already inside Unreal.
- Pocket TTS: code MIT, weights CC BY 4.0 (credit; clone only with consent).
- Kokoro: Apache 2.0; its usual pronunciation helper is GPL.
- Piper: old engine MIT, current GPL, same helper; each voice licensed separately.
- NVIDIA's Chatterbox package: NVIDIA model licence, not on our list.

## What to do, in order

1. Look inside the installed engine: its runtime version, and whether game code can use it directly (half a day).
2. Convert Nano into three pieces plus saved voices, following Resemble's Turbo layout; shrink to 8-bit; rerun August's ten-seed stop test (3–4 days).
3. Convert the watermarker; apply it per sentence. If impossible, a question for Jafar (1–3 days).
4. Time processor against card with the street running (1 day).
5. Build the voice into the game on its own thread, feeding the existing sound queue (2–3 days).
6. Package; play thirty minutes in a fresh Windows account; the game lists every file it loaded and fails if any lies outside its folder (1–2 days).

About two working weeks (my estimate): bigger than the list item looks, so Jafar should hear it. If he picks a paid voice, this becomes the offline fallback.

## Not verified

Blocked: Hugging Face, NVIDIA and Microsoft documentation, Unreal's forums; their figures are search summaries. Unmeasured: Nano's converted speed here; direct use of Unreal's runtime; the watermarker's conversion; DirectML's redistribution terms; the Piper VCTK voice's licence.
