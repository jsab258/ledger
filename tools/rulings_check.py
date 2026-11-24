#!/usr/bin/env python3
"""EVERY STANDING RULING NAMES THE CHECK THAT ENFORCES IT, AND THAT CHECK EXISTS.

    python tools/rulings_check.py             # one line: rulingsCheck lines=N enforced=N faults=N, then each fault
    python tools/rulings_check.py --list      # each standing line's opening words and its enforcers
    python tools/rulings_check.py --added-since 2026-11-16   # Monday: lines added or changed that week, with enforcers
    python tools/rulings_check.py --selftest

WHY, 17 November 2026 (his message 16:38 through the advisor, 205): "every standing rule of his gets its enforcement
the same day, without him asking. The check is code, not memory." Each standing line in RULINGS.md names its
enforcer: a test or script by file name, a gate (fresh_gate.py, the page's publish check, retention.py, the pre-commit
hook), one of the advisor's scheduled checks, or the Monday audit for what only judgement catches.

WHERE THE ENFORCERS LIVE: production/rulings-enforcers.json, not at the end of each line. RULINGS.md is at its
4,900-word cap, raised only with his yes (RULINGS, its head), and 84 lines each ending "Enforced by: <check>" would
add about 400 words; the companion file keeps the cap and is checked the same way (DECISIONS 17 Nov). A line is
matched by its opening words ("line": the first characters of the line after "- ", at least 24); when a ruling's
opening changes, the check fails until its entry is updated, so an edited ruling is looked at again.

WHAT COUNTS AS A STANDING LINE: every top-level "- " bullet of RULINGS.md (a sub-bullet belongs to its parent). A
one-off decision that ends needs no line in RULINGS at all (it lives in DECISIONS.md).

AN ENFORCER, each a string in the entry's "by" list:
  tools/x.py                   a file in the repository (any path that exists)
  tools/x.py::words            that file contains these words (a test's name, a check's message)
  advisor:<name>               one of the advisor's scheduled checks: watchdog, night-check, needs-you-check, daily-backstop
  monday-audit                 the Monday audit (production/research/token-audit/MONDAY-AUDIT-<date>.md), judgement only
It fails when a standing line has no entry, an entry matches no line, an entry has no enforcer, or an enforcer names a
file that does not exist, words not in that file, or an unknown advisor check. Run in the pre-commit hook (when the
commit carries RULINGS.md or the enforcers file) and by the start gate (tools/fresh_gate.py, a line of its own).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULINGS = os.path.join(ROOT, "RULINGS.md")
ENFORCED = os.path.join(ROOT, "RULINGS-ENFORCED.md")  # advisor 367, 24 Nov: enforced lines moved word for word


def rulings_text():
    """RULINGS.md and RULINGS-ENFORCED.md together: one set of standing lines across both files."""
    parts = [open(RULINGS, encoding="utf-8").read()]
    if os.path.isfile(ENFORCED):
        parts.append(open(ENFORCED, encoding="utf-8").read())
    return "\n".join(parts)


ENFORCERS = os.path.join(ROOT, "production", "rulings-enforcers.json")
ADVISOR = ("watchdog", "night-check", "needs-you-check", "daily-backstop")
MIN_KEY = 24


def standing_lines(text):
    return [ln[2:].strip() for ln in text.splitlines() if ln.startswith("- ")]


def enforcer_fault(by, root=ROOT):
    if by == "monday-audit":
        return None
    if by.startswith("advisor:"):
        return None if by[8:] in ADVISOR else "unknown advisor check %r (one of %s)" % (by[8:], ", ".join(ADVISOR))
    path, _, words = by.partition("::")
    full = os.path.join(root, path)
    if not os.path.isfile(full):
        return "file not found: %s" % path
    if words and words not in open(full, encoding="utf-8", errors="replace").read():
        return "%s does not contain %r" % (path, words)
    return None


def faults(text, entries, root=ROOT):
    lines = standing_lines(text)
    out, used = [], set()
    for e in entries:
        key = e.get("line", "")
        if len(key) < MIN_KEY:
            out.append("entry %r: 'line' needs at least %d characters of the ruling's opening" % (key, MIN_KEY))
            continue
        hits = [i for i, ln in enumerate(lines) if ln.startswith(key)]
        if not hits:
            out.append("entry %r matches no standing line (the ruling's opening changed or it left RULINGS)" % key[:50])
        elif len(hits) > 1:
            out.append("entry %r matches %d lines: lengthen it" % (key[:50], len(hits)))
        used.update(hits)
        if not e.get("by"):
            out.append("entry %r names no enforcer" % key[:50])
        for b in e.get("by", []):
            f = enforcer_fault(b, root)
            if f:
                out.append("entry %r: %s" % (key[:50], f))
    for i, ln in enumerate(lines):
        if i not in used:
            out.append("standing line without an enforcer: %r" % ln[:70])
    return out, len(lines), len(used)


def load(path=ENFORCERS):
    return json.load(open(path, encoding="utf-8"))["entries"] if os.path.exists(path) else []


def selftest():
    import tempfile
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("rulings_check selftest FAIL " + name)
    t = tempfile.mkdtemp()
    os.makedirs(os.path.join(t, "tools"))
    open(os.path.join(t, "tools", "g.py"), "w").write("def selftest():\n    'backup due, held'\n")
    text = "# R\n- 17 Nov: his hands only when nothing else can, enforced.\n  - a sub-bullet\n- 3 Oct: never MetaHuman files in git at all.\n"
    good = [{"line": "17 Nov: his hands only when", "by": ["tools/g.py::backup due"]},
            {"line": "3 Oct: never MetaHuman files", "by": ["monday-audit", "advisor:watchdog"]}]
    f, n, u = faults(text, good, t)
    check("two standing lines, both enforced", f == [] and n == 2 and u == 2)
    check("a sub-bullet is not a standing line", len(standing_lines(text)) == 2)
    check("a line without an entry fails", any("without an enforcer" in x for x in faults(text, good[:1], t)[0]))
    check("an entry naming a missing file fails", faults(text, [dict(good[0], by=["tools/nope.py"]), good[1]], t)[0] != [])
    check("an entry naming words not in the file fails", faults(text, [dict(good[0], by=["tools/g.py::no such test"]), good[1]], t)[0] != [])
    check("an unknown advisor check fails", faults(text, [good[0], dict(good[1], by=["advisor:memory"])], t)[0] != [])
    check("an entry with no enforcer fails", faults(text, [dict(good[0], by=[]), good[1]], t)[0] != [])
    check("an edited opening fails until its entry follows",
          faults(text.replace("17 Nov: his hands", "17 Nov: His hands"), good, t)[0] != [])
    check("a too-short key fails", faults(text, [dict(good[0], line="17 Nov"), good[1]], t)[0] != [])
    print("rulings_check selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    text = rulings_text()
    entries = load()
    if "--added-since" in a:
        # MONDAY'S NUMBERS (advisor 205, point 4): standing lines added or changed since a day, with their enforcers
        import subprocess
        since = a[a.index("--added-since") + 1]
        diff = subprocess.run(["git", "-C", ROOT, "log", "--since", since, "-p", "--format=", "--", "RULINGS.md", "RULINGS-ENFORCED.md"],
                              capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        now = set(standing_lines(text))
        added = sorted({ln[3:].strip() for ln in diff.splitlines() if ln.startswith("+- ")} & now)
        for ln in added:
            by = [", ".join(e.get("by", [])) for e in entries if ln.startswith(e["line"])]
            print("%s | %s" % (ln[:70], by[0] if by else "NO ENFORCER"))
        f = faults(text, entries)[0]
        print("rulings added or changed since %s: %d; flagged now: %d" % (since, len(added), len(f)))
        return 0
    if "--list" in a:
        for e in entries:
            print("%s | %s" % (e["line"][:60], ", ".join(e.get("by", []))))
        return 0
    f, n, u = faults(text, entries)
    print("rulingsCheck lines=%d enforced=%d faults=%d" % (n, u, len(f)))
    for x in f:
        print("rulingsCheck FAIL " + x)
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
