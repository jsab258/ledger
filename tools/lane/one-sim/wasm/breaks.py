#!/usr/bin/env python3
"""one-sim: planted breaks. Does anything notice a changed rule?

  python -I breaks.py --repo REPO --work DIR --cxx WASM_CLANG++ --golden TABLE [--json OUT.json]

Each break is ONE small change to a COPY of the port's files (made in DIR, never in the
repository): a step an hour late, a step dropped, two steps swapped, a routine an hour out.
Both browser builds are made from the changed copy (the brain, and the check build that can
answer any row of the table) and ALL the checks are run on them: T1, every row of the C#
Core's golden table, and the front door's own (T2 routines, T3 the week hour by hour, and
the rest). Each break is printed with three counts: rows of the whole table that differ
(T1), places wrong (T2), hours wrong (T3). A break nothing notices is printed as NOT SEEN:
that is a finding about the table and the checks, not a pass.
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
        check = os.path.join(src, "one-sim-check.wasm")
        # The same flags as one-sim.sh wasm: the brain, and the check build (the brain plus the golden reader).
        for target, extra in ((wasm, []), (check, ["-DONE_SIM_CHECK=1"])):
            cmd = ["nice", "-n", "15", a.cxx, "-std=c++17", "-O2", "-w", "-fno-exceptions", "-DLEDGER_CORE_NO_EXCEPTIONS=1",
                   "-mexec-model=reactor"] + extra + ["-I", os.path.join(src, "Public"), "-I", os.path.join(a.repo, "ue-probe/tests/unreal-shim"),
                   "-o", target, os.path.join(here, "one_sim.cpp"), os.path.join(a.repo, PRIVATE)]
            b = subprocess.run(cmd, capture_output=True, text=True)
            if b.returncode != 0:
                return "not built", b.stderr[-300:], None
        out = os.path.join(src, "report.json")
        if os.path.exists(out):
            os.remove(out)
        subprocess.run(["nice", "-n", "15", "node", "--no-warnings", os.path.join(here, "test_one_sim.mjs"), "--brain", wasm, "--check", check,
                        "--golden", a.golden, "--specs", os.path.join(a.repo, "production/specs"), "--json", out],
                       capture_output=True, text=True)
        if not os.path.exists(out):
            return "not run", "the checks wrote no report", None
        r = json.load(open(out, encoding="utf-8"))
        seen = [x["name"].split(" ")[0] for x in r["results"] if not x["ok"]]
        t1 = r["T1"]
        counts = {"T1": t1["mismatch"] + t1["unknown"] + t1["short"], "T1rows": t1["ok"] + t1["mismatch"] + t1["unknown"] + t1["short"],
                  "T2": r["T2"]["bad"], "T2rows": r["T2"]["rows"], "T3": r["T3"]["bad"], "T3rows": r["T3"]["rows"]}
        detail = "T1 %d of %d rows of the whole table differ, T2 %d of %d places wrong, T3 %d of %d hours wrong" % (
            counts["T1"], counts["T1rows"], counts["T2"], counts["T2rows"], counts["T3"], counts["T3rows"])
        return ("seen by " + "+".join(seen)) if seen else "NOT SEEN", detail, counts

    verdict, detail, _ = build_and_check("untouched")
    print("[0] the untouched copy: %s (%s)" % ("passes" if verdict == "NOT SEEN" else verdict, detail), flush=True)
    if verdict != "NOT SEEN":
        print("breaks: the untouched copy does not pass, so nothing below would mean anything")
        return 1
    rows, bad = [], 0
    for i, (name, f, edits) in enumerate(BREAKS, 1):
        verdict, detail, counts = build_and_check("break%d" % i, f, edits)
        if verdict.startswith("not "):
            bad += 1
        rows.append({"break": name, "file": f, "verdict": verdict, "detail": detail, "counts": counts})
        print("[%d] %s (%s): %s; %s" % (i, name, f, verdict, detail), flush=True)
    planted = [r for r in rows if r["counts"]]
    seen = sum(1 for r in planted if r["verdict"].startswith("seen"))
    by_table = sum(1 for r in planted if r["counts"]["T1"] > 0)
    by_door = sum(1 for r in planted if r["counts"]["T2"] > 0 or r["counts"]["T3"] > 0)
    print("breaks: of %d planted one-line breaks, %d fail a row of the whole table (T1), %d fail the front door's routines or week (T2, T3), "
          "%d are seen by nothing" % (len(planted), by_table, by_door, len(planted) - seen))
    if a.json:
        json.dump({"seen": seen, "seen_by_whole_table": by_table, "seen_by_front_door": by_door, "planted": len(planted), "rows": rows},
                  open(a.json, "w", encoding="utf-8"), indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
