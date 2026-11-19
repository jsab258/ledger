"""The publish gate for the LEDGER loop prototype (task 4o; his decision of 18 Nov, 21:54).

Nothing is published to him unless this passes. Four parts:

  1. the scripted tests: the prototype's build check, Fable's tests and the lane's checks (run_proto_tests.py, pytest)
  2. the clumsy newcomer (clumsy.py): the experience rules as invariants, every failure with its steps
  3. the AI hands-on session: a fresh helper plays HANDS-ON-ROUTE.md through the real controls (prompt in
     HANDS-ON-PROMPT.md); its write-up is read here when given with --hands-on FILE
  4. the note for him (NOTE-TEMPLATE.md), filled from the numbers: what to try, the known issues, honestly

    python gate.py --assets DIR [--out DIR] [--known KNOWN.json] [--hands-on FILE] [--skip-scripted]

A round passes when the scripted tests pass, the clumsy newcomer shows no failure that is not in the known
list (KNOWN.json: rule names with the reason each is known and accepted for now), and the hands-on write-up
names no new fault marked "blocker". Exit code 0 means pass.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.join(os.path.dirname(HERE), "prototype")
sys.path.insert(0, HERE)


def scripted(assets, out):
    runs = []
    for name, cmd in [
        ("prototype tests", [sys.executable, os.path.join(PROTO, "run_proto_tests.py"), "--assets", assets, "--no-playtest"]),
        ("lane checks", [sys.executable, "-m", "pytest", "-q", os.path.join(PROTO, "tests")]),
        ("gate's own checks", [sys.executable, "-m", "pytest", "-q", os.path.join(HERE, "test_invariants.py"), os.path.join(HERE, "test_gate.py")]),
    ]:
        env = dict(os.environ, LEDGER_PROTO_ASSETS=assets)
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=3600)
        log = os.path.join(out, name.replace(" ", "-").replace("'", "") + ".log")
        with open(log, "w") as f:
            f.write(p.stdout + "\n" + p.stderr)
        runs.append({"part": name, "ok": p.returncode == 0, "log": log})
    return runs


def judge(clumsy_report, known, hands_on_text=None, scripted_runs=None):
    """Pure: decide pass or fail from the parts' results. Returns (ok, new_failures, known_failures, blockers)."""
    new, old = [], []
    for r in clumsy_report.get("results", []):
        if r["ok"]:
            continue
        (old if r["rule"] in known else new).append(r)
    blockers = []
    if hands_on_text:
        for line in hands_on_text.splitlines():
            low = line.lower()
            if "blocker" in low and "known blocker" not in low:
                blockers.append(line.strip())
    scripted_ok = all(s["ok"] for s in (scripted_runs or []))
    return scripted_ok and not new and not blockers, new, old, blockers


def note(clumsy_report, known, new, try_lines):
    """The short note for him: what to try, then the known issues in plain words."""
    lines = ["What to try:"] + ["- " + t for t in try_lines] + ["", "Known issues:"]
    seen = set()
    for r in clumsy_report.get("results", []):
        if r["ok"] or r["rule"] in seen:
            continue
        seen.add(r["rule"])
        why = known.get(r["rule"], "new, not yet fixed")
        lines.append("- %s (%s)" % (r["rule"], why))
    if not seen:
        lines.append("- none found by the gate")
    lines.append("Live AI talk only runs inside claude.ai: untested here.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), ".cache", "ledger-gate",
                                                   "gate-" + datetime.datetime.now().strftime("%Y%m%d-%H%M")))
    ap.add_argument("--known", default=os.path.join(HERE, "KNOWN.json"))
    ap.add_argument("--hands-on")
    ap.add_argument("--try", dest="try_lines", action="append", default=[])
    ap.add_argument("--skip-scripted", action="store_true")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    known = json.load(open(a.known)) if os.path.exists(a.known) else {}
    runs = [] if a.skip_scripted else scripted(a.assets, a.out)
    import clumsy
    clumsy.main(["--assets", a.assets, "--out", os.path.join(a.out, "clumsy")])
    rep = json.load(open(os.path.join(a.out, "clumsy", "report.json")))
    ho = open(a.hands_on).read() if a.hands_on else None
    ok, new, old, blockers = judge(rep, known, ho, runs)
    result = {"pass": bool(ok and ho), "scripted": runs, "new_failures": new, "known_failures": len(old), "hands_on_blockers": blockers,
              "hands_on_given": bool(ho)}
    with open(os.path.join(a.out, "GATE.json"), "w") as f:
        json.dump(result, f, indent=1)
    with open(os.path.join(a.out, "NOTE.md"), "w") as f:
        f.write(note(rep, known, new, a.try_lines or ["(the round's own change)"]))
    print("PASS" if ok else "FAIL", "-", len(new), "new failures,", len(old), "known,", len(blockers), "hands-on blockers")
    if not ho:
        print("hands-on write-up not given: the gate is not complete until it is (HANDS-ON-PROMPT.md)")
    return 0 if ok and ho else 1


if __name__ == "__main__":
    sys.exit(main())
