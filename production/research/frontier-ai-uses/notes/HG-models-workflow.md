> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand G: frontier models, and how one person directs them (July to October 2026)

Written 7 October 2026 by a research helper. About 30 minutes of searching.

Marks: [SHOWN] read on the vendor's or project's own page, docs or code; [ABS] arXiv abstract read through the API (the authors' own claim); [CLAIMED] an announcement or customer quote on a vendor page, not checkable; [SS] search summary only, a lead and not evidence; UNREACHED could not be opened; [I] my inference.

What I could reach: Anthropic's pages (www.anthropic.com, platform.claude.com docs, code.claude.com docs, support.claude.com), arXiv API, raw.githubusercontent.com, and GitHub web pages through WebFetch only. UNREACHED (proxy refused): openai.com, platform.openai.com, blog.google, deepmind.google, ai.google.dev, huggingface.co, openrouter.ai, artificialanalysis.ai, lmarena.ai, llm-stats.com, datacamp.com, mistral.ai, api-docs.deepseek.com, qwenlm.github.io, ollama.com, reddit.com, rocm.docs.amd.com. Nothing below about OpenAI or Google is concluded from those sites; where only search summaries exist, it is marked [SS].

---

## 1. Which frontier models came out, July to October 2026

### Anthropic (all [SHOWN] from platform.claude.com model pages and the announcements unless marked)

| Model | Released | Price in/out per million tokens | Context / max output | Notes |
|---|---|---|---|---|
| Claude Sonnet 5 | 30 June 2026 (just before the window) | $2 / $10 (the "introductory" price became permanent; the planned rise to $3/$15 on 1 Sept was cancelled) | 1M / 128K | Now "Legacy"; retirement not sooner than 30 June 2027. This is LEDGER's live-talk writer. |
| Claude Opus 5 | 24 July 2026 | $5 / $25 | 1M / 128K | Now Legacy. |
| Claude Fable 5.1 (and Mythos 5.1, same model, gated) | 1 Sept 2026 | $10 / $50, cache reads $0.25 | 1M / 128K | "For demanding reasoning and long-horizon agentic work". Thinking always on. |
| Claude Opus 5.5 | 22 Sept 2026 | $4 / $20, cache reads $0.20 | 1M / 128K | Default model in the docs. Thinking cannot be turned off; default effort `medium`. Fast mode $8/$40, "up to 2.5x" speed (research preview). |
| Claude Sonnet 5.5 | 28 Sept 2026 | $2 / $10, cache reads $0.20 | 1M / 128K | "30%+ faster" output than Sonnet 5 [CLAIMED]. Thinking off is now `thinking: {type: "between_tools"}`. |
| Claude Haiku 4.5 | 15 Oct 2025 (background) | $1 / $5, cache reads $0.10 | 200K / 64K | Still the current Haiku. Retirement "not sooner than 15 October 2026"; not deprecated; Anthropic gives at least 60 days' notice. LEDGER's claim checker. |
| Claude Haiku 5.5 | not released | unknown | unknown | Opus 5.5 and Sonnet 5.5 announcements both say it "will join the Claude 5.5 family in the coming weeks" [CLAIMED]. Not on the models page today. |

Benchmarks Anthropic publishes (all vendor-run, [CLAIMED] as results; the tables themselves [SHOWN]):
- Opus 5.5: Terminal-Bench 4.0 66.4% (xhigh), FrontierCode v1.1 54.4%, CursorBench 4.0 57.8%, GDPval-AA v2.1 1846 Elo, OSWorld 2.1 81.8% (partial), Humanity's Last Exam 67.7% with tools, "Chartography" chart reading 89.0% with tools. Anthropic itself says "benchmark margins have become a less reliable guide to real-world differences".
- Sonnet 5.5: Terminal-Bench 4.0 70.6% (Sonnet 5: 10.3%), CursorBench 4.0 55.5%, GDPval-AA 1844, OSWorld 2.1 80.1%, Chartography 61.6% without tools (Opus 5.5 64.4%). "First Sonnet model to beat Pokémon Red working only from screenshots".
- Long tasks [CLAIMED, customer quotes on the Opus 5.5 page]: Clio ran it "unattended" for "over 18 hours" across six repositories; Stripe: "one Claude Opus 5.5 session directed a dozen more sessions" on a multi-day rebase of 40 stacked pull requests, "All 40 passed CI the next afternoon"; Quantium: a task that took "38 prompts over four days came in at 11 prompts over three hours".
- Games and 3D [CLAIMED]: Opus 5.5 page: "A different tester had several Claude models build a game from a single prompt; Opus 5.5 scored higher than any other model on the strength of its graphics and polish." Sonnet 5.5 page: Epic Games (COO Daniel Vogel) says it "managed tens of thousands of lines of code for gameplay system architecture ... handled multi-hour tasks"; Unity says "the majority of Claude Sonnet 5.5's work passed" a runtime check and it "completed 90% of tasks in our multi-step Unity Editor and coding benchmark"; a creative coder: "When Claude Opus 5.5 sets the architecture ... I would feel confident in letting Sonnet 5.5 implement it." Opus 5 page (July): rebuilt a machine part as a FreeCAD model from a drawing by writing its own vision pipeline. Fable 5 (June, background): beat Pokémon FireRed "with vision alone".

URLs: https://platform.claude.com/docs/en/models/overview , https://platform.claude.com/docs/en/about-claude/model-deprecations , https://platform.claude.com/docs/en/about-claude/pricing , https://www.anthropic.com/claude-opus-5-5 , https://www.anthropic.com/claude-sonnet-5-5 , https://www.anthropic.com/claude-fable-and-mythos-5-1 , https://www.anthropic.com/news/claude-opus-5 , https://www.anthropic.com/news/claude-sonnet-5

### OpenAI (UNREACHED at source)
- "GPT-6 Astra": exists as a named competitor row on Anthropic's Opus 5.5 page, with figures "as reported by OpenAI": Terminal-Bench 4.0 57.9%, FrontierCode 53.3%, GDPval-AA 1542, AutomationBench 41.4%, HLE 57.2% with tools, Terminal-Bench-Science 64.6% [SHOWN that Anthropic prints these; the numbers are OpenAI's claims]. Also named in an arXiv abstract (Code4Scene, below) as narrowly leading a Unreal scene benchmark [ABS]. Release date and price: [SS] only, and the summaries disagree (3 or 4 September 2026; $10/$50 or $5/$25 per million). Claimed "best computer use model", OSWorld 2.0 72.6% [SS].
- "GPT-6 Sol": named on Anthropic's Sonnet 5.5 page (FrontierCode 49.3%, 52.1% at xhigh; GDPval-AA 1487; Chartography 53.6%; Anthropic notes OpenAI "recently fixed a bug that degraded image understanding in GPT-6 Sol") [SHOWN as printed by Anthropic].
- "GPT-5.6 Sol": named on both Anthropic pages (Terminal-Bench 4.0 37.3%).
- "GPT-6.1 Sol": I could NOT verify it. Only search summaries say it was released 29 September 2026 at $2/$10 per million with a 1.1M context [SS]. No reachable primary page; zero arXiv hits for "GPT-6.1".
- "GPT-6 Luna" at $0.10/$0.50 per million [SS only]. "GPT-Live-1" and "GPT-realtime-2.1" voice agents are named in an arXiv voice benchmark [ABS]. "GPT-Realtime-2" at about $0.15 to $0.20 per minute of conversation [SS].

### Google (UNREACHED at source)
- "Gemini 3.8 Flash": [SS] says 2 September 2026, 1M context, prices conflicting ($0.75/$3.75 or $0.375/$1.88). Named in arXiv abstracts: "leads editing" on Code4Scene, and "Gemini-3.8-Live" in two voice benchmarks [ABS]. "Gemini-3.1-Flash" was the best image-fault spotter in a game-clipping study [ABS].
- [SS]: Gemini 3.6 Flash and 3.5 Flash-Lite in July; Gemini 3.5 Pro announced in May but not shipped; Gemini 4 not released.

### Open-weight models
- Qwen3.8 (Alibaba): 2.4T-A95B on 12 August and 27B on 14 August 2026 [SHOWN, GitHub README of QwenLM]. Weights licence is "released with the model weights on Hugging Face" (UNREACHED); the GitHub repo itself is Apache 2.0 [SHOWN]. Neither size fits a 10 GB card [I]. RSIGame (arXiv, 30 Sept) reports Qwen3.8-27B with "experience internalization" beating GPT-5.5 one-shot on two game engines with 11x fewer tokens [ABS].
- Small sizes that would fit (background, before July): Qwen3.5 0.8B, 2B, 4B, 9B (2 March 2026) and Qwen3.6-35B-A3B (16 April) [SHOWN, same README]; Gemma 4 E2B, E4B, 26B MoE (4B active), 31B: existence [SHOWN] in google-deepmind/gemma code (`Gemma4_E4B`); release 2 April 2026 and an Apache 2.0 weights licence [SS]. gpt-oss-20b (Aug 2025): Apache 2.0, 21B with 3.6B active, "run within 16GB of memory" [SHOWN, openai/gpt-oss README]: too big for the 10 GB card alone.
- Llama 4 (April 2025, background): licence withholds rights for multimodal models from anyone domiciled in the EU (end users exempt) [SHOWN, LICENSE/USE_POLICY in meta-llama/llama-models]. Switzerland is not in the EU, but the models are far too large anyway.

---

## 2. Live talk (problem 1): what the model releases change

1. Sonnet 5.5 is the obvious successor to Sonnet 5 for the reply writer: same price, "30%+ faster" output [CLAIMED]. Anthropic publishes no time-to-first-token figures; independent measurements (Artificial Analysis and the like) were UNREACHED. Only a measurement on LEDGER's real path will say whether it moves the 4.6 s.
   Migration points [SHOWN, Sonnet 5.5 "what's new" page]: thinking `disabled` now returns a 400; send `between_tools` (allowed at low/medium/high effort). For "chat and other latency-sensitive work, start at `medium` or `low`". Forced `tool_choice` (`any`/`tool`) returns a 400: if LEDGER forces a tool to get structured replies, it must switch to structured outputs or `auto` plus `strict`. Thinking blocks are bound to the conversation; accounts created on or after 31 August 2026 get a 400 when earlier turns are edited and a thinking block is replayed. New safety classifiers can stop a reply with `stop_reason: "refusal"`; the code must handle it.
2. The claim check on Haiku 4.5: Haiku 4.5 is safe for now (not deprecated; at least 60 days' notice; earliest retirement date 15 October 2026, so not before December in practice [I]). Haiku 5.5 is promised "in the coming weeks" [CLAIMED]: the moment it ships, time it as the checker.
   Haiku 4.5's minimum cacheable prompt is 4,096 tokens (Opus 5.5/Sonnet 5.5: 512) [SHOWN, Claude API reference bundled with Claude Code]. A shorter claim-check prompt silently never caches. Worth checking `cache_read_input_tokens` on the real path [I].
3. No paid fast lane for Sonnet: fast mode exists only for Opus (5.5 at $8/$40), and Priority Tier is not offered on Opus 5.5, Sonnet 5 or Sonnet 5.5 [SHOWN, Claude API reference]. Opus 5.5 cannot turn thinking off, so fast mode does not suit a sub-2 s reply [I].
4. An LLM verifier can match a code verifier: in the VAmoS voice benchmark (29 Sept), an LLM-as-verifier checking spoken figures against requirements "agrees with a code verifier on 99.1% of checks" [ABS, arXiv 2609.38512]. That is offline accuracy, not latency.
5. Speech-to-speech cloud agents still fail at stateful work: APEX-Voice (28 Sept) reports none of GPT-Live-1, Gemini-3.8-Live, Grok-Voice-Think-2.0, Step-Audio3 or GPT-realtime-2.1 exceeds 25% Pass@1 [ABS, arXiv 2609.34973]. They also could not run the claim check before speaking, and LEDGER's voices are cast locally [I].

## 3. Cost of one hour of talk on each fast tier

Prices [SHOWN] from the pricing page; the conversation shape is my assumption [I]. Per exchange: about 10,000 tokens of stable prefix (character sheet, canon, memories) read from cache, 500 new tokens written to the 5-minute cache, a 150-token spoken reply, and no thinking unless the model forces it. "No cache" means all 10,500 input tokens at full price. 60 exchanges an hour is one a minute; 120 is fast back-and-forth.

| Reply writer | Warm cache, 60/h | Warm cache, 120/h | No cache, 60/h | No cache, 120/h |
|---|---|---|---|---|
| Haiku 4.5 | $0.14 | $0.29 | $0.68 | $1.35 |
| Sonnet 5 or 5.5 | $0.29 | $0.57 | $1.35 | $2.70 |
| Opus 5.5 (+~300 thinking tokens it cannot skip, assumed) | $0.81 | $1.62 | $3.06 | $6.12 |
| Opus 5.5 fast mode (assumed 2x every rate) | $1.62 | $3.24 | $6.12 | $12.24 |
| Fable 5.1 (+~300 thinking tokens) | $1.88 | $3.75 | $7.65 | $15.30 |

Claim check on Haiku 4.5 (3,000 tokens in, below its 4,096 cache minimum so uncached, 100 out): $0.0035 a check, about $0.21 an hour at 60 checks and $0.42 at 120. Sonnet as checker: about double.

So Sonnet plus a Haiku check costs roughly $0.50 to $1.00 an hour of continuous talk with a warm cache, and up to about $3 without one [I]. At LEDGER's $5 friends'-evening cap, money is not what binds; latency is [I]. Non-Anthropic fast tiers (GPT-6.1 Sol $2/$10, GPT-6 Luna $0.10/$0.50, Gemini 3.8 Flash $0.38 to $0.75 in) are [SS] only. GPT-Realtime-2 at about $9 to $12 an hour [SS] is around ten times the cost, and it bundles a voice LEDGER does not want.

## 4. Can these models judge images? (gate, look, clothes clipping)

What the vendor says [SHOWN, platform.claude.com vision doc]:
- Claude 4.7 and later (Opus 5.5, Sonnet 5.5, Fable 5.1) see images up to 2576 px on the long edge and 4,784 visual tokens; older models, Haiku 4.5 included, cap at 1568 px. A 2560x1440 game frame is exactly 92 x 52 = 4,784 patches, so it is seen at full resolution on the newer models and shrunk to about 1456x819 on Haiku 4.5 [I, from the doc's rule]. Cost per frame on Opus 5.5 is about $0.019 at API prices (4,784 tokens); on the subscription it counts against the weekly allowance.
- Listed limits: spatial reasoning is "approximate", counting "approximate", and "Claude cannot determine whether an image is AI-generated".

Studies [ABS]:
- VisionQ (30 Sept 2026, 2610.00666): 20 VLM judges asked which image is best on a named visual criterion. The strongest reach "only 63.1% accuracy (chance 32.2%)", and reliability "varies sharply across criteria". A DPO-tuned Gemma-4-E4B judge is released.
- D3-Omni / "OmniJudge or OmniBias?" (25 Aug 2026, 2608.24160): multimodal judges "confirm satisfied requirements far more reliably than they detect violated ones". In other words, they are biased towards passing work.
- Geometry clipping in game QA (28 July 2026, 2607.25921): six VLMs (Gemini, GPT, Qwen, Gemma, Llama, Ministral). All give "substantial false positives on ... near-contact geometry and partial occlusions"; Gemini-3.1-Flash is best; the authors recommend them only "as high-recall candidate filters", not standalone detectors.
- SWE-Game (27 Sept 2026, 2609.33678): on 100 agent-built games, executable checks reach 92.59% balanced accuracy against 78.41% for a video VLM judge; rubric-based visual scores correlate with human ratings at Spearman 0.829 over 200 clips.
- WorldAuditBench (30 Sept 2026, 2609.40325): anomaly hunting in Unreal Engine 5 and Three.js worlds (floating objects, walk-through walls). Success is 6.6% to 42.3%, against 83.4% for humans.
- Background (before July): TempGlitch (May): temporal glitches near chance for 12 VLMs. RefGlitch-Bench (April): giving a clean reference frame helps. Industrial study of 19,738 keyframes (March): precision 0.50, accuracy 0.72, and "a secondary judge model" adds only marginal improvement. R4-CGQA (March): VLMs are "not sufficiently accurate in judging fine-grained CG quality"; retrieving descriptions of similar images helps.
- Anthropic's own engineering post (24 March 2026, background, [SHOWN]): "agents reliably skew positive when grading their own work"; "Out of the box, Claude is a poor QA agent ... identify legitimate issues, then talk itself into deciding they weren't a big deal". What helped: a separate evaluator, explicit criteria, and "few-shot examples with detailed score breakdowns". https://www.anthropic.com/engineering/harness-design-long-running-apps

No benchmark I found measures "is this frame as photoreal as the Hook sheet / KCD2". No vendor publishes a photorealism-judging score [I].

LEDGER angle: the gate's reviewer is right to be a fresh agent, but the evidence says it will miss faults more often than it invents them. The studies suggest four things [I]:
- Ask criterion by criterion ("is any garment passing through the body in this frame, yes/no, where"), not "does it pass".
- Always show a reference frame beside the test frame.
- Calibrate the reviewer with a few of Jafar's past verdicts as worked examples.
- Treat it as a high-recall filter, backed by deterministic checks where any exist (penetration tests in Unreal, debug-object census).

Use a model of the 4.7-or-later generation for frames; Haiku downscales them.

## 5. Game-engine agents: new measured results (all [ABS], September 2026)

- CraftBench-UE (19 Sept, 2609.23142): 70 Unreal Engine tasks, deterministic checks, no LLM judge. On paired tasks, C++ completion beats Blueprint by 30.0 and 42.9 points; 42% to 50% of Blueprint submissions that pass asset checks still fail runtime assertions. LEDGER [I]: have agents write gameplay in C++ or editor Python, and judge by runtime assertions, not by assets existing.
- Code4Scene (29 Sept, 2609.36777): 190 Unreal scene build/edit cases, 14 agent setups. Fable 5.1 leads construction, Gemini 3.8 Flash editing, GPT-6 Astra overall. Best repair F1 is 0.527, and "35.8% of edits that fully recover the target still introduce unintended changes elsewhere in the scene". LEDGER [I]: after any agent edit to the street level, diff the whole level (actor list, transforms) against the previous version.
- GameLogicBench (18 Sept, 2609.21562), Godot: best 52.78%. Under Claude Code all twelve models do worse as scope grows. Without mutant-validated tests, "incorrect agent submissions passed", and agents copied code from public repositories when the network was open. This matches LEDGER's golden-row rule and its no-copying rule.
- OpenGameEval (1 Oct, 2610.02563), Roblox: best 51.7% single attempt, 39.4% five times out of five. Runs that inspect the objects first pass 9.8 to 13.4 points more often.
- SWE-Game (27 Sept): Opus 5 best on all five task types; all below 60/100. GameXpert-Bench (22 Aug, 2608.21833): agents are better at building than at "discovering defects, verifying runtime behavior, and preserving functionality across changes". A2Z GameSpec-Bench (30 Sept, 2609.39564): requirement-specific feedback improves fidelity by 10.9% relative to self-revision.

## 6. One person directing many agents (problem 5)

Tooling [SHOWN, code.claude.com docs, current]:
- Claude Code offers five ways to run work in parallel:
  - subagents;
  - agent view ("research preview");
  - agent teams ("experimental and disabled by default");
  - dynamic workflows (a script running many subagents, "up to 16 concurrent agents by default");
  - Projects (parallel cloud sessions, "public beta on Pro and Max").
  https://code.claude.com/docs/en/agents.md
- Usage limits: a workflow that hits the plan's limit "pauses rather than failing": agents wait for the reset, no new agents start, and it resumes on its own. It fails on the third hit, and "a weekly limit can reset further out". Controlled by `autoContinueAtUsageLimit`. This is a built-in alternative to anything that keeps retrying, like the 1 October stop-hook loop [I]. https://code.claude.com/docs/en/workflows.md
- Cost advice on the costs page: "Use Sonnet for teammates", "Keep teams small", and give simple subagents `model: haiku`. Move specialised CLAUDE.md instructions into skills, because CLAUDE.md "is loaded into context at session start" and skills "load on-demand only". You "can't turn off thinking on Opus 5.5, Sonnet 5.5, or the Fable models"; lower the effort instead. https://code.claude.com/docs/en/costs.md
- Subscription limits [SHOWN, support.claude.com]: Max has a five-hour session limit and a weekly limit "across all models" that resets at a fixed time per account. "Limit resets" are given occasionally, are spent when the user chooses, and restore either the five-hour or the weekly limit. They cannot be spent from Claude Code in the terminal (only on the web or Claude Desktop). The Opus 5.5 announcement (22 Sept) says five-hour limits were raised on Pro, Max, Team and seat-based Enterprise plans, and subscribers were given a saved reset [CLAIMED]. Background: on 6 May 2026 Claude Code's five-hour limits were doubled [SHOWN announcement].

Studies [ABS]:
- SquidAgent (6 Oct, 2610.08647): "existing parallel multi-agent systems often run slower than a single-agent baseline", because workers re-explore what the orchestrator already knew and outputs must be reconciled. Forking workers from the orchestrator's session and giving them a shared conventions block gave 2.6x wall-time over Claude Code.
- "How Much of a Harness ..." (30 Sept, 2609.40303): with equal time and the same model, elaborate multi-agent harnesses gave "no advantages over a single session of a minimal-harness coding agent".
- Personalized skills (10 Aug, 2608.10319): generic skills pooled across 13 developers helped most; skills distilled from one developer's history gave "small and inconsistent" gains.
- (Im)Paired Programming (29 July, 2607.26375): 54 students; agents raise completion but "harm users' code comprehension".
- AutoCompact (1 Oct, 2610.02163): learning when to compact context added 9.2 points on SWE-bench Verified. Context management matters on long tasks.

Game-dev practitioners: only [SS] (for example a "Claude Code Game Studios" template with 49 agents). No measured results reached.

LEDGER angle [I]:
- LEDGER's "one ordered list, one item at a time" is consistent with the evidence that more parallel agents and more harness often do not pay.
- The cheap wins on the weekly budget:
  - Trim the very long CLAUDE.md, which every session and subagent loads, by moving rarely needed sections into skills.
  - Run research helpers and mechanical subagents on Sonnet 5.5 at low or medium effort.
  - Keep Opus 5.5 at its default medium effort for building, and raise it only for hard items.
  - Let workflows pause at limits instead of looping.
  - Keep one saved limit reset for a crunch.
- Every full-resolution frame costs about 4.8k tokens. A review of three references plus ten frames is about 62k input tokens.

## 7. Small open models on this PC (RX 6700 10 GB, Ryzen 5 5600X, Windows)

- llama.cpp: release b11467 (7 Oct 2026) ships "Windows x64 (Vulkan)" and "Windows x64 (ROCm 10.0)" builds [SHOWN, releases page through WebFetch]. Its build docs say the RDNA2 override `HSA_OVERRIDE_GFX_VERSION` (needed for gfx1031 = RX 6700) "is not supported on Windows" [SHOWN, docs/build.md]. So Vulkan is the practical runtime on this card [I]. ROCm on Windows support for gfx1031 could not be checked (AMD docs UNREACHED).
- Speed: the community Vulkan scoreboard (llama.cpp discussion #10879, Llama 2 7B Q4_0) lists the RX 6700 XT at 1,051 tokens/s prompt processing and 83.9 tokens/s generation [SHOWN as community-reported; read through WebFetch]. No RX 6700 (non-XT) row. Expect less: 36 vs 40 compute units, 320 vs 384 GB/s [I]. So a 2,000-token prompt into a 7B model takes about 2 s on an idle card. A 2B to 4B model might take 0.7 to 1 s, but this card also runs the game and the voice, and nothing has been measured here [I].
- DirectML (LEDGER's TTS runtime) is "in maintenance mode ... no new functionality or feature updates are planned". Microsoft points to Windows ML on Windows 11 24H2+ [SHOWN, microsoft/DirectML README]. ONNX Runtime GenAI supports DirectML and lists Qwen, Gemma, Phi and gpt-oss; "AMD GPU" is "on the roadmap" [SHOWN].
- Candidates that fit beside the game: Qwen3.5-2B or 4B, Gemma 4 E2B or E4B (all background releases, March to April 2026). Licences: Gemma 4 Apache 2.0 [SS]; Qwen weights licence UNREACHED (repo Apache 2.0 [SHOWN]). None is marked NoAI as far as I saw, but the Hugging Face model cards were UNREACHED and must be read from the PC before any use.
- Uses [I]:
  - A first-pass local fault screener on renders at night, when the editor is closed (VisionQ's Gemma-4-E4B judge shows such a model can be tuned for judging, at 63% accuracy at best).
  - Possibly a local claim check, to remove the network round trip. Whether it beats Haiku over the network while the game and TTS share the GPU is unmeasured and doubtful.

## 8. What LEDGER could do with this (summary of angles)

1. Problem 1:
   - Measure Sonnet 5.5 with `between_tools` at low effort against Sonnet 5 on the real path.
   - Check that the claim-check prompt actually caches (Haiku's 4,096-token minimum).
   - Time Haiku 5.5 as the checker the day it ships.
   - Handle `refusal` and the 400s from forced `tool_choice` before migrating.
2. Problem 5: trim CLAUDE.md into skills; use Sonnet 5.5 for helpers; use workflows' pause-at-limit; keep a saved reset.
3. Gate and look:
   - Make the reviewer a high-recall, criterion-by-criterion checker that is shown the reference beside each frame and calibrated on Jafar's past verdicts.
   - Use a 4.7-or-later model so frames are seen at 2560x1440.
   - Add deterministic Unreal checks (penetration, debug-object census).
   - Diff the whole level after every agent edit (Code4Scene's 35.8%).
4. Unreal work: prefer C++ or editor Python over Blueprint assets for agent-written gameplay, verified by runtime assertions (CraftBench-UE).
5. Risks:
   - DirectML is frozen.
   - Haiku 4.5 will be retired eventually; watch the deprecations page.
   - Model names from OpenAI and Google in this period are unverified at source.
