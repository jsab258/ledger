# Review: one simulation in the browser, steps 1 and 2 (19 November 2026)

Fresh reviewer, about 20 minutes. Read: the study (production/research/lane/ONE-SIM-METHOD-2026-11-19.md), tools/lane/one-sim (README, PROGRESS, one-sim.sh, every file in wasm/ and reference/), the cited lines in canon.md, DECISIONS.md, CATALOGUE.md, FINDINGS.md, CrimeProbe.cpp, TownWeek.h, CoreGolden.h, the three original project files under ledger/, and the licence allowlist. Ran `one-sim.sh test` (nice 10): exit 0 in 13 s, every number the study gives for T1 to T7 came out the same (16.4 ms a game day this time, inside the 13 to 18 ms range it gives).

## Verdict: PASS WITH FIXES

The pick is justified by the sources. The C# Core is the reference (canon.md line 199, OPEN 1; DECISIONS.md line 339; the PerceptionGolden project note, all quoted correctly). The game runs its hour through TownWeek RunHour (CrimeProbe.cpp line 7821). The front door holds no rule of its own. Its expected answers all come from the table the C# Core writes. No check compares a file with itself. Skips are by name, counted, and must add up (checks.mjs lines 61 to 70). The self-test shows T1, T2 and T3 can fail. No licence is claimed as allowed. The study says plainly that none of the new parts is on the allowlist. Nothing under ledger/ or ue-probe/ was changed: git status is clean, the lane's commit touches only its own two folders, and no build output was left in the repository, ignored files included. No other game's material was fetched. There are no em-dashes.

The fixes below are about claims that run a little ahead of what the committed tests prove, plus three gaps in records. None of them changes the pick.

## Findings, worst first

1. **"Same digest in Node and in Chromium" is not checked by any test.** checks.mjs lines 204 to 207 only compare two runs inside the same engine. Inside one engine they can hardly differ, because the loader always answers the clock and random numbers with zero (one-sim.mjs lines 48 and 49). Nothing compares the Node report with the browser report. The claim was read by hand. Today both reports do hold 37e81244f129619f (checked in the work folder's test-report.json and browser-report.json), so the claim is true, but no test holds it. Claimed at study line 100 and PROGRESS line 33.
   Fix: in one-sim.sh `all` (line 221), after `browser`, read `T4.first` from $W/logs/test-report.json and from $W/logs/browser-report.json and fail (rc=1) if they differ, printing both. Also say in the study that T4 within one engine is almost certain by design, and that the cross-engine comparison is the real test.

2. **"The other two fail no row of the whole table either" is not what breaks.py measures.** breaks.py line 79 runs `test_one_sim.mjs --bridge-only`, which skips T1 (the whole table). The whole-table result comes from separate runs whose logs (break5-full.log, break6-full.log) sit in the work folder, which does not last. Claimed at study line 105 and PROGRESS lines 48 and 49.
   Fix: in breaks.py, also build the check build from the broken copy (add `-DONE_SIM_CHECK=1`, as one-sim.sh line 158 does). Then run test_one_sim.mjs with `--check` instead of `--bridge-only`, and print each break's T1 mismatch count beside its T2 and T3 counts.

3. **The reference builds use the lane's own copies of the project files, not the originals, with one setting that changes behaviour.** tools/lane/one-sim/reference/Directory.Build.props line 15 adds `InvariantGlobalization=true`, which none of ledger/PerceptionGolden, CoreTests or Soak .csproj sets. Line 16 adds `NoWarn`, and the .csproj files add a `Remove` of obj/. The include lists do match the originals (checked). For the golden table this made no difference, because it came out byte for byte the same. But CoreTests run under invariant globalisation could hide a fault that depends on the computer's language settings, which the PC's own run would show. So study line 38 ("no edit") and line 34 ("nothing copied") say a little more than is true.
   Fix: in study section 1 and README "What is here", add one line: "The three check programs are built from lane-written project files that list the same sources as the originals, with invariant globalisation added (reason: …)". Give the real reason, for example the cloud has no ICU library, once that is confirmed. Add a step to `reference` that compares each lane .csproj's source list with the original's and fails if they differ.

4. **`test`, `selftest` and `browser` can run against an old table.** They use $W/golden-fresh.txt from whichever run last did `reference` (one-sim.sh lines 176, 189 and 196), and never check that it still matches the committed table. If someone runs `test` on its own after the table changes, it passes against the old table.
   Fix: add a helper that compares the CR-stripped $TABLE with `cat ue-probe/perception-golden/part-*.txt | tr -d '\r'`, as lines 122 to 126 do. Call it at the top of test_, selftest and browser, and stop with "NOTHING MEASURED: the C# table is older than the committed one; run reference" (exit 3) if they differ.

5. **A wrong fact at study line 32.** It says "Four of its files mention Unity, in comments only". In fact 25 of the 140 files contain "Unity", and some of those are in program text, not comments (for example StreetVignettePieces.cs lines 259, 325, 327 and 721). The point it supports still holds: the only "UnityEngine" in the Core is inside a comment (StreetVignette.cs line 107), and the Core built on plain .NET today.
   Fix: replace it with "No file of the Core uses UnityEngine (one comment names it); 25 files mention Unity in comments or messages. It builds on plain .NET (built today)."

6. **T7 checks the module against itself, not against the C# Core.** It compares the number of facts read back with the module's own count field for that hour, and checks two rules about the witness. The details of each fact (saw or told, hops, from whom, rung, how sure) are never compared with C# rows. None exist yet. Study line 101 is careful about this. PROGRESS line 43 and README line 38 ("the Ledger's facts") could be read as checked.
   Fix: add to study section 3 and PROGRESS: "The details of each fact are not yet compared with the C# Core; no golden rows exist for them." Add to Next: golden rows for who knows what after each scripted hour, written by the C# side. That is the main session's job, because the lane does not touch the Core.

7. **Study line 9 says a little too much.** "matched the C# Core on all 225 hours" means the thirteen summary answers each hour (with the count of stories), not the whole town's state.
   Fix: "matched the C# Core's thirteen answers for each of the 225 hours (who found the damage, who went to the police, … how many stories the town holds)".

8. **The web rule.** Study line 77: the wasi-sdk version was found by trying release addresses (34, 35, 36). Study line 179: a mirror copy of wasi-libc's LICENSE was fetched. Neither address came from a search result. For the other web sources (Microsoft Learn, Andrew Lock, the Emscripten changelog mirror, the two GitHub repository pages), the study does not say how they were reached. Only the nuget.org page is marked "through the search tool".
   Fix: in the Sources list, mark each web page with how it was reached (search result, or direct). Stop guessing addresses. Find the wasi-sdk 34 release page through a search, which also gives its release date (still unverified). Fetching toolchains from pinned package addresses (conda-forge, GitHub releases, PyPI) is downloading tools, not reading web pages. Record in the lane log that this was done, so the main session can confirm the lane's rules allow it.

9. **One download is not pinned.** one-sim.sh line 71 runs `pip install zstandard` with no version and no checksum, while the header (line 30) says the toolchains are "pinned by name and checksum". Today it got 0.25.0. Its licence is listed as unread (study line 131).
   Fix: pin it, for example `pip install --require-hashes -r reference/zstd-requirements.txt`, holding `zstandard==0.25.0 --hash=sha256:<hash of the wheel used>`. Read its licence at the source and fill in study line 131.

10. **Licence records: nothing is claimed as allowed that is not on the allowlist, but there are three gaps.**
    (a) The table of shipped parts (study lines 113 to 120) covers only what is inside one-sim.wasm. Add rows for the loader one-sim.mjs and the cast files, both ours.
    (b) Study line 162 sends the licence line to his list with "yes, after wasi-libc's and the helper routines' licence texts have been read". Read them first. They ship inside the wasi-sdk 34 sources, and wasi-libc includes code taken from older libraries such as musl and dlmalloc. Then his line can be a plain yes or no, with nothing still to check.
    (c) The allowlist's PROCESS 2 (a decision record for each new tool) is named in study line 111, but no DECISIONS.md entry exists for wasi-sdk or for the .NET SDK from conda-forge (searched). Write the record, or hand it to the main session in the lane's handover in one line.

11. **Plain words.** The seven-line answer and the choice in section 6 are plain. The licence line in section 6 (line 162) is written for a lawyer, not for him ("the LLVM project's C++ library and helper routines and of wasi-libc").
    Fix: put one plain sentence in front of it and keep the exact names in the line itself. For example: "Small standard pieces of the compiler's own library end up inside the 80 KB simulation file. Their free licences allow shipping them, with a credit line."

12. **A small gap in reason 2 of section 5** ("the same call the front door makes"). The game passes its own hooks into RunHour (CrimeProbe.cpp lines 7777 to 7821); the front door passes none (one_sim.cpp line 185). The hooks are words on screen, the session file and the log. One of them, ConstableHour (CrimeProbe.cpp lines 7710 to 7720), also records that the player is held (bHeldPending, GHeldUntil). That state belongs to the game, not the town. The prototype must keep it itself, from the "held" answer the hour returns.
    Fix: add one sentence to study section 5 point 2, and note it in PROGRESS Next item 2 (the bridge).

## Checked and found right

- The line references: canon.md OPEN 1 (line 199), DECISIONS.md line 339, CrimeProbe.cpp line 7821, CATALOGUE.md line 30 (11 of 30 planted breaks), FINDINGS.md line 9, and the PerceptionGolden note.
- The counts: the Core's 140 files and 50,561 lines; the 27 files with the same names on both sides.
- The game's flags: LedgerProbe.Build.cs line 113 sets LEDGER_CORE_NO_EXCEPTIONS, and no C++ standard is set there.
- The clang path in port-golden-check.sh (lines 134 to 136, C++14, O1).
- Planted break 6: the step names are typed beside the calls (TownWeek.h lines 259 to 263), so swapping the two calls cannot change the TownWeekSteps rows. The finding stands.
- The golden reader's CastFileReader hook already exists in ue-probe (CoreGolden.h line 1300). It was not added by this lane.
- The read-only view the C# programs run in was taken down after use: it is no longer mounted.
