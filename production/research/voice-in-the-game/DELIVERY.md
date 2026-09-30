# Putting the voice inside the game: the detail

Research, 30 September 2026, by a separate research helper. Companion to SUMMARY.md.

(The helper returned its text; the session that asked for it saved it here unchanged except for this note. That session checked the project figures against the records: the card timing of 24 September (production/research/nano-listening-test/card-timing-2026-09-24.md and the archived FINDINGS: game 3.5 GB, Nano 2.1 GB, 1.3 s of work per second of speech beside the game, about 1.9 on the processor in Python), D50 in production/archive/DECISIONS-to-2026-09-24.md, and the USoundWaveProcedural queue in CrimeProbe.cpp.)

Question: how do shipped games run speech models inside the game, from start to finish? And what does that mean for Chatterbox Nano (today's voice), the other Chatterbox sizes, Pocket TTS, Kokoro and Piper? The hardware is this PC: RX 6700 with 10 GB, Ryzen 5 5600X, UE 5.8.2.

Web sources are W-numbers and project records are P-numbers; both lists are at the end. "Established" means documented practice by others. "My recommendation" and "my estimate" are mine.

## (a) The professional pipeline, stage by stage

### 1. Export

Established:
- The research model is exported to ONNX one sub-network at a time, or converted to GGUF for ggml runtimes.
- Everything Python did around the network is rewritten natively: text normalisation, tokeniser, sampling and stop rules.
- Example: Chatterbox-turbo-cpp reimplements the BPE tokeniser in C++ and drives three ONNX graphs through ONNX Runtime (ORT) [W22].
- Example: PocketTTS.cpp is one C++ file over ORT, with no Python at run time [W32].
- Voice conditioning is computed once and stored:
  - Chatterbox-turbo-cpp precomputes the speaker conditioning in Python and ships it as a small file [W22].
  - PocketTTS.cpp caches the speaker embedding and also the transformer's state after conditioning; restoring that state takes about 4 ms [W32].

For LEDGER: the cast is fixed, and the voice server already learns each voice once and keeps it (P3). So the part that learns a voice from a clip need not ship. Ship each character's conditioning as data instead.

### 2. Splitting an autoregressive model

Established layout for Chatterbox-family ONNX, used by Resemble's own Turbo export and by onnx-community's export of the original [W18, W19, W22]:
- speech_encoder: reference clip → speaker embedding and prompt tokens.
- embed_tokens: tokens → embeddings. In the original model, exaggeration enters here.
- language_model: the transformer, with the KV cache ("past key values") as inputs and outputs.
- conditional_decoder: speech tokens → waveform (flow decoder plus vocoder).

Pocket TTS ports split differently: text conditioner, main flow LM, flow head, Mimi encoder and Mimi decoder [W32].

- **One language-model graph serves both passes.** It handles the first pass over the prompt ("prefill") and every later step, because prefill is simply a step with a long input and an empty cache. This is my knowledge of Hugging Face's exporter, which these repos follow; I did not re-read it this session.
  - The project's August export used separate prefill and step graphs, each about 3 GB at fp32 (P5). That fits each graph carrying its own copy of the transformer.
  - The hardware-floor note asked whether the two load two copies (P5). The one-graph layout removes the question.
- **On a card, keep the KV cache on the device between steps** with ORT's I/O binding. ORT's docs: "When the input is not copied to the target device, ORT copies it from the CPU as part of the Run() call ... This eats into the execution time of the graph" [W11].
  - The project measured this on this card in August: 42 ms per step with the cache crossing to the host, 17 ms bound to the card, and 142 µs per position of pure round trip (P1, P8).
- **Two August findings are rules, not tips:**
  - Device buffers from one DirectML session fed into another gave "fluent garbage" with no error.
  - Two DirectML sessions run at the same time from two threads crashed with an access violation.
  - Hence one thread, strictly interleaved (P1, P8).
- **On the processor the question does not arise:** the cache never leaves main memory.
- **Fixed-size cache.** A cache of fixed size, updated in place, is the usual alternative when a runtime handles changing shapes badly. This is my knowledge: ONNX Runtime GenAI works this way. Not verified this session.
- **The inverse STFT.** The vocoder's inverse STFT has no ONNX operator, so exports rewrite it with real-valued operations.
  - The project already has such a patch (P8, stft_patch.py).
  - It also avoids what kept Nano's vocoder off the card on 24 September: DirectML has no complex numbers (P3).

### 3. Precision

Established:
- fp16 for graphics cards.
- 8-bit for processors: the weights of the matrix multiplications are quantised per channel, activations are quantised on the fly, and convolutions often stay at fp32.
- 4-bit weight-only for browsers.
- Mixed precision where the numbers are delicate.

Examples:
- Resemble's Turbo ONNX ships the decoder in fp32, fp16 and 4-bit versions [W18].
- KitsuMate's Nano export uses a "fused mixed-INT8 language model" and an fp32 decoder with dynamic INT8 matrix multiplications; convolutions stay fp32 [W20].
- PocketTTS.cpp uses INT8 by default: "~4x smaller models at comparable quality" [W32].

Caution: 8-bit is not automatically faster on every processor. One Kokoro test on a 4-core Xeon found INT8 slowest and fp16 fastest [W39].

The project's own lesson (P1, 12 August):
- Converting the whole original Chatterbox language model to fp16 cut steps to 26 ms but broke the stop decision.
- Four of ten seeds stopped before 15 tokens, and the survivors ran 2 to 2.5 times too long.

The standard remedy is mixed precision: keep layer norms, softmax and the output head at fp32. ORT's converter accepts a block list for this, and P1 already calls it the "salvage". The ten-seed stop sweep is the right gate for any change of precision.

### 4. Runtime

There are four families; section (b) has the table:
- The engine's own: Unreal NNE.
- The vendor library: ONNX Runtime called directly, with DirectML or Windows ML.
- ggml / llama.cpp descendants: audio.cpp, chatterbox.cpp, NVIDIA's NVIGI.
- Middleware: ReadSpeaker speechEngine, Fab plugins.

Shipped or commercial evidence:
- **Epic's speech-to-face solver** ships in UE 5.8 as a beta plugin running on NNERuntimeORT, CPU or DirectML, prebuilt for packaged games (P4, read from the installed engine).
- **NVIDIA's Chatterbox TTS Plugin Pack 1.0.0** (updated 30 January 2026) [W25]:
  - It runs Chatterbox Turbo and Multilingual through GGML/llama.cpp, with CUDA, Vulkan and D3D12 back ends.
  - It needs about 2.3 GB of card memory for Turbo alone.
  - Its Vulkan back end creates its own device rather than sharing the game's, because sharing gave wrong output.
- **PUBG Ally (Krafton)** runs speech recognition, a small language model and a "custom in-house" TTS model on the player's RTX card, which must have at least 8 GB. The 4-bit language model alone takes 1.6 to 2.1 GB [W45].
- **Dead Meat (GDC 2025) and Mecha BREAK** moved the text model onto the device but kept ElevenLabs cloud voices [W46, W47].
- **ReadSpeaker** sells on-device neural TTS as an Unreal, Unity and Wwise plugin [W48].
- **A Fab plugin** runs Piper and Kokoro voices through ONNX Runtime, as whole lines or as streamed float PCM [W8].

My reading: fully local, cloned, conversational voices in shipped PC games exist so far only on NVIDIA-specific stacks. Nobody has published an AMD-card or processor-only version of what LEDGER wants. The processor route is therefore less trodden, but not exotic: it is what the Pocket TTS, Kokoro and Piper ports do everywhere.

### 5. Threading and streaming into the engine's audio

Established:
- **Inference runs on a dedicated worker thread.** The game thread only receives finished PCM through a thread-safe queue.
  - NNE's RDG interface is the exception: it is "invoked from the render thread" [W1]. That suits per-frame image models and is wrong for hundreds of token steps per line (my judgement).
- **Streaming APIs hand out short float PCM chunks.**
  - PocketTTS.cpp's C API is stream start, read and end. It runs token generation and audio decoding in parallel ("pipelined streaming", about 30 ms to the first chunk) [W32].
  - The Fab TTS plugin offers whole-line or streaming synthesis, with sample rate and channel count [W8].
- **Cap the runtime's own thread pool** so it does not fight the engine's worker threads: 2 to 3 threads on a 6-core part. This is my recommendation. ORT exposes an intra-op thread count and a no-spinning option (my knowledge; check in ORT's docs).
- **LEDGER already has the engine side** (P9). The game queues each piece on a procedural sound wave, joins streamed pieces without gaps, and drives the mouth from the queued PCM. A native worker only has to hand PCM to that queue instead of WAV file names.
- **The watermark in a stream** [W30]:
  - NVIDIA's NeMo applies Perth to each 480 to 640 ms chunk, with tapering at the joins.
  - A reviewer warned that the watermarker looks about 150 ms either side (2048-point FFT, 320-sample hop, five convolutions of width 7), so chunk edges are fragile.
  - The watermark model works at 32 kHz.
  - For LEDGER, applying it once per sentence piece avoids most edges (my recommendation).

### 6. Packaging and staging

Established, from Unreal's own documentation [W3]:
- **DLLs:**
  - Declare them with RuntimeDependencies so staging copies them next to the executable ("$(TargetOutputDir)", "$(BinaryOutputDir)", "$(PluginDir)").
  - Delay-load them with PublicDelayLoadDLLs.
  - Explicit loads go through FPlatformProcess::GetDllHandle, which "attempts to resolve any DLL dependencies to files in the engine's list of search paths".
- **Other files** are staged as one of two types:
  - UFS: "Only accessed through Unreal filesystem functions, and may be included in a PAK file".
  - NonUFS: "Must be kept as part of the loose filesystem".
- ORT opens models by file path, so any model it reads directly must be NonUFS.
- The alternative is to read the model through the engine's file system and hand ORT the bytes, which lets it go in the pak. ORT can create a session from memory (my knowledge).
- **NNE:**
  - Models import as NNE model-data assets and are cooked with the rest of the game.
  - Each asset can be enabled per runtime, to trim packaging [W1].
  - An asset loaded only by path must sit in a folder the cook always includes. P4 found the same for the mouth solver's model.
  - Large models whose weights sit in a separate file (over 2 GB) are a reported difficulty in NNE (forum, June 2026) [W5]. Nano's graphs are far below 2 GB.
- **DLL clashes:**
  - Plugins that bundle their own onnxruntime.dll clash with NNERuntimeORT, which has been enabled by default since 5.5; their makers tell users to disable Epic's plugin [W7, W9]. LEDGER cannot disable it, because the mouth solver needs it (P4).
  - Separately, Windows ships its own DirectML.dll in System32, which can differ from the version ORT needs. ORT users load their own copy explicitly [W13].
- **Current versions:**
  - ORT itself is at 1.30.0.
  - The newest DirectML build of ORT is 1.24.4 (PyPI upload 17 March 2026) [W12].
  - Microsoft's docs: "DirectML is in sustained engineering ... new feature development has moved to WinML" [W10].
  - Windows ML chooses a vendor's execution provider at run time [W15], but AMD's GPU provider (MIGraphX) needs RDNA 3 or later [W14]. The RX 6700 is RDNA 2, so on this card Windows ML would fall back to DirectML anyway.
- **The August C# route** pinned ORT 1.20.1 with DirectML 1.15.2: three DLLs, about 32 MB in all (P8).

### 7. Testing on a clean machine

Established practice (my knowledge; no source read this session):
- A Shipping build, with the engine's prerequisites installer (Visual C++ runtime) included.
- A machine or account with no development tools on it.
- A record of every library and data file the process actually opens.
- A long session, watching memory and frame time.

For LEDGER:
- The disk rules forbid moving or renaming anything outside the project's list, so the test cannot hide the tools folder on F: or Python.
- Instead the game proves where it loaded from. At start, and after its first spoken line, it lists its loaded modules and every model file it opened. The test fails if any path lies outside the installed game folder or Windows' own system folders.
- Shipping builds compile logging out unless the target enables it (bUseLoggingInShipping; my knowledge). So either enable it for the test build, or have the voice module write its own small report file.
- Windows Sandbox (Windows Pro only) would give a truly clean OS for a processor-only voice. Its graphics support is uncertain (my knowledge).

## (b) Runtime options in Unreal 5.8

| Option | How it works | CPU / card on this AMD PC | Packaging | Maturity | Licence |
|---|---|---|---|---|---|
| NNE with NNERuntimeORTCpu | Engine plugin running ORT on the CPU. "Input and output tensors are provided on the CPU and there is no memory transfer to another device" [W1] | CPU: yes | Model is a cooked asset; no extra DLLs; same ORT as the mouth solver | Ships with the engine; Epic's mouth solver uses it (P4); the solver plugin is beta, and NNE's overview page carries a status warning; changing shapes and thread control unverified | Unreal EULA; the ORT inside is MIT |
| NNE with NNERuntimeORTDml (GPU interface) | ORT with DirectML. Tensors are "provided as CPU memory ... the runtime will upload and download them" on every run [W1] | Card: DirectML runs on AMD GCN and later [W10], but the KV cache crosses PCIe every step (42 ms against 17 ms bound, P1) | As above | As above; DirectML is in "sustained engineering" [W10] | As above |
| NNE RDG interface | Tensors are render-graph buffers; inference "invoked from the render thread" [W1]; a GPU-only style-transfer port exists [W6] | Card only; ties the voice to frame rendering | As above | Suits per-frame image models | As above |
| ONNX Runtime called directly | Full C/C++ API: I/O binding [W11], session and thread options, sessions from memory | CPU: yes. Card: DirectML (last build 1.24.4) [W12]; Windows ML's AMD provider needs RDNA 3 [W14] | Ship onnxruntime.dll plus DirectML.dll (32 MB in August, P8), which clashes with the engine's copy [W7]; or link the engine's own copy (unverified) | Mature; the project ran this path from C# in August (P8) | MIT; DirectML's redistribution terms not read |
| ggml family: audio.cpp, chatterbox.cpp, pocket-tts.cpp, TTS.cpp | Native C++ over ggml; GGUF weights (16-bit, Q8); KV cache native; back ends CPU, Vulkan, CUDA, HIP, Metal [W24] | CPU: yes. Card: Vulkan works on AMD, but as a second graphics device beside Unreal's D3D12 | Ship ggml DLLs and GGUF files; no ORT clash | Young: audio.cpp went from 0.1 to 0.8.2 between June and 23 Sep 2026 [W24]; Chatterbox Turbo there is a community port | audio.cpp Apache-2.0 [W24]; chatterbox.cpp MIT [W23]; TTS.cpp MIT/Apache, but GPL if eSpeak is compiled in [W40] |
| NVIGI Chatterbox TTS Plugin Pack | NVIDIA's in-game SDK: GGML with CUDA, Vulkan and D3D12; Turbo and Multilingual; about 2.3 GB for Turbo [W25] | NVIGI names NVIDIA RTX 30-series or newer as its hardware [W26]; AMD not supported on paper | Prebuilt DLLs and GGUF files | 1.0.0, January 2026 | SDK MIT; NVIDIA's models under NVIDIA's own model licence [W25, W26]: not on the allowlist |
| sherpa-onnx | C/C++ library over ORT: Pocket TTS cloning, Kokoro, Piper and others; optional DirectML build [W34] | CPU: yes; card optional | Brings its own onnxruntime.dll (the same clash) | Mature, many platforms | Apache-2.0 [W34]; Kokoro and Piper paths normally use eSpeak-NG (GPL) for pronunciation (my understanding for sherpa's build) |
| Middleware: ReadSpeaker speechEngine; the Fab Piper/Kokoro plugin | A vendor runtime inside an Unreal plugin [W48, W8] | CPU | Vendor-packaged | Commercial | Paid (a money decision); ReadSpeaker speaks with its own voices, not our cast |
| Windows ML | ORT with the vendor's provider chosen at run time [W15] | Falls back to DirectML on RDNA 2 [W14] | Windows App SDK package | Generally available since 2025 | Microsoft terms (not read) |

NVIDIA also offers a TensorRT-for-RTX runtime for NNE [W49]. It is NVIDIA-only, so it does not apply here.

## (c) The models

### Chatterbox original (about 0.5 B parameters; exaggeration and CFG)

- **Ports:**
  - onnx-community/chatterbox-ONNX: four graphs, exaggeration applied in embed_tokens, defaults exaggeration 0.5 and cfg 0.5, MIT [W19]. Variants beyond fp32 not confirmed (card not readable).
  - The project's own August export: three graphs plus a chunked decoder (P1, P8).
  - audio.cpp's "chatterbox" family: 0.5 B backbone, GGUF 16-bit and Q8 [W24].
  - chatterbox.cpp (ggml) [W23].
- **Streaming:** not in the reference implementation. The project built chunked decoding with a seam cache (P1).
- **Published speed and memory:** none found for AMD. The project's own figures on the RX 6700 (P1, P5, P2):
  - 42 ms per step on the host path, 17 ms bound to the card.
  - fp16: 26 ms per step, but stops broken.
  - CPU: 68 to 77 ms per step.
  - Graphs of about 3 + 3 + 2 GB at fp32.
  - Chunk decode: 0.454 s per second of audio.
- **Weights licence:** MIT (repository LICENSE read 19 September, P2; audio.cpp's licence table of 21 Sep 2026 [W24]).
- **Implication:** this is the only route back to the mood control, and it is card-only. Not for this release. If revived, use the one-graph layout and mixed precision.

### Chatterbox Turbo (350 M; one-step decoder; tags; exaggeration ignored)

- **Ports:**
  - Resemble's official ONNX: embed_tokens, language_model with cache, conditional_decoder, speech_encoder; decoder in fp32, fp16 and 4-bit [W18, W22].
  - Chatterbox-turbo-cpp: C++, ORT 1.22 or newer, CPU or CUDA, MIT [W22].
  - chatterbox.cpp [W23].
  - An audio.cpp community port [W24].
  - NVIGI's GGUF files [W25].
- **Streaming:** not stated for the official ONNX sample (search summary only).
- **Speed:**
  - Vendor: "up to 6x faster than real-time on a modern GPU", about 75 ms latency; hardware not stated [W28].
  - NVIGI: about 2.3 GB of card memory for Turbo alone (NVIDIA's figure) [W25].
- **Weights licence:** MIT [W24, W16]. Exaggeration is accepted and ignored (P2).
- **Implication:** Resemble's Turbo layout is the template for exporting Nano, which "shares Turbo's architecture" [W16].

### Chatterbox Nano (110 M): the current voice

- **Ports:** no official ONNX found. Community exports:
  - KitsuMate/chatterbox-nano-v2-onnx [W20]:
    - Made from the fp32 checkpoint; English only; not streaming.
    - INT8 language model; fp32 decoder with INT8 matrix multiplications.
    - Its speech encoder's resampling changed about 6% of prompt tokens.
  - owensong/chatterbox-nano-ONNX: not streaming; one decoder call per line; publishes no quality or speed figures [W21].
  - audio.cpp lists Nano variants among its community ports [W24].
- **Speed:**
  - Vendor: "3x realtime on 8 cores" on the processor and 10x on a card; no hardware or method given [W16, W27].
  - Project, 23 September: PyTorch on this CPU while another build was running, 1.7 to 2.7 s of work per second of speech (P3).
  - Project, 24 September, on the card:
    - Nano alone: 0.90 to 1.04.
    - Beside the game: 1.28 to 1.32.
    - The game's slowest 1% of frames went from 12.9 to 16.0 ms.
    - Card memory: 2.1 GB for Nano beside the game's 3.5 GB.
- **Weights licence:** MIT [W27; repository LICENSE].
- **What the August numbers imply (my estimate; crude):**
  - The original model's CPU step was 68 to 77 ms for about 0.5 B parameters. Scaled by parameter count, a 110 M step would take roughly 15 ms at fp32, and less at 8-bit.
  - At 25 tokens per second of speech (P1), the token loop would then cost roughly a third of real time on this CPU. The decoder's cost is unknown.
  - The Python figure of about 1.9 includes Python and eager-PyTorch overhead on a busy CPU, so it is not the ceiling.
  - Measure before trusting any of this.
- **Card memory:** the 24 September test shows the game (3.0 to 3.5 GB) plus Nano (2.1 GB) fit on the 10 GB card. The hardware-floor fear (street 6 GB plus voice 5 GB) was about the original model at fp32 (P5). For Nano the binding constraint is time, not memory.

### Pocket TTS (100 M; set aside on accent grounds on 26 and 28 September, P10)

- **Ports:** many, listed by Kyutai [W31]:
  - PocketTTS.cpp: ORT, five graphs, INT8, streaming C API, cached voice state; MIT [W32].
  - sherpa-onnx: Apache-2.0, Pocket voice cloning [W34].
  - pocket-tts.cpp: ggml, pre-alpha.
  - Rust ports (candle, xn).
  - An ONNX export for the browser.
  - audio.cpp: GGUF, streaming [W24].
- **Streaming:** yes, built in [W31]:
  - "~200ms to get the first audio chunk"; "~6x real-time on a CPU of MacBook Air M4"; "Uses only 2 CPU cores".
  - On a 4-vCPU virtual machine with a T4 card, the CPU real-time factor was about 2.3 to 2.5.
- **Other published speed and memory:**
  - PocketTTS.cpp: 9.2x real time and 30 ms to first audio on a Ryzen 7 3800X, INT8; the maintainer's figure [W32].
  - Independent benchmark reported in P6: 122 ms to first audio, 4.35x real time and 2.29 GB peak memory on a Ryzen 9 9950X3D.
- **Licences:**
  - Weights: CC BY 4.0, with cloning gated behind consent terms [W33, W24]. Code: MIT [W31].
  - sherpa-onnx's model README wrongly says "non-commercial". An issue of 21 September 2026 points out that the bundled licence is CC BY 4.0 [W35].
- **Implication:** technically the easiest model to embed. PocketTTS.cpp is a complete reference for the pipeline LEDGER needs: graph split, INT8, cached voice state and a streaming C API. As a voice, it stays set aside.

### Kokoro (82 M; Apache-2.0)

- **Ports:** ONNX (onnx-community, kokoro-onnx), sherpa-onnx, TTS.cpp (CPU GGUF), audio.cpp (which lists en-gb) [W34, W40, W24], and a Fab plugin for Unreal [W8].
- **No cloning:** fixed preset voices, 54 in v1.0 [W24]. It cannot speak as Ron, Sheila or Darren.
- **Speed** [W36, 17 Feb 2025]:
  - 5x real time on a 32-vCPU AMD EPYC, for both PyTorch and ONNX on the CPU.
  - 20 to 37x real time with ONNX on T4 and L4 cards.
- **Licences:** weights Apache-2.0 [W24]. The usual pronunciation route uses eSpeak-NG (GPL-3.0), and kokoro-onnx requires phonemizer (GPLv3+) [W37, W38].
- **Implication:** small and fast, but wrong for a cloned cast, and the GPL pronunciation helper should be kept out of a closed game.

### Piper (VITS; no token loop)

- **Engine:** rhasspy/piper (MIT) was archived on 6 October 2025, and development moved to OHF-Voice/piper1-gpl (GPL-3.0) [W41]. Both use eSpeak-NG (GPL) for pronunciation. TTS.cpp states that compiling eSpeak in makes the binary GPL-3.0-or-later [W40].
- **Voices:** each is trained separately; no cloning. One find:
  - The en_GB-vctk-medium voice (77 MB) is trained on the same corpus as Ron's and Darren's clips.
  - Its 109 speakers include p227 (id 82) and p241 (id 98) [W42].
  - Its licence sits in a model card I could not open; Piper's voice list warns that some voices are restrictive [W43].
- **Speed:** very fast on the CPU (not measured here).
- **Implication:** at most a cheap fallback for barks. It would need its licence read and a pronunciation route free of GPL code.

## (d) Steps for LEDGER, in order

**0. Tell Jafar the size first.**
- About two working weeks (my estimate, below).
- It depends on the voice decision that is still open (paid voices were researched on 28 September, P10).
- If he chooses a paid voice, the local model becomes the offline fallback, and this work can shrink to steps 1, 7 and 8.
- A local runtime, if adopted, needs a DECISIONS entry citing the weights licence (Chatterbox MIT) and the runtime's licence (ORT MIT), under the allowlist's process rule.

**1. Read the installed engine (half a day).** In UE 5.8.2, find the ORT that NNERuntimeORT bundles and check:
- its version, and whether its DirectML provider is compiled in;
- whether a game module can compile against its headers and import library (same DLL, no second copy);
- whether NNE CPU model instances accept a new input shape on every call, and at what cost;
- whether the ORT thread count can be set through NNE;
- which runtime the mouth solver uses (P4).

**2. Export Nano (3 to 4 days, including parity checks).** Follow Resemble's Turbo ONNX layout [W18, W22]:
- The graphs:
  - embed_tokens;
  - language_model: one graph for prefill and steps, with the cache in and out;
  - conditional_decoder: the one-step decoder plus vocoder, with the inverse STFT as real-valued operations, as the existing patch already does.
- Not the speech encoder. Make each cast member's conditioning at build time from the approved clip and ship it as data, named by the exact clip it was made from (the handover rule on exact versions).
- Tokeniser and text normalisation in C++, checked against the Python tokeniser on a corpus of the game's own lines (the project's tokeniser reference exists).
- The sampler:
  - Nano and Turbo's defaults, quoted in P2: temperature 0.8, top-p 0.95, top-k 1000, repetition penalty 1.2.
  - The stop rules the Core already has (P1).
- Parity:
  - Greedy decoding (top-k 1) must give exactly the same tokens as Python.
  - Sampled output is judged by its distribution (step 3).
  - For identical tokens, compare the audio against Python by correlation, the method of P3's one-copy test.
- The community Nano exports [W20, W21] may be used for a first speed reading only.

**3. Precision (1 day).**
- Processor: 8-bit dynamic quantisation of the language model's matrix multiplications. Keep the decoder at fp32 first; try 8-bit matrix multiplications there only if the ear passes it.
- Card (only if chosen): fp16, with layer norms, softmax and the output head kept at fp32.
- The gate for either: the August ten-seed stop sweep on several lines (token counts inside the fp32 spread, no early stops), then the voice gate by ear.

**4. Watermark (1 to 3 days).**
- Export Perth's implicit watermarker (MIT) [W29] to ONNX.
- Run it on the processor on each sentence piece before the piece is queued. Chatterbox's Python applies it to every output [W17].
- Check with Perth's own detector, in Python, that the game's output carries the mark.
- If it will not export, that is a question for Jafar under D50 (P7).

**5. Measure (1 day).**
- Set-up: this PC, the street running at his settings, the three cast voices, the listening-test lines.
- Compare the processor at 2, 3 and 4 threads with the card using I/O binding.
- Record:
  - seconds of work per second of speech (median line and slowest line);
  - time to first sound;
  - game frame times (median and slowest 1%);
  - process memory and card memory.
- Proposed gate (mine): choose the processor if work is at most 0.6 s per second of speech on the median line and at most 0.9 on the slowest, and the slowest-1% frame time worsens by no more than 1 ms. Otherwise, the card.

**6. Choose the host, by rule:**
- Processor, and NNE CPU passes step 1's checks → NNE. This is the cheapest: nothing extra to ship, one ORT in the process, and the models cooked as assets.
- Processor, but NNE fails a check → ORT called directly.
- Card → ORT called directly. NNE's GPU interface copies tensors through main memory on every call, and its RDG interface runs on the render thread [W1].
  - Keep all voice sessions on one thread.
  - Never pass device buffers between sessions.
  - Never run the voice's DirectML session at the same time as another DirectML session (P1).
- If ORT is called directly:
  - First choice: compile against the engine's own ORT (step 1).
  - Second choice: your own ORT build, loaded by full path from the game's folder, under a name that cannot collide with the engine's (my suggestion; untested).
  - Never ship a second plain onnxruntime.dll beside Epic's [W7, W9].

**7. Build the worker into the game (2 to 3 days).**
- One worker thread owns the sessions: lines go in, PCM pieces come out.
- The pieces pass through a thread-safe queue to the existing procedural-wave queue and the mouth tick (P9).
- Keep the first piece short, as the Python server does (P3).
- The voice starts automatically in Shipping, with no command line.
- The Python server stays available in development builds, for A/B comparison only.

**8. Package and test (1 to 2 days).**
- Packaging:
  - NNE route: models as NNE assets in an always-cooked folder.
  - ORT route: models staged NonUFS (or read as bytes through the engine's file system), and DLLs through RuntimeDependencies [W3].
- Licence texts go in the credits: Chatterbox MIT, Perth MIT, ORT MIT, and DirectML's terms if it is used.
- Record any file of 100 MB or more in the large-file record.
- The test:
  - Create a fresh local Windows account on this PC, with no Python on its path and no Hugging Face sign-in.
  - Install the packaged build there.
  - The game writes out its list of loaded libraries and opened model files. The test fails on any path outside the game folder or Windows' own folders.
  - Play for thirty minutes; the AI tester walks it.

**Effort (my estimate):** 0.5 + 3–4 + 1 + 1–3 + 1 + 2–3 + 1–2 days, about 9.5 to 14.5 days in all: roughly two working weeks.

**A stopgap, honestly costed.**
- The list item's wording ("needs no outside scripts or arguments") could also be met by packing Python, the Nano model and its libraries inside the game folder, and having the game start them without arguments.
- Many desktop AI tools ship this way (my knowledge).
- Cost: 1 to 2 days and about 1.5 to 3 GB on disk (my estimate).
- Against it:
  - The card library it relies on was last released on 15 September 2024 and pins torch 2.4.1 [W44].
  - The server takes 16.5 s to be ready (P3).
  - The Python DirectML path crashed with access violations in August (P1).
- Use it only if item 3's thirty-minute walk has to happen before the native worker exists.

## (e) What could not be verified or reached

**Blocked by the network policy (403):**
- huggingface.co: every model card (Resemble's Turbo ONNX and Nano, onnx-community, KitsuMate, owensong, Kyutai, the piper-voices model cards).
- docs.nvidia.com and developer.nvidia.com: NVIGI docs, the PUBG Ally Q&A, the NNE TensorRT blog.
- learn.microsoft.com: Windows ML.
- forums.unrealengine.com.
- docs.georgy.dev and georgy.dev.
- readspeaker.com, resemble.ai, murmurtts.com, gpuopen.com, akiya-research-institute.github.io, videocardz.com, invenglobal.com, arcanumrpgs.com.
- The GitHub API was gated; raw files on GitHub were readable.

Figures from those sites are search summaries (SNIPPET).

**Not established:**
1. The ORT version inside UE 5.8.2, whether its DirectML provider is included, and whether game code can link against it.
2. Whether NNE CPU handles a cache that grows each step, at what per-call cost, and whether its thread count can be set.
3. Any speed or memory figure for Nano in ONNX on this PC, on the processor or the card.
   - My memory estimate (under about 1.5 GB on the processor) assumes Nano uses a decoder the size of Turbo's.
   - NVIDIA's file list names a 266 M "S3Gen-Meanflow" decoder for Turbo [W25].
   - Unverified.
4. Whether Resemble's Turbo ONNX decoder runs on DirectML.
5. Whether the Perth watermarker exports to ONNX, and its cost per sentence.
6. The file sizes of Resemble's ONNX variants, and whether the community Nano exports carry a licence file.
7. DirectML's redistribution terms, and Windows ML's Windows-version requirements.
8. The licence text of Piper's en_GB-vctk-medium voice.
9. Whether NVIGI's D3D12 back end runs on AMD cards, and the exact text of NVIDIA's model licence for its Chatterbox files.
10. No GDC or studio talk on shipping on-device TTS was found. The shipped-game evidence is press and vendor material.

## Sources

Web, all read 30 Sep 2026:

- W1. "Neural Network Engine Overview in Unreal Engine", Epic Games, undated (UE 5.8 documentation), https://dev.epicgames.com/documentation/en-us/unreal-engine/neural-network-engine-overview-in-unreal-engine, read 30 Sep 2026, OPENED.
- W2. "NNERuntimeORT" (plugin API page), Epic Games, undated (UE 5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/API/PluginIndex/NNERuntimeORT, read 30 Sep 2026, OPENED.
- W3. "Integrating Third-Party Libraries into Unreal Engine", Epic Games, undated (UE 5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine, read 30 Sep 2026, OPENED.
- W4. "NNE - Quick Start Guide - 5.3", Epic Games, undated, https://dev.epicgames.com/community/learning/tutorials/34q9/unreal-engine-nne-quick-start-guide-5-3, read 30 Sep 2026, SNIPPET (page body did not render).
- W5. "How to load the model .onnx with .onnx.data in NNE", Epic Developer Community forum, June 2026 (per the search summary), https://forums.unrealengine.com/t/how-to-load-the-model-onnx-with-onnx-data-in-nne/2731383, read 30 Sep 2026, SNIPPET.
- W6. "ONNX Runtime sample port for Unreal Engine 5.5 using NNE RDG - GPU-only inference", Epic Developer Community forum, undated, https://forums.unrealengine.com/t/onnx-runtime-sample-port-for-unreal-engine-5-5-using-nne-rdg-gpu-only-inference/2669899, read 30 Sep 2026, SNIPPET.
- W7. "System Requirements - NNEngine Manual", Akiya Research Institute, undated, https://akiya-research-institute.github.io/NNEngine-API/en/system-requirement/, read 30 Sep 2026, SNIPPET.
- W8. "Runtime Text To Speech", Georgy Dev, undated, https://solutions.georgy.dev/runtime-text-to-speech (and https://docs.georgy.dev/runtime-text-to-speech/overview/), read 30 Sep 2026, SNIPPET.
- W9. "Platform-specific Configuration", Georgy Dev Docs, undated, https://docs.georgy.dev/runtime-text-to-speech/platform-specific-configuration/, read 30 Sep 2026, SNIPPET.
- W10. "DirectML Execution Provider", Microsoft (ONNX Runtime docs), undated, https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html (read from its source, https://raw.githubusercontent.com/microsoft/onnxruntime/gh-pages/docs/execution-providers/DirectML-ExecutionProvider.md), read 30 Sep 2026, OPENED.
- W11. "I/O Binding", Microsoft (ONNX Runtime docs), undated, https://onnxruntime.ai/docs/performance/tune-performance/iobinding.html (source: https://raw.githubusercontent.com/microsoft/onnxruntime/gh-pages/docs/performance/tune-performance/iobinding.md), read 30 Sep 2026, OPENED.
- W12. Package version listings, NuGet and PyPI (Microsoft): Microsoft.ML.OnnxRuntime latest 1.30.0; Microsoft.ML.OnnxRuntime.DirectML latest 1.24.4; Microsoft.Windows.AI.MachineLearning 2.6.74-rc; onnxruntime-directml 1.24.4 uploaded 17 Mar 2026. https://api.nuget.org/v3-flatcontainer/microsoft.ml.onnxruntime.directml/index.json and https://pypi.org/project/onnxruntime-directml/, read 30 Sep 2026, OPENED.
- W13. "Support for loading a specific DirectML.dll", issue #18831, microsoft/onnxruntime, undated, https://github.com/microsoft/onnxruntime/issues/18831, read 30 Sep 2026, SNIPPET.
- W14. "KB5128774: AMD MIGraphX Execution Provider update (version 2.2609.2.0)", Microsoft Support, September 2026, https://support.microsoft.com/en-us/servicing/os/windows/ai-components/2026/09/kb5128774-windows-11-24h2-25h2-ml-model, read 30 Sep 2026, SNIPPET.
- W15. "Windows ML GA: Production-Ready On-Device AI Runtime for Windows 11", Windows Forum, undated (2025), https://windowsforum.com/threads/windows-ml-ga-production-ready-on-device-ai-runtime-for-windows-11.381965/, read 30 Sep 2026, SNIPPET.
- W16. "chatterbox" README, Resemble AI, undated (master branch), https://github.com/resemble-ai/chatterbox, read 30 Sep 2026, OPENED.
- W17. "src/chatterbox/tts_turbo.py", Resemble AI, undated (master branch), https://raw.githubusercontent.com/resemble-ai/chatterbox/master/src/chatterbox/tts_turbo.py, read 30 Sep 2026, OPENED (watermark lines only).
- W18. "ResembleAI/chatterbox-turbo-ONNX", Resemble AI (Hugging Face), undated, https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX, read 30 Sep 2026, SNIPPET.
- W19. "onnx-community/chatterbox-ONNX", onnx-community (Hugging Face), undated, https://huggingface.co/onnx-community/chatterbox-ONNX, read 30 Sep 2026, SNIPPET.
- W20. "KitsuMate/chatterbox-nano-v2-onnx", KitsuMate (Hugging Face), undated, https://huggingface.co/KitsuMate/chatterbox-nano-v2-onnx, read 30 Sep 2026, SNIPPET.
- W21. "owensong/chatterbox-nano-ONNX", owensong (Hugging Face), undated, https://huggingface.co/owensong/chatterbox-nano-ONNX, read 30 Sep 2026, SNIPPET.
- W22. "Chatterbox-turbo-cpp" README, DDATT, undated (2026), https://github.com/DDATT/Chatterbox-turbo-cpp, read 30 Sep 2026, OPENED.
- W23. "chatterbox.cpp: Chatterbox tts engine ported to ggml", wgabrys88, undated (2026), https://github.com/wgabrys88/chatterbox.cpp, read 30 Sep 2026, OPENED (front page only; README body not rendered).
- W24. "audio.cpp" README, LICENSE and docs/model_licenses.md, ShugoAI LLC, release v0.8.2 of 23 Sep 2026 (licence table dated 21 Sep 2026), https://github.com/0xShug0/audio.cpp, read 30 Sep 2026, OPENED.
- W25. "NVIDIA In-Game Inferencing (NVIGI) Chatterbox TTS Plugin Pack 1.0.0", with its model card, programming guide and getting-started pages, NVIDIA, last updated 30 Jan 2026 (per the search summary), https://docs.nvidia.com/ace-for-games/chatterbox-tts/index.html and https://docs.nvidia.com/ace-for-games/chatterbox-tts/nvigi-chatterbox-model-card.html, read 30 Sep 2026, SNIPPET.
- W26. NVIGI-Core LICENSE and README, NVIDIA, 2024–2026, https://github.com/NVIDIA-RTX/NVIGI-Core, read 30 Sep 2026, OPENED.
- W27. "Chatterbox Nano and Flash: Speed at the edge, throughput at scale", Resemble AI, undated (2026), https://www.resemble.ai/resources/chatterbox-nano-and-flash-speed-at-the-edge-throughput-at-scale, read 30 Sep 2026, SNIPPET.
- W28. "Chatterbox Turbo: Open Source, Ultrafast Text-to-Speech", Resemble AI, undated, https://www.resemble.ai/chatterbox-turbo/, read 30 Sep 2026, SNIPPET.
- W29. "Perth" README, Resemble AI, undated, https://github.com/resemble-ai/Perth, read 30 Sep 2026, OPENED.
- W30. "feat(tts): vendor Perth watermarking in EasyMagpie codec stage", pull request #16208, NVIDIA-NeMo/Speech, opened 2 Sep 2026, https://github.com/NVIDIA-NeMo/Speech/pull/16208, read 30 Sep 2026, OPENED.
- W31. "pocket-tts" README, Kyutai, undated (tech report of 13 Jan 2026), https://github.com/kyutai-labs/pocket-tts, read 30 Sep 2026, OPENED.
- W32. "PocketTTS.cpp" README, VolgaGerm, undated, https://github.com/VolgaGerm/PocketTTS.cpp, read 30 Sep 2026, OPENED.
- W33. "kyutai/pocket-tts" model card and the "Open access to the model" discussion, Kyutai (Hugging Face), undated, https://huggingface.co/kyutai/pocket-tts, read 30 Sep 2026, SNIPPET.
- W34. "sherpa-onnx" README, CMakeLists.txt and LICENSE, k2-fsa, undated, https://github.com/k2-fsa/sherpa-onnx, read 30 Sep 2026, OPENED.
- W35. "pocket-tts model README says 'non-commercial' but the bundled LICENSE is CC-BY-4.0", issue #3971, k2-fsa/sherpa-onnx, 21 Sep 2026, https://github.com/k2-fsa/sherpa-onnx/issues/3971, read 30 Sep 2026, OPENED.
- W36. "Kokoro v1 Benchmark (PyTorch/ONNX, CPU/GPU)", efemaer (GitHub gist), 17 Feb 2025, https://gist.github.com/efemaer/23d9a3b949b751dde315192b4dcf0653, read 30 Sep 2026, OPENED.
- W37. "[Question] GPL implications of espeak-ng dependency", issue #247, hexgrad/kokoro, undated, https://github.com/hexgrad/kokoro/issues/247, read 30 Sep 2026, SNIPPET.
- W38. "kokoro-onnx pulls in phonemizer (GPLv3+), a real licence conflict the new notices check catches", issue #619, Rumeasiyan/askwell, undated, https://github.com/Rumeasiyan/askwell/issues/619, read 30 Sep 2026, SNIPPET.
- W39. "Self-Hosted TTS with Kokoro ONNX: What CPU-Only Inference Actually Gets You", NemesisNet Lab, undated, https://blog.nemesisnet.co.za/self-hosted-tts-with-kokoro-onnx-what-cpu-only-inference-actually-gets-you/, read 30 Sep 2026, SNIPPET.
- W40. "TTS.cpp" README, mmwillet, undated, https://github.com/mmwillet/TTS.cpp, read 30 Sep 2026, OPENED.
- W41. "Piper TTS Explained: Metrics, Licensing and Limits", Cekura, undated, https://www.cekura.ai/discover/piper-tts, read 30 Sep 2026, SNIPPET.
- W42. "voices.json", rhasspy/piper-samples, undated, https://github.com/rhasspy/piper-samples/blob/master/voices.json, read 30 Sep 2026, OPENED.
- W43. "docs/VOICES.md", OHF-Voice/piper1-gpl, undated, https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md, read 30 Sep 2026, OPENED.
- W44. "torch-directml" release history, Microsoft (PyPI), latest release 0.2.5.dev240914 of 15 Sep 2024, https://pypi.org/project/torch-directml/, read 30 Sep 2026, OPENED.
- W45. "Q&A: How KRAFTON Built PUBG Ally, a Co-Playable Character Powered by NVIDIA ACE", NVIDIA Technical Blog, undated, https://developer.nvidia.com/blog/how-krafton-built-pubg-ally-a-co-playable-character-powered-by-nvidia-ace/; and "NVIDIA ACE AI teammate now available in PUBG, needs RTX GPU with at least 8GB VRAM", VideoCardz, undated, https://videocardz.com/newz/nvidia-ace-ai-teammate-now-available-in-pubg-needs-rtx-gpu-with-at-least-8gb-vram; read 30 Sep 2026, SNIPPET.
- W46. "Bringing AI NPCs to Life With NVIDIA ACE On-Device Small Language Models in Meaning Machine's Dead Meat", GDC 2025 session, NVIDIA On-Demand, March 2025, https://www.nvidia.com/en-us/on-demand/session/gdc25-gdc1010/, read 30 Sep 2026, SNIPPET.
- W47. "NVIDIA ACE & Digital Human Technologies Showcased In First Game, Mecha BREAK", NVIDIA GeForce News, undated, https://www.nvidia.com/en-ph/geforce/news/mecha-break-nvidia-ace-nims-rtx-pc-laptop-games-apps, read 30 Sep 2026, SNIPPET.
- W48. "Runtime Text to Speech plugin (On-Device AI voices - TTS) by ReadSpeaker", Fab / Unreal Marketplace, undated, https://www.unrealengine.com/marketplace/en-US/product/runtime-text-to-speech-plugin; and "speechEngine SDK", ReadSpeaker, undated, https://www.readspeaker.com/products/speechengine-sdk/; read 30 Sep 2026, SNIPPET.
- W49. "Speed Up Unreal Engine NNE Inference with NVIDIA TensorRT for RTX Runtime", NVIDIA Technical Blog, undated, https://developer.nvidia.com/blog/speed-up-unreal-engine-nne-inference-with-nvidia-tensorrt-for-rtx-runtime/, read 30 Sep 2026, SNIPPET.

Project records, read 30 Sep 2026 in the repository:

- P1. game-design/live-speech-latency.md: the August measurements (42 and 17 ms steps; the fp16 sweep; CPU 68–77 ms per step; the one-thread rule after the crash).
- P2. production/research/live-speech-architecture/SUMMARY.md and RECHECK.md (19 September): Turbo and Nano ignore exaggeration; the sampler defaults; chunk decode at 0.454 s per second of audio.
- P3. production/research/nano-listening-test/: cpu-speed-2026-09-23.txt, card-timing-2026-09-24.md, voice-server-one-copy-2026-09-25.md.
- P4. production/research/lip-sync/NOTE-2026-09-30.md.
- P5. production/research/hardware-floor/SUMMARY.md.
- P6. production/research/live-speech-architecture/conversation-latency-2026-09-25.md.
- P7. production/research/tts-licensing-and-consent/SUMMARY.md; D50 ("The voice watermark is kept") in production/archive/DECISIONS-to-2026-09-24.md.
- P8. ledger/Assets/Scripts/Game/OnnxSpeech.cs; tools/fetch-onnxruntime.py; tools/voice-live/bench-binding.py, convert-fp16.py and stft_patch.py.
- P9. ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp, about lines 2790–2850 (voice start-up and the procedural-wave queue).
- P10. DECISIONS.md (Pocket TTS set aside on 26 and 28 September); production/research/live-speech-architecture/paid-voices-2026-09-28.md.
- P11. production/specs/voice-engines.json; tools/voice-live/voice-server.py and pocket-server.py; ledger-v2/research/license-allowlist.md.
