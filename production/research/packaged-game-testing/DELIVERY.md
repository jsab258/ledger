# Testing the packaged game with real inputs: the detail

Research, 30 September 2026, by a separate research helper. Question: how professionals test a packaged Unreal game automatically with real inputs, from start to finish, and how a one-person project sets that up to walk a release build. (The helper returned its text; the session that asked for it saved it here. That session checked [P2] to [P5] against the files and commit 72802eca, and added one option to the talk decision in Step 3; nothing else was changed.)

How this was done: Epic's 5.8 documentation pages and GitHub repositories were opened and read. Most other sites were blocked by this machine's network filter: GDC Vault, gamedeveloper.com, Epic's forums and issue tracker, unrealengine.com, YouTube, arXiv, EA, Riot's tech blog, Microsoft Learn, GitHub Docs, the vendors' sites and several small-studio blogs. Epic's community pages (knowledge base, snippets, talks) load their text by script behind a bot check and returned no body. Those sources are cited from search summaries and labelled SNIPPET. The engine source cannot be read from here. Where it matters, this note leans on production/research/ai-tester/WHAT-UNREAL-PROVIDES.md (23 September), which read the installed 5.8 source on the PC; it is cited as [P1]. Source numbers [S#] are listed at the end. Throughout, "established practice" means what the sources show studios do, and "recommendation" means my judgement for LEDGER.

## (a) The professional pipeline, stage by stage

### 1. Build configurations

| | Development | Test | Shipping |
|---|---|---|---|
| Optimisation | "all but the most time-consuming" [S5] | "the Shipping configuration, but with some console commands, stats, and profiling tools enabled" [S5] | full; "strips out console commands, stats, and profiling tools" [S5][S6] |
| Console, `-ExecCmds` | yes [P1] | some [S5][S6] | no. `bUseConsoleInShipping` exists [S7]; forum snippets say re-enabling it needs a source-built engine [S42] |
| Log file | yes | off by default: `bUseLoggingInShipping` is "for test/shipping builds" [S7] | off by default [S7]. On an installed (launcher) engine, forum and knowledge-base snippets say `bUseLoggingInShipping = true` plus `bOverrideBuildEnvironment = true` in the target file works [S41]; unverified |
| Checks | yes | off by default (`bUseChecksInShipping`, "test/shipping") [S7] | off by default [S7] |
| Automation test runner, functional tests | yes: every non-Shipping game build includes AutomationWorker and FunctionalTesting [P1] | runner present per [P1]. My understanding is that development automation tests are compiled out of Test unless `bForceCompileDevelopmentAutomationTests` is set [S7]; unverified | no [P1] |
| Gameplay Debugger, `Slate.ForceRawInputSimulation`, Gauntlet's RPC receiver | yes [P1] | not checked | no [P1] |
| Available on a launcher engine | yes | **no: needs a source-built engine** [S24 OPENED; S40 SNIPPET]; not tried on this PC | yes |

Established practice: Epic's own Gauntlet examples package and run Development [S2]. The community Gauntlet projects [S21][S22][S23] and a forum report that Gauntlet runs "get stuck" in Test while Development works [S43] point the same way. For performance, Intel's Unreal guide recommends a slightly modified Test build [S44], because Development carries debugging overhead. Shipping is what players get, so release candidates are checked on it, but it offers the fewest hooks.

### 2. Packaging

`RunUAT BuildCookRun -project=… -platform=Win64 -configuration=Development -build -cook -pak -stage` [S2]. LEDGER already does this in its Unreal workflow with `-clientconfig=Development … -archive` [P4]. Shipping is the same command with `-clientconfig=Shipping` into a separate archive folder. Gauntlet does not build; it needs an existing packaged or staged build [S1].

### 3. Launching and supervising: Gauntlet

- **RunUnreal** (a UAT command) builds a list of tests and runs them against a build [S1][S2]: `RunUAT RunUnreal -project=… -platform=Win64 -configuration=Development -build=<local|path> -test=<name>` [S2].
- **Built-in tests**: `UE.BootTest`, `UE.EditorBootTest`, `UE.EditorAutomation`, `UE.TargetAutomation` (runs the Automation Test Framework on a client), `UE.Networking`, `UE.ErrorTest` and `UE.PLMTest` [S2]. Custom tests derive from `UnrealTestNode<UnrealTestConfiguration>` [S2]. `-ResumeOnCriticalFailure` resumes after crashes, up to three times [S2].
- On this PC, `UnrealGame.DefaultTest` starts one client, waits for it to exit or time out, then sorts the result into fatal error, failed start, ensures, killed at the time limit, a normal requested exit, or unhandled. It needs no C# [P1], and LEDGER's tools/ai-tester/launch.ps1 already uses it [P3].
- **In-game half (optional, beta plugin)**: a `UGauntletTestController` chosen with `-gauntlet=Name`, with `OnInit`, `OnTick`, `OnStateChange` and `EndTest(ExitCode)` [S4]. Heartbeats let Gauntlet stop a run that stops making progress [P1]. The docs call it "well suited to smoke tests that require several steps to execute" [S3]. Gauntlet itself "does not require any specific game-side automation code" [S3].
- **At studio scale**, Horde (Epic's build farm, source-distributed with the engine, needs a server and agents) and BuildGraph run the pipeline and gather results into an "Automation Hub" with screenshots, logs and call stacks [S14][S15]. Riot's 2024 Unreal Fest talk covers UAT, UBT and BuildGraph [S33, SNIPPET]. All of this is too heavy for one PC; GitHub Actions on the self-hosted runner does the same job here.

### 4. Driving the game (established practice)

- **Tests that call game code directly.** Rare built Sea of Thieves with automated gameplay tests from the start: unit, integration and "actor" tests run on each check-in [S28][S29, SNIPPET]. Their framework was merged into the engine as CQTest [S34, SNIPPET]. These tests do not pass through real input.
- **Bots that press the player's controls in software.** Ubisoft Reflections' "Client Bots" for The Division are "a custom built AI layer that directly controls the player's inputs … every system in the game still believes that a human player is playing". They play missions through automatically, wander the streets for performance data and help reproduce bugs [S30, SNIPPET].
- **Test controllers.** Community examples script a match and check its outcome [S22], or drive a camera route while recording performance CSVs [S23]. Daedalic's plug-in adds Blueprint nodes that "simulate player input, both actions and axes" [S21]; Daedalic also used it for performance tests on Gollum.
- **UI automation through the platform layer.** The Automation Driver "simulates input at the platform layer" and blocks real input while it runs [S10][P1]. Riot drives the League client's web front end with Selenium and ChromeDriver [S32, SNIPPET].
- **Large regression suites per build.** Riot's Build Verification System runs about 5,500 tests in about 18 minutes for every build (about 100,000 a day) and finds about half of all critical or blocker bugs [S31, SNIPPET].
- **Machine-learning and AI agents.** EA SEED deployed reinforcement-learning test agents in Battlefield V and Dead Space and wrote up the practical difficulties [S35][S51, SNIPPET]. Start-ups (nunu.ai, modl.ai) sell agents that play from the rendered frames [S49, SNIPPET].
- **What agents that watch the screen can currently do.** On VideoGameBench, the best models of May 2025 completed about 0.48% of the games. A "Lite" variant pauses the game while the model thinks [S36, SNIPPET]. OmniGameArena, a 2026 benchmark of twelve UE5 games, runs the games with a remote input port. It offers two clocks: one "pauses the game during inference", the other "charges model inference time to the game clock" [S27 OPENED, S37].

### 5. What is checked (established practice)

Smoke or boot test on each build; a scripted main-route ("golden path") play-through [S30][S31]; soak runs for crashes and memory; performance captures on fixed routes [S23][S39]; screenshot comparison against approved "ground truth" images with tolerances, kept separately per platform and graphics interface [S16]; and scanning logs, ensures and crashes after every run [P1].

### 6. Results and reports

- Gauntlet writes an artifact folder with logs, crash dumps and the exit reason [P1].
- Automation tests take `-ReportExportPath` to write JSON and HTML [S8].
- Daedalic's plug-in writes JUnit XML for CI dashboards [S21].
- Horde's Automation Hub gathers results and history [S15].
- The CSV profiler's output is turned into HTML charts by PerfReportTool [S23].

### 7. Schedule

Established practice: a smoke test on every build, longer suites nightly, and full passes on release candidates [S31][S15]. Epic runs this through Horde and BuildGraph [S14]; other studios use Jenkins, TeamCity or similar.

## (b) Options for driving inputs

"Real input" here means it passes through the same path as a player's hand: Windows messages, then Unreal's platform layer, then Slate and UI focus, then Enhanced Input's mappings, triggers and modifiers, then the game.

| Option | How it works | Build configurations | Real input? | Cost | Licence |
|---|---|---|---|---|---|
| **OS-level key presses (SendInput)**, as LEDGER's AI tester sends them | Scan-code key presses, relative mouse moves and typing one character at a time, sent to the focused game window [P2]. The project found that Unicode "packet" typing never reached the talk box, so it types real keys [P2] | All, including Shipping | **Yes, the whole path.** It is the only option here that catches focus bugs, text-box bugs and key-mapping bugs such as "typing a line also walks Tom" [P2] | Free | Windows API |
| Enhanced Input `Input.+key` / `Input.-key` | A console command that "force[s] simulated input onto your player" for a named key [S11] | Needs the console, so Development (and presumably Test); not Shipping | Partly. It starts from a key, but skips Windows and UI focus. Its exact path is not verified | Free | Engine EULA |
| Enhanced Input injection (`InjectInputForAction`, `StartContinuousInputInjectionForAction`, `…ForPlayerMapping`) | Game or test code injects a value for an action; it "runs modifiers and triggers delegates as if the input had come through the underlying input system as FKeys" [S12][S13] | Any build the calling code is compiled into; no editor-only restriction is documented [S13] | **No.** It skips keys, mappings, Windows and UI focus | Free | Engine EULA |
| Gauntlet in-game test controller | Plug-in code inside the game that drives and checks the game's state [S3][S4] | Development. Shipping support not verified | No, not by itself | Free (beta) | Engine EULA |
| Gauntlet's C# key-press messages | Unfinished; the receiver is compiled out of Shipping [P1] | Not usable | n/a | n/a | n/a |
| Automation Driver | Replaces the platform input handler inside the game; C++ tests find widgets by tag or path [S10][P1] | Not Shipping [P1] | Partly: enters at Unreal's platform layer, and blocks real input while active | Free | Engine EULA |
| Record and replay (e.g. AutoReplay) | Records input at the Slate viewport and replays it from JSON. "Unreal Engine is a non-deterministic engine", so replays drift [S25] | Wherever the plug-in is compiled in | Partly (from the viewport onwards) | Free | Licence not checked |
| Bots controlling the player's input (Division-style) | A custom AI layer presses the player's virtual controls [S30] | Any build it is compiled into | Partly (from the virtual controller onwards) | Weeks of work | Own code |
| AI agent looking at the screen (LEDGER's AI tester) | A Claude Code session reads screenshots and sends OS-level input [P2] | All | Yes | Subscription only; no API calls | n/a |
| GameDriver | A plug-in inside the game plus an outside API to find objects and drive them [S47, SNIPPET] | Instrumented builds | Mostly in-process | Free for solo developers and educators; 14-day trial for businesses; "Starter" from $150 a month (press release, 17 March 2025) [S47, SNIPPET] | Proprietary; would need a decision record |
| AltTester Unreal SDK | Instrumented build; exposes the object tree to outside tests. Vendor advises never shipping an instrumented build [S48, SNIPPET] | Instrumented builds | Mostly in-process | "Lite" free on request under €500k annual revenue; Pro €540 per seat per year; a pricing update took effect 1 July 2026, so these figures may be out of date [S48, SNIPPET] | Non-GPL Unreal SDK, commercial [S48, SNIPPET] |
| nunu.ai, modl.ai | Hosted AI agents that play from the screen [S49, SNIPPET] | Any | Yes | Price on request | Commercial service |

My conclusion (recommendation): for the audit's "actual inputs", the scripted route and the AI tester should both use OS-level key presses, which the project already has. Enhanced Input injection is a cheaper, headless second layer; it does not replace them.

## (c) What to check and how to report

- **Exit.** Gauntlet's classification: a normal requested exit passes; a timeout, crash, fatal error, failed start or ensure fails [P1].
- **Crash files.** A packaged game writes a crash folder (log, minidump, XML context) under its own Saved\Crashes in the user's application-data folder [S46, SNIPPET]. Epic's page covers only the optional crash-report client [S17]. Whether Shipping writes the folder without that client is **unverified**; one deliberate test crash settles it.
- **Log scan (Development).** Fail on `Fatal error`, `Ensure condition failed`, `Assertion failed`, new `Error:` lines, `LogScript: Warning: … Accessed None`, and anything not on a short list of known warnings. Compare against the last passing run, so that only new lines fail.
- **The game's own check lines as assertions (recommendation).** One line per route stage, for example `LEDGER-ROUTE stage=talk-typed ok moved_cm=0`, is written by the game's own code for watching only, never for driving. The route script waits for each line with a time limit. Shipping keeps no log by default, so these lines should also go to a small file the game writes itself, or logging should be switched back on (S41; unverified).
- **Independent behavioural expectations.** Written in plain words from canon, rulings and the NOW list, each checked by a stage line and a picture. For example: typing w, a, s, d in the talk box moves Tom 0 cm; a reply is spoken within N seconds (stand-in talk); after Z the shops are shut at their canon hours; a reload puts Tom where and when he saved. These are not golden comparisons.
- **Pictures.** One per stage, kept with the run. They are judged against the last passing run by eye or by an unbriefed reviewer, not by pixel comparison, because the light, the people and the clock move. Epic's screenshot comparison suits fixed cameras [S16].
- **Performance.** On Development, the engine's CSV profiler and PerfReportTool work, but the numbers run slower than a release build. On any build, including Shipping, the PresentMon console app records every frame's CPU, GPU and display times from outside the game through Windows' own event tracing (ETW) [S26]. It is MIT-licensed (Intel, 2017–2024) and works across vendors and graphics APIs. Unreal Insights tracing in Shipping is limited ("full tracing in shipping is not supported", 5.5) [S45, SNIPPET].
- **Soak.** The route looped for hours, watching the game's memory from outside and counting crash-free hours.
- **Report shape.** One folder per run holding a verdict file (pass or fail per stage), log, crash files, pictures, a frame-time summary per stage, and the AI tester's notes, worst first.

## (d) Concrete steps for LEDGER, in order

Efforts are my estimates, in AI-session days.

**Step 0. Three one-off trials (2–3 hours, mostly packaging time).**
(a) Package once with the Test client configuration. It is expected to fail on the launcher engine; if it builds, Test becomes the performance build.
(b) Package Shipping with logging turned on by the installed-engine route [S41]. If it works, decide whether logging stays in players' copies or only in testing copies.
(c) Point launch.ps1's Gauntlet call at the Shipping build with `-configuration=Shipping` and confirm it finds and supervises the exe.

**Step 1. Smoke test on every packaged build (0.5–1 day).**
- Development: in the same workflow job as packaging, so it can never overlap a build. Gauntlet `UnrealGame.DefaultTest` with a limit of about 5 minutes. The game gets a smoke switch that reaches the street, waits N seconds, writes `LEDGER-CHECK smoke ok` and quits itself, which counts as a normal requested exit. It passes on that exit plus the check line, with no crash folder and no new error lines. Off-screen rendering is fine here, because nothing is pressed.
- Shipping (release candidates): the same, judged on exit code, crash folder and the game's own event file. Alternatively, quit through the real menu with real key presses, which also tests the menu and needs no test switch in the release binary.

**Step 2. The scripted route with real inputs (2–4 days). This is the audit's missing layer.**
- **Driver.** A fixed script built from the AI tester's own key, mouse and typing functions [P2], with no model involved. Gauntlet supervises. The window must be visible at 1280x720, never rendered off-screen.
- **Stages, from NOW item 1.** Street reached; talk box opened; a line containing w, a, s and d typed, with Tom not moved; a reply spoken (stand-in); Rita's window broken; witness sees; Z waits and the town's hours run; gossip reaches its hearer; consequence the next morning; save; quit; relaunch; Continue; Tom at the saved place and minute.
- **Robustness.** Start from a fixed spawn. Walk in short legs, checking between legs and correcting with a turn. Wait on stage lines, not fixed sleeps. Retry once, then fail with a picture. Tell apart "the script got lost" and "the game failed". Never teleport or call game code to make progress; that would not be real input.
- **Status.** Established practice: scripted play-throughs of the main route [S30][S31]. Recommendation: do it with OS-level input, because the known escaped bug lived in the keyboard-to-game layer [P2].

**Step 2b (optional, 1–2 days).** Convert the CI walk, which now moves the pawn with `AddMovementInput` [P5], to Enhanced Input injection of the player's own actions, so it exercises triggers, modifiers and the character's input handlers. It runs off-screen and does not need the desktop. It does **not** cover Windows, focus or typing, so it supplements Step 2 and cannot replace it.

**Step 3. The AI tester's exploratory walk (0.5–2 days of changes).**
- It already exists: Claude Code reads screenshots and sends real keys, and Gauntlet supervises [P2][P3]. Its default target should be the packaged Development build, with the real cast, light and sound. Talk must not use LEDGER's live key, because no automated tool may. Two ways remain, and the choice is Jafar's: the stand-in; or, added by the session that saved this note, real replies written through Claude Code's non-interactive mode on his subscription, which CLAUDE.md already allows for "the few talk checks that need a real reply", if the talk helper can be pointed at it (not checked).
- **Clock.** At two game minutes per real second, ten seconds of thinking costs twenty game minutes. In Development, pause the world between steps using real key presses: the console's pause, or a development-only key that holds the clock. The benchmarks do the same [S27][S36]. In Shipping, use the game's own pause menu if it has one; otherwise treat clock oddities in the report as possibly caused by the tester.
- **Shipping in a fresh Windows account (Step 3b, about 1 day including a trial).** Try launching the Shipping game from Jafar's session as the fresh user. Windows' "run as different user", with that user's profile loaded, gives the fresh account's folders, settings and PATH, while the window stays on Jafar's desktop where the tester can see and press. **Unverified**: confirm profile, GPU, audio and input once. Fallbacks: an automated walk in Jafar's account with the game's saved folder emptied, plus a five-minute manual start in the fresh account. Camera turning in Shipping must use relative mouse moves, which play.py already sends [P2], because `Slate.ForceRawInputSimulation` does not exist there [P1].

**Step 4. Performance (0.5 day plus a decision record).** PresentMon runs during Step 2's route and gives frame-time percentiles per stage. It is a new tool, so it needs a decision record (licence allowlist, process rule 2).

**Step 5. Running on this PC without clashing.**
- One lock: the AI tester already waits while the build machine runs any game or Unreal [P2]. The route script and Shipping smoke should use the same check. Development smoke runs inside the packaging job.
- Steps 2 and 3 need an unlocked, idle desktop; a runner working in Jafar's interactive session, not as a Windows service [P1][S50]; and the game and driver at the same administrator level [P1]. A locked screen stops the key presses [P1], so night runs need Jafar's decision.
- The graphics card is the builder's first: schedule the route when no render job runs.
- Before adding a scheduled workflow: it holds the build machine for about 20–30 minutes and uses no API. GitHub's 2026 billing for self-hosted runners was **not verified**.

**Step 6. How often.**
- Smoke: every packaged build, and every Shipping release candidate.
- Real-input route: nightly while the playable route is the priority, after any change to controls, the talk box, UI or save, and on Shipping for each release candidate.
- AI tester: 20–30 minutes daily during this push, and 30 minutes on Shipping per release candidate (NOW item 3).
- Performance: every route run.
- Soak: weekly, once the route passes.

**Step 7. What Jafar sees.** One line per run in the day's summary, for example: "Route walk, last night, packaged game: 12 of 13 stages passed; failed at 'reload puts Tom where he saved' (picture)." Failures go to FINDINGS, and the tester's worst three notes are listed. Nothing goes on his approval page, because none of this is taste.

Total: about 5–9 days for everything. Steps 0–2, about 3–5 days, answer the audit.

## (e) What could not be verified or reached

- **Engine source.** Not readable here; [P1] is relied on for anything in the engine code.
- **Build configurations.**
  - The Test configuration on launcher 5.8.2 [S24][S40]: not tried.
  - Logging in Shipping on an installed engine [S41]: snippet only.
  - Whether development automation tests are compiled into Test.
- **Gauntlet with Shipping.** Whether Gauntlet supervises a Shipping build, and whether its plug-in compiles into Shipping.
- **Shipping behaviour.**
  - Whether `Input.+key` exists in Shipping, and the exact path it takes.
  - Whether custom launch switches reach the game in Shipping on Windows (believed yes).
  - Whether Shipping writes crash folders without the crash-report client.
- **This PC.**
  - Whether "run as different user" works for the fresh-account walk.
  - Whether the game keeps ticking normally while Windows is locked (relevant to Step 2b).
  - GitHub billing for self-hosted runners in 2026. The session's search limit ran out before this could be checked.
- **Blocked sources, taken from search summaries only:** GDC Vault and GDC news, gamedeveloper.com, 80.lv's full text, Epic's forums, issue tracker and community pages, unrealengine.com, YouTube, arXiv, ea.com, Riot's tech blog, Microsoft Learn, GitHub Docs, alttester.com, gamedriver.io, intel.com, Hōru's Gauntlet blog (a small studio's write-up; horugame.com), Andrew Fray's blog, bugnet.io and jessicabaker.co.uk.

## Sources

Each source was read on 30 Sep 2026. Epic documentation pages carry no date; they are the 5.8 documentation.

**Opened**
- [S1] Gauntlet Automation Framework Overview in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-overview-in-unreal-engine
- [S2] Running Gauntlet Tests in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine
- [S3] Gauntlet Automation Framework in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine
- [S4] Gauntlet Controller in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/unreal-engine/gauntlet-controller-in-unreal-engine
- [S5] Build Configurations Reference, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configurations-reference-for-unreal-engine
- [S6] Packaging Your Project, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project
- [S7] Unreal Engine Build Tool Target Reference, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-build-tool-target-reference
- [S8] Run Automation Tests in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- [S9] Functional Testing in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine
- [S10] Automation Driver in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine
- [S11] Enhanced Input in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine
- [S12] Inject Input for Action (Blueprint API), Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Input/InjectInputforAction
- [S13] IEnhancedInputSubsystemInterface (API), Epic Games, undated (5.8), https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/EnhancedInput/IEnhancedInputSubsystemInterface
- [S14] Horde in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/unreal-engine/horde-in-unreal-engine?lang=en-US
- [S15] Horde Test Automation Tutorial, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-test-automation-tutorial-for-unreal-engine
- [S16] Screenshot Comparison Tool in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine
- [S17] Crash Reporting in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/crash-reporting-in-unreal-engine
- [S18] Automation Test Framework in Unreal Engine, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine (says nothing about build configurations)
- [S19] Introduction to Performance Profiling and Configuration, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine (says nothing on which configuration to profile)
- [S20] Trace Quick Start Guide, Epic Games, undated (5.8), https://dev.epicgames.com/documentation/en-us/unreal-engine/trace-quick-start-guide-in-unreal-engine (says nothing on Shipping)
- [S21] ue4-test-automation README, Daedalic Entertainment, repository created 21 Apr 2020, last push 18 Aug 2022, MIT, https://github.com/DaedalicEntertainment/ue4-test-automation
- [S22] UE5_GauntletAutomation README, Narsell, 16 Jul 2024, https://github.com/Narsell/UE5_GauntletAutomation
- [S23] GauntletAutomationDemo, S1Lazza, 24 Mar to 21 Apr 2024, MIT, https://github.com/S1Lazza/GauntletAutomationDemo
- [S24] ue4-unreal-automation-tool README, botman99, undated, https://github.com/botman99/ue4-unreal-automation-tool/blob/main/README.md
- [S25] AutoReplay README, msaljuk, created 1 Apr 2024, updated 12 Aug 2026, https://github.com/msaljuk/AutoReplay
- [S26] PresentMon README and licence, Intel (GameTechDev), © 2017–2024, MIT, https://github.com/GameTechDev/PresentMon
- [S27] OmniGameArena README, mxlin043, 2026, https://github.com/mxlin043/OmniGameArena

**Snippet only**
- [S28] Automated Testing of Gameplay Features in 'Sea of Thieves', Robert Masella (Rare), GDC 2019, https://gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features
- [S29] Automated Testing at Scale in Sea of Thieves, Jessica Baker (Rare), Unreal Fest Europe 2019, https://dev.epicgames.com/community/learning/talks-and-demos/R1w/automated-testing-at-scale-in-sea-of-thieves-unreal-fest-europe-2019-unreal-engine
- [S30] Automated Testing: Using AI Controlled Players to Test 'The Division', Jose Paredes and Pete Jones (Ubisoft Reflections), GDC 2019, https://gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled ; write-up at https://80.lv/articles/gdc-using-ai-controlled-players-to-test-the-division
- [S31] Automated Testing for League of Legends, Riot Games (Jim Merrill), undated in the summary, https://technology.riotgames.com/news/automated-testing-league-legends
- [S32] Running an Automated Test Pipeline for the League Client Update, Riot Games, undated in the summary, https://technology.riotgames.com/news/running-automated-test-pipeline-league-client-update
- [S33] Using Unreal Automation at Riot Games: Make Unreal Do the Work for You, Riot Games, Unreal Fest Gold Coast 2024, https://dev.epicgames.com/community/learning/talks-and-demos/PYqL/unreal-engine-using-unreal-automation-at-riot-games-make-unreal-do-the-work-for-you-unreal-fest-gold-coast-2024
- [S34] The Topography of Unreal Test Automation in 2025, Andrew Fray, 9 Apr 2025, https://andrewfray.wordpress.com/2025/04/09/the-topography-of-unreal-test-automation-in-2025/
- [S35] Technical Challenges of Deploying Reinforcement Learning Agents for Game Testing in AAA Games, EA SEED, CoG 2023 (arXiv July 2023), https://arxiv.org/abs/2307.11105 and https://www.ea.com/seed/news/cog23-challenges-deploying-rl-agents-game-testing
- [S36] VideoGameBench: Can Vision-Language Models complete popular video games?, authors not recorded, May 2025, https://arxiv.org/abs/2505.18134
- [S37] OmniGameArena: A Unified UE5 Benchmark for VLM Game Agents with Improvement Dynamics, 8 Jun 2026, https://arxiv.org/abs/2606.09826
- [S38] Gauntlet Primer, Branden T. (Epic knowledge base), undated, https://dev.epicgames.com/community/learning/knowledge-base/9yod/unreal-engine-gauntlet-primer (page body did not load)
- [S39] A Tech Artist's Guide to Automated Performance Testing, Unreal Fest Bali 2025, https://dev.epicgames.com/community/learning/talks-and-demos/0zx9/unreal-engine-a-tech-artist-s-guide-to-automated-performance-testing-unreal-fest-bali-2025
- [S40] "Enabling the 'Test' build configuration in a launcher/binary build?" (https://forums.unrealengine.com/t/enabling-the-test-build-configuration-in-a-launcher-binary-build/51319) and "Test build configuration not available" (https://forums.unrealengine.com/t/test-build-configuration-not-available/1815558), Epic forums, undated
- [S41] "Enable logging in shipping build using Installed Builds?", Epic forums, undated, https://forums.unrealengine.com/t/enable-logging-in-shipping-build-using-installed-builds/1805603 ; "Enabling Logging in Shipping Builds", Epic knowledge base, undated, https://dev.epicgames.com/community/learning/knowledge-base/vzvZ/unreal-engine-enabling-logging-in-shipping-builds
- [S42] "[UE5.0] How to enable console command in shipping build?", Epic forums, undated, https://forums.unrealengine.com/t/ue5-0-how-to-enable-console-command-in-shipping-build/541210
- [S43] "Running Gauntlet tests in 'Test' configuration", Epic forums, undated, https://forums.unrealengine.com/t/running-gauntlet-tests-in-test-configuration/1360273
- [S44] Unreal Engine Optimization Guide: Profiling Fundamentals, Intel, undated, https://www.intel.com/content/www/us/en/developer/articles/technical/unreal-engine-optimization-profiling-fundamentals.html
- [S45] "Full tracing in shipping is not supported", Epic forums, undated, https://forums.unrealengine.com/t/full-tracing-in-shipping-is-not-supported/2628210
- [S46] Unreal Engine Crash Log Analysis, Bugnet, undated, https://bugnet.io/blog/unreal-engine-crash-log-analysis
- [S47] "GameDriver Unveils Standalone Test Assistant for Unity and Unreal, Alongside Transparent Pricing", Business Wire, 17 Mar 2025, https://www.businesswire.com/news/home/20250317108053/en/GameDriver-Unveils-Standalone-Test-Assistant-for-Unity-and-Unreal-Alongside-Transparent-Pricing ; "Getting Started with GameDriver and Unreal Engine", GameDriver, undated, https://kb.gamedriver.ai/getting-started-with-gamedriver-and-unreal-engine
- [S48] AltTester pricing, undated, https://alttester.com/pricing/ ; "AltTester Pricing & Plans Update, effective from July 1st, 2026", https://alttester.com/alttester-pricing-plans-update-effective-from-july-1st-2026/ ; AltTester Unreal SDK "Get Started", undated, https://alttester.com/docs/unreal-sdk/latest/pages/get-started.html
- [S49] "The State of AI for Game QA", Naavik, undated, https://naavik.co/ai-gaming/the-state-of-ai-for-game-qa/ ; "How to Test Your Game or App with AI Agents", nunu.ai, undated, https://nunu.ai/blog/how-nunu-works
- [S50] actions/runner issue #2540, "Running as a service doesn't include user PATH env var", GitHub, undated, https://github.com/actions/runner/issues/2540
- [S51] "SEED Applies ML Research to the Growing Demands of AAA Game Testing", EA SEED, undated, https://www.ea.com/seed/news/seed-ml-research-aaa-game-testing

**The project's own files, read 30 Sep 2026**
- [P1] production/research/ai-tester/WHAT-UNREAL-PROVIDES.md (23 Sep 2026; read the engine source on the PC)
- [P2] tools/ai-tester/play.py, and commit 72802eca (29 Sep 2026), which records the typing bug the tester found once it typed with real key presses
- [P3] tools/ai-tester/launch.ps1
- [P4] the packaging step in .github/workflows/ledger-probe-unreal.yml
- [P5] ue-probe/Source/LedgerProbe/Private/WalkProbe.cpp
