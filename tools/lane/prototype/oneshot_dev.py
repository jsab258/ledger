#!/usr/bin/env python3
"""The one-shot's working loop (20 Nov 2026): build the edited source and run chosen tests, without pinning.

  python oneshot_dev.py [--work DIR] build              build with --allow-changed, pictures in, test shim in
  python oneshot_dev.py [--work DIR] test NAME [NAME..] build, then node test/NAME.mjs in the work folder
                                                        (NAME may be a path under test/, such as game/crew)
  python oneshot_dev.py [--work DIR] pieces [NAME..]    node test/pieces.mjs (no build, no browser)

Each author uses a work folder of their own (--work), so two never share one. Pictures: LEDGER_PROTO_ASSETS
or /home/claude/proto-assets. Exit 0 only when everything asked for passed (a test passes when it exits 0
and prints no TEST FAIL, FAILED or PAGEERR, the rule of run_proto_tests.py).
"""
import argparse, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402
import run_proto_tests as R  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=B.DEFAULT_WORK)
    ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument("what", choices=["build", "test", "pieces"])
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    assets = os.environ.get("LEDGER_PROTO_ASSETS", "/home/claude/proto-assets")
    if a.what == "pieces":
        return subprocess.run(["node", "test/pieces.mjs"] + a.names, cwd=os.path.join(HERE, "project")).returncode
    with B.work_lock(a.work):
        probs = B.build(assets_dir=assets, allow_changed=True, dist=os.path.join(a.work, "dist-check"), work=a.work, locked=True)
        probs = [p for p in probs if "differs from the published page" not in p]
        if probs:
            print("build:", "; ".join(probs))
            return 1
        R.install_shim(a.work)
        print("built in", a.work)
        bad = 0
        for n in a.names if a.what == "test" else []:
            t0 = time.time()
            script = R.SCRIPTS.get(n, ["test/%s.mjs" % n])
            try:
                env = dict(os.environ)
                # two authors testing at once never share a port: each work folder gets its own thousand
                env.setdefault("LEDGER_PORT_SHIFT", str(1000 * (1 + sum(map(ord, os.path.basename(a.work.rstrip("/")))) % 20)))
                p = subprocess.run(["nice", "-n", "5", "node"] + script, cwd=a.work, env=env, capture_output=True, text=True, timeout=a.timeout)
                out, code = p.stdout + p.stderr, p.returncode
            except subprocess.TimeoutExpired:
                out, code = "TIMEOUT", 124
            v = R.verdict(n.split("/")[-1], code, out)
            logs = os.path.join(a.work, "lane-test-logs")
            os.makedirs(os.path.join(logs, os.path.dirname(n)), exist_ok=True)
            open(os.path.join(logs, n + ".log"), "w", encoding="utf-8").write(out)
            print("%-22s %-5s %4.0f s" % (n, v, time.time() - t0), flush=True)
            if v == "FAIL":
                bad += 1
                print("\n".join(out.strip().splitlines()[-25:]))
        return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
