#!/usr/bin/env python3
"""one-sim: run the checks inside a real web browser (headless Chromium, through Playwright).

  python -I browser_test.py --brain one-sim.wasm --check one-sim-check.wasm \
         --golden TABLE.txt --specs production/specs --site DIR [--json OUT.json]

Copies the page (browser/index.html), the loader, the bridge and the checks (one-sim.mjs,
one-sim-bridge.mjs, checks.mjs), the
two modules, the golden table the C# Core wrote and the three data files into DIR (outside the
repository), serves DIR on this machine only, opens the page and waits for its result. The
checks are the same file the Node test runs. Exit 0 only if every check passed in the page.
"""
import argparse
import functools
import http.server
import json
import os
import shutil
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    for name in ("brain", "check", "golden", "specs", "site"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--json")
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()

    os.makedirs(a.site, exist_ok=True)
    shutil.copy(os.path.join(HERE, "browser", "index.html"), a.site)
    for f in ("one-sim.mjs", "one-sim-bridge.mjs", "checks.mjs"):
        shutil.copy(os.path.join(HERE, f), a.site)
    shutil.copy(a.brain, os.path.join(a.site, "one-sim.wasm"))
    shutil.copy(a.check, os.path.join(a.site, "one-sim-check.wasm"))
    shutil.copy(a.golden, os.path.join(a.site, "golden.txt"))
    for f in ("hook-cast.json", "quay-cast.json", "town-news.json"):
        shutil.copy(os.path.join(a.specs, f), a.site)

    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map,
                              **{".wasm": "application/wasm", ".mjs": "text/javascript", ".json": "application/json"})

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=a.site))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/index.html" % server.server_address[1]

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("NOTHING MEASURED: Playwright is not installed here, so no browser was opened.")
        return 3
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        version = browser.version
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url)
        page.wait_for_function("() => window.__oneSim !== undefined", timeout=a.timeout * 1000)
        got = page.evaluate("() => window.__oneSim")
        browser.close()
    server.shutdown()

    for line in got.get("log", []):
        print(line)
    if errors or got.get("error"):
        print("PAGE ERROR:", errors or got.get("error"))
        return 1
    report = got["report"]
    report["browser"] = "Chromium " + version
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1)
    failed = report.get("failed", 1)
    print("one-sim in a real browser (Chromium %s): %s" % (version, "%d FAILED" % failed if failed else "all passed"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
