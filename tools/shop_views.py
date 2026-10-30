#!/usr/bin/env python3
"""A SHOP FRONT'S OWN GATE VIEWS IN THE EDITOR, REPEATABLY (from the left, square on, from the right and across the road,
by day or at night).

    python tools/shop_views.py OUT_DIR [--night] [--shop chandler@42.025] [--game-arg -Switch ...]
    python tools/shop_views.py --selftest

WHY, 30 October 2026 (his order D11, the look; the chandler's wear, S1 and S3): each shop's gate since 3 October has
been photographed by the game's own -PageShots=shop / shopnight (CrimeProbe.cpp PageShotsTick: 1.2 m out on the pavement
from the left, square on and from the right, each looking at the window's middle, and the whole front from across the
road), people hidden, but each round's command line was kept nowhere and the chandler's window middle (street x 42.025,
its display's x 40.35 to 43.70) had to be read back off its pictures. This keeps the command line and the game's
summary lines beside the pictures. The editor's game, at the level the game ships at (-ExecCmds "scalability 2"), from
the project's staged copy of the repository's files, refreshed first (as tools/street_views.py). Nothing here runs while
the build machine works or Unreal is open (the caller checks).
"""
import glob
import os
import shutil
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UE = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
PROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")
# the street as played (an editor photograph waits silently without them: tools/p1-packaged.ps1's list)
BASE = ["-LedgerSlice", "-LedgerCrime", "-Encounter=live", "-LiveFresh", "-TalkFake", "-NoTitle", "-PageNoPeople"]
KEEP = ("LedgerPageShots", "LedgerWear", "LedgerBrickStreaks", "LedgerClock light", "streetStatus=")
SHOP = "chandler@42.025"


def command(night=False, shop=SHOP, extra=()):
    return [UE, PROJECT, "-game"] + BASE + ["-PageShots=" + ("shopnight" if night else "shop"), "-PageShopList=" + shop,
                                            "-PageShotSize=2560x1440", "-ResX=2560", "-ResY=1440", "-windowed", "-unattended",
                                            "-nosplash", "-nopause", '-ExecCmds="scalability 2"', "-log=shop-views.log"] + list(extra)


def run(out, night, shop, extra):
    os.makedirs(out, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(REPO, "tools", "ue", "stage_game_data.py")], cwd=REPO, capture_output=True)
    shutil.copyfile(os.path.join(REPO, "production", "specs", "vignette-pieces.json"), os.path.join(REPO, "ue-probe", "vignette-pieces.json"))
    shots = os.path.join(REPO, "ue-probe", "Saved", "PageShots")
    for p in glob.glob(os.path.join(shots, "*.png")):
        os.remove(p)
    cmd = command(night, shop, extra)
    line = " ".join('"%s"' % x if " " in x and '"' not in x else x for x in cmd)
    open(os.path.join(out, "command.txt"), "w", encoding="utf-8").write(line + "\n")
    t0 = time.time()
    g = subprocess.Popen(line, cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        g.wait(timeout=1200)
    except subprocess.TimeoutExpired:
        print("shopViews status=TIMEOUT after 1200 s")
        # its own editor only, by its process tree (never every editor by name)
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(g.pid)], capture_output=True)
    got = []
    for p in sorted(glob.glob(os.path.join(shots, "*.png"))):
        shutil.copyfile(p, os.path.join(out, os.path.basename(p)))
        got.append(os.path.basename(p))
    log = os.path.join(REPO, "ue-probe", "Saved", "Logs", "shop-views.log")
    lines = []
    if os.path.exists(log):
        shutil.copyfile(log, os.path.join(out, "shop-views.log"))
        lines = [l.rstrip()[:600] for l in open(log, encoding="utf-8", errors="replace") if any(k in l for k in KEEP)]
    open(os.path.join(out, "shop-lines.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("shopViews pictures=%s seconds=%d night=%d out=%s" % (",".join(got) or "NONE", time.time() - t0, night, out))
    return 0 if len(got) == 4 else 1


def selftest():
    c = command(True, "chandler@42.025", ["-NoBrickStreaks"])
    ok = [c[0] == UE, "-PageShots=shopnight" in c, "-PageShopList=chandler@42.025" in c, "-PageNoPeople" in c,
          '-ExecCmds="scalability 2"' in c, not any(x.startswith("-LedgerRepo=") for x in c), c[-1] == "-NoBrickStreaks",
          "-PageShots=shop" in command(False)]
    print("shop_views selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    sys.exit(run(a[0], "--night" in a, a[a.index("--shop") + 1] if "--shop" in a else SHOP,
                 [a[i + 1] for i, x in enumerate(a) if x == "--game-arg"]))
