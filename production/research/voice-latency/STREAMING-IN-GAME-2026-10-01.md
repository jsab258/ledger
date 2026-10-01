# The voice in pieces, tried in the game (1 October 2026)

The builder's measurements, following FAST-FIRST-AUDIO-2026-10-01.md step 2. Every number below was measured on this PC (Ryzen 5 5600X, RX 6700); "in the game" means beside the packaged game in the street, the AI tester talking.

## What was built

tools/voice-live/nano_stream.py: Nano's token loop yielding each token as it is made (the same operations, so the same seed gives the same tokens: checked on six lines), and CosyVoice 2's chunked decode (each pass decodes all tokens so far with the last three held as lookahead, the vocoder runs on the new frames with 8 frames and the source signal carried over, 160 ms faded into the next piece). Two fixes the installed package needed:

- Its `finalize=False` trims the encoding but not its padding mask, so it fails on shape (530 against 536); `flow_unfinished` trims both.
- The decoder's noise drawn from the token loop's random sequence changed the following tokens; it is forked, and the loop has its own generator when the decoder runs on another thread.

The server's streamed path (LEDGER_VOICE_STREAM=1) sends pieces "joined" onto the playing sound, the game's existing way for Sopro, holding the first piece until the rates measured so far say the rest will follow with no gap.

## Quality, on the idle PC (six of Rocco's lines)

- The pieces' spectrogram against the whole take's, same tokens and noise: 0.3 to 0.8% of its range on average, at most 1.5 to 3.9% near a join. Two whole takes of the same tokens with different noise differ by 2.6 to 3.0% on average. So the pieces are closer to the whole take than two takes are to each other.
- Decoding a pass as if the sentence ended there, and dropping its edge, was worse (5 to 8% near a join): not used.
- Clicks: CosyVoice's Hamming crossfade stops at 8% at both ends and left a small step in quiet stretches; a fade from exactly 0 to 1 replaced it. A click score (energy above 7 kHz in 4 ms against the 40 ms around it) at the joins was within the range of ordinary speech elsewhere in each line. Not yet heard by a person.

## Speed

| | First piece | Whole reply |
|---|---|---|
| Idle PC, decoder in line with the loop | 0.75 to 0.79 s | about real time |
| Idle PC, decoder on its own thread | 0.98 to 1.01 s (warm), no gaps | |
| In the game, decoder on its own thread | 2.2 and 4.1 s | 10 to 12 s for 3 to 4 s of speech, 3 gaps up to 0.9 s |
| In the game, today's whole sentences (for comparison) | 2.98 s median for 1.62 s of speech | |

Each pass decodes the voice's reference (about 6 s, 300 frames) again with the new tokens. That costs 0.45 s on the idle PC and 1.5 s in the game, against 0.6 s of speech a pass, so in the game the pieces cannot keep up. **Streaming does not fit this PC beside the game; it stays off (whole sentences remain the default).**

## Why the game slows the voice

- The token loop: 57 tokens a second on the idle PC (on the card), 25 to 29 beside the game; on the processor, 38 to 41 idle and 19 to 24 beside the game (3 and 6 threads). Both slow about twice over.
- Not the card's load: capping the game at 60 or 30 frames a second changed nothing (3.09 and 2.99 s against 2.98).
- Not process priority: "above normal" for the voice changed nothing (2.95 s).
- Not the per-token checks with the card: checking for the stop token every 4, 8 or 16 tokens instead of every token gave the same 55 to 60 tokens a second idle.
- Not Windows' timer: a 1 ms timer for the process changed nothing (16.0 ms a token either way).

The first reading was that the cost is Python issuing the loop's several hundred small operations a token, which the game's threads halve, so a compiled loop (one call a token) would fix it. The next section tested that, and it was wrong.

## Then the compiled step, and the card's load (the same night)

tools/voice-live/nano_step_graph.py writes Nano's one-token step out plainly from the model's own modules (its scores agree with the library's to 0.00002 at ten positions) and exports it to ONNX (406 MB, F:/LedgerTools/voice-graphs/nano). ONNX Runtime 1.24.4 with DirectML was already in the voice's environment.

| Token loop | Idle PC | Beside the game |
|---|---|---|
| Today's (PyTorch on the card) | 57 a second | 24 to 29 |
| Today's on the processor, 3 / 6 threads | 38 / 41 | 19 to 21 / 21 to 24 |
| Compiled step, ONNX Runtime on the card | 92 | 16.5 to 16.9 |
| Compiled step, ONNX Runtime on the processor (3 threads) | 38 to 43 | not measured |

On the card the compiled step's scores differ from the library's by up to 0.009 (the card's own rounding; on the processor 0.00001).

The packaged game here runs at Highest at 3440 by 1440 with every quality group at 3 (its saved settings; about 26 ms of card time a frame, by the title's own measure of 30 September). Drawing it at half resolution (r.ScreenPercentage=50, confirmed in its log) left the voice's work for a short line at 3.12 s median (2.98 at full size).

**Reading:** not the card's load, not the frame rate, not process priority, not Python's per-step work. Beside the running game both the processor and the card give the voice about half their idle speed, and the compiled step, with almost no work for the processor, slows most (5.5 times): a step that waits for the card once a token waits about 60 ms. The voice's turns on the card come late while the game holds it, whatever its work weighs. The one lead not tried: a card queue of high priority for the voice, which needs the voice inside the game (the "proper conversion", about two weeks by the earlier note), not a Python program beside it. Unproven; to be researched before it is relied on.

**Status:** set aside past the two-tries rule (in-game attempts after the research: streaming, the compiled step; and the cheap tests: two frame caps, priority, half resolution). Today's voice stays: whole sentences, flow on the card, 2.98 s of work for a short line beside the game.
