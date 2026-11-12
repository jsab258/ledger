#!/usr/bin/env python3
"""EVERY NEW TOOL TEST, FIRST TRY AND VERDICT NAMES ITS RESEARCHED METHOD (his rule, 12 Nov 2026, 09:21, via the
advisor's message 116; RULINGS "7 Nov, tries").

    python tools/method_line_check.py            # fails when a new such file lacks the line
    python tools/method_line_check.py --selftest

WHY. The Vellum test of 12 Nov skipped researching the professional method under a 30-minute box, and its verdict was
passed on. His rule: the professional method is researched first, in a dated note, and every tool test, first try and
verdict file carries a line "Method researched: <research file, date>"; no time box overrides it.

WHAT COUNTS. A Markdown file under production/research/ whose name contains VERDICT, TEST or TRY (any case), or any
file under a production/research/tool-tests-* folder, that did not exist at the rule's commit (BASE, 12 Nov). Older
files are left as they were. The line must name something: "Method researched:" followed by a path or a source.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "cd0f7632d"   # the commit before the rule; files present there are not judged
NAME = re.compile(r"(verdict|test|try)", re.I)
LINE = re.compile(r"^\W*Method researched:\s*\S{4,}", re.I | re.M)


def judged(rel):
    rel = rel.replace("\\", "/")
    if not rel.startswith("production/research/") or not rel.endswith(".md"):
        return False
    if re.search(r"(method|reading)", os.path.basename(rel), re.I):
        return False   # the research notes themselves, which the line points to
    return bool(NAME.search(os.path.basename(rel))) or rel.startswith("production/research/tool-tests-")


def has_line(text):
    return bool(LINE.search(text))


def existing_at_base():
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE, "production/research"],
                         cwd=REPO, capture_output=True, text=True)
    return set(out.stdout.split()) if out.returncode == 0 else None


def current_files():
    out = []
    root = os.path.join(REPO, "production", "research")
    for d, _dirs, names in os.walk(root):
        for n in names:
            out.append(os.path.relpath(os.path.join(d, n), REPO).replace("\\", "/"))
    return out


def selftest():
    cases = [
        ("a verdict file is judged", judged("production/research/x/SOME-VERDICT-2026-11-12.md"), True),
        ("a test file is judged", judged("production/research/x/VELLUM-TEST3-2026-11-12.md"), True),
        ("any file in a tool-tests folder", judged("production/research/tool-tests-2026-11/NOTES.md"), True),
        ("a reading note is not", judged("production/research/x/UE4SS-READING-2026-11-12.md"), False),
        ("a method note in a tool-tests folder is not", judged("production/research/tool-tests-2026-11/VELLUM-METHOD-2026-11-12.md"), False),
        ("outside research is not", judged("production/handover/TEST.md"), False),
        ("the line found", has_line("# T\n\nMethod researched: production/research/x/METHOD.md, 12 Nov\n"), True),
        ("the line in a list", has_line("- Method researched: SideFX docs, 12 Nov"), True),
        ("an empty line fails", has_line("Method researched: \n"), False),
        ("no line fails", has_line("# T\nnothing\n"), False),
    ]
    bad = [n for n, got, want in cases if got != want]
    print("method_line_check selftest:", "passed (%d cases)" % len(cases) if not bad else "FAILED " + ", ".join(bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    old = existing_at_base()
    if old is None:
        print("method_line_check: base commit %s not found, nothing judged" % BASE)
        return 0
    missing = []
    for rel in current_files():
        if rel in old or not judged(rel):
            continue
        with open(os.path.join(REPO, rel), encoding="utf-8", errors="replace") as fh:
            if not has_line(fh.read()):
                missing.append(rel)
    for m in missing:
        print("method_line_check FAIL %s has no 'Method researched: <file, date>' line (his rule, 12 Nov)" % m)
    print("method_line_check: %d new file(s) without the line" % len(missing))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
