#!/usr/bin/env python3
"""Does any workflow name a branch this repository does not have?

    python3 tools/workflow-branch-refs.py             # the live tree
    python3 tools/workflow-branch-refs.py --selftest  # both outcomes, accepting first
    python3 tools/workflow-branch-refs.py --branches  # just the branch list and its source

WHY THIS EXISTS. Queue 269. Six of eighteen workflows carried

    push:
      branches: [claude/game-dev-ai-automation-2h67ix]

the branch of the repository we left on 2026-09-10. It does not exist on
jsab258/ledger. A push trigger naming a branch that does not exist produces NO
run, NO log and NO red tick, so nothing said so for three days:
`publish-glance.yml`, the workflow behind the link on Jafar's phone, had a run
count of 0 out of 0 on this repository and his console had not rebuilt since
the move. That is CLAUDE.md rule 12 with the channel silent and rule 4's
answer, somebody opening the artifact, as the only thing that could have
surfaced it.

The same file named the dead branch at ten sites, not one, and the other nine
are the half that turns a partial fix into a worse fault than the fault. Four
`actions/checkout` `ref:`s pinned it, so every job checked out nothing; two
commit loops ended in `git push origin HEAD:<dead-branch>`, which would have
CREATED that branch here the moment the checkouts stopped failing. A trigger
moved without its refs fires and then works on nothing; refs moved without the
pushes grow a second head no session should push to. So this check reads
TRIGGER FILTERS, CHECKOUT REFS AND GIT COMMANDS, not just the `on:` block.

WHERE THE BRANCH LIST COMES FROM, and it is not a fixed allowlist.

    1. `git ls-remote --heads origin`. The repository itself, over the
       network, and it is what runs here today: measured 2026-09-13 from this
       container at 0.8s, returning exactly main, art/atlas-01, pc-inbox and
       pc-results, which agrees with the branches API. That is the source.
    2. If that fails (no network, no remote), the local remote-tracking refs
       under refs/remotes/origin/. THIS IS THE WEAKER SOURCE AND SAYS SO IN
       ITS OWN KEY, because it is stale by construction: measured the same
       day, this container held FIVE such refs against the remote's four, the
       extra being refs/remotes/origin/claude/vigilant-ritchie-qvxj87, which
       `ls-remote` does not list. A stale list can wave through a branch that
       no longer exists, and a reader has to be able to see which list the
       verdict was taken from. Hence `branchSource=` on every line of output.
    3. If neither yields a branch, this refuses OUT LOUD with the words
       nothing measured and SKIPS. A check that cannot get its denominator
       must not go green, and must not go red either: a false red here blocks
       every commit made offline.

It also prints the remote URL it read, because a check that does not say which
world its numbers are of is the fault the 2026-09-10 ruling found in
`tools/d1-cycles.py`.

A `#` LINE IS PROSE, NOT A SETTING, and that is deliberate rather than lazy.
The fix for queue 269 writes the dead branch name into six workflows on
purpose: each one carries a comment naming what was read to decide between
re-pointing to `main` and deleting the trigger, and those comments quote the
name they retired. A check that grepped the file would refuse the explanation
of its own repair. The same rule drops shell comments inside `run:` blocks,
which start with `#` too, and no live git command is ever inside one.

WHAT IT CANNOT DECIDE, counted rather than dropped. `${{ github.sha }}`,
`${GITHUB_REF_NAME}` and `$BR` resolve at run time; `releases/**` is a glob
that matches a set rather than naming a member. Neither can be tested for
membership from disk, so both are counted into `skipped=` with their own
buckets and the done line carries the numbers. A skip that does not print is
how a check ends up reporting a clean zero over nothing at all.
"""

import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"

# Remote names a git command in a workflow can plausibly carry. Anything else
# (a URL, a variable) falls through to the expression bucket.
REMOTE_WORDS = ("origin", "upstream")

# Tokens that are git's own, never a branch.
GIT_OWN = ("HEAD", "FETCH_HEAD", "ORIG_HEAD", "MERGE_HEAD", "CHERRY_PICK_HEAD")

SHA = re.compile(r"^[0-9a-f]{7,40}$")
KEY_BRANCHES = re.compile(r"^(\s*)(branches|branches-ignore):\s*(.*)$")
KEY_REF = re.compile(r"^\s*ref:\s*(.+)$")
LIST_ITEM = re.compile(r"^\s*-\s*(.*)$")
REFS_HEADS = re.compile(r"refs/heads/([^\s:'\"]+)")
REMOTE_SLASH = re.compile(r"^['\"]?(?:%s)/([^\s'\"]+)['\"]?$" % "|".join(REMOTE_WORDS))

# WHAT CAN BE A BRANCH NAME AT ALL, and this line exists because the FIRST run
# of this check on the live tree reported one false positive: `git fetch
# --depth=1 origin \` in publish-glance.yml, where the token after the remote
# is a shell line-continuation. git-check-ref-format forbids a backslash, a
# space, `~`, `^`, `:`, `?`, `*` and `[` in a ref name, so shell punctuation is
# not a branch claim at all and is not counted as one. An unresolved expression
# still passes this gate on purpose, so that it reaches the skip buckets and is
# COUNTED rather than dropped: the two outcomes are different facts.
REFNAME_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")

NOTHING_MEASURED = "nothing measured"


# --------------------------------------------------------------- the branch list
def branch_list(root=None):
    """(branches, sourceKey, originUrl). Never guesses, always says which.

    `branches` is None when nothing could be read, which is a SKIP upstream and
    not a pass: see the docstring's point 3."""
    root = root or ROOT
    origin = _git(["config", "--get", "remote.origin.url"], root) or "?"
    origin = re.sub(r"^https?://", "", origin).rstrip("/")

    out = _git(["ls-remote", "--heads", "origin"], root, timeout=30)
    if out:
        names = sorted({l.split("refs/heads/", 1)[1].strip()
                        for l in out.splitlines() if "refs/heads/" in l})
        if names:
            return names, "git-ls-remote/origin", origin

    out = _git(["for-each-ref", "--format=%(refname)", "refs/remotes/origin/"], root)
    if out:
        names = sorted({l.split("refs/remotes/origin/", 1)[1].strip()
                        for l in out.splitlines() if "refs/remotes/origin/" in l
                        and not l.endswith("/HEAD")})
        if names:
            return names, "local-tracking-refs/MAY-BE-STALE", origin

    return None, "none/" + NOTHING_MEASURED.replace(" ", "-"), origin


def _git(args, cwd, timeout=15):
    try:
        p = subprocess.run(["git"] + args, cwd=str(cwd), capture_output=True,
                           text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return ""
    return p.stdout.strip() if p.returncode == 0 else ""


# ------------------------------------------------------------------- extraction
def _decomment(s):
    """Drop a trailing YAML comment. A `#` only opens one at the start of the
    line or after whitespace, which is also what YAML says."""
    m = re.search(r"(?:^|\s)#", s)
    return s[:m.start()] if m else s


def _classify(name):
    """None when this value IS a branch name to test, else the skip bucket.

    Every return here is a number on the done line. Nothing is dropped."""
    name = name.strip().strip("'\"").strip()
    if not name:
        return "empty"
    if "$" in name or "{{" in name:
        return "expr"
    if name in GIT_OWN:
        return "expr"
    if SHA.match(name):
        return "sha"
    if any(c in name for c in "*?![]"):
        return "glob"
    return None


def claims(text):
    """[(line, kind, name)] for every branch this file NAMES as a live setting.

    Three passes, because the fault has three shapes and fixing one without the
    others is the partial fix queue 254 named:
      filter    `on: push: branches:` and `branches-ignore`, both YAML forms
      ref       an `actions/checkout` `ref:`, which is what a run works ON
      git       a fetch, rebase, pull or push target inside a `run:` block,
                which is what can CREATE a branch that should not exist
    """
    lines = text.split("\n")
    found = []
    for i, raw in enumerate(lines):
        if raw.lstrip().startswith("#"):
            continue
        line = _decomment(raw)
        n = i + 1

        m = KEY_BRANCHES.match(line)
        if m:
            indent, val = len(m.group(1)), m.group(3).strip()
            if val.startswith("[") and val.endswith("]"):
                for tok in val[1:-1].split(","):
                    if tok.strip():
                        found.append((n, "filter", tok))
            elif not val:
                found.extend(_block_items(lines, i, indent, "filter"))
            continue

        m = KEY_REF.match(line)
        if m:
            found.append((n, "ref", m.group(1)))
            continue

        if "git " in line:
            found.extend((n, "git", v) for v in _git_targets(line))
    return found


def _block_items(lines, i, indent, kind):
    """The `- name` items under a key that had no inline value."""
    out, j = [], i + 1
    while j < len(lines):
        s = lines[j]
        if not s.strip() or s.lstrip().startswith("#"):
            j += 1
            continue
        if (len(s) - len(s.lstrip())) <= indent:
            break
        m = LIST_ITEM.match(_decomment(s))
        if not m:
            break
        if m.group(1).strip():
            out.append((j + 1, kind, m.group(1)))
        j += 1
    return out


def _git_targets(line):
    """Branch names a git command on this line would act on."""
    toks = line.split()
    out = []
    fetching = any(t in ("fetch", "pull") for t in toks)
    for k, t in enumerate(toks):
        bare = t.strip("'\"")
        if bare.startswith("HEAD:"):                       # push refspec
            out.append(bare[5:])
        for m in REFS_HEADS.finditer(bare):                # explicit refspec
            out.append(m.group(1))
        m = REMOTE_SLASH.match(t)                          # rebase/merge target
        if m and not m.group(1).startswith("refs/"):
            out.append(m.group(1))
        if fetching and bare in REMOTE_WORDS and k + 1 < len(toks):
            nxt = toks[k + 1].strip("'\"")
            if nxt and not nxt.startswith("-") and ":" not in nxt \
                    and not nxt.startswith("refs/"):
                out.append(nxt)
    return [t for t in out if _plausible(t)]


def _plausible(tok):
    """Could this token be a ref name at all? See REFNAME_OK."""
    return bool(REFNAME_OK.match(tok)) or "$" in tok or "{" in tok


# ------------------------------------------------------------------ the check
def check(files, branches):
    """(dead, tested, skips) over `files`, each a (name, text) pair.

    `tested` is the count of names actually compared, and it is the denominator
    the zero needs: 0 dead of 0 tested means this check saw nothing, which is
    not the same fact as 0 dead of 14."""
    dead, tested = [], 0
    skips = {"expr": 0, "glob": 0, "sha": 0, "empty": 0}
    for name, text in files:
        for line, kind, raw in claims(text):
            bucket = _classify(raw)
            if bucket:
                skips[bucket] += 1
                continue
            tested += 1
            value = raw.strip().strip("'\"").strip()
            if value not in branches:
                dead.append((name, line, kind, value))
    return dead, tested, skips


REMEDY = [
    "REMEDY, and it is a decision per workflow rather than a find-and-replace:",
    "  Re-point the trigger to a branch that exists, OR delete the dead push",
    "  trigger so only workflow_dispatch remains. Which one depends on what the",
    "  job COSTS: an expensive job is opt-in (CLAUDE.md rule 9), a one-minute",
    "  check on ubuntu-latest with its own concurrency group is not. Write the",
    "  reason in that workflow's own YAML comment, naming what you read.",
    "  A checkout `ref:` or a `git push origin HEAD:<branch>` naming a dead",
    "  branch MOVES IN THE SAME EDIT as the trigger. A trigger fixed alone",
    "  fires and then works on nothing; refs fixed alone let the next push",
    "  CREATE the dead branch here, a second head no session should push to",
    "  (queue 254). Use ${GITHUB_REF_NAME}: a dispatched ref exists already.",
]


def _report(files, branches, source, origin):
    """The done line carries WHOLE-RUN numbers and nothing per-file.

    Three denominators, because three different zeros can hide here: how many
    workflows were walked, how many branch references were FOUND, and how many
    of those could actually be tested. `0 dead` over 0 examined and `0 dead`
    over 38 examined are different facts, and the second is only reassuring if
    the reader can also see that 30 of them were skipped and why.

    It prints the branch list it compared against, in full, on both outcomes.
    A check whose verdict depends on a list the reader cannot see is a check
    the reader has to take on trust."""
    dead, tested, skips = check(files, branches)
    examined = tested + sum(skips.values())
    skipline = "skipped=" + "/".join("%d%s" % (skips[k], k)
                                     for k in ("expr", "glob", "sha", "empty"))
    counts = ("walked=%dworkflow(s) examined=%dref(s) tested=%d %s"
              % (len(files), examined, tested, skipline))
    where = ("branchSource=%s origin=%s repoBranches=%d comparedAgainst=%s"
             % (source, origin, len(branches), ",".join(branches)))
    if dead:
        print("workflow-branch-refs: %d of %d branch name(s) tested name a branch "
              "ABSENT from this repository" % (len(dead), tested))
        print("  " + counts)
        print("  " + where)
        shown = dead[:20]
        for name, line, kind, value in shown:
            print("  %s:%d  %s -> %s" % (name, line, kind, value))
        if len(dead) > len(shown):
            print("  (+%d more not shown)" % (len(dead) - len(shown)))
        for l in REMEDY:
            print("  " + l)
        return 1, dead, tested
    print("workflow-branch-refs: 0 dead of %d branch name(s) tested in %d "
          "workflow(s)" % (tested, len(files)))
    print("  " + counts)
    print("  " + where)
    if not tested:
        print("  %s: no workflow named a testable branch, so this run proves "
              "nothing about them." % NOTHING_MEASURED)
    return 0, dead, tested


def _live_files():
    if not WORKFLOWS.is_dir():
        return []
    paths = sorted(list(WORKFLOWS.glob("*.yml")) + list(WORKFLOWS.glob("*.yaml")))
    return [(p.name, p.read_text(encoding="utf-8")) for p in paths]


# ------------------------------------------------------------------- selftest
ACCEPT_YML = """\
on:
  push:
    branches: [main]
    paths:
      - 'tools/**'
  workflow_dispatch:
jobs:
  a:
    steps:
      - uses: actions/checkout@v4
        with:
          ref: pc-inbox
      - run: |
          git fetch origin pc-results
          git push origin "HEAD:${GITHUB_REF_NAME}"
"""

REJECT_YML = """\
on:
  push:
    branches: [claude/game-dev-ai-automation-2h67ix]
  workflow_dispatch:
"""

REJECT_BLOCK_YML = """\
on:
  pull_request:
    branches:
      - main
      - claude/game-dev-ai-automation-2h67ix
"""

REJECT_PUSH_YML = """\
jobs:
  a:
    steps:
      - run: |
          git fetch origin claude/game-dev-ai-automation-2h67ix || true
          git rebase origin/claude/game-dev-ai-automation-2h67ix || true
          git push origin HEAD:claude/game-dev-ai-automation-2h67ix
"""

COMMENT_YML = """\
# This file USED to say claude/game-dev-ai-automation-2h67ix and the comment
# explaining the repair must not be the thing that fails the repair.
on:
  push:
    # `main`, not claude/game-dev-ai-automation-2h67ix, which is gone.
    branches: [main]
  workflow_dispatch:
"""

SKIPPABLE_YML = """\
on:
  push:
    branches: [main, 'releases/**']
jobs:
  a:
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}
      - run: |
          git push "$origin" HEAD:${GITHUB_REF_NAME}
"""


def selftest():
    """BOTH OUTCOMES, AND THE ACCEPTING ONE FIRST (CLAUDE.md rule 5b).

    THE LIVE TREE IS THE ACCEPTING FIXTURE, per .claude/rules/instruments.md:
    for a tool that checks the project itself, doing the work the tool asks for
    must never be able to break the tool. The rejecting fixtures are synthetic
    and name a branch that exists nowhere.

    It is not enough to prove the check can fail. Case 2b plants a branch that
    DOES exist in the same syntactic slot as case 2's dead one, so a guard that
    simply refuses every branch name it sees cannot pass this suite. A guard
    that cannot tell a regression from an improvement is a ratchet."""
    passed = failed = 0

    def case(ok, label, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
        print("  %s %s%s" % ("ok  " if ok else "FAIL", label,
                             ("  [%s]" % detail) if detail else ""))

    branches, source, origin = branch_list()
    if branches is None:
        print("  SKIPPED (no branch-list in this container: neither "
              "`git ls-remote --heads origin` nor refs/remotes/origin answered)")
        print("workflow-branch-refs selftest: 0 passed, 0 failed, 0 checks run "
              "(%s)" % NOTHING_MEASURED)
        return 0

    # 1. ACCEPTING, the live tree. A zero here carries its denominator, and the
    #    denominator must not itself be zero or the pass is over nothing.
    live = _live_files()
    dead, tested, _ = check(live, branches)
    case(live and not dead and tested > 0,
         "the live .github/workflows tree names no absent branch",
         "%d workflow(s), %d name(s) tested, %d dead" % (len(live), tested, len(dead)))

    # 2. REJECTING, one synthetic workflow per shape the fault takes.
    d, t, _ = check([("reject-inline.yml", REJECT_YML)], branches)
    case(len(d) == 1 and d[0][2] == "filter" and t == 1,
         "an inline `branches: [<absent>]` filter is caught",
         "%d of %d tested" % (len(d), t))

    d, t, _ = check([("reject-block.yml", REJECT_BLOCK_YML)], branches)
    case(len(d) == 1 and t == 2 and d[0][3].startswith("claude/"),
         "a block-form branches list is caught, and `main` beside it is not",
         "%d of %d tested" % (len(d), t))

    d, t, _ = check([("reject-push.yml", REJECT_PUSH_YML)], branches)
    case(len(d) == 3 and t == 3 and all(x[2] == "git" for x in d),
         "the fetch, the rebase and the HEAD: push that would CREATE it are caught",
         "%d of %d tested" % (len(d), t))

    # 2b. THE CASE THAT STOPS THIS BEING A RATCHET: the same slots, live names.
    d, t, _ = check([("accept-live-names.yml", ACCEPT_YML)], branches)
    case(not d and t == 3,
         "a filter, a checkout ref and a fetch naming EXISTING branches pass",
         "%d dead of %d tested" % (len(d), t))

    # 3. A comment naming the dead branch is prose, not a setting.
    d, t, _ = check([("comment.yml", COMMENT_YML)], branches)
    case(not d and t == 1,
         "a comment quoting the retired branch does not fail the repair",
         "%d dead of %d tested" % (len(d), t))

    # 4. Unresolvable values are SKIPPED WITH A COUNT, never silently dropped.
    d, t, sk = check([("skippable.yml", SKIPPABLE_YML)], branches)
    case(not d and t == 1 and sk["glob"] == 1 and sk["expr"] == 2,
         "expressions and globs are counted into skipped=, not dropped",
         "tested=%d glob=%d expr=%d" % (t, sk["glob"], sk["expr"]))

    # 5. An empty tree must say nothing measured rather than report a clean 0.
    d, t, _ = check([], branches)
    case(not d and t == 0,
         "no workflows at all measures nothing, and the denominator says so",
         "tested=%d" % t)

    print("workflow-branch-refs selftest: %d passed, %d failed, %d checks run"
          % (passed, failed, passed + failed))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--branches", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    branches, source, origin = branch_list()
    if args.branches:
        print("branchSource=%s origin=%s repoBranches=%s"
              % (source, origin, "0" if branches is None else len(branches)))
        for b in branches or []:
            print("  " + b)
        if branches is None:
            print("  " + NOTHING_MEASURED)
        return 0

    if branches is None:
        # NOT A PASS AND NOT A RED. Offline, the list this check compares
        # against does not exist, and inventing one would be a threshold nobody
        # measured. verify.py turns this line into a SKIP in the footer, so a
        # commit made without the check says so in its own message.
        print("workflow-branch-refs: SKIPPED (no branch-list in this container: "
              "neither `git ls-remote --heads origin` nor refs/remotes/origin "
              "answered). %s about %d workflow(s)."
              % (NOTHING_MEASURED, len(_live_files())))
        return 0

    if not WORKFLOWS.is_dir():
        print("workflow-branch-refs: SKIPPED (no workflows-directory on disk). "
              "%s." % NOTHING_MEASURED)
        return 0

    code, _, _ = _report(_live_files(), branches, source, origin)
    return code


if __name__ == "__main__":
    sys.exit(main())
