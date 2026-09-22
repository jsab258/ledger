#!/usr/bin/env python3
"""DID THE CRIME ACTUALLY HAPPEN? Read the probe's verdict and say.

    python3 tools/crime-verdict-check.py [PATH] [--sha SHORTSHA]
    python3 tools/crime-verdict-check.py --selftest

WHY THIS EXISTS, in the verdict file's own words. `ue-crime-verdict.txt`
carries this sentence at the top of every run:

    WHAT IS NOT TRUE YET, said here rather than left to be assumed: no
    automated check anywhere reads these lines, so a run in which the input
    path was dead is committed and pushed GREEN. A human reading this file is
    the only thing that catches it today.

That is the hole. The probe measures the crime beautifully and nothing reads
what it measured, so the one failure that matters most - the key press
silently stops working and the deed never happens - lands green, gets
committed, and is found days later by somebody scrolling a text file.

WHAT IT CHECKS, AND WHY EACH ONE. Every rule here is a thing that, if it
quietly stopped being true, would leave the run looking healthy:

  THE PRESS. pressLanded says how far an injected press got and requestsSeen
  says how many times the character's own binding fired. Those are separate
  facts on purpose - a press can land on a controller that never routes it -
  and BOTH have to be real or "attempted=yes" is describing something other
  than a key press. staleDropped must be zero: presses found waiting when the
  phase opened belong to no crime and a healthy run has none.

  THE DEED. crimeStatus=COMMITTED and the glass gone afterwards, read back
  off the actor rather than assumed from having asked.

  THE WITNESS AND THE CONTROL, WHICH ARE THE SAME RUN. w1 sees crime A from
  a metre and a half and files an observation with a rung; n2 is behind a
  building and files nothing. THE CONTROL IS THE HALF THAT USUALLY ROTS: a
  perception bug that makes everyone a witness passes every "did the witness
  see it" check ever written, and fails this one.

  THE MILL. Round 1 is the same two people too far apart to talk and must
  pass nothing; round 2 is the same two in the yard and must pass the rumour.
  Again a pair, and again the negative half is the one that catches a change
  that makes gossip travel regardless of distance.

  THE OVERHEARD LINE, because the whole point of the ruling is that the
  player hears the consequence.

  AND THE FILE IS THIS RUN'S. Line 1 names the commit it was measured on. A
  check that reads a verdict from last week and passes is worse than no check
  at all, which is the fault `sim-shots-stage.sh` exists for elsewhere in
  this repository.

IT REFUSES RATHER THAN GUESSES. A missing file, an unreadable one, or a
verdict that never reached its end is NOT a pass; it is a refusal that says
which, because "the crime did not happen" and "nothing measured whether it
happened" are different facts with different fixes.
"""
import os
import re
import sys

DEFAULT_PATH = os.path.join("production", "d1-probe", "ue-crime-verdict.txt")

#: A value in this file is `key=value` with no spaces inside the value; the
#: file says so at its head and the probe enforces it by turning spaces into
#: dashes. So a line is a bag of pairs and the parser is one split.
PAIR_RE = re.compile(r"([A-Za-z][A-Za-z0-9_]*)=([^\s]*)")


def pairs(line):
    """Every key=value on one line, as a dict."""
    return dict(PAIR_RE.findall(line))


def lines_named(text, key, value=None):
    """Every non-comment line carrying `key`, optionally with that value.

    A LINE MAY LEAD WITH A BARE TOKEN rather than a pair, and `crimeAct` does:
    it reads `crimeAct id=A pressesSent=1 ...`, where the first word names the
    KIND of line and everything after it is pairs. A reader that only
    understood `key=value` found no crimeAct line at all and reported that
    nothing said how the deed arrived - on a verdict that says so in detail.
    So a leading bare word counts as that key being present, with an empty
    value, which is what it is.
    """
    out = []
    for raw in text.splitlines():
        if raw.startswith("#") or not raw.strip():
            continue
        p = pairs(raw)
        head = raw.split()[0]
        if "=" not in head and head not in p:
            p[head] = ""
        if key in p and (value is None or p[key] == value):
            out.append(p)
    return out


def head_sha(text):
    """The short sha on line 1, or ''. The line reads `# UE crime probe <sha> @<stamp>`."""
    for raw in text.splitlines():
        if raw.startswith("#"):
            m = re.match(r"#\s*UE crime probe\s+([0-9a-f]{6,40})\b", raw)
            if m:
                return m.group(1)
        break
    return ""


def judge(text, sha=""):
    """(faults, notes). An empty faults list is a pass.

    PURE, so the selftest drives exactly what the run drives, with a real
    verdict as the accepting case and doctored copies of it as the rejecting
    ones. A check tested only against fixtures it invented is a check that
    agrees with itself.
    """
    faults, notes = [], []

    if not text.strip():
        return ["the verdict file is empty; nothing measured whether a crime happened"], notes

    got = head_sha(text)
    if not got:
        faults.append("line 1 does not name the commit this was measured on")
    elif sha and not (got.startswith(sha) or sha.startswith(got)):
        faults.append("the verdict was measured on %s and this run is %s - it is "
                      "an older file, not this run's answer" % (got, sha))
    else:
        notes.append("measuredOn=%s" % (got or "unknown"))

    # ---- the press --------------------------------------------------------
    acts = lines_named(text, "crimeAct")
    if not acts:
        faults.append("no crimeAct line: nothing says how the deed arrived")
    for a in acts:
        who = a.get("id", "?")
        if a.get("pressLanded") not in ("player-input", "controller"):
            faults.append("crime %s: the injected press landed nowhere (pressLanded=%s)"
                          % (who, a.get("pressLanded")))
        try:
            seen = int(a.get("requestsSeen", "0"))
        except ValueError:
            seen = 0
        if seen < 1:
            faults.append("crime %s: the character's own binding never fired "
                          "(requestsSeen=%s) - the deed did not come from a key press"
                          % (who, a.get("requestsSeen")))
        if a.get("attempted") != "yes":
            faults.append("crime %s: the deed was never begun (attempted=%s)"
                          % (who, a.get("attempted")))
        if a.get("took") != "yes":
            faults.append("crime %s: the deed was begun and did not take (took=%s)"
                          % (who, a.get("took")))
        if a.get("gaveUp") not in (None, "no"):
            faults.append("crime %s: the await phase gave up (gaveUp=%s)"
                          % (who, a.get("gaveUp")))
        if a.get("staleDropped") not in (None, "0"):
            faults.append("crime %s: %s stale press(es) were waiting when the phase "
                          "opened, which is a bug on a healthy run"
                          % (who, a.get("staleDropped")))
    notes.append("crimes=%d" % len(acts))

    # ---- the deed ---------------------------------------------------------
    crimes = lines_named(text, "crime")
    if not crimes:
        faults.append("no crime= line: nothing says whether a window went in")
    for c in crimes:
        who = c.get("crime", "?")
        if c.get("crimeStatus") != "COMMITTED":
            faults.append("crime %s did not happen (crimeStatus=%s)"
                          % (who, c.get("crimeStatus")))
        if c.get("glassHiddenAfter") != "yes":
            faults.append("crime %s: the glass is still standing afterwards" % who)

    # ---- the witness AND the control --------------------------------------
    filed = [w for w in lines_named(text, "witness") if w.get("filed") == "yes"]
    empty = [w for w in lines_named(text, "witness") if w.get("filed") == "no"]
    if not filed:
        faults.append("NOBODY SAW IT: not one witness filed an observation, so the "
                      "crime happened and left no trace in anybody's head")
    for w in filed:
        try:
            rung = int(w.get("idRung", "0"))
        except ValueError:
            rung = 0
        if rung < 1:
            faults.append("witness %s filed on %s at rung 0, which is an observation "
                          "carrying no identification at all"
                          % (w.get("witness"), w.get("event")))
    if not empty:
        faults.append("THE CONTROL IS MISSING: every witness filed something. The "
                      "occluded witness exists so that a change making everybody a "
                      "witness fails here rather than passing every other check")
    notes.append("filed=%d/%d" % (len(filed), len(filed) + len(empty)))

    # ---- the mill, both halves -------------------------------------------
    rounds = {r.get("gossipRound"): r for r in lines_named(text, "gossipRound")}
    if "1" not in rounds or "2" not in rounds:
        faults.append("the rule-5b pair is not both here (rounds present: %s)"
                      % ",".join(sorted(rounds)) or "none")
    else:
        if rounds["1"].get("passedStatus") != "NOT-TOGETHER":
            faults.append("round 1: two people nineteen metres apart passed a rumour "
                          "(passedStatus=%s) - distance stopped mattering"
                          % rounds["1"].get("passedStatus"))
        if rounds["2"].get("passedStatus") != "PASSED":
            faults.append("round 2: two people standing together passed nothing "
                          "(passedStatus=%s)" % rounds["2"].get("passedStatus"))

    # ---- the consequence the player hears ---------------------------------
    over = lines_named(text, "overheardStatus")
    if not over:
        faults.append("no overheard line: nothing says whether the player heard it")
    elif over[0].get("overheardStatus") != "HEARD":
        faults.append("the player heard nothing (overheardStatus=%s)"
                      % over[0].get("overheardStatus"))

    # ---- and the memories reached the disk ---------------------------------
    mem = lines_named(text, "memoryFiles")
    if mem:
        got_mem = mem[0].get("memoryFiles", "")
        if "/" in got_mem:
            wrote, asked = got_mem.split("/", 1)
            if wrote != asked:
                faults.append("only %s of %s memory files were written" % (wrote, asked))
        notes.append("memoryFiles=%s" % got_mem)

    return faults, notes


# ---------------------------------------------------------------------------


def selftest():
    passed = failed = 0

    def check(name, ok, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print("crime-verdict selftest FAIL %s: %s" % (name, detail))

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, DEFAULT_PATH)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            real = fh.read()
    except OSError:
        real = ""

    # THE ACCEPTING CASE IS THE LANDED VERDICT ITSELF, not a fixture. A check
    # proved against a file it made up proves only that it agrees with itself,
    # and the committed verdict is a real green run.
    if real:
        faults, notes = judge(real, head_sha(real))
        check("accept/the-landed-verdict-passes", not faults,
              "; ".join(faults[:3]))
        check("accept/and-it-counted-what-it-read",
              any(n.startswith("crimes=") for n in notes), str(notes))
    else:
        check("accept/the-landed-verdict-is-readable", False, "no verdict on disk")

    # THE REJECTING CASES ARE THAT SAME FILE, DOCTORED ONE VALUE AT A TIME.
    # Each one is a real failure this is meant to catch, and the point of
    # doctoring the real file rather than writing a small one is that the
    # check has to find the fault in a verdict that is otherwise perfect.
    if real:
        for name, old, new in (
                ("the-press-landed-nowhere", "pressLanded=player-input", "pressLanded=none"),
                ("the-binding-never-fired", "requestsSeen=1", "requestsSeen=0"),
                ("the-deed-was-never-begun", "attempted=yes", "attempted=no"),
                ("the-deed-did-not-take", "took=yes", "took=no"),
                ("a-stale-press-was-waiting", "staleDropped=0", "staleDropped=2"),
                ("the-crime-did-not-happen", "crimeStatus=COMMITTED", "crimeStatus=REFUSED"),
                ("the-glass-is-still-standing", "glassHiddenAfter=yes", "glassHiddenAfter=no"),
                ("the-rumour-travelled-nineteen-metres",
                 "passedStatus=NOT-TOGETHER", "passedStatus=PASSED"),
                ("nobody-heard-the-consequence",
                 "overheardStatus=HEARD", "overheardStatus=SILENT"),
        ):
            if old not in real:
                check("reject/%s" % name, False, "the real verdict has no %r to doctor" % old)
                continue
            faults, _n = judge(real.replace(old, new), head_sha(real))
            check("reject/%s-is-caught" % name, bool(faults), "no fault reported")

        # NOBODY SAW IT, which needs every filed=yes turned off at once.
        faults, _n = judge(real.replace("filed=yes", "filed=no"), head_sha(real))
        check("reject/a-crime-nobody-saw-is-caught", bool(faults))
        # AND EVERYBODY SAW IT, which is the control rotting away and is the
        # half a careless version of this would leave out.
        faults, _n = judge(real.replace("filed=no", "filed=yes"), head_sha(real))
        check("reject/a-crime-EVERYBODY-saw-is-caught-too", bool(faults),
              "the control is what catches a perception bug that files everything")

        # A VERDICT FROM ANOTHER COMMIT IS NOT THIS RUN'S ANSWER.
        faults, _n = judge(real, "0000000")
        check("reject/a-stale-verdict-is-refused", bool(faults))

    faults, _n = judge("")
    check("reject/an-empty-file-is-refused-not-passed", bool(faults))
    faults, _n = judge("# UE crime probe abc1234 @1\nnothing else here\n", "abc1234")
    check("reject/a-verdict-that-measured-nothing-is-refused", bool(faults))

    print("crime-verdict selftest: passed=%d/%d failed=%d"
          % (passed, passed + failed, failed))
    return 0 if failed == 0 else 4


def main(argv):
    args = argv[1:]
    if "--selftest" in args:
        return selftest()
    sha = ""
    path = ""
    i = 0
    while i < len(args):
        if args[i] == "--sha" and i + 1 < len(args):
            sha = args[i + 1]
            i += 2
            continue
        if args[i].startswith("--"):
            print("crime-verdict refused: unknown-flag/%s nothing measured" % args[i])
            return 2
        path = args[i]
        i += 1
    if not path:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, DEFAULT_PATH)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        print("crime-verdict refused: the verdict is unreadable (%s at %s). This is "
              "not a clean run; it is nothing measured."
              % (type(exc).__name__, path))
        return 3

    faults, notes = judge(text, sha)
    for n in notes:
        print("  %s" % n)
    if faults:
        print("crime-verdict: THE CRIME DID NOT HAPPEN AS IT SHOULD, %d fault(s):"
              % len(faults))
        for f in faults:
            print("  - %s" % f)
        return 1
    print("crime-verdict: the deed came from a key press, it took, one witness "
          "filed it and one did not, the rumour travelled only when they stood "
          "together, and the player heard it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
