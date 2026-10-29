#!/usr/bin/env python3
"""THE STREET'S THREE GATE VIEWS IN THE EDITOR, REPEATABLY (the hook camera by day, the reverse view, the street at night).

    python tools/street_views.py OUT_DIR [--game-arg -Switch ...]
    python tools/street_views.py --selftest

WHY, 29 October 2026 (his order D11, the look): each view's gate needs the same three pictures as the morning's
(tools/morning_pictures.py film: the editor's -LedgerVignette run), but at the level the game ships at (-ExecCmds
"scalability 2", as every editor gate picture since 26 October) and from the project's staged copy of the repository's
files, refreshed first,
and until today each round was started by hand with its command line kept nowhere. This keeps the command line and
the street's own summary lines beside the pictures. Nothing here runs while the build machine works or Unreal is open.
"""
import os
import shutil
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UE = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
PROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")
SHOTS = ("vign_hook_day", "vign_reverse_day", "vign_hook_night")
KEEP = ("streetStatus=", "LedgerWear", "lookFrom=", "LedgerClock light")


def command(extra=()):
    # NOT -LedgerRepo (29 October: with it the vignette's hook shot came out as Tom seated in the office, where the
    # morning job's own run, which reads the project's staged copy, shows the street); tools/ue/stage_game_data.py
    # refreshes that copy first (run())
    return [UE, PROJECT, "-game", "-LedgerVignette", "-NoControlQuads", "-LedgerCommit=gate", "-ResX=2560", "-ResY=1440",
            "-windowed", "-unattended", "-nosplash", "-nopause", '-ExecCmds="scalability 2"',
            "-log=street-views.log"] + list(extra)


def run(out, extra):
    os.makedirs(out, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(REPO, "tools", "ue", "stage_game_data.py")], cwd=REPO, capture_output=True)
    shutil.copyfile(os.path.join(REPO, "production", "specs", "vignette-pieces.json"), os.path.join(REPO, "ue-probe", "vignette-pieces.json"))
    for s in SHOTS:
        p = os.path.join(REPO, "ue-probe", "ue-%s.png" % s)
        if os.path.exists(p):
            os.remove(p)
    cmd = command(extra)
    line = " ".join('"%s"' % x if " " in x and '"' not in x else x for x in cmd)
    open(os.path.join(out, "command.txt"), "w", encoding="utf-8").write(line + "\n")
    t0 = time.time()
    try:
        subprocess.run(line, cwd=REPO, timeout=1800, capture_output=True)
    except subprocess.TimeoutExpired:
        print("streetViews status=TIMEOUT after 1800 s")
    got = []
    for s in SHOTS:
        src = os.path.join(REPO, "ue-probe", "ue-%s.png" % s)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(out, "ue-%s.png" % s))
            got.append(s)
    log = os.path.join(REPO, "ue-probe", "Saved", "Logs", "street-views.log")
    lines = []
    if os.path.exists(log):
        shutil.copyfile(log, os.path.join(out, "street-views.log"))
        lines = [l.rstrip()[:600] for l in open(log, encoding="utf-8", errors="replace") if any(k in l for k in KEEP)]
    open(os.path.join(out, "street-lines.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("streetViews pictures=%s seconds=%d out=%s" % (",".join(got) or "NONE", time.time() - t0, out))
    return 0 if len(got) == len(SHOTS) else 1


def selftest():
    c = command(["-NoOfficeGrade"])
    ok = [c[0] == UE, "-LedgerVignette" in c, '-ExecCmds="scalability 2"' in c, not any(x.startswith("-LedgerRepo=") for x in c),
          c[-1] == "-NoOfficeGrade"]
    print("street_views selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    sys.exit(run(a[0], [a[i + 1] for i, x in enumerate(a) if x == "--game-arg"]))
