#!/usr/bin/env python3
"""NOTHING NEW AT C:'S ROOT: BEFORE AND AFTER EVERY TOOL-LOOP ROUND (advisor 163, 14 November 2026).

    python tools/c_root_guard.py check     # one line: C-ROOT OK, or C-ROOT NEW: names (fails the round, exit 1)
    python tools/c_root_guard.py accept    # record the root as it stands now (only after his yes or a cleanup)
    python tools/c_root_guard.py --selftest

WHY: seven picture folders (a2, r4, diag, base, tube0, pics, closeups) appeared at C:'s root on 13 and 14 November,
written by fixers' Blender runs given relative output paths; nobody noticed until he saw them. The known list lives in
production/handover/c-root.json with C:'s free space; anything at the root not on it fails the round and is named in
its report. Free space is printed beside it (a fall of more than 1 GB in a round is said too).
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "production", "handover", "c-root.json")
DRIVE = "C:\\"


def listing(drive=DRIVE):
    return sorted(os.listdir(drive))


def free_gb(drive=DRIVE):
    return round(shutil.disk_usage(drive).free / 1e9, 1)


def compare(known, now, free_before=None, free_now=None):
    new = sorted(set(now) - set(known))
    line = ("C-ROOT NEW: %s (advisor 163: fails the round; name it in the report)" % ", ".join(new)) if new else "C-ROOT OK"
    if free_before is not None and free_now is not None:
        line += "; C: %.1f GB free (%+.1f since recorded)" % (free_now, free_now - free_before)
        if free_before - free_now > 1.0:
            line += " FELL OVER 1 GB"
    return line, bool(new)


def main(a):
    if "--selftest" in a:
        cases = [("nothing new", compare(["Users", "Windows"], ["Users", "Windows"])[1], False),
                 ("a new folder fails", compare(["Users"], ["Users", "closeups"])[1], True),
                 ("a gone folder is fine", compare(["Users", "pics"], ["Users"])[1], False),
                 ("names the new one", "closeups" in compare(["Users"], ["Users", "closeups"])[0], True),
                 ("a 2 GB fall is said", "FELL" in compare([], [], 80.0, 78.0)[0], True),
                 ("a small fall is not", "FELL" in compare([], [], 80.0, 79.5)[0], False)]
        bad = [n for n, got, want in cases if got != want]
        print("c_root_guard selftest:", "passed (%d cases)" % len(cases) if not bad else "FAILED " + ", ".join(bad))
        return 1 if bad else 0
    if "accept" in a:
        json.dump({"root": listing(), "freeGB": free_gb()}, open(STATE, "w", encoding="utf-8"), indent=1)
        print("C-ROOT recorded: %d names, %.1f GB free" % (len(listing()), free_gb()))
        return 0
    s = json.load(open(STATE, encoding="utf-8"))
    line, bad = compare(s["root"], listing(), s.get("freeGB"), free_gb())
    print(line)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
