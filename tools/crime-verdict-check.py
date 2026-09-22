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

    # ---- the header's own selftest, run again on the machine ----------------
    # The verdict has always printed it and nothing ever read it: a failing
    # in-game selftest now fails the run (independent check, 22 September).
    st = lines_named(text, "crimeSelftestChecks")
    if st:
        failed = st[0].get("crimeSelftestFailed", "")
        if not failed.startswith("0/"):
            faults.append("the crime selftest failed on the machine (crimeSelftestFailed=%s, "
                          "first: %s)" % (failed, st[0].get("crimeSelftestFirstFailure")))

    # ---- the third resident: ROADMAP's stage-3 reach gate ------------------
    # "A witnessed crime reaching a second and a third resident within one
    # in-game week." GATED LIKE THE RESTART: a verdict from before the third
    # resident existed has no reach line, and that is a NOTE in capitals.
    #
    # WHAT IS A FAULT AND WHAT IS A FINDING. The mill's own rule says what one
    # retelling carries - confidence x tie x hop decay, dropped under the
    # floor - and the line prints that arithmetic beside what the mill did.
    # If they DISAGREE, the build is wrong and it is a fault. If they agree
    # that it does not reach him, the gate is not met at today's numbers:
    # that is a measurement for Jafar, not a broken build, and it is a note.
    rch = lines_named(text, "reach")
    if not rch:
        notes.append("reach=NOT-IN-THIS-VERDICT/no-third-resident-measured")
    else:
        rr = rch[0]
        def rnum(k, cast=float):
            try:
                return cast(rr.get(k, ""))
            except ValueError:
                return None
        third = rr.get("thirdResident")
        would, floor = rnum("wouldArrive"), rnum("floor")
        margin = rr.get("marginOverFloor", "")
        # THE SIGN OF THE UNROUNDED MARGIN DECIDES, not the two printed
        # numbers: wouldArrive is printed to three places and the floor to
        # two, so a true 0.1996 prints as 0.200 and would read as clearing
        # a floor the mill correctly refused it at. The margin is worked
        # before rounding and printed with its sign.
        should = margin.startswith("+")
        # AN UNREADABLE LINE IS A FAULT, not an honest miss (independent
        # check, finding 5): with wouldArrive missing, "should" used to come
        # out False and a NOT-REACHED became a note.
        if would is None or floor is None or would != would or margin[:1] not in ("+", "-"):
            faults.append("the reach line's arithmetic is unreadable (wouldArrive=%s floor=%s "
                          "marginOverFloor=%s)" % (rr.get("wouldArrive"), rr.get("floor"), margin))
        # THE STREET'S OWN NUMBERS, read off round 2 of the same run rather
        # than typed here: the mate is tied at the tie the shopkeeper and the
        # lad have, against the floor the mill used for them (finding 4).
        r2 = rounds.get("2", {})
        if rr.get("thirdTie") != r2.get("tie"):
            faults.append("the mate is tied at %s, not the street's own %s from round 2"
                          % (rr.get("thirdTie"), r2.get("tie")))
        if rr.get("floor") != r2.get("minShare"):
            faults.append("the reach floor %s is not the floor round 2 ran at (%s)"
                          % (rr.get("floor"), r2.get("minShare")))
        # THE WEEK IS RECOMPUTED FROM THE HOURS, never taken from the flag
        # beside them (finding 3), and the hours come off his memory.
        try:
            hours = int(rr.get("hoursAfterCrime", ""))
        except ValueError:
            hours = None
        week_ok = hours is not None and 0 <= hours <= 168
        if rr.get("withinOneWeek") != ("yes" if week_ok else "no"):
            faults.append("withinOneWeek=%s disagrees with hoursAfterCrime=%s"
                          % (rr.get("withinOneWeek"), rr.get("hoursAfterCrime")))
        # A MATE WHO NEVER APPEARED, OR WAS NOT WITH THE LAD, IS SAID SO
        # (finding 7), before anything reads it as the mill disagreeing.
        if rr.get("thirdBody") != "spawned":
            faults.append("the mate never appeared (thirdBody=%s)" % rr.get("thirdBody"))
        elif rr.get("thirdTogether") != "yes" and third != "NOT-RUN":
            faults.append("the mate and the lad met %s m apart, not together"
                          % rr.get("thirdPairMetres"))
        if third == "NOT-RUN":
            faults.append("the third resident's meeting never ran (thirdResident=NOT-RUN)")
        elif third == "REACHED":
            if rnum("thirdHops", int) != 2:
                faults.append("the third resident was reached at %s hops, not by a second "
                              "retelling (2) - he was tied to somebody he should not be"
                              % rr.get("thirdHops"))
            holding = rnum("residentsHolding", int)
            if holding is None or holding < 3:
                faults.append("the third resident was reached but only %s resident(s) hold "
                              "crime A" % rr.get("residentsHolding"))
            if not week_ok:
                faults.append("reached, but not within one in-game week (hoursAfterCrime=%s)"
                              % rr.get("hoursAfterCrime"))
            if not should:
                faults.append("the third resident was reached although the mill's own rule "
                              "says %s is under the floor %s" % (rr.get("wouldArrive"), rr.get("floor")))
        elif third == "NOT-REACHED":
            if should:
                faults.append("the mill's own rule says %s clears the floor %s and the third "
                              "resident was not reached - the mill and its arithmetic disagree"
                              % (rr.get("wouldArrive"), rr.get("floor")))
            else:
                notes.append("REACH GATE NOT MET AT TODAY'S NUMBERS: %s under the floor %s"
                             % (rr.get("wouldArrive"), rr.get("floor")))
        else:
            faults.append("the reach line says thirdResident=%s" % third)
        notes.append("reach=third %s, %s resident(s) hold A, %s hours after, margin %s"
                     % (third, rr.get("residentsHolding"), rr.get("hoursAfterCrime"),
                        rr.get("marginOverFloor")))

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

    # ---- the arrest, once the probe carries one -----------------------------
    # ROADMAP's stage-3 gate: "arrest reachable from live play, its callers
    # outside Core counted and printed rather than zero". GATED EXACTLY AS
    # THE CONTROL AND THE RESTART ARE: a verdict from before the constable
    # existed has no arrest line, and that is a NOTE in capitals rather than a
    # pass or a failure - the lesson of 22 September, when a selftest whose
    # fixture was a file CI rewrites went red on the runner and green here.
    ar = lines_named(text, "arrest")
    if not ar:
        notes.append("arrest=NOT-IN-THIS-VERDICT/nothing-measured-about-the-end-of-the-story")
    else:
        a = ar[0]
        if a.get("arrest") != "RAN":
            faults.append("THE ARREST WAS NOT ASKED (arrest=%s): the end of the story is "
                          "still unreachable from live play" % a.get("arrest"))
        else:
            try:
                calls = int(a.get("confrontCalls", ""))
            except ValueError:
                calls = None
            if calls is None or calls < 2:
                faults.append("the arrest was asked %s time(s); it must be asked for the "
                              "witnessed crime AND the control" % a.get("confrontCalls"))
            if not a.get("callSite"):
                faults.append("the arrest line names no caller, and a caller with no "
                              "name is a count anybody could have typed")
            if a.get("constableBody") != "spawned":
                faults.append("the constable's body was %s, so nothing he saw was "
                              "measured" % a.get("constableBody"))
            # WHAT A MUST BE IS WORKED OUT HERE, FROM WHO HE IS - never taken
            # from the verdict's own expectA. The first version believed the
            # run about itself, and the independent check of 22 September
            # showed what that lets through: familiarity 0.35 with
            # expectA=NothingToArrest and outcomeA=NothingToArrest passed, a
            # run in which a constable who knows him watched it and nobody was
            # arrested. RecognitionFamiliarity is 0.35 in both engines.
            try:
                fam = float(a.get("constableFamiliarity", ""))
            except ValueError:
                fam = None
            # AND THE RULING HAS TO HAVE REACHED THE READING. A familiarity
            # that was set in the header and dropped on the way to the
            # constable's reading falls back to a stranger's 0.0, and without
            # this comparison would pass as if a stranger had been ruled.
            try:
                ruled = float(a.get("constableRuled", ""))
            except ValueError:
                ruled = None
            if ruled is None:
                faults.append("the arrest line does not say what was ruled for the constable "
                              "(constableRuled=%s)" % a.get("constableRuled"))
            elif fam is not None and abs(ruled - fam) > 1e-6:
                faults.append("THE RULING NEVER REACHED THE CONSTABLE: %s was ruled and his "
                              "reading used %s" % (a.get("constableRuled"), a.get("constableFamiliarity")))
            if fam is None:
                faults.append("the arrest line does not say who the constable is to him "
                              "(constableFamiliarity=%s), so what he should have done "
                              "cannot be worked out" % a.get("constableFamiliarity"))
                want = None
            else:
                want = "Arrest" if fam >= 0.35 - 1e-9 else "NothingToArrest"
            if want and a.get("expectA") != want:
                faults.append("the run's own expectA=%s disagrees with what familiarity %s "
                              "requires (%s): the probe's arithmetic and this check's have "
                              "come apart" % (a.get("expectA"), a.get("constableFamiliarity"), want))
            if want == "NothingToArrest":
                notes.append("NO ARREST CAN HAPPEN UNDER THIS RULING: the constable is a stranger "
                             "(familiarity %s), and a stranger cannot place him. The stage-3 "
                             "gate is not met by this run, by design." % a.get("constableFamiliarity"))
            got = a.get("outcomeA")
            if want and got != want:
                faults.append("crime A: the constable should have answered %s and answered "
                              "%s (rung %s, can see the actor %s, occluded %s by %s, "
                              "watched %s s)"
                              % (want, got, a.get("rungA"), a.get("hasActorA"),
                                 a.get("occludedA"), a.get("blockerA"),
                                 a.get("watchSecondsA")))
            # AND B NEVER ARRESTS, whoever he is: it is the control, and a
            # constable arresting for a crime he could not see is Core
            # inventing a sighting.
            if a.get("outcomeB") != "NothingToArrest":
                faults.append("THE CONTROL ARRESTED: crime B answered %s, and the "
                              "constable was behind the terrace for it"
                              % a.get("outcomeB"))
            # AND FOR THE RIGHT REASON. B's NothingToArrest proves something
            # about SEEING only if the terrace is what stopped him - not a
            # glance too short or a face turned away, which the probe's own
            # comment says the control must not rely on.
            if a.get("occludedB") != "1":
                faults.append("the control answered NothingToArrest without the terrace "
                              "between them (occludedB=%s), so it proves nothing about "
                              "seeing" % a.get("occludedB"))
        notes.append("arrest=%s; A %s (expected %s), B %s; asked %s time(s) from %s"
                     % (a.get("arrest"), a.get("outcomeA"), a.get("expectA"),
                        a.get("outcomeB"), a.get("confrontCalls"), a.get("callSite")))

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
            # THE PAIR ACROSS THE RESTART, 22 September: the crime somebody
            # saw must come back with every rumour it had, and the crime
            # nobody could see must still have none - the control holding
            # nothing AFTER the reload, which is what the list asks. Gated on
            # the fields being there, loud when they are not, like the line.
            if "rumoursAboutBAfter" not in r:
                notes.append("restartPair=NOT-IN-THIS-VERDICT/the-control-was-not-"
                             "counted-after-the-reload")
            else:
                ab, aa = num("rumoursAboutABefore"), num("rumoursAboutAAfter")
                bb, ba = num("rumoursAboutBBefore"), num("rumoursAboutBAfter")
                if aa is None or ab is None or aa != ab:
                    faults.append("the witnessed crime's rumours did not all survive the "
                                  "restart (%s before, %s after)"
                                  % (r.get("rumoursAboutABefore"), r.get("rumoursAboutAAfter")))
                elif aa < 1:
                    faults.append("there was no rumour about the witnessed crime to survive")
                if ba is None or ba != 0:
                    faults.append("the unwitnessed control holds a rumour after the reload "
                                  "(rumoursAboutBAfter=%s)" % r.get("rumoursAboutBAfter"))
                if bb is None or bb != 0:
                    faults.append("the unwitnessed control held a rumour before the save "
                                  "(rumoursAboutBBefore=%s)" % r.get("rumoursAboutBBefore"))
                # THE MATE'S OWN RECORD, once the run has a mate.
                if "r3RumoursAfter" in r:
                    r3b, r3a = num("r3RumoursBefore"), num("r3RumoursAfter")
                    m3b, m3a = num("r3MemoryBefore"), num("r3MemoryAfter")
                    if r3a is None or r3b is None or r3a != r3b:
                        faults.append("the lad's mate lost rumours across the restart (%s before, "
                                      "%s after)" % (r.get("r3RumoursBefore"), r.get("r3RumoursAfter")))
                    if m3a is None or m3b is None or m3a != m3b:
                        faults.append("the lad's mate's memory changed across the restart (%s "
                                      "before, %s after)" % (r.get("r3MemoryBefore"), r.get("r3MemoryAfter")))
                    h3 = num("r3HopsAfter")
                    if r3a and h3 != 2:
                        faults.append("the lad's mate came back %s retellings out, not 2" % h3)
                notes.append("restartPair=A %s->%s, B %s->%s"
                             % (r.get("rumoursAboutABefore"), r.get("rumoursAboutAAfter"),
                                r.get("rumoursAboutBBefore"), r.get("rumoursAboutBAfter")))
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
               "n2HopsAfter=1 memoryTextStable=yes rumoursAboutABefore=2 "
               "rumoursAboutAAfter=2 rumoursAboutBBefore=0 rumoursAboutBAfter=0")
    if real:
        # THE FIXTURE IS THE ONLY RESTART LINE, the same isolation the control
        # and the arrest already have. The landed verdict carries a restart
        # line of its own and judge reads the FIRST; these cases passed only
        # because str.replace doctored the real line too, whose values
        # happened to match. A field the real line lacks - the pair, until a
        # probe run carries it - would have been doctored in the fixture alone
        # and never looked at.
        base_rt = LF.join(l for l in real.split(LF) if not l.startswith("restart="))
        ok_text = base_rt.rstrip(chr(10)) + chr(10) + GOOD_RT + chr(10)
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
                ("the-control-gained-a-rumour-across-the-restart",
                 "rumoursAboutBAfter=0", "rumoursAboutBAfter=1"),
                ("the-witnessed-crime-lost-a-rumour-across-the-restart",
                 "rumoursAboutAAfter=2", "rumoursAboutAAfter=1"),
                ("nothing-about-the-witnessed-crime-survived",
                 "rumoursAboutAAfter=2", "rumoursAboutAAfter=0"),
        ):
            faults, _n = judge(ok_text.replace(old_v, new_v), head_sha(real))
            check("reject/%s-is-caught" % name, bool(faults))

    # THE REACH RULES, on a fixture that is the ONLY reach line.
    GOOD_REACH = ("reach=A residentsHolding=3 thirdResident=REACHED thirdBody=spawned "
                  "thirdTogether=yes thirdPairMetres=2.5 thirdHops=2 heardAt=D4-18h "
                  "hoursAfterCrime=78 withinOneWeek=yes thirdTie=0.60 wouldArrive=0.217 "
                  "floor=0.20 marginOverFloor=+0.017")
    if real:
        base_r = LF.join(l for l in real.split(LF) if not l.startswith("reach="))
        ok_r = base_r.rstrip(chr(10)) + chr(10) + GOOD_REACH + chr(10)
        faults, _n = judge(ok_r, head_sha(real))
        check("accept/a-good-reach-line-passes", not faults, "; ".join(faults[:2]))
        for name, old_v, new_v in (
                ("reached-at-one-hop", "thirdHops=2", "thirdHops=1"),
                ("reached-outside-the-week", "withinOneWeek=yes", "withinOneWeek=no"),
                ("the-mill-disagrees-with-its-rule", "thirdResident=REACHED", "thirdResident=NOT-REACHED"),
                ("the-meeting-never-ran", "thirdResident=REACHED", "thirdResident=NOT-RUN"),
                ("only-two-hold-it", "residentsHolding=3", "residentsHolding=2"),
                ("the-week-flag-lies", "hoursAfterCrime=78", "hoursAfterCrime=500"),
                ("tied-stronger-than-the-street", "thirdTie=0.60", "thirdTie=1.00"),
                ("a-lower-floor", "floor=0.20", "floor=0.10"),
                ("an-unreadable-margin", "marginOverFloor=+0.017", "marginOverFloor=nan"),
                ("the-mate-never-appeared", "thirdBody=spawned", "thirdBody=MISSING"),
                ("they-met-apart", "thirdTogether=yes", "thirdTogether=no"),
        ):
            faults, _n = judge(ok_r.replace(old_v, new_v), head_sha(real))
            check("reject/%s-is-caught" % name, bool(faults))
        # AND THE HONEST MISS IS NOT A FAULT: under the floor, not reached.
        miss = (GOOD_REACH.replace("thirdResident=REACHED", "thirdResident=NOT-REACHED")
                .replace("wouldArrive=0.217", "wouldArrive=0.180")
                .replace("marginOverFloor=+0.017", "marginOverFloor=-0.020")
                .replace("residentsHolding=3", "residentsHolding=2")
                .replace("heardAt=D4-18h", "heardAt=none")
                .replace("hoursAfterCrime=78", "hoursAfterCrime=none")
                .replace("withinOneWeek=yes", "withinOneWeek=no"))
        faults, notes_m = judge(base_r.rstrip(chr(10)) + chr(10) + miss + chr(10), head_sha(real))
        check("accept/a-miss-the-arithmetic-predicts-is-a-finding-not-a-fault",
              not faults, "; ".join(faults[:2]))
        # AND THE ROUNDING EDGE (finding 6): printed 0.200 against 0.20 with
        # a NEGATIVE margin is a correct refusal, not a disagreement.
        edge = miss.replace("wouldArrive=0.180", "wouldArrive=0.200").replace(
            "marginOverFloor=-0.020", "marginOverFloor=-0.000")
        faults, _n = judge(base_r.rstrip(chr(10)) + chr(10) + edge + chr(10), head_sha(real))
        check("accept/a-refusal-just-under-the-floor-is-not-a-disagreement",
              not faults, "; ".join(faults[:2]))

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

    # THE ARREST'S OWN RULES, on a verdict that carries the line - and ONLY
    # that line: any arrest line the landed verdict already has is stripped
    # first, so the fixture is the one being doctored. That is the exact fault
    # that reddened three probe runs on 22 September, in the control's cases.
    GOOD_ARREST = ("arrest=RAN confrontCalls=2 callSite=CrimeProbe.cpp/ResolveAndFile "
                   "constable=c1 constableRuled=0.35 constableFamiliarity=0.35 expectA=Arrest outcomeA=Arrest "
                   "rungA=4 hasActorA=1 occludedA=0 blockerA=none watchSecondsA=1.20 "
                   "cataloguesCoatA=1 outcomeB=NothingToArrest rungB=0 occludedB=1 "
                   "constableBody=spawned")
    if real:
        base_a = LF.join(l for l in real.split(LF) if not l.startswith("arrest="))
        ok_a = base_a.rstrip(chr(10)) + chr(10) + GOOD_ARREST + chr(10)
        faults, _n = judge(ok_a, head_sha(real))
        check("accept/a-good-arrest-line-passes", not faults, "; ".join(faults[:2]))
        stranger = (GOOD_ARREST.replace("constableRuled=0.35", "constableRuled=0.00")
                    .replace("constableFamiliarity=0.35", "constableFamiliarity=0.00")
                    .replace("expectA=Arrest", "expectA=NothingToArrest")
                    .replace("outcomeA=Arrest", "outcomeA=NothingToArrest")
                    .replace("rungA=4", "rungA=3"))
        faults, _n = judge(base_a.rstrip(chr(10)) + chr(10) + stranger + chr(10), head_sha(real))
        check("accept/a-stranger-ruling-that-cannot-arrest-passes", not faults,
              "; ".join(faults[:2]))
        for name, old_v, new_v in (
                ("the-arrest-was-never-asked", "arrest=RAN", "arrest=NOT-RUN"),
                ("the-control-arrested", "outcomeB=NothingToArrest", "outcomeB=Arrest"),
                ("a-constable-who-knows-him-let-him-go", "outcomeA=Arrest",
                 "outcomeA=NothingToArrest"),
                ("only-one-crime-was-asked-about", "confrontCalls=2", "confrontCalls=1"),
                ("the-constable-never-spawned", "constableBody=spawned", "constableBody=MISSING"),
                ("the-caller-has-no-name", "callSite=CrimeProbe.cpp/ResolveAndFile ", ""),
                # THE INDEPENDENT CHECK'S CASES, 22 September: a run that
                # agrees with itself about nobody being arrested.
                ("a-self-consistent-run-where-nobody-was-arrested",
                 "expectA=Arrest outcomeA=Arrest", "expectA=NothingToArrest outcomeA=NothingToArrest"),
                ("the-control-was-clean-for-the-wrong-reason", "occludedB=1", "occludedB=0"),
                ("the-line-hides-who-the-constable-is", "constableFamiliarity=0.35 ", ""),
                ("the-ruling-was-dropped-before-the-reading",
                 "constableFamiliarity=0.35 expectA=Arrest outcomeA=Arrest",
                 "constableFamiliarity=0.00 expectA=NothingToArrest outcomeA=NothingToArrest"),
        ):
            faults, _n = judge(base_a.rstrip(chr(10)) + chr(10)
                               + GOOD_ARREST.replace(old_v, new_v) + chr(10), head_sha(real))
            check("reject/%s-is-caught" % name, bool(faults))
        faults, notes = judge(base_a, head_sha(real))
        check("accept/a-verdict-from-before-the-constable-is-a-note-not-a-fault",
              not any("ARREST" in f for f in faults)
              and any(n.startswith("arrest=NOT-IN-THIS-VERDICT") for n in notes),
              str(notes))

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
