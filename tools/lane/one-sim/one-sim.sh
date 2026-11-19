#!/usr/bin/env bash
# ONE SIMULATION IN THE BROWSER: build and test (first slice, 19 November 2026).
#
#   tools/lane/one-sim/one-sim.sh setup       fetch the two toolchains (once, about 320 MB down, 1.2 GB unpacked)
#   tools/lane/one-sim/one-sim.sh reference   the REAL C# Core: build it, write its golden table, run its own tests
#   tools/lane/one-sim/one-sim.sh wasm        the game's C++ port, compiled for the browser
#   tools/lane/one-sim/one-sim.sh test        the browser copy against the reference, under Node
#   tools/lane/one-sim/one-sim.sh browser     the same checks inside a real web page (headless Chromium)
#   tools/lane/one-sim/one-sim.sh selftest    the checks themselves: a wrong table must fail them
#   tools/lane/one-sim/one-sim.sh breaks      seven planted one-line breaks: does the whole table, or the front door, see them?
#   tools/lane/one-sim/one-sim.sh differences the prototype's own JavaScript town against the real rules, measured (DIFFERENCES.md)
#   tools/lane/one-sim/one-sim.sh all         reference, wasm, test, selftest, browser, and Node against the browser
#
# NOTHING IS WRITTEN UNDER ledger/ OR ue-probe/. Their files are compiled from where they
# live, never copied; every toolchain and build output goes to $ONE_SIM_WORK (default
# /home/claude/one-sim-work), outside the repository. The C# programs look upward from
# their own folder for the repository's data files, so they are run under
# $ONE_SIM_WORK/root, whose entries are links to a READ-ONLY view of the repository
# (a read-only bind mount): they can read everything and can write nothing there.
#
# Exit codes: 0 all good; 1 a check failed; 2 usage; 3 NOTHING MEASURED (a toolchain or
# an input is missing: a check that did not run must never read like one that passed).
set -u

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
export ONE_SIM_WORK=${ONE_SIM_WORK:-/home/claude/one-sim-work}
W=$ONE_SIM_WORK
NICE="nice -n 15"

# The toolchains, pinned by name and checksum (read 19 November 2026). The one Python module
# setup needs is pinned the same way, in reference/zstd-requirements.txt.
CONDA=https://conda.anaconda.org/conda-forge/linux-64
DOTNET_RUNTIME=dotnet-runtime-8.0.34-h7148c6a_0.conda
DOTNET_RUNTIME_SHA=3224423dff5be5d33ed20fd21a346f766e58be69696bbdbae041bbb0babf3c87
DOTNET_SDK=dotnet-sdk-8.0.428-h7148c6a_0.conda
DOTNET_SDK_SHA=080f68706a39f0c899a02a604bef1aded42feb8d1b7d609bfbbdfaee42167074
WASI_SDK=wasi-sdk-34.0-x86_64-linux.tar.gz
WASI_SDK_URL=https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-34/$WASI_SDK
WASI_SDK_SHA=b761e3a0721dbae9c09a0059e5fdb2bf917d1b4a8a7b430fb3b5aafb0984b2c4

export DOTNET_ROOT=$W/dotnet8/lib/dotnet DOTNET_CLI_HOME=$W/dotnet-home
export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1 DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
DOTNET=$DOTNET_ROOT/dotnet
CXX=$W/wasi-sdk/bin/wasm32-wasip1-clang++
STRIP=$W/wasi-sdk/bin/llvm-strip
PORT_PUBLIC=ue-probe/Source/LedgerProbe/Public
PORT_SHIM=ue-probe/tests/unreal-shim
PORT_CPP=ue-probe/Source/LedgerProbe/Private/Perception.cpp
TABLE=$W/golden-fresh.txt

say() { printf '%s\n' "$*"; }
need() { # file  what  how
  [ -e "$1" ] && return 0
  say "NOTHING MEASURED: $2 is missing ($1). Run: tools/lane/one-sim/one-sim.sh $3"
  exit 3
}

# ---------------------------------------------------------------- setup
fetch() { # url  dest  sha256
  if [ -f "$2" ] && [ "$(sha256sum "$2" | cut -d' ' -f1)" = "$3" ]; then return 0; fi
  mkdir -p "$(dirname "$2")"
  $NICE curl -sS -L -m 1800 -o "$2" "$1" || { say "download failed: $1"; return 1; }
  [ "$(sha256sum "$2" | cut -d' ' -f1)" = "$3" ] || { say "checksum mismatch: $2"; return 1; }
}

setup() {
  mkdir -p "$W/dl" "$W/logs" "$DOTNET_CLI_HOME"
  if [ ! -x "$DOTNET" ]; then
    fetch "$CONDA/$DOTNET_RUNTIME" "$W/dl/$DOTNET_RUNTIME" "$DOTNET_RUNTIME_SHA" || return 3
    fetch "$CONDA/$DOTNET_SDK" "$W/dl/$DOTNET_SDK" "$DOTNET_SDK_SHA" || return 3
    # A .conda file is a zip holding a zstd tar; Python's zstandard (from PyPI) opens it.
    # Pinned like the toolchains: one exact file, by version and checksum (reference/zstd-requirements.txt).
    [ -d "$W/pylib/zstandard" ] || $NICE python3 -m pip install --quiet --target "$W/pylib" --no-deps --only-binary=:all: \
        --require-hashes -r "$HERE/reference/zstd-requirements.txt" \
      || { say "setup: the pinned zstandard wheel could not be installed (another Python version needs its own line in reference/zstd-requirements.txt)"; return 3; }
    $NICE python3 -I "$HERE/reference/conda_unpack.py" "$W/pylib" "$W/dotnet8" "$W/dl/$DOTNET_RUNTIME" "$W/dl/$DOTNET_SDK" || return 3
  fi
  if [ ! -x "$CXX" ]; then
    fetch "$WASI_SDK_URL" "$W/dl/$WASI_SDK" "$WASI_SDK_SHA" || return 3
    mkdir -p "$W/wasi-sdk" && $NICE tar -xzf "$W/dl/$WASI_SDK" -C "$W/wasi-sdk" --strip-components=1 || return 3
  fi
  say "setup: .NET SDK $($DOTNET --version 2>/dev/null) and wasi-sdk $(head -n 1 "$W/wasi-sdk/VERSION" 2>/dev/null) are in $W"
}

# A read-only view of the repository, and a folder of links into it, for the C# programs.
view() {
  mkdir -p "$W/ro-repo" "$W/root"
  if ! mountpoint -q "$W/ro-repo"; then
    mount --bind "$REPO" "$W/ro-repo" 2>/dev/null && mount -o remount,ro,bind "$W/ro-repo" 2>/dev/null
  fi
  if ! mountpoint -q "$W/ro-repo" || touch "$W/ro-repo/.one-sim-probe" 2>/dev/null; then
    rm -f "$W/ro-repo/.one-sim-probe" 2>/dev/null
    unview
    say "NOTHING MEASURED: no read-only view of the repository could be made (needs mount rights)."
    say "The C# programs are not run against a writable repository."
    return 3
  fi
  local e
  for e in "$W/ro-repo"/*; do ln -sfn "$e" "$W/root/$(basename "$e")"; done
}
# The view is taken down after every use, so nothing of the repository stays mounted
# under the work folder (deleting the work folder must never be able to reach the repository).
unview() { mountpoint -q "$W/ro-repo" && umount "$W/ro-repo" 2>/dev/null; return 0; }

# ---------------------------------------------------------------- reference
reference() {
  need "$DOTNET" "the .NET SDK" setup
  mkdir -p "$W/logs"
  view || return $?
  reference_run
  local rc=$?
  unview
  return $rc
}
# The lane's project files must list exactly the sources the originals list. MSBuild itself is
# asked for both lists (nothing is built, nothing is written; the originals are read through the
# read-only view), and reference/compare_sources.py compares them.
sources_match() {
  local p rc=0 s
  for p in PerceptionGolden Soak CoreTests; do
    ( cd "$HERE/reference" && $NICE "$DOTNET" msbuild "$p.csproj" -nologo -getItem:Compile ) > "$W/logs/sources-lane-$p.json" 2> "$W/logs/sources-lane-$p.err"
    ( cd "$W/ro-repo/ledger/$p" && $NICE "$DOTNET" msbuild "$W/ro-repo/ledger/$p/$p.csproj" -nologo -getItem:Compile ) > "$W/logs/sources-original-$p.json" 2> "$W/logs/sources-original-$p.err"
    python3 -I "$HERE/reference/compare_sources.py" "$p" "$W/logs/sources-lane-$p.json" "$REPO/" "$W/logs/sources-original-$p.json" "$W/ro-repo/"
    s=$?
    case $s in 0) ;; 1) rc=1 ;; *) [ $rc -eq 1 ] || rc=$s ;; esac
  done
  return $rc
}

reference_run() {
  local p rc=0
  sources_match || return $?
  for p in PerceptionGolden Soak CoreTests; do
    ( cd "$HERE/reference" && $NICE "$DOTNET" build "$p.csproj" -c Release -v q ) > "$W/logs/build-$p.log" 2>&1 \
      || { say "reference: $p did not build (see $W/logs/build-$p.log)"; tail -n 5 "$W/logs/build-$p.log"; return 1; }
  done
  say "reference: PerceptionGolden, Soak and CoreTests built from the real Core (ledger/Assets/Scripts/Core, $(ls "$REPO"/ledger/Assets/Scripts/Core/*.cs | wc -l) files), .NET SDK $($DOTNET --version)"
  local bin=$W/root/artifacts/bin

  ( cd "$W/root" && $NICE "$DOTNET" "$bin/PerceptionGolden/release/PerceptionGolden.dll" "$TABLE" ) > "$W/logs/run-golden.log" 2>&1
  if [ $? -ne 0 ] || [ ! -s "$TABLE" ]; then say "NOTHING MEASURED: the Core wrote no golden table"; tail -n 5 "$W/logs/run-golden.log"; return 3; fi
  cat "$REPO"/ue-probe/perception-golden/part-*.txt | tr -d '\r' > "$W/golden-committed.norm.txt"
  tr -d '\r' < "$TABLE" > "$W/golden-fresh.norm.txt"
  local rows rules
  rows=$(grep -cv '^#' "$W/golden-fresh.norm.txt"); rules=$(grep -v '^#' "$W/golden-fresh.norm.txt" | cut -d'|' -f1 | sort -u | wc -l)
  if cmp -s "$W/golden-committed.norm.txt" "$W/golden-fresh.norm.txt"; then
    say "ok   C# goldens: the table the Core writes today ($rows rows, $rules rules) is the committed table (ue-probe/perception-golden), byte for byte"
  else
    say "FAIL C# goldens: the Core's table today ($rows rows) differs from the committed parts; tools/port-golden-check.sh names the rows"; rc=1
  fi

  ( cd "$W/root" && $NICE "$DOTNET" "$bin/Soak/release/Soak.dll" ) > "$W/logs/run-soak.log" 2>&1
  if [ $? -eq 0 ]; then say "ok   Soak: $(grep -m1 '^soak ok' "$W/logs/run-soak.log")"; else say "FAIL Soak (see $W/logs/run-soak.log)"; rc=1; fi

  ( cd "$W/root" && $NICE timeout 900 "$DOTNET" "$bin/CoreTests/release/CoreTests.dll" ) > "$W/logs/run-coretests.log" 2>&1
  if [ $? -eq 0 ]; then say "ok   CoreTests: $(grep -m1 '^All .* checks passed' "$W/logs/run-coretests.log")"
  else say "FAIL CoreTests: $(grep -m3 '^FAILED\|^  FAIL\|not ok' "$W/logs/run-coretests.log" | tr '\n' ' ') (see $W/logs/run-coretests.log)"; rc=1; fi
  return $rc
}

# ---------------------------------------------------------------- wasm
# The flags. -fno-exceptions and LEDGER_CORE_NO_EXCEPTIONS=1 are the game's own (LedgerProbe.Build.cs).
# C++17, not the port test's C++14: the port names a constant inside a class (AdasTea::Ada) in a
# way C++14 needs a second line for; g++ lets it pass, clang does not link it. Noted in
# PROGRESS.md as a finding for the port's owner.
wasm() {
  need "$CXX" "wasi-sdk" setup
  mkdir -p "$W/wasm" "$W/logs"
  local common="-std=c++17 -O2 -w -I $PORT_PUBLIC -I $PORT_SHIM"
  local game="-fno-exceptions -DLEDGER_CORE_NO_EXCEPTIONS=1"
  build() { # name  log  flags...
    local name=$1; shift
    ( cd "$REPO" && $NICE "$CXX" "$@" ) > "$W/logs/wasm-$name.log" 2>&1 \
      || { say "wasm: $name did not build (see $W/logs/wasm-$name.log)"; tail -n 6 "$W/logs/wasm-$name.log"; return 1; }
  }
  # The brain a page loads, and the same plus the port's golden reader (the proof, never shipped).
  build brain $common $game -mexec-model=reactor -o "$W/wasm/one-sim.full.wasm" "$HERE/wasm/one_sim.cpp" $PORT_CPP || return 1
  build check $common $game -mexec-model=reactor -DONE_SIM_CHECK=1 -o "$W/wasm/one-sim-check.full.wasm" "$HERE/wasm/one_sim.cpp" $PORT_CPP || return 1
  "$STRIP" -o "$W/wasm/one-sim.wasm" "$W/wasm/one-sim.full.wasm" && "$STRIP" -o "$W/wasm/one-sim-check.wasm" "$W/wasm/one-sim-check.full.wasm" || return 1
  # The port's own golden test (ue-probe/tests/core-port-test.cpp), unchanged, as a WebAssembly
  # program: once with the game's flags, once with exceptions on (which answers four more rows).
  build port-test $common $game -o "$W/wasm/core-port-test.wasm" ue-probe/tests/core-port-test.cpp $PORT_CPP || return 1
  build port-test-eh $common -fwasm-exceptions -o "$W/wasm/core-port-test.eh.wasm" ue-probe/tests/core-port-test.cpp $PORT_CPP -lunwind || return 1
  say "wasm: built with wasi-sdk $(head -n 1 "$W/wasi-sdk/VERSION"): one-sim.wasm $(stat -c %s "$W/wasm/one-sim.wasm") bytes, one-sim-check.wasm $(stat -c %s "$W/wasm/one-sim-check.wasm") bytes, and the port's own test twice"
}

# ---------------------------------------------------------------- tests
port_test() { # wasm  label
  ( cd "$W" && $NICE node --no-warnings "$HERE/wasm/run_wasi.mjs" "$1" --quiet --dir "/data=$W/data" --dir "production/specs=$REPO/production/specs" -- /data/golden.txt ) > "$W/logs/$2.out" 2>&1
  local rc=$?
  if [ $rc -eq 0 ]; then say "ok   $2: $(tail -n 1 "$W/logs/$2.out")"; else say "FAIL $2 (exit $rc): $(tail -n 1 "$W/logs/$2.out")"; fi
  return $rc
}

# The table every check reads is the one `reference` last wrote into the work folder. It must
# still be the committed table: if the committed one has moved on since (or the Core and the
# committed table disagree), a check run against the old copy would pass against the wrong thing.
table_current() {
  need "$TABLE" "the golden table from the C# Core" reference
  if ! cmp -s <(cat "$REPO"/ue-probe/perception-golden/part-*.txt | tr -d '\r') <(tr -d '\r' < "$TABLE"); then
    say "NOTHING MEASURED: the C# table in the work folder is older than the committed one, or differs from it"
    say "($TABLE against ue-probe/perception-golden). Run: tools/lane/one-sim/one-sim.sh reference"
    return 3
  fi
}

test_() {
  table_current || return $?
  need "$W/wasm/one-sim.wasm" "the browser build" wasm
  command -v node >/dev/null 2>&1 || { say "NOTHING MEASURED: no node"; return 3; }
  mkdir -p "$W/data" && cp "$TABLE" "$W/data/golden.txt"
  rm -f "$W/logs/test-report.json"
  local rc=0
  port_test "$W/wasm/core-port-test.wasm" "port-test-as-wasm-game-flags" || rc=1
  port_test "$W/wasm/core-port-test.eh.wasm" "port-test-as-wasm-with-exceptions" || rc=1
  ( cd "$W" && $NICE node --no-warnings "$HERE/wasm/test_one_sim.mjs" --brain "$W/wasm/one-sim.wasm" --check "$W/wasm/one-sim-check.wasm" \
      --golden "$TABLE" --specs "$REPO/production/specs" --json "$W/logs/test-report.json" ) || rc=1
  return $rc
}

selftest() {
  table_current || return $?
  need "$W/wasm/one-sim.wasm" "the browser build" wasm
  local rc=0
  ( cd "$W" && $NICE node --no-warnings "$HERE/wasm/selftest.mjs" --brain "$W/wasm/one-sim.wasm" --check "$W/wasm/one-sim-check.wasm" \
      --golden "$TABLE" --specs "$REPO/production/specs" ) || rc=1
  python3 -I "$HERE/wasm/engines_agree.py" --selftest || rc=1
  python3 -I "$HERE/reference/compare_sources.py" --selftest "$W/selftest-sources" || rc=1
  return $rc
}

browser() {
  table_current || return $?
  need "$W/wasm/one-sim.wasm" "the browser build" wasm
  rm -f "$W/logs/browser-report.json"
  ( cd "$W" && $NICE python3 -I "$HERE/wasm/browser_test.py" --brain "$W/wasm/one-sim.wasm" --check "$W/wasm/one-sim-check.wasm" \
      --golden "$TABLE" --specs "$REPO/production/specs" --site "$W/browser-site" --json "$W/logs/browser-report.json" )
}

# Fix 1 of the review: the same town in Node and in the real browser. Both reports are deleted
# before their runs (above), so a report here is always from the run just made.
engines_agree() {
  python3 -I "$HERE/wasm/engines_agree.py" "$W/logs/test-report.json" "$W/logs/browser-report.json"
}

# A measurement, not a gate: each break is made in a copy under $W/breaks, never in the repository.
breaks() {
  table_current || return $?
  need "$CXX" "wasi-sdk" setup
  ( cd "$W" && $NICE python3 -I "$HERE/wasm/breaks.py" --repo "$REPO" --work "$W" --cxx "$CXX" --golden "$TABLE" --json "$W/logs/breaks.json" )
}

# A measurement, not a gate: the prototype's frozen rule files (read, never changed) beside the real town.
differences() {
  need "$W/wasm/one-sim.wasm" "the browser build" wasm
  command -v node >/dev/null 2>&1 || { say "NOTHING MEASURED: no node"; return 3; }
  mkdir -p "$W/logs"
  ( cd "$W" && $NICE node --no-warnings "$HERE/differences/measure.mjs" --brain "$W/wasm/one-sim.wasm" --specs "$REPO/production/specs" \
      --prototype "$REPO/tools/lane/prototype/project/src" --json "$W/logs/differences.json" )
}

case "${1:-}" in
  setup)     setup;     exit $? ;;
  breaks)    breaks;    exit $? ;;
  differences) differences; exit $? ;;
  reference) reference; exit $? ;;
  wasm)      wasm;      exit $? ;;
  test)      test_;     exit $? ;;
  selftest)  selftest;  exit $? ;;
  browser)   browser;   exit $? ;;
  all)
    rc=0
    # A failed check (1) outranks a check that could not run (3), which outranks good (0).
    fold() { case $1 in 0) ;; 3) [ $rc -eq 0 ] && rc=3 ;; *) rc=1 ;; esac; return 0; }
    reference || rc=$?
    [ $rc -le 1 ] && { wasm || rc=$?; }
    if [ $rc -le 1 ]; then
      test_; fold $?
      selftest; fold $?
      browser; fold $?
      engines_agree; fold $?
    fi
    [ $rc -eq 0 ] && say "one-sim: everything passed" || say "one-sim: NOT all passed (exit $rc)"
    exit $rc ;;
  *) say "usage: one-sim.sh setup|reference|wasm|test|selftest|browser|breaks|differences|all"; exit 2 ;;
esac
