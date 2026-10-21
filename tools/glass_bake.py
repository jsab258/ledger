"""Bake the shop glass: the street each window reflects, caught once by day and once at night, for
the game to look up instead of catching it in play.

    python tools/glass_bake.py              # two game runs (about two minutes each), then the stamp
    python tools/glass_bake.py --selftest

WHY, 21 October 2026 (his order, item 6; production/cloud-week/research/1d-shop-glass-without-frame-cost.md,
route A): the game's slow frames were its catches, the windows' street pictures re-taken with full
Lumen at load and at each change of light. Shipped games take such pictures once per light at build
time and only look them up. Each run here starts the game in the street as it is played
(-LedgerSlice -LedgerCrime -Encounter=live), in day or night light (-PageShots=bake -GlassBake=day|night,
CrimeProbe.cpp), catches every window live as before (the heroes at their 1024, the rest at 512),
writes each window's cube as <mesh>.hdr (VignetteShot.cpp DumpGlassCatches) under
F:/LedgerTools/game-inputs/glass-bake/<light>/ and quits. Then manifest.json records the hashes of the
files the street was built from (tools/ue/import_glass_bake.py STAMPED), which the import checks.

RUN IT AFTER EVERY STREET EXPORT, LOOK OR SHOP CHANGE: a stale bake is not imported, and the game
then catches every window live (right, but its slow frames come back). It refuses to start while the
build machine, an editor or a game runs (their pictures and graphics work would be in it).
"""
import json
import os
import shutil
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "ue"))
import import_glass_bake as IGB  # noqa: E402

UE = os.environ.get("LEDGER_UE", r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe")
PROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")


def busy():
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout
    except OSError:
        return []
    return [n for n in ("Runner.Worker", "UnrealEditor", "LedgerProbe") if n.lower() in out.lower()]


def args_for(light, out_dir):
    return [UE, PROJECT, "-game", "-LedgerSlice", "-LedgerCrime", "-Encounter=live", "-LiveFresh", "-TalkFake",
            "-NoTitle", "-PageShots=bake", "-GlassBake=" + light, "-GlassBakeDir=" + out_dir.replace("\\", "/"),
            "-RenderOffScreen", "-ResX=1280", "-ResY=720", "-LedgerRepo=" + REPO.replace("\\", "/"),
            "-unattended", "-nosplash", "-nopause", "-log=glass-bake-%s.log" % light]


def bake(root=IGB.BAKE_ROOT):
    who = busy()
    if who:
        print("glassBake status=BUSY running=%s" % ",".join(who))
        return 2
    t0 = time.time()
    got = {}
    for light in IGB.LIGHTS:
        d = os.path.join(root, light)
        if os.path.isdir(d):
            shutil.rmtree(d)            # this tool's own last bake, never anything else
        os.makedirs(d)
        subprocess.run(args_for(light, root), timeout=900)
        got[light] = sorted(os.path.splitext(n)[0] for n in os.listdir(d) if n.endswith(".hdr"))
        print("glassBake light=%s windows=%d" % (light, len(got[light])))
    if not got["day"] or got["day"] != got["night"]:
        print("glassBake status=FAILED day=%d night=%d (each light must catch the same windows)" % (len(got["day"]), len(got["night"])))
        return 1
    man = {"what": "the shop glass's street, baked by tools/glass_bake.py (route A of research note 1d); "
                   "imported by tools/ue/import_glass_bake.py only while every stamped file is unchanged",
           "made": time.strftime("%Y-%m-%dT%H:%M:%S"), "seconds": round(time.time() - t0),
           "windows": got["day"], "stamp": IGB.stamp(REPO)}
    with open(os.path.join(root, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(man, f, indent=1)
    print("glassBake status=OK windows=%d seconds=%d dir=%s" % (len(got["day"]), man["seconds"], root))
    return 0


def selftest():
    passed = failed = 0

    def ok(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("glass_bake selftest FAIL " + name)
    a = args_for("night", r"F:\x\glass-bake")
    ok("a night bake asks for night", "-GlassBake=night" in a and "-PageShots=bake" in a)
    ok("the bake is played as the street is", all(x in a for x in ("-LedgerSlice", "-LedgerCrime", "-Encounter=live")))
    ok("the folder is given with forward slashes", "-GlassBakeDir=F:/x/glass-bake" in a)
    ok("both lights are baked", IGB.LIGHTS == ("day", "night"))
    src = open(os.path.join(REPO, "ue-probe", "Source", "LedgerProbe", "Private", "CrimeProbe.cpp"), encoding="utf-8").read()
    ok("the game knows the bake's switches", 'TEXT("GlassBake=")' in src and 'TEXT("GlassBakeDir=")' in src and 'Mode == TEXT("bake")' in src)
    print("glass_bake selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else bake())
