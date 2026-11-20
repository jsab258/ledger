# Testing the testers (4t piece 8)

His plan of 19 Nov, point 8: each week plant faults on purpose and record how many the testers catch; record the
panel's verdicts beside his own words when he plays, and fix the panel when they keep disagreeing. Method and
sources: production/research/lane/TESTING-THE-TESTERS-2026-11-20.md.

- faults.json: the planted faults, each from a fault our testing or he met before, with the machine testers that
  should catch it and the narrow run that is enough.
- plant.py: copies the game's source outside the repository (never the game's own folder), plants one fault,
  builds, runs each named tester on the clean and the planted build, and writes TESTER-CATCH.md (copy it to
  production/lane/TESTER-CATCH-<date>.md). About 20 minutes for all, no model. Each planted build stays in
  OUT/<fault>/dist, for a loop to serve the AI testers once a week; their catches are added with --ai FILE.
- panel_vs_him.py: the panel's verdicts beside his words (production/lane/PANEL-VS-JAFAR.json); says "fix the
  panel" on two disagreements in the last three plays.
- test_plant.py: checks with no browser; one of them fails when the game's source moved and a fault no longer
  applies (renew it then).

Run weekly (Mondays, beside the loop) and add one fault from that week's real finds.

    python -m pytest -q test_plant.py
    python plant.py [--only id1,id2] [--out DIR] [--report FILE] [--ai FILE]
    python panel_vs_him.py [--out MD]
