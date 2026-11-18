#!/usr/bin/env python3
"""Make the one file a panel reviewer sees: the playtester's record of one build, and nothing else.

Usage: python packet.py PLAYTEST_DIR OUT.md [--label "build of 18 Nov 12:00"]
PLAYTEST_DIR holds the playtester's newcomer.md, sweep.md and transcripts.md (and report.json when there).
Lines that speak of our own intentions are left out: only what was played, said and measured goes in.
"""
import argparse
import json
import os
import re

DROP = re.compile(r"objective|design|canon|ruling|intended|on purpose|Fable|lane|advisor", re.I)


def read(path):
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def make(d, label):
    nc, sw, tr = read(os.path.join(d, "newcomer.md")), read(os.path.join(d, "sweep.md")), read(os.path.join(d, "transcripts.md"))
    rep = {}
    if os.path.exists(os.path.join(d, "report.json")):
        rep = json.load(open(os.path.join(d, "report.json"), encoding="utf-8"))
    L = ["# What a tester recorded playing one build of a game (%s)" % label, "",
         "An automated tester played the first hour as a newcomer would (walking up to people, talking, taking work when offered), "
         "then walked up to every person at four times of day. Below: the share of time spent on each thing, when something new "
         "appeared, tense moments, faults it saw on screen, and the full talk transcripts. Times are estimates of a human's pace.", ""]
    for line in nc.splitlines():
        if line.startswith("# "):
            continue
        if DROP.search(line):
            line = re.sub(r"toDo=.*", "", line)
            if DROP.search(line):
                continue
        L.append(line)
    if "## Tense moments" not in nc:
        L += ["", "## Tense moments", "", "- not counted for this build"]
    L += ["", "# The walk-up sweep", ""] + [l for l in sw.splitlines() if not l.startswith("# ") and not DROP.search(l)]
    L += ["", "# Transcripts (first hour)", ""] + [l for l in tr.splitlines() if not l.startswith("# ")]
    if rep.get("errors"):
        L += ["", "## Page errors", ""] + ["- " + str(e)[:200] for e in rep["errors"][:10]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("out")
    ap.add_argument("--label", default="one build")
    a = ap.parse_args()
    open(a.out, "w", encoding="utf-8").write(make(a.dir, a.label))
    print("packet written:", a.out)
