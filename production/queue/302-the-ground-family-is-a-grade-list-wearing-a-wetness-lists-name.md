line: engine (SurfaceBind.h, the shared spec, tools/surface-tint-check.py)
spec: IsGroundSurface copies AssetLibrary.WetSurfaces character for
  character, and that list was written for rain ("Ground the rain
  lands on. Walls and roofs are deliberately absent", AssetLibrary.cs
  908 to 911) and borrowed for brightness by BaseColour; its author
  named the borrowing a contamination and named the fix (516 to 526:
  split the ground family out of WetSurfaces, do not move the
  number). In the vignette the 150 concrete pieces are 72 sills and
  lintels, 6 stall fronts, 4 parapet and coping, 2 roofdecks, 1 kiosk
  plinth, 5 chimney pots and 60 chewing-gum discs; none is a wall
  face and 61 sit on the pavement. Concrete is ONE logical surface
  covering gum on the ground and lintels on a wall, so a grade keyed
  on the surface name cannot be right for both; the split is by role
  or edge, which the pieces file carries per piece. Unity is the
  legacy reference build (D16) and no run of it will land, so the
  grade's list and its two constants move out of the legacy C# table
  into the shared spec both readers read (a per-surface block beside
  surface_tiling, A4 every field written out), the Unreal reader
  reads them from there, and tools/surface-tint-check.py is extended
  INSIDE THE EXISTING TOOL to refuse a disagreement between the
  spec's list and constants and any reader's literal, accepting case
  first on the live tree. Splitting the family does not move 0.55 or
  0.74/0.76/0.80: the values are judged numbers and the judge is
  Jafar under D23.
acceptance: first, the landed frame from 299 looked at with the
  sills, lintels, stall fronts and gum in mind, and one sentence
  written here: do the trim pieces read too dark. If not, the split
  waits and the spec move is still owed. If so, both suites green on
  the split, surface-tint-check.py shown refusing a planted
  disagreement and accepting the live tree, and a run in which the
  concrete line prints the grade the split gave it. A director's
  item, Core question, because it touches the spec contract both
  engines read.
max_sessions: 2
status: READY 2026-09-15, filed by the ruling of 00:52Z
  (decision-2026-09-15-ruling-the-grade-lands-as-the-legacy-number-
  and-the-outbox-brief-was-never-a-net.md). BLOCKED on 299's frame
  being looked at; the block is spent by the landing read of that
  run and by nothing else.
