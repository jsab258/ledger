# Local checkers for the first sentence: research, 26 October 2026

The owner's order of 26 October 2026 asks for a two-speed check. A small checker on this PC clears only the first sentences it is sure are supported by the speaker's facts. Everything else waits for Haiku.

The gate for the sold game has three parts:
- On the 127 held-out details (85 true, 42 invented), it lets through no more invented details than Haiku does (1 of 42).
- It answers in 0.15 s or less beside the running game, without frame stalls.
- Its licence allows use in a sold game.

Every source was read on 26 October 2026; the numbered list is at the end. "Estimate" means worked out here, not measured. UNVERIFIED means not confirmed in a primary source.

**How the sources were read.** Pages were read through a fetch tool that hands back a model-written digest of each page, not its raw text. Where the tool reported a page was cut short, the rest was read in a second pass (this happened with the MiniCheck paper). Licence wording was asked for word for word. Even so, a digest is not the page itself, so a licence should be re-read on the page before anything ships.

## Bottom line

1. **Only the TinyLettuce family (17M, 32M and 68M parameters) has a realistic chance of 0.15 s on the CPU.** That holds for 300 to 800 tokens of facts, sharing the CPU with Unreal and the Pocket voice. The fit is likely for 17M and 32M; 68M is borderline. All three are MIT, and their training code is published. No one has published a measured CPU time for them, so they must be measured here.
2. **LettuceDetect-base (ModernBERT, 150M) and HHEM-2.1-Open (about 110M) are more accurate on paper.** The estimate for both is 0.2 to 0.6 s on this CPU in full precision. They would meet the 0.15 s limit only with 8-bit (int8) ONNX models, a shorter premise (just the 1 to 3 facts the drafter cites), or the GPU.
3. **MiniCheck's small models are too slow on this CPU (estimate 0.5 to 3 s).** Two of them were partly trained on ANLI, a non-commercial dataset. Bespoke-MiniCheck-7B is non-commercial (CC BY-NC 4.0) and is out.
4. **A small general model (Qwen3 0.6B, Granite Guardian 2B) could meet 0.15 s only on the GPU.** Sharing the GPU with the game has no published measurement.
5. **Anthropic's terms are unclear on training a checker with Haiku's labels.**
   - The Commercial Terms bar only competing models.
   - Anthropic's help article names classifiers as allowed uses, but says training needs written permission.
   - The Usage Policy bars training any AI model on outputs without prior authorisation.

   Recommendation: get Anthropic's written permission before a Haiku-trained checker ships, or make the training labels some other way.
6. **TypeSafe's Jev is a closed, US-hosted cloud model in early access.** It scores 78.7 on the LLM-AggreFact leaderboard. From Switzerland it cannot answer in 0.15 s; the round trip alone is at least about 0.1 s.

**Measure first on the 127:** TinyLettuce (all three sizes in one run), then LettuceDetect-base as an int8 ONNX model, then HHEM-2.1-Open. The reasons are in the "What to measure first" section.

## The PC and what the check competes with

- The project's records name the PC's parts as a Ryzen 5 5600X (6 cores, 12 threads) and an RTX 3080 with 10 GB. The Pocket voice already runs on the CPU (production/research/voice-latency/POCKET-CPU-2026-10-21.md).
- The checker therefore shares the CPU with Unreal's threads and the voice. The GPU belongs to the game.
- ONNX Runtime's CPU speed roughly halves with each doubling of threads, up to 4 to 8 threads, and then stops improving [35]. A checker held to 2 to 4 threads will run slower than the 8-thread figures below.

## 1. The named checkers

### MiniCheck (Tang, Laban and Durrett; EMNLP 2024)

- **What it is.** Sentence-level fact checkers. The input is a document and one claim sentence, and the output is a label plus a probability that the document supports the claim [1][3]. Multi-sentence claims should be split first [1].
- **Variants and sizes.**
  - MiniCheck-RoBERTa-Large: 355M parameters, fine-tuned from AlignScore's RoBERTa-large [2][4].
  - MiniCheck-DeBERTa-v3-Large: about 0.4B. The model card lists 0.4B and the paper's table says 355M; which is right is UNVERIFIED [2][5].
  - MiniCheck-Flan-T5-Large: 770M [2].
  - Bespoke-MiniCheck-7B: 8B on its card, fine-tuned from InternLM2.5-7B-chat [6].
- **Input limits.** Long documents are cut into chunks: about 400 tokens for RoBERTa and DeBERTa, 500 words for Flan-T5. The score is the highest across chunks [2]. Bespoke-7B needs no chunking below 32K tokens [6].
- **Published accuracy** (LLM-AggreFact, balanced accuracy, fixed threshold 0.5) [2]:

  | Model | Balanced accuracy |
  |---|---|
  | MiniCheck-Flan-T5 | 74.7 (75.0 on the leaderboard [10]) |
  | MiniCheck-RoBERTa | 72.7 |
  | MiniCheck-DeBERTa | 72.6 |
  | GPT-4 (for comparison) | 75.3 |
  | Bespoke-MiniCheck-7B | 77.4 (leaderboard) [10] |

  Tuning the threshold barely changed the results: 75.1 for Flan-T5 [2].
- **Speed.**
  - Cost on the 13K-example test set at $0.8 per GPU hour: $0.20 to $0.24 [2]. That is GPU time on an RTX A6000, not CPU time [2].
  - Flan-T5-Large and Bespoke-7B each exceed about 500 documents a minute on one A6000 [6].
  - No CPU figures are published.
- **Fine-tuning.**
  - The synthetic-data generation code and the 14K synthetic examples are published (MIT) [1][7].
  - The repository does not plainly describe a training script, so this is UNVERIFIED [1].
- **Licences.**
  - Code: Apache-2.0 [1]. Small models' weights: MIT [3][4][5].
  - Base models: Flan-T5-Large is Apache-2.0 [43]; DeBERTa-v3-large and RoBERTa-large are MIT [44].
  - Training data:
    - The DeBERTa and Flan-T5 versions add 21K examples from ANLI [2][3][5]. ANLI is Creative Commons Non-Commercial 4.0 [8].
    - The synthetic data was written by GPT-4 [2].
    - The paper says its use of datasets is for research purposes [2].
    - AlignScore (the RoBERTa version's starting point) is MIT, but its 4.7M-example training mix was not checked dataset by dataset (UNVERIFIED) [9].
  - Bespoke-MiniCheck-7B is CC BY-NC 4.0; commercial use means contacting Bespoke Labs [6].
- **Verdict for a sold game.**
  - RoBERTa: **unclear, leaning yes.** The weights are MIT; the AlignScore data mix is unchecked.
  - DeBERTa and Flan-T5: **unclear.** The weights are MIT, but they were trained partly on non-commercial ANLI. A licence on weights does not clean the data they were trained on; this is a judgement, not legal advice.
  - Bespoke-7B: **no**, unless a commercial licence is bought, and an 8B model would not fit beside the game anyway.

### HHEM-2.1-Open (Vectara, August 2024)

- **What it is.** The T5-base encoder with a classification head. The model code builds a T5 encoder-only token classifier and reads the score at the first position [11]. Hugging Face lists 0.1B parameters. The base is Flan-T5-base [11].
- **Input and output.** A (premise, hypothesis) pair goes in; a score from 0 (not supported) to 1 (supported) comes out [11]. The card says the context length is unlimited, against 512 tokens for HHEM-1.0 [11].
- **Published accuracy** (balanced accuracy) [11]:

  | Benchmark | HHEM-2.1-Open | GPT-4 (for comparison) |
  |---|---|---|
  | AggreFact-SOTA | 76.55 | 73.78 |
  | RAGTruth-Summ | 64.42 | 62.62 |
  | RAGTruth-QA | 74.28 | 74.11 |

  HHEM is not on the current LLM-AggreFact leaderboard [10].
- **Speed.**
  - Under 600 MB of RAM in 32-bit floating point, and about 1.5 s for a 2,000-token input on a modern x86 CPU [11]. The blog names the CPU as a Xeon w7-3445 [12].
  - About 0.6 s on an RTX 3090, input length not stated [12].
- **Fine-tuning.** No training code is published. The repository's model file is for running the model only [11]. As a standard T5 classifier it could be fine-tuned with ordinary tools (estimate).
- **Licences.**
  - Weights: Apache-2.0 [11]. Base: Flan-T5, Apache-2.0 [43].
  - Training data: not disclosed anywhere read [11][12].
  - The download is gated: it asks for company and country, so it needs a signed-in Hugging Face account [11].
  - The commercial HHEM-2.3 is available only through Vectara's platform [11].
- **Verdict.** **Yes, probably.** The licence is permissive. The unknown training data is a small residual risk, and the gated download needs the owner signed in.

### LettuceDetect (KR Labs; v1 February 2025, v2 June 2026)

- **What it is.** Token classifiers that mark which words of an answer are not supported. The input is context passages, a question and the answer [13][14]. The output is per-token probabilities or spans with a confidence [13].
- **A trap with the threshold.** The span output only reports spans at 0.5 confidence or above, so a strict threshold needs the per-token output [13].
- **Models.**

  | Model | Size | RAGTruth result |
  |---|---|---|
  | base (ModernBERT-base) [14][19] | 150M | example-level F1 76.07; span F1 55.44 [14] |
  | large (ModernBERT-large) [14] | 395M | example-level F1 79.22; span F1 58.93 [14] |
  | Multilingual (EuroBERT) [13][20] | 210M and 610M | not needed for an English game |
  | v2 mmBERT-base [21][31] | 307M (110M without the word table) | official test example-level F1 74.3 [21] |
  | v2 Qwen3.5-2B [22][23] | 2B | example-level F1 81.8 [23] |
  | LFM2.5-Encoder-350M detector [24] | 0.4B | example-level F1 0.744 [24] |

  For comparison, fine-tuned Llama-2-13B scores 78.7 and a GPT-4 prompt 63.4 [14].
- **Context length.** v1 was trained on up to 4,096 tokens [14]. RAGTruth examples average 801 tokens [14].
- **Speed.** 30 to 60 examples a second on a single GPU (GPU unnamed) [14]. No CPU figures [13][14][19][21][22].
- **Fine-tuning.** Training and evaluation scripts are published, with the exact settings [13].
- **Licences.**
  - Code: MIT [13]. Weights: v1 and EuroBERT models are MIT; the v2 models are tagged Apache-2.0 [20].
  - The LFM2.5 detector is under "lfm1.0", whose terms were not read [24].
  - Base models: ModernBERT is Apache-2.0 [33]; mmBERT is MIT [31]; Qwen3.5 is Apache-2.0 [42]. The EuroBERT base licence was not checked.
  - Training data: RAGTruth's repository is MIT [26]. But its source passages come from MS MARCO, the Yelp Open Dataset and CNN/Daily Mail [27].
    - MS MARCO is for non-commercial research only [28].
    - Yelp's is for educational use [29].
    - RAGTruth's answers were written by GPT-3.5, GPT-4, Llama-2 and Mistral [26].
  - v2 adds a CC-BY-4.0 prose dataset [25]; its injected errors were made with Gemma 4 31B and Qwen 3.6 [23].
- **Verdict.**
  - v1, v2 mmBERT and v2 Qwen-2B: **yes, with a small data-ancestry risk.** The weights are MIT or Apache, but the training passages carry non-commercial terms. The LLM-written answers are a provenance note, not a bar on us (judgement).
  - LFM2.5 detector: **unclear** until its licence is read.

### TinyLettuce (KR Labs, 31 August 2025)

- **What it is.** LettuceDetect retrained on LightOn and Johns Hopkins' Ettin encoders, which use the ModernBERT design [15][30]. Sizes are 17M, 32M and 68M parameters [15].
  - 17M: 7 layers, width 256.
  - 32M: 10 layers, width 384.
  - 68M: 19 layers, width 512 [30].
- **Input and output.** As LettuceDetect, with a 4,096-token limit stated on the 68M card. The 17M card says both 4,096 and 8K [17][18].
- **Published accuracy** (example-level F1) [15][16]:

  | Model | RAGTruth | Their synthetic test |
  |---|---|---|
  | TinyLettuce-17M | 68.52 | 90.87 |
  | TinyLettuce-32M | 72.15 | 88.76 |
  | TinyLettuce-68M | 74.97 | 92.64 |
  | LettuceDetect-base (ModernBERT) | 76.07 | 87.60 |

  A July 2026 outside test of word-by-word detection while text is generated found the 68M model weak: F1 0.29 against 0.36 for LettuceDetect-base [16b].
- **Speed.** Described as real time on a CPU, but with no measured figure, CPU model or thread count anywhere read [15][16][17][18].
- **Fine-tuning.** The recipe is published, and the cards say the models are meant mainly for fine-tuning on small, domain-specific sets [15][17][18].
- **Licences.**
  - Weights and code: MIT [15][20]. Ettin base: MIT, trained on openly published data [30].
  - Training data: RAGTruth (so the same MS MARCO and Yelp ancestry) plus 3,000 synthetic examples written with gpt-oss-120b [16]. The 68M card contradicts itself about whether synthetic data was mixed in [18].
- **Verdict.** **Yes, with the same small data-ancestry risk as LettuceDetect.** Fine-tuning straight from the base Ettin encoder (MIT, open data) on LEDGER labels alone would avoid that risk entirely.

## 2. A small general model as the checker

- **For speed, the best "general" choice is a plain encoder, not a chat model.** Ettin 17M to 150M (MIT, open training data [30]) or ModernBERT-base (Apache-2.0, with ready-made ONNX files including int8 [33]), with a yes/no head trained on LEDGER's labels. This is TinyLettuce without its inherited training data.
- **If a small instruct model is wanted, the best two:**
  1. **Granite Guardian 3.1-2B (IBM, Apache-2.0)** [37].
     - It already checks whether a reply is grounded: context in, reply in, yes or no plus a probability out.
     - On the TRUE benchmark it averages 0.84 AUC [37]. The 8B 3.3 model scores 76.5 on LLM-AggreFact [10].
     - Training data: human-labelled hh-rlhf pairs plus synthetic data [37]. The card asks that it be used only in its yes/no scoring mode [37].
     - Hugging Face lists about 3B parameters [37]. The 3.2-3B-A800M variant scores lower, 0.77 [38].
     - Its use: a zero-shot reference that needs no Claude labels.
  2. **Qwen3-0.6B (Alibaba, Apache-2.0, text only)** with a classification head [40].
     - 0.44B parameters without the word table, 32K context [40].
     - Qwen3.5-0.8B is also Apache-2.0 [41][42], but it carries a vision encoder this job does not need [41].
- **Expected latency.**
  - On this CPU, both are well over 0.15 s. A 7B model reads a 512-token prompt at 23.7 tokens a second on a 5600X [36]. Scaled to 0.44B, that is roughly 380 tokens a second, about 0.8 to 2.1 s for 300 to 800 tokens (estimate). Granite 2B would be several seconds.
  - On the RTX 3080 they would likely take tens of milliseconds (estimate, UNVERIFIED), at the cost of game VRAM and GPU time.

## 3. Which can answer in 0.15 s or less

**Measured numbers found.** None of them is on this PC.

| What | Measured | Source |
|---|---|---|
| ModernBERT-base, CPU, full precision, 8 threads, batch 1 (CPU unnamed) | 0.087 s at 128 tokens, 0.335 s at 512, 0.793 s at 1,024 | [34] |
| ModernBERT-large, same setup | 0.274 s, 1.015 s, 2.117 s | [34] |
| ModernBERT-base on an RTX 4090, large batches | about 148,000 tokens a second | [32] |
| DeBERTa-v3 on the same GPU | about half ModernBERT's speed | [32] |
| LettuceDetect (ModernBERT), one unnamed GPU | 30 to 60 examples a second, about 17 to 33 ms each | [14] |
| HHEM-2.1-Open, 20-core Xeon | about 1.5 s for 2,000 tokens | [11][12] |
| HHEM-2.1-Open, RTX 3090 | about 0.6 s, length not stated | [12] |
| MiniCheck-Flan-T5 or Bespoke-7B, one A6000 | over 500 documents a minute | [6] |
| Enoki's encoder check (earlier note, hardware not stated) | 0.13 s a sentence | production/research/frontier-ai-uses/notes/HE-speech-small-models.md |

**Estimates for this CPU at 300 to 800 tokens of facts.** These scale the ModernBERT-base measurement [34] by each model's size without its word table, and are UNVERIFIED. 8-bit ONNX would be faster. Holding the checker to 2 to 4 threads beside the game would be slower, perhaps 1.5 to 2.5 times [35].

| Model | Estimate | Fits 0.15 s? |
|---|---|---|
| TinyLettuce-17M | about 0.01 to 0.03 s | likely |
| TinyLettuce-32M | about 0.02 to 0.07 s | likely |
| TinyLettuce-68M | about 0.08 to 0.23 s | only with int8 or a shorter premise |
| LettuceDetect-base, v2 mmBERT-base, HHEM-2.1-Open | about 0.2 to 0.6 s | only with int8 plus a shorter premise, or the GPU |
| LettuceDetect-large, MiniCheck-RoBERTa | about 0.5 to 1.6 s | no |
| MiniCheck-Flan-T5 | about 0.6 to 1.8 s | no |
| MiniCheck-DeBERTa | about 1.2 to 3.4 s | no |
| Qwen3-0.6B | 0.8 to 2.1 s | no |
| Granite Guardian 2B | several seconds | no |
| Bespoke-7B | not runnable beside the game | no |

**Three levers.**
1. **Check against only the 1 to 3 facts the drafter cites, not all 300 to 800 tokens.** This cuts time roughly in proportion and can only cause more fallbacks to Haiku, not more leaks (judgement).
2. **Use ModernBERT-family ONNX models in 8-bit (int8).** They already exist for ModernBERT-base [33], and Ettin uses the same design [30].
3. **Keep it on the CPU with a fixed small thread count.** No published measurement was found of a model sharing a GPU with a running game. NVIDIA's game-inference kit says it schedules AI and graphics together but gives no frame figures [46].

**The frame-stall half of the gate must be measured here.** Compare the worst 1% of frame times with and without the checker running, with the voice on.

## 4. Anthropic's terms on training a classifier with Haiku labels

Clauses are paraphrased with their section numbers; one short quotation is kept, to stay within quoting limits.

- **Commercial Terms** (effective 17 June 2025) [47]. These cover the API key.
  - B: the customer owns its Outputs, and Anthropic assigns its rights in them.
  - D.4(a): the customer may not use the Services to build a competing product, including to train competing AI models.
  - D.2: the Usage Policy is part of the Terms.
  - No other clause read limits training a non-competing model.
- **Usage Policy** (the page shows an effective date of 12 November 2026, three weeks from now; the earlier version's wording was not reached) [48].
  - In its section on platform abuse, it forbids users to "Use outputs to train an AI model ... without prior authorization from Anthropic".
  - It applies to API and commercial customers too [48].
- **Help article "Can I use my Outputs to train an AI model?"** (dated 16 March 2026) [49].
  - Its opening says training AI models needs Anthropic's written permission.
  - It then says Outputs may train models that do not compete, and lists sentiment, categorisation, extraction and anomaly-detection classifiers as examples.
  - Its prohibited list includes general chatbots, open-ended text generators, and a bare line, with no qualifier, against using Outputs as training targets for models.
- **Consumer Terms** (8 October 2025), if labels were made through a personal plan [50]. Section 3 bars developing competing products, including training AI models.

**Plain judgement: unclear.** In substance, a checker inside a game looks like the non-competing classifier the help article allows. The wording, though, requires prior written permission: the Usage Policy's bullet and the article's opening sentence. And a fact-checking classifier is trained with Haiku's labels as its targets. The way to remove the doubt is a short written request to Anthropic before a Haiku-trained checker ships. Until then, labels for anything that ships could come from the simulation itself (true facts and edited false ones, as proposed on 7 October) or from people. This is a licence question for the owner.

## 5. TypeSafe's Jev

- **Who.** TypeSafe AI, Inc., San Francisco. The founder is Diogo Almeida, formerly of OpenAI [52][54].
- **What.** A "System One" decision model, launched 15 September 2026 [52].
  - It takes a text "state" plus typed questions and returns choices, scores or a 0-to-1 truth value [53].
  - It writes no text, so its claim that it cannot hallucinate is about the answer format, not about being right [52].
  - Its weights are closed, and there is no self-hosted option in anything read [52].
  - Version jev-1.13.0 is current [55].
- **Accuracy.** "Jev 1.13.0" averages 78.7 on the LLM-AggreFact leaderboard. That is above Bespoke-MiniCheck-7B (77.4) and Claude 3.5 Sonnet (77.2), and level with the 27B "Decider" [10]. The leaderboard shows no date.
- **Speed claims.** 70 to 500 ms end to end, measured from laptops on the US West Coast [52], and 0.114 s on its home page [51].
  - From Switzerland, a fibre round trip to California is at least about 0.1 s (about 18,800 km at about 200,000 km/s; calculation). So 0.15 s is not reachable here.
  - Expect perhaps 0.2 to 0.6 s (estimate, UNVERIFIED): faster than Haiku's 1 s if it holds.
- **Price.** $0.042 per million input tokens, output free. TypeSafe says the price may be subsidised [52][55].
- **Terms.**
  - The public site terms are for personal use of the website, with liability capped at $100 [54].
  - The API terms, privacy policy and data retention were not found.
  - Access is early access, off a waitlist [52].
- **Use to LEDGER.** At most a possible middle tier between the local checker and Haiku. It would be another US cloud dependency inside a sold game, on unseen terms.

## Comparison

"Expected latency here" means this PC's CPU, 300 to 800 tokens of facts; all figures are estimates (section 3).

| Model | Size | Licence verdict (sold game) | Published accuracy | Expected latency here | Fine-tunable |
|---|---|---|---|---|---|
| TinyLettuce-17M | 17M | Yes (MIT; data-ancestry risk) | RAGTruth F1 68.5 | 0.01–0.03 s | Yes, recipe published |
| TinyLettuce-32M | 32M | Yes (as above) | RAGTruth F1 72.2 | 0.02–0.07 s | Yes |
| TinyLettuce-68M | 68M | Yes (as above) | RAGTruth F1 75.0 | 0.08–0.23 s | Yes |
| LettuceDetect-base | 150M | Yes (as above) | RAGTruth F1 76.1 | 0.2–0.6 s; GPU about 17–33 ms | Yes |
| LettuceDetect-large | 395M | Yes (as above) | RAGTruth F1 79.2 | 0.6–1.6 s | Yes |
| LettuceDetect v2 mmBERT | 307M | Yes (Apache; as above) | RAGTruth F1 74.3 | 0.2–0.6 s | Yes |
| LettuceDetect v2 Qwen-2B | 2B | Yes (Apache; as above) | RAGTruth F1 81.8 | GPU only | Yes (low-rank adapters) |
| LFM2.5 detector | 0.4B | Unclear (lfm1.0 unread) | RAGTruth F1 74.4 | 0.4–1.2 s | – |
| HHEM-2.1-Open | about 0.1B | Yes, probably (Apache; data undisclosed; gated) | AggreFact-SOTA 76.6; RAGTruth-QA 74.3 | 0.2–0.6 s | No code; possible |
| MiniCheck-RoBERTa | 355M | Unclear, leaning yes | LLM-AggreFact 72.7 | 0.5–1.4 s | Data code only |
| MiniCheck-DeBERTa | about 0.4B | Unclear (ANLI non-commercial) | LLM-AggreFact 72.6 | 1.2–3.4 s | Data code only |
| MiniCheck-Flan-T5 | 770M | Unclear (ANLI non-commercial) | LLM-AggreFact 74.7–75.0 | 0.6–1.8 s | Data code only |
| Bespoke-MiniCheck-7B | 8B | No (CC BY-NC 4.0) | LLM-AggreFact 77.4 | Does not fit | – |
| Granite Guardian 3.1-2B | about 2–3B | Yes (Apache) | TRUE AUC 0.84 | Several seconds; GPU only | Yes |
| Qwen3-0.6B + head | 0.6B | Yes (Apache) | None for this task | 0.8–2.1 s; GPU only | Yes |
| Jev (cloud) | closed | Service; API terms unseen | LLM-AggreFact 78.7 | Over 0.1 s by physics; claimed 0.07–0.5 s | No |

## What to measure first on the 127

1. **TinyLettuce 17M, 32M and 68M, in one run.**
   - It is the only family likely to pass the speed gate on the CPU, its licence is clean, and its recipe is published.
   - Measure zero-shot first, then fine-tuned. Run one fine-tune from TinyLettuce's weights and one from the plain Ettin encoder, to see what the inherited data is worth.
2. **LettuceDetect-base as an 8-bit ONNX model.** It is the accuracy step up on the same code, so it costs little to add. It passes only if int8 plus the cited-facts premise bring it under 0.15 s.
3. **HHEM-2.1-Open.** It is a different family, with one probability per sentence, which suits a strict threshold. Measuring it zero-shot needs no Claude labels. The gated download needs the owner signed in to Hugging Face.

**Held back:**
- MiniCheck: too slow on the CPU, and ANLI is in its training. Use it only as an offline accuracy reference.
- Bespoke-7B: licence.
- Granite Guardian and Qwen: GPU only, until GPU sharing is measured safe.
- Jev: cloud, and it cannot reach 0.15 s.

**How to read the 127 fairly.**
- Choose each model's strict threshold on a separate tuning set, never on the 127.
- Report three numbers on the 127:
  - invented details cleared: must be 1 or fewer of 42;
  - true details cleared: this is the time saved;
  - the median and the slowest 5% of answer times, beside the running game with the voice on.
- Keep the 127 and any near-copies out of the fine-tuning set.
- 1 of 42 is a small sample. The 95% upper bound on the true leak rate is 12.6% for 1 of 42, and 8.4% even for 0 of 42 (exact binomial, worked here). The 127 can show parity with Haiku but not a low leak rate; a larger invented set would.
- LettuceDetect reads the player's question alongside the facts. It was not checked whether something the player merely asserts counts as support. Test that case (the "Where Winds Meet" failure), or leave the player's words out of the context.

## Questions this raises for the owner (licence)

- **Training on Haiku's labels.**
  - (a) Write to Anthropic for permission first (recommended).
  - (b) Train only on labels made from the simulation and by people.
  - (c) Train on Haiku labels without asking.
- **Inherited training data.**
  - (a) Fine-tune from the plain base encoder only (cleanest).
  - (b) Use TinyLettuce or LettuceDetect weights and accept their inherited MS MARCO and Yelp ancestry (recommended only if (a) is clearly less accurate).

## Unverified / not reached

- No CPU latency for any named checker has been measured on a 5600X, or published at all for TinyLettuce. Every "expected latency here" figure is an estimate scaled from [34], whose CPU is unnamed.
- The 5600X prompt-reading figure [36] is for a 7B model in 2024. A search summary mentioned a faster 62-tokens-a-second result in the same thread, which was not found on the page.
- No measurement found of an AI model sharing a GPU with a running game. NVIDIA's page has none [46].
- Not disclosed or not read:
  - HHEM-2.1-Open's training data; the input length behind its 0.6 s GPU figure.
  - AlignScore's per-dataset training list (generate_training_data.py not read).
  - FactCG's training data. FactCG-DeBERTa-L (0.4B, MIT tag, 75.6 on LLM-AggreFact) is a possible extra candidate [10][45].
  - The EuroBERT base licence; PsiloQA's licence; the full card of the v2 prose dataset (cut short) [25]; the lfm1.0 licence text [24]; Gemma 4's terms for data it generated.
- Conflicting figures:
  - MiniCheck-DeBERTa's size: 355M in the paper, 0.4B on the card.
  - LettuceDetect-base's card says "Large" in its text.
  - TinyLettuce's context length and training data, between cards.
- Not reached:
  - Anthropic's Usage Policy version history; whether the 12 November 2026 version or an earlier one applies today; how "prior authorization" is requested.
  - TypeSafe's API terms, privacy policy and evals site; OpenRouter's Jev page (404); paywalled Medium and Towards AI articles on Jev. Secondary reviews (modemguides, eesel, vktr, techjacksolutions) were seen only as search summaries and are not evidence.
  - Hugging Face page "tinylettuce-ettin-17m-en-v1" (401; the real name is "tinylettuce-ettin-17m-en", which was read).
  - The LLM-AggreFact leaderboard's date and threshold rules (not on the page).
- [16b] is listed below under sources.

## Sources (all read 26 October 2026)

1. MiniCheck repository: https://github.com/Liyan06/MiniCheck
2. MiniCheck paper, full text with appendices: https://arxiv.org/html/2404.10774v2 (abstract https://arxiv.org/abs/2404.10774; v2 1 Oct 2024)
3. https://huggingface.co/lytang/MiniCheck-Flan-T5-Large
4. https://huggingface.co/lytang/MiniCheck-RoBERTa-Large
5. https://huggingface.co/lytang/MiniCheck-DeBERTa-v3-Large
6. https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B
7. https://huggingface.co/datasets/lytang/C2D-and-D2C-MiniCheck
8. ANLI: https://github.com/facebookresearch/anli
9. AlignScore: https://github.com/yuh-zha/AlignScore
10. LLM-AggreFact leaderboard: https://llm-aggrefact.github.io/
11. HHEM-2.1-Open card, raw README, config and model code: https://huggingface.co/vectara/hallucination_evaluation_model
12. Vectara blog, 5 Aug 2024: https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model
13. LettuceDetect repository: https://github.com/KRLabsOrg/LettuceDetect
14. LettuceDetect paper: https://arxiv.org/html/2502.17125
15. TinyLettuce docs: https://github.com/KRLabsOrg/LettuceDetect/blob/main/docs/TINYLETTUCE.md
16. TinyLettuce blog, 31 Aug 2025: https://huggingface.co/blog/adaamko/tinylettuce
16b. LettucePrevent blog, 29 Jul 2026: https://huggingface.co/blog/lebe1/lettuceprevent-blogpost
17. https://huggingface.co/KRLabsOrg/tinylettuce-ettin-17m-en
18. https://huggingface.co/KRLabsOrg/tinylettuce-ettin-68m-en
19. https://huggingface.co/KRLabsOrg/lettucedect-base-modernbert-en-v1
20. KR Labs model list with licence tags: https://huggingface.co/api/models?author=KRLabsOrg&limit=100
21. https://huggingface.co/KRLabsOrg/lettucedect-v2-mmbert-base
22. https://huggingface.co/KRLabsOrg/lettucedect-v2-qwen-2b
23. LettuceDetect v2 paper, 1 Jul 2026: https://arxiv.org/html/2607.00895
24. https://huggingface.co/KRLabsOrg/LFM2.5-Encoder-350M-hallucination-detector
25. https://huggingface.co/datasets/KRLabsOrg/lettucedetect-prose-hallucination
26. RAGTruth repository: https://github.com/ParticleMedia/RAGTruth
27. RAGTruth paper: https://arxiv.org/html/2401.00396v2
28. MS MARCO terms: https://microsoft.github.io/msmarco/
29. Yelp Open Dataset: https://business.yelp.com/data/resources/open-dataset/
30. Ettin encoder card and config: https://huggingface.co/jhu-clsp/ettin-encoder-17m
31. https://huggingface.co/jhu-clsp/mmBERT-base
32. ModernBERT paper: https://arxiv.org/html/2412.13663
33. ModernBERT-base files and licence: https://huggingface.co/api/models/answerdotai/ModernBERT-base
34. Instavar CPU and GPU benchmark, 30 Jul 2026: https://instavar.com/research/ocr/lfm2-5-encoder-vs-modernbert-cpu-gpu-legal-benchmark-2026
35. ONNX Runtime thread scaling: https://github.com/ironblock/sidekick/pull/72
36. llamafile CPU benchmarks: https://github.com/mozilla-ai/llamafile/discussions/450
37. https://huggingface.co/ibm-granite/granite-guardian-3.1-2b
38. https://huggingface.co/ibm-granite/granite-guardian-3.2-3b-a800m
39. Granite Guardian list: https://huggingface.co/api/models?author=ibm-granite&search=guardian&limit=50
40. https://huggingface.co/Qwen/Qwen3-0.6B
41. https://huggingface.co/Qwen/Qwen3.5-0.8B
42. Qwen3.5 list: https://huggingface.co/api/models?author=Qwen&search=Qwen3.5&limit=60
43. https://huggingface.co/google/flan-t5-large
44. https://huggingface.co/api/models/microsoft/deberta-v3-large and https://huggingface.co/api/models/FacebookAI/roberta-large
45. https://huggingface.co/yaxili96/FactCG-DeBERTa-v3-Large
46. NVIDIA In-Game Inferencing: https://developer.nvidia.com/rtx/in-game-inferencing
47. Anthropic Commercial Terms: https://www.anthropic.com/legal/commercial-terms
48. Anthropic Usage Policy: https://www.anthropic.com/legal/aup
49. Anthropic help article: https://support.claude.com/en/articles/12326764-can-i-use-my-outputs-to-train-an-ai-model
50. Anthropic Consumer Terms: https://www.anthropic.com/legal/consumer-terms
51. https://typesafe.ai
52. Jev launch post: https://typesafe.ai/blog/introducing-system-one-models-and-jev
53. https://docs.typesafe.ai/introduction
54. TypeSafe terms of use: https://typesafe.ai/legal/terms
55. LiteLLM on Jev, 20 Sep 2026: https://docs.litellm.ai/blog/typesafe_jev

## Measured, untrained, on the 127 (26 October, evening)

His yes the same afternoon: the five models downloaded (1.45 GB, F:/LedgerTools/hf) and the flan-t5-base tokenizer HHEM loads (2.5 MB, his second yes). Measured by tools/checkers/measure_checkers.py: each checker scores every labelled detail against the speaker's facts; its threshold is set on the 121 tuning details as the most lenient at which no invented tuning detail is cleared, then it is tested once on the 127 held-out details (85 true, 42 invented). Times are the checker alone on this PC's processor, other work running beside it (Unreal and builds), so they are generous to nothing. Raw: production/research/invented-claims/checkers-untrained-2026-10-26.json.

| Checker | Invented cleared (Haiku: 1 of 42) | True cleared, of 85 | Seconds, median |
|---|---|---|---|
| TinyLettuce 17M | 0 | 0 | 0.26 |
| TinyLettuce 32M | 0 | 0 | 0.51 |
| TinyLettuce 68M | 0 | 2 | 1.36 |
| LettuceDetect base | 1 | 9 | 2.59 |
| HHEM-2.1-Open | 3 | 19 | 2.12 |

**None passes untrained.** At a threshold safe enough for his bar they clear almost no true detail (the most useful, LettuceDetect base, clears 9 of 85 at Haiku's 1 of 42), and none comes near 0.15 s on the processor; HHEM lets 3 through even at its tuned threshold. So the order's second step, training on LEDGER's own first sentences, is the only route left among the open checkers; the smallest (TinyLettuce 17M, 0.26 s here untrained and unbatched) is the candidate for speed, and its training waits on Anthropic's answer (his pick: ask first; the request drafted, ANTHROPIC-REQUEST-2026-10-26.md). Not yet measured: the times beside the running game, and on the graphics card.
