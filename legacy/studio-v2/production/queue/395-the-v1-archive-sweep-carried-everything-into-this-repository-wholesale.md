line: docs (v1 and legacy audit; production/repo-move-plan.md's follow-on)
spec: Jafar, 2026-09-21 ("THE CLEANUPS"): "The archive sweep of 10
  September ran before the move, so everything it put in legacy/ was
  carried into this repository wholesale. The old repository still holds
  every commit, so anything here purely as history does not need to be
  here. Go through legacy/ and the v1 remnants and rule, for each, whether
  it is live, referenced by something live, or only history: the Unity
  character bodies and game scripts D16 retired, the fifteen probe
  projects, game-design/ with its seventy decision files, the
  voice-selection folders, the two thousand generated clips, and
  game-design/PLAYTEST-RUNBOOK.md, marked LIVE and verified 15 August, a
  Unity-on-macOS build guide superseded by production/playtest/RUNBOOK.md.
  What is only history is removed from main and the removal names the
  commit in wc26-picks where it still lives. What stays, stays with a
  reason. The C# Core stays; it is the source of truth the port is
  checked against."

  Verify each of his six named categories by grep or glob rather than by
  his count alone before ruling on it: his own counts, fifteen probe
  projects and seventy decision files, are his estimate and this item's
  job is to check them, the way every other reading in this project is
  checked before it is stated. game-design/PLAYTEST-RUNBOOK.md
  specifically: confirm its STATUS line still reads LIVE and compare it
  against production/playtest/RUNBOOK.md, the 19-line, 342-word document
  Jafar dictated 2026-09-19 per production/NOW.md, before ruling it
  superseded.

  wc26-picks is the archive branch named in CLAUDE.md: "Branch: main of
  jsab258/ledger; wc26-picks is the archive, never pushed." Naming a
  commit there means citing a real commit hash reachable on that branch,
  checked rather than assumed, for every file this item removes.
acceptance: every item in his six named categories is ruled LIVE,
  REFERENCED-BY-LIVE (naming what references it), or ONLY-HISTORY, with
  the rule stated for each rather than left implicit; every ONLY-HISTORY
  item is removed from main in a commit whose message names the
  wc26-picks commit hash where it still exists, that hash checked to
  actually resolve on wc26-picks before it is cited; every item ruled to
  stay carries its reason in the same commit; ledger/CoreTests and the
  rest of the C# Core are confirmed untouched, a diff or file-count check,
  printed; and game-design/PLAYTEST-RUNBOOK.md's STATUS line is either
  corrected from LIVE to superseded-by-production/playtest/RUNBOOK.md, or,
  if it is found to still carry information the new file does not, that
  difference is named before either file is touched
max_sessions: 3
status: READY 2026-09-21, filed as studio-third work, taken at a
  checkpoint. Not gated on the visual slice or the measurements.
  DESTRUCTIVE: this item deletes files from main. Per CLAUDE.md rule 5,
  look at what is there first and scope the removal to exactly what is
  ruled only-history; run `git status` and ensure nothing uncommitted is
  lost before any deletion. This is this week's work.
