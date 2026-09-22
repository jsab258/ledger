#!/usr/bin/env bash
# THE C++ PORT IS CHECKED AGAINST THE C# AS IT IS TODAY, NOT AS IT WAS COMMITTED.
#
# WHY THIS EXISTS, and it is a fault that was live when it was written. The
# port's agreement with the C# Core was measured against
# `ue-probe/perception-golden.txt`, a FILE IN THE REPOSITORY. Nothing
# regenerated it. On 2026-09-22 the committed table was seven rows short of
# what `ledger/PerceptionGolden` emits from the real Core: the `claims` rows,
# which pin that a caught claim is remembered and never learned. The reason
# they were missing is written into PerceptionGolden's own source — the port
# cannot answer them, and the port test fails on a row it cannot answer, so
# the rows were left out and the comparison went green by never being asked.
#
# A golden table nobody regenerates stops describing the game the moment the
# game moves, and nothing anywhere turns red. So: regenerate from the Core,
# say loudly when the committed copy has drifted, and run the comparison
# against the FRESH output.
#
# EXIT CODES, one per outcome:
#   0  the committed table matches the Core and the port agrees with it
#   1  drift, or the port disagreed
#   2  usage error
#   3  NOTHING MEASURED — the Core emitted no rows, or no compiler was found
#   4  --selftest found this script itself broken
#
#   tools/port-golden-check.sh             # the check
#   tools/port-golden-check.sh --accept    # regenerate in place and keep it
#   tools/port-golden-check.sh --selftest  # this script, both ways
set -u

REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
COMMITTED="$REPO/ue-probe/perception-golden.txt"
PORT_TEST="ue-probe/tests/core-port-test.cpp"
PORT_SRC="ue-probe/Source/LedgerProbe/Private/Perception.cpp"
INC_PUBLIC="ue-probe/Source/LedgerProbe/Public"
INC_SHIM="ue-probe/tests/unreal-shim"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/port-golden.XXXXXX")
cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

# ---------------------------------------------------------------- pieces

# THE C# CORE, ASKED NOW. Writes the table to $1 and prints the row count it
# emitted. A build failure or an empty table is exit 3, not a quiet zero: a
# comparison against nothing passes, which is the reading this whole file
# exists to prevent.
regenerate() {
  local dest="$1"
  ( cd "$REPO" && dotnet run --project ledger/PerceptionGolden -c Release -- "$dest" ) \
    > "$WORK/regen.log" 2>&1
  local rc=$?
  if [ $rc -ne 0 ] || [ ! -s "$dest" ]; then
    echo "NOTHING MEASURED — ledger/PerceptionGolden did not emit a table (exit $rc)."
    tail -n 20 "$WORK/regen.log"
    return 3
  fi
  return 0
}

rows_in() { grep -cv '^#' "$1" 2>/dev/null | tr -d ' '; }

# DRIFT, NAMED IN ROWS RATHER THAN AS A DIFF. Line endings are normalised
# first: the table is written by .NET on Windows and read by g++ on Linux,
# and a CRLF difference is not drift.
drift_check() {
  local committed="$1" fresh="$2"
  local a="$WORK/a.norm" b="$WORK/b.norm"
  tr -d '\r' < "$committed" > "$a" 2>/dev/null || : > "$a"
  tr -d '\r' < "$fresh"     > "$b"
  if cmp -s "$a" "$b"; then
    echo "goldenDrift=no committedRows=$(rows_in "$a") coreRows=$(rows_in "$b")"
    return 0
  fi
  local only_core only_committed
  only_core=$(comm -13 <(sort "$a") <(sort "$b") | wc -l | tr -d ' ')
  only_committed=$(comm -23 <(sort "$a") <(sort "$b") | wc -l | tr -d ' ')
  echo "goldenDrift=YES committedRows=$(rows_in "$a") coreRows=$(rows_in "$b")" \
       "rowsTheCoreEmitsThatTheTableLacks=$only_core" \
       "rowsTheTableCarriesThatTheCoreNoLongerEmits=$only_committed"
  echo "--- the first 10 rows the Core emits and the committed table does not ---"
  comm -13 <(sort "$a") <(sort "$b") | head -n 10
  echo "--- the first 10 rows the committed table carries and the Core does not ---"
  comm -23 <(sort "$a") <(sort "$b") | head -n 10
  echo "FIX: tools/port-golden-check.sh --accept, then commit the table."
  return 1
}

# THE COMPILER, WHICHEVER THIS MACHINE HAS. g++ on the Linux runner where the
# push checks live; MSVC on Jafar's PC, which is the toolchain Unreal itself
# builds the port with. NO COMPILER IS EXIT 3 AND SAYS WHICH ONES IT LOOKED
# FOR — a comparison that did not run must never read like one that agreed.
build_port() {
  local out="$WORK/core-port-test"
  if command -v g++ >/dev/null 2>&1; then
    echo "portCompiler=g++" >&2
    ( cd "$REPO" && g++ -std=c++11 -O1 -w -I "$INC_PUBLIC" -I "$INC_SHIM" \
        -o "$out" "$PORT_TEST" "$PORT_SRC" ) >&2 || return 1
    echo "$out"; return 0
  fi
  if command -v clang++ >/dev/null 2>&1; then
    echo "portCompiler=clang++" >&2
    ( cd "$REPO" && clang++ -std=c++11 -O1 -w -I "$INC_PUBLIC" -I "$INC_SHIM" \
        -o "$out" "$PORT_TEST" "$PORT_SRC" ) >&2 || return 1
    echo "$out"; return 0
  fi
  local vcvars
  for vcvars in \
    "C:/Program Files/Microsoft Visual Studio/2022/BuildTools/VC/Auxiliary/Build/vcvars64.bat" \
    "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat" \
    "C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Auxiliary/Build/vcvars64.bat" \
    "C:/Program Files (x86)/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat"
  do
    [ -f "$vcvars" ] || continue
    echo "portCompiler=msvc" >&2
    {
      echo "@echo off"
      echo "call \"$(echo "$vcvars" | tr '/' '\\')\" >nul 2>&1 || exit /b 90"
      echo "cd /d \"$(cd "$REPO" && pwd -W 2>/dev/null || echo "$REPO")\""
      echo "cl /nologo /EHsc /std:c++14 /w /I \"$(echo "$INC_PUBLIC" | tr '/' '\\')\" /I \"$(echo "$INC_SHIM" | tr '/' '\\')\" /Fe:\"$(cd "$WORK" && pwd -W 2>/dev/null || echo "$WORK")\\core-port-test.exe\" /Fo:\"$(cd "$WORK" && pwd -W 2>/dev/null || echo "$WORK")\\\\\" \"$(echo "$PORT_TEST" | tr '/' '\\')\" \"$(echo "$PORT_SRC" | tr '/' '\\')\""
      echo "exit /b %errorlevel%"
    } > "$WORK/build.bat"
    ( cd "$WORK" && cmd //c "$(cd "$WORK" && pwd -W 2>/dev/null || echo "$WORK")\\build.bat" ) >&2 || return 1
    echo "$out.exe"; return 0
  done
  echo "NOTHING MEASURED — no C++ compiler. Looked for: g++, clang++, MSVC 2022 vcvars64." >&2
  return 3
}

# ---------------------------------------------------------------- the check

check() {
  local fresh="$WORK/fresh.txt"
  echo "===== the C# Core, asked now"
  regenerate "$fresh" || return $?
  tail -n 1 "$WORK/regen.log"

  echo
  echo "===== the committed table against it"
  local drift=0
  drift_check "$COMMITTED" "$fresh" || drift=1

  echo
  echo "===== the C++ port against the FRESH table"
  local bin rc
  bin=$(build_port); rc=$?
  if [ $rc -ne 0 ]; then
    [ $rc -eq 3 ] && return 3
    echo "the port did not compile"
    return 1
  fi
  ( cd "$REPO" && "$bin" "$fresh" )
  local prc=$?

  echo
  if [ $drift -ne 0 ]; then
    echo "port-golden done: THE COMMITTED TABLE HAS DRIFTED from the C# Core."
    return 1
  fi
  if [ $prc -ne 0 ]; then
    echo "port-golden done: the port disagrees with the C# Core (exit $prc)."
    return 1
  fi
  echo "port-golden done: table matches the Core, and the port agrees with it."
  return 0
}

accept() {
  local fresh="$WORK/fresh.txt"
  regenerate "$fresh" || return $?
  tail -n 1 "$WORK/regen.log"
  if drift_check "$COMMITTED" "$fresh" > "$WORK/drift.txt" 2>&1; then
    cat "$WORK/drift.txt"
    echo "port-golden --accept: the committed table was already what the Core emits; nothing written."
    return 0
  fi
  cat "$WORK/drift.txt"
  cp "$fresh" "$COMMITTED"
  echo "port-golden --accept: ue-probe/perception-golden.txt rewritten from the C# Core. COMMIT IT."
  return 0
}

# ---------------------------------------------------------------- selftest

# THE ACCEPTING CASE IS FIRST. The expensive failure in this family is a check
# nothing survives, not one that lets something through.
selftest() {
  local pass=0 fail=0 bin rc out

  _ok() { # name  condition-already-evaluated-as-rc  expected-substring
    local what="$1" want_rc="$2" want_txt="$3"
    if [ "$rc" != "$want_rc" ]; then
      echo "  FAIL $what — exit $rc, wanted $want_rc"; fail=$((fail + 1)); return
    fi
    if [ -n "$want_txt" ] && ! printf '%s' "$out" | grep -qF -- "$want_txt"; then
      echo "  FAIL $what — output did not contain: $want_txt"; fail=$((fail + 1)); return
    fi
    echo "  ok   $what"; pass=$((pass + 1))
  }

  echo "port-golden selftest — this script, not the game"
  echo

  bin=$(build_port); rc=$?
  if [ $rc -eq 3 ]; then echo "  no compiler; nothing here can run"; return 3; fi
  if [ $rc -ne 0 ]; then echo "  FAIL the port did not compile"; return 4; fi

  local good="$WORK/good.txt"
  regenerate "$good" || return 4

  echo "[1] ACCEPTING CASE: the fresh table, straight from the Core"
  out=$( cd "$REPO" && "$bin" "$good" 2>&1 ); rc=$?
  _ok "the port agrees with the Core" 0 "0 failure(s)"

  echo
  echo "[2] A CORRUPTED EXPECTED VALUE MUST BE CAUGHT"
  sed 's/^MotionFactor|1|.*/MotionFactor|1|0.5/' "$good" > "$WORK/bad.txt"
  out=$( cd "$REPO" && "$bin" "$WORK/bad.txt" 2>&1 ); rc=$?
  _ok "a wrong row fails the comparison" 2 "MISMATCH"

  echo
  echo "[3] A MISSING TABLE IS NOT AN AGREEMENT"
  out=$( cd "$REPO" && "$bin" "$WORK/no-such-table.txt" 2>&1 ); rc=$?
  _ok "no table says nothing measured" 2 "nothing measured"

  echo
  echo "[4] A ROW NAMING SOMETHING THE PORT CANNOT ANSWER STILL FAILS"
  { cat "$good"; echo "Scenario|no_such_scenario|whatever|1"; } > "$WORK/unknown.txt"
  out=$( cd "$REPO" && "$bin" "$WORK/unknown.txt" 2>&1 ); rc=$?
  _ok "an unanswerable row is red" 2 "unanswered"

  echo
  echo "[5] AND THE NAMED HOLE IS SKIPPED, COUNTED, AND STILL GREEN"
  out=$( cd "$REPO" && "$bin" "$good" 2>&1 ); rc=$?
  _ok "the claims rows are skipped by name" 0 "SKIPPED scenario=claims"
  _ok "and the count is printed beside them" 0 "skippedTotal=7"

  echo
  echo "[6] DRIFT IS SEEN, IN BOTH DIRECTIONS"
  out=$(drift_check "$good" "$good" 2>&1); rc=$?
  _ok "identical tables report no drift" 0 "goldenDrift=no"
  head -n -1 "$good" > "$WORK/short.txt"
  out=$(drift_check "$WORK/short.txt" "$good" 2>&1); rc=$?
  _ok "a table missing a row the Core emits is drift" 1 "goldenDrift=YES"
  { cat "$good"; echo "MotionFactor|999|1"; } > "$WORK/long.txt"
  out=$(drift_check "$WORK/long.txt" "$good" 2>&1); rc=$?
  _ok "a table carrying a row the Core dropped is drift too" 1 "goldenDrift=YES"

  echo
  echo "port-golden selftest: passed=$pass/$((pass + fail)) failed=$fail"
  [ "$fail" -eq 0 ] && return 0
  return 4
}

# -------------------------------------------------------------------- main

case "${1:-}" in
  "")          check;    exit $? ;;
  --accept)    accept;   exit $? ;;
  --selftest)  selftest; exit $? ;;
  *) echo "usage: port-golden-check.sh [--accept|--selftest]" >&2; exit 2 ;;
esac
