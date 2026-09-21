line: instruments (the UE side has no key manifest and the Unity side does)
spec: FOUND 2026-09-21 BY THE RESIDENT RUNNING A TOOL ON A FALSE PREMISE, and
  the premise is the useful half.

  THE RESIDENT'S ERROR, recorded first. A wake armed at 15:50Z instructed
  "after run 56 lands, run verdict-keys --learn", on the assumption that it
  would baseline run 56's new keys. IT CANNOT. `tools/verdict-keys.py:51` reads
  `VERDICT = game-design/sim-shots/verdict.txt`, which is the SIM verdict from
  the Unity pipeline. Run 55 and 56 are the UE PROBE, whose verdict is
  `production/d1-probe/ue-vignette-verdict.txt`. They are different files from
  different pipelines and the tool has never touched the second one.

  WHAT RUNNING IT ACTUALLY DID, measured rather than assumed: it announced
  "learning from verdict.txt (no run file matches any recent commit)" and
  rebaselined from a verdict whose own first line names commit cb4767e, not run
  56's d3529180. The result was 170 insertions and ZERO deletions, so the
  failure its docstring warns about ("rewriting it from a stale run deletes
  keys") did NOT occur, and the 170 are the ones the verify footer had been
  asking for all day. The change is kept because nothing was lost and the tool
  was explicitly requesting it; it is simply unrelated to run 56.

  THE GAP THAT LEAVES, AND IT IS THE ITEM. The Unity verdict has a key
  manifest, so a key that silently vanishes is caught. THE UE PROBE VERDICT HAS
  NONE. Checked: `verdict-keys.json` is the only manifest in the tree, and the
  four tools that read `ue-vignette-verdict.txt` are
  `tools/dashboard/build-dashboard.py`, `tools/frame-shadow-probe.py`,
  `tools/map.py` and `tools/verdict-shot-files.py`, none of which is a
  registry.

  SO EVERY KEY THIS WEEK'S WORK ADDED IS UNGUARDED: settleStatus,
  settleSettled, settleCapBit, settleNoFile, settleWorstLastDelta,
  shotSettle*, rigRepeats*, rigRepeatFamily, quadOn, controlQuad*,
  surfacePopulation*, surfacesAccountedFor, surfacesProcedural. If any of them
  stopped printing tomorrow, NOTHING WOULD SAY SO, and the run would read as a
  run that measured those things and found nothing rather than as a run whose
  instrument went quiet. That is the exact failure this project names in its
  own rules, sitting on the side of the tree where all the current work is.

  AND THE ASYMMETRY IS THE POINT: the pipeline D16 RETIRED is the one with the
  guard, and the pipeline every landing since has used is the one without.
acceptance: the UE probe verdict has a key manifest of its own with the same
  two properties the sim one has, a learn step and a missing-key report; the
  first run after it lands prints the count of keys examined AND the count
  missing against the manifest, so a zero carries its denominator; and the
  manifest is built from a run file that NAMES THE COMMIT IT CAME FROM, never
  from whichever verdict happens to be on disk, because that is the mistake
  this item was found by making
max_sessions: 2
status: READY 2026-09-21. Instrument work under D45: a test, no review, no
  ruling record.

  IT SITS IN THE STUDIO'S THIRD and behind his evening ruling of 2026-09-21,
  which put the assembled facade, the exposure fix and the figure first. Filed
  now because the gap was found now, not because it is next.
