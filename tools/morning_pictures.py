#!/usr/bin/env python3
"""THE MORNING PICTURES: THE SAME THREE VIEWS EVERY MORNING, SO JAFAR CAN WATCH THE STREET CHANGE.

Jafar, 5 October 2026 (the plan's edit 8): "every morning by 07:30, the same three views, the
hook camera by day, the reverse view and the street at night, as previews in production/previews/,
shown in the overview beside yesterday's and beside the Hook sheet. No decision asked; they are so
I can watch the street change." And his goal of the same day: the overview names the phase, the
current item and the next by 07:30 each morning.

WHAT IT DOES, run at 05:15 by Windows' Task Scheduler (the task "LEDGER morning pictures"):
 1. waits until nothing else drives Unreal (the build machine's Runner.Worker, an editor, a build),
    giving up at 06:50 so the overview still says why by 07:30;
 2. checks the free space (C: 40 GB, F: 20 GB) through tools/retention.py;
 3. films the street with the game's own vignette mode (about seven minutes; every shot of
    production/specs/vignette-scene.json, the same frames the build machine judges) and keeps
    three: vign_hook_day, vign_reverse_day and vign_hook_night, full size on
    F:/LedgerTools/renders/morning/<date>;
 4. writes their previews, production/previews/morning-{hook-day,reverse-day,night}-<date>.jpg;
 5. writes the morning's record on his progress page's data (production/progress-page/progress.json,
    its "street" block, read by tools/progress_page.py and the page): today's date added to
    street.days when all three previews exist, and street.morning: the phase, the current item and
    the next (read from NOW.md, their home), today's three and yesterday's, the Hook sheet, and on
    Mondays the repository's size;
 6. commits only those files and pushes them to the branch wip when that is a fast-forward.
Any failure is written into the record plainly ("no morning pictures today: ..."), never skipped.

9 NOV 2026 (RULINGS 9 Nov, records): the overview's summary file is stopped, so step 5 no longer
rewrites a morning block there; the same content goes on the progress page's data instead. The
pictures, the commit and the push are unchanged.

  python tools/morning_pictures.py               # the whole morning
  python tools/morning_pictures.py --no-film     # steps 4 to 6 from today's renders already on F:
  python tools/morning_pictures.py --block-only  # only the progress page's morning record (no film, no commit)
  python tools/morning_pictures.py --no-commit   # the whole morning but the commit (a trial run)
  python tools/morning_pictures.py --selftest
"""
import argparse
import datetime as dt
import io
import os
import re
import shutil
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

UE = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
PROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")
RENDERS = "F:/LedgerTools/renders/morning"
VIEWS = [  # (shot, preview name, the line's words)
    ("vign_hook_day", "morning-hook-day", "The hook camera by day"),
    ("vign_reverse_day", "morning-reverse-day", "The reverse view"),
    ("vign_hook_night", "morning-night", "The street at night"),
]
HOOK_SHEET_PREVIEW = "production/previews/hook-sheet-2026-10-05.jpg"
BUSY = ("runner.worker", "unrealeditor", "unrealbuildtool", "build.bat", "unrealeditor-cmd")
GIVE_UP_AT = dt.time(6, 50)
PROGRESS_REL = "production/progress-page/progress.json"
PROGRESS = os.path.join(REPO, *PROGRESS_REL.split("/"))


def log(msg):
    print("%s %s" % (dt.datetime.now().strftime("%H:%M:%S"), msg), flush=True)


def busy():
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=60).stdout.lower()
    except Exception:
        return "tasklist failed"
    for name in BUSY:
        if name in out:
            return name
    return ""


def wait_idle():
    while True:
        b = busy()
        if not b:
            return ""
        if dt.datetime.now().time() >= GIVE_UP_AT:
            return "the PC was still busy with %s at %s" % (b, GIVE_UP_AT.strftime("%H:%M"))
        time.sleep(60)


def space_ok():
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "retention.py"), "space",
                        "--job", "morning pictures", "--drives", "CF"], capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1]


def film(day):
    shutil.copyfile(os.path.join(REPO, "production", "specs", "vignette-pieces.json"),
                    os.path.join(REPO, "ue-probe", "vignette-pieces.json"))
    for v in VIEWS:
        p = os.path.join(REPO, "ue-probe", "ue-%s.png" % v[0])
        if os.path.exists(p):
            os.remove(p)
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=REPO).stdout.strip()
    args = [UE, PROJECT, "-game", "-LedgerVignette", "-NoControlQuads", "-LedgerCommit=morning-" + sha,
            "-ResX=2560", "-ResY=1440", "-windowed", "-unattended", "-nosplash", "-nopause", "-log=morning.log"]
    log("filming at %s" % sha)
    try:
        subprocess.run(args, cwd=REPO, timeout=1800, capture_output=True)
    except subprocess.TimeoutExpired:
        return "the film ran past 30 minutes and was stopped", sha
    out = os.path.join(RENDERS, day.isoformat())
    os.makedirs(out, exist_ok=True)
    missing = []
    for shot, _, _ in VIEWS:
        src = os.path.join(REPO, "ue-probe", "ue-%s.png" % shot)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(out, "ue-%s.png" % shot))
        else:
            missing.append(shot)
    return ("the film gave no " + ", ".join(missing)) if missing else "", sha


def previews(day):
    import make_preview
    made = []
    for shot, name, _ in VIEWS:
        src = os.path.join(RENDERS, day.isoformat(), "ue-%s.png" % shot)
        if os.path.exists(src):
            make_preview.make(src, name, day.isoformat())
            made.append("production/previews/%s-%s.jpg" % (name, day.isoformat()))
    return made


def now_items(now_text):
    """(phase title, current item, next item) from NOW.md, the list's home: the first open item,
    the phase heading above it, and the open item after it."""
    phase, cur, nxt, seen_phase = "", "", "", ""
    for line in now_text.splitlines():
        m = re.match(r"^##\s+(Phase\s+\d+[^(]*)", line)
        if m:
            seen_phase = m.group(1).strip().rstrip(":")
            continue
        m = re.match(r"^- \[ \] (.+)$", line)
        if m:
            if not cur:
                cur, phase = m.group(1).strip(), seen_phase
            elif not nxt:
                nxt = m.group(1).strip()
                break
    return phase, cur, nxt


def record(day, failure, now_text, exists=os.path.exists):
    """The morning's record for the progress page's street.morning (until 9 Nov the overview's block in
    the stopped summary file): the line naming the phase, the current item and the next, any failure
    said plainly, today's three pictures beside yesterday's (None where there is none), the Hook sheet,
    and on Mondays the repository's size."""
    phase, cur, nxt = now_items(now_text)
    y = day - dt.timedelta(days=1)
    line = "Morning, %s. %s. On: %s. Next: %s." % (day.strftime("%A %d %B").replace(" 0", " "),
                                                  (phase or "No phase open").replace(": ", ", ", 1),
                                                  (cur or "nothing open").rstrip("."), (nxt or "nothing after it").rstrip("."))
    views = []
    for _, name, words in VIEWS:
        cells = {}
        for key, d in (("today", day), ("yesterday", y)):
            p = "production/previews/%s-%s.jpg" % (name, d.isoformat())
            cells[key] = p if exists(os.path.join(REPO, p)) else None
        views.append(dict(label=words, **cells))
    rec = {"date": day.isoformat(), "line": line,
           "failure": ("No morning pictures today: %s. Yesterday's stand." % failure) if failure else "",
           "views": views, "hook_sheet": HOOK_SHEET_PREVIEW,
           "note": "No decision asked: these are for watching the street change.",
           "by": "tools/morning_pictures.py"}
    # MONDAYS, THE REPOSITORY'S SIZE (Jafar, 5 October 2026, after the history was cleaned from
    # 30.8 GB to about 3 GB: "the repository's size goes into the Monday review").
    if day.weekday() == 0:
        rec["repo_size"] = repo_size()
    return rec


def repo_size():
    """GitHub's own figure for the repository and this PC's packed history, or why not measured."""
    import urllib.request
    import json as _json
    gh = "not measured (GitHub did not answer)"
    try:
        with urllib.request.urlopen("https://api.github.com/repos/jsab258/ledger", timeout=20) as r:
            kb = _json.load(r).get("size")
            if isinstance(kb, int):
                gh = "%.2f GB on GitHub" % (kb / 1e6)
    except Exception:
        pass
    local = "not measured here"
    try:
        out = subprocess.run(["git", "count-objects", "-v"], cwd=REPO, capture_output=True, text=True).stdout
        kb = sum(int(l.split()[1]) for l in out.splitlines() if l.startswith(("size:", "size-pack:")))
        local = "%.2f GB packed on this PC" % (kb / 1e6)
    except Exception:
        pass
    return "%s; %s (the history was 30.8 GB before 5 October's cleaning; a guard refuses large files before every push)." % (gh, local)


def put_record(data, rec):
    """The record into the progress page's data: street.morning replaced (never repeated), and the
    day added to street.days when all three of its previews exist (the page's flipbook and
    tools/progress_page.py --check read that list)."""
    street = data.setdefault("street", {})
    street["morning"] = rec
    if all(v["today"] for v in rec["views"]):
        street["days"] = sorted(set(street.get("days", [])) | {rec["date"]})
    return data


def write_record(day, failure, now_text):
    import json
    data = json.load(io.open(PROGRESS, encoding="utf-8"))
    put_record(data, record(day, failure, now_text))
    with io.open(PROGRESS, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def commit(paths, day):
    for attempt in range(5):
        r = subprocess.run(["git", "add", "--"] + paths, cwd=REPO, capture_output=True, text=True)
        if r.returncode == 0:
            r = subprocess.run(["git", "commit", "-q", "-m",
                                "Morning pictures, %s: the hook by day, the reverse view, the street at night\n\n"
                                "Made by tools/morning_pictures.py (Jafar, 5 October: the same three views every\n"
                                "morning by 07:30, beside yesterday's and the Hook sheet; no decision).\n\n"
                                "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" % day.isoformat(),
                                "--"] + paths, cwd=REPO, capture_output=True, text=True)
            if r.returncode == 0:
                break
        if "index.lock" not in (r.stderr or ""):
            return "commit failed: " + (r.stderr or r.stdout).strip()[:200]
        time.sleep(20)
    else:
        return "commit failed: the index stayed locked"
    subprocess.run(["git", "fetch", "-q", "origin", "wip"], cwd=REPO, capture_output=True)
    ff = subprocess.run(["git", "merge-base", "--is-ancestor", "origin/wip", "HEAD"], cwd=REPO).returncode == 0
    if not ff:
        return "committed; not pushed (wip has commits this copy lacks; the session pushes)"
    r = subprocess.run(["git", "push", "-q", "origin", "HEAD:wip"], cwd=REPO, capture_output=True, text=True)
    return "committed and pushed to wip" if r.returncode == 0 else "committed; push failed: " + r.stderr.strip()[:200]


def run(day, do_film=True, do_commit=True):
    failure = ""
    if do_film:
        failure = wait_idle()
        if not failure:
            ok, line = space_ok()
            if not ok:
                failure = "the free-space check refused (%s)" % line
        if not failure:
            failure, _ = film(day)
    made = previews(day)
    if not made and not failure:
        failure = "no renders were found for today"
    now_text = io.open(os.path.join(REPO, "NOW.md"), encoding="utf-8").read()
    write_record(day, failure, now_text)
    log("progress page's morning record written%s" % (": " + failure if failure else ""))
    if do_commit:
        log(commit(made + [PROGRESS_REL], day))
    return 0 if not failure else 1


def selftest():
    ok = True

    def check(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    now_text = "GOAL\n\n## Phase 0: recover control (0.20W)\n\n- [x] 0.1 done.\n- [ ] 0.2 Time log.\n- [ ] 0.3 Sweep.\n\n## Phase 1: prove (1.00W)\n\n- [ ] 1.1 Mickey's.\n"
    check(now_items(now_text) == ("Phase 0: recover control", "0.2 Time log.", "0.3 Sweep."), "the phase, the current item and the next come from NOW.md")
    check(now_items(now_text.replace("- [ ] 0.2", "- [x] 0.2").replace("- [ ] 0.3", "- [x] 0.3"))[0:2] == ("Phase 1: prove", "1.1 Mickey's."), "when phase 0 is done the block names phase 1")
    day = dt.date(2026, 10, 6)
    b = record(day, "", now_text, exists=lambda p: "2026-10-06" in p)
    check(b["date"] == "2026-10-06" and all(v["today"] and v["yesterday"] is None for v in b["views"]) and "hook-sheet" in b["hook_sheet"]
          and "On: 0.2 Time log. Next: 0.3 Sweep." in b["line"] and "repo_size" not in b, "today's three beside yesterday's (none yet) and the Hook sheet")
    b2 = record(day, "the PC was still busy", now_text, exists=lambda p: False)
    check("No morning pictures today: the PC was still busy" in b2["failure"], "a failure is said plainly, never skipped")
    data = {"street": {"days": ["2026-10-05"], "views": []}, "stations": []}
    put_record(data, b)
    check(data["street"]["days"] == ["2026-10-05", "2026-10-06"] and data["street"]["morning"]["date"] == "2026-10-06" and data["stations"] == [],
          "the record goes on the progress page's street block and its day joins the flipbook's days")
    put_record(data, b2)
    check(data["street"]["morning"] is b2 and data["street"]["days"] == ["2026-10-05", "2026-10-06"],
          "a second record replaces the first, and a day without its three pictures is not added")
    check("FOR-" + "JAFAR" not in open(os.path.abspath(__file__), encoding="utf-8").read(),
          "the stopped summary file is neither written nor required (RULINGS 9 Nov)")
    sink = io.StringIO()
    hook = "%s-2026-10-05.jpg" % VIEWS[0][1]
    check(fresh(2, dt.date(2026, 10, 7), [hook, "x.jpg"], sink) == 0, "pictures two days old pass")
    check(fresh(2, dt.date(2026, 10, 8), [hook], sink) == 1, "pictures three days old fail the build")
    check(fresh(2, dt.date(2026, 10, 5), [], sink) == 1, "no morning pictures at all fail too")
    print("morning_pictures selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def fresh(days, today=None, names=None, out=sys.stdout):
    """THE MORNING PICTURES' OWN ALARM (5 October, the phase 0 exit's reviewer: nothing failed the
    build if the 05:15 task stopped). Fails when the newest hook-camera preview is missing or more
    than `days` days old."""
    if names is None:
        d = os.path.join(REPO, "production", "previews")
        names = os.listdir(d) if os.path.isdir(d) else []
    pre = "%s-" % VIEWS[0][1]
    days_seen = []
    for n in names:
        if n.startswith(pre) and n.endswith(".jpg"):
            try:
                days_seen.append(dt.date.fromisoformat(n[len(pre):-4]))
            except ValueError:
                pass
    last = max(days_seen) if days_seen else None
    age = ((today or dt.date.today()) - last).days if last else None
    ok = age is not None and age <= days
    print("morning-fresh newest=%s ageDays=%s limit=%d outcome=%s" % (last, age, days, "PASS" if ok else "FAIL"), file=out)
    if not ok:
        print("morning-fresh FAIL no morning pictures for over %d days: the task 'LEDGER morning pictures' (05:15) has stopped or failed" % days, file=out)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-film", action="store_true")
    ap.add_argument("--block-only", action="store_true")
    ap.add_argument("--no-commit", action="store_true")
    ap.add_argument("--date")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fresh", type=int)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.fresh is not None:
        return fresh(a.fresh)
    # ANY GAME WINDOW LEFT OPEN IS CLOSED FIRST (Jafar, 7 October: three copies left by a cut-off
    # measurement held the graphics card and the film ran past its time).
    if not a.block_only:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import close_games
            close_games.close_games()
        except Exception as e:
            print("morning_pictures: close games failed: %s" % e)
    day = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    if a.block_only:
        now_text = io.open(os.path.join(REPO, "NOW.md"), encoding="utf-8").read()
        write_record(day, "", now_text)
        return 0
    return run(day, do_film=not a.no_film, do_commit=not a.no_commit)


if __name__ == "__main__":
    sys.exit(main())
