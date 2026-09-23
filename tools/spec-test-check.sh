#!/usr/bin/env bash
# The street's own files, checked on every push: ue-probe/tests/vignette-spec-test.cpp.
#
#   bash tools/spec-test-check.sh
#
# WHY IT EXISTS, 23 September. The test reads the files the game engine reads -
# the scene's pieces, the look, the people, the parked cars, the sounds and the
# slice's cast - with the engine's own readers (StreetMeshes.h, VignetteSpec.h),
# and FINDINGS.md said on 22 September that nothing ran it. A test nobody runs
# is a test that quietly stops describing the game. This compiles it with
# whichever compiler the machine has, as tools/port-golden-check.sh does, and
# runs it from the repository root.
#
# NO COMPILER IS EXIT 3 AND SAYS SO: a test that did not run must never read
# like one that passed.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TEST="ue-probe/tests/vignette-spec-test.cpp"
INC_PUBLIC="ue-probe/Source/LedgerProbe/Public"
INC_SHIM="ue-probe/tests/unreal-shim"
WORK="$(mktemp -d 2>/dev/null || echo "$REPO/.spec-test-work")"
mkdir -p "$WORK"

build() {
  if command -v g++ >/dev/null 2>&1; then
    echo "specCompiler=g++" >&2
    ( cd "$REPO" && g++ -std=c++14 -O1 -w -I "$INC_PUBLIC" -I "$INC_SHIM" -o "$WORK/spec-test" "$TEST" ) >&2 || return 1
    echo "$WORK/spec-test"; return 0
  fi
  if command -v clang++ >/dev/null 2>&1; then
    echo "specCompiler=clang++" >&2
    ( cd "$REPO" && clang++ -std=c++14 -O1 -w -I "$INC_PUBLIC" -I "$INC_SHIM" -o "$WORK/spec-test" "$TEST" ) >&2 || return 1
    echo "$WORK/spec-test"; return 0
  fi
  local vcvars
  for vcvars in \
    "C:/Program Files/Microsoft Visual Studio/2022/BuildTools/VC/Auxiliary/Build/vcvars64.bat" \
    "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat" \
    "C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Auxiliary/Build/vcvars64.bat" \
    "C:/Program Files (x86)/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat"
  do
    [ -f "$vcvars" ] || continue
    echo "specCompiler=msvc" >&2
    local w; w="$(cd "$WORK" && pwd -W 2>/dev/null || echo "$WORK")"
    {
      echo "@echo off"
      echo "call \"$(echo "$vcvars" | tr '/' '\\')\" >nul 2>&1 || exit /b 90"
      echo "cd /d \"$(cd "$REPO" && pwd -W 2>/dev/null || echo "$REPO")\""
      echo "cl /nologo /EHsc /std:c++14 /w /I \"$(echo "$INC_PUBLIC" | tr '/' '\\')\" /I \"$(echo "$INC_SHIM" | tr '/' '\\')\" /Fe:\"$w\\spec-test.exe\" /Fo:\"$w\\\\\" \"$(echo "$TEST" | tr '/' '\\')\""
      echo "exit /b %errorlevel%"
    } > "$WORK/build.bat"
    ( cd "$WORK" && cmd //c "$w\\build.bat" ) >&2 || return 1
    echo "$WORK/spec-test.exe"; return 0
  done
  echo "NOTHING MEASURED - no C++ compiler. Looked for: g++, clang++, MSVC 2022 vcvars64." >&2
  return 3
}

EXE="$(build)"; rc=$?
if [ $rc -ne 0 ]; then
  [ $rc -eq 3 ] && exit 3
  echo "spec-test: the test did not compile" >&2
  exit 1
fi
( cd "$REPO" && "$EXE" ) > "$WORK/out.txt" 2>&1; rc=$?
grep -E "^  FAILED|^PASS:|^FAIL:" "$WORK/out.txt" | tail -20

exit $rc
