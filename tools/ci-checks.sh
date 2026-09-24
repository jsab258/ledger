#!/usr/bin/env bash
# EVERY CHEAP CHECK RUNS, AND THE JOB FAILS AT THE END NAMING WHICH.
#
# WHY, and it is rule 3b wearing a workflow's clothes. Until 25 Aug the
# `LEDGER core tests` job was eight bare `run:` steps in a row. A red step at
# position 4 SKIPS every step below it, so four consecutive pushes — 80a9104,
# 6137608, cfd728a, b88adbb — ran the reach check, failed it, and never ran
# the docs check, either shape check, the attribution check, the 2,884
# CoreTests or the AI playtest. The job's one red said nothing about which of
# the eight it was, and six checks reporting NOTHING looked exactly like six
# checks reporting fine. The whole cheap feedback channel was dark and no
# output said so.
#
# The fix is not `continue-on-error` on its own — a step that fails without
# failing the job is a gate loosened, and rule 2 forbids moving a bound to
# make red go away. Every check runs, every outcome is recorded, and this
# script exits non-zero listing the failures BY NAME with the count of what
# was examined beside them.
#
# THE SUMMARY IS AT THE END ON PURPOSE. Rule 12: the only log channel this
# environment can read is a fixed ~4KB BYTE TAIL, so anything that has to be
# read must be the last thing printed. That is also why failed checks get
# their output re-printed down there rather than only where it happened.
#
# EXIT CODES, one per outcome:
#   0  every check passed
#   1  at least one check failed  (named on the done line)
#   2  usage error
#   3  NOTHING MEASURED — the table was empty; a clean run cannot look like this
#   4  --selftest found the harness itself broken
#
#   tools/ci-checks.sh              # the real table, on this repo
#   tools/ci-checks.sh --list       # what would run, and nothing else
#   tools/ci-checks.sh --selftest   # the harness, both ways, in a second
set -u

REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

# HOW MANY LINES OF A FAILED CHECK'S OUTPUT GET RE-PRINTED AT THE END.
#
# SET FROM A PRINTED SERIES, NOT CHOSEN. This script printed `outLines` per
# check before any bound existed here. Measured on this repository, 25 Aug:
#
#   green run      reach-check 10   attribution 23   attribution-selftest 61
#                  docs-check 91    playtest-fake 108   shape-check 156
#                  shape-check-selftest 452   core-tests 3877
#   failing run    reach-check 13 lines / 844 bytes
#                  docs-check  88 lines / 5393 bytes
#   density        42.2 to 83.4 bytes per line, median ~60
#
# 120 covers the WHOLE output of five of the eight, including both checks
# measured failing. It truncates shape-check (-36), shape-check-selftest
# (-332) and core-tests (-3757), and says so each time.
#
# THE TAIL IS THE RIGHT END FOR SEVEN OF THE EIGHT: CoreTests throws on the
# first failure and prints `FAILED: ...` as its LAST line, reach-check,
# shape-check, attribution and the playtest all summarise at the end.
# `docs-check` is the exception — it prints the offending document inline in
# alphabetical order and its last line is only `1 problem(s)` — which is why
# the cap is 120 rather than the ~68 lines that fit a 4KB log window, and why
# the full output is left printed where it happened as well.
TAIL_LINES=${CI_CHECKS_TAIL:-120}

LOGDIR=$(mktemp -d "${TMPDIR:-/tmp}/ci-checks.XXXXXX")
# FAIL READABLE. A correct run that ends in a stray temp directory or a
# BrokenPipeError costs twenty minutes before anybody notices it worked.
cleanup() { rm -rf "$LOGDIR"; }
trap cleanup EXIT
trap '' PIPE

# THREE CHECKS LEFT THIS TABLE ON 2026-09-22, when the studio was paused, and
# they left because their SUBJECTS were archived rather than because anyone
# decided they were wrong:
#
#   docs-check       read game-design/ and production/queue/ for the document
#                    law and the queue's three states. The queue is archived
#                    and the document law went with the old CLAUDE.md.
#   canon-register   read ledger-v2/respec/decision-register/, now archived.
#                    Canon itself is still gated: canon-gate --corpus stays
#                    below and is the check that matters for the game.
#   goal-block       compared the goal block at the top of CLAUDE.md against
#                    ledger-v2/respec/vision-pillars-v2.md. The new CLAUDE.md
#                    carries no goal block, so the check has nothing to compare.
#
# All three, and their selftests, are in legacy/studio-v2/tools/ with their
# subjects. legacy/studio-v2/REACTIVATE.md restores them as one step.
#
# FOUR SUITES CAME BACK ON 2026-09-22: Soak, SaveChaos, PerceptionGolden and
# StrangerTest. D16 named five suites, CoreTests included, as the ones that
# keep running when Unity was archived - "these keep running and are not
# archived" - and when the studio was paused only CoreTests and the fake-player
# harness came across into this table. Their PROJECT DIRECTORIES survived the
# whole time, which is exactly what made the loss invisible: `ledger/Soak/`
# sitting on disk reads like a suite that runs. A suite nothing invokes is not
# a suite. They are invoked here, by name, and they cost about a minute between
# them.
#
# PerceptionGolden IS NOT INVOKED DIRECTLY, and that is the second half of the
# repair. It EMITS the table the C++ port is compared against, and for as long
# as the comparison read the COMMITTED copy of that table the C# could move and
# nothing would go red - it had, by seven rows. `port-golden-check.sh`
# regenerates the table from the Core, fails on drift from the committed copy,
# and runs the port against the FRESH output. Its selftest is a separate entry
# for the reason the attribution check is two: "the port disagrees" and "the
# comparison is broken" are different facts with different fixes.
#
# THE REAL TABLE. One check per line: name <TAB> working-dir <TAB> command.
# Names carry no spaces — every reader of this output splits on whitespace.
#
# The attribution check is TWO entries where the workflow had one step running
# two commands, because "the licence audit failed" and "the licence auditor is
# broken" are different facts with different fixes, and one step could not say
# which had happened.
# THE PYTHON THAT ACTUALLY RUNS, RESOLVED ONCE, RATHER THAN THE FIRST NAME
# THAT ANSWERS.
#
# EIGHT OF THE SIXTEEN CHECKS BELOW HAD NEVER RUN ON JAFAR'S PC and nothing
# said so. They invoke `python3`, and on Windows `python3` is the MICROSOFT
# STORE APP EXECUTION ALIAS: a stub that prints "Python was not found; run
# without arguments to install from the Microsoft Store" and exits. Every one
# of them came back failed with a single line of output that looks like an
# installation problem, in a suite whose whole purpose is to be run before a
# commit - so the shape check, the attribution audit, the canon gate and both
# sky checks were simply never run here, while passing in CI, where the
# runner's PATH has a real python3 on it.
#
# THE SAME ALIAS HAS NOW BITTEN THREE TIMES IN ONE DAY: this, the stop hook
# (which would have permitted every stop, silently, forever) and the Blender
# render driver (which refused with NO-BLENDER). It answers to its name, it
# exits without an error anybody notices, and it is on PATH ahead of the real
# interpreter. So the rule here is the rule the hook already uses: a
# candidate has to EVALUATE SOMETHING before it is believed.
PY=""
for _cand in python3 python py; do
  if [ "$("$_cand" -c 'print(7*6)' 2>/dev/null)" = "42" ]; then PY="$_cand"; break; fi
done
if [ -z "$PY" ]; then
  echo "ci-checks refused: NO WORKING PYTHON. None of python3, python or py" \
       "could evaluate anything on this machine. Eight of the sixteen checks" \
       "below are python, so this is not a clean run with a few skips - it is" \
       "half the suite unmeasured, and it says so rather than reporting it."
  exit 3
fi
echo "ci-checks python=$PY"

real_table() {
  printf '%s\t%s\t%s\n' \
    reach-check           "$REPO"                 "bash tools/reach-check.sh" \
    shape-check           "$REPO"                 "$PY tools/shape-check.py" \
    shape-check-selftest  "$REPO"                 "$PY tools/shape-check.py --selftest" \
    attribution           "$REPO"                 "$PY tools/attribution-check.py" \
    attribution-selftest  "$REPO"                 "$PY tools/attribution-check.py --selftest" \
    canon-gate            "$REPO"                 "$PY tools/canon-gate.py --corpus" \
    canon-gate-selftest   "$REPO"                 "$PY tools/canon-gate.py --selftest" \
    spec-test             "$REPO"                 "bash tools/spec-test-check.sh" \
    talk-helper-selftest  "$REPO"                 "dotnet run --project ledger/TalkHelper -c Release -- --selftest" \
    crime-verdict-selftest "$REPO"                "$PY tools/crime-verdict-check.py --selftest" \
    encounter-check-selftest "$REPO"                "$PY tools/encounter-verdict-check.py --selftest" \
    sky-material-selftest "$REPO"                 "$PY tools/ue/make_sky_material.py --selftest" \
    sky-longlat-selftest  "$REPO"                 "$PY tools/hdr-to-longlat.py --selftest" \
    facade-drawing-selftest "$REPO"               "$PY tools/facade-drawing.py --selftest" \
    slice-perf-selftest   "$REPO"                 "$PY tools/slice-perf.py --selftest" \
    core-tests            "$REPO"                 "dotnet run --project ledger/CoreTests -c Release" \
    soak                  "$REPO"                 "dotnet run --project ledger/Soak -c Release" \
    save-chaos            "$REPO"                 "dotnet run --project ledger/SaveChaos -c Release" \
    perception-golden     "$REPO"                 "bash tools/port-golden-check.sh" \
    perception-golden-selftest "$REPO"            "bash tools/port-golden-check.sh --selftest" \
    stranger-test         "$REPO"                 "dotnet run --project ledger/StrangerTest -c Release -- --selftest" \
    playtest-fake         "$REPO/ledger/SimHarness" "dotnet run -c Release"
}

# ONE RUNNER. The real table and both selftest fixtures go through this same
# function — a selftest that exercises a different code path from the thing
# shipped proves nothing about the thing shipped.
#
# Reads the table on stdin. Prints one `check name=... outcome=...` line per
# check as it finishes, then the done line, then the detail for failures.
run_table() {
  local label="$1"
  local -a names=() outcomes=() rcs=() secs=() lines=()
  local total=0 passed=0
  local name dir cmd rc t0 t1 n

  while IFS=$'\t' read -r name dir cmd; do
    [ -z "${name:-}" ] && continue
    total=$((total + 1))
    echo
    echo "===== $label check $total: $name"
    echo "      \$ $cmd"
    t0=$(date +%s)
    # `tee` so the output is visible where it happened AND capturable for the
    # end-of-log summary. PIPESTATUS[0], never $? — $? here is tee's.
    ( cd "$dir" 2>/dev/null && eval "$cmd" ) 2>&1 | tee "$LOGDIR/$total.log"
    rc=${PIPESTATUS[0]}
    t1=$(date +%s)
    n=$(wc -l < "$LOGDIR/$total.log" | tr -d ' ')
    names+=("$name"); rcs+=("$rc"); secs+=("$((t1 - t0))"); lines+=("$n")
    if [ "$rc" -eq 0 ]; then
      outcomes+=("PASS"); passed=$((passed + 1))
    else
      outcomes+=("FAIL")
    fi
    # PER-CHECK LINE, per-check numbers only. outLines is the series the
    # TAIL_LINES bound above was set from; leave it printed.
    echo "check name=$name outcome=${outcomes[$((total - 1))]} rc=$rc secs=${secs[$((total - 1))]} outLines=$n"
  done

  echo

  # A ZERO NEEDS A DENOMINATOR, and an empty table is the zero that reads
  # most like health: no check failed because no check ran.
  if [ "$total" -eq 0 ]; then
    echo "$label done: nothing measured — 0 checks in the table"
    return 3
  fi

  local -a failed=()
  local i
  for i in "${!names[@]}"; do
    [ "${outcomes[$i]}" = "FAIL" ] && failed+=("${names[$i]}:rc${rcs[$i]}")
  done

  if [ "${#failed[@]}" -eq 0 ]; then
    # WHOLE-RUN NUMBERS ON THE DONE LINE. passed/total is one entry carrying
    # both halves, so no reader has to hold two keys' relationship in mind.
    echo "$label done: passed=$total/$total failed=none"
    return 0
  fi

  local joined
  joined=$(IFS=,; echo "${failed[*]}")

  # THE FAILURES' OUTPUT AGAIN, then the done line LAST. The order is the
  # whole point and it is not cosmetic: rule 12 says the only log channel
  # this environment can read is a fixed ~4KB BYTE TAIL, and a detail block
  # can run to seven. Printing the done line first would push the one line
  # that names WHICH check failed out of the readable window exactly when
  # there is most to read. Capped, and the cap says when it bit.
  for i in "${!names[@]}"; do
    [ "${outcomes[$i]}" = "FAIL" ] || continue
    echo
    echo "----- FAILURE DETAIL: ${names[$i]} (rc=${rcs[$i]}, ${lines[$i]} lines of output)"
    if [ "${lines[$i]}" -gt "$TAIL_LINES" ]; then
      echo "      (+$((lines[$i] - TAIL_LINES)) earlier lines not shown — see the run above)"
    fi
    tail -n "$TAIL_LINES" "$LOGDIR/$((i + 1)).log"
  done

  echo
  echo "$label done: passed=$passed/$total failed=$joined"
  return 1
}

# ---------------------------------------------------------------- selftest

# THE ACCEPTING CASE IS FIRST, deliberately. The expensive failure in this
# family is a harness nothing survives, not one that lets something through:
# four guards on this project passed their failure case and had never once
# been run against the case they must ACCEPT, and every one of them blocked
# the good result.
#
# The fixtures are synthetic (`true`, `false`, `exit 7`) rather than real
# checks, so the harness can be proved in a second and doing the work the
# harness prompts can never break the harness. The live repository is the
# accepting fixture for the REAL table — that is `tools/ci-checks.sh` with no
# arguments, and its output is the evidence.
selftest() {
  local pass=0 fail=0 out rc

  _expect() { # name expected-rc expected-substring
    local what="$1" want_rc="$2" want_txt="$3"
    if [ "$rc" != "$want_rc" ]; then
      echo "  FAIL $what — exit $rc, wanted $want_rc"; fail=$((fail + 1)); return
    fi
    if ! printf '%s' "$out" | grep -qF -- "$want_txt"; then
      echo "  FAIL $what — output did not contain: $want_txt"; fail=$((fail + 1)); return
    fi
    echo "  ok   $what — exit $rc, said: $want_txt"; pass=$((pass + 1))
  }

  echo "ci-checks selftest — the harness, not the project"
  echo

  echo "[1] ACCEPTING CASE: three checks that all pass"
  out=$(printf '%s\t%s\t%s\n' a . true b . true c . true | run_table selftest 2>&1); rc=$?
  _expect "all-pass exits 0"              0 "selftest done: passed=3/3 failed=none"
  _expect "all-pass names no failure"     0 "failed=none"

  echo
  echo "[2] REJECTING CASE: the middle check fails"
  out=$(printf '%s\t%s\t%s\n' a . true b . false c . true | run_table selftest 2>&1); rc=$?
  _expect "one-fail exits 1"              1 "selftest done: passed=2/3 failed=b:rc1"
  _expect "one-fail prints the detail"    1 "FAILURE DETAIL: b"

  echo
  echo "[3] THE ACTUAL FAULT: a failing check must not skip the ones below it"
  out=$(printf '%s\t%s\t%s\n' a . false b . "echo I-STILL-RAN" c . "echo SO-DID-I" \
        | run_table selftest 2>&1); rc=$?
  _expect "check after a failure ran"     1 "I-STILL-RAN"
  _expect "last check ran too"            1 "SO-DID-I"
  _expect "and the job is still red"      1 "passed=2/3 failed=a:rc1"

  echo
  echo "[4] EVERY check red, and the count says so rather than the names alone"
  out=$(printf '%s\t%s\t%s\n' a . false b . "exit 7" | run_table selftest 2>&1); rc=$?
  _expect "all-fail exits 1"              1 "passed=0/2 failed=a:rc1,b:rc7"
  _expect "the real exit code survives"   1 "rc=7"

  echo
  echo "[5] NOTHING MEASURED must not read as clean"
  out=$(printf '' | run_table selftest 2>&1); rc=$?
  _expect "empty table exits 3"           3 "nothing measured — 0 checks in the table"

  echo
  echo "[6] THE CAP ANNOUNCES ITSELF WHEN IT BITES"
  local saved="$TAIL_LINES"; TAIL_LINES=5
  out=$(printf '%s\t%s\t%s\n' big . "seq 1 20; false" | run_table selftest 2>&1); rc=$?
  _expect "cap says how much it hid"      1 "(+15 earlier lines not shown"
  _expect "and shows the tail"            1 "20"
  TAIL_LINES="$saved"

  echo
  echo "[7] A MISSING COMMAND IS A FAILURE, NOT A PASS"
  out=$(printf '%s\t%s\t%s\n' ghost . "no-such-command-here" | run_table selftest 2>&1); rc=$?
  _expect "missing binary fails"          1 "passed=0/1"

  echo
  echo "[8] THE DONE LINE IS LAST, so a 4KB log tail always reaches it"
  out=$(printf '%s\t%s\t%s\n' noisy . "seq 1 400; false" | run_table selftest 2>&1); rc=$?
  local lastline
  lastline=$(printf '%s' "$out" | tail -n 1)
  if [ "$rc" = 1 ] && [ "$lastline" = "selftest done: passed=0/1 failed=noisy:rc1" ]; then
    echo "  ok   done line is the final line, under 400 lines of detail"
    pass=$((pass + 1))
  else
    echo "  FAIL done line was not last — got: $lastline (exit $rc)"
    fail=$((fail + 1))
  fi
  _expect "and the detail is above it"    1 "(+280 earlier lines not shown"

  echo
  echo "ci-checks selftest: passed=$pass/$((pass + fail)) failed=$fail"
  [ "$fail" -eq 0 ] && return 0
  return 4
}

# -------------------------------------------------------------------- main

case "${1:-}" in
  --selftest)
    selftest; exit $? ;;
  --list)
    n=$(real_table | wc -l | tr -d ' ')
    echo "ci-checks table: $n checks"
    real_table | while IFS=$'\t' read -r name dir cmd; do
      printf '  %-22s %s\n' "$name" "$cmd"
    done
    exit 0 ;;
  "")
    real_table | run_table ci-checks; exit $? ;;
  *)
    echo "usage: ci-checks.sh [--list|--selftest]" >&2; exit 2 ;;
esac
