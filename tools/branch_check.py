#!/usr/bin/env python3
"""NO BRANCH OLDER THAN A WEEK STAYS ON GITHUB UNLESS IT IS ARCHIVED, OR THE BUILD FAILS.

Jafar, 5 October 2026 (the plan's edit 10): "every rule from phase 0 gets a check that fails the
build wherever possible: a branch older than a week that is neither merged nor archived". The
September atlas lay a fortnight on a branch nobody knew of. The method
(production/research/catalogue-and-homes/NOTE.md): a branch leaves the list once its work is in
main or kept, archived as a tag archive/<name> so its commits stay reachable; a merged branch is
archived the same way. So the check is simple and needs no history: every branch on GitHub but
main and wip whose last commit is more than seven days old fails, unless it is held in
production/branches-held.json for a stated reason (his page, awaiting his answer), and a hold
itself fails after fourteen days.

The cloud's copy is shallow; there the tips are fetched alone (depth 1, no file contents), so the
dates are real everywhere. Nothing fetched reads as not measured, never as clean.

  python tools/branch_check.py              # exit 1 naming each stale branch or expired hold
  python tools/branch_check.py --selftest
"""
import datetime as dt
import io
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELD = os.path.join(REPO, "production", "branches-held.json")
KEEP = {"main", "wip"}
MAX_AGE_DAYS = 7
MAX_HOLD_DAYS = 14


def git(*args):
    return subprocess.run(("git",) + args, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")


def tips():
    """{branch: last commit time} for every branch on GitHub."""
    shallow = git("rev-parse", "--is-shallow-repository").stdout.strip() == "true"
    if shallow:
        git("fetch", "-q", "--depth=1", "--filter=blob:none", "origin", "+refs/heads/*:refs/remotes/origin/*")
    else:
        git("fetch", "-q", "--prune", "origin")
    out = git("for-each-ref", "--format=%(refname)|%(committerdate:iso-strict)", "refs/remotes/origin").stdout
    found = {}
    for line in out.splitlines():
        ref, _, when = line.partition("|")
        name = ref.replace("refs/remotes/origin/", "", 1)
        if name == "HEAD" or not when:
            continue
        found[name] = dt.datetime.fromisoformat(when)
    return found


def judge(found, held, now):
    bad, holds = [], 0
    for name, when in sorted(found.items()):
        if name in KEEP:
            continue
        age = (now - when).days
        if age <= MAX_AGE_DAYS:
            continue
        h = held.get(name)
        if h:
            holds += 1
            since = dt.datetime.fromisoformat(h["since"]).replace(tzinfo=now.tzinfo)
            if (now - since).days > MAX_HOLD_DAYS:
                bad.append("%s: held since %s for %s, past %d days" % (name, h["since"], h["why"], MAX_HOLD_DAYS))
            continue
        bad.append("%s: last commit %d days ago, neither archived nor held" % (name, age))
    return bad, holds


def check(out=sys.stdout):
    found = tips()
    if "main" not in found:
        print("branch-check outcome=NOT-MEASURED: no branch read from GitHub (offline?)", file=out)
        return 1
    held = {}
    if os.path.exists(HELD):
        for h in json.load(io.open(HELD, encoding="utf-8"))["held"]:
            held[h["branch"]] = h
    now = dt.datetime.now(dt.timezone.utc)
    bad, holds = judge(found, held, now)
    for b in bad:
        print("branch-check FAIL " + b, file=out)
    print("branch-check branches=%d held=%d stale=%d outcome=%s" % (len(found), holds, len(bad), "FAIL" if bad else "PASS"), file=out)
    return 1 if bad else 0


def selftest():
    ok = True

    def t(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    now = dt.datetime(2026, 10, 5, 12, tzinfo=dt.timezone.utc)
    d = lambda n: now - dt.timedelta(days=n)
    found = {"main": d(30), "wip": d(20), "new-work": d(2), "old-work": d(9), "held-work": d(20)}
    held = {"held-work": {"branch": "held-work", "why": "his page", "since": "2026-10-01"}}
    bad, holds = judge(found, held, now)
    t(any(b.startswith("old-work") for b in bad), "a branch older than a week, neither archived nor held, fails")
    t(not any(b.startswith(x) for b in bad for x in ("main", "wip", "new-work", "held-work")), "main, wip, a fresh branch and a held one pass")
    held["held-work"]["since"] = "2026-09-15"
    bad, _ = judge(found, held, now)
    t(any(b.startswith("held-work") for b in bad), "a hold older than fourteen days fails")
    print("branch_check selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
