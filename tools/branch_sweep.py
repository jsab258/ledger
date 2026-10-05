#!/usr/bin/env python3
"""EVERY BRANCH ON GITHUB, MEASURED AGAINST MAIN: ALREADY IN IT, HOLDING WORK NOWHERE ELSE, OR ARCHIVABLE.

Jafar, 5 October 2026 (the plan's edit 9): "Phase 0 recovers everything that exists but nobody
looks at. This morning a district map was drawn from nothing, contradicting the September atlas
on art/atlas-01, which nobody knew about. Sweep every branch on GitHub ... for each, whether it is
already in main, holds work that exists nowhere else and is worth keeping, or can be archived."

THE METHOD (git's own, nothing guessed):
  - merged:       the branch's tip is an ancestor of origin/main (git merge-base --is-ancestor);
  - equivalent:   every commit of the branch missing from main has a patch-id twin in main
                  (git cherry: no "+" lines), i.e. it was rebased or cherry-picked in;
  - content in:   not merged, but every file the branch changed is in main byte for byte as the
                  branch's tip has it (a squash or a later copy), or was deleted on both;
  - unique:       something else: the files whose content exists nowhere on main are listed.
Each branch also gets its last commit, its author, its age, how many commits main lacks, the
folders it touches, and a flag where it touches taste or identity (art, maps, faces, voices,
casting, canon, story), which goes to Jafar on one page before any merge.

  python tools/branch_sweep.py [--out production/audits/sweep-2026-10-05/branches.json]
  python tools/branch_sweep.py --selftest
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITY = ("art/", "production/art/", "atlas", "map", "canon", "casting", "CASTING", "cast/",
            "faces", "voice", "game-design/story", "story", "production/reference", "content/brands")


def git(*args, check=True):
    r = subprocess.run(("git",) + args, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), r.stderr.strip()[:300]))
    return r.stdout


def branches():
    out = git("for-each-ref", "--format=%(refname)", "refs/remotes/origin")
    return sorted(b for b in out.split() if b not in ("refs/remotes/origin/HEAD", "refs/remotes/origin/main"))


MAIN_BLOBS = None
TREES = {}


def tree(ref):
    """path -> blob for every file of a commit, read once."""
    if ref not in TREES:
        TREES[ref] = {}
        for line in git("ls-tree", "-r", "-z", ref).split("\0"):
            if line:
                meta, path = line.split("\t", 1)
                parts = meta.split()
                if parts[1] == "blob":
                    TREES[ref][path] = parts[2]
    return TREES[ref]


def main_blobs(main="origin/main"):
    """Every file content main holds, wherever it sits: a branch's file copied into main under
    another folder (a research note moved into production/research) is in main, not unique."""
    global MAIN_BLOBS
    if MAIN_BLOBS is None:
        MAIN_BLOBS = set(tree(main).values())
    return MAIN_BLOBS


def identity_flag(paths):
    hits = sorted({p for p in paths if any(k.lower() in p.lower() for k in IDENTITY)})
    return hits


def measure(br, main="origin/main"):
    tip = git("rev-parse", br).strip()
    last = git("log", "-1", "--format=%cI|%an|%s", br).strip().split("|", 2)
    age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(last[0])).days
    merged = subprocess.run(["git", "merge-base", "--is-ancestor", br, main], cwd=REPO).returncode == 0
    base = git("merge-base", br, main, check=False).strip()
    unrelated = not base
    if unrelated:   # a branch with no history in common with main (an orphan): all its files count
        base = git("hash-object", "-t", "tree", "--stdin", check=False).strip() or "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    ahead = int(git("rev-list", "--count", "%s..%s" % (main, br)).strip() or 0)
    cherry = [l for l in git("cherry", main, br).splitlines() if l.strip()]
    plus = [l for l in cherry if l.startswith("+")]
    changed = [l.split("\t") for l in git("diff", "--name-status", "--no-renames", base, br).splitlines() if l.strip()]
    paths = [c[-1] for c in changed]
    unique_files = []
    br_tree = tree(br)          # one read of each tree, not a git call per file
    main_tree = tree(main)
    for status, *rest in changed:
        path = rest[-1]
        if status == "D":
            continue            # a file this branch deleted holds no work of its own
        b_blob = br_tree.get(path, "")
        if b_blob and b_blob != main_tree.get(path) and b_blob not in main_blobs(main):
            unique_files.append(path)
    if merged:
        state = "merged"
    elif not unique_files:
        state = "content in main"
    elif not plus:
        state = "equivalent"
    else:
        state = "unique"
    folders = {}
    for p in paths:
        top = "/".join(p.split("/")[:2]) if "/" in p else p
        folders[top] = folders.get(top, 0) + 1
    return {
        "branch": br.replace("refs/remotes/origin/", "", 1), "unrelated_history": unrelated, "tip": tip[:10], "last": last[0][:10], "author": last[1],
        "subject": last[2][:160], "age_days": age, "state": state, "ahead": ahead,
        "unpicked_commits": len(plus), "files_changed": len(paths), "files_not_in_main": len(unique_files),
        "not_in_main_sample": unique_files[:40], "folders": dict(sorted(folders.items(), key=lambda kv: -kv[1])[:12]),
        "identity": identity_flag([u.split(" (")[0] for u in unique_files])[:20],
        "subjects": [s for s in git("log", "--format=%s", "%s..%s" % (main, br)).splitlines()][:25],
    }


def selftest():
    ok = True

    def check(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    check(identity_flag(["production/art/atlas/map.json", "tools/x.py"]) == ["production/art/atlas/map.json"],
          "a branch touching the atlas is flagged for his page; a tool is not")
    check(identity_flag(["canon.md"]) == ["canon.md"], "canon is identity")
    check(identity_flag(["ledger/Core/Sim.cs"]) == [], "the simulation's code is not taste")
    print("branch_sweep selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "production", "audits", "sweep-2026-10-05", "branches.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    git("fetch", "-q", "--prune", "origin")
    rows = []
    for br in branches():
        try:
            rows.append(measure(br))
        except RuntimeError as e:
            rows.append({"branch": br, "state": "error", "error": str(e)})
        print("%-50s %-16s files not in main %s" % (rows[-1]["branch"], rows[-1]["state"], rows[-1].get("files_not_in_main", "?")), flush=True)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"measured_at": dt.datetime.now().isoformat(timespec="minutes"),
                   "main": git("rev-parse", "--short", "origin/main").strip(), "branches": rows}, f, indent=1, ensure_ascii=False)
    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    print("branches=%d %s" % (len(rows), " ".join("%s=%d" % kv for kv in sorted(counts.items()))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
