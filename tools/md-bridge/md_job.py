#!/usr/bin/env python3
"""Hand one job to Marvelous Designer through LEDGER's bridge and wait for its result.

    python tools/md-bridge/md_job.py JOB.py [--timeout 600]   # prints the result JSON; exit 1 on failure
    python tools/md-bridge/md_job.py --alive                  # is the bridge running? (exit 1 if not)
    python tools/md-bridge/md_job.py --selftest

The bridge (tools/md-bridge/ledger_md_bridge.py, started by Jafar's one click a session) runs each .py
dropped in F:/LedgerTools/md-jobs/inbox on Marvelous's own thread, with CLO's API modules imported and a
`result` dict and `log()` function in scope, and writes out/<job>.json. A job is copied in whole (written
beside, then renamed) so the bridge never reads half a file. If the heartbeat is older than 30 s the
bridge is not running: that needs his click, so this says so and stops (Needs you).
"""
import json
import os
import shutil
import sys
import time

ROOT = os.environ.get("LEDGER_MD_JOBS", r"F:\LedgerTools\md-jobs")
STALE_S = 30.0


def alive(root=ROOT, now=None):
    """(True, note) when the bridge wrote its heartbeat in the last 30 s and has not stopped."""
    p = os.path.join(root, "heartbeat.json")
    if not os.path.exists(p):
        return False, "no heartbeat: the bridge has never run"
    age = (now or time.time()) - os.path.getmtime(p)
    beat = json.load(open(p, encoding="utf-8"))
    if "stopped" in beat:
        return False, "the bridge was stopped at %s" % beat["stopped"]
    if age > STALE_S:
        return False, "the heartbeat is %d s old: Marvelous closed or the bridge not clicked" % age
    return True, "alive, %s jobs run" % beat.get("jobs")


def submit(job, timeout, root=ROOT):
    ok, note = alive(root)
    if not ok:
        print(json.dumps({"ok": False, "bridge": note, "needsJafar": "open Marvelous and click the LEDGER bridge once"}))
        return 1
    name = os.path.splitext(os.path.basename(job))[0]
    out = os.path.join(root, "out", name + ".json")
    if os.path.exists(out):
        os.remove(out)
    tmp = os.path.join(root, "inbox", name + ".part")
    shutil.copyfile(job, tmp)
    os.replace(tmp, os.path.join(root, "inbox", name + ".py"))
    t0 = time.time()
    while time.time() - t0 < timeout:
        if os.path.exists(out):
            res = json.load(open(out, encoding="utf-8"))
            print(json.dumps(res, indent=1))
            return 0 if res.get("ok") else 1
        time.sleep(0.5)
    print(json.dumps({"ok": False, "job": name, "timeout": timeout}))
    return 1


def selftest():
    import tempfile
    ok = 0
    with tempfile.TemporaryDirectory() as d:
        r = alive(d)
        ok += (r[0] is False and "never" in r[1])
        json.dump({"alive": "x", "jobs": 2}, open(os.path.join(d, "heartbeat.json"), "w"))
        ok += alive(d)[0] is True
        ok += alive(d, now=time.time() + 60)[0] is False
        json.dump({"stopped": "x"}, open(os.path.join(d, "heartbeat.json"), "w"))
        ok += alive(d)[0] is False
    print("md_job selftest: passed=%d/4 failed=%d" % (ok, 4 - ok))
    return 0 if ok == 4 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--alive" in a:
        r = alive()
        print(r[1])
        sys.exit(0 if r[0] else 1)
    sys.exit(submit(a[0], float(a[a.index("--timeout") + 1]) if "--timeout" in a else 600.0))
