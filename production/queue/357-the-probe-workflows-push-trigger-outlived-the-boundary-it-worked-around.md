line: instruments (.github/workflows/ledger-probe-unreal.yml, the `on:` block;
  production/d1-probe/DISPATCH, the sentinel that doubles as the dispatch log)
spec: the probe workflow triggers TWO ways: `workflow_dispatch`, and a push
  that touches `production/d1-probe/DISPATCH`. The push trigger is a
  documented workaround, and the file says so in its own words at lines 18-40:

      GitHub only dispatches a `workflow_dispatch` workflow that exists on the
      DEFAULT BRANCH. This repo's default is `main`; ... this one lives on the
      working branch, so a dispatch of it returns 404. Confirmed by
      dispatching and reading the error, not assumed from the docs.
      ...
      WHEN THIS FILE REACHES `main`, DELETE THE PUSH TRIGGER AND THE SENTINEL.
      ... the push trigger is a workaround for a permission boundary, not a
      design, and leaving it in place after the boundary moves would be the
      kind of scaffolding that outlives its reason.

  THE BOUNDARY HAS MOVED. Checked rather than assumed, 2026-09-16:
  `git ls-tree origin/main --name-only .github/workflows/ledger-probe-unreal.yml`
  returns the path, and `git symbolic-ref --short HEAD` is `main`. The
  workflow is on the default branch. The condition its own comment names as
  the trigger for its own removal is met.
acceptance: either the push trigger and the sentinel are gone and a
  `workflow_dispatch` is shown to have STARTED A RUN (the effect, not the API
  returning 204), or the file says in one line why the workaround is kept, so
  the next reader does not have to re-derive that it is deliberate
max_sessions: 1
status: READY 2026-09-16, filed and NOT started, under Jafar's standing rule
  of today: an audit finding is filed and the standing order resumes. Today is
  the visual slice.

  DO NOT DELETE THE PUSH TRIGGER BEFORE A DISPATCH IS PROVEN TO WORK, and this
  is the whole reason this is an item rather than an edit. The push trigger is
  currently THE ONLY DISPATCH PATH ANYONE HAS DEMONSTRATED. Removing it on the
  strength of "the file is on main now, so dispatch should work" would be
  exactly the reasoning `.claude/rules/ci.md` forbids: run the existing entry
  point and read its output before proposing a mechanism. The order is prove
  first, delete second, in that order and never the reverse. A studio that
  deletes its only working dispatch on a docs reading spends an evening
  finding out.

  AND THE SENTINEL IS NOT ONLY A SENTINEL, which the comment does not say and
  whoever takes this must not miss. `production/d1-probe/DISPATCH` is also the
  DISPATCH LOG: one appended line per run, 48 runs deep, each naming what that
  run was for. Deleting the file to remove the trigger would delete the log of
  every probe run this project has made. If the trigger goes, the log moves
  somewhere first.
