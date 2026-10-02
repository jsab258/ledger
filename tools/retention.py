#!/usr/bin/env python3
"""Retention for drives C: and F:: what this project keeps, measured and enforced every night.

    python tools/retention.py census [--since ISO] [--out FILE]   # every place of the project's, folder by folder, largest first
    python tools/retention.py plan                                 # what the limits would delete now (nothing is deleted)
    python tools/retention.py run                                  # deletes what the limits say, logs each deletion
    python tools/retention.py delete PATH --why "..."              # one deletion by hand, through the same checks and log
    python tools/retention.py nightly                              # census, run, census, the morning line (Task Scheduler, 04:30)
    python tools/retention.py space --job "what" [--drives CF] [--need-c 40 --need-f 20]   # before any build, render or large job
    python tools/retention.py line                                 # the overview's first line, from the last two censuses
    python tools/retention.py --selftest

WHY, 2 October. On the night of 1 October C: reached 0 bytes and the build
machine's runner crashed; F: was down to 2.4 GB. Jafar: "I suspect it is
mostly waste that nothing ever deletes: the cleanup rule only covers files you
recorded yourself, only at the end of a day, and with goals running nonstop
that barely happens." His ruling: a fixed limit for every kind of output,
enforced by a script that runs by itself every night inside the project's
places and nowhere else, never touching his own files, logging what it
deleted; a line at the top of the overview each morning; and a free-space
check before every build, render or large job (C: keeps 40 GB, F: 20 GB): if
cleaning cannot make room, the job stops and goes into Needs you.

THE LIMITS live in production/retention.json, one row per kind of output with
the folders it governs, beside the places deletion may ever happen, the
protected paths, the model registry and the holds. Everything the Dropbox
backup covers is protected as well (tools/backup-to-dropbox.py's own list). A
link or junction is removed as a link, never entered (tools/cleanup.py's
remove_tree). The nightly task runs outside the Claude app, so it sees the
real AppData; from inside Claude a session sees its private copy on top.
"""
import datetime as dt
import fnmatch
import glob
import json
import os
import shutil
import stat
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
POLICY = os.environ.get("LEDGER_RETENTION_POLICY", os.path.join(REPO, "production", "retention.json"))
STATE = os.environ.get("LEDGER_RETENTION_STATE", r"F:\LedgerTools\retention")
HOME = os.path.expanduser("~")
LOCAL = os.path.join(HOME, "AppData", "Local")
CLAUDE_COPY = os.path.join(LOCAL, "Packages", "Claude_pzs8sxrjxfjjc", "LocalCache", "Local")
MODEL_FLOOR = 50e6          # models under 50 MB are settings files, never worth a rule
HOLD_MAX_DAYS = 14


def policy():
    return json.load(open(POLICY, encoding="utf-8"))


def norm(p):
    return os.path.normcase(os.path.abspath(p.replace("/", os.sep)))


def inside(path, root):
    try:
        return os.path.commonpath([norm(path), norm(root)]) == norm(root)
    except ValueError:
        return False


def is_link(path):
    """A symbolic link or a junction: measured as nothing, never walked through."""
    try:
        st = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


# ---- WHAT MAY EVER BE DELETED ----------------------------------------------

def backup_paths():
    """Everything the Dropbox backup copies: never deleted here."""
    try:
        spec = json.load(open(os.path.join(REPO, "production", "specs", "in-game.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for e in spec.get("placed", []):
        for b in e.get("backup", []):
            p = b.get("path", "")
            out.append(p if os.path.isabs(p) else os.path.join(REPO, p))
    for b in spec.get("backupAlso", []):
        p = b.get("path", "") if isinstance(b, dict) else str(b)
        out.append(p if os.path.isabs(p) else os.path.join(REPO, p))
    return [p for p in out if p]


def held(pol, path, today=None):
    today = today or dt.date.today()
    for h in pol.get("holds", []):
        try:
            until = dt.date.fromisoformat(h["until"])
        except (KeyError, ValueError):
            continue
        if until < today or (until - today).days > HOLD_MAX_DAYS:
            continue          # a lapsed hold, or one longer than the rule allows, holds nothing
        if inside(path, h["path"]) or inside(h["path"], path):
            return h
    return None


def may_delete(pol, path, protected_extra=()):
    """(ok, why) for one path."""
    if not any(inside(path, p) for p in pol["places"]):
        return False, "outside the project's places"
    for p in list(pol["protected"]) + list(protected_extra):
        if inside(path, p):
            return False, "protected: " + p
        if inside(p, path):
            return False, "holds a protected path: " + p
    if tracked(path):
        return False, "tracked by git (the project's own files)"
    h = held(pol, path)
    if h:
        return False, "held until %s: %s" % (h["until"], h.get("why", ""))
    return True, "ok"


def _remove(path, done):
    """On Windows, tools/cleanup.py's remove_tree (long paths, junctions removed as links).
    Elsewhere (the Core checks run on Linux) the same rule by hand: a link is unlinked, never entered."""
    if os.name == "nt":
        import cleanup
        cleanup.remove_tree(path, done)
        return
    if os.path.islink(path) or not os.path.isdir(path):
        st = os.lstat(path)
        os.unlink(path)
        done["links" if stat.S_ISLNK(st.st_mode) else "files"] += 1
        done["bytes"] += 0 if stat.S_ISLNK(st.st_mode) else st.st_size
        return
    for e in list(os.scandir(path)):
        _remove(e.path, done)
    os.rmdir(path)


def log(entry):
    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, "deleted.log"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def size_of(path):
    if is_link(path):
        return 0
    if os.path.isfile(path):
        try:
            return os.path.getsize(path)
        except OSError:
            return 0
    total = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not is_link(os.path.join(root, d))]
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def delete(pol, path, rule, why, dry=False, protected_extra=()):
    ok, reason = may_delete(pol, path, protected_extra)
    entry = {"at": dt.datetime.now().isoformat(timespec="seconds"), "path": path, "rule": rule, "why": why}
    if not os.path.exists(path) and not is_link(path):
        # NOT FOUND IS NOT DELETED (2 October: a list read with Windows line endings
        # gave every path a hidden carriage return, and each was logged as gone).
        entry["refused"] = "not found"
        return entry
    if not ok:
        entry["refused"] = reason
        return entry
    entry["bytes"] = size_of(path)
    if dry:
        entry["dry"] = True
        return entry
    done = {"files": 0, "links": 0, "bytes": 0, "failed": []}
    try:
        _remove(path, done)
    except OSError as e:
        done["failed"].append("%s (%s)" % (path, e.strerror))
    entry.update({"files": done["files"], "links": done["links"], "failed": done["failed"][:3],
                  "gone": not os.path.exists(path)})
    log(entry)
    return entry


# ---- THE LIMITS -------------------------------------------------------------

def expand(pattern):
    pattern = pattern.replace("/", os.sep)
    return sorted(glob.glob(pattern)) if any(c in pattern for c in "*?[") else ([pattern] if os.path.exists(pattern) else [])


def newest_mtime(path):
    """The newest file written anywhere under path (links not entered). A
    folder's own date moves whenever something inside it is added or removed,
    deletions included, so it counts only for a folder with no files at all."""
    try:
        own = os.lstat(path).st_mtime
    except OSError:
        return 0.0
    if not os.path.isdir(path) or is_link(path):
        return own
    best = None
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not is_link(os.path.join(root, d))]
        for n in files:
            try:
                t = os.lstat(os.path.join(root, n)).st_mtime
            except OSError:
                continue
            best = t if best is None else max(best, t)
    return own if best is None else best


def prune_old(top, now, limit):
    """What under `top` is older than `limit`: a folder whose newest file is
    older goes whole (one entry); otherwise it is entered and its old files and
    folders go one by one, so a session's folder with today's work in it still
    loses last week's."""
    out = []
    try:
        entries = list(os.scandir(top))
    except OSError:
        return out
    for e in entries:
        try:
            if e.is_symlink() or is_link(e.path):
                if now - os.lstat(e.path).st_mtime > limit:
                    out.append(e.path)
                continue
            if e.is_dir(follow_symlinks=False):
                if now - newest_mtime(e.path) > limit:
                    out.append(e.path)
                else:
                    out += prune_old(e.path, now, limit)
            elif now - e.stat(follow_symlinks=False).st_mtime > limit:
                out.append(e.path)
        except OSError:
            continue
    return out


def tracked(path):
    """True when git tracks the path or anything under it, in any of the project's checkouts."""
    for repo in (REPO, os.path.join(HOME, "ledger-town"), os.path.join(HOME, "ledger-clothes"),
                 r"C:\actions-runner-ledger\_work\ledger\ledger"):
        if inside(path, repo) and not inside(path, os.path.join(repo, ".git")):
            try:
                r = subprocess.run(["git", "-C", repo, "ls-files", "--", os.path.relpath(path, repo)],
                                   capture_output=True, text=True, timeout=60)
            except (OSError, subprocess.SubprocessError):
                return True        # unsure: keep
            return r.returncode != 0 or bool(r.stdout.strip())
    return False


def busy():
    """What is running that a deletion must not pull files from under."""
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=60).stdout.lower()
    except (OSError, subprocess.SubprocessError):
        return {"unknown"}
    names = {"runner.worker.exe": "runner", "unrealeditor.exe": "unreal", "unrealbuildtool.exe": "unreal",
             "zenserver.exe": "zen", "ledgerprobe.exe": "game", "marvelousdesigner": "marvelous"}
    return {v for k, v in names.items() if k in out}


def runner_path(p):
    return inside(p, r"C:\actions-runner-ledger")


def unreal_path(p):
    return any(s in norm(p) for s in (os.sep + "ue-probe" + os.sep, os.sep + "unrealengine" + os.sep))


def candidates(pol, now=None, running=None):
    """[(path, rule, why)] the limits would delete now."""
    now = now or time.time()
    running = busy() if running is None else running
    out = []

    def skip(p):
        return (runner_path(p) and "runner" in running) or (unreal_path(p) and ("unreal" in running or "zen" in running))

    for lim in pol["limits"]:
        rule = lim["rule"]
        if rule == "age":
            limit = lim["days"] * 86400
            for pat in lim["folders"]:
                for top in expand(pat):
                    if skip(top) or not os.path.isdir(top) or is_link(top):
                        continue
                    if os.path.basename(top) in ("StagedBuilds",):
                        if now - newest_mtime(top) > limit:
                            out.append((top, lim["kind"], "untouched for over %d day(s)" % lim["days"]))
                        continue
                    out += [(p, lim["kind"], "untouched for over %d day(s)" % lim["days"]) for p in prune_old(top, now, limit)]
        elif rule == "builds":
            builds = []
            for pat in lim["folders"]:
                for p in expand(pat):
                    if os.path.isdir(p) and not is_link(p):
                        builds.append((newest_mtime(p), p))
            builds.sort(reverse=True)
            mine = [b for b in builds if not inside(b[1], r"F:\LedgerTools\played-game")]
            keep = 1 if len(mine) < len(builds) else 2        # his played copy is always one of the two
            for _, p in mine[keep:]:
                if not skip(p):
                    out.append((p, lim["kind"], "older than the latest two builds"))
        elif rule == "gitleftovers":
            limit = lim["hours"] * 3600
            for pat in lim["folders"]:
                for d in expand(pat):
                    if skip(d):
                        continue
                    for f in glob.glob(os.path.join(d, "tmp_*")):
                        try:
                            if now - os.path.getmtime(f) > limit:
                                out.append((f, lim["kind"], "an interrupted download's leftover"))
                        except OSError:
                            pass
        elif rule == "models":
            registered = {norm(m["path"]): m for m in pol.get("models", [])}
            for pat in lim["folders"]:
                for p in expand(pat):
                    m = registered.get(norm(p))
                    if m:
                        if not any(os.path.exists(os.path.join(REPO, u)) for u in m.get("usedBy", [])):
                            out.append((p, lim["kind"], "registered, but nothing that used it is left"))
                        continue
                    if size_of(p) >= MODEL_FLOOR and now - newest_mtime(p) > lim["days"] * 86400:
                        out.append((p, lim["kind"], "no tool registered as using it, untouched for %d days" % lim["days"]))
        elif rule == "caches":
            for c in pol.get("caches", []):
                for p in c.get("mustStayEmpty", []):
                    if os.path.isdir(p) and size_of(p) > 100e6 and not skip(p):
                        out.append((p, "tool caches", "%s writes to %s; this copy on C: is a stray" % (c["name"], c["writes"])))
    seen, uniq = set(), []
    for p, r, w in out:
        if norm(p) not in seen:
            seen.add(norm(p))
            uniq.append((p, r, w))
    return uniq


def enforce(pol, dry=False):
    protected_extra = backup_paths()
    results = []
    for p, rule, why in candidates(pol):
        results.append(delete(pol, p, rule, why, dry=dry, protected_extra=protected_extra))
    return results


def cache_report(pol):
    rows = []
    for c in pol.get("caches", []):
        gb = size_of(c["writes"]) / 1e9 if os.path.exists(c["writes"]) else 0.0
        stray = [p for p in c.get("mustStayEmpty", []) if os.path.isdir(p) and size_of(p) > 100e6]
        rows.append({"name": c["name"], "writes": c["writes"], "gb": round(gb, 2), "capGb": c["capGb"],
                     "over": gb > c["capGb"], "stray": stray})
    return rows


# ---- MEASURING -------------------------------------------------------------

def walk_sizes(root, since_ts, depth=2):
    """{relative folder (up to `depth` levels): [bytes, bytes written since]} for one root.

    Files directly in a folder count toward it; links are counted as nothing
    and never entered, so a folder linked from C: to F: is measured once, where
    it lives."""
    out = {}
    if not os.path.exists(root):
        return out
    if os.path.isfile(root):
        try:
            st = os.stat(root)
        except OSError:
            return out
        out[""] = [st.st_size, st.st_size if st.st_mtime >= since_ts else 0]
        return out
    stack = [(root, "")]
    while stack:
        path, rel = stack.pop()
        try:
            it = os.scandir(path)
        except OSError:
            continue
        with it:
            for e in it:
                try:
                    if e.is_symlink() or (hasattr(e, "is_junction") and e.is_junction()):
                        continue
                    if e.is_dir(follow_symlinks=False):
                        stack.append((e.path, (rel + "\\" + e.name) if rel else e.name))
                        continue
                    st = e.stat(follow_symlinks=False)
                except OSError:
                    continue
                parts = rel.split("\\") if rel else []
                for k in range(0, min(depth, len(parts)) + 1):
                    row = out.setdefault("\\".join(parts[:k]), [0, 0])
                    row[0] += st.st_size
                    if st.st_mtime >= since_ts:
                        row[1] += st.st_size
    return out


def census_roots():
    """Every place the project and its tools write, on C: and F:, by name."""
    roots = [
        ("ledger-local (the builder)", os.path.join(HOME, "ledger-local")),
        ("ledger-town (the town)", os.path.join(HOME, "ledger-town")),
        ("ledger-clothes (clothing)", os.path.join(HOME, "ledger-clothes")),
        ("build machine", r"C:\actions-runner-ledger"),
        ("C:\\LedgerTools", r"C:\LedgerTools"),
        ("Unreal's cache and settings (AppData)", os.path.join(LOCAL, "UnrealEngine")),
        ("the packaged game's saves and logs (AppData)", os.path.join(LOCAL, "LedgerProbe")),
        ("the Claude app's private AppData copy", CLAUDE_COPY),
        ("Claude Code's scratch", os.path.join(LOCAL, "Temp", "claude")),
        ("Windows' temporary files (other)", os.path.join(LOCAL, "Temp")),
        ("crash dumps (AppData)", os.path.join(LOCAL, "CrashDumps")),
        ("Windows error reports", r"C:\ProgramData\Microsoft\Windows\WER"),
        ("model caches (.cache)", os.path.join(HOME, ".cache")),
        ("NuGet packages (.NET)", os.path.join(HOME, ".nuget")),
        ("Marvelous Designer (AppData)", os.path.join(LOCAL, "CLO Virtual Fashion")),
        ("Marvelous Designer (Documents)", os.path.join(HOME, "Documents", "CLO Virtual Fashion")),
        ("older project folders", None),
        ("F:\\LedgerTools", r"F:\LedgerTools"),
        ("F: outside LedgerTools", "F:\\"),
    ]
    out = []
    for name, path in roots:
        if path is None:
            for d in sorted(os.listdir(HOME)):
                full = os.path.join(HOME, d)
                if d.startswith("ledger-") and d not in ("ledger-local", "ledger-town", "ledger-clothes") and os.path.isdir(full):
                    out.append(("older project folder " + d, full))
            continue
        out.append((name, path))
    return out


def census(since, depth=2):
    since_ts = since.timestamp()
    rows = []
    claude_tmp = os.path.join(LOCAL, "Temp", "claude")
    for name, root in census_roots():
        if root == "F:\\":
            sizes = {}
            try:
                tops = [e for e in os.scandir("F:\\") if e.name != "LedgerTools"]
            except OSError:
                tops = []
            for e in tops:
                try:
                    if e.is_symlink():
                        continue
                    part = walk_sizes(e.path, since_ts, depth=1) if e.is_dir() else {"": [e.stat().st_size, 0]}
                except OSError:
                    continue
                for k, v in part.items():
                    sizes[e.name + ("\\" + k if k else "")] = v
                    if not k:
                        top = sizes.setdefault("", [0, 0]); top[0] += v[0]; top[1] += v[1]
        else:
            sizes = walk_sizes(root, since_ts, depth=depth)
            if norm(root) == norm(os.path.join(LOCAL, "Temp")) and "claude" in sizes:
                c = sizes["claude"]            # counted on its own row above
                sizes[""] = [sizes[""][0] - c[0], sizes[""][1] - c[1]]
                sizes = {k: v for k, v in sizes.items() if not (k == "claude" or k.startswith("claude\\"))}
        for rel, (b, r) in sizes.items():
            rows.append({"place": name, "path": os.path.join(root, rel) if rel else root,
                         "level": 0 if not rel else rel.count("\\") + 1, "gb": round(b / 1e9, 3),
                         "grewGb": round(r / 1e9, 3)})
    return rows


def free_gb():
    out = {}
    for d in ("C:\\", "F:\\"):
        try:
            out[d[0]] = round(shutil.disk_usage(d).free / 1e9, 1)
        except OSError:
            out[d[0]] = None
    return out


def snapshot(since=None):
    since = since or dt.datetime.now() - dt.timedelta(days=1)
    return {"at": dt.datetime.now().isoformat(timespec="seconds"), "since": since.isoformat(timespec="minutes"),
            "free": free_gb(), "rows": census(since)}


def save_snapshot(snap):
    os.makedirs(STATE, exist_ok=True)
    path = os.path.join(STATE, "census-%s.json" % snap["at"][:16].replace(":", ""))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=0)
    return path


def morning_line(snaps=None):
    """Free space on both drives and the three folders that grew most since the census a day before."""
    if snaps is None:
        files = sorted(glob.glob(os.path.join(STATE, "census-*.json")))
        snaps = [json.load(open(f, encoding="utf-8")) for f in files[-12:]]
    if not snaps:
        return "Disk: no census yet."
    last = snaps[-1]
    t_last = dt.datetime.fromisoformat(last["at"])
    prev = None
    for s in reversed(snaps[:-1]):
        if t_last - dt.datetime.fromisoformat(s["at"]) >= dt.timedelta(hours=20):
            prev = s
            break
    level = lambda s: {r["path"]: r["gb"] for r in s["rows"] if r["level"] in (1, 2)}
    if prev:
        a, b = level(prev), level(last)
        growth = {p: b[p] - a.get(p, 0.0) for p in b}
        rows = {r["path"]: r["level"] for r in last["rows"] if r["level"] in (1, 2)}
        items = []
        for p, lv in rows.items():
            if lv != 1:
                continue
            g = growth.get(p, 0.0)
            kids = sorted(((growth[k], k) for k, kl in rows.items() if kl == 2 and os.path.dirname(k) == p), reverse=True)
            # name the folder that grew, not its parent, when one child holds most of the growth
            items.append(kids[0] if kids and kids[0][0] >= 0.6 * g and kids[0][0] > 0 else (g, p))
        picked = [(g, p) for g, p in sorted(items, reverse=True) if g >= 0.05][:3]
        tops = ", ".join("%s +%.1f GB" % (p, g) for g, p in picked) or "nothing over 0.05 GB"
        since = "since %s" % prev["at"][5:16].replace("T", " ")
    else:
        rows = sorted((r for r in last["rows"] if r["level"] == 1), key=lambda r: -r["grewGb"])[:3]
        tops = ", ".join("%s +%.1f GB written" % (r["path"], r["grewGb"]) for r in rows)
        since = "files written in the day before"
    return "Disk (%s): C: %s GB free, F: %s GB free; grew most %s: %s." % (
        last["at"][5:16].replace("T", " "), last["free"]["C"], last["free"]["F"], since, tops)


# ---- THE FREE-SPACE CHECK BEFORE A JOB ---------------------------------------

def space(job, need_c, need_f, drives="CF"):
    """GO or STOP for a job, on the drives it writes to (an Unreal build writes to
    both: its cache is on F:; a .NET test run with its temporary files on C: only C:)."""
    pol = policy()
    free = free_gb()
    need_c = need_c if "C" in drives.upper() else 0
    need_f = need_f if "F" in drives.upper() else 0
    short = lambda f: (f["C"] is not None and f["C"] < need_c) or (f["F"] is not None and f["F"] < need_f)
    out = {"job": job, "drives": drives.upper(), "before": free}
    if short(free):
        out["cleaned"] = [r for r in enforce(pol) if "refused" not in r]
        free = free_gb()
        out["after"] = free
    if short(free):
        out["verdict"] = "STOP"
        out["needsYou"] = ("%s stopped: C: has %s GB free (needs %s), F: %s GB (needs %s) after the nightly limits ran. "
                           "Put this in Needs you and do not retry until there is room." % (job, free["C"], need_c, free["F"], need_f))
    else:
        out["verdict"] = "GO"
    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, "space-checks.log"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(dict(out, at=dt.datetime.now().isoformat(timespec="seconds"), cleaned=len(out.get("cleaned", [])))) + "\n")
    return out


# ---- THE SELF-TEST -----------------------------------------------------------

def selftest():
    import tempfile
    failures = []

    def check(cond, what):
        if not cond:
            failures.append(what)

    base = tempfile.mkdtemp(prefix="retention-selftest-", dir=os.environ.get("LEDGER_SELFTEST_DIR"))
    try:
        j = lambda *a: os.path.join(base, *a)
        old = time.time() - 10 * 86400
        recent = time.time() - 3600

        def make(path, when, size=10):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(b"x" * size)
            os.utime(path, (when, when))

        make(j("tmp", "old-job", "a.wav"), old)
        make(j("tmp", "new-job", "a.wav"), recent)
        make(j("tmp", "mixed", "old.wav"), old)
        make(j("tmp", "mixed", "new.wav"), recent)
        make(j("tmp", "held-job", "a.wav"), old)
        make(j("renders", "four-days", "f.png"), time.time() - 4 * 86400)
        make(j("renders", "two-days", "f.png"), time.time() - 2 * 86400)
        make(j("protected", "keep.bin"), old)
        make(j("tmp", "protected-inside", "keep.bin"), old)
        make(j("outside", "x.bin"), old)
        make(j("builds", "b1", "g.exe"), time.time() - 3 * 86400)
        make(j("builds", "b2", "g.exe"), time.time() - 2 * 86400)
        make(j("builds", "b3", "g.exe"), time.time() - 1 * 86400)
        make(j("git", "tmp_pack_abc"), time.time() - 86400)
        make(j("git", "tmp_pack_now"), time.time() - 60)
        make(j("git", "pack-1.pack"), old)
        make(j("hf", "models--unused--big"), old, size=60_000_000)
        make(j("hf", "models--registered--big"), old, size=60_000_000)
        make(j("hf", "models--orphan--big"), old, size=60_000_000)
        make(j("hf", "models--small--cfg"), old, size=1000)
        # a junction out of the scratch into something protected: removed as a link, its target untouched
        link_made = False
        if os.name == "nt":
            r = subprocess.run(["cmd", "/c", "mklink", "/J", j("tmp", "old-job", "link"), j("protected")], capture_output=True)
            link_made = r.returncode == 0
            if link_made:
                os.utime(j("tmp", "old-job"), (old, old))
        pol = {"places": [j("tmp"), j("renders"), j("builds"), j("git"), j("hf")],
               "protected": [j("protected"), j("tmp", "protected-inside")],
               "holds": [{"path": j("tmp", "held-job"), "why": "test", "until": (dt.date.today() + dt.timedelta(days=3)).isoformat()},
                         {"path": j("tmp", "old-job"), "why": "too long a hold", "until": (dt.date.today() + dt.timedelta(days=30)).isoformat()}],
               "models": [{"path": j("hf", "models--registered--big"), "usedBy": ["tools/retention.py"]},
                          {"path": j("hf", "models--orphan--big"), "usedBy": ["tools/no-such-tool.py"]}],
               "caches": [],
               "limits": [{"kind": "scratch", "rule": "age", "days": 7, "folders": [j("tmp")]},
                          {"kind": "renders", "rule": "age", "days": 3, "folders": [j("renders")]},
                          {"kind": "builds", "rule": "builds", "folders": [j("builds", "*")]},
                          {"kind": "git", "rule": "gitleftovers", "hours": 12, "folders": [j("git")]},
                          {"kind": "models", "rule": "models", "days": 7, "folders": [j("hf", "models--*")]}]}
        global STATE
        saved_state, STATE = STATE, j("state")
        try:
            got = {os.path.relpath(p, base) for p, _, _ in candidates(pol, running=set())}
            want = {os.path.join("tmp", "old-job"), os.path.join("tmp", "protected-inside"), os.path.join("tmp", "held-job"),
                    os.path.join("tmp", "mixed", "old.wav"), os.path.join("renders", "four-days"),
                    os.path.join("builds", "b1"), os.path.join("git", "tmp_pack_abc"), os.path.join("hf", "models--unused--big"),
                    os.path.join("hf", "models--orphan--big")}
            check(got == want, "candidates %s, wanted %s" % (sorted(got), sorted(want)))
            res = {os.path.relpath(r["path"], base): r for r in enforce_with(pol)}
            check("refused" in res.get(os.path.join("tmp", "protected-inside"), {}), "a protected folder inside the scratch was refused")
            check(not os.path.exists(j("tmp", "old-job")), "the old job is gone")
            check(os.path.exists(j("protected", "keep.bin")), "the junction's target survived")
            check(os.path.exists(j("tmp", "mixed", "new.wav")) and not os.path.exists(j("tmp", "mixed", "old.wav")),
                  "a folder with a recent file keeps it and loses its old one")
            check(os.path.exists(j("tmp", "held-job")), "a held folder stays")
            check(os.path.exists(j("builds", "b2")) and os.path.exists(j("builds", "b3")), "the latest two builds stay")
            check(os.path.exists(j("git", "tmp_pack_now")) and os.path.exists(j("git", "pack-1.pack")), "a live download and the real pack stay")
            check(os.path.exists(j("hf", "models--registered--big")) and os.path.exists(j("hf", "models--small--cfg")), "used and tiny models stay")
            ok, why = may_delete(pol, j("outside", "x.bin"))
            check(not ok and "outside" in why, "a path outside the places is refused")
            lines = open(j("state", "deleted.log"), encoding="utf-8").read().splitlines()
            check(len(lines) == 7, "seven deletions logged, got %d" % len(lines))
            check(link_made or os.name != "nt", "the junction test ran")
            snaps = [{"at": "2026-10-01T04:30:00", "free": {"C": 30, "F": 3}, "rows": [{"path": "A", "level": 1, "gb": 1.0}, {"path": "A\\x", "level": 2, "gb": 0.5}, {"path": "B", "level": 1, "gb": 2.0}]},
                     {"at": "2026-10-02T04:30:00", "free": {"C": 70, "F": 25}, "rows": [{"path": "A", "level": 1, "gb": 3.0}, {"path": "A\\x", "level": 2, "gb": 2.4}, {"path": "B", "level": 1, "gb": 2.5}]}]
            line = morning_line(snaps)
            check("C: 70 GB free, F: 25 GB free" in line and "A\\x +1.9 GB" in line and "B +0.5 GB" in line and "A +2.0" not in line,
                  "the morning line: " + line)
        finally:
            STATE = saved_state
    finally:
        import cleanup
        done = {"files": 0, "links": 0, "bytes": 0, "failed": []}
        try:
            cleanup.remove_tree(base, done)
        except OSError:
            pass
    print("retention selftest: %s" % ("passed" if not failures else "FAILED: " + "; ".join(failures)))
    return 0 if not failures else 1


def enforce_with(pol):
    return [delete(pol, p, r, w) for p, r, w in candidates(pol, running=set())]


# ---- COMMANDS -------------------------------------------------------------------

def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]

    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default

    if cmd == "--selftest":
        return selftest()
    if cmd == "census":
        since = dt.datetime.fromisoformat(opt("--since")) if opt("--since") else None
        snap = snapshot(since)
        if opt("--out"):
            with open(opt("--out"), "w", encoding="utf-8") as fh:
                json.dump(snap, fh, indent=0)
        for r in sorted((r for r in snap["rows"] if r["level"] == 0), key=lambda r: -r["gb"]):
            print("%8.2f GB  grew %7.2f  %s  (%s)" % (r["gb"], r["grewGb"], r["place"], r["path"]))
        print("free: C: %s GB, F: %s GB" % (snap["free"]["C"], snap["free"]["F"]))
        return 0
    if cmd in ("plan", "run"):
        res = enforce(policy(), dry=(cmd == "plan"))
        for r in res:
            print("%s %7.2f GB  %-26s %s%s" % ("REFUSED" if "refused" in r else ("would" if cmd == "plan" else "deleted"),
                                              r.get("bytes", 0) / 1e9, r["rule"], r["path"],
                                              ("  (" + r["refused"] + ")") if "refused" in r else ""))
        print("%s: %.2f GB in %d place(s)" % (cmd, sum(r.get("bytes", 0) for r in res if "refused" not in r) / 1e9,
                                             sum(1 for r in res if "refused" not in r)))
        return 0
    if cmd == "delete":
        if not args or not opt("--why"):
            print("usage: delete PATH --why TEXT")
            return 2
        r = delete(policy(), args[0], "by hand", opt("--why"), protected_extra=backup_paths())
        print(json.dumps(r))
        return 1 if "refused" in r or r.get("failed") else 0
    if cmd == "nightly":
        before = snapshot()
        save_snapshot(before)
        res = enforce(policy())
        after = snapshot()
        save_snapshot(after)
        line = morning_line()
        summary = {"at": after["at"], "freeBefore": before["free"], "freeAfter": after["free"],
                   "deletedGb": round(sum(r.get("bytes", 0) for r in res if "refused" not in r) / 1e9, 2),
                   "deleted": len([r for r in res if "refused" not in r]), "refused": [r for r in res if "refused" in r][:20],
                   "caches": cache_report(policy()), "line": line}
        with open(os.path.join(STATE, "nightly-%s.json" % after["at"][:10]), "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1)
        with open(os.path.join(STATE, "line.txt"), "w", encoding="utf-8") as fh:
            fh.write(line + "\n")
        # thirty days of censuses are enough to see a trend
        for f in sorted(glob.glob(os.path.join(STATE, "census-*.json")))[:-60]:
            os.remove(f)
        print(line)
        return 0
    if cmd == "line":
        print(morning_line())
        return 0
    if cmd == "caches":
        for c in cache_report(policy()):
            print("%-40s %6.2f GB of %4.1f  %s%s" % (c["name"], c["gb"], c["capGb"], c["writes"], "  OVER" if c["over"] else ""))
        return 0
    if cmd == "space":
        r = space(opt("--job", "a job"), float(opt("--need-c", 40)), float(opt("--need-f", 20)), opt("--drives", "CF"))
        print(json.dumps({k: v for k, v in r.items() if k != "cleaned"}))
        return 0 if r["verdict"] == "GO" else 3
    print("unknown command " + cmd)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception:
        # The nightly task runs without a window (pythonw): a failure must leave a trace the morning check reads.
        import traceback
        os.makedirs(STATE, exist_ok=True)
        with open(os.path.join(STATE, "errors.log"), "a", encoding="utf-8") as fh:
            fh.write("%s %s\n%s\n" % (dt.datetime.now().isoformat(timespec="seconds"), sys.argv[1:], traceback.format_exc()))
        raise
