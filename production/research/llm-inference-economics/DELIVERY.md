# Local LLM inference economics

Research topic 19. Delivered to the studio. Nothing here is an instruction.

Scope split with the neighbouring topics, declared once: topic 2 asked what
FITS on the card (memory, a wall). Topic 17 asked what is FAST in the frame
(milliseconds, a negotiation). Topic 1 asked how the live speech stack should
be shaped. This one asks what it COSTS to run the language half, in dollars per
played hour if it is remote and in milliseconds and gigabytes if it is local,
and what the choice between those two commits us to.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

Egress, stated because it fails silently: `arxiv.org` is EGRESS_BLOCKED from
this container, measured 2026-09-14. That is the second research topic in this
queue blocked by it (topic 2 hit the same wall on the same class of paper), and
the single most relevant published work to this topic is behind it.

---

## Part 1. What this repository has actually built, which is not local

Every claim in this part was produced by a command run on 2026-09-14.

### 1.1 The conversation client is a cloud client

CITED, `ledger/Assets/Scripts/Core/LlmClient.cs`: the implemented client is
`AnthropicClient`, described in its own header as a "Raw-HTTP Anthropic Messages
API client", posting to `https://api.anthropic.com/v1/messages`. `ILlmClient` is
a one-method interface with `CompleteAsync`.

CITED, same file, `Models`: a two-tier routing table with a rate card in USD
per million tokens.

    public const string Core = "claude-sonnet-5";      // (3.0 in, 15.0 out)
    public const string Ambient = "claude-haiku-4-5";  // (1.0 in,  5.0 out)

described in the comment as "cheap/fast for the ambient population, stronger
for the authored core cast".

CITED, `Core/CostTracker.cs`: accumulates tokens per model and estimates spend,
with its header stating the target: "instrumentation is an M0 pass/fail
requirement (target: <= $0.05 per ambient played hour)".

DERIVED: there is no local inference path in this checkout. A grep across
`ledger-v2/`, `production/`, `game-design/`, `tools/` and the C# sources for
qwen, llama, mistral, phi, gemma, ollama, llama.cpp and gguf returns zero real
hits (every match is a hex commit sha or the substring "3b" in "rule 3b"). No
open-weight model has ever been named in this project.

### 1.2 The licence allowlist, which is law, has no category for a language model

CITED, `ledger-v2/research/license-allowlist.md`, read in full. It has six
SHIP-SAFE categories: voices, 3D, characters, faces, music, geodata. It has six
NEVER SHIP entries. It has three PROCESS rules, of which rule 2 is "New tool
adoption requires a decision record citing the weights license."

DERIVED, and it is the finding of this topic that costs nothing to fix and
everything to discover late: pillar 2 of the vision is a live LLM, and the
document CLAUDE.md calls law ("THE LICENCE ALLOWLIST IS LAW: nothing ships that
is not on it") does not contain a language-model category at all. A cloud API
is arguably out of its scope, since nothing is redistributed. A bundled
open-weight model is emphatically not, and would be the first thing in the game
whose licence the allowlist has never considered.

Also CITED from the same file, PROCESS rule 3: "At ship-prep: Steam generative-
AI disclosure for player-facing content (coding tools exempt)". A live
conversation model is the most player-facing generative AI a game can have,
under either path.

### 1.3 What a turn actually costs to send, measured rather than estimated

The prompt is assembled in `Core/ConversationEngine.cs:45`,
`BuildSystemPrompt`: the card block, then beliefs, then retrieved memories,
then a suspicion descriptor, then the scene, then a fixed rules block.

CITED, measured by running the project's own probe,
`dotnet run --project ledger/ConvoProbe -- --dry` on 2026-09-14:

    Lena Moreau id=lena     tier=core     sections=5 facts=4 prompt=5430 chars
    Rocco       id=rocco    tier=ambient  sections=4 facts=3 prompt=4701 chars
    Ada         id=ada      tier=ambient  sections=4 facts=3 prompt=4839 chars
    Sam         id=sam      tier=ambient  sections=4 facts=3 prompt=4581 chars

That is the CARD BLOCK only, four cards, 4,581 to 5,430 characters.

CITED, measured by extracting the `sb.AppendLine` string literals from
`BuildSystemPrompt`: 18 literals, 2,854 characters of fixed rules and labels.

DERIVED, and named for what it is a statistic OF: the FLOOR of one system
prompt, card block plus fixed rules, before a single memory or belief or scene
line is added, is 7,435 to 8,284 characters. At the usual four characters per
token that is roughly 1,860 to 2,070 tokens, sent on EVERY turn.

CITED, the output bound: `Core/ResponseValidator.cs:13`, `MaxChars = 900`, and
`LlmClient.cs:22`, `MaxTokens = 1024`. So a reply is at most 900 characters,
about 200 tokens.

### 1.4 The client does not use prompt caching

CITED: a grep of `LlmClient.cs` for `cache_control`, `cache`, `ephemeral` and
`anthropic-beta` returns nothing. The request body is built with `model`,
`max_tokens`, `messages` and `system`, and the only headers are `x-api-key` and
`anthropic-version: 2023-06-01`.

DERIVED: the fixed 7,400-character prefix per character is re-sent, and re-paid
for, on every turn. That prefix is exactly the shape prompt caching exists for.

### 1.5 The latency budget, and the half of it nobody has bounded

CITED, `game-design/m0-plan.md:64`: "Feel: reply latency <= ~4s to first spoken
word".

CITED, `game-design/live-speech-latency.md` (STATUS: SPEC, 2026-08-12): the
speech half's budget is "time from 'reply text exists' to the first audible
sample. Target under ~1.2s".

DERIVED: the language half therefore has roughly 2.8 seconds to turn a
2,000-token prompt into a 200-token reply, and no document in this checkout
states that as a budget. `ledger-v2/studio-v2/verification.md:46` plans the
gate ("Latency gate: live conversation budgets (first token, first audio) once
Phase 2 lands") and it does not exist yet.

### 1.6 The target has never been measured, and its denominator is undefined

CITED, `game-design/roadmap-history.md:219`: "Cost envelope telemetry (§9).
Target < $0.05/hour ambient, 'measured from day one.' CostTracker exists but no
per-hour readout."

CITED, checked today: still no per-hour readout. A grep of the C# sources for
`PerHour`, `usdPerHour` and `costPerHour` returns nothing, and
`game-design/sim-shots/verdict.txt` carries no token or cost key at all.

HOLE, and it matters for every number in Part 3: "per ambient played hour" is
not defined anywhere. It could mean an hour of ordinary play in which ambient
characters are occasionally spoken to, or an hour in which only the ambient
tier is used. Those are different denominators and they differ by an order of
magnitude. Part 3 prices both and says which is which.

### 1.7 The current design puts the key in the player's hands

CITED, `game-design/how-to-play.md` (STATUS: LIVE, verified 2026-08-04),
line 35: "F2 | API key entry (conversations are live LLM; get one at
console.anthropic.com)".

CITED, `game-design/roadmap-history.md:1075`: "LLM cost: deferred by the player,
explicitly not a build-time blocker. If we publish, the pricing models to weigh
are subscription, pay-as-you-go, cheap purchase plus a local model, or a
dedicated server. `ILlmClient` is a one-method interface precisely so none of
these is a rewrite."

DERIVED: the decision is on the record as DEFERRED, with four options named and
the abstraction built so that deferring is cheap. That is good engineering and
this topic is the evidence coming back for it. Note also that these are
pre-respec documents: `ledger-v2/` supersedes prior design docs, and nothing in
v2 has revisited the question.

---

## Part 2. The published figures for local inference

### 2.1 The paper that asks our exact question, and is blocked

CITED: "Fixed-Persona SLMs with Modular Memory: Scalable NPC Dialogue on
Consumer Hardware", arXiv 2511.10277. Small language models LoRA-fine-tuned to
encode a persona, paired with runtime-swappable vector memory modules that
preserve per-character context "without retraining or model reloading during
gameplay".
[arXiv abstract page](https://arxiv.org/abs/2511.10277) (EGRESS BLOCKED; the
figures below are from search summaries, not from the paper as read)

CITED, its measured figures, via search summary:

| variant | model | VRAM | disk | latency | TTFT |
|---|---|---|---|---|---|
| Jack | DistilGPT-2 | ~130 MB | ~0.4 GB | ~0.8 s | <0.2 s |
| Casper | TinyLlama-1.1B-Chat | ~807 MB | 2.73 GB | 1.7 to 1.9 s | <0.2 s |
| OliverS | Mistral-7B-Instruct | ~4.2 GB | 15.93 GB | 5.49 s | <0.2 s |
| OliverQ | Mistral-7B quantised | ~4.2 GB | 3.9 GB | 34.58 s | 0.70 s |

Memory module swap time: under 0.03 s, described as enabling "seamless and
imperceptible NPC instance switching during gameplay".

DERIVED against our own budget from 1.5: a 2.8-second language budget ACCEPTS
the 1.1B class at 1.7 to 1.9 s and REFUSES Mistral-7B at 5.49 s. The quantised
7B at 34.58 s is refused by a factor of twelve, and that row is the most
instructive in the table because it is counterintuitive: quantisation made it
twenty times slower, not faster, which is what a quantisation running partly
off the accelerator looks like. It is a warning that a size that fits is not
the same as a size that runs.

The sub-0.03 s memory swap is the single most architecturally relevant number
here. LEDGER needs 30 to 50 residents at phase 2, each with a card and a
distinct memory. One persona model plus swappable memory is exactly that shape.

### 2.2 What the hardware can do, and what nobody has measured

CITED: ROCm is mature on Linux for RDNA3 and later; for cards predating RDNA3
"the practical route is a Vulkan backend instead of ROCm".
[llama.cpp Vulkan performance discussion](https://github.com/ggml-org/llama.cpp/discussions/10879),
[llama.cpp ROCm/HIP performance discussion](https://github.com/ggml-org/llama.cpp/discussions/15021)

CITED, adjacent cards for scale: an RX 9070 XT decodes Llama 2 7B Q4_0 at
137 tok/s on Vulkan against 101 on ROCm; on RDNA3 and Intel Arc, Vulkan reaches
70 to 85 percent of CUDA's tokens per second on equivalent dense models.
[RDNA4 Vulkan vs ROCm benchmark](https://runaihome.com/blog/rdna4-vulkan-vs-rocm-local-llm-benchmark-2026/),
[AMD ROCm local LLM setup](https://localaimaster.com/blog/amd-rocm-local-llm-setup)

HOLE: no source found states a tokens-per-second figure for the RX 6700, which
is the card in `production/mesh-reports/mesh-machine-report.txt` and therefore
the only machine this project can measure on. It is RDNA2, so the Vulkan path
applies and the RDNA3 and RDNA4 numbers above are ceilings rather than
estimates. Two searches did not produce a number and I am not inventing one.

Worth noting as the counterweight: this project HAS run a transformer on that
card and measured it. `game-design/live-speech-latency.md:161` records
"RX 6700: pos10 34.5ms, pos100 45.1ms, pos200 59.3ms, pos400 89.5ms, 31.8ms
flat + 142us per position" for the speech model's decode step. The card is not
an unknown quantity for this class of work; it is an unmeasured one for this
particular workload.

### 2.3 Licences, which is where a local model can die after the engineering works

CITED, with the contradiction recorded rather than resolved: Qwen3 and Mistral
Small are reported under Apache 2.0, which permits commercial use and
redistribution with no royalty. Llama carries Meta's Community License with a
700 million monthly-active-user cap "plus the EU multimodal exclusion". Gemma
is described in one summary as Apache 2.0 and in another, in the same result
set, as "Google's Gemma Terms (more restrictive, review carefully)".
[HuggingFace blog, Best Open-Source LLM Models in 2026](https://huggingface.co/blog/daya-shankar/open-source-llms),
[Best Open-Weight AI Models 2026](https://vucense.com/dev-corner/best-open-weight-ai-models-2026/),
[Open Source LLM Comparison Table 2026](https://computingforgeeks.com/open-source-llm-comparison/)

HOLE, and the allowlist's own rule names the remedy: these are aggregator
blogs, they disagree with each other about Gemma, and the allowlist says
"verify weights license, not code license". Nothing here is a licence read. The
licence file itself, on the model card, is what a decision record would have to
cite.

DERIVED, and it is a direct precedent inside our own law: the allowlist already
bans Hunyuan3D outputs because of a territory exclusion, reasoning "given
Switzerland plus likely EU reach, treat as banned". Llama's reported EU
exclusion is the same shape of problem in the same jurisdictions. That is a
reason to read Llama's licence carefully before engineering against it, not a
verdict on it.

### 2.4 There is precedent for shipping a local model in a game

CITED: GladeCore, a plugin that lets players talk to NPCs by text or voice and
get unscripted in-character replies "driven by a language model that runs
entirely on the player's machine", shipping as an Unreal Engine plugin and a
Godot GDExtension, working offline.
[GladeCore on itch.io](https://lukaslicon.itch.io/gladecore)

CITED, in general terms and without a named title: at least one indie game has
shipped with a small local offline LLM for NPC dialogue.
[Local AI NPCs for Game Dev](https://localaimaster.com/blog/local-ai-game-npcs)

HOLE: the shipped game is not named in the summary and I could not identify it.
Treat the precedent as "tooling exists and is sold" rather than "a shipped
commercial title has done this", which is a weaker claim and the one the
evidence supports.

---

## Part 3. The arithmetic

All from the repository's own rate card in `LlmClient.cs`, and the measured
prompt floor from 1.3. Inputs stated so every step can be disputed: 2,000
tokens of system prompt in, 200 tokens of reply out.

### 3.1 One turn

| tier | uncached | with cache reads | cut |
|---|---|---|---|
| core, claude-sonnet-5 | $0.00900 | $0.00360 | 60% |
| ambient, claude-haiku-4-5 | $0.00300 | $0.00120 | 60% |

The cache rates: Anthropic charges 1.25x base input on a cache write with a
five-minute TTL or 2x for a one-hour TTL, and 0.1x on every read inside the
TTL, a 90 percent discount on input.
[Anthropic prompt caching pricing mechanics](https://technspire.com/en/blog/anthropic-prompt-caching-pricing-mechanics),
[Claude prompt caching, 5-min vs 1-hour](https://blog.sandbase.ai/anthropic-cache-pricing-5m-1h-explained/)

The cut is 60 percent rather than 90 because once input is nearly free the
OUTPUT dominates, and output is not cacheable.

### 3.2 One hour, on the production plan's own assumption

`game-design/production-plan-audio-art.md:33` assumes "20 conversations/hour,
~6 replies each", which is 120 turns per hour. Using that:

| mix | uncached | cached |
|---|---|---|
| all ambient | $0.360/hr | $0.144/hr |
| 20% core, 80% ambient | $0.504/hr | $0.202/hr |
| all core | $1.080/hr | $0.432/hr |

Against the repository's own target of $0.05 per ambient played hour:

| case | multiple of target |
|---|---|
| all ambient, cached | 2.9x |
| all ambient, uncached | 7.2x |
| 20% core, cached | 4.0x |
| 20% core, uncached | 10.1x |

### 3.3 Read the other way, which is the fairer reading

Turning it around removes the denominator ambiguity from 1.6. At the measured
prompt size, $0.05 buys:

- 42 ambient turns per hour WITH prompt caching
- 17 ambient turns per hour without it

DERIVED: the $0.05 target is not absurd. It is a target for a game in which the
player has about seven short conversations an hour, and it is unreachable for a
game in which they have twenty. Which of those LEDGER is has never been stated,
and the production plan's 20-conversation assumption dates from 2026-07-28 and
was written about TTS, not about this.

The lever with the best ratio of effort to effect is not the model tier. It is
the 2,000-token prompt floor. Caching it is a header and a marker, and it moves
every row above by 60 percent.

### 3.4 The local path, priced in the units it is actually paid in

A local model costs $0.00 per hour and its price is taken in three other
currencies.

- GRAPHICS MEMORY. Topic 2 put the street at roughly 6 GB (assumed, its own
  shakiest number) and the speech stack at 5.2 to 8.2 GB measured off disk, on
  a 9.98 GB card. Against 2.1's table, a 1.1B-class model at ~807 MB is the
  only row that could plausibly join that, and a 7B at ~4.2 GB cannot.
- LATENCY. The 2.8-second language budget from 1.5 accepts the 1.1B class and
  refuses the 7B class on the paper's numbers.
- CAPABILITY, and this is the one the other two hide. The job has two halves
  and they pull in opposite directions. Pillar 3 says "LLMs classify, never
  adjudicate", and closed-set classification is a small model's natural job.
  But `BuildSystemPrompt` also asks for period British dialogue under about
  fifteen style prohibitions at once, including "no dashes, no neat lists of
  three, no 'it's not just X, it's Y'", plus a hard rule against inventing a
  person. Holding many simultaneous negative constraints is exactly what small
  models are worst at.

HOLE, and it is the one that would decide this: nothing in this project has
ever tested a small model against `ResponseValidator` and the card prompts. The
probe that would do it already exists, `ConvoProbe`, whose `--dry` mode ran for
this topic in seconds, and `ILlmClient` is a one-method interface. The
experiment is one implementation of one method.

### 3.5 The third option the record already names, and this topic's view of it

`roadmap-history.md:1075` lists four shapes: subscription, pay-as-you-go, cheap
purchase plus a local model, or a dedicated server. The arithmetic above says
something about each.

A dedicated server means we pay 3.2's numbers per player-hour, for every player,
for ever. At $0.144 per hour all-ambient cached, a hundred players at twenty
hours each is $288. That is survivable at this scale and it is a recurring
liability that grows exactly as the game succeeds, which is the wrong shape for
a project with a small budget and no revenue plan.

Player-supplied keys, which is what `how-to-play.md` describes today, moves the
cost to the player and keeps the best models. It also puts a console account
between a player and the game, which is a barrier no game in the Meridian
Test's comparison set has.

A bundled local model moves the cost to the player's hardware, needs no account,
works offline, and raises the floor topic 2 already found uncomfortable.

Nothing here picks one. What the arithmetic does say is that the split does not
have to be all-or-nothing: the two-tier routing already in `Models` is the
natural seam. The ambient population is the volume, is the cheap half, and is
the half a 1.1B persona model plausibly serves; the named cast is the low
volume, is where the writing has to be good, and is where a remote model earns
its cost.

---

## Part 4. What could not be established

1. **The paper.** arXiv is egress-blocked, for the second topic running. The
   figures in 2.1 are search summaries of the only published work asking our
   exact question.
2. **Tokens per second on an RX 6700.** No source states one. Adjacent
   RDNA3/RDNA4 numbers are ceilings.
3. **What "$0.05 per ambient played hour" denominates.** Not defined anywhere.
4. **Any licence, as read.** Aggregator blogs, contradicting each other on
   Gemma. The allowlist's own rule requires the weights licence itself.
5. **A named shipped commercial game with a bundled local LLM.** Tooling is
   sold; a title was not named.
6. **Whether a small model can hold this prompt's constraints.** Never tested,
   and testable in one afternoon with tools that already exist.
7. **What a real turn costs in tokens.** Part 1.3 measures the prompt FLOOR.
   Beliefs, retrieved memories and scene context are added per turn and are
   unmeasured, so every figure in Part 3 is a LOWER BOUND on the true cost.

---

## Part 5. Findings and interpretation

### Findings

F1. The implemented conversation client is a cloud client posting to the
Anthropic Messages API, with a two-tier model table and a USD rate card. There
is no local inference path in this checkout.

F2. No open-weight model has ever been named anywhere in this project.

F3. The licence allowlist, which CLAUDE.md calls law, has no language-model
category. A bundled model would be the first shipped component its six
categories do not cover.

F4. Measured today with the project's own probe: card prompt blocks are 4,581
to 5,430 characters, and the fixed rules block is 2,854 characters, so a system
prompt floor is 7,435 to 8,284 characters, about 1,860 to 2,070 tokens, every
turn.

F5. The client does not use prompt caching. The fixed prefix is re-sent and
re-paid on every turn.

F6. The whole-chain latency budget is about 4 s to first spoken word and the
speech half claims about 1.2 s, leaving the language half about 2.8 s. No
document states that as a budget and the latency gate is planned, not built.

F7. The $0.05 per ambient played hour target has no per-hour readout, no landed
measurement, and no defined denominator.

F8. At the measured prompt floor and the repo's own rate card, 120 turns an
hour costs $0.36 all-ambient uncached, $0.144 all-ambient cached, and $0.504
mixed uncached: 2.9x to 10.1x the target.

F9. Read the other way, $0.05 buys 42 ambient turns an hour with caching and 17
without.

F10. Published figures put a 1.1B-class persona model at ~807 MB of VRAM and
1.7 to 1.9 s latency, and Mistral-7B at ~4.2 GB and 5.49 s, with a quantised 7B
at 34.58 s. Memory-module swap is under 0.03 s.

F11. The RX 6700 is RDNA2, so the Vulkan backend rather than ROCm, and no
tokens-per-second figure for it was found.

F12. Llama's licence reportedly carries an EU exclusion, which is the same
shape of problem that already put Hunyuan3D on the allowlist's NEVER SHIP list.

### Interpretation

I1. The cheapest large win available is prompt caching. It is a marker and a
header on a request the project already sends, it needs no model change, and it
moves every cost row by 60 percent. It is also the change that makes the
cloud-versus-local question a real choice rather than a forced one.

I2. The second cheapest is measuring, not deciding. `ConvoProbe` exists,
`ILlmClient` is one method, and nothing has ever put a small local model behind
it. Until that runs, every argument about local inference here, mine included,
is arithmetic on other people's benchmarks.

I3. The two-tier routing already in the code is the right seam and it was built
for cost, not for locality. Ambient local, named cast remote, is a shape the
architecture already supports without a rewrite.

I4. The finding with the longest fuse is the licence one. Engineering a local
model and discovering afterwards that its weights cannot ship is the exact
failure the allowlist was written to prevent, and it currently has no rule that
would catch it because it has no category for the thing.

I5. Every cost figure in Part 3 is a LOWER bound, because it prices the prompt
floor and not the memories and scene lines a real turn adds. That is the
direction that matters: the honest reading is that the real number is worse
than the table, not better.
