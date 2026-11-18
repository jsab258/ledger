#!/usr/bin/env python3
"""Build the LEDGER loop prototype from its source folder into dist/.

Stage 0 (18 Nov 2026): the source is the published page as it stands
(version in src/MANIFEST.json), its game script kept in parts under 1 MB
so git's size guard passes. The build joins the parts, checks every byte
against the published checksums, and writes:

  dist/index.html, dist/ledger.js        the page and its script
  dist/publish-files.json                the `files` map for one Artifact
                                         publish: code from dist/, pictures
                                         and the people rig copied server
                                         side from the live page itself
  dist/<asset>                           only with --assets DIR (a local
                                         folder holding the pictures), for
                                         playing or testing offline

Usage:
  python build.py                 build and check
  python build.py --assets DIR    also copy the pictures in, checked
  python build.py --allow-changed build even when the code no longer
                                  matches the published checksums (for
                                  stage 1 on, once the source is edited)
"""
import argparse
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
DIST = os.path.join(HERE, "dist")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_manifest():
    with open(os.path.join(SRC, "MANIFEST.json"), encoding="utf-8") as f:
        return json.load(f)


def join_parts(manifest):
    parts = manifest["code"]["ledger.js"]["parts"]
    out = b""
    for name in parts:
        with open(os.path.join(SRC, "bundle", name), "rb") as f:
            out += f.read()
    return out


def build(assets_dir=None, allow_changed=False, dist=DIST):
    m = load_manifest()
    problems = []
    script = join_parts(m)
    with open(os.path.join(SRC, "index.html"), "rb") as f:
        page = f.read()
    for name, data in (("ledger.js", script), ("index.html", page)):
        want = m["code"][name]["sha256"]
        if sha(data) != want:
            problems.append("%s differs from the published version %s" % (name, m["version"]))
    if problems and not allow_changed:
        raise SystemExit("Build stopped: " + "; ".join(problems))
    os.makedirs(dist, exist_ok=True)
    with open(os.path.join(dist, "ledger.js"), "wb") as f:
        f.write(script)
    with open(os.path.join(dist, "index.html"), "wb") as f:
        f.write(page)
    rel = os.path.relpath(dist, REPO).replace(os.sep, "/")
    files = {"ledger.js": rel + "/ledger.js"}
    new_page_files = dict(files)
    for a in m["assets"]:
        new_page_files[a["path"]] = {"artifact": m["page"], "path": a["path"]}
        if assets_dir:
            src = os.path.join(assets_dir, a["path"])
            with open(src, "rb") as f:
                data = f.read()
            if sha(data) != a["sha256"]:
                raise SystemExit("Picture %s does not match the manifest" % a["path"])
            shutil.copyfile(src, os.path.join(dist, a["path"]))
    pub = {
        "page": m["page"],
        "built_on_version": m["version"],
        "file_path": rel + "/index.html",
        "files": files,
        "files_for_a_new_page": new_page_files,
        "paths_relative_to": "the repository root (the publish tool reads paths from the working directory)",
        "before_publishing": "Read the live page first: if its version is not built_on_version, someone changed it since; merge that first. An update keeps the pictures it does not name, so 'files' names only the script.",
        "after_publishing": "Read index.html and ledger.js back and compare their checksums with dist/.",
    }
    with open(os.path.join(dist, "publish-files.json"), "w", encoding="utf-8") as f:
        json.dump(pub, f, indent=1)
    return {"script_bytes": len(script), "page_bytes": len(page), "changed": problems, "assets": len(m["assets"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets")
    ap.add_argument("--allow-changed", action="store_true")
    a = ap.parse_args()
    r = build(a.assets, a.allow_changed)
    print("Built: script %d bytes, page %d bytes, %d pictures listed%s" % (
        r["script_bytes"], r["page_bytes"], r["assets"],
        "; CHANGED from the published version" if r["changed"] else "; identical to the published version"))


if __name__ == "__main__":
    sys.exit(main())
