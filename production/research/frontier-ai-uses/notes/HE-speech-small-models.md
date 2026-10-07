> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand E: live talk (LEDGER problem 1), July to October 2026

Helper report, 7 October 2026. Web research only, about 30 minutes. Nothing was run on LEDGER's PC, so every LEDGER-side latency figure below is either LEDGER's own measurement (from the brief) or my inference [I].

Marks: [SHOWN] = evidence I read (released code/weights page, shipped product, or a paper's own reported experiment, which is still the authors' report); [CLAIMED] = vendor or press claim only; [ABS] = arXiv abstract read through the API (authors' claim); [SS] = search summary only, a lead and not evidence; UNREACHED = could not be opened; [I] = my inference.

Most vendor and press hosts (openai.com, Google, Hugging Face, NVIDIA NGC, artificialanalysis.ai, games press, Steam) were unreachable. Everything about closed products below is therefore [SS]. arXiv (API and PDFs through export.arxiv.org), GitHub READMEs and Anthropic's own docs were reachable.

---

## 0. Bottom line

1. **The check, not the voice, sets the floor, and nothing new removes it for free.** No new speech-to-speech model can keep a check before the first sound. Every full-duplex design published or shipped in the period (OpenAI GPT-Live-1 [SS], SALMONN-duo [ABS], Qwen-Audio-Agent [ABS], Context Spanning [ABS]) works the same way: a fast front model talks at once and a slower back end brings the facts later. That moves the problem. The first words are spoken unchecked.
2. **The likeliest route under 2 s: make the first sentence's check local and narrow, and keep Haiku for the rest.** Have Sonnet name the fact IDs it is about to use before it writes sentence 1. Check those IDs against the simulation in code, which takes no measurable time. Then check sentence 1 against only those 1 to 3 facts with a small local encoder: a rule pass on names, numbers and times, plus an entailment model. Published small checkers report about 0.1 s per sentence, measured on the authors' own hardware, not on a CPU like LEDGER's (Enoki encoder 0.13 s per sentence [SHOWN, paper]; HallDetect uses a DeBERTa-v3-large verifier of 435M parameters in under 1 GB of VRAM [SHOWN, paper]; TinyLettuce 17M to 68M "real-time on CPU" [SHOWN, README, background Aug 2025]). Sentences 2 onward keep today's Haiku check, which runs while sentence 1 plays. If the local check fails, the line falls back to today's path, so the worst case is today's latency. From LEDGER's own numbers this would give about 1.0 to 1.4 s with a streaming cloud voice, and still about 2.5 to 3 s with today's local voice [I, arithmetic in section 1].
3. **"That's all I know" is mostly a retrieval and abstention question, not a wording one.** It should be measured in two parts: (a) was the answering fact in the prompt at all? (b) given that it was, did the model still abstain? A forced step that "picks the facts first" makes every abstention an explicit, auditable decision (section 6).
4. **Licence trap for distillation.** The Anthropic Consumer Terms (effective 8 October 2025), which cover Claude Code on his Max plan, forbid using the Services "To develop any products or services that compete with our Services, including to develop or train any artificial intelligence or machine learning algorithms or models" [SHOWN, anthropic.com/legal/consumer-terms]. The Commercial (API) Terms bar only "train competing AI models" [SHOWN]. Training LEDGER's own checker on Claude-written examples is therefore a licence question for Jafar. Training it on examples generated from the simulation by code, or by a locally run Apache-2.0 model, avoids the question [I].
5. **Model lifecycle (checked today).** Claude Haiku 4.5 is Active, "Not sooner than October 15, 2026" for retirement, with no deprecation notice yet. Anthropic gives at least 60 days' notice, so it is safe until at least about mid-December 2026 [SHOWN, platform.claude.com model deprecations]. The current Sonnet is **Sonnet 5.5** (claude-sonnet-5-5, $2 / $10 per million tokens). Sonnet 5 is still Active ("legacy" list), with retirement not sooner than 30 June 2027 [SHOWN].

---

## 1. Where the 2 seconds go (arithmetic from LEDGER's own figures) [I]

Measured by LEDGER (from the brief):
- About 2.4 s with streaming cloud TTS.
- The claim check of sentence 1 takes 1.27 to 1.34 s.
- About 4.0 s at best with local Chatterbox Nano.

What follows from those numbers:
- **Sonnet plus network to the first full sentence is about 0.8 to 1.0 s** (2.4 − 1.3 − about 0.1 to 0.3 s of cloud TTS first audio).
- **Local TTS first audio beside the game is about 1.7 to 1.9 s** (4.0 − 1.3 − 0.9).

What that means for each option:
- **Replace the 1.3 s check with a local check of about 0.05 to 0.15 s:** cloud TTS path about 1.0 to 1.4 s, inside the target. Local TTS path about 2.6 to 2.9 s, still outside it. For the local voice, a faster first audio is needed as well, for example synthesising only the first clause, or a smaller CPU voice.
- **Start work before the player's line ends** (retrieval and prompt assembly speculatively, as in the papers in section 4c): saves the retrieval time and some of the time to the first token. The papers report 19% (Never Stop Thinking [ABS]) and 5.79 s → 4.60 s median time to first audio (Android tool agent [ABS]).
- **Prompt caching of each character's stable memory** (Anthropic prompt caching; put changing memories at the tail): lowers time to the first token for long prompts. Anthropic's latency page lists only model choice, shorter prompts and outputs, and streaming [SHOWN]. I have no measured caching figure for Sonnet 5.x [I].

None of these numbers is from the real path. They are arithmetic on LEDGER's measurements and must be measured before anything is concluded.

---

## 2. Speech-to-speech and full-duplex models

### 2a. Closed, cloud

| Item | Who / date | What is claimed | Mark |
|---|---|---|---|
| GPT-Live-1 | OpenAI, in the API from 10 Sep 2026 | Full-duplex speech-to-speech. Decides "many times per second" whether to speak, listen, pause, interrupt or call a tool. Hands reasoning to a separate back-end model and "keeps talking to you in the meantime". $0.05 per minute for the front voice layer, billed per second; the back end costs extra. Endpoint v1/live/sessions. | [SS]; openai.com and developers.openai.com UNREACHED |
| gpt-realtime-2.1 and 2.1-mini | OpenAI, 6 Jul 2026 | Reasoning and tool use added. p95 latency at least 25% lower through caching. Mini prices per million tokens: text $0.60 in / $2.40 out, audio $10 in / $20 out. | [SS]; community.openai.com UNREACHED |
| Gemini 3.8 Live (15 Sep 2026), Gemini 3.8 Flash TTS (22 Sep 2026) | Google | Native-audio live model with function calling, under 500 ms end to end. Developer forum threads on the older 2.5 native-audio model report 2.2 to 5.4 s processing, and some 10 to 15 s stalls. | [SS] only |
| Eleven v4 | ElevenLabs, 28 Sep 2026 | TTS, top of the Artificial Analysis Speech Arena (Elo 1316) | [SS] |
| "Interaction Models" | Thinking Machines Lab | A "200 millisecond latency budget" | [SS], lead only |

**LEDGER angle**
- All of these are cloud services and new paid accounts (Jafar's yes needed). None runs on the PC.
- GPT-Live-1's design matches what LEDGER cannot accept: the front model speaks before the facts are checked. Only a front model confined to non-factual turn-taking would keep the check. That is close to an "opening", so it is a scope question for Jafar, not mine to decide.
- Cost: about $3 per hour for GPT-Live-1's front layer plus the back end [SS arithmetic]. That fits the $5-per-evening cap only for short sessions. I could not verify Realtime audio-token rates, so I give no per-hour figure for gpt-realtime-2.1-mini.
- Voices are the vendor's. Whether a cast British 1990 voice is possible, and the cloning and consent terms, are unverified (UNREACHED).
- Output terms are OpenAI's and Google's (not read).

### 2b. Open weights

| Item | Who / date | Facts | Mark |
|---|---|---|---|
| NemotronLabs VoiceChat-11B | NVIDIA, about 3 Aug 2026 | First open full-duplex model with tool calls: a separate output channel emits tool calls while the speech goes on. About 450 ms on smooth turn-taking and 480 ms on user interruption (model card). BFCL-v3 average 56.1% (argument accuracy 44.2%). **Licence OpenMDW v1.1, "research purposes only"**. Needs a GPU of at least 80 GB (A100, H100 and so on, through vLLM). | [SS]; NGC and Hugging Face UNREACHED |
| PersonaPlex-7B | NVIDIA, paper arXiv 2602.06053 (Feb 2026, background) | Built on Moshi. Persona set by a text prompt, voice by an audio embedding (fixed voice set NATF0-3, NATM0-3 and so on). Facts go into the prompt as plain text ("Information: ..."). Partly trained on the **Fisher English Corpus (LDC)**. CUDA-oriented, with a `--cpu-offload` option. Model licence must be accepted on Hugging Face. | [SHOWN, GitHub README]; licence text UNREACHED |

**LEDGER angle**
- Neither runs usefully on an RX 6700 10 GB under Windows: CUDA plus 7B to 11B in a speech loop, beside the game.
- VoiceChat's licence bars a sold game.
- PersonaPlex's training on LDC Fisher data is a dataset-licence question, and grounding is prompt-only with no check.
- Exclude both.

### 2c. Research in the period (all [ABS] unless marked)

- **RePlay** (Udupa, Kumar, Folmsbee; 25 Sep 2026, arXiv 2609.31588) [SHOWN, paper read].
  - A PersonaPlex model cut down to layer 15. Instead of generating, it retrieves and plays **pre-recorded authored lines** from its hidden state as the user speaks.
  - Median 383 ms against 2.6 s for an ASR → commercial LLM cascade (6.8× faster). p10 to p90 spread only 106 ms.
  - Dialogue quality was similar (judge Q 3.76 vs 3.90). Exact-line choice was worse (R@1 0.35 vs 0.52).
  - Users preferred it in 63% of ratings against 12% for a fast small-LLM cascade (N=14).
  - 300 lines for one character; trained on 8 A100 40 GB.
  - LEDGER angle: shows that selecting authored lines beats a small LLM on speed and quality. But it covers only a fixed line set, so it cannot speak dynamic simulation facts ("Ron saw you at the quay at 9") without generated glue. Its evaluation used non-commercial Breeze-TTS-2. Not usable as is. It is evidence for "selection plus glue" (section 6).
- **SALMONN-duo** (Yu, Wang, Chiba, Chen et al.; 28 Sep 2026, 2609.34247): a fast full-duplex front model learns when to answer directly and when to hand off to a slow LLM agent. "Knowledge-boundary-aware training avoids unnecessary system 2 invocations". No latency numbers in the abstract.
- **Context Spanning** (Go et al.; 27 Sep 2026, 2609.33443): retrieved text is injected as plain text into a running duplex model through chunked prefill "inside the real-time frame budget". This is the mechanism that would let a duplex model see simulation facts. There is still no gate before speech.
- **Qwen-Audio-3.1-Realtime / Qwen-Audio-Agent** (Qwen team, per the titles; 21 Sep 2026, 2609.25176, 2609.25195): tool use; a foreground-background harness; "M²-OPD" on-policy distillation from several teachers. Task success 78.4% → 82.0% on a τ-Voice adaptation. Weights not established (I could not check the Qwen pages).
- **CharDuplex** (28 Sep 2026, 2609.34461): persona-consistent full-duplex model built from GLM-4-Voice.
- **RelayS2S** (Mar 2026, background, 2603.23346; code at github.com/mailong25/relays2s):
  - How it works: a duplex model drafts a short prefix; a cascaded LLM continues from it; a "lightweight learned verifier" decides whether the prefix is committed.
  - Results: P90 first chunk 81 ms vs 1,006 ms, excluding TTS and network; real dialogues −479 ms on average.
  - LEDGER angle: the closest published pattern to "fast draft, verified before speech". Here the verifier judges whether the prefix fits, not whether its facts are true.
- **"Building Enterprise Realtime Voice Agents from Scratch"** (Mar 2026, background, 2603.05413): self-hosted Qwen3-Omni full speech pipeline took about 146 s per turn in Transformers. Cascade with ElevenLabs measured 755 ms time to first audio. Supports the view that self-hosted end-to-end speech is not ready.

---

## 3. Newest low-latency streaming TTS for an RX 6700 or a 6-core CPU

Not re-researched: Chatterbox Nano, Pocket TTS, Sopro, VoxCPM2, ElevenLabs Flash v2.5, Inworld TTS-2 Flash, Cartesia, Deepgram Aura-2.

| Model | Who / date | Size, runtime | Latency evidence | Licence | Runs here? |
|---|---|---|---|---|---|
| X2Streaming-TTS | X-Square-Robot; code 6 Aug 2026, weights 7 Sep 2026; arXiv 2608.18661 | 1.7B, on Qwen3-TTS through its "Qwen3TTS-Streaming" engine (ONNX/TensorRT) | Strict token-level streaming from incoming text: median time to first audio token **15.8 ms** for one request, 260.8 ms at 128 concurrent (GPU not named in the text I grepped) [SHOWN, paper] | Code MIT [SHOWN]; weights' licence on Hugging Face UNREACHED (Qwen3-TTS is Apache-2.0 [I, background]) | TensorRT path is NVIDIA-only. A 1.7B voice beside the game on 10 GB AMD is doubtful [I]. Of interest for the idea: it speaks from text tokens as they arrive, without waiting for a sentence. |
| Chatterbox-Flash | Resemble AI; paper May 2026 (background), arXiv 2605.30748 | Block-diffusion decoder fine-tuned from Chatterbox | "Time-to-first-packet on par with streaming AR systems and substantially lower real-time factor" [ABS] | MIT [SHOWN] | README defaults to CUDA (SDPA, FlashInfer). On AMD unknown. |
| Chatterbox-Nano (LEDGER's current voice) | Resemble AI | 110M | README: "3x faster than realtime on 8 CPU cores", the same single-step decoder as Turbo [SHOWN] | MIT, Perth watermark in every output [SHOWN] | Already in use |
| MOSS-TTS-Nano | OpenMOSS / MOSI.AI; released 10 Apr 2026, ONNX CPU build 17 Apr 2026 (background) | 0.1B, ONNX Runtime CPU, no PyTorch, voice cloning, "Realtime Streaming Decode", streaming "on a 4-core CPU" | No first-audio figure given [SHOWN, README] | Apache-2.0 LICENSE file [SHOWN] | Yes, CPU. A candidate for the CPU path if its first audio beats Nano. Needs a British accent check by ear. |
| Supertonic 3 | Supertone; 29 Apr 2026 (background) | 99M, ONNX, CPU | "fast on CPU" chart, no number in the text [SHOWN] | Code MIT. **Weights OpenRAIL-M** (use restrictions that must pass to users [I]). **Repo archived, no support.** No local voice cloning: custom voices need Supertone's hosted Voice Builder. | Runs on CPU, but casting a voice needs their service. Weak fit. |
| Breeze TTS 2 | BreezeBlue, 25 Aug 2026 | 3B, CUDA | under 40 ms on H100 | **Research and Non-Commercial** | Excluded [SS] |
| Gemini 3.8 Flash TTS, Eleven v4 | Sep 2026 | cloud | unknown | vendor terms | Cloud. Same floor problem as the cloud voices already tried [SS]. |

**LEDGER angle.** No new local voice changes the floor while the check takes 1.3 s. Once the first-sentence check is local (section 0), the local voice becomes the bottleneck at about 1.7 to 1.9 s [I]. The cheapest local test then is MOSS-TTS-Nano ONNX CPU against Chatterbox Nano, measured on first-clause synthesis. Speaking the first clause, not the whole first sentence, is the main lever for local first audio [I].

---

## 4. Small models as fast checkers; constrained and speculative generation

### 4a. Checkers that read a claim against evidence

| Item | Who / date | What | Speed | Licence | LEDGER fit |
|---|---|---|---|---|---|
| **Enoki** | Rykov et al. (s-nlp); 1 Sep 2026, arXiv 2609.00581; code github.com/s-nlp/Enoki | Extracts relation triples from each sentence, checks each against evidence, maps failures back to spans. LLM, encoder or rule extractors behind one interface. | Per sentence on FactCheck-Bench: **encoder 0.13 s** (0.06 extract + 0.07 verify), **rule 0.11 s**, against 11.95 s for the Claimify LLM pipeline [SHOWN, paper Table 10]. Hardware not stated ("relative comparison"). | No LICENSE file found (404) → **licence unknown** | Its shape (triples checked against a fact list) matches LEDGER's simulation facts closely. Usable only once the licence is known, or as a design to rebuild. |
| **HallDetect** | Oukelmoun, Semmar, De Chalendar; 6 Aug 2026, arXiv 2608.05823 | Split into atomic claims (by a quantised local LLM), then a **DeBERTa-v3-large (435M) entailment model** checks each claim against source chunks. One confidently contradicted claim flags the answer. | Verifier under 1 GB VRAM, one forward pass per claim-chunk pair, at most 31 per claim [SHOWN, paper]. No wall-clock figure found. | Code link not found in the abstract | Supports "one contradiction blocks the line". The split step is the slow part; LEDGER can avoid it if Sonnet names its facts itself. |
| **LettuceDetect v2 / TinyLettuce** | KR Labs; v0.2.0 22 Jun 2026, 0.2.2 5 Jul 2026; TinyLettuce Aug 2025 (background) | Marks unsupported tokens or spans given context. v2 adds `lettucedect-v2-mmbert-base` (fast encoder) and `lettucedect-v2-qwen-2b`. TinyLettuce Ettin encoders are 17M / 32M / 68M. | TinyLettuce "real-time on CPU" (no figure in the docs). Span-F1 on their v2 test: 0.642 (mmBERT) and 0.689 (Qwen-2B) [SHOWN, README] | **MIT** code and models [SHOWN] | The best-licensed base to fine-tune on LEDGER's own facts. Its synthetic data was made with GPT-5-mini or gpt-oss-120b [SHOWN]. Using their released models is fine [I]; it is a dataset-provenance note, not a NoAI mark. |
| "Small Encoders Can Rival Large Decoders in Detecting Groundedness" | Chandar lab, Jun 2025 (background), 2506.21288 | Checks *before* generating whether the query is answerable from the document at all. RoBERTa / NomicBERT about equal to Llama3-8B / GPT-4o, "orders of magnitude" faster [ABS] | | code public | Could decide "this person knows something about that" before Sonnet runs. That is the other half of "that's all I know". |
| SingProbe (Aug 2026, 2608.30703), D-Score (Jul 2026), MoE signals (Aug 2026) | various | Detect hallucination from the model's own hidden states during generation | | | Needs a local model's internals. **Not usable with Claude.** |

**What a LEDGER checker would look like** [I]: a two-part local check for sentence 1 only.
1. **Rules (about 0 ms):** every cited fact ID belongs to this character's knowledge in the simulation. Every person, place, time, number and object named in the sentence appears in those facts or in the character's known-entities list. This is Enoki-RULE in spirit, and it catches the commonest invented fact, a wrong name, time or place.
2. **Entailment (estimated 20 to 150 ms on the 5600X, to be measured):** a small encoder (TinyLettuce-class 17M to 68M, or mmBERT-base) fine-tuned on LEDGER's own data decides whether the sentence is entailed by the 1 to 3 cited facts. Anything uncertain goes back to Haiku.

**Training data without the terms problem:** generated from the simulation by code.
- True sentences: templates over real facts.
- False ones: swap the person, time, place or object; reverse who saw whom; assert things the character could not know; accept the player's claims as fact (the Where Winds Meet failure, section 5).
- Optionally paraphrased by a locally run Apache-2.0 model.

**Safety bar:** on LEDGER's existing bench plus an adversarial set, the local check must miss no more false claims than Haiku does today. Until it passes, Haiku stays authoritative for every sentence.

### 4b. Constrained decoding against a fact table

Claude structured outputs use constrained decoding from compiled grammars, on Sonnet 5.5, Sonnet 5 and Haiku 4.5 among others. `enum` values are supported (capitalisation not guaranteed). Streaming works [SHOWN, platform.claude.com structured-outputs].

But: "The first time you use a specific schema, there is additional latency while the grammar compiles". The cache lasts 24 h, and changing the schema structure invalidates it [SHOWN]. A per-turn enum of the character's fact IDs would recompile on every turn [I].

**Fit:** a *fixed* schema, `{"facts": [string matching ^F[0-9]+$], "line": string}`, with IDs then looked up in code. The grammar guarantees the shape. The lookup guarantees the IDs exist and belong to this character. The wording still needs the check in 4a. Streaming lets LEDGER read the `facts` array before `line` starts [I].

### 4c. Speculative and cascaded generation (shortening time to the first sentence)

- **Hiding Tool Latency ... through Speculative Execution** (Jung, Park, Lee, Park et al.; 6 Oct 2026, 2610.07641) [ABS]: guesses tool calls from partial speech and runs them early; worst case bounded by the serial pipeline. Median time to first audio 5.79 → 4.60 s on Android.
- **Never Stop Thinking** (Li, Shi; Jul 2026, 2609.17416) [ABS]: "thinking while listening" with an unmodified text model cut live-pipeline latency by 19% overall. Also warns that LLM judges reward visible reasoning: a judged gain reversed sign under an independent judge. That is relevant to LEDGER's own blind judging.
- **Endpoint Anticipation** (Jun 2026, 2606.13450) [ABS]: predicts the end of the speaker's turn up to 2.56 s early, so the LLM and TTS can start on partial input.
- **Voice-Light** (Braun; 17 Sep 2026, 2609.20995; code github.com/BertilBraun/Voice-Light) [ABS]: open full-duplex *cascade*. Median 758 ms from end of speech to first server audio over 36 measured turns, "an instrumented case study". Uses "audible bridge speech" during tool calls, which LEDGER's no-openings rule likely forbids.

**LEDGER angle:** while the player is still typing or speaking, run the simulation retrieval and build the prompt (milliseconds of work, but it takes them off the critical path). Optionally start Sonnet on the partial line and drop it if the final line differs. Cost: wasted tokens on dropped drafts, within the paid key's cap [I].

---

## 5. Games that shipped live LLM characters (2025-2026)

Almost everything here is [SS]. Steam, the games press and the studios' pages were UNREACHED, and I found **no measured latency figures from any shipped game.**

- **Where Winds Meet** (NetEase / Everstone, shipped 2025) [SS]: LLM chat NPCs. Players **skipped quests by asserting events in brackets** ("(Suddenly, her two brothers appear)"; "hands you the missing object"), and by repeating the NPC's line until it declared the quest complete. LEDGER angle: a grounding failure in which **the player's claim is taken as fact**. LEDGER's check must reject sentences that endorse facts only the player asserted. That belongs in the adversarial test set.
- **inZOI Smart Zoi** (Krafton, NVIDIA ACE, 2025) [SS]: an on-device 0.5B Mistral-NeMo-Minitron model on RTX 3060 / 4060 class GPUs with 8 GB. It drives behaviour, not open voiced conversation. NVIDIA-only.
- **Whispers from the Star** (Anuttacon, Aug 2025) [SS]: one voiced character, all server-side, with filters "to keep responses lore-friendly". No numbers found.
- **Dead Meat** (Meaning Machine) [SS]: interrogation game with about 15 LLM suspects; session-only memory. Release status unverified.
- **Wanderfolk** (Kinetic Sky, announced for 2026) [SS, vendor's own site]: villagers remember the player. Memories are summarised, embedded and retrieved with pgvector. Claims 1 to 3 s of cloud latency. Its site was UNREACHED.
- **Ubisoft "Teammates"** (Nov 2025) [SS]: voice-commanded AI squadmates, a research playtest with a few hundred players.
- Respan / Cinevva industry guides (2026) [SS] say that lore contradiction is the commonest failure players report, and that cloud round trips of 1 to 2 s "read as a stall". These are secondary write-ups, not evidence.
- **Research prototype: "Long-Lived Characters, Local Inference"** (Zimu Xu, 16 Sep 2026, 2609.18935) [ABS]: updates a local NPC's memory in place in a quantised Qwen hybrid model without re-reading its whole life. It notes that "a fluent but incorrect account of who owns an item ... can corrupt the input to otherwise deterministic rules". It needs a local LLM. The Claude analogue is to keep each character's stable memory as a cached prompt prefix and append changes at the end [I].

**Conclusion:** no shipped game in reach of this research shows a verified-before-speech design with measured first-sound times. LEDGER's check-then-speak design appears to be stricter than what shipped games use [I, from absence of evidence; not proof].

---

## 6. Grounded answers instead of "that's all I know" (23-25 of 48)

1. **Split the measurement first** [I]. For each of the 48 bench questions, log whether the answering fact was in the prompt.
   - If it was missing: retrieval failed, and prompt changes cannot help. This fits the note that prompt-only fixes failed.
   - If it was present and the character still abstained: the abstention policy is too strict.

   "Rethinking Faithfulness in LLMs: A Pairwise Context-Sensitive Perspective" (6 Oct 2026, 2610.07894) [ABS] makes the same point: score each question twice, once with sufficient context and once without, so that over-abstention and over-answering are measured together. LEDGER's bench should gain the "without" twin of every answerable question.
2. **Pick the facts, then word them** [I, supported by Enoki / HallDetect design and RePlay's results]. Use a forced first step: "choose 0 to 3 facts from this list that bear on the question". Sonnet's structured output (4b) carries the IDs. An empty list then becomes an explicit decision that can be logged and audited. The wording step gets only the chosen facts plus the voice sheet. The check then has an exact target, which is what makes a fast local check possible (section 4a).
3. **Retrieval over the simulation's memory.** Rank by entity overlap with the question (people, places, objects, times), recency and salience, not only embeddings. Wanderfolk's claimed setup (summaries, embeddings, cosine) is the baseline that shipped [SS]. A pre-generation answerability classifier (the 2025 groundedness encoders) can say "this character does hold something relevant" before Sonnet runs [I].
4. **Authored lines plus generated glue.** RePlay shows that retrieving authored lines beats a small LLM on speed and quality [SHOWN]. LEDGER's facts are dynamic, so the authored part would have to be *templates with slots filled from the fact*, and Sonnet writes only the connecting phrase. Whether a slot template counts as a "prepared opening" is Jafar's call; I would treat it as scope, not decide it.
5. **The Where Winds Meet lesson:** "grounded" must mean grounded in the simulation, not in what the player said.

---

## 7. Licences and terms, in one place

- **Anthropic Consumer Terms** (8 Oct 2025): no use of the Services "to develop or train any artificial intelligence or machine learning algorithms or models" (worded as part of "products or services that compete"). It is ambiguous whether this covers a small checker for a game → **question for Jafar** if any training data is written by Claude through his Max plan. Commercial Terms (API) bar only "competing AI models" [SHOWN]. The paid key is reserved for live play under LEDGER's own rules, so it is not a way round this.
- **LettuceDetect / TinyLettuce:** MIT [SHOWN]. **Enoki:** licence not found. **MOSS-TTS-Nano:** Apache-2.0 [SHOWN]. **Chatterbox / Chatterbox-Flash:** MIT [SHOWN]. **X2Streaming-TTS:** code MIT [SHOWN], weights UNREACHED. **Supertonic 3:** OpenRAIL-M weights plus archived repo [SHOWN]. **Breeze TTS 2:** non-commercial [SS]. **NVIDIA VoiceChat-11B:** research only [SS]. **PersonaPlex:** NVIDIA model licence (text UNREACHED), with Fisher/LDC training data.
- **NoAI:** none of these are Fab items, and none I read bars AI use. Licences with use restrictions (OpenRAIL-M) must be carried into the game's terms [I].
- **Territory:** none of the licences I read has an EU, UK or Switzerland exclusion. The Hugging Face model-card licences were UNREACHED, so this cannot be confirmed for those.

---

## 8. What I would try, cheapest first (all to be measured on the real path)

1. **Instrument the bench** (no new tools): for each question, log fact present or absent, abstained or not, Sonnet time to the end of sentence 1, check time, and TTS first audio. Add the "without context" twin and a Where-Winds-Meet-style adversarial set.
2. **Fixed-schema structured output** from Sonnet: `facts` IDs, then `line`. Deterministic ID and entity rules on sentence 1. Measure what fraction of Haiku's rejections the rules alone already catch.
3. **Local entailment check for sentence 1:** an MIT TinyLettuce or mmBERT encoder through ONNX on the CPU (not the GPU, which the game and voice share). Fine-tune it on simulation-generated true and false sentences, not Claude output. Keep Haiku as fallback and for sentences 2 onward. Pass bar: misses no more false claims than Haiku on the bench.
4. **Speculative retrieval and prompt assembly** while the player is still typing or speaking.
5. Only then **the voice:** MOSS-TTS-Nano ONNX CPU against Chatterbox Nano, on first-clause synthesis, judged by ear for accent.
6. **Not recommended now:** full-duplex speech-to-speech (open ones are research-only or 80 GB / CUDA; closed ones speak before any check and are new paid accounts); retrieval-only playback of authored lines (RePlay-style) for a world with changing facts.

---

## 9. Unreached sources (nothing concluded from them)

openai.com, developers.openai.com, community.openai.com (GPT-Live-1, gpt-realtime-2.1); Google AI and Vertex docs and forum (Gemini 3.8 Live and TTS); huggingface.co (all model cards and licences, including PersonaPlex, VoiceChat, X2Streaming weights, TinyLettuce cards); catalog.ngc.nvidia.com; artificialanalysis.ai; dev.to; eesel.ai; futureagi.com; wanderfolk.ai; arcanumrpgs.com; Steam; games press; news.ycombinator.com; kyutai.org; bentoml.com; arxiv.org HTML (the PDFs came through export.arxiv.org).

## Sources read

- Anthropic: platform.claude.com/docs/en/about-claude/models/overview; /about-claude/model-deprecations; /test-and-evaluate/strengthen-guardrails/reduce-latency; /build-with-claude/structured-outputs; anthropic.com/legal/consumer-terms; anthropic.com/legal/commercial-terms.
- arXiv papers (full text): 2609.31588 RePlay; 2609.00581 Enoki; 2608.05823 HallDetect; 2608.18661 X2Streaming-TTS.
- arXiv abstracts: 2609.34247, 2609.33443, 2609.25176, 2609.25195, 2609.34461, 2609.35115, 2603.23346, 2603.05413, 2605.30748, 2610.07641, 2609.17416, 2606.13450, 2609.20995, 2609.18935, 2610.07894, 2506.21288, 2608.30703.
- GitHub READMEs and licence files: NVIDIA/personaplex, KRLabsOrg/LettuceDetect (README, docs/TINYLETTUCE.md, LICENSE), s-nlp/Enoki, OpenMOSS/MOSS-TTS-Nano (README, LICENSE), supertone-inc/supertonic, resemble-ai/chatterbox, resemble-ai/chatterbox-flash, X-Square-Robot/X2Streaming-TTS.
- Search summaries only: GPT-Live-1, gpt-realtime-2.1, Gemini 3.8, Eleven v4, Breeze TTS 2, NVIDIA VoiceChat-11B, Where Winds Meet, inZOI, Whispers from the Star, Dead Meat, Wanderfolk, Ubisoft Teammates, Thinking Machines.
