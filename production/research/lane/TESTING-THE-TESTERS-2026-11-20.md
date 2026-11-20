# Testing the testers: method (4t piece 8)

Written by the cloud lane, 20 Nov 2026, for his plan of 19 Nov (point 8: "each week plant faults on purpose and record how many the testers catch; record the panel's verdicts beside his own words when he plays, and fix the panel when they keep disagreeing"). The wider research is AI-PLAYTESTING-METHODS-2026-11-20.md (same folder); this file adds only what piece 8 needs.

## Questions

1. Is planting faults on purpose a fair test of a set of testers?
2. Which faults should be planted?
3. How do we tell whether an AI judge (the panel) agrees with a person well enough?

## Sources (read 20 Nov 2026)

| Source | What it says | What we take |
|---|---|---|
| Just, Jalali, Inozemtseva, Ernst, Holmes, Fraser, "Are mutants a valid substitute for real faults in software testing?", FSE 2014 (Nov 2014), abstract page https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html | On 357 real faults in 5 open-source programs (321,000 lines), "a statistically significant correlation between mutant detection and real fault detection, independently of code coverage"; also "some inherent limitations". | Planting faults is a fair measure of a test set, with limits. Only the abstract was read; the paper's coupling share is not quoted here (unverified). |
| Thomas, Biagiola et al., muPRL, ICSE 2025; lab blog 27 Apr 2025 https://lab-design.github.io/news/2025/04/27/uprl-mutation-testing-reinforcement-learning/ (read for AI-PLAYTESTING-METHODS) | Faults drawn from real bug histories, planted to see whether tests catch them (as the lab's blog summarises the paper; the paper itself was not read). | Our planted faults sit where our testing or he met real faults (his complaints, the round fixes); each change itself is made up. |
| "Judge's Verdict", NVIDIA, arXiv 2510.09738v1, 10 Oct 2025 https://arxiv.org/html/2510.09738v1 (first part read in full: method and measures) | Correlation alone is not enough; agreement is measured with Cohen's kappa, which corrects for chance. A judge is "human-like" when its kappa with people sits within one spread of the people's kappa with each other (human-human kappa 0.80 there). Needs many rated samples (1,994 there). | We have one person and few plays, so a kappa means nothing at first: shown only from ten plays with a verdict. Until then a plain rule: two disagreements in the last three plays mean "fix the panel". |

## Method as built

1. Faults (tools/lane/gate/plant/faults.json): each one a small change to a copy of the game's source, named with where it comes from (his complaints of 18 Nov, the round 6 fixes, the content rule, the consequence rule, save and reload, ER-CAM-01). The game's own folder is never changed: the source is copied outside the repository, one fault applied, built there.
2. Each fault names the machine testers that should catch it, the narrow run that is enough, and the checks it aims at. The same narrow run is made twice on the clean build first; anything that differs between the two clean runs is noise and never counts. A fault counts as caught only by a new failure in a check it aims at. When such a check could not be made ("not reached"), the tester broke, or a feel number was already outside its band on the clean build, the fault counts as not tested, never as missed or caught.
3. A fault whose text the game no longer has is reported "not planted: renew the fault", so the list cannot rot silently (a test checks every fault applies to the current source).
4. The AI testers (player types, breakers, the panel) cost a model, so they are tested in a loop, once a week: the loop serves them one planted build each from the run's folders and adds their catches with --ai.
5. The panel beside him: production/lane/PANEL-VS-JAFAR.json, one entry each time he plays a judged build, from his own words (never asked of him); tools/lane/gate/plant/panel_vs_him.py flags "fix the panel" on two disagreements in three, or on the panel naming fewer than half of his problems in two of three.

## Limits

- Seven faults are few; each week's run should add one from that week's real finds and drop none that still apply.
- A planted fault is one clean change; real faults are often several small ones together, and the abstract above notes mutants' limits.
- Word overlap decides whether the panel "named" one of his problems; a loop reads the lines by eye when the flag comes up.
