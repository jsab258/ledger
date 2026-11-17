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

Runs once a day: since 9 Nov 2026 the day's first commit sets it off
(tools/hooks/post-commit, installed into .git/hooks; until then the closing
summary's commit in FOR-JAFAR.md did, now stopped), and its line goes to
backup-to-dropbox.log in the shared git folder:
backupToDropbox=<status> copied=<n> unchanged=<n> deferred=<n> ...
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
FLOOR_GB = 40.0         # C: keeps at least this free (C:'s floor in RULINGS; advisor 197, 17 Nov: raised from 1.8)
STALE_HOURS = 26        # advisor 197: a last good backup older than this is an item on his page that hour
KILN = "F:/LedgerTools/tool-dev/kiln"
BUNDLE = "F:/LedgerTools/backup-staging/kiln.bundle"   # Kiln's whole history, one file, remade each night (no GitHub)

# Never copied, whatever the list says: the key, and the place it lives.
NEVER = ("secrets.json", os.path.join("LocalLow", "DefaultCompany"), ".ledger-gh-token",
         os.path.join("LedgerTools", "keys"), "aesKeys", ".env", "api-key", "apikey")


NEVER_NAMES = ("secrets.json", "aeskeys", "api_key", "api-key", "apikey", "token.txt", "id_rsa", "id_ed25519",
               "credentials.json", ".ledger-gh-token", ".env", ".netrc")
NEVER_DIRS = (os.path.join("ledgertools", "keys"), os.path.join("locallow", "defaultcompany"), "fmodel", ".ssh")


def refused(path):
    """Never copied: the keys and anything named like a secret, judged case-blind on the path and its real target."""
    for p in {path, os.path.realpath(path)}:
        low = p.replace("/", os.sep).lower()
        name = os.path.basename(low)
        if any(n in name for n in NEVER_NAMES) or any(d in low for d in NEVER_DIRS):
            return True
    return False


def sources(list_path=LIST):
    """(source, name under the backup, first?[, folder names left out]) from the approved entries."""
    d = json.load(open(list_path, encoding="utf-8"))
    items = [b for e in d.get("placed", []) for b in e.get("backup", [])] + list(d.get("backupAlso", []))
    out = []
    for b in items:
        src = b["path"] if os.path.isabs(b["path"]) else os.path.join(REPO, b["path"])
        ex = tuple(b.get("exclude", ()))
        out.append((os.path.normpath(src), os.path.normpath(b["as"]), bool(b.get("first"))) + ((ex,) if ex else ()))
    # first things first: the sources to rebuild from and the voices
    return sorted(out, key=lambda x: not x[2])


def pairs(srcs, dest):
    """Every (source file, destination file, first?) the list names, in order."""
    out = []
    for item in srcs:
        src, name, first = item[:3]
        exclude = set(item[3]) if len(item) > 3 else set()
        target = os.path.join(dest, name)
        if os.path.isdir(src):
            for root, dirs, files in os.walk(src):
                dirs[:] = [x for x in dirs if x not in exclude and not linked(os.path.join(root, x))]
                files = [f for f in files if not linked(os.path.join(root, f))]
                for f in sorted(files):
                    s = os.path.join(root, f)
                    out.append((s, os.path.join(target, os.path.relpath(s, src)), first))
        elif os.path.isfile(src):
            out.append((src, target, first))
    return [(s, d, f) for s, d, f in out if not refused(s)]


def linked(path):
    """A symbolic link or a junction: never followed by the backup."""
    return os.path.islink(path) or bool(getattr(os.path, "isjunction", lambda _p: False)(path))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def same(src, dst):
    return os.path.exists(dst) and os.path.getsize(src) == os.path.getsize(dst) and sha(src) == sha(dst)


# ITS OWN FINGERPRINTS (advisor 198, 17 Nov): the backup keeps a SHA-256 manifest of every file it has written, on F:
# beside the Kiln bundle, so a run compares a source with the manifest instead of reading the backup's copy. A copy
# that is online-only in Dropbox is then never pulled down again just to be compared. A file the manifest does not
# know is compared the old way once (reading the backup) and recorded. --verify and --restore-check still read the
# backup itself: they are the checks that the manifest is true.
MANIFEST = "F:/LedgerTools/backup-staging/manifest.json"


def load_manifest(path):
    try:
        m = json.load(open(path, encoding="utf-8")) if path and os.path.exists(path) else {}
    except (OSError, ValueError):
        return {}
    return m if isinstance(m, dict) else {}


def save_manifest(man, path):
    if not path:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".new"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(man, fh)
    shutil.copyfile(tmp, path)      # the manifest on F: only, never inside Dropbox


def known_same(src, dst, man):
    """same(), from the manifest when it knows dst; the backup's copy is read only for a file it does not know."""
    key = os.path.normcase(os.path.abspath(dst))
    e = man.get(key)
    if e is not None:
        st = os.stat(src)
        if st.st_size != e["size"] or not os.path.exists(dst) or os.path.getsize(dst) != e["size"]:
            return False
        if e.get("srcMtime") == st.st_mtime:
            return True
        h = sha(src)
        if h == e["sha"]:
            e["srcMtime"] = st.st_mtime
            return True
        return False
    if same(src, dst):
        record(man, src, dst)
        return True
    return False


def record(man, src, dst, digest=None):
    st = os.stat(src)
    man[os.path.normcase(os.path.abspath(dst))] = {"sha": digest or sha(src), "size": st.st_size, "srcMtime": st.st_mtime}


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


def run(srcs, dest, dry=False, verify_only=False, floor_gb=FLOOR_GB, now=None, manifest=None):
    copied = unchanged = size = deferred = versioned = 0
    man = load_manifest(manifest)
    eq = same if verify_only else (lambda a, b: known_same(a, b, man))   # --verify reads the backup itself
    broken = []
    missing = [x[0] for x in srcs if not os.path.exists(x[0])]
    # JAFAR'S DROPBOX IS HIS, 24 September: "just need to be 10000000% sure you
    # don't fuck up my dropbox". Every file this writes is checked to lie
    # inside the backup's own folder before anything is written, and one that
    # does not stops the whole run with nothing copied.
    plan = pairs(srcs, dest)
    stamp = (now or datetime.datetime.now()).strftime("%Y-%m-%d-%H%M")
    outside = [d for _, d, _ in plan if not inside(d, dest)]
    outside += [os.path.join(dest, "versions", stamp, os.path.relpath(d, dest)) for _, d, _ in plan
                if not inside(os.path.join(dest, "versions", stamp, os.path.relpath(d, dest)), dest)]
    if outside or linked(dest):
        return "backupToDropbox=REFUSED-OUTSIDE-ITS-FOLDER copied=0 first=%s" % (outside[:1] or [dest])[0].replace(" ", "~")
    held_back = False
    for s, d, first in plan:
        if eq(s, d):
            unchanged += 1
            continue
        if verify_only:
            rel = os.path.relpath(d, dest)
            vroot = os.path.join(dest, "versions")
            if os.path.isdir(vroot) and any(same(s, os.path.join(vroot, v, rel)) for v in os.listdir(vroot)
                                            if os.path.exists(os.path.join(vroot, v, rel))):
                unchanged += 1              # the change is held beside, under versions/: not damage
            elif os.path.exists(d):
                broken.append(d)            # there, but not the same bytes
            else:
                deferred += 1               # not there yet
            continue
        target = d
        if os.path.exists(d):
            # NEVER OVERWRITTEN: the backup's copy stays; the new one goes beside it.
            target = os.path.join(dest, "versions", stamp, os.path.relpath(d, dest))
            if eq(s, target):
                unchanged += 1
                continue
            # UNLESS AN EARLIER VERSION ALREADY HOLDS THESE BYTES (3 October: the cast rebuilt
            # without Epic's clothes was copied again, 1.46 GB, at every summary's commit,
            # because only the first copy was compared).
            rel = os.path.relpath(d, dest)
            vroot = os.path.join(dest, "versions")
            if os.path.isdir(vroot) and any(eq(s, os.path.join(vroot, v, rel))
                                            for v in sorted(os.listdir(vroot), reverse=True)
                                            if os.path.exists(os.path.join(vroot, v, rel))):
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
            # TWO RUNS IN ONE MINUTE (backup review, 17 Nov, low): the minute's versions folder may already hold this
            # file with other bytes; never write over it, take the next free folder beside it instead.
            n = 2
            while target != d and os.path.exists(target):
                target = os.path.join(dest, "versions", "%s-%d" % (stamp, n), os.path.relpath(d, dest))
                n += 1
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(s, target)
            if not same(s, target):        # the fresh local copy, read back once by SHA-256
                broken.append(target)
            else:
                record(man, s, target)
        copied += 1
        size += os.path.getsize(s)
    if not dry and not verify_only:
        save_manifest(man, manifest)
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


def stale(lines, now=None):
    """(stale?, hours since the last good run or None): only a plain OK counts (a DEFERRED night is not a backup)."""
    now = now or datetime.datetime.now()
    last = None
    for ln in lines:
        if "backupToDropbox=OK" in ln and "bundle=FAILED" not in ln:
            try:
                when = datetime.datetime.strptime(ln.split()[0], "%Y-%m-%dT%H:%M:%S")
            except (ValueError, IndexError):
                continue
            if when <= now:         # a date in the future never counts
                last = when
    if last is None:
        return True, None
    hours = (now - last).total_seconds() / 3600
    return hours > STALE_HOURS, hours


def log_path():
    import subprocess
    common = subprocess.run(["git", "-C", REPO, "rev-parse", "--git-common-dir"], capture_output=True, text=True).stdout.strip()
    return os.path.join(common if os.path.isabs(common) else os.path.join(REPO, common), "backup-to-dropbox.log")


def make_bundle():
    """Kiln's whole history as one file (advisor 197: Dropbox only, no GitHub repository). Written to the staging
    folder on F:, never into Dropbox directly; the copy then keeps each changed night's bundle under versions/."""
    import subprocess
    os.makedirs(os.path.dirname(BUNDLE), exist_ok=True)
    tmp = BUNDLE + ".new"
    r = subprocess.run(["git", "-C", KILN, "bundle", "create", tmp, "--all"], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(tmp):
        return "bundle=FAILED"
    shutil.copyfile(tmp, BUNDLE)   # the staging file on F: only, outside Dropbox
    return "bundle=OK"


def restore_check(srcs, dest, n=20, seed=None):
    """Weekly (advisor 197): about n files sampled across the listed folders, copied back from the backup into a
    temporary folder and compared with the source by SHA-256 (a source changed since is compared with its newest
    version). Reads the backup; writes only the temporary folder."""
    import random
    import tempfile
    plan = [(s, d) for s, d, _ in pairs(srcs, dest) if os.path.exists(d)]
    pick = random.Random(seed).sample(plan, min(n, len(plan)))
    vroot = os.path.join(dest, "versions")
    bad = []
    with tempfile.TemporaryDirectory() as t:
        for i, (s, d) in enumerate(pick):
            if free_gb(t) - os.path.getsize(d) / 1e9 < FLOOR_GB:
                continue        # the temporary copy never takes C: below its floor (backup review 17 Nov)
            back = os.path.join(t, "%02d_%s" % (i, os.path.basename(d)))
            shutil.copy2(d, back)
            if not os.path.exists(s) or sha(back) == sha(s):
                continue
            rel = os.path.relpath(d, dest)
            held = os.path.isdir(vroot) and any(same(s, os.path.join(vroot, v, rel)) for v in os.listdir(vroot)
                                                if os.path.exists(os.path.join(vroot, v, rel)))
            if not held:
                bad.append(d)
    return "restoreCheck=%s sampled=%d differ=%d%s" % ("OK" if not bad else "DIFFER", len(pick), len(bad),
                                                       (" first=" + bad[0].replace(" ", "~")) if bad else "")


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
    check("the list comes from the approved entries and names the four faces, Tom's included",
          sum(1 for x in real if "Content" in x[0] and "Cast" in x[0]) == 4
          and any("MH_TomL1" in x[0] for x in real))
    check("no listed source is the key", not any(refused(x[0]) for x in real))
    check("the keys folder and an .env are refused", refused(r"F:\LedgerTools\keys\a.txt") and refused(r"F:\x\.env"))
    check("Kiln, the game inputs and the judge folder are listed",
          all(any(os.path.normpath(w) == x[0] for x in real) for w in (KILN, "F:/LedgerTools/game-inputs",
                                                                       "F:/LedgerTools/tool-dev/judge", BUNDLE)))
    check("Kiln's build folders and run outputs are left out",
          any(x[0] == os.path.normpath(KILN) and {"target", "out", ".git"} <= set(x[3] if len(x) > 3 else ()) for x in real))
    check("the key is refused by name", refused(r"C:\Users\x\AppData\LocalLow\DefaultCompany\ledger\secrets.json"))
    check("the sources to rebuild from go first", [x[2] for x in real] == sorted([x[2] for x in real], reverse=True))
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
        again = run(lst, dst, floor_gb=0, now=datetime.datetime(2026, 9, 26, 7, 0))
        check("a changed file already held as a version is not copied again", "versioned=0" in again and "copied=0" in again)
        open(os.path.join(src, "b.bin"), "wb").write(b"changed twice")
        run(lst, dst, floor_gb=0, now=when)
        check("a second change in the same minute never writes over that minute's version",
              open(os.path.join(dst, "versions", "2026-09-25-2330", "b.bin"), "rb").read() == b"changed"
              and open(os.path.join(dst, "versions", "2026-09-25-2330-2", "b.bin"), "rb").read() == b"changed twice")
        os.remove(os.path.join(src, "b.bin"))
        fourth = run(lst, dst, floor_gb=0, now=when)
        check("a file gone from the source stays in the backup", os.path.exists(os.path.join(dst, "b.bin")))
        check("and the gone source is named", "MISSING-SOURCE" in fourth)
        low = run([(os.path.join(src, "d"), "dir2", True)], dst, floor_gb=1e9)
        check("a copy that would fill the drive is put off", "DEFERRED-LOW-SPACE" in low and not os.path.exists(os.path.join(dst, "dir2")))
        os.makedirs(os.path.join(src, "k", "target"))
        open(os.path.join(src, "k", "target", "big.exe"), "wb").write(b"b")
        open(os.path.join(src, "k", "main.rs"), "wb").write(b"m")
        run([(os.path.join(src, "k"), "kiln", True, ("target",))], dst, floor_gb=0, now=when)
        check("an excluded folder is not copied, the rest is",
              os.path.exists(os.path.join(dst, "kiln", "main.rs")) and not os.path.exists(os.path.join(dst, "kiln", "target")))
        check("a log line older than 26 h is stale, a fresh one is not",
              stale(["2026-09-24T04:00:00 abc backupToDropbox=OK copied=0"], when)[0]
              and not stale(["2026-09-25T04:00:00 abc backupToDropbox=OK copied=0"], when)[0])
        check("a failed run does not count as the last good one",
              stale(["2026-09-24T04:00:00 a backupToDropbox=OK", "2026-09-25T20:00:00 b backupToDropbox=BROKEN-COPY"], when)[0])
        check("the restore check finds the copies whole", restore_check(lst, dst, seed=1).startswith("restoreCheck=OK"))
        check("keys are refused case-blind", refused("F:/LedgerTools/Keys/x.txt") and refused("C:/a/Secrets.JSON"))
        check("a stale line after a failed bundle", stale(["2026-09-25T04:00:00 a bundle=FAILED backupToDropbox=OK"], when)[0])
        check("a DEFERRED night is not a backup", stale(["2026-09-25T04:00:00 a backupToDropbox=DEFERRED-LOW-SPACE"], when)[0])
        mpath = os.path.join(t, "manifest.json")
        run(lst[:1], os.path.join(t, "dst3"), floor_gb=0, now=when, manifest=mpath)
        man = load_manifest(mpath)
        check("the manifest records each file written", len(man) == 1 and all(len(e["sha"]) == 64 for e in man.values()))
        reads = []
        global sha
        real_sha = sha
        sha = lambda pth: reads.append(pth) or real_sha(pth)
        again3 = run(lst[:1], os.path.join(t, "dst3"), floor_gb=0, now=when, manifest=mpath)
        sha = real_sha
        check("a second run compares with the manifest and reads no backup copy",
              "copied=0 unchanged=1" in again3 and not any(os.path.join(t, "dst3") in r for r in reads))
        lost = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(t, "dst3")) for f in fs][0]
        open(lost, "wb").write(b"")
        check("a damaged copy the manifest knows is noticed", "unchanged=1" not in run(lst[:1], os.path.join(t, "dst3"),
                                                                                   floor_gb=0, now=when, manifest=mpath))
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
    if "--stale" in sys.argv:
        lines = open(log_path(), encoding="utf-8").read().splitlines() if os.path.exists(log_path()) else []
        is_stale, hours = stale(lines)
        print("backupStale=%s hours=%s" % ("YES" if is_stale else "no", "none" if hours is None else "%.1f" % hours))
        sys.exit(1 if is_stale else 0)
    if "--restore-check" in sys.argv:
        line = restore_check(sources(), DEST)
        print(line)
        sys.exit(0 if "=OK" in line else 1)
    pre = ""
    if not ("--dry-run" in sys.argv or "--verify" in sys.argv):
        pre = make_bundle() + " "
    line = run(sources(), DEST, dry="--dry-run" in sys.argv, verify_only="--verify" in sys.argv, manifest=MANIFEST)
    print(pre + line)
    if "--log" in sys.argv:
        # THE NIGHTLY RUN (advisor 197: about 05:00 through Windows' Task Scheduler, after retention, whether or not
        # there was a commit): the line goes to the same log the post-commit hook writes and --stale reads.
        import subprocess
        head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        with open(log_path(), "a", encoding="utf-8") as fh:
            fh.write("%s %s %s\n" % (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), head or "-", pre + line))
    sys.exit(0 if any(s in line for s in ("=OK", "=DRY-RUN", "=VERIFIED", "=DEFERRED-LOW-SPACE")) else 1)   # VERIFIED-SO-FAR too
