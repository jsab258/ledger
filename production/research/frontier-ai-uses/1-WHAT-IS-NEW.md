# 1. What is new, July to October 2026, and what was actually shown

## Marks

- **[SHOWN]:** the evidence was read: released code, weights or licence pages, a vendor's own documentation, a shipped product page, or a paper's own reported experiment. A paper or README is still its authors' account; nothing here was run.
- **[ABS]:** an arXiv abstract, read through the arXiv API. The authors' claim only.
- **[CLAIMED]:** an announcement, vendor page or customer quote that could not be checked.
- **[SS]:** a search summary only. A lead, never evidence.
- **UNREACHED:** the host refused this session.
- **[I]:** this note's inference.
- **"Checked here":** this session re-read the source itself.

This cloud session could reach the arXiv API, GitHub, Wikipedia, Epic's documentation and Anthropic's pages. It could not reach OpenAI, Google and DeepMind, Hugging Face, Reddit, YouTube, X, the games press, the hardware sites or any legislation site. **Nothing about OpenAI's or Google's models is concluded here from their own pages.**

## 1.1 The models

| Model | Date | What its maker shows | Mark |
|---|---|---|---|
| Claude Opus 5 | 24 Jul 2026 | $5/$25 per million tokens | [SHOWN] |
| Claude Fable 5.1 | 1 Sep 2026 | $10/$50; thinking always on | [SHOWN] |
| Claude Opus 5.5 | 22 Sep 2026 | $4/$20. Thinking cannot be turned off. One line on games: "A different tester had several Claude models build a game from a single prompt; Opus 5.5 scored higher than any other model on the strength of its graphics and polish." No details. | [SHOWN, checked here]; the game test itself [CLAIMED] |
| Claude Sonnet 5.5 | 28 Sep 2026 | $2/$10, "30%+ faster" output than Sonnet 5. Thinking is switched off with `between_tools`; `disabled` now errors. | [SHOWN]; the speed [CLAIMED] |
| Claude Haiku 4.5 | (Oct 2025) | Still current. Retirement "not sooner than 15 October 2026", with at least 60 days' notice. Haiku 5.5 is promised "in the coming weeks". | [SHOWN]; Haiku 5.5 [CLAIMED] |
| "GPT-6 Astra" | early Sep 2026 [SS] | Exists as a competitor row on Anthropic's Opus 5.5 page, with figures "as reported by OpenAI". Price and date conflict between search summaries. | [SHOWN that Anthropic names it, checked here]; everything else [SS]; openai.com UNREACHED |
| "GPT-6.1 Sol" | 29 Sep 2026 [SS] | **Not verified.** No primary page; not on Anthropic's pages; no arXiv mention. | [SS] only |
| "GPT-6 Sol", "GPT-5.6 Sol" | | Named on Anthropic's pages as competitors | [SHOWN as named] |
| Gemini 3.8 Flash, Gemini 3.8 Live | Sep 2026 [SS] | Named in arXiv abstracts as baselines | [ABS] names only |
| Qwen3.8 (2.4T-A95B, 27B) | 12–14 Aug 2026 | Open weights; neither fits a 10 GB card | [SHOWN, GitHub] |

On 6 October Anthropic said its general models "have conservative cyber safeguards that block most cyber work", with binary reverse engineering under a verified tier [SHOWN]. Decompiling with them may be refused [I].

## 1.2 Decompiling, porting and modding games

| What | Who, date | Models and tools | Shown, or only claimed |
|---|---|---|---|
| **Wave Race 64 recompiled to native PC** | Daniel Gomes Vieira; releases 10–14 Sep | "Written by Claude ... in Claude Code" under his direction; N64Recomp. Phase gates with byte-matching checks; generated code is never hand-edited; faults found by instrumenting rather than guessing. | [SHOWN, README and plan]. Needs the user's own ROM; GPL-3.0. |
| **Fable 2 recompiled to PC** | himdo, Sep | A local Qwen3.8 27B booted it "after about an hour"; then "a large amount of human trial and error". Has a debug-only AI control channel: scripted input, a game-state reporter, frames captured from the renderer. | [SHOWN, README] |
| **Snowboard Kids 2 matching decompilation** | Chris Lewis; 100% on 30 May (background) | Claude Code in a loop, easiest functions first; stalled near 75% until functions were ranked and similar solved ones retrieved | [SS]; blog UNREACHED |
| AI-assisted Mario Kart Wii port; DK64 port "made without AI" | 15 Jul; 29 Aug | | [SS] |
| **"Recompile more, preserve less"** | arXiv 2609.05370, 4 Sep | LLM clean-up lifts the build rate from 75% to 90%, but behaviour-matching falls from 74% to 62%. Code that passes every test still diverges on fuzzed inputs (4.9%, up to 13%). | [ABS, checked here] |
| **Planted text steers reverse-engineering agents** | arXiv 2607.12507, 14 Jul | 35 of 40 adversarial cases | [ABS] |
| **Universal Modder** | rehan-remade; 30 Sep [SS for the date]; MIT | A Claude Code plugin. 57 game notes dated 28 Sep to 7 Oct, most self-labelled Opus 5.5: Minecraft inside GTA V, a Victoria 2 total conversion, a Terraria boss rebuilt as a simulator from the decompiled game. Its "Oracles" note (1 Oct): run a mechanical check after every change; stop after about three identical failures; prove the screenshot capture is live, because Windows capture returned byte-identical frames while the game ran. | [SHOWN, README and notes]; the mods themselves were not run |
| **The mashup wave** | from about 28 Sep | Games inside other games (Skate in Modern Warfare 2, Minecraft in Elden Ring). Many exist only as clips. | [SS]; press UNREACHED |
| Nexus Mods tightens AI tagging | about 1 Aug | | [SS] |

## 1.3 Agents in game engines and editors

| What | Who, date | What it is | Mark |
|---|---|---|---|
| **Unreal MCP in the UE 5.8 editor** | Epic, with UE 5.8 (June) | An MCP server inside the editor at 127.0.0.1:8000, "no authentication layer", Experimental. Clients listed: Claude Code, Cursor, VS Code, Gemini, Codex. Tools for actors, lights, materials, PCG, Blueprints, automation tests, screenshots, and any editor Python. **"Cooked and shipping game builds can host an MCP server by calling `IModelContextProtocolModule::StartServer()`."** | [SHOWN, checked here] |
| **Epic's Claude Code plugin** | Epic; MIT; in Anthropic's marketplace | Shows the model three meta-tools by default "so the prompt cache stays warm". Epic warns: arbitrary Python runs in the editor; don't skip permission prompts; commit before long sessions. | [SHOWN, README and licence] |
| **PCG skills for language models** | UE 5.8 docs | Including `Skill_PCGShapeGrammarDefinition`, for facades and street furniture along a path. Already in LEDGER's asset plan, for when a whole district must be filled. | [SHOWN] |
| MCP for Blender 2.1.9 | 6 Oct; MIT | A `look` tool; Poly Haven import; 3D generators (cloud); anonymous telemetry on by default | [SHOWN] |
| CraftBench-UE | arXiv 2609.23142, 19 Sep | 70 Unreal tasks. Agents' C++ beats Blueprint by 30–43 points; about half the Blueprints that pass asset checks fail at run time. | [ABS, checked here] |
| Code4Scene | 2609.36777, 29 Sep | Unreal scene edits: best repair F1 0.527. 35.8% of edits that reach their target still change something else. | [ABS, checked here] |
| GameEngineBench, GameLogicBench, OpenGameEval, SWE-Game | Jul–Oct | Best UE5 C++ pass rate 55.5%. Tests not checked against deliberately broken versions pass wrong code. Inspecting before editing adds 10–13 points. State checks agree with humans 92.6% of the time, against 78.4% for a video judge. | [ABS] |
| Opus 5.5 at 81.8% on OSWorld 2.1 (computer use) | Anthropic | Vendor-run | [CLAIMED] |

## 1.4 Agents that judge frames, and agents that play and test games

| What | Date | Result | Mark |
|---|---|---|---|
| WorldAuditBench: agents that walk UE5 and Three.js worlds on a fixed exploration budget, looking for floating objects, walls you can pass through and the like | 30 Sep | Agents find 6.6–42.3% of 213 planted anomalies; people 83.4% | [ABS, checked here] |
| VisionQ: 20 model judges pick the best image on a named criterion | 30 Sep | At most 63.1% (chance 32.2%) | [ABS] |
| D3-Omni: judges' bias | 25 Aug | They "confirm satisfied requirements far more reliably than they detect violated ones" | [ABS] |
| Clipping detection in game QA (six models) | 28 Jul | Many false alarms; use "as high-recall candidate filters" only | [ABS] |
| RefGlitch (background, April) | | Comparing with the last clean frame works best | [ABS] |
| Anthropic's harness post (background, March) | | "Out of the box, Claude is a poor QA agent", and grades its own work too kindly | [SHOWN] |
| Capcom's AI playtesting (CEDEC, 23 Jul) | | Agents play the shipped build through virtual input; crash traces deduplicated; a 9 AM summary each morning; "30,000 hours" a month automated | [SS]; pages UNREACHED |
| "GPT-6 Astra finishes Portal" | 6 Sep | 3,336 tool calls, $571, about 24 hours, with the game paused while the model thought | [SS]; unverified |
| PlaySuite, OmniGameArena | Jun–Oct | A gap between what agents perceive and what they then do | [ABS] |

**No study found measures whether a model can judge a game frame's photorealism against a concept image.** That is an absence of evidence, not proof none exists.

## 1.5 Generated worlds, 3D assets and garments

| What | Date | Shown | Usable for a sold game on this PC? |
|---|---|---|---|
| Video world models (Genie 3, Runway GWM Worlds 2) | Sep [SS] | Video only, no geometry | No |
| HY-World 2.x (Tencent) | Jul update | Meshes and splats [SHOWN] | **No.** The licence excludes the EU, UK and South Korea, including use of its output. Also CUDA, 80B models. |
| NVIDIA Lyra 2.0 | 20 Jul | [SHOWN] | **No:** research-only weights; H100 timings |
| World Labs Marble / Atlas | Sep [SS] | Splats and a mesh of about 600k triangles | Terms UNREACHED; paid |
| TRELLIS.2, Pixal3D (image to 3D) | 2026 | [SHOWN] | **Not now.** NVIDIA with 24 GB or more; its renderer nvdiffrast is non-commercial; trained on Objaverse-XL's Sketchfab subset (a NoAI question). LEDGER's allowlist lists TRELLIS 2 as MIT, and image-to-3D waits by his 22 September ruling. |
| Hunyuan3D-2.1 | | [SHOWN licence] | **No:** excludes the EU and UK |
| Meshy 7 and 7.1; Tripo P2.0 | Aug–Sep [SS] | Hosted, paid; training data undisclosed | The NoAI check is impossible |
| **LLMs writing assets as code** (Nova3D, 22 Jul; Procedura, 26 Aug; MatLoom materials, 30 Sep) | | Assets and materials as Blender programs; Nova3D meets 51 of 52 stated constraints and concedes texture realism | [ABS]. **Runs here today:** Claude plus Blender. |
| **Garments:** SewFusion, GarmentWeaver, PatternGSL, EASE, TailorCoPilot, EasyFashion | Jun–Sep | Full texts searched: **no tailored jacket with a notched lapel in any**. GarmentCode, the field's base, has a "SimpleLapel" but no front opening, facings or pockets. PatternGSL's own limits: "closed garments". | [SHOWN, paper texts] |
| CLO 2026 Pattern Drafter; Marvelous Designer 2026.1; Style3D AI | 2026 [SS] | No AI pattern-making for tailoring shown | Paid |
| UE 5.8 Chaos Cloth: CLO and Marvelous round-trip editing | Jun | [SHOWN, release notes] | Engine feature |

## 1.6 Motion

| What | Date | Shown | Licence for a sold game |
|---|---|---|---|
| **MetaHuman Animator Markerless Motion Capture** | UE 5.8, June | "Capture body, or both body and face performance from a single camera". Processed "locally on your machine". Experimental, Windows only, **installed from Fab**. Epic recommends an RX 6800 XT or better. | Epic tool, but **its Fab "Allows usage with AI" flag is unread** [SHOWN, checked here] |
| **NVIDIA Kimodo, SOMA "RP" weights** | Mar–Apr (background) | Text plus keyframes to motion, as BVH. "Trained on ... 700 hours" of licensed studio mocap (Bones Rigplay 1), not AMASS. About 17 GB of video memory, or under 3 GB with the text encoder on the processor. | Code Apache-2.0; weights under the NVIDIA Open Model License (the licence page itself UNREACHED). **The SMPL-X version is non-commercial.** "Most extensively tested" on RTX 3090, 4090 and A100. [SHOWN, checked here] |
| NVIDIA ARDY (real-time sibling) | 10 Jul | Streaming, steerable by text, waypoints or keyboard | As Kimodo; too heavy beside the game here [I] |
| GEM-X (video to motion); SAM 3D Body in ComfyUI | Mar; 23 Aug | Video-to-motion paths | Apache-2.0 / NVIDIA OML; SAM License [SHOWN]. CUDA, or plausibly ONNX [I]. |
| HY-Motion, MixiMotion, FlowHMR, GVHMR, PromptHMR, GEM-SMPL | | | **Excluded:** territory-limited or non-commercial [SHOWN] |
| GENEA 2026 gesture challenge | 11 Aug | Best speech-driven gesture system 32% against a 62% motion-capture ceiling | [ABS] |
| UE 5.8: IK retargeter foot plane, Motion Matching and Motion Warping (Production), Control Rig Physics (Beta) | Jun | [SHOWN, release notes] | Engine |

## 1.7 Speech and small models

| What | Date | Shown | Mark |
|---|---|---|---|
| OpenAI GPT-Live-1: full-duplex speech that "keeps talking" while a back end reasons | API from 10 Sep | $0.05 a minute plus the back end | [SS]; UNREACHED |
| SALMONN-duo; Context Spanning; Qwen-Audio-Agent | Sep | A fast front model speaks while a slow back end brings the facts | [ABS] |
| NVIDIA VoiceChat-11B | about 3 Aug | Full-duplex with tool calls; **"research purposes only"**; 80 GB GPU | [SS] |
| **RePlay** (Disney Research) | arXiv 2609.31588, 25 Sep | Plays only pre-recorded lines, picked from a cut-down PersonaPlex's hidden state: median 383 ms, against 2.6 s for its strongest cascade, which was left out of the user study. Against a fast small-model cascade, 8 listeners preferred it in 63% of ratings against 12% (on wait, pace and back-and-forth); against a stronger one, 6 listeners, 46% against 21%, not significant. | [SHOWN, paper; checked here] |
| **Enoki** | 2609.00581, 1 Sep | Checks a sentence's claims against evidence: its encoder version 0.13 s at 69.1% F1, against 76.4% for its slow LLM version; a rules version 0.11 s. The slowest pipeline compared (Claimify) took 11.95 s; the others under a second. The paper calls its timings a "relative comparison", hardware not stated. | [SHOWN, paper; checked here]. Licence file not found. |
| HallDetect | 6 Aug | A 435M entailment verifier in under 1 GB | [SHOWN, paper] |
| **LettuceDetect v2 / TinyLettuce** | Jun–Jul (v2) | Hallucinated-span detectors, 17M to 2B, "real-time on CPU" for the small ones | **MIT** [SHOWN, checked here] |
| Speculative execution for voice agents | 2610.07641, 6 Oct | Starts tool calls on partial speech: 5.79 s to 4.60 s median | [ABS, checked here] |
| MOSS-TTS-Nano (CPU, ONNX, voice cloning) | Apr (background) | | Apache-2.0 [SHOWN] |
| X2Streaming-TTS | Aug–Sep | 15.8 ms to first audio token, on TensorRT (NVIDIA) | Code MIT [SHOWN] |
| Shipped games with live LLM characters: Where Winds Meet, inZOI, Whispers from the Star | 2025–26 | No measured reply time was found in what could be reached; the games press was unreached, so nothing is concluded. In Where Winds Meet, players reportedly skipped quests by asserting events in brackets, which the characters took as fact. LEDGER found and closed the same failure on 25 September (ClaimCheck.cs). | [SS] |

## What could not be verified

- **Everything about OpenAI's and Google's models** beyond names printed by Anthropic or arXiv authors.
- **Every press report:** Capcom, the mashup wave, the Portal run, Nexus Mods' policy, DLSS 5.
- **Every Hugging Face model card and licence**, including the NVIDIA Open Model License text.
- **Every Fab listing,** including Epic's markerless motion-capture plugin.
