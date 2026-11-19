# The simulation's five gates run in the cloud lane

Lane, 18 Nov 2026, 10:24 to 10:35 Swiss time. Measured, not estimated.

## What was found

- CLAUDE.md asks for CoreTests, Soak, SaveChaos, PerceptionGolden and StrangerTest before any simulation commit. All five build and pass here, on Linux with the .NET 8 SDK, without Unity, the graphics card or his PC, on branch lane-2026-11 with wip merged:
  - CoreTests: all 5,255 checks passed, about 12 s.
  - Soak: all 9 checks passed, about 1 s.
  - SaveChaos: all 149 checks passed, about 2 s.
  - PerceptionGolden: 102,960 rows, byte for byte identical to the committed goldens (ue-probe/perception-golden/, parts joined in order), about 5 s.
  - StrangerTest --sweep: 108 of 108 paths, 6 seeds, finished.
- BalanceLab (the ending matrix) runs too: production/research/lane/BALANCELAB-RUN-2026-11-18.txt.
- So simulation work that today waits for the PC (the town task's code, a golden-row change, the K2 police-file fix when its phase comes) can be written and gated here first; the PC then only repeats the gates and does the Unreal port check.

## How (tools/lane/sim_gates.py, tests in test_sim_gates.py, 10 pass; fresh review PASS WITH FIXES, 6 applied: production/lane/reviews/REVIEW-SIM-GATES-2026-11-18.md)

- One command: `python3 tools/lane/sim_gates.py --repo <repository> --work <scratch folder>`; exit 0 when all five pass.
- Needs `apt-get install dotnet-sdk-8.0` (8.0.134 used). NuGet sources are cleared per project: the projects use no packages, and the cloud proxy refuses nuget.org (403).
- Nothing is built inside the repository: the projects and the C# sources are copied to the work folder, the rest is linked by name so the tests' file lookups (they walk up from the binary) find their inputs.
- Found while writing it: StrangerTest --sweep rewrites production/stranger-test/study-sweep.txt and appends to study.txt. Through a plain link that reached the repository once in this run; both files were restored with git checkout at once, nothing was committed. The tool now copies that folder instead of linking it, refuses a used work folder (it would gate stale copies), reports a crash or timeout as FAIL, and fails if the repository changes during the run (git status with ignored and all untracked files, plus a hash of every listed file). Never add CoreTests' --write-vignette-pieces mode to it: that writes production/specs/ through a link.

## For the main session

- Nothing to merge into the game. If the town task should use the lane for simulation work, say so in the next order; the tool lives in tools/lane/.
- The PerceptionGolden run here matching the committed goldens is a second, independent machine agreeing with them (same code, different operating system).
