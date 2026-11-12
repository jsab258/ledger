"""Motionsmith round 1 (advisor 119/120, 12 Nov): run his tool's own test jobs and move library from copies
whose inputs point into his folder and whose outputs go to F:, twice each, and gather checks, times and FBX hashes.
    python tools/tool-tests/motionsmith_r1.py [pass-name]
Never writes into C:/Game Dev Tools."""
import hashlib, json, os, subprocess, sys, time
APP = "C:/Game Dev Tools/Motionsmith/app"
EXE = APP + "/target/debug/motionsmith.exe"
W = "F:/LedgerTools/tool-tests-2026-11/motionsmith-r1"
tag = sys.argv[1] if len(sys.argv) > 1 else "a"
jobs = [os.path.join(APP, "jobs", f) for f in sorted(os.listdir(APP + "/jobs")) if f.endswith(".json")]
jobs += [os.path.join(APP, "jobs", "moves", f) for f in sorted(os.listdir(APP + "/jobs/moves")) if f.endswith(".json")]
rows = []
for src in jobs:
    j = json.load(open(src, encoding="utf-8"))
    base = os.path.dirname(src)
    for k in ("input", "move"):
        if isinstance(j.get(k), str) and not j[k].startswith(("fbx:", "dna:")) and ("/" in j[k] or "\\" in j[k]):
            j[k] = os.path.normpath(os.path.join(base, j[k])).replace("\\", "/")
    out = j.setdefault("output", {})
    out["folder"] = "%s/out-%s/%s" % (W, tag, j["name"])
    out["film"] = True
    dst = "%s/jobs-%s/%s.json" % (W, tag, j["name"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(j, open(dst, "w", encoding="utf-8"), indent=1)
    t0 = time.time()
    p = subprocess.run([EXE, "--job", dst], cwd=W, capture_output=True, text=True)
    dt = time.time() - t0
    fbx = [f for f in os.listdir(out["folder"]) if f.endswith(".fbx")] if os.path.isdir(out["folder"]) else []
    h = hashlib.sha256(open(os.path.join(out["folder"], fbx[0]), "rb").read()).hexdigest()[:16] if fbx else None
    ck = os.path.join(out["folder"], "checks.json")
    checks = json.load(open(ck, encoding="utf-8")) if os.path.isfile(ck) else None
    rows.append({"job": j["name"], "exit": p.returncode, "s": round(dt, 1), "fbx": h, "checks": checks,
                 "stderr": p.stderr[-400:]})
    print(j["name"], p.returncode, round(dt, 1), h, flush=True)
json.dump(rows, open("%s/summary-%s.json" % (W, tag), "w", encoding="utf-8"), indent=1)
