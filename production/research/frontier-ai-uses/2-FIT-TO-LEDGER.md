# 2. What applies to LEDGER's five problems

Marks as in 1-WHAT-IS-NEW.md. "This PC": the Ryzen 5 5600X with an RX 6700 (10 GB, no CUDA) shared with the game and the voice, on Windows. "Cost": new money only; subscription usage is noted where large. "Licence": for a game that will be sold, including the NoAI ruling. Every idea is read against his rulings as they stand (RULINGS.md) and the project's earlier research, which the first version of this note missed (SOURCES.md, the independent check).

## Problem 1. Live talk: first sound 4.6 s against 2 s, and "that's all I know"

**Where it stands under his rulings** (7 October). Speech under two seconds was reported failed, as a blocked core capability. No third attempt at the voice, no cloud voice, the faster first sentence off, no prepared openings. A research step on the first sentence's check was proposed to him and recommended parked (DECISIONS.md, 7 October). No paid voice service (29 September).

**What sets the first sound today: the voice, not the check** [I, from LEDGER's own measurements, production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md]. With one model:
- the first sentence is written at 1.35 s (median);
- its check clears it at 2.96 s;
- the voice takes 2.2–4.4 s to make its first piece, working while the check runs;
- the first sounds came at 3.6–5.7 s, about the moment of writing plus the voice's time.

So even an instant check would barely move the first sound, as LEDGER's own proposal of 7 October says. His words that day, "the check on the first sentence, not the voice, sets the floor", hold for a fast cloud voice, not for the free voice he kept. **Nothing found in this period brings two seconds within his rulings.** What is left open is the writing time (proof 2), and the check's next model before Haiku 4.5 retires (proof 3).

**What the research shows.**

| Idea | Evidence | Where it stands |
|---|---|---|
| Speech-to-speech and full-duplex models (OpenAI's GPT-Live-1, SALMONN-duo, Context Spanning, NVIDIA's VoiceChat) | A fast front model speaks while a slow back end brings the facts [SS, ABS] | They speak before any check, are cloud voices (ruled out) or research-only, and would replace the cast's voices |
| Authored lines picked live (RePlay, Disney Research) | Median 383 ms against 2.6 s for its strongest comparison, which was left out of its user study. Against a fast small-model cascade, 8 listeners preferred it in 63% of ratings against 12%, on wait and pace; against a stronger one (6 listeners), 46% against 21%, not significant. It plays only pre-recorded lines [SHOWN, paper, checked here]. | No prepared openings (7 October); built on NVIDIA's PersonaPlex |
| A small checker for the first sentence (Enoki; LettuceDetect and TinyLettuce) | Enoki's fast encoder: 0.13 s a sentence at 69.1% F1, against 76.4% for its slow LLM version. The slowest pipeline compared took 11.95 s; others under a second. Hardware not stated [SHOWN, paper, checked here]. LettuceDetect's code is MIT; its weights' licence pages were unreached. | Matters only once the voice is fast. Less exact than the slow check. Training it with Claude's help is arguable under Anthropic's consumer terms, and he ruled no training on the router's answers (24 September). |
| The facts chosen before writing | **Already LEDGER's method.** Choosing the facts by code before writing cut "that's all I know" from 36 to a mean of 21.7 of sixty (30 September). Having the model plan its facts first was no better (18.3 against 21.7, p = 1.0) and added about a quarter of a second (DECISIONS.md, 30 September). Neither was measured for the check's time on the real path, the 7 October proposal's third direction. | Part of the parked check study |
| Starting work while the player types | 19% lower latency (Never Stop Thinking); 5.79 s to 4.60 s median (speculative execution, 6 Oct) [ABS] | Would move the writing earlier, not the voice. Small, and untried here. |
| Sonnet 5.5 in place of Sonnet 5 | "30%+ faster" output, same price [CLAIMED]; thinking off is now `between_tools`, and forced tool choice now errors [SHOWN]; the live talk still writes with Sonnet 5 (read here) | **Not ruled out:** the writing time adds straight to the voice's. Proof 2. |
| The check's next model | Haiku 4.5's retirement "not sooner than 15 October 2026", 60 days' notice [SHOWN]; Haiku 5.5 promised "in the coming weeks" [CLAIMED]; the risk register's W3 has no proof | **Not ruled out:** forced sooner or later. Proof 3. |

**"That's all I know."** Nothing new in this period goes beyond what LEDGER has measured:
- **Its own research** traced the empty answers to knowledge the characters were never given (production/research/grounded-dialogue-selection, 30 September). His tap was to write down what the street would know.
- **The failure seen in one shipped game** (players stating events in brackets, which the characters took as fact, Where Winds Meet [SS]) was found and closed here on 25 September. What the player says is not sent to the claim check at all (ClaimCheck.cs, read here).

**One new risk for live talk: quoted lyrics.** Canon forbids real lyrics. The talk's real-names rule already forbids naming "a band or singer" (RealWorld.cs), and a small-talk bench asks about music (ClaimBench). But a quotation names nobody, and nothing looks for one [I]. A Munich court reportedly found song lyrics reproduced by a chatbot infringing (GEMA v. OpenAI, November 2025) [SS]. Proof 4 tests it.

**Cost of talk** [I, from LEDGER's own measurements]:
- with one model, writing and checks cost about $0.026 a reply (7 October);
- at the pace played so far (15 replies an hour) that is about $0.39 an hour;
- heavy talk (60 an hour) is about $1.56.

The $0.57 and $2.28 in the 7 October note include the faster first sentence and a cloud voice, both ruled out. The binding constraint is time, not money.

Haiku 4.5 caches nothing under 4,096 tokens, so a shorter check prompt silently never caches [SHOWN]. Check `cache_read_input_tokens` on the real path.

## Problem 2. The look

**What does not help.**
- **World models and generated scenes** produce video or splats, not the street's geometry. HY-World's licence excludes the EU and UK, including use of its output. Lyra 2.0's weights are research-only. Marble's terms are unread and it is paid [SHOWN / SS].
- **Image-to-3D** waits by his 22 September ruling until hand-made props are the bottleneck. When it returns:
  - TRELLIS.2 and Pixal3D need NVIDIA cards with 24 GB or more;
  - Hunyuan3D is territory-limited;
  - the hosted services (Meshy, Tripo) do not disclose their training data, so the NoAI check cannot be made [SHOWN / SS].
  - **The licence allowlist lists TRELLIS 2 as MIT.** The research found its renderer, nvdiffrast, licensed for non-commercial use only, and its training data drawn partly from Sketchfab items now tagged NoAI [SHOWN, notes/HC]. The entry should be re-read before image-to-3D returns; it is his decision.
- **Neural "photoreal" filters:**
  - DLSS 5 is RTX 50 only, and AMD's machine-learning upscaling needs RDNA 4 [SS];
  - the open GAN filters were trained on another game's frames [SHOWN];
  - training one on LEDGER's frames would use the engine as training input to a generative AI, which the Unreal licence, 6(e), forbids (read from his PC on 3 October, production/research/terms-2026-10-03).

The look has to come from LEDGER's own assets, materials and light, as the asset plan says.

**What could help.**

| Idea | Evidence | This PC | Cost | Licence |
|---|---|---|---|---|
| **The gate as a fault screen, not a judge of the look.** The last approved frame beside each new one; one question per kind of fault. Use a model that sees 2560×1440 whole: Opus 5.5 and Sonnet 5.5 do; Haiku 4.5 shrinks it. | D3-Omni, VisionQ, clipping detection, RefGlitch [ABS]; "Claude is a poor QA agent" out of the box [SHOWN]; vision limits [SHOWN] | yes | subscription: about 4,800 tokens a frame | The allowlist reads Unreal 6(e) and Adobe 17(C) as barring MetaHuman and Mixamo people from a test of an AI; his 3 October ruling reads them as training clauses. His to settle — proof 1 |
| **Check the capture is live before judging it**: two frames a second apart must differ | Universal Modder's "Oracles" note: Windows capture froze while the game ran [SHOWN]. The tester already takes the game window's own pixels and falls back when they come back black (tools/ai-tester/play.py, read here); a frozen-frame check is not there [I]. | yes | none | none; a small addition beside the one-line fault in 4-FIVE-PROOFS.md |
| **Compare the whole level after every agent edit** (actors and positions) | Code4Scene: 35.8% of successful edits changed something else [ABS] | yes | none | none |
| **Assets and materials written as code by the model**, with mechanical checks (it compiles, the parts connect), then the gate | Nova3D, Procedura, MatLoom [ABS]; they concede texture realism | yes (Claude plus Blender) | none | none beyond Claude |

Already in LEDGER, so not new:
- **The recipes** (terrace-front.py, shop-room.py) already write assets as code. No paper shows such programs reaching the KCD2 bar [I].
- **Epic's PCG shape grammar**, with its language-model skill, is already in the asset plan, to try "when a whole district must be filled, not before" (production/research/asset-plan/1-BUILDINGS-AND-INTERIORS.md).

## Problem 3. Clothing

**Nothing new solves it.** No tool or paper from July to October 2026 shows a tailored men's jacket with a notched lapel in research [SHOWN, paper texts]. The commercial tools show no AI tailoring either, as far as search summaries go [SS].
- The research field's common base, GarmentCode, has a "SimpleLapel" collar but no front opening, facing or pocket. PatternGSL limits itself to "closed garments" [SHOWN].
- UE 5.8 adds round-trip cloth editing with CLO and Marvelous Designer [SHOWN]. Both cost money, and Marvelous draping was stopped on 2 October.

His 3 October ruling parks tailoring "until the tools catch up". This period's research confirms they have not. The plain clothes go on as ruled (MakeHuman's CC0 suits and coats refitted in Blender, 30 September; plain trousers, jumpers and shoes to his floor).

## Problem 4. Animation without NoAI assets

**Under his rulings**, poses come from MetaHuman's clips and Mixamo (3 October), and the sitting clips from last month's Mixamo harvest (7 October). The method for walking, turning and sitting was set on 6 October (production/research/sit-and-turn). The project's 14 September research on motion capture concluded "no, not now" (production/research/markerless-mocap).

What this period adds, as a fallback only if those clips fail the floor ("nobody frozen stiff"):

| Idea | Evidence | This PC | Licence |
|---|---|---|---|
| **Epic's markerless motion capture from one phone camera** (UE 5.8, June): sit, stand, turn and listen-idle filmed, solved offline onto the MetaHuman skeleton | Epic's documentation [SHOWN, checked here]; Experimental; Windows only; recommended card RX 6800 XT | Unknown: the RX 6700 is below Epic's recommendation | His own footage, so no dataset; **the plugin comes from Fab and its "Allows usage with AI" flag is unread** |
| **NVIDIA's Kimodo, RP weights** (March–April): text plus keyframes to motion | README [SHOWN, checked here]: trained on 700 hours of licensed studio capture; "most extensively tested" on RTX 3090, 4090 and A100; about 17 GB of video memory, or less with the text encoder on the processor | Unproven on AMD | Code Apache-2.0; weights under the NVIDIA Open Model License, whose text was unreached; a new tool enters only by a record naming its weights licence (24 September). **Never the SMPL-X version** (non-commercial). |
| UE 5.8 engine features: foot-plane retargeting, Motion Warping, Control Rig Physics | Release notes [SHOWN] | yes | Engine; already in the 6 October method |
| Generated gestures from speech | GENEA 2026: the best system 32% against 62% for motion capture [ABS] | | Not worth it |
| Excluded: HY-Motion, FlowHMR, GVHMR, PromptHMR, GEM-SMPL, anything trained on AMASS or HumanML3D | Licence files [SHOWN] | | Territory-limited or non-commercial |

## Problem 5. The way of working

| Idea | Evidence | Fit |
|---|---|---|
| **Epic's MCP server in the editor and its Claude Code plugin**: lights, materials, actors, PCG, automation tests, screenshots through the game camera | [SHOWN, checked here]. Three meta-tools keep the prompt cache warm. No authentication. Arbitrary Python. | Untried here; proof 5. Prompts on, commit first, never during a build. |
| **Agents write code or editor Python, not Blueprint graphs**, and inspect before editing | CraftBench-UE: 30–43 points better; OpenGameEval: +10–13 [ABS] | Already how the builder works [I] |
| **Seeded random worlds through both languages**, and deliberately broken copies, to test the port | **Already done.** LEDGER's gossip generator caught all 37 planted faults the hand-written rows missed (GossipFuzz.cs). The port audit of 5 October ran 651,000 random scripts and 30 planted breaks, 11 of which no test catches (production/audits/sweep-2026-10-05/port-vs-core.md). Decompilation research: code passing every test still diverged on random inputs 4.9% of the time [ABS]. | Nothing new; the open lines are a fault (4-FIVE-PROOFS.md, "Found on the way") |
| **A check after every change, and a stop** after about three identical failures | Universal Modder's "Oracles" note [SHOWN] | The same shape as LEDGER's two-tries rule |
| **Claude Code budget tactics**: workflows pause at a usage limit and resume, failing after the third pause; rarely needed instructions moved into skills that load on demand; Sonnet for helpers | Claude Code docs [SHOWN] | For the weekly allowance |
| **One session, few agents** | Parallel agent setups often ran slower than one agent (SquidAgent); elaborate harnesses gained nothing over a minimal one [ABS] | Supports CLAUDE.md's one production session |
| **Text inside files LEDGER did not make is data, never instructions** | Planted text steered reverse-engineering agents in 35 of 40 cases [ABS] | Downloaded assets, plugins, captures |
| *Not needed:* the tester reading the town's memory through an MCP server | The game already writes its own record of each walk, and the nightly report reads it (tools/nightly_walk.py, read here) | Nothing to add |

## What could not be verified

- **Every latency figure for LEDGER in this section** is arithmetic on LEDGER's own measurements, not a run.
- **The hardware behind Enoki's 0.13 s.**
- **Whether Epic's markerless plugin runs on an RX 6700, and its Fab flag.**
- **Whether Kimodo runs on an AMD card.**
- **The NVIDIA Open Model License's text; the small checkers' weights licences.**
- **Sonnet 5.5's real speed.**
