"""The clothing session's bridge into Marvelous Designer: run ONCE inside the program, then it runs every job script
the session drops in a folder, so one start serves the whole sitting.

HOW TO START IT (Jafar, once each time Marvelous Designer is opened): in Marvelous Designer, open the Python script
window (Script menu, "Python" or "Python Script"), open this file (C:\\Users\\Jafar\\ledger-clothes\\tools\\md\\
md_bridge.py) and press Run. The program then looks busy while it works; leave it open. To stop it, the session writes
the file F:\\LedgerTools\\md-bridge\\stop.

WHY, 1 October (Jafar's ruling: Marvelous Designer joins the clothing lane for one jacket proof; DECISIONS.md).
Marvelous Designer has no command line and no way to run a script at start-up: someone must start a script from its
own window each time it opens (production/research/clothing-pipeline/MD-SCRIPTING-2026-09-29.md). This bridge is that
one script. It polls F:\\LedgerTools\\md-bridge\\inbox for job files (*.py); each is run in one shared namespace that
already holds Marvelous Designer's API modules, its printed output and any error are written to
F:\\LedgerTools\\md-bridge\\outbox\\<job>.txt (the first line "OK" or "ERROR"), and the job file is removed. A
heartbeat file (alive.txt) is rewritten every few seconds, so the session can tell the bridge is running.
Nothing here reaches the network; it only reads job files the clothing session writes.
"""
import contextlib
import io
import os
import time
import traceback

ROOT = r"F:\LedgerTools\md-bridge"
INBOX = os.path.join(ROOT, "inbox")
OUTBOX = os.path.join(ROOT, "outbox")
STOP = os.path.join(ROOT, "stop")
ALIVE = os.path.join(ROOT, "alive.txt")
for d in (INBOX, OUTBOX):
    os.makedirs(d, exist_ok=True)
if os.path.exists(STOP):
    os.remove(STOP)

SHARED = {"__name__": "md_job"}
for mod in ("ApiTypes", "fabric_api", "pattern_api", "import_api", "export_api", "utility_api", "mdsa", "mdpy",
            "avatar_api", "garment_api", "sewing_api", "simulation_api", "arrangement_api", "trim_api", "uv_api"):
    try:
        SHARED[mod] = __import__(mod)
    except Exception:
        pass
SHARED["BRIDGE_MODULES"] = sorted(k for k in SHARED if not k.startswith("__"))

last_beat = 0.0
while not os.path.exists(STOP):
    now = time.time()
    if now - last_beat > 3:
        with open(ALIVE, "w") as f:
            f.write("%s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), " ".join(SHARED["BRIDGE_MODULES"])))
        last_beat = now
    jobs = sorted(j for j in os.listdir(INBOX) if j.endswith(".py"))
    for job in jobs:
        path = os.path.join(INBOX, job)
        try:
            code = open(path, encoding="utf-8").read()
        except Exception:
            continue
        os.remove(path)
        buf = io.StringIO()
        status = "OK"
        started = time.time()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                exec(compile(code, job, "exec"), SHARED)
        except Exception:
            status = "ERROR"
            buf.write(traceback.format_exc())
        with open(os.path.join(OUTBOX, job[:-3] + ".txt"), "w", encoding="utf-8") as f:
            f.write("%s %.1fs\n%s" % (status, time.time() - started, buf.getvalue()))
    time.sleep(0.5)
with open(ALIVE, "w") as f:
    f.write("stopped %s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
