"""Runs the portable voice with a bare environment: only Windows' own folders
and the bundle's own on PATH, no PYTHONHOME, no user site, a fresh temp folder.
First its self-test, then one line spoken on the processor (--cpu, so the
graphics card is left alone), timed."""
import json
import os
import subprocess
import sys
import tempfile
import time

B = r"F:\LedgerTools\voice-portable"
PY = os.path.join(B, "python", "python.exe")
SCRIPT = os.path.join(B, "tools", "voice-live", "voice-server.py")
tmp = tempfile.mkdtemp(prefix="voice-bare-")
env = {
    "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),
    "WINDIR": os.environ.get("WINDIR", r"C:\Windows"),
    "PATH": os.pathsep.join([os.path.join(B, "python"), os.path.join(B, "python", "Library", "bin"),
                             r"C:\Windows\System32", r"C:\Windows"]),
    "TEMP": tmp, "TMP": tmp,
    "USERPROFILE": tmp, "LOCALAPPDATA": tmp, "APPDATA": tmp, "HOME": tmp,
    "PYTHONNOUSERSITE": "1",
    "NANO_PKG": os.path.join(B, "nano", "src-master", "src"),
    "NANO_WEIGHTS": os.path.join(B, "nano", "weights"),
    "NANO_VOICE_CACHE": os.path.join(B, "nano", "voice-cache"),
    "HF_HOME": os.path.join(tmp, "hf"),
}
r = subprocess.run([PY, "-c", "import sys, torch; print(sys.prefix); print(torch.__version__, torch.__file__)"],
                   env=env, capture_output=True, text=True, timeout=300)
print("python and torch:", r.returncode, (r.stdout + r.stderr).strip()[-400:])
r = subprocess.run([PY, SCRIPT, "--selftest"], env=env, capture_output=True, text=True, timeout=300)
print("selftest:", r.returncode, (r.stdout + r.stderr).strip()[-300:])
t0 = time.time()
p = subprocess.Popen([PY, SCRIPT, "--cpu", "--out", os.path.join(tmp, "out")], env=env, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
ready = None
for line in p.stdout:
    if '"ready"' in line:
        ready = time.time() - t0
        break
print("ready after %.1f s" % ready if ready else "never ready")
if ready:
    t1 = time.time()
    p.stdin.write(json.dumps({"id": 1, "who": "sam", "text": "Alright. Not seen you round here before."}) + "\n")
    p.stdin.flush()
    first = None
    for line in p.stdout:
        if '"wav"' in line:
            d = json.loads(line)
            if first is None:
                first = time.time() - t1
            print("piece:", {k: d.get(k) for k in ("part", "last", "seconds", "ms")}, "exists", os.path.exists(d.get("wav", "")))
            if d.get("last"):
                break
    print("first sound ready %.1f s after the line" % first if first else "no sound")
p.stdin.close()
try:
    p.wait(timeout=30)
except Exception:
    p.kill()
err = p.stderr.read()[-600:] if p.stderr else ""
if not ready:
    print("stderr:", err)
