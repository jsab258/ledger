# 255. Thirty-one launchers and three tools still name the old folder, the dead branch, or the archive

STATUS: READY, 2026-09-10, after queue 257. Ruled out of the move batch by
`game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-behind.md`
section 5, findings 2, 3, 4 and the second half of 5.

## What is wrong

The move batch repointed six root launchers, three workflows, the installer
and the daemons. Everything else Jafar can double-click still carries
`set "REPO=%USERPROFILE%\wc26-picks"` or the dead branch: the grep this was
filed from found the string in about 31 files under `tools/`, chiefly
`tools/voice-live/*.bat`, `tools/voice-gen/*.bat`, `tools/mixamo-pick/*.bat`,
`tools/meshgen/1 MAKE THE PROPS.bat`, `tools/imagegen/1 MAKE THE PICTURES.bat`,
`tools/runner/1 SET UP THE BUILD RUNNER.bat` to `5 PUT BUILDS ON YOUR SCREEN.bat`
and `tools/runner/PLAY THE STREET.bat`. Three tools too: `tools/d1-cycles.py`
line 269 reads CI runs from `repos/jsab258/wc26-picks/actions`, an instrument
that answers with the wrong world's numbers; `tools/runner/run-night.ps1` line
41 checks out from the dead branch; `tools/producer-check.py` lines 356 and
1486 allow a research link into the archive tree.

## Why this is not a blind replace

Some of these are destructive when clicked, and the batch's own discipline
applies to each: `tools/voice-live/8 START THE WATCHER.bat` lines 87 to 92
fetch `origin %BRANCH%` and hard-reset to it, so it needs the remote repair
or the URL pin before the reset, exactly like `START THE STUDIO MACHINE.bat`;
`tools/mixamo-pick/SETUP.bat` line 106 clones the archive outright;
`GO.bat` line 62 tells him to; the meshgen and imagegen launchers pull the
dead branch. `1 SET UP THE BUILD RUNNER.bat` line 102 is the first row of the
table: the runner is registered correctly today, and the next person to
follow that file would register it to the archive and blind the studio
silently.

## The deliverable

A per-file table in the landing record: file, line, what it does when
clicked (path only, pull, fetch and reset, clone, register), old text, new
text, and for every destructive row which of the two guards it got. Then the
edits. `d1-cycles.py` additionally prints the repository it reads on its
first output line, so the world the numbers are of is on the page.

## Done looks like

`grep -rn 'wc26-picks' tools/ *.bat *.ps1` and the same for the dead branch
both at 0 over the files scanned, with the denominators printed; the verify
lint from queue 254 widened to `tools/` and the root launchers once this
lands (never before, or it is red on day one for a reason nobody can act on);
and `python3 tools/d1-cycles.py --selftest` green.

## Dependencies and risk

After queue 257: until the fleet moves, nothing on his disk runs the
committed launchers at all, so landing this earlier changes nothing he can
click and risks a merge under a checkout that is about to be reset. Risk: a
row mislabelled as path-only that actually resets; the table is the guard.
