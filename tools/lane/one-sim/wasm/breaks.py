#!/usr/bin/env python3
"""one-sim: planted breaks. Do the front door's checks notice a changed rule?

  python -I breaks.py --repo REPO --work DIR --cxx WASM_CLANG++ [--json OUT.json]

Each break is ONE small change to a COPY of the port's files (made in DIR, never in the
repository): a step an hour late, a step dropped, two steps swapped, a routine an hour out.
The browser build is made from the changed copy and the front door's checks are run on it
(T2 routines, T3 the week hour by hour, both against the C# Core's rows). A break the checks
do not notice is printed as NOT SEEN: that is a finding about the checks, not a pass.
The untouched copy is built and checked first and must pass.

A measurement, not a gate: exit 0 when every break was planted and built, whatever was seen;
1 if the untouched copy fails or a break could not be planted (its text has moved).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

PUBLIC = "ue-probe/Source/LedgerProbe/Public"
PRIVATE = "ue-probe/Source/LedgerProbe/Private/Perception.cpp"
NINE = "Done.Went = NineReports(Mill, Cast, Now);"
ELLIS = "Done.Why = NineEllis(Mill, Now, Cast);"

# name, file, [(old, new), ...]: every old text must occur exactly once.
BREAKS = [
    ("witnesses go to the police at eight, not nine", "TownWeek.h",
     [("if (Now.Hour != 9 || DeedDay < 0 ||", "if (Now.Hour != 8 || DeedDay < 0 ||")]),
    ("the constable comes at eleven, not ten", "TownWeek.h",
     [("if (Now.Hour != 10 || Holding(Now)) return nullptr;", "if (Now.Hour != 11 || Holding(Now)) return nullptr;")]),
    ("Ron comes at nine in the evening, not eight", "TownWeek.h",
     [("if (Now.Hour != 20 || !Asks.AsksOn(Now.Day)", "if (Now.Hour != 21 || !Asks.AsksOn(Now.Day)")]),
    ("Ron's step is dropped from the hour", "TownWeek.h",
     [("Done.bRon = TwentyRon(Mill, Now);", "Done.bRon = false;")]),
    ("the week's end is never closed", "TownWeek.h",
     [("\t\t\tWeek.Close(Now, Mill, Cast);\n", "")]),
    ("DS Ellis's step runs before the witnesses' reports", "TownWeek.h",
     [(NINE, "@@SWAP@@"), (ELLIS, NINE), ("@@SWAP@@", ELLIS)]),
    ("routines run an hour out", "CastDay.h",
     [("const int H = ((Hour % 24) + 24) % 24;", "const int H = ((Hour % 24) + 25) % 24;")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--cxx", required=True)
    ap.add_argument("--golden", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(a.work, "breaks")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)

    def build_and_check(tag, edits_file=None, edits=()):
        src = os.path.join(base, tag)
        shutil.copytree(os.path.join(a.repo, PUBLIC), os.path.join(src, "Public"))
        if edits_file:
            path = os.path.join(src, "Public", edits_file)
            text = open(path, encoding="utf-8").read()
            for old, new in edits:
                if text.count(old) != 1:
                    return "not planted", "text found %d times: %r" % (text.count(old), old[:50])
                text = text.replace(old, new)
            open(path, "w", encoding="utf-8", newline="").write(text)
        wasm = os.path.join(src, "one-sim.wasm")
        cmd = ["nice", "-n", "15", a.cxx, "-std=c++17", "-O2", "-w", "-fno-exceptions", "-DLEDGER_CORE_NO_EXCEPTIONS=1",
               "-mexec-model=reactor", "-I", os.path.join(src, "Public"), "-I", os.path.join(a.repo, "ue-probe/tests/unreal-shim"),
               "-o", wasm, os.path.join(here, "one_sim.cpp"), os.path.join(a.repo, PRIVATE)]
        b = subprocess.run(cmd, capture_output=True, text=True)
        if b.returncode != 0:
            return "not built", b.stderr[-300:]
        out = os.path.join(src, "report.json")
        subprocess.run(["nice", "-n", "15", "node", "--no-warnings", os.path.join(here, "test_one_sim.mjs"), "--bridge-only", "--brain", wasm,
                        "--golden", a.golden, "--specs", os.path.join(a.repo, "production/specs"), "--json", out],
                       capture_output=True, text=True)
        r = json.load(open(out, encoding="utf-8"))
        seen = [x["name"].split(" ")[0] for x in r["results"] if not x["ok"]]
        detail = "T2 %d of %d places wrong, T3 %d of %d hours wrong" % (r["T2"]["bad"], r["T2"]["rows"], r["T3"]["bad"], r["T3"]["rows"])
        return ("seen by " + "+".join(seen)) if seen else "NOT SEEN", detail

    verdict, detail = build_and_check("untouched")
    print("[0] the untouched copy: %s (%s)" % ("passes" if verdict == "NOT SEEN" else verdict, detail))
    if verdict != "NOT SEEN":
        print("breaks: the untouched copy does not pass, so nothing below would mean anything")
        return 1
    rows, bad = [], 0
    for i, (name, f, edits) in enumerate(BREAKS, 1):
        verdict, detail = build_and_check("break%d" % i, f, edits)
        if verdict.startswith("not "):
            bad += 1
        rows.append({"break": name, "file": f, "verdict": verdict, "detail": detail})
        print("[%d] %s (%s): %s; %s" % (i, name, f, verdict, detail))
    seen = sum(1 for r in rows if r["verdict"].startswith("seen"))
    print("breaks: %d of %d planted one-line breaks were seen by the front door's checks" % (seen, len(rows)))
    if a.json:
        json.dump({"seen": seen, "planted": len(rows), "rows": rows}, open(a.json, "w", encoding="utf-8"), indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
