#!/usr/bin/env python3
"""EVERY FOLDER OF ART AND RESEARCH HAS A LINE IN THE CATALOGUE, OR THE BUILD FAILS.

Jafar, 5 October 2026 (the plan's edits 9 and 10): "A short catalogue of what exists, maps,
district plans, concept images, research topics and approved assets" and "rules alone have not
held; checks that fail loudly have ... anything new in the art or research folders without a
catalogue line". On 4 October a district map was drawn from nothing while the September atlas
sat on a branch nobody knew about. CATALOGUE.md at the root is the catalogue; this fails when a
folder or file directly under production/art or production/research is not named in it, and
when the catalogue names one that no longer exists there.

  python tools/catalogue.py              # exit 1 naming each missing or stale entry
  python tools/catalogue.py --selftest
"""
import io
import os
import re
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHED = ("production/art", "production/research")


def named(text, name):
    return re.search(r"(?<![\w.-])" + re.escape(name) + r"(?![\w-])", text) is not None


def check(root=REPO, out=sys.stdout):
    path = os.path.join(root, "CATALOGUE.md")
    if not os.path.exists(path):
        print("catalogue FAIL CATALOGUE.md is missing", file=out)
        return 1
    text = io.open(path, encoding="utf-8").read()
    missing, seen = [], 0
    for base in WATCHED:
        full = os.path.join(root, base)
        if not os.path.isdir(full):
            print("catalogue FAIL %s is missing: nothing measured must never read as clean" % base, file=out)
            return 1
        for name in sorted(os.listdir(full)):
            if name.startswith("."):
                continue
            seen += 1
            if not named(text, name):
                missing.append("%s/%s" % (base, name))
    stale = []
    for line in text.splitlines():
        if line.startswith("- **") and "**:" in line and any(w in line for w in ("The street and its look", "The town and its people", "Talk and voices", "People on screen", "Play, testing", "How the work is done")):
            for item in line.split("**:", 1)[1].split(","):
                name = item.strip().split(" (")[0].rstrip(".").strip()
                if name and not os.path.exists(os.path.join(root, "production", "research", name)):
                    stale.append("production/research/" + name)
    for m in missing:
        print("catalogue FAIL no catalogue line for %s" % m, file=out)
    for s in stale:
        print("catalogue FAIL the catalogue names %s, which does not exist" % s, file=out)
    print("catalogue entries=%d missing=%d stale=%d outcome=%s" % (seen, len(missing), len(stale), "FAIL" if missing or stale else "PASS"), file=out)
    return 1 if missing or stale else 0


def selftest():
    ok = True

    def t(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    d = tempfile.mkdtemp()
    for base in WATCHED:
        os.makedirs(os.path.join(d, base))
    os.makedirs(os.path.join(d, "production/research/rumours"))
    os.makedirs(os.path.join(d, "production/art/atlas-01"))
    cat = "# CATALOGUE\n\n- atlas-01: the map.\n\n## Research\n\n- **Talk and voices**: rumours.\n"
    io.open(os.path.join(d, "CATALOGUE.md"), "w", encoding="utf-8").write(cat)
    sink = io.StringIO()
    t(check(d, sink) == 0, "every folder named passes")
    os.makedirs(os.path.join(d, "production/art/district-map"))
    t(check(d, sink) == 1, "a new art folder with no line fails")
    io.open(os.path.join(d, "CATALOGUE.md"), "w", encoding="utf-8").write(cat.replace("atlas-01: the map.", "atlas-01, district-map: maps.").replace("rumours.", "rumours, gone-topic."))
    t(check(d, sink) == 1, "a research topic the catalogue names but the folder lacks fails")
    t(named("atlas-01-old", "atlas-01") is False and named("(atlas-01)", "atlas-01"), "a name inside a longer name does not count")
    print("catalogue selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
