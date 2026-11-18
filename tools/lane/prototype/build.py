#!/usr/bin/env python3
"""Build the LEDGER loop prototype from Fable's readable source (stage 1, 18 Nov 2026).

The source is project/ (Fable's round of 18 Nov, published beside the page under source/).
The build runs Fable's own build (npm ci --ignore-scripts, then node tools/build.mjs: esbuild
0.28.2 bundling src/main.js with three.js 0.187.0) in a work folder OUTSIDE the repository, so
node_modules and dist never land in git, and checks the result against PUBLISHED.json: the
published ledger.js and index.html, byte for byte.

  dist/index.html, dist/ledger.js        the page and its script
  dist/publish-files.json                the `files` map for one Artifact publish to the same
                                         page by its owner (the lane never publishes)
  dist/<asset>                           only with --assets DIR (the pictures and the people
                                         rig, checked against PUBLISHED.json)

The pictures and the people rig (13 files, 4.8 MB; people.txt is 1.5 MB, over the size guard's
1 MB) are not in git. Fetch them from the page (Artifact tool: action read, url in
PUBLISHED.json, paths = the asset names, out_dir = a folder outside the repository), or on the
PC from the page's "Source and files" zip, then check them with --check-assets DIR.

Usage:
  python build.py                     build and check against the published checksums
  python build.py --assets DIR        also copy the pictures in, checked
  python build.py --check-assets DIR  only check a folder of pictures
  python build.py --allow-changed     build even when the code no longer matches the published
                                      page (once the source is edited on purpose)
  python build.py --work DIR          the work folder (default: ~/.cache/ledger-proto-work)
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.join(HERE, "project")
DIST = os.path.join(HERE, "dist")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DEFAULT_WORK = os.path.join(os.path.expanduser("~"), ".cache", "ledger-proto-work")
SKIP = {"node_modules", "dist", "site", "out", "assets"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as f:
        return sha(f.read())


def load_published():
    with open(os.path.join(HERE, "PUBLISHED.json"), encoding="utf-8") as f:
        return json.load(f)


def check_assets(folder, published=None):
    """Problems with a folder of pictures, against PUBLISHED.json; [] when all are right."""
    published = published or load_published()
    problems = []
    for a in published["assets"]:
        p = os.path.join(folder, a["path"])
        if not os.path.isfile(p):
            problems.append("missing asset: " + a["path"])
        elif sha_file(p) != a["sha256"]:
            problems.append("asset differs from the page: " + a["path"])
    return problems


def _inside_repo(path):
    path = os.path.realpath(path)
    return path == REPO or path.startswith(REPO + os.sep)


def prepare_work(work=None, log=print):
    """Copy project/ into the work folder and install its packages there (once per lock file)."""
    work = os.path.abspath(work or DEFAULT_WORK)
    if _inside_repo(work):
        raise SystemExit("the work folder must be outside the repository: " + work)
    os.makedirs(work, exist_ok=True)
    # fresh copy of the source, keeping node_modules if the lock file is unchanged
    for name in os.listdir(work):
        if name in ("node_modules", ".lock-sha"):
            continue
        p = os.path.join(work, name)
        shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
    for name in os.listdir(PROJECT):
        if name in SKIP:
            continue
        s, d = os.path.join(PROJECT, name), os.path.join(work, name)
        shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)
    lock = sha_file(os.path.join(PROJECT, "package-lock.json"))
    stamp = os.path.join(work, ".lock-sha")
    have = open(stamp).read().strip() if os.path.exists(stamp) else ""
    if have != lock or not os.path.isdir(os.path.join(work, "node_modules", "esbuild")):
        log("npm ci --ignore-scripts (once per lock file) ...")
        subprocess.run(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"], cwd=work,
                       check=True, stdout=subprocess.DEVNULL)
        # esbuild's install script is skipped by --ignore-scripts; its platform binary still
        # arrives as an optional package, so the build works without running any package script
        with open(stamp, "w") as f:
            f.write(lock)
    return work


def build(assets_dir=None, allow_changed=False, dist=DIST, work=None, log=print):
    """Build into dist. Returns the list of problems (empty when the build matches the page)."""
    pub = load_published()
    problems = []
    if assets_dir:
        problems += check_assets(assets_dir, pub)
        if problems:
            return problems
    work = prepare_work(work, log=log)
    wa = os.path.join(work, "assets")
    os.makedirs(wa, exist_ok=True)
    if assets_dir:
        for a in pub["assets"]:
            shutil.copy2(os.path.join(assets_dir, a["path"]), os.path.join(wa, a["path"]))
    subprocess.run(["node", "tools/build.mjs"], cwd=work, check=True, stdout=subprocess.DEVNULL)
    for name, want in pub["built"].items():
        got = sha_file(os.path.join(work, "dist", name))
        if got != want["sha256"]:
            problems.append("%s differs from the published page (%s, published %s)"
                            % (name, got[:12], want["sha256"][:12]))
    if problems and not allow_changed:
        return problems
    os.makedirs(dist, exist_ok=True)
    for name in os.listdir(os.path.join(work, "dist")):
        shutil.copy2(os.path.join(work, "dist", name), os.path.join(dist, name))
    rel = os.path.relpath(dist, REPO).replace(os.sep, "/")
    publish = {
        "page": pub["page"],
        "built_on_version": pub["version"],
        "note": "For the page's owner only (the lane never publishes). Read the live page "
                "first and merge any newer change; files not named are kept on the page.",
        "files": {"ledger.js": rel + "/ledger.js"},
        "file_path": rel + "/index.html",
    }
    with open(os.path.join(dist, "publish-files.json"), "w", encoding="utf-8") as f:
        json.dump(publish, f, indent=1)
    return problems if allow_changed else []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets")
    ap.add_argument("--check-assets")
    ap.add_argument("--allow-changed", action="store_true")
    ap.add_argument("--work")
    ap.add_argument("--dist", default=DIST)
    a = ap.parse_args(argv)
    if a.check_assets:
        probs = check_assets(a.check_assets)
        print("\n".join(probs) or "all 13 assets match the page")
        return 1 if probs else 0
    probs = build(a.assets, a.allow_changed, a.dist, a.work)
    if probs:
        print("\n".join(probs))
        return 1
    print("built", a.dist, "- ledger.js and index.html match the published page byte for byte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
