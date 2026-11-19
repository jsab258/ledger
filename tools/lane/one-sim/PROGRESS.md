# one-sim: progress (task 4s, "one simulation in the browser")

Run 1, 19 November 2026, 13:19 to 14:12 UTC, in the cloud: the study and the first build (steps 1 and 2). A fresh reviewer checked them the same day (production/lane/REVIEW-ONE-SIM-STEP1-2.md: pass with fixes, 12 findings).

Run 2, 19 November 2026, 16:18 to about 17:10 UTC, in a fresh cloud machine: the 12 fixes, the bridge (step 3a) and the list of differences (step 3b). Everything was rebuilt from nothing. Run 2's work has not had a fresh reviewer yet.

## Where it stands, in five lines

1. The game's own C++ town code runs in a real browser and gives the C# Core's answers: all 102,949 comparable golden rows, 8,568 routine hours, and 225 hours of six scripted weeks. Node and Chromium end with the same town, now compared by the script.
2. The review's 12 fixes are in, each once. Nothing they touched changed a result.
3. The bridge for the prototype is written and tested (BRIDGE.md, wasm/one-sim-bridge.mjs): the prototype hands over its clock, gets back what each hour did, and carries the town in its save. Driven by a clock in odd steps it gives the C# Core's rows at 225 of 225 hours, and a town saved in mid-week plays on the same in 6 of 6 weeks.
4. The differences between the prototype's own town and the real rules are listed with what each changes for the player, three of them measured (DIFFERENCES.md). The prototype's source is untouched: the swap is step 4.
5. Nothing may be published yet. The licence line for the library pieces inside the simulation file is held, so the allowlist does not carry it, and the swap needs four decisions of his first (DIFFERENCES.md, the end).

## Done, with evidence

One command, last run with the files as committed: `tools/lane/one-sim/one-sim.sh all`, 17:01 to 17:05 UTC, 228 s, exit 0, last line "one-sim: everything passed". It was run three times in run 2: after the fixes (16:26, 183 s, on the machine as it came), after the bridge went in (16:46, 215 s) and at the end, each time exit 0. Logs are in /home/claude/one-sim-work/logs/ (outside the repository, so they do not last: the numbers are copied here).

| Name in the output | What it checks | Result |
|---|---|---|
| source lists (run 2) | The lane's three project files list the same sources as ledger/PerceptionGolden, Soak and CoreTests | the same: 142, 142 and 153 files |
| reference: built | PerceptionGolden, Soak and CoreTests built from the real Core (140 files) by path, .NET SDK 8.0.428 | built, no errors |
| C# goldens | The table the Core writes today against the committed one (ue-probe/perception-golden) | 102,960 rows, 267 rules, identical byte for byte |
| Soak | The Core's own soak check | ok, all 9 checks passed |
| CoreTests | The Core's own tests | "All 5255 checks passed." |
| port-test-as-wasm-game-flags | The port's own golden test (ue-probe/tests/core-port-test.cpp, unchanged) as a WebAssembly program, built with the game's flags | 102,993 checks, 0 failures over 102,949 rows, 0 unanswered, 11 skipped by name (7 claims, 4 FactNull) |
| port-test-as-wasm-with-exceptions | The same with C++ exceptions on | 102,997 checks, 0 failures over 102,953 rows, 7 skipped (claims) |
| T1 golden rows through JavaScript | Every row asked through the loader, no files (data handed in as text) | 102,949 agree, 0 differ, 0 unanswered, 11 skipped by name |
| T1b, T1c | Only the two named holes are skipped; the 3,500 seeded GossipFuzz rows are among those checked | ok |
| T2 routines through the front door | Where each person is each hour, both cast files, against the Core's CastPlaceOf rows | 8,568 of 8,568 |
| T3 the week hour by hour through the front door | Six scripted weeks played by calls from JavaScript, each hour's 13 answers against the Core's TownWeekHour rows | 225 of 225 |
| T4 the same calls twice give the same town | A digest of every hour, the final state and every held story | 37e81244f129619f both times. Inside one engine this is almost certain by design. |
| T4x Node against the browser (run 2) | The real test of the same town: `all` compares Node's digest with Chromium's and fails if they differ | 37e81244f129619f in both, and the bridge's weeks d678e26b179e7b68 in both |
| T5 | Speed and size | 17 to 22 ms a game day over run 2's runs (41 people); one-sim.wasm 423,015 bytes, 142,080 gzip, 108,526 Brotli (run 1, before the save routines: 301,665, 102,362, 79,767); loader 8,938 bytes; bridge 14,155 bytes |
| T6 the front door takes rough handling | Calls before a town exists, broken cast files, times that are no time, answers outside the list, odd and long text, a thirty-day jump, a second town | nothing fell over |
| T7 the Ledger's facts through the front door | Who knows what and how, read back after every scripted hour | the count is the hour's own at all 225 hours; nobody but the witness is said to have seen the window go; the witness holds it first-hand, recognised, at 130 of 130 hours after the deed. The details of each fact are not yet compared with the C# Core; no golden rows exist for them. |
| T8 the bridge, talk by the hour (run 2) | The six weeks again, driven by a clock in steps of 7.3 game minutes through the bridge, with the prototype's own id for Darren | 225 of 225 hours agree with the C# Core's rows; the bridge's "held" agrees at all 225 |
| T9 the bridge, talk by the minute (run 2) | The packaged game's order, with the clock ticked every game minute, every 0.37 and every 7.3 | the same town in all three; 15 to 21 ms a game day |
| T10 a save in the middle (run 2) | Each week saved after two fifths of its hours, as text, loaded into a fresh module, played on | 6 of 6 end as the week played straight through; held in the cells at the save, still held after the load until the same minute; the biggest save 16,826 characters |
| T11 the bridge takes rough handling (run 2) | The prototype's start at 15:36, jumps, a clock going back, acts out of turn, the prototype's own ids, a thirty-day jump, eight saves and casts that must be refused | all as they should be |
| selftest | Four rows spoiled on purpose must be caught, each by its own check; the three small comparers checked too | 9 of 9, 8 of 8, 5 of 5 |
| browser | The same checks inside a real page, headless Chromium 157.0.8103.78 | all passed |
| stale table (run 2, tried by hand) | `test`, `selftest`, `browser`, `breaks` with a table that is not the committed one | each stops with NOTHING MEASURED, exit 3 |
| breaks (run apart: `one-sim.sh breaks`) | Seven one-line breaks planted in a copy of the port; both browser builds made from each, every check run, the whole table included | 5 of 7 fail rows of the whole table (44, 9, 12, 145 and 2,812 of 102,949 rows); the same 5 fail T2 or T3, and the bridge's T8 sees them too; 2 are seen by nothing, the bridge's checks included. See findings 2 and 3. Run twice in run 2, before and after the bridge went in: the same counts. Last run 16:50 to 17:00 UTC, 10 minutes 31 s. |
| differences (run apart: `one-sim.sh differences`) | The prototype's own rule files, unchanged, beside the real town: M1 where nine people are, M2 when people move, M3 how far one story travels | measured in 6 s; the numbers are in DIFFERENCES.md |

The front door (wasm/one_sim.cpp) has 35 calls, four of them plumbing, no rule of its own. Run 2 added ten: a sighting that is no damage, "held until", and four calls each way for the save. The save calls hand out and take back the same texts the packaged game writes into its save folder, made and read by the port's own save routines.

The module now asks seven small things of the page, where run 1's asked four: printing, close, seek, the clock (answered with zero), and since the save was added the computer's list of settings (answered: none, two calls) and "stop" (answered with an error; no test ever reached it).

Run 2, the review's 12 fixes, each once:

1. `all` compares Node's digest with the browser's (T4x above; wasm/engines_agree.py).
2. breaks.py runs the whole table on every broken copy (the breaks row above).
3. The lane's project files against the originals: `reference` compares the two source lists on every run and stops if they differ. Invariant globalisation, which only the lane's files set, is removed: it was not needed here and no result changed. Finding 5 below is what it could have hidden.
4. `test`, `selftest`, `browser` and `breaks` stop when the table in the work folder is no longer the committed one.
5. The study's wrong count of files that mention Unity is corrected (25 of 140, none uses UnityEngine).
6. T7's limit is said where T7 is named (above, the study, the README).
7. The study's answer now says "thirteen answers for each hour", not the whole state.
8. The study's sources say how each web page was reached. No address was guessed in run 2. The tool downloads are recorded in the lane's log for the main session to confirm.
9. zstandard is pinned by version and checksum (reference/zstd-requirements.txt). Its licence was read: BSD 3-clause.
10. Licences: rows for the loader, the bridge and the cast file; the full texts read and what they add written into the study's section 4; the decision record handed to the main session (below).
11. A plain sentence stands in front of the licence line in the study's section 6.
12. The study's section 5 says that the game passes its own hooks into the hour and the front door none, and that "held" is the prototype's to keep. The bridge keeps it (BRIDGE.md).

## For the main session (things the lane may not write)

- DECISIONS.md has no entry for the two new tools (the allowlist's PROCESS 2 asks for one): wasi-sdk 34 with clang, and the .NET SDK 8.0.428 from conda-forge, both tools never shipped, his yes of 19 November 16:18 (allowlist item 17).
- The allowlist's item 17 carries the tools line only, on the lane's branch and on wip alike. The line for the pieces that ship inside the simulation file is held: the allowlist does not carry it. The fuller wording is in production/licences/one-sim/README.md. How it gets onto the allowlist is the main session's to settle; the lane only reports that it is not there, and that the texts, now read in full, say nothing that stops a page from shipping these pieces with a credits file. Measured in run 2 with a link map, on the file as it stands: 69 objects from wasi-libc, 10 from the C++ library, none of the helper routines (compiler-rt) and nothing from the BSD 3-clause part (musl-fts). The study's section 4 has the detail, and what is still to read before a credits file can be written (four notice files).
- Playwright (Apache 2.0 by its own package) runs the page test here and the prototype's tests. The allowlist's item 13 names puppeteer-core, not Playwright.
- RECIPE.md asks for a few lines from every finished unit. The lane may not write it. Offered: "One set of rules in two places: compile the shipped rule code for the second place instead of copying it; hold both to one table written by the reference; test the glue with a clock in odd steps and a save in the middle; plant small breaks to learn what the table does not see. Cost: two cloud runs of about an hour each. Failed: nothing; found two orders of the same hour that the table cannot tell apart. Evidence: tools/lane/one-sim/PROGRESS.md."
- Four decisions for him before the swap, written out at the end of DIFFERENCES.md: the names, what each person thinks of him, the week's length, the solicitor's bill and the chase.

## Findings for whoever owns the port, the table and the Core (not fixed here: nothing under ue-probe/ or ledger/ was touched)

1. FirstWeek.h declares AdasTea::Ada in a way the C++14 standard needs a second line for. g++ accepts it. clang does not link it under C++14 ("undefined reference to LedgerCore::AdasTea::Ada"). Tried in run 1 with this machine's clang++ 18 and the exact command tools/port-golden-check.sh uses when g++ is missing (-std=c++14 -O1): the port test does not link. So that script's clang path is broken; its g++ and MSVC paths are not affected as far as seen here (MSVC not tried). The browser build uses C++17, where it is fine.
2. Planted break, seen by nothing: removing `Week.Close(Now, Mill, Cast);` from TownWeek.h HourEnd fails no golden row (0 of 102,949, measured by breaks.py) and changes nothing in the six scripted weeks, through the front door or through the bridge. The week's end closing each hour is not pinned by any row.
3. Planted break, seen by nothing: swapping the two nine o'clock calls in TownWeek.h RunHour (DS Ellis before the witnesses' reports) fails no golden row (0 of 102,949). The TownWeekSteps rows record the step names, which are typed beside the calls, not the calls. Today the swap probably cannot change any outcome, because only damage is ever reported and she comes for a crime only from wounding up (K2's reading). It will matter with the first serious crime.
4. The golden reader asks for town-news.json through the same hook as the cast files. A host that hands in only the two cast files gets four rows unanswered (TownNewsWitnesses and three KeepsHisDeeds). Not a fault, but easy to trip on.
5. (run 2) The Core writes one number with the computer's own language settings. Suspicion.cs lines 122 and 176 build the lines of the suspicion trail with a plain number format, so on a computer set to a decimal comma they read "-0,05" where the tests expect "-0.05". Measured by running the Core's own checks under four settings: under German (Germany) and Turkish, CoreTests stops at its first failed check, "and a fall still reads as a fall" (CoreTests/Program.cs line 1625), after 237 passed lines, so the rest of its 5,255 checks were not run under those settings; under Swiss German and British, all 5,255 pass. The golden table came out identical to the committed one under all four, and Soak passed under the two it was run with. The port does not carry this trail. On his PC it shows only if Windows is set to a decimal comma.
6. (run 2) The golden table's scripted weeks and the packaged game run an hour in different orders. The table's weeks (ledger/PerceptionGolden/Program.cs, EmitTownWeek) run each hour's steps and then the talk since the hour before. The game runs the talk of the hour before first (CrimeProbe.cpp line 7956) and lets it follow the minutes. Both use the same rules, and the bridge can do both. Measured over the six scripted weeks: 129 of 225 hours come out identical; in the two weeks that hold a deed the count of stories differs at 96 hours from five in the afternoon of the deed's day, and at one hour somebody more finds the damage. Who goes to the police, DS Ellis's first visit and the first arrest are the same in all six. So the order the game really plays is held to the C# Core only through the same code proved in the other order. Golden rows played the game's way would close it.

## Next, in order

1. One fresh reviewer for run 2 (the fixes, the bridge, the differences) against their sources, and a fresh helper to try to break the bridge. Neither was done in this run.
2. His word, through the main session: the licence line for the shipped pieces, and the four decisions at the end of DIFFERENCES.md.
3. What step 4 needs that waits on no decision:
   - a call on the front door for how well a witness sees him (the port's Perception and Sighting), held to its golden rows through JavaScript as T2 holds the routines;
   - the table from the cast file's 30 places to spots on the prototype's map, and from where he stands to the cast file's 24 areas;
   - the words the screens need (Ada's line, the arrest's words).
4. Step 4, the swap, through the publish gate: the prototype's routines, talk, witnessing and police timetable replaced by the bridge's calls; its save version raised; its own tests run again. Those tests need the prototype's packages installed (three, esbuild, puppeteer-core), which this run did not do.
5. For the C# side, so the main session's: golden rows for the week played the game's way (finding 6), and for who knows what after each scripted hour (T7's limit).
6. The credits file for the library pieces, once the four notice files are read (the study, section 4).
7. Firefox and Safari's engine: still not tried. The module asks for nothing beyond plain WebAssembly, which is a reason to expect it to work, not a test.
8. If he ever picks B in the study's section 6: a GitHub build machine job that builds the C# Core for the browser, behind the same front door, held to the same checks.

## Blocked, and why

- Publishing anything with one-sim.wasm inside: the licence line for the shipped pieces is held, and the allowlist is law. It is open until the allowlist carries the line.
- The swap in the prototype (step 4): by the task's own order it is a later round through the publish gate, and it needs the four decisions.
- The C# Core compiled for the browser (way a): the cloud's network refused NuGet and Microsoft's download sites in run 1 (403 at the gate for api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com, dotnetcli.azureedge.net). Run 2 did not try them again: he chose way A, and the .NET SDK for the checks comes from conda-forge. Not a fault of the method.

## Exact commands

From the repository root, Linux, two processors are enough. Heavy steps run at low priority (nice 15) and one compile at a time.

    tools/lane/one-sim/one-sim.sh setup        # once (8 s here). Fetches, with checksums:
                                               #   dotnet-runtime-8.0.34 and dotnet-sdk-8.0.428 from conda-forge (157 MB)
                                               #   wasi-sdk-34.0-x86_64-linux.tar.gz from GitHub releases (192 MB)
                                               #   the zstandard 0.25.0 wheel for Python 3.13 from PyPI (5.5 MB)
    tools/lane/one-sim/one-sim.sh all          # reference, wasm, test, selftest, browser, Node against the browser: about 3.5 minutes
    tools/lane/one-sim/one-sim.sh reference    # the C# Core: source lists, build, golden table, Soak, CoreTests (about 50 s)
    tools/lane/one-sim/one-sim.sh wasm         # the four WebAssembly builds (about 2.5 minutes)
    tools/lane/one-sim/one-sim.sh test         # under Node (18 s)
    tools/lane/one-sim/one-sim.sh selftest
    tools/lane/one-sim/one-sim.sh browser      # needs Python's playwright with Chromium, as the prototype's tests do
    tools/lane/one-sim/one-sim.sh breaks       # the seven planted breaks (about 10 minutes)
    tools/lane/one-sim/one-sim.sh differences  # the prototype's town against the real rules (6 s)

Things to know:

- Everything large is in /home/claude/one-sim-work (set ONE_SIM_WORK to move it): the downloads about 340 MB, the .NET SDK unpacked 555 MB, wasi-sdk unpacked 635 MB, build output. None of it is in git. tools/lane/one-sim holds text only, the largest file under 40 KB.
- `reference` needs the right to mount: the C# check programs look upward from their own folder for the repository's data files, so they run under a folder of links into a read-only view of the repository (a read-only bind mount at $ONE_SIM_WORK/ro-repo). The script takes the view down again after use. Without mount rights it says NOTHING MEASURED and runs nothing against a writable repository.
- `reference` also needs an ICU library on the machine, as .NET on Linux does by default (Ubuntu 24.04 has libicu74).
- Another Python than 3.13 needs its own line in reference/zstd-requirements.txt: pip refuses a file whose checksum is not listed.
- The built one-sim.wasm is at $ONE_SIM_WORK/wasm/one-sim.wasm (one-sim.full.wasm keeps the names for debugging).
- Exit codes: 0 good, 1 a check failed, 2 usage, 3 nothing measured. In `all`, a failed check outranks a check that could not run.
- Versions today: Node 22.23.5, Python 3.13.18, g++ 13.3.0, Chromium 157.0.8103.78 (Playwright 1.63.0), wasi-sdk 34.0 (LLVM 23.1.0), .NET SDK 8.0.428.
