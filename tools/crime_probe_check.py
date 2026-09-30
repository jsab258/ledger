#!/usr/bin/env python3
"""THE CRIME PROBE'S OWN SELF-TEST, BUILT AND RUN (30 September).

    python tools/crime_probe_check.py      # exit 0 when LedgerCrime::Selftest passes

WHY: ue-probe/tests/crime-probe-test.cpp runs LedgerCrime::Selftest() (the
decision path of the crime, its witnesses and the deed's stories, engine-free)
against the real witness line bank, but the script that ran it
(ledger/verify.py) is gone, so it ran only inside the game. The independent
review of 30 September found faults in exactly this path (A1, A3, A4); its
design tests go into that self-test, and this runs them in the checks, with
whatever C++ compiler the machine has (g++ or clang++, or MSVC 2022 on
Jafar's PC), as tools/route_week_check.py does.

NOTHING MEASURED is exit 3 (no compiler), never a pass.
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST = os.path.join(REPO, "ue-probe", "tests", "crime-probe-test.cpp")
SRC = os.path.join(REPO, "ue-probe", "Source", "LedgerProbe", "Private", "Perception.cpp")
INC = os.path.join(REPO, "ue-probe", "Source", "LedgerProbe", "Public")
SHIM = os.path.join(REPO, "ue-probe", "tests", "unreal-shim")
BANK = os.path.join(REPO, "content", "dialogue", "crime-witness-v1.json")
VCVARS = [r"C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
          r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
          r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
          r"C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"]


def build(work):
    exe = os.path.join(work, "crime-probe-test" + (".exe" if os.name == "nt" else ""))
    for cxx in ("g++", "clang++"):
        if shutil.which(cxx):
            p = subprocess.run([cxx, "-std=c++14", "-O1", "-Werror=shadow=local", "-I", INC, "-I", SHIM, "-o", exe, TEST, SRC], capture_output=True, text=True)
            return (exe, None) if p.returncode == 0 else (None, cxx + " failed:\n" + p.stderr[-2000:])
    for vc in VCVARS:
        if os.path.isfile(vc):
            bat = os.path.join(work, "build.bat")
            with open(bat, "w") as fh:
                fh.write('@echo off\ncall "%s" >nul 2>&1 || exit /b 90\ncd /d "%s"\n' % (vc, work))
                # Unreal treats a name hiding another as an error (C4456 to C4459); so does this.
                fh.write('cl /nologo /EHsc /std:c++14 /W4 /we4456 /we4457 /we4458 /we4459 /I "%s" /I "%s" /Fe:"%s" "%s" "%s" >"%s" 2>&1\nexit /b %%errorlevel%%\n' % (INC, SHIM, exe, TEST, SRC, os.path.join(work, "cl.txt")))
            p = subprocess.run(["cmd", "/c", bat], capture_output=True, text=True)
            if p.returncode == 0:
                return exe, None
            out = open(os.path.join(work, "cl.txt"), encoding="utf-8", errors="replace").read() if os.path.isfile(os.path.join(work, "cl.txt")) else p.stdout + p.stderr
            errs = [l for l in out.splitlines() if " error " in l or "error C" in l]
            return None, "msvc failed:\n" + "\n".join(errs[:20] or out.splitlines()[-30:])
    return None, "no C++ compiler (g++, clang++, MSVC 2022)"


def main():
    work = tempfile.mkdtemp(prefix="crime-probe-")
    try:
        exe, why = build(work)
        if exe is None:
            print(why)
            print("crime-probe: NOTHING MEASURED (%s)" % why.splitlines()[0])
            return 3 if why.startswith("no C++") else 1
        p = subprocess.run([exe, BANK], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    out = p.stdout + p.stderr
    fails = [l for l in out.splitlines() if "FAIL" in l]
    for l in fails[:40]:
        print(l)
    last = [l for l in out.splitlines() if l.strip()][-3:]
    for l in last:
        print(l)
    print("crime-probe: exit %d, %d failing line(s)" % (p.returncode, len(fails)))
    return 0 if p.returncode == 0 and not fails else 1


if __name__ == "__main__":
    sys.exit(main())
