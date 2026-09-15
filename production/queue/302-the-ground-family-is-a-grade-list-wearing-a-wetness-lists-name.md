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

  THE BLOCK IS NOT SPENT, AND THE FIRST ANSWER WRITTEN HERE WAS WITHDRAWN
  BEFORE IT LANDED, 2026-09-15 after run 44 on 17710df.

  WHAT WAS WRITTEN AND IS FALSE: "the sills and lintels have gone from pale
  stone trim to near-black bars, and they no longer read as stone at all". It
  was written from two crops looked at several minutes apart, which is how a
  difference gets constructed rather than found, and it is the exact failure
  CLAUDE.md rule 4 names: looking is strong evidence that something is wrong
  and weak evidence of what, so print the quantity before acting on it.

  WHAT THE QUANTITY SAYS. The 72 C13_sills_lintels pieces were projected
  through cam_hook; 54 land on screen. THEIR MEDIAN PROJECTED HEIGHT IS 5.1
  PIXELS, smallest 2.1, largest 20.0, and that largest one sits at x=26, half
  off the left edge of frame. A 3x3 patch on a piece five pixels tall is
  mostly the wall behind it, so the median before-and-after ratio it produces,
  0.825, is contamination and not a reading: the concrete surface as a whole
  measured 0.591 and every ground surface takes an identical grade, so a
  lintel cannot really have moved by 0.825 while its own surface moved by
  0.591.

  AND THE ONE LINTEL BIG ENOUGH TO LOOK AT REFUSES THE CLAIM. west_south_gf1_
  lintel0 at 7.6 m, 20 pixels tall, cropped at 4x nearest-neighbour so no
  pixel is invented, in both runs: it reads as a DARK BAR IN THE BRICK BEFORE
  THE GRADE AND A SLIGHTLY DARKER ONE AFTER. It was never pale stone trim.

  SO THIS CAMERA CANNOT ANSWER THIS ITEM. The acceptance asks whether the trim
  pieces read too dark, and cam_hook renders them at five pixels. That is not
  a finding about the grade, it is a finding about the instrument, and rule 3
  says to suspect the instrument first.

  WHAT WOULD SPEND THE BLOCK, named so the next session does not repeat this:
  a frame in which a sill or lintel is large enough to read as a material, and
  the near ones are on the west flank at 7 to 9 m. Either a camera placed to
  see one, or the existing cam_B if it shows one larger, or a native-
  resolution crop of a lintel that fills more than a few pixels. Until then
  THE SPLIT IS UNJUSTIFIED BY EVIDENCE, however good the argument from
  AssetLibrary.cs 908 to 911 is, and the argument is not the evidence.

  status: STILL BLOCKED 2026-09-15. The block was described as spent by the
  landing read of run 44; that reading did not survive its own measurement,
  and the block stands.

