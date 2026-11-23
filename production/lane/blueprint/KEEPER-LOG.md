# Blueprint keeper log

Every keeper run reads this first, then folds in what has landed since the last run's "Next run" list.

## Run 1, Monday 23 November 2026, from 13:18 (claude-opus-5-5)

- Start row 2026-11-23-1318-blueprint on his page.
- Read canon.md and RULINGS.md on wip; worked on lane-2026-11 (fetched at 6923fd0f).
- Built v1: BLUEPRINT.md (index, the game in one page, binding rules, how to read, chapter counts, story pointer, questions for him) and BLUEPRINT-01 to -11 (ten groups by the parts tree, then conflicts and gaps). 424 parts: 111 measured (36 on reference or real-world figures), 133 decided, 42 pending, 45 unmeasured, 14 out, 57 outside, 22 machinery; 401 coverage rows plus 1.6.15 hold-ups. 194 conflicts settled or corrected, 303 gaps, 20 questions for him.
- Method: scratch scripts (prep, assemble, index) map every coverage row to its parts-tree part; five Sonnet helpers wrote each entry's "how it works" from the sources with conflicts, gaps and his questions.
- Landed during the run and folded in: design proof run 5 (design pass 4, 401 rows). Seen, nothing to fold yet: production/lane/checkers/LOG.md (checkers proving themselves on planted faults), production/lane/premortem/GUARDS.md.
- Fresh Opus review: 41 points, fixed once (see the changelog). Left as gaps for the design proof: hold-ups' coverage row, the revolver at rung 2 against guns late, B2's custody wording, coverage.json's stale standard lines.
- Not landed yet, so not folded in: production/lane/blueprint/ prep files (tech plan, numbers run, inventory, sound plan), production/research/lane/aaa-studies/, PRIOR-RESEARCH-INDEX.md, the PC measuring sheets (23 to 28 Nov), the story v3 pick.

Next run starts here:
0. Rebuild method if needed: the scratch scripts are gone; edit the chapter files directly, one changelog line per change.
1. Fold in whichever of the not-landed sources above now exist; each change one line in BLUEPRINT-CHANGELOG.md; update BLUEPRINT-STATUS.json.
2. When the PC measuring reports: move pending and unmeasured entries to measured where a reference figure lands; close the matching gaps in BLUEPRINT-11.
3. When story v3 is picked: name it in BLUEPRINT.md's story section and point chapter 03 at its bible.
4. When he answers a question (his page or advisor rows): replace the recommendation, drop the question.
5. When a design proof run lands (design pass, fit check rerun, red teams 3 and 4): fold its changed rows in.
Prior research index of 23 Nov: fold PRIOR-RESEARCH-INDEX.md into the blueprint; every part's standard names prior research where it exists.
