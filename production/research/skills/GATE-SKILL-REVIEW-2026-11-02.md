# Review of the gate skill, 2 November 2026

**Verdict: PASS WITH FIXES.** The shape matches the garment skill (nine checked steps, Always block, records). Its content follows the sources, except below.

## Fixes

1. Step 9 predates the 2 Nov ruling (RULINGS 2 Nov; CLAUDE.md "His page"). Replace its first bullet: "His page is one permanent page, 'LEDGER: Needs you' (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8), never a daily page. A frame or person is one item in production/approvals/needs-you/items.json (one line, a link to each full-size 2560x1440 picture, recommendation, shortfalls first); run tools/needs_you_page.py --check, rebuild, republish to the same link; --close ID "how" once answered. Read its verdicts before asking." Drop "dated the day made".
2. Step 5 asks the reviewer for a verdict. BRIEF-3: "No overall pass or fail: the maker reads the three lists"; REPORT.md: it failed all 58 pictures. Replace with: "one file: changes (each fault or not), newFaults (block), knownShortfalls (each narrow or not); no overall verdict; the view fails only if newFaults is not empty."
3. Step 5 omits the model and two brief lines. RULINGS 25 Oct: "Opus for ... every final review"; BRIEF-3: "Not the maker's verdict". Add: "Opus; no maker's verdict; if a tool needs clicks, stop and report."
4. Clothes are judged on the floor, not the Hook sheet (RULINGS 3 Oct). Add to step 5: "For clothes the reviewer gets RUBRIC.md, not the Hook sheet, and answers each line pass or fail with its frame."
5. Folders differ from practice (gate-chandler, gate-grocer). Use "F:/LedgerTools/gate/last-good/<piece>/<view>.png" and "gate/new/<piece>-<date>/r1, r2".
6. Step 6 stores editor pictures as last good, but the game passes only packaged (memory photograph-at-the-played-level). Add: "After step 8 the packaged copy's picture replaces the editor's."
7. Step 2's machine rule is thin (memory editor-blocks-runner-build; Task Scheduler 01:30, 03:30, 04:15). Replace: "No local Unreal or Build.bat while Runner.Worker builds or plays, nor from 15 minutes before 01:30 and 04:15." Name tools/shop_views.py and street_views.py.
8. Two-tries line lacks its outcome (CLAUDE.md). Add: "Without his yes the fault is set aside, named in the summary and listed in FINDINGS.md; the ask goes in Needs you."
9. Records omit homes. Add: "Gate record in production/audits/gate-<piece>/GATE.md; preview JPEG (about 1600 px, under 500 KB) in production/previews/; pictures stay on F:."
10. Step 8 lacks the route (memory package-request-needs-watched-path). Add: "Request the package with tools/nightly_package.py; the session runs the tester, never a helper."
11. The Hook sheet's home is production/reference/hook-sheet.png (CATALOGUE.md); the preview is a copy. The sheet mirrors the hook frame (LUMEN-COAT-REFLECTIONS-REVIEW, aside). Replace "where its view is the mirror" with "for the hook views".
12. Add to step 9: "Anything touching taste or identity (a map, a face, a voice, the look) reaches him on one page before merging" (CLAUDE.md).
13. Minor: "My own look" should read "The builder's own look".

## Named files or switches that do not exist

- tools/pool_clip.py: it is production/audits/night-2026-10-08/pool_clip.py.
- -ExecCmds is Unreal's own switch, not in ue-probe/Source.

Every other named file and switch exists.
