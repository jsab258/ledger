#!/usr/bin/env python3
"""A COPY THAT DISAGREES WITH ITS HOME FAILS THE BUILD, UNLESS THE DISAGREEMENT IS KNOWN AND LISTED.

Jafar, 5 October 2026 (the plan's edits 9 and 10): "One home for every kind of fact ... Everything
else is derived from its home and checked against it" and "a derived thing that disagrees with
its home" fails the build. The homes are CATALOGUE.md's table. This compares the pairs a script
can compare today:

  walkers    every figure on the street (production/specs/street-people.json) stands for a
             resident (production/specs/hook-cast.json, the Core's people) or is ruled scenery;
  plan       NOW.md's phases are PLAN.md's phases, by number and name;
  atlas      once the atlas is in main (production/art/atlas-01/data/atlas.json), its street
             (length, road, pavements, the yard gap, Mickey's place) is the built street's
             (production/specs/vignette-scene.json).
The port against the Core is compared by tools/port-golden-check.sh, the pieces against the
scene by CoreTests.

A disagreement already listed in CATALOGUE.md is recorded in production/homes-known.json with
when it is meant to end; the check fails on any disagreement not recorded there, and on a
recorded one that has ended (so the list never goes stale).

  python tools/homes_check.py
  python tools/homes_check.py --selftest
"""
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel, root=REPO):
    with io.open(os.path.join(root, rel), encoding="utf-8") as f:
        return json.load(f)


def walkers(root=REPO):
    people = load("production/specs/street-people.json", root)
    residents = {p["id"] for p in load("production/specs/hook-cast.json", root)["people"]}
    replaced = {c["replaces"]: c["id"] for c in people.get("cast", [])}
    out = []
    for p in people["people"]:
        g = p["glb"]
        who = p.get("resident") or replaced.get(g)
        if who and who in residents:
            continue
        if p.get("scenery"):
            continue
        out.append("walker-without-resident:%s" % g)
    for c in people.get("cast", []):
        if c["id"] not in residents:
            out.append("cast-not-a-resident:%s" % c["id"])
    return out


def plan(root=REPO):
    now = io.open(os.path.join(root, "NOW.md"), encoding="utf-8").read()
    pl = io.open(os.path.join(root, "PLAN.md"), encoding="utf-8").read()
    phases = {m.group(1): m.group(2).strip().lower() for m in re.finditer(r"^\*\*(\d)\. ([^.*]+)\.\*\*", pl, re.M)}
    out = []
    for m in re.finditer(r"^## Phase (\d): ([^(]+)", now, re.M):
        n, name = m.group(1), m.group(2).strip().lower()
        if n not in phases:
            out.append("now-phase-not-in-plan:%s" % n)
        elif name != phases[n]:
            out.append("now-phase-name:%s" % n)
    return out


def atlas(root=REPO):
    path = "production/art/atlas-01/data/atlas.json"
    if not os.path.exists(os.path.join(root, path)):
        return []
    a = load(path, root)["street_anchor"]
    s = load("production/specs/vignette-scene.json", root)
    st = s["street"]
    blocks = {b["id"]: b for b in s["blocks"]}
    ws, wn, ep = blocks["west_south"], blocks["west_north"], blocks["east_parade"]
    built = {
        "length": st["length_m"],
        "carriageway": 2 * st["carriageway"]["half_width_m"],
        "footway": st["footway"]["width_m"],
        "yard-gap": [ws["start_x_m"] + ws["bays"] * ws["bay_width_m"], wn["start_x_m"]],
        "mickeys-x": [ep["start_x_m"], ep["start_x_m"] + ep["bay_width_m"]],
    }
    theirs = {"length": a["length_m"], "carriageway": a["carriageway_m"], "footway": a["footway_each_m"],
              "yard-gap": a["yard_gap_x"], "mickeys-x": a["mickeys_x_range"]}
    return ["atlas-street:%s" % k for k in theirs if not _same(theirs[k], built[k])]


def _same(a, b):
    if isinstance(a, list):
        return len(a) == len(b) and all(abs(float(x) - float(y)) < 1e-6 for x, y in zip(a, b))
    return abs(float(a) - float(b)) < 1e-6


def check(root=REPO, out=sys.stdout):
    found = set(walkers(root) + plan(root) + atlas(root))
    known_path = os.path.join(root, "production", "homes-known.json")
    known = {k["key"]: k for k in load("production/homes-known.json", root)["known"]} if os.path.exists(known_path) else {}
    new = sorted(found - set(known))
    ended = sorted(set(known) - found)
    for k in new:
        print("homes FAIL a copy disagrees with its home and the disagreement is not listed: " + k, file=out)
    for k in ended:
        print("homes FAIL a listed disagreement has ended; take it off production/homes-known.json: " + k, file=out)
    print("homes disagreements=%d known=%d new=%d ended=%d outcome=%s" % (len(found), len(known), len(new), len(ended), "FAIL" if new or ended else "PASS"), file=out)
    return 1 if new or ended else 0


def selftest():
    import tempfile
    ok = True

    def t(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "production", "specs"))
    w = lambda rel, obj: io.open(os.path.join(d, rel), "w", encoding="utf-8").write(json.dumps(obj) if not isinstance(obj, str) else obj)
    w("production/specs/hook-cast.json", {"people": [{"id": "rocco"}, {"id": "hana"}]})
    w("production/specs/street-people.json", {"people": [{"glb": "joe"}, {"glb": "martha"}, {"glb": "bin-man", "scenery": "a ruling"}], "cast": [{"id": "rocco", "replaces": "joe"}]})
    w("NOW.md", "GOAL\n\n## Phase 0: recover control (0.20W)\n")
    w("PLAN.md", "**0. Recover control.** Ceiling\n")
    t(walkers(d) == ["walker-without-resident:martha"], "a figure with no resident is found; a cast member and ruled scenery are not")
    t(plan(d) == [], "NOW.md's phase matches PLAN.md's")
    w("NOW.md", "## Phase 0: something else (x)\n")
    t(plan(d) == ["now-phase-name:0"], "a phase renamed in NOW.md alone is found")
    w("NOW.md", "## Phase 0: recover control (0.20W)\n")
    sink = io.StringIO()
    t(check(d, sink) == 1, "an unlisted disagreement fails")
    w("production/homes-known.json", {"known": [{"key": "walker-without-resident:martha"}]})
    t(check(d, sink) == 0, "a listed one passes")
    w("production/specs/street-people.json", {"people": [{"glb": "joe"}], "cast": [{"id": "rocco", "replaces": "joe"}]})
    t(check(d, sink) == 1, "a listed one that has ended fails until it is taken off the list")
    print("homes_check selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
