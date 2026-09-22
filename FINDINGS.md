# FINDINGS

One line each, dated, newest last.

- 2026-09-22 The golden table the C++ port is checked against was seven rows behind the C# Core; the missing rows are the caught-claim ones, and they were left out precisely because the port cannot answer them, so the comparison passed by never being asked. Fixed: the table is regenerated from the Core and the hole is named and counted.
- 2026-09-22 Four of the five suites D16 named as "these keep running" — Soak, SaveChaos, PerceptionGolden, StrangerTest — were in no push check. Their project directories survived the whole time, which is exactly what made the loss invisible.
- 2026-09-22 The Unreal safeguard could not turn a run red: the build step was marked continue-on-error and the last step banked evidence and exited clean, so a failed build reported green.
- 2026-09-22 The two golden comparisons are not equally strict. The g++ one fails on a row it cannot answer; the in-engine one counts it, prints a note and still says PASS. Left as it is for now, written down so the next reader is not surprised by a green engine and a red runner.
- 2026-09-22 The scheduled task "LEDGER supervisor" was still running on this PC, driving the other checkout, which pushes to the same repository.
- 2026-09-22 The commit-message hook in .githooks/ is not wired up (no hooks path set), so it has never refused anything. Left as found; noted so it is not mistaken for a live gate.
- 2026-09-22 The Blender preview workflow the lamp recipe derives its own invocation from is gone (archived with the studio), so one of the recipe selftest checks has been failing on a dead path; a second, the bad-args refusal check, fails too. Both predate this sitting. Recipe passes 71 of 73.
