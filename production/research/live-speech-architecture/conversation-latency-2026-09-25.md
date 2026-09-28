Research checked **25 September 2026**. **Try CPU-based streaming speech before more Radeon optimisation.** No public benchmark I found combines your RX 6700, Unreal workload and cloned British voices. Your CPU is unspecified; hardware delay ranges below are conditional engineering estimates.

**How much silence is tolerable?**

Human conversation commonly has median turn gaps below **300 ms**; that describes behaviour, not a universal tolerance limit (Meyer, April 2023). [1](https://pubmed.ncbi.nlm.nih.gov/37033404/) A July 2025 study with **54 participants**, spoken virtual characters and gamified tasks compared **1.5, 4 and 6.5 seconds**: perceived responsiveness worsened at 4 seconds, and willingness to reuse the system was lowest with long delays. [2](https://arxiv.org/html/2507.22352v1) Conversely, an August 2024 driving-assistant study preferred **1.5 seconds**, but involved only **six experts**. Context matters. [3](https://journals.sagepub.com/doi/10.1177/10711813241260290)

For LEDGER, my design target is **under one second to a substantive reply**, with **1–2 seconds** an interim target and repeated **4+ seconds** unacceptable. A grunt is acknowledgement, not the reply.

**Where the six seconds goes**

Your described sequence makes LLM generation and speech generation additive. LEDGER’s [24 September voice-server.py](https://github.com/jsab258/ledger/blob/6de07a0b178199873ee6c3999d7331f07dbe33d1/tools/voice-live/voice-server.py) already keeps models loaded and splits sentences, but calls `generate(piece)`, writes the completed WAV, then announces it. It also conditions each voice on its first use, and keeps separate CPU and DirectML models. [FINDINGS.md](https://github.com/jsab258/ledger/blob/6de07a0b178199873ee6c3999d7331f07dbe33d1/FINDINGS.md) records **four seconds’ generation for three seconds’ speech** under game load.

Thus **roughly two seconds LLM/transport plus four seconds TTS** is plausible, but not a measured breakdown. First-use conditioning can add more.

The changes worth testing:

- **Instrument the actual path:** submission, LLM first token, first speakable clause, TTS first PCM, first audible sample. Record median/p95, audio underruns and game frame time. Typed input needs **no speech recognition or silence detection**.
- **Stream LLM output into TTS:** request a short opening sentence and concise answers; use a fast non-reasoning model, compact relevant context and prompt caching where supported. Begin with a complete short clause, perhaps 5–10 words; synthesising isolated words sacrifices context and prosody.
- **Stream generated audio into Unreal**, with a small playback buffer. Sending a finished WAV in network chunks does not remove its synthesis wait. Keep generating the following sentence while the current one plays. ElevenLabs documents a hidden trap: its default input buffer waits for **120 characters**; explicit flushing or shorter thresholds reduces waiting, with a quality trade-off. [4](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tts)
- **Precompute all cast voice conditioning before interaction.** Compare CPU-only execution against the current GPU/CPU split; CPU-native speech avoids graphics-memory contention, but still competes for processor time. Cap rendering to the intended frame rate during measurement.

**Streaming alone cannot cure insufficient throughput.** If the recorded real-time factor of 4/3 persists, a nine-second answer takes approximately twelve seconds to generate: continuous playback needs roughly three seconds’ initial lead even with ideal streaming. Shorter sentences relocate the gaps unless throughput improves.

**Free cloning models worth testing**

An independent Windows 11 benchmark used a **Ryzen 9 9950X3D CPU**, with cloning, five prompts, three runs per case, models already loaded and no reported game workload. Its reported first-audio times exclude the LLM. This is useful evidence, but that processor may substantially outperform yours. Checked 25 September: [5](https://5uck1ess.github.io/tts-bench/speed.html)[6](https://5uck1ess.github.io/tts-bench/windows-cloning/index.html)

| Model | Warm first audio / generation speed | Peak system RAM; commercial licence |
|---|---:|---|
| **Pocket TTS, 100M** | **122 ms / 4.35× realtime** | **2.29 GB**; MIT code, CC-BY-4.0 weights, attribution and cloning-consent conditions. [7](https://huggingface.co/kyutai/pocket-tts/blob/main/README.md)[8](https://github.com/kyutai-labs/pocket-tts) |
| **Sopro V2 Turbo, 120M**, August 2026 | **504 ms / 2.49× realtime**, streaming | **1.32 GB**; Apache-2.0 code/weights. Clones 5–20-second references. [9](https://huggingface.co/samuel-vitorino/sopro-v2-turbo) |
| **MOSS-TTS-Nano, 100M**, April 2026 | **5.04 s / 1.25× realtime** in the tested path | **3.05 GB**; Apache-2.0. A separate ONNX route exists, but this measured result does not establish subsecond onset. [10](https://github.com/OpenMOSS/MOSS-TTS-Nano)[11](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Nano-100M-ONNX)[12](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX) |

For Pocket, the MIT **PocketTTS.cpp** runtime additionally reports **30 ms first chunk on Ryzen 7 3800X**, with cached conditioning and INT8. That is its maintainer’s measurement, not independently verified game performance. [13](https://github.com/VolgaGerm/PocketTTS.cpp) **Qwen3-TTS 0.6B**, Apache-2.0, is a lower-priority trial: a July 2026 independent CPU cloning test measured **RTF 3.17** on four shared vCPUs. [14](https://arxiv.org/html/2601.15621v1)[15](https://ocdevel.com/blog/20260711-quantized-cpu-tts)

Quality remains a trade-off: an independent **five-prompt, one-reference** comparison scored Pocket’s speaker similarity **0.513**, versus original Chatterbox **0.627** and streaming Sopro **0.579**. These are embedding scores, **not percentages of resemblance or listening ratings**. [16](https://5uck1ess.github.io/tts-bench/scores.html) I found no robust Northern-English cloning listening test for these candidates. Expect to audition your actual cast for accent drift, missing words and unnatural joins; do not accept “supports English” as evidence.

**Paid cloud speech: measured latency and costs**

Coval’s September measurements below include leading silence but exclude connection setup; they use fixed benchmark voices. They exclude your LLM and Unreal playback. Keep connections open. [17](https://github.com/coval-ai/benchmarks/blob/main/docs/methodology.md)

| Commercial cloning service—**paid** | Median / p99 first audible audio | Estimated USD per generated hour* |
|---|---:|---:|
| Inworld TTS-2 Flash | **70 / 179 ms** | **$0.90**, on demand |
| Inworld TTS-2 | **164 / 299 ms** | **$1.50**, on demand |
| ElevenLabs Flash v2.5 | **185 / 331 ms** | **$3**, $6/month Starter minimum |
| Cartesia Sonic 3.6 | **357 / 863 ms** | **~$3**, $5/month Pro minimum |

Latency: Coval, checked 25 September. [18](https://benchmarks.coval.ai/benchmarks/time-to-first-audio) Prices and commercial/cloning terms: current provider pages; free ElevenLabs/Cartesia tiers do not qualify. [19](https://inworld.ai/pricing)[20](https://elevenlabs.io/pricing/api)[21](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform)[22](https://www.cartesia.ai/pricing)[23](https://www.cartesia.ai/vs/cartesia-vs-gemini-tts) *Calculation assumes 60,000 characters/hour, standard instant clones and fully used allowances; excludes LLM charges.*

Sonic 3.6 has stronger general listening evidence: it led **VOICE-H’s 9 September English evaluation**. That does not establish superiority for your clones. Inworld Flash is the cheapest latency experiment; network location and service congestion still affect results. [24](https://labs.askable.com/research/voice-h-round-two/)

**Making a pause look intentional**

The 2025 study found thinking gestures plus voiced fillers improved perceived waiting; loading icons/sounds did not significantly help. [2](https://arxiv.org/html/2507.22352v1) For LEDGER, pre-render several character-specific breaths, “Hmm” and brief acknowledgements; pair them with gaze shifts or continuing a task. Use them selectively, avoid accidental agreement, and permit interruption. A cached, situation-valid opening line can provide substantive speech immediately; include it in the LLM context so the continuation matches. Never force a filler to finish when the answer is ready.

**What shipped games demonstrate**

**Vaudeville**, released November 2025, left characters motionless during generation. A **25 February 2026 hands-on review** reported over five seconds before the first sentence, awkward silence and unskippable speech. It did not solve the problem. [25](https://www.thedrastikmeasure.com/2026/02/25/vaudeville-pc-review/)

**AI2U**, now released, uses cloud LLMs and Minimax TTS. [26](https://store.steampowered.com/app/2880730/) During its April 2026 early-access update, players reported **up to 30 seconds**, a persistent “Thinking…” indicator, and near-unplayability; another remained engaged but found it annoying. These are anecdotes about that build, not today’s latency measurements. [27](https://steamcommunity.com/app/2880730/discussions/0/802345631536534109/?l=spanish)

Confidence: **high** on the serial bottleneck and reported study results; **moderate** on model ranking; **low-to-moderate** on this PC’s achievable ranges until CPU and in-game timings are known.

**Ranked next-week trials**

1. **Free: instrument, preload voices and stream LLM clauses to the existing server.** A deliberately short opener might reach **2–4 seconds**; an ordinary three-second sentence still costs about **four seconds of TTS alone**.
2. **Free: Pocket TTS on CPU**, then its C++ runtime if necessary; audition Sopro if resemblance fails. With the first LLM clause available in **0.5–1 second**, budget **0.2–0.8 seconds TTS + 0.05–0.15 playback**: approximately **0.8–2 seconds total**. Keep the optional local LLM off during this comparison. Reject configurations that cannot sustain speech beside the game.
3. **Paid: Inworld Flash**, then Sonic 3.6 if voice quality justifies it. With streamed LLM output, target **0.7–1.5 seconds typical**, while measuring long-tail delays.
4. **Free: cached acknowledgements/openers**, audible in approximately **0.1–0.3 seconds**. They improve perceived response; they do not reduce dynamic-answer latency.
