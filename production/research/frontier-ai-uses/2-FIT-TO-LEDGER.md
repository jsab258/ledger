# 2. What applies to LEDGER's five problems

Marks as in 1-WHAT-IS-NEW.md.
- **"This PC":** the Ryzen 5 5600X with an RX 6700 (10 GB, no CUDA) shared with the game and the voice, on Windows.
- **"Cost":** new money only; subscription usage is noted where it is large.
- **"Licence":** for a game that will be sold, including the NoAI ruling.

## Problem 1. Live talk: first sound 4.6 s against 2 s, and "that's all I know"

**What does not help.** Every new speech-to-speech and full-duplex design speaks first and checks later: a fast front model talks while a slow back end brings the facts. That covers OpenAI's GPT-Live-1 [SS], SALMONN-duo, Context Spanning and Qwen-Audio-Agent [ABS]. LEDGER's design checks a sentence before it is heard, so these move the problem rather than solve it.
- The open full-duplex models are research-only or need an 80 GB GPU (NVIDIA VoiceChat-11B [SS]), or are CUDA-bound and trained partly on licensed telephone corpora (PersonaPlex [SHOWN]).
- The closed ones are new paid cloud accounts with the vendor's voices, so they would reopen "voices as chosen".
- **No shipped game was found with measured first-sound times, or with a check before speech** [SS]. LEDGER's design is stricter than what has shipped [I, from absence of evidence].

**What could move it.**

| Idea | Evidence | This PC | Cost | Licence | Verdict |
|---|---|---|---|---|---|
| **Name the facts, then check the first sentence locally.** Sonnet first emits the fact IDs it will use, in a fixed-schema structured output, then the line. Code checks the IDs belong to this character, and every name, place, time and number in sentence 1. A small encoder checks sentence 1 against only those one to three facts. Haiku keeps checking sentences 2 onward while sentence 1 plays, and takes over whenever the local check is unsure. | Structured outputs use constrained decoding; a schema compiles once and is cached 24 h, so a per-turn list of IDs would recompile each turn [SHOWN, Anthropic docs]. Enoki checks a sentence's claims in 0.11–0.13 s [SHOWN, paper; hardware unstated]. LettuceDetect/TinyLettuce detectors, 17M to 2B, MIT [SHOWN]. | Yes: the encoder on the processor, not the shared card [I] | none | MIT; **train it on sentences made from the simulation by code, not on Claude's output** (see below) | The one route found that attacks the floor itself (proof 1) |
| **Sonnet 5.5** in place of Sonnet 5 | "30%+ faster" output [CLAIMED]; same price; thinking off is now `between_tools`; forced tool choice now errors [SHOWN] | cloud | none | as today | Measure on the real path; part of proof 1 |
| **Start work while the player types**: retrieval and prompt assembly, and optionally Sonnet on the partial line | 19% lower latency (Never Stop Thinking); 5.79 s to 4.60 s median (speculative execution, 6 Oct) [ABS] | yes | wasted tokens on dropped drafts | as today | Cheap; part of proof 1 |
| A faster local voice: MOSS-TTS-Nano, or synthesising only the first clause | Apache-2.0, CPU, ONNX [SHOWN]; no first-audio figure published | yes (CPU) | none | Apache-2.0; accent by ear | Only matters once the check is fast. He ruled no third attempt at the voice (7 Oct), so this is his call. |

**The arithmetic, stated plainly** [I, from LEDGER's own measurements in production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md]. With one model (his ruling keeps the faster first sentence off), sentence 1 is written at 1.35 s median, and its check clears it 1.0–1.9 s later.
- A local check of about 0.1 s brings the moment the sentence is "cleared to speak" to roughly 1.45 s.
- **With a streaming cloud voice** (about 0.2 s to first audio), first sound would be about 1.65 s, inside 2 s with little to spare. Sonnet 5.5's claimed speed or starting while the player types would add margin.
- **With today's local voice** (1.6–4.4 s to make the first sound), it stays above 2 s, as LEDGER's own proposal of 7 October already says.

So a faster check is necessary but not sufficient. The 2 s exit also needs a faster first audio, which today means a paid cloud voice: a money and scope decision already on his page.

**"That's all I know."**
- Split the measurement before changing anything [I]. For each bench question, record:
  - whether the answering fact was in the prompt at all (retrieval);
  - whether, given that it was, the character still declined (abstention).
- Score each question twice, with sufficient facts and without, so over-cautious and over-confident answers show together ("Rethinking Faithfulness", 6 Oct [ABS]).
- "Pick the facts, then word them" makes every empty answer an explicit choice that can be logged.
- Add the Where Winds Meet failure to the test set: **a player stating something as fact must never make it a fact** [SS for the game; I for the test].
- Authored lines plus generated glue was faster and preferred in RePlay [SHOWN], but it may count as "prepared openings" under his 7 October ruling. That is his call.

**Cost of talk.** LEDGER's own measurements put writing and checks at about $0.026 a reply: roughly $0.57 an hour at the pace played so far, and $2.30 for heavy talk with a cloud voice (production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md). A helper's estimate from Anthropic's published prices, with a warm prompt cache, came lower, at $0.50–1.00 an hour (notes/HG-models-workflow.md). Either way the binding constraint is latency, not money.

Haiku 4.5 caches nothing under 4,096 tokens, so a shorter check prompt silently never caches [SHOWN]. Check `cache_read_input_tokens` on the real path.

**The licence trap.** Anthropic's Consumer Terms, which cover Claude Code on his Max plan, forbid using the Services "To develop any products or services that compete with our Services, including to develop or train any artificial intelligence or machine learning algorithms or models" [SHOWN, checked here, effective 8 Oct 2025]. Whether a small game checker "competes" is arguable. The clean route is to make its training sentences from the simulation by code:
- true sentences from real facts;
- false ones with the person, time or place swapped, or with something the character could not know.

## Problem 2. The look

**What does not help.**
- **World models and generated scenes** produce video or splats, not the street's geometry. HY-World's licence excludes the EU and UK, including use of its output. Lyra 2.0's weights are research-only. Marble's terms are unread and it is paid [SHOWN / SS].
- **Image-to-3D:**
  - TRELLIS.2 and Pixal3D need NVIDIA with 24 GB or more, depend on non-commercial nvdiffrast, and were trained on Objaverse-XL's Sketchfab subset, which raises the NoAI question.
  - Hunyuan3D is territory-limited.
  - The hosted services (Meshy, Tripo) do not disclose their training data, so the NoAI check is impossible [SHOWN / SS].
- **Neural "photoreal" filters:**
  - DLSS 5 is RTX 50 only, and AMD's machine-learning upscaling needs RDNA 4 [SS].
  - The open GAN filters reach just over 20 fps at 1080p on an RTX 4090, and were trained on GTA V frames [SHOWN].
  - Retraining one on LEDGER's frames would mean training a generative model on Unreal output, which the Unreal licence is reported to forbid [SS; the EULA was UNREACHED].

The look has to come from LEDGER's own assets, materials and light, as the asset plan says.

**What could help.**

| Idea | Evidence | This PC | Cost | Licence |
|---|---|---|---|---|
| **The gate as a fault screen, not a judge of the look.** Show the last approved frame beside each new one and ask criterion by criterion ("is anything floating, clipping, black, a debug object?"). Calibrate on planted faults and his past verdicts. Use a model that sees 2560×1440 whole: Opus 5.5 and Sonnet 5.5 do; Haiku 4.5 shrinks it. | WorldAuditBench, VisionQ, D3-Omni, RefGlitch [ABS]; "Claude is a poor QA agent" out of the box [SHOWN]; vision limits [SHOWN] | yes | subscription: about 4,800 tokens a frame | none | 
| **Prove the capture is live before judging it**: hash two captures a second apart; capture from the render target, not the desktop | Universal Modder's "Oracles" note: Windows capture froze while the game ran [SHOWN] | yes | none | none |
| **Diff the whole level after every agent edit** (actors, transforms) | Code4Scene: 35.8% of successful edits changed something else [ABS] | yes | none | none |
| **Epic's PCG shape-grammar skill** for facades and street furniture by rule, with the modules from the asset plan | UE 5.8 docs [SHOWN] | yes (editor) | none | Engine feature; the City Sample PCG content needs a Fab NoAI check |
| **Assets and materials written as code by the model**, with typed checks (compiles, parts connect), then the gate | Nova3D, Procedura, MatLoom [ABS]; they concede texture realism | yes (Claude plus Blender) | none | none beyond Claude |

LEDGER's recipes (terrace-front.py, shop-room.py) are already this method. The new parts are the mechanical checks and material programs, and no paper shows them reaching the KCD2 bar [I].

## Problem 3. Clothing

**Nothing new solves it.** No tool or paper from July to October 2026 shows a tailored men's jacket with a notched lapel, in research or commercially.
- **The research field cannot express a lapel.** Its common base, GarmentCode, has a "SimpleLapel" collar but no front opening, facing or pocket; PatternGSL limits itself to "closed garments" [SHOWN, paper texts and design file].
- **The commercial tools are paid** and show no AI tailoring [SS].

What exists:
- **FreeSewing's Jaeger,** an MIT sport-coat pattern with a lapel, which LEDGER's route has met before [SHOWN].
- **UE 5.8's round-trip cloth editing** with CLO and Marvelous Designer [SHOWN], but both tools cost money.

The honest reading [I]: the missing piece is the construction method (how studios build a tailored jacket, with the lapel modelled and skinned rather than simulated), not an AI tool. The project's own rule says research that method before another attempt. His 3 October ruling already parks tailoring "until the tools catch up". The research confirms they have not.

## Problem 4. Animation without NoAI assets

| Idea | Evidence | This PC | Cost | Licence |
|---|---|---|---|---|
| **Epic's markerless motion capture from phone video**: film sit, stand, turn and listen-idle, and solve them offline onto the MetaHuman skeleton | Epic's docs [SHOWN, checked here]; Experimental; Windows only; recommended card RX 6800 XT | **Unknown**: the RX 6700 is below Epic's recommendation; one evening's test | none | His own footage, so no dataset. **The plugin comes from Fab: read its "Allows usage with AI" flag first.** |
| **Kimodo, SOMA RP weights**: text plus keyframes to motion, BVH, then Blender, FBX and Unreal's IK retargeter; Motion Warping lands a sit-down on a given chair | README [SHOWN, checked here] | Unproven on AMD; offline on the processor with the text encoder there (under 3 GB of video memory) | none | Code Apache-2.0; weights NVIDIA Open Model License (text UNREACHED); trained on licensed mocap. **Never the SMPL-X version; never "drunk" prompts.** |
| UE 5.8 Motion Matching and Choosers on a database of LEDGER's own clips; foot-plane retargeting; Control Rig Physics for settling | Release notes [SHOWN] | yes | none | Engine features; the Game Animation Sample's data stays out |
| Captured or authored idle and listening clips, not live-generated gestures | GENEA 2026: the best generated gestures 32% against 62% for capture [ABS] | | | |
| Excluded: HY-Motion and its distillations, FlowHMR, GVHMR, PromptHMR, GEM-SMPL, anything trained on AMASS or HumanML3D | Licence files [SHOWN] | | | Territory-limited or non-commercial |

## Problem 5. The way of working

| Idea | Evidence | Fit |
|---|---|---|
| **Epic's Unreal MCP and Claude Code plugin** for the builder: lights, materials, actors, PCG, automation tests, screenshots from the game camera | [SHOWN, checked here]. Three meta-tools keep the prompt cache warm; no authentication; arbitrary Python. | Keep permission prompts on; commit before sessions; one Unreal session at a time |
| **The same server in a Development build**, with a few read-only C++ tools for the nightly tester: who noticed what, reply timestamps, frames from the render target | "Cooked and shipping game builds can host an MCP server" [SHOWN, checked here]. State checks agree with humans 92.6% of the time, a video judge 78.4% (SWE-Game) [ABS]. | Kept out of the friends' build. Every number comes from the real path, as CLAUDE.md asks. |
| **Agents write C++ or editor Python, not Blueprint graphs**; they inspect before editing | CraftBench-UE: 30–43 points better; OpenGameEval: +10–13 [ABS] | Fits the port and the tools |
| **Differential fuzzing of the C++ port**: seeded random worlds through the C# Core and the port, compared tick by tick; and **mutant checks** that the golden rows reject deliberately broken code | Decompilation research: passing every test still diverged on fuzz 4.9% of the time [ABS]. GameLogicBench: tests unchecked against mutants pass wrong code [ABS]. LEDGER's own review of 1 October found 12 one-line mutants of new C++ that the golden comparison passed. | Processor only; free |
| **An oracle after every change, and a circuit breaker** after about three identical failures | Universal Modder's "Oracles" note [SHOWN] | The same shape as LEDGER's two-tries rule; nothing new to adopt beyond the live-capture check |
| **Claude Code budget tactics**: workflows pause at a usage limit and resume, failing after the third pause; move rarely needed CLAUDE.md sections into skills that load on demand; Sonnet for helpers; keep a saved limit reset for a crunch | Claude Code docs [SHOWN] | Directly for the weekly allowance |
| **One session, few agents** | Parallel agent setups often run slower than one agent (SquidAgent); elaborate harnesses gave no gain over a minimal one [ABS] | Supports PLAN.md's one production session |
| **Treat text inside files LEDGER did not make as data, never instructions** | Planted text steered reverse-engineering agents in 35 of 40 cases [ABS] | Downloaded assets, plugins, captures |

## Something new LEDGER could do

1. **Measure "the town visibly knows them" from the game's own memory,** not from video. The Development-build tools above would let the nightly tester read who noticed the deed and who later mentioned it, then compare that with what was said aloud.
2. **A morning-picture fault screen.** Each day's three views compared with yesterday's and with the last approved frames (RefGlitch), before anything reaches his page.
3. **A lyrics guard in live talk:** characters never quote song lyrics or long copyrighted text (section 3, the GEMA rulings).

## What could not be verified

- **Every latency figure for LEDGER in this section** is arithmetic on LEDGER's own measurements, not a run.
- **Whether Enoki-style checking reaches 0.1 s on a 5600X.**
- **Whether Epic's markerless plugin runs on an RX 6700, and its Fab flag.**
- **Whether Kimodo runs here.**
- **The NVIDIA Open Model License's text.**
- **Sonnet 5.5's real speed.**
