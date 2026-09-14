# Topic 2: the hardware floor

STATUS: SPEC (research delivery). Branch `research/hardware-floor`, from commit
`074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item is filed, no decision
record written, no tile proposed. It ends at a number and a recommendation, and
the decision is Jafar's.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE.

SOURCING LIMIT, unchanged and re-confirmed this session: no external page was
read in full, because outbound HTTPS to research hosts is refused by the egress
proxy (`arxiv.org` was added to the blocked list this session, on top of the
five found during the coverage audit). Every external citation is the search
channel's summary of a named page. Repository claims name their file and line
and were produced by commands run this session.

This topic overlaps queue topic 17 by design. The split I have used: **topic 2
is about what FITS, topic 17 is about what is FAST.** Memory is a hard wall and
frame time is a negotiation, so the wall comes first and this file stops where
milliseconds begin.

## 1. The answer, first

**The floor the design should be held against is 12 GB of video memory, 16 GB of
system memory, a 6-core CPU and an SSD, at 1080p, with the conversation pillar
running a 3B-class model. A 7B-class conversation model needs 16 GB of video
memory and should be an option rather than the floor.**

Two facts make that number, and the second one is uncomfortable.

**Fact one, measured from this repository:** the voice pipeline as currently
exported is enormous. `game-design/voice-live/export-report.txt`, run on
Jafar's machine 2026-08-22, reads the graphs off disk: `t3-step.onnx` is
"2001 MB, 3002 MB with weights", `t3-prefill.onnx` is "2029 MB, 3044 MB with
weights", and the decode export is "1317+805 MB".
`game-design/voice-live/speed-report.txt` records three ONNX sessions opened
for one line. Speech alone is therefore somewhere between roughly 3 and 8 GB
depending on whether the prefill and step sessions share their weights, which
this checkout does not say.

**Fact two, measured from this repository:** the machine the game is being built
on has 9.98 GB of video memory.
`production/mesh-reports/mesh-machine-report.txt`, written 2026-09-01:
AMD Ryzen 5 5600X, 6 cores; 31.9 GB RAM; an AMD Radeon RX 6700 with
"9.98 GB from vram_bytes_registry"; no NVIDIA driver; Windows 11 Pro.

So the floor I am recommending is above the development machine, and the
development machine is where the Meridian Test's fourth condition happens.
That is section 6 and it is the most consequential thing in this file.

## 2. Why there has never been a number, and what the number has to answer

The tile "the hardware floor" is typed absent and its note is exact: "The
minimum machine the game must hold its frame on. Distinct from the frame budget
tile, which measures this build on this machine. Nothing measured: no target
hardware has ever been named in a ruling."

The reason the question stayed open is that LEDGER asks something almost no
shipped game asks: **one graphics card must hold a photoreal street, a language
model and a speech model at the same time.** Every published hardware guide
answers one of those three in isolation. There is no external source that
answers all three together, because the configuration is unusual.

So the number has to be built, not looked up. Three consumers, one pool.

## 3. Consumer one: the street

CITED (search summary of "Best VRAM for Unreal Engine 5 in 2026", Medium, and
the UE5 performance guides): "8GB is the realistic minimum for 1080p gaming in
UE5", and at that capacity "you will be limited to simple scenes and will likely
need to disable features like Virtual Shadow Maps or lower the resolution of
your textures". For development rather than play, "16GB VRAM is considered a
safe baseline for smooth development".

CITED (search summary of Epic's Lumen Performance Guide and StraySpark's
optimisation guides): Lumen targets 30 and 60 fps on consoles with 8ms and 4ms
budgets at 1080p; on a mid-range GPU at 1080p, software Lumen at default quality
costs 3 to 6ms and hardware ray tracing at quality mode 2 reaches 10 to 14ms.

ASSUMED, and it is the weakest number in this file: **6 GB for a dense
photoreal street at 1080p with software Lumen, moderate texture resolution and
Virtual Shadow Maps on.** That sits below the quoted 8 GB "realistic minimum"
because that figure is for a game using the whole card, and LEDGER cannot. It is
an assumption a builder may change freely and nothing downstream should treat it
as researched. HOLE: this repository has never measured the Unreal street's
video memory. The tile "the frame budget" is typed partial for exactly this
reason and its note says "no budget for the Unreal street at a resident count is
set in this checkout". **Measuring it is queue topic 17's first job and it would
replace this assumption with a fact.**

The frame-time half is topic 17's. One note that belongs here because it is
about fitting rather than speed: hardware ray-traced Lumen at 10 to 14ms leaves
2.7 to 6.7ms of a 16.7ms frame for everything else at 60fps. Software Lumen at
3 to 6ms leaves 10.7 to 13.7ms. DERIVED: at the visual bar D8 sets, software
Lumen is the only version of this that has room for a town in it, and that is a
constraint on the art direction, not only on the settings menu.

## 4. Consumer two: the conversation

CITED (search summaries of llmhardware.io's quantization guide, promptquorum's
VRAM charts and willitrunai's GGUF guide): a 7B model at Q4_K_M needs
approximately 4 to 5 GB of video memory, "calculated as parameters in billions
times 0.5 bytes per parameter, plus about 20% overhead", plus 1 to 2 GB of
headroom for the KV cache and the operating system. Q4_K_M "cuts VRAM 72% with
minor quality loss". Budget-tier consumer GPUs run 7B to 8B models at 25 to 35
tokens per second. An 8 GB card handles 7B at Q4_K_M "comfortably at up to about
8K context".

CITED (search summary of the arXiv paper "Fixed-Persona SLMs with Modular
Memory: Scalable NPC Dialogue on Consumer Hardware", arXiv 2511.10277): the
paper reports NPC dialogue models at roughly 130 MB, roughly 807 MB "for
balanced efficiency and performance", and roughly 4.2 GB for its largest
variant. HOLE: `arxiv.org` is egress-blocked, I could not read the paper, and
these three figures are a summariser's rendering of it. **It is the closest
thing to a published answer to LEDGER's exact question that I found, and reading
it properly should be the first thing anybody does with this topic.**

DERIVED, the range the design has to choose within:

| Conversation model | Video memory | What it costs the game |
|---|---|---|
| 1B to 3B at Q4, fixed persona | 0.8 to 2.0 GB | fits anywhere; quality is the open question |
| 7B to 8B at Q4_K_M | 4.0 to 5.0 GB plus 1 to 2 GB context | the single largest line item after the street |
| Anything on the CPU instead | 0 GB video, 4 to 6 GB system | free of the card, and see below |

THE CPU OPTION IS REAL HERE AND IS USUALLY NOT. Jafar's machine has 31.9 GB of
system memory and 6 cores, and the Steam survey says 16 GB is the most common
configuration. Moving the language model to the CPU takes the largest competitor
off the card entirely. DERIVED and ASSUMED: a 7B at Q4 on six cores is
single-digit tokens per second, which is too slow for conversation; a 1B to 3B
might reach the 15 to 25 range. HOLE: I have no cited figure for CPU inference
rates on a Ryzen 5 5600X and did not find one. That measurement is cheap, it is
not in this repository, and it would change the recommendation if it came back
well.

## 5. Consumer three: the voice, and it is bigger than anyone has said

This is the section with real measurements in it, and they are ours.

Read from `game-design/voice-live/export-report.txt` (run 2026-08-22 on
Jafar-Desktop, reading the graph files themselves):

| Graph | On disk |
|---|---|
| `t3-step.onnx` | 2001 MB, 3002 MB with weights |
| `t3-prefill.onnx` | 2029 MB, 3044 MB with weights |
| decode export | 1317 + 805 MB |

`game-design/voice-live/speed-report.txt` (2026-08-22) records "three sessions
in 41.9s total" for one line, using `DmlExecutionProvider`.

DERIVED, with the uncertainty stated rather than hidden: if the prefill and step
sessions each hold their own copy of the weights, the speech stack is roughly
**8.2 GB**. If ONNX Runtime shares them, it is roughly **5.2 GB**. Either way it
is the largest single consumer on the card, larger than a 7B language model, and
larger than I expected before reading the file.

WHY IT IS THIS BIG: the export is fp32. The latency file records the reason in
its own words, as the rationale for a conversion that later failed: "the shipped
weights are bfloat16 upstream, we exported at fp32, DOUBLING the bandwidth the
model was trained to need". So the size is a property of the export, not of the
model, and the fp16 attempt that would have halved it was closed on 12 August
because it corrupted the sampling distribution.

**This is the second independent argument for the Chatterbox Turbo evaluation
recommended in topic 1**, and it is a different argument from the first. Topic 1
recommended it for latency, because its decoder is distilled from ten solver
steps to one. This topic wants it for SIZE: 350M parameters against whatever the
current export is (DERIVED from 2001 MB of fp32 weights: roughly 0.5B). A
smaller model in an official export is the only route I can see to a speech
stack that leaves room for a game.

RECORDED AS A CORRECTION TO TOPIC 1, found while doing this one. Topic 1 flagged
the chunk decode cost as its weakest link, "the file's estimate at a speed that
never arrived", with nothing in the checkout measuring it. That was not quite
right and I am correcting it rather than leaving it: `speed-report.txt` reads
"decode: 1.68s for 3.7s of audio", which is 0.454s of decode per second of
audio, and corroborates the latency file's ~0.5s estimate to within ten percent.
The caveat that survives: a CHUNKED decode re-encodes the prompt and all tokens
so far on every chunk, so per-chunk cost grows along the line and is not simply
the whole-line figure divided by its seconds. So 0.454s is a floor for the
per-chunk cost, not the cost. Topic 1's arithmetic stands and its hole is
narrower than it said.

A SECOND THING THE SAME FILE SAYS, and it matters for both topics.
`speed-report.txt` on 22 August reads "92 steps in 4.4s, first 157ms, median
42ms" and concludes "ONE LINE: 6.4s of work for 3.7s of speech, 1.7x real time".
That is the PRE-residency step cost. The 17.2ms that topic 1 rests on is the C#
resident binding described in the latency file, and grepping the four report
files in `game-design/voice-live/` for `17.2`, `resident`, `IoBinding` and
`IOBinding` returns nothing. DERIVED: the two numbers describe two different
code paths, the Python path through the shipped graphs and the C# bench, which
is consistent rather than contradictory. But **nobody has measured the resident
path end to end on a real line**, and the newest end-to-end number in this
repository still reads 1.7x real time. Topic 1's recommendation is unchanged;
its confidence should be.

## 6. What this means for the machine the game is being built on

`production/mesh-reports/mesh-machine-report.txt`, 2026-09-01:

- AMD Ryzen 5 5600X, 6 cores
- 31.9 GB system RAM
- AMD Radeon RX 6700, **9.98 GB** video memory
- No NVIDIA driver at all ("no nvidia-smi: there is no NVIDIA driver on this
  machine")
- Windows 11 Pro, 90.7 GB free on C:

DERIVED, adding the three consumers at their most favourable plausible values:

| | Optimistic (shared weights, 3B model) | Realistic (separate weights, 7B model) |
|---|---|---|
| Street (ASSUMED) | 6.0 GB | 6.0 GB |
| Voice (measured export) | 5.2 GB | 8.2 GB |
| Conversation | 2.0 GB | 5.0 GB |
| **Total** | **13.2 GB** | **19.2 GB** |
| Against the machine | 9.98 GB | 9.98 GB |

**It does not fit, and it does not nearly fit.** Even the optimistic column is a
third over the card, and that column already assumes weight sharing this
checkout has not verified and a conversation model nobody has chosen.

THREE THINGS FOLLOW, and they are the useful part of this file.

1. **The voice export has to shrink before anything else is worth optimising.**
   It is the largest consumer, it is large for a reason that is fixable (fp32 on
   bf16-native weights), and the fix is the same evaluation topic 1 already
   recommends for a different reason. Two topics arriving at the same next step
   from opposite directions is the strongest signal this research lane has
   produced so far.
2. **The conversation model should be assumed small until proven otherwise.**
   The design has never named a size. Every gigabyte it takes is a gigabyte the
   street does not have, and the arXiv paper above suggests a fixed-persona
   model under one gigabyte is a researched position rather than a compromise.
   Pillar 2 says LLMs "classify, never adjudicate" and that outputs are
   "classifications and closed-set choices that deterministic Core executes",
   which is a much smaller job than open-ended generation, and small jobs suit
   small models.
3. **Jafar's machine cannot demonstrate the full stack at the visual bar**, and
   the Meridian Test's fourth condition is him choosing to play it. Section 8
   is what to do about that.

## 7. What the world actually owns

All CITED from search summaries of the Steam Hardware Survey coverage for
July and August 2026 (tbreak, thefpsreview, tech-insider, specclear, club386).

**Video memory, August 2026:**

| Configuration | Share |
|---|---|
| 16 GB | 26.92% |
| 8 GB | 25.75% |
| 12 GB | 12.99% |
| 24 GB | 5.43% (July figure) |
| 4 GB | 5.69% |
| **10 GB or more** | **51.42%** |

July 2026 was the first month 16 GB overtook 8 GB as the single most common
configuration, and the first month a majority of Steam players crossed 10 GB.

**System memory, August 2026:** 16 GB is 41.07%, 32 GB is 38.47%. Together
nearly 80%.

**CPU cores:** 8-core passed 6-core for the first time, 27.85% against 27.52%.

DERIVED, and stated as a lower bound because my sources do not break out 10 GB
and 11 GB cards separately: **at least 45.3% of Steam has 12 GB or more**
(26.92 + 12.99 + 5.43), and **at least 32.4% has 16 GB or more**. The true 12 GB
figure is 51.42% minus the 10-and-11 GB share, which I could not establish.

NOTE THE COINCIDENCE, because it is almost funny. The survey's own headline
threshold this year is 10 GB, and the development machine has 9.98 GB. It is on
the wrong side of the line the industry chose to celebrate, by twenty megabytes.

## 8. The number, and what it is a number OF

**THE FLOOR, recommended as the thing the design is held against:**

| | Minimum | Recommended |
|---|---|---|
| Video memory | **12 GB** | 16 GB |
| System memory | 16 GB | 32 GB |
| CPU | 6 cores | 8 cores |
| Storage | SSD | SSD |
| Resolution and frame rate | 1080p, 30 fps | 1080p or 1440p, 60 fps |
| Conversation model | 3B class, or CPU | 7B class on the card |
| Reach on Steam today | at least 45% of players | at least 32% |

**AND THE CONDITION THAT MAKES IT ACHIEVABLE, which is not hardware:** the
speech stack has to come down from its measured 5 to 8 GB to roughly 1.5 to
2 GB. Without that, 12 GB is not a floor, it is a fiction, and the honest floor
would be 20 GB, which is 5.43% of Steam.

WHAT THIS NUMBER IS A STATISTIC OF, because a number without that is not a
measurement: it is a MEMORY budget, derived by adding three consumers, two of
them measured from this repository's own files and one of them assumed. It is
not a frame-time budget and says nothing about whether the game runs at 60 fps
on a 12 GB card. That is queue topic 17 and this file deliberately stops here.

WHAT WOULD MOVE IT:

- **Down to 10 GB**, which would include the development machine: a speech stack
  under 1.5 GB AND the conversation model on the CPU. Both are plausible and
  neither is measured.
- **Up to 16 GB**: if the street turns out to want 8 GB rather than the 6 GB I
  assumed, which is the single most likely way this number is wrong.

## 9. Recommendation

1. **Name 12 GB as the floor now, provisionally, and write it down.** The tile
   has been absent since the respec and an unwritten floor has let three
   separate decisions be taken without one. A provisional number that gets
   corrected is worth more than no number, because it can be argued with.
2. **Treat the speech export's size as a blocker, not a detail.** It is the
   largest consumer on the card and the reason the floor is 12 rather than 10.
3. **Measure three things, in this order, all cheap:**
   - The Unreal street's video memory at a resident count. Replaces the only
     assumed number in the budget, and is topic 17's first job anyway.
   - Whether the two text sessions share their weights. It is the difference
     between 5.2 GB and 8.2 GB, and one line of a probe answers it.
   - A conversation model's rate on the Ryzen 5 5600X, on the CPU. If it is
     usable, the whole budget changes shape.
4. **Read the arXiv paper properly through CI.** It is the only published work I
   found that asks LEDGER's exact question, and I could not open it.

## 10. What could not be established

1. **The Unreal street's actual video memory.** Never measured here. The 6 GB
   in every table above is ASSUMED, and it is load-bearing.
2. **Whether the prefill and step sessions share weights.** The difference is
   3 GB, which is a quarter of the recommended floor.
3. **CPU inference rates on the development machine.** No cited figure found for
   a Ryzen 5 5600X, and none in this repository.
4. **The arXiv paper's real contents** (2511.10277). Egress-blocked; its three
   figures are a summariser's rendering.
5. **The exact share of Steam at 12 GB or more.** My sources give 10 GB or more
   (51.42%) and individual buckets, but not the 10-and-11 GB slice needed to
   subtract. The 45.3% is a lower bound and is labelled as one.
6. **Any measurement of the three consumers running together.** Every figure in
   this file is a consumer measured or estimated alone. Contention, allocator
   behaviour and the fact that DirectML already crashed this project once when
   two sessions ran concurrently all argue that the sum is optimistic.
7. **The conversation model itself.** No model has been chosen, so its size is a
   range rather than a number, and that is a design decision this file cannot
   make.
8. **Console and Steam Deck**, both out of scope: canon says PC first.

## 11. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- tbreak, "Steam Hardware Survey: 16GB VRAM Overtakes 8GB (July 2026)", https://tbreak.com/steam-hardware-survey-16gb-vram-overtakes-8gb/
- The FPS Review, "The July Steam Survey Is In: 16GB GPUs Have Officially Overtaken 8GB for the First Time", https://www.thefpsreview.com/2026/08/10/the-july-steam-survey-is-in-16gb-gpus-have-officially-overtaken-8gb-for-the-first-time/
- tech-insider, "Steam Hardware Survey Aug 2026: Windows 11 at 70.97%", https://tech-insider.org/steam-hardware-survey-august-2026/
- tech-insider, "Steam Hardware Survey: 16GB GPUs Pass 8GB at 25.9%", https://tech-insider.org/steam-hardware-survey-july-2026/
- specclear, "Steam Hardware Survey July 2026", https://specclear.com/steam-hardware-survey-july-2026/
- Club386, "Steam Hardware Survey shows 16GB VRAM GPUs and eight-core CPUs are the new majority", https://www.club386.com/steam-hardware-survey-july-2026/
- Valve, "Steam Hardware and Software Survey", https://store.steampowered.com/hwsurvey/En?platform=pc
- Epic, "Lumen Performance Guide for Unreal Engine", https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine
- StraySpark, "UE5 Lumen Optimization Guide: Achieving 60fps with Dynamic Global Illumination", https://www.strayspark.studio/blog/ue5-lumen-optimization-60fps
- Medium (Mumbamweni), "Best VRAM for Unreal Engine 5 in 2026", https://medium.com/@mumbamweni3/best-vram-for-unreal-engine-5-in-2026-stop-freezing-during-real-time-rendering-f4d2539299e2
- Epic Developer Community Forums, "Nanite and Raytracing using increasing amounts of VRAM in 5.6.1", https://forums.unrealengine.com/t/nanite-and-raytracing-using-increasing-amounts-of-vram-in-5-6-1-after-upgrading-from-5-4-4/2657184
- llmhardware.io, "LLM Quantization Explained: Q4, Q8, FP16 and VRAM Tradeoffs (2026)", https://llmhardware.io/guides/llm-quantization-guide
- promptquorum, "How Much VRAM for Local LLM? 7B to 70B Charts (2026)", https://www.promptquorum.com/local-llms/how-much-vram-local-llm
- willitrunai, "GGUF Quantization Guide (2026)", https://willitrunai.com/blog/quantization-guide-gguf-explained
- Spheron, "GPU Requirements Cheat Sheet 2026", https://www.spheron.network/blog/gpu-requirements-cheat-sheet-2026/
- localaimaster, "How Much VRAM Do You Need for AI Models? (2026)", https://localaimaster.com/blog/vram-requirements-2026
- arXiv 2511.10277, "Fixed-Persona SLMs with Modular Memory: Scalable NPC Dialogue on Consumer Hardware", https://arxiv.org/pdf/2511.10277 (EGRESS BLOCKED)
- NVIDIA, "In-Game Inferencing", https://developer.nvidia.com/rtx/in-game-inferencing
- PCGamesN, "Kingdom Come Deliverance 2 system requirements", https://www.pcgamesn.com/kingdom-come-deliverance-2/system-requirements
- Windows Central, "Kingdom Come: Deliverance 2 PC system requirements and specs", https://www.windowscentral.com/gaming/kingdom-come-deliverance-2-pc-system-requirements-specs
- CORSAIR, "Kingdom Come: Deliverance 2 System Requirements and Recommended Specs", https://www.corsair.com/us/en/explorer/gamer/gaming-pcs/kingdom-come-deliverance-ii-system-requirements-and-recommended-specs/

Repository sources, read this session at commit `074f85b`:
`production/mesh-reports/mesh-machine-report.txt`,
`game-design/voice-live/export-report.txt`,
`game-design/voice-live/speed-report.txt`,
`game-design/voice-live/step-report.txt`,
`game-design/live-speech-latency.md`, `production/systems-inventory.json`,
`ledger-v2/respec/vision-pillars-v2.md`, `canon.md`,
`ledger-v2/studio-v2/learning.md`.
