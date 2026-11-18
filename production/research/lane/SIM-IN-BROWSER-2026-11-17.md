# Can the game's own simulation run in a web browser? (17 November 2026)

Review applied: the fresh review of 17 November (production/lane/reviews/REVIEW-SIM-IN-BROWSER-2026-11-17.md, PASS WITH FIXES) had 12 fixes, and all 12 are applied here. One town day was also timed, and the fallback tools were moved to tools/lane/simwasm/.

## The answer in five lines

1. Yes, very likely. The town simulation is plain C#. Two files hold parts a browser cannot use (starting a helper program, and the AI server's network handler). They stay in the build but are never called in the browser.
2. Proved today in the cloud: the simulation built on its own, and its 102,960 test answers came out identical, letter for letter, to the table kept in the project. One in-game day for the seven-resident test town took 0.4 thousandths of a second.
3. Not proved today: the browser step itself. The cloud's network refused Microsoft's two download sites, so it stopped after two tries. A GitHub build machine can reach them without changing anything.
4. Expected cost: about 2 to 4 MB for a player's browser to download (not measured), 15 to 27 hours of cloud work, and at most 2 hours on his PC. The parts are free MIT-style licences, but shipping them in a page is not yet on his licence list.
5. Recommendation: run the real simulation in the browser, with no second copy of the rules in JavaScript. It needs one licence line from him; the build goes on a GitHub build machine, so no network setting is needed. It waits for the next Monday order.

## What the question was

Could the browser prototype run the same C# simulation the game uses (the Core, the code the console checks such as PerceptionGolden, CoreTests and SimHarness already build), compiled to WebAssembly, instead of the rules being written a second time in JavaScript?

Correction to the brief: the Core today is 140 .cs files and 50,512 lines (2.76 MB of source), not about 280 files.

## What was tried, with exact results

All work was done on copies in the cloud scratch folder. The only project changes are this file and the small tools folder tools/lane/simwasm/.

| Step | Result |
|---|---|
| Microsoft's install script (dot.net) | Refused by the cloud's network (403). |
| .NET SDK from Ubuntu's own archive | Worked: .NET SDK 10.0.115, runtime 10.0.15, MSBuild 18.0.37, Ubuntu 24.04. |
| Build PerceptionGolden against the real Core (copied, target changed from net8.0 to net10.0 only; the reviewer diffed the copy against the Core and it is identical) | Built in 7.4 s, no errors, 5 warnings. Needed no packages from the internet. |
| Run it and compare with the committed table (ue-probe/perception-golden, five parts joined, line endings ignored) | First run differed: the program finds the casting files (production/specs/*.json) by looking upward from where it is built, and the copy was outside the project. With that folder linked in read-only, the output was IDENTICAL: 102,960 answers (102,962 lines, of which 2 are header lines) across 267 rule names. The reviewer re-ran it and got the same. |
| Speed, native, whole table | 3.69 s, 3.69 s and 3.80 s over three runs, including starting .NET (the reviewer measured 3.55 s). |
| Speed, native, the town's day loop (a copy of the Soak check, 7 residents, 500 in-game days run twice, seed 1) | 0.20 s and 0.18 s for the two runs: 0.0004 s per in-game day. All 9 Soak checks passed. This is a seven-resident town; a full town of hundreds is not measured. |
| Build the Core alone as a library, with Microsoft's browser compatibility check switched on | Built. Core library 1,140,224 bytes, 412,874 bytes gzipped, untrimmed. The browser check flagged only FastChecker.cs (starts a separate program) and LlmClient.cs (a network handler the browser does not have). These are warnings, not errors. No trimming warnings. |
| Install the browser build tools (dotnet workload install wasm-tools) | Refused: needs api.nuget.org, which the cloud's network blocks. This was the second and last attempt, as the rules say. |
| Look for the browser runtime on npm (which the cloud can reach) | Nothing usable: the runtime is published only on NuGet. |
| The fallback, tried for real: export the golden table to JSON and check JavaScript rules against it | Works. 102,960 rows, 267 rules, JSON 6.97 MB (432 KB gzipped). Three Perception rules written in JavaScript passed all 30 of their rows to 1e-9 under Node 22.23.4: MotionFactor 12 rows, ConeWeight 10, LightFactor 8. The four constants they use were each checked against rows that sit exactly on them. |

### What the scan of the Core found

- No reflection, no unsafe code, no native calls, and no JSON or XML libraries that need reflection. These are the usual causes of trouble in browser builds, and they are absent. The only GetType() calls (FastChecker.cs, MiniJson.cs) are in error messages and are harmless.
- The two browser-unfriendly files cannot simply be left out. LlmClient.cs (25 KB) also holds the message types and interfaces that six to eight other Core files use. ConversationEngine.cs keeps a FastChecker field. So both stay compiled. Their unsupported calls (Process.Start, SocketsHttpHandler) would fail only if called, and the browser front door never creates an AnthropicClient or a FastChecker.
- Threads: FastChecker.cs uses Task.Run and blocking waits. ConversationEngine.cs:1841 also uses Task.Run, but its result reads (lines 1812 and 1949) are guarded by a finished-task check, so nothing blocks. ClaimCheck.cs reads finished results the same way. A browser runs .NET on one thread, so the simulation should run inside a Web Worker (a background page thread) so the page never freezes.
- Files: only MemoryStore.cs reads and writes files (FastChecker aside), and only if given a path. The browser version has an in-memory file system, so it would still work; saves would be handed to the page as text instead.
- The golden program, but not the Core, reads the casting files from disk. In the browser these would be packed in with the build, or fetched and passed in as text.
- 17 Core files already use CultureInfo.InvariantCulture. Switching the browser build to "invariant globalisation" saves about a third of the download and leaves ICU, the locale data, out of the shipped files. The golden table would show at once if any rule depended on the locale.

## Size and speed

| | Figure | Source |
|---|---|---|
| .NET runtime in a browser, smallest app, default | 6.8 MB raw, 2.5 MB gzip, 2.0 MB Brotli | Andrew Lock, 12 Aug 2025, .NET 10 preview 6 (reviewer re-read it) |
| Same, with invariant globalisation | 4.3 MB raw, 1.7 MB gzip, 1.4 MB Brotli | same |
| Our Core library, untrimmed | 1.14 MB raw, 0.41 MB gzip | measured today |
| Estimated total, interpreted | about 2 to 4 MB compressed, unmeasured until plan step 4 | estimate. Lock's baseline is a trimmed hello-world. The Core also pulls in framework parts that baseline lacks: Regex (used in 23 files), Linq, Tasks and HttpClient. |
| With ahead-of-time compilation (faster) | "most AOT-compiled apps are about twice the size" | Microsoft Learn, ASP.NET Core 10 page, updated 22 Jul 2026 |
| Speed, interpreted | not measured. Microsoft says only that it runs "slower" than normal .NET, and that AOT gives "dramatic improvements" for heavy work. | Microsoft Learn, same page |
| Older data point, start-up | 1.4 s with AOT against 2.5 s interpreted | Uno Platform, 4 Dec 2020 (old) |

Plain reading: natively, one in-game day for the seven-resident test town takes 0.4 thousandths of a second. Even if the browser's interpreter is ten or more times slower (my estimate, not measured), a prototype that steps a small town a few times a second has a lot of room. That does not yet hold for a town of hundreds; plan step 4 measures it, and AOT is the tool if the interpreter is too slow.

## What it would take (the plan)

1. Write the decision record in DECISIONS.md (the allowlist's PROCESS 2) once he has ruled on the licence line. 0.5 hour.
2. Build on a GitHub build machine, which already reaches Microsoft's servers, so the cloud's network setting is not needed. Wiring it up: 0.5 to 1 hour. (The other way round the network is to have the cloud allowed to reach dot.net, builds.dotnet.microsoft.com and api.nuget.org.)
3. Add a new small project in its own folder. It compiles all the Core files for the browser (browser-wasm) exactly as PerceptionGolden does, FastChecker.cs and LlmClient.cs included, with no Core edit. It adds a thin front door marked [JSExport] (start a town, step it, give an action, read the state as JSON) that never creates the AI client or FastChecker. 3 to 6 hours. The other option is a Core edit that moves the message types out of LlmClient.cs; it touches game code and needs the full simulation check suite, so it is not recommended.
4. Run PerceptionGolden's rows inside the browser build under Node, and compare them with the committed table the way tools/port-golden-check.sh compares the C++ port. This proves the browser and the game agree. 2 to 4 hours.
5. Trim, switch on invariant globalisation and Brotli. Measure the real download and the time per town day, for the test town and a large one, and put the simulation in a Web Worker. 3 to 5 hours.
6. Wire the prototype page to it. 4 to 8 hours.
7. RECIPE.md lines, and one fresh review of the result. 1.5 to 2.5 hours.
8. Optional: an AOT build if the interpreter is too slow. Microsoft says it needs Python on Linux. 2 hours.

Hours: cloud, machine-free: 15 to 27 (steps 1 to 7), plus 2 if AOT is needed. On his Windows PC: 0 to 2, only to open the prototype in Edge or Chrome and look; nothing needs installing there. Under the weekly budget this is new work, so it goes on the Monday order's waiting list, not into the running week.

### Risks

- Network: the browser parts come only from Microsoft's servers. The GitHub build machine avoids this.
- Threading: multithreaded .NET in the browser is described as experimental in .NET 10 by a commenter (oroztocil) on dotnet/runtime issue 129900; the page as fetched shows no date. Microsoft's own documentation on this was not read, so the status is unverified. The plan does not depend on it: stay single-threaded in one Web Worker.
- Trimming: the scan found no reflection, so the risk is low, and the golden table catches any mistake.
- Version: .NET 11 came out on 10 November 2026 (search titles only, unverified). The Core targets net8.0 and builds unchanged on 10. Pin one version for the browser build.
- Drift: the browser build must compile the Core files directly, never a copy, exactly as PerceptionGolden does, or it stops proving anything.

## The fallback, if the browser route fails

Keep the rules in JavaScript, but hold them to the same answers. The tools are in the project at tools/lane/simwasm/:

- export_golden.py turns the committed golden table into JSON grouped by rule: { "MotionFactor": [ { "args": ["0.06"], "expected": "0.5012658227848101" }, ... ] }. The JSON is 6.97 MB (432 KB gzipped), so it is made on demand and never committed.
- harness.mjs loads the rows, calls the matching JavaScript rule, and fails on any wrong row. Its README line says how to run both. Demonstrated today: 30 of 30 rows passing.
- Number or text: every value stays a string exactly as the C# wrote it. Each JavaScript rule declares how it is compared: 'number' (within 1e-9, as for the C++ port; the C# writes these with D()) or 'text' (an exact match, which covers bits, written "0" or "1" by Bit(), and ids and words). Nothing is guessed from the value, so a bit is never compared as a number by accident.
- Constants: the harness does not trust its hand-typed constants (walk and run pace, the two view angles). It checks each one against rows that sit exactly on it, so a constant that drifts fails at once. The same pattern applies to every rule that is ported.
- Casting data: rules whose rows depend on the casting files (for example CastPlaceOf, 8,568 rows) need the same production/specs/*.json files in the JavaScript, loaded from the repository at the same commit the table was made from. The export should record that commit.
- Which rows: only the rules the prototype uses. Every JavaScript rule must have all its rows pass, and a rule with no rows in the table fails the harness. The table has 267 rule names; the biggest are WSoundRing (15,910 rows), OutdoorsAt (12,996), Stance (9,926), WTellWilling (9,472) and CastPlaceOf (8,568).
- Weaknesses: each JavaScript rule is a second copy that can drift from the game. And the golden rows check single rules, not the order in which a town steps, so a JavaScript town loop would have no check beyond its per-rule rows. These are the two reasons this is the fallback and not the plan.

## Licences against the allowlist (ledger-v2/research/license-allowlist.md, read today)

The project already builds and runs its console checks (CoreTests, PerceptionGolden) on the .NET SDK, so the new decision is narrow: shipping the .NET browser runtime and Emscripten's runtime pieces inside a prototype web page.

| Piece | Licence | On the allowlist? |
|---|---|---|
| .NET runtime and libraries (dotnet/runtime), shipped in the page | MIT, "Copyright (c) .NET Foundation and Contributors" (read from the installed SDK's LICENSE.txt today) | No |
| Third-party parts inside it (LLVM, zlib-ng, Mono; ICU and Unicode data only if invariant globalisation is off, which the plan avoids) | permissive notices listed in dotnet/runtime THIRD-PARTY-NOTICES.TXT | No |
| Emscripten (the tool that builds the browser runtime; its runtime pieces end up in the download) | MIT or University of Illinois/NCSA: "In practice you can just consider Emscripten as MIT licensed" | No |
| Node (only for running the tests, never shipped) | MIT, "Copyright Node.js contributors" (read from the installed Node 22.23.4 LICENSE today) | No, but it ships nothing |

The allowlist lists assets plus three MIT tools named by his pick (FoldCraft, ast-grep and PresentMon). It says nothing about the .NET runtime. Its PROCESS 2 asks for a decision record for any new tool (plan step 1). All of these are permissive and allow use in a sold product with the notice kept. The game itself is PC only; a browser prototype is a working tool, not a release.

## Recommendation

Use the browser route with the real Core, built on a GitHub build machine. It goes on the waiting list for the next Monday order. Two separate asks, kept apart as the rules require:

- Licence (his ruling): add "the .NET runtime (MIT) and Emscripten's runtime pieces (MIT), shipped only inside a browser prototype page, notices kept" to the allowlist. Recommended: yes. Without it, use the fallback (JavaScript rules held to the golden rows).
- Network (his sign-in or hands): none needed if the build runs on a GitHub build machine, which is recommended. Only if he would rather the cloud build it: on claude.ai in a web browser, Settings > Capabilities, allow dot.net, builds.dotnet.microsoft.com and api.nuget.org.

Until he answers, the fallback tools already serve either route at no risk: their rows are the same check the browser build must pass.

## Sources (all read or searched 17 November 2026)

- Microsoft Learn, "dotnet-install scripts reference": https://learn.microsoft.com/dotnet/core/tools/dotnet-install-script (install script location and flags).
- Microsoft Learn, "ASP.NET Core Blazor WebAssembly build tools and ahead-of-time (AOT) compilation", ASP.NET Core 10, updated 22 July 2026: https://learn.microsoft.com/aspnet/core/blazor/webassembly-build-tools-and-aot (wasm-tools is Emscripten-based, needs Python on Linux, AOT about twice the size, interpreter slower).
- Microsoft Learn, "Run .NET from JavaScript", ASP.NET Core 10: https://learn.microsoft.com/en-us/aspnet/core/client-side/dotnet-interop (JSImport and JSExport).
- Andrew Lock, "Running .NET in the browser without Blazor", 12 August 2025: https://andrewlock.net/running-dotnet-in-the-browser-without-blazor (wasmbrowser template, sizes).
- dotnet/runtime issue 129900, multithreaded WebAssembly crash: https://github.com/dotnet/runtime/issues/129900 (commenter oroztocil: "multithreading is still an experimental feature in .NET 10"; no date on the page as fetched).
- Start Debugging, "How to run CPU-bound work in a Blazor WebAssembly app with Web Workers in .NET 11", 2 August 2026: https://startdebugging.net/2026/08/how-to-run-cpu-bound-work-in-a-blazor-webassembly-app-with-web-workers-in-dotnet-11/ (single UI thread; the Web Worker approach).
- Uno Platform blog, 4 December 2020: https://platform.uno/?p=4063 (old start-up and size figures for AOT against the interpreter).
- dotnet/runtime THIRD-PARTY-NOTICES.TXT: https://www.github.com/dotnet/runtime/blob/main/THIRD-PARTY-NOTICES.TXT (the page as fetched was cut short).
- Emscripten README (Chromium mirror): https://chromium.googlesource.com/external/github.com/emscripten-core/emscripten/ (licence).
- .NET 11 release date, 10 November 2026: search result titles only, unverified (a forum page listing ".NET 11 GA, .NET 10.0.15, .NET 9.0.23 and .NET 8.0.34, Nov 10 2026" could not be fetched). The runtime installed today, 10.0.15, matches.
- Local: the installed SDK's /usr/lib/dotnet/LICENSE.txt (MIT); Node's /opt/node22/LICENSE (MIT); the committed golden table ue-probe/perception-golden/part-01 to part-05; the Soak check's own output.

Unreached, and therefore not evidence: dot.net and api.nuget.org (blocked by the cloud network), the forum page above, and Microsoft's own documentation on WebAssembly multithreading (not read).
