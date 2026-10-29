#!/usr/bin/env python3
"""THE LOOK'S PICTURES THROUGH HIS CAMERA, IN THE PACKAGED GAME, REPEATABLY (his order D11, the look).

    python tools/office_look.py OUT_DIR [--editor] [--here] [--night] [--calibrate] [--buffers] [--no-people] [--no-others]
        [--x 6.2 --z 6.3 --yaw 30 --pitch -12] [--res 1920x1080] [--game-arg -Switch ...] [--exec "r.ForceLOD 0"]
    python tools/office_look.py --selftest

WHY. The office's marks, the calibration chart and the street's surfaces are all photographed by the game's own
-OfficeLook switches (CrimeProbe.cpp OfficeLookTick: Tom placed, two pictures through his camera, then with
-OfficeLookBuffers the base-colour and roughness views), but until 29 October each run was started by hand and its
command line was kept nowhere (F:/LedgerTools/gate/new/calibration/2026-10-28/day.out has none). This starts the
played copy with the same base switches as tools/p1-packaged.ps1, waits for it to close itself, and keeps beside the
pictures the command line, the game's log and the lines the look is judged by: the camera, the day's condition with
the exposure bias in force (VignetteShot.cpp ApplyPlayCondition), the office's own exposure, the calibrator.

Nothing here runs while the build machine works or Unreal is open (the caller checks, as for every local game run);
the game's child process is ended with its launcher (taskkill /T), so none is left behind.
"""
import glob
import os
import shutil
import subprocess
import sys
import time

PLAYED = r"F:\LedgerTools\played-game\Windows"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# --editor (29 October: Unreal's buffer views are not in the packaged build, so base colour is read in the editor's own
# game run, at the played quality level, as tools/stain_check.py's pictures were)
EDITOR = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
UPROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")
EXE = os.path.join(PLAYED, "LedgerProbe.exe")
SAVED = os.path.join(PLAYED, "LedgerProbe", "Saved")
BASE = ["-LedgerSlice", "-LedgerCrime", "-Encounter=live", "-LiveFresh", "-TalkFake", "-NoTitle", "-windowed", "-ForceRes",
        "-nosplash", "-unattended", "-OfficeLook"]
FLAGS = {"--here": "-OfficeLookHere", "--night": "-OfficeLookNight", "--calibrate": "-OfficeLookCalibrate",
         "--buffers": "-OfficeLookBuffers", "--no-people": "-OfficeLookNoPeople", "--no-others": "-OfficeLookNoOthers"}
VALUES = {"--x": "OfficeLookX", "--z": "OfficeLookZ", "--yaw": "OfficeLookYaw", "--pitch": "OfficeLookPitch"}
KEEP = ("LedgerCamera:", "ledgerOfficeLook", "LedgerClock light", "LedgerOffice: its own exposure", "tonemapRead=")
NAMES = {1: "lit", 2: "lit-2", 3: "basecolor", 4: "roughness"}


def command(a):
    args = list(BASE)
    if "--editor" in a:
        # --exec "cmd,cmd" (29 October, the jacket's levels of detail: r.ForceLOD 0 beside the plain view) joins the
        # played quality level's own command in the one -ExecCmds Unreal reads
        extra = ("," + a[a.index("--exec") + 1]) if "--exec" in a else ""
        args = [UPROJECT, "-game"] + args + ['-ExecCmds="scalability 2%s"' % extra, "-LedgerRepo=" + REPO]
    for k, sw in FLAGS.items():
        if k in a:
            args.append(sw)
    for k, sw in VALUES.items():
        if k in a:
            args.append("-%s=%s" % (sw, a[a.index(k) + 1]))
    # the office is built (its room, lights and own exposure) only with -MickeysInside (CrimeProbe.cpp); 29 October's
    # first office views without it came out unlit, one black: every view placed by --x/--z gets it
    if "--here" not in a and "-MickeysInside" not in a:
        args.append("-MickeysInside")
    w, h = (a[a.index("--res") + 1] if "--res" in a else "1920x1080").split("x")
    args += ["-ResX=" + w, "-ResY=" + h]
    for i, x in enumerate(a):
        if x == "--game-arg":
            args.append(a[i + 1])
    return [EDITOR if "--editor" in a else EXE] + args


def run(out, a):
    os.makedirs(out, exist_ok=True)
    saved = os.path.join(REPO, "ue-probe", "Saved") if "--editor" in a else SAVED
    if "--editor" in a:
        # the editor's game reads the scene's pieces from the project folder's own copy (as tools/morning_pictures.py
        # refreshes it), not the repository's: on 29 October a stale copy left two editor runs at the old pin 2.000
        shutil.copyfile(os.path.join(REPO, "production", "specs", "vignette-pieces.json"),
                        os.path.join(REPO, "ue-probe", "vignette-pieces.json"))
    shots = os.path.join(saved, "OfficeLook")
    for p in glob.glob(os.path.join(shots, "*.png")):
        os.remove(p)
    cmd = command(a)
    # one command line, each piece quoted only where it holds a space and no quote of its own, so -ExecCmds="scalability 2"
    # reaches Unreal as Unreal writes it
    line = " ".join('"%s"' % x if " " in x and '"' not in x else x for x in cmd)
    open(os.path.join(out, "command.txt"), "w", encoding="utf-8").write(line + "\n")
    t0 = time.time()
    g = subprocess.Popen(line, stdout=open(os.path.join(out, "game.out"), "w"), stderr=subprocess.STDOUT)
    try:
        g.wait(timeout=600)
    except subprocess.TimeoutExpired:
        print("officeLook status=TIMEOUT after 600 s")
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(g.pid)], capture_output=True)
    # the child under Binaries outlives its launcher; only the played copy's, never the build machine's own runs
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    "Get-CimInstance Win32_Process -Filter \"Name='LedgerProbe.exe'\" | Where-Object { $_.ExecutablePath -like '%s*' } "
                    "| ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" % PLAYED], capture_output=True)
    night = "--night" in a
    got = []
    for p in sorted(glob.glob(os.path.join(shots, "look-*.png"))):
        n = int(os.path.splitext(p)[0].rsplit("-", 1)[1])
        dst = os.path.join(out, NAMES.get(n, "shot-%d" % n) + ".png")
        shutil.copyfile(p, dst)
        got.append(os.path.basename(dst))
    log = os.path.join(saved, "Logs", "LedgerProbe.log")
    lines = []
    if os.path.exists(log):
        shutil.copyfile(log, os.path.join(out, "LedgerProbe.log"))
        for line in open(log, encoding="utf-8", errors="replace"):
            if any(k in line for k in KEEP):
                lines.append(line.rstrip()[:900])
    open(os.path.join(out, "look-lines.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    for line in lines:
        print(line[:400])
    print("officeLook pictures=%s seconds=%d night=%d out=%s" % (",".join(got) or "NONE", time.time() - t0, night, out))
    return 0 if got else 1


def selftest():
    c = command(["--here", "--buffers", "--yaw", "180", "--res", "1280x720", "--game-arg", "-PlayBlackLift=0.01"])
    ok = [c[0] == EXE, "-OfficeLookHere" in c and "-OfficeLookBuffers" in c and "-OfficeLookNight" not in c,
          "-OfficeLookYaw=180" in c, "-ResX=1280" in c and "-ResY=720" in c, c[-1] == "-PlayBlackLift=0.01"]
    print("office_look selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else run(a[0], a[1:]))
