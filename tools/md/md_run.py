"""Send one job to Marvelous Designer through the bridge (tools/md/md_bridge.py) and print what it printed.

    python tools/md/md_run.py JOB.py [--timeout 1800]
    python tools/md/md_run.py --code "print(dir(pattern_api))"
    python tools/md/md_run.py --alive

The job runs inside Marvelous Designer in one shared namespace that already holds its API modules (pattern_api,
fabric_api, import_api, export_api, utility_api, ApiTypes, ...), so names a job defines are there for the next one.
Exits 0 when the job printed "OK", 1 on an error inside Marvelous Designer, 2 when the bridge is not running or the
job timed out.
"""
import os
import sys
import time

ROOT = r"F:\LedgerTools\md-bridge"
INBOX = os.path.join(ROOT, "inbox")
OUTBOX = os.path.join(ROOT, "outbox")
ALIVE = os.path.join(ROOT, "alive.txt")


def alive(max_age=15.0):
    try:
        return time.time() - os.path.getmtime(ALIVE) < max_age and not open(ALIVE).read().startswith("stopped")
    except OSError:
        return False


def main(argv):
    if "--alive" in argv:
        ok = alive()
        print("bridge running" if ok else "bridge NOT running")
        return 0 if ok else 2
    timeout = float(argv[argv.index("--timeout") + 1]) if "--timeout" in argv else 1800.0
    if "--code" in argv:
        code = argv[argv.index("--code") + 1]
        name = "inline"
    else:
        path = argv[0]
        code = open(path, encoding="utf-8").read()
        name = os.path.splitext(os.path.basename(path))[0]
    if not alive():
        print("bridge NOT running: start tools/md/md_bridge.py in Marvelous Designer's Python window")
        return 2
    os.makedirs(INBOX, exist_ok=True)
    job = "%s_%d" % (name, int(time.time() * 1000))
    tmp = os.path.join(INBOX, job + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(code)
    os.replace(tmp, os.path.join(INBOX, job + ".py"))
    out = os.path.join(OUTBOX, job + ".txt")
    t0 = time.time()
    while time.time() - t0 < timeout:
        if os.path.exists(out):
            time.sleep(0.2)
            text = open(out, encoding="utf-8").read()
            print(text)
            return 0 if text.startswith("OK") else 1
        time.sleep(0.5)
    print("timed out after %.0f s (the job may still be running in Marvelous Designer)" % timeout)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
