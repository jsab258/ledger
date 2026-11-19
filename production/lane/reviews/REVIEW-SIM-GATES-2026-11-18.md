# Review: tools/lane/sim_gates.py (fresh reviewer, 18 Nov 2026)

Verdict: PASS WITH FIXES

## Checked

- Tests: 7 of 7 pass.
- Live run, fresh work folder: all five PASS in 50 s. CoreTests 5,255; Soak 9; SaveChaos 149; PerceptionGolden identical to the goldens; StrangerTest 108/108. Repository unchanged: same git status before and after (ignored files included, -uall), and no repository file newer than the run's start.
- Every write in the gates' C#: CoreTests writes only to the temp folder, except `--write-vignette-pieces`, which writes production/specs/ through a link but is never passed. PerceptionGolden writes into its copied working folder. StrangerTest --sweep writes production/stranger-test/ under RepoRoot, which is the work folder (found by the linked CLAUDE.md), and that folder is a copy. No project builds into a linked folder.
- Pass judgement: the exit code comes first, then a marker. Every gate returns non-zero on failure. No false PASS found.

## Fixes

1. Reusing a --work folder gates stale code. prepare() skips copying folders that already exist, so the sources are never refreshed after a code change, and the run could print PASS for the old code. Fix: re-copy the sources and projects on every run, or refuse a work folder that is not empty.
2. An old work folder where production/stranger-test is a link keeps that link. Fix: check that every WRITTEN entry is a real folder, and stop if not.
3. The repository check is weaker than the note claims. `git status --porcelain` misses writes to ignored paths, further changes to a file already modified, and new files inside an untracked folder that already exists. Fix: add `--ignored --untracked-files=all` and compare hashes of modified files.
4. A timeout, a crash or a missing golden output raises an exception: a traceback, no FAIL line, and the repository check skipped. Catch the error and report it as FAIL.
5. StrangerTest: require paths=N/N, not just the word "strangerSweep".
6. Minor: `goldens_match` passes when there are no part files and the output is empty. Require at least one part.

Latent risk: adding --write-vignette-pieces to GATES would write into the repository through the production/specs link.
