#!/usr/bin/env python3
"""EVERY FILE THE SHOT VERDICT NAMES IS A FILE THE COMMIT WILL CARRY.

    python3 tools/verdict-shot-files.py                  # the live UE vignette verdict
    python3 tools/verdict-shot-files.py --verdict PATH   # any verdict with shot lines
    python3 tools/verdict-shot-files.py --selftest       # accepting case FIRST

WHY THIS EXISTS, MEASURED ON 16 SEPTEMBER AND NOT SUSPECTED.

`production/d1-probe/ue-vignette-verdict.txt` names 43 shot files, each with a
byte count the engine measured. Four of them had never been in the repository,
on any commit, from any run:

    git log --oneline --all -- 'production/d1-probe/ue-pinset_night_*.png'  0
    git log --oneline --all -- 'production/d1-probe/ue-vign_*.png'         29

The four are `ue-pinset_night_1.png` through `_4.png`. The probe collects and
stages its frames BY NAME PREFIX, `ue-vign_*.png`, which is ci.md's rule obeyed
exactly, and that rule is right: `git add <directory>` is how a failed run
commits its stale checkout's files as its own evidence. But a by-name stage
goes blind the moment a new shot family arrives under a name no pattern covers,
and nothing was watching the join. Two of the four had rendered perfectly that
run, at 1367920 and 1278041 bytes, and were thrown away beside the two that
came back blank. The queue item asking for the blank ones to be diagnosed could
not be done, because the pictures did not exist.

A WIDER GLOB IS NOT THE FIX, IT IS THE SAME BET PLACED AGAIN. The fix is that
the join gets watched by something. The verdict is the list of what the run
says it produced; the index is the list of what the commit will carry; a name
in the first and not the second is a frame nobody can ever open. That
comparison is this file, and it does not care what the glob is.

WHAT IT REFUSES TO CONFLATE.
  ABSENT and UNTRACKED are separate counts because they are separate faults.
  A frame that never rendered is the engine's problem. A frame sitting on disk
  that git does not know about is the staging step's problem, and that is the
  one that has been happening here.

  A VERDICT THAT MEASURED NOTHING IS NOT A CLEAN RUN. The probe writes a
  NOTHING-EMITTED placeholder when it never reached a capture, and a
  placeholder names no files at all. `0 missing of 0 named` would read green
  for ever, so that case prints the words `nothing-measured` instead, and rides
  a separate key so no reader has to infer it (rule 3b).

  A SHOT LINE WITH NO `file=` IS NOT A NAMED FILE. It is counted, on the same
  done line, as `shotLinesWithoutFile`, so the named count always ships the
  population it was drawn from.

WHAT THE NUMBERS ARE STATISTICS OF: all of them are CUMULATIVE COUNTS OVER ONE
VERDICT FILE. Not peaks, not medians, not last-wins. `shotFilesStat=` on the
done line says so in the output rather than only here, because a number nobody
has read yet is the one most likely to be quoted as the wrong kind.
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

# ONE IMPLEMENTATION PER IDEA: the truncation notice and the never-measured
# words already exist in this repo and are imported, never re-typed.
sys.path.insert(0, str(HERE))                        # tools/capsay.py
from capsay import cap, NOTHING_MEASURED             # noqa: E402

DEFAULT_VERDICT = ROOT / "production" / "d1-probe" / "ue-vignette-verdict.txt"

# EXIT CODES, ONE PER OUTCOME, so a caller can tell the three apart without
# reading prose. A report that ends in the wrong exit code costs twenty
# minutes before somebody notices which thing happened.
EXIT_OK = 0            # every named file is on disk and in the index
EXIT_MISSING = 1       # at least one named file is absent, or present untracked
EXIT_NO_VERDICT = 2    # could not look: there is no verdict file to read
EXIT_NAMED_NONE = 3    # the verdict claims a capture and still names no file

# THE SPELLINGS THE PROBE WRITES WHEN A RUN MEASURED NOTHING, quoted from
# .github/workflows/ledger-probe-unreal.yml rather than paraphrased. A marker
# matched loosely is a marker that stops matching the day somebody rewords the
# sentence, and both placeholders in that workflow carry both of these.
NO_CAPTURE = ("captureStatus=NOTHING-MEASURED", "NOTHING MEASURED")

SHOT_LINE = re.compile(r"^shot\s+(\S+)")
FILE_RX = re.compile(r"\bfile=(\S+)")
STATUS_RX = re.compile(r"\bstatus=(\S+)")
BYTES_RX = re.compile(r"\bbytes=(\d+)")
STAMP_RX = re.compile(r"\b([0-9a-f]{7,40})\s+@(\d+)")

# HOW MANY FAULTS GET A LINE EACH before the cap bites. The cap announces
# itself through `capsay.cap`, which appends `(+N more of M)`; there is no
# second truncation in this file.
DETAIL_KEEP = 12
DETAIL_WIDTH = 200

# A WAIVER LIVED HERE AND HAS EXPIRED ON ITS OWN, WHICH IS WHY IT WAS BUILT
# THAT WAY. From 16 September it forgave four named-but-absent frames,
# `ue-pinset_night_1.png` through `_4.png`, and only while the verdict on disk
# was the one measured by run c738797: the staging repair for them could not
# land while this check was red, so the forgiveness was pinned to that ONE RUN
# rather than to the names, and nobody had to remember to delete it. Run 48
# landed the four frames at 4e257ee, the pin stopped matching by itself, and
# the machinery is deleted here rather than left as a constant nobody dares
# remove. `git log -S WAIVED_ABSENT_FILES` has the whole of it.


def _nospace(s):
    """A value safe for a `key=value` channel every reader splits on
    whitespace. Paths in this project have no spaces; a scratch directory in a
    selftest can, and a silently truncated path is the failure this encodes
    around rather than risks."""
    return re.sub(r"\s", "%20", str(s))


def _git(cwd, args):
    try:
        p = subprocess.run(["git"] + args, cwd=str(cwd), capture_output=True,
                           text=True)
    except (OSError, ValueError):
        return 1, ""
    return p.returncode, p.stdout


def shot_rows(text):
    """Every `shot ` line's (shot id, file, status, bytes), in file order.

    READ OFF THE `shot ` LINES ONLY, never by a `grep -o 'file='` over the
    whole file. The header of a verdict is prose, and prose that happens to
    contain the token would be collected as a frame. That is the `verdict-read`
    incident in miniature: a value returned from a line the reader cannot name.
    """
    rows = []
    for n, line in enumerate(text.splitlines(), 1):
        m = SHOT_LINE.match(line)
        if not m:
            continue
        f = FILE_RX.search(line)
        s = STATUS_RX.search(line)
        b = BYTES_RX.search(line)
        rows.append({
            "line": n,
            "shot": m.group(1),
            "file": f.group(1) if f else None,
            "status": s.group(1) if s else "no-status",
            "bytes": b.group(1) if b else "no-bytes",
        })
    return rows


def read(verdict):
    """The whole reading for one verdict, as data. No printing here.

    Measurement arithmetic lives where the tests run, so the tally and the
    comparison are in this function and the strings are in `report_lines`;
    both are driven by `--selftest`."""
    vp = pathlib.Path(verdict)
    r = {
        "verdict": vp,
        "verdictExists": vp.is_file(),
        "run": None, "stamp": None,
        "captured": False,
        "shotLines": 0, "linesWithoutFile": 0,
        "named": 0, "present": 0, "tracked": 0, "untracked": 0, "missing": 0,
        "namedWithPath": 0,
        "faults": [],           # one dict per fault, in verdict order
        "trackedKnown": False,  # whether git could answer at all
    }
    if not vp.is_file():
        return r

    text = vp.read_text(encoding="utf-8", errors="replace")
    first = text.split("\n", 1)[0]
    m = STAMP_RX.search(first)
    if m:
        r["run"], r["stamp"] = m.group(1), m.group(2)
    # A CAPTURE IS CLAIMED UNLESS THE FILE SAYS IT MEASURED NOTHING. Stated
    # this way round on purpose: a verdict that has lost its banner reads as
    # claiming a capture, which is the direction that goes red rather than the
    # direction that goes quietly green.
    r["captured"] = not any(mark in text for mark in NO_CAPTURE)

    rows = shot_rows(text)
    r["shotLines"] = len(rows)

    vdir = vp.parent
    # THE INDEX, ASKED ONCE. 43 `git ls-files --error-unmatch` calls answer the
    # same question 43 times and cost 43 processes; one listing of the
    # directory is the same answer. `git ls-files` reads the INDEX, which is
    # what the next commit will carry, and that is the question being asked:
    # not "is it in HEAD" but "would committing now include it".
    code, out = _git(vdir, ["rev-parse", "--show-toplevel"])
    tracked = None
    if code == 0 and out.strip():
        top = pathlib.Path(out.strip())
        code, out = _git(top, ["ls-files", "--full-name", "--",
                               os.path.relpath(str(vdir), str(top))])
        if code == 0:
            tracked = set(l.strip() for l in out.splitlines() if l.strip())
            r["trackedKnown"] = True
            r["top"] = top

    for row in rows:
        name = row["file"]
        if name is None:
            r["linesWithoutFile"] += 1
            continue
        r["named"] += 1
        if "/" in name or "\\" in name:
            # ANNOUNCED RATHER THAN NORMALISED AWAY. The engine writes a bare
            # leaf (`ue-<shotId>.png`), so a separator here means the emitter
            # changed shape and the reader should know before the count is
            # believed.
            r["namedWithPath"] += 1
        target = vdir / name
        on_disk = target.is_file()
        in_index = None
        if tracked is not None and "top" in r:
            rel = os.path.relpath(str(target), str(r["top"])).replace(os.sep, "/")
            in_index = rel in tracked
        if on_disk:
            r["present"] += 1
        if in_index:
            r["tracked"] += 1
        if on_disk and in_index is False:
            r["untracked"] += 1
        if not on_disk:
            r["missing"] += 1
        if on_disk and in_index is not False:
            continue
        # THE FAULT NAMES BOTH HALVES AT ONCE. "absent" and "untracked" are
        # different repairs: one is the engine or the copy step, the other is
        # the staging step, and a single word would send the reader to the
        # wrong one half the time.
        if not on_disk and in_index:
            why = "absent-from-disk-but-in-the-index"
        elif not on_disk:
            why = "absent-from-disk-and-not-in-the-index"
        else:
            why = "on-disk-but-not-in-the-index"
        r["faults"].append({**row, "why": why})

    return r


def report_lines(r):
    """The printed report for one reading, as a list of lines.

    THE SHAPE IS FIXED: per-shot faults on their own lines, whole-run counts on
    the `done` line and nowhere else. A reader grepping `shotFilesNamed` across
    two lines would otherwise be reading two moments as one."""
    L = []
    vrel = _nospace(_rel(r["verdict"]))

    if not r["verdictExists"]:
        L.append("NOTHING MEASURED - there is no verdict at %s to read, so no "
                 "shot file was examined; this is not a clean tree, it is an "
                 "unexamined one." % vrel)
        L.append("done shotFilesVerdict=%s verdictRun=%s shotFilesReading=%s "
                 "verdictShotLines=0 shotLinesWithoutFile=0 shotFilesNamed=0 "
                 "shotFilesPresent=0 shotFilesMissing=0 shotFilesTracked=0 "
                 "shotFilesUntracked=0 shotFilesStat=cumulative-over-one-verdict"
                 % (vrel, NOTHING_MEASURED, NOTHING_MEASURED))
        return L

    if r["faults"]:
        detail = ["shotFileFault file=%s shot=%s verdictStatus=%s "
                  "verdictBytes=%s verdictLine=%d fault=%s"
                  % (_nospace(f["file"]), _nospace(f["shot"]), _nospace(f["status"]),
                     _nospace(f["bytes"]), f["line"], f["why"])
                  for f in r["faults"]]
        # EVERY CAP ANNOUNCES ITSELF, and this is the project's one
        # implementation of that: `capsay.cap` appends `(+N more of M)` and
        # appends nothing when it did not bite.
        L.extend(cap(detail, keep=DETAIL_KEEP, width=DETAIL_WIDTH,
                     sep="\n").split("\n"))

    reading = "cumulative-over-one-verdict"
    if r["named"] == 0 and not r["captured"]:
        reading = NOTHING_MEASURED
        L.append("NOTHING MEASURED - the verdict at %s says it captured "
                 "nothing and names no shot file, so a zero here counts "
                 "nothing examined rather than nothing wrong." % vrel)
    elif r["named"] == 0:
        L.append("SHOT VERDICT NAMES NO FILE AT ALL while claiming a capture: "
                 "%d shot line(s), %d of them with no file= on them. The "
                 "emitter changed shape or the grep that builds this stopped "
                 "matching." % (r["shotLines"], r["linesWithoutFile"]))

    L.append("done shotFilesVerdict=%s verdictRun=%s shotFilesReading=%s "
             "verdictCaptured=%s verdictShotLines=%d shotLinesWithoutFile=%d "
             "shotFilesNamed=%d shotFilesPresent=%d shotFilesMissing=%d "
             "shotFilesTracked=%s shotFilesUntracked=%s shotFilesNamedWithPath=%d "
             # `shotFilesFaults` is the number the exit code is made of,
             # printed so nobody has to derive it - and it cannot be derived
             # from the per-shot lines above, because the cap can truncate
             # those. It was `shotFilesUnwaivedFaults` until the waiver was
             # retired on 16 September; there is no waiver left to be un-.
             "shotFilesFaults=%d "
             "shotFilesStat=cumulative-over-one-verdict"
             % (vrel, _nospace(r["run"] or NOTHING_MEASURED), reading,
                "yes" if r["captured"] else "no",
                r["shotLines"], r["linesWithoutFile"], r["named"], r["present"],
                r["missing"],
                r["tracked"] if r["trackedKnown"] else NOTHING_MEASURED,
                r["untracked"] if r["trackedKnown"] else NOTHING_MEASURED,
                r["namedWithPath"], len(r["faults"])))
    return L


def _rel(p):
    try:
        return pathlib.Path(p).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def verdict_exit(r):
    """Which outcome this reading is. One code per outcome."""
    if not r["verdictExists"]:
        return EXIT_NO_VERDICT
    if r["faults"]:
        return EXIT_MISSING
    if r["named"] == 0 and r["captured"]:
        return EXIT_NAMED_NONE
    return EXIT_OK


# --------------------------------------------------------------- selftest
def _live_tracked(directory, want):
    """Up to `want` files git reports TRACKED in `directory` and that are on
    disk right now, name-sorted so the pick is stable.

    THE ACCEPTING FIXTURE'S SUPPLY, AND IT ASKS THE INDEX RATHER THAN A GLOB.
    A live-tree fixture may assert INVARIANTS and must not assert today's
    incidental values, so nothing here names a shot family, a file count or a
    run: it takes whatever is tracked, and the caller derives its expected
    counts from HOW MANY came back. Names carrying whitespace are dropped
    because the fixture writes them into a `key=value` channel.
    """
    code, out = _git(directory, ["ls-files", "--", "."])
    if code != 0:
        return []
    names = sorted(set(l.strip() for l in out.splitlines()
                       if l.strip() and "/" not in l.strip()
                       and not re.search(r"\s", l.strip())))
    return [n for n in names if (directory / n).is_file()][:want]


def _write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _verdict_text(rows, captured=True, run="abc1234"):
    """A verdict built from (shotId, fileName) pairs, in the live file's shape."""
    L = ["# UE vignette shot %s @1789517651" % run,
         "# Line 1 names the commit this was measured on.",
         ""]
    if not captured:
        L += ["sceneStatus=NOTHING-EMITTED piecesEmitted=0/0",
              "captureStatus=NOTHING-MEASURED shotsWrote=0/0 shotsBlank=0/0",
              "NOTHING MEASURED - no frame of the street was taken on this commit."]
    for i, (sid, fname) in enumerate(rows):
        L.append("shot %s camera=cam_A condition=overcast_day status=WROTE "
                 "px=1280x720 file=%s bytes=%d shotBlank=no"
                 % (sid, fname, 1000 + i))
    L.append("shotReached=end")
    return "\n".join(L) + "\n"


def selftest():
    """Both outcomes watched, ACCEPTING CASE FIRST (CLAUDE.md rule 5b).

    THE ACCEPTING FIXTURE IS THE LIVE REPOSITORY. Real files that are on disk
    and in the index today are named by a verdict this builds, so the case this
    tool must let through is made of assets somebody would have to delete to
    break. THE REJECTING FIXTURES ARE SYNTHETIC, naming files that exist
    nowhere, so doing the work this tool asks for (landing the frames a verdict
    names) can never make the selftest fail.

    AND A LIVE-TREE FIXTURE ASSERTS INVARIANTS, NEVER TODAY'S VALUES. This is
    the lesson the first version of this file paid for: it also asserted WHICH
    RUN the live verdict was measured on, and the morning the missing frames
    landed, doing the work the tool exists to prompt turned the tool red. No
    fixture below asserts a run sha, a file count the next probe run changes,
    or which shots exist; the live counts are derived from the files git names
    at the moment the fixture is built.

    The expensive failure for a checker is the validator nothing survives, so
    the first two fixtures below, the live tree and a verdict that honestly
    measured nothing, are both cases that must come back GREEN.
    """
    ok, bad = 0, []

    def want(label, got, expect):
        nonlocal ok
        if got == expect:
            ok += 1
            print("  ok   %-58s %r" % (label, got))
        else:
            bad.append("%s: got %r, wanted %r" % (label, got, expect))
            print("  FAIL %-58s %r  wanted %r" % (label, got, expect))

    def want_in(label, needle, hay):
        nonlocal ok
        if needle in hay:
            ok += 1
            print("  ok   %-58s contains %r" % (label, needle))
        else:
            bad.append("%s: %r not in %r" % (label, needle, hay[:400]))
            print("  FAIL %-58s missing %r" % (label, needle))

    def want_not_in(label, needle, hay):
        nonlocal ok
        if needle not in hay:
            ok += 1
            print("  ok   %-58s omits %r" % (label, needle))
        else:
            bad.append("%s: %r unexpectedly in %r" % (label, needle, hay[:400]))
            print("  FAIL %-58s contains %r" % (label, needle))

    print("verdict-shot-files selftest - ACCEPTING CASES FIRST (a gate that")
    print("nothing survives proves nothing when it is red)\n")

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="vsf-selftest-"))

    # ---- ACCEPTING 1: the live repository's own tracked files, named by a
    # verdict written beside them. Real paths, the real index, really here.
    #
    # THE FILES ARE WHATEVER GIT NAMES, AND THE COUNTS COME FROM THAT LIST.
    # An earlier version globbed one shot family out of production/d1-probe and
    # demanded three of them; that is a count the next probe run moves and a
    # family name the next spec renames, in a fixture whose whole job is to be
    # unbreakable by doing the work. This directory holds THIS FILE, tracked,
    # so the supply cannot run dry, and nothing in production/ is written to.
    live = _live_tracked(HERE, want=3)
    liveN = len(live)
    # THE DENOMINATOR RIDES THE LABEL. A fixture that quietly found nothing to
    # examine would print the same `ok` as one that examined three files.
    want("live tracked: fixture built from %d live file(s), needs >=1" % liveN,
         liveN >= 1, True)
    if liveN:
        acc = HERE / ".selftest-accept-verdict.txt"
        # WRITTEN BESIDE THE FILES AND REMOVED AGAIN. It has to sit in a real
        # tracked directory because the whole question is about real paths and
        # the real index; it is deleted in the `finally` below either way.
        try:
            _write(acc, _verdict_text([("selftest_live_%d" % i, name)
                                       for i, name in enumerate(live, 1)]))
            r = read(acc)
            text = "\n".join(report_lines(r))
            want("live tracked: named", r["named"], liveN)
            want("live tracked: present", r["present"], liveN)
            want("live tracked: missing", r["missing"], 0)
            want("live tracked: tracked (git answered)", r["tracked"], liveN)
            want("live tracked: untracked", r["untracked"], 0)
            want("live tracked: exit code is OK", verdict_exit(r), EXIT_OK)
            want_in("live tracked: done line ships the denominator",
                    "shotFilesNamed=%d shotFilesPresent=%d shotFilesMissing=0"
                    % (liveN, liveN), text)
            want_not_in("live tracked: a clean run says no cap bit",
                        "more of", text)
            want_not_in("live tracked: a clean run is not nothing-measured",
                        NOTHING_MEASURED, text)
        finally:
            acc.unlink(missing_ok=True)

    # ---- ACCEPTING 2: a verdict that honestly measured nothing is GREEN and
    # says the words. Red here would be a ratchet: every local commit would be
    # blocked by a probe run that failed on somebody else's machine, for a
    # join that does not exist when nothing was captured.
    none_v = tmp / "nothing" / "ue-vignette-verdict.txt"
    _write(none_v, _verdict_text([], captured=False))
    r = read(none_v)
    text = "\n".join(report_lines(r))
    want("measured nothing: exit code is OK", verdict_exit(r), EXIT_OK)
    want("measured nothing: named", r["named"], 0)
    want_in("measured nothing: prints the words", NOTHING_MEASURED, text)
    want_in("measured nothing: and says so in prose", "NOTHING MEASURED", text)
    want_in("measured nothing: verdictCaptured=no", "verdictCaptured=no", text)

    # ---- REJECTING 1: a name that exists nowhere. SYNTHETIC on purpose: it
    # can never be satisfied by doing the work, so it cannot rot into a
    # fixture somebody has to keep alive.
    rej = tmp / "reject" / "ue-vignette-verdict.txt"
    _write(rej, _verdict_text([("selftest_nosuchshot",
                                "ue-selftest_nosuchshot_9x9.png")]))
    r = read(rej)
    text = "\n".join(report_lines(r))
    want("a file that exists nowhere: exit code is MISSING",
         verdict_exit(r), EXIT_MISSING)
    want("a file that exists nowhere: missing count", r["missing"], 1)
    want("a file that exists nowhere: named count", r["named"], 1)
    want_in("a file that exists nowhere: it is NAMED in the output",
            "file=ue-selftest_nosuchshot_9x9.png", text)
    want_in("a file that exists nowhere: the fault says which half",
            "fault=absent-from-disk", text)

    # ---- REJECTING 2: rendered, on disk, and never staged. This is the exact
    # shape of the live fault and it needs its own scratch repository, because
    # "on disk" and "in the index" are the two halves that must not be one
    # number twice: here one moves and the other does not.
    repo = tmp / "scratch-repo"
    (repo / "shots").mkdir(parents=True, exist_ok=True)
    _git(repo, ["init", "-q"])
    _git(repo, ["config", "user.email", "selftest@ledger.local"])
    _git(repo, ["config", "user.name", "selftest"])
    (repo / "shots" / "ue-staged.png").write_bytes(b"\x89PNG\r\n\x1a\n staged")
    _git(repo, ["add", "-A", "--", "shots/ue-staged.png"])
    (repo / "shots" / "ue-unstaged.png").write_bytes(b"\x89PNG\r\n\x1a\n loose")
    both = repo / "shots" / "ue-vignette-verdict.txt"
    _write(both, _verdict_text([("staged", "ue-staged.png"),
                                ("unstaged", "ue-unstaged.png")]))
    r = read(both)
    text = "\n".join(report_lines(r))
    want("on disk but unstaged: git answered at all", r["trackedKnown"], True)
    want("on disk but unstaged: present counts both", r["present"], 2)
    want("on disk but unstaged: missing is zero", r["missing"], 0)
    want("on disk but unstaged: untracked is one", r["untracked"], 1)
    want("on disk but unstaged: exit code is MISSING",
         verdict_exit(r), EXIT_MISSING)
    want_in("on disk but unstaged: the fault says which half",
            "fault=on-disk-but-not-in-the-index", text)
    want_not_in("on disk but unstaged: the staged one is not a fault",
                "file=ue-staged.png", text)

    # ---- REJECTING 3: no verdict at all is NOT a pass. Exit 2, its own code,
    # because "I could not look" and "I looked and it was clean" are the two
    # readings this project keeps confusing for each other.
    r = read(tmp / "no-such-dir" / "ue-vignette-verdict.txt")
    text = "\n".join(report_lines(r))
    want("no verdict at all: exit code is NO_VERDICT",
         verdict_exit(r), EXIT_NO_VERDICT)
    want_in("no verdict at all: prints the words", NOTHING_MEASURED, text)

    # ---- REJECTING 4: a verdict claiming a capture that names no file is its
    # own outcome. A grep that stopped matching produces exactly this and it
    # must not read as a clean zero.
    empty = tmp / "claims" / "ue-vignette-verdict.txt"
    _write(empty, "# UE vignette shot abc1234 @1\n\nshot lonely camera=cam_A "
                  "status=NO-FILE\nshotReached=end\n")
    r = read(empty)
    text = "\n".join(report_lines(r))
    want("claims a capture, names nothing: exit code is NAMED_NONE",
         verdict_exit(r), EXIT_NAMED_NONE)
    want("claims a capture, names nothing: the line is still counted",
         r["shotLines"], 1)
    want("claims a capture, names nothing: and counted as file-less",
         r["linesWithoutFile"], 1)

    # ---- THE CAP ANNOUNCES ITSELF WHEN IT BITES, and stays silent when it
    # does not. Both halves, because a cap that stamps its clause on
    # everything trains readers to skip the clause that matters.
    many = tmp / "many" / "ue-vignette-verdict.txt"
    n = DETAIL_KEEP + 7
    _write(many, _verdict_text([("selftest_gone_%d" % i,
                                 "ue-selftest_gone_%d.png" % i)
                                for i in range(n)]))
    r = read(many)
    text = "\n".join(report_lines(r))
    want("%d faults: all are counted" % n, r["missing"], n)
    want_in("%d faults: the cap says it bit" % n,
            "(+%d more of %d)" % (n - DETAIL_KEEP, n), text)
    want("%d faults: only the cap's worth are shown" % n,
         text.count("shotFileFault "), DETAIL_KEEP)

    # ---- NO VALUE CARRIES A SPACE, on any line this prints, in any outcome.
    # Every reader in this project splits on whitespace and truncates silently.
    spaced = []
    for label, rr in (("live-shaped", read(many)), ("nothing", read(none_v))):
        for line in report_lines(rr):
            if line.startswith("NOTHING MEASURED") or line.startswith("SHOT "):
                continue          # prose lines are prose, not a key=value channel
            for tok in line.split():
                if "=" in tok and " " in tok.split("=", 1)[1]:
                    spaced.append("%s: %s" % (label, tok))
    want("no key=value on a record line carries a space", spaced, [])

    # ---- WIRED: the modes this file advertises reach their functions. Rule 6
    # in miniature, and it costs one read of this file.
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    want("--selftest and --verdict both reach code",
         ("a.selftest" in src and "selftest()" in src
          and "read(a.verdict)" in src), True)

    import shutil as _sh
    _sh.rmtree(tmp, ignore_errors=True)

    print()
    for b in bad:
        print("FAIL " + b)
    print("verdict-shot-files selftest: %d passed, %d failed" % (ok, len(bad)))
    return 0 if not bad else 1


def main(argv=None):
    # A CORRECT RUN MUST SURVIVE `| head`. A traceback after a clean reading
    # costs twenty minutes before anybody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--verdict", default=str(DEFAULT_VERDICT),
                    help="the verdict to read (default: the UE vignette one)")
    ap.add_argument("--selftest", action="store_true",
                    help="accepting case first, then the rejecting ones")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    r = read(a.verdict)
    for line in report_lines(r):
        print(line)
    return verdict_exit(r)


if __name__ == "__main__":
    sys.exit(main())
