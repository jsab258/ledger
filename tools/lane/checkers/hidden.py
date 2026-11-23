#!/usr/bin/env python3
"""The hidden-check harness (checkers proven, 23 Nov 2026). Spec: production/lane/checkers/HIDDEN-CHECKS-SPEC.md.

Keeps the one-shot's hidden playthrough checks out of the builder's reach and turns a checker run into what the
builder and the go or no-go may see. No game knowledge here: it works on files and result records.

    python hidden.py manifest CHECKS_DIR > manifest.json          fingerprint every hidden check file (sha256)
    python hidden.py verify CHECKS_DIR manifest.json              the checks are the ones fingerprinted at the start
    python hidden.py leak CHECKS_DIR TREE [TREE..]                 any canary or check file found in the builder's tree?
    python hidden.py redact RESULTS.json > for-builder.json        what the builder may see: story id, pass or fail,
                                                                   what the player met; never the check's code
    python hidden.py verdict RESULTS.json [--need 0.5]             the go or no-go on the first-week checks

A result record (one per check per run): {"check": "W07", "story": "S05", "week": 1, "run": 1, "variant": "off-path",
"verdict": "pass" | "fail" | "not reached" | "page error", "met": "what the player met, in words", "code": "..."}.
"""
import argparse, hashlib, json, os, re, sys

CANARY = re.compile(r"LEDGER-HIDDEN-CANARY-[0-9a-f]{16}")


def files(d):
    for root, _, names in os.walk(d):
        for n in sorted(names):
            p = os.path.join(root, n)
            yield os.path.relpath(p, d).replace(os.sep, "/"), p


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def manifest(d):
    return {rel: sha(p) for rel, p in files(d)}


def verify(d, m):
    """Problems, empty when the checks are exactly the fingerprinted ones (none added, changed or missing)."""
    now = manifest(d)
    out = ["changed: " + k for k in sorted(now) if k in m and now[k] != m[k]]
    out += ["added: " + k for k in sorted(set(now) - set(m))]
    out += ["missing: " + k for k in sorted(set(m) - set(now))]
    return out


def canaries(d):
    found = set()
    for _, p in files(d):
        try:
            found |= set(CANARY.findall(open(p, encoding="utf-8", errors="ignore").read()))
        except OSError:
            pass
    return found


def leak(checks, trees):
    """Leaks of the hidden checks into the builder's trees: a canary string, or a file with the same content."""
    cans = canaries(checks)
    hashes = {sha(p): rel for rel, p in files(checks) if os.path.getsize(p) > 200}
    out = []
    for t in trees:
        for rel, p in files(t):
            if "/.git/" in "/" + rel + "/" or rel.startswith(".git/"):
                continue
            try:
                text = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for c in cans:
                if c in text:
                    out.append("canary %s in %s/%s" % (c[-6:], os.path.basename(t), rel))
            if os.path.getsize(p) > 200 and sha(p) in hashes:
                out.append("check file %s copied to %s/%s" % (hashes[sha(p)], os.path.basename(t), rel))
    return out


def redact(results):
    keep = ("story", "week", "run", "verdict", "met")
    out = []
    for r in results:
        met = CANARY.sub("[hidden]", str(r.get("met", "")))[:300]
        out.append(dict({k: r.get(k) for k in keep if k != "met"}, met=met))
    return out


def verdict(results, need=0.5):
    """Go only when at least `need` of the first-week checks really work. A check really works when every run of
    it, on every variant (the scripted path and off it), passed; a check never run, unreached or flaky fails."""
    by = {}
    for r in results:
        if r.get("week") != 1:
            continue
        by.setdefault(r["check"], []).append(r)
    if not by:
        return {"go": False, "working": 0, "of": 0, "why": "no first-week check was run"}
    working, flaky, notes = 0, 0, []
    for c, rs in sorted(by.items()):
        vs = [r.get("verdict") for r in rs]
        runs = {r.get("run") for r in rs}
        variants = {r.get("variant") for r in rs}
        ok = all(v == "pass" for v in vs) and len(runs) >= 2 and "off-path" in variants
        for var in variants:  # flaky: the same variant passed on one run and not on another
            vv = {r.get("verdict") == "pass" for r in rs if r.get("variant") == var}
            if len(vv) == 2:
                flaky += 1
                break
        path_bound = not ok and any(r.get("verdict") == "pass" for r in rs if r.get("variant") == "scripted") and \
            not any(r.get("verdict") == "pass" for r in rs if r.get("variant") == "off-path")
        if path_bound:
            notes.append(c + " (passes only on the scripted path)")
            continue
        if ok:
            working += 1
        else:
            notes.append(c)
    share = working / len(by)
    return {"go": share >= need, "working": working, "of": len(by), "share": round(share, 3), "flaky": flaky,
            "not_working": notes}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("manifest"); s.add_argument("checks")
    s = sub.add_parser("verify"); s.add_argument("checks"); s.add_argument("manifest")
    s = sub.add_parser("leak"); s.add_argument("checks"); s.add_argument("trees", nargs="+")
    s = sub.add_parser("redact"); s.add_argument("results")
    s = sub.add_parser("verdict"); s.add_argument("results"); s.add_argument("--need", type=float, default=0.5)
    a = ap.parse_args()
    if a.cmd == "manifest":
        json.dump(manifest(a.checks), sys.stdout, indent=1); return 0
    if a.cmd == "verify":
        p = verify(a.checks, json.load(open(a.manifest))); print("\n".join(p) or "the checks are the fingerprinted ones"); return 1 if p else 0
    if a.cmd == "leak":
        p = leak(a.checks, a.trees); print("\n".join(p) or "no leak"); return 1 if p else 0
    if a.cmd == "redact":
        json.dump(redact(json.load(open(a.results))), sys.stdout, indent=1); return 0
    v = verdict(json.load(open(a.results)), a.need)
    print(json.dumps(v, indent=1)); return 0 if v["go"] else 1


if __name__ == "__main__":
    sys.exit(main())
