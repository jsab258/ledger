#!/usr/bin/env python3
"""one-sim: do the lane's project files list the same sources as the originals?

  python -I compare_sources.py NAME LANE.json LANE_PREFIX ORIGINAL.json ORIGINAL_PREFIX
  python -I compare_sources.py --selftest DIR      (writes its small test lists into DIR)

The three check programs (PerceptionGolden, Soak, CoreTests) are built here from lane-written
project files, so that no build output lands under ledger/. That is only honest while each
lists exactly the sources its original lists (ledger/<NAME>/<NAME>.csproj). Each .json is
what `dotnet msbuild <project> -getItem:Compile` printed: MSBuild's own answer to "which files
does this project compile", globs and the folder's own files included. The two prefixes are
cut from the front of each path so that both lists name files from the repository's root.

Exit 0 the same list; 1 they differ (the names are printed); 3 a list could not be read or is empty.
"""
import json
import sys


def listed(path, prefix):
    with open(path, encoding="utf-8") as f:
        items = json.load(f)["Items"]["Compile"]
    out = set()
    for it in items:
        full = it["FullPath"].replace("\\", "/")
        out.add(full[len(prefix):] if full.startswith(prefix) else full)
    return out


def run(name, lane_json, lane_prefix, orig_json, orig_prefix, say=print):
    """-> exit code"""
    try:
        lane, orig = listed(lane_json, lane_prefix), listed(orig_json, orig_prefix)
    except (OSError, ValueError, KeyError) as e:
        say("NOTHING MEASURED: %s: a source list could not be read (%s)" % (name, e))
        return 3
    if not lane or not orig:
        say("NOTHING MEASURED: %s: an empty source list (lane %d files, original %d)" % (name, len(lane), len(orig)))
        return 3
    if lane == orig:
        say("ok   %s: the lane's project file lists the same %d sources as ledger/%s/%s.csproj" % (name, len(lane), name, name))
        return 0
    say("FAIL %s: the lane's project file and ledger/%s/%s.csproj list different sources" % (name, name, name))
    for f in sorted(lane - orig)[:20]:
        say("     only in the lane's list: " + f)
    for f in sorted(orig - lane)[:20]:
        say("     only in the original's list: " + f)
    return 1


def selftest(folder):
    """The comparison can fail: one file more, one file fewer, an empty list, a list that is no list."""
    import os

    def write(name, paths):
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"Items": {"Compile": [{"FullPath": p} for p in paths]}}, f)
        return path

    os.makedirs(folder, exist_ok=True)
    a = write("st-a.json", ["/lane/ledger/Core/A.cs", "/lane/ledger/Core/B.cs"])
    same = write("st-same.json", ["/view/ledger/Core/B.cs", "/view/ledger/Core/A.cs"])
    more = write("st-more.json", ["/view/ledger/Core/A.cs", "/view/ledger/Core/B.cs", "/view/ledger/Core/C.cs"])
    fewer = write("st-fewer.json", ["/view/ledger/Core/A.cs"])
    empty = write("st-empty.json", [])
    junk = os.path.join(folder, "st-junk.json")
    with open(junk, "w", encoding="utf-8") as f:
        f.write("not a list")
    quiet = lambda line: None
    cases = [
        ("the same files under two roots pass", run("T", a, "/lane/", same, "/view/", quiet) == 0),
        ("a file only the original lists fails", run("T", a, "/lane/", more, "/view/", quiet) == 1),
        ("a file only the lane lists fails", run("T", a, "/lane/", fewer, "/view/", quiet) == 1),
        ("an empty list is nothing measured", run("T", a, "/lane/", empty, "/view/", quiet) == 3),
        ("a list that cannot be read is nothing measured", run("T", a, "/lane/", junk, "/view/", quiet) == 3),
    ]
    for what, ok in cases:
        print("  %s %s" % ("ok  " if ok else "FAIL", what))
    bad = sum(1 for _, ok in cases if not ok)
    print("one-sim compare_sources selftest: passed=%d/%d" % (len(cases) - bad, len(cases)))
    return 4 if bad else 0


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--selftest":
        return selftest(sys.argv[2])
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    return run(*sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
