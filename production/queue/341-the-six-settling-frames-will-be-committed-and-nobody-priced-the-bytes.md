line: CI (.github/workflows/ledger-probe-unreal.yml, the staged leaf list)
spec: Commit 00bf7189 changed the staging step to derive its leaf list from the
  spec's own shot ids, which is what finally landed the four pinset_night
  frames. The consequence nobody priced: EVERY shot id is now committed as
  ue-<id>.png whatever it is called, so queue 334's six settling frames will be
  committed too, at roughly 7 to 10 MB per run, on a run that happens often.
  The 06:35Z ruling priced those rows as "one probe-free capture each" and did
  not price them as committed bytes.
acceptance: a decision, recorded: either the settling frames are committed and
  the cost is named, or the leaf list gains an opt-out that a row can set and
  the staging line prints how many rows took it
max_sessions: 1
status: READY 2026-09-16, found by the 334 builder while correcting a sentence
  the same commit had falsified.

  THE FALSIFIED SENTENCE, which is the other half of this and is already
  corrected in the scene spec: pin_setter_night's note claimed its ids
  "deliberately do NOT carry the vign_ prefix, so the workflow's ue-vign_*.png
  staging does not commit them". That was true when it was written and 00bf7189
  made it false on 2026-09-16 at 02:40Z. The fix that landed the missing frames
  is the same change that makes this item necessary.

  THE NUMBER IS THE BUILDER'S AND IS NOT RE-MEASURED HERE: roughly 7 to 10 MB
  per run for six frames, from the sizes of the existing night PNGs. Before
  anyone decides, weigh it against what the repository already carries per run
  and say which, because a megabyte figure with no denominator is the fault
  this project keeps finding in its own reasoning.

  UNDER D45 a tool that measures the game: a test, no review.
