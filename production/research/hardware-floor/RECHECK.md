# RECHECK: what arXiv 2511.10277 actually establishes

STATUS: SPEC (research recheck). Branch `research/hardware-floor`, added on top
of `cdca0e1`. Written 2026-09-19 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item, no decision record, no
floor written.

## 0. How the paper was read

`arxiv.org` is still refused by the gateway (403 to CONNECT).
`export.arxiv.org` is not, and it is arXiv's own programmatic mirror, so the
paper was read there: the abstract listing (200, 41,477 bytes) and the LaTeXML
full text at `export.arxiv.org/html/2511.10277v1` (200, 124,231 bytes, 41,474
characters of extracted text). The PDF was also downloaded (1,247,450 bytes, 8
pages) and not used, because no text extractor in this container works.

WHAT WAS NOT READ: the figures. Every number below comes from the paper's PROSE,
which quotes its own figures, not from the plotted values. Figures 2 to 12 are
images and I did not open them. That matters for precision, not for direction:
where the prose gives a number I give the prose's number.

Full identification: arXiv:2511.10277v1 [cs.AI], 13 Nov 2025, "Fixed-Persona
SLMs with Modular Memory: Scalable NPC Dialogue on Consumer Hardware", Martin
Braas Andreasen and Lukas Esterle, Department of Electrical and Computer
Engineering, Aarhus University. No venue is named on the listing. A v1 preprint.

## 1. The short answer: the three numbers are real and topic 2 read them backwards

Topic 2 recorded "NPC dialogue models at roughly 130 MB, roughly 807 MB for
balanced efficiency and performance, and roughly 4.2 GB for its largest
variant", and called the paper "the closest thing to a published answer to
LEDGER's exact question".

The three numbers are in the paper. They are **mean GPU VRAM during inference**
for three off-the-shelf models, not for compressed NPC dialogue models the
authors built:

| Paper's name | Base model | Mean VRAM at inference | Disk |
|---|---|---|---|
| Jack | DistilGPT-2 | 130 MB | 0.4 GB |
| Casper | TinyLlama-1.1B-Chat | 807 MB | 2.73 GB |
| Oliver | Mistral-7B-Instruct | 4.2 GB | 15.93 GB (3.9 GB quantized) |

The contribution of the paper is not a small model. It is LoRA persona
fine-tuning plus runtime-swappable ChromaDB memory stores, measured on three
sizes of an existing model.

## 2. And the sub-gigabyte model is the one the paper declines to recommend

This is the part that overturns topic 2's use of it. Quality tracks size hard.
Denominators are the paper's own: factuality over 100 responses per variant
judged by Openchat-3.6 as an automated judge; context retention over 30
multi-turn interactions; world knowledge retrieval over 30 queries; fluency over
30 responses scored by LanguageTool. Suffix S is the smaller training set, L the
larger.

| | factuality | context retention | knowledge retrieval | fluency | latency | TTFT |
|---|---|---|---|---|---|---|
| Jack (DistilGPT-2, 130 MB) | 16% / 9% | 6.7% / 10% | "significant shortcomings" | "significant grammatical issues" | ~0.8s | ~0.2s |
| Casper (TinyLlama, 807 MB) | 55% / 39% | 63.3% | 76.7% | "nearly error-free" | 1.91s | ~0.2s |
| Oliver (Mistral-7B, 4.2 GB) | 93% | 100% | 100% | 0 errors | 5.49s | 0.1145s |

The paper's own verdict on the 130 MB model, quoted: Jack models "offer
extremely low latency and minimal GPU usage. Such traits position Jack models as
viable candidates for simple NPCs, but not for dialogue related scenarios", and
it "is therefore not recommended without careful consideration of its use-case".

The paper's recommendation is the 7B: "OliverS consistently achieved superior
performance across all dialogue quality metrics".

**So the sentence topic 2 built on, that "a fixed-persona model under one
gigabyte is a researched position rather than a compromise", is not what this
paper establishes. It establishes the opposite for the sub-gigabyte case, and
puts the balanced option at 807 MB with 55% factual accuracy.**

## 3. A number in the paper that does not add up, and it is the one topic 2 quoted

Oliver's disk footprint is 15.93 GB. Its mean VRAM during inference is 4.2 GB.
The machine has one RTX 2070 Super with 8 GB. A 15.93 GB model does not fit in
8 GB, so something moved weights in and out, and **the paper never says what**:
it does not mention offloading, `device_map`, or loading in 4-bit at runtime,
and I searched the full text for all of them.

Consequences, stated rather than resolved:

- "4.2 GB" cannot be read as "this model needs 4.2 GB of video memory". It is a
  mean of a series whose loading strategy is unstated.
- Oliver's 5.49s latency against Casper's 1.91s is consistent with a slow path
  (offload, or streaming from system memory), which would also mean the latency
  is not a property of the model either.
- This is rule 2's case exactly: two numbers from one undescribed setup.

## 4. What the paper measured on, and it is not our machine

Quoted: "All experiments, including training and evaluation, has been conducted
locally on a Windows 11 Desktop PC with an Intel Core i7-8700K CPU, 4x8GB
3200MHz RAM, and an NVIDIA RTX 2070 Super GPU (8GB VRAM)."

NVIDIA, CUDA, 8 GB, one GPU, nothing else running on it. No AMD anywhere in the
paper, no DirectML, no concurrent renderer, no speech model. LEDGER's whole
difficulty, three consumers on one card, is not in this paper at all.

## 5. Quantization went the wrong way, on one datapoint

OliverQ, quantized with AutoGPTQ: disk 15.93 GB down to 3.9 GB, and latency
5.49s up to **34.58s**, with TTFT 0.1145s up to 0.7022s, plus "moderate
degradation in factual accuracy and context retention".

This does not refute topic 2's Q4_K_M arithmetic, which came from GGUF and
llama.cpp figures in search summaries: a different quantizer on a different
runtime. But it is the only MEASURED quantization datapoint the topic has, and
it points the other way. The paper's own conclusion is that a system able to run
a 4 GB model will not care about 16 GB of disk, so do not quantize.

## 6. The part of the paper worth more to LEDGER than the hardware floor

Topic 2 did not extract this, and it is the closest thing in the paper to our
moat. One fine-tuned model powering many NPC instances, each with its own
swappable memory store, measured over 50 swaps per size combination:

- Memory swap time: **0.012 to 0.027 seconds** across small (100 entries),
  medium (500) and large (1000) databases.
- Memory retrieval: **under 0.042 seconds** at 1000 entries, for both the
  conversational and the world-knowledge store.
- Database disk: **3.92 MB at 100 entries, 8.98 MB at 1000**.
- RAM during swap: not measurable, because ChromaDB lazy-loads and memory-maps.
  The paper says so rather than printing a zero.

Two conversational memory stores per NPC, at under 9 MB and 30 milliseconds to
swap, is a costed precedent for per-character memory at a population size. It
says nothing about quality of recall in a real game, and the retention figures
in section 2 are the quality half.

## 7. What changes for the hardware floor

1. **The conversation line of the budget gets a measured anchor and it is worse
   than assumed.** Topic 2's table read "1B to 3B at Q4, fixed persona, 0.8 to
   2.0 GB, quality is the open question". The nearest published measurement of a
   1.1B fixed-persona NPC is 55% factual accuracy and 63.3% context retention
   against an LLM judge. That is not a floor input, it is a quality risk.
2. **Recommendation 2 of topic 2 should be struck or rewritten.** "The
   conversation model should be assumed small until proven otherwise ... the
   arXiv paper above suggests a fixed-persona model under one gigabyte is a
   researched position rather than a compromise" is not supported by the paper.
3. **Recommendation 4 is discharged.** "Read the arXiv paper properly through
   CI" is done, from a desk, through the export mirror. No CI run is needed.
4. **The 12 GB floor is not moved by this.** Nothing here touches the street or
   the voice, which are the two largest lines. What moves is the confidence in
   the smallest line: a 3B-class conversation model can no longer be assumed to
   be both small and good on this evidence.
5. **Pillar 2's job description is the mitigation and is worth saying here.**
   LEDGER's LLMs "classify, never adjudicate", which is not the open-ended
   persona dialogue this paper measures. A 55% factuality score on open
   questions says little about closed-set classification. Whoever writes the
   floor should say which job the model is being sized for, because the paper
   sizes a different one.

## 8. What could not be established

1. The plotted values in figures 2 to 12. Prose only, as stated in section 0.
2. How Mistral-7B was loaded on an 8 GB card (section 3). The paper is silent.
3. Any AMD or DirectML figure. Not in the paper.
4. Whether the judge is sound. Factuality and refusal behaviour were scored by
   Openchat-3.6 prompted with an instruction template. An LLM judging an LLM is
   the instrument here, and the paper does not validate it against humans.
5. Whether the paper is peer reviewed. v1 preprint, no venue on the listing.
6. CPU inference rates on a Ryzen 5 5600X. Still nothing, here or anywhere:
   the paper's CPU is an i7-8700K and it reports no CPU-only inference at all.
7. Everything topic 2 listed under its own section 10 that this paper does not
   touch: the Unreal street's video memory, whether the two speech sessions
   share weights, the 12 GB share of Steam, and any measurement of the three
   consumers running together.

## 9. Sources

Primary, read 2026-09-19 through `export.arxiv.org`:

- arXiv:2511.10277v1, abstract listing, `export.arxiv.org/abs/2511.10277`
- the same paper's full text, `export.arxiv.org/html/2511.10277v1`

Refused this session: `arxiv.org` itself, `huggingface.co`. Open and unused for
this topic: `dev.epicgames.com`, `datashare.ed.ac.uk`, `en.wikipedia.org`,
`docs.blender.org`, `raw.githubusercontent.com`.

Repository figures quoted from topic 2 at `074f85b` and not re-measured here.
