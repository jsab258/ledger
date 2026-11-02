# Review of the packaged-walk skill, 2 November 2026

One fresh reviewer (general-purpose, read only; no scripts, builds, games, clicks or UI Automation) checked .claude/skills/packaged-walk/SKILL.md against its source files: the build machine's workflow, nightly_package.py, build-local.ps1, retention.py and retention.json, play.py, route_walk.py, nightly_walk.py, close_games.py, p1-packaged.ps1, film_webp.py, stage_game_data.py, ci-checks.sh, the night record of 2 Nov, CLAUDE.md and the 21 memory notes plus MEMORY.md.

**Verdict: PASS WITH FIXES.** About 95 claims checked: 9 wrong or unbacked, 1 imprecise, 5 points missing, no setting or story leaks. The builder checked items 1, 2, 3 and 7 against the files before applying them.

## Wrong or unbacked (all applied)

1. Step 5 said the build starts with the editor target. The build step first builds the game target, cold then warm; coldBuildExit is the cold build's exit (workflow, lines 500 to 523). Then the editor target, the material, staging and BuildCookRun.
2. Step 6 and Records put the pictures on F:. The tester's step pictures go to production/playtest/ai-tester/<time>/ (gitignored, .gitignore:145), where nightly_walk.py reads them. The night folder holds route/verdict.json, walk.log, the bench and state.json, and films go to F:/LedgerTools/tmp/ai-tester/film. nightly_walk.py's own docstring ("pictures stay on F:") disagrees with its code.
3. Step 6, "a switch on the night's walk": there is no such switch. run_walk passes only `--town --out`. Now reads "a change to nightly_walk.py's route call; check first".
4. Step 8 gave 600 s to every editor run. The first run after a street re-import needs over 25 minutes (editor-photographs-need-the-street). It now gets its own longer limit.
5. Step 2 said play.py checks for Runner.Worker. Only `start --editor` does (play.py line 498). The packaged start waits only for the build machine's own game or Unreal processes (runner_busy).
6. Step 4: the `if:` reads `github.event.head_commit.message`, so only the push's last commit counts. A [package] commit with another pushed on top of it builds nothing.
7. Always, rule 2: retention.py never reads retention.json's `floors`. The 40 and 20 GB come from the command's own defaults (`--need-c 40 --need-f 20`, line 762), and build-local.ps1 checks C: only.
8. Step 7: the talk is the stand-in unless `start --real-talk` (packaged only, with a budget cap; the game reads its own key). The tester itself never reads or passes a key.
9. The checks in steps 5, 6 and 9:
   - LEDGER-STABLE-COPY.txt can still read COPIED after a locked copy, because OLD-COPY-LOCKED goes only to the run's summary. Read the sha on its first line instead.
   - The night report records no build commit, and a later build may replace the copy after the walk. Comparing the copy's time with the walk's start is marked "check first".

## Imprecise (applied)

10. Step 8 presented p1-packaged.ps1 as a general packaged-measuring tool. It is a fixed frame-and-memory profile: three 1800-frame captures at 3440x1440 with the voice speaking, written to runs.jsonl. Its `-Only` and `-Voice none` are now named.

## Missing (all added)

- Runner.Worker vanishes for a moment between two queued runs, so for heavy GPU work check twice, a minute apart (editor-blocks-runner-build).
- nightly_walk.py waits 90 minutes and then walks anyway. If the build is still running, the walk plays the old copy, and the build's stable-copy step closes games running from that copy, ending the walk mid-run.
- A run stopped by the space check commits nothing, so ue-build.txt stays the previous run's. The stable-copy step is continue-on-error, so a green run does not prove the played copy was replaced.
- film-marks.json exists only after a route walk that filmed named stretches (`--sit`, or the `--camera` switch, which is missing from route_walk.py's usage line). A free-play film uses film_webp's `FILM_DIR FIRST LAST OUT.webp` form.
- The sources disagree on whether a separate "LEDGER nightly package" task exists: the workflow's comment names one, but nightly_walk.py calls nightly_package.py itself and the 29 Oct reading listed three tasks. Marked "check first". nightly_package.py works from origin/wip, so local commits must be pushed first.

## Backed

Always rules 1 and 3 to 6; steps 1 and 3 in full; step 4 apart from item 6, including the full list of watched paths, the concurrency rule and nightly_package's output lines; step 2's space log, night times and the docstring contradiction, close_games, the launcher's child, the editor's 40 s exit and the card holders; step 5's wait, stable copy, commit, colour reads and runner restart; step 7's play.py and route_walk commands, the never-tail rule and the close without /T; step 8's switches, scalability 2, MSYS and the fixed step; step 9; the references to the gate skill (step 8) and the garment skill (step 9).
