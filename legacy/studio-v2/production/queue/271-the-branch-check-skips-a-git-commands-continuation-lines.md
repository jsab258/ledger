# 271: the branch check skips a git command's continuation lines

STATUS: READY
OPENED: 2026-09-13, filed by the ruling at
decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md section 7.

## The fault, measured on 2026-09-13

`tools/workflow-branch-refs.py`'s `claims()` examines a line for git targets
only when that line itself contains `git `. A multi-line shell command puts the
target on a continuation line, which therefore goes unexamined.

The live instance, found by the director reading the file rather than by the
check reporting it: `.github/workflows/publish-glance.yml` lines 197 to 198
carry `refs/heads/art/atlas-01` on a continuation. That name is a real branch,
so nothing is wrong today. A DEAD name in the same position would pass green,
which is the whole point: the check's clean result is currently narrower than
it reads.

THE CHECK IS NOT AT FAULT FOR PASSING. It is at fault for not saying that this
shape is outside what it examined. Its denominator prints `examined=38ref(s)`
and those 38 do not include continuations.

## Done looks like

1. A `run:` block is joined on backslash-newline BEFORE the git pass, so a
   target on a continuation is examined like any other.
2. A rejecting fixture plants a dead branch name on a continuation line and the
   check fails on it, named as such.
3. The live tree still passes, and the accepting case runs first per CLAUDE.md
   rule 5b: `refs/heads/art/atlas-01` at publish-glance.yml 197 to 198 is a real
   branch and must keep passing once it becomes visible to the check.
4. The printed `examined=` count goes UP, and the change in that number is the
   evidence the fix reached something. A fix that leaves the denominator where
   it was has not been proven.

## What this does not cover

Any other shell shape that hides a branch name from a line-at-a-time reader:
a name in a variable, a heredoc, a name built by string concatenation. The
check already skips `${GITHUB_REF_NAME}` and friends deliberately and says so.
This item is the continuation case alone, because that is the one with a live
instance in the tree.
