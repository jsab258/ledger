> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand B: AI agents in game engines and 3D editors, agents that judge by sight, agents that play and test games (July to October 2026)

Research helper report, 7 October 2026. About 30 minutes. Plain words.

Marks: [SHOWN] = I read the released code, licence, documentation page or shipped product page myself. [CLAIMED] = vendor page or press only. [ABS] = arXiv abstract read through the API (the authors' own claim; I did not read the paper body). [SS] = search summary only, a lead and not evidence. UNREACHED = could not be opened. [I] = my inference.

Reachability: github.com pages returned 403 to curl, but raw.githubusercontent.com worked, so READMEs and LICENSE files were read there. dev.epicgames.com and www.anthropic.com worked. UNREACHED: unrealengine.com, epicgames.com news, nvidia.com, pugetsystems.com, gamefromscratch.com, edge-online, automaton-media.com, invenglobal, openai.com, claude.com (one fetch got a summary, a later curl was refused), Wikipedia (rate-limited).

---

## Bottom line for LEDGER

1. **Epic now ships its own way for Claude Code to drive the Unreal 5.8 editor.** It is an experimental MCP plugin (MCP is the standard way an AI tool calls another program's functions) plus an MIT-licensed Claude Code plugin from Epic in Anthropic's official marketplace. It can take screenshots, move the camera, place lights, edit materials, PCG graphs and Blueprints, run automation tests, and run any editor Python. [SHOWN] It runs locally on this PC: the editor does the work and Claude only receives text and screenshots. It is the most directly useful item in this strand for problem 5. Its main risks: it has no authentication; it runs arbitrary Python inside the editor; and Epic itself warns against using it with permission prompts turned off.
2. **The same Epic plugin can run inside a packaged game build, with tools registered in C++.** [SHOWN, Epic docs] That gives the nightly AI tester a clean, official way to work: play a development build of LEDGER while also querying game state (who noticed what, reply timings) without screen-scraping. The build sent to friends must not contain it. [I]
3. **No study in the window measures whether a model can judge photorealism of a game frame against a concept image, or match a look by adjusting engine settings.** The nearest measurements all say model judges trail trained humans clearly. WorldAuditBench: models found 6.6 to 42.3% of anomalies, humans 83.4%. A 41-hour industrial study got 0.50 precision. 3D-DefectBench: the best of 12 models still trails trained labellers. A model looking at frames is useful for spotting faults, especially when compared with a known-good frame. It is not reliable as the judge of the look. That supports LEDGER's existing gate (fresh reviewer plus Jafar's eye). [ABS, I]
4. **Real-time "photoreal filters" do not fit this PC or this game.** DLSS 5 (neural rendering, available since 3 September 2026) is RTX 50 only [SS]. AMD's machine-learning features (FSR Redstone) need RDNA 4; the RX 6700 is RDNA 2 [SS]. The open GAN filters (REGEN, HyPER-GAN) were benchmarked on an RTX 4090 at just over 20 fps at 1080p inside UE5 [SHOWN, README]. Their pretrained weights come from GTA V frames plus Cityscapes/Mapillary, which taints the training data for a sold game. Training one on LEDGER's own frames would likely conflict with the Unreal licence clause on training generative AI with engine output (as CLAUDE.md records it). [I]
5. **Agents building or editing scenes still make unintended changes.** Code4Scene (29 Sep): even when an edit fully recovered the target, 35.8% of edits still broke something else. The best repair F1 was 0.527. CraftBench-UE (19 Sep): Blueprint deliverables were 30 to 43 points worse than C++, and about half of Blueprints that passed asset checks failed runtime tests. [ABS] For LEDGER: have agents write C++/Python rather than Blueprint graphs where possible, and check a scene-state diff after every agent edit to the street, not only a picture. [I]

---

## 1. Agents driving Unreal Engine

### 1.1 Epic's Unreal MCP plugin (UE 5.8, Experimental)
- **What:** an MCP server embedded in the Unreal Editor. Any MCP client (the docs list Claude Code, Cursor, VS Code, Gemini, Codex CLI) drives the editor over local HTTP at `http://127.0.0.1:8000/mcp`. Tools come from a "Toolset Registry" (examples named: `ActorTools`, `SceneTools`, `MaterialInstanceTools`, `ObjectTools`). Custom tools can be written in Python (`unreal.ToolsetDefinition`) or C++ (`UToolsetDefinition`). The API includes `MakeImageResult`, so a tool can return a picture to the model. Calls run serially on the game thread. Transport is HTTP/SSE only, there is no authentication, and it binds to loopback only. Epic says "many features are incomplete or missing" and the APIs may change. [SHOWN: dev.epicgames.com "Unreal MCP in Unreal Editor" page and the ModelContextProtocol API page, read 7 Oct]
- **Packaged builds:** "Cooked and shipping game builds can host an MCP server by calling `IModelContextProtocolModule::StartServer()` at startup". Registry toolsets are not auto-discovered there, so tools must be registered with `IModelContextProtocolModule::AddTool()`. [SHOWN, same page]
- **Who/when:** Epic Games. UE 5.8 came out with the State of Unreal keynote, Unreal Fest Chicago, 17 June 2026; the release date is given as 18 June. [SS] At that event Epic also said AI models will be a core pillar of UE6 (Early Access targeted for late 2027), and it showed agents in UEFN. [SS]
- **Shown vs claimed:** the documentation and API are real and readable. Epic's stage demo (Claude Code pulling objects from a library, placing them and adjusting lighting) I know only from press. [SS] An independent hands-on by Puget Systems (Kelly Shipman, 9 July 2026) tested rooms, Blueprint lighting interactions, controls and a PCG city. Its verdict per the summaries: "some systems were accessible, others were not … early in its maturity". The page was UNREACHED. It names "Claude Opus 4.8", which I could not verify. [SS]
- **LEDGER angle:** problem 5 directly, problem 2 partly (lights, materials, post-process, camera and screenshots are all scriptable from Claude Code). It runs on this PC: it is part of the engine, uses no extra GPU beyond the open editor, and has no cost beyond the existing subscription. Licence: it ships in Unreal itself; no NoAI question, because it is an engine feature, not a Fab item. [I] Data caution [I]: screenshots and scene data go to Anthropic for each call. CLAUDE.md records that the Unreal licence forbids using the engine or MetaHumans as training input for generative AI. Check that the subscription's "help improve the model" (training) setting is off before long MCP sessions that send MetaHuman frames.

### 1.2 Epic's "Unreal Engine Skills for Claude Code" plugin
- **What:** an Epic-published Claude Code plugin (MIT licence, "Copyright (c) 2026 Epic Games, Inc."), in Anthropic's official marketplace. It contains one skill (`unreal-mcp`) and a SessionStart hook. It needs the `ModelContextProtocol` and `AllToolsets` plugins enabled; it claims "hundreds of tools … across 30+ toolsets". These cover actors, Blueprints, materials, meshes, Niagara, Control Rig, Sequencer, State Trees, UMG, GAS, automation tests, and "Editor: screenshots, camera control … log inspection". Install: `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official`. [SHOWN: README, SKILL.md and LICENSE read on raw.githubusercontent.com, repo EpicGames/unreal-engine-skills-for-claude-code-plugin]
- **Details that matter:** by default the server shows only three meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`) "so … the prompt cache stays warm". That saves context and usage budget. An optional proxy keeps the session alive while the editor restarts. On Windows the hook needs Git Bash or WSL, though the tools work without it. Epic's own warnings: `ProgrammaticToolset.execute_tool_script` "executes arbitrary Python inside the editor process"; "Localhost is not a trust boundary"; "Prefer not to run Claude Code with `--dangerously-skip-permissions` while this plugin is loaded"; save and commit before any long session. [SHOWN]
- **LEDGER angle:** problem 5. It is the cheapest official route and fits "of two fine ways, take the cheaper". The builder session alone should use it, because it needs the open editor and the graphics card. [I]

### 1.3 Epic's PCG skills for LLMs, and the City Sample PCG + MCP demo
- **What:** UE 5.8 docs "Working with PCG and LLMs using Unreal MCP" list five skills. They are `Skill_PCGGraphGeneration`, `Skill_PCGShapeGrammarDefinition` ("rule-driven sequence of modules … along a path", which covers facades and street furniture), `Skill_PCGMeshPartition`, `Skill_PCGInstancingOnMeshActor` and `Skill_PCGBiomeCore`. A separate page shows the City Sample PCG driven by an LLM: building heights, styles and eras, road widths, plus a "Default Lighting Outdoor skill" that lights by location and time. Marked Experimental. The docs do not mention the model looking at screenshots in this loop. [SHOWN via WebFetch summary of the dev.epicgames.com pages]
- **LEDGER angle:** problem 2, facades and street dressing done by rules rather than by hand. The facade modules must still come from LEDGER's asset plan. Before any use, even as a reference, check the City Sample PCG content's Fab "Allows usage with AI" flag, under the NoAI rule. The skills themselves are engine documentation. [I] It runs on this PC (in-editor).

### 1.4 Third-party Unreal MCP servers (for comparison)
- **ChiR24/Unreal_mcp:** MIT, TypeScript plus a C++ "Automation Bridge" plugin, UE 5.0 to 5.8 ("5.8 preview validated"). `control_editor` covers PIE, camera, viewport and screenshots; it has optional token auth, which Epic's lacks. [SHOWN, README and licence badge]
- **atomantic/UEMCP:** MIT, uses UE's built-in Python remote execution (no C++ plugin to compile); `viewport_screenshot`, `viewport_camera`, `viewport_render_mode`; Windows via WSL or Git Bash. [SHOWN, README]
- **StraySpark** sells Unreal and Blender MCP servers; its complete bundle is $1,299. [SS] That is money, and not needed now that Epic's is free. [I]
- **LEDGER angle:** these add nothing important over Epic's official plugin for UE 5.8. Keep one as a fallback if Epic's experimental plugin breaks. [I]

### 1.5 Benchmarks of coding agents inside Unreal (all [ABS])
- **CraftBench-UE** (Wu, Calderone, Tsen; arXiv 2609.23142, 19 Sep 2026): 70 tasks (C++, Blueprint, editor scripting), deterministic build, asset and runtime checks, no model judge. On paired tasks, C++ completion beat Blueprint by 30.0 and 42.9 points. Among Blueprints that passed asset checks, 42.2% and 50.0% failed runtime assertions.
- **Code4Scene** (Ye et al.; 2609.36777, 29 Sep 2026): 190 Unreal scene construction and editing cases. Best repair F1 0.527. 35.8% of edits that fully recover the target "still introduce unintended changes elsewhere". It names "Claude Fable 5.1" (a real Anthropic model: anthropic.com lists it on 1 Sep 2026), "Gemini 3.8 Flash" and "GPT-6 Astra" (I could not verify the last two).
- **GameEngineBench** (La et al.; 2607.03525, 3 Jul 2026): 110 C++ tasks in nine real UE5 projects; best pass@1 55.5%; 31 tasks unsolved by every model.
- **Code2Games** (Wu et al.; 2610.05033, 4 Oct 2026): Blender world, then UE5 adaptation fixed by compile, runtime and test feedback.
- **SPEAR** (Roberts, Richter et al.; 2607.06701, 7 Jul 2026; MIT code, CC0 assets) [ABS + SHOWN README]: a Python library that controls any UE application through a plugin and exposes over 14K UE functions. It renders 1920x1080 frames straight into NumPy at 73 fps, with material IDs and shading buffers, and includes one example of "editing scenes using natural language via an AI coding assistant". Its demos use Epic sample projects, including the Game Animation Sample, which LEDGER may not touch.
- **AutoUE** (2603.07106, March 2026; background): multi-agent UE game generation with an automated play-test pipeline.
- **LEDGER angle:** problem 5 (how to let agents work). Prefer C++ and Python over Blueprint graphs for agent-written work. Test runtime behaviour, not only that an asset exists. Diff the level's actor and property list after every agent edit. [I]

---

## 2. Blender, Unity, Godot

### 2.1 MCP for Blender (formerly blender-mcp, by Siddharth Ahuja)
- **What:** MIT. The PyPI package is now `mcp-for-blender`, version 2.1.9 released 6 Oct 2026, with five releases on 5 and 6 October. [SHOWN, PyPI JSON and README] Its `look` tool returns the viewport, the camera view, an auto-framed multi-view sheet or an animation strip, in solid, material or rendered shading. It can search and import from Poly Haven (CC0), Sketchfab and Poly Pizza, and generate 3D models through Tripo, Hunyuan3D or Hyper3D Rodin. `BLENDER_MCP_SAFE_MODE=1` blocks risky scripts. Telemetry: a minimal anonymous usage record by default (tool name, success, timings, versions, OS); prompts, code, screenshots and "trajectory" data only after opting in. It can be fully disabled by an environment variable. [SHOWN]
- **Successors:** StraySpark's paid "Blender MCP Server" v2/v3 (claimed 228 to 404 tools, vision and async jobs; v3 said to be 31 July 2026). [SS]
- **LEDGER angle:** problem 3 (clothing session in Blender) and problem 2 (props made "in Blender from real-world photographs"). It runs on this PC; it is the clothing session's tool. Licence cautions [I]: 
  - Turn the anonymous telemetry off too.
  - Use only Poly Haven (CC0) through it. Sketchfab items need a per-item licence and NoAI check.
  - The AI generators (Hunyuan3D, Tripo, Rodin) are cloud services. Their outputs fall under their own terms, and Hunyuan3D's licence has historically excluded the EU, UK and South Korea (background, not re-checked here). Keep them off for LEDGER.

### 2.2 Research on agents that see their own Blender renders ([ABS])
- **3DHarnessBench** (Liu, Gong, Parakkat, Ovsjanikov; 2609.06535, 6 Sep 2026): uses Blender MCP. Recovering geometry improves "significantly with richer function call access", but the gain is "strongly model-dependent".
- **Thinking in Blender / SEIG** (He, Luo, Ma, Averbuch-Elor; 2606.02580, 1 Jun 2026): rebuilds a scene from one image as a Blender program in stages (geometry, materials, composition, lighting). Staging "substantially improves" fidelity.
- **PhotoFlow** (Guo et al.; 2605.23771, 22 May 2026): a Director, Reviewer and Reflector agent picks camera shots in Blender scenes under a six-render budget. It beats one-shot and random search on the authors' benchmark of 47 scenes and 141 missions.
- **3DCodeBench** (Gao et al.; 2606.01057, 31 May 2026): 12 vision models writing procedural modelling code. Failures are mostly API mismatches; successful renders "still suffer from disconnected or floating" parts; more thinking and multi-turn refinement help.
- **4DCodeBench** (2610.03715, 2 Oct 2026), and VIGA / BlenderBench (2601.11109, Jan 2026; background).
- **LEDGER angle:** the code, render, inspect loop helps, but on object-level tasks with numeric targets, not on judging the look of a street. [I]

### 2.3 Unity and Godot
- **Unity AI open beta**, with an official MCP server for Unity 6, announced 11 May 2026; clients include Claude Code. [SS]
- **"Godot AI"** MCP add-on, from the makers of "MCP for Unity". [SS]
- **GameCraft-Bench** (2606.17861, 16 Jun 2026): 140 Godot tasks; the best agent scored 41.46%. Agents "struggle to deliver complete games with … functional visual feedback, and coherent presentation". [ABS]
- **LEDGER angle:** none directly (LEDGER is on Unreal). It only shows that every major engine now has an official MCP route. [I]

---

## 3. Agents that work by sight: how well do models judge frames?

| Study | Date | What was measured | Result [ABS] |
|---|---|---|---|
| 3D-DefectBench (Zhao et al., 2607.10826) | 12 Jul 2026 | 12 model judges, 84 pipeline designs, about 3.2M defect decisions on 3D assets | Best model "still trail[s] trained human labelers"; texture agreement drops on noisier labels; a six-view RGB set is as good as denser views or added depth and normals |
| WorldAuditBench (Jiang, … Jaakkola et al., 2609.40325) | 30 Sep 2026 | 213 anomaly tasks (floating objects, walk-through walls, out-of-place objects) in 13 UE5 and Three.js worlds | Agents 6.6 to 42.3% success; humans 83.4% |
| RefGlitch-Bench (Yu et al., 2604.11082) | Apr 2026 (background) | Glitch detection with a reference frame | Comparing with the "LastCleanFrame" performed best and transferred across models; it also improved results on real gameplay |
| VLM visual bug study (Lu, … Bezemer, 2603.22706) | Mar 2026 (background) | 19,738 keyframes from 41 hours of industrial QA video | Precision 0.50, accuracy 0.72; a second judge and retrieval of past bug reports gave "only marginal" gains |
| SceneCritic (2604.13035) | Apr 2026 (background) | Model judges of 3D room layouts | Model scores are "sensitive to viewpoint, prompt phrasing, and hallucination"; a symbolic checker agrees better with humans |
| Lumera (Chen et al., 2607.20889) | 23 Jul 2026 | Recovering UE5 lights from one image | Light recall 0.998, but per-light F1 0.209 at 0.5 m; colour error median ΔE 4.59; intensity r = 0.628. Built from "2,513 UE5 projects" of unstated origin, so treat the data as possibly tainted |

- **Vendor numbers:** Claude Opus 5.5 (22 Sep 2026) scores 81.8% on OSWorld 2.1 (computer use) and 89.0% on Chartography (with tools). One early tester said it "scored higher than any other model on the strength of its graphics and polish" when building a game. [CLAIMED, anthropic.com page read]
- **Not found:** in the window I found no measured study of a model judging the photorealism of game frames against a concept image, or iterating lighting and materials in an engine to match a reference look. A search of arXiv titles and abstracts and of the web turned up only the studies above. Absence of evidence, not proof none exists.
- **LEDGER angle (problem 2 and the gate):** models looking at frames are a fair screen for visible faults such as debug objects, black squares, floating props and holes. They are best when each frame is compared with an approved earlier frame of the same camera, the RefGlitch method. That fits LEDGER's rule "nothing reaches his page with a visible fault". They are not a trustworthy judge of "would this pass in a 2026 game". Expect roughly half of their fault flags to be false; they miss many anomalies. The fresh reviewer and Jafar's eye stay the judges. [I]

---

## 4. Vision agents that play and test games

- **Capcom, CEDEC 2026 (23 July 2026)** [SS; pages UNREACHED]:
  - Agents play the shipped build of *Monster Hunter Stories 3* through virtual keyboard and controller input only. They do not read the game's internal data, because shipped builds have the debug code stripped.
  - Work is split across terminals by role (story, combat, field). Start and end conditions, prompts and frequency are set per task.
  - Crash stack traces are vectorised and compared with earlier crashes to tell new bugs from known ones, then filed automatically.
  - A plain-language status interface, and "an automated summary of the previous day's data … every morning at 9 AM".
  - Claimed "over 30,000 hours of engineering work per month" automated. The model names are not in the summaries.
- **"GPT-6 Astra" finishes Portal (posted 6 Sep 2026 by "CozyBlaze")** [SS]:
  - The model reportedly played through MCP plus Valve's SourcePauseTool, which pauses the game while the model thinks.
  - 3,336 tool calls, $571.18, about 24 hours of wall time for 1 h 53 min of play.
  - The summaries themselves note that Portal is heavily documented online, so the model probably met the puzzles in training.
  - I could not verify that "GPT-6 Astra" exists: openai.com was unreachable. It appears only in press summaries and in the Code4Scene abstract.
- **nunu.ai** (Swiss, ETH founders; Gemini-based agents that see rendered frames and use keyboard and mouse; paid QA service; one customer claims 50% lower QA cost) [SS]. **Razer QA Companion-AI** (GDC, March 2026; background) [SS]. **modl.ai** [SS]. All paid.
- **Benchmarks** [ABS]:
  - PlaySuite (2610.07127, 5 Oct 2026): more than 5K open-source games; 14 open models show a "perception-action gap", with "recurring failures in spatial grounding, action execution, and self-correction".
  - OmniGameArena (2606.09826, 8 Jun 2026): 12 new UE5 games and a reflection harness that refines a skill prompt over rounds.
  - GameWorld (2604.07429, Apr 2026; background): even the best agent is "far from" human level.
  - CA2 (2605.13918, May 2026): uses call-stack signals to steer test agents.
- **Background (before July):** SIMA 2 (Google DeepMind, 13 Nov 2025) [SS]. NitroGen (NVIDIA et al., 4 Jan 2026; 40,000 hours of gameplay video, gamepad-style games; weights under an "NVIDIA License" whose commercial terms I did not check) [ABS, SS].
- **LEDGER angle (the nightly AI tester):**
  - Capcom's setup is close to LEDGER's: real build, virtual input, crash dedup, morning summary. The difference is that LEDGER's core questions are social ("who noticed, who mentioned it, how long did the reply take").
  - Epic's MCP server can be hosted in a cooked development build with tools registered in C++. The tester could then (a) play through injected input and screenshots, as a player would, and (b) call read-only tools for measurement: NPC memory entries, gossip passes, timestamps of the player's line and of the first audio sample. Every number would then come from the real path. [I, based on SHOWN docs]
  - The Portal run's trick, pausing the game while the model thinks, suits walking and looking, where model latency is not part of what is measured. It must not be used while a talk exchange is being timed. [I]
  - It runs on this PC: Claude Code on the subscription drives it, with no API cost, consistent with "no API calls in development". The game and the voice share the RX 6700, so the tester's screenshots should be taken at the game's own resolution and kept to what is needed. [I]
  - Under LEDGER's "no MCP server in the build friends play" rule: build the tester tools only into Development configs, behind a compile flag. [I]

---

## 5. AI on top of the game frame: neural rendering and photoreal filters

- **NVIDIA DLSS 5** ("3D-guided neural rendering"): shown at GTC, March 2026. A pixel-space diffusion transformer takes the frame plus G-buffer (albedo, normals, depth, roughness, motion) and re-synthesises lighting and materials. Developers get masks and intensity controls. Available 3 Sep 2026 on RTX 50 only, with RTX 40 promised later. Critics report altered faces and art direction. A developer-forum thread says the UE 5.8 DLSS 5 plugin was not yet downloadable. [SS; nvidia.com UNREACHED] It does not run on the RX 6700, and LEDGER's players on AMD would never see it. [I]
- **AMD FSR Redstone:** the machine-learning features are RDNA 4 only; RX 6000 cards get the "Analytical" fallback. Reports say FSR 4 is "coming" to RDNA 2 and 3. [SS] No AMD answer to DLSS 5 was found.
- **REGEN** (Pasios and Nikolaidis; BSD-2-Clause) and **HyPER-GAN** (Pasios and Nikolaidis, arXiv 2603.10604, March 2026; MIT): lightweight GAN filters that push game frames toward Cityscapes or Mapillary photo statistics. A README update dated 09/06/2026 added ONNX export and UE5 integration through the engine's neural network (NNE) post-process path. "At a resolution of 1920x1080, an RTX 4090 can achieve above 20 FPS when integrating HyPER-GAN into Unreal Engine 5". [SHOWN, README and LICENSE read]
  - Pretrained models: GTA V frames (the "Playing for Data" set) to Cityscapes or Mapillary. Taint for a sold game [I]: GTA V frames are another game's output, and Cityscapes is, to my knowledge, licensed for non-commercial use only (not re-checked here).
  - Retraining on LEDGER's own UE frames would mean training a generative model on Unreal output. CLAUDE.md records that the Unreal licence forbids exactly that. Jafar's decision, and the default should be no. [I]
  - On an RX 6700 through DirectML, which has far less compute than a 4090 and shares VRAM with the voice model, real time at 1440p is unlikely. [I]
- **Hybrid Sim2Real** (Pasios, 2605.02291, 4 May 2026): FLUX.2-4B Klein alone was beaten by REGEN; combining the two gave better realism. [ABS] FLUX.2 Klein licence not checked.
- **SANA-Streaming** (2605.30409, 28 May 2026): real-time video-to-video editing at 1280x704 and 24 fps end to end on one RTX 5090, with kernels tuned for NVIDIA Blackwell. [ABS] Not for this PC.
- **LEDGER angle (problem 2):** none of these is a usable shortcut to the look on this PC within the licence rules. The look has to come from assets, materials, light and post-processing inside Unreal. [I]

---

## 6. What runs on this PC (Ryzen 5 5600X, RX 6700 10 GB, Windows)

| Item | Runs here? | Cost | Licence for a sold game |
|---|---|---|---|
| Epic Unreal MCP (UE 5.8) + Epic Claude Code plugin | Yes (in the editor; packaged dev builds with C++-registered tools) | None beyond subscription | Engine feature; plugin MIT. Check the training-data setting (see 1.1) |
| Epic PCG LLM skills, City Sample PCG | Yes (editor) | None | Skills are engine docs; City Sample content needs a Fab NoAI check first |
| ChiR24 Unreal_mcp, UEMCP | Yes | None | MIT |
| MCP for Blender 2.1.9 | Yes | None (generators are paid or cloud) | MIT; use Poly Haven only; turn telemetry off; avoid the generators |
| SPEAR | Probably (Windows UE plugin; not tested) | None | MIT code, CC0 assets |
| DLSS 5 | No (RTX 50 only) | n/a | n/a |
| FSR Redstone ML | No (RDNA 4 only) | n/a | n/a |
| REGEN / HyPER-GAN in UE5 via ONNX | Technically yes, but likely far from real time [I] | None | Code MIT/BSD; weights tainted (GTA V frames, Cityscapes); retraining on UE frames conflicts with the UE licence clause [I] |
| SANA-Streaming | No (Blackwell-tuned) | n/a | not checked |
| Capcom-style tester, nunu.ai, Razer, modl.ai | The method yes; the services are paid | Services cost money | n/a |

## 7. Suggested next steps (for the builder; none touches canon, money or scope)
1. Install Epic's Claude Code plugin and the UE 5.8 MCP plugin on the builder's machine. Run read-only calls first: list actors, take a screenshot from the game camera. Keep permission prompts on. Save and commit before any MCP session. [I]
2. Prototype one or two tester tools registered in C++ in a Development build: a game-state read (NPC memory, reply timestamps) and a screenshot. Keep them out of Shipping. [I]
3. For the frame fault check, compare each frame with the last approved frame from the same camera, the RefGlitch method, and treat model flags as leads, not verdicts. [I]
4. Ask Jafar (money/licence) only if someone proposes a neural filter or a paid QA service. Recommendation: no. [I]

## Sources read (URLs)
- Epic, Unreal MCP in Unreal Editor: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor
- Epic, ModelContextProtocol API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/ModelContextProtocol
- Epic, UE 5.8 release notes: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes
- Epic, Working with PCG and LLMs: https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-pcg-and-llms-using-unreal-mcp-in-unreal-engine
- Epic, City Sample PCG and MCP: https://dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-pcg-and-mcp-server-interaction-in-unreal-engine
- Epic plugin repo (README, SKILL.md, LICENSE via raw): https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin
- ChiR24/Unreal_mcp README: https://github.com/ChiR24/Unreal_mcp ; atomantic/UEMCP README: https://github.com/atomantic/UEMCP
- MCP for Blender README: https://github.com/ahujasid/blender-mcp ; PyPI: https://pypi.org/project/mcp-for-blender/
- REGEN: https://github.com/stefanos50/REGEN ; HyPER-GAN: https://github.com/stefanos50/HyPER-GAN
- SPEAR: https://github.com/spear-sim/spear
- Anthropic, Claude Opus 5.5: https://www.anthropic.com/news/claude-opus-5-5 ; news list https://www.anthropic.com/news
- arXiv (abstracts): 2609.23142, 2609.36777, 2607.03525, 2610.05033, 2607.06701, 2603.07106, 2609.06535, 2606.02580, 2605.23771, 2606.01057, 2610.03715, 2601.11109, 2606.17861, 2607.10826, 2609.40325, 2604.11082, 2603.22706, 2604.13035, 2607.20889, 2610.07127, 2606.09826, 2604.07429, 2605.13918, 2601.02427, 2603.10604, 2508.17061, 2605.02291, 2605.30409 (all at https://arxiv.org/abs/<id>)
- Search-summary leads only [SS]: Puget Systems hands-on (https://www.pugetsystems.com/blog/2026/07/09/unreal-engine-mcp-hands-on-testing-ai-inside-the-editor/, UNREACHED); State of Unreal 2026 (https://www.unrealengine.com/news/state-of-unreal-2026-top-news-from-the-show, UNREACHED); Capcom CEDEC 2026 (https://www.invenglobal.com/articles/24103/capcoms-quest-for-efficient-ai-driven-testing, UNREACHED); GPT-6 Astra Portal (https://www.techno-edge.net/article/2026/09/08/5472.html); DLSS 5 (https://nvidia.com/en-us/geforce/news/dlss-5-3d-guided-neural-rendering/, UNREACHED; https://forums.developer.nvidia.com/t/official-dlss-5-neural-rendering-plugin-access-for-unreal-engine-5-8-2/382731); FSR Redstone (https://www.guru3d.com/review/amd-fsr-redstone-quick-deepdive-review/); Unity AI (https://unity.com/blog/unity-ai-how-to-get-started); nunu.ai (https://www.venturekick.ch/nunuai-raises-USD-6M-to-advance-AIpowered-video-game-testing); StraySpark (https://www.strayspark.studio/products/blender-complete).
