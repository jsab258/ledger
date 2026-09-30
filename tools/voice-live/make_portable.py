"""The voice stopgap's trial (item 3, Jafar 30 September): today's voice
program made portable in one folder, with no installed Python behind it.

Copies only; deletes nothing. Layout (the voice server finds its clips and
spec from its own ROOT, two folders above the script):

  F:/LedgerTools/voice-portable/
    python/            base Python 3.12 runtime (miniconda's), stdlib, DLLs, Library/bin DLLs,
                       and env-dml's site-packages in python/Lib/site-packages
    nano/src, nano/weights, nano/voice-cache
    tools/voice-live/  voice-server.py and its helpers
    game-design/picked-clips, production/specs/voice-engines.json, production/casting/in-game-2026-09-25/voice
"""
import os
import shutil
import sys

BASE = r"C:\Users\Jafar\miniconda3"
ENV = r"C:\LedgerTools\chatterbox-nano\env-dml"
NANO = r"C:\LedgerTools\chatterbox-nano"
REPO = r"C:\Users\Jafar\ledger-local"
OUT = r"F:\LedgerTools\voice-portable"

if os.path.exists(OUT):
    sys.exit("already there: " + OUT)


def ignore_cache(d, names):
    return [n for n in names if n == "__pycache__"]


py = os.path.join(OUT, "python")
os.makedirs(py)
for f in os.listdir(BASE):
    p = os.path.join(BASE, f)
    if os.path.isfile(p) and (f.lower().endswith(".dll") or f.lower() in ("python.exe", "pythonw.exe", "license_python.txt")):
        shutil.copy2(p, py)
shutil.copytree(os.path.join(BASE, "DLLs"), os.path.join(py, "DLLs"), ignore=ignore_cache)
shutil.copytree(os.path.join(BASE, "Lib"), os.path.join(py, "Lib"),
                ignore=lambda d, n: [x for x in n if x == "__pycache__" or (os.path.normcase(d) == os.path.normcase(os.path.join(BASE, "Lib")) and x == "site-packages")])
os.makedirs(os.path.join(py, "Library"))
shutil.copytree(os.path.join(BASE, "Library", "bin"), os.path.join(py, "Library", "bin"),
                ignore=lambda d, n: [x for x in n if not x.lower().endswith(".dll")])
shutil.copytree(os.path.join(ENV, "Lib", "site-packages"), os.path.join(py, "Lib", "site-packages"), ignore=ignore_cache)
for sub in ("src-master", "weights", "voice-cache"):
    shutil.copytree(os.path.join(NANO, sub), os.path.join(OUT, "nano", sub), ignore=ignore_cache)
shutil.copytree(os.path.join(REPO, "tools", "voice-live"), os.path.join(OUT, "tools", "voice-live"), ignore=ignore_cache)
shutil.copytree(os.path.join(REPO, "game-design", "picked-clips"), os.path.join(OUT, "game-design", "picked-clips"))
os.makedirs(os.path.join(OUT, "production", "specs"))
shutil.copy2(os.path.join(REPO, "production", "specs", "voice-engines.json"), os.path.join(OUT, "production", "specs"))
cast = os.path.join(REPO, "production", "casting", "in-game-2026-09-25", "voice")
if os.path.isdir(cast):
    shutil.copytree(cast, os.path.join(OUT, "production", "casting", "in-game-2026-09-25", "voice"))
total = 0
for d, _, fs in os.walk(OUT):
    for f in fs:
        total += os.path.getsize(os.path.join(d, f))
print("voice-portable: %.2f GB at %s" % (total / 1e9, OUT))
