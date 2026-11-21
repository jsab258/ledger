#!/usr/bin/env python3
"""Export every saved Marvelous project on F:/LedgerTools before the subscription month ends (21 November 2026).

    python tools/md-bridge/export_all.py [--only SUBSTRING]   # one bridge job per .zprj; a summary JSON at the end

Each .zprj gets jobs/export_one.py with SRC set: opened in a fresh scene (the reopen check), pattern JSON and garment
FBX written beside it. Results go to F:/LedgerTools/md-jobs/export-2026-11-21.json; a project whose two files already
exist is skipped, so a rerun picks up where one stopped.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BODY = open(os.path.join(HERE, "jobs", "export_one.py"), encoding="utf-8").read()
OUT = r"F:\LedgerTools\md-jobs\export-2026-11-21.json"


def projects():
    return sorted(glob.glob(r"F:\LedgerTools\**\*.zprj", recursive=True))


def main():
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else ""
    done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    for i, src in enumerate(projects()):
        if only and only not in src:
            continue
        base = os.path.splitext(src)[0]
        if all(os.path.isfile(base + s) for s in (".pattern.json", ".garment.fbx")):
            done.setdefault(src, {"skipped": "both files present"})
            continue
        tmp = os.path.join(tempfile.gettempdir(), "ledger_export_%02d.py" % i)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("SRC = %r\n" % src + BODY)
        r = subprocess.run([sys.executable, os.path.join(HERE, "md_job.py"), tmp, "--timeout", "300"],
                           capture_output=True, text=True)
        os.remove(tmp)
        try:
            done[src] = json.loads(r.stdout)
        except ValueError:
            done[src] = {"ok": False, "exit": r.returncode, "said": (r.stdout + r.stderr)[-400:]}
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(done, f, indent=1)
        print(os.path.relpath(src, r"F:\LedgerTools"), "exit", r.returncode, flush=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(done, f, indent=1)


if __name__ == "__main__":
    main()
