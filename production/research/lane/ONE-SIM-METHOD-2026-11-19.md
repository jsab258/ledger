# One simulation in the browser: which way (19 November 2026)

Task 4s of the cloud lane, first run. Written the same day the things below were built and run. Every number here was measured today in the cloud unless it says otherwise. Not yet reviewed by a fresh reviewer.

## The answer in seven lines

1. The reference is the C# Core. Canon says so, the golden table is written by it, and the Unreal port is checked against it. All three were re-run today and agree.
2. Picked for building now: the game's own C++ town code (the Unreal port), compiled to WebAssembly. It is the code the packaged game runs, so prototype and game then share the same files.
3. It works today, in a real browser. All 102,949 comparable answers of the C# Core's table came out the same, and six scripted weeks played hour by hour through the new front door matched the C# Core on all 225 hours.
4. It is small and fast: 80 KB to download (compressed), and about 15 thousandths of a second of work for one game day with the Hook's 41 people.
5. The C# Core itself in the browser (his first choice in the decision of 17 November, "if it works") could not be built here: the cloud's network still refuses Microsoft's package site. It has not failed. It has not been tried.
6. A JavaScript port by hand is not picked. It would be a new copy of about 13,000 lines of rules, which is the fault the audit named (H20).
7. Two things need his word before anything is published: one choice (keep this way, or also build the C# one on a GitHub build machine) and licence lines for the list. Both are written out below.

## The questions this study answered

1. Which of the three copies is the reference, and how is that proved?
2. Can the C# Core be built for the browser from the cloud? If not, what exactly stops it?
3. Can the C++ port be built for the browser, and does it give the C# Core's answers there?
4. What would a hand-written JavaScript port cost, and what would hold it true?
5. For each way: download size, speed for one game day, the licence of every tool and shipped part, what it needs from Unity or Unreal, and the risk.
6. Which way, and what does it leave undone?

## 1. Which copy is the reference

The C# Core (ledger/Assets/Scripts/Core, 140 files, 50,561 lines). Evidence, each read or run today:

- canon.md, OPEN 1: "Unity is the legacy reference build; the C# Core stays the source of truth the C++ port is checked against."
- DECISIONS.md, 17 November 22:38, his decision: "one simulation (the C# Core in the browser if it works, else the same goldens)".
- The golden table is written by the Core itself. ledger/PerceptionGolden compiles the Core's files directly, with this note in its project file: "A golden table generated from a copy of the logic would prove the copy agrees with itself."
- How the port proves it matches: tools/port-golden-check.sh asks the Core for a fresh table, compares it with the committed one (ue-probe/perception-golden, five parts), then compiles the port's own test (ue-probe/tests/core-port-test.cpp) and has the port answer every row. Numbers must agree to 1e-9, everything else exactly. Rows the port cannot answer are skipped only by name and counted.
- The Core has no Unity in it. Four of its files mention Unity, in comments only (searched today). It builds on plain .NET.

Run today, on the real files, nothing copied:

| Check | Result |
|---|---|
| Core built with .NET SDK 8.0.428 (the version its projects ask for, no edit) | Built in 8 s, no errors. |
| Golden table from the Core today | 102,960 rows, 267 rule names. Identical to the committed table. |
| CoreTests (the Core's own tests) | "All 5255 checks passed." 11 s. |
| Soak (7 residents, 500 game days, twice) | "all 9 checks passed". 0.0003 s per game day. |
| The port, built natively (g++), against the fresh table | 102,953 rows compared, 0 differ, 7 skipped by name. 1.3 s. |

Limits of that proof, so nobody reads more into it than is there:

- The port holds 27 of the Core's 140 files (by name: Gossip, MemoryStore, CastDay, Perception, Observation, Sighting, Suspicion, Suspecting, Reaction, PoliceFile, TownWeek, TownRounds, TownNews, TownSave, SaveCodec, Arrangement, FirstWeek, WeeksEnd, Waiting, StreetVoice, OwnLines and a few more). Money, debts, jobs, fights and talk are C# only.
- Seven rows (the player's claims) are not ported. They are skipped by name.
- The audit of 5 October found that 11 of 30 planted one-line breaks in the port failed no test (CATALOGUE.md). Rows were added on 28 October. How many of the 11 are caught today was not re-measured: unverified.
- In the packaged game, talk is decided by the C# Core in a helper program, the town's hours by the port (FINDINGS.md line 9). So the game itself runs two of the three copies.
- Measured today with seven newly planted breaks (section 3): two of them fail no row of the table. One is the hourly closing of the week's end (TownWeek.h, HourEnd). The other is the order of the two nine o'clock steps, which the table records by name only. The table's blind spots are the same for the port in the game and for the browser copy.

## 2. The three ways, side by side

| | (a) The C# Core compiled for the browser (.NET) | (b) The game's C++ port compiled for the browser | (c) A JavaScript port by hand |
|---|---|---|---|
| What runs | The reference itself, all 140 files | The code the packaged game runs, 27 of the 140 | A new copy |
| Built today? | No. The cloud cannot fetch its parts. | Yes. Built, tested, run in Chromium. | No. Three small rules exist from 17 November. |
| Download | About 2 to 4 MB compressed. Estimate, not measured. | 80 KB compressed (measured: 301,665 bytes, 102,362 gzip, 79,767 Brotli), plus a 3 KB loader. | Smallest. Text only. |
| Speed, one game day | Not measured in a browser. Natively the Core does a 7-resident day in 0.0003 s. Microsoft says the browser's interpreter runs "slower". | About 15 ms for 41 people, town talk included (measured, 13 to 18 ms over ten runs). | Not measured |
| Whole golden table | 4.3 s natively, including starting .NET | 2.4 s in the browser engine. Natively 1.3 s. | Not applicable |
| Needs from Unity or Unreal | Nothing. Two files (FastChecker.cs, LlmClient.cs) use things a browser lacks. They stay compiled and are never called (study of 17 November). | Nothing. The port's test already builds these files with an empty stand-in for Unreal's header. The same stand-in is used. | Nothing |
| Tools | .NET SDK, the browser runtime pack (only on NuGet), Emscripten for the faster kind of build | wasi-sdk 34 (one download from GitHub) | None |
| Can the cloud build and test it? | No. NuGet is refused. Needs a GitHub build machine for every change. | Yes. With the tools downloaded once, everything builds and all tests pass in about two and a half minutes (148 s on the last run). | Yes |
| Main risk | Size, start-up time, and the prototype running rules the game's port does not have yet | Only the ported rules are there. A new rule must be written in C# and then in C++ before the prototype shows it. | A hand copy drifts. The table checks single rules, not the order of a day. |

### (a) The C# Core compiled for the browser

- What stops it here. The browser runtime (Microsoft.NETCore.App.Runtime.Mono.browser-wasm) is published only on NuGet. Today the cloud's network gate answered 403 for api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com and dotnetcli.azureedge.net. That is the same refusal as on 17 November. It is a network rule, not a fault in the method. No way round it was tried.
- What did work today. The .NET SDK itself can be had in the cloud from conda-forge (8.0.428, with 10.0.404 and 11.0.100 also there). That is how the Core, its table and its tests were run here. On 17 November the SDK came from Ubuntu's archive. Today that archive answered only over https (its lists were read at 13:54 UTC). It carries the SDK (8.0.134 and 10.0.115) and no browser runtime for .NET.
- Looked for the browser runtime elsewhere: npm (searched today, nothing), conda-forge (its whole index searched today, nothing) and Ubuntu's archive (package names searched today, nothing). PyPI was not searched. So it stays a GitHub build machine job, as the study of 17 November said.
- Size. Not measured. A smallest .NET browser app is 6.8 MB, or 2.0 MB with Brotli. With "invariant globalisation" it is 4.3 MB, or 1.4 MB with Brotli (Andrew Lock, 12 August 2025, .NET 10 preview 6, re-read today). Our Core adds about 1.1 MB before trimming (measured 17 November). Hence "about 2 to 4 MB".
- Speed. Not measured. Microsoft: "Because the .NET IL code is interpreted, apps typically run slower than they would on a server-side .NET JIT runtime." The faster kind of build makes most apps "about twice the size" and needs Emscripten, and Python on Linux (Microsoft Learn, read today).
- Versions. The browser runtime pack is at 11.0.0 and 10.0.15, both dated 10 November 2026, MIT (nuget.org page, read today through the search tool, not from this machine). The Core targets .NET 8.

### (b) The game's C++ port compiled for the browser

- Tool. wasi-sdk 34.0, which is the clang compiler (LLVM 23.1.0) with a C and C++ library for WebAssembly. One file from GitHub's release downloads, which the cloud can reach. Version 34 was found by trying the release addresses: 34 answers, 35 and 36 do not. Its release date was not read.
- Emscripten, the usual tool for this, was not needed and not tried. Its own download site (storage.googleapis.com) is refused by the cloud. Its latest release is 7.0.0 of 6 November 2026 (its changelog, read today). conda-forge carries an older 4.0.9 and Ubuntu's archive a much older 3.1.6.
- Flags. The game's own: no C++ exceptions, with the same switch the Unreal module sets (LEDGER_CORE_NO_EXCEPTIONS). Four rows (FactNull) need exceptions and are skipped by name, exactly as in the Unreal build. Built a second time with exceptions on, those four are answered too and agree.
- One snag, one line. The port names a constant inside a class (AdasTea::Ada in FirstWeek.h) in a way the C++14 standard needs a second line for. g++ lets it pass. This compiler does not. Built as C++17 it is fine. The Unreal project sets no standard of its own (searched), so the game takes Unreal 5.8's default, which was not looked up today. Nothing was changed in ue-probe. It is a small finding for the port's owner: this machine's own clang, given the command tools/port-golden-check.sh uses when g++ is missing, fails to link the port test for the same reason.
- What the module asks of the outside world: four small system calls (print, close, seek, and the clock). The loader answers the clock with zero. The port's own source never reads the computer's clock or random numbers (searched today). The same calls therefore always give the same town.

### (c) A JavaScript port by hand

- The port's rule files are 12,926 lines of C++. A JavaScript port is that much again, typed by hand, as a new copy.
- The tools from 17 November (tools/lane/simwasm) hold a JavaScript rule to the golden rows. They still work. They check single rules. They cannot check the order in which a town's hour runs unless someone ports that too.
- It needs no tool, ships no runtime and raises no licence question. Those are its only advantages.

## 3. What was built and what it proved today

All in tools/lane/one-sim/. Nothing was written under ledger/ or ue-probe/. Their files are compiled from where they live.

| Test | What it shows | Result |
|---|---|---|
| The port's own golden test, unchanged, compiled to WebAssembly (game's flags) | The port gives the C# Core's answers inside a browser engine | 102,949 rows compared, 0 differ, 0 unanswered, 11 skipped by name (7 claims, 4 FactNull) |
| The same, with exceptions on | The four FactNull rows too | 102,953 compared, 0 differ, 7 skipped |
| T1: every golden row asked through JavaScript, no files (cast files handed in as text) | The module loaded the way a page loads it gives the same answers | 102,949 agree, 0 differ, 11 skipped by name. 3,500 of the rows are seeded whole runs (GossipFuzz). |
| T2: routines through the front door | Where each person is, each hour of the week, both casts | 8,568 of 8,568 agree with the C# Core |
| T3: the week hour by hour through the front door | Six scripted weeks (a refusal, a night away, held in the cells, five days with Rita's window and the tea, the wind-down, the tea day). What the player does is called from JavaScript. Each hour's 13 results are compared with the C# Core's row for that hour. | 225 of 225 hours agree, field for field |
| T4: same calls twice | The same town to the last character | Same digest both times, and the same digest in Node and in Chromium |
| T7: the Ledger's facts through the front door | Who knows what and how (saw it or was told, from whom, how well the first witness saw him), read back after every scripted hour | At all 225 hours the number of facts is the hour's own count, which T3 holds to the C# Core. Nobody but the witness is said to have seen the window go. The witness holds it first-hand and recognised at all 130 hours after the deed. |
| T6: rough handling | Calls before a town exists, broken cast files, times that are no time, answers outside the list, odd text, a thirty-day jump, a second town | Nothing fell over. The thirty-day jump took about 0.16 s. |
| The same checks inside a real web page | It works in a browser, not only in Node | Chromium 157.0.8103.78, headless: all passed |
| Selftest: four rows spoiled on purpose | The checks can fail | Each spoiled row was caught by its own check, 7 of 7 |
| Planted breaks: seven one-line changes to a copy of the port (a step an hour late, a step dropped, two steps swapped, routines an hour out) | Whether the front door's checks (T2, T3) notice a changed rule | 5 of 7 seen. The other two fail no row of the whole table either. |

The front door so far (wasm/one_sim.cpp, 25 calls, four of them plumbing, no rule of its own): make a town from a cast file, run one game hour in the game's own order (TownWeek::RunHour), the player's acts between hours (the deed, his answer to the ask, the tea, the week's end, a police report, being taken in), and reading back: where someone is, the week's state as the game's save writes it, and who knows what and how. That last one is what a Ledger screen would be drawn from.

## 4. Licences against the allowlist (ledger-v2/research/license-allowlist.md, read today)

None of the parts below is on the list. Item 13 covers three.js, esbuild, acorn and puppeteer-core for the prototype. PROCESS 2 asks for a decision record for any new tool. Nothing has been published. These are lines for his list, not assumptions.

Shipped inside the prototype page (inside one-sim.wasm):

| Part | Licence | How it was checked |
|---|---|---|
| Pieces of the C++ library, libc++ and libc++abi (the LLVM project) | Apache 2.0 with the LLVM exception | Read today in the shipped files themselves: the licence line appears 3,378 times in the headers that came with the compiler. |
| The compiler's small helper routines (compiler-rt, also the LLVM project) | Not read: unverified | Their own notice was not found in the download. To be read at the source before anything ships. |
| Pieces of the C library, wasi-libc | Its source page lists three licence files: Apache 2.0, Apache 2.0 with the LLVM exception, and MIT | Page read today. The licence text itself, and the notices of the older libraries it is built from, were not read: unverified. To be read before anything ships. |
| The town rules themselves | Ours | |

Tools, never shipped:

| Tool | Licence | How it was checked |
|---|---|---|
| wasi-sdk 34 (with clang and LLVM 23.1.0) | Apache 2.0 | Its source page, read today. The download carries no licence file (searched). |
| .NET SDK 8.0.428 and runtime 8.0.34, to run the Core's checks in the cloud | MIT, "Copyright (c) .NET Foundation and Contributors" | Read today from the licence file shipped in the package. The project already uses the .NET SDK on the PC and the build machine. |
| conda-forge's packaging of it | BSD 3-clause (the recipe) | Read today in the package. |
| Node 22 (tests) | MIT | Read on 17 November by the earlier study. |
| Playwright with Chromium (the page test) | Not read: unverified | Already used by the prototype's tests in the cloud. |
| The Python zstandard module (unpacks the conda packages) | Not read: unverified | |

If way (a) is ever built, it adds the .NET browser runtime (MIT) and the parts inside it, as the study of 17 November listed.

## 5. The pick, and why

Way (b): the game's own C++ town code, compiled for the browser.

1. It is proved, today, in a browser. The other two are not.
2. It is the game's code. Read today: the game's own CrimeProbe.cpp (line 7821) runs each game hour through TownWeek RunHour, the same call the front door makes. After this, prototype and packaged game run the same files. With (a) the prototype would run the reference while the game went on running the port, and the two could still differ wherever the port does.
3. It is 80 KB against an estimated 2 to 4 MB, and it starts at once.
4. The cloud can build and test it alone in under three minutes. Way (a) needs a GitHub build machine for every change.
5. It fits his decision of 17 November as written: "the C# Core in the browser if it works, else the same goldens". This is the same goldens, and not through a new copy.
6. It closes no door. The front door is text in, text out. A C# build could sit behind the same calls later and be held to the same tests.

What it does not give:

- Rules that live only in C# (money, debts, jobs, fights, talk). In the prototype these stay in its JavaScript for now. That part of H20 stays open until they are ported or (a) is built.
- A new town rule reaches the prototype only after it is in the Core with golden rows and in the port. That is already the rule for the game. It makes trying a rule in the prototype slower than editing JavaScript.
- Where the port is wrong and the table does not see it, the prototype is wrong the same way. So is the game.

## 6. For his list

One choice (scope), recommendation marked:

- A (recommended): the prototype runs the game's own town code compiled for the browser, as built today. Nothing more to buy or install.
- B: as A, and also build the C# Core for the browser on a GitHub build machine (15 to 27 hours of cloud work by the estimate of 17 November) and compare the two. Worth it only if the prototype is to run C#-only rules before they are ported.
- C: wait for B before changing the prototype.

Licence lines (needed before the prototype page is published with this inside):

- "The browser prototype only: the pieces of the LLVM project's C++ library and helper routines and of wasi-libc that the compiler builds into the simulation file (Apache 2.0 with the LLVM exception, Apache 2.0, MIT), notices kept." Recommended: yes, after wasi-libc's and the helper routines' licence texts have been read in full.
- "Tools, never shipped: wasi-sdk 34 with clang (Apache 2.0); the .NET SDK from conda-forge (MIT) for the Core's checks in the cloud." Recommended: yes.

## Sources (all read 19 November 2026)

- In the project: canon.md (OPEN 1); DECISIONS.md line 339; tools/port-golden-check.sh; ledger/PerceptionGolden/PerceptionGolden.csproj; ue-probe/tests/core-port-test.cpp and unreal-shim/CoreMinimal.h; ue-probe/Source/LedgerProbe/LedgerProbe.Build.cs; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp (line 7821); CATALOGUE.md line 30; FINDINGS.md line 9; production/audits/full-2026-11/AUDIT-REPORT.md (H20); production/research/lane/SIM-IN-BROWSER-2026-11-17.md; production/lane/K2-SIM-PORT-FAULTS-2026-11-18.md; ledger-v2/research/license-allowlist.md.
- Measured here: the logs of tools/lane/one-sim/one-sim.sh all (last run 14:05 UTC, 148 s, everything passed), Node 22.23.5, Chromium 157.0.8103.78, g++ 13.3.0.
- conda-forge package index (conda.anaconda.org/conda-forge, linux-64 and noarch, downloaded and searched): dotnet-sdk 8.0.428, 10.0.404, 11.0.100; emscripten 4.0.9; no .NET browser runtime.
- Ubuntu 24.04's package lists (archive.ubuntu.com over https, noble and noble-updates, main and universe): dotnet-sdk-8.0 8.0.134, dotnet-sdk-10.0 10.0.115, emscripten 3.1.6; no .NET browser runtime.
- The .NET licence file inside dotnet-runtime-8.0.34 from conda-forge.
- wasi-sdk 34.0 from https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-34/ (its VERSION file: LLVM 23.1.0, wasi-libc 2e6fb9d8ee0c); the repository page https://github.com/webassembly/wasi-sdk (licence box).
- https://github.com/webassembly/wasi-libc (licence files listed).
- https://www.nuget.org/packages/Microsoft.NETCore.App.Runtime.Mono.browser-wasm (versions, dates, MIT, 24.18 MB).
- Microsoft Learn, "ASP.NET Core Blazor WebAssembly build tools and ahead-of-time (AOT) compilation", .NET 11 version, footer "Last updated on 2026-07-22": https://learn.microsoft.com/en-us/aspnet/core/blazor/webassembly-build-tools-and-aot
- Andrew Lock, "Running .NET in the browser without Blazor", 12 August 2025: https://andrewlock.net/running-dotnet-in-the-browser-without-blazor
- Emscripten ChangeLog (Chromium mirror): https://chromium.googlesource.com/external/github.com/kripken/emscripten/+show/HEAD/ChangeLog.md ("7.0.0 - 11/06/26"). Only the first part of the page was read.

Unreached, and therefore not evidence: api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com, dotnetcli.azureedge.net and packages.microsoft.com (.NET's parts); storage.googleapis.com (Emscripten's downloads); Ubuntu's archive over plain http (over https it answers); api.github.com (so wasi-sdk's release list and date); a mirror copy of wasi-libc's LICENSE (came back unreadable).

Unverified, said again in one place: the size and speed of way (a) in a browser; wasi-libc's full licence text; the licences of the compiler's helper routines, Playwright, Chromium and zstandard; Unreal 5.8's default C++ standard; wasi-sdk 34's release date; how many of the audit's 11 unseen planted breaks are caught today; speed for a town of hundreds (41 people measured); any browser but Chromium (Firefox and Safari's engine were not on this machine).

Not done, by the project's own rules: a fresh reviewer has not checked this study against its sources, and no fresh helper has yet tried to break the build.
