# 270: tools_tracked cannot see a tool only verify.py runs

STATUS: READY
OPENED: 2026-09-13, filed by the ruling at
decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md section 7.

## The fault, measured on 2026-09-13

Four new tools landed in one batch. `tools_tracked` walks tools NAMED IN A
WORKFLOW, so its reach over them is:

    tools/budget-ceiling.py          reached only through tools/glance.py:90
    tools/budget-ceiling-check.py    reached only through tools/glance.py:683
    tools/workflow-branch-refs.py    reached by NOTHING
    tools/budget-log-mark.py         reached by NOTHING

The first two are reached at all only because `glance.py` is named in
`publish-glance.yml` and now mentions them, and both of those mentions are
COMMENT LINES. The last two are named only by `ledger/verify.py` and by
themselves.

WHAT THAT COSTS. A new tool that only `verify.py` runs can be left untracked
and nothing says so. It survives in the container that wrote it, and a fresh
checkout is missing it: the first symptom is a check that cannot run, on a
machine that is not the one where the mistake was made. On this batch two of
the four were flagged and two were not, and the two that were not are the ones
the resident had to remember by hand.

## Done looks like

1. `tools_tracked` walks `ledger/verify.py` as a SECOND ROOT alongside the
   workflows, matching all three forms it uses to name a tool: the
   `tools/<name>.py` string, the `"tools" / "<name>.py"` join, and the rels in
   `TOOL_SELFTESTS`.
2. It prints reach PER ROOT, so a reader can tell where a tool is reached from:
   `viaWorkflows=N viaVerify=M`, and where it can be told, the count reached
   ONLY through a comment line is named separately, because a tool held by a
   comment is one edit from being held by nothing.
3. Tested both ways per CLAUDE.md rule 5b, accepting case first: the live tree
   passes, and a synthetic verify text naming a tool that exists nowhere fails.
4. The zero ships its denominator: how many tools were examined, not just how
   many were untracked.

## Risk

None. It is a wider denominator on a check that already exists, so the only
way it can newly fail is by finding something real.
