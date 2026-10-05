#!/usr/bin/env python3
"""NOTHING LARGE AND NOTHING FROM THE OLD HISTORY REACHES GITHUB AGAIN: THE GUARD BEFORE EVERY PUSH.

Jafar, 5 October 2026, after the history was cleaned into a new repository (30.8 GB to about
3 GB): "Make sure this never happens again, with checks that fail loudly, not rules: a guard on
this PC before every push, no file over 1 MB and no picture outside production/previews/ or over
500 KB within it ... any push containing a commit from the old history, found through the map,
is rejected."

For every commit a push would add (not already on GitHub, and not one of the cleaned history's
own commits, which are the baseline), it refuses:
  - a file added or changed that is over 1 MB;
  - a picture or film added or changed outside production/previews/;
  - a picture in production/previews/ of 500 KB or more;
  - any commit of the old history: every old fingerprint is in the map of old to new commits,
    production/audits/history-clean-2026-10/commit-map.txt.

  git pre-push hook (tools/hooks/pre-push):  python tools/push_guard.py <remote> <url>  < refs on stdin
  CI on every push (ledger-push-guard.yml):  python tools/push_guard.py --range BEFORE AFTER
                                         and  python tools/push_guard.py --branch HEAD
  the build machine before its commit:     python tools/push_guard.py --staged --build-machine
  python tools/push_guard.py --selftest
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(REPO, "production", "audits", "history-clean-2026-10", "commit-map.txt")
FILE_LIMIT = 1_000_000
PREVIEWS = "production/previews/"
PREVIEW_LIMIT = 500_000
PICTURES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tga", ".tif", ".tiff", ".exr", ".hdr",
            ".psd", ".dds", ".heic", ".avif", ".mp4", ".mov", ".avi", ".webm", ".mkv"}
ZERO = "0" * 40


def git(*args, check=True, repo=None):
    r = subprocess.run(("git",) + args, cwd=repo or REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), r.stderr.strip()[:300]))
    return r.stdout


def load_map(path=MAP):
    """(old fingerprints, cleaned baseline fingerprints) from the map."""
    old, new = set(), set()
    if not os.path.exists(path):
        return None, None
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and len(parts[0]) == 40:
                old.add(parts[0])
                if parts[1] != ZERO:
                    new.add(parts[1])
    return old, new


def verdict(path, size):
    """Why a file added or changed may not be pushed, or None."""
    ext = os.path.splitext(path)[1].lower()
    if ext in PICTURES:
        if not path.startswith(PREVIEWS):
            return "a picture outside %s" % PREVIEWS
        if size >= PREVIEW_LIMIT:
            return "a preview of %d KB, at or over the 500 KB a preview may be" % (size // 1000)
    if size > FILE_LIMIT:
        return "%.1f MB, over the 1 MB any file may be" % (size / 1e6)
    return None


def commits_to_check(local_sha, remote_sha, baseline, remote="origin", repo=None):
    """Every commit the push would add that is not already on THE REMOTE BEING PUSHED TO.
    5 October, found by the guard's own test: excluding what any remote knew let an old commit
    through, because the private archive (another remote) knows every old commit. Only the
    target remote's branches count as already there."""
    if local_sha == ZERO:
        return []
    if remote is None:
        # THE WHOLE BRANCH SINCE THE CLEANING (--branch): nothing counts as already checked but the
        # cleaned baseline, so a commit that reached GitHub unguarded is found at the next push.
        out = git("rev-list", local_sha, repo=repo)
    elif remote_sha != ZERO and git("cat-file", "-t", remote_sha, check=False, repo=repo).strip() == "commit":
        out = git("rev-list", local_sha, "^" + remote_sha, repo=repo)
    else:
        out = git("rev-list", local_sha, "--not", "--remotes=%s" % remote, repo=repo)
    return [c for c in out.split() if c not in baseline]


def files_of(commit, repo=None):
    """(path, size) of every file the commit adds or changes (against its first parent)."""
    out = git("diff-tree", "--root", "-r", "--no-commit-id", "-z", "--diff-filter=AMCR", "--no-renames", commit, repo=repo)
    parts = out.split("\0")
    res = []
    i = 0
    while i + 1 < len(parts):
        meta, path = parts[i], parts[i + 1]
        i += 2
        if not meta.startswith(":"):
            continue
        blob = meta.split()[3]
        size = int(git("cat-file", "-s", blob, repo=repo).strip() or 0)
        res.append((path, size))
    return res


def check(pairs, out=sys.stdout, map_path=MAP, remote="origin", repo=None):
    old, baseline = load_map(map_path)
    if old is None:
        print("push-guard FAIL the map of old to new commits is missing (%s): nothing is pushed unmeasured" % map_path, file=out)
        return 1
    bad, seen = [], 0
    for local_sha, remote_sha in pairs:
        for c in commits_to_check(local_sha, remote_sha, baseline, remote, repo):
            seen += 1
            if c in old:
                bad.append("%s is a commit of the old history (it is in the map of old to new commits)" % c[:10])
                continue
            for path, size in files_of(c, repo):
                why = verdict(path, size)
                if why:
                    bad.append("%s %s: %s" % (c[:10], path, why))
    for b in bad:
        print("push-guard REFUSED " + b, file=out)
    print("push-guard commits=%d refused=%d outcome=%s" % (seen, len(bad), "FAIL" if bad else "PASS"), file=out)
    return 1 if bad else 0


def selftest():
    import tempfile
    ok = True

    def t(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    t(verdict("production/art/x.png", 10) is not None, "a picture outside production/previews/ is refused, however small")
    t(verdict("production/previews/a-2026-10-05.jpg", 499_999) is None, "a preview under 500 KB passes")
    t(verdict("production/previews/a-2026-10-05.jpg", 500_000) is not None, "a preview of 500 KB is refused")
    t(verdict("production/assets/street/quay-street.glb", 1_000_001) is not None, "a mesh over 1 MB is refused")
    t(verdict("production/audits/history-clean-2026-10/commit-map.txt", 400_000) is None, "a text file under 1 MB passes")
    t(verdict("production/d1-probe/ue-vign_hook_day.MP4", 5) is not None, "a film is a picture too, whatever its case")
    d = tempfile.mkdtemp()
    m = os.path.join(d, "map.txt")
    with open(m, "w") as f:
        f.write("old new\n" + "a" * 40 + " " + "b" * 40 + "\n" + "c" * 40 + " " + ZERO + "\n")
    old, new = load_map(m)
    t(old == {"a" * 40, "c" * 40} and new == {"b" * 40}, "the map gives the old fingerprints and the cleaned baseline")
    sink = __import__("io").StringIO()
    t(check([], sink, os.path.join(d, "missing.txt")) == 1, "no map, no push: nothing passes unmeasured")
    t(is_text(b"probeTest=PASS\n") and not is_text(b"\x89PNG\0\0"), "text is told from a binary by its bytes")
    # A TINY REPOSITORY, as the real one stands since 5 October: an old commit the archive (another
    # remote) knows, a cleaned baseline on the remote being pushed to, and new work on top.
    r = tempfile.mkdtemp()
    def rg(*a):
        return subprocess.run(("git",) + a, cwd=r, capture_output=True, text=True).stdout.strip()
    rg("init", "-q"); rg("config", "user.email", "t@t"); rg("config", "user.name", "t")
    open(os.path.join(r, "a.txt"), "w").write("old")
    rg("add", "a.txt"); rg("commit", "-q", "-m", "old")
    old_c = rg("rev-parse", "HEAD")
    rg("update-ref", "refs/remotes/archive/main", old_c)
    rg("checkout", "-q", "--orphan", "clean")
    open(os.path.join(r, "a.txt"), "w").write("cleaned")
    rg("add", "a.txt"); rg("commit", "-q", "-m", "cleaned")
    base = rg("rev-parse", "HEAD")
    rg("update-ref", "refs/remotes/origin/main", base)
    with open(os.path.join(r, "big.bin"), "wb") as f:
        f.write(b"x" * 1_100_000)
    rg("add", "big.bin"); rg("commit", "-q", "-m", "big")
    big = rg("rev-parse", "HEAD")
    mp = os.path.join(r, "map.txt")
    with open(mp, "w") as f:
        f.write("old new\n%s %s\n" % (old_c, base))
    sink2 = __import__("io").StringIO()
    t(check([(old_c, ZERO)], sink2, mp, "origin", r) == 1, "an old commit is refused even when the archive, another remote, knows it")
    t(check([(big, base)], sink2, mp, "origin", r) == 1, "a new commit carrying a file over 1 MB is refused")
    t(check([(base, ZERO)], sink2, mp, "origin", r) == 0, "the cleaned baseline itself passes")
    rg("update-ref", "refs/remotes/origin/main", big)
    t(check([(big, ZERO)], sink2, mp, None, r) == 1, "a big file already on the remote is still found when the whole branch is read")
    t(check([(base, ZERO)], sink2, mp, None, r) == 0, "the whole branch read back to the baseline passes")
    print("push_guard selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


# THE BUILD MACHINE COMMITS ONLY TEXT (Jafar, 5 October: "the build machine writes only text back
# to git, its pictures to the drive"). Its one exception, named so it is seen: the three small
# material files the Unreal cook needs and the build itself remakes (ledger-probe-unreal.yml).
BUILD_MACHINE_BINARIES = {"ue-probe/Content/Ledger/M_LedgerSurface.uasset",
                          "ue-probe/Content/Ledger/T_LedgerDefaultNormal.uasset",
                          "ue-probe/Content/Ledger/T_LedgerDefaultRough.uasset"}


def is_text(data):
    return b"\0" not in data[:8192]


def staged(build_machine, out=sys.stdout):
    """Refuses what is staged for the next commit by the push limits; for the build machine,
    also any picture at all and anything that is not text but the named material files."""
    names = [n for n in git("diff", "--cached", "--name-only", "-z", "--diff-filter=AMCR", "--no-renames").split("\0") if n]
    bad = []
    for n in names:
        blob = git("rev-parse", ":" + n).strip()
        size = int(git("cat-file", "-s", blob).strip() or 0)
        why = verdict(n, size)
        if build_machine and not why:
            if os.path.splitext(n)[1].lower() in PICTURES:
                why = "a picture: the build machine's pictures go to the drive"
            elif n not in BUILD_MACHINE_BINARIES:
                data = subprocess.run(["git", "cat-file", "blob", blob], cwd=REPO, capture_output=True).stdout
                if not is_text(data):
                    why = "not text: the build machine commits only text"
        if why:
            bad.append("%s: %s" % (n, why))
    for b in bad:
        print("push-guard REFUSED staged " + b, file=out)
    print("push-guard staged=%d refused=%d outcome=%s" % (len(names), len(bad), "FAIL" if bad else "PASS"), file=out)
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--staged" in argv:
        return staged("--build-machine" in argv)
    if "--branch" in argv:
        # 5 October: a push made by a workflow with GitHub's own token starts no other workflow, so
        # ledger-push-guard.yml never sees the build machine's pushes. This re-reads the whole
        # branch since the cleaning on every push that does start it.
        return check([(git("rev-parse", argv[argv.index("--branch") + 1]).strip(), ZERO)], remote=None)
    if "--range" in argv:
        i = argv.index("--range")
        before, after = argv[i + 1], argv[i + 2]
        return check([(after, before)])
    pairs = []
    for line in sys.stdin.read().splitlines():
        p = line.split()
        if len(p) == 4:
            pairs.append((p[1], p[3]))
    remote = argv[0] if argv and not argv[0].startswith("-") else "origin"
    return check(pairs, remote=remote)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
