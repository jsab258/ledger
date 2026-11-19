# One simulation in the browser: which way (19 November 2026)

Task 4s of the cloud lane, first run. Written the same day the things below were built and run. Every number here was measured today in the cloud unless it says otherwise.

Reviewed the same day by a fresh reviewer (production/lane/REVIEW-ONE-SIM-STEP1-2.md: pass with fixes, 12 findings). The 12 fixes were applied in run 2, also on 19 November, and everything was built and run again from nothing. Where a fix changed a fact, the line says "(run 2)". A second fresh reviewer then checked run 2 (production/lane/REVIEW-ONE-SIM-RUN2.md: the 12 closed, pass with fixes for the bridge and the differences).

(run 3, 19 November) Two facts in this study have moved since, and their lines below say so: the licence line for the pieces that ship inside the simulation file is now on the allowlist (item 18, his yes of 17:29), and the sentence about Playwright and the prototype's tests was wrong and is corrected.

## The answer in seven lines

1. The reference is the C# Core. Canon says so, the golden table is written by it, and the Unreal port is checked against it. All three were re-run today and agree.
2. Picked for building now: the game's own C++ town code (the Unreal port), compiled to WebAssembly. It is the code the packaged game runs, so prototype and game then share the same files.
3. It works today, in a real browser. All 102,949 comparable answers of the C# Core's table came out the same, and six scripted weeks played hour by hour through the new front door matched the C# Core's thirteen answers for each of the 225 hours (who found the damage, who went to the police, why DS Ellis came, whether he was taken, Ada's invitation, Ron's envelope, the tea, held or not, the asks, what the outfit's man holds, how many stories the town holds, her first visit, his first arrest). Those thirteen are each hour's summary, not the whole town's state.
4. It is small and fast: 80 KB to download (compressed), and about 15 thousandths of a second of work for one game day with the Hook's 41 people (run 2 measured 17 to 22). (run 2) With the save routines the bridge needs, the download is 109 KB.
5. The C# Core itself in the browser (his first choice in the decision of 17 November, "if it works") could not be built here: the cloud's network still refuses Microsoft's package site. It has not failed. It has not been tried.
6. A JavaScript port by hand is not picked. It would be a new copy of about 13,000 lines of rules, which is the fault the audit named (H20).
7. Two things needed his word. He gave both on 19 November: way A (this one), and the licence line for the tools, now item 17 of the allowlist. The second licence line, for the small library pieces that end up inside the simulation file, was held in run 2: their full licence texts, read since, name four more licences than this study did (section 4). (run 3) He gave his yes to the fuller line the same day at 17:29, and the allowlist carries it as item 18. What still stands between the simulation file and a published page is the credits file (section 4) and the publish gate, not a licence.

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
- The Core has no Unity in it. No file of the Core uses UnityEngine (one comment names it, StreetVignette.cs line 107); 25 of the 140 files mention Unity in comments or messages (counted again in run 2). It builds on plain .NET (built today).

Run today on the real source files, compiled from where they live. No source file was copied or edited. The project files that list them are the lane's own:

- (run 2) The three check programs are built from lane-written project files (tools/lane/one-sim/reference) that list the same sources as the originals, so that no build output lands under ledger/. Since run 2 the script asks the build tool itself for both lists on every run and stops if they differ. Today they are the same: 142 files for PerceptionGolden, 142 for Soak, 153 for CoreTests.
- (run 2) Run 1's project files also switched on a setting the originals do not have (invariant globalisation: .NET ignores the computer's language settings). The reason is not recorded. It was not needed: this machine has the library .NET wants for language settings (libicu 74), and it has no language set, so .NET uses neutral settings here either way (checked with a three-line test program). The setting is removed. Every result below came out the same without it.
- (run 2) What that leaves unseen, measured: the cloud never runs the Core under a computer's real language settings. Run by hand under German and under Turkish settings (decimal comma), the golden table still came out identical to the committed one and Soak passed, but CoreTests stopped at its first failed check, "and a fall still reads as a fall", which got "-0,05" where it expects "-0.05". The cause is in the Core: Suspicion.cs lines 122 and 176 write a number with the computer's own settings. CoreTests stops at its first failure, so the checks after that one (it had passed 237 lines) were not run under those settings. This is a finding for the Core's owner, not fixed here. Under Swiss German and under British settings, which write a decimal point, all 5,255 checks passed and the table was identical.

| Check | Result |
|---|---|
| Core built with .NET SDK 8.0.428 (the version its projects ask for, no edit to any source) | Built in 8 s, no errors. |
| Golden table from the Core today | 102,960 rows, 267 rule names. Identical to the committed table. |
| CoreTests (the Core's own tests) | "All 5255 checks passed." 11 s. |
| Soak (7 residents, 500 game days, twice) | "all 9 checks passed". 0.0003 s per game day. |
| The port, built natively (g++), against the fresh table | 102,953 rows compared, 0 differ, 7 skipped by name. 1.3 s. |

Limits of that proof, so nobody reads more into it than is there:

- The port holds 27 of the Core's 140 files (by name: Gossip, MemoryStore, CastDay, Perception, Observation, Sighting, Suspicion, Suspecting, Reaction, PoliceFile, TownWeek, TownRounds, TownNews, TownSave, SaveCodec, Arrangement, FirstWeek, WeeksEnd, Waiting, StreetVoice, OwnLines and a few more). Money, debts, jobs, fights and talk are C# only.
- Seven rows (the player's claims) are not ported. They are skipped by name.
- The audit of 5 October found that 11 of 30 planted one-line breaks in the port failed no test (CATALOGUE.md). Rows were added on 28 October. How many of the 11 are caught today was not re-measured: unverified.
- In the packaged game, talk is decided by the C# Core in a helper program, the town's hours by the port (FINDINGS.md line 9). So the game itself runs two of the three copies.
- Measured today with seven newly planted breaks (section 3): two of them fail no row of the table. One is the hourly closing of the week's end (TownWeek.h, HourEnd). The other is the order of the two nine o'clock steps, which the table records by name only. The table's blind spots are the same for the port in the game and for the browser copy. (run 2) The breaks script now asks every row of the whole table of each broken copy itself, so this no longer rests on logs kept by hand: for both breaks, 0 of 102,949 rows differ.

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
| Can the cloud build and test it? | No. NuGet is refused. Needs a GitHub build machine for every change. | Yes. With the tools downloaded once, everything builds and all tests pass in about three minutes (148 s in run 1, 183 s in run 2 from a fresh machine). | Yes |
| Main risk | Size, start-up time, and the prototype running rules the game's port does not have yet | Only the ported rules are there. A new rule must be written in C# and then in C++ before the prototype shows it. | A hand copy drifts. The table checks single rules, not the order of a day. |

### (a) The C# Core compiled for the browser

- What stops it here. The browser runtime (Microsoft.NETCore.App.Runtime.Mono.browser-wasm) is published only on NuGet. Today the cloud's network gate answered 403 for api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com and dotnetcli.azureedge.net. That is the same refusal as on 17 November. It is a network rule, not a fault in the method. No way round it was tried.
- What did work today. The .NET SDK itself can be had in the cloud from conda-forge (8.0.428, with 10.0.404 and 11.0.100 also there). That is how the Core, its table and its tests were run here. On 17 November the SDK came from Ubuntu's archive. Today that archive answered only over https (its lists were read at 13:54 UTC). It carries the SDK (8.0.134 and 10.0.115) and no browser runtime for .NET.
- Looked for the browser runtime elsewhere: npm (searched today, nothing), conda-forge (its whole index searched today, nothing) and Ubuntu's archive (package names searched today, nothing). PyPI was not searched. So it stays a GitHub build machine job, as the study of 17 November said.
- Size. Not measured. A smallest .NET browser app is 6.8 MB, or 2.0 MB with Brotli. With "invariant globalisation" it is 4.3 MB, or 1.4 MB with Brotli (Andrew Lock, 12 August 2025, .NET 10 preview 6, re-read today). Our Core adds about 1.1 MB before trimming (measured 17 November). Hence "about 2 to 4 MB".
- Speed. Not measured. Microsoft: "Because the .NET IL code is interpreted, apps typically run slower than they would on a server-side .NET JIT runtime." The faster kind of build makes most apps "about twice the size" and needs Emscripten, and Python on Linux (Microsoft Learn, read today).
- Versions. The browser runtime pack is at 11.0.0 and 10.0.15, both dated 10 November 2026, MIT (nuget.org page, read today through the search tool, not from this machine). The Core targets .NET 8.

### (b) The game's C++ port compiled for the browser

- Tool. wasi-sdk 34.0, which is the clang compiler (LLVM 23.1.0) with a C and C++ library for WebAssembly. One file from GitHub's release downloads, which the cloud can reach. Version 34 was found by trying the release addresses: 34 answers, 35 and 36 do not. Its release date was not read. (run 2) Trying addresses is guessing, which the web rule does not allow, and it was not done again. The project's own page, found through a search, names wasi-sdk 34 in its notes. Two searches did not find the release's own page, so its release date stays unverified. The files inside the download are dated 24 August 2026.
- Emscripten, the usual tool for this, was not needed and not tried. Its own download site (storage.googleapis.com) is refused by the cloud. Its latest release is 7.0.0 of 6 November 2026 (its changelog, read today). conda-forge carries an older 4.0.9 and Ubuntu's archive a much older 3.1.6.
- Flags. The game's own: no C++ exceptions, with the same switch the Unreal module sets (LEDGER_CORE_NO_EXCEPTIONS). Four rows (FactNull) need exceptions and are skipped by name, exactly as in the Unreal build. Built a second time with exceptions on, those four are answered too and agree.
- One snag, one line. The port names a constant inside a class (AdasTea::Ada in FirstWeek.h) in a way the C++14 standard needs a second line for. g++ lets it pass. This compiler does not. Built as C++17 it is fine. The Unreal project sets no standard of its own (searched), so the game takes Unreal 5.8's default, which was not looked up today. Nothing was changed in ue-probe. It is a small finding for the port's owner: this machine's own clang, given the command tools/port-golden-check.sh uses when g++ is missing, fails to link the port test for the same reason.
- What the module asks of the outside world: four small system calls (print, close, seek, and the clock). The loader answers the clock with zero. The port's own source never reads the computer's clock or random numbers (searched today). The same calls therefore always give the same town. (run 2) With the save routines added it asks seven: the three new ones are the computer's list of settings, in two calls (answered: none), and "stop" (answered with an error; no test reached it).

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
| T4: same calls twice | The same town to the last character | Same digest both times. Inside one engine this is almost certain by design: the loader answers the clock and the random numbers with zero, so two runs have nothing to differ by. |
| T4x (run 2): Node against the browser | The real test of "the same town": the digest Node worked out against the digest the page in Chromium worked out, compared by the script inside `one-sim.sh all`, which fails if they differ. In run 1 this was read by hand. | Digest 37e81244f129619f in both, over the same table (102,960 rows). The comparison has its own self-test (5 of 5). |
| T7: the Ledger's facts through the front door | Who knows what and how (saw it or was told, from whom, how well the first witness saw him), read back after every scripted hour | At all 225 hours the number of facts is the hour's own count, which T3 holds to the C# Core. Nobody but the witness is said to have seen the window go. The witness holds it first-hand and recognised at all 130 hours after the deed. This checks the module against itself and against two plain rules. The details of each fact are not yet compared with the C# Core; no golden rows exist for them. |
| T6: rough handling | Calls before a town exists, broken cast files, times that are no time, answers outside the list, odd text, a thirty-day jump, a second town | Nothing fell over. The thirty-day jump took about 0.16 s. |
| The same checks inside a real web page | It works in a browser, not only in Node | Chromium 157.0.8103.78, headless: all passed |
| Selftest: four rows spoiled on purpose | The checks can fail | Each spoiled row was caught by its own check, 7 of 7 |
| Planted breaks: seven one-line changes to a copy of the port (a step an hour late, a step dropped, two steps swapped, routines an hour out) | Whether anything notices a changed rule: the whole table (T1) and the front door's checks (T2, T3). (run 2) The script builds both browser builds from each broken copy and runs every check on them. | 5 of 7 fail rows of the whole table, the same 5 fail the front door's checks, 2 are seen by nothing. Rows of the table that differ, break by break: 44, 9, 12, 145, 0, 0 and 2,812 of 102,949. The two zeros are the week's end never closed, and DS Ellis's step run before the witnesses' reports. |

The front door after run 1 (wasm/one_sim.cpp, 25 calls, four of them plumbing, no rule of its own): make a town from a cast file, run one game hour in the game's own order (TownWeek::RunHour), the player's acts between hours (the deed, his answer to the ask, the tea, the week's end, a police report, being taken in), and reading back: where someone is, the week's state as the game's save writes it, and who knows what and how. That last one is what a Ledger screen would be drawn from.

(run 2) Ten calls were added for the prototype's bridge, 35 in all: a sighting that is no damage, "held until", and the save and the load, which hand out and take back the same texts the packaged game writes into its save folder. The save routines made the simulation file larger: 423,015 bytes, 142,080 with gzip, 108,526 with Brotli. The bridge and its tests are in tools/lane/one-sim/BRIDGE.md; where the prototype's own town differs from these rules is in DIFFERENCES.md. One finding from the bridge belongs here, because it is about the reference: the golden table's scripted weeks run an hour's steps before the talk of the hour before, and the packaged game runs that talk first. Played the game's way, the same six weeks differ from the table's rows in the count of stories at 96 of 225 hours, and at one hour in who finds the damage; who goes to the police, DS Ellis's first visit and the first arrest are the same.

## 4. Licences against the allowlist (ledger-v2/research/license-allowlist.md, read today and again in run 2)

Where the list stands (run 3, read on the lane's branch after wip was merged into it): both lines are on the list. Item 17 carries the tools line, "Tools, never shipped: wasi-sdk 34 with clang (Apache 2.0); the .NET SDK (MIT) for the Core's checks in the cloud", with his yes of 19 November, 16:18. Item 18 carries the shipped pieces, "The browser prototype only: the pieces of the LLVM project's C++ library and helper routines and of wasi-libc that the compiler builds into the simulation file (Apache 2.0 with the LLVM exception, Apache 2.0, MIT; with portions under BSD-2-Clause, BSD-3-Clause, CC0 and the University of Illinois/NCSA licence), notices kept", with his yes of 19 November, 17:29. In run 2 the second line was held, because the full licence texts named licences this study had not; item 18 is the fuller line that came of it. "Notices kept" is a condition of item 18: the credits file below must exist before anything with the simulation file inside is published. Item 13 covers three.js, esbuild, acorn and puppeteer-core for the prototype. PROCESS 2 asks for a decision record for any new tool: none exists yet for wasi-sdk or for the .NET SDK from conda-forge (DECISIONS.md is not the lane's to write; handed to the main session in PROGRESS.md).

### What ships inside the prototype page

| Part | Licence | How it was checked |
|---|---|---|
| The town rules themselves, compiled (87% of the simulation file's code and data) | Ours | |
| The loader one-sim.mjs and the bridge one-sim-bridge.mjs | Ours | Written in this lane. No library inside. |
| The cast file (production/specs/hook-cast.json), handed to the simulation as text | Ours | The project's own data. |
| Pieces of the C++ library, libc++ and libc++abi (the LLVM project): 10 of their objects, 3% of the file, plus header code the compiler builds into our own part | Apache 2.0 with the LLVM exception | Read in run 1 in the shipped files themselves: the licence line appears 3,378 times in the headers that came with the compiler. |
| Pieces of the C library, wasi-libc: 69 of its objects, 10% of the file | Apache 2.0 with the LLVM exception, Apache 2.0 and MIT for the library as a whole. Portions come from older works under their own licences: dlmalloc (CC0), emmalloc (MIT), cloudlibc (BSD 2-clause), musl (MIT), musl-fts (BSD 3-clause). | (run 2) Full text read: production/licences/one-sim/wasi-libc-LICENSE and wasi-libc-LICENSE-MIT, fetched by the main session from the exact version wasi-sdk 34 was built from (2e6fb9d8ee0c). |
| The compiler's small helper routines (compiler-rt, the LLVM project) | Apache 2.0 with the LLVM exception. Older code in it is under the "legacy" licence too: the University of Illinois/NCSA licence or MIT, at the user's choice. | (run 2) Full text read: production/licences/one-sim/compiler-rt-LICENSE.TXT, fetched by the main session from the LLVM project's main branch, not from the exact version the compiler was built from (895aa2c896ad). Measured in run 2: none of these routines is inside the simulation file today (next paragraph). |

What is really inside, measured in run 2. The simulation file was linked once more with the same command and a link map switched on, which lists every library object the linker took. Measured twice: before the bridge's save routines were added (57 objects from wasi-libc) and after, which is the file as it stands. The result as it stands: 4 objects from libc++, 6 from libc++abi, 69 from wasi-libc, and none from compiler-rt. Among the 69 are the memory allocator (dlmalloc, the CC0 part) and musl's printing, number reading, text, language-setting and maths routines (the MIT part). There is no object from musl-fts (the BSD 3-clause part) and none from emmalloc. Which of the 69 come from cloudlibc (the BSD 2-clause part) cannot be told from their names, and the library's source was not fetched to check: unverified, so BSD 2-clause is counted as inside. A later change to the rules could pull in other pieces, the helper routines included, so the line for his list names every licence the two texts name.

What the full texts add to this study, in plain words:

- Three licences this study did not name for wasi-libc: CC0, BSD 2-clause and BSD 3-clause, for the portions listed above.
- One it did not name for the helper routines: the University of Illinois/NCSA licence (with MIT as its alternative), for older code. Run 1 had the helper routines' licence down as unread.
- All of them are free licences that let their code be shipped inside a product, paid or free, changed or not. CC0 asks for nothing. MIT, BSD 2-clause, BSD 3-clause and NCSA ask that their copyright notice and licence text travel with what is shipped. BSD 3-clause and NCSA also say their authors' names must not be used to promote the product. The LLVM exception lifts the notice duty for pieces of the LLVM code that the compiler builds into a program. This is a reading of the texts, not legal advice.
- So "notices kept" has a concrete meaning: a credits file beside the page with those notices in it. The wasi-libc text points to four more files for the wording of the portions' own notices (the notice in dlmalloc's malloc.c, cloudlibc's LICENSE, musl's COPYRIGHT, musl-fts's COPYING). Those four were not read in this run: unverified, and needed for the credits file before anything ships. The folder also holds only two of wasi-libc's four licence files: the two Apache texts are named in its README as read, but are not stored there.

### Tools, never shipped

| Tool | Licence | How it was checked |
|---|---|---|
| wasi-sdk 34 (with clang and LLVM 23.1.0) | Apache 2.0 | Its source page, read in run 1 and again in run 2 (found through a search). The download carries no licence file (searched in both runs). On the allowlist: item 17. |
| .NET SDK 8.0.428 and runtime 8.0.34, to run the Core's checks in the cloud | MIT, "Copyright (c) .NET Foundation and Contributors" | Read in run 1 from the licence file shipped in the package. The project already uses the .NET SDK on the PC and the build machine. On the allowlist: item 17. |
| conda-forge's packaging of it | BSD 3-clause (the recipe) | Read in run 1 in the package. |
| Node 22 (tests) | MIT | Read on 17 November by the earlier study. |
| The Python zstandard module, 0.25.0 (unpacks the conda packages) | BSD 3-clause, "Copyright (c) 2016, Gregory Szorc" | (run 2) Read in full in the licence file inside the exact file installed, which is now pinned by version and checksum (reference/zstd-requirements.txt). The compression library compiled inside it (zstd) has its own licence, which the file does not carry: not read, unverified. |
| Playwright for Python, 1.63.0 (the page test) | Apache 2.0 | (run 2) Stated by the installed package itself (its licence field, and its licence file, which opens "Apache License"; the whole text was not read through). It carries Node and other parts with their own notices, not read. Not on the allowlist by name: item 13 names puppeteer-core. (run 3) Run 2 wrote here that the prototype's tests already use it. That was wrong: the prototype's own tests use puppeteer-core (its package.json), and no file of the prototype names Playwright. Only this lane's page test uses Playwright. |
| Chromium 157 (the browser Playwright starts) | Not read: unverified | |

If way (a) is ever built, it adds the .NET browser runtime (MIT) and the parts inside it, as the study of 17 November listed.

## 5. The pick, and why

Way (b): the game's own C++ town code, compiled for the browser.

1. It is proved, today, in a browser. The other two are not.
2. It is the game's code. Read today: the game's own CrimeProbe.cpp (line 7821) runs each game hour through TownWeek RunHour, the same call the front door makes. After this, prototype and packaged game run the same files. With (a) the prototype would run the reference while the game went on running the port, and the two could still differ wherever the port does. (run 2) One difference in how the call is made: the game hands RunHour its own hooks (CrimeProbe.cpp lines 7777 to 7821), and the front door hands it none. The hooks are the game's words on screen, its session file and its log. One of them (ConstableHour, lines 7710 to 7720) also notes that the player is held and until when. That belongs to the game, not the town, so the prototype's bridge keeps it itself, from the "held" answer each hour returns (tools/lane/one-sim/BRIDGE.md).
3. It is 80 KB against an estimated 2 to 4 MB, and it starts at once.
4. The cloud can build and test it alone in under three minutes. Way (a) needs a GitHub build machine for every change.
5. It fits his decision of 17 November as written: "the C# Core in the browser if it works, else the same goldens". This is the same goldens, and not through a new copy.
6. It closes no door. The front door is text in, text out. A C# build could sit behind the same calls later and be held to the same tests.

What it does not give:

- Rules that live only in C# (money, debts, jobs, fights, talk). In the prototype these stay in its JavaScript for now. That part of H20 stays open until they are ported or (a) is built.
- A new town rule reaches the prototype only after it is in the Core with golden rows and in the port. That is already the rule for the game. It makes trying a rule in the prototype slower than editing JavaScript.
- Where the port is wrong and the table does not see it, the prototype is wrong the same way. So is the game.

## 6. For his list

The choice (scope), as it was put, recommendation marked. He chose A on 19 November.

- A (recommended, chosen): the prototype runs the game's own town code compiled for the browser, as built today. Nothing more to buy or install.
- B: as A, and also build the C# Core for the browser on a GitHub build machine (15 to 27 hours of cloud work by the estimate of 17 November) and compare the two. Worth it only if the prototype is to run C#-only rules before they are ported.
- C: wait for B before changing the prototype.

The two licence lines, and where each stands (run 2):

- The tools: "Tools, never shipped: wasi-sdk 34 with clang (Apache 2.0); the .NET SDK from conda-forge (MIT) for the Core's checks in the cloud." Done: his yes of 19 November, 16:18, item 17 of the allowlist.
- The shipped pieces. In plain words first: small standard pieces of the compiler's own libraries end up inside the simulation file (80 KB when this was first written, 109 KB with the bridge's save routines). Their free licences allow shipping them, with a credits file beside the page. The exact line, as the main session reworded it after reading the full texts (production/licences/one-sim/README.md): "The browser prototype only: the pieces of the LLVM project's C++ library and helper routines and of wasi-libc that the compiler builds into the simulation file (Apache 2.0 with the LLVM exception, Apache 2.0, MIT; with portions under BSD-2-Clause, BSD-3-Clause, CC0 and the University of Illinois/NCSA licence), notices kept." (run 3) Done: his yes of 19 November, 17:29, item 18 of the allowlist. In run 2 this line was still open and nothing with the simulation file inside could be published. One thing is still to do before publishing: the credits file itself, which needs the four notice files section 4 names. Until it exists, "notices kept" is not met.

## Sources (all read 19 November 2026)

- In the project: canon.md (OPEN 1); DECISIONS.md line 339; tools/port-golden-check.sh; ledger/PerceptionGolden/PerceptionGolden.csproj; ue-probe/tests/core-port-test.cpp and unreal-shim/CoreMinimal.h; ue-probe/Source/LedgerProbe/LedgerProbe.Build.cs; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp (line 7821); CATALOGUE.md line 30; FINDINGS.md line 9; production/audits/full-2026-11/AUDIT-REPORT.md (H20); production/research/lane/SIM-IN-BROWSER-2026-11-17.md; production/lane/K2-SIM-PORT-FAULTS-2026-11-18.md; ledger-v2/research/license-allowlist.md. Added in run 2: production/licences/one-sim/ (its README and the three licence texts, each read in full); production/lane/REVIEW-ONE-SIM-STEP1-2.md; ledger/Assets/Scripts/Core/Suspicion.cs (lines 122 and 176) and ledger/CoreTests/Program.cs (line 1625).
- Measured here: the logs of tools/lane/one-sim/one-sim.sh all. Run 1: last run 14:05 UTC, 148 s, everything passed. Run 2: first full run 16:26 to 16:29 UTC on a fresh machine, 183 s, exit 0, "one-sim: everything passed"; the planted breaks 16:29 to 16:38, 9 minutes 14 s; with the bridge and its checks, 16:46 to 16:50 UTC, 215 s, exit 0, and the planted breaks again after it, 10 minutes 31 s, the same counts; last full run 17:07 to 17:10 UTC, 196 s, exit 0, "one-sim: everything passed". Node 22.23.5, Chromium 157.0.8103.78, g++ 13.3.0.

Web pages, each with how it was reached. Run 1 recorded this for one page only. In run 2 every page below was found again by a web search at the address given, so each is reachable by the rule. Only the wasi-sdk page was read again in run 2; the quotes from the others are run 1's.

- https://github.com/webassembly/wasi-sdk (licence box: Apache 2.0). Run 1: how it was reached is not recorded. Run 2: a search result, read again.
- https://github.com/webassembly/wasi-libc (licence files listed). Run 1: not recorded. Run 2: a search result, not read again; the licence texts themselves are now in the project.
- https://www.nuget.org/packages/Microsoft.NETCore.App.Runtime.Mono.browser-wasm (versions, dates, MIT, 24.18 MB). Run 1: through the search tool. Run 2: a search result.
- Microsoft Learn, "ASP.NET Core Blazor WebAssembly build tools and ahead-of-time (AOT) compilation", .NET 11 version, footer "Last updated on 2026-07-22": https://learn.microsoft.com/en-us/aspnet/core/blazor/webassembly-build-tools-and-aot. Run 1: not recorded. Run 2: a search result.
- Andrew Lock, "Running .NET in the browser without Blazor", 12 August 2025: https://andrewlock.net/running-dotnet-in-the-browser-without-blazor. Run 1: not recorded. Run 2: a search result.
- Emscripten ChangeLog (Chromium mirror): https://chromium.googlesource.com/external/github.com/kripken/emscripten/+show/HEAD/ChangeLog.md ("7.0.0 - 11/06/26"). Only the first part of the page was read. Run 1: not recorded. Run 2: a search result.
- MacPorts' page for wasi-sdk (run 2, a search result, read): it lists version 33 with the licence "Apache-2 and NCSA". A second-hand page, used only as a pointer; it gave no date for version 34.

Downloads of tools, which are not web pages read for facts. Each comes from a fixed address written in one-sim.sh and is checked against a checksum before use:

- conda-forge (conda.anaconda.org/conda-forge/linux-64): dotnet-runtime 8.0.34 and dotnet-sdk 8.0.428. Run 1 also downloaded and searched its package index (linux-64 and noarch): dotnet-sdk 8.0.428, 10.0.404, 11.0.100; emscripten 4.0.9; no .NET browser runtime. The .NET licence file was read inside the runtime package.
- GitHub's release downloads: wasi-sdk 34.0 (its VERSION file: LLVM 23.1.0, wasi-libc 2e6fb9d8ee0c). Run 1 found the address by trying version numbers, which was guessing. The address is now fixed in the script with its checksum.
- PyPI, through pip: zstandard 0.25.0, pinned by checksum since run 2.
- Ubuntu 24.04's package lists (archive.ubuntu.com over https, noble and noble-updates, main and universe), read in run 1: dotnet-sdk-8.0 8.0.134, dotnet-sdk-10.0 10.0.115, emscripten 3.1.6; no .NET browser runtime.
- Fetched by the main session on the PC, not by the lane: the licence texts in production/licences/one-sim/ (their README gives the addresses).

Whether the lane's rules allow downloading tools from such fixed addresses is the main session's to confirm. It is recorded in the lane's log for that.

Unreached, and therefore not evidence: api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com, dotnetcli.azureedge.net and packages.microsoft.com (.NET's parts; run 1); storage.googleapis.com (Emscripten's downloads; run 1); Ubuntu's archive over plain http (over https it answers); api.github.com (so wasi-sdk's release list and date; run 1); a mirror copy of wasi-libc's LICENSE that run 1 fetched from an address no search had given (it came back unreadable, and is no source). Run 2 did not try the Microsoft hosts again: the .NET SDK came from conda-forge, as in run 1. Run 2's search for wasi-sdk's releases led to a list that showed only the releases of 2019, so the release page of version 34 counts as unreached.

Unverified, said again in one place: the size and speed of way (a) in a browser; the four notice files wasi-libc's licence points to (dlmalloc, cloudlibc, musl, musl-fts) and wasi-libc's two Apache texts as stored copies; which of the 69 wasi-libc objects come from its BSD 2-clause part; whether the helper routines' licence text on LLVM's main branch is word for word the one of the version the compiler was built from; the licences of Chromium and of the zstd library inside zstandard; Unreal 5.8's default C++ standard; wasi-sdk 34's release date (its files are dated 24 August 2026); how many of the audit's 11 unseen planted breaks are caught today; speed for a town of hundreds (41 people measured); any browser but Chromium (Firefox and Safari's engine were not on this machine); the rest of CoreTests under a computer set to a decimal comma.

Not done, by the project's own rules: the fixes of run 2 have not had a second review, and no fresh helper has yet tried to break the build.
