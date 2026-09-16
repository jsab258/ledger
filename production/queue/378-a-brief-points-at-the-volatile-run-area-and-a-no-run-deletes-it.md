line: instruments and reporting, jointly
spec: FOUND BY A GATE GOING RED FOR A CORRECT REASON, 2026-09-16, which is the
  best way to find one.

  `tools/runner/brief.py --selftest` failed its ACCEPTING case
  `accept/live/2026-09-16-names-a-picture-that-is-on-this-disk`. The picture
  was gone. Today's brief, ALREADY SENT TO JAFAR, named
  `production/d1-probe/ue-vign_hook_day.png`, and run 52 deleted it.

  RUN 52 WAS RIGHT TO DELETE IT. Its build published no binary, so it measured
  nothing, and `.claude/rules/ci.md` says a run that measured nothing must not
  carry the previous run's files forward under its own name. The deletion is
  that rule working. THE BUG IS THE REFERENCE, NOT THE DELETION.

  `production/d1-probe/` IS THE VOLATILE PER-RUN AREA and every file in it is
  the current run's to replace or disown. CLAUDE.md rule 12 already names the
  durable one in as many words: "The channel that works here is a file
  committed by CI, under `game-design/sim-shots/`." A brief that points into
  the volatile area has a reference with a half-life of one CI run, and it
  breaks silently, in a document that has already been read.

  FIXED IN PLACE FOR THIS BRIEF, and the fix is the shape the rule should take:
  the still was restored out of 468ba206 into
  `game-design/sim-shots/brief_2026-09-16_hook_day_run51.png`, named for the
  run that actually produced it, and the sidecar repointed there. It was NOT
  restored into `production/d1-probe/`, because putting a run-51 still back
  into run 52's working area is precisely what would make it read as run 52's
  evidence. The selftest reads 58 passed, 0 failed again.
acceptance: a brief cannot name a picture under `production/d1-probe/` at all,
  refused by the gate that already reads briefs, with the accepting case (a
  brief naming a sim-shots copy) proven first; and the copy carries the run
  that produced it in its name
max_sessions: 1
status: READY 2026-09-16, filed and NOT started. The one live brief is
  repaired; this item is the rule that stops the next one.

  WHAT THIS ALSO CONFIRMED, opened rather than inferred: the restored day frame
  shows the sky photograph's HORIZON BAND far more plainly than any night frame
  does, a clear tree line across the vanishing point of Quay Street. That is
  queue 373, and it is now seen in daylight rather than argued from the
  photograph's filename.
