line: instruments (a guard whose accepting fixture is a snapshot, not the tree)
spec: FOUND 2026-09-21 by the resident, diagnosing why the setts contact sheet
  never appeared. `tools/citypack/fetch_textures.py --selftest` had pinned
  three constants for `kerb.jpg` as its accepting case. Established by blob
  hash rather than inference: commit 07ea030d (2026-09-15T22:57:59Z) wrote the
  constants while kerb.jpg was blob 8bff82f4; commit ad02021a, TWENTY MINUTES
  LATER, replaced it with blob 3eea4439, which is still HEAD's. choices.json
  records that swap on purpose (`kerb Concrete034 -> Rock048`). The kerb was a
  flat card, queue 300 found it, the shortlist route existed to replace it,
  and replacing it broke the guard that route depends on.

  instruments.md already forbids this, by its exact final clause: "the live
  codebase is the accepting fixture ... SO THAT DOING THE WORK THE TOOL
  PROMPTS CAN NEVER BREAK THE TOOL." A pinned snapshot of the live codebase is
  not the live codebase. The rule was written; the shape was not recognised
  when it recurred one file away.

  THE COST WAS NOT SIX DAYS OF RED. It was silence. This workflow has three
  runs ever: run 1 (35033500220) passed pre-swap, run 2 (35033510147) was
  cancelled, run 3 (35629210889, today) is the FIRST since the swap and it
  failed at step 5 before one candidate was downloaded. A guard nothing asks
  is a guard nobody knows is broken, so the six days are a measure of how
  rarely it ran, not of how long anyone ignored it.

  AND THE COMMIT GATE NEVER SAW IT, which is the other half of why it went
  six days unseen. `grep -n 'citypack\|fetch_textures\|pack_check'
  ledger/verify.py` returns NOTHING: this selftest is in none of verify.py's
  84 checks. It is exercised by one CI workflow and by nothing a person runs
  before committing, so a green local verify has never said anything about
  it either way. A guard reachable from one rarely-pushed workflow is a
  guard with one chance a week to tell you it is broken.

  THE QUESTION THIS ITEM ASKS, AND IT IS NOT ANSWERED HERE: how many other
  guards in this repository assert a constant that was read off the tree
  rather than derived from it? The class is specific and greppable, not a
  vibe: a literal float or int in a test or gate whose value came from
  measuring a file that the project's own pipelines are expected to replace.
  `verify.py`'s footer says `guard-tester` has NEVER been selected in the
  whole agent log (3 of 15 definitions never selected, it names them), and
  guard-tester is the role written for precisely this sweep.

  NOT DONE IN THE SESSION THAT FOUND IT, under CLAUDE.md rule 11: an audit
  finding is filed and the standing order resumes. The one instance blocking
  the week's slice was fixed on the spot because it WAS the blocker; the class
  is this item.
acceptance: a written inventory of every guard whose accepting case compares
  against a pinned constant, with, per guard, whether the value is derived at
  run time or copied; whether the artifact it reads is one a pipeline in this
  repo can replace; and, for each one that can be replaced, either a
  conversion to a self-deriving check or a named reason it must stay pinned.
  A zero ships its denominator: how many guards were examined, not just how
  many were faulty. At least one planted fault per converted guard, proving it
  still goes red, and the accepting case run first.
status: READY 2026-09-21. Instrument work under D45, so no review gate; the
  natural owner is guard-tester, which has never run. Blocked on nothing.
