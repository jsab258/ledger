> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand A: frontier AI in decompiling, modding, mashups and one-person game building (July to October 2026)

Helper A. Written 7 October 2026. Time spent about 30 minutes.
Marks: [SHOWN] = I read the evidence myself (code page, README, release page, the vendor's own page); [ABS] = arXiv abstract only, the authors' claim; [SS] = search summary only, a lead and not evidence; UNREACHED = could not open; [I] = my inference. Where a README is the evidence, it is still the author's own account: I read it, I did not run anything.

Unreached this session (blocked by the proxy): pcgamer.com, timeextension.com, kotaku.com, the-decoder.com, simonwillison.net, blog.chrislewis.au, gambiconf.substack.com, icml.cc, fortnite.com, Fab. Everything said about them below comes from search summaries and is marked [SS].

---

## 0. Models named in this strand (what I could check)

- **Claude Opus 5**: Anthropic's page "Introducing Claude Opus 5", dated 24 July 2026: "comes close to ... Claude Fable 5 at half the price"; $5/$25 per million tokens; a Fast mode. [SHOWN, anthropic.com/news/claude-opus-5]
- **Claude Opus 5.5**: Anthropic's page dated 22 September 2026: "performs at the level of Claude Fable 5.1 on most work and costs 40% less to run than Opus 5"; $4/$20 per million tokens. On games, only one line: "A different tester had several Claude models build a game from a single prompt; Opus 5.5 scored higher than any other model on the strength of its graphics and polish." No details or link. [SHOWN that Anthropic says it; the game test itself is CLAIMED.] https://www.anthropic.com/claude-opus-5-5
- **Cyber safeguards (matters for reverse engineering)**: Anthropic, 6 October 2026: "our generally available models, such as Claude Opus 5.5, Claude Fable 5.1, and Claude Sonnet 5.5, have conservative cyber safeguards that block most cyber work"; reverse-engineering malware is named under the verified "Defense Access" tier. [SHOWN] https://www.anthropic.com/news/cyber-verification-program . Whether decompiling a game binary trips those blocks I could not establish [I: it might, since binary analysis looks like cyber work]. That said, the mod notes in section 3 report Opus 5.5 decompiling .NET games and hooking native ones (late September to October), so ordinary game work evidently gets through at least sometimes.
- **OpenAI**: search summaries name GPT-5.6 "Terra", "Luna" and "Sol" in Codex, and say GPT-5.4 left Codex on 31 August 2026 [SS]. An arXiv abstract (Echo, 16 Sept 2026) uses "GPT-5.6" and "Codex" as baselines [ABS]. The Universal Modder README uses "Codex (gpt-6)" as an example string [SHOWN as a string only]. **I could not verify "GPT-6 Astra" or "GPT-6.1 Sol"**. One Italian headline mentions "ChatGPT Astra" [SS]. openai.com is unreached.
- **Gemini**: nothing in this strand verified. Epic's Unreal MCP docs list Gemini CLI as a supported client [SHOWN], and Universal Modder installs into Gemini CLI [SHOWN]. "Gemini 3.6 Flash for Unreal" appears only on a vendor page [SS, unverified].
- **Open models actually used**: Qwen3.8 27B (Fable 2 port, author's statement) [SHOWN README]; DeepSeek V4.1 Flash, MiMo v2.6 Flash and others named in mod notes' front matter [SHOWN as self-labels]; Gemma4:31b in a decompilation paper [ABS].

---

## 1. Decompiling, reverse engineering and recompiling games

### 1.1 Wave Race 64: Recompiled (N64 to native PC), written by Claude in Claude Code
- **Who/when**: Daniel Gomes Vieira (upstream); fork by Brian Tate (elliotttate) using Codex. Upstream releases v0.7.1 on 10 Sept to v1.0.2 on 14 Sept (the release page shows no year; [I] 2026, consistent with press of the period).
- **What was shown**: [SHOWN] Public repo with Windows, macOS and Linux releases. README: "The original upstream project was written by Claude, Anthropic's AI model, working in Claude Code under the direction of Daniel Gomes Vieira, who set the goals, made the decisions, played the builds and reported what he saw." Built on N64Recomp, N64ModernRuntime (GPL-3.0) and the RT64 renderer; leans on an existing human decompilation for function names. The fork adds a "modern water" shader, bundled AI-made HD textures (folder named "nano-banana-2", Google's image model), and validation "through native playtesting and deterministic replays".
- **Method worth noting** [SHOWN, docs/PLAN.md]: seven phase-gated stages, each with a measurable gate (for example, "an assembled ELF whose code section matches the original ROM byte-for-byte"). Standing rules: generated code is never hand-edited, and fixes go into tooling. "Instrument with a function-entry trace; a debugger on 19 MB of generated C is not a plan." Interpolation faults were counted per frame by instrumenting the renderer, not guessed at.
- **URLs**: https://github.com/danielgomesvieira2000/wave-race-64-recomp ; https://github.com/elliotttate/wave-race-64-recomp
- **Legal flag**: needs the user's own ROM dump; the built executable is a GPL-3.0 combined work; the menu library has no licence (README says so).

### 1.2 Fable 2 (Xbox 360 to PC) with a local open model
- **Who/when**: himdo, around September 2026 (a Russian news item dated 22 Sept 2026 [SS]). Uses the ReXGlue static-recompilation SDK v0.10.0.
- **Shown vs claimed**: README [SHOWN]: "this project was made to test the capabilities of local and open source AI. This project was made using Qwen3.8 27b. After about an hour it got the game running. Then after a large amount of human trial and error..." So the model got it booting, and a person did most of the rest. That is the author's own account.
- **Useful pattern** [SHOWN]: a **debug-only AI remote-control channel**. It is a localhost TCP server speaking JSON, one line per request. It can press buttons, move sticks and run atomic timed scripts, and it has a `game_state` classifier that reports which screen the game is on. A `screenshot` command reads "the current game frame ... in-process from the renderer's output texture ... not from the desktop", so covered or unfocused windows never spoil it. It is compiled out of release builds ("must not ship to players").
- **URL**: https://github.com/himdo/Fable-2-Recomp

### 1.3 Snowboard Kids 2: matching decompilation with Claude Code (background, then recompiled)
- Chris Lewis. "100% decompiled" announced 30 May 2026 [SS] (before the window); the recompiled PC port was released later [SS, date not established]. Search summaries say that after three months of manual work at 25%, Claude Code in non-interactive mode, taking the easiest functions first, reached 45% in about three weeks. A follow-up post, "The Long Tail of LLM-Assisted Decompilation", reports progress stalling around 75%, then the use of a logistic-regression ranking of functions by difficulty and text-embedding similarity search over already-decompiled functions [SS]. The blog is UNREACHED. The repo README links these posts and credits decomp.me, decomp.dev, splat and decomp-permuter [SHOWN]. https://github.com/cdlewis/snowboardkids2-decomp
- Claude, GLM and Codex all helped [SS].

### 1.4 Other ports in the window (press only)
- **Mario Kart Wiicompiled** (Patchzzy): announced 15 July 2026 as the first static recompilation of a Wii game, with AI-assisted coding and a public beta planned for August [SS; release state unverified; press UNREACHED].
- **DK64 Rekongpiled**: released 29 August 2026 and **explicitly made without generative AI**, after its makers objected to an AI-made rival port [SS].
- The press frames this as a split in the scene ("PC ports of old console games are the new AI vibe coding battleground", PC Gamer, UNREACHED) [SS].

### 1.5 Ghidra/IDA through MCP (tooling background)
- Several open MCP servers expose Ghidra or IDA to agents: LaurieWired/GhidraMCP, a headless Ghidra MCP with "212 tools", and mrexodia/ida-pro-mcp [SS; I did not open them]. A demonstration from January 2026 (Quesma) gave River Raid unlimited lives through Claude + Ghidra + MCP [SS, before the window].

### 1.6 Research papers, July to October 2026 [ABS unless stated]
- **Echo** (16 Sept, 2609.18706): matching decompilation through "trusted back-translation", with compilation used as feedback; claims 2.43x more exact matches than the strongest baseline, and 2.75x/7.4x as many functions as GPT-5.6/Codex on the Mirai binary.
- **When LLM Decompilers Recompile More and Preserve Less** (4 Sept, 2609.05370): LLM refinement lifts Ghidra's build rate from 75% to 90% while its behaviour-matched rate falls from 74% to 62%. Code that passes every shipped test still diverges on fuzzed inputs (4.9% overall, up to 13%). **Lesson: compiling and passing tests is not equivalence. Differential fuzzing against the reference catches what tests miss.**
- **CHISEL** (28 Aug, 2608.27981): compiler plus coverage-guided fuzzer feedback, test-suite-free, using the open Gemma4:31b; 96.1% recompile and 79.8% re-execute in about 2.1 iterations.
- **Recompilation Is Not Enough** (7 Sept, 2609.07201): adding test-gate feedback gets 87.5% of 104 Coreutils binaries to recompile and pass.
- **When Binaries Talk Back** (14 July, 2607.12507): text planted inside a binary steers LLM reverse-engineering agents. Models proposed the planted unsafe action in 35/40 adversarial cases, and 15 still did so when the content was shown "as data only". **Lesson: anything an agent reads from a file it did not make is untrusted.**
- **A Memorization Floor** (15 Sept, 2609.17236): LLM renaming of decompiled code draws on the model's prior, not the input's dataflow.
- An ICML 2026 talk, "Matching Decompilation as a Verifier-Guided Task for Human-Centered Coding Agents", is UNREACHED (icml.cc) [SS].

---

## 2. Modding with AI help

### 2.1 Universal Modder (the tool behind much of the late-September wave)
- **Who/when**: Rehan ("rehan-remade"), released on GitHub 30 September 2026 [SS for the date]. MIT licence [SHOWN].
- **What it is** [SHOWN README]: a Claude Code plugin (also for Codex, Gemini CLI, Copilot, Cursor and OpenCode). It has skills for recon, reverse engineering (ILSpy, Cpp2IL, Ghidra and IDA over MCP, Frida, RenderDoc), asset generation through the paid fal API (or local ComfyUI), in-game testing, showcase video and **mashup-mods**, plus a `um` command-line tool. The fixed loop: search the knowledge base, recon, safe lab, read the actual code, "build one working slice", assets, "verify in the real game", record, package, then write a field note "for the next agent". Rules: it refuses online games with anti-cheat, and "never ships game files or decompiled code".
- **Knowledge base** [SHOWN index]: 57 game notes and 17 technique notes, dated 28 Sept to 7 Oct 2026. Most are labelled "Claude Code (Opus 5.5)"; some say Sonnet 5.5, Opus 5, DeepSeek V4.1 Flash or OpenCode. Labels are self-reported. Examples:
  - Minecraft inside GTA V story mode (passthrough; a Fabric mod and a ScriptHookV add-on exchange camera and events over a local WebSocket, and Minecraft's colour and depth are composited into GTA's frame), 30 Sept, Opus 5.5.
  - "Portalcraft" (Minecraft inside Portal 2), 5 Oct.
  - A "CS2 conversion of Elden Ring offline" as a native Rust DLL.
  - A Victoria 2 total conversion into an LA gang-territory game, 3 Oct, Opus 5.5.
  - An RL agent for Terraria's Eye of Cthulhu, 28 Sept, Opus 5.5. The game was decompiled with ilspycmd, the boss AI ported into a vectorised simulator, and real traces replayed against the sim until they matched (99.9% per variable, per the oracles note). A PPO policy trained in the sim was exported back into the game.
  - Halo 3 weapons and vehicles ported into Minecraft "from your own MCC install".
- **The "Oracles" technique note** (1 Oct 2026, Opus 5.5) [SHOWN, directly useful]: "Agents fail at modding by drifting: confidently building on a wrong guess about the engine. The cure is an oracle, something mechanical that says right or wrong, run after every change." The table covers round trip, trace replay, a scripted scene plus a "screenshot you actually look at", the game log, a synthetic host, a measurement scene for latency and sync, a byte-matching build, a headless bench and a scripted real run. Its rules:
  - automate the whole loop, from launch to check;
  - "a circuit breaker: after about 3 identical failures, stop, write down what you know, and change approach";
  - keep a journal that "survives context compaction";
  - "write down what the oracle did not cover".
  Gotcha 4 (2026-10-01): **the screenshot oracle froze**. Windows.Graphics.Capture returned byte-identical frames (same SHA-256) minutes apart while the game was rendering, so the agent kept judging a stale frame. Fix: "prove the oracle is live before trusting it". Take two captures a second apart and compare hashes, check the process is burning CPU, or capture from inside the renderer.
  https://github.com/rehan-remade/universal-modder (knowledge/techniques/oracles-how-agents-know-a-mod-works.md)

### 2.2 Other modding items
- **Nexus Mods** tightened its generative-AI tagging around 1 August 2026: separate tags for AI-generated content, AI media and AI-assisted, with moderation for undisclosed use [SS; nexusmods.com not opened].
- **Mantella** (Skyrim/Fallout 4 LLM NPC conversations; background, v0.14 April 2026 [SS]). Its public config [SHOWN] shows its latency tactics: sentences go to text-to-speech one at a time, once a sentence has a minimum word count (default 3); replies are capped at 4 sentences for a single NPC; lip-sync generation can be switched off "to improve response times"; and there is a "Speed" provider-routing option. **None of this is new to LEDGER** [I]: it streams sentence by sentence and has no fact check before speech, so it does not face LEDGER's check-sets-the-floor problem.
- A Take-Two copyright strike removed an AI-powered GTA V mod from Nexus [SS, date unclear].

---

## 3. Game mashups

- **What happened**: from about 28 September 2026, viral clips of AI-made mashups appeared: Skate in Modern Warfare 2, Minecraft inside Elden Ring, Spider-Man's web-swinging in Arkham Knight's Gotham. Many were "not downloadable yet and solely exist as Twitter clips" [SS: ground.news, tech4gamers, a Kotaku headline "Modders, Please Stop Putting Games Inside Other Games With AI", UNREACHED]. Universal Modder's README says its playbooks "draw on the September 2026 wave of AI-built mods" [SHOWN].
- **How they work** [SHOWN, Universal Modder]. There are three routes:
  - "passthrough": two games run at once and exchange state over a local socket, with one composited into the other's frame.
  - "content ports": assets converted from the user's own install.
  - "reimplementation": the guest game's rules rebuilt as a headless simulation, with the host as the view.
- **Shown vs claimed**: the knowledge-base notes give versions, routes and gotchas [SHOWN as write-ups]. I ran nothing. Press claims of "decompiled with Claude" are [SS].
- **Legal flag** (for the legal helper): these mods move another game's code, behaviour and assets into a different game. Even "from your own install" they rest on the original publisher's IP. Some ship converters rather than assets, which reduces but does not remove the risk. **Not a route for LEDGER in any form**: it would be copying another game's code or assets.

---

## 4. Games and tools built fast by one person with agents

- **Agentic game-dev benchmarks**, a cluster between July and October 2026 [ABS]. These are the most useful evidence here for LEDGER's way of working:
  - **CraftBench-UE** (19 Sept, 2609.23142): 70 Unreal Engine tasks (C++, Blueprint, editor scripting), deterministic build, asset and runtime checks, no LLM judge. "C++ completion rates exceed Blueprint by 30.0 and 42.9 percentage points"; of the Blueprint submissions that pass asset checks, 42.2% and 50.0% "fail explicit runtime assertions".
  - **GameEngineBench** (3 July, 2607.03525): 110 scoped C++ tasks in real UE5 projects; the best configuration reaches 55.5% pass@1, and 31 tasks are solved by none.
  - **SWE-Game** (27 Sept, 2609.33678): Godot. "Opus5 achieves the highest overall score in all five task types". **Executable state checks reach 92.59% balanced accuracy against human labels, against 78.41% for a video-based VLM judge**, while rubric-based visual scores correlate 0.829 with human ratings of presentation.
  - **GameLogicBench** (18 Sept, 2609.21562): checks rules at every simulation tick. "Without this validation [against mutants], incorrect agent submissions passed." It also found "agents copying code from public repositories when network access is open."
  - **OpenGameEval** (1 Oct, Roblox, MIT): a run that inspects the objects a solution touches before editing passes 9.8 to 13.4 percentage points more often.
  - **GameXpert-Bench** (22 Aug): agents are better at "playable foundations and explicit requirements than at discovering defects, verifying runtime behavior, and preserving functionality across changes".
  - **Recursive Game Creator** (6 Oct): a Designer, Builder, Player and Reviewer loop, where a "coding-native Player" drives the game through programmatic interfaces rather than the GUI; "code is coming soon" (not released).
- **Claude Code Game Studios** (Donchitos, MIT): a template with 49 agents, 74 skills and 12 hooks [SHOWN README; date not established]. Its own measurement, as reported in the README (CLAIMED; no data published): four games were built from one brief at different rigour levels; the "standard" level wrote 30 documents before the first line of code (58 minutes) and "two blind reviewers and a human playtest then ranked the standard build last — the extra 29 documents bought traceability, not a better game". It also rules that a visible change is not closed until the game is launched, observed and a screenshot retained. https://github.com/Donchitos/Claude-Code-Game-Studios
- **unreal-engine-skills** (quodsoler, MIT) [SHOWN]: 31 agent skills for UE C++. It claims "Every API in every skill was checked against the UE 5.8 headers", with tables correcting APIs that agents hallucinate (for example `FStateTreeActorContext`, `UAISense_Sight::ReportSightEvent`; "MassEntity is a runtime module in 5.8, not a plugin"). It includes Mass Entity, State Tree, animation and character-movement skills. https://github.com/quodsoler/unreal-engine-skills
- **Epic's Unreal MCP** [SHOWN docs, dev.epicgames.com]: an MCP server built into the UE 5.8 editor, **Experimental**. Supported clients: "ClaudeCode, Cursor, VSCode, Gemini, and Codex". It runs over HTTP/SSE at 127.0.0.1:8000/mcp, loopback only, with "no authentication layer". Toolsets include scenes, actors, lighting, material instances, Slate widget inspection and **running automation tests**. Registry auto-discovery works in the editor only. Extended to UEFN on 20 August 2026 [SS]. https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
- **RenderDoc MCP servers** [SHOWN README]: JiaboLi-GitHub/renderdoc-mcp (MIT, 59 tools: open .rdc captures, inspect passes, debug pixels, diff two captures) and Linkingooo/renderdoc-mcp (D3D12 supported; the author calls it a "vibe-coding project ... not for production").
- Also from search only [SS]: Unreal Insights trace tools for agents (a Fab plugin "MCP Python Bridge"; **Fab UNREACHED, NoAI status unknown**), CLI-Anything's unrealinsights harness, and indie claims of games built with parallel Claude Code agents (Void Balls, Catvivors, CODEX MORTIS; all before July 2026). "Claude Opus 5" browser 3D-game demos by Matt Shumer and others were reported by The Decoder, which is UNREACHED.

---

## 5. The LEDGER angle

Nothing here needs another game's code or assets. The useful part is **method**: how these projects make an agent's work checkable. Ordered by expected value for LEDGER:

1. **Matching-decompilation discipline for the C++ port (problem 5; simulation).** LEDGER's rule that the C++ port must match the C# golden table is the same shape as a byte-matching decomp oracle.
   - Transferable: run Claude Code non-interactively over a queue ranked easiest-first, with the oracle in the loop (Snowboard Kids 2) [SS on details].
   - Never hand-edit generated output; fix the tooling (Wave Race PLAN) [SHOWN].
   - Golden rows alone are not enough. "Recompile more and preserve less" shows that code which passes all fixed tests still diverges on fuzzed inputs [ABS]. **Add differential fuzzing: random seeded worlds run through both C# Core and the C++ port, compared tick by tick** [I]. The same applies to GameLogicBench's mutant check: a test suite that does not reject a deliberately broken version is not a test. That speaks directly to Jafar's 30 September ruling on golden rows [I].
   - Runs on this PC: yes, CPU only. Cost: subscription usage only. Licence: own code.
2. **A proper channel for the AI tester (problems 1 and 5).** Patterns: Fable 2's debug-only localhost JSON control (atomic scripted input, a state classifier, frames captured from the render target, not the desktop) [SHOWN]; Recursive Game Creator's code-driven player [ABS]; SWE-Game's finding that state probes beat a video judge (92.6% against 78.4%) [ABS].
   - For LEDGER's nightly "does the town know Tom" walk, the numbers (who noticed, who mentioned it, "that's all I know" count, reply latency) should come from **engine-state and log probes**, with pictures used only for presentation [I].
   - Caveat: LEDGER's tester walks the packaged release build. A control channel must be compiled into that build in a form that cannot reach players, for example only in Unreal's Test configuration, or behind a command-line flag in a build that is never distributed. Which build the tester walks is a decision for the builder [I].
   - Runs on this PC: yes. Cost: none.
3. **Prove the screenshot oracle is live (problem 2 and the gate).** LEDGER's gate and pages live on captured frames. Universal Modder's frozen-capture gotcha (byte-identical frames while the game ran) is cheap to guard against: hash two captures a second apart; capture inside the engine, not from the desktop [SHOWN; I for the LEDGER fit]. It also connects to Jafar's 2 October ruling: "nothing comes to him for a look that has not visibly changed". A stale capture could make a changed frame look unchanged, or the other way round.
4. **Epic's Unreal MCP in UE 5.8 (problem 5).** Lets the builder drive the editor (actors, lights, material instances, automation tests) instead of only editing files and Python. Experimental, loopback only, no authentication. CraftBench-UE's result supports keeping agent work in **C++ and editor scripting rather than Blueprint** (30 to 43 points better; about half of "passing" Blueprints fail runtime assertions) [ABS].
   - Runs on this PC: yes (Windows, local). Cost: none; it ships with UE 5.8.
   - **Flag for the legal helper**: the UE licence clause against using the engine or MetaHumans as training input to generative AI. Driving the editor through Claude Code sends editor data to Anthropic. Worth confirming that Jafar's Claude account has model-training on his chats and code switched off [I].
5. **RenderDoc MCP on LEDGER's own frames (problem 2, diagnostic only).**
   - Good uses: let an agent count passes and lights, find the source of black squares or debug objects, and diff the night frame before and after a change.
   - It will not make the street beautiful. It helps find faults before a page.
   - Runs on this PC: RenderDoc supports D3D12 on AMD [I]. Cost: free, MIT.
   - **Do not point it at other games' frames** (KCD2 or any other): many EULAs bar reverse engineering, and anti-tamper often blocks capture (legal flag). Studying how KCD2 or others light a street should come from **published talks and graphics studies**, not from captures [I].
6. **unreal-engine-skills (problem 5, and problem 4 for animation).** A cheap way to stop agents emitting stale or non-existent UE 5.8 APIs, including Mass (crowds), State Tree and animation [SHOWN]. MIT. Read it before adopting; its "checked against 5.8 headers" claim is the author's.
7. **Working-method evidence (problem 5).**
   - The oracles note's "about 3 identical failures, stop and change approach" matches LEDGER's two-tries rule.
   - "Write down what the oracle did not cover" matches LEDGER's rule that every number says whether it came from the real path.
   - Claude Code Game Studios' own (unverified) measurement says more upfront documents did not make a better game. Worth weighing against LEDGER's record-keeping load [CLAIMED].
   - OpenGameEval: inspect before editing (+10 to 13 points) [ABS].

**Not useful, or not allowed, for LEDGER**:
- Mashups, content ports and any decompiling of another game, for reference or reuse. That is copying, with legal exposure, and Opus 5.5's general cyber safeguards may block binary work anyway [SHOWN that the safeguards exist; I for whether they apply].
- Universal Modder's asset route, which calls the paid fal API (costs money; LEDGER has a no-API rule).
- Mantella's latency tricks, which LEDGER already has.

**Security note**: if an agent ever reads files LEDGER did not make (downloaded assets, third-party plugins, captures), treat their text as data, never as instructions (When Binaries Talk Back [ABS]).

---

## Sources (opened unless marked)
- https://www.anthropic.com/news/claude-opus-5 ; https://www.anthropic.com/claude-opus-5-5 ; https://www.anthropic.com/news/cyber-verification-program
- https://github.com/danielgomesvieira2000/wave-race-64-recomp (README, releases) ; https://github.com/elliotttate/wave-race-64-recomp (README, docs/PLAN.md)
- https://github.com/himdo/Fable-2-Recomp (README)
- https://github.com/cdlewis/snowboardkids2-decomp (README); blog.chrislewis.au UNREACHED
- https://github.com/rehan-remade/universal-modder (README, knowledge/INDEX.md, techniques/oracles..., games/terraria/eye-of-cthulhu-rl-agent.md, games/minecraft/kindred...)
- https://github.com/art-from-the-machine/Mantella (README, src/config/definitions)
- https://github.com/Donchitos/Claude-Code-Game-Studios (README) ; https://github.com/quodsoler/unreal-engine-skills (README, LICENSE)
- https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
- https://github.com/JiaboLi-GitHub/renderdoc-mcp ; https://github.com/Linkingooo/renderdoc-mcp
- arXiv abstracts: 2609.18706, 2609.05370, 2608.27981, 2609.07201, 2607.12507, 2609.17236, 2610.06900, 2609.23142, 2607.03525, 2609.33678, 2609.21562, 2610.02563, 2608.21833, 2610.08621
- Search summaries only: pcgamer.com (AI recomp battleground), timeextension.com (Mario Kart Wii, DK64), tomshardware/notebookcheck (Mario Kart Wii), dotesports, kotaku/ground.news/tech4gamers (mashups), vidaextra (Universal Modder date), shacknews/pcgamer (Nexus policy), fortnite.com (UEFN MCP), the-decoder (Opus 5 game demos), thurrott/digg (Opus 5.5).
