#!/usr/bin/env python3
"""Run the simulation's five pre-commit gates headless, outside the repository.

The lane (cloud, Linux, no Unity) can run CLAUDE.md's simulation gates:
CoreTests, Soak, SaveChaos, PerceptionGolden (compared byte for byte with the
committed goldens in ue-probe/perception-golden/) and StrangerTest (--sweep).
Nothing is built inside the repository: each project and the C# sources are
copied to a work folder; everything else in the repository is linked read-only
by name so the tests' file lookups (they walk up from the binary) find it.

Needs the .NET 8 SDK (apt-get install dotnet-sdk-8.0). NuGet sources are
cleared: the projects use no packages, and the cloud proxy refuses nuget.org.

Usage: python3 tools/lane/sim_gates.py --repo /home/claude/ledger --work DIR
Exit 0 when all five pass; a summary line per gate is printed.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time

GATES = [
    ("CoreTests", [], "All {n} checks passed"),
    ("Soak", [], "soak ok"),
    ("SaveChaos", [], "save chaos ok"),
    ("PerceptionGolden", [], "golden rows emitted"),
    ("StrangerTest", ["--sweep"], "strangerSweep"),
]
WRITTEN = {"stranger-test"}
NUGET = ('<?xml version="1.0"?>\n<configuration><packageSources><clear/>'
         '</packageSources></configuration>\n')


def passed(name, rc, out):
    """Judge one gate from its exit code and console text."""
    if rc != 0:
        return False
    if name == "CoreTests":
        return "checks passed" in out and "FAILED" not in out
    if name == "StrangerTest":
        m = re.search(r"strangerSweep paths=(\d+)/(\d+)", out)
        return bool(m) and m.group(1) == m.group(2) and int(m.group(2)) > 0
    marker = dict((g[0], g[2]) for g in GATES)[name]
    return marker in out


def goldens_match(repo, emitted):
    """The emitted golden equals the committed parts joined in order."""
    folder = os.path.join(repo, "ue-probe", "perception-golden")
    parts = sorted(p for p in os.listdir(folder) if p.startswith("part-"))
    if not parts or not os.path.exists(emitted):
        return False
    committed = b"".join(open(os.path.join(folder, p), "rb").read() for p in parts)
    return committed == open(emitted, "rb").read()


def prepare(repo, work):
    """Fill an empty work folder; a used one would gate stale copies."""
    if os.path.exists(work) and os.listdir(work):
        raise SystemExit(f"work folder {work} is not empty: give a new one")
    lg = os.path.join(repo, "ledger")
    os.makedirs(os.path.join(work, "Assets", "Scripts"), exist_ok=True)
    for sub in ("Core", "Game"):
        dst = os.path.join(work, "Assets", "Scripts", sub)
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(lg, "Assets", "Scripts", sub), dst)
    for proj in [g[0] for g in GATES] + ["DevTools"]:
        dst = os.path.join(work, proj)
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(lg, proj), dst)
        if proj != "DevTools":
            open(os.path.join(dst, "nuget.config"), "w").write(NUGET)
    # production/ is a real folder of links, with the folders the gates write
    # into (WRITTEN) copied, so no gate can write through a link into the
    # repository (StrangerTest --sweep rewrites production/stranger-test/).
    prod = os.path.join(work, "production")
    os.makedirs(prod, exist_ok=True)
    for name in os.listdir(os.path.join(repo, "production")):
        src, dst = os.path.join(repo, "production", name), os.path.join(prod, name)
        if os.path.lexists(dst):
            continue
        if name in WRITTEN:
            shutil.copytree(src, dst)
        else:
            os.symlink(src, dst)
    for base in (repo, lg):
        for name in os.listdir(base):
            if name in (".git", "production"):
                continue
            link = os.path.join(work, name)
            if not os.path.lexists(link):
                os.symlink(os.path.join(base, name), link)


def repo_state(repo):
    """git status (ignored and every untracked file included) plus a hash of
    each listed file, to prove the gates changed nothing in the repository."""
    st = subprocess.run(["git", "status", "--porcelain", "--ignored",
                         "--untracked-files=all"], cwd=repo,
                        capture_output=True, text=True).stdout
    h = hashlib.sha256(st.encode())
    for line in st.splitlines():
        path = os.path.join(repo, line[3:].split(" -> ")[-1])
        if os.path.isfile(path):
            h.update(open(path, "rb").read())
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    if shutil.which("dotnet") is None:
        print("dotnet not found: apt-get install dotnet-sdk-8.0")
        return 2
    before = repo_state(a.repo)
    prepare(a.repo, a.work)
    ok_all = True
    for name, args, _ in GATES:
        pdir = os.path.join(a.work, name)
        b = subprocess.run(["dotnet", "build", "-c", "Release", "-v", "q"], cwd=pdir,
                           capture_output=True, text=True,
                           env=dict(os.environ, DOTNET_CLI_TELEMETRY_OPTOUT="1"))
        if b.returncode != 0:
            print(f"{name}: BUILD FAILED")
            ok_all = False
            continue
        t = time.time()
        try:
            r = subprocess.run([os.path.join(pdir, "bin", "Release", "net8.0", name)] + args,
                               cwd=pdir, capture_output=True, text=True, timeout=600)
        except (subprocess.TimeoutExpired, OSError) as e:
            print(f"{name}: FAIL ({type(e).__name__})")
            ok_all = False
            continue
        out = r.stdout + r.stderr
        ok = passed(name, r.returncode, out)
        note = ""
        if name == "PerceptionGolden" and ok:
            ok = goldens_match(a.repo, os.path.join(pdir, "perception-golden.txt"))
            note = " (identical to the committed goldens)" if ok else " (DIFFERS from the committed goldens)"
        last = out.strip().splitlines()[-1][:120] if out.strip() else ""
        print(f"{name}: {'PASS' if ok else 'FAIL'} in {time.time() - t:.0f} s{note} | {last}")
        ok_all = ok_all and ok
    if repo_state(a.repo) != before:
        print("REPOSITORY CHANGED by a gate: restore with git checkout and add the folder to WRITTEN")
        ok_all = False
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
