#!/usr/bin/env python3
"""Run the prototype's own tests (Fable's project/test/*.mjs) in the cloud's headless Chromium.

Fable's tests use puppeteer-core and a system Chrome. Here the lane builds the page from the
readable source (build.py, in a work folder outside the repository), puts its stand-in
shim/puppeteer-core (the same calls, carried out by Playwright's installed Chromium) in place of
the real package in the work folder's node_modules, and runs the tests unchanged, in Fable's
order (npm test): numbers, walks, same week, week, publish set, arrivals, nights,
town, ledger rules, layout, files, talk, eyes. oldsave runs only with
OLD=<folder holding an older build of the page>. Last, the lane's AI playtester
(playtester/playtest.py: the sweep and the newcomer run) writes its reports to
<work>/lane-test-logs/playtest/; it gives findings, not a verdict (SEE), and fails only if it
crashes. --no-playtest leaves it out; --playtest-minutes sets the newcomer's play time.

Needs the pictures: --assets DIR or LEDGER_PROTO_ASSETS (checked against PUBLISHED.json).

  python run_proto_tests.py --assets DIR [--only nights,layout] [--work DIR]

Prints one line per test (PASS, FAIL, or SEE: a test that prints its findings without a
verdict) and writes the full output of each to <work>/lane-test-logs/. Exit 0 only if no test
failed.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402

# Fable's npm test order (second round of 18 Nov), the lane's round-1 checks, then oldsave, which needs an older build
ORDER = ["numbers", "walks", "same_week", "week", "publish_set", "arrivals", "nights", "town",
         "ledger_rules", "layout", "files", "talk", "eyes", "fixes1", "watch2", "melee3", "melee4", "talk5", "oldsave"]
SCRIPTS = {"numbers": ["tools/numbers.mjs", "left"], "walks": ["tools/walk_times.mjs"],
           "publish_set": ["tools/publish_set.mjs"]}


def verdict(name, code, out):
    """PASS, FAIL or SEE from a test's exit code and output (the tests print, few exit non-zero)."""
    lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    if code != 0:
        return "FAIL"
    if name == "publish_set":
        return "PASS"
    if name in ("numbers", "walks"):
        return "PASS" if re.search(r"^PASS\b", out, re.M) else "FAIL"
    if re.search(r"\bTEST FAIL\b|\bFAILED\b|PAGEERR", out):
        return "FAIL"
    if last == "PASS" or last.endswith(" PASS") or last.startswith("PASS:"):
        return "PASS"
    if last == "FAIL" or re.search(r"^FAIL\b", last) or last.startswith("FAIL:"):
        return "FAIL"
    if name == "week":
        return "PASS" if re.search(r"^MEASURES ", out, re.M) and "TEST FAIL" not in out else "FAIL"
    return "SEE"


def install_shim(work):
    nm = os.path.join(work, "node_modules", "puppeteer-core")
    if os.path.islink(nm) or os.path.isfile(nm):
        os.remove(nm)
    elif os.path.isdir(nm):
        shutil.rmtree(nm)
    shutil.copytree(os.path.join(HERE, "shim", "puppeteer-core"), nm)


def run(assets, only=None, work=None, timeout=1200, playtest_minutes=60.0):
    """Build and run the tests, holding the work folder's lock the whole time."""
    work = work or build.DEFAULT_WORK
    with build.work_lock(work):
        results = _run(assets, only, work, timeout)
    # the playtester builds for itself (taking the same lock), so it runs after the lock is let go
    logs = os.path.join(work, "lane-test-logs")
    os.makedirs(logs, exist_ok=True)
    if results.get("build") == "FAIL":
        return results
    if (not only or "playtest" in only) and playtest_minutes > 0:
        t0 = time.time()
        out_dir = os.path.join(logs, "playtest")
        cmd = [sys.executable, os.path.join(HERE, "playtester", "playtest.py"), "--assets", assets,
               "--out", out_dir, "--minutes", str(playtest_minutes)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=max(timeout, 3600))
            out, code = p.stdout + p.stderr, p.returncode
        except subprocess.TimeoutExpired:
            out, code = "TIMEOUT", 124
        os.makedirs(logs, exist_ok=True)  # the playtester's own build clears the work folder, logs and all
        with open(os.path.join(logs, "playtest.log"), "w", encoding="utf-8") as f:
            f.write(out)
        results["playtest"] = "SEE" if code == 0 else "FAIL"
        print("%-12s %-5s %4.0f s  (reports in %s)" % ("playtest", results["playtest"], time.time() - t0, out_dir), flush=True)
    return results


def _run(assets, only, work, timeout):
    probs = build.build(assets_dir=assets, dist=os.path.join(work, "dist-check"), work=work,
                        locked=True)
    if probs:
        print("build:", "; ".join(probs))
        return {"build": "FAIL"}
    install_shim(work)
    logs = os.path.join(work, "lane-test-logs")
    os.makedirs(logs, exist_ok=True)
    env = dict(os.environ)
    results = {}
    for name in ORDER:
        if only and name not in only:
            continue
        if name == "oldsave" and not env.get("OLD"):
            results[name] = "SKIP (no OLD build given)"
            print("%-12s %s" % (name, results[name]))
            continue
        script = SCRIPTS.get(name, ["test/%s.mjs" % name])
        t0 = time.time()
        try:
            p = subprocess.run(["node"] + script, cwd=work, env=env, capture_output=True, text=True,
                               timeout=timeout)
            out, code = p.stdout + p.stderr, p.returncode
        except subprocess.TimeoutExpired as e:
            out, code = (e.stdout or "") if isinstance(e.stdout, str) else "", 124
            out += "\nTIMEOUT after %d s" % timeout
        with open(os.path.join(logs, name + ".log"), "w", encoding="utf-8") as f:
            f.write(out)
        results[name] = verdict(name, code, out)
        print("%-12s %-5s %4.0f s" % (name, results[name], time.time() - t0), flush=True)
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets", default=os.environ.get("LEDGER_PROTO_ASSETS"))
    ap.add_argument("--only")
    ap.add_argument("--work")
    ap.add_argument("--timeout", type=int, default=1200)
    ap.add_argument("--no-playtest", action="store_true")
    ap.add_argument("--playtest-minutes", type=float, default=60.0)
    a = ap.parse_args(argv)
    if not a.assets:
        print("needs the pictures: --assets DIR or LEDGER_PROTO_ASSETS")
        return 2
    res = run(a.assets, a.only.split(",") if a.only else None, a.work, a.timeout,
              0 if a.no_playtest else a.playtest_minutes)
    return 1 if any(v == "FAIL" for v in res.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
