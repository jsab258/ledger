# Review of 4t piece 8 (testing the testers), 20 Nov 2026

Fresh reviewer: one Opus helper at high effort, read only, given the files and the goal, not the builder's view.
Verdict: PASS WITH FIXES (3 must, 5 should, 5 minor). All must and should fixed once, minors fixed except where noted.

Must
1. Unmade checks in clumsy.py are marked failed with "not reached" in their note, not their steps, so a planted run could count as caught when nothing was measured. Fixed: steps, note and place are all read; such a check makes the fault not tested.
2. Any unmade check anywhere turned a real miss into "not tested". Fixed: each fault names the checks it aims at (watch); only those count, both for catches and for "not tested".
3. One clean run against one planted run cannot tell a catch from run-to-run noise (the camera check waits on real time). Fixed: two clean runs; any line differing between them never counts.

Should
4. The camera fault was given to scenarios that aim the camera into the wall, so it would likely be missed through no fault of the tester. Fixed: it goes to the machine checks' long run (the camera at every named place).
5. No lock on the work folder. Fixed: the run holds the prototype build's work lock.
6. The panel's word match was far too loose. Fixed: common words and the game's everywhere-words left out, all telling words (two of three or more) must match; tests use the reviewer's three examples.
7. "Fix the panel" is noisy with few plays. Kept as the rule (one person, few plays), and the report now says a flag is a prompt to look, not proof.
8. A tester running past 30 minutes stopped the whole run. Fixed: counted as the tester broke, so not tested.

Minor
- An empty build error message, an AI row's evidence given as text, and the total counting faults never tested: fixed.
- --out and --report inside the repository: now refused.
- The faults' "from" lines name areas of past faults; the changes are made up. Said so in faults.json and the research note; muPRL is quoted only as its lab's blog states it.
