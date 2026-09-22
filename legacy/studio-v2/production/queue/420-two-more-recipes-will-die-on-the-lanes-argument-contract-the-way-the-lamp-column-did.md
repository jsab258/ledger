line: instruments (a contract two consumers do not implement)
spec: FOUND 2026-09-21 by the builder that fixed the lighting column, and
  CONFIRMED HERE BY COMMAND rather than taken on report:

    for f in tools/art-recipes/*.py; do grep -c '"--commission"' "$f"; done

  gives fascia-cornice-elevation.py MISSING, quay-street-mickeys-walk.py
  MISSING, mickeys-blockout.py ACCEPTED, lighting-column.py ACCEPTED (as of
  tonight).

  THIS IS NOT A PREDICTION, IT IS THE FAULT THAT ALREADY HAPPENED, one file
  over. `.github/workflows/ledger-art-blender-preview.yml` invokes every recipe
  as `blender --background --factory-startup --python <recipe> -- --out $outDir
  --root $ws --commission $commission --run-sha $artSha --studio-sha
  $studioSha`. On 2026-09-21 the lighting column met that line for the first
  time and refused: `status=BAD-ARGS reason=unknown-flag/--commission`,
  blenderExit=2, nothing rendered, run 35649856734. The two recipes above will
  do exactly the same on their first real lane run, and neither has had one.

  THE COST IS NOT THE FLAG, IT IS THE ROUND TRIP. Each of these failures costs a
  dispatch to Jafar's PC, a runner slot and the wall clock to find out something
  a local test can now answer in a second, because `lane_contract()` in
  lighting-column.py DERIVES the lane's flag list at test time from the
  workflow and from run-recipe.py rather than from a retyped list.

  DO NOT COPY `lane_contract()` INTO EACH RECIPE. Its author wrote it to be
  lifted into a shared module when a second consumer appears, and said so; a
  copy per recipe is the second-site fault this project keeps finding, and it
  would go stale independently in each copy.
acceptance: the two named recipes accept the lane's contract and prove it with
  a test that DERIVES that contract rather than restating it, with the
  derivation shared rather than copied; a planted removal of one flag turns
  each red naming that flag; and the count is stated with its denominator, how
  many recipes exist and how many are covered, so a third recipe added later
  reads as uncovered rather than as fine. If a recipe legitimately does not
  need a lane flag, it still accepts it and says in one comment why it ignores
  it, because a refusal on an unknown flag is what breaks the run.
status: READY 2026-09-21. Filed and not chased in the session that found it,
  under rule 11. Blocked on nothing.

  THE RELATED HOLE, NAMED AND NOT FIXED TONIGHT: mickeys-blockout.py's own
  BAD-ARGS path writes no verdict file either, measured rather than reasoned:
  run it with a valid `--out` and a bad flag and it prints, exits 2, and does
  not even create the directory. lighting-column.py was fixed tonight; the
  precedent it copied was not. Same class, same evening, different file.
