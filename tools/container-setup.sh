#!/usr/bin/env bash
# LEDGER container setup. Paste into the environment's setup script field so a
# fresh container starts able to run the project's own gate.
#
# WHY THIS FILE EXISTS, measured on 2026-09-10 and not guessed. On the first
# session after the move to `ledger`, `python3 ledger/verify.py` raised
# FileNotFoundError on its FIRST check and died:
#
#     File "ledger/verify.py", line 121, in shape
#       code, out = run(["dotnet", "run", "-c", "Release", ...
#     FileNotFoundError: [Errno 2] No such file or directory: 'dotnet'
#
# checksRun=0. Not one check executed, no footer was written, and so every
# commit made from that container was ungated. Five things were installed by
# hand to get from that to `checks=81ran/0skipped/81total` with exit 0. This
# script is those five things, in order, so nobody has to rediscover them.
#
# IT IS IDEMPOTENT. Every step checks before it acts and says which it did, so
# re-running costs seconds and changes nothing.
#
# IT NEVER FAILS THE WHOLE CONTAINER FOR ONE MISSING PIECE. Each step reports
# ok or FAILED and the summary at the end carries the count with its
# denominator. A container that comes up with four of five is worth having and
# worth knowing about; one that dies on step two is not.

set -uo pipefail          # deliberately NOT -e: see the paragraph above
export DEBIAN_FRONTEND=noninteractive
export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1

STEPS_OK=0
STEPS_RUN=0
FAILED=""

step() {                  # step <name> <command...>
  local name="$1"; shift
  STEPS_RUN=$((STEPS_RUN + 1))
  if "$@"; then
    STEPS_OK=$((STEPS_OK + 1))
    echo "setup: ${name}=ok"
  else
    FAILED="${FAILED} ${name}"
    echo "setup: ${name}=FAILED"
  fi
}

# ---------------------------------------------------------------- 1. dotnet
# ShapeCheck targets net8.0 (ledger/ShapeCheck/ShapeCheck.csproj), so the SDK
# must be 8. It is in Ubuntu noble's own archive, which is why this is apt and
# not the Microsoft feed: fewer moving parts and no extra key to trust.
# Without it these checks cannot run at all: shape, game_compiles, reach,
# core_tests. `tools/gamecheck.py` and `tools/reach-check.sh` shell out to
# dotnet themselves, one process boundary below verify.py, so a skip guard in
# verify.py alone does not save them.
install_dotnet() {
  if command -v dotnet >/dev/null 2>&1; then
    echo "  dotnet already present: $(dotnet --version 2>/dev/null)"
    return 0
  fi
  apt-get update -qq </dev/null >/dev/null 2>&1
  apt-get install -y -qq dotnet-sdk-8.0 </dev/null >/dev/null 2>&1
  command -v dotnet >/dev/null 2>&1 || return 1
  echo "  dotnet installed: $(dotnet --version 2>/dev/null)"
}

# ------------------------------------------------------------ 2. PowerShell
# Needed by `blender_hash_parse` (which otherwise exits 1 rather than skipping)
# and by `powershell_steps`, which parses the pwsh in the 18 workflows.
#
# DO NOT USE `dotnet tool install --global PowerShell`. verify.py's own skip
# message recommends exactly that and it FAILS on this image:
#     The settings file in the tool's NuGet package is invalid:
#     Settings file 'DotnetToolSettings.xml' was not found in the package.
# The official tarball works. That correction is the reason this comment is
# longer than the code under it.
PWSH_VERSION="${PWSH_VERSION:-7.4.6}"
install_pwsh() {
  if command -v pwsh >/dev/null 2>&1; then
    echo "  pwsh already present: $(pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>/dev/null)"
    return 0
  fi
  local url tmp
  url="https://github.com/PowerShell/PowerShell/releases/download/v${PWSH_VERSION}/powershell-${PWSH_VERSION}-linux-x64.tar.gz"
  tmp="$(mktemp -d)"
  curl -sSL -o "${tmp}/pwsh.tar.gz" "$url" || { rm -rf "$tmp"; return 1; }
  [ -s "${tmp}/pwsh.tar.gz" ] || { rm -rf "$tmp"; return 1; }
  mkdir -p /opt/pwsh
  tar -xzf "${tmp}/pwsh.tar.gz" -C /opt/pwsh || { rm -rf "$tmp"; return 1; }
  chmod +x /opt/pwsh/pwsh
  ln -sf /opt/pwsh/pwsh /usr/local/bin/pwsh
  rm -rf "$tmp"
  command -v pwsh >/dev/null 2>&1 || return 1
  echo "  pwsh installed: $(pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>/dev/null)"
}

# -------------------------------------------------- 3. the Python modules
# Three imports, three checks that fail without them, and they fail as a
# ModuleNotFoundError rather than as a skip:
#   PIL          ref_bench
#   numpy        decal_ink
#   onnxruntime  voice_live (tools/voice-live/time-the-shape.py)
# These are ordinary pip packages and need no pin today; add one here the first
# time a version breaks a check, with the failure quoted beside it.
install_pymods() {
  python3 -m pip install --quiet --disable-pip-version-check \
      pillow numpy onnxruntime >/dev/null 2>&1
  python3 - <<'PY' || return 1
import sys
# IMPORT EACH ONE FOR REAL rather than asking the loader whether it could.
# The first draft of this used importlib.util.find_spec without importing
# importlib.util, which raises AttributeError and reported every module
# missing on a container where all three were installed. Caught by running
# this script on the accepting case; a find_spec that answers yes also does
# not prove the module actually loads.
need = ("PIL", "numpy", "onnxruntime")
missing = []
for m in need:
    try:
        __import__(m)
    except Exception:
        missing.append(m)
print("  modules present=%d/%d%s" % (
    len(need) - len(missing), len(need),
    (" missing=" + ",".join(missing)) if missing else ""))
sys.exit(1 if missing else 0)
PY
}

# ------------------------------------------------------- 4. the full clone
# THE CONTAINER CLONES SHALLOW, 60 commits deep, and two things need the whole
# history. `runs_map_to_commits` compares 362 run files against the commits it
# can see and reads 362-against-60 as a fault. And dating anything is
# impossible: the gate hook's boundary bug could not be dated at all until the
# clone was deepened, at which point it resolved immediately to its first
# commit, cd30c19a on 24 August, seventeen days open.
# This costs bandwidth once and is skipped when the clone is already complete.
unshallow_clone() {
  if [ ! -d .git ]; then
    echo "  not a git checkout, nothing to deepen"
    return 0
  fi
  if [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" != "true" ]; then
    echo "  clone already complete: $(git rev-list --count HEAD 2>/dev/null) commit(s)"
    return 0
  fi
  git fetch --unshallow origin >/dev/null 2>&1 || return 1
  echo "  clone deepened to $(git rev-list --count HEAD 2>/dev/null) commit(s)"
}

# --------------------------------------------------------------- 5. on PATH
# `dotnet tool install --global` puts things in ~/.dotnet/tools, which is not
# on PATH by default. Nothing here needs it today, since the PowerShell tool
# install is the one that failed, but a later tool will and the omission is
# silent when it happens.
add_dotnet_tools_path() {
  local line='export PATH="$PATH:/root/.dotnet/tools"'
  grep -qF "/root/.dotnet/tools" /root/.bashrc 2>/dev/null || echo "$line" >> /root/.bashrc
  echo "  ~/.dotnet/tools on PATH in /root/.bashrc"
}

echo "=== LEDGER container setup ==="
step dotnet       install_dotnet
step pwsh         install_pwsh
step pymods       install_pymods
step fullclone    unshallow_clone
step dotnettools  add_dotnet_tools_path

# --------------------------------------------------------------- the verdict
# ONE LINE, key=value, no spaces inside a value, per .claude/rules/instruments.md.
# The count ships its denominator so "5 ok" can never be read without knowing
# how many were attempted.
echo
echo "setup done: stepsOk=${STEPS_OK}/${STEPS_RUN}${FAILED:+ failed=$(echo "$FAILED" | tr ' ' ',' | sed 's/^,//')}"

# WHAT THIS DOES NOT DO, said out loud rather than left to be discovered:
#   - It does not run `python3 ledger/verify.py`. The gate takes minutes and
#     belongs to the session, not to container start. Run it once by hand after
#     the first boot to confirm the tooling took.
#   - It does not install Blender or a GPU stack. `blender` is absent here and
#     the checks that want it already skip by name.
#   - It cannot make `voice_live` measure anything: that needs an exported
#     decode graph which only the PC's export job produces, so the check reports
#     nothing measured on any container and that is correct.
#
# TESTED ON BOTH OUTCOMES, ACCEPTING CASE FIRST, and the counts are pasted
# rather than described because the first draft of the module check FAILED A
# PASSING CASE and nobody would otherwise know whether the repaired one can
# still fail a failing one.
#
#   ACCEPTING, this container with all three modules installed:
#       modules present=3/3
#       setup: pymods=ok
#       setup done: stepsOk=5/5
#
#   REJECTING, the same script with one module name that exists nowhere
#   planted into the list:
#       modules present=3/4 missing=fnord_not_a_module
#       setup: pymods=FAILED
#       setup done: stepsOk=4/5 failed=pymods
#
# A check that cannot tell those apart is a ratchet.

# EXPECTED AFTER A CLEAN BOOT, and it is the thing to compare against:
#     python3 ledger/verify.py   ->  exit 0, checks=81ran/0skipped/81total
# If it reads fewer than 81 ran, a step above did not take; the setup line names
# which.
