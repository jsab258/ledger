"""Motionsmith round 3 (advisor 131, 13 Nov): his updated tool's own jobs and move library, run twice from copies
whose outputs go to F:, plus our real chair-rise through his job 07, plus the identity test (every library
move's output fixed again with his fix and compared with --compare).
    python tools/tool-tests/motionsmith_r3.py run [a|b]     # all jobs, the real rise, summary-<tag>.json
    python tools/tool-tests/motionsmith_r3.py identity      # fix every move's out-a FBX again, compare
Never writes into C:/Game Dev Tools."""
import hashlib, json, os, subprocess, sys, time
APP = "C:/Game Dev Tools/Motionsmith/app"
EXE = APP + "/target/debug/motionsmith.exe"
W = "F:/LedgerTools/tool-tests-2026-11/motionsmith-r3"
RISE = "F:/LedgerTools/tool-tests-2026-11/motionsmith-r2/rise430s_Body.fbx"


def job_files():
    js = [os.path.join(APP, "jobs", f) for f in sorted(os.listdir(APP + "/jobs")) if f.endswith(".json")]
    js += [os.path.join(APP, "jobs", "moves", f) for f in sorted(os.listdir(APP + "/jobs/moves")) if f.endswith(".json")]
    return js


def absolutise(j, base):
    for k in ("input", "move", "reference"):
        if isinstance(j.get(k), str) and not j[k].startswith(("fbx:", "dna:")) and ("/" in j[k] or "\\" in j[k]):
            j[k] = os.path.normpath(os.path.join(base, j[k])).replace("\\", "/")
    return j


def run_job(j, tag, film=True):
    out = j.setdefault("output", {})
    out["folder"] = "%s/out-%s/%s" % (W, tag, j["name"])
    out["film"] = film
    dst = "%s/jobs-%s/%s.json" % (W, tag, j["name"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(j, open(dst, "w", encoding="utf-8"), indent=1)
    t0 = time.time()
    p = subprocess.run([EXE, "--job", dst], cwd=W, capture_output=True, text=True)
    dt = time.time() - t0
    fbx = [f for f in os.listdir(out["folder"]) if f.endswith(".fbx")] if os.path.isdir(out["folder"]) else []
    path = os.path.join(out["folder"], fbx[0]) if fbx else None
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16] if path else None
    ck = os.path.join(out["folder"], "checks.json")
    checks = json.load(open(ck, encoding="utf-8")) if os.path.isfile(ck) else None
    print(j["name"], p.returncode, round(dt, 1), h, flush=True)
    return {"job": j["name"], "exit": p.returncode, "s": round(dt, 1), "fbx": path, "hash": h, "checks": checks,
            "stderr": p.stderr[-400:]}


def run(tag):
    rows = []
    for src in job_files():
        j = absolutise(json.load(open(src, encoding="utf-8")), os.path.dirname(src))
        rows.append(run_job(j, tag))
    j = absolutise(json.load(open(APP + "/jobs/07_chair_rise_fix.json", encoding="utf-8")), APP + "/jobs")
    j["name"] = "r3_real_rise_fix"
    j["input"] = RISE
    j["output"] = {"name": "A_Ledger_RealRise_Fixed"}
    rows.append(run_job(j, tag))
    json.dump(rows, open("%s/summary-%s.json" % (W, tag), "w", encoding="utf-8"), indent=1)


def identity():
    rows = []
    for src in sorted(os.listdir(APP + "/jobs/moves")):
        name = json.load(open(os.path.join(APP, "jobs/moves", src), encoding="utf-8"))["name"]
        d = "%s/out-a/%s" % (W, name)
        fbx = [f for f in os.listdir(d) if f.endswith(".fbx")] if os.path.isdir(d) else []
        if not fbx:
            rows.append({"move": name, "error": "no out-a fbx"}); continue
        inp = os.path.join(d, fbx[0]).replace("\\", "/")
        j = {"name": "id_" + name, "type": "fix", "input": inp,
             "pass": {"foot_slide_cm": 1.0, "knee_deg": 5.0, "toe_tilt_deg": 3.0, "floor_cm": 0.5,
                      "timing_lag_frames": 0, "timing_corr": 0.98},
             "output": {"name": "ID_" + name}}
        r = run_job(j, "id", film=False)
        cmp_ = subprocess.run([EXE, "--compare", inp, r["fbx"]], cwd=W, capture_output=True, text=True) if r["fbx"] else None
        r["move"] = name
        r["compare"] = (cmp_.stdout[-1500:] if cmp_ else None)
        r["compare_exit"] = cmp_.returncode if cmp_ else None
        rows.append(r)
    json.dump(rows, open("%s/identity.json" % W, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    os.makedirs(W, exist_ok=True)
    if sys.argv[1] == "run":
        run(sys.argv[2] if len(sys.argv) > 2 else "a")
    elif sys.argv[1] == "identity":
        identity()
