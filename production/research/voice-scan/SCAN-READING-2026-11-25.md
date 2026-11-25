Built on: QUESTIONS-2026-11-25.md

All pages read on 25 Nov 2026 through a page-to-text reader (a small model summarises the fetched page, so a figure the reader did not return is marked "not stated on the page read"). "Secondary" means a blog or aggregator, not the maker. Nothing was downloaded or installed. No ranking or choice is made here.

## 1. Open-weight local TTS released or majorly updated, 1 Sep to 25 Nov 2026

Order of the table is by date found, not merit. Latency numbers are the maker's, on the hardware named; none was measured here.

### 1a. ZONOS3-Mini (Zyphra)
- Date: blog dated 11 Nov (byline) / 12 Nov (header) 2026. https://huggingface.co/blog/Zyphra/zonos3-mini (read 25 Nov 2026). Aggregators say 9 Nov (unverified).
- Licence as written: "Model weights are released under Apache 2.0" (https://huggingface.co/Zyphra/ZONOS3-Mini, read 25 Nov 2026); transformers copy: "The weights are released under the Apache License 2.0", remote code MIT, with adapted Apache-2.0 and BSD-2-Clause parts, "see NOTICE and licenses/" (https://huggingface.co/Zyphra/ZONOS3-Mini-hf, read 25 Nov 2026). Runtime repo: MIT (https://github.com/Zyphra/ZONOS3-Mini, read 25 Nov 2026). The weights licence file itself, output ownership and any AI-training clause: not stated on the pages read; unverified.
- Size: 800M total, about 100M active (latent MoE, 64 experts, top-2); Hub shows 0.9B (HF blog, model card).
- CPU or GPU: both. "synthesizes 44.1 kHz mono speech on CPU or GPU with nothing but torch and transformers" (-hf card); C++/ggml server and CLI for CPU, CUDA, Metal, Vulkan, no Python at runtime, needs a Rust toolchain to build (GitHub); WebGPU in browser. No minimum specs or RAM figure stated.
- Published latency: median time to first audio 80 ms at concurrency 8 on one H100 80GB; under 150 ms on an M3 MacBook Air; under 570 ms in the browser on a Pixel 9; peak 457 s of audio per second on the H100 (HF blog). No real-time factor and no Windows CPU or consumer NVIDIA figure stated.
- Streaming: yes (SGLang server streams 44.1 kHz PCM; decoder renders as frames are generated).
- Cloning: zero-shot, in-context reference "5-10s" in the example, up to 60 s allowed, or a 192-d speaker embedding (model card, blog).
- English accents: "accent steering" with task vectors and optional adapters (`--accent-adapters`). Blog demo shows General American base, "british: 1.5" steering described as "an approximation of the Southern English target", and "australian: 1.5". No Scottish, Irish or northern English mentioned. Evaluation is listening only, "no accent metrics".
- Watermark or consent clause: none mentioned on the pages read.
- Maker's quality claim (vendor-reported, unverified): first among open-weight models on its own ZTTS2 capability index, ahead of Fish S2 Pro and MOSS TTS v1.5; Pocket TTS and Kokoro not mentioned.

### 1b. Phonon 31M English (Gradium; 40M variants too)
- Date: "launched two weeks before" a post dated 5 Nov 2026, so about 22 Oct (https://gradium.ai/blog/phonon-closer-look, read 25 Nov 2026); model card shows "Updated Oct 23" for the collection, no release date stated (https://huggingface.co/gradium/phonon-31m-en, read 25 Nov 2026). Artificial Analysis lists it as Oct 2026.
- Licence as written: "The weights, tokenizer and voices in this repository are released under Apache 2.0, which allows commercial use." Runtime "MIT OR Apache-2.0". Phonon 40m: non-commercial licence (Gradium blog). Output ownership and AI-training clause: not stated on pages read; unverified.
- Size: 31M parameters excluding tokenizer; q8 GGUF file 64.5 MB. Builds on Kyutai's Pocket TTS lineage and the Mimi codec (Gradium blog).
- CPU or GPU: "a browser tab, on a phone, or on a laptop CPU"; ptts runtime supports CPU, GPU, NPU.
- Published latency: time to first audio (95th percentile) 28 ms for Phonon 31M EN, 38 ms for 40M EN, Pocket TTS 165 ms, on "Hugging Face's CPU streaming benchmark"; benchmark hardware and real-time factor not stated (Gradium blog). The model card gives no latency figure.
- Streaming: yes.
- Cloning: the card mentions cloning through Gradium Studio (a hosted product); no local reference-clip cloning with this release's weights is described on the card, and no clip length is given. Whether the open model clones from a reference clip: unverified. About 100 built-in voices (gradium/phonon-voices); example voice "Easton (en-us)".
- English accents: none listed beyond en-us; "English only".
- Maker's quality claims (vendor-reported): 1.5% hard-set LLM WER, 0.51% Seed-TTS LLM WER; card's own table lists Kokoro at 0.45% on Seed-TTS.
- Note: the card prohibits impersonation and cloning without consent; asks that listeners be told speech is synthetic "where that matters".

### 1c. Ming-3.0-tts, 0.5B and tiny (inclusionAI / Ant Group)
- Date: "2026.10" in the GitHub news (https://github.com/inclusionAI/Ming-3.0-tts, read 25 Nov 2026). Exact day (19 Oct) only in secondary sources, unverified.
- Licence: MIT (cards https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B and https://huggingface.co/inclusionAI/Ming-3.0-tts-tiny, read 25 Nov 2026); the licence file text not reproduced on the pages read.
- Size: 0.5B dense (Qwen2.5-0.5B backbone, Hub shows "1B params" in F32/BF16); tiny is MoE, 7.9B total, 1.3B active.
- CPU or GPU: tested on NVIDIA H800-80GB and H20-96G; tiny: "recommends NVIDIA H800". No CPU support mentioned.
- Latency or RTF: not stated; streaming not mentioned.
- Cloning: from a reference WAV plus its transcript ("a short reference clip", no length). Voice design from text.
- English: recommended voices UK_George (English UK, male) and US_Emma; Sichuanese and Cantonese dialect control; no English regional accents listed.
- Quality claims (WER, speaker similarity, UTMOS) are the maker's.

### 1d. Fish Audio Drama 3 (Fish Audio)
- Date: Oct 2026 (Artificial Analysis); secondary sources say 13 or 14 Oct, an aggregator says 1 Oct. Unverified which.
- Size: 35B MoE, 3B active, FP8 experts (https://huggingface.co/fishaudio/drama-3, read 25 Nov 2026). Runs on SGLang-Omni or vLLM-Omni; benchmarks on one NVIDIA H200: first audio about 89 ms (p50) single stream, RTF 0.37 at concurrency 16. No consumer-PC or CPU figure; a 35B model is not stated to fit a consumer card (unverified).
- Licence, Fish Audio Community License v1.0, read from https://huggingface.co/fishaudio/drama-3/blob/main/LICENSE on 25 Nov 2026 (through the reader; the model page's licence tag instead says "fish-audio-research-license", an inconsistency):
  - Commercial: free "only while Your Annual Revenue is less than USD 500,000" (III(a)); revenue counts "You and Your Affiliates, in aggregate, from all sources"; "no license is granted under this Agreement to offer a Hosted Service" (III(c)); other commercial use "requires a separate written license agreement from Fish Audio" (III(d)).
  - Output ownership: "You own any outputs generated from the Models or Derivative Works to the extent permitted by applicable law." (IV(c)(iii))
  - AI training: may not use the materials or outputs "to create, train, distill, or improve any foundational generative AI model" (IV(b)); detection and watermark-verification training excluded.
  - Attribution: products must prominently display "Built with Fish Audio" (IV(a)).
  - Consent: may not "generate speech that imitates the voice of an identifiable natural person without that person's prior consent" (IV(b)(i)).
- Streaming: per chunk. Cloning: yes (supported; reference length not stated). Accents: not stated on the page read.

### 1e. Audio8-TTS-Realistic-Air (Edge0)
- Date: 14 Oct 2026 per an aggregator (https://theopenweights.com/categories/tts-audio, read 25 Nov 2026); not stated on the model card. Unverified.
- Licence: Apache 2.0 (https://huggingface.co/Edge0/Audio8-TTS-Realistic-Air, read 25 Nov 2026); full text not shown.
- Size: 0.6B; 23 languages. Transformers package tested on an NVIDIA H20 in BF16; "CUDA-capable GPU" recommended; a native llama.cpp build with a 3.76 GB F32 bundle and incremental streaming is mentioned. No CPU latency or RTF stated. Cloning: reference recording plus exact transcript. Accents: not stated. Maker's Seed-TTS error 1.25%.

### 1f. Pocket TTS small English models
See question 2 (released 20 Oct 2026).

### 1g. Dia2 (Nari Labs)
- README line "UPDATE (11/19): Dia2 is released on Github and HuggingFace" has no year (https://github.com/nari-labs/dia, read 25 Nov 2026), so whether it is 19 Nov 2026 is unverified. Card https://huggingface.co/nari-labs/Dia2-2B: Apache 2.0, 2B (and a 1B), English only, streaming dialogue model, CPU fallback, CUDA 12.8+ for GPU, no accents mentioned, no cloning wording (prefix audio gives conversational context). Latency not stated. Release date not stated.

### 1h. Seen in the window but not usable or not confirmed
- MOSS-TTS family (OpenMOSS): README (https://github.com/OpenMOSS/MOSS-TTS, read 25 Nov 2026) has no entry after 2026.6.18, so no release in the window. Apache 2.0; MOSS-TTS-Nano (about 0.1B, 13 Apr 2026) is CPU-first, "Realtime generation on just 4 CPU cores". Listed only because it is a CPU model.
- Breeze TTS 2: weights and code 25 Aug 2026, before the window (https://huggingface.co/BreezeBlue/Breeze-TTS-2, read 25 Nov 2026). Weights "for research and non-commercial use only"; Linux plus CUDA, 12 GB GPU minimum; under 40 ms first audio on an H100. Named only because it ranks high on the leaderboards in question 3.
- Voxtral TTS (Mistral): Mar 2026, outside window; CC BY-NC 4.0 per its card (https://huggingface.co/mistralai/Voxtral-4B-TTS-2603, read 25 Nov 2026).
- Listed by one aggregator in the window with no primary page read: StepAudio 3 Gen (10 Sep; a search found only preview APIs, open weights unconfirmed), Nari Labs TTS and ASR (14 Sep; nothing found), Maya2 Native (26 Oct, Indic), Apriel Voice 27B (28 Oct), LFM3-Omni-2B (21 Oct), Liquid-Codec (16 Sep), Haru-4B (12 Nov). All unverified, none read at the maker.
- Cloud-only, skipped: Fish Audio hosted API, Gradium Studio, BreezeBlue platform/API, StepAudio 3 preview APIs.

## 2. Pocket TTS since 26 Oct 2026

- No release found after 26 Oct. PyPI lists latest 4.0.1 on 21 Oct 2026 (https://pypi.org/project/pocket-tts/, read 25 Nov 2026). GitHub releases page lists v4.0.1 as the newest, 21 Oct (https://github.com/kyutai-labs/pocket-tts/releases, read 25 Nov 2026). The Kyutai blog (https://kyutai.org/blog/, read 25 Nov 2026) lists no Pocket post after 20 Oct 2026.
- What landed just before 26 Oct (possibly after the ledger's own 26 Oct record was made; whether the 26 Oct tests used it is unverified):
  - v4.0.0, 20 Oct: six new English models, 18M, 7M and 2M (with "refl" reward-fine-tuned variants; 2M experimental), standalone binaries and a Rust CLI, retrained French, Italian, Dutch, German, Spanish, Portuguese, community models for Greek, Japanese, Turkish; onset-click fix (5 ms fade-in) (https://github.com/kyutai-labs/pocket-tts/releases/tag/v4.0.0, read 25 Nov 2026).
  - v4.0.1, 21 Oct: fixes sub-20M models; "Makes english_2026-10 the default English model" (releases page).
  - Parameter counts: 18.2M, 6.9M, 1.9M with decoder (README, raw GitHub, read 25 Nov 2026). The main model is about 100M.
  - Earlier in the window: v3.0.0 on 25 Aug (training code), v3.1.0 3 Sep, v3.2.0 23 Sep, v3.3.0 24 Sep (temperature 0.3 for every shipped model; Dutch added).
- Blog posts "Building a Pocket TTS with a drifting objective" (28 Sep) and "The tiny TTS was actually 10x too big" (20 Oct): pages reached but the reader returned only the title and date, no article body. Their numbers are unread.
- Licence: the model card says "cc-by-4.0" (https://huggingface.co/kyutai/pocket-tts, read 25 Nov 2026), files gated behind accepting conditions. The card's prohibited use section bars "voice impersonation or cloning without explicit and lawful consent". The code licence is MIT (https://raw.githubusercontent.com/kyutai-labs/pocket-tts/main/LICENSE, read 25 Nov 2026). Voice files carry their own licences (separate repo, not read).
- Published speed: "~200ms to get the first audio chunk", "~6x real-time on a CPU of MacBook Air M4" on 2 cores; cloud x86 4 vCPU with T4, about 2.3-2.5x real time on CPU and 6.28x on GPU (README, GitHub page, read 25 Nov 2026).

## 3. Comparisons and leaderboards (dated)

- Artificial Analysis Speech Arena, open-weights page (https://artificialanalysis.ai/text-to-speech/leaderboard/open-weights, read 25 Nov 2026). The page carries no snapshot date and the reader saw the "All" filter, so the list mixes closed and open entries; AA's "release" column is its own. Elo (95% interval): Fish Audio Drama 3 1277 (Oct 2026); Drama 3 Preview 1240; Breeze TTS 2 1229 (Aug 2026); Ming-3.0-tts 1180 (Oct 2026); Phonon 31M English 1109 (Oct 2026); Fish Audio S2 Pro 1103; Step Audio EditX 1101; Voxtral TTS 1093; Magpie-Multilingual 357M 1066; Kokoro 82M v1.0 1061; Maya1 1049; Chatterbox 1021; Zonos-v0.1 1000 (anchor). Pocket TTS and ZONOS3-Mini were not in the list read. Licences not shown. The leaderboard's own order of the open models is a preference ranking, not a check of accent.
- Hugging Face Open TTS Leaderboard, launched 30 Sep 2026 per a third-party review (https://www.creativeainews.com/articles/open-tts-leaderboard-license-cpu-test-2026/, read 25 Nov 2026; the leaderboard itself not read). It ranks 31 models on WER, RTFx and speaker similarity, plus a streaming tab (time to first audio on GPU, CPU for four entries). English top: Kokoro-82M (1.46 WER, 71.15 RTFx on an H200), Fish Audio S2 Pro (1.58 WER), then Supertonic 3, OmniVoice, pocket-tts, Chatterbox, Qwen3-TTS 1.7B, VibeVoice-Realtime; top ten span 1.46 to 1.82 WER. The reviewer's own CPU test (6 vCPU container, AMD Ryzen 7 9700X, PyTorch 2.14.1): pocket-tts first audio median 69 ms on 6 threads, about 71 ms on 2; Kokoro 367 ms; the leaderboard's own CPU column read 272.7 ms and 913.4 ms. The reviewer notes WER and SIM "do not measure how natural a voice sounds". Phonon and ZONOS3-Mini are not named in the excerpt.
- Zyphra's ZTTS2 capability index (vendor, in the HF blog above): ZONOS3-Mini first among open-weight; no numeric scores in the text read. Unverified independently.
- Gradium's leaderboard figures for Phonon (Elo 2098, WER) are on its own card; vendor-reported.
- builderai.tools, 23 Jul 2026 (https://builderai.tools/blog/open-weight-text-to-speech-models-2026, read 25 Nov 2026): about 20 models, no ranking, licence table; predates the window.
- Hugging Face TTS Arena V2 space (https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2): page returned no usable data; its summary text was not trusted. Unreached.

## 4. British regional accent kept from a reference clip

Nothing found that shows a northern English, Scottish or Irish accent kept from a reference clip, for any model in question 1.
- ZONOS3-Mini: accent comes from steering controls on a neutral voice (British ~"Southern English", Australian); the blog does not say whether an accent carries over from a cloned clip, and no regional British accents are named (HF blog, read 25 Nov 2026).
- Ming-3.0-tts: UK_George voice and Sichuanese/Cantonese dialects only.
- Phonon, Pocket, Drama 3, Audio8, Dia2: no accent statement on the pages read.
- Outside the window: Shravani Limited "UK Regional Neural Engine", 7 Feb 2026, repository Shravani-Limited/VideoAvatar-UK-Voice-Engine, claims Manchester, Scouse, Geordie, Scottish, Welsh, Irish, Brummie, zero-shot cloning from 3-10 s, "Open Weights", trained on the CSTR VCTK corpus; no listening test, metric, licence, size or hardware given, only press claims (https://shravani.group/press/regional-ai-voice-models, read 25 Nov 2026). The Hugging Face repo itself was not opened: unverified. Secondary blog claims that Mistral's Voxtral TTS keeps the reference clip's accent were seen only in search results and not read in full; Voxtral's own card says "diverse dialects" without naming any (Mar 2026, CC BY-NC 4.0).

## 5. Not reached or not confirmed

- Kyutai blog bodies for 28 Sep and 20 Oct 2026 (title and date only returned).
- Hugging Face TTS Arena V2 page (no usable content); Hugging Face Open TTS Leaderboard itself (second-hand only); Artificial Analysis snapshot date (not stated; open-weights filter not applied in what was read).
- First try at huggingface.co/Zyphra/Zonos-3-Mini returned HTTP 401 (wrong name); zyphra.com/post/zonos3 returned 404. The ZONOS3-Mini pages above were read afterwards at their right addresses.
- Licence file texts for ZONOS3-Mini, Phonon, Ming, Audio8 (pages state the licence name, not the full text); Pocket's per-voice licences repo; Phonon 40M card.
- Exact release dates: Phonon (about 22 Oct), Drama 3 (1, 13 or 14 Oct), Audio8 (14 Oct), Dia2 (year), Ming (day). The arXiv report for ZONOS3-Mini (ID 2611.16525) was not opened.
- StepAudio 3 Gen, Nari Labs 14 Sep release, Maya2 Native, Apriel Voice, LFM3-Omni, Haru-4B, Liquid-Codec: no primary page read.
- No first-audio figure on a Windows PC with a consumer card was found for any model in 1a-1e; all published numbers are Mac, phone, browser or H100/H200/H800 server figures (Pocket's README adds an x86 T4 VM).
- No search covered every release in the window; the list comes from one aggregator, one leaderboard and several searches, so a model missing here is not shown to be absent.
