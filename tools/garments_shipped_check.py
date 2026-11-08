"""EVERY GARMENT IN THE PROJECT THAT SHIPS (n02-9-asset-check-gaps, 8 November 2026).

    python tools/garments_shipped_check.py             # production/specs/garments.json against the shipping project
    python tools/garments_shipped_check.py --selftest  # the rule on plain data

WHY. Only one MetaHuman project's folder reaches the packaged game: the build machine mirrors
C:/LedgerTools/mh-assemble/Content/Ledger/MetaHumans into its checkout (the workflow's metahumanCopied
step). An import into the dressing project on F: (mh-dress) succeeds, writes its report and changes
nothing in the game; it happened once and cost a night (the asset-import skill's review, 2 November;
memory: garments import into mh-assemble).

THE RULE. For each garment row in production/specs/garments.json:
  - SKM_<name>.uasset is in the shipping project's Garments/<name>/ folder (else MISSING);
  - it is not older than the row's source FBX on F: (else STALE: the source changed after the last import
    into the shipping project);
  - a copy in the dressing project newer than the shipping one is WRONG-PROJECT (the last import went to F:).
A source FBX that is not on this PC is skipped and named, never guessed. Without the shipping project
(another machine) the check says SKIP and fails nothing.

ONE LINE: garmentsShipped=PASS|FAIL|SKIP garments=<n> missing=<n> stale=<n> wrongProject=<n> first=<name>:<why>
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GARMENTS = os.path.join(REPO, "production", "specs", "garments.json")
SHIPPING = "C:/LedgerTools/mh-assemble/Content/Ledger/MetaHumans/Garments"
DRESSING = "F:/LedgerTools/mh-dress/Content/Ledger/MetaHumans/Garments"
SLACK_S = 120  # an import writes its uasset a little after reading the FBX; two minutes either way is the same import


def mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def judge(rows, shipped, dressed, sources):
    """rows: [(name, fbx)]; shipped/dressed/sources: name or path -> mtime or None. Returns findings [(name, why)]."""
    out = []
    for name, fbx in rows:
        s = shipped.get(name)
        if s is None:
            out.append((name, "missing"))
            continue
        d = dressed.get(name)
        if d is not None and d > s + SLACK_S:
            out.append((name, "wrong-project"))
            continue
        f = sources.get(fbx)
        if f is not None and f > s + SLACK_S:
            out.append((name, "stale"))
    return out


def line(rows, findings, skipped_sources):
    n = lambda w: sum(1 for _, why in findings if why == w)
    first = "%s:%s" % findings[0] if findings else "none"
    extra = (" sourceNotHere=%d" % len(skipped_sources)) if skipped_sources else ""
    return "garmentsShipped=%s garments=%d missing=%d stale=%d wrongProject=%d first=%s%s" % (
        "FAIL" if findings else "PASS", len(rows), n("missing"), n("stale"), n("wrong-project"), first, extra)


def main():
    if not os.path.isdir(SHIPPING):
        print("garmentsShipped=SKIP no shipping project on this PC (%s)" % SHIPPING)
        return 0
    with open(GARMENTS, encoding="utf-8") as fh:
        g = json.load(fh)["garments"]
    rows = [(r["name"], r.get("fbx", "")) for r in g]
    shipped = {n: mtime(os.path.join(SHIPPING, n, "SKM_%s.uasset" % n)) for n, _ in rows}
    dressed = {n: mtime(os.path.join(DRESSING, n, "SKM_%s.uasset" % n)) for n, _ in rows}
    sources = {f: mtime(f) for _, f in rows if f}
    skipped = [f for f, t in sources.items() if t is None]
    findings = judge(rows, shipped, dressed, sources)
    print(line(rows, findings, skipped))
    for name, why in findings:
        print("  %s: %s" % (name, why))
    return 1 if findings else 0


def selftest():
    ok = fail = 0

    def check(what, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print("garments_shipped selftest FAIL", what)

    rows = [("A", "a.fbx"), ("B", "b.fbx"), ("C", "c.fbx"), ("D", "d.fbx"), ("E", "")]
    shipped = {"A": 1000, "B": None, "C": 1000, "D": 1000, "E": 1000}
    dressed = {"A": 1050, "B": None, "C": 5000, "D": None, "E": None}
    sources = {"a.fbx": 900, "b.fbx": 900, "c.fbx": 900, "d.fbx": 4000}
    f = dict(judge(rows, shipped, dressed, sources))
    check("a fresh import inside the slack passes", "A" not in f)
    check("a garment absent from the shipping project is missing", f.get("B") == "missing")
    check("a newer copy in the dressing project is the wrong project", f.get("C") == "wrong-project")
    check("a source newer than the shipped import is stale", f.get("D") == "stale")
    check("a row with no source is judged on presence only", "E" not in f)
    check("a source not on this PC is skipped, never stale", judge([("X", "x.fbx")], {"X": 1}, {}, {"x.fbx": None}) == [])
    check("the line fails on any finding", line(rows, list(f.items()), []).startswith("garmentsShipped=FAIL"))
    check("the line passes clean", line(rows, [], []).startswith("garmentsShipped=PASS garments=5"))
    print("garments_shipped selftest: passed=%d/%d failed=%d" % (ok, ok + fail, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
