# 254. Six push filters name a dead branch, and one would resurrect it

STATUS: READY, 2026-09-10. Ruled out of the move batch by
`game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-behind.md`
section 5, finding 1.

## What is wrong

Six workflows filter `push: branches: [claude/game-dev-ai-automation-2h67ix]`,
a branch that does not exist in jsab258/ledger, so none of them fires on a
push any more: `voice-candidates`, `citypack-fetch`, `props-fetch`,
`ledger-build-mac`, `citypack-inventory`, `publish-glance`. All keep
`workflow_dispatch`.

`voice-candidates.yml` is the sharp one. Beyond the filter (line 23) it names
the dead branch at four `ref:` sites (69, 121, 148, 207) and at two pushes
(86 and 401, `git push origin HEAD:claude/game-dev-ai-automation-2h67ix`).
TODAY THE HAZARD IS LATENT: every job checks out the dead ref first, the
checkout fails, and no push is reached. IT BECOMES LIVE ON A PARTIAL FIX: move
the filter or the refs without the two pushes and the next inventory or fetch
run creates the old branch in the new repository, a second head that no
session should ever push to.

## The deliverable

One edit per workflow, and for `voice-candidates.yml` all seven sites in ONE
edit, with the proof being `grep -c 'claude/game-dev-ai-automation-2h67ix'`
printing 0 for that file and for `.github/workflows/` as a whole (denominator:
files scanned). `citypack-fetch`, `props-fetch` and `citypack-inventory`
already push to `${GITHUB_REF_NAME}`, so only their filters move.

Two stay as they are, by ruling: `ledger-build-mac.yml` stays push-dead (D16
retired the Unity build, and `macos-latest` minutes are the expensive class;
write that sentence into the file beside the filter). `publish-glance.yml`
flips together with the site links in queue 256, after one dispatched run on
`ledger` prints the served commit.

## Done looks like

The grep above at 0 over `.github/workflows/`, a verify lint that refuses the
dead branch name anywhere under `.github/workflows/` from then on (its
accepting case the live tree, its rejecting case a synthetic workflow
fixture), and one dispatched `voice-candidates` inventory run landing its
table on `main` and nowhere else (`git ls-remote` shows no new branch).

## Dependencies and risk

None on the fleet. Risk is the partial fix described above; the lint is what
makes it a refusal rather than a memory.
