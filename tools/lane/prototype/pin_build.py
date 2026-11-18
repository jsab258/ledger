#!/usr/bin/env python3
"""Pin a new build of the lane's own round in PUBLISHED.json (the byte-for-byte check).

Usage: python pin_build.py --round "lane round 1 (eight fixes)" [--dist DIR] [--version V]
Moves the current pin under "previous" (once per version) and records ledger.js and index.html
from DIST (default: dist/, written by build.py --allow-changed). The page's version is filled in
after publishing (--version), since the page names it only then.
"""
import argparse, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))


def sha(path):
    with open(path, "rb") as f:
        b = f.read()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def pin(round_name, dist, version=None, read=None):
    p = os.path.join(HERE, "PUBLISHED.json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    new = {"ledger.js": sha(os.path.join(dist, "ledger.js")), "index.html": sha(os.path.join(dist, "index.html"))}
    if new != d["built"]:
        prev = d.setdefault("previous", [])
        if not any(x.get("version") == d["version"] for x in prev):
            prev.insert(0, {"version": d["version"], "round": d.get("round", "Fable's second round of 18 Nov"),
                            "ledger.js": d["built"]["ledger.js"], "index.html": d["built"]["index.html"]})
        d["built"] = new
        d["round"] = round_name
    if version:
        d["version"] = version
    if read:
        d["read"] = read
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1)
        f.write("\n")
    return d


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--dist", default=os.path.join(HERE, "dist"))
    ap.add_argument("--version")
    ap.add_argument("--read")
    a = ap.parse_args()
    d = pin(a.round, a.dist, a.version, a.read)
    print("pinned", d["built"]["ledger.js"]["sha256"][:12], d["built"]["index.html"]["sha256"][:12])
