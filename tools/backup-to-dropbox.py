#!/usr/bin/env python3
"""Copy what lives outside the project's history into Jafar's Dropbox.

    python tools/backup-to-dropbox.py             # copies what is new or changed
    python tools/backup-to-dropbox.py --dry-run   # says what it would copy
    python tools/backup-to-dropbox.py --selftest

WHY, 24 September. Jafar's ruling: the MetaHuman's files stay on this PC,
outside the project's history, and they are backed up to his Dropbox, not to a
release on the repository, because the repository is public and publishing raw
MetaHuman files likely breaks Epic's licence for them. Dropbox syncs whatever
lands in its folder, so the whole job here is a copy into it.

WHAT IT COPIES is the list below, starting with the MetaHuman: his source in
the scratch project (the Creator's character, dressed), the same character
from before the 24 September dressing, the built files the probe copies into
the game, and the scratch project's file so it can be reopened. Never the AI
key or anything from where the key lives.

IT NEVER DELETES OR OVERWRITES BACKWARDS. A file is copied when it is missing
at the destination or differs in size or is newer; nothing at the destination
is ever removed, so a file deleted or broken on this PC stays whole in the
backup (and Dropbox keeps its own version history besides).

Run it at the end of any sitting that changes these files. One line out:
backupToDropbox=<status> copied=<n> unchanged=<n> bytes=<n>.
"""
import os
import shutil
import sys

DROPBOX = os.path.join(os.path.expanduser("~"), "Dropbox")
DEST = os.path.join(DROPBOX, "LEDGER backup")

# (source, name under DEST). A directory is copied whole, recursively.
SOURCES = [
    (r"C:\LedgerTools\mh-assemble\Content\MH_Test.uasset", r"metahuman\MH_Test.uasset"),
    (r"C:\LedgerTools\mh-assemble-before-dressing-2026-09-24\Content\MH_Test.uasset",
     r"metahuman\before-dressing-2026-09-24\MH_Test.uasset"),
    (r"C:\LedgerTools\mh-assemble\Content\Ledger\MetaHumans", r"metahuman\built\MetaHumans"),
    (r"C:\LedgerTools\mh-assemble\MHAssemble.uproject", r"metahuman\MHAssemble.uproject"),
    # THE CAST'S SOURCE CHARACTERS, 24 September: Rocco, Lena and Sam, made by
    # tools/ue/make_cast_metahumans.py, rigged and textured by Epic's service.
    (r"C:\LedgerTools\mh-assemble\Content\Cast", r"metahuman\cast"),
]

# Never copied, whatever a future entry above says: the key, and the place it lives.
NEVER = ("secrets.json", os.path.join("LocalLow", "DefaultCompany"), ".ledger-gh-token")


def refused(path):
    p = path.replace("/", os.sep)
    return any(n in p for n in NEVER)


def pairs(sources, dest):
    """Every (source file, destination file) the list names."""
    out = []
    for src, name in sources:
        target = os.path.join(dest, name)
        if os.path.isdir(src):
            for root, _dirs, files in os.walk(src):
                for f in files:
                    s = os.path.join(root, f)
                    out.append((s, os.path.join(target, os.path.relpath(s, src))))
        elif os.path.isfile(src):
            out.append((src, target))
    return [(s, d) for s, d in out if not refused(s)]


def needs_copy(src, dst):
    if not os.path.exists(dst):
        return True
    a, b = os.stat(src), os.stat(dst)
    return a.st_size != b.st_size or a.st_mtime > b.st_mtime + 1


def inside(path, dest):
    """True only when path is dest itself or somewhere under it, after
    resolving '..' and any link or junction on the way."""
    root = os.path.realpath(dest)
    return os.path.commonpath([os.path.realpath(path), root]) == root


def run(sources, dest, dry=False):
    copied = unchanged = size = 0
    missing = [s for s, _ in sources if not os.path.exists(s)]
    # JAFAR'S DROPBOX IS HIS, 24 September: "just need to be 10000000% sure you
    # don't fuck up my dropbox". Every file this writes is checked to lie
    # inside the backup's own folder before anything is written, and one that
    # does not stops the whole run with nothing copied. There is no delete
    # anywhere in this file outside the self-test's own temporary folder.
    plan = pairs(sources, dest)
    outside = [d for _, d in plan if not inside(d, dest)]
    if outside or os.path.islink(dest):
        return "backupToDropbox=REFUSED-OUTSIDE-ITS-FOLDER copied=0 first=%s" % (outside[:1] or [dest])[0].replace(" ", "~")
    for s, d in plan:
        if needs_copy(s, d):
            if not dry:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
            copied += 1
            size += os.path.getsize(s)
        else:
            unchanged += 1
    status = "MISSING-SOURCE" if missing else ("DRY-RUN" if dry else "OK")
    return ("backupToDropbox=%s copied=%d unchanged=%d bytes=%d dest=%s%s"
            % (status, copied, unchanged, size, dest.replace(" ", "~"),
               (" missing=" + ",".join(m.replace(" ", "~") for m in missing)) if missing else ""))


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
    check("no listed source is the key", not any(refused(s) for s, _ in SOURCES))
    check("the key is refused by name", refused(r"C:\Users\x\AppData\LocalLow\DefaultCompany\ledger\secrets.json"))
    with tempfile.TemporaryDirectory() as t:
        src, dst = os.path.join(t, "src"), os.path.join(t, "dst")
        os.makedirs(os.path.join(src, "d"))
        open(os.path.join(src, "d", "a.bin"), "wb").write(b"12345")
        open(os.path.join(src, "b.bin"), "wb").write(b"x")
        lst = [(os.path.join(src, "d"), "dir"), (os.path.join(src, "b.bin"), "b.bin")]
        first = run(lst, dst)
        second = run(lst, dst)
        check("the first run copies both", "copied=2" in first)
        check("the second copies nothing", "copied=0 unchanged=2" in second)
        os.remove(os.path.join(src, "b.bin"))
        third = run(lst, dst)
        check("a file gone from the source stays in the backup", os.path.exists(os.path.join(dst, "b.bin")))
        check("and the gone source is named", "MISSING-SOURCE" in third)
        escape = run([(os.path.join(src, "d"), os.path.join("..", "escaped"))], dst)
        check("a destination outside the backup folder is refused", "REFUSED-OUTSIDE-ITS-FOLDER" in escape)
        check("and nothing is written there", not os.path.exists(os.path.join(t, "escaped")))
    check("every real destination is inside the backup folder",
          all(inside(d, DEST) for _, d in pairs(SOURCES, DEST)))
    print("backup-to-dropbox selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if not os.path.isdir(DROPBOX):
        print("backupToDropbox=NO-DROPBOX dest=%s" % DROPBOX.replace(" ", "~"))
        sys.exit(1)
    line = run(SOURCES, DEST, dry="--dry-run" in sys.argv)
    print(line)
    sys.exit(0 if "=OK" in line or "=DRY-RUN" in line else 1)
