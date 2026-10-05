#!/usr/bin/env python3
"""THE FILES EVERY SESSION READS STAY SHORT ENOUGH TO BE READ, NOT SKIMMED.

Jafar, 3 October: DECISIONS.md reached 23,600 words in ten days, CLAUDE.md
4,000 against a cap of 600, NOW.md 2,300 against five lines; at that length the
sessions skimmed them and could not tell which ruling was current. So the caps
are checked by the build, not by good intentions: this fails when a file is
over its cap, and when a file it must measure is missing (nothing measured
must never read as clean).

Words are counted as `wc -w` counts them: runs of non-space characters.

  python tools/doc-caps.py             # the real files; exit 1 naming each one over
  python tools/doc-caps.py --staged    # only the capped files a commit carries (the pre-commit hook)
  python tools/doc-caps.py --selftest  # the check itself, both ways

APPLIED 3 October by the builder from production/drafts/rulings-2026-10-03 (CHECK.md), with
two changes so it never stops another session's work: the commit hook checks only the capped
files that commit carries (in a worktree whose branch is behind, the other files are not that
commit's business), and the town's and clothing's status files are reported, not failed, until
each session has trimmed its own and taken it out of NOT_YET.
"""
import os
import re
import sys
import tempfile

# THE CAPS. A new session's own status file is added here, with its cap, in the
# same commit that creates it.
CAPS = [
    ("CLAUDE.md", 1000),
    ("RULINGS.md", 2500),
    ("NOW.md", 200),
    ("TOWN.md", 300),
    ("CLOTHES.md", 300),
    # Adopted 5 October from the outside audit's drafts (production/audits/2026-10-04-*).
    ("CHARTER.md", 400),
    ("PLAN.md", 1200),
]
# Measured and printed, not failed, until the session that owns the file has trimmed it under its
# cap and removed it from here (handed over 3 October).
NOT_YET = set()  # 5 October: TOWN.md and CLOTHES.md trimmed to bounded-task briefs; nothing exempt.


def words(text):
    return len(text.split())


def sections(text):
    """The largest '## ' sections, so a refusal says where to cut."""
    parts, name, buf = [], "(before the first heading)", []
    for line in text.splitlines():
        if re.match(r"^#{1,3} ", line):
            parts.append((words("\n".join(buf)), name))
            name, buf = line.strip("# ").strip(), []
        else:
            buf.append(line)
    parts.append((words("\n".join(buf)), name))
    return sorted(parts, reverse=True)[:3]


def check(root, caps=CAPS, out=sys.stdout, not_yet=frozenset()):
    over = 0
    for rel, cap in caps:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print("doc-caps file=%s words=- cap=%d outcome=MISSING" % (rel, cap), file=out)
            over += 1
            continue
        text = open(path, encoding="utf-8").read()
        n = words(text)
        ok = n <= cap
        if not ok and rel in not_yet:
            print("doc-caps file=%s words=%d cap=%d outcome=OVER-NOT-YET (its session trims it)" % (rel, n, cap), file=out)
            continue
        print("doc-caps file=%s words=%d cap=%d outcome=%s" % (rel, n, cap, "PASS" if ok else "FAIL"), file=out)
        if not ok:
            over += 1
            print("  largest sections: " + "; ".join("%s (%d)" % (s, w) for w, s in sections(text)), file=out)
    print("doc-caps: %d of %d over cap or missing" % (over, len(caps)), file=out)
    return over


def selftest():
    import io
    fails = 0

    def case(name, files, want_over):
        nonlocal fails
        with tempfile.TemporaryDirectory() as d:
            for rel, text in files.items():
                open(os.path.join(d, rel), "w", encoding="utf-8").write(text)
            buf = io.StringIO()
            got = check(d, [("A.md", 5), ("B.md", 3)], out=buf)
            ok = got == want_over
            fails += 0 if ok else 1
            print("  %s %s: over=%d, wanted %d" % ("ok  " if ok else "FAIL", name, got, want_over))

    print("doc-caps selftest")
    case("ACCEPT both at or under their caps", {"A.md": "one two three four five", "B.md": "a b"}, 0)
    case("ACCEPT markdown and line breaks count as wc -w does", {"A.md": "# H\n\n- x y\n", "B.md": "a\nb\nc"}, 0)
    case("REFUSE one word over the cap", {"A.md": "1 2 3 4 5 6", "B.md": "a"}, 1)
    case("REFUSE a missing file, never read as clean", {"A.md": "1"}, 1)
    case("REFUSE both over", {"A.md": "1 2 3 4 5 6", "B.md": "a b c d"}, 2)
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "A.md"), "w", encoding="utf-8").write("1 2 3 4 5 6")
        open(os.path.join(d, "B.md"), "w", encoding="utf-8").write("a")
        got = check(d, [("A.md", 5), ("B.md", 3)], out=io.StringIO(), not_yet={"A.md"})
        ok = got == 0
        fails += 0 if ok else 1
        print("  %s ACCEPT a file over its cap whose session has not trimmed it yet: over=%d" % ("ok  " if ok else "FAIL", got))
    print("doc-caps selftest: %s" % ("passed" if fails == 0 else "FAILED (%d)" % fails))
    return 1 if fails else 0


def staged():
    """Only the capped files the commit being made carries, as staged."""
    import subprocess
    names = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                           capture_output=True, text=True).stdout.split()
    caps = [(rel, cap) for rel, cap in CAPS if rel in names]
    over = 0
    for rel, cap in caps:
        n = words(subprocess.run(["git", "show", ":" + rel], capture_output=True, text=True, encoding="utf-8").stdout)
        if n > cap:
            over += 1
            print("doc-caps: this commit is refused: %s is %d words, over its cap of %d (CLAUDE.md, Records). Cut it; never --no-verify." % (rel, n, cap))
    return over


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    if "--staged" in sys.argv[1:]:
        sys.exit(1 if staged() else 0)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(1 if check(root, not_yet=NOT_YET) else 0)
