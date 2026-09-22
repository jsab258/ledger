# FINDINGS

One line each, dated, newest last.

- 2026-09-22 The golden table the C++ port is checked against was seven rows behind the C# Core; the missing rows are the caught-claim ones, and they were left out precisely because the port cannot answer them, so the comparison passed by never being asked. Fixed: the table is regenerated from the Core and the hole is named and counted.
- 2026-09-22 Four of the five suites D16 named as "these keep running" — Soak, SaveChaos, PerceptionGolden, StrangerTest — were in no push check. Their project directories survived the whole time, which is exactly what made the loss invisible.
- 2026-09-22 The Unreal safeguard could not turn a run red: the build step was marked continue-on-error and the last step banked evidence and exited clean, so a failed build reported green.
- 2026-09-22 The two golden comparisons are not equally strict. The g++ one fails on a row it cannot answer; the in-engine one counts it, prints a note and still says PASS. Left as it is for now, written down so the next reader is not surprised by a green engine and a red runner.
- 2026-09-22 The scheduled task "LEDGER supervisor" was still running on this PC, driving the other checkout, which pushes to the same repository.
- 2026-09-22 The commit-message hook in .githooks/ is not wired up (no hooks path set), so it has never refused anything. Left as found; noted so it is not mistaken for a live gate.
- 2026-09-22 The Blender preview workflow the lamp recipe derives its own invocation from is gone (archived with the studio), so one of the recipe selftest checks has been failing on a dead path; a second, the bad-args refusal check, fails too. Both predate this sitting. Recipe passes 71 of 73.
- 2026-09-22 A full cold build, cook and package of the Unreal project takes 4.3 minutes on this PC, and a warm one 1 to 2. That number had never existed; the workflow allows sixty minutes for it.
- 2026-09-22 The independent check earned its place on its first use: given the act gate and the intended behaviour in plain words, an outside reader found that a press left over from an abandoned attempt would be credited to the NEXT crime, that the evidence called the deed committed before it had happened, that keyRouted meant only "a controller exists", that the ceiling constant could be set to zero with every test still green, and that the real gate lived in a file no test compiles. All fixed before the commit.
- 2026-09-22 The crime verdict's witnessStatusNote is a hardcoded string. It printed "w1-filed-on-A-with-a-rung" on a run where nothing was witnessed at all. Not fixed today; named here because it is a sentence the evidence file asserts rather than measures.
- 2026-09-22 Nothing automated reads the crime verdict. A run in which the input path was dead commits and pushes green; only a human reading the file catches it. That gate belongs with the witnessed/control regression pair, which is the next sitting's work.
