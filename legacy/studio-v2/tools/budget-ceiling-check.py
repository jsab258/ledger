#!/usr/bin/env python3
"""EXACTLY ONE MACHINE-READABLE CEILING LINE IN production/budget.md, and the
prose beside it saying the same number.

    python3 tools/budget-ceiling-check.py            # walk the live document
    python3 tools/budget-ceiling-check.py --selftest # the fixtures, verbose

WHAT IT GUARDS, AND WHY IT IS NOT IN THE BOT'S SUITE. Queue 268. The bot's
selftest already read the live document, so deleting the machine line turned
the commit gate red, and that was a guard living in another tool's tests:
it holds only while that suite exists and only while it keeps reading the
live file, and nothing said so where an editor of either would see it. A
rule about the SHAPE OF A DOCUMENT belongs beside the other document checks
(`tools/docs-check.py` is the other one, and ledger/verify.py runs both at
every commit), not inside the channel that runs on Jafar's PC.

THE ASYMMETRY WITH THE BOT IS RULED AND IS NOT AN OVERSIGHT (2026-09-13,
game-design/decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md
section 2b point 2). `budget-ceiling.ceiling_from_text` ANSWERS when two
matching lines agree and refuses only when they disagree, because refusing
Jafar a verdict over a harmless duplicate is the wrong trade for a channel.
THIS fails on ANY duplicate, because two agreeing lines today are two lines
that disagree after the next edit touches one of them, and the document's
rule is exactly one. Every fixture below prints BOTH verdicts on the same
bytes, so the asymmetry is a measured pair in one run and not a comment that
decays.

WHAT IT CHECKS, three checks, each named in its own failure:
  1. machine-line/deleted      zero `Ceiling for LEDGER: N%` lines
  2. machine-line/duplicated   two or more, agreeing or not
  3. prose/missing or prose/disagrees, the sentence Jafar reads against the
     line the tools read. A cross-check and never a second source: it carries
     no number of its own, it only refuses to let the halves drift apart in
     silence. Check 3 CANNOT RUN when check 1 or 2 failed, and it says
     "nothing measured" rather than passing.

EXIT CODES, distinct per outcome. 0 clean. 1 the document broke a rule, each
named. 2 NOTHING MEASURED: the document is not there or could not be read,
which is not the same as a clean document and must never read as one. 3 the
selftest failed. 4 tools/budget-ceiling.py could not be imported, so there is
no pattern behind the sweep and this program will not report a clean result it
could not perform.
"""
import argparse
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULE = pathlib.Path(__file__).resolve().parent / "budget-ceiling.py"
# HOW MANY LINE NUMBERS A VALUE CARRIES BEFORE THE CAP BITES. The live
# document carries one and the worst fixture here carries two; the cap exists
# for the pathological document, and it announces itself when it bites rather
# than printing a shorter list that reads as a smaller fault.
LINES_SHOWN = 8


def load_patterns():
    """(module, why) for tools/budget-ceiling.py, imported by path because the
    file name carries a hyphen. ONE IMPLEMENTATION PER IDEA: the patterns are
    the ones tools/glance.py draws with and tools/runner/telegram-bot.py
    judges with, so this guard cannot pass a document those two would fail."""
    try:
        spec = importlib.util.spec_from_file_location("ledger_budget_ceiling",
                                                      str(MODULE))
        if spec is None or spec.loader is None:
            return None, "%s could not be loaded as a python module" % MODULE
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as exc:                                     # noqa: BLE001
        return None, ("tools/budget-ceiling.py could not be imported (%s: %s)"
                      % (type(exc).__name__, exc))
    for name in ("BUDGET", "CEILING", "ROW_CEILING", "PROSE_CEILING",
                 "ceiling_from_text", "line_hits"):
        if not hasattr(mod, name):
            return None, ("tools/budget-ceiling.py carries no %s, so this "
                          "guard has no pattern to check the document with"
                          % name)
    return mod, ""


def _lines_value(nums):
    """Line numbers as ONE key=value value: no spaces, `/` for structure, and
    the cap announcing itself in the value itself. A truncated list that does
    not say it was truncated reads as a smaller fault than the one measured."""
    if not nums:
        return "nothing-measured"
    shown = "/".join(str(n) for n in nums[:LINES_SHOWN])
    if len(nums) > LINES_SHOWN:
        shown += "/..+%d-more-not-shown" % (len(nums) - LINES_SHOWN)
    return shown


def census(text, bc, rel=None):
    """What the document says, counted. PURE: text in, numbers out, so the
    arithmetic and the strings are exercised by the fixtures below rather
    than only by a live file that is right today.

    Every count here is CUMULATIVE OVER ONE DOCUMENT: how many lines were
    examined, how many machine lines matched and where, how many prose
    statements matched and where. No peak, no median: one walk, one total.
    """
    rel = rel or bc.BUDGET
    # `splitlines`, NOT `count("\n") + 1`: every file here ends in a newline,
    # so the second counts one line more than the document has, and a
    # denominator larger than the set examined is CLAUDE.md rule 3b's false
    # claim with a number on it. Measured on the live document while this was
    # written: wc -l 601, splitlines 601, count-plus-one 602.
    machine = bc.line_hits(text, bc.CEILING)
    prose = bc.line_hits(text, bc.PROSE_CEILING)
    return {
        "rel": rel,
        "examined": len(text.splitlines()),
        "machineAt": [ln for ln, _m in machine],
        "machinePct": [int(m.group(1)) for _ln, m in machine],
        "proseAt": [ln for ln, _m in prose],
        "prosePct": [int(m.group(1)) for _ln, m in prose],
    }


def faults_in(c):
    """[(name, message)] for one census, in check order, each naming its
    remedy. A CLEAN RESULT IS AN EMPTY LIST BESIDE `checksRun`, never a bare
    zero: check 3 cannot run when check 1 or 2 failed, and the done line
    prints which of the three actually ran."""
    out = []
    n = len(c["machineAt"])
    if n == 0:
        out.append(("machine-line/deleted",
                    "%s carries no 'Ceiling for LEDGER: N%%' line, of %d "
                    "line(s) examined. That is the state 1aedef87 left this "
                    "repository in for two days, with the console printing "
                    "ceilingPct=nothing-measured and no bar on his page. "
                    "REMEDY: restore one line reading 'Ceiling for LEDGER: "
                    "N%% of the weekly limit.' under the DO NOT TIDY THIS "
                    "AWAY paragraph, carrying the number the prose states."
                    % (c["rel"], c["examined"])))
    elif n > 1:
        vals = sorted(set(c["machinePct"]))
        agree = ("all saying %d percent" % vals[0] if len(vals) == 1
                 else "saying %s percent"
                 % " and ".join(str(v) for v in vals))
        out.append(("machine-line/duplicated",
                    "%s carries %d 'Ceiling for LEDGER: N%%' lines (line(s) "
                    "%s of %d examined), %s, where exactly one is the rule. "
                    "%s REMEDY: delete every copy but the one under the DO "
                    "NOT TIDY THIS AWAY paragraph."
                    % (c["rel"], n, _lines_value(c["machineAt"]),
                       c["examined"], agree,
                       "Two that agree today are two that disagree after the "
                       "next edit touches one of them; the bot still answers "
                       "on this document and that leniency is ruled, so this "
                       "is the only guard that fails."
                       if len(vals) == 1 else
                       "The bot refuses a verdict on this document, so Jafar "
                       "gets no reading at all until it is fixed.")))
    if len(c["proseAt"]) == 0:
        out.append(("prose/missing",
                    "%s carries no sentence of the form 'THE CEILING IS N ON "
                    "THE HIGHER METER', of %d line(s) examined, so the half "
                    "Jafar reads states no ceiling at all and the machine "
                    "line has nothing to be checked against. REMEDY: state "
                    "the ceiling in his words beside the machine line; both "
                    "halves change in the same edit."
                    % (c["rel"], c["examined"])))
    elif n == 1:
        want = c["machinePct"][0]
        wrong = sorted(set(p for p in c["prosePct"] if p != want))
        if wrong:
            out.append(("prose/disagrees",
                        "%s states %d in prose (line(s) %s) against the "
                        "machine line's %d on line %d, of %d line(s) "
                        "examined. That is the 2026-09-11 fault: the file "
                        "carried both numbers at once, the wrong one was "
                        "nearer the top, and work was narrowed for a breach "
                        "that had not happened. REMEDY: fix whichever is "
                        "wrong; the prose and the line change in the same "
                        "edit."
                        % (c["rel"], wrong[0],
                           _lines_value([ln for ln, p
                                         in zip(c["proseAt"], c["prosePct"])
                                         if p != want]),
                           want, c["machineAt"][0], c["examined"])))
    return out


def checks_run(c):
    """(run, total). The third check CANNOT RUN without exactly one machine
    line to compare against, and a check that did not run is never counted as
    a check that passed."""
    return (3 if len(c["machineAt"]) == 1 else 2), 3


def done_line(c, faults, fx_pass, fx_fail):
    """The one machine line, whole-document numbers only. Per-fixture numbers
    go on the fixture lines above it, never under one key here: a reader
    greping across lines would otherwise take two moments as one.

    No spaces inside any value: `/` and `..` carry the structure, because
    every reader of a key=value channel splits on whitespace."""
    ran, total = checks_run(c)
    pct = (str(c["machinePct"][0]) if len(c["machinePct"]) == 1
           else "nothing-measured")
    return ("budget-ceiling-check: %s doc=%s linesExamined=%d "
            "machineLines=%d/1-wanted machineAt=%s machinePct=%s "
            "proseStatements=%d proseAt=%s proseValues=%s "
            "checksRun=%d/%d-checks faults=%d/%d-checks-that-ran "
            "fixturesAgreed=%d/%d-fixtures"
            % ("PASS" if not faults else "FAIL", c["rel"], c["examined"],
               len(c["machineAt"]), _lines_value(c["machineAt"]), pct,
               len(c["proseAt"]), _lines_value(c["proseAt"]),
               "/".join(str(v) for v in sorted(set(c["prosePct"])))
               or "nothing-measured",
               ran, total, len(faults), ran, fx_pass, fx_pass + fx_fail))


def nothing_measured_line(rel, why):
    """A run that measured nothing says so in the same channel, and never
    prints a zero that a reader could take for a clean document."""
    return ("budget-ceiling-check: NOTHING MEASURED doc=%s linesExamined=0 "
            "machineLines=nothing-measured proseStatements=nothing-measured "
            "checksRun=0/3-checks faults=nothing-measured why=%s"
            % (rel, why.replace(" ", "-")))


# ------------------------------------------------------------------ fixtures
#
# ACCEPTING CASE FIRST, and the accepting case that matters most is THE LIVE
# DOCUMENT, walked by a plain run: for a tool that checks the project itself
# the live file is the accepting fixture (instruments.md), and the rejecting
# fixtures are synthetic documents that exist nowhere, so doing the work this
# guard prompts can never break the guard.
#
# The synthetic accepting fixture below exists for the other direction: the
# day the patterns stop matching anything, the live document alone would go
# red and read as a broken document rather than a broken guard.
_PROSE = "THE STANDING CEILING IS 85 ON THE HIGHER METER. Ruled by Jafar.\n"
_LINE85 = "Ceiling for LEDGER: 85% of the weekly limit. The other 15% is his.\n"
_LINE80 = "Ceiling for LEDGER: 80% of the weekly limit. The other 20% is his.\n"

FIXTURES = (
    ("accept/one-line-and-the-prose-agreeing",
     _PROSE + "some prose in between\n" + _LINE85, None),
    ("reject/the-machine-line-deleted-by-a-header-rewrite",
     _PROSE + "four paragraphs of prose and no line a tool can read\n",
     "machine-line/deleted"),
    ("reject/two-lines-at-the-same-number",
     _PROSE + _LINE85 + "sixty lines of prose\n" + _LINE85,
     "machine-line/duplicated"),
    ("reject/two-lines-that-disagree",
     _PROSE + _LINE80 + "sixty lines of prose\n" + _LINE85,
     "machine-line/duplicated"),
    ("reject/the-prose-disagreeing-with-the-line",
     "THE CEILING IS 80 ON THE HIGHER METER.\n" + _LINE85,
     "prose/disagrees"),
    ("reject/no-prose-at-all", _LINE85, "prose/missing"),
)


def fixture_lines(bc):
    """(passed, failed, lines). PURE, so it runs on EVERY invocation and not
    behind a flag: what it guards is silent in both directions. The day the
    accepting pattern stops matching, the live document goes red and reads as
    a broken document; the day a refusal stops firing, a duplicate comes back
    and nothing says a word.

    EACH LINE CARRIES BOTH VERDICTS ON THE SAME BYTES: this guard's, and the
    bot reader's (`ceiling_from_text`). That pair is the ruled asymmetry made
    visible in one run from one vantage: on the agreeing duplicate the bot
    ANSWERS 85 and this guard FAILS, and both are correct.
    """
    passed, failed, lines = 0, 0, []
    for name, text, want in FIXTURES:
        c = census(text, bc, rel="fixture/%s" % name.split("/")[-1])
        got = [n for n, _msg in faults_in(c)]
        good = (want is None and not got) or (want is not None and want in got)
        pct, _from, why = bc.ceiling_from_text(text, c["rel"])
        bot = ("answers-%d" % pct if pct is not None else "refuses")
        lines.append("  %-6s %-46s guard=%s botReader=%s faults=%s"
                     % ("ok" if good else "FAIL", name,
                        "PASS" if not got else "FAIL", bot,
                        ",".join(got) or "none/0-of-3-checks"))
        if not good:
            failed += 1
            lines.append("         wanted %s, got %s (why: %s)"
                         % (want or "no fault", got or "none", why or "-"))
        else:
            passed += 1
    return passed, failed, lines


def read_live(bc):
    """(text, why) for the live document. A missing file is NOTHING MEASURED
    and never an empty document."""
    path = ROOT / pathlib.Path(bc.BUDGET)
    try:
        return path.read_text(encoding="utf-8"), ""
    except OSError as exc:
        return None, ("%s could not be read (%s)"
                      % (bc.BUDGET, type(exc).__name__))


def main():
    bc, why = load_patterns()
    if bc is None:
        sys.stderr.write("budget-ceiling-check: %s; refusing to report a "
                         "clean document with no pattern behind the sweep\n"
                         % why)
        return 4
    text, why = read_live(bc)
    if text is None:
        print(nothing_measured_line(bc.BUDGET, why))
        return 2
    c = census(text, bc)
    faults = faults_in(c)
    # NOT `budget-ceiling-check: ` ON THIS LINE, and the colon is the whole
    # reason. The done line at the bottom carries that prefix, and a reader
    # taking the FIRST line with it got this header instead: ledger/verify.py
    # reported "the guard exited 0 without reporting machineLines/..." on a
    # run that had reported all of them, one line further down. One prefix,
    # one machine line.
    print("budget-ceiling-check reads %s, the live document, walked first"
          % bc.BUDGET)
    # THE ZERO SHIPS ITS DENOMINATOR ON BOTH HALVES: "0 machine lines" beside
    # the count of lines that were examined looking for one, so a document
    # this guard could not read never reads as a document it found clean.
    print("  %d machine line(s) of 1 wanted, at line(s) %s; %d prose "
          "statement(s), at line(s) %s; %d line(s) examined"
          % (len(c["machineAt"]), _lines_value(c["machineAt"]),
             len(c["proseAt"]), _lines_value(c["proseAt"]), c["examined"]))
    for name, msg in faults:
        print("  FAIL %s: %s" % (name, msg))
    fx_pass, fx_fail, lines = fixture_lines(bc)
    print("\n  the fixtures, accepting first (the live document above is the "
          "other accepting case):")
    for line in lines:
        print(line)
    print()
    print(done_line(c, faults, fx_pass, fx_fail))
    return 1 if (faults or fx_fail) else 0


def selftest():
    """The verbose form, ACCEPTING CASE FIRST and the live document is it."""
    bc, why = load_patterns()
    if bc is None:
        print("budget-ceiling-check --selftest: 0 passed, 1 failed. %s" % why)
        return 4
    print("budget-ceiling-check --selftest: ACCEPTING CASE FIRST, and it is "
          "the live %s\n" % bc.BUDGET)
    text, why = read_live(bc)
    bad = 0
    if text is None:
        print("  FAIL live document: %s" % why)
        bad += 1
        c = census("", bc)
        live_ok = False
    else:
        c = census(text, bc)
        live_faults = faults_in(c)
        live_ok = not live_faults
        bad += 0 if live_ok else 1
        print("  %-6s live/%s: machineLines=%d/1-wanted machineAt=%s "
              "machinePct=%s proseStatements=%d proseAt=%s"
              % ("ok" if live_ok else "FAIL", bc.BUDGET, len(c["machineAt"]),
                 _lines_value(c["machineAt"]),
                 "/".join(str(v) for v in c["machinePct"]) or "nothing-measured",
                 len(c["proseAt"]), _lines_value(c["proseAt"])))
        for name, msg in live_faults:
            print("         %s: %s" % (name, msg))
    print("\n  THE SYNTHETIC FIXTURES, one accepting and five rejecting, each "
          "printing this guard's verdict beside the bot reader's on the same "
          "bytes (the asymmetry is ruled, section 2b point 2):\n")
    fx_pass, fx_fail, lines = fixture_lines(bc)
    for line in lines:
        print(line)
    bad += fx_fail
    total = 1 + fx_pass + fx_fail
    accepting = 1 + sum(1 for _n, _t, w in FIXTURES if w is None)
    rejecting = sum(1 for _n, _t, w in FIXTURES if w is not None)
    print("\nbudget-ceiling-check --selftest: %s. %d passed, %d failed, %d "
          "accepting case(s) (the live document and %d synthetic), %d "
          "rejecting fixture(s)."
          % ("PASS" if not bad else "FAILED", total - bad, bad, accepting,
             accepting - 1, rejecting))
    return 0 if not bad else 3


if __name__ == "__main__":
    # A correct run that ends in a BrokenPipeError traceback costs twenty
    # minutes before anybody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    _ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    _ap.add_argument("--selftest", action="store_true")
    sys.exit(selftest() if _ap.parse_args().selftest else main())
