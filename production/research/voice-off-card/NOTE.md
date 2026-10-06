# The voice off the card: the method, researched first (6 October 2026)

For proof P2 (production/research/pre-production/3-PROOFS.md, "P2. The voice off the card, timed beside the game"). The question: can Chatterbox Nano leave the graphics card, or get cheaper, with its own share of the delay at most 1.0 s median beside the game? Approach A is fixed by the plan: the 8-bit decoder on the processor. Approach B is chosen here from the evidence.

Written by a bounded helper session on 6 October. The web reading was done by a separate research helper the same morning (about 35 pages; its sources are listed below). Everything under "Checked on this PC" was run here today.

## Checked on this PC, 6 October

- **Processor.** AMD Ryzen 5 5600X: 6 cores and 12 threads, AVX2 and FMA, no AVX-512 and no VNNI (Zen 3). 32 GB of memory.
- **Libraries.** The voice's environment (C:/LedgerTools/chatterbox-nano/env-dml) has:
  - ONNX Runtime 1.24.4, the DirectML build, which carries the processor provider too (installed under F:/LedgerTools/voice-env-export);
  - onnx 1.22.0;
  - torch 2.4.1 (processor build), with torch-directml for the card;
  - transformers 5.2.0.
  - `onnxruntime.quantization` (quantize_dynamic, quant_pre_process) imports and runs.
- **The portable voice the game ships** (F:/LedgerTools/voice-portable) has no ONNX Runtime in it today. Either approach would need it added (about 30 MB) before a friend's PC could use it.
- **Nano's decoder works on the voice's whole reference every line.** For each voice the reference is 250 sound tokens (10 s), so the flow handles 500 frames of reference plus the new line's frames (72 for a typical first sentence).
  - Measured on the processor (torch, 4 threads): the encoder takes 0.25 s; each of the two meanflow steps of the estimator takes 0.65 s.
  - The same step on the new line's 72 frames alone takes 0.10 s.
  - **About 87% of the decoder's work is the reference, not the words.** Its attention runs over all frames in both directions, so that work cannot be kept from line to line without changing the sound.
- **The token model's fixed prefix can be kept, exactly.** Every line starts with the same speaker vector and reference tokens (281 to 376 positions), and the model reads left to right.
  - Keeping that prefix's keys and values once per voice changes the scores by at most 6e-6.
  - It saves about 0.25 s a line on the processor.
  - Both approaches use it.
- **The quantizer has a fault on this graph.** ONNX Runtime's `quantize_dynamic` turns each Gemm into a MatMul by transposing its weight in place, "assuming B is not used by any other node" (onnxruntime/quantization/onnx_model.py, read here).
  - Nano's two meanflow steps share their weights, so the graph would not load afterwards.
  - Each Gemm now gets its own copy of the weight first (tools/voice-live/off_card.py --quantize).
  - Its pre-processing pass (`quant_pre_process`) hit the same fault, so it is not used. The docs advise it but do not require it.

## How 8-bit is done with ONNX Runtime on a processor

- **Dynamic against static.** Dynamic quantisation stores the weights in 8 bits and works out each activation's scale while the model runs. Static quantisation calibrates the scales on sample data beforehand. The docs advise dynamic for transformers and static for convolutional networks [1].
- **What gets quantised.** By default `quantize_dynamic` takes Conv, MatMul, Attention, LSTM, Gather, Transpose and EmbedLayerNormalization; Gemm is not on the list [2][3].
- **On AVX2 without VNNI (this processor):**
  - ORT's U8S8 path can saturate. The docs: "on AVX2 and AVX512 machines, you will generally need to enable reduce-range as well if per-channel is enabled" [1]. Used here: per-channel QInt8 weights with reduce_range.
  - The docs warn that 8-bit is often no faster on such hardware [1]. A Ryzen 3700X went only from 38.05 to 35.08 ms, against 31.46 to 19.76 ms on a VNNI part [4].
- **Convolutions stay at 32 bits.** Dynamic convolutions (ConvInteger) are never fused [5]. A HiFi-GAN vocoder ran about ten times slower quantised that way [6], and a Piper voice nearly four times slower [7]. The usual workaround is `op_types_to_quantize=["MatMul"]` [5], used here.
- **Version risk.** One report has dynamic quantisation of transformer layers silently stopping between ORT 1.20.1 and 1.21 [8]. Here the flow graph gained 445 MatMulInteger nodes, so it did quantise.

## Quality: what has been reported

- **Chatterbox's own decoder (S3Gen) is the most quantisation-sensitive part of the model** [24].
  - It lost 2.17 UTMOS at 4-bit weights.
  - With 8-bit S3Gen and a 4-bit token model the loss was only 0.02.
  - Per-tensor scaling "even at 8 bits" could wreck quality.
- **Supertonic.** Full dynamic int8 raised the word error rate from 0.028 to 1.11 and ran at twice the 32-bit time. MatMul-only int8 with convolutions at 32 bits kept quality [24].
- **Elsewhere.** Int8 vocoders have been reported going faint (Supertonic-3, 0.46 times the level [25]) and gaining steady tones (Kokoro via sherpa-onnx [26]).
- **CosyVoice ports** (Nano's decoder family) keep the flow at bf16, fp16 or fp32 and quantise only the language model [28][29][30].
- **Chatterbox exports.**
  - Resemble's Turbo export ships a q8 decoder (327 MB against 769 MB fp32) but publishes no quality or processor-speed figures [13][14]. Users found q8 "way slower than Q4 on CPU" and speech "gibberish" below q8 [15].
  - KitsuMate's Nano export keeps the decoder's convolutions at 32 bits with 8-bit MatMuls, and checked only Whisper transcripts on six sentences, never by ear [19].
- **On this PC, before any listening** (off_card.py --check, same tokens and noise):
  - The 32-bit flow graph matches the library to 0.0001% of the spectrogram's range.
  - The 8-bit flow moves it by 4.1% on average and 17.5% at most.
  - For scale, two takes of the same tokens with different noise differ by 2.6 to 3.0% (STREAMING-IN-GAME-2026-10-01.md). **So the 8-bit flow changes the sound by more than a fresh take does.**
  - The 8-bit token step (2 October) moves the scores by up to 1.9, enough to change which tokens are drawn.

## Threads, beside a game

- ONNX Runtime uses one thread per physical core by default (6 here), and its threads spin while they wait [9].
- Spinning off: `session.intra_op.allow_spinning` = 0. opentrack, which runs beside games, saw processor use fall from 434% to 36% with no change in output [10]. rf-detr found an idle spinning session made other work about 29 times slower [11].
- Affinity: `session.intra_op_thread_affinities` exists, but the docs say "normally best to not set" it [9].
- **Used here:** 4 threads with spinning off. The voice's own process is kept to logical processors 8 to 11 (Windows SetProcessAffinityMask, set by the voice itself). Nothing is done to the game. The 2 October evidence held the game off those processors too; that needs a change to the game and is not tested here.

## The second approach, chosen from the evidence

Candidates, against what was found:

1. **Stream the decoder in pieces** (CosyVoice 2's method [31][32]; Martlet streamed Chatterbox Turbo to 350–400 ms first audio, on an RTX 5080 [33]).
   - Each piece still decodes the whole 10 s reference. On this processor the first piece's flow alone takes 0.78 s at 8 bits (0.98 s at 32 bits) with 15 new tokens, so prefill plus the first 12 tokens plus the flow plus the vocoder comes to about 1.4 s.
   - That is idle, before the game takes any of the processor. Cannot pass. Not chosen.
2. **Keep the decoder on the card, quantised.**
   - The card's trouble beside the game is when the voice gets its turns and the memory pushed out of the card (EVIDENCE-2026-10-01.md), not the arithmetic.
   - The flow on the card took 1.62 s beside the game (1 October, voice_profile.py).
   - DirectML is in "sustained engineering" [34]. Not chosen.
3. **Fewer threads.** It frees the game's processor time but makes the voice slower. Measured instead through A's frame times.
4. **A lighter decoder: read less of the reference.** The profile above says the reference is 87% of the decoder's work.
   - Idle, the flow for 15 new tokens takes 0.36 s at 32 bits with the reference's last 100 tokens (4 s), against 0.98 s with all 250.
   - It changes what the decoder hears of the voice, so it must be judged by ear and by the likeness check.
   - **Chosen as B:** the whole voice on the processor, the decoder at full precision (no 8-bit loss) reading the last 4 s of the reference, the token model's 8-bit step and kept prefix as in A.
5. **One meanflow step instead of two.** Resemble's card says the decoder was distilled "from 10 steps to just one" [22], which would halve the estimator. But today's voice runs two, and the code's own path uses two. Left for a later test; it changes the sound too.

**Streaming does not rescue either approach.** Even idle, the processor's work runs at about real time or slower, as the measurements in RESULTS-2026-10-06.md show. A first piece played early would run out before the next one arrives, so a first sound with no gap after it comes no sooner than the whole sentence.

## Sources (read 6 October 2026 unless marked)

1. ONNX Runtime, "Quantize ONNX models", https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html, undated, READ.
2. ONNX Runtime source, quantization/registry.py, https://raw.githubusercontent.com/microsoft/onnxruntime/main/onnxruntime/python/tools/quantization/registry.py, READ.
3. ONNX Runtime source, quantization/quantize.py (same folder), READ; and the installed 1.24.4 copy of onnx_model.py, read on this PC.
4. microsoft/onnxruntime issue 6695, https://github.com/microsoft/onnxruntime/issues/6695, 15 Feb 2021, READ.
5. onnxsim pull 1207, https://github.com/onnxsim/onnxsim/pull/1207, 6 Sep 2026, READ.
6. microsoft/onnxruntime issue 12854, https://github.com/microsoft/onnxruntime/issues/12854, 5 Sep 2022, READ.
7. LoveLogicAI/piper-en_US-amy-medium-int8, https://huggingface.co/LoveLogicAI/piper-en_US-amy-medium-int8, 4 Oct 2026, READ.
8. microsoft/onnxruntime issue 24459, https://github.com/microsoft/onnxruntime/issues/24459, 17 Apr 2025, READ.
9. ONNX Runtime, "Thread management", https://onnxruntime.ai/docs/performance/tune-performance/threading.html, undated, READ.
10. opentrack pull 2223, https://github.com/opentrack/opentrack/pull/2223, 23 Sep 2026, READ.
11. roboflow/rf-detr pull 1456, https://github.com/roboflow/rf-detr/pull/1456, 14 Sep 2026, READ.
12. dseelinger/d47 issue 753, https://github.com/dseelinger/d47/issues/753, 1 Oct 2026, READ.
13. ResembleAI/chatterbox-turbo-ONNX, https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX, about Dec 2025, READ.
14. The same, file list, https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX/tree/main/onnx, READ.
15. The same, discussion 5, https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX/discussions/5, 24–27 Dec 2025, READ.
16. The same, discussion 7, https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX/discussions/7, Jan 2026, READ.
17. Wikipedia, "Zen 4", https://en.wikipedia.org/wiki/Zen_4, undated, READ (Zen 3 has no AVX-512 VNNI).
18. onnx-community/chatterbox-ONNX, https://huggingface.co/onnx-community/chatterbox-ONNX, about 2025, READ.
19. KitsuMate/chatterbox-nano-v2-onnx, https://huggingface.co/KitsuMate/chatterbox-nano-v2-onnx, undated, READ.
20. owensong/chatterbox-nano-ONNX, https://huggingface.co/owensong/chatterbox-nano-ONNX, undated, READ.
21. Resemble AI, "Chatterbox Nano and Flash", https://www.resemble.ai/resources/chatterbox-nano-and-flash-speed-at-the-edge-throughput-at-scale, 6 Jul 2026, READ.
22. ResembleAI/chatterbox-nano, https://huggingface.co/ResembleAI/chatterbox-nano, undated, READ.
23. 0xShug0/audio.cpp pull 394, https://github.com/0xShug0/audio.cpp/pull/394, 4 Sep 2026, READ.
24. arXiv 2609.28974 (post-training quantisation of TTS), https://arxiv.org/abs/2609.28974, 24 Sep 2026, READ.
25. askurios8/supertonic-3-int8, https://huggingface.co/askurios8/supertonic-3-int8, undated, READ.
26. elboaf/YAAH issue 298, https://github.com/elboaf/YAAH/issues/298, 4 Oct 2026, READ.
27. k2-fsa/sherpa-onnx issue 3754, https://github.com/k2-fsa/sherpa-onnx/issues/3754, 11 Jul 2026, READ.
28. soniqo, CosyVoice guide, https://soniqo.audio/guides/cosyvoice, undated, READ.
29. Lourdle/CosyVoice2-0.5B_ONNX, https://huggingface.co/Lourdle/CosyVoice2-0.5B_ONNX, undated, READ.
30. ayousanz/cosy-voice3-onnx, https://huggingface.co/ayousanz/cosy-voice3-onnx, undated, READ.
31. CosyVoice source, cosyvoice/cli/model.py, https://raw.githubusercontent.com/FunAudioLLM/CosyVoice/main/cosyvoice/cli/model.py, READ.
32. CosyVoice 2 paper, https://arxiv.org/abs/2412.10117, 13 Dec 2024, READ (abstract only; its "150 ms first packet" was seen in a search snippet only).
33. throndir2/Martlet pull 321, https://github.com/throndir2/Martlet/pull/321, 3 Oct 2026, READ.
34. ONNX Runtime, "DirectML Execution Provider", https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html, undated, READ.
35. NVIDIA, Chatterbox TTS programming guide, https://docs.nvidia.com/ace-for-games/chatterbox-tts/programming-guide-tts-chatterbox.html, 8 Jul 2026, READ.

Unreached or snippet only (not evidence): the sherpa-onnx docs, FluidAudio PR 925, YAAH 74, nishkmg/chatterbox-nano-api (a page with no details). No published first-audio figure for Chatterbox Turbo or Nano on a desktop x86 processor was found.
