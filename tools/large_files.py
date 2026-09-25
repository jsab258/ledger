#!/usr/bin/env python3
"""The record of every large file or folder I create, so disk use cannot creep back.

    python tools/large_files.py add PATH --made-by "..." --why "..." [--status kept|rejected|superseded]
    python tools/large_files.py mark PATH rejected|superseded|kept [--why "..."]
    python tools/large_files.py list                # every entry, its size now and its status
    python tools/large_files.py sweep               # what the end-of-sitting sweep may delete (nothing is deleted)
    python tools/large_files.py free                # free space on C: and F:
    python tools/large_files.py --selftest

WHY, 25 September (night). Jafar: "The C: drive is full again two days after
we freed a lot of it, because nothing cleans up after itself." From now on
every file or folder of LARGE_MB or more that I create is recorded here, in
production/large-files.json, with what made it and why. At the end of a
sitting only my own entries marked rejected or superseded may go, and only
inside the places CLAUDE.md lists (tools/cleanup.py enforces the list; this
tool never deletes anything itself). Never anything I did not create, and
never by guessing that something is unused.
"""
import datetime
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORD = os.path.join(REPO, "production", "large-files.json")
LARGE_MB = 100
STATUSES = ("kept", "rejected", "superseded")


def load(path=RECORD):
    if not os.path.exists(path):
        return {"about": "Every file or folder of %d MB or more that Claude created, with what made it and why "
                         "(tools/large_files.py; CLAUDE.md, Disk)." % LARGE_MB, "entries": []}
    return json.load(open(path, encoding="utf-8"))


def save(d, path=RECORD):
    d["entries"].sort(key=lambda e: e["path"].lower())
    open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


def size_mb(path):
    if os.path.isfile(path):
        return os.path.getsize(path) / 1e6
    total = 0
    for root, _d, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / 1e6


def norm(p):
    return os.path.normpath(p).replace("\\", "/")


def add(d, path, made_by, why, status="kept", when=None):
    path = norm(path)
    e = next((x for x in d["entries"] if x["path"] == path), None)
    if e is None:
        e = {"path": path}
        d["entries"].append(e)
    e.update({"madeBy": made_by, "why": why, "status": status,
              "recorded": (when or datetime.date.today()).isoformat(),
              "mb": round(size_mb(path)) if os.path.exists(path) else e.get("mb", 0)})
    return e


def mark(d, path, status, why=None):
    assert status in STATUSES, status
    e = next(x for x in d["entries"] if x["path"] == norm(path))
    e["status"] = status
    if why:
        e["statusWhy"] = why
    return e


def sweepable(d):
    """Entries the end-of-sitting sweep may offer for deletion: mine, rejected or superseded, still there."""
    return [e for e in d["entries"] if e.get("status") in ("rejected", "superseded") and os.path.exists(e["path"])]


def free():
    out = {}
    for drive in ("C:\\", "F:\\"):
        if os.path.exists(drive):
            out[drive[0]] = round(shutil.disk_usage(drive).free / 1e9, 1)
    return out


def selftest():
    import tempfile
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("large_files selftest FAIL " + name)
    with tempfile.TemporaryDirectory() as t:
        rec = os.path.join(t, "rec.json")
        big = os.path.join(t, "big")
        os.makedirs(big)
        open(os.path.join(big, "a.bin"), "wb").write(b"x" * 1000)
        d = load(rec)
        add(d, big, "test", "a test")
        save(d, rec)
        d = load(rec)
        check("an entry is recorded with its maker and reason", d["entries"][0]["madeBy"] == "test" and d["entries"][0]["why"] == "a test")
        check("a kept entry is never offered", sweepable(d) == [])
        mark(d, big, "superseded", "a newer one")
        check("a superseded entry is offered", len(sweepable(d)) == 1)
        check("and nothing was deleted", os.path.exists(big))
    src = open(os.path.abspath(__file__), encoding="utf-8").read().split("def selftest")[0]
    check("this tool deletes nothing", all(w not in src for w in ("os.remove(", "shutil.rmtree", "os.unlink(", "os.rmdir(")))
    check("free space is read for C:", "C" in free())
    print("large_files selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    cmd = argv[0] if argv else "list"
    opt = lambda k, default=None: argv[argv.index(k) + 1] if k in argv else default
    if cmd == "free":
        print(" ".join("%s:=%s GB" % (k, v) for k, v in free().items()))
        return 0
    d = load()
    if cmd == "add":
        e = add(d, argv[1], opt("--made-by", "?"), opt("--why", "?"), opt("--status", "kept"))
        save(d)
        print("recorded %s %d MB %s" % (e["path"], e["mb"], e["status"]))
    elif cmd == "mark":
        e = mark(d, argv[1], argv[2], opt("--why"))
        save(d)
        print("marked %s %s" % (e["path"], e["status"]))
    elif cmd == "sweep":
        for e in sweepable(d):
            print("%-10s %6d MB  %s  (%s)" % (e["status"], size_mb(e["path"]), e["path"], e.get("statusWhy", e["why"])))
    else:
        for e in d["entries"]:
            now = size_mb(e["path"]) if os.path.exists(e["path"]) else 0
            print("%-10s %6d MB  %s" % (e["status"], now, e["path"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
