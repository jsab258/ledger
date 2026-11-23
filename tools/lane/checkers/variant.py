#!/usr/bin/env python3
"""Checkers proven (23 Nov 2026): build a planted copy of the prototype and run the checkers on it, blind.

The planted file (a JSON list of faults, each with edits {file, old, new}) is kept outside the repository while the
checkers run, and no checker is given it, its path, or the planted source: they get only the built page (dist),
exactly as they will get the one-shot's build. The game's own folder is never changed: the project is copied
outside the repository, the edits applied there, and the copy built.

    python variant.py build   --work DIR [--faults FILE --ids a,b] [--overlay]   (--overlay: the mended story watchers)
    python variant.py stories --work DIR [S01 S02 ...]        the play stories as in-game tests, in order, once
    python variant.py machine --work DIR --out DIR [args..]    the machine checks on the variant's build
    python variant.py clumsy  --work DIR --out DIR [args..]
    python variant.py conseq  --work DIR --out DIR [args..]

Each variant keeps its own story saves (DIR/../<name>-saves), so two variants never share a save.
"""
import argparse, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
PROTO = os.path.join(LANE, "prototype")
GATE = os.path.join(LANE, "gate")
sys.path.insert(0, PROTO)
import build as B  # noqa: E402
import run_proto_tests as R  # noqa: E402

ASSETS = os.environ.get("LEDGER_PROTO_ASSETS", "/home/claude/proto-assets")


def apply_edits(project, fault):
    for e in fault["edits"]:
        p = os.path.join(project, "src", e["file"])
        text = open(p, encoding="utf-8").read()
        n = text.count(e["old"])
        if n != 1:
            return "%s: the text to change occurs %d times in %s" % (fault["id"], n, e["file"])
        open(p, "w", encoding="utf-8").write(text.replace(e["old"], e["new"]))
    return None


def do_build(work, faults_file=None, ids=None, overlay=False):
    work = os.path.abspath(work)
    proj = work + "-project"
    if os.path.exists(proj):
        shutil.rmtree(proj)
    shutil.copytree(B.PROJECT, proj, ignore=shutil.ignore_patterns("node_modules", "dist", "site", "out", "assets"))
    if faults_file:
        faults = json.load(open(faults_file, encoding="utf-8"))["faults"]
        want = [f for f in faults if not ids or f["id"] in ids]
        for f in want:
            why = apply_edits(proj, f)
            if why:
                print("NOT PLANTED:", why)
                return 1
        print("planted %d" % len(want))
    if overlay:  # the checkers' mended story player (watchers), copied over the project's own test files
        od = os.path.join(HERE, "overlay")
        for root, _, names in os.walk(od):
            for n in names:
                rel = os.path.relpath(os.path.join(root, n), od)
                os.makedirs(os.path.dirname(os.path.join(proj, rel)), exist_ok=True)
                shutil.copy2(os.path.join(root, n), os.path.join(proj, rel))
        print("overlay in")
    B.PROJECT = proj
    seed = os.environ.get("CHECKERS_SEED_WORK")  # a built work folder whose packages can be copied (saves npm ci)
    if seed and not os.path.isdir(os.path.join(work, "node_modules")) and os.path.isdir(os.path.join(seed, "node_modules")):
        os.makedirs(work, exist_ok=True)
        shutil.copytree(os.path.join(seed, "node_modules"), os.path.join(work, "node_modules"), symlinks=True)
        shutil.copy2(os.path.join(seed, ".lock-sha"), os.path.join(work, ".lock-sha"))
    with B.work_lock(work):
        probs = B.build(assets_dir=ASSETS, allow_changed=True, dist=os.path.join(work, "dist-check"), work=work, locked=True)
        probs = [p for p in probs if "differs from the published page" not in p]
        if probs:
            print("build:", "; ".join(probs))
            return 1
        R.install_shim(work)
    # the source beside the build, for the content scan (it must read what was built); the planted file is not here
    src = os.path.join(work, "dist-check", "_src")
    if os.path.exists(src):
        shutil.rmtree(src)
    shutil.copytree(os.path.join(work, "src"), src)
    shutil.rmtree(proj)
    print("built", work)
    return 0


def do_stories(work, names):
    work = os.path.abspath(work)
    env = dict(os.environ, LEDGER_STORY_ONCE="1", LEDGER_STORY_SAVES=work + "-saves")
    env.setdefault("LEDGER_PORT_SHIFT", str(1000 * (1 + sum(map(ord, os.path.basename(work))) % 20)))
    shutil.rmtree(work + "-saves", ignore_errors=True)
    logs = os.path.join(work, "story-logs")
    os.makedirs(logs, exist_ok=True)
    res = {}
    for n in names:
        t0 = time.time()
        try:
            p = subprocess.run(["nice", "-n", "5", "node", "test/stories/%s.mjs" % n], cwd=work, env=env,
                               capture_output=True, text=True, timeout=1500)
            out, code = p.stdout + p.stderr, p.returncode
        except subprocess.TimeoutExpired:
            out, code = "TIMEOUT", 124
        v = R.verdict(n, code, out)
        open(os.path.join(logs, n + ".log"), "w", encoding="utf-8").write(out)
        fails = [l for l in out.splitlines() if "TEST FAIL" in l or "FAIL (" in l or "PAGEERR" in l or "TIMEOUT" in l]
        res[n] = {"verdict": v, "secs": round(time.time() - t0), "fails": fails[:40]}
        print("%-5s %-5s %4.0f s" % (n, v, time.time() - t0), flush=True)
        for l in fails[:12]:
            print("   ", l[:220])
    json.dump(res, open(os.path.join(work, "stories.json"), "w"), indent=1)
    return 0 if all(r["verdict"] == "PASS" for r in res.values()) else 1


def do_tester(script, work, out, extra, with_src=False):
    dist = os.path.join(os.path.abspath(work), "dist-check")
    cmd = [sys.executable, os.path.join(GATE, script), "--dist", dist, "--out", out] + extra
    if with_src:
        cmd += ["--src", os.path.join(dist, "_src")]  # the gate's own frame baseline, as in the one-shot
    os.makedirs(out, exist_ok=True)
    p = subprocess.run(cmd, cwd=GATE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=3600)
    open(os.path.join(out, "run.log"), "w").write(p.stdout)
    print(p.stdout[-1500:])
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["build", "stories", "machine", "clumsy", "conseq"])
    ap.add_argument("--work", required=True)
    ap.add_argument("--faults")
    ap.add_argument("--ids", default="")
    ap.add_argument("--out")
    ap.add_argument("--overlay", action="store_true")
    a, rest = ap.parse_known_args()
    if B._inside_repo(a.work):
        raise SystemExit("work outside the repository")
    if a.what == "build":
        return do_build(a.work, a.faults, [x for x in a.ids.split(",") if x], a.overlay)
    if a.what == "stories":
        return do_stories(a.work, rest or ["S01", "S02", "S03", "S04", "S05", "S06"])
    script = {"machine": "machine_checks.py", "clumsy": "clumsy.py", "conseq": "consequences.py"}[a.what]
    return do_tester(script, a.work, a.out, rest, with_src=a.what == "machine")


if __name__ == "__main__":
    sys.exit(main())
