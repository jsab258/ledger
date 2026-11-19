#!/usr/bin/env python3
"""one-sim: is it the same town in Node and in the real browser?

  python -I engines_agree.py NODE_REPORT.json BROWSER_REPORT.json
  python -I engines_agree.py --selftest

T4 inside one engine can hardly fail: the loader answers the clock and the random numbers
with zero, so two runs in the same engine have nothing to differ by. The real test is across
engines: the digest of every scripted hour, the final state and every held story, as Node
worked it out, against the same digest as the page in Chromium worked it out. Both reports
come from the same checks file (checks.mjs) reading the same table; the table's own digest is
compared first, so a difference in the table is never mistaken for a difference in the town.

Exit 0 the same; 1 they differ (both are printed); 3 nothing measured (a report is missing).
"""
import json
import sys


def compare(node, page):
    """-> (exit code, line)"""
    for name, r in (("Node", node), ("the browser", page)):
        if not isinstance(r, dict) or "T4" not in r or "table" not in r:
            return 3, "NOTHING MEASURED: the report from %s holds no T4 digest" % name
    if node["table"].get("sha256") != page["table"].get("sha256"):
        return 1, "FAIL T4x Node and the browser read different tables (%s and %s), so their towns cannot be compared" % (
            node["table"].get("sha256"), page["table"].get("sha256"))
    a, b = node["T4"].get("first"), page["T4"].get("first")
    where = page.get("browser", "the browser")
    if not a or not b:
        return 3, "NOTHING MEASURED: an empty T4 digest (Node %r, %s %r)" % (a, where, b)
    if a != b:
        return 1, "FAIL T4x the same calls give a different town in Node (%s) and in %s (%s)" % (a, where, b)
    # The bridge's weeks too (T9's digest), when both reports carry one.
    c, d = (node.get("bridge") or {}).get("digest"), (page.get("bridge") or {}).get("digest")
    if (c or d) and c != d:
        return 1, "FAIL T4x the bridge's weeks give a different town in Node (%s) and in %s (%s)" % (c, where, d)
    return 0, "ok   T4x the same town in Node and in %s: digest %s in both%s (the same %d rows of table, %s)" % (
        where, a, ", and the bridge's weeks %s in both" % c if c else "", node["table"].get("rows", 0), node["table"].get("sha256"))


def selftest():
    good = {"table": {"sha256": "aa", "rows": 3}, "T4": {"first": "1234", "second": "1234"}}
    cases = [
        ("the same digest passes", compare(good, dict(good, browser="Chromium 1"))[0] == 0),
        ("a different digest fails", compare(good, dict(good, T4={"first": "9999"}))[0] == 1),
        ("the same bridge digest passes", compare(dict(good, bridge={"digest": "77"}), dict(good, bridge={"digest": "77"}))[0] == 0),
        ("a different bridge digest fails", compare(dict(good, bridge={"digest": "77"}), dict(good, bridge={"digest": "78"}))[0] == 1),
        ("a bridge digest on one side only fails", compare(dict(good, bridge={"digest": "77"}), good)[0] == 1),
        ("a different table fails", compare(good, dict(good, table={"sha256": "bb"}))[0] == 1),
        ("a report with no T4 is nothing measured", compare(good, {"table": {"sha256": "aa"}})[0] == 3),
        ("an empty digest is nothing measured", compare(good, dict(good, T4={"first": ""}))[0] == 3),
    ]
    for what, ok in cases:
        print("  %s %s" % ("ok  " if ok else "FAIL", what))
    bad = sum(1 for _, ok in cases if not ok)
    print("one-sim engines_agree selftest: passed=%d/%d" % (len(cases) - bad, len(cases)))
    return 4 if bad else 0


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    reports = []
    for path in sys.argv[1:]:
        try:
            with open(path, encoding="utf-8") as f:
                reports.append(json.load(f))
        except (OSError, ValueError) as e:
            print("NOTHING MEASURED: %s could not be read (%s). Run test and browser first." % (path, e))
            return 3
    code, line = compare(*reports)
    print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
