#!/usr/bin/env python3
"""Run the prototype's own tests (Fable's project/test/*.mjs) in the cloud's headless Chromium.

Fable's tests use puppeteer-core and a system Chrome. Here the lane builds the page from the
readable source (build.py, in a work folder outside the repository), puts its stand-in
shim/puppeteer-core (the same calls, carried out by Playwright's installed Chromium) in place of
the real package in the work folder's node_modules, and runs the tests unchanged, in Fable's
order (npm test): numbers, walks, same week, week, publish set, arrivals, nights,
town, ledger rules, layout, files, talk, eyes. oldsave runs only with
OLD=<folder holding an older build of the page>.

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

# Fable's npm test order (second round of 18 Nov), then oldsave, which needs an older build
ORDER = ["numbers", "walks", "same_week", "week", "publish_set", "arrivals", "nights", "town",
         "ledger_rules", "layout", "files", "talk", "eyes", "oldsave"]
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


def run(assets, only=None, work=None, timeout=1200):
    """Build and run the tests, holding the work folder's lock the whole time."""
    work = work or build.DEFAULT_WORK
    with build.work_lock(work):
        return _run(assets, only, work, timeout)


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
    a = ap.parse_args(argv)
    if not a.assets:
        print("needs the pictures: --assets DIR or LEDGER_PROTO_ASSETS")
        return 2
    res = run(a.assets, a.only.split(",") if a.only else None, a.work, a.timeout)
    return 1 if any(v == "FAIL" for v in res.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
