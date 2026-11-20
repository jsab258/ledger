"""The publish gate for the LEDGER loop prototype (task 4o; his decision of 18 Nov, 21:54).

Nothing is published to him unless this passes. Four parts:

  1. the scripted tests: the prototype's build check, Fable's tests and the lane's checks (run_proto_tests.py, pytest)
  2. the clumsy newcomer (clumsy.py): the experience rules as invariants, every failure with its steps
  3. the AI hands-on session: a fresh helper plays HANDS-ON-ROUTE.md through the real controls (prompt in
     HANDS-ON-PROMPT.md); its write-up is read here when given with --hands-on FILE
  4. the note for him (NOTE-TEMPLATE.md), filled from the numbers: what to try, the known issues, honestly
  5. the machine checks (machine_checks.py, lane task 4t piece 1): rules every game hour, save and reload, never
     stuck, camera never inside a wall, frame rate against the accepted build, the content words; code, no model
  6. the consequence checker (consequences.py, piece 5): every memory traced back through its tellings to the act,
     every reaction to a memory, no line repeated, nothing wrong for 1990, the content words in what is shown

    python gate.py --assets DIR [--out DIR] [--known KNOWN.json] [--hands-on FILE] [--skip-scripted]
                   [--skip-machine] [--machine-hours 24]

A round passes when the scripted tests pass, the clumsy newcomer shows no failure that is not in the known
list (KNOWN.json: "rule | what it was about" keys, as signature() writes them, with the reason each is known and
accepted for now), the machine checks show no failure that is not in the same known list (keyed the same way,
the rule plus the named place), and the hands-on write-up is given and names no new fault marked BLOCKER or MAJOR. Exit code 0
means pass.
"""
import argparse
import datetime
import json
import os
import re
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
        ("gate's own checks", [sys.executable, "-m", "pytest", "-q", os.path.join(HERE, "test_invariants.py"), os.path.join(HERE, "test_gate.py"), os.path.join(HERE, "test_consequences.py")]),
    ]:
        env = dict(os.environ, LEDGER_PROTO_ASSETS=assets)
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=3600)
        log = os.path.join(out, name.replace(" ", "-").replace("'", "") + ".log")
        with open(log, "w") as f:
            f.write(p.stdout + "\n" + p.stderr)
        runs.append({"part": name, "ok": p.returncode == 0, "log": log})
    return runs


SIGNATURE_KEYS = ("phase", "target", "prop", "room", "where", "person", "place")
FAULT_LINE = re.compile(r"^\W*(known\s+)?(blocker|major)\b\s*[:\-]", re.I)


def signature(r):
    """A failure's key in KNOWN.json: the rule plus what it was about (the phase, the target, the room...), so one
    accepted fault never hides a new fault of the same rule somewhere else."""
    for k in SIGNATURE_KEYS:
        if r.get(k):
            return "%s | %s" % (r["rule"], r[k])
    return r["rule"]


def hands_on_faults(text):
    """The BLOCKER and MAJOR lines of the hands-on write-up that are not marked known. A line counts only when it
    starts with the marker ("BLOCKER: ...", "- MAJOR - ..."), so "No blockers" and "unknown" are never misread."""
    out = []
    for line in (text or "").splitlines():
        m = FAULT_LINE.match(line)
        if m and not m.group(1):
            out.append(line.strip())
    return out


def judge(clumsy_report, known, hands_on_text=None, scripted_runs=None, machine_report=None):
    """Pure: decide pass or fail from the parts' results. Returns (ok, new_failures, known_failures, blockers).
    Without the hands-on write-up the gate never passes. New BLOCKER and MAJOR faults from it both block.
    A machine check that was asked for but gave no report (machine_report == {}) is itself a new failure."""
    new, old = [], []
    machine = []
    if machine_report is not None:
        machine = [dict(r, source=r.get("source", "machine")) for r in machine_report.get("results", [])]
        if not any(r["source"] == "machine" for r in machine):
            machine += [{"rule": "machine checks ran", "ok": False, "source": "machine", "steps": "not reached: no report"}]
    for r in clumsy_report.get("results", []) + machine:
        if r["ok"] or r["ok"] is None:  # None: a rule with nothing to check this time; listed in the note, never a pass
            continue
        (old if signature(r) in known else new).append(r)
    blockers = hands_on_faults(hands_on_text)
    if not (hands_on_text or "").strip():
        blockers.append("no hands-on write-up given (HANDS-ON-PROMPT.md)")
    scripted_ok = all(s["ok"] for s in (scripted_runs or []))
    return scripted_ok and not new and not blockers, new, old, blockers


def note(clumsy_report, known, new, try_lines, machine_report=None):
    """The short note for him: what to try, then the known issues in plain words."""
    lines = ["What to try:"] + ["- " + t for t in try_lines] + ["", "Known issues:"]
    seen = set()
    for r in clumsy_report.get("results", []) + (machine_report or {}).get("results", []):
        if r["ok"] or r["ok"] is None or signature(r) in seen:
            continue
        seen.add(signature(r))
        why = known.get(signature(r), "new, not yet fixed")
        lines.append("- %s (%s)" % (signature(r), why))
    if not seen:
        lines.append("- none found by the gate")
    unreached = sorted(set(r["rule"] for r in (machine_report or {}).get("results", []) if r.get("ok") is None))
    if unreached:
        lines += ["", "Not reached this time (nothing to check, so not passed): " + "; ".join(unreached)]
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
    ap.add_argument("--skip-machine", action="store_true", help="only for the gate's own tests; a real round never skips it")
    ap.add_argument("--machine-hours", type=int, default=24)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    known = json.load(open(a.known)) if os.path.exists(a.known) else {}
    runs = [] if a.skip_scripted else scripted(a.assets, a.out)
    import clumsy
    clumsy.main(["--assets", a.assets, "--out", os.path.join(a.out, "clumsy")])
    rep = json.load(open(os.path.join(a.out, "clumsy", "report.json")))
    mrep = None
    if not a.skip_machine:
        mpath = os.path.join(a.out, "machine", "machine.json")  # always this build's own run: no old report is taken
        if os.path.exists(mpath):
            os.remove(mpath)
        import machine_checks
        try:
            machine_checks.main(["--assets", a.assets, "--out", os.path.join(a.out, "machine"),
                                 "--hours", str(a.machine_hours)])
        except Exception as e:  # noqa: BLE001 - a check that breaks is itself a finding
            print("machine checks broke:", str(e)[:300])
        mrep = json.load(open(mpath)) if os.path.exists(mpath) else {}
        # piece 5, the consequence checker's own run (code, no model): its faults count like the machine checks'
        cpath = os.path.join(a.out, "consequences", "consequences.json")
        if os.path.exists(cpath):
            os.remove(cpath)
        import consequences
        try:
            consequences.main(["--assets", a.assets, "--out", os.path.dirname(cpath), "--hours", str(a.machine_hours)])
        except Exception as e:  # noqa: BLE001
            print("consequence checker broke:", str(e)[:300])
        crep = json.load(open(cpath)) if os.path.exists(cpath) else {}
        cres = [dict(r, source="consequences") for r in crep.get("results", [])] or [
            {"rule": "consequence checker ran", "ok": False, "source": "consequences", "steps": "not reached: no report"}]
        mrep["results"] = mrep.get("results", []) + cres  # kept even when the machine checks gave no report
    ho = open(a.hands_on).read() if a.hands_on else None
    ok, new, old, blockers = judge(rep, known, ho, runs, mrep)
    ok = ok and mrep is not None  # a gate run with the machine checks skipped never passes
    result = {"pass": bool(ok), "scripted": runs, "machine_checked": mrep is not None, "new_failures": new, "known_failures": len(old), "hands_on_blockers": blockers,
              "hands_on_given": bool(ho)}
    with open(os.path.join(a.out, "GATE.json"), "w") as f:
        json.dump(result, f, indent=1)
    with open(os.path.join(a.out, "NOTE.md"), "w") as f:
        f.write(note(rep, known, new, a.try_lines or ["(the round's own change)"], mrep))
    print("PASS" if ok else "FAIL", "-", len(new), "new failures,", len(old), "known,", len(blockers), "hands-on blockers")
    if mrep is None:
        print("machine checks skipped: not a real round's gate")
    if not ho:
        print("hands-on write-up not given: the gate is not complete until it is (HANDS-ON-PROMPT.md)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
