#!/usr/bin/env python3
"""THE NIGHT'S PACKAGED BUILD, ASKED FOR ONLY WHEN THE WORK HAS MOVED (Jafar, 6 October).

    python tools/nightly_package.py              # ask for tonight's build if wip moved since the played copy
    python tools/nightly_package.py --dry-run    # say what it would do
    python tools/nightly_package.py --selftest

WHY. Jafar, 6 October: "Pushes to the working branch, wip, no longer start a packaged build. My
push rule was meant to make your work visible, not to build it eight times a day. The packaged
build runs only when you ask for it as a step's evidence, in the nightly run, or when work goes
to main." The build machine's workflow (.github/workflows/ledger-probe-unreal.yml) now builds on
a push to wip only when the pushed commit's message carries [package]. This is the nightly run's
half: tools/nightly_walk.py calls it first, at 02:30, so the walk plays tonight's work.

HOW, WITHOUT TOUCHING THE CHECKOUT. The builder may have work in progress in the same checkout at
night, so nothing here uses the working tree or the index: the request is one line appended to
production/d1-probe/PACKAGE.md in a commit built with git's plumbing on top of origin/wip (a
throwaway index file), and that commit is pushed fast-forward to wip, through the same guards as
any push. No key or token is read: git uses the PC's own credential manager, as every push does.

WHEN IT ASKS. Only when origin/wip has a commit after the played copy's own (Content/LedgerData/
build-commit.txt) that is not the build machine's own result ("UE machine probe from ...").
"""
import datetime as dt
import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYED_STAMP = r"F:\LedgerTools\played-game\Windows\LedgerProbe\Content\LedgerData\build-commit.txt"
REQUEST_FILE = "production/d1-probe/PACKAGE.md"
FLAG = "[package]"
RUNNER_PREFIX = "UE machine probe from "


def git(*args, env=None, inp=None):
    r = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, env=env, input=inp)
    if r.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args[:3]), (r.stderr or r.stdout).strip()[:300]))
    return r.stdout


def needs_build(built, subjects):
    """True when any commit after the built one is someone's work and not the build machine's
    own result. subjects: the commit subjects from the built commit (exclusive) to the head."""
    if not built:
        return True
    return any(not s.startswith(RUNNER_PREFIX) for s in subjects)


def request_line(date, head, built):
    return "- %s nightly: wip at %s, the played copy at %s\n" % (date, head[:8], (built or "none")[:8])


def main(dry=False):
    built = open(PLAYED_STAMP, encoding="utf-8").read().strip() if os.path.isfile(PLAYED_STAMP) else ""
    git("fetch", "-q", "origin", "wip")
    head = git("rev-parse", "origin/wip").strip()
    try:
        subjects = git("log", "--format=%s", "%s..origin/wip" % built).splitlines() if built else []
    except RuntimeError:
        subjects = ["(the played copy's commit is not on wip)"]
    if not needs_build(built, subjects):
        print("nightlyPackage=UP-TO-DATE built=%s head=%s" % (built[:8], head[:8]))
        return 0
    if dry:
        print("nightlyPackage=WOULD-ASK built=%s head=%s newCommits=%d" % (built[:8], head[:8], len(subjects)))
        return 0
    try:
        old = git("show", "origin/wip:" + REQUEST_FILE)
    except RuntimeError:
        old = ("# Packaged builds asked for on wip\n\nOne line per request: a step's evidence (the builder's "
               "commit carries [package]) or the night's, by tools/nightly_package.py.\n\n")
    blob = git("hash-object", "-w", "--stdin", inp=old + request_line(dt.date.today().isoformat(), head, built)).strip()
    fd, index = tempfile.mkstemp(prefix="nightly-index-")
    os.close(fd)
    os.remove(index)
    env = dict(os.environ, GIT_INDEX_FILE=index)
    try:
        git("read-tree", "origin/wip", env=env)
        git("update-index", "--add", "--cacheinfo", "100644,%s,%s" % (blob, REQUEST_FILE), env=env)
        tree = git("write-tree", env=env).strip()
    finally:
        if os.path.exists(index):
            os.remove(index)
    msg = "Nightly packaged build of wip %s %s\n\nThe night's run (tools/nightly_package.py): wip has moved since the played copy (%s).\n" % (
        head[:8], FLAG, (built or "none")[:8])
    commit = git("commit-tree", tree, "-p", head, "-m", msg).strip()
    git("push", "origin", "%s:refs/heads/wip" % commit)
    print("nightlyPackage=ASKED commit=%s built=%s head=%s" % (commit[:8], built[:8], head[:8]))
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("nightly_package selftest FAIL " + name)
    check("nothing after the built commit: no build", not needs_build("abc", []))
    check("only the build machine's own result after it: no build",
          not needs_build("abc", ["UE machine probe from abc1234"]))
    check("any other commit after it: a build", needs_build("abc", ["UE machine probe from abc", "Item 1.1's fixes"]))
    check("no played copy at all: a build", needs_build("", []))
    line = request_line("2026-10-07", "0123456789abcdef", "fedcba9876543210")
    check("the request line names both commits, short", "01234567" in line and "fedcba98" in line and line.endswith("\n"))
    check("the workflow builds wip only on the flag this writes",
          FLAG in open(os.path.join(REPO, ".github", "workflows", "ledger-probe-unreal.yml"), encoding="utf-8").read())
    print("nightly_package selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main(dry="--dry-run" in sys.argv))
