#!/usr/bin/env python3
"""Retention for drives C: and F:: what this project keeps, measured and enforced every night.

    python tools/retention.py census [--since ISO] [--out FILE]   # every place of the project's, folder by folder, largest first
    python tools/retention.py plan                                 # what the limits and the storage map's rules would delete now (nothing is deleted)
    python tools/retention.py run                                  # deletes what the limits say (and the map's rules once live), logs each deletion
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

THE STORAGE MAP (production/storage-map.json, RULINGS 17 Nov) gives every
folder a shelf and an expiry. Its rules (map_plan: working 3 days, tools 14
days unused and refetchable, else his page; lasting and side sessions never)
are listed by `plan` beside the limits, with the "his page" candidates and the
floors (the map's: F: 20, C: 40). `run`, `nightly` and `space` remove the
map's rows only once production/retention.json sets "mapRulesLive": true, and
only what `plan` lists, through the same delete() and its log.
"""
import datetime as dt
import fnmatch
import glob
import json
import ntpath
import os
import re
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


def _named(text, key):
    """key ('runs/fixer-r7') appears in text as a whole name: no name character after it, and a full stop
    counts as an end only when no name character follows it."""
    i = text.find(key)
    while i >= 0:
        nxt, after = text[i + len(key):i + len(key) + 1], text[i + len(key) + 1:i + len(key) + 2]
        if not (nxt.isalnum() or nxt in "_-") and not (nxt == "." and (after.isalnum() or after in "_-")):
            return True
        i = text.find(key, i + 1)
    return False


def named_keep(pol):
    """Entries directly under a `namedKeep` folder that one of its `namedIn` files names, as '<folder>/<entry>'
    (17 Nov, KILN-DISK: run outputs expire, but never a run the regression jobs, the judge's HASHES.txt, a report
    or an approval names). Never opens the judge's held-back jobs."""
    out = []
    for nk in pol.get("namedKeep", []):
        texts = []
        for pat in nk.get("namedIn", []):
            for f in glob.glob(pat.replace("/", os.sep), recursive=True):
                if "heldback" in norm(f) or not os.path.isfile(f):
                    continue
                try:
                    with open(f, encoding="utf-8", errors="replace") as fh:
                        texts.append(fh.read())
                except OSError:
                    pass
        text = "\n".join(texts).replace("\\\\", "/").replace("\\", "/").lower()
        for pat in nk.get("under", []):
            for top in expand(pat):
                if not os.path.isdir(top) or is_link(top):
                    continue
                for e in os.scandir(top):
                    if _named(text, (os.path.basename(top.rstrip("\\/")) + "/" + e.name).lower()):
                        out.append(e.path)
    return out


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


def newest_any(path):
    """The newest modification or creation time of path and anything under it (links not entered): the map's age
    (the step-2 review, 17 Nov, S2: a move or copy keeps files' modification times, so a set moved in today
    would read as weeks unwritten; on Windows st_ctime is the creation time, st_birthtime where Python has it)."""
    def t(st):
        born = getattr(st, "st_birthtime", st.st_ctime if os.name == "nt" else st.st_mtime)
        return max(st.st_mtime, born)
    try:
        best = t(os.lstat(path))
    except OSError:
        return 0.0
    if not os.path.isdir(path) or is_link(path):
        return best
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not is_link(os.path.join(root, d))]
        for n in files + dirs:
            try:
                best = max(best, t(os.lstat(os.path.join(root, n))))
            except OSError:
                continue
    return best


MAP_AGE = [newest_any]     # the self-test's fixtures can set only modification times, so they swap in newest_mtime


def real(p):
    return os.path.normcase(os.path.realpath(p))


def map_files_committed(repo=REPO):
    """True when production/storage-map.json and production/retention.json have no uncommitted change (S5): the
    night acts on map rows only from reviewed, committed files."""
    try:
        out = subprocess.run(["git", "-C", repo, "status", "--porcelain", "--", "production/storage-map.json",
                              "production/retention.json"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0 and not out.stdout.strip()


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


def enforce(pol, dry=False, mp=None, map_live=None, committed=None):
    """The limits' rows, then the storage map's (map_plan's 'remove' list only): listed when dry, removed only when
    the map's rules are live (retention.json "mapRulesLive": true). Each goes through delete() and its checks."""
    protected_extra = backup_paths() + named_keep(pol)
    results = []
    for p, rule, why in candidates(pol):
        results.append(delete(pol, p, rule, why, dry=dry, protected_extra=protected_extra))
    live = map_rules_live(pol) if map_live is None else map_live
    if dry or live:
        if mp is None:
            try:
                mp = map_plan(storage_map(), pol)
            except Exception as e:          # S4: a malformed map lists nothing; the limits' rows stand
                print("storage map unreadable (%s: %s): the map's rules list nothing" % (type(e).__name__, e))
                mp = {"remove": []}
        done = [r["path"] for r in results]
        committed = True if dry else (map_files_committed() if committed is None else committed)
        running = busy() if mp.get("remove") else set()
        for p, rule, why in mp.get("remove", []):
            if any(inside(p, d) for d in done):
                continue            # a limit's row already covers it
            if not committed:
                results.append({"path": p, "rule": rule, "bytes": 0, "map": True,
                                "refused": "storage-map.json or retention.json has uncommitted changes (S5)"})
                continue
            if (runner_path(p) and "runner" in running) or (unreal_path(p) and ("unreal" in running or "zen" in running)):
                results.append({"path": p, "rule": rule, "bytes": 0, "map": True,
                                "refused": "Unreal or the runner is running (M1)"})
                continue
            r = delete(pol, p, rule, why, dry=dry, protected_extra=protected_extra)
            r["map"] = True
            results.append(r)
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
        # TWELVE HOURS, NOT TWENTY (3 October): the census of 2 October ran at 09:42 and the
        # night's at 04:30, under twenty hours apart, so the line fell back to "files written",
        # and git touching two old packs it already had (18.9 and 12.2 GB) read as the history
        # growing 31.5 GB; their sizes say 0.23 GB.
        if t_last - dt.datetime.fromisoformat(s["at"]) >= dt.timedelta(hours=12):
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
            # ntpath, not os.path (5 October): the census is this PC's, its paths Windows ones, and on
            # GitHub's Linux machine os.path.dirname saw no parent in them and failed the selftest.
            kids = sorted(((growth[k], k) for k, kl in rows.items() if kl == 2 and ntpath.dirname(k) == p), reverse=True)
            # name the folder that grew, not its parent, when one child holds most of the growth
            items.append(kids[0] if kids and kids[0][0] >= 0.6 * g and kids[0][0] > 0 else (g, p))
        picked = [(g, p) for g, p in sorted(items, reverse=True) if g >= 0.05][:3]
        tops = ", ".join("%s +%.1f GB" % (p, g) for g, p in picked) or "nothing over 0.05 GB"
        since = "since %s" % prev["at"][5:16].replace("T", " ")
    else:
        # no census twelve hours old: say what was touched, never call it growth (a file git
        # only touches counts whole here)
        rows = sorted((r for r in last["rows"] if r["level"] == 1), key=lambda r: -r["grewGb"])[:3]
        tops = ", ".join("%s %.1f GB touched" % (r["path"], r["grewGb"]) for r in rows)
        since = "(no census a day old, so not growth) files touched in the day before"
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
            # namedKeep (17 Nov): a run a report names stays past its age limit; an unnamed one, and one whose
            # name only begins like a named one, go. A full stop after the name and backslashes still name it.
            make(j("runs", "named-run", "a.obj"), old)
            make(j("runs", "named-run-2", "a.obj"), old)
            make(j("runs", "other-run", "a.obj"), old)
            os.makedirs(j("reports"), exist_ok=True)
            with open(j("reports", "R.md"), "w", encoding="utf-8") as fh:
                fh.write("Evidence in F:\\\\x\\runs\\named-run. Done.\n")
            pol2 = {"places": [j("runs")], "protected": [], "holds": [], "caches": [],
                    "namedKeep": [{"under": [j("runs")], "namedIn": [j("reports", "*.md")]}],
                    "limits": [{"kind": "runs", "rule": "age", "days": 7, "folders": [j("runs")]}]}
            check([os.path.basename(p) for p in named_keep(pol2)] == ["named-run"], "namedKeep names only named-run")
            enforce(pol2)
            check(os.path.exists(j("runs", "named-run", "a.obj")), "a run a report names stays")
            check(not os.path.exists(j("runs", "named-run-2")) and not os.path.exists(j("runs", "other-run")),
                  "unnamed runs past their limit go")
            failures.extend(map_rule_cases(j, make, check_only=True))
        finally:
            STATE = saved_state
        # THE STORAGE MAP, read only (17 Nov): a folder inside a mapped one is covered, a new one is flagged
        os.makedirs(j("map", "kept", "inner"))
        os.makedirs(j("map", "new"))
        open(j("map", "kept", "inner", "a.bin"), "wb").write(b"0" * 1000)
        fake = {"folders": [{"path": j("map", "kept"), "shelf": "lasting"}],
                "shelves_gb": {"F": {"lasting": 10, "floor": 20}}}
        check(mapped(fake, j("map", "kept", "inner"))["path"] == j("map", "kept"), "a folder inside a mapped one is covered")
        check(unmapped(fake, roots=(j("map"),)) == [j("map", "new")], "an unmapped folder is flagged, a mapped one is not")
        real = storage_map()
        check(not any(e["path"].lower().rstrip("/").endswith(("vuze", "$recycle.bin")) for e in real["folders"]),
              "nothing of his is on the map")
        check(all(e.get("shelf") and e.get("expiry") for e in real["folders"]), "every mapped folder has a shelf and an expiry")
        check(sum(v for k, v in real["shelves_gb"]["F"].items()) <= 120.5, "F:'s shelves and floor fit the drive")
        check(floors(real) == {"C": 40.0, "F": 20.0}, "the real map's floors are C: 40, F: 20")
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


def map_rule_cases(j, make, check_only=True):
    """The storage map's expiry rules on temp folders and a fake map (step 2, 17 Nov). Returns the failures."""
    fails = []

    def check(cond, what):
        if not cond:
            fails.append("map rules: " + what)

    mp_ = lambda *a: j("mp", *a)
    now = time.time()
    d1, d5, d10, d20 = (now - n * 86400 for n in (1, 5, 10, 20))
    fx = [("work-old", "working", d10, {"proposal": "remove: test"}),
          ("work-new", "working", d1, {"proposal": "remove: test"}),
          ("work-keep", "working", d10, {"proposal": "keep, test"}),
          ("work-shrink", "working", d10, {"proposal": "remove/shrink candidate"}),
          ("work-read", "working", d10, {"proposal": "remove: test"}),
          ("work-side", "working", d10, {"proposal": "remove: test", "source": "made by the lab side session"}),
          ("work-protected", "working", d10, {"proposal": "remove: test"}),
          ("work-held", "working", d10, {"proposal": "remove: test"}),
          ("work-holds", "working", d10, {"proposal": "remove: test"}),
          ("work-backup", "working", d10, {"proposal": "remove: test", "backup": "yes (all of it)"}),
          ("work-his", "working", d10, {"proposal": "remove: test", "owner": "Jafar"}),
          ("work-linenamed", "working", d10, {"proposal": "remove candidate, no path reader (tools/cleanup.py imports it)"}),
          ("work-limitrow", "working", d10, {"proposal": "remove: empty", "serves": "production/retention.json (limit row)"}),
          ("tool-public", "tools", d20, {"proposal": "remove candidate", "source": "public PyPI"}),
          ("tool-unknown", "tools", d20, {"proposal": "remove candidate", "source": "unknown"}),
          ("tool-signin", "tools", d20, {"proposal": "", "source": "public, needs the owner's sign-in"}),
          ("tool-recent", "tools", d5, {"proposal": "remove candidate", "source": "public PyPI"}),
          ("tool-keep", "tools", d20, {"proposal": "keep", "source": "public PyPI"}),
          ("lasting-old", "lasting", d20, {"proposal": "remove"}),
          ("side-old", "side-session", d20, {"proposal": "remove"}),
          ("cache-old", "build-cache", d20, {"proposal": "remove"}),
          ("work-noowner", "working", d10, {"proposal": "remove: test", "owner": ""}),
          ("work-unknownsrc", "working", d10, {"proposal": "remove: test", "source": "source unknown"})]
    fake = {"shelves_gb": {"F": {"floor": 20}, "C": {"floor": 40}}, "folders": []}
    for name, shelf, when, extra in fx:
        make(mp_(name, "f.bin"), when, size=1000)
        fake["folders"].append(dict({"path": mp_(name), "shelf": shelf, "source": "made by LEDGER runs",
                                     "serves": "test", "proposal": "", "owner": "LEDGER"}, **extra))
    make(mp_("work-holds", "inner", "g.bin"), d10)
    fake["folders"].append({"path": mp_("work-holds", "inner"), "shelf": "lasting", "proposal": "keep"})
    make(mp_("unmapped-old", "f.bin"), d20)                       # in the places, old, not on the map
    make(j("mp-elsewhere", "stray", "f.bin"), d10)                # on the map, outside the places
    fake["folders"].append({"path": j("mp-elsewhere", "stray"), "shelf": "working", "proposal": "remove: stray", "owner": "LEDGER", "source": "made by LEDGER runs"})
    make(j("mp-target", "keep.bin"), d10)                         # a junction's target, outside the places
    link_made = False
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", mp_("work-old", "link"), j("mp-target")], capture_output=True)
        link_made = r.returncode == 0
    elif hasattr(os, "symlink"):
        try:
            os.symlink(j("mp-target"), mp_("work-old", "link"))
            link_made = True
        except OSError:
            pass
    pol = {"places": [j("mp")], "protected": [mp_("work-protected")], "caches": [], "limits": [],
           "holds": [{"path": mp_("work-held"), "why": "test", "until": (dt.date.today() + dt.timedelta(days=3)).isoformat()}],
           "floors": {"C": 30, "F": 20}}
    readers = "open(r'%s\\data.json')" % mp_("work-read")
    # S2: a file made today with a 30-day-old modification time reads as new to the map's age
    make(j("s2", "old.bin"), d20)
    check(now - newest_any(j("s2")) < 3600 and now - newest_mtime(j("s2")) > 86400 * 15,
          "a copied-in old file reads as new by its creation time (S2)")
    MAP_AGE[0] = newest_mtime
    plan = map_plan(fake, pol, readers=readers)
    rel = lambda rows: {os.path.relpath(r[0], j()) for r in rows}
    want_remove = {os.path.join("mp", "work-old"), os.path.join("mp", "tool-public"), os.path.join("mp", "work-limitrow")}
    want_page = {os.path.join("mp", "tool-unknown"), os.path.join("mp", "tool-signin")}
    want_refused = {os.path.join("mp", "work-protected"), os.path.join("mp", "work-held"),
                    os.path.join("mp-elsewhere", "stray")}
    check(rel(plan["remove"]) == want_remove, "remove %s, wanted %s" % (sorted(rel(plan["remove"])), sorted(want_remove)))
    check(rel(plan["hisPage"]) == want_page, "his page %s, wanted %s" % (sorted(rel(plan["hisPage"])), sorted(want_page)))
    check(rel(plan["refused"]) == want_refused, "refused %s, wanted %s" % (sorted(rel(plan["refused"])), sorted(want_refused)))
    listed = rel(plan["remove"]) | rel(plan["hisPage"]) | rel(plan["refused"]) | rel(plan["kept"])
    check(os.path.join("mp", "unmapped-old") not in listed, "an unmapped folder is on no list")
    why = {os.path.relpath(p, j()): w for p, w, _ in plan["kept"]}
    for name, frag in (("work-new", "inside its 3 days"), ("tool-recent", "inside its 14 days"),
                       ("work-keep", "keeps it"), ("work-shrink", "keeps it"), ("tool-keep", "keeps it"),
                       ("work-read", "names it"), ("work-side", "side session"), ("work-holds", "holds another"),
                       ("work-backup", "backed up"), ("work-his", "owner"), ("lasting-old", "never"),
                       ("work-linenamed", "names a reader (tools/cleanup.py)"),
                       ("side-old", "never"), ("cache-old", "never"),
                       ("work-noowner", "owner not written"), ("work-unknownsrc", "source unknown")):
        check(frag in why.get(os.path.join("mp", name), ""), "%s kept for '%s', got '%s'"
              % (name, frag, why.get(os.path.join("mp", name))))
    check(any("protected" in w for p, _, w in plan["refused"] if p.endswith("work-protected")), "protected is refused as protected")
    # S1: a twin line (lasting) of a working folder, and a '..' path, keep it; S3: "removed ... kept" is no order;
    # S4: a malformed map raises, which enforce and run turn into an empty list
    twin = {"folders": [dict(fake["folders"][0]), {"path": mp_("work-old") + os.sep, "shelf": "lasting", "owner": "LEDGER"}]}
    tp = map_plan(twin, pol, readers=readers)
    check(not tp["remove"] and any("another line" in w for _, w, _ in tp["kept"]), "a lasting twin keeps a working line (S1)")
    dots = {"folders": [dict(fake["folders"][0], path=os.path.join(j("mp"), "x", "..", "work-old"))]}
    check(not map_plan(dots, pol, readers=readers)["remove"], "a path with '..' is never removed (S1)")
    said = {"folders": [dict(fake["folders"][0], proposal="removed 17 Nov by his yes; designed voices kept")]}
    check(not map_plan(said, pol, readers=readers)["remove"], "'removed ... kept' is not a remove order (S3)")
    said2 = {"folders": [dict(fake["folders"][0], proposal="remove candidate: check with him before any delete")]}
    check(not map_plan(said2, pol, readers=readers)["remove"], "'check with him' is not a remove order (S3)")
    bad_map = False
    try:
        map_plan({"folders": "oops"}, pol, readers=readers)
    except ValueError:
        bad_map = True
    check(bad_map and map_plan({"folders": [None, {"path": 5}]}, pol, readers=readers)["remove"] == [],
          "a malformed map raises or lists nothing (S4)")
    # the step-2 review, B1: a script inside a lasting folder that names a removable one is a reader
    make(j("mp-final", "run_all.ps1"), d1, size=0)
    open(j("mp-final", "run_all.ps1"), "w").write("& python x.py --in '%s'" % mp_("work-old"))
    check(_named(reader_text(j(), extra_dirs=[j("mp-final")]), path_key(mp_("work-old"))),
          "a lasting folder's script naming a folder counts as its reader")
    nr = {"folders": [dict(fake["folders"][0]),
                      {"path": mp_("work-newer"), "shelf": "working", "owner": "LEDGER", "source": "made by LEDGER runs",
                       "proposal": "keep"}]}
    make(mp_("work-newer", "run_all.ps1"), d1, size=0)
    open(mp_("work-newer", "run_all.ps1"), "w").write("python x.py --in '%s'" % mp_("work-old"))
    np_ = map_plan(nr, pol)
    check(not np_["remove"] and any("files in" in w for q, w, _ in np_["kept"] if q.endswith("work-old")),
          "a newer working round's script keeps the old round it reads, through map_plan (N2)")
    open(mp_("work-old", "self.ps1"), "w").write("python x.py --out '%s'" % mp_("work-old"))
    os.remove(mp_("work-newer", "run_all.ps1"))
    check(not any("files in" in w for q, w, _ in map_plan(nr, pol)["kept"] if q.endswith("work-old")),
          "a folder's own script never counts as its own reader (N2)")
    os.remove(mp_("work-old", "self.ps1"))
    unk = {"folders": [dict(fake["folders"][0], source="unknown")]}
    check(not map_plan(unk, pol, readers=readers)["remove"], "a plain 'unknown' source keeps the row (N1)")
    check(any("held" in w for p, _, w in plan["refused"] if p.endswith("work-held")), "a held folder is refused as held")
    check(any("outside" in w for p, _, w in plan["refused"] if p.endswith("stray")), "outside the places is refused")
    # not live: run removes none of the map's rows
    res = enforce(pol, dry=False, mp=plan, map_live=False)
    check(not [r for r in res if r.get("map")] and os.path.exists(mp_("work-old", "f.bin")), "not live: nothing of the map's removed")
    # plan (dry) lists exactly the remove list
    res = enforce(pol, dry=True, mp=plan)
    check({os.path.relpath(r["path"], j()) for r in res if r.get("map") and r.get("dry")} == want_remove,
          "the dry plan lists the remove list")
    check(os.path.exists(mp_("work-old", "f.bin")), "the dry plan removed nothing")
    # live: removes only what the plan lists, through delete() and its log
    log_before = len(open(os.path.join(STATE, "deleted.log"), encoding="utf-8").read().splitlines()) \
        if os.path.exists(os.path.join(STATE, "deleted.log")) else 0
    unc = enforce(pol, dry=False, mp=plan, map_live=True, committed=False)
    check(not [r for r in unc if r.get("map") and "refused" not in r] and os.path.exists(mp_("work-old", "f.bin")),
          "live, but the map files uncommitted: nothing of the map's removed (S5)")
    res = enforce(pol, dry=False, mp=plan, map_live=True, committed=True)
    gone = {os.path.relpath(r["path"], j()) for r in res if r.get("map") and r.get("gone")}
    check(gone == want_remove, "live run removed %s, wanted %s" % (sorted(gone), sorted(want_remove)))
    check(not os.path.exists(mp_("work-old")) and not os.path.exists(mp_("tool-public"))
          and not os.path.exists(mp_("work-limitrow")), "the expired folders are gone")
    check(os.path.exists(j("mp-target", "keep.bin")), "the junction's target survived")
    check(link_made, "the junction test ran")
    if link_made:
        row = [r for r in res if r.get("map") and r["path"].endswith("work-old")]
        check(row and row[0].get("links") == 1, "the junction was removed as one link")
    for name in ("work-new", "work-keep", "work-shrink", "work-read", "work-side", "work-protected", "work-held",
                 "work-holds", "work-backup", "work-his", "work-linenamed", "tool-unknown", "tool-signin", "tool-recent", "tool-keep",
                 "lasting-old", "side-old", "cache-old", "unmapped-old"):
        check(os.path.exists(mp_(name, "f.bin")), "%s stays" % name)
    check(os.path.exists(j("mp-elsewhere", "stray", "f.bin")), "the stray outside the places stays")
    log_path = os.path.join(STATE, "deleted.log")
    lines = open(log_path, encoding="utf-8").read().splitlines()[log_before:] if os.path.exists(log_path) else []
    check(len(lines) == 3 and all(json.loads(x)["rule"].startswith("map ") for x in lines), "three map deletions logged")
    # floors: the map's win over retention.json's; a drive below its floor is flagged before and after
    fl = floors(fake, pol)
    check(fl == {"C": 40.0, "F": 20.0}, "the map's floors: %s" % fl)
    check(floors({}, pol) == {"C": 30.0, "F": 20.0} and floors({}, {}) == {"C": 40.0, "F": 20.0}, "floor fallbacks")
    rows = {r["drive"]: r for r in floor_rows(fl, {"C": 35.0, "F": 25.0}, {"C": 3e9})}
    check(rows["C"]["below"] and rows["C"]["after"] == 38.0 and rows["C"]["belowAfter"] and not rows["F"]["below"],
          "floor rows: %s" % rows)
    rows = {r["drive"]: r for r in floor_rows(fl, {"C": 38.0, "F": None}, {"C": 3e9})}
    check(rows["C"]["below"] and not rows["C"]["belowAfter"] and not rows["F"]["below"], "freeing lifts a drive over its floor")
    return fails


# ---- THE STORAGE MAP (advisor 196, his pick 17 Nov 12:43; RULINGS 17 Nov) ---------------------------------
# Every folder LEDGER writes has a shelf in production/storage-map.json. Step 1 (17 Nov) only READS the map: which
# folders are not on it (flagged in the hourly row, his page after a day) and how full each shelf is (85% = clear it
# that day). Deleting by the map's expiry rules is step 2, after its fixture tests and a hostile fresh review.

MAP = os.environ.get("LEDGER_STORAGE_MAP", os.path.join(REPO, "production", "storage-map.json"))
MAP_ROOTS = ("F:/", "F:/LedgerTools", "C:/LedgerTools")
NOT_OURS = {"$recycle.bin", "system volume information", "vuze"}   # named only, never opened (advisor 196, 1)


def storage_map(path=None):
    return json.load(open(path or MAP, encoding="utf-8"))


def mapped(m, path):
    """The map entry covering path (the folder itself or one it lies inside), the deepest first; None if unmapped."""
    best = None
    for e in m.get("folders", []):
        if inside(path, e["path"]) and (best is None or len(norm(e["path"])) > len(norm(best["path"]))):
            best = e
    return best


def unmapped(m, roots=MAP_ROOTS):
    """Folders directly under each root that no map entry covers (links and his folders left out)."""
    out = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            p = os.path.join(root, name)
            if name.lower() in NOT_OURS or not os.path.isdir(p) or is_link(p):
                continue
            if norm(p) in {norm(r) for r in roots}:
                continue
            if mapped(m, p) is None:
                out.append(p)
    return out


def shelves(m, measure=size_of):
    """F:'s shelves: GB used (the map's folders on F:, measured now) against each shelf's size; over 85% flagged."""
    sizes = m.get("shelves_gb", {}).get("F", {})
    used = {}
    for e in m.get("folders", []):
        p = e["path"]
        if not norm(p).startswith(norm("F:/")) or any(inside(p, o["path"]) and norm(o["path"]) != norm(p)
                                                      for o in m["folders"]):
            continue        # count each tree once, at its top mapped folder
        if os.path.isdir(p) and not is_link(p):
            used[e["shelf"]] = used.get(e["shelf"], 0) + measure(p) / 1e9
    return [{"shelf": s, "gb": round(used.get(s, 0), 1), "sizeGb": sizes[s],
             "over85": used.get(s, 0) > 0.85 * sizes[s]} for s in sizes if s not in ("floor", "spare")]


# ---- THE MAP'S EXPIRY RULES (step 2) ---------------------------------------------------------------------------
# What the rules mean here, and what code cannot judge:
# - working, "3 days, or once its numbers are recorded": a mapped working folder whose newest file is over 3 days
#   old, that no tool names and whose map line proposes removal ("remove..." with no "keep" or "shrink") goes
#   whole. Whether its numbers are recorded, and "a superseded review picture keeps its preview only", are not
#   judged by code: an expired folder the map's line keeps is listed as kept, for the map to be corrected.
# - tools, "14 days unused: removed if refetchable, else his page": a tool is read, not written, so a file date
#   alone does not say it is unused. Unused here = no file written for 14 days AND no tool in the repository names
#   its path. Refetchable = the map's source names a public origin and nothing doubtful (unknown, sign-in,
#   unverified, not refetchable). Unused and refetchable goes only if the map's line proposes removal; unused and
#   not known refetchable is a "his page" candidate (unless the map's line keeps it), never removed.
# - lasting, side-session, build-cache, installed program, not-LEDGER, or any other shelf: never by the map
#   (build caches stay under retention.json's limits and caps).
# - never by the map either: an owner other than LEDGER or Claude (the map says nothing of his is on it; an entry
#   with another owner is his), a line naming a side session, a line backed up ("backup": "yes ..."), a folder
#   holding another mapped folder, a mapped link (its target is mapped where it lives), and everything delete()
#   refuses (outside retention.json's places, protected, backed up, tracked by git, held, named by a report).
# - a folder not on the map is never removed by the map's rules.

MAP_WORKING_DAYS = 3
MAP_TOOLS_DAYS = 14
LEDGER_OWNERS = {"ledger", "claude", "session"}
REFETCH_WORDS = ("public", "pypi", "hugging face", "blender.org", "npm install", "microsoft download",
                 "github runner release", "rebuilt by")
DOUBT_WORDS = ("unknown", "sign-in", "sign in", "unverified", "not refetchable", "not found", "no requirements",
               "needs his", "owner's", "unique")
READER_DIRS = ("tools", os.path.join("ue-probe", "Source"), os.path.join("ue-probe", "Config"),
               os.path.join("production", "specs"), ".github")
READER_EXT = (".py", ".ps1", ".psm1", ".bat", ".cmd", ".json", ".cs", ".cpp", ".h", ".ini", ".yml", ".yaml",
              ".toml", ".txt", ".sh", ".rs")


LINE_FILE = re.compile(r"[A-Za-z0-9_./-]+[.](?:py|ps1|bat|cs|cpp|h|rs|json|ini|yml)")
NOT_READERS = ("production/retention.json", "production/storage-map.json")


def line_reader(e, repo=REPO):
    """A repository file the map's own line names as using the folder ('tools/x.py imports it'), if it exists;
    retention.json and the map itself name folders without reading them."""
    for k in ("serves", "proposal", "source"):
        for f in LINE_FILE.findall(str(e.get(k, ""))):
            f = f.strip("./")
            if f.replace("\\", "/").lower() not in NOT_READERS and os.path.isfile(os.path.join(repo, f)):
                return f
    return None


def map_rules_live(pol):
    return pol.get("mapRulesLive") is True


def reader_text(repo=REPO, extra_dirs=()):
    """Where a path a tool or record reads would be named, lower case, backslashes as '/': every text file git tracks in
    the repository (tools, game source, specs, workflows and the records, approvals and casting notes: the step-2
    review, 17 Nov, B1, found four removal rows named only in records), and the scripts and notes inside the map's
    lasting and protected folders (extra_dirs; a protected run's run_all.ps1 read a removable folder, the scalp
    pattern). Paths built from pieces are missed (INVENTORY-2026-11-17, not measured)."""
    import subprocess
    parts = []
    me = norm(os.path.abspath(__file__))
    skip = {norm(os.path.join(repo or REPO, x)) for x in NOT_READERS}

    def take(f):
        if norm(f) == me or norm(f) in skip or not f.lower().endswith(READER_EXT + (".md", ".jsonl", ".csv")):
            return
        try:
            if os.path.getsize(f) > 2_000_000:
                return
            with open(f, encoding="utf-8", errors="replace") as fh:
                parts.append(fh.read())
        except OSError:
            pass
    if repo is None:
        names, repo = [], REPO
        skip_repo = True
    else:
        listed = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace")
        names = [x for x in listed.split("\0") if x]
        skip_repo = False
    if skip_repo:
        pass
    elif names:
        for n in names:
            take(os.path.join(repo, n))
    else:   # not a checkout (the self-test's folders): the old reader folders
        for d in READER_DIRS:
            for root, dirs, files in os.walk(os.path.join(repo, d)):
                dirs[:] = [x for x in dirs if x not in ("__pycache__", "node_modules", ".git")]
                for n in files:
                    take(os.path.join(root, n))
    for d in extra_dirs:
        seen = 0
        for root, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x not in ("__pycache__", "node_modules", ".git", "target", "Intermediate",
                                                    "Saved", "DerivedDataCache", ".venv")]
            for n in files:
                if n.lower().endswith((".py", ".ps1", ".bat", ".cmd", ".sh", ".json", ".md", ".txt", ".toml", ".ini")):
                    take(os.path.join(root, n))
                    seen += 1
            if seen > 5000:
                break
    return "\n".join(parts).replace("\\\\", "/").replace("\\", "/").lower()


def path_key(p):
    """A path as the reader text writes it, without its drive ('F:/LedgerTools/old' -> '/ledgertools/old')."""
    k = p.replace("\\", "/").rstrip("/").lower()
    return k[2:] if len(k) > 1 and k[1] == ":" else k


def floors(m=None, pol=None):
    """{'C': GB, 'F': GB} each drive keeps free: the map's floors (their home since 17 Nov), else retention.json's,
    else 40 and 20."""
    out = {"C": 40.0, "F": 20.0}
    for d in out:
        v = (pol or {}).get("floors", {}).get(d)
        if isinstance(v, (int, float)):
            out[d] = float(v)
        v = (m or {}).get("shelves_gb", {}).get(d, {}).get("floor")
        if isinstance(v, (int, float)):
            out[d] = float(v)
    return out


def floor_rows(fl, free, freed_bytes):
    """One row per drive: free now, its floor, free after what would be removed, and whether it is below."""
    rows = []
    for d in ("C", "F"):
        f = free.get(d)
        after = None if f is None else round(f + freed_bytes.get(d, 0) / 1e9, 1)
        rows.append({"drive": d, "free": f, "floor": fl[d], "after": after,
                     "below": f is not None and f < fl[d], "belowAfter": after is not None and after < fl[d]})
    return rows


def map_plan(m, pol, now=None, readers=None):
    """What the map's expiry rules say now: {'remove': [(path, rule, why)], 'hisPage': [(path, rule, why)],
    'refused': [(path, rule, why)], 'kept': [(path, why, expired)]}. Removes nothing."""
    now = now or time.time()
    out = {"remove": [], "hisPage": [], "refused": [], "kept": []}
    folders = m.get("folders", [])
    if not isinstance(folders, list):
        raise ValueError("folders is %s, not a list" % type(folders).__name__)
    folders = [e for e in folders if isinstance(e, dict) and isinstance(e.get("path"), str) and e.get("path").strip()]
    text, protected_extra = None, None
    reals = [(i, real(e["path"]), str(e.get("shelf", "")).strip().lower(), str(e.get("owner", "") or "").strip().lower())
             for i, e in enumerate(folders)]

    def kept(p, why, expired=False):
        out["kept"].append((p, why, expired))

    for idx, e in enumerate(folders):
        p = e.get("path", "")
        if not p:
            continue
        shelf = str(e.get("shelf", "")).strip().lower()
        if shelf in ("working", "tools"):
            # S1: the guarantee goes by the real folder, not its spelling
            me = real(p)
            if ".." in p.replace("\\", "/").split("/"):
                kept(p, "the path climbs with '..': never removed by the map (S1)")
                continue
            if me != os.path.normcase(os.path.abspath(p)):
                kept(p, "the path reaches its folder through a link or a short name: never removed by the map (S1)")
                continue
            twin = [i for i, r, sh, ow in reals if i != idx and (r == me or me.startswith(r.rstrip(os.sep) + os.sep))
                    and (sh not in ("working", "tools") or ow not in LEDGER_OWNERS)]
            if twin:
                kept(p, "another line (%s) holds the same folder or a parent of it: never removed by the map (S1)"
                     % folders[twin[0]]["path"])
                continue
        line = " ".join(str(e.get(k, "")) for k in ("source", "serves", "proposal")).lower()
        proposal = str(e.get("proposal", "")).strip().lower()
        owner = str(e.get("owner", "") or "").strip().lower()
        if shelf not in ("working", "tools"):
            kept(p, "shelf %s: never removed by the map" % (shelf or "missing"))
            continue
        if owner not in LEDGER_OWNERS:
            # when in doubt, it is his (RULINGS 29 Oct; the step-2 review, 17 Nov, B2): only a line whose owner is
            # written as LEDGER's or Claude's may be removed by the map's rules
            kept(p, "owner %s: only an owner written as LEDGER or Claude is touched" % (e.get("owner") or "not written"))
            continue
        src = str(e.get("source", "") or "").strip().lower()
        if shelf == "working" and (not src or any(w in src for w in DOUBT_WORDS)):   # tools rows in doubt go to his page below
            # the second review, 17 Nov, N1: the map writes "unknown"; any doubt or no source is his
            kept(p, "source %s: when in doubt, it is his" % (src or "not written"))
            continue
        if os.path.basename(p.rstrip("/\\")).lower() in NOT_OURS:
            kept(p, "not LEDGER's")
            continue
        if "side session" in line or "side-session" in line:
            kept(p, "a side session's work: never touched")
            continue
        if str(e.get("backup", "")).strip().lower().startswith("yes"):
            kept(p, "backed up: never removed")
            continue
        if is_link(p):
            kept(p, "a link: its target is mapped where it lives")
            continue
        if not os.path.exists(p):
            kept(p, "not on disk")
            continue
        inner = [o["path"] for o in folders if o.get("path") and norm(o["path"]) != norm(p) and inside(o["path"], p)]
        if inner:
            kept(p, "holds another mapped folder (%s)" % inner[0])
            continue
        days = MAP_WORKING_DAYS if shelf == "working" else MAP_TOOLS_DAYS
        age = (now - MAP_AGE[0](p)) / 86400
        if age <= days:
            kept(p, "written %.1f day(s) ago, inside its %d days" % (age, days))
            continue
        if text is None:
            text = reader_text() if readers is None else readers.replace("\\\\", "/").replace("\\", "/").lower()
            # the second review, 17 Nov, N2: every mapped folder (any shelf) and every protected path is scanned,
            # each kept apart so a folder's own files never count as its own reader
            scan = [o["path"] for o in folders if o.get("path") and os.path.isdir(o["path"])]
            scan += [x for x in pol.get("protected", []) if isinstance(x, str) and os.path.isdir(x)]
            others = [(d, reader_text(None, extra_dirs=[d])) for d in dict.fromkeys(scan)]
        key = path_key(p)
        by_folder = [d for d, t in others if not inside(d, p) and _named(t, key)]
        if _named(text, key) or by_folder:
            kept(p, "no write for %.0f days, but %s names it" % (age, ("files in " + by_folder[0]) if by_folder
                                                                    else "a tool in the repository"), True)
            continue
        named_by = line_reader(e)
        if named_by:
            kept(p, "no write for %.0f days, but the map's line names a reader (%s)" % (age, named_by), True)
            continue
        says_remove = ((proposal.startswith("remove:") or proposal.startswith("remove candidate")
                        or proposal.startswith("remove ")) and not proposal.startswith("removed")
                       and not re.search(r"\b(keep|kept|shrink|his yes|check with him|needs his|ask)\b", proposal))
        rule = "map %s %dd" % (shelf, days)
        if shelf == "tools":
            source = str(e.get("source", "")).lower()
            refetch = any(w in source for w in REFETCH_WORDS) and not any(w in source for w in DOUBT_WORDS)
            if not refetch:
                if "keep" in proposal:
                    kept(p, "unused %.0f days, not known refetchable; the map's line keeps it (%s)"
                         % (age, e.get("proposal", "")), True)
                else:
                    out["hisPage"].append((p, rule, "unused %.0f days, no tool names it, not known refetchable (source: %s)"
                                           % (age, e.get("source", "") or "none")))
                continue
            if not says_remove:
                kept(p, "unused %.0f days and refetchable; the map's line keeps it (%s)" % (age, e.get("proposal", "")), True)
                continue
            why = "unused %.0f days, no tool names it, refetchable (%s)" % (age, e.get("source", ""))
        else:
            if not says_remove:
                kept(p, "no write for %.0f days; the map's line keeps it (%s)" % (age, e.get("proposal", "")), True)
                continue
            why = "no write for %.0f days, no tool names it; the map: %s" % (age, e.get("proposal", ""))
        if protected_extra is None:
            protected_extra = backup_paths() + named_keep(pol)
        ok, reason = may_delete(pol, p, protected_extra)
        if not ok:
            out["refused"].append((p, rule, reason))
            continue
        out["remove"].append((p, rule, why))
    return out


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
        pol = policy()
        try:
            m = storage_map()
            mp = map_plan(m, pol)
        except Exception as e:              # S4
            print("storage map unreadable (%s): the map's rules list nothing" % e)
            m, mp = {}, {"remove": [], "hisPage": [], "refused": [], "kept": []}
        live = map_rules_live(pol)
        res = enforce(pol, dry=(cmd == "plan"), mp=mp)
        verb = "would" if cmd == "plan" else "deleted"
        row = lambda r: "%s %7.2f GB  %-26s %s%s" % ("REFUSED" if "refused" in r else verb, r.get("bytes", 0) / 1e9,
                                                     r["rule"], r["path"],
                                                     ("  (" + r["refused"] + ")") if "refused" in r else "")
        print("== retention.json limits")
        for r in res:
            if not r.get("map"):
                print(row(r))
        print("== storage map rules (%s)" % ("live" if live else "NOT LIVE: listed only; run removes them once "
                                              "production/retention.json sets \"mapRulesLive\": true"))
        for r in res:
            if r.get("map"):
                print(row(r) + ("" if "refused" in r else "  [" + r["why"] + "]"))
        for p, rule, why in mp["refused"]:
            print("REFUSED %7.2f GB  %-26s %s  (%s)" % (size_of(p) / 1e9, rule, p, why))
        page_bytes = 0
        for p, rule, why in mp["hisPage"]:
            b = size_of(p)
            page_bytes += b
            print("HISPAGE %7.2f GB  %-26s %s  (%s)" % (b / 1e9, rule, p, why))
        expired_kept = [k for k in mp["kept"] if k[2]]
        for p, why, _ in expired_kept:
            print("kept    expired   %-26s %s  (%s)" % ("map", p, why))
        print("map: %d folder(s) kept that are not expired or never removed by the map" % (len(mp["kept"]) - len(expired_kept)))
        done = [r for r in res if "refused" not in r]
        freed = {}
        for r in done:
            d = r["path"][:1].upper()
            freed[d] = freed.get(d, 0) + r.get("bytes", 0)
        for f in floor_rows(floors(m, pol), free_gb(), freed):
            print("floor %s: %s GB free, floor %.0f, after this %s%s" % (
                f["drive"], f["free"], f["floor"], f["after"],
                "  BELOW ITS FLOOR: his page within the hour (the map's shelf rule)" if f["belowAfter"] else ""))
        lim_b = sum(r.get("bytes", 0) for r in done if not r.get("map"))
        map_b = sum(r.get("bytes", 0) for r in done if r.get("map"))
        print("%s: %.2f GB in %d place(s) (limits %.2f GB, map %.2f GB%s); his page %.2f GB in %d" % (
            cmd, (lim_b + map_b) / 1e9, len(done), lim_b / 1e9, map_b / 1e9, "" if live else ", not live",
            page_bytes / 1e9, len(mp["hisPage"])))
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
    if cmd == "unmapped":
        out = unmapped(storage_map())
        for p in out:
            print("UNMAPPED " + p)
        print("unmapped=%d" % len(out))
        return 0
    if cmd == "shelves":
        for s in shelves(storage_map()):
            print("%-10s %6.1f GB of %5.1f%s" % (s["shelf"], s["gb"], s["sizeGb"], "  OVER 85%" if s["over85"] else ""))
        return 0
    if cmd == "space":
        try:
            fl = floors(storage_map(), policy())
        except (OSError, ValueError):
            fl = floors(None, policy())
        r = space(opt("--job", "a job"), float(opt("--need-c", fl["C"])), float(opt("--need-f", fl["F"])), opt("--drives", "CF"))
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
