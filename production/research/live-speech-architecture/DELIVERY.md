# Topic 1: live speech, and whether the architecture is still right

STATUS: SPEC (research delivery). Branch `research/live-speech-architecture`,
from commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item is filed, no decision
record written, no code touched. It ends at a recommendation.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE, as defined in
`production/art/atlas-02/research/small-pub-plan-measured.md` and used through
the coverage audit.

SOURCING LIMIT, measured this session and not carried over on trust. Outbound
HTTPS to research hosts is refused by the egress proxy: five hosts were fetched
during the audit and each answered `EGRESS_BLOCKED`. WebSearch works and returns
the search channel's summary of a page with its title and URL. So every external
citation below is that summary and NOT a page read in full. HuggingFace is
blocked here by the same policy, which matters specifically for section 5:
`ResembleAI/chatterbox-turbo-ONNX` is named in search results and I could not
open it, so nothing about its contents is claimed.

Claims about this repository name their file and line and were produced by
commands run this session.

## 1. The answer, first

**The experiment written in `game-design/live-speech-latency.md` is no longer
the right next step, and not because the architecture is wrong. It is because
most of that experiment has already run, and the premise the brief quotes was
superseded inside the same document a month ago.**

The brief says: "the arithmetic in game-design/live-speech-latency.md says
generation runs at 23.8 tokens per second against playback's 25, so streaming
would underrun."

That sentence is in the file, in the table in section 8. Section 4 of the same
file, further up, records this on 12 August:

> **LEVER A LANDED (12 Aug, round seven of seven): 17.2ms flat, ZERO slope,
> bit-exact.** [...] 58 tok/s sustained against playback's 25, sustainability
> crossed at 2.3x margin, in fp32, with guidance, on the vendor-neutral path. A
> whole ~86-token line is now ~1.5s of steps + 0.08s prefill + decode: the line
> computes faster than it plays even unstreamed.

So the document contradicts itself, and the contradiction is the ordinary kind:
section 8's budget table is the state of the world before the levers ran, and
nobody went back to it. The 23.8 figure is a live claim in a live document and
it is false. That is rule 1's decay case, and the sentence rather than the site
is what needs finding: 23.8 appears in section 2 as the starting measurement
(correct, historical) and in section 8's table as "today" (wrong).

**What is true as of the last measurement in this repository, which is 12 August
2026:** streaming does not underrun. The step loop runs at 17.2ms flat with zero
position slope, bit-exact against the host path, on the RX 6700 over DirectML in
fp32 with guidance on.

**What the brief should be asking instead**, and what sections 4 and 5 answer:
the margin that actually governs the streaming worker is not the step rate, and
it is thinner than 2.3x. And a model released since these measurements were
taken would change the term that governs it.

## 2. What has already run, and what has not

The file's own experiment order (its section 9), against what its section 4
records as landed. Read from the document this session.

| # | Experiment | State |
|---|---|---|
| 1 | probe-step-costs: step time vs position, GPU name, contention | **DONE, 12 Aug.** 31.8ms flat + 142us/position measured; card is an RX 6700 sharing with a Parsec display encoder; contention closed the hard way (see below) |
| 2 | rep-penalty retest of no-guidance (lever C) | **DONE, 12 Aug.** Confounding proven, then lever C killed anyway on a better measurement: guidance stays |
| 3 | fp16 export and selftests (lever B) | **DONE and CLOSED, 12 Aug.** Speed was real (26ms steps) and the conversion corrupts the sampling distribution: ten seeds gave 4, 0, 170, 0, 97, 233, 222, 214, 0, 18 tokens on one nine-word line |
| 4 | IOBinding spike, the engineering half of lever A | **DONE and LANDED, 12 Aug**, in seven rounds, with a seven-fault ledger written for the next person |
| 5 | chunk-seam test (lever D's quality) | **NOT RUN** |
| 6 | LLM leg timing | **NOT RUN**, and the file calls it "the leg nobody has measured" |

Also settled by experiment 1, and it is the most consequential structural result
in the file: running the step session and the decode session concurrently from
two threads crashes the process with an access violation, on a stack where
running them sequentially has worked hundreds of times. CITED (the file, section
8): "the streaming design is settled by a crash rather than a benchmark: one
thread, strictly interleaved, N steps, then a chunk decode, never overlapped."

MEASURED THIS SESSION: `game-design/voice-live/step-report.txt` is stamped
"ran on Jafar-Desktop (Windows), 2026-08-12 13:33 UTC" and there is no later
live-speech report in this checkout. The four report files carry a filesystem
date of 2026-09-10, which is when this clone was written, not when they ran.
So 12 August is the newest evidence and this file does not assume anything has
happened since.

## 3. The margin that governs the worker, and it is not 58 against 25

This is the correction that matters most, and it is arithmetic over the file's
own numbers rather than anything external.

The 2.3x margin is a STEP margin: 58 steps per second against 25 tokens of
playback per second. But the interleave rule means the decode pause is inside
the same thread, so the real budget is the file's own: per chunk, N steps PLUS
one chunk decode must fit inside the audio that chunk buys.

DERIVED, from the file's figures, with the arithmetic printed so it can be
refuted:

- A 25-token chunk buys 1.00s of audio (the model emits 25 acoustic tokens per
  second of audio; CITED, the file section 2, from 86 tokens rendering 3.44s).
- 25 steps at the landed 17.2ms = **0.43s**.
- One chunk decode at 4 solver steps: the file estimates **~0.5s** (its section
  8 budget, quoted at "residency+fp16 speeds (~15ms steps, ~0.5s chunk)").
- Total **0.93s of work per 1.00s of audio. Sustainable, at a margin of 1.07x.**

So the file's conclusion holds and its headline number oversells it by a factor
of two. Sustainability is crossed by seven percent, not by 130 percent, and
seven percent is inside the noise of a machine that also runs a Parsec display
encoder (the file flags that caveat itself) and that will, in the shipped
configuration, be running an Unreal frame and a local language model at the same
time.

HOLE, and it is the weakest link in this section: the ~0.5s chunk decode is the
file's estimate at a speed that never arrived (fp16 died), not a measurement.
Nothing in this checkout measures a chunk decode. Everything in section 3 and
section 5 is only as good as that number, and measuring it is cheap.

## 4. What has changed outside since 12 August

### 4.1 The field split into two architectures, and ours is on the slower side

CITED (search summary of "Best Open Source TTS Models in 2026: Kokoro,
Chatterbox, Fish Audio Compared", tryspeakeasy.io, and CodeSOTA's TTS guide):
"the real-time factor differences between models come down to architecture:
Kokoro (StyleTTS 2 + ISTFTNet) and F5-TTS (flow matching) are non-autoregressive
[...] Chatterbox, Orpheus 3B and Bark are autoregressive speech LLMs that emit
audio tokens one at a time. The published real-time factors split so sharply
(Kokoro around 0.03, F5-TTS around 0.15) even though the models sit within an
order of magnitude of each other in size."

DERIVED, and it reframes the whole latency document: the "25 tokens per second
of audio" break-even that orders every lever in that file is not a fact about
text-to-speech. It is a property of choosing an autoregressive token-emitting
model. A non-autoregressive model has no break-even to cross, because it does
not emit tokens at playback rate; it renders a clip in a fixed number of passes.

That does NOT mean we chose wrong. `game-design/decisions-pending.md:250` records
the engine decision of 2026-07-28: four engines were benchmarked (piper as a
control floor, kokoro, xtts, chatterbox) and chatterbox won on the direction
test, because it "exposes an `exaggeration` control" and clones identity from a
reference. `game-design/voice-casting-history.md:104` records that Jafar heard
the mood control himself. Kokoro was dropped for a reason that has not changed:
CITED (search summary of Pinggy and localaimaster), Kokoro-82M ships 54 fixed
voices and is Apache 2.0; it does not do zero-shot cloning, and nineteen cast
voices were built on cloning.

So the architecture question has a clean answer: **the autoregressive choice was
made deliberately, for a capability the fast architectures do not have, and it
should not be reopened on speed grounds.** What should be reopened is which
member of the chatterbox family we run, which is section 5.

### 4.2 What the latency literature actually says, and how our target compares

CITED (search summaries of AssemblyAI, "The 300ms rule", Telnyx, Hamming AI and
Picovoice): research on turn-taking across languages puts the gap between one
speaker finishing and the next beginning at 200 to 300ms. Under 300ms "feels
magical"; 300 to 800ms is "the sweet spot for most production deployments";
600 to 1000ms is "noticeable but tolerable"; "above 1000ms, user experience
degrades reliably".

Our own target, CITED from the file's section 1: "Target under ~1.2s, which with
an acknowledgment beat (the character turns, breathes, taps the bar) reads as a
person deciding to answer."

**So the project's stated latency target sits above the number this literature
calls the point where experience degrades reliably.** That is worth saying
plainly and it is NOT straightforwardly a fault, for two reasons the literature
does not cover:

1. Every source above is about voice ASSISTANTS, where a person speaks and then
   waits with nothing happening. A game has cover: the text is instant, the
   character can turn and react, and the file's design lever F is exactly this.
2. The 200 to 300ms figure describes the gap between conversational turns, not
   the time a person takes to answer a hard question. A publican taking 1.2
   seconds to decide what to tell you is not broken; he is thinking.

DERIVED, and it is a design question nobody in this repository has framed: those
two facts point in opposite directions for different lines. A reflexive
one-word answer at 1.2s reads as lag. A considered answer at 1.2s reads as
thought. The file treats latency as one budget; the literature suggests it is
two, and that the cheap one (a bark, a "No.", a grunt) has a much tighter
requirement than the expensive one. Nothing measures or distinguishes them
today. Flagged rather than proposed.

### 4.3 The API path, priced

CITED (search summaries of Deepgram's 2026 API roundup, futureagi, pkgpulse and
texttolab), per 1,000 characters: OpenAI TTS $0.015, Cartesia $0.038, Fish Audio
S2 Pro $15 per million, ElevenLabs $0.18 to $0.30.

DERIVED, at an ASSUMED 70 characters for a typical spoken line of around twelve
words (the assumption is mine and a line-length distribution from the bark bank
would replace it):

| Provider | Per line | Per 300-line session | Per 30h playthrough at 300 lines/hour |
|---|---|---|---|
| OpenAI TTS | $0.001 | $0.32 | $9.45 |
| Cartesia | $0.0027 | $0.80 | $23.94 |
| ElevenLabs | $0.013 to $0.021 | $3.78 to $6.30 | $113 to $189 |

Three things follow and none of them is about the price.

- **It is a per-player operating cost on a product with no recurring revenue.**
  Even the cheapest column is a cost that arrives every time somebody plays,
  forever, against a one-time purchase. The project has a small budget and no
  deadline, and a per-player meter is the one shape of cost that does not fit
  either.
- **It deletes offline play**, which for a single-player crime sim is not a
  feature to trade. Pillar 2 says "spoken via the local voice pipeline"; the
  word local is doing work.
- **It reopens a licence question that is currently closed.** The allowlist
  makes the local pipeline and chatterbox (MIT, keep watermark) ship-safe, and
  bans "cloned real voices". Nineteen voices cast under the consent rule and
  cloned locally is one legal posture; sending those same reference clips to a
  third-party API is a different one, and it belongs to queue topic 20 rather
  than being decided here.

RECOMMENDATION on the API path: **OUT as the shipping path.** Worth keeping as a
development convenience if anybody wants to hear a line without a GPU, which is
a tooling decision and not an architecture one.

### 4.4 What runs alongside a game engine now

CITED (search summaries of NVIDIA's In-Game Inferencing SDK page and the NVIDIA
technical blog, "Build On-Device AI Companions with the NVIDIA ACE Game Agent
SDK and Unreal Engine 5 Plugins"): NVIDIA now ships ACE plugins for Unreal
Engine 5 covering speech recognition, a small language model for low-latency
text, and text-to-speech with "a high-quality 350M TTS model", with an
In-Game Inferencing SDK for in-process C++ execution and "CUDA in Graphics" to
let graphics and compute run together at low latency. Their own guidance names
our exact problem: agents "can make excessive calls to the GPU that compete with
graphics", so minimise calls and maximise what each accomplishes.

CITED (search summary of the NVIDIA ACE Chatterbox TTS model card at
docs.nvidia.com/ace-for-games/chatterbox-tts): NVIDIA ships a Chatterbox TTS
plugin pack for games.

TWO THINGS TO TAKE FROM THIS AND ONE NOT TO.

- **Take**: the 350M model NVIDIA ships in its game TTS plugin and Chatterbox
  Turbo's 350M parameter count are the same number, and NVIDIA's plugin pack is
  named Chatterbox. The engine this project picked in July is the one a hardware
  vendor productised for games. That is independent confirmation of the choice,
  and of the direction section 5 recommends.
- **Take**: "minimise the number of inference calls" is guidance we can act on
  without NVIDIA's SDK, and it argues for sentence-level pipelining rather than
  token-level chatter, which the file's lever F already names.
- **Do not take**: NVIGI and CUDA-in-Graphics are NVIDIA-only. The file settles
  this already and it is worth not re-litigating: the dev machine is an AMD RX
  6700, the game must ship for both, and "DirectML is not a fallback, it is the
  shipping baseline, the one vendor-neutral GPU path on Windows."

## 5. The thing that did not exist on 12 August

**Chatterbox Turbo.** Same family, same vendor, same licence, released since the
measurements in the latency file were taken.

CITED (search summaries of resemble.ai's Chatterbox Turbo page, the Hugging Face
model card listing, Communeify and aigazine):

- 350M parameters, MIT licence, PerTh watermarking on every output.
- "The speech-token-to-mel decoder was distilled, reducing generation from 10
  steps to just one, while retaining high-fidelity audio output."
- Streaming-ready inference with a configurable chunk size, default 50 speech
  tokens.
- An official ONNX release exists: `ResembleAI/chatterbox-turbo-ONNX`.

CONTESTED, and recorded rather than resolved: the same set of sources gives
"75ms latency and 6x real-time" in one place and "a real-time factor of 0.499 on
an RTX 4090, with first-chunk latency around 472ms" in another. RTF 0.499 is 2x
real time, not 6x, and 472ms is not 75ms. I could not reach either page. Both
figures are also on an RTX 4090, which is not an RX 6700. **Treat every Turbo
speed number in this file as a direction.**

### 5.1 Why this matters more than any remaining lever

Section 3 established that the governing budget is steps plus ONE CHUNK DECODE
per chunk of audio, and that the decode is roughly half of it. Turbo's headline
change is a decoder distilled from ten solver steps to one.

We run four solver steps, not ten (CITED, the file section 2: "Decode at 4
solver steps runs at ~2.1x real time on the card"). So the saving for us is 4 to
1, not 10 to 1.

DERIVED, under the ASSUMED and stated approximation that flow-solver decode cost
is roughly linear in solver steps:

| | steps per 25-token chunk | chunk decode | total per 1.00s of audio | margin |
|---|---|---|---|---|
| Today (lever A landed, 4-step decode) | 0.43s | ~0.50s | 0.93s | 1.07x |
| With a one-step decoder | 0.43s | ~0.125s | 0.555s | **1.80x** |

And time to first sound, prefill 0.08s plus one chunk:

| | first sound |
|---|---|
| Today | ~1.01s |
| With a one-step decoder | ~0.64s |

DERIVED again: ~1.01s sits exactly on the 1000ms line the latency literature
calls the point where experience degrades reliably. ~0.64s sits inside the 300
to 800ms band the same sources call the production sweet spot. That is not a
marginal improvement, it is the difference between the two sides of the only
external threshold anybody has offered us.

### 5.2 Why it is a low-risk change and where the risk actually is

- Same family, same vendor, same MIT licence, already on the allowlist ("keep
  watermark"), so no new decision record is needed for the licence.
- Same cloning mechanism, so the nineteen cast voices are reference clips and
  not fine-tunes. HOLE: I did not verify that Turbo accepts the same reference
  format.
- Official ONNX release, and this repository's entire voice path is ONNX plus
  DirectML with a hand-built resident KV cache.

THE TWO RISKS, both unresolved here and both cheap to resolve.

1. **Does Turbo keep the `exaggeration` control?** This is the deciding
   question, not a detail. `game-design/production-plan-audio-art.md:134`
   records that chatterbox was added "specifically because it exposes an
   `exaggeration` control", and the engine decision of 2026-07-28 was made on
   the direction test that control enables. A faster model that cannot do moods
   is not an upgrade, it is a different decision. **HOLE: not established.**
2. **Does the ONNX export run on the DirectML execution provider?** CITED
   (search summary of the devnen/Chatterbox-TTS-Server README): installation
   paths cover CPU, NVIDIA CUDA and AMD ROCm. DirectML is not named anywhere I
   found, and the same search says so explicitly. ROCm is not a Windows shipping
   path for this project. An ONNX graph can in principle run on the DML
   execution provider, but operator coverage is exactly the kind of thing that
   fails silently or loudly on conversion, and this repository already has a
   seven-fault ledger about DML's behaviour. **HOLE: not established, and it is
   the one that decides whether any of section 5 is usable.**

## 6. Recommendation, stated plainly

**The architecture does not need to change. The model probably does, and that
question should be answered before the streaming worker is built, not after.**

Reasoning, in order:

1. The streaming worker's entire design is shaped by two constraints: the
   one-thread interleave rule (settled by a crash, not negotiable) and the size
   of the chunk decode pause. The second of those is the term Chatterbox Turbo
   changes, by roughly a factor of four.
2. Building the worker against a 0.5s decode and then swapping to a 0.125s
   decode means having designed the chunk size, the head-start rule and the
   underrun guard around a constraint that is no longer there.
3. The current margin is 1.07x on a machine that is not yet running the game, a
   language model, or an Unreal frame. Seven percent is not a margin, it is a
   rounding error, and every one of those three additions eats it.
4. The change is inside an existing decision (D-less, but recorded on
   2026-07-28), inside an existing licence line, and inside an existing ONNX
   plus DirectML pipeline.

WHAT I WOULD DO FIRST, and all of it is measurement rather than building:

- **Measure the chunk decode.** It is the largest term in the governing budget
  and the only one in this analysis that is an estimate rather than a number.
  Everything in sections 3 and 5 is bounded by it.
- **Answer the two Turbo questions**, in this order because the second is
  pointless if the first fails: does it keep `exaggeration`, and does its ONNX
  export load and run on the DirectML execution provider on the RX 6700. Both
  need HuggingFace, which is blocked here, so both go through CI, and the
  project's own rule applies: make the run maximally informative rather than a
  blind attempt.
- **Then experiment 6, the LLM leg.** It has never been measured, the file calls
  it that, and it sits upstream of every number above. A 2-second
  time-to-first-sentence upstream makes a 0.4-second saving downstream
  irrelevant, and nobody knows which world we are in.

WHAT I WOULD NOT DO YET: experiment 5, the chunk-seam test. It measures the
audible quality of a seam produced by a decoder that may be replaced.

## 7. What could not be established

1. **The chunk decode cost.** Nothing in this checkout measures it; the ~0.5s is
   the latency file's estimate at a speed that never arrived. Sections 3 and 5
   rest on it.
2. **Whether Chatterbox Turbo keeps `exaggeration`.** The deciding question for
   the recommendation, and unanswered.
3. **Whether the Turbo ONNX export runs on DirectML.** Not named in any source I
   reached. HuggingFace is blocked here.
4. **Turbo's speed on an RX 6700.** Every figure found is on an RTX 4090, and
   the two figures found disagree with each other (75ms against 472ms, 6x
   against RTF 0.499).
5. **Whether anything has happened since 12 August 2026.** That is the newest
   live-speech measurement in this checkout, per `step-report.txt`'s own stamp,
   and I have no access to the machine.
6. **A line-length distribution** for the API arithmetic; 70 characters is
   ASSUMED and the bark bank would replace it.
7. **The latency literature's applicability.** All of it is voice assistants.
   No source I found measures tolerance for a GAME character's reply, where the
   player is not waiting in silence. Section 4.2's two-budget suggestion is
   DERIVED reasoning, not a cited finding.
8. **Not surveyed**: speech recognition, which the pipeline will also need if
   the player speaks rather than picks; Orpheus, Higgs, VibeVoice and Maya1,
   which appear in the 2026 roundups and were not examined because none of them
   is in the chatterbox family and the cloning requirement rules out the fixed
   voice sets.

## 8. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Resemble AI, "Chatterbox Turbo: Open Source, Ultrafast Text-to-Speech", https://www.resemble.ai/chatterbox-turbo/
- Hugging Face, "ResembleAI/chatterbox-turbo", https://huggingface.co/ResembleAI/chatterbox-turbo
- Hugging Face, "ResembleAI/chatterbox-turbo-ONNX", https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX
- GitHub, "resemble-ai/chatterbox", https://github.com/resemble-ai/chatterbox
- GitHub, "devnen/Chatterbox-TTS-Server", https://github.com/devnen/Chatterbox-TTS-Server
- GitHub, "DDATT/Chatterbox-turbo-cpp", https://github.com/DDATT/Chatterbox-turbo-cpp
- NVIDIA, "NVIGI Chatterbox TTS model card", https://docs.nvidia.com/ace-for-games/chatterbox-tts/nvigi-chatterbox-model-card.html
- NVIDIA, "Build On-Device AI Companions with the NVIDIA ACE Game Agent SDK and Unreal Engine 5 Plugins", https://developer.nvidia.com/blog/build-on-device-ai-companions-with-the-nvidia-ace-game-agent-sdk-and-unreal-engine-5-plugins/
- NVIDIA, "In-Game Inferencing", https://developer.nvidia.com/rtx/in-game-inferencing
- Communeify, "Unveiling Resemble AI's Chatterbox-Turbo", https://www.communeify.com/en/blog/resemble-ai-chatterbox-turbo-opensource-tts-realism-performance/
- aigazine, "AI Launches 350M-Parameter Chatterbox-Turbo for Real-Time Voice Agents", https://aigazine.com/startups/ai-launches-350mparameter-chatterboxturbo-for-realtime-voice-agents--s
- tryspeakeasy, "Best Open Source TTS Models in 2026: Kokoro, Chatterbox, Fish Audio Compared", https://www.tryspeakeasy.io/blog/open-source-text-to-speech-2026
- CodeSOTA, "Best TTS Models 2026: Open-Source Voice AI Compared", https://www.codesota.com/guides/tts-models
- Pinggy, "Best Open Source Self-Hosted Text-to-Speech Models", https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/
- localaimaster, "Best Local TTS Models 2026: 8 Open-Source Voices Tested", https://localaimaster.com/blog/best-local-tts-models
- BentoML, "The Best Open-Source Text-to-Speech Models in 2026", https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models
- AssemblyAI, "The 300ms rule: Why latency makes or breaks voice AI applications", https://www.assemblyai.com/blog/low-latency-voice-ai
- Telnyx, "What is Voice AI Latency? Typical Numbers, Standards and How to Measure", https://telnyx.com/resources/low-latency-voice-ai
- Hamming AI, "Voice AI Latency: What's Fast, What's Slow, and How to Fix It", https://hamming.ai/resources/voice-ai-latency-whats-fast-whats-slow-how-to-fix-it
- Picovoice, "Voice Agent Latency, Turn-Taking, and Barge-In", https://picovoice.ai/guide/voice-agents/voice-ux-latency-turn-taking/
- Tavus, "Factors affecting latency in real-time voice AI conversations", https://www.tavus.io/blog/voice-ai-latency
- Deepgram, "Best Text to Speech APIs: Pricing, Features and Comparison", https://deepgram.com/learn/best-text-to-speech-apis-2026
- futureagi, "Best Text-to-Speech APIs in 2026", https://futureagi.com/blog/best-text-to-speech-providers-2026/
- pkgpulse, "ElevenLabs vs OpenAI TTS vs Cartesia 2026", https://www.pkgpulse.com/guides/elevenlabs-vs-openai-tts-vs-cartesia-text-to-speech-2026
- texttolab, "Best Text to Speech API 2026: 12 TTS APIs Compared", https://texttolab.com/blog/best-text-to-speech-api

Repository sources, read this session at commit `074f85b`:
`game-design/live-speech-latency.md` (all 276 lines),
`game-design/voice-live/step-report.txt`,
`ledger-v2/research/license-allowlist.md`,
`ledger-v2/respec/vision-pillars-v2.md`, `canon.md`,
`game-design/decisions-pending.md`, `game-design/voice-casting-history.md`,
`game-design/production-plan-audio-art.md`, `game-design/roadmap-history.md`.
