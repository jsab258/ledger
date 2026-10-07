# The reviewer test (7 October 2026)

Does the gate's AI reviewer catch the kinds of fault that have reached him? Start with **REPORT.md**, the one page.

- METHOD.md: how it was done, and what it cannot tell.
- BRIEF-AS-USED.md: the gate's brief as every reviewer got it, and each change from the original with its reason.
- KEY.md and key.json: which frame is which, the planted faults and where they are.
- SCORING.md: the scoring rules, written before any review ran.
- SCORES.md: every frame's result in each run, the clean pictures and the false alarms.
- CHECK-RESCORE.md and CHECK-FALSE-ALARMS.md: the two independent checks, word for word.
- reviews/: all fifty-eight reviews, word for word.
- plant_faults.py: remakes the test's pictures from the committed previews (the pictures themselves stay out of git).
