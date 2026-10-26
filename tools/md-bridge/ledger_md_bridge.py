"""LEDGER's bridge into Marvelous Designer: one click a session, then jobs from a folder.

    In Marvelous Designer: Plugin tab > Plug-in Manager > + ADD > this file (once); then click it once a session.
    From the PC's side: python tools/md-bridge/md_job.py JOB.py   (drops the job, waits for its result)

WHY, 26 October 2026. Jafar's order of 25 October, item 3: Tom's outfit made in Marvelous Designer.
Marvelous runs scripts only from inside its own window (production/research/game-clothing-pipeline/
MD-SCRIPTING-2026-10-26.md), and this session cannot click outside its browser. His answer the same
afternoon: "one click per session. I accept the licence judgement for this plug-in: it uses CLO's own
Python tools inside Marvelous. Keep Marvelous open between garments and batch the work into as few
sessions as possible, so I click rarely."

HOW. Clicked, this file starts a Windows timer on Marvelous's own thread and returns, so Marvelous stays
usable. Every 300 ms the timer looks in F:/LedgerTools/md-jobs/inbox for a job (a .py file); it runs the
oldest one there, on Marvelous's thread, with CLO's API modules already imported, and writes
out/<job>.json: ok, seconds, the job's `result` dict, its log lines and any error. The job file moves to
done/. A file named stop.job ends the timer. heartbeat.json says the bridge is alive (written every
10 s). No network port is opened: only files on this PC's drive F: reach it. A second click while it
runs says so and starts nothing.

Nothing here is CLO's code. It uses CLO's documented Python modules (utility_api, import_api,
pattern_api, fabric_api, export_api and ApiTypes, developer.marvelousdesigner.com) and the Windows
timer from user32 through ctypes, both from Python's standard library.
"""
import builtins
import contextlib
import ctypes
import io
import json
import os
import sys
import time
import traceback
from ctypes import wintypes

ROOT = os.environ.get("LEDGER_MD_JOBS", r"F:\LedgerTools\md-jobs")
INBOX, DONE, OUT = (os.path.join(ROOT, d) for d in ("inbox", "done", "out"))
TICK_MS, BEAT_S = 300, 10.0
API_MODULES = ("utility_api", "import_api", "pattern_api", "fabric_api", "export_api", "ApiTypes")
KEY = "_ledger_md_bridge"


def api_namespace():
    """CLO's modules, each imported if this Marvelous has it."""
    ns, missing = {}, []
    for name in API_MODULES:
        try:
            ns[name] = __import__(name)
        except Exception:
            missing.append(name)
    return ns, missing


def write_json(path, data):
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, default=str)
    os.replace(tmp, path)


def run_job(path, state):
    name = os.path.splitext(os.path.basename(path))[0]
    ns, missing = api_namespace()
    lines = []
    ns.update({"result": {}, "log": lambda *a: lines.append(" ".join(str(x) for x in a)),
               "JOB_DIR": ROOT, "__name__": "ledger_md_job"})
    t0 = time.time()
    out = {"job": name, "ok": False, "missingModules": missing}
    buf = io.StringIO()
    try:
        code = open(path, encoding="utf-8").read()
        with contextlib.redirect_stdout(buf):
            exec(compile(code, path, "exec"), ns)
        out["ok"] = True
    except Exception:
        out["error"] = traceback.format_exc()[-4000:]
    out.update({"seconds": round(time.time() - t0, 2), "result": ns.get("result", {}), "log": lines,
                "stdout": buf.getvalue()[-4000:]})
    write_json(os.path.join(OUT, name + ".json"), out)
    os.replace(path, os.path.join(DONE, "%s-%d.py" % (name, int(t0))))
    state["jobs"] += 1


def tick(state):
    if state["busy"]:
        return
    state["busy"] = True
    try:
        now = time.time()
        if now - state["beat"] >= BEAT_S:
            state["beat"] = now
            write_json(os.path.join(ROOT, "heartbeat.json"), {"alive": time.strftime("%Y-%m-%d %H:%M:%S"),
                                                             "jobs": state["jobs"], "python": sys.version.split()[0]})
        if os.path.exists(os.path.join(INBOX, "stop.job")):
            os.remove(os.path.join(INBOX, "stop.job"))
            stop(state)
            return
        jobs = sorted((os.path.getmtime(os.path.join(INBOX, f)), f) for f in os.listdir(INBOX) if f.endswith(".py"))
        if jobs:
            run_job(os.path.join(INBOX, jobs[0][1]), state)
    except Exception:
        try:
            write_json(os.path.join(ROOT, "bridge-error.json"), {"at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                "error": traceback.format_exc()[-4000:]})
        except Exception:
            pass
    finally:
        state["busy"] = False


def stop(state):
    user32 = ctypes.windll.user32
    user32.KillTimer.argtypes = (wintypes.HWND, ctypes.c_size_t)
    user32.KillTimer(None, state["timer"])
    write_json(os.path.join(ROOT, "heartbeat.json"), {"stopped": time.strftime("%Y-%m-%d %H:%M:%S"), "jobs": state["jobs"]})
    setattr(builtins, KEY, None)


def start():
    running = getattr(builtins, KEY, None)
    if running:
        print("LEDGER bridge: already running (%d jobs so far)." % running["jobs"])
        return
    for d in (INBOX, DONE, OUT):
        os.makedirs(d, exist_ok=True)
    TIMERPROC = ctypes.WINFUNCTYPE(None, wintypes.HWND, wintypes.UINT, ctypes.c_size_t, wintypes.DWORD)
    state = {"busy": False, "beat": 0.0, "jobs": 0}
    state["proc"] = TIMERPROC(lambda h, m, i, t: tick(state))      # kept, or the callback is collected
    user32 = ctypes.windll.user32
    user32.SetTimer.restype = ctypes.c_size_t
    user32.SetTimer.argtypes = (wintypes.HWND, ctypes.c_size_t, wintypes.UINT, TIMERPROC)
    state["timer"] = user32.SetTimer(None, 0, TICK_MS, state["proc"])
    if not state["timer"]:
        print("LEDGER bridge: Windows refused the timer; nothing started.")
        return
    setattr(builtins, KEY, state)
    write_json(os.path.join(ROOT, "heartbeat.json"), {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "jobs": 0,
                                                     "python": sys.version.split()[0]})
    print("LEDGER bridge: running. Jobs are read from %s; leave Marvelous open." % INBOX)


start()
