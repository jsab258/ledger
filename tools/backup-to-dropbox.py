#!/usr/bin/env python3
"""Copy what Jafar has approved, and what rebuilds it, into his Dropbox.

    python tools/backup-to-dropbox.py             # copies what is new, then checks every file arrived whole
    python tools/backup-to-dropbox.py --dry-run   # says what it would copy
    python tools/backup-to-dropbox.py --verify    # copies nothing; checks every listed file against the backup
    python tools/backup-to-dropbox.py --selftest

WHY, 24 September. Jafar's ruling: the MetaHuman's files stay on this PC,
outside the project's history, and they are backed up to his Dropbox, not to a
release on the repository, because the repository is public and publishing raw
MetaHuman files likely breaks Epic's licence for them. Dropbox syncs whatever
lands in its folder, so the whole job here is a copy into it.

WHAT IT COPIES, from 25 September (night; Jafar: "make its list come from what
I have approved, today's faces and voices included, and from the sources
needed to rebuild them"): every entry of production/specs/in-game.json that
carries a "backup" list (an entry gets one when he approves it) and that
file's "backupAlso" (what rebuilds them). Each item names a path, in the
repository or outside it, and where it goes under the backup folder. The
list written on 24 September, with the old names, is retired; what it copied
stays in the backup untouched.

ITS RULES, unchanged in spirit and tightened in fact:
- It never deletes anything in Dropbox. There is no delete in this file
  outside the self-test's own temporary folder.
- It never overwrites. A file already in the backup that differs from the
  source is left as it is, and the new one is written beside the backup's
  other versions, under versions/<date-time>/ with the same relative path.
  (Until 25 September it overwrote with a newer copy.)
- It never writes outside its own folder, "LEDGER backup" in his Dropbox:
  every destination is checked, after resolving links, before anything is
  written, and one outside stops the whole run.
- It never fills drive C: (Dropbox lives there). A copy that would leave less
  than FLOOR_GB free is put off, and the run says so; items marked "first"
  (the sources to rebuild from, the voices) go before the rest.
- Every file it copies is read back and compared, byte for byte, by SHA-256.

Runs at the end of every sitting: the closing summary's commit sets it off
(tools/hooks/post-commit, installed into .git/hooks), and the summary carries
its line: backupToDropbox=<status> copied=<n> unchanged=<n> deferred=<n> ...
"""
import datetime
import hashlib
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROPBOX = os.path.join(os.path.expanduser("~"), "Dropbox")
DEST = os.path.join(DROPBOX, "LEDGER backup")
LIST = os.path.join(REPO, "production", "specs", "in-game.json")
FLOOR_GB = 1.8          # C: keeps at least this free: Windows, Dropbox and the build machine need room

# Never copied, whatever the list says: the key, and the place it lives.
NEVER = ("secrets.json", os.path.join("LocalLow", "DefaultCompany"), ".ledger-gh-token")


def refused(path):
    p = path.replace("/", os.sep)
    return any(n in p for n in NEVER)


def sources(list_path=LIST):
    """(source, name under the backup, first?) from the approved entries."""
    d = json.load(open(list_path, encoding="utf-8"))
    items = [b for e in d.get("placed", []) for b in e.get("backup", [])] + list(d.get("backupAlso", []))
    out = []
    for b in items:
        src = b["path"] if os.path.isabs(b["path"]) else os.path.join(REPO, b["path"])
        out.append((os.path.normpath(src), os.path.normpath(b["as"]), bool(b.get("first"))))
    # first things first: the sources to rebuild from and the voices
    return sorted(out, key=lambda x: not x[2])


def pairs(srcs, dest):
    """Every (source file, destination file, first?) the list names, in order."""
    out = []
    for src, name, first in srcs:
        target = os.path.join(dest, name)
        if os.path.isdir(src):
            for root, _dirs, files in os.walk(src):
                for f in sorted(files):
                    s = os.path.join(root, f)
                    out.append((s, os.path.join(target, os.path.relpath(s, src)), first))
        elif os.path.isfile(src):
            out.append((src, target, first))
    return [(s, d, f) for s, d, f in out if not refused(s)]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def same(src, dst):
    return os.path.exists(dst) and os.path.getsize(src) == os.path.getsize(dst) and sha(src) == sha(dst)


def inside(path, dest):
    """True only when path is dest itself or somewhere under it, after
    resolving '..' and any link or junction on the way."""
    root = os.path.realpath(dest)
    return os.path.commonpath([os.path.realpath(path), root]) == root


def free_gb(path):
    probe = path
    while not os.path.exists(probe):
        probe = os.path.dirname(probe)
    return shutil.disk_usage(probe).free / 1e9


def run(srcs, dest, dry=False, verify_only=False, floor_gb=FLOOR_GB, now=None):
    copied = unchanged = size = deferred = versioned = 0
    broken = []
    missing = [s for s, _, _ in srcs if not os.path.exists(s)]
    # JAFAR'S DROPBOX IS HIS, 24 September: "just need to be 10000000% sure you
    # don't fuck up my dropbox". Every file this writes is checked to lie
    # inside the backup's own folder before anything is written, and one that
    # does not stops the whole run with nothing copied.
    plan = pairs(srcs, dest)
    stamp = (now or datetime.datetime.now()).strftime("%Y-%m-%d-%H%M")
    outside = [d for _, d, _ in plan if not inside(d, dest)]
    outside += [os.path.join(dest, "versions", stamp, os.path.relpath(d, dest)) for _, d, _ in plan
                if not inside(os.path.join(dest, "versions", stamp, os.path.relpath(d, dest)), dest)]
    if outside or os.path.islink(dest):
        return "backupToDropbox=REFUSED-OUTSIDE-ITS-FOLDER copied=0 first=%s" % (outside[:1] or [dest])[0].replace(" ", "~")
    held_back = False
    for s, d, first in plan:
        if same(s, d):
            unchanged += 1
            continue
        if verify_only:
            if os.path.exists(d):
                broken.append(d)            # there, but not the same bytes
            else:
                deferred += 1               # not there yet
            continue
        target = d
        if os.path.exists(d):
            # NEVER OVERWRITTEN: the backup's copy stays; the new one goes beside it.
            target = os.path.join(dest, "versions", stamp, os.path.relpath(d, dest))
            if same(s, target):
                unchanged += 1
                continue
            versioned += 1
        need = os.path.getsize(s) / 1e9
        # ONCE A FIRST THING WAITS, NOTHING BEHIND IT TAKES ITS ROOM (25
        # September: Darren's rebuild source was put off while small built
        # files behind it still fitted).
        if free_gb(dest) - need < floor_gb or (held_back and not first):
            deferred += 1
            held_back = held_back or first
            continue
        if not dry:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(s, target)
            if not same(s, target):
                broken.append(target)
        copied += 1
        size += os.path.getsize(s)
    if verify_only:
        status = "NOT-WHOLE" if broken or missing else ("VERIFIED-SO-FAR" if deferred else "VERIFIED")
    elif broken:
        status = "BROKEN-COPY"
    elif missing:
        status = "MISSING-SOURCE"
    elif deferred:
        status = "DEFERRED-LOW-SPACE"
    else:
        status = "DRY-RUN" if dry else "OK"
    return ("backupToDropbox=%s copied=%d unchanged=%d deferred=%d versioned=%d bytes=%d freeGB=%.1f dest=%s%s%s"
            % (status, copied, unchanged, deferred, versioned, size, free_gb(dest), dest.replace(" ", "~"),
               (" missing=" + ",".join(m.replace(" ", "~") for m in missing)) if missing else "",
               (" notWhole=%d first=%s" % (len(broken), broken[0].replace(" ", "~"))) if broken else ""))


def selftest():
    import tempfile
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("backup-to-dropbox selftest FAIL " + name)
    check("the backup lands inside Dropbox", os.path.commonpath([DEST, DROPBOX]) == DROPBOX)
    real = sources()
    check("the list comes from the approved entries and names the three faces",
          sum(1 for s, n, _ in real if "Content" in s and "Cast" in s) == 3)
    check("no listed source is the key", not any(refused(s) for s, _, _ in real))
    check("the key is refused by name", refused(r"C:\Users\x\AppData\LocalLow\DefaultCompany\ledger\secrets.json"))
    check("the sources to rebuild from go first", [f for _, _, f in real] == sorted([f for _, _, f in real], reverse=True))
    with tempfile.TemporaryDirectory() as t:
        src, dst = os.path.join(t, "src"), os.path.join(t, "dst")
        os.makedirs(os.path.join(src, "d"))
        open(os.path.join(src, "d", "a.bin"), "wb").write(b"12345")
        open(os.path.join(src, "b.bin"), "wb").write(b"x")
        lst = [(os.path.join(src, "d"), "dir", True), (os.path.join(src, "b.bin"), "b.bin", False)]
        when = datetime.datetime(2026, 9, 25, 23, 30)
        first = run(lst, dst, floor_gb=0, now=when)
        second = run(lst, dst, floor_gb=0, now=when)
        check("the first run copies both, and checks them whole", "copied=2" in first and "=OK" in first)
        check("the second copies nothing", "copied=0 unchanged=2" in second)
        check("a check-only run finds them whole", "=VERIFIED " in run(lst, dst, verify_only=True, floor_gb=0))
        check("and one not yet copied is waiting, not broken",
              "VERIFIED-SO-FAR" in run(lst + [(os.path.join(src, "d"), "later", False)], dst, verify_only=True, floor_gb=0))
        open(os.path.join(src, "b.bin"), "wb").write(b"changed")
        third = run(lst, dst, floor_gb=0, now=when)
        check("a changed file is not overwritten", open(os.path.join(dst, "b.bin"), "rb").read() == b"x")
        check("it goes beside, under versions/", open(os.path.join(dst, "versions", "2026-09-25-2330", "b.bin"), "rb").read() == b"changed"
              and "versioned=1" in third)
        os.remove(os.path.join(src, "b.bin"))
        fourth = run(lst, dst, floor_gb=0, now=when)
        check("a file gone from the source stays in the backup", os.path.exists(os.path.join(dst, "b.bin")))
        check("and the gone source is named", "MISSING-SOURCE" in fourth)
        low = run([(os.path.join(src, "d"), "dir2", True)], dst, floor_gb=1e9)
        check("a copy that would fill the drive is put off", "DEFERRED-LOW-SPACE" in low and not os.path.exists(os.path.join(dst, "dir2")))
        escape = run([(os.path.join(src, "d"), os.path.join("..", "escaped"), True)], dst, floor_gb=0)
        check("a destination outside the backup folder is refused", "REFUSED-OUTSIDE-ITS-FOLDER" in escape)
        check("and nothing is written there", not os.path.exists(os.path.join(t, "escaped")))
    check("every real destination is inside the backup folder", all(inside(d, DEST) for _, d, _ in pairs(real, DEST)))
    src_text = open(os.path.abspath(__file__), encoding="utf-8").read()
    check("no delete or move in the copying code",
          all(w not in src_text.split("def selftest")[0] for w in ("os.remove(", "shutil.rmtree", "os.unlink(", "shutil.move(", "os.rename(", "os.replace(")))
    print("backup-to-dropbox selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if not os.path.isdir(DROPBOX):
        print("backupToDropbox=NO-DROPBOX dest=%s" % DROPBOX.replace(" ", "~"))
        sys.exit(1)
    line = run(sources(), DEST, dry="--dry-run" in sys.argv, verify_only="--verify" in sys.argv)
    print(line)
    sys.exit(0 if any(s in line for s in ("=OK", "=DRY-RUN", "=VERIFIED", "=DEFERRED-LOW-SPACE")) else 1)   # VERIFIED-SO-FAR too
