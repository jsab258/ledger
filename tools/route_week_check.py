#!/usr/bin/env python3
"""THE ROUTE'S ACCEPTANCE: the game's week, driven as the Core's, gives the Core's rows.

    python tools/route_week_check.py            # exit 0 when the sixteen rows and the stops agree
    python tools/route_week_check.py --selftest

WHY, 30 September (Jafar's list after the audit, item 1; the town's half of
the route, production/handovers/ROUTE.md, section 4: "the route played the
same way must give the same rows"). The Core's own week is
`TownReach --week-waits` (ledger/TownReach/Program.cs, WeekRows); the game's
hour is TownWeek.h, driven by ue-probe/tests/route-week-test.cpp with the
Core's stand-ins for what the player does. This runs the one, builds and runs
the other with whatever C++ compiler the machine has (g++ or clang++, or MSVC
2022 on Jafar's PC, as tools/port-golden-check.sh finds them), and compares
the sixteen rows and the first row's stops line for line.

NOTHING MEASURED is exit 3 (no .NET or no compiler), never a pass.
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAST = os.path.join(REPO, "production", "specs", "hook-cast.json")
TEST = os.path.join(REPO, "ue-probe", "tests", "route-week-test.cpp")
SRC = os.path.join(REPO, "ue-probe", "Source", "LedgerProbe", "Private", "Perception.cpp")
INC = os.path.join(REPO, "ue-probe", "Source", "LedgerProbe", "Public")
SHIM = os.path.join(REPO, "ue-probe", "tests", "unreal-shim")
VCVARS = [r"C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
          r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
          r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
          r"C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"]


def parse(text):
    """The rows after "with walks 30, 120, 30" and the stops after "the stops, first row"."""
    lines = text.splitlines()
    rows, stops = [], []
    i = next((k for k, l in enumerate(lines) if l.startswith("with walks 30, 120, 30")), None)
    if i is not None:
        for l in lines[i + 1:]:
            if l.startswith("| the envelope") or l.startswith("|---"):
                continue
            if l.startswith("| "):
                rows.append(l.strip())
            elif rows:
                break
    j = next((k for k, l in enumerate(lines) if l.startswith("the stops, first row")), None)
    if j is not None:
        for l in lines[j + 1:]:
            if l.startswith("  day "):
                stops.append(l.strip())
            elif stops:
                break
    return rows, stops


def core_rows():
    dotnet = shutil.which("dotnet") or os.path.expanduser("~/.dotnet/dotnet")
    if not dotnet or not (shutil.which("dotnet") or os.path.exists(dotnet)):
        return None, "no .NET"
    p = subprocess.run([dotnet, "run", "--project", os.path.join(REPO, "ledger", "TownReach"), "-c", "Release", "--",
                        "--cast", CAST, "--week-waits"], capture_output=True, text=True, encoding="utf-8", cwd=REPO)
    if p.returncode != 0:
        return None, "TownReach failed: " + (p.stderr or p.stdout)[-400:]
    return parse(p.stdout), None


def build(work):
    exe = os.path.join(work, "route-week-test" + (".exe" if os.name == "nt" else ""))
    for cxx in ("g++", "clang++"):
        if shutil.which(cxx):
            p = subprocess.run([cxx, "-std=c++14", "-O1", "-w", "-I", INC, "-I", SHIM, "-o", exe, TEST, SRC], capture_output=True, text=True)
            return (exe, None) if p.returncode == 0 else (None, cxx + " failed:\n" + p.stderr[-2000:])
    for vc in VCVARS:
        if os.path.isfile(vc):
            bat = os.path.join(work, "build.bat")
            with open(bat, "w") as fh:
                fh.write('@echo off\ncall "%s" >nul 2>&1 || exit /b 90\ncd /d "%s"\n' % (vc, work))
                fh.write('cl /nologo /EHsc /std:c++14 /w /I "%s" /I "%s" /Fe:"%s" "%s" "%s"\nexit /b %%errorlevel%%\n' % (INC, SHIM, exe, TEST, SRC))
            p = subprocess.run(["cmd", "/c", bat], capture_output=True, text=True)
            return (exe, None) if p.returncode == 0 else (None, "msvc failed:\n" + (p.stdout + p.stderr)[-2000:])
    return None, "no C++ compiler (g++, clang++, MSVC 2022)"


def compare(core, port):
    (crows, cstops), (prows, pstops) = core, port
    bad = []
    if len(crows) != 16:
        bad.append("the Core gave %d rows, not 16" % len(crows))
    for k in range(max(len(crows), len(prows))):
        a = crows[k] if k < len(crows) else "(none)"
        b = prows[k] if k < len(prows) else "(none)"
        if a != b:
            bad.append("row %d\n  core: %s\n  game: %s" % (k + 1, a, b))
    for k in range(max(len(cstops), len(pstops))):
        a = cstops[k] if k < len(cstops) else "(none)"
        b = pstops[k] if k < len(pstops) else "(none)"
        if a != b:
            bad.append("stop %d\n  core: %s\n  game: %s" % (k + 1, a, b))
    return bad


def selftest():
    sample = ("with walks 30, 120, 30:\n| the envelope | x |\n|---|---|\n| takes it | a |\n| tells Ron no | b |\n"
              "the stops, first row (takes the envelope, sits with Ada, Sheila sees the window):\n  day 2 20:00 ron: \"x\"\n")
    rows, stops = parse(sample)
    ok = rows == ["| takes it | a |", "| tells Ron no | b |"] and stops == ['day 2 20:00 ron: "x"']
    bad = compare((rows * 8, stops), (rows * 8, stops))
    bad2 = compare((rows * 8, stops), (rows * 8, []))
    passed = sum([ok, bad == [], len(bad2) == 1])
    print("route_week_check selftest: passed=%d/3 failed=%d" % (passed, 3 - passed))
    return 0 if passed == 3 else 1


def main():
    core, why = core_rows()
    if core is None:
        print("route-week: NOTHING MEASURED (%s)" % why)
        return 3
    work = tempfile.mkdtemp(prefix="route-week-")
    try:
        exe, why = build(work)
        if exe is None:
            print("route-week: NOTHING MEASURED (%s)" % why)
            return 3
        p = subprocess.run([exe, CAST], capture_output=True, text=True, encoding="utf-8")
        if p.returncode != 0:
            print("route-week: the game's week failed to run: " + p.stderr[-800:])
            return 1
        port = parse(p.stdout)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    bad = compare(core, port)
    for b in bad:
        print(b)
    print("route-week: %d rows and %d stops; %s" % (len(core[0]), len(core[1]),
          "the game's week gives the Core's" if not bad else "%d difference(s)" % len(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
