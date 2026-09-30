# Getting the voice's first sound out fast (research note, 1 October 2026)

A separate research helper, about thirty minutes: the web, plus the installed Nano package read in place. It builds on NOTE-2026-09-30.md, voice-in-the-game/ and live-speech-latency.md without repeating them.

## A correction to the brief

The card is an **AMD Radeon RX 6700**, with a Ryzen 5 5600X (read from Windows today; also card-timing-2026-09-24.md), not NVIDIA. CUDA, TensorRT, CUDA graphs and NVIDIA's in-game scheduler do not apply. PyTorch's AMD route on Windows supports only RX 9000 and R9000 cards ([ROCm 10.0.0 matrix, 25 Aug 2026](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html)). The card routes left are DirectML and Vulkan.

## 1. The method, end to end

- **Stream inside the sentence.** Today the voice makes a whole sentence before any sound. Streaming makes speech tokens (25 per second of audio) and decodes them in chunks:
  - a small first chunk, then bigger ones ([mstar PR #303, 22–30 Sep 2026](https://github.com/mstar-project/mstar/pull/303));
  - each chunk decoded with earlier tokens as left context, that context's audio cut off, and a short fade at the join ([chatterbox-streaming](https://github.com/davidbrowne17/chatterbox-streaming), undated: chunk 25 tokens, context 50, fade 20 ms);
  - 25-token chunks with 25 tokens of context and crossfades ([vllm-omni PR #3004, 13 Jul 2026](https://github.com/vllm-project/vllm-omni/pull/3004), unmerged).
- **Cutting the text into pieces only moves the wait.** The first sound still waits for the whole first piece, as LEDGER's does today. NVIDIA's own Chatterbox plugin works this way (40 words a piece). On an RTX 4090 running a 3D scene it takes about 0.97 to 1.2 s to Turbo's first audio ([NVIDIA, updated 8 Jul 2026](https://docs.nvidia.com/ace-for-games/chatterbox-tts/programming-guide-tts-chatterbox.html)).
- **Nano's decoder was designed to stream.** It comes from CosyVoice 2, whose paper reports streaming as virtually lossless, with the first packet at 150 ms ([arXiv 2412.10117, 13 Dec 2024](https://arxiv.org/abs/2412.10117)). The installed package has the hooks: a causal decoder with a 3-token lookahead, `finalize=False` for chunks that are not the last, and a vocoder cache carried across chunks.
- **The work done per token often costs more than the maths.**
  - On an RTX A6000 under Windows, Turbo's stock token loop ran at about 22 tokens a second, below the 25 needed, because Python issued hundreds of small card operations per token.
  - One step recorded as a CUDA graph reached about 385, with matching logits ([devnen issue #175, 23 Sep 2026](https://github.com/devnen/Chatterbox-TTS-Server/issues/175)).
  - The fix is CUDA-only; the diagnosis carries over.
- **Exported runtimes and 8-bit weights.**
  - Resemble's Turbo ONNX ships fp32, fp16, q8 and q4, MIT, with no streaming guidance ([Dec 2025](https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX)).
  - Two community Nano exports, both MIT and non-streaming: [KitsuMate](https://huggingface.co/KitsuMate/chatterbox-nano-v2-onnx) (undated; a "CPU speed" layout, mostly 8-bit; timed on a phone only) and [owensong](https://huggingface.co/owensong/chatterbox-nano-ONNX) (undated; its authors say it is not for low-latency use).
  - The nearest processor evidence is another small TTS model, ZeroTTS (not Chatterbox), on a Ryzen 5 5600 under Windows 11 ([issue #8, 16 Sep 2026](https://github.com/zeroweight-ai/ZeroTTS/issues/8); [PR #6, 16–17 Sep 2026](https://github.com/zeroweight-ai/ZeroTTS/pull/6)): 8-bit was 2.7 times faster than 32-bit, 4 threads was best, and the first chunk came at about 150 ms instead of 230. The 8-bit version shifted pauses and length slightly.
- **Beside other work, cap the threads.** ONNX Runtime uses one thread per physical core by default, and its "spinning" threads burn processor time while they wait ([threading docs](https://onnxruntime.ai/docs/performance/tune-performance/threading.html), undated).
- **Nano elsewhere against here.**
  - An RTX 5070 Ti with a Ryzen 5 5600, a sentence at a time: first audio 466 ms median, at 0.15 of real time ([kadirnar PR #111, 25 Sep 2026](https://github.com/kadirnar/voice-agent-next/pull/111)).
  - Here: about 1.0 s of work per second of speech on the idle card (24 Sep), about six times slower.
  - My reading, unmeasured: the gap is mostly the stack (the Python library on DirectML, one token at a time), not the model.

## 2. Chatterbox and its variants

- **No official streaming for Turbo or Nano.** Neither [the repository](https://github.com/resemble-ai/chatterbox) (read today) nor [Nano's card](https://huggingface.co/ResembleAI/chatterbox-nano) (undated) mentions streaming or ONNX. Resemble's 75 ms for Turbo is for "a GPU", unnamed ([Turbo page](https://www.resemble.ai/learn/models/chatterbox-turbo), undated).
- **chatterbox-streaming** covers the original 0.5 B model only, not Nano (MIT): 0.472 s to the first chunk on an RTX 4090 under Linux. It watermarks each chunk and publishes no quality comparison.
- **Seams are the known risk.** People streaming Turbo's ONNX decoder in 10- to 100-token chunks heard clicks at the joins. There was no clean fix; keeping more audio buffered ahead helped ([discussion #18, Dec 2025 to Jan 2026](https://huggingface.co/ResembleAI/chatterbox-turbo/discussions/18)).
- **No public Nano streaming fork exists.** The hooks are already in the installed decoder, so this is a change to our voice server, not a new engine.
- **Streaming need not change the voice.** Rhythm and intonation live in the tokens, and streaming leaves the token loop alone. With the same seed on the same device, a streamed take has the same tokens as a whole one; only the joins can differ. This is my reading of the installed code.

## 3. Processor, card, or split

- The one report of a cloned voice beside a running game chose the processor (d47, in the 30 September note). NVIDIA's card-side scheduling has no AMD equivalent found.
- LEDGER is already split: the token loop runs on the card through DirectML, the decoder and watermark on the processor. Streaming lets the two run at the same time.
- Risks on this PC:
  - DirectML: two sessions at once crashed in August, and its Python library was last released in September 2024.
  - The slowest frames went from 12.9 to 16.0 ms with Nano on the card (24 Sep).
  - On the processor, the voice's threads compete with Unreal's.
- Beside the game, Nano does 1.3 s of work per second of speech, so plain streaming would stall mid-sentence. August's head-start rule avoids that: start playing when the work left is less than the audio left.

## 4. Settings that carry the liveliness

- Nano ignores exaggeration, CFG and min_p: the installed code warns and drops them, and [NVIDIA's guide](https://docs.nvidia.com/nvigi-sdk/1.7.0/docs/ProgrammingGuideTTSChatterbox.html) (14 Aug 2026) says the same of Turbo.
- Its liveliness therefore comes from two things:
  - the reference clip: up to 15 s for the token model and 10 s for the decoder;
  - the sampler: temperature 0.8, top-k 1000, top-p 0.95, repetition penalty 1.2, in that order.
- Anything faster that changes these changes the voice: greedy decoding, another order, a lower temperature, a shorter clip.
- So can lower precision: 8-bit shifted pauses (ZeroTTS), and fp16 broke the stop decision here in August.
- Streaming and loop tidying change none of these settings.

## Not verified

- How today's 3.7 s splits between queue, token loop, decoder and watermark: nothing has been profiled.
- Any Nano streaming figure, or Nano ONNX speed on a desktop processor.
- Whether Nano's joins are audible. Whether Resemble trained the decoder for chunks is unknown: the streaming line in its code is commented out.
- The watermark's cost per piece: no figure was found.

## What to try first on this PC (all free)

1. **Profile the voice's share, idle and beside the game (half a day).** It gains nothing by itself, but it decides steps 2 to 4. Done when there is a table of milliseconds per token, decoder, watermark and queue wait.
2. **Stream Nano in today's voice server (1–2 days).**
   - How: chunks of 12–15, then 25, then 50 tokens, each with 25–50 tokens of context; `finalize=False` and the vocoder cache; 20 ms fades; the watermark on each piece; the head-start rule; the game's joined pieces.
   - Gain (my estimate): the voice's share from about 3.7 s to 1.0–1.6 s beside the game. With `--pending`, heard ≈ max(2.0, 0.9 + 1.3) + 0.1 ≈ 2.3 s median.
   - Done when: the first piece is ready within 1.5 s beside the game; the tokens match a whole take with the same seed; and a fresh listener cannot find the joins blind. Then one blind A/B for Jafar.
3. **Slim the token loop's work per step (1 day).**
   - How: drop the per-step sync check and the progress bar; keep the repetition history as a running tensor; keep the sampler order exact.
   - Gain: perhaps 1.2 to 2 times on the loop (my guess).
   - Done when: the tokens are identical for a fixed seed, at fewer milliseconds each.
4. **Nano on the processor, ONNX Runtime at 8-bit (3–5 days; voice-in-the-game step 2).**
   - How: KitsuMate's export first for a speed reading; 3 threads, no spinning.
   - Gain (my estimate): first audio in 0.3–0.8 s, and the card freed.
   - Done when: first audio comes under 0.8 s beside the game; the slowest 1% of frames stays within 1 ms; the ten-seed stop sweep is clean; and a blind A/B cannot tell it apart.

Not recommended: a shorter reference clip, a lower temperature, or another engine. Each changes the approved voice.
