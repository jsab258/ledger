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

    # ---- the unwitnessed control ------------------------------------------
    # GATED THE SAME WAY AS THE RESTART: absent means not measured and says
    # so, present means judged. The control is crime B, which happens in the
    # same run as crime A with both agents behind a building - same build,
    # same mill, same perception code, same frame, and the only thing that
    # differs is whether anybody could see it.
    ctl = lines_named(text, "control")
    if not ctl:
        notes.append("control=NOT-IN-THIS-VERDICT/nothing-measured-about-the-crime-nobody-saw")
    else:
        c = ctl[0]
        def cnum(k):
            try:
                return int(c.get(k, ""))
            except ValueError:
                return None
        sa, sb = cnum("seenA"), cnum("seenB")
        ra, rb = cnum("rumoursAboutA"), cnum("rumoursAboutB")
        if sa is None or sa < 1:
            faults.append("the WITNESSED crime was seen by nobody (seenA=%s) - there is "
                          "no positive half to compare the control against"
                          % c.get("seenA"))
        if sb is None or sb != 0:
            faults.append("THE CONTROL WAS SEEN: %s observation(s) filed on a crime both "
                          "agents were behind a building for" % c.get("seenB"))
        if rb is None or rb != 0:
            faults.append("THE CONTROL PRODUCED A RUMOUR: %s about a crime nobody "
                          "witnessed, which is the mill inventing" % c.get("rumoursAboutB"))
        if ra is None or ra < 1:
            faults.append("the witnessed crime produced no rumour (rumoursAboutA=%s), so "
                          "the control proving nothing proves nothing" % c.get("rumoursAboutA"))
        notes.append("control=A seen by %s and carried by %s; B seen by %s and carried by %s"
                     % (c.get("seenA"), c.get("rumoursAboutA"),
                        c.get("seenB"), c.get("rumoursAboutB")))

    # ---- the restart, once the probe carries one --------------------------
    # GATED ON THE LINE BEING THERE, AND LOUD WHEN IT IS NOT. The probe
    # learned to save, rebuild and reload on 22 September and the verdict
    # committed before that build has no restart line. Treating its absence
    # as a pass would be the quiet kind of nothing-measured this file exists
    # to refuse, so it is a NOTE that says so in capitals - and the moment a
    # verdict carries the line, every rule below bites.
    rt = lines_named(text, "restart")
    if not rt:
        notes.append("restart=NOT-IN-THIS-VERDICT/nothing-measured-about-surviving-a-restart")
    else:
        r = rt[0]
        if r.get("restart") != "RAN":
            faults.append("the restart did not run (restart=%s)" % r.get("restart"))
        else:
            def num(k):
                try:
                    return int(r.get(k, ""))
                except ValueError:
                    return None
            w1b, w1a = num("w1RumoursBefore"), num("w1RumoursAfter")
            n2b, n2a = num("n2RumoursBefore"), num("n2RumoursAfter")
            if w1a is None or w1b is None or w1a != w1b:
                faults.append("the witness lost rumours across the restart (%s before, %s after)"
                              % (r.get("w1RumoursBefore"), r.get("w1RumoursAfter")))
            elif w1a < 1:
                faults.append("the witness held no rumour to survive the restart")
            if n2a is None or n2b is None or n2a != n2b:
                faults.append("the lad in the yard lost rumours across the restart "
                              "(%s before, %s after)"
                              % (r.get("n2RumoursBefore"), r.get("n2RumoursAfter")))
            mb, ma = num("w1MemoryBefore"), num("w1MemoryAfter")
            if mb is None or ma is None or mb != ma:
                faults.append("the witness's memory changed across the restart "
                              "(%s events before, %s after)"
                              % (r.get("w1MemoryBefore"), r.get("w1MemoryAfter")))
            if r.get("memoryTextStable") != "yes":
                faults.append("the memory markdown did not come back the same "
                              "(memoryTextStable=%s)" % r.get("memoryTextStable"))
            # THE CONTROL, AND IT IS THE HOP COUNT THAT CARRIES IT. The
            # shopkeeper SAW it and comes back first-hand; the lad HEARD it
            # and comes back one hop out. A restore that handed every agent
            # the same records keeps every count above correct and collapses
            # these two into each other.
            wh, nh = num("w1HopsAfter"), num("n2HopsAfter")
            if wh is not None and wh != 0:
                faults.append("the witness who SAW it came back %s hops out, not first-hand" % wh)
            if nh is not None and nh < 1:
                faults.append("the lad who HEARD it came back first-hand - the restore "
                              "handed him the witness's own observation")
            notes.append("restart=w1 %s->%s rumours, hops %s; n2 %s->%s, hops %s"
                         % (r.get("w1RumoursBefore"), r.get("w1RumoursAfter"), r.get("w1HopsAfter"),
                            r.get("n2RumoursBefore"), r.get("n2RumoursAfter"), r.get("n2HopsAfter")))

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


LF = chr(10)


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

    # THE RESTART RULES, on a verdict that carries the line. The landed one
    # does not yet, so these are driven from a minimal fixture - and the
    # ACCEPTING case is included so the rejecting ones are known to be
    # rejecting something a good line would pass.
    GOOD_RT = ("restart=RAN w1RumoursBefore=1 w1RumoursAfter=1 n2RumoursBefore=1 "
               "n2RumoursAfter=1 w1MemoryBefore=1 w1MemoryAfter=1 w1HopsAfter=0 "
               "n2HopsAfter=1 memoryTextStable=yes")
    if real:
        ok_text = real.rstrip(chr(10)) + chr(10) + GOOD_RT + chr(10)
        faults, _n = judge(ok_text, head_sha(real))
        check("accept/a-good-restart-line-passes", not faults, "; ".join(faults[:2]))
        for name, old_v, new_v in (
                ("the-witness-lost-a-rumour", "w1RumoursAfter=1", "w1RumoursAfter=0"),
                ("the-lad-lost-a-rumour", "n2RumoursAfter=1", "n2RumoursAfter=0"),
                ("the-memory-changed", "w1MemoryAfter=1", "w1MemoryAfter=2"),
                ("the-markdown-did-not-round-trip",
                 "memoryTextStable=yes", "memoryTextStable=no"),
                ("the-restart-never-ran", "restart=RAN", "restart=NOT-RUN"),
                ("everyone-came-back-first-hand", "n2HopsAfter=1", "n2HopsAfter=0"),
                ("the-eyewitness-came-back-second-hand", "w1HopsAfter=0", "w1HopsAfter=1"),
        ):
            faults, _n = judge(ok_text.replace(old_v, new_v), head_sha(real))
            check("reject/%s-is-caught" % name, bool(faults))

    # THE CONTROL'S OWN RULES, on a verdict that carries the line.
    GOOD_CTL = ("control=RAN controlCrime=B seenA=1 seenB=0 "
                "rumoursAboutA=1 rumoursAboutB=0")
    if real:
        # THE FIXTURE MUST BE THE ONLY CONTROL LINE IN THE FILE, and it was
        # not. This appended GOOD_CTL to the landed verdict and doctored it
        # one value at a time - which worked exactly as long as the landed
        # verdict had NO control line of its own. On 22 September the probe
        # started emitting one, so every runner copy carried two: the real
        # line and the fixture. judge reads the first it finds, which is the
        # real one, so doctoring the fixture changed nothing it looked at and
        # `reject/the-witnessed-one-carried-nothing-is-caught` stopped being
        # able to fail-and-be-caught. It failed on the runner and passed here,
        # because the local copy of the verdict predated the control line.
        # THAT ONE FAILING CASE REDDENED EVERY PROBE RUN, because the workflow
        # runs `--selftest || exit 1` before it judges anything: three runs
        # went red with a perfectly good verdict sitting beside them.
        base = LF.join(l for l in real.split(LF) if not l.startswith("control="))
        ok_c = base.rstrip(chr(10)) + chr(10) + GOOD_CTL + chr(10)
        faults, _n = judge(ok_c, head_sha(real))
        check("accept/a-good-control-line-passes", not faults, "; ".join(faults[:2]))
        for name, old_v, new_v in (
                ("the-control-was-seen", "seenB=0", "seenB=2"),
                ("the-control-produced-a-rumour", "rumoursAboutB=0", "rumoursAboutB=1"),
                ("nobody-saw-the-witnessed-one", "seenA=1", "seenA=0"),
                ("the-witnessed-one-carried-nothing", "rumoursAboutA=1", "rumoursAboutA=0"),
        ):
            faults, _n = judge(ok_c.replace(old_v, new_v), head_sha(real))
            check("reject/%s-is-caught" % name, bool(faults))

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
